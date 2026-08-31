"""What a span records about the request it traced.

`snapshot` is general: every wrapper hands a span payload the caller can still
edit. Only Bedrock uses it so far - anthropic and openai have the same aliasing
and are a separate change.
"""

from __future__ import annotations

import copy
import logging
from collections import ChainMap
from typing import Any, cast

from aigie._system_prompt import system_prompt_text

logger = logging.getLogger(__name__)

_MAX_DEPTH = 24
_CIRCULAR = "<circular reference>"
_ATOMIC = (str, bytes, int, float, complex, bool, type(None))

__all__ = ["publish_system_prompt", "snapshot"]


def snapshot(value: Any) -> Any:
    """A copy of a request or response the caller cannot edit out from under us.

    A finalized span is handed to `create_task`, so its payload is read after the
    caller has resumed - not at flush. In an async host that is the very next
    turn of the loop, which is exactly when a conversation loop appends the next
    message. Holding the caller's own objects lets those edits rewrite a request
    the provider has already answered.

    Deep, because a shallow copy still shares the message dicts.
    """
    try:
        return copy.deepcopy(value)
    except Exception as e:  # noqa: BLE001 - a request can carry anything
        logger.debug("[wrapper] Could not copy a provider payload whole: %s", e)
    try:
        return _copied_around(value, _MAX_DEPTH, {}, set(), [])
    except Exception as e:  # noqa: BLE001 - nor can we always copy it in parts
        logger.debug("[wrapper] Could not copy a provider payload in parts: %s", e)
        return value


def _copied_around(
    value: Any, depth: int, memo: dict[int, Any], active: set[int], kept: list[Any]
) -> Any:
    """Copy what can be copied, keeping only the parts that refused.

    One uncopyable leaf - a file handle, a lock, a client - must not cost the
    whole graph its protection, which returning the original outright would do.

    `memo` is not an optimisation: without it a shared subtree is re-walked once
    per reference, which on a wide graph is seconds of the caller's own CPU.
    `active` holds the ancestors currently being copied, so a back-reference
    becomes a marker rather than a cycle, which JSON cannot represent.

    `kept` holds originals against a container whose `__iter__` yields
    temporaries, whose ids would otherwise be free to be reused mid-walk.
    """
    marker = id(value)
    if marker in active:
        return _CIRCULAR
    if marker in memo:
        return memo[marker]

    # Identity, not `isinstance` and not `in`: a `str` subclass can carry a
    # mutable `__dict__`, and a class with an `__eq__` metaclass is unhashable.
    kind = type(value)
    if any(kind is atomic for atomic in _ATOMIC):
        return value

    kept.append(value)
    if not isinstance(value, (dict, list, tuple, set, frozenset)):
        return _copied_leaf(value, memo)
    if depth <= 0:
        logger.debug("[wrapper] Payload deeper than %s levels - not copied below", _MAX_DEPTH)
        return value

    active.add(marker)
    try:
        if isinstance(value, dict):
            out: Any = {
                key: _copied_around(item, depth - 1, memo, active, kept)
                for key, item in value.items()
            }
        else:
            out = _like(value, [_copied_around(i, depth - 1, memo, active, kept) for i in value])
    finally:
        active.discard(marker)
    memo[marker] = out
    return out


def _copied_leaf(value: Any, memo: dict[int, Any]) -> Any:
    """Copy one non-container, on its own memo.

    `deepcopy` registers a container before filling it, so a failure part-way
    through would otherwise publish a truncated copy to every later reference in
    our walk. The layer is a `ChainMap` rather than a copy: writes land in the
    throwaway map and reads still reach the shared one, so isolation costs O(1)
    instead of O(len(memo)) per leaf.
    """
    # `deepcopy` is annotated for a dict, but only ever does mapping operations
    # on the memo - all of which a ChainMap answers, including the keep-alive
    # list it stores under its own id.
    layer = cast("dict[int, Any]", ChainMap({}, memo))
    try:
        out = copy.deepcopy(value, layer)
    except Exception:  # noqa: BLE001 - this leaf is the one that refused
        return value
    # Only on success, and only into the shared memo: a leaf that hangs off
    # every message would otherwise be copied once per reference.
    memo[id(value)] = out
    return out


def _like(original: Any, items: list[Any]) -> Any:
    """Rebuild a sequence as its own kind, falling back to a builtin.

    A namedtuple is the one kind that takes its fields positionally, so it is
    the one kind spread - and it is spread first, because a one-field namedtuple
    *accepts* the list and binds it as the field, turning `One(5)` into
    `One(x=[5])` with nothing raised to notice. Spreading anything else would
    quietly rebuild it from the wrong elements.
    """
    if isinstance(original, list):
        return items
    kind = type(original)
    if hasattr(original, "_fields"):
        try:
            return kind(*items)
        except Exception as e:  # noqa: BLE001 - a subclass may take anything
            logger.debug("[wrapper] %s refused its fields spread: %s", kind.__name__, e)
    try:
        return kind(items)
    except Exception as e:  # noqa: BLE001 - nor an iterable
        logger.debug("[wrapper] %s refused an iterable: %s", kind.__name__, e)
    # The last resort must not raise either: escaping here would cost the whole
    # graph the protection this walk exists to give one leaf.
    try:
        if isinstance(original, tuple):
            return tuple(items)
        return frozenset(items) if isinstance(original, frozenset) else set(items)
    except Exception as e:  # noqa: BLE001 - an element may not survive as itself
        logger.debug("[wrapper] Could not rebuild a %s at all: %s", kind.__name__, e)
        return items


def publish_system_prompt(span_input: dict, value: Any) -> str | None:
    """Flatten a provider's system prompt onto the span input under one name.

    Providers state it three ways - a body key, a `system=` argument, a message
    with a system role - and the span view reads only `input.system_prompt`.
    """
    text = system_prompt_text(value)
    if text:
        span_input["system_prompt"] = text
    return text or None
