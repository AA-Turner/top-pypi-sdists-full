from lgt_jobs.lgt_data.models.base import BaseModel
from lgt_jobs.lgt_data.models.post.message import PostMessage


class Post(BaseModel):
    messages: list[PostMessage]
    title: str

    @classmethod
    def from_dic(cls, dic: dict):
        if not dic:
            return None
        model: Post | None = super().from_dic(dic)
        model.messages = [PostMessage.from_dic(message) for message in dic.get('messages', [])]
        return model
