#!/usr/bin/env python

__RCSID__ = "$Id$"

# generic imports
import os
from multiprocessing import Pool

# DIRAC imports
import DIRAC
from DIRAC import gLogger
from DIRAC.Core.Base.Script import Script
from DIRAC.DataManagementSystem.Client.DataManager import DataManager

from CTADIRAC.Core.Utilities.tool_box import read_inputs_from_file

Script.setUsageMessage(
    """
Extension of dirac-dms-replicate-lfn in multi-thread mode
Allows for bulk replication of a list of LFNs to a destination Storage Element
Usage:
   cta-prod-replicate-lfn <lfn> <SE>
   cta-prod-replicate-lfn <ascii file with lfn list> <SE>
"""
)

Script.parseCommandLine(ignoreErrors=True)

args = Script.getPositionalArgs()
if len(args) > 1:
    infile = args[0]
    SE = args[1]
else:
    Script.showHelp()

DIRAC.initialize()


@Script()
def main():
    if os.path.isfile(infile):
        infileList = read_inputs_from_file(infile)
    else:
        infileList = [infile]
    p = Pool(10)
    p.map(replicateFile, infileList)


def replicateFile(lfn):
    voName = lfn.split("/")[1]
    if voName not in ["ctao", "vo.cta.in2p3.fr"]:
        message = (
            f"Wrong lfn: path must start with vo name (ctao or vo.cta.in2p3.fr):\n{lfn}"
        )
        gLogger.error(message)
        return
    dm = DataManager(vo=voName)
    res = dm.replicateAndRegister(lfn, SE)
    if not res["OK"]:
        gLogger.error("Error replicating file", lfn)
        return res["Message"]


if __name__ == "__main__":
    main()
