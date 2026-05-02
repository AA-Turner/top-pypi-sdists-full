# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["SpanSearchResponse", "Span"]


class Span(BaseModel):
    duration: str

    events: Optional[List[object]] = None

    links: Optional[List[object]] = None

    parent_span_id: Optional[str] = None

    resource_attributes: Optional[Dict[str, str]] = None

    scope_name: Optional[str] = None

    scope_version: Optional[str] = None

    service_name: Optional[str] = None

    span_attributes: Optional[Dict[str, str]] = None

    span_id: str

    span_kind: Optional[str] = None

    span_name: Optional[str] = None

    status_code: Optional[str] = None

    status_message: Optional[str] = None

    timestamp: datetime

    trace_id: str

    trace_state: Optional[str] = None


class SpanSearchResponse(BaseModel):
    spans: List[Span]
