# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
from collections.abc import Mapping
from functools import lru_cache
import os
import socket
import ssl
import sys

import logging as stdlib_logging
import logging.handlers as stdlib_logging_handlers
from typing import Any, NamedTuple, TextIO

import contrast
from contrast.assess_extensions import cs_str
from contrast.configuration.agent_config import AgentConfig
from contrast.configuration.config_option import ConfigOption
from contrast.utils.decorators import fail_loudly
from contrast.utils.loggers.structlog import RotationConfig, init_structlog
from contrast.utils.configuration_utils import get_hostname
from contrast.utils.namespace import Namespace

from contrast.utils.string_utils import ensure_string
from contrast_vendor import structlog

from . import (
    DEFAULT_LOG_LEVEL,
    DEFAULT_PROGNAME,
    LOGGER_NAME,
    DEFAULT_AGENT_LOGGER_PATH,
)

STDOUT = "STDOUT"
STDERR = "STDERR"

CONFIG_KEY_STDOUT = "agent.logger.stdout"
CONFIG_KEY_STDERR = "agent.logger.stderr"
CONFIG_KEY_LOGGER_PATH = "agent.logger.path"
CONFIG_KEY_LOGGER_LEVEL = "agent.logger.level"
CONFIG_KEY_PROGNAME = "agent.logger.progname"


class module(Namespace):
    initialized: bool = False
    cef_security_logger: stdlib_logging.Logger | None = None
    syslog_logger: SysLogger | None = None


def setup_basic_agent_logger(level="INFO"):
    """
    Setup a logger without any user-supplied configuration, with defaults:
        1. log to stdout
        2. log in INFO level
        3. with default progname

    The logger created here is expected to be overridden with config values
    provided later on in the middleware creation cycle.
    """
    if not module.initialized:
        init_structlog(level, DEFAULT_AGENT_LOGGER_PATH, DEFAULT_PROGNAME)
        module.initialized = True

    return structlog.getLogger(LOGGER_NAME)


def configure_agent_logger(config: AgentConfig) -> None:
    """
    Configures the core agent logger with the user configuration.

    This function can be called multiple times to reconfigure the
    agent logger.
    """
    path_config_option, path = _logger_path(config)
    level_config_option = config.get_option(CONFIG_KEY_LOGGER_LEVEL)
    level = config[CONFIG_KEY_LOGGER_LEVEL].upper()
    progname = config[CONFIG_KEY_PROGNAME]

    cache_logger = _cache_logger(path_config_option, level_config_option)
    rotation_config = (
        None
        if (backups := config["agent.logger.backups"]) == 0
        else RotationConfig(
            backup_count=backups,
            # roll_size is in MB
            max_bytes=config["agent.logger.roll_size"] * 1024 * 1024,
        )
    )
    init_structlog(
        level,
        path,
        progname,
        cache_logger=cache_logger,
        rotation_config=rotation_config,
    )

    cs_str.initialize_logger(structlog.getLogger(LOGGER_NAME))
    # Avoid circular import
    from contrast.agent.agent_lib import update_log_options

    update_log_options(level)


@lru_cache(maxsize=1)
@fail_loudly("Failed to get the fully qualified domain name.", return_value="-")
def _get_fqdn() -> str:
    return socket.getfqdn()


class CEFFormatter(stdlib_logging.Formatter):
    ATTACK_MSG_FMT = (
        f"%(asctime)s {get_hostname()} CEF:0|Contrast Security|Contrast Agent Python|{contrast.__version__}|"
        "SECURITY|%(message)s|%(level)s|pri=%(rule_id)s src=%(source_ip)s spt=%(source_port)s "
        "request=%(request_url)s requestMethod=%(request_method)s app=%(application)s "
        f"contrastAgentServer=%(server)s dvchost={_get_fqdn()} outcome=%(outcome)s"
    )

    def __init__(self):
        super().__init__(CEFFormatter.ATTACK_MSG_FMT, "%b %d %H:%M:%S")


def setup_security_logger(config: Mapping):
    if not config.get("protect.enable"):
        return

    path = config.get("agent.security_logger.path")
    level = config.get("agent.security_logger.level").upper()

    logger = stdlib_logging.getLogger("contrast-security-logger")

    _set_level(logger, level)

    handler = _get_handler(path)
    handler.setFormatter(CEFFormatter())
    logger.addHandler(handler)
    module.cef_security_logger = logger


