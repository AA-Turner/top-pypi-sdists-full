#!/usr/bin/env python
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
"""Fix incorrect file GUIDs."""
import os

import DIRAC
from DIRAC.Core.Base.Script import Script

keep = None
localFile = None


def leave(msg, error=None, exitCode=0):
    from DIRAC import gLogger

    if error is None:
        error = {}

    if not keep and os.path.exists(localFile):
        os.remove(localFile)
        gLogger.info(f"Local file {localFile} removed")

    if error:
        errMsg = error.get(
            "Message",
            list(error.get("Value", {}).get("Failed", {"": "Unknown reason"}).values())[0],
        )
        gLogger.error(msg, f": {errMsg}")
    else:
        gLogger.always(msg)
    DIRAC.exit(exitCode)


@Script()
def main():
    global keep
    global localFile

    Script.registerSwitch("f:", "OldLFN=", "LFN of existing file to be fixed.")
    Script.registerSwitch(
        "n:", "NewLFN=", "Optional: specify a new LFN for the file (retaining the existing file with incorrect GUID)."
    )
    Script.registerSwitch("D:", "Directory=", "Optional: directory to download file (defaults to TMPDIR then PWD).")
    Script.registerSwitch("k", "Keep", "Optional: specify this switch to retain the local copy of the downloaded file")
    Script.registerSwitch(
        "m", "SafeMode", "Optional: specify this switch to run the script in safe mode (will check the GUIDs only)"
    )
    Script.setUsageMessage("\n".join([__doc__, "Usage:", f"  {Script.scriptName} [option|cfgfile] [OldLFN]"]))
    Script.parseCommandLine(ignoreErrors=True)

    args = Script.getPositionalArgs()

    from DIRAC.Interfaces.API.Dirac import Dirac
    from LHCbDIRAC.Core.Utilities.File import makeGuid

    from DIRAC import gLogger

    oldLFN = ""
    newLFN = ""
    localFile = ""
    keep = False
    safe = False
    directory = os.getcwd()
    if "TMPDIR" in os.environ:
        directory = os.environ["TMPDIR"]

    dirac = Dirac()

    if args:
        oldLFN = args.pop(0)

    for switch in Script.getUnprocessedSwitches():
        if switch[0].lower() in ("f", "oldlfn"):
            oldLFN = switch[1]
        elif switch[0].lower() in ("n", "newlfn"):
            newLFN = switch[1]
        elif switch[0].lower() in ("d", "directory"):
            directory = switch[1]
        elif switch[0].lower() in ("k", "keep"):
            keep = True
        elif switch[0].lower() in ("m", "safemode"):
            safe = True

    oldLFN = oldLFN.replace("LFN:", "")
    newLFN = newLFN.replace("LFN:", "")

    if not oldLFN:
        leave("The original LFN of the file to be fixed must be specified", exitCode=2)

    if not os.path.exists(directory):
        leave(f"Optional directory {directory} doesn't exist", exitCode=2)

    if not newLFN:
        gLogger.verbose(f"No new LFN specified, will replace the existing LFN {oldLFN}")
        newLFN = oldLFN

    gLogger.verbose(f"Directory for downloading file is set to {directory}")

    replicaInfo = dirac.getReplicas(oldLFN)
    if not replicaInfo["OK"] or replicaInfo["Value"]["Failed"]:
        leave(f"Could not get replica information for {oldLFN}", replicaInfo, exitCode=2)

    replicas = replicaInfo["Value"]["Successful"][oldLFN]
    storageElements = list(replicas)
    if not storageElements:
        leave(f"Could not determine SEs for replicas of {oldLFN}", exitCode=2)

    gLogger.info(f"Existing LFN has replicas at: {', '.join(storageElements)}")

    oldGUID = dirac.getLfnMetadata(oldLFN)
    if not oldGUID["OK"] or oldGUID["Value"]["Failed"]:
        leave("Could not obtain GUID from FC for %s - %s" % oldLFN, oldGUID, exitCode=2)
    oldGUID = oldGUID["Value"]["Successful"][oldLFN]["GUID"]
    gLogger.verbose(f"Existing GUID is {oldGUID}")

    # retrieve original file
    localFile = os.path.join(directory, os.path.basename(oldLFN))
    if not os.path.exists(localFile):
        download = dirac.getFile(oldLFN, directory)
        if not download["OK"] or download["Value"]["Failed"]:
            leave(f"Could not download file with message - {download['Message']}", download, exitCode=2)
    else:
        gLogger.always(f"Found file {os.path.basename(oldLFN)} in local directory, will not re-download")

    newGUID = makeGuid(localFile)[localFile]

    if newGUID == oldGUID:
        leave(f"Old and new GUIDs have the same value ({oldGUID}), exiting without changes")

    if safe:
        leave(f"Safe mode - found file GUID = {newGUID} and existing GUID = {oldGUID}, exiting without changes")

    gLogger.verbose(f"Will set old GUID to {newGUID} from {oldGUID}")
    if newLFN == oldLFN:
        gLogger.always("Removing old LFN from storages before adding new LFN")
        result = dirac.removeFile(oldLFN)
        if not result["OK"]:
            leave("Could not remove existing LFN from Grid storage", result, exitCode=2)

    gLogger.always(f"Uploading {localFile} as LFN:{newLFN} with replica at {storageElements[0]} and GUID = {newGUID}")
    result = dirac.addFile(newLFN, localFile, storageElements[0], fileGuid=newGUID, printOutput=False)
    if not result["OK"]:
        leave(f"Failed to copy and register new LFN:{newLFN}", result, exitCode=2)

    leave("")


if __name__ == "__main__":
    main()
