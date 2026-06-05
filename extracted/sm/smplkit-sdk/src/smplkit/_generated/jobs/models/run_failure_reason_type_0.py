from typing import Literal, cast

RunFailureReasonType0 = Literal[
    "CONNECTION_ERROR", "NON_SUCCESS_STATUS", "QUOTA_EXCEEDED", "SSRF_BLOCKED", "TIMEOUT", "WORKER_LOST"
]

RUN_FAILURE_REASON_TYPE_0_VALUES: set[RunFailureReasonType0] = {
    "CONNECTION_ERROR",
    "NON_SUCCESS_STATUS",
    "QUOTA_EXCEEDED",
    "SSRF_BLOCKED",
    "TIMEOUT",
    "WORKER_LOST",
}


def check_run_failure_reason_type_0(value: str) -> RunFailureReasonType0:
    if value in RUN_FAILURE_REASON_TYPE_0_VALUES:
        return cast(RunFailureReasonType0, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {RUN_FAILURE_REASON_TYPE_0_VALUES!r}")
