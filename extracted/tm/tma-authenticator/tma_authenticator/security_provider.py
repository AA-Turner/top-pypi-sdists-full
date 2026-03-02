from abc import ABC, abstractmethod


class SecurityProvider(ABC):
    @abstractmethod
    async def validate(self, access_token: str) -> bool:
        pass
