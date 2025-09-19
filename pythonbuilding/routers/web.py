from typing import Annotated
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from pythonbuilding.db import get_session
from pythonbuilding.routers.car import get_cars

router = APIRouter()
templates = Jinja2Templates(directory="pythonbuilding/templates")

@router.get("/", response_class=HTMLResponse)
def home(request :Request):
    return templates.TemplateResponse("home.html", {"request" :request})

@router.post(path="/search", response_class=HTMLResponse)
def search(
    size: Annotated[str, Form()],
    doors: Annotated[int, Form()],
    request: Request,
    session: Annotated[Session, Depends(get_session)],
):
    cars = get_cars(size=size, doors=doors, session=session)
    return templates.TemplateResponse(
        "search_results.html",
        {"request": request, "cars": cars}
    )
