from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def use_posix_platform_for_platform_neutral_tests():
    """Keep mocked subprocess calls from affecting platform detection."""
    with patch("agentic_devtools.cli.workflows.worktree_auto_start_ui.platform.system", return_value="Linux"):
        yield
