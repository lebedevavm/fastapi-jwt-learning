from slowapi import Limiter
from security import get_username_from_request

limiter = Limiter(key_func=get_username_from_request)
