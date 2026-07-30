"""Unit tests for the has_<attr> presence case in _populate_attribute.

BUG: a selector-bound textual_query with selected_attribute_name='has_<attr>'
falls through to the ValueError branch because _populate_attribute has no
presence case.

Producer emits the raw HTML attribute name after 'has_' (e.g.
'has_aria-expanded' → check 'aria-expanded'; 'has_controls' → check
'controls'), so no underscore→hyphen conversion is needed in the handler.

Each test calls _populate_attribute directly to isolate the fix from the
findElement / SmartWait path.
"""
import unittest
from unittest.mock import MagicMock

from testmu_selenium._helpers.textual_query import _populate_attribute


def _element(present_attrs: dict):
    """Minimal element mock whose get_attribute honours HTML attribute presence."""
    el = MagicMock()
    el.tag_name = "div"
    # Return None for absent keys — mirrors Selenium's get_attribute behaviour.
    el.get_attribute.side_effect = lambda key: present_attrs.get(key)
    return el


class HasAttrPresenceTests(unittest.TestCase):
    """_populate_attribute('has_<attr>') returns bool, never raises ValueError."""

    def test_attr_present_returns_true(self):
        """has_href on element with href attribute → True (not ValueError)."""
        el = _element({"href": "https://example.com"})
        result = _populate_attribute(el, MagicMock(), "has_href")
        self.assertIs(result, True)

    def test_attr_absent_returns_false(self):
        """has_href on element without href attribute → False (not ValueError)."""
        el = _element({})
        result = _populate_attribute(el, MagicMock(), "has_href")
        self.assertIs(result, False)

    def test_return_type_is_bool(self):
        """Result must be a Python bool, not a truthy string or None."""
        el = _element({"disabled": "true"})
        result = _populate_attribute(el, MagicMock(), "has_disabled")
        self.assertIsInstance(result, bool)

    def test_boolean_attribute_present(self):
        """has_controls on video with 'controls' attr (boolean HTML attribute) → True."""
        el = _element({"controls": "true"})
        result = _populate_attribute(el, MagicMock(), "has_controls")
        self.assertIs(result, True)

    def test_boolean_attribute_absent(self):
        """has_controls on element without controls → False."""
        el = _element({})
        result = _populate_attribute(el, MagicMock(), "has_controls")
        self.assertIs(result, False)

    def test_hyphenated_attr_name_preserved(self):
        """has_aria-expanded → check 'aria-expanded' as-is (no conversion).

        The producer emits the raw HTML attr name after 'has_', so hyphens are
        already in the name and must NOT be converted to underscores.
        """
        el = _element({"aria-expanded": "true"})
        result = _populate_attribute(el, MagicMock(), "has_aria-expanded")
        self.assertIs(result, True)

    def test_hyphenated_attr_absent(self):
        """has_aria-expanded on element without aria-expanded → False."""
        el = _element({})
        result = _populate_attribute(el, MagicMock(), "has_aria-expanded")
        self.assertIs(result, False)

    def test_required_attr_present(self):
        """has_required → True when 'required' attribute present."""
        el = _element({"required": "true"})
        result = _populate_attribute(el, MagicMock(), "has_required")
        self.assertIs(result, True)


if __name__ == "__main__":
    unittest.main()
