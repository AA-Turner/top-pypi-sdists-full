"""execute_api() — arbitrary HTTP request via request_with_retry."""
import json

import httpx
import pytest
import respx

from testmu_appium._helpers.execute_api import execute_api
from testmu_appium._vars import _variable_store, clear_state, set_var

_URL = "https://api.example.test/widgets"


@pytest.fixture(autouse=True)
def _clear_vars():
    clear_state()
    yield
    clear_state()


@respx.mock
def test_get_returns_status_headers_and_json_body():
    respx.get(_URL).mock(
        return_value=httpx.Response(200, json={"id": 1}, headers={"x-foo": "bar"})
    )
    result = execute_api(method="GET", url=_URL)
    assert result["status"] == 200
    assert result["response_body"] == {"id": 1}
    assert result["status_code"] == 200
    assert result["body"] == {"id": 1}
    assert result["headers"]["x-foo"] == "bar"


@respx.mock
def test_post_sends_json_body_and_headers():
    route = respx.post(_URL).mock(return_value=httpx.Response(201, json={"ok": True}))
    result = execute_api(
        method="POST", url=_URL,
        headers={"X-Custom": "abc"}, body={"name": "widget"},
    )
    assert result["status_code"] == 201
    sent = route.calls[0].request
    assert sent.headers["x-custom"] == "abc"
    assert json.loads(sent.content) == {"name": "widget"}


@respx.mock
def test_non_json_response_body_falls_back_to_text():
    respx.get(_URL).mock(return_value=httpx.Response(200, text="plain text body"))
    result = execute_api(method="GET", url=_URL)
    assert result["body"] == "plain text body"


@pytest.mark.parametrize("method", ["GET", "POST", "PUT", "PATCH", "DELETE"])
@respx.mock
def test_every_http_method_is_dispatched(method):
    route = respx.route(method=method, url=_URL).mock(return_value=httpx.Response(200, json={}))
    execute_api(method=method, url=_URL)
    assert route.called


@respx.mock
def test_url_resolves_variable_tokens():
    set_var("widget_id", "42")
    route = respx.get("https://api.example.test/widgets/42").mock(
        return_value=httpx.Response(200, json={})
    )
    execute_api(method="GET", url="https://api.example.test/widgets/{{widget_id}}")
    assert route.called


@respx.mock
def test_header_values_resolve_variable_tokens():
    set_var("token", "secret123")
    route = respx.get(_URL).mock(return_value=httpx.Response(200, json={}))
    execute_api(method="GET", url=_URL, headers={"Authorization": "Bearer {{token}}"})
    assert route.calls[0].request.headers["authorization"] == "Bearer secret123"


@respx.mock
def test_body_values_resolve_variable_tokens():
    set_var("name", "gizmo")
    route = respx.post(_URL).mock(return_value=httpx.Response(200, json={}))
    execute_api(method="POST", url=_URL, body={"name": "{{name}}"})
    assert json.loads(route.calls[0].request.content) == {"name": "gizmo"}


class TestNativeTypesSurviveResolution:
    """A resolved leaf keeps the stored value's type (selenium `_deep_resolve` parity).

    A leaf recorded as "{{n}}" with n=42 goes on the wire as the JSON number 42, and
    one recorded as "{{flag}}" with flag=True as the JSON literal `true`.
    """

    @pytest.mark.parametrize(
        "stored,expected",
        [
            (42, 42),
            (3.5, 3.5),
            (True, True),
            (False, False),
            (None, None),
            ("text", "text"),
            ({"nested": 1}, {"nested": 1}),
            ([1, 2], [1, 2]),
        ],
        ids=["int", "float", "true", "false", "null", "str", "dict", "list"],
    )
    @respx.mock
    def test_whole_string_template_body_leaf_keeps_its_type(self, stored, expected):
        set_var("v", stored)
        route = respx.post(_URL).mock(return_value=httpx.Response(200, json={}))
        execute_api(method="POST", url=_URL, body={"field": "{{v}}"})
        assert json.loads(route.calls[0].request.content) == {"field": expected}

    @respx.mock
    def test_nested_and_list_leaves_resolve_natively(self):
        set_var("qty", 7)
        set_var("flag", True)
        route = respx.post(_URL).mock(return_value=httpx.Response(200, json={}))
        execute_api(
            method="POST", url=_URL,
            body={"order": {"qty": "{{qty}}"}, "flags": ["{{flag}}", "plain"]},
        )
        assert json.loads(route.calls[0].request.content) == {
            "order": {"qty": 7}, "flags": [True, "plain"],
        }

    @respx.mock
    def test_embedded_templates_still_render_as_text(self):
        """Only a WHOLE-string template carries a native value; a token embedded in
        surrounding text is a string by construction."""
        set_var("qty", 7)
        route = respx.post(_URL).mock(return_value=httpx.Response(200, json={}))
        execute_api(method="POST", url=_URL, body={"note": "qty is {{qty}}"})
        assert json.loads(route.calls[0].request.content) == {"note": "qty is 7"}

    @respx.mock
    def test_non_string_leaves_pass_through_untouched(self):
        route = respx.post(_URL).mock(return_value=httpx.Response(200, json={}))
        execute_api(method="POST", url=_URL, body={"n": 1, "b": True, "z": None})
        assert json.loads(route.calls[0].request.content) == {"n": 1, "b": True, "z": None}

    @respx.mock
    def test_header_values_are_rendered_as_text(self):
        """HTTP header values are byte strings; httpx rejects anything else."""
        set_var("n", 42)
        route = respx.get(_URL).mock(return_value=httpx.Response(200, json={}))
        execute_api(method="GET", url=_URL, headers={"X-Count": "{{n}}"})
        assert route.calls[0].request.headers["x-count"] == "42"

    @respx.mock
    def test_param_values_resolve_natively(self):
        set_var("page", 3)
        route = respx.get(_URL).mock(return_value=httpx.Response(200, json={}))
        execute_api(method="GET", url=_URL, params={"page": "{{page}}"})
        assert route.calls[0].request.url.params["page"] == "3"


