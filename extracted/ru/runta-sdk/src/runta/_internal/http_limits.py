"""HTTP connection budgets shared by synchronous and asynchronous clients."""

import httpx


def connection_limits(pool_size: int | None) -> httpx.Limits:
    if pool_size is not None and (type(pool_size) is not int or pool_size <= 0):
        raise ValueError("connection_pool_maxsize must be a positive integer or None")
    return httpx.Limits(
        max_connections=pool_size,
        max_keepalive_connections=None,
        keepalive_expiry=30.0,
    )
