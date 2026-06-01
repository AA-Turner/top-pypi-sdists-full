"""Tests for the eval-harness ground-truth schema + loader."""

from __future__ import annotations

from pathlib import Path

import pytest
from evals.ground_truth import GroundTruth, load_ground_truth

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "evals" / "fixtures"


def _write(tmp_path: Path, body: str) -> Path:
    p = tmp_path / "GROUND_TRUTH.yaml"
    p.write_text(body, encoding="utf-8")
    return p


def _minimal_yaml(**overrides: str) -> str:
    """Build a minimal valid GROUND_TRUTH.yaml string with overrides."""
    fields = {
        "fixture_id": "test-fixture",
        "description": "test fixture",
        "authored_by": "tester@example.com",
        "authored_at": "2026-05-08",
        "revision": "1",
        "frmr_version": "0.9.43-beta",
    }
    fields.update(overrides)
    body = "\n".join(f"{k}: {v}" for k, v in fields.items()) + "\n"
    return body


def test_load_minimal_ground_truth(tmp_path: Path) -> None:
    """A minimal valid ground-truth YAML loads + validates."""
    path = _write(tmp_path, _minimal_yaml())
    gt = load_ground_truth(path)
    assert gt.fixture_id == "test-fixture"
    assert gt.revision == 1
    assert gt.frmr_version == "0.9.43-beta"


def test_load_rejects_unsupported_frmr_version(tmp_path: Path) -> None:
    """Phase 1 fails closed on FRMR version mismatch (migration tool
    is Phase 2 work). Lock the fail-closed contract."""
    path = _write(tmp_path, _minimal_yaml(frmr_version="0.10.0-beta"))
    with pytest.raises(ValueError, match="not in supported set"):
        load_ground_truth(path)


def test_load_rejects_unrecognized_status(tmp_path: Path) -> None:
    """A typo in the status enum should fail the loader, not silently
    skip the KSI in metric calculation."""
    body = _minimal_yaml() + (
        "expected_classifications:\n  KSI-IAM-MFA: parshul\n"  # typo of 'partial'
    )
    path = _write(tmp_path, body)
    with pytest.raises(ValueError, match="unrecognized status"):
        load_ground_truth(path)


def test_load_accepts_status_alternation(tmp_path: Path) -> None:
    """The `<status1>|<status2>` alternation lets fixture authors
    express acceptable verdicts without committing to a single one.
    Resolves the sketch's open question on
    `evidence_layer_inapplicable` vs `not_applicable` for procedural-
    only KSIs."""
    body = _minimal_yaml() + (
        "expected_classifications:\n"
        "  KSI-CMT-RVP: evidence_layer_inapplicable|not_applicable\n"
        "  KSI-IAM-MFA: partial|not_implemented\n"
    )
    path = _write(tmp_path, body)
    gt = load_ground_truth(path)
    assert gt.acceptable_statuses("KSI-CMT-RVP") == {
        "evidence_layer_inapplicable",
        "not_applicable",
    }
    assert gt.acceptable_statuses("KSI-IAM-MFA") == {"partial", "not_implemented"}


def test_acceptable_statuses_returns_none_for_unlabeled_ksi(tmp_path: Path) -> None:
    """Unlabeled KSIs return None — metric functions skip these
    rather than penalizing. This is what lets fixture authors land
    partial labeling without forcing a 100% labeled corpus."""
    path = _write(tmp_path, _minimal_yaml())
    gt = load_ground_truth(path)
    assert gt.acceptable_statuses("KSI-NEVER-LABELED") is None


def test_poam_max_must_not_be_less_than_min(tmp_path: Path) -> None:
    """POAM expectations validation: excluded_count_max < min is a
    fixture-author error and should fail loading."""
    body = _minimal_yaml() + ("expected_poam:\n  excluded_count_min: 5\n  excluded_count_max: 2\n")
    path = _write(tmp_path, body)
    with pytest.raises(ValueError, match="excluded_count_max"):
        load_ground_truth(path)


def test_load_rejects_non_mapping_yaml(tmp_path: Path) -> None:
    """A YAML file that's a list / scalar / null at top-level fails
    cleanly with a descriptive error rather than a Pydantic stack
    trace."""
    p = tmp_path / "GROUND_TRUTH.yaml"
    p.write_text("- this is a list\n", encoding="utf-8")
    with pytest.raises(ValueError, match="expected a YAML mapping"):
        load_ground_truth(p)


def test_govnotes_v1_fixture_loads_clean() -> None:
    """The shipped govnotes-v1 fixture must load without errors. Locks
    that the schema and the fixture stay in sync (regression on either
    fails this test)."""
    gt = load_ground_truth(FIXTURES_DIR / "govnotes-v1" / "GROUND_TRUTH.yaml")
    assert gt.fixture_id == "govnotes-v1"
    assert gt.revision >= 1
    # Sanity check: the fixture labels a non-empty subset of KSIs.
    assert len(gt.expected_classifications) >= 5, (
        "govnotes-v1 should label at least the high-confidence baseline KSIs"
    )
    # Spot-check: the AFR-UCM mapping added in v0.1.42 should be labeled.
    assert "KSI-AFR-UCM" in gt.expected_classifications
    # Spot-check: alternation is parseable for procedural-only KSIs.
    cmt_rvp = gt.acceptable_statuses("KSI-CMT-RVP")
    assert cmt_rvp is not None
    assert "evidence_layer_inapplicable" in cmt_rvp


def _build_ground_truth(**classifications: str) -> GroundTruth:
    """Convenience: construct a GroundTruth from a kwarg-style mapping
    rather than YAML round-tripping. Used by the metrics tests."""
    return GroundTruth(
        fixture_id="test",
        description="test",
        authored_by="t@e",
        authored_at="2026-05-08",
        revision=1,
        frmr_version="0.9.43-beta",
        expected_classifications=dict(classifications),
    )


def test_build_ground_truth_helper_works() -> None:
    """Used by the metrics tests; confirm it actually constructs."""
    gt = _build_ground_truth(**{"KSI-IAM-MFA": "partial"})
    assert gt.acceptable_statuses("KSI-IAM-MFA") == {"partial"}
