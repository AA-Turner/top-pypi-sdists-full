# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import threading

import contrast
from contrast.agent.heartbeat_thread import HEARTBEAT_THREAD_NAME
from contrast.agent.settings import Settings
from contrast.agent.settings_threads import SETTINGS_THREAD_NAME
from contrast.agent.telemetry import TELEMETRY_THREAD_NAME, Telemetry
from contrast.reporting import get_reporting_client
from contrast.reporting.reporting_client import (
    REPORTING_CLIENT_THREAD_NAME,
)
from contrast.utils.decorators import fail_quietly
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")

LOG_MSG = "%s thread wasn't running - restarting it now"

# The lock here is to prevent a race condition when restarting background threads.
# We need to ensure that only one thread at once can get the list of running threads and
# act accordingly based on that list.
MODULE_LOCK = threading.Lock()


@fail_quietly("failed to check background threads")
def ensure_running(agent_state_module, skip_telemetry=False):
    """
    Check that long-running agent background threads are running in the current process.
    Restart any threads that appear to have been killed.

    This occurs most often when a webserver that preloads the application forks its
    master process to spawn workers. In this case, any threads started in the master
    process don't transfer over to workers, so they need to be restarted.

    :param skip_telemetry: If `True`, do not check the telemetry thread
    """
    logger.debug("checking background threads")

    with MODULE_LOCK:
        # PERF: this is a critical section (inside of a lock). Be mindful!
        threads_by_name = {t.name: t for t in threading.enumerate()}
        _check_reporting_client(threads_by_name, agent_state_module)
        if not skip_telemetry:
            _check_telemetry(threads_by_name)
        _check_heartbeat(threads_by_name, agent_state_module.reporting_client)
        _check_settings(threads_by_name, agent_state_module.reporting_client)


def _check_telemetry(threads_by_name):
    # PERF: this is a critical section (inside of a lock). Be mindful!
    thread = threads_by_name.get(TELEMETRY_THREAD_NAME)
    if thread is not None or contrast.telemetry_disabled():
        return

    logger.debug(LOG_MSG, TELEMETRY_THREAD_NAME)
    contrast.TELEMETRY = Telemetry()
    contrast.TELEMETRY.start()


def _check_heartbeat(threads_by_name, reporting_client):
    # PERF: this is a critical section (inside of a lock). Be mindful!
    thread = threads_by_name.get(HEARTBEAT_THREAD_NAME)
    if thread is not None:
        return

    settings = Settings()
    logger.debug(LOG_MSG, HEARTBEAT_THREAD_NAME)
    settings.heartbeat = None
    settings.establish_heartbeat(reporting_client)


def _check_settings(threads_by_name, reporting_client):
    # PERF: this is a critical section (inside of a lock). Be mindful!
    thread = threads_by_name.get(SETTINGS_THREAD_NAME)
    if thread is not None:
        return

    settings = Settings()
    logger.debug(LOG_MSG, SETTINGS_THREAD_NAME)
    settings.settings_thread = None
    settings.establish_settings_thread(reporting_client)


def _check_reporting_client(threads_by_name, agent_state_module):
    # PERF: this is a critical section (inside of a lock). Be mindful!
    thread = threads_by_name.get(REPORTING_CLIENT_THREAD_NAME)
    if thread is not None:
        return

    # the reporting client thread should always be running; there are no conditions here

    logger.debug(LOG_MSG, REPORTING_CLIENT_THREAD_NAME)
    agent_state_module.reporting_client = get_reporting_client(Settings().config)
    agent_state_module.reporting_client.start()
