#!/usr/bin/env python3
"""Build wheel with grpc_common vendored.

Usage:
    python scripts/build_wheel.py          # builds both sdist and wheel
    python scripts/build_wheel.py --wheel  # builds wheel only
    python scripts/build_wheel.py --sdist  # builds sdist only

This script temporarily adds hook configuration to pyproject.toml,
builds, then restores it. This allows:
- Docker editable installs to work (no hook file required in pyproject.toml)
- Wheel/sdist builds to include vendored grpc_common via the hook
"""

import subprocess
import sys
from pathlib import Path

PYPROJECT = Path(__file__).parent.parent / "pyproject.toml"
GRPC_COMMON = (
    Path(__file__).parent.parent.parent / "grpc_common_py" / "langgraph_grpc_common"
)
HOOK_FILE = Path(__file__).parent.parent / "hatch_build.py"

# Hook configuration to inject
SDIST_HOOK = """
[tool.hatch.build.targets.sdist.hooks.custom]
path = "hatch_build.py"
"""

WHEEL_HOOK = """
[tool.hatch.build.targets.wheel.hooks.custom]
path = "hatch_build.py"
"""


def main():
    if not GRPC_COMMON.exists():
        sys.stderr.write(f"Error: grpc_common not found at {GRPC_COMMON}\n")
        sys.exit(1)

    if not HOOK_FILE.exists():
        sys.stderr.write(f"Error: hook file not found at {HOOK_FILE}\n")
        sys.exit(1)

    # Read original
    original = PYPROJECT.read_text()

    # Inject hook configurations
    modified = original

    # Add sdist hook before [tool.hatch.build.targets.sdist]
    if "[tool.hatch.build.targets.sdist.hooks.custom]" not in modified:
        modified = modified.replace(
            "[tool.hatch.build.targets.sdist]",
            f"{SDIST_HOOK.strip()}\n\n[tool.hatch.build.targets.sdist]",
        )

    # Add wheel hook before [tool.hatch.build.targets.wheel.force-include]
    if "[tool.hatch.build.targets.wheel.hooks.custom]" not in modified:
        modified = modified.replace(
            "[tool.hatch.build.targets.wheel.force-include]",
            f"{WHEEL_HOOK.strip()}\n\n[tool.hatch.build.targets.wheel.force-include]",
        )

    try:
        # Write modified
        PYPROJECT.write_text(modified)

        # Build
        args = ["uv", "build"]
        if "--wheel" in sys.argv:
            args.append("--wheel")
        elif "--sdist" in sys.argv:
            args.append("--sdist")

        result = subprocess.run(args, check=False)
        sys.exit(result.returncode)
    finally:
        # Restore original
        PYPROJECT.write_text(original)


if __name__ == "__main__":
    main()
