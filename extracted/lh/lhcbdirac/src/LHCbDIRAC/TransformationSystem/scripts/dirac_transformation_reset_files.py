#! /usr/bin/env python
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
"""Set the status (default Unused) of a list of LFNs or files in status
<Status> of Transformation <TransID>"""
import DIRAC

from DIRAC.Core.Base.Script import Script


@Script()
def main():
    from LHCbDIRAC.DataManagementSystem.Client.DMScript import DMScript

    dmScript = DMScript()
    dmScript.registerFileSwitches()
    newStatus = "Unused"
    statusList = (
        "Unused",
        "Assigned",
        "Done",
        "Problematic",
        "MissingLFC",
        "MissingInFC",
        "MaxReset",
        "Processed",
        "NotProcessed",
        "Removed",
        "ProbInFC",
    )
    Script.registerSwitch("", "Status=", f"Select files with a given status from {str(statusList)}")
    Script.registerSwitch("", "NewStatus=", f"New status to be set (default: {newStatus})")
    Script.setUsageMessage(
        __doc__
        + "\n".join(
            [
                "Usage:",
                f"  {Script.scriptName} [option|cfgfile] <TransID> <Status>",
            ]
        )
    )
    Script.parseCommandLine()

    from DIRAC.Core.Utilities.List import breakListIntoChunks
    from DIRAC.TransformationSystem.Client.TransformationClient import TransformationClient
    from DIRAC.TransformationSystem.Utilities.ScriptUtilities import getTransformations

    switches = Script.getUnprocessedSwitches()
    status = None
    for opt, val in switches:
        if opt == "Status":
            val = set(val.split(","))
            if val & set(statusList) != val:
                print(f"Unknown status {','.join(val)}... Select in {str(statusList)}")
                Script.showHelp(exitCode=1)
            status = list(val)
        elif opt == "NewStatus":
            if val not in statusList:
                print(f"Unknown status {val}... Select in {str(statusList)}")
                Script.showHelp()
                DIRAC.exit(1)
            newStatus = val

    args = Script.getPositionalArgs()
    idList = getTransformations([args[0]])
    if not idList:
        DIRAC.exit(1)

    if len(args) == 2:
        status = args[1].split(",")
    elif not status:
        status = ["Unknown"]
    lfnsExplicit = dmScript.getOption("LFNs")

    transClient = TransformationClient()

    for transID in idList:
        lfns = lfnsExplicit
        if not lfns:
            res = transClient.getTransformation(transID)
            if not res["OK"]:
                print(f"Failed to get transformation information: {res['Message']}")
                DIRAC.exit(2)

            selectDict = {"TransformationID": res["Value"]["TransformationID"], "Status": status}
            res = transClient.getTransformationFiles(condDict=selectDict)
            if not res["OK"]:
                print(f"Failed to get files: {res['Message']}")
                DIRAC.exit(2)

            lfns = [d["LFN"] for d in res["Value"]]
            if not lfns:
                print(f"No files found in transformation {transID}, status {status}")

        if not lfns:
            print("No files to be set in transformation", transID)
        else:
            resetFiles = 0
            failed = {}
            for lfnChunk in breakListIntoChunks(lfns, 10000):
                force = "MaxReset" in status or "Processed" in status or lfnsExplicit
                res = transClient.setFileStatusForTransformation(transID, newStatus, lfnChunk, force=force)
                if res["OK"]:
                    resetFiles += len(res["Value"].get("Successful", res["Value"]))
                    for lfn, reason in res["Value"].get("Failed", {}).items():
                        if reason != "File not found in the Transformation Database":
                            failed.setdefault(reason, []).append(lfn)
                else:
                    print(
                        "Failed to set %d files to %s in transformation %s: %s"
                        % (len(lfns), newStatus, transID, res["Message"])
                    )
            print("%d files were set %s in transformation %s" % (resetFiles, newStatus, transID))
            if failed:
                for reason in failed:
                    print(f"Failed for {len(failed[reason])} files: {reason}")
    DIRAC.exit(0)


if __name__ == "__main__":
    main()
