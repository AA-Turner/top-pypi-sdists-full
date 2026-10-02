"""Pinned provider, normalization, and assertion semantics for network v1."""
import base64

import pytest

from testmu_appium import _config
from testmu_appium._helpers import network_query as module
from testmu_appium._helpers.network_query import (
    ASSERTION_SCHEMA_VERSION,
    CAPTURE_SCHEMA_VERSION,
    NetworkAssertionError,
    NetworkCaptureContractError,
    NetworkCaptureTimeout,
    NetworkCaptureUnavailable,
    evaluate_network_assertion,
    network_capture_capabilities,
    network_capture_query,
    network_query,
)
from testmu_appium._vars import clear_state, set_var


class _FakeDriver:
    pass


@pytest.fixture(autouse=True)
def _clean_network_env(monkeypatch):
    clear_state()
    monkeypatch.delenv("TESTMU_NETWORK_CAPTURE_URL", raising=False)
    monkeypatch.delenv("TESTMU_NETWORK_CAPTURE_PROVIDER", raising=False)
    monkeypatch.delenv("HOST_IP", raising=False)
    monkeypatch.delenv("PROXY_API_PORT", raising=False)
    monkeypatch.delenv("TESTMU_NETWORK_CAPTURE_SCHEME", raising=False)
    monkeypatch.delenv("TESTMU_SKIP_ASSERTION_FAILURE", raising=False)
    monkeypatch.setattr(_config, "run_target", "local")
    yield
    clear_state()


def _flow(flow_id="flow-1", *, method="GET", url="https://api.test/items", body=None):
    return {
        "schema_version": CAPTURE_SCHEMA_VERSION,
        "id": flow_id,
        "lifecycle": "completed",
        "request": {"method": method, "url": url, "headers": [], "body": body or {}},
        "response": {"status": 200, "headers": [], "body": body or {}},
    }


def _contract(**selector):
    return {
        "schema_version": CAPTURE_SCHEMA_VERSION,
        "selector": {
            "method": "GET", "url": "https://api.test/items", "occurrence": 0,
            "flow_id": "", **selector,
        },
        "wait": {"poll_interval_ms": 10, "timeout_ms": 10},
    }


def test_local_without_explicit_provider_is_typed_unavailable():
    with pytest.raises(NetworkCaptureUnavailable):
        network_capture_query(_FakeDriver(), contract=_contract())


def test_canonical_contract_uses_the_pinned_stable_flows_endpoint(monkeypatch):
    monkeypatch.setenv("TESTMU_NETWORK_CAPTURE_URL", "http://capture.internal/")
    calls = []

    def request_json(url, *, timeout):
        calls.append((url, timeout))
        return 200, {"flows": [_flow("first"), _flow("second")]}

    monkeypatch.setattr(module, "_request_json", request_json)
    result = network_capture_query(_FakeDriver(), contract=_contract(occurrence=1))

    assert calls == [("http://capture.internal/v1/network/capture/flows", 1)]
    assert result["schema_version"] == CAPTURE_SCHEMA_VERSION
    assert result["id"] == "second"
    assert result["request"]["url"] == "https://api.test/items"


def test_detail_flow_id_is_path_quoted_and_uses_the_pinned_endpoint(monkeypatch):
    monkeypatch.setenv("TESTMU_NETWORK_CAPTURE_URL", "http://capture.internal")
    calls = []
    monkeypatch.setattr(module, "_request_json", lambda url, *, timeout: (
        calls.append(url) or 200, {"flow": _flow("a/b")}
    ))

    result = network_capture_query(_FakeDriver(), contract=_contract(flow_id="a/b"))

    assert calls == ["http://capture.internal/v1/network/capture/flows/a%2Fb"]
    assert result["id"] == "a/b"


