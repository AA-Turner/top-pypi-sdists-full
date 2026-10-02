"""@testmu_appium.test — marks and announces the test body.

It announces the test (`begin_test`) and NOTHING ELSE. `run()` is the sole verdict
emitter: it emits exactly one pass_test/fail_test on every path, including the
fail-continue one, where a body returns cleanly with failures recorded.
"""
import functools
from typing import Callable

from testmu_appium._reporter import reporter


def test(fn: Callable) -> Callable:
    """Mark a function as the test entrypoint."""

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        reporter().begin_test(fn.__name__)
        return fn(*args, **kwargs)

    wrapper._testmu_test = True
    return wrapper
