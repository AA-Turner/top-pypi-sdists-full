"""Tests for audit_dispatch_evaluation_command()."""

import json
import os
import sys
from unittest.mock import patch

import pytest

from agentic_devtools.cli.audit.commands import audit_dispatch_evaluation_command


class TestAuditDispatchEvaluationCommand:
    """Tests for the audit dispatch CLI entry point."""

    def test_prints_dispatch_json(self, capsys) -> None:
        dispatch_result = {
            "batch_id": "batch-123",
            "tracking_issue": 2042,
            "batch_branch": "audit/batch-batch123",
            "dispatch_method": "coding_agent_task",
            "dispatch_task_id": "task-77",
            "dispatch_task_url": "https://example/task-77",
            "batch_meta_path": "audit-batches/batch-123/batch-meta.json",
        }

        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-audit-dispatch-evaluation",
                    "--batch-id",
                    "batch-123",
                    "--output-dir",
                    "/workspace/audit-batches/batch-123",
                    "--pr-numbers",
                    "1, 2,3",
                    "--repo",
                    "owner/from-arg",
                ],
            ),
            patch.dict(os.environ, {"GITHUB_WORKSPACE": "/workspace/from-env"}, clear=True),
            patch(
                "agentic_devtools.cli.audit.commands.resolve_github_repo",
                return_value="owner/from-arg",
            ) as mock_resolve,
            patch(
                "agentic_devtools.cli.ci.github_provider.GitHubActionsProvider",
            ) as mock_provider_cls,
            patch(
                "agentic_devtools.cli.audit.dispatch.dispatch_audit_evaluation",
                return_value=dispatch_result,
            ) as mock_dispatch,
        ):
            audit_dispatch_evaluation_command()

        mock_resolve.assert_called_once_with("owner/from-arg")
        mock_provider_cls.assert_called_once_with(repo="owner/from-arg")
        mock_dispatch.assert_called_once_with(
            provider=mock_provider_cls.return_value,
            batch_id="batch-123",
            output_dir="/workspace/audit-batches/batch-123",
            pr_numbers=[1, 2, 3],
            repo_path="/workspace/from-env",
            github_repo="owner/from-arg",
        )
        assert json.loads(capsys.readouterr().out) == dispatch_result

    def test_exits_one_when_dispatch_fails(self) -> None:
        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-audit-dispatch-evaluation",
                    "--batch-id",
                    "batch-123",
                    "--output-dir",
                    "/workspace/audit-batches/batch-123",
                    "--pr-numbers",
                    "1,2,3",
                ],
            ),
            patch.dict(os.environ, {"GITHUB_REPOSITORY": "owner/from-env"}, clear=True),
            patch(
                "agentic_devtools.cli.audit.commands.resolve_github_repo",
                return_value="owner/from-env",
            ),
            patch(
                "agentic_devtools.cli.ci.github_provider.GitHubActionsProvider",
            ),
            patch(
                "agentic_devtools.cli.audit.dispatch.dispatch_audit_evaluation",
                side_effect=RuntimeError("boom"),
            ),
            patch("os.getcwd", return_value="/cwd/fallback"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                audit_dispatch_evaluation_command()

        assert exc_info.value.code == 1
