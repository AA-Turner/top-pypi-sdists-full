from unittest.mock import Mock

from agentic_devtools.cli.ci.windows_process_cleanup import ProcessCleanupDiagnostic, _attempt_process_cleanup


def test_attempt_process_cleanup_returns_results_and_collects_failures() -> None:
    errors: list[ProcessCleanupDiagnostic] = []
    result, cancellation, failed = _attempt_process_cleanup("drain", Mock(return_value="value"), (), errors, None)

    assert (result, cancellation, failed, errors) == ("value", None, False, [])

    _, cancellation, failed = _attempt_process_cleanup(
        "reap", Mock(side_effect=OSError("reap failed")), (), errors, None
    )
    assert cancellation is None
    assert failed
    assert errors == [ProcessCleanupDiagnostic("reap", "reap failed")]


def test_attempt_process_cleanup_preserves_primary_cancellation() -> None:
    errors: list[ProcessCleanupDiagnostic] = []
    cancellation = KeyboardInterrupt("caller cancelled")

    _, returned_cancellation, failed = _attempt_process_cleanup(
        "reap", Mock(side_effect=cancellation), (), errors, None
    )
    assert returned_cancellation is cancellation
    assert failed
    assert errors == []

    _, returned_cancellation, failed = _attempt_process_cleanup(
        "close", Mock(side_effect=SystemExit("secondary cancellation")), (), errors, cancellation
    )
    assert returned_cancellation is cancellation
    assert failed
    assert errors == [ProcessCleanupDiagnostic("close", "secondary cancellation")]
