from pydantic import BaseModel, Field
from typing import Optional


class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="The priority must be between 1 to 5")
    complete: bool

class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str

class UserOut(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str

    class Config:
        orm_mode=True
