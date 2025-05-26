import logging
from datetime import timedelta, datetime, timezone

from fastapi import Depends
from jose import jwt
from passlib.context import CryptContext

from src.core.db_connector import get_db

logger = logging.getLogger(__name__)

class AccessHandler:
    def __init__(
        self,
        pwd_context=None,
        secret_key="test_secret_key",
        algorithm="HS256",
        access_token_expire_minutes=30,
    ):
        self.pwd_context = pwd_context or CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes

    # метод сравнивает, верный ли пароль ввел пользователь
    def verify_password(self, plain_password, hashed_password):
        logger.info("Password verification")
        return self.pwd_context.verify(plain_password, hashed_password)

    # метод для хэширования пароля
    def get_password_hash(self, password: str) -> str:
        logger.info("Request to hash password")
        return self.pwd_context.hash(password)

    # метод на проверку существования юзера
    # и верный ли пароль
    def authenticate_user(self, user_id: int, password: str, db=Depends(get_db)):
        logger.info("Request to authentication")
        with db.cursor() as cursor:
            cursor.execute("SELECT id, hashed_password FROM users WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            if not result:
                return False
            db_id, db_hashed_password = result
            if not self.verify_password(password, db_hashed_password):
                return False
            return {
                "id": db_id,
                "hashed_password": db_hashed_password,
            }

    # создание токена
    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        logger.info("Creating an access token")
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=self.access_token_expire_minutes))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt


# access_object: AccessHandler | None = None


def get_access_handler() -> AccessHandler:
    # assert access_object is not None, "Access_object not initialized"
    return AccessHandler()