# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import threading

from contrast.agent import scope
from contrast.agent.settings import Settings
from contrast.utils.decorators import fail_loudly
from contrast.utils.timer import sleep
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")
SETTINGS_THREAD_NAME = "ContrastSettings"
MIN_INTERVAL_MS = 10_000


class SettingsThread(threading.Thread):
    def __init__(self, reporting_client):
        self.stopped = False
        # Agent should not ping too frequently
        self.settings_interval_ms = max(
            min(
                Settings().config.application_settings_poll_interval,
                Settings().config.server_settings_poll_interval,
            ),
            MIN_INTERVAL_MS,
        )
        self.reporting_client = reporting_client

        super().__init__()
        # A thread must have had __init__ called, but not start, to set daemon
        self.daemon = True
        self.name = SETTINGS_THREAD_NAME

    def start(self):
        self.stopped = False
        super().start()

    @property
    def settings_interval_sec(self):
        return self.settings_interval_ms / 1000

    def run(self):
        # Ensure the polling thread runs in scope because it is
        # initialized before our thread.start patch is applied.
        with scope.contrast_scope():
            logger.debug("Starting settings polling thread", name=self.name)
            while not self.stopped and Settings().is_agent_config_enabled():
                self.send_settings()
                sleep(self.settings_interval_sec)

    @fail_loudly("Error sending settings message")
    def send_settings(self):
        settings = Settings()
        if settings.config is None:
            return

        if ui_settings := self.reporting_client.get_settings_if_changed():
            # The agent was designed with the intention of having Server settings before Application settings.
            # This order must be maintained or a more significant refactor is required.
            settings.apply_server_settings(ui_settings.get("server_settings", {}))
            settings.apply_application_settings(
                ui_settings.get("application_settings", {})
            )
            settings.apply_identification(ui_settings.get("identification", {}))

            settings.log_effective_config()
            if (
                settings.is_agent_config_enabled()
                # This is necessary to ensure the application exists in TeamServer
                and settings.config.session_id != ""
            ):
                self.reporting_client.new_effective_config(
                    settings.generate_effective_config()
                )
