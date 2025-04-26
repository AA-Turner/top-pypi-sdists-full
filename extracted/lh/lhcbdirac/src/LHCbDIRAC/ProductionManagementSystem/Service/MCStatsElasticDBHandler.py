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
""" DIRAC service that expose access for MCStatsElasticDBs (several ElasticSearch DBs)
"""
from DIRAC import S_OK
from DIRAC.Core.DISET.RequestHandler import RequestHandler
from LHCbDIRAC.ProductionManagementSystem.DB.ElasticApplicationSummaryDB import ElasticApplicationSummaryDB
from LHCbDIRAC.ProductionManagementSystem.DB.ElasticLogErrorsDB import ElasticLogErrorsDB
from LHCbDIRAC.ProductionManagementSystem.DB.ElasticPrMonDB import ElasticPrMonDB


class MCStatsElasticDBHandler(RequestHandler):
    """Tiny service for setting/getting/removing data from ElasticSearch MCStats DBs"""

    @classmethod
    def initializeHandler(cls, serviceInfoDict):
        elasticApplicationSummaryDB = ElasticApplicationSummaryDB()
        elasticLogErrorsDB = ElasticLogErrorsDB()
        elasticPrMonDB = ElasticPrMonDB()

        cls.db = {
            "XMLSummary": elasticApplicationSummaryDB,
            "errors": elasticLogErrorsDB,
            "prMon": elasticPrMonDB,
        }

        return S_OK()

    types_set = [str, (dict, list)]

    def export_set(self, typeName, data):
        if isinstance(data, dict):
            data = [data]
        return self.db[typeName].set(data)

    types_get = [str, (str, int)]

    def export_get(self, typeName, productionID):
        return self.db[typeName].get(productionID)

    types_remove = [str, (str, int)]

    def export_remove(self, typeName, productionID):
        return self.db[typeName].remove(productionID)
