"""A run_log write that the database refuses is captured as an error — never only a log line.

Live 2026-10-28 (Track answers, run a085c304): a review issue owned by another organization made the
database refuse every later flag on the shared workflow; write_run_log returned recorded=False and the
run went on with nothing but a log line. The recorder still never fails the run.
"""

from __future__ import annotations

from typing import Any

import matrx_graph.run_log as run_log


class _Rows:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self.rows = rows

    async def values(self, *_: str) -> list[dict[str, Any]]:
        return self.rows


class _Run:
    @staticmethod
    def filter(**_: Any) -> _Rows:
        return _Rows([{"definition_id": "def-1", "organization_id": "org-a"}])


class _RunLog:
    @staticmethod
    async def create_item(**_: Any) -> Any:
        raise RuntimeError("assert_same_org: run_log.issue_id points at a row in another organization")


async def test_a_refused_flag_is_captured_and_the_run_is_not_failed(monkeypatch: Any) -> None:
    import matrx_graph.db._registry as registry
    import matrx_utils

    monkeypatch.setattr(registry, "get_model", lambda name: {"WfRun": _Run, "WfRunLog": _RunLog}[name])

    async def no_entries(*_: Any, **__: Any) -> int:
        return 0

    monkeypatch.setattr(run_log, "run_log_count", no_entries)
    captured: list[dict[str, Any]] = []

    async def capture(exc: BaseException, *, kind: str, **fields: Any) -> None:
        captured.append({"kind": kind, **fields})

    monkeypatch.setattr(matrx_utils, "capture_error", capture)
    entry = await run_log.write_run_log(
        run_id="run-1", node_id="report_close_missed", step=3, attempt=1,
        label="answered_in_place_unmatched", message="named no question", severity="error",
        organization_id="org-a", needs_review=True, category="validation_failed", source="record_step",
    )
    assert entry.recorded is False and "assert_same_org" in (entry.not_recorded_reason or "")
    assert [c["kind"] for c in captured] == [run_log.NOT_RECORDED_ERROR_KIND], "a lost flag left no error row"
    assert captured[0]["context"]["label"] == "answered_in_place_unmatched"
