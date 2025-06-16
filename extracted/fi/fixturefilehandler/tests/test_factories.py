"""Tests for factories module."""
from pathlib import Path

import pytest

from fixturefilehandler import ResourceFileDeployer, TargetFilePathVacator
from fixturefilehandler.factories import DeployerFactory, VacatorFactory
from fixturefilehandler.file_paths import RelativeDeployFilePath, SimpleDeployFilePath, YamlConfigFilePathBuilder


class TestVacatorFactory:
    """Tests for VacatorFactory."""

    @staticmethod
    @pytest.mark.parametrize(
        "file_path",
        [
            (SimpleDeployFilePath(Path("path_b"), Path("path_c"), Path("path_a"))),
            (RelativeDeployFilePath(Path("path_1"), Path("path_2"), Path("path_3"))),
            (YamlConfigFilePathBuilder()),
        ],
    )
    def test(file_path):
        """
        Factory creates vacator instance.
        Created handler has same file_path with argument.
        """
        vacator = VacatorFactory.create(file_path)
        assert issubclass(vacator, TargetFilePathVacator)
        # Reason: pylint bug @see https://github.com/PyCQA/pylint/issues/3167
        # pylint: disable=no-member
        assert vacator.FILE_PATH == file_path


class TestDeployerFactory:
    """Tests for DeployerFactory."""

    @staticmethod
    @pytest.mark.parametrize(
        "file_path",
        [
            (SimpleDeployFilePath(Path("path_b"), Path("path_c"), Path("path_a"))),
            (RelativeDeployFilePath(Path("path_1"), Path("path_2"), Path("path_3"))),
            (YamlConfigFilePathBuilder()),
        ],
    )
    def test(file_path):
        """
        Factory creates deployer instance.
        Created handler has same file_path with argument.
        """
        deployer = DeployerFactory.create(file_path)
        assert issubclass(deployer, ResourceFileDeployer)
        # Reason: pylint bug @see https://github.com/PyCQA/pylint/issues/3167
        # pylint: disable=no-member
        assert deployer.FILE_PATH == file_path
