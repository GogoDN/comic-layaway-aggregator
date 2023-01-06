import httpx

from fastapi import HTTPException


class SearchComicsClient:
    def __init__(self) -> None:
        self.url = "http://localhost/v1/searchComics"
        self.client = httpx.AsyncClient(timeout=10.0)

    async def get_comic_by_id(self, comic_id: int):
        url = self.url + f"/comics/{comic_id}"
        try:
            return await self.client.get(url)
        except Exception:
            raise HTTPException(
                503, detail="Communication with services unavailable"
            )

    async def get_multiple_comics(self, comic_ids: list[int]):
        comics = []
        for comic_id in comic_ids:
            response = await self.get_comic_by_id(comic_id)
            if response.status_code == 200:
                comics.append(response.json())
            else:
                comics.append(None)
        return comics
