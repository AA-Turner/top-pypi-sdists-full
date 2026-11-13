"""The model's reasoning apart from its content (D4, F3): verl is token-in/token-out, so the reasoning span is found by
the model's own think tokens in that turn's ids (Qwen3 `</think>`, id 151668), never by a text regex. Content stays
as the loop built it, less that span."""

from __future__ import annotations

import logging
import threading
import weakref
from collections.abc import Sequence
from typing import Any

logger = logging.getLogger(__name__)

THINK_START = "<think>"
THINK_END = "</think>"
#: tokenizer -> (start id or None, end id) or None (no think-end token in its vocabulary); weak, so a new tokenizer
#: never reads a dead one's answer.
_THINK_IDS: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()
_LOCK = threading.Lock()


def get_think_ids(tokenizer: Any) -> tuple[int | None, int] | None:
    """The tokenizer's think-start and think-end token ids; None when it has no think-end token."""
    try:
        with _LOCK:
            if tokenizer in _THINK_IDS:
                return _THINK_IDS[tokenizer]
    except TypeError:  # not weakly referenceable or not hashable: asked each time
        pass
    found = _find_token(tokenizer, THINK_END)
    ids = None if found is None else (_find_token(tokenizer, THINK_START), found)
    try:
        with _LOCK:
            _THINK_IDS[tokenizer] = ids
    except TypeError:
        pass
    return ids


def has_think_token(tokenizer: Any) -> bool:
    return tokenizer is not None and get_think_ids(tokenizer) is not None


def split_reasoning(content: str, ids: Sequence[int], tokenizer: Any) -> tuple[str, str | None]:
    """(content without the reasoning span, the reasoning or None). The span runs from the turn's start (or its
    think-start token) through its think-end token; a turn cut inside its thinking (a think-start, no end) is all
    reasoning. No think token: no reasoning, the content as it was."""
    think = get_think_ids(tokenizer) if tokenizer is not None else None
    if think is None or not ids:
        return content, None
    start_id, end_id = think
    ids = [int(token) for token in ids]
    end = ids.index(end_id) if end_id in ids else None
    start = ids.index(start_id) if start_id is not None and start_id in ids[: end if end is not None else len(ids)] else None
    if end is None and start is None:
        return content, None
    span_end = end + 1 if end is not None else len(ids)
    reasoning = str(tokenizer.decode(ids[(start + 1 if start is not None else 0): end if end is not None else len(ids)]))
    reasoning = reasoning.strip()
    if not reasoning:
        return content, None
    prefix = str(tokenizer.decode(ids[:span_end]))
    if content.startswith(prefix):
        return content[len(prefix):], reasoning
    logger.debug("probe: a verl turn's content does not start with its decoded reasoning span; content kept whole")
    return content, reasoning


def _find_token(tokenizer: Any, token: str) -> int | None:
    try:
        found = tokenizer.convert_tokens_to_ids(token)
        if isinstance(found, list):
            found = found[0] if len(found) == 1 else None
        if not isinstance(found, int) or found < 0 or found == getattr(tokenizer, "unk_token_id", None):
            return None
        back = tokenizer.convert_ids_to_tokens(found)
        return found if (back[0] if isinstance(back, list) else back) == token else None
    except Exception:  # noqa: BLE001 -- a tokenizer that cannot say has no such token
        return None
