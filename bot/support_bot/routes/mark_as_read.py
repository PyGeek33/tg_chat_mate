from aiohttp import web
from aiohttp.web_request import Request

from support_bot import db
from support_bot.misc import (
    get_manager_from_request,
    set_cors_headers,
    web_routes,
)
from support_bot.routes.utils import require_auth


@web_routes.post("/tg-bot/mark-as-read")
@require_auth
async def mark_message_as_read(request: Request):
    payload = await request.json()
    modified_count = await db.message.mark_as_read(
        payload.get("chat_id"), payload.get("message_id")
    )
    response = web.json_response(
        {"result": "Marked!", "modified_count": modified_count}, status=200
    )
    return set_cors_headers(response)


@web_routes.post("/tg-bot/mark-chat-as-read")
async def mark_chat_as_read(request: Request):
    payload = await request.json()
    manager = get_manager_from_request(request)
    if manager is None:
        response = web.json_response(
            {"result": "AuthorizationToken", "modified_count": 0}, status=401
        )
        return set_cors_headers(response)

    payload = await request.json()
    chat_id = payload.get("chat_id")
    modified_count = await db.message.mark_chat_as_read(chat_id)
    response = web.json_response(
        {"result": "Marked!", "modified_count": modified_count}, status=200
    )
    return set_cors_headers(response)
