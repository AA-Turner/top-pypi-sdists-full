"""Fixture-driven tests for `github.piy_sdlc_security_gates`."""

from __future__ import annotations

from pathlib import Path

from efterlev.detectors.github.piy_sdlc_security_gates.detector import detect
from efterlev.github_workflows import parse_workflow_file

DETECTOR_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "efterlev"
    / "detectors"
    / "github"
    / "piy_sdlc_security_gates"
)


def _run(path: Path) -> list:
    return detect([parse_workflow_file(path)])


# --- should_match -------------------------------------------------------------


def test_codeql_workflow_emits_configured_with_codeql_gate() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "codeql.yml")
    assert len(results) == 1
    ev = results[0]
    assert ev.detector_id == "github.piy_sdlc_security_gates"
    assert ev.ksis_evidenced == ["KSI-PIY-RSD"]
    assert set(ev.controls_evidenced) == {"SA-3", "SA-8"}
    assert ev.content["resource_type"] == "github_workflow"
    assert ev.content["resource_name"] == "CodeQL"
    assert ev.content["gate_state"] == "configured"
    assert ev.content["gates_present"] == ["codeql"]


def test_dependency_review_workflow_emits_configured() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "dependency_review.yml")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["gate_state"] == "configured"
    assert ev.content["gates_present"] == ["dependency_review"]


def test_secret_scan_workflow_emits_configured_with_secret_scanning() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "secret_scan.yml")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["gate_state"] == "configured"
    assert ev.content["gates_present"] == ["secret_scanning"]


def test_all_three_gates_in_one_workflow_emits_all_present() -> None:
    """A combined workflow with all three gates should list all three
    in `gates_present` (sorted alphabetically)."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "all_three_gates.yml")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["gate_state"] == "configured"
    assert ev.content["gates_present"] == [
        "codeql",
        "dependency_review",
        "secret_scanning",
    ]


# --- should_not_match ---------------------------------------------------------


def test_ci_only_workflow_emits_absent() -> None:
    """A pytest-only CI workflow has no security gates → absent."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "ci_only.yml")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["gate_state"] == "absent"
    assert "no SDLC security gate detected" in ev.content["gap"]
    assert "gates_present" not in ev.content


def test_deploy_only_workflow_emits_absent() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "deploy_only.yml")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["gate_state"] == "absent"


# --- contract pins ------------------------------------------------------------


def test_detector_declares_expected_mappings() -> None:
    from efterlev.detectors.base import _REGISTRY

    spec = _REGISTRY.get("github.piy_sdlc_security_gates")
    assert spec is not None
    assert list(spec.ksis) == ["KSI-PIY-RSD"]
    assert set(spec.controls) == {"SA-3", "SA-8"}
    assert spec.source == "github-workflows"


def test_detector_emits_only_documented_states() -> None:
    """Lock the schema: gate_state in {configured, absent}."""
    fixtures = list((DETECTOR_DIR / "fixtures").rglob("*.yml"))
    seen = set()
    for f in fixtures:
        for ev in _run(f):
            seen.add(ev.content.get("gate_state"))
    assert seen <= {"configured", "absent"}, (
        f"detector emitted unexpected gate_state values: {seen}"
    )


def test_detector_only_uses_documented_gate_labels() -> None:
    """Lock the gates_present enum: only {codeql, dependency_review,
    secret_scanning}. A future detector expansion that adds a new gate
    must update this allowlist deliberately."""
    fixtures = list((DETECTOR_DIR / "fixtures").rglob("*.yml"))
    seen = set()
    for f in fixtures:
        for ev in _run(f):
            for gate in ev.content.get("gates_present", []):
                seen.add(gate)
    assert seen <= {"codeql", "dependency_review", "secret_scanning"}, (
        f"detector emitted unexpected gate labels: {seen}"
    )
