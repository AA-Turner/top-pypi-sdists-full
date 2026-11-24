from __future__ import annotations

from types import SimpleNamespace

import pytest
from matrx_rag import repo_ingest


@pytest.mark.asyncio
async def test_snapshot_bytes_use_stable_source_identity_without_changing_direct_call(
    tmp_path, monkeypatch
):
    first, second = tmp_path / "snapshot-one", tmp_path / "snapshot-two"
    first.mkdir()
    second.mkdir()
    (first / "example.py").write_text("print(1)")
    (second / "example.py").write_text("print(1)")
    captured = []
    progress = []

    class Progress:
        async def stage(self, *args, **kwargs):
            progress.append(kwargs.get("message", ""))

    def emitter(_emitter, *, source_kind, source_id):
        progress.append(source_id)
        return Progress()

    class Query:
        def limit(self, count):
            return self

        async def values(self, *columns):
            return []

    class CodeFiles:
        @staticmethod
        def filter(**kwargs):
            return Query()

        @staticmethod
        async def create(**kwargs):
            captured.append((kwargs["metadata"]["repo_root"], kwargs["content"]))
            return SimpleNamespace(id="synthetic-id")

    async def ingest_source(*args, **kwargs):
        return SimpleNamespace(
            error=None, skipped_unchanged=False, chunks_written=1, embeddings_written=1
        )

    monkeypatch.setattr(repo_ingest, "from_emitter", emitter)
    monkeypatch.setattr(repo_ingest, "get_db_model", lambda _name: CodeFiles)
    monkeypatch.setattr(repo_ingest, "ingest_source", ingest_source)
    for snapshot in (first, second):
        result = await repo_ingest.ingest_repository(
            str(snapshot), user_id="u", organization_id="o", source_repo_root="/owned/repo"
        )
        assert result.repo_path == "/owned/repo"
    result = await repo_ingest.ingest_repository(str(first), user_id="u", organization_id="o")
    assert result.repo_path == str(first)
    assert captured == [
        ("/owned/repo", "print(1)"),
        ("/owned/repo", "print(1)"),
        (str(first), "print(1)"),
    ]
    assert progress.count("/owned/repo") == 2
    assert all(str(second) not in str(item) for item in progress)
