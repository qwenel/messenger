from urllib import request

from fastapi import Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter

from app.chat_manager import user_manager


main_router = APIRouter()

templates = Jinja2Templates(directory="../frontend/")


@main_router.get("/")
async def entrance(request: Request):
    user = await user_manager.get_user(host=request.client.host)
    if user is None:
        return templates.TemplateResponse("login.html", {"request": request, "error": None})

    return RedirectResponse(url=f"/{user.user_id}", status_code=302)

@main_router.get("/login")
async def login_template(request: Request, error: str = None):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@main_router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):

    user = await user_manager.get_user(name=username)

    if user is None:
        result = await user_manager.register(name=username, host=request.client.host, password=password)
        if result["code"] == 0:
            return templates.TemplateResponse("login.html", {"request": request, "error": result["message"]})
        return RedirectResponse(url=f"""/{result["id"]}""", status_code=302)

    result = await user_manager.login(name=username, password=password)
    if result["code"] == 0:
        return templates.TemplateResponse("login.html", {"request": request, "error": result["message"]})
    return RedirectResponse(url=f"""/{result["id"]}""", status_code=302)

@main_router.get("/{client_id}")
async def chat(request: Request, client_id: str):

    user = user_manager.users.get(client_id)

    if user is None:
        return templates.TemplateResponse("login.html", {"request": request, "error": None})

    return templates.TemplateResponse(
        "chat_room.html", {"request": request, "client_id": client_id, "username": user.name})