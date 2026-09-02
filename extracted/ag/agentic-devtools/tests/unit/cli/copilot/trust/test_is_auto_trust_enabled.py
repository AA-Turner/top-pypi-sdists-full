"""Tests for is_auto_trust_enabled."""

import agentic_devtools.cli.config.project_config as project_config
from agentic_devtools.cli.copilot.trust import is_auto_trust_enabled


def _boom(_key):
    raise RuntimeError("project config unavailable")


class TestIsAutoTrustEnabled:
    """Tests for is_auto_trust_enabled."""

    def test_kill_switch_zero_disables(self, monkeypatch):
        """AGDT_AUTO_TRUST_COPILOT=0 disables seeding."""
        monkeypatch.setenv("AGDT_AUTO_TRUST_COPILOT", "0")
        assert is_auto_trust_enabled() is False

    def test_kill_switch_word_disables(self, monkeypatch):
        """A falsy word in the env var disables seeding (case-insensitive)."""
        monkeypatch.setenv("AGDT_AUTO_TRUST_COPILOT", "FALSE")
        assert is_auto_trust_enabled() is False

    def test_project_config_error_defaults_true(self, monkeypatch):
        """A project-config read error defaults to enabled."""
        monkeypatch.delenv("AGDT_AUTO_TRUST_COPILOT", raising=False)
        monkeypatch.setattr(project_config, "get_effective_project_config_value", _boom)
        assert is_auto_trust_enabled() is True

    def test_flag_absent_defaults_true(self, monkeypatch):
        """An absent project flag defaults to enabled."""
        monkeypatch.delenv("AGDT_AUTO_TRUST_COPILOT", raising=False)
        monkeypatch.setattr(project_config, "get_effective_project_config_value", lambda _k: None)
        assert is_auto_trust_enabled() is True

    def test_flag_false_disables(self, monkeypatch):
        """A falsy project flag disables seeding."""
        monkeypatch.delenv("AGDT_AUTO_TRUST_COPILOT", raising=False)
        monkeypatch.setattr(project_config, "get_effective_project_config_value", lambda _k: "false")
        assert is_auto_trust_enabled() is False

    def test_flag_true_enables(self, monkeypatch):
        """A truthy project flag enables seeding."""
        monkeypatch.delenv("AGDT_AUTO_TRUST_COPILOT", raising=False)
        monkeypatch.setattr(project_config, "get_effective_project_config_value", lambda _k: "true")
        assert is_auto_trust_enabled() is True
