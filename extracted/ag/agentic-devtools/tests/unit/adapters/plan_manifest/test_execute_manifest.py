"""Tests for execute_manifest() convenience wrapper."""

from __future__ import annotations

from agentic_devtools.adapters.issue_provider import InMemoryIssueProvider
from agentic_devtools.adapters.plan_manifest import execute_manifest


class TestExecuteManifest:
    """Verify execute_manifest convenience wrapper."""

    def test_execute_manifest_creates_issues(self):
        """execute_manifest is a convenience wrapper for plan_manifest(dry_run=False)."""
        provider = InMemoryIssueProvider()
        manifest = {
            "nodes": [
                {"ref": "task-1", "title": "Task 1", "body": "Body 1", "issue_type": "task"},
                {"ref": "task-2", "title": "Task 2", "body": "Body 2", "issue_type": "task"},
            ]
        }

        plan = execute_manifest(manifest, provider)

        assert plan.dry_run is False
        assert plan.check_existing is False
        assert len(plan.create_operations) == 2
        assert all(op.status == "created" for op in plan.create_operations)
        assert len(provider.issues) == 2

    def test_execute_manifest_with_links(self):
        """execute_manifest handles parent-child links."""
        provider = InMemoryIssueProvider()
        manifest = {
            "nodes": [
                {"ref": "parent", "title": "Parent", "body": "P body", "issue_type": "feature"},
                {"ref": "child", "title": "Child", "body": "C body", "issue_type": "subtask", "parent_ref": "parent"},
            ]
        }

        plan = execute_manifest(manifest, provider)

        assert len(plan.link_operations) == 1
        assert plan.link_operations[0].status == "linked"
        assert len(provider.parent_child_links) == 1
