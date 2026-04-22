from contextlib import contextmanager
import json
from typing import Optional, Union

import httpx
from dlt._workspace.exceptions import WorkspaceException
from dlt._workspace.cli.exceptions import CliCommandInnerException
from dlt.common.runtime.exceptions import RuntimeException
from dlt_runtime.runtime_clients.api.errors import (
    UnexpectedStatus as ApiUnexpectedStatus,
)
from dlt_runtime.runtime_clients.auth.errors import (
    UnexpectedStatus as AuthUnexpectedStatus,
)
from dlt_runtime.runtime_clients.api.types import Response as ApiResponse
from dlt_runtime.runtime_clients.auth.types import Response as AuthResponse


UnexpectedStatus = Union[ApiUnexpectedStatus, AuthUnexpectedStatus]
Response = Union[ApiResponse, AuthResponse]


class RuntimeNotAuthenticated(RuntimeException):
    pass


class RuntimeOperationNotAuthorized(WorkspaceException, RuntimeException):
    pass


class NoRunsFound(CliCommandInnerException):
    """Raised when no runs exist for a job or workspace."""

    def __init__(self, msg: str):
        super().__init__(cmd="runtime", msg=msg)


class NoRunnableRun(CliCommandInnerException):
    """Raised when a run is already in a terminal state and cannot be cancelled."""

    def __init__(self, msg: str):
        super().__init__(cmd="runtime", msg=msg)


class WorkspaceNotFound(RuntimeException):
    """Raised when `_resolve_workspace` cannot match the input to an owned workspace."""

    def __init__(self, workspace: str, is_uuid: bool):
        super().__init__(
            f"Workspace '{workspace}' not found among your owned workspaces."
        )
        self.workspace = workspace
        self.is_uuid = is_uuid


@contextmanager
def handle_client_exceptions(message: Optional[str] = None):
    message = message or "Error calling the Runtime API"
    try:
        yield
    except (ApiUnexpectedStatus, AuthUnexpectedStatus) as e:
        # As clients are initialized with raise_on_unexpected_status=True, HTTP exceptions
        # that are not documented in the source OpenAPI document are raised as
        # UnexpectedStatus and handled here
        raise exception_from_response(message, e) from e
    except httpx.TimeoutException as e:
        raise CliCommandInnerException(
            cmd="runtime",
            msg=(
                f"{message}. The request timed out. "
                "Please check your connection and try again."
            ),
        ) from e
    except httpx.NetworkError as e:
        raise CliCommandInnerException(
            cmd="runtime",
            msg=(
                f"{message}. A network error occurred. "
                "Please check your connection and try again."
            ),
        ) from e
    except json.JSONDecodeError as e:
        message = (
            "Error parsing the JSON response from the Runtime API. "
            "It's likely due to server issues, please contact support"
        )
        raise RuntimeError(message) from e
    except Exception as e:
        # Other unforeseen exceptions, e.g. on protocol level
        message += f". Underlying error: {e}"
        raise RuntimeError(message) from e


def exception_from_response(
    message: str, response: Union[Response, UnexpectedStatus]
) -> BaseException:
    status = response.status_code
    try:
        details = json.loads(response.content.decode("utf-8"))["detail"]
    except Exception:
        details = response.content.decode("utf-8")

    if status == 401:
        message += f". {details} (HTTP {status}). Please run 'dlt runtime login' to re-authenticate"
    elif status < 500:
        message += f". {details.capitalize()} (HTTP {status})"
    else:
        message += f". Server error: {details} (HTTP {status})"
    return CliCommandInnerException(cmd="runtime", msg=message)
