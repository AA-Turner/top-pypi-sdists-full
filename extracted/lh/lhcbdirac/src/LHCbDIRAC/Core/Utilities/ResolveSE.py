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
"""Resolve SE takes the workflow SE description and returns the list of
destination storage elements for uploading an output file."""
from DIRAC import gLogger
from DIRAC.DataManagementSystem.Utilities.ResolveSE import getDestinationSEList as diracGetDestinationSEList


def getDestinationSEList(outputSE, site, outputmode="Any", run=None):
    """Evaluate the output SE list from a workflow and return the concrete list
    of SEs to upload output data."""
    if outputmode.lower() not in ("any", "local", "run"):
        raise RuntimeError("Unexpected outputmode")

    if outputmode.lower() == "run":
        gLogger.verbose("Output mode set to 'run', thus ignoring site parameter")
        if not run:
            raise RuntimeError("Expected runNumber")
        try:
            run = int(run)
        except ValueError as ve:
            raise RuntimeError(f"Expected runNumber as a number: {ve}")

        gLogger.debug("RunNumber = %d" % run)
        from LHCbDIRAC.TransformationSystem.Client.TransformationClient import TransformationClient

        runDestination = TransformationClient().getDestinationForRun(run)
        if not runDestination["OK"] or run not in runDestination["Value"]:
            raise RuntimeError(
                "Issue getting destinationForRun (%d): " % run + runDestination.get("Message", "unknown run")
            )
        site = runDestination["Value"][run]
        gLogger.verbose("Site set to %s for run %d" % (site, run))
        outputmode = "Local"

    return diracGetDestinationSEList(outputSE, site, outputmode)
