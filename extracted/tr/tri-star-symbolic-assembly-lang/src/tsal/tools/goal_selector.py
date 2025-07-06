"""Score goals for priority based on mesh and alignment."""  # [!INTERNAL STUB]
# TODO: refine scoring with RL signals (experimental)

from dataclasses import dataclass
from typing import Iterable, List

@dataclass
class Goal:
    name: str
    mesh_benefit: float
    alignment: float
    cost: float
    novelty: float

def score_goals(goals: Iterable[Goal]) -> List[Goal]:
    """Return goals ordered by priority."""
    return sorted(
        goals,
        key=lambda g: (
            g.mesh_benefit * g.alignment
            + 0.1 * g.mesh_benefit
            - g.cost
            + g.novelty
        ),
        reverse=True,
    )
