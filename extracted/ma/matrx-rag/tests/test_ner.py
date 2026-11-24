"""Phase C — LLM-driven NER → kg_entities widening.

Verifies matrx_rag.ner.extract_entities against in-memory ORM model fakes,
including the typed correlated ``confidence_avg`` update:

* entity dedup across two chunks mentioning the same canonical name produces
  one kg_entities row and two mentions.
* kg_chunk_entities mention rows are written with spans + confidence.
* a co_occurs_with edge is emitted for two entities sharing one chunk.
* a REUSED chunk (one whose content_sha256 already exists) does NOT trigger
  re-NER — the ingest pipeline only feeds NEW (inserted) chunk ids to NER, so
  the extractor is never called for it.
* with NO extractor injected, extract_entities is a clean no-op.
* tier-B's bulk_upsert (ON CONFLICT on the canonical partial index) inherits
  a pre-existing row's id instead of duplicating it (regression for the
  deadlock-fix refactor — see ner.py module docstring).

No live DB, no network — mirrors test_chunk_reuse's fake style.
"""

from __future__ import annotations

import asyncio
import uuid
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_rag import _ext

# ---------------------------------------------------------------------------
# Fake DB + fake ORM models — the minimal surface ner.py touches.
# ---------------------------------------------------------------------------


class _KgDb:
    def __init__(self) -> None:
        self.entities: dict[str, dict[str, Any]] = {}  # by id
        self.mentions: list[dict[str, Any]] = []
        self.edges: list[dict[str, Any]] = []
        # chunk_id -> the completion stamp persist_chunk_entities wrote
        self.stamps: dict[str, dict[str, Any]] = {}
        # tier-B ON CONFLICT DO UPDATE calls (must stay 0: they lock existing entity rows FOR UPDATE)
        self.entity_upserts = 0

    def find_entity(self, org: str, kind: str, name: str) -> dict[str, Any] | None:
        for e in self.entities.values():
            e_org = e["organization_id"] or "00000000-0000-0000-0000-000000000000"
            if e_org == org and e["kind"] == kind and e["name"].lower() == name.lower():
                return e
        return None


_ORG_SENTINEL = "00000000-0000-0000-0000-000000000000"


class _ChunkLockQuery:
    """``KgChunks.filter(id=...).select_for_update(mode=...).values("id")``: the lock read."""

    def select_for_update(self, **_kw: Any) -> _ChunkLockQuery:
        return self

    async def values(self, *_fields: str) -> list[dict[str, Any]]:
        return []


