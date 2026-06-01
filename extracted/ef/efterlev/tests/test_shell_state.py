"""Tests for `efterlev.shell.state` — snapshot reading + next-step suggestion."""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path

from efterlev.shell.state import (
    WorkspaceSnapshot,
    format_cost_summary,
    format_status_summary,
    humanize_relative_time,
    read_snapshot,
    suggest_next,
)


def _make_workspace(
    root: Path,
    *,
    baseline: str | None = "fedramp-20x-moderate",
    evidence: int = 0,
    claims: int = 0,
    scan_ts: datetime | None = None,
    receipts: list[dict] | None = None,
) -> None:
    """Build a fake `.efterlev/` tree the snapshot reader can ingest."""
    efterlev = root / ".efterlev"
    efterlev.mkdir(parents=True, exist_ok=True)
    if baseline is not None:
        (efterlev / "config.toml").write_text(f'baseline = "{baseline}"\n', encoding="utf-8")
    # SQLite store with minimal records schema (record_type + primitive + timestamp).
    conn = sqlite3.connect(efterlev / "store.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS provenance_records ("
        "record_id TEXT PRIMARY KEY, record_type TEXT, primitive TEXT, timestamp TEXT)"
    )
    for i in range(evidence):
        conn.execute(
            "INSERT INTO provenance_records VALUES (?, ?, ?, ?)",
            (
                f"ev{i}",
                "evidence",
                "scan_terraform@0.1.0",
                (scan_ts or datetime.now(UTC)).isoformat(),
            ),
        )
    for i in range(claims):
        conn.execute(
            "INSERT INTO provenance_records VALUES (?, ?, ?, ?)",
            (f"cl{i}", "claim", "gap_agent@0.1.0", datetime.now(UTC).isoformat()),
        )
    conn.commit()
    conn.close()
    if receipts is not None:
        (efterlev / "receipts.log").write_text(
            "\n".join(json.dumps(r) for r in receipts) + "\n", encoding="utf-8"
        )


def test_read_snapshot_uninitialized(tmp_path: Path) -> None:
    snap = read_snapshot(tmp_path)
    assert snap.initialized is False
    assert snap.baseline is None
    assert snap.evidence_count is None


def test_read_snapshot_initialized_empty(tmp_path: Path) -> None:
    _make_workspace(tmp_path, evidence=0)
    snap = read_snapshot(tmp_path)
    assert snap.initialized is True
    assert snap.baseline == "fedramp-20x-moderate"
    assert snap.evidence_count == 0
    assert snap.claim_count == 0
    assert snap.last_scan_at is None


def test_read_snapshot_counts_evidence_and_claims(tmp_path: Path) -> None:
    _make_workspace(tmp_path, evidence=5, claims=3, scan_ts=datetime.now(UTC))
    snap = read_snapshot(tmp_path)
    assert snap.evidence_count == 5
    assert snap.claim_count == 3
    assert snap.last_scan_at is not None


def test_read_snapshot_reads_cost_receipts(tmp_path: Path) -> None:
    _make_workspace(
        tmp_path,
        evidence=1,
        receipts=[
            {
                "ts": datetime.now(UTC).isoformat(),
                "model": "claude-opus-4-7",
                "input_tokens": 10_000,
                "output_tokens": 2_000,
            },
            {
                "ts": datetime.now(UTC).isoformat(),
                "model": "claude-haiku-4-5",
                "input_tokens": 5_000,
                "output_tokens": 500,
            },
        ],
    )
    snap = read_snapshot(tmp_path)
    assert "claude-opus-4-7" in snap.cost_by_model
    assert "claude-haiku-4-5" in snap.cost_by_model
    assert snap.cost_by_model["claude-opus-4-7"][0] == 10_000
    assert snap.cost_by_model["claude-opus-4-7"][1] == 2_000


def test_read_snapshot_tolerates_malformed_config(tmp_path: Path) -> None:
    """A malformed config.toml should degrade to baseline=None, not crash."""
    (tmp_path / ".efterlev").mkdir()
    (tmp_path / ".efterlev/config.toml").write_text(
        "this is = not valid = toml\n", encoding="utf-8"
    )
    snap = read_snapshot(tmp_path)
    assert snap.initialized is True
    assert snap.baseline is None


# ── suggest_next ────────────────────────────────────────────────────────────


def _snap(**overrides) -> WorkspaceSnapshot:
    """Build a snapshot for suggest_next tests; overridable fields."""
    defaults = dict(
        root=Path("/tmp/x"),
        initialized=True,
        baseline="fedramp-20x-moderate",
        evidence_count=0,
        claim_count=0,
        last_scan_at=None,
        cost_by_model={},
    )
    defaults.update(overrides)
    return WorkspaceSnapshot(**defaults)  # type: ignore[arg-type]


