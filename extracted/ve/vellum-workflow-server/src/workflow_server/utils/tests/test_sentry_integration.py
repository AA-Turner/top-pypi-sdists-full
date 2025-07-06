import pytest
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
