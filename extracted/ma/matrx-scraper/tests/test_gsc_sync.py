"""Pure-part tests for the GSC sync — binding parse, response paging → rows,
URL→page scope mapping, vault credential resolution, and the summary shape."""

from __future__ import annotations

from datetime import date

import httpx
import pytest

from matrx_scraper.web_crawl.contracts import GscSyncSummary
from matrx_scraper.web_crawl.gsc_sync import (
    GscDailyPageRow,
    build_gsc_client,
    compute_sync_window,
    fetch_search_analytics_rows,
    parse_gsc_binding,
    parse_search_analytics_rows,
    parse_submitted_sitemaps,
    partition_rows_by_scope,
    resolve_google_credential,
)


# ---------------------------------------------------------------------------
# Binding
# ---------------------------------------------------------------------------


def _binding(**overrides: object) -> dict:
    binding = {
        "enabled": True,
        "credential_ref": "11111111-1111-1111-1111-111111111111",
        "resource_ref": "sc-domain:example.com",
    }
    binding.update(overrides)
    return {"marketing": {"providers": {"google_search_console": binding}}}


def test_parse_gsc_binding_extracts_fields() -> None:
    binding = parse_gsc_binding(_binding())
    assert binding.credential_ref == "11111111-1111-1111-1111-111111111111"
    assert binding.resource_ref == "sc-domain:example.com"


@pytest.mark.parametrize(
    "integrations",
    [
        {},
        {"marketing": {}},
        {"marketing": {"providers": {}}},
        _binding(enabled=False),
        _binding(credential_ref=""),
        _binding(resource_ref=None),
    ],
)
def test_parse_gsc_binding_is_loud_on_every_gap(integrations: dict) -> None:
    with pytest.raises(ValueError):
        parse_gsc_binding(integrations)


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------


def test_parse_search_analytics_rows_typed() -> None:
    rows = parse_search_analytics_rows(
        {
            "rows": [
                {
                    "keys": ["2026-07-01", "https://example.com/a"],
                    "clicks": 3,
                    "impressions": 90,
                    "ctr": 0.0333,
                    "position": 12.4,
                },
                {"keys": ["2026-07-02", "https://example.com/a"], "clicks": 0},
            ]
        }
    )
    assert rows[0] == GscDailyPageRow(
        date=date(2026, 7, 1),
        page_url="https://example.com/a",
        clicks=3,
        impressions=90,
        ctr=0.0333,
        position=12.4,
    )
    assert rows[1].clicks == 0 and rows[1].position is None


def test_parse_search_analytics_rows_skips_malformed_and_handles_empty() -> None:
    assert parse_search_analytics_rows({}) == []
    rows = parse_search_analytics_rows(
        {
            "rows": [
                "junk",
                {"keys": ["only-one"]},
                {"keys": ["not-a-date", "https://example.com/x"]},
                {"keys": ["2026-07-01", ""]},
                {"keys": ["2026-07-01", "https://example.com/ok"]},
            ]
        }
    )
    assert [r.page_url for r in rows] == ["https://example.com/ok"]


def test_parse_search_analytics_rows_rejects_non_list_rows() -> None:
    with pytest.raises(ValueError):
        parse_search_analytics_rows({"rows": {"nope": True}})


def test_parse_submitted_sitemaps() -> None:
    entries = parse_submitted_sitemaps(
        {
            "sitemap": [
                {
                    "path": "https://example.com/sitemap.xml",
                    "lastSubmitted": "2026-07-01T00:00:00.000Z",
                    "isPending": False,
                    "errors": "0",
                    "warnings": 2,
                },
                {"no_path": True},
            ]
        }
    )
    assert entries == [
        {
            "path": "https://example.com/sitemap.xml",
            "last_submitted": "2026-07-01T00:00:00.000Z",
            "last_downloaded": None,
            "is_pending": False,
            "errors": 0,
            "warnings": 2,
        }
    ]
    assert parse_submitted_sitemaps({}) == []


