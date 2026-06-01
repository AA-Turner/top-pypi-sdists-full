"""OS handler tests."""

import pytest
from bacore.domain.settings import System
from bacore.domain.system import CLIProgram
from bacore.interactors.os_handler import command_on_path, system_information_os

pytestmark = pytest.mark.interactors


@pytest.fixture
def fixture_test_command_on_path():
    """Fixture for command_on_path."""
    match system_information_os().os:
        case "Darwin":
            return "ls"
        case "Linux":
            return "ls"
        case "Windows":
            return "dir"
        case _:
            raise ValueError("OS is not supported.")


@pytest.fixture
def fixture_test_system_information():
    """Fixture for system_information_os."""
    return "Darwin"


def test_system_information_os(fixture_test_system_information):
    """Test system_information_os."""
    information = system_information_os(
        func_os=fixture_test_system_information
    )
    assert isinstance(information, System)
    assert information.os == "Darwin"


def test_command_on_path(fixture_test_command_on_path):
    """Test command_on_path."""
    assert command_on_path(CLIProgram(name=fixture_test_command_on_path)) is True
    assert command_on_path(CLIProgram(name="bogus_does_not_exist")) is False
