"""Shared fixtures and helpers for record_discovery_baseline tests."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def _load_module():
    """Load scripts/record_discovery_baseline.py as a module."""
    script_path = REPO_ROOT / "scripts" / "record_discovery_baseline.py"
    spec = importlib.util.spec_from_file_location("record_discovery_baseline", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load record_discovery_baseline.py from {script_path!s}")
    module = importlib.util.module_from_spec(spec)
    # sys.modules registration is required so that @dataclass can resolve
    # forward references via sys.modules.get(cls.__module__).__dict__.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


baseline = _load_module()


def build_repo(tmp_path: Path, *, prompts=(), agents=(), skills=None) -> Path:
    """Create a fake repository tree with the requested units."""
    prompts_dir = tmp_path / baseline.PROMPTS_DIR
    prompts_dir.mkdir(parents=True)
    for name in prompts:
        (prompts_dir / name).write_text("prompt", encoding="utf-8")

    agents_dir = tmp_path / baseline.AGENTS_DIR
    agents_dir.mkdir(parents=True)
    for name in agents:
        (agents_dir / name).write_text("agent", encoding="utf-8")

    if skills is not None:
        for name in skills:
            skill_dir = tmp_path / baseline.SKILLS_DIR / name
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("skill", encoding="utf-8")

    return tmp_path
