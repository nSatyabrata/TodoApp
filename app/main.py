from fastapi import FastAPI

from app import models
from app.database import engine
from .routers import auth, todo, user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(todo.router)