def _make_fake_models(db: _KgDb) -> dict[str, Any]:
    """Fake matrx-orm model classes implementing exactly the surface ner.py
    uses (filter/values for the tier-B preflight, bulk_upsert for tier-B
    resolution, bulk_insert_ignore / bulk_upsert_increment for tier C),
    backed by the shared in-memory _KgDb. Injected via
    ``configure(db_models=...)`` — the same seam a divergent host would use."""

    class _EntityQuery:
        def __init__(self, filters: dict[str, Any]) -> None:
            self._filters = filters

        def filter(self, **kw: Any) -> _EntityQuery:
            self._filters.update(kw)
            return self

        async def values(self, *fields: str) -> list[dict[str, Any]]:
            out: list[dict[str, Any]] = []
            for e in db.entities.values():
                if "kind" in self._filters and e["kind"] != self._filters["kind"]:
                    continue
                if self._filters.get("organization_id__isnull"):
                    if e["organization_id"] is not None:
                        continue
                elif "organization_id" in self._filters and (
                    e["organization_id"] != self._filters["organization_id"]
                ):
                    continue
                out.append({f: e[f] for f in fields})
            return out

    class _FakeKgEntities:
        @classmethod
        def filter(cls, **kw: Any) -> _EntityQuery:
            return _EntityQuery(dict(kw))

        @classmethod
        async def update_where(cls, filters: dict[str, Any], **updates: Any) -> Any:
            """Fakes tier-D's ``KgEntities.update_where({"id": eid},
            confidence_avg=Subquery(...), updated_at=Now())``. Business-logic
            equivalent of the real correlated-subquery UPDATE (mean confidence
            across this entity's kg_chunk_entities mentions) — the fake DB
            replicates the RESULT rather than interpreting the rendered SQL,
            same as every other fake model here."""
            from matrx_orm import Subquery as _Subquery

            eid = filters.get("id")
            row = db.entities.get(eid)
            if row is None:
                return SimpleNamespace(rows_affected=0)
            for k, v in updates.items():
                if isinstance(v, _Subquery):
                    confs = [
                        m["confidence"]
                        for m in db.mentions
                        if m["entity_id"] == eid and m["confidence"] is not None
                    ]
                    row[k] = (sum(confs) / len(confs)) if confs else None
                else:
                    row[k] = v
            return SimpleNamespace(rows_affected=1)

        @classmethod
        async def bulk_upsert(cls, *_a: Any, **_kw: Any) -> list[Any]:
            # ON CONFLICT DO UPDATE on kg_entities locks every EXISTING row FOR UPDATE (``kind`` is a key
            # column), which deadlocked against tier C's foreign-key share locks (live 40P01, 2026-11-16).
            db.entity_upserts += 1
            raise AssertionError("tier B must never DO UPDATE existing kg_entities rows")

        @classmethod
        async def bulk_insert_ignore(
            cls,
            objects_data: list[dict[str, Any]],
            *,
            on_conflict: Any = None,
            returning: Any = False,
        ) -> Any:
            # INSERT ... ON CONFLICT (canonical partial index) DO NOTHING RETURNING * —
            # only NEW buckets come back; an existing bucket is skipped and never locked.
            landed: list[dict[str, Any]] = []
            for row in objects_data:
                org_key = row["organization_id"] or _ORG_SENTINEL
                if db.find_entity(org_key, row["kind"], row["name"]) is not None:
                    continue
                new_id = str(uuid.uuid4())
                db.entities[new_id] = {
                    "id": new_id,
                    "organization_id": row["organization_id"],
                    "kind": row["kind"],
                    "name": row["name"],
                    "attrs": row["attrs"],
                    "is_concept": row.get("is_concept"),
                    "confidence_avg": None,
                }
                landed.append(dict(db.entities[new_id]))
            return landed if returning else len(landed)

    class _MentionRowsQuery:
        """``KgChunkEntities.filter(chunk_id=...).values("entity_id")`` — the
        replace step's read of a chunk's previous mentions. Any other chained
        use (tier D's Subquery) is a no-op stand-in."""

        def __init__(self, kw: dict[str, Any]) -> None:
            self._kw = kw

        def filter(self, **kw: Any) -> _MentionRowsQuery:
            self._kw.update(kw)
            return self

        def annotate(self, **kw: Any) -> _MentionRowsQuery:
            return self

        def select(self, *fields: str) -> _MentionRowsQuery:
            return self

        async def values(self, *fields: str) -> list[dict[str, Any]]:
            cid = self._kw.get("chunk_id")
            return [{f: m.get(f) for f in fields} for m in db.mentions if m["chunk_id"] == cid]

    class _StubMentionQuery:
        """Chainable no-op stand-in for ``KgChunkEntities.filter(...)
        .annotate(...).select(...)`` — tier-D's ``_bump_confidence_avg``
        builds this expression to WRAP in a real ``Subquery(...)``, but
        never renders it (``_FakeKgEntities.update_where`` intercepts the
        ``Subquery`` instance and computes the equivalent business result
        directly from ``db.mentions`` — see above). Only needs to exist and
        be chainable, never to be semantically correct."""

        def filter(self, **kw: Any) -> _StubMentionQuery:
            return self

        def annotate(self, **kw: Any) -> _StubMentionQuery:
            return self

        def select(self, *fields: str) -> _StubMentionQuery:
            return self

    class _FakeKgChunkEntities:
        @classmethod
        def filter(cls, **kw: Any) -> _MentionRowsQuery:
            return _MentionRowsQuery(dict(kw))

        @classmethod
        async def delete_where(cls, **kw: Any) -> int:
            before = len(db.mentions)
            db.mentions[:] = [m for m in db.mentions if m["chunk_id"] != kw.get("chunk_id")]
            return before - len(db.mentions)

        @classmethod
        async def bulk_insert_ignore(
            cls,
            objects_data: list[dict[str, Any]],
            *,
            on_conflict: Any = None,
            connection: Any = None,
        ) -> int:
            n = 0
            for r in objects_data:
                # ON CONFLICT (chunk_id, entity_id, span_start) DO NOTHING.
                if any(
                    m["chunk_id"] == r["chunk_id"]
                    and m["entity_id"] == r["entity_id"]
                    and m["span_start"] == r["span_start"]
                    for m in db.mentions
                ):
                    continue
                db.mentions.append(dict(r))
                n += 1
            return n

    class _FakeKgEdges:
        @classmethod
        async def delete_where(cls, **kw: Any) -> int:
            before = len(db.edges)
            db.edges[:] = [
                e
                for e in db.edges
                if not (e["source_chunk_id"] == kw.get("source_chunk_id") and e["kind"] == kw.get("kind"))
            ]
            return before - len(db.edges)

        @classmethod
        async def bulk_upsert_increment(
            cls,
            objects_data: list[dict[str, Any]],
            *,
            on_conflict: Any = None,
            increments: dict[str, int] | None = None,
            connection: Any = None,
        ) -> int:
            bump = (increments or {}).get("weight", 1)
            n = 0
            for r in objects_data:
                hit = next(
                    (
                        e
                        for e in db.edges
                        if e["kind"] == "co_occurs_with"
                        and e["source_chunk_id"] == r["source_chunk_id"]
                        and e["src_id"] == r["src_id"]
                        and e["dst_id"] == r["dst_id"]
                    ),
                    None,
                )
                if hit is not None:
                    hit["weight"] = (hit.get("weight") or 0) + bump
                else:
                    db.edges.append(dict(r))
                    n += 1
            return n

    class _FakeKgChunks:
        @classmethod
        def filter(cls, **_kw: Any) -> _ChunkLockQuery:
            return _ChunkLockQuery()

        @classmethod
        async def update_where(cls, filters: dict[str, Any], **updates: Any) -> Any:
            """The completion stamp: ``ner_extracted_at`` + a ``JsonbMerge`` of
            ``{"ner": {...}}`` into ``metadata`` (the merged value is recorded)."""
            for cid in filters.get("id__in", []):
                row = db.stamps.setdefault(cid, {"metadata": {}})
                for k, v in updates.items():
                    merged = getattr(v, "value", None)
                    if k == "metadata" and isinstance(merged, dict):
                        row["metadata"].update(merged)
                    else:
                        row[k] = v
            return SimpleNamespace(rows_affected=len(filters.get("id__in", [])))

    return {
        "KgEntities": _FakeKgEntities,
        "KgChunkEntities": _FakeKgChunkEntities,
        "KgEdges": _FakeKgEdges,
        "KgChunks": _FakeKgChunks,
    }


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def reset_ext():
    _ext._reset_for_tests()
    yield
    _ext._reset_for_tests()


