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
"""Set ExtendedDQOK systems for the given run."""
import DIRAC
from DIRAC.Core.Base.Script import Script


@Script()
def main():
    Script.registerSwitch("", "Overwrite", "Overwrite already registered list")
    Script.setUsageMessage(
        __doc__
        + "\n".join(
            [
                "Usage:",
                f"  {Script.scriptName} [option|cfgfile] ... Run [Systems]",
                "Arguments:",
                "  Run:      Run number",
                "  Systems:  Comma separated list of system names (unset all when not specified)",
            ]
        )
    )
    Script.parseCommandLine(ignoreErrors=True)
    overwrite = False
    for switch in Script.getUnprocessedSwitches():
        if switch[0] == "Overwrite":
            overwrite = True
    args = Script.getPositionalArgs()

    from LHCbDIRAC.BookkeepingSystem.Client.BookkeepingClient import BookkeepingClient

    bk = BookkeepingClient()

    systems = []
    if len(args) not in {1, 2}:
        Script.showHelp()
    elif len(args) == 2:
        systems = args[1].split(",")

    exitCode = 0
    rnb = int(args[0])
    result = bk.setExtendedDQOK(rnb, overwrite, systems)

    if not result["OK"]:
        if "ORA-20007" in result["Message"]:
            print("ERROR: different list is already registered for the run (use --Overwrite when desired)")
        else:
            print(f"ERROR: {result['Message']}")
        exitCode = 2
    else:
        print("The list was updated")

    DIRAC.exit(exitCode)


if __name__ == "__main__":
    main()
