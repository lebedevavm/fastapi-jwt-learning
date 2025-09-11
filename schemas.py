from pydantic import BaseModel


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
    token_type: str = "bearer"


class MessageResponse(BaseModel):
    message: str