class _FakeTransactionCtx:
    """Stand-in for ``matrx_orm.transaction()`` — ner.py's persist step no
    longer touches a raw pool/connection at all (every write rides the
    fully-ORM ``bulk_insert_ignore`` / ``bulk_upsert_increment`` seam), so
    the fake model classes below never see a connection either way. This
    just needs to be a valid async context manager."""

    def __call__(self, *_a: Any, **_kw: Any) -> _FakeTransactionCtx:
        return self

    async def __aenter__(self) -> None:
        return None

    async def __aexit__(self, *exc: Any) -> bool:
        return False


@pytest.fixture
def kgdb(monkeypatch, reset_ext) -> _KgDb:
    db = _KgDb()

    import matrx_rag.ner as ner_mod

    monkeypatch.setattr(ner_mod, "transaction", _FakeTransactionCtx())
    # Inject fake model classes through the db_models override seam so the
    # (now ORM-only) tier-B/C paths run against the in-memory _KgDb.
    _ext.configure(db_models=_make_fake_models(db))
    yield db


class _FixedExtractor:
    """Returns a deterministic entity set keyed on the chunk text. Records the
    chunk texts it was called with so a test can assert a reused chunk never
    reached the extractor."""

    def __init__(self, by_text: dict[str, list[dict[str, Any]]]) -> None:
        self.by_text = by_text
        self.calls: list[str] = []

    async def extract(
        self,
        text,
        *,
        organization_id=None,
        user_id,
        source_kind=None,
        source_id=None,
    ):
        self.calls.append(text)
        return self.by_text.get(text, [])


ORG = "11111111-1111-1111-1111-111111111111"
USER = "22222222-2222-2222-2222-222222222222"


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_no_extractor_is_noop(kgdb):
    from matrx_rag.ner import NerChunkInput, extract_entities

    # No extractor injected → clean no-op.
    res = await extract_entities(
        [NerChunkInput(chunk_id=str(uuid.uuid4()), content_text="Acme Corp called.")],
        organization_id=ORG,
        user_id=USER,
    )
    assert res.skipped_reason == "no_extractor"
    assert res.entities_written == 0
    assert kgdb.entities == {}


@pytest.mark.asyncio
async def test_ner_keeps_at_most_the_bound_in_flight(kgdb, monkeypatch):
    """Tier A runs chunks in parallel up to ``NER_EXTRACT_CONCURRENCY`` and never more.

    Each extraction is an agent run that does database work (request rows, the COPPA
    gate, error capture) before the provider gate paces it; dispatching every chunk at
    once drained the 10-slot pool (``database_pool_saturation``, 2026-11-02, every
    holder in ``_extract_one``)."""
    import matrx_rag.ner as ner_mod
    from matrx_rag.ner import NerChunkInput, extract_entities

    monkeypatch.setattr(ner_mod, "NER_EXTRACT_CONCURRENCY", 3)
    gauge = {"now": 0, "peak": 0, "calls": 0}

    class _SlowExtractor:
        async def extract(self, text: str, **_: Any) -> list[dict[str, Any]]:
            gauge["now"] += 1
            gauge["calls"] += 1
            gauge["peak"] = max(gauge["peak"], gauge["now"])
            await asyncio.sleep(0.01)
            gauge["now"] -= 1
            return []

    _ext.configure(ner_extractor=_SlowExtractor())
    await extract_entities(
        [NerChunkInput(chunk_id=str(uuid.uuid4()), content_text=f"chunk-{i}") for i in range(30)],
        organization_id=ORG,
        user_id=USER,
    )
    assert gauge["calls"] == 30, "every visible chunk is still extracted"
    assert gauge["peak"] <= 3, f"{gauge['peak']} chunks were in flight at once; the bound is 3"
    assert gauge["peak"] >= 2, "chunks must still run in parallel up to the bound"


