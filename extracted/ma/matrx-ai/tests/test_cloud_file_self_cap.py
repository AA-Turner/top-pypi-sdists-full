"""`cloud_file` list / batch_get bound their own result.

Production (ops ``tool_result_overflow:cloud_file``, 2026-09-01): ``action='list'``
with ``limit=80`` returned 71,649 chars of full file rows. Both multi-row actions
now carry at most ``CLOUD_FILE_RESULT_MAX_CHARS`` of rows and name the exact
continuation (``next_offset`` / ``not_returned``).
"""

from __future__ import annotations

import json
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.tools.implementations import cloud_files
from matrx_ai.tools.output_caps import TOOL_RESULT_SOFT_CAP_CHARS
from matrx_ai.tools.result_gate import _SINKS, apply_size_gate, register_tool_result_gate_sink


def _file(i: int) -> dict[str, Any]:
    return {
        "id": f"00000000-0000-4000-8000-{i:012d}",
        "file_name": f"scan-{i:03d}.pdf",
        "file_path": f"/users/u/documents/2026/cases/scan-{i:03d}.pdf",
        "mime_type": "application/pdf",
        "metadata": {"ocr": {"pages": 12, "summary": "s" * 650}},
    }


class _DB:
    def __init__(self, n: int):
        self.rows = [_file(i) for i in range(n)]

    async def list_files_filtered_async(self, user_id, *, folder_id, mime_prefix, offset, limit):
        return self.rows[offset : offset + limit]


@pytest.fixture
def db(monkeypatch):
    fake = _DB(200)
    monkeypatch.setattr(cloud_files, "_get_file_db", lambda: fake)

    async def fetch_one(_db, fid, user_id):
        return next((r for r in fake.rows if r["id"] == fid), None)

    monkeypatch.setattr(cloud_files, "_fetch_one", fetch_one)
    return fake


@pytest.fixture
def gate_events():
    events = []
    register_tool_result_gate_sink(events.append)
    yield events
    _SINKS.remove(events.append)


def _ctx() -> SimpleNamespace:
    return SimpleNamespace(call_id="c-cf", user_id="u")


def _wire(result) -> str:
    cd, truncated = apply_size_gate(
        result.to_tool_result_content(),
        output_self_capped=result.output_self_capped,
        tool_name="cloud_file",
        tool_kind="native",
        conversation_id="c",
        user_id="u",
    )
    assert truncated is False
    return cd["content"]


async def test_list_limit_80_is_bounded_with_exact_continuation(db, gate_events) -> None:
    r = await cloud_files.cloud_file({"action": "list", "limit": 80}, _ctx())
    assert r.success and r.output_self_capped
    out = r.output
    assert out["truncated"] is True and out["fetched"] == 80
    assert out["next_offset"] == out["count"] < 80
    assert f"offset={out['count']}" in out["note"]
    assert len(_wire(r)) < TOOL_RESULT_SOFT_CAP_CHARS
    assert gate_events == []
    # The continuation resumes exactly where the page stopped.
    r2 = await cloud_files.cloud_file({"action": "list", "limit": 80, "offset": out["next_offset"]}, _ctx())
    assert r2.output["files"][0]["id"] == db.rows[out["count"]]["id"]


async def test_batch_get_names_what_it_did_not_return(db, gate_events) -> None:
    ids = [r["id"] for r in db.rows[:90]]
    r = await cloud_files.cloud_file({"action": "batch_get", "file_ids": ids}, _ctx())
    out = r.output
    assert out["truncated"] is True
    assert out["count"] + len(out["not_returned"]) == 90
    assert [f["id"] for f in out["files"]] + out["not_returned"] == ids
    assert len(_wire(r)) < TOOL_RESULT_SOFT_CAP_CHARS
    assert gate_events == []


async def test_small_list_is_unchanged(db) -> None:
    r = await cloud_files.cloud_file({"action": "list", "limit": 5}, _ctx())
    assert r.output["count"] == 5 and "truncated" not in r.output
    assert r.output["next_offset"] == 5  # full page → more may exist
