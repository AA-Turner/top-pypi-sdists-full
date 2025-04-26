import json
import sys
from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import Set
from typing import Tuple

import click

from tecton._internals import metadata_service
from tecton._internals.display import Displayable
from tecton.cli import printer
from tecton.cli.command import TectonGroup
from tecton_core.errors import TectonAPIValidationError
from tecton_proto.auth.authorization_service__client_pb2 import Assignment
from tecton_proto.auth.authorization_service__client_pb2 import AssignRolesRequest
from tecton_proto.auth.authorization_service__client_pb2 import GetRolesRequest
from tecton_proto.auth.authorization_service__client_pb2 import ListAssignedPrincipalsRequest
from tecton_proto.auth.authorization_service__client_pb2 import ListAssignedRolesRequest
from tecton_proto.auth.authorization_service__client_pb2 import ListAssignedRolesResponse
from tecton_proto.auth.authorization_service__client_pb2 import UnassignRolesRequest
from tecton_proto.auth.principal__client_pb2 import PrincipalType
from tecton_proto.auth.resource__client_pb2 import ResourceType
from tecton_proto.auth.resource_role_assignments__client_pb2 import RoleAssignmentType
from tecton_proto.metadataservice.metadata_service__client_pb2 import GetUserRequest


RESOURCE_TYPES = {
    "workspace": ResourceType.RESOURCE_TYPE_WORKSPACE,
    "organization": ResourceType.RESOURCE_TYPE_ORGANIZATION,
    "secret-scope": ResourceType.RESOURCE_TYPE_SECRET_SCOPE,
}


def _get_role_definitions():
    request = GetRolesRequest()
    response = metadata_service.instance().GetRoles(request)
    return response.roles


@click.command("access-control", cls=TectonGroup)
def access_control():
    """Manage Access Controls."""


@access_control.command("assign-role")
@click.option(
    "-w", "--workspace", required=False, help="Assign role to a specific workspace (default is current workspace)"
)
@click.option("--all-workspaces", required=False, is_flag=True, help="Assign role to all workspaces")
@click.option("-c", "--secret-scope", required=False, help="Assign role to a specific secret scope")
# we can't make the role help dynamic without making top level usage of the CLI make a network request
# since even lazy loading following https://github.com/pallets/click/pull/2348 doesn't work for help text
@click.option(
    "-r", "--role", required=True, type=str, help="Role name (e.g. admin, owner, editor, consumer, viewer, etc)"
)
@click.option("-u", "--user", default=None, help="User Email")
@click.option("-s", "--service-account", default=None, help="Service Account ID")
@click.option("-g", "--principal-group", default=None, help="Principal Group ID")
@click.option("-f", "--file", default=None, help="Newline separated list of user emails.", type=click.File("r"))
def assign_role_command(workspace, all_workspaces, secret_scope, role, user, service_account, principal_group, file):
    """Assign a role to a principal."""
    workspace_resource, workspace_principal = _validate_assign_unassign_input(
        workspace, all_workspaces, secret_scope, user, service_account, principal_group, file
    )

    if file is not None:
        if user or service_account or principal_group:
            msg = "Please use exactly one of: --user, --service-account, --principal-group, or --file"
            raise click.ClickException(msg)
        _bulk_update_user_role(workspace_resource, all_workspaces, secret_scope, file, role)
    else:
        _update_role(
            workspace_resource,
            all_workspaces,
            secret_scope,
            role,
            user,
            service_account,
            principal_group,
            workspace_principal,
        )


