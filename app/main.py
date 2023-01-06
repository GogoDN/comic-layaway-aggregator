from fastapi import FastAPI

from .routers import layaway

from .scripts import db_bootstrap


db_bootstrap.run()

app = FastAPI()

app.include_router(layaway.router)
