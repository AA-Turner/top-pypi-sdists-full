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
import math
import sys
from collections import defaultdict
from datetime import datetime, timezone

from rich.table import Table
from rich.markdown import Markdown
from rich.prompt import Prompt

from DIRAC.Core.Utilities.ReturnValues import returnValueOrRaise
from LHCbDIRAC.TransformationSystem.Client.TransformationClient import TransformationClient

from .actions import (
    ExtendEndRunAction,
    SubmitProductionsAction,
    UpdateIssueStateLabel,
    CheckValidationAction,
    CleanValidationAction,
    CompleteTransformationAction,
    CloseIssueAction,
    AddLabelAction,
    UpdateTransformationStatusAction,
    UpdateRequestStateAction,
    SubmitRemovalTransformationAction,
)
from .integrations import EVENTTYPE_TO_STREAM

ACTIVE_PRODUCTION_STATES = {
    "run-validation",
    "ready",
    "running",
    "running-concurrent",
    "update-end-run",
    "checking",
    "debugging",
}
CHECK_DISPLAY = {None: "❔", True: "✅"}


def status_emoji(status):
    if status in {"Archived", "Completed"}:
        return ""
    if status in {"Cleaned", "Cleaning"}:
        return "🧹"
    if status in {"Active", "Idle"}:
        return "🏃"
    if status in {"Stopped"}:
        return "⏹️"
    return "❔"


