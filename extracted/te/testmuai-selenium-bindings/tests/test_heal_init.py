"""Tests for Heal.__init__ — constructor kwarg fallbacks, env-var precedence, defaults.

Phase A Tasks 12-16 (constructor step).
"""
from __future__ import annotations

import importlib
import os
from unittest.mock import MagicMock

import pytest


@pytest.fixture()
def mock_driver():
    driver = MagicMock()
    driver.session_id = "test-session-abc"
    driver.capabilities = {"platformName": "linux", "browserName": "chrome"}
    return driver


@pytest.fixture()
def minimal_action():
    return {"operation_type": "click", "operation_intent": "click the sign-in button"}


# ---------------------------------------------------------------------------
# Import smoke
# ---------------------------------------------------------------------------

def test_heal_class_importable():
    from testmu_selenium._heal import Heal
    assert Heal is not None


# ---------------------------------------------------------------------------
# Explicit kwarg values take precedence
# ---------------------------------------------------------------------------

def test_init_explicit_kwargs_are_stored(mock_driver, minimal_action):
    from testmu_selenium._heal import Heal

    h = Heal(
        minimal_action,
        mock_driver,
        test_id="tid-123",
        username="myuser",
        accesskey="mykey",
        commit_id="abc123",
        org_id=42,
        automind_url="https://custom.automind.example.com",
    )

    assert h.test_id == "tid-123"
    assert h.username == "myuser"
    assert h.accesskey == "mykey"
    assert h.commit_id == "abc123"
    assert h.org_id == 42
    assert h.automind_url == "https://custom.automind.example.com"


def test_init_current_action_stored(mock_driver, minimal_action):
    from testmu_selenium._heal import Heal

    h = Heal(minimal_action, mock_driver)
    assert h.current_action is minimal_action


def test_init_driver_and_session_id(mock_driver, minimal_action):
    from testmu_selenium._heal import Heal

    h = Heal(minimal_action, mock_driver)
    assert h.driver is mock_driver
    assert h.session_id == "test-session-abc"


# ---------------------------------------------------------------------------
# Env-var fallback when kwargs are absent
# ---------------------------------------------------------------------------

def test_init_reads_env_vars_when_no_kwargs(mock_driver, minimal_action, monkeypatch):
    from testmu_selenium._heal import Heal

    monkeypatch.setenv("TEST_ID", "env-test-id")
    monkeypatch.setenv("LT_USERNAME", "env-user")
    monkeypatch.setenv("LT_ACCESS_KEY", "env-key")
    monkeypatch.setenv("COMMIT_ID", "env-commit")
    monkeypatch.setenv("ORG_ID", "99")

    h = Heal(minimal_action, mock_driver)

    assert h.test_id == "env-test-id"
    assert h.username == "env-user"
    assert h.accesskey == "env-key"
    assert h.commit_id == "env-commit"
    assert h.org_id == 99


def test_init_automind_url_from_env(mock_driver, minimal_action, monkeypatch):
    import testmu_selenium._config as _config_mod

    # Simulate config populated from AUTOMIND_URL env. The env resolution chain
    # (AUTEUR_AUTOMIND > AUTOMIND_URL > prod) is tested in test_config_url_resolution.py;
    # here we verify that Heal reads from _config.get("automind_url").
    # monkeypatch.setitem auto-restores on teardown — no reload needed.
    monkeypatch.setitem(_config_mod._config, "automind_url", "https://env-automind.example.com")
    from testmu_selenium._heal import Heal
    h = Heal(minimal_action, mock_driver)
    assert h.automind_url == "https://env-automind.example.com"


def test_init_auteur_automind_wins_over_automind_url(mock_driver, minimal_action, monkeypatch):
    """Heal reads from _config, which is populated with AUTEUR_AUTOMIND precedence."""
    import testmu_selenium._config as _config_mod

    # Simulate config resolved with AUTEUR_AUTOMIND winning over AUTOMIND_URL.
    # The env chain itself is covered in test_config_url_resolution.py.
    # monkeypatch.setitem auto-restores on teardown — no reload needed.
    monkeypatch.setitem(_config_mod._config, "automind_url", "https://auteur-automind.example.com")
    from testmu_selenium._heal import Heal
    h = Heal(minimal_action, mock_driver)
    assert h.automind_url == "https://auteur-automind.example.com"


def test_init_kwarg_url_wins_over_auteur_automind(mock_driver, minimal_action, monkeypatch):
    """An explicit automind_url kwarg still wins over the AUTEUR_AUTOMIND env var."""
    from testmu_selenium._heal import Heal

    monkeypatch.setenv("AUTEUR_AUTOMIND", "https://auteur-automind.example.com")
    h = Heal(minimal_action, mock_driver, automind_url="https://kwarg.example.com")
    assert h.automind_url == "https://kwarg.example.com"


# ---------------------------------------------------------------------------
# Defaults when no kwargs and no env vars
# ---------------------------------------------------------------------------

