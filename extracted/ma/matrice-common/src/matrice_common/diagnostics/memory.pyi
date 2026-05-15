"""Auto-generated stub for module: memory."""
from typing import Any, Dict

# Constants
logger: Any

# Functions
def delta(before: Any, after: Any) -> Any:
    """
    Return ``after - before`` per field. Missing fields stay None.
    """
    ...
def format_table(snap: Any) -> str:
    """
    Render a snapshot as a human-readable multi-line table.
    """
    ...
def snapshot() -> Any:
    """
    Capture memory state from every available source.
    """
    ...

# Classes
class MemorySnapshot:
    # A point-in-time memory reading from multiple sources. All sizes in bytes.

    def to_dict(self: Any) -> Dict[str, Any]: ...

