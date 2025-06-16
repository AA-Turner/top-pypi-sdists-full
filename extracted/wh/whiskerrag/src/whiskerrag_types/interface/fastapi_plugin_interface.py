import logging
from abc import ABC, abstractmethod
from typing import Callable, List, Tuple

from .settings_interface import SettingsInterface


class FastAPIPluginInterface(ABC):
    def __init__(self, settings: SettingsInterface) -> None:
        self.settings = settings
        self.logger = logging.getLogger("whisker")
        self._initialized: bool = False

    @abstractmethod
    def get_extra_middleware_list(self) -> List[Tuple[Callable, dict]]:
        pass
