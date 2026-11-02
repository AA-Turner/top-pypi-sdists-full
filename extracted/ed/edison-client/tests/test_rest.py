import asyncio
import datetime
import json
import time
from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError
from pytest_subtests import SubTests

from edison_client.clients import (
    JobNames,
)
from edison_client.clients.rest_client import (
    JobEventBatchCreationError,
    JobEventCreationError,
    JobEventUpdateError,
    ProjectError,
    RestClient,
)
from edison_client.models.app import (
    GitDeploymentInfo,
    JobDeploymentConfig,
    LiteTaskResponse,
    PhoenixTaskResponse,
    PQATaskResponse,
    RuntimeConfig,
    TaskRequest,
    TaskResponse,
    TaskResponseVerbose,
)
from edison_client.models.job_event import (
    CostComponent,
    ExecutionType,
    JobEventBatchCreateRequest,
    JobEventBatchItemRequest,
    JobEventCreateRequest,
    JobEventUpdateRequest,
)
from edison_client.models.rest import (
    ExecutionStatus,
    WorldModel,
)

TEST_MAX_POLLS = 100

# Per-task budget for live-agent tests that dispatch against the crow-high
# warmpool. Sized to survive a full warmpool rotation: the crow-high agent
# image is ~15 GB and cold nodes take 4-6 minutes to pull it, during which
# fresh dispatches can repeatedly hit SandboxNotFoundError ("deleted before
# becoming ready") and retry. 600s covers a couple of rotation rounds with
# headroom; smaller values (e.g. 180s) reliably time out during rollouts.
CONTINUATION_PER_TASK_TIMEOUT = 600

# Pytest wall-clock for test_continuation_task, which runs 2 sequential tasks
# each bounded by CONTINUATION_PER_TASK_TIMEOUT. Headroom covers client setup
# and assertion time.
CONTINUATION_TEST_TIMEOUT = 1500


@pytest.fixture(name="task_req")
def fixture_task_req():
    """Create a sample task request."""
    return TaskRequest(
        name=JobNames.from_string("dummy"),
        query="How many moons does earth have?",
    )


@pytest.fixture(name="pqa_task_req")
def fixture_pqa_task_req():
    return TaskRequest(
        name=JobNames.from_string("crow"),
        query="How many moons does earth have?",
    )


@pytest.fixture(name="phoenix_task_req")
def fixture_phoenix_task_req():
    return TaskRequest(
        name=JobNames.from_string("phoenix"),
        query="What is the molecular weight of ascorbic acids?",
    )


def _create_job_payload(
    tmp_path,
    sandbox_infra_manager_image: str | None = None,
    metadata: dict | None = None,
):
    module_dir = tmp_path / "agent"
    module_dir.mkdir()
    (module_dir / "env.py").write_text("class Env:\n    pass\n", encoding="utf-8")
    (module_dir / "requirements.txt").write_text("", encoding="utf-8")
    if metadata is not None:
        (module_dir / ".edison-deployment.json").write_text(json.dumps(metadata))

    response = MagicMock()
    response.raise_for_status.return_value = None
    response.json.return_value = {"build_id": str(uuid4())}
    multipart_client = MagicMock()
    multipart_client.post.return_value = response

    with (
        patch(
            "edison_client.clients.rest_client.RestClient._fetch_my_orgs",
            return_value=["FutureHouse"],
        ),
        patch(
            "edison_client.clients.rest_client.RestClient._check_job",
            return_value={"exists": False},
        ),
        patch(
            "edison_client.clients.rest_client.RestClient.multipart_client",
            new_callable=PropertyMock,
        ) as multipart_client_prop,
    ):
        multipart_client_prop.return_value = multipart_client
        client = RestClient(api_key="test-key", cleanup_on_exit=False)
        client.create_job(
            JobDeploymentConfig(
                path=module_dir,
                name="test-job",
                environment="test_env",
                task_description="test task",
                sandbox_infra_manager_image=sandbox_infra_manager_image,
            )
        )

    return multipart_client.post.call_args.kwargs


def test_create_job_sends_sandbox_infra_manager_image(tmp_path):
    request = _create_job_payload(
        tmp_path,
        sandbox_infra_manager_image="sandbox-infra-manager:branch",
    )

    assert (
        request["data"]["sandbox_infra_manager_image"] == "sandbox-infra-manager:branch"
    )


def test_create_job_omits_empty_sandbox_infra_manager_image(tmp_path):
    data = _create_job_payload(tmp_path)["data"]

    assert "sandbox_infra_manager_image" not in data


