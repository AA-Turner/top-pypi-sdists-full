"""Generator for the repo-root ``setup-dev-tools.py``.

The generated script contains the ``# AGDT-MANAGED-ORCHESTRATOR`` marker
and delegates to ``.agdt/agentic-devtools-complete-setup.py`` then
``setup-repo-specific-dev-tools.py`` with fail-fast semantics.
"""

from __future__ import annotations

from .constants import COMPLETE_SETUP_FILENAME, ORCHESTRATOR_MARKER, REPO_SPECIFIC_FILENAME


def generate_root_entry_point() -> str:
    """Return the full content of ``setup-dev-tools.py``."""
    return _ROOT_TEMPLATE.format(
        marker=ORCHESTRATOR_MARKER,
        complete=COMPLETE_SETUP_FILENAME,
        repo_specific=REPO_SPECIFIC_FILENAME,
    )


_ROOT_TEMPLATE = '''\
#!/usr/bin/env python3
"""Development environment setup — entry point.

This script is managed by agentic-devtools and regenerated on every
``agdt-setup`` run.  DO NOT EDIT — your changes will be overwritten.

Calls ``.agdt/agentic-devtools-complete-setup.py`` (managed) then
``setup-repo-specific-dev-tools.py`` (customer-owned) with fail-fast
semantics: if the complete-setup script fails, the repo-specific
script is NOT executed.

Supports: ``--foreground`` (default, forward-compatible no-op).

Note: When invoked by ``agdt-setup`` autorun, the environment variable
``AGDT_SETUP_AUTORUN`` is set to ``"1"``. The guard below stores that
value defensively; normal delegation proceeds unchanged during autorun.
When ``AGDT_SETUP_TARGET_REPO_ROOT`` is set, setup execution targets that
repository root while still loading managed scripts from this script's
directory.
"""

{marker}

import argparse
import os
import subprocess
import sys
from pathlib import Path

# AGDT-SETUP-AUTORUN-GUARD
# AGDT_SETUP_AUTORUN is set by the agdt-setup autorun helper when invoking this
# script. Recursion prevention is enforced in that helper (not here); this read
# is a forward-looking defensive reference. Currently a no-op — normal
# delegation to complete-setup and repo-specific scripts proceeds unchanged.
_AGDT_AUTORUN_ACTIVE = os.environ.get("AGDT_SETUP_AUTORUN")


def main():
    parser = argparse.ArgumentParser(
        description="Development environment setup.",
    )
    parser.add_argument(
        "--foreground", action="store_true", default=True,
        help="Run in foreground (default, forward-compatible no-op).",
    )
    parser.parse_args()

    _AGDT_TARGET_REPO_ROOT = os.environ.get("AGDT_SETUP_TARGET_REPO_ROOT")
    script_root = Path(__file__).resolve().parent
    repo_root = Path(_AGDT_TARGET_REPO_ROOT).resolve() if _AGDT_TARGET_REPO_ROOT else script_root
    foreground_args = ["--foreground"]

    # Step 1: Complete setup (managed by agentic-devtools)
    agdt_dir = script_root / ".agdt"
    if not agdt_dir.is_dir():
        print(
            "  ✗ .agdt/ directory not found. Run 'agdt-setup' first to"
            " generate the required setup scripts.",
            file=sys.stderr,
        )
        sys.exit(1)

    complete = agdt_dir / "{complete}"
    if not complete.exists():
        print(
            f"  ✗ Complete setup script not found: {{complete}}\\n"
            "    Run 'agdt-setup' to regenerate setup scripts.",
            file=sys.stderr,
        )
        sys.exit(1)

    result = subprocess.run(
        [sys.executable, str(complete)] + foreground_args,
        cwd=str(repo_root),
    )
    if result.returncode != 0:
        print(
            "  ✗ Complete setup failed — skipping repo-specific setup.",
            file=sys.stderr,
        )
        sys.exit(result.returncode)

    # Step 2: Repo-specific setup (customer-owned, optional).
    # Resolve from repo_root so __file__ and sys.path[0] match the real checkout
    # even when AGDT_SETUP_TARGET_REPO_ROOT is set for temporary worktree runs.
    repo_specific = repo_root / "{repo_specific}"
    if repo_specific.exists():
        result = subprocess.run(
            [sys.executable, str(repo_specific)] + foreground_args,
            cwd=str(repo_root),
        )
        if result.returncode != 0:
            print("  ✗ Repo-specific setup failed.", file=sys.stderr)
            sys.exit(result.returncode)
    else:
        print(
            "  ℹ No repo-specific setup found"
            " (setup-repo-specific-dev-tools.py)."
        )


if __name__ == "__main__":
    main()
'''
