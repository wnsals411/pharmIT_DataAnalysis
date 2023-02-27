from fastapi import Request, APIRouter, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.library.helpers import *
from app.model import Menu
from app.database.schema import AnalMenu

# import shutil
# from pydantic.main import BaseModel

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get("/")
async def root():
    return RedirectResponse('/login/')

@router.get("/login/")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/home/", response_class=HTMLResponse)
async def home(request: Request):
    # data = openfile("menu.md")

    data = AnalMenu.getallsort()
    return templates.TemplateResponse("base.html", {"request": request, "data": data})
    
@router.get("/anal/", response_class=HTMLResponse)
async def anal(request: Request):
    data = openfile("anal.md")
    # print (data)
    # print (request)
    return templates.TemplateResponse("page.html", {"request": request, "data": data})