@pytest.mark.asyncio
async def test_dedup_across_chunks_and_mentions(kgdb):
    from matrx_rag.ner import NerChunkInput, extract_entities

    # Two chunks both mention "Acme Corp". Chunk 1 also mentions a phone, so it
    # has two entities → expect a co_occurs_with edge on chunk 1.
    text1 = "Acme Corp can be reached at 555-1234."
    text2 = "We signed the Acme Corp contract today."
    extractor = _FixedExtractor(
        {
            text1: [
                {
                    "kind": "organization",
                    "canonical_name": "Acme Corp",
                    "span_start": 0,
                    "span_end": 9,
                    "confidence": 0.95,
                },
                {
                    "kind": "phone",
                    "canonical_name": "+15551234",
                    "span_start": 28,
                    "span_end": 36,
                    "confidence": 0.8,
                    "attrs": {"e164": "+15551234"},
                },
            ],
            text2: [
                {
                    "kind": "organization",
                    "canonical_name": "acme corp",
                    "span_start": 14,
                    "span_end": 23,
                    "confidence": 0.9,
                },
            ],
        }
    )
    _ext.configure(ner_extractor=extractor)

    c1 = str(uuid.uuid4())
    c2 = str(uuid.uuid4())
    res = await extract_entities(
        [
            NerChunkInput(chunk_id=c1, content_text=text1),
            NerChunkInput(chunk_id=c2, content_text=text2),
        ],
        organization_id=ORG,
        user_id=USER,
    )

    # Dedup: "Acme Corp" / "acme corp" collapse to ONE entity row (case-
    # insensitive). Plus the phone = 2 distinct entities total.
    org_entities = [e for e in kgdb.entities.values() if e["kind"] == "organization"]
    assert len(org_entities) == 1, "Acme Corp must dedup across chunks (case-insensitive)"
    assert len(kgdb.entities) == 2  # org + phone

    assert res.entities_written == 2  # org + phone created once
    assert res.entities_reused == 1  # chunk2's acme corp deduped onto chunk1's

    # Three mention rows total (org x2 + phone x1), each carrying its span.
    assert len(kgdb.mentions) == 3
    org_id = org_entities[0]["id"]
    org_mentions = [m for m in kgdb.mentions if m["entity_id"] == org_id]
    assert len(org_mentions) == 2
    assert {(m["span_start"], m["span_end"]) for m in org_mentions} == {(0, 9), (14, 23)}

    # confidence_avg maintained (mean of 0.95 and 0.9).
    assert org_entities[0]["confidence_avg"] == pytest.approx((0.95 + 0.9) / 2)

    # co_occurs_with edge for the two entities in chunk1.
    edges = [e for e in kgdb.edges if e["kind"] == "co_occurs_with"]
    assert len(edges) == 1
    assert edges[0]["source_chunk_id"] == c1
    assert res.edges_written == 1


@pytest.mark.asyncio
async def test_reused_chunk_not_re_nerd(kgdb):
    """The cost-reuse contract: the ingest pipeline only hands NEW (inserted)
    chunk ids to NER. A reused chunk's text is never passed in, so the extractor
    is never called for it."""
    from matrx_rag.ner import NerChunkInput, extract_entities

    new_text = "Brand new content about Globex."
    reused_text = "Old unchanged content about Initech."
    extractor = _FixedExtractor(
        {
            new_text: [
                {
                    "kind": "organization",
                    "canonical_name": "Globex",
                    "span_start": 24,
                    "span_end": 30,
                    "confidence": 0.9,
                },
            ],
            reused_text: [
                {
                    "kind": "organization",
                    "canonical_name": "Initech",
                    "span_start": 28,
                    "span_end": 35,
                    "confidence": 0.9,
                },
            ],
        }
    )
    _ext.configure(ner_extractor=extractor)

    # Simulate the pipeline: ONLY the new chunk is handed to NER (the reused one
    # is filtered out upstream by inserted_chunk_ids).
    await extract_entities(
        [NerChunkInput(chunk_id=str(uuid.uuid4()), content_text=new_text)],
        organization_id=ORG,
        user_id=USER,
    )

    assert extractor.calls == [new_text], "only the new chunk should reach the extractor"
    assert reused_text not in extractor.calls
    # Only Globex was created — Initech (the reused chunk) never got re-NER'd.
    names = {e["name"] for e in kgdb.entities.values()}
    assert names == {"Globex"}


