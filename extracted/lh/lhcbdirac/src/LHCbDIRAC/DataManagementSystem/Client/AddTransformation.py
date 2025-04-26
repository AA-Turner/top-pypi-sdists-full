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
"""Actual engine for adding a DM transformation, called by dirac-dms-add-
Transformation."""
import os
import json
from collections import defaultdict

import DIRAC
from DIRAC import gLogger
from DIRAC.Core.Base.Script import Script
from DIRAC.Core.Utilities.List import breakListIntoChunks
from DIRAC.Core.Utilities.ObjectLoader import ObjectLoader

from LHCbDIRAC.TransformationSystem.Client.Transformation import Transformation
from LHCbDIRAC.TransformationSystem.Client.TransformationClient import TransformationClient
from LHCbDIRAC.BookkeepingSystem.Client.BookkeepingClient import BookkeepingClient
from LHCbDIRAC.BookkeepingSystem.Client.BKQuery import getProcessingPasses, BKQuery
from LHCbDIRAC.ProductionManagementSystem.Client.ProductionRequestClient import ProductionRequestClient
from LHCbDIRAC.TransformationSystem.Utilities.PluginUtilities import getRemovalPlugins, getReplicationPlugins
from LHCbDIRAC.DataManagementSystem.Utilities.FCUtilities import chown
from LHCbDIRAC.DataManagementSystem.Client.DMScript import ProgressBar


def _checkMCReplication(bkPaths):
    """
    Check all MC replication transformations and list those that are obsolete
    """
    # Check only against Idle transformations
    res = TransformationClient().getTransformations(
        {"TransformationGroup": "LHCbMCDSTBroadcastRandom", "Status": ["Idle"]}
    )
    if not res["OK"]:
        gLogger.fatal("Error getting transformations", res["Message"])
        DIRAC.exit(1)
    transPaths = [(dt["TransformationID"], dt["TransformationName"].replace("Replication-", "")) for dt in res["Value"]]
    gLogger.notice(f"Checking {len(transPaths)} transformations against {len(bkPaths)} active BK paths")
    # Only keep BK paths
    transPaths = [trans for trans in transPaths if trans[1].startswith("/MC/")]
    obsoleteTrans = []
    for transID, path in transPaths:
        # Check if name ends with -<number>
        xx = path.split("-")
        if xx[-1].isdigit():
            path = "-".join(xx[:-1])
        if path not in bkPaths:
            obsoleteTrans.append(transID)
    return obsoleteTrans


def getTransformationName(transName, unique):
    """
    Get a transformation name from a base name
    If unique is requested, return None if already exists
    """
    tName = transName
    trial = 0
    transClient = TransformationClient()
    while True:
        # Check if there is already a transformation with that name
        res = transClient.getTransformation(tName)
        if res["OK"]:
            # Transformation already exists
            if unique:
                # If unique is required and the transformation is not in a final status, give up
                if res["Value"]["Status"] not in (
                    "Archived",
                    "Cleaned",
                    "Cleaning",
                    "Deleted",
                    "TransformationCleaned",
                ):
                    tName = None
                    gLogger.notice(
                        "Transformation %s already exists with ID %d, status %s"
                        % (transName, res["Value"]["TransformationID"], res["Value"]["Status"])
                    )
                    break
            trial += 1
            # Check again with new name
            tName = transName + "-" + str(trial)
        else:
            # Transformation doesn't exist, OK
            break
    return tName


