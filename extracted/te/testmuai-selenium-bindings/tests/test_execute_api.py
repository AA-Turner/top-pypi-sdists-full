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


def test_execute_api_proxy_error_fails_with_cause():
    import httpx

    # V2: proxy/connect failures FAIL the step with a message
    # naming the cause — the server was never reached, so there is no response
    # for a status assertion to judge. Other failures (e.g. ReadTimeout) stay soft.
    with patch("httpx.get", side_effect=httpx.ProxyError("tunnel down")):
        with pytest.raises(httpx.ProxyError, match="API request failed — proxy could not reach the server: tunnel down"):
            execute_api(method="GET", url="https://example.com/api")


def test_execute_api_connect_error_fails_with_cause():
    import httpx

    # V2: proxy/connect failures FAIL the step with a message
    # naming the cause — the server was never reached, so there is no response
    # for a status assertion to judge. Other failures (e.g. ReadTimeout) stay soft.
    with patch("httpx.get", side_effect=httpx.ConnectError("refused")):
        with pytest.raises(httpx.ConnectError, match="API request failed — could not connect to the server: refused"):
            execute_api(method="GET", url="https://example.com/api")


# ---------------------------------------------------------------------------
# V2 — multipart bodies
# ---------------------------------------------------------------------------

def _wire(method):
    """Spy that builds the request exactly as httpx would and records it."""
    import httpx
    seen = {}

    def spy(url, **kw):
        req = httpx.Request(method, url, headers=kw.get("headers"),
                            data=kw.get("data"), files=kw.get("files"))
        seen["content_type"] = req.headers.get("content-type", "")
        seen["body"] = req.read()
        return httpx.Response(200, json={"ok": True}, request=req)
    return spy, seen


def test_multipart_dict_body_is_sent_as_real_multipart():
    # Stripping the header alone left httpx form-URL-encoding the dict.
    spy, seen = _wire("POST")
    with patch("httpx.post", spy):
        execute_api(method="POST", url="https://example.com/api",
                    headers={"Content-Type": "multipart/form-data; boundary=authored"},
                    body='{"name": "parth"}')
    assert seen["content_type"].startswith("multipart/form-data; boundary=")
    # The authored boundary cannot match the client-built body, so it is dropped.
    assert "boundary=authored" not in seen["content_type"]
    assert b'name="name"\r\n\r\nparth' in seen["body"]


def test_multipart_coerces_non_string_values():
    # httpx calls .read() on anything that is not str/bytes.
    spy, seen = _wire("POST")
    with patch("httpx.post", spy):
        execute_api(method="POST", url="https://example.com/api",
                    headers={"Content-Type": "multipart/form-data"},
                    body={"age": 30, "meta": {"a": 1}})
    assert b'name="age"\r\n\r\n30' in seen["body"]
    assert b'{"a": 1}' in seen["body"]


def test_urlencoded_body_is_unchanged():
    spy, seen = _wire("POST")
    with patch("httpx.post", spy):
        execute_api(method="POST", url="https://example.com/api",
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    body={"q": "1"})
    assert seen["content_type"] == "application/x-www-form-urlencoded"


# ---------------------------------------------------------------------------
# An empty params dict must never reach httpx
#
# httpx >= 0.28 treats params={} as "replace the query string", so a URL that
# already carries ?key=value loses it. The reported symptom was an API returning
# 401 instead of 302 because its auth query parameter had been stripped.
# pyproject allows httpx>=0.27.0, so both behaviours are in range — the binding
# normalises the empty case to None rather than pinning the dependency.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("params", [None, {}, "", "{}", "not-json"])
def test_empty_params_are_passed_as_none_not_empty_dict(params):
    fake_resp = _mock_response(status=200, json_body={"ok": True})
    with patch("httpx.get", return_value=fake_resp) as mock_get:
        execute_api(method="GET", url="https://example.com/api?key=value", params=params)
    assert mock_get.call_args.kwargs["params"] is None, (
        "an empty params must reach httpx as None; {} strips the URL's query string"
    )


def test_real_params_are_still_forwarded():
    fake_resp = _mock_response(status=200, json_body={"ok": True})
    with patch("httpx.get", return_value=fake_resp) as mock_get:
        execute_api(method="GET", url="https://example.com/api", params={"a": "1"})
    assert mock_get.call_args.kwargs["params"] == {"a": "1"}


def test_url_query_string_survives_an_empty_params():
    """End-to-end on the real httpx URL builder — this is the actual bug."""
    import httpx

    url = "https://example.com/api?key=value"
    assert str(httpx.Request("GET", url, params={}).url) == "https://example.com/api", (
        "guard: this test is meaningless if httpx stops stripping on {}"
    )
    assert str(httpx.Request("GET", url, params=None).url) == url
