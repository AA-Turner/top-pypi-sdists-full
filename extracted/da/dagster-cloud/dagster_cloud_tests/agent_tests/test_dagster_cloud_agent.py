import concurrent.futures
import datetime
import logging
import os
import time
import uuid
from pathlib import Path
from unittest import mock

import freezegun
import pytest
import redis
import requests
from dagster import (
    DailyPartitionsDefinition,
    RunRequest,
    asset,
    build_schedule_from_partitioned_job,
    define_asset_job,
    graph,
    in_process_executor,
    op,
    repository,
    sensor,
)
from dagster._core.definitions.selector import JobSelector
from dagster._core.errors import DagsterUserCodeUnreachableError
from dagster._core.launcher import WorkerStatus
from dagster._core.launcher.base import LaunchRunContext
from dagster._core.remote_origin import (
    RegisteredCodeLocationOrigin,
    RemoteJobOrigin,
    RemoteRepositoryOrigin,
)
from dagster._core.remote_representation.code_location import GrpcServerCodeLocation
from dagster._core.remote_representation.external_data import DEFAULT_MODE_NAME
from dagster._core.test_utils import (
    freeze_time,
    instance_for_test,
    poll_for_finished_run,
    poll_for_step_start,
)
from dagster._core.utils import make_new_run_id
from dagster._grpc.types import (
    ExecutionPlanSnapshotArgs,
    ExternalScheduleExecutionArgs,
    JobSubsetSnapshotArgs,
    NotebookPathArgs,
    PartitionArgs,
    PartitionNamesArgs,
    PartitionSetExecutionParamArgs,
    SensorExecutionArgs,
)
from dagster._serdes import serialize_value
from dagster._time import create_datetime, get_current_datetime, get_current_timestamp
from dagster._utils import file_relative_path
from dagster._utils.container import CGroupVersion
from dagster._utils.error import SerializableErrorInfo
from dagster_cloud import DagsterCloudAgentInstance
from dagster_cloud.agent import AgentQueuesConfig
from dagster_cloud.agent.dagster_cloud_agent import (
    AGENT_HEARTBEAT_INTERVAL_SECONDS,
    AGENT_MAX_THREADPOOL_WORKERS,
    AGENT_UTILIZATION_METRICS_INTERVAL_SECONDS,
    DagsterCloudAgent,
    batch_upload_api_response,
    upload_api_response,
)
from dagster_cloud.api.dagster_cloud_api import (
    AgentHeartbeat,
    DagsterCloudApi,
    DagsterCloudApiGrpcResponse,
    DagsterCloudApiSuccess,
    DagsterCloudApiUnknownCommandResponse,
    DagsterCloudUploadApiResponse,
    DagsterCloudUploadWorkspaceEntry,
    LaunchRunArgs,
    PingLocationArgs,
    TerminateRunArgs,
    TimestampedError,
)
from dagster_cloud.execution.cloud_run_launcher.process import PID_TAG
from dagster_cloud.execution.monitoring import (
    CloudCodeServerHeartbeat,
    CloudCodeServerStatus,
    CloudRunWorkerStatus,
    CloudRunWorkerStatuses,
)
from dagster_cloud.version import __version__ as DAGSTER_CLOUD_VERSION
from dagster_cloud.workspace.ecs.launcher import EcsUserCodeLauncher
from dagster_cloud.workspace.kubernetes.launcher import K8sUserCodeLauncher
from dagster_cloud.workspace.user_code_launcher import DagsterCloudUserCodeLauncher
from dagster_cloud_backend.agent_details import AgentDetails, AgentStatus
from dagster_cloud_backend.instance import (
    RECENT_AGENT_DETAILS_STALE_SECONDS,
    DeploymentScopedHostInstance,
    UnscopedHostInstance,
)
from dagster_cloud_backend.storage.host_cloud.cloud_storage.deployment import (
    DagsterCloudDeploymentMetadata,
)
from dagster_cloud_backend.storage.host_cloud.cloud_storage.implementation.postgres_cloud_storage import (
    PostgresCloudStorage,
)
from dagster_cloud_backend.storage.host_cloud.cloud_storage.integrations.branch_deployments import (
    BranchDeploymentGitMetadata,
)
from dagster_cloud_backend.storage.host_cloud.cloud_storage.schema import (
    RepositoryLocationsDataTable,
    RepositoryLocationsTable,
)
from dagster_cloud_backend.types import DeploymentAgentType
from dagster_cloud_backend.user_code.workspace import (
    dagster_cloud_api_call,
    gen_dagster_cloud_api_call,
)
from dagster_cloud_cli.core.errors import DagsterCloudHTTPError
from dagster_cloud_cli.core.graphql_client import DagsterCloudGraphQLClient
from dagster_cloud_cli.core.workspace import CodeLocationDeployData
from dagster_shared.serdes.serdes import deserialize_value
from urllib3.connection import HTTPConnection

FAKE_AGENT_UUID = str(uuid.uuid4())


def _add_location(cloud_storage, location_name="location", agent_queue=None):
    cloud_storage.add_location(
        location_name,
        code_location_deploy_data=CodeLocationDeployData(
            python_file=__file__,
            agent_queue=agent_queue,
        ),
    )

    return RegisteredCodeLocationOrigin(location_name)


@pytest.fixture
def agent(
    agent_instance,
):
    with DagsterCloudAgent(agent_instance) as agent:
        yield agent


@pytest.fixture
def agent_queues_agent(agent_queues_agent_instance):
    with DagsterCloudAgent(agent_queues_agent_instance) as agent:
        yield agent


@pytest.fixture
def user_code_launcher(agent_instance):
    user_code_launcher = agent_instance.user_code_launcher

    # Tests manually trigger reconcilation, so don't run it in a background thread
    user_code_launcher.start(run_reconcile_thread=False, run_metrics_thread=False)

    yield user_code_launcher


@pytest.fixture
def isolated_agents_user_code_launcher(isolated_agents_instance):
    user_code_launcher = isolated_agents_instance.user_code_launcher
    user_code_launcher.start(run_reconcile_thread=False, run_metrics_thread=False)

    yield user_code_launcher


@pytest.fixture
def server_ttl_user_code_launcher(server_ttl_agent_instance):
    user_code_launcher = server_ttl_agent_instance.user_code_launcher
    user_code_launcher.start(run_reconcile_thread=False, run_metrics_thread=False)

    yield user_code_launcher


@pytest.fixture
def branch_deployments_user_code_launcher(branch_deployments_agent_instance):
    user_code_launcher = branch_deployments_agent_instance.user_code_launcher
    user_code_launcher.start(run_reconcile_thread=False, run_metrics_thread=False)

    yield user_code_launcher


@pytest.fixture
def agent_queues_user_code_launcher(agent_queues_agent_instance):
    user_code_launcher = agent_queues_agent_instance.user_code_launcher
    user_code_launcher.start(run_reconcile_thread=False)

    yield user_code_launcher


@pytest.fixture(autouse=True)
def cloud_storage(host_instance):
    cloud_storage = host_instance.cloud_storage

    yield cloud_storage

    with cloud_storage.transaction() as conn:
        conn.execute(RepositoryLocationsDataTable.delete())
        conn.execute(RepositoryLocationsTable.delete())


@pytest.fixture
def user_cloud_agent_request_storage(host_instance):
    user_cloud_agent_request_storage = host_instance.user_cloud_agent_request_storage
    yield user_cloud_agent_request_storage


@pytest.fixture
def code_location(agent, agent_instance, user_code_launcher, cloud_storage):
    code_location_origin = _add_location(cloud_storage)

    _run_initial_reconcilation(agent, user_code_launcher)

    endpoint = user_code_launcher.get_grpc_endpoint("sandbox", code_location_origin.location_name)

    with GrpcServerCodeLocation(
        origin=code_location_origin,
        port=endpoint.port,
        socket=endpoint.socket,
        host=endpoint.host,
        heartbeat=True,
        watch_server=False,
        instance=agent_instance,
    ) as location:
        yield location


@pytest.fixture
def code_location_isolated_agents(
    isolated_agents_instance, isolated_agents_user_code_launcher, cloud_storage
):
    with DagsterCloudAgent(isolated_agents_instance) as agent:
        code_location_origin = _add_location(cloud_storage)

        _run_initial_reconcilation(agent, isolated_agents_user_code_launcher)

        endpoint = isolated_agents_user_code_launcher.get_grpc_endpoint(
            "sandbox", code_location_origin.location_name
        )

        with GrpcServerCodeLocation(
            origin=code_location_origin,
            port=endpoint.port,
            socket=endpoint.socket,
            host=endpoint.host,
            heartbeat=True,
            watch_server=False,
            instance=isolated_agents_instance,
        ) as location:
            yield location


@pytest.fixture
def cpu_usage_mock():
    with mock.patch(
        "dagster._utils.container._retrieve_containerized_cpu_usage",
    ) as mocker:
        yield mocker


@pytest.fixture
def cpu_cfs_quota_us_mock():
    with mock.patch(
        "dagster._utils.container._retrieve_containerized_cpu_cfs_quota_us",
    ) as mocker:
        yield mocker


@pytest.fixture
def cpu_cfs_period_us_mock():
    with mock.patch(
        "dagster._utils.container._retrieve_containerized_cpu_cfs_period_us",
    ) as mocker:
        yield mocker


@pytest.fixture
def num_cores_mock():
    with mock.patch(
        "dagster._utils.container._retrieve_containerized_num_allocated_cores"
    ) as mocker:
        yield mocker


@pytest.fixture
def mem_usage_mock():
    with mock.patch("dagster._utils.container._retrieve_containerized_memory_usage") as mocker:
        yield mocker


@pytest.fixture
def mem_limit_mock():
    with mock.patch("dagster._utils.container._retrieve_containerized_memory_limit") as mocker:
        yield mocker


@pytest.fixture
def cgroup_version_mock():
    with mock.patch("dagster._utils.container._retrieve_cgroup_version") as mocker:
        yield mocker


@op
def success():
    time.sleep(1)


@graph
def success_graph():
    success()


@op
def sleepy_op():
    start_time = time.time()
    while True:
        time.sleep(1)
        if time.time() - start_time > 120:
            raise Exception("Timed out")


@graph
def sleepy_graph():
    sleepy_op()


@sensor(name="success_job_sensor", job_name="success_job")
def success_job_sensor():
    yield RunRequest(run_key=None)


@sensor(name="sleepy_sensor", job_name="success_job")
def sleepy_sensor():
    time.sleep(5)
    yield RunRequest(run_key=None)


success_job = success_graph.to_job(
    name="success_job",
    executor_def=in_process_executor,
    partitions_def=DailyPartitionsDefinition(start_date=datetime.datetime(2020, 1, 1)),
)

daily_success_job = build_schedule_from_partitioned_job(success_job, name="daily_success_job")


sleepy_job = sleepy_graph.to_job(name="sleepy_job", executor_def=in_process_executor)


@asset
def foo():
    return 1


@asset
def bar(foo):
    return foo


@asset
def baz(bar):
    return bar


@repository
def repo():
    return [
        success_job,
        daily_success_job,
        success_job_sensor,
        sleepy_job,
        foo,
        bar,
        baz,
        define_asset_job("asset_job", selection="*bar"),
        sleepy_sensor,
    ]


def _assert_responses_for_requests(
    gen_responses,
    num_requests,
    response_type=(DagsterCloudApiGrpcResponse, DagsterCloudApiSuccess),
):
    assert len(gen_responses) == num_requests

    for gen_response in gen_responses:
        response = next(gen_response)
        assert isinstance(response, response_type), response

        assert response.thread_telemetry


def _run_to_request_completion(agent, user_code_launcher):
    # Submit requests to thread pool
    next(agent.run_iteration(user_code_launcher))

    # Wait for all futures to return before processing
    futures = agent.request_ids_to_futures.values()

    _done, not_done = concurrent.futures.wait(futures, timeout=60)
    if not_done:
        raise Exception("Futures did not finish after 60 seconds: " + str(not_done))

    num_requests = len(agent.request_ids_to_futures)

    while num_requests > 0:
        # Process all finished requests
        next(agent.run_iteration(user_code_launcher))
        # at least one request popped off the queue
        assert len(agent.request_ids_to_futures) < num_requests
        num_requests = len(agent.request_ids_to_futures)


def _wait_for_healthy_agent(instance: DeploymentScopedHostInstance, timeout: float = 5.0) -> bool:
    # has_healthy_agent reads a cache that, when stale, attempts a non-blocking lock
    # acquire to refresh. Under CI fan-out the agent's worker pool can be holding the
    # same lock at the moment of a single call, in which case the refresh is skipped
    # and the pre-heartbeat (empty) cache is returned. Poll briefly so the lock holder
    # has a chance to release. time.monotonic / time.sleep are not patched by
    # freezegun, so this remains real-time even inside freeze_time blocks.
    deadline = time.monotonic() + timeout
    while not instance.has_healthy_agent():
        if time.monotonic() >= deadline:
            return False
        time.sleep(0.05)
    return True


def _code_server_heartbeat_for_location(
    host_instance: DeploymentScopedHostInstance,
    location_name: str,
) -> CloudCodeServerHeartbeat | None:
    agent_details = host_instance.fetch_all_agent_details(include_inactive_agents=True)
    assert len(agent_details) == 1
    code_server_heartbeats = agent_details[0].last_heartbeat.code_server_heartbeats
    location_heartbeat = [
        heartbeat
        for heartbeat in code_server_heartbeats
        if heartbeat.location_name == location_name
    ]
    if not location_heartbeat:
        return None
    assert len(location_heartbeat) == 1
    return location_heartbeat[0]


def _run_initial_reconcilation(
    agent, user_code_launcher, upload_outdated=True, agent_id=FAKE_AGENT_UUID
):
    # pulls initial locations from graphql and tells the user code launcher to asynchronously
    # reconcile them
    agent._check_update_workspace(  # noqa: SLF001
        user_code_launcher, upload_outdated=upload_outdated
    )

    agent._check_add_heartbeat(  # noqa: SLF001
        agent_id, AGENT_HEARTBEAT_INTERVAL_SECONDS
    )

    # trigger the reconiliation
    user_code_launcher.reconcile()


def _verify_agent_health_metrics(
    agent: DagsterCloudAgent,
    expected_metrics: dict,
    agent_instance: DagsterCloudAgentInstance,
    cloud_storage: PostgresCloudStorage,
    host_instance: UnscopedHostInstance,
) -> None:
    agent._check_add_heartbeat(  # noqa: SLF001
        FAKE_AGENT_UUID, heartbeat_interval_seconds=0
    )
    heartbeats = cloud_storage.get_agent_heartbeats(
        host_instance.cloud_deployment,
    )
    assert len(heartbeats) == 1

    heartbeat = list(heartbeats.values()).pop()
    assert heartbeat.metadata
    assert "utilization_metrics" in heartbeat.metadata
    utilization_metrics = heartbeat.metadata["utilization_metrics"]
    assert utilization_metrics == expected_metrics


def test_grpc_server_metrics_retrieval_no_metrics(
    agent: DagsterCloudAgent,
    agent_instance: DagsterCloudAgentInstance,
    host_instance: DeploymentScopedHostInstance,
) -> None:
    # Mock out get_grpc_endpoints to return a location that pings to no metrics.
    with mock.patch.object(
        agent_instance.user_code_launcher,
        "get_grpc_endpoints",
        return_value={
            ("dep", "loc"): mock.MagicMock(
                ping=mock.MagicMock(
                    return_value={"serialized_server_utilization_metrics": ""},
                )
            )
        },
    ):
        agent_instance.user_code_launcher.update_utilization_metrics_all_locations()

        assert agent_instance.user_code_launcher._per_location_metrics == {}  # noqa: SLF001


