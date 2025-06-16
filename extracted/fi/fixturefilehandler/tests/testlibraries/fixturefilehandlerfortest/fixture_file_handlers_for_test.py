"""This module implements file path aggregates for test."""
import os
import shutil
from abc import abstractmethod
from typing import Generic, TypeVar

from tests.testlibraries.fixturefilehandlerfortest.file_paths_for_test import (
    DeployFilePathBuilderForTest,
    VacateFilePathBuilderForTest,
)


class FixtureFileHandlerForTest:
    """This class implements basic static methods."""

    @staticmethod
    def vacate_target_if_exist_and_remove_backup_if_exist(file_path) -> None:
        """
        This method vacate target file if target file exist,
        and remove backup file if backup file exist.
        :return: None
        """
        if file_path.target.is_file():
            os.replace(str(file_path.target), str(file_path.backup_for_test))
        if file_path.backup.exists():
            os.unlink(str(file_path.backup))

    @staticmethod
    def deploy_resource(file_path) -> None:
        """
        This method vacate target file if target file exist.
        :return: None
        """
        FixtureFileHandlerForTest.vacate_target_if_exist_and_remove_backup_if_exist(file_path)
        shutil.copy(str(file_path.resource), str(file_path.target))

    @staticmethod
    def restore_target_if_backup_for_test_exist(file_path: VacateFilePathBuilderForTest) -> None:
        """
        This method restore backup file by if exist.
        :return: None
        """
        if not file_path.backup_for_test.is_file():
            return
        if file_path.target.is_file():
            os.unlink(str(file_path.target))
        os.replace(str(file_path.backup_for_test), str(file_path.target))


TVacateFilePathInterfaceForTest = TypeVar("TVacateFilePathInterfaceForTest", bound=VacateFilePathBuilderForTest)


class HandlerInterfaceForTest(Generic[TVacateFilePathInterfaceForTest]):
    """This class implements interface of handler."""

    FILE_PATH: TVacateFilePathInterfaceForTest

    @classmethod
    @abstractmethod
    def set_up(cls) -> None:
        """This function setup."""

    @classmethod
    def do_cleanups(cls) -> None:
        """This function restore backup if exist."""
        FixtureFileHandlerForTest.restore_target_if_backup_for_test_exist(cls.FILE_PATH)


class TargetFilePathVacatorForTest(HandlerInterfaceForTest):
    """This class vacates target file path."""

    FILE_PATH: VacateFilePathBuilderForTest

    @classmethod
    def set_up(cls) -> None:
        FixtureFileHandlerForTest.vacate_target_if_exist_and_remove_backup_if_exist(cls.FILE_PATH)


class FixtureFileDeployerForTest(HandlerInterfaceForTest):
    """This class deploys resource file into target file path."""

    FILE_PATH: DeployFilePathBuilderForTest

    @classmethod
    def set_up(cls) -> None:
        FixtureFileHandlerForTest.deploy_resource(cls.FILE_PATH)
