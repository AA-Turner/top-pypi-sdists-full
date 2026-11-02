"""THE CONTROL-TOKEN FILTER — a declared machine line never reaches the wire.

Forcing function, not decoration: every assertion here reads the REAL NDJSON the
emitter put on its outbound queue, character by character, after feeding it the
same split deltas a provider streams. Delete the filter from
``StreamEmitter.send_chunk`` and these fail; break the value routing and they
fail; leave a stripped line in the persisted turn text and they fail.

The incident: ``WRAP_RATING: 4`` printed into a person's own vision interview
(wall W9 tail, 2026-09-15).
"""

from __future__ import annotations

import asyncio

import orjson
import pytest

from matrx_connect.context.events import (
    PAYLOAD_REGISTRY,
    VALID_EVENT_TYPES,
    ControlTokenPayload,
    EventType,
)
from matrx_connect.emitters.control_tokens import (
    ControlTokenFilter,
    ControlTokenRegistry,
    ControlTokenSpec,
    strip_control_tokens,
)
from matrx_connect.emitters.stream_emitter import StreamEmitter

WRAP_RATING = ControlTokenSpec(
    name="WRAP_RATING",
    declared_by="vision_interview room primary role (DB system prompt)",
    purpose="the primary voice's 1-5 self-rating of how ready this stage is to wrap",
    value_pattern=r"[1-5]",
)


@pytest.fixture()
def registry() -> ControlTokenRegistry:
    reg = ControlTokenRegistry()
    reg.register(WRAP_RATING)
    return reg


# ---------------------------------------------------------------------------
# Helpers — read the actual wire, never the emitter's internals
# ---------------------------------------------------------------------------


def _drain(emitter: StreamEmitter) -> list[dict]:
    frames: list[dict] = []
    while not emitter.queue.empty():
        item = emitter.queue.get_nowait()
        if item is None:
            continue
        raw = item if isinstance(item, bytes) else item.encode()
        for line in raw.splitlines():
            if line.strip():
                frames.append(orjson.loads(line))
    return frames


def _visible_text(frames: list[dict]) -> str:
    return "".join(f["t"] for f in frames if f.get("e") == "c")


def _control_events(frames: list[dict]) -> list[dict]:
    return [f["data"] for f in frames if f.get("event") == EventType.CONTROL_TOKEN.value]


async def _stream(deltas: list[str], registry: ControlTokenRegistry) -> list[dict]:
    emitter = StreamEmitter()
    emitter._control_filter = ControlTokenFilter(registry=registry)
    for delta in deltas:
        await emitter.send_chunk(delta)
    await emitter.send_end()
    return _drain(emitter)


# ---------------------------------------------------------------------------
# The event exists and is typed
# ---------------------------------------------------------------------------


def test_control_token_event_is_registered():
    assert "control_token" in VALID_EVENT_TYPES
    assert PAYLOAD_REGISTRY[EventType.CONTROL_TOKEN] is ControlTokenPayload


def test_control_token_payload_forbids_extras():
    with pytest.raises(Exception):
        ControlTokenPayload(name="WRAP_RATING", value="4", surprise=True)


# ---------------------------------------------------------------------------
# THE FORCING TEST — a token-bearing delta stream
# ---------------------------------------------------------------------------


def test_token_bearing_stream_is_clean_and_the_value_is_carried(registry):
    """The exact shape of the incident: a role's answer ending in its rating."""
    frames = asyncio.run(
        _stream(
            [
                "That is a strong start. ",
                "Tell me about the first customer.\n",
                "WRAP_RATING: 4\n",
            ],
            registry,
        )
    )

    visible = _visible_text(frames)
    assert "WRAP_RATING" not in visible
    assert "4" not in visible.replace("first customer", "")
    assert visible == "That is a strong start. Tell me about the first customer.\n"

    events = _control_events(frames)
    assert events == [
        {
            "name": "WRAP_RATING",
            "value": "4",
            "declared_by": WRAP_RATING.declared_by,
        }
    ]


def test_a_token_split_across_deltas_still_never_reaches_the_wire(registry):
    """Providers do not respect line boundaries. Neither may the filter."""
    frames = asyncio.run(
        _stream(["Here is the question.\n", "WRAP", "_RA", "TING", ": ", "2", "\n"], registry)
    )

    visible = _visible_text(frames)
    assert visible == "Here is the question.\n"
    assert "WRAP" not in visible
    assert [e["value"] for e in _control_events(frames)] == ["2"]


def test_a_token_on_the_last_line_with_no_newline_is_still_stripped(registry):
    """A model that ends its turn on the control line, mid-line, at EOF."""
    frames = asyncio.run(_stream(["All set.\n", "WRAP_RATING: 5"], registry))

    assert _visible_text(frames) == "All set.\n"
    assert [e["value"] for e in _control_events(frames)] == ["5"]


