"""Regression guard: ensure spec_kitty_tracker.__version__ matches pyproject.toml.

The runtime ``__version__`` constant in ``src/spec_kitty_tracker/__init__.py``
must always match the ``[project].version`` field in ``pyproject.toml``.
Downstream code and diagnostics that read the runtime version need both
sources of truth to agree, otherwise pinned consumers can make wrong contract
decisions based on a stale runtime version.

This test was added in response to a post-merge mission review that found the
runtime constant lagged the package metadata after a 0.2.0 → 0.3.0 bump.
"""

from __future__ import annotations

import sys
import tomllib
from pathlib import Path

import spec_kitty_tracker

PYPROJECT_PATH = Path(__file__).parent.parent / "pyproject.toml"


def test_runtime_version_matches_pyproject() -> None:
    """``spec_kitty_tracker.__version__`` must equal ``pyproject.toml [project].version``."""
    with PYPROJECT_PATH.open("rb") as f:
        data = tomllib.load(f)
    pyproject_version = data["project"]["version"]
    runtime_version = spec_kitty_tracker.__version__

    assert runtime_version == pyproject_version, (
        f"Version mismatch: runtime __version__ is {runtime_version!r} but "
        f"pyproject.toml [project].version is {pyproject_version!r}. "
        f"Update src/spec_kitty_tracker/__init__.py:__version__ to match."
    )


def test_runtime_version_is_not_empty() -> None:
    """``__version__`` must be a non-empty string."""
    assert isinstance(spec_kitty_tracker.__version__, str)
    assert spec_kitty_tracker.__version__, "__version__ must not be empty"


def test_python_version_supports_tomllib() -> None:
    """Sanity check: this regression test relies on stdlib ``tomllib`` (Python 3.11+).

    spec-kitty-tracker requires Python >= 3.11 in pyproject.toml, so tomllib is
    always available. If this assertion fails, the package's minimum Python
    version has dropped below 3.11 and this test needs a fallback.
    """
    assert sys.version_info >= (3, 11), (
        "tomllib is stdlib in Python 3.11+; spec-kitty-tracker requires 3.11+. "
        "If you are running an older interpreter, the regression test cannot run."
    )
