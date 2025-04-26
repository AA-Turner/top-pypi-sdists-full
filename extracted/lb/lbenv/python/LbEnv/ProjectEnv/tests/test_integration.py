###############################################################################
# (c) Copyright 2018 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

__author__ = "Chris Burr <c.b@cern.ch>"

import os
import re
import tempfile
import shutil
from pathlib import Path
from subprocess import PIPE, STDOUT, CalledProcessError, check_output, run

import pytest
from LbPlatformUtils.inspect import os_id

if os_id().endswith("slc6"):
    CAN_RUN_NATIVE_SLC5 = True
    CAN_RUN_NATIVE_SLC6 = True
    CAN_RUN_NATIVE_CENTOS7 = False
elif os_id().endswith("centos7"):
    CAN_RUN_NATIVE_SLC5 = False
    CAN_RUN_NATIVE_SLC6 = True
    CAN_RUN_NATIVE_CENTOS7 = True
elif os_id().endswith("centos8"):
    CAN_RUN_NATIVE_SLC5 = False
    CAN_RUN_NATIVE_SLC6 = False
    CAN_RUN_NATIVE_CENTOS7 = False
else:
    CAN_RUN_NATIVE_SLC5 = False
    CAN_RUN_NATIVE_SLC6 = False
    CAN_RUN_NATIVE_CENTOS7 = False
CONTAINER_IMPLEMENTATION = os.environ.get("CONTAINER_IMPLEMENTATION", "")


BASE_LBRUN_COMMAND = ["lb-run", "--debug"]
SETUPPTOJECT_COMMAND = ["--platform", "x86_64-slc5-gcc46-opt", "Gaudi/v23r0"]


def _check_gaudirun(options):
    output = check_output(BASE_LBRUN_COMMAND + options + ["gaudirun.py"], stderr=STDOUT)
    output = output.decode()
    assert "Application Manager Terminated successfully" in output
    used_container = (
        "preparing singularity wrapper command" in output
        or "preparing apptainer wrapper command" in output
    )
    return output, used_container

@pytest.fixture(scope="session", autouse=True)
def setup():
    if not os.path.isdir("/cvmfs/lhcb.cern.ch"):
        pytest.skip("Skipping integration tests due to missing siteroot")
    if not os.path.isdir("/cvmfs/cernvm-prod.cern.ch"):
        pytest.skip("Skipping integration tests due to missing cernvm")
    if not CONTAINER_IMPLEMENTATION:
        pytest.skip(
            "Skipping integration tests due CONTAINER_IMPLEMENTATION not being set"
        )
    if not shutil.which(CONTAINER_IMPLEMENTATION):
        raise RuntimeError("Failed to find %s" % CONTAINER_IMPLEMENTATION)

    if CONTAINER_IMPLEMENTATION == "singularity":
        # Only singularity 3 will work correctly
        singularity_version = check_output(
            [CONTAINER_IMPLEMENTATION, "--version"]
        ).decode()
        match = re.search(r"(?:^| )(\d+)\.\d+\.\d+", singularity_version)
        assert match, singularity_version
        if int(match.groups()[0]) < 3:
            pytest.skip("Singularity 3 or newer is required for integration tests")

    from os.path import abspath, dirname, join, pardir

    # FIXME compatibility py2-py3
    os.environ["CMAKE_PREFIX_PATH"] = abspath(
        join(
            dirname(__file__),
            pardir,
            pardir,
            pardir,
            pardir,
            pardir,
            "python",
            "LbEnv",
            "ProjectEnv",
            "tests",
            "data",
        )
    )
    yield


def test_setupproject():
    command = SETUPPTOJECT_COMMAND
    try:
        output, used_container = _check_gaudirun(["--disallow-containers"] + command)
    except CalledProcessError:
        assert not CAN_RUN_NATIVE_SLC5
    else:
        assert CAN_RUN_NATIVE_SLC5, output

    output, used_container = _check_gaudirun(
        ["--container", CONTAINER_IMPLEMENTATION] + command
    )
    assert used_container, output

    output, used_container = _check_gaudirun(command)
    assert used_container != CAN_RUN_NATIVE_SLC5, output
    if not CAN_RUN_NATIVE_SLC5:
        assert "Decided best container to use is" in output, output

    output, used_container = _check_gaudirun(
        ["--allow-containers", "--prefer-container"] + command
    )
    assert used_container, output
    assert "Decided best container to use is" in output, output


def test_setupproject_best():
    command = ["--platform", "best", "Gaudi/v23r0"]
    try:
        output, used_container = _check_gaudirun(["--disallow-containers"] + command)
    except CalledProcessError:
        assert not CAN_RUN_NATIVE_SLC5
    else:
        assert CAN_RUN_NATIVE_SLC5, output
        assert not used_container, output

    output, used_container = _check_gaudirun(
        ["--container", CONTAINER_IMPLEMENTATION] + command
    )
    assert used_container, output

    output, used_container = _check_gaudirun(command)
    assert used_container != CAN_RUN_NATIVE_SLC5, output
    if not CAN_RUN_NATIVE_SLC5:
        assert "Decided best container to use is" in output, output

    output, used_container = _check_gaudirun(
        ["--allow-containers", "--prefer-container"] + command
    )
    assert used_container, output
    assert "Decided best container to use is" in output, output


