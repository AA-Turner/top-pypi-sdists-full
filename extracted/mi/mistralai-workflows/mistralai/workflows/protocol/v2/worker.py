import uuid
from typing import Annotated, Literal

from pydantic import BaseModel, Field, PlainSerializer

# Keep this protocol contract in sync with
# albe/albe/services/event_route_token_models.py.
EVENT_ROUTE_TOKEN_HEADER = "X-Workflow-Route-Token"
JWT_AUDIENCE = "abraxas-events-v2"
EVENT_ROUTE_TOKEN_SCOPE_UNSUPPORTED_CODE = "V2_SCOPE_UNSUPPORTED"
EVENT_ROUTE_TOKEN_EXPIRED_CODE = "EVENT_ROUTE_TOKEN_EXPIRED"
EVENT_ROUTE_TOKEN_INVALID_CODE = "EVENT_ROUTE_TOKEN_INVALID"
EVENT_ROUTE_EXECUTION_TOKEN_NOT_FOUND_CODE = "EVENT_ROUTE_EXECUTION_TOKEN_NOT_FOUND"
EVENT_ROUTE_SCOPE_NOT_FOUND_CODE = "EVENT_ROUTE_SCOPE_NOT_FOUND"
EVENT_ROUTE_EXECUTION_NOT_MATERIALIZED_CODE = "EVENT_ROUTE_EXECUTION_NOT_MATERIALIZED"
EVENT_ROUTE_TOKEN_BINDING_INVALID_CODE = "EVENT_ROUTE_TOKEN_BINDING_INVALID"
EVENT_ROUTE_EXECUTION_GONE_CODE = "EVENT_ROUTE_EXECUTION_GONE"


JSONSerializableUUID = Annotated[
    uuid.UUID,
    PlainSerializer(lambda value: str(value), return_type=str, when_used="always"),
]


class EventRouteTokenRequest(BaseModel):
    # execution_token is legacy: new workers identify the run by (workflow_exec_id, workflow_run_id).
    # The mint endpoint accepts either; the token path is kept for backward compatibility only and
    # should be removed as soon as every supported worker mints by run identity.
    execution_token: uuid.UUID | None = None
    workflow_exec_id: str = Field(description="Execution ID of the workflow run the worker wants to publish for.")
    workflow_run_id: str = Field(description="Run ID of the workflow run the worker wants to publish for.")


class EventRouteTokenResponse(BaseModel):
    route_token: str
    expires_in_seconds: int


class EventRouteClaims(BaseModel):
    scope_kind: Literal["root"]
    workflow_owner_customer_id: JSONSerializableUUID
    workflow_owner_workspace_id: JSONSerializableUUID
    execution_owner_customer_id: JSONSerializableUUID
    execution_owner_workspace_id: JSONSerializableUUID
    workflow_id: JSONSerializableUUID
    workflow_name: str = Field(min_length=1)
    workflow_exec_id: str = Field(min_length=1)
    workflow_run_id: str = Field(min_length=1)
    root_workflow_exec_id: str = Field(min_length=1)
    parent_workflow_exec_id: str | None = Field(default=None, min_length=1)
    # Optional during migration; lets the events handler skip the run lookup.
    execution_id: JSONSerializableUUID | None = None
