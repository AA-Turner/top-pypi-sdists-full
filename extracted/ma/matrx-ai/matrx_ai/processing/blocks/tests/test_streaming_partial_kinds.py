"""The streaming partial-kinds contract, over the REAL StreamBlockProcessor.

Everything here drives the production processor with real token streams — no
mocks, no hand-built events. The invariants asserted are the ones a client
actually depends on: every partial is parseable JSON, values only ever advance
toward the truth, and every announced partial ends in exactly ONE terminal
event so a skeleton can never be left on screen forever.

Contract: ``common-docs/systems/content-ir-system/STREAMING_PARTIAL_KINDS.md``.
"""

from __future__ import annotations

import json

import pytest
from matrx_ai.processing.blocks.envelope import IR_ENVELOPE_KEY
from matrx_ai.processing.blocks.models.base import BlockStatus
from matrx_ai.processing.blocks.stream_processor import StreamBlockProcessor
from matrx_graph.content_ir.partial import (
    IR_PARTIAL_KEY,
    PARTIAL_STATES,
    read_partial_event,
)

QUIZ = {
    "quiz_title": "Space Basics",
    "multiple_choice": [
        {
            "question": "Closest star to Earth?",
            "options": ["The Sun", "Sirius", "Alpha Centauri"],
            "correct_answer": "The Sun",
            "explanation": "About 150 million km away — far closer than any other star.",
        },
        {
            "question": "Which planet is red?",
            "options": ["Mars", "Venus"],
            "correct_answer": "Mars",
            "explanation": "Iron oxide on the surface gives Mars its colour.",
        },
    ],
}

QUIZ_DOC = "Here is your quiz.\n\n```json\n" + json.dumps(QUIZ, indent=2) + "\n```\n\nGood luck!\n"


def drive(document: str, *, chunk: int = 7):
    """Stream ``document`` through the real processor and return every event."""
    processor = StreamBlockProcessor()
    events = []
    for i in range(0, len(document), chunk):
        events.extend(processor.process_token(document[i : i + chunk]))
    events.extend(processor.finalize())
    return events


def partial_events(events):
    out = []
    for event in events:
        parsed = read_partial_event(event.metadata)
        if parsed is not None:
            out.append((event, parsed))
    return out


# ---------------------------------------------------------------------------
# The happy path — pre-recognition, progressive fill, finalize
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("chunk", [1, 3, 7, 40])
def test_a_streaming_kind_fills_in_and_then_finalizes(chunk):
    """The contract end to end, at four different token granularities.

    Chunk size is the parameter that breaks naive streaming parsers, so the
    same document is driven one character at a time and forty at a time.
    """
    events = drive(QUIZ_DOC, chunk=chunk)
    channel = partial_events(events)
    assert channel, "no partial was ever announced for a streaming quiz"

    states = [event["state"] for _, event in channel]
    assert states[0] == "partial", "the first thing a client hears must be provisional"
    assert states[-1] == "superseded", "the quiz completed as a quiz — it must supersede"
    assert states.count("superseded") == 1
    assert "retracted" not in states

    # Pre-recognition is stated, not implied.
    first = channel[0][1]
    assert first["root"]["kindState"] == "speculative"
    assert first["root"]["status"] == "streaming"
    assert first["root"]["kind"]

    # Every partial value is real, parseable JSON carrying its own identity.
    for _, event in channel:
        if event["state"] != "partial":
            continue
        value = event["root"]["value"]
        json.loads(json.dumps(value))
        assert value["__kind"] == event["root"]["kind"]

    # seq is monotonic per block — the client's staleness key.
    seqs = [event["seq"] for _, event in channel]
    assert seqs == sorted(seqs)
    assert len(set(seqs)) == len(seqs), "a repeated seq makes ordering undecidable"


