"""
Shared fixtures for all unit tests.
"""

from unittest.mock import patch

import pytest

from tests.helpers import make_mock_popen


@pytest.fixture
def mock_background_and_state(tmp_path):
    """Mock both background task infrastructure and state."""
    with patch("agentic_devtools.state.get_state_dir", return_value=tmp_path):
        with patch("agentic_devtools.task_state.get_state_dir", return_value=tmp_path):
            with patch("agentic_devtools.background_tasks.subprocess.Popen") as mock_popen:
                mock_popen.return_value = make_mock_popen()
                yield {
                    "state_dir": tmp_path,
                    "mock_popen": mock_popen,
                }
