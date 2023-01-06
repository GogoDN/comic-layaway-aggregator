from fastapi import Header


class AuthHeaders:
    def __init__(
        self,
        x_user_id: str = Header(""),
        x_token: str = Header(""),
    ) -> None:
        self.x_user_id = x_user_id
        self.x_token = x_token

    def to_dict(self):
        return {
            "X-User-Id": self.x_user_id,
            "X-Token": self.x_token,
        }