def test_grpc_server_metrics_retrieval(
    metrics_instance: DagsterCloudAgentInstance,
    host_instance: DeploymentScopedHostInstance,
) -> None:
    with DagsterCloudAgent(metrics_instance) as agent:
        cloud_storage = host_instance.cloud_storage
        if not cloud_storage.get_organization_by_id(host_instance.organization_id):
            cloud_storage.create_organization("sandbox")
        user_code_launcher = metrics_instance.user_code_launcher
        _add_location(cloud_storage)
        _run_initial_reconcilation(agent, user_code_launcher)

        user_code_launcher.record_resource_limit_metrics_all_locations()
        user_code_launcher.update_utilization_metrics_all_locations()

        agent._check_add_heartbeat(  # noqa: SLF001
            FAKE_AGENT_UUID, heartbeat_interval_seconds=0
        )

        heartbeat = _code_server_heartbeat_for_location(host_instance, "location")
        assert heartbeat is not None

        if metrics_instance.user_code_launcher.code_server_metrics_enabled:
            assert "utilization_metrics" in heartbeat.metadata
            utilization_metrics = heartbeat.metadata["utilization_metrics"]
            assert utilization_metrics["per_api_metrics"] == {
                "Ping": {
                    "current_request_count": 1,
                }
            }
            assert "container_utilization" in utilization_metrics
            assert "request_utilization" in utilization_metrics
            assert "resource_limits" in utilization_metrics
            assert list(utilization_metrics["resource_limits"].keys()) == ["process"]
        else:
            assert heartbeat.metadata == {}


@pytest.fixture(
    params=[True, False, None],
    ids=["enabled", "disabled", "unset"],
)
def metrics_instance(agent_token, ursula_graphql_client, request):
    config = {
        "instance_class": {
            "module": "dagster_cloud",
            "class": "DagsterCloudAgentInstance",
        },
        "user_code_launcher": {
            "module": "dagster_cloud.workspace.user_code_launcher",
            "class": "ProcessUserCodeLauncher",
            "config": {
                "wait_for_processes": True,
            },
        },
        "dagster_cloud_api": {
            "url": "http://localhost:2874",
            "agent_token": agent_token,
            "deployment": "sandbox",
        },
        "compute_logs": {
            "module": "dagster._core.storage.noop_compute_log_manager",
            "class": "NoOpComputeLogManager",
        },
    }

    if request.param is not None:
        config["user_code_launcher"]["config"]["agent_metrics"] = {"enabled": request.param}
        config["user_code_launcher"]["config"]["code_server_metrics"] = {"enabled": request.param}

    with instance_for_test(config) as instance:
        yield instance


def test_agent_heartbeat_utilization_metrics(
    metrics_instance,
    cloud_storage,
    host_instance,
    user_code_launcher,
    code_location,
):
    remote_repository = code_location.get_repository("repo")
    with DagsterCloudAgent(metrics_instance) as agent:
        agent._check_update_workspace(  # noqa: SLF001
            user_code_launcher,
            upload_outdated=True,
        )
        agent._update_utilization_metrics(user_code_launcher)  # noqa: SLF001
        # Simulate enough time passing for the agent to update utilization metrics on the next pass.
        freeze_datetime = get_current_datetime() + datetime.timedelta(
            seconds=AGENT_UTILIZATION_METRICS_INTERVAL_SECONDS
        )
        with freeze_time(freeze_datetime):
            agent._check_add_heartbeat(  # noqa: SLF001
                FAKE_AGENT_UUID, heartbeat_interval_seconds=0
            )
            heartbeats = cloud_storage.get_agent_heartbeats(
                host_instance.cloud_deployment,
            )
            assert len(heartbeats) == 1

            heartbeat = list(heartbeats.values()).pop()
            assert "utilization_metrics" in heartbeat.metadata
            expected_metrics = {
                "max_concurrent_requests": AGENT_MAX_THREADPOOL_WORKERS,
                "num_running_requests": 0,
                "num_queued_requests": 0,
            }
            if metrics_instance.user_code_launcher.agent_metrics_enabled:
                assert (
                    heartbeat.metadata["utilization_metrics"]["request_utilization"]
                    == expected_metrics
                )
            else:
                assert heartbeat.metadata["utilization_metrics"] == {}

            # trigger 5 sensor executions, expect that the heartbeat metrics are updated to reflect
            for _ in range(5):
                gen_response = gen_dagster_cloud_api_call(
                    host_instance,
                    DagsterCloudApi.GET_EXTERNAL_SENSOR_EXECUTION_DATA,
                    SensorExecutionArgs(
                        repository_origin=remote_repository.get_remote_origin(),
                        instance_ref=metrics_instance.get_ref(),
                        sensor_name="sleepy_sensor",
                        last_tick_completion_time=None,
                        last_run_key=None,
                        cursor=None,
                    ),
                )
                next(gen_response)

            # Submit all requests to thread pool, and update health metrics.
            next(agent.run_iteration(user_code_launcher))
            agent._check_add_heartbeat(  # noqa: SLF001
                FAKE_AGENT_UUID, heartbeat_interval_seconds=0
            )
            heartbeats = cloud_storage.get_agent_heartbeats(
                host_instance.cloud_deployment,
            )
            assert len(heartbeats) == 1

            heartbeat = list(heartbeats.values()).pop()
            assert "utilization_metrics" in heartbeat.metadata
            expected_metrics = {
                "max_concurrent_requests": AGENT_MAX_THREADPOOL_WORKERS,
                "num_running_requests": 5,
                "num_queued_requests": 0,
            }
            if metrics_instance.user_code_launcher.agent_metrics_enabled:
                assert (
                    heartbeat.metadata["utilization_metrics"]["request_utilization"]
                    == expected_metrics
                )
            else:
                assert heartbeat.metadata["utilization_metrics"] == {}


def test_agent_heartbeat_resource_metrics(
    metrics_instance: DagsterCloudAgentInstance,
    cloud_storage: PostgresCloudStorage,
    host_instance: UnscopedHostInstance,
    user_code_launcher: DagsterCloudUserCodeLauncher,
    cpu_usage_mock: mock.MagicMock,
    cpu_cfs_period_us_mock: mock.MagicMock,
    cpu_cfs_quota_us_mock: mock.MagicMock,
    num_cores_mock: mock.MagicMock,
    mem_usage_mock: mock.MagicMock,
    mem_limit_mock: mock.MagicMock,
    cgroup_version_mock: mock.MagicMock,
) -> None:
    freeze_datetime = create_datetime(2020, 1, 1)
    with DagsterCloudAgent(metrics_instance) as agent:
        with freeze_time(freeze_datetime):
            agent._check_update_workspace(  # noqa: SLF001
                user_code_launcher,
                upload_outdated=True,
            )
            # Test the case where no metrics are successfully retrieved.
            cpu_usage_mock.return_value = None
            cpu_cfs_period_us_mock.return_value = None
            cpu_cfs_quota_us_mock.return_value = None
            num_cores_mock.return_value = None
            mem_usage_mock.return_value = None
            mem_limit_mock.return_value = None
            cgroup_version_mock.return_value = None

            # Update once to set initial state (since the agent initializes metrics on startup, before mocks apply)
            agent._update_utilization_metrics(user_code_launcher=user_code_launcher)  # noqa: SLF001
            # Update again to set second state
            agent._update_utilization_metrics(user_code_launcher=user_code_launcher)  # noqa: SLF001
            expected_metrics = (
                {
                    "request_utilization": {
                        "max_concurrent_requests": AGENT_MAX_THREADPOOL_WORKERS,
                        "num_running_requests": 0,
                        "num_queued_requests": 0,
                    },
                    "container_utilization": {
                        "cgroup_version": None,
                        "cpu_usage": None,
                        "num_allocated_cores": None,
                        "cpu_cfs_quota_us": None,
                        "cpu_cfs_period_us": None,
                        "memory_usage": None,
                        "memory_limit": None,
                        "previous_cpu_usage": None,
                        "previous_measurement_timestamp": freeze_datetime.timestamp(),
                        "measurement_timestamp": freeze_datetime.timestamp(),
                    },
                    "resource_limits": {},
                }
                if metrics_instance.user_code_launcher.agent_metrics_enabled
                else {}
            )

            _verify_agent_health_metrics(
                agent, expected_metrics, metrics_instance, cloud_storage, host_instance
            )

            cpu_usage_mock.return_value = 1000
            cpu_cfs_period_us_mock.return_value = 1000
            cpu_cfs_quota_us_mock.return_value = 1000
            num_cores_mock.return_value = 4
            mem_usage_mock.return_value = 1000
            mem_limit_mock.return_value = 1000
            cgroup_version_mock.return_value = CGroupVersion.V1

            agent._update_utilization_metrics(user_code_launcher)  # noqa: SLF001

            expected_metrics = (
                {
                    "request_utilization": {
                        "num_running_requests": 0,
                        "max_concurrent_requests": AGENT_MAX_THREADPOOL_WORKERS,
                        "num_queued_requests": 0,
                    },
                    "container_utilization": {
                        "cgroup_version": "V1",
                        "cpu_usage": 1000,
                        "cpu_cfs_quota_us": 1000,
                        "cpu_cfs_period_us": 1000,
                        "num_allocated_cores": 4,
                        "memory_usage": 1000,
                        "memory_limit": 1000,
                        "previous_cpu_usage": None,
                        "previous_measurement_timestamp": freeze_datetime.timestamp(),
                        "measurement_timestamp": freeze_datetime.timestamp(),
                    },
                    "resource_limits": {},
                }
                if metrics_instance.user_code_launcher.agent_metrics_enabled
                else {}
            )
            _verify_agent_health_metrics(
                agent, expected_metrics, metrics_instance, cloud_storage, host_instance
            )

        original_freeze_datetime = freeze_datetime
        freeze_datetime = freeze_datetime + datetime.timedelta(
            seconds=AGENT_HEARTBEAT_INTERVAL_SECONDS
        )
        with freeze_time(freeze_datetime):
            cpu_usage_mock.return_value = 1000
            num_cores_mock.return_value = 4
            mem_usage_mock.return_value = 500
            mem_limit_mock.return_value = 1000
            agent._update_utilization_metrics(user_code_launcher)  # noqa: SLF001

            expected_metrics = (
                {
                    "request_utilization": {
                        "num_running_requests": 0,
                        "max_concurrent_requests": AGENT_MAX_THREADPOOL_WORKERS,
                        "num_queued_requests": 0,
                    },
                    "container_utilization": {
                        "cgroup_version": "V1",
                        "cpu_usage": 1000,
                        "cpu_cfs_quota_us": 1000,
                        "cpu_cfs_period_us": 1000,
                        "num_allocated_cores": 4,
                        "memory_usage": 500,
                        "memory_limit": 1000,
                        "previous_cpu_usage": 1000,
                        "previous_measurement_timestamp": original_freeze_datetime.timestamp(),
                        "measurement_timestamp": freeze_datetime.timestamp(),
                    },
                    "resource_limits": {},
                }
                if metrics_instance.user_code_launcher.agent_metrics_enabled
                else {}
            )
            _verify_agent_health_metrics(
                agent, expected_metrics, metrics_instance, cloud_storage, host_instance
            )


@pytest.mark.parametrize("upload_outdated", [True, False])
def test_initial_reconcilation_populates_servers(
    agent,
    agent_instance,
    user_code_launcher,
    host_instance,
    cloud_storage,
    upload_outdated,
):
    _add_location(cloud_storage, location_name="location1")

    with pytest.raises(Exception):
        user_code_launcher.get_grpc_endpoint("sandbox", "location1")

    agent._check_update_workspace(  # noqa: SLF001
        user_code_launcher, upload_outdated=upload_outdated
    )

    agent._check_add_heartbeat(  # noqa: SLF001
        FAKE_AGENT_UUID, heartbeat_interval_seconds=0
    )

    assert (
        _code_server_heartbeat_for_location(host_instance, "location1").server_status  # ty: ignore[unresolved-attribute]
        == CloudCodeServerStatus.STARTING
    )

    # trigger the reconiliation
    user_code_launcher.reconcile()

    agent._check_add_heartbeat(  # noqa: SLF001
        FAKE_AGENT_UUID, heartbeat_interval_seconds=0
    )

    assert (
        _code_server_heartbeat_for_location(host_instance, "location1").server_status  # ty: ignore[unresolved-attribute]
        == CloudCodeServerStatus.RUNNING
    )

    assert user_code_launcher.get_grpc_endpoint("sandbox", "location1")

    location_entry = cloud_storage.get_workspace_location_entry("location1")

    if upload_outdated:
        assert location_entry.code_location
    else:
        # Does not automatically upload
        assert not location_entry.load_error
        assert not location_entry.code_location


def test_upload_outdated_only_uploads_outdated_locations(
    agent,
    agent_instance,
    user_code_launcher,
    host_instance,
    cloud_storage,
):
    """Verify that upload_outdated=True only queues locations the control plane marks as outdated,
    not all locations.
    """
    # Set up location1 and fully reconcile so its data is uploaded (no longer outdated)
    _add_location(cloud_storage, location_name="location1")
    _run_initial_reconcilation(agent, user_code_launcher, upload_outdated=True)

    location1_entry = cloud_storage.get_workspace_location_entry("location1")
    assert location1_entry.code_location, "location1 should have data uploaded after reconciliation"

    # Now add a new location2 which has no data uploaded yet (outdated)
    _add_location(cloud_storage, location_name="location2")

    # Query workspace with upload_outdated=True — only location2 should be queued for upload
    # Call _query_for_workspace_updates directly to bypass the time-based throttle
    agent._query_for_workspace_updates(  # noqa: SLF001
        user_code_launcher, upload_outdated=True
    )

    upload_locations = user_code_launcher._upload_locations  # noqa: SLF001
    assert ("sandbox", "location2") in upload_locations, (
        "location2 (outdated) should be queued for upload"
    )
    assert ("sandbox", "location1") not in upload_locations, (
        "location1 (up-to-date) should NOT be queued for upload"
    )


def _test_check_initial_deployment_names(agent_token, ursula_graphql_client, agent, agent_instance):
    invalid_deployment = "blargh"

    with instance_for_test(
        {
            "instance_class": {
                "module": "dagster_cloud",
                "class": "DagsterCloudAgentInstance",
            },
            "user_code_launcher": {
                "module": "dagster_cloud.workspace.user_code_launcher",
                "class": "ProcessUserCodeLauncher",
                "config": {
                    "wait_for_processes": True,
                },
            },
            "dagster_cloud_api": {
                "url": "http://localhost:2874",
                "agent_token": agent_token,
                "deployment": invalid_deployment,
            },
            "compute_logs": {
                "module": "dagster._core.storage.noop_compute_log_manager",
                "class": "NoOpComputeLogManager",
            },
        }
    ) as invalid_instance:
        with DagsterCloudAgent(invalid_instance) as invalid_agent:  # ty: ignore[invalid-argument-type]
            with pytest.raises(
                Exception,
                match=f"Agent is configured to serve an invalid deployment {invalid_deployment}.",
            ):
                invalid_agent._check_initial_deployment_names()  # noqa: SLF001
    agent._check_initial_deployment_names()  # noqa: SLF001


def test_location_import_error(
    agent,
    agent_instance,
    user_code_launcher,
    cloud_storage,
):
    cloud_storage.add_location(
        "location_does_not_exist",
        code_location_deploy_data=CodeLocationDeployData(package_name="does_not_exist"),
    )
    agent._check_update_workspace(  # noqa: SLF001
        user_code_launcher, upload_outdated=False
    )

    agent._check_add_heartbeat(  # noqa: SLF001
        FAKE_AGENT_UUID, heartbeat_interval_seconds=0
    )

    # trigger the reconiliation
    user_code_launcher.reconcile()

    with pytest.raises(Exception, match="ImportError: `No module named 'does_not_exist'`"):
        user_code_launcher.get_grpc_endpoint("sandbox", "location_does_not_exist")


def _execution_plan_api_call(host_instance, code_location_origin):
    pipeline_origin = RemoteJobOrigin(
        job_name="success_job",
        repository_origin=RemoteRepositoryOrigin(
            repository_name="repo",
            code_location_origin=code_location_origin,
        ),
    )
    request_args = ExecutionPlanSnapshotArgs(
        job_origin=pipeline_origin,
        asset_selection=None,
        op_selection=[],
        run_config={},
        mode=DEFAULT_MODE_NAME,
        step_keys_to_execute=None,
        job_snapshot_id="fake_pipeline_snapshot_id",
        known_state=None,
    )
    return gen_dagster_cloud_api_call(
        host_instance,
        DagsterCloudApi.GET_EXTERNAL_EXECUTION_PLAN,
        request_args,
    )