@access_control.command()
@click.option(
    "-w", "--workspace", required=False, help="Unassign role to a specific workspace (default is current workspace)"
)
@click.option("--all-workspaces", required=False, is_flag=True, help="Unassign role to all workspaces")
@click.option("-c", "--secret-scope", required=False, help="Assign role to a specific secret scope")
# we can't make the role help dynamic without making top level usage of the CLI make a network request
# since even lazy loading following https://github.com/pallets/click/pull/2348 doesn't work for help text
@click.option(
    "-r", "--role", required=True, type=str, help="Role name (e.g. admin, owner, editor, consumer, viewer, etc)"
)
@click.option("-u", "--user", default=None, help="User Email")
@click.option("-s", "--service-account", default=None, help="Service Account ID")
@click.option("-g", "--principal-group", default=None, help="Principal Group ID")
def unassign_role(workspace, all_workspaces, secret_scope, role, user, service_account, principal_group):
    """Unassign a role from a principal."""
    workspace_resource, workspace_principal = _validate_assign_unassign_input(
        workspace, all_workspaces, secret_scope, user, service_account, principal_group, None
    )

    _update_role(
        workspace_resource,
        all_workspaces,
        secret_scope,
        role,
        user,
        service_account,
        principal_group,
        workspace_principal,
        unassign=True,
    )


def _validate_assign_unassign_input(
    workspace, all_workspaces, secret_scope, user, service_account, principal_group, file
) -> Tuple[Optional[str], Optional[str]]:
    """
    Validate input parameters to assign-role/unassign-role.
    Also mutate 1 parameter workspace into either workspace_resource or workspace_principal.

    :return: pair of workspace_resource, workspace_principal
    """
    if all_workspaces and (workspace or secret_scope):
        msg = "The --all_workspaces flag cannot be used with --workspace or --secret_scope. Please assign roles separately."
        raise click.ClickException(msg)
        # --workspace and --secret_scope can be used together when workspace is the principal
    if workspace and secret_scope:
        workspace_principal = workspace
        workspace_resource = None
        if user or service_account or principal_group or file:
            msg = (
                "When using --secret-scope and --workspace to grant a workspace access to a secret scope, other principal flags "
                "--user, --service-account, --principal-group, --file must be removed."
            )
            raise click.ClickException(msg)
    else:
        workspace_principal = None
        workspace_resource = workspace
    return (workspace_resource, workspace_principal)


def _update_role(
    workspace_resource,
    all_workspaces,
    secret_scope,
    role,
    user,
    service_account,
    principal_group,
    workspace_principal,
    unassign=False,
):
    role = role.lower()
    assignment = Assignment()
    principal_type, principal_id = get_principal_details(user, service_account, principal_group, workspace_principal)

    if role == "admin":
        if all_workspaces or workspace_resource or secret_scope:
            msg = (
                "'Admin' is a cluster-wide role. Please remove --workspace, --all-workspace, and --secret-scope options"
            )
            raise click.ClickException(msg)
        resource_type = ResourceType.RESOURCE_TYPE_ORGANIZATION
    elif all_workspaces:
        resource_type = ResourceType.RESOURCE_TYPE_ORGANIZATION
    elif workspace_resource:
        resource_type = ResourceType.RESOURCE_TYPE_WORKSPACE
        assignment.resource_id = workspace_resource
    elif secret_scope:
        resource_type = ResourceType.RESOURCE_TYPE_SECRET_SCOPE
        assignment.resource_id = secret_scope
    else:
        msg = "Must specify either --workspace, --all-workspaces, or --secret-scope"
        raise click.ClickException(msg)

    role_defs = _get_role_definitions()
    if resource_type == ResourceType.RESOURCE_TYPE_SECRET_SCOPE and not any(
        ResourceType.RESOURCE_TYPE_SECRET_SCOPE in r.assignable_on_resource_types for r in role_defs
    ):
        msg = (
            "Tecton Secrets is not enabled on your cluster. "
            + "Currently, Secrets is only available on the Rift platform. Please contact Tecton Support for more assistance."
        )
        raise click.ClickException(msg)
    role_def = next(
        (r for r in role_defs if r.id == role and _is_role_assignable(r, principal_type, resource_type)), None
    )
    if role_def is None:
        msg = f"Invalid role. Possible values are: {', '.join(r.id for r in role_defs if _is_role_assignable(r, principal_type, resource_type))}"
        raise click.ClickException(msg)

    assignment.resource_type = resource_type
    assignment.principal_type = principal_type
    assignment.principal_id = principal_id
    assignment.role = role_def.legacy_id
    if user is not None:
        human_readable_principal_name = user
    elif service_account is not None:
        human_readable_principal_name = service_account
    elif principal_group is not None:
        human_readable_principal_name = principal_group
    else:
        human_readable_principal_name = workspace_principal
    try:
        if unassign:
            request = UnassignRolesRequest()
            request.assignments.append(assignment)
            metadata_service.instance().UnassignRoles(request)
        else:
            request = AssignRolesRequest()
            request.assignments.append(assignment)
            metadata_service.instance().AssignRoles(request)
        printer.safe_print(f"Successfully updated role for [{human_readable_principal_name}]")
    except Exception as e:
        printer.safe_print(f"Failed to update role for [{human_readable_principal_name}]: {e}", file=sys.stderr)
        sys.exit(1)


