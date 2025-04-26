###############################################################################
# (c) Copyright 2023 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import importlib_metadata as metadata


def test_entrypoints():
    """Make sure all console_scripts defined by LHCbDIRAC are importable."""
    errors = []
    for ep in metadata.entry_points(group="console_scripts"):
        if ep.module.startswith("LHCbDIRAC"):
            try:
                ep.load()
            except ModuleNotFoundError as e:
                errors.append(str(e))
    assert not errors, errors