# ---------------------------------------------------------------------------
# Paging
# ---------------------------------------------------------------------------


class _StubGscClient:
    timeout = 5.0

    async def access_token(self) -> str:
        return "token-123"


class _FakeHttp:
    def __init__(self, responses: list[httpx.Response]) -> None:
        self.responses = responses
        self.requests: list[dict] = []

    async def __aenter__(self) -> _FakeHttp:
        return self

    async def __aexit__(self, *args: object) -> None:
        return None

    async def post(self, url: str, *, headers: dict, json: dict) -> httpx.Response:
        self.requests.append(json)
        return self.responses[len(self.requests) - 1]


def _response(status: int, payload: dict) -> httpx.Response:
    return httpx.Response(
        status,
        json=payload,
        request=httpx.Request("POST", "https://searchconsole.googleapis.com/"),
    )


@pytest.mark.asyncio
async def test_fetch_search_analytics_rows_paginates_fully(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    page_one = {
        "rows": [
            {"keys": ["2026-07-01", "https://example.com/a"], "clicks": 1},
            {"keys": ["2026-07-01", "https://example.com/b"], "clicks": 2},
        ]
    }
    page_two = {"rows": [{"keys": ["2026-07-02", "https://example.com/a"], "clicks": 3}]}
    fake = _FakeHttp([_response(200, page_one), _response(200, page_two)])
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.gsc_sync.httpx.AsyncClient",
        lambda **kwargs: fake,
    )
    rows = await fetch_search_analytics_rows(
        _StubGscClient(),  # type: ignore[arg-type]
        property_ref="sc-domain:example.com",
        start=date(2026, 7, 1),
        end=date(2026, 7, 2),
        row_limit=2,
    )
    assert len(rows) == 3
    assert fake.requests[0]["startRow"] == 0
    assert fake.requests[1]["startRow"] == 2
    assert fake.requests[0]["dimensions"] == ["date", "page"]


@pytest.mark.asyncio
async def test_fetch_search_analytics_rows_raises_on_http_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake = _FakeHttp([_response(403, {"error": {"status": "PERMISSION_DENIED"}})])
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.gsc_sync.httpx.AsyncClient",
        lambda **kwargs: fake,
    )
    with pytest.raises(RuntimeError, match="HTTP 403"):
        await fetch_search_analytics_rows(
            _StubGscClient(),  # type: ignore[arg-type]
            property_ref="sc-domain:example.com",
            start=date(2026, 7, 1),
            end=date(2026, 7, 2),
        )


# ---------------------------------------------------------------------------
# Scope mapping
# ---------------------------------------------------------------------------


def _row(url: str, day: str = "2026-07-01") -> GscDailyPageRow:
    return GscDailyPageRow(
        date=date.fromisoformat(day),
        page_url=url,
        clicks=1,
        impressions=1,
        ctr=1.0,
        position=1.0,
    )


def test_partition_rows_by_scope_groups_by_normalized_url() -> None:
    grouped, skipped = partition_rows_by_scope(
        [
            _row("https://example.com/a"),
            _row("https://example.com/a/", day="2026-07-02"),
            _row("https://www.example.com/b"),
            _row("https://other.com/c"),
            _row("ftp://example.com/d"),
        ],
        root_host="example.com",
    )
    assert set(grouped) == {"https://example.com/a", "https://www.example.com/b"}
    assert len(grouped["https://example.com/a"]) == 2
    assert skipped == 2


