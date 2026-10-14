# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

import click  # noqa: F401
import json  # noqa: F401
from services.mysql.src.oci_cli_mysql.generated import mysql_service_cli
from services.mysql.src.oci_cli_blue_green_deployments.generated import bluegreendeployments_cli
from oci_cli import cli_util  # noqa: F401
from oci_cli import custom_types  # noqa: F401
from oci_cli import json_skeleton_utils  # noqa: F401


# oci mysql blue-green-deployments -> oci mysql blue-green-deployment
cli_util.rename_command(mysql_service_cli, mysql_service_cli.mysql_service_group, bluegreendeployments_cli.blue_green_deployments_root_group, "blue-green-deployment")
