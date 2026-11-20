import copy
import logging
from datetime import datetime
from typing import Any
from unittest.mock import MagicMock, patch

import httpx
import pytest
from pydantic import ValidationError

from edison_client import EdisonClient
from edison_client.models.app import (
    RELEASE_NAME_TO_ENUM_MAPPINGS,
    AuthType,
    JobNames,
    RuntimeConfig,
    TaskRequest,
    TaskResponse,
    TaskResponseVerbose,
)
from edison_client.utils.auth import RefreshingJWT


@pytest.fixture(name="mock_client")
def fixture_mock_client() -> MagicMock:
    """Create a mock synchronous HTTP client that returns success on first auth attempt."""
    client = MagicMock(spec=httpx.Client)
    response = MagicMock()
    response.raise_for_status.return_value = None
    response.json.return_value = {
        "access_token": "test_token_from_api",
        "expires_in": 300,
    }
    client.post.return_value = response
    return client


@pytest.fixture(name="failing_then_success_client")
def fixture_failing_then_success_client() -> tuple[MagicMock, MagicMock]:
    """Create a client that fails with 401 on first call, then succeeds on retry."""
    client = MagicMock(spec=httpx.Client)

    first_response = MagicMock(status_code=401)
    success_response = MagicMock()
    success_response.raise_for_status.return_value = None
    success_response.json.return_value = {
        "access_token": "refreshed_token",
        "expires_in": 300,
    }

    client.post.return_value = success_response

    return client, first_response


def test_refreshing_jwt_with_api_key(mock_client: MagicMock) -> None:
    """Test that RefreshingJWT works with API key authentication."""
    api_key = "mock_api_key_12345"

    auth = RefreshingJWT(
        auth_client=mock_client, auth_type=AuthType.API_KEY, api_key=api_key
    )

    assert auth._jwt == "test_token_from_api"

    mock_client.post.assert_called_once()
    args, kwargs = mock_client.post.call_args
    assert args[0] == "/auth/login"
    assert "json" in kwargs
    assert kwargs["json"] == {"api_key": api_key}


def test_refreshing_jwt_with_jwt_token() -> None:
    """Test that RefreshingJWT works with JWT authentication."""
    jwt_token = "mock.jwt.token"

    auth = RefreshingJWT(auth_client=MagicMock(), auth_type=AuthType.JWT, jwt=jwt_token)

    assert auth._jwt == jwt_token


def test_refreshing_jwt_rejects_invalid_auth_type(mock_client: MagicMock) -> None:
    with pytest.raises(ValueError, match="AuthType"):
        RefreshingJWT(
            auth_client=mock_client,
            auth_type="unsupported",  # ty: ignore[invalid-argument-type]
            jwt="mock.jwt.token",
        )
    mock_client.post.assert_not_called()


def test_refreshing_jwt_refresh_token(mock_client: MagicMock) -> None:
    """Test that refresh_token method correctly gets a new token."""
    api_key = "mock_api_key_12345"

    auth = RefreshingJWT(
        auth_client=mock_client, auth_type=AuthType.API_KEY, api_key=api_key
    )

    original_token = auth._jwt

    new_response = MagicMock()
    new_response.raise_for_status.return_value = None
    new_response.json.return_value = {
        "access_token": "new_refreshed_token",
        "expires_in": 300,
    }
    mock_client.post.return_value = new_response

    auth.refresh_token()

    assert auth._jwt == "new_refreshed_token"
    assert auth._jwt != original_token

    assert mock_client.post.call_count == 2  # Initial auth + refresh


