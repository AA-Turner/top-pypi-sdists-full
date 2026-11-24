"""`fs_search` over the durable VFS answers inside its dispatch room — never a 120 s system error.

Live 2026-11-12 (system_error c6beed97): a walk over a mounted cloud-files tree spent the whole
``agents.tool_dispatch`` ceiling resolving folder access row by row; the executor canceled it and the
agent got a system error with nothing. The walk now stops at ``dispatch_room_seconds`` and answers with
what it found so far, ``truncated`` and a plain ``stopped_reason``.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from matrx_ai.tools.implementations import vfs_filesystem
from matrx_ai.tools.models import ToolContext


class _SlowTreeVFS:
    """One file at the root, then a folder whose listing never comes back in time."""

    async def _isdir(self, path: str) -> bool:
        return True

    async def _walk(self, base: str, topdown: bool = True):
        yield base, ["slow"], ["found.md"]
        await asyncio.sleep(30)  # the mounted folder that resolves access one row at a time
        yield base + "/slow", [], ["late.md"]

    async def _info(self, path: str) -> dict[str, Any]:
        return {"size": 7}

    async def _cat_file(self, path: str) -> bytes:
        return b"needle"


@pytest.fixture
def slow_vfs(monkeypatch):
    async def _get(ctx: Any) -> _SlowTreeVFS:
        return _SlowTreeVFS()

    monkeypatch.setattr(vfs_filesystem, "get_workspace_fs", _get)
    monkeypatch.setattr(vfs_filesystem, "dispatch_room_seconds", lambda name: 0.2, raising=False)


@pytest.mark.parametrize("content_search", [False, True])
async def test_a_slow_walk_answers_with_what_it_found(slow_vfs, content_search: bool) -> None:
    ctx = ToolContext(call_id="c-fs-search", user_id="u")
    args = {"pattern": "needle" if content_search else "*.md", "path": ".", "content_search": content_search}
    result = await asyncio.wait_for(vfs_filesystem.fs_search(args, ctx), timeout=5)
    assert result.success, result.error
    assert [r["path"] for r in result.output["results"]] == ["found.md"]
    assert result.output["truncated"] is True
    assert "narrower path" in result.output["stopped_reason"]


def test_the_room_is_inside_the_ceiling(monkeypatch) -> None:
    from matrx_ai.tools import knobs
    from matrx_ai.tools.mcp_resilience import dispatch_room_seconds

    monkeypatch.setattr(knobs, "dispatch_timeout_ceiling", lambda name: 120.0)
    assert dispatch_room_seconds("fs_search") == pytest.approx(100.0)
