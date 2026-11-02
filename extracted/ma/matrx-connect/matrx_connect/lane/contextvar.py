from __future__ import annotations

from contextvars import ContextVar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from matrx_connect.lane.core import RequestLane


# A SEPARATE ContextVar — not a field on AppContext, which is frozen.
# asyncio.create_task snapshots the current context via copy_context(), so
# child agents and tasks spawned during a request automatically inherit
# the parent lane. Intermediate set_app_context() / clear_app_context()
# calls only touch _app_context; they leave _request_lane untouched.
_request_lane: ContextVar["RequestLane | None"] = ContextVar(
    "matrx_connect.lane.request_lane", default=None
)


def get_current_lane() -> "RequestLane | None":
    """Return the lane in the current ContextVar, or None if not in a lane scope.

    Returning None is a *normal* outcome — non-HTTP scripts, migrations, and
    tests that haven't opened a lane will see None. Callers MUST handle this
    case (typically by running inline + logging a warning, see RequestLane.submit).
    """
    return _request_lane.get()


def set_current_lane(lane: "RequestLane | None"):
    """Install a lane in the current ContextVar. Returns the reset token.

    Only the lane's own context-manager / open()/close() should call this.
    Application code should never reach for set_current_lane directly.
    """
    return _request_lane.set(lane)


def reset_current_lane(token) -> None:
    """Reset the ContextVar to its prior value (paired with set_current_lane)."""
    _request_lane.reset(token)
