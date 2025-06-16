"""Tests for unittest scenario"""
import pytest

from tests.testlibraries.fixturefilehandlerfortest.fixture_file_handlers_for_test import (
    FixtureFileDeployerForTest,
    TargetFilePathVacatorForTest,
)
from tests.testscenarios import (
    CONTENT_IN_PROJECT_TEST_RESOURCE_FILE_FOR_ADVANCED,
    CONTENT_IN_TEST_RESOURCE_FILE,
    FILE_PATH_DEPLOY,
    FILE_PATH_VACATE,
)
from yourproduct.unittest_context_advanced import AdvancedConfigurableTestCase
from yourproduct.unittest_context_basic import ConfigurableTestCase


class TestConfigHandlerUnittest(ConfigurableTestCase):
    """Tests for unittest scenario"""

    @staticmethod
    def test():
        """Config file for test should be loaded."""
        assert not FILE_PATH_DEPLOY.target.exists()


@pytest.fixture
def target_file():
    """This fixture prepares resource file."""

    class Deployer(FixtureFileDeployerForTest):
        """This class deploys resource file into target file path."""

        FILE_PATH = FILE_PATH_DEPLOY

    Deployer.set_up()
    yield
    Deployer.do_cleanups()


@pytest.fixture
def target_file_empty():
    """This fixture prepares target file path empty."""

    class Vacator(TargetFilePathVacatorForTest):
        """This class vacates resource file into target file path."""

        FILE_PATH = FILE_PATH_VACATE

    Vacator.set_up()
    yield
    Vacator.do_cleanups()


class TestConfigHandlerUnittestBeforeAfter:
    """Tests for before / after states of ConfigHandler implemented by unittest."""

    # Reason: pytest fixture. pylint: disable=unused-argument, redefined-outer-name
    def test_case_when_target_exist(self, target_file):
        """
        Target file should be test resource before set up.
        Target file should not exist between set up and do cleanups.
        Target file should be test resource after do cleanups.
        """
        assert FILE_PATH_DEPLOY.target.read_text() == CONTENT_IN_TEST_RESOURCE_FILE
        self._set_up_by_unittest()
        assert not FILE_PATH_DEPLOY.target.exists()
        self._do_cleanups_by_unittest()
        assert FILE_PATH_DEPLOY.target.read_text() == CONTENT_IN_TEST_RESOURCE_FILE

    # Reason: pytest fixture. pylint: disable=unused-argument, redefined-outer-name
    def test_case_when_target_not_exist(self, target_file_empty):
        """
        Target file should not exist anytime.
        """
        assert not FILE_PATH_VACATE.target.exists()
        self._set_up_by_unittest()
        assert not FILE_PATH_VACATE.target.exists()
        self._do_cleanups_by_unittest()
        assert not FILE_PATH_VACATE.target.exists()

    @staticmethod
    def _set_up_by_unittest():
        ConfigurableTestCase(methodName="setUp").setUp()

    @staticmethod
    def _do_cleanups_by_unittest():
        ConfigurableTestCase(methodName="doCleanups").doCleanups()


class TestAdvancedConfigHandlerUnittest(AdvancedConfigurableTestCase):
    """Tests for unittest scenario"""

    @staticmethod
    def test_advanced():
        """Config file for test should be loaded."""
        assert FILE_PATH_DEPLOY.target.read_text() == CONTENT_IN_PROJECT_TEST_RESOURCE_FILE_FOR_ADVANCED
