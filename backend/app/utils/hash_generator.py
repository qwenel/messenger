import hashlib


async def get_sha256_hash(input_string):
    """
    Функция для получения SHA-256 хэша из строки.

    :param input_string: Исходная строка для хэширования.
    :return: Хэш в виде шестнадцатеричной строки.
    """
    sha256_hash = hashlib.sha256()

    sha256_hash.update(input_string.encode('utf-8'))

    return sha256_hash.hexdigest()


async def get_sha256_hash_chat(input_string):
    """
    Функция для получения SHA-256 хэша из строки для создания чата.

    :param input_string: Исходная строка для хэширования.
    :return: Хэш в виде шестнадцатеричной строки.
    """
    sha256_hash = hashlib.sha256()

    sha256_hash.update(input_string.encode('utf-8'))

    return sha256_hash.hexdigest()