from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from ..dependencies import AuthHeaders
from ..services.layaway import LayawayService


router = APIRouter(
    prefix="/addToLayaway",
    tags=["add_to_layaway"],
    responses={404: {"description": "Not Found"}},
)


class LayawayIn(BaseModel):
    comic_ids: list[int]


@router.post("/")
def add(
    layaway: LayawayIn,
    headers: AuthHeaders = Depends(AuthHeaders),
    service: LayawayService = Depends(LayawayService),
):
    response = service.create_layaway(layaway.comic_ids, headers)
    return JSONResponse(response, status_code=201)


@router.patch("/")
def update(
    layaway: LayawayIn,
    headers: AuthHeaders = Depends(AuthHeaders),
    service: LayawayService = Depends(LayawayService),
):
    response = service.update_layaway(layaway.comic_ids, headers)
    return JSONResponse(response, status_code=200)


@router.put("/")
def overwrite(
    layaway: LayawayIn,
    headers: AuthHeaders = Depends(AuthHeaders),
    service: LayawayService = Depends(LayawayService),
):
    response = service.overwrite_layaway(layaway.comic_ids, headers)
    return JSONResponse(response, status_code=200)
