# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo
from .command_param import CommandParam
from .command_frame_param import CommandFrameParam
from .command_target_param import CommandTargetParam
from .command_expectation_param import CommandExpectationParam

__all__ = [
    "SessionCommandsParams",
    "Commands",
    "CommandsNavigateCommand",
    "CommandsBackCommand",
    "CommandsForwardCommand",
    "CommandsReloadCommand",
    "CommandsSnapshotCommand",
    "CommandsClickCommand",
    "CommandsDblclickCommand",
    "CommandsHoverCommand",
    "CommandsFocusCommand",
    "CommandsTypeCommand",
    "CommandsFillCommand",
    "CommandsPressCommand",
    "CommandsKeydownCommand",
    "CommandsKeyupCommand",
    "CommandsMouseCommand",
    "CommandsSelectCommand",
    "CommandsCheckCommand",
    "CommandsUploadCommand",
    "CommandsDragCommand",
    "CommandsUncheckCommand",
    "CommandsGetCommand",
    "CommandsIsCommand",
    "CommandsWaitCommand",
    "CommandsScreenshotCommand",
    "CommandsEvalCommand",
    "CommandsPdfCommand",
    "CommandsScrollCommand",
    "CommandsFindCommand",
    "CommandsTabCommand",
    "Observe",
]


class SessionCommandsParams(TypedDict, total=False):
    commands: Required[Commands]
    """One command, or an array of up to 50.

    They run in order and stop at the first failure. Commands that already ran are
    not undone.
    """

    after: str
    """The next value from your last response.

    A retry with the same after and commands runs only once.
    """

    observe: Observe
    """Returns a snapshot, or a diff against the last one, after the commands."""

    idempotency_key: Annotated[str, PropertyInfo(alias="idempotency-key")]


class CommandsNavigateCommand(TypedDict, total=False):
    """Opens a URL in the tab.

    Only http, https, and about:blank. A URL without a scheme gets https://.
    """

    command: Required[Literal["navigate"]]

    url: Required[str]

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""


class CommandsBackCommand(TypedDict, total=False):
    """Goes back one history entry."""

    command: Required[Literal["back"]]

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""


class CommandsForwardCommand(TypedDict, total=False):
    """Goes forward one history entry."""

    command: Required[Literal["forward"]]

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""


class CommandsReloadCommand(TypedDict, total=False):
    """Reloads the tab."""

    command: Required[Literal["reload"]]

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""


class CommandsSnapshotCommand(TypedDict, total=False):
    """
    Returns the accessibility tree of the page, with a ref for each element you can act on.
    """

    command: Required[Literal["snapshot"]]

    compact: bool
    """Only lines with refs or values, and their ancestors."""

    depth: int
    """Only lines up to this depth."""

    interactive: bool
    """Only lines with refs."""

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""


class CommandsClickCommand(TypedDict, total=False):
    """Clicks the element with the mouse."""

    command: Required[Literal["click"]]

    target: Required[CommandTargetParam]
    """A ref from a snapshot such as e12, a CSS selector, or a locator."""

    expect: CommandExpectationParam
    """Fails the command when the element does not have this role or name."""

    frame: CommandFrameParam
    """The iframe to look in. List nested iframes from the outside in."""

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""


class CommandsDblclickCommand(TypedDict, total=False):
    """Double-clicks the element with the mouse."""

    command: Required[Literal["dblclick"]]

    target: Required[CommandTargetParam]
    """A ref from a snapshot such as e12, a CSS selector, or a locator."""

    expect: CommandExpectationParam
    """Fails the command when the element does not have this role or name."""

    frame: CommandFrameParam
    """The iframe to look in. List nested iframes from the outside in."""

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""


class CommandsHoverCommand(TypedDict, total=False):
    """Moves the mouse onto the element."""

    command: Required[Literal["hover"]]

    target: Required[CommandTargetParam]
    """A ref from a snapshot such as e12, a CSS selector, or a locator."""

    expect: CommandExpectationParam
    """Fails the command when the element does not have this role or name."""

    frame: CommandFrameParam
    """The iframe to look in. List nested iframes from the outside in."""

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""


class CommandsFocusCommand(TypedDict, total=False):
    """Focuses the element."""

    command: Required[Literal["focus"]]

    target: Required[CommandTargetParam]
    """A ref from a snapshot such as e12, a CSS selector, or a locator."""

    expect: CommandExpectationParam
    """Fails the command when the element does not have this role or name."""

    frame: CommandFrameParam
    """The iframe to look in. List nested iframes from the outside in."""

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""


class CommandsTypeCommand(TypedDict, total=False):
    """Types text one key press at a time, after the current content."""

    command: Required[Literal["type"]]

    target: Required[CommandTargetParam]
    """A ref from a snapshot such as e12, a CSS selector, or a locator."""

    text: Required[str]

    clear: bool
    """Replace the current content."""

    delay: int
    """Milliseconds to wait between key presses."""

    expect: CommandExpectationParam
    """Fails the command when the element does not have this role or name."""

    frame: CommandFrameParam
    """The iframe to look in. List nested iframes from the outside in."""

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""


