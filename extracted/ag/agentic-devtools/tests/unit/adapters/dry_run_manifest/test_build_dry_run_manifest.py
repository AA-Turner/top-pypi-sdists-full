"""Tests for build_dry_run_manifest utility."""

from __future__ import annotations

from agentic_devtools.adapters.dry_run_manifest import build_dry_run_manifest


class TestBuildDryRunManifest:
    """Verify dry-run manifest builder."""

    def test_empty_manifest(self):
        result = build_dry_run_manifest(issues=[], dependencies=[])
        assert result == {"issues": [], "dependencies": []}

    def test_manifest_with_issues(self):
        issues = [
            {"title": "Epic", "issue_type": "epic", "operation": "POST /issues", "status": "dry-run"},
            {"title": "Story", "issue_type": "story", "operation": "POST /issues", "status": "dry-run"},
        ]
        result = build_dry_run_manifest(issues=issues, dependencies=[])
        assert len(result["issues"]) == 2
        assert result["issues"][0]["title"] == "Epic"

    def test_manifest_with_dependencies(self):
        deps = [
            {"source": "A", "target": "B", "type": "blocks", "operation": "POST /graphql", "status": "dry-run"},
        ]
        result = build_dry_run_manifest(issues=[], dependencies=deps)
        assert len(result["dependencies"]) == 1
        assert result["dependencies"][0]["source"] == "A"

    def test_manifest_with_nested_children(self):
        issues = [
            {
                "title": "Epic",
                "issue_type": "epic",
                "operation": "POST /issues",
                "status": "dry-run",
                "children": [
                    {"title": "Child", "issue_type": "story", "operation": "POST /issues", "status": "dry-run"},
                ],
            },
        ]
        result = build_dry_run_manifest(issues=issues, dependencies=[])
        assert result["issues"][0]["children"][0]["title"] == "Child"

    def test_manifest_preserves_all_fields(self):
        issues = [{"title": "X", "issue_type": "task", "operation": "POST", "status": "dry-run", "extra": "data"}]
        deps = [{"source": "A", "target": "B", "type": "blocks", "operation": "POST", "status": "dry-run"}]
        result = build_dry_run_manifest(issues=issues, dependencies=deps)
        assert result["issues"][0]["extra"] == "data"
