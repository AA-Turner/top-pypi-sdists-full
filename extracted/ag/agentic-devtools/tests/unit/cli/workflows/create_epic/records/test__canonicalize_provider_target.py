import pytest

from agentic_devtools.cli.workflows.create_epic.records import _canonicalize_provider_target


def test_canonicalize_provider_target_preserves_unknown_provider_targets():
    assert _canonicalize_provider_target("custom", " target ") == "target"


def test_canonicalize_provider_target_rejects_invalid_jira_url():
    with pytest.raises(ValueError, match="HTTP"):
        _canonicalize_provider_target("jira", "jira.example.com")


@pytest.mark.parametrize(
    "target",
    [
        "https://account@jira.example.com/PROJ",
        "https://jira.example.com/PROJ?filter=recent",
        "https://jira.example.com/PROJ#details",
    ],
)
def test_canonicalize_provider_target_rejects_jira_userinfo_query_and_fragment(target):
    with pytest.raises(ValueError, match="userinfo, query, or fragment"):
        _canonicalize_provider_target("jira", target)


def test_canonicalize_provider_target_rejects_invalid_jira_port():
    with pytest.raises(ValueError, match="valid port"):
        _canonicalize_provider_target("jira", "https://jira.example.com:invalid")


def test_canonicalize_provider_target_normalizes_jira_ipv6_and_port():
    assert _canonicalize_provider_target("jira", "HTTP://[2001:DB8::1]:8080/PROJ") == "http://[2001:db8::1]:8080/PROJ"


def test_canonicalize_provider_target_rejects_jira_url_missing_project_key():
    with pytest.raises(ValueError, match="project-key path segment"):
        _canonicalize_provider_target("jira", "https://jira.example.com")


def test_canonicalize_provider_target_preserves_context_path_segments():
    # Only the final path segment is the project key; any preceding segments
    # (e.g. a Jira context path) are preserved as part of the canonical target.
    assert (
        _canonicalize_provider_target("jira", "https://jira.example.com/JIRA/PROJ")
        == "https://jira.example.com/JIRA/PROJ"
    )


def test_canonicalize_provider_target_preserves_internal_context_path_slashes():
    assert (
        _canonicalize_provider_target("jira", "https://jira.example.com/team//jira/PROJ")
        == "https://jira.example.com/team//jira/PROJ"
    )


def test_canonicalize_provider_target_casefolds_jira_project_key():
    assert _canonicalize_provider_target("jira", "https://jira.example.com/PROJ") == ("https://jira.example.com/PROJ")
    assert _canonicalize_provider_target("jira", "https://JIRA.Example.com/proj") == ("https://jira.example.com/PROJ")
