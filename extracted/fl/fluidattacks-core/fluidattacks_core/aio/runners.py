from collections.abc import Coroutine
from typing import Any, TypeVar

import uvloop

T = TypeVar("T")


def run(coroutine: Coroutine[Any, Any, T]) -> T:
    """Run a coroutine and return the result, using uvloop."""
    return uvloop.run(coroutine)
