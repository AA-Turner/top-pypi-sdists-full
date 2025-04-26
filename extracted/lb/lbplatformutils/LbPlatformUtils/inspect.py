#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
"""
Utility functions for platform detection and compatibility mapping.

Part of the code was imported from Gaudi and inspired by
* https://github.com/HEP-SF/documents/tree/master/HSF-TN/draft-2015-NAM
* https://github.com/HEP-SF/tools
"""
__all__ = ("os_id", "architecture", "compiler_id")

import os
import platform
import re

try:
    from subprocess import STDOUT, CalledProcessError, check_output
except ImportError:  # pragma no cover
    # check_output was introduced in Python 2.7
    from subprocess import STDOUT, CalledProcessError

    def check_output(*args, **kwargs):
        """
        Minimal backport to Python 2.6 of check_output.
        """
        from subprocess import PIPE, Popen

        kwargs["stdout"] = PIPE
        proc = Popen(*args, **kwargs)
        out_err = proc.communicate()
        if proc.returncode:
            raise CalledProcessError(proc.returncode, args[0])
        return out_err


_root = "/cvmfs/lhcb.cern.ch/containers/os-base"
# The paths can contain arch and variant as defined in the OCI image spec:
# https://github.com/opencontainers/image-spec/blob/main/config.md#properties
_arch = platform.machine()
_arch = {"x86_64": "amd64", "aarch64": "arm64", "ppc64le": "ppc64le"}.get(_arch, _arch)
_variant = "" if _arch == "amd64" else "v8"
# FIXME: we should only list the paths and _detect_ the os_id and architecture in there
APPTAINER_ROOTS = [
    (
        "{root}/{image}/prod/{arch}{variant}".format(
            root=_root, image=image, arch=_arch, variant=_variant
        ),
        os_id,
    )
    # The first available container will be chosen by LbEnv
    # As the current OSs are only backwards compatible, newer OSs should be
    # placed lower in the list
    for os_id, image in [
        ("sl6", "slc6-devel"),
        ("sl7", "centos7-devel"),
        ("el9", "alma9-devel"),
    ]
]

# For backwards compatibility
SINGULARITY_ROOTS = APPTAINER_ROOTS


def parse_os_release(file_obj):
    """
    Extract OS id from content of /etc/os-release.

    See https://www.freedesktop.org/software/systemd/man/os-release.html
    """
    release = dict(
        stripped.split("=", 1)
        for line in file_obj
        for stripped in (line.strip(),)
        if "=" in stripped
    )

    for key in release:  # values might be surrounded by quotes
        release[key] = release[key].strip('"').strip("'")

    name = release.get("ID", "linux").split("-", 1)[0]
    compatible = name + release.get("ID_LIKE", "")
    if "rhel" in compatible or "suse" in compatible:
        version = release.get("VERSION_ID", "").split(".", 1)[0]
    else:
        version = release.get(
            "VERSION_ID", "testing" if name == "debian" else ""
        ).replace(".", "")
    if name == "scientific":
        name = "sl"  # that's the traditional name of

    return name, version


def parse_system_release(s):
    """
    Extract OS id from content of /etc/redhat-release like files.
    """
    name = "unknown"
    version = ""

    m = re.match(r"(.*) release (\d+)", s)
    if m:
        fullname, version = m.groups()
        if "CERN" in fullname:
            name = "slc"
        elif "Scientific Linux" in fullname:
            name = "sl"
        elif "CentOS" in fullname:
            name = "centos"
        elif "Red Hat Enterprise Linux" in fullname:
            name = "rhel"

    return name, version


def parse_lsb_release(lines):
    """
    Extract OS id from content of /etc/lsb-release files (in Debian derived OSs).
    """
    name = "unknown"
    version = ""

    for l in lines:
        if l.startswith("DISTRIB_ID="):
            name = l.strip()[11:].lower()
        elif l.startswith("DISTRIB_RELEASE="):
            version = l.strip()[16:].replace(".", "")

    return name, version


def _Linux_os():
    name = "unknown"
    version = ""

    try:
        os_release_fn = "/etc/os-release"
        # Some systems have an empty /etc/os-release that we should ignore
        if os.path.exists(os_release_fn) and os.path.getsize(os_release_fn) > 0:
            name, version = parse_os_release(open(os_release_fn))

        elif os.path.exists("/etc/redhat-release"):
            name, version = parse_system_release(open("/etc/redhat-release").read())

        elif os.path.exists("/etc/lsb-release"):
            name, version = parse_lsb_release(open("/etc/lsb-release"))

    except IOError:  # pragma: no cover
        pass  # ignore the error when we cannot read the file

    return name + version


def _Darwin_os():
    version = platform.mac_ver()[0].split(".")
    return "macos" + "".join(version[:2])


def _Windows_os():
    return "win" + platform.win32_ver()[1].split(".", 1)[0]


def _unknown_os():
    return "unknown"


_os_id_impl = globals().get("_%s_os" % platform.system(), _unknown_os)

