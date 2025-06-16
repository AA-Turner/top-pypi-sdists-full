"""This module implements fixture file handler."""
import os
import shutil
from abc import abstractmethod
from typing import Generic, TypeVar

from fixturefilehandler.exceptions import BackupAlreadyExistError
from fixturefilehandler.file_paths import DeployFilePathInterface, VacateFilePathInterface

__all__ = [
    "FixtureFileHandler",
    "TVacateFilePathInterface",
    "HandlerInterface",
    "TargetFilePathVacator",
    "ResourceFileDeployer",
]


class FixtureFileHandler:
    """This class implements basic static methods."""

    @staticmethod
    def vacate_target_if_exist(file_path: VacateFilePathInterface) -> None:
        """
        This method vacate target file if target file exist.
        :return: None
        """
        if file_path.backup.exists():
            raise BackupAlreadyExistError()
        if file_path.target.is_file() or file_path.target.is_dir():
            os.replace(str(file_path.target), str(file_path.backup))

    @staticmethod
    def deploy_resource(file_path: DeployFilePathInterface) -> None:
        """
        This method vacate target file if target file exist.
        :return: None
        """
        FixtureFileHandler.vacate_target_if_exist(file_path)
        if file_path.resource.is_dir():
            shutil.copytree(str(file_path.resource), str(file_path.target))
            return
        shutil.copy(str(file_path.resource), str(file_path.target))

    @staticmethod
    def restore_backup_if_exist(file_path: VacateFilePathInterface) -> None:
        """
        This method restore backup file by if exist.
        :return: None
        """
        if file_path.backup.is_file() or file_path.backup.is_dir():
            if file_path.target.is_dir():
                shutil.rmtree(str(file_path.target))
            os.replace(str(file_path.backup), str(file_path.target))


TVacateFilePathInterface = TypeVar("TVacateFilePathInterface", bound=VacateFilePathInterface)


class HandlerInterface(Generic[TVacateFilePathInterface]):
    """This class implements interface of handler."""

    FILE_PATH: TVacateFilePathInterface

    @classmethod
    @abstractmethod
    def setup(cls, file_path: TVacateFilePathInterface = None) -> None:
        """This function setup."""

    @classmethod
    def teardown(cls, file_path: TVacateFilePathInterface = None) -> None:
        """This function restore backup if exist."""
        if file_path is None:
            file_path = cls.FILE_PATH
        FixtureFileHandler.restore_backup_if_exist(file_path)


class TargetFilePathVacator(HandlerInterface):
    """This class Vacate target file path."""

    FILE_PATH: VacateFilePathInterface

    @classmethod
    def setup(cls, file_path: VacateFilePathInterface = None) -> None:
        """This function vacate target if exist."""
        if file_path is None:
            file_path = cls.FILE_PATH
        FixtureFileHandler.vacate_target_if_exist(file_path)


class ResourceFileDeployer(HandlerInterface):
    """This class Deploy resource file into target file path."""

    FILE_PATH: DeployFilePathInterface

    @classmethod
    def setup(cls, file_path: DeployFilePathInterface = None) -> None:
        """
        This method replace config file by file_path.resource.
        If file already exists, process backs up existing file.
        :return: No return
        """
        if file_path is None:
            file_path = cls.FILE_PATH
        FixtureFileHandler.deploy_resource(file_path)