def test_held_text_that_was_not_a_token_is_released_verbatim(registry):
    """Nothing is ever dropped: a line that merely LOOKED like a token is text."""
    frames = asyncio.run(_stream(["WRAP", "PED in paper, not a token"], registry))

    assert _visible_text(frames) == "WRAPPED in paper, not a token"
    assert _control_events(frames) == []


def test_prose_mentioning_the_token_is_untouched(registry):
    text = "I would rate this a WRAP_RATING of sorts, but let us keep going.\n"
    frames = asyncio.run(_stream([text], registry))

    assert _visible_text(frames) == text
    assert _control_events(frames) == []


def test_an_out_of_contract_value_is_left_alone(registry):
    """The value shape is part of the declaration: ``WRAP_RATING: 9`` is prose."""
    frames = asyncio.run(_stream(["WRAP_RATING: 9\n"], registry))

    assert _visible_text(frames) == "WRAP_RATING: 9\n"
    assert _control_events(frames) == []


def test_ordinary_prose_is_never_delayed(registry):
    """The filter must not buffer normal text waiting for a newline."""
    emitter = StreamEmitter()
    emitter._control_filter = ControlTokenFilter(registry=registry)

    async def _run() -> str:
        await emitter.send_chunk("Once upon a time there was a very long sentence")
        await emitter._flush_text()
        return _visible_text(_drain(emitter))

    assert asyncio.run(_run()) == "Once upon a time there was a very long sentence"


USED = ControlTokenSpec(
    name="USED",
    declared_by="rag_kinds grounded synthesis (aidream/services/rag_kinds/service.py)",
    purpose="the chunk_ids the answer actually drew a fact from",
)


def _live_text(deltas: list[str], registry: ControlTokenRegistry) -> str:
    """What the client has on screen after every delta — BEFORE the stream ends."""
    emitter = StreamEmitter()
    emitter._control_filter = ControlTokenFilter(registry=registry)

    async def _run() -> str:
        for delta in deltas:
            await emitter.send_chunk(delta)
        await emitter._flush_text()
        return _visible_text(_drain(emitter))

    return asyncio.run(_run())


def test_a_mid_line_delta_that_starts_like_a_token_is_never_held():
    """THE 2026-09-24 INCIDENT (conversation 1891df9d…).

    A structured-output answer is ONE long line of JSON. The provider split
    "overused" as ``" over"`` + ``"used classics…"``; the filter judged the
    second delta as if it began a line, saw the ``USED`` prefix, and held every
    byte after it until END — after ``completion`` and the directive receipt —
    so the client rendered a truncated directive plus a stray markdown tail.
    A delta that continues a line whose start already reached the wire can
    never be a control line.
    """
    reg = ControlTokenRegistry()
    reg.register(USED)
    reg.register(WRAP_RATING)
    deltas = [
        '{"__kind":"directive_v1_action_create_agent_definition","items":[{"text":"Avoid',
        " over",
        'used classics. Wr',
        'ap it up.\\n- More"}]}',
    ]
    assert _live_text(deltas, reg) == "".join(deltas)


def test_line_start_prose_that_only_shares_a_token_word_is_released_early():
    """``USED`` needs ``USED:`` — "Used cars" can never become the token, so it
    must not wait for a newline that a one-line answer never sends."""
    reg = ControlTokenRegistry()
    reg.register(USED)
    assert _live_text(["Used", " cars are cheaper"], reg) == "Used cars are cheaper"


def test_a_real_token_is_still_held_across_deltas_at_line_start():
    reg = ControlTokenRegistry()
    reg.register(USED)
    assert _live_text(["Answer.\n", "USED", ": c1, c2"], reg) == "Answer.\n"


def test_a_new_model_call_starts_a_new_line(registry):
    """A call that ended mid-line must not make the NEXT call's control line a
    "continuation" — ``reset_turn_text`` is the turn boundary."""
    emitter = StreamEmitter()
    emitter._control_filter = ControlTokenFilter(registry=registry)

    async def _run() -> str:
        await emitter.send_chunk("Let me check that.")
        emitter.reset_turn_text()
        await emitter.send_chunk("WRAP_RATING: 4\n")
        await emitter.send_end()
        return _visible_text(_drain(emitter))

    assert asyncio.run(_run()) == "Let me check that."


@pytest.mark.parametrize("brk", [" ", " ", "\x0b", "\x0c", "\x85", "\r"])
def test_every_splitlines_break_ends_a_line(brk):
    reg = ControlTokenRegistry()
    reg.register(USED)
    assert _live_text([f"Intro.{brk}", "USED: c1\n"], reg) == f"Intro.{brk}"