def _bulk_update_user_role(workspace, all_workspaces, secret_scope, file, role):
    for user in [line.strip() for line in file.readlines() if len(line.strip()) > 0]:
        _update_role(
            workspace,
            all_workspaces,
            secret_scope,
            role,
            user,
            service_account=None,
            principal_group=None,
            workspace_principal=None,
        )


def _is_role_assignable(role_def, principal_type, resource_type):
    return (
        principal_type in role_def.assignable_to_principal_types
        and resource_type in role_def.assignable_on_resource_types
    )


def get_roles(principal_type, principal_id, resource_type):
    request = ListAssignedRolesRequest()
    request.principal_type = principal_type
    request.principal_id = principal_id
    request.resource_type = resource_type
    response = metadata_service.instance().ListAssignedRoles(request)
    return response


def display_table(headings, roles):
    table = Displayable.from_table(headings=headings, rows=roles, max_width=0)
    # Align columns in the middle horizontally
    table._text_table.set_cols_align(["c" for _ in range(len(headings))])
    printer.safe_print(table)


@dataclass
class ResourceWithRoleAssignments:
    resource_id: Optional[str]

    # sorted list of roles (order will be preserved)
    roles_sorted: List[str]
    # set of roles that have direct assignments
    directly_assigned_roles: Set[str]
    # role to a list of group names that the role is assigned through
    group_assignments_by_role: Mapping[str, List[str]]


