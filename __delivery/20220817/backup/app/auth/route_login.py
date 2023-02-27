from datetime import datetime, timedelta

# import bcrypt
import hashlib, secrets
import jwt
from fastapi import Request, APIRouter, Depends, HTTPException
# from fastapi.templating import Jinja2Templates
from sqlalchemy import true

# TODO:
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.common.consts import JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
# from app.database.conn import db
from app.database.schema import User
from app.model import Token, UserToken, UserRegister, UserMe
from app.errors import exceptions as ex

router = APIRouter()

# templates = Jinja2Templates(directory="templates/")

# @router.get("/login/")
# def login(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})



# @router.post("/login/", status_code=200, response_model=Token)
@router.post("/login/", status_code=200)
async def login(user_info: UserRegister):
    
    # print(user_info.UserId)
    # print(user_info.LoginPwd)
    
    is_exist = await is_userid_exist(user_info.UserId)
    # print(is_exist)
    # print(not is_exist)
    # if not user_info.userid or not user_info.password:
    #     return JSONResponse(status_code=400, content=dict(msg="아이디와 비밀번호를 입력하세요."))
    
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
    token = dict(
        Authorization=f"Bearer {create_access_token(data=UserToken.from_orm(user).dict(),expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES )}")
        # Authorization=f"Bearer {create_access_token(data=UserToken.from_orm(user).dict(exclude={'UserId', 'EmpName'}),)}")
    
    # Response.set_cookie(key="access_token", value=token, httponly=True)

    # print(token)
    response = JSONResponse(status_code=200, content=dict(msg="OK"))

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
    # return token

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
