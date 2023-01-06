import httpx

from fastapi import HTTPException

from ...config import settings


class UsersClient:
    def __init__(self) -> None:
        self.url = f"{settings.env_url}/v1/users"
        self.client = httpx.AsyncClient(timeout=10.0)

    async def get_logged_user(self, headers):
        url = self.url + "/me"
        try:
            response = await self.client.get(url=url, headers=headers)
            if response.status_code == 200:
                return response.json()
            if response.status_code == 401:
                return
        except Exception:
            raise HTTPException(
                503, detail="Communication with services unavailable"
            )
