"""URL verification sweep — the HEAD/GET fallback, the content-type vocabulary,
and the crash-safety guarantee.

The chaos test at the bottom is the one that matters: it kills a worker mid-run
(claimed items left unsettled, exactly what a deploy/OOM does) and asserts the
job still finishes with zero dropped and zero duplicated items.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta

import httpx
import pytest

pytest.importorskip("matrx_runtime")

from matrx_runtime import WorkItemState  # noqa: E402
from matrx_runtime.store import InMemoryExecutionStore  # noqa: E402
from matrx_utils.web_page_class import (  # noqa: E402
    UNKNOWN_CONTENT_TYPES,
    is_machine_resource,
)

from matrx_scraper.scraper import ContentType, content_type_from_header  # noqa: E402
from matrx_scraper.web_crawl import url_verify  # noqa: E402
from matrx_scraper.web_crawl.url_verify import (  # noqa: E402
    NO_RESPONSE_STATUS,
    UNKNOWN_CONTENT_TYPE,
    PoliteVerifier,
    VerificationSummary,
    classify_status,
    run_frontier,
    seed_frontier,
)

EXEC = "verify-exec-1"


# ---------------------------------------------------------------------------
# Content-type vocabulary — the sweep MUST land on the crawler's tokens


@pytest.mark.parametrize(
    ("header", "expected"),
    [
        ("text/html; charset=utf-8", ContentType.HTML),
        ("TEXT/HTML", ContentType.HTML),
        ("application/xhtml+xml", ContentType.HTML),
        ("application/pdf", ContentType.PDF),
        ("application/json", ContentType.JSON),
        ("application/ld+json", ContentType.JSON),
        ("application/xml", ContentType.XML),
        ("text/xml; charset=utf-8", ContentType.XML),
        ("application/rss+xml", ContentType.XML),
        ("text/plain", ContentType.PLAIN_TEXT),
        ("image/webp", ContentType.IMAGE),
        ("text/markdown", ContentType.MARKDOWN),
    ],
)
def test_header_maps_to_the_crawlers_own_token(header, expected) -> None:
    assert content_type_from_header(header) is expected


@pytest.mark.parametrize("header", [None, "", "application/octet-stream", "garbage"])
def test_unrecognised_header_is_none_never_a_guess(header) -> None:
    """None means "the response did not tell us" — the sweep writes `unknown`,
    which the classifier treats as no signal. Guessing here would let a header
    the platform does not understand hide a real page."""
    assert content_type_from_header(header) is None


def test_unknown_token_is_not_a_machine_resource_signal() -> None:
    assert UNKNOWN_CONTENT_TYPE in UNKNOWN_CONTENT_TYPES
    # A verified-but-untyped ordinary URL stays a page...
    assert is_machine_resource("https://x.test/about", UNKNOWN_CONTENT_TYPE) is False
    # ...while URL shape still decides on its own.
    assert is_machine_resource("https://x.test/a.pdf", UNKNOWN_CONTENT_TYPE) is True


def test_the_token_written_matches_the_crawlers_column_vocabulary() -> None:
    """Both writers of `web.page.content_type_last` must speak one language."""
    for header, token in [
        ("text/html", "html"),
        ("application/pdf", "pdf"),
        ("application/json", "json"),
        ("image/png", "image"),
    ]:
        assert str(content_type_from_header(header)) == token


# ---------------------------------------------------------------------------
# HEAD → ranged-GET fallback


def _client(handler) -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=httpx.MockTransport(handler), follow_redirects=True)


@pytest.fixture(autouse=True)
def _no_dns(monkeypatch):
    """The SSRF guard does real DNS; these hosts are fictional. Tests that want
    the guard's behaviour override this explicitly."""

    async def _ok(url: str) -> str:
        return url

    monkeypatch.setattr(url_verify, "validate_public_http_url", _ok)


@pytest.mark.asyncio
async def test_head_answer_is_used_when_the_server_allows_head() -> None:
    seen: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request.method)
        return httpx.Response(200, headers={"content-type": "text/html"})

    async with _client(handler) as http:
        outcome = await PoliteVerifier(http, per_host_spacing_s=0).verify("https://x.test/a")

    assert seen == ["HEAD"], "a working HEAD must not be followed by a GET"
    assert outcome.http_status == 200
    assert outcome.content_type == "html"
    assert outcome.method == "HEAD"


