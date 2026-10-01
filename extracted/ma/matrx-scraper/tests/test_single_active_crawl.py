"""One ACTIVE session per (site, start lane).

Lanes: `site_crawl` (full/list) and `site_initialization` (initialization /
homepage). `prepare_start` names a live holder up front (409 "already
active"); the ARBITER is the `crawl_session_one_active_start_per_lane` unique
index — the session INSERT is the claim, so two racing starts can never both
land (2026-09-14: one site creation ran two initializations 0.4 s apart).
These tests pin the live judgment and the claim loop; the index itself is
proven on the dev clone by `test_crawl_start_claim_clone.py`.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest
from matrx_orm import IntegrityError

from matrx_scraper.web_crawl import service as service_module
from matrx_scraper.web_crawl.persistence import (
    START_CLAIM_INDEX,
    STALE_SESSION_AFTER,
    CrawlStartConflict,
    WebCrawlRepository,
    is_start_claim_conflict,
)
from matrx_scraper.web_crawl.service import WebCrawlService, _session_blocks_new_crawl

NOW = datetime(2026, 8, 8, 12, 0, 0, tzinfo=UTC)


def _session(
    *,
    mode: str = "full",
    status: str = "queued",
    updated_ago: timedelta = timedelta(seconds=10),
    lease: dict | None = None,
    session_id: str = "s-1",
    created_at: datetime | None = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=session_id,
        scope={"mode": mode},
        status=status,
        updated_at=NOW - updated_ago,
        created_at=created_at or (NOW - updated_ago),
        metadata={"run_lease": lease} if lease else {},
    )


# ---------------------------------------------------------------------------
# Which sessions block a new full/list start
# ---------------------------------------------------------------------------


def test_fresh_queued_full_session_blocks() -> None:
    assert _session_blocks_new_crawl(_session(), now=NOW)


def test_fresh_running_leased_session_blocks() -> None:
    session = _session(
        status="running",
        lease={"owner": "tok", "heartbeat_at": (NOW - timedelta(seconds=5)).isoformat()},
    )
    assert _session_blocks_new_crawl(session, now=NOW)


def test_stale_sessions_do_not_block() -> None:
    """A session past STALE_SESSION_AFTER without a heartbeat is a crash the
    reaper owns — it must never block a legitimate new start."""
    stale = STALE_SESSION_AFTER + timedelta(minutes=1)
    assert not _session_blocks_new_crawl(_session(updated_ago=stale), now=NOW)
    dead_run = _session(
        status="running",
        updated_ago=stale,
        lease={"owner": "tok", "heartbeat_at": (NOW - stale).isoformat()},
    )
    assert not _session_blocks_new_crawl(dead_run, now=NOW)


@pytest.mark.parametrize("mode", ["homepage", "initialization", "page_fetch", "sitemap_sync"])
def test_other_lanes_never_block_a_site_crawl(mode: str) -> None:
    assert not _session_blocks_new_crawl(_session(mode=mode), now=NOW)


@pytest.mark.parametrize("mode", ["initialization", "homepage"])
def test_a_live_initialization_blocks_another_initialization(mode: str) -> None:
    """The 2026-09-14 defect: initialization had NO lane, so a second start
    (0.4 s later) ran a whole second initialization."""
    assert _session_blocks_new_crawl(_session(mode=mode), lane="site_initialization", now=NOW)


@pytest.mark.parametrize("mode", ["full", "list", "page_fetch", "gsc_sync"])
def test_other_modes_never_block_an_initialization(mode: str) -> None:
    assert not _session_blocks_new_crawl(_session(mode=mode), lane="site_initialization", now=NOW)


def test_modeless_rows_never_block() -> None:
    session = _session()
    session.scope = {}
    assert not _session_blocks_new_crawl(session, now=NOW)


def test_list_mode_blocks_like_full() -> None:
    assert _session_blocks_new_crawl(_session(mode="list"), now=NOW)


def test_queued_with_unreadable_updated_at_fails_closed() -> None:
    session = _session()
    session.updated_at = None
    assert _session_blocks_new_crawl(session, now=NOW)


def test_terminal_statuses_never_block() -> None:
    for status in ("complete", "partial", "failed", "cancelled"):
        assert not _session_blocks_new_crawl(_session(status=status), now=NOW)


# ---------------------------------------------------------------------------
# The claim — the INSERT is the arbiter
# ---------------------------------------------------------------------------


def _claim_violation() -> IntegrityError:
    return IntegrityError(
        constraint="unique",
        constraint_name=START_CLAIM_INDEX,
        original_error=f'duplicate key value violates unique constraint "{START_CLAIM_INDEX}"',
    )


def test_only_the_start_claim_index_counts_as_a_claim_conflict() -> None:
    assert is_start_claim_conflict(_claim_violation())
    other = IntegrityError(
        constraint="unique",
        constraint_name="crawl_event_session_sequence_unique",
        original_error="duplicate key value violates unique constraint",
    )
    assert not is_start_claim_conflict(other)


class _Repo:
    def __init__(self, outcomes: list[object]) -> None:
        self.outcomes = outcomes
        self.calls = 0

    async def create_session(self, site_id: str, **_: object) -> tuple[str, str, str, str]:
        self.calls += 1
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        return ("https://example.com/", str(outcome), "org", "owner")


def _live_init(session_id: str = "live-1") -> SimpleNamespace:
    return SimpleNamespace(
        id=session_id,
        scope={"mode": "initialization"},
        status="queued",
        updated_at=datetime.now(UTC),
        created_at=datetime.now(UTC),
        metadata={},
    )


async def _claim(repo: _Repo, lane: str | None = "site_initialization"):
    return await WebCrawlService._claim_session(
        repo,  # type: ignore[arg-type]
        "site-1",
        lane=lane,
        scope={"mode": "initialization"},
        user_id="user-1",
        trigger="manual",
    )


@pytest.mark.asyncio
async def test_losing_the_claim_to_a_live_run_is_a_409_naming_the_run_to_follow(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    holder = _live_init("the-first-one")

    async def active(_site_id: str) -> list[object]:
        return [holder]

    monkeypatch.setattr(WebCrawlRepository, "list_active_sessions_for_site", staticmethod(active))
    repo = _Repo([_claim_violation()])
    with pytest.raises(CrawlStartConflict) as caught:
        await _claim(repo)
    assert "already active" in str(caught.value)
    assert caught.value.active_session_id == "the-first-one"
    assert repo.calls == 1, "a live holder must never be retried against"


@pytest.mark.asyncio
async def test_a_dead_claim_holder_is_retired_and_the_start_claims_once_more(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    dead = _live_init("dead-1")
    dead.status = "running"
    dead.metadata = {
        "run_lease": {"owner": "x", "heartbeat_at": "2020-01-01T00:00:00+00:00"}
    }
    dead.updated_at = datetime(2020, 1, 1, tzinfo=UTC)
    retired: list[str] = []

    async def active(_site_id: str) -> list[object]:
        return [] if retired else [dead]

    async def retire(session_id: str) -> int:
        retired.append(session_id)
        return 1

    monkeypatch.setattr(WebCrawlRepository, "list_active_sessions_for_site", staticmethod(active))
    monkeypatch.setattr(WebCrawlRepository, "retire_dead_session", staticmethod(retire))
    repo = _Repo([_claim_violation(), "new-session"])
    result = await _claim(repo)
    assert result[1] == "new-session"
    assert retired == ["dead-1"]


@pytest.mark.asyncio
async def test_losing_twice_is_final(monkeypatch: pytest.MonkeyPatch) -> None:
    async def active(_site_id: str) -> list[object]:
        return []

    async def retire(_session_id: str) -> int:
        return 0

    monkeypatch.setattr(WebCrawlRepository, "list_active_sessions_for_site", staticmethod(active))
    monkeypatch.setattr(WebCrawlRepository, "retire_dead_session", staticmethod(retire))
    repo = _Repo([_claim_violation(), _claim_violation()])
    with pytest.raises(CrawlStartConflict, match="already active"):
        await _claim(repo)
    assert repo.calls == 2


@pytest.mark.asyncio
async def test_unlaned_modes_never_swallow_an_integrity_error() -> None:
    repo = _Repo([_claim_violation()])
    with pytest.raises(IntegrityError):
        await _claim(repo, lane=None)


def test_initialization_and_homepage_share_a_lane() -> None:
    lanes = service_module.START_LANE_BY_MODE
    assert lanes["initialization"] == lanes["homepage"] == "site_initialization"
    assert lanes["full"] == lanes["list"] == "site_crawl"
    assert "page_fetch" not in lanes


# ---------------------------------------------------------------------------
# Crawl artifacts are the organization's — stated, never left to a default
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_crawl_artifacts_state_the_type_default_audience() -> None:
    """2026-09-30: after access ladder T-13 an upload with no stated audience is
    born "only_me", and the persister's own org-artifact check then refused
    EVERY capture ("could not save one of the captured pages")."""
    from matrx_files.cloud_sync.sync_engine import SyncResult
    from matrx_utils.row_access import SHOWN_TO_TYPE_DEFAULT

    from matrx_scraper.web_crawl.persistence import (
        CanonicalBodyPersister,
        CrawlPersistenceState,
    )

    seen: dict[str, object] = {}

    class Files:
        async def upload_for_organization(self, _payload: bytes, **kwargs: object) -> dict:
            seen.update(kwargs)
            result = SyncResult.__new__(SyncResult)
            result.__dict__.update(
                is_new=True,
                published_to_web=False,
                shown_to=None,
                storage_uri="s3://bucket/key",
                file_id="f-1",
            )
            return {"result": result}

    persister = CanonicalBodyPersister.__new__(CanonicalBodyPersister)
    persister.files = Files()  # type: ignore[assignment]
    persister.root_url = "https://example.com/"
    persister.state = CrawlPersistenceState(
        site_id="site-1",
        session_id="sess-1",
        user_id="user-1",
        organization_id="org-1",
        file_owner_id="owner-1",
        coverage_qualified=False,
    )
    await persister._write_artifact(
        file_path="captures/body.html",
        content="<html></html>",
        mime_type="text/html",
        artifact_kind="body",
        capture_id="cap-1",
    )
    assert seen["shown_to"] == SHOWN_TO_TYPE_DEFAULT
    assert seen["published_to_web"] is False
