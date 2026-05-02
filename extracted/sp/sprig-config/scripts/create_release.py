#!/usr/bin/env python3
"""
Python wrapper for create-release-tag.sh script.
This allows the release script to be called via Poetry: poetry run create-release
"""
import subprocess
import sys
from pathlib import Path


def main():
    """Execute the create-release-tag.sh bash script."""
    script_dir = Path(__file__).parent
    bash_script = script_dir / "create-release-tag.sh"

    if not bash_script.exists():
        print(f"❌ Error: Script not found at {bash_script}", file=sys.stderr)
        sys.exit(1)

    # Execute the bash script
    try:
        result = subprocess.run(
            ["/bin/bash", str(bash_script)],
            check=False,  # Don't raise on non-zero exit
            cwd=script_dir.parent,  # Run from project root
        )
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n⚠️  Release creation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Error executing release script: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
