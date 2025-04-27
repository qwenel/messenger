from fastapi import WebSocket

from backend.app.utils.hash_generator import get_sha256_hash_chat


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


class ChatManager:
    def __init__(self):
        self.chats_list = {}



class Chat:
    def __init__(self):
        self.id = None
        self.admin_user = None
        self.users_list = []

    async def create(self, admin_user):
        self.id = await get_sha256_hash_chat(admin_user)
        self.users_list.append(admin_user)
        self.admin_user = admin_user

