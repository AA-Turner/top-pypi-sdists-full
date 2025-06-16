"""This module implements aggregate object about file paths for vacate or deploy fixture for unit testing."""
import os
from pathlib import Path


class VacateFilePathBuilderForTest:
    """This class builds file path for vacate specific target file path."""

    def __init__(self, target: Path, backup: Path, backup_for_test: Path, base: Path = Path(os.getcwd())):
        self._target: Path = target
        self._backup: Path = backup
        self._backup_for_test: Path = backup_for_test
        self._base: Path = base

    @property
    def target(self) -> Path:
        """This property return path to target file."""
        return self._base / self._target

    @property
    def backup(self) -> Path:
        """This property return path to backup file which production code back up."""
        return self._base / self._backup

    @property
    def backup_for_test(self) -> Path:
        """This property return path to backup file which unit testing code back up."""
        return self._base / self._backup_for_test


class DeployFilePathBuilderForTest(VacateFilePathBuilderForTest):
    """This class builds file path for deploy specific resource file into specific target file path."""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        target: Path,
        backup: Path,
        backup_for_test: Path,
        resource: Path,
        base: Path = Path(os.getcwd()),
        base_resource: Path = Path(os.getcwd()) / "tests",
    ):
        super().__init__(target, backup, backup_for_test, base)
        self._resource = resource
        self._base_resource = base_resource

    @property
    def resource(self) -> Path:
        """This method return path to resource file"""
        return self._base_resource / self._resource
