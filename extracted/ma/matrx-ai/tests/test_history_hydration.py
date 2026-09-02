"""The server-authoritative-history contract (matrx_ai.agents.history_hydration).

Guards the 2026-07-11 defect: a client sending only the NEW turn against an
existing conversation_id got no history and was stored as if it were turn 1.

Several cases below are adversarial-review findings against the FIRST draft of
this primitive, which inferred the client's shape by prefix-matching message text
and raised a 422 on divergence. They are pinned here because each one failed a
real user's turn over a heuristic about the past.
"""

from __future__ import annotations

import pytest

from matrx_ai.agents.history_hydration import hydrate_persisted_history
from matrx_ai.config.message_config import MessageList, UnifiedMessage


def _msg(role: str, text: str, *, id: str | None = None) -> UnifiedMessage:
    data: dict[str, object] = {"role": role, "content": text}
    if id:
        data["id"] = id
    return UnifiedMessage.from_dict(data)


class _Config:
    """Minimal stand-in for UnifiedConfig — hydration only touches .messages."""

    def __init__(self, messages: list[UnifiedMessage]) -> None:
        self.messages = MessageList(list(messages))


def _loader(persisted: list[UnifiedMessage]):
    async def load(conversation_id: str) -> list[UnifiedMessage]:
        return list(persisted)

    return load


def _texts(config: _Config) -> list[str]:
    return [f"{m.role}:{m.get_output()}" for m in config.messages]


PERSISTED = [
    _msg("user", "Say OK only.", id="m0"),
    _msg("assistant", "OK", id="m1"),
]


@pytest.mark.asyncio
async def test_delta_client_gets_history_prepended():
    """The delta shape — the whole point of the primitive."""
    config = _Config([_msg("user", "What did I just say?")])

    new_count = await hydrate_persisted_history(config, "c1", load=_loader(PERSISTED))

    assert new_count == 1
    assert _texts(config) == [
        "user:Say OK only.",
        "assistant:OK",
        "user:What did I just say?",
    ]


@pytest.mark.asyncio
async def test_new_turn_lands_after_the_whole_history():
    """The corruption guard: the new turn continues the conversation."""
    config = _Config([_msg("user", "third turn")])

    await hydrate_persisted_history(config, "c1", load=_loader(PERSISTED))

    assert len(config.messages) - 1 == 2  # index of the new user message


@pytest.mark.asyncio
async def test_repeating_the_opening_message_is_a_normal_turn_not_a_rewrite():
    """ADVERSARIAL: a user whose new message repeats the conversation's opening
    words ('continue', 'ok', 'hi', a reused prompt template). The first draft
    read the accidental text match as a truncated replay and 422'd the turn."""
    config = _Config([_msg("user", "Say OK only.")])

    new_count = await hydrate_persisted_history(config, "c1", load=_loader(PERSISTED))

    assert new_count == 1
    assert _texts(config) == ["user:Say OK only.", "assistant:OK", "user:Say OK only."]


@pytest.mark.asyncio
async def test_full_history_replay_is_deduplicated_not_doubled():
    config = _Config([*PERSISTED, _msg("user", "next")])

    new_count = await hydrate_persisted_history(config, "c1", load=_loader(PERSISTED))

    assert new_count == 1
    assert _texts(config) == ["user:Say OK only.", "assistant:OK", "user:next"]


@pytest.mark.asyncio
async def test_replay_is_dropped_by_cx_message_id_even_when_text_differs():
    """ADVERSARIAL: the loader returns the MODEL-visible rebuild (tool blocks
    re-serialized, hidden rows dropped), which never text-matches a client's own
    view of the same conversation. The id is the exact signal."""
    config = _Config(
        [
            _msg("user", "Say OK only.", id="m0"),
            _msg("assistant", "OK (as rendered by the client)", id="m1"),
            _msg("user", "next"),
        ]
    )

    new_count = await hydrate_persisted_history(config, "c1", load=_loader(PERSISTED))

    assert new_count == 1
    assert _texts(config) == ["user:Say OK only.", "assistant:OK", "user:next"]


@pytest.mark.asyncio
async def test_a_client_turn_is_never_rejected():
    """ADVERSARIAL: a divergent/rewritten past must not kill the user's turn.
    The DB wins (the edit is ignored + logged); the new turn still runs."""
    config = _Config(
        [
            _msg("user", "Say OK only."),
            _msg("assistant", "TAMPERED"),
            _msg("user", "next"),
        ]
    )

    new_count = await hydrate_persisted_history(config, "c1", load=_loader(PERSISTED))

    assert new_count == 1
    assert _texts(config) == ["user:Say OK only.", "assistant:OK", "user:next"]


@pytest.mark.asyncio
async def test_no_persisted_history_is_a_noop():
    """A brand-new / ephemeral conversation: the client's list IS the history."""
    config = _Config([_msg("user", "first")])

    new_count = await hydrate_persisted_history(config, "c1", load=_loader([]))

    assert new_count == 1
    assert _texts(config) == ["user:first"]
