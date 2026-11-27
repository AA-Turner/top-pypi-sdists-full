from unittest.mock import patch

from mistralai.workflows.core.tracing.utils import _record_event


def test_record_event_does_not_log_custom_attributes() -> None:
    with patch("mistralai.workflows.core.tracing.utils.logger") as logger:
        _record_event("custom", {"value": "SYNTHETIC_SECRET"})

    logger.debug.assert_called_once_with("Recording event", event_name="custom")
    assert "SYNTHETIC_SECRET" not in str(logger.debug.call_args)
