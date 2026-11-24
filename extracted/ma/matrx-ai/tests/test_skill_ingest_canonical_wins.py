"""The catalog ingest keeps the CANONICAL copy of a skill and never reads a leftover tree.

2026-11-02: 80 ``skill.definition`` rows came from ``apps/matrx-extend/.matrx/task1-active/cleanup-source-…``,
a leftover copy on a developer's machine, and "later root wins" let those stale bodies override the fresh
canonicals. Two independent layers, each tested alone:
1. discovery refuses a skills folder under a hidden or scratch tree (``.matrx/task1-active``, ``temp``, ``work``);
2. between differing copies the file at the path its own banner names as canonical wins, in either order.
"""

from __future__ import annotations

from pathlib import Path

from matrx_ai.skills.ingest import discover_skill_roots, walk_paths

BANNER = "<!-- SYNCED COPY — do not edit here.\n     Canonical: docs/skills/{name}/SKILL.md\n-->\n"


def _skill(root: Path, name: str, body: str) -> None:
    d = root / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: \"Use when testing {name}.\"\n---\n\n{BANNER.format(name=name)}\n{body}\n",
        encoding="utf-8",
    )


def _repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    _skill(repo / "docs" / "skills", "alpha", "FRESH canonical body")
    _skill(repo / ".claude" / "skills", "alpha", "FRESH canonical body")
    _skill(repo / "app" / ".matrx" / "skills", "beta", "a real .matrx skills folder")
    for leftover in (
        repo / "app" / ".matrx" / "task1-active" / "cleanup-source-x" / ".claude" / "skills",
        repo / "temp" / "run-1" / ".claude" / "skills",
        repo / "work" / "copy" / "skills",
    ):
        _skill(leftover, "alpha", "STALE leftover body")
    return repo


def test_a_leftover_tree_is_never_a_skills_root(tmp_path):
    repo = _repo(tmp_path)
    roots = {str(r.relative_to(repo)) for r in discover_skill_roots(repo)}
    assert roots == {"docs/skills", ".claude/skills", "app/.matrx/skills"}, roots


def test_the_canonical_copy_wins_in_either_order(tmp_path):
    repo = _repo(tmp_path)
    canonical = repo / "docs" / "skills"
    stale = tmp_path / "stale" / "skills"
    _skill(stale, "alpha", "STALE body passed explicitly")
    for order in ([canonical, stale], [stale, canonical]):
        parsed, _roots, collisions = walk_paths(order)
        alpha = next(p for p in parsed if p.skill_id == "alpha")
        assert "FRESH canonical body" in alpha.body, (order, alpha.source_path)
        assert alpha.source_path.endswith("docs/skills/alpha/SKILL.md")
        assert collisions and "using " + alpha.source_path in collisions[0]


def test_identical_copies_record_the_canonical_path(tmp_path):
    repo = _repo(tmp_path)
    parsed, _roots, collisions = walk_paths([repo / "docs" / "skills", repo / ".claude" / "skills"])
    alpha = next(p for p in parsed if p.skill_id == "alpha")
    assert alpha.source_path.endswith("docs/skills/alpha/SKILL.md") and not collisions


def test_a_refused_leftover_tree_says_so(tmp_path, monkeypatch):
    from matrx_ai.skills import ingest

    said: list[str] = []
    monkeypatch.setattr(ingest, "vcprint", lambda msg, **_: said.append(str(msg)))
    discover_skill_roots(_repo(tmp_path))
    skipped = [m for m in said if "SKIPPED skills under a scratch/leftover tree" in m]
    assert any("task1-active" in m for m in skipped) and len(skipped) == 3, said