def test_suggest_cd_when_uninitialized_and_no_iac_files(tmp_path) -> None:
    """v0.1.136: if the cwd has no IaC files, suggest /cd before /init."""
    s = suggest_next(
        _snap(
            root=tmp_path,
            initialized=False,
            baseline=None,
            evidence_count=None,
            claim_count=None,
        )
    )
    assert s is not None
    assert s.command == "/cd <repo-root>"
    assert "no .tf" in s.why


def test_suggest_init_when_uninitialized_and_iac_files_present(tmp_path) -> None:
    """v0.1.136: with IaC files present, /init is the right suggestion."""
    (tmp_path / "main.tf").write_text("# tf\n", encoding="utf-8")
    s = suggest_next(
        _snap(
            root=tmp_path,
            initialized=False,
            baseline=None,
            evidence_count=None,
            claim_count=None,
        )
    )
    assert s is not None
    assert s.command == "/init"


def test_suggest_scan_when_initialized_but_no_scan() -> None:
    s = suggest_next(_snap(last_scan_at=None))
    assert s is not None
    assert s.command == "/scan"


def test_suggest_gap_when_evidence_present_but_no_claims() -> None:
    s = suggest_next(_snap(evidence_count=10, claim_count=0, last_scan_at=datetime.now(UTC)))
    assert s is not None
    assert s.command == "/agent gap"


def test_suggest_report_when_evidence_and_claims_present() -> None:
    s = suggest_next(_snap(evidence_count=10, claim_count=60, last_scan_at=datetime.now(UTC)))
    assert s is not None
    assert s.command == "/report"


# v0.1.144 / #349: post-/report ladder advances past `/report` once its
# four artifacts (attestation + POA&M md + OSCAL POA&M + OSCAL CD) exist
# and are newer than the most recent scan.


def _make_report_artifacts(root: Path, *, fresh: bool = True) -> None:
    """Create the four artifact files `/report` produces under `.efterlev/reports/`.

    `fresh=True` writes them with current mtime; `fresh=False` writes them
    with an old mtime (10 minutes before now) so the recency check fails.
    """
    import os
    import time

    reports = root / ".efterlev" / "reports"
    (reports / "poam").mkdir(parents=True, exist_ok=True)
    (reports / "oscal").mkdir(parents=True, exist_ok=True)
    files = [
        reports / "attestation-20260516-210417.json",
        reports / "poam" / "poam-20260516-210418.md",
        reports / "oscal" / "poam-20260516-210418.json",
        reports / "oscal" / "component-definition-20260516-210418.json",
    ]
    for f in files:
        f.write_text("{}", encoding="utf-8")
    if not fresh:
        old = time.time() - 600
        for f in files:
            os.utime(f, (old, old))


def test_suggest_readiness_after_report_artifacts_present(tmp_path) -> None:
    """v0.1.144 / #349: after `/report` has produced all four artifacts
    newer than the last scan, advance the suggestion to `/readiness` and
    `/package` — not back to `/report` again (the prior bug).
    """
    _make_report_artifacts(tmp_path, fresh=True)
    s = suggest_next(
        _snap(
            root=tmp_path,
            evidence_count=10,
            claim_count=60,
            last_scan_at=datetime.now(UTC) - timedelta(minutes=12),
        )
    )
    assert s is not None
    assert s.command == "/readiness"
    assert "/package" in s.why


def test_suggest_none_after_submission_package_built(tmp_path) -> None:
    """End of the pipeline: when the submission ZIP exists newer than the
    last scan, the Next hint drops to None rather than nag."""
    _make_report_artifacts(tmp_path, fresh=True)
    submissions = tmp_path / ".efterlev" / "submissions"
    submissions.mkdir(parents=True, exist_ok=True)
    (submissions / "submission-20260516-210500.zip").write_text("", encoding="utf-8")
    s = suggest_next(
        _snap(
            root=tmp_path,
            evidence_count=10,
            claim_count=60,
            last_scan_at=datetime.now(UTC) - timedelta(minutes=12),
        )
    )
    assert s is None


def test_suggest_report_again_when_scan_is_newer_than_artifacts(tmp_path) -> None:
    """If the user re-runs `/scan` after a `/report`, the artifacts are
    stale relative to the new scan. The ladder should drop back to
    `/report` because the bundle no longer reflects the latest evidence.
    """
    _make_report_artifacts(tmp_path, fresh=False)  # artifacts mtime = 10 min ago
    s = suggest_next(
        _snap(
            root=tmp_path,
            evidence_count=10,
            claim_count=60,
            # last_scan_at is RIGHT NOW (newer than the stale artifacts)
            last_scan_at=datetime.now(UTC),
        )
    )
    assert s is not None
    assert s.command == "/report"


