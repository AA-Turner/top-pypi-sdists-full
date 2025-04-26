#!/usr/bin/env python
###############################################################################
# (c) Copyright 2022 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""Create production requests from a YAML document"""
import json
from pathlib import Path

import yaml

from DIRAC import gLogger
from DIRAC.Core.Base.Script import Script
from DIRAC.Core.Utilities.ReturnValues import convertToReturnValue, returnValueOrRaise

from LHCbDIRAC.ProductionManagementSystem.Utilities.Models import parse_obj, ProductionBase


def parseArgs():
    doSubmit = False
    createFiletypes = False
    outputFilename: Path | None = None

    @convertToReturnValue
    def enableSubmit(_):
        nonlocal doSubmit
        doSubmit = True

    @convertToReturnValue
    def enableCreateFiletypes(_):
        nonlocal createFiletypes
        createFiletypes = True

    @convertToReturnValue
    def setOutputFilename(filename):
        nonlocal outputFilename
        outputFilename = Path(filename)

    switches = [
        ("", "submit", "Actually create steps and submit productions", enableSubmit),
        ("", "create-filetypes", "Create missing file types", enableCreateFiletypes),
        ("", "output-json=", "Write the production IDs to a JSON file", setOutputFilename),
    ]
    Script.registerSwitches(switches)
    Script.registerArgument("yaml_path: Path to the YAML file containing productions to submit")
    Script.parseCommandLine(ignoreErrors=False)
    (yaml_path,) = Script.getPositionalArgs()
    return Path(yaml_path), doSubmit, createFiletypes, outputFilename


@Script()
def main():
    yamlPath, doSubmit, createFiletypes, outputFilename = parseArgs()

    productionRequests = [parse_obj(spec) for spec in yaml.safe_load(yamlPath.read_text())]
    productionIDs = submitProductionRequests(productionRequests, dryRun=not doSubmit, createFiletypes=createFiletypes)
    if productionIDs and outputFilename:
        outputFilename.write_text(json.dumps(productionIDs))
    if not doSubmit:
        gLogger.always('This was a dry run! Pass "--submit" to actually submit production requests.')


def submitProductionRequests(
    productionRequests: list[ProductionBase], *, dryRun=True, createFiletypes
) -> list[tuple[int, int | None, dict[str, int | None]]]:
    """Submit a collection of production requests

    :param productionRequests: List of production requests to submit
    :param dryRun: Set to False to actually submit the production requests
    """
    from LHCbDIRAC.BookkeepingSystem.Client.BookkeepingClient import BookkeepingClient
    from LHCbDIRAC.ProductionManagementSystem.Utilities.ModelCompatibility import retValToListOfDict

    # Register filetypes
    requiredFileTypes = set()
    for prod in productionRequests:
        for step in prod.steps:
            requiredFileTypes |= {x.type for x in step.input}
            requiredFileTypes |= {x.type for x in step.output}
    knownFileTypes = {x["FileType"] for x in retValToListOfDict(BookkeepingClient().getAvailableFileTypes())}
    if missingFileTypes := requiredFileTypes - knownFileTypes:
        if not createFiletypes:
            raise NotImplementedError(f"Unknown file types that need to be registered: {missingFileTypes!r}")
        if not dryRun:
            for missingFileType in missingFileTypes:
                returnValueOrRaise(BookkeepingClient().insertFileTypes(missingFileType.upper(), "", "1"))

    # Create steps and submit production requests
    productionIDs = []
    for i, prod in enumerate(productionRequests):
        gLogger.always("Considering production", f"{i+1} of {len(productionRequests)}: {prod.name}")
        prod_id, sub_prod_id = _submitProductionRequests(prod, dryRun=dryRun)
        productionIDs.append([i, prod_id, sub_prod_id])
    return productionIDs


def _submitProductionRequests(prod: ProductionBase, *, dryRun=True) -> tuple[int | None, dict[str, int | None]]:
    from LHCbDIRAC.BookkeepingSystem.Client.BookkeepingClient import BookkeepingClient
    from LHCbDIRAC.ProductionManagementSystem.Client.ProductionRequestClient import ProductionRequestClient
    from LHCbDIRAC.ProductionManagementSystem.Utilities.Models import ProductionStates
    from LHCbDIRAC.ProductionManagementSystem.Utilities.ModelCompatibility import (
        find_step_id,
        make_subprod_legacy_dict,
        production_to_legacy_dict,
        step_to_step_manager_dict,
    )

    prc = ProductionRequestClient()

    for j, step in enumerate(prod.steps, start=1):
        step.id = find_step_id(j, step)
        if step.id is not None:
            gLogger.info(f"Step {j} of {len(prod.steps)}: Found existing step with ID {step.id=}")
            continue

        if step.application.nightly is not None:
            raise ValueError("Nightly builds cannot be used for submitted productions")

        step_info = step_to_step_manager_dict(j, step)
        gLogger.verbose("Running insertStep with", step_info)
        if not dryRun:
            step.id = returnValueOrRaise(BookkeepingClient().insertStep(step_info))
            gLogger.info(f"Step {j} of {len(prod.steps)}: Created step with ID {step.id=}")

    if prod.id is not None:
        raise RuntimeError(f"{prod.id} has already been submitted")
    request_info, sub_productions = production_to_legacy_dict(prod)
    gLogger.verbose(f"Creating production request with", request_info)
    if not dryRun:
        prod.id = returnValueOrRaise(prc.createProductionRequest(request_info))

    sub_prod_ids = {}
    for sub_prod in sub_productions:
        if prod.state != ProductionStates.NEW:
            raise RuntimeError("Can only add sub productions to productions in state 'New'")
        sub_prod_info = make_subprod_legacy_dict(sub_prod, prod.id)
        gLogger.verbose("Creating production sub request with", request_info)
        sub_prod_id = None if dryRun else returnValueOrRaise(prc.createProductionRequest(sub_prod_info))

        event_type = sub_prod["EventType"]
        if event_type in sub_prod_ids:
            raise NotImplementedError(f"Duplicate event type {event_type} in sub productions")
        sub_prod_ids[event_type] = sub_prod_id

    prod.state = ProductionStates.SUBMITTED
    if not dryRun:
        returnValueOrRaise(prc.updateProductionRequest(prod.id, {"RequestState": prod.state.value}))
        gLogger.always(f"Submitted production {prod.id} with sub productions {sub_prod_ids}")
    return prod.id, sub_prod_ids


if __name__ == "__main__":
    main()
