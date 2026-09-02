"""Run-over-run diff — the canonical replacement for the legacy `site_run_diffs`.

Two things get proven here, and they are the two things that actually break.

1. **The comparison itself** (`compute_diff`) — added / removed / returned /
   changed, the status-direction classification, and the rule that COUNTS stay
   complete when the arrays are capped. A diff that under-reports silently is
   worse than no diff: it reads as "nothing changed".

2. **The page-set derivation** (`build_session_pages`) — that a diff is built
   from `web.crawl_url` (every attempted URL) and not `web.snapshot`
   (successful captures only), and that aliases are flattened through
   `canonical_page_id`. Both are regressions that produce a *plausible* diff:
   a snapshot-only diff loses every 200→404 transition, and an unflattened one
   reports the same page as added AND removed.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_scraper.web_crawl import diff as D
from matrx_scraper.web_crawl.contracts import CrawlSessionRef

T0 = datetime(2026, 8, 1, tzinfo=UTC)
T1 = T0 + timedelta(days=1)
T2 = T0 + timedelta(days=2)


def state(
    key: str,
    *,
    url: str | None = None,
    status: int | None = 200,
    title: str | None = "T",
    meta: str | None = "M",
    content_hash: str | None = "h",
    words: int | None = 100,
    first_seen: datetime | None = T0,
) -> D.PageState:
    return D.PageState(
        page_id=key,
        url=url or f"https://example.com/{key}",
        first_seen=first_seen,
        http_status=status,
        title=title,
        meta_description=meta,
        content_hash=content_hash,
        word_count=words,
    )


def pages(*states: D.PageState, session_id: str = "s", truncated: bool = False) -> D.SessionPages:
    return D.SessionPages(
        session_id=session_id,
        pages={s.page_id: s for s in states},
        truncated=truncated,
    )


def ref(session_id: str) -> CrawlSessionRef:
    return CrawlSessionRef(session_id=session_id, site_id="site", status="completed")


def run_diff(base: D.SessionPages | None, compare: D.SessionPages, *, boundary=T1):
    return D.compute_diff(
        site_id="site",
        base=base,
        compare=compare,
        base_ref=ref("base") if base is not None else None,
        compare_ref=ref("compare"),
        boundary=boundary,
    )


# ---------------------------------------------------------------------------
# The comparison


def test_added_removed_unchanged():
    result = run_diff(pages(state("a"), state("b")), pages(state("a"), state("c")))
    assert result.counts.pages_added == 1
    assert result.counts.pages_removed == 1
    assert result.counts.pages_unchanged == 1
    assert result.counts.pages_changed == 0
    assert [p.page_id for p in result.added] == ["c"]
    assert [p.page_id for p in result.removed] == ["b"]


def test_first_crawl_has_no_base_and_reports_everything_added():
    result = run_diff(None, pages(state("a"), state("b")), boundary=T0)
    assert result.base is None
    assert result.counts.pages_added == 2
    assert result.counts.pages_removed == 0
    assert result.counts.pages_changed == 0


@pytest.mark.parametrize(
    "field,before,after",
    [
        ("title", "Old", "New"),
        ("meta_description", "Old", "New"),
        ("content_hash", "h1", "h2"),
        ("word_count", 100, 250),
        ("http_status", 200, 404),
    ],
)
def test_each_compared_field_is_a_change(field: str, before: Any, after: Any):
    kw_before = {"a": before}
    kw_after = {"a": after}
    key = {
        "title": "title",
        "meta_description": "meta",
        "content_hash": "content_hash",
        "word_count": "words",
        "http_status": "status",
    }[field]
    result = run_diff(
        pages(state("a", **{key: kw_before["a"]})),
        pages(state("a", **{key: kw_after["a"]})),
    )
    assert result.counts.pages_changed == 1
    assert result.counts.pages_unchanged == 0
    assert result.changed[0].changed_fields == [field]
    assert getattr(result.changed[0], f"{field}_before") == before
    assert getattr(result.changed[0], f"{field}_after") == after


def test_content_hash_change_alone_is_reported():
    """The legacy DB reconcile function compared only status/title/word_count,
    so a rewritten page that kept its title and length looked UNCHANGED."""

    result = run_diff(pages(state("a", content_hash="h1")), pages(state("a", content_hash="h2")))
    assert result.counts.pages_changed == 1
    assert result.changed[0].changed_fields == ["content_hash"]


@pytest.mark.parametrize(
    "before,after,worse,better",
    [
        (200, 404, 1, 0),
        (301, 500, 1, 0),
        (404, 200, 0, 1),
        (200, 301, 0, 0),  # a redirect is a change, not a regression
        (404, 410, 0, 0),  # still broken, no direction
        (None, 404, 0, 0),  # never observed before — no direction to claim
        (200, None, 0, 0),
    ],
)
def test_status_direction(before: int | None, after: int | None, worse: int, better: int):
    result = run_diff(pages(state("a", status=before)), pages(state("a", status=after)))
    assert result.counts.pages_changed == 1
    assert result.counts.pages_status_worse == worse
    assert result.counts.pages_status_better == better


def test_returned_is_an_added_page_the_site_already_knew():
    result = run_diff(
        pages(state("a")),
        pages(state("a"), state("back", first_seen=T0), state("brand-new", first_seen=T2)),
        boundary=T1,
    )
    assert result.counts.pages_added == 2
    assert result.counts.pages_returned == 1
    assert [p.page_id for p in result.returned] == ["back"]


def test_a_first_crawl_reports_nothing_as_returned():
    """With no base run there is nothing to have returned FROM. Passing the
    compare session's own start as the boundary instead would label every page
    a prior sitemap sync had already created "returned" — 41 of 41 on a real
    site, which is noise presented as a finding.
    """

    result = run_diff(None, pages(state("a", first_seen=T0)), boundary=None)
    assert result.counts.pages_added == 1
    assert result.counts.pages_returned == 0


def test_counts_stay_complete_when_arrays_are_capped(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(D, "MAX_LIST_ITEMS", 2)
    compare = pages(*[state(f"p{i:03d}") for i in range(10)])
    result = run_diff(pages(), compare)
    assert result.counts.pages_added == 10
    assert len(result.added) == 2
    assert result.truncated is True


def test_a_truncated_session_scan_taints_the_diff():
    result = run_diff(pages(state("a")), pages(state("a"), truncated=True))
    assert result.truncated is True


def test_untruncated_diff_says_so():
    result = run_diff(pages(state("a")), pages(state("a"), state("b")))
    assert result.truncated is False


# ---------------------------------------------------------------------------
# Session selection


def session(
    session_id: str,
    *,
    mode: str | None = "full",
    finished_at: datetime | None = None,
    started_at: datetime | None = None,
    created_at: datetime = T0,
    site_id: str = "site",
    status: str = "completed",
    stats: dict[str, Any] | None = None,
) -> Any:
    return SimpleNamespace(
        id=session_id,
        site_id=site_id,
        status=status,
        stats=stats or {},
        scope={"mode": mode} if mode is not None else {},
        started_at=started_at,
        finished_at=finished_at,
        created_at=created_at,
    )


@pytest.mark.parametrize(
    "mode,expected",
    [("full", True), ("list", True), ("page_fetch", False), ("gsc_sync", False), (None, False)],
)
def test_only_site_wide_crawls_are_diff_baselines(mode: str | None, expected: bool):
    assert D.is_diffable(session("s", mode=mode)) is expected


def test_session_ran_at_falls_back_through_started_then_created():
    assert D.session_ran_at(session("s", finished_at=T2, started_at=T1, created_at=T0)) == T2
    assert D.session_ran_at(session("s", started_at=T1, created_at=T0)) == T1
    assert D.session_ran_at(session("s", created_at=T0)) == T0


@pytest.mark.asyncio
async def test_previous_session_skips_page_fetches_and_later_runs(monkeypatch):
    current = session("cur", finished_at=T2)
    candidates = [
        session("later", finished_at=T2 + timedelta(days=1)),
        current,
        session("a-page-fetch", mode="page_fetch", finished_at=T1 + timedelta(hours=1)),
        session("want", finished_at=T1),
        session("older", finished_at=T0),
    ]
    _patch_all(monkeypatch, D.WebCrawlSession, candidates)
    assert (await D._resolve_previous(current)).id == "want"


@pytest.mark.asyncio
async def test_previous_session_is_none_on_a_first_crawl(monkeypatch):
    current = session("cur", finished_at=T2)
    _patch_all(monkeypatch, D.WebCrawlSession, [current, session("pf", mode="page_fetch")])
    assert await D._resolve_previous(current) is None


# ---------------------------------------------------------------------------
# Page-set derivation from the ledger


class _FakeQB:
    def __init__(self, rows: list[Any], calls: list[Any], *, values_rows=None):
        self._rows = rows
        self._values_rows = values_rows
        self._calls = calls

    def order_by(self, *terms):
        return self

    def limit(self, n):
        return self

    async def all(self):
        return self._rows

    async def values(self, *fields):
        return self._values_rows or []


def _patch_all(monkeypatch: pytest.MonkeyPatch, model: Any, rows: list[Any]) -> list[Any]:
    """Make `model.filter(...).…all()` return `rows`, recording the filters."""

    calls: list[dict[str, Any]] = []

    def _filter(cls, *args, **kwargs):
        calls.append(kwargs)
        matched = rows
        if "id__in" in kwargs:
            wanted = set(kwargs["id__in"])
            matched = [row for row in rows if str(row.id) in wanted]
        return _FakeQB(matched, calls)

    monkeypatch.setattr(model, "filter", classmethod(_filter), raising=False)
    return calls


def _patch_ledger(monkeypatch: pytest.MonkeyPatch, by_session: dict[str, list[dict[str, Any]]]):
    calls: list[dict[str, Any]] = []

    def _filter(cls, *args, **kwargs):
        calls.append(kwargs)
        rows = by_session.get(str(kwargs.get("session_id")), [])
        if kwargs.get("sequence__gt") is not None:
            rows = [r for r in rows if r["sequence"] > kwargs["sequence__gt"]]
        return _FakeQB([], calls, values_rows=rows)

    monkeypatch.setattr(D.WebCrawlUrl, "filter", classmethod(_filter), raising=False)
    return calls


def page_row(page_id: str, url: str, *, canonical: str | None = None, first_seen=T0) -> Any:
    return SimpleNamespace(
        id=page_id, url=url, canonical_page_id=canonical or page_id, first_seen=first_seen
    )


def snapshot_row(snapshot_id: str, *, title="T", meta="M", content_hash="h", words=100) -> Any:
    return SimpleNamespace(
        id=snapshot_id,
        head_tags={"title": title, "meta_description": meta},
        content_hash=content_hash,
        word_count=words,
    )


def ledger(page_id: str, *, sequence: int, status: int | None, snapshot: str | None) -> dict:
    return {
        "page_id": page_id,
        "snapshot_id": snapshot,
        "http_status": status,
        "sequence": sequence,
    }


@pytest.mark.asyncio
async def test_failed_fetch_with_no_snapshot_still_appears_with_its_status(monkeypatch):
    """The whole reason the diff reads `web.crawl_url` and not `web.snapshot`.

    A page that 404s writes NO snapshot. Diffing snapshots would drop it from
    the current run entirely — reporting "removed" instead of "broke", and
    losing `pages_status_worse` outright.
    """

    _patch_ledger(
        monkeypatch,
        {
            "old": [ledger("p1", sequence=1, status=200, snapshot="sn1")],
            "new": [ledger("p1", sequence=1, status=404, snapshot=None)],
        },
    )
    _patch_all(monkeypatch, D.WebPage, [page_row("p1", "https://example.com/x")])
    _patch_all(monkeypatch, D.WebSnapshot, [snapshot_row("sn1")])

    loaded = await D.build_session_pages(["old", "new"])
    result = D.compute_diff(
        site_id="site",
        base=loaded["old"],
        compare=loaded["new"],
        base_ref=ref("old"),
        compare_ref=ref("new"),
        boundary=T1,
    )
    assert result.counts.pages_removed == 0
    assert result.counts.pages_changed == 1
    assert result.counts.pages_status_worse == 1
    assert loaded["new"].pages["p1"].http_status == 404


@pytest.mark.asyncio
async def test_only_attempted_outcomes_count_as_presence(monkeypatch):
    calls = _patch_ledger(monkeypatch, {"s": []})
    _patch_all(monkeypatch, D.WebPage, [])
    _patch_all(monkeypatch, D.WebSnapshot, [])

    await D.build_session_pages(["s"])
    assert calls[0]["outcome__in"] == sorted(D.ATTEMPTED_OUTCOMES)
    assert calls[0]["page_id__isnull"] is False
    assert "discovered" not in calls[0]["outcome__in"]
    assert "duplicate" not in calls[0]["outcome__in"]


@pytest.mark.asyncio
async def test_aliases_collapse_to_one_canonical_page(monkeypatch):
    """Two spellings of one URL must not diff as added + removed."""

    _patch_ledger(
        monkeypatch,
        {
            "old": [ledger("canon", sequence=1, status=200, snapshot="sn1")],
            # Next run reached the same page through its alias row instead.
            "new": [ledger("alias", sequence=1, status=200, snapshot="sn1")],
        },
    )
    _patch_all(
        monkeypatch,
        D.WebPage,
        [
            page_row("canon", "https://example.com/x"),
            page_row("alias", "https://example.com/X/", canonical="canon"),
        ],
    )
    _patch_all(monkeypatch, D.WebSnapshot, [snapshot_row("sn1")])

    loaded = await D.build_session_pages(["old", "new"])
    assert set(loaded["new"].pages) == {"canon"}
    assert loaded["new"].pages["canon"].url == "https://example.com/x"

    result = D.compute_diff(
        site_id="site",
        base=loaded["old"],
        compare=loaded["new"],
        base_ref=ref("old"),
        compare_ref=ref("new"),
        boundary=T1,
    )
    assert result.counts.pages_added == 0
    assert result.counts.pages_removed == 0
    assert result.counts.pages_unchanged == 1


@pytest.mark.asyncio
async def test_the_last_decision_for_a_page_wins(monkeypatch):
    """A retried URL has several ledger rows in one session; the diff must use
    the final one, matching the legacy `DISTINCT ON ... ORDER BY fetched_at`."""

    _patch_ledger(
        monkeypatch,
        {
            "s": [
                ledger("p1", sequence=1, status=500, snapshot=None),
                ledger("p1", sequence=2, status=200, snapshot="sn1"),
            ]
        },
    )
    _patch_all(monkeypatch, D.WebPage, [page_row("p1", "https://example.com/x")])
    _patch_all(monkeypatch, D.WebSnapshot, [snapshot_row("sn1", title="Final")])

    loaded = await D.build_session_pages(["s"])
    assert loaded["s"].pages["p1"].http_status == 200
    assert loaded["s"].pages["p1"].title == "Final"


@pytest.mark.asyncio
async def test_oversized_session_is_marked_truncated_not_silently_clipped(monkeypatch):
    monkeypatch.setattr(D, "MAX_PAGES_PER_SESSION", 2)
    monkeypatch.setattr(D, "LEDGER_BATCH_SIZE", 10)
    _patch_ledger(
        monkeypatch,
        {"s": [ledger(f"p{i}", sequence=i, status=200, snapshot=None) for i in range(1, 6)]},
    )
    _patch_all(
        monkeypatch,
        D.WebPage,
        [page_row(f"p{i}", f"https://example.com/{i}") for i in range(1, 6)],
    )
    _patch_all(monkeypatch, D.WebSnapshot, [])

    loaded = await D.build_session_pages(["s"])
    assert loaded["s"].truncated is True
    assert len(loaded["s"].pages) == 2


@pytest.mark.asyncio
async def test_snapshot_metadata_lands_on_the_page_state(monkeypatch):
    _patch_ledger(monkeypatch, {"s": [ledger("p1", sequence=1, status=200, snapshot="sn1")]})
    _patch_all(monkeypatch, D.WebPage, [page_row("p1", "https://example.com/x")])
    _patch_all(
        monkeypatch,
        D.WebSnapshot,
        [snapshot_row("sn1", title="Hello", meta="Desc", content_hash="abc", words=42)],
    )

    loaded = await D.build_session_pages(["s"])
    page_state = loaded["s"].pages["p1"]
    assert (page_state.title, page_state.meta_description) == ("Hello", "Desc")
    assert (page_state.content_hash, page_state.word_count) == ("abc", 42)


def test_session_ref_carries_the_runs_own_stats():
    """`list_site_diffs` rendered a history table from one call — the run's
    self-reported fetched/failed counts travel with the diff so it still can."""

    built = D.session_ref(
        session("s", finished_at=T1, stats={"pages_fetched": 120, "pages_failed": 3}),
        page_count=118,
    )
    assert (built.pages, built.pages_fetched, built.pages_failed) == (118, 120, 3)
    assert built.mode == "full"


def test_session_ref_tolerates_a_statless_session():
    built = D.session_ref(session("s"))
    assert built.pages_fetched is None and built.pages_failed is None
