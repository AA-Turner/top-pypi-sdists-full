from logging import Logger
import time
from typing import List
from _qwak_proto.qwak.builds.builds_pb2 import BuildStatus
from qwak.clients.build_orchestrator import BuildOrchestratorClient


def __get_current_status(build_id) -> BuildStatus:
    return BuildOrchestratorClient().get_build(build_id).build.build_status


def __end_state_statuses() -> List[BuildStatus.ValueType]:
    return [BuildStatus.FAILED, BuildStatus.SUCCESSFUL, BuildStatus.REMOTE_BUILD_CANCELLED, BuildStatus.REMOTE_BUILD_TIMED_OUT]


def wait_until_finished(build_id, log: Logger, pool_interval_seconds=10) -> None:
    status = __get_current_status(build_id)
    log.info(f"Waiting for build {build_id} to finish. Aborting this process will not stop the build!")
    log.debug(f"Current status of build {build_id}: {BuildStatus.DESCRIPTOR.values_by_number[status].name}")
    while status not in __end_state_statuses():
        time.sleep(pool_interval_seconds)
        status = __get_current_status(build_id)
        log.debug(f"Current status of build {build_id}: {BuildStatus.DESCRIPTOR.values_by_number[status].name}")


def is_final_status_successful(build_id) -> bool:
    return __get_current_status(build_id) == BuildStatus.SUCCESSFUL