class CommandsFillCommand(TypedDict, total=False):
    """Replaces the content of a field in one step, without key presses."""

    command: Required[Literal["fill"]]

    target: Required[CommandTargetParam]
    """A ref from a snapshot such as e12, a CSS selector, or a locator."""

    value: Required[str]

    expect: CommandExpectationParam
    """Fails the command when the element does not have this role or name."""

    frame: CommandFrameParam
    """The iframe to look in. List nested iframes from the outside in."""

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""


class CommandsPressCommand(TypedDict, total=False):
    """Presses a key, such as Enter, or a combination such as Control+a."""

    command: Required[Literal["press"]]

    key: Required[str]

    expect: CommandExpectationParam
    """Fails the command when the element does not have this role or name."""

    frame: CommandFrameParam
    """The iframe to look in. List nested iframes from the outside in."""

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""

    target: CommandTargetParam
    """A ref from a snapshot such as e12, a CSS selector, or a locator."""


class CommandsKeydownCommand(TypedDict, total=False):
    """Holds a key down until its keyup."""

    command: Required[Literal["keydown"]]

    key: Required[str]

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""


class CommandsKeyupCommand(TypedDict, total=False):
    """Lets go of a key held with keydown."""

    command: Required[Literal["keyup"]]

    key: Required[str]

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""


class CommandsMouseCommand(TypedDict, total=False):
    """
    Mouse input at a point in CSS pixels of the visible part of the page, for pages without useful elements such as a canvas.
    """

    action: Required[Literal["move", "down", "up", "click", "wheel"]]

    command: Required[Literal["mouse"]]

    button: Literal["left", "right", "middle"]

    clicks: int

    delta_x: Annotated[float, PropertyInfo(alias="deltaX")]

    delta_y: Annotated[float, PropertyInfo(alias="deltaY")]

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""

    x: float

    y: float


class CommandsSelectCommand(TypedDict, total=False):
    """Selects options. Matches by value, then by label."""

    command: Required[Literal["select"]]

    target: Required[CommandTargetParam]
    """A ref from a snapshot such as e12, a CSS selector, or a locator."""

    values: Required[Union[str, SequenceNotStr[str]]]

    expect: CommandExpectationParam
    """Fails the command when the element does not have this role or name."""

    frame: CommandFrameParam
    """The iframe to look in. List nested iframes from the outside in."""

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""


class CommandsCheckCommand(TypedDict, total=False):
    """Checks a checkbox, radio button, switch, or toggle button."""

    command: Required[Literal["check"]]

    target: Required[CommandTargetParam]
    """A ref from a snapshot such as e12, a CSS selector, or a locator."""

    expect: CommandExpectationParam
    """Fails the command when the element does not have this role or name."""

    frame: CommandFrameParam
    """The iframe to look in. List nested iframes from the outside in."""

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""


class CommandsUploadCommand(TypedDict, total=False):
    """Sets the files of a file input. Upload the files to the session first."""

    command: Required[Literal["upload"]]

    files: Required[Union[str, SequenceNotStr[str]]]

    target: Required[CommandTargetParam]
    """A ref from a snapshot such as e12, a CSS selector, or a locator."""

    expect: CommandExpectationParam
    """Fails the command when the element does not have this role or name."""

    frame: CommandFrameParam
    """The iframe to look in. List nested iframes from the outside in."""

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""


class CommandsDragCommand(TypedDict, total=False):
    """Drags one element onto another with the mouse."""

    command: Required[Literal["drag"]]

    source: Required[CommandTargetParam]
    """A ref from a snapshot such as e12, a CSS selector, or a locator."""

    target: Required[CommandTargetParam]
    """A ref from a snapshot such as e12, a CSS selector, or a locator."""

    frame: CommandFrameParam
    """The iframe to look in. List nested iframes from the outside in."""

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""


class CommandsUncheckCommand(TypedDict, total=False):
    """Unchecks a checkbox, switch, or toggle button."""

    command: Required[Literal["uncheck"]]

    target: Required[CommandTargetParam]
    """A ref from a snapshot such as e12, a CSS selector, or a locator."""

    expect: CommandExpectationParam
    """Fails the command when the element does not have this role or name."""

    frame: CommandFrameParam
    """The iframe to look in. List nested iframes from the outside in."""

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""


class CommandsGetCommand(TypedDict, total=False):
    """Reads something from the page or an element."""

    command: Required[Literal["get"]]

    what: Required[Literal["text", "html", "markdown", "value", "attr", "title", "url", "count", "box", "locator"]]

    attribute: str
    """The attribute to read with attr."""

    expect: CommandExpectationParam
    """Fails the command when the element does not have this role or name."""

    frame: CommandFrameParam
    """The iframe to look in. List nested iframes from the outside in."""

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""

    target: CommandTargetParam
    """A ref from a snapshot such as e12, a CSS selector, or a locator."""


