"""Splitting the system block so a per-request tail stops costing the whole prefix.

agno appends additional_context to the tail of the system message, and both cache
wrappers put a single breakpoint after the whole block. Prompt caching matches an
exact prefix, so an agent whose context changes between turns (the gateway, every
turn) missed on system and on every message downstream of it. These tests pin the
split, and above all that it is behaviourally inert: the concatenated prompt text
is byte-identical with and without it.
"""

from __future__ import annotations

import pytest

from xpander_sdk.modules.backend.frameworks._anthropic_cache import (
    _CACHE_CONTROL,
    _inject_system_split,
)
from xpander_sdk.modules.backend.frameworks._bedrock_cache import (
    _CACHE_POINT,
    _split_system_blocks,
)
from xpander_sdk.modules.backend.frameworks._cache_split import (
    MIN_STABLE_CHARS,
    MIN_VOLATILE_CHARS,
    split_system_text,
)

_STABLE = "S" * 10_000
_VOLATILE = "<context>" + "V" * 2_000 + "</context>"
_SYSTEM = _STABLE + _VOLATILE


def _bedrock_text(blocks) -> str:
    return "".join(b["text"] for b in blocks if isinstance(b, dict) and "text" in b)


# ---- split point ------------------------------------------------------ #


def test_splits_at_the_start_of_the_volatile_tail():
    stable, tail = split_system_text(_SYSTEM, _VOLATILE)
    assert stable == _STABLE
    assert tail == _VOLATILE


def test_split_is_lossless():
    stable, tail = split_system_text(_SYSTEM, _VOLATILE)
    assert stable + tail == _SYSTEM


def test_volatile_is_matched_after_stripping():
    stable, tail = split_system_text(_SYSTEM, f"\n  {_VOLATILE}  \n")
    assert stable + tail == _SYSTEM


@pytest.mark.parametrize(
    "text,volatile",
    [
        (None, _VOLATILE),
        ("", _VOLATILE),
        (_SYSTEM, None),
        (_SYSTEM, ""),
        (_STABLE, _VOLATILE),  # tail absent from the system text
        (_VOLATILE, _VOLATILE),  # the whole message is volatile
        ("S" * 100 + _VOLATILE, _VOLATILE),  # stable half too small to cache
        (_STABLE + "tiny", "tiny"),  # tail too small to be worth a breakpoint
    ],
)
def test_no_split_falls_back(text, volatile):
    assert split_system_text(text, volatile) is None


def test_thresholds_are_the_documented_floors():
    assert MIN_STABLE_CHARS >= 4_000
    assert MIN_VOLATILE_CHARS >= 100


# ---- bedrock ---------------------------------------------------------- #


def test_bedrock_inserts_a_cachepoint_between_the_halves():
    out = _split_system_blocks([{"text": _SYSTEM}], _VOLATILE)
    assert len(out) == 3
    assert out[0] == {"text": _STABLE}
    assert out[1] == _CACHE_POINT
    assert out[2] == {"text": _VOLATILE}


def test_bedrock_split_is_byte_identical():
    out = _split_system_blocks([{"text": _SYSTEM}], _VOLATILE)
    assert _bedrock_text(out) == _SYSTEM


def test_bedrock_returns_blocks_untouched_when_nothing_to_split():
    blocks = [{"text": _SYSTEM}]
    assert _split_system_blocks(blocks, None) is blocks
    assert _split_system_blocks(blocks, "not present in the text") is blocks


def test_bedrock_tolerates_odd_block_shapes():
    blocks = ["junk", {"notext": 1}, {"text": _SYSTEM}]
    out = _split_system_blocks(blocks, _VOLATILE)
    assert _bedrock_text(out) == _SYSTEM
    assert _CACHE_POINT in out


def test_bedrock_empty_blocks_are_safe():
    assert _split_system_blocks([], _VOLATILE) == []


# ---- anthropic -------------------------------------------------------- #


def _anthropic_kwargs():
    return {
        "system": [
            {"type": "text", "text": _SYSTEM, "cache_control": dict(_CACHE_CONTROL)}
        ]
    }


def test_anthropic_splits_into_two_cached_blocks():
    kwargs = _anthropic_kwargs()
    _inject_system_split(kwargs, _VOLATILE)
    system = kwargs["system"]
    assert len(system) == 2
    assert system[0]["text"] == _STABLE
    assert system[1]["text"] == _VOLATILE
    # The tail keeps its breakpoint so one arun's tool-call turns still cache the
    # full system block; that is the ceiling of four, counting tools + last message.
    assert "cache_control" in system[0]
    assert "cache_control" in system[1]


def test_anthropic_split_is_byte_identical():
    kwargs = _anthropic_kwargs()
    _inject_system_split(kwargs, _VOLATILE)
    assert "".join(b["text"] for b in kwargs["system"]) == _SYSTEM


def test_anthropic_leaves_the_block_alone_when_nothing_to_split():
    kwargs = _anthropic_kwargs()
    _inject_system_split(kwargs, None)
    assert len(kwargs["system"]) == 1
    assert kwargs["system"][0]["text"] == _SYSTEM


@pytest.mark.parametrize("system", [None, "a string, not a list", []])
def test_anthropic_tolerates_odd_system_shapes(system):
    kwargs = {"system": system} if system is not None else {}
    _inject_system_split(kwargs, _VOLATILE)


# ---- wrapper wiring ---------------------------------------------------- #


def test_wrappers_default_to_no_volatile_hint():
    from xpander_sdk.modules.backend.frameworks._anthropic_cache import CachingClaude
    from xpander_sdk.modules.backend.frameworks._bedrock_cache import CachingAwsBedrock

    assert CachingAwsBedrock.xp_volatile_system is None
    assert CachingClaude.xp_volatile_system is None


# ---- per-request override ---------------------------------------------- #


def test_context_var_overrides_the_instance_attribute():
    """A shared model instance must not leak one conversation's tail into another."""
    from xpander_sdk.modules.backend.frameworks._cache_split import (
        current_volatile_system,
        resolve_volatile,
    )

    token = current_volatile_system.set("per-request tail")
    try:
        assert resolve_volatile("instance attribute") == "per-request tail"
    finally:
        current_volatile_system.reset(token)


def test_falls_back_to_the_instance_attribute():
    from xpander_sdk.modules.backend.frameworks._cache_split import resolve_volatile

    assert resolve_volatile("instance attribute") == "instance attribute"
    assert resolve_volatile(None) is None


@pytest.mark.asyncio
async def test_context_var_does_not_leak_between_concurrent_runs():
    import asyncio

    from xpander_sdk.modules.backend.frameworks._cache_split import (
        current_volatile_system,
        resolve_volatile,
    )

    async def run(tail: str) -> str:
        current_volatile_system.set(tail)
        await asyncio.sleep(0)
        return resolve_volatile(None)

    seen = await asyncio.gather(run("conversation-a"), run("conversation-b"))
    assert seen == ["conversation-a", "conversation-b"]
