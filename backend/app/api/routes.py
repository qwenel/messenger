from fastapi import Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter

from app.chat_manager import user_manager


main_router = APIRouter()

templates = Jinja2Templates(directory="../frontend/")


@main_router.get("/")
async def entrance(request: Request):
    """
    Корневой роут мессенджера, перенаправляющий пользователя на страницу регистрации/входа, если он не прошел авторизацию
    и на главную страницу мессенджера в ином случае

    :param request: FastAPI объект входящего запроса
    :type request: fastapi.Request

    :return: HTML страница авторизации (login.html)
    :rtype: fastapi.templating.Jinja2Templates.TemplateResponse
    :return: Перенаправление запроса на страницу пользователя 
    :rtype: fastapi.responses.RedirectResponse
    """
    user = await user_manager.get_user(host=request.client.host)
    if user is None:
        return templates.TemplateResponse("login.html", {"request": request, "error": None})

    return RedirectResponse(url=f"/{user.user_id}", status_code=302)

@main_router.get("/login")
async def login_template(request: Request, error: str = None):
    """
    Роут авторизации пользователя

    :param request: FastAPI объект входящего запроса
    :type request: fastapi.Request
    :param error: Ошибка, с которой мог поступить запрос (неверный пароль, логин или др.)
    :type error: str

    :return: HTML страница авторизации (login.html)
    :rtype: fastapi.templating.Jinja2Templates.TemplateResponse
    """
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@main_router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    """
    Отправка заполненных полей логина и пароля для прохождения авторизации
    В случае неудачи пользователь получит сообщение (Неверный логин или пароль)
    В случае успеха будет перенаправлен на главную страницу 

    :param request: FastAPI объект входящего запроса
    :type request: fastapi.Request
    :param username: Логин пользователя
    :type username: str
    :param password: Пароль пользователя
    :type password: str

    :return: HTML страница авторизации (login.html)
    :rtype: fastapi.templating.Jinja2Templates.TemplateResponse
    :return: Перенаправление запроса на страницу пользователя 
    :rtype: fastapi.responses.RedirectResponse
    """
    user = await user_manager.get_user(name=username)

    if user is None:
        result = await user_manager.register(name=username, host=request.client.host, password=password)
        if result["code"] == 0:
            return templates.TemplateResponse("login.html", {"request": request, "error": result["message"]})
        return RedirectResponse(url=f"""/{result["id"]}""", status_code=302)

    result = await user_manager.login(name=username, password=password, host=request.client.host)
    if result["code"] == 0:
        return templates.TemplateResponse("login.html", {"request": request, "error": result["message"]})
    return RedirectResponse(url=f"""/{result["id"]}""", status_code=302)

@main_router.get("/{client_id}")
async def chat(request: Request, client_id: str):
    """
    Главная страница мессенджера, где может находится только авторизованный пользователь
    При попытке входа неавторизованный пользователь будет перенаправлен на страницу авторизации

    :param request: FastAPI объект входящего запроса
    :type request: fastapi.Request
    :param client_id: Идентификатор пользователя
    :type client_id: str

    :return: HTML страница авторизации (login.html)
    :rtype: fastapi.templating.Jinja2Templates.TemplateResponse
    :return: HTML главной страницы мессенджера (chat_room.html)
    :rtype: fastapi.templating.Jinja2Templates.TemplateResponse
    """
    user = user_manager.users.get(client_id)

    if user is None:
        return templates.TemplateResponse("login.html", {"request": request, "error": None})

    return templates.TemplateResponse(
        "chat_room.html", {"request": request, "client_id": client_id, "username": user.name})
