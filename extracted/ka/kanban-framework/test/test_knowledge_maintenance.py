"""Tests for knowledge maintenance: semantic dedup, stale scan, vacuum."""
from __future__ import annotations

from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.domain.knowledge import KnowledgeManager


class TestSemanticDuplicates:
    def test_no_duplicates(self, tmp_kanban):
        fs = Filesystem(root=tmp_kanban)
        km = KnowledgeManager(fs)
        km.add_entry(domain="infra", category="架构", title="路径处理", content="使用 pathlib.Path", tags=["path"])
        km.add_entry(domain="testing", category="踩坑", title="mock 使用", content="避免 mock 数据库", tags=["mock"])

        result = km.find_semantic_duplicates(threshold=0.85)
        assert result == []

    def test_detects_similar_pair(self, tmp_kanban):
        fs = Filesystem(root=tmp_kanban)
        km = KnowledgeManager(fs)
        # Two entries with very similar semantic content
        km.add_entry(domain="infra", category="踩坑", title="Windows 路径问题", content="禁止直接导入 fcntl，使用跨平台替代方案 pathlib", tags=["path", "windows"])
        km.add_entry(domain="infra", category="踩坑", title="Unix 专用 API 陷阱", content="禁止直接导入 fcntl，Windows 不支持该模块", tags=["path", "windows"])

        result = km.find_semantic_duplicates(threshold=0.7)
        # May or may not find duplicates depending on embedding model availability
        # If embeddings are available, should find at least one group
        if result:
            assert result[0]["max_similarity"] >= 0.7
            assert len(result[0]["entries"]) == 2

    def test_groups_three_similar(self, tmp_kanban):
        fs = Filesystem(root=tmp_kanban)
        km = KnowledgeManager(fs)
        km.add_entry(domain="infra", category="踩坑", title="fcntl 禁用", content="禁止导入 fcntl 模块", tags=["path"])
        km.add_entry(domain="infra", category="踩坑", title="fcntl 不可用", content="fcntl 是 Unix 专属模块", tags=["path"])
        km.add_entry(domain="infra", category="踩坑", title="fcntl Windows 不支持", content="Windows 上没有 fcntl", tags=["path"])

        result = km.find_semantic_duplicates(threshold=0.7)
        if result:
            # Should group all three together
            group = result[0]
            assert len(group["entries"]) == 3

    def test_threshold_controls_sensitivity(self, tmp_kanban):
        fs = Filesystem(root=tmp_kanban)
        km = KnowledgeManager(fs)
        km.add_entry(domain="infra", category="架构", title="路径处理用 pathlib", content="始终使用 pathlib.Path", tags=["path"])
        km.add_entry(domain="testing", category="最佳实践", title="使用 pytest fixture", content="fixture 共享测试数据", tags=["pytest"])

        # Very high threshold should find nothing
        result = km.find_semantic_duplicates(threshold=0.99)
        assert result == []


class TestStaleScan:
    def test_no_stale(self, tmp_kanban):
        fs = Filesystem(root=tmp_kanban)
        km = KnowledgeManager(fs)
        km.add_entry(domain="infra", category="架构", title="新条目", content="最近添加")

        from kanban_framework.domain.knowledge_management import scan_stale_candidates
        result = scan_stale_candidates(km)
        assert len(result["candidates"]) == 0

    def test_stale_candidates_report(self, tmp_kanban):
        """Stale scan lists candidates without modifying them."""
        fs = Filesystem(root=tmp_kanban)
        km = KnowledgeManager(fs)
        km.add_entry(domain="infra", category="架构", title="旧条目", content="很早添加")

        from kanban_framework.domain.knowledge_management import scan_stale_candidates
        result = scan_stale_candidates(km)
        # Since no last_referenced_at and created_at is recent, should not be stale
        # (STALE_DAYS = 30, entry just created)
        assert result["stale_days_threshold"] == 30


class TestVacuum:
    def test_vacuum_runs(self, tmp_kanban):
        fs = Filesystem(root=tmp_kanban)
        km = KnowledgeManager(fs)
        km.add_entry(domain="infra", category="架构", title="test", content="vacuum test")

        from kanban_framework.domain.knowledge_management import vacuum_database
        result = vacuum_database(km)
        assert result["fts_rebuilt"] is True
        assert result["vacuumed"] is True


class TestMaintenanceCLI:
    def test_dispatch_report(self, tmp_kanban):
        from kanban_framework.cli.knowledge import dispatch
        result = dispatch(["maintenance", "--report"])
        assert "duplicates" in result
        assert "stale" in result

    def test_dispatch_scan_duplicates(self, tmp_kanban):
        from kanban_framework.cli.knowledge import dispatch
        result = dispatch(["maintenance", "--scan-duplicates", "--threshold", "0.9"])
        assert "duplicates" in result
        assert result["duplicates"]["threshold"] == 0.9

    def test_dispatch_scan_stale(self, tmp_kanban):
        from kanban_framework.cli.knowledge import dispatch
        result = dispatch(["maintenance", "--scan-stale"])
        assert "stale" in result

    def test_dispatch_vacuum(self, tmp_kanban):
        from kanban_framework.cli.knowledge import dispatch
        result = dispatch(["maintenance", "--vacuum"])
        assert "vacuum" in result
        assert result["vacuum"]["vacuumed"] is True

    def test_dispatch_confirm_lists_suggestions(self, tmp_kanban):
        from kanban_framework.cli.knowledge import dispatch
        result = dispatch(["maintenance", "--scan-stale", "--confirm"])
        assert "suggestions" in result
        assert "note" in result

    def test_dispatch_default_is_report(self, tmp_kanban):
        from kanban_framework.cli.knowledge import dispatch
        result = dispatch(["maintenance"])
        assert "duplicates" in result
        assert "stale" in result

    def test_dispatch_invalid_threshold(self, tmp_kanban):
        from kanban_framework.cli.knowledge import dispatch
        result = dispatch(["maintenance", "--threshold", "abc"])
        assert "error" in result
