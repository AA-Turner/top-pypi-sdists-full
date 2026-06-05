from typing import Literal, cast

RunStatus = Literal["CANCELED", "FAILED", "PENDING", "RUNNING", "SUCCEEDED"]

RUN_STATUS_VALUES: set[RunStatus] = {
    "CANCELED",
    "FAILED",
    "PENDING",
    "RUNNING",
    "SUCCEEDED",
}


def check_run_status(value: str) -> RunStatus:
    if value in RUN_STATUS_VALUES:
        return cast(RunStatus, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {RUN_STATUS_VALUES!r}")
