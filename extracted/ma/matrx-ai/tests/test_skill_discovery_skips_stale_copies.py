"""Skill discovery never ingests a stale copy from a git-ignored folder or a nested checkout.

2026-09-24: matrx-frontend's git-ignored ``work/`` held scratch copies of other checkouts
(``work/lockfile-repair``, ``work/aidream``) with OLD skill bodies; the catalog ingest let one
of them win over the freshly synced ``handoffs`` skill, so the DB never received it.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from matrx_ai.skills.ingest import discover_skill_roots


def _skill(root: Path, name: str) -> None:
    d = root / ".claude" / "skills" / name
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(f"---\nname: {name}\ndescription: x\n---\nbody\n", encoding="utf-8")


def test_ignored_and_nested_checkouts_are_skipped(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    (repo / ".gitignore").write_text("work/\n", encoding="utf-8")
    _skill(repo, "handoffs")
    _skill(repo / "work" / "plain-copy", "handoffs")          # ignored scratch copy, no .git
    nested = repo / "tools" / "other-checkout"
    nested.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(nested)], check=True)
    _skill(nested, "handoffs")                                  # a nested checkout

    roots = [p.resolve() for p in discover_skill_roots(repo)]
    assert roots == [(repo / ".claude" / "skills").resolve()]
