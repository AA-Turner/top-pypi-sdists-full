import subprocess
from unittest.mock import Mock

from agentic_devtools.cli.ci.windows_process_cleanup import ProcessCleanupDiagnostic, _drain_and_reap_process


def _as_text(value: str | bytes | None) -> str | None:
    return value.decode() if isinstance(value, bytes) else value


def _prefer_output(previous: str | None, latest: str | bytes | None) -> str | None:
    text = _as_text(latest)
    return text if text is not None and (previous is None or len(text) >= len(previous)) else previous


def test_drain_and_reap_skips_absent_process() -> None:
    errors: list[ProcessCleanupDiagnostic] = []
    drain, reap = Mock(), Mock()

    result = _drain_and_reap_process(None, 5, drain, reap, _as_text, _prefer_output, errors, None)

    assert result == (None, None, None, None)
    assert errors == []
    drain.assert_not_called()
    reap.assert_not_called()


def test_drain_and_reap_preserves_recovered_output_and_reap_cancellation() -> None:
    process = object()
    interruption = KeyboardInterrupt("reap interrupted")
    errors: list[ProcessCleanupDiagnostic] = []

    stdout, stderr, timeout, cancellation = _drain_and_reap_process(
        process,
        5,
        Mock(return_value=("recovered stdout", "recovered stderr")),
        Mock(side_effect=interruption),
        _as_text,
        _prefer_output,
        errors,
        None,
    )

    assert (stdout, stderr, timeout, cancellation) == (
        "recovered stdout",
        "recovered stderr",
        None,
        interruption,
    )
    assert errors == [ProcessCleanupDiagnostic("reap", "reap interrupted")]


def test_drain_and_reap_preserves_timeout_output_and_returncode() -> None:
    process = object()
    timeout = subprocess.TimeoutExpired(["tool"], 5, output=b"partial stdout", stderr=b"partial stderr")
    errors: list[ProcessCleanupDiagnostic] = []

    stdout, stderr, drain_timeout, cancellation = _drain_and_reap_process(
        process,
        5,
        Mock(side_effect=timeout),
        Mock(),
        _as_text,
        _prefer_output,
        errors,
        None,
    )

    assert (stdout, stderr, drain_timeout, cancellation) == ("partial stdout", "partial stderr", timeout, None)
    assert errors == [ProcessCleanupDiagnostic("drain", str(timeout))]


def test_drain_and_reap_records_drain_cancellation_and_ordinary_failure() -> None:
    primary_cancellation = KeyboardInterrupt("primary cancellation")
    drain_cancellation = KeyboardInterrupt("drain interrupted")
    system_exit = SystemExit("drain exit")
    generator_exit = GeneratorExit("drain generator exit")
    for drain_error, initial_cancellation, expected_cancellation in (
        (OSError("drain failed"), None, None),
        (drain_cancellation, None, drain_cancellation),
        (system_exit, None, system_exit),
        (generator_exit, None, generator_exit),
        (SystemExit("secondary drain exit"), primary_cancellation, primary_cancellation),
    ):
        setattr(drain_error, "output", b"partial stdout")
        setattr(drain_error, "stderr", b"partial stderr")
        errors: list[ProcessCleanupDiagnostic] = []

        stdout, stderr, timeout, cancellation = _drain_and_reap_process(
            object(),
            5,
            Mock(side_effect=drain_error),
            Mock(),
            _as_text,
            _prefer_output,
            errors,
            initial_cancellation,
        )

        assert (stdout, stderr, timeout) == ("partial stdout", "partial stderr", None)
        assert cancellation is expected_cancellation
        assert errors[0] == ProcessCleanupDiagnostic("drain", str(drain_error))