def test_agent_heartbeat_truncation(
    agent_instance_local_ursula: DagsterCloudAgentInstance,
    host_instance: DeploymentScopedHostInstance,
):
    agent_instance = agent_instance_local_ursula
    with DagsterCloudAgent(agent_instance_local_ursula) as agent:
        host_instance.cloud_storage.wipe_agent_heartbeats()
        assert not host_instance.cloud_storage.get_agent_heartbeats()

        run_id_1 = make_new_run_id()
        run_id_2 = make_new_run_id()

        code_server_heartbeats = [
            CloudCodeServerHeartbeat(
                location_name="foo",
                server_status=CloudCodeServerStatus.RUNNING,
                error=None,
                metadata={
                    "utilization_metrics": {
                        "resource_limits": {
                            "ecs": {"cpu_limit": "1024"},
                        },
                        "container_utilization": {
                            "container_utilization": {
                                "memory_usage": 1024**2,
                            },
                            "num_allocated_cores": 2,
                        },
                        "request_utilization": {},
                        "per_api_metrics": {},
                    }
                },
            ),
            CloudCodeServerHeartbeat(
                location_name="quux",
                server_status=CloudCodeServerStatus.FAILED,
                error=SerializableErrorInfo("oops", ["i", "goofed"], "OopsException"),
                metadata={},
            ),
        ]
        run_worker_heartbeats = CloudRunWorkerStatuses(
            statuses=[
                CloudRunWorkerStatus(
                    run_id=run_id_1,
                    status_type=WorkerStatus.RUNNING,
                    message="all good",
                    transient=None,
                    run_worker_id="hi",
                ),
                CloudRunWorkerStatus(
                    run_id=run_id_2,
                    status_type=WorkerStatus.FAILED,
                    message="oops",
                    transient=False,
                    run_worker_id="bye",
                ),
            ],
            run_worker_monitoring_supported=True,
            run_worker_monitoring_thread_alive=True,
        )

        now = time.time()

        heartbeat_with_messages_and_errors = AgentHeartbeat(
            timestamp=now,
            agent_id="nonce",
            agent_label="My label",
            agent_type="Process",
            errors=[
                TimestampedError(
                    timestamp=now - 100,
                    error=SerializableErrorInfo(
                        "Oops", ["My", "agent", "crashed"], cls_name="AgentError"
                    ),
                )
            ],
            metadata={
                "image_tag": "master",
                "utilization_metrics": {
                    "container_utilization": {
                        "container_utilization": {
                            "memory_usage": 1024**2,
                        },
                        "num_allocated_cores": 2,
                    },
                    "request_utilization": {},
                    "resource_limits": {},
                },
            },
            run_worker_statuses=run_worker_heartbeats,
            code_server_heartbeats=code_server_heartbeats,
            agent_queues_config=AgentQueuesConfig(
                include_default_queue=False, additional_queues=["foo", "bar"]
            ),
        )

        heartbeat_without_messages_and_errors = AgentHeartbeat(
            timestamp=now,
            agent_id="nonce",
            agent_label="My label",
            agent_type="Process",
            errors=[],
            metadata={
                "image_tag": "master",
            },
            run_worker_statuses=CloudRunWorkerStatuses(
                statuses=[
                    CloudRunWorkerStatus(
                        run_id=run_id_1,
                        status_type=WorkerStatus.RUNNING,
                        message="",
                        transient=None,
                        run_worker_id="hi",
                    ),
                    CloudRunWorkerStatus(
                        run_id=run_id_2,
                        status_type=WorkerStatus.FAILED,
                        message="",
                        transient=False,
                        run_worker_id="bye",
                    ),
                ],
                run_worker_monitoring_supported=True,
                run_worker_monitoring_thread_alive=True,
            ),
            code_server_heartbeats=[
                CloudCodeServerHeartbeat(
                    location_name="foo",
                    server_status=CloudCodeServerStatus.RUNNING,
                    error=None,
                    metadata={},
                ),
                CloudCodeServerHeartbeat(
                    location_name="quux",
                    server_status=CloudCodeServerStatus.FAILED,
                    error=None,
                    metadata={},
                ),
            ],
            agent_queues_config=AgentQueuesConfig(
                include_default_queue=False, additional_queues=["foo", "bar"]
            ),
        )

        assert (
            heartbeat_with_messages_and_errors.without_messages_and_errors()
            == heartbeat_without_messages_and_errors
        )

        agent._check_update_workspace(  # noqa: SLF001
            agent_instance.user_code_launcher, upload_outdated=True
        )

        with mock.patch.object(
            agent_instance.user_code_launcher, "get_cloud_run_worker_statuses"
        ) as mock_get_cloud_run_worker_statuses:
            mock_get_cloud_run_worker_statuses.return_value = {
                host_instance.cloud_deployment.name: run_worker_heartbeats
            }

            with mock.patch.object(
                agent_instance.user_code_launcher, "get_grpc_server_heartbeats"
            ) as mock_get_grpc_server_heartbeats:
                mock_get_grpc_server_heartbeats.return_value = {
                    host_instance.cloud_deployment.name: code_server_heartbeats
                }

                # Add the full heartbeat, verify it was applied
                agent._check_add_heartbeat(  # noqa: SLF001
                    FAKE_AGENT_UUID, heartbeat_interval_seconds=0
                )

                heartbeat = next(iter(host_instance.cloud_storage.get_agent_heartbeats().values()))

                assert heartbeat.code_server_heartbeats == code_server_heartbeats
                assert heartbeat.run_worker_statuses == run_worker_heartbeats

                # Simulate a 413 on the first request, verify the slimmed down heartbeat is stored
                # instead
                original_graphql_execute = DagsterCloudGraphQLClient.execute
                num_called = {"called": 0}

                def _mock_execute(*args, **kwargs):
                    # Raise a 413 if there is any metadata
                    num_called["called"] += 1

                    if num_called["called"] == 1:
                        mock_response = mock.Mock(spec=requests.Response)
                        mock_response.status_code = 413
                        mock_response.content = b"Too big"
                        raise DagsterCloudHTTPError(
                            requests.HTTPError("Too big", response=mock_response)
                        )

                    return original_graphql_execute(*args, **kwargs)

                with mock.patch.object(DagsterCloudGraphQLClient, "execute", _mock_execute):
                    agent._check_add_heartbeat(  # noqa: SLF001
                        FAKE_AGENT_UUID, heartbeat_interval_seconds=0
                    )
                    heartbeat = next(
                        iter(host_instance.cloud_storage.get_agent_heartbeats().values())
                    )

                    # Heartbeat succeeded on retry with the slimmed down heartbeats

                    assert (
                        heartbeat.code_server_heartbeats
                        == heartbeat_without_messages_and_errors.code_server_heartbeats
                    )
                    assert (
                        heartbeat.run_worker_statuses
                        == heartbeat_without_messages_and_errors.run_worker_statuses
                    )


def test_agent_with_ttl(
    server_ttl_agent_instance,
    server_ttl_user_code_launcher,
    host_instance,
    cloud_storage,
):
    with DagsterCloudAgent(server_ttl_agent_instance) as agent:
        user_code_launcher = server_ttl_user_code_launcher

        now = time.time()

        location_add_time = now - 10
        with mock.patch("time.time", mock.MagicMock(return_value=location_add_time)):
            code_location_origin = _add_location(cloud_storage)

        with pytest.raises(Exception):
            user_code_launcher.get_grpc_endpoint("sandbox", code_location_origin.location_name)

        # Reconciliation does not create the endpoint since nothing has asked for the location yet
        _run_initial_reconcilation(agent, user_code_launcher)

        with pytest.raises(Exception):
            user_code_launcher.get_grpc_endpoint("sandbox", code_location_origin.location_name)

        # But it's still heartbeating nonetheless
        assert host_instance.has_healthy_agent()

        assert not _code_server_heartbeat_for_location(
            host_instance, code_location_origin.location_name
        )

        gen_responses = []

        first_response = _execution_plan_api_call(
            host_instance,
            code_location_origin,
        )

        gen_responses.append(first_response)
        next(first_response)

        next(agent.run_iteration(user_code_launcher))
        assert len(agent._pending_requests) == 1  # noqa: SLF001

        # Stays pending until a reconciliation happens
        next(agent.run_iteration(user_code_launcher))
        assert len(agent._pending_requests) == 1  # noqa: SLF001

        # Once we update the workspace and reconcile, the next iteration actually
        # runs the request since the server is now up to date
        agent._query_for_workspace_updates(  # noqa: SLF001
            user_code_launcher, upload_outdated=False
        )

        agent._check_add_heartbeat(  # noqa: SLF001
            FAKE_AGENT_UUID, heartbeat_interval_seconds=0
        )

        assert (
            _code_server_heartbeat_for_location(
                host_instance, code_location_origin.location_name
            ).server_status  # ty: ignore[unresolved-attribute]
            == CloudCodeServerStatus.STARTING
        )

        user_code_launcher.reconcile()
        user_code_launcher.get_grpc_endpoint("sandbox", code_location_origin.location_name)

        agent._check_add_heartbeat(  # noqa: SLF001
            FAKE_AGENT_UUID, heartbeat_interval_seconds=0
        )

        assert (
            _code_server_heartbeat_for_location(
                host_instance, code_location_origin.location_name
            ).server_status  # ty: ignore[unresolved-attribute]
            == CloudCodeServerStatus.RUNNING
        )

        next(agent.run_iteration(user_code_launcher))
        assert len(agent._pending_requests) == 0  # noqa: SLF001

        # A new request is served immediately since the server is now up and the TTL
        # has not expired
        second_response = _execution_plan_api_call(
            host_instance,
            code_location_origin,
        )
        gen_responses.append(second_response)
        next(second_response)

        next(agent.run_iteration(user_code_launcher))
        assert len(agent._pending_requests) == 0  # noqa: SLF001

        _run_to_request_completion(agent, user_code_launcher)

        _assert_responses_for_requests(gen_responses, 2)

        # When the metadata timestamp is updated, requests still are served right away
        location_add_time = now - 5
        with mock.patch("time.time", mock.MagicMock(return_value=location_add_time)):
            cloud_storage.mark_location_out_of_date("location")

        third_response = _execution_plan_api_call(
            host_instance,
            code_location_origin,
        )
        next(third_response)
        next(agent.run_iteration(user_code_launcher))
        assert len(agent._pending_requests) == 0  # noqa: SLF001

        agent._query_for_workspace_updates(  # noqa: SLF001
            user_code_launcher, upload_outdated=False
        )

        user_code_launcher.reconcile()
        next(agent.run_iteration(user_code_launcher))
        assert len(agent._pending_requests) == 0  # noqa: SLF001

        _run_to_request_completion(agent, user_code_launcher)
        _assert_responses_for_requests([third_response], 1)

        # After the TTL has passed, the servers are spun down
        with mock.patch(
            "time.time",
            mock.MagicMock(
                return_value=time.time() + 1.5 * user_code_launcher.full_deployment_ttl_seconds
            ),
        ):
            agent._query_for_workspace_updates(  # noqa: SLF001
                user_code_launcher, upload_outdated=False
            )

        user_code_launcher.reconcile()

        # RIP Server
        with pytest.raises(Exception):
            user_code_launcher.get_grpc_endpoint("sandbox", code_location_origin.location_name)

        # But it rises once more once a new request comes in (as soon as a reconcilation
        # happens)
        last_response = _execution_plan_api_call(
            host_instance,
            code_location_origin,
        )
        next(last_response)
        next(agent.run_iteration(user_code_launcher))
        assert len(agent._pending_requests) == 1  # noqa: SLF001

        agent._query_for_workspace_updates(  # noqa: SLF001
            user_code_launcher, upload_outdated=False
        )

        user_code_launcher.reconcile()
        user_code_launcher.get_grpc_endpoint("sandbox", code_location_origin.location_name)

        _run_to_request_completion(agent, user_code_launcher)

        _assert_responses_for_requests([last_response], 1)


def test_upload_error_written(
    host_instance,
    agent,
    agent_instance,
    cloud_storage,
):
    user_code_launcher = agent_instance.user_code_launcher
    # clear snapshots to ensure we have to upload
    host_instance.blob_object_store.wipe_for_test()

    class SpecialException(Exception): ...

    def _raise(*_a, **_k):
        raise SpecialException()

    with mock.patch.object(user_code_launcher, "upload_job_snap_direct", new=_raise):
        _add_location(cloud_storage, "error_loc")

        _run_initial_reconcilation(agent, user_code_launcher, upload_outdated=False)

        dagster_cloud_api_call(
            host_instance,
            DagsterCloudApi.CHECK_FOR_WORKSPACE_UPDATES,
            wait_for_response=False,
        )
        _run_to_request_completion(agent, user_code_launcher)
        user_code_launcher.reconcile()

    location_entries = host_instance.cloud_storage.all_workspace_location_entries()
    assert location_entries.get("error_loc")
    assert location_entries["error_loc"].load_error
    assert SpecialException.__name__ in location_entries["error_loc"].load_error.to_string()


def test_check_for_workspace_updates_affects_ttl(
    server_ttl_agent_instance,
    server_ttl_user_code_launcher,
    host_instance,
    cloud_storage,
):
    with DagsterCloudAgent(server_ttl_agent_instance) as agent:
        user_code_launcher = server_ttl_user_code_launcher

        now = time.time()

        _run_initial_reconcilation(agent, user_code_launcher)

        location_add_time = now - 10
        with mock.patch("time.time", mock.MagicMock(return_value=location_add_time)):
            code_location_origin = _add_location(cloud_storage)

        with pytest.raises(Exception):
            user_code_launcher.get_grpc_endpoint("sandbox", code_location_origin.location_name)

        dagster_cloud_api_call(
            host_instance,
            DagsterCloudApi.CHECK_FOR_WORKSPACE_UPDATES,
            wait_for_response=False,
        )
        _run_to_request_completion(agent, user_code_launcher)
        user_code_launcher.reconcile()

        user_code_launcher.get_grpc_endpoint("sandbox", code_location_origin.location_name)

        assert cloud_storage.get_workspace_location_entry("location").code_location

        # Server stays up after the next reconcilation loop too

        agent._query_for_workspace_updates(  # noqa: SLF001
            user_code_launcher, upload_outdated=False
        )
        user_code_launcher.reconcile()

        user_code_launcher.get_grpc_endpoint("sandbox", code_location_origin.location_name)

        # Requests about the location now return immediately without waiting for
        # reconciliation since the server was used to update metadata and it sticks around
        response = _execution_plan_api_call(
            host_instance,
            code_location_origin,
        )
        next(response)
        next(agent.run_iteration(user_code_launcher))
        assert len(agent._pending_requests) == 0  # noqa: SLF001

        _run_to_request_completion(agent, user_code_launcher)

        _assert_responses_for_requests([response], 1)


def test_ping_location_affects_ttl(
    server_ttl_agent_instance,
    server_ttl_user_code_launcher,
    host_instance,
    cloud_storage,
):
    with DagsterCloudAgent(server_ttl_agent_instance) as agent:
        user_code_launcher = server_ttl_user_code_launcher

        _run_initial_reconcilation(agent, user_code_launcher)

        code_location_origin = _add_location(cloud_storage)

        # Sending a PING_LOCATION request makes the gRPC server available

        dagster_cloud_api_call(
            host_instance,
            DagsterCloudApi.PING_LOCATION,
            request_args=PingLocationArgs(location_name=code_location_origin.location_name),
            wait_for_response=False,
        )

        next(agent.run_iteration(user_code_launcher))

        agent._query_for_workspace_updates(  # noqa: SLF001
            user_code_launcher, upload_outdated=False
        )

        user_code_launcher.reconcile()

        user_code_launcher.get_grpc_endpoint("sandbox", code_location_origin.location_name)


