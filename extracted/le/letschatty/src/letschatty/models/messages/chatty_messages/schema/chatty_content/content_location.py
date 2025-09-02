from pydantic import BaseModel

class ChattyContentLocation(BaseModel):
    latitude: float
    longitude: float

    def get_body_or_caption(self) -> str:
        return f"Location: {self.latitude}, {self.longitude}"