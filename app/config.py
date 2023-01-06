from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_db_conn_str: str
    env_url: str


settings = Settings()
