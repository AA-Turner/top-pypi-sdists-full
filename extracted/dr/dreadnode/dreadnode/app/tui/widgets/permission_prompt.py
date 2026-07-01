"""Runtime permission widget (Allow / Allow Session / Deny).

This widget renders runtime tool-gating prompts only — the flow that
intercepts a tool call (e.g. ``bash`` wants to run a destructive
command). Agent-initiated questions go through ``HumanPromptWidget``
in ``human_prompt.py``.

Today the runtime permission flow has no production emitter — hooks
that would gate tool calls aren't wired through to a wire event yet.
The widget is kept as a placeholder so the future ticket that adds
``permissionrequired`` events has a UI surface to plug into. Tests
exercise it directly.
"""

from __future__ import annotations

import typing as t

from rich.text import Text
from textual.containers import Horizontal
from textual.message import Message
from textual.widgets import Button, Static

from dreadnode.app.tui.theme import BG_LIGHTER, FG, FG_SUBTLE, WARNING

if t.TYPE_CHECKING:
    from textual.app import ComposeResult


class PermissionPrompt(Static):
    """Runtime tool-gating prompt — Allow / Allow Session / Deny."""

    class Action(Message):
        """Posted when the user picks a permission decision."""

        def __init__(self, request_id: str, decision: str) -> None:
            self.request_id = request_id
            self.decision = decision
            super().__init__()

    DEFAULT_CSS = f"""
    PermissionPrompt {{
        display: none;
        height: auto;
        padding: 1 2;
        background: {BG_LIGHTER};
        border: solid {WARNING};
    }}
    PermissionPrompt.-active {{
        display: block;
    }}
    PermissionPrompt .perm-label {{
        height: auto;
        margin-bottom: 1;
    }}
    PermissionPrompt .perm-detail {{
        height: auto;
        color: {FG_SUBTLE};
        margin-bottom: 1;
    }}
    PermissionPrompt .perm-buttons {{
        height: 3;
    }}
    PermissionPrompt Button {{
        margin-right: 1;
    }}
    """

    def __init__(self, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)
        self._request_id: str = ""

    def compose(self) -> ComposeResult:
        yield Static("", id="perm-label", classes="perm-label")
        yield Static("", id="perm-detail", classes="perm-detail")
        yield Horizontal(
            Button("Allow", id="perm-allow", variant="success"),
            Button("Allow Session", id="perm-allow-session", variant="warning"),
            Button("Deny", id="perm-deny", variant="error"),
            classes="perm-buttons",
        )

    def show(self, request_id: str, summary: str, *, detail: str = "") -> None:
        """Display a permission request."""
        self._request_id = request_id
        label = Text()
        label.append("Approval required: ", style=f"bold {WARNING}")
        label.append(summary, style=f"bold {FG}")
        self.query_one("#perm-label", Static).update(label)
        self.query_one("#perm-detail", Static).update(detail)
        self.add_class("-active")

    def hide(self) -> None:
        self.remove_class("-active")
        self._request_id = ""

    @property
    def is_active(self) -> bool:
        return self.has_class("-active")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if not self._request_id:
            return
        decision_map = {
            "perm-allow": "allow",
            "perm-allow-session": "allow_session",
            "perm-deny": "deny",
        }
        decision = decision_map.get(event.button.id or "", "deny")
        request_id = self._request_id
        self.hide()
        self.post_message(self.Action(request_id, decision))
