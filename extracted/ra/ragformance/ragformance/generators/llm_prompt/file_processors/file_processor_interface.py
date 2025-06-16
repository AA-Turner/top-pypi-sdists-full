from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from ragformance.models.corpus import DocModel

class FileProcessor(ABC):
    @abstractmethod
    def can_process(self, file_path: Path) -> bool:
        """Return True if this processor can handle the file."""
        pass

    @abstractmethod
    def process(self, file_path: Path) -> List[DocModel]:
        """Process the file and return a list of DocModel instances."""
        pass
