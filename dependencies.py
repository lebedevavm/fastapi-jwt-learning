from fastapi import Depends, HTTPException, status

from security import get_user_from_token
from crud import get_user_by_name
from schemas import UserBase


async def get_current_user(
    current_username: str = Depends(get_user_from_token),
) -> UserBase:
    user = await get_user_by_name(current_username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return UserBase(username=user["username"], role=user["role"])


def get_rate_limit_by_role(key: str) -> str:
    """
    key = username (или "_guest")
    """
    if key == "_guest":
        return "5/minute"

    try:
        from security import refresh_tokens, verify_token
        if key not in refresh_tokens:
            return "5/minute"
        payload = verify_token(refresh_tokens[key])
        role = payload.get("role")
    except Exception:
        role = None

    limits = {"admin": "1000/minute", "user": "20/minute"}
    return limits.get(role, "5/minute")
