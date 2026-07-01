"""Re-export usage-counter tool so the capability loader discovers it."""

import sys
from pathlib import Path

_CAPABILITY_ROOT = Path(__file__).resolve().parents[1]
if str(_CAPABILITY_ROOT) not in sys.path:
    sys.path.insert(0, str(_CAPABILITY_ROOT))

from self_improvement_lib.skill_io import record_skill_outcome  # noqa: E402

__all__ = ["record_skill_outcome"]
