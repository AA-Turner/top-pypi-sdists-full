import click

from . import context
from .input_helpers import get_org_from_input_or_ctx, update_if_not_none
from .input_helpers import get_user_id_from_input_or_ctx
from .input_helpers import update_org_from_input_or_ctx, strip_none
from .create import handle_api_409
from agilicus.output.table import make_columns
from . import resource_helpers


from .output.table import (
    subobject_column,
    format_table,
    metadata_column,
    spec_column,
    status_column,
    subtable,
)
import agilicus

permissioned_resource_types = [
    "application",
    "fileshare",
    "application_service",
    "desktop",
    "group",
    "launcher",
    "ssh",
    "database",
]
resource_types = permissioned_resource_types + ["service_forwarder"]
permissioned_resource_type_enum = click.Choice(permissioned_resource_types)
resource_type_enum = click.Choice(resource_types)


def query_permissions(ctx, org_id=None, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    query_results = apiclient.permissions_api.list_resource_permissions(
        org_id=org_id, **strip_none(kwargs)
    )
    if query_results:
        return query_results.resource_permissions
    return []


def render_permissions(ctx, org_id=None, user_id=None, limit=None, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    user_id = get_user_id_from_input_or_ctx(ctx, user_id=user_id)
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    query_results = apiclient.user_api.list_all_resource_permissions(
        org_id=org_id, user_id=user_id, **strip_none(kwargs)
    )
    if query_results:
        return query_results.resource_permissions
    return []


def format_permissions(ctx, roles):
    columns = [
        metadata_column("id"),
        spec_column("resource_type", "type"),
        spec_column("user_id", "user id"),
        spec_column("org_id", "org id"),
        spec_column("resource_id", "resource id"),
        spec_column("resource_role_name", "role"),
    ]
    return format_table(ctx, roles, columns)


def add_permission(
    ctx, user_id, resource_id, resource_type, resource_role_name, org_id=None
):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    spec = agilicus.ResourcePermissionSpec(
        org_id=org_id,
        user_id=user_id,
        resource_type=resource_type,
        resource_role_name=resource_role_name,
        resource_id=resource_id,
    )
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    return apiclient.permissions_api.create_resource_permission(
        agilicus.ResourcePermission(spec=spec)
    ).to_dict()


def delete_permission(ctx, id, org_id=None):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    return apiclient.permissions_api.delete_resource_permission(id, org_id=org_id)


def bulk_delete_permission(ctx, **kwargs):
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    apiclient = context.get_apiclient_from_ctx(ctx)
    return apiclient.permissions_api.bulk_delete_resource_permission(
        **strip_none(kwargs)
    )


def query_resources(ctx, org_id=None, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = org_id
    params = {}
    update_if_not_none(params, kwargs)
    query_results = apiclient.resources_api.list_resources(**params)
    if query_results:
        return query_results.resources
    return []


def format_resources(ctx, resources, show_columns=None, reset_columns=None):
    columns = make_columns(
        ctx,
        resources,
        """
          - metadata.id(newname=id)
          - spec.resource_type(newname=resource_type)
          - spec.name(newname=name)
          - status.resource_stats.overall_status(newname=status)
        """,
        show=show_columns,
        clear=reset_columns,
    )
    return format_table(ctx, resources, columns)


def query_roles(ctx, org_id=None, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    query_results = apiclient.permissions_api.list_resource_roles(
        org_id=org_id, **strip_none(kwargs)
    )
    return query_results.resource_roles


def format_roles(ctx, roles):
    columns = [
        spec_column("resource_type", "type"),
        spec_column("role_name", "name"),
    ]
    return format_table(ctx, roles, columns)


def create_resource_group(ctx, resource_members, name, org_id=None):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    member_objs = []
    for member in resource_members:
        member_objs.append(agilicus.ResourceMember(id=member))
    spec = agilicus.ResourceSpec(
        resource_members=member_objs, resource_type="group", name=name, org_id=org_id
    )
    resource = agilicus.Resource(spec=spec)

    return apiclient.resources_api.add_resource(resource).to_dict()


def delete_resource(ctx, id, org_id=None):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    return apiclient.resources_api.delete_resource(id, org_id=org_id)


def _get_resource(ctx, id, org_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.resources_api.get_resource(id, org_id=org_id, **strip_none(kwargs))


def get_resource(ctx, id, org_id=None, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    resource = _get_resource(ctx, id, org_id, **kwargs)
    return resource.to_dict()


def reconcile_default_policy(ctx, resource_id, org_id=None):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    resource = _get_resource(ctx, resource_id, org_id)
    try:
        resource = apiclient.resources_api.reconcile_default_policy(
            resource_id, resource=resource
        )
    except agilicus.ApiException as exc:
        if exc.status != 409:
            # If there was already a default, nothing for us to do
            raise
        return handle_api_409(exc, klass=agilicus.Resource)
    return resource


def update_resource(
    ctx,
    id,
    resource_members=None,
    remove_resource_members=None,
    name=None,
    org_id=None,
    rules_config_file=None,
    roles_config_file=None,
    published=None,
    hide=None,
    bundle_id=None,
    **kwargs,
):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    resource = apiclient.resources_api.get_resource(id, org_id=org_id)
    if remove_resource_members is not None:
        old_members = resource.spec.resource_members
        resource.spec.resource_members = []
        for member in old_members:
            if member.id in remove_resource_members:
                # needs to be removed.
                continue
            resource.spec.resource_members.append(member)

    config = resource.spec.config
    if config is None:
        config = agilicus.ResourceConfig()
        resource.spec.config = config

    if resource_members is not None:
        for member in resource_members:
            resource.spec.resource_members.append(agilicus.ResourceMember(id=member))
    if name is not None:
        resource.spec.name = name
    if rules_config_file is not None:
        resource.spec.config.rules_config = rules_config_file
    if roles_config_file is not None:
        resource.spec.config.roles_config = roles_config_file
    if published is not None:
        resource.spec.config.published = published
    if bundle_id is not None:
        resource.spec.bundle_id = bundle_id

    if hide:
        display_info = config.display_info
        if display_info is None:
            display_info = agilicus.DisplayInfo(icons=[])
            config.display_info = display_info
        display_info.hide = hide

    return apiclient.resources_api.replace_resource(id, resource=resource).to_dict()


def add_display_info_icon(
    ctx, resource_id, uri, purpose, height_px, width_px, org_id, **kwargs
):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    resource = _get_resource(ctx, resource_id, org_id=org_id)

    config = resource.spec.config
    if config is None:
        config = agilicus.ResourceConfig()
        resource.spec.config = config

    resource_helpers.add_display_info_icon(config, uri, purpose, height_px, width_px)

    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.resources_api.replace_resource(
        resource_id, resource=resource
    ).to_dict()


def delete_display_info_icon(ctx, resource_id, uri, org_id, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    resource = _get_resource(ctx, resource_id, org_id=org_id)

    config = resource.spec.config
    if not resource_helpers.delete_display_info_icon(config, uri):
        return resource.to_dict()

    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.resources_api.replace_resource(
        resource_id, resource=resource
    ).to_dict()


def list_combined_resource_rules(ctx, org_id=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id, **kwargs)
    kwargs = strip_none(kwargs)
    query_results = apiclient.resources_api.list_combined_resource_rules(
        org_id=org_id, **kwargs
    )
    if query_results:
        return query_results.combined_resource_rules
    return []


def format_combined_resource_rules_as_text(ctx, resource_rules):
    def node_column(name):
        return subobject_column(name, name, "node")

    rules_columns = [
        subobject_column("priority", "priority", "node"),
        subobject_column("rule.name", "name", "node"),
    ]

    columns = [
        status_column("org_id"),
        status_column("resource_id"),
        status_column("scope"),
        status_column("role_name"),
        subtable(ctx, "rules", rules_columns, subobject_name="status"),
    ]

    return format_table(ctx, resource_rules, columns)


def list_resource_groups(ctx, org_id=None, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_ids = []
    if org_id:
        org_ids.append(org_id)
    query_results = apiclient.resources_api.list_resource_groups(
        org_ids=org_ids, **strip_none(kwargs)
    )
    if query_results:
        return query_results.resource_groups
    return []
