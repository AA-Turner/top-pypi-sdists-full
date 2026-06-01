"""Smoke tests for `efterlev.cli.readiness_cli.run_readiness`.

Exercises the CLI wrapper (exit codes, JSON shape, scorecard render, strict-gate
exit semantics) — complements `test_readiness_score.py` / `test_readiness_gate.py`
which cover the underlying primitive math.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from efterlev.cli.readiness_cli import run_readiness
from efterlev.frmr.loader import FrmrDocument
from efterlev.models.indicator import Indicator, Theme


def _seed_frmr_cache(root: Path) -> None:
    """Write a minimal FrmrDocument to the workspace's FRMR cache path.

    Two indicators is enough to drive both the readiness math (denominator > 0)
    and the strict-gate per-KSI loop.
    """
    cache_dir = root / ".efterlev" / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    doc = FrmrDocument(
        version="0.9.43-beta",
        last_updated="2026-04-08",
        themes={
            "SVC": Theme(id="SVC", name="Service Configuration"),
            "AFR": Theme(id="AFR", name="Application + Foundation Resources"),
        },
        indicators={
            "KSI-SVC-SNT": Indicator(
                id="KSI-SVC-SNT",
                theme="SVC",
                name="Securing Network Traffic",
                statement="Encrypt traffic between system components.",
            ),
            "KSI-AFR-PER": Indicator(
                id="KSI-AFR-PER",
                theme="AFR",
                name="Personnel Security",
                statement="Background-check personnel with privileged access.",
            ),
        },
    )
    (cache_dir / "frmr_document.json").write_text(doc.model_dump_json(), encoding="utf-8")


def _seed_store(
    root: Path,
    *,
    classifications: dict[str, str] | None = None,
) -> None:
    """Build the SQLite + blob store readiness reads from.

    Same shape as `tests/test_readiness_score.py::_seed_workspace`; kept local
    so the two test files stay independently runnable.
    """
    efterlev = root / ".efterlev"
    efterlev.mkdir(parents=True, exist_ok=True)
    (efterlev / "manifests").mkdir(exist_ok=True)
    blob_dir = efterlev / "store"
    blob_dir.mkdir(exist_ok=True)

    conn = sqlite3.connect(efterlev / "store.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS provenance_records ("
        "record_id TEXT PRIMARY KEY, record_type TEXT, content_ref TEXT, "
        "derived_from TEXT, primitive TEXT, agent TEXT, model TEXT, "
        "prompt_hash TEXT, timestamp TEXT, metadata TEXT)"
    )
    if classifications:
        for i, (ksi_id, status) in enumerate(classifications.items()):
            blob_rel = f"cl{i}.json"
            (blob_dir / blob_rel).write_text(
                json.dumps({"content": {"ksi_id": ksi_id, "status": status}}),
                encoding="utf-8",
            )
            conn.execute(
                "INSERT INTO provenance_records "
                "(record_id, record_type, content_ref, derived_from, "
                "primitive, timestamp, metadata) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    f"cl{i}",
                    "claim",
                    blob_rel,
                    "[]",
                    "gap_agent@0.1.0",
                    f"2026-05-27T00:00:{i:02d}Z",
                    json.dumps({"ksi_id": ksi_id, "kind": "ksi_classification"}),
                ),
            )
    conn.commit()
    conn.close()


def test_returns_1_when_frmr_cache_missing(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Missing FRMR cache → fail with stderr nudge to run init."""
    rc = run_readiness(tmp_path)
    assert rc == 1
    err = capsys.readouterr().err
    assert "FRMR cache missing" in err
    assert "efterlev init" in err


def test_default_mode_renders_scorecard(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Happy default path: scorecard rendered, exit 0."""
    _seed_frmr_cache(tmp_path)
    _seed_store(tmp_path, classifications={"KSI-SVC-SNT": "implemented"})

    rc = run_readiness(tmp_path)
    out = capsys.readouterr().out

    assert rc == 0
    assert "Readiness for FedRAMP 20x Moderate" in out
    assert "Score" in out
    assert "KSI coverage" in out
    assert "When ready" in out


def test_json_mode_emits_stable_keys(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """`--json` shape is the downstream-consumer contract — pin it."""
    _seed_frmr_cache(tmp_path)
    _seed_store(tmp_path, classifications={"KSI-SVC-SNT": "implemented"})

    rc = run_readiness(tmp_path, json_output=True)
    out = capsys.readouterr().out

    assert rc == 0
    payload = json.loads(out)
    assert set(payload.keys()) >= {
        "score",
        "ksi_classifications_total",
        "ksis_in_baseline",
        "open_poam",
        "detectors_fired",
        "manifests_loaded",
        "top_blockers",
    }
    assert set(payload["score"].keys()) >= {
        "overall_pct",
        "ksi_coverage_pct",
        "manifest_coverage_pct",
        "severity_penalty_pct",
        "band_label",
    }
    assert set(payload["open_poam"].keys()) == {"high", "medium", "low"}


def test_strict_mode_returns_2_on_empty_workspace(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Strict RFC-0017 gate on an empty workspace: every KSI fails → exit 2.

    Exit 2 (not 1) is the documented "gate-fail vs tool-error" split — pre-
    submission CI keys off it. Cadence config is missing, which surfaces as a
    stderr warning but does not flip the exit code.
    """
    _seed_frmr_cache(tmp_path)
    _seed_store(tmp_path)  # no classifications, no cadence config

    rc = run_readiness(tmp_path, strict=True)
    captured = capsys.readouterr()

    assert rc == 2
    assert "RFC-0017 readiness gate" in captured.out
    assert "FAIL" in captured.out


def test_strict_mode_json_exits_2_and_emits_gate_shape(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Strict mode with `--json` returns the gate-report shape verbatim."""
    _seed_frmr_cache(tmp_path)
    _seed_store(tmp_path)

    rc = run_readiness(tmp_path, json_output=True, strict=True)
    out = capsys.readouterr().out

    assert rc == 2
    payload = json.loads(out)
    assert payload["passed"] is False
    assert payload["baseline_ksi_count"] == 2  # the two seeded indicators
    assert "ksi_results" in payload
    assert all("ksi_id" in k and "failed_items" in k for k in payload["ksi_results"])
