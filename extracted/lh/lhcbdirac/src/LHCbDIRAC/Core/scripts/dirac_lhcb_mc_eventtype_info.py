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
"""Report info on event types for MC"""
from collections import defaultdict
import DIRAC
from DIRAC.Core.Base.Script import Script
from LHCbDIRAC.BookkeepingSystem.Client.BookkeepingClient import BookkeepingClient
from LHCbDIRAC.BookkeepingSystem.Client.BKQuery import BKQuery


@Script()
def main():
    Script.registerSwitch("", "FileType=", "FileType to search [default:ALLSTREAMS.DST]")

    Script.setUsageMessage(__doc__ + "\n".join(["Usage:", f"  {Script.scriptName} [option] eventType (mandatory)"]))
    fileType = "ALLSTREAMS.DST"
    Script.parseCommandLine(ignoreErrors=True)
    for switch in Script.getUnprocessedSwitches():
        if switch[0] == "FileType":
            fileType = str(switch[1])

    args = Script.getPositionalArgs()
    if len(args) < 1:
        Script.showHelp(exitCode=1)

    eventTypes = args[0]
    bkQuery = BKQuery({"EventType": eventTypes, "ConfigName": "MC"}, fileTypes=fileType, visible=True)
    print("BK query:", bkQuery)
    prods = bkQuery.getBKProductions()

    pathInfo = defaultdict(lambda: defaultdict(int))
    for prod in prods:
        res = BookkeepingClient().getProductionInformation(prod)
        if not res["OK"]:
            print(res["Message"])
            DIRAC.exit(1)
        value = res["Value"]
        path = value["Path"].split("\n")[1]
        nfiles = 0
        for nf in value["Number of files"]:
            if nf[1] == fileType:
                nfiles += nf[0]
        nevents = 0
        for ne in value["Number of events"]:
            if ne[0] == fileType:
                nevents += ne[1]
        pathInfo[path]["Files"] += nfiles
        pathInfo[path]["Events"] += nevents

    for path in sorted(pathInfo):
        print(f"{path}: {pathInfo[path]['Files']} files, {pathInfo[path]['Events']} events")


if __name__ == "__main__":
    main()
