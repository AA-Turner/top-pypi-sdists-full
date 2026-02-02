"""Per-request context variables.

Affect things like logging and the names of metrics.
"""

import contextvars
import uuid
from dataclasses import dataclass

# These are sentinels used only in the Requester object below rather than actual org
# ids that our query middleware uses to make query instrumentation decisions
NOBODY_ORG_ID = "org-nobody"  # an org that owns nothing
SUPERUSER_ORG_ID = "org-superuser"  # an org that can see everything


@dataclass(frozen=True)
class Requester:
    """Info about the issuer of the request, populated by middleware."""

    org_id: str


_SERVICE_NAME = contextvars.ContextVar("service_name", default="corvic")
_TRACE_ID = contextvars.ContextVar("trace_id", default="")
_REQUESTER = contextvars.ContextVar(
    "requester_identity", default=Requester(org_id=NOBODY_ORG_ID)
)


def get_trace_id() -> str:
    """Get current trace id."""
    return _TRACE_ID.get()


def get_service_name() -> str:
    """Get current service name."""
    return _SERVICE_NAME.get()


def get_requester() -> Requester:
    """Get current requester."""
    return _REQUESTER.get()


def reset_context(*, service_name: str):
    """Reset contextvars for a new request."""
    _SERVICE_NAME.set(service_name)
    _TRACE_ID.set(str(uuid.uuid4()))
    _REQUESTER.set(Requester(org_id=NOBODY_ORG_ID))


def update_context(
    *, new_requester: Requester | None = None, new_service_name: str | None = None
):
    """Update selected contextvars for the current request."""
    if new_requester is not None:
        _REQUESTER.set(new_requester)
    if new_service_name is not None:
        _SERVICE_NAME.set(new_service_name)
