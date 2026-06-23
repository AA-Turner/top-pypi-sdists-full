import json
from enum import StrEnum
from http import HTTPStatus
from typing import Any

import httpx
from mistralai.client.errors import MistralError
from temporalio.client import WorkflowQueryRejectedError
from temporalio.exceptions import (
    ActivityError as TemporalActivityError,
)
from temporalio.exceptions import (
    ApplicationError as TemporalApplicationError,
)
from temporalio.exceptions import (
    TemporalError,
    WorkflowAlreadyStartedError,
)
from temporalio.service import RPCError, RPCStatusCode

from mistralai.workflows.worker_client.errors import SDKError

_TERMINAL_CODES: dict[str, str] = {
    # WF_1104 = WorkflowsErrorCode.WORKFLOW_REGISTRATION_FAILED (abraxas)
    "WF_1104": "Workflow registration failed: credential is not authorized for this deployment",
}

_TRANSIENT_STATUSES: frozenset[HTTPStatus] = frozenset(
    {
        HTTPStatus.BAD_GATEWAY,
        HTTPStatus.GATEWAY_TIMEOUT,
        HTTPStatus.SERVICE_UNAVAILABLE,
    }
)


class ErrorCode(StrEnum):
    EXECUTION_ERROR = "execution_error"
    TEMPORAL_ERROR = "temporal_error"
    TEMPORAL_SERVICE_ERROR = "temporal_service_error"
    TEMPORAL_CONNECTION_ERROR = "temporal_connection_error"

    ACTIVITY_DEFINITION_ERROR = "activity_definition_error"
    ACTIVITY_NOT_FOUND_ERROR = "activity_not_found_error"
    INVALID_ARGUMENTS_ERROR = "invalid_arguments_error"
    ACTIVITY_NOT_MODULE_LEVEL = "activity_not_module_level"
    ACTIVITY_RESERVED_NAME = "activity_reserved_name"
    TOOL_ARGUMENT_ERROR = "tool_argument_error"
    RATE_LIMIT_ERROR = "rate_limit_error"
    STICKY_WORKER_SESSION_MISSING = "sticky_worker_session_missing"

    WORKFLOW_DEFINITION_ERROR = "workflow_definition_error"
    WORKFLOW_DESCRIPTION_ERROR = "workflow_description_error"
    WORKFLOW_ALREADY_STARTED = "workflow_already_started"
    WORKFLOW_NOT_FOUND = "workflow_not_found"
    INVALID_PARAMS_ERROR = "invalid_params_error"
    WORKFLOW_TIMEOUT_ERROR = "workflow_timeout_error"
    WORKFLOW_SIGNAL_DEFINITION_ERROR = "workflow_signal_definition_error"
    WORKFLOW_UPDATE_DEFINITION_ERROR = "workflow_update_definition_error"
    WORKFLOW_QUERY_ERROR = "workflow_query_error"

    WORKER_REGISTRATION_ERROR = "worker_registration_error"
    WORKER_RUNTIME_CONFIG_ERROR = "worker_runtime_config_error"

    AGENT_EXECUTION_ERROR = "agent_execution_error"

    IN_MEMORY_CACHE_ERROR = "in_memory_cache_error"
    REJECTED_QUERY_ERROR = "rejected_query_error"
    UNSERIALIZABLE_PAYLOAD_ERROR = "unserializable_payload_error"
    BLOB_STORAGE_CONFIG_ERROR = "blob_storage_config_error"
    INPUT_SIZE_EXCEEDED_ERROR = "input_size_exceeded_error"

    # API endpoint errors following {HTTP_METHOD}_{ENDPOINT}_ERROR convention
    GET_WORKFLOWS_ERROR = "get_workflows_error"
    GET_WORKFLOWS_VERSIONS_ERROR = "get_workflows_versions_error"
    GET_WORKERS_WHOAMI_ERROR = "get_workers_whoami_error"
    POST_WORKFLOWS_REGISTER_ERROR = "post_workflows_register_error"
    POST_WORKFLOWS_EXECUTE_ERROR = "post_workflows_execute_error"
    POST_EXECUTIONS_TERMINATE_ERROR = "post_executions_terminate_error"
    GET_EXECUTIONS_ERROR = "get_executions_error"
    GET_EXECUTIONS_TRACE_OTEL_ERROR = "get_executions_trace_otel_error"
    GET_EXECUTIONS_TRACE_SUMMARY_ERROR = "get_executions_trace_summary_error"
    GET_EXECUTIONS_TRACE_EVENTS_ERROR = "get_executions_trace_events_error"
    POST_EXECUTIONS_SIGNALS_ERROR = "post_executions_signals_error"
    POST_EXECUTIONS_QUERIES_ERROR = "post_executions_queries_error"
    POST_EXECUTIONS_UPDATES_ERROR = "post_executions_updates_error"
    POST_SCHEDULES_ERROR = "post_schedules_error"
    GET_EVENTS_STREAM_ERROR = "get_events_stream_error"
    POST_EVENTS_ERROR = "post_events_error"
    POST_EVENT_ROUTE_TOKEN_ERROR = "post_event_route_token_error"
    POST_WORKERS_HEARTBEAT_ERROR = "post_workers_heartbeat_error"
    POST_EXECUTION_IDENTITY_ERROR = "post_execution_identity_error"


