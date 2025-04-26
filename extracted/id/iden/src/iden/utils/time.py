r"""Contain utility functions to measure time."""

from __future__ import annotations

__all__ = ["sync_perf_counter", "timeblock"]

import logging
import time
from contextlib import contextmanager
from typing import TYPE_CHECKING
from unittest.mock import Mock

from coola.utils import is_torch_available

from iden.utils.format import human_time

if is_torch_available():
    import torch
else:  # pragma: no cover
    torch = Mock()


if TYPE_CHECKING:
    from collections.abc import Generator


logger = logging.getLogger(__name__)


def sync_perf_counter() -> float:
    r"""Extension of ``time.perf_counter`` that waits for all kernels in
    all streams on a CUDA device to complete.

    Returns:
        Same as ``time.perf_counter()``.
            See https://docs.python.org/3/library/time.html#time.perf_counter
            for more information.

    Example usage:

    ```pycon

    >>> from iden.utils.time import sync_perf_counter
    >>> tic = sync_perf_counter()
    >>> x = [1, 2, 3]
    >>> toc = sync_perf_counter()
    >>> toc - tic

    ```
    """
    if is_torch_available() and torch.cuda.is_available():
        torch.cuda.synchronize()
    return time.perf_counter()


@contextmanager
def timeblock(message: str = "Total time: {time}") -> Generator[None]:
    r"""Implement a context manager to measure the execution time of a
    block of code.

    Args:
        message: The message displayed when the time is logged.

    Example usage:

    ```pycon

    >>> from iden.utils.time import timeblock
    >>> with timeblock():
    ...     x = [1, 2, 3]
    ...
    >>> with timeblock("Training: {time}"):
    ...     y = [1, 2, 3]
    ...

    ```
    """
    if "{time}" not in message:
        msg = f"{{time}} is missing in the message (received: {message})"
        raise RuntimeError(msg)
    start_time = sync_perf_counter()
    try:
        yield
    finally:
        logger.info(message.format(time=human_time(sync_perf_counter() - start_time)))
