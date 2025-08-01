# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import threading
from contrast.agent import scope
from contrast.agent.settings import Settings
from contrast.reporting.teamserver_messages import Heartbeat
from contrast.utils.decorators import fail_loudly
from contrast.utils.timer import now_ms, sleep

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")
HEARTBEAT_THREAD_NAME = "ContrastHeartbeat"


class HeartbeatThread(threading.Thread):
    def __init__(self, reporting_client):
        self.stopped = False
        self.heartbeat_interval_ms = Settings().config.heartbeat_poll_interval
        # Agent should not ping too frequently
        self.heartbeat_interval_ms = max(10000, self.heartbeat_interval_ms)

        super().__init__()
        # A thread must have had __init__ called, but not start, to set daemon
        self.daemon = True
        self.name = HEARTBEAT_THREAD_NAME
        self.reporting_client = reporting_client

    def start(self):
        self.stopped = False
        super().start()

    @property
    def settings_interval_sec(self):
        return self.heartbeat_interval_ms / 1000

    def run(self):
        # Ensure the heartbeat thread runs in scope because it is initialized
        # before our thread.start patch is applied.
        with scope.contrast_scope():
            logger.debug("Establishing heartbeat")

            while not self.stopped and Settings().is_agent_config_enabled():
                self.send_heartbeat()
                sleep(self.settings_interval_sec)

    @fail_loudly("Error sending a heartbeat message")
    def send_heartbeat(self):
        settings = Settings()
        if settings.config is None:
            return

        # only send after we have not updated after the last interval time set in the config
        if (
            settings.last_app_update_time_ms is None
            or (now_ms() - settings.last_app_update_time_ms)
            < self.heartbeat_interval_ms
        ):
            return

        msg = Heartbeat()
        response = self.reporting_client.send_message(msg)
        msg.process_response(response, self.reporting_client)
