from abc import ABC, abstractmethod
from collections import defaultdict
import os


class ConfigRetriever(ABC):
    @abstractmethod
    def get_config_variable(self, config_name):
        pass
