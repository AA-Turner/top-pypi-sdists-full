# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

from .config_builder import ConfigBuilder
from .config_option import ConfigOption
from contrast.utils.configuration_utils import str_to_bool
from contrast.utils.loggers import (
    DEFAULT_PROGNAME,
    DEFAULT_SECURITY_LOG_PATH,
    DEFAULT_SECURITY_LOG_LEVEL,
    DEFAULT_LOG_PATH,
    DEFAULT_LOG_LEVEL,
)


class Agent(ConfigBuilder):
    def __init__(self):
        super().__init__()

        self.default_options = [
            # Some logger default values are handled by the logger
            ConfigOption(
                canonical_name="agent.logger.level",
                default_value=DEFAULT_LOG_LEVEL,
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="agent.logger.path",
                default_value=DEFAULT_LOG_PATH,
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="agent.logger.stdout",
                default_value=False,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="agent.logger.stderr",
                default_value=False,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="agent.logger.backups",
                default_value=10,
                type_cast=int,
            ),
            ConfigOption(
                canonical_name="agent.logger.roll_size",
                default_value=100,  # specified in MB
                type_cast=int,
            ),
            ConfigOption(
                canonical_name="agent.logger.progname",
                default_value=DEFAULT_PROGNAME,
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="agent.security_logger.path",
                default_value=DEFAULT_SECURITY_LOG_PATH,
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="agent.security_logger.level",
                default_value=DEFAULT_SECURITY_LOG_LEVEL,
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="agent.security_logger.syslog.enable",
                default_value=False,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="agent.security_logger.syslog.protocol",
                default_value="UDP",
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="agent.security_logger.syslog.server_host",
                default_value=None,
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="agent.security_logger.syslog.ip",
                default_value=None,
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="agent.security_logger.syslog.port",
                default_value=None,
                type_cast=int,
            ),
            ConfigOption(
                canonical_name="agent.security_logger.syslog.facility",
                default_value=19,
                type_cast=int,
            ),
            ConfigOption(
                canonical_name="agent.security_logger.syslog.severity_exploited",
                default_value="ALERT",
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="agent.security_logger.syslog.severity_blocked",
                default_value="NOTICE",
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="agent.security_logger.syslog.severity_blocked_perimeter",
                default_value="NOTICE",
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="agent.security_logger.syslog.severity_probed",
                default_value="WARNING",
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="agent.security_logger.syslog.severity_suspicious",
                default_value="WARNING",
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="agent.python.pytest_rewrite",
                default_value=False,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="agent.python.enable_automatic_middleware",
                default_value=True,
                type_cast=str_to_bool,
                log_effective_config=False,
            ),
            ConfigOption(
                canonical_name="agent.python.enable_drf_response_analysis",
                default_value=True,
                type_cast=str_to_bool,
                log_effective_config=False,
            ),
            # TODO: PYT-3337 - we should issue a deprecation warning if
            # agent.python.enable_profiler is used
            ConfigOption(
                canonical_name="agent.python.enable_profiler",
                default_value=False,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="agent.python.profiler.enable",
                default_value=False,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="agent.python.tracer.enable",
                default_value=False,
                type_cast=str_to_bool,
            ),
            ConfigOption(
                canonical_name="agent.python.tracer.min_duration_ms",
                default_value=0.010,  # 10us
                type_cast=float,
            ),
            ConfigOption(
                canonical_name="agent.polling.app_settings_ms",
                default_value=30_000,
                type_cast=int,
            ),
            ConfigOption(
                canonical_name="agent.polling.server_settings_ms",
                default_value=30_000,
                type_cast=int,
            ),
            ConfigOption(
                canonical_name="agent.polling.heartbeat_ms",
                default_value=30_000,
                type_cast=int,
            ),
            ConfigOption(
                canonical_name="agent.route_coverage.report_on_error",
                default_value=False,
                type_cast=str_to_bool,
            ),
        ]
