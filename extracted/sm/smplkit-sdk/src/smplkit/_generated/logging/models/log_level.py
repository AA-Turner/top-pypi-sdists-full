from typing import Literal, cast

LogLevel = Literal["DEBUG", "ERROR", "FATAL", "INFO", "SILENT", "TRACE", "WARN"]

LOG_LEVEL_VALUES: set[LogLevel] = {
    "DEBUG",
    "ERROR",
    "FATAL",
    "INFO",
    "SILENT",
    "TRACE",
    "WARN",
}


def check_log_level(value: str) -> LogLevel:
    if value in LOG_LEVEL_VALUES:
        return cast(LogLevel, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LOG_LEVEL_VALUES!r}")
