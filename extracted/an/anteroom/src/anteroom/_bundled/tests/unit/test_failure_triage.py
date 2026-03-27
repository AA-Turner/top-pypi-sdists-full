"""Tests for failure triage extraction."""

from __future__ import annotations

from anteroom.services.failure_triage import compute_failure_signature, extract_failure_triage


class TestExtractFailureTriage:
    def test_pytest_failed_line(self) -> None:
        summary = "FAILED tests/unit/test_foo.py::TestBar::test_baz - AssertionError: assert 1 == 2"
        result = extract_failure_triage(summary, [], {})
        assert result is not None
        assert result["first_failing_test"] == "tests/unit/test_foo.py::TestBar::test_baz"
        assert result["first_assertion"] == "AssertionError: assert 1 == 2"

    def test_traceback_extraction(self) -> None:
        summary = "src/anteroom/services/foo.py:45: in test_bar\n    assert x == y"
        result = extract_failure_triage(summary, [], {})
        assert result is not None
        assert result["first_traceback_file"] == "src/anteroom/services/foo.py"
        assert result["first_traceback_line"] == 45

    def test_assertion_line(self) -> None:
        summary = "E   AssertionError: expected 3 but got 5"
        result = extract_failure_triage(summary, [], {})
        assert result is not None
        assert result["first_assertion"] == "AssertionError: expected 3 but got 5"

    def test_ruff_error(self) -> None:
        summary = "src/anteroom/tools/safety.py:12:5: E501 Line too long (130 > 120)"
        result = extract_failure_triage(summary, [], {})
        assert result is not None
        assert result["first_failing_test"] == "src/anteroom/tools/safety.py:12:5"

    def test_exit_code_from_artifacts(self) -> None:
        result = extract_failure_triage("Exit code 1", [], {"exit_code": 1})
        assert result is not None
        assert result["exit_code"] == 1

    def test_none_when_no_signal(self) -> None:
        result = extract_failure_triage("", [], {})
        assert result is None

    def test_none_when_empty_text(self) -> None:
        result = extract_failure_triage("   ", [], {})
        assert result is None

    def test_findings_searched_when_summary_sparse(self) -> None:
        findings = [{"type": "stdout", "content": "FAILED tests/unit/test_x.py::test_y - assert False"}]
        result = extract_failure_triage("Exit code 1", findings, {"exit_code": 1})
        assert result is not None
        assert result["first_failing_test"] == "tests/unit/test_x.py::test_y"

    def test_failure_count(self) -> None:
        summary = "3 failed, 10 passed in 5.2s"
        result = extract_failure_triage(summary, [], {})
        assert result is not None
        assert result["failure_count"] == 3

    def test_ruff_failure_count(self) -> None:
        summary = "Found 5 errors."
        result = extract_failure_triage(summary, [], {})
        assert result is not None
        assert result["failure_count"] == 5

    def test_multiple_failed_lines_first_wins(self) -> None:
        summary = "FAILED tests/a.py::test_a - err1\nFAILED tests/b.py::test_b - err2"
        result = extract_failure_triage(summary, [], {})
        assert result is not None
        assert result["first_failing_test"] == "tests/a.py::test_a"

    def test_combined_extraction(self) -> None:
        summary = (
            "FAILED tests/unit/test_foo.py::test_bar - AssertionError\n"
            "src/anteroom/foo.py:10: in do_thing\n"
            "1 failed in 2.1s"
        )
        result = extract_failure_triage(summary, [], {"exit_code": 1})
        assert result is not None
        assert result["first_failing_test"] == "tests/unit/test_foo.py::test_bar"
        assert result["first_traceback_file"] == "src/anteroom/foo.py"
        assert result["first_traceback_line"] == 10
        assert result["exit_code"] == 1
        assert result["failure_count"] == 1
        assert "failure_signature" in result


class TestComputeFailureSignature:
    def test_stable_across_calls(self) -> None:
        triage = {"first_failing_test": "tests/a.py::test_x", "first_assertion": "assert False"}
        sig1 = compute_failure_signature(triage)
        sig2 = compute_failure_signature(triage)
        assert sig1 == sig2

    def test_changes_when_test_changes(self) -> None:
        t1 = {"first_failing_test": "tests/a.py::test_x"}
        t2 = {"first_failing_test": "tests/b.py::test_y"}
        assert compute_failure_signature(t1) != compute_failure_signature(t2)

    def test_fallback_to_exit_code(self) -> None:
        triage = {"exit_code": 1}
        sig = compute_failure_signature(triage)
        assert len(sig) == 16

    def test_length(self) -> None:
        triage = {"first_failing_test": "tests/a.py::test_x"}
        assert len(compute_failure_signature(triage)) == 16
