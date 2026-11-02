import os
import sys
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.ai_providers.copilot_discovery import user_config_dir


def test_uses_xdg_config_home_when_set(tmp_path: Path) -> None:
    with patch.object(sys, "platform", "linux"):
        with patch.dict(os.environ, {"XDG_CONFIG_HOME": str(tmp_path)}, clear=False):
            assert user_config_dir() == tmp_path


def test_expands_user_in_xdg_config_home(tmp_path: Path) -> None:
    with patch.object(sys, "platform", "linux"):
        with patch.dict(os.environ, {"XDG_CONFIG_HOME": "~/agdt-config"}, clear=False):
            assert user_config_dir() == Path.home() / "agdt-config"


def test_ignores_relative_xdg_config_home() -> None:
    with patch.object(sys, "platform", "linux"):
        with patch.dict(os.environ, {"XDG_CONFIG_HOME": "relative-config"}, clear=False):
            assert user_config_dir() == Path.home() / ".config"


def test_falls_back_to_dot_config_when_xdg_is_unset() -> None:
    with patch.object(sys, "platform", "linux"):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("XDG_CONFIG_HOME", None)

            assert user_config_dir() == Path.home() / ".config"
