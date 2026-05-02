from pydantic import BaseModel, Field
from enum import StrEnum
from typing import Optional, List



class CentralNotificationStatus(StrEnum):
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    INFO = "info"
    INFO_HIGHLIGHTED = "info_highlighted"

# Soolo se generan DESDE LA BASE DE DATOS

class ChattyContentCentral(BaseModel):
    body: str
    status: Optional[CentralNotificationStatus] = Field(default=CentralNotificationStatus.INFO)
    calls_to_action: Optional[List[str]] = None

    def model_dump(self, *args, **kwargs):
        kwargs['exclude_unset'] = True
        return super().model_dump(*args, **kwargs)

    def get_body_or_caption(self) -> str:
        return self.body