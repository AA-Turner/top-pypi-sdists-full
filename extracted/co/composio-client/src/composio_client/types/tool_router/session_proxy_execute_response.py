# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_router.session_proxy_execute_response."""

from __future__ import annotations

from typing import Dict, Literal, Optional, TypeAlias, Union

from pydantic import ConfigDict
from ..._base_model import BaseModel


class BinaryData(BaseModel):
    "Binary body response data. Present when the response is a binary file."

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    content_type: str
    "Content-Type of the binary data"
    expires_at: Optional[str] = None
    "ISO 8601 timestamp when the URL expires"
    size: float
    "File size in bytes"
    url: str
    "URL to download binary content"


class CurrentSessionProxyExecuteResponseHookResultVariant0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    status: Literal["evaluated"]
    outcome: Literal["continue", "block"]


class CurrentSessionProxyExecuteResponseHookResultVariant1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    status: Literal["unavailable"]


class SessionProxyExecuteResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    binary_data: Optional[BinaryData] = None
    "Binary body response data. Present when the response is a binary file."
    data: Optional[object] = None
    "The response data returned from the proxied API"
    headers: Optional[Dict[str, str]] = None
    "The HTTP headers returned from the proxied API"
    status: float
    "The HTTP status code returned from the proxied API"
    hook_results: list[CurrentSessionProxyExecuteResponseHookResultVariant0 | CurrentSessionProxyExecuteResponseHookResultVariant1] | None = None
    result_type: Optional[Literal["completed"]] = None


class CurrentSessionProxyExecuteBlockedResponseReasonVariant0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    type: Literal["request_blocked"]
    hook_id: str


class CurrentSessionProxyExecuteBlockedResponseReasonVariant1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    type: Literal["response_blocked"]
    hook_id: str


class CurrentSessionProxyExecuteBlockedResponseHookResultVariant0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    status: Literal["evaluated"]
    outcome: Literal["continue", "block"]


class CurrentSessionProxyExecuteBlockedResponseHookResultVariant1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    status: Literal["unavailable"]


class SessionProxyExecuteBlockedResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    result_type: Literal["blocked"]
    reason: CurrentSessionProxyExecuteBlockedResponseReasonVariant0 | CurrentSessionProxyExecuteBlockedResponseReasonVariant1
    message: str
    hook_results: list[CurrentSessionProxyExecuteBlockedResponseHookResultVariant0 | CurrentSessionProxyExecuteBlockedResponseHookResultVariant1] | None = None


class CurrentSessionProxyExecuteInputRequiredResponseInputRequestsValue(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    type: Literal["elicitation"]
    mode: Literal["form"]
    message: str
    requested_schema: dict[str, object | None]


class SessionProxyExecuteInputRequiredResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    result_type: Literal["input_required"]
    input_requests: dict[str, CurrentSessionProxyExecuteInputRequiredResponseInputRequestsValue]
    request_state: str | None = None


# Complete return union; the Response class remains constructible for legacy callers.
SessionProxyExecuteResult: TypeAlias = Union[SessionProxyExecuteResponse, SessionProxyExecuteBlockedResponse, SessionProxyExecuteInputRequiredResponse]

__all__ = [
    "SessionProxyExecuteResponse",
    "BinaryData",
    "SessionProxyExecuteBlockedResponse",
    "SessionProxyExecuteInputRequiredResponse",
    "CurrentSessionProxyExecuteResponseHookResultVariant0",
    "CurrentSessionProxyExecuteResponseHookResultVariant1",
    "CurrentSessionProxyExecuteBlockedResponseReasonVariant0",
    "CurrentSessionProxyExecuteBlockedResponseReasonVariant1",
    "CurrentSessionProxyExecuteBlockedResponseHookResultVariant0",
    "CurrentSessionProxyExecuteBlockedResponseHookResultVariant1",
    "CurrentSessionProxyExecuteInputRequiredResponseInputRequestsValue",
    "SessionProxyExecuteResult",
]
