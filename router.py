from fastapi import APIRouter, Depends, status, Response, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
import json
from db import get_db
from services import get_messages, create_message
from ws_manager import WebSocketManager
from schemas import MessageSend


msg_router = APIRouter(
    tags=["Messages"], prefix="/message"
)


# @msg_router.get("", responses={404: {"model": ReturnResponseFailure}, 200: {"model": ReturnResponseSuccess}})
@msg_router.get("")
async def get_all_messages(response: Response, db: Session = Depends(get_db)):
    """
    Get All Active Messages
    """
    messages = await get_messages(db)
    return messages


@msg_router.post("/send/{room_id}")
async def get_all_messages(message: MessageSend, room_id:int, response: Response, db: Session = Depends(get_db)):
    """
    Send New Message
    """
    socket_manager = WebSocketManager()

    created_message = await create_message(message, db)
    # print(type(created_message))
    # print(type(created_message.__dict__))
    # print(MessageSend(created_message))
    # Get the message data as a dictionary
    message_data = (created_message.__dict__)
    del message_data['_sa_instance_state']
    message_data = MessageSend(**created_message.__dict__).model_dump()
    
    # Convert the message data to JSON
    # return
    message_json = json.dumps(message_data)

    # Broadcast the message to the specified room_id
    await socket_manager.broadcast_to_room_from_restapi(str(room_id), message_json)

    # await socket_manager.broadcast_to_room(str(room_id), messages)
    return created_message