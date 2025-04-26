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
import random
import string

from DIRAC.Core.Utilities.ReturnValues import returnValueOrRaise


def test_file_types_basic(bkdb):
    ftype = "".join(random.choices(string.ascii_uppercase, k=10)) + ".ROOT"
    assert (ftype, "Some description") not in returnValueOrRaise(bkdb.getAvailableFileTypes())
    returnValueOrRaise(bkdb.insertFileTypes(ftype, "Some description", "ROOT"))
    assert (ftype, "Some description") in returnValueOrRaise(bkdb.getAvailableFileTypes())
