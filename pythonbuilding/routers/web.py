from os import path
from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, Request, Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from pythonbuilding.db import get_session
from pythonbuilding.routers.car import get_cars
from pythonbuilding.routers.user import create_user
from pythonbuilding.schemas import UserInput

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

# GET signup page
@router.get("/auth/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


# POST signup form
from fastapi.responses import RedirectResponse

@router.post("/auth/signup")
def signup_web(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    user_input = UserInput(username=username, password=password)
    try:
        user = create_user(user_input, session)
        # Redirect to home page
        response = RedirectResponse(url="/", status_code=303)
        return response
    except Exception as e:
        return templates.TemplateResponse(
            "signup.html",
            {"request": request, "error": str(e)}
        )
