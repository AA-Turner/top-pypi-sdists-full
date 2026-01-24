# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import platform
import sys

from datetime import datetime, timezone
from typing import Any

import contrast
from contrast import __version__
from contrast.agent.exceptions import _Exception
from contrast.agent.validator import Validator
from contrast.agent.metrics import MetricsDict
from contrast_rewriter import is_rewriter_enabled
from contrast_vendor import structlog as logging


logger = logging.getLogger("contrast")


class TelemetryEvent:
    def __init__(self, instance_id: str):
        self.timestamp = datetime.now(timezone.utc).astimezone().isoformat()
        self.telemetry_instance_id = instance_id
        self.tags = MetricsDict(str)

    @property
    def path(self) -> str:
        return ""

    def add_tags(self) -> None:
        from contrast.agent.agent_state import (
            detected_framework,
            free_threading_available,
            free_threading_enabled,
            jit_available,
            jit_enabled,
        )

        telemetry = contrast.TELEMETRY
        settings = telemetry.settings

        self.tags["is_public_build"] = str(telemetry.is_public_build).lower()
        self.tags["agent_version"] = __version__
        self.tags["python_version"] = sys.version
        self.tags["python_version_simple"] = platform.python_version()
        self.tags["os_type"] = platform.system()
        self.tags["os_arch"] = platform.machine()
        self.tags["os_version"] = platform.version()
        self.tags["app_framework_version"] = str(detected_framework())
        self.tags["server_framework_version"] = str(settings.server)
        self.tags["teamserver"] = settings.config.teamserver_type
        self.tags["rewriter_enabled"] = str(is_rewriter_enabled()).lower()
        self.tags["free_threading_available"] = str(free_threading_available()).lower()
        self.tags["free_threading_enabled"] = str(free_threading_enabled()).lower()
        self.tags["jit_available"] = str(jit_available()).lower()
        self.tags["jit_enabled"] = str(jit_enabled()).lower()

    def to_json(self) -> dict[str, Any]:
        return dict(
            timestamp=self.timestamp,
            instance=self.telemetry_instance_id,
            tags=self.tags,
        )


class MetricsTelemetryEvent(TelemetryEvent):
    def __init__(self, instance_id: str) -> None:
        super().__init__(instance_id)
        self.fields = MetricsDict(int)
        self.fields["_filler"] = 0

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.to_json()}"

    def to_json(self) -> dict[str, Any]:
        return {
            **super().to_json(),
            **dict(fields=self.fields),
        }


class StartupMetricsTelemetryEvent(MetricsTelemetryEvent):
    def __init__(self, instance_id: str) -> None:
        super().__init__(instance_id)

        try:
            self.add_tags()
        except Exception as ex:
            logger.debug("Telemetry failed to create StartupMetrics msg: %s", ex)
            logger.debug("Disabling telemetry")
            contrast.TELEMETRY.enabled = False

    @property
    def path(self) -> str:
        return "/metrics/startup"


class ErrorTelemetryEvent(TelemetryEvent, Validator):
    VALIDATIONS = dict(
        telemetry_instance_id=dict(required=True, range=(12, 64)),
        # tags field is required to be reported but can be empty
        tags=dict(required=True, range=(0, 512)),
        exceptions=dict(required=True, range=(1, 512)),
        # some agents use this for named logger
        logger=dict(required=False, range=(0, 128)),
        # logged message, not exception message
        message=dict(required=False, range=(0, 256)),
        occurrences=dict(required=False, default=0),
    )

    def __init__(
        self, instance_id: str, error: Exception, logger_="", message="", skip_frames=0
    ) -> None:
        super().__init__(instance_id)

        # We may not use this field, it's meant to represent a named logger
        # to easily filter a specific feature
        self.logger = logger_
        # message that was logged, not the exception message
        self.message = message
        self.occurrences = 1
        # +1 to skip the current ErrorTelemetryEvent frame
        self.exceptions = [_Exception(error, skip_frames + 1)]

        try:
            self.add_tags()
        except Exception as ex:
            logger.debug("Adding tags failed: %s", ex)

        self.validate()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.to_json()}"

    @property
    def path(self) -> str:
        return "/exceptions/error"

    def to_json(self) -> dict[str, Any]:
        return {
            **super().to_json(),
            **dict(
                occurrences=self.occurrences,
                logger=self.logger,
                message=self.message,
                exceptions=[ex.to_json() for ex in self.exceptions],
            ),
        }