def test_the_persisted_turn_text_is_clean_too(registry):
    """``get_turn_text`` persists an interrupted turn — it must not carry the line."""
    emitter = StreamEmitter()
    emitter._control_filter = ControlTokenFilter(registry=registry)

    async def _run() -> str:
        await emitter.send_chunk("The answer.\nWRAP_RATING: 3\n")
        return emitter.get_turn_text()

    assert asyncio.run(_run()) == "The answer.\n"


def test_the_snapshot_defence_still_fires_under_filtering(registry):
    """The snapshot check compares against RAW provider text, not cleaned text.

    A cumulative provider repeats the control line it already sent; comparing
    against the stripped text would miss the repeat and replay the whole turn.
    """
    emitter = StreamEmitter()
    emitter._control_filter = ControlTokenFilter(registry=registry)

    async def _run() -> list[dict]:
        await emitter.send_chunk("Hello there.\nWRAP_RATING: 1\n")
        # A snapshot provider re-sends everything plus the new text.
        await emitter.send_chunk("Hello there.\nWRAP_RATING: 1\nAnd more.")
        await emitter.send_end()
        return _drain(emitter)

    frames = asyncio.run(_run())
    assert emitter.provider_sent_snapshots is True
    assert _visible_text(frames) == "Hello there.\nAnd more."
    assert [e["value"] for e in _control_events(frames)] == ["1"]


# ---------------------------------------------------------------------------
# The knob
# ---------------------------------------------------------------------------


def test_the_per_mandate_knob_turns_filtering_off(registry):
    registry.set_mandate_filtering("bench.a2_loop", False)
    emitter = StreamEmitter()
    emitter._control_filter = ControlTokenFilter(registry=registry)
    emitter.configure_control_tokens(mandate_key="bench.a2_loop")

    async def _run() -> list[dict]:
        await emitter.send_chunk("line\nWRAP_RATING: 4\n")
        await emitter.send_end()
        return _drain(emitter)

    frames = asyncio.run(_run())
    assert "WRAP_RATING: 4" in _visible_text(frames)
    assert _control_events(frames) == []


def test_a_spec_declared_unfiltered_is_known_but_left_in_the_text():
    reg = ControlTokenRegistry()
    reg.register(
        ControlTokenSpec(
            name="SEARCH",
            declared_by="masterworks bench A2 research loop",
            purpose="the arm's next query",
            filter_enabled=False,
        )
    )
    assert reg.names() == ("SEARCH",)
    assert reg.active_specs() == ()

    filtered = ControlTokenFilter(registry=reg).feed("SEARCH: how does it work\n")
    assert filtered.text == "SEARCH: how does it work\n"
    assert filtered.hits == ()


def test_two_matchers_for_one_token_are_refused():
    reg = ControlTokenRegistry()
    reg.register(WRAP_RATING)
    reg.register(WRAP_RATING)  # identical re-registration is a no-op
    with pytest.raises(ValueError, match="already declared"):
        reg.register(
            ControlTokenSpec(
                name="WRAP_RATING",
                declared_by="somebody else",
                purpose="a second opinion",
                value_pattern=r"\d+",
            )
        )


def test_a_token_must_name_the_mandate_that_emits_it():
    with pytest.raises(ValueError, match="must name the mandate"):
        ControlTokenSpec(name="ORPHAN", declared_by="", purpose="nobody owns me")


# ---------------------------------------------------------------------------
# The whole-text stripper (non-streaming consumers)
# ---------------------------------------------------------------------------


def test_whole_text_stripper_matches_the_streaming_filter():
    reg = ControlTokenRegistry()
    reg.register(WRAP_RATING)
    result = strip_control_tokens(
        "Answer body.\nWRAP_RATING: 4\ntrailing line\n", registry=reg
    )
    assert result.text == "Answer body.\ntrailing line\n"
    assert [(h.name, h.value) for h in result.hits] == [("WRAP_RATING", "4")]


def test_a_bare_protocol_word_is_matched_only_on_its_own_line():
    reg = ControlTokenRegistry()
    reg.register(
        ControlTokenSpec(
            name="FINAL",
            declared_by="masterworks bench A2 research loop",
            purpose="the arm declaring its finished deliverable follows",
            bare=True,
        )
    )
    result = strip_control_tokens("thinking\nFINAL\nthe deliverable\n", registry=reg)
    assert result.text == "thinking\nthe deliverable\n"
    assert [h.name for h in result.hits] == ["FINAL"]

    untouched = strip_control_tokens("this is my FINAL answer\n", registry=reg)
    assert untouched.text == "this is my FINAL answer\n"
    assert untouched.hits == ()
