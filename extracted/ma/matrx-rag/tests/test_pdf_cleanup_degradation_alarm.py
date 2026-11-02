"""PDF cleanup that falls back to RAW text must SCREAM in aggregate.

The incident this locks down (2026-07-11): ingest runs from a detached task
with no ambient AppContext, so EVERY ``rag_pdf_page_cleaner`` agent call died
instantly with "No AppContext is set". ``clean_pdf_text`` caught each one,
logged a per-page WARNING, and returned the RAW text. The run then chunked and
embedded that raw text and reported success. Nothing 500'd; the corpus just
silently got worse, one PDF at a time.

Per-page fallback is CORRECT (a raw page beats a dropped page). Per-page
silence is not. The fallback must be counted and alarmed on.
"""

from __future__ import annotations

import asyncio

import matrx_rag.llm as llm_mod
from matrx_rag.llm import CleanedPage, clean_pdf_pages


def _install_cleaner(monkeypatch, *, fail_indexes: set[int] | None = None) -> None:
    """Stub the host-injected cleaner runner; fail the requested page bodies."""
    fail = fail_indexes if fail_indexes is not None else set()
    seen: list[str] = []

    class _Runner:
        async def clean_page(self, raw: str, *, timeout: float | None = None):
            idx = int(raw.split("-")[1])
            seen.append(raw)
            if idx in fail:
                raise RuntimeError(
                    "No AppContext is set. Ensure AuthMiddleware is registered "
                    "and running before this code path."
                )
            return {"text": f"cleaned-{idx}", "section_kind": "letter"}

    monkeypatch.setattr(llm_mod, "_require_runner", lambda: _Runner())


def _capture_banners(monkeypatch) -> list[str]:
    banners: list[str] = []
    monkeypatch.setattr(
        llm_mod, "vcprint", lambda *a, **kw: banners.append(str(kw.get("title", "")))
    )
    return banners


def test_total_cleanup_failure_screams_and_marks_pages_degraded(monkeypatch):
    """Every page failed ⇒ a WIRING bug. One loud banner naming it, and every
    returned page flagged ``degraded`` so no caller can mistake raw text for
    cleaned text."""
    pages = [f"page-{i}" for i in range(4)]
    _install_cleaner(monkeypatch, fail_indexes={0, 1, 2, 3})
    banners = _capture_banners(monkeypatch)

    out = asyncio.run(clean_pdf_pages(pages, concurrency=2))

    # The page still flows downstream, carrying its RAW text — never dropped.
    assert [p.text for p in out] == pages
    assert all(p.degraded for p in out)

    assert len(banners) == 1, f"expected exactly one alarm, got {banners}"
    assert "TOTAL FAILURE" in banners[0]


def test_partial_cleanup_failure_screams_but_keeps_the_good_pages(monkeypatch):
    """A few pages failed ⇒ still an alarm (embedding raw text is a quality
    regression), but the pages that DID clean keep their cleaned text."""
    pages = [f"page-{i}" for i in range(4)]
    _install_cleaner(monkeypatch, fail_indexes={2})
    banners = _capture_banners(monkeypatch)

    out = asyncio.run(clean_pdf_pages(pages, concurrency=4))

    assert out[0].text == "cleaned-0" and not out[0].degraded
    assert out[2].text == "page-2" and out[2].degraded

    assert len(banners) == 1
    assert "DEGRADED" in banners[0]
    assert "TOTAL FAILURE" not in banners[0]


def test_clean_run_is_silent(monkeypatch):
    """The alarm must not fire when nothing degraded — a guard that cries wolf
    on a healthy run is a guard everyone learns to ignore."""
    pages = [f"page-{i}" for i in range(3)]
    _install_cleaner(monkeypatch, fail_indexes=set())
    banners = _capture_banners(monkeypatch)

    out = asyncio.run(clean_pdf_pages(pages, concurrency=3))

    assert [p.text for p in out] == ["cleaned-0", "cleaned-1", "cleaned-2"]
    assert not any(p.degraded for p in out)
    assert banners == []


def test_skipped_pages_are_not_counted_as_degraded(monkeypatch):
    """Resume path: pages skipped because they were cleaned in an earlier run
    carry a raw-text placeholder by design. They are NOT failures and must not
    trip the alarm — otherwise every resumed run would false-alarm."""
    pages = [f"page-{i}" for i in range(3)]
    _install_cleaner(monkeypatch, fail_indexes=set())
    banners = _capture_banners(monkeypatch)

    out = asyncio.run(clean_pdf_pages(pages, concurrency=3, skip_indexes={0, 1}))

    assert isinstance(out[0], CleanedPage)
    assert not out[0].degraded
    assert banners == []


def test_cleanup_dispatches_whole_batch_even_with_legacy_concurrency_one(monkeypatch):
    async def scenario() -> None:
        entered = 0
        all_entered = asyncio.Event()
        release = asyncio.Event()

        async def fake_clean(raw: str) -> CleanedPage:
            nonlocal entered
            entered += 1
            if entered == 12:
                all_entered.set()
            await release.wait()
            return CleanedPage(text=f"cleaned-{raw}")

        monkeypatch.setattr(llm_mod, "clean_pdf_text", fake_clean)
        task = asyncio.create_task(
            clean_pdf_pages([f"page-{i}" for i in range(12)], concurrency=1)
        )
        await asyncio.wait_for(all_entered.wait(), timeout=0.5)
        assert entered == 12
        release.set()
        await task

    asyncio.run(scenario())
