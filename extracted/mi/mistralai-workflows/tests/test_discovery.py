from unittest.mock import patch

from structlog.testing import capture_logs

from mistralai.workflows.core.discovery import discover_workflows_in_module


def test_module_import_failure_does_not_log_exception_message() -> None:
    secret = "SYNTHETIC_SECRET"
    exc = ModuleNotFoundError(secret, name="workflow_dependency")

    with (
        patch("mistralai.workflows.core.discovery.importlib.import_module", side_effect=exc),
        capture_logs() as logs,
    ):
        assert discover_workflows_in_module("customer_workflows") == []

    assert logs == [
        {
            "event": "Failed to import module",
            "module": "customer_workflows",
            "error_type": "ModuleNotFoundError",
            "missing_module": "workflow_dependency",
            "log_level": "warning",
        }
    ]
    assert secret not in str(logs)