@pytest.mark.parametrize("status", sorted(url_verify.HEAD_FALLBACK_STATUSES))
async def test_head_rejection_falls_back_to_a_ranged_get(status) -> None:
    """405 (and friends) mean "this host dislikes HEAD", not "this URL is
    broken" — recording the rejection as the URL's status is the whole bug."""
    seen: list[tuple[str, str | None]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append((request.method, request.headers.get("range")))
        if request.method == "HEAD":
            return httpx.Response(status)
        return httpx.Response(206, headers={"content-type": "application/pdf"})

    async with _client(handler) as http:
        outcome = await PoliteVerifier(http, per_host_spacing_s=0).verify("https://x.test/doc")

    assert [m for m, _ in seen] == ["HEAD", "GET"]
    assert seen[1][1] == "bytes=0-0", "the fallback must not download a body"
    assert outcome.http_status == 206
    assert outcome.content_type == "pdf"
    assert outcome.method == "GET"


@pytest.mark.asyncio
async def test_head_transport_error_falls_back_to_get() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "HEAD":
            raise httpx.ConnectError("head not supported")
        return httpx.Response(200, headers={"content-type": "text/html"})

    async with _client(handler) as http:
        outcome = await PoliteVerifier(http, per_host_spacing_s=0).verify("https://x.test/a")
    assert outcome.http_status == 200
    assert outcome.method == "GET"


@pytest.mark.asyncio
async def test_a_real_404_is_recorded_not_retried() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, headers={"content-type": "text/html"})

    async with _client(handler) as http:
        outcome = await PoliteVerifier(http, per_host_spacing_s=0).verify("https://x.test/gone")
    # 404 is not in the HEAD-fallback set: it is a terminal answer about the URL.
    assert outcome.http_status == 404
    assert outcome.retryable is False


@pytest.mark.asyncio
async def test_no_response_records_zero_not_a_fake_status() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectTimeout("dead host")

    async with _client(handler) as http:
        outcome = await PoliteVerifier(http, per_host_spacing_s=0).verify("https://dead.test/a")
    assert outcome.http_status == NO_RESPONSE_STATUS
    assert outcome.content_type is None
    assert outcome.retryable is True


@pytest.mark.asyncio
async def test_missing_content_type_yields_unknown_never_a_guess() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200)

    async with _client(handler) as http:
        outcome = await PoliteVerifier(http, per_host_spacing_s=0).verify("https://x.test/a")
    assert outcome.http_status == 200
    assert outcome.content_type is None


@pytest.mark.asyncio
async def test_redirect_is_followed_and_both_ends_are_recorded() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/old":
            return httpx.Response(301, headers={"location": "https://x.test/new"})
        return httpx.Response(200, headers={"content-type": "text/html"})

    async with _client(handler) as http:
        outcome = await PoliteVerifier(http, per_host_spacing_s=0).verify("https://x.test/old")

    # The FINAL status goes in http_status_last (the crawler's meaning), and the
    # hop that makes this a sitemap finding is kept as evidence.
    assert outcome.http_status == 200
    assert outcome.redirected is True
    assert outcome.hop_status == 301
    assert outcome.final_url == "https://x.test/new"
    assert outcome.redirect_is_material is True


@pytest.mark.parametrize(
    ("requested", "final"),
    [
        # Our stored identity strips the trailing slash, so a slash-serving
        # site 301s EVERY stored URL to itself.
        ("https://x.test/about", "https://x.test/about/"),
        # www and scheme are alias forms too — `url_match_key` owns that list.
        ("https://x.test/about", "https://www.x.test/about"),
        ("http://x.test/about", "https://x.test/about"),
    ],
)
@pytest.mark.asyncio
async def test_a_redirect_to_our_own_url_in_another_dress_is_not_a_finding(
    requested, final
) -> None:
    """Live proof this matters: 422 of www.pbw-law.com's 429 URLs "redirected",
    every one a bare trailing-slash 301 to itself. Reporting those would tell a
    customer their entire sitemap is broken when nothing is wrong — and the
    Identity Contract forbids it ("a redirect is not reported as a finding until
    we have confirmed we requested the canonical form")."""

    def handler(request: httpx.Request) -> httpx.Response:
        if str(request.url) == requested:
            return httpx.Response(301, headers={"location": final})
        return httpx.Response(200, headers={"content-type": "text/html"})

    async with _client(handler) as http:
        outcome = await PoliteVerifier(http, per_host_spacing_s=0).verify(requested)

    assert outcome.redirected is True, "the hop is still recorded as a raw fact"
    assert outcome.redirect_is_material is False, "…but it is NOT a finding"


