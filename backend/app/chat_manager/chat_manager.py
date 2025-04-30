from fastapi import WebSocket


class ConnectionManager:
    """
    Класс предназначенный для менеджмента соединений
    Ответственен за их обработку, хранение и обновление(подключение, отключение)
    """
    def __init__(self):
        """
        Метод, инициализирующий список активных соединений

        :return: None
        """
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """
        Метод, добавляющий в список новое соединение

        :param WebSocket: Вебсокет соединение
        :type WebSocket: fastapi.WebSocket

        :return: None
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """
        Метод, удаляющий из списка отключенное соединение

        :param WebSocket: Вебсокет соединение
        :type WebSocket: fastapi.WebSocket

        :return: None
        """
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """
        Метод, отправляющий сообщение по конкретному соединению

        :param message: Отправляемое сообщение
        :type message: str
        :param WebSocket: Вебсокет соединение
        :type WebSocket: fastapi.WebSocket
        
        :return: None
        """
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        """
        Метод, отправляющий сообщение всем в списке активных соединений

        :param message: Отправляемое сообщение
        :type message: str

        :return: None
        """
        for connection in self.active_connections:
            await connection.send_text(message)