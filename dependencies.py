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
