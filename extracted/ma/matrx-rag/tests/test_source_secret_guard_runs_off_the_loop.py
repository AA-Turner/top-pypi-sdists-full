"""``sources.resolve`` scans a source body for secrets OFF the event loop.

Live 2026-11-07 (event_loop_stall f4c375ed, workflow-worker, 22 stalls in one process, worst 7.2 s):
``resolve`` called ``guard_text`` directly, and ``find_secrets`` runs every detector regex over the
whole body - pure CPU. On a large source the ingest step froze the worker's loop: no other step, no
heartbeat, no pool checkout ran for 1-7 s. RED before: the scan ran on the loop thread.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest
from matrx_rag import sources

NOTE_ID = "00000000-0000-4000-8000-00000000feed"
USER_ID = "00000000-0000-4000-8000-0000000000aa"
ENV_NOTE = "my .env backup\n\nADMIN_API_TOKEN=9f8b7a6c5d4e3f2a1b0c9d8e7f6a5b4c\nPORT=8000\n"


def _install_fake_notes(monkeypatch: pytest.MonkeyPatch, content: str) -> None:
    """Stand in for the ORM's Notes model with ONE row holding ``content``."""

    class _NotesQuery:
        async def values(self, *fields: str) -> list[dict[str, object]]:
            return [
                {
                    "id": NOTE_ID,
                    "created_by": USER_ID,
                    "organization_id": "00000000-0000-4000-8000-0000000000bb",
                    "label": "env backup",
                    "content": content,
                    "home_scope_id": None,
                    "tags": None,
                    "metadata": {},
                }
            ]

    class _Notes:
        @classmethod
        def filter(cls, **kwargs: object) -> _NotesQuery:
            return _NotesQuery()

    monkeypatch.setattr(sources, "get_db_model", lambda name: _Notes)


def _on_loop_thread() -> bool:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return False
    return True


@pytest.mark.asyncio
async def test_the_secret_scan_never_runs_on_the_loop(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_fake_notes(monkeypatch, ENV_NOTE)
    seen: list[bool] = []
    real_guard = sources.guard_text

    def spy_guard(*a: Any, **k: Any) -> Any:
        seen.append(_on_loop_thread())
        return real_guard(*a, **k)

    monkeypatch.setattr(sources, "guard_text", spy_guard)

    resolved = await sources.resolve("note", NOTE_ID, user_id=USER_ID)

    assert seen == [False], "guard_text ran on the event loop thread"
    # The guard still did its job from the thread: values gone, count recorded.
    assert resolved is not None
    assert "ADMIN_API_TOKEN=<redacted:ADMIN_API_TOKEN>" in resolved.text
    assert resolved.metadata.get("secrets_redacted") == 1
    assert "9f8b7a6c5d4e3f2a1b0c9d8e7f6a5b4c" not in resolved.text


@pytest.fixture(autouse=True)
def _the_access_check_lets_the_reader_in(monkeypatch):
    """Indexing follows ``iam.has_access_for`` (matrx_orm.platform_access_check), not ``created_by``;
    the policy itself is proved in test_resolvers_follow_the_access_check.py."""
    import matrx_orm

    async def _allowed(*_a, **_k):
        return True

    monkeypatch.setattr(matrx_orm, "platform_access_check", _allowed)
