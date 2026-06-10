import typing as t


class Cache(t.Protocol):
    """Cache Protocol
    Keep this in sync with the package defined in flow_services/packages/cache
    """

    def get(
        self, key: str, *, skip_local_cache: bool = False
    ) -> t.Optional[str]:
        """Get a value. If skip_local_cache=True, bypass in-memory tier."""
        ...  # pragma: no cover

    def put(
        self, key: str, value: str, time_to_live: t.Optional[int] = None
    ) -> None:
        """Put a value"""
        ...  # pragma: no cover

    def delete(self, key: str) -> None:
        """Delete a values"""
        ...  # pragma: no cover

    def put_marker(self, key: str, ttl_seconds: int) -> bool:
        """Put a marker, return True if first to write"""
        ...  # pragma: no cover

    def increment(self, key: str, amount: int, ttl_seconds: int) -> int:
        """Atomically add ``amount`` to the counter at ``key`` and return the
        post-increment value. Sets the TTL on first write. Used by PEP-295
        recursion accounting."""
        ...  # pragma: no cover
