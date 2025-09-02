"""Data models used for WebSocket payloads in the BlueCurrent API."""

from dataclasses import dataclass
from typing import List


@dataclass
class OverrideCurrentPayload:
    """
    Payload for overriding the charging current on a set of chargepoints.

    Attributes:
        chargepoints (List[str]): List of chargepoint IDs to apply the override to.
        overridestarttime (str): Start time in HH24:MI format.
        overridestartdays (List[str]): Start days using 2-letter weekday codes (e.g., 'MO', 'TU').
        overridestoptime (str): Stop time in HH24:MI format.
        overridestopdays (List[str]): Stop days using 2-letter weekday codes.
        overridevalue (float): Amperes to override the chargepoints with.
    """

    chargepoints: List[str]
    overridestarttime: str
    overridestartdays: List[str]
    overridestoptime: str
    overridestopdays: List[str]
    overridevalue: float
