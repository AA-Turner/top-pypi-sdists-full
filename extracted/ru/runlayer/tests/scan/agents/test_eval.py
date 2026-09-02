"""Acceptance gate (FR8): 100% framework + language on the corpus, zero FP.

This is the CI regression that locks in detection quality. The committed corpus
under ``cli/tests/fixtures/agent_detection`` is the anonymized agent test set
(source + manifest per sample) plus non-agent samples for the false-positive
gate.
"""

from __future__ import annotations

from pathlib import Path

from runlayer_cli.scan.agents.detect import collect_agents

from .harness import evaluate_detections, format_evaluation

FIXTURES = Path(__file__).resolve().parents[2] / "fixtures" / "agent_detection"
SAMPLES = FIXTURES / "samples"
LABELS = FIXTURES / "labels.json"
NON_AGENT = FIXTURES / "non_agent"


def test_fixtures_present():
    assert SAMPLES.is_dir()
    assert LABELS.is_file()
    assert NON_AGENT.is_dir()


def test_one_hundred_percent_framework_and_language():
    detections = collect_agents([SAMPLES], include_unknown=True)
    result = evaluate_detections(detections, LABELS)

    assert result["framework"]["accuracy"] == 1.0, format_evaluation(result)
    assert result["language"]["accuracy"] == 1.0, format_evaluation(result)
    assert result["mismatches"] == [], format_evaluation(result)
    assert result["missing"] == [], format_evaluation(result)


def test_zero_false_positives_on_non_agent_sample():
    detections = collect_agents([NON_AGENT], include_unknown=True)
    false_positives = [d for d in detections if d.is_agent]
    assert false_positives == [], (
        "non-agent code was misclassified as an agent: "
        + ", ".join(f"{d.name}->{d.framework_id}" for d in false_positives)
    )
    # The non-agent projects were still discovered as (unknown) units.
    assert len(detections) >= 3


def test_every_detected_agent_has_a_discriminating_dependency():
    """Each corpus detection rests on a real package dependency, not just a symbol."""
    detections = collect_agents([SAMPLES])
    assert len(detections) == 18
    for d in detections:
        kinds = {e.kind for e in d.evidence}
        assert "package_dep" in kinds, (
            f"{d.name} ({d.framework_id}) lacks a package_dep"
        )