def executeAddTransformation(pluginScript):
    """Method for actually adding a DM transformation It takes its options and
    argument values from pluginScript."""
    test = False
    start = False
    force = False
    invisible = False
    fcCheck = True
    unique = False
    bkQuery = None
    depth = None
    userGroup = None
    listProcessingPasses = False
    mcVersionSet = None
    nameOption = None
    checkMCReplication = False
    bodyPlugin = None
    transBody = None

    switches = Script.getUnprocessedSwitches()
    for opt, val in switches:
        if opt in ("s", "Start"):
            start = True
        elif opt == "Test":
            test = True
        elif opt == "Force":
            force = True
        elif opt == "SetInvisible":
            invisible = True
        elif opt == "NoFCCheck":
            fcCheck = False
        elif opt == "Unique":
            unique = True
        elif opt == "Chown":
            userGroup = val.split("/")
            if len(userGroup) != 2 or not userGroup[1].startswith("lhcb_"):
                gLogger.fatal("Wrong user/group")
                DIRAC.exit(2)
        elif opt == "Depth":
            try:
                depth = int(val)
            except ValueError:
                gLogger.fatal("Illegal integer depth:", val)
                DIRAC.exit(2)
        elif opt == "ListProcessingPasses":
            listProcessingPasses = True
        elif opt == "Name":
            nameOption = val
        elif opt == "MCVersion":
            if not mcVersionSet:
                mcVersionSet = {x.lower() for x in val.split(",")}
        elif opt == "CheckMCReplication":
            # Force to check all versions
            mcVersionSet = {"all"}
            checkMCReplication = True
        elif opt == "BodyPlugin":
            bodyPlugin = val
        elif opt == "TransBody":
            transBody = val

    if bodyPlugin and transBody:
        gLogger.fatal("Cannot specify both BodyPlugin and TransBody")
        DIRAC.exit(1)
    if userGroup:
        from DIRAC.Core.Security.ProxyInfo import getProxyInfo

        res = getProxyInfo()
        if not res["OK"]:
            gLogger.fatal("Can't get proxy info", res["Message"])
            DIRAC.exit(1)
        properties = res["Value"].get("groupProperties", [])
        if "FileCatalogManagement" not in properties:
            gLogger.error("You need to use a proxy from a group with FileCatalogManagement")
            DIRAC.exit(5)

    plugin = pluginScript.getOption("Plugin")
    # Default plugin for MCDST replication
    if mcVersionSet and not plugin:
        plugin = "LHCbMCDSTBroadcastRandom"

    if not plugin and not listProcessingPasses:
        gLogger.fatal("ERROR: No plugin supplied...")
        Script.showHelp(exitCode=1)
    prods = pluginScript.getOption("Productions")
    requestID = pluginScript.getOption("RequestID")
    fileType = pluginScript.getOption("FileType")
    pluginParams = pluginScript.getPluginParameters()
    pluginSEParams = pluginScript.getPluginSEParameters()
    requestedLFNs = pluginScript.getOption("LFNs")

    transType = None
    if plugin in getRemovalPlugins():
        transType = "Removal"
    elif plugin in getReplicationPlugins():
        transType = "Replication"
    elif not listProcessingPasses:
        gLogger.notice("This script can only create Removal or Replication plugins")
        gLogger.notice("Replication :", str(getReplicationPlugins()))
        gLogger.notice("Removal     :", str(getRemovalPlugins()))
        gLogger.notice(f"If needed, ask for adding {plugin} to the known list of plugins")
        DIRAC.exit(2)

    bk = BookkeepingClient()
    tr = TransformationClient()

    if plugin in ("DestroyDataset", "DestroyDatasetWhenProcessed") or prods:
        # visible = 'All'
        fcCheck = False

    # If mcVersions are defined, get the processing passes
    if mcVersionSet:
        # We keep only numerical values or "all"
        mcVersions = {mcv for mcv in mcVersionSet if mcv.isdigit() or mcv == "all"}
        if not mcVersions:
            gLogger.fatal("Invalid MC versions", ",".join(sorted(mcVersionSet)))
            DIRAC.exit(2)
        if mcVersions != mcVersionSet:
            gLogger.notice("WARNING: list of MC versions reduced to", ",".join(sorted(mcVersions)))
        # Force transformations names to be unique
        unique = True
        res = ProductionRequestClient().getProductionRequestList(
            0, "RequestID", "DESC", 0, 0, {"RequestState": "Active", "RequestType": "Simulation"}
        )
        if not res["OK"]:
            gLogger.fatal("Error getting production requests", res["Message"])
        prodReq = res["Value"]["Rows"]
        reqDict = defaultdict(set)
        for row in prodReq:
            mcVersion = json.loads(row["Extra"])["mcConfigVersion"]
            # If "all" we take all numerical values, otherwise we take the explicit values
            if ("all" in mcVersions and mcVersion.isdigit()) or mcVersion in mcVersions:
                proPath = row["ProPath"]
                if "/Reco" in proPath:
                    reqDict[mcVersion].add(proPath)
        bkPaths = []
        for mcVersion, proPaths in reqDict.items():
            for proPath in proPaths:
                bkPaths.append(f"/MC/{mcVersion}//{proPath}")
    elif not requestedLFNs:
        # If BK path is given, set it such that one goes through the loop below
        bkPaths = [None]
    else:
        bkPaths = []

    transBKQuery = {}
    bkQueries = []
    bkPaths.sort()
    if checkMCReplication:
        gLogger.notice("List of active BK paths to be kept:")
    for bkPath in sorted(bkPaths):
        if bkPath:
            bkQuery = BKQuery(bkPath)
            if checkMCReplication:
                if "..." in bkPath or "*" in bkPath:
                    gLogger.notice(f"Getting list of BK paths for {bkPath}")
                else:
                    gLogger.notice(f"BK path {bkPath}")
            elif not listProcessingPasses:
                gLogger.notice(f"For BK path: {bkPath}")
        else:
            bkQuery = pluginScript.getBKQuery()
        if not bkQuery and not force:
            gLogger.fatal("No LFNs and no BK query were given...")
            Script.showHelp(exitCode=2)
        if bkQuery:
            processingPass = bkQuery.getProcessingPass()
            if "..." in processingPass or "*" in processingPass:
                bkPath = bkQuery.getPath().replace("RealData", "Real Data")
                if listProcessingPasses:
                    gLogger.notice("List of processing passes for BK path", bkPath)
                processingPasses = getProcessingPasses(bkQuery, depth=depth)
                # Skip AnaProd productions for MC unless explicitly requested
                if mcVersionSet and processingPasses:
                    processingPasses = [pp for pp in processingPasses if "AnaProd" not in pp]
                if processingPasses:
                    if not checkMCReplication:
                        if not listProcessingPasses:
                            gLogger.notice(
                                "Transformations will be launched for the following list of processing passes:"
                            )
                        gLogger.notice("\t" + "\n\t".join(processingPasses))
                else:
                    gLogger.notice("No processing passes matching the BK path")
                    continue
                # Create a list of BK queries, taking into account visibility and if needed excluded file types
                exceptTypes = bkQuery.getExceptFileTypes()
                visible = bkQuery.isVisible()
                for pp in processingPasses:
                    query = BKQuery(bkPath.replace(processingPass, pp), visible=visible)
                    query.setExceptFileTypes(exceptTypes)
                    bkQueries.append(query)
            else:
                bkQueries.append(bkQuery)
        if bkPath and not checkMCReplication:
            gLogger.notice("====================================")

    if listProcessingPasses:
        DIRAC.exit(0)

    # Check all MC replication transformations and list obsolete ones
    if checkMCReplication:
        bkPaths = [bkQuery.getPath() for bkQuery in bkQueries]
        obsoleteTrans = _checkMCReplication(bkPaths)
        gLogger.notice("====================================")
        # Print list of BK paths
        gLogger.notice(
            f"List of {len(obsoleteTrans)} transformations to set Completed:",
            "\n" + ",".join(str(transID) for transID in obsoleteTrans),
        )
        DIRAC.exit(0)

    reqID = pluginScript.getRequestID()
    if not requestID and reqID:
        requestID = reqID

    transGroup = plugin
    # If no BK queries are given, set to None to go once in the loop
    if not bkQueries:
        bkQueries = [None]

    for bkQuery in bkQueries:
        if bkQuery != bkQueries[0]:
            gLogger.notice("**************************************")
        # Create the transformation
        transformation = Transformation()
        transformation.setType(transType)
        transName = transType

        # In case there is a loop on processing passes
        if bkQuery:
            transBKQuery = bkQuery.getQueryDict()
        if requestedLFNs:
            longName = transGroup + f" for {len(requestedLFNs)} LFNs"
            transName += "-LFNs"
        elif prods:
            if not fileType:
                fileType = ["All"]
            prodsStr = ",".join(str(p) for p in prods)
            fileStr = ",".join(fileType)
            longName = transGroup + " of " + fileStr + f" for productions {prodsStr} "
            if len(prods) > 5:
                prodsStr = f"{len(prods)}-productions"
            if len(fileStr) > 30:
                fileStr = f"{len(fileType)}-fileTypes"
            transName += "-" + fileStr + "-" + prodsStr
        elif transBKQuery and "FileType" in transBKQuery and "BKPath" not in pluginScript.getOptions():
            if isinstance(transBKQuery["FileType"], list):
                strQuery = ",".join(transBKQuery["FileType"])
            else:
                strQuery = str(transBKQuery["FileType"])
            longName = transGroup + " for fileType " + strQuery
            transName += "-" + str(transBKQuery["FileType"])
        elif bkQuery:
            queryPath = bkQuery.getPath()
            longName = transGroup + " for BKQuery " + queryPath
            transName += "-" + queryPath
        else:
            transName = ""

        dqFlag = transBKQuery.get("DataQuality", [])
        if "BAD" in dqFlag:
            dqFlag = f" (DQ: {','.join(dqFlag)})"
            transName += dqFlag
            longName += dqFlag

        if requestID:
            transName += f"-Request{requestID}"
        # If a name is given in the options, use it
        if nameOption:
            transName = nameOption
            longName = transGroup + " - " + transName
        if not transName:
            gLogger.fatal("Didn't manage to find a name for this transformation, check options")
            DIRAC.exit(1)
        # Find a name for this transformation (transName remains the base name)
        tName = getTransformationName(transName, unique)
        # If needed, skip this BK query
        if tName is None:
            continue

        transformation.setTransformationName(tName)
        transformation.setTransformationGroup(transGroup)
        transformation.setDescription(longName[:255])
        transformation.setLongDescription(longName)
        transformation.setType(transType)

        # Rename plugin
        if plugin == "DestroyDatasetWhenProcessed":
            plugin = "DeleteReplicasWhenProcessed"
            # Set the polling period to 0 if not defined
            pluginParams.setdefault("Period", 0)

        # If we have a body plugin, load it
        if bodyPlugin:
            objLoader = ObjectLoader()
            _class = objLoader.loadObject(f"TransformationSystem.Client.BodyPlugin.{bodyPlugin}", bodyPlugin)

            if not _class["OK"]:
                raise Exception(_class["Message"])
            # TODO: handle the case of a body plugin with arguments
            transBody = _class["Value"]()
        else:
            # If we don't have a body, define it for Removal transformations
            if not transBody and transType == "Removal":
                if plugin == "DestroyDataset":
                    transBody = "removal;RemoveFile"
                elif plugin == "DestroyDatasetWhenProcessed":
                    transBody = "removal;RemoveFile"
                else:
                    transBody = "removal;RemoveReplica"

        if transBody:
            transformation.setBody(transBody)

        if pluginSEParams:
            for key, val in pluginSEParams.items():
                res = transformation.setSEParam(key, val)
                if not res["OK"]:
                    gLogger.error("Error setting SE parameter", res["Message"])
                    DIRAC.exit(1)
        if pluginParams:
            for key, val in pluginParams.items():
                res = transformation.setAdditionalParam(key, val)
                if not res["OK"]:
                    gLogger.error("Error setting additional parameter", res["Message"])
                    DIRAC.exit(1)

        transformation.setPlugin(plugin)

        if test:
            gLogger.notice("Transformation type:", transType)
            gLogger.notice("Transformation Name:", transName)
            gLogger.notice("Transformation group:", transGroup)
            gLogger.notice("Long description:", longName)
            gLogger.notice("Transformation body:", transBody)
            if transBKQuery:
                gLogger.notice("BK Query:", transBKQuery)
            elif requestedLFNs:
                gLogger.notice(f"List of {len(requestedLFNs)} LFNs")
            else:
                # Should not happen here, but who knows ;-)
                gLogger.error("No BK query provided...")
                Script.showHelp(exitCode=1)

        if force:
            lfns = []
        elif transBKQuery:
            bkPath = bkQuery.getPath()
            title = "Executing BK query"
            if bkPath:
                title += " for " + bkPath
            else:
                title += ": " + str(bkQuery)
            progressBar = ProgressBar(1, title=title)
            lfns = bkQuery.getLFNs(
                printSEUsage=(transType == "Removal" and not pluginScript.getOption("Runs")), printOutput=test
            )
            progressBar.endLoop(message=(f"found {len(lfns)} files" if lfns else "no files found"))
        else:
            lfns = requestedLFNs
        nfiles = len(lfns)

        if test:
            gLogger.notice("Plugin:", plugin)
            gLogger.notice("Parameters:", pluginParams)
            gLogger.notice("RequestID:", requestID)
            continue

        if not force and nfiles == 0:
            gLogger.notice("No files, but if you anyway want to submit the transformation, use option --Force")
            continue

        if userGroup:
            directories = {os.path.dirname(lfn) for lfn in lfns}
            res = chown(directories, user=userGroup[0], group=userGroup[1])
            if not res["OK"]:
                gLogger.fatal("Error changing ownership", res["Message"])
                DIRAC.exit(3)
            gLogger.notice("Successfully changed owner/group for %d directories" % res["Value"])

        # If the transformation is a removal transformation,
        #  check all files are in the FC. If not, remove their replica flag
        if fcCheck and transType == "Removal":
            from DIRAC.Resources.Catalog.FileCatalog import FileCatalog

            fc = FileCatalog()
            success = 0
            missingLFNs = set()
            chunkSize = 1000
            progressBar = ProgressBar(len(lfns), title=f"Checking {len(lfns)} files in FC", chunk=chunkSize)
            for lfnChunk in breakListIntoChunks(lfns, chunkSize):
                progressBar.loop()
                res = fc.exists(lfnChunk)
                if res["OK"]:
                    success += len(res["Value"]["Successful"])
                    missingLFNs |= set(res["Value"]["Failed"])
                else:
                    gLogger.fatal("\nError checking files in the FC", res["Message"])
                    DIRAC.exit(2)
            progressBar.endLoop(message="all found" if not missingLFNs else None)
            if missingLFNs:
                gLogger.notice(
                    "%d are in the FC, %d are not. Attempting to remove GotReplica" % (success, len(missingLFNs))
                )
                res = bk.removeFiles(list(missingLFNs))
                if res["OK"]:
                    gLogger.notice("Replica flag successfully removed in BK")
                else:
                    gLogger.fatal("Error removing BK flag", res["Message"])
                    DIRAC.exit(2)

        # Prepare the transformation
        if transBKQuery:
            # !!!! Hack in order to remain compatible with hte BKQuery table...
            for transKey, bkKey in (
                ("ProductionID", "Production"),
                ("RunNumbers", "RunNumber"),
                ("DataQualityFlag", "DataQuality"),
            ):
                if bkKey in transBKQuery:
                    transBKQuery[transKey] = transBKQuery.pop(bkKey)
            transformation.setBkQuery(transBKQuery)

        # If the transformation uses the RemoveDatasetFromDisk plugin, set the files invisible in the BK...
        # Try and let them visible such that users can see they are archived...
        # It was:
        # setInvisiblePlugins = ("RemoveDatasetFromDisk", )
        setInvisiblePlugins = tuple()
        if invisible or plugin in setInvisiblePlugins:
            chunkSize = 1000
            progressBar = ProgressBar(len(lfns), title=f"Setting {len(lfns)} files invisible", chunk=chunkSize)
            okFiles = 0
            for lfnChunk in breakListIntoChunks(lfns, chunkSize):
                progressBar.loop()
                res = bk.setFilesInvisible(lfnChunk)
                if res["OK"]:
                    okFiles += len(lfnChunk)
            if okFiles == len(lfns):
                msg = "all files successfully set invisible in BK"
            else:
                msg = "%d files successfully set invisible in BK" % okFiles
            progressBar.endLoop(message=msg)
            if res["OK"]:
                if transBKQuery:
                    savedVisi = transBKQuery.get("Visible")
                    transBKQuery["Visible"] = "All"
                    transformation.setBkQuery(transBKQuery.copy())
                    if savedVisi:
                        transBKQuery["Visible"] = savedVisi
                    else:
                        transBKQuery.pop("Visible")
            else:
                gLogger.error("Failed to set files invisible: ", res["Message"])

        errMsg = ""
        while True:
            res = transformation.addTransformation()
            if not res["OK"]:
                errMsg = "Couldn't create transformation"
                break
            res = transformation.getTransformationID()
            if res["OK"]:
                transID = res["Value"]
            else:
                errMsg = "Error getting transformationID"
                break
            # If some LFNs must be added, do it now
            if requestedLFNs:
                from LHCbDIRAC.TransformationSystem.Utilities.PluginUtilities import addFilesToTransformation

                res = addFilesToTransformation(transID, requestedLFNs, addRunInfo=True)
                if not res["OK"]:
                    errMsg = "Could not add files to transformation"
                    break
                gLogger.notice(f"{len(res['Value']['Successful'])} files successfully added to transformation")
                if res["Value"]["Failed"]:
                    errors = defaultdict(int)
                    for error in res["Value"]["Failed"].values():
                        errors[error] += 1
                    for error, count in errors.items():
                        gLogger.always("Failed to add %d files to transformation %d:" % (count, transID), error)
            if requestID:
                transformation.setTransformationFamily(requestID)
            if start:
                transformation.setStatus("Active")
                transformation.setAgentType("Automatic")
            gLogger.notice(f"Name: {transName}")
            gLogger.notice("Transformation body:", transBody)
            gLogger.notice("Plugin:", plugin)
            if pluginParams:
                gLogger.notice("Additional parameters:", pluginParams)
            if requestID:
                gLogger.notice("RequestID:", requestID)
            break
        if errMsg:
            gLogger.notice(errMsg, res["Message"])

    DIRAC.exit(0)
