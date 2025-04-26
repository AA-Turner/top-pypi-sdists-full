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
"""Get Data Quality Flag for the given run."""
import DIRAC

from DIRAC import gLogger
from DIRAC.Core.Base.Script import Script


@Script()
def main():
    Script.setUsageMessage(
        __doc__
        + "\n".join(
            ["Usage:", f"  {Script.scriptName} [option|cfgfile] ... Run ...", "Arguments:", "  Run:      Run number"]
        )
    )
    Script.parseCommandLine(ignoreErrors=True)
    runSet = {int(id) for arg in Script.getPositionalArgs() for id in arg.split(",")}

    if not runSet:
        Script.showHelp(exitCode=1)

    gLogger.showHeaders(False)
    from LHCbDIRAC.BookkeepingSystem.Client.BookkeepingClient import BookkeepingClient

    cl = BookkeepingClient()

    gLogger.notice("Run Number".ljust(15) + "ExtendedDQOK".ljust(15))

    error = False
    for runId in sorted(runSet):
        retVal = cl.getRunExtendedDQOK(runId)
        if retVal["OK"]:
            systems = ",".join(retVal["Value"])
            gLogger.notice(str(runId).ljust(15) + str(systems).ljust(15))
        else:
            gLogger.error(retVal["Message"])
            error = True

    if error:
        DIRAC.exit(1)


if __name__ == "__main__":
    main()
