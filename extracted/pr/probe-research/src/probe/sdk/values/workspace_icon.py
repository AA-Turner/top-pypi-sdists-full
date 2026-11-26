"""The workspace icon rule the client checks before it sends: one emoji (twin: `_EMOJI_PATTERN` in
app/projects/workspaces/icon/icon.py; tests/unit/projects/workspaces/test_icon_rule_twin.py holds them equal)."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .. import errors

if TYPE_CHECKING:
    from ...generated.models import WorkspaceIconEdit

_EMOJI_BASE = "[©®‼⁉™\u2139〰〽㊗㊙\\u2190-\\u21ff\\u2300-\\u27ff\\u2900-\\u2bff\\U0001f000-\\U0001faff]"
_EMOJI_PART = _EMOJI_BASE + r"\ufe0f?[\U0001f3fb-\U0001f3ff]?"
#: One emoji: a flag, a keycap, a tag sequence, or parts joined by zero-width joiners.
EMOJI_PATTERN = re.compile(
    rf"(?:[\U0001f1e6-\U0001f1ff]{{2}}|[0-9#*]\ufe0f?\u20e3|"
    rf"\U0001f3f4[\U000e0061-\U000e007a]+\U000e007f|{_EMOJI_PART}(?:\u200d{_EMOJI_PART})*)"
)
#: The server's words for a refused emoji.
NOT_ONE_EMOJI = "Enter one emoji for the workspace icon."


def check_workspace_icon(icon: WorkspaceIconEdit) -> None:
    """Raise `ValidationError` unless `icon` is one emoji or one image, as the server would."""
    emoji = icon.emoji.root if icon.emoji is not None else None
    if (emoji is None) == (icon.image is None):
        raise errors.ValidationError("Choose one emoji or one image.")
    if emoji is not None and not EMOJI_PATTERN.fullmatch(emoji):
        raise errors.ValidationError(NOT_ONE_EMOJI)