@pytest.mark.asyncio
async def test_a_redirect_to_a_different_page_is_a_finding() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/old-product":
            return httpx.Response(301, headers={"location": "https://x.test/catalog"})
        return httpx.Response(200, headers={"content-type": "text/html"})

    async with _client(handler) as http:
        outcome = await PoliteVerifier(http, per_host_spacing_s=0).verify(
            "https://x.test/old-product"
        )
    assert outcome.redirect_is_material is True


@pytest.mark.asyncio
async def test_ssrf_rejection_never_issues_a_request(monkeypatch) -> None:
    async def _reject(url: str) -> str:
        raise ValueError("URL host resolves to a non-public IP address")

    monkeypatch.setattr(url_verify, "validate_public_http_url", _reject)
    calls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(str(request.url))
        return httpx.Response(200)

    async with _client(handler) as http:
        outcome = await PoliteVerifier(http, per_host_spacing_s=0).verify(
            "http://169.254.169.254/latest/meta-data/"
        )

    assert calls == [], "the guard must fire BEFORE any bytes leave the box"
    assert outcome.method == "none"
    assert outcome.http_status == NO_RESPONSE_STATUS


@pytest.mark.asyncio
async def test_per_host_spacing_is_enforced() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html"})

    async with _client(handler) as http:
        verifier = PoliteVerifier(http, concurrency=4, per_host_spacing_s=0.05)
        start = asyncio.get_running_loop().time()
        await asyncio.gather(*(verifier.verify(f"https://same.test/{i}") for i in range(4)))
        elapsed = asyncio.get_running_loop().time() - start
    assert elapsed >= 0.15, "four requests to one host must be spaced apart"


def test_the_lease_covers_the_whole_claimed_batchs_worst_case() -> None:
    """A claim leases every item from the moment it is taken, but the last item
    is not touched until the ones ahead of it finish. A lease shorter than the
    batch's worst case gets reclaimed out from under a LIVE worker — which is
    what a hardcoded 120s against a 20-item batch did on allgreenrecycling.com.
    """
    worst_case = url_verify.CLAIM_BATCH_SIZE * 2 * url_verify.REQUEST_TIMEOUT_SECONDS
    assert url_verify.ITEM_LEASE_SECONDS >= worst_case, (
        f"lease {url_verify.ITEM_LEASE_SECONDS}s cannot cover "
        f"{url_verify.CLAIM_BATCH_SIZE} items × two {url_verify.REQUEST_TIMEOUT_SECONDS}s "
        "timeouts — live items will be reclaimed and re-worked"
    )


def test_retryable_classification_separates_moments_from_verdicts() -> None:
    for transient in (429, 500, 502, 503, 504, 408):
        assert classify_status(transient) is True
    for verdict in (200, 301, 404, 410, 451):
        assert classify_status(verdict) is False


# ---------------------------------------------------------------------------
# Durability — the frontier


def _candidates(n: int) -> list[dict]:
    return [
        {
            "page_id": f"page-{i}",
            "url": f"https://x.test/{i}",
            "in_sitemap": True,
            "gsc_impressions": 0,
        }
        for i in range(n)
    ]


@pytest.mark.asyncio
async def test_seeding_is_idempotent_on_page_identity() -> None:
    store = InMemoryExecutionStore()
    assert await seed_frontier(store, EXEC, _candidates(5)) == 5
    # A resumed sweep re-seeds the same set — the unique canonical key makes
    # that a no-op rather than a doubling.
    assert await seed_frontier(store, EXEC, _candidates(5)) == 0
    counts = await store.work_item_counts(EXEC)
    assert counts[WorkItemState.PENDING] == 5


