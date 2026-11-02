"""Tests for _invalid_result."""

from agentic_devtools.cli.suggestion_confirm import _invalid_result


def test_returns_normalized_invalid_payload() -> None:
    result = _invalid_result(ValueError("invalid request"))

    assert result == {
        "success": False,
        "provider": "unknown",
        "status": "invalid",
        "reply_id": None,
        "diagnostics": ["invalid request"],
    }


def test_truncates_diagnostics_to_one_thousand_characters() -> None:
    result = _invalid_result(ValueError("x" * 1500))

    diagnostics = result["diagnostics"]
    assert isinstance(diagnostics, list)
    assert isinstance(diagnostics[0], str)
    assert len(diagnostics[0]) == 1000