def test_suggest_report_when_only_some_report_artifacts_present(tmp_path) -> None:
    """Partial `/report` run (e.g. interrupted mid-pipeline) — the ladder
    requires all four artifacts to advance. Missing OSCAL means we
    haven't completed the bundle."""
    reports = tmp_path / ".efterlev" / "reports"
    (reports / "poam").mkdir(parents=True, exist_ok=True)
    (reports / "attestation-x.json").write_text("{}", encoding="utf-8")
    (reports / "poam" / "poam-x.md").write_text("", encoding="utf-8")
    # No oscal/ directory; report bundle incomplete.
    s = suggest_next(
        _snap(
            root=tmp_path,
            evidence_count=10,
            claim_count=60,
            last_scan_at=datetime.now(UTC) - timedelta(minutes=12),
        )
    )
    assert s is not None
    assert s.command == "/report"


# ── formatters ──────────────────────────────────────────────────────────────


def test_humanize_relative_time_just_now() -> None:
    assert humanize_relative_time(datetime.now(UTC)) == "just now"


def test_humanize_relative_time_minutes() -> None:
    ts = datetime.now(UTC) - timedelta(minutes=5)
    assert humanize_relative_time(ts) == "5m ago"


def test_humanize_relative_time_hours() -> None:
    ts = datetime.now(UTC) - timedelta(hours=3)
    assert humanize_relative_time(ts) == "3h ago"


def test_humanize_relative_time_days() -> None:
    ts = datetime.now(UTC) - timedelta(days=2)
    assert humanize_relative_time(ts) == "2d ago"


def test_format_status_summary_uninitialized() -> None:
    s = _snap(initialized=False, evidence_count=None, claim_count=None)
    assert "no .efterlev/" in format_status_summary(s)


def test_format_status_summary_with_scan() -> None:
    out = format_status_summary(
        _snap(evidence_count=23, claim_count=60, last_scan_at=datetime.now(UTC))
    )
    assert "23 evidence records" in out
    assert "60 claims" in out
    assert "last scan just now" in out


def test_format_cost_summary_empty_returns_none() -> None:
    assert format_cost_summary(_snap()) is None


def test_format_cost_summary_single_model() -> None:
    s = _snap(cost_by_model={"claude-opus-4-7": (10_000, 2_000, 1.23)})
    out = format_cost_summary(s)
    assert out is not None
    assert "$1.23" in out
    # _short_model_name strips "claude-" prefix.
    assert "opus-4-7" in out


def test_format_cost_summary_multi_model() -> None:
    s = _snap(
        cost_by_model={
            "claude-opus-4-7": (10_000, 2_000, 1.23),
            "claude-haiku-4-5": (5_000, 500, 0.04),
        }
    )
    out = format_cost_summary(s)
    assert out is not None
    assert "$1.23" in out
    assert "$0.04" in out
    assert "$1.27 total" in out


# v0.1.151 / #356: cost line is backend-aware for subscription.


def test_format_cost_summary_subscription_with_no_history_returns_subscription_marker() -> None:
    """Fresh workspace on claude_code with zero receipts. The cost-by-model
    dict is empty; before v0.1.151 this would return None and no Cost line
    would show. Now it returns a subscription marker so the user sees a
    clear signal that calls bill against the subscription."""
    s = _snap(llm_backend="claude_code")
    out = format_cost_summary(s)
    assert out == "subscription (no per-call billing)"


def test_format_cost_summary_subscription_collapses_zero_cost_run() -> None:
    """After a subscription run, ClaudeCodeClient writes tokens=0 so
    cost rolls up to $0. Without the v0.1.151 fix we'd print
    `$0.00 sonnet-4-6` which reads as 'this run was free' rather than
    'you're on subscription'. New behavior: collapse to the
    subscription marker."""
    s = _snap(
        llm_backend="claude_code",
        cost_by_model={"claude-sonnet-4-6": (0, 0, 0.0)},
    )
    out = format_cost_summary(s)
    assert out == "subscription (no per-call billing)"


def test_format_cost_summary_subscription_preserves_legacy_cost_with_marker() -> None:
    """User switched from API to subscription mid-workspace. Historical
    receipts (real $) get shown; a `subscription active` tag clarifies
    that NEW calls bill $0."""
    s = _snap(
        llm_backend="claude_code",
        cost_by_model={"claude-sonnet-4-6": (10_000, 2_000, 1.23)},
    )
    out = format_cost_summary(s)
    assert out is not None
    assert "$1.23" in out
    assert "subscription active" in out
    assert "new calls bill $0" in out
