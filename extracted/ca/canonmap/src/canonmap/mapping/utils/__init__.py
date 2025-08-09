from .blocking import (
    block_candidates,
    block_by_exact_match,
    block_by_initialism,
    block_by_phonetic,
    block_by_soundex,
    BLOCKING_HANDLERS,
)
from .normalize import normalize
from .scoring import scorer

__all__ = [
    "block_candidates",
    "block_by_exact_match",
    "block_by_initialism", 
    "block_by_phonetic",
    "block_by_soundex",
    "BLOCKING_HANDLERS",
    "normalize",
    "scorer"
]
