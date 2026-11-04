# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_router.session_execute_meta_response."""

from __future__ import annotations

from typing import Dict, Literal, Optional, TypeAlias, Union

from pydantic import ConfigDict
from ..._base_model import BaseModel


class CurrentSessionExecuteMetaResponseInstantCharge(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    amount: str
    currency: Literal["USD"]
    charged_by: Literal["composio"]


class CurrentSessionExecuteMetaResponseHookResultVariant0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    status: Literal["evaluated"]
    outcome: Literal["continue", "block"]


class CurrentSessionExecuteMetaResponseHookResultVariant1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    status: Literal["unavailable"]


class SessionExecuteMetaResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    data: Dict[str, Optional[object]]
    "The data returned by the tool execution"
    error: Optional[str] = None
    "Error message if the execution failed, null otherwise"
    log_id: str
    "Unique identifier for the execution log"
    instant_charge: CurrentSessionExecuteMetaResponseInstantCharge | None = None
    hook_results: list[CurrentSessionExecuteMetaResponseHookResultVariant0 | CurrentSessionExecuteMetaResponseHookResultVariant1] | None = None
    result_type: Optional[Literal["completed", "failed"]] = None


class CurrentSessionExecuteMetaBlockedResponseReasonVariant0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    type: Literal["request_blocked"]
    hook_id: str


class CurrentSessionExecuteMetaBlockedResponseReasonVariant1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    type: Literal["response_blocked"]
    hook_id: str


class CurrentSessionExecuteMetaBlockedResponseInstantCharge(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    amount: str
    currency: Literal["USD"]
    charged_by: Literal["composio"]


class CurrentSessionExecuteMetaBlockedResponseHookResultVariant0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    status: Literal["evaluated"]
    outcome: Literal["continue", "block"]


class CurrentSessionExecuteMetaBlockedResponseHookResultVariant1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    status: Literal["unavailable"]


class SessionExecuteMetaBlockedResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    result_type: Literal["blocked"]
    reason: CurrentSessionExecuteMetaBlockedResponseReasonVariant0 | CurrentSessionExecuteMetaBlockedResponseReasonVariant1
    message: str
    log_id: str | None = None
    instant_charge: CurrentSessionExecuteMetaBlockedResponseInstantCharge | None = None
    hook_results: list[CurrentSessionExecuteMetaBlockedResponseHookResultVariant0 | CurrentSessionExecuteMetaBlockedResponseHookResultVariant1] | None = None


class CurrentSessionExecuteMetaInputRequiredResponseInputRequestsValue(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    type: Literal["elicitation"]
    mode: Literal["form"]
    message: str
    requested_schema: dict[str, object | None]


class SessionExecuteMetaInputRequiredResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    result_type: Literal["input_required"]
    input_requests: dict[str, CurrentSessionExecuteMetaInputRequiredResponseInputRequestsValue]
    request_state: str | None = None


# Complete return union; the Response class remains constructible for legacy callers.
SessionExecuteMetaResult: TypeAlias = Union[SessionExecuteMetaResponse, SessionExecuteMetaBlockedResponse, SessionExecuteMetaInputRequiredResponse]

__all__ = [
    "SessionExecuteMetaResponse",
    "SessionExecuteMetaBlockedResponse",
    "SessionExecuteMetaInputRequiredResponse",
    "CurrentSessionExecuteMetaResponseInstantCharge",
    "CurrentSessionExecuteMetaResponseHookResultVariant0",
    "CurrentSessionExecuteMetaResponseHookResultVariant1",
    "CurrentSessionExecuteMetaBlockedResponseReasonVariant0",
    "CurrentSessionExecuteMetaBlockedResponseReasonVariant1",
    "CurrentSessionExecuteMetaBlockedResponseInstantCharge",
    "CurrentSessionExecuteMetaBlockedResponseHookResultVariant0",
    "CurrentSessionExecuteMetaBlockedResponseHookResultVariant1",
    "CurrentSessionExecuteMetaInputRequiredResponseInputRequestsValue",
    "SessionExecuteMetaResult",
]
