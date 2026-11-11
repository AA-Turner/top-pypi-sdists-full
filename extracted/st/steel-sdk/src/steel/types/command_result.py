# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from pydantic import Field as FieldInfo

from .._utils import PropertyInfo
from .._models import BaseModel
from .command_dialog import CommandDialog
from .command_error_info import CommandErrorInfo

__all__ = [
    "CommandResult",
    "NavigateResult",
    "BackResult",
    "ForwardResult",
    "ReloadResult",
    "SnapshotResult",
    "ClickResult",
    "DblclickResult",
    "HoverResult",
    "FocusResult",
    "TypeResult",
    "FillResult",
    "PressResult",
    "KeydownResult",
    "KeyupResult",
    "MouseResult",
    "SelectResult",
    "CheckResult",
    "UncheckResult",
    "UploadResult",
    "DragResult",
    "GetResult",
    "IsResult",
    "WaitResult",
    "ScreenshotResult",
    "EvalResult",
    "PdfResult",
    "ScrollResult",
    "FindResult",
    "FindResultMatch",
    "TabResult",
    "TabResultTab",
]


class NavigateResult(BaseModel):
    """Result of a navigate command."""

    command: Literal["navigate"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    error: Optional[CommandErrorInfo] = None

    url: Optional[str] = None


class BackResult(BaseModel):
    """Result of a back command."""

    command: Literal["back"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    error: Optional[CommandErrorInfo] = None

    navigated: Optional[bool] = None
    """False when there was no history entry."""

    url: Optional[str] = None


class ForwardResult(BaseModel):
    """Result of a forward command."""

    command: Literal["forward"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    error: Optional[CommandErrorInfo] = None

    navigated: Optional[bool] = None
    """False when there was no history entry."""

    url: Optional[str] = None


class ReloadResult(BaseModel):
    """Result of a reload command."""

    command: Literal["reload"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    error: Optional[CommandErrorInfo] = None

    url: Optional[str] = None


class SnapshotResult(BaseModel):
    """Result of a snapshot command."""

    command: Literal["snapshot"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    error: Optional[CommandErrorInfo] = None

    snapshot: Optional[str] = None

    snapshot_id: Optional[str] = FieldInfo(alias="snapshotId", default=None)


class ClickResult(BaseModel):
    """Result of a click command."""

    command: Literal["click"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    dialog: Optional[CommandDialog] = None
    """A dialog that the command opened. It blocks the tab until it closes."""

    error: Optional[CommandErrorInfo] = None

    loading: Optional[bool] = None
    """The command started a navigation that was still loading when it returned."""


class DblclickResult(BaseModel):
    """Result of a dblclick command."""

    command: Literal["dblclick"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    dialog: Optional[CommandDialog] = None
    """A dialog that the command opened. It blocks the tab until it closes."""

    error: Optional[CommandErrorInfo] = None

    loading: Optional[bool] = None
    """The command started a navigation that was still loading when it returned."""


class HoverResult(BaseModel):
    """Result of a hover command."""

    command: Literal["hover"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    dialog: Optional[CommandDialog] = None
    """A dialog that the command opened. It blocks the tab until it closes."""

    error: Optional[CommandErrorInfo] = None


class FocusResult(BaseModel):
    """Result of a focus command."""

    command: Literal["focus"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    error: Optional[CommandErrorInfo] = None


class TypeResult(BaseModel):
    """Result of a type command."""

    command: Literal["type"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    dialog: Optional[CommandDialog] = None
    """A dialog that the command opened. It blocks the tab until it closes."""

    error: Optional[CommandErrorInfo] = None

    loading: Optional[bool] = None
    """The command started a navigation that was still loading when it returned."""


class FillResult(BaseModel):
    """Result of a fill command."""

    command: Literal["fill"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    dialog: Optional[CommandDialog] = None
    """A dialog that the command opened. It blocks the tab until it closes."""

    error: Optional[CommandErrorInfo] = None

    loading: Optional[bool] = None
    """The command started a navigation that was still loading when it returned."""


class PressResult(BaseModel):
    """Result of a press command."""

    command: Literal["press"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    dialog: Optional[CommandDialog] = None
    """A dialog that the command opened. It blocks the tab until it closes."""

    error: Optional[CommandErrorInfo] = None

    loading: Optional[bool] = None
    """The command started a navigation that was still loading when it returned."""


class KeydownResult(BaseModel):
    """Result of a keydown command."""

    command: Literal["keydown"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    dialog: Optional[CommandDialog] = None
    """A dialog that the command opened. It blocks the tab until it closes."""

    error: Optional[CommandErrorInfo] = None

    loading: Optional[bool] = None
    """The command started a navigation that was still loading when it returned."""


class KeyupResult(BaseModel):
    """Result of a keyup command."""

    command: Literal["keyup"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    dialog: Optional[CommandDialog] = None
    """A dialog that the command opened. It blocks the tab until it closes."""

    error: Optional[CommandErrorInfo] = None

    loading: Optional[bool] = None
    """The command started a navigation that was still loading when it returned."""


class MouseResult(BaseModel):
    """Result of a mouse command."""

    command: Literal["mouse"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    dialog: Optional[CommandDialog] = None
    """A dialog that the command opened. It blocks the tab until it closes."""

    error: Optional[CommandErrorInfo] = None

    loading: Optional[bool] = None
    """The command started a navigation that was still loading when it returned."""


class SelectResult(BaseModel):
    """Result of a select command."""

    command: Literal["select"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    dialog: Optional[CommandDialog] = None
    """A dialog that the command opened. It blocks the tab until it closes."""

    error: Optional[CommandErrorInfo] = None

    loading: Optional[bool] = None
    """The command started a navigation that was still loading when it returned."""

    selected: Optional[List[str]] = None
    """The values of the selected options."""


class CheckResult(BaseModel):
    """Result of a check command."""

    command: Literal["check"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    checked: Optional[bool] = None

    dialog: Optional[CommandDialog] = None
    """A dialog that the command opened. It blocks the tab until it closes."""

    error: Optional[CommandErrorInfo] = None

    loading: Optional[bool] = None
    """The command started a navigation that was still loading when it returned."""


class UncheckResult(BaseModel):
    """Result of a uncheck command."""

    command: Literal["uncheck"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    checked: Optional[bool] = None

    dialog: Optional[CommandDialog] = None
    """A dialog that the command opened. It blocks the tab until it closes."""

    error: Optional[CommandErrorInfo] = None

    loading: Optional[bool] = None
    """The command started a navigation that was still loading when it returned."""


class UploadResult(BaseModel):
    """Result of a upload command."""

    command: Literal["upload"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    dialog: Optional[CommandDialog] = None
    """A dialog that the command opened. It blocks the tab until it closes."""

    error: Optional[CommandErrorInfo] = None

    files: Optional[List[str]] = None

    loading: Optional[bool] = None
    """The command started a navigation that was still loading when it returned."""


class DragResult(BaseModel):
    """Result of a drag command."""

    command: Literal["drag"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    dialog: Optional[CommandDialog] = None
    """A dialog that the command opened. It blocks the tab until it closes."""

    error: Optional[CommandErrorInfo] = None

    loading: Optional[bool] = None
    """The command started a navigation that was still loading when it returned."""


class GetResult(BaseModel):
    """Result of a get command."""

    command: Literal["get"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    error: Optional[CommandErrorInfo] = None

    masked: Optional[bool] = None
    """The value is a secret, so it is left out."""

    value: Optional[object] = None
    """A string for text, html, markdown, value, attr, title, and url.

    A number for count. { x, y, width, height } or null for box. A list of locators
    for locator.
    """


class IsResult(BaseModel):
    """Result of a is command."""

    command: Literal["is"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    error: Optional[CommandErrorInfo] = None

    value: Optional[bool] = None


class WaitResult(BaseModel):
    """Result of a wait command."""

    command: Literal["wait"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    bytes: Optional[int] = None

    error: Optional[CommandErrorInfo] = None

    file: Optional[str] = None
    """The downloaded file, for download."""

    waited: Optional[Literal["ms", "target", "text", "url", "load", "download"]] = None


class ScreenshotResult(BaseModel):
    """Result of a screenshot command."""

    command: Literal["screenshot"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    data: Optional[str] = None

    error: Optional[CommandErrorInfo] = None

    format: Optional[Literal["png", "jpeg", "webp"]] = None


class EvalResult(BaseModel):
    """Result of a eval command."""

    command: Literal["eval"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    dialog: Optional[CommandDialog] = None
    """A dialog that the command opened. It blocks the tab until it closes."""

    error: Optional[CommandErrorInfo] = None

    loading: Optional[bool] = None
    """The command started a navigation that was still loading when it returned."""

    value: Optional[object] = None
    """The result of the script as JSON."""


class PdfResult(BaseModel):
    """Result of a pdf command."""

    command: Literal["pdf"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    data: Optional[str] = None

    error: Optional[CommandErrorInfo] = None

    format: Optional[Literal["pdf"]] = None


class ScrollResult(BaseModel):
    """Result of a scroll command."""

    command: Literal["scroll"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    error: Optional[CommandErrorInfo] = None

    moved: Optional[bool] = None

    x: Optional[float] = None

    y: Optional[float] = None


class FindResultMatch(BaseModel):
    name: str

    ref: str

    role: str


class FindResult(BaseModel):
    """Result of a find command."""

    command: Literal["find"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    count: Optional[int] = None

    error: Optional[CommandErrorInfo] = None

    matches: Optional[List[FindResultMatch]] = None


class TabResultTab(BaseModel):
    tab: str

    title: str

    url: str


class TabResult(BaseModel):
    """Result of a tab command."""

    command: Literal["tab"]

    effect: Literal["none", "applied", "unknown"]
    """What happened to the page: nothing, a change, or a possible change."""

    ok: bool

    error: Optional[CommandErrorInfo] = None

    tab: Optional[str] = None

    tabs: Optional[List[TabResultTab]] = None


CommandResult: TypeAlias = Annotated[
    Union[
        NavigateResult,
        BackResult,
        ForwardResult,
        ReloadResult,
        SnapshotResult,
        ClickResult,
        DblclickResult,
        HoverResult,
        FocusResult,
        TypeResult,
        FillResult,
        PressResult,
        KeydownResult,
        KeyupResult,
        MouseResult,
        SelectResult,
        CheckResult,
        UncheckResult,
        UploadResult,
        DragResult,
        GetResult,
        IsResult,
        WaitResult,
        ScreenshotResult,
        EvalResult,
        PdfResult,
        ScrollResult,
        FindResult,
        TabResult,
    ],
    PropertyInfo(discriminator="command"),
]
