import typing as t


class Cache(t.Protocol):
    """Cache Protocol
    Keep this in sync with the package defined in flow_services/packages/cache
    """

    def get(self, key: str) -> t.Optional[str]:
        """Get a value"""

    def put(
        self, key: str, value: str, time_to_live: t.Optional[int] = None
    ) -> None:
        """Put a value"""

    def delete(self, key: str) -> None:
        """Delete a values"""
