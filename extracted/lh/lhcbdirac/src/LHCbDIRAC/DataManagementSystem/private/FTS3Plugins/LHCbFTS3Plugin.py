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
"""
    This module implements the default behavior for the FTS3Agent for TPC and source SE selection
"""
import random
import itertools
import re
from DIRAC import S_OK, S_ERROR, gLogger
from DIRAC.Core.Utilities.ReturnValues import returnSingleResult
from DIRAC.DataManagementSystem.Client.DataManager import DataManager
from DIRAC.DataManagementSystem.Utilities.DMSHelpers import DMSHelpers
from DIRAC.DataManagementSystem.private.FTS3Plugins.DefaultFTS3Plugin import DefaultFTS3Plugin
from DIRAC.Resources.Storage.StorageElement import StorageElement

sLog = gLogger.getSubLogger(__name__)


class LHCbFTS3Plugin(DefaultFTS3Plugin):
    @staticmethod
    def _isRalAntaresEchoStaging(sourceSEName=None, destSEName=None):
        """Check if the transfer goes from Antares to Echo at RAL"""
        try:
            srcSE = StorageElement(sourceSEName)
            srcBaseSEName = srcSE.options.get("BaseSE")
            dstSE = StorageElement(destSEName)
            dstBaseSEName = dstSE.options.get("BaseSE")

            if srcBaseSEName in ("RAL-ANTARES-DATACHALLENGE", "RAL-ANTARES"):
                if dstBaseSEName in ("RAL-ECHO", "RAL-ECHO-DATACHALLENGE"):
                    return True

        except Exception:
            pass

        return False

    def selectTPCProtocols(self, ftsJob=None, sourceSEName=None, destSEName=None, **kwargs):
        """Specialised TPC selection"""

        if not sourceSEName:
            sourceSEName = ftsJob.sourceSE
        if not destSEName:
            destSEName = ftsJob.targetSE

        # # if we stage from Antares to Echo, return root as TPC
        # if self._isRalAntaresEchoStaging(sourceSEName=sourceSEName, destSEName=destSEName):
        #     return ["root"]

        return super().selectTPCProtocols(ftsJob=ftsJob, sourceSEName=sourceSEName, destSEName=destSEName, **kwargs)

    def selectSourceSE(self, ftsFile, replicaDict, allowedSources):
        """
        This is basically a copy/paste of the parent method, with the exception
        of prefering local staging.
        """

        allowedSourcesSet = set(allowedSources) if allowedSources else set()

        # If we have a restriction, apply it, otherwise take all the replicas
        allowedReplicaSource = (set(replicaDict) & allowedSourcesSet) if allowedSourcesSet else replicaDict
        if not allowedReplicaSource:
            sLog.warn(
                "Incompatible restriction, trying to find more replicas",
                f"{ftsFile.lfn=}, {replicaDict=}, {allowedSources=}",
            )

            # Query again the replicas in order to prefer disks
            # as this is not the case when specifying preferd sources
            allowedReplicaSource = returnSingleResult(
                DataManager().getActiveReplicas(ftsFile.lfn, getUrl=False, preferDisk=True)
            ).get("Value")
            if not allowedReplicaSource:
                sLog.warn(
                    "Could not retrieve replicas again, taking all replicas",
                    f"{ftsFile.lfn=} {replicaDict=}, {allowedSources=}",
                )
                allowedReplicaSource = replicaDict

        # If we have a replica at the same site as the destination
        # use that one
        # This is mostly done in order to favor local staging
        #
        # We go with the naive assumption that the site name
        # is always the first part of the SE name, separated
        # by either a - or a _ (like `_MC-DST`)
        # (I know there are "proper tools" for checking if a SE is on the same site
        # but since we are in the sheltered LHCb only environment, I can do that
        # sort of optimization)
        targetSite = re.split("-|_", ftsFile.targetSE)[0]
        sameSiteSE = [srcSE for srcSE in allowedReplicaSource if targetSite in srcSE]
        if sameSiteSE:
            allowedReplicaSource = sameSiteSE

        randSource = random.choice(list(allowedReplicaSource))  # one has to convert to list
        return randSource

    def inferFTSActivity(self, ftsOperation, rmsRequest, rmsOperation):
        """
        Tries to infer the FTS Activity
        """

        ### Data Challenge activity
        # All the tests with data challenges are done
        # on SE with '-DC-' in their name
        targetSEs = rmsOperation.targetSEList
        if any("-DC-" in se for se in targetSEs):
            return "Data Challenge"

        return super().inferFTSActivity(ftsOperation, rmsRequest, rmsOperation)
