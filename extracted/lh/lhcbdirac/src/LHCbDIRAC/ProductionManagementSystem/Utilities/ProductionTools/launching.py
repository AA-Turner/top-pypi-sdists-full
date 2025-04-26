#!/usr/bin/env python
###############################################################################
# (c) Copyright 2024 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
from __future__ import annotations

__all__ = ["start_productions", "check_validation"]

import traceback
import json
import math

from LHCbDIRAC.ProductionManagementSystem.Utilities.Models import parse_obj
from LHCbDIRAC.ProductionManagementSystem.scripts.dirac_production_request_submit import submitProductionRequests
from DIRAC.Core.Utilities.ReturnValues import returnValueOrRaise
from LHCbDIRAC.TransformationSystem.Client.Transformation import Transformation
from LHCbDIRAC.TransformationSystem.Client.TransformationClient import TransformationClient
from LHCbDIRAC.ProductionManagementSystem.Client.ProductionRequest import ProductionRequest
from LHCbDIRAC.BookkeepingSystem.Client.BookkeepingClient import BookkeepingClient
from LHCbDIRAC.ProductionManagementSystem.Client.ProductionRequestClient import ProductionRequestClient
from LHCbDIRAC.ProductionManagementSystem.Utilities.ModelCompatibility import configure_input, runs_to_input_query

from .integrations import Validation, Request, RepoIssue


def get_request_state(request_id):
    return returnValueOrRaise(ProductionRequestClient().getProductionRequest([request_id]))[int(request_id)][
        "RequestState"
    ]


def update_request_state(request_id, state):
    returnValueOrRaise(ProductionRequestClient().updateProductionRequest(int(request_id), {"RequestState": state}))
    print(f"Request {request_id} set to {state}")


def start_productions(logbook, issue):
    if "state::run-validation" in issue.labels:
        validation = True
    elif "state::ready" in issue.labels:
        if not issue.metadata.validations:
            raise NotImplementedError("No validation found")
        for request_id, request_info in issue.metadata.validations.items():
            if request_info.running:
                raise NotImplementedError()
            for result in returnValueOrRaise(
                TransformationClient().getTransformations(
                    {"TransformationID": request_info.transform_ids}, columns=["TransformationID", "Status"]
                )
            ):
                if result["Status"] not in {"Cleaning", "Cleaned"}:
                    raise NotImplementedError(f"Request {request_id} is not cleaned")
            current_state = get_request_state(request_id)
            if current_state == "Active":
                update_request_state(request_id, "Done")
            elif current_state not in {"Done", "Rejected"}:
                raise NotImplementedError(f"Request {request_id} is in state {current_state}")
        validation = False
    else:
        raise NotImplementedError(issue.labels)

    productionRequest = parse_obj(issue.request_yaml)
    match productionRequest.type:
        case "Sprucing":
            launch_func = launch_sprucing
            logbook_systems = ["Sprucing", "Production"]
        case "Reconstruction":
            launch_func = launch_reco
            logbook_systems = ["Production"]
        case _:
            raise NotImplementedError(productionRequest.type)
    if validation:
        productionRequest.name = f"Validation - {productionRequest.name}"
    productionIDs = submitProductionRequests([productionRequest], dryRun=False, createFiletypes=True)

    request_id = productionIDs[0][1]

    print("Submitted request", request_id)
    transform_ids, n_files_expected = launch_func(
        request_id,
        validation=validation,
        validation_runs=issue.run_yaml["validation_runs"],
        start_run=issue.run_yaml["start_run"],
        end_run=issue.run_yaml["end_run"],
    )

    try:
        if validation:
            if request_id in issue.metadata.validations:
                raise NotImplementedError()
            issue.metadata.validations[request_id] = Validation(
                transform_ids=transform_ids,
                n_files_expected=n_files_expected,
            )
        else:
            issue.labels.pop(issue.labels.index("state::ready"))
            issue.labels.append("state::running-concurrent" if issue.run_yaml["concurrent"] else "state::running")
            issue.metadata.requests[request_id] = Request(transform_ids=transform_ids)
        issue.update_metadata()
    except Exception:
        print("Failed to update metadata in issue", issue.metadata)
        traceback.print_exc()

    subject = productionRequest.name
    if validation:
        body = f"Validation production was submitted with request ID: {request_id}"
    else:
        body = f"Production was submitted with request ID: {request_id}"
    if validation:
        subject = f"{subject} - Validation"
    attachments = {
        f"{request_id}-request.yaml": issue.request_yaml_blob,
        f"{request_id}-extra.yaml": issue.run_yaml_blob,
    }
    try:
        logbook.create_post(issue.url, transform_ids, subject, body, attachments, logbook_systems)
    except Exception:
        print("Failed to post to logbook")
        traceback.print_exc()

    try:
        update_request_state(request_id, "Active")
    except Exception:
        print("Failed to set request to active")
        traceback.print_exc()


