from pydantic import BaseModel

class ChattyContentButton(BaseModel):
    text: str
    payload: str

    def get_body_or_caption(self) -> str:
        return f"Button: {self.text}"