import asyncio
import contextlib
from typing import Callable

import pytest

from zapros._errors import ConnectTimeoutError, ReadTimeoutError, WriteTimeoutError
from zapros._handlers._exc_map import (
    map_asyncio_connect_exceptions,
    map_asyncio_read_exceptions,
    map_asyncio_write_exceptions,
)


@pytest.mark.parametrize(
    ("mapper", "expected"),
    [
        (map_asyncio_connect_exceptions, ConnectTimeoutError),
        (map_asyncio_read_exceptions, ReadTimeoutError),
        (map_asyncio_write_exceptions, WriteTimeoutError),
    ],
)
def test_asyncio_timeout_error_is_mapped(
    mapper: Callable[[], contextlib.AbstractContextManager[None]],
    expected: type[Exception],
) -> None:
    # On Python 3.10 this is not the builtin TimeoutError.
    with pytest.raises(expected):
        with mapper():
            raise asyncio.TimeoutError
