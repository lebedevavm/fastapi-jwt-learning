# this project is solution to tasks:
# https://stepik.org/lesson/1044675/step/12?unit=1053249
# https://stepik.org/lesson/1044675/step/13?unit=1053249
# https://stepik.org/lesson/1044675/step/14?unit=1053249
# https://stepik.org/lesson/1044676/step/11?unit=1053250

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from extensions import limiter
from routers.users import router as router_users
from routers.main_routers import router as router_main
from database import lifespan, init_db


init_db()

app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.include_router(router_users)
app.include_router(router_main)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Too many requests"})