@pytest.mark.asyncio
async def test_chaos_a_killed_worker_loses_nothing_and_duplicates_nothing(
    monkeypatch,
) -> None:
    """Kill the process mid-sweep; the job still completes.

    Phase 1: a worker claims items and is killed before settling them — exactly
    what a deploy, an OOM kill, or a restart does. Phase 2: the lease expires,
    the reaper returns the items to pending, and a fresh worker drains the
    frontier. Every URL must be verified exactly once.
    """

    store = InMemoryExecutionStore()
    total = 24
    await seed_frontier(store, EXEC, _candidates(total))

    persisted: list[str] = []
    persist_lock = asyncio.Lock()

    async def fake_persist(page_id, outcome):
        async with persist_lock:
            # The real persist is a compare-and-swap on "still NULL", so a
            # duplicate delivery writes nothing. Model that exactly.
            if page_id in persisted:
                return False
            persisted.append(page_id)
            return True

    monkeypatch.setattr(url_verify, "persist_verification", fake_persist)

    killed = asyncio.Event()

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html"})

    # --- Phase 1: a worker dies mid-flight -------------------------------
    async with _client(handler) as http:

        async def die_after_a_few(*args, **kwargs):
            if len(persisted) >= 6:
                killed.set()
                raise asyncio.CancelledError("process killed")
            return await fake_persist(*args, **kwargs)

        monkeypatch.setattr(url_verify, "persist_verification", die_after_a_few)
        with pytest.raises(asyncio.CancelledError):
            await run_frontier(
                store,
                EXEC,
                holder="proc-A",
                concurrency=1,
                per_host_spacing_s=0,
                http=http,
            )

    assert killed.is_set()
    partial = len(persisted)
    assert 0 < partial < total, "the crash must land mid-run to prove anything"

    counts = await store.work_item_counts(EXEC)
    stranded = counts.get(WorkItemState.IN_PROGRESS, 0)
    assert stranded > 0, "the dead worker must leave claimed-but-unsettled items"

    # --- Phase 2: leases expire, a new process resumes --------------------
    reclaimed = await store.reclaim_expired_work_items(
        now=datetime.now(UTC) + timedelta(seconds=url_verify.ITEM_LEASE_SECONDS + 60)
    )
    assert reclaimed == stranded

    monkeypatch.setattr(url_verify, "persist_verification", fake_persist)
    summary = VerificationSummary()
    async with _client(handler) as http:
        await run_frontier(
            store,
            EXEC,
            holder="proc-B",
            concurrency=4,
            per_host_spacing_s=0,
            summary=summary,
            http=http,
        )

    # Zero dropped: every seeded URL got verified.
    assert len(persisted) == total
    assert len(set(persisted)) == total
    # Zero pending left, and nothing stuck in flight.
    final = await store.work_item_counts(EXEC)
    assert final.get(WorkItemState.PENDING, 0) == 0
    assert final.get(WorkItemState.IN_PROGRESS, 0) == 0
    assert final.get(WorkItemState.SUCCEEDED, 0) == total


@pytest.mark.asyncio
async def test_a_crawl_that_wins_the_race_is_never_overwritten(monkeypatch) -> None:
    """The persist is a CAS on "still unverified". When a real crawl fills the
    row first, the sweep declines — and counts it rather than hiding it."""

    store = InMemoryExecutionStore()
    await seed_frontier(store, EXEC, _candidates(3))

    async def crawl_already_won(page_id, outcome):
        return False

    monkeypatch.setattr(url_verify, "persist_verification", crawl_already_won)

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html"})

    summary = VerificationSummary()
    async with _client(handler) as http:
        await run_frontier(
            store,
            EXEC,
            holder="p",
            concurrency=1,
            per_host_spacing_s=0,
            summary=summary,
            http=http,
        )

    assert summary.checked == 3
    assert summary.persisted == 0
    assert summary.lost_to_crawl == 3


@pytest.mark.asyncio
async def test_robots_disallowed_urls_are_skipped_not_fetched(monkeypatch) -> None:
    from matrx_scraper.robots_txt import parse_robots_txt

    store = InMemoryExecutionStore()
    await seed_frontier(
        store,
        EXEC,
        [
            {
                "page_id": "p1",
                "url": "https://x.test/private/a",
                "in_sitemap": True,
                "gsc_impressions": 0,
            },
            {
                "page_id": "p2",
                "url": "https://x.test/public/b",
                "in_sitemap": True,
                "gsc_impressions": 0,
            },
        ],
    )
    robots = parse_robots_txt("User-agent: *\nDisallow: /private/\n")

    fetched: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        fetched.append(str(request.url))
        return httpx.Response(200, headers={"content-type": "text/html"})

    async def ok_persist(page_id, outcome):
        return True

    monkeypatch.setattr(url_verify, "persist_verification", ok_persist)
    summary = VerificationSummary()
    async with _client(handler) as http:
        await run_frontier(
            store,
            EXEC,
            holder="p",
            robots=robots,
            concurrency=1,
            per_host_spacing_s=0,
            summary=summary,
            http=http,
        )

    assert summary.robots_skipped == 1
    assert all("/private/" not in u for u in fetched)
    assert summary.checked == 1


