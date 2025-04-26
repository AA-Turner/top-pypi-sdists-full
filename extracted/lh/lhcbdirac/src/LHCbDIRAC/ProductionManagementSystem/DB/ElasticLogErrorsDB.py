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
""" Module containing a front-end to the OpenSearch-based ElasticLogErrorsDB.

    Here we define a mapping which is taken from a list of log errors.
"""

from DIRAC import S_OK, gConfig
from DIRAC.ConfigurationSystem.Client.Helpers import CSGlobals
from DIRAC.ConfigurationSystem.Client.PathFinder import getDatabaseSection
from DIRAC.Core.Utilities.ReturnValues import DReturnType
from LHCbDIRAC.ProductionManagementSystem.DB.ElasticMCStatsDBBase import ElasticMCStatsDBBase

name = "ElasticLogErrorsDB"

mapping = {
    "properties": {
        "wmsID": {"type": "long"},
        "ProductionID": {"type": "long"},
        "JobID": {"type": "long"},
        "Application": {"type": "keyword"},
        "ApplicationVersion": {"type": "keyword"},
        "Errors": {"type": "long"},
        "ErrorType": {"type": "keyword"},
        "timestamp": {"type": "date"},
    }
}


class ElasticLogErrorsDB(ElasticMCStatsDBBase):
    def __init__(self) -> None:
        """Standard Constructor"""
        try:
            section = getDatabaseSection("ProductionManagement", "ElasticLogErrorsDB")
            indexPrefix = gConfig.getValue(f"{section}/IndexPrefix", CSGlobals.getSetup()).lower()

            # Connecting to the ES cluster
            super().__init__(name, "ProductionManagement/ElasticLogErrorsDB", indexPrefix)
        except Exception as ex:
            self.log.error("Can't connect to ElasticLogErrorsDB", repr(ex))
            raise RuntimeError("Can't connect to ElasticLogErrorsDB")

        self.indexName = f"{self.getIndexPrefix()}_{name.lower()}"
        # Verifying if the index is there, and if not create it
        if not self.client.indices.exists(self.indexName):
            result = self.createIndex(self.indexName, mapping, period=None)
            if not result["OK"]:
                self.log.error(result["Message"])
                raise RuntimeError(result["Message"])
            self.log.always("Index created:", self.indexName)

        self.dslSearch = self._Search(self.indexName)

    def set(self, data: list[dict]) -> DReturnType[int]:
        """
        Inserts data into ES index

        :param data: data to be inserted
        :returns: S_OK/S_ERROR as result of indexing
        """
        self.log.debug(
            self.__class__.__name__,
            f".set(): inserting data in {self.indexName}",  # pylint: disable=no-member
        )
        result = self.bulk_index(
            indexPrefix=self.indexName, data=data, mapping=mapping, period=None
        )  # pylint: disable=no-member
        if not result["OK"]:
            self.log.error("ERROR: Could not insert data", result["Message"])
        return result

    def get(self, productionID: int) -> DReturnType[list]:
        """
        Retrieves data from ES index

        :param productionID: production ID
        :returns: S_OK/S_ERROR as result of get
        """
        resultList = []
        query = {"query": {"term": {"ProductionID": str(productionID)}}}  # no scoring

        self.log.debug(self.__class__.__name__, f".get(): retrieving data from {self.indexName}")

        res = self.query(index=self.indexName, query=query)
        if not res["OK"]:
            return res
        res = res["Value"]["hits"]["hits"]
        for doc in res:
            resultList.append(doc["_source"])
        return S_OK(resultList)
