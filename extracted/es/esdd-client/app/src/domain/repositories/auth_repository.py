from abc import ABC, abstractmethod


class AuthRepository(ABC):
    @abstractmethod
    def generate_auth_url(self, *args, **kwargs) -> str:
        """Generate authentication URL"""
        pass
