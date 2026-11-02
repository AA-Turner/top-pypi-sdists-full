"""Tests for audit_prepare_command()."""

import json
import os
import sys
from unittest.mock import patch

import pytest

from agentic_devtools.cli.audit.commands import audit_prepare_command
from agentic_devtools.cli.audit.models import AuditBatch


class TestAuditPrepareCommand:
    """Tests for the audit_prepare_command CLI entry point."""

    def test_prints_batch_json(self, capsys) -> None:
        batch = AuditBatch(
            batch_id="batch-123",
            created_at="2024-01-15T10:00:00Z",
            status="ready",
            pr_numbers=[3, 5],
            output_dir="/workspace/audit-batches/batch-123",
        )

        with (
            patch.object(
                sys,
                "argv",
                ["agdt-audit-prepare", "--batch-size", "2", "--repo", "owner/from-arg"],
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
                "agentic_devtools.cli.audit.prepare.prepare_audit_batch",
                return_value=batch,
            ) as mock_prepare,
        ):
            audit_prepare_command()

        mock_resolve.assert_called_once_with("owner/from-arg")
        mock_provider_cls.assert_called_once_with(repo="owner/from-arg")
        mock_prepare.assert_called_once_with(
            mock_provider_cls.return_value,
            2,
            "/workspace/from-env",
        )
        assert json.loads(capsys.readouterr().out) == {
            "batch_id": "batch-123",
            "status": "ready",
            "pr_count": 2,
            "pr_numbers": [3, 5],
            "output_dir": "/workspace/audit-batches/batch-123",
        }

    def test_exits_one_when_preparation_fails(self) -> None:
        with (
            patch.object(sys, "argv", ["agdt-audit-prepare"]),
            patch.dict(os.environ, {"GITHUB_REPOSITORY": "owner/from-env"}, clear=True),
            patch(
                "agentic_devtools.cli.audit.commands.resolve_github_repo",
                return_value="owner/from-env",
            ) as mock_resolve,
            patch(
                "agentic_devtools.cli.ci.github_provider.GitHubActionsProvider",
            ) as mock_provider_cls,
            patch(
                "agentic_devtools.cli.audit.prepare.prepare_audit_batch",
                side_effect=RuntimeError("boom"),
            ),
            patch("os.getcwd", return_value="/cwd/fallback"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                audit_prepare_command()

        assert exc_info.value.code == 1
        mock_resolve.assert_called_once_with("owner/from-env")
        mock_provider_cls.assert_called_once_with(repo="owner/from-env")
