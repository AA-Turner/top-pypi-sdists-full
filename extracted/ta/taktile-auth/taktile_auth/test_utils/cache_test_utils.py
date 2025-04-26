import typing as t


class MemoryCache:
    """Only for testing purposes"""

    def __init__(self) -> None:
        self._cache: t.Dict[str, str] = {}

    def get(self, key: str) -> t.Optional[str]:
        return self._cache.get(key)

    def put(
        self, key: str, value: str, time_to_live: t.Optional[int] = None
    ) -> None:
        del time_to_live
        self._cache[key] = value

    def delete(self, key: str) -> None:
        if key in self._cache:
            del self._cache[key]
