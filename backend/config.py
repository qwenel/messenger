from urllib.parse import urlparse

import yaml
import logging

try:
    with open("config/settings.yaml") as file:
        settings = yaml.load(file, Loader=yaml.FullLoader)
        for row in settings:

            if settings.get("DATABASE_URI") is not None:
                DATABASE_URI = settings.get("DATABASE_URI")
                ASYNC_DATABASE_URI = settings.get("DATABASE_URI").replace(
                    "postgresql://", "postgresql+asyncpg://", 1)

            if settings.get("DATABASE_SCHEME") is not None:
                DATABASE_SCHEME = settings.get("DATABASE_SCHEME")

            if settings.get("LOCAL_ADDRESS") is not None:
                LOCAL_ADDRESS = settings.get("LOCAL_ADDRESS")
                LOCAL_HOST = urlparse(LOCAL_ADDRESS).hostname
                LOCAL_PORT = urlparse(LOCAL_ADDRESS).port


except FileNotFoundError:
    logging.warning("Файл settings.yaml не найден: используются настройки по умолчанию")
except Exception as e:
    raise e
