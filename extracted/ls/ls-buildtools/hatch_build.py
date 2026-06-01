import sys
import os
from pathlib import Path

# hack to add the source of this package itself to the python path to use itself as hatchling hook
parent = os.path.join(Path(__file__).parent, "src")
sys.path.append(parent)

# import the hook such that it is detected by hatchling
from ls_buildtools._integration.hatchling import HatchlingProtectionHook  # noqa: E402

__all__ = [HatchlingProtectionHook]
