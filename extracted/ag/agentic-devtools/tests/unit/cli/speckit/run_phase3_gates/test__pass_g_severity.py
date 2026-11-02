"""Tests for normalized Pass G finding severities."""

import pytest

from agentic_devtools.cli.speckit.run_phase3_gates import _pass_g_severity


@pytest.mark.parametrize(
    ("finding", "expected"),
    [
        ({"status": "invalid", "candidates": []}, "HIGH"),
        ({"status": "invalid", "candidates": [{}]}, "MEDIUM"),
        ({"status": "ambiguous", "candidates": []}, "MEDIUM"),
        ({"status": "partial", "candidates": []}, "LOW"),
        ({"status": "skipped", "candidates": []}, "LOW"),
        ({"status": "matched", "candidates": []}, "LOW"),
        ({"status": "new_symbol", "candidates": []}, "LOW"),
    ],
)
def test_maps_supported_finding_status_to_report_severity(finding: dict, expected: str) -> None:
    assert _pass_g_severity(finding) == expected


def test_rejects_unknown_status() -> None:
    with pytest.raises(ValueError, match="unsupported Pass G status"):
        _pass_g_severity({"status": "unknown", "candidates": []})


def test_rejects_invalid_candidates_shape() -> None:
    with pytest.raises(ValueError, match="candidates"):
        _pass_g_severity({"status": "invalid", "candidates": None})


def test_rejects_non_object_candidate() -> None:
    with pytest.raises(ValueError, match="candidates"):
        _pass_g_severity({"status": "invalid", "candidates": ["candidate"]})
