from typing import Optional, List

class NoCache:
    """Noop cache implementation — for tests or services that don't need caching."""

    async def get(self, key: str) -> Optional[str]:
        return None

    async def set(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        pass

    async def delete(self, key: str) -> None:
        pass

    async def delete_many(self, keys: List[str]) -> None:
        pass

    async def get_many(self, keys: List[str]) -> List[Optional[str]]:
        return [None] * len(keys)

    async def flush_all(self) -> None:
        pass
