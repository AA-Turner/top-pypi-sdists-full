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
"""Bookkeeping Reporting module (just prepare the files, do not send them
(which is done in the uploadOutput)"""

import os
import re
import shlex
import time

from DIRAC import gLogger, S_OK, S_ERROR, gConfig
from DIRAC.Core.Utilities.Subprocess import systemCall
from DIRAC.Resources.Catalog.PoolXMLFile import getGUID
from DIRAC.Workflow.Utilities.Utils import getStepCPUTimes

import LHCbDIRAC
from LHCbDIRAC.Resources.Catalog.PoolXMLFile import getOutputType
from LHCbDIRAC.Workflow.Modules.ModuleBase import ModuleBase
from LHCbDIRAC.Core.Utilities.ProductionData import constructProductionLFNs
from LHCbDIRAC.Core.Utilities.XMLSummaries import XMLSummary, XMLSummaryError
from LHCbDIRAC.Core.Utilities.BookkeepingJobInfo import BookkeepingJobInfo


class BookkeepingReport(ModuleBase):
    """BookkeepingReport class."""

    def __init__(self, bkClient=None, dm=None):
        """Usual c'tor."""

        self.log = gLogger.getSubLogger("BookkeepingReport")

        super().__init__(self.log, bkClientIn=bkClient, dm=dm)

        self.simDescription = "NoSimConditions"
        self.eventType = ""
        self.poolXMLCatName = ""
        self.stepInputData = []
        self.firstStepInput = ""
        self.jobType = ""
        self.stepOutputs = []
        self.histogram = False
        self.xf_o = None

        self.ldate = None
        self.ltime = None
        self.ldatestart = None
        self.ltimestart = None

    ################################################################################

    def execute(
        self,
        production_id=None,
        prod_job_id=None,
        wms_job_id=None,
        workflowStatus=None,
        stepStatus=None,
        wf_commons=None,
        step_commons=None,
        step_number=None,
        step_id=None,
        saveOnFile=True,
    ):
        """Usual executor."""
        try:
            super().execute(
                production_id,
                prod_job_id,
                wms_job_id,
                workflowStatus,
                stepStatus,
                wf_commons,
                step_commons,
                step_number,
                step_id,
            )

            if not self._checkWFAndStepStatus():
                return S_OK()

            bkLFNs, logFilePath = self._resolveInputVariables()

            doc = self.__makeBookkeepingXML(bkLFNs, logFilePath)

            if saveOnFile:
                bfilename = f"bookkeeping_{self.step_id}.xml"
                with open(bfilename, "wb") as bfile:
                    bfile.write(doc)
            else:
                print(doc)

            return S_OK()

        except Exception as e:  # pylint:disable=broad-except
            self.log.exception("Failure in BookkeepingReport execute module", lException=e)
            self.setApplicationStatus(repr(e))
            return S_ERROR(str(e))

        finally:
            super().finalize()

    ################################################################################
    # AUXILIAR FUNCTIONS
    ################################################################################

    def _resolveInputVariables(self):
        """By convention the module parameters are resolved here."""

        super()._resolveInputVariables()
        super()._resolveInputStep()

        self.stepOutputs, _sot, _hist = self._determineOutputs()

        # # VARS FROM WORKFLOW_COMMONS ##

        if "outputList" in self.workflow_commons:
            for outputItem in self.stepOutputs:
                if outputItem not in self.workflow_commons["outputList"]:
                    self.workflow_commons["outputList"].append(outputItem)
        else:
            self.workflow_commons["outputList"] = self.stepOutputs

        if (
            "BookkeepingLFNs" in self.workflow_commons
            and "LogFilePath" in self.workflow_commons
            and "ProductionOutputData" in self.workflow_commons
        ):
            logFilePath = self.workflow_commons["LogFilePath"]
            bkLFNs = self.workflow_commons["BookkeepingLFNs"]

            if not isinstance(bkLFNs, list):
                bkLFNs = [i.strip() for i in bkLFNs.split(";")]

        else:
            self.log.info("LogFilePath / BookkeepingLFNs parameters not found, creating on the fly")
            result = constructProductionLFNs(self.workflow_commons, self.bkClient)
            if not result["OK"]:
                self.log.error("Could not create production LFNs", result["Message"])
                raise ValueError("Could not create production LFNs")

            bkLFNs = result["Value"]["BookkeepingLFNs"]
            logFilePath = result["Value"]["LogFilePath"][0]

        self.ldate = time.strftime("%Y-%m-%d", time.gmtime(time.time()))
        self.ltime = time.strftime("%H:%M:%S", time.gmtime(time.time()))

        if "StartTime" in self.step_commons:
            startTime = self.step_commons["StartTime"]
            self.ldatestart = time.strftime("%Y-%m-%d", time.gmtime(startTime))
            self.ltimestart = time.strftime("%H:%M:%S", time.gmtime(startTime))

        try:
            self.xf_o = self.step_commons["XMLSummary_o"]
        except KeyError:
            self.log.warn("XML Summary object not found, will try to create it (again?)")
            try:
                xmlSummaryFile = self.step_commons["XMLSummary"]
            except KeyError:
                self.log.warn("XML Summary file name not found, will try to guess it")
                xmlSummaryFile = "summary{}_{}_{}_{}.xml".format(
                    self.cleanedApplicationName,
                    self.production_id,
                    self.prod_job_id,
                    self.step_number,
                )
                self.log.warn(f"Trying {xmlSummaryFile}")
                if xmlSummaryFile not in os.listdir("."):
                    self.log.warn(f"XML Summary file {xmlSummaryFile} not found, will try to guess a second time")
                    xmlSummaryFile = f"summary{self.cleanedApplicationName}_{self.step_id}.xml"
                    self.log.warn(f"Trying {xmlSummaryFile}")
                    if xmlSummaryFile not in os.listdir("."):
                        self.log.warn(
                            f"XML Summary file {xmlSummaryFile} not found, will try to guess a third and last time"
                        )
                        xmlSummaryFile = f"summary{self.cleanedApplicationName}_{self.step_number}.xml"
                        self.log.warn(f"Trying {xmlSummaryFile}")
            try:
                self.xf_o = XMLSummary(xmlSummaryFile)
            except XMLSummaryError as e:
                self.log.warn("No XML summary available", f"{repr(e)}")
                self.xf_o = None

        return bkLFNs, logFilePath

    ################################################################################
    ################################################################################

    def __makeBookkeepingXML(self, bkLFNs, logFilePath):
        """Bookkeeping xml looks like this::

        <Job ConfigName="" ConfigVersion="" Date="" Time="">
          <TypedParameter Name="" Type="" Value=""/>
          ...
          <InputFile Name=""/>
          ...
          <OutputFile Name="" TypeName="" TypeVersion="">
            <Parameter Name="" Value=""/>
            ...
            <Replica Location="" Name=""/>
            ....
          </OutputFile>
          ...
          <SimulationCondition>
            <Parameter Name="" Value=""/>
          </SimulationCondition>
        </Job>

        """
        job_info = BookkeepingJobInfo(
            ConfigName=self.workflow_commons.get("configName", self.applicationName),
            ConfigVersion=self.workflow_commons.get("configVersion", self.applicationVersion),
            Date=self.ldate,
            Time=self.ltime,
        )
        # Generate TypedParams
        self.__generateTypedParams(job_info)
        # Generate InputFiles
        self.__generateInputFiles(job_info, bkLFNs)
        # Generate OutputFiles
        self.__generateOutputFiles(job_info, bkLFNs, logFilePath)
        # Generate SimulationConditions
        if self.applicationName == "Gauss":
            job_info.simulation_condition = self.simDescription
        return job_info.to_xml()

    ################################################################################

    def __generateTypedParams(self, job_info):
        """Set fields in job_info.typed_parameters"""
        exectime, cputime = getStepCPUTimes(self.step_commons)
        job_info.typed_parameters.CPUTIME = str(cputime)
        job_info.typed_parameters.ExecTime = str(exectime)

        try:
            job_info.typed_parameters.WNMEMORY = str(self.xf_o.memory)
        except AttributeError:
            pass

        diracPower = gConfig.getValue("/LocalSite/CPUNormalizationFactor", "0")
        job_info.typed_parameters.WNCPUHS06 = diracPower
        mjfPower = gConfig.getValue("/LocalSite/CPUScalingFactor", "0")
        # Trick to know that the value is obtained from MJF: # from diracPower
        if mjfPower != diracPower:
            job_info.typed_parameters.WNMJFHS06 = str(mjfPower)
        job_info.typed_parameters.NumberOfProcessors = str(self.numberOfProcessors)
        job_info.typed_parameters.Production = str(self.production_id)
        job_info.typed_parameters.DiracJobId = str(self.jobID)
        job_info.typed_parameters.Name = str(self.step_id)
        job_info.typed_parameters.JobStart = f"{self.ldatestart} {self.ltimestart}"
        job_info.typed_parameters.JobEnd = f"{self.ldate} {self.ltime}"
        job_info.typed_parameters.Location = self.siteName
        job_info.typed_parameters.JobType = self.jobType

        job_info.typed_parameters.ProgramName = self.applicationName
        job_info.typed_parameters.ProgramVersion = self.applicationVersion

        job_info.typed_parameters.FirstEventNumber = str(1)

        job_info.typed_parameters.StatisticsRequested = str(self.numberOfEvents)

        job_info.typed_parameters.StepID = str(self.BKstepID)

        try:
            noOfEvents = self.xf_o.inputEventsTotal if self.xf_o.inputEventsTotal else self.xf_o.outputEventsTotal
        except AttributeError:
            # This happens iff the XML summary can't be created (e.g. for merging MDF files)
            res = self.bkClient.getFileMetadata(self.stepInputData)
            if not res["OK"]:
                raise AttributeError("Can't get the BKK file metadata")
            noOfEvents = sum(fileMeta["EventStat"] for fileMeta in res["Value"]["Successful"].values())
        job_info.typed_parameters.NumberOfEvents = str(noOfEvents)

    ################################################################################

    def __generateInputFiles(self, job_info, bkLFNs):
        self.log.debug("Adding InputData: bkLFNs", bkLFNs)
        self.log.debug("Adding InputData: self.stepInputData", self.stepInputData)
        for inputname in self.stepInputData or []:
            for bkLFN in bkLFNs:
                if os.path.basename(bkLFN).lower() == os.path.basename(inputname).lower():
                    # preserve the case
                    inputF = os.path.join(os.path.dirname(os.path.normpath(bkLFN)), os.path.basename(inputname))
                    job_info.input_files.append(inputF)
                    break
            else:
                # inputname is an LFN
                job_info.input_files.append(inputname)

    ################################################################################

    def __generateOutputFiles(self, job_info, bkLFNs, logFilePath):
        if self.eventType is not None:
            eventtype = self.eventType
        else:
            self.log.warn("BookkeepingReport: no eventType specified")
            eventtype = "Unknown"
        self.log.info("Event type =", eventtype)

        outputs = []
        bkTypeDict = {}
        for stepOutput in self.stepOutputs:
            if "outputDataName" in stepOutput:
                outputs.append(((stepOutput["outputDataName"]), (stepOutput["outputDataType"])))
            if "outputBKType" in stepOutput:
                bkTypeDict[stepOutput["outputDataName"]] = stepOutput["outputBKType"]
        outputs.append(((self.applicationLog), ("LOG")))
        self.log.info("Found outputs", outputs)

        if isinstance(logFilePath, list):
            logFilePath = logFilePath[0]

        for output, outputtype in outputs:
            self.log.info("Looking at output", f"{output} with type {outputtype}")
            typeName = outputtype.upper()
            typeVersion = "1"
            fileStats = "0"
            if output in bkTypeDict:
                typeVersion = getOutputType(output, self.stepInputData)[output]
                self.log.info("Setting POOL XML catalog type", f"for {output} to {typeVersion}")
                typeName = bkTypeDict[output].upper()
                self.log.info(
                    "Setting explicit BK type version",
                    f"for {output} to {typeVersion} and file type to {typeName}",
                )
                fileStats, output = self._getFileStatsFromXMLSummary(output, outputtype)

            if not os.path.exists(output):
                self.log.error("Output file does not exist", f"Output file name: {output}")
                continue
            # Output file size
            if "size" not in self.step_commons or output not in self.step_commons["size"]:
                try:
                    outputsize = str(os.path.getsize(output))
                except OSError:
                    outputsize = "0"
            else:
                outputsize = self.step_commons["size"][output]

            if "md5" not in self.step_commons or output not in self.step_commons["md5"]:
                comm = "md5sum " + str(output)
                resultTuple = systemCall(0, shlex.split(comm))
                status = resultTuple["Value"][0]
                out = resultTuple["Value"][1]
            else:
                status = 0
                out = self.step_commons["md5"][output]

            if status:
                self.log.info(f"Failed to get md5sum of {str(output)}")
                self.log.info(str(out))
                md5sum = "000000000000000000000000000000000000"
            else:
                md5sum = out.split()[0]

            if "guid" not in self.step_commons or output not in self.step_commons["guid"]:
                guidResult = getGUID(output)
                guid = ""
                if not guidResult["OK"]:
                    self.log.error("Could not find GUID", f"for {output} with message {guidResult['Message']}")
                elif guidResult["generated"]:
                    self.log.warn(
                        "PoolXMLFile generated GUID(s) for the following files ", ", ".join(guidResult["generated"])
                    )
                    guid = guidResult["Value"][output]
                else:
                    guid = guidResult["Value"][output]
                    self.log.info("Setting POOL XML catalog GUID", f"for {output} to {guid}")
            else:
                guid = self.step_commons["guid"][output]

            if not guid:
                self.log.error("No GUID found", f"for {output}")
                raise NameError("No GUID found")

            # find the constructed lfn
            if re.search(r"\.log$", output):
                lfn = os.path.join(logFilePath, self.applicationLog)
            else:
                for outputLFN in bkLFNs:
                    if os.path.basename(outputLFN) == output:
                        lfn = outputLFN
                        break
                else:
                    self.log.error("Could not find LFN", f"for {output}")
                    raise NameError("Could not find LFN of output file")

            oldTypeName = None
            if "HIST" in typeName.upper():
                typeVersion = "0"

            # PROTECTION for old production XMLs
            # TODO: think about removing this!
            if typeName.upper() == "HIST":
                typeName = f"{self.applicationName.upper()}HIST"

            # Add Output to the XML file
            outputFile = BookkeepingJobInfo.OutputFile(
                Name=lfn,
                TypeName=typeName,
                TypeVersion=typeVersion,
                FileSize=outputsize,
                CreationDate=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time())),
                MD5Sum=md5sum,
                Guid=guid,
            )

            # HIST is in the dataTypes e.g. we may have new names in the future ;)
            if oldTypeName:
                typeName = oldTypeName

            if outputtype != "LOG":
                outputFile.EventTypeId = eventtype
                if fileStats != "Unknown":
                    outputFile.EventStat = fileStats

            # Log file replica information
            if self.applicationLog:
                logfile = self.applicationLog
                if logfile == output:
                    outputFile.Replica = f"http://lhcb-logs.cern.ch/storage{logFilePath}/{self.applicationLog}"

            job_info.output_files.append(outputFile)

    ################################################################################

    def _getFileStatsFromXMLSummary(self, output, outputtype):
        """Gets stats per file from the XML summary, considering files registered
        with different cases.

        :params str output: file name looked out
        :params str outputType: file type looked out
        :returns: (str, str) with stats and actual file name
        """
        try:
            return str(self.xf_o.outputsEvents[output]), output
        except AttributeError as e:
            # This happens iff the XML summary can't be created (e.g. for merging MDF files)
            self.log.warn(
                "XML summary not created, unable to determine the output events and setting to 'Unknown'", repr(e)
            )
            return "Unknown", output
        except KeyError as e:
            self.log.warn("Could not find output LFN in XML summary object", repr(e))

            # here starting to look if by chance the file has been produced with a different case
            for outputFileInXML in self.xf_o.outputsEvents:
                if output.lower() == outputFileInXML.lower():
                    self.log.info(
                        "Found output LFN in XML summary object with different case",
                        f"{output} -> {outputFileInXML}",
                    )
                    return str(self.xf_o.outputsEvents[outputFileInXML]), outputFileInXML

            if ("hist" in outputtype.lower()) or (".root" in outputtype.lower()):
                self.log.warn(
                    "HIST file not found in XML summary, event stats set to 'Unknown'", f"HIST not found = {output}"
                )
                return "Unknown", output

            raise KeyError("Could not find output LFN in XML summary object")
