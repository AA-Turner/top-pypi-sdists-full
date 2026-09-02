"""Tests for ConfigError exception class."""

from agentic_devtools.epic_tree.errors import ConfigError


class TestConfigError:
    """Tests for ConfigError exception."""

    def test_attributes(self):
        """ConfigError stores config_path and field."""
        err = ConfigError("/path/to/config.json", "epicTree.maxDepth", "must be <= 3")
        assert err.config_path == "/path/to/config.json"
        assert err.field == "epicTree.maxDepth"

    def test_message_format(self):
        """ConfigError message includes path, field, and reason."""
        err = ConfigError("/path/config.json", "epicTree.maxDepth", "must be <= 3")
        msg = str(err)
        assert "/path/config.json" in msg
        assert "epicTree.maxDepth" in msg
        assert "must be <= 3" in msg

    def test_is_exception(self):
        """ConfigError is an Exception subclass."""
        err = ConfigError("file.json", "field", "msg")
        assert isinstance(err, Exception)