@pytest.mark.asyncio
async def test_invisible_chunk_skipped(kgdb):
    from matrx_rag.ner import NerChunkInput, extract_entities

    extractor = _FixedExtractor(
        {
            "hidden": [
                {
                    "kind": "person",
                    "canonical_name": "Ghost",
                    "span_start": 0,
                    "span_end": 5,
                    "confidence": 0.9,
                }
            ]
        }
    )
    _ext.configure(ner_extractor=extractor)

    res = await extract_entities(
        [
            NerChunkInput(
                chunk_id=str(uuid.uuid4()), content_text="hidden", is_visible_to_model=False
            )
        ],
        organization_id=ORG,
        user_id=USER,
    )
    assert res.chunks_skipped == 1
    assert extractor.calls == []
    assert kgdb.entities == {}


@pytest.mark.asyncio
async def test_tier_b_race_falls_back_to_winner(kgdb):
    """Regression for the deadlock-fix refactor.

    Setup: chunk1 tries to create entity ``Acme Corp`` but a parallel
    coordinator (the "racer") already landed the canonical bucket row.

    Expected: tier-B's bulk_upsert hits the kg_entities_ner_canonical_idx
    ON CONFLICT path, resolves to the racer's row, and RETURNING hands back
    the racer's id. Tier-C then writes the mention against THAT id. No new
    entity row, no advisory lock, no deadlock, no orphan.

    This proves the storage-layer-uniqueness-as-source-of-truth path
    actually works — the matrx-orm bulk_upsert pattern this refactor
    landed on (the SELECT→savepoint→23505→re-SELECT dance it replaced is
    gone).
    """
    from matrx_rag.ner import NerChunkInput, extract_entities

    text = "Acme Corp delivered the contract."
    extractor = _FixedExtractor(
        {
            text: [
                {
                    "kind": "organization",
                    "canonical_name": "Acme Corp",
                    "span_start": 0,
                    "span_end": 9,
                    "confidence": 0.9,
                },
            ],
        }
    )
    _ext.configure(ner_extractor=extractor)

    # The racer's row is already committed before our tier-B runs.
    racer_id = "99999999-9999-9999-9999-999999999999"
    kgdb.entities[racer_id] = {
        "id": racer_id,
        "organization_id": ORG,
        "kind": "organization",
        "name": "Acme Corp",
        "attrs": "{}",
        "confidence_avg": None,
    }

    chunk_id = str(uuid.uuid4())
    res = await extract_entities(
        [NerChunkInput(chunk_id=chunk_id, content_text=text)],
        organization_id=ORG,
        user_id=USER,
    )

    # We DID NOT create a new entity — the racer's id was inherited.
    assert len(kgdb.entities) == 1
    assert res.entities_written == 0
    assert res.entities_reused == 1
    # The mention is attached to the RACER's id, not to a freshly-minted one.
    assert len(kgdb.mentions) == 1
    assert kgdb.mentions[0]["entity_id"] == racer_id
    assert kgdb.mentions[0]["chunk_id"] == chunk_id
    # The chunk is marked succeeded — race was handled cleanly.
    assert chunk_id in res.succeeded_chunk_ids
    assert res.errors == []
    # The racer's row was found by a read, never locked by ON CONFLICT DO UPDATE (live 40P01, 2026-11-16).
    assert kgdb.entity_upserts == 0


async def test_tier_b_finds_an_existing_entity_of_another_case_without_locking_it(kgdb):
    """An existing ``ACME CORP`` is the bucket ``(organization, acme corp)``: tier B inserts nothing,
    never asks DO UPDATE (which locked existing rows FOR UPDATE and deadlocked tier C's FK share locks),
    and the mention lands on the existing id."""
    from matrx_rag.ner import NerChunkInput, extract_entities

    text = "Acme Corp and Beta LLC signed."
    _ext.configure(ner_extractor=_FixedExtractor({text: [
        {"kind": "organization", "canonical_name": "Acme Corp", "span_start": 0, "span_end": 9, "confidence": 0.9},
        {"kind": "organization", "canonical_name": "Beta LLC", "span_start": 14, "span_end": 22, "confidence": 0.9},
    ]}))
    existing = "88888888-8888-8888-8888-888888888888"
    kgdb.entities[existing] = {"id": existing, "organization_id": ORG, "kind": "organization",
                               "name": "ACME CORP", "attrs": "{}", "confidence_avg": None}

    chunk_id = str(uuid.uuid4())
    res = await extract_entities([NerChunkInput(chunk_id=chunk_id, content_text=text)],
                                 organization_id=ORG, user_id=USER)

    assert kgdb.entity_upserts == 0
    assert res.errors == []
    assert len(kgdb.entities) == 2
    assert res.entities_written == 1
    assert {m["entity_id"] for m in kgdb.mentions} >= {existing}
    assert chunk_id in res.succeeded_chunk_ids


