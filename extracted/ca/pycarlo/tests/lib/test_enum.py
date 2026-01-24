"""
Tests for pycarlo.lib.types.Enum - the backward-compatible GraphQL enum type.
"""

import logging
from unittest import TestCase

import sgqlc.types

from pycarlo.lib.types import Enum


class TestForgivingEnum(TestCase):
    """Test the custom Enum class that gracefully handles unknown values."""

    def setUp(self):
        """Create a test enum for each test."""

        # Create a fresh enum class for each test to avoid state pollution
        class TestEnum(Enum):
            __schema__ = sgqlc.types.Schema()
            __choices__ = ("RED", "GREEN", "BLUE")

        self.TestEnum = TestEnum

    def test_known_value_returns_string(self):
        """Known enum values should be returned as strings."""
        result = self.TestEnum("RED")
        self.assertEqual(result, "RED")
        self.assertIsInstance(result, str)

    def test_known_value_equals_class_attribute(self):
        """Known values should equal the class attribute."""
        result = self.TestEnum("GREEN")
        self.assertEqual(result, self.TestEnum.GREEN)  # type: ignore
        self.assertEqual(result, "GREEN")

    def test_unknown_value_returns_string(self):
        """Unknown enum values should be returned as strings without crashing."""
        result = self.TestEnum("YELLOW")
        self.assertEqual(result, "YELLOW")
        self.assertIsInstance(result, str)

    def test_unknown_value_logs_warning(self):
        """Unknown enum values should log a warning."""
        with self.assertLogs("pycarlo.lib.types", level=logging.WARNING) as log:
            self.TestEnum("YELLOW")

        self.assertEqual(len(log.records), 1)
        self.assertIn("Unknown enum value 'YELLOW'", log.records[0].message)
        self.assertIn("TestEnum", log.records[0].message)

    def test_none_value_returns_none(self):
        """None values should return None (same as sgqlc.types.Enum)."""
        result = self.TestEnum(None)
        self.assertIsNone(result)

    def test_known_value_in_enum(self):
        """The 'in' operator should work for known values."""
        self.assertIn("RED", self.TestEnum)
        self.assertIn("GREEN", self.TestEnum)
        self.assertIn("BLUE", self.TestEnum)

    def test_unknown_value_not_in_enum(self):
        """The 'in' operator should return False for unknown values."""
        self.assertNotIn("YELLOW", self.TestEnum)
        self.assertNotIn("PURPLE", self.TestEnum)

    def test_comparison_with_known_values(self):
        """Comparisons should work correctly with known values."""
        result = self.TestEnum("RED")
        self.assertTrue(result == "RED")
        self.assertTrue(result == self.TestEnum.RED)  # type: ignore
        self.assertFalse(result == "GREEN")
        self.assertFalse(result == self.TestEnum.GREEN)  # type: ignore

    def test_comparison_with_unknown_values(self):
        """Comparisons should work correctly with unknown values."""
        result = self.TestEnum("YELLOW")
        self.assertTrue(result == "YELLOW")
        self.assertFalse(result == "RED")
        self.assertFalse(result == self.TestEnum.RED)  # type: ignore

    def test_use_in_set(self):
        """Enum values should work in sets."""
        values = {self.TestEnum("RED"), self.TestEnum("GREEN"), self.TestEnum("YELLOW")}
        self.assertEqual(len(values), 3)
        self.assertIn("RED", values)
        self.assertIn("GREEN", values)
        self.assertIn("YELLOW", values)

    def test_use_in_dict(self):
        """Enum values should work as dict keys."""
        mapping = {
            self.TestEnum("RED"): "red_value",
            self.TestEnum("YELLOW"): "yellow_value",
        }
        self.assertEqual(mapping["RED"], "red_value")
        self.assertEqual(mapping["YELLOW"], "yellow_value")

    def test_use_in_list_comprehension(self):
        """Enum values should work in list comprehensions and filtering."""
        values = [self.TestEnum("RED"), self.TestEnum("YELLOW"), self.TestEnum("GREEN")]

        # Filter known values
        known = [v for v in values if v in self.TestEnum]
        self.assertEqual(known, ["RED", "GREEN"])

        # Filter unknown values
        unknown = [v for v in values if v not in self.TestEnum]
        self.assertEqual(unknown, ["YELLOW"])

    def test_mixed_known_and_unknown_values(self):
        """Lists with mixed known and unknown values should work correctly."""
        values = [
            self.TestEnum("RED"),
            self.TestEnum("UNKNOWN_1"),
            self.TestEnum("GREEN"),
            self.TestEnum("UNKNOWN_2"),
            self.TestEnum("BLUE"),
        ]

        self.assertEqual(len(values), 5)
        self.assertEqual(values[0], "RED")
        self.assertEqual(values[1], "UNKNOWN_1")
        self.assertEqual(values[2], "GREEN")
        self.assertEqual(values[3], "UNKNOWN_2")
        self.assertEqual(values[4], "BLUE")

    def test_backward_compatibility_scenario(self):
        """
        Simulate the real-world scenario: old SDK receiving new enum values from API.
        This is the core use case we're solving.
        """
        # Simulate API response with a mix of known and unknown entitlements
        api_response = [
            "RED",  # Known
            "NEW_FEATURE_A",  # Unknown - added in newer API version
            "GREEN",  # Known
            "NEW_FEATURE_B",  # Unknown - added in newer API version
            "BLUE",  # Known
        ]

        # Deserialize all values (this would crash with standard sgqlc.types.Enum)
        with self.assertLogs("pycarlo.lib.types", level=logging.WARNING) as log:
            deserialized = [self.TestEnum(v) for v in api_response]

        # All values should be present
        self.assertEqual(len(deserialized), 5)
        self.assertEqual(deserialized, api_response)

        # Should have logged warnings for unknown values
        self.assertEqual(len(log.records), 2)

        # Code can still check for known values
        self.assertIn("RED", deserialized)
        self.assertIn("GREEN", deserialized)
        self.assertIn("BLUE", deserialized)

        # Code can also check for unknown values if needed
        self.assertIn("NEW_FEATURE_A", deserialized)
        self.assertIn("NEW_FEATURE_B", deserialized)

        # Can filter to only known values
        known_only = [v for v in deserialized if v in self.TestEnum]
        self.assertEqual(known_only, ["RED", "GREEN", "BLUE"])
