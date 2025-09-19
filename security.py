import jwt
import secrets
from fastapi import HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from passlib.context import CryptContext

from schemas import TokenResponse, UserBase


SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
refresh_tokens: dict[str, str] = {}


def create_jwt_token(data: dict, token_type: str, expires_delta: timedelta) -> str:
    """
    Generate a JWT token with given data.
    :param data: dict containing payload (e.g., {"sub": username})
    :param token_type: str ("access" or "refresh")
    :param expires_delta: timedelta
    :return: encoded JWT string
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Verify JWT token for user.
    :param token: JWT token
    :return: data for token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token is expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")


def get_user_from_token(token: str = Depends(oauth2_scheme)) -> str:
    """
    Verify JWT token for user.
    :param token: JWT token
    :return: user name
    """
    payload = verify_token(token)
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid type token")
    return payload.get("sub")


def verify_refresh_token(token: str = Depends(oauth2_scheme)) -> TokenResponse:
    """
    Verify and update refresh token for user.
    :param token: JWT token
    :return: user name
    """
    payload = verify_token(token)
    token_type = payload.get("type")
    user = payload.get("sub")
    if token_type != "refresh":
        raise HTTPException(status_code=401, detail="Invalid type token")
    if user not in refresh_tokens or refresh_tokens[user] != token:
        raise HTTPException(status_code=401, detail="Not known token")
    return generate_tokens(user)


def generate_tokens(user: UserBase) -> TokenResponse:
    payload = {"sub": user.username, "role": user.role}  # username  # роль
    access_token = create_jwt_token(
        payload, token_type="access", expires_delta=timedelta(minutes=15)
    )
    refresh_token = create_jwt_token(
        payload, token_type="refresh", expires_delta=timedelta(days=7)
    )
    refresh_tokens[user.username] = refresh_token
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


def get_username_from_request(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    token = auth_header.split()[-1] if auth_header else None
    if not token:
        return "_guest"
    try:
        payload = verify_token(token)
        return payload.get("sub", "_guest")
    except jwt.PyJWTError:
        return "_guest"