def test_create_job_keeps_controlled_tools_internal(tmp_path):
    data = _create_job_payload(tmp_path)["data"]
    for field, value in [
        ("controlled_tool_groups", ["literature"]),
        ("controlled_tools_image", "controlled-tools:test"),
    ]:
        assert field not in data
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            JobDeploymentConfig.model_validate({
                "name": "test-job",
                "environment": "test_env",
                field: value,
            })


@pytest.mark.parametrize("groups", [[], ["literature"]])
def test_create_job_uploads_generated_profile_metadata(tmp_path, groups):
    metadata = {"controlled_tool_groups": groups}
    request = _create_job_payload(tmp_path, metadata=metadata)
    uploaded = {
        name: content
        for _, (name, content, _) in request["files"]
        if name.endswith("/.edison-deployment.json")
    }
    assert len(uploaded) == 1
    assert json.loads(next(iter(uploaded.values()))) == metadata
    assert "controlled_tool_groups" not in request["data"]
    assert "controlled_tools_image" not in request["data"]


@pytest.fixture(name="running_trajectory_id")
def fixture_running_trajectory_id(
    admin_client: RestClient, task_req: TaskRequest
) -> str:
    return admin_client.create_task(task_req)


@pytest.mark.live_agent
@pytest.mark.timeout(300)
@pytest.mark.flaky(reruns=3)
def test_futurehouse_dummy_env_crow(admin_client: RestClient, task_req: TaskRequest):
    task_id = admin_client.create_task(task_req)
    print(f"\n\nTrajectory ID: {task_id}\n")
    while (task_status := admin_client.get_task(task_id).status) in {
        "queued",
        "in progress",
    }:
        time.sleep(5)
    assert task_status == "success"


def test_insufficient_permissions_request(
    pub_client: RestClient, task_req: TaskRequest
):
    # Create a new instance so that cached credentials aren't reused
    with pytest.raises(PermissionError) as exc_info:
        pub_client.create_task(task_req)

    assert "Error creating task" in str(exc_info.value)


@pytest.mark.timeout(350)
@pytest.mark.asyncio
@pytest.mark.skip(reason="Skipping due to buggy pqa on dev")
async def test_job_response(  # noqa: PLR0915
    subtests: SubTests,
    admin_client: RestClient,
    pqa_task_req: TaskRequest,
    phoenix_task_req: TaskRequest,
):
    task_id = admin_client.create_task(pqa_task_req)
    atask_id = await admin_client.acreate_task(pqa_task_req)
    phoenix_task_id = admin_client.create_task(phoenix_task_req)
    aphoenix_task_id = await admin_client.acreate_task(phoenix_task_req)

    with subtests.test("Test TaskResponse with queued task"):
        task_response = admin_client.get_task(task_id)
        assert task_response.status in {"queued", "in progress"}
        assert not isinstance(task_response, LiteTaskResponse)
        assert task_response.job_name == pqa_task_req.name
        assert task_response.query == pqa_task_req.query
        task_response = await admin_client.aget_task(atask_id)
        assert task_response.status in {"queued", "in progress"}
        assert not isinstance(task_response, LiteTaskResponse)
        assert task_response.job_name == pqa_task_req.name
        assert task_response.query == pqa_task_req.query

    for _ in range(TEST_MAX_POLLS):
        task_response = admin_client.get_task(task_id)
        if task_response.status in ExecutionStatus.terminal_states():
            break
        await asyncio.sleep(5)

    for _ in range(TEST_MAX_POLLS):
        task_response = await admin_client.aget_task(atask_id)
        if task_response.status in ExecutionStatus.terminal_states():
            break
        await asyncio.sleep(5)

    with subtests.test("Test PQA job response"):
        task_response = admin_client.get_task(task_id)
        assert isinstance(task_response, PQATaskResponse)
        # assert it has general fields
        assert task_response.status == "success"
        assert task_response.task_id is not None
        assert pqa_task_req.name in task_response.job_name
        assert pqa_task_req.query in task_response.query
        # assert it has PQA specific fields
        assert task_response.answer is not None
        # assert it's not verbose
        assert not hasattr(task_response, "environment_frame")
        assert not hasattr(task_response, "agent_state")

    with subtests.test("Test async PQA job response"):
        task_response = await admin_client.aget_task(atask_id)
        assert isinstance(task_response, PQATaskResponse)
        # assert it has general fields
        assert task_response.status == "success"
        assert task_response.task_id is not None
        assert pqa_task_req.name in task_response.job_name
        assert pqa_task_req.query in task_response.query
        # assert it has PQA specific fields
        assert task_response.answer is not None
        # assert it's not verbose
        assert not hasattr(task_response, "environment_frame")
        assert not hasattr(task_response, "agent_state")

    with subtests.test("Test Phoenix job response"):
        task_response = admin_client.get_task(phoenix_task_id)
        assert isinstance(task_response, PhoenixTaskResponse)
        assert task_response.status == "success"
        assert task_response.task_id is not None
        assert phoenix_task_req.name in task_response.job_name
        assert phoenix_task_req.query in task_response.query

    with subtests.test("Test async Phoenix job response"):
        task_response = await admin_client.aget_task(aphoenix_task_id)
        assert isinstance(task_response, PhoenixTaskResponse)
        assert task_response.status == "success"
        assert task_response.task_id is not None
        assert phoenix_task_req.name in task_response.job_name
        assert phoenix_task_req.query in task_response.query

    with subtests.test("Test task response with verbose"):
        task_response = admin_client.get_task(task_id, verbose=True)
        assert isinstance(task_response, TaskResponseVerbose)
        assert task_response.status == "success"
        assert task_response.environment_frame is not None
        assert task_response.agent_state is not None

    with subtests.test("Test task async response with verbose"):
        task_response = await admin_client.aget_task(atask_id, verbose=True)
        assert isinstance(task_response, TaskResponseVerbose)
        assert task_response.status == "success"
        assert task_response.environment_frame is not None
        assert task_response.agent_state is not None


