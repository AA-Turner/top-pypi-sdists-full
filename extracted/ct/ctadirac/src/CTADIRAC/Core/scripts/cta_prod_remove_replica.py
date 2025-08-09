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
Bulk removal of a list of replicas or a single replicas from a given SE
Usage:
   cta-prod-remove-replica [options] <lfn> <SE>
   cta-prod-remove-replica [options] <ascii file with lfn list> <SE>
"""
)

Script.parseCommandLine(ignoreErrors=True)

DIRAC.initialize()

args = Script.getPositionalArgs()
if len(args) > 1:
    infile = args[0]
    SE = args[1]
else:
    Script.showHelp()

if os.path.isfile(infile):
    infileList = read_inputs_from_file(infile)
else:
    infileList = [infile]


def removeReplica(lfn):
    voName = lfn.split("/")[1]
    if voName not in ["ctao", "vo.cta.in2p3.fr"]:
        message = (
            f"Wrong lfn: path must start with vo name (ctao or vo.cta.in2p3.fr):\n{lfn}"
        )
        gLogger.error(message)
        return
    dm = DataManager(vo=voName)
    res = dm.removeReplica(SE, lfn)
    if not res["OK"]:
        message = res["Message"]
        gLogger.error(f"Error removing replica {lfn} from {SE}:\n{message}")
        return


@Script()
def main():
    p = Pool(10)
    p.map(removeReplica, infileList)


if __name__ == "__main__":
    main()
