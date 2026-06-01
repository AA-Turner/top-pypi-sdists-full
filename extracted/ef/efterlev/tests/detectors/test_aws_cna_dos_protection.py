"""Fixture-driven tests for `aws.cna_dos_protection`."""

from __future__ import annotations

from pathlib import Path

from efterlev.detectors.aws.cna_dos_protection.detector import detect
from efterlev.terraform import parse_terraform_file

DETECTOR_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "efterlev"
    / "detectors"
    / "aws"
    / "cna_dos_protection"
)


def _run(path: Path) -> list:
    return detect(parse_terraform_file(path))


def test_wafv2_with_rate_based_emits_evidence_with_count() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "wafv2_with_rate_based.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.detector_id == "aws.cna_dos_protection"
    assert ev.ksis_evidenced == ["KSI-CNA-RVP"]
    assert set(ev.controls_evidenced) == {"SC-5", "SI-8"}
    assert ev.content["resource_type"] == "aws_wafv2_web_acl"
    assert ev.content["resource_name"] == "edge"
    assert ev.content["protection_state"] == "configured"
    assert ev.content["pattern"] == "waf_acl"
    assert "rate_based_rules=1" in ev.content["detail"]


def test_wafv2_attached_to_alb_emits_attached_pattern() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "wafv2_attached_to_alb.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_type"] == "aws_wafv2_web_acl_association"
    assert ev.content["pattern"] == "waf_attached"
    assert "loadbalancer/app/edge-alb" in ev.content["detail"]


def test_waf_classic_emits_classic_pattern() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "waf_classic.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_type"] == "aws_waf_web_acl"
    assert ev.content["pattern"] == "waf_classic_acl"
    assert ev.content["protection_state"] == "configured"


def test_shield_protection_emits_shield_pattern() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "shield_protection.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_type"] == "aws_shield_protection"
    assert ev.content["pattern"] == "shield_protection"
    assert "loadbalancer/app/edge-alb" in ev.content["detail"]


def test_no_protection_resources_emits_no_evidence() -> None:
    """Workspace with no WAF/Shield resources → no evidence emitted.
    The detector does NOT emit negative evidence for absent protection
    (many workspaces serve no public traffic; the absence isn't a gap
    per se)."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "no_protection_resources.tf")
    assert results == []


# --- contract pins ------------------------------------------------------------


def test_detector_declares_expected_mappings() -> None:
    from efterlev.detectors.base import _REGISTRY

    spec = _REGISTRY.get("aws.cna_dos_protection")
    assert spec is not None
    assert list(spec.ksis) == ["KSI-CNA-RVP"]
    assert set(spec.controls) == {"SC-5", "SI-8"}


def test_detector_emits_only_documented_patterns() -> None:
    """Lock the schema: pattern in {waf_acl, waf_attached,
    waf_classic_acl, shield_protection}."""
    fixtures = list((DETECTOR_DIR / "fixtures").rglob("*.tf"))
    seen = set()
    for f in fixtures:
        for ev in _run(f):
            seen.add(ev.content.get("pattern"))
    assert seen <= {"waf_acl", "waf_attached", "waf_classic_acl", "shield_protection"}, (
        f"detector emitted unexpected pattern values: {seen}"
    )


def test_detector_only_emits_configured_state() -> None:
    """v0.1.31 emits only positive (configured) evidence — no negative
    path. Lock that contract so a future expansion that adds negatives
    is a deliberate design decision in a separate PR."""
    fixtures = list((DETECTOR_DIR / "fixtures").rglob("*.tf"))
    seen = set()
    for f in fixtures:
        for ev in _run(f):
            seen.add(ev.content.get("protection_state"))
    assert seen <= {"configured"}, (
        f"detector emitted protection_state values other than 'configured': {seen}. "
        f"v0.1.31 contract: positive-only. Adding negatives needs a design entry."
    )