def start_removal_transformation(logbook, issue: RepoIssue, request_id: int):
    if "state::running" not in issue.labels:
        raise NotImplementedError("Only submitting removals for issues in state::running")

    request_metadata = issue.metadata.requests[request_id]
    sprucing_tid, merging_tid = request_metadata.transform_ids

    tc = TransformationClient()
    bkquery = returnValueOrRaise(tc.getBookkeepingQuery(sprucing_tid))
    bkquery["ProcessingPass"] = "/" + bkquery["ProcessingPass"]
    extra_param = returnValueOrRaise(tc.getAdditionalParameters(sprucing_tid))
    removal_trans = Transformation()
    removal_trans.setType("Removal")

    trans_name = "/".join(
        [
            "Removal-",
            bkquery["ConfigName"],
            bkquery["ConfigVersion"],
            bkquery["DataTakingConditions"],
            bkquery["ProcessingPass"],
            str(bkquery["EventType"]),
            f"{bkquery['FileType']}-issue-{issue.issue.iid}",
        ]
    )
    removal_trans.setBkQuery(bkquery)
    removal_trans.setTransformationName(trans_name)
    removal_trans.setTransformationGroup("RemoveReplicasWhenProcessed")
    removal_trans.setPlugin("RemoveReplicasWhenProcessed")
    removal_trans.setBody("removal;RemoveReplica")
    removal_trans.setSEParam("FromSEs", "['Tier1-Buffer']")
    long_name = f"RemoveReplicasWhenProcessed for issue {issue.issue.iid}"
    removal_trans.setDescription(long_name[:255])
    removal_trans.setLongDescription(long_name[:255])
    removal_trans.setAdditionalParam("ProcessingPasses", extra_param["groupDescription"].strip("/"))
    # removal_trans.setStatus("Active")
    removal_trans.setAgentType("Automatic")
    returnValueOrRaise(removal_trans.addTransformation())
    removal_id = returnValueOrRaise(removal_trans.getTransformationID())
    print(f"Submitted removal transforation {request_id=} {removal_id=}", request_id)

    try:

        issue.metadata.requests[request_id].removal = removal_id
        issue.update_metadata()
    except Exception:
        print("Failed to update metadata in issue", issue.metadata)
        traceback.print_exc()

    productionRequest = parse_obj(issue.request_yaml)
    subject = f"Removal for {productionRequest.name}"
    body = f"Removal transformation was submitted: {removal_id}\n\n"

    body += json.dumps(removal_trans.paramValues, indent=3)

    try:
        logbook.create_post(issue.url, [removal_id], subject, body, {}, ["Sprucing", "Data Management", "Production"])
    except Exception:
        print("Failed to post to logbook")
        traceback.print_exc()


