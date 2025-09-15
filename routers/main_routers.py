from fastapi import APIRouter, Depends

from rbac import PermissionChecker
from dependencies import get_current_user
from schemas import MessageResponse, UserBase

router = APIRouter(prefix="/resources")


@router.get("/admin")
@PermissionChecker(["admin"])
async def admin_info(
    current_user: UserBase = Depends(get_current_user),
) -> MessageResponse:
    return MessageResponse(
        message=f"Hello, {current_user.username}! Welcome to the admin page."
    )


@router.get("/user")
@PermissionChecker(["user"])
async def user_info(
    current_user: UserBase = Depends(get_current_user),
) -> MessageResponse:
    return MessageResponse(
        message=f"Hello, {current_user.username}! Welcome to the user page."
    )


@router.get("/about_me")
async def about_me(current_user: UserBase = Depends(get_current_user)) -> UserBase:
    return current_user


@router.get("/protected_resource")
@PermissionChecker(["admin", "user"])
async def get_protected_resource(
    current_user: UserBase = Depends(get_current_user),
) -> MessageResponse:
    msg = f"You got access to the protected resource, welcome, {current_user.username}"
    return MessageResponse(message=msg)
