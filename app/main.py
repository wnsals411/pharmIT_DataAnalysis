import uvicorn

from dataclasses import asdict
from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles


from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.middlewares.token_validator import access_control
from app.middlewares.trusted_hosts import TrustedHostMiddleware

from app.routers import index
from app.auth import route_login   #new 
from app.common.config import conf
from app.database.conn import db

# API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)

def create_app():
    """
    앱 함수 실행
    :return:
    """
    c = conf()
    app = FastAPI()
    conf_dict = asdict(c)
    # print("-----------------------------------------------")
    # print(conf_dict)
    # print(type(conf_dict))

     # 데이터베이스 초기화
    db.init_app(app, **conf_dict)
    
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # 레디스 이니셜라이즈

    # 미들웨어 정의
    app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control) 
    app.add_middleware(
        CORSMiddleware,
        allow_origins=conf().ALLOW_SITE,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=conf().TRUSTED_HOSTS, except_path=["/health"])


    # 라우터 정의
    app.include_router(index.router)
    # app.include_router(route_login.router)
    # app.include_router(route_login.router, prefix="", tags=["auth-webapp"])   #new
    # app.include_router(route_login.router, prefix="/api", tags=["Authentication"] )
    # app.include_router(route_login.router, tags=["Users"], prefix="/api", dependencies=[Depends(API_KEY_HEADER)])
    app.include_router(route_login.router)

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
    