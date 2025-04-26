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

from DIRAC.Core.Base.Script import Script


@Script()
def main():
    from DIRAC.Core.Base.Script import parseCommandLine

    parseCommandLine()

    import sys

    transIDs = Script.getPositionalArgs()
    if not transIDs:
        print("Usage: dirac-production-verify-outputdata transID [transID] [transID]")
        sys.exit()
    transIDs = [int(arg) for arg in transIDs]

    from LHCbDIRAC.TransformationSystem.Agent.ValidateOutputDataAgent import ValidateOutputDataAgent

    agent = ValidateOutputDataAgent(
        "Transformation/ValidateOutputDataAgent",
        "Transformation/ValidateOutputDataAgent",
        "dirac-production-verify-outputdata",
    )
    agent.initialize()

    for transID in transIDs:
        agent.checkTransformationIntegrity(transID)


if __name__ == "__main__":
    main()
