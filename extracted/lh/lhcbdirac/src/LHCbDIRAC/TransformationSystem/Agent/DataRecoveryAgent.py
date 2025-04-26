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
"""In general for data processing productions we need to completely abandon the
'by hand' reschedule operation such that accidental reschedulings don't result
in data being processed twice.

For all above cases the following procedure should be used to achieve 100%:

- Starting from the data in the Production DB for each transformation
  look for files in the following status:

    - Assigned
    - MaxReset

  some of these will correspond to the final WMS status 'Failed'.

For files in MaxReset and Assigned:

- Discover corresponding job WMS ID
- Check that there are no outstanding requests for the job
  o wait until all are treated before proceeding
- Check that none of the job input data has BK descendants for the current production
  o if the data has a replica flag it means all was uploaded successfully - should be investigated by hand
  o if there is no replica flag can proceed with file removal from FC / storage (can be disabled by flag)
- Mark the recovered input file status as 'Unused' in the ProductionDB if they were not in MaxReset
"""
import datetime

from DIRAC import S_OK
from DIRAC.Core.Base.AgentModule import AgentModule
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations
from DIRAC.RequestManagementSystem.Client.ReqClient import ReqClient

from LHCbDIRAC.DataManagementSystem.Client.ConsistencyChecks import ConsistencyChecks
from LHCbDIRAC.TransformationSystem.Client.TransformationClient import TransformationClient

AGENT_NAME = "Transformation/DataRecoveryAgent"


