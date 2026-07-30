"""Bug D regression: ATMS_URL default + reserved-namespace error propagation.

D1: _atms_get_variable and _atms_get_totp_seed must use a real HTTPS default
    when ATMS_URL env var is unset, not "". "" → "No scheme supplied" errors
    that are swallowed or surface as mysterious failures.
    Matches the PW sibling (testmu/_vars.py lines 429/443).

D2: resolve_variable must let TestmuConfigError propagate for reserved namespaces
    (global/totp/environment) rather than catching and returning the raw mustache
    literal — which causes false-passes (test looks green but var unresolved).
"""
import pytest
import requests

from testmu_selenium import _config
from testmu_selenium._vars import (
    _atms_get_totp_seed,
    _atms_get_variable,
    clear_state,
    resolve_variable,
)
from testmu_selenium._errors import TestmuConfigError

_EXPECTED_DEFAULT_HOST = "test-manager-api.lambdatest.com"


@pytest.fixture(autouse=True)
def reset(monkeypatch):
    clear_state()
    # No ATMS_URL in env — exercises the "unset" default path.
    monkeypatch.delenv("ATMS_URL", raising=False)
    yield
    clear_state()


# ---------------------------------------------------------------------------
# D1 — ATMS URL default at the two READ sites
# ---------------------------------------------------------------------------

class _FakeResp:
    def __init__(self, status_code, data):
        self.status_code = status_code
        self._data = data

    def json(self):
        return {"data": self._data}


class TestAtmsUrlDefault:
    def test_get_variable_uses_https_default(self, monkeypatch):
        """_atms_get_variable: ATMS_URL unset → URL contains the hardcoded HTTPS host."""
        captured = {}

        def fake_get(url, headers=None, **kwargs):
            captured["url"] = url
            return _FakeResp(200, {"value": "x"})

        monkeypatch.setattr(requests, "get", fake_get)
        _atms_get_variable("some_var")

        url = captured.get("url", "")
        assert url.startswith("https://"), (
            f"Expected URL to start with 'https://', got {url!r}. "
            f"ATMS_URL was unset — default must be the hardcoded host."
        )
        assert _EXPECTED_DEFAULT_HOST in url, (
            f"Expected URL to contain '{_EXPECTED_DEFAULT_HOST}', got {url!r}"
        )

    def test_get_totp_seed_uses_https_default(self, monkeypatch):
        """_atms_get_totp_seed: ATMS_URL unset → URL contains the hardcoded HTTPS host."""
        captured = {}

        def fake_get(url, headers=None, **kwargs):
            captured["url"] = url
            return _FakeResp(200, "JBSWY3DPEHPK3PXP")

        monkeypatch.setattr(requests, "get", fake_get)
        _atms_get_totp_seed("login_secret")

        url = captured.get("url", "")
        assert url.startswith("https://"), (
            f"Expected URL to start with 'https://', got {url!r}. "
            f"ATMS_URL was unset — default must be the hardcoded host."
        )
        assert _EXPECTED_DEFAULT_HOST in url, (
            f"Expected URL to contain '{_EXPECTED_DEFAULT_HOST}', got {url!r}"
        )


# ---------------------------------------------------------------------------
# D2 — reserved-namespace failures must propagate, not return the literal
# ---------------------------------------------------------------------------

class TestReservedNsErrorPropagation:
    def test_totp_no_creds_no_env_raises_via_resolve_variable(self, monkeypatch):
        """{{totp.x}} with no LT creds + no TESTMU_TOTP_* → TestmuConfigError raised.

        Old behavior: catch + return '{{totp.login}}' → false-pass.
        New behavior: propagate → test aborts loudly.
        """
        monkeypatch.setattr(_config, "lt_auth", False)
        monkeypatch.delenv("TESTMU_TOTP_login", raising=False)
        with pytest.raises(TestmuConfigError):
            resolve_variable("totp.login", "{{totp.login}}")

    def test_global_no_creds_no_env_raises_via_resolve_variable(self, monkeypatch):
        """{{global.x}} with no creds + no store/env fallback → TestmuConfigError raised."""
        monkeypatch.setattr(_config, "lt_auth", False)
        monkeypatch.delenv("TESTMU_VAR_ghost", raising=False)
        with pytest.raises(TestmuConfigError):
            resolve_variable("ghost", "{{global.ghost}}")

    def test_bare_name_path_also_propagates(self, monkeypatch):
        """resolve_variable(name, plain_default) bare-name path: reserved-ns raises."""
        monkeypatch.setattr(_config, "lt_auth", False)
        monkeypatch.delenv("TESTMU_TOTP_acct", raising=False)
        # No {{}} in template — exercises the `if name:` branch of resolve_variable.
        with pytest.raises(TestmuConfigError):
            resolve_variable("totp.acct", "plain_default")
