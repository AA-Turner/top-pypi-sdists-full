"""`fs_read` bounds its own result on every backend.

Production (ops ``tool_result_overflow:fs_read``, 07-07 → 09-05): whole-file reads
of page.html (423,130 chars), content-splitter-v2.ts (76,087), and
``limit=60000`` reads of catalog markdown (53K). The local and durable-VFS
branches read up to 1 MB by default. Every read now carries at most
``FS_READ_MAX_CHARS`` with ``truncated`` + ``next_offset`` to continue, and the
pages concatenate back to the exact file.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from matrx_ai.tools.implementations import filesystem, vfs_filesystem
from matrx_ai.tools.models import ToolContext
from matrx_ai.tools.output_caps import TOOL_RESULT_SOFT_CAP_CHARS
from matrx_ai.tools.result_gate import _SINKS, apply_size_gate, register_tool_result_gate_sink

BUDGET = getattr(filesystem, "FS_READ_MAX_CHARS", 40_000)
BODY = "".join(f"<div class='row-{i}'>é ünïcode {i}</div>\n" for i in range(12_000))  # ~400K


@pytest.fixture
def gate_events():
    events: list[Any] = []
    register_tool_result_gate_sink(events.append)
    yield events
    _SINKS.remove(events.append)


def _wire_len(result) -> int:
    cd, truncated = apply_size_gate(
        result.to_tool_result_content(),
        output_self_capped=result.output_self_capped,
        tool_name="fs_read",
        tool_kind="native",
        conversation_id="c",
        user_id="u",
    )
    assert truncated is False
    return len(cd["content"])


async def _read_all(read, **base: Any) -> tuple[str, list[Any]]:
    pages, parts, offset = [], [], 0
    while True:
        r = await read({"path": "page.html", "offset": offset, **base})
        assert r.success, r.error
        pages.append(r)
        parts.append(r.output["content"])
        if not r.output["truncated"]:
            return "".join(parts), pages
        offset = r.output["next_offset"]


@pytest.fixture
def local_fs(monkeypatch, tmp_path: Path):
    (tmp_path / "page.html").write_text(BODY, encoding="utf-8")
    monkeypatch.setattr(filesystem, "_should_use_durable_vfs", lambda: False)
    monkeypatch.setattr(filesystem, "get_active_sandbox", lambda: None)
    monkeypatch.setattr(filesystem, "_resolve_path", lambda rel, ctx: tmp_path / rel)
    ctx = ToolContext(call_id="c-fs", user_id="u")
    return lambda args: filesystem.fs_read(args, ctx)


@pytest.fixture
def vfs_fs(monkeypatch):
    class _VFS:
        async def _cat_file(self, path: str) -> bytes:
            return BODY.encode("utf-8")

    async def _get(ctx: Any) -> _VFS:
        return _VFS()

    monkeypatch.setattr(vfs_filesystem, "get_workspace_fs", _get)
    ctx = ToolContext(call_id="c-vfs", user_id="u")
    return lambda args: vfs_filesystem.fs_read(args, ctx)


@pytest.mark.parametrize("backend", ["local_fs", "vfs_fs"])
async def test_whole_file_read_is_one_bounded_page(request, gate_events, backend) -> None:
    read = request.getfixturevalue(backend)
    r = await read({"path": "page.html"})
    assert r.output_self_capped is True
    assert r.output["truncated"] is True
    assert len(r.output["content"].encode("utf-8")) <= BUDGET
    assert isinstance(r.output["next_offset"], int)
    assert _wire_len(r) < TOOL_RESULT_SOFT_CAP_CHARS
    assert gate_events == []


@pytest.mark.parametrize("backend", ["local_fs", "vfs_fs"])
async def test_a_larger_limit_is_clamped(request, backend) -> None:
    read = request.getfixturevalue(backend)
    r = await read({"path": "page.html", "limit": 60_000})
    assert len(r.output["content"].encode("utf-8")) <= BUDGET
    assert r.output["limit"] == BUDGET


@pytest.mark.parametrize("backend", ["local_fs", "vfs_fs"])
async def test_pages_reassemble_the_exact_file(request, backend) -> None:
    read = request.getfixturevalue(backend)
    text, pages = await _read_all(read)
    assert text == BODY  # no character split or lost at a page edge
    assert len(pages) > 1
    assert pages[-1].output["next_offset"] is None
