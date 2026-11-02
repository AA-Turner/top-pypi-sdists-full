"""Arms present in this install (operator 2026-10-03): the console shows a surface
only when the package that owns it is installed — hugpy-core is the base, the
rest are legos.

An arm is present when its package is installed in core's environment, or when
any installed distribution declares it in the ``hugpy.arms`` entry-point group
(``[project.entry-points."hugpy.arms"] media = "hugpy_media.api:bp"``).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

DEFAULT_ARMS_DIR = "/usr/share/hugpy/arms.d"

# surface key -> the distribution that owns it (None: entry point only)
ARMS = {
    # 2026-10-20: the agent is a backend (its /fleet page was retired); its
    # surfaces are API-only. Sessions are the console's own Station tab.
    "nodes":     {"label": "Agent Nodes", "package": "hugpy-agent", "ui": None},
    "fleet":     {"label": "Fleet",       "package": "hugpy-agent", "ui": None},
    "media":     {"label": "Media",       "package": "hugpy-media", "ui": "@hugpy/media-intelligence-ui"},
    "video":     {"label": "Video",       "package": "hugpy-video", "ui": "@hugpy/video-intelligence-ui"},
    "trace":     {"label": "Trace",       "package": None},
    "evictions": {"label": "Evictions",   "package": None},
    # docs-only owners (a docs page shows when its owner is present)
    "discord":   {"label": "Discord",     "package": "hugpy-discord"},
    "toolserver": {"label": "Toolserver", "package": "abstract-toolserver"},
    "station":   {"label": "Station",     "package": None},
    "vmpool":    {"label": "VM pool",     "package": None},
    "phonebrick": {"label": "Phone brick", "package": None},   # retired with hugpy_fleet
}


def _version(dist: Optional[str]) -> Optional[str]:
    if not dist:
        return None
    try:
        from importlib.metadata import version
        return version(dist)
    except Exception:  # noqa: BLE001 — not installed
        return None


def _declared() -> dict:
    """{arm key: provider/version} from entry points and arm descriptors."""
    out = {}
    try:
        from importlib.metadata import entry_points
        for ep in entry_points(group="hugpy.arms"):
            out[ep.name] = {"package": getattr(getattr(ep, "dist", None), "name", None)}
    except Exception:  # noqa: BLE001
        pass
    root = Path(os.environ.get("HUGPY_ARMS_DIR") or DEFAULT_ARMS_DIR)
    try:
        for path in root.glob("*.json"):
            try:
                doc = json.loads(path.read_text(encoding="utf-8"))
                key = str(doc.get("arm") or "").strip() if isinstance(doc, dict) else ""
                if key:
                    current = out.setdefault(key, {})
                    current.setdefault("package", doc.get("package") or f"hugpy-{key}")
                    current["version"] = doc.get("version") or current.get("version")
            except (OSError, ValueError, TypeError):
                continue
    except OSError:
        pass
    return out


def arms() -> dict:
    declared = _declared()
    out = {}
    for key, a in ARMS.items():
        # Standalone Agent installs one `agent` descriptor. Its console
        # surfaces retain the existing `nodes` and `fleet` keys.
        provider = "agent" if key in ("nodes", "fleet") else key
        registration = declared.get(key) or declared.get(provider) or {}
        ver = _version(a["package"])
        present = ver is not None or key in declared or provider in declared
        out[key] = {"label": a["label"], "present": present,
                    "package": a["package"] if ver is not None else registration.get("package"),
                    "version": ver or registration.get("version"), "ui": a.get("ui")}
    return out


# The base: hugpy-core's own UI package (the console) — the inverse index's root.
CORE = {"package": "hugpy-core", "ui": "@hugpy/ui"}