def analyse_active_productions(repo, *, states: set[str] = ACTIVE_PRODUCTION_STATES):
    all_issues = repo.poll(states=states)
    actions = defaultdict(list)

    # Find validations that need to be submitted
    for issue in all_issues.get("run-validation", []):
        needs_submit = True
        for request_id, meta in issue.metadata.validations.items():
            if meta.running:
                actions[issue].append(CheckValidationAction(issue, request_id))
                needs_submit = False
        if needs_submit:
            actions[issue].append(SubmitProductionsAction(issue))

    # Find productions that need to be submitted
    for issue in all_issues.get("ready", []):
        for request_id, meta in issue.metadata.validations.items():
            if not meta.cleaned:
                actions[issue].append(CleanValidationAction(issue, request_id))
        actions[issue].append(SubmitProductionsAction(issue))

    issues_by_state = {k: v for k, v in all_issues.items() if k in states}
    # Find metadata for all relevant transformations
    all_tids = set()
    for state, issues in issues_by_state.items():
        for issue in issues:
            for request_id, request_meta in issue.metadata.requests.items():
                all_tids.update(request_meta.all_transform_ids)
    if all_tids:
        retVal = TransformationClient().getTransformations(
            {"TransformationID": list(all_tids)},
            columns=[
                "TransformationFamily",
                "TransformationID",
                "Type",
                "TransformationGroup",
                "CreationDate",
                "Status",
            ],
        )
        tinfo = {x["TransformationID"]: x for x in returnValueOrRaise(retVal)}
        input_queries = returnValueOrRaise(TransformationClient().getBookkeepingQueries(list(tinfo)))
    else:
        tinfo = {}
        input_queries = {}

    # Create the table data
    last_update = datetime.fromtimestamp(0, timezone.utc)
    tables_data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))
    for state, issues in issues_by_state.items():
        for issue in issues:
            last_update = max(last_update, issue.metadata.last_updated)
            for request_id, request_meta in issue.metadata.requests.items():
                main_tid, merge_tid = request_meta.transform_ids
                if tinfo[merge_tid]["Type"] != "Merge":
                    raise NotImplementedError(tinfo[merge_tid])
                input_query = input_queries[main_tid]
                proc_pass = tinfo[main_tid]["TransformationGroup"].split("/")[-1]
                row_data = [f"[link={issue.url}]#{issue.issue.iid}[/link]"]
                row_data += [request_id, state]
                row_data += [input_query["DataTakingConditions"]]
                row_data += [
                    f"{tid} {status_emoji(tinfo[tid]['Status'])}" if tid else "⚠️"
                    for tid in [main_tid, merge_tid, request_meta.removal, request_meta.replication]
                ]
                row_data += [f"{input_query['StartRun']}:{input_query['EndRun']}"]
                file_status = request_meta.file_status.get(main_tid, {})
                total = sum(file_status.values())
                row_data.append(total)
                row_data.append(file_status.get("Processed", 0))
                for status in ["MaxReset", "Problematic"]:
                    count = file_status.get(status, 0)
                    row_data.append(f"{count} 🚨" if count else 0)
                for file_status_tid in [main_tid, merge_tid, request_meta.removal]:
                    file_status = request_meta.file_status.get(file_status_tid, {})
                    total = sum(file_status.values())
                    row_data.append(
                        f"{math.floor(file_status.get('Processed', 0) / total * 100_00) / 100:.2f}%" if total else ""
                    )
                n_checks = 0
                n_checks_passed = 0
                for check_name in ["dm_check", "pm_check"]:
                    check_status = [getattr(request_meta.checks, check_name).get(x) for x in request_meta.transform_ids]
                    row_data.append(" ".join(CHECK_DISPLAY[x] for x in check_status))
                    n_checks += len(check_status)
                    n_checks_passed += sum(filter(None, check_status))
                req_cleaned = request_meta.checks.dm_clean.get(request_id)
                row_data.append(CHECK_DISPLAY[req_cleaned])
                n_checks += 1
                n_checks_passed += bool(req_cleaned)

                config = input_query["ConfigVersion"]
                event_type = input_query["EventType"]
                expected_labels = {f"config::{config}", f"proc::{proc_pass}", f"stream::{event_type}"}
                for label in expected_labels:
                    if label not in issue.labels:
                        actions[issue].append(AddLabelAction(repo, issue, label))

                tables_data[config][proc_pass][event_type][tinfo[main_tid]["Type"]].append(row_data)

                if state == "running":
                    if not request_meta.removal:
                        actions[issue].append(SubmitRemovalTransformationAction(issue, request_id))

                    all_finished = True
                    for tid in request_meta.transform_ids + [request_meta.removal]:
                        file_status = request_meta.file_status.get(tid, {})
                        total = sum(file_status.values())
                        finished = sum(
                            file_status.get(status, 0) for status in ["Processed", "NotProcessed", "Removed"]
                        )
                        if total == 0 or total != finished:
                            all_finished = False
                            continue
                        if tid not in tinfo:
                            print(f"Missing transformation {tid}, maybe a metadata refresh is needed?")
                            continue
                        match tinfo[tid]["Status"]:
                            case "Active":
                                all_finished = False
                            case "Idle":
                                actions[issue].append(UpdateTransformationStatusAction(tid, "Stopped"))
                    if all_finished:
                        actions[issue].append(UpdateIssueStateLabel(issue, "running", "checking"))

                if state == "checking" and n_checks == n_checks_passed:
                    actions[issue].append(CompleteTransformationAction(issue, main_tid))
                    actions[issue].append(CompleteTransformationAction(issue, merge_tid))
                    actions[issue].append(CompleteTransformationAction(issue, request_meta.removal))
                    actions[issue].append(UpdateRequestStateAction(request_id, "Done"))
                    actions[issue].append(UpdateIssueStateLabel(issue, "checking", "done"))
                    actions[issue].append(CloseIssueAction(issue))

                # Ensure the start run is sensible
                if input_queries.get(main_tid, {}).get("StartRun") != issue.run_yaml.get("start_run"):
                    raise NotImplementedError(f"Start run mismatch: {issue} {main_tid}")
                if (
                    request_meta.removal
                    and input_queries.get(request_meta.removal, {}).get("StartRun")
                    != input_queries[main_tid]["StartRun"]
                ):
                    raise NotImplementedError(f"Removal start run mismatch: {issue} {request_meta.removal}")

                # Check if the end run needs to be extended
                main_value = input_queries.get(main_tid, {}).get("EndRun")
                expected_value = issue.run_yaml.get("end_run")
                if main_value != expected_value:
                    if state != "update-end-run":
                        raise NotImplementedError(
                            f"End run mismatch: {issue} {main_tid} {main_value} != {expected_value}"
                        )
                    actions[issue].append(ExtendEndRunAction(issue, main_tid, expected_value))
                    if request_meta.removal is not None:
                        actions[issue].append(ExtendEndRunAction(issue, request_meta.removal, expected_value))
                    new_state = "running-concurrent" if issue.run_yaml["concurrent"] else "running"
                    actions[issue].append(UpdateIssueStateLabel(issue, "update-end-run", new_state))
                elif state == "update-end-run":
                    raise NotImplementedError(f"State is update-end-run there is nothing to change: {issue}")

                # Ensure the removal is consistent with the main transformation
                if request_meta.removal is not None:
                    removal_value = input_queries.get(request_meta.removal, {}).get("EndRun")
                    if removal_value != main_value:
                        raise NotImplementedError(
                            f"Removal end run mismatch: {issue} {request_meta.removal} {removal_value} != {main_value}"
                        )

    return last_update, tables_data, actions


