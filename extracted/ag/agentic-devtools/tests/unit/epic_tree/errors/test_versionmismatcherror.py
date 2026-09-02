"""Tests for VersionMismatchError exception."""

import pytest

from agentic_devtools.epic_tree.errors import VersionMismatchError


class TestVersionMismatchError:
    """Tests for the VersionMismatchError exception."""

    def test_is_exception(self):
        """VersionMismatchError is an Exception subclass."""
        assert issubclass(VersionMismatchError, Exception)

    def test_attributes(self):
        """Error stores found_version and supported_major."""
        error = VersionMismatchError("2.0.0", 1)
        assert error.found_version == "2.0.0"
        assert error.supported_major == 1

    def test_message_format(self):
        """Error message includes version and supported major."""
        error = VersionMismatchError("2.0.0", 1)
        assert "2.0.0" in str(error)
        assert "1" in str(error)

    def test_can_be_raised_and_caught(self):
        """VersionMismatchError can be raised and caught."""
        with pytest.raises(VersionMismatchError) as exc_info:
            raise VersionMismatchError("3.1.0", 1)
        assert exc_info.value.found_version == "3.1.0"
        assert exc_info.value.supported_major == 1
