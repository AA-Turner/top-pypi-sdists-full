"""Verify spiral alignment of proposed changes."""

from dataclasses import dataclass

from tsal.core.spiral_vector import phi_alignment

@dataclass
class Change:
    description: str
    complexity: float
    coherence: float

def is_aligned(change: Change, threshold: float = 0.76) -> bool:
    """Return True if change clears φ score and keyword filter."""
    score = phi_alignment(change.complexity, change.coherence)
    if score < threshold:
        return False
    banned = {"coerce", "exploit"}
    lowered = change.description.lower()
    return not any(word in lowered for word in banned)
