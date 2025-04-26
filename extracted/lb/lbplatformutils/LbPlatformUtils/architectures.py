#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# (c) Copyright 2019-2024 CERN                                                #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""
Module to host definition of architecture names in terms of supported
instruction sets.
"""
import LbPlatformUtils._arch_details

ARCH_DEFS = LbPlatformUtils._arch_details.defs()


def _compatible_archs(flags, up):
    """
    Helper to match compatible architectures.

    If 'up' is True, we return the included architectures, if False we return
    the including.
    """
    flags = set(flags)
    matches = flags.issuperset if up else flags.issubset
    for name, available_flags in ARCH_DEFS.items():
        if matches(available_flags):
            yield name


def get_supported_archs(host_flags):
    """
    Return an iterable over the list of architecture names that can be run
    on a host with the given list of microarch flags.

    >>> list(get_supported_archs(ARCH_DEFS['nehalem']))
    ['nehalem', 'x86_64_v2', 'core2', 'x86_64']
    >>> list(get_supported_archs(['dummy']))
    []
    """
    for a in _compatible_archs(host_flags, True):
        yield a


def get_compatible_archs(target_flags):
    """
    Return an iterable over the list of architecture names that can run
    a binary compiled for with the given list of microarch flags.

    >>> list(get_compatible_archs(['avx2']))
    ['cannonlake', 'skylake_avx512', 'x86_64_v4', 'skylake', 'broadwell', 'haswell', 'x86_64_v3']
    >>> list(get_compatible_archs(['sha_ni']))
    ['cannonlake']
    """
    for a in _compatible_archs(target_flags, False):
        yield a
