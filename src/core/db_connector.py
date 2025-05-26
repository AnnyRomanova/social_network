import logging

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

def get_db():
    logger.info("Connection to DataBase")
    connection = settings.DB.make_connection()
    try:
        yield connection
    finally:
        connection.close()