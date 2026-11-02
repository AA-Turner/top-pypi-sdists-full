"""Tests for HierarchyValidationError exception."""

import pytest

from agentic_devtools.cli.speckit.hierarchy import HierarchyValidationError


class TestHierarchyValidationError:
    """Tests for HierarchyValidationError exception."""

    def test_inherits_from_valueerror(self):
        """Test that HierarchyValidationError is a ValueError."""
        assert issubclass(HierarchyValidationError, ValueError)

    def test_stores_field_name(self):
        """Test that field_name attribute is stored."""
        err = HierarchyValidationError("level", "invalid value")
        assert err.field_name == "level"

    def test_stores_detail(self):
        """Test that detail attribute is stored."""
        err = HierarchyValidationError("title", "must not be empty")
        assert err.detail == "must not be empty"

    def test_message_format(self):
        """Test that str representation includes field and detail."""
        err = HierarchyValidationError("children", "must be a list")
        assert "children" in str(err)
        assert "must be a list" in str(err)

    def test_catchable_as_valueerror(self):
        """Test that it can be caught as ValueError."""
        with pytest.raises(ValueError):
            raise HierarchyValidationError("x", "y")
