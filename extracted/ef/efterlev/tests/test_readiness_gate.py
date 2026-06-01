"""Tests for `efterlev.primitives.readiness.gate` — RFC-0017 per-KSI gate.

The gate evaluates each baseline KSI against the 5 RFC-0017 PVA items:
implementation_goal, consolidated_inventory, automated_validation_cadence,
human_validation_cadence, current_status. Each test isolates one item or
one cross-cutting behavior (workspace-level cadence, evidence vs manifest
equivalence, etc.).

The store-seeding helper mirrors the layout `_load_classified_ksis` and
`_load_ksi_evidence_citations` read: `.efterlev/store.db` with rows in
`provenance_records`, blobs at `.efterlev/store/<content_ref>`.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from efterlev.primitives.readiness import compute_rfc_0017_gate


def _seed_workspace(
    root: Path,
    *,
    classifications: dict[str, str] | None = None,
    evidence_by_ksi: dict[str, int] | None = None,
    manifest_ksi_ids: list[str] | None = None,
) -> None:
    """Fake workspace populator.

    classifications maps ksi_id → status (any non-empty status counts for
    gate item 5; the gate doesn't care about the status value, only the
    record's existence).

    evidence_by_ksi maps ksi_id → count of Evidence records that cite it.
    Each Evidence blob carries `ksis_evidenced: [ksi_id]` at top level.

    manifest_ksi_ids names KSIs that have a signed manifest at
    `.efterlev/manifests/<ksi-id-lowercase>.yml`.
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
                    f"2026-05-19T00:00:{i:02d}Z",
                    json.dumps({"ksi_id": ksi_id, "kind": "ksi_classification"}),
                ),
            )

    if evidence_by_ksi:
        idx = 0
        for ksi_id, count in evidence_by_ksi.items():
            for _ in range(count):
                blob_rel = f"ev{idx}.json"
                (blob_dir / blob_rel).write_text(
                    json.dumps({"ksis_evidenced": [ksi_id]}),
                    encoding="utf-8",
                )
                conn.execute(
                    "INSERT INTO provenance_records "
                    "(record_id, record_type, content_ref, derived_from, "
                    "primitive, timestamp, metadata) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (
                        f"ev{idx}",
                        "evidence",
                        blob_rel,
                        "[]",
                        "scan_terraform@0.1.0",
                        "2026-05-19T00:00:00Z",
                        "{}",
                    ),
                )
                idx += 1

    conn.commit()
    conn.close()

    if manifest_ksi_ids:
        for ksi_id in manifest_ksi_ids:
            (efterlev / "manifests" / f"{ksi_id.lower()}.yml").write_text("---\n", encoding="utf-8")


# --- item-1: implementation_goal ---------------------------------------


def test_implementation_goal_always_passes(tmp_path: Path) -> None:
    """Item 1 is satisfied by the FRMR catalog. The gate accepts that
    every KSI in baseline has an implementation goal (catalog-vouched);
    the caller is responsible for only passing real catalog ids.
    """
    report = compute_rfc_0017_gate(
        tmp_path,
        baseline_ksi_ids=["KSI-A"],
        machine_validation_cadence="every PR",
        human_validation_cadence="quarterly",
    )
    [ksi] = report.ksi_results
    assert "implementation_goal" in ksi.passed_items


# --- item-2: consolidated_inventory ------------------------------------


def test_item_2_passes_with_evidence(tmp_path: Path) -> None:
    _seed_workspace(tmp_path, evidence_by_ksi={"KSI-A": 1})
    report = compute_rfc_0017_gate(
        tmp_path,
        baseline_ksi_ids=["KSI-A"],
        machine_validation_cadence="every PR",
        human_validation_cadence="quarterly",
    )
    [ksi] = report.ksi_results
    assert "consolidated_inventory" in ksi.passed_items


def test_item_2_passes_with_manifest_only(tmp_path: Path) -> None:
    """A procedural KSI with no Evidence but a signed manifest passes."""
    _seed_workspace(tmp_path, manifest_ksi_ids=["KSI-AFR-FSI"])
    report = compute_rfc_0017_gate(
        tmp_path,
        baseline_ksi_ids=["KSI-AFR-FSI"],
        machine_validation_cadence="every PR",
        human_validation_cadence="quarterly",
    )
    [ksi] = report.ksi_results
    assert "consolidated_inventory" in ksi.passed_items


