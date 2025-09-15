from pydantic import BaseModel
from enum import Enum
from typing import Literal


class RoleName(str, Enum):
    admin = "admin"
    user = "user"
    guest = "guest"


class UserBase(BaseModel):
    username: str
    role: RoleName = RoleName.guest

    class Config:
        from_attributes = True


class User(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    user: UserBase
    message: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Literal["bearer"] = "bearer"


class MessageResponse(BaseModel):
    message: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str
