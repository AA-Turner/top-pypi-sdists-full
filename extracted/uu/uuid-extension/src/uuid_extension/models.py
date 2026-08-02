"""
UUID version 7 implementation as specified in RFC.

This implementation generates UUIDv7 values with:
- 48 bits of Unix timestamp in milliseconds
- 4 bits for version (set to 7)
- 2 bits for variant (set to 0b10)
- 74 bits of random data for uniqueness
"""

from __future__ import annotations

from datetime import datetime
from secrets import randbits
from typing import Union
from uuid import UUID

from .utils import generate_unix_ts_in_ms


class UUID7(UUID):
    """
    Class for generating and working with UUID version 7
    values according to specification.

    UUID version 7 provides time-ordered values with Unix Epoch timestamp in
    milliseconds as the most significant 48 bits, and random data for
    the remaining bits (with proper version and variant bits set).
    """

    def __init__(
        self,
        timestamp: Union[float, datetime, None] = None,
        counter: Union[int, None] = None,
    ) -> None:
        uuid7 = self._generate(timestamp, counter)
        super().__init__(int=uuid7.int)

    def __repr__(self) -> str:
        """
        Return a string representation of the UUID7 object.

        Returns:
            str: The string representation of the UUID7 object
        """
        return f"UUID7('{str(self)}')"

    # -------------------------------------------------------- #
    #                        CONVERSION                        #
    # -------------------------------------------------------- #
    def to_timestamp(self) -> float:
        """
        Extract the timestamp from a UUID version 7.

        Returns:
            float: Unix timestamp in seconds

        Raises:
            ValueError: If the UUID is not version 7
        """
        # Verify this is a version 7 UUID
        if self.version != 7:
            err_msg = f"Expected UUID version 7, got version {self.version}"
            raise ValueError(err_msg)

        # Extract the timestamp from the most significant 48 bits
        # Shift right to get the timestamp bits and mask to 48 bits
        timestamp_ms = (self.int >> 80) & 0xFFFFFFFFFFFF

        # Convert milliseconds to seconds
        return timestamp_ms / 1000.0

    def to_datetime(self, tz=None) -> datetime:
        """
        Extract the datetime from a UUID version 7.

        Args:
            tz: Optional timezone for the returned datetime, default: UTC

        Returns:
            datetime: Datetime object representing the UUID timestamp

        Raises:
            ValueError: If the UUID is not version 7
        """
        # Get the timestamp in seconds
        timestamp = self.to_timestamp()

        # Convert to datetime
        return datetime.fromtimestamp(timestamp, tz=tz)

    # -------------------------------------------------------- #
    #                         INTERNALS                        #
    # -------------------------------------------------------- #
    def _generate(
        self,
        timestamp: Union[float, datetime, None] = None,
        counter: Union[int, None] = None,
    ) -> UUID:
        """
        Generate a UUID version 7 according to the specification.

        Args:
            timestamp: Optional timestamp to use instead of current time.
                     Can be a float/int (unix timestamp in seconds),
                     or datetime object. If None, current time is used.

            counter: Optional counter for monotonicity within milliseconds.
                    If None, random data is used.

        Returns:
            UUID: A version 7 UUID object
        """

        # Get current Unix timestamp in milliseconds (48 bits)
        unix_ts_ms = generate_unix_ts_in_ms(timestamp)

        # Create the initial 64 bits
        # Shift timestamp left by 16 bits to make room for version and rand_a
        time_high = (unix_ts_ms << 16) & 0xFFFFFFFFFFFF0000

        # Set version bits (0b0111 = 7) in the appropriate position
        version = 0x7000  # 0b0111 shifted to the right position

        # If counter is provided, use it for rand_a (12 bits)
        if counter is not None:
            rand_a = counter & 0xFFF  # Use only 12 bits
        else:
            rand_a = randbits(12)

        # Combine timestamp, version and rand_a into the first 64 bits
        # most_significant_bits
        msb = time_high | version | rand_a

        # Generate random bits for rand_b (62 bits)
        # But first, create a 64-bit value with the variant bits (0b10)
        rand_b = randbits(62)

        # least significant bit
        lsb = (0x8000000000000000 | rand_b) & 0xFFFFFFFFFFFFFFFF

        # Combine all bits into a 128-bit integer
        uuid_int = (msb << 64) | lsb

        # Convert to UUID object
        return UUID(int=uuid_int)


def uuid7(
    timestamp: Union[float, datetime, None] = None,
    counter: Union[int, None] = None,
) -> UUID7:
    return UUID7(timestamp, counter)
