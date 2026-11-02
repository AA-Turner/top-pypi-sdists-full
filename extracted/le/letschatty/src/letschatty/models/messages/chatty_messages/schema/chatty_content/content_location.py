from typing import Optional
from pydantic import BaseModel


class ChattyContentLocation(BaseModel):
    latitude: float
    longitude: float
    name: Optional[str] = None
    address: Optional[str] = None
    url: Optional[str] = None

    def get_body_or_caption(self) -> str:
        if self.name and self.address:
            return f"{self.name} - {self.address}"
        if self.name:
            return self.name
        if self.address:
            return self.address
        return f"Location: {self.latitude}, {self.longitude}"