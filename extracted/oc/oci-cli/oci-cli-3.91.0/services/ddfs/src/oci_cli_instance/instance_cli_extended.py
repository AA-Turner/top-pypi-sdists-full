# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

import click  # noqa: F401
import json  # noqa: F401
from services.ddfs.src.oci_cli_instance.generated import instance_cli
from oci_cli import cli_util  # noqa: F401
from oci_cli import custom_types  # noqa: F401
from oci_cli import json_skeleton_utils  # noqa: F401


# oci ddfs instance-collection list-instances -> oci ddfs instance-collection list
cli_util.rename_command(instance_cli, instance_cli.instance_collection_group, instance_cli.list_instances, "list")


# Move commands under 'oci ddfs instance-collection' -> 'oci ddfs instance'
instance_cli.ddfs_root_group.commands.pop(instance_cli.instance_collection_group.name)
instance_cli.instance_group.add_command(instance_cli.list_instances)


# oci ddfs work-request-log-entry list-work-request-logs -> oci ddfs work-request-log-entry list
cli_util.rename_command(instance_cli, instance_cli.work_request_log_entry_group, instance_cli.list_work_request_logs, "list")


# oci ddfs work-request-log-entry -> oci ddfs work-request-log
cli_util.rename_command(instance_cli, instance_cli.ddfs_root_group, instance_cli.work_request_log_entry_group, "work-request-log")