def test_partition_rows_merges_same_date_url_variants() -> None:
    """Regression: URL variants that normalize to the same page (trailing
    slash, scheme/host case, fragments) reported by GSC for the SAME day must
    collapse to one row per (page, date) — two rows for one key made the
    ``ON CONFLICT (page_id, date)`` upsert throw CardinalityViolation and
    killed every sync (2026-07-21, All Green)."""

    grouped, skipped = partition_rows_by_scope(
        [
            GscDailyPageRow(
                date=date.fromisoformat("2026-07-01"),
                page_url="https://example.com/a",
                clicks=3,
                impressions=30,
                ctr=0.1,
                position=4.0,
            ),
            GscDailyPageRow(
                date=date.fromisoformat("2026-07-01"),
                page_url="HTTPS://EXAMPLE.COM/a/#top",
                clicks=1,
                impressions=10,
                ctr=0.1,
                position=8.0,
            ),
            GscDailyPageRow(
                date=date.fromisoformat("2026-07-02"),
                page_url="https://example.com/a",
                clicks=2,
                impressions=20,
                ctr=0.1,
                position=5.0,
            ),
        ],
        root_host="example.com",
    )
    assert skipped == 0
    rows = grouped["https://example.com/a"]
    assert [r.date.isoformat() for r in rows] == ["2026-07-01", "2026-07-02"]
    merged = rows[0]
    assert merged.clicks == 4
    assert merged.impressions == 40
    assert merged.ctr == pytest.approx(0.1)
    # impressions-weighted: (4*30 + 8*10) / 40 = 5.0
    assert merged.position == pytest.approx(5.0)
    # per-date uniqueness is the actual DB invariant
    assert len({(id(grouped), r.date) for r in rows}) == len(rows)


# ---------------------------------------------------------------------------
# Window
# ---------------------------------------------------------------------------


def test_compute_sync_window_last_28_days_with_gsc_lag() -> None:
    start, end = compute_sync_window(days=28, today=date(2026, 7, 20))
    assert end == date(2026, 7, 18)
    assert start == date(2026, 6, 21)
    assert (end - start).days == 27
    with pytest.raises(ValueError):
        compute_sync_window(days=0)


# ---------------------------------------------------------------------------
# Credential resolution (canonical vault via aidream's internal endpoint)
# ---------------------------------------------------------------------------


class _FakeGetHttp:
    def __init__(self, response: httpx.Response) -> None:
        self.response = response
        self.calls: list[dict] = []

    async def __aenter__(self) -> _FakeGetHttp:
        return self

    async def __aexit__(self, *args: object) -> None:
        return None

    async def get(self, url: str, *, params: dict, headers: dict) -> httpx.Response:
        self.calls.append({"url": url, "params": params, "headers": headers})
        return self.response


@pytest.mark.asyncio
async def test_resolve_google_credential_calls_aidream(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("AIDREAM_URL", "https://server.example/")
    monkeypatch.setenv("AIDREAM_SERVICE_TOKEN", "svc-token")
    fake = _FakeGetHttp(
        _response(
            200,
            {
                "refresh_token": "1//refresh",
                "client_id": "abc.apps.googleusercontent.com",
                "client_secret": "shhh",
            },
        )
    )
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.gsc_sync.httpx.AsyncClient",
        lambda **kwargs: fake,
    )
    credential = await resolve_google_credential(
        credential_ref="conn-1",
        site_organization_id="org-1",
        user_id="user-1",
    )
    assert credential.refresh_token == "1//refresh"
    assert credential.client_id == "abc.apps.googleusercontent.com"
    call = fake.calls[0]
    assert call["url"] == "https://server.example/api/google-integrations/internal/credential"
    assert call["params"] == {"connection_id": "conn-1", "organization_id": "org-1"}
    assert call["headers"]["Authorization"] == "Bearer svc-token"
    assert call["headers"]["X-Matrx-User-Id"] == "user-1"
    client = build_gsc_client(credential)
    assert client.refresh_token == "1//refresh"
    assert client.client_id == "abc.apps.googleusercontent.com"


@pytest.mark.asyncio
async def test_resolve_google_credential_http_error_is_loud(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("AIDREAM_URL", "https://server.example")
    monkeypatch.setenv("AIDREAM_SERVICE_TOKEN", "svc-token")
    fake = _FakeGetHttp(_response(409, {"detail": "needs re-authentication"}))
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.gsc_sync.httpx.AsyncClient",
        lambda **kwargs: fake,
    )
    with pytest.raises(RuntimeError, match="HTTP 409"):
        await resolve_google_credential(
            credential_ref="conn-1",
            site_organization_id="org-1",
            user_id="user-1",
        )


