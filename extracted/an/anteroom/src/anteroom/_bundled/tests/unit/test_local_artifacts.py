"""Tests for services/local_artifacts.py."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from anteroom.db import _SCHEMA, ThreadSafeConnection
from anteroom.services.local_artifacts import (
    _LOCAL_DIR,
    discover_local_artifacts,
    load_local_artifacts,
    scaffold_local_artifact,
)


@pytest.fixture()
def db() -> ThreadSafeConnection:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(_SCHEMA)
    conn.commit()
    return ThreadSafeConnection(conn)


class TestDiscoverLocalArtifacts:
    def test_empty_dir(self, tmp_path: Path) -> None:
        assert discover_local_artifacts(tmp_path) == []

    def test_nonexistent_dir(self, tmp_path: Path) -> None:
        assert discover_local_artifacts(tmp_path / "nope") == []

    def test_discovers_rules(self, tmp_path: Path) -> None:
        rules = tmp_path / "rules"
        rules.mkdir()
        (rules / "my-rule.md").write_text("# My Rule\nDo stuff.\n")
        result = discover_local_artifacts(tmp_path)
        assert len(result) == 1
        assert result[0]["type"] == "rule"
        assert result[0]["name"] == "my-rule"
        assert result[0]["namespace"] == "local"
        assert "@local/rule/my-rule" == result[0]["fqn"]

    def test_discovers_skills(self, tmp_path: Path) -> None:
        skills = tmp_path / "skills"
        (skills / "greet").mkdir(parents=True)
        (skills / "greet" / "SKILL.md").write_text("---\nname: greet\n---\n\nsay hi\n")
        result = discover_local_artifacts(tmp_path)
        assert len(result) == 1
        assert result[0]["type"] == "skill"
        assert "say hi" in result[0]["content"]

    def test_skips_wrong_extension(self, tmp_path: Path) -> None:
        rules = tmp_path / "rules"
        rules.mkdir()
        (rules / "readme.py").write_text("not a rule")
        assert discover_local_artifacts(tmp_path) == []

    def test_skips_directories(self, tmp_path: Path) -> None:
        rules = tmp_path / "rules"
        rules.mkdir()
        (rules / "subdir").mkdir()
        assert discover_local_artifacts(tmp_path) == []

    def test_multiple_types(self, tmp_path: Path) -> None:
        (tmp_path / "rules").mkdir()
        (tmp_path / "rules" / "r1.md").write_text("rule 1")
        (tmp_path / "skills").mkdir()
        (tmp_path / "skills" / "s1").mkdir()
        (tmp_path / "skills" / "s1" / "SKILL.md").write_text("---\nname: s1\n---\n\nskill 1\n")
        (tmp_path / "instructions").mkdir()
        (tmp_path / "instructions" / "i1.md").write_text("instruction 1")
        result = discover_local_artifacts(tmp_path)
        types = {a["type"] for a in result}
        assert types == {"rule", "skill", "instruction"}


class TestLoadLocalArtifacts:
    def test_loads_global(self, db: ThreadSafeConnection, tmp_path: Path) -> None:
        local = tmp_path / _LOCAL_DIR
        rules = local / "rules"
        rules.mkdir(parents=True)
        (rules / "no-eval.md").write_text("Don't use eval()")
        count = load_local_artifacts(db, tmp_path)
        assert count == 1
        row = db.execute("SELECT * FROM artifacts WHERE name = 'no-eval'").fetchone()
        assert row is not None
        assert row["source"] == "local"

    def test_loads_project(self, db: ThreadSafeConnection, tmp_path: Path) -> None:
        proj = tmp_path / "myproject"
        proj.mkdir()
        local = proj / ".anteroom" / _LOCAL_DIR / "rules"
        local.mkdir(parents=True)
        (local / "proj-rule.md").write_text("Project rule")
        count = load_local_artifacts(db, tmp_path, project_dir=proj)
        assert count == 1

    def test_loads_both_global_and_project(self, db: ThreadSafeConnection, tmp_path: Path) -> None:
        # Global
        g = tmp_path / _LOCAL_DIR / "rules"
        g.mkdir(parents=True)
        (g / "global.md").write_text("global")
        # Project
        proj = tmp_path / "proj"
        proj.mkdir()
        p = proj / ".anteroom" / _LOCAL_DIR / "rules"
        p.mkdir(parents=True)
        (p / "local.md").write_text("local")
        count = load_local_artifacts(db, tmp_path, project_dir=proj)
        assert count == 2

    def test_returns_zero_when_no_artifacts(self, db: ThreadSafeConnection, tmp_path: Path) -> None:
        assert load_local_artifacts(db, tmp_path) == 0


class TestScaffoldLocalArtifact:
    def test_creates_rule(self, tmp_path: Path) -> None:
        path = scaffold_local_artifact("rule", "my-rule", tmp_path)
        assert path.exists()
        assert path.name == "my-rule.md"
        content = path.read_text()
        assert "my-rule" in content

    def test_creates_skill(self, tmp_path: Path) -> None:
        path = scaffold_local_artifact("skill", "my-skill", tmp_path)
        assert path.exists()
        assert path.name == "SKILL.md"
        assert path.parent.name == "my-skill"

    def test_creates_in_project_dir(self, tmp_path: Path) -> None:
        proj = tmp_path / "proj"
        proj.mkdir()
        path = scaffold_local_artifact("rule", "r1", tmp_path, project=True, project_dir=proj)
        assert ".anteroom" in str(path)
        assert path.exists()

    def test_rejects_path_traversal_name(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="Invalid artifact name"):
            scaffold_local_artifact("rule", "../../evil", tmp_path)

    def test_rejects_slash_in_name(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="Invalid artifact name"):
            scaffold_local_artifact("rule", "foo/bar", tmp_path)

    def test_invalid_type_raises(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="Invalid artifact type"):
            scaffold_local_artifact("bogus", "test", tmp_path)

    def test_duplicate_raises(self, tmp_path: Path) -> None:
        scaffold_local_artifact("rule", "dup", tmp_path)
        with pytest.raises(ValueError, match="already exists"):
            scaffold_local_artifact("rule", "dup", tmp_path)

    def test_project_without_dir_raises(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="project_dir required"):
            scaffold_local_artifact("rule", "r1", tmp_path, project=True)


class TestMemoryScopeDerivation:
    """Verify that load_local_artifacts derives FQN/namespace/metadata for memory
    artifacts based on which discovery root produced them."""

    def test_global_root_produces_user_scope(self, db: ThreadSafeConnection, tmp_path: Path) -> None:
        memories = tmp_path / _LOCAL_DIR / "memories"
        memories.mkdir(parents=True)
        (memories / "my-pref.md").write_text("I prefer dark mode")
        load_local_artifacts(db, tmp_path)
        row = db.execute("SELECT * FROM artifacts WHERE name = 'my-pref'").fetchone()
        assert row is not None
        assert row["namespace"] == "user"
        assert row["fqn"] == "@user/memory/my-pref"
        import json

        meta = json.loads(row["metadata"])
        assert meta["memory_scope"] == "user"
        assert meta["memory_category"] == "project_fact"
        assert meta["memory_status"] == "active"

    def test_project_root_produces_project_scope(self, db: ThreadSafeConnection, tmp_path: Path) -> None:
        proj = tmp_path / "myproject"
        memories = proj / ".anteroom" / _LOCAL_DIR / "memories"
        memories.mkdir(parents=True)
        (memories / "proj-note.md").write_text("project uses postgres")
        load_local_artifacts(db, tmp_path, project_dir=proj)
        row = db.execute("SELECT * FROM artifacts WHERE name = 'proj-note'").fetchone()
        assert row is not None
        assert row["namespace"] == "project"
        assert row["fqn"] == "@project/memory/proj-note"
        import json

        meta = json.loads(row["metadata"])
        assert meta["memory_scope"] == "project"

    def test_space_root_produces_local_scope(self, db: ThreadSafeConnection, tmp_path: Path) -> None:
        space = tmp_path / "myspace"
        memories = space / ".anteroom" / _LOCAL_DIR / "memories"
        memories.mkdir(parents=True)
        (memories / "space-note.md").write_text("space-local note")
        load_local_artifacts(db, tmp_path, space_dirs=[space])
        row = db.execute("SELECT * FROM artifacts WHERE name = 'space-note'").fetchone()
        assert row is not None
        assert row["namespace"] == "local"
        assert row["fqn"] == "@local/memory/space-note"
        import json

        meta = json.loads(row["metadata"])
        assert meta["memory_scope"] == "local"

    def test_non_memory_types_unchanged(self, db: ThreadSafeConnection, tmp_path: Path) -> None:
        """Rules from global root should still use @local namespace."""
        rules = tmp_path / _LOCAL_DIR / "rules"
        rules.mkdir(parents=True)
        (rules / "my-rule.md").write_text("a rule")
        load_local_artifacts(db, tmp_path)
        row = db.execute("SELECT * FROM artifacts WHERE name = 'my-rule'").fetchone()
        assert row is not None
        assert row["namespace"] == "local"
        assert row["fqn"] == "@local/rule/my-rule"

    def test_memory_metadata_has_all_fields(self, db: ThreadSafeConnection, tmp_path: Path) -> None:
        memories = tmp_path / _LOCAL_DIR / "memories"
        memories.mkdir(parents=True)
        (memories / "full-check.md").write_text("checking metadata fields")
        load_local_artifacts(db, tmp_path)
        row = db.execute("SELECT * FROM artifacts WHERE name = 'full-check'").fetchone()
        import json

        meta = json.loads(row["metadata"])
        assert "memory_scope" in meta
        assert "memory_category" in meta
        assert "memory_status" in meta
        assert "provenance" in meta
        assert "created_by" in meta
        assert "last_recalled_at" in meta
        assert "recall_count" in meta
        assert meta["recall_count"] == 0


class TestLocalArtifactBundledSkills:
    def test_discover_bundled_skill(self, tmp_path: Path) -> None:
        skills_dir = tmp_path / "skills"
        skill_dir = skills_dir / "deploy"
        skill_dir.mkdir(parents=True)
        skill_content = (
            "---\nname: deploy\ndescription: Deploy skill\nresources:\n  - data.md\n---\n\nDeploy the thing.\n"
        )
        (skill_dir / "SKILL.md").write_text(skill_content, encoding="utf-8")
        (skill_dir / "data.md").write_text("## Deploy data\nsome content\n", encoding="utf-8")

        result = discover_local_artifacts(tmp_path)
        skills = [a for a in result if a["type"] == "skill"]
        assert len(skills) == 1
        art = skills[0]
        assert "<bundled_resources>" in art["content"]
        assert '<resource path="data.md">' in art["content"]
        meta = art.get("metadata", {})
        assert meta.get("bundle") is True
        assert meta.get("resource_count") == 1

    def test_discover_skill_no_resources(self, tmp_path: Path) -> None:
        skills_dir = tmp_path / "skills"
        skill_dir = skills_dir / "greet"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("---\nname: greet\n---\n\nSay hello.\n", encoding="utf-8")

        result = discover_local_artifacts(tmp_path)
        skills = [a for a in result if a["type"] == "skill"]
        assert len(skills) == 1
        art = skills[0]
        assert "<bundled_resources>" not in art["content"]
        meta = art.get("metadata", {})
        assert not meta.get("bundle")