@access_control.command("get-roles")
@click.option("-u", "--user", default=None, help="User Email")
@click.option("-s", "--service-account", default=None, help="Service Account ID")
@click.option("-g", "--principal-group", default=None, help="Principal Group ID")
@click.option("-w", "--workspace", default=None, help="Workspace Principal Name")
@click.option(
    "-r",
    "--resource_type",
    default=None,
    type=click.Choice(RESOURCE_TYPES.keys()),
    help="Optional Resource Type to which the Principal has roles assigned.",
)
@click.option("--json-out", default=False, is_flag=True, help="Format Output as JSON")
def get_assigned_roles(user, service_account, principal_group, workspace, resource_type, json_out):
    """Get the roles assigned to a principal."""
    if resource_type is not None:
        resource_type = RESOURCE_TYPES[resource_type]
    principal_type, principal_id = get_principal_details(user, service_account, principal_group, workspace)

    role_defs = _get_role_definitions()

    ws_roles_response = None
    org_roles_response = None
    try:
        if resource_type is None or resource_type == ResourceType.RESOURCE_TYPE_WORKSPACE:
            ws_roles_response = get_roles(principal_type, principal_id, ResourceType.RESOURCE_TYPE_WORKSPACE)
        if resource_type is None or resource_type == ResourceType.RESOURCE_TYPE_ORGANIZATION:
            org_roles_response = get_roles(principal_type, principal_id, ResourceType.RESOURCE_TYPE_ORGANIZATION)
    except Exception as e:
        printer.safe_print(f"Failed to Get Roles: {e}", file=sys.stderr)
        sys.exit(1)

    scope_roles_response = None
    try:
        if resource_type is None or resource_type == ResourceType.RESOURCE_TYPE_SECRET_SCOPE:
            scope_roles_response = get_roles(principal_type, principal_id, ResourceType.RESOURCE_TYPE_SECRET_SCOPE)
    except TectonAPIValidationError as e:
        # TODO: remove when Secrets manager is enabled on every cluster
        # Secrets not enabled on this cluster yet
        scope_roles_response = ListAssignedRolesResponse(assignments=[])
    except Exception as e:
        printer.safe_print(f"Failed to Get Roles: {e}", file=sys.stderr)
        sys.exit(1)

    ws_roles: List[ResourceWithRoleAssignments] = []
    org_roles = ResourceWithRoleAssignments(None, [], set(), {})
    scope_roles: List[ResourceWithRoleAssignments] = []

    ws_roles_response = list(ws_roles_response.assignments) if ws_roles_response else []
    org_roles_response = list(org_roles_response.assignments) if org_roles_response else []
    scope_roles_response = list(scope_roles_response.assignments) if scope_roles_response else []
    for assignment in ws_roles_response + org_roles_response + scope_roles_response:
        roles_for_resource: List[str] = []
        roles_assigned_directly: Set[str] = set()
        role_to_group_names: Mapping[str, List[str]] = {}
        for role_granted in assignment.roles_granted:
            role = _maybe_convert_legacy_role_id(role_defs, role_granted.role)
            groups_with_role = []
            for role_source in role_granted.role_assignment_sources:
                if role_source.assignment_type == RoleAssignmentType.ROLE_ASSIGNMENT_TYPE_DIRECT:
                    roles_assigned_directly.add(role)
                elif role_source.assignment_type == RoleAssignmentType.ROLE_ASSIGNMENT_TYPE_FROM_PRINCIPAL_GROUP:
                    group_name = role_source.principal_group_name
                    groups_with_role.append(group_name)
            roles_for_resource.append(role)
            role_to_group_names[role] = groups_with_role

        if len(roles_for_resource) > 0:
            if assignment.resource_type == ResourceType.RESOURCE_TYPE_WORKSPACE:
                ws_roles.append(
                    ResourceWithRoleAssignments(
                        assignment.resource_id,
                        roles_for_resource,
                        roles_assigned_directly,
                        role_to_group_names,
                    )
                )
            elif assignment.resource_type == ResourceType.RESOURCE_TYPE_ORGANIZATION:
                for role in roles_for_resource:
                    if role not in org_roles.roles_sorted:
                        org_roles.roles_sorted.append(role)
                org_roles.directly_assigned_roles.update(roles_assigned_directly)
                org_roles.group_assignments_by_role.update(role_to_group_names)
            elif assignment.resource_type == ResourceType.RESOURCE_TYPE_SECRET_SCOPE:
                scope_roles.append(
                    ResourceWithRoleAssignments(
                        assignment.resource_id,
                        roles_for_resource,
                        roles_assigned_directly,
                        role_to_group_names,
                    )
                )

    # roles are sorted server side, but re-sort in case org roles came from 2 separate calls to getAssignedRoles
    # (workspace roles also return org roles because of roles on all workspaces)
    org_roles.roles_sorted = sorted(org_roles.roles_sorted)

    if json_out:
        json_output = _convert_assigned_roles_to_json(
            ws_roles=ws_roles,
            org_roles=org_roles,
            scope_roles=scope_roles,
        )
        printer.safe_print(json.dumps(json_output, indent=4))
    else:
        _pretty_print_get_roles_output(
            ws_roles=ws_roles,
            org_roles=org_roles,
            scope_roles=scope_roles,
            show_principal_group_col=workspace is None,
        )


