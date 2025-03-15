from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import main_router
from app.api.websockets import websockets_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("server is running")
    yield


app = FastAPI(lifespan=lifespan)

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
