from datetime import datetime
from typing import Optional

from bson import ObjectId

from lgt_jobs.lgt_data.models.chat.message import ChatMessage
from lgt_jobs.lgt_data.models.people.people import SlackMemberInformation


class UserContact(SlackMemberInformation):
    chat_id: str
    user_id: ObjectId
    source_id: str
    last_message_at: Optional[datetime]

    @classmethod
    def from_dic(cls, dic: dict):
        if not dic:
            return None
        model: UserContact | None = super().from_dic(dic)
        model.chat_history = [ChatMessage.from_dic(message) for message in dic.get('chat_history', [])]
        return model
