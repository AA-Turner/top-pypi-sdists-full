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
"""File utilities module (e.g. make GUIDs)"""
import uproot

from DIRAC import gLogger, S_OK, S_ERROR
from DIRAC.Core.Utilities.File import makeGuid as DIRACMakeGUID


def getRootFileGUIDs(fileList):
    """Retrieve a list of GUIDs for a list of files."""
    guids = {"Successful": {}, "Failed": {}}
    for fileName in fileList:
        res = getRootFileGUID(fileName)
        if res["OK"]:
            gLogger.verbose("GUID from ROOT", f"{res['Value']}")
            guids["Successful"][fileName] = res["Value"]
        else:
            guids["Failed"][fileName] = res["Message"]
    return S_OK(guids)


def getRootFileGUID(fileName):
    """Function to retrieve a file GUID using uproot."""
    try:
        with uproot.open(fileName) as f:
            branch = f["Refs"]["Params"]
            for item in branch.array():
                if item.startswith("FID="):
                    return S_OK(item.split("=")[1])
        return S_ERROR("GUID not found")
    except Exception as e:
        errorMsg = f"Error extracting GUID: {e}"
        return S_ERROR(errorMsg)


def makeGuid(fileNames):
    """Function to retrieve a file GUID using uproot."""
    if isinstance(fileNames, str):
        fileNames = [fileNames]

    fileGUIDs = {}
    for fileName in fileNames:
        res = getRootFileGUID(fileName)
        if res["OK"]:
            gLogger.verbose("GUID from ROOT", f"{res['Value']}")
            fileGUIDs[fileName] = res["Value"]
        else:
            gLogger.info("Could not obtain GUID from file through Gaudi, using standard DIRAC method")
            fileGUIDs[fileName] = DIRACMakeGUID(fileName)

    return fileGUIDs
