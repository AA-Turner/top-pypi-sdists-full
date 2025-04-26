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
import argparse
import asyncio

import DIRAC
from DIRAC.Core.Security.Properties import PRODUCTION_MANAGEMENT
from rich.console import Console
from rich.prompt import Prompt


def main():
    parser = argparse.ArgumentParser(description="Manage LHCbDIRAC production requests")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparser = subparsers.add_parser("show-requests", help="Show the current status of the production requests")
    subparser.set_defaults(func=show_requests)
    subparser.add_argument("--execute-actions", action="store_true", help="Execute the actions")

    subparser = subparsers.add_parser("update-metadata", help="Update the metadata stored on GitLab")
    subparser.set_defaults(func=update_metadata)

    subparser = subparsers.add_parser("run-checks", help="Run checks on the production requests")
    subparser.set_defaults(func=run_checks)

    args = parser.parse_args()
    args.func(args)


def show_requests(args):
    DIRAC.initialize()
    from LHCbDIRAC.ProductionManagementSystem.Utilities.ProductionTools import ProdRequestsGitlabRepo
    from LHCbDIRAC.ProductionManagementSystem.Utilities.ProductionTools.monitoring import (
        analyse_active_productions,
        display_table,
        display_actions,
    )

    if args.execute_actions:
        DIRAC.initialize(security_expression=PRODUCTION_MANAGEMENT)
        match Prompt.ask("Update metadata?", choices=["yes", "no"], default="yes"):
            case "yes":
                update_metadata(args)

    repo = ProdRequestsGitlabRepo(with_auth=args.execute_actions)
    last_update, tables_data, actions = analyse_active_productions(repo)
    console = Console()
    console.rule()
    display_table(console, tables_data)
    console.print(f"Last update: {last_update}")
    console.rule()
    display_actions(console, actions, execute=args.execute_actions)


def update_metadata(args):
    DIRAC.initialize(security_expression=PRODUCTION_MANAGEMENT)
    from LHCbDIRAC.ProductionManagementSystem.Utilities.ProductionTools import ProdRequestsGitlabRepo
    from LHCbDIRAC.ProductionManagementSystem.Utilities.ProductionTools.monitoring import ACTIVE_PRODUCTION_STATES

    repo = ProdRequestsGitlabRepo(with_auth=True)
    repo.poll(do_status_update=True, states=ACTIVE_PRODUCTION_STATES)


def run_checks(args):
    DIRAC.initialize(security_expression=PRODUCTION_MANAGEMENT)
    from LHCbDIRAC.ProductionManagementSystem.Utilities.ProductionTools import (
        ProdRequestsGitlabRepo,
        OperationsLogbook,
        do_checks,
    )
    from LHCbDIRAC.ProductionManagementSystem.Utilities.ProductionTools.monitoring import (
        analyse_active_productions,
        display_table,
    )

    repo = ProdRequestsGitlabRepo(with_auth=True)
    logbook = OperationsLogbook()
    last_update, tables_data, _ = analyse_active_productions(repo, states=["checking"])

    console = Console()
    console.rule()
    display_table(console, tables_data)
    console.print(f"Last update: {last_update}")
    console.rule()

    request_ids = {
        str(x[1]): x[0]
        for v in tables_data.values()
        for vv in v.values()
        for vvv in vv.values()
        for vvvv in vvv.values()
        for x in vvvv
    }

    asyncio.run(do_checks(console, logbook, repo, request_ids))


if __name__ == "__main__":
    main()
