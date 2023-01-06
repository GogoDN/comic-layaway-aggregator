import requests

from fastapi import HTTPException

from ...config import settings


class SearchComicsClient:
    def __init__(self) -> None:
        self.url = f"{settings.env_url}/v1/searchComics"
        self.client = requests

    def get_comic_by_id(self, comic_id: int):
        url = self.url + f"/comics/{comic_id}"
        try:
            return self.client.get(url)
        except Exception:
            raise HTTPException(
                503, detail="Communication with services unavailable"
            )

    def get_multiple_comics(self, comic_ids: list[int]):
        comics = []
        comics_not_found = []
        for comic_id in comic_ids:
            response = self.get_comic_by_id(comic_id)
            if response.status_code == 200:
                comics.append(response.json())
            else:
                comics_not_found.append(comic_id)
        return comics, comics_not_found
