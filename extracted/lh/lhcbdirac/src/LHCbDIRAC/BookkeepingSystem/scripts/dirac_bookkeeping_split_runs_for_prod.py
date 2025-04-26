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
"""
Split a bookkeeping path into run ranges containing more or less a certain number of files.
This is used to prepare the (in)famous production spreadsheet

We expect that a one and only one event type be provided
"""

from collections import defaultdict
from DIRAC.Core.Base.Script import Script


def take_run_while(run_files, chunk_size):
    """
    Return list of run number as long as the total number of files
    is not above a certain threshold
    Of course, it can overshoot...

    :param run_files: run_number: nb of files in it
    :param chunk_size: max sum

    :return: run list, sum

    """

    fileSum = 0
    first_idx = 0

    runs = sorted(run_files)
    for i, run in enumerate(runs):
        fileSum += run_files[run]
        if fileSum > chunk_size:
            chunk = runs[first_idx : i + 1]
            first_idx = i + 1
            chunkSum = fileSum
            fileSum = 0
            yield chunk, chunkSum
    yield runs[first_idx:], sum([run_files[run] for run in runs[first_idx:]])


def executeSplitRunsForProd(bkQuery, chunk_size):
    from DIRAC import gLogger, exit as diracExit

    from LHCbDIRAC.BookkeepingSystem.Client.BookkeepingClient import BookkeepingClient

    bkClient = BookkeepingClient()

    if not bkQuery:
        gLogger.notice("No BK query given...")
        diracExit(1)

    runList = sorted(bkQuery.getBKRuns())
    requested_event_type = bkQuery.getBKEventTypes()

    if len(requested_event_type) != 1:
        gLogger.notice("Only one event type supported")
        diracExit(1)

    requested_event_type = int(requested_event_type[0])

    requested_cond = bkQuery.getConditions()

    cond_runs = defaultdict(dict)
    for run in runList:
        res = bkClient.getRunInformations(run)
        if not res["OK"]:
            gLogger.notice(f"Error getting info for run {run}:{res['Message']}")
            continue
        runInfo = res["Value"]
        actual_cond = runInfo["DataTakingDescription"]
        if requested_cond and actual_cond != requested_cond:
            continue
        try:
            nb_of_files = runInfo["Number of file"][runInfo["Stream"].index(requested_event_type)]
            cond_runs[actual_cond][run] = nb_of_files
            pass
        # No files of the requested event type
        except ValueError:
            continue

    for cond, runsDict in cond_runs.items():
        for run_list, nb_of_files in take_run_while(runsDict, chunk_size):
            print(f"{cond}:{run_list[0]}:{run_list[-1]}:{nb_of_files}")


@Script()
def main():
    from LHCbDIRAC.DataManagementSystem.Client.DMScript import DMScript

    dmScript = DMScript()
    dmScript.registerBKSwitches()
    Script.registerSwitch("", "ChunkSize=", "   Size of the chunks (default 50000)")

    Script.setUsageMessage(__doc__ + "\n".join(["Usage:", f"  {Script.scriptName} [option|cfgfile] ... "]))

    Script.parseCommandLine(ignoreErrors=True)

    chunk_size = 50000
    switches = Script.getUnprocessedSwitches()
    for switch in switches:
        if switch[0] == "ChunkSize":
            chunk_size = int(switch[1])

    executeSplitRunsForProd(dmScript.getBKQuery(), chunk_size)


if __name__ == "__main__":
    main()
