"""Stub file for diagnostics directory."""
from typing import Any, Dict

from .memory import delta, format_table, snapshot

# Constants
logger: Any = ...  # From memory

# Functions
# From __main__
def main(argv: Any = None) -> int: ...

# From memory
def delta(before: Any, after: Any) -> Any:
    """
    Return ``after - before`` per field. Missing fields stay None.
    """
    ...

# From memory
def format_table(snap: Any) -> str:
    """
    Render a snapshot as a human-readable multi-line table.
    """
    ...

# From memory
def snapshot() -> Any:
    """
    Capture memory state from every available source.
    """
    ...

# Classes
# From memory
class MemorySnapshot:
    # A point-in-time memory reading from multiple sources. All sizes in bytes.

    def to_dict(self: Any) -> Dict[str, Any]: ...


from . import __main__, memory