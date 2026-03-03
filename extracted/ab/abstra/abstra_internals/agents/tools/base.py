from abc import ABC, abstractmethod


class AgentTools(ABC):
    @abstractmethod
    def __tools__(self) -> list[str]:
        raise NotImplementedError("You must implement the __tools__ method")