_force_host_os_warning_printed = False


def os_id():
    if "force_host_os" in os.environ:
        global _force_host_os_warning_printed
        if not _force_host_os_warning_printed:
            from logging import warning

            warning(
                "overriding host os detection (using %s)", os.environ["force_host_os"]
            )
            _force_host_os_warning_printed = True
        return os.environ["force_host_os"]
    return _os_id_impl()


def architecture(minimum=False):
    """
    Return the host CPU architecture based on the supported instructions.

    The result is the most recent known architecture matching the supported
    instructions, unless minimum is set to True, in which case we return the
    base architecture.
    """
    from LbPlatformUtils.architectures import get_supported_archs

    flags = microarch_flags()
    arch = None
    if flags:
        # if minimum is true we take the latest entry, otherwise we take the first
        for arch in get_supported_archs(flags):
            if not minimum:
                break
    # no flag found or architecture unknown
    return arch or platform.machine() or "unknown"


def model_name():
    """
    Return CPU model name from /proc/cpuinfo.
    """
    if os.path.exists("/proc/cpuinfo"):
        cpuinfo = open("/proc/cpuinfo")
        for l in cpuinfo:
            if l.startswith("model name"):
                return l.split(":", 1)[1].strip()

    # if there's no model name in cpuinfo we can try with lscpu
    from distutils.spawn import find_executable

    if find_executable("lscpu"):
        for l in check_output(["lscpu"], stderr=STDOUT).decode().splitlines():
            if l.startswith("Model name"):
                return l.split(":", 1)[1].strip()

    return "unknown"


def microarch_flags():
    """
    Return a set with all microarchitecture flags from /proc/cpuinfo.
    """
    if os.path.exists("/proc/cpuinfo"):
        cpuinfo = open("/proc/cpuinfo")
        for l in cpuinfo:
            if l.startswith("flags") or l.startswith("Features"):
                flags = set(l.split(":", 1)[1].split())
                machine = platform.machine()
                if machine:
                    flags.add(machine)
                return flags
    # FIXME: This should probably print a warning
    return set()


def compiler_id(cmd=os.environ.get("CC", "cc")):
    """
    Return id of system compiler.
    """
    # prevent interference from localization
    env = dict(os.environ)
    env["LC_ALL"] = "C"
    try:
        m = re.search(
            r"(gcc|clang|icc|LLVM) version (\d+)\.(\d+)",
            check_output([cmd, "-v"], stderr=STDOUT, env=env).decode("utf-8"),
        )
        comp = "clang" if m.group(1) == "LLVM" else m.group(1)
        vers = m.group(2)
        if (comp == "gcc" and int(vers) < 7) or comp == "clang":
            vers += m.group(3)
        return comp + vers
    except (AttributeError, CalledProcessError, OSError):
        # prevent crashes if the compiler is not supported or not present
        return "unknown"


def apptainer_os_ids():
    """
    List the platforms supported via apptainer.
    """
    return _generic_os_ids("apptainer")


def singularity_os_ids():
    """
    List the platforms supported via singularity.
    """
    return _generic_os_ids("singularity")


def _generic_os_ids(container_executable):
    available_roots = [
        # 'path' generally refers to a sandbox, but in specific cases, it can
        # point to a sif file so we just need to check its existence.
        # This is the case in environments lacking a proper /cvmfs mountpoint
        # (e.g. HPCs) and relying on a shared file system (e.g. GPFS).
        (path, os_id)
        for path, os_id in APPTAINER_ROOTS
        if os.path.exists(path)
    ]
    # In some situations (e.g. /eos/user/l/lhcbsoft) the real path is not the
    # same as the path we are given, so we need to resolve the path to avoid
    # apptainer from failing to set the current working directory correctly.
    cwd = os.path.realpath(os.getcwd())

    # Having PWD set causes some versions of apptainer to ignore the current
    # working directory and, if the path in PWD contains symlinks, apptainer can
    # fail to set the current working directory correctly and default to $HOME.
    env = os.environ.copy()
    env.pop("PWD", None)

    try:
        wrapper = [
            container_executable,
            "--silent",
            "exec",
            "--bind",
            "/cvmfs",
            "--bind",
            cwd,
            "--userns",
        ]
        if "X509_USER_PROXY" in os.environ and os.path.isfile(
            os.environ["X509_USER_PROXY"]
        ):
            wrapper += ["--bind", os.environ["X509_USER_PROXY"]]
        test_cmd = wrapper + [available_roots[0][0], "pwd"]
        # we try to convince the container to start in the directory we bind-mount
        container_dir = check_output(test_cmd, stderr=STDOUT, cwd=cwd, env=env).decode()
    except (CalledProcessError, OSError, IndexError):
        return []

    # If setting up the bind mounts fails it will quietly change the
    # current working directory to be $HOME so fail if the current working
    # directory is not what we expect
    if cwd == container_dir.strip():
        return available_roots
    else:
        return []
