import time

import pytest
from dagster_cloud.execution.utils import TaskStatus
from dagster_cloud.execution.utils.process import check_on_process, kill_process, launch_process
from dagster_cloud.workspace.user_code_launcher import DEFAULT_SERVER_PROCESS_STARTUP_TIMEOUT

from dagster_cloud_tests import gen_agent_instance


@pytest.fixture
def cleaup_zombie_processes(agent_instance_local_ursula):
    agent_instance_local_ursula.user_code_launcher.start()
    yield


def test_default_instance(agent_instance):
    assert (
        agent_instance.user_code_launcher._server_process_startup_timeout  # noqa: SLF001
        == DEFAULT_SERVER_PROCESS_STARTUP_TIMEOUT
    )


def test_override_timeout(dagster_cloud_url):
    with gen_agent_instance(
        dagster_cloud_url,
        "token",
        user_code_launcher_config={"server_process_startup_timeout": 1234},
    ) as instance:
        assert instance.user_code_launcher._server_process_startup_timeout == 1234  # noqa: SLF001  # pyright: ignore[reportAttributeAccessIssue]


def test_launch_process(tmp_path, cleaup_zombie_processes):
    test_file = tmp_path / "test_file"
    launch_process(["touch", str(test_file)])

    start_time = time.time()
    while not test_file.exists():
        time.sleep(0.1)
        if time.time() - start_time > 10:
            raise Exception("Timed out waiting for process to create file")


def test_kill_process(cleaup_zombie_processes):
    pid = launch_process(["sleep", "300"])
    assert check_on_process(pid) == TaskStatus.RUNNING
    kill_process(pid)

    start_time = time.time()
    while check_on_process(pid) == TaskStatus.RUNNING:
        time.sleep(0.1)
        if time.time() - start_time > 10:
            raise Exception("Timed out waiting for process to be killed")

    assert check_on_process(pid) == TaskStatus.NOT_FOUND


def test_check_on_process(cleaup_zombie_processes):
    assert check_on_process(123456789) == TaskStatus.NOT_FOUND
