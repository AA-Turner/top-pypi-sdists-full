"""This module implements file path aggregates."""
import os
from abc import abstractmethod
from pathlib import Path

__all__ = [
    "VacateFilePathInterface",
    "DeployFilePathInterface",
    "SimpleVacateFilePath",
    "SimpleDeployFilePath",
    "RelativeVacateFilePath",
    "RelativeDeployFilePath",
    "YamlConfigFilePathBuilder",
]


class VacateFilePathInterface:
    """This interface defines properties"""

    @property
    @abstractmethod
    def target(self) -> Path:
        """This property return path to target file"""

    @property
    @abstractmethod
    def backup(self) -> Path:
        """This property return path to backup file"""


class DeployFilePathInterface(VacateFilePathInterface):
    """This interface defines properties"""

    @property
    @abstractmethod
    def resource(self) -> Path:
        """This property return path to resource file"""


class SimpleVacateFilePath(VacateFilePathInterface):
    """This class implements simple paths for vacate."""

    def __init__(self, target: Path, backup: Path):
        self._target = target
        self._backup = backup

    @property
    def target(self) -> Path:
        return self._target

    @property
    def backup(self) -> Path:
        return self._backup


class SimpleDeployFilePath(SimpleVacateFilePath, DeployFilePathInterface):
    """This class implements simple paths for deploy."""

    def __init__(self, target: Path, backup: Path, resource: Path):
        super().__init__(target, backup)
        self._resource = resource

    @property
    def resource(self) -> Path:
        return self._resource


class RelativeVacateFilePath(SimpleVacateFilePath):
    """This class implements relative paths for vacate."""

    def __init__(self, target: Path, backup: Path, base: Path = Path(os.getcwd())):
        super().__init__(target, backup)
        self._base = base

    @property
    def target(self) -> Path:
        return self._base / self._target

    @property
    def backup(self) -> Path:
        return self._base / self._backup


class RelativeDeployFilePath(SimpleDeployFilePath, RelativeVacateFilePath):
    """This class implements relative paths for deploy."""

    def __init__(self, target: Path, backup: Path, resource: Path, base: Path = Path(os.getcwd())):
        super().__init__(target, backup, resource)
        self._base = base

    @property
    def resource(self) -> Path:
        return self._base / self._resource


class YamlConfigFilePathBuilder(DeployFilePathInterface):
    """
    This class builds file path for config file.
    Default value is maybe suitable for standard directory structure of python project.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        path_target_directory: Path = Path(os.getcwd()),
        path_test_directory: Path = Path("tests"),
        file_target: Path = Path("config.yml"),
        file_backup: Path = Path("config.yml.bak"),
        file_resource: Path = Path("config.yml.dist"),
    ):
        self.path_target_directory = path_target_directory
        self.path_test_directory = path_test_directory
        self.file_target = file_target
        self.file_backup = file_backup
        self.file_resource = file_resource

    @property
    def target(self) -> Path:
        return self.path_target_directory / self.file_target

    @property
    def backup(self) -> Path:
        return self.path_target_directory / self.file_backup

    @property
    def resource(self) -> Path:
        return self.path_resource_directory / self.file_resource

    @property
    def path_resource_directory(self) -> Path:
        """This property returns calculated path for resource directory."""
        return self.path_target_directory / self.path_test_directory
