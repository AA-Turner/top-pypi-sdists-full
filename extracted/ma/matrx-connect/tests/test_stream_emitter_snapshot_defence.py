"""THE DELTA DEFENSE — a provider that streams snapshots must not reach the wire.

Every provider streams visible text through ``StreamEmitter.send_chunk``, but
they do not all agree on what a chunk IS. Anthropic and OpenAI key off explicit
``.delta`` fields (each chunk is the NEW text); a provider that hands back the
running text so far is sending a growing SNAPSHOT, and forwarding those verbatim
replays the whole turn on every chunk — the ~860K-characters-for-a-6K-envelope
shape seen live on 2026-09-08.

``send_chunk`` is the one seam every provider passes through on its way to a
user's wire, and the only one that already holds the accumulated turn text a
snapshot has to be diffed against, so the repair lives there. These tests pin
both halves of the contract: snapshots are reduced to deltas AND screamed about,
true deltas are untouched AND silent.
"""

from __future__ import annotations

import orjson
import pytest

from matrx_connect.emitters import stream_emitter as se
from matrx_connect.streaming import error_capture


@pytest.fixture(autouse=True)
def _reset_capture():
    error_capture.configure_error_capture(None)
    yield
    error_capture.configure_error_capture(None)


class _Captures:
    def __init__(self) -> None:
        self.calls: list[tuple[BaseException, dict]] = []

    async def __call__(self, exc: BaseException, **fields) -> None:
        self.calls.append((exc, fields))


@pytest.fixture
def captures(monkeypatch: pytest.MonkeyPatch) -> _Captures:
    sink = _Captures()
    error_capture.configure_error_capture(sink, allow_in_tests=True)
    return sink


def _emitter() -> se.StreamEmitter:
    em = se.StreamEmitter()
    em._last_chunk_time = -1e9  # force a flush on every chunk so the wire is exact
    return em


async def _wire_text(em: se.StreamEmitter) -> str:
    """The text actually published to the NDJSON wire, concatenated."""
    await em._flush_text()
    out: list[str] = []
    for raw in em._wire_replay:
        try:
            event = orjson.loads(raw)
        except orjson.JSONDecodeError:
            continue
        if event.get("e") == "c":
            out.append(event.get("t", ""))
    return "".join(out)


ANSWER = "Here is the raw specification you asked for, in full, with no omissions."


def _snapshots(text: str, step: int = 7) -> list[str]:
    """The broken shape: each chunk is the running text SO FAR."""
    return [text[:i] for i in range(step, len(text) + step, step)][: (len(text) // step) + 1] + [
        text
    ]


def _deltas(text: str, step: int = 7) -> list[str]:
    """The correct shape: each chunk is only the NEW text."""
    return [text[i : i + step] for i in range(0, len(text), step)]


@pytest.mark.asyncio
async def test_snapshot_chunks_reach_the_wire_as_deltas_only(captures: _Captures) -> None:
    em = _emitter()
    for chunk in _snapshots(ANSWER):
        await em.send_chunk(chunk)

    wire = await _wire_text(em)
    assert wire == ANSWER, "the wire must carry the answer exactly once, not N growing copies"
    assert em.get_turn_text() == ANSWER
    assert em.provider_sent_snapshots is True


@pytest.mark.asyncio
async def test_snapshot_stream_without_the_defence_would_explode() -> None:
    """Falsification: the raw snapshot stream really is quadratic.

    If this ever stops being true the fixture is wrong and the test above proves
    nothing.
    """
    raw = "".join(_snapshots(ANSWER))
    assert len(raw) > 5 * len(ANSWER)


@pytest.mark.asyncio
async def test_snapshot_screams_exactly_once_per_run(captures: _Captures) -> None:
    em = _emitter()
    for chunk in _snapshots(ANSWER):
        await em.send_chunk(chunk)
    # A second turn on the same run — still one capture total.
    em.reset_turn_text()
    for chunk in _snapshots("A second cumulative answer that also arrives as snapshots."):
        await em.send_chunk(chunk)

    assert len(captures.calls) == 1, "the scream must be once per run, not once per chunk"
    exc, fields = captures.calls[0]
    assert isinstance(exc, se.ProviderSentSnapshotNotDelta)
    assert fields["kind"].startswith(se.SNAPSHOT_CAPTURE_KIND)
    # chunk_chars/accumulated_chars are NOT top-level kwargs — the capture sink
    # takes a fixed keyword surface (record_error) and anything else must ride
    # in `context`, or the call raises TypeError and the scream is never filed
    # at all (see commit 6af31b415b). Assert the property this test protects —
    # the scream fires once and carries chunk_chars — against that real shape.
    context = fields["context"]
    assert context["chunk_chars"] > context["accumulated_chars"]


@pytest.mark.asyncio
async def test_true_deltas_pass_through_untouched_and_silently(captures: _Captures) -> None:
    em = _emitter()
    for chunk in _deltas(ANSWER):
        await em.send_chunk(chunk)

    assert await _wire_text(em) == ANSWER
    assert em.get_turn_text() == ANSWER
    assert em.provider_sent_snapshots is False
    assert captures.calls == [], "a well-behaved provider must never be screamed about"


@pytest.mark.asyncio
async def test_repeated_text_that_is_not_a_prefix_extension_is_never_touched(
    captures: _Captures,
) -> None:
    """The defense NEVER guesses — only a strict growing prefix is a snapshot."""
    em = _emitter()
    long_delta = "x" * 200
    await em.send_chunk(long_delta)
    await em.send_chunk("y" * 400)  # longer than the accumulator, but not a prefix extension

    assert await _wire_text(em) == long_delta + "y" * 400
    assert captures.calls == []


@pytest.mark.asyncio
@pytest.mark.parametrize("opening", ["\n", " ", "a"])
async def test_a_degenerate_opening_is_never_read_as_a_snapshot(
    captures: _Captures, opening: str
) -> None:
    """The floor's job: whitespace-ish or one-character openings, where a delta
    stream really can produce a prefix coincidence, stay below detection."""
    em = _emitter()
    follow = opening * 3 + "and then the real answer continues from here."
    await em.send_chunk(opening)
    await em.send_chunk(follow)

    assert await _wire_text(em) == opening + follow
    assert em.provider_sent_snapshots is False
    assert captures.calls == []


@pytest.mark.asyncio
async def test_detection_must_land_on_the_second_chunk(captures: _Captures) -> None:
    """Why the floor is low. Once one raw snapshot has been forwarded, the
    accumulator is a concatenation of snapshots and no later snapshot is a
    prefix of it — so a high floor would mean never detecting at all."""
    assert se.SNAPSHOT_MIN_ACCUMULATED <= 4
    em = _emitter()
    chunks = _snapshots(ANSWER)
    await em.send_chunk(chunks[0])
    await em.send_chunk(chunks[1])
    assert em.provider_sent_snapshots is True, "the second chunk is the only reliable tell"


@pytest.mark.asyncio
async def test_a_duplicate_snapshot_chunk_adds_nothing_to_the_wire(captures: _Captures) -> None:
    em = _emitter()
    await em.send_chunk(ANSWER)
    await em.send_chunk(ANSWER)  # the same snapshot again, no growth

    assert await _wire_text(em) == ANSWER


@pytest.mark.asyncio
async def test_reset_turn_text_clears_the_accumulator_and_its_length() -> None:
    em = _emitter()
    await em.send_chunk(ANSWER)
    em.reset_turn_text()
    assert em.get_turn_text() == ""
    assert em._turn_text_len == 0
