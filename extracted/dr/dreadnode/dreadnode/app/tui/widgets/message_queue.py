"""Message queue widget — shows pending messages queued while the agent is working."""

from __future__ import annotations

import typing as t

from textual.widgets import Static

from dreadnode.app.tui.theme import FG_MUTED


class MessageQueue(Static):
    """Displays queued messages. Hidden when empty."""

    DEFAULT_CSS = f"""
    MessageQueue {{
        display: none;
        height: auto;
        color: {FG_MUTED};
    }}
    MessageQueue.-visible {{
        display: block;
    }}
    """

    def __init__(self, **kwargs: t.Any) -> None:
        super().__init__("", **kwargs)
        self._messages: list[str] = []

    def set_messages(self, messages: list[str]) -> None:
        """Update displayed queue contents."""
        self._messages = list(messages)
        if not self._messages:
            self.update("")
            self.remove_class("-visible")
            return
        self.add_class("-visible")
        self.update(self._format_queue())

    def _format_queue(self) -> str:
        """Render queued messages as plain styled text with hint."""
        max_len = max(self.size.width - 4, 20)  # leave room for bullet + padding
        lines: list[str] = []
        for msg in self._messages:
            display = msg.replace("\n", " ")
            if len(display) > max_len:
                display = display[: max_len - 1] + "\u2026"
            lines.append(f"\u23f5 {display}")
        lines.append("\u2191 to edit")
        return "\n".join(lines)
