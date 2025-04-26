###############################################################################
# (c) Copyright 2022 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""Run a local test job for based on a production request YAML specification"""
from __future__ import annotations

import json
import os
import random
import shlex
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path
from textwrap import dedent

import yaml

from DIRAC import gLogger
from DIRAC.ConfigurationSystem.Client.Helpers import CSGlobals
from DIRAC.Core.Base.Script import Script
from DIRAC.Core.Utilities.ReturnValues import returnValueOrRaise, convertToReturnValue


from LHCbDIRAC.ProductionManagementSystem.Utilities.Models import (
    parse_obj,
    ProductionBase,
    SimulationProduction,
    DataProduction,
    ProductionStep,
)


def preprocess_spec(pr: ProductionBase):
    """production-request-run-local does not support multiple input types so easily, so we need to split them"""
    new_steps = []

    for step in pr.steps:
        if len(step.input) > 1:
            print(f"Splitting step {step.name}")
            # we need to split this step
            for i, input_filetype in enumerate(step.input):
                split_step = step.model_copy(
                    deep=True,
                    update={
                        "name": f"{step.name}ft{i}",
                        "processing_pass": f"{step.processing_pass}{i}",
                        "input": [input_filetype],
                        "output": [input_filetype.model_copy(deep=True)],
                    },
                )
                new_steps.append(split_step)
                print(split_step)
        else:
            new_steps.append(step)
    return pr.model_copy(
        deep=True,
        update={
            "steps": new_steps,
        },
    )


def parseArgs():
    useCfgOverride = True
    inputFiles = None
    inputFileType = None
    ancestorDepth = None
    numTestLFNs = 1
    testRunNumbers = None
    startRun = None
    endRun = None
    exportTestLFNs = None

    @convertToReturnValue
    def disableCfgOverride(_):
        nonlocal useCfgOverride
        useCfgOverride = False

    @convertToReturnValue
    def setInputFiles(s: str):
        nonlocal inputFiles
        inputFiles = s.split(",")

    @convertToReturnValue
    def setOutputFileType(s: str):
        nonlocal inputFileType
        inputFileType = s

    @convertToReturnValue
    def setAncestorDepth(s: str):
        nonlocal ancestorDepth
        ancestorDepth = int(s)

    @convertToReturnValue
    def setNumTestLFNs(s: str):
        nonlocal numTestLFNs
        numTestLFNs = int(s)

    @convertToReturnValue
    def setTestRunNumbers(s: str):
        nonlocal testRunNumbers
        testRunNumbers = s.split(",")

    @convertToReturnValue
    def setStartRun(s: str):
        nonlocal startRun
        startRun = int(s)

    @convertToReturnValue
    def setEndRun(s: str):
        nonlocal endRun
        endRun = int(s)

    @convertToReturnValue
    def setExportTestLFNsPath(s: str):
        nonlocal exportTestLFNs
        exportTestLFNs = s

    switches = [
        ("", "input-files=", "Comma separated list of input files (Data only)", setInputFiles),
        ("", "no-cfg-override", "Internal implementation detail", disableCfgOverride),
        ("", "input-file-type=", "Limit the file type for generic merge steps", setOutputFileType),
        ("", "ancestor-depth=", "Set the ancestor depth that should be included in the pool catalog", setAncestorDepth),
        ("", "num-test-lfns=", "Number of LFNs to test with", setNumTestLFNs),
        ("", "test-runs=", "Comma separated list of test runs to use", setTestRunNumbers),
        ("", "start-run=", "Start run number for data production", setStartRun),
        ("", "end-run=", "End run number for data production", setEndRun),
        (
            "",
            "export-test-lfns=",
            "Export the LFNs that would have been used for testing to a file",
            setExportTestLFNsPath,
        ),
    ]
    Script.registerSwitches(switches)
    Script.registerArgument("yaml_path: Path to the YAML file containing productions to submit")
    Script.registerArgument("name: Name of the production to submit", mandatory=False)
    Script.registerArgument("event_type: The event type to generate (Simulation only)", mandatory=False)
    Script.parseCommandLine(ignoreErrors=False)
    yaml_path, name, eventType = Script.getPositionalArgs(group=True)

    from DIRAC.ConfigurationSystem.Client.ConfigurationClient import ConfigurationClient

    if not ConfigurationClient().ping()["OK"]:
        gLogger.fatal("Failed to contact CS, do you have a valid proxy?")
        sys.exit(1)

    if (startRun or endRun) and testRunNumbers:
        gLogger.fatal("Cannot specify both --test-runs and --start-run/--end-run")
        sys.exit(1)

    return (
        Path(yaml_path),
        name,
        eventType,
        inputFiles,
        useCfgOverride,
        inputFileType,
        ancestorDepth,
        numTestLFNs,
        testRunNumbers,
        startRun,
        endRun,
        exportTestLFNs,
    )


