from datetime import datetime as dt

from app.db import projects_table, database
from app.models.projects import ProjectSchema


async def post(payload: ProjectSchema):
    query = projects_table.insert().values(
        name=payload.name)
    return await database.execute(query=query)


async def get(id: int):
    query = projects_table.select().where(id == projects_table.c.id)
    return await database.fetch_one(query=query)


async def get_all():
    query = projects_table.select()
    return await database.fetch_all(query=query)


async def put(id: int, payload=ProjectSchema):
    # created_date = dt.now().strftime("%Y-%m-%d %H:%M")
    query = (
        projects_table.update().where(id == projects_table.c.id).values(
            name=payload.name)
        .returning(projects_table.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = projects_table.delete().where(id == projects_table.c.id)
    return await database.execute(query=query)
