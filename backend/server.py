import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.staticfiles import StaticFiles

from app.api.routes import main_router
from app.api.websockets import websockets_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    logging.info("server is running")
    yield


app = FastAPI(lifespan=lifespan)

# Получаем абсолютный путь к папке 'frontend/static'
static_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "static")

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все домены (или укажите конкретные)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (включая WebSocket)
    allow_headers=["*"],  # Разрешить все заголовки
)
app.include_router(main_router)
app.include_router(websockets_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
