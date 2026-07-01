"""Test env-var detection for run_target / lt_auth (mirrors playwright sibling)."""
import importlib

import pytest

import testmu_selenium._config as _config_mod


def _reload_config(monkeypatch, **env):
    """Reload _config with controlled env vars; return the fresh module."""
    for key in ("TESTMU_RUN_TARGET", "LT_USERNAME", "LT_ACCESS_KEY"):
        monkeypatch.delenv(key, raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    return importlib.reload(_config_mod)


class TestRunTarget:
    def test_default_run_target_is_local(self, monkeypatch):
        cfg = _reload_config(monkeypatch)
        assert cfg.run_target == "local"

    def test_run_target_cloud_override(self, monkeypatch):
        cfg = _reload_config(monkeypatch, TESTMU_RUN_TARGET="cloud")
        assert cfg.run_target == "cloud"

    def test_run_target_lowercased(self, monkeypatch):
        cfg = _reload_config(monkeypatch, TESTMU_RUN_TARGET="CLOUD")
        assert cfg.run_target == "cloud"


class TestLtAuth:
    def test_lt_auth_false_when_no_creds(self, monkeypatch):
        cfg = _reload_config(monkeypatch)
        assert cfg.lt_auth is False

    def test_lt_auth_false_when_only_username(self, monkeypatch):
        cfg = _reload_config(monkeypatch, LT_USERNAME="u")
        assert cfg.lt_auth is False

    def test_lt_auth_false_when_only_access_key(self, monkeypatch):
        cfg = _reload_config(monkeypatch, LT_ACCESS_KEY="k")
        assert cfg.lt_auth is False

    def test_lt_auth_true_when_both_present(self, monkeypatch):
        cfg = _reload_config(monkeypatch, LT_USERNAME="u", LT_ACCESS_KEY="k")
        assert cfg.lt_auth is True

    def test_lt_auth_false_when_creds_empty_strings(self, monkeypatch):
        cfg = _reload_config(monkeypatch, LT_USERNAME="", LT_ACCESS_KEY="")
        assert cfg.lt_auth is False


@pytest.fixture(autouse=True, scope="module")
def _restore_config():
    """Reload _config once at module teardown so other tests see baseline state."""
    yield
    importlib.reload(_config_mod)
