# from fastapi import Request, APIRouter, Cookie
from fastapi import Request, APIRouter, Depends # 추가
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse # 추가
from fastapi.templating import Jinja2Templates
from app.library.helpers import *
from app.model import MessageOk, Data, PostXML
from app.database.schema import AnalMenu, User, AnalDept, AnalGroup, AnalSecu, AnalSecuDept, AnalSecuGroup # 추가
from fastapi.encoders import jsonable_encoder # 추가
import pymssql # 추가
import json # 추가

from app.database.conn import db # 추가
from sqlalchemy.orm import Session # 추가

import datetime
 
now = datetime.datetime.now()
# from app.database.conn import db


# import shutil
# from pydantic.main import BaseModel

# 서버 정보
server = "112.221.63.59:14233"
database = "PHARM"
username = "pharmdba"
password = "pharmbio!@#$"


router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get("/")
async def root():
    return RedirectResponse('/login/')

@router.get("/login/")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# @router.get("/home/", response_class=HTMLResponse)
# async def home(request: Request):
#     # data = openfile("menu.md")

#     user = request.state.user
#     data = AnalMenu.getallsort()
#     return templates.TemplateResponse("base.html", {"request": request, "data": data, "user": user})

@router.get("/home/", response_class=HTMLResponse)
async def home(request: Request):
    # data = openfile("menu.md")

    user = request.state.user

    user_group = AnalGroup.getsort(UserID=user.UserId)
   
    data = AnalSecu.getallsort(UserId=user.UserId, YN='Y')
    data2 = AnalSecuDept.getallsort(DeptSeq=user.DeptSeq, YN='Y')

    if len(user_group) == 0:
        data3 = AnalSecuGroup.getallsort(GroupSeq=0, YN='Y')
    elif len(user_group) == 1:
        data3 = AnalSecuGroup.getallsort(GroupSeq=user_group[0].GroupSeq, YN='Y')

    return templates.TemplateResponse("base.html", {"request": request, "data": data, "data2": data2, "data3": data3, "user": user})

@router.get("/anal/", response_class=HTMLResponse)
async def anal(request: Request):
    data = openfile("anal.md")
    # print (data)
    # print (request)
    return templates.TemplateResponse("page.html", {"request": request, "data": data})

# @router.get("/secu/", response_class=HTMLResponse)
# async def secu(request: Request):
#     return templates.TemplateResponse("secu.html", {"request": request})    

@router.get("/secu/", response_class=HTMLResponse)
async def secu(request: Request):
    user = request.state.user
    if user.Chk == 1:    
        return templates.TemplateResponse("secu.html", {"request": request})    
    else:
        return RedirectResponse(url="/home", status_code=302)

@router.get("/json_menu/")
async def secu(request: Request):
    Menu = AnalMenu.getsort()
    Menu_json = jsonable_encoder(Menu) # 인코딩 필수

    return JSONResponse(content=Menu_json)

@router.get("/json_emp/")
async def secu(request: Request):
    emp = User.getsort()
    emp_json = jsonable_encoder(emp) # 인코딩 필수

    return JSONResponse(content=emp_json)

@router.get("/json_dept/")
async def secu(request: Request):
    dept = AnalDept.getsort()
    dept_json = jsonable_encoder(dept) # 인코딩 필수

    return JSONResponse(content=dept_json)

@router.get("/json_group/")
async def secu(request: Request):
    group = AnalGroup.getsort()
    group_json = jsonable_encoder(group) # 인코딩 필수

    return JSONResponse(content=group_json)   

@router.get("/secu/emp/{MenuId}")
async def secu(request: Request, MenuId):
    Menu = AnalSecu.getsort(MenuId = MenuId, YN = 'Y')
    Menu_json = jsonable_encoder(Menu) # 인코딩 필수

    return JSONResponse(content=Menu_json)            

@router.get("/secu/dept/{MenuId}")
async def secu(request: Request, MenuId):
    Menu = AnalSecuDept.getsort(MenuId = MenuId, YN = 'Y')
    Menu_json = jsonable_encoder(Menu) # 인코딩 필수

    return JSONResponse(content=Menu_json)            

@router.get("/secu/group/{MenuId}")
async def secu(request: Request, MenuId):
    Menu = AnalSecuGroup.getsort(MenuId = MenuId, YN = 'Y')
    Menu_json = jsonable_encoder(Menu) # 인코딩 필수

    return JSONResponse(content=Menu_json)                

