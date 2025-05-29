import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.api.routers import router
from src.core.db_connector import settings

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Start and connecting to DataBase")
    connection = settings.DB.make_connection()
    app.state.db_connection = connection
    try:
        yield
    finally:
        logger.info("Closing DataBase at shutdown")
        connection.close()


app = FastAPI(lifespan=lifespan)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, log_config="core/logging.yaml")