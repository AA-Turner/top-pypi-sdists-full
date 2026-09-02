"""Tests for legacy_state_present (issue #2117)."""

from unittest.mock import patch

from agentic_devtools.cli import jira
from agentic_devtools.cli.jira.create_epic_router import legacy_state_present


def test_no_state_returns_false(temp_state_dir, clear_state_before):
    assert legacy_state_present() is False


def test_non_dict_root_state_returns_false(temp_state_dir, clear_state_before):
    with patch("agentic_devtools.cli.jira.create_epic_router.load_state", return_value=[]):
        assert legacy_state_present() is False


def test_non_dict_jira_namespace_returns_false(temp_state_dir, clear_state_before):
    from agentic_devtools.state import set_value

    set_value("jira", "not-a-dict")
    assert legacy_state_present() is False


def test_any_legacy_key_present_returns_true(temp_state_dir, clear_state_before):
    jira.set_jira_value("project_key", "PROJECT")
    assert legacy_state_present() is True


def test_empty_value_still_present(temp_state_dir, clear_state_before):
    jira.set_jira_value("labels", "")
    assert legacy_state_present() is True


def test_unrelated_jira_key_not_legacy(temp_state_dir, clear_state_before):
    jira.set_jira_value("issue_key", "PROJECT-1")
    assert legacy_state_present() is False
