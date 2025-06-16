"""This module implements executer for test target method."""
from abc import abstractmethod
from enum import Enum
from typing import Generic, Type

import pytest

from fixturefilehandler import (
    BackupAlreadyExistError,
    DeployFilePathInterface,
    FixtureFileHandler,
    ResourceFileDeployer,
    TargetFilePathVacator,
    VacateFilePathInterface,
)
from tests.testlibraries.parametrizer import TypeVarVacateFilePathInterface


def create_vacator_class(file_path):
    """This function returns vacator class."""

    class Vacator(TargetFilePathVacator):
        """This class implements concrete file path."""

        FILE_PATH = file_path

    return Vacator


def create_deployer_class(file_path):
    """This function returns deployer class."""

    class Deployer(ResourceFileDeployer):
        """This class implements concrete file path."""

        FILE_PATH = file_path

    return Deployer


class ActionExecutor(Generic[TypeVarVacateFilePathInterface]):
    """This class implements abstract action executor."""

    @staticmethod
    @abstractmethod
    def execute(file_path: TypeVarVacateFilePathInterface):
        """This method execute action."""


class VacateTargetIfExistExecutor(ActionExecutor[VacateFilePathInterface]):
    """This class implements action executor for vacate_target_if_exist()."""

    @staticmethod
    def execute(file_path: VacateFilePathInterface):
        FixtureFileHandler.vacate_target_if_exist(file_path)


class VacateTargetIfExistAssertErrorExecutor(ActionExecutor[VacateFilePathInterface]):
    """This class implements action executor for vacate_target_if_exist() with argument."""

    @staticmethod
    def execute(file_path: VacateFilePathInterface):
        with pytest.raises(BackupAlreadyExistError):
            FixtureFileHandler.vacate_target_if_exist(file_path)


class DeployResourceExecutor(ActionExecutor[DeployFilePathInterface]):
    """This class implements action executor for deploy_resource()."""

    @staticmethod
    def execute(file_path: DeployFilePathInterface):
        FixtureFileHandler.deploy_resource(file_path)


class DeployResourceAssertErrorExecutor(ActionExecutor[DeployFilePathInterface]):
    """This class implements action executor for deploy_resource() with argument and expect error."""

    @staticmethod
    def execute(file_path: DeployFilePathInterface):
        with pytest.raises(FileNotFoundError):
            FixtureFileHandler.deploy_resource(file_path)


class RestoreBackupIfExistExecutor(ActionExecutor[VacateFilePathInterface]):
    """This class implements action executor for restore_backup_if_exist() with argument."""

    @staticmethod
    def execute(file_path: VacateFilePathInterface):
        FixtureFileHandler.restore_backup_if_exist(file_path)


class VacatorSetupExecutor(ActionExecutor[VacateFilePathInterface]):
    """This class implements action executor for Vacator.setup()."""

    @staticmethod
    def execute(file_path: VacateFilePathInterface):
        create_vacator_class(file_path).setup()


class VacatorSetupWithArgumentExecutor(ActionExecutor[VacateFilePathInterface]):
    """This class implements action executor for Vacator.setup() with argument."""

    @staticmethod
    def execute(file_path: VacateFilePathInterface):
        TargetFilePathVacator.setup(file_path)


class VacatorTeardownExecutor(ActionExecutor[VacateFilePathInterface]):
    """This class implements action executor for Vacator.teardown()."""

    @staticmethod
    def execute(file_path: VacateFilePathInterface):
        create_vacator_class(file_path).teardown()


class VacatorTeardownWithArgumentExecutor(ActionExecutor[VacateFilePathInterface]):
    """This class implements action executor for Vacator.teardown() with argument."""

    @staticmethod
    def execute(file_path: VacateFilePathInterface):
        TargetFilePathVacator.teardown(file_path)


class DeployerSetupExecutor(ActionExecutor[DeployFilePathInterface]):
    """This class implements action executor for Deployer.setup()."""

    @staticmethod
    def execute(file_path: DeployFilePathInterface):
        create_deployer_class(file_path).setup()


class DeployerSetupWithArgumentExecutor(ActionExecutor[DeployFilePathInterface]):
    """This class implements action executor for Deployer.setup() with argument."""

    @staticmethod
    def execute(file_path: DeployFilePathInterface):
        ResourceFileDeployer.setup(file_path)


class DeployerTeardownExecutor(ActionExecutor[DeployFilePathInterface]):
    """This class implements action executor for Deployer.teardown()."""

    @staticmethod
    def execute(file_path: DeployFilePathInterface):
        create_deployer_class(file_path).teardown()


class DeployerTeardownWithArgumentExecutor(ActionExecutor[VacateFilePathInterface]):
    """This class implements action executor for Deployer.teardown() with argument."""

    @staticmethod
    def execute(file_path: VacateFilePathInterface):
        ResourceFileDeployer.teardown(file_path)


class Action(Enum):
    """This class implements kinds of action executor."""

    VACATE_TARGET_IF_EXIST = VacateTargetIfExistExecutor
    VACATE_TARGET_IF_EXIST_ASSERT_ERROR = VacateTargetIfExistAssertErrorExecutor
    DEPLOY_RESOURCE = DeployResourceExecutor
    DEPLOY_RESOURCE_ASSERT_ERROR = DeployResourceAssertErrorExecutor
    RESTORE_BACKUP_IF_EXIST = RestoreBackupIfExistExecutor
    VACATOR_SETUP = VacatorSetupExecutor
    VACATOR_SETUP_WITH_ARGUMENT = VacatorSetupWithArgumentExecutor
    VACATOR_TEARDOWN = VacatorTeardownExecutor
    VACATOR_TEARDOWN_WITH_ARGUMENT = VacatorTeardownWithArgumentExecutor
    DEPLOYER_SETUP = DeployerSetupExecutor
    DEPLOYER_SETUP_WITH_ARGUMENT = DeployerSetupWithArgumentExecutor
    DEPLOYER_TEARDOWN = DeployerTeardownExecutor
    DEPLOYER_TEARDOWN_WITH_ARGUMENT = DeployerTeardownWithArgumentExecutor

    def execute(self, file_path: VacateFilePathInterface):
        """This method be short cut for value's method."""
        self.value.execute(file_path)  # type: ignore

    @property
    def value(self) -> Type[ActionExecutor[VacateFilePathInterface]]:
        return super().value
