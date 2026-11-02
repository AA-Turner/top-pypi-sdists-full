"""Tests for removing inherited Git repository routing."""

import pytest

from agentic_devtools.git_env import sanitize_git_environment


@pytest.mark.parametrize(
    "key",
    [
        "GIT_DIR",
        "GIT_WORK_TREE",
        "GIT_INDEX_FILE",
        "GIT_COMMON_DIR",
        "GIT_OBJECT_DIRECTORY",
        "GIT_ALTERNATE_OBJECT_DIRECTORIES",
        "GIT_NAMESPACE",
        "GIT_PREFIX",
        "GIT_CONFIG",
        "GIT_CONFIG_PARAMETERS",
        "GIT_CONFIG_COUNT",
        "GIT_CONFIG_KEY_0",
        "GIT_CONFIG_VALUE_0",
        "GIT_CONFIG_KEY_123",
        "GIT_CONFIG_VALUE_123",
        "git_dir",
        "git_config_key_0",
    ],
)
def test_removes_routing_without_mutating_input(key):
    original = {key: "unsafe", "PATH": "tools", "GIT_CONFIG_GLOBAL": "global-config", "COVERAGE_CORE": "sysmon"}

    assert sanitize_git_environment(original) == {
        "PATH": "tools",
        "GIT_CONFIG_GLOBAL": "global-config",
        "COVERAGE_CORE": "sysmon",
    }
    assert original[key] == "unsafe"


def test_empty_environment():
    assert sanitize_git_environment({}) == {}
