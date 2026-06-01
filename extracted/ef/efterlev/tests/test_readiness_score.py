"""Tests for `efterlev.primitives.readiness.score` — readiness scoring heuristic."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from efterlev.primitives.readiness import compute_readiness


def _seed_workspace(
    root: Path,
    *,
    classifications: dict[str, str] | None = None,
    evidence_count: int = 0,
    manifest_count: int = 0,
) -> None:
    """Build a fake workspace with the records readiness needs to read.

    classifications maps ksi_id → status. evidence_count writes N
    placeholder evidence records. manifest_count creates N empty
    manifest YAML files.
    """
    efterlev = root / ".efterlev"
    efterlev.mkdir(parents=True, exist_ok=True)
    (efterlev / "manifests").mkdir(exist_ok=True)
    # Real path is `.efterlev/store/` (per ProvenanceStore.blob_dir). v0.1.146
    # caught that the readiness scorer was looking at `.efterlev/blobs/` — fixed
    # in score.py; tests now mirror the real layout.
    blob_dir = efterlev / "store"
    blob_dir.mkdir(exist_ok=True)

    # Use the real schema (provenance_records). content_ref points at a
    # blob file under .efterlev/store/; the test writes both the row AND
    # the blob so the scorer can read claim status from the payload.
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
                    f"2026-05-16T00:00:{i:02d}Z",
                    json.dumps({"ksi_id": ksi_id, "kind": "ksi_classification"}),
                ),
            )
    for i in range(evidence_count):
        conn.execute(
            "INSERT INTO provenance_records "
            "(record_id, record_type, content_ref, derived_from, primitive, timestamp, metadata) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                f"ev{i}",
                "evidence",
                f"ev{i}.json",
                "[]",
                "scan_terraform@0.1.0",
                "2026-05-16T00:00:00Z",
                "{}",
            ),
        )
    conn.commit()
    conn.close()

    for i in range(manifest_count):
        (efterlev / "manifests" / f"m{i}.yml").write_text("---\n", encoding="utf-8")


def test_uninitialized_workspace_returns_baseline_score(tmp_path: Path) -> None:
    """No classifications + no procedural KSIs + no opens:
    0% ksi_coverage * 0.5 + 100% manifest (no procedural) * 0.3 + 100% severity * 0.2 = 50.
    The score floor is non-zero because "no work done" looks identical to
    "no work needed" without classifications. The user sees "0/N ksis classified"
    in the scorecard so the meaning is clear; the numeric score isn't load-bearing
    when nothing has run.
    """
    report = compute_readiness(
        tmp_path, baseline_ksi_ids=["KSI-A", "KSI-B"], procedural_ksi_ids=set()
    )
    assert report.score.overall_pct == 50.0
    assert report.ksi_classifications_total == 0


def test_all_implemented_gives_high_score(tmp_path: Path) -> None:
    _seed_workspace(
        tmp_path,
        classifications={"KSI-A": "implemented", "KSI-B": "implemented"},
        evidence_count=10,
    )
    report = compute_readiness(
        tmp_path, baseline_ksi_ids=["KSI-A", "KSI-B"], procedural_ksi_ids=set()
    )
    # KSI coverage 100% * 0.5 + manifest 100% * 0.3 + severity 100% * 0.2 = 100
    assert report.score.overall_pct == 100.0
    assert report.score.band_label == "ready to package and engage a 3PAO"


def test_all_not_implemented_tanks_score(tmp_path: Path) -> None:
    _seed_workspace(
        tmp_path,
        classifications={f"KSI-A{i}": "not_implemented" for i in range(20)},
    )
    baseline = [f"KSI-A{i}" for i in range(20)]
    report = compute_readiness(tmp_path, baseline_ksi_ids=baseline, procedural_ksi_ids=set())
    # 20 opens * 5 = 100; severity penalty = 0
    # KSI coverage = 0 (all not_implemented count zero)
    # Manifest = 100 (no procedural)
    # Overall = 0*0.5 + 100*0.3 + 0*0.2 = 30
    assert report.score.overall_pct == 30.0
    assert report.open_poam_high == 20


def test_partial_counts_as_half(tmp_path: Path) -> None:
    _seed_workspace(tmp_path, classifications={"KSI-A": "partial", "KSI-B": "implemented"})
    report = compute_readiness(
        tmp_path, baseline_ksi_ids=["KSI-A", "KSI-B"], procedural_ksi_ids=set()
    )
    # KSI coverage = (0.5 + 1.0) / 2 * 100 = 75
    # Manifest = 100; severity = 100 - 0 high = 100 (1 medium doesn't penalize)
    # Overall = 75*0.5 + 100*0.3 + 100*0.2 = 87.5
    assert report.score.overall_pct == 87.5
    assert report.open_poam_medium == 1
    assert report.open_poam_high == 0


def test_procedural_ksis_need_manifests_for_full_credit(tmp_path: Path) -> None:
    """A workspace with all procedural KSIs classified inapplicable but no
    manifests should NOT score 100 — manifest coverage = 0."""
    _seed_workspace(
        tmp_path,
        classifications={
            "KSI-AFR-A": "evidence_layer_inapplicable",
            "KSI-AFR-B": "evidence_layer_inapplicable",
        },
        manifest_count=0,
    )
    report = compute_readiness(
        tmp_path,
        baseline_ksi_ids=["KSI-AFR-A", "KSI-AFR-B"],
        procedural_ksi_ids={"KSI-AFR-A", "KSI-AFR-B"},
    )
    # KSI coverage = 100 (both classified inapplicable)
    # Manifest coverage = 0 (no manifests for 2 procedural)
    # Severity = 100
    # Overall = 100*0.5 + 0*0.3 + 100*0.2 = 70
    assert report.score.manifest_coverage_pct == 0.0
    assert report.score.overall_pct == 70.0


def test_procedural_ksis_with_manifests_score_full(tmp_path: Path) -> None:
    _seed_workspace(
        tmp_path,
        classifications={
            "KSI-AFR-A": "evidence_layer_inapplicable",
            "KSI-AFR-B": "evidence_layer_inapplicable",
        },
        manifest_count=2,
    )
    report = compute_readiness(
        tmp_path,
        baseline_ksi_ids=["KSI-AFR-A", "KSI-AFR-B"],
        procedural_ksi_ids={"KSI-AFR-A", "KSI-AFR-B"},
    )
    assert report.score.manifest_coverage_pct == 100.0
    assert report.score.overall_pct == 100.0


def test_top_blockers_ranks_not_implemented_first(tmp_path: Path) -> None:
    _seed_workspace(
        tmp_path,
        classifications={
            "KSI-A": "not_implemented",
            "KSI-B": "not_implemented",
            "KSI-C": "not_implemented",
            "KSI-D": "implemented",
        },
    )
    report = compute_readiness(
        tmp_path,
        baseline_ksi_ids=["KSI-A", "KSI-B", "KSI-C", "KSI-D"],
        procedural_ksi_ids=set(),
    )
    assert len(report.top_blockers) == 3
    ksi_ids = {b.ksi_id for b in report.top_blockers}
    assert ksi_ids == {"KSI-A", "KSI-B", "KSI-C"}
    for b in report.top_blockers:
        assert "/agent remediate" in b.suggested_action


def test_score_tolerates_missing_store(tmp_path: Path) -> None:
    """No .efterlev/store.db → empty classifications, no crash."""
    report = compute_readiness(tmp_path, baseline_ksi_ids=["KSI-A"], procedural_ksi_ids=set())
    assert report.ksi_classifications_total == 0
    assert report.detectors_fired == 0
    assert report.manifests_loaded == 0


def test_readiness_finds_claims_in_real_blob_layout(tmp_path: Path) -> None:
    """v0.1.146 regression: readiness must read blobs from `.efterlev/store/`
    (the real ProvenanceStore.blob_dir), not `.efterlev/blobs/`.

    Customer hit this 2026-05-17: workspace had 306 claims in the store
    but /readiness reported "0 / 60 KSIs classified" — and suggested
    re-running scan + gap (which had already succeeded). Root cause:
    `_load_latest_claims` was looking at `.efterlev/blobs/` (nonexistent)
    instead of `.efterlev/store/` (real).

    This test exercises the actual sharded layout the store writes,
    not the test fixture's flat layout, so a future blob-path drift
    can't silently re-introduce the bug.
    """
    efterlev = tmp_path / ".efterlev"
    efterlev.mkdir()
    store_dir = efterlev / "store"
    store_dir.mkdir()

    # Write a claim blob at the real sharded path: ab/cd/abcd...json
    import hashlib

    claim_payload = json.dumps(
        {"content": {"ksi_id": "KSI-A", "status": "implemented"}}, sort_keys=True
    ).encode("utf-8")
    digest = hashlib.sha256(claim_payload).hexdigest()
    blob_subdir = store_dir / digest[:2] / digest[2:4]
    blob_subdir.mkdir(parents=True)
    blob_path = blob_subdir / f"{digest}.json"
    blob_path.write_bytes(claim_payload)
    content_ref = f"{digest[:2]}/{digest[2:4]}/{digest}.json"

    # Write the SQL row pointing at that blob.
    conn = sqlite3.connect(efterlev / "store.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS provenance_records ("
        "record_id TEXT PRIMARY KEY, record_type TEXT, content_ref TEXT, "
        "derived_from TEXT, primitive TEXT, agent TEXT, model TEXT, "
        "prompt_hash TEXT, timestamp TEXT, metadata TEXT)"
    )
    conn.execute(
        "INSERT INTO provenance_records "
        "(record_id, record_type, content_ref, derived_from, primitive, "
        "timestamp, metadata) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            "claim-1",
            "claim",
            content_ref,
            "[]",
            "gap_agent@0.1.0",
            "2026-05-17T00:00:00Z",
            json.dumps({"ksi_id": "KSI-A", "kind": "ksi_classification"}),
        ),
    )
    conn.commit()
    conn.close()

    report = compute_readiness(tmp_path, baseline_ksi_ids=["KSI-A"], procedural_ksi_ids=set())
    # Pre-v0.1.146 this returned 0 (blob lookup failed silently); fix
    # restores the expected 1.
    assert report.ksi_classifications_total == 1


def test_band_label_thresholds() -> None:
    """Verify the four band labels are hit by different overall scores."""
    from efterlev.primitives.readiness.score import ReadinessScore

    assert ReadinessScore(95, 100, 100, 100).band_label == "ready to package and engage a 3PAO"
    assert ReadinessScore(80, 90, 90, 90).band_label == "ready for 3PAO scoping conversation"
    assert (
        ReadinessScore(60, 70, 70, 70).band_label
        == "substantial work remaining; close the top blockers first"
    )
    assert (
        ReadinessScore(30, 30, 30, 30).band_label
        == "early; finish scan/gap and start authoring procedural manifests"
    )
    assert (
        ReadinessScore(5, 5, 5, 5).band_label
        == "not started — run /tour to walk through the pipeline"
    )
