from fastapi import APIRouter, HTTPException, Path
from typing import List
from datetime import datetime as dt

import app.cruds.builds as crud
from app.models.builds import BuildDB, BuildSchema

router = APIRouter()


@router.post("/", response_model=BuildDB, status_code=201)
async def create_build(payload: BuildSchema):
    build_id = await crud.post(payload)
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")

    response_object = {
        "id": build_id,
        "job_name": payload.job_name,
        "build_number": payload.build_number,
        "state": payload.state,
        "url": payload.url,
        "parameters": payload.parameters,
        "causes": payload.causes,
        "status": payload.status,
        "created_date": created_date,
    }
    return response_object


@router.get("/{id}/", response_model=BuildDB)
async def read_build(id: int = Path(..., gt=0),):
    build = await crud.get(id)
    if not build:
        raise HTTPException(status_code=404, detail="Build not found")
    return build


@router.get("/build_number/{id}/", response_model=BuildDB)
async def read_by_build_number(id: int = Path(..., gt=0),):
    build = await crud.get_by_build_number(id)
    # build = await crud.get(id)
    if not build:
        raise HTTPException(status_code=404, detail="Build not found")
    return build


@router.get("/", response_model=List[BuildDB])
async def read_all_builds():
    return await crud.get_all()


#UPDATE route
@router.put("/{id}/", response_model=BuildDB)
async def update_build(payload:BuildSchema, id:int=Path(...,gt=0)): #Ensures the input is greater than 0
    build = await crud.get(id)
    if not build:
        raise HTTPException(status_code=404, detail="Build not found")
    build_id = await crud.put(id, payload)
    response_object = {
        "id": build_id,
        "job_name": payload.job_name,
        "build_number": payload.build_number,
        "state": payload.state,
        "url": payload.url,
        "parameters": payload.parameters,
        "causes": payload.causes,
        "status": payload.status,
        "created_date": payload.created_date,
    }
    return response_object


#DELETE route
@router.delete("/{id}/", response_model=BuildDB)
async def delete_build(id: int = Path(..., gt=0)):
    build = await crud.get(id)
    if not build:
        raise HTTPException(status_code=404, detail="Build not found")
    await crud.delete(id)

    return build