def test_item_2_fails_without_evidence_or_manifest(tmp_path: Path) -> None:
    report = compute_rfc_0017_gate(
        tmp_path,
        baseline_ksi_ids=["KSI-A"],
        machine_validation_cadence="every PR",
        human_validation_cadence="quarterly",
    )
    [ksi] = report.ksi_results
    assert "consolidated_inventory" in ksi.failed_items
    assert "no Evidence record" in ksi.failure_details["consolidated_inventory"]


# --- items 3 + 4: workspace-level cadence ------------------------------


def test_empty_machine_cadence_fails_every_ksi(tmp_path: Path) -> None:
    _seed_workspace(
        tmp_path,
        classifications={"KSI-A": "implemented", "KSI-B": "implemented"},
        evidence_by_ksi={"KSI-A": 1, "KSI-B": 1},
    )
    report = compute_rfc_0017_gate(
        tmp_path,
        baseline_ksi_ids=["KSI-A", "KSI-B"],
        machine_validation_cadence="",
        human_validation_cadence="quarterly",
    )
    for ksi in report.ksi_results:
        assert "automated_validation_cadence" in ksi.failed_items
        assert "human_validation_cadence" in ksi.passed_items


def test_whitespace_only_cadence_treated_as_empty(tmp_path: Path) -> None:
    """A `[cadence].machine_validation_cadence = "   "` shouldn't sneak through."""
    report = compute_rfc_0017_gate(
        tmp_path,
        baseline_ksi_ids=["KSI-A"],
        machine_validation_cadence="   ",
        human_validation_cadence="quarterly",
    )
    [ksi] = report.ksi_results
    assert "automated_validation_cadence" in ksi.failed_items


def test_both_cadences_set_passes_items_3_and_4(tmp_path: Path) -> None:
    report = compute_rfc_0017_gate(
        tmp_path,
        baseline_ksi_ids=["KSI-A"],
        machine_validation_cadence="every PR",
        human_validation_cadence="quarterly",
    )
    [ksi] = report.ksi_results
    assert "automated_validation_cadence" in ksi.passed_items
    assert "human_validation_cadence" in ksi.passed_items


# --- item-5: current_status --------------------------------------------


def test_item_5_passes_for_any_classification_status(tmp_path: Path) -> None:
    """`not_implemented` is a valid current status. The gate only cares
    that a status has been declared, not what it is.
    """
    _seed_workspace(
        tmp_path,
        classifications={
            "KSI-A": "implemented",
            "KSI-B": "not_implemented",
            "KSI-C": "partial",
        },
    )
    report = compute_rfc_0017_gate(
        tmp_path,
        baseline_ksi_ids=["KSI-A", "KSI-B", "KSI-C"],
        machine_validation_cadence="every PR",
        human_validation_cadence="quarterly",
    )
    for ksi in report.ksi_results:
        assert "current_status" in ksi.passed_items


def test_item_5_fails_when_unclassified(tmp_path: Path) -> None:
    _seed_workspace(tmp_path, classifications={"KSI-A": "implemented"})
    report = compute_rfc_0017_gate(
        tmp_path,
        baseline_ksi_ids=["KSI-A", "KSI-B"],  # B not classified
        machine_validation_cadence="every PR",
        human_validation_cadence="quarterly",
    )
    by_id = {k.ksi_id: k for k in report.ksi_results}
    assert "current_status" in by_id["KSI-A"].passed_items
    assert "current_status" in by_id["KSI-B"].failed_items


# --- gate-level pass/fail aggregation ----------------------------------


def test_gate_passes_when_every_ksi_passes(tmp_path: Path) -> None:
    _seed_workspace(
        tmp_path,
        classifications={"KSI-A": "implemented", "KSI-B": "implemented"},
        evidence_by_ksi={"KSI-A": 1, "KSI-B": 1},
    )
    report = compute_rfc_0017_gate(
        tmp_path,
        baseline_ksi_ids=["KSI-A", "KSI-B"],
        machine_validation_cadence="every PR",
        human_validation_cadence="quarterly",
    )
    assert report.passed
    assert report.passing_count == 2
    assert report.failing_count == 0