@pytest.mark.asyncio
async def test_a_run_waits_out_retry_backoff_instead_of_declaring_victory(
    monkeypatch,
) -> None:
    """An empty claim does not mean the job is done.

    A retryable item sits on a `not_before` backoff and is unclaimable for a
    while. Returning on the first empty claim abandoned it mid-run: live, that
    left titaniummarketing.com at 27 of 64 URLs verified while the run reported
    success. The run must keep going until nothing is outstanding.
    """

    store = InMemoryExecutionStore()
    await seed_frontier(store, EXEC, _candidates(3))

    attempts: dict[str, int] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        key = str(request.url)
        attempts[key] = attempts.get(key, 0) + 1
        # Fail once with a retryable status, then succeed.
        if attempts[key] == 1:
            return httpx.Response(503)
        return httpx.Response(200, headers={"content-type": "text/html"})

    persisted: list[str] = []

    async def ok_persist(page_id, outcome):
        persisted.append(page_id)
        return True

    monkeypatch.setattr(url_verify, "persist_verification", ok_persist)
    # Short backoff/poll so the test exercises the wait without sleeping for real.
    monkeypatch.setattr(url_verify, "RETRY_BACKOFF_SECONDS", 0.01)
    monkeypatch.setattr(url_verify, "IDLE_POLL_SECONDS", 0.01)

    summary = VerificationSummary()
    async with _client(handler) as http:
        await run_frontier(
            store,
            EXEC,
            holder="p",
            concurrency=1,
            per_host_spacing_s=0,
            summary=summary,
            http=http,
        )

    assert sorted(persisted) == ["page-0", "page-1", "page-2"]
    counts = await store.work_item_counts(EXEC)
    assert counts.get(WorkItemState.PENDING, 0) == 0
    assert counts.get(WorkItemState.SUCCEEDED, 0) == 3


@pytest.mark.asyncio
async def test_response_counters_and_url_counters_are_not_the_same_number(
    monkeypatch,
) -> None:
    """`broken` counts RESPONSES; `terminal_failures` counts URLs.

    Live, vasaro.com reported `broken=1089` and it read as "1,089 broken pages".
    Only 25 URLs ever failed terminally — the rest was one host handing out 429s
    that succeeded on retry. Anyone reporting this to a customer needs the URL
    number, so the two must stay visibly distinct.
    """

    store = InMemoryExecutionStore()
    await seed_frontier(store, EXEC, _candidates(1))
    attempts = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        attempts["n"] += 1
        if attempts["n"] <= 2:
            return httpx.Response(429)  # retryable: counted as `broken` each time
        return httpx.Response(200, headers={"content-type": "text/html"})

    async def ok_persist(page_id, outcome):
        return True

    monkeypatch.setattr(url_verify, "persist_verification", ok_persist)
    monkeypatch.setattr(url_verify, "RETRY_BACKOFF_SECONDS", 0.01)
    monkeypatch.setattr(url_verify, "IDLE_POLL_SECONDS", 0.01)

    summary = VerificationSummary()
    async with _client(handler) as http:
        await run_frontier(
            store,
            EXEC,
            holder="p",
            concurrency=1,
            per_host_spacing_s=0,
            summary=summary,
            http=http,
        )

    assert summary.checked == 3, "three responses for one URL"
    assert summary.broken == 2, "two of them were failing RESPONSES"
    assert summary.persisted == 1, "…but exactly one URL was answered"
    assert summary.terminal_failures == 0, "and that URL is not broken at all"


@pytest.mark.asyncio
async def test_retryable_answers_eventually_dead_letter_loudly(monkeypatch) -> None:
    """A URL that never gives a terminal answer must not spin forever, and must
    not be silently counted as swept."""

    store = InMemoryExecutionStore()
    await seed_frontier(store, EXEC, _candidates(1))

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(503)

    async def ok_persist(page_id, outcome):
        return True

    monkeypatch.setattr(url_verify, "persist_verification", ok_persist)
    monkeypatch.setattr(url_verify, "RETRY_BACKOFF_SECONDS", 0.0)

    async with _client(handler) as http:
        for _ in range(url_verify.ITEM_MAX_ATTEMPTS + 1):
            await run_frontier(
                store, EXEC, holder="p", concurrency=1, per_host_spacing_s=0, http=http
            )

    counts = await store.work_item_counts(EXEC)
    assert counts.get(WorkItemState.PENDING, 0) == 0
    assert counts.get(WorkItemState.DEAD_LETTER, 0) == 1
