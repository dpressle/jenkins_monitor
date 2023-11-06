from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routes import ping, releases, builds, projects
from app.db import engine, metadata, database

metadata.create_all(engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(ping.router)
app.include_router(builds.router, prefix="/builds", tags=["builds"])
app.include_router(releases.router, prefix="/releases", tags=["releases"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
