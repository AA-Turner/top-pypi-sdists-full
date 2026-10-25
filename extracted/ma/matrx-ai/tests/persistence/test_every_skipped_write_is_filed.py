"""A row the persist path cannot write is never only a log line (the persistence law).

Every skip path in ``db/persistence.py`` (a row or a row's update it gave up on: an
unresolvable model FK, a missing conversation/request id, a failed tool-call backfill, a failed
pointer update, a reserved message it could not close) must file a ``run_history_write_failure``
through ``surface_skipped_write``. Found 2026-10-24: a device run on a person's own model file
wrote no chat.request row ("ai_model_id unresolvable") and filed nothing.

* the class: every skip log in the module is followed by ``surface_skipped_write`` and every
  listed stage is used (a new skip that only logs is red);
* the door: ``surface_skipped_write`` files a ``run_history_write_failure`` for a stored run.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

SOURCE = Path(__file__).resolve().parents[2] / "matrx_ai" / "db" / "persistence.py"
SKIP_LOG = re.compile(
    r"Skipping cx_request INSERT|No valid conversation_id to update|No valid request_id|"
    r"cx_tool_call backfill error|tool pointer block update error|Failed to close reserved message"
)


def test_every_skip_log_is_followed_by_a_filed_write_failure() -> None:
    lines = SOURCE.read_text().split("\n")
    hits = [i for i, line in enumerate(lines) if SKIP_LOG.search(line)]
    assert len(hits) >= 6, f"the skip census moved: {hits}"
    missing = [
        f"persistence.py:{i + 1}"
        for i in hits
        if not any("surface_skipped_write(" in lines[j] for j in range(i, min(i + 8, len(lines))))
    ]
    assert missing == [], f"a skip that only logs (persistence law): {missing}"


def test_every_listed_stage_is_filed_somewhere() -> None:
    from matrx_ai.db.persistence import SKIPPED_WRITE_STAGES

    text = SOURCE.read_text()
    for stage in SKIPPED_WRITE_STAGES:
        assert re.search(rf'surface_skipped_write\(\s*"{stage}"', text), stage


@pytest.mark.asyncio
async def test_a_skipped_write_files_a_run_history_write_failure(monkeypatch) -> None:
    from matrx_ai.db import persistence

    filed: list[dict] = []

    def record_error(exc, **kw):
        filed.append({"exc": exc, **kw})
        return None

    monkeypatch.setattr("matrx_ai._ext.get_ext", lambda name: record_error if name == "record_error" else None)
    monkeypatch.setattr(persistence, "stored_run_in_context", lambda: True)
    await persistence.surface_skipped_write(
        "cx_request_model_unresolvable", "no model", conversation_id="c-1", request_id="r-1"
    )
    assert len(filed) == 1
    assert filed[0]["kind"] == persistence.RUN_HISTORY_WRITE_FAILURE_KIND
    assert isinstance(filed[0]["exc"], persistence.SkippedPersistenceWrite)
    monkeypatch.setattr(persistence, "stored_run_in_context", lambda: False)
    await persistence.surface_skipped_write("cx_request_model_unresolvable", "no model")
    assert len(filed) == 1, "an unsaved run has no row to lose"
