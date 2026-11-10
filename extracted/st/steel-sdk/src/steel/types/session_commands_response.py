# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .command_dialog import CommandDialog
from .command_events import CommandEvents
from .command_error_info import CommandErrorInfo

__all__ = [
    "SessionCommandsResponse",
    "CommandsExecution",
    "CommandsExecutionExecution",
    "CommandsExecutionPage",
    "CommandsExecutionResult",
    "CommandsExecutionObserve",
    "CommandsDialogAnswer",
]


class CommandsExecutionExecution(BaseModel):
    id: str

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ran: int
    """Commands started."""

    replayed: bool

    state: Literal["queued", "running", "completed", "failed", "cancelled", "timeout", "expired"]

    error: Optional[CommandErrorInfo] = None


class CommandsExecutionPage(BaseModel):
    """The tab the execution used."""

    tab: str

    title: str

    url: str


class CommandsExecutionResult(BaseModel):
    """Result of one command.

    Commands add their own fields, such as snapshot, value, url, or loading.
    """

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    error: Optional[CommandErrorInfo] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class CommandsExecutionObserve(BaseModel):
    additions: Optional[int] = None

    base: Optional[str] = None

    diff: Optional[str] = None

    error: Optional[CommandErrorInfo] = None

    full: Optional[bool] = None

    removals: Optional[int] = None

    snapshot: Optional[str] = None

    snapshot_id: Optional[str] = FieldInfo(alias="snapshotId", default=None)


class CommandsExecution(BaseModel):
    epoch: int
    """
    Goes up when commands or a dialog answer change the page, and when the browser
    restarts.
    """

    execution: CommandsExecutionExecution

    page: Optional[CommandsExecutionPage] = None
    """The tab the execution used."""

    results: List[CommandsExecutionResult]

    body_expired: Optional[bool] = FieldInfo(alias="bodyExpired", default=None)

    dialog: Optional[CommandDialog] = None
    """A JavaScript dialog: alert, confirm, prompt, or beforeunload."""

    epoch_changed: Optional[bool] = FieldInfo(alias="epochChanged", default=None)
    """Whether another Commands API client changed the session since after."""

    events: Optional[CommandEvents] = None
    """Navigations, opened and closed tabs, dialogs, and downloads since eventsAfter."""

    next: Optional[str] = None
    """Send it as after in the next request."""

    observe: Optional[CommandsExecutionObserve] = None


class CommandsDialogAnswer(BaseModel):
    """Response to the dialog command."""

    answered: CommandDialog
    """A JavaScript dialog: alert, confirm, prompt, or beforeunload."""

    epoch: int

    events: Optional[CommandEvents] = None
    """Navigations, opened and closed tabs, dialogs, and downloads since eventsAfter."""


SessionCommandsResponse: TypeAlias = Union[CommandsExecution, CommandsDialogAnswer]
