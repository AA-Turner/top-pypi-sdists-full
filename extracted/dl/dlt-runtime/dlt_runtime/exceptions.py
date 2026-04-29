from contextlib import contextmanager
import json
from typing import TYPE_CHECKING, Optional, Union

import httpx
from dlt._workspace.exceptions import WorkspaceException
from dlt.common.exceptions import DltException
from dlt_runtime.runtime_clients.api.errors import (
    UnexpectedStatus as ApiUnexpectedStatus,
)
from dlt_runtime.runtime_clients.auth.errors import (
    UnexpectedStatus as AuthUnexpectedStatus,
)
from dlt_runtime.runtime_clients.api.types import Response as ApiResponse
from dlt_runtime.runtime_clients.auth.types import Response as AuthResponse

if TYPE_CHECKING:
    # Avoid runtime import cycle: runtime.py imports from this module.
    from dlt._workspace.deployment.typing import TJobDefinition
    from dlt_runtime.runtime import WorkspaceInfo


UnexpectedStatus = Union[ApiUnexpectedStatus, AuthUnexpectedStatus]
Response = Union[ApiResponse, AuthResponse]


class RuntimeClientException(DltException):
    """Base for runtime CLI domain errors."""


class RuntimeNotAuthenticated(RuntimeClientException):
    """No valid token locally OR API rejected with 401."""


class RuntimeOperationNotAuthorized(WorkspaceException, RuntimeClientException):
    """Authenticated but not authorized for this operation."""


class NoRunsFound(RuntimeClientException):
    """No runs exist for the requested job or workspace."""


class NoRunnableRun(RuntimeClientException):
    """Run is already in a terminal state and cannot be cancelled."""


class WorkspaceNotFound(RuntimeClientException):
    """Workspace name/UUID does not match any owned workspace."""

    def __init__(self, workspace: str, is_uuid: bool):
        super().__init__(
            f"Workspace '{workspace}' not found among your owned workspaces."
        )
        self.workspace = workspace
        self.is_uuid = is_uuid


class AmbiguousWorkspaceName(ValueError, RuntimeClientException):
    """Multiple owned workspaces share the requested name."""

    def __init__(self, name: str, workspaces: list["WorkspaceInfo"]):
        ids = ", ".join(ws.id for ws in workspaces)
        super().__init__(
            f"Multiple owned workspaces are named '{name}' ({ids}). "
            "Pass the workspace ID instead to avoid ambiguity."
        )
        self.name = name
        self.workspaces = workspaces


class AmbiguousJobSelector(ValueError, RuntimeClientException):
    """Selector matched more than one job; user must narrow it."""

    def __init__(self, matches: list[tuple["TJobDefinition", str]]):
        job_list = "\n".join(f"  - {jd['job_ref']} (trigger: {t})" for jd, t in matches)
        super().__init__(
            f"Multiple jobs matched. Use a more specific selector or job ref:\n{job_list}"
        )
        self.matches = matches


@contextmanager
def handle_client_exceptions(message: Optional[str] = None):
    """Translate HTTP/network errors from generated clients to typed exceptions."""
    message = message or "Error calling the Runtime API"
    try:
        yield
    except (ApiUnexpectedStatus, AuthUnexpectedStatus) as e:
        # Generated clients use raise_on_unexpected_status=True, so undocumented
        # statuses bubble up as UnexpectedStatus and we convert here.
        raise exception_from_response(message, e) from e
    except httpx.TimeoutException as e:
        raise TimeoutError(
            f"{message}. The request timed out. "
            "Please check your connection and try again."
        ) from e
    except httpx.NetworkError as e:
        raise ConnectionError(
            f"{message}. A network error occurred. "
            "Please check your connection and try again."
        ) from e
    except json.JSONDecodeError as e:
        # Malformed server response — programmer-side, not a user error.
        raise RuntimeError(
            "Error parsing the JSON response from the Runtime API. "
            "It's likely due to server issues, please contact support"
        ) from e
    except Exception as e:
        # Anything else is unexpected (protocol-level, etc.); surface as RuntimeError
        # so it doesn't get formatted as a normal user-facing CLI error.
        raise RuntimeError(f"{message}. Underlying error: {e}") from e


def exception_from_response(
    message: str, response: Union[Response, UnexpectedStatus]
) -> BaseException:
    """Build a typed exception from an API response or UnexpectedStatus."""
    status = response.status_code
    try:
        details = json.loads(response.content.decode("utf-8"))["detail"]
    except Exception:
        details = response.content.decode("utf-8")

    # 401 gets a dedicated type so commands.py:execute() can route it to
    # the Phase 1 device-flow recovery (issue #645).
    if status == 401:
        return RuntimeNotAuthenticated(f"{message}. {details} (HTTP {status})")
    if status < 500:
        return RuntimeClientException(
            f"{message}. {details.capitalize()} (HTTP {status})"
        )
    return RuntimeClientException(f"{message}. Server error: {details} (HTTP {status})")
