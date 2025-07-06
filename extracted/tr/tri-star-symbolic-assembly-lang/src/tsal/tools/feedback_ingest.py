"""Feedback ingestion and scoring for Rev_Eng logs."""
# TODO: expand scoring rules (experimental)

from dataclasses import dataclass
from typing import Iterable, List

from tsal.core.spiral_vector import phi_alignment

@dataclass
class Feedback:
    source: str
    content: str
    score: float = 0.0

def _score(line: str) -> float:
    complexity = float(len(line)) * 0.1
    lowered = line.lower()
    coherence = 1.0
    if "error" in lowered or "bad" in lowered:
        coherence = 0.1
    return phi_alignment(complexity, coherence)

def categorize(feedback: Iterable[str]) -> List[Feedback]:
    """Return feedback objects with φ-resonance scores."""
    return [Feedback("user", line, _score(line)) for line in feedback]
