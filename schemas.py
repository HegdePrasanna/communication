from pydantic import BaseModel, Field


class MessageSend(BaseModel):
    message: str = Field(...)
    is_reply: bool = Field(default=False)
    to_message: int = Field(None)
    user_grp_id: int = Field(None)
    user_id: int = Field(...)
    group_id: int = Field(...)