def test_collapse_overlapping_spans_prefers_higher_confidence():
    """Two GLiNER spans at the SAME position with different kinds collapse
    to one entry — the highest-confidence wins. This is the structural fix
    that prevents the 2026-06-06 ``Postgres-as-organization-AND-concept``
    duplicate-entity bug from re-occurring.
    """
    from matrx_rag.ner import _collapse_overlapping_spans

    spans = [
        {
            "kind": "organization",
            "name": "Postgres",
            "span_start": 546,
            "span_end": 554,
            "confidence": 0.55,
            "attrs": {},
        },
        {
            "kind": "concept",
            "name": "Postgres",
            "span_start": 546,
            "span_end": 554,
            "confidence": 0.51,
            "attrs": {},
        },
    ]
    out = _collapse_overlapping_spans(spans)
    assert len(out) == 1
    assert out[0]["kind"] == "organization"  # higher confidence wins
    assert out[0]["confidence"] == 0.55


def test_collapse_overlapping_spans_keeps_non_overlapping():
    """Two spans for the same surface at DIFFERENT positions are both kept —
    they're distinct mentions, not duplicates. The tier-B bucket layer
    merges them into one entity afterwards.
    """
    from matrx_rag.ner import _collapse_overlapping_spans

    spans = [
        {
            "kind": "concept",
            "name": "Postgres",
            "span_start": 100,
            "span_end": 108,
            "confidence": 0.7,
            "attrs": {},
        },
        {
            "kind": "concept",
            "name": "Postgres",
            "span_start": 200,
            "span_end": 208,
            "confidence": 0.6,
            "attrs": {},
        },
    ]
    out = _collapse_overlapping_spans(spans)
    assert len(out) == 2


def test_collapse_overlapping_spans_tie_break_is_deterministic():
    """When two same-position spans have IDENTICAL confidence, the tie-break
    must be deterministic so re-extraction of the same chunk produces a
    byte-identical norm list (which is how the valid_to-IS-NULL dedup logic
    detects 'this chunk's NER hasn't drifted'). Rule: alphabetical kind,
    then alphabetical name.
    """
    from matrx_rag.ner import _collapse_overlapping_spans

    spans_a = [
        {
            "kind": "organization",
            "name": "Postgres",
            "span_start": 0,
            "span_end": 8,
            "confidence": 0.5,
            "attrs": {},
        },
        {
            "kind": "concept",
            "name": "Postgres",
            "span_start": 0,
            "span_end": 8,
            "confidence": 0.5,
            "attrs": {},
        },
    ]
    spans_b = list(reversed(spans_a))
    out_a = _collapse_overlapping_spans(spans_a)
    out_b = _collapse_overlapping_spans(spans_b)
    assert out_a == out_b
    assert out_a[0]["kind"] == "concept"  # alphabetically first


def test_collapse_overlapping_spans_passes_through_unpositioned():
    """Spans with span_start >= span_end (no valid position) MUST NOT be
    collapsed — some extractors emit source-level entities with no position.
    Over-merging those would silently drop real entities.
    """
    from matrx_rag.ner import _collapse_overlapping_spans

    spans = [
        {
            "kind": "concept",
            "name": "A",
            "span_start": 0,
            "span_end": 0,
            "confidence": 0.8,
            "attrs": {},
        },
        {
            "kind": "concept",
            "name": "B",
            "span_start": 0,
            "span_end": 0,
            "confidence": 0.7,
            "attrs": {},
        },
        {
            "kind": "person",
            "name": "Mendel",
            "span_start": 50,
            "span_end": 56,
            "confidence": 0.9,
            "attrs": {},
        },
    ]
    out = _collapse_overlapping_spans(spans)
    # 2 unpositioned + 1 positioned
    assert len(out) == 3


# ---------------------------------------------------------------------------
# Tier-C lock order + whole-transaction retry (live 40P01, 2026-10-01 22:29Z,
# chunk a59fb1ff…: two concurrent NER runs of the same note deadlocked on
# kg_chunk_entities). Lock order must be the conflict key, and a residual
# deadlock must re-run the whole per-chunk transaction, not drop the chunk.
# ---------------------------------------------------------------------------


def _two_orgs_extractor(text: str) -> _FixedExtractor:
    # Span order (Zeta first) deliberately disagrees with the conflict-key
    # order (acme < zeta), so an unsorted write is visible.
    return _FixedExtractor(
        {
            text: [
                {
                    "kind": "organization",
                    "canonical_name": "Zeta Corp",
                    "span_start": 0,
                    "span_end": 9,
                    "confidence": 0.9,
                },
                {
                    "kind": "organization",
                    "canonical_name": "Acme Corp",
                    "span_start": 20,
                    "span_end": 29,
                    "confidence": 0.9,
                },
                {
                    "kind": "organization",
                    "canonical_name": "Zeta Corp",
                    "span_start": 40,
                    "span_end": 49,
                    "confidence": 0.9,
                },
            ]
        }
    )