def test_auth_flow_with_retry(
    failing_then_success_client: tuple[MagicMock, MagicMock],
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that auth_flow retries with new token after receiving a 401."""
    caplog.set_level(logging.INFO, logger="edison_client.utils.auth")

    client, first_response = failing_then_success_client
    api_key = "mock_api_key_12345"
    auth = RefreshingJWT(
        auth_client=client, auth_type=AuthType.API_KEY, api_key=api_key
    )
    request = httpx.Request("GET", "https://fh.org/api/v1/trajectories?status=pending")

    flow = auth.auth_flow(request)
    first_request = next(flow)
    assert first_request.headers["Authorization"] == f"Bearer {auth._jwt}"

    second_request = flow.send(first_response)
    assert auth._jwt == "refreshed_token"
    assert second_request.headers["Authorization"] == "Bearer refreshed_token"
    success_response = httpx.Response(200)

    try:
        flow.send(success_response)
        pytest.fail("Generator should have exited after processing the response")
    except StopIteration:
        pass

    client.post.assert_called_with("/auth/login", json={"api_key": api_key})

    assert any(
        "Received 401 for request [GET https://fh.org/api/v1/trajectories?status=pending]"
        in record.message
        for record in caplog.records
    )


def test_auth_flow_jwt_does_not_refresh_on_401(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """JWT auth cannot refresh — auth_flow should pass the response through."""
    caplog.set_level(logging.INFO, logger="edison_client.utils.auth")

    auth_client = MagicMock(spec=httpx.Client)
    jwt_token = "mock.jwt.token"
    auth = RefreshingJWT(auth_client=auth_client, auth_type=AuthType.JWT, jwt=jwt_token)
    request = httpx.Request("GET", "https://fh.org/api/v1/trajectories?status=pending")

    flow = auth.auth_flow(request)
    first_request = next(flow)
    assert first_request.headers["Authorization"] == f"Bearer {jwt_token}"

    failing_response = MagicMock(status_code=401)
    with pytest.raises(StopIteration):
        flow.send(failing_response)

    auth_client.post.assert_not_called()
    assert auth._jwt == jwt_token
    assert not any("refreshing token" in record.message for record in caplog.records)


def test_task_response_does_not_mutate_original_data() -> None:
    """Test that TaskResponse doesn't mutate the original data when creating an instance."""
    original_data: dict[str, Any] = {
        "crow": "test-crow",
        "task": "test task",
        "metadata": {
            "environment_name": "test-env",
            "agent_name": "test-agent",
            "some_other_field": "should not be modified",
        },
        "status": "success",
        "created_at": datetime.now(),
        "share_status": "PUBLIC",
    }

    original_data_copy = copy.deepcopy(original_data)

    task_response = TaskResponse(**original_data)

    assert original_data == original_data_copy, "Original data was mutated"

    # Assert the fields are set correctly
    assert task_response.job_name == original_data["crow"]
    assert task_response.query == original_data["task"]
    metadata = original_data.get("metadata", {})
    assert task_response.environment_name == metadata.get("environment_name")
    assert task_response.agent_name == metadata.get("agent_name")


@pytest.mark.parametrize("response_type", [TaskResponse, TaskResponseVerbose])
@pytest.mark.parametrize(
    "permitted_accessors",
    [
        None,
        {"users": ["reader@example.com"], "organizations": [123], "groups": None},
        {
            "users": None,
            "organizations": None,
            "groups": ["df91c7de-86af-49a1-ac19-bf6fe41f4ee9"],
        },
    ],
)
def test_task_response_preserves_nullable_permitted_accessors(
    response_type: type[TaskResponse],
    permitted_accessors: dict[str, list[str | int] | None] | None,
) -> None:
    response = response_type.model_validate({
        "crow": "test-crow",
        "task": "test task",
        "status": "success",
        "created_at": "2026-11-15T12:00:00Z",
        "share_status": "shared",
        "permitted_accessors": permitted_accessors,
    })

    assert response.permitted_accessors == permitted_accessors


def test_create_task_raises_error_with_both_files_parameter_and_env_config() -> None:
    """Test that create_task raises ValueError when both files parameter and environment config files are provided."""
    with patch(
        "edison_client.clients.rest_client.RestClient._fetch_my_orgs",
        return_value=["test-org"],
    ):
        client = EdisonClient(api_key="test_key")

    task_data = TaskRequest(
        name="test-job",
        query="Test query",
        runtime_config=RuntimeConfig(
            environment_config={"data_storage_uris": ["data_entry:existing-uri"]}
        ),
    )

    files = ["data_entry:new-uri"]

    with pytest.raises(
        ValueError,
        match="Please provide file uris either in the files parameter or within the environment configuration, not both",
    ):
        client.create_task(task_data, files=files)


@pytest.mark.asyncio
async def test_acreate_task_raises_error_with_both_files_parameter_and_env_config() -> (
    None
):
    """Test that acreate_task raises ValueError when both files parameter and environment config files are provided."""
    with patch(
        "edison_client.clients.rest_client.RestClient._fetch_my_orgs",
        return_value=["test-org"],
    ):
        client = EdisonClient(api_key="test_key")

    task_data = TaskRequest(
        name="test-job",
        query="Test query",
        runtime_config=RuntimeConfig(
            environment_config={"data_storage_uris": ["data_entry:existing-uri"]}
        ),
    )

    files = ["data_entry:new-uri"]

    with pytest.raises(
        ValueError,
        match="Please provide file uris either in the files parameter or within the environment configuration, not both",
    ):
        await client.acreate_task(task_data, files=files)


@pytest.mark.parametrize("asynchronous", [False, True], ids=["sync", "async"])
@pytest.mark.parametrize("trajectory_id", ["test-trajectory", None, 123])
async def test_create_task_validates_trajectory_id(
    monkeypatch: pytest.MonkeyPatch, asynchronous: bool, trajectory_id: str | int | None
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        assert request.url.path == "/v0.1/crows"
        return httpx.Response(200, json={"trajectory_id": trajectory_id})

    transport = httpx.MockTransport(handle)
    with httpx.Client(base_url="https://example.com", transport=transport) as sync:
        async with httpx.AsyncClient(
            base_url="https://example.com", transport=transport
        ) as async_client:
            monkeypatch.setattr(EdisonClient, "client", property(lambda _: sync))
            monkeypatch.setattr(
                EdisonClient, "async_client", property(lambda _: async_client)
            )
            client = EdisonClient(
                auth_type=AuthType.JWT, jwt="test-jwt", cleanup_on_exit=False
            )
            client.trajectory_id = "previous-trajectory"
            task = TaskRequest(name="test-job", query="Test query")

            async def submit() -> str:
                return (
                    await client.acreate_task(task)
                    if asynchronous
                    else client.create_task(task)
                )

            if isinstance(trajectory_id, str):
                assert await submit() == trajectory_id
                assert client.trajectory_id == trajectory_id
            else:
                with pytest.raises(ValidationError, match="valid string"):
                    await submit()
                assert client.trajectory_id == "previous-trajectory"

    assert len(requests) == 1


class TestLazyOrganizations:
    """Test suite for lazily resolved organizations."""

    def test_construction_issues_no_request(self) -> None:
        """Constructing a client must not touch the network."""
        with (
            patch.object(EdisonClient, "get_client") as get_client,
            patch.object(EdisonClient, "_fetch_my_orgs") as fetch_my_orgs,
        ):
            EdisonClient(api_key="test_key", cleanup_on_exit=False)

            assert not get_client.called
            assert not fetch_my_orgs.called

    def test_organizations_fetches_once_and_caches(self) -> None:
        """Reading organizations fetches on first access only."""
        with patch.object(
            EdisonClient, "_fetch_my_orgs", return_value=["test-org", "other-org"]
        ) as fetch_my_orgs:
            client = EdisonClient(api_key="test_key", cleanup_on_exit=False)

            assert client.organizations == ["test-org", "other-org"]
            assert client.organizations == ["test-org", "other-org"]
            fetch_my_orgs.assert_called_once()

    def test_organization_argument_filters_organizations(self) -> None:
        """The organization argument narrows the list to that organization."""
        with patch.object(
            EdisonClient, "_fetch_my_orgs", return_value=["test-org", "other-org"]
        ):
            client = EdisonClient(
                api_key="test_key", organization="other-org", cleanup_on_exit=False
            )

            assert client.organizations == ["other-org"]

    def test_unknown_organization_raises_on_access(self) -> None:
        """An unknown organization raises when the caller reads organizations."""
        with patch.object(EdisonClient, "_fetch_my_orgs", return_value=["test-org"]):
            client = EdisonClient(
                api_key="test_key", organization="missing-org", cleanup_on_exit=False
            )

            with pytest.raises(
                ValueError, match="Organization 'missing-org' not found"
            ):
                _ = client.organizations

    def test_check_credentials_raises_on_bad_credentials(self) -> None:
        """check_credentials surfaces the auth failure that __init__ used to raise."""
        request = httpx.Request("GET", "https://example.com/v0.1/organizations")
        error = httpx.HTTPStatusError(
            "unauthorized",
            request=request,
            response=httpx.Response(401, request=request),
        )
        with patch.object(EdisonClient, "_fetch_my_orgs", side_effect=error):
            client = EdisonClient(api_key="test_key", cleanup_on_exit=False)

            with pytest.raises(httpx.HTTPStatusError):
                client.check_credentials()

    def test_check_credentials_warms_the_cache(self) -> None:
        """check_credentials resolves organizations so later reads cost nothing."""
        with patch.object(
            EdisonClient, "_fetch_my_orgs", return_value=["test-org"]
        ) as fetch_my_orgs:
            client = EdisonClient(api_key="test_key", cleanup_on_exit=False)
            client.check_credentials()

            assert client.organizations == ["test-org"]
            fetch_my_orgs.assert_called_once()


class TestReleaseNameToEnumMappings:
    """Test suite for RELEASE_NAME_TO_ENUM_MAPPINGS and JobNames.from_string()."""

    def test_release_name_mappings_exist(self) -> None:
        """Verify the expected release name mappings are defined."""
        assert "literature-20260216" in RELEASE_NAME_TO_ENUM_MAPPINGS
        assert "literature-high-20260216" in RELEASE_NAME_TO_ENUM_MAPPINGS
        assert RELEASE_NAME_TO_ENUM_MAPPINGS["literature-20260216"] == "LITERATURE"
        assert (
            RELEASE_NAME_TO_ENUM_MAPPINGS["literature-high-20260216"]
            == "LITERATURE_HIGH"
        )

    def test_from_string_with_release_name_lowercase(self) -> None:
        """Test from_string correctly handles lowercase release-dated names."""
        result = JobNames.from_string("literature-20260216")
        assert result == JobNames.LITERATURE
        assert result.value == "job-futurehouse-paperqa3"

        result_high = JobNames.from_string("literature-high-20260216")
        assert result_high == JobNames.LITERATURE_HIGH
        assert result_high.value == "job-futurehouse-paperqa3-high"

    def test_from_string_with_release_name_uppercase(self) -> None:
        """Test from_string correctly handles uppercase release-dated names (case-insensitive)."""
        result = JobNames.from_string("LITERATURE-20260216")
        assert result == JobNames.LITERATURE
        assert result.value == "job-futurehouse-paperqa3"

        result_high = JobNames.from_string("LITERATURE-HIGH-20260216")
        assert result_high == JobNames.LITERATURE_HIGH
        assert result_high.value == "job-futurehouse-paperqa3-high"

    def test_from_string_with_release_name_mixed_case(self) -> None:
        """Test from_string correctly handles mixed case release-dated names."""
        result = JobNames.from_string("Literature-20260216")
        assert result == JobNames.LITERATURE

        result_high = JobNames.from_string("Literature-High-20260216")
        assert result_high == JobNames.LITERATURE_HIGH

    def test_from_string_with_enum_names_still_works(self) -> None:
        """Test from_string still works with regular enum names."""
        assert JobNames.from_string("literature") == JobNames.LITERATURE
        assert JobNames.from_string("LITERATURE") == JobNames.LITERATURE
        assert JobNames.from_string("literature_high") == JobNames.LITERATURE_HIGH
        assert JobNames.from_string("LITERATURE_HIGH") == JobNames.LITERATURE_HIGH
        assert JobNames.from_string("crow") == JobNames.CROW
        assert JobNames.from_string("analysis") == JobNames.ANALYSIS

    def test_from_string_invalid_name_raises_error(self) -> None:
        """Test from_string raises ValueError for invalid job names."""
        with pytest.raises(ValueError, match="Invalid job name"):
            JobNames.from_string("nonexistent-job")

        with pytest.raises(ValueError, match="Invalid job name"):
            JobNames.from_string("literature-99999999")  # Non-existent release date

    def test_release_name_returns_correct_job_value(self) -> None:
        """Test that release names return JobNames with correct underlying job values."""
        literature_job = JobNames.from_string("literature-20260216")
        literature_high_job = JobNames.from_string("literature-high-20260216")

        # Verify they map to the correct job identifiers used by the backend
        assert literature_job.value == "job-futurehouse-paperqa3"
        assert literature_high_job.value == "job-futurehouse-paperqa3-high"

        # Verify they are equivalent to the canonical enum values
        assert literature_job == JobNames.LITERATURE
        assert literature_high_job == JobNames.LITERATURE_HIGH

    def test_release_name_works_with_task_request(self) -> None:
        """Test that release names can be used to create TaskRequest objects."""
        job_name = JobNames.from_string("literature-20260216")
        task_request = TaskRequest(
            name=job_name, query="Test query using release-dated job name"
        )

        assert task_request.name == JobNames.LITERATURE
        assert task_request.query == "Test query using release-dated job name"

    def test_all_release_mappings_resolve_to_valid_enum(self) -> None:
        """Test all entries in RELEASE_NAME_TO_ENUM_MAPPINGS resolve to valid JobNames."""
        for release_name, enum_name in RELEASE_NAME_TO_ENUM_MAPPINGS.items():
            # Verify the enum name exists in JobNames
            assert hasattr(JobNames, enum_name), f"JobNames.{enum_name} does not exist"

            # Verify from_string resolves correctly
            result = JobNames.from_string(release_name)
            assert result == JobNames[enum_name]
