import logging
from collections.abc import Callable

import tenacity
from ClusterShell.RangeSet import RangeSet

from fitrequest.errors import HTTPStatusError

logger = logging.getLogger(__name__)


def retry(max_retries: int, on_status: str) -> Callable:
    """
    A decorator to simplify adding retry logic to functions using Tenacity.

    Args:

        - ``max_retries (int)``: Maximum number of retry attempts.
        - ``on_status (str)``: HTTP status code range triggering retries, in RangeSet syntax.
            See: `RangeSet documentation
            <https://clustershell.readthedocs.io/en/v1.9.1/api/RangeSet.html#ClusterShell.RangeSet.RangeSet>`_

    The decorator uses the ``wait_exponential_jitter`` strategy for retries,
    which combines exponential backoff and jitter for efficient retry timing.
    See: `tenacity documentation
    <https://tenacity.readthedocs.io/en/latest/api.html?#tenacity.wait.wait_exponential_jitter>`_

    Example:

    .. code-block:: python

        @retry(max_retries: int = 10, on_status = '503,507,512-600')
        def get_item(item_id:int) -> dict:
            ...

    """
    return tenacity.retry(
        wait=tenacity.wait_exponential_jitter(initial=1, exp_base=2, jitter=1),
        before_sleep=tenacity.before_sleep_log(logger=logger, log_level=logging.WARNING),
        retry=tenacity.retry_if_exception(
            lambda err: isinstance(err, HTTPStatusError) and err.status_code in RangeSet(on_status),
        ),
        stop=tenacity.stop.stop_after_attempt(max_attempt_number=max_retries),
    )