@router.post("/save_emp/", status_code=200, response_model=MessageOk)
async def save(request: Request, data: Data, session: Session = Depends(db.session),):

    if (len(data.call1) != 0):
        for i in range(len(data.call1)): # N으로 변경
            if (AnalSecu.filter(MenuId = int(data.callmenu[0]), UserId = data.call1[i], YN = 'N').count() == 1): # 변화 없는경우 -> pass
                continue
            elif (AnalSecu.filter(MenuId = int(data.callmenu[0]), UserId = data.call1[i]).count() == 1): # 기존 데이터 있는경우 -> Update
                AnalSecu.filter(MenuId = int(data.callmenu[0]), UserId = data.call1[i]).update(YN = 'N', LastDateTime = now)
            elif (AnalSecu.filter(MenuId = int(data.callmenu[0]), UserId = data.call1[i]).count() == 0): # 기존 데이터 없는경우 -> Insert
                tmp = User.getsort(UserId = data.call1[i])
                AnalSecu.create(session = session, DeptSeq = int(tmp[0].DeptSeq), DeptName = tmp[0].DeptName, UserId = data.call1[i], EmpName = tmp[0].EmpName, MenuId = int(data.callmenu[0]), MenuName = data.callmenu[1], MenuUrl = data.callmenu[2], Sort = data.callmenu[3], YN = 'N', LastDateTime = now)
    
    if (len(data.call2) != 0):
        for i in range(len(data.call2)): # Y으로 변경
            if (AnalSecu.filter(MenuId = int(data.callmenu[0]), UserId = data.call2[i], YN = 'Y').count() == 1): # 변화 없는경우 -> pass
                continue    
            elif (AnalSecu.filter(MenuId = int(data.callmenu[0]), UserId = data.call2[i]).count() == 1): # 기존 데이터 있는경우 -> Update
                AnalSecu.filter(MenuId = int(data.callmenu[0]), UserId = data.call2[i]).update(YN = 'Y', LastDateTime = now)
            elif (AnalSecu.filter(MenuId = int(data.callmenu[0]), UserId = data.call2[i]).count() == 0): # 기존 데이터 없는경우 -> Insert
                tmp = User.getsort(UserId = data.call2[i])
                AnalSecu.create(session = session, DeptSeq = int(tmp[0].DeptSeq), DeptName = tmp[0].DeptName, UserId = data.call2[i], EmpName = tmp[0].EmpName, MenuId = int(data.callmenu[0]), MenuName = data.callmenu[1], MenuUrl = data.callmenu[2], Sort = data.callmenu[3], YN = 'Y', LastDateTime = now)

    response = JSONResponse(status_code=200, content=dict(msg="OK"))

    return response

@router.post("/save_dept/", status_code=200, response_model=MessageOk)
async def save(request: Request, data: Data, session: Session = Depends(db.session),):

    for i in range(len(data.call1)):
        if (AnalSecuDept.filter(MenuId = int(data.callmenu[0]), DeptSeq = int(data.call1[i]), YN = 'N').count() == 1):
            continue
        elif (AnalSecuDept.filter(MenuId = int(data.callmenu[0]), DeptSeq = int(data.call1[i])).count() == 1):
            AnalSecuDept.filter(MenuId = int(data.callmenu[0]), DeptSeq = int(data.call1[i])).update(YN = 'N', LastDateTime = now)
        elif (AnalSecuDept.filter(MenuId = int(data.callmenu[0]), DeptSeq = int(data.call1[i])).count() == 0):
            tmp = AnalDept.getsort(DeptSeq = data.call1[i])
            AnalSecuDept.create(session = session, DeptSeq = data.call1[i], DeptName = tmp[0].DeptName, MenuId = int(data.callmenu[0]), MenuName = data.callmenu[1], MenuUrl = data.callmenu[2], Sort = data.callmenu[3], YN = 'N', LastDateTime = now)

    for i in range(len(data.call2)):
        if (AnalSecuDept.filter(MenuId = int(data.callmenu[0]), DeptSeq = int(data.call2[i]), YN = 'Y').count() == 1):
            continue
        elif (AnalSecuDept.filter(MenuId = int(data.callmenu[0]), DeptSeq = int(data.call2[i])).count() == 1):
            AnalSecuDept.filter(MenuId = int(data.callmenu[0]), DeptSeq = int(data.call2[i])).update(YN = 'Y', LastDateTime = now)
        elif (AnalSecuDept.filter(MenuId = int(data.callmenu[0]), DeptSeq = int(data.call2[i])).count() == 0):
            tmp = AnalDept.getsort(DeptSeq = data.call2[i])
            AnalSecuDept.create(session = session, DeptSeq = data.call2[i], DeptName = tmp[0].DeptName, MenuId = int(data.callmenu[0]), MenuName = data.callmenu[1], MenuUrl = data.callmenu[2], Sort = data.callmenu[3], YN = 'Y', LastDateTime = now)            

    response = JSONResponse(status_code=200, content=dict(msg="OK"))

    return response

