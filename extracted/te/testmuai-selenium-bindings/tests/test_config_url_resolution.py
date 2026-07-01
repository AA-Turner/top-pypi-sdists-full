"""Tests for env-resolution chains in _config.py.

Covers _resolve_automind_url() and _resolve_lt_hub_url() helpers introduced in 0.1.6.

Resolution contracts:
  automind_url: AUTEUR_AUTOMIND > AUTOMIND_URL > prod default
  lt_hub_url:   LT_HUB_URL (explicit) > derived(HYE_HUB + creds) > prod default
  no side-effects: the resolvers are pure — neither AUTOMIND_URL nor LT_HUB_URL is
                   mutated in os.environ (the binding must not change the host env).
"""
import importlib
import os

import pytest

import testmu_selenium._config as _config_mod

_PROD_AUTOMIND = "https://kaneai-api.lambdatest.com"
_PROD_LT_HUB = "https://hub.lambdatest.com/wd/hub"

# All env vars that the resolution helpers may read or write — must all be cleared
# before every reload so test ordering cannot affect results.
_URL_ENV_VARS = (
    "AUTEUR_AUTOMIND",
    "AUTOMIND_URL",
    "LT_HUB_URL",
    "HYE_HUB",
    "LT_USERNAME",
    "LT_ACCESS_KEY",
)


def _reload(monkeypatch, **env):
    """Clear all URL-related env vars, then set only the ones supplied, then reload."""
    for key in _URL_ENV_VARS:
        monkeypatch.delenv(key, raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    return importlib.reload(_config_mod)


# ---------------------------------------------------------------------------
# automind_url resolution chain
# ---------------------------------------------------------------------------


class TestAutomindUrlResolution:
    def test_auteur_automind_wins_over_automind_url(self, monkeypatch):
        """AUTEUR_AUTOMIND takes priority when both env vars are set."""
        cfg = _reload(
            monkeypatch,
            AUTEUR_AUTOMIND="https://hephaestus-dev.example.com",
            AUTOMIND_URL="https://other.example.com",
        )
        assert cfg.get("automind_url") == "https://hephaestus-dev.example.com"

    def test_auteur_automind_wins_when_automind_url_unset(self, monkeypatch):
        """AUTEUR_AUTOMIND wins even if AUTOMIND_URL is absent."""
        cfg = _reload(monkeypatch, AUTEUR_AUTOMIND="https://hephaestus-dev.example.com")
        assert cfg.get("automind_url") == "https://hephaestus-dev.example.com"

    def test_automind_url_wins_when_auteur_automind_unset(self, monkeypatch):
        """Falls back to AUTOMIND_URL when AUTEUR_AUTOMIND is not set."""
        cfg = _reload(monkeypatch, AUTOMIND_URL="https://custom-automind.example.com")
        assert cfg.get("automind_url") == "https://custom-automind.example.com"

    def test_prod_default_when_both_unset(self, monkeypatch):
        """Falls back to prod default when neither AUTEUR_AUTOMIND nor AUTOMIND_URL is set."""
        cfg = _reload(monkeypatch)
        assert cfg.get("automind_url") == _PROD_AUTOMIND

    def test_resolve_does_not_mutate_automind_url_env(self, monkeypatch):
        """The resolver is pure: resolving from AUTEUR_AUTOMIND must NOT write
        os.environ["AUTOMIND_URL"] (the binding must not mutate the host env)."""
        cfg = _reload(monkeypatch, AUTEUR_AUTOMIND="https://hephaestus-dev.example.com")
        assert cfg.get("automind_url") == "https://hephaestus-dev.example.com"
        # AUTOMIND_URL was delenv'd in _reload and must remain absent
        assert os.environ.get("AUTOMIND_URL") is None

    def test_resolve_prod_default_does_not_write_env(self, monkeypatch):
        """Even when falling back to the prod default, os.environ["AUTOMIND_URL"]
        must NOT be written."""
        cfg = _reload(monkeypatch)
        assert cfg.get("automind_url") == _PROD_AUTOMIND
        assert os.environ.get("AUTOMIND_URL") is None


# ---------------------------------------------------------------------------
# lt_hub_url resolution chain
# ---------------------------------------------------------------------------


class TestLtHubUrlResolution:
    def test_explicit_lt_hub_url_wins(self, monkeypatch):
        """Explicit LT_HUB_URL takes priority over HYE_HUB derivation."""
        cfg = _reload(
            monkeypatch,
            LT_HUB_URL="https://explicit-hub.example.com/wd/hub",
            HYE_HUB="hye-cluster.example.com",
            LT_USERNAME="user",
            LT_ACCESS_KEY="key",
        )
        assert cfg.get("lt_hub_url") == "https://explicit-hub.example.com/wd/hub"

    def test_derived_url_when_hye_hub_and_creds_set(self, monkeypatch):
        """Derives http://user:key@hye/wd/hub when LT_HUB_URL is absent but all creds present."""
        cfg = _reload(
            monkeypatch,
            HYE_HUB="hye-cluster.example.com",
            LT_USERNAME="myuser",
            LT_ACCESS_KEY="mykey",
        )
        assert cfg.get("lt_hub_url") == "http://myuser:mykey@hye-cluster.example.com/wd/hub"

    def test_prod_default_when_hye_hub_set_but_username_missing(self, monkeypatch):
        """Does NOT derive when LT_USERNAME is absent — avoids malformed URL."""
        cfg = _reload(
            monkeypatch,
            HYE_HUB="hye-cluster.example.com",
            LT_ACCESS_KEY="mykey",
        )
        assert cfg.get("lt_hub_url") == _PROD_LT_HUB

    def test_prod_default_when_hye_hub_set_but_accesskey_missing(self, monkeypatch):
        """Does NOT derive when LT_ACCESS_KEY is absent — avoids malformed URL."""
        cfg = _reload(
            monkeypatch,
            HYE_HUB="hye-cluster.example.com",
            LT_USERNAME="myuser",
        )
        assert cfg.get("lt_hub_url") == _PROD_LT_HUB

    def test_prod_default_when_hye_hub_unset(self, monkeypatch):
        """Falls back to prod default when HYE_HUB is not set."""
        cfg = _reload(monkeypatch, LT_USERNAME="myuser", LT_ACCESS_KEY="mykey")
        assert cfg.get("lt_hub_url") == _PROD_LT_HUB

    def test_lt_hub_url_env_not_mutated(self, monkeypatch):
        """os.environ["LT_HUB_URL"] is NOT written as a side-effect (unlike AUTOMIND_URL)."""
        _reload(
            monkeypatch,
            HYE_HUB="hye-cluster.example.com",
            LT_USERNAME="myuser",
            LT_ACCESS_KEY="mykey",
        )
        # LT_HUB_URL was delenv'd in _reload; it must remain absent after resolution
        assert os.environ.get("LT_HUB_URL") is None


# ---------------------------------------------------------------------------
# Module teardown — restore _config to a clean baseline for other test modules
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True, scope="module")
def _restore_config():
    """Reload _config once at module teardown so other tests see baseline state."""
    yield
    importlib.reload(_config_mod)
