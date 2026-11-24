"""Tier-C NER chunk writes share ONE process-wide budget sized from the pool.

database_pool_saturation census (2026-11-01): 9 holders in ``_write_chunk_once``
— the per-call cap of 8 was a fresh semaphore per NER job, so concurrent jobs
multiplied it past the 10-slot pool. Every call now gets the same semaphore,
never larger than ``NER_PERSIST_POOL_SHARE`` of the pool.
"""

from __future__ import annotations

from matrx_orm import pool_fanout_limit, reset_fanout_slots

from matrx_rag import ner


async def test_every_ner_job_gets_the_same_pool_sized_slots():
    reset_fanout_slots()
    first = ner._ner_persist_slots()
    second = ner._ner_persist_slots()
    assert first is second
    budget = pool_fanout_limit(
        ner.PACKAGE_DB_NAME, share=ner.NER_PERSIST_POOL_SHARE, ceiling=ner.NER_PERSIST_CONCURRENCY
    )
    assert first._value == budget
    assert budget <= ner.NER_PERSIST_CONCURRENCY
    reset_fanout_slots()
