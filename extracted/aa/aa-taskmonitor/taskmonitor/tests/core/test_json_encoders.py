import json
import unittest
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from taskmonitor.core.json_encoders import UniversalJSONEncoder


class TestUniversalJSONEncoder(unittest.TestCase):
    def setUp(self):
        """Helper to run json.dumps with our encoder."""
        self.encode = lambda obj: json.dumps(obj, cls=UniversalJSONEncoder)

    def test_standard_types(self):
        """Ensure standard types still encode correctly."""
        data = {"string": "hello", "number": 42, "boolean": True, "none": None}
        expected = '{"string": "hello", "number": 42, "boolean": true, "none": null}'
        self.assertEqual(self.encode(data), expected)

    def test_datetime_and_date(self):
        """Ensure datetime and date objects convert to ISO format strings."""
        dt = datetime(2026, 6, 30, 12, 0, 0)
        d = date(2026, 6, 30)

        self.assertEqual(self.encode(dt), '"2026-06-30T12:00:00"')
        self.assertEqual(self.encode(d), '"2026-06-30"')

    def test_sets_and_frozensets(self):
        """Ensure sets and frozensets are converted to lists."""
        # We test single-item sets because set ordering in JSON strings can be unpredictable
        regular_set = {"apple"}
        frozen_set = frozenset(["orange"])

        self.assertEqual(self.encode(regular_set), '["apple"]')
        self.assertEqual(self.encode(frozen_set), '["orange"]')

    def test_custom_class_instances(self):
        """Ensure custom classes are serialized via their __dict__."""

        class MockUser:
            def __init__(self, username, active):
                self.username = username
                self.active = active

        user = MockUser("dev_user", True)
        expected = '{"username": "dev_user", "active": true}'
        self.assertEqual(self.encode(user), expected)

    def test_decimal_and_uuid(self):
        """Ensure Decimals become floats and UUIDs become strings."""
        dec = Decimal("45.67")
        uid = UUID("9f8e7d6c-5b4a-3f2e-1d0c-9b8a7f6e5d4c")

        self.assertEqual(self.encode(dec), '"45.67"')
        self.assertEqual(self.encode(uid), '"9f8e7d6c-5b4a-3f2e-1d0c-9b8a7f6e5d4c"')

    def test_fallback_to_string(self):
        """Ensure completely unhandled types safely fall back to their string representation."""

        def mock_function():
            pass

        result = self.encode(mock_function)

        # It should wrap the function's string representation in valid JSON quotes
        self.assertIn(
            "<function TestUniversalJSONEncoder.test_fallback_to_string.<locals>.mock_function",
            result,
        )
        self.assertTrue(result.startswith('"'))
        self.assertTrue(result.endswith('"'))