@pytest.mark.asyncio
async def test_resolve_google_credential_incomplete_payload_is_loud(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("AIDREAM_URL", "https://server.example")
    monkeypatch.setenv("AIDREAM_SERVICE_TOKEN", "svc-token")
    fake = _FakeGetHttp(_response(200, {"refresh_token": "x"}))
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.gsc_sync.httpx.AsyncClient",
        lambda **kwargs: fake,
    )
    with pytest.raises(RuntimeError, match="incomplete credential"):
        await resolve_google_credential(
            credential_ref="conn-1",
            site_organization_id="org-1",
            user_id="user-1",
        )


@pytest.mark.asyncio
async def test_injected_resolver_wins_and_needs_no_aidream_env(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The standalone path: a host injects a resolver and NOTHING reaches for
    an aidream URL/token. This is what makes gsc_sync usable outside the Matrx
    scraper microservice."""

    from matrx_scraper._ext import _registry, configure_ext

    monkeypatch.delenv("AIDREAM_URL", raising=False)
    monkeypatch.delenv("AIDREAM_SERVICE_TOKEN", raising=False)
    monkeypatch.setattr(
        "matrx_scraper.web_crawl.gsc_sync.httpx.AsyncClient",
        lambda **kwargs: pytest.fail("injected resolver must not fall back to HTTP"),
    )

    seen: dict[str, object] = {}

    async def _resolver(**kwargs: object) -> dict[str, str]:
        seen.update(kwargs)
        return {
            "refresh_token": "1//injected",
            "client_id": "abc.apps.googleusercontent.com",
            "client_secret": "shhh",
        }

    configure_ext(google_credential_resolver=_resolver)
    try:
        credential = await resolve_google_credential(
            credential_ref="conn-1",
            site_organization_id="org-1",
            user_id="user-1",
            resource_type="search_console_property",
            resource_ref="sc-domain:example.com",
        )
    finally:
        _registry.pop("google_credential_resolver", None)

    assert credential.refresh_token == "1//injected"
    assert seen["credential_ref"] == "conn-1"
    assert seen["site_organization_id"] == "org-1"
    assert seen["user_id"] == "user-1"
    assert seen["resource_type"] == "search_console_property"
    assert seen["resource_ref"] == "sc-domain:example.com"


@pytest.mark.asyncio
async def test_injected_resolver_incomplete_payload_is_loud(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_scraper._ext import _registry, configure_ext

    async def _resolver(**kwargs: object) -> dict[str, str]:
        return {"refresh_token": "x"}

    configure_ext(google_credential_resolver=_resolver)
    try:
        with pytest.raises(RuntimeError, match="incomplete Google credential"):
            await resolve_google_credential(
                credential_ref="conn-1",
                site_organization_id="org-1",
                user_id="user-1",
            )
    finally:
        _registry.pop("google_credential_resolver", None)


@pytest.mark.asyncio
async def test_resolve_google_credential_requires_config(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("AIDREAM_URL", raising=False)
    monkeypatch.delenv("AIDREAM_SERVICE_TOKEN", raising=False)
    with pytest.raises(RuntimeError, match="not configured"):
        await resolve_google_credential(
            credential_ref="conn-1",
            site_organization_id="org-1",
            user_id="user-1",
        )


# ---------------------------------------------------------------------------
# Summary shape
# ---------------------------------------------------------------------------


def test_gsc_sync_summary_shape() -> None:
    summary = GscSyncSummary(property="sc-domain:example.com", days=28)
    assert summary.model_dump(mode="json") == {
        "property": "sc-domain:example.com",
        "days": 28,
        "pages": 0,
        "stats_rows": 0,
        "submitted_sitemaps": [],
        "skipped_out_of_scope": 0,
        "errors": [],
    }