# Known trajectory with deployment_config in metadata (for testing admin-only access)
TRAJECTORY_WITH_DEPLOYMENT_CONFIG = "b1330ceb-6723-4af9-a8be-c7807ac4bd6c"


@pytest.mark.timeout(60)
def test_deployment_config_visible_to_fh_admin(admin_client: RestClient):
    """FutureHouse admin should see deployment_config with git metadata."""
    task = admin_client.get_task(TRAJECTORY_WITH_DEPLOYMENT_CONFIG, verbose=True)
    assert isinstance(task, TaskResponseVerbose)
    assert task.deployment_config is not None, "FH admin should see deployment_config"
    assert isinstance(task.deployment_config, GitDeploymentInfo)
    assert task.deployment_config.commit_hash is not None


@pytest.mark.timeout(60)
def test_deployment_config_hidden_from_non_fh_admin(pub_client: RestClient):
    """Non-FutureHouse-admin should NOT see deployment_config."""
    task = pub_client.get_task(TRAJECTORY_WITH_DEPLOYMENT_CONFIG, verbose=True)
    assert isinstance(task, TaskResponseVerbose)
    assert task.deployment_config is None, (
        "Non-FH-admin should NOT see deployment_config"
    )


@pytest.mark.live_agent
@pytest.mark.timeout(300)
@pytest.mark.flaky(reruns=3)
def test_run_until_done_futurehouse_dummy_env_crow(
    admin_client: RestClient, task_req: TaskRequest
):
    tasks_to_do = [task_req, task_req]

    results = admin_client.run_tasks_until_done(tasks_to_do, timeout=240)

    assert len(results) == len(tasks_to_do), "Should return 2 tasks."
    assert all(task.status == "success" for task in results)


@pytest.mark.live_agent
@pytest.mark.timeout(300)
@pytest.mark.flaky(reruns=3)
def test_run_until_done_returns_task_response(
    admin_client: RestClient, task_req: TaskRequest
):
    """Test that run_tasks_until_done returns TaskResponse instead of LiteTaskResponse."""
    tasks_to_do = [task_req, task_req]

    results = admin_client.run_tasks_until_done(tasks_to_do, timeout=240)

    assert len(results) == len(tasks_to_do), "Should return 2 tasks."
    assert all(task.status == "success" for task in results)

    for task in results:
        assert isinstance(task, TaskResponse), (
            f"Expected TaskResponse, got {type(task)}"
        )


@pytest.mark.live_agent
@pytest.mark.timeout(300)
@pytest.mark.flaky(reruns=3)
@pytest.mark.asyncio
async def test_arun_until_done_futurehouse_dummy_env_crow(
    admin_client: RestClient, task_req: TaskRequest
):
    tasks_to_do = [task_req, task_req]

    results = await admin_client.arun_tasks_until_done(tasks_to_do)

    assert len(results) == len(tasks_to_do), "Should return 2 tasks."
    assert all(task.status == "success" for task in results)


