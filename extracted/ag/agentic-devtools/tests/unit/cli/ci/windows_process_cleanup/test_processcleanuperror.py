import subprocess

from agentic_devtools.cli.ci.windows_process_cleanup import ProcessCleanupDiagnostic, ProcessCleanupError


def test_process_cleanup_error_preserves_completed_result_and_diagnostics() -> None:
    completed = subprocess.CompletedProcess(["tool"], 0, "output", "diagnostic")
    diagnostic = ProcessCleanupDiagnostic("close", "injected close failure")
    error = ProcessCleanupError(completed, (diagnostic,))

    assert error.completed_process is completed
    assert error.cleanup_errors == (diagnostic,)
    assert "close: injected close failure" in str(error)
