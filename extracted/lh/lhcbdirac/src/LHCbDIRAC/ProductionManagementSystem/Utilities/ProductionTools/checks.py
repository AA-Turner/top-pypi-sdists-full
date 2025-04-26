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

import shlex
import sys
import time
from asyncio.subprocess import create_subprocess_exec, PIPE, STDOUT
from tempfile import NamedTemporaryFile

from rich.markdown import Markdown
from rich.prompt import Prompt
from DIRAC.Core.Utilities.ReturnValues import returnValueOrRaise

from .integrations import RepoIssue


async def do_checks(console, logbook, repo, request_ids):
    while True:
        choice = ask("Which request would you like to check?", choices=request_ids)
        issue_iid = int(request_ids[choice].split("#")[1].split("[")[0])
        request_id = int(choice)

        issue = RepoIssue(repo.get_issue(issue_iid))
        request_metadata = issue.metadata.requests[request_id]
        choice = ask("Which transformation would you like to check?", choices=request_metadata.transform_ids + ["all"])
        choice = request_metadata.transform_ids if choice == "all" else [int(choice)]
        for transform_id in choice:
            console.rule(f"Checking transformation {transform_id}")

            console.rule()
            choice = ask("Would you like to run the PM checks?", choices=["yes", "no"], default="yes")
            if choice == "yes":
                await pm_checks(console, logbook, issue, request_id, transform_id)
            else:
                console.print("Skipping PM checks")

            console.rule()
            choice = ask("Would you like to run the DM checks?", choices=["yes", "no"], default="yes")
            if choice == "yes":
                await dm_checks(console, logbook, issue, request_id, transform_id)
            else:
                console.print("Skipping DM checks")

        console.rule()
        choice = ask("Would you like to check if the buffer has been cleaned?", choices=["yes", "no"], default="yes")
        if choice == "yes":
            await buffer_check_removal(console, logbook, issue, request_id)
        else:
            console.print("Skipping buffer check")


async def pm_checks(console, logbook, issue, request_id, transform_id):
    console.print(f"Running PM checks for request {request_id} transformation {transform_id} ({issue.url})")
    cmd = ["dirac-production-check-descendants", str(transform_id), "--Force"]
    output = await run_command(cmd, console)

    choice = ask("Would you like to mark check as successful?", choices=["yes", "no"])
    if choice == "yes":
        issue.metadata.requests[request_id].checks.pm_check[transform_id] = True
        issue.update_metadata()
    maybe_post_logbook(
        console, logbook, issue.url, transform_id, choice == "yes", [(cmd, output)], ["Sprucing", "Production"]
    )


async def dm_checks(console, logbook, issue, request_id, transform_id):
    console.print(f"Running DM checks for request {request_id} transformation {transform_id} ({issue.url})")

    cmd = ["dirac-dms-check-fc2bkk", "--Production", transform_id]
    output = await run_command(cmd, console)

    cmd2 = ["dirac-dms-check-bkk2fc", "--Production", transform_id]
    output2 = await run_command(cmd2, console)

    choice = ask("Would you like to mark check as successful?", choices=["yes", "no"])
    if choice == "yes":
        issue.metadata.requests[request_id].checks.dm_check[transform_id] = True
        issue.update_metadata()
    maybe_post_logbook(
        console,
        logbook,
        issue.url,
        transform_id,
        choice == "yes",
        [(cmd, output), (cmd2, output2)],
        ["Sprucing", "Data Management", "Production"],
    )


async def run_command(cmd, console):
    cmd = list(map(str, cmd))
    console.rule()
    console.print(f"[bold]Output from:[/bold] {shlex.join(cmd)}")
    spinner = console.status(f"[bold]Running command:[/bold] {shlex.join(cmd)}", spinner="bouncingBall")
    start = time.monotonic()
    spinner.start()

    proc = await create_subprocess_exec(*cmd, stdout=PIPE, stderr=STDOUT)
    output = ""
    while line := await proc.stdout.readline():
        line = line.decode()
        output += line
        console.print(line, end="")
    await proc.communicate()
    spinner.stop()
    end = time.monotonic()
    console.print(f"[bold]Command finished with return code {proc.returncode} in {end - start:.2f}s[/bold]")
    console.rule()
    return output


