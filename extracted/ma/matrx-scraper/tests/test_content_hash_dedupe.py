"""Content-hash dedupe for re-crawls (approved 2026-08-08).

A capture whose stored bytes are byte-identical to the page's PREVIOUS
capture still appends a snapshot row (observation history stays truthful)
but POINTS AT the previously stored files.files objects instead of writing
fresh copies. Body html and markdown hash and dedupe independently, compared
only against the page's current capture (latest_snapshot_id).

THE correctness risk: a shared file must never be purged by the failure
compensation path — reused files are never added to the `written` list, so
`_purge_unreferenced` cannot touch them. Tested explicitly below.
"""

from __future__ import annotations

import hashlib
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock

import pytest
from matrx_files.cloud_sync.models import SyncResult

from matrx_scraper.crawler import PersistRequest, PersistResult
from matrx_scraper.events import PageSummary
from matrx_scraper.web_crawl.persistence import (
    CanonicalBodyPersister,
    CrawlPersistenceState,
    WebCrawlRepository,
)
from matrx_scraper.web_crawl.url_identity import CrawlIdentityResolution

BODY = "<html><body>" + " ".join(["stable content"] * 60) + "</body></html>"
MARKDOWN = "# stable content\n\nstable markdown body"
BODY_SHA = hashlib.sha256(BODY.encode("utf-8")).hexdigest()
MARKDOWN_SHA = hashlib.sha256(MARKDOWN.encode("utf-8")).hexdigest()
PREV_SNAPSHOT_ID = "99999999-9999-4999-8999-999999999999"
PREV_BODY_FILE = "prev-body-file-id"
PREV_MD_FILE = "prev-md-file-id"


@pytest.fixture(autouse=True)
def _stub_identity(monkeypatch: pytest.MonkeyPatch) -> None:
    async def resolve_identity(**kwargs: Any) -> CrawlIdentityResolution:
        final_url = str(kwargs["final_url"])
        return CrawlIdentityResolution(
            requested_url=str(kwargs["requested_url"]),
            final_url=final_url,
            canonical_url=final_url,
            page_id="22913054-1933-44b8-ba94-f592f362b8c1",
            canonical_was_new=False,
        )

    monkeypatch.setattr(
        "matrx_scraper.web_crawl.persistence.resolve_crawl_page_identity",
        resolve_identity,
    )

    class FakeFileService:
        def __init__(self, file_manager: object) -> None:
            self.file_manager = file_manager

    monkeypatch.setattr("matrx_scraper.web_crawl.persistence.FileService", FakeFileService)


def _previous_snapshot(
    *, markdown_hash: str | None = MARKDOWN_SHA, content_hash: str = BODY_SHA
) -> SimpleNamespace:
    metadata: dict[str, Any] = {}
    hashes: dict[str, str] = {"body_sha256": content_hash}
    if markdown_hash is not None:
        hashes["markdown_sha256"] = markdown_hash
    metadata["artifact_hashes"] = hashes
    if markdown_hash is None:
        # Legacy pre-feature snapshot: content_hash column only, no metadata.
        metadata = {}
    return SimpleNamespace(
        id=PREV_SNAPSHOT_ID,
        body_file_id=PREV_BODY_FILE,
        markdown_file_id=PREV_MD_FILE,
        content_hash=content_hash,
        metadata=metadata,
        deleted_at=None,
    )


def _persister(
    previous: SimpleNamespace | None,
    *,
    persist_rows: AsyncMock | None = None,
) -> tuple[CanonicalBodyPersister, AsyncMock, AsyncMock, AsyncMock]:
    state = CrawlPersistenceState(
        site_id="d0aff5b6-0710-4848-8304-164db3c80ab7",
        session_id="2b262f8c-1fbe-4575-81f5-c99c0709bd61",
        user_id="4cf62e4e-2679-484f-b652-034e697418df",
        file_owner_id="4cf62e4e-2679-484f-b652-034e697418df",
        organization_id="5dc930e9-bd65-44a1-8369-af773f6e1a5b",
        coverage_qualified=False,
    )
    purge = AsyncMock()
    persister = CanonicalBodyPersister(
        WebCrawlRepository({"sub": state.user_id, "role": "authenticated"}),
        state,
        file_manager=SimpleNamespace(
            sync_engine=SimpleNamespace(hard_delete_and_purge_async=purge)
        ),  # type: ignore[arg-type]
    )
    persister._load_previous_snapshot = AsyncMock(  # type: ignore[method-assign]
        return_value=previous
    )

    write_count = {"n": 0}

    async def fake_write(**kwargs: Any) -> SyncResult:
        write_count["n"] += 1
        return SyncResult(
            file_id=f"new-file-{write_count['n']}-{kwargs['artifact_kind']}",
            storage_uri=f"s3://canonical/new-{write_count['n']}",
            version_number=1,
            is_new=True,
            visibility="internal",
        )

    write = AsyncMock(side_effect=fake_write)
    persister._write_artifact = write  # type: ignore[method-assign]
    rows = persist_rows or AsyncMock(
        return_value=PersistResult(page_id="page-1", snapshot_id="snap-1")
    )
    persister._persist_rows = rows  # type: ignore[method-assign]
    return persister, write, rows, purge


