"""Re-export reflector tools so the capability loader discovers them."""

import sys
from pathlib import Path

_CAPABILITY_ROOT = Path(__file__).resolve().parents[1]
if str(_CAPABILITY_ROOT) not in sys.path:
    sys.path.insert(0, str(_CAPABILITY_ROOT))

from self_improvement_lib.skill_io import update_skill, write_skill  # noqa: E402

__all__ = ["update_skill", "write_skill"]
