"""This module implements tests for file_paths module."""
import os
from pathlib import Path

import pytest

from fixturefilehandler.file_paths import (
    RelativeDeployFilePath,
    RelativeVacateFilePath,
    SimpleDeployFilePath,
    SimpleVacateFilePath,
    YamlConfigFilePathBuilder,
)


class TestSimpleVacateFilePath:
    """Tests for SimpleVacateFilePath."""

    @staticmethod
    @pytest.mark.parametrize(
        "path_target, path_backup", [(Path("path_a"), Path("path_b")), (Path("path_1"), Path("path_2"))]
    )
    def test(path_target, path_backup):
        """Each property returns appropriate path based on python execution directory."""
        config_path_builder = SimpleVacateFilePath(path_target, path_backup)
        assert config_path_builder.target == path_target
        assert config_path_builder.backup == path_backup


class TestSimpleDeployFilePath:
    """Tests for SimpleDeployFilePath."""

    @staticmethod
    @pytest.mark.parametrize(
        "path_target, path_backup, path_resource",
        [(Path("path_a"), Path("path_b"), Path("path_c")), (Path("path_1"), Path("path_2"), Path("path_3"))],
    )
    def test(path_target, path_backup, path_resource):
        """Each property returns appropriate path based on python execution directory."""
        config_path_builder = SimpleDeployFilePath(path_target, path_backup, path_resource)
        assert config_path_builder.target == path_target
        assert config_path_builder.backup == path_backup
        assert config_path_builder.resource == path_resource


class TestRelativeVacateFilePath:
    """Tests for RelativeVacateFilePath."""

    @staticmethod
    def test_default():
        """Each property returns appropriate path based on python execution directory."""
        config_path_builder = RelativeVacateFilePath(Path("path_a"), Path("path_b"),)
        assert config_path_builder.target == Path(os.getcwd()) / "path_a"
        assert config_path_builder.backup == Path(os.getcwd()) / "path_b"

    @staticmethod
    def test_customize():
        """Argument should be applied to properties."""
        config_path_builder = RelativeVacateFilePath(Path("path_1"), Path("path_2"), Path(__file__))
        assert config_path_builder.target == Path(__file__) / "path_1"
        assert config_path_builder.backup == Path(__file__) / "path_2"


class TestRelativeDeployFilePath:
    """Tests for RelativeFilePath."""

    @staticmethod
    def test_default():
        """Each property returns appropriate path based on python execution directory."""
        config_path_builder = RelativeDeployFilePath(Path("path_a"), Path("path_b"), Path("path_c"))
        assert config_path_builder.target == Path(os.getcwd()) / "path_a"
        assert config_path_builder.backup == Path(os.getcwd()) / "path_b"
        assert config_path_builder.resource == Path(os.getcwd()) / "path_c"

    @staticmethod
    def test_customize():
        """Argument should be applied to properties."""
        config_path_builder = RelativeDeployFilePath(Path("path_1"), Path("path_2"), Path("path_3"), Path(__file__))
        assert config_path_builder.target == Path(__file__) / "path_1"
        assert config_path_builder.backup == Path(__file__) / "path_2"
        assert config_path_builder.resource == Path(__file__) / "path_3"


class TestYamlConfigFilePathBuilder:
    """Tests for YamlConfigFilePathBuilder."""

    @staticmethod
    def test_default():
        """Each property returns appropriate path based on python execution directory."""
        config_path_builder = YamlConfigFilePathBuilder()
        assert config_path_builder.target == Path(os.getcwd()) / "config.yml"
        assert config_path_builder.backup == Path(os.getcwd()) / "config.yml.bak"
        assert config_path_builder.resource == Path(os.getcwd()) / "tests" / "config.yml.dist"

    @staticmethod
    def test_specify_target_directory():
        """Each property returns appropriate path based on specific directory."""
        config_path_builder = YamlConfigFilePathBuilder(path_target_directory=Path(__file__))
        assert config_path_builder.target == Path(__file__) / "config.yml"
        assert config_path_builder.backup == Path(__file__) / "config.yml.bak"
        assert config_path_builder.resource == Path(__file__) / "tests" / "config.yml.dist"

    @staticmethod
    def test_customize():
        """Argument should be applied to properties."""
        config_path_builder = YamlConfigFilePathBuilder(
            Path(__file__),
            Path("test/testresources"),
            Path("config_a.yml"),
            Path("config_backup.yml"),
            Path("config_b.yml"),
        )
        assert config_path_builder.target == Path(__file__) / "config_a.yml"
        assert config_path_builder.backup == Path(__file__) / "config_backup.yml"
        assert config_path_builder.resource == Path(__file__) / "test" / "testresources" / "config_b.yml"
