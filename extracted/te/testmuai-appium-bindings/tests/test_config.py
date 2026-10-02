"""Env gates and URL resolvers."""
import importlib
import os

import pytest

from testmu_appium import _config


def _reload(monkeypatch, **env):
    for key, value in env.items():
        if value is None:
            monkeypatch.delenv(key, raising=False)
        else:
            monkeypatch.setenv(key, value)
    return importlib.reload(_config)


def test_smart_defaults_to_enabled(monkeypatch):
    """TESTMU_SMART defaults to "1"."""
    mod = _reload(monkeypatch, TESTMU_SMART=None)
    assert mod.smart is True


def test_smart_off_when_env_zero(monkeypatch):
    mod = _reload(monkeypatch, TESTMU_SMART="0")
    assert mod.smart is False


def test_run_target_defaults_local(monkeypatch):
    mod = _reload(monkeypatch, TESTMU_RUN_TARGET=None)
    assert mod.run_target == "local"


def test_lt_auth_requires_both_credentials(monkeypatch):
    mod = _reload(monkeypatch, LT_USERNAME="u", LT_ACCESS_KEY=None)
    assert mod.lt_auth is False
    mod = _reload(monkeypatch, LT_USERNAME="u", LT_ACCESS_KEY="k")
    assert mod.lt_auth is True


@pytest.mark.parametrize(
    "env,expected",
    [
        ({}, "http://127.0.0.1:4723"),
        ({"APPIUM_URL": "http://10.0.0.5:4723"}, "http://10.0.0.5:4723"),
    ],
)
def test_resolve_appium_url(monkeypatch, env, expected):
    monkeypatch.delenv("APPIUM_URL", raising=False)
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    assert _config._resolve_appium_url() == expected


@pytest.mark.parametrize(
    "env,expected",
    [
        ({}, "https://mobile-hub.lambdatest.com/wd/hub"),
        ({"LT_HUB_URL": "http://custom/wd/hub"}, "http://custom/wd/hub"),
        # Forge and code-export export the V2-style bare host; passed verbatim
        # to webdriver.Remote it 404s on /session, so resolution widens it.
        ({"LT_HUB_URL": "mobile-hub.lambdatest.com"}, "https://mobile-hub.lambdatest.com/wd/hub"),
        (
            {"LT_HUB_URL": "stage-mobile-hub.lambdatestinternal.com"},
            "https://stage-mobile-hub.lambdatestinternal.com/wd/hub",
        ),
        ({"LT_HUB_URL": "https://custom-hub/"}, "https://custom-hub/wd/hub"),
    ],
)
def test_resolve_lt_hub_url(monkeypatch, env, expected):
    monkeypatch.delenv("LT_HUB_URL", raising=False)
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    assert _config._resolve_lt_hub_url() == expected


def test_import_does_not_mutate_env():
    """The binding never writes os.environ at import."""
    before = dict(os.environ)
    importlib.reload(_config)
    assert dict(os.environ) == before


@pytest.mark.parametrize(
    "env,expected",
    [
        ({}, None),
        ({"TESTMU_API_PROXY_PORT": "20037"}, "http://127.0.0.1:20037"),
        (
            {"TESTMU_API_PROXY_HOST": "10.0.0.5", "TESTMU_API_PROXY_PORT": "8080"},
            "http://10.0.0.5:8080",
        ),
        # A host alone selects nothing — the port is the on switch.
        ({"TESTMU_API_PROXY_HOST": "10.0.0.5"}, None),
    ],
)
def test_get_api_proxy_url(monkeypatch, env, expected):
    for k in ("TESTMU_API_PROXY_HOST", "TESTMU_API_PROXY_PORT"):
        monkeypatch.delenv(k, raising=False)
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    assert _config.get_api_proxy_url() == expected
