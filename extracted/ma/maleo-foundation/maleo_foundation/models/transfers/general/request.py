from __future__ import annotations
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_serializer
from starlette.datastructures import QueryParams
from typing import Dict, Any
from uuid import UUID
from maleo_foundation.types import BaseTypes

class RequestContext(BaseModel):
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

    class Config:
        arbitrary_types_allowed = True

    @field_serializer('query_params', when_used='json')
    def serialize_query_params(self, qp: QueryParams, _info) -> str:
        return str(qp)

    def to_google_pubsub_object(self) -> Dict[str, Any]:
        result = {
            "request_id": str(self.request_id),
            "requested_at": self.requested_at.isoformat(),
            "method": self.method,
            "url": self.url,
            "path_params": None if self.path_params is None else {"map": self.path_params},
            "query_params": None if self.query_params is None else {"string": self.query_params},
            "ip_address": self.ip_address,
            "is_internal": None if self.is_internal is None else {"boolean": self.is_internal},
            "user_agent": None if self.user_agent is None else {"string": self.user_agent},
            "ua_browser": None if self.ua_browser is None else {"string": self.ua_browser},
            "ua_mobile": None if self.ua_mobile is None else {"string": self.ua_mobile},
            "platform": None if self.platform is None else {"string": self.platform},
            "referer": None if self.referer is None else {"array": self.referer},
            "origin": None if self.origin is None else {"array": self.origin},
            "host": None if self.host is None else {"array": self.host},
            "forwarded_proto": None if self.forwarded_proto is None else {"array": self.forwarded_proto},
            "language": None if self.language is None else {"array": self.language}
        }

        return result

    @classmethod
    def from_google_pubsub_object(cls, obj:Dict[str, Any]):
        return cls(
            request_id = UUID(obj["request_id"]),
            requested_at = datetime.fromisoformat(obj["requested_at"]),
            method = obj["method"],
            url = obj["url"],
            path_params = None if obj["path_params`"] is None else obj["path_params"]["map"],
            query_params = None if obj["query_params"] is None else obj["query_params"]["string"],
            ip_address = obj["ip_address"],
            is_internal = None if obj["is_internal"] is None else bool(obj["is_internal"]["boolean"]),
            user_agent = None if obj["user_agent"] is None else obj["user_agent"]["string"],
            ua_browser = None if obj["ua_browser"] is None else obj["ua_browser"]["string"],
            ua_mobile = None if obj["ua_mobile"] is None else obj["ua_mobile"]["string"],
            platform = None if obj["platform"] is None else obj["platform"]["string"],
            referer = None if obj["referer"] is None else obj["referer"]["string"],
            origin = None if obj["origin"] is None else obj["origin"]["string"],
            host = None if obj["host"] is None else obj["host"]["string"],
            forwarded_proto = None if obj["forwarded_proto"] is None else obj["forwarded_proto"]["string"],
            language = None if obj["language"] is None else obj["language"]["string"],
        )