def test_lambda_har_is_normalized_and_security_prefixed_base64_json_is_parsed(monkeypatch):
    monkeypatch.setenv("TESTMU_NETWORK_CAPTURE_URL", "http://lambda.internal")
    monkeypatch.setenv("TESTMU_NETWORK_CAPTURE_PROVIDER", "lambda-har")
    encoded = base64.b64encode(b")]}'\n{\"ok\":true}").decode()
    har = {
        "_id": "har-1", "startedDateTime": "2026-07-29T10:00:00Z",
        "_resourceType": "xhr", "request": {
            "method": "GET", "url": "https://api.test/items",
            "headers": [{"name": "Accept", "value": "application/json"}],
            "queryString": [{"name": "page", "value": "1"}],
            "cookies": [{"name": "sid", "value": "abc"}],
            "postData": {"mimeType": "application/json", "text": "{}"}, "bodySize": 2,
        },
        "response": {
            "status": 200, "headers": [{"name": "Content-Type", "value": "application/json"}],
            "content": {"mimeType": "application/json", "encoding": "base64", "text": encoded, "size": 17},
            "redirectURL": "https://api.test/next",
        },
        "timings": {"wait": 7, "dns": -1, "unknown": "omit"}, "time": 9,
        "serverIPAddress": "10.0.0.1",
        "_webSocketMessages": [{"type": "send", "time": 1.5, "opcode": 1, "data": "hello"}],
    }
    monkeypatch.setattr(module, "_request_json", lambda url, *, timeout: (200, {"log": {"entries": [har]}}))

    result = network_capture_query(_FakeDriver(), contract=_contract())

    assert result["schema_version"] == CAPTURE_SCHEMA_VERSION
    assert result["id"] == "har-1"
    assert result["resource_type"] == "xhr"
    assert result["request"]["query"] == [{"name": "page", "value": "1"}]
    assert result["request"]["body"]["size"] == 2
    assert result["request"]["body"]["json"] == {}
    assert result["response"]["redirect_url"] == "https://api.test/next"
    assert result["response"]["body"] == {
        "availability": "complete", "available": True, "encoding": "utf-8",
        "mime_type": "application/json", "content_encoding": "", "size": 17,
        "captured_size": len(")]}'\n{\"ok\":true}".encode()), "data": ")]}'\n{\"ok\":true}",
        "json": {"ok": True}, "truncation_reason": None,
    }
    assert result["timings"] == {"wait": 7, "dns": None, "total": 9}
    assert result["connection"] == {"server_ip": "10.0.0.1", "id": ""}
    assert result["messages"] == [{
        "direction": "send", "time": 1.5, "opcode": 1,
        "body": {
            "availability": "complete", "available": True, "encoding": "utf-8",
            "mime_type": "", "content_encoding": "", "size": None,
            "captured_size": 5, "data": "hello", "json": None, "truncation_reason": None,
        },
    }]


def test_capabilities_uses_pinned_endpoint_and_lambda_is_synthesized(monkeypatch):
    monkeypatch.setenv("TESTMU_NETWORK_CAPTURE_URL", "http://capture.internal")
    calls = []
    monkeypatch.setattr(module, "_request_json", lambda url, *, timeout: (
        calls.append(url) or 200, {
            "schema_version": CAPTURE_SCHEMA_VERSION,
            "provider": "contract",
            "protocols": ["http", "https"],
            "https_decryption": True,
            "request_bodies": "complete",
            "response_bodies": "complete",
            "live_events": False,
            "tls_metadata": False,
            "limitations": [],
        }
    ))
    assert network_capture_capabilities()["provider"] == "contract"
    assert calls == ["http://capture.internal/v1/network/capture/capabilities"]

    monkeypatch.setenv("TESTMU_NETWORK_CAPTURE_PROVIDER", "lambda-har")
    lambda_capabilities = network_capture_capabilities()
    assert lambda_capabilities["provider"] == "lambda-har"
    assert lambda_capabilities["request_bodies"] == "partial"
    assert calls == ["http://capture.internal/v1/network/capture/capabilities"]


def test_capabilities_rejects_an_incomplete_contract_provider(monkeypatch):
    monkeypatch.setenv("TESTMU_NETWORK_CAPTURE_URL", "http://capture.internal")
    monkeypatch.setattr(
        module,
        "_request_json",
        lambda url, *, timeout: (
            200,
            {
                "schema_version": CAPTURE_SCHEMA_VERSION,
                "provider": "contract",
            },
        ),
    )

    with pytest.raises(NetworkCaptureContractError, match="protocols"):
        network_capture_capabilities()


@pytest.mark.parametrize("contract", [
    {},
    {"schema_version": "network.capture.v0", "selector": {}, "wait": {}},
    _contract(method="get"),
    _contract(url="/items"),
    _contract(flow_id="not valid"),
    _contract(occurrence=-1),
    _contract(occurrence=10001),
    {**_contract(), "wait": {"poll_interval_ms": 0, "timeout_ms": 10}},
    {**_contract(), "wait": {"poll_interval_ms": 10, "timeout_ms": 120001}},
    {**_contract(), "wait": {"poll_interval_ms": 20, "timeout_ms": 10}},
])
def test_canonical_contract_rejects_schema_and_invalid_timings(contract):
    with pytest.raises(NetworkCaptureContractError):
        network_capture_query(_FakeDriver(), contract=contract)