class CommandsIsCommand(TypedDict, total=False):
    """Checks the state of an element."""

    command: Required[Literal["is"]]

    target: Required[CommandTargetParam]
    """A ref from a snapshot such as e12, a CSS selector, or a locator."""

    what: Required[Literal["visible", "enabled", "checked"]]

    expect: CommandExpectationParam
    """Fails the command when the element does not have this role or name."""

    frame: CommandFrameParam
    """The iframe to look in. List nested iframes from the outside in."""

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""


class CommandsWaitCommand(TypedDict, total=False):
    """
    Waits for one of an element, text, a URL, a load state, a download, or a fixed time.
    """

    command: Required[Literal["wait"]]

    download: Literal[True]
    """Waits for the next download to finish."""

    expect: CommandExpectationParam
    """Fails the command when the element does not have this role or name."""

    frame: CommandFrameParam
    """The iframe to look in. List nested iframes from the outside in."""

    load: Literal["load", "domcontentloaded", "networkidle"]

    ms: int

    state: Literal["visible", "hidden", "attached", "detached"]

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""

    target: CommandTargetParam
    """A ref from a snapshot such as e12, a CSS selector, or a locator."""

    text: str

    timeout: int
    """Milliseconds. 10000 by default."""

    url: str
    """A URL pattern. \\** matches any characters."""


class CommandsScreenshotCommand(TypedDict, total=False):
    """Captures the page or an element as base64 data."""

    command: Required[Literal["screenshot"]]

    expect: CommandExpectationParam
    """Fails the command when the element does not have this role or name."""

    format: Literal["png", "jpeg", "webp"]

    frame: CommandFrameParam
    """The iframe to look in. List nested iframes from the outside in."""

    full_page: Annotated[bool, PropertyInfo(alias="fullPage")]

    quality: int

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""

    target: CommandTargetParam
    """A ref from a snapshot such as e12, a CSS selector, or a locator."""


class CommandsEvalCommand(TypedDict, total=False):
    """Runs JavaScript in the page and returns the result as JSON."""

    command: Required[Literal["eval"]]

    script: Required[str]

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""

    timeout: int
    """Milliseconds. 10000 by default."""


class CommandsPdfCommand(TypedDict, total=False):
    """Prints the page to a PDF as base64 data."""

    command: Required[Literal["pdf"]]

    landscape: bool

    print_background: Annotated[bool, PropertyInfo(alias="printBackground")]

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""


class CommandsScrollCommand(TypedDict, total=False):
    """Scrolls the page, or an element when target is set."""

    command: Required[Literal["scroll"]]

    amount: float
    """Pixels. 300 by default."""

    direction: Literal["up", "down", "left", "right"]

    expect: CommandExpectationParam
    """Fails the command when the element does not have this role or name."""

    frame: CommandFrameParam
    """The iframe to look in. List nested iframes from the outside in."""

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""

    target: CommandTargetParam
    """A ref from a snapshot such as e12, a CSS selector, or a locator."""


class CommandsFindCommand(TypedDict, total=False):
    """Finds elements and returns refs for up to 50 matches.

    With nth, it returns that one match.
    """

    command: Required[Literal["find"]]

    target: Required[CommandTargetParam]
    """A CSS selector or a locator, not a ref."""

    frame: CommandFrameParam
    """The iframe to look in. List nested iframes from the outside in."""

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""


class CommandsTabCommand(TypedDict, total=False):
    """Lists, opens, or closes tabs. The last tab cannot be closed."""

    action: Required[Literal["list", "new", "close"]]

    command: Required[Literal["tab"]]

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""

    url: str


Commands: TypeAlias = Union[
    CommandsNavigateCommand,
    CommandsBackCommand,
    CommandsForwardCommand,
    CommandsReloadCommand,
    CommandsSnapshotCommand,
    CommandsClickCommand,
    CommandsDblclickCommand,
    CommandsHoverCommand,
    CommandsFocusCommand,
    CommandsTypeCommand,
    CommandsFillCommand,
    CommandsPressCommand,
    CommandsKeydownCommand,
    CommandsKeyupCommand,
    CommandsMouseCommand,
    CommandsSelectCommand,
    CommandsCheckCommand,
    CommandsUploadCommand,
    CommandsDragCommand,
    CommandsUncheckCommand,
    CommandsGetCommand,
    CommandsIsCommand,
    CommandsWaitCommand,
    CommandsScreenshotCommand,
    CommandsEvalCommand,
    CommandsPdfCommand,
    CommandsScrollCommand,
    CommandsFindCommand,
    CommandsTabCommand,
    Iterable[CommandParam],
]


class Observe(TypedDict, total=False):
    """Returns a snapshot, or a diff against the last one, after the commands."""

    mode: Required[Literal["none", "snapshot", "diff"]]

    base: str
    """A snapshot id to diff against."""

    compact: bool
    """Only lines with refs or values, and their ancestors."""

    depth: int
    """Only lines up to this depth."""

    interactive: bool
    """Only lines with refs."""

    tab: str
    """A tab id such as t2. A command on a ref does not need it."""