def test_wait_to_pull_requests_after_limit(
    server_ttl_agent_instance,
    server_ttl_user_code_launcher,
    host_instance,
    cloud_storage,
):
    # Verifies that if enough pending requests builds up, the agent waits to pull more
    # until the location
    agent_instance = server_ttl_agent_instance
    user_code_launcher = server_ttl_user_code_launcher
    request_limit = 3

    with DagsterCloudAgent(agent_instance, pending_requests_limit=request_limit) as agent:
        _run_initial_reconcilation(agent, user_code_launcher)

        code_location_origin = _add_location(cloud_storage)

        # Put enough pending requests on the queue to hit the limit
        api_calls = []
        for _i in range(request_limit):
            api_call = _execution_plan_api_call(
                host_instance,
                code_location_origin,
            )
            next(api_call)
            api_calls.append(api_call)

        next(agent.run_iteration(user_code_launcher))
        assert len(agent._pending_requests) == 3  # noqa: SLF001
        # Agent is now at the limit, new requests should not be processed until existing requests are processed

        # add more requests
        for _i in range(request_limit):
            api_call = _execution_plan_api_call(
                host_instance,
                code_location_origin,
            )
            next(api_call)
            api_calls.append(api_call)

        next(agent.run_iteration(user_code_launcher))

        # Still at 3 (didn't fetch the new requests from the queue)
        assert len(agent._pending_requests) == 3  # noqa: SLF001

        # Once a reconcilation happens and the queue goes back down to 0, subsequent requests will start again
        agent._query_for_workspace_updates(  # noqa: SLF001
            user_code_launcher, upload_outdated=False
        )

        user_code_launcher.reconcile()

        next(agent.run_iteration(user_code_launcher))

        assert len(agent._pending_requests) == 0  # noqa: SLF001

        # The next iteration picks up new requests again and we're back to normal

        next(agent.run_iteration(user_code_launcher))

        assert len(agent._pending_requests) == 0  # noqa: SLF001

        _run_to_request_completion(agent, user_code_launcher)

        _assert_responses_for_requests(api_calls, 6)


def test_max_server_limit(
    agent,
    server_ttl_agent_instance,
    server_ttl_user_code_launcher,
    host_instance,
    cloud_storage,
):
    # Verifies that the max_servers field is respected for locations with TTLs
    with DagsterCloudAgent(server_ttl_agent_instance) as agent:
        agent_instance = server_ttl_agent_instance
        user_code_launcher = server_ttl_user_code_launcher

        _run_initial_reconcilation(agent, user_code_launcher)

        max_servers = agent_instance.user_code_launcher.server_ttl_max_servers

        assert max_servers == 5

        origins = {}

        now = time.time()

        api_calls = []

        num_locations = max_servers + 2

        # Add enough servers that we will have to make some hard choices
        for i in range(num_locations):
            origins[i] = _add_location(cloud_storage, f"location_{i}")
            # Each makes a call one second papart
            with mock.patch("time.time", mock.MagicMock(return_value=now + i)):
                api_call = _execution_plan_api_call(
                    host_instance,
                    origins[i],
                )
                next(api_call)
                api_calls.append(api_call)
                next(agent.run_iteration(user_code_launcher))

        assert len(agent._pending_requests) == num_locations  # noqa: SLF001

        agent._query_for_workspace_updates(  # noqa: SLF001
            user_code_launcher, upload_outdated=False
        )
        user_code_launcher.reconcile()

        # More than max servers were created, because they all have pending requests
        assert len(user_code_launcher.get_grpc_endpoints()) == num_locations

        # As soon as the pending requests are cleared, we drop down to max_servers, picking
        # the ones that were most recently queried
        _run_to_request_completion(agent, user_code_launcher)

        agent._query_for_workspace_updates(  # noqa: SLF001
            user_code_launcher, upload_outdated=False
        )
        user_code_launcher.reconcile()

        assert len(user_code_launcher.get_grpc_endpoints()) == max_servers

        # The 5 most recently queries locations are the ones included
        assert set(user_code_launcher.get_grpc_endpoints().keys()) == {
            ("sandbox", location)
            for location in {
                "location_2",
                "location_3",
                "location_4",
                "location_5",
                "location_6",
            }
        }


def test_location_removal_clears_pending_requests(
    server_ttl_agent_instance,
    server_ttl_user_code_launcher,
    host_instance,
    cloud_storage,
):
    with DagsterCloudAgent(server_ttl_agent_instance) as agent:
        user_code_launcher = server_ttl_user_code_launcher

        now = time.time()

        _run_initial_reconcilation(agent, user_code_launcher)

        location_add_time = now - 10
        with mock.patch("time.time", mock.MagicMock(return_value=location_add_time)):
            code_location_origin = _add_location(cloud_storage)

        api_calls = [
            _execution_plan_api_call(
                host_instance,
                code_location_origin,
            ),
            _execution_plan_api_call(
                host_instance,
                code_location_origin,
            ),
        ]
        for api_call in api_calls:
            next(api_call)

        next(agent.run_iteration(user_code_launcher))

        assert len(agent._pending_requests) == 2  # noqa: SLF001

        # Deleting the location fires any pending requests for that location
        # immediately after the next reconcilation (returning an error to the
        # caller about the location being unloadable)
        cloud_storage.delete_location("location")

        next(agent.run_iteration(user_code_launcher))
        assert len(agent._pending_requests) == 2  # noqa: SLF001

        agent._query_for_workspace_updates(  # noqa: SLF001
            user_code_launcher, upload_outdated=False
        )

        next(agent.run_iteration(user_code_launcher))
        assert len(agent._pending_requests) == 0  # noqa: SLF001

        _run_to_request_completion(agent, user_code_launcher)

        for api_call in api_calls:
            with pytest.raises(
                DagsterUserCodeUnreachableError,
                match="No server endpoint exists for sandbox:location",
            ):
                next(api_call)


def test_agent_metadata(
    agent_instance,
    user_code_launcher,
    host_instance,
):
    with DagsterCloudAgent(agent_instance) as agent:
        _run_initial_reconcilation(agent, user_code_launcher)

        agent_details: list[AgentDetails] = host_instance.fetch_all_agent_details(
            include_inactive_agents=True
        )
        assert len(agent_details) == 1
        assert agent_details[0].status == AgentStatus.RUNNING
        assert agent_details[0].agent_id == FAKE_AGENT_UUID
        assert agent_details[0].metadata.get("type") == "ProcessUserCodeLauncher"
        assert agent_details[0].metadata.get("version") == DAGSTER_CLOUD_VERSION


def test_agent_automatically_syncs(
    agent,
    agent_instance,
    user_code_launcher,
    cloud_storage,
):
    code_location_origin_one = _add_location(cloud_storage, location_name="location1")

    _run_initial_reconcilation(agent, user_code_launcher)

    code_location_origin_two = _add_location(cloud_storage, location_name="location2")

    list(agent.run_iteration(user_code_launcher))

    user_code_launcher.reconcile()

    # At first only one location is set
    assert user_code_launcher.get_grpc_endpoint("sandbox", code_location_origin_one.location_name)

    with pytest.raises(Exception):
        user_code_launcher.get_grpc_endpoint("sandbox", code_location_origin_two.location_name)

    # Make the next workspace check succeed by resetting the timestamp
    agent._last_workspace_check_time = None  # noqa: SLF001

    # After the next worskpace check + reconcile, both locations are set
    agent._check_update_workspace(  # noqa: SLF001
        user_code_launcher, upload_outdated=False
    )
    user_code_launcher.reconcile()

    assert user_code_launcher.get_grpc_endpoint("sandbox", code_location_origin_one.location_name)

    assert user_code_launcher.get_grpc_endpoint("sandbox", code_location_origin_two.location_name)


def test_autosync_while_checking_for_workspace_updates(
    agent,
    agent_instance,
    user_code_launcher,
    cloud_storage,
    host_instance,
):
    # Verify that if a reconciliation happens right after a CHECK_FOR_WORKSPACE_UPDATE
    # call (to write outdated data back to Dagit), the write still happens

    _run_initial_reconcilation(agent, user_code_launcher)

    code_location_origin_one = _add_location(cloud_storage, location_name="location1")

    assert not cloud_storage.get_workspace_location_entry("location1").code_location

    dagster_cloud_api_call(
        host_instance,
        DagsterCloudApi.CHECK_FOR_WORKSPACE_UPDATES,
        wait_for_response=False,
    )
    _run_to_request_completion(agent, user_code_launcher)

    # Make the next workspace check succeed by resetting the timestamp
    agent._last_workspace_check_time = None  # noqa: SLF001

    # agent also polls for an update, gets one
    agent._check_update_workspace(  # noqa: SLF001
        user_code_launcher, upload_outdated=False
    )

    # next reconcilation should still result in the upload triggered by the
    # CHECK_FOR_WORKSPACE_UPDATES call from dagit
    user_code_launcher.reconcile()

    assert user_code_launcher.get_grpc_endpoint("sandbox", code_location_origin_one.location_name)
    assert cloud_storage.get_workspace_location_entry("location1").code_location


@pytest.mark.parametrize("num_requests", [1, 10])
def test_check_for_workspace_updates(
    agent,
    user_code_launcher,
    agent_instance,
    cloud_storage,
    host_instance,
    num_requests,
):
    code_location_origin_one = _add_location(cloud_storage, location_name="location1")

    _run_initial_reconcilation(agent, user_code_launcher)

    code_location_origin_two = _add_location(cloud_storage, location_name="location2")

    gen_responses = []
    for _ in range(num_requests):
        gen_response = gen_dagster_cloud_api_call(
            host_instance,
            DagsterCloudApi.CHECK_FOR_WORKSPACE_UPDATES,
        )
        next(gen_response)

        gen_responses.append(gen_response)

    _run_to_request_completion(agent, user_code_launcher)

    user_code_launcher.reconcile()

    assert user_code_launcher.get_grpc_endpoint("sandbox", code_location_origin_one.location_name)

    # Also uploads data to cloud for both locations (one already reconciled, one not)
    first_entry = cloud_storage.get_workspace_location_entry("location1")
    assert first_entry.code_location, str(first_entry.load_error)

    assert user_code_launcher.get_grpc_endpoint("sandbox", code_location_origin_two.location_name)
    second_entry = cloud_storage.get_workspace_location_entry("location2")

    assert second_entry.code_location, str(second_entry.load_error)

    _assert_responses_for_requests(gen_responses, num_requests)


def test_no_requests_before_initial_reconciliation(
    agent, agent_instance, user_code_launcher, host_instance, cloud_storage
):
    agent._check_update_workspace(  # noqa: SLF001
        user_code_launcher, upload_outdated=True
    )

    agent._check_add_heartbeat(  # noqa: SLF001
        FAKE_AGENT_UUID, heartbeat_interval_seconds=0
    )

    assert not agent.request_ids_to_futures

    gen_response = gen_dagster_cloud_api_call(
        host_instance,
        DagsterCloudApi.CHECK_FOR_WORKSPACE_UPDATES,
    )
    next(gen_response)
    assert list(agent.run_iteration(user_code_launcher)) == []

    assert not agent.request_ids_to_futures
    _run_initial_reconcilation(agent, user_code_launcher, upload_outdated=False)
    next(agent.run_iteration(user_code_launcher))
    assert agent.request_ids_to_futures
    _run_to_request_completion(agent, user_code_launcher)


@pytest.mark.parametrize("num_requests", [1, 10])
def test_get_remote_execution_plan(
    agent,
    agent_instance,
    user_code_launcher,
    host_instance,
    code_location,
    num_requests,
):
    _run_initial_reconcilation(agent, user_code_launcher)

    remote_job = code_location.get_repository("repo").get_full_job("success_job")

    gen_responses = []
    for _ in range(num_requests):
        gen_response = gen_dagster_cloud_api_call(
            host_instance,
            DagsterCloudApi.GET_EXTERNAL_EXECUTION_PLAN,
            ExecutionPlanSnapshotArgs(
                job_origin=remote_job.get_remote_origin(),
                asset_selection=remote_job.asset_selection,
                op_selection=remote_job.op_selection or [],
                run_config={},
                mode=DEFAULT_MODE_NAME,
                step_keys_to_execute=None,
                job_snapshot_id=remote_job.identifying_job_snapshot_id,
                known_state=None,
            ),
        )
        next(gen_response)

        gen_responses.append(gen_response)

    _run_to_request_completion(agent, user_code_launcher)

    _assert_responses_for_requests(gen_responses, num_requests)


@pytest.mark.parametrize("num_requests", [1, 10])
def test_get_subset_remote_job_result(
    agent,
    agent_instance,
    user_code_launcher,
    host_instance,
    code_location,
    num_requests,
):
    _run_initial_reconcilation(agent, user_code_launcher)

    remote_job = code_location.get_repository("repo").get_full_job("success_job")

    gen_responses = []
    for _ in range(num_requests):
        gen_response = gen_dagster_cloud_api_call(
            host_instance,
            DagsterCloudApi.GET_SUBSET_EXTERNAL_PIPELINE_RESULT,
            JobSubsetSnapshotArgs(
                job_origin=remote_job.get_remote_origin(),
                op_selection=None,
                asset_selection=None,
                include_parent_snapshot=False,
            ),
        )
        next(gen_response)
        gen_responses.append(gen_response)

    _run_to_request_completion(agent, user_code_launcher)

    _assert_responses_for_requests(gen_responses, num_requests)


@pytest.mark.parametrize("num_requests", [1, 10])
def test_get_remote_partition_config(
    agent,
    agent_instance,
    user_code_launcher,
    host_instance,
    code_location,
    num_requests,
):
    _run_initial_reconcilation(agent, user_code_launcher)

    remote_repository = code_location.get_repository("repo")

    gen_responses = []
    for _ in range(num_requests):
        gen_response = gen_dagster_cloud_api_call(
            host_instance,
            DagsterCloudApi.GET_EXTERNAL_PARTITION_CONFIG,
            PartitionArgs(
                repository_origin=remote_repository.get_remote_origin(),
                job_name="success_job",
                partition_set_name="success_job_partition_set",
                partition_name="2020-01-01",
                instance_ref=agent_instance.get_ref(),
            ),
        )
        next(gen_response)

        gen_responses.append(gen_response)

    _run_to_request_completion(agent, user_code_launcher)

    _assert_responses_for_requests(gen_responses, num_requests)


@pytest.mark.parametrize("num_requests", [1, 10])
def test_get_external_partition_tags(
    agent,
    agent_instance,
    user_code_launcher,
    host_instance,
    code_location,
    num_requests,
):
    _run_initial_reconcilation(agent, user_code_launcher)

    remote_repository = code_location.get_repository("repo")

    gen_responses = []
    for _ in range(num_requests):
        gen_response = gen_dagster_cloud_api_call(
            host_instance,
            DagsterCloudApi.GET_EXTERNAL_PARTITION_TAGS,
            PartitionArgs(
                repository_origin=remote_repository.get_remote_origin(),
                job_name="success_job",
                partition_set_name="success_job_partition_set",
                partition_name="2020-01-01",
                instance_ref=agent_instance.get_ref(),
            ),
        )
        next(gen_response)

        gen_responses.append(gen_response)

    _run_to_request_completion(agent, user_code_launcher)

    _assert_responses_for_requests(gen_responses, num_requests)


@pytest.mark.parametrize("num_requests", [1, 10])
def test_get_external_partition_names(
    agent,
    agent_instance,
    user_code_launcher,
    host_instance,
    code_location,
    num_requests,
):
    _run_initial_reconcilation(agent, user_code_launcher)

    remote_repository = code_location.get_repository("repo")

    gen_responses = []
    for _ in range(num_requests):
        gen_response = gen_dagster_cloud_api_call(
            host_instance,
            DagsterCloudApi.GET_EXTERNAL_PARTITION_NAMES,
            PartitionNamesArgs(
                repository_origin=remote_repository.get_remote_origin(),
                job_name="success_job",
                partition_set_name="success_job_partition_set",
            ),
        )
        next(gen_response)

        gen_responses.append(gen_response)

    _run_to_request_completion(agent, user_code_launcher)

    _assert_responses_for_requests(gen_responses, num_requests)


@pytest.mark.parametrize("num_requests", [1, 10])
def test_get_external_partition_set_execution_param_data(
    agent,
    agent_instance,
    user_code_launcher,
    host_instance,
    code_location,
    num_requests,
):
    _run_initial_reconcilation(agent, user_code_launcher)

    remote_repository = code_location.get_repository("repo")

    gen_responses = []
    for _ in range(num_requests):
        gen_response = gen_dagster_cloud_api_call(
            host_instance,
            DagsterCloudApi.GET_EXTERNAL_PARTITION_SET_EXECUTION_PARAM_DATA,
            PartitionSetExecutionParamArgs(
                repository_origin=remote_repository.get_remote_origin(),
                partition_set_name="success_job_partition_set",
                partition_names=["2020-01-01"],
                instance_ref=agent_instance.get_ref(),
            ),
        )
        next(gen_response)

        gen_responses.append(gen_response)

    _run_to_request_completion(agent, user_code_launcher)

    _assert_responses_for_requests(gen_responses, num_requests)


