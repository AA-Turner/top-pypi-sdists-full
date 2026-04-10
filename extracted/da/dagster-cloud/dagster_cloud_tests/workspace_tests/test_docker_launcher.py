# ruff: noqa: SLF001
import time
from contextlib import contextmanager

import docker
import pytest
from dagster._core.test_utils import instance_for_test
from dagster_cloud.workspace.docker import (
    AGENT_LABEL,
    GRPC_SERVER_LABEL,
    STOP_TIMEOUT_LABEL,
    DockerUserCodeLauncher,
)
from dagster_cloud.workspace.docker.utils import unique_docker_resource_name
from dagster_cloud.workspace.user_code_launcher import DEFAULT_SERVER_PROCESS_STARTUP_TIMEOUT
from dagster_cloud.workspace.user_code_launcher.user_code_launcher import UserCodeLauncherEntry
from dagster_cloud.workspace.user_code_launcher.utils import deterministic_label_for_location
from dagster_cloud_cli.core.workspace import CodeLocationDeployData


@pytest.fixture
def docker_client():
    client = docker.client.from_env()

    existing_containers = client.containers.list(all=True)

    yield client

    for container in client.containers.list(all=True):
        if container not in existing_containers:
            container.stop()
            container.remove(force=True)


def test_config():
    assert DockerUserCodeLauncher.config_type()


@contextmanager
def docker_instance(user_code_launcher_overrides=None):
    with instance_for_test(
        {
            "instance_class": {
                "module": "dagster_cloud",
                "class": "DagsterCloudAgentInstance",
            },
            "user_code_launcher": {
                "module": "dagster_cloud.workspace.docker",
                "class": "DockerUserCodeLauncher",
                "config": user_code_launcher_overrides or {},
            },
            "dagster_cloud_api": {
                "url": "http://localhost:2874",
                "agent_token": "FAKE_TOKEN",
            },
            "compute_logs": {
                "module": "dagster._core.storage.noop_compute_log_manager",
                "class": "NoOpComputeLogManager",
            },
        }
    ) as instance:
        yield instance


def test_default_instance():
    with docker_instance() as instance:
        assert instance.user_code_launcher.env_vars == []  # pyright: ignore[reportAttributeAccessIssue]
        assert instance.user_code_launcher.container_kwargs == {}  # pyright: ignore[reportAttributeAccessIssue]
        assert (
            instance.user_code_launcher._server_process_startup_timeout  # pyright: ignore[reportAttributeAccessIssue]
            == DEFAULT_SERVER_PROCESS_STARTUP_TIMEOUT
        )


def test_container_kwargs():
    container_kwargs = {"auto_remove": True}
    with docker_instance({"container_kwargs": container_kwargs}) as instance:
        assert instance.run_launcher.container_kwargs == container_kwargs  # pyright: ignore[reportAttributeAccessIssue]


def test_override_timeout():
    with docker_instance({"server_process_startup_timeout": 1234}) as instance:
        assert instance.user_code_launcher._server_process_startup_timeout == 1234  # pyright: ignore[reportAttributeAccessIssue]


def test_get_standalone_server_handles_for_location(docker_client):
    with docker_instance() as instance:
        assert not instance.user_code_launcher._get_standalone_dagster_server_handles_for_location(  # pyright: ignore[reportAttributeAccessIssue]
            deployment_name="foo",
            location_name="bar",
        )

        docker_client.images.pull("dagster/dagster-cloud-examples:1.12.5")
        docker_client.containers.create(
            image="dagster/dagster-cloud-examples:1.12.5",
            labels={
                GRPC_SERVER_LABEL: "",
                deterministic_label_for_location("foo", "bar"): "",
                AGENT_LABEL: instance.instance_uuid,  # pyright: ignore[reportAttributeAccessIssue]
            },
        )

        handles = instance.user_code_launcher._get_standalone_dagster_server_handles_for_location(  # pyright: ignore[reportAttributeAccessIssue]
            deployment_name="foo",
            location_name="bar",
        )

        assert len(handles) == 1

        handle = handles[0]
        create_timestamp = instance.user_code_launcher.get_server_create_timestamp(handle)  # pyright: ignore[reportAttributeAccessIssue]

        assert create_timestamp <= time.time() and create_timestamp >= time.time() - 60 * 5


def test_long_docker_resource_name():
    long_deployment_name = "a" * 128
    long_location_name = "b" * 128

    assert len(unique_docker_resource_name(long_deployment_name, long_location_name)) == 63


def test_container_kwargs_stop_timeout():
    with docker_instance() as instance:
        assert not instance.user_code_launcher._get_standalone_dagster_server_handles_for_location(  # pyright: ignore[reportAttributeAccessIssue]
            deployment_name="foo",
            location_name="bar",
        )

        result = instance.user_code_launcher._start_new_server_spinup(  # type: ignore
            deployment_name="foo",
            location_name="bar",
            desired_entry=UserCodeLauncherEntry(
                code_location_deploy_data=CodeLocationDeployData(
                    image="dagster/dagster-cloud-examples:1.9.10",
                    package_name="dagster-cloud-examples",
                    container_context={"docker": {"container_kwargs": {"stop_timeout": 23}}},
                ),
                update_timestamp=time.time(),
            ),
        )
        assert result.server_handle.container.labels[STOP_TIMEOUT_LABEL] == "23"

        assert instance.user_code_launcher._get_standalone_dagster_server_handles_for_location(  # pyright: ignore[reportAttributeAccessIssue]
            deployment_name="foo",
            location_name="bar",
        )

        instance.user_code_launcher._remove_server_handle(result.server_handle)  # type: ignore
