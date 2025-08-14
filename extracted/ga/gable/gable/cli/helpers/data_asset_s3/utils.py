"""
Utility functions for the inventory report manager.
"""

import urllib.parse
from datetime import datetime
from typing import Optional


class Utils:
    """Utility functions used across the application"""

    @staticmethod
    def fully_decode(encoded_str: str) -> str:
        """
        Robustly decode a URL-encoded string, handling multiple encoding layers.
        """
        prev = encoded_str
        for _ in range(5):  # up to 5 passes if needed
            decoded = urllib.parse.unquote(prev)
            if decoded == prev:
                break
            prev = decoded
        return prev

    @staticmethod
    def format_timestamp(ts: Optional[str]) -> Optional[str]:
        """Format a timestamp string to a standard format"""
        if not ts:
            return None

        try:
            # Try with milliseconds
            dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            try:
                # Try without milliseconds
                dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
            except Exception:
                return ts

        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")

    @staticmethod
    def parse_timestamp(ts: str) -> datetime:
        """Parse a timestamp string to a datetime object

        Supports multiple formats:
        - ISO format with Z: 2025-05-25T13:00:14.000Z
        - ISO format with timezone: 2025-05-25T13:00:14+00:00
        - UTC format: 2024-07-25 03:01:54 UTC
        - Standard format: 2024-07-25 03:01:54
        - Date only: 2024-07-25
        """
        # Handle ISO format with Z suffix
        if ts.endswith("Z"):
            ts_str = ts[:-1] + "+00:00"
            return datetime.fromisoformat(ts_str)

        # Handle UTC format: "2024-07-25 03:01:54 UTC"
        if ts.endswith(" UTC"):
            ts_str = ts[:-4] + "+00:00"
            return datetime.fromisoformat(ts_str)

        # Handle ISO format with timezone offset
        if "T" in ts or ("+" in ts or "-" in ts[-6:]):
            return datetime.fromisoformat(ts)

        # Handle standard format: "2024-07-25 03:01:54"
        if " " in ts and ":" in ts:
            try:
                return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                # Try with microseconds
                return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f")

        # Handle date only format: "2024-07-25"
        if len(ts) == 10 and ts.count("-") == 2:
            return datetime.strptime(ts, "%Y-%m-%d")

        # Try ISO format without timezone
        try:
            return datetime.fromisoformat(ts)
        except ValueError:
            # Try various other common formats
            formats = [
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%S.%f",
                "%Y/%m/%d %H:%M:%S",
                "%Y/%m/%d %H:%M:%S.%f",
                "%m/%d/%Y %H:%M:%S",
                "%m/%d/%Y %H:%M:%S.%f",
                "%d/%m/%Y %H:%M:%S",
                "%d/%m/%Y %H:%M:%S.%f",
            ]

            for fmt in formats:
                try:
                    return datetime.strptime(ts, fmt)
                except ValueError:
                    continue

            raise ValueError(f"Unable to parse timestamp: {ts}")