@pytest.mark.parametrize("num_requests", [1, 10])
def test_get_external_schedule_execution_data(
    agent,
    agent_instance,
    user_code_launcher,
    host_instance,
    code_location,
    num_requests,
):
    _run_initial_reconcilation(agent, user_code_launcher)

    remote_repository = code_location.get_repository("repo")

    gen_responses = []
    for _ in range(num_requests):
        gen_response = gen_dagster_cloud_api_call(
            host_instance,
            DagsterCloudApi.GET_EXTERNAL_SCHEDULE_EXECUTION_DATA,
            ExternalScheduleExecutionArgs(
                repository_origin=remote_repository.get_remote_origin(),
                instance_ref=agent_instance.get_ref(),
                schedule_name="daily_success_job",
            ),
        )
        next(gen_response)

        gen_responses.append(gen_response)

    _run_to_request_completion(agent, user_code_launcher)

    _assert_responses_for_requests(gen_responses, num_requests)


@pytest.mark.parametrize("num_requests", [1, 10])
def test_get_external_sensor_execution_data(
    agent,
    agent_instance,
    user_code_launcher,
    host_instance,
    code_location,
    num_requests,
):
    _run_initial_reconcilation(agent, user_code_launcher)

    remote_repository = code_location.get_repository("repo")

    gen_responses = []
    for _ in range(num_requests):
        gen_response = gen_dagster_cloud_api_call(
            host_instance,
            DagsterCloudApi.GET_EXTERNAL_SENSOR_EXECUTION_DATA,
            SensorExecutionArgs(
                repository_origin=remote_repository.get_remote_origin(),
                instance_ref=agent_instance.get_ref(),
                sensor_name="success_job_sensor",
                last_tick_completion_time=None,
                last_run_key=None,
                cursor=None,
            ),
        )

        next(gen_response)

        gen_responses.append(gen_response)

    _run_to_request_completion(agent, user_code_launcher)

    _assert_responses_for_requests(gen_responses, num_requests)


def _wait_for_run_process(host_instance, run_id):
    # Ensure that the pid used to launch this run has termianted
    run = host_instance.get_run_by_id(run_id)
    pid = int(run.tags[PID_TAG])
    start_time = time.time()
    while True:
        if time.time() - start_time > 60:
            raise Exception("Timed out waiting for process to finish")

        try:
            os.kill(pid, 0)
        except OSError:
            # Error indicates the process has finished
            return

        time.sleep(1)


@pytest.mark.parametrize("num_requests", [1, 10])
def test_get_external_notebook_data(
    agent,
    agent_instance,
    user_code_launcher,
    host_instance,
    code_location,
    num_requests,
):
    _run_initial_reconcilation(agent, user_code_launcher)

    gen_responses = []
    for _ in range(num_requests):
        gen_response = gen_dagster_cloud_api_call(
            host_instance,
            DagsterCloudApi.GET_EXTERNAL_NOTEBOOK_DATA,
            NotebookPathArgs(
                code_location_origin=code_location.origin,
                notebook_path=file_relative_path(__file__, "foo.ipynb"),
            ),
        )
        next(gen_response)

        gen_responses.append(gen_response)

    _run_to_request_completion(agent, user_code_launcher)

    _assert_responses_for_requests(gen_responses, num_requests)


@pytest.mark.parametrize("num_requests", [1, 5])
def test_launch_run(
    agent,
    agent_instance,
    user_code_launcher,
    host_instance,
    code_location,
    num_requests,
):
    _run_initial_reconcilation(agent, user_code_launcher)

    remote_job = code_location.get_repository("repo").get_full_job("success_job")

    runs = {}

    gen_responses = []
    for _ in range(num_requests):
        run = host_instance.create_run_for_job(
            job_def=success_job,
            remote_job_origin=remote_job.get_remote_origin(),
            job_code_origin=remote_job.get_python_origin(),
        )
        runs[run.run_id] = run
        gen_response = gen_dagster_cloud_api_call(
            host_instance,
            DagsterCloudApi.LAUNCH_RUN,
            LaunchRunArgs(dagster_run=run),
        )
        next(gen_response)

        gen_responses.append(gen_response)

    _run_to_request_completion(agent, user_code_launcher)

    _assert_responses_for_requests(gen_responses, num_requests)

    for run_id in runs:
        poll_for_finished_run(host_instance, run_id)
        _wait_for_run_process(host_instance, run_id)


@pytest.mark.parametrize("num_requests", [1, 10])
def test_terminate_run(
    agent,
    agent_instance,
    user_code_launcher,
    host_instance,
    code_location,
    num_requests,
):
    _run_initial_reconcilation(agent, user_code_launcher)

    remote_job = code_location.get_repository("repo").get_full_job("sleepy_job")

    launcher = user_code_launcher.run_launcher()

    runs = {}

    for _ in range(num_requests):
        run = host_instance.create_run_for_job(
            job_def=sleepy_job,
            remote_job_origin=remote_job.get_remote_origin(),
            job_code_origin=remote_job.get_python_origin(),
        )
        runs[run.run_id] = run

        launcher.launch_run(LaunchRunContext(dagster_run=run, workspace=None))

    for run_id in runs:
        poll_for_step_start(host_instance, run_id)

    gen_responses = []
    for run_id in runs:
        run = runs[run_id]
        gen_response = gen_dagster_cloud_api_call(
            host_instance,
            DagsterCloudApi.TERMINATE_RUN,
            TerminateRunArgs(dagster_run=run),
        )
        next(gen_response)

        gen_responses.append(gen_response)

    _run_to_request_completion(agent, user_code_launcher)

    _assert_responses_for_requests(gen_responses, num_requests)

    for run_id in runs:
        poll_for_finished_run(host_instance, run_id)
        _wait_for_run_process(host_instance, run_id)


@pytest.mark.parametrize("num_requests", [1, 6])
def test_terminate_run_isolated_agents(
    isolated_agents_instance,
    isolated_agents_user_code_launcher,
    host_instance,
    code_location_isolated_agents,
    num_requests,
):
    with DagsterCloudAgent(isolated_agents_instance) as agent:
        _run_initial_reconcilation(agent, isolated_agents_user_code_launcher)

        remote_job = code_location_isolated_agents.get_repository("repo").get_full_job("sleepy_job")

        launcher = isolated_agents_user_code_launcher.run_launcher()

        runs = {}

        for _ in range(num_requests):
            run = host_instance.create_run_for_job(
                job_def=sleepy_job,
                remote_job_origin=remote_job.get_remote_origin(),
                job_code_origin=remote_job.get_python_origin(),
            )
            runs[run.run_id] = run

            launcher.launch_run(LaunchRunContext(dagster_run=run, workspace=None))

        for run_id in runs:
            poll_for_step_start(host_instance, run_id)

        gen_responses = []
        for run_id in runs:
            run = runs[run_id]
            gen_response = gen_dagster_cloud_api_call(
                host_instance,
                DagsterCloudApi.TERMINATE_RUN,
                TerminateRunArgs(dagster_run=run),
            )
            next(gen_response)

            gen_responses.append(gen_response)

        _run_to_request_completion(agent, isolated_agents_user_code_launcher)

        _assert_responses_for_requests(gen_responses, num_requests)

        for run_id in runs:
            poll_for_finished_run(host_instance, run_id)
            _wait_for_run_process(host_instance, run_id)


@pytest.mark.parametrize("exception", [concurrent.futures.TimeoutError(), Exception("Failure")])
def test_future_exception(
    agent,
    agent_instance,
    user_code_launcher,
    host_instance,
    code_location,
    monkeypatch,
    exception,
):
    _run_initial_reconcilation(agent, user_code_launcher)

    remote_job = code_location.get_repository("repo").get_full_job("success_job")

    original_submit = agent.executor.submit

    def submit(*args, **kwargs):
        future = original_submit(*args, **kwargs)
        future.set_exception(exception)

        return future

    monkeypatch.setattr(agent.executor, "submit", submit)

    dagster_cloud_api_call(
        host_instance,
        DagsterCloudApi.GET_EXTERNAL_EXECUTION_PLAN,
        ExecutionPlanSnapshotArgs(
            job_origin=remote_job.get_remote_origin(),
            asset_selection=remote_job.asset_selection,
            op_selection=remote_job.op_selection or [],
            run_config={},
            mode=DEFAULT_MODE_NAME,
            step_keys_to_execute=None,
            job_snapshot_id=remote_job.identifying_job_snapshot_id,
            known_state=None,
        ),
        wait_for_response=False,
    )

    result = next(agent.run_iteration(user_code_launcher))

    assert isinstance(result, SerializableErrorInfo)
    assert result.cls_name == exception.__class__.__name__

    # loop recovers
    result = next(agent.run_iteration(user_code_launcher))
    assert not result


def test_unknown_api(
    agent,
    agent_instance,
    user_code_launcher,
    user_cloud_agent_request_storage,
    host_instance,
):
    _run_initial_reconcilation(agent, user_code_launcher)

    agent._process_api_request(  # noqa: SLF001
        {
            "requestId": "foobar",
            "requestApi": "DO_THE_HOKEY_POKEY",
            "requestBody": "",
            "deploymentName": "sandbox",
            "isBranchDeployment": False,
        },
        user_code_launcher,
        get_current_timestamp(),
    )

    serialized_response = user_cloud_agent_request_storage.get_deployment_scoped_response(
        "foobar",
        organization_id=host_instance.cloud_deployment.organization_id,
        deployment_id=host_instance.cloud_deployment.deployment_id,
    )
    response = deserialize_value(serialized_response, DagsterCloudApiUnknownCommandResponse)
    assert response.thread_telemetry


def test_upload_api_response(
    agent,
    agent_instance,
    user_code_launcher,
    user_cloud_agent_request_storage,
    host_instance,
):
    _run_initial_reconcilation(agent, user_code_launcher)

    response_body = DagsterCloudApiSuccess()

    upload_response = DagsterCloudUploadApiResponse(
        request_id="my_request",
        request_api="my_api",
        response=response_body,
    )

    upload_api_response(agent_instance, "sandbox", upload_response)

    response = user_cloud_agent_request_storage.get_deployment_scoped_response(
        "my_request",
        organization_id=host_instance.cloud_deployment.organization_id,
        deployment_id=host_instance.cloud_deployment.deployment_id,
    )
    assert response == serialize_value(response_body)


def test_batch_upload_api_response(
    agent,
    agent_instance,
    user_code_launcher,
    user_cloud_agent_request_storage,
    host_instance,
):
    _run_initial_reconcilation(agent, user_code_launcher)

    response_body = DagsterCloudApiSuccess()

    upload_response = DagsterCloudUploadApiResponse(
        request_id="my_request",
        request_api="my_api",
        response=response_body,
    )

    batch_upload_api_response(agent_instance, "sandbox", [upload_response])

    response = user_cloud_agent_request_storage.get_deployment_scoped_response(
        "my_request",
        organization_id=host_instance.cloud_deployment.organization_id,
        deployment_id=host_instance.cloud_deployment.deployment_id,
    )
    assert response == serialize_value(response_body)


def test_upload_api_response_redis_timeout(
    agent_instance_local_ursula: DagsterCloudAgentInstance,
    host_instance: DeploymentScopedHostInstance,
):
    response_body = DagsterCloudApiSuccess()

    upload_response = DagsterCloudUploadApiResponse(
        request_id="my_request",
        request_api="my_api",
        response=response_body,
    )

    with mock.patch(
        "ursula.server.send_user_agent_response",
        side_effect=redis.exceptions.TimeoutError,
    ):
        with pytest.raises(Exception, match="503 Service Unavailable"):
            upload_api_response(agent_instance_local_ursula, "sandbox", upload_response)


def test_upload_api_response_idempotence(
    agent,
    agent_instance,
    user_code_launcher,
    user_cloud_agent_request_storage,
    host_instance,
):
    state = {}

    _run_initial_reconcilation(agent, user_code_launcher)

    response_body = DagsterCloudApiSuccess()

    upload_response = DagsterCloudUploadApiResponse(
        request_id="my_request",
        request_api="my_api",
        response=response_body,
    )

    original = HTTPConnection.getresponse

    def fake_getresponse(*args, **kwargs):
        if not state.get("threw"):
            original(*args, **kwargs)
            state["threw"] = True
            raise TimeoutError()

        state["passed"] = True
        return original(*args, **kwargs)

    with mock.patch.object(HTTPConnection, "getresponse", new=fake_getresponse):
        upload_api_response(agent_instance, "sandbox", upload_response)

    response = user_cloud_agent_request_storage.get_deployment_scoped_response(
        "my_request",
        organization_id=host_instance.cloud_deployment.organization_id,
        deployment_id=host_instance.cloud_deployment.deployment_id,
    )
    assert response == serialize_value(response_body)

    # ensure we failed and retried
    assert state["threw"] is True
    assert state["passed"] is True


def test_no_server_endpoint_unreachable(
    agent,
    agent_instance,
    user_code_launcher,
    host_instance,
):
    _run_initial_reconcilation(agent, user_code_launcher)

    invalid_repository_origin = RemoteRepositoryOrigin(
        code_location_origin=RegisteredCodeLocationOrigin(
            location_name="missing_location",
        ),
        repository_name="fake_repo",
    )

    gen_api_call = gen_dagster_cloud_api_call(
        host_instance,
        DagsterCloudApi.GET_EXTERNAL_PARTITION_TAGS,
        PartitionArgs(
            repository_origin=invalid_repository_origin,
            job_name="daily_success_job",
            partition_set_name="daily_success_job_partitions",
            partition_name="2020-01-01",
            instance_ref=agent_instance.get_ref(),
        ),
    )
    next(gen_api_call)

    next(agent.run_iteration(user_code_launcher))
    assert len(agent._pending_requests) == 1  # noqa: SLF001

    agent._query_for_workspace_updates(  # noqa: SLF001
        user_code_launcher, upload_outdated=False
    )

    _run_to_request_completion(agent, user_code_launcher)

    with pytest.raises(
        DagsterUserCodeUnreachableError,
        match="No server endpoint exists for sandbox:missing_location",
    ):
        next(gen_api_call)


def test_invalid_server_endpoint_unreachable(
    agent,
    agent_instance,
    user_code_launcher,
    host_instance,
):
    host_instance.cloud_storage.add_location(
        "bad_location",
        code_location_deploy_data=CodeLocationDeployData(
            python_file=__file__, image="images_do_not_work"
        ),
    )

    _run_initial_reconcilation(agent, user_code_launcher)

    bad_repository_origin = RemoteRepositoryOrigin(
        code_location_origin=RegisteredCodeLocationOrigin(
            location_name="bad_location",
        ),
        repository_name="fake_repo",
    )

    gen_api_call = gen_dagster_cloud_api_call(
        host_instance,
        DagsterCloudApi.GET_EXTERNAL_PARTITION_TAGS,
        PartitionArgs(
            repository_origin=bad_repository_origin,
            job_name="daily_success_job",
            partition_set_name="daily_success_job_partitions",
            partition_name="2020-01-01",
            instance_ref=agent_instance.get_ref(),
        ),
    )
    next(gen_api_call)

    _run_to_request_completion(agent, user_code_launcher)

    with pytest.raises(
        DagsterUserCodeUnreachableError,
        match=(
            "Failure loading server endpoint for sandbox:bad_location:\nException: Your agent's"
            " configuration cannot load locations that specify a Docker image"
        ),
    ):
        next(gen_api_call)


def test_timeout_unreachable(
    agent,
    agent_instance,
    user_code_launcher,
    host_instance,
):
    _run_initial_reconcilation(agent, user_code_launcher)

    with pytest.raises(
        DagsterUserCodeUnreachableError,
        match="Timed out waiting for",
    ):
        dagster_cloud_api_call(
            host_instance,
            DagsterCloudApi.CHECK_FOR_WORKSPACE_UPDATES,
            timeout=1,
        )


@pytest.fixture(scope="module")
def organization(host_unscoped_instance):
    return host_unscoped_instance.cloud_storage.get_organization_by_non_unique_name("acme")


