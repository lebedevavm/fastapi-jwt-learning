import jwt
import secrets
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from passlib.context import CryptContext


SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_jwt_token(data: dict) -> str:
    """
    Generate a JWT token with given data.
    :param data: dict containing payload (e.g., {"sub": username})
    :return: encoded JWT string
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=3)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_from_token(token: str = Depends(oauth2_scheme)) -> str:
    """
    Verify JWT token for user.
    :param token: JWT token
    :return: user name
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token is expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")
