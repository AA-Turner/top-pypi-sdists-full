"""Tests for testmu_selenium._helpers.execute_api — sync HTTP request helper."""
from unittest.mock import MagicMock, patch

import pytest

from testmu_selenium._helpers.execute_api import execute_api
from testmu_selenium._vars import set_var, _variable_store


@pytest.fixture(autouse=True)
def _reset_vars():
    _variable_store.clear()
    yield
    _variable_store.clear()


def _mock_response(status=200, json_body=None, headers=None):
    resp = MagicMock()
    resp.status_code = status
    resp.headers = headers or {}
    resp.cookies = {}
    import json as _json
    body_bytes = _json.dumps(json_body or {}).encode("utf-8")
    resp.content = body_bytes
    return resp


def test_execute_api_get_returns_response_dict():
    fake_resp = _mock_response(status=200, json_body={"ok": True})
    with patch("httpx.get", return_value=fake_resp) as mock_get:
        result = execute_api(method="GET", url="https://example.com/api")
    assert result["status"] == 200
    assert mock_get.called


def test_execute_api_logs_response_body(caplog):
    """The API response body must be surfaced in the step log so it shows up
    on the LambdaTest automation dashboard (parity with execute_db/js)."""
    import logging

    fake_resp = _mock_response(status=200, json_body={"token": "abc123"})
    with patch("httpx.get", return_value=fake_resp):
        # execute_api logs under the package-root "testmu_selenium" logger.
        with caplog.at_level(logging.INFO, logger="testmu_selenium"):
            execute_api(method="GET", url="https://example.com/api")

    result_lines = [r.getMessage() for r in caplog.records if "[execute_api] result=" in r.getMessage()]
    assert result_lines, "expected an '[execute_api] result=' log line"
    assert "abc123" in result_lines[0]


def test_execute_api_resolves_url_template():
    set_var("base", "https://example.com")
    fake_resp = _mock_response(status=200, json_body={"ok": True})
    with patch("httpx.get", return_value=fake_resp) as mock_get:
        execute_api(method="GET", url="{{base}}/api")
    # First positional or url kwarg should hold the resolved URL
    call_args = mock_get.call_args
    actual_url = call_args.args[0] if call_args.args else call_args.kwargs.get("url")
    assert actual_url == "https://example.com/api"


# ---------------------------------------------------------------------------
# Recursive template resolution in nested dict body, headers, params (RED → GREEN)
# ---------------------------------------------------------------------------

def test_execute_api_resolves_nested_dict_body_template():
    """When the body arrives as a native dict (not a JSON string), nested
    {{x}} templates must still be resolved before the request is sent.

    This is the real gap: _resolve_templates returns non-strings unchanged,
    so native dict bodies with embedded templates are sent unresolved without
    a recursive deep-resolver applied after the json-parse block.
    """
    import json as _json
    set_var("x", "abc")

    fake_resp = _mock_response(status=200, json_body={"ok": True})
    captured = {}

    def _fake_post(url, headers=None, data=None, params=None, **kwargs):
        captured["data"] = data
        return fake_resp

    # Pass body as a native dict (not a JSON string) — the gap case.
    native_body = {"outer": {"inner": "{{x}}"}}
    with patch("httpx.post", side_effect=_fake_post):
        execute_api(
            method="POST",
            url="https://example.com/api",
            headers={"Content-Type": "application/json"},
            body=native_body,
        )

    assert "data" in captured, "httpx.post was not called"
    sent = _json.loads(captured["data"])
    assert sent["outer"]["inner"] == "abc", (
        f"Expected 'abc' in nested dict body, got: {sent!r}"
    )


def test_execute_api_resolves_native_list_body_template():
    """When the body arrives as a native list with nested {{x}} templates in
    dict entries, those templates must be resolved before the request is sent.
    """
    set_var("x", "abc")

    fake_resp = _mock_response(status=200, json_body={"ok": True})
    captured = {}

    def _fake_post(url, headers=None, data=None, params=None, **kwargs):
        captured["data"] = data
        return fake_resp

    # Pass body as a native list — the gap case.
    native_body = [{"val": "{{x}}"}, {"val": "plain"}]
    with patch("httpx.post", side_effect=_fake_post):
        execute_api(
            method="POST",
            url="https://example.com/api",
            body=native_body,
        )

    assert "data" in captured, "httpx.post was not called"
    # data_kwarg is the list itself (execute_api only json.dumps dict bodies)
    assert isinstance(captured["data"], list), (
        f"Expected list data, got: {type(captured['data'])}"
    )
    assert captured["data"][0]["val"] == "abc", (
        f"Expected 'abc' at [0].val, got: {captured['data']!r}"
    )
    assert captured["data"][1]["val"] == "plain"


