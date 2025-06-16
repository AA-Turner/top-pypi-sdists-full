"""Tests for fixturefilehandler.__init__ module."""

import pytest

from fixturefilehandler.file_paths import VacateFilePathInterface
from tests.testlibraries.parametrizer.action_executors import Action as Act
from tests.testlibraries.parametrizer.file_path_with_resource_factories import (
    FilePathWithDirectoryFactory,
    FilePathWithFileFactory,
)
from tests.testlibraries.parametrizer.file_states import FilePathState as FPS  # noqa
from tests.testlibraries.parametrizer.file_states import MultipleFilePathState
from tests.testlibraries.parametrizer.file_states import ThreeFilePathState as ThS
from tests.testlibraries.parametrizer.file_states import TwoFilePathState as TwS

# pylint: disable=line-too-long,bad-whitespace
PARAMS = [
    # TestFixtureFileHandler
    # test_vacate_target_if_exist
    (TwS(FPS.EXISTING, FPS.NOT_EXIST), Act.VACATE_TARGET_IF_EXIST, TwS(FPS.NOT_EXIST, FPS.EXISTING)),  # noqa E501
    (TwS(FPS.NOT_EXIST, FPS.NOT_EXIST), Act.VACATE_TARGET_IF_EXIST, TwS(FPS.NOT_EXIST, FPS.NOT_EXIST)),  # noqa E501
    (
        TwS(FPS.NOT_EXIST, FPS.BACKUP),
        Act.VACATE_TARGET_IF_EXIST_ASSERT_ERROR,
        TwS(FPS.NOT_EXIST, FPS.BACKUP),
    ),  # noqa E501
    # test_restore_backup_if_exist
    (TwS(FPS.EXISTING, FPS.BACKUP), Act.RESTORE_BACKUP_IF_EXIST, TwS(FPS.BACKUP, FPS.NOT_EXIST)),  # noqa E501
    (TwS(FPS.EXISTING, FPS.NOT_EXIST), Act.RESTORE_BACKUP_IF_EXIST, TwS(FPS.EXISTING, FPS.NOT_EXIST)),  # noqa E501
    # test_deploy_resource
    (
        ThS(FPS.EXISTING, FPS.NOT_EXIST, FPS.RESOURCE),
        Act.DEPLOY_RESOURCE,
        ThS(FPS.RESOURCE, FPS.EXISTING, FPS.RESOURCE),
    ),  # noqa E501
    (
        ThS(FPS.NOT_EXIST, FPS.NOT_EXIST, FPS.RESOURCE),
        Act.DEPLOY_RESOURCE,
        ThS(FPS.RESOURCE, FPS.NOT_EXIST, FPS.RESOURCE),
    ),  # noqa E501
    (
        ThS(FPS.NOT_EXIST, FPS.NOT_EXIST, FPS.NOT_EXIST),
        Act.DEPLOY_RESOURCE_ASSERT_ERROR,
        ThS(FPS.NOT_EXIST, FPS.NOT_EXIST, FPS.NOT_EXIST),
    ),  # noqa E501
    # TeFPSargetFilePathVacator
    # test_setup
    (TwS(FPS.EXISTING, FPS.NOT_EXIST), Act.VACATOR_SETUP, TwS(FPS.NOT_EXIST, FPS.EXISTING)),  # noqa E501
    (TwS(FPS.EXISTING, FPS.NOT_EXIST), Act.VACATOR_SETUP_WITH_ARGUMENT, TwS(FPS.NOT_EXIST, FPS.EXISTING)),  # noqa E501
    # test_teardown
    (TwS(FPS.EXISTING, FPS.BACKUP), Act.VACATOR_TEARDOWN, TwS(FPS.BACKUP, FPS.NOT_EXIST)),  # noqa E501
    (TwS(FPS.EXISTING, FPS.BACKUP), Act.VACATOR_TEARDOWN_WITH_ARGUMENT, TwS(FPS.BACKUP, FPS.NOT_EXIST)),  # noqa E501
    # TestResourceFileDeployer
    # test_setup
    (
        ThS(FPS.EXISTING, FPS.NOT_EXIST, FPS.RESOURCE),
        Act.DEPLOYER_SETUP,
        ThS(FPS.RESOURCE, FPS.EXISTING, FPS.RESOURCE),
    ),  # noqa E501
    (
        ThS(FPS.EXISTING, FPS.NOT_EXIST, FPS.RESOURCE),
        Act.DEPLOYER_SETUP_WITH_ARGUMENT,
        ThS(FPS.RESOURCE, FPS.EXISTING, FPS.RESOURCE),
    ),  # noqa E501
    # test_teardown (integration test)
    (
        ThS(FPS.EXISTING, FPS.BACKUP, FPS.RESOURCE),
        Act.DEPLOYER_TEARDOWN,
        ThS(FPS.BACKUP, FPS.NOT_EXIST, FPS.RESOURCE),
    ),  # noqa E501
    (
        ThS(FPS.EXISTING, FPS.NOT_EXIST, FPS.RESOURCE),
        Act.DEPLOYER_TEARDOWN,
        ThS(FPS.EXISTING, FPS.NOT_EXIST, FPS.RESOURCE),
    ),  # noqa E501
]


@pytest.fixture
def file_path_with_file(request, tmp_path):
    """
    This fixture prepares file path aggregate
    and files specified by param (TwoFilesState or ThreeFileState) on tmp_path.
    """
    yield FilePathWithFileFactory.create(tmp_path, request.param)


@pytest.fixture
def file_path_with_directory(request, tmp_path):
    """
    This fixture prepares file path aggregate
    and files specified by param (TwoFilesState or ThreeFileState) on tmp_path.
    """
    yield FilePathWithDirectoryFactory.create(tmp_path, request.param)


class TestFixtureFileHandlerModules:
    """Tests for fixturefilehandler modules."""

    @staticmethod
    @pytest.mark.parametrize("file_path_with_file, action, expect", PARAMS, indirect=["file_path_with_file"])
    # Reason: pytest fixture. pylint: disable=redefined-outer-name
    def test_file(file_path_with_file: VacateFilePathInterface, action: Act, expect: MultipleFilePathState):
        """Specific action should update state of each files to appropriate states."""
        action.execute(file_path_with_file)
        expect.assert_file_state(file_path_with_file)

    @staticmethod
    @pytest.mark.parametrize("file_path_with_directory, action, expect", PARAMS, indirect=["file_path_with_directory"])
    # Reason: pytest fixture. pylint: disable=redefined-outer-name
    def test_directory(file_path_with_directory: VacateFilePathInterface, action: Act, expect: MultipleFilePathState):
        """Specific action should update state of each files to appropriate states."""
        action.execute(file_path_with_directory)
        expect.assert_directory_state(file_path_with_directory)
