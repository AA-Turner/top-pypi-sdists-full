# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""The `run_bigquery_dbt_job` tool's workflow-dispatch contract."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from airbyte_ops_mcp.github_actions import (
    DEFAULT_WORKFLOW_BRANCH_OVERRIDE_ENV,
    WorkflowDispatchResult,
)
from airbyte_ops_mcp.mcp import github_ops
from airbyte_ops_mcp.mcp.data_ops import run_bigquery_dbt_job
from airbyte_ops_mcp.mcp.github_ops import (
    TriggerCIWorkflowResult,
)

pytestmark = pytest.mark.unit


def _dispatch(**kwargs: Any) -> tuple[TriggerCIWorkflowResult, MagicMock]:
    """Call the tool with workflow dispatch and token lookup stubbed."""
    with patch.object(
        github_ops, "trigger_workflow_dispatch"
    ) as mock_dispatch, patch.object(
        github_ops, "resolve_ci_trigger_github_token"
    ) as mock_resolve_token:
        mock_resolve_token.return_value = "test-token"
        mock_dispatch.return_value = WorkflowDispatchResult(
            workflow_url="https://github.com/airbytehq/airbyte-warehouse/actions/workflows/dbt-run-command.yml"
        )
        result = run_bigquery_dbt_job(
            wait_for_completion=False,
            **kwargs,
        )

    return result, mock_dispatch


def test_defaults_dispatch_all_operation_flags() -> None:
    result, mock_dispatch = _dispatch()

    assert result.success is True
    assert mock_dispatch.call_args is not None
    dispatch = mock_dispatch.call_args.kwargs
    assert dispatch["owner"] == "airbytehq"
    assert dispatch["repo"] == "airbyte-warehouse"
    assert dispatch["workflow_file"] == "dbt-run-command.yml"
    assert dispatch["ref"] == "main"
    assert dispatch["inputs"] == {
        "seed": "false",
        "run": "true",
        "snapshot": "false",
        "test": "false",
        "full_refresh": "false",
    }
    assert "pr" not in dispatch["inputs"]


def test_pr_dispatches_pr_input_but_keeps_main_workflow_ref() -> None:
    _, mock_dispatch = _dispatch(pr=3487)

    assert mock_dispatch.call_args is not None
    dispatch = mock_dispatch.call_args.kwargs
    assert dispatch["inputs"]["pr"] == "3487"
    assert dispatch["ref"] == "main"
    assert "comment-id" not in dispatch["inputs"]


def test_selectors_are_preserved_and_whitespace_only_values_are_omitted() -> None:
    multi_selector = (
        "resource_type:model,+opportunity_by_day resource_type:model,+opportunity"
    )
    _, mock_dispatch = _dispatch(select=multi_selector, exclude=" tag:ignored ")

    assert mock_dispatch.call_args is not None
    assert mock_dispatch.call_args.kwargs["inputs"] == {
        "seed": "false",
        "run": "true",
        "snapshot": "false",
        "test": "false",
        "full_refresh": "false",
        "select": multi_selector,
        "exclude": " tag:ignored ",
    }

    _, mock_dispatch = _dispatch(select=" \t ", exclude="\n ")
    assert mock_dispatch.call_args is not None
    assert mock_dispatch.call_args.kwargs["inputs"] == {
        "seed": "false",
        "run": "true",
        "snapshot": "false",
        "test": "false",
        "full_refresh": "false",
    }


def test_operation_flags_and_full_refresh_are_dispatched() -> None:
    _, mock_dispatch = _dispatch(
        seed=True, run=False, snapshot=True, test=True, full_refresh=True
    )

    assert mock_dispatch.call_args is not None
    assert mock_dispatch.call_args.kwargs["inputs"] == {
        "seed": "true",
        "run": "false",
        "snapshot": "true",
        "test": "true",
        "full_refresh": "true",
    }


def test_explicit_main_ref_ignores_default_branch_override(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(DEFAULT_WORKFLOW_BRANCH_OVERRIDE_ENV, "feature/workflows")

    _, mock_dispatch = _dispatch()

    assert mock_dispatch.call_args is not None
    assert mock_dispatch.call_args.kwargs["ref"] == "main"


def test_all_operations_disabled_raises_before_dispatch() -> None:
    with patch.object(
        github_ops, "trigger_workflow_dispatch"
    ) as mock_dispatch, patch.object(
        github_ops, "resolve_ci_trigger_github_token"
    ) as mock_resolve_token, pytest.raises(ValueError, match="At least one"):
        run_bigquery_dbt_job(
            seed=False,
            run=False,
            snapshot=False,
            test=False,
            wait_for_completion=False,
        )

    mock_dispatch.assert_not_called()
    mock_resolve_token.assert_not_called()


def test_nonpositive_pr_raises_before_dispatch() -> None:
    with patch.object(
        github_ops, "trigger_workflow_dispatch"
    ) as mock_dispatch, patch.object(
        github_ops, "resolve_ci_trigger_github_token"
    ) as mock_resolve_token, pytest.raises(
        ValueError, match="PR number must be a positive integer"
    ):
        run_bigquery_dbt_job(
            pr=0,
            wait_for_completion=False,
        )

    mock_dispatch.assert_not_called()
    mock_resolve_token.assert_not_called()
