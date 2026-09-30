"""Both substitution tripwires report through ONE reporter, parameterized by kind.

Canonical audit (2026-09-29): ``picklist_runtime`` carried ``_report_unresolved`` and a
copy-pasted ``_report_unresolved_source_set`` — the same log line, error-capture seam,
detached task and loop fallback twice, on the hot path of every run. A fix to one (the
detached-task naming, the no-loop close) could never reach the other.
"""

from __future__ import annotations

import matrx_ai._ext as ext
from matrx_ai.config import picklist_runtime as pr


def _capture(monkeypatch) -> list[dict]:
    recorded: list[dict] = []

    def record_error(exc, **kw):  # sync recorder: no running loop needed
        recorded.append(kw)

    monkeypatch.setitem(ext._registry, "record_error", record_error)
    return recorded


def test_a_picklist_and_a_source_set_record_their_own_kind(monkeypatch) -> None:
    recorded = _capture(monkeypatch)
    pr.guard_unresolved_refs({"tone": {"type": "picklist_ref", "label": "Warm", "list_item_id": "i-1"}})
    pr.guard_unresolved_source_sets({"sources": {"__kind": "source_set", "sources": [{}]}})
    assert [(r["kind"], r["payload"]) for r in recorded] == [
        ("picklist_unresolved", {"variable": "tone"}),
        ("source_set_unresolved", {"variable": "sources"}),
    ]


def test_the_source_set_guard_uses_the_one_reporter(monkeypatch) -> None:
    calls: list[tuple] = []
    monkeypatch.setattr(pr, "_report_unresolved", lambda *a, **k: calls.append(a))
    pr.guard_unresolved_source_sets({"sources": {"__kind": "source_set", "sources": []}})
    assert calls == [("sources", "source_set_unresolved")]
    assert not hasattr(pr, "_report_unresolved_source_set")
