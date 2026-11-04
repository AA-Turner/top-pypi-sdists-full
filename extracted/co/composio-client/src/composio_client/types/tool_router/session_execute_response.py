# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_router.session_execute_response."""

from __future__ import annotations

from typing import Dict, Literal, Optional, TypeAlias, Union

from pydantic import ConfigDict
from ..._base_model import BaseModel


class CurrentSessionExecuteResponseInstantCharge(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    amount: str
    currency: Literal["USD"]
    charged_by: Literal["composio"]


class CurrentSessionExecuteResponseHookResultVariant0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    status: Literal["evaluated"]
    outcome: Literal["continue", "block"]


class CurrentSessionExecuteResponseHookResultVariant1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    status: Literal["unavailable"]


class SessionExecuteResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    data: Dict[str, Optional[object]]
    "The data returned by the tool execution"
    error: Optional[str] = None
    "Error message if the execution failed, null otherwise"
    log_id: str
    "Unique identifier for the execution log"
    instant_charge: CurrentSessionExecuteResponseInstantCharge | None = None
    hook_results: list[CurrentSessionExecuteResponseHookResultVariant0 | CurrentSessionExecuteResponseHookResultVariant1] | None = None
    result_type: Optional[Literal["completed", "failed"]] = None


class CurrentSessionExecuteBlockedResponseReasonVariant0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    type: Literal["request_blocked"]
    hook_id: str


class CurrentSessionExecuteBlockedResponseReasonVariant1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    type: Literal["response_blocked"]
    hook_id: str


class CurrentSessionExecuteBlockedResponseInstantCharge(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    amount: str
    currency: Literal["USD"]
    charged_by: Literal["composio"]


class CurrentSessionExecuteBlockedResponseHookResultVariant0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    status: Literal["evaluated"]
    outcome: Literal["continue", "block"]


class CurrentSessionExecuteBlockedResponseHookResultVariant1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    status: Literal["unavailable"]


class SessionExecuteBlockedResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    result_type: Literal["blocked"]
    reason: CurrentSessionExecuteBlockedResponseReasonVariant0 | CurrentSessionExecuteBlockedResponseReasonVariant1
    message: str
    log_id: str | None = None
    instant_charge: CurrentSessionExecuteBlockedResponseInstantCharge | None = None
    hook_results: list[CurrentSessionExecuteBlockedResponseHookResultVariant0 | CurrentSessionExecuteBlockedResponseHookResultVariant1] | None = None


class CurrentSessionExecuteInputRequiredResponseInputRequestsValue(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    type: Literal["elicitation"]
    mode: Literal["form"]
    message: str
    requested_schema: dict[str, object | None]


class SessionExecuteInputRequiredResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    result_type: Literal["input_required"]
    input_requests: dict[str, CurrentSessionExecuteInputRequiredResponseInputRequestsValue]
    request_state: str | None = None


# Complete return union; the Response class remains constructible for legacy callers.
SessionExecuteResult: TypeAlias = Union[SessionExecuteResponse, SessionExecuteBlockedResponse, SessionExecuteInputRequiredResponse]

__all__ = [
    "SessionExecuteResponse",
    "SessionExecuteBlockedResponse",
    "SessionExecuteInputRequiredResponse",
    "CurrentSessionExecuteResponseInstantCharge",
    "CurrentSessionExecuteResponseHookResultVariant0",
    "CurrentSessionExecuteResponseHookResultVariant1",
    "CurrentSessionExecuteBlockedResponseReasonVariant0",
    "CurrentSessionExecuteBlockedResponseReasonVariant1",
    "CurrentSessionExecuteBlockedResponseInstantCharge",
    "CurrentSessionExecuteBlockedResponseHookResultVariant0",
    "CurrentSessionExecuteBlockedResponseHookResultVariant1",
    "CurrentSessionExecuteInputRequiredResponseInputRequestsValue",
    "SessionExecuteResult",
]
