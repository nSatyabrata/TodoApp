from typing import Optional
from fastapi import Depends, APIRouter
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError

import app.models as models
from app.database import get_db
from app.config import settings
import app.utils.exceptions as exceptions

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.access_token_expire_minutes)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter(
    tags=["Authentication APIs"],
    prefix="/auth",
    responses={401: {"description": "Not authorized"}}
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def get_hashed_password(password: str) -> str:
    """ Takses in normal password, 
        returns hashed password using bcrypt hash method. """

    return bcrypt_context.hash(password)



def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Takes in normal password and hashed password, 
        verfiy password using bcrypt verify method. """

    return bcrypt_context.verify(plain_password, hashed_password)



def authenticate_user(username: str, password: str, db: Session) -> models.Users:
    """ Takes in username, password and database session,
        return authenicated user."""

    user = db.query(models.Users)\
        .filter(models.Users.username == username)\
        .first()

    if not user or not verify_password(password, user.hashed_password):
        return False
    return user



def create_access_token(username: str, user_id: int,
                        expires_delta: Optional[timedelta] = None):
    """ Takes in username, user id and expires,
        returns token"""

    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({"exp":expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)



async def get_current_user(token: str = Depends(oauth2_bearer)):
    """ Takes in generated token, returns current username and user id."""

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        user_id: int = payload.get("id")

        if username is None or user_id is None:
            raise exceptions.get_user_exception()

        return {"username": username, "id": user_id}
    except JWTError:
        raise exceptions.get_user_exception()


@router.post("/generateToken")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise exceptions.token_exception()

    token = create_access_token(user.username, user.id)

    return {"token": token}

