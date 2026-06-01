"""Maintainer-validation test for the v0.1.120 extended Config fixture.

Mirrors `tests/test_security_hub_extended_fixture.py` (v0.1.119) but
for AWS Config evaluations. Same regression-gate posture: deterministic
ingest, ground-truth-locked expected output, fails when the mapping
table changes without a corresponding GROUND_TRUTH.yaml refresh.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from efterlev.imports.config import (
    IngestConfigInput,
    ingest_config,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = REPO_ROOT / "evals/fixtures/config-evaluations-extended"


def _load_ground_truth() -> dict:
    return yaml.safe_load((FIXTURE_DIR / "GROUND_TRUTH.yaml").read_text(encoding="utf-8"))


def _ingest() -> object:
    return ingest_config(IngestConfigInput(config_path=FIXTURE_DIR / "evaluations.json"))


def test_aggregate_counts_match_ground_truth() -> None:
    gt = _load_ground_truth()["expected_ingest"]
    out = _ingest()
    assert out.evaluations_total == gt["evaluations_total"], (
        f"evaluations_total {out.evaluations_total} != expected {gt['evaluations_total']}"
    )
    assert out.evaluations_emitted == gt["evidence_emitted"], (
        f"evidence_emitted {out.evaluations_emitted} != expected {gt['evidence_emitted']}"
    )
    assert out.skipped_insufficient_data == gt["skipped_insufficient_data"], (
        f"skipped INSUFFICIENT_DATA {out.skipped_insufficient_data} != "
        f"expected {gt['skipped_insufficient_data']}"
    )


def test_skipped_unmapped_config_rule_names_match_ground_truth() -> None:
    gt = _load_ground_truth()["expected_ingest"]
    out = _ingest()
    actual_skipped = sorted(out.skipped_unmapped_config_rule_names)
    expected_skipped = sorted(gt["skipped_unmapped_config_rule_names"])
    assert actual_skipped == expected_skipped, (
        f"skipped-unmapped mismatch.\nactual:   {actual_skipped}\nexpected: {expected_skipped}"
    )


def test_per_config_rule_mappings_match_ground_truth() -> None:
    """Per (Config rule name) — count + KSI list + control list match the ground truth."""
    gt = _load_ground_truth()["expected_mappings"]
    out = _ingest()

    by_rule: dict[str, list] = {}
    for ev in out.evidence:
        rule = ev.content.get("config_rule_name", "")
        by_rule.setdefault(rule, []).append(ev)

    for rule, expected in gt.items():
        evs = by_rule.get(rule, [])
        assert len(evs) == expected["evaluations_count"], (
            f"{rule}: emitted {len(evs)} Evidence records, expected {expected['evaluations_count']}"
        )
        for ev in evs:
            assert sorted(ev.ksis_evidenced) == sorted(expected["ksis"]), (
                f"{rule}: ksis_evidenced {ev.ksis_evidenced} != {expected['ksis']}"
            )
            assert sorted(ev.controls_evidenced) == sorted(expected["controls"]), (
                f"{rule}: controls_evidenced {ev.controls_evidenced} != {expected['controls']}"
            )


def test_no_unexpected_config_rules_emitted() -> None:
    """Every emitted Evidence's Config rule name appears in the ground truth."""
    gt = _load_ground_truth()["expected_mappings"]
    out = _ingest()
    expected_rules = set(gt.keys())
    actual_rules = {ev.content.get("config_rule_name", "") for ev in out.evidence}
    extra = actual_rules - expected_rules
    assert not extra, f"emitted Evidence for unexpected Config rules: {extra}"


def test_each_emitted_evidence_carries_required_content_fields() -> None:
    """Sanity check: ingest output preserves the canonical content fields."""
    out = _ingest()
    required_keys = {
        "import_source",
        "config_rule_name",
        "config_compliance_type",
        "config_resource_type",
        "config_resource_id",
        "evidence_strength",
        "mapping_title",
    }
    for ev in out.evidence:
        missing = required_keys - set(ev.content.keys())
        assert not missing, f"Evidence {ev.evidence_id} missing content keys: {missing}"
        assert ev.content["import_source"] == "aws.config.evaluations"


def test_compliance_type_distribution_matches_input() -> None:
    """Sanity check: emitted Evidence preserves both COMPLIANT + NON_COMPLIANT."""
    out = _ingest()
    types = {ev.content["config_compliance_type"] for ev in out.evidence}
    assert "COMPLIANT" in types
    assert "NON_COMPLIANT" in types
