# this project is solution to task
# https://stepik.org/lesson/1044675/step/12?unit=1053249
from fastapi import FastAPI
from fastapi import Depends

from routers import router as router_users
from database import lifespan, init_db
from services import get_user_from_token
from schemas import MessageResponse


init_db()

app = FastAPI(lifespan=lifespan)
app.include_router(router_users)


@app.get("/protected_resource")
async def get_protected_resource(username: str = Depends(get_user_from_token)):
    return MessageResponse(
        message=f"You got access to the protected resource, welcome, {username}"
    )
