import pytest
import logging
from uuid import uuid4

from workflow_server.server import create_app


@pytest.fixture
def mock_sentry_capture_envelope(mocker):
    mock_transport = mocker.patch("sentry_sdk.client.make_transport")
    return mock_transport.return_value.capture_envelope


def test_sentry_integration_with_workflow_endpoints(monkeypatch, mock_sentry_capture_envelope):
    # GIVEN sentry is configured
    monkeypatch.setenv("SENTRY_DSN", "https://test-dsn@sentry.io/1234567890")

    # AND our /workflow/stream endpoint raises an exception
    def mock_get_version():
        raise Exception("Test exception")

    monkeypatch.setattr("workflow_server.api.workflow_view.get_version", mock_get_version)

    # AND we have a mock trace_id
    trace_id = str(uuid4())

    # AND we have a mock request body
    body = {
        "execution_id": uuid4(),
        "inputs": [],
        "environment_api_key": "test",
        "module": "workflow",
        "timeout": 360,
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow

class Workflow(BaseWorkflow):
    pass
""",
        },
        "execution_context": {
            "trace_id": trace_id,
            "parent_context": {
                "type": "API_REQUEST",
                "span_id": str(uuid4()),
                "parent": None,
            },
        },
    }

    # WHEN we call the /workflow/version endpoint
    flask_app = create_app()

    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/stream", json=body)

        # THEN we get a 500 error
        assert response.status_code == 500

        # AND sentry captures the error with the correct data
        assert mock_sentry_capture_envelope.call_count == 1
        envelope = mock_sentry_capture_envelope.call_args[0][0]
        event = envelope.get_event()
        assert event["level"] == "error"
        assert "Test exception" in event["exception"]["values"][0]["value"]

        # AND the trace_id is tagged
        assert event["tags"]["vellum_trace_id"] == trace_id

        # AND the default version tags are included
        assert "server_version" in event["tags"]
        assert "sdk_version" in event["tags"]


def test_sentry_integration_applies_custom_tags_from_logger_extra(monkeypatch, mock_sentry_capture_envelope):
    """Test that Sentry events include custom tags from logger exception extra data."""

    # GIVEN sentry is configured
    monkeypatch.setenv("SENTRY_DSN", "https://test-dsn@sentry.io/1234567890")

    # AND we have a function that will log with custom sentry_tags when called
    def mock_get_version():
        logger = logging.getLogger(__name__)
        try:
            raise Exception("Test exception with custom tags")
        except Exception:
            logger.exception(
                "Failed during workflow execution",
                extra={
                    "sentry_tags": {
                        "operation": "stream",
                        "test_tag": "test_value",
                        "numeric_tag": "12345",
                    }
                },
            )
            raise

    monkeypatch.setattr("workflow_server.api.workflow_view.get_version", mock_get_version)

    # AND we have a valid request body
    body = {
        "execution_id": str(uuid4()),
        "inputs": [],
        "environment_api_key": "test",
        "module": "workflow",
        "timeout": 360,
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow

class Workflow(BaseWorkflow):
    pass
""",
        },
        "execution_context": {
            "trace_id": str(uuid4()),
            "parent_context": {
                "type": "API_REQUEST",
                "span_id": str(uuid4()),
                "parent": None,
            },
        },
    }

    # WHEN we call an endpoint that triggers the error
    flask_app = create_app()

    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/stream", json=body)

        # THEN we get a 500 error
        assert response.status_code == 500

        # AND sentry captures the error
        assert mock_sentry_capture_envelope.call_count == 1
        envelope = mock_sentry_capture_envelope.call_args[0][0]
        event = envelope.get_event()

        # AND the custom tags are included in the event
        assert "tags" in event
        assert event["tags"]["operation"] == "stream"
        assert event["tags"]["test_tag"] == "test_value"
        assert event["tags"]["numeric_tag"] == "12345"
