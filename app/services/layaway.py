from fastapi import HTTPException

from ..dependencies import AuthHeaders

from ..clients.internal.users import UsersClient
from ..clients.internal.comics import SearchComicsClient
from ..data.adapter import MongoDbClient


class LayawayService:
    def __init__(self) -> None:
        self.users_client = UsersClient()
        self.comics_client = SearchComicsClient()
        self.mongo_client = MongoDbClient()

    def __get_logged_user(self, headers: AuthHeaders):
        user = self.users_client.get_logged_user(headers.to_dict())
        if not user:
            raise HTTPException(401, "Invalid Credentials")
        return user

    def __validate_document_existence(self, user_id: str):
        return self.mongo_client.find_one_by_id_user(user_id) is not None

    def __validate_params(self, comic_ids: list, headers: AuthHeaders):
        user = self.__get_logged_user(headers)
        comics, comics_not_found = self.comics_client.get_multiple_comics(
            comic_ids
        )

        if len(comics_not_found) > 0:
            raise HTTPException(
                422,
                {
                    "message": "Comics not found in catalogue",
                    "comic_ids": comics_not_found,
                },
            )
        return user, comics

    def __get_layaway_template(self, user_id):
        return {"user_id": user_id, "comics": []}

    def __add_comics_to_layaway(self, comics: list, layaway: dict):
        layaway["comics"] = comics

    def __get_comic_titles_list(self, comics):
        return [comic.get("title") for comic in comics]

    def create_layaway(self, comic_ids: list, headers: AuthHeaders):
        user, comics = self.__validate_params(comic_ids, headers)

        if self.__validate_document_existence(user.get("id")):
            raise HTTPException(
                422,
                "There's an existing layaway for this user, "
                "use PATCH to update or PUT to overwrite",
            )

        comic_titles = self.__get_comic_titles_list(comics)

        layaway = self.__get_layaway_template(user.get("id"))
        self.__add_comics_to_layaway(comics, layaway)
        self.mongo_client.insert_layaway(layaway)
        return {
            "message": "Layaway created",
            "details": {"user": user.get("name"), "comics": comic_titles},
        }

    def update_layaway(self, comic_ids: list, headers: AuthHeaders):
        user, comics = self.__validate_params(comic_ids, headers)
        comic_titles = self.__get_comic_titles_list(comics)
        layaway = self.mongo_client.find_and_push_by_user_id(
            user.get("id"), comics
        )

        if not layaway:
            raise HTTPException(404, "Not Found")

        return {
            "message": "Layaway udpated",
            "details": {"user": user.get("name"), "comics": comic_titles},
        }

    def overwrite_layaway(self, comic_ids: list, headers: AuthHeaders):
        user, comics = self.__validate_params(comic_ids, headers)
        comic_titles = self.__get_comic_titles_list(comics)
        layaway = self.mongo_client.find_and_overwrite_by_user_id(
            user.get("id"), comics
        )

        if not layaway:
            raise HTTPException(404, "Not Found")

        return {
            "message": "Layaway udpated",
            "details": {"user": user.get("name"), "comics": comic_titles},
        }