@pytest.fixture
def branch1_instance(host_unscoped_instance: UnscopedHostInstance, organization):
    name = uuid.uuid4().hex
    with host_unscoped_instance.for_organization(organization) as org_instance:
        branch = host_unscoped_instance.cloud_storage.getx_deployment_by_id(
            organization.organization_id,
            org_instance.cloud_storage.create_deployment(
                name,
                is_branch_deployment=True,
                deployment_metadata=DagsterCloudDeploymentMetadata(
                    branch_deployment_metadata=BranchDeploymentGitMetadata("foo", name)
                ),
            ),
        )
        with host_unscoped_instance.for_deployment(organization, branch) as branch_instance:
            _add_location(branch_instance.cloud_storage, "location1")
            yield branch_instance


@pytest.fixture
def branch2_instance(host_unscoped_instance: UnscopedHostInstance, organization):
    name = uuid.uuid4().hex
    with host_unscoped_instance.for_organization(organization) as org_instance:
        branch = host_unscoped_instance.cloud_storage.getx_deployment_by_id(
            organization.organization_id,
            org_instance.cloud_storage.create_deployment(
                name,
                is_branch_deployment=True,
                deployment_metadata=DagsterCloudDeploymentMetadata(
                    branch_deployment_metadata=BranchDeploymentGitMetadata("foo", name)
                ),
            ),
        )
        with host_unscoped_instance.for_deployment(organization, branch) as branch_instance:
            _add_location(branch_instance.cloud_storage, "location1")
            _add_location(branch_instance.cloud_storage, "location2")
            yield branch_instance


def test_branch_deployments_agent(
    branch1_instance,
    branch2_instance,
    branch_deployments_agent_instance,
    branch_deployments_user_code_launcher,
):
    with (
        DagsterCloudAgent(branch_deployments_agent_instance) as agent,
        freezegun.freeze_time(tick=True) as frozen_time,
    ):
        agent_instance = branch_deployments_agent_instance
        user_code_launcher = branch_deployments_user_code_launcher

        branch1_instance.cloud_storage.wipe_agent_heartbeats()
        branch2_instance.cloud_storage.wipe_agent_heartbeats()

        with pytest.raises(Exception):
            user_code_launcher.get_grpc_endpoint(branch1_instance.deployment_name, "location1")

        # Agent heartbeats for each location with active grpc servers (neither)
        _run_initial_reconcilation(agent, user_code_launcher)
        assert not branch1_instance.has_healthy_agent()
        assert not branch2_instance.has_healthy_agent()

        location1_origin = RegisteredCodeLocationOrigin("location1")
        location2_origin = RegisteredCodeLocationOrigin("location2")

        # Two locations make requests
        gen_responses = []
        first_response = _execution_plan_api_call(
            branch1_instance,
            location1_origin,
        )
        gen_responses.append(first_response)
        next(first_response)

        second_response = _execution_plan_api_call(
            branch2_instance,
            location2_origin,
        )
        gen_responses.append(second_response)
        next(second_response)

        # Agent picks up both requests from the queue
        next(agent.run_iteration(user_code_launcher))
        assert len(agent._pending_requests) == 2  # noqa: SLF001

        agent._query_for_workspace_updates(  # noqa: SLF001
            user_code_launcher, upload_outdated=False
        )

        agent._check_add_heartbeat(  # noqa: SLF001
            FAKE_AGENT_UUID, heartbeat_interval_seconds=0
        )
        assert (
            _code_server_heartbeat_for_location(branch1_instance, "location1").server_status  # ty: ignore[unresolved-attribute]
            == CloudCodeServerStatus.STARTING
        )
        assert (
            _code_server_heartbeat_for_location(branch2_instance, "location2").server_status  # ty: ignore[unresolved-attribute]
            == CloudCodeServerStatus.STARTING
        )

        user_code_launcher.reconcile()

        frozen_time.tick()  # tick to reset tick=True progression for accurate timedelta
        frozen_time.tick(datetime.timedelta(seconds=RECENT_AGENT_DETAILS_STALE_SECONDS + 1))

        # Agent heartbeats for each location with active grpc servers (neither...because TTL)
        agent._check_add_heartbeat(  # noqa: SLF001
            FAKE_AGENT_UUID, heartbeat_interval_seconds=0
        )
        assert _wait_for_healthy_agent(branch1_instance)
        assert _wait_for_healthy_agent(branch2_instance)

        assert (
            _code_server_heartbeat_for_location(branch1_instance, "location1").server_status  # ty: ignore[unresolved-attribute]
            == CloudCodeServerStatus.RUNNING
        )
        assert (
            _code_server_heartbeat_for_location(branch2_instance, "location2").server_status  # ty: ignore[unresolved-attribute]
            == CloudCodeServerStatus.RUNNING
        )

        # Garbage collect heartbeats
        branch1_instance.cloud_storage.wipe_agent_heartbeats()
        branch2_instance.cloud_storage.wipe_agent_heartbeats()

        user_code_launcher.get_grpc_endpoint(branch1_instance.deployment_name, "location1")
        user_code_launcher.get_grpc_endpoint(branch2_instance.deployment_name, "location2")

        # Agent serves requests from two different branch deployments!

        _run_to_request_completion(agent, user_code_launcher)
        _assert_responses_for_requests(gen_responses, 2)

        # Branch 2 sends a request to upload metadata

        dagster_cloud_api_call(
            branch2_instance,
            DagsterCloudApi.CHECK_FOR_WORKSPACE_UPDATES,
            wait_for_response=False,
        )

        _run_to_request_completion(agent, user_code_launcher)
        user_code_launcher.reconcile()

        # Now all three locations are available, and the branch has filled out its metadata

        user_code_launcher.get_grpc_endpoint(branch1_instance.deployment_name, "location1")
        user_code_launcher.get_grpc_endpoint(branch2_instance.deployment_name, "location1")
        user_code_launcher.get_grpc_endpoint(branch2_instance.deployment_name, "location2")

        assert branch2_instance.cloud_storage.get_workspace_location_entry(
            "location1"
        ).code_location
        assert branch2_instance.cloud_storage.get_workspace_location_entry(
            "location2"
        ).code_location

        # but only triggered branch2 not branch1
        assert not branch1_instance.cloud_storage.get_workspace_location_entry(
            "location1"
        ).code_location

        # After TTL passes, they all fall out
        frozen_time.tick()  # tick to reset tick=True progression for accurate timedelta
        frozen_time.tick(
            datetime.timedelta(
                seconds=1.5 * agent_instance.user_code_launcher.branch_deployment_ttl_seconds
            )
        )

        agent._query_for_workspace_updates(  # noqa: SLF001
            user_code_launcher, upload_outdated=False
        )

        user_code_launcher.reconcile()

        with pytest.raises(Exception):
            user_code_launcher.get_grpc_endpoint(branch1_instance.deployment_name, "location1")

        with pytest.raises(Exception):
            user_code_launcher.get_grpc_endpoint(branch2_instance.deployment_name, "location1")

        with pytest.raises(Exception):
            user_code_launcher.get_grpc_endpoint(branch2_instance.deployment_name, "location2")

        # Agent heartbeats for each location with active grpc servers (neither...because TTL)
        agent._check_add_heartbeat(  # noqa: SLF001
            FAKE_AGENT_UUID, heartbeat_interval_seconds=0
        )
        assert not branch1_instance.has_healthy_agent()
        assert not branch2_instance.has_healthy_agent()


@pytest.fixture
def prod_host_instance(host_unscoped_instance):
    with host_unscoped_instance.load_for_deployment_by_non_unique_name(
        "acme", "prod"
    ) as scoped_instance:
        yield scoped_instance


@pytest.fixture
def serverless_host_instance(host_unscoped_instance):
    with host_unscoped_instance.load_for_deployment_by_non_unique_name(
        "acme", "serverless"
    ) as scoped_instance:
        yield scoped_instance


def test_branch_deployments_and_serverless_agent(
    branch1_instance,
    branch2_instance,
    serverless_instance,
    prod_host_instance,
    serverless_host_instance,
):
    branch1_instance.cloud_storage.wipe_agent_heartbeats()
    branch2_instance.cloud_storage.wipe_agent_heartbeats()
    serverless_host_instance.cloud_storage.wipe_agent_heartbeats()
    prod_host_instance.cloud_storage.wipe_agent_heartbeats()
    with (
        freezegun.freeze_time(tick=True) as frozen_time,
        DagsterCloudAgent(serverless_instance) as agent,
    ):
        agent_instance = serverless_instance
        user_code_launcher = serverless_instance.user_code_launcher
        user_code_launcher.start(run_reconcile_thread=False, run_metrics_thread=False)

        serverless_origin = _add_location(serverless_host_instance.cloud_storage)
        prod_origin = _add_location(prod_host_instance.cloud_storage)

        with pytest.raises(Exception):
            user_code_launcher.get_grpc_endpoint(branch1_instance.deployment_name, "location1")

        with pytest.raises(Exception):
            user_code_launcher.get_grpc_endpoint("serverless", serverless_origin.location_name)

        # Non-serverless deployments not loaded
        with pytest.raises(Exception):
            user_code_launcher.get_grpc_endpoint("prod", prod_origin.location_name)

        # Agent heartbeats for each location with active grpc servers (only the non-branch deployment)
        _run_initial_reconcilation(agent, user_code_launcher)
        assert not branch1_instance.has_healthy_agent()
        assert not branch2_instance.has_healthy_agent()
        assert serverless_host_instance.has_healthy_agent()
        assert not prod_host_instance.has_healthy_agent()  # prod instance not loaded

        location1_origin = RegisteredCodeLocationOrigin("location1")
        location2_origin = RegisteredCodeLocationOrigin("location2")

        # Two locations make requests
        gen_responses = []
        first_response = _execution_plan_api_call(
            branch1_instance,
            location1_origin,
        )
        gen_responses.append(first_response)
        next(first_response)

        second_response = _execution_plan_api_call(
            branch2_instance,
            location2_origin,
        )
        gen_responses.append(second_response)
        next(second_response)

        # Agent picks up both requests from the queue
        next(agent.run_iteration(user_code_launcher))
        assert len(agent._pending_requests) == 2  # noqa: SLF001

        agent._query_for_workspace_updates(  # noqa: SLF001
            user_code_launcher, upload_outdated=False
        )

        user_code_launcher.reconcile()

        frozen_time.tick()  # tick to reset tick=True progression for accurate timedelta
        frozen_time.tick(datetime.timedelta(seconds=30))

        # Agent heartbeats for each location with active grpc servers (both)
        agent._check_add_heartbeat(  # noqa: SLF001
            FAKE_AGENT_UUID, heartbeat_interval_seconds=0
        )
        assert branch1_instance.has_healthy_agent()
        assert branch2_instance.has_healthy_agent()
        assert serverless_host_instance.has_healthy_agent()
        assert not prod_host_instance.has_healthy_agent()

        # Garbage collect heartbeats
        branch1_instance.cloud_storage.wipe_agent_heartbeats()
        branch2_instance.cloud_storage.wipe_agent_heartbeats()
        serverless_host_instance.cloud_storage.wipe_agent_heartbeats()

        user_code_launcher.get_grpc_endpoint(branch1_instance.deployment_name, "location1")
        user_code_launcher.get_grpc_endpoint(branch2_instance.deployment_name, "location2")
        user_code_launcher.get_grpc_endpoint("serverless", serverless_origin.location_name)
        with pytest.raises(Exception):
            user_code_launcher.get_grpc_endpoint("prod", prod_origin.location_name)

        # Agent serves requests from two different branch deployments!

        _run_to_request_completion(agent, user_code_launcher)
        _assert_responses_for_requests(gen_responses, 2)

        # Branch 2 sends a request to upload metadata

        dagster_cloud_api_call(
            branch2_instance,
            DagsterCloudApi.CHECK_FOR_WORKSPACE_UPDATES,
            wait_for_response=False,
        )

        _run_to_request_completion(agent, user_code_launcher)
        user_code_launcher.reconcile()

        # Now all four locations are available, and the branch has filled out its metadata

        user_code_launcher.get_grpc_endpoint(branch1_instance.deployment_name, "location1")
        user_code_launcher.get_grpc_endpoint(branch2_instance.deployment_name, "location1")
        user_code_launcher.get_grpc_endpoint(branch2_instance.deployment_name, "location2")
        user_code_launcher.get_grpc_endpoint("serverless", serverless_origin.location_name)
        with pytest.raises(Exception):
            user_code_launcher.get_grpc_endpoint("prod", prod_origin.location_name)

        assert branch2_instance.cloud_storage.get_workspace_location_entry(
            "location1"
        ).code_location
        assert branch2_instance.cloud_storage.get_workspace_location_entry(
            "location2"
        ).code_location

        # but only triggered branch2 not branch1
        assert not branch1_instance.cloud_storage.get_workspace_location_entry(
            "location1"
        ).code_location

        # After TTL passes, they all fall out except for the sandbox one
        frozen_time.tick()  # tick to reset tick=True progression for accurate timedelta
        frozen_time.tick(
            datetime.timedelta(
                seconds=1.5 * agent_instance.user_code_launcher.branch_deployment_ttl_seconds
            )
        )

        agent._query_for_workspace_updates(  # noqa: SLF001
            user_code_launcher, upload_outdated=False
        )

        user_code_launcher.reconcile()

        with pytest.raises(Exception):
            user_code_launcher.get_grpc_endpoint(branch1_instance.deployment_name, "location1")

        with pytest.raises(Exception):
            user_code_launcher.get_grpc_endpoint(branch2_instance.deployment_name, "location1")

        with pytest.raises(Exception):
            user_code_launcher.get_grpc_endpoint(branch2_instance.deployment_name, "location2")

        user_code_launcher.get_grpc_endpoint("serverless", serverless_origin.location_name)
        with pytest.raises(Exception):
            user_code_launcher.get_grpc_endpoint("prod", prod_origin.location_name)

        # Agent heartbeats for each location with active grpc servers (no branch deployments...because TTL)
        agent._check_add_heartbeat(  # noqa: SLF001
            FAKE_AGENT_UUID, heartbeat_interval_seconds=0
        )
        assert not branch1_instance.has_healthy_agent()
        assert not branch2_instance.has_healthy_agent()
        assert serverless_host_instance.has_healthy_agent()
        assert not prod_host_instance.has_healthy_agent()


