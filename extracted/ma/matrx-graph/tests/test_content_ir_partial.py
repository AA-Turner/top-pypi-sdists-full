"""The streaming partial-kinds primitive — closer + the three-event contract.

Forcing-function posture: every closer case asserts the output is REAL valid
JSON by parsing it, and asserts the recovered value, so a closer that emits
syntactically-valid nonsense fails here rather than in a renderer.
"""

from __future__ import annotations

import json

import pytest
from matrx_graph.content_ir.envelope import IR_VERSION, KIND_KEY
from matrx_graph.content_ir.partial import (
    IR_PARTIAL_KEY,
    PARTIAL_STATES,
    PartialKindTracker,
    close_partial_json,
    parse_partial_json,
    partial_kind_event,
    read_partial_event,
    retracted_event,
    superseded_event,
)

DISCRIMINATOR = {"format": "fence", "language": "quiz"}


# ---------------------------------------------------------------------------
# The closer
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        # Empty and freshly-opened containers close to empty ones.
        ("{", {}),
        ("[", []),
        ('{"a"', {}),  # a bare KEY is never invented into a field
        ('{"a":', {}),  # dangling colon
        ('{"a": 1,', {"a": 1}),  # trailing comma dropped
        ('{"a": 1, "b', {"a": 1}),  # next key not yet a field
        # A number at the buffer edge may still grow — dropped, never guessed.
        ('{"a": 1', {}),
        ('{"a": 1.', {}),
        ('{"a": tru', {}),
        # The three keywords cannot extend, so they survive the edge.
        ('{"a": true', {"a": True}),
        ('{"a": null', {"a": None}),
        # An open string VALUE renders progressively (the whole point).
        ('{"a": "hel', {"a": "hel"}),
        ('{"a":"', {"a": ""}),
        ('{"a":"line1\\nline', {"a": "line1\nline"}),
        # Cuts never land mid-escape or mid-\uXXXX.
        ('{"a":"x\\', {"a": "x"}),
        ('{"a":"x\\u26', {"a": "x"}),
        ('{"a":"x\\u2665', {"a": "x♥"}),
        # Nesting: the deepest still-closeable point wins.
        ('[1, 2, {"x": "incompl', [1, 2, {"x": "incompl"}]),
        ('{"a": [1,2],"b":{"c":', {"a": [1, 2], "b": {}}),
        # Already-complete documents round-trip untouched.
        ('{"a": true}', {"a": True}),
        ("[]", []),
    ],
)
def test_closer_produces_valid_json_with_the_expected_value(raw, expected):
    closed = close_partial_json(raw)
    assert closed is not None, f"closer refused {raw!r}"
    assert json.loads(closed) == expected
    assert parse_partial_json(raw) == expected


@pytest.mark.parametrize("raw", ["", "not json", "   ", "}", "]", ":"])
def test_closer_refuses_what_it_cannot_make_valid(raw):
    """The loud posture: no partial beats an unparseable one."""
    assert close_partial_json(raw) is None


def test_open_string_can_be_excluded_for_a_stricter_caller():
    assert json.loads(close_partial_json('{"a": "hel', include_open_string=False)) == {}


def test_a_key_is_never_rendered_as_a_string_value():
    """An unterminated KEY invents a field name — it must be dropped."""
    assert json.loads(close_partial_json('{"a": 1, "bb')) == {"a": 1}


def test_every_prefix_of_a_real_document_closes_validly():
    """The property that matters on a live stream: EVERY prefix is parseable.

    A closer that works on hand-picked cases and fails on token boundary 47 is
    a closer that breaks in production, so this walks all of them.
    """
    doc = json.dumps(
        {
            "title": 'A "quoted" quiz',
            "questions": [
                {"q": "Why?", "options": ["a", "b"], "answer": 1, "ok": True},
                {"q": "How ♥?", "options": [], "answer": None},
            ],
            "meta": {"n": 2, "tags": ["x"]},
        }
    )
    produced = 0
    for i in range(1, len(doc) + 1):
        closed = close_partial_json(doc[:i])
        if closed is None:
            continue
        produced += 1
        json.loads(closed)  # raises if the closer ever emits invalid JSON
    assert produced > len(doc) // 2, "closer refused most prefixes — not usable live"
    assert json.loads(close_partial_json(doc)) == json.loads(doc)


