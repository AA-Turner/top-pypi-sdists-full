"""Legacy single-line prompt status widget."""

from __future__ import annotations

from rich.text import Text
from textual.reactive import reactive
from textual.widgets import Static

from dreadnode.app.tui.model_variants import render_tokens
from dreadnode.app.tui.theme import FG_FAINTEST, FG_MUTED, FG_SUBTLE


class PromptInfo(Static):
    """Single-line prompt status used by legacy TUI tests."""

    agent_name: reactive[str] = reactive("")
    session_label: reactive[str] = reactive("")
    model_name: reactive[str] = reactive("")
    workspace_label: reactive[str] = reactive("")
    working_dir: reactive[str] = reactive("")
    connection: reactive[str] = reactive("")
    status_text: reactive[str] = reactive("")
    last_input_tokens: reactive[int] = reactive(0)
    model_max_tokens: reactive[int] = reactive(0)
    busy: reactive[bool] = reactive(False)

    def render(self) -> Text:
        parts: list[tuple[str, str] | Text] = []

        if self.session_label:
            parts.append((self.session_label, FG_SUBTLE))
        if self.workspace_label:
            parts.append((self.workspace_label, FG_MUTED))
        if self.agent_name:
            parts.append((f"@{self.agent_name}", FG_SUBTLE))
        if self.model_name:
            parts.append((self.model_name, "bold"))

        connection = (self.connection or "").strip()
        if connection.startswith(("http://", "https://")):
            parts.append(("platform", FG_MUTED))
        elif connection:
            parts.append((connection, FG_MUTED))
        elif self.working_dir:
            parts.append(("local", FG_MUTED))

        if self.last_input_tokens > 0:
            limit = self.model_max_tokens if self.model_max_tokens > 0 else None
            parts.append(render_tokens(self.last_input_tokens, limit))

        if self.status_text and not self.busy:
            parts.append((self.status_text, FG_FAINTEST))

        rendered = Text(no_wrap=True, overflow="ellipsis")
        for index, part in enumerate(parts):
            if index:
                rendered.append(" · ", style=FG_FAINTEST)
            if isinstance(part, Text):
                rendered.append_text(part)
            else:
                rendered.append(part[0], style=part[1])

        return rendered
