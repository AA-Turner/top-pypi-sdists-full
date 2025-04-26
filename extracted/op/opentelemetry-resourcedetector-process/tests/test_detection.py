import os
import sys

import pytest
from opentelemetry.sdk.resources import Resource

from opentelemetry_resourcedetector_process import Attributes, ProcessResourceDetector


@pytest.fixture(scope='module')
def resource() -> Resource:
    return ProcessResourceDetector().detect()


@pytest.fixture(scope='module')
def attributes(resource: Resource) -> Attributes:
    return dict(resource.attributes)


def test_python_version_info(attributes: Attributes):
    assert attributes['process.runtime.name'] == sys.implementation.name
    assert attributes['process.runtime.description'] == sys.version
    assert attributes['process.runtime.version']


def test_pid(attributes: Attributes):
    assert attributes['process.pid'] == os.getpid()


def test_executable(attributes: Attributes):
    assert attributes['process.executable.name'] == 'pytest'

    path = attributes['process.executable.path']
    assert isinstance(path, str)
    assert '/python3' in path


def test_command_line(attributes: Attributes):
    command_line = attributes['process.command_line']
    assert isinstance(command_line, str)

    command = attributes['process.command']
    assert isinstance(command, str)

    command_args = attributes['process.command_args']
    assert isinstance(command_args, str)

    assert '/python' in command_line
    assert '/python' in command
    assert '/python' not in command_args

    assert '/pytest' in command_line
    assert '/pytest' not in command
    assert '/pytest' in command_args

    assert command_line == (command + ' ' + command_args).strip()
