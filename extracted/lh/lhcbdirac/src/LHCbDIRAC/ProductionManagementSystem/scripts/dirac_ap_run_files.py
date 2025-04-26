###############################################################################
# (c) Copyright 2024 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""
Find files in an Analysis Production containing a specified run number.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
import re
from itertools import islice
from pathlib import Path
import sys

from rich.progress import track

from DIRAC import gLogger
from DIRAC.Core.Base.Script import Script
from DIRAC.Core.Utilities.ReturnValues import returnValueOrRaise, convertToReturnValue
from DIRAC.ConfigurationSystem.Client.ConfigurationClient import ConfigurationClient
from LHCbDIRAC.ProductionManagementSystem.Client.AnalysisProductionsClient import AnalysisProductionsClient
from LHCbDIRAC.BookkeepingSystem.Client.BookkeepingClient import BookkeepingClient
from LHCbDIRAC.TransformationSystem.Client.TransformationClient import TransformationClient

from LHCbDIRAC.ProductionManagementSystem.scripts.dirac_ap_input_metadata import (
    _get_info_from_apd,
    _get_ancestors_info,
    _attach_ancestors,
    _batched,
)


def parseArgs():
    version = ""
    output = ""

    @convertToReturnValue
    def setVersion(s: str):
        nonlocal version
        version = s

    @convertToReturnValue
    def setOutput(s: str):
        nonlocal output
        output = s

    switches = [
        ("", "version=", "Version of the Analysis Production (optional)", setVersion),
        ("", "output=", "Path to a file to dump the output to", setOutput),
    ]
    Script.registerSwitches(switches)
    Script.registerArgument("run: run to find files for")
    Script.registerArgument("wg: Name of the WG the production belongs to e.g. `bnoc`")
    Script.registerArgument("analysis: Name of the analysis e.g. `bds2kstkstb`")
    Script.registerArgument("name: Name of the job in the production e.g. `13104007_bs2kst_892_kstb_892_2011_magup`")
    Script.parseCommandLine(ignoreErrors=False)
    run, wg, analysis, name = Script.getPositionalArgs(group=True)
    wg = wg.lower()
    analysis = analysis.lower()
    name = name.lower()
    run = int(run)

    if not ConfigurationClient().ping()["OK"]:
        gLogger.fatal("Failed to contact CS, do you have a valid proxy?")
        sys.exit(1)

    return (
        run,
        wg,
        analysis,
        name,
        version,
        output,
    )


@Script()
def main():
    run, wg, analysis, name, version, output = parseArgs()
    config = {
        "wg": wg,
        "analysis": analysis,
        "name": name,
    }
    if version != "":
        config["version"] = version
    save_output = False
    if output != "":
        output = Path(output)
        save_output = True

    tc = TransformationClient()
    bk = BookkeepingClient()
    apc = AnalysisProductionsClient()

    gLogger.info("Finding Analysis Productions files")
    apd_info = _get_info_from_apd(apc, config)

    gLogger.info("Finding descendents")
    apd_id, filetype = _get_prodid_and_filetype(bk, tc, apd_info)
    collision_files = _get_collision_files(bk, apd_info, filetype, run)

    decs_dict = returnValueOrRaise(
        bk.getFileDescendents(collision_files, depth=apd_info["depth"], checkreplica=True, production=apd_id)
    )

    if decs_dict["Failed"] != []:
        raise RuntimeError("Failed to find descendents")

    lfns_from_run = []
    for lfns in decs_dict["Successful"].values():
        lfns_from_run += lfns

    lfns_from_run = sorted(set(lfns_from_run))

    if lfns_from_run != []:
        gLogger.always(f"Found {len(lfns_from_run)} files in Aprod from run {run}:")
        for lfn in lfns_from_run:
            gLogger.always(lfn)
    else:
        gLogger.warn(f"Could not find any files in Aprod from run {run}")

    if save_output:
        gLogger.always(f"Saving LFNs to {str(output)}")
        with open(output, "w") as out_file:
            for lfn in lfns_from_run:
                out_file.write(f"{lfn}\n")


def _get_prodid_and_filetype(bk, tc, apd_info):
    prev_tid = apd_info["transformations"][0]["id"]
    next_tid = apd_info["transformations"][1]["id"]
    query = None
    prev_query = returnValueOrRaise(tc.getBookkeepingQuery(prev_tid))
    next_query = returnValueOrRaise(tc.getBookkeepingQuery(next_tid))
    if "ProductionID" in prev_query and prev_query["ProductionID"] == next_tid:
        query = next_query
    elif "ProductionID" in next_query and next_query["ProductionID"] == prev_tid:
        query = prev_query
    else:
        raise RuntimeError(
            f"Could not determine the merge step for\
                           {apd_info['transformations']}"
        )
    filetype = query["FileType"]
    return next_tid, filetype


def _get_collision_files(bk, apd_info, filetype, run):
    test_lfn = apd_info["apd_lfns"][0]
    ancestors = returnValueOrRaise(bk.getFileAncestors(test_lfn, depth=apd_info["depth"]))
    if ancestors["Failed"] != []:
        raise FileNotFoundError(f"Could not find ancestors for lfn {test_lfn}")
    job_info = returnValueOrRaise(bk.getJobInfo(ancestors["Successful"][test_lfn][0]["FileName"]))
    prod_id = job_info[0][18]

    collision_query = {"RunNumber": run, "Production": prod_id, "FileType": filetype.upper(), "Visible": "Yes"}
    collision_files = returnValueOrRaise(bk.getFiles(collision_query))
    return collision_files


if __name__ == "__main__":
    main()
