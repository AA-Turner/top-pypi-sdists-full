"""Compare the installed dreamscale against the newest release on PyPI."""

from __future__ import annotations

import os
import re
import sys

PYPI_URL = "https://pypi.org/pypi/dreamscale/json"
SKIP_ENV = "DREAMSCALE_SKIP_VERSION_CHECK"

# The release shapes we publish: 0.1.0, 0.1.0a64, 0.1.0rc1, 0.1.0.post1.
_VERSION_RE = re.compile(r"^(\d+(?:\.\d+)*)(?:(a|b|rc)(\d+))?(?:\.post(\d+))?$")
_PRE_RANK = {"a": 0, "b": 1, "rc": 2}


def version_key(version: str) -> tuple | None:
    """Sortable key for a release version, or None for a shape we don't publish."""
    match = _VERSION_RE.match(version)
    if match is None:
        return None
    release, pre, pre_n, post = match.groups()
    numbers = tuple(int(part) for part in release.split("."))
    numbers += (0,) * (4 - len(numbers))
    # A final release sorts after every pre-release of the same number.
    pre_key = (_PRE_RANK[pre], int(pre_n)) if pre else (3, 0)
    return numbers, pre_key, int(post or -1)


def latest_release(timeout_s: float = 2.0) -> str | None:
    """Newest non-yanked dreamscale on PyPI, pre-releases included; None if unknown."""
    import httpx

    try:
        timeout = httpx.Timeout(timeout_s, connect=min(1.0, timeout_s))
        response = httpx.get(PYPI_URL, timeout=timeout)
        response.raise_for_status()
        releases = response.json()["releases"]
    except (httpx.HTTPError, ValueError, KeyError, TypeError):
        return None
    keyed = [
        (key, version)
        for version, files in releases.items()
        if files and not all(f.get("yanked") for f in files)
        if (key := version_key(version)) is not None
    ]
    return max(keyed)[1] if keyed else None


def upgrade_command(latest: str) -> str:
    """The command that moves this install to `latest`."""
    if "uv/tools/" in sys.prefix.replace("\\", "/"):
        return _exact_pin_reinstall() or "uv tool upgrade dreamscale"
    if sys.prefix != sys.base_prefix or "VIRTUAL_ENV" in os.environ:
        return f'uv add "dreamscale=={latest}"'
    return f'pip install --upgrade "dreamscale=={latest}"'


def _exact_pin_reinstall() -> str | None:
    """A one-time unpinned reinstall for a tool installed as `dreamscale==X`.

    `uv tool upgrade` keeps the constraint a tool was installed with, so an exact
    pin never moves. Reinstalling without it keeps the extras and Python version.
    """
    import tomllib
    from pathlib import Path

    try:
        receipt = tomllib.loads((Path(sys.prefix) / "uv-receipt.toml").read_text())
    except (OSError, ValueError):
        return None
    tool = receipt.get("tool", {})
    requirement = next(
        (r for r in tool.get("requirements", []) if r.get("name") == "dreamscale"), {}
    )
    if not str(requirement.get("specifier", "")).startswith("=="):
        return None
    extras = requirement.get("extras") or []
    target = f"dreamscale[{','.join(extras)}]" if extras else "dreamscale"
    python = f" --python {tool['python']}" if tool.get("python") else ""
    return f'uv tool install --force{python} "{target}"'


_STYLE = {"current": "green", "outdated": "yellow", "unknown": None}


def update_status(current: str) -> tuple[str, str | None, str | None] | None:
    """(status line, color, upgrade command or None), or None when the check is skipped."""
    if os.environ.get(SKIP_ENV):
        return None
    latest = latest_release()
    current_key = version_key(current)
    if latest is None or current_key is None:
        return "Could not check PyPI for updates.", _STYLE["unknown"], None
    if version_key(latest) > current_key:
        message = f"A new version is available: {latest} (installed: {current})"
        return message, _STYLE["outdated"], upgrade_command(latest)
    return "Up to date.", _STYLE["current"], None
