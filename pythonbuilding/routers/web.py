from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="pythonbuilding/templates")

@router.get("/", response_class=HTMLResponse)
def home(request :Request):
    return templates.TemplateResponse("home.html", {"request" :request})

#@router.post(path: "/")