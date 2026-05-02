from datetime import datetime

from bson import ObjectId

from lgt_jobs.lgt_data.models.base import BaseModel


class ScheduledMessage(BaseModel):
    post_at: datetime
    bot_id: ObjectId
    user_id: ObjectId
    sender_id: str
    text: str | None
    files: list
