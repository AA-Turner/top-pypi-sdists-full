import sys
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci import windows_process_tree


@pytest.mark.skipif(sys.platform != "win32", reason="Exercises native Windows API failure paths")
def test_setup_failure_preserves_interrupted_cleanup_diagnostics(monkeypatch: pytest.MonkeyPatch) -> None:
    process = Mock()
    interruption = KeyboardInterrupt("cleanup interrupted")
    setattr(
        interruption,
        "cleanup_errors",
        (
            windows_process_tree.ProcessCleanupDiagnostic("terminate", "termination failed"),
            windows_process_tree.ProcessCleanupDiagnostic("drain", "drain failed"),
        ),
    )
    monkeypatch.setattr(windows_process_tree, "_create_job_object", Mock(return_value=17))
    monkeypatch.setattr(windows_process_tree.subprocess, "Popen", Mock(return_value=process))
    monkeypatch.setattr(
        windows_process_tree,
        "_assign_process_to_job",
        Mock(side_effect=OSError("assignment failed")),
    )
    cleanup = Mock(side_effect=interruption)
    monkeypatch.setattr(windows_process_tree, "_cleanup_process", cleanup)

    with pytest.raises(OSError, match="ownership setup failed") as raised:
        getattr(windows_process_tree, "_start_windows_process")(["tool"], cwd=None, env={})

    assert tuple((error.stage, error.message) for error in getattr(raised.value, "cleanup_errors", ())) == (
        ("terminate", "termination failed"),
        ("drain", "drain failed"),
    )
    cleanup.assert_called_once()
