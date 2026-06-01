# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for the `--override-level` dispatcher on the cloud connector CLI.

Covers:

- Validation errors raised by `_validate_override_scope_args` for each scope.
- Dispatch wiring: `set-version-override` and `clear-version-override` route
  to the correct core helper in
  `airbyte_ops_mcp.cloud_admin.version_overrides` for each `override_level`.
- Resolver-error handling for invalid `--actor-definition-id` values.
"""

from __future__ import annotations

from typing import Any, Literal
from unittest.mock import MagicMock, patch

import pytest
from airbyte.exceptions import PyAirbyteInputError

from airbyte_ops_mcp.cli import cloud as cloud_cli
from airbyte_ops_mcp.cloud_admin.version_overrides import ResolvedCloudAuth


def _build_actor_result(success: bool = True) -> MagicMock:
    """Mimic the `VersionOverrideOperationResult` returned by the actor helper."""
    result = MagicMock()
    result.success = success
    result.message = "actor scope ok"
    result.model_dump.return_value = {"success": success, "message": "actor scope ok"}
    return result


def _build_workspace_result(success: bool = True) -> MagicMock:
    """Mimic the `WorkspaceVersionOverrideResult` returned by the workspace helper."""
    result = MagicMock()
    result.success = success
    result.message = "workspace scope ok"
    result.model_dump.return_value = {
        "success": success,
        "message": "workspace scope ok",
    }
    return result


def _build_organization_result(success: bool = True) -> MagicMock:
    """Mimic the `OrganizationVersionOverrideResult` returned by the org helper."""
    result = MagicMock()
    result.success = success
    result.message = "organization scope ok"
    result.model_dump.return_value = {
        "success": success,
        "message": "organization scope ok",
    }
    return result


def _fake_auth() -> ResolvedCloudAuth:
    """Return a deterministic `ResolvedCloudAuth` for dispatcher tests."""
    return ResolvedCloudAuth(bearer_token="fake-token")


@pytest.mark.parametrize(
    ("kwargs", "expected_substring"),
    [
        pytest.param(
            {
                "override_level": "actor",
                "workspace_id": None,
                "organization_id": None,
                "connector_id": "c-1",
                "connector_type": "source",
                "actor_definition_id": None,
            },
            "Override level 'actor' requires --workspace-id",
            id="actor_missing_workspace_id",
        ),
        pytest.param(
            {
                "override_level": "actor",
                "workspace_id": "ws-1",
                "organization_id": None,
                "connector_id": "c-1",
                "connector_type": "source",
                "actor_definition_id": "def-1",
            },
            "must not be combined with --actor-definition-id",
            id="actor_with_actor_definition_id",
        ),
        pytest.param(
            {
                "override_level": "workspace",
                "workspace_id": "ws-1",
                "organization_id": None,
                "connector_id": None,
                "connector_type": None,
                "actor_definition_id": None,
            },
            "Override level 'workspace' requires --actor-definition-id",
            id="workspace_missing_actor_definition_id",
        ),
        pytest.param(
            {
                "override_level": "workspace",
                "workspace_id": "ws-1",
                "organization_id": None,
                "connector_id": "c-1",
                "connector_type": None,
                "actor_definition_id": "def-1",
            },
            "must not be combined with --connector-id or --connector-type",
            id="workspace_with_connector_id",
        ),
        pytest.param(
            {
                "override_level": "organization",
                "workspace_id": None,
                "organization_id": None,
                "connector_id": None,
                "connector_type": None,
                "actor_definition_id": "def-1",
            },
            "Override level 'organization' requires --organization-id",
            id="organization_missing_organization_id",
        ),
        pytest.param(
            {
                "override_level": "organization",
                "workspace_id": "ws-1",
                "organization_id": "org-1",
                "connector_id": None,
                "connector_type": None,
                "actor_definition_id": "def-1",
            },
            "must not be combined with --workspace-id",
            id="organization_with_workspace_id",
        ),
    ],
)
def test_validate_override_scope_args_exits_with_error(
    kwargs: dict[str, Any], expected_substring: str
) -> None:
    """Each scope rejects inconsistent argument combos with a clear message."""
    with patch.object(cloud_cli, "exit_with_error") as mock_exit:
        mock_exit.side_effect = SystemExit(1)
        with pytest.raises(SystemExit):
            cloud_cli._validate_override_scope_args(**kwargs)

    mock_exit.assert_called_once()
    assert expected_substring in mock_exit.call_args.args[0]


@pytest.mark.parametrize(
    ("override_level", "workspace_id", "organization_id"),
    [
        pytest.param("actor", "ws-1", None, id="actor_valid"),
        pytest.param("workspace", "ws-1", None, id="workspace_valid"),
        pytest.param("organization", None, "org-1", id="organization_valid"),
    ],
)
def test_validate_override_scope_args_accepts_valid_combos(
    override_level: Literal["actor", "workspace", "organization"],
    workspace_id: str | None,
    organization_id: str | None,
) -> None:
    """Valid scope-specific argument combos pass validation without raising."""
    if override_level == "actor":
        kwargs: dict[str, Any] = {
            "override_level": override_level,
            "workspace_id": workspace_id,
            "organization_id": None,
            "connector_id": "c-1",
            "connector_type": "source",
            "actor_definition_id": None,
        }
    elif override_level == "workspace":
        kwargs = {
            "override_level": override_level,
            "workspace_id": workspace_id,
            "organization_id": None,
            "connector_id": None,
            "connector_type": None,
            "actor_definition_id": "def-1",
        }
    else:
        kwargs = {
            "override_level": override_level,
            "workspace_id": None,
            "organization_id": organization_id,
            "connector_id": None,
            "connector_type": None,
            "actor_definition_id": "def-1",
        }
    with patch.object(cloud_cli, "exit_with_error") as mock_exit:
        cloud_cli._validate_override_scope_args(**kwargs)
    mock_exit.assert_not_called()


def test_dispatch_actor_scope_calls_actor_helper() -> None:
    """`override_level='actor'` dispatches to `set_actor_version_override`."""
    auth = _fake_auth()
    with patch.object(
        cloud_cli, "_resolve_cli_cloud_auth", return_value=auth
    ), patch.object(
        cloud_cli,
        "set_actor_version_override",
        return_value=_build_actor_result(),
    ) as mock_actor, patch.object(
        cloud_cli, "set_workspace_version_override"
    ) as mock_workspace, patch.object(
        cloud_cli, "set_organization_version_override"
    ) as mock_org, patch.object(
        cloud_cli, "resolve_definition_id_to_canonical_info"
    ) as mock_resolve:
        cloud_cli._dispatch_version_override(
            override_level="actor",
            workspace_id="ws-1",
            organization_id=None,
            connector_id="c-1",
            connector_type="source",
            actor_definition_id=None,
            version="1.0.0",
            unset=False,
            reason="needed for testing change",
            reason_url=None,
            issue_url="https://github.com/airbytehq/airbyte/issues/1",
            approval_comment_url="https://airbyte.slack.com/archives/X/p1234",
            ai_agent_session_url=None,
            customer_tier_filter="TIER_2",
        )

    mock_workspace.assert_not_called()
    mock_org.assert_not_called()
    mock_resolve.assert_not_called()
    mock_actor.assert_called_once()
    actor_kwargs = mock_actor.call_args.kwargs
    assert actor_kwargs["auth"] is auth
    assert actor_kwargs["workspace_id"] == "ws-1"
    assert actor_kwargs["actor_id"] == "c-1"
    assert actor_kwargs["actor_type"] == "source"
    assert actor_kwargs["version"] == "1.0.0"
    assert actor_kwargs["unset"] is False
    assert actor_kwargs["override_reason"] == "needed for testing change"
    assert actor_kwargs["customer_tier_filter"] == "TIER_2"


def test_dispatch_workspace_scope_calls_workspace_helper() -> None:
    """`override_level='workspace'` resolves the UUID and dispatches accordingly."""
    auth = _fake_auth()
    with patch.object(
        cloud_cli, "_resolve_cli_cloud_auth", return_value=auth
    ), patch.object(
        cloud_cli,
        "resolve_definition_id_to_canonical_info",
        return_value=("source-github", "source"),
    ) as mock_resolve, patch.object(
        cloud_cli, "set_actor_version_override"
    ) as mock_actor, patch.object(
        cloud_cli,
        "set_workspace_version_override",
        return_value=_build_workspace_result(),
    ) as mock_workspace, patch.object(
        cloud_cli, "set_organization_version_override"
    ) as mock_org:
        cloud_cli._dispatch_version_override(
            override_level="workspace",
            workspace_id="ws-1",
            organization_id=None,
            connector_id=None,
            connector_type=None,
            actor_definition_id="def-uuid",
            version="2.0.0",
            unset=False,
            reason="workspace pin reason text",
            reason_url=None,
            issue_url="https://github.com/airbytehq/airbyte/issues/2",
            approval_comment_url="https://airbyte.slack.com/archives/X/p1235",
            ai_agent_session_url=None,
            customer_tier_filter="TIER_2",
        )

    mock_actor.assert_not_called()
    mock_org.assert_not_called()
    mock_resolve.assert_called_once_with("def-uuid")
    mock_workspace.assert_called_once()
    ws_kwargs = mock_workspace.call_args.kwargs
    assert ws_kwargs["auth"] is auth
    assert ws_kwargs["workspace_id"] == "ws-1"
    assert ws_kwargs["connector_name"] == "source-github"
    assert ws_kwargs["connector_type"] == "source"
    assert ws_kwargs["version"] == "2.0.0"
    assert ws_kwargs["unset"] is False


def test_dispatch_organization_scope_clear_calls_org_helper() -> None:
    """`override_level='organization'` with `unset=True` clears via the org helper."""
    auth = _fake_auth()
    with patch.object(
        cloud_cli, "_resolve_cli_cloud_auth", return_value=auth
    ), patch.object(
        cloud_cli,
        "resolve_definition_id_to_canonical_info",
        return_value=("destination-bigquery", "destination"),
    ) as mock_resolve, patch.object(
        cloud_cli, "set_actor_version_override"
    ) as mock_actor, patch.object(
        cloud_cli, "set_workspace_version_override"
    ) as mock_workspace, patch.object(
        cloud_cli,
        "set_organization_version_override",
        return_value=_build_organization_result(),
    ) as mock_org:
        cloud_cli._dispatch_version_override(
            override_level="organization",
            workspace_id=None,
            organization_id="org-1",
            connector_id=None,
            connector_type=None,
            actor_definition_id="def-uuid",
            version=None,
            unset=True,
            reason=None,
            reason_url=None,
            issue_url="https://github.com/airbytehq/airbyte/issues/3",
            approval_comment_url="https://airbyte.slack.com/archives/X/p1236",
            ai_agent_session_url=None,
            customer_tier_filter="TIER_2",
        )

    mock_actor.assert_not_called()
    mock_workspace.assert_not_called()
    mock_resolve.assert_called_once_with("def-uuid")
    mock_org.assert_called_once()
    org_kwargs = mock_org.call_args.kwargs
    assert org_kwargs["auth"] is auth
    assert org_kwargs["organization_id"] == "org-1"
    assert org_kwargs["connector_name"] == "destination-bigquery"
    assert org_kwargs["connector_type"] == "destination"
    assert org_kwargs["version"] is None
    assert org_kwargs["unset"] is True


def test_dispatch_invalid_actor_definition_id_exits_cleanly() -> None:
    """An unresolvable `--actor-definition-id` surfaces as a CLI error, not a stack trace."""
    with patch.object(
        cloud_cli, "_resolve_cli_cloud_auth", return_value=_fake_auth()
    ), patch.object(
        cloud_cli,
        "resolve_definition_id_to_canonical_info",
        side_effect=PyAirbyteInputError(
            message="Could not find connector definition for actor_definition_id: bad-uuid",
        ),
    ), patch.object(
        cloud_cli, "set_workspace_version_override"
    ) as mock_workspace, patch.object(cloud_cli, "exit_with_error") as mock_exit:
        mock_exit.side_effect = SystemExit(2)
        with pytest.raises(SystemExit):
            cloud_cli._dispatch_version_override(
                override_level="workspace",
                workspace_id="ws-1",
                organization_id=None,
                connector_id=None,
                connector_type=None,
                actor_definition_id="bad-uuid",
                version="1.0.0",
                unset=False,
                reason="some reason text long enough",
                reason_url=None,
                issue_url="https://github.com/airbytehq/airbyte/issues/4",
                approval_comment_url="https://airbyte.slack.com/archives/X/p1237",
                ai_agent_session_url=None,
                customer_tier_filter="TIER_2",
            )

    mock_workspace.assert_not_called()
    mock_exit.assert_called_once()
    assert "Failed to resolve --actor-definition-id" in mock_exit.call_args.args[0]
