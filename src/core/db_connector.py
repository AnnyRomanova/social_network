import logging
from fastapi import Request
from pydantic_settings import BaseSettings

import psycopg2

logger = logging.getLogger(__name__)

class DatabaseConfig(BaseSettings):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    DB: str

    def make_connection(self):
        logger.debug(f"Connecting with: host={self.HOST}, port={self.PORT}, user={self.USER}, db={self.DB}")
        connection = psycopg2.connect(
            host=self.HOST,
            user=self.USER,
            password=self.PASSWORD,
            database=self.DB
        )
        return connection

class Settings(BaseSettings):
    DB: DatabaseConfig

    class Config:
        env_nested_delimiter = '__'


settings = Settings()

def get_db(request: Request):
    logger.info("Connection to DataBase")
    connection = request.app.state.db_connection
    yield connection