def _runWithConfigOverride(argv):
    """Relaunch the process with DIRACSYSCONFIG overridden for local tests"""
    cfg_content = f"""
    DIRAC
    {{
        Setup={CSGlobals.getSetup()}
    }}
    LocalSite
    {{
        Site = DIRAC.LocalProdTest.local
        GridCE = jenkins.cern.ch
        CEQueue = jenkins-queue_not_important
        LocalSE = CERN-DST-EOS
        LocalSE += CERN-HIST-EOS
        LocalSE += CERN-RAW
        LocalSE += CERN-FREEZER-EOS
        LocalSE += CERN-SWTEST
        Architecture = x86_64-centos7
        SharedArea = /cvmfs/lhcb.cern.ch/lib
        CPUTimeLeft = 123456
    }}
    """
    with tempfile.NamedTemporaryFile(mode="wt") as tmp:
        tmp.write(dedent(cfg_content))
        tmp.flush()

        env = dict(os.environ)
        env["DIRACSYSCONFIG"] = ",".join([tmp.name] + env.get("DIRACSYSCONFIG", "").split(","))

        gLogger.always("Overriding DIRACSYSCONFIG to", env["DIRACSYSCONFIG"])
        gLogger.always("Restarting process with", argv)
        proc = subprocess.run(argv, env=env, check=False)
    sys.exit(proc.returncode)


@Script()
def main():
    (
        yamlPath,
        name,
        eventType,
        inputFiles,
        useCfgOverride,
        inputFileType,
        ancestorDepth,
        numTestLFNs,
        testRunNumbers,
        startRun,
        endRun,
        exportTestLFNs,
    ) = parseArgs()

    if useCfgOverride:
        return _runWithConfigOverride(sys.argv + ["--no-cfg-override"])

    productionRequests = defaultdict(list)
    for spec in yaml.safe_load(yamlPath.read_text()):
        productionRequest = parse_obj(spec)
        productionRequest = preprocess_spec(productionRequest)
        productionRequests[productionRequest.name] += [productionRequest]

    if name is None:
        if len(productionRequests) == 1:
            name = list(productionRequests)[0]
        else:
            gLogger.fatal(
                "Multiple production requests available, please specify a name. Available options are:\n",
                "   * " + "\n    * ".join(map(shlex.quote, productionRequests)),
            )
            sys.exit(1)
    if name not in productionRequests:
        gLogger.fatal(
            "Unrecognised production request name. Available options are:\n",
            "   * " + "\n    * ".join(map(shlex.quote, productionRequests)),
        )
        sys.exit(1)
    if len(productionRequests[name]) > 1:
        gLogger.fatal("Ambiguous production requests found with identical names", shlex.quote(name))
        sys.exit(1)
    productionRequest = productionRequests[name][0]

    numTestEvents = None
    if isinstance(productionRequest, SimulationProduction):
        availableEventTypes = {e.id: e.num_test_events for e in productionRequest.event_types}
        if eventType is None and isinstance(productionRequest, SimulationProduction):
            if len(productionRequest.event_types) == 1:
                eventType = productionRequest.event_types[0].id
            else:
                gLogger.fatal(
                    "Multiple event types available, please specify a one.\nAvailable options are:\n",
                    "   * " + "\n    * ".join(availableEventTypes),
                )
                sys.exit(1)
        if eventType not in availableEventTypes:
            gLogger.fatal(f"Invalid event type passed ({eventType}), available options are: {availableEventTypes!r}")
            sys.exit(1)
        numTestEvents = availableEventTypes[eventType]
    elif eventType is not None:
        gLogger.fatal(f"{eventType!r} but this is not a simulation production!")
        sys.exit(1)

    pr, kwargs = prepareProductionRequest(
        productionRequest,
        eventType=eventType,
        numTestEvents=numTestEvents,
        inputFiles=inputFiles,
        inputFileType=inputFileType,
        ancestorDepth=ancestorDepth,
        numTestLFNs=numTestLFNs,
        testRunNumbers=testRunNumbers,
        startRun=startRun,
        endRun=endRun,
    )

    if exportTestLFNs:
        Path(exportTestLFNs).write_text(json.dumps(kwargs["inputDataList"]))
        gLogger.notice(f"Exported test LFNs to {exportTestLFNs}")
        sys.exit(0)

    # TODO: pr._buildProduction eats stepsInProd
    prod = pr._buildProduction(**kwargs)
    returnValueOrRaise(prod.runLocal())


