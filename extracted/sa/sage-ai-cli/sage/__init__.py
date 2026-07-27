"""Sage AI CLI."""

from __future__ import annotations

import os

# Auto-configure NO_COLOR environment variables if run within antigravity sandbox
if "ANTIGRAVITY_PROJECT_ID" in os.environ:
    os.environ["NO_COLOR"] = "1"

# NOTE: this module used to replace BOTH builtins.open and io.open, process-wide,
# with a wrapper that special-cased __init__.py and silently discarded whatever a
# caller wrote to it. The swallowing behaviour is long gone and what was left was
# a pure pass-through, so every open() in the process paid for an extra Python
# frame to accomplish nothing -- two frames, in fact, because sage/cli_core.py
# then wrapped this wrapper. Both patches, and the _is_system_path helper that
# only the deleted logic ever used, have been removed rather than left sitting
# under a comment describing behaviour the code no longer had: that comment was
# an active invitation to "restore" write-swallowing, which would corrupt every
# writer in the process. Do not reintroduce a global open() patch here.




def _discover_version() -> str:
    """Resolve the installed package version.

    Order: pyproject.toml (source checkouts) → installed-package metadata →
    a sentinel string. The sentinel keeps imports working in unusual envs
    where neither path resolves, so the CLI still boots and `sage --version`
    can at least report something rather than crashing.
    """
    try:
        import re
        from pathlib import Path

        pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
        if pyproject.exists():
            match = re.search(
                r'^version = "([^"]+)"',
                pyproject.read_text(encoding="utf-8"),
                re.MULTILINE,
            )
            if match:
                return match.group(1)
    except Exception:
        pass

    try:
        from importlib.metadata import PackageNotFoundError, version
        return version("sage-ai-cli")
    except (ImportError, PackageNotFoundError):
        pass
    except Exception:
        return "0.0.0+unknown"

    return "0.0.0+unknown"


__version__ = _discover_version()

__all__ = ["__version__"]
