from fastapi import APIRouter, HTTPException, Path
from typing import List
from datetime import datetime as dt

import app.cruds.releases as crud
from app.models.releases import ReleaseDB, ReleaseSchema


router = APIRouter()


@router.post("/", response_model=ReleaseDB, status_code=201)
async def create_release(payload: ReleaseSchema):
    release_id = await crud.post(payload)
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")

    response_object = {
        "id": release_id,
        "version": payload.version,
        "branch": payload.branch,
        "state": payload.state,
        "url": payload.url,
        "created_date": created_date,
    }
    return response_object


@router.get("/{id}/", response_model=ReleaseDB)
async def read_release(id: int = Path(..., gt=0),):
    release = await crud.get(id)
    if not release:
        raise HTTPException(status_code=404, detail="Build not found")
    return release


@router.get("/", response_model=List[ReleaseDB])
async def read_all_releases():
    return await crud.get_all()


#UPDATE route
@router.put("/{id}/", response_model=ReleaseDB)
# Ensures the input is greater than 0
async def update_release(payload: ReleaseSchema, id: int = Path(..., gt=0)):
    release = await crud.get(id)
    if not release:
        raise HTTPException(status_code=404, detail="Release not found")
    release_id = await crud.put(id, payload)
    response_object = {
        "id": release_id,
        "version": payload.version,
        "branch": payload.branch,
        "state": payload.state,
        "url": payload.url,
    }
    return response_object


#DELETE route
@router.delete("/{id}/", response_model=ReleaseDB)
async def delete_release(id: int = Path(..., gt=0)):
    release = await crud.get(id)
    if not release:
        raise HTTPException(status_code=404, detail="Release not found")
    await crud.delete(id)

    return release