@pytest.mark.asyncio
async def test_mentions_are_written_in_conflict_key_order(kgdb):
    """Every concurrent writer must take kg_chunk_entities unique-key locks (and
    the FK KEY SHARE locks on kg_entities) in ONE global order — the tier-B
    bucket order, then span — or two writers of the same chunk cycle (40P01)."""
    from matrx_rag.ner import NerChunkInput, extract_entities

    text = "Zeta Corp met with Acme Corp; Zeta Corp agreed."
    _ext.configure(ner_extractor=_two_orgs_extractor(text))
    seen: list[list[dict[str, Any]]] = []
    import matrx_rag.ner as ner_mod

    real = ner_mod._bulk_insert_mentions

    async def _spy(rows):
        seen.append([dict(r) for r in rows])
        return await real(rows)

    mp = pytest.MonkeyPatch()
    mp.setattr(ner_mod, "_bulk_insert_mentions", _spy)
    try:
        res = await extract_entities(
            [NerChunkInput(chunk_id=str(uuid.uuid4()), content_text=text)],
            organization_id=ORG,
            user_id=USER,
        )
    finally:
        mp.undo()

    assert not res.errors
    assert len(seen) == 1
    by_id = {e["id"]: e["name"].lower() for e in kgdb.entities.values()}
    written = [(by_id[r["entity_id"]], r["span_start"]) for r in seen[0]]
    assert written == [("acme corp", 20), ("zeta corp", 0), ("zeta corp", 40)], written


@pytest.mark.asyncio
async def test_deadlock_reruns_the_whole_chunk_transaction(kgdb, monkeypatch):
    """A 40P01 inside the per-chunk transaction re-runs that transaction; the
    chunk lands, is marked succeeded, and its counters are counted once."""
    from matrx_orm import LockContentionError

    import matrx_rag.ner as ner_mod
    from matrx_rag.ner import NerChunkInput, extract_entities

    text = "Zeta Corp met with Acme Corp; Zeta Corp agreed."
    _ext.configure(ner_extractor=_two_orgs_extractor(text))

    async def _no_sleep(_s):
        return None

    monkeypatch.setattr(asyncio, "sleep", _no_sleep)
    real = ner_mod._bulk_insert_mentions
    calls = {"n": 0}

    async def _deadlock_once(rows):
        calls["n"] += 1
        if calls["n"] == 1:
            raise LockContentionError(original_error="deadlock detected", in_transaction=True)
        return await real(rows)

    monkeypatch.setattr(ner_mod, "_bulk_insert_mentions", _deadlock_once)
    cid = str(uuid.uuid4())
    res = await extract_entities(
        [NerChunkInput(chunk_id=cid, content_text=text)], organization_id=ORG, user_id=USER
    )

    assert calls["n"] == 2
    assert cid in res.succeeded_chunk_ids
    assert not res.errors
    assert len(kgdb.mentions) == 3
    assert res.mentions_written == 3
    assert res.edges_written == 1


@pytest.mark.asyncio
async def test_persist_that_never_heals_leaves_chunk_retryable_and_screams(
    kgdb, monkeypatch, caplog
):
    from matrx_orm import LockContentionError

    import matrx_rag.ner as ner_mod
    from matrx_rag.ner import NerChunkInput, extract_entities

    text = "Zeta Corp met with Acme Corp; Zeta Corp agreed."
    _ext.configure(ner_extractor=_two_orgs_extractor(text))

    async def _no_sleep(_s):
        return None

    monkeypatch.setattr(asyncio, "sleep", _no_sleep)

    async def _always(rows):
        raise LockContentionError(original_error="deadlock detected", in_transaction=True)

    monkeypatch.setattr(ner_mod, "_bulk_insert_mentions", _always)
    cid = str(uuid.uuid4())
    with caplog.at_level("ERROR", logger="matrx_rag.ner"):
        res = await extract_entities(
            [NerChunkInput(chunk_id=cid, content_text=text)], organization_id=ORG, user_id=USER
        )

    assert cid not in res.succeeded_chunk_ids  # ner_extracted_at stays NULL → re-extracted
    assert any(cid in e for e in res.errors)
    assert res.mentions_written == 0 and res.edges_written == 0
    assert any(r.levelname == "ERROR" and cid in r.getMessage() for r in caplog.records)


