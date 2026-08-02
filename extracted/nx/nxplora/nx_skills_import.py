"""
nx_skills_import.py - local skill summary helpers for NX CLI.
"""

from __future__ import annotations

import json
import os
from pathlib import Path


def _summary_candidates() -> list[Path]:
    env_path = os.environ.get("NX_SKILLS_SUMMARY_PATH")
    candidates = []
    home = Path.home()
    if env_path:
        # Only honour the env override when it resolves UNDER ~/.nx — prevents
        # a hostile NX_SKILLS_SUMMARY_PATH from pointing the loader at an
        # arbitrary file outside NX's own state directory.
        try:
            p = Path(env_path).expanduser().resolve()
            nx_root = (home / ".nx").resolve()
            if str(p) == str(nx_root) or str(p).startswith(str(nx_root) + os.sep):
                candidates.append(p)
        except Exception:
            pass

    candidates.extend(
        [
            home / ".nx" / "skills_summary.json",
            home / ".nx" / "skills" / "summary.json",
            home / ".nx" / "skills" / "manifest.json",
        ]
    )
    return candidates


def _normalize_summary(data: dict) -> dict:
    totals = data.get("totals", {}) if isinstance(data.get("totals"), dict) else {}
    normalized_totals = {
        "elite_specs": int(totals.get("elite_specs", 0) or 0),
        "taxonomy": int(totals.get("taxonomy", 0) or 0),
        "elite_caps": int(totals.get("elite_caps", 0) or 0),
        "packages": int(totals.get("packages", 0) or 0),
        "slash": int(totals.get("slash", 0) or 0),
        "rag": int(totals.get("rag", 0) or 0),
    }
    total = data.get("total")
    if total is None:
        total = sum(normalized_totals.values())
    total = int(total or 0)
    imported = bool(data.get("imported")) or total > 0 or any(normalized_totals.values())
    return {"imported": imported, "total": total, "totals": normalized_totals}


def skills_summary() -> dict:
    for path in _summary_candidates():
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            continue
        if isinstance(data, dict):
            return _normalize_summary(data)

    return {
        "imported": False,
        "total": 0,
        "totals": {
            "elite_specs": 0,
            "taxonomy": 0,
            "elite_caps": 0,
            "packages": 0,
            "slash": 0,
            "rag": 0,
        },
    }
