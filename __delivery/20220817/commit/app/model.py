from pydantic import Field
from pydantic.main import BaseModel
from app.utils.form_body import toform_data

@toform_data
class AuthUser(BaseModel):
    # pip install 'pydantic[email]'
    UserId: str = None
    LoginPwd: str = None

class UserRegister(BaseModel):
    # pip install 'pydantic[email]'
    UserId: str = None
    LoginPwd: str = None
    EmpName: str = None   

class Token(BaseModel):
    Authorization: str = None

class MessageOk(BaseModel):
    message: str = Field(default="OK")

class UserToken(BaseModel):
    UserId: int
    EmpName: str = None

    class Config:
        orm_mode = True

class UserMe(BaseModel):
    UserId: str = None
    EmpName: str = None

    class Config:
        orm_mode = True

class Menu(BaseModel):
    MenuId: int
    MenuName: str = None
    MenuUrl: str = None
