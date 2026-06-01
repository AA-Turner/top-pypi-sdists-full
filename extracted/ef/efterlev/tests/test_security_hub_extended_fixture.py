"""Maintainer-validation test for the v0.1.119 extended ASFF fixture.

Mirrors the CFN/TF eval-harness ground-truth-comparison pattern, but for
a deterministic ingest primitive: there's no LLM, so the "validation"
is structural — does the parser + mapping table produce exactly the
counts and per-control mappings the GROUND_TRUTH.yaml declares.

When the mapping table grows in v0.1.115.x batches, this test will
fail until either (a) the GROUND_TRUTH.yaml is updated to reflect the
new coverage, or (b) the new mappings move some findings from
unmapped → mapped. Failing here is the gate that catches "we expanded
the table but forgot to refresh the labeled fixture."
"""

from __future__ import annotations

from pathlib import Path

import yaml

from efterlev.imports.security_hub import (
    IngestSecurityHubInput,
    ingest_security_hub,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = REPO_ROOT / "evals/fixtures/security-hub-asff-extended"


def _load_ground_truth() -> dict:
    return yaml.safe_load((FIXTURE_DIR / "GROUND_TRUTH.yaml").read_text(encoding="utf-8"))


def _ingest() -> object:
    """Run the deterministic ingest against the labeled fixture."""
    return ingest_security_hub(IngestSecurityHubInput(asff_path=FIXTURE_DIR / "findings.json"))


def test_aggregate_counts_match_ground_truth() -> None:
    gt = _load_ground_truth()["expected_ingest"]
    out = _ingest()
    assert out.findings_total == gt["findings_total"], (
        f"findings_total {out.findings_total} != expected {gt['findings_total']}"
    )
    assert out.findings_emitted == gt["evidence_emitted"], (
        f"evidence_emitted {out.findings_emitted} != expected {gt['evidence_emitted']}"
    )
    assert out.skipped_status_not_available == gt["skipped_status_not_available"], (
        f"skipped NOT_AVAILABLE {out.skipped_status_not_available} != "
        f"expected {gt['skipped_status_not_available']}"
    )


def test_skipped_unmapped_generator_ids_match_ground_truth() -> None:
    gt = _load_ground_truth()["expected_ingest"]
    out = _ingest()
    actual_skipped = sorted(out.skipped_unmapped_generator_ids)
    expected_skipped = sorted(gt["skipped_unmapped_generator_ids"])
    assert actual_skipped == expected_skipped, (
        f"skipped-unmapped mismatch.\nactual:   {actual_skipped}\nexpected: {expected_skipped}"
    )


def test_per_generator_id_mappings_match_ground_truth() -> None:
    """Per (generator-id) — count + KSI list + control list match the ground truth."""
    gt = _load_ground_truth()["expected_mappings"]
    out = _ingest()

    # Bucket Evidence by the generator-id that produced it.
    by_generator: dict[str, list] = {}
    for ev in out.evidence:
        gid = ev.content.get("asff_generator_id", "")
        by_generator.setdefault(gid, []).append(ev)

    for gid, expected in gt.items():
        evs = by_generator.get(gid, [])
        assert len(evs) == expected["findings_count"], (
            f"{gid}: emitted {len(evs)} Evidence records, expected {expected['findings_count']}"
        )
        for ev in evs:
            assert sorted(ev.ksis_evidenced) == sorted(expected["ksis"]), (
                f"{gid}: ksis_evidenced {ev.ksis_evidenced} != {expected['ksis']}"
            )
            assert sorted(ev.controls_evidenced) == sorted(expected["controls"]), (
                f"{gid}: controls_evidenced {ev.controls_evidenced} != {expected['controls']}"
            )


def test_no_unexpected_generator_ids_emitted() -> None:
    """Every emitted Evidence record's generator-id appears in the ground truth."""
    gt = _load_ground_truth()["expected_mappings"]
    out = _ingest()
    expected_ids = set(gt.keys())
    actual_ids = {ev.content.get("asff_generator_id", "") for ev in out.evidence}
    extra = actual_ids - expected_ids
    assert not extra, f"emitted Evidence for unexpected generator-ids: {extra}"


def test_each_emitted_evidence_carries_required_content_fields() -> None:
    """Sanity check: ingest output preserves the canonical content fields."""
    out = _ingest()
    required_keys = {
        "import_source",
        "asff_finding_id",
        "asff_generator_id",
        "asff_compliance_status",
        "asff_title",
        "asff_description",
        "asff_resources",
        "evidence_strength",
        "mapping_title",
    }
    for ev in out.evidence:
        missing = required_keys - set(ev.content.keys())
        assert not missing, f"Evidence {ev.evidence_id} missing content keys: {missing}"
        assert ev.content["import_source"] == "aws.security_hub.asff"


def test_compliance_status_distribution_matches_input() -> None:
    """Sanity check: emitted Evidence preserves both PASSED + FAILED finds."""
    out = _ingest()
    statuses = {ev.content["asff_compliance_status"] for ev in out.evidence}
    # We have a mix of PASSED + FAILED across the 14 emitted; both should be present.
    assert "PASSED" in statuses
    assert "FAILED" in statuses