@respx.mock
def test_output_variable_is_written():
    respx.get(_URL).mock(return_value=httpx.Response(200, json={"id": 7}))
    result = execute_api(method="GET", url=_URL, output_variable="resp")
    assert _variable_store["resp"] == result
    assert _variable_store["resp"]["body"] == {"id": 7}


@respx.mock
def test_proxy_env_reaches_the_http_client(monkeypatch):
    """TESTMU_API_PROXY_* routes THIS helper's request; unset stays direct."""
    respx.get(_URL).mock(return_value=httpx.Response(200, json={}))
    seen = []
    original = httpx.Client.__init__

    def _record(self, *args, **kwargs):
        seen.append(kwargs.get("proxy"))
        kwargs.pop("proxy", None)  # respx's transport handles the request; the
        return original(self, *args, **kwargs)  # proxy target need not exist

    monkeypatch.setattr(httpx.Client, "__init__", _record)

    monkeypatch.setenv("TESTMU_API_PROXY_PORT", "20037")
    execute_api(method="GET", url=_URL)
    monkeypatch.delenv("TESTMU_API_PROXY_PORT")
    execute_api(method="GET", url=_URL)

    assert seen == ["http://127.0.0.1:20037", None]


# ── cloud run: the request goes through the grid hook, as V2's export does ──


class _HookDriver:
    """Records the lambda-hook call and answers in auteur's response shape."""

    session_id = "sess-123"

    def __init__(self, answer):
        self.answer = answer
        self.calls = []

    def execute_script(self, script, args):
        self.calls.append((script, args))
        return self.answer


_AUTEUR_ANSWER = {
    "status": 200,
    "headers": [{"content-type": "application/json"}, {"x-foo": "bar"}],
    "cookies": [],
    "response_body": {"ip": "1.2.3.4"},
    "time": 12.5,
}


@pytest.fixture
def cloud_session(monkeypatch):
    from testmu_appium import _config
    from testmu_appium._helpers.driver import _clear_drivers, _set_driver

    monkeypatch.delenv("TESTMU_API_PROXY_PORT", raising=False)
    monkeypatch.setattr(_config, "run_target", "cloud")

    def _attach(answer=_AUTEUR_ANSWER):
        driver = _HookDriver(answer)
        _set_driver("default", driver)
        return driver

    yield _attach
    _clear_drivers()


