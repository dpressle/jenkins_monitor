from datetime import datetime as dt

from app.db import release_table, database
from app.models.releases import ReleaseSchema


async def post(payload: ReleaseSchema):
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")
    query = release_table.insert().values(
        version=payload.version,
        branch=payload.branch,
        state=payload.state,
        url=payload.url,
        created_date=created_date)
    return await database.execute(query=query)


async def get(id: int):
    query = release_table.select().where(id == release_table.c.id)
    return await database.fetch_one(query=query)


async def get_by_release(release: str):
    query = release_table.select().where(
        release == release_table.c.release)
    return await database.fetch_one(query=query)


async def get_all():
    query = release_table.select()
    return await database.fetch_all(query=query)


async def put(id: int, payload=ReleaseSchema):
    # created_date = dt.now().strftime("%Y-%m-%d %H:%M")
    query = (
        release_table.update().where(id == release_table.c.id).values(
            version=payload.version,
            branch=payload.branch,
            state=payload.state,
            url=payload.url,)
        .returning(release_table.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = release_table.delete().where(id == release_table.c.id)
    return await database.execute(query=query)
