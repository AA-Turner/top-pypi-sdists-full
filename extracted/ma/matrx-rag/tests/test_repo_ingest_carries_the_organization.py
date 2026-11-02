"""A repository is indexed into an organization the host carries: no organization is refused before any work,
and each file's ingest receives the organization and the person (it raised without them — 2026-10-28 census)."""

from __future__ import annotations

from typing import Any

import pytest

from matrx_rag import repo_ingest


@pytest.mark.asyncio
@pytest.mark.parametrize("entry", ["ingest_repository", "incremental_update"])
async def test_no_organization_is_refused_before_any_work(entry: str) -> None:
    fn = getattr(repo_ingest, entry)
    kwargs: dict[str, Any] = {"user_id": "u-1"}
    if entry == "incremental_update":
        kwargs["since_ref"] = "HEAD~1"
    with pytest.raises(ValueError, match="organization_id is required"):
        await fn("/nowhere", **kwargs)


@pytest.mark.asyncio
async def test_each_file_ingest_carries_the_organization_and_person(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    async def upsert(**_kw: Any) -> tuple[str, bool]:
        return "code-1", True

    async def ingest(kind: str, source_id: str, **kw: Any) -> Any:
        seen.update(kw, kind=kind, source_id=source_id)
        return "result"

    monkeypatch.setattr(repo_ingest, "_upsert_code_file", upsert)
    monkeypatch.setattr(repo_ingest, "ingest_source", ingest)
    file = type("F", (), {"rel_path": "a.py", "language": "python"})()
    await repo_ingest._ingest_one(user_id="u-1", organization_id="o-1", repo_root="/r", repo_ref="main", file=file, force=False)
    assert (seen["user_id"], seen["organization_id"], seen["kind"]) == ("u-1", "o-1", "code_file")
