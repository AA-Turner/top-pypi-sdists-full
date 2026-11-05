"""A proxied hook event's answer as actions (`hooks.run` v2, `reply: "actions"`): what pi's extension does with it.

Twin: `plugins/probe-research-pi/src/serviceActions.ts` (one fixture set, `tests/fixtures/hook_actions.json`,
drives both). pi has no hooks, so its extension asks the service for each event and applies these through
pi's own API; a kind the extension does not know is ignored and logged, never an error.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .env import HOOK_REPLY_ACTIONS as REPLY_ACTIONS  # noqa: F401 -- v2's `reply`, read here with the actions


class HookAction(str, Enum):
    """One thing the extension does with an event's answer."""

    #: Append `text` to this turn's system prompt.
    SYSTEM_PROMPT = "system_prompt"
    #: Keep `text` for the session: appended to every later turn's system prompt (session-start context).
    CONTEXT = "context"
    #: This turn's message to the model (`text`, not shown to the person).
    MESSAGE = "message"
    #: The typed line: `action` continue, or transform to `text`.
    INPUT = "input"
    #: Refuse the tool call, with `text` as the reason.
    BLOCK = "block"
    #: Keep the agent going: one more entry (`text`, shown) and continue.
    CONTINUE = "continue"
    #: Tell the person `text` at `level`.
    NOTIFY = "notify"
    #: Set the footer item `key` to `text` (None clears it).
    STATUS = "status"
    #: Ack delivery `receipt` once the extension applied this answer (`hooks.ack`).
    RECEIPT = "receipt"


class InputAction(str, Enum):
    """`HookAction.INPUT`'s `action` (pi's own `InputEventResult` words)."""

    CONTINUE = "continue"
    TRANSFORM = "transform"


class NotifyLevel(str, Enum):
    """`HookAction.NOTIFY`'s `level` (pi's `ui.notify` levels)."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True)
class ReplyAction:
    """One action of an answer; `to_dict` is its wire shape (`{"kind": ..., ...}`, fields left out when unset)."""

    kind: HookAction
    text: str | None = None
    level: NotifyLevel | None = None
    key: str | None = None
    action: InputAction | None = None
    receipt: str | None = None

    def to_dict(self) -> dict:
        out: dict = {"kind": self.kind.value}
        for name in ("text", "key", "receipt"):
            value = getattr(self, name)
            if value is not None:
                out[name] = value
        if self.level is not None:
            out["level"] = self.level.value
        if self.action is not None:
            out["action"] = self.action.value
        return out
