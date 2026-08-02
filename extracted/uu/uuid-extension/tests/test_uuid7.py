"""
Tests for UUID version 7 implementation.

Verifies conformance to RFC 9562 section 5.7 specification and best practices
from section 6.
"""

import time
import unittest
from datetime import datetime

from uuid_extension import uuid7


class TestUUID7(unittest.TestCase):
    """Test UUID version 7 implementation."""

    def test_uuid7_format(self):
        """Verify UUID7 format matches RFC 9562 section 5.7 field layout."""
        # Generate a UUID7
        u = uuid7()

        # Check UUID version is 7
        self.assertEqual(u.version, 7, "UUID version must be 7")

        # Check variant is RFC variant (0b10xx or 8/9/a/b)
        self.assertTrue(
            2 <= (u.int >> 62) & 0x3 <= 3,
            "UUID variant must be 0b10xx",
        )

        # Binary representation should have bit pattern matching section 5.7
        # - bits 48-51 should be version (0111)
        # - bits 64-65 should be variant (10)
        uuid_bin = bin(u.int)[2:].zfill(128)
        self.assertEqual(uuid_bin[48:52], "0111", "Version bits should be 0111")
        self.assertEqual(uuid_bin[64:66], "10", "Variant bits should be 10")

    def test_timestamp_extraction(self):
        """Verify timestamp extraction works correctly."""
        # Use a fixed timestamp to test
        fixed_ts = (
            1645557742.123  # Tuesday, February 22, 2022 2:22:22.123 PM GMT
        )
        u = uuid7(fixed_ts)

        # Extract timestamp
        extracted_ts = u.to_timestamp()

        # Should be within 1ms due to millisecond precision
        self.assertAlmostEqual(fixed_ts, extracted_ts, delta=0.001)

        # Test with datetime object
        dt = datetime.fromtimestamp(fixed_ts)
        u_dt = uuid7(dt)
        extracted_ts_dt = u_dt.to_timestamp()
        self.assertAlmostEqual(fixed_ts, extracted_ts_dt, delta=0.001)

    def test_datetime_extraction(self):
        """Verify datetime extraction works correctly."""
        # Use a fixed timestamp to test
        fixed_ts = 1645557742.123
        u = uuid7(fixed_ts)

        # Extract datetime
        dt = u.to_datetime()

        # Should be the expected datetime
        expected_dt = datetime.fromtimestamp(fixed_ts)
        self.assertAlmostEqual(
            dt.timestamp(),
            expected_dt.timestamp(),
            delta=0.001,
        )

    def test_time_ordering(self):
        """
        Test that UUIDs are monotonically increasing with time.

        This verifies the primary benefit of UUIDv7 time ordering
        per section 6.11.
        """
        # Generate UUIDs with increasing timestamps
        timestamps = [
            1645557742.000,  # Base time
            1645557742.001,  # +1ms
            1645557742.010,  # +10ms
            1645557742.100,  # +100ms
            1645557743.000,  # +1s
        ]

        uuids = [uuid7(ts) for ts in timestamps]

        # Verify UUIDs are in ascending order
        for i in range(1, len(uuids)):
            self.assertGreater(
                uuids[i],
                uuids[i - 1],
                "UUIDs with increasing timestamps should "
                "sort in ascending order",
            )

    def test_uuid_string_format(self):
        """Test string representation of UUIDs."""
        # Generate UUID string
        uuid_str = str(uuid7())

        # Should match format pattern xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        self.assertRegex(
            uuid_str,
            r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
            "UUID string should match the standard format with version 7",
        )

    def test_uniqueness(self):
        """
        Test basic uniqueness of generated UUIDs.

        While we can't prove true uniqueness in a unit test, we can check
        that a batch of UUIDs generated in sequence are all unique.
        """
        # Generate a batch of UUIDs
        count = 1000
        uuids = [uuid7() for _ in range(count)]

        # Check for uniqueness
        unique_uuids = set(uuids)
        self.assertEqual(
            len(unique_uuids),
            count,
            "Generated UUIDs should all be unique",
        )

    def test_millisecond_timestamp_precision(self):
        """
        Verify timestamp has millisecond precision.

        According to RFC 9562 section 5.7,
        UUIDv7 uses Unix Epoch time in milliseconds.
        """
        # Generate UUIDs with timestamps differing by microseconds
        base_ts = 1645557742.123456
        u1 = uuid7(base_ts)
        u2 = uuid7(base_ts + 0.000001)  # Add 1μs

        # Timestamps should be the same when extracted (millisecond precision)
        ts1 = u1.to_timestamp()
        ts2 = u2.to_timestamp()
        self.assertEqual(
            round(ts1 * 1000),
            round(ts2 * 1000),
            "Timestamps should have millisecond precision",
        )

        # But UUIDs with different milliseconds should have different timestamps
        u3 = uuid7(base_ts + 0.001)  # Add 1ms
        ts3 = u3.to_timestamp()
        self.assertNotEqual(
            round(ts1 * 1000),
            round(ts3 * 1000),
            "UUIDs with different milliseconds "
            "should have different timestamps",
        )

    def test_timestamp_truncation(self):
        """
        Test that timestamps are properly truncated to 48 bits.

        Per section 6.1, when timestamps need to be truncated,
        the lower bits must be used.
        """
        # A timestamp far in the future (beyond 48-bit milliseconds)
        far_future_ts = time.time() + (2**48 / 1000) + 1000
        u = uuid7(far_future_ts)

        # The extracted timestamp should be the truncated value
        extracted_ts = u.to_timestamp()

        # Check that the extracted timestamp is the truncation (mod 2^48)
        expected_ts = far_future_ts % (2**48 / 1000)
        self.assertAlmostEqual(
            extracted_ts % (2**48 / 1000),
            expected_ts,
            delta=0.001,
        )


if __name__ == "__main__":
    unittest.main()