def _unescaped_protect_rule_msg(rule_name, outcome, evaluation, masker):
    masked_input = masker.mask_attack_input(evaluation.input) if evaluation else None
    input_type = (
        evaluation.input.type.cef_string(masked_input.name) if masked_input else "-"
    )
    input_value = (
        masker.mask_attack_vector(ensure_string(masked_input.value, errors="replace"))
        if masked_input
        else "-"
    )
    if outcome == "exploited":
        if not evaluation:
            return f"An effective attack was detected against {rule_name}"
        return f"The {input_type} had a value that successfully exploited {rule_name} - {input_value}"
    if outcome in ("blocked", "ineffective"):
        if not evaluation:
            return f"An unsuccessful attack was detected against {rule_name}"
        return f"The {input_type} had a value that matched a signature for, but did not successfully exploit {rule_name} - {input_value}"
    if outcome == "suspicious":
        if not evaluation:
            return f"Suspicious activity indicates a potential attack using {rule_name} - {input_value}"
        return f"The {input_type} included a potential attack value that was detected as suspicious using {rule_name} - {input_value}"
    raise ValueError(f"Unknown outcome: {outcome}")


@fail_loudly("Failed to log attack event to security loggers")
def security_log_attack(attack, evaluation):
    """
    Logs a security event to the CEF security logger and syslog logger.

    Virtual patches, IP denylist and bot blocker activities are not yet supported.
    """
    if not module.cef_security_logger and not module.syslog_logger:
        # No security loggers configured.
        return

    from contrast.agent import agent_state

    app_name = agent_state.get_app_name()
    server_name = agent_state.get_server_name()
    masker = agent_state.module.request_data_masker

    ip = port = url = method_name = "-"

    if (context := contrast.REQUEST_CONTEXT.get()) is not None:
        ip = context.request.client_addr or "-"
        port = context.request.host_port
        method_name = context.request.method
        url = context.request.path
        masker = context.request_data_masker

    rule_name = attack.rule_id
    outcome = attack.report_result()
    msg = _escape_prefix(
        _unescaped_protect_rule_msg(rule_name, outcome, evaluation, masker)
    )

    log_context = _escape_metadata(
        {
            "level": "WARN",
            "rule_id": rule_name,
            "source_ip": ip,
            "source_port": port,
            "request_url": url,
            "request_method": method_name,
            "application": app_name or "-",
            "server": server_name or "-",
            "outcome": outcome.upper(),
        }
    )

    if module.cef_security_logger:
        module.cef_security_logger.warning(msg, extra=log_context)
    _syslog_msg(msg, log_context, outcome, perimeter=attack.perimeter_blocked)


def _escape_prefix(msg: str):
    # Order matters here. Escaping `|` before `\` would result in double escaping.
    return (
        msg.replace("\\", r"\\")
        .replace("|", r"\|")
        .replace("\n", r"\n")
        .replace("\r", r"\r")
    )


def _escape_metadata(metadata: dict[str, str]):
    return {
        # Order matters here. `\` must be escaped first since it's used to escape other characters.
        k: v.replace("\\", r"\\")
        .replace("=", r"\=")
        .replace("\n", r"\n")
        .replace("\r", r"\r")
        for k, v in metadata.items()
    }


def _syslog_msg(msg, log_context, outcome, perimeter):
    syslogger = module.syslog_logger
    if not syslogger:
        # syslog logger isn't configured.
        return
    outcome = outcome.lower()
    if perimeter and outcome == "blocked":
        outcome = "blocked_perimeter"
    syslogger.logger.warning(
        msg, extra={**log_context, "_severity": syslogger.outcome_to_severity[outcome]}
    )
    structlog.getLogger(LOGGER_NAME).debug("Sent security event to syslog")


class SysLogger(NamedTuple):
    logger: stdlib_logging.Logger
    outcome_to_severity: dict[str, str]


