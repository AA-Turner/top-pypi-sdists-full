import pytest

from agentic_devtools.cli.workflows.create_epic.records import _canonicalize_provider_target


def test_canonicalize_provider_target_preserves_unknown_provider_targets():
    assert _canonicalize_provider_target("custom", " target ") == "target"


def test_canonicalize_provider_target_rejects_invalid_jira_url():
    with pytest.raises(ValueError, match="HTTP"):
        _canonicalize_provider_target("jira", "jira.example.com")


def test_canonicalize_provider_target_rejects_invalid_jira_port():
    with pytest.raises(ValueError, match="valid port"):
        _canonicalize_provider_target("jira", "https://jira.example.com:invalid")


def test_canonicalize_provider_target_normalizes_jira_ipv6_and_port():
    assert _canonicalize_provider_target("jira", "HTTP://[2001:DB8::1]:8080/") == "http://[2001:db8::1]:8080"
