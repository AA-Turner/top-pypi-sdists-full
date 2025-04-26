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
"""Module holding MCStatsClient class."""
from DIRAC.Core.Base.Client import Client, createClient
from DIRAC.Core.Utilities.ReturnValues import DReturnType


@createClient("ProductionManagement/MCStatsElasticDB")
class MCStatsClient(Client):
    """Client for MCStatsElasticDB"""

    def __init__(self, **kwargs):
        """simple constructor."""

        super().__init__(**kwargs)
        self.setServer("ProductionManagement/MCStatsElasticDB")

    def set(self, typeName: str, data: dict) -> DReturnType:
        """set some data in a certain type.

        :params typeName: type name (e.g. 'errors')
        :params data: dictionary of data to insert

        :returns: S_OK/S_ERROR
        """
        return self._getRPC().set(typeName, data)

    def get(self, typeName: str, productionID: int) -> DReturnType:
        """get per production ID

        :params typeName: type name (e.g. 'errors')
        :params productionID: production ID
        """
        return self._getRPC().get(typeName, productionID)

    def remove(self, typeName: str, productionID: int) -> DReturnType:
        """remove data for productionID.

        :params typeName: type name (e.g. 'errors')
        :params productionID: production ID
        """
        return self._getRPC().remove(typeName, productionID)