def test_partial_values_only_ever_grow_toward_the_finished_quiz():
    """A partial may be INCOMPLETE; it may never be WRONG.

    This is what lets the frontend render a partial without lying to the user:
    a question list only gains entries, and a string only gains characters.
    """
    channel = [e for _, e in partial_events(drive(QUIZ_DOC)) if e["state"] == "partial"]
    counts = []
    for event in channel:
        value = event["root"]["value"]
        questions = value.get("questions") or value.get("multiple_choice") or []
        counts.append(len(questions))
        for i, question in enumerate(questions):
            truth = QUIZ["multiple_choice"][i]
            text = question.get("question") or ""
            assert truth["question"].startswith(text), (
                f"partial question {text!r} is not a prefix of {truth['question']!r}"
            )
    assert counts == sorted(counts), "the question list shrank mid-stream"
    assert counts[-1] == len(QUIZ["multiple_choice"])


def test_no_partial_is_ever_stamped_where_the_verified_envelope_lives():
    """Law 1 of the envelope producers, honoured literally.

    A partial on ``__ir`` would be seeded into the frontend's fingerprint-keyed
    envelope cache and poison every later read of the region. The two channels
    must never touch.
    """
    for event in drive(QUIZ_DOC):
        if event.status != BlockStatus.COMPLETE:
            assert IR_ENVELOPE_KEY not in (event.metadata or {})
        partial = read_partial_event(event.metadata)
        if partial is not None and partial["state"] == "partial":
            assert IR_ENVELOPE_KEY not in (event.metadata or {})


def test_prose_and_code_get_no_partial_at_all():
    """A partial is only worth announcing where it can progressively FILL.

    Prose and code stream as content already; announcing a kind for them would
    be a skeleton with nothing to put in it.
    """
    document = "Just some prose.\n\n```python\nprint('hi')\n```\n\nMore prose.\n"
    assert partial_events(drive(document)) == []


# ---------------------------------------------------------------------------
# The escape hatch
# ---------------------------------------------------------------------------


def test_a_wrong_detection_is_retracted_and_names_what_it_became():
    """A region that stops being the detected kind must say so explicitly.

    This is a REAL retraction produced by the production detector: a bare JSON
    object with a quiz root key is recognized as a quiz while it streams, and
    then prose continues on the same line, so the final split reads the whole
    region as text.
    """
    document = '{"quiz_title": "X", "multiple_choice": [1]} and then I kept talking inline.\n'
    channel = partial_events(drive(document, chunk=4))
    states = [event["state"] for _, event in channel]

    assert "partial" in states, "detection never fired — this fixture proves nothing"
    assert states[-1] == "retracted"
    retraction = channel[-1][1]
    assert retraction["reason"], "a retraction with no reason is a silent swap"
    # 'became something else' and 'completed' are structurally distinguishable.
    assert "becameKind" in retraction and "becameBlockType" in retraction
    assert retraction["becameBlockType"] == "text"
    assert "kindState" not in retraction  # never confusable with a partial


@pytest.mark.parametrize(
    "document",
    [
        QUIZ_DOC,
        '{"quiz_title": "X", "multiple_choice": [1]} and then I kept talking inline.\n',
        '{"quiz_title": "X", "multiple_choice": [array of questions]}\n',
        "```json\n{\"quiz_title\": \"Y\", \"multiple_choice\": []}\n```\n",
        "```flashcards\nQ: a\nA: b\n",  # a fence that never closes
        "text\n\n| One | Two |\n|---|---|\n| a | b |\n",
        "Just prose, nothing structured at all.\n",
    ],
)
def test_every_announced_partial_ends_in_exactly_one_terminal(document):
    """THE invariant. A partial that never terminates is a stuck skeleton.

    Asserted per block over a corpus that includes a clean finish, two real
    retractions, an unterminated fence, a re-absorbed phantom, and pure prose —
    the shapes that each break a different half of the bookkeeping.
    """
    per_block: dict[str, list[str]] = {}
    for event, parsed in partial_events(drive(document, chunk=4)):
        assert parsed["state"] in PARTIAL_STATES
        per_block.setdefault(event.block_id, []).append(parsed["state"])

    for block_id, states in per_block.items():
        terminals = [s for s in states if s != "partial"]
        assert len(terminals) == 1, (
            f"block {block_id} produced {len(terminals)} terminal events "
            f"({states}) — the client cannot know when to stop rendering a skeleton"
        )
        assert states[-1] == terminals[0], (
            f"block {block_id} emitted a partial AFTER its terminal: {states}"
        )
        assert states[0] == "partial"