@pytest.mark.live_agent
@pytest.mark.timeout(300)
@pytest.mark.flaky(reruns=3)
@pytest.mark.asyncio
async def test_arun_until_done_returns_task_response(
    admin_client: RestClient, task_req: TaskRequest
):
    """Test that arun_tasks_until_done returns TaskResponse instead of LiteTaskResponse."""
    tasks_to_do = [task_req, task_req]

    results = await admin_client.arun_tasks_until_done(tasks_to_do)

    assert len(results) == len(tasks_to_do), "Should return 2 tasks."
    assert all(task.status == "success" for task in results)

    for task in results:
        assert isinstance(task, TaskResponse), (
            f"Expected TaskResponse, got {type(task)}"
        )


@pytest.mark.live_agent
@pytest.mark.timeout(CONTINUATION_TEST_TIMEOUT)
def test_continuation_task(admin_client: RestClient):
    """Test running a continuation task against data-analysis-crow-high."""
    initial_task = TaskRequest(
        name=JobNames.ANALYSIS,
        query="What is 2 + 2? Just give me the number.",
        runtime_config=RuntimeConfig(timeout=CONTINUATION_PER_TASK_TIMEOUT),
    )
    print(initial_task)

    initial_results = admin_client.run_tasks_until_done(
        task_data=initial_task,
        verbose=True,
        progress_bar=True,
        timeout=CONTINUATION_PER_TASK_TIMEOUT,
    )

    assert len(initial_results) == 1
    initial_result = initial_results[0]
    assert initial_result.status == "success", (
        f"Initial task did not complete successfully. Status: {initial_result.status}. "
        f"Task ID: {initial_result.task_id}"
    )

    continuation_task = TaskRequest(
        name=JobNames.ANALYSIS,
        query="Now multiply that result by 3. Just give me the number.",
        runtime_config=RuntimeConfig(
            timeout=CONTINUATION_PER_TASK_TIMEOUT,
            continued_job_id=initial_result.task_id,
        ),
    )

    continuation_results = admin_client.run_tasks_until_done(
        task_data=continuation_task,
        verbose=True,
        progress_bar=True,
        timeout=CONTINUATION_PER_TASK_TIMEOUT,
    )

    assert len(continuation_results) == 1
    continuation_result = continuation_results[0]
    assert continuation_result.status == "success", (
        f"Continuation task did not complete successfully. Status: {continuation_result.status}. "
        f"Task ID: {continuation_result.task_id}"
    )


@pytest.mark.live_agent
@pytest.mark.timeout(60)
@pytest.mark.flaky(reruns=3)
@pytest.mark.asyncio
async def test_timeout_run_until_done_futurehouse_dummy_env_crow(
    admin_client: RestClient, task_req: TaskRequest
):
    tasks_to_do = [task_req, task_req]

    # Use a very short timeout to ensure tasks don't complete
    # The default polling time is 5 seconds, so a very short timeout ensures
    # we timeout after the first poll but before the second poll occurs
    short_timeout = 0.1

    results = await admin_client.arun_tasks_until_done(
        tasks_to_do, verbose=True, timeout=short_timeout, progress_bar=True
    )

    assert len(results) == len(tasks_to_do), "Should return 2 tasks."
    # With a 0.1-second timeout, tasks should not have time to complete
    # Check that not all tasks succeeded (at least some should be incomplete)
    statuses = [task.status for task in results]
    assert not all(status == "success" for status in statuses), (
        f"With {short_timeout}s timeout, not all tasks should complete successfully. "
        f"Got statuses: {statuses}"
    )
    assert all(not isinstance(task, PQATaskResponse) for task in results), (
        "Should be verbose."
    )

    results = admin_client.run_tasks_until_done(
        tasks_to_do, verbose=True, timeout=short_timeout, progress_bar=True
    )

    assert len(results) == len(tasks_to_do), "Should return 2 tasks."
    # Same expectation for sync version
    statuses = [task.status for task in results]
    assert not all(status == "success" for status in statuses), (
        f"With {short_timeout}s timeout, not all tasks should complete successfully. "
        f"Got statuses: {statuses}"
    )
    assert all(not isinstance(task, PQATaskResponse) for task in results), (
        "Should be verbose."
    )


@pytest.mark.timeout(300)
@pytest.mark.flaky(reruns=3)
def test_cancel_task(admin_client: RestClient):
    """Test successful task cancellation using MagicMock."""
    task_id = "1c28bb94-efbf-442f-954c-f0d8ddb0cff5"

    with (
        patch.object(admin_client.client, "post") as mock_post,
        patch.object(admin_client, "get_task") as mock_get_task,
    ):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        mock_task_response_running = MagicMock()
        mock_task_response_running.status = "in progress"

        mock_task_response_cancelled = MagicMock()
        mock_task_response_cancelled.status = ExecutionStatus.CANCELLED.value

        mock_get_task.side_effect = [
            mock_task_response_running,
            mock_task_response_cancelled,
        ]

        result = admin_client.cancel_task(task_id)

        assert result is True

        expected_url = f"/v0.1/trajectories/{task_id}/cancel"
        mock_post.assert_called_once_with(expected_url)

        assert mock_get_task.call_count == 2


