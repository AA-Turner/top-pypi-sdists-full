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
import os
import sys

import importlib_resources
from importlib_metadata import PackageNotFoundError, version

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    # package is not installed
    __version__ = "unknown"

DEFAULT_SITEROOT = "/cvmfs/lhcb.cern.ch/lib"


def computeDefaultSiteRoot():
    if "MYSITEROOT" in os.environ:
        mysiteroot = os.environ["MYSITEROOT"]
    elif "VO_LHCB_SW_DIR" in os.environ:
        mysiteroot = os.path.join(os.environ["VO_LHCB_SW_DIR"], "lib")
    elif "VIRTUAL_ENV" in os.environ:
        mysiteroot = os.environ["VIRTUAL_ENV"]
        # the venv is usually in #MYSITEROOT/var/..., so we try to deduce it
        head, tail = mysiteroot, "none"
        while tail and tail != "var":
            head, tail = os.path.split(head)
        if tail:
            # 'var' was found in the path, so the parent directory is the root
            mysiteroot = head
    elif os.path.isdir(DEFAULT_SITEROOT):
        mysiteroot = DEFAULT_SITEROOT
    else:
        sys.stderr.write("error: not valid siteroot provided\n")
        sys.exit(1)
    return mysiteroot


def which(name, path=None):
    """
    Locate a file in the path.
    """
    if path is None:
        path = os.environ.get("PATH", "")
    if isinstance(path, str):
        path = path.split(os.path.pathsep)
    for p in path:
        fp = os.path.join(p, name)
        if os.path.exists(fp):
            return fp
    return None


def resource_string(name):
    """
    Helper to get data stored with the package.
    """
    ref = importlib_resources.files(__name__).joinpath("data/" + name)
    return ref.read_text()


def getProjectNames():
    """
    Return an iterator over the known project names.
    """
    for line in resource_string("projects.txt").splitlines():
        # remove comments and whitespaces
        project = line.split("#", 1)[0].strip()
        if project:
            yield project


def getPackageNames():
    """
    Return an iterator over the known project names.
    """
    for line in resource_string("packages.txt").splitlines():
        # remove comments and whitespaces
        package = line.split("#", 1)[0].strip()
        if package:
            yield package


_PROJECT_NAMES = None


def fixProjectCase(project):
    """
    Convert a project name to its canonical case, if known, otherwise return
    the string unchanged.

    >>> fixProjectCase('gaudi')
    'Gaudi'
    >>> fixProjectCase('DAvinci')
    'DaVinci'
    >>> fixProjectCase('UnKnown')
    'UnKnown'
    """
    global _PROJECT_NAMES
    if _PROJECT_NAMES is None:
        _PROJECT_NAMES = {name.lower(): name for name in getProjectNames()}
    return _PROJECT_NAMES.get(project.lower(), project)
