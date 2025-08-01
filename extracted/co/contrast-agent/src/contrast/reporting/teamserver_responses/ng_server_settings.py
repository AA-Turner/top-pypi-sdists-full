# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

from contrast.utils.mapping import GlomDict


class NGServerSettings:
    def __init__(self, features: dict | None = None):
        self.features = GlomDict(features or {})

    def common_config(self) -> dict[str, object]:
        """
        Returns the settings in a flattened common configuration format.
        """
        return {
            "server.environment": self.features.get("environment", ""),
            "assess.enable": self.features.get("features.assessment.enabled"),
            "assess.sampling.enable": self.features.get(
                "features.assessment.sampling.enabled", False
            ),
            "assess.sampling.baseline": self.features.get(
                "features.assessment.sampling.baseline"
            ),
            "assess.sampling.request_frequency": self.features.get(
                "features.assessment.sampling.frequency"
            ),
            "assess.sampling.window_ms": (
                window * 1000
                if (window := self.features.get("features.assessment.sampling.window"))
                else None
            ),
            "agent.logger.level": self.features.get("features.logLevel"),
            "agent.logger.path": self.features.get("features.logFile"),
            "agent.security_logger.syslog.enable": self.features.get(
                "features.defend.syslog.syslogEnabled"
            ),
            "agent.security_logger.syslog.protocol": self.features.get(
                "features.defend.syslog.syslogProtocol"
            ),
            # features.defend.syslog.syslogConnectionType is ignored because the protocol
            # includes the connection type.
            "agent.security_logger.syslog.server_host": self.features.get(
                "features.defend.syslog.syslogIpAddress"
            ),
            "agent.security_logger.syslog.port": self.features.get(
                "features.defend.syslog.syslogPortNumber"
            ),
            "agent.security_logger.syslog.facility": self.features.get(
                "features.defend.syslog.syslogFacilityCode"
            ),
            "agent.security_logger.syslog.severity_exploited": self.features.get(
                "features.defend.syslog.syslogSeverityExploited"
            ),
            "agent.security_logger.syslog.severity_blocked": self.features.get(
                "features.defend.syslog.syslogSeverityBlocked"
            ),
            # there is no severity_blocked_perimeter in the ng version of the endpoint.
            "agent.security_logger.syslog.severity_probed": self.features.get(
                "features.defend.syslog.syslogSeverityProbed"
            ),
            "agent.security_logger.syslog.severity_suspicious": self.features.get(
                "features.defend.syslog.syslogSeveritySuspicious"
            ),
            "protect.enable": self.features.get("features.defend.enabled", False),
        }