def prepareProductionRequest(
    productionRequest: ProductionBase,
    *,
    eventType: str | None = None,
    numTestEvents: int = 10,
    inputFiles: list[str] | None = None,
    inputFileType: str | None = None,
    ancestorDepth=None,
    numTestLFNs: int = 1,
    testRunNumbers: list[str] | None = None,
    startRun: int | None = None,
    endRun: int | None = None,
):
    """Prepare a ProductionRequest for running locally and return the kwargs to pass to ProductionRequest._buildProduction"""
    from DIRAC.DataManagementSystem.Client.DataManager import DataManager
    from LHCbDIRAC.BookkeepingSystem.Client.BookkeepingClient import BookkeepingClient
    from LHCbDIRAC.ProductionManagementSystem.Utilities.ModelCompatibility import (
        production_to_legacy_dict,
        configure_input,
    )
    from LHCbDIRAC.ProductionManagementSystem.Client.ProductionRequest import ProductionRequest

    pr = ProductionRequest()
    kwargs = {}
    legacy_dict, _ = production_to_legacy_dict(productionRequest)
    pr.prodGroup = json.loads(legacy_dict["ProDetail"])["pDsc"]
    if isinstance(productionRequest, SimulationProduction):
        pr.configName = "MC"
        pr.configVersion = productionRequest.mc_config_version
        pr.dataTakingConditions = productionRequest.sim_condition
        pr.eventType = eventType

        kwargs |= dict(
            events=numTestEvents,
            multicore=False,
            prodType="MCSimulation" if productionRequest.fast_simulation_type == "None" else "MCFastSimulation",
        )
    elif isinstance(productionRequest, DataProduction):
        if not inputFiles:
            configure_input(pr, legacy_dict, runs=testRunNumbers, startRun=startRun, endRun=endRun)
            bkQueryDict = pr._getBKKQuery().copy()
            if "RunNumbers" in bkQueryDict:
                bkQueryDict["RunNumbers"] = bkQueryDict["RunNumbers"].split(";;;")
            if "DataQualityFlag" in bkQueryDict:
                bkQueryDict["DataQualityFlag"] = bkQueryDict["DataQualityFlag"].split(";;;")
            if "ExtendedDQOK" in bkQueryDict:
                bkQueryDict["ExtendedDQOK"] = bkQueryDict["ExtendedDQOK"].split(";;;")
            result = returnValueOrRaise(BookkeepingClient().getFilesWithMetadata(bkQueryDict))
            if result["TotalRecords"] == 0:
                raise ValueError("No input files found in the bookkeeping")

            # Remove the smallest 50% of files to avoid unusually small files
            sizeIndex = result["ParameterNames"].index("FileSize")
            records = sorted(result["Records"], key=lambda x: x[sizeIndex])
            if len(records) // 2 >= numTestLFNs:
                records = records[len(records) // 2 :]

            # Shuffle the LFNs so we pick a random one
            random.shuffle(records)

            # Only run tests with files which have available replicas
            filenameIndex = result["ParameterNames"].index("FileName")
            inputFiles = []
            for record in records:
                lfn = record[filenameIndex]
                result = returnValueOrRaise(DataManager().getReplicasForJobs([lfn], diskOnly=True))
                inputFiles.extend(result["Successful"])
                if len(inputFiles) == numTestLFNs:
                    break
                if result["Failed"]:
                    gLogger.warn("Skipping LFN as it has no replicas for jobs", result["Failed"])
            else:
                raise ValueError(f"Only {len(inputFiles)} input files found, requested {numTestLFNs}")

        if len(inputFiles) < numTestLFNs:
            raise ValueError(f"Only {len(inputFiles)} input files found, requested {numTestLFNs}")

        kwargs |= dict(
            inputDataList=inputFiles,
            prodType=productionRequest.type,
            inputDataPolicy="download",
        )
    else:
        raise NotImplementedError(type(productionRequest))

    pr.outConfigName = "validation"
    pr.outputSEs = ["Tier1-Buffer"]

    if ancestorDepth is not None:
        kwargs["ancestorDepth"] = ancestorDepth

    kwargs["stepsInProd"] = _steps_to_production_dict(productionRequest.steps, inputFileType)
    kwargs["outputSE"] = {
        t["FileType"]: "Tier1-Buffer" for step in kwargs["stepsInProd"] for t in step["visibilityFlag"]
    }
    kwargs["priority"] = 0
    kwargs["cpu"] = 100

    return pr, kwargs


def _steps_to_production_dict(steps: list[ProductionStep], inputFileType: str | None) -> list[dict]:
    """Convert steps into list of dictionaries expected by ProductionRequest._buildProduction

    Normally this is handled by ProductionRequest.resolveSteps however this only
    supports reading from the bookkeeping.

    TODO: The ProductionRequest class should be refactored.
    """
    from LHCbDIRAC.ProductionManagementSystem.Utilities.ModelCompatibility import step_to_step_manager_dict

    stepsInProd = []
    for i, dirac_step in enumerate(steps):
        result = step_to_step_manager_dict(i + 1, dirac_step)
        step_dict = result["Step"]
        step_dict["StepId"] = step_dict.get("StepId", 12345)
        if len(dirac_step.input) > 1 and inputFileType is None:
            raise NotImplementedError(
                f"Multiple input file types found, pick one of with --input-file-type:"
                f" {' '.join(repr(f.type) for f in dirac_step.input)}"
            )
        step_dict["fileTypesIn"] = [
            f.type for f in dirac_step.input if inputFileType is None or f.type == inputFileType
        ]
        if len(dirac_step.input) > 1:
            print(f"Assuming that step {i+1} is a merging step and reducing output filetypes to {inputFileType}")
            step_dict["fileTypesOut"] = [f.type for f in dirac_step.output if f.type == inputFileType]
            if len(step_dict["fileTypesOut"]) != 1:
                raise NotImplementedError(step_dict["fileTypesOut"])
        else:
            step_dict["fileTypesOut"] = [f.type for f in dirac_step.output]
        step_dict["ExtraPackages"] = ";".join([f"{d.name}.{d.version}" for d in dirac_step.data_pkgs])
        step_dict.setdefault("OptionsFormat", "")
        step_dict.setdefault("SystemConfig", "")
        step_dict.setdefault("mcTCK", "")
        step_dict["ExtraOptions"] = ""
        step_dict["visibilityFlag"] = result["OutputFileTypes"]
        step_dict["EventTimeout"] = None
        # Normally ProductionRequest.resolveSteps will set these but that only supports getting IDs from the bookkeeping
        for field in ["CONDDB", "DDDB", "DQTag"]:
            if step_dict[field] == "fromPreviousStep":
                step_dict[field] = stepsInProd[i - 1][field]
        stepsInProd.append(step_dict)
    return stepsInProd


if __name__ == "__main__":
    main()
