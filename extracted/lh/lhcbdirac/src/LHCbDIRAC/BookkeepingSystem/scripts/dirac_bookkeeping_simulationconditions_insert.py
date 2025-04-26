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
"""Insert a new set of simulation conditions in the Bookkeeping.

To run this script interactively pass no keyword arguments. The script will
then prompt you for the required information.

Alternatively, you can run the script in batch mode by --batch. In this case,
you need to provide all the required information as keyword arguments.
"""
from functools import partial

import DIRAC
from DIRAC import gLogger
from DIRAC.Core.Base.Script import Script
from DIRAC.Core.Utilities.ReturnValues import convertToReturnValue

REQUIRED_KEYS = {
    "SimDescription",
    "BeamCond",
    "BeamEnergy",
    "Generator",
    "MagneticField",
    "DetectorCond",
    "Luminosity",
    "G4settings",
}


def parseArgs():
    condDict = {"Visible": "Y"}
    batch = False

    @convertToReturnValue
    def setKey(key: str, value: str):
        condDict[key] = value

    @convertToReturnValue
    def setBatch(_):
        nonlocal batch
        batch = True

    switches = [
        ("", "sim-description=", "SimDescription", partial(setKey, "SimDescription")),
        ("", "beam-cond=", "BeamCond", partial(setKey, "BeamCond")),
        ("", "beam-energy=", "BeamEnergy", partial(setKey, "BeamEnergy")),
        ("", "generator=", "Generator", partial(setKey, "Generator")),
        ("", "magnetic-field=", "MagneticField", partial(setKey, "MagneticField")),
        ("", "detector-cond=", "DetectorCond", partial(setKey, "DetectorCond")),
        ("", "luminosity=", "Luminosity", partial(setKey, "Luminosity")),
        ("", "g4settings=", "G4settings", partial(setKey, "G4settings")),
        ("", "batch", "Don't ask for confirmation before inserting", setBatch),
    ]
    Script.registerSwitches(switches)
    Script.parseCommandLine(ignoreErrors=False)

    if batch:
        misingKeys = REQUIRED_KEYS - set(condDict.keys())
        if misingKeys:
            gLogger.error(f"Running with --batch but missing required keys: {misingKeys}")
            DIRAC.exit(1)

    return condDict, batch


@Script()
def main():
    condDict, batch = parseArgs()

    from LHCbDIRAC.BookkeepingSystem.Client.BookkeepingClient import BookkeepingClient

    bk = BookkeepingClient()

    for key in REQUIRED_KEYS:
        if key not in condDict:
            condDict[key] = input(f"{key}: ")

    if not batch:
        gLogger.notice("Do you want to add these new simulation conditions? (yes or no)")
        value = input("Choice:")
        choice = value.lower()
        if choice not in ["yes", "y"]:
            gLogger.notice("Aborted!")
            DIRAC.exit(2)

    res = bk.insertSimConditions(condDict)
    if not res["OK"]:
        gLogger.error(res["Message"])
        DIRAC.exit(3)

    gLogger.notice("The simulation conditions added successfully!")


if __name__ == "__main__":
    main()