def test_execute_api_resolves_nested_header_template():
    """Header values nested inside dicts containing {{x}} templates must resolve.
    (Existing _resolve_dict_templates only handles one level — this confirms it
    handles a header value containing a template regardless of nesting depth.)
    """
    set_var("x", "abc")

    fake_resp = _mock_response(status=200, json_body={"ok": True})
    captured = {}

    def _fake_get(url, headers=None, params=None, **kwargs):
        captured["headers"] = dict(headers or {})
        return fake_resp

    with patch("httpx.get", side_effect=_fake_get):
        execute_api(
            method="GET",
            url="https://example.com/api",
            headers={"X-Custom": "{{x}}"},
        )

    assert captured["headers"]["X-Custom"] == "abc", (
        f"Expected 'abc' in header, got: {captured['headers']!r}"
    )


def test_execute_api_resolves_param_template():
    """Query param values containing {{x}} templates must resolve to the stored value."""
    set_var("x", "abc")

    fake_resp = _mock_response(status=200, json_body={"ok": True})
    captured = {}

    def _fake_get(url, headers=None, params=None, **kwargs):
        captured["params"] = params
        return fake_resp

    with patch("httpx.get", side_effect=_fake_get):
        execute_api(
            method="GET",
            url="https://example.com/api",
            params={"key": "{{x}}"},
        )

    assert captured["params"]["key"] == "abc", (
        f"Expected 'abc' in param, got: {captured['params']!r}"
    )


def test_execute_api_string_body_unchanged():
    """Plain string bodies (non-JSON) must NOT be modified — regression guard."""
    set_var("x", "abc")

    fake_resp = _mock_response(status=200, json_body={"ok": True})
    captured = {}

    def _fake_post(url, headers=None, data=None, params=None, **kwargs):
        captured["data"] = data
        return fake_resp

    plain_body = "raw body with no templates"
    with patch("httpx.post", side_effect=_fake_post):
        execute_api(
            method="POST",
            url="https://example.com/api",
            body=plain_body,
        )

    assert captured["data"] == plain_body, (
        f"Plain string body must pass through unchanged, got: {captured['data']!r}"
    )


# --- V2 parity: request errors fail open (soft 400 dict), not hard-fail --------
# Mirrors the V2 source execute_api: ANY request failure — timeout,
# proxy/connect stall through the HyperExecute proxy, or other network error —
# becomes {status:400, message:...} so the test continues and the author's own
# status assertion can handle it. Only input-validation errors hard-fail.


def test_execute_api_timeout_returns_soft_400_dict():
    import httpx

    with patch("httpx.get", side_effect=httpx.ReadTimeout("The read operation timed out")):
        result = execute_api(method="GET", url="https://example.com/api")
    assert result == {
        "status": 400,
        "message": "API request failed The read operation timed out",
    }


def test_execute_api_generic_exception_returns_soft_400_dict():
    with patch("httpx.get", side_effect=Exception("boom")):
        result = execute_api(method="GET", url="https://example.com/api")
    assert result == {"status": 400, "message": "API request failed boom"}


def test_execute_api_proxy_error_returns_soft_400_dict():
    import httpx

    with patch("httpx.get", side_effect=httpx.ProxyError("tunnel down")):
        result = execute_api(method="GET", url="https://example.com/api")
    assert result == {"status": 400, "message": "API request failed tunnel down"}


def test_execute_api_connect_error_returns_soft_400_dict():
    import httpx

    with patch("httpx.get", side_effect=httpx.ConnectError("refused")):
        result = execute_api(method="GET", url="https://example.com/api")
    assert result == {"status": 400, "message": "API request failed refused"}
