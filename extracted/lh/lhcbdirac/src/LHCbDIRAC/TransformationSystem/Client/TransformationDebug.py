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
Actual executor methods of the dirac-transformation-debug script
"""
import datetime
import itertools
import os
import sys
import tempfile
import zipfile
from collections import defaultdict
from fnmatch import fnmatch
from docutils.nodes import line

import DIRAC
from DIRAC import gLogger
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations
from DIRAC.Core.Base import Script
from DIRAC.Core.Utilities.File import mkDir
from DIRAC.Core.Utilities.List import breakListIntoChunks
from DIRAC.Core.Utilities.ReturnValues import returnSingleResult
from DIRAC.DataManagementSystem.Client.DataManager import DataManager
from DIRAC.RequestManagementSystem.Client.ReqClient import ReqClient, printOperation
from DIRAC.Resources.Catalog.FileCatalog import FileCatalog
from DIRAC.Resources.Storage.StorageElement import StorageElement
from DIRAC.TransformationSystem.Utilities.ScriptUtilities import getTransformations
from DIRAC.WorkloadManagementSystem.Client.JobMonitoringClient import JobMonitoringClient
from DIRAC.WorkloadManagementSystem.Client.SandboxStoreClient import SandboxStoreClient

from LHCbDIRAC.BookkeepingSystem.Client.BookkeepingClient import BookkeepingClient
from LHCbDIRAC.DataManagementSystem.Client.DMScript import DMScript, ProgressBar
from LHCbDIRAC.TransformationSystem.Client.TransformationClient import TransformationClient
from LHCbDIRAC.TransformationSystem.Utilities.PluginUtilities import PluginUtilities


def _checkReplicasForProblematic(lfns, replicas, nbReplicasProblematic, problematicReplicas):
    """
    Check replicas of Problematic files

    :param lfns: list of LFNs
    :type lfns: list
    :param replicas: replica dict
    :type replicas:dict
    :param nbReplicasProblematic: dict to be filled with stat per number of SE
    :type nbReplicasProblematic: dict
    :param problematicReplicas: dict of LFNs per SE
    :type problematicReplicas: dict
    """
    for lfn in lfns:
        # Problematic files, let's see why
        realSEs = [se for se in replicas.get(lfn, []) if not se.endswith("-ARCHIVE")]
        nbSEs = len(realSEs)
        nbReplicasProblematic[nbSEs] += 1
        if not nbSEs:
            problematicReplicas[None].append(lfn)
        for se in realSEs:
            problematicReplicas[se].append(lfn)


def _genericLfn(lfn, lfnList):
    """
    From a file name, replace the job number with <jobNumber>
    """
    if lfn not in lfnList and os.path.dirname(lfn) == "":
        spl = lfn.split("_")
        if len(spl) == 3:
            spl[1] = "<jobNumber>"
        lfn = "_".join(spl)
    return lfn


def __buildURL(urlBase, ref):
    """Build URL from a base, checking whether the ref file is an absolute or relative path"""
    # If absolute path, get the hostas base
    if os.path.isabs(ref):
        urlBase = os.path.sep.join(urlBase.split(os.path.sep)[:3])
        ref = ref[1:]
    return os.path.join(urlBase, ref)


def _getLog(urlBase, logFile, debug=False):
    """
    Get a logfile and return its content
    """
    # if logFile == "" it is assumed the file is directly the urlBase
    # Otherwise it can either be referenced within urlBase or contained (.tar.gz)

    # In order to use https with the correct CA, use the FancyURLOpener and the user proxy as certificate
    logLevel = gLogger.getLevel()
    gLogger.setLevel("ERROR")
    try:
        logSE = StorageElement("LogSE-EOS")
        lfnBase = DMScript().getLFNsFromList([urlBase], directories=True)[0]
        logLFN = os.path.normpath(lfnBase) + ".zip"
        if debug:
            print("Entering getLog", logLFN, logFile)
        if debug:
            print("Opening zip file ", logLFN)
        # retrieve the zipped file
        tmpDir = tempfile.gettempdir()
        tmp = os.path.join(tmpDir, os.path.basename(logLFN))
        if debug:
            print("Retrieve the file in ", tmp)
        if os.path.exists(tmp):
            os.remove(tmp)
        # urlOpener.retrieve(logLFN, tmp)
        res = returnSingleResult(logSE.getFile(logLFN, localPath=tmpDir))
        if not res["OK"]:
            # If the logfile was uploaded by a request, its URL is different, try it!
            splitURL = urlBase.split("/")
            logLFN = lfnBase + f"{splitURL[9]}_{splitURL[11]}.tar"
            tmp = os.path.join(tmpDir, os.path.basename(logLFN))
            if os.path.exists(tmp):
                os.remove(tmp)
            res = returnSingleResult(logSE.getFile(logLFN, localPath=tmpDir))
            if not res["OK"]:
                gLogger.error("Error getting log zip", res["Message"])
                return None
            if debug:
                print("Logfile is a failover upload zip with a .tar extension")
        if debug:
            print("Open zip file ", tmp)
        zf = zipfile.ZipFile(tmp)
        mn = zf.namelist()
        if debug:
            print("Found those members", mn, ", looking for", logFile)
        # There may be more than one file matching the name, read them all
        matchingFiles = []
        for fileName in mn:
            if fnmatch(fileName, "*/" + logFile + "*"):
                if debug:
                    print("Found ", logFile, " in zip object ", fileName)
                matchingFiles.append(fileName)
        # read the actual files...
        cc = []
        for fileName in matchingFiles:
            with zf.open(fileName) as fd:
                if debug:
                    print(f"File {fileName} successfully open")
                cc += fd.read().decode("utf-8").split("\n")
        if debug:
            print(f"{len(matchingFiles)} files read... {len(cc)} lines")
        if zf:
            zf.close()
        if tmp:
            os.remove(tmp)
        return cc
    finally:
        gLogger.setLevel(logLevel)


def _getSandbox(job, logFile, debug=False):
    """
    Get a sandox and return its content
    """
    fd = None
    files = []
    try:
        tmpDir = os.path.join(tempfile.gettempdir(), "sandBoxes/")
        mkDir(tmpDir)
        if debug:
            print("Job", job, ": sandbox being retrieved in", tmpDir)

        res = SandboxStoreClient(smdb=False).downloadSandboxForJob(job, "Output", tmpDir)
        if res["OK"]:
            if debug:
                print("Sandbox successfully retrieved")
            files = os.listdir(tmpDir)
            if debug:
                print("Files:", files)
            for lf in files:
                if fnmatch(lf, logFile):
                    if debug:
                        print(lf, "matched", logFile)
                    with open(os.path.join(tmpDir, lf)) as fd:
                        return fd.readlines()
            return ""
    except OSError as e:
        gLogger.exception("Exception while getting sandbox", lException=e)
        return ""
    finally:
        for lf in files:
            os.remove(os.path.join(tmpDir, lf))
        os.rmdir(tmpDir)


def _checkXMLSummary(job, logURL):
    """
    Look in an XMLSummary file for partly processed files of failed files
    Return the list of bad LFNs
    """
    debug = False
    try:
        xmlFile = _getLog(logURL, "summary*.xml*", debug=debug)
        if not xmlFile:
            if debug:
                print("XML not found in logs")
            xmlFile = _getSandbox(job, "summary*.xml*", debug=debug)
            if xmlFile and debug:
                print("XML from SB")
        elif debug:
            print("XML from logs")
        lfns = {}
        if xmlFile:
            for line in xmlFile:
                if 'status="part"' in line and "LFN:" in line:
                    event = line.split(">")[1].split("<")[0]
                    lfns.update({line.split("LFN:")[1].split('"')[0]: f"Partial (last event {event})"})
                elif 'status="fail"' in line and "LFN:" in line:
                    lfns.update({line.split("LFN:")[1].split('"')[0]: "Failed"})
            if not lfns:
                lfns = {None: "No errors found in XML summary"}
        return lfns
    except Exception as e:
        gLogger.exception("Exception while checking XML summary", lException=e)
        return {None: "Could not open XML summary"}


def _getTiming(logURL):
    """
    Extract timing information from logfile
    """
    for i in range(5, 0, -1):
        logFile = _getLog(logURL, f"*_{i}.log", debug=False)
        if logFile:
            break
    timing = {}
    for ll in logFile:
        if "EVENT LOOP" in ll:
            content = ll.split()
            timing["User"] = int(float(content[8])) / 1000.0
            timing["Clock"] = int(float(content[10])) / 1000.0
            timing["min"] = int(float(content[12])) / 1000.0
            timing["max"] = int(float(content[13])) / 1000.0
            timing["sigma"] = int(float(content[14])) / 1000.0
            timing["Entries"] = int(content[16])
            timing["Total"] = float(content[18])
            break
    return timing


def _checkLog(logURL):
    """
    Find ERROR string, core dump or "stalled events" in a logfile
    """
    debug = False
    for i in range(5, 0, -1):
        logFile = _getLog(logURL, f"*_{i}.log", debug=debug)
        if logFile:
            break
    logDump = []
    if logFile:
        space = False
        for line in logFile:
            if " ERROR " in line or "*** Break ***" in line:
                if space:
                    logDump.append("....")
                    space = False
                logDump.append(line)
            else:
                space = True
            if "Stalled event" in line:
                logDump = ["Stalled Event"]
                break
    else:
        logDump = [f"Couldn't find log file in {logURL}"]
    return logDump[-10:]


class TransformationDebug:
    """
    This class houses all methods for debugging transformations
    """

    def __init__(self):
        self.transClient = TransformationClient()
        self.reqClient = ReqClient()
        self.bkClient = BookkeepingClient()
        self.dataManager = DataManager()
        self.fileCatalog = FileCatalog()
        self.monitoring = None
        self.dataManagerTransTypes = ("Replication", "Removal")
        self.transID = None
        self.transType = None
        self.fixIt = False
        self.kickRequests = False
        self.cancelRequests = False
        self.pluginUtil = None
        self.listOfAssignedRequests = {}
        self.transPlugin = None

    def __getFilesForRun(
        self, runID=None, status=None, lfnList=None, seList=None, taskList=None, transID=None, since=None
    ):
        """
        Get a lit of TS files fulfilling criteria

        :param runList: list of run numbers
        :type runList: list
        :param seList: list of UsedSE
        :type seList: list
        :param status: file TS status
        :type status: string or list
        :param taskList: list of task IDs
        :type taskList: list
        :param lfnList: list of LFNs
        :type lfnList: list
        :param transID: transformation ID
        :type transID: int

        :return : list of TS files (i.e. dictionaries) fulfilling the criteria
        """
        if transID is None:
            transID = self.transID
        # print transID, runID, status, lfnList
        selectDict = {"TransformationID": transID}
        if runID is not None:
            if runID:
                selectDict["RunNumber"] = runID
            else:
                selectDict["RunNumber"] = str(runID)
        if status:
            selectDict["Status"] = status
        if lfnList:
            selectDict["LFN"] = lfnList
        if seList:
            selectDict["UsedSE"] = seList
        taskFiles = defaultdict(set)
        if taskList:
            # First get fileID per task as the task may no longer be in the TransformationFiles table
            for taskID in taskList:
                res = self.transClient.getTableDistinctAttributeValues(
                    "TransformationFileTasks", ["FileID"], {"TransformationID": transID, "TaskID": taskID}
                )
                if res["OK"]:
                    # Keep track of which file corresponds to which task
                    if res["Value"]["FileID"]:
                        for fileID in res["Value"]["FileID"]:
                            taskFiles[fileID].add(taskID)
                            selectDict.setdefault("FileID", []).append(fileID)
                else:
                    gLogger.error("Error getting Transformation tasks:", res["Message"])
                    return []
        res = self.transClient.getTransformationFiles(selectDict, newer=since)
        if res["OK"]:
            if taskFiles:
                # Set the correct taskID as it may have changed
                fileDictList = []
                for fileDict in res["Value"]:
                    for taskID in taskFiles[fileDict["FileID"]]:
                        newFile = fileDict.copy()
                        newFile["TaskID"] = taskID
                        fileDictList.append(newFile)
            else:
                fileDictList = res["Value"]
            return fileDictList
        gLogger.error("Error getting Transformation files:", res["Message"])
        return []

    def __filesProcessed(self, runID):
        """
        Get the number of files and number of processed files in a run

        :param runID: run number
        :type runID: int, long
        :return : tuple (nb of files, nb of files Processed)
        """
        transFilesList = self.__getFilesForRun(runID, None)
        files = len(transFilesList)
        processed = sum(fileDict["Status"] == "Processed" for fileDict in transFilesList)
        return (files, processed)

    def __getRuns(self, runList=None, byRuns=True, seList=None, status=None, taskList=None, transID=None, since=None):
        """
        Get a list of TS runs fulfilling criteria

        :param runList: list of run numbers
        :type runList: list
        :param byRuns: if True, get a list of runs, else just None
        :type byRuns: boolean
        :param seList: list of UsedSE
        :type seList: list
        :param status: file TS status
        :type status: string or list
        :param taskList: list of task IDs
        :type taskList: list

        :return : list of dictionaries (one per run) fulfilling the criteria
        """
        runs = []
        if status and byRuns and not runList:
            files = self.__getFilesForRun(status=status, taskList=taskList, transID=transID, since=since)
            runList = {str(fileDict["RunNumber"]) for fileDict in files}

        if runList:
            for runRange in runList:
                runRange = runRange.split(":")
                if len(runRange) == 1:
                    runs.append(int(runRange[0]))
                else:
                    for run in range(int(runRange[0]), int(runRange[1]) + 1):
                        runs.append(run)
            selectDict = {"TransformationID": self.transID, "RunNumber": runs}
            if runs == [0]:
                runs = [{"RunNumber": 0}]
            else:
                if seList:
                    selectDict["SelectedSite"] = seList
                res = self.transClient.getTransformationRuns(selectDict)
                if res["OK"]:
                    if len(res["Value"]) == 0:
                        gLogger.notice("No runs found, set to None")
                        runs = [{"RunNumber": None}]
                    else:
                        runs = res["Value"]
        elif not byRuns:
            # No run selection
            runs = [{"RunNumber": None}]
        elif not status:
            # All runs selected explicitly
            selectDict = {"TransformationID": self.transID}
            if seList:
                selectDict["SelectedSite"] = seList
            res = self.transClient.getTransformationRuns(selectDict)
            if res["OK"]:
                if len(res["Value"]) == 0:
                    gLogger.notice("No runs found, set to None")
                    runs = [{"RunNumber": None}]
                else:
                    runs = res["Value"]
        return runs

    def __justStats(self, status, seList):
        """
        Print out statistics per usedSE about TS files in a given status targeting some sites

        :param status: (list of) status
        :type status: list or string
        :param seList: list of usedSE
        :type seList: list or string

        :return : list of jobIDs that are not in a proper status w.r.t. status
        """
        improperJobs = []
        if not status:
            status = "Assigned"
        transFilesList = self.__getFilesForRun(status=status, seList=seList)
        if not transFilesList:
            return improperJobs
        statsPerSE = {}
        # print transFilesList
        statusList = {"Received", "Checking", "Staging", "Waiting", "Running", "Stalled"}
        if status == "Processed":
            statusList.update({"Done", "Completed", "Failed"})
        taskList = [fileDict["TaskID"] for fileDict in transFilesList]
        res = self.transClient.getTransformationTasks({"TransformationID": self.transID, "TaskID": taskList})
        if not res["OK"]:
            gLogger.notice("Could not get the list of tasks...", res["Message"])
            DIRAC.exit(2)
        for task in res["Value"]:
            # print task
            targetSE = task["TargetSE"]
            stat = task["ExternalStatus"]
            statusList.add(stat)
            statsPerSE[targetSE][stat] = (
                statsPerSE.setdefault(targetSE, dict.fromkeys(statusList, 0)).setdefault(stat, 0) + 1
            )
            if status == "Processed" and stat not in ("Done", "Completed", "Stalled", "Failed", "Killed", "Running"):
                improperJobs.append(task["ExternalID"])

        shift = 0
        for se in statsPerSE:
            shift = max(shift, len(se) + 2)
        prString = "SE".ljust(shift)
        for stat in statusList:
            prString += stat.ljust(10)
        gLogger.notice(prString)
        for se in sorted(statsPerSE):
            prString = se.ljust(shift)
            for stat in statusList:
                prString += str(statsPerSE[se].get(stat, 0)).ljust(10)
            gLogger.notice(prString)
        return improperJobs

    def __getTransformationInfo(self, transSep):
        """
        Print out information about a given transformation

        :param transSep: separator to print out before info
        :type transSep: string

        :return : tuple ("Job"|"Request", file type in BK query)
        """
        res = self.transClient.getTransformation(self.transID, extraParams=False)
        if not res["OK"]:
            gLogger.notice("Couldn't find transformation", self.transID)
            return None, None
        transStatus = res["Value"]["Status"]
        self.transType = res["Value"]["Type"]
        transBody = res["Value"]["Body"]
        self.transPlugin = res["Value"]["Plugin"]
        strPlugin = self.transPlugin
        if self.transType in ("Merge", "MCMerge", "DataStripping", "MCStripping", "Sprucing"):
            strPlugin += f", GroupSize: {str(res['Value']['GroupSize'])}"
        if self.transType in self.dataManagerTransTypes:
            taskType = "Request"
        else:
            taskType = "Job"
        transGroup = res["Value"]["TransformationGroup"]
        gLogger.notice(
            f"{transSep} Transformation {self.transID} ({transStatus}) of"
            + f" type {self.transType} (plugin {strPlugin}) in {transGroup}"
        )
        if self.transType == "Removal":
            gLogger.notice("Transformation body:", transBody)
        res = self.transClient.getBookkeepingQuery(self.transID)
        if res["OK"] and res["Value"]:
            gLogger.notice("BKQuery:", res["Value"])
            queryFileTypes = res["Value"].get("FileType")
        else:
            gLogger.notice("No BKQuery for this transformation")
            queryFileTypes = None
        gLogger.notice("")
        return taskType, queryFileTypes

    def __fixRunNumber(self, filesToFix, fixRun, noTable=False):
        """
        Fix run information in TS

        :param filesToFix: list of TS files to get fixed
        :type filesToFix: list
        :param fixRun: if set, fix run, else print out number of files
        :type fixRun: boolean
        :param noTable: if True, the run is absent, else it is 0
        :type noTable: boolean
        """
        if not fixRun:
            if noTable:
                gLogger.notice(
                    f"{len(filesToFix)} files have run number not in run table, use --FixRun to get this fixed"
                )
            else:
                gLogger.notice(f"{len(filesToFix)} files have run number 0, use --FixRun to get this fixed")
        else:
            fixedFiles = 0
            res = self.bkClient.getFileMetadata(filesToFix)
            if res["OK"]:
                runFiles = defaultdict(list)
                for lfn, metadata in res["Value"]["Successful"].items():  # can be an iterator
                    runFiles[metadata["RunNumber"]].append(lfn)
                for run in runFiles:
                    if not run:
                        gLogger.notice(
                            f"{len(runFiles[run])} files found in BK with run '{str(run)}': {str(runFiles[run])}"
                        )
                        continue
                    res = self.transClient.addTransformationRunFiles(self.transID, run, runFiles[run])
                    # print run, runFiles[run], res
                    if not res["OK"]:
                        gLogger.notice(
                            f"***ERROR*** setting {len(runFiles[run])} files to run {run} in transformation {self.transID}",
                            res["Message"],
                        )
                    else:
                        fixedFiles += len(runFiles[run])
                if fixedFiles:
                    gLogger.notice(f"Successfully fixed run number for {fixedFiles} files")
                else:
                    gLogger.notice("There were no files for which to fix the run number")
            else:
                gLogger.notice(f"***ERROR*** getting metadata for {len(filesToFix)} files:", res["Message"])

    def __checkFilesMissingInFC(self, transFilesList, status):
        """
        Check a list of files that are missing in FC and print information

        :param transFilesList: list of TS files
        :type transFilesList: list
        :param status: (list of) status
        :type status: list or string
        """
        lfns = [fileDict["LFN"] for fileDict in transFilesList if fileDict["Status"] == "MissingInFC"]
        if lfns:
            res = self.dataManager.getReplicas(lfns)
            if res["OK"]:
                replicas = res["Value"]["Successful"]
                notMissing = len(replicas)
                if notMissing:
                    if not self.kickRequests:
                        gLogger.notice(
                            f"{notMissing} files are {status} but indeed are in the FC - \
              Use --KickRequests to reset them Unused"
                        )
                    else:
                        res = self.transClient.setFileStatusForTransformation(
                            self.transID, "Unused", list(replicas), force=True
                        )
                        if res["OK"]:
                            gLogger.notice(
                                f"{notMissing} files were {status} but " + "indeed are in the FC - Reset to Unused"
                            )
                        else:
                            gLogger.notice(f"Error resetting {notMissing} files Unused", res["Message"])
                else:
                    res = self.bkClient.getFileMetadata(lfns)
                    if not res["OK"]:
                        gLogger.notice("ERROR getting metadata from BK", res["Message"])
                    else:
                        metadata = res["Value"]["Successful"]
                        lfnsWithReplicaFlag = [lfn for lfn in metadata if metadata[lfn]["GotReplica"] == "Yes"]
                        if lfnsWithReplicaFlag:
                            gLogger.notice("All files are really missing in FC")
                            if not self.fixIt:
                                gLogger.notice(
                                    f"{len(lfnsWithReplicaFlag)} files are not in the FC but have a replica flag in BK"
                                    + ", use --FixIt to fix"
                                )
                            else:
                                res = self.bkClient.removeFiles(lfnsWithReplicaFlag)
                                if not res["OK"]:
                                    gLogger.notice("ERROR removing replica flag:", res["Message"])
                                else:
                                    gLogger.notice(f"Replica flag removed from {len(lfnsWithReplicaFlag)} files")
                        else:
                            gLogger.notice("All files are really missing in FC and BK")

    def __getReplicas(self, lfns):
        """
        Get replicas of a list of LFNs

        :param lfns: list of LFNs
        :type lfns: list
        """
        replicas = {}
        for lfnChunk in breakListIntoChunks(lfns, 1000):
            res = self.dataManager.getReplicas(lfnChunk, getUrl=False)
            if res["OK"]:
                replicas.update(res["Value"]["Successful"])
            else:
                gLogger.notice("Error getting replicas", res["Message"])
        return replicas

    def __getTasks(self, taskIDs: list[int]) -> dict[int, dict]:
        """
        Get the TS tasks, indexed by task ID

        :param taskID: task IDs
        """
        res = self.transClient.getTransformationTasks({"TransformationID": self.transID, "TaskID": taskIDs})
        if not res["OK"] or not res["Value"]:
            return {}
        return {task["TaskID"]: task for task in res["Value"]}

    def __fillStatsPerSE(self, seStat, rep, listSEs):
        """
        Fill statistics per SE for a set of replicas and a list of SEs
        Depending whether the transformation is replication or removal, give the stat of missing or still present SEs

        :param seStat: returned dictionary (number per SE)
        :type seStat: dictionary
        :param rep: list of replicas
        :type rep: list or dict
        :param listSEs: list of SEs to give statistics about
        :type listSEs: list
        """
        seStat["Total"] += 1
        completed = True
        if not rep:
            seStat[None] += 1
        if not listSEs:
            listSEs = ["Some"]
        for se in listSEs:
            if self.transType == "Replication":
                if se == "Some" or se not in rep:
                    seStat[se] += 1
                    completed = False
            elif self.transType == "Removal":
                if se == "Some" or se in rep:
                    seStat[se] += 1
                    completed = False
            else:
                if se not in rep:
                    seStat[se] += 1
        return completed

    def __getRequestName(self, requestID):
        """
        Return request name from ID

        :param requestID: request ID
        :type requestID: int
        """
        level = gLogger.getLevel()
        gLogger.setLevel("FATAL")
        try:
            if not requestID:
                return None
            res = self.reqClient.getRequestInfo(requestID)
            if res["OK"]:
                return res["Value"][2]
            gLogger.notice(f"No such request found: {requestID}")
            return None
        except IndexError:
            return None
        finally:
            gLogger.setLevel(level)

    def __getAssignedRequests(self):
        """
        Set member variable to the list of Assigned requests
        """
        if not self.listOfAssignedRequests:
            res = self.reqClient.getRequestIDsList(["Assigned"], limit=10000)
            if res["OK"]:
                self.listOfAssignedRequests = [reqID for reqID, _x, _y in res["Value"]]

    def __printRequestInfo(self, task, lfnsInTask, taskCompleted, status, dmFileStatusComment):
        """
        Print information about a request for a given task

        :param task: TS task
        :type task: dictionary
        :param lfnsInTask: List of LFNs in that task
        :type lfnsInTask: list
        :param taskCompleted: flag telling whether task is supposed to be completed or not
        :type taskCompleted: boolean
        :param status: status of TS files
        :type status: string
        :param dmFileStatusComment: comment
        :type dmFileStatusComment: string
        """
        requestID = int(task["ExternalID"])
        taskID = task["TaskID"]
        taskName = "%08d_%08d" % (self.transID, taskID)
        if taskCompleted and (
            task["ExternalStatus"] not in ("Done", "Failed") or set(status) & {"Assigned", "Problematic"}
        ):
            # If the task is completed but files are not set Processed, wand or fix it
            #   note that this may just be to a delay of the RequestTaskAgent, but it wouldn't harm anyway
            prString = f"\tTask {taskName} is completed: no {dmFileStatusComment} replicas"
            if self.kickRequests:
                res = self.transClient.setFileStatusForTransformation(self.transID, "Processed", lfnsInTask, force=True)
                if res["OK"]:
                    prString += f" - {len(lfnsInTask)} files set Processed"
                else:
                    prString += f" - Failed to set {len(lfnsInTask)} files Processed ({res['Message']})"
            else:
                prString += " - To mark files Processed, use option --KickRequests"
            gLogger.notice(prString)

        if not requestID:
            if task["ExternalStatus"] == "Submitted":
                # This should not happen: a Submitted task should have an associated request: warn or fix
                prString = f"\tTask {taskName} is Submitted but has no external ID"
                if taskCompleted:
                    newStatus = "Done"
                else:
                    newStatus = "Created"
                if self.kickRequests:
                    res = self.transClient.setTaskStatus(self.transID, taskID, newStatus)
                    if res["OK"]:
                        prString += f" - Task reset {newStatus}"
                    else:
                        prString += f" - Failed to set task {newStatus} ({res['Message']})"
                else:
                    prString += f" - To reset task {newStatus}, use option --KickRequests"
                gLogger.notice(prString)
            return 0
        # This method updates self.listOfAssignedRequests
        self.__getAssignedRequests()
        request = None
        res = self.reqClient.peekRequest(requestID)
        if res["OK"]:
            if res["Value"] is not None:
                request = res["Value"]
                requestStatus = request.Status if request.RequestID not in self.listOfAssignedRequests else "Assigned"
                if requestStatus != task["ExternalStatus"]:
                    gLogger.notice(
                        "\tRequest %d status: %s updated last %s" % (requestID, requestStatus, request.LastUpdate)
                    )
                if task["ExternalStatus"] == "Failed":
                    # Find out why this task is failed
                    for i, op in enumerate(request):
                        if op.Status == "Failed":
                            printOperation((i, op), onlyFailed=True)
            else:
                requestStatus = "NotExisting"
        else:
            gLogger.notice("Failed to peek request:", res["Message"])
            requestStatus = "Unknown"

        res = self.reqClient.getRequestFileStatus(requestID, lfnsInTask)
        if res["OK"]:
            reqFiles = res["Value"]
            statFiles = defaultdict(int)
            for stat in reqFiles.values():
                statFiles[stat] += 1
            for stat in sorted(statFiles):
                gLogger.notice("\t%s: %d files" % (stat, statFiles[stat]))
            # If all files failed, set the request as failed
            if requestStatus != "Failed" and statFiles.get("Failed", -1) == len(reqFiles):
                prString = "\tAll transfers failed for that request"
                if not self.kickRequests:
                    prString += ": it should be marked as Failed, use --KickRequests"
                else:
                    request.Status = "Failed"
                    res = self.reqClient.putRequest(request)
                    if res["OK"]:
                        prString += ": request set to Failed"
                    else:
                        prString += f": error setting to Failed: {res['Message']}"
                gLogger.notice(prString)
            # If some files are Scheduled, try and get information about the FTS jobs
            if statFiles.get("Scheduled", 0) and request:
                try:
                    from DIRAC.DataManagementSystem.Client.FTS3Client import FTS3Client

                    fts3Client = FTS3Client()
                    # We take all the operationIDs
                    rmsOpIDs = [o.OperationID for o in request if o.Type == "ReplicateAndRegister"]
                    fts3Ops = []
                    for rmsOpID in rmsOpIDs:
                        res = fts3Client.getOperationsFromRMSOpID(rmsOpID)
                        if not res["OK"]:
                            gLogger.warn(f"Could not get FTS operations associated to RMS Operation {rmsOpID}: {res}")
                            continue
                        fts3Ops.extend(res["Value"])

                    fts3FileStatusCount = defaultdict(int)
                    for fts3Op in fts3Ops:
                        for fts3File in fts3Op.ftsFiles:
                            fts3FileStatusCount[fts3File.status] += 1

                    prStr = []
                    for stat, statusCount in fts3FileStatusCount.items():  # can be an iterator
                        prStr.append("%s:%d" % (stat, statusCount))
                    gLogger.notice(f"\tFTS files statuses: {', '.join(prStr)}")

                    # Get FTS jobs that are still active
                    activeFtsGUID = set()
                    for fts3Op in fts3Ops:
                        for fts3File in fts3Op.ftsFiles:
                            if fts3File.status != "Finished":
                                activeFtsGUID.add(fts3File.ftsGUID)
                                # If asking for Assigned or Problematic  files, list those that are not yet replicated
                                if set(status) & {"Assigned", "Problematic"}:
                                    gLogger.notice(f"\t{fts3File.status} : {fts3File.lfn}")

                    fts3Jobs = []
                    for fts3Op in fts3Ops:
                        for job in fts3Op.ftsJobs:
                            if job.ftsGUID in activeFtsGUID:
                                fts3Jobs.append(job)

                    if not fts3Jobs:
                        gLogger.notice("\tNo active FTS jobs found for that request")
                    else:
                        gLogger.notice("\tActive associated FTS jobs:")
                        for job in fts3Jobs:
                            gLogger.notice(
                                "\t\t%s/fts3/ftsmon/#/job/%s (%s, completed at %s %%)"
                                % (
                                    job.ftsServer.replace(
                                        ":8446", ":8449"
                                    ),  # Submission port is 8446, web port is 8449
                                    job.ftsGUID,
                                    job.status,
                                    job.completeness,
                                )
                            )
                except ImportError as e:
                    gLogger.notice("\tNo FTS information:", repr(e))

        # Kicking stuck requests in status Assigned
        toBeKicked = 0
        assignedReqLimit = datetime.datetime.utcnow() - datetime.timedelta(hours=2)
        if request:
            if request.RequestID in self.listOfAssignedRequests and request.LastUpdate < assignedReqLimit:
                gLogger.notice("\tRequest stuck: %d Updated %s" % (request.RequestID, request.LastUpdate))
                toBeKicked += 1
                if self.kickRequests:
                    res = self.reqClient.putRequest(request)
                    if res["OK"]:
                        gLogger.notice("\tRequest %d is reset" % requestID)
                    else:
                        gLogger.notice("\tError resetting request", res["Message"])
                elif self.cancelRequests:
                    res = self.reqClient.cancelRequest(request)
                    if res["OK"]:
                        gLogger.notice("\tRequest %d is canceled" % requestID)
                    else:
                        gLogger.notice("\tError canceling request", res["Message"])
        else:
            selectDict = {"RequestID": requestID}
            res = self.reqClient.getRequestSummaryWeb(selectDict, [], 0, 100000)
            if res["OK"]:
                params = res["Value"]["ParameterNames"]
                records = res["Value"]["Records"]
                for rec in records:
                    subReqDict = {}
                    subReqStr = ""
                    conj = ""
                    for i, param in enumerate(params):
                        subReqDict.update({param: rec[i]})
                        subReqStr += conj + param + ": " + rec[i]
                        conj = ", "

                    if subReqDict["Status"] == "Assigned" and subReqDict["LastUpdateTime"] < str(assignedReqLimit):
                        gLogger.notice(subReqStr)
                        toBeKicked += 1
                        if self.kickRequests:
                            res = self.reqClient.setRequestStatus(requestID, "Waiting")
                            if res["OK"]:
                                gLogger.notice("\tRequest %d reset Waiting" % requestID)
                            else:
                                gLogger.notice("\tError resetting request %d" % requestID, res["Message"])
        return toBeKicked

    def __checkProblematicFiles(self, nbReplicasProblematic, problematicReplicas, failedFiles):
        """
        Check files found Problematic in TS

        :param nbReplicasProblematic: dict of frequency of nb of replicas
        :type nbReplicasProblematic: dict
        :param problematicReplicas: problematic replicas by SE
        :type problematicReplicas: dict {SE:list of LFNs}
        :param failedFiles: list of files in Failed status
        :type failedFiles: list
        """
        from DIRAC.Core.Utilities.Adler import compareAdler

        gLogger.notice("\nStatistics for Problematic files in FC:")
        existingReplicas = defaultdict(list)
        lfns = set()
        lfnsInFC = set()
        for nb in sorted(nbReplicasProblematic):
            gLogger.notice("   %d replicas in FC: %d files" % (nb, nbReplicasProblematic[nb]))
        # level = gLogger.getLevel()
        # gLogger.setLevel( 'FATAL' )
        lfnCheckSum = {}
        badChecksum = defaultdict(list)
        error = {}
        for se in problematicReplicas:
            lfns.update(problematicReplicas[se])
            if se:
                lfnsInFC.update(problematicReplicas[se])
                res = self.fileCatalog.getFileMetadata(
                    [lfn for lfn in problematicReplicas[se] if lfn not in lfnCheckSum]
                )
                if res["OK"]:
                    success = res["Value"]["Successful"]
                    lfnCheckSum.update({lfn: success[lfn]["Checksum"] for lfn in success})
                res = self.dataManager.getReplicaMetadata(problematicReplicas[se], se)
                if res["OK"]:
                    for lfn in res["Value"]["Successful"]:
                        existingReplicas[lfn].append(se)
                        # Compare checksums
                        checkSum = res["Value"]["Successful"][lfn]["Checksum"]
                        if not checkSum or not compareAdler(checkSum, lfnCheckSum[lfn]):
                            badChecksum[lfn].append(se)
                else:
                    error[se] = res["Message"]
        nbProblematic = len(lfns) - len(existingReplicas)
        nbExistingReplicas = defaultdict(int)
        for lfn in existingReplicas:
            nbReplicas = len(existingReplicas[lfn])
            nbExistingReplicas[nbReplicas] += 1
        nonExistingReplicas = defaultdict(list)
        if error:
            gLogger.notice("Could not get information for some problematic files from SEs:")
            for se, err in error.items():  # can be an iterator
                gLogger.notice(f"\t{se}: {err}")
            gLogger.notice("This check may be totally meaningless, thus no report is made")
            return
        if nbProblematic == len(lfns):
            gLogger.notice(f"None of the {len(lfns)} problematic files actually have an active replica")
        else:
            strMsg = f"Out of {len(lfns)} problematic files"
            if nbProblematic:
                strMsg += ", only %d have an active replica" % (len(lfns) - nbProblematic)
            else:
                strMsg += ", all have an active replica"
            gLogger.notice(strMsg)
            for nb in sorted(nbExistingReplicas):
                gLogger.notice("   %d active replicas: %d files" % (nb, nbExistingReplicas[nb]))
            for se in problematicReplicas:
                lfns = [
                    lfn
                    for lfn in problematicReplicas[se]
                    if lfn not in existingReplicas or se not in existingReplicas[lfn]
                ]
                str2Msg = ""
                if len(lfns):
                    nonExistingReplicas[se].extend(lfns)
                    if not self.fixIt:
                        str2Msg = " Use --FixIt to remove them"
                    else:
                        str2Msg = " Will be removed from FC"
                    strMsg = f"{len(lfns)}"
                else:
                    strMsg = "none"
                if se:
                    gLogger.notice(
                        "   %s : %d replicas of problematic files in FC, %s physically missing.%s"
                        % (str(se).ljust(15), len(problematicReplicas[se]), strMsg, str2Msg)
                    )
                else:
                    gLogger.notice(f"   {''.ljust(15)} : {len(problematicReplicas[se])} files are not in FC")
            lfns = [lfn for lfn in existingReplicas if lfn in failedFiles]
            if lfns:
                prString = "Failed transfers but existing replicas"
                if self.fixIt:
                    prString += ". Use --FixIt to fix it"
                else:
                    for lfn in lfns:
                        res = self.transClient.setFileStatusForTransformation(self.transID, "Unused", lfns, force=True)
                        if res["OK"]:
                            prString += f" - {len(lfns)} files reset Unused"
                gLogger.notice(prString)
        filesInFCNotExisting = list(lfnsInFC - set(existingReplicas))
        if filesInFCNotExisting:
            prString = f"{len(filesInFCNotExisting)} files are in the FC but are not physically existing. "
            if self.fixIt:
                prString += "Removing them now from FC..."
            else:
                prString += "Use --FixIt to remove them"
            gLogger.notice(prString)
            if self.fixIt:
                self.__removeFiles(filesInFCNotExisting)
        if badChecksum:
            prString = f"{len(badChecksum)} files have a checksum mismatch:"
            replicasToRemove = {}
            filesToRemove = []
            for lfn in badChecksum:
                if badChecksum[lfn] == existingReplicas[lfn]:
                    filesToRemove.append(lfn)
                else:
                    replicasToRemove[lfn] = badChecksum[lfn]
            if filesToRemove:
                prString += f" {len(filesToRemove)} files have no correct replica;"
            if replicasToRemove:
                prString += f" {len(replicasToRemove)} files have at least an incorrect replica"
            if not self.fixIt:
                prString += " Use --FixIt to remove them"
            else:
                prString += " Removing them now..."
            gLogger.notice(prString)
            if self.fixIt:
                if filesToRemove:
                    self.__removeFiles(filesToRemove)
                if replicasToRemove:
                    seFiles = defaultdict(list)
                    for lfn, reps in replicasToRemove.items():
                        for se in reps:
                            seFiles[se].append(lfn)
                    for se in seFiles:
                        res = self.dataManager.removeReplica(se, seFiles[se])
                        if not res["OK"]:
                            gLogger.notice("ERROR: error removing replicas", res["Message"])
                        else:
                            gLogger.notice("Successfully removed %d replicas from %s" % (len(seFiles[se], se)))
        elif existingReplicas:
            gLogger.notice("All existing replicas have a good checksum")
        if self.fixIt and nonExistingReplicas:
            nRemoved = 0
            failures = defaultdict(list)
            # If SE == None, the file is not in the FC
            notInFC = nonExistingReplicas.get(None)
            if notInFC:
                nonExistingReplicas.pop(None)
                nRemoved, transRemoved = self.__removeFilesFromTS(notInFC)
                if nRemoved:
                    gLogger.notice(
                        "Successfully removed %d files from transformations %s" % (nRemoved, ",".join(transRemoved))
                    )
            for se in nonExistingReplicas:
                lfns = [lfn for lfn in nonExistingReplicas[se] if lfn not in filesInFCNotExisting]
                res = self.dataManager.removeReplica(se, lfns)
                if not res["OK"]:
                    gLogger.notice(f"ERROR when removing replicas from FC at {se}", res["Message"])
                else:
                    failed = res["Value"]["Failed"]
                    if failed:
                        gLogger.notice(f"Failed to remove {len(failed)} replicas at {se}")
                        gLogger.notice("\n".join(sorted(failed)))
                        for lfn in failed:
                            failures[failed[lfn]].append(lfn)
                    nRemoved += len(res["Value"]["Successful"])
            if nRemoved:
                gLogger.notice(f"Successfully removed {nRemoved} replicas from FC")
            if failures:
                gLogger.notice("Failures:")
                for error in failures:
                    gLogger.notice(f"{error}: {len(failures[error])} replicas")
        gLogger.notice("")

    def __removeFilesFromTS(self, lfnList):
        """
        Set a list of files in status Removed

        :param lfnList: list of LFNs
        :type lfnList: list

        :return : (nb of removed files, list of removed LFNs)
        """
        res = self.transClient.getTransformationFiles({"LFN": lfnList})
        if not res["OK"]:
            gLogger.notice(f"Error getting {len(lfnList)} files in the TS", res["Message"])
            return (None, None)
        transFiles = defaultdict(list)
        removed = 0
        for fd in res["Value"]:
            transFiles[fd["TransformationID"]].append(fd["LFN"])
        for transID, lfns in transFiles.items():  # can be an iterator
            res = self.transClient.setFileStatusForTransformation(transID, "Removed", lfns, force=True)
            if not res["OK"]:
                gLogger.notice(f"Error setting {len(lfns)} files Removed", res["Message"])
            else:
                removed += len(lfns)
        return removed, [str(tr) for tr in transFiles]

    def __removeFiles(self, lfns):
        """
        Remove files from FC and TS

        :param lfns: list of LFNs
        :type lfns: list
        """
        res = self.dataManager.removeFile(lfns)
        if res["OK"]:
            gLogger.notice(f"Successfully removed {len(lfns)} files from FC")
            nRemoved, transRemoved = self.__removeFilesFromTS(lfns)
            if nRemoved:
                gLogger.notice(
                    "Successfully removed %d files from transformations %s" % (nRemoved, ",".join(transRemoved))
                )
        else:
            gLogger.notice("ERROR when removing files from FC:", res["Message"])

    def __getJobStatus(self, job):
        """
        Get the status of a (list of) job, return it formated <major>;<minor>;<application>
        """
        if isinstance(job, str):
            jobs = [int(job)]
        elif isinstance(job, int):
            jobs = [job]
        else:
            jobs = list(int(jid) for jid in job)
        if not self.monitoring:
            self.monitoring = JobMonitoringClient()
        res = self.monitoring.getJobsStatus(jobs)
        if res["OK"]:
            jobStatus = res["Value"]
            res = self.monitoring.getJobsMinorStatus(jobs)
            if res["OK"]:
                jobMinorStatus = res["Value"]
                res = self.monitoring.getJobsApplicationStatus(jobs)
                if res["OK"]:
                    jobApplicationStatus = res["Value"]
        if not res["OK"]:
            return {}
        return {
            job: "%s; %s; %s"
            % (
                jobStatus.get(job, {}).get("Status", "Unknown"),
                jobMinorStatus.get(job, {}).get("MinorStatus", "Unknown"),
                jobApplicationStatus.get(job, {}).get("ApplicationStatus", "Unknown"),
            )
            for job in jobs
        }

    def __getJobSites(self, job):
        """
        Get the status of a (list of) job, return it formated <major>;<minor>;<application>
        """
        if isinstance(job, str):
            jobs = [int(job)]
        elif isinstance(job, int):
            jobs = [job]
        else:
            jobs = list(int(jid) for jid in job)
        if not self.monitoring:
            self.monitoring = JobMonitoringClient()
        res = self.monitoring.getJobsSites(jobs)
        if res["OK"]:
            jobSites = res["Value"]
        else:
            return {}
        return {job: jobSites.get(job, {}).get("Site", "Unknown") for job in jobs}

    def __getJobCPU(self, job):
        """
        Get the status of a (list of) job, return it formated <major>;<minor>;<application>
        """
        if isinstance(job, str):
            jobs = [int(job)]
        elif isinstance(job, int):
            jobs = [job]
        else:
            jobs = list(int(jid) for jid in job)
        if not self.monitoring:
            self.monitoring = JobMonitoringClient()
        jobCPU = {}
        stdoutTag = " (h:m:s)"
        for job in jobs:
            param = "TotalCPUTime(s)"
            res = self.monitoring.getJobParameter(job, param)
            if res["OK"] and param in res["Value"]:
                jobCPU[job] = res["Value"][param] + " s"
            else:
                # Try and get the stdout
                param = "StandardOutput"
                res = self.monitoring.getJobParameter(job, param)
                if res["OK"]:
                    try:
                        for line in res["Value"].get(param, "").splitlines():
                            if stdoutTag in line:
                                cpu = line.split(stdoutTag)[0].split()[-1].split(":")
                                cpu = 3600 * int(cpu[0]) + 60 * int(cpu[1]) + int(cpu[2])
                                jobCPU[job] = "%d s" % cpu
                                break
                    except (IndexError, ValueError):
                        pass
        return jobCPU

    def __checkJobs(self, jobsForLfn, byFiles=False, checkLogs=False, timing=False, lastXML=False):
        """
        Extract all information about jobs referring to list of LFNs

        :param jobsForLfn: dict { lfnString : [jobs] }
        :type jobsForLfn: dict
        :param byFiles: print file information
        :type byFiles: boolean
        :param checkLogs: check also logfiles of jobs
        :type checkLogs: boolean
        :param timing: print timing information for Done jobs
        :type timing: boolean
        """
        if not self.monitoring:
            self.monitoring = JobMonitoringClient()
        failedLfns = defaultdict(list)
        idrLfns = defaultdict(list)
        jobLogURL = {}
        jobSites = {}
        jobCPU = {}
        jobsDone = set()
        for lfnStr, allJobs in jobsForLfn.items():  # can be an iterator
            lfnList = lfnStr.split(",")
            exitedJobs = {}
            allJobs.sort()
            allStatus = self.__getJobStatus(allJobs)
            if "Message" in allStatus:
                gLogger.notice("Error getting jobs statuses:", allStatus["Message"])
                return
            prStr = f"{len(allJobs)} jobs (sorted):" if len(allJobs) > 1 else "job"
            if byFiles or len(lfnList) < 3:
                gLogger.notice(f"\n {len(lfnList)} LFNs: {str(lfnList)} : Status of corresponding {prStr}")
            else:
                gLogger.notice(f"\n {len(lfnList)} LFNs: Status of corresponding {prStr}")
                # Get the sites
            if not timing or len(allJobs) > 1:
                jobSites.update(self.__getJobSites(allJobs))
                jobCPU.update(self.__getJobCPU(allJobs))
                for job, cpu in jobCPU.items():
                    jobCPU[job] = f"{float(cpu.split()[0]):.2f} s"
                # gLogger.notice("Jobs:", ", ".join(allJobs))
                gLogger.notice(
                    "Sites (Job: CPU):",
                    ", ".join(
                        f"{jobSites.get(int(job), 'Site unknown')} " + f"({job}: {jobCPU.get(int(job), 'CPU unknown')})"
                        for job in allJobs
                    ),
                )
            prevStatus = None
            allStatus[sys.maxsize] = ""
            jobs = []
            for job in sorted(allStatus):
                status = allStatus[job]
                job = int(job)
                if status == prevStatus:
                    jobs.append(job)
                    continue
                if not prevStatus:
                    prevStatus = status
                    jobs = [job]
                    continue
                prStr = f"{len(jobs):3} jobs {str(jobs)}" if len(jobs) > 1 else f"Job {jobs[0]}"
                if "Failed" in prevStatus or "Done" in prevStatus or "Completed" in prevStatus:
                    prStr += " terminated with status:"
                else:
                    prStr += " in status:"
                gLogger.notice(prStr, prevStatus)
                majorStatus, minorStatus, applicationStatus = prevStatus.split("; ")
                if majorStatus == "Done":
                    jobsDone.add(jobs[0])
                if majorStatus == "Failed" and (
                    "exited with status" in applicationStatus.lower()
                    or "non-zero exit status" in applicationStatus.lower()
                    or "problem executing application" in applicationStatus.lower()
                ):
                    exitedJobs.update(dict.fromkeys(jobs, applicationStatus))
                elif majorStatus == "Failed" and (
                    applicationStatus == "Failed Input Data Resolution " or minorStatus == "Payload failed"
                ):
                    # Try and find out which file was faulty
                    for jb in jobs:
                        res = self.monitoring.getJobParameter(jb, "DownloadInputData")
                        if res["OK"] and "Failed to download" in res["Value"].get("DownloadInputData", ""):
                            lfns = (
                                res["Value"]["DownloadInputData"].split("Failed to download")[1].split(":")[1].split()
                            )
                            for lfn in lfns:
                                idrLfns[lfn].append(jb)
                elif minorStatus in ("Job stalled: pilot not running", "Watchdog identified this job as stalled"):
                    lastLine = ""
                    # Now get last lines
                    for jb in sorted(jobs) + [0]:
                        line = ""
                        if jb:
                            res = self.monitoring.getJobParameter(jb, "StandardOutput")
                            if res["OK"]:
                                line = (
                                    f"({jobSites.get(jb, 'Unknown')}) "
                                    + res["Value"]
                                    .get("StandardOutput", "stdout not available\n")
                                    .splitlines()[-1]
                                    .split("UTC ")[-1]
                                )
                        if not lastLine:
                            lastLine = line
                            jobs = [jb]
                            continue
                        if line == lastLine:
                            jobs.append(job)
                            continue
                        maxLineLength = 120
                        gLogger.notice(
                            "\t%3d jobs stalled with last line: %s%s"
                            % (len(jobs), lastLine[:maxLineLength], " [...]" if len(lastLine) > maxLineLength else "")
                        )
                        lastLine = line
                        jobs = [jb]
                jobs = [job]
                prevStatus = status
                if exitedJobs:
                    badLfns = {}
                    for lastJob in sorted(exitedJobs, reverse=True)[0:10]:
                        res = self.monitoring.getJobParameter(lastJob, "Log URL")
                        if res["OK"] and "Log URL" in res["Value"]:
                            logURL = res["Value"]["Log URL"].split('"')[1]  # + "/"
                            jobLogURL[lastJob] = logURL
                            lfns = _checkXMLSummary(str(lastJob), logURL)
                            lfns = {_genericLfn(lfn, lfnList): error for lfn, error in lfns.items() if lfn}
                            if lfns:
                                badLfns.update({lastJob: lfns})
                        if lastXML:
                            exit
                    if not badLfns:
                        gLogger.notice("\tNo error was found in XML summary files")
                    else:
                        # lfnsFound is an AND of files found bad in all jobs
                        lfnsFound = set(badLfns[sorted(badLfns, reverse=True)[0]])
                        for lfns in badLfns.values():
                            lfnsFound &= set(lfns)
                        if lfnsFound:
                            for lfn, job, reason in [
                                (x, job, lfns[x]) for job, lfns in badLfns.items() for x in set(lfns) & lfnsFound
                            ]:  # can be an iterator
                                if job in exitedJobs:
                                    exitStatus = exitedJobs[job].split("status ")
                                    if len(exitStatus) == 2:
                                        reason = f"(exit code {exitStatus[1]}) was " + reason
                                failedLfns[(lfn, reason)].append(job)
                        else:
                            gLogger.notice("No common error was found in all XML summary files")
                    exitedJobs = {}
        if idrLfns:
            gLogger.notice("\nSummary of failures due to Input Data Resolution\n")
            for lfn, jobs in idrLfns.items():  # can be an iterator
                jobs = sorted(set(jobs))
                js = {jobSites.get(job, "Unknown") for job in jobs}
                if len(js) == 1:
                    gLogger.notice(
                        "ERROR ==> %s could not be downloaded by jobs: %s (%s)"
                        % (lfn, ", ".join(str(job) for job in jobs), list(js)[0])
                    )
                else:
                    gLogger.notice(
                        "ERROR ==> %s could not be downloaded by jobs: %s"
                        % (lfn, ", ".join("%d (%s)" % (job, jobSites.get(job, "Unknown")) for job in jobs))
                    )

        if timing and jobsDone:
            timingInfo = {}
            progressBar = ProgressBar(len(jobsDone), title=f"\nGet timing information for {len(jobsDone):d} Done jobs")
            for job in jobsDone:
                progressBar.loop()
                res = self.monitoring.getJobParameter(job, "Log URL")
                if res["OK"] and "Log URL" in res["Value"]:
                    logURL = res["Value"]["Log URL"].split('"')[1]  # + "/"
                    ti = _getTiming(logURL)
                    if ti:
                        timingInfo[job] = ti
            progressBar.endLoop()
            gLogger.notice("\nTiming information for Done jobs:\n")
            for job in sorted(timingInfo):
                ti = timingInfo[job]
                gLogger.notice(
                    f"Job {job} - Time for {ti['Entries']} events: {ti['Total']:.1f} seconds,"
                    + " per event (min, max, mean) = "
                    + f"{ti['min']:.3f} s, {ti['max']:.1f} s, {ti['Clock']:.3f} s"
                )

        if failedLfns:
            gLogger.notice("\nSummary of failures due to: Application Exited with non-zero status\n")
            lfnDict = {}
            partial = "Partial (last event "
            for (lfn, reason), jobs in list(failedLfns.items()):
                if partial not in reason:
                    continue
                failedLfns.pop((lfn, reason))
                otherReasons = lfnDict.get(lfn)
                if not otherReasons:
                    lfnDict[lfn] = (reason, jobs)
                else:
                    lastEvent = int(reason.split(partial)[1][:-1])
                    lfnDict[lfn] = (otherReasons[0][:-1] + ",%d)" % lastEvent, otherReasons[1] + jobs)
            for lfn, (reason, jobs) in lfnDict.items():  # can be an iterator
                failedLfns[(lfn, reason)] = jobs

            for (lfn, reason), jobs in failedLfns.items():  # can be an iterator
                js = {jobSites.get(job, "Unknown") for job in jobs}
                # If only one site, print it once only
                if len(js) == 1:
                    gLogger.notice(
                        "ERROR ==> %s %s during processing from jobs: %s (%s)"
                        % (lfn, reason, ", ".join(str(job) for job in jobs), list(js)[0])
                    )
                else:
                    gLogger.notice(
                        "ERROR ==> %s %s during processing from jobs: %s"
                        % (lfn, reason, ", ".join("%d (%s)" % (job, jobSites.get(job, "Unknown")) for job in jobs))
                    )
                # Get an example log if possible
                if checkLogs:
                    logDump = _checkLog(jobLogURL[jobs[0]])
                    prStr = f"\tFrom logfile of job {jobs[0]}: "
                    if len(logDump) == 1:
                        prStr += logDump[0]
                    else:
                        prStr += "\n\t".join([""] + logDump)
                    gLogger.notice(prStr)
        gLogger.notice("")

    def __checkRunsToFlush(self, runID, transFilesList, runStatus, evtType=90000000, fileTypes=None):
        """
        Check whether the run is flushed and if not, why it was not

        :param runID: run number
        :type runID: int
        :param transFilesList: list of TS files
        :type transFilesList: list
        :param runStatus: current status of run
        :type runStatus: string
        :param evtType: event type
        :type evtType: int
        :param fileTypes: file types
        :type fileTypes: list
        """
        if not runID:
            gLogger.notice("Cannot check flush status for run", runID)
            return
        rawFiles = self.pluginUtil.getNbRAWInRun(runID, evtType)
        if not rawFiles:
            gLogger.notice(f"Run {runID} is not finished...")
            return
        paramValues = [""]
        if "FileType" in self.transPlugin:
            param = "FileType"
        elif "EventType" in self.transPlugin:
            param = "EventType"
        else:
            param = ""
        if param:
            res = self.bkClient.getFileMetadata([fileDict["LFN"] for fileDict in transFilesList])
            if not res["OK"]:
                gLogger.notice("Error getting files metadata", res["Message"])
                DIRAC.exit(2)
            evtType = list(res["Value"]["Successful"].values())[0]["EventType"]
            if isinstance(fileTypes, (list, set)) and param == "FileType":
                paramValues = sorted(fileTypes)
            elif evtType and param == "EventType":
                paramValues = [evtType]
            else:
                paramValues = sorted({meta[param] for meta in res["Value"]["Successful"].values() if param in meta})
        ancestors = defaultdict(list)
        # print "*** Param values", ','.join( paramValues )
        for paramValue in paramValues:
            try:
                nbAnc = self.pluginUtil.getRAWAncestorsForRun(runID, param, paramValue)
                # print '*** For %s = %s: %d ancestors' % ( param, paramValue, nbAnc )
                ancestors[nbAnc].append(paramValue)
            except Exception as e:  # pylint: disable=broad-except
                gLogger.exception("Exception calling pluginUtilities:", lException=e)
        prStr = ""
        for anc in sorted(ancestors):
            ft = ancestors[anc]
            if ft and ft != [""]:
                prStr += "%d ancestors found for %s; " % (anc, ",".join(ft))
            else:
                prStr = "%d ancestors found" % anc
        toFlush = False
        flushError = False
        for ancestorRawFiles in ancestors:
            if rawFiles == ancestorRawFiles:
                toFlush = True
            elif ancestorRawFiles > rawFiles:
                flushError = True

        # Missing ancestors, find out which ones
        if not toFlush and not flushError:
            gLogger.notice(
                "Run %s flushed: %s while %d RAW files"
                % ("should not be" if runStatus == "Flush" else "not", prStr, rawFiles)
            )
            # Find out which ones are missing
            res = self.bkClient.getRunFiles(int(runID))
            if not res["OK"]:
                gLogger.notice("Error getting run files", res["Message"])
            else:
                res = self.bkClient.getFileMetadata(sorted(res["Value"]))
                if not res["OK"]:
                    gLogger.notice("Error getting files metadata", res["Message"])
                else:
                    metadata = res["Value"]["Successful"]
                    runRAWFiles = {
                        lfn
                        for lfn, meta in metadata.items()  # can be an iterator
                        if meta["EventType"] == evtType and meta["GotReplica"] == "Yes"
                    }
                    badRAWFiles = {
                        lfn for lfn, meta in metadata.items() if meta["EventType"] == evtType
                    } - runRAWFiles  # can be an iterator
                    # print len( runRAWFiles ), 'RAW files'
                    allAncestors = set()
                    for paramValue in paramValues:
                        # This call returns only the base name of LFNs as they are unique
                        ancFiles = self.pluginUtil.getRAWAncestorsForRun(runID, param, paramValue, getFiles=True)
                        allAncestors.update(ancFiles)
                    # Remove ancestors from their basename in a list of LFNs
                    missingFiles = {lfn for lfn in runRAWFiles if os.path.basename(lfn) not in allAncestors}
                    if missingFiles:
                        gLogger.notice("Missing RAW files:\n\t%s" % "\n\t".join(sorted(missingFiles)))
                    else:
                        if badRAWFiles:
                            gLogger.notice(f"Indeed {len(badRAWFiles)} RAW files have no replicas and therefore...")
                        else:
                            gLogger.notice("No RAW files are missing in the end and therefore...")
                        rawFiles = len(runRAWFiles)
                        toFlush = True
        if toFlush:
            gLogger.notice(
                "Run %s flushed: %d RAW files and ancestors found"
                % ("correctly" if runStatus == "Flush" else "should be", rawFiles)
            )
            if runStatus != "Flush":
                if self.fixIt:
                    res = self.transClient.setTransformationRunStatus(self.transID, runID, "Flush")
                    if res["OK"]:
                        gLogger.notice("Run %d successfully flushed" % runID)
                    else:
                        gLogger.notice("Error flushing run %d" % runID, res["Message"])
                else:
                    gLogger.notice("Use --FixIt to flush the run")
        if flushError:
            gLogger.notice(
                "More ancestors than RAW files (%d) for run %d ==> Problem!\n\t%s"
                % (rawFiles, runID, prStr.replace("; ", "\n\t"))
            )

    def __checkWaitingTasks(self):
        """
        Check waiting tasks:
        They can be really waiting (assigned files), Failed, Done or just orphan (no files)
        """
        res = self.transClient.getTransformationTasks({"TransformationID": self.transID, "ExternalStatus": "Waiting"})
        if not res["OK"]:
            gLogger.notice("Error getting waiting tasks:", res["Message"])
            return
        tasks = res["Value"]
        taskStatuses = defaultdict(list)
        gLogger.notice(f"Found {len(tasks)} waiting tasks")
        for task in tasks:
            fileDicts = self.transClient.getTransformationFiles(
                {"TransformationID": self.transID, "TaskID": task["TaskID"]}
            ).get("Value", [])
            if not fileDicts:
                status = "Orphan"
            else:
                statuses = sorted({fileName["Status"] for fileName in fileDicts})
                if statuses == ["Processed"]:
                    status = "Done"
                elif statuses == ["Failed"]:
                    status = "Failed"
                else:
                    status = None
            if status:
                taskStatuses[status].append((task["TaskID"], int(task["ExternalID"])))
        if not taskStatuses:
            gLogger.notice("All tasks look OK")
            return
        for status in taskStatuses:
            gLogger.notice(f"{len(taskStatuses[status])} tasks are indeed {status}")
            if self.kickRequests:
                fixed = 0
                ids = taskStatuses[status]
                if status == "Orphan":
                    status = "Failed"
                for taskID, requestID in ids:
                    requestName = self.__getRequestName(requestID)
                    if requestName:
                        res = self.transClient.setTaskStatus(self.transID, taskID, status)
                        if not res["OK"]:
                            gLogger.notice(f"Error setting task {requestID} to {status}", res["Message"])
                        res = self.reqClient.peekRequest(requestID)
                        if res["OK"]:
                            request = res["Value"]
                            request.Status = status
                            res = self.reqClient.putRequest(request)
                            if res["OK"]:
                                fixed += 1
                        if not res["OK"]:
                            gLogger.notice(f"Error setting {requestID} to {status}", res["Message"])
                gLogger.notice("\t%d requests set to status %s" % (fixed, status))
        if not self.kickRequests:
            gLogger.notice("Use --KickRequests to fix them")

    def __getRunsForFiles(self, lfnList):
        """
        Get run list for a set of files
        """
        transFiles = self.__getFilesForRun(lfnList=lfnList)
        return list({str(f["RunNumber"]) for f in transFiles})

    def __checkInput(self):
        """
        Compares the transformation files with the result of the BK query to find missing or extra files
        """
        # Get the input BK query and check against all files
        res = self.transClient.getBookkeepingQuery(self.transID)
        if res["OK"] and res["Value"]:
            bkQuery = res["Value"]
        else:
            gLogger.notice("No BKQuery for this transformation")
            return

        inputProd = bkQuery.get("ProductionID", None)
        bkQuery.update({"ReplicaFlag": "All"})
        # Get files list from BK
        progressBar = ProgressBar(1, title="Getting files from BK")
        res = self.bkClient.getFiles(bkQuery)
        if not res["OK"]:
            bkFilesList = set()
            progressBar.endLoop(f"Error during BK query:, {res['Message']}")
        else:
            bkFilesList = set(res["Value"])
            progressBar.endLoop(f"Obtained {len(bkFilesList)} files", timing=True)
        if len(bkFilesList) > 50000 or not bkFilesList:
            # If the number of files is too large, get run list and then files by run
            progressBar = ProgressBar(1, title=f"Get the runs as the number of expected files is {len(bkFilesList)}")
            runs = self.__getRuns()
            progressBar.endLoop(f"Obtained {len(runs)} runs", timing=True)
            if bkFilesList:
                chunk = max(1, int(20000 * len(runs) / len(bkFilesList)))
                prStr = ""
            else:
                chunk = 5
                prStr = "and BK "
            progressBar = ProgressBar(
                len(runs), chunk=chunk, title=f"Getting files from TS {prStr}for {len(runs)} runs"
            )
            trFiles = []
            for runChunk in breakListIntoChunks(runs, chunk):
                runList = [run["RunNumber"] for run in runChunk]
                if prStr:
                    bkQuery["RunNumber"] = runList
                    res = self.bkClient.getFiles(bkQuery)
                    if not res["OK"]:
                        progressBar.endLoop(f"Error during BK query:, {res['Message']}")
                        return
                    bkFilesList.update(res["Value"])
                trFiles += self.__getFilesForRun(runID=runList)
                progressBar.loop()
        else:
            progressBar = ProgressBar(1, title="Getting files from TS")
            trFiles = self.__getFilesForRun()
        progressBar.endLoop(f"Obtained {len(trFiles)} files", timing=True)
        if not trFiles:
            gLogger.notice(f"No files obtained from TS ({len(bkFilesList)} from BK), hence no check...")
            return
        transFilesList = {filesDict["LFN"] for filesDict in trFiles}
        missingFiles = bkFilesList - transFilesList
        if missingFiles:
            # Now check if these files exist
            missingFiles = self.__getReplicas(missingFiles)
        extraFiles = transFilesList - bkFilesList
        if not missingFiles and not extraFiles:
            gLogger.notice(f"All is OK with the {len(bkFilesList)} input files of transformation {self.transID}")
            return
        baseName = f"CheckTransformationInput-{self.transID}"
        suffix = ""
        nb = 0
        while True:
            fileName = baseName + f"{suffix}.txt"
            if not os.path.exists(fileName):
                break
            nb += 1
            suffix = "-%d" % nb
        fp = open(fileName, "w")
        if missingFiles:
            prStr = "(first 10 files):" if len(missingFiles) > 10 else ":"
            gLogger.notice(f"There are {len(missingFiles)} missing files in transformation {self.transID} {prStr}")
            for n, lfn in enumerate(sorted(missingFiles)):
                fp.write(f"\nMissingFiles {lfn}")
                if n < 10:
                    gLogger.notice(f"\t{lfn}")
            gLogger.notice(f"Complete list of files with: grep MissingFiles {fileName}")
            if inputProd:
                gLogger.notice(
                    "You may want to run the following command:",
                    f"\ngrep MissingFiles {fileName} | dirac-bookkeeping-get-file-ancestors |"
                    f" grep -v {inputProd} | grep '/lhcb/' | dirac-production-check-descendants {inputProd}",
                )
        if extraFiles:
            prStr = "(first 10 files):" if len(extraFiles) > 10 else ":"
            gLogger.notice(f"There are {len(extraFiles)} extra files in transformation {self.transID} {prStr}")
            for n, lfn in enumerate(sorted(extraFiles)):
                fp.write(f"\nExtraFiles {lfn}")
                if n < 10:
                    gLogger.notice(f"\t{lfn}")
            gLogger.notice(f"Complete list of files with: grep ExtraFiles {fileName}")
        fp.close()
        return

    def debugTransformation(self, dmScript, infoList, statusList):
        """
        Actual script execution code: parses arguments and implements the checking logic

        :param dmScript: DMScript object to be parsed
        :type dmScript: DMScript
        :param infoList: list of possible information
        :type infoList: tuple
        :param statusList: list of possible statuses
        :type statusList: tuple
        """

        verbose = False
        byFiles = False
        byRuns = False
        byTasks = False
        byJobs = False
        dumpFiles = False
        status = []
        taskList = []
        seList = []
        runList = None
        justStats = False
        fixRun = False
        allTasks = False
        checkFlush = False
        checkWaitingTasks = False
        checkSubmittedTasks = False
        checkLogs = False
        jobList = []
        exceptProd = None
        timing = False
        since = None
        checkInput = False

        switches = Script.getUnprocessedSwitches()
        for opt, val in switches:
            if opt == "Info":
                infos = val.split(",")
                for val in infos:
                    val = val.lower()
                    if val not in infoList:
                        gLogger.notice(f"Unknown information... Select in {str(infoList)}")
                        DIRAC.exit(0)
                    elif val == "files":
                        byFiles = True
                    elif val == "runs":
                        byRuns = True
                    elif val == "tasks":
                        byTasks = True
                    elif val == "jobs":
                        byJobs = True
                    elif val == "alltasks":
                        allTasks = True
                    elif val == "flush":
                        byRuns = True
                        checkFlush = True
                    elif val == "log":
                        checkLogs = True
                    elif val == "timing":
                        timing = True
                        byJobs = True
                    elif val == "input":
                        checkInput = True
            elif opt == "Status":
                status = val.split(",")
                val = set(status) - set(statusList)
                if val:
                    gLogger.notice(f"Unknown status {sorted(val)}... Select in {str(statusList)}")
                    DIRAC.exit(1)
            elif opt == "Runs":
                runList = val.split(",")
            elif opt == "SEs":
                seList = val.split(",")
            elif opt in ("v", "Verbose"):
                verbose = True
            elif opt == "Tasks":
                taskList = [int(x) for x in val.split(",")]
            elif opt == "KickRequests":
                self.kickRequests = True
            elif opt == "CancelRequests":
                self.cancelRequests = True
            elif opt == "DumpFiles":
                dumpFiles = True
            elif opt == "Statistics":
                justStats = True
            elif opt == "FixIt":
                self.fixIt = True
            elif opt == "FixRun":
                fixRun = True
                runList = ["0"]
            elif opt == "CheckWaitingTasks":
                checkWaitingTasks = True
            elif opt == "CheckSubmittedTasks":
                checkSubmittedTasks = True
                byTasks = True
            elif opt == "Jobs":
                # in TransformationTasks job is a string
                jobList = [job for job in val.split(",") if job.isdigit()]
            elif opt == "ExceptActiveRunsFromProduction":
                exceptProd = int(val)
            elif opt == "Since":
                since = val

        lfnList = dmScript.getOption("LFNs", [])
        if lfnList:
            byFiles = True
        if dumpFiles:
            byFiles = True
        if allTasks:
            byTasks = True
        if byJobs:
            allTasks = True
            byTasks = False
        if fixRun and not status:
            status = "Unused"

        transList = getTransformations(Script.getPositionalArgs()) if not jobList and not checkSubmittedTasks else []

        improperJobs = []
        # gLogger.setLevel( 'INFO' )

        # If looking for MaxReset files, and no transformation is specified, get the list
        if status in (["MaxReset"], ["Problematic"]) and not transList:
            res = self.transClient.getTransformationFiles({"Status": status}, newer=since)
            if not res["OK"]:
                gLogger.notice("Failed getting MaxReset files", res["Message"])
                DIRAC.exit(1)
            transList = getTransformations([",".join({str(fd["TransformationID"]) for fd in res["Value"]})])
            if transList:
                gLogger.notice(
                    "Transformations to be debugged", f": {','.join(str(trans) for trans in sorted(transList))}\n"
                )

        # Get list of transformations from the list of jobs
        if jobList:
            # Check first which JobGroup jobs come from
            transJobs = defaultdict(list)
            badJobs = []
            if not self.monitoring:
                self.monitoring = JobMonitoringClient()
            for job in jobList:
                trans = self.monitoring.getJobAttribute(int(job), "JobGroup").get("Value")
                if trans.isdigit() and (not transList or int(trans) in transList):
                    transJobs[int(trans)].append(job)
                else:
                    badJobs.append(job)
            if badJobs:
                gLogger.notice("Jobs are not production jobs", ",".join(badJobs))
            transList = defaultdict(list)
            for trans, jobs in transJobs.items():
                res = self.transClient.getTransformationTasks({"TransformationID": trans, "ExternalID": jobs})
                if not res["OK"]:
                    gLogger.notice("Error getting jobs:", res["Message"])
                else:
                    for task in res["Value"]:
                        transList[trans].append(task["TaskID"])
            if transList:
                gLogger.notice(
                    "Transformations to be debugged", f": {','.join(str(trans) for trans in sorted(transList))}\n"
                )

        # Get list of transformations that have tasks in status Submitted
        if checkSubmittedTasks:
            res = self.transClient.getTransformationTasks({"ExternalStatus": "Submitted", "ExternalID": "0"})
            if not res["OK"]:
                gLogger.notice("Error getting submitted tasks:", res["Message"])
            elif not res["Value"]:
                gLogger.notice("No tasks submitted with no task ID")
            else:
                transList = defaultdict(list)
                for task in res["Value"]:
                    transList[task["TransformationID"]].append(task["TaskID"])

        # Get list of transformations if not given but a list of LFNs
        if not transList and lfnList:
            res = self.transClient.getTransformationFiles({"LFN": lfnList})
            if res["OK"]:
                transList = {tr["TransformationID"] for tr in res["Value"]}

        # At this point we should have a list of transformations, othewise stop
        if not transList:
            gLogger.notice("No valid transformation found...")
            DIRAC.exit(0)

        transSep = ""
        for transID in sorted(transList):
            self.transID = transID
            if isinstance(transList, dict):
                taskList = transList[transID]
            problematicReplicas = defaultdict(list)
            failedFiles = []
            nbReplicasProblematic = defaultdict(int)
            taskType, queryFileTypes = self.__getTransformationInfo(transSep)
            if taskType is None:
                continue
            transSep = "==============================\n"
            if checkInput:
                # This will check the input files of the transformation vs its BK query
                self.__checkInput()
                continue

            dmFileStatusComment = {"Replication": "missing", "Removal": "remaining"}.get(self.transType, "absent")
            if not transID:
                continue
            #####################
            # If just statistics are requested
            if justStats:
                improperJobs += self.__justStats(status, seList)
                continue
            #####################
            # If only checking waiting tasks
            if checkWaitingTasks:
                self.__checkWaitingTasks()
                continue

            self.pluginUtil = PluginUtilities(
                self.transPlugin,
                transClient=self.transClient,
                dataManager=self.dataManager,
                bkClient=self.bkClient,
                debug=verbose,
                transID=transID,
            )
            # Select runs, or all
            # If byRuns is requested but LFNs are provided, get the list of runs
            if byRuns and lfnList:
                runList = self.__getRunsForFiles(lfnList)
                gLogger.notice(f"Files are from runs {','.join(runList)}")
            runsDictList = self.__getRuns(runList=runList, byRuns=byRuns, seList=seList, status=status, since=since)
            # If some runs must be excluded, remove them
            if status and byRuns and exceptProd:
                exceptRunsDict = self.__getRuns(
                    runList=[],
                    byRuns=byRuns,
                    seList=seList,
                    status=["Assigned", "Problematic", "Unused", "MaxReset"],
                    transID=exceptProd,
                    since=since,
                )
                exceptRuns = [run["RunNumber"] for run in exceptRunsDict]
                for run in list(runsDictList):
                    if run["RunNumber"] in exceptRuns:
                        runsDictList.remove(run)
            else:
                exceptRuns = []
            if runList and [run["RunNumber"] for run in runsDictList] == [None]:
                gLogger.notice("None of the requested runs was found, exit")
                DIRAC.exit(0)
            if status and byRuns and not runList:
                if not runsDictList:
                    if exceptRuns:
                        gLogger.notice(
                            "No runs left, runs %s have non-processed files in production %d"
                            % (",".join([str(r) for r in exceptRuns]), exceptProd)
                        )
                    else:
                        gLogger.notice("No runs found...")
                else:
                    gLogger.notice(
                        "%d runs found: %s"
                        % (len(runsDictList), ",".join(str(runDict["RunNumber"]) for runDict in runsDictList))
                    )
                    if exceptRuns:
                        gLogger.notice(
                            "Runs %s excluded: they have non-processed files in production %d"
                            % (",".join([str(r) for r in exceptRuns]), exceptProd)
                        )
            seStat = defaultdict(int)
            allFiles = []
            toBeKicked = 0

            # Loop over all requested runs or just all in one go (runID == None)
            runsInTable = {}
            for runDict in runsDictList:
                runID = runDict["RunNumber"]
                selectedSEs = runDict.get("SelectedSite", "None").split(",")
                runStatus = runDict.get("Status")

                # Get all files from TransformationDB
                transFilesList = sorted(
                    self.__getFilesForRun(
                        runID=runID, status=status, lfnList=lfnList, seList=seList, taskList=taskList, since=since
                    ),
                    key=lambda d: (d["TaskID"] if d["TaskID"] is not None else 0, d["LFN"]),
                )
                transFilesLFNsSet = {fileDict["LFN"] for fileDict in transFilesList}
                if jobList and allTasks:
                    taskList = []
                if lfnList:
                    notFoundFiles = set(lfnList) - transFilesLFNsSet
                    if notFoundFiles:
                        gLogger.notice(f"Some requested files were not found in transformation ({len(notFoundFiles)}):")
                        gLogger.notice("\n\t".join(notFoundFiles))

                # No files found in transDB
                if not transFilesList:
                    if not byRuns:
                        gLogger.notice("No files found with given criteria")
                    continue

                # Run display
                if byRuns and runID:
                    files, processed = self.__filesProcessed(runID)
                    if runID:
                        prString = "Run: %d" % runID
                    else:
                        prString = "No run"
                    if runStatus:
                        prString += f" ({runStatus})"
                    tasks = set()
                    nFilesNoTask = 0
                    for fileDict in transFilesList:
                        if fileDict["TaskID"]:
                            tasks.add(fileDict["TaskID"])
                        else:
                            nFilesNoTask += 1
                    prString += " - %d files (" % files
                    if nFilesNoTask:
                        prString += "%d files in no task, " % nFilesNoTask
                    prString += "%d tasks, SelectedSite: %s), %d processed, status: %s" % (
                        len(tasks),
                        selectedSEs,
                        processed,
                        runStatus,
                    )
                    gLogger.notice(prString)

                if checkFlush or ((byRuns and runID) and status == "Unused" and "WithFlush" in self.transPlugin):
                    if runStatus != "Flush":
                        # Check if the run should be flushed
                        lfn = transFilesList[0]["LFN"]
                        evtType = self.pluginUtil.getMetadataFromTSorBK(lfn, "EventType").get(lfn, 90000000)
                        self.__checkRunsToFlush(
                            runID, transFilesList, runStatus, evtType=evtType, fileTypes=queryFileTypes
                        )
                    else:
                        gLogger.notice("Run %d is already flushed" % runID)

                prString = f"{len(transFilesList)} files found"
                nbUniqueFiles = len({t["LFN"] for t in transFilesList})
                if nbUniqueFiles != len(transFilesList):
                    prString += " (%d unique LFNs)" % nbUniqueFiles
                if status:
                    prString += f" with status {status}"
                if runID:
                    prString += " in run %d" % runID
                if since:
                    prString += f" since {since}"
                gLogger.notice(prString + "\n")

                # Extract task list
                filesWithRunZero = []
                filesWithNoRunTable = []
                problematicFiles = []
                taskDict = defaultdict(list)
                for fileDict in transFilesList:
                    if not allTasks:
                        taskID = fileDict["TaskID"] if fileDict["TaskID"] is not None else 0
                        taskDict[taskID].append(fileDict["LFN"])
                        if "Problematic" in status and not fileDict["TaskID"]:
                            problematicFiles.append(fileDict["LFN"])
                    else:
                        # Get all tasks associated to that file
                        res = self.transClient.getTableDistinctAttributeValues(
                            "TransformationFileTasks",
                            ["TaskID"],
                            {"TransformationID": transID, "FileID": fileDict["FileID"]},
                        )
                        if not res["OK"]:
                            gLogger.notice(f"Error when getting tasks for file {fileDict['LFN']}")
                        else:
                            for taskID in res["Value"]["TaskID"]:
                                if taskID is None:
                                    taskID = 0
                                taskDict[taskID].append(fileDict["LFN"])
                    fileRun = fileDict.get("RunNumber")
                    fileLfn = fileDict["LFN"]
                    if byFiles:
                        gLogger.notice(
                            "%s - Run: %s - Status: %s - UsedSE: %s - ErrorCount %s"
                            % (fileLfn, fileRun, fileDict["Status"], fileDict["UsedSE"], fileDict["ErrorCount"])
                        )
                    if not fileRun and "/MC" not in fileLfn:
                        filesWithRunZero.append(fileLfn)
                    if fileRun:
                        runInTable = runsInTable.get(fileRun)
                        if not runInTable:
                            runInTable = self.__getRuns(runList=[str(fileRun)], byRuns=True)[0].get("RunNumber")
                            runsInTable[fileRun] = runInTable
                        if not runInTable:
                            filesWithNoRunTable.append(fileLfn)

                # Files with run# == 0
                transWithRun = self.transPlugin in Operations().getValue("TransformationPlugins/PluginsWithRunInfo", [])
                if filesWithRunZero and transWithRun:
                    self.__fixRunNumber(filesWithRunZero, fixRun)
                if filesWithNoRunTable and transWithRun:
                    self.__fixRunNumber(filesWithNoRunTable, fixRun, noTable=True)

                # Problematic files
                if problematicFiles and not byFiles:
                    _checkReplicasForProblematic(
                        problematicFiles,
                        self.__getReplicas(problematicFiles),
                        nbReplicasProblematic,
                        problematicReplicas,
                    )

                # Check files with missing FC
                if status:
                    self.__checkFilesMissingInFC(transFilesList, status)

                ####################
                # Now loop on all tasks
                jobsForLfn = defaultdict(list)
                if verbose:
                    gLogger.notice("Tasks:", ",".join(str(taskID) for taskID in sorted(taskDict)))
                if allTasks:
                    # Sort tasks by LFNs in order to print them together
                    lfnTask = defaultdict(list)
                    for taskID in sorted(taskDict):
                        for lfn in taskDict[taskID]:
                            lfnTask[lfn].append(taskID)
                    sortedTasks = []
                    for lfn in sorted(lfnTask):
                        for taskID in lfnTask[lfn]:
                            if taskID not in sortedTasks:
                                sortedTasks.append(taskID)
                else:
                    sortedTasks = sorted(taskDict)
                lfnsInTask = []
                allTaskIDs = sorted(taskList) if taskList else sortedTasks
                allTaskDefs = self.__getTasks(allTaskIDs)
                allTasksLFNs = list(itertools.chain(*taskDict.values()))
                allTasksReplicas = self.__getReplicas(allTasksLFNs)
                for taskID in allTaskIDs:
                    if allTasks and not byJobs and taskDict[taskID] != lfnsInTask:
                        gLogger.notice("")
                    if taskID not in taskDict:
                        gLogger.notice(f"Task {taskID} not found in the transformation files table")
                        lfnsInTask = []
                    else:
                        lfnsInTask = taskDict[taskID]
                    task = allTaskDefs.get(taskID)
                    if not task:
                        continue
                    # Analyse jobs
                    if byJobs and taskType == "Job":
                        job = task["ExternalID"]
                        lfns = set(lfnsInTask if lfnsInTask else [""]) & transFilesLFNsSet
                        if not jobList or job in jobList:
                            jobsForLfn[",".join(sorted(lfns))].append(job)
                        if not byFiles and not byTasks:
                            continue
                    nfiles = len(lfnsInTask)
                    allFiles += lfnsInTask
                    # Take the replicas from the specific task
                    # We have to make sure all the lfns are in allTasksReplicas
                    # because some file may not exist
                    replicas = {k: allTasksReplicas[k] for k in allTasksReplicas.keys() & set(lfnsInTask)}
                    targetSE = task.get("TargetSE")
                    if targetSE == "None":
                        targetSE = "Some"
                    # Accounting per SE
                    listSEs = targetSE.split(",")
                    # If a list of LFNs is provided, we may not have all files in the task, set to False
                    taskCompleted = not lfnList

                    # Check problematic files
                    if "Problematic" in status:
                        _checkReplicasForProblematic(lfnsInTask, replicas, nbReplicasProblematic, problematicReplicas)

                    # Collect statistics per SE
                    for lfn, reps in replicas.items():
                        taskCompleted = self.__fillStatsPerSE(seStat, reps, listSEs) and taskCompleted

                    # Print out task's information
                    if byTasks:
                        # print task
                        prString = "TaskID: %s (created %s, updated %s) - %d files" % (
                            taskID,
                            task["CreationTime"],
                            task["LastUpdateTime"],
                            nfiles,
                        )
                        if byFiles and lfnsInTask:
                            sep = ","  # if sys.stdout.isatty() else '\n'
                            prString += " (" + sep.join(lfnsInTask) + ")"
                        prString += f"- {taskType}: {task['ExternalID']} - Status: {task['ExternalStatus']}"
                        if targetSE:
                            prString += f" - TargetSE: {targetSE}"
                        gLogger.notice(prString)

                        # More information from Request tasks
                        if taskType == "Request":
                            toBeKicked += self.__printRequestInfo(
                                task, lfnsInTask, taskCompleted, status, dmFileStatusComment
                            )
                        elif task["ExternalStatus"] in ("Failed", "Done", "Completed"):
                            # Get job statuses
                            jobID = int(task["ExternalID"])
                            jobStatus = self.__getJobStatus(jobID)
                            jobSite = self.__getJobSites(jobID)
                            gLogger.notice(f"Job status at {jobSite[int(jobID)]}:", jobStatus[jobID])
                        if not allTasks:
                            gLogger.notice("")
                if byJobs and jobsForLfn:
                    self.__checkJobs(jobsForLfn, byFiles, checkLogs, timing)
            if "Problematic" in status and nbReplicasProblematic and not byFiles:
                self.__checkProblematicFiles(nbReplicasProblematic, problematicReplicas, failedFiles)
            if toBeKicked:
                if self.kickRequests:
                    gLogger.notice("%d requests have been kicked" % toBeKicked)
                else:
                    gLogger.notice(
                        f"{toBeKicked} requests are eligible to be kicked or canceled"
                        + " (use option --KickRequests or --CancelRequests)"
                    )

            ###########
            # Print out statistics of SEs if relevant (DMS)
            if seStat["Total"] and self.transType in self.dataManagerTransTypes and not checkSubmittedTasks:
                gLogger.notice("%d files found in tasks" % seStat["Total"])
                seStat.pop("Total")
                if None in seStat:
                    gLogger.notice("Found without replicas: %d files" % seStat[None])
                    seStat.pop(None)
                gLogger.notice(f"Statistics per {dmFileStatusComment} SE:")
                selectedSEs = sorted(seStat)
                found = False
                for se in selectedSEs:
                    gLogger.notice("%s %d files" % (se, seStat[se]))
                    found = True
                if not found:
                    gLogger.notice("... None ...")
            elif self.transType == "Removal" and (not status or "MissingInFC" not in status):
                gLogger.notice("All files have been successfully removed!")

            # All files?
            if dumpFiles and allFiles:
                gLogger.notice("List of files found:")
                gLogger.notice("\n".join(allFiles))

        if improperJobs:
            gLogger.notice(f"List of {len(improperJobs)} jobs in improper status:")
            gLogger.notice(" ".join(str(j) for j in sorted(improperJobs)))