def test_finalize_retracts_anything_still_open_as_the_last_backstop():
    """The independent second layer, exercised directly.

    The per-block paths close the ordinary cases; this is what fires the day
    one of them silently doesn't, so it is asserted rather than assumed.
    """
    processor = StreamBlockProcessor()
    for i in range(0, len(QUIZ_DOC), 7):
        processor.process_token(QUIZ_DOC[i : i + 7])

    open_ids = [b.block_id for b in processor.get_blocks() if processor._partials.is_open(b.block_id)]
    assert open_ids, "fixture never opened a partial — the backstop is untested"

    drained = processor.drain_open_partials("stream ended before the block resolved")
    assert [e.block_id for e in drained] == open_ids
    for event in drained:
        parsed = read_partial_event(event.metadata)
        assert parsed is not None and parsed["state"] == "retracted"
        assert "stream ended" in parsed["reason"]
    # Draining twice must not double-terminate.
    assert processor.drain_open_partials("again") == []


def test_a_block_that_vanished_from_the_split_still_gets_its_terminal():
    """LAW 1 HAS NO "unless the block is still there" CLAUSE (closed 2026-08-31).

    The drain empties the tracker in one shot, so a block the tracker names and
    the processor no longer holds used to be SKIPPED — closed on the server,
    open forever on the client. That is the one case the ordinary per-block
    paths structurally cannot reach, so it is the case that matters most.

    The vanishing is forced directly (the block list is emptied under the
    tracker) because that is exactly the state the hole describes: the ledger
    says a kind was announced, and nothing in the block list can terminate it.
    """
    processor = StreamBlockProcessor()
    for i in range(0, len(QUIZ_DOC), 7):
        processor.process_token(QUIZ_DOC[i : i + 7])

    open_ids = [b.block_id for b in processor.get_blocks() if processor._partials.is_open(b.block_id)]
    assert open_ids, "fixture never opened a partial — this test attacks nothing"
    announced_types = {bid: processor._partial_shadow[bid][1] for bid in open_ids}

    processor._blocks = []  # the block vanished from the final split

    drained = processor.drain_open_partials("stream ended before the block resolved")
    assert [e.block_id for e in drained] == open_ids, (
        "a block missing from the final list got NO terminal — the client is "
        "left rendering a skeleton that will fill in never"
    )
    for event in drained:
        parsed = read_partial_event(event.metadata)
        assert parsed is not None and parsed["state"] == "retracted"
        # The synthesized event is honest about what it is: an empty, complete
        # block, typed as it was when the kind was announced.
        assert event.status == BlockStatus.COMPLETE
        assert event.type == announced_types[event.block_id]
        assert not event.content and not event.data
    assert processor.drain_open_partials("again") == []


def test_a_drained_retraction_names_what_the_region_became():
    """§3.3's ``becameBlockType`` is POPULATED, not decorative (2026-08-31).

    The drain is holding the block and its final type; passing neither made
    every drained retraction serialize ``becameKind: null`` /
    ``becameBlockType: null``, so a consumer's "re-route on what it became"
    branch was structurally unreachable.
    """
    processor = StreamBlockProcessor()
    for i in range(0, len(QUIZ_DOC), 7):
        processor.process_token(QUIZ_DOC[i : i + 7])

    by_id = {b.block_id: b for b in processor.get_blocks()}
    drained = processor.drain_open_partials("stream ended before the block resolved")
    assert drained, "fixture never opened a partial"
    for event in drained:
        parsed = read_partial_event(event.metadata)
        assert parsed is not None
        assert parsed["becameBlockType"] == by_id[event.block_id].type, (
            "the drain knows the block's final type and must say so"
        )
        # A quiz fence maps to a registered kind, so the resolvable half is
        # populated too — null here would mean "no registered kind", a lie.
        assert parsed["becameKind"] == "quiz_set"


