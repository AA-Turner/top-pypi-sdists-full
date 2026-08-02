# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Environment compatibility check."""

import sys


def check_python_string(python_lower, python_upper=None):
    """Ensure current Python interpreter is a version between lower and upper.

    Arguments:
        python_lower (str): Required lower bound for Python version.
        python_upper (str): Optional upper bound for Python version.
    Raises:
        RuntimeError: If current Python executable is not compatible with powertrain_build.

    """
    versions = [_split_version(python_lower)]
    if python_upper:
        versions.append(_split_version(python_upper))
    check_python_tuple(*versions)


def check_python_tuple(python_lower, python_upper=None):
    """Ensure current Python interpreter is a version between lower and upper.

    Arguments:
        python_lower (2-tuple): Required lower bound for Python version.
        python_upper (2-tuple): Optional upper bound for Python version.
    Raises:
        RuntimeError: If current Python executable is not compatible with powertrain_build.

    """
    cur_version = sys.version_info[:2]

    if cur_version[0] < python_lower[0] or cur_version[1] < python_lower[1]:
        raise RuntimeError(_format_error(f'must be higher than {python_lower}'))

    if python_upper and (cur_version[0] > python_upper[0] or cur_version[1] > python_upper[1]):
        raise RuntimeError(_format_error(f'must be lower than {python_upper}'))


def _split_version(version_string):
    """Split a major.minor style string and returns a 2-tuple of integers."""
    parts = version_string.split('.')
    return (int(parts[0]), int(parts[1]))


def _format_error(message):
    """Return a version error string including current interpreter, version and a custom message."""
    return f'Unsupported Python version ({sys.version_info}), {message}. Path: {sys.executable}'
