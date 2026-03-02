# mypy: disable-error-code="attr-defined,return-value,no-untyped-def"
from __future__ import annotations

from types import SimpleNamespace

import pytest
from polars_cloud import Workspace
from polars_cloud.exceptions import WorkspaceResolveError


@pytest.mark.usefixtures("_mock_workspace_by_default")
def test_get_default_workspace(workspace_id, workspace_name) -> None:
    w = Workspace()
    assert w.name == workspace_name
    assert w.id == workspace_id


@pytest.mark.usefixtures(
    "_mock_workspace_by_default_no_access", "_mock_workspace_details"
)
def test_get_default_workspace_no_access() -> None:
    with pytest.raises(
        WorkspaceResolveError,
        match=r"The workspace you had set as default either does not exist anymore",
    ):
        Workspace()


@pytest.mark.usefixtures(
    "_mock_workspace_details", "_mock_user_without_default_workspace"
)
def test_err_get_default_workspace() -> None:
    with pytest.raises(
        WorkspaceResolveError, match=r"No \(default\) workspace specified"
    ):
        Workspace()


@pytest.mark.usefixtures("_mock_workspace_by_name")
def test_get_workspace_by_name(workspace_name, workspace_id) -> None:
    w = Workspace(name=workspace_name)
    assert w.name == workspace_name
    assert w.id == workspace_id


@pytest.mark.usefixtures("_mock_workspace_by_name")
def test_err_get_workspace_by_name() -> None:
    name = "DOES NOT EXIST"
    with pytest.raises(
        WorkspaceResolveError, match=f"Workspace {name!r} does not exist"
    ):
        Workspace(name=name)


@pytest.mark.usefixtures("_mock_workspace_by_id")
def test_get_workspace_by_id(
    organization_id, workspace_id, workspace_name, workspace_status
) -> None:
    w = Workspace(id=workspace_id)
    assert w.id == workspace_id
    assert w.organization.id == organization_id
    assert w.name == workspace_name
    assert w.status == workspace_status


def test_err_duplicate_workspace_names_on_single_account(
    mock_api_client,
    workspace_id,
    workspace_name,
    workspace_rust_status,
) -> None:
    def get_workspaces(name: str):
        mock_workspace = SimpleNamespace()
        mock_workspace.id = str(workspace_id)
        mock_workspace.name = workspace_name
        mock_workspace.status = workspace_rust_status
        mock_get_workspaces = [mock_workspace, mock_workspace]

        return [w for w in mock_get_workspaces if w.name.startswith(name)]

    mock_api_client.get_workspaces = get_workspaces

    with pytest.raises(
        WorkspaceResolveError, match=r"Multiple workspaces with the same name"
    ):
        Workspace(name=workspace_name)
