"""
UUID v7 Implementation.

UUID v7 features:
- Time-ordered (sortable by creation time)
- Better database indexing performance
- Embedded timestamps (millisecond precision)
- Distributed system friendly
- Compliant with RFC 4122 (draft)

Format:
- 48 bits: Unix timestamp (milliseconds)
- 12 bits: Monotonic counter
- 62 bits: Random data
- 6 bits: Version and variant
"""

import re
import secrets
import time
from datetime import datetime


def uuidv7() -> str:
    """
    Generate a UUID v7.

    Returns:
        UUID v7 string in standard format
    """
    # Get current timestamp in milliseconds
    timestamp = int(time.time() * 1000)

    # Generate random bytes
    random_bytes = secrets.token_bytes(10)

    # Build timestamp hex (48 bits = 6 bytes)
    timestamp_hex = f"{timestamp:012x}"

    # Set version (0111 = 7) in the most significant 4 bits
    version_byte = 0x70 | (random_bytes[2] & 0x0F)

    # Set variant (10xx) in the most significant 2 bits
    variant_byte = 0x80 | (random_bytes[3] & 0x3F)

    # Construct UUID string
    return (
        f"{timestamp_hex[:8]}-"
        f"{timestamp_hex[8:12]}-"
        f"{version_byte:02x}{random_bytes[0]:02x}-"
        f"{variant_byte:02x}{random_bytes[1]:02x}-"
        f"{random_bytes[4]:02x}{random_bytes[5]:02x}"
        f"{random_bytes[6]:02x}{random_bytes[7]:02x}"
        f"{random_bytes[8]:02x}{random_bytes[9]:02x}"
    )



def extract_timestamp(uuid: str) -> int | None:
    """
    Extract timestamp from UUID v7.

    Args:
        uuid: UUID v7 string

    Returns:
        Timestamp in milliseconds, or None if invalid
    """
    if not is_valid_uuidv7(uuid):
        return None

    # Remove dashes and extract first 12 hex characters (48 bits)
    hex_str = uuid.replace("-", "")[:12]
    return int(hex_str, 16)


def is_valid_uuidv7(uuid: str) -> bool:
    """
    Validate if a UUID is a valid UUID v7.

    Args:
        uuid: UUID string to validate

    Returns:
        True if valid UUID v7
    """
    # Check format: xxxxxxxx-xxxx-7xxx-yxxx-xxxxxxxxxxxx
    uuidv7_pattern = re.compile(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$", re.IGNORECASE
    )
    return bool(uuidv7_pattern.match(uuid))


def uuidv7_to_datetime(uuid: str) -> datetime | None:
    """
    Convert UUID v7 to datetime object.

    Args:
        uuid: UUID v7 string

    Returns:
        Datetime object, or None if invalid
    """
    timestamp = extract_timestamp(uuid)
    return datetime.fromtimestamp(timestamp / 1000) if timestamp is not None else None


def compare_uuidv7(a: str, b: str) -> int | None:
    """
    Compare two UUID v7s by their timestamps.

    Args:
        a: First UUID v7
        b: Second UUID v7

    Returns:
        -1 if a < b, 0 if a == b, 1 if a > b, None if invalid
    """
    timestamp_a = extract_timestamp(a)
    timestamp_b = extract_timestamp(b)

    if timestamp_a is None or timestamp_b is None:
        return None

    if timestamp_a < timestamp_b:
        return -1
    if timestamp_a > timestamp_b:
        return 1

    # If timestamps are equal, compare full UUIDs lexicographically
    if a < b:
        return -1
    if a > b:
        return 1
    return 0


def generate_batch_uuidv7(count: int) -> list[str]:
    """
    Generate a batch of UUID v7s.

    Ensures monotonic ordering within the same millisecond by
    incrementing the random portion slightly.

    Args:
        count: Number of UUIDs to generate

    Returns:
        List of UUID v7 strings
    """
    uuids = []
    timestamp = int(time.time() * 1000)

    for i in range(count):
        # Add a small increment to ensure ordering
        adjusted_timestamp = timestamp + (i // 1000)
        uuid = uuidv7_with_timestamp(adjusted_timestamp, i % 1000)
        uuids.append(uuid)

    return uuids


def uuidv7_with_timestamp(timestamp: int, counter: int = 0) -> str:
    """
    Generate UUID v7 with a specific timestamp.

    For testing or custom scenarios.

    Args:
        timestamp: Timestamp in milliseconds
        counter: Optional monotonic counter (0-4095)

    Returns:
        UUID v7 string
    """
    # Ensure counter is within 12-bit range
    counter = counter & 0xFFF

    # Generate random bytes
    random_bytes = secrets.token_bytes(8)

    # Build timestamp hex (48 bits)
    timestamp_hex = f"{timestamp:012x}"

    # Build counter hex (12 bits)
    counter_hex = f"{counter:03x}"

    # Set version (0111 = 7)
    version_nibble = "7"

    # Set variant (10xx)
    variant_byte = 0x80 | (random_bytes[0] & 0x3F)

    # Construct UUID string
    return (
        f"{timestamp_hex[:8]}-"
        f"{timestamp_hex[8:12]}-"
        f"{version_nibble}{counter_hex}-"
        f"{variant_byte:02x}{random_bytes[1]:02x}-"
        f"{random_bytes[2]:02x}{random_bytes[3]:02x}"
        f"{random_bytes[4]:02x}{random_bytes[5]:02x}"
        f"{random_bytes[6]:02x}{random_bytes[7]:02x}"
    )



def get_uuidv7_age(uuid: str) -> int | None:
    """
    Get the age of a UUID v7 in milliseconds.

    Args:
        uuid: UUID v7 string

    Returns:
        Age in milliseconds, or None if invalid
    """
    timestamp = extract_timestamp(uuid)
    if timestamp is None:
        return None

    current_timestamp = int(time.time() * 1000)
    return current_timestamp - timestamp
