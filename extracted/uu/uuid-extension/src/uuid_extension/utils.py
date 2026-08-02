"""
Utility functions for the uuid-extension package.

This module provides helper functions for timestamp manipulation and other
utility operations used by the uuid-extension package.
"""

from __future__ import annotations

from datetime import datetime
from time import time
from typing import Union


def generate_unix_ts_in_ms(
    timestamp: Union[float, datetime, None] = None,
) -> int:
    """
    Generate a Unix timestamp in milliseconds (48-bit compatible).

    Converts the provided timestamp to milliseconds since Unix epoch.
    If no timestamp is provided, uses the current time.
    Ensures the timestamp fits within a 48-bit integer.

    Args:
        timestamp: The timestamp to convert. Can be:
            - float/int: Seconds since Unix epoch
            - datetime: Python datetime object
            - None: Current time will be used

    Returns:
        int: Unix timestamp in milliseconds, masked to 48 bits

    Raises:
        # TypeError: If the provided timestamp is of an unsupported type

    Examples:
        >>> generate_unix_ts_in_ms()  # Current time
        1621234567890
        >>> generate_unix_ts_in_ms(1621234567.89)  # From seconds
        1621234567890
        >>> from datetime import datetime
        >>> dt = datetime(2021, 5, 17, 12, 34, 56)
        >>> generate_unix_ts_in_ms(dt)
        1621255696000
    """
    # Get current Unix timestamp in milliseconds (48 bits)
    if timestamp is None:
        return int(time() * 1000) & 0xFFFFFFFFFFFF

    # Convert numeric timestamp (seconds) to milliseconds
    if isinstance(timestamp, (float, int)):
        return int(timestamp * 1000) & 0xFFFFFFFFFFFF

    # Convert datetime to milliseconds
    if isinstance(timestamp, datetime):
        return int(timestamp.timestamp() * 1000) & 0xFFFFFFFFFFFF

    msg = f"Unsupported timestamp type: {type(timestamp).__name__}"
    raise TypeError(msg)
