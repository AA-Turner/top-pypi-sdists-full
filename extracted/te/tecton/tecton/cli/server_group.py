import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List
from typing import Optional

import click
from google.protobuf.json_format import MessageToJson
from texttable import Texttable

from tecton import tecton_context
from tecton._internals import metadata_service
from tecton.cli import printer
from tecton.cli.cli_utils import display_table
from tecton.cli.cli_utils import timestamp_to_string
from tecton.cli.command import TectonGroup
from tecton_proto.common.server_group_status__client_pb2 import ServerGroupStatus
from tecton_proto.common.server_group_type__client_pb2 import ServerGroupType
from tecton_proto.servergroupservice.server_group_service__client_pb2 import GetServerGroupRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import ListServerGroupsRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import ServerGroupInfo


logger = logging.getLogger(__name__)

ERROR_MESSAGE_PREFIX = "⛔ ERROR: "
CHECK_MARK = "✅"
ERROR_SIGN = "⛔"
INFO_SIGN = "💡"


@dataclass
class ServerGroupIdentifier:
    id: Optional[str]
    name: Optional[str]

    def __post_init__(self):
        if not self.id and not self.name:
            printer.safe_print(
                f"{ERROR_MESSAGE_PREFIX} At least one of `id` or `name` must be provided", file=sys.stderr
            )
            sys.exit(1)

    def __str__(self):
        if self.id:
            return f"id: {self.id}"
        elif self.name:
            return f"name: {self.name}"
        else:
            return "No name or id set"

    def __eq__(self, identifier):
        if isinstance(identifier, ServerGroupIdentifier):
            if self.id:
                return self.id == identifier.id
            elif self.name:
                return self.name == identifier.name
        return False


@click.command("server-group", cls=TectonGroup)
def server_group():
    """Manage Server Groups for Online Serving and Realtime Execution."""


@server_group.command("list")
def list():
    """List all available Server Groups in workspace"""
    workspace = tecton_context.get_current_workspace()
    server_groups = _list_server_groups(workspace)
    _display_server_groups(server_groups)


@server_group.command("describe")
@click.option("-n", "--name", help="Name of the Server Group", required=True, type=str)
@click.option(
    "-o",
    "--output-file",
    help="JSON Output file to write Server Group Information to. If not specified, the Server Group information will be printed to stdout",
    required=False,
    type=click.Path(exists=False),
)
def describe(name: str, output_file: Optional[str] = None):
    """Describe a Server Group"""
    workspace = tecton_context.get_current_workspace()
    group = _get_server_group(workspace, name)
    if output_file:
        output_path = Path(output_file)
        _write_to_json(group, output_path)
    else:
        _display_server_group_info(group)


def _list_server_groups(workspace: str, type: ServerGroupType = None):
    try:
        req = ListServerGroupsRequest(workspace=workspace)
        if type:
            req.type = type
        response = metadata_service.instance().ListServerGroups(req)
        return response.server_groups

    except Exception as e:
        printer.safe_print(f"{ERROR_MESSAGE_PREFIX} Failed to fetch Server Groups: {e}", file=sys.stderr)
        sys.exit(1)


def _display_server_groups(server_groups: List[ServerGroupInfo], type_filter: ServerGroupType = None):
    headings = [
        "Id",
        "Name",
        "Type",
        "Status",
        "Environment",
        "Description",
        "Created At",
        "Owner",
        "Last Modified By",
    ]
    if type_filter and type_filter == ServerGroupType.SERVER_GROUP_TYPE_TRANSFORM_SERVER_GROUP:
        headings.append("Environment")
    display_table(
        headings,
        [
            (
                group.server_group_id,
                group.name,
                ServerGroupType.Name(group.type).split("SERVER_GROUP_TYPE_")[-1],
                ServerGroupStatus.Name(group.status).split("SERVER_GROUP_STATUS_")[-1],
                group.environment or "None"
                if group.type is ServerGroupType.SERVER_GROUP_TYPE_TRANSFORM_SERVER_GROUP
                else "N/A",
                group.description or "None",
                timestamp_to_string(group.created_at),
                group.owner,
                group.last_modified_by,
            )
            for group in server_groups
        ],
    )


def _get_server_group(workspace: str, server_group_name: str) -> ServerGroupInfo:
    try:
        req = GetServerGroupRequest(workspace=workspace, server_group_name=server_group_name)
        response = metadata_service.instance().GetServerGroup(req)
        return response.server_group

    except Exception as e:
        printer.safe_print(f"{ERROR_MESSAGE_PREFIX} Failed to fetch Server Groups: {e}", file=sys.stderr)
        sys.exit(1)


def _display_server_group_info(group: ServerGroupInfo):
    def _display_table(headings, rows):
        table = Texttable()
        table.header(headings)
        table.add_rows(rows, header=False)
        print(table.draw())
        print()

    def print_section_header(title):
        print("\n" + "=" * len(title))
        print(title.upper())
        print("=" * len(title))

    # Server Group Details
    print_section_header("Server Group Details")
    details = [
        ("ID", group.server_group_id),
        ("Name", group.name),
        ("Type", ServerGroupType.Name(group.type).split("SERVER_GROUP_TYPE_")[-1]),
        ("Status", ServerGroupStatus.Name(group.status).split("SERVER_GROUP_STATUS_")[-1]),
        ("Status Details", group.status_details or "N/A"),
        ("Created At", timestamp_to_string(group.created_at)),
        ("Description", group.description or "N/A"),
        ("Owner", group.owner or "N/A"),
        ("Last Modified By", group.last_modified_by),
    ]
    if group.type == ServerGroupType.SERVER_GROUP_TYPE_TRANSFORM_SERVER_GROUP:
        details.append(("Environment", group.environment))

    _display_table(["Field", "Value"], details)

    # Scaling Configurations
    desired_autoscaling_enabled = group.desired_config.autoscaling_enabled
    current_autoscaling_enabled = group.current_config.autoscaling_enabled

    scaling_config = [
        (
            "Autoscaling Enabled",
            bool_to_string(desired_autoscaling_enabled),
            bool_to_string(current_autoscaling_enabled),
        ),
        (
            "Min Nodes\n(Autoscaling Config)",
            "N/A" if not desired_autoscaling_enabled else group.desired_config.min_nodes,
            "N/A" if not current_autoscaling_enabled else group.current_config.min_nodes,
        ),
        (
            "Max Nodes\n(Autoscaling Config)",
            "N/A" if not desired_autoscaling_enabled else group.desired_config.max_nodes,
            "N/A" if not current_autoscaling_enabled else group.current_config.max_nodes,
        ),
        (
            "Desired Nodes\n(Provisioned Config)",
            "N/A" if desired_autoscaling_enabled else group.desired_config.desired_nodes,
            "N/A" if current_autoscaling_enabled else group.current_config.desired_nodes,
        ),
        (
            "Last Updated At",
            timestamp_to_string(group.desired_config.last_updated_at),
            timestamp_to_string(group.current_config.last_updated_at),
        ),
    ]

    print_section_header("Scaling Configurations")
    _display_table(["Field", "Target Configuration", "Active Configuration"], scaling_config)


def bool_to_string(value):
    return "True" if bool(value) else "False"


def _write_to_json(server_group_info: ServerGroupInfo, output_path: Path):
    server_group_json = MessageToJson(server_group_info)
    with output_path.open("w") as f:
        f.write(server_group_json)
