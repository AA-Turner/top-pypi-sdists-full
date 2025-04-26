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
"""Reads .log-files and outputs summary of counters as a .json-file
"""
import os
import json

from DIRAC import gLogger, S_OK, S_ERROR
from DIRAC.Core.Utilities import TimeUtilities
from DIRAC.Core.Utilities.ReturnValues import DReturnType


def readLogFile(
    logFile: str,
    jobID: str,
    prodID: str,
    wmsID: str,
    application: str,
    applicationVersion: str,
    name: str = "errors.json",
) -> DReturnType:
    """The script that runs everything.

    :param logFile: the name of the logfile
    :param jobID: the JobID
    :param prodID: the production ID
    :param wmsID: the wmsID
    :param name: the name of the output json file, standardised to 'errors.json'
    """
    logString = ""
    dictG4Errors = {
        "G4Exception": "",
        "G4 Exception": "",
        "ERROR ": "",
        "FATAL ": "",
        "PYTHIA WARNING ": "",
    }
    errorG4Dict = dict()
    errorDict = dict()
    if logFile.endswith(".log"):
        res = __getLogString(logFile, logString)
        if not res["OK"]:
            return res
        logString = res["Value"]
    else:
        gLogger.debug("The log is already in a readable string")
        logString = logFile

    reversedKeys = sorted(dictG4Errors, reverse=True)
    for errorString in reversedKeys:
        ctest = logString.count(errorString)
        test = logString.find(errorString)
        for i in range(ctest):
            start = test
            test = logString.find(errorString, start)
            alreadyFound = False
            for error in reversedKeys:
                if error == errorString:
                    break
                checke = logString[test : test + 100].find(error)
                if checke != -1:
                    alreadyFound = True
                    test += len(error)
                    break
            if alreadyFound:
                continue

            if test != -1:
                if errorString.find("G4") != -1:
                    check = logString[test : test + 250].find("***")
                    if check != -1:
                        errorBase = logString[test : test + 250].split("***")[0]
                        strippedErrString = errorBase.rstrip().replace("\n", "")
                        if not strippedErrString.startswith("G4Exception-END") and not strippedErrString.startswith(
                            "G4Exception-START"
                        ):
                            if strippedErrString in errorG4Dict:
                                errorG4Dict[strippedErrString] = errorG4Dict[strippedErrString] + 1
                            else:
                                errorG4Dict[strippedErrString] = 1
                        test += len(errorBase)
                else:
                    errorBase = logString[test : test + 250].split("\n")[0].rstrip()
                    if errorBase in errorDict:
                        errorDict[errorBase] = errorDict[errorBase] + 1
                    else:
                        errorDict[errorBase] = 1
                    test += len(errorBase)

    dictBase = {
        "JobID": jobID,
        "ProductionID": prodID,
        "wmsID": wmsID,
        "Application": application,
        "ApplicationVersion": applicationVersion,
        "timestamp": int(TimeUtilities.toEpochMilliSeconds()),
    }
    with open(name, "w") as output:
        output.write(json.dumps(dictBase | errorDict | errorG4Dict, indent=2))
    gLogger.notice("Finished creating the JSON file with Gauss Errors")
    return S_OK()


def __getLogString(logFile: str, logString: str) -> DReturnType:
    """Checks if the log file can be opened, and saves the text in logFile into logString.

    :param logFile: the name of the logFile
    :param logStr: the name of the variable that will save the contents of logFile
    """

    gLogger.notice("Attempting to open", logFile)
    if not os.path.exists(logFile):
        gLogger.error("File could not be found", f"({logFile})")
        return S_ERROR()
    if os.stat(logFile)[6] == 0:
        gLogger.error("File is empty", f"({logFile})")
        return S_ERROR()
    with open(logFile) as f:
        logString = f.read()
    gLogger.notice("Successfully read", logFile)
    return S_OK(logString)
