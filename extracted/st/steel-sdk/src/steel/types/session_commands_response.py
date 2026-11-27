# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .command_held import CommandHeld
from .command_dialog import CommandDialog
from .command_result import CommandResult
from .command_error_info import CommandErrorInfo

__all__ = ["SessionCommandsResponse", "Page", "Observe"]


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
    """The id of this execution. Use it to get or cancel the execution."""

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    page: Optional[Page] = None
    """The tab the execution used."""

    ran: int
    """Commands started."""

    replayed: bool
    """This is the stored result of an earlier request. Nothing ran again."""

    results: List[CommandResult]

    state: Literal["running", "completed", "failed", "cancelled", "timeout"]

    body_expired: Optional[bool] = FieldInfo(alias="bodyExpired", default=None)

    dialog: Optional[CommandDialog] = None
    """A dialog that is open on the tab and blocks it until it closes."""

    epoch_changed: Optional[bool] = FieldInfo(alias="epochChanged", default=None)
    """Set when the execution ran with after.

    Whether another execution, a quick action, or a browser restart changed the
    session since then. Input from CDP clients or the live view does not count.
    """

    held: Optional[List[CommandHeld]] = None
    """Tabs with keys or a mouse button still held down.

    Left out when nothing is held.
    """

    next: Optional[str] = None
    """Send it as after in the next request."""

    observe: Optional[Observe] = None

    stopped: Optional[CommandErrorInfo] = None
    """
    Why the execution stopped early, such as a cancel, a timeout, or a browser
    restart. A failed command has its error in results instead.
    """
