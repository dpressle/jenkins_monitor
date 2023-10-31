import requests
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/builds/{release_version}")
def builds(request: Request, release_version: str):
    print(request)
    return templates.TemplateResponse("builds.html", {"request": request, "release_version": release_version})
