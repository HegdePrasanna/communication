from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.openapi.utils import get_openapi
import json

from middlewares import ResponseTimeMiddleware
from router import msg_router
from ws_manager import WebSocketManager

app = FastAPI()
socket_manager = WebSocketManager()
app.add_middleware(ResponseTimeMiddleware)

app.include_router(msg_router, prefix="/api")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Communication Portal",
        version="0.0.1",
        summary="Seamless Communication with Websockets",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    openapi_schema["info"]["x-api-response-time"] = {
        "description": "Response time in seconds",
        "type": "number",
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.websocket("/ws/{room_id}/{user_id}")
async def group_chat(websocket: WebSocket, room_id: str, user_id: int):
    await socket_manager.add_user_to_room(room_id, websocket)
    message = {
        "user_id": user_id,
        "room_id": room_id,
        "message": f"User {user_id} connected to room - {room_id}"
    }
    await socket_manager.broadcast_to_room(room_id, json.dumps(message))
    try:
        while True:
            data = await websocket.receive_text()
            message = {
                "user_id": user_id,
                "room_id": room_id,
                "message": data
            }
            await socket_manager.broadcast_to_room(room_id, json.dumps(message))

    except WebSocketDisconnect:
        await socket_manager.remove_user_from_room(room_id, websocket)

        message = {
            "user_id": user_id,
            "room_id": room_id,
            "message": f"User {user_id} disconnected from room - {room_id}"
        }
        await socket_manager.broadcast_to_room(room_id, json.dumps(message))



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8100)
