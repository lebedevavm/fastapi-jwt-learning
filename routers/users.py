from fastapi import APIRouter, HTTPException, Request

from schemas import (
    User,
    UserResponse,
    UserBase,
    TokenResponse,
    RefreshTokenRequest,
    UserLogin,
)
from crud import get_user_by_name, create_user
from security import generate_tokens, pwd_context, verify_refresh_token
from extensions import limiter


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", status_code=201, response_model=UserResponse)
@limiter.limit("1/minute")
async def new_user(user: User, request: Request) -> UserResponse:
    """
    Register a new user.
    :param user: User object containing username and password
    :return: UserResponse object
    """
    existed_user = await get_user_by_name(user.username)
    if existed_user is not None:
        raise HTTPException(
            status_code=409,
            detail="User already exists",
        )
    db_user = await create_user(
        user.username, pwd_context.hash(user.password), user.role
    )
    if not db_user:
        raise HTTPException(status_code=500, detail="User is not created")
    return UserResponse(
        user=UserBase(username=user.username, role=user.role),
        message="New user created",
    )


@router.post("/login", status_code=200, response_model=TokenResponse)
@limiter.limit("5/minute")
async def login(user: UserLogin, request: Request) -> TokenResponse:
    """
    Login with existed user.
    :param user: User object with username and password
    :return: TokenResponse containing JWT access token
    """
    existed_user = await get_user_by_name(user.username)
    if existed_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    if not pwd_context.verify(user.password, existed_user["password_hash"]):
        raise HTTPException(
            status_code=401,
            detail="Authorization failed",
        )
    user_obj = UserBase(username=existed_user["username"], role=existed_user["role"])
    return generate_tokens(user_obj)


@router.post("/refresh", status_code=200, response_model=TokenResponse)
@limiter.limit("5/minute")
def refresh_token(token: RefreshTokenRequest, request: Request):
    return verify_refresh_token(token.refresh_token)
