"""Central constants derived from the Codex Fireproof white paper."""

from .symbols import PHI

PERCEPTION_THRESHOLD = 0.75
LEARNING_RATE = 0.05
CONNECTION_DECAY = 0.01
MAX_NODES = 8192
MAX_AGENTS = 1024
MAX_DIMENSIONS = 8

__all__ = [
    "PHI",
    "PERCEPTION_THRESHOLD",
    "LEARNING_RATE",
    "CONNECTION_DECAY",
    "MAX_NODES",
    "MAX_AGENTS",
    "MAX_DIMENSIONS",
]
