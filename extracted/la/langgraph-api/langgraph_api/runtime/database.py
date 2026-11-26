from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any


class CoreApiConnectionProto:
    """No-op connection for operations persisted through Go core."""

    @asynccontextmanager
    async def pipeline(self):
        yield None

    @asynccontextmanager
    async def transaction(self):
        yield None


@asynccontextmanager
async def connect(
    *, supports_core_api: bool = True, __test__: bool = False
) -> AsyncIterator[Any]:
    yield CoreApiConnectionProto()


async def start_pool() -> None:
    pass


async def stop_pool() -> None:
    pass


async def healthcheck(*, check_db: bool = True) -> None:
    pass


def pool_stats(*args: Any, **kwargs: Any) -> dict[str, dict[str, int]]:
    return {}