def maybe_post_logbook(console, logbook, url, transform_id, success, cmds, systems):
    body = []
    if success:
        subject = "Checks successful"
        body.append("Checks have been successfully completed.")
    else:
        subject = "Checks failed"
        body.append("Checks were ran.")
    for cmd, output in cmds:
        body.append("")
        if cmd is not None:
            body.append("Command: " + shlex.join(map(str, cmd)))
            body.append("")
        body.append("Output:")
        body.append("```")
        body.append(output)
        body.append("```")

    body = "\n".join(body)

    console.print(Markdown(f"### Subject: {subject}\n\n{body}"))

    choice = ask("Would you like to make the above logbook entry?", choices=["yes", "no"])
    if choice == "yes":
        logbook.create_post(url, [transform_id], subject, body, {}, systems)


async def buffer_check_removal(console, logbook, issue, request_id):
    from LHCbDIRAC.TransformationSystem.Client.TransformationClient import TransformationClient
    from LHCbDIRAC.ProductionManagementSystem.Utilities.ProductionTools.integrations import get_file_status

    transform_id = issue.metadata.requests[request_id].transform_ids[0]
    removal_id = issue.metadata.requests[request_id].removal

    body = []
    cmd_out = []
    spruce_file_status = {k["Status"]: v for k, v in await get_file_status(transform_id)}
    body.append(f"File statuses for first transformation {transform_id}: {spruce_file_status}")
    removal_file_status = {k["Status"]: v for k, v in await get_file_status(removal_id)}
    body.append(f"File statuses for removal transformation {removal_id}: {removal_file_status}")
    if not set(spruce_file_status).issubset({"Processed", "NotProcessed", "Removed"}):
        raise NotImplementedError()
    if not set(removal_file_status).issubset({"Processed", "Unused"}):
        raise NotImplementedError()
    not_processed_lfns = {
        x["LFN"]
        for x in returnValueOrRaise(
            TransformationClient().getTransformationFiles(
                {"TransformationID": transform_id, "Status": "NotProcessed"}, columns=["LFN"]
            )
        )
    }
    unused_lfns = {
        x["LFN"]
        for x in returnValueOrRaise(
            TransformationClient().getTransformationFiles(
                {"TransformationID": removal_id, "Status": "Unused"}, columns=["LFN"]
            )
        )
    }
    if lfns_to_clean := not_processed_lfns.intersection(unused_lfns):
        body.append(f"* {len(lfns_to_clean)} LFNs which are Unused due to being set NotProcessed:")
        body += lfns_to_clean
    if lfns := not_processed_lfns - unused_lfns:
        raise NotImplementedError(lfns)
    if lfns := unused_lfns - not_processed_lfns:
        raise NotImplementedError(lfns)
    body = "\n".join(body)
    cmd_out = [(None, body)]
    console.print(body)

    if lfns_to_clean:
        choice = ask(f"Would you like to remove {len(lfns_to_clean)} LFNs from the buffers?", choices=["yes", "no"])
        if choice == "yes":
            with NamedTemporaryFile("wt") as f:
                f.write("\n".join(lfns))
                f.flush()
                cmd = ["dirac-dms-remove-replicas", "--SE", "Tier1-Buffer", f"--File={f.name}"]
                output = await run_command(cmd, console)
                cmd_out.append((cmd, output))

    choice = ask("Would you like to mark check as successful?", choices=["yes", "no"])
    if choice == "yes":
        issue.metadata.requests[request_id].checks.dm_clean[request_id] = True
        issue.update_metadata()
    maybe_post_logbook(
        console,
        logbook,
        issue.url,
        transform_id,
        choice == "yes",
        cmd_out,
        ["Sprucing", "Data Management", "Production"],
    )


def ask(question, choices, **kwargs):
    choices = sorted(str(choices) for choices in choices)
    choice = Prompt.ask(question, choices=choices + ["quit"], **kwargs)
    if choice == "quit":
        sys.exit(0)
    return choice