@router.post("/save_group/", status_code=200, response_model=MessageOk)
async def save(request: Request, data: Data, session: Session = Depends(db.session),):

    for i in range(len(data.call1)):
        if (AnalSecuGroup.filter(MenuId = int(data.callmenu[0]), GroupSeq = int(data.call1[i]), YN = 'N').count() == 1):
            continue
        elif (AnalSecuGroup.filter(MenuId = int(data.callmenu[0]), GroupSeq = int(data.call1[i])).count() == 1):
            AnalSecuGroup.filter(MenuId = int(data.callmenu[0]), GroupSeq = int(data.call1[i])).update(YN = 'N', LastDateTime = now)
        elif (AnalSecuGroup.filter(MenuId = int(data.callmenu[0]), GroupSeq = int(data.call1[i])).count() == 0):
            tmp = AnalSecuGroup.getsort(GroupSeq = data.call1[i])
            AnalSecuGroup.create(session = session, GroupSeq = data.call1[i], GroupName = tmp[0].GroupName, MenuId = int(data.callmenu[0]), MenuName = data.callmenu[1], MenuUrl = data.callmenu[2], Sort = data.callmenu[3], YN = 'N', LastDateTime = now)

    for i in range(len(data.call2)):
        if (AnalSecuGroup.filter(MenuId = int(data.callmenu[0]), GroupSeq = int(data.call2[i]), YN = 'Y').count() == 1):
            continue
        elif (AnalSecuGroup.filter(MenuId = int(data.callmenu[0]), GroupSeq = int(data.call2[i])).count() == 1):
            AnalSecuGroup.filter(MenuId = int(data.callmenu[0]), GroupSeq = int(data.call2[i])).update(YN = 'Y', LastDateTime = now)
        elif (AnalSecuGroup.filter(MenuId = int(data.callmenu[0]), GroupSeq = int(data.call2[i])).count() == 0):
            tmp = AnalGroup.getsort(GroupSeq = data.call2[i])
            AnalSecuGroup.create(session = session, GroupSeq = data.call2[i], GroupName = tmp[0].GroupName, MenuId = int(data.callmenu[0]), MenuName = data.callmenu[1], MenuUrl = data.callmenu[2], Sort = data.callmenu[3], YN = 'Y', LastDateTime = now)            

    response = JSONResponse(status_code=200, content=dict(msg="OK"))

    return response        


# @router.get("/group_mapping/", response_class=HTMLResponse)
# async def group(request: Request):
#     group = AnalGroup.getallsort()
#     return templates.TemplateResponse("group.html", {"request": request, "group": group})

@router.get("/group_mapping/", response_class=HTMLResponse)
async def secu(request: Request):
    user = request.state.user

    if user.Chk == 1:    
        group = AnalGroup.getallsort()
        return templates.TemplateResponse("group.html", {"request": request, "group": group})
    else:
        return RedirectResponse(url="/home", status_code=302)    

@router.post("/save_groupmapping/", status_code=200, response_model=MessageOk)
async def save(save_xml: PostXML):
    cnxn =  pymssql.connect(server , username, password, database)
    cursor = cnxn.cursor()
    sql = "EXEC pharm_AnalGroupMapping @XML =" + save_xml.save_xml
    cursor.execute(sql)
    cnxn.commit()
    cnxn.close()    
    response = JSONResponse(status_code=200, content=dict(msg="OK"))

    return response    

#uvicorn app.main:app --reload --host=127.0.0.1 --port=8081