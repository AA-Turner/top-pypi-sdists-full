import os
from pathlib import Path

import pytest
from traitlets.config import Config


# https://github.com/jupyter-server/pytest-jupyter
pytest_plugins = ["pytest_jupyter.jupyter_server"]


@pytest.fixture()
def jp_server_config():
    """Allows tests to setup their specific configuration values."""
    return Config(
        {
            "ServerApp": {
                "jpserver_extensions": {"ploomber_extension": True},
            }
        }
    )


@pytest.fixture
def tmp_empty(tmp_path):
    """
    Create temporary path using pytest native fixture,
    them move it, yield, and restore the original path
    """

    old = os.getcwd()
    os.chdir(str(tmp_path))
    yield str(Path(tmp_path).resolve())
    os.chdir(old)
