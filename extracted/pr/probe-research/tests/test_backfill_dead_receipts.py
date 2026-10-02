"""Retiring a failed unit must retain the siblings with verified receipts."""

import json
from pathlib import Path

import pytest

from probe.cli import backfill_import as imp, import_jobs_ui, tui
from probe.cli.backfill_coverage import CoverageError
from probe.cli.backfill_ledger import Ledger, MAX_UNIT_ATTEMPTS
from tests import test_backfill_background as fixtures

background_harness = fixtures.background_harness


@pytest.mark.parametrize("legacy_marker", [False, True])
def test_partial_exhausted_unit_retries_only_the_sibling_without_a_receipt(
    background_harness, monkeypatch, legacy_marker,
):
    h, queued = background_harness
    (h.folder / "b.py").write_text("b = 2\n")
    h.run(background=True)
    payload = queued[0]
    ledger = Ledger(Path(payload["directory"]) / "units.jsonl")
    record, = ledger.read().units.values()
    for _ in range(MAX_UNIT_ATTEMPTS):
        ledger.start_unit(record.unit.unit_id)
        ledger.finish_unit(record.unit.unit_id, ok=False, error="synthetic agent failure")
    manifest = Path(payload["directory"]) / "manifests" / f"{record.unit.unit_id}.jsonl"
    manifest.write_text(json.dumps({"path": "a.py"}) + "\n")

    with pytest.raises(CoverageError, match="failed repeatedly"):
        imp.run_background_job(payload, progress=lambda *a, **k: None)
    assert h.report()["delivered"] == ["a.py"]
    assert h.report()["dead"] == ["b.py"]
    with h.coverage().writer() as coverage:
        delivered = coverage.rows_for(["a.py"])["a.py"]
        assert delivered["dead"] is None
        if legacy_marker:
            # A previous worker version could persist the successful receipt
            # without clearing the failed-unit marker on this current version.
            with coverage.conn:
                coverage.conn.execute("UPDATE files SET dead='old failure' WHERE path='a.py'")

    # Ordinary backfill preserves both the successful receipt and the cap;
    # only an explicit new review may retry the unfinished sibling.
    h.run()
    assert len(h.remote.calls) == 1 and len(h.classified) == 1
    assert h.report()["delivered"] == ["a.py"]
    reviews = []

    def review(title, lines, choices):
        reviews.append(title)
        return "import"

    monkeypatch.setattr(tui, "review", review)
    monkeypatch.setattr(import_jobs_ui, "show_started_import", lambda job: job)
    h.run(retry_dead=True, interactive=True, yes=False, background=True)
    assert "Review the import plan" in reviews
    assert h.classified == [["a.py", "b.py"], ["b.py"]]
    with h.coverage().writer() as coverage:
        retained = coverage.rows_for(["a.py"])["a.py"]
        for field in ("approved_hash", "project_id", "manifest", "correlation"):
            assert retained[field] == delivered[field]
    imp.run_background_job(queued[-1], progress=lambda *a, **k: None)
    h.run()
    assert h.report()["delivered"] == ["a.py", "b.py"]
    assert h.report()["dead"] == []
    assert sorted(call[1] for call in h.remote.calls) == ["a.py", "b.py"]


def test_old_receipt_cannot_clear_a_newly_approved_versions_failed_marker(background_harness):
    h, queued = background_harness
    h.run(background=True)
    imp.run_background_job(queued[0], progress=lambda *a, **k: None)
    with h.coverage().writer() as coverage:
        original = coverage.rows_for(["a.py"])["a.py"]
        receipt = h.client.delivery_state(original["correlation"])
        (h.folder / "a.py").write_text("a new approved version\n")
        coverage.observe(h.folder, ["a.py"])
        coverage.approve({"a.py": h.projects[original["project_id"]]}, changed=True)
        coverage.mark_dead(["a.py"], "new version failed")
        replacement = coverage.rows_for(["a.py"])["a.py"]
        assert replacement["approved_hash"] != original["approved_hash"]

        coverage.accept_receipt(original["correlation"], receipt)
        assert coverage.rows_for(["a.py"])["a.py"] == replacement
        assert coverage.report()["dead"] == ["a.py"]