def test_an_identical_value_is_not_re_sent_every_token():
    """Wire cost: the block re-splits per token, the partial must not."""
    channel = [e for _, e in partial_events(drive(QUIZ_DOC, chunk=1)) if e["state"] == "partial"]
    serialized = [json.dumps(e["root"]["value"], sort_keys=True) for e in channel]
    assert len(set(serialized)) == len(serialized), "the same partial value shipped twice"


# ---------------------------------------------------------------------------
# Root-kind pre-recognition — the UNFENCED bound-agent stream
# ---------------------------------------------------------------------------
#
# An agent bound through ``response_format_for_kind`` streams a bare JSON
# document: no fence, no XML tag. Before 2026-08-23 the detector typed it
# ``text``/``code`` and announced NOTHING, so the user watched raw JSON
# accumulate and then snap into a component (Arman, on a live Study Pack run).
# The recognizer reads the FIRST key and nothing else, which is what makes the
# announcement land on the first ~30 characters of the answer.

FLASHCARDS_UNFENCED = json.dumps(
    {
        "__kind": "flashcard_set",
        "title": "Photosynthesis",
        "cards": [
            {"front": "What splits water?", "back": "Photosystem II.", "difficulty": "medium"},
            {"front": "Where do light reactions run?", "back": "The thylakoid membrane.", "difficulty": "easy"},
        ],
    },
    indent=2,
)


def test_unfenced_root_kind_json_announces_on_its_first_key():
    events = drive(FLASHCARDS_UNFENCED, chunk=6)
    channel = [e for _, e in partial_events(events)]
    partials = [e for e in channel if e["state"] == "partial"]

    assert partials, "an unfenced __kind document announced no partial at all"
    assert all(e["root"]["kind"] == "flashcard_set" for e in partials)
    # Pre-recognition: the FIRST announcement arrives before the answer's own
    # content does — the whole point is a kind-specific loader, not a late swap.
    first_value = partials[0]["root"]["value"]
    assert first_value.get("__kind") == "flashcard_set"
    assert not first_value.get("cards"), (
        "the first partial already carried cards — recognition was late, so the "
        "user watched raw JSON before anything rendered"
    )
    # It fills in, card by card, exactly like the XML flashcard renderer does.
    card_counts = [len(e["root"]["value"].get("cards") or []) for e in partials]
    assert card_counts[-1] == 2
    assert card_counts == sorted(card_counts), f"a partial LOST cards: {card_counts}"
    terminals = [e for e in channel if e["state"] != "partial"]
    assert [e["state"] for e in terminals] == ["superseded"]


def test_a_late_or_absent_kind_key_announces_nothing():
    """Pre-recognition is FIRST-key only — a late ``__kind`` is not recognition."""
    late = json.dumps({"title": "Photosynthesis", "__kind": "flashcard_set", "cards": []})
    assert [e for _, e in partial_events(drive(late, chunk=6))] == []


def test_a_declared_fence_still_wins_over_a_body_level_kind_key():
    """Two declarations for one region is the bug; the detector's type wins."""
    doc = "```json\n" + json.dumps({"__kind": "quiz_set", "quiz_title": "X", "multiple_choice": []}) + "\n```\n"
    kinds = {e["root"]["kind"] for _, e in partial_events(drive(doc, chunk=5)) if e["state"] == "partial"}
    assert kinds <= {"quiz_set"}