@pytest.mark.asyncio
async def test_a_chunk_replaced_mid_pass_is_superseded_not_an_error(kgdb, monkeypatch, caplog):
    """Live 2026-11-02 17:04Z: a re-ingest deleted the chunks while NER for them was in flight,
    and 50 inserts died on kg_chunk_entities_chunk_id_fkey as ERRORs left for a re-extraction
    that can never succeed. The chunk is gone: the work is dropped at INFO."""
    import asyncpg

    import matrx_rag.ner as ner_mod
    from matrx_rag.ner import NerChunkInput, extract_entities

    text = "Zeta Corp met with Acme Corp; Zeta Corp agreed."
    _ext.configure(ner_extractor=_two_orgs_extractor(text))

    async def _chunk_gone(rows):
        exc = asyncpg.exceptions.ForeignKeyViolationError("chunk is not present in kg_chunks")
        exc.sqlstate = "23503"
        exc.constraint_name = "kg_chunk_entities_chunk_id_fkey"
        raise exc

    monkeypatch.setattr(ner_mod, "_bulk_insert_mentions", _chunk_gone)
    cid = str(uuid.uuid4())
    with caplog.at_level("INFO", logger="matrx_rag.ner"):
        res = await extract_entities(
            [NerChunkInput(chunk_id=cid, content_text=text)], organization_id=ORG, user_id=USER
        )

    assert res.superseded_chunk_ids == [cid]
    assert not res.errors
    assert cid not in res.succeeded_chunk_ids
    assert not any(r.levelname == "ERROR" and cid in r.getMessage() for r in caplog.records)


# ---------------------------------------------------------------------------
# One source, one NER run at a time: a note save that fires twice must not pay
# the extractor twice for the same chunk (the second run waits, then finds the
# chunk already stamped).
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_two_concurrent_ner_runs_of_one_source_extract_each_chunk_once(kgdb):
    from matrx_rag.ingestion import run_ner_for_source

    chunk_id = str(uuid.uuid4())
    chunk = {
        "id": chunk_id,
        "content_text": "Acme Corp signed today.",
        "organization_id": ORG,
        "created_by": USER,
        "parent_chunk_id": None,
        "ner_extracted_at": None,
    }

    class _ChunkQuery:
        def __init__(self, kw: dict[str, Any]) -> None:
            self.kw = dict(kw)

        def filter(self, **kw: Any) -> _ChunkQuery:
            self.kw.update(kw)
            return self

        def select_for_update(self, **_kw: Any) -> _ChunkQuery:
            return self

        async def values(self, *fields: str) -> list[dict[str, Any]]:
            if self.kw.get("parent_chunk_id__isnull") is False:
                return []
            if self.kw.get("ner_extracted_at__isnull") and chunk["ner_extracted_at"] is not None:
                return []
            return [{f: chunk[f] for f in fields}]

    class _FakeKgChunks:
        @classmethod
        def filter(cls, **kw: Any) -> _ChunkQuery:
            return _ChunkQuery(kw)

        @classmethod
        async def update_where(cls, filters: dict[str, Any], **kw: Any) -> Any:
            if chunk_id in filters.get("id__in", []):
                chunk["ner_extracted_at"] = kw["ner_extracted_at"]
                return SimpleNamespace(rows_affected=1)
            return SimpleNamespace(rows_affected=0)

    models = _make_fake_models(kgdb)
    models["KgChunks"] = _FakeKgChunks
    _ext.configure(db_models=models)

    calls: list[str] = []

    class _SlowExtractor:
        async def extract(self, text, **_kw):
            calls.append(text)
            await asyncio.sleep(0.02)  # both runs are in flight together
            return [
                {
                    "kind": "organization",
                    "canonical_name": "Acme Corp",
                    "span_start": 0,
                    "span_end": 9,
                    "confidence": 0.9,
                }
            ]

    _ext.configure(ner_extractor=_SlowExtractor())

    async def _run():
        return await run_ner_for_source(
            source_kind="note", source_id="n-1", field_id=None, organization_id=ORG, user_id=USER
        )

    first, second = await asyncio.gather(_run(), _run())

    assert len(calls) == 1, f"extractor paid {len(calls)} times for one chunk"
    assert chunk["ner_extracted_at"] is not None
    assert first.state == "done" and second.state == "done"
    assert len(kgdb.mentions) == 1


@pytest.mark.asyncio
async def test_the_ner_stamp_locks_its_chunks_in_id_order(monkeypatch) -> None:
    """Two NER passes and a re-ingest delete each lock many kg_chunks rows in one statement;
    the plan, not the sorted list, decides that order, and three of them deadlocked (40P01,
    2026-11-15 22:24Z). The stamp routes through the ORM's ordered-lock UPDATE."""
    from matrx_rag import ner as ner_mod

    calls: list[dict] = []

    class _Chunks:
        @classmethod
        async def update_where(cls, filters, **kwargs):
            calls.append({"filters": filters, **kwargs})

    monkeypatch.setattr(ner_mod, "get_db_model", lambda _name: _Chunks)
    await ner_mod._stamp_chunks(["c-1", "c-2"], ner_mod.NerEngineStamp(name="e", version="1"))
    assert len(calls) == 1
    assert calls[0]["filters"] == {"id__in": ["c-1", "c-2"]}
    assert calls[0]["lock_rows_in_pk_order"] is True
