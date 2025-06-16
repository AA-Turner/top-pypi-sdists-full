"""This module implements handler factory"""
from typing import Type

from fixturefilehandler.fixture_file_handler import (
    DeployFilePathInterface,
    ResourceFileDeployer,
    TargetFilePathVacator,
    VacateFilePathInterface,
)

__all__ = ["VacatorFactory", "DeployerFactory"]


class VacatorFactory:
    """This class implements create method for Vacator."""

    @staticmethod
    def create(file_path: VacateFilePathInterface) -> Type[TargetFilePathVacator]:
        """This method returns FILE_PATH override Vacator."""

        class Vacator(TargetFilePathVacator):
            """This class Vacate target file path."""

            FILE_PATH = file_path

        return Vacator


class DeployerFactory:
    """This class implements create method for Deployer."""

    @staticmethod
    def create(file_path: DeployFilePathInterface) -> Type[ResourceFileDeployer]:
        """This method returns FILE_PATH override Deployer."""

        class Deployer(ResourceFileDeployer):
            """This class deploy resource file into target file path."""

            FILE_PATH = file_path

        return Deployer
