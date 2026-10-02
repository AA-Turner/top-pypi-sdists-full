# Copyright 2025 Agnostiq Inc.

import sys
from unittest.mock import patch

import pytest

import covalent_cloud as cc
from covalent_cloud.shared.classes.api import DispatcherAPI
from covalent_cloud.swe_management.swe_manager import PY_VERSION_WARNING_TEMPLATE

_MOCK_LOCAL_VERSION_INFO = (3, 10, 16)
_MOCK_LOCAL_VERSION = ".".join(map(str, _MOCK_LOCAL_VERSION_INFO))


def test_python_version_unspecified():
    """Test that no warning is raised when Python version is not specified."""
    with patch.object(DispatcherAPI, "post"):
        with pytest.warns(None):
            cc.create_env("testing_env", pip=[], conda=[], wait=False)


def test_python_version_exact():
    """Test that the exact local Python version is not warned against."""
    with patch.object(DispatcherAPI, "post"), patch.object(
        sys, "version_info", _MOCK_LOCAL_VERSION_INFO
    ):
        with pytest.warns(None):
            cc.create_env(
                "testing_env", pip=[], conda=[f"python={_MOCK_LOCAL_VERSION}"], wait=False
            )


@pytest.mark.parametrize(
    "req_version",
    [
        # Strict requirement, different from local version.
        ("python=3.1.2"),
        ("python=3.9.1"),
        ("python=2.0.8"),
        ("python=3.8.4"),
        ("python=3.9"),
        ("python=3.7"),
        ("python=3"),
        # Flexible requirement with bound at same as local version.
        (f"python<{_MOCK_LOCAL_VERSION}"),
        (f"python>{_MOCK_LOCAL_VERSION}"),
        (f"python<={_MOCK_LOCAL_VERSION}"),
        (f"python>={_MOCK_LOCAL_VERSION}"),
        (f"python!={_MOCK_LOCAL_VERSION}"),
        # Multi-part requirement, necessarily flexible.
        ("python>=3.9,<3.12"),
        ("python>=3.9,<3.12,!=3.9.2"),
    ],
)
def test_python_version_warnings(req_version):
    """Test valid Python versions that cause a warning due to local environment."""
    with patch.object(DispatcherAPI, "post"):
        with pytest.warns(UserWarning) as record:
            cc.create_env("testing_env", pip=[], conda=[req_version], wait=False)

    assert len(record) == 1
    assert record[0].message.args[0] == PY_VERSION_WARNING_TEMPLATE.format(
        local_version=_MOCK_LOCAL_VERSION,
        dependency=req_version,
    )


@pytest.mark.parametrize(
    "req_version",
    [
        ("python 3.10"),
        ("python"),
        ("python::3.10"),
    ],
)
def test_python_dependency_invalid(req_version):
    """
    Test failure to match the Python version regex.
    Cases must be recognized as Python versions to be considered.
    E.g. 'pythoon=3.10' will not raise an error here.
    """
    with patch.object(DispatcherAPI, "post"):
        with pytest.raises(ValueError, match="Invalid python dependency: "):
            cc.create_env("testing_env", pip=[], conda=[req_version], wait=False)


@pytest.mark.parametrize(
    "req_version",
    [
        ("python>=3,<-312"),
        ("python>3,abcde"),
        ("python="),
    ],
)
def test_python_version_invalid(req_version):
    """
    Test failure due to `packaging.version.parse` errors.
    These errors happen when the pattern is matched but the
    version code is not parsable.
    """
    with patch.object(DispatcherAPI, "post"):
        with pytest.raises(ValueError, match="Invalid python version: "):
            cc.create_env("testing_env", pip=[], conda=[req_version], wait=False)
