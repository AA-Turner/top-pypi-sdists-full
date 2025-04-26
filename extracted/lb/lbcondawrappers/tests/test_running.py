###############################################################################
# (c) Copyright 2022 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

import os
import random
import subprocess
from os.path import join
from tempfile import NamedTemporaryFile, TemporaryDirectory

import pytest

from LbCondaWrappers import (
    CONDA_ENVIRONMENTS,
    DISPLAY_VERSIONS,
    check_install_root_available,
)


@pytest.fixture
def require_cvmfs_lhcbdev():
    assert os.listdir("/cvmfs/lhcbdev.cern.ch")


def check_output(cmd, rc=0, write_stdin=None):
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        universal_newlines=True,
    )
    stdout, stderr = proc.communicate(input=write_stdin)
    assert proc.returncode == rc, (stdout, stderr)
    return stdout, stderr


def get_random_env():
    # Try with a random version
    env_names = list(CONDA_ENVIRONMENTS)
    random.shuffle(env_names)
    for env_name in env_names:
        env_versions = list(CONDA_ENVIRONMENTS[env_name])
        random.shuffle(env_versions)
        env_version = env_versions[0]
        print("Running tests with", env_names, env_version)
        return env_name, env_version
    raise ValueError("Failed to find a version to test with")


def test_versions(require_cvmfs_lhcbdev):
    assert len(CONDA_ENVIRONMENTS) >= 1
    assert len(DISPLAY_VERSIONS) == len(CONDA_ENVIRONMENTS)


def test_lb_conda_list_names(require_cvmfs_lhcbdev):
    stdout, stderr = check_output(["lb-conda", "--list"])
    for name in CONDA_ENVIRONMENTS:
        assert name in stdout


@pytest.mark.parametrize(
    "cmd",
    [
        ["--list", get_random_env()[0]],
        ["--list", get_random_env()[0], "bash"],
        ["--list", get_random_env()[0], "exit", "100"],
    ],
)
def test_lb_conda_list_versions(cmd, require_cvmfs_lhcbdev):
    stdout, stderr = check_output(["lb-conda", *cmd])
    env_name, env_version = get_random_env()
    for version in CONDA_ENVIRONMENTS[cmd[1]]:
        assert version in stdout or version.split("_")[0] in stdout


def test_lb_conda_echo_list(require_cvmfs_lhcbdev):
    env_name, env_version = get_random_env()
    stdout, stderr = check_output(["lb-conda", env_name, "echo", "--list"])
    assert stdout.strip() == "--list"
    stdout, stderr = check_output(
        ["lb-conda", env_name + "/" + env_version, "echo", "--list"]
    )
    assert stdout.strip() == "--list"


@pytest.mark.parametrize(
    "cmd",
    [
        ["--export", get_random_env()[0]],
        [get_random_env()[0], "--export"],
        ["--export", get_random_env()[0], "bash"],
        ["--export", get_random_env()[0], "exit", "100"],
    ],
)
def test_lb_conda_export(cmd, require_cvmfs_lhcbdev):
    stdout, stderr = check_output(["lb-conda", *cmd])
    assert "channels:" in stdout
    assert "dependencies:" in stdout


def test_lb_conda_command(require_cvmfs_lhcbdev):
    env_name, env_version = get_random_env()

    stdout, stderr = check_output(["lb-conda", env_name, "env"])
    assert env_name in stdout

    stdout, stderr = check_output(["lb-conda", env_name + "/" + env_version, "env"])
    assert join(env_name, env_version) in stdout


@pytest.mark.parametrize(
    "texlive_arg",
    [
        ["--texlive"],
        ["--texlive-version=2020"],
        ["--texlive-version", "2020"],
    ],
)
def test_lb_conda_command_texlive(require_cvmfs_lhcbdev, texlive_arg):
    env_name, env_version = get_random_env()
    year = "2020"
    arch = "x86_64-linux"
    path_to_latex = f"/cvmfs/lhcbdev.cern.ch/tools/texlive/{year}/bin/{arch}/latex"
    lb_conda_cmd = ["lb-conda", *texlive_arg, env_name]

    stdout, stderr = check_output([*lb_conda_cmd, "which", "latex"])
    assert stdout.strip() == path_to_latex

    stdout, stderr = check_output([*lb_conda_cmd, "latex", "--version"])
    assert f"TeX Live {year}" in stdout.strip()


# def test_lb_conda_shells(require_cvmfs_lhcbdev):
#     stdout, stderr = check_output(["lb-conda", "bash", "-c", "env"])
#     assert "DIRAC=" in stdout

#     stdout, stderr = check_output(["lb-conda", "sh", "-c", "env"], rc=1)
#     assert "ERROR" in stderr

#     stdout, stderr = check_output(["lb-conda", "zsh", "-c", "env"], rc=1)
#     assert "ERROR" in stderr

#     stdout, stderr = check_output(["lb-conda", "ksh", "-c", "env"], rc=1)
#     assert "ERROR" in stderr

#     stdout, stderr = check_output(["lb-conda", "csh", "-c", "env"], rc=1)
#     assert "ERROR" in stderr

#     stdout, stderr = check_output(["lb-conda", "tcsh", "-c", "env"], rc=1)
#     assert "ERROR" in stderr

#     stdout, stderr = check_output(["lb-conda", "fish", "-c", "env"], rc=1)
#     assert "ERROR" in stderr


def test_lb_conda_interactive(require_cvmfs_lhcbdev):
    env_name, env_version = get_random_env()

    stdout, stderr = check_output(["lb-conda", env_name], write_stdin="env")
    assert env_name in stdout

    stdout, stderr = check_output(
        ["lb-conda", env_name + "/" + env_version], write_stdin="env"
    )
    assert join(env_name, env_version) in stdout

    stdout, stderr = check_output(["lb-conda", env_name, "bash"], write_stdin="env")
    assert env_name in stdout

    stdout, stderr = check_output(
        ["lb-conda", env_name + "/" + env_version, "bash"], write_stdin="env"
    )
    assert join(env_name, env_version) in stdout


# def test_install_locations(require_cvmfs_lhcbdev, require_cvmfs_lhcbdev):
#     stdout, stderr = check_output(["lb-conda", "env"])
#     assert "DIRAC=/cvmfs/lhcb.cern.ch" in stdout

#     version = get_random_version(path="/cvmfs/lhcb.cern.ch")
#     stdout, stderr = check_output(["lb-conda", version, "env"])
#     assert "DIRAC=/cvmfs/lhcb.cern.ch" in stdout

#     version = get_random_version(path="/cvmfs/lhcbdev.cern.ch")
#     stdout, stderr = check_output(["lb-conda", version, "env"])
#     assert "DIRAC=/cvmfs/lhcbdev.cern.ch" in stdout


def test_lb_conda_command_extravars(require_cvmfs_lhcbdev):
    env_name, env_version = get_random_env()

    stdout, stderr = check_output(
        ["lb-conda", "-e", "TESTVAR=TESTVALUE", env_name, "printenv", "TESTVAR"]
    )
    assert stdout.strip() == "TESTVALUE"


def test_cvmfs_lhcbdev_available():
    with TemporaryDirectory() as td:
        assert not check_install_root_available(td)
        with NamedTemporaryFile(dir=td):
            assert check_install_root_available(td)
    assert not check_install_root_available(td)
