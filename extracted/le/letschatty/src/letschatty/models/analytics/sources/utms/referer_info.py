from pydantic import BaseModel, Field
from datetime import datetime
from ....utils.types.identifier import StrObjectId
from enum import StrEnum
from typing import Optional
from .utm_query_params import QueryUTMParams
class DeviceType(StrEnum):
    DESKTOP = "desktop"
    MOBILE = "mobile"
    TABLET = "tablet"
    UNKNOWN = "unknown"

class RefererInfo(BaseModel):
    url: str
    topic_id: StrObjectId
    button_id: str
    timestamp: datetime
    button_name: str = Field(default="")
    device_type: DeviceType = Field(default=DeviceType.UNKNOWN)
    contact_point_id: Optional[StrObjectId] = Field(default=None)
    client_ip_address: Optional[str] = Field(default=None)
    client_user_agent: Optional[str] = Field(default=None)
    client_external_id: Optional[str] = Field(default=None)

    @property
    def query_params(self) -> QueryUTMParams:
        return QueryUTMParams.from_url(self.url)
