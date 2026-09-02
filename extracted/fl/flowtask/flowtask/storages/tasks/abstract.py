from typing import Any
from pathlib import PurePath
from abc import ABC, abstractmethod
from navconfig.logging import logging


class AbstractTaskStorage(ABC):
    """
    Abstract Base class for all Task Storages.
    """
    _name_: str = "TaskStorage"

    def __init__(self, *args, **kwargs) -> None:
        self.path: PurePath = None
        self.logger = logging.getLogger(
            f"FlowTask.Storage.Task.{self._name_}"
        )

    def get_path(self) -> PurePath:
        return self.path

    @abstractmethod
    async def open_task(self, task: str, program: str = None, **kwargs) -> Any:
        """open_task.
        Open A Task from Task Storage, support JSON, YAML and TOML formats.
        """
