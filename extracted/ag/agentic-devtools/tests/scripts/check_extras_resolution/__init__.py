"""Shared fixtures and helpers for check_extras_resolution tests."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _load_module():
    """Load scripts/check_extras_resolution.py as a module."""
    repo_root = Path(__file__).resolve().parents[3]
    script_path = repo_root / "scripts" / "check_extras_resolution.py"
    spec = importlib.util.spec_from_file_location("check_extras_resolution", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load check_extras_resolution.py from {script_path!s}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


checker = _load_module()
