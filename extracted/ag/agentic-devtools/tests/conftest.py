"""
Pytest configuration and fixtures for agentic_devtools tests.

Defines platform-specific markers for conditional test execution:
- @pytest.mark.windows_only: Tests that only run on Windows (msvcrt file locking)
- @pytest.mark.linux_only: Tests that only run on Linux/Unix (fcntl file locking)
"""

import importlib.util
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools import state

try:
    from agentic_devtools.git_env import sanitize_git_environment
except ModuleNotFoundError as exc:
    if exc.name != "agentic_devtools.git_env":
        raise
    git_env_path = Path(__file__).parent.parent / "agentic_devtools" / "git_env.py"
    git_env_spec = importlib.util.spec_from_file_location("agentic_devtools.git_env", git_env_path)
    if git_env_spec is None or git_env_spec.loader is None:
        raise ImportError(f"Could not load Git environment helper from {git_env_path!s}") from exc
    git_env_module = importlib.util.module_from_spec(git_env_spec)
    sys.modules[git_env_spec.name] = git_env_module
    git_env_spec.loader.exec_module(git_env_module)
    sanitize_git_environment = git_env_module.sanitize_git_environment


@pytest.fixture(autouse=True)
def isolate_git_environment(monkeypatch):
    """Keep hook routing and config overrides out of every test, restoring them afterward."""
    for key in os.environ.keys() - sanitize_git_environment(os.environ).keys():
        monkeypatch.delenv(key)


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "windows_only: mark test to run only on Windows")
    config.addinivalue_line("markers", "linux_only: mark test to run only on Linux/Unix")
    config.addinivalue_line("markers", "real_vpn: mark test to use real VPN (skips mock_jira_vpn_context fixture)")


def pytest_collection_modifyitems(config, items):
    """Skip tests based on platform markers."""
    is_windows = sys.platform == "win32"

    skip_windows = pytest.mark.skip(reason="Test only runs on Windows")
    skip_linux = pytest.mark.skip(reason="Test only runs on Linux/Unix")

    for item in items:
        if "windows_only" in item.keywords and not is_windows:
            item.add_marker(skip_windows)
        elif "linux_only" in item.keywords and is_windows:
            item.add_marker(skip_linux)


@pytest.fixture
def isolated_test_runtime(tmp_path, monkeypatch, isolate_git_environment):
    """Contain cwd- and Git-root-based runtime writes without disabling writers."""
    root = tmp_path / "runtime"
    root.mkdir()
    (root / ".agdt").mkdir()
    # Clear inherited Git routing variables before the first Git command so cwd=root,
    # not an inherited checkout, decides where sandbox Git state is written.
    for key in os.environ.keys() - sanitize_git_environment(os.environ).keys():
        monkeypatch.delenv(key, raising=False)
    for args in (
        ["init"],
        ["config", "--local", "user.name", "Isolation Test"],
        ["config", "--local", "user.email", "isolation@example.com"],
    ):
        subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)
    # Register AGENTIC_DEVTOOLS_STATE_DIR's original state even when it starts absent, so a
    # direct os.environ assignment by code under test is removed when the fixture tears down.
    monkeypatch.setenv("AGENTIC_DEVTOOLS_STATE_DIR", os.environ.get("AGENTIC_DEVTOOLS_STATE_DIR", ""))
    monkeypatch.delenv("AGENTIC_DEVTOOLS_STATE_DIR")
    monkeypatch.chdir(root)
    return root


@pytest.fixture
def temp_state_dir(tmp_path, isolated_test_runtime):
    """Create a temporary directory for state files."""
    with patch.object(state, "get_state_dir", return_value=tmp_path):
        yield tmp_path


@pytest.fixture
def clear_state_before(temp_state_dir):
    """Clear state before each test."""
    state.clear_state()
    yield


@pytest.fixture(autouse=True)
def mock_jira_vpn_context(request):
    """
    Auto-mock the JiraVpnContext to prevent real VPN operations during tests.

    This fixture automatically mocks the VPN context manager used by Jira commands
    to ensure no real VPN connect/disconnect operations happen during test runs.

    To test real VPN functionality, mark the test with @pytest.mark.real_vpn:
        @pytest.mark.real_vpn
        def test_with_real_vpn():
            ...
    """
    # Skip mocking for tests that need real VPN behavior
    if "real_vpn" in request.keywords:
        yield
        return

    # Skip mocking for VPN-specific tests that test the VPN module itself
    from pathlib import Path

    test_path = str(request.fspath)
    test_path_parts = Path(request.fspath).parts
    if "test_vpn_toggle" in test_path or "test_vpn_wrapper" in test_path or "vpn_wrapper" in test_path_parts:
        yield
        return

    # Create a mock context manager that does nothing
    mock_context = MagicMock()
    mock_context.__enter__ = MagicMock(return_value=mock_context)
    mock_context.__exit__ = MagicMock(return_value=False)
    mock_context.on_corporate_network = True  # Simulate being on corporate network
    mock_context.vpn_was_off = False
    mock_context.connected_vpn = False

    # Patch the JiraVpnContext class in the vpn_toggle module (where it's defined)
    # This works because vpn_wrapper imports it dynamically from vpn_toggle
    with patch(
        "agentic_devtools.cli.azure_devops.vpn_toggle.JiraVpnContext",
        return_value=mock_context,
    ):
        with patch(
            "agentic_devtools.cli.azure_devops.vpn_toggle.get_vpn_url_from_state",
            return_value="https://mock.vpn",
        ):
            yield mock_context
