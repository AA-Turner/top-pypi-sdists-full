"""Unit tests for resolve_template_path."""

from pathlib import Path
from unittest.mock import patch

import agentic_devtools.cli.setup.provider_configuration as provider_configuration


def test_resolve_template_path_returns_none_when_template_is_missing() -> None:
    with patch.object(Path, "exists", side_effect=[False, False]):
        assert provider_configuration.resolve_template_path() is None


def test_resolve_template_path_returns_packaged_path_when_checkout_is_missing() -> None:
    with patch.object(Path, "exists", side_effect=[False, True]):
        assert provider_configuration.resolve_template_path() is not None
