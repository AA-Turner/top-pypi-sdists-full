"""Tests for the cache command."""

import re
import tempfile
from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from runlayer_cli.main import app

runner = CliRunner()


def strip_ansi(text: str) -> str:
    """Strip ANSI escape codes from text."""
    ansi_escape = re.compile(r"\x1b\[[0-9;]*m")
    return ansi_escape.sub("", text)


def test_cache_help():
    """Test that cache help shows usage information."""
    result = runner.invoke(app, ["cache", "--help"])
    assert result.exit_code == 0
    plain_output = strip_ansi(result.stdout)
    assert "Manage Runlayer CLI OAuth client cache" in plain_output
    assert "clear" in plain_output


def test_cache_clear_help():
    """Test that cache clear help shows usage information."""
    result = runner.invoke(app, ["cache", "clear", "--help"])
    assert result.exit_code == 0
    plain_output = strip_ansi(result.stdout)
    assert "Remove the OAuth client cache directory" in plain_output


def test_cache_clear_removes_directory():
    """Test that cache clear removes the cache directory when it exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_dir = Path(tmpdir) / "oauth-mcp-client-cache"
        cache_dir.mkdir()
        # Create a test file in the cache directory
        (cache_dir / "test_file.json").write_text("{}")

        with patch(
            "runlayer_cli.commands.cache.default_cache_dir", return_value=cache_dir
        ):
            result = runner.invoke(app, ["cache", "clear"])

        assert result.exit_code == 0
        assert "Removed cache directory" in result.stdout
        assert not cache_dir.exists()


def test_cache_clear_handles_missing_directory():
    """Test that cache clear handles non-existent directory gracefully."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_dir = Path(tmpdir) / "oauth-mcp-client-cache"
        # Don't create the directory

        with patch(
            "runlayer_cli.commands.cache.default_cache_dir", return_value=cache_dir
        ):
            result = runner.invoke(app, ["cache", "clear"])

        assert result.exit_code == 0
        assert "nothing to clear" in result.stdout