def test_cloud_run_issues_the_request_through_the_grid_hook(cloud_session, monkeypatch):
    """No proxy env + cloud target = the HYE box: the device's mitm is not
    reachable from here, so the call is handed to auteur beside the device
    (lambda-kane-ai / executeAPI), which issues it through the local proxy and
    the device network log records it."""
    driver = cloud_session()
    monkeypatch.setattr(
        httpx.Client, "__init__",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("direct request issued")),
    )
    set_var("tok", "abc")

    result = execute_api(
        method="get", url=_URL, headers={"Authorization": "Bearer {{tok}}", "X-N": 7},
        body={"q": "{{tok}}"}, params={"page": 2}, timeout=10, verify=False,
        output_variable="resp",
    )

    (script, args), = driver.calls
    assert script == "lambda-kane-ai"
    assert args["command"] == "executeAPI"
    assert args["testId"] == "sess-123"
    assert args["requestTimeout"] == 10
    payload = args["payload"]
    assert payload["method"] == "GET"
    assert payload["url"] == _URL
    assert payload["headers"] == {"Authorization": "Bearer abc", "X-N": "7"}
    assert payload["body"] == {"q": "abc"}
    assert payload["params"] == {"page": 2}
    assert payload["timeout"] == 10000  # auteur's helper divides by 1000
    assert payload["verify"] is False

    assert result["status"] == 200 and result["status_code"] == 200
    assert result["body"] == {"ip": "1.2.3.4"}
    assert result["response_body"] == {"ip": "1.2.3.4"}
    assert result["headers"] == {"content-type": "application/json", "x-foo": "bar"}
    assert _variable_store["resp"] == result


def test_auteur_refusal_is_returned_as_the_result(cloud_session):
    """auteur answers a bad URL / timeout as {"status": 4xx, "message": ...};
    V2 stores that answer as the api variable — so does this."""
    cloud_session({"status": 408, "message": "Request Timed out", "time": 10000})

    result = execute_api(method="GET", url=_URL)

    assert result["status"] == 408
    assert result["message"] == "Request Timed out"
    assert result["body"] is None


def test_a_grid_failure_propagates(cloud_session):
    """The hook's own failure is the driver's exception — no client-side
    fallback to a direct request, which would pass the step while silently
    losing the network-log entry."""
    driver = cloud_session()

    def _boom(script, args):
        raise RuntimeError("lambda hook: auteur unreachable")

    driver.execute_script = _boom
    with pytest.raises(RuntimeError, match="auteur unreachable"):
        execute_api(method="GET", url=_URL)


def test_a_non_dict_hook_answer_is_rejected(cloud_session):
    cloud_session(None)
    with pytest.raises(RuntimeError, match="invalid executeAPI response"):
        execute_api(method="GET", url=_URL)


def test_cloud_run_without_a_session_fails_loud(cloud_session):
    from testmu_appium._helpers.driver import _clear_drivers

    _clear_drivers()
    with pytest.raises(RuntimeError, match="needs the live session"):
        execute_api(method="GET", url=_URL)


@respx.mock
def test_proxy_env_wins_over_the_hook_on_a_cloud_target(cloud_session, monkeypatch):
    """auteur's in-process replay sets TESTMU_API_PROXY_PORT (the device's mitm
    on the same host) — that stays a direct request through the proxy even when
    the target reads cloud."""
    driver = cloud_session()
    respx.get(_URL).mock(return_value=httpx.Response(200, json={"ok": True}))
    original = httpx.Client.__init__
    seen = []

    def _record(self, *args, **kwargs):
        seen.append(kwargs.get("proxy"))
        kwargs.pop("proxy", None)
        return original(self, *args, **kwargs)

    monkeypatch.setattr(httpx.Client, "__init__", _record)
    monkeypatch.setenv("TESTMU_API_PROXY_PORT", "20037")

    result = execute_api(method="GET", url=_URL)

    assert driver.calls == []
    assert seen == ["http://127.0.0.1:20037"]
    assert result["body"] == {"ok": True}


@respx.mock
@pytest.mark.parametrize("timeout_ms", [15000, 250, 1500.5])
def test_explicit_millisecond_timeout_reaches_http_client_in_seconds(timeout_ms):
    route = respx.get(_URL).mock(return_value=httpx.Response(200, json={}))
    execute_api(method="GET", url=_URL, timeout_ms=timeout_ms)
    assert route.calls[0].request.extensions["timeout"]["read"] <= timeout_ms / 1000
    assert route.calls[0].request.extensions["timeout"]["read"] > timeout_ms / 2000


@respx.mock
def test_timeout_raises_execution_error_without_setting_output_variable():
    respx.get(_URL).mock(side_effect=httpx.ReadTimeout("delayed"))
    with pytest.raises(RuntimeError, match="execute_api failed: delayed") as error:
        execute_api(method="GET", url=_URL, timeout_ms=15000, output_variable="result")
    assert isinstance(error.value.__cause__, httpx.ReadTimeout)
    assert "result" not in _variable_store


def test_millisecond_and_second_timeouts_are_mutually_exclusive():
    with pytest.raises(ValueError, match="timeout"):
        execute_api(method="GET", url=_URL, timeout=15, timeout_ms=15000)


@respx.mock
def test_seconds_timeout_remains_supported():
    route = respx.get(_URL).mock(return_value=httpx.Response(200, json={}))
    execute_api(method="GET", url=_URL, timeout=15)
    assert 14 < route.calls[0].request.extensions["timeout"]["read"] <= 15


