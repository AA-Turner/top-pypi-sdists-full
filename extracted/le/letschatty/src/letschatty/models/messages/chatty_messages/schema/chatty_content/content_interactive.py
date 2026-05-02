from pydantic import BaseModel

class ChattyContentInteractive(BaseModel):
    pass

    def get_body_or_caption(self) -> str:
        return f"Interactive content"