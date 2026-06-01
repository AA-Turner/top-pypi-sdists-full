from typing import Literal, cast

Severity = Literal["DEBUG", "ERROR", "FATAL", "INFO", "TRACE", "WARN"]

SEVERITY_VALUES: set[Severity] = {
    "DEBUG",
    "ERROR",
    "FATAL",
    "INFO",
    "TRACE",
    "WARN",
}


def check_severity(value: str) -> Severity:
    if value in SEVERITY_VALUES:
        return cast(Severity, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SEVERITY_VALUES!r}")
