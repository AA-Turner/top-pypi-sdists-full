"""Toast notification widget -- single line, auto-hides after a configurable duration."""

from __future__ import annotations

import typing as t

from textual.widgets import Static

from dreadnode.app.tui.theme import ERROR, FG_FAINTEST, FG_SUBTLE, INFO, SUCCESS, WARNING

if t.TYPE_CHECKING:
    from textual.timer import Timer


class Flash(Static):
    """Single-line notification that auto-hides after a duration."""

    DEFAULT_CSS = f"""
    Flash {{
        height: 1;
        text-align: center;
        color: {FG_FAINTEST};
    }}
    Flash.-visible {{
        color: {FG_SUBTLE};
    }}
    Flash.-success {{
        background: {SUCCESS} 15%;
        color: {SUCCESS};
    }}
    Flash.-error {{
        background: {ERROR} 15%;
        color: {ERROR};
    }}
    Flash.-warning {{
        background: {WARNING} 15%;
        color: {WARNING};
    }}
    Flash.-info {{
        background: {INFO} 15%;
        color: {INFO};
    }}
    """

    _STYLES = ("success", "error", "warning", "info")

    def __init__(self, **kwargs: t.Any) -> None:
        super().__init__("", **kwargs)
        self._hide_timer: Timer | None = None

    def flash(self, message: str, *, duration: float = 3.0, severity: str = "info") -> None:
        """Show *message* for *duration* seconds, styled by *severity*."""
        # Cancel any pending hide
        if self._hide_timer is not None:
            self._hide_timer.stop()
            self._hide_timer = None

        # Swap style classes
        for cls in self._STYLES:
            self.remove_class(f"-{cls}")
        if severity in self._STYLES:
            self.add_class(f"-{severity}")

        self.update(message)
        self.add_class("-visible")

        self._hide_timer = self.set_timer(duration, self._auto_hide)

    def _auto_hide(self) -> None:
        self.update("")
        self.remove_class("-visible")
        for cls in self._STYLES:
            self.remove_class(f"-{cls}")
        self._hide_timer = None
