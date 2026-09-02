import pytest

import datetime
import json
import requests

from eumdac.request import get, post, patch, put, delete


class MockResponse:
    def __init__(self, status_code, text=None):
        self.status_code = status_code
        self.text = text


def test_request_calls(monkeypatch):
    def mock_session_call(*args, **kwargs):
        return MockResponse(200)

    monkeypatch.setattr(requests.Session, "get", mock_session_call)
    monkeypatch.setattr(requests.Session, "post", mock_session_call)
    monkeypatch.setattr(requests.Session, "patch", mock_session_call)
    monkeypatch.setattr(requests.Session, "put", mock_session_call)
    monkeypatch.setattr(requests.Session, "delete", mock_session_call)

    assert get("https://test.test").status_code == 200
    assert post("https://test.test").status_code == 200
    assert patch("https://test.test").status_code == 200
    assert put("https://test.test").status_code == 200
    assert delete("https://test.test").status_code == 200


@pytest.mark.parametrize("message", [0, 1, 2])
def test_request_should_retry(message):
    jsons = [
        {
            "message": {
                "retryAfter": (datetime.timedelta(seconds=5) + datetime.datetime.now()).timestamp()
                * 1000,
                "reason": "test",
            }
        },
        {
            "message": {
                "reason": "Maximum number of connections exceeded",
            }
        },
        {
            "message": {
                "reason": "Maximum number of requests exceeded",
            }
        },
    ]
    from eumdac.request import _should_retry

    r = MockResponse(429, json.dumps(jsons[message]))
    assert _should_retry(r, 1)


@pytest.mark.parametrize("status_code", [200, 400, 500])
def test_request_should_not_retry(status_code):
    from eumdac.request import _should_retry

    r = MockResponse(status_code)
    assert not _should_retry(r)
