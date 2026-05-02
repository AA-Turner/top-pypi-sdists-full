from typing import List

from lgt_jobs.lgt_data.models.chat.message import ChatMessage


class GroupedMessagesModel:
    messages: List[ChatMessage] = []

    @classmethod
    def from_dic(cls, dic: dict):
        if not dic:
            return None

        model = cls()
        model.messages = [ChatMessage.from_dic(message) for message in dic.get('messages', [])]
        return model
    