def test_branch_deployments_and_prod_deployments_agent(
    branch1_instance,
    branch2_instance,
    branch_deployments_and_prod_deployments_instance,
    host_instance,
    prod_host_instance,
    cloud_storage,  # wipe storage
):
    branch1_instance.cloud_storage.wipe_agent_heartbeats()
    branch2_instance.cloud_storage.wipe_agent_heartbeats()
    host_instance.cloud_storage.wipe_agent_heartbeats()
    prod_host_instance.cloud_storage.wipe_agent_heartbeats()

    cloud_storage = host_instance.cloud_storage

    with (
        freezegun.freeze_time(tick=True) as frozen_time,
        DagsterCloudAgent(branch_deployments_and_prod_deployments_instance) as agent,
    ):
        agent_instance = branch_deployments_and_prod_deployments_instance
        user_code_launcher = branch_deployments_and_prod_deployments_instance.user_code_launcher
        user_code_launcher.start(run_reconcile_thread=False, run_metrics_thread=False)

        sandbox_origin = _add_location(cloud_storage)
        prod_origin = _add_location(prod_host_instance.cloud_storage)

        sandbox_instance = host_instance
        prod_instance = prod_host_instance

        with pytest.raises(Exception):
            user_code_launcher.get_grpc_endpoint(branch1_instance.deployment_name, "location1")

        with pytest.raises(Exception):
            user_code_launcher.get_grpc_endpoint("sandbox", sandbox_origin.location_name)

        with pytest.raises(Exception):
            user_code_launcher.get_grpc_endpoint("prod", prod_origin.location_name)

        # Agent heartbeats for each location with active grpc servers (only the non-branch deployment)
        _run_initial_reconcilation(agent, user_code_launcher)
        assert not branch1_instance.has_healthy_agent()
        assert not branch2_instance.has_healthy_agent()
        assert sandbox_instance.has_healthy_agent()
        assert prod_instance.has_healthy_agent()

        location1_origin = RegisteredCodeLocationOrigin("location1")
        location2_origin = RegisteredCodeLocationOrigin("location2")

        # Two locations make requests
        gen_responses = []
        first_response = _execution_plan_api_call(
            branch1_instance,
            location1_origin,
        )
        gen_responses.append(first_response)
        next(first_response)

        second_response = _execution_plan_api_call(
            branch2_instance,
            location2_origin,
        )
        gen_responses.append(second_response)
        next(second_response)

        # Agent picks up both requests from the queue
        next(agent.run_iteration(user_code_launcher))
        assert len(agent._pending_requests) == 2  # noqa: SLF001

        agent._query_for_workspace_updates(  # noqa: SLF001
            user_code_launcher, upload_outdated=False
        )

        user_code_launcher.reconcile()

        # Agent heartbeats for each location with active grpc servers (both)
        agent._check_add_heartbeat(  # noqa: SLF001
            FAKE_AGENT_UUID, heartbeat_interval_seconds=0
        )

        # Wait long enough that enough time has passed between heartbeats that
        # has_healthy_agent will refetch
        frozen_time.tick()  # tick to reset tick=True progression for accurate timedelta
        frozen_time.tick(datetime.timedelta(seconds=30))

        assert branch1_instance.has_healthy_agent()
        assert branch2_instance.has_healthy_agent()
        assert sandbox_instance.has_healthy_agent()
        assert prod_instance.has_healthy_agent()

        # Garbage collect heartbeats
        branch1_instance.cloud_storage.wipe_agent_heartbeats()
        branch2_instance.cloud_storage.wipe_agent_heartbeats()
        sandbox_instance.cloud_storage.wipe_agent_heartbeats()
        prod_instance.cloud_storage.wipe_agent_heartbeats()

        user_code_launcher.get_grpc_endpoint(branch1_instance.deployment_name, "location1")
        user_code_launcher.get_grpc_endpoint(branch2_instance.deployment_name, "location2")
        user_code_launcher.get_grpc_endpoint("sandbox", sandbox_origin.location_name)
        user_code_launcher.get_grpc_endpoint("prod", prod_origin.location_name)

        # Agent serves requests from two different branch deployments!

        _run_to_request_completion(agent, user_code_launcher)
        _assert_responses_for_requests(gen_responses, 2)

        # Branch 2 sends a request to upload metadata

        dagster_cloud_api_call(
            branch2_instance,
            DagsterCloudApi.CHECK_FOR_WORKSPACE_UPDATES,
            wait_for_response=False,
        )

        _run_to_request_completion(agent, user_code_launcher)
        user_code_launcher.reconcile()

        # Now all four locations are available, and the branch has filled out its metadata

        user_code_launcher.get_grpc_endpoint(branch1_instance.deployment_name, "location1")
        user_code_launcher.get_grpc_endpoint(branch2_instance.deployment_name, "location1")
        user_code_launcher.get_grpc_endpoint(branch2_instance.deployment_name, "location2")
        user_code_launcher.get_grpc_endpoint("sandbox", sandbox_origin.location_name)
        user_code_launcher.get_grpc_endpoint("prod", prod_origin.location_name)

        assert branch2_instance.cloud_storage.get_workspace_location_entry(
            "location1"
        ).code_location
        assert branch2_instance.cloud_storage.get_workspace_location_entry(
            "location2"
        ).code_location

        # but only triggered branch2 not branch1
        assert not branch1_instance.cloud_storage.get_workspace_location_entry(
            "location1"
        ).code_location

        # After TTL passes, they all fall out except for the sandbox one
        frozen_time.tick()  # tick to reset tick=True progression for accurate timedelta
        frozen_time.tick(
            datetime.timedelta(
                seconds=1.5 * agent_instance.user_code_launcher.branch_deployment_ttl_seconds
            )
        )

        agent._query_for_workspace_updates(  # noqa: SLF001
            user_code_launcher, upload_outdated=False
        )

        user_code_launcher.reconcile()

        with pytest.raises(Exception):
            user_code_launcher.get_grpc_endpoint(branch1_instance.deployment_name, "location1")

        with pytest.raises(Exception):
            user_code_launcher.get_grpc_endpoint(branch2_instance.deployment_name, "location1")

        with pytest.raises(Exception):
            user_code_launcher.get_grpc_endpoint(branch2_instance.deployment_name, "location2")

        user_code_launcher.get_grpc_endpoint("sandbox", sandbox_origin.location_name)
        user_code_launcher.get_grpc_endpoint("prod", prod_origin.location_name)

        # Agent heartbeats for each location with active grpc servers (no branch deployments...because TTL)
        agent._check_add_heartbeat(  # noqa: SLF001
            FAKE_AGENT_UUID, heartbeat_interval_seconds=0
        )
        assert not branch1_instance.has_healthy_agent()
        assert not branch2_instance.has_healthy_agent()
        assert sandbox_instance.has_healthy_agent()
        assert prod_instance.has_healthy_agent()


def test_upload_job_snapshot_error(
    user_code_launcher,
    code_location,
    agent,
    agent_instance,
):
    _run_initial_reconcilation(agent, user_code_launcher)

    # test error propagates
    with pytest.raises(Exception, match="Error fetching job data in code server"):
        user_code_launcher.upload_job_snapshot(
            "sandbox",
            JobSelector(
                location_name=code_location.origin.location_name,
                repository_name="repo",
                job_name="bad_job_name",
            ),
            server=user_code_launcher.get_grpc_server(
                "sandbox",
                code_location.name,
            ),
        )

    with pytest.raises(Exception, match="Error fetching job data in code server"):
        user_code_launcher.upload_job_snap_direct(
            "sandbox",
            JobSelector(
                location_name=code_location.origin.location_name,
                repository_name="repo",
                job_name="bad_job_name",
            ),
            server=user_code_launcher.get_grpc_server(
                "sandbox",
                code_location.name,
            ),
        )


def test_workspace_upload_missing_location_raises_404(host_instance, agent_instance, cloud_storage):
    invalid_entry = DagsterCloudUploadWorkspaceEntry(
        location_name="missing_location",
        code_location_deploy_data=CodeLocationDeployData(
            python_file=__file__, image="images_do_not_work"
        ),
        upload_location_data=None,
        serialized_error_info=SerializableErrorInfo(message="hi", stack=[], cls_name="Exception"),
    )

    with pytest.raises(DagsterCloudHTTPError, match="404"):
        agent_instance.user_code_launcher._update_workspace_entry(  # noqa
            "sandbox",
            invalid_entry,
            server_or_error=SerializableErrorInfo(message="hi", stack=[], cls_name="Exception"),
        )


@pytest.mark.parametrize(
    "direct_upload",
    [False, True],
    ids=["server", "blob_store_direct"],
)
def test_workspace_upload_idempotence(
    host_instance,
    agent,
    agent_instance,
    legacy_snapshot_upload_agent_instance,
    cloud_storage,
    direct_upload,
):
    if direct_upload:
        urls = [
            "/code_location_update_result",
            "/check_snapshot",
            "/confirm_upload",
        ]
    else:
        agent_instance = legacy_snapshot_upload_agent_instance
        urls = [
            "/upload_workspace_entry",
            "/upload_job_snapshot",
        ]
    # clear snapshots to ensure we have to upload
    host_instance.blob_object_store.wipe_for_test()
    user_code_launcher = agent_instance.user_code_launcher
    _run_initial_reconcilation(agent, user_code_launcher)
    dagster_cloud_api_call(
        host_instance,
        DagsterCloudApi.CHECK_FOR_WORKSPACE_UPDATES,
        wait_for_response=False,
    )
    _add_location(cloud_storage)

    # to simulate network failures, we mock out network request & response
    # to fail the target requests on the first attempt then pass on the second

    state = {url: {"failed": 0} for url in urls}
    original_request = HTTPConnection.request

    def fake_request(*args, **kwargs):
        conn = args[0]
        url = args[2].split("?")[0]
        if url in state:
            request_state = state[url]
            # unless we already failed for this request, set the connection to fail in getresponse
            if "let_next_pass" not in request_state:
                request_state["conn_to_fail"] = conn
            else:
                del request_state["let_next_pass"]

        return original_request(*args, **kwargs)

    original_getresponse = HTTPConnection.getresponse

    def fake_getresponse(*args, **kwargs):
        conn = args[0]
        for request_state in state.values():
            if "conn_to_fail" in request_state and request_state["conn_to_fail"] == conn:
                # fake a read timeout by raising after resolving the request
                original_getresponse(*args, **kwargs)
                if request_state.get("conn_to_fail"):
                    del request_state["conn_to_fail"]
                    request_state["let_next_pass"] = True
                    request_state["failed"] += 1
                    raise TimeoutError()

        return original_getresponse(*args, **kwargs)

    with (
        mock.patch.object(HTTPConnection, "getresponse", new=fake_getresponse),
        mock.patch.object(HTTPConnection, "request", new=fake_request),
    ):
        _run_to_request_completion(agent, user_code_launcher)
        user_code_launcher.reconcile()

    location_entries = host_instance.cloud_storage.all_workspace_location_entries()
    assert location_entries.get("location")
    assert location_entries["location"].code_location
    ex_job = (
        location_entries["location"]
        .code_location.get_repository("repo")
        .get_full_job("success_job")
    )
    assert ex_job.identifying_job_snapshot_id == success_job.get_job_snapshot_id()
    assert ex_job.job_snapshot

    for url in urls:
        assert state[url]["failed"] >= 1, url


def test_agent_queues(
    agent,
    agent_instance,
    user_code_launcher,
    agent_queues_agent,
    agent_queues_agent_instance,
    agent_queues_user_code_launcher,
    host_instance,
    cloud_storage,
):
    assert agent_instance.deployment_name == agent_queues_agent_instance.deployment_name
    deployment = agent_instance.deployment_name

    assert agent_instance.agent_queues_config.queues == AgentQueuesConfig.default_queues()
    assert agent_queues_agent_instance.agent_queues_config
    queue = agent_queues_agent_instance.agent_queues_config.queues[0]

    _run_initial_reconcilation(agent, agent_queues_user_code_launcher, agent_id=str(uuid.uuid4()))
    _run_initial_reconcilation(agent_queues_agent, user_code_launcher, agent_id=str(uuid.uuid4()))

    default_location_origin = _add_location(cloud_storage, "default")
    routed_location_origin = _add_location(cloud_storage, "routed", agent_queue=queue)

    assert not user_code_launcher.get_grpc_endpoints()
    assert not agent_queues_user_code_launcher.get_grpc_endpoints()

    dagster_cloud_api_call(
        host_instance,
        DagsterCloudApi.CHECK_FOR_WORKSPACE_UPDATES,
        wait_for_response=False,
        agent_queues=host_instance.get_all_agent_queues(),
    )
    _run_to_request_completion(agent, user_code_launcher)
    _run_to_request_completion(agent_queues_agent, agent_queues_user_code_launcher)

    user_code_launcher.reconcile()
    agent_queues_user_code_launcher.reconcile()

    assert len(user_code_launcher.get_grpc_endpoints()) == 1
    default_endpoint = user_code_launcher.get_grpc_endpoint(
        deployment,
        default_location_origin.location_name,
    )
    assert default_endpoint

    assert len(agent_queues_user_code_launcher.get_grpc_endpoints()) == 1
    routed_endpoint = agent_queues_user_code_launcher.get_grpc_endpoint(
        deployment,
        routed_location_origin.location_name,
    )
    assert routed_endpoint

    with (
        GrpcServerCodeLocation(
            instance=agent_instance,
            origin=default_location_origin,
            port=default_endpoint.port,
            socket=default_endpoint.socket,
            host=default_endpoint.host,
            heartbeat=True,
            watch_server=False,
        ) as default_location,
        GrpcServerCodeLocation(
            instance=agent_queues_agent_instance,
            origin=routed_location_origin,
            port=routed_endpoint.port,
            socket=routed_endpoint.socket,
            host=routed_endpoint.host,
            heartbeat=True,
            watch_server=False,
        ) as routed_location,
    ):
        default_external_job = default_location.get_repository("repo").get_full_job("success_job")
        default_run = host_instance.create_run_for_job(
            job_def=success_job,
            remote_job_origin=default_external_job.get_remote_origin(),
            job_code_origin=default_external_job.get_python_origin(),
        )

        routed_external_job = routed_location.get_repository("repo").get_full_job("success_job")
        routed_run = host_instance.create_run_for_job(
            job_def=success_job,
            remote_job_origin=routed_external_job.get_remote_origin(),
            job_code_origin=routed_external_job.get_python_origin(),
        )

        dagster_cloud_api_call(
            host_instance,
            DagsterCloudApi.LAUNCH_RUN,
            LaunchRunArgs(dagster_run=default_run),
            wait_for_response=False,
        )

        dagster_cloud_api_call(
            host_instance,
            DagsterCloudApi.LAUNCH_RUN,
            LaunchRunArgs(dagster_run=routed_run),
            wait_for_response=False,
            agent_queues=[queue],
        )

    _run_to_request_completion(agent, user_code_launcher)
    _run_to_request_completion(agent_queues_agent, agent_queues_user_code_launcher)

    _wait_for_run_process(host_instance, default_run.run_id)
    _wait_for_run_process(host_instance, routed_run.run_id)

    assert (
        host_instance.get_run_by_id(default_run.run_id).tags.get("dagster/agent_id")
        == agent_instance.instance_uuid
    )
    assert (
        host_instance.get_run_by_id(routed_run.run_id).tags.get("dagster/agent_id")
        == agent_queues_agent_instance.instance_uuid
    )


@pytest.mark.parametrize(
    ["agent_type", "action_message"],
    [
        (
            DeploymentAgentType.HYBRID,
            "Check your agent and restart it if it is no longer running.",
        ),
        (
            DeploymentAgentType.SERVERLESS,
            "Contact Support for further assistance. You can create a support ticket from inside the Help menu.",
        ),
    ],
    ids=["hybrid", "serverless"],
)
def test_agent_not_running_unreachable(mocker, host_instance, agent_type, action_message):
    with freezegun.freeze_time(tick=True) as frozen_time:
        frozen_time.tick(datetime.timedelta(days=1))  # tick past any heartbeats from other tests

        mocker.patch(
            "dagster_cloud_backend.storage.host_cloud.cloud_storage.deployment.DagsterCloudDeployment.compute_agent_type",
            return_value=agent_type,
        )

        with pytest.raises(
            DagsterUserCodeUnreachableError,
            match=(
                "Could not send a request to your Dagster Cloud agent since no agents have recently"
                f" heartbeated. {action_message}"
            ),
        ):
            dagster_cloud_api_call(host_instance, DagsterCloudApi.CHECK_FOR_WORKSPACE_UPDATES)


def test_override_agent_not_running_unreachable(host_instance):
    with freezegun.freeze_time(tick=True) as frozen_time:
        frozen_time.tick(datetime.timedelta(days=1))  # tick past any heartbeats from other tests

        dagster_cloud_api_call(
            host_instance,
            DagsterCloudApi.CHECK_FOR_WORKSPACE_UPDATES,
            wait_for_response=False,
            send_if_agent_unreachable=True,
        )


@pytest.mark.parametrize(
    ["last_touch", "touch_error", "touch_called", "touch_exception"],
    [
        (None, None, True, None),  # First write
        (300, None, True, None),  # Overdue write
        (1, None, False, None),  # Not overdue
        (None, Exception(), True, "Failed to write liveness"),
    ],
)
def test_agent_liveness_sentinel(
    last_touch: float | None,
    touch_error,
    touch_called,
    touch_exception,
    agent,
    caplog,
):
    # arrange
    if last_touch:
        agent._last_liveness_check_time = time.time() - last_touch  # noqa: SLF001

    with mock.patch.object(os, "access") as mock_os_access:
        mock_os_access.return_value = True
        with mock.patch.object(Path, "touch") as mock_touch:
            mock_touch.side_effect = touch_error

            # act
            agent._write_liveness_sentinel_if_overdue("/opt")  # noqa: SLF001

            # assert
            if touch_called:
                mock_touch.assert_called_once()
                assert agent._last_liveness_check_time is not None  # noqa: SLF001

            if touch_exception:
                assert touch_exception in caplog.text
                assert agent._last_liveness_check_time is False  # noqa: SLF001


