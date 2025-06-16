"""This module implements factory for file path with file."""
from abc import abstractmethod
from pathlib import Path
from typing import Generic, Type, TypeVar

from fixturefilehandler.file_paths import RelativeDeployFilePath, RelativeVacateFilePath
from tests.testlibraries.parametrizer.file_states import MultipleFilePathState, ThreeFilePathState, TwoFilePathState

PATH_TARGET = Path("test.txt")
PATH_BACKUP = Path("test.txt.bak")
PATH_RESOURCE = Path("test.txt.dist")
TypeVarTwoFilesState = TypeVar("TypeVarTwoFilesState", bound=TwoFilePathState)


class AbstractFilePathWithResourceFactory(Generic[TypeVarTwoFilesState]):
    """This class implements abstract factory."""

    @staticmethod
    @abstractmethod
    def create(tmp_path, file_state: TypeVarTwoFilesState):
        """This class creates files and returns file path"""


class VacateFilePathWithFileFactory(AbstractFilePathWithResourceFactory):
    """This class implements factory for vacate file path."""

    @staticmethod
    def create(tmp_path, file_state: TwoFilePathState):
        file_path = RelativeVacateFilePath(PATH_TARGET, PATH_BACKUP, tmp_path)
        file_state.expect_target.create_file(file_path)
        file_state.expect_backup.create_file(file_path)
        return file_path


class DeployFilePathWithFileFactory(AbstractFilePathWithResourceFactory):
    """This class implements factory for deploy file path."""

    @staticmethod
    def create(tmp_path, file_state: ThreeFilePathState):
        file_path = RelativeDeployFilePath(PATH_TARGET, PATH_BACKUP, PATH_RESOURCE, tmp_path)
        file_state.expect_target.create_file(file_path)
        file_state.expect_backup.create_file(file_path)
        file_state.expect_resource.create_file(file_path)
        return file_path


class VacateFilePathWithDirectoryFactory(AbstractFilePathWithResourceFactory):
    """This class implements factory for vacate file path."""

    @staticmethod
    def create(tmp_path, file_state: TwoFilePathState):
        file_path = RelativeVacateFilePath(PATH_TARGET, PATH_BACKUP, tmp_path)
        file_state.expect_target.create_directory(file_path)
        file_state.expect_backup.create_directory(file_path)
        return file_path


class DeployFilePathWithDirectoryFactory(AbstractFilePathWithResourceFactory):
    """This class implements factory for deploy file path."""

    @staticmethod
    def create(tmp_path, file_state: ThreeFilePathState):
        file_path = RelativeDeployFilePath(PATH_TARGET, PATH_BACKUP, PATH_RESOURCE, tmp_path)
        file_state.expect_target.create_directory(file_path)
        file_state.expect_backup.create_directory(file_path)
        file_state.expect_resource.create_directory(file_path)
        return file_path


class FilePathWithFileFactory:
    """This class implements factory for file path and file."""

    @classmethod
    def create(cls, tmp_path, multi_file_state):
        """This class creates files and returns file path"""
        factory = cls._create(multi_file_state)
        return factory.create(tmp_path, multi_file_state)

    @classmethod
    def _create(cls, multi_file_state: MultipleFilePathState) -> Type[AbstractFilePathWithResourceFactory]:
        if isinstance(multi_file_state, TwoFilePathState):
            return VacateFilePathWithFileFactory
        if isinstance(multi_file_state, ThreeFilePathState):
            return DeployFilePathWithFileFactory
        raise ValueError()


class FilePathWithDirectoryFactory:
    """This class implements factory for file path and file."""

    @classmethod
    def create(cls, tmp_path, multi_file_state):
        """This class creates files and returns file path"""
        factory = cls._create(multi_file_state)
        return factory.create(tmp_path, multi_file_state)

    @classmethod
    def _create(cls, multi_file_state: MultipleFilePathState) -> Type[AbstractFilePathWithResourceFactory]:
        if isinstance(multi_file_state, TwoFilePathState):
            return VacateFilePathWithDirectoryFactory
        if isinstance(multi_file_state, ThreeFilePathState):
            return DeployFilePathWithDirectoryFactory
        raise ValueError()
