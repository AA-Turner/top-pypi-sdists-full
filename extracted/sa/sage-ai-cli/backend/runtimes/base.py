from abc import ABC, abstractmethod

from ..schemas import ChatMessage


class RuntimeAdapter(ABC):
    @abstractmethod
    def load(self, model_path: str, threads: int | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def chat(
        self,
        messages: list[ChatMessage],
        temperature: float,
        max_tokens: int,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def stream_chat(
        self,
        messages: list[ChatMessage],
        temperature: float,
        max_tokens: int,
    ):
        raise NotImplementedError
