"""Compact centered confirm dialog.

Mirrors the rest of the TUI's minimal-chrome aesthetic: a small bordered
box with a title, a message, and a one-line keyboard hint — no buttons,
no extra padding, all styling in ``dreadnode.tcss``.

Returns ``True`` when the user confirms, ``False`` (or ``None`` from
Escape) when they cancel. The dialog is parameterized by ``intent``:

- ``danger``    — destructive (delete). Border + title in red.
                  ``Enter`` does NOT fire — only ``y`` confirms.
                  Prevents fat-finger Enter from firing destructive ops.
- ``warning``   — terminal but reversible-feeling (freeze). Border in
                  warning color. ``Enter`` and ``y`` both confirm.
- ``info``      — non-destructive prompts. ``Enter`` and ``y`` confirm.
"""

import typing as t

from rich.text import Text
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Static

from dreadnode.app.tui.theme import (
    ERROR,
    FG_MUTED,
    FG_SUBTLE,
    WARNING,
)

if t.TYPE_CHECKING:
    from textual.app import ComposeResult

Intent = t.Literal["danger", "warning", "info"]


class ConfirmModal(ModalScreen[bool]):
    """Small centered confirm dialog. Keyboard-driven, no buttons."""

    BINDINGS: t.ClassVar[list[Binding]] = [
        Binding("escape", "cancel", "Cancel", show=False),
        Binding("y", "confirm", "Confirm", show=False),
        Binding("n", "cancel", "Cancel", show=False),
        # Enter routes through ``soft_confirm`` so it's a no-op for
        # ``danger`` intent — fat-finger Enter on a delete prompt
        # silently does nothing instead of firing the destructive action.
        Binding("enter", "soft_confirm", "Confirm", show=False),
    ]

    def __init__(
        self,
        *,
        title: str,
        message: str,
        confirm_label: str = "Confirm",
        cancel_label: str = "Cancel",
        intent: Intent = "warning",
    ) -> None:
        super().__init__()
        self._title = title
        self._message = message
        self._confirm_label = confirm_label
        self._cancel_label = cancel_label
        self._intent = intent
        self.add_class(f"-{intent}")

    def compose(self) -> "ComposeResult":
        with Vertical(id="confirm-box"):
            yield Static(self._title_text(), id="confirm-title")
            yield Static(Text(self._message, style=FG_SUBTLE), id="confirm-message")
            yield Static(self._hint_text(), id="confirm-hint")

    def _title_text(self) -> Text:
        if self._intent == "danger":
            color = ERROR
        elif self._intent == "warning":
            color = WARNING
        else:
            color = FG_SUBTLE
        return Text(self._title, style=f"bold {color}")

    def _hint_text(self) -> Text:
        # Right-aligned via #confirm-hint CSS; verb pairs read as "key →
        # action" so the user knows which letter does what without
        # hunting for a button focus ring.
        text = Text(justify="right")
        text.append("y", style=f"bold {FG_MUTED}")
        text.append(f" {self._confirm_label.lower()}   ", style=FG_SUBTLE)
        text.append("n / esc", style=f"bold {FG_MUTED}")
        text.append(f" {self._cancel_label.lower()}", style=FG_SUBTLE)
        return text

    def action_confirm(self) -> None:
        self.dismiss(True)

    def action_soft_confirm(self) -> None:
        """Enter handler — confirms for non-danger intents only.

        ``danger`` prompts force the user to deliberately press ``y``;
        Enter is intentionally a no-op there.
        """
        if self._intent == "danger":
            return
        self.dismiss(True)

    def action_cancel(self) -> None:
        self.dismiss(False)