def test_timeout_is_typed_never_an_empty_dict(monkeypatch):
    monkeypatch.setenv("TESTMU_NETWORK_CAPTURE_URL", "http://capture.internal")
    monkeypatch.setattr(module, "_request_json", lambda url, *, timeout: (200, {"flows": []}))
    with pytest.raises(NetworkCaptureTimeout):
        network_capture_query(_FakeDriver(), contract=_contract())


def test_zero_length_body_is_complete_not_unavailable(monkeypatch):
    monkeypatch.setenv("TESTMU_NETWORK_CAPTURE_URL", "http://lambda.internal")
    monkeypatch.setenv("TESTMU_NETWORK_CAPTURE_PROVIDER", "lambda-har")
    har = {
        "_id": "empty",
        "request": {
            "method": "GET",
            "url": "https://api.test/items",
            "bodySize": 0,
        },
        "response": {"status": 204, "bodySize": 0, "content": {"size": 0}},
    }
    monkeypatch.setattr(
        module,
        "_request_json",
        lambda url, *, timeout: (200, {"log": {"entries": [har]}}),
    )

    flow = network_capture_query(_FakeDriver(), contract=_contract())

    assert flow["request"]["body"]["availability"] == "complete"
    assert flow["request"]["body"]["data"] == ""
    assert flow["response"]["body"]["availability"] == "complete"
    assert flow["response"]["body"]["data"] == ""


def test_legacy_query_wraps_the_canonical_contract_and_writes_output(monkeypatch):
    monkeypatch.setenv("TESTMU_NETWORK_CAPTURE_URL", "http://capture.internal")
    monkeypatch.setattr(module, "_request_json", lambda url, *, timeout: (200, {"flows": [_flow()]}))

    result = network_query(_FakeDriver(), method="GET", url="https://api.test/items", output_variable="flow")

    assert result["id"] == "flow-1"
    assertion = evaluate_network_assertion({"operator": "equals", "left_operand": "{{flow.id}}", "right_operand": "flow-1"})
    assert assertion["status"] == "passed"
    assert assertion["matched_flow_ids"] == ["flow-1"]


def test_host_details_select_lambda_even_when_authoring_config_left_run_target_local(monkeypatch):
    monkeypatch.setenv("HOST_IP", "10.0.0.5")
    monkeypatch.setenv("PROXY_API_PORT", "8181")
    calls = []
    monkeypatch.setattr(module, "_request_json", lambda url, *, timeout: (
        calls.append(url) or 200, {"log": {"entries": [{
            "_id": "har", "request": {"method": "GET", "url": "https://api.test/items"}, "response": {},
        }]}}
    ))

    flow = network_capture_query(_FakeDriver(), contract=_contract())
    assert flow["id"] == "har"
    assert flow["resource_type"] == "http"
    assert calls == ["http://10.0.0.5:8181/har"]


def test_network_assertion_returns_evidence_and_raises_typed_error_on_failed():
    set_var("response", {"status": 500})
    with pytest.raises(NetworkAssertionError) as error:
        evaluate_network_assertion({"operator": "equals", "left_operand": "{{response.status}}", "right_operand": "200"})
    assert error.value.result["schema_version"] == ASSERTION_SCHEMA_VERSION
    assert error.value.result["outcome"] == "failed"
    assert error.value.result["evaluations"][0]["left"] == 500


def test_network_assertion_marks_unavailable_body_indeterminate_and_can_be_skipped(monkeypatch):
    set_var("flow", _flow(body={"available": False}))
    tree = {"operator": "equals", "left_operand": "{{flow.response.body.json.ok}}", "right_operand": "true"}
    with pytest.raises(NetworkAssertionError) as error:
        evaluate_network_assertion(tree)
    assert error.value.result["status"] == "indeterminate"
    assert error.value.result["evaluations"][0]["reason"] == "body_unavailable"

    monkeypatch.setenv("TESTMU_SKIP_ASSERTION_FAILURE", "true")
    result = evaluate_network_assertion(tree)
    assert result["outcome"] == result["status"] == "indeterminate"