class WorkflowsException(Exception):
    def __init__(
        self,
        message: str,
        status: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
        code: ErrorCode = ErrorCode.TEMPORAL_SERVICE_ERROR,
        type: str = "invalid_request_error",
        logging_message: str | None = None,
        logging_properties: dict[str, Any] | None = None,
    ) -> None:
        self.status = status
        self.message = message
        self.code = code
        self.type = type
        self.logging_message = logging_message
        self.logging_properties = logging_properties or {}

    def is_terminal(self) -> bool:
        """True if this error is non-recoverable and should terminate the worker."""
        if self.status == HTTPStatus.UNAUTHORIZED:
            return True
        return str(self.code) in _TERMINAL_CODES

    def is_transient(self) -> bool:
        """True if this error is likely transient and safe to retry."""
        return self.status in _TRANSIENT_STATUSES

    def terminal_label(self) -> str | None:
        """Human-readable log label for a terminal error, or None if not in the catalog."""
        return _TERMINAL_CODES.get(str(self.code))

    def asdict(self) -> dict[str, str]:
        return {"object": "Error", "message": self.message, "type": self.type, "code": str(self.code)}

    def __str__(self) -> str:
        return (
            f"{self.type}: {self.message} \n"
            f"Workflow Code: {self.code} -- "
            f"HTTP status: {self.status.value if self.status else None})"
        )

    @classmethod
    def from_rpc_error(
        cls,
        rpc_error: RPCError,
        message_override: str | None = None,
        status_override: HTTPStatus | None = None,
    ) -> "WorkflowsException":
        message = message_override if message_override is not None else rpc_error.message or "An error occurred"
        match rpc_error.status:
            case RPCStatusCode.NOT_FOUND:
                code = ErrorCode.WORKFLOW_NOT_FOUND
            case _:
                code = ErrorCode.TEMPORAL_SERVICE_ERROR

        return cls(
            message,
            status_override or HTTPStatus.INTERNAL_SERVER_ERROR,
            code,
        )

    @classmethod
    def from_temporal_error(
        cls,
        temporal_error: TemporalError,
        message_override: str | None = None,
        status_override: HTTPStatus | None = None,
        code: ErrorCode | None = None,
    ) -> "WorkflowsException":
        match temporal_error:
            case RPCError():
                return cls.from_rpc_error(temporal_error, message_override, status_override)
            case WorkflowQueryRejectedError():
                return cls(
                    message_override or "An error occurred",
                    status_override or HTTPStatus.INTERNAL_SERVER_ERROR,
                    ErrorCode.REJECTED_QUERY_ERROR,
                )
            case WorkflowAlreadyStartedError():
                return cls(
                    message_override or temporal_error.message,
                    status_override or HTTPStatus.CONFLICT,
                    ErrorCode.WORKFLOW_ALREADY_STARTED,
                )
            case _:
                return cls(
                    message_override or "An error occurred",
                    status_override or HTTPStatus.INTERNAL_SERVER_ERROR,
                    code or ErrorCode.TEMPORAL_SERVICE_ERROR,
                )

    @classmethod
    def from_sdk_error(
        cls,
        exc: SDKError,
        message: str = "HTTP request failed",
        code: ErrorCode = ErrorCode.TEMPORAL_CONNECTION_ERROR,
        logging_message: str | None = None,
        logging_properties: dict[str, Any] | None = None,
    ) -> "WorkflowsException":
        try:
            http_status = HTTPStatus(exc.status_code)
        except ValueError:
            http_status = HTTPStatus.INTERNAL_SERVER_ERROR
        try:
            body = json.loads(exc.body)
        except (json.JSONDecodeError, ValueError):
            body = {}
        if not isinstance(body, dict):
            # to handle valid JSON that is not a dict
            body = {}
        return cls(
            message=body.get("message", message),
            code=body.get("code", code),
            status=http_status,
            type=body.get("type", "api_error"),
            logging_message=logging_message,
            logging_properties=logging_properties,
        )

    @classmethod
    def from_api_client_error(
        cls,
        exc: Exception,
        message: str = "HTTP request failed",
        code: ErrorCode = ErrorCode.TEMPORAL_CONNECTION_ERROR,
        status: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
        type: str = "httpx_error",
        logging_message: str | None = None,
        logging_properties: dict[str, Any] | None = None,
    ) -> "WorkflowsException":
        if isinstance(exc, cls):
            return exc
        if isinstance(exc, SDKError):
            return cls.from_sdk_error(
                exc,
                message=message,
                code=code,
                logging_message=logging_message,
                logging_properties=logging_properties,
            )
        if isinstance(exc, MistralError):
            try:
                http_status = HTTPStatus(exc.status_code)
            except ValueError:
                http_status = HTTPStatus.INTERNAL_SERVER_ERROR
            try:
                body = json.loads(exc.body)
            except (json.JSONDecodeError, ValueError):
                body = {}
            if not isinstance(body, dict):
                body = {}
            return cls(
                message=body.get("message", message),
                code=body.get("code", code),
                status=http_status,
                type=body.get("type", "api_error"),
                logging_message=logging_message,
                logging_properties=logging_properties,
            )
        if isinstance(exc, httpx.HTTPStatusError):
            try:
                status = HTTPStatus(exc.response.status_code)
            except ValueError:
                pass
        if isinstance(exc, httpx.ConnectError | httpx.TimeoutException):
            status = HTTPStatus.BAD_GATEWAY
        return cls(
            message=f"{message}: {exc}",
            code=code,
            status=status,
            type=type,
            logging_message=logging_message,
            logging_properties=logging_properties,
        )


class WorkflowError(TemporalApplicationError):
    """Base exception for all Mistral Workflows errors."""

    pass


class NotInTemporalContextError(WorkflowError):
    """Raised when code is executed outside of a Temporal workflow or activity context."""

    def __init__(self) -> None:
        super().__init__("Not in a Temporal context. This function must be called from within a workflow or activity.")


ActivityError = TemporalActivityError