class SecureSysLogHandler(stdlib_logging_handlers.SysLogHandler):
    """
    A SysLogHandler that logs security events to syslog.

    This handler extends SysLogHandler to use SSL/TLS if the secure option is
    set to True. It also adds security event outcomes as log levels in the
    standard logging module.
    """

    _valid_severities = {
        "ALERT",
        "CRITICAL",
        "ERROR",
        "WARNING",
        "NOTICE",
        "INFO",
        "DEBUG",
    }

    @classmethod
    def severity(cls, s: str):
        if s.upper() not in cls._valid_severities:
            raise ValueError(f"Invalid syslog severity: {s}")
        return s.lower()

    _valid_protocols = {"UDP", "TCP", "TCP_TLS"}

    @classmethod
    def protocol(cls, p: str):
        if p.upper() not in cls._valid_protocols:
            raise ValueError(f"Invalid syslog protocol: {p}")
        return p.upper()

    def __init__(self, *args, secure=False, **kwargs):
        # Store the config so we can reference it later and potentially
        # avoid reconfiguring the logger if the config hasn't changed.
        self.config = {
            "args": args,
            "kwargs": {
                **kwargs,
                "secure": secure,
            },
        }

        super().__init__(*args, **kwargs)
        self.append_nul = False
        if secure:
            ctx = ssl.create_default_context()
            self.socket = ctx.wrap_socket(self.socket, server_hostname=self.address[0])

    def format(self, record) -> str:
        # HACK: The SysLogHandler extension capabilities are based on
        # adding custom logging levels, which is very difficult to do
        # safely as a library. Levels need integers and there's always
        # a chance the integer we choose will conflict with another
        # library. We'd prefer to avoid introducing log levels.
        #
        # Instead, we use this format call as a hook at the start of
        # the emit method to overwrite the levelname since levelname
        # is the only way to set the message priority.
        record.levelname = record.__dict__["_severity"]
        return super().format(record)

    def mapPriority(self, levelName: str) -> str:
        # bypass the priorityMap conversion.
        return levelName

    def close(self) -> None:
        """
        Closes the socket.

        Adds safety checks for before Python 3.10 to account for unset
        socket crash: https://github.com/python/cpython/issues/82961
        """
        if sys.version_info >= (3, 10):
            return super().close()

        self.acquire()
        try:
            if sock := getattr(self, "socket", None):
                self.socket = None
                sock.close()
            stdlib_logging.Handler.close(self)
        finally:
            self.release()


DEFAULT_SYSLOG_PORTS = {
    "UDP": 514,
    "TCP": 601,
    "TCP_TLS": 6514,
}


def configure_syslog_logger(config: Mapping) -> bool:
    """
    Configures the syslog logger with AgentConfig. This function can be called
    multiple times to reconfigure the logger with new configurations. The
    return value indicates whether the logger was reconfigured.

    The syslog logger uses the standard logging module to send messages to an
    adapted SysLogHandler.
    """
    if not config.get("protect.enable") or not config.get(
        "agent.security_logger.syslog.enable"
    ):
        return close_syslog_logger()

    outcome_to_severity: dict[str, str] = {
        "blocked": SecureSysLogHandler.severity(
            config.get("agent.security_logger.syslog.severity_blocked")
        ),
        "exploited": SecureSysLogHandler.severity(
            config.get("agent.security_logger.syslog.severity_exploited")
        ),
        "ineffective": SecureSysLogHandler.severity(
            config.get("agent.security_logger.syslog.severity_probed")
        ),
        "blocked_perimeter": SecureSysLogHandler.severity(
            config.get("agent.security_logger.syslog.severity_blocked_perimeter")
        ),
        "suspicious": SecureSysLogHandler.severity(
            config.get("agent.security_logger.syslog.severity_suspicious")
        ),
    }
    new_handler_config = _syslog_handler_config(config)

    logger, changed = _configure_syslog_std_logger(new_handler_config)
    module.syslog_logger = SysLogger(logger, outcome_to_severity)
    return changed


