"""Tests for the dedicated skill-sync credential (``SkillSyncOrgApiKey``).

``resolve_skill_sync_secret`` mirrors the MDM org-key resolution, including
the managed-host-match refusal: without a matching managed host, releasing
the key would exfiltrate it to a user-supplied ``--host``.
"""

from __future__ import annotations

from unittest.mock import patch

import pytest

import runlayer_cli.config as config_mod
from runlayer_cli.config import resolve_skill_sync_secret

HOST = "https://tenant.runlayer.com"


@pytest.fixture(autouse=True)
def _no_ambient_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("RUNLAYER_SKILL_SYNC_API_KEY", raising=False)


def _with_managed(managed: dict):
    return patch.object(config_mod, "read_managed_config", return_value=managed)


def test_managed_key_released_for_matching_host():
    with _with_managed({"host": HOST, "skill_sync_org_api_key": "rl_org_sync"}):
        assert resolve_skill_sync_secret(HOST) == "rl_org_sync"


def test_managed_key_released_when_managed_host_needs_normalizing():
    with _with_managed({"host": HOST + "/", "skill_sync_org_api_key": "rl_org_sync"}):
        assert resolve_skill_sync_secret(HOST) == "rl_org_sync"


def test_managed_key_refused_on_host_mismatch():
    """A user-supplied --host must not receive the managed sync key."""
    with _with_managed({"host": HOST, "skill_sync_org_api_key": "rl_org_sync"}):
        assert resolve_skill_sync_secret("https://attacker.example.com") is None


def test_managed_key_refused_without_managed_host():
    with _with_managed({"skill_sync_org_api_key": "rl_org_sync"}):
        assert resolve_skill_sync_secret(HOST) is None


def test_env_fallback_when_no_managed_key(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("RUNLAYER_SKILL_SYNC_API_KEY", "rl_org_env_sync")
    with _with_managed({}):
        assert resolve_skill_sync_secret(HOST) == "rl_org_env_sync"


def test_managed_key_beats_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("RUNLAYER_SKILL_SYNC_API_KEY", "rl_org_env_sync")
    with _with_managed({"host": HOST, "skill_sync_org_api_key": "rl_org_mdm_sync"}):
        assert resolve_skill_sync_secret(HOST) == "rl_org_mdm_sync"


def test_host_mismatch_still_falls_back_to_env(monkeypatch: pytest.MonkeyPatch):
    # The env var is operator-supplied on this device (Linux credentials
    # file), not host-scoped like the managed key.
    monkeypatch.setenv("RUNLAYER_SKILL_SYNC_API_KEY", "rl_org_env_sync")
    with _with_managed({"host": HOST, "skill_sync_org_api_key": "rl_org_mdm_sync"}):
        assert (
            resolve_skill_sync_secret("https://other.example.com") == "rl_org_env_sync"
        )


def test_none_when_no_key_anywhere():
    with _with_managed({}):
        assert resolve_skill_sync_secret(HOST) is None


def test_empty_env_value_treated_as_absent(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("RUNLAYER_SKILL_SYNC_API_KEY", "")
    with _with_managed({}):
        assert resolve_skill_sync_secret(HOST) is None
