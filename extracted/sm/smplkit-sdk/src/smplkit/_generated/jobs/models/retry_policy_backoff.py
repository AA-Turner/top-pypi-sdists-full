from typing import Literal, cast

RetryPolicyBackoff = Literal["exponential", "fixed"]

RETRY_POLICY_BACKOFF_VALUES: set[RetryPolicyBackoff] = {
    "exponential",
    "fixed",
}


def check_retry_policy_backoff(value: str) -> RetryPolicyBackoff:
    if value in RETRY_POLICY_BACKOFF_VALUES:
        return cast(RetryPolicyBackoff, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {RETRY_POLICY_BACKOFF_VALUES!r}")
