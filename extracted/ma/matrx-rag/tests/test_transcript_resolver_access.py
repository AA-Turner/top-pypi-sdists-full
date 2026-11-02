"""A transcript is indexed for whoever may READ it (iam.has_access_for), never only its creator.

A public video's ONE shared transcript is owned by the system principal and every organization reads
it (social-media-unification); the old ``created_by == user`` filter silently skipped it in every
knowledge-base build. Run: uv run pytest packages/matrx-rag/tests/test_transcript_resolver_access.py
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_rag import sources

ROW = {"id": "t1", "created_by": "system-principal", "organization_id": "system-org", "title": "A video",
       "description": "", "segments": [{"text": "hello world"}], "folder_name": "YouTube", "tags": [],
       "source_type": "video", "metadata": {}}


class _Q:
    def __init__(self, seen: dict[str, Any]) -> None:
        self.seen = seen

    def filter(self, *args: Any, **kw: Any) -> "_Q":
        self.seen.update(kw)
        return self

    async def values(self, *_fields: str) -> list[dict[str, Any]]:
        return [ROW]


@pytest.fixture
def wired(monkeypatch):
    seen: dict[str, Any] = {}

    class Transcripts:
        @staticmethod
        def filter(*args: Any, **kw: Any) -> _Q:
            seen.update(kw)
            return _Q(seen)

    monkeypatch.setattr(sources, "get_db_model", lambda name: Transcripts)
    return seen


async def test_a_shared_transcript_resolves_for_a_reader_who_did_not_create_it(wired, monkeypatch):
    import matrx_orm

    async def allowed(actor, token, entity_id, level="viewer"):
        assert (actor, token, entity_id, level) == ("reader-1", "transcript", "t1", "viewer")
        return True

    monkeypatch.setattr(matrx_orm, "platform_access_check", allowed)
    out = await sources._resolve_transcript("t1", user_id="reader-1")
    assert out is not None and "created_by" not in wired


async def test_a_transcript_the_person_cannot_reach_does_not_exist_for_them(wired, monkeypatch):
    import matrx_orm

    async def refused(*_a, **_k):
        return False

    monkeypatch.setattr(matrx_orm, "platform_access_check", refused)
    assert await sources._resolve_transcript("t1", user_id="stranger") is None
