"""pipx install: reinstall with its extras and re-inject what was injected."""

from __future__ import annotations
import json
import re
import sys
from pathlib import Path


def _pipx_metadata(prefix: str | Path | None = None) -> dict:
    path = Path(prefix if prefix is not None else sys.prefix) / "pipx_metadata.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def pipx_injected(prefix: str | Path | None = None) -> list[str]:
    """Packages injected beside this pipx install (`pipx inject`), from its
    `pipx_metadata.json`: `pipx install --force` drops them."""
    injected = _pipx_metadata(prefix).get("injected_packages") or {}
    out = []
    for name, record in injected.items():
        spec = (record or {}).get("package_or_url") if isinstance(record, dict) else None
        out.append(str(spec or name))
    return out


def pipx_extras(prefix: str | Path | None = None) -> tuple[str, ...]:
    """The extras this pipx install was installed with (its recorded spec):
    `pipx install --force probe-research[all]` would record `[all]` alone."""
    main = _pipx_metadata(prefix).get("main_package") or {}
    spec = str(main.get("package_or_url") or "") if isinstance(main, dict) else ""
    found = re.match(r"^\s*probe-research\s*\[([^\]]*)\]", spec)
    if not found:
        return ()
    return tuple(e.strip() for e in found.group(1).split(",") if e.strip())
