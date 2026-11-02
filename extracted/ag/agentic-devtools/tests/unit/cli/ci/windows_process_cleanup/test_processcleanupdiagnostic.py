import pytest

from agentic_devtools.cli.ci.windows_process_cleanup import ProcessCleanupDiagnostic


def test_process_cleanup_diagnostic_is_immutable() -> None:
    diagnostic = ProcessCleanupDiagnostic("close", "injected close failure")

    assert diagnostic.stage == "close"
    assert diagnostic.message == "injected close failure"
    with pytest.raises(AttributeError):
        setattr(diagnostic, "stage", "drain")