def test_lbrun_slc6():
    command = ["--platform", "x86_64-slc6-gcc8-opt", "Gaudi/v32r0"]
    try:
        output, used_container = _check_gaudirun(["--disallow-containers"] + command)
    except CalledProcessError:
        assert not CAN_RUN_NATIVE_SLC6
    else:
        assert CAN_RUN_NATIVE_SLC6, output
        assert not used_container, output

    output, used_container = _check_gaudirun(
        ["--container", CONTAINER_IMPLEMENTATION] + command
    )
    assert used_container, output

    output, used_container = _check_gaudirun(command)
    assert used_container != CAN_RUN_NATIVE_SLC6, output
    if not CAN_RUN_NATIVE_SLC6:
        assert "Decided best container to use is" in output, output

    output, used_container = _check_gaudirun(
        ["--allow-containers", "--prefer-container"] + command
    )
    assert used_container, output
    assert "Decided best container to use is" in output, output


def test_lbrun_centos7():
    command = ["--platform", "x86_64-centos7-gcc8-opt", "Gaudi/v32r0"]
    try:
        output, used_container = _check_gaudirun(["--disallow-containers"] + command)
    except CalledProcessError:
        assert not CAN_RUN_NATIVE_CENTOS7
    else:
        assert CAN_RUN_NATIVE_CENTOS7, output
        assert not used_container, output

    output, used_container = _check_gaudirun(
        ["--container", CONTAINER_IMPLEMENTATION] + command
    )
    assert used_container, output

    output, used_container = _check_gaudirun(command)
    assert used_container != CAN_RUN_NATIVE_CENTOS7, output
    if not CAN_RUN_NATIVE_CENTOS7:
        assert "Decided best container to use is" in output, output

    output, used_container = _check_gaudirun(
        ["--allow-containers", "--prefer-container"] + command
    )
    assert used_container, output
    assert "Decided best container to use is" in output, output


def test_lbrun_best():
    command = ["--platform", "best", "Gaudi/v32r0"]
    try:
        output, used_container = _check_gaudirun(["--disallow-containers"] + command)
    except CalledProcessError:
        assert not (CAN_RUN_NATIVE_SLC6 or CAN_RUN_NATIVE_CENTOS7)
    else:
        assert CAN_RUN_NATIVE_SLC6 or CAN_RUN_NATIVE_CENTOS7, output
        assert not used_container, output

    output, used_container = _check_gaudirun(
        ["--container", CONTAINER_IMPLEMENTATION] + command
    )
    assert used_container, output

    output, used_container = _check_gaudirun(command)
    assert used_container != (CAN_RUN_NATIVE_SLC6 or CAN_RUN_NATIVE_CENTOS7), output
    if not (CAN_RUN_NATIVE_SLC6 or CAN_RUN_NATIVE_CENTOS7):
        assert "Decided best container to use is" in output, output

    output, used_container = _check_gaudirun(
        ["--allow-containers", "--prefer-container"] + command
    )
    assert used_container, output
    assert "Decided best container to use is" in output, output


@pytest.mark.parametrize(
    "command,error_message",
    [
        (SETUPPTOJECT_COMMAND, "Cannot find project 'Gaudi'"),
        (
            ["--platform", "best", "Gaudi/v32r0"],
            "current host does not support any of Gaudi/v32r0",
        ),
    ],
)
def test_setupproject_siteroot(command, error_message):
    message = "Using default siteroot of /cvmfs/lhcb.cern.ch/lib"

    output, _ = _check_gaudirun(command)
    assert message in output, output

    output, _ = _check_gaudirun(["--siteroot", "/cvmfs/lhcb.cern.ch/lib"] + command)
    assert message not in output, output

    try:
        _check_gaudirun(["--siteroot", "/cvmfs/lhcb.invalid"] + command)
    except CalledProcessError as e:
        assert error_message in e.output.decode()


_bind_tmp_dir = tempfile.TemporaryDirectory()
bind_tmp_dir = Path(_bind_tmp_dir.name)


@pytest.mark.parametrize("use_env", [True, False])
@pytest.mark.parametrize(
    "bind_specs,test_dir,expect_success",
    [
        ([f"{bind_tmp_dir.parent}:/mounted_path"], "/mounted_path", True),
        (None, "/mounted_path", False),
        ([f"{bind_tmp_dir.parent}:/mounted_path"], "/wrong_path", False),
        (
            [
                f"{bind_tmp_dir.parent}:/mounted_path",
                f"{bind_tmp_dir.parent}:/other_path",
            ],
            "/wrong_path",
            False,
        ),
        (
            [
                f"{bind_tmp_dir.parent}:/mounted_path",
                f"{bind_tmp_dir.parent}:/other_path",
            ],
            "/mounted_path",
            True,
        ),
        (
            [
                f"{bind_tmp_dir.parent}:/mounted_path",
                f"{bind_tmp_dir.parent}:/other_path",
            ],
            "/other_path",
            True,
        ),
    ],
)
def test_bind(use_env, bind_specs, test_dir, expect_success):
    command = SETUPPTOJECT_COMMAND + ["ls", test_dir]
    env = os.environ
    if bind_specs is not None:
        if use_env:
            env = {**env, "LBRUN_BINDS": ";".join(bind_specs)}
        else:
            for bind_spec in bind_specs:
                command = ["--bind", bind_spec] + command
    proc = run(
        ["lb-run"] + command,
        stdout=PIPE,
        stderr=STDOUT,
        text=True,
        check=False,
        env=env,
    )
    if expect_success:
        assert proc.returncode == 0, proc.stdout
        assert "No such file or directory" not in proc.stdout, proc.stdout
        assert bind_tmp_dir.name in proc.stdout, proc.stdout
    else:
        assert proc.returncode != 1, proc.stdout
        assert "No such file or directory" in proc.stdout, proc.stdout