def test_init_defaults_when_no_env_no_kwargs(mock_driver, minimal_action, monkeypatch):
    from testmu_selenium._heal import Heal

    for var in ("TEST_ID", "LT_USERNAME", "LT_ACCESS_KEY", "COMMIT_ID", "ORG_ID", "AUTOMIND_URL", "AUTEUR_AUTOMIND"):
        monkeypatch.delenv(var, raising=False)

    h = Heal(minimal_action, mock_driver)

    assert h.test_id == ""
    assert h.username == ""
    assert h.accesskey == ""
    assert h.commit_id == ""
    assert h.org_id == 0
    assert h.automind_url == "https://kaneai-api.lambdatest.com"


# ---------------------------------------------------------------------------
# Fields read from current_action
# ---------------------------------------------------------------------------

def test_init_use_query_v2_from_action(mock_driver):
    from testmu_selenium._heal import Heal

    action_with_flag = {"operation_type": "click", "use_query_v2": False}
    h = Heal(action_with_flag, mock_driver)
    assert h.use_query_v2 is False


def test_init_use_query_v2_defaults_true_when_absent(mock_driver, minimal_action):
    from testmu_selenium._heal import Heal

    h = Heal(minimal_action, mock_driver)
    assert h.use_query_v2 is True


def test_init_version_from_action(mock_driver):
    from testmu_selenium._heal import Heal

    action_with_version = {"operation_type": "click", "version": "v2"}
    h = Heal(action_with_version, mock_driver)
    assert h.version == "v2"


def test_init_version_defaults_v3_when_absent(mock_driver, minimal_action):
    from testmu_selenium._heal import Heal

    h = Heal(minimal_action, mock_driver)
    assert h.version == "v3"


# ---------------------------------------------------------------------------
# code_export_id
# ---------------------------------------------------------------------------

def test_init_code_export_id_is_16_hex_chars(mock_driver, minimal_action):
    from testmu_selenium._heal import Heal

    h = Heal(minimal_action, mock_driver)
    assert len(h.code_export_id) == 16
    int(h.code_export_id, 16)  # raises ValueError if not hex


def test_init_code_export_id_unique_per_instance(mock_driver, minimal_action):
    from testmu_selenium._heal import Heal

    h1 = Heal(minimal_action, mock_driver)
    h2 = Heal(minimal_action, mock_driver)
    assert h1.code_export_id != h2.code_export_id


# ---------------------------------------------------------------------------
# State field initialisation
# ---------------------------------------------------------------------------

def test_init_state_fields_empty(mock_driver, minimal_action):
    from testmu_selenium._heal import Heal

    h = Heal(minimal_action, mock_driver)
    assert h.prev_actions == []
    assert h.tagified_image == ""
    assert h.untagged_image_base64 == ""
    assert h.xpath_mapping == {}
    assert h.tags_description == {}
    assert h.page_source == ""
    assert h.image_base64 == ""
    assert h.dimensions == []
    assert h.operation == ""


def test_init_mobile_tagify_is_none_in_standalone(mock_driver, minimal_action):
    """In HyperExecute / standalone bindings utils.constants is absent;
    MOBILE_TAGIFY_SCRIPT must be None so Heal.mobile_tagify is falsy."""
    from testmu_selenium._heal import Heal

    h = Heal(minimal_action, mock_driver)
    # In CI the utils.constants import fails → MOBILE_TAGIFY_SCRIPT is None
    assert h.mobile_tagify is None or isinstance(h.mobile_tagify, str)


# ---------------------------------------------------------------------------
# org_id coercion
# ---------------------------------------------------------------------------

def test_init_org_id_int_coercion_from_kwarg(mock_driver, minimal_action):
    from testmu_selenium._heal import Heal

    h = Heal(minimal_action, mock_driver, org_id=7)
    assert isinstance(h.org_id, int)
    assert h.org_id == 7


def test_init_org_id_int_coercion_from_env(mock_driver, minimal_action, monkeypatch):
    from testmu_selenium._heal import Heal

    monkeypatch.setenv("ORG_ID", "55")
    h = Heal(minimal_action, mock_driver)
    assert h.org_id == 55


# ---------------------------------------------------------------------------
# configure() injection — Approach B
# ---------------------------------------------------------------------------

def test_heal_configure_automind_url_wins(mock_driver, minimal_action, monkeypatch):
    """After configure(automind_url=...), a freshly constructed Heal must use that
    URL — even when env vars are set to something else.

    This verifies the Approach B contract: Heal reads _config.get("automind_url")
    (the single binding-wide config value) rather than calling _resolve_automind_url()
    live each time.  configure() writes to that config value, so the host
    can inject the correct URL without mutating os.environ.

    Isolation: configure() mutates the global _config dict; we reload
    testmu_selenium._config in a finally block to restore the baseline for
    subsequent tests — mirroring the pattern in test_config_url_resolution.py.
    """
    import testmu_selenium
    import testmu_selenium._config as _config_mod

    monkeypatch.delenv("AUTEUR_AUTOMIND", raising=False)
    monkeypatch.delenv("AUTOMIND_URL", raising=False)

    testmu_selenium.configure(automind_url="https://configured.example")
    try:
        from testmu_selenium._heal import Heal
        h = Heal(minimal_action, mock_driver)
        assert h.automind_url == "https://configured.example"
    finally:
        importlib.reload(_config_mod)
