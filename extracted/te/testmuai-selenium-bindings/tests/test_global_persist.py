"""Global-variable ATMS write-back from set_var (V2 parity).

When V3 exported code runs standalone (HyperExecute / code export), the host runtime's
in-product persist hook (web.py -> v3_hooks -> _persist_global_variable) is
absent. The generated code only calls set_var("global.X", value), which writes
the in-memory store and nothing else — so persist-enabled globals never update
on the variables page.

V2 exported code self-persists via update_variable_value_by_name
(PUT {ATMS_URL}/api/v1/variables/name/{name}). These tests pin the equivalent
behavior for the V3 binding: set_var must mirror that PUT for `global.`-prefixed
names (server's 200/403 decides persist, exactly like V2 — no local is_persist
check), guarded on LT creds.
"""
import base64

import pytest
import requests

from testmu_selenium import _config
from testmu_selenium._vars import set_var, var, clear_state, _variable_store


@pytest.fixture(autouse=True)
def reset_state():
    clear_state()
    yield
    clear_state()


class _FakeResp:
    def __init__(self, status_code, text=""):
        self.status_code = status_code
        self.text = text


@pytest.fixture
def lt_creds(monkeypatch):
    monkeypatch.setattr(_config, "lt_auth", True)
    monkeypatch.setenv("ATMS_URL", "https://atms.example.com")
    monkeypatch.setenv("LT_USERNAME", "user")
    monkeypatch.setenv("LT_ACCESS_KEY", "key")


@pytest.fixture
def capture_put(monkeypatch):
    calls = []

    def fake_put(url, headers=None, json=None, **kwargs):
        calls.append({"url": url, "headers": headers, "json": json})
        return _FakeResp(200)

    monkeypatch.setattr(requests, "put", fake_put)
    return calls


class TestSetVarGlobalPersist:
    def test_global_set_var_puts_to_atms_variables_endpoint(self, lt_creds, capture_put):
        """A global. set_var writes the value back to the ATMS variables backend
        with the exact V2 contract (PUT /api/v1/variables/name/{bare_name})."""
        set_var("global.token", "abc123")

        assert len(capture_put) == 1
        call = capture_put[0]
        assert call["url"] == "https://atms.example.com/api/v1/variables/name/token"
        assert call["json"] == {
            "value": "abc123",
            "value_type": "string",
            "type": "variable",
            "environment_id": 0,
        }
        expected_auth = "Basic " + base64.b64encode(b"user:key").decode()
        assert call["headers"]["Authorization"] == expected_auth
        # in-memory store still written (existing behavior preserved)
        assert _variable_store["token"] == "abc123"

    def test_global_set_var_stringifies_value(self, lt_creds, capture_put):
        """Non-string values are coerced to str for the PUT body (V2 parity)."""
        set_var("global.count", 42)
        assert capture_put[0]["json"]["value"] == "42"

    def test_global_set_var_403_does_not_raise(self, lt_creds, monkeypatch):
        """403 = variable not persist-enabled; treat as session-only, never raise."""
        monkeypatch.setattr(requests, "put", lambda *a, **k: _FakeResp(403, "not persistent"))
        set_var("global.token", "abc")  # must not raise
        assert _variable_store["token"] == "abc"

    def test_global_set_var_swallows_network_error(self, lt_creds, monkeypatch):
        """A backend/network failure must not break the running test."""
        def boom(*a, **k):
            raise requests.exceptions.ConnectionError("down")
        monkeypatch.setattr(requests, "put", boom)
        set_var("global.token", "abc")  # must not raise
        assert _variable_store["token"] == "abc"

    def test_non_global_set_var_does_not_call_atms(self, lt_creds, capture_put):
        """Plain (non-global) set_var stays a pure in-memory write — no network."""
        set_var("token", "abc")
        assert capture_put == []
        assert _variable_store["token"] == "abc"

    def test_global_set_var_without_creds_skips_atms(self, monkeypatch, capture_put):
        """No LT creds (standalone / local run) → no ATMS write, store still set."""
        monkeypatch.setattr(_config, "lt_auth", False)
        set_var("global.token", "abc")
        assert capture_put == []
        assert _variable_store["token"] == "abc"


class TestGlobalSetVarResolvesBareReference:
    """The store/resolution key for a global is the BARE name.

    Generated code writes the global output via set_var("global.X", value) but
    reads it back with the BARE reference var("{{X}}") (codegen never prefixes
    reads — global-ness is a property, not part of the canonical name). So a
    global. write MUST land under the bare key, otherwise the bare read misses
    the freshly-set value: it returns the literal template (Selenium symptom) or
    a stale authoring-time seed left under the bare key (Playwright symptom).
    """

    def test_global_write_resolves_via_bare_reference(self, lt_creds, capture_put):
        set_var("global.js_randomInt", "NEW")
        assert var("{{js_randomInt}}") == "NEW"

    def test_global_write_overrides_seeded_bare_value(self, lt_creds, capture_put):
        # test_level_variables seeds the authoring-time value under the bare key.
        _variable_store["js_randomInt"] = "OLD_SEED"
        set_var("global.js_randomInt", "NEW")
        assert var("{{js_randomInt}}") == "NEW"

    def test_global_write_no_creds_resolves_via_bare_reference(self, monkeypatch):
        monkeypatch.setattr(_config, "lt_auth", False)
        set_var("global.js_randomInt", "NEW")
        assert var("{{js_randomInt}}") == "NEW"
