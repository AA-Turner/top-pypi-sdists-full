from unittest.mock import Mock

from agentic_devtools.cli.ci.windows_process_cleanup import _attempt_cleanup


def test_records_failures_and_preserves_first_cancellation() -> None:
    errors: list[str] = []
    assert _attempt_cleanup(Mock(), (), errors, None) is None

    assert _attempt_cleanup(Mock(side_effect=OSError("ordinary failure")), (), errors, None) is None
    assert errors == ["ordinary failure"]

    interruption = KeyboardInterrupt("caller cancellation")
    assert _attempt_cleanup(Mock(side_effect=interruption), (), errors, None) is interruption
    assert (
        _attempt_cleanup(
            Mock(side_effect=SystemExit("secondary cancellation")),
            (),
            errors,
            interruption,
        )
        is interruption
    )
    assert errors == ["ordinary failure", "secondary cancellation"]
