from typing import Dict
from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session

from app.database import get_db
from .auth import get_current_user
import app.utils.exceptions as exceptions
from app import models,schemas

router = APIRouter(
    tags=["Todo APIs"],
    prefix="/todos",
    responses={404: {"description": "Not found"}}
)

@router.get("/")
async def get_all_todos_by_user(user: Dict = Depends(get_current_user), 
                            db: Session = Depends(get_db)):
    if user is None:
        raise exceptions.get_user_exception()

    return db.query(models.Todos)\
            .filter(models.Todos.owner_id == user.get("id"))\
            .all()



@router.get("/{id}")
async def get_todo_by_id(id: int, 
                    db: Session = Depends(get_db),
                    user: Dict = Depends(get_current_user)):

    if user is None:
        raise exceptions.get_user_exception()

    todo_model = db.query(models.Todos)\
        .filter(models.Todos.id == id)\
        .filter(models.Todos.owner_id == user.get("id"))\
        .first()

    if todo_model is None:
        raise exceptions.todo_not_found_exception(id)
    
    return todo_model

    

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: schemas.Todo, 
                      db: Session = Depends(get_db),
                      user: Dict = Depends(get_current_user)):

    if user is None:
        raise exceptions.get_user_exception()

    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.owner_id = user.get("id")

    db.add(todo_model)
    db.commit()

    return {"message":"Successful"}


@router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def update_todo(id: int, 
                      todo: schemas.Todo,
                      db: Session = Depends(get_db),
                      user: Dict = Depends(get_current_user)):

    if user is None:
        raise exceptions.get_user_exception()

    todo_model = db.query(models.Todos)\
        .filter(models.Todos.id == id)\
        .filter(models.Todos.owner_id == user.get("id"))\
        .first()

    if todo_model is None:
        raise exceptions.todo_not_found_exception(id)
    
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()

    return {"message":"Successful"}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(id: int, 
                      db: Session = Depends(get_db),
                      user: Dict = Depends(get_current_user)):

    if user is None:
        raise exceptions.get_user_exception()

    todo_model = db.query(models.Todos)\
        .filter(models.Todos.id == id)\
        .filter(models.Todos.owner_id == user.get("id"))\
        .first()

    if todo_model is None:
        raise exceptions.todo_not_found_exception(id)
    
    db.query(models.Todos)\
        .filter(models.Todos.id == id)\
        .delete()

    db.commit()
