from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel


@dataclass
class Message:
    msg_id: int
    read_ct: int  # 被读取的次数。
    enqueued_at: datetime
    vt: datetime
    message: dict


class MessagePublic(BaseModel):
    msg_id: int
    read_ct: int  # 被读取的次数。
    enqueued_at: datetime
    vt: datetime
    message: dict


class MessagePullItem(BaseModel):
    queue: str
    limit: int = 1


class MessagePullReq(BaseModel):
    items: list[MessagePullItem]


class MessagePullResponseItem(BaseModel):
    queue: str
    messages: list[MessagePublic]


class MessagePullResponse(BaseModel):
    data: list[MessagePullResponseItem]


class MessageSendPublic(BaseModel):
    queue: str
    messages: list[dict]


class MessageAckRequest(BaseModel):
    queue: str
    msg_ids: list[str]
