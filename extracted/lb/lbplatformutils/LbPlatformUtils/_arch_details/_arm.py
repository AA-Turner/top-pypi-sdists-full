###############################################################################
# (c) Copyright 2024 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""
Code used to generate the microarch -> flags dictionary for Intel CPUs.
"""


def defs():
    from collections import OrderedDict

    # Data based on the information found at
    # https://javathunderx.blogspot.com/2018/11/cheat-sheet-for-cpuinfo-features-on.html
    data = [("aarch64", [])]
    data.append(
        (
            "armv8_a",
            data[-1][1] + ["fp", "asimd", "evtstrm", "aes", "pmull", "sha1", "sha2"],
        )
    )
    data.append(("armv8.1_a", data[-1][1] + ["crc32", "atomics", "asimdrdm"]))
    data.append(("armv8.2_a", data[-1][1] + ["dcpop"]))
    data.append(("armv8.3_a", data[-1][1] + ["jscvt", "lrcpc"]))
    data.reverse()
    return OrderedDict((k, set(v + ["aarch64"])) for k, v in data)
