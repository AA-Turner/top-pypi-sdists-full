"""Sage AI CLI."""

from __future__ import annotations


def _discover_version() -> str:
    """Resolve the installed package version.

    Order: installed-package metadata → pyproject.toml (source checkouts) →
    a sentinel string. The sentinel keeps imports working in unusual envs
    where neither path resolves, so the CLI still boots and `sage --version`
    can at least report something rather than crashing.
    """
    try:
        from importlib.metadata import PackageNotFoundError, version
    except ImportError:
        return "0.0.0+unknown"

    try:
        return version("sage-ai-cli")
    except PackageNotFoundError:
        pass
    except Exception:
        return "0.0.0+unknown"

    try:
        import re
        from pathlib import Path

        pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
        match = re.search(
            r'^version = "([^"]+)"',
            pyproject.read_text(encoding="utf-8"),
            re.MULTILINE,
        )
        if match:
            return match.group(1)
    except Exception:
        pass

    return "0.0.0+unknown"


__version__ = _discover_version()

__all__ = ["__version__"]
