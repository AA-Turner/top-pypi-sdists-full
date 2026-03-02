from typing import Optional

from pydantic import BaseModel


class UpdateBotConfiguration(BaseModel):
    bot_token: str
    orders_chat_id: Optional[int] = None


class UpdateBotChatId(BaseModel):
    chat_id: Optional[int] = None