def test_gate_fails_when_any_ksi_fails_any_item(tmp_path: Path) -> None:
    """One KSI with one missing item is enough to fail the entire gate."""
    _seed_workspace(
        tmp_path,
        classifications={"KSI-A": "implemented", "KSI-B": "implemented"},
        evidence_by_ksi={"KSI-A": 1},  # KSI-B has no evidence
    )
    report = compute_rfc_0017_gate(
        tmp_path,
        baseline_ksi_ids=["KSI-A", "KSI-B"],
        machine_validation_cadence="every PR",
        human_validation_cadence="quarterly",
    )
    assert not report.passed
    assert report.passing_count == 1
    assert report.failing_count == 1


def test_uninitialized_workspace_fails_everything_except_item_1(
    tmp_path: Path,
) -> None:
    """Fresh `efterlev init` (no scan, no agent gap, no manifests) plus
    default cadence strings should fail items 2 + 5 universally; cadence
    items 3 + 4 pass because the default `[cadence]` config is non-empty.
    """
    # No seed — no store, no manifests.
    report = compute_rfc_0017_gate(
        tmp_path,
        baseline_ksi_ids=["KSI-A", "KSI-B"],
        machine_validation_cadence="every PR via .github/workflows/...",
        human_validation_cadence="per manifest next_review",
    )
    assert not report.passed
    for ksi in report.ksi_results:
        assert "implementation_goal" in ksi.passed_items
        assert "automated_validation_cadence" in ksi.passed_items
        assert "human_validation_cadence" in ksi.passed_items
        assert "consolidated_inventory" in ksi.failed_items
        assert "current_status" in ksi.failed_items


def test_evidence_nested_under_output_wrapper_is_found(tmp_path: Path) -> None:
    """Primitive-wrapped Evidence ({"input":..., "output":{"evidence":[...]}})
    should be recognized by the gate just like top-level Evidence."""
    efterlev = tmp_path / ".efterlev"
    efterlev.mkdir(parents=True, exist_ok=True)
    (efterlev / "manifests").mkdir(exist_ok=True)
    blob_dir = efterlev / "store"
    blob_dir.mkdir(exist_ok=True)

    blob = {
        "input": {},
        "output": {"evidence": [{"ksis_evidenced": ["KSI-A"]}]},
    }
    (blob_dir / "ev0.json").write_text(json.dumps(blob), encoding="utf-8")

    conn = sqlite3.connect(efterlev / "store.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS provenance_records ("
        "record_id TEXT PRIMARY KEY, record_type TEXT, content_ref TEXT, "
        "derived_from TEXT, primitive TEXT, agent TEXT, model TEXT, "
        "prompt_hash TEXT, timestamp TEXT, metadata TEXT)"
    )
    conn.execute(
        "INSERT INTO provenance_records "
        "(record_id, record_type, content_ref, derived_from, primitive, timestamp, metadata) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        ("ev0", "evidence", "ev0.json", "[]", "scan_x@0.1.0", "2026-05-19T00:00:00Z", "{}"),
    )
    conn.commit()
    conn.close()

    report = compute_rfc_0017_gate(
        tmp_path,
        baseline_ksi_ids=["KSI-A"],
        machine_validation_cadence="every PR",
        human_validation_cadence="quarterly",
    )
    [ksi] = report.ksi_results
    assert "consolidated_inventory" in ksi.passed_items


def test_manifest_filename_case_insensitive_match(tmp_path: Path) -> None:
    """Manifest files are named `<ksi-id>.yml` lowercase; the gate accepts
    the canonical uppercase form in baseline_ksi_ids and finds them."""
    _seed_workspace(tmp_path, manifest_ksi_ids=["KSI-AFR-PSC"])
    # Manifest written as ksi-afr-psc.yml; baseline uses canonical uppercase
    report = compute_rfc_0017_gate(
        tmp_path,
        baseline_ksi_ids=["KSI-AFR-PSC"],
        machine_validation_cadence="every PR",
        human_validation_cadence="quarterly",
    )
    [ksi] = report.ksi_results
    assert "consolidated_inventory" in ksi.passed_items
