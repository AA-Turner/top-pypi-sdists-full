from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def use_posix_command_quoting():
    """These expectations exercise generated Bash commands."""
    with patch("agentic_devtools.cli.workflows.worktree_setup_helpers.platform.system", return_value="Linux"):
        yield
