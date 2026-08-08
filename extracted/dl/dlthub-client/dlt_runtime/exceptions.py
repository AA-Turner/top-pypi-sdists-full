# Python internals
import json
from contextlib import contextmanager
from typing import TYPE_CHECKING, Optional, Union

# Other libraries
import httpx
from dlt._workspace.exceptions import WorkspaceException
from dlt.common.exceptions import DltException

# Current package
from dlt_runtime.runtime_clients.api.errors import (
    UnexpectedStatus as ApiUnexpectedStatus,
)
from dlt_runtime.runtime_clients.api.types import Response as ApiResponse
from dlt_runtime.runtime_clients.auth.errors import (
    UnexpectedStatus as AuthUnexpectedStatus,
)
from dlt_runtime.runtime_clients.auth.types import Response as AuthResponse
from dlt_runtime.runtime_clients.dataplane_api.errors import (
    UnexpectedStatus as DataplaneApiUnexpectedStatus,
)
from dlt_runtime.runtime_clients.dataplane_api.types import (
    Response as DataplaneApiResponse,
)
from dlt_runtime.runtime_clients.logs.errors import (
    UnexpectedStatus as LogUnexpectedStatus,
)
from dlt_runtime.runtime_clients.logs.types import Response as LogResponse

if TYPE_CHECKING:
    # Avoid runtime import cycle: runtime.py imports from this module.
    # Current package
    from dlt_runtime.typing import WorkspaceInfo


UnexpectedStatus = Union[
    ApiUnexpectedStatus,
    AuthUnexpectedStatus,
    LogUnexpectedStatus,
    DataplaneApiUnexpectedStatus,
]
Response = Union[ApiResponse, AuthResponse, LogResponse, DataplaneApiResponse]


class RuntimeClientException(DltException):
    """Base for runtime CLI domain errors."""


class RuntimeNotAuthenticated(RuntimeClientException):
    """No valid token locally OR API rejected with 401."""


class ApiKeyInvalid(RuntimeClientException):
    """The provided API key is not valid.

    Not a subclass of RuntimeNotAuthenticated: a bad api-key isn't a
    session/login problem, so JWT-recovery code paths (`@requires_login`
    in helpers, `RuntimeNotAuthenticated` handlers in commands.py)
    shouldn't catch it.
    """

    def __init__(self, detail: Optional[str] = None) -> None:
        base = (
            "Your API key is not valid. Generate a new one, "
            "or remove the configured API key to authenticate via login."
        )
        super().__init__(f"{base} ({detail})" if detail else base)


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


class OrgRegionRequired(RuntimeClientException):
    """Organization has no region set; one must be chosen before creating a workspace.

    Only reachable by the org owner: the region gate on invites/member-adds means
    a region-less org has no members other than its owner.
    """

    def __init__(self) -> None:
        super().__init__("Organization region must be set before creating workspaces.")


class AmbiguousWorkspaceName(ValueError, RuntimeClientException):
    """Multiple owned workspaces share the requested name."""

    def __init__(self, name: str, workspaces: list["WorkspaceInfo"]):
        ids = ", ".join(ws["id"] for ws in workspaces)
        super().__init__(
            f"Multiple owned workspaces are named '{name}' ({ids}). "
            "Pass the workspace ID instead to avoid ambiguity."
        )
        self.name = name
        self.workspaces = workspaces


@contextmanager
def handle_client_exceptions(message: Optional[str] = None):
    """Translate HTTP/network errors from generated clients to typed exceptions."""
    message = message or "Error calling the dltHub API"
    try:
        yield
    except (
        ApiUnexpectedStatus,
        AuthUnexpectedStatus,
        LogUnexpectedStatus,
        DataplaneApiUnexpectedStatus,
    ) as e:
        # Generated clients use raise_on_unexpected_status=True, so undocumented
        # statuses bubble up as UnexpectedStatus and we convert here.
        raise exception_from_response(message, e) from e
    except httpx.TimeoutException as e:
        raise TimeoutError(
            f"{message}. The request timed out. "
            "Please check your connection and try again."
        ) from e
    except httpx.NetworkError as e:
        # Include the socket-level cause (e.g. `[Errno 111] Connection refused`)
        # so users can act on it; the wrapped str otherwise shows nothing useful.
        raise ConnectionError(f"{message}. Underlying error: {e}") from e
    except json.JSONDecodeError as e:
        # Malformed server response — programmer-side, not a user error.
        raise RuntimeError(
            "Error parsing the JSON response from the dltHub API. "
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
        # Upper-case the first character only. `.capitalize()` would lower-case the
        # rest, which flattens a multi-sentence detail. `details` may be None.
        detail_text = f"{details[:1].upper()}{details[1:]}" if details else details
        return RuntimeClientException(f"{message}. {detail_text} (HTTP {status})")
    return RuntimeClientException(f"{message}. Server error: {details} (HTTP {status})")
