from __future__ import annotations

import random
import re
import time
from collections.abc import Callable
from typing import TypeVar

_T = TypeVar("_T")


def retry_call(
    fn: Callable[[], _T],
    *,
    attempts: int,
    retry_if: Callable[[Exception], bool] | None = None,
    wait: Callable[[int], float] | float = 0,
    after_failure: Callable[[int, Exception], None] | None = None,
) -> _T:
    if attempts < 1:
        raise ValueError("attempts must be at least 1")

    for attempt_number in range(1, attempts + 1):
        try:
            return fn()
        except Exception as exc:
            should_retry = retry_if(exc) if retry_if is not None else True
            if after_failure is not None:
                after_failure(attempt_number, exc)
            if attempt_number == attempts or not should_retry:
                raise

            sleep_seconds = wait(attempt_number) if callable(wait) else wait
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)

    raise AssertionError("unreachable")


def retry_if_exception_message(pattern: str) -> Callable[[Exception], bool]:
    compiled = re.compile(pattern)

    def matches(exc: Exception) -> bool:
        return compiled.search(str(exc)) is not None

    return matches


def wait_exponential_jitter(
    *,
    initial: float = 1,
    max_seconds: float = 60,
    exp_base: float = 2,
    jitter: float = 1,
) -> Callable[[int], float]:
    def wait(attempt_number: int) -> float:
        return min(initial * exp_base ** (attempt_number - 1) + random.uniform(0, jitter), max_seconds)

    return wait
