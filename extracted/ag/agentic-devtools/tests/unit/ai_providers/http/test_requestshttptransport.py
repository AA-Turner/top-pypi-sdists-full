from unittest.mock import Mock, patch

import pytest
import requests

from agentic_devtools.ai_providers import DeliveryState, RequestsHttpTransport, TransportError


def test_transport_returns_json_response_without_retry() -> None:
    response = Mock(status_code=202)
    response.json.return_value = {"id": "task-1"}
    session = Mock()
    session.request.return_value = response

    with patch("agentic_devtools.ai_providers.http.requests.Session", return_value=session):
        result = RequestsHttpTransport().request(
            "POST",
            "https://example.test/tasks",
            headers={"X-GitHub-Api-Version": "2026-03-10"},
            json_body={"prompt": "p"},
            timeout=2.0,
        )

    assert result.status_code == 202
    assert result.body == {"id": "task-1"}
    assert result.delivery_state is DeliveryState.DELIVERED
    session.request.assert_called_once()
    assert session.trust_env is False
    assert session.request.call_args.kwargs["allow_redirects"] is False
    assert session.request.call_args.kwargs["headers"] == {"X-GitHub-Api-Version": "2026-03-10"}


def test_transport_preserves_non_json_body() -> None:
    response = Mock(status_code=500, text="not json")
    response.json.side_effect = ValueError("bad json")

    session = Mock()
    session.request.return_value = response
    with patch("agentic_devtools.ai_providers.http.requests.Session", return_value=session):
        result = RequestsHttpTransport().request(
            "GET",
            "https://example.test/tasks/1",
            headers={},
            json_body=None,
            timeout=2.0,
        )

    assert result.body == "not json"


def test_transport_wraps_request_exception_as_ambiguous() -> None:
    session = Mock()
    session.request.side_effect = requests.ConnectionError("secret")
    with patch("agentic_devtools.ai_providers.http.requests.Session", return_value=session):
        with pytest.raises(TransportError) as caught:
            RequestsHttpTransport().request(
                "GET",
                "https://example.test/tasks/1",
                headers={},
                json_body=None,
                timeout=2.0,
            )

    assert caught.value.delivery_state is DeliveryState.AMBIGUOUS
    assert caught.value.retryable is False
    assert "secret" not in str(caught.value)
    assert caught.value.__cause__ is None
    assert caught.value.__suppress_context__ is True


def test_transport_classifies_connect_timeout_as_not_delivered() -> None:
    session = Mock()
    session.request.side_effect = requests.ConnectTimeout()
    with patch("agentic_devtools.ai_providers.http.requests.Session", return_value=session):
        with pytest.raises(TransportError) as caught:
            RequestsHttpTransport().request(
                "POST",
                "https://example.test/tasks",
                headers={},
                json_body=None,
                timeout=2.0,
            )

    assert caught.value.delivery_state is DeliveryState.NOT_DELIVERED
    assert caught.value.retryable is True
