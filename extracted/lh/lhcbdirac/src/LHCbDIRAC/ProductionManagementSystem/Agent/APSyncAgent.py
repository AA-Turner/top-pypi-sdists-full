###############################################################################
# (c) Copyright 2022 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""Agent to populate AnalysisProductionsDB"""
import ast
import xml.etree.ElementTree as etree
from collections import Counter, defaultdict
from typing import Any, Optional

from DIRAC.Core.Base.AgentModule import AgentModule
from DIRAC.Core.Utilities.ReturnValues import convertToReturnValue, returnValueOrRaise

from LHCbDIRAC.ProductionManagementSystem.Client.AnalysisProductionsClient import AnalysisProductionsClient
from LHCbDIRAC.TransformationSystem.Client.TransformationClient import TransformationClient
from LHCbDIRAC.ProductionManagementSystem.Client.ProductionRequestClient import ProductionRequestClient
from LHCbDIRAC.ProductionManagementSystem.Utilities.Utils import unpackOptionFile

AGENT_NAME = "ProductionManagement/APSyncAgent"
DONE_TRANSFORMATION_STATES = ["Archived", "Completed"]
REMOVED_TRANSFORMATION_STATES = ["Deleted", "Cleaned", "Cleaning", "New"]


class APSyncAgent(AgentModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Currently unused however if needed this agent could optimised to
        # update inactive samples less frequently
        self.wg = None
        self.analysis = None
        self.state = None
        self.apc = AnalysisProductionsClient()
        # Caches that are used as part of execution
        self._fileCounts: dict[int, dict[str, int]] = {}
        self._samples: list[dict[str, Any]] = {}

    @convertToReturnValue
    def execute(self):
        tIDs = self._updateAndListTranformIDs()
        # Populate the local cache of file counts
        self._updateFileCountCache(tIDs)

        self.log.info("Discovering known samples")
        retVal = self.apc.getProductions(
            wg=self.wg,
            analysis=self.analysis,
            state=self.state,
            with_lfns=True,
            with_pfns=True,
            with_transformations=True,
        )
        self._samples = returnValueOrRaise(retVal)
        self.log.verbose(
            "Transformation status counts",
            dict(Counter(t["status"] for s in self._samples for t in s["transformations"])),
        )

        self._updateRequestStates()
        self._handleArchivedRequests()

    def _updateAndListTranformIDs(self) -> set[int]:
        """Get the transformation IDs the productions that are being updated

        Metadata about transformations is cached in the AnalaysisProductionsDB.
        This is a workaround for the fact that extracting transformation
        metadata from the workflow XML is slow.
        """
        self.log.info("Updating registered transformations")
        retVal = self.apc.getProductions(
            wg=self.wg,
            analysis=self.analysis,
            state=self.state,
            with_lfns=False,
            with_pfns=False,
            with_transformations=True,
        )
        samples = returnValueOrRaise(retVal)
        tIDs = {tInfo["id"] for sample in samples for tInfo in sample["transformations"]}
        self.log.info("Checking for new transformations")
        newIDs = self._registerNewTransformations({s["request_id"] for s in samples}, tIDs)
        if newIDs:
            self.log.info("Found new transformations", f"({len(newIDs)}) {','.join(map(str, newIDs))}")
            tIDs |= newIDs
        return tIDs

    def _updateFileCountCache(self, tIDs: set[int]) -> None:
        """Populate a cache with the file counts for the given transformation IDs

        This method is used to fill ``self._fileCounts`` with a single RPC. This
        is considerably faster than calling ``TransformationClient().getCounters``
        more frequently.
        """
        self.log.info("Getting file counts for", f"{len(tIDs)} transformations")
        if not tIDs:
            self._fileCounts = {}
            return
        result = TransformationClient().getCounters(
            "TransformationFiles",
            ["TransformationID", "Status"],
            {"TransformationID": list(tIDs)},
        )
        statusDict = defaultdict(lambda: defaultdict(int, **{"Total": 0}))
        for attrDict, count in returnValueOrRaise(result):
            tID = attrDict["TransformationID"]
            status = attrDict["Status"]
            statusDict[tID][status] = count
            statusDict[tID]["Total"] += count
        # Loop over transformationIDs to ensure all IDs are included in the output
        self._fileCounts = {int(tID): dict(statusDict[int(tID)]) for tID in tIDs}

    def _updateRequestStates(self) -> None:
        """Update the cached status/progress in the AnalysisProductionsDB

        As getting the status of an AnalysisProduction is too slow the result
        is cached in the AnalysisProductions DB. This method takes the sample
        and computes the state so it can be added in the DB.
        """
        self.log.info("Checking status of", f"{len(self._samples)} Analysis Productions")
        summaryStats = Counter()
        samplesToUpdate = defaultdict(lambda: defaultdict(dict))  # dict[int, dict[str, Any]]
        for sample in self._samples:
            state, progress = self._sampleToState(sample)
            if state != sample["state"]:
                samplesToUpdate[sample["request_id"]][sample["filetype"]]["state"] = state
            if progress != sample.get("progress"):
                samplesToUpdate[sample["request_id"]][sample["filetype"]]["progress"] = progress
            summaryStats[state] += 1
        self.log.verbose("Analysis Productions statistics summary", repr(summaryStats))
        if samplesToUpdate:
            self.log.info("Updating state for", f"{len(samplesToUpdate)} Analysis Productions")
            returnValueOrRaise(self.apc.setState({k: dict(v) for k, v in samplesToUpdate.items()}))

    def _handleArchivedRequests(self) -> None:
        """Currently unused and just logs the number of archived requests"""
        archivedRequests = returnValueOrRaise(self.apc.getArchivedRequests())
        self.log.verbose("There are currently", f"{len(archivedRequests)} archived requests")

    def _sampleToState(self, sample) -> tuple[str, float | None]:
        """Compute the state and progress of a given sample for caching in the DB

        :returns: The string representation of the state and, if still running,
                  the fractional progress of the production.
        """
        if not sample["transformations"]:
            return "waiting", None
        # Use a list to define the progress so that if there are
        # N transformations each progresses the overall production by 100/N %
        progress = []
        for tInfo in sample["transformations"]:
            if tInfo["status"] in REMOVED_TRANSFORMATION_STATES:
                continue
            if tInfo["status"] in DONE_TRANSFORMATION_STATES:
                continue
            tID = tInfo["id"]
            fileCounts = self._fileCounts[tID]
            if fileCounts["Total"] == 0:
                progress += [0.0]
            elif fileCounts.get("Processed", 0) != fileCounts["Total"]:
                progress += [fileCounts.get("Processed", 0) / fileCounts["Total"]]
        if progress:
            return "active", sum(progress) / len(progress)
        if sample["available_bytes"] != sample["total_bytes"]:
            return "replicating", sample["available_bytes"] / sample["total_bytes"]
        return "ready", None

    def _registerNewTransformations(self, requestIDs: set, knownTransformIDs: set) -> set[int]:
        """Register new transformations in the AnalysisProductionsDB's cache

        :param requestIDs: Production request IDs that correspond to AnalysisProductions
        :param knownTransformIDs: Transformation IDs that are already registered
        :returns: ``set`` of the newly registered transformation IDs
        """
        if not requestIDs:
            return set()
        allTransforms = returnValueOrRaise(
            TransformationClient().getTransformations(
                {"TransformationFamily": list(requestIDs)},
                columns=["TransformationID", "Type", "Status", "TransformationFamily"],
                limit=10000,
            )
        )
        requestIDsToCheck = set()
        for tInfo in allTransforms:
            tID = tInfo["TransformationID"]

            if tInfo["Type"] not in ["WGProduction", "APPostProc", "Merge", "APMerge"]:
                self.log.debug(
                    "Skipping tInfo due to unknown type:",
                    f"{tInfo['Type']!r} id: {tID}",
                )
                continue

            if tInfo["Status"] in REMOVED_TRANSFORMATION_STATES:
                if tID in knownTransformIDs:
                    requestIDsToCheck.add(tInfo["TransformationFamily"])
            else:
                if tID not in knownTransformIDs:
                    requestIDsToCheck.add(tInfo["TransformationFamily"])

        if not requestIDsToCheck:
            return set()

        result = TransformationClient().getTransformations(
            {"TransformationFamily": list(requestIDsToCheck)},
            columns=["TransformationID", "Type", "Status", "Body", "TransformationFamily"],
            limit=10000,
        )

        prodProgress = returnValueOrRaise(ProductionRequestClient().getAllProductionProgress())
        newTransformations = defaultdict(lambda: defaultdict(list))
        toDeregister = defaultdict(lambda: defaultdict(list))

        tInfoByFamily = defaultdict(dict)
        for tInfo in returnValueOrRaise(result):
            tInfoByFamily[tInfo["TransformationFamily"]][tInfo["TransformationID"]] = tInfo

        for requestId in tInfoByFamily:
            inputQueries = returnValueOrRaise(
                TransformationClient().getBookkeepingQueries(
                    list(tInfoByFamily[requestId]),
                )
            )

            # First find the output filetypes of the request which are visible
            tInfoByFileType = defaultdict(list)
            for tInfo in tInfoByFamily[requestId].values():
                if tInfo["Status"] in REMOVED_TRANSFORMATION_STATES:
                    continue
                parameters = _paramsFromBody(tInfo["Body"])
                steps_info = parameters["BKProcessingPass"]
                for step_info in steps_info.values():
                    for filetype in step_info["OutputFileTypes"]:
                        if filetype["Visible"] == "Y":
                            tInfoByFileType[filetype["FileType"]].append(tInfo)

            # Now include the parent transfromations that are still in this request
            for filetype, tInfos in tInfoByFileType.items():
                if len(tInfos) != 1:
                    raise NotImplementedError(filetype, tInfos)
                tInfo = tInfos[0]
                while prod_id := inputQueries[tInfo["TransformationID"]].get("ProductionID"):
                    # If we find the input query specifies another transformation in this
                    # production request then include it in the transformations for this filetype
                    if tInfo := tInfoByFamily[requestId].get(prod_id):
                        tInfos.insert(0, tInfo)
                        continue

                # Now we know all of the transformations which produce this filetype
                # so we can add the to the ones we will register
                for tInfo in tInfos:
                    transformationID = int(tInfo["TransformationID"])
                    if transformationID in knownTransformIDs:
                        if tInfo["Status"] in REMOVED_TRANSFORMATION_STATES:
                            # Occasionally the transformations are buggy and then cleaned
                            # If this happeneds deregister them from the cache
                            toDeregister[int(tInfo["TransformationFamily"])][filetype].append(transformationID)
                            print("BAD", tInfo["TransformationFamily"])
                            continue
                        continue
                    requestID = int(tInfo["TransformationFamily"])

                    parameters = _paramsFromBody(tInfo["Body"])
                    steps = [
                        parameters["BKProcessingPass"][f"Step{i}"] for i in range(len(parameters["BKProcessingPass"]))
                    ]
                    if tInfo["Status"] in REMOVED_TRANSFORMATION_STATES:
                        # We don't want to bother caching cleaned transformations
                        continue
                    newTransformations[requestID][filetype] += [
                        {
                            "id": transformationID,
                            "used": bool(prodProgress[requestID][transformationID]["Used"]),
                            "steps": [
                                {
                                    "stepID": sInfo["BKStepID"],
                                    "application": sInfo["ApplicationName"] + "/" + sInfo["ApplicationVersion"],
                                    "extras": (sInfo.get("ExtraPackages") or "").split(";"),
                                    "options": unpackOptionFile(sInfo["OptionFiles"]),
                                }
                                for sInfo in steps
                            ],
                        }
                    ]

        if toDeregister:
            self.log.verbose("Deregistering", toDeregister)
            returnValueOrRaise(self.apc.deregisterTransformations({k: dict(v) for k, v in toDeregister.items()}))
        if newTransformations:
            self.log.verbose("Registering transformations for productions", list(toDeregister))
            returnValueOrRaise(self.apc.registerTransformations({k: dict(v) for k, v in newTransformations.items()}))
            return {t["id"] for fts in newTransformations.values() for ts in fts.values() for t in ts}


def _paramsFromBody(body: str) -> dict[str, Any]:
    """Extract Paramters from the the XML in the Body of a Transformation

    This is done manually by reading the XML as the DIRAC machinery for this is
    overly complex and incredibly slow.
    """
    root = etree.fromstring(body)
    workflow = list(root.iter("Workflow"))
    if len(workflow) != 1:
        raise NotImplementedError()
    workflow = workflow.pop()
    parameters = {p.attrib["name"]: (p.attrib["type"], next(p.iter("value")).text) for p in workflow.iter("Parameter")}
    result = {}
    for name, (param_type, value) in parameters.items():
        if param_type in ["dict", "list"]:
            result[name] = ast.literal_eval(value)
        elif param_type in ["string", "JDL"]:
            result[name] = value
        else:
            raise NotImplementedError(name, param_type, value)
    return result
