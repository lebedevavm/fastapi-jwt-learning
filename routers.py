from fastapi import APIRouter, HTTPException

from schemas import User, UserResponse, UserBase, TokenResponse
from crud import get_user_by_name, create_user
from services import create_jwt_token, pwd_context


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", status_code=201, response_model=UserResponse)
async def new_user(user: User) -> UserResponse:
    """
    Register a new user.
    :param user: User object containing username and password
    :return: UserResponse object
    """
    existed_user = await get_user_by_name(user.username)
    if existed_user is not None:
        raise HTTPException(
            status_code=409,
            detail=f"User with username={user.username} already exists",
        )
    db_user = await create_user(user.username, pwd_context.hash(user.password))
    if not db_user:
        raise HTTPException(status_code=500, detail="User is not created")
    return UserResponse(
        user=UserBase(username=user.username), message="User registered successfully"
    )


@router.post("/login", status_code=200, response_model=TokenResponse)
async def login(user: User) -> TokenResponse:
    """
    Login with existed user.
    :param user: User object with username and password
    :return: TokenResponse containing JWT access token
    """
    existed_user = await get_user_by_name(user.username)
    if existed_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )
    if not pwd_context.verify(user.password, existed_user["password_hash"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )
    token = create_jwt_token({"sub": user.username})
    return TokenResponse(access_token=token)
