# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.
# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20220901

from oci_cli.cli_root import cli
from oci_cli import cli_util
from oci_cli.aliasing import CommandGroupWithAlias


@cli.command(cli_util.override('work_request.os_management_hub_service_group.command_name', 'os-management-hub'), cls=CommandGroupWithAlias, help=cli_util.override('work_request.os_management_hub_service_group.help', """Use the OS Management Hub API to manage and monitor updates and patches for instances in OCI, your private data center, or 3rd-party clouds.
For more information, see [Overview of OS Management Hub]."""), short_help=cli_util.override('work_request.os_management_hub_service_group.short_help', """OS Management Hub API"""))
@cli_util.help_option_group
def os_management_hub_service_group():
    pass
