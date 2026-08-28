"""Auto-generated stub for module: rtp_probe."""
from typing import Any

# Constants
RESET_BACKWARD_TICKS: Any
RTP_CLOCK_HZ: int
RTP_WRAP: Any

# Functions
def gcd_of(values: list[int], round_to: int = 100) -> int:
    """
    GCD of values, rounding each to the nearest `round_to` first so that ±1-tick
    RTP jitter (e.g. 11999/12000/12001) does not collapse the grid to 1.
    """
    ...
def main() -> int: ...
def parse_message(values: dict) -> dict | None:
    """
    Extract the fields we care about from one stream entry's `result` JSON.
    """
    ...
def probe(rows: list[dict]) -> dict:
    """
    Analyse collected rows; returns a report dict.
    """
    ...
def stream_key(camera_id: str, app_deployment_id: str) -> str: ...
def unwrap_rtp(rtp_values: list[int]) -> list[int]:
    """
    Convert a list of raw uint32 rtp timestamps into a continuous monotone
    sequence, undoing 2**32 wrap.  A genuine loop reset (large backward jump
    that is NOT a near-2**32 wrap) is left in place so it can be detected.
    """
    ...
