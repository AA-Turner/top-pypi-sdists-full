"""Tests for invalid config_mode rejection at resolution time."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.config.project_config import (
    get_effective_project_config_value,
    load_effective_project_config,
)


class TestInvalidConfigModeRejection:
    """Tests that invalid config_mode raises ValueError at resolution time."""

    def test_load_effective_raises_on_invalid_mode(self) -> None:
        """load_effective_project_config raises ValueError for invalid mode."""
        with patch(
            "agentic_devtools.state.get_value",
            return_value="bogus",
        ):
            with pytest.raises(ValueError, match="Invalid config_mode"):
                load_effective_project_config()

    def test_get_effective_value_raises_on_invalid_mode(self) -> None:
        """get_effective_project_config_value raises ValueError for invalid mode."""
        with patch(
            "agentic_devtools.state.get_value",
            return_value="bogus",
        ):
            with pytest.raises(ValueError, match="Invalid config_mode"):
                get_effective_project_config_value("some_key")
