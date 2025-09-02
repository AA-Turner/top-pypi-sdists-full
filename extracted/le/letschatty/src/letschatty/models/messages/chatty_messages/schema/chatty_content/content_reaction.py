from pydantic import BaseModel

class ChattyContentReaction(BaseModel):
    emoji: str

    def get_body_or_caption(self) -> str:
        return self.emoji