from typing import Any
from abc import ABC, abstractmethod
from navconfig import DEBUG
from navconfig.logging import logging
from ..exceptions import StoreError


class AbstractStore(ABC):
    """Abstract class for File Store."""

    def __init__(self, *args, **kwargs) -> None:
        self._name = self.__class__.__name__
        self._program: Any = kwargs.pop("program", None)
        self.logger = logging.getLogger(f"FlowTask.Files.{self._name}")
        if DEBUG is True:
            self.logger.notice(f":: Starting Store {self._name}")
        self.kwargs = kwargs
        self.args = args

    def set_program(self, program: str) -> None:
        self._program = program

    @abstractmethod
    def default_directory(self, directory: str):
        pass

    @abstractmethod
    def get_directory(self, directory: str):
        pass
