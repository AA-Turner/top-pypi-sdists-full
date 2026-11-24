"""``clean_pdf_pages`` keeps at most ``concurrency`` pages in flight.

The incident (2026-10-27 .. 2026-11-03): ``concurrency`` was accepted and ignored,
so a long PDF started every page at once. Each page does database work around its
provider call (request rows, error capture, ``persist_one``) before the provider
gate can pace it, and the pages drained the process's 10-slot database pool —
the top holder in every ``database_pool_saturation`` census was this function.
"""

from __future__ import annotations

import asyncio


import matrx_rag.llm as llm_mod
from matrx_rag.llm import clean_pdf_pages


def _install_slow_cleaner(monkeypatch, gauge: dict[str, int]) -> None:
    class _Runner:
        async def clean_page(self, raw: str, *, timeout: float | None = None):
            gauge["now"] += 1
            gauge["peak"] = max(gauge["peak"], gauge["now"])
            await asyncio.sleep(0.01)
            gauge["now"] -= 1
            return {"text": f"cleaned:{raw}", "section_kind": "letter"}

    monkeypatch.setattr(llm_mod, "_require_runner", lambda: _Runner())


def test_pages_in_flight_never_exceed_concurrency(monkeypatch):
    gauge = {"now": 0, "peak": 0}
    _install_slow_cleaner(monkeypatch, gauge)
    persisted: list[int] = []

    async def _persist(idx, _cleaned):
        persisted.append(idx)

    pages = [f"p{i}" for i in range(40)]
    out = asyncio.run(clean_pdf_pages(pages, concurrency=3, persist_one=_persist))

    assert gauge["peak"] <= 3, f"{gauge['peak']} pages were in flight at once; the bound is 3"
    assert gauge["peak"] >= 2, "pages must still run in parallel up to the bound"
    assert [p.text for p in out] == [f"cleaned:{p}" for p in pages]
    assert sorted(persisted) == list(range(40))


def test_a_nonsense_concurrency_still_runs_one_at_a_time(monkeypatch):
    gauge = {"now": 0, "peak": 0}
    _install_slow_cleaner(monkeypatch, gauge)
    out = asyncio.run(clean_pdf_pages(["a", "b", "c"], concurrency=0))
    assert gauge["peak"] == 1
    assert [p.text for p in out] == ["cleaned:a", "cleaned:b", "cleaned:c"]
