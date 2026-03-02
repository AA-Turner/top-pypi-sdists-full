from typing import Union
from tenacity import Retrying
from tenacity import stop_after_attempt, wait_exponential

from dlt.common import logger
from dlt.common.exceptions import ValueErrorWithKnownValues
from dlt.common.validation import validate_dict

from dlthub._runner.typing import RetryPolicyConfig


def _format_number(n: Union[int, float]) -> str:
    if isinstance(n, float) and n.is_integer():
        return str(int(n))
    return str(n)


def create_retry_policy_description(retry_policy: Retrying) -> str:
    """Create a description of the retry policy"""
    try:
        parts = []

        if hasattr(retry_policy, "stop") and retry_policy.stop:
            stop_func = retry_policy.stop
            stop_type = type(stop_func).__name__
            if stop_type == "stop_after_attempt":
                max_attempts = getattr(stop_func, "max_attempt_number", None)
                if max_attempts is not None:
                    parts.append(f"{_format_number(max_attempts)} attempts")
                else:
                    parts.append("limited attempts")
            elif stop_type == "stop_after_delay":
                timeout = getattr(stop_func, "max_delay", None)
                if timeout is None:
                    timeout = getattr(stop_func, "timeout", None)
                if timeout is None:
                    timeout = getattr(stop_func, "_timeout", None)
                if timeout is not None:
                    parts.append(f"timeout after {_format_number(timeout)}s")
                else:
                    parts.append("timeout after unknown seconds")
            else:
                parts.append(f"stop: {stop_type}")

        # Analyze wait strategy
        if hasattr(retry_policy, "wait") and retry_policy.wait:
            wait_func = retry_policy.wait
            wait_type = type(wait_func).__name__
            if wait_type == "wait_exponential":
                multiplier = getattr(wait_func, "multiplier", getattr(wait_func, "_multiplier", 1))
                min_wait = getattr(wait_func, "min", getattr(wait_func, "_min", 0))
                max_wait = getattr(wait_func, "max", getattr(wait_func, "_max", float("inf")))
                parts.append(
                    f"exponential backoff (multiplier={_format_number(multiplier)}, "
                    f"min={_format_number(min_wait)}s, max={_format_number(max_wait)}s)"
                )
            elif wait_type == "wait_fixed":
                wait_time = getattr(wait_func, "wait_fixed", None)
                if wait_time is None:
                    wait_time = getattr(wait_func, "wait", getattr(wait_func, "_wait", 0))
                parts.append(f"fixed {_format_number(wait_time)}s delay")
            elif wait_type == "wait_random":
                min_wait = getattr(wait_func, "wait_random_min", None)
                max_wait = getattr(wait_func, "wait_random_max", None)
                if min_wait is None:
                    min_wait = getattr(wait_func, "min", getattr(wait_func, "_min", 0))
                if max_wait is None:
                    max_wait = getattr(wait_func, "max", getattr(wait_func, "_max", 0))
                parts.append(
                    f"random delay ({_format_number(min_wait)}s-{_format_number(max_wait)}s)"
                )
            else:
                parts.append(f"wait: {wait_type}")

        # Add reraise info
        if getattr(retry_policy, "reraise", False):
            parts.append("reraise exceptions")

        if parts:
            return ", ".join(parts)
        else:
            return "custom retry policy"
    except Exception:
        logger.warning("Failed to create retry policy description", exc_info=True)
        return "indeterminate retry policy"


def parse_retry_policy(policy_dict: RetryPolicyConfig) -> Retrying:
    validate_dict(RetryPolicyConfig, policy_dict, ".")
    if not policy_dict or policy_dict.get("type") == "none":
        retry = Retrying(stop=stop_after_attempt(1), reraise=True)
        return retry
    if policy_dict.get("type") == "backoff":
        max_attempts = policy_dict.get("max_attempts", 5)
        multiplier = policy_dict.get("multiplier", 2)
        min_wait = policy_dict.get("min", 4)
        max_wait = policy_dict.get("max", 10)
        retry = Retrying(
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(
                multiplier=multiplier,
                min=min_wait,
                max=max_wait,
            ),
            reraise=True,
        )

        return retry
    if policy_dict.get("type") == "fixed":
        max_attempts = policy_dict.get("max_attempts", 3)
        retry = Retrying(stop=stop_after_attempt(max_attempts), reraise=True)
        return retry
    raise ValueErrorWithKnownValues(
        key="type",
        value_received=policy_dict.get("type"),
        valid_values=["none", "backoff", "fixed"],
    )
