# We need an abstraction layer above library calls to take into account interactive vs non-interactive mode differences
# and specify common colors/styles/icons for different types of messages (e.g. info, error, etc.).

from enum import StrEnum
from types import TracebackType
from typing import Optional, Type

from rich.console import Console
from rich.progress import Progress


# The differences between interactive and non-interactive mode outputs are:
#          Non-Interactive                          Interactive
# stdout   command output for scripts               user-friendly messages about execution status
# stderr   logs according to loglevel or nothing    nothing
# logfile  logs according to loglevel or nothing    logs according to loglevel or nothing
_is_interactive_mode: bool = False

def set_interactive_mode(interactive: bool) -> None:
    global _is_interactive_mode
    _is_interactive_mode = interactive

def is_interactive() -> bool:
    return _is_interactive_mode


class ConsoleTheme(StrEnum):
    """
    For different terminal backgrounds and accessibility issues we need different console themes.
    """
    DARK  = "dark"
    LIGHT = "light"
    HIGH_CONTRAST_BW = "high-contrast-bw"

_console_theme: ConsoleTheme = ConsoleTheme.DARK

def set_console_theme(theme: ConsoleTheme) -> None:
    global _console_theme
    _console_theme = theme


class MsgType(StrEnum):
    """
    Message types for console output.
    """
    TITLE   = "title"
    INFO    = "info"
    SUCCESS = "success"
    ERROR   = "error"
    WARNING = "warning"

_prefix_texts: dict[MsgType, str] = {
    MsgType.TITLE:   "[bold]i[/bold]",
    MsgType.INFO:    "➞",
    MsgType.SUCCESS: "✓",
    MsgType.ERROR:   "[bold]✗ ERROR:[/bold]",
    MsgType.WARNING: "⚠"
}

_msg_prefix_styles: dict[ConsoleTheme, dict[MsgType, str]] = {
    ConsoleTheme.DARK: {
        MsgType.TITLE: "bright_yellow", # https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors
        MsgType.INFO: "#4E9CC0",
        MsgType.SUCCESS: "#38A585",
        MsgType.ERROR: "#FB5D5D",
        MsgType.WARNING: "#C08A00",
    },
    ConsoleTheme.LIGHT: {
        MsgType.TITLE: "royal_blue1",
        MsgType.INFO: "#4E9CC0",
        MsgType.SUCCESS: "#38A515",
        MsgType.ERROR: "#FB1D1D",
        MsgType.WARNING: "#804A00",
    },
    ConsoleTheme.HIGH_CONTRAST_BW: {
        MsgType.TITLE: "bright_white on black",
        MsgType.INFO: "white on black",
        MsgType.SUCCESS: "bright_white on black",
        MsgType.ERROR: "bright_white on black",
        MsgType.WARNING: "bright_white on black",
    },
}

_msg_text_styles: dict[ConsoleTheme, dict[MsgType, str]] = {
    ConsoleTheme.DARK: {
        MsgType.TITLE:   "#FFFFFF",
        MsgType.INFO:    "#939393",
        MsgType.SUCCESS: "#FFFFFF",
        MsgType.ERROR:   "#FFFFFF",
        MsgType.WARNING: "#939393",
    },
    ConsoleTheme.LIGHT: {
        MsgType.TITLE:   "#000000",
        MsgType.INFO:    "#535353",
        MsgType.SUCCESS: "#000000",
        MsgType.ERROR:   "#000000",
        MsgType.WARNING: "#535353",
    },
    ConsoleTheme.HIGH_CONTRAST_BW: {
        MsgType.TITLE:   "bright_white on black",
        MsgType.INFO:    "white on black",
        MsgType.SUCCESS: "bright_white on black",
        MsgType.ERROR:   "bright_white on black",
        MsgType.WARNING: "bright_white on black",
    },
}

_console = Console(highlight=False)

def print_message(msg_type: MsgType, text: str) -> None:
    """
    Print a message to the console with the appropriate style and prefix.
    """
    if _is_interactive_mode:
        _console.print(_prefix_texts[msg_type], style=_msg_prefix_styles[_console_theme][msg_type], end=" ")
        _console.print(text, style=_msg_text_styles[_console_theme][msg_type], end="\n")

def title(text: str) -> None:
    print_message(MsgType.TITLE, text)

def info(text: str) -> None:
    print_message(MsgType.INFO, text)

def success(text: str) -> None:
    print_message(MsgType.SUCCESS, text)

def error(text: str) -> None:
    print_message(MsgType.ERROR, text)

def warning(text: str) -> None:
    print_message(MsgType.WARNING, text)


class JobProgress:
    """
    A class to manage job progress in the console. Shall do nothing in non-interactive mode.
    """
    _progress: Progress | None = None
    _description: str = "Waiting..."
    _total: float | None = None

    def __init__(self, description: str, total_steps: float | None = None) -> None:
        if _is_interactive_mode:
            self._progress = Progress(transient=True)
            self._description = description
            self._total = total_steps

    def __enter__(self) -> 'JobProgress':
        if self._progress is not None:
            self._progress.__enter__()
            self._progress.add_task(self._description, total=self._total)
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        if self._progress is not None:
            self._progress.__exit__(exc_type, exc_value, traceback)

    def update(self, advance: float) -> None:
        if self._progress is not None and len(self._progress.tasks) > 0:
            self._progress.update(self._progress.tasks[0].id, advance=advance)