def check_validation(issue, prod_id):
    request_metadata = issue.metadata.validations[prod_id]

    if not request_metadata.running:
        raise NotImplementedError()

    result = returnValueOrRaise(
        TransformationClient().getTransformations(
            {"TransformationID": request_metadata.transform_ids}, columns=["TransformationID", "Status"]
        )
    )
    statuses = {x["Status"] for x in result}
    if statuses.issubset({"Cleaning", "Cleaned"}):
        request_metadata.running = False
        request_metadata.cleaned = True
        issue.update_metadata()
        update_request_state(prod_id, "Done")
        print("Request is cleaned, validation will need to be resubmitted")
        return

    query = {"TransformationID": request_metadata.transform_ids}
    results = {}
    stats = returnValueOrRaise(TransformationClient().getTransformations(query, columns=["TransformationID", "Status"]))
    for stat in stats:
        results[stat.pop("TransformationID")] = stat | {"FileStatus": {}}
    file_stats = returnValueOrRaise(
        TransformationClient().getCounters("TransformationFiles", ["TransformationID", "Status"], query)
    )
    for meta, count in file_stats:
        results[meta["TransformationID"]]["FileStatus"][meta["Status"]] = count
    is_idle = all(
        x["Status"] == "Idle" and "Assigned" not in x["FileStatus"] and sum(x["FileStatus"].values()) > 0
        for x in results.values()
    )
    is_complete = all(set(x["FileStatus"]) == {"Processed"} for x in results.values())
    print(f"Request {prod_id}: {request_metadata.n_files_expected=} {is_idle=} {is_complete=}: {results}")
    if not is_idle:
        print("Validation is still running")
    elif is_complete:
        if request_metadata.n_files_expected != results[min(results)]["FileStatus"]["Processed"]:
            raise NotImplementedError()
        message = (
            """The validation is complete. Please check the results and update the ~"state::ready" when appropriate."""
        )
        issue.discussions.create({"body": message})
        issue.labels.pop(issue.labels.index("state::run-validation"))
        issue.labels.append("state::check-validation")
        request_metadata.running = False
        issue.update_metadata()
        print("Validation is complete")
    else:
        print("Something went wrong, please check the status of the transformations!")


def launch_reco(request_id: int, **kwargs):
    return _launch_inner(request_id, **kwargs, configure_steps=configure_steps_reco)


def launch_sprucing(request_id: int, **kwargs):
    return _launch_inner(request_id, **kwargs, configure_steps=configure_steps_spruce)


def _launch_inner(
    request_id: int,
    *,
    validation: bool,
    validation_runs: list[int] | None = None,
    start_run: int | None = None,
    end_run: int | None = None,
    append_name: str = "1",
    ancestor_depth: int = 0,
    configure_steps: callable,
):
    prods = returnValueOrRaise(ProductionRequestClient().getProductionRequest([request_id]))
    data = prods[request_id]
    n_files_expected = None

    pr = ProductionRequest()
    pr.requestID = str(request_id)
    pr.appendName = append_name
    pr.visibility = "Yes"
    kwargs = {} if validation else dict(startRun=start_run, endRun=end_run)
    configure_input(pr, data, **kwargs)
    pr.prodGroup = f"{pr.processingPass}/{json.loads(data['ProDetail'])['pDsc']}"
    pr.outConfigName = "validation" if validation else pr.configName
    if validation:
        bkQueryDict = pr._getBKKQuery().copy()
        if "RunNumbers" in bkQueryDict:
            bkQueryDict["RunNumbers"] = bkQueryDict["RunNumbers"].split(";;;")
        if "DataQualityFlag" in bkQueryDict:
            bkQueryDict["DataQualityFlag"] = bkQueryDict["DataQualityFlag"].split(";;;")
        if "ExtendedDQOK" in bkQueryDict:
            bkQueryDict["ExtendedDQOK"] = bkQueryDict["ExtendedDQOK"].split(";;;")
        all_runs = sorted(
            run
            for run in returnValueOrRaise(BookkeepingClient().getListOfRuns(bkQueryDict))
            if (start_run or 0) <= run <= (end_run or math.inf)
        )
        if validation_runs:
            runs = validation_runs
        else:
            # Run validations with the first run to ensure it will have been distributed
            # Originally we tried to use first + random + last run however when sites are
            # full the last run might not be distributed and the validation will be stuck.
            runs = [all_runs.pop(0)]
            runs = sorted(set(runs))
        print("Runs to be validated: ", runs)
        n_files_expected = 0
        for run in runs:
            result = returnValueOrRaise(BookkeepingClient().getFilesWithMetadata(bkQueryDict | {"RunNumbers": run}))
            if result["TotalRecords"] == 0:
                raise NotImplementedError(f"Run {run} has no files")
            print(f"Run {run} has {result['TotalRecords']} files")
            n_files_expected += result["TotalRecords"]
        pr.runsList = ",".join(runs_to_input_query(runs))
    configure_steps(pr, data, ancestor_depth)
    transform_ids = returnValueOrRaise(pr.buildAndLaunchRequest())
    return transform_ids, n_files_expected


