from sqlalchemy import Column, Integer, String

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(length=70), unique=True, nullable=False)
    password_hash = Column(String(length=250), nullable=False)
    role = Column(String(length=20), nullable=False, server_default="guest")
