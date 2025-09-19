from fastapi import APIRouter, Depends, Request

from rbac import PermissionChecker
from dependencies import get_current_user, get_rate_limit_by_role
from schemas import MessageResponse, UserBase
from extensions import limiter

router = APIRouter(prefix="/resources")


@router.get("/admin")
@PermissionChecker(["admin"])
@limiter.limit(get_rate_limit_by_role)
async def admin_info(
    request: Request,
    current_user: UserBase = Depends(get_current_user),
) -> MessageResponse:
    return MessageResponse(
        message=f"Hello, {current_user.username}! Welcome to the admin page."
    )


@router.get("/user")
@PermissionChecker(["user"])
@limiter.limit(get_rate_limit_by_role)
async def user_info(
    request: Request,
    current_user: UserBase = Depends(get_current_user),
) -> MessageResponse:
    return MessageResponse(
        message=f"Hello, {current_user.username}! Welcome to the user page."
    )


@router.get("/guest")
@PermissionChecker(["guest"])
@limiter.limit(get_rate_limit_by_role)
async def guest_info(
    request: Request,
    current_user: UserBase = Depends(get_current_user),
) -> MessageResponse:
    return MessageResponse(
        message=f"Hello, {current_user.username}! Welcome to the guest page."
    )


@router.get("/about_me")
@limiter.limit(get_rate_limit_by_role)
async def about_me(
    request: Request, current_user: UserBase = Depends(get_current_user)
) -> UserBase:
    return current_user


@router.get("/protected_resource")
@PermissionChecker(["admin", "user"])
@limiter.limit(get_rate_limit_by_role)
async def get_protected_resource(
    request: Request,
    current_user: UserBase = Depends(get_current_user),
) -> MessageResponse:
    msg = f"You got access to the protected resource, welcome, {current_user.username}"
    return MessageResponse(message=msg)