class DataRecoveryAgent(AgentModule):
    """Standard DIRAC agent class."""

    def __init__(self, *args, **kwargs):
        """c'tor."""
        AgentModule.__init__(self, *args, **kwargs)

        self.transClient = None
        self.reqClient = None
        self.consChecks = None

        self.enableFlag = True
        self.transformationTypes = []
        self.transLogger = self.log

    #############################################################################

    def initialize(self):
        """Sets defaults."""
        self.am_setOption("shifterProxy", "ProductionManager")

        self.transClient = TransformationClient()
        self.reqClient = ReqClient()
        self.consChecks = ConsistencyChecks(interactive=False, transClient=self.transClient)

        transformationTypes = Operations().getValue("Transformations/DataProcessing", [])
        extendableTTypes = Operations().getValue("Transformations/ExtendableTransfTypes", ["MCSimulation"])
        self.transformationTypes = list(set(transformationTypes) - set(extendableTTypes))

        return S_OK()

    #############################################################################
    def execute(self):
        """The main execution method."""
        # Configuration settings
        self.enableFlag = self.am_getOption("EnableFlag", True)
        self.log.verbose(f"Enable flag is {self.enableFlag}")
        if not self.transformationTypes:
            self.log.warn("No transformation types to look for... aborting")
            return S_OK()

        transformationStatus = self.am_getOption("TransformationStatus", ["Active", "Completing"])
        fileSelectionStatus = self.am_getOption("FileSelectionStatus", ["Assigned", "MaxReset"])
        unrecoverableStatus = self.am_getOption("UnrecoverableStatus", ["MaxReset"])
        updateStatus = self.am_getOption("FileUpdateStatus", "Unused")
        wmsStatusList = self.am_getOption("WMSStatus", ["Failed"])

        # only worry about files > 12hrs since last update
        selectDelay = self.am_getOption("SelectionDelay", 1)  # hours

        transformationDict = {}
        for transStatus in transformationStatus:
            result = self.__getEligibleTransformations(transStatus, self.transformationTypes)
            if not result["OK"]:
                self.log.error(
                    "Could not obtain eligible transformations",
                    f"Status '{transStatus}': {result['Message']}",
                )
                return result

            if not result["Value"]:
                self.log.info(
                    'No "%s" transformations of types %s to process.'
                    % (transStatus, ", ".join(self.transformationTypes))
                )
                continue

            transformationDict.update(result["Value"])

        self.log.info(
            f"Selected {len(transformationDict)} transformations of types {', '.join(self.transformationTypes)}"
        )
        self.log.verbose(f"Transformations selected:\n{', '.join(transformationDict)}")

        for transformation, typeName in transformationDict.items():
            self.transLogger = self.log.getSubLogger(f"Trans-{transformation}")
            result = self.__selectTransformationFiles(transformation, fileSelectionStatus)
            if not result["OK"]:
                self.transLogger.error(
                    "Could not select files for transformation", f"{transformation}: {result['Message']}"
                )
                continue
            fileDict = result["Value"]
            if not fileDict:
                self.transLogger.verbose(
                    "No files in status %s selected for transformation %s"
                    % (", ".join(fileSelectionStatus), transformation)
                )
                continue

            title = f"Looking at transformation {transformation}, type {typeName} "
            self.transLogger.info("=" * len(title))
            self.transLogger.info(title)

            self.transLogger.info(f"Selected {len(fileDict)} files with status {','.join(fileSelectionStatus)}")
            result = self.__obtainWMSJobIDs(transformation, fileDict, selectDelay, wmsStatusList)
            if not result["OK"]:
                self.transLogger.error("Could not obtain jobs for files of transformation", result["Message"])
                continue
            jobFileDict = result["Value"]
            if not jobFileDict:
                self.transLogger.info(f"No {' or '.join(wmsStatusList)} jobs found for selected files")
                continue

            self.transLogger.verbose(f"Looking at WMS jobs {','.join(str(jobID) for jobID in jobFileDict)}")

            fileCount = sum(len(lfnList) for lfnList in jobFileDict.values())
            self.transLogger.verbose(
                f"{str(fileCount) if fileCount else 'No'} files are selected after examining WMS jobs"
            )
            if not fileCount:
                continue

            result = self.__removePendingRequestsJobs(jobFileDict)
            if not result["OK"]:
                self.transLogger.error("Error while removing jobs with pending requests", result["Message"])
                continue
            # This method modifies the input dictionary
            if not jobFileDict:
                self.transLogger.info("No WMS jobs without pending requests to process.")
                continue

            fileCount = sum(len(lfnList) for lfnList in jobFileDict.values())
            self.transLogger.info(
                "%s files are selected in %d jobs after removing any job with pending requests"
                % (str(fileCount) if fileCount else "No", len(jobFileDict))
            )
            if not fileCount:
                continue

            jobsThatDidntProduceOutputs, jobsThatProducedOutputs = self.__checkdescendants(transformation, jobFileDict)
            title = f"======== Transformation {transformation}: results ========"
            self.transLogger.info(title)
            self.transLogger.info(f"\tTotal jobs that can be updated now: {len(jobsThatDidntProduceOutputs)}")
            if jobsThatProducedOutputs:
                self.transLogger.info(f"\t{len(jobsThatProducedOutputs)} jobs have descendants")
            else:
                self.transLogger.info("\tNo jobs have descendants")

            filesToUpdate = []
            filesMaxReset = []
            filesWithDescendants = []
            for job, fileList in jobFileDict.items():
                if job in jobsThatDidntProduceOutputs:
                    recoverableFiles = {lfn for lfn in fileList if fileDict[lfn][1] not in unrecoverableStatus}
                    filesToUpdate += list(recoverableFiles)
                    filesMaxReset += list(set(fileList) - recoverableFiles)
                elif job in jobsThatProducedOutputs:
                    filesWithDescendants += fileList

            if filesToUpdate:
                self.transLogger.info(f"\tUpdating {len(filesToUpdate)} files to '{updateStatus}'")
                result = self.__updateFileStatus(transformation, filesToUpdate, updateStatus)
                if not result["OK"]:
                    self.transLogger.error("\tRecoverable files were not updated", result["Message"])

            if filesMaxReset:
                self.transLogger.info(
                    "\t%d files are in %s status and have no descendants"
                    % (len(filesMaxReset), ",".join(unrecoverableStatus))
                )

            if filesWithDescendants:
                self.transLogger.warn(
                    "\t!!!!!!!! Transformation has descendants for files that are not marked as processed !!!!!!!!"
                )
                self.transLogger.warn("\tFiles with descendants:", ",".join(filesWithDescendants))
                self.transLogger.info(f"\tUpdating {len(filesWithDescendants)} files to '{'Processed'}'")
                result = self.__updateFileStatus(transformation, filesWithDescendants, "Processed")
                if not result["OK"]:
                    self.transLogger.error("\tRecovered files were not updated", result["Message"])

        return S_OK()

    #############################################################################
    def __getEligibleTransformations(self, status, typeList):
        """Select transformations of given status and type."""
        res = self.transClient.getTransformations(condDict={"Status": status, "Type": typeList})
        if not res["OK"]:
            return res
        transformations = {str(prod["TransformationID"]): prod["Type"] for prod in res["Value"]}
        return S_OK(transformations)

    #############################################################################
    def __selectTransformationFiles(self, transformation, statusList):
        """Select files, production jobIDs in specified file status for a given
        transformation."""
        # Until a query for files with timestamp can be obtained must rely on the
        # WMS job last update
        res = self.transClient.getTransformationFiles(
            condDict={"TransformationID": transformation, "Status": statusList}
        )
        if not res["OK"]:
            return res
        resDict = {}
        mandatoryKeys = {"LFN", "TaskID", "LastUpdate"}
        for fileDict in res["Value"]:
            missingKeys = mandatoryKeys - set(fileDict)
            if missingKeys:
                for key in missingKeys:
                    self.transLogger.warn(f"{key} is mandatory, but missing for:\n\t{str(fileDict)}")
            else:
                resDict[fileDict["LFN"]] = (fileDict["TaskID"], fileDict["Status"])
        return S_OK(resDict)

    #############################################################################
    def __obtainWMSJobIDs(self, transformation, fileDict, selectDelay, wmsStatusList):
        """Group files by the corresponding WMS jobIDs, check the corresponding
        jobs have not been updated for the delay time.

        Can't get into any mess because we start from files only in MaxReset
        / Assigned and check corresponding jobs.  Mixtures of files for jobs
        in MaxReset and Assigned statuses only possibly include some files
        in Unused status (not Processed for example) that will not be
        touched.
        """
        taskIDList = sorted({taskID for taskID, _status in fileDict.values()})
        self.transLogger.verbose(
            "The following %d task IDs correspond to the selected files:\n%s"
            % (len(taskIDList), ", ".join(str(taskID) for taskID in taskIDList))
        )

        jobFileDict = {}
        olderThan = datetime.datetime.utcnow() - datetime.timedelta(hours=selectDelay)

        res = self.transClient.getTransformationTasks(
            condDict={"TransformationID": transformation, "TaskID": taskIDList},
            older=olderThan,
            timeStamp="LastUpdateTime",
        )
        if not res["OK"]:
            self.transLogger.error("getTransformationTasks returned an error", f"{res['Message']}")
            return res

        mandatoryKeys = {"TaskID", "ExternalID", "LastUpdateTime", "ExternalStatus"}
        for taskDict in res["Value"]:
            missingKey = mandatoryKeys - set(taskDict)
            if missingKey:
                for key in missingKey:
                    self.transLogger.warn(f"Missing key {key} for job dictionary:\n\t{str(taskDict)}")
                continue

            taskID = taskDict["TaskID"]
            wmsID = taskDict["ExternalID"]
            wmsStatus = taskDict["ExternalStatus"]

            if not int(wmsID):
                self.transLogger.verbose(
                    f"TaskID {taskID}: status is {wmsStatus} (jobID = {wmsID}) so will not recheck with WMS"
                )
                continue

            # Exclude jobs not having appropriate WMS status - have to trust that production management status is correct
            if wmsStatus not in wmsStatusList:
                self.transLogger.verbose(
                    "Job %s is in status %s, not in %s so will be ignored"
                    % (wmsID, wmsStatus, ", ".join(wmsStatusList))
                )
                continue

            # Must map unique files -> jobs in expected state
            jobFileDict[wmsID] = [lfn for lfn, (tID, _st) in fileDict.items() if int(tID) == int(taskID)]

            self.transLogger.info(
                "Found %d files for taskID %s, jobID %s (%s), last update %s"
                % (len(jobFileDict[wmsID]), taskID, wmsID, wmsStatus, taskDict["LastUpdateTime"])
            )

        return S_OK(jobFileDict)

    #############################################################################

    def __removePendingRequestsJobs(self, jobFileDict):
        """Before doing anything check that no outstanding requests are pending for
        the set of WMS jobIDs."""
        jobs = list(jobFileDict)

        level = self.reqClient.log.getLevel()
        self.reqClient.log.setLevel("ERROR")
        result = self.reqClient.getRequestIDsForJobs(jobs)
        self.reqClient.log.setLevel(level)
        if not result["OK"]:
            return result

        if not result["Value"]["Successful"]:
            self.transLogger.verbose("None of the jobs have pending requests")
            return S_OK()

        for jobID, requestID in result["Value"]["Successful"].items():
            res = self.reqClient.getRequestStatus(requestID)
            if not res["OK"]:
                self.transLogger.error("Failed to get Status for Request", f"{requestID}:{res['Message']}")
            elif res["Value"] != "Done":
                # If we fail to get the Status or it is not Done, we must wait, so remove the job from the list.
                del jobFileDict[str(jobID)]
                self.transLogger.verbose(f"Removing jobID {jobID} from consideration until requests are completed")

        return S_OK()

    #############################################################################
    def __checkdescendants(self, transformation, jobFileDict):
        """Check BK descendants for input files, prepare list of actions to be
        taken for recovery."""

        jobsThatDidntProduceOutputs = []
        jobsThatProducedOutputs = []

        self.consChecks.prod = transformation
        for job, fileList in jobFileDict.items():
            result = self.consChecks.getDescendants(fileList)
            filesWithDesc = result[0]
            filesWithMultipleDesc = result[2]
            if filesWithDesc or filesWithMultipleDesc:
                jobsThatProducedOutputs.append(job)
            else:
                jobsThatDidntProduceOutputs.append(job)

        return jobsThatDidntProduceOutputs, jobsThatProducedOutputs

    ############################################################################
    def __updateFileStatus(self, transformation, fileList, fileStatus):
        """Update file list to specified status."""
        if not self.enableFlag:
            self.transLogger.info(
                "\tEnable flag is False, would have updated %d files to '%s' status for %s"
                % (len(fileList), fileStatus, transformation)
            )
            return S_OK()

        return self.transClient.setFileStatusForTransformation(int(transformation), fileStatus, fileList, force=False)
