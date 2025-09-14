from pydantic import BaseModel
from typing import Literal


class UserBase(BaseModel):
    username: str

    class Config:
        from_attributes = True


class User(UserBase):
    password: str


class UserResponse(BaseModel):
    user: UserBase
    message: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = Literal["bearer"]


class MessageResponse(BaseModel):
    message: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str
