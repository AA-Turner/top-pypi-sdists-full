"""pylhasa - LHA/LZH archive reader with safe extraction and streaming."""

from ._archive import Archive, Entry, from_bytes, open, open_bytes, open_fileobj
from ._exceptions import BadArchiveError, PylhasaError, UnsafePathError

__all__: list[str] = [
    "Archive",
    "Entry",
    "open",
    "from_bytes",
    "open_bytes",
    "open_fileobj",
    "PylhasaError",
    "BadArchiveError",
    "UnsafePathError",
]

__version__: str = "0.1.1"