@access_control.command("get-principals")
@click.option("-w", "--workspace", required=False, help="Workspace name")
@click.option("-c", "--secret-scope", required=False, help="Secret scope name")
def get_assigned_principals(workspace, secret_scope):
    """Get principals with access to a resource."""
    if workspace and secret_scope:
        msg = "At most one of --workspace and --secret-scope can be used at the same time."

    request = ListAssignedPrincipalsRequest()
    if workspace:
        request.resource_type = ResourceType.RESOURCE_TYPE_WORKSPACE
        request.resource_id = workspace
    elif secret_scope:
        request.resource_type = ResourceType.RESOURCE_TYPE_SECRET_SCOPE
        request.resource_id = secret_scope
    else:
        request.resource_type = ResourceType.RESOURCE_TYPE_ORGANIZATION
    response = metadata_service.instance().ListAssignedPrincipals(request)

    headings = ["Principal Type", "Principal", "Role", "All Workspaces", "Assigned Directly", "Assigned via Groups"]
    if not workspace:
        headings = [h for h in headings if h != "All Workspaces"]

    output_rows = []
    for assignment_basic_v2 in response.assignments:
        principal = assignment_basic_v2.principal
        if principal.HasField("user"):
            principal_type = "User"
            principal_id_or_email = principal.user.login_email
        elif principal.HasField("service_account"):
            principal_type = "Service Account"
            principal_id_or_email = principal.service_account.id
        elif principal.HasField("group"):
            principal_type = "Group"
            principal_id_or_email = principal.group.id  # customers may complain about the id
        else:
            principal_type = "Workspace"
            principal_id_or_email = principal.workspace.name

        for role_assignment in assignment_basic_v2.role_assignments:
            resource_type = role_assignment.resource_type
            all_workspaces = workspace and resource_type == ResourceType.RESOURCE_TYPE_ORGANIZATION

            for roles_granted in role_assignment.roles_granted:
                role = roles_granted.role
                assigned_directly = False
                assigned_via_groups = []
                for source in roles_granted.role_assignment_sources:
                    if source.assignment_type == RoleAssignmentType.ROLE_ASSIGNMENT_TYPE_DIRECT:
                        assigned_directly = True
                    elif source.assignment_type == RoleAssignmentType.ROLE_ASSIGNMENT_TYPE_FROM_PRINCIPAL_GROUP:
                        assigned_via_groups.append(source.principal_group_name)

                row = [principal_type, principal_id_or_email, role]
                if workspace:
                    row += ["yes" if all_workspaces else ""]
                row += ["directly" if assigned_directly else "", ",".join(assigned_via_groups)]
                output_rows.append(tuple(row))
    display_table(headings, output_rows)


def _convert_assigned_roles_json_generic_resource(
    resource_type_for_output: str,
    # This parameter is is needed for legacy reasons, because for workspaces we called the field "workspace_name"
    # In 1.0 we can remove this parameter and just call the field "name"
    resource_name_field_name: Optional[str],
    roles: List[ResourceWithRoleAssignments],
) -> List[Dict]:
    json_output = []
    for resource in roles:
        roles_granted = []
        for role in resource.roles_sorted:
            assignment_sources = []
            if role in resource.directly_assigned_roles:
                assignment_sources.append({"assignment_type": "DIRECT"})
            for group_name in resource.group_assignments_by_role[role]:
                assignment_sources.append({"assignment_type": "PRINCIPAL_GROUP", "group_name": group_name})
            roles_granted.append({"role": role, "assignment_sources": assignment_sources})
        if len(roles_granted) > 0:
            if resource_name_field_name is None:
                json_output.append(
                    {
                        "resource_type": resource_type_for_output,
                        "roles_granted": roles_granted,
                    }
                )
            else:
                json_output.append(
                    {
                        "resource_type": resource_type_for_output,
                        resource_name_field_name: resource.resource_id,
                        "roles_granted": roles_granted,
                    }
                )
    return json_output


def _convert_assigned_roles_to_json(
    ws_roles: List[ResourceWithRoleAssignments],
    org_roles: ResourceWithRoleAssignments,
    scope_roles: List[ResourceWithRoleAssignments],
) -> List[Dict]:
    json_output = []
    json_output += _convert_assigned_roles_json_generic_resource("WORKSPACE", "workspace_name", ws_roles)
    json_output += _convert_assigned_roles_json_generic_resource("ORGANIZATION", None, [org_roles])
    json_output += _convert_assigned_roles_json_generic_resource("SECRET_SCOPE", "name", scope_roles)
    return json_output


