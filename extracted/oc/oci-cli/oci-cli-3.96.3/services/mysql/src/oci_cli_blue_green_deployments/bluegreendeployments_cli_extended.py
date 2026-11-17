# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

import click  # noqa: F401
import json  # noqa: F401
from services.mysql.src.oci_cli_blue_green_deployments.generated import bluegreendeployments_cli
from oci_cli import cli_util  # noqa: F401
from oci_cli import custom_types  # noqa: F401
from oci_cli import json_skeleton_utils  # noqa: F401


bluegreendeployments_cli.blue_green_deployments_root_group.help = bluegreendeployments_cli.blue_green_deployment_group.help
bluegreendeployments_cli.blue_green_deployments_root_group.short_help = "Manage blue/green deployments."


# oci mysql blue-green-deployments blue-green-deployment-collection list-blue-green-deployments -> oci mysql blue-green-deployments blue-green-deployment-collection list
cli_util.rename_command(bluegreendeployments_cli, bluegreendeployments_cli.blue_green_deployment_collection_group, bluegreendeployments_cli.list_blue_green_deployments, "list")


# Remove blue-green-deployment-collection from oci mysql blue-green-deployments
bluegreendeployments_cli.blue_green_deployments_root_group.commands.pop(bluegreendeployments_cli.blue_green_deployment_collection_group.name)


# oci mysql blue-green-deployments blue-green-deployment-collection list-blue-green-deployments -> oci mysql blue-green-deployments
bluegreendeployments_cli.blue_green_deployment_collection_group.commands.pop(bluegreendeployments_cli.list_blue_green_deployments.name)
bluegreendeployments_cli.blue_green_deployments_root_group.add_command(bluegreendeployments_cli.list_blue_green_deployments)


# Move commands under 'oci mysql blue-green-deployments blue-green-deployment' -> 'oci mysql blue-green-deployments'
bluegreendeployments_cli.blue_green_deployments_root_group.commands.pop(bluegreendeployments_cli.blue_green_deployment_group.name)
bluegreendeployments_cli.blue_green_deployments_root_group.add_command(bluegreendeployments_cli.change_blue_green_deployment_compartment)
bluegreendeployments_cli.blue_green_deployments_root_group.add_command(bluegreendeployments_cli.create_blue_green_deployment)
bluegreendeployments_cli.blue_green_deployments_root_group.add_command(bluegreendeployments_cli.delete_blue_green_deployment)
bluegreendeployments_cli.blue_green_deployments_root_group.add_command(bluegreendeployments_cli.get_blue_green_deployment)
bluegreendeployments_cli.blue_green_deployments_root_group.add_command(bluegreendeployments_cli.switchover_blue_green_deployment)
bluegreendeployments_cli.blue_green_deployments_root_group.add_command(bluegreendeployments_cli.update_blue_green_deployment)