@pytest.mark.asyncio
async def test_world_model_acreate_and_aget(admin_client: RestClient):
    model = WorldModel(
        content="test content",
        name="Test Model",
        description="This is a test model.",
    )
    model_id = await admin_client.acreate_world_model(model)

    # try getting the newly created model by id
    model_by_id = await admin_client.aget_world_model(model_id)

    assert str(model_by_id.id) == str(model_id)
    assert model_by_id.content == model.content

    updated_model = WorldModel(
        content="updated test content",
        prior=model_id,
    )

    updated_model_id = await admin_client.acreate_world_model(updated_model)

    # try getting the newly created model by id
    updated_model_by_id = await admin_client.aget_world_model(updated_model_id)

    assert updated_model_by_id.name == model.name
    assert updated_model_by_id.content != model.content


def test_world_model_create_and_get(admin_client: RestClient):
    model = WorldModel(
        content="test content",
        name="Test Model",
        description="This is a test model.",
    )
    model_id = admin_client.create_world_model(model)

    # try getting the newly created model by id
    model_by_id = admin_client.get_world_model(model_id)

    assert str(model_by_id.id) == str(model_id)
    assert model_by_id.content == model.content

    updated_model = WorldModel(
        content="updated test content",
        prior=model_id,
    )

    updated_model_id = admin_client.create_world_model(updated_model)

    # try getting the newly created model by id
    updated_model_by_id = admin_client.get_world_model(updated_model_id)

    assert updated_model_by_id.name == model.name
    assert updated_model_by_id.content != model.content


class TestProjectOperations:
    @pytest.fixture
    def test_project_name(self):
        return f"test-project-{uuid4()}"

    def test_create_project_success(
        self, admin_client: RestClient, test_project_name: str
    ):
        project_id = admin_client.create_project(test_project_name)
        assert isinstance(project_id, UUID)

    def test_get_project_by_name_success(
        self, admin_client: RestClient, test_project_name: str
    ):
        created_project_id = admin_client.create_project(test_project_name)
        retrieved_project_id = admin_client.get_project_by_name(test_project_name)
        assert retrieved_project_id == created_project_id

    def test_get_project_by_name_not_found(self, admin_client: RestClient):
        with pytest.raises(ProjectError, match="No project found with name"):
            admin_client.get_project_by_name("non-existent-project-12345")

    def test_get_project_by_name_multiple_found(self, admin_client: RestClient):
        with patch.object(admin_client.client, "get") as mock_get:
            mock_response = MagicMock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = [
                {"id": str(uuid4()), "name": "test"},
                {"id": str(uuid4()), "name": "test"},
            ]
            mock_get.return_value = mock_response

            projects = admin_client.get_project_by_name("test")
            assert isinstance(projects, list)
            assert len(projects) == 2

    def test_add_task_to_project_success(
        self, admin_client: RestClient, test_project_name: str, task_req: TaskRequest
    ):
        project_id = admin_client.create_project(test_project_name)
        trajectory_id = admin_client.create_task(task_req)
        admin_client.add_task_to_project(project_id, trajectory_id)

    def test_add_task_to_project_not_found(self, admin_client: RestClient):
        fake_project_id = uuid4()
        fake_trajectory_id = str(uuid4())

        with patch.object(admin_client.client, "post") as mock_post:
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = Exception("404 Not Found")
            mock_post.return_value = mock_response

            with pytest.raises(
                ProjectError, match="Error adding trajectory to project"
            ):
                admin_client.add_task_to_project(fake_project_id, fake_trajectory_id)

    def test_create_project_with_http_error(self, admin_client: RestClient):
        with patch.object(admin_client.client, "post") as mock_post:
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = Exception("400 Bad Request")
            mock_response.status_code = 400
            mock_response.text = "Invalid project name"
            mock_post.return_value = mock_response

            with pytest.raises(ProjectError, match="Error creating project"):
                admin_client.create_project("invalid project name")

    def test_create_project_passes_description_through_metadata(
        self, admin_client: RestClient
    ):
        with patch.object(admin_client.client, "post") as mock_post:
            mock_response = MagicMock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = str(uuid4())
            mock_post.return_value = mock_response

            admin_client.create_project(
                name="brca1-study",
                description="Review BRCA1 mutation landscape in breast cancer.",
            )

            _, kwargs = mock_post.call_args
            body = kwargs["json"]
            assert body["metadata"] == {
                "description": "Review BRCA1 mutation landscape in breast cancer."
            }

    def test_create_project_does_not_mutate_caller_metadata(
        self, admin_client: RestClient
    ):
        caller_metadata = {"agent": "kosmos"}
        with patch.object(admin_client.client, "post") as mock_post:
            mock_response = MagicMock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = str(uuid4())
            mock_post.return_value = mock_response

            admin_client.create_project(
                name="brca1-study",
                metadata=caller_metadata,
                description="Review BRCA1 mutation landscape in breast cancer.",
            )

            assert caller_metadata == {"agent": "kosmos"}
            _, kwargs = mock_post.call_args
            body = kwargs["json"]
            assert body["metadata"] == {
                "agent": "kosmos",
                "description": "Review BRCA1 mutation landscape in breast cancer.",
            }

    def test_create_project_omits_description_when_not_provided(
        self, admin_client: RestClient
    ):
        with patch.object(admin_client.client, "post") as mock_post:
            mock_response = MagicMock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = str(uuid4())
            mock_post.return_value = mock_response

            admin_client.create_project(name="brca1-study")

            _, kwargs = mock_post.call_args
            body = kwargs["json"]
            assert "description" not in body["metadata"]


