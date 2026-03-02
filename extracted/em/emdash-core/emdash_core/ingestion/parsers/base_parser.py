"""Abstract base class for language-specific parsers."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional

from ...core.models import FileEntities


class BaseLanguageParser(ABC):
    """Abstract base class for language-specific parsers."""

    def __init__(self, file_path: Path, repo_root: Optional[Path] = None):
        """Initialize parser.

        Args:
            file_path: Path to source file
            repo_root: Root directory of repository (for module name calculation)
        """
        self.file_path = file_path
        self.repo_root = repo_root or file_path.parent
        self.module_name = self._calculate_module_name()

    @abstractmethod
    def parse(self) -> FileEntities:
        """Parse file and extract code entities.

        Returns:
            FileEntities containing classes, functions, imports, etc.
        """
        pass

    @classmethod
    @abstractmethod
    def get_supported_extensions(cls) -> List[str]:
        """Return list of file extensions this parser handles.

        Returns:
            List of file extensions (e.g., ['.py'] or ['.ts', '.tsx', '.js', '.jsx'])
        """
        pass

    def _calculate_module_name(self) -> str:
        """Calculate module name from file path (language-agnostic logic).

        Returns:
            Module name like "src.module.submodule"
        """
        try:
            # Get relative path from repo root
            relative_path = self.file_path.relative_to(self.repo_root)

            # Convert path to module name
            parts = list(relative_path.parts[:-1])  # Exclude filename
            filename = relative_path.stem  # Get filename without extension

            # Skip index files (index.ts, __init__.py)
            if filename not in ["__init__", "index"]:
                parts.append(filename)

            module_name = ".".join(parts) if parts else filename
            return module_name

        except ValueError:
            # File is outside repo root
            return self.file_path.stem
