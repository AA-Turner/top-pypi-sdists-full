"""render_server_message: the server's sentence first and unchanged, then one line saying what to do
(its `Action`) in the words each surface uses, left out when the sentence already says it."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from probe.foundation.request_identity.surface import Surface

from .server_messages import Action, ServerMessage

#: How a script's own environment updates the SDK.
UPGRADE_COMMAND = "pip install -U probe-research"
#: How the CLI and its MCP server update (`probe.sdk.session_marker.WIZARD_HINT`; a test pins the two).
WIZARD_HINT = "run the Probe wizard: probe wizard or npx probe-research"
#: Where a person writes to Probe.
SUPPORT_ADDRESS = "support@prbe.ai"


@dataclass(frozen=True)
class ActionLine:
    """One action's line: its words per surface (`{target}` is the release to reach), and the
    phrases that show the server's sentence already says it."""

    words: Mapping[Surface, str]
    said_by: tuple[str, ...]

    def render(self, message: ServerMessage, surface: Surface) -> str | None:
        if any(phrase in message.text for phrase in self.said_by):
            return None
        target = f"probe-research {message.min_version} or later" if message.min_version else "a newer probe-research"
        return self.words[surface].format(target=target)


def _make_same_words(text: str) -> Mapping[Surface, str]:
    return {surface: text for surface in Surface}


#: Every action that has a line; `Action.NONE` has none.
ACTION_LINES: Mapping[Action, ActionLine] = {
    Action.UPDATE: ActionLine(
        words={Surface.SDK: f"Upgrade to {{target}}: `{UPGRADE_COMMAND}`.",
               Surface.CLI: f"Upgrade to {{target}}: {WIZARD_HINT}.",
               Surface.MCP: f"Upgrade to {{target}}: {WIZARD_HINT}."},
        said_by=("pip install", "probe wizard", "npx probe-research"),
    ),
    Action.REINSTALL: ActionLine(_make_same_words("Reinstall Probe: `npx probe-research`."), said_by=("npx probe-research",)),
    Action.CONTACT_SUPPORT: ActionLine(_make_same_words(f"Write to {SUPPORT_ADDRESS}."), said_by=(SUPPORT_ADDRESS,)),
}


def render_server_message(message: ServerMessage, surface: Surface = Surface.SDK) -> str:
    """The sentence, then its action line on a line of its own when it has one."""
    line = ACTION_LINES[message.action].render(message, surface) if message.action in ACTION_LINES else None
    text = message.text.rstrip()
    if line is None:
        return text
    return f"{text}\n{line}" if text else line
