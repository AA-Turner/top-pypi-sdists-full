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
"""Extension of DIRAC Task Manager."""
from DIRAC.TransformationSystem.Client.WorkflowTasks import WorkflowTasks

COMPONENT_NAME = "LHCbTaskManager"


class LHCbWorkflowTasks(WorkflowTasks):
    """A simple LHCb extension to the task manager, for now only used to set the
    runNumber and runMetadata."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parametricSequencedKeys = ["JOB_ID", "PRODUCTION_ID", "InputData", "runNumber"]

    def _handleInputs(self, oJob, paramsDict):
        """set job inputs (+ metadata)"""
        try:
            if paramsDict["InputData"]:
                self.log.verbose(f"Setting input data to {paramsDict['InputData']}")
                self.log.verbose(f"Setting run number to {str(paramsDict.get('RunNumber'))}")
                oJob.setInputData(paramsDict["InputData"], runNumber=paramsDict.get("RunNumber"))

                try:
                    runMetadata = paramsDict["RunMetadata"]
                    self.log.verbose(f"Setting run metadata information to {str(runMetadata)}")
                    oJob.setRunMetadata(runMetadata)
                except KeyError:
                    pass

        except KeyError:
            self.log.exception("Could not find input data or a run number")
            raise KeyError("Could not found an input data or a run number")

    def _handleInputsBulk(self, seqDict, paramsDict, transID):
        """set job inputs (+ metadata)"""
        method = "_handleInputsBulk"
        if seqDict:
            self._logVerbose(f"Setting job input data to {seqDict}", transID=transID, method=method)

        # Handle Input Data
        inputData = paramsDict.get("InputData")
        if inputData:
            if isinstance(inputData, str):
                inputData = inputData.replace(" ", "").split(";")
            self._logVerbose(f"Setting input data {inputData} to {seqDict}", transID=transID, method=method)
            seqDict["InputData"] = inputData
            seqDict["runNumber"] = paramsDict.get("RunNumber")

        for paramName, paramValue in paramsDict.items():
            if paramName not in ("InputData", "Site", "TargetSE", "runNumber"):
                if paramValue:
                    self._logVerbose(f"Setting {paramName} to {paramValue}", transID=transID, method=method)
                    seqDict[paramName] = paramValue

        return inputData

    def _handleRest(self, oJob, paramsDict):
        """add as JDL parameters all the other parameters that are not for inputs
        or destination."""

        for paramName, paramValue in paramsDict.items():
            if paramName not in ("InputData", "RunNumber", "RunMetadata", "Site", "TargetSE"):
                if paramValue:
                    self.log.verbose(f"Setting {paramName} to {paramValue}")
                    oJob._addJDLParameter(paramName, paramValue)

    #############################################################################
