"""Connection error screen — shown when the platform is unreachable."""

from __future__ import annotations

import typing as t

from rich.text import Text
from textual.binding import Binding
from textual.containers import Vertical
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Static

from dreadnode.app.config import UserConfig
from dreadnode.app.tui.theme import (
    BRAND,
    ERROR,
    FG_MUTED,
    FG_SUBTLE,
    pick_logo,
)

if t.TYPE_CHECKING:
    from textual.app import ComposeResult

STATUS_URL = "https://status.dreadnode.io"


class _Banner(Static):
    """Responsive logo banner — mirrors _AuthBanner in auth.py."""

    def render(self) -> Text:
        t = Text(justify="center")
        logo = pick_logo(self.size.width)
        if logo is not None:
            for line in logo.splitlines():
                t.append(line, style=BRAND)
                t.append("\n")
        else:
            t.append("DREADNODE", style=f"bold {BRAND}")
            t.append("\n")
        return t


class ConnectionErrorScreen(ModalScreen[bool]):
    """Full-screen modal shown when the platform server is unreachable.

    Stays mounted during retries — updates in-place to show connecting /
    error states so the user never sees the main screen flash through.

    Dismisses with ``True`` on successful reconnect or ``False`` to quit.
    """

    class RetryRequested(Message):
        """Posted when the user presses *r* — handled by the app."""

    class ProfileSwitchRequested(Message):
        """Posted when the user presses *p* to switch profiles."""

    BINDINGS: t.ClassVar[list[Binding]] = [
        Binding("r", "retry", "Retry", show=False),
        Binding("p", "switch_profile", "Profiles", show=False),
        Binding("escape", "quit_app", "Quit", show=False, priority=True),
        Binding("ctrl+q", "quit_app", "Quit", show=False),
    ]

    DEFAULT_CSS = """
    ConnectionErrorScreen {
        align: center middle;
    }
    #conn-error-box {
        width: 1fr;
        height: auto;
        padding: 1 2;
        content-align: center middle;
    }
    #conn-error-banner {
        width: 1fr;
        text-align: center;
        margin-top: 3;
        margin-bottom: 0;
    }
    #conn-error-message {
        width: 1fr;
        text-align: center;
        margin-top: 1;
    }
    #conn-error-status {
        width: 1fr;
        margin-top: 1;
        text-align: center;
    }
    #conn-error-hint {
        width: 1fr;
        text-align: center;
        margin-top: 1;
    }
    """

    def __init__(self, message: str) -> None:
        super().__init__()
        self._message = message
        self._retrying = False

    def compose(self) -> ComposeResult:
        with Vertical(id="conn-error-box"):
            yield _Banner(id="conn-error-banner")
            yield Static(id="conn-error-message")
            yield Static(id="conn-error-status")
            yield Static(id="conn-error-hint")

    def on_mount(self) -> None:
        self._show_error(self._message)

    def _show_error(self, message: str) -> None:
        self._retrying = False
        self._message = message

        msg = Text(message, style=ERROR, justify="center")
        self.query_one("#conn-error-message", Static).update(msg)

        status = Text(justify="center")
        status.append(STATUS_URL, style=f"underline {FG_MUTED} link {STATUS_URL}")
        self.query_one("#conn-error-status", Static).update(status)

        hint = Text(justify="center")
        hint.append("r ", style=f"bold {FG_MUTED}")
        hint.append("retry   ", style=FG_SUBTLE)
        if len(UserConfig.read().servers) > 1:
            hint.append("p ", style=f"bold {FG_MUTED}")
            hint.append("profiles   ", style=FG_SUBTLE)
        hint.append("Esc ", style=f"bold {FG_MUTED}")
        hint.append("quit", style=FG_SUBTLE)
        self.query_one("#conn-error-hint", Static).update(hint)

    def _show_connecting(self) -> None:
        self._retrying = True

        msg = Text("Connecting…", style=FG_MUTED, justify="center")
        self.query_one("#conn-error-message", Static).update(msg)
        self.query_one("#conn-error-status", Static).update("")

        hint = Text("Esc to cancel", style=FG_SUBTLE, justify="center")
        self.query_one("#conn-error-hint", Static).update(hint)

    def show_error(self, message: str) -> None:
        """Called by the app when a retry attempt fails."""
        self._show_error(message)

    def action_retry(self) -> None:
        if self._retrying:
            return
        self._show_connecting()
        self.post_message(self.RetryRequested())

    def action_switch_profile(self) -> None:
        if self._retrying:
            return
        if len(UserConfig.read().servers) <= 1:
            return
        self.post_message(self.ProfileSwitchRequested())

    def action_quit_app(self) -> None:
        self.dismiss(False)
