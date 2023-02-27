# import base64
# import hmac
# import typing
from ast import And
import time
import re
import jwt
import sqlalchemy.exc

from jwt.exceptions import ExpiredSignatureError, DecodeError
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.common.consts import EXCEPT_PATH_LIST, EXCEPT_PATH_REGEX
from app.errors import exceptions as ex

from app.common import consts #, config
from app.errors.exceptions import APIException, SqlFailureEx #, APIQueryStringEx
from app.model import UserToken

from app.utils.date_utils import D
from app.utils.logger import api_logger

async def access_control(request: Request, call_next):
    request.state.req_time = D.datetime()
    request.state.start = time.time()
    request.state.inspect = None
    request.state.user = None
    request.state.service = None

    ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
    request.state.ip = ip.split(",")[0] if "," in ip else ip
    # headers = request.headers
    cookies = request.cookies
    
    url = request.url.path
    print(url)
    try:

        if not (await url_pattern_check(url, EXCEPT_PATH_REGEX)) and not (url in EXCEPT_PATH_LIST):
            # 템플릿 렌더링인 경우 쿠키에서 토큰 검사
            # cookies["Authorization"] = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTQsImVtYWlsIjoia29hbGFAZGluZ3JyLmNvbSIsIm5hbWUiOm51bGwsInBob25lX251bWJlciI6bnVsbCwicHJvZmlsZV9pbWciOm51bGwsInNuc190eXBlIjpudWxsfQ.4vgrFvxgH8odoXMvV70BBqyqXOFa2NDQtzYkGywhV48"
            if "Authorization" not in cookies.keys():
                raise ex.NotAuthorized()
            token_info = await token_decode(access_token=cookies.get("Authorization"))
            request.state.user = UserToken(**token_info)
        
        response = await call_next(request)
        await api_logger(request=request, response=response)         
        
    except Exception as e:
        error = await exception_handler(e)
        error_dict = dict(status=error.status_code, msg=error.msg, detail=error.detail, code=error.code)
       
        response = JSONResponse(status_code=200, content=error_dict)
        # if error_dict["status"] =='400':
        #     response = ex.NotFoundUserEx()
        await api_logger(request=request, error=error)

    return response

async def url_pattern_check(path, pattern):
    result = re.match(pattern, path)
    if result:
        # print("True")
        return True
    # print("False")
    return False

async def token_decode(access_token):
    """
    :param access_token:
    :return:
    """
    try:
        access_token = eval(access_token.replace("Bearer ", ""))['Authorization']
        # print(access_token)
        payload = jwt.decode(access_token, key=consts.JWT_SECRET, algorithms=[consts.JWT_ALGORITHM])
        
    except ExpiredSignatureError:
        raise ex.TokenExpiredEx()
    except DecodeError:
        raise ex.TokenDecodeEx()
    return payload

async def exception_handler(error: Exception):
    # print("exception_handler : error")
    # print(error)
    # print(isinstance(error, sqlalchemy.exc.OperationalError))
    # print(isinstance(error, APIException))
    if isinstance(error, sqlalchemy.exc.OperationalError):
        error = SqlFailureEx(ex=error)    
    if not isinstance(error, APIException):
        error = APIException(ex=error, detail=str(error))
    return error