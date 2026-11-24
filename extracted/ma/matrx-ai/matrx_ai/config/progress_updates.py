"""Progress updates: reply text a provider delivers inside a reasoning-shaped block.

Recent Claude models return the text they write between tool calls ("what I found, what I'll do next" — and, for
an advisor, the advice it writes before asking its questions) as a ``thinking`` block whose signature labels it
``narration``, not as a ``text`` block. It is the model's words to the person, so the platform reads it as REPLY
TEXT: ``UnifiedMessage.from_anthropic_content`` makes it a ``TextContent``, the Anthropic stream sends it as
visible text, and every reader (the chat, the advice-first guard, titles, summaries) sees it as text.

The provider still owns the block: on replay it must come back exactly as it was sent (preserved thinking binds a
conversation to the blocks it produced). The ``TextContent`` therefore carries the original block under
``metadata[REPLAY_AS_KEY]`` and ``TextContent.to_anthropic`` sends that block back unchanged.

How a block is recognized: the signature is a base64 envelope whose first bytes name the block's kind
(``thinking`` for reasoning, ``narration`` for a progress update). Under ``display: "updates"`` the provider's
documented rule is "a thinking block with text is a progress update"; under ``"summarized"`` (what this platform
sends so people can read the thought process) both kinds carry text, and the label is the only signal. If the
label ever disappears, blocks fall back to reasoning — the old behaviour — and the advice-first guard in Agent
Understanding is the second layer that still notices a turn with no visible text.
"""

from __future__ import annotations

import base64
import binascii
from typing import Any

#: ``TextContent.metadata`` key: the provider block this text arrived as, replayed verbatim to that provider.
REPLAY_AS_KEY = "replay_as"

# The kind label inside the signature envelope: protobuf field 8, length 9, "narration".
_NARRATION_LABEL = b"\x42\x09narration"
# The label sits in the envelope's first bytes; 64 base64 characters decode to 48 bytes.
_HEAD_CHARS = 64


def is_progress_update_signature(signature: Any) -> bool:
    """Whether an Anthropic thinking-block signature labels the block a progress update (``narration``)."""
    if not isinstance(signature, str) or len(signature) < _HEAD_CHARS:
        return False
    try:
        head = base64.b64decode(signature[:_HEAD_CHARS], validate=True)
    except (binascii.Error, ValueError):
        return False
    return _NARRATION_LABEL in head


def anthropic_replay_block(text: str, signature: str) -> dict[str, Any]:
    """The ``metadata[REPLAY_AS_KEY]`` value for an Anthropic progress-update block (its exact wire form)."""
    return {"provider": "anthropic", "type": "thinking", "thinking": text, "signature": signature}


__all__ = ["REPLAY_AS_KEY", "anthropic_replay_block", "is_progress_update_signature"]
