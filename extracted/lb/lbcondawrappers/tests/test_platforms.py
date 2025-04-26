###############################################################################
# (c) Copyright 2021 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import platform

import pytest

import LbCondaWrappers


@pytest.mark.parametrize(
    "system, arch, expected",
    [
        ["Linux", "x86_64", "linux-64"],
        ["Linux", "aarch64", "linux-aarch64"],
        ["Linux", "ppc64le", "linux-ppc64le"],
        ["Darwin", "x86_64", "osx-64"],
        ["Darwin", "arm64", "osx-arm64"],
    ],
)
def test_compute_conda_subdir(system, arch, expected, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: system)
    monkeypatch.setattr(platform, "machine", lambda: arch)
    assert LbCondaWrappers.compute_conda_subdir() == expected


def test_env_override(monkeypatch):
    assert LbCondaWrappers.compute_conda_subdir() == "linux-64"
    monkeypatch.setenv("CONDA_SUBDIR", "something-something")
    assert LbCondaWrappers.compute_conda_subdir() == "something-something"


def test_known_subdirs():
    assert "linux-64" in LbCondaWrappers.KNOWN_CONDA_SUBDIRS
    assert "linux-ppc64le" in LbCondaWrappers.KNOWN_CONDA_SUBDIRS
    assert "linux-aarch64" in LbCondaWrappers.KNOWN_CONDA_SUBDIRS
