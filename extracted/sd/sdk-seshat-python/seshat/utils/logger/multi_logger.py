import os
from typing import Any, Optional

from seshat.utils.logger.base_logger import BaseLogger, LogLevel, LogConfig, LogEncoding
from seshat.utils.logger.console_logger import ConsoleLogger
from seshat.utils.logger.logstash_logger import LogstashLogger
from seshat.utils.logger.cloudwatch_logger import CloudWatchLogger


class MultiLogger(BaseLogger):
    def __init__(self, loggers: list[BaseLogger], sentry_client: Optional[Any] = None):
        self.loggers = loggers
        self.sentry_client = sentry_client

    def debug(self, msg: str, **fields: Any) -> None:
        for logger in self.loggers:
            logger.debug(msg, **fields)

    def info(self, msg: str, **fields: Any) -> None:
        for logger in self.loggers:
            logger.info(msg, **fields)

    def warn(self, msg: str, **fields: Any) -> None:
        for logger in self.loggers:
            logger.warn(msg, **fields)

    def warning(self, msg: str, **fields: Any) -> None:
        self.warn(msg, **fields)

    def error(self, msg: str, **fields: Any) -> None:
        for logger in self.loggers:
            logger.error(msg, **fields)

    def fatal(self, msg: str, **fields: Any) -> None:
        for logger in self.loggers:
            logger.fatal(msg, **fields)

        if self.sentry_client:
            self.sentry_client.capture_message(msg, level="fatal", extra=fields)
            self.sentry_client.flush(timeout=2.0)

    def sync(self) -> None:
        errors = []
        for logger in self.loggers:
            try:
                logger.sync()
            except Exception as e:
                errors.append(e)

        if errors:
            raise Exception(f"Multiple sync errors occurred: {errors}")

    def set_sentry_client(self, client: Any) -> None:
        self.sentry_client = client


def get_multi_logger(sentry_client: Optional[Any] = None) -> BaseLogger:
    loggers: list[BaseLogger] = []
    log_level = LogLevel(os.getenv("LOG_LEVEL", "info").upper())
    config = LogConfig(level=log_level, format_type=LogEncoding.CONSOLE)

    if os.getenv("CONSOLE_LOGGING", "true").lower() == "true":
        loggers.append(ConsoleLogger(config))

    if os.getenv("LOGSTASH_LOGGING", "false").lower() == "true":
        loggers.append(LogstashLogger(config))

    if os.getenv("AWS_LOGGING", "false").lower() == "true":
        try:
            pipeline_name = os.getenv("HEISENBERG_JOB_NAME", "unknown")
            loggers.append(CloudWatchLogger(pipeline_name, config))
        except Exception as e:
            print(f"Failed to initialize CloudWatch logger: {e}")

    return MultiLogger(loggers, sentry_client)
