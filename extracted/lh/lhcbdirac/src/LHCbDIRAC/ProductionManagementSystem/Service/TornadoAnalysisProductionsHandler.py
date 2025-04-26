###############################################################################
# (c) Copyright 2021 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""Provides access to Analysis Productions specific functionality

For more information see :py:mod:`.AnalysisProductionsClient`.
"""
from datetime import datetime
from itertools import chain

from DIRAC import gConfig, gLogger
from DIRAC.Core.Tornado.Server.TornadoService import TornadoService
from DIRAC.Core.Security.Properties import PRODUCTION_MANAGEMENT
from DIRAC.Core.Utilities.ReturnValues import returnValueOrRaise, convertToReturnValue
from DIRAC.DataManagementSystem.Client.DataManager import DataManager
from DIRAC.Resources.Storage.StorageElement import StorageElement
from LHCbDIRAC.BookkeepingSystem.Client.BookkeepingClient import BookkeepingClient
from LHCbDIRAC.TransformationSystem.Client.TransformationClient import TransformationClient
from LHCbDIRAC.ProductionManagementSystem.DB.AnalysisProductionsDB import AnalysisProductionsDB

optDate = (type(None), datetime)
optString = (type(None), str)
optList = (type(None), list)
optBool = (type(None), bool)

sLog = gLogger.getSubLogger(__name__)
sLog._setOption("tornadoComponent", "ProductionManagement/TornadoAnalysisProduction")


class TornadoAnalysisProductionsHandler(TornadoService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def initializeHandler(cls, serviceInfoDict):
        """initialize handler"""
        cls._db = AnalysisProductionsDB(parentLogger=cls.log)

    types_listAnalyses = [optDate]

    @convertToReturnValue
    def export_listAnalyses(self, at_time):
        """See :meth:`~.AnalysisProductionsClient.listAnalyses`"""
        return self._db.listAnalyses(at_time=at_time)

    types_listAnalyses2 = [optDate]

    @convertToReturnValue
    def export_listAnalyses2(self, at_time):
        """See :meth:`~.AnalysisProductionsClient.listAnalyses2`"""
        return self._db.listAnalyses2(at_time=at_time)

    types_listRequests = [optDate]

    @convertToReturnValue
    def export_listRequests(self):
        """See :meth:`~.AnalysisProductionsClient.listRequests`"""
        return self._db.listRequests()

    types_getOwners = [str, str]

    @convertToReturnValue
    def export_getOwners(self, wg, analysis):
        """See :meth:`~.AnalysisProductionsClient.getOwners`"""
        return self._db.getOwners(wg=wg, analysis=analysis)

    types_setOwners = [str, str, list]

    @convertToReturnValue
    def export_setOwners(self, wg, analysis, owners):
        """See :meth:`~.AnalysisProductionsClient.setOwners`"""
        return self._db.setOwners(wg=wg, analysis=analysis, owners=owners)

    types_getProductions = [
        optString,
        optString,
        optString,
        optString,
        optString,
        bool,
        bool,
        bool,
        optDate,
        optBool,
        optBool,
    ]

    @convertToReturnValue
    def export_getProductions(
        self,
        wg,
        analysis,
        version,
        name,
        state,
        with_lfns,
        with_pfns,
        with_transformations,
        at_time,
        show_archived=False,
        require_has_publication=False,
    ):
        """See :meth:`~.AnalysisProductionsClient.getProductions`"""
        if (analysis or name or version) and wg is None:
            raise TypeError("wg must be specified when providing an analysis name or sample name/version")
        if with_pfns and not with_lfns:
            raise TypeError("with_pfns cannot be used without with_lfns")
        results = self._db.getProductions(
            wg=wg,
            analysis=analysis,
            version=version,
            name=name,
            state=state,
            at_time=at_time,
            show_archived=show_archived,
            require_has_publication=require_has_publication,
        )
        return _queryToResults(results, with_lfns, with_pfns, with_transformations)

    types_getArchivedRequests = [optString, bool, bool, bool]

    @convertToReturnValue
    def export_getArchivedRequests(self, state, with_lfns, with_pfns, with_transformations):
        """See :meth:`~.AnalysisProductionsClient.getArchivedRequests`"""
        if with_pfns and not with_lfns:
            raise TypeError("with_pfns cannot be used without with_lfns")
        results = self._db.getArchivedRequests(state=state)
        return _queryToResults(results, with_lfns, with_pfns, with_transformations)

    types_getTags = [optString, optString, optDate]

    @convertToReturnValue
    def export_getTags(self, wg, analysis, at_time):
        """See :meth:`~.AnalysisProductionsClient.getTags`"""
        return self._db.getTags(wg, analysis, at_time=at_time)

    types_getKnownAutoTags = []

    @convertToReturnValue
    def export_getKnownAutoTags(self):
        """See :meth:`~.AnalysisProductionsClient.getKnownAutoTags`"""
        return list(self._db.getKnownAutoTags())

    types_registerTransformations = [dict]

    @convertToReturnValue
    def export_registerTransformations(self, transforms):
        """See :meth:`~.AnalysisProductionsClient.registerTransformations`"""
        transforms = {int(k): v for k, v in transforms.items()}
        return self._db.registerTransformations(transforms)

    types_deregisterTransformations = [dict]

    @convertToReturnValue
    def export_deregisterTransformations(self, tIDs):
        """See :meth:`~.AnalysisProductionsClient.deregisterTransformations`"""
        tIDs = {int(k): v for k, v in tIDs.items()}
        return self._db.deregisterTransformations(tIDs)

    types_registerRequests = [list]

    @convertToReturnValue
    def export_registerRequests(self, requests):
        """See :meth:`~.AnalysisProductionsClient.registerRequests`"""
        results = self._db.registerRequests(requests)
        return _queryToResults(results, with_lfns=False, with_pfns=False, with_transformations=False)

    types_addRequestsToAnalysis = [str, str, list[tuple[int, str]]]

    @convertToReturnValue
    def export_addRequestsToAnalysis(self, wg, analysis, requests):
        """See :meth:`~.AnalysisProductionsClient.addRequestsToAnalysis`"""
        return self._db.addRequestsToAnalysis(wg, analysis, requests)

    types_archiveSamples = [list]

    @convertToReturnValue
    def export_archiveSamples(self, sample_ids):
        """See :meth:`~.AnalysisProductionsClient.archiveSamples`"""
        return self._db.archiveSamples(sample_ids)

    types_archiveSamplesAtSpecificTime = [list, datetime]

    @convertToReturnValue
    def export_archiveSamplesAtSpecificTime(self, sample_ids, archive_time):
        """See :meth:`~.AnalysisProductionsClient.archiveSamplesAtSpecificTime`"""
        return self._db.archiveSamplesAtSpecificTime(sample_ids, archive_time)

    types_setState = [dict]

    @convertToReturnValue
    def export_setState(self, newState):
        """See :meth:`~.AnalysisProductionsClient.setState`"""
        newState = {(int(k), ft): vv for k, v in newState.items() for ft, vv in v.items()}
        return self._db.setState(newState)

    types_setTags = [dict, dict]

    @convertToReturnValue
    def export_setTags(self, oldTags, newTags):
        """See :meth:`~.AnalysisProductionsClient.setTags`"""
        return self._db.setTags(oldTags, newTags)

    types_delayHousekeepingInteractionDue = [list, datetime]

    @convertToReturnValue
    def export_delayHousekeepingInteractionDue(self, samples, next_interaction_due):
        """See :meth:`~.AnalysisProductionsClient.delayHousekeepingInteractionDue`"""
        return self._db.delayHousekeepingInteractionDue(samples, next_interaction_due)

    types_getHousekeepingInteractionDueNow = []

    @convertToReturnValue
    def export_getHousekeepingInteractionDueNow(self):
        """See :meth:`~.AnalysisProductionsClient.getHousekeepingInteractionDueNow`"""
        return self._db.getHousekeepingInteractionDueNow()

    types_addPublication = [list, str]

    @convertToReturnValue
    def export_addPublication(self, samples, number):
        """See :meth:`~.AnalysisProductionsClient.addPublication`"""
        return self._db.addPublication(samples, number)

    types_getPublications = [optList]

    @convertToReturnValue
    def export_getPublications(self, sample_ids):
        """See :meth:`~.AnalysisProductionsClient.getPublications`"""
        return self._db.getPublications(sample_ids)


def _queryToResults(results, with_lfns, with_pfns, with_transformations):
    """Convert a query of Request or AP objects to a JSON compatible object"""
    p2tID = {
        (result["request_id"], result["filetype"]): {tInfo["id"]: tInfo["used"] for tInfo in result["transformations"]}
        for result in results
    }

    if with_lfns:
        lfns = _getOutputLFNs(p2tID)
        if with_pfns:
            replicas = _getReplicas(list(chain(*lfns.values())))

        for result in results:
            result["lfns"] = {} if with_pfns else []
            result["total_bytes"] = 0
            if with_pfns:
                result["available_bytes"] = 0
            for tInfo in result["transformations"]:
                for lfn, lfnMeta in lfns.get(tInfo["id"], {}).items():
                    result["total_bytes"] += lfnMeta["FileSize"]
                    if not with_pfns:
                        result["lfns"].append(lfn)
                    # TODO: Remove when https://github.com/pylint-dev/pylint/issues/9628 is fixed
                    elif lfn in replicas["Failed"]:  # pylint: disable=possibly-used-before-assignment
                        result["lfns"][lfn] = []
                        sLog.warn(
                            "Failed to get replicas for Analysis Production LFN",
                            "%s in rID=%s tID=%s: %s"
                            % (lfn, result["request_id"], tInfo["id"], replicas["Failed"][lfn]),
                        )
                    else:
                        result["lfns"][lfn] = [
                            pfn
                            for pfn in replicas["Successful"][lfn].values()
                            # Ignore entries with the value True as these are at unsupported SEs
                            if isinstance(pfn, str)
                        ]
                        if result["lfns"][lfn]:
                            result["available_bytes"] += lfnMeta["FileSize"]

    if with_transformations:
        tIDs = list(set(chain(*p2tID.values())))
        if tIDs:
            tClient = TransformationClient()
            retVal = tClient.getTransformations(
                condDict={"TransformationID": tIDs},
                limit=10000,
                columns=["TransformationID", "Status", "Type"],
            )
            extraTransInfos = {t["TransformationID"]: t for t in returnValueOrRaise(retVal)}
            # Query any transformation save for types without well defined input queries
            inputQueries = returnValueOrRaise(
                tClient.getBookkeepingQueries(
                    [tID for tID in tIDs if extraTransInfos[tID]["Type"] not in ["DerriviedAnalysisProduction"]]
                )
            )
            for tInfo in chain(*(r["transformations"] for r in results)):
                tInfo["status"] = extraTransInfos[tInfo["id"]]["Status"]
                tInfo["input_query"] = inputQueries.get(tInfo["id"], {})
    else:
        for result in results:
            del result["transformations"]

    return results


def _getOutputLFNs(pID2tID):
    sLog.info("Getting output LFNs")
    keys = [(tID, ft) for (_, ft), tIDs in pID2tID.items() for tID, used in tIDs.items() if used]
    lfns = {}
    if not keys:
        return lfns
    retVal = BookkeepingClient().getProductionFilesBulk(
        *map(list, zip(*keys, strict=True)),
        "ALL",
    )
    for tID, lfnMetadata in returnValueOrRaise(retVal).items():
        lfns[int(tID)] = {lfn: meta for lfn, meta in lfnMetadata.items() if meta["GotReplica"].lower().startswith("y")}
    return lfns


def _getReplicas(lfns):
    sLog.info("Getting replicas for", f"{len(lfns)} LFNs")
    replicas = returnValueOrRaise(DataManager().getReplicas(lfns, diskOnly=True, getUrl=False))
    for se in gConfig.getValue("/Resources/Sites/LCG/LCG.CERN.cern/SE", []):
        seLFNs = {lfn for lfn, replicaInfo in replicas["Successful"].items() if se in replicaInfo}
        if not seLFNs:
            continue
        sLog.info("Getting PFNs for", f"{len(seLFNs)} LFNs at {se}")
        result = returnValueOrRaise(StorageElement(se).getURL(list(seLFNs), protocol="root"))
        if result["Failed"]:
            raise NotImplementedError(result["Failed"])
        for lfn, pfn in result["Successful"].items():
            replicas["Successful"][lfn][se] = pfn
    return replicas
