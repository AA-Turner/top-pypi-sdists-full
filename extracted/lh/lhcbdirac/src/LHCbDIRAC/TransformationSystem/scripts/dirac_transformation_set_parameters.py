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
"""Adds a parameter to an existing transformation"""

from DIRAC import gLogger
from DIRAC.Core.Base.Script import Script


@Script()
def main():
    from LHCbDIRAC.TransformationSystem.Utilities.PluginScript import PluginScript

    pluginScript = PluginScript()
    pluginScript.registerPluginSEParameters()
    pluginScript.registerPluginAdditionalParameters()
    Script.registerSwitch("", "Name=", "   Give a name to the transformation, only if files are given")
    Script.registerSwitch("", "Unique", "   Refuses to create a transformation with an existing name")

    Script.parseCommandLine(ignoreErrors=True)

    from DIRAC.TransformationSystem.Utilities.ScriptUtilities import getTransformations

    from LHCbDIRAC.DataManagementSystem.Client.AddTransformation import getTransformationName
    from LHCbDIRAC.TransformationSystem.Client.Transformation import Transformation
    from LHCbDIRAC.TransformationSystem.Client.TransformationClient import TransformationClient

    transList = getTransformations(Script.getPositionalArgs())

    transClient = TransformationClient()
    pluginParams = pluginScript.getPluginParameters()
    pluginSEParams = pluginScript.getPluginSEParameters()

    switches = Script.getUnprocessedSwitches()
    transName = None
    unique = False
    for opt, val in switches:
        if opt == "Name":
            transName = val
        elif opt == "Unique":
            unique = True

    for transID in transList:
        transformation = Transformation(transID, transClient)
        if transName:
            tName = getTransformationName(transName, unique)
            # Set name only if it doesn't exist
            if tName:
                res = transformation.setTransformationName(tName)
                if not res["OK"]:
                    gLogger.error("Error setting transformation name", f"as {tName} : {res['Message']}")
                else:
                    gLogger.notice("Successfully set transformation name", f"as {tName}")
            else:
                gLogger.error("Cannot set transformation name", f"as {transName}")
        for key, val in pluginSEParams.items():
            res = transformation.setSEParam(key, val)
            if not res["OK"]:
                gLogger.error("Error setting SE parameter", f"{key} = {val} : {res['Message']}")
            else:
                gLogger.notice("Successfully set parameter", f"{key} = {val}")
        for key, val in pluginParams.items():
            res = transformation.setAdditionalParam(key, val)
            if not res["OK"]:
                gLogger.error("Error setting additional parameter", f"{key} = {val} : {res['Message']}")
            else:
                gLogger.notice("Successfully set parameter", f"{key} = {val}")


if __name__ == "__main__":
    main()
