"""THE FLAT-FILE GUARD: only a self-declaring `<name>.md` is a skill.

Failing-then-passing witness for the 2026-07-16 import, which ingested
`common-docs/skills/index.md` (a listing) and
`matrx-frontend/features/skills/FEATURE.md` (a React feature's doc) as live
platform skills named "index" and "FEATURE". Both walkers (local FS and the
sandbox proxy) share `_flat_md_is_skill`; this test covers the local one plus
the helper directly.
"""

from __future__ import annotations

from pathlib import Path

from matrx_ai.skills.ingest import (
    _flat_md_is_skill,
    _looks_like_skills_dir,
    walk_filesystem,
)

SKILL_MD = """---
name: real-flat-skill
description: A flat-layout skill that declares itself.
---

# Real flat skill

Body.
"""

INDEX_MD = """# Skills

- [handoffs](/skills/handoffs/SKILL.md)
"""

FEATURE_MD = """---
title: skills feature
---

# FEATURE.md — `skills`

The frontend feature doc that happens to live in a folder named `skills`.
"""


def test_helper_accepts_only_self_declaring_flat_files() -> None:
    assert _flat_md_is_skill("real-flat-skill.md", SKILL_MD) is True
    assert _flat_md_is_skill("index.md", INDEX_MD) is False
    assert _flat_md_is_skill("FEATURE.md", FEATURE_MD) is False
    assert _flat_md_is_skill("README.md", SKILL_MD) is False
    # No frontmatter at all → never a skill, whatever it is called.
    assert _flat_md_is_skill("notes-on-things.md", "# Just a doc\n\ntext\n") is False


def test_walk_skips_docs_beside_skills(tmp_path: Path) -> None:
    root = tmp_path / "skills"
    root.mkdir()
    (root / "index.md").write_text(INDEX_MD)
    (root / "FEATURE.md").write_text(FEATURE_MD)
    (root / "real-flat-skill.md").write_text(SKILL_MD)
    folder = root / "folder-skill"
    folder.mkdir()
    (folder / "SKILL.md").write_text(
        "---\nname: folder-skill\ndescription: Folder layout.\n---\n\nBody.\n"
    )

    ids = sorted(p.skill_id for p in walk_filesystem(root))
    assert ids == ["folder-skill", "real-flat-skill"]


def test_doc_only_dir_named_skills_is_not_a_skills_root(tmp_path: Path) -> None:
    """A code feature's `skills/` folder with only docs is not a skills leaf."""
    feature = tmp_path / "features" / "skills"
    feature.mkdir(parents=True)
    (feature / "FEATURE.md").write_text(FEATURE_MD)
    assert _looks_like_skills_dir(feature) is False
