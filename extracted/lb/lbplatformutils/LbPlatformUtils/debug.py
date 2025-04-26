#!/usr/bin/env python
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
from __future__ import absolute_import, division, print_function

import argparse
import json
import os
import subprocess
import sys
from collections import defaultdict
from distutils.spawn import find_executable

try:
    from shlex import join as join_cmd
except ImportError:

    def join_cmd(cmd):
        from pipes import quote

        return " ".join(quote(c) for c in cmd)


try:
    FileNotFoundError
except NameError:
    FileNotFoundError = OSError


ENV_VARS = [
    "BINARY_TAG",
    "CMAKE_PREFIX_PATH",
    "CMTCONFIG",
    "CMTPROJECTPATH",
    "force_host_os",
    "HOSTNAME",
    "LD_LIBRARY_PATH",
    "MYSITEROOT",
    "PATH",
    "PYTHONHOME",
    "PYTHONPATH",
    "ROOT_INCLUDE_PATH",
    "DIRACSITE",
]


REQUIRED_CVMFS_LOCATIONS = [
    "/cvmfs/cernvm-prod.cern.ch",
    "/cvmfs/lhcb-condb.cern.ch",
    "/cvmfs/lhcb.cern.ch",
]


OPTIONAL_CVMFS_LOCATIONS = [
    "/cvmfs/lhcbdev.cern.ch",
    "/cvmfs/sft.cern.ch",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="Path to a file to write results as JSON")
    parser.add_argument("--debug", action="store_true")
    # Primarily used to make it easier to run in CI
    parser.add_argument("--no-exit-with-error-count", action="store_true")
    args = parser.parse_args()

    result = check_system()

    if args.debug:
        print(json.dumps(result, indent=4))

    if args.output:
        print("Writing results to", args.output)
        with open(args.output, "wt") as fp:
            json.dump(result, fp, indent=4)

    print("Found", len(result["errors"]), "errors")
    for error in result["errors"]:
        print("    >", error)

    if not args.no_exit_with_error_count:
        sys.exit(len(result["errors"]))


def check_system():
    results = defaultdict(dict)
    results["errors"] = []

    results["cwd"] = os.getcwd()

    check_environment(results)

    check_cvmfs(results)

    run_cmd(results, ["lb-describe-platform"])

    check_file(results, "/proc/cpuinfo")
    check_file(results, "/etc/os-release")
    check_file(results, "/etc/redhat-release", missing_ok=True)
    check_file(results, "/etc/lsb-release", missing_ok=True)
    check_file(results, "/proc/mounts", missing_ok=True)

    check_apptainer(results)

    return dict(results)


def check_environment(results):
    for var in ENV_VARS:
        results["env"][var] = os.environ.get(var)


def check_cvmfs(results):
    for path in REQUIRED_CVMFS_LOCATIONS:
        try:
            results["required_cvmfs"][path] = os.listdir(path)
        except OSError:
            results["required_cvmfs"][path] = None
            results["errors"].append(
                "Required CVMFS location " + path + " is not mounted"
            )

    for path in OPTIONAL_CVMFS_LOCATIONS:
        try:
            results["optional_cvmfs"][path] = os.listdir(path)
        except OSError:
            results["optional_cvmfs"][path] = None


def check_apptainer(results):
    try:
        with open("/proc/sys/user/max_user_namespaces", "rt") as fp:
            results["max_user_namespaces"] = fp.read()
        if int(results["max_user_namespaces"]) < 1000:
            results["errors"].append(
                "/proc/sys/user/max_user_namespaces should contain a "
                "large number (e.g. 15076)"
            )
    except Exception as e:
        results["errors"].append(
            "Failed to parse /proc/sys/user/max_user_namespaces: %s" % e
        )

    results["apptainer"] = find_executable("apptainer")

    if results["apptainer"] is None:
        results["errors"].append("No apptainer binary found")
    else:
        run_cmd(results, ["apptainer", "--version"])

        rc, stdout, stderr = run_apptainer(results, ["pwd"], silent=True)
        if os.getcwd() != os.path.normpath(stdout.strip()):
            results["errors"].append(
                "Working directory inside apptainer (%s) doesn't match outside (%s)"
                % (os.path.normpath(stdout.strip()), os.getcwd())
            )

        run_apptainer(results, ["pwd"], verbose=True)

        run_cmd(
            results,
            [
                "lb-run",
                "--container",
                "apptainer",
                "-c",
                "best",
                "--siteroot=/cvmfs/lhcb.cern.ch/lib",
                "DaVinci/v45r5",
                "gaudirun.py",
                "--help",
            ],
        )


def run_cmd(results, command):
    cmd = join_cmd(command)

    # Having PWD set causes some versions of apptainer to ignore the current
    # working directory and, if the path in PWD contains symlinks, apptainer can
    # fail to set the current working directory correctly and default to $HOME.
    env = os.environ.copy()
    env.pop("PWD", None)

    try:
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            env=env,
        )
        stdout, stderr = proc.communicate()
    except FileNotFoundError:
        results["commands"][cmd] = None, None, None
        results["errors"].append("File not found when running %s" % cmd)
    else:
        results["commands"][cmd] = proc.returncode, stdout, stderr
        if proc.returncode > 0:
            results["errors"].append(
                "Command exited with %d: %s" % (proc.returncode, cmd)
            )
    return results["commands"][cmd]


def run_apptainer(results, cmd, silent=False, verbose=False):
    apptainer_cmd_base = ["apptainer"]
    if silent:
        apptainer_cmd_base += ["--silent"]
    if verbose:
        apptainer_cmd_base += ["--debug"]

    apptainer_cmd_base += [
        "exec",
        "--bind",
        "/cvmfs",
        "--bind",
        os.getcwd(),
        "--userns",
    ]
    if "X509_USER_PROXY" in os.environ and os.path.isfile(
        os.environ["X509_USER_PROXY"]
    ):
        apptainer_cmd_base += ["--bind", os.environ["X509_USER_PROXY"]]
    apptainer_cmd_base += ["/cvmfs/cernvm-prod.cern.ch/cvm3"]
    return run_cmd(results, apptainer_cmd_base + cmd)


def check_file(results, fn, missing_ok=False):
    if os.path.exists(fn):
        try:
            with open(fn, "rt") as fp:
                results["files"][fn] = fp.read()
        except Exception as e:
            results["errors"].append("Failed to read %s: %s" % (fn, e))
            results["cpuinfo"] = repr(e)
    else:
        results["files"][fn] = None
        if not missing_ok:
            results["errors"].append("%s does not exist" % fn)


if __name__ == "__main__":
    main()
