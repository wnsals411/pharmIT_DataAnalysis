
from datetime import datetime, timedelta

# import bcrypt
import hashlib   #, secrets
import jwt
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.common.consts import JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.database.schema import User
from app.model import UserToken, AuthUser, MessageOk
from app.errors import exceptions as ex

router = APIRouter()

templates = Jinja2Templates(directory="templates/")

# @router.post("/login/", status_code=200, response_model=MessageOk)
@router.post("/login/", status_code=200, response_model=MessageOk)
# async def login(request: Request, user_info: AuthUser = Depends(AuthUser)):
async def login(user_info:AuthUser):  
# async def login(UserId: str = Form(), LoginPwd: str = Form()):

    # print(user_info.UserId)
    # print(user_info.LoginPwd)
    
    is_exist = await is_userid_exist(user_info.UserId)
    
    if not is_exist:
        # return JSONResponse(status_code=400, content=dict(msg="NO_MATCH_USER"))
        # raise HTTPException(status_code=400, detail="NOT_MATCH_USER")
        raise ex.NotFoundUserEx()
        # return ex.NotFoundUserEx()
        
    user = User.getfirst(UserId=user_info.UserId)
   
    # print(user_info.LoginPwd)
    # print(user.LoginPwd)

    PLoginPwd = hashlib.sha512((user_info.LoginPwd).encode('utf-8')).hexdigest()
    
    is_verified = (PLoginPwd==user.LoginPwd)
    
    # is_verified = bcrypt.checkpw(user_info.LoginPwd.encode("utf-8"), user.LoginPwd.encode("utf-8"))

    if not is_verified:
        # return JSONResponse(status_code=400, content=dict(msg="NO_MATCH_USER"))
        raise ex.NotFoundUserEx()
        # return templates.TemplateResponse("error.html", {"request": request, "data": ex.NotFoundUserEx(), "user": user})
    
    token = dict(
        Authorization=f"Bearer {create_access_token(data=UserToken.from_orm(user).dict(),expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES )}")
        # Authorization=f"Bearer {create_access_token(data=UserToken.from_orm(user).dict(exclude={'UserId', 'EmpName'}),)}") 

    # print(token)
    response = JSONResponse(status_code=200, content=dict(msg="OK"))
    # response = RedirectResponse('/home/', status_code=303)
    # response = MessageOk()
    
    response.set_cookie(
    key="Authorization",
    value=token,
    secure=False,
    httponly=True,
    samesite=None,
    expires= datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # domain="example.com"
    )

    return response

@router.get("/logout", status_code=200, response_model=MessageOk)
async def logout():

    response = JSONResponse(status_code=200, content=dict(msg="OK"))
    # response = response.delete_cookie('Authorization')
    response.set_cookie(
    key="Authorization",
    value='',
    secure=False,
    httponly=True,
    samesite=None,
    expires= datetime.utcnow()
    # domain="example.com"
    )
        
    return response

async def is_userid_exist(userid: str):

    get_userid = User.getfirst(UserId=userid)

    if get_userid:
        return True
    return False


def create_access_token(*, data: dict = None, expires_delta: int = None):

    to_encode = data.copy()
    # print(expires_delta)
    if expires_delta:
        # print(datetime.utcnow())
        # print(timedelta(minutes=expires_delta))
        # print(datetime.utcnow() + timedelta(minutes=expires_delta))
        to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=expires_delta)})
    
    # print(to_encode)
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    # encoded_jwt = (jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM, headers=None, json_encoder=None)).encode('utf-8')
    # encoded_jwt = jwt.encode(payload, key, algorithm="HS256", headers=None, json_encoder=None)
    # print(encoded_jwt)
    return encoded_jwt
