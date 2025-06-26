from datetime import datetime, timezone
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional
from .request import RequestContext
from .token import MaleoFoundationTokenGeneralTransfers
from maleo_foundation.enums import BaseEnums
from maleo_foundation.types import BaseTypes

class DatabaseAccess(BaseModel):
    accessed_at: datetime = Field(datetime.now(tz=timezone.utc), description="Accessed at timestamp")
    request_id: UUID = Field(..., description="Request Id")
    request_context: RequestContext = Field(..., description="Request context")
    organization_id: BaseTypes.OptionalInteger = Field(None, ge=1, description="Organization Id")
    user_id: int = Field(0, ge=0, description="User Id")
    token_string: BaseTypes.OptionalString = Field(None, description="Token string")
    token_payload: Optional[MaleoFoundationTokenGeneralTransfers.DecodePayload] = Field(None, description="Token payload")
    service: BaseEnums.Service = Field(..., description="Service key")
    table: str = Field(..., description="Table name")
    data_id: int = Field(..., ge=1, description="Data Id")
    data: BaseTypes.StringToAnyDict = Field(..., description="Data")

    def to_google_pubsub_object(self) -> BaseTypes.StringToAnyDict:
        result = {
            "accessed_at": self.accessed_at.isoformat(),
            "request_id": str(self.request_id),
            "request_context": self.request_context.to_google_pubsub_object(),
            "organization_id": None if self.organization_id is None else {"int": self.organization_id},
            "user_id": self.user_id,
            "token_string": None if self.token_string is None else {"string": self.token_string},
            "token_payload": None if self.token_payload is None else {"TokenPayload": self.token_payload.to_google_pubsub_object()},
            "service": self.service.replace("-", "_"),
            "table": self.table,
            "data_id": self.data_id,
            "data": self.data
        }

        return result