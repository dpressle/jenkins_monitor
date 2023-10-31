from app.api.models import BuildSchema
from app.db import builds_table, database
from datetime import datetime as dt

async def post(payload: BuildSchema):
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")
    query = builds_table.insert().values(
        job_name=payload.job_name,
        build_number=payload.build_number,
        state=payload.state,
        url=payload.url,
        parameters=payload.parameters,
        causes=payload.causes,
        status=payload.status,
        created_date=created_date)
    return await database.execute(query=query)


async def get(id: int):
    query = builds_table.select().where(id == builds_table.c.id)
    return await database.fetch_one(query=query)


async def get_by_build_number(build_number: int):
    query = builds_table.select().where(
        build_number == builds_table.c.build_number)
    return await database.fetch_one(query=query)


async def get_all():
    query = builds_table.select()
    return await database.fetch_all(query=query)


async def put(id: int, payload=BuildSchema):
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")
    query = (
        builds_table.update().where(id == builds_table.c.id).values(
            job_name=payload.job_name,
            build_number=payload.build_number,
            state=payload.state,
            url=payload.url,
            parameters=payload.parameters,
            causes=payload.causes,
            status=payload.status,
            created_date=created_date)
        .returning(builds_table.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = builds_table.delete().where(id == builds_table.c.id)
    return await database.execute(query=query)
