"""@testmu_selenium.test — decorator wrapping a test function with lifecycle reporting."""
import functools
import logging
from typing import Callable

from testmu_selenium._step import get_step_count

logger = logging.getLogger(__name__)


def test(fn: Callable) -> Callable:
    """Decorator marking a function as the test entrypoint.

    Lifecycle log format mirrors playwright-python/testmu/_reporter/lt.py so
    HE worker logs read the same across drivers:

        [TEST START] <name>
          [STEP 1] <description>
          [STEP 2] <description>
        [TEST PASS] (N steps)
    """
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        logger.info("[TEST START] %s", fn.__name__)
        try:
            result = fn(*args, **kwargs)
            logger.info("[TEST PASS] (%d steps)", get_step_count())
            return result
        except Exception as e:
            logger.error("[TEST FAIL] at step %d — %s", get_step_count(), e)
            raise
    wrapper._testmu_test = True
    return wrapper
