from abc import abstractmethod
from typing import Protocol


class ITimer(Protocol):
    @abstractmethod
    def cancel(self) -> None: ...

    @property
    @abstractmethod
    def daemon(self) -> bool: ...

    @daemon.setter
    @abstractmethod
    def daemon(self, __arg0: bool) -> None: ...

    @abstractmethod
    def start(self) -> None: ...
