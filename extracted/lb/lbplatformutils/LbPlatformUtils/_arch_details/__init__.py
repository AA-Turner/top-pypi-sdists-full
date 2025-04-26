#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
def defs():
    """
    Return a dict from micro architecture name to flags (instructions sets)
    available on that type of CPU.
    """
    from collections import OrderedDict

    from LbPlatformUtils._arch_details import _arm, _intel

    data = OrderedDict()
    for arch in (_intel, _arm):
        data.update(arch.defs())
    return data
