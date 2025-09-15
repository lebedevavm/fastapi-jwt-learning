from typing import Any
from sqlalchemy import insert, select

from database import database
from models import User
from schemas import RoleName


async def create_user(name: str, password_hash: str, role: RoleName) -> int:
    """
    Add a new user in DB.
    :param name: name for new user
    :param password_hash: hash for password for new user
    :param role: role for new user
    :return: int: id created user
    """
    query = insert(User).values(username=name, password_hash=password_hash, role=role)
    return await database.execute(query)


async def get_user(user_id: int) -> dict[str, Any] | None:
    """
    Get information for user from DB.
    :param user_id: user id
    :return: information for user or None if user doesn't exist
    """
    query = select(User).where(User.id == user_id)
    record = await database.fetch_one(query)
    return dict(record) if record else None


async def get_user_by_name(user_name: str) -> dict[str, Any] | None:
    """
    Get information for user by user name from DB.
    :param user_name: user name
    :return: information for user or None if user doesn't exist
    """
    query = select(User).where(User.username == user_name)
    record = await database.fetch_one(query)
    return dict(record) if record else None