def test_agent_liveness_sentinel_warning_on_permission_error(
    agent,
    caplog,
):
    agent._last_liveness_check_time = None  # noqa: SLF001
    with mock.patch.object(os, "access") as mock_os_access:
        mock_os_access.return_value = False

        agent._write_liveness_sentinel_if_overdue("/opt")  # noqa: SLF001

        assert "Disabling liveness sentinel" in caplog.text
        assert "is not writable" in caplog.text
        assert agent._last_liveness_check_time is False  # noqa: SLF001


def test_agent_liveness_sentinel_skipped_when_no_sentinel_dir(
    agent,
):
    """When sentinel_dir is None (base class default), liveness sentinel is a no-op."""
    agent._last_liveness_check_time = None  # noqa: SLF001

    agent._write_liveness_sentinel_if_overdue(None)  # noqa: SLF001

    # Still None (not touched), not False (not disabled)
    assert agent._last_liveness_check_time is None  # noqa: SLF001


def test_sentinel_dir_defaults():
    """Base class defaults to None, ECS to /opt, K8s to /tmp."""
    assert (
        DagsterCloudUserCodeLauncher._default_sentinel_dir.fget(  # pyright: ignore[reportOptionalCall]  # noqa: SLF001
            mock.MagicMock(spec=DagsterCloudUserCodeLauncher)
        )
        is None
    )
    assert (
        EcsUserCodeLauncher._default_sentinel_dir.fget(  # pyright: ignore[reportOptionalCall]  # noqa: SLF001
            mock.MagicMock(spec=EcsUserCodeLauncher)
        )
        == "/opt"
    )
    assert (
        K8sUserCodeLauncher._default_sentinel_dir.fget(  # pyright: ignore[reportOptionalCall]  # noqa: SLF001
            mock.MagicMock(spec=K8sUserCodeLauncher)
        )
        == "/tmp"
    )


def test_sentinel_dir_uses_default_when_env_var_unset():
    """Without env var, sentinel_dir returns _default_sentinel_dir."""
    env_var = DagsterCloudUserCodeLauncher.SENTINEL_BASE_DIR_ENV_VAR
    with mock.patch.dict(os.environ, {}, clear=False):
        os.environ.pop(env_var, None)

        launcher = mock.MagicMock(spec=DagsterCloudUserCodeLauncher)
        launcher.SENTINEL_BASE_DIR_ENV_VAR = env_var
        launcher._default_sentinel_dir = "/opt"  # noqa: SLF001
        result = DagsterCloudUserCodeLauncher.sentinel_dir.fget(launcher)  # pyright: ignore[reportOptionalCall]
        assert result == "/opt"

        launcher._default_sentinel_dir = None  # noqa: SLF001
        result = DagsterCloudUserCodeLauncher.sentinel_dir.fget(launcher)  # pyright: ignore[reportOptionalCall]
        assert result is None


def test_sentinel_dir_env_var_override():
    """Env var overrides the default for any launcher."""
    env_var = DagsterCloudUserCodeLauncher.SENTINEL_BASE_DIR_ENV_VAR
    with mock.patch.dict(os.environ, {env_var: "/custom"}):
        launcher = mock.MagicMock(spec=DagsterCloudUserCodeLauncher)
        launcher.SENTINEL_BASE_DIR_ENV_VAR = env_var
        launcher._default_sentinel_dir = "/opt"  # noqa: SLF001
        result = DagsterCloudUserCodeLauncher.sentinel_dir.fget(launcher)  # pyright: ignore[reportOptionalCall]
        assert result == "/custom"


def test_sentinel_dir_empty_string_disables():
    """Setting the env var to empty string disables sentinels."""
    env_var = DagsterCloudUserCodeLauncher.SENTINEL_BASE_DIR_ENV_VAR
    with mock.patch.dict(os.environ, {env_var: ""}):
        launcher = mock.MagicMock(spec=DagsterCloudUserCodeLauncher)
        launcher.SENTINEL_BASE_DIR_ENV_VAR = env_var
        launcher._default_sentinel_dir = "/opt"  # noqa: SLF001
        result = DagsterCloudUserCodeLauncher.sentinel_dir.fget(launcher)  # pyright: ignore[reportOptionalCall]
        assert result is None


def test_agent_liveness_sentinel_uses_custom_dir(agent, tmp_path):
    agent._last_liveness_check_time = None  # noqa: SLF001

    agent._write_liveness_sentinel_if_overdue(str(tmp_path))  # noqa: SLF001

    assert (tmp_path / "liveness_sentinel.txt").exists()


def test_readiness_sentinel_writes_to_sentinel_dir(tmp_path):
    """Base class _write_readiness_sentinel writes to sentinel_dir."""
    launcher = mock.MagicMock(spec=DagsterCloudUserCodeLauncher)
    launcher.sentinel_dir = str(tmp_path)
    launcher._logger = logging.getLogger("test")  # noqa: SLF001

    DagsterCloudUserCodeLauncher._write_readiness_sentinel(launcher)  # noqa: SLF001

    assert (tmp_path / "finished_initial_reconciliation_sentinel.txt").exists()


def test_readiness_sentinel_noop_when_no_sentinel_dir(tmp_path):
    """Base class _write_readiness_sentinel is a no-op when sentinel_dir is None."""
    launcher = mock.MagicMock(spec=DagsterCloudUserCodeLauncher)
    launcher.sentinel_dir = None

    DagsterCloudUserCodeLauncher._write_readiness_sentinel(launcher)  # noqa: SLF001

    # No sentinel file should exist anywhere
    assert not list(tmp_path.glob("*sentinel*"))


def test_ecs_sentinel_path_is_opt(tmp_path):
    """ECS healthchecks expect /opt/finished_initial_reconciliation_sentinel.txt.

    This is checked in CloudFormation templates and the serverless template.
    Changing this default will break deploys.
    """
    env_var = DagsterCloudUserCodeLauncher.SENTINEL_BASE_DIR_ENV_VAR
    with mock.patch.dict(os.environ, {}, clear=False):
        os.environ.pop(env_var, None)

        launcher = mock.MagicMock(spec=EcsUserCodeLauncher)
        launcher.SENTINEL_BASE_DIR_ENV_VAR = env_var
        launcher._default_sentinel_dir = EcsUserCodeLauncher._default_sentinel_dir.fget(launcher)  # pyright: ignore[reportOptionalCall]  # noqa: SLF001
        sentinel_dir = DagsterCloudUserCodeLauncher.sentinel_dir.fget(launcher)  # pyright: ignore[reportOptionalCall]
        assert sentinel_dir == "/opt"
        assert (
            os.path.join(sentinel_dir, "finished_initial_reconciliation_sentinel.txt")
            == "/opt/finished_initial_reconciliation_sentinel.txt"
        )


def test_serverless_sentinel_path_is_opt():
    """Serverless launcher inherits ECS default of /opt.

    The serverless template healthcheck expects /opt/finished_initial_reconciliation_sentinel.txt.
    Changing this default will break deploys.
    """
    serverless_mod = pytest.importorskip(
        "dagster_cloud_serverless_agent.serverless.user_code_launcher"
    )
    ServerlessUserCodeLauncher = serverless_mod.ServerlessUserCodeLauncher

    env_var = DagsterCloudUserCodeLauncher.SENTINEL_BASE_DIR_ENV_VAR
    with mock.patch.dict(os.environ, {}, clear=False):
        os.environ.pop(env_var, None)

        launcher = mock.MagicMock(spec=ServerlessUserCodeLauncher)
        launcher.SENTINEL_BASE_DIR_ENV_VAR = env_var
        launcher._default_sentinel_dir = ServerlessUserCodeLauncher._default_sentinel_dir.fget(  # pyright: ignore[reportOptionalCall]  # noqa: SLF001
            launcher
        )
        sentinel_dir = DagsterCloudUserCodeLauncher.sentinel_dir.fget(launcher)  # pyright: ignore[reportOptionalCall]
        assert sentinel_dir == "/opt"
        assert (
            os.path.join(sentinel_dir, "finished_initial_reconciliation_sentinel.txt")
            == "/opt/finished_initial_reconciliation_sentinel.txt"
        )


def test_legacy_snap_upload(
    host_instance,
    legacy_snapshot_upload_agent_instance,
    cloud_storage,
):
    user_code_launcher = legacy_snapshot_upload_agent_instance.user_code_launcher
    _add_location(cloud_storage)

    with DagsterCloudAgent(legacy_snapshot_upload_agent_instance) as agent:
        _run_initial_reconcilation(agent, user_code_launcher)

        dagster_cloud_api_call(
            host_instance,
            DagsterCloudApi.CHECK_FOR_WORKSPACE_UPDATES,
            wait_for_response=False,
        )
        _run_to_request_completion(agent, user_code_launcher)
        user_code_launcher.reconcile()

        location_entries = host_instance.cloud_storage.all_workspace_location_entries()
        assert location_entries.get("location")
        assert location_entries["location"].code_location
        ex_job = (
            location_entries["location"]
            .code_location.get_repository("repo")
            .get_full_job("success_job")
        )
        assert ex_job.identifying_job_snapshot_id == success_job.get_job_snapshot_id()
        assert ex_job.job_snapshot


@pytest.fixture
def allowed_locations_agent(allowed_locations_agent_instance):
    with DagsterCloudAgent(allowed_locations_agent_instance) as agent:
        yield agent


@pytest.fixture
def allowed_locations_user_code_launcher(allowed_locations_agent_instance):
    user_code_launcher = allowed_locations_agent_instance.user_code_launcher
    user_code_launcher.start(run_reconcile_thread=False, run_metrics_thread=False)
    yield user_code_launcher


@pytest.fixture
def allowed_branch_locations_agent(allowed_branch_locations_agent_instance):
    with DagsterCloudAgent(allowed_branch_locations_agent_instance) as agent:
        yield agent


@pytest.fixture
def allowed_branch_locations_user_code_launcher(allowed_branch_locations_agent_instance):
    user_code_launcher = allowed_branch_locations_agent_instance.user_code_launcher
    user_code_launcher.start(run_reconcile_thread=False, run_metrics_thread=False)
    yield user_code_launcher


def test_allowed_full_deployment_locations_filters_workspace_updates(
    allowed_locations_agent,
    allowed_locations_agent_instance,
    allowed_locations_user_code_launcher,
    host_instance,
    cloud_storage,
):
    """Test that locations not in allowed_full_deployment_locations are filtered during workspace updates."""
    deployment = allowed_locations_agent_instance.deployment_name
    assert deployment == "sandbox"

    # Run initial reconciliation
    _run_initial_reconcilation(allowed_locations_agent, allowed_locations_user_code_launcher)

    # Add two locations - one allowed and one not allowed
    _add_location(cloud_storage, "allowed-location")
    _add_location(cloud_storage, "disallowed-location")

    # Trigger workspace update
    dagster_cloud_api_call(
        host_instance,
        DagsterCloudApi.CHECK_FOR_WORKSPACE_UPDATES,
        wait_for_response=False,
    )
    _run_to_request_completion(allowed_locations_agent, allowed_locations_user_code_launcher)

    allowed_locations_user_code_launcher.reconcile()

    # Only the allowed location should have a grpc endpoint
    endpoints = allowed_locations_user_code_launcher.get_grpc_endpoints()
    assert len(endpoints) == 1

    allowed_endpoint = allowed_locations_user_code_launcher.get_grpc_endpoint(
        deployment,
        "allowed-location",
    )
    assert allowed_endpoint

    with pytest.raises(
        Exception, match="No server endpoint exists for sandbox:disallowed-location"
    ):
        allowed_locations_user_code_launcher.get_grpc_endpoint(
            deployment,
            "disallowed-location",
        )


def test_allowed_branch_deployment_locations_filters_workspace_updates(
    allowed_branch_locations_agent,
    allowed_branch_locations_agent_instance,
    allowed_branch_locations_user_code_launcher,
    branch1_instance,
):
    """Test that locations not in allowed_branch_deployment_locations are filtered during workspace updates."""
    # Run initial reconciliation
    _run_initial_reconcilation(
        allowed_branch_locations_agent, allowed_branch_locations_user_code_launcher
    )

    cloud_storage = branch1_instance.cloud_storage

    # Add two locations - one allowed and one not allowed
    _add_location(cloud_storage, "allowed-branch-location")
    _add_location(cloud_storage, "disallowed-branch-location")

    # Trigger workspace update
    dagster_cloud_api_call(
        branch1_instance,
        DagsterCloudApi.CHECK_FOR_WORKSPACE_UPDATES,
        wait_for_response=False,
    )
    _run_to_request_completion(
        allowed_branch_locations_agent, allowed_branch_locations_user_code_launcher
    )

    allowed_branch_locations_user_code_launcher.reconcile()

    # Only the allowed location should have a grpc endpoint
    endpoints = allowed_branch_locations_user_code_launcher.get_grpc_endpoints()
    assert len(endpoints) == 1

    # Check that only allowed location has endpoint
    all_endpoints = allowed_branch_locations_user_code_launcher.get_grpc_endpoints()
    location_names = [
        loc_name for (dep_name, loc_name), endpoint in all_endpoints.items() if endpoint is not None
    ]
    assert "allowed-branch-location" in location_names
    assert "disallowed-branch-location" not in location_names


def test_allowed_locations_rejects_api_requests(
    allowed_locations_agent,
    allowed_locations_agent_instance,
    allowed_locations_user_code_launcher,
    host_instance,
    cloud_storage,
):
    """Test that API requests for disallowed locations raise an exception."""
    deployment = allowed_locations_agent_instance.deployment_name

    # Run initial reconciliation
    _run_initial_reconcilation(allowed_locations_agent, allowed_locations_user_code_launcher)

    # Add a disallowed location
    _add_location(cloud_storage, "disallowed-location")

    remote_job_origin = RemoteJobOrigin(
        repository_origin=RemoteRepositoryOrigin(
            code_location_origin=RegisteredCodeLocationOrigin(location_name="disallowed-location"),
            repository_name="repo",
        ),
        job_name="success_job",
    )

    # Try to make an API request for the disallowed location - should raise exception
    gen_response = gen_dagster_cloud_api_call(
        host_instance,
        DagsterCloudApi.GET_SUBSET_EXTERNAL_PIPELINE_RESULT,
        JobSubsetSnapshotArgs(
            job_origin=remote_job_origin,
            op_selection=None,
            asset_selection=None,
            include_parent_snapshot=False,
        ),
        wait_for_response=True,
    )
    next(gen_response)

    _run_to_request_completion(allowed_locations_agent, allowed_locations_user_code_launcher)

    with pytest.raises(Exception) as exc_info:
        list(gen_response)

    assert "not allowed to serve location 'disallowed-location'" in str(exc_info.value)
    assert f"in deployment '{deployment}'" in str(exc_info.value)


def test_allowed_branch_locations_rejects_api_requests(
    allowed_branch_locations_agent,
    allowed_branch_locations_agent_instance,
    allowed_branch_locations_user_code_launcher,
    branch1_instance,
):
    """Test that API requests for disallowed branch locations raise an exception."""
    # Run initial reconciliation
    _run_initial_reconcilation(
        allowed_branch_locations_agent, allowed_branch_locations_user_code_launcher
    )

    # Add a disallowed branch location
    _add_location(branch1_instance.cloud_storage, "disallowed-branch-location")

    remote_job_origin = RemoteJobOrigin(
        repository_origin=RemoteRepositoryOrigin(
            code_location_origin=RegisteredCodeLocationOrigin(
                location_name="disallowed-branch-location"
            ),
            repository_name="repo",
        ),
        job_name="success_job",
    )

    # Try to make an API request for the disallowed location - should raise exception
    gen_response = gen_dagster_cloud_api_call(
        branch1_instance,
        DagsterCloudApi.GET_SUBSET_EXTERNAL_PIPELINE_RESULT,
        JobSubsetSnapshotArgs(
            job_origin=remote_job_origin,
            op_selection=None,
            asset_selection=None,
            include_parent_snapshot=False,
        ),
        wait_for_response=True,
    )
    next(gen_response)

    _run_to_request_completion(
        allowed_branch_locations_agent, allowed_branch_locations_user_code_launcher
    )

    with pytest.raises(Exception) as exc_info:
        list(gen_response)

    assert "not allowed to serve location 'disallowed-branch-location'" in str(exc_info.value)
    assert "for branch deployments" in str(exc_info.value)
