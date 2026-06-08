"""Tests for sage.core.memory — persistent project + user memory.

Sage starts cold every session. This module lets the agent persist facts
(user preferences, project conventions, ongoing initiatives) to disk and
re-load them in future sessions so it doesn't re-explore the codebase
from scratch each conversation.

Storage layout under `<root>/memory/`:
  MEMORY.md             — index, one line per memory: `- [Title](file.md) — hook`
  <slug>.md             — individual memories with YAML frontmatter

Memory types match Claude Code's auto-memory conventions:
  - "user":    role, preferences, knowledge level
  - "feedback": guidance the user has given about how to work
  - "project": ongoing initiatives, decisions, deadlines
  - "reference": pointers to external systems (Linear, Slack, Grafana)
"""

from __future__ import annotations

from pathlib import Path

import pytest


# ── Saving + loading ─────────────────────────────────────────────────────


class TestSaveAndLoad:

    def test_save_creates_file_with_frontmatter(self, tmp_path):
        from sage.core.memory import MemoryStore
        store = MemoryStore(tmp_path)
        store.save(
            name="user_role",
            description="user is a senior backend engineer focused on Python",
            type="user",
            content="The user has 10 years of Python experience and prefers terse responses.",
        )
        files = list((tmp_path / "memory").glob("*.md"))
        # MEMORY.md + the new memory file
        names = {f.name for f in files}
        assert "MEMORY.md" in names
        assert any(n.startswith("user_role") for n in names)

    def test_saved_file_contains_frontmatter_and_body(self, tmp_path):
        from sage.core.memory import MemoryStore
        store = MemoryStore(tmp_path)
        store.save(
            name="ts_preferred",
            description="user prefers TypeScript over JavaScript",
            type="user",
            content="Whenever stack choice is ambiguous, choose TypeScript.",
        )
        memory_file = next((tmp_path / "memory").glob("ts_preferred*.md"))
        text = memory_file.read_text()
        assert text.startswith("---")
        assert "name: ts_preferred" in text
        assert "type: user" in text
        assert "description:" in text
        assert "Whenever stack choice is ambiguous" in text

    def test_load_returns_saved_memory(self, tmp_path):
        from sage.core.memory import MemoryStore
        store = MemoryStore(tmp_path)
        store.save(
            name="incident_timeout",
            description="prior incident — session timeouts",
            type="feedback",
            content="Don't mock auth in integration tests; we got burned in Q3.",
        )
        loaded = store.load_all()
        assert len(loaded) == 1
        assert loaded[0].name == "incident_timeout"
        assert loaded[0].type == "feedback"
        assert "Don't mock auth" in loaded[0].content

    def test_memory_index_updated_after_save(self, tmp_path):
        from sage.core.memory import MemoryStore
        store = MemoryStore(tmp_path)
        store.save(name="a", description="memory A", type="user", content="alpha")
        store.save(name="b", description="memory B", type="project", content="beta")
        index = (tmp_path / "memory" / "MEMORY.md").read_text()
        # Both entries appear in the index
        assert "memory A" in index or "[a]" in index
        assert "memory B" in index or "[b]" in index


# ── Filtering + deleting ─────────────────────────────────────────────────


class TestFilterAndDelete:

    def test_list_filters_by_type(self, tmp_path):
        from sage.core.memory import MemoryStore
        store = MemoryStore(tmp_path)
        store.save(name="u1", description="user fact", type="user", content="x")
        store.save(name="p1", description="project fact", type="project", content="y")
        store.save(name="f1", description="feedback fact", type="feedback", content="z")
        users = store.load_all(type_filter="user")
        assert len(users) == 1
        assert users[0].name == "u1"

    def test_delete_removes_file(self, tmp_path):
        from sage.core.memory import MemoryStore
        store = MemoryStore(tmp_path)
        store.save(name="tmp", description="d", type="user", content="x")
        assert any(f.name.startswith("tmp") for f in (tmp_path / "memory").iterdir())
        store.delete("tmp")
        files = list((tmp_path / "memory").iterdir())
        memory_files = [f for f in files if f.name != "MEMORY.md"]
        assert all(not f.name.startswith("tmp") for f in memory_files)


# ── Prompt integration ───────────────────────────────────────────────────


class TestFormatForPrompt:

    def test_empty_memory_produces_empty_section(self, tmp_path):
        from sage.core.memory import MemoryStore
        store = MemoryStore(tmp_path)
        out = store.format_for_prompt()
        # Empty memory → empty string, not a confusing header with nothing under it
        assert out == ""

    def test_with_memories_produces_markdown_section(self, tmp_path):
        from sage.core.memory import MemoryStore
        store = MemoryStore(tmp_path)
        store.save(name="lang", description="prefers TypeScript",
                   type="user", content="Use TypeScript when stack is ambiguous.")
        store.save(name="freeze", description="merge freeze starts March 5",
                   type="project", content="No non-critical merges after 2026-03-05.")
        out = store.format_for_prompt()
        # Section has a header and lists both entries
        assert "MEMORY" in out.upper() or "## " in out
        assert "TypeScript" in out
        assert "merge freeze" in out.lower()

    def test_format_limits_total_length(self, tmp_path):
        """The formatted section should respect a token budget so we don't
        blow up the prompt with stale memories."""
        from sage.core.memory import MemoryStore
        store = MemoryStore(tmp_path)
        # 100 memories with long content
        for i in range(100):
            store.save(
                name=f"mem{i:03d}",
                description=f"memory {i}",
                type="user",
                content="X" * 500,
            )
        out = store.format_for_prompt(max_chars=4000)
        assert len(out) <= 4000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
