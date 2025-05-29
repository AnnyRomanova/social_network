from datetime import timedelta

from fastapi import HTTPException

from fastapi import Depends, APIRouter, FastAPI

from src.schemas.models import UserCreate, UserOUT, UserLogin, Token
from src.core.db_connector import get_db
from src.controllers.password_controller import AccessHandler, get_access_handler

router = APIRouter()
app = FastAPI()
app.include_router(router)
access_handler = AccessHandler()

@router.post("/user/register", status_code=201, response_model=UserOUT)
async def register_user(user_data: UserCreate, access_object: AccessHandler = Depends(get_access_handler), db = Depends(get_db)) -> UserOUT:
    with db.cursor() as cursor:
        cursor.execute(
            "INSERT INTO users (first_name, last_name, birth_date, gender, interests, city, hashed_password)" 
            "VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;",
            (user_data.first_name,
            user_data.last_name,
            user_data.birth_date,
            user_data.gender,
            user_data.interests,
            user_data.city,
            access_object.get_password_hash(user_data.password))
        )
        id = cursor.fetchone()[0]
        db.commit()

        return UserOUT(
            id=id,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            birth_date=user_data.birth_date,
            gender=user_data.gender,
            interests=user_data.interests,
            city=user_data.city
        )


@router.get("/user/get/{user_id}", response_model=UserOUT)
async def get_user_profile(user_id: int, db=Depends(get_db), current_user: str = Depends(access_handler.get_current_user)) -> UserOUT:
    with db.cursor() as cursor:
        cursor.execute("SELECT id, first_name, last_name, birth_date, gender, interests, city FROM users WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        return UserOUT(
            id=row[0],
            first_name=row[1],
            last_name=row[2],
            birth_date=row[3],
            gender=row[4],
            interests=row[5],
            city=row[6]
        ) if row else {"error": "not found"}


@router.post("/login", response_model=Token)
async def login(login_data: UserLogin, access_object: AccessHandler = Depends(get_access_handler), db=Depends(get_db)):
    user = access_object.authenticate_user(login_data.id, login_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail=f"Incorrect id or password")
    access_token = access_object.create_access_token(
        data={"sub": str(user["id"])},
        expires_delta=timedelta(minutes=access_object.access_token_expire_minutes)
    )
    return {"access_token": access_token, "token_type": "bearer"}