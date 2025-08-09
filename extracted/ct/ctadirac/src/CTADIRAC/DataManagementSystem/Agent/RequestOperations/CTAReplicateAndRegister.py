""" CTA specific ReplicateAndRegister class to handle lfns starting with both the old and new VO name """

# # imports
import re
from collections import defaultdict

# # imports from DIRAC
from DIRAC import S_ERROR, S_OK, gLogger
from DIRAC.Core.Utilities.Adler import compareAdler, hexAdlerToInt, intAdlerToHex
from DIRAC.DataManagementSystem.Agent.RequestOperations.ReplicateAndRegister import (
    ReplicateAndRegister,
)
from DIRAC.DataManagementSystem.Client.DataManager import DataManager
from DIRAC.Resources.Catalog.FileCatalog import FileCatalog
from DIRAC.Resources.Storage.StorageElement import StorageElement


def filterReplicas(opFile, logger=None, opSources=None, activeReplicas=None):
    """filter out banned/invalid source SEs

    :param list opSources: list of SE names to which limit the possible sources
    :param dict activeReplicas: the result of dm.getActiveReplicas(*)["Value"]. Used as a cache

    :returns: Valid list of SEs valid as source

    """
    ## LA: Added for CTADIRAC Legacy
    voName = opFile.LFN.split("/")[1]
    dataManager = DataManager(vo=voName)
    if logger is None:
        logger = gLogger

    log = logger.getSubLogger("filterReplicas")
    result = defaultdict(list)

    activeReplicas = _getActiveReplicas(opFile, dataManager, activeReplicas, log)

    _checkReplicaExists(opFile, activeReplicas)

    replicas = activeReplicas["Successful"].get(opFile.LFN, {})

    # If user set sourceSEs, only consider those replicas
    if opSources:
        replicas = {x: y for (x, y) in replicas.items() if x in opSources}

    noReplicas = False
    if not replicas:
        noReplicas = _handleNoReplicas(dataManager, opFile, result, log)
        if isinstance(noReplicas, dict):  # Means an error was returned
            return noReplicas

    _setFileChecksumIfMissing(opFile)
    # If no replica was found, return what we collected as information
    if not replicas:
        return S_OK(result)

    for repSEName in replicas:
        ## LA: Added for CTA-DIRAC Legacy
        _processReplica(opFile, voName, repSEName, result, log, noReplicas)

    return S_OK(result)


def _getActiveReplicas(opFile, dataManager, activeReplicas, log):
    if activeReplicas:
        return activeReplicas

    res = dataManager.getActiveReplicas(opFile.LFN, getUrl=False, preferDisk=True)
    if not res["OK"]:
        log.error(f"Failed to get active replicas {res['Message']}")
        return res

    return res["Value"]


def _checkReplicaExists(opFile, activeReplicas):
    reNotExists = re.compile(r".*such file.*")
    failed = activeReplicas["Failed"].get(opFile.LFN, "")
    if reNotExists.match(failed.lower()):
        opFile.Status = "Failed"
        opFile.Error = failed
        return S_ERROR(failed)


def _handleNoReplicas(dataManager, opFile, result, log):
    allReplicas = dataManager.getReplicas(opFile.LFN, getUrl=False)
    if not allReplicas["OK"]:
        return allReplicas

    allReplicas = allReplicas["Value"]["Successful"].get(opFile.LFN, {})
    if not allReplicas:
        result["NoReplicas"].append(None)
        noReplicas = True
    else:
        # There are replicas but we cannot get metadata because the replica is not active
        result["NoActiveReplicas"] += list(allReplicas)
        noReplicas = False
    log.verbose(
        f"File has no{'' if noReplicas else ' active'} replica in File Catalog",
        opFile.LFN,
    )
    return noReplicas


def _setFileChecksumIfMissing(opFile):
    if not opFile.Checksum or hexAdlerToInt(opFile.Checksum) is False:
        # Set Checksum to FC checksum if not set in the request
        fcMetadata = FileCatalog().getFileMetadata(opFile.LFN)
        fcChecksum = (
            fcMetadata.get("Value", {})
            .get("Successful", {})
            .get(opFile.LFN, {})
            .get("Checksum")
        )
        # Replace opFile.Checksum if it doesn't match a valid FC checksum
        if fcChecksum:
            if hexAdlerToInt(fcChecksum) is not False:
                opFile.Checksum = fcChecksum
                opFile.ChecksumType = fcMetadata["Value"]["Successful"][opFile.LFN].get(
                    "ChecksumType", "Adler32"
                )
            else:
                opFile.Checksum = None


def _processReplica(opFile, voName, repSEName, result, log, noReplicas):
    ## LA: Added for CTA-DIRAC Legacy
    repSEMetadata = StorageElement(repSEName, vo=voName).getFileMetadata(opFile.LFN)
    error = repSEMetadata.get(
        "Message", repSEMetadata.get("Value", {}).get("Failed", {}).get(opFile.LFN)
    )
    if error:
        log.warn(
            f"unable to get metadata at {repSEName} for {opFile.LFN}",
            error.replace("\n", ""),
        )
        if "File does not exist" in error or "No such file" in error:
            result["NoReplicas"].append(repSEName)
        else:
            result["NoMetadata"].append(repSEName)
    elif not noReplicas:
        repSEMetadata = repSEMetadata["Value"]["Successful"][opFile.LFN]
        seChecksum = repSEMetadata.get("Checksum")

        ## LA: Bug fix for empty checksum
        if seChecksum == "":
            seChecksum = hexAdlerToInt(False)
        else:
            seChecksum = hexAdlerToInt(seChecksum)
        # As from here seChecksum is an integer or False, not a hex string!
        if seChecksum is False and opFile.Checksum:
            result["NoMetadata"].append(repSEName)
        elif not seChecksum and opFile.Checksum:
            opFile.Checksum = None
            opFile.ChecksumType = None
        elif seChecksum and (not opFile.Checksum or opFile.Checksum == "False"):
            # Use the SE checksum (convert to hex) and force type to be Adler32
            opFile.Checksum = intAdlerToHex(seChecksum)
            opFile.ChecksumType = "Adler32"
        if (
            not opFile.Checksum
            or not seChecksum
            or compareAdler(intAdlerToHex(seChecksum), opFile.Checksum)
        ):
            # # All checksums are OK
            result["Valid"].append(repSEName)
        else:
            log.warn(
                " %s checksum mismatch, FC: '%s' @%s: '%s'"
                % (
                    opFile.LFN,
                    opFile.Checksum,
                    repSEName,
                    intAdlerToHex(seChecksum),
                )
            )
            result["Bad"].append(repSEName)
    else:
        # If a replica was found somewhere, don't set the file as no replicas
        result["NoReplicas"] = []


class CTAReplicateAndRegister(ReplicateAndRegister):
    def _filterReplicas(self, opFile, activeReplicas):
        """filter out banned/invalid source SEs"""
        return filterReplicas(
            opFile,
            logger=self.log,
            opSources=self.operation.sourceSEList,
            activeReplicas=activeReplicas,
        )
