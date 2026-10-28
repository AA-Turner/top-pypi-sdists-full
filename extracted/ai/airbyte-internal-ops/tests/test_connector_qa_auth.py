# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Caller Cloud authentication for regression-test workspace validation."""

from __future__ import annotations

from typing import Any, cast
from unittest.mock import Mock

import pytest
from airbyte.exceptions import PyAirbyteSecretNotFoundError
from fastmcp import Context

from airbyte_ops_mcp.cloud_admin.version_overrides import ResolvedCloudAuth
from airbyte_ops_mcp.github_actions import WorkflowDispatchResult
from airbyte_ops_mcp.mcp import connector_qa
from airbyte_ops_mcp.mcp.connector_qa import (
    ConnectorRepo,
    RunRegressionTestsResponse,
    run_regression_tests,
)
from airbyte_ops_mcp.mcp.connector_qa import (
    TestRunStatus as RegressionTestStatus,
)


def _run_tool(*, ctx: Context, **kwargs: Any) -> RunRegressionTestsResponse:
    return run_regression_tests(
        connector_name="source-pokeapi",
        pr=1,
        repo=ConnectorRepo.AIRBYTE,
        ctx=ctx,
        **kwargs,
    )


def _stub_workflow_dispatch(
    monkeypatch: pytest.MonkeyPatch,
    dispatch: Mock,
) -> None:
    monkeypatch.setattr(
        connector_qa, "resolve_ci_trigger_github_token", lambda: "token"
    )
    monkeypatch.setattr(connector_qa, "trigger_workflow_dispatch", dispatch)


def _dispatch_result() -> WorkflowDispatchResult:
    return WorkflowDispatchResult(workflow_url="https://example.com/workflow")


def test_run_regression_tests_uses_caller_bearer_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("AIRBYTE_CLOUD_CLIENT_ID", raising=False)
    monkeypatch.delenv("AIRBYTE_CLOUD_CLIENT_SECRET", raising=False)
    cloud_workspace = Mock()
    connection = Mock()
    cloud_workspace.return_value.get_connection.return_value = connection
    monkeypatch.setattr(connector_qa, "CloudWorkspace", cloud_workspace)
    monkeypatch.setattr(
        connector_qa,
        "resolve_cloud_auth",
        lambda _ctx: ResolvedCloudAuth(bearer_token="caller-token"),
    )
    dispatch = Mock(return_value=_dispatch_result())
    _stub_workflow_dispatch(monkeypatch, dispatch)

    _run_tool(
        ctx=cast(Context, object()),
        connection_id="connection-id",
        workspace_id="workspace-id",
    )

    cloud_workspace.assert_called_once_with(
        workspace_id="workspace-id",
        client_id=None,
        client_secret=None,
        bearer_token="caller-token",
    )
    connection.check_is_valid.assert_called_once_with()
    dispatch.assert_called_once()


@pytest.mark.parametrize("return_empty_auth", [True, False])
def test_run_regression_tests_without_credentials_does_not_dispatch(
    monkeypatch: pytest.MonkeyPatch,
    return_empty_auth: bool,
) -> None:
    monkeypatch.delenv("AIRBYTE_CLOUD_CLIENT_ID", raising=False)
    monkeypatch.delenv("AIRBYTE_CLOUD_CLIENT_SECRET", raising=False)
    if return_empty_auth:
        monkeypatch.setattr(
            connector_qa,
            "resolve_cloud_auth",
            lambda _ctx: ResolvedCloudAuth(),
        )
    else:
        monkeypatch.setattr(
            connector_qa,
            "resolve_cloud_auth",
            Mock(
                side_effect=PyAirbyteSecretNotFoundError(
                    secret_name="AIRBYTE_CLOUD_CLIENT_ID"
                )
            ),
        )
    dispatch = Mock(return_value=_dispatch_result())
    _stub_workflow_dispatch(monkeypatch, dispatch)

    response = _run_tool(
        ctx=cast(Context, object()),
        connection_id="connection-id",
        workspace_id="workspace-id",
    )

    assert response.status == RegressionTestStatus.FAILED
    assert "Authorization bearer token" in response.message
    assert "X-Airbyte-Cloud-Client-Id" in response.message
    assert "AIRBYTE_CLOUD_CLIENT_ID" in response.message
    assert response.workflow_url is None
    dispatch.assert_not_called()


def test_run_regression_tests_without_workspace_does_not_resolve_auth(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("AIRBYTE_CLOUD_CLIENT_ID", raising=False)
    monkeypatch.delenv("AIRBYTE_CLOUD_CLIENT_SECRET", raising=False)
    monkeypatch.setattr(
        connector_qa,
        "resolve_cloud_auth",
        Mock(side_effect=AssertionError("Cloud auth should not be resolved")),
    )
    dispatch = Mock(return_value=_dispatch_result())
    _stub_workflow_dispatch(monkeypatch, dispatch)

    response = _run_tool(
        ctx=cast(Context, object()),
        connection_id="connection-id",
    )

    assert response.status == RegressionTestStatus.QUEUED
    dispatch.assert_called_once()
