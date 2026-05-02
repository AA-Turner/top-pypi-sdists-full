from dataclasses import dataclass
from typing import Optional


@dataclass
class SearchItemFilters:
    track: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    year: Optional[int] = None
    # TODO: Add missing fields options
