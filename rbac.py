from fastapi import HTTPException, status
from functools import wraps
from schemas import RoleName


class PermissionChecker:
    def __init__(self, roles: list[str]):
        self.roles = roles

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = kwargs.get("current_user")
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Authentication required",
                )

            if user.role == RoleName.admin:
                return await func(*args, **kwargs)

            if user.role not in self.roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough rights to access",
                )
            return await func(*args, **kwargs)

        return wrapper
