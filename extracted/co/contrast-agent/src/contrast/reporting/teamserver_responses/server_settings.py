# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

from contrast.utils.mapping import GlomDict


class ServerSettings:
    """
    This class is responsible for safely parsing V1 TeamServer Server Settings from a
    response to a usable format. The format can be found here:
    https://github.com/Contrast-Security-Inc/contrast-agent-api-spec

    At the time of the creation of this class, the specific schema is ServerSettings in
    agent-endpoints.yml.
    """

    def __init__(self, server_settings_json: dict | None = None):
        self.server_settings_json = GlomDict(server_settings_json or {})

    def common_config(self) -> dict[str, object]:
        """
        Returns the settings in a flattened common configuration format.
        """
        return {
            "server.environment": self.server_settings_json.get("environment", ""),
            "assess.enable": self.server_settings_json.get("assess.enable"),
            "assess.sampling.enable": self.server_settings_json.get(
                "assess.sampling.enable", False
            ),
            "assess.sampling.baseline": self.server_settings_json.get(
                "assess.sampling.baseline"
            ),
            "assess.sampling.request_frequency": self.server_settings_json.get(
                "assess.sampling.request_frequency"
            ),
            "assess.sampling.window_ms": (
                # teamserver incorrectly reports window_ms in seconds
                window * 1000
                if (
                    window := self.server_settings_json.get("assess.sampling.window_ms")
                )
                else None
            ),
            "agent.logger.level": self.server_settings_json.get("logger.level"),
            "agent.logger.path": self.server_settings_json.get("logger.path"),
            "agent.security_logger.syslog.enable": self.server_settings_json.get(
                "security_logger.syslog.enable"
            ),
            "agent.security_logger.syslog.protocol": self.server_settings_json.get(
                "security_logger.syslog.protocol"
            ),
            # security_logger.syslog.connection_type is ignored because the protocol
            # includes the connection type.
            "agent.security_logger.syslog.server_host": self.server_settings_json.get(
                "security_logger.syslog.ip"
            ),
            "agent.security_logger.syslog.port": self.server_settings_json.get(
                "security_logger.syslog.port"
            ),
            "agent.security_logger.syslog.facility": self.server_settings_json.get(
                "security_logger.syslog.facility"
            ),
            "agent.security_logger.syslog.severity_exploited": self.server_settings_json.get(
                "security_logger.syslog.severity_exploited"
            ),
            "agent.security_logger.syslog.severity_blocked": self.server_settings_json.get(
                "security_logger.syslog.severity_blocked"
            ),
            "agent.security_logger.syslog.severity_blocked_perimeter": self.server_settings_json.get(
                "security_logger.syslog.severity_blocked_perimeter"
            ),
            "agent.security_logger.syslog.severity_probed": self.server_settings_json.get(
                "security_logger.syslog.severity_probed"
            ),
            "agent.security_logger.syslog.severity_suspicious": self.server_settings_json.get(
                "security_logger.syslog.severity_suspicious"
            ),
            "protect.enable": self.server_settings_json.get("protect.enable"),
        }