def configure_steps_reco(pr, data, ancestor_depth):
    pd = json.loads(data["ProDetail"])
    steps = {int(k[1 : -len("Step")]): v for k, v in pd.items() if k.endswith("Step")}
    if len(steps) != 1:
        raise NotImplementedError("Only one step is supported at the moment")
    pr.stepsList = [int(v) for k, v in sorted(steps.items())]
    pr.prodsTypeList = ["DataReconstruction"]
    pr.stepsInProds = [list(range(1, len(pr.stepsList) + 1))]
    pr.targets = [""]
    pr.outputSEs = ["Tier1-DST"]
    pr.specialOutputSEs = [{}]
    pr.removeInputsFlags = [False]
    pr.priorities = [2]
    pr.inputs = [[]]
    pr.inputDataPolicies = ["download"]
    pr.multicore = ["True"]
    pr.outputModes = ["Run"]
    pr.targets = ["ALL"]
    pr.events = ["-1"]
    pr.ancestorDepths = [ancestor_depth]
    pr.compressionLvl = ["HIGH"]
    pr.plugins = ["RAWProcessing"]
    pr.groupSizes = [1]
    pr.cpus = [1_000_000]
    pr.outputVisFlag = [{"1": "Y"}]
    pr.specialOutputVisFlag = [{"1": {}}]


def configure_steps_spruce(pr, data, ancestor_depth):
    pd = json.loads(data["ProDetail"])
    steps = {int(k[1 : -len("Step")]): v for k, v in pd.items() if k.endswith("Step")}
    pr.stepsList = [int(v) for k, v in sorted(steps.items())]
    pr.prodsTypeList = ["Sprucing", "Merge"]
    pr.stepsInProds = [list(range(1, len(pr.stepsList))), [len(pr.stepsList)]]
    pr.targets = ["", ""]
    pr.outputSEs = ["Tier1-Buffer", "Tier1-DST"]
    pr.specialOutputSEs = [{}, {}]
    pr.removeInputsFlags = [False, True]
    pr.priorities = [2, 8]
    pr.inputs = [[], []]
    pr.inputDataPolicies = ["download", "download"]
    pr.multicore = ["True", "True"]
    pr.outputModes = ["Run", "Run"]
    pr.targets = ["ALL", "ALL"]
    pr.events = ["-1", "-1"]
    pr.ancestorDepths = [ancestor_depth, 0]
    pr.compressionLvl = ["LOW", "HIGH"]
    pr.plugins = ["Sprucing", "ByRunFileTypeSizeWithFlush"]
    pr.groupSizes = [1, 5]
    pr.cpus = [1_000_000, 300_000]
    pr.outputVisFlag = [{"1": "N"}, {"2": "Y"}]
    pr.specialOutputVisFlag = [{"1": {}}, {"2": {}}]