def test_network_assertion_rejects_an_unknown_contract_version():
    with pytest.raises(NetworkAssertionError):
        evaluate_network_assertion({}, contract_version="network.assert.v0")


def test_network_assertion_supports_exists_not_exists_and_matches(monkeypatch):
    set_var("payload", {"name": "alice-42"})
    assert evaluate_network_assertion({"operator": "exists", "left_operand": "{{payload.name}}"})["status"] == "passed"
    assert evaluate_network_assertion({"operator": "not_exists", "left_operand": "{{payload.missing}}"})["status"] == "passed"
    assert evaluate_network_assertion({"operator": "matches", "left_operand": "{{payload.name}}", "right_operand": r"^alice-\d+$"})["status"] == "passed"


def test_network_assertion_resolves_zero_based_dotted_list_indexes():
    set_var("flow", {**_flow(), "messages": [{"body": {"data": "connected"}}]})

    result = evaluate_network_assertion({
        "operator": "equals",
        "left_operand": "{{flow.messages.0.body.data}}",
        "right_operand": "connected",
    })

    assert result["status"] == "passed"
    assert result["matched_flow_ids"] == ["flow-1"]


def test_a_stale_flow_id_falls_back_to_selector_matching(monkeypatch):
    """The recorded id belongs to the authoring session's provider; a replay's
    provider minted its own. The miss falls back to the live method/url match
    (the web helper's semantics) instead of failing the step."""
    monkeypatch.setenv("TESTMU_NETWORK_CAPTURE_URL", "http://capture.internal")
    calls = []

    def _fake(url, *, timeout):
        calls.append(url)
        if "/flows/stale-id" in url:
            return 404, None  # non-JSON 404 body, as the lambda proxy answers
        return 200, {"flows": [_flow("fresh-1")]}

    monkeypatch.setattr(module, "_request_json", _fake)
    result = network_capture_query(_FakeDriver(), contract=_contract(flow_id="stale-id"))
    assert result["id"] == "fresh-1"
    assert calls[0].endswith("/flows/stale-id")


def test_a_stale_flow_id_with_no_matching_traffic_times_out(monkeypatch):
    """The fallback is a real search, not a rescue: when the live capture never
    shows the selector's flow either, the query ends in the typed timeout."""
    monkeypatch.setenv("TESTMU_NETWORK_CAPTURE_URL", "http://capture.internal")

    def _fake(url, *, timeout):
        if "/flows/stale-id" in url:
            return 404, None
        return 200, {"flows": []}

    monkeypatch.setattr(module, "_request_json", _fake)
    with pytest.raises(NetworkCaptureTimeout):
        network_capture_query(_FakeDriver(), contract=_contract(flow_id="stale-id"))


def test_a_non_json_error_body_reports_its_status_not_a_contract_error(monkeypatch):
    """A 404 with an empty/HTML body is a 404 — parse failure must not mask the
    status the caller translates. A 2xx with a broken body stays a contract
    error."""
    class _Resp:
        def __init__(self, status):
            self.status_code = status

        def json(self):
            raise ValueError("not json")

    responses = {}
    monkeypatch.setattr(
        module, "request_with_retry",
        lambda method, url, *, timeout, silent: responses["resp"])

    responses["resp"] = _Resp(404)
    assert module._request_json("http://capture.internal/x", timeout=1) == (404, None)

    responses["resp"] = _Resp(200)
    with pytest.raises(NetworkCaptureContractError):
        module._request_json("http://capture.internal/x", timeout=1)


def test_legacy_index_is_one_based_like_v2_and_web(monkeypatch):
    """`index=1` is the FIRST occurrence (V2's poll loop and the web helper both
    count 1-based); the canonical contract is 0-based, so the wrapper subtracts.
    Passing it raw asked for the occurrence after the recorded one — a
    guaranteed timeout for a single matching flow."""
    monkeypatch.setenv("TESTMU_NETWORK_CAPTURE_URL", "http://capture.internal")
    flows = {"flows": [_flow("first"), _flow("second")]}
    monkeypatch.setattr(module, "_request_json", lambda url, *, timeout: (200, flows))

    assert network_query(_FakeDriver(), method="GET", url="https://api.test/items",
                         index=1)["id"] == "first"
    assert network_query(_FakeDriver(), method="GET", url="https://api.test/items",
                         index=2)["id"] == "second"
