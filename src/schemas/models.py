from datetime import date

from pydantic import BaseModel


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    gender: str
    interests: str
    city: str
    password: str


class UserOUT(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: date
    gender: str
    interests: str
    city: str


class UserLogin(BaseModel):
    id: int
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str