###############################################################################
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""LHCbDIRAC Job DB.

Extends the DIRAC JobDB with minor things
"""
from DIRAC.WorkloadManagementSystem.DB.JobDB import JobDB as DIRACJobDB


class JobDB(DIRACJobDB):
    """Extension of the DIRAC Job DB."""

    def __init__(self, *args, **kwargs):
        """The standard constructor takes the database name (dbname) and the name
        of the configuration section (dbconfig)"""
        DIRACJobDB.__init__(self, *args, **kwargs)
        self.jdl2DBParameters += ["runNumber"]
