from typing import Dict
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from . auth import get_hashed_password, get_current_user
from app.database import get_db
import app.utils.exceptions as exceptions


router = APIRouter(
    tags=["User APIs"],
    prefix="/user"
)

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def user_signup(create_user: schemas.CreateUser, db: Session = Depends(get_db)):
    user_model = models.Users()
    user_model.email = create_user.email
    user_model.username = create_user.username
    user_model.first_name = create_user.first_name
    user_model.last_name = create_user.last_name
    user_model.hashed_password = get_hashed_password(create_user.password) 
    user_model.is_active = True

    db.add(user_model)
    db.commit()

    return {"message":"Successful"}


@router.get("/details", response_model=schemas.UserOut)
async def get_user_details(db: Session = Depends(get_db),
                           user: Dict = Depends(get_current_user)):
    
    if user is None:
        raise exceptions.get_user_exception()
    
    return db.query(models.Users)\
                    .filter(models.Users.id == user.get("id"))\
                    .first()


@router.delete("/remove", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: Session = Depends(get_db),
                      user: Dict = Depends(get_current_user)):

    if user is None:
        raise exceptions.get_user_exception()

    user_model = db.query(models.Users)\
            .filter(models.Users.id == user.get("id"))\
            .first()
 
    if user_model is None:
        raise exceptions.user_not_exist_exception()
    
    db.query(models.Users)\
            .filter(models.Users.id == user.get("id"))\
            .delete()
    db.commit()  