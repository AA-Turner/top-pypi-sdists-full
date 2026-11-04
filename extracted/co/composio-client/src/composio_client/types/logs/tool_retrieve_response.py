# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.logs.tool_retrieve_response."""

from __future__ import annotations

from typing import Dict, Literal, Optional

from pydantic import ConfigDict, Field
from ..._base_model import BaseModel


class App(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    icon: str
    name: str
    unique_id: str = Field(alias="uniqueId")


class Connection(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    entity: str
    id: str


class StepLogRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    headers: Optional[Dict[str, str]] = None
    json_: Optional[Dict[str, Optional[object]]] = Field(default=None, alias="json")
    method: str
    params: Optional[Dict[str, Optional[object]]] = None
    timeout: Optional[float] = None
    url: str


class StepLogResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    status: float
    time: str


class StepLog(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    level: str
    message: str
    request: StepLogRequest
    request_id: str = Field(alias="requestId")
    response: StepLogResponse
    time: float
    type: Literal['network', 'system']


class StepMetadata(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    encryption: Optional[str] = None


class Step(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    end_time: float = Field(alias="endTime")
    logs: Optional[list[StepLog]] = None
    message: str
    metadata: Optional[StepMetadata] = None
    start_time: float = Field(alias="startTime")
    status: Literal['success', 'failure', 'error']
    total_duration: float = Field(alias="totalDuration")
    type: Literal['tool_execution', 'fetch_connection_details']


class ToolRetrieveResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    action_id: str = Field(alias="actionId")
    action_log_id: str = Field(alias="actionLogId")
    app: App
    connection: Connection
    end_time: float = Field(alias="endTime")
    error: Dict[str, Optional[object]]
    execution_metadata: Dict[str, Optional[object]] = Field(alias="executionMetadata")
    payload_received: Dict[str, Optional[object]] = Field(alias="payloadReceived")
    response: Dict[str, Optional[object]]
    session: Dict[str, Optional[object]]
    start_time: float = Field(alias="startTime")
    status: Literal['success', 'error', 'warning', 'info']
    steps: list[Step]
    total_duration: str = Field(alias="totalDuration")
    version: str
    credential_source: Literal["connected_account", "instant_account", "custom_auth", "no_auth"] | None = Field(default=None, alias="credentialSource")
    instant_charge: str | None = Field(default=None, alias="instantCharge")


__all__ = [
    "ToolRetrieveResponse",
    "App",
    "Connection",
    "Step",
    "StepLog",
    "StepLogRequest",
    "StepLogResponse",
    "StepMetadata",
]