class TestAsyncProjectOperations:
    @pytest.fixture
    def test_project_name(self):
        return f"test-async-project-{uuid4()}"

    @pytest.mark.asyncio
    async def test_acreate_project_success(
        self, admin_client: RestClient, test_project_name: str
    ):
        project_id = await admin_client.acreate_project(test_project_name)
        assert isinstance(project_id, UUID)

    @pytest.mark.asyncio
    async def test_aget_project_by_name_success(
        self, admin_client: RestClient, test_project_name: str
    ):
        created_project_id = await admin_client.acreate_project(test_project_name)
        retrieved_project_id = await admin_client.aget_project_by_name(
            test_project_name
        )
        assert retrieved_project_id == created_project_id

    @pytest.mark.asyncio
    async def test_aget_project_by_name_not_found(self, admin_client: RestClient):
        with pytest.raises(ProjectError, match="No project found with name"):
            await admin_client.aget_project_by_name("non-existent-async-project-12345")

    @pytest.mark.asyncio
    async def test_aadd_task_to_project_success(
        self, admin_client: RestClient, test_project_name: str, task_req: TaskRequest
    ):
        project_id = await admin_client.acreate_project(test_project_name)
        trajectory_id = await admin_client.acreate_task(task_req)
        await admin_client.aadd_task_to_project(project_id, trajectory_id)

    @pytest.mark.asyncio
    async def test_acreate_project_passes_description_through_metadata(
        self, admin_client: RestClient
    ):
        persona_id = uuid4()
        with patch.object(
            admin_client.async_client, "post", new_callable=AsyncMock
        ) as mock_post:
            mock_response = MagicMock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"id": str(uuid4())}
            mock_post.return_value = mock_response

            await admin_client.acreate_project(
                name="brca1-study",
                persona_id=persona_id,
                description="Review BRCA1 mutation landscape in breast cancer.",
            )

            args, kwargs = mock_post.call_args
            assert args[0] == f"/v0.1/personas/{persona_id}/projects"
            body = kwargs["json"]
            assert body["metadata"] == {
                "description": "Review BRCA1 mutation landscape in breast cancer."
            }

    @pytest.mark.asyncio
    async def test_acreate_project_does_not_mutate_caller_metadata(
        self, admin_client: RestClient
    ):
        caller_metadata = {"source": "subagent"}
        with patch.object(
            admin_client.async_client, "post", new_callable=AsyncMock
        ) as mock_post:
            mock_response = MagicMock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = str(uuid4())
            mock_post.return_value = mock_response

            await admin_client.acreate_project(
                name="brca1-study",
                metadata=caller_metadata,
                description="Review BRCA1 mutation landscape in breast cancer.",
            )

            assert caller_metadata == {"source": "subagent"}

    @pytest.mark.asyncio
    async def test_aadd_task_to_project_permission_denied(
        self, admin_client: RestClient
    ):
        fake_project_id = uuid4()
        fake_trajectory_id = str(uuid4())

        with patch.object(admin_client.async_client, "post") as mock_post:
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = Exception("403 Forbidden")
            mock_response.status_code = 403
            mock_post.return_value = mock_response

            with pytest.raises(
                ProjectError, match="Error adding trajectory to project: 403 Forbidden"
            ):
                await admin_client.aadd_task_to_project(
                    fake_project_id, fake_trajectory_id
                )