def _request(*, body: str = BODY, markdown: str | None = MARKDOWN) -> PersistRequest:
    url = "https://acme.example/page"
    return PersistRequest(
        run_id="2b262f8c-1fbe-4575-81f5-c99c0709bd61",
        url=url,
        final_url=url,
        body=body,
        markdown=markdown,
        mime_type="text/html",
        page_summary=PageSummary(url=url, final_url=url, http_status=200, mime_type="html"),
    )


@pytest.mark.asyncio
async def test_identical_bytes_reuse_previous_files_and_count_unchanged() -> None:
    persister, write, rows, _purge = _persister(_previous_snapshot())

    result = await persister(_request())

    # Nothing was uploaded — both references point at the previous capture.
    assert write.await_count == 0
    kwargs = rows.await_args.kwargs
    assert kwargs["body_artifact"].file_id == PREV_BODY_FILE
    assert kwargs["body_artifact"].reused is True
    assert kwargs["markdown_artifact"].file_id == PREV_MD_FILE
    assert kwargs["markdown_artifact"].reused is True
    assert kwargs["reused_from_snapshot_id"] == PREV_SNAPSHOT_ID
    assert kwargs["artifact_hashes"] == {
        "body_sha256": BODY_SHA,
        "markdown_sha256": MARKDOWN_SHA,
    }
    assert result.page_id == "page-1"
    assert persister.state.pages_unchanged == 1


@pytest.mark.asyncio
async def test_changed_body_writes_fresh_files() -> None:
    persister, write, rows, _purge = _persister(_previous_snapshot())

    await persister(_request(body=BODY + "<!-- changed -->"))

    kwargs = rows.await_args.kwargs
    assert kwargs["body_artifact"].reused is False
    assert kwargs["reused_from_snapshot_id"] is None or kwargs["markdown_artifact"].reused
    assert write.await_count >= 1
    assert persister.state.pages_unchanged == 0


@pytest.mark.asyncio
async def test_body_and_markdown_dedupe_independently() -> None:
    """Same body, changed markdown: body reuses, markdown writes fresh."""
    persister, write, rows, _purge = _persister(_previous_snapshot())

    await persister(_request(markdown=MARKDOWN + "\nchanged"))

    kwargs = rows.await_args.kwargs
    assert kwargs["body_artifact"].reused is True
    assert kwargs["markdown_artifact"].reused is False
    assert write.await_count == 1  # markdown only
    assert write.await_args.kwargs["artifact_kind"] == "markdown_body"
    # Body identical = unchanged observation even when derived markdown moved.
    assert persister.state.pages_unchanged == 1


@pytest.mark.asyncio
async def test_legacy_previous_snapshot_dedupes_body_only() -> None:
    """Pre-feature snapshots carry content_hash but no markdown hash — body
    dedupes via the column, markdown must be written fresh (no hash, no
    guess)."""
    persister, write, rows, _purge = _persister(_previous_snapshot(markdown_hash=None))

    await persister(_request())

    kwargs = rows.await_args.kwargs
    assert kwargs["body_artifact"].reused is True
    assert kwargs["markdown_artifact"].reused is False
    assert write.await_count == 1
    assert write.await_args.kwargs["artifact_kind"] == "markdown_body"


@pytest.mark.asyncio
async def test_no_previous_snapshot_writes_everything() -> None:
    persister, write, rows, _purge = _persister(None)

    await persister(_request())

    kwargs = rows.await_args.kwargs
    assert kwargs["body_artifact"].reused is False
    assert kwargs["markdown_artifact"].reused is False
    assert kwargs["reused_from_snapshot_id"] is None
    assert write.await_count == 2
    assert persister.state.pages_unchanged == 0


@pytest.mark.asyncio
async def test_failed_persist_never_purges_a_reused_shared_file() -> None:
    """THE correctness risk: compensation after a failed persist must purge
    only freshly written artifacts — never the previous capture's files that
    a live snapshot still references."""
    rows = AsyncMock(side_effect=RuntimeError("row persistence failed"))
    # Body identical (reused), markdown changed (fresh write).
    persister, write, _rows, purge = _persister(_previous_snapshot(), persist_rows=rows)

    with pytest.raises(RuntimeError, match="row persistence failed"):
        await persister(_request(markdown=MARKDOWN + "\nchanged"))

    # Exactly the fresh markdown artifact was purged; the reused body file —
    # still referenced by the previous snapshot — was never touched.
    purged_file_ids = {call.args[0] for call in purge.await_args_list}
    assert PREV_BODY_FILE not in purged_file_ids
    assert PREV_MD_FILE not in purged_file_ids
    assert len(purged_file_ids) == 1
    assert next(iter(purged_file_ids)).startswith("new-file-")
