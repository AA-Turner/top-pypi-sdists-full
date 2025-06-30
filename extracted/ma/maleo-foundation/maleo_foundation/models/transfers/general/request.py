from __future__ import annotations
from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from maleo_foundation.types import BaseTypes

class RequestContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    request_id: UUID = Field(..., description="Unique identifier for tracing the request")
    requested_at: datetime = Field(datetime.now(tz=timezone.utc), description="Request timestamp")
    method: str = Field(..., description="Request's method")
    url: str = Field(..., description="Request's URL")
    path_params: BaseTypes.OptionalStringToAnyDict = Field(None, description="Request's path parameters")
    query_params: BaseTypes.OptionalString = Field(None, description="Request's query parameters")
    ip_address: str = Field("unknown", description="Client's IP address")
    is_internal: BaseTypes.OptionalBoolean = Field(None, description="True if IP is internal")
    user_agent: BaseTypes.OptionalString = Field(None, description="User-Agent string")
    ua_browser: BaseTypes.OptionalString = Field(None, description="Browser info from sec-ch-ua")
    ua_mobile: BaseTypes.OptionalString = Field(None, description="Is mobile device?")
    platform: BaseTypes.OptionalString = Field(None, description="Client platform or OS")
    referer: BaseTypes.OptionalString = Field(None, description="Referrer URL")
    origin: BaseTypes.OptionalString = Field(None, description="Origin of the request")
    host: BaseTypes.OptionalString = Field(None, description="Host header from request")
    forwarded_proto: BaseTypes.OptionalString = Field(None, description="Forwarded protocol (http/https)")
    language: BaseTypes.OptionalString = Field(None, description="Accepted languages from client")