def test_partial_values_only_ever_grow_toward_the_truth():
    """No prefix may assert a value the finished document contradicts.

    This is the contract that lets a client render a partial without lying:
    a scalar that appears may still GROW (a string gains characters), but it
    may never flip to a different completed value.
    """
    doc = '{"a": "hello", "b": 12, "c": [1, 2]}'
    final = json.loads(doc)
    for i in range(1, len(doc) + 1):
        closed = close_partial_json(doc[:i])
        if closed is None:
            continue
        value = json.loads(closed)
        for key, seen in value.items():
            truth = final[key]
            if isinstance(seen, str) and isinstance(truth, str):
                assert truth.startswith(seen), f"{seen!r} is not a prefix of {truth!r}"
            elif isinstance(seen, list) and isinstance(truth, list):
                assert seen == truth[: len(seen)]
            else:
                assert seen == truth, f"{key}: partial {seen!r} contradicts {truth!r}"


# ---------------------------------------------------------------------------
# The three events
# ---------------------------------------------------------------------------


def test_partial_event_is_a_self_describing_kind_instance_marked_provisional():
    event = partial_kind_event(
        kind="quiz",
        value={"questions": []},
        seq=1,
        source_text='{"questions": []',
        discriminator=DISCRIMINATOR,
        truncated=True,
    )
    assert event["state"] == "partial"
    assert event["v"] == IR_VERSION
    # The payload says what it is, exactly like a finished instance.
    assert event["root"]["value"][KIND_KEY] == "quiz"
    # Pre-recognition, in the frontend's own IR vocabulary.
    assert event["root"]["kindState"] == "speculative"
    assert event["root"]["status"] == "streaming"
    codes = {n["code"] for n in event["root"]["residue"]["notices"]}
    assert "partial_unvalidated" in codes
    assert "partial_truncated" in codes
    # It is JSON — the whole point of closing it.
    assert json.loads(json.dumps(event)) == event


def test_terminal_events_are_distinguishable_from_each_other():
    """'this completed' and 'this became something else' never share a shape."""
    done = superseded_event(kind="quiz", seq=4)
    wrong = retracted_event(
        kind="quiz", seq=4, reason="final split reclassified", became_kind="markdown"
    )
    assert done["state"] == "superseded"
    assert wrong["state"] == "retracted"
    assert wrong["becameKind"] == "markdown"
    assert wrong["reason"]
    assert done.keys() != wrong.keys()
    assert {done["state"], wrong["state"]} <= PARTIAL_STATES


def test_reader_rejects_a_malformed_or_foreign_partial():
    good = {IR_PARTIAL_KEY: superseded_event(kind="quiz", seq=1)}
    assert read_partial_event(good) is not None

    assert read_partial_event(None) is None
    assert read_partial_event({}) is None
    assert read_partial_event({IR_PARTIAL_KEY: "nope"}) is None
    assert read_partial_event({IR_PARTIAL_KEY: {"v": 1, "state": "made_up", "seq": 1}}) is None
    assert read_partial_event({IR_PARTIAL_KEY: {"v": 99, "state": "partial", "seq": 1}}) is None
    assert read_partial_event({IR_PARTIAL_KEY: {"v": 1, "state": "partial"}}) is None


def _valid_partial() -> dict:
    return partial_kind_event(
        kind="quiz_set",
        value={"quiz_title": "X"},
        seq=3,
        source_text='{"quiz_title": "X"',
        discriminator={"format": "fence", "language": "json"},
    )


def _valid_retraction() -> dict:
    return retracted_event(
        kind="quiz_set",
        seq=4,
        reason="completed as 'text'",
        became_kind=None,
        became_block_type="text",
    )


@pytest.mark.parametrize(
    ("label", "mutate"),
    [
        # Every one of these passed the OLD reader (which checked only v +
        # state + isinstance(seq, int)) and was rejected by the TS twin, so a
        # Python consumer trusted an event no browser would ever render.
        ("no engine", lambda e: e.pop("engine")),
        ("engine is not a string", lambda e: e.update(engine=7)),
        ("seq is a bool", lambda e: e.update(seq=True)),
        ("no root at all", lambda e: e.pop("root")),
        ("root is not an object", lambda e: e.update(root="quiz")),
        ("root role is wrong", lambda e: e["root"].update(role="text")),
        ("root status is not streaming", lambda e: e["root"].update(status="complete")),
        ("kindState is not speculative", lambda e: e["root"].update(kindState="resolved")),
        ("kind is empty", lambda e: e["root"].update(kind="")),
        ("value is not an object", lambda e: e["root"].update(value=[1, 2])),
        ("discriminator is a foreign shape", lambda e: e["root"].update(discriminator={"format": "toml"})),
        ("path holds a non-segment", lambda e: e["root"].update(path=[{"a": 1}])),
        ("residue is not an object", lambda e: e["root"].update(residue="none")),
        ("a notice has no message", lambda e: e["root"]["residue"]["notices"].append({"code": "x"})),
    ],
)
def test_the_reader_rejects_a_structurally_corrupt_partial(label, mutate):
    """The two readers must accept exactly the same events (closed 2026-08-31).

    Twin: TS ``readPartialKindEvent`` in ``@ai-matrx/content-ir``
    ``wire/partial-kind.ts``. A reader that is looser than its twin is not
    "permissive", it is a divergence: Workflow Studio and the parity harness
    read the channel through THIS function.
    """
    event = _valid_partial()
    assert read_partial_event({IR_PARTIAL_KEY: event}) is not None, "fixture is not valid"
    mutate(event)
    assert read_partial_event({IR_PARTIAL_KEY: event}) is None, (
        f"a partial with {label} was accepted — the TS reader rejects it"
    )


@pytest.mark.parametrize(
    ("label", "mutate"),
    [
        ("no kind", lambda e: e.pop("kind")),
        ("empty kind", lambda e: e.update(kind="")),
        ("no reason", lambda e: e.pop("reason")),
        ("empty reason", lambda e: e.update(reason="")),
        ("becameKind missing entirely", lambda e: e.pop("becameKind")),
        ("becameKind is not a string", lambda e: e.update(becameKind=3)),
        ("becameBlockType missing entirely", lambda e: e.pop("becameBlockType")),
        ("becameBlockType is not a string", lambda e: e.update(becameBlockType={})),
    ],
)
def test_the_reader_rejects_a_structurally_corrupt_terminal(label, mutate):
    event = _valid_retraction()
    assert read_partial_event({IR_PARTIAL_KEY: event}) is not None, "fixture is not valid"
    mutate(event)
    assert read_partial_event({IR_PARTIAL_KEY: event}) is None, (
        f"a retraction with {label} was accepted — the TS reader rejects it"
    )


def test_the_reader_still_accepts_every_event_the_producer_actually_builds():
    """Tightening must not reject the producer's own output — the other failure."""
    for event in (
        _valid_partial(),
        superseded_event(kind="quiz_set", seq=9),
        _valid_retraction(),
        retracted_event(kind="q", seq=2, reason="r", became_kind="k", became_block_type="text"),
    ):
        # Through a JSON round trip, which is how a consumer really receives it.
        wire = json.loads(json.dumps({IR_PARTIAL_KEY: event}))
        assert read_partial_event(wire) is not None


def test_tracker_leaves_no_partial_without_a_terminal_event():
    """The anti-stuck-skeleton guarantee, asserted rather than hoped for."""
    tracker = PartialKindTracker()
    tracker.opened("blk_0", "quiz")
    tracker.opened("blk_1", "timeline")
    tracker.closed("blk_0")

    drained = tracker.drain("stream ended before the block closed")
    assert [block_id for block_id, _ in drained] == ["blk_1"]
    event = drained[0][1]
    assert event["state"] == "retracted"
    assert event["kind"] == "timeline"
    assert "stream ended" in event["reason"]
    assert not tracker.is_open("blk_1")
    assert tracker.drain("again") == []


def test_the_drain_asks_what_each_region_became():
    """§3.3: a drained retraction carries what it turned out to be."""
    tracker = PartialKindTracker()
    tracker.opened("blk_0", "quiz_set")
    drained = tracker.drain("stream ended", resolve=lambda _bid: ("table_set", "table"))
    event = drained[0][1]
    assert event["becameKind"] == "table_set"
    assert event["becameBlockType"] == "table"


def test_a_resolver_that_raises_never_costs_a_block_its_terminal():
    """Law 1 outranks the extra detail: the retraction ships without it."""
    tracker = PartialKindTracker()
    tracker.opened("blk_0", "quiz_set")

    def _boom(_block_id: str):
        raise RuntimeError("resolver exploded")

    drained = tracker.drain("stream ended", resolve=_boom)
    assert [block_id for block_id, _ in drained] == ["blk_0"]
    assert drained[0][1]["state"] == "retracted"
    assert drained[0][1]["becameBlockType"] is None


def test_drain_clears_the_per_block_accounting_it_owns():
    """A drained block must not leave its high-water / last-value behind."""
    tracker = PartialKindTracker()
    tracker.opened("blk_0", "quiz_set")
    assert tracker.advanced("blk_0", {"a": 1})
    assert tracker.regressed("blk_0", 5) is False
    tracker.drain("stream ended")
    # A re-typed region starts its own accounting: less source is not a regression.
    assert tracker.regressed("blk_0", 2) is False
    assert tracker.advanced("blk_0", {"a": 1})


def test_tracker_sequence_numbers_are_monotonic_per_block():
    tracker = PartialKindTracker()
    assert [tracker.next_seq("blk_0") for _ in range(3)] == [1, 2, 3]
    assert tracker.next_seq("blk_1") == 1
