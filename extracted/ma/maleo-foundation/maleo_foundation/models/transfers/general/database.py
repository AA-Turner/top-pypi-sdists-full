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