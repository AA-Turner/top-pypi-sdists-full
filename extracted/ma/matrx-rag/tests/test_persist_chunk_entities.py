"""``persist_chunk_entities`` — the ONE write path the inline pass and a host's
batch lane share (knowledge buckets PLAN §1A "Entities").

Forcing cases, each red on the pre-split ``extract_entities`` (which appended
mentions, double-counted edge weights on a re-delivery, stamped nothing on the
chunk and knew no engine):

* the chunk is stamped ``metadata.ner = {engine, version, at}`` + ``ner_extracted_at``
  and every mention carries the engine;
* a re-delivered answer converges — same mentions, edge weight stays 1;
* an engine switch REPLACES the previous engine's mentions and edges;
* a chunk whose answer holds nothing is still stamped (never re-sent);
* the widened kinds persist, and the thematic ones are concepts;
* a dispatching extractor's ``resolve_engine`` picks the engine per call and
  its name is what the chunk is stamped with.

Reuses ``test_ner``'s in-memory fakes (no live DB, no network).
"""

from __future__ import annotations

import uuid
from typing import Any

import pytest
from matrx_rag import _ext

from test_ner import ORG, USER, _FakeTransactionCtx, _KgDb, _make_fake_models  # noqa: F401


@pytest.fixture(autouse=True)
def _reset():
    _ext._reset_for_tests()
    yield
    _ext._reset_for_tests()


@pytest.fixture
def kgdb(monkeypatch) -> _KgDb:
    import matrx_rag.ner as ner_mod

    db = _KgDb()
    monkeypatch.setattr(ner_mod, "transaction", _FakeTransactionCtx())
    _ext.configure(db_models=_make_fake_models(db))
    return db


def _ent(kind: str, name: str, start: int, end: int, conf: float = 0.9) -> dict[str, Any]:
    return {"kind": kind, "canonical_name": name, "span_start": start, "span_end": end, "confidence": conf}


TEXT = "Ava met Acme Corp about hip replacement recovery."
ANSWER = [
    _ent("person", "Ava", 0, 3),
    _ent("organization", "Acme Corp", 8, 17),
    _ent("subject", "hip replacement recovery", 24, 48),
]


async def _persist(chunk_id: str, entities: list[dict[str, Any]], engine: str = "batch", version: str = "v1"):
    from matrx_rag.ner import ChunkExtraction, NerEngineStamp, persist_chunk_entities

    return await persist_chunk_entities(
        [ChunkExtraction(chunk_id=chunk_id, content_text=TEXT, entities=entities)],
        organization_id=ORG,
        user_id=USER,
        engine=NerEngineStamp(engine, version),
        source_kind="note",
        source_id="n-1",
    )


@pytest.mark.asyncio
async def test_the_chunk_and_every_mention_carry_the_engine(kgdb):
    cid = str(uuid.uuid4())
    res = await _persist(cid, ANSWER)

    assert res.succeeded_chunk_ids == {cid}
    stamp = kgdb.stamps[cid]
    assert stamp["ner_extracted_at"] is not None
    assert stamp["metadata"]["ner"]["engine"] == "batch"
    assert stamp["metadata"]["ner"]["version"] == "v1"
    assert stamp["metadata"]["ner"]["at"]
    assert len(kgdb.mentions) == 3
    for m in kgdb.mentions:
        # Native, never pre-dumped: the ORM field stores a str as a JSON STRING.
        assert m["metadata"] == {"engine": "batch", "engine_version": "v1"}


@pytest.mark.asyncio
async def test_a_redelivered_answer_converges(kgdb):
    cid = str(uuid.uuid4())
    await _persist(cid, ANSWER)
    await _persist(cid, ANSWER)  # at-least-once handler: the same delivery again

    assert len(kgdb.mentions) == 3
    assert len(kgdb.edges) == 3
    assert all(e["weight"] == 1 for e in kgdb.edges), [e["weight"] for e in kgdb.edges]


