"""This module implements """
from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Generic, Type

from fixturefilehandler import DeployFilePathInterface, VacateFilePathInterface
from tests.testlibraries.parametrizer import TypeVarVacateFilePathInterface
from tests.testlibraries.parametrizer.file_path_state_handlers import (
    ContentBackupHandler,
    ContentExistingHandler,
    ContentResourceHandler,
    FilePathStateHandler,
    NoExistHandler,
)


class FilePathState(Enum):
    """This class implements kinds of file state."""

    NOT_EXIST: Type[FilePathStateHandler] = NoExistHandler
    EXISTING: Type[FilePathStateHandler] = ContentExistingHandler
    BACKUP: Type[FilePathStateHandler] = ContentBackupHandler
    RESOURCE: Type[FilePathStateHandler] = ContentResourceHandler

    def assert_file_state(self, path):
        """This method checks file state."""
        self.value.assert_file_state(path)

    def assert_directory_state(self, path):
        """This method checks file state."""
        self.value.assert_directory_state(path)

    def create_file(self, path):
        """This method creates file."""
        self.value.create_file(path)

    def create_directory(self, path):
        """This method creates file."""
        self.value.create_directory(path)

    @property
    def value(self) -> Type[FilePathStateHandler]:
        return super().value


class MultipleFilePathState(Generic[TypeVarVacateFilePathInterface]):
    """This class implements abstract multiple file state."""

    @abstractmethod
    def assert_file_state(self, file_path: TypeVarVacateFilePathInterface):
        """This method checks file state."""

    @abstractmethod
    def assert_directory_state(self, file_path: TypeVarVacateFilePathInterface):
        """This method checks file state."""


@dataclass
class TwoFilePathState(MultipleFilePathState):
    """This class implements states of two files."""

    expect_target: FilePathState
    expect_backup: FilePathState

    def assert_file_state(self, file_path: VacateFilePathInterface):
        self.expect_target.assert_file_state(file_path.target)
        self.expect_backup.assert_file_state(file_path.backup)

    def assert_directory_state(self, file_path: VacateFilePathInterface):
        self.expect_target.assert_directory_state(file_path.target)
        self.expect_backup.assert_directory_state(file_path.backup)


@dataclass
class ThreeFilePathState(MultipleFilePathState):
    """This class implements states of three files."""

    expect_target: FilePathState
    expect_backup: FilePathState
    expect_resource: FilePathState

    def assert_file_state(self, file_path: DeployFilePathInterface):
        self.expect_target.assert_file_state(file_path.target)
        self.expect_backup.assert_file_state(file_path.backup)
        self.expect_resource.assert_file_state(file_path.resource)

    def assert_directory_state(self, file_path: DeployFilePathInterface):
        self.expect_target.assert_directory_state(file_path.target)
        self.expect_backup.assert_directory_state(file_path.backup)
        self.expect_resource.assert_directory_state(file_path.resource)
