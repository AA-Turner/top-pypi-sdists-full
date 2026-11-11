# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .command_dialog import CommandDialog
from .command_result import CommandResult
from .command_error_info import CommandErrorInfo

__all__ = ["SessionCommandsResponse", "Execution", "Page", "Observe"]


class Execution(BaseModel):
    id: str

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ran: int
    """Commands started."""

    replayed: bool

    state: Literal["queued", "running", "completed", "failed", "cancelled", "timeout", "expired"]

    error: Optional[CommandErrorInfo] = None


class Page(BaseModel):
    """The tab the execution used."""

    tab: str

    title: str

    url: str


class Observe(BaseModel):
    additions: Optional[int] = None

    base: Optional[str] = None

    diff: Optional[str] = None

    error: Optional[CommandErrorInfo] = None

    full: Optional[bool] = None

    removals: Optional[int] = None

    snapshot: Optional[str] = None

    snapshot_id: Optional[str] = FieldInfo(alias="snapshotId", default=None)


class SessionCommandsResponse(BaseModel):
    id: str
    """The id of this execution, the same as execution.id.

    Use it to get or cancel the execution.
    """

    execution: Execution

    page: Optional[Page] = None
    """The tab the execution used."""

    results: List[CommandResult]

    body_expired: Optional[bool] = FieldInfo(alias="bodyExpired", default=None)

    dialog: Optional[CommandDialog] = None
    """A dialog that is open on the tab and blocks it until it closes."""

    epoch_changed: Optional[bool] = FieldInfo(alias="epochChanged", default=None)
    """Set when the execution ran with after.

    Whether another execution, a quick action, or a browser restart changed the
    session since then. Input from CDP clients or the live view does not count.
    """

    next: Optional[str] = None
    """Send it as after in the next request."""

    observe: Optional[Observe] = None
