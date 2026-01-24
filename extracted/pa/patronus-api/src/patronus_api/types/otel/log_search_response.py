# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["LogSearchResponse", "Log"]


class Log(BaseModel):
    body: object

    log_attributes: Optional[Dict[str, str]] = None

    resource_attributes: Optional[Dict[str, str]] = None

    resource_schema_url: Optional[str] = None

    scope_attributes: Optional[Dict[str, str]] = None

    scope_name: Optional[str] = None

    scope_schema_url: Optional[str] = None

    scope_version: Optional[str] = None

    service_name: Optional[str] = None

    severity_number: Optional[int] = None

    severity_text: Optional[str] = None

    span_id: Optional[str] = None

    timestamp: Optional[datetime] = None

    trace_flags: Optional[int] = None

    trace_id: Optional[str] = None


class LogSearchResponse(BaseModel):
    logs: List[Log]
