"""Tests for EpicTreeConfig dataclass."""

from agentic_devtools.config import DEFAULT_ISSUE_ADAPTER
from agentic_devtools.epic_tree.config import EpicTreeConfig


class TestEpicTreeConfigProvider:
    """Tests for the provider field on EpicTreeConfig."""

    def test_provider_defaults_to_default_issue_adapter(self):
        """Provider field defaults to DEFAULT_ISSUE_ADAPTER."""
        config = EpicTreeConfig()
        assert config.provider == DEFAULT_ISSUE_ADAPTER

    def test_provider_can_be_set_explicitly(self):
        """Provider field can be set explicitly at construction."""
        config = EpicTreeConfig(provider="github")
        assert config.provider == "github"

    def test_provider_is_frozen(self):
        """Provider field cannot be modified after construction."""
        config = EpicTreeConfig(provider="github")
        import pytest

        with pytest.raises(AttributeError):
            config.provider = "jira"  # type: ignore[misc]