@pytest.mark.asyncio
async def test_an_engine_switch_replaces_the_previous_mentions(kgdb):
    cid = str(uuid.uuid4())
    other = str(uuid.uuid4())
    await _persist(other, [_ent("person", "Ava", 0, 3)], engine="gliner")
    await _persist(cid, [_ent("concept", "Ava met", 0, 7), _ent("person", "Ava", 0, 3)], engine="gliner")
    await _persist(cid, ANSWER, engine="batch")

    names = sorted(kgdb.entities[m["entity_id"]]["name"] for m in kgdb.mentions if m["chunk_id"] == cid)
    assert names == ["Acme Corp", "Ava", "hip replacement recovery"]
    # Another chunk's mentions are never touched.
    assert [m["chunk_id"] for m in kgdb.mentions].count(other) == 1
    assert kgdb.stamps[cid]["metadata"]["ner"]["engine"] == "batch"


@pytest.mark.asyncio
async def test_an_empty_answer_is_still_done(kgdb):
    cid = str(uuid.uuid4())
    await _persist(cid, ANSWER, engine="gliner")
    res = await _persist(cid, [], engine="batch")

    assert res.succeeded_chunk_ids == {cid}
    assert kgdb.stamps[cid]["metadata"]["ner"]["engine"] == "batch"
    assert [m for m in kgdb.mentions if m["chunk_id"] == cid] == []


@pytest.mark.asyncio
async def test_widened_kinds_persist_and_thematic_ones_are_concepts(kgdb):
    from matrx_rag.ner import CONCEPT_KINDS, NER_KINDS

    assert {"product", "place", "subject", "activity"} <= NER_KINDS
    cid = str(uuid.uuid4())
    await _persist(
        cid,
        [
            _ent("product", "Supabase", 0, 8),
            _ent("place", "Irvine", 10, 16),
            _ent("subject", "AP chemistry", 18, 30),
            _ent("activity", "quarterly tax filing", 31, 51),
            _ent("spaceship", "Enterprise", 52, 62),  # invented kind: dropped
        ],
    )
    kinds = {e["kind"]: e["is_concept"] for e in kgdb.entities.values()}
    assert kinds == {"product": False, "place": False, "subject": True, "activity": True}
    assert CONCEPT_KINDS == {"concept", "subject", "activity"}


@pytest.mark.asyncio
async def test_a_dispatching_extractor_picks_the_engine_per_call(kgdb):
    from matrx_rag.ner import NerChunkInput, NerEngine, NerEngineStamp, extract_entities

    class _Engine:
        def __init__(self, name: str) -> None:
            self.name = name
            self.calls = 0

        async def extract(self, text, **_kw):
            self.calls += 1
            return [_ent("person", "Ava", 0, 3)]

    fast, slow = _Engine("gliner"), _Engine("llm")
    asked: list[tuple[str, str, str | None]] = []

    class _Dispatcher:
        async def extract(self, text, **_kw):  # never used: resolve_engine answers
            raise AssertionError("the dispatcher itself must not extract")

        async def resolve_engine(self, *, organization_id, user_id, source_kind):
            asked.append((organization_id, user_id, source_kind))
            eng = slow if source_kind == "transcript" else fast
            return NerEngine(stamp=NerEngineStamp(eng.name, "7"), extractor=eng)

    _ext.configure(ner_extractor=_Dispatcher())
    a, b = str(uuid.uuid4()), str(uuid.uuid4())
    await extract_entities([NerChunkInput(a, TEXT)], organization_id=ORG, user_id=USER, source_kind="note")
    await extract_entities([NerChunkInput(b, TEXT)], organization_id=ORG, user_id=USER, source_kind="transcript")

    assert (fast.calls, slow.calls) == (1, 1)
    assert asked == [(ORG, USER, "note"), (ORG, USER, "transcript")]
    assert kgdb.stamps[a]["metadata"]["ner"] | {"at": None} == {"engine": "gliner", "version": "7", "at": None}
    assert kgdb.stamps[b]["metadata"]["ner"]["engine"] == "llm"


@pytest.mark.asyncio
async def test_an_engine_that_cannot_be_resolved_extracts_nothing_and_says_so(kgdb):
    from matrx_rag.ner import NerChunkInput, extract_entities

    class _Broken:
        async def extract(self, text, **_kw):
            raise AssertionError("must not extract")

        async def resolve_engine(self, **_kw):
            raise RuntimeError("knob knowledge.ner_engine names 'spacy'")

    _ext.configure(ner_extractor=_Broken())
    cid = str(uuid.uuid4())
    res = await extract_entities([NerChunkInput(cid, TEXT)], organization_id=ORG, user_id=USER)
    assert res.succeeded_chunk_ids == set()
    assert any("engine_resolution_error" in e for e in res.errors)
    assert cid not in kgdb.stamps
