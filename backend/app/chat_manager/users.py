from typing import Any

from app.utils.hash_generator import get_sha256_hash


class User:
    def __init__(self, name: str, password: str, user_id: str):
        self.name = name
        self.password = password
        self.user_id = user_id
        self.hosts = set()


class UserManager:
    def __init__(self):
        self.users = {}

    async def get_user(self, name: str = None, host: str = None) -> "User":
        if name is None:
            for user in self.users.values():
                if host in user.hosts:
                    print(user)
                    return user
            return None

        user_id = await get_sha256_hash(name)
        return self.users.get(user_id)

    async def register(self, name: str, host: str, password: str):
        user_id = await get_sha256_hash(name)

        if self.users.get(user_id) is not None:
            return {"code": 0, "message": "Имя занято, попробуйте другое"}

        self.users[user_id] = User(name, password, user_id)
        self.users[user_id].hosts.add(host)
        return {"code": 1, "message": f"Пользователь {name} успешно зарегистрирован", "id": user_id}

    async def login(self, name: str, password: str, host: str) -> dict[str, Any]:
        user_id = await get_sha256_hash(name)

        if self.users.get(user_id) is None or self.users.get(user_id).password != password:
            return {"code": 0, "message": "Логин или пароль введены неверно"}

        self.users[user_id].hosts.add(host)
        return {"code": 1, "message": "Пользователь авторизован", "id": user_id}

    async def remove_user(self, user: User):
        del self.users[user.user_id]