def _configure_syslog_std_logger(config) -> tuple[stdlib_logging.Logger, bool]:
    agent_logger = structlog.getLogger(LOGGER_NAME)

    logger = (
        module.syslog_logger.logger
        if module.syslog_logger
        else stdlib_logging.getLogger("contrast-syslog-logger")
    )
    previous_handler = None
    if (
        logger.handlers
        and (handler := logger.handlers[0])
        and isinstance(handler, SecureSysLogHandler)
    ):
        if handler.config == {"args": tuple(), "kwargs": config}:
            # The configuration hasn't changed. Continue to use the existing
            # handler.
            agent_logger.debug("Syslog logger configuration unchanged", config=config)
            return logger, False

        # previous_handler will be closed and removed after the new handler
        # is added. This ordering prevents dropping messages.
        #
        # A message could be written to both the previous_handler and the
        # latest handler. This is arguably duplication, but we can counter
        # by calling it redundancy, and this implementation side-steps the
        # need for additional locking or other synchronization.
        #
        # We could be finer grained in the condition above so that we keep
        # the existing connection in the address hasn't changed, but syslog
        # configurations from TeamServer don't happen frequently (at most once
        # per server settings polling period), so we'll keep it simple.
        previous_handler = handler

    try:
        handler = SecureSysLogHandler(**config)
    except OSError as e:
        agent_logger.error(
            "Failed to connect to syslog server",
            error=str(e),
            config=config,
        )
        return logger, False

    handler.setFormatter(CEFFormatter())

    logger.addHandler(handler)
    if previous_handler:
        previous_handler.close()
        logger.removeHandler(previous_handler)

    agent_logger.info("Syslog logger configuration updated", config=config)
    return logger, True


def _syslog_handler_config(config: Mapping) -> dict[str, Any]:
    protocol = SecureSysLogHandler.protocol(
        config.get("agent.security_logger.syslog.protocol")
    )
    host = config.get("agent.security_logger.syslog.server_host")
    if not host:
        # ip is deprecated in favor of server_host
        # In the future, it would be nice if the deprecated config
        # could be encapsulated within the get method.
        host = config.get("agent.security_logger.syslog.ip")
    port = config.get("agent.security_logger.syslog.port") or DEFAULT_SYSLOG_PORTS.get(
        protocol
    )
    facility = config.get("agent.security_logger.syslog.facility")
    socket_type = socket.SOCK_DGRAM if protocol == "UDP" else socket.SOCK_STREAM
    return {
        "address": (host, port),
        "facility": facility,
        "socktype": socket_type,
        "secure": protocol == "TCP_TLS",
    }


def close_syslog_logger():
    """
    Closes the syslog logger if it is currently enabled.

    Returns False if the logger is already disabled.
    """
    syslogger = module.syslog_logger
    if not syslogger:
        return False
    module.syslog_logger = None
    handlers = syslogger.logger.handlers
    for handler in handlers:
        handler.close()
    handlers.clear()
    return True


def _logger_path(
    config: AgentConfig,
) -> tuple[ConfigOption | None, TextIO | str]:
    if (option := config.get_option(CONFIG_KEY_STDOUT)) and option.value():
        path = sys.stdout
    elif (option := config.get_option(CONFIG_KEY_STDERR)) and option.value():
        path = sys.stderr
    elif (option := config.get_option(CONFIG_KEY_LOGGER_PATH)) and option.value():
        path = option.value()
    else:
        path = DEFAULT_AGENT_LOGGER_PATH
    return option, path


def _cache_logger(
    path_config_option: ConfigOption | None,
    level_config_option: ConfigOption | None,
) -> bool:
    return bool(
        path_config_option
        and level_config_option
        and path_config_option.is_definitely_static()
        and level_config_option.is_definitely_static()
    )


def _get_handler(path):
    if path == STDOUT:
        handler = stdlib_logging.StreamHandler(sys.stdout)
    elif path == STDERR:
        handler = stdlib_logging.StreamHandler(sys.stderr)
    else:
        try:
            if dirname := os.path.dirname(path):
                os.makedirs(dirname, exist_ok=True)
            handler = stdlib_logging.FileHandler(path)
        except Exception as e:
            sys.stderr.write(f"{str(e)}\n")
            # path could be '' or None
            handler = stdlib_logging.StreamHandler()

    return handler


def _set_level(logger, level: str) -> None:
    if level.upper() == "TRACE":
        level = "DEBUG"
        sys.stderr.write(
            "Contrast Python Agent: TRACE logging is equivalent to DEBUG\n"
        )
    try:
        logger.setLevel(level)
    except ValueError:
        # this fails validation if the level is an invalid value
        logger.setLevel(DEFAULT_LOG_LEVEL)