def _pretty_print_assigned_roles_generic_resource(
    resource_type_for_display: str,
    roles: List[ResourceWithRoleAssignments],
    show_principal_groups_col: bool,
):
    """For generic resources of which there can be many (e.g. workspace, secret scope)"""
    headings = [resource_type_for_display, "Role", "Assigned Directly"]
    if show_principal_groups_col:
        headings += ["Assigned via Groups"]
    display_rows = []
    for assignment_for_resource in roles:
        resource_name = assignment_for_resource.resource_id
        already_displayed_resource_name = False
        for role in assignment_for_resource.roles_sorted:
            resource_name_to_display = "" if already_displayed_resource_name else resource_name
            already_displayed_resource_name = True
            assigned_directly = "direct" if role in assignment_for_resource.directly_assigned_roles else ""
            resource_role_row = (resource_name_to_display, role, assigned_directly)
            if show_principal_groups_col:
                group_names = ", ".join(assignment_for_resource.group_assignments_by_role[role])
                resource_role_row += (group_names,)

            display_rows.append(resource_role_row)
    display_table(headings, display_rows)


def _pretty_print_assigned_roles_org_resource(
    org_roles: ResourceWithRoleAssignments,
):
    """For the singleton organization resource"""
    headings = ["Organization Roles", "Assigned Directly", "Assigned via Groups"]
    display_rows = []
    for role in org_roles.roles_sorted:
        assigned_directly = "direct" if role in org_roles.directly_assigned_roles else ""
        group_names = ", ".join(org_roles.group_assignments_by_role[role])
        role_row = (role, assigned_directly, group_names)

        display_rows.append(role_row)
    display_table(headings, display_rows)


def _pretty_print_get_roles_output(
    ws_roles: List[ResourceWithRoleAssignments],
    org_roles: ResourceWithRoleAssignments,
    scope_roles: List[ResourceWithRoleAssignments],
    show_principal_group_col: bool,
):
    if len(ws_roles) > 0:
        _pretty_print_assigned_roles_generic_resource("Workspace", ws_roles, True)
        printer.safe_print()
    if len(org_roles.roles_sorted) > 0:
        _pretty_print_assigned_roles_org_resource(org_roles)
        printer.safe_print()
    if len(scope_roles) > 0:
        _pretty_print_assigned_roles_generic_resource("Secret Scope", scope_roles, show_principal_group_col)


def _maybe_convert_legacy_role_id(role_defs, id):
    role_def = next((r for r in role_defs if r.id == id or r.legacy_id == id), None)
    role_id = id if role_def is None else role_def.id
    return role_id


def get_user_id(email):
    try:
        request = GetUserRequest()
        request.email = email
        response = metadata_service.instance().GetUser(request)
        return response.user.okta_id
    except Exception as e:
        printer.safe_print(f"Failed to Get Roles for email [{email}]: {e}", file=sys.stderr)
        sys.exit(1)


def get_principal_details(user, service_account, principal_group, workspace_principal):
    principal_type_count = sum([p is not None for p in [user, service_account, principal_group, workspace_principal]])
    if principal_type_count > 1:
        msg = "Please mention a single Principal Type using one of --user, --service-account, or --principal-group (or --workspace if using --secret-scope)"
        raise click.ClickException(msg)
    if user:
        return PrincipalType.PRINCIPAL_TYPE_USER, get_user_id(user)
    elif service_account:
        return PrincipalType.PRINCIPAL_TYPE_SERVICE_ACCOUNT, service_account
    elif principal_group:
        return PrincipalType.PRINCIPAL_TYPE_GROUP, principal_group
    elif workspace_principal:
        return PrincipalType.PRINCIPAL_TYPE_WORKSPACE, workspace_principal
    else:
        msg = "Please mention a Principal Type using --user, --service-account, or --principal-group (or --workspace for workspace authorization on secret scopes)."
        raise click.ClickException(msg)
