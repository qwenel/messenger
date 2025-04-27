from fastapi.routing import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from app.chat_manager import connection_manager, user_manager

websockets_router = APIRouter()


@websockets_router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):

    user = user_manager.users.get(client_id)

    await connection_manager.connect(websocket)

    try:
        while True:
            text = await websocket.receive_text()
            await connection_manager.broadcast(f"{user.name}: {text}")
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        await connection_manager.broadcast(f"{client_id} покинул чат")