def display_table(console, tables_data):
    # Create the rich tables from the table data
    tables = defaultdict(list)
    for config in sorted(tables_data):
        for proc_pass in sorted(tables_data[config]):
            section = f"# {config} {proc_pass}"
            for eventtype in sorted(tables_data[config][proc_pass]):
                for tran_type, table_rows in sorted(tables_data[config][proc_pass][eventtype].items()):
                    table = Table(
                        *["Issue", "Request", "State", "Conditions", tran_type, "Merging", "Removal", "Replication"],
                        *["Runs", "RAWs", "Processed", "MaxReset", "Problematic", "% Done", "(merge)", "(removal)"],
                        *["DM Check", "PM Check", "DM Clean"],
                        row_styles=["dim", ""],
                        title=f"[bold]{eventtype} ({EVENTTYPE_TO_STREAM.get(eventtype)})",
                    )
                    for row in sorted(table_rows, key=lambda x: x[4]):
                        table.add_row(*map(str, row))
                    tables[section].append(table)

    # Make the columns the same width across all tables
    for cols in zip(*(x.columns for section_tables in tables.values() for x in section_tables)):
        width = max(console.measure(cell).maximum for col in cols for cell in col.cells)
        width = max(width, len(cols[0].header))
        for col in cols:
            col.width = width
    # Display the tables
    for section, tables in tables.items():
        console.print(Markdown(section))
        for table in tables:
            console.print(table)


def display_actions(console, actions, *, execute=False):
    console.print(Markdown("# Recommended Actions"))
    for issue, action_list in actions.items():
        lines = [f"## {issue.url} ({issue.state})\n"]

        automatic_actions = []
        prompted_actions = []
        for action in action_list:
            if action.safe:
                automatic_actions.append(action)
            else:
                prompted_actions.append(action)

        if automatic_actions:
            lines.append("\nAutomatic actions:\n")
            lines.extend(f"- {action.message()}" for action in automatic_actions)

        if prompted_actions:
            lines.append("\nManual actions:\n")
            lines.extend(f"- {action.message()}" for action in prompted_actions)

        console.print(Markdown("\n".join(lines)))

        if not execute:
            continue

        for action in automatic_actions:
            action.run()

        if not prompted_actions:
            continue

        match response := Prompt.ask(
            "Do you want to run these manual actions?", choices=["run-all", "ask-each", "no", "quit"], default="no"
        ):
            case "run-all":
                for action in prompted_actions:
                    action.run()
            case "ask-each":
                for action in prompted_actions:
                    if Prompt.ask(f"Run the action: {action.message()}?", choices=["yes", "no"]) == "yes":
                        action.run()
            case "no":
                continue
            case "quit":
                sys.exit(0)
            case _:
                raise NotImplementedError(f"Invalid response: {response}")