@pytest.mark.live_agent
@pytest.mark.timeout(300)
@pytest.mark.flaky(reruns=3)
def test_get_tasks_with_project_filter(admin_client: RestClient, task_req: TaskRequest):
    """Test retrieving trajectories filtered by project_id using real API calls."""
    project_name = f"e2e-trajectories-fetch-{uuid4()}"
    project_id = admin_client.create_project(project_name)

    trajectory_id = admin_client.create_task(task_req)
    admin_client.add_task_to_project(project_id, trajectory_id)

    poll_deadline = time.monotonic() + 240
    while (task_status := admin_client.get_task(trajectory_id).status) in {
        "queued",
        "in progress",
    }:
        assert time.monotonic() < poll_deadline, (
            f"Task {trajectory_id} still {task_status} after 240s"
        )
        time.sleep(5)

    trajectories = admin_client.get_tasks(project_id=project_id)

    trajectory_ids = [t["id"] for t in trajectories]
    assert trajectory_id in trajectory_ids


@pytest.mark.live_agent
@pytest.mark.timeout(300)
@pytest.mark.flaky(reruns=3)
@pytest.mark.asyncio
async def test_aget_tasks_with_project_filter(
    admin_client: RestClient, task_req: TaskRequest
):
    """Test async retrieving trajectories filtered by project_id using real API calls."""
    project_name = f"e2e-trajectories-async-fetch-{uuid4()}"
    project_id = await admin_client.acreate_project(project_name)

    trajectory_id = await admin_client.acreate_task(task_req)
    await admin_client.aadd_task_to_project(project_id, trajectory_id)

    poll_deadline = time.monotonic() + 240
    while True:
        task = await admin_client.aget_task(trajectory_id)
        if task.status not in {"queued", "in progress"}:
            break
        assert time.monotonic() < poll_deadline, (
            f"Task {trajectory_id} still {task.status} after 240s"
        )
        await asyncio.sleep(5)

    trajectories = await admin_client.aget_tasks(project_id=project_id)

    trajectory_ids = [t["id"] for t in trajectories]
    assert trajectory_id in trajectory_ids


