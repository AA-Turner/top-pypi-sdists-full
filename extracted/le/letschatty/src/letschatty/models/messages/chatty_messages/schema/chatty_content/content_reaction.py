from pydantic import BaseModel

class ChattyContentReaction(BaseModel):
    # Empty string = reaction removal (mirrors MetaReactionContent).
    # chat_getter.py and get_caption_or_body_or_preview.py branch on truthiness.
    emoji: str = ""

    def get_body_or_caption(self) -> str:
        return self.emoji