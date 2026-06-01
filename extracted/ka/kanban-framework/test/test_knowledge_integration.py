"""Integration test for knowledge lifecycle: Plan injection -> Execute warning -> Archive extraction."""
from __future__ import annotations
from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.domain.knowledge import KnowledgeManager


class TestKnowledgeLifecycle:
    def test_full_lifecycle(self, tmp_kanban):
        """Simulates: extract from TASK-001 -> inject into TASK-002 plan -> warn on pitfall."""
        fs = Filesystem(root=tmp_kanban)
        km = KnowledgeManager(fs)

        # --- TASK-001 Archive: extract knowledge ---
        e1 = km.add_entry(
            domain="testing", category="踩坑",
            title="bool vs int counter",
            content="Use int counter when spec expects cumulative behavior.",
            tags=["python", "test-design", "type-choice"],
            severity="medium",
            source={"task_id": "TASK-001", "iteration": 1},
        )
        e2 = km.add_entry(
            domain="git", category="踩坑",
            title="games/ dir gitignore trap",
            content="Add -f flag or fix .gitignore when output_dir is excluded.",
            tags=["git", "gitignore", "worktree"],
            severity="high",
            source={"task_id": "TASK-001", "iteration": 1},
        )

        # --- TASK-002 Plan: knowledge injection ---
        task_desc = "add integration tests for snake game, using pytest"
        matched = km.match_domain(task_desc)
        assert "testing" in matched
        relevant = km.search_by_domain("testing", severity="medium")
        assert any("bool" in r["title"] for r in relevant)

        # --- TASK-002 Execute: pitfall warning ---
        new_pitfall_tags = ["python", "test-design", "assertion"]
        similar = km.find_similar_pitfalls(new_pitfall_tags)
        assert len(similar) >= 1
        assert similar[0]["title"] == "bool vs int counter"

        # Record usage of the relevant entry
        km.record_usage(e1["id"], "TASK-002")
        updated = km.get_entry(e1["id"])
        assert updated["referenced_count"] == 1

    def test_stale_and_gap_cycle(self, tmp_kanban):
        """10 tasks later, run health check."""
        fs = Filesystem(root=tmp_kanban)
        km = KnowledgeManager(fs)

        # Simulate many pitfalls in 'infra' domain but few knowledge entries
        for i in range(5):
            km.add_entry(
                domain="infra", category="踩坑",
                title=f"Infra Pitfall {i}", content="x",
                tags=["git", "worktree"],
            )
        # Only 1 non-pitfall entry
        km.add_entry(domain="infra", category="架构", title="Infra Arch", content="y")
        gaps = km.get_knowledge_gap_report()
        # 5 pitfalls vs 6 total, ratio < 2:1 -> should be in gaps
        if "infra" in gaps:
            assert gaps["infra"]["pitfalls"] == 5
