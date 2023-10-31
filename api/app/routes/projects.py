from fastapi import APIRouter, HTTPException, Path
from typing import List

import app.cruds.projects as crud
from app.models.projects import ProjectDB, ProjectSchema


router = APIRouter()


@router.post("/", response_model=ProjectDB, status_code=201)
async def create_project(payload: ProjectSchema):
    project_id = await crud.post(payload)

    response_object = {
        "id": project_id,
        "name": payload.name
    }
    return response_object


@router.get("/{id}/", response_model=ProjectDB)
async def read_project(id: int = Path(..., gt=0),):
    project = await crud.get(id)
    if not project:
        raise HTTPException(status_code=404, detail="Build not found")
    return project


@router.get("/", response_model=List[ProjectDB])
async def read_all_projects():
    return await crud.get_all()


#UPDATE route
@router.put("/{id}/", response_model=ProjectDB)
# Ensures the input is greater than 0
async def update_project(payload: ProjectSchema, id: int = Path(..., gt=0)):
    project = await crud.get(id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project_id = await crud.put(id, payload)
    response_object = {
        "id": project_id,
        "name": payload.name
    }
    return response_object


#DELETE route
@router.delete("/{id}/", response_model=ProjectDB)
async def delete_project(id: int = Path(..., gt=0)):
    project = await crud.get(id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    await crud.delete(id)

    return project
