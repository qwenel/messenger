from typing import Any

from app.utils.hash_generator import get_sha256_hash


class User:
    """
    Класс для описания объекта Пользователя, содержит в себе следующую информацию:
        name (логин, имя)
        password (пароль)
        user_id (уникальный идентификатор пользователя)
        hosts (подключенные устройства пользователя)
    """
    def __init__(self, name: str, password: str, user_id: str):
        """
        Метод для создания объекта пользователя

        :param name: Имя пользователя (логин)
        :type name: str
        :param password: Пароль пользователя
        :type password: str
        :param user_id: Идентификатор пользователя
        :type user_id: str
        """
        self.name = name
        self.password = password
        self.user_id = user_id
        self.hosts = set()


class UserManager:
    """
    Класс описывающий Менеджера обработчика пользователей
    """
    def __init__(self):
        """
        Метод для создания менеджера пользователей
        Создает пустой словарь пользователей
        """
        self.users = {}

    async def get_user(self, name: str = None, host: str = None) -> "User":
        """
        Метод для получения объекта пользователя по имени
        
        :param name: Имя пользователя (логин)
        :type name: str
        :param host: Адрес устройства пользователя
        :type host: str
        
        :return User: Объект найденного по имени пользователя
        :rtype: User
        :return None: Пользователь не найден
        """
        if name is None:
            for user in self.users.values():
                if host in user.hosts:
                    return user
            return None

        user_id = await get_sha256_hash(name)
        return self.users.get(user_id)

    async def register(self, name: str, host: str, password: str):
        """
        Метод для регистрации нового пользователя

        :param name: Имя пользователя (логин)
        :type name: str
        :param host: Адрес устройства пользователя
        :type host: str
        :param password: Пароль пользователя
        :type password: str
        
        :return dict: Возвращаем информацию об успешном прохождении регистрации
        :rtype: dict
        :return dict: Возвращаем информацию о неудачном прохождении регистрации
        :rtype: dict
        """
        user_id = await get_sha256_hash(name)

        if self.users.get(user_id) is not None:
            return {"code": 0, "message": "Имя занято, попробуйте другое"}

        self.users[user_id] = User(name, password, user_id)
        self.users[user_id].hosts.add(host)
        return {"code": 1, "message": f"Пользователь {name} успешно зарегистрирован", "id": user_id}

    async def login(self, name: str, password: str, host: str) -> dict[str, Any]:
        """
        Метод для авторизации пользователя

        :param name: Имя пользователя (логин)
        :type name: str
        :param password: Пароль пользователя
        :type password: str
        :param host: Адрес устройства пользователя
        :type host: str
        
        :return dict: Возвращаем информацию об успешном прохождении авторизации
        :rtype: dict
        :return dict: Возвращаем информацию о неудачном прохождении авторизации
        :rtype: dict
        """
        user_id = await get_sha256_hash(name)

        if self.users.get(user_id) is None or self.users.get(user_id).password != password:
            return {"code": 0, "message": "Логин или пароль введены неверно"}

        self.users[user_id].hosts.add(host)
        return {"code": 1, "message": "Пользователь авторизован", "id": user_id}

    async def remove_user(self, user: User):
        """
        Метод для удаления пользователя из мессенджера

        :param user: Объект пользователя
        :type user: User
        """
        del self.users[user.user_id]