class TestJobEventOperations:
    @pytest.fixture
    def test_trajectory_id(
        self, admin_client: RestClient, task_req: TaskRequest
    ) -> str:
        """Create a real trajectory for job event testing."""
        return admin_client.create_task(task_req)

    @pytest.fixture
    def job_event_create_request(self, test_trajectory_id: str):
        return JobEventCreateRequest(
            execution_id=UUID(test_trajectory_id),
            execution_type=ExecutionType.TRAJECTORY,
            cost_component=CostComponent.LLM_USAGE,
            started_at=datetime.datetime.now(),
            ended_at=datetime.datetime.now(),
            amount_usd=0.005,
            rate=0.0001,
            input_token_count=100,
            completion_token_count=50,
            metadata={"model": "gpt-4o", "temperature": 0.7},
        )

    @pytest.fixture
    def job_event_update_request(self):
        return JobEventUpdateRequest(
            amount_usd=0.007,
            rate=0.00015,
            input_token_count=120,
            completion_token_count=60,
            metadata={"model": "gpt-4o", "temperature": 0.5, "updated": True},
        )

    @pytest.mark.timeout(300)
    def test_create_job_event_success(
        self, admin_client: RestClient, job_event_create_request
    ):
        response = admin_client.create_job_event(job_event_create_request)
        assert response.id is not None
        assert isinstance(response.id, UUID)

    @pytest.mark.asyncio
    @pytest.mark.timeout(300)
    async def test_acreate_job_event_success(
        self, admin_client: RestClient, job_event_create_request
    ):
        response = await admin_client.acreate_job_event(job_event_create_request)
        assert response.id is not None
        assert isinstance(response.id, UUID)

    def test_create_job_event_execution_not_found(
        self, admin_client: RestClient, job_event_create_request
    ):
        # Create a new request with a non-existent execution ID
        invalid_request = JobEventCreateRequest(
            execution_id=uuid4(),  # Non-existent ID
            execution_type=job_event_create_request.execution_type,
            cost_component=job_event_create_request.cost_component,
            started_at=job_event_create_request.started_at,
            ended_at=job_event_create_request.ended_at,
            amount_usd=job_event_create_request.amount_usd,
            rate=job_event_create_request.rate,
            input_token_count=job_event_create_request.input_token_count,
            completion_token_count=job_event_create_request.completion_token_count,
            metadata=job_event_create_request.metadata,
        )
        with pytest.raises(JobEventCreationError, match="Execution not found"):
            admin_client.create_job_event(invalid_request)

    @pytest.mark.asyncio
    async def test_acreate_job_event_execution_not_found(
        self, admin_client: RestClient, job_event_create_request
    ):
        # Create a new request with a non-existent execution ID
        invalid_request = JobEventCreateRequest(
            execution_id=uuid4(),  # Non-existent ID
            execution_type=job_event_create_request.execution_type,
            cost_component=job_event_create_request.cost_component,
            started_at=job_event_create_request.started_at,
            ended_at=job_event_create_request.ended_at,
            amount_usd=job_event_create_request.amount_usd,
            rate=job_event_create_request.rate,
            input_token_count=job_event_create_request.input_token_count,
            completion_token_count=job_event_create_request.completion_token_count,
            metadata=job_event_create_request.metadata,
        )
        with pytest.raises(JobEventCreationError, match="Execution not found"):
            await admin_client.acreate_job_event(invalid_request)

    @pytest.mark.timeout(300)
    def test_update_job_event_success(
        self,
        admin_client: RestClient,
        job_event_create_request,
        job_event_update_request,
    ):
        create_response = admin_client.create_job_event(job_event_create_request)
        job_event_id = create_response.id

        # Should not raise an exception and return None
        result = admin_client.update_job_event(job_event_id, job_event_update_request)
        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.timeout(300)
    async def test_aupdate_job_event_success(
        self,
        admin_client: RestClient,
        job_event_create_request,
        job_event_update_request,
    ):
        create_response = await admin_client.acreate_job_event(job_event_create_request)
        job_event_id = create_response.id

        await admin_client.aupdate_job_event(job_event_id, job_event_update_request)

    def test_update_job_event_not_found(
        self, admin_client: RestClient, job_event_update_request
    ):
        job_event_id = uuid4()
        with pytest.raises(
            JobEventUpdateError, match=r"Job event with ID .* not found"
        ):
            admin_client.update_job_event(job_event_id, job_event_update_request)

    @pytest.mark.asyncio
    async def test_aupdate_job_event_not_found(
        self, admin_client: RestClient, job_event_update_request
    ):
        job_event_id = uuid4()
        with pytest.raises(
            JobEventUpdateError, match=r"Job event with ID .* not found"
        ):
            await admin_client.aupdate_job_event(job_event_id, job_event_update_request)

    @pytest.fixture
    def job_event_batch_create_request(self, test_trajectory_id: str):
        return JobEventBatchCreateRequest(
            execution_id=UUID(test_trajectory_id),
            execution_type=ExecutionType.TRAJECTORY,
            job_events=[
                JobEventBatchItemRequest(
                    cost_component=CostComponent.LLM_USAGE,
                    started_at=datetime.datetime.now(),
                    ended_at=datetime.datetime.now(),
                    amount_usd=0.005,
                    rate=0.0001,
                    input_token_count=100,
                    completion_token_count=50,
                    metadata={"model": "gpt-4o", "temperature": 0.7},
                ),
                JobEventBatchItemRequest(
                    cost_component=CostComponent.STEP,
                    started_at=datetime.datetime.now(),
                    ended_at=datetime.datetime.now(),
                    amount_usd=0.001,
                ),
            ],
        )

    @pytest.mark.asyncio
    @pytest.mark.timeout(300)
    async def test_acreate_job_events_batch_success(
        self, admin_client: RestClient, job_event_batch_create_request
    ):
        response = await admin_client.acreate_job_events_batch(
            job_event_batch_create_request
        )
        assert response.ids is not None
        assert len(response.ids) == 2
        assert response.created_count == 2
        assert all(isinstance(job_id, UUID) for job_id in response.ids)

    @pytest.mark.asyncio
    async def test_acreate_job_events_batch_execution_not_found(
        self, admin_client: RestClient, job_event_batch_create_request
    ):
        invalid_request = JobEventBatchCreateRequest(
            execution_id=uuid4(),  # Non-existent ID
            execution_type=job_event_batch_create_request.execution_type,
            job_events=job_event_batch_create_request.job_events,
        )

        with pytest.raises(
            JobEventBatchCreationError, match=r"Trajectory with ID .* not found"
        ):
            await admin_client.acreate_job_events_batch(invalid_request)
