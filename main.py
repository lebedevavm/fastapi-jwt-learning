# this project is solution to tasks:
# https://stepik.org/lesson/1044675/step/12?unit=1053249
# https://stepik.org/lesson/1044675/step/13?unit=1053249
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from extensions import limiter
from routers import router as router_users
from database import lifespan, init_db
from services import get_user_from_token
from schemas import MessageResponse


init_db()

app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.include_router(router_users)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Too many requests"})


@app.get("/protected_resource")
async def get_protected_resource(username: str = Depends(get_user_from_token)):
    return MessageResponse(
        message=f"You got access to the protected resource, welcome, {username}"
    )