def test_connect_timeout_retries_cannot_restart_the_timeout_budget(monkeypatch):
    from testmu_appium._helpers import _http
    clock = [0.0]
    calls = []

    def fail(method, url, **kwargs):
        calls.append(kwargs["timeout"])
        clock[0] += kwargs["timeout"]
        raise httpx.ConnectTimeout("connection stalled")

    monkeypatch.setattr(_http, "_monotonic", lambda: clock[0])
    monkeypatch.setattr(_http, "_request_once", fail)
    with pytest.raises(RuntimeError, match="execute_api failed") as error:
        execute_api(method="GET", url=_URL, timeout_ms=15000)
    assert isinstance(error.value.__cause__, httpx.TimeoutException)
    assert calls == [15.0]


@pytest.mark.parametrize("timeout_ms", [0, -1, True, float("inf"), float("nan")])
def test_invalid_millisecond_timeout_is_rejected(timeout_ms):
    with pytest.raises(ValueError, match="timeout_ms"):
        execute_api(method="GET", url=_URL, timeout_ms=timeout_ms)


def test_cloud_millisecond_timeout_uses_15_second_hook_deadline(cloud_session):
    driver = cloud_session({"status": 408, "message": "Request Timed out"})
    result = execute_api(method="GET", url=_URL, timeout_ms=15000)
    (_, args), = driver.calls
    assert args["requestTimeout"] == 15
    assert args["payload"]["timeout"] == 15000
    assert result["status"] == 408


@pytest.mark.parametrize("payload", [{"name": "Admin"}, [{"name": "Admin"}]])
@pytest.mark.parametrize("encoded_by_auteur", [False, True], ids=["raw-json", "auteur-encoded"])
@respx.mock
def test_raw_json_body_reaches_server_as_json_value(payload, encoded_by_auteur):
    raw = json.dumps(payload, indent=2)
    body = json.dumps(raw) if encoded_by_auteur else raw
    route = respx.post(_URL).mock(return_value=httpx.Response(200, json={}))
    execute_api(method="POST", url=_URL, headers={"Content-Type": "application/json"}, body=body)
    assert json.loads(route.calls[0].request.content) == payload


@pytest.mark.parametrize("body", ["plain text", "name=Admin&role=user", "{invalid JSON", "123", "true", "null"])
@respx.mock
def test_non_container_raw_body_remains_sendable(body):
    route = respx.post(_URL).mock(return_value=httpx.Response(200, json={}))
    execute_api(method="POST", url=_URL, body=body)
    assert route.calls[0].request.content == body.encode()


@respx.mock
def test_auteur_encoded_plain_text_loses_only_its_serialization_wrapper():
    route = respx.post(_URL).mock(return_value=httpx.Response(200, json={}))
    execute_api(method="POST", url=_URL, body=json.dumps("plain text"))
    assert route.calls[0].request.content == b"plain text"


def test_cloud_hook_receives_raw_json_without_auteur_serialization_wrapper(cloud_session):
    driver = cloud_session()
    raw = '{\n  "name": "Admin"\n}'
    execute_api(method="POST", url=_URL, headers={"Content-Type": "application/json"}, body=json.dumps(raw))
    (_, args), = driver.calls
    assert args["payload"]["body"] == raw


@pytest.mark.parametrize("settings, expected", [(None, 200), ({}, 200), ({"automatically_follow_redirect": True}, 200), ({"automatically_follow_redirect": False}, 301)])
@respx.mock(assert_all_called=False)
def test_redirect_setting_controls_http_request(settings, expected, respx_mock):
    redirect = respx_mock.get(_URL).mock(return_value=httpx.Response(301, headers={"Location": _URL + "/final"}))
    destination = respx_mock.get(_URL + "/final").mock(return_value=httpx.Response(200, text="destination"))
    result = execute_api(method="GET", url=_URL, settings=settings)
    assert result["status"] == expected
    assert redirect.call_count == 1
    assert destination.call_count == (1 if expected == 200 else 0)
    if expected == 301:
        assert result["headers"]["location"] == _URL + "/final"


@pytest.mark.parametrize("settings, expected", [(None, True), ({}, True), ({"automatically_follow_redirect": True}, True), ({"automatically_follow_redirect": False}, False)])
def test_redirect_setting_reaches_cloud_hook(cloud_session, settings, expected):
    driver = cloud_session()
    execute_api(method="GET", url=_URL, settings=settings)
    assert driver.calls[0][1]["payload"]["settings"]["automatically_follow_redirect"] is expected
