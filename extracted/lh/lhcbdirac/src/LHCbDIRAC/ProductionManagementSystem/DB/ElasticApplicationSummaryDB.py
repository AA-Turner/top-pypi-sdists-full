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
""" Module containing a front-end to the ElasticSearch-based ElasticApplicationSummaryDB.
"""

from DIRAC import gConfig
from DIRAC.ConfigurationSystem.Client.PathFinder import getDatabaseSection
from DIRAC.ConfigurationSystem.Client.Helpers import CSGlobals
from LHCbDIRAC.ProductionManagementSystem.DB.ElasticMCStatsDBBase import ElasticMCStatsDBBase

name = "ElasticApplicationSummaryDB"

mapping = {
    "properties": {
        "wmsID": {"type": "long"},
        "ProductionID": {"type": "integer"},
        "JobID": {"type": "integer"},
        # TODO
    }
}


class ElasticApplicationSummaryDB(ElasticMCStatsDBBase):
    def __init__(self):
        """Standard Constructor"""

        section = getDatabaseSection("ProductionManagement", "ElasticApplicationSummaryDB")
        indexPrefix = gConfig.getValue(f"{section}/IndexPrefix", CSGlobals.getSetup()).lower()

        # Connecting to the ES cluster
        super().__init__(name, "ProductionManagement/ElasticApplicationSummaryDB", indexPrefix)

        self.indexName = f"{self.getIndexPrefix()}_{name.lower()}"
        # Verifying if the index is there, and if not create it
        if not self.client.indices.exists(self.indexName):
            result = self.createIndex(self.indexName, mapping, period=None)
            if not result["OK"]:
                self.log.error(result["Message"])
                raise RuntimeError(result["Message"])
            self.log.always("Index created:", self.indexName)

        self.dslSearch = self._Search(self.indexName)
