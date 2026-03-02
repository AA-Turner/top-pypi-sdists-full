# mypy: disable-error-code="attr-defined,return-value,no-untyped-def"
import uuid
from types import SimpleNamespace
from uuid import UUID, uuid4

import polars_cloud.polars_cloud as pcr
import pytest
from polars_cloud import WorkspaceStatus, constants


@pytest.fixture
def organization_id():
    return uuid4()


@pytest.fixture
def organization_name() -> str:
    return "MockedOrganization"


class MockedAPIClient:
    pass


@pytest.fixture
def mock_api_client(monkeypatch: pytest.MonkeyPatch):
    api_client = MockedAPIClient()
    monkeypatch.setattr(constants, "API_CLIENT", api_client)
    return api_client


@pytest.fixture
def _mock_get_organizations(mock_api_client, organization_id, organization_name):
    def get_organizations(name: str):
        mock = SimpleNamespace()
        mock.id = organization_id
        mock.name = organization_name
        mock_list = [mock]
        return [w for w in mock_list if w.name.startswith(name)]

    mock_api_client.get_organizations = get_organizations


@pytest.fixture
def _mock_organization_details(mock_api_client, organization_id, organization_name):  # noqa: ARG001
    def organization_details(organization_id: UUID):
        if organization_id == organization_id:
            mock = SimpleNamespace()
            mock.id = organization_id
            mock.name = organization_name
            return mock
        else:
            msg = "Organization not found"
            raise pcr.NotFoundError(msg)

    mock_api_client.get_organization = organization_details


@pytest.fixture
def workspace_name() -> str:
    return "MockedWorkspace"


@pytest.fixture
def workspace_id():
    return uuid4()


@pytest.fixture
def instance_type():
    return "t3.MOCKED"


@pytest.fixture
def workspace_rust_status():
    return pcr.WorkspaceStateSchema.Active


@pytest.fixture
def workspace_status():
    return WorkspaceStatus._from_api_schema(pcr.WorkspaceStateSchema.Active)


@pytest.fixture
def _mock_user_default_workspace(mock_api_client, workspace_id):
    def mock_user_schema_with_default():
        mocked_user_schema = SimpleNamespace()
        mocked_user_schema.default_workspace_id = workspace_id
        return mocked_user_schema

    mock_api_client.get_user = mock_user_schema_with_default


@pytest.fixture
def _mock_workspace_by_default_no_access(mock_api_client):
    def mock_user_schema_with_default():
        mocked_user_schema = SimpleNamespace()
        mocked_user_schema.default_workspace_id = uuid.uuid4()
        return mocked_user_schema

    mock_api_client.get_user = mock_user_schema_with_default


@pytest.fixture
def _mock_user_without_default_workspace(mock_api_client):
    def mock_user_schema_without_default():
        mocked_user_schema = SimpleNamespace()
        mocked_user_schema.default_workspace_id = None
        return mocked_user_schema

    mock_api_client.get_user = mock_user_schema_without_default


@pytest.fixture
def _mock_workspace_details(
    mock_api_client,
    organization_id,
    workspace_id,
    workspace_rust_status,
    workspace_name,
):
    def workspace_details(inner_workspace_id: UUID):
        if inner_workspace_id == workspace_id:
            mock_workspace = SimpleNamespace()
            mock_workspace.id = workspace_id
            mock_workspace.organization_id = organization_id
            mock_workspace.name = workspace_name
            mock_workspace.cloud_resources_url = "mock_url"
            mock_workspace.status = workspace_rust_status
            return mock_workspace
        else:
            msg = "Workspace not found"
            raise pcr.NotFoundError(msg)

    mock_api_client.get_workspace = workspace_details


@pytest.fixture
def _mock_get_workspaces(
    mock_api_client,
    organization_id,
    workspace_id,
    workspace_rust_status,
    workspace_name,
):
    def get_workspaces(name: str):
        mock_workspace = SimpleNamespace()
        mock_workspace.id = workspace_id
        mock_workspace.organization_id = organization_id
        mock_workspace.name = workspace_name
        mock_workspace.cloud_resources_url = "mock_url"
        mock_workspace.status = workspace_rust_status
        mock_get_workspaces = [mock_workspace]
        return [w for w in mock_get_workspaces if w.name.startswith(name)]

    mock_api_client.get_workspaces = get_workspaces


@pytest.fixture
def _mock_no_default_cluster_settings(instance_type, mock_api_client):  # noqa: ARG001
    def no_default(_workspace_id: UUID):
        return None

    mock_api_client.get_workspace_default_compute_specs = no_default


@pytest.fixture
def _mock_defaults_failure(mock_api_client):
    def mock_failure(_workspace_id: UUID):
        msg = "Failure"
        raise RuntimeError(msg)

    mock_api_client.get_workspace_default_compute_specs = mock_failure


@pytest.fixture
def _mock_default_cluster_settings_instance_type(mock_api_client, instance_type):
    def get_workspace_default_compute_specs(_workspace_id: UUID):
        mock_result = SimpleNamespace()
        mock_result.instance_type = instance_type
        mock_result.cpus = None
        mock_result.ram_gb = None
        mock_result.storage = 16
        mock_result.cluster_size = 1
        return mock_result

    mock_api_client.get_workspace_default_compute_specs = (
        get_workspace_default_compute_specs
    )


# These are for convenience to easier understand what we are mocking functionally
@pytest.fixture
def _mock_organization_by_name(_mock_get_organizations):
    pass


@pytest.fixture
def _mock_organization_by_id(_mock_organization_details):
    pass


@pytest.fixture
def _mock_workspace_by_default(_mock_user_default_workspace, _mock_workspace_details):
    pass


@pytest.fixture
def _mock_workspace_by_name(_mock_get_workspaces):
    pass


@pytest.fixture
def _mock_workspace_by_name_with_workspace_defaults(
    _mock_get_workspaces, _mock_default_cluster_settings_instance_type
):
    pass


@pytest.fixture
def _mock_workspace_by_id(_mock_workspace_details):
    pass