# x-www-form-urlencoded bodies
#
# Two defects, one root cause. The re-encode ran BEFORE template resolution, so
# it percent-encoded the template's own braces ("phone={{phone}}" ->
# "phone=%7B%7Bphone%7D%7D") and the resolver could never match them. And the
# round-trip was plus-decoding, so a resolved E.164 number ("+9198…") had its
# "+" read as a space.
# ---------------------------------------------------------------------------

_FORM_CT = {"Content-Type": "application/x-www-form-urlencoded"}


def _sent_body(body):
    fake_resp = _mock_response(status=200, json_body={"ok": True})
    with patch("httpx.post", return_value=fake_resp) as mock_post:
        execute_api(method="POST", url="https://example.com/api",
                    headers=dict(_FORM_CT), body=body)
    return mock_post.call_args.kwargs.get("data")


def test_template_in_urlencoded_body_is_resolved():
    set_var("phone", "+919876543210")
    assert _sent_body("phone={{phone}}") == "phone=%2B919876543210"


def test_resolved_literal_plus_is_percent_encoded_not_turned_into_a_space():
    """The reported bug: an E.164 prefix arriving at the API as ' 9198…'."""
    set_var("phone", "+919876543210")
    sent = _sent_body("phone={{phone}}")
    assert "%2B" in sent
    assert "phone=+" not in sent, "a bare '+' decodes to a space server-side"


def test_pre_encoded_plus_survives_unchanged():
    assert _sent_body("phone=%2B919876543210") == "phone=%2B919876543210"


def test_multiple_pairs_and_spaces():
    set_var("phone", "+91")
    assert _sent_body("a=1&phone={{phone}}&c=hi there") == "a=1&phone=%2B91&c=hi%20there"


def test_key_without_value_is_preserved():
    assert _sent_body("flag&a=1") == "flag&a=1"


def test_malformed_body_is_returned_unchanged_rather_than_raising():
    from testmu_selenium._helpers.execute_api import _reencode_urlencoded_body
    with patch("testmu_selenium._helpers.execute_api.unquote",
               side_effect=ValueError("boom")):
        assert _reencode_urlencoded_body("a=1") == "a=1"


def test_non_form_content_type_body_is_untouched():
    fake_resp = _mock_response(status=200, json_body={"ok": True})
    with patch("httpx.post", return_value=fake_resp) as mock_post:
        execute_api(method="POST", url="https://example.com/api",
                    headers={"Content-Type": "text/plain"}, body="a+b c")
    assert mock_post.call_args.kwargs.get("data") == "a+b c"


# --- V2: opt-in nested-JSON unwrap --------------------------


def test_json_splitter_unwraps_nested_json_only_when_enabled():
    import httpx
    import json as _json
    payload = {"data": _json.dumps({"id": 7, "tags": _json.dumps(["a"])}), "plain": "{not json", "n": "7"}

    def fake_get(url, **kw):
        return httpx.Response(200, json=payload, request=httpx.Request("GET", url))

    with patch("httpx.get", fake_get):
        off = execute_api(method="GET", url="https://example.com/api")
        on = execute_api(method="GET", url="https://example.com/api",
                         settings={"enable_json_splitter": True})
    assert isinstance(off["response_body"]["data"], str)          # V2 default: opt-in
    assert on["response_body"]["data"] == {"id": 7, "tags": ["a"]}  # recursive
    assert on["response_body"]["plain"] == "{not json"            # malformed kept
    assert on["response_body"]["n"] == "7"                        # only {/[ strings


def test_json_splitter_also_applies_under_normalization():
    # auteur applies both: normalized envelope AND the opt-in unwrap (Java/C#/TS parity).
    import httpx
    import json as _json
    payload = {"data": _json.dumps({"id": 7}), "n": "7"}

    def fake_get(url, **kw):
        return httpx.Response(200, json=payload, request=httpx.Request("GET", url))

    with patch("httpx.get", fake_get):
        on = execute_api(method="GET", url="https://example.com/api",
                         settings={"normalization": True, "enable_json_splitter": True})
        off = execute_api(method="GET", url="https://example.com/api",
                          settings={"normalization": True})
    assert isinstance(on["headers"], dict)                       # still the normalized envelope
    assert on["response_body"]["data"] == {"id": 7}
    assert on["body"]["data"] == {"id": 7}
    assert on["response_body"]["n"] == "7"
    assert isinstance(off["response_body"]["data"], str)         # splitter stays opt-in
