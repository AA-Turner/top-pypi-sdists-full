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
"""It interprets the XML reports and make a job, file, or replica object."""
from xml.parsers.expat import ExpatError
from xml.dom.minidom import parse, parseString
from DIRAC import gLogger, S_OK, S_ERROR
from DIRAC.Core.Utilities.ReturnValues import convertToReturnValue, returnValueOrRaise
from DIRAC.DataManagementSystem.Client.DataManager import DataManager
from LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB import OracleBookkeepingDB
from LHCbDIRAC.BookkeepingSystem.Service.XMLReader.Job.FileParam import FileParam
from LHCbDIRAC.BookkeepingSystem.Service.XMLReader.Job.JobParameters import JobParameters
from LHCbDIRAC.BookkeepingSystem.Service.XMLReader.JobReader import JobReader
from LHCbDIRAC.BookkeepingSystem.Service.XMLReader.ReplicaReader import ReplicaReader
from LHCbDIRAC.BookkeepingSystem.DB.DataTakingConditionInterpreter import generateConditionDescription


class XMLFilesReaderManager:
    """XMLFilesReaderManager class."""

    #############################################################################

    def __init__(self):
        """initialize the member of class."""
        self.db = OracleBookkeepingDB()
        self.log = gLogger.getSubLogger("XMLFilesReaderManager")

    #############################################################################
    @staticmethod
    def readFile(filename):
        """reads an file content which format is XML."""
        try:
            with open(filename) as stream:
                doc = parse(stream)

            docType = doc.doctype  # job or replica
            xmltype = docType.name
        except NameError as ex:
            gLogger.error("XML reading error", filename)
            return S_ERROR(ex)

        return xmltype, doc, filename

    #############################################################################
    @staticmethod
    def smogInjectionSMOG2Gas(smogValue):
        """converts RunDB/CondDB SMOG value format into BK format (currently SMOG2 only or NoGas)."""
        fields = smogValue.split("_")
        type = fields[0]
        gas = fields[1] if len(fields) > 1 else ""
        unstable = fields[2] if len(fields) > 2 else ""
        if type == "NONE" or gas == "NONE":  # we set NoGas even when it is speicified for SMOG(1)
            return "NoGas"
        if type != "SMOG2":
            return "Unknown"  # register the value, means "we know it is unknown"
        if unstable not in ["", "Unstable"] or not gas:
            gLogger.error(f"SMOG value '{smogValue}' has unexpected format")
            return ""
        return gas.capitalize() + unstable

    #############################################################################
    def readXMLfromString(self, xmlString):
        """read the xml string."""
        try:
            doc = parseString(xmlString)

            docType = doc.doctype  # job or replica
            xmltype = docType.name

            if xmltype == "Replicas":
                replica = ReplicaReader().readReplica(doc, "IN Memory")
                result = self.processReplicas(replica)
                del replica
                return result
            elif xmltype == "Job":
                job = JobReader().readJob(doc, "IN Memory")
                result = self.processJob(job)
                del job
                return result
            else:
                self.log.error("unknown XML file!!!")
        except ExpatError as ex:
            self.log.error("XML reading error", repr(ex))
            self.log.exception()
            return S_ERROR(ex)

    #############################################################################
    def processJob(self, job):
        """interprets the xml content."""
        self.log.debug("Start Job Processing")

        # prepare for the insert, check the existence of the input files and retreive the fileid
        inputFiles = [inputFile.name for inputFile in job.inputFiles]
        if inputFiles:
            result = self.db.bulkgetIDsFromFilesTable(inputFiles)
            if not result["OK"]:
                return result
            if result["Value"]["Failed"]:
                self.log.error("The following files are not in the bkk", f"{','.join(result['Value']['Failed'])}")
                return S_ERROR("Files not in bkk")

            for inputFile in job.inputFiles:
                inputFile.fileID = int(result["Value"]["Successful"][inputFile.name]["FileId"])

        fileTypeCache = {}
        for outputfile in job.outputFiles:
            typeName = outputfile.type
            typeVersion = outputfile.version
            cachedTypeNameVersion = typeName + "<<" + typeVersion
            if cachedTypeNameVersion in fileTypeCache:
                self.log.debug(cachedTypeNameVersion + " in the cache!")
                typeID = fileTypeCache[cachedTypeNameVersion]
                outputfile.typeID = typeID
            else:
                result = self.db.checkFileTypeAndVersion(typeName, typeVersion)
                if not result["OK"]:
                    self.log.error("The [type:version] is missing", f"[{typeName}: {typeVersion}]")
                    return S_ERROR("[type:version] missing")

                self.log.debug(cachedTypeNameVersion + " added to the cache!")
                typeID = int(result["Value"])
                outputfile.typeID = typeID
                fileTypeCache[cachedTypeNameVersion] = typeID

            if (
                job.getParam("JobType") and job.getParam("JobType").value == "DQHISTOMERGING"
            ):  # all the merged histogram files have to be visible
                newFileParams = FileParam()
                newFileParams.name = "VisibilityFlag"
                newFileParams.value = "Y"
                outputfile.addFileParam(newFileParams)
                self.log.debug("The Merged histograms visibility flag has to be Y!")

            evtExists = False

            for param in outputfile.params:
                self.log.debug("ParamName check of " + str(param.name))

                if param.name == "EventType" and param.value:
                    result = self.db.checkEventType(int(param.value))
                    if not result["OK"]:
                        return S_ERROR(f"The event type {str(param.value)} is missing!")

                if param.name == "EventTypeId" and param.value:
                    result = self.db.checkEventType(int(param.value))
                    if not result["OK"]:
                        return S_ERROR(f"The event type {str(param.value)} is missing!")
                    evtExists = True

            if not evtExists and outputfile.type != "LOG":
                inputFiles = job.inputFiles

                if inputFiles:
                    fileName = inputFiles[0].name
                    res = self.db.getFileMetadata([fileName])
                    if not res["OK"]:
                        return res
                    fileMetadata = res["Value"]["Successful"].get(fileName)
                    if fileMetadata:
                        if "EventTypeId" in fileMetadata:
                            if outputfile.exists("EventTypeId"):
                                param = outputfile.getParam("EventTypeId")
                                param.value = str(fileMetadata["EventTypeId"])
                            else:
                                newFileParams = FileParam()
                                newFileParams.name = "EventTypeId"
                                newFileParams.value = str(fileMetadata["EventTypeId"])
                                outputfile.addFileParam(newFileParams)
                    else:
                        errMsg = f"Can not get the metadata of {fileName} file"
                        self.log.error(errMsg)
                        return S_ERROR(errMsg)

                elif job.getOutputFileParam("EventTypeId") is not None:
                    param = job.getOutputFileParam("EventTypeId")
                    newFileParams = FileParam()
                    newFileParams.name = "EventTypeId"
                    newFileParams.value = param.value
                    outputfile.addFileParam(newFileParams)

                else:
                    return S_ERROR("It can not fill the EventTypeId because there is no input files!")

        dqvalue = None
        infiles = job.inputFiles
        if not job.exists("RunNumber") and infiles:  # case of, e.g., MCReconstruction
            # Discover the run(s) and TCK(s) of the input files
            # One goal is to discover which dataquality to use

            res = self._getRunNumbersAndTCKs([jif.name for jif in job.inputFiles])
            if not res["OK"]:  # pylint: disable=invalid-sequence-index
                return res
            runNumbers, tcks = res["Value"]  # pylint: disable=invalid-sequence-index

            if len(runNumbers) > 1:
                self.log.debug("More than 1 run", ",".join(str(r) for r in runNumbers))
            elif len(runNumbers) == 1:
                runNumber = runNumbers.pop()
                self.log.debug("The output files of the job might inherit run", runNumber)
                newJobParams = JobParameters()
                newJobParams.name = "RunNumber"
                newJobParams.value = str(runNumber)
                job.addJobParams(newJobParams)

                if job.getParam("JobType") and job.getParam("JobType").value == "DQHISTOMERGING":
                    self.log.debug("DQ merging!")
                    retVal = self.db.getJobInfo(job.inputFiles[0].name)
                    if not retVal["OK"]:
                        return retVal
                    prod = retVal["Value"][0][18]
                    newJobParams = JobParameters()
                    newJobParams.name = "Production"
                    newJobParams.value = str(prod)
                    job.addJobParams(newJobParams)
                    self.log.debug("Production inherited from input", prod)
                else:
                    prod = job.getParam("Production").value
                    self.log.debug("Production:", f"{prod}")

                retVal = self.db.getProductionProcessingPassID(prod)
                if not retVal["OK"]:
                    return retVal

                res = self._getDataQuality(prod, runNumber)
                if not res["OK"]:
                    return res
                dqvalue = res["Value"]
                if not dqvalue:  # dqvalue can be None, if run/procid is not in newrunquality table
                    self.log.warn(
                        "Could not find run quality",
                        "for %d production (run number: %d)" % (int(prod), int(runNumber)),
                    )

            if len(tcks) > 1:
                self.log.debug("More than 1 TCK", f"[{','.join(tcks)}]")
                tck = -2
            elif len(tcks) == 1:
                tck = tcks.pop()
                self.log.debug("The output files of the job inherits the following TCK:", tck)
                if not job.exists("Tck"):
                    newJobParams = JobParameters()
                    newJobParams.name = "Tck"
                    newJobParams.value = tck
                    job.addJobParams(newJobParams)

        sumEventInputStat = 0
        sumEvtStat = 0
        sumLuminosity = 0

        if job.exists("JobType"):
            job.removeParam("JobType")

        inputfiles = job.inputFiles

        # This must be replaced by a single call!!!!
        # ## It is not urgent as we do not have a huge load on the database
        for i in inputfiles:
            fname = i.name
            res = self.db.getJobInfo(fname)
            if not res["OK"]:
                return res

            value = res["Value"]
            if value and value[0][2] is not None:
                sumEventInputStat += value[0][2]

            res = self.db.getFileMetadata([fname])
            if not res["OK"]:
                return res

            fileMetadata = res["Value"]["Successful"].get(fname)
            if fileMetadata:
                if fileMetadata["EventStat"] is not None:
                    sumEvtStat += fileMetadata["EventStat"]
                if fileMetadata["Luminosity"] is not None:
                    sumLuminosity += fileMetadata["Luminosity"]
                if dqvalue is None:
                    dqvalue = fileMetadata.get("DataqualityFlag", fileMetadata.get("DQFlag"))
            else:
                errMsg = f"Can not get the metadata of {fname} file"
                self.log.error(errMsg)
                return S_ERROR(errMsg)

        evtinput = 0
        if int(sumEvtStat) > int(sumEventInputStat):
            evtinput = sumEvtStat
        else:
            evtinput = sumEventInputStat

        if inputfiles:
            if not job.exists("EventInputStat"):
                newJobParams = JobParameters()
                newJobParams.name = "EventInputStat"
                newJobParams.value = str(evtinput)
                job.addJobParams(newJobParams)
            else:
                currentEventInputStat = job.getParam("EventInputStat")
                currentEventInputStat.value = evtinput

        self.log.debug("Luminosity:", sumLuminosity)
        outputFiles = job.outputFiles
        for outputfile in outputFiles:
            if outputfile.type not in ["LOG"] and sumLuminosity > 0 and not outputfile.exists("Luminosity"):
                newFileParams = FileParam()
                newFileParams.name = "Luminosity"
                newFileParams.value = sumLuminosity
                outputfile.addFileParam(newFileParams)
                self.log.debug("Luminosity added to ", outputfile.name)
            ################

        for param in job.parameters:
            if param.name == "RunNumber":
                value = int(param.value)
                if value <= 0 and len(job.inputFiles) == 0:
                    # The files which inherits the runs can be entered to the database
                    return S_ERROR("The run number not greater 0!")

        result = self.__insertJob(job)
        if not result["OK"]:
            config = job.configuration
            errorMessage = "Unable to create Job: {} , {}, {} .\n Error: {}".format(
                str(config.configName),
                str(config.configVersion),
                str(config.date),
                str(result["Message"]),
            )
            return S_ERROR(errorMessage)

        job.jobID = int(result["Value"])

        if job.exists("RunNumber"):  # case of, e.g., real data processing
            try:
                runnumber = int(job.getParam("RunNumber").value)
            except ValueError:
                runnumber = -1
            if runnumber != -1:
                self.log.verbose("Registering the run status for ", f"Run number {runnumber},  JobId {job.jobID}")
                result = self.db.insertRunStatus(runnumber, job.jobID, "N")
                if not result["OK"]:
                    errorMessage = ("Unable to register run status", runnumber + result["Message"])
                    self.log.error(errorMessage[0], errorMessage[1])
                    res = self.db.deleteJob(job.jobID)
                    if not res["OK"]:
                        self.log.warn("Unable to delete job", str(job.jobID) + res["Message"])
                    return S_ERROR(errorMessage[0])

                # we may be using HLT2 output to flag the runs: as a consequence we may have already flagged the run
                retVal = self._getDataQuality(runNumber=runnumber)
                if not retVal["OK"]:
                    return retVal
                if retVal["Value"]:  # if not "None", override what is found in the ancestors
                    dqvalue = retVal["Value"]
                    self.log.verbose("The run data quality flag for", "run %d is %s" % (runnumber, dqvalue))

            else:
                # we ran on multiple runs
                self.log.warn("Run number can not determined for production:", job.getParam("Production").value)

        inputFiles = job.inputFiles
        for inputfile in inputFiles:
            result = self.db.insertInputFile(job.jobID, inputfile.fileID)
            if not result["OK"]:
                errorMessage = ("Unable to insert input file", (str(inputfile.name)) + result["Message"])
                self.log.error(errorMessage[0], errorMessage[1])
                res = self.db.deleteJob(job.jobID)
                if not res["OK"]:
                    self.log.warn("Unable to delete job", str(job.jobID) + res["Message"])
                return S_ERROR(errorMessage[0])

        outputFiles = job.outputFiles
        prod = job.getParam("Production").value
        stepid = job.getParam("StepID").value
        retVal = self.db.getProductionOutputFileTypes(prod, stepid)
        if not retVal["OK"]:
            return retVal
        outputFileTypes = retVal["Value"]
        for outputfile in outputFiles:
            if dqvalue is not None:
                newFileParams = FileParam()
                newFileParams.name = "QualityId"
                newFileParams.value = dqvalue
                outputfile.addFileParam(newFileParams)
            elif not job.exists("RunNumber"):  # if it is MC
                newFileParams = FileParam()
                newFileParams.name = "QualityId"
                newFileParams.value = "OK"
                outputfile.addFileParam(newFileParams)
            ftype = outputfile.type
            if ftype in outputFileTypes:
                vFileParams = FileParam()
                vFileParams.name = "VisibilityFlag"
                vFileParams.value = outputFileTypes[ftype]
                outputfile.addFileParam(vFileParams)
                self.log.debug("The visibility flag is", outputFileTypes[ftype])

            result = self.__insertOutputFiles(job, outputfile)
            if not result["OK"]:
                errorMessage = (
                    "Unable to insert output file",
                    f"{outputfile.name} ! ERROR: {result['Message']}",
                )
                self.log.error(errorMessage[0], errorMessage[1])
                res = self.db.deleteInputFiles(job.jobID)
                if not res["OK"]:
                    self.log.warn("Unable to delete inputfiles of", str(job.jobID) + res["Message"])
                res = self.db.deleteJob(job.jobID)
                if not res["OK"]:
                    self.log.warn("Unable to delete job", str(job.jobID) + res["Message"])
                return S_ERROR(errorMessage[0])
            else:
                fileid = int(result["Value"])
                outputfile.fileID = fileid

            replicas = outputfile.replicas
            for replica in replicas:
                params = replica.params
                for param in params:
                    # just one param exist in params list, because JobReader only one param add to Replica
                    name = param.name
                result = self.db.updateReplicaRow(outputfile.fileID, "No")
                if not result["OK"]:
                    return S_ERROR(f"Unable to create Replica {str(name)} !")

        self.log.debug("End Processing!")

        return S_OK()

    @convertToReturnValue
    def _getRunNumbersAndTCKs(self, fileList):
        """Utility to get run numbers and TCKs of a list of files"""
        runnumbers = set()
        tcks = set()
        for lfn in fileList:
            for runtck in returnValueOrRaise(self.db.getRunNbAndTck(lfn)):
                if runtck[0]:
                    runnumbers.add(runtck[0])
                if runtck[1] and runtck[1] != "None":
                    tcks.add(runtck[1])
        return (runnumbers, tcks)

    @convertToReturnValue
    def _getDataQuality(self, prod=None, runNumber=None):
        """Return the DQ for a given prod and run number.
        A failure in finding the processing pass ID is a genuine error,
        while not finding a DQ flag can be okay (case of real data taking, not yet flagged)
        """
        if not runNumber:
            return None
        procID = returnValueOrRaise(self.db.getProductionProcessingPassID(prod or runNumber * -1))
        return self.db.getRunAndProcessingPassDataQuality(runNumber, procID).get("Value")

    def __insertJob(self, job):
        """Inserts the job to the database."""
        config = job.configuration

        production = None

        condParams = job.dataTakingCondition  # real data
        if condParams:
            datataking = condParams.parameters
            config = job.configuration

            ver = config.configVersion  # online bug fix
            ver = ver.capitalize()
            config.configVersion = ver
            self.log.debug("Data taking:", f"{datataking}")
            dtDescription = generateConditionDescription(datataking, config.configName)
            self.log.debug(dtDescription)
            datataking["Description"] = dtDescription

            res = self.db._getDataTakingConditionId(dtDescription)
            if not res["OK"]:
                self.log.error(
                    "Error retrieving the DataTaking Condition ID",
                    f"Description: {dtDescription}. Error: {res['Message']}",
                )
                return res

            daqid = res["Value"]
            # If there is no condition matching the description, create one
            if daqid == -1:  # yes... -1 for non existing conditions
                res = self.db.insertDataTakingCondDesc(dtDescription)
                if not res["OK"]:
                    self.log.error("Cannot insert DataTaking Condition Description", res["Message"])
                    return res
                daqid = res["Value"]

            # insert processing pass
            programName = None
            programVersion = None
            conddb = None
            dddb = None
            found = False
            for param in job.parameters:
                if param.name == "ProgramName":
                    programName = param.value
                elif param.name == "ProgramVersion":
                    programVersion = param.value
                elif param.name == "CondDB":
                    conddb = param.value
                elif param.name == "DDDB":
                    dddb = param.value
                elif param.name == "RunNumber":
                    production = int(param.value) * -1
                    found = True

            if job.exists("CondDB"):
                job.removeParam("CondDB")
            if job.exists("DDDB"):
                job.removeParam("DDDB")

            if not found:
                self.log.error("Run number is missing!")
                return S_ERROR("Run number is missing!")

            if "SmogInjection" in datataking:
                # "RunNumber" is checked several lines above (for production)
                gas = self.smogInjectionSMOG2Gas(datataking["SmogInjection"])
                if gas:
                    retVal = self.db.setSMOG2State(gas, False, [production * -1])
                    if not retVal["OK"]:
                        self.log.error(f"Can't set SMOG2 state {gas} for run {production * -1}, will ignore...")
                        # return S_ERROR("Can't set SMOG2 state for run") # TOCHANGE: Ignore till SMOG2 is checked

            retVal = self.db.getStepIdandNameForRUN(programName, programVersion, conddb, dddb)

            if not retVal["OK"]:
                return retVal

            stepid = retVal["Value"][0]

            # now we have to get the list of eventtypes
            eventtypes = []
            for outputFiles in job.outputFiles:
                for outPutfileParam in outputFiles.params:
                    outputFileParamName = outPutfileParam.name
                    if outputFileParamName == "EventTypeId":
                        eventtypes.append(int(outPutfileParam.value))

            steps = {
                "Steps": [
                    {
                        "StepId": stepid,
                        "StepName": retVal["Value"][1],
                        "ProcessingPass": retVal["Value"][1],
                        "Visible": "Y",
                        "OutputFileTypes": [{"FileType": "RAW"}],
                    }
                ]
            }

            self.log.debug("Pass_indexid", f"{steps}")
            self.log.debug("Data taking", f"{dtDescription}")
            self.log.debug("production", production)

            newJobParams = JobParameters()
            newJobParams.name = "StepID"
            newJobParams.value = str(stepid)
            job.addJobParams(newJobParams)

            message = f"StepID for run: {str(production)}"
            self.log.info(message, stepid)

            res = self.db.addProduction(
                production,
                simcond=None,
                daq=dtDescription,
                steps=steps["Steps"],
                inputproc="",
                configName=config.configName,
                configVersion=config.configVersion,
                eventType=eventtypes,
            )
            if res["OK"]:
                self.log.verbose("New processing pass has been created!")
                self.log.verbose("New production is:", production)
            elif job.exists("RunNumber"):
                self.log.warn("The run already registered!")
            else:
                self.log.error("Failing adding production", production + res["Message"])
                retVal = self.db.deleteStepContainer(production)
                if not retVal["OK"]:
                    return retVal
                return S_ERROR("Failing adding production")

        attrList = {"ConfigName": config.configName, "ConfigVersion": config.configVersion, "JobStart": None}

        for param in job.parameters:
            attrList[str(param.name)] = param.value

        res = self.db.checkProcessingPassAndSimCond(attrList["Production"])
        if not res["OK"]:
            self.log.error("check processing pass and simulation condition error", res["Message"])
        else:
            value = res["Value"]
            if value[0][0] == 0:
                errorMessage = "Missing processing pass and simulation conditions: "
                errorMessage += f"please fill it. Production = {str(attrList['Production'])}"
                self.log.warn(errorMessage)

        if attrList["JobStart"] is None:
            # date = config.date.split('-')
            # time = config.time.split(':')
            # dateAndTime = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), 0, 0)
            attrList["JobStart"] = config.date + " " + config.time

        if production is not None:  # for the online registration
            attrList["Production"] = production

        res = self.db.insertJob(attrList)

        if not res["OK"] and production is not None and production < 0:
            self.log.error("Failed inserting job", res["Message"])
            retVal = self.db.deleteProductionsContainer(production)
            if not retVal["OK"]:
                self.log.error(retVal["Message"])
        return res

    #############################################################################
    def __insertOutputFiles(self, job, outputfile):
        """insert the files produced by a job."""
        attrList = {"FileName": outputfile.name, "FileTypeId": outputfile.typeID, "JobId": job.jobID}

        for param in outputfile.params:
            attrList[str(param.name)] = param.value
        return self.db.insertOutputFile(attrList)

    #############################################################################
    def processReplicas(self, replica):
        """process the replica registration request."""
        outputfile = replica.name
        self.log.debug("Processing replicas:", f"{outputfile}")
        fileID = -1

        delete = True

        replicaFileName = ""
        for param in replica.params:
            replicaFileName = param.file
            location = param.location
            delete = param.action == "Delete"

            result = self.db.checkfile(replicaFileName)
            if not result["OK"]:
                message = "No replica can be "
                if delete:
                    message += "removed"
                else:
                    message += "added"
                message += " to file " + str(replicaFileName) + " for " + str(location) + ".\n"
                return S_ERROR(message)
            else:
                fileID = int(result["Value"][0][0])
                self.log.debug("FileId:", fileID)

            if delete:
                result = DataManager().getReplicas(replicaFileName)
                replicaList = result["Value"]["Successful"]
                if len(replicaList) == 0:
                    result = self.db.updateReplicaRow(fileID, "No")
                    if not result["OK"]:
                        self.log.warn("Unable to set the Got_Replica flag for ", f"{replicaFileName}")
                        return S_ERROR("Unable to set the Got_Replica flag for ", f"{replicaFileName}")
            else:
                result = self.db.updateReplicaRow(fileID, "Yes")
                if not result["OK"]:
                    return S_ERROR("Unable to set the Got_Replica flag for " + str(replicaFileName))

        self.log.debug("End Processing replicas!")

        return S_OK()
