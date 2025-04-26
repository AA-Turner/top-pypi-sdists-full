from dataclasses import dataclass
from . import (
    apps,
    orgs,
    context,
    issuers as _issuers,
    users as _users,
    resources as _resources,
    connectors as _connectors,
    output,
)


@dataclass
class PrimaryKeyMapping:
    primary_key_field: str
    collection: str = None


def get_key_from_dict(obj, pk_mapping):
    if pk_mapping.collection:
        return obj[pk_mapping.collection][pk_mapping.primary_key_field]
    return obj[pk_mapping.primary_key_field]


def get_key_from_obj(obj, pk_mapping):
    if pk_mapping.collection:
        base = getattr(obj, pk_mapping.collection)
        return getattr(base, pk_mapping.primary_key_field)
    return getattr(obj, pk_mapping.primary_key_field)


def _get_primary_keys(obj, primary_key_mapping):
    res = []
    for mapping in primary_key_mapping:
        if isinstance(obj, dict):
            res.append(get_key_from_dict(obj, mapping))
        else:
            res.append(get_key_from_obj(obj, mapping))
    if len(res) == 1:
        return res[0]
    return tuple(res)


def get_orphaned_resources(working_resource_set, obj_list, primary_key_mapping):
    result = []
    for obj in obj_list:
        key = _get_primary_keys(obj, primary_key_mapping)
        if key not in working_resource_set:
            result.append(obj)
    return result


def get_org_id_list(ctx, enabled=None, **kwargs):
    return {org["id"] for org in orgs.query(ctx, enabled=enabled, **kwargs)}


def get_org_id_map(ctx, enabled=None, **kwargs):
    orgs_map = {}
    for org in orgs.query(ctx, enabled=enabled, **kwargs):
        orgs_map[org["id"]] = org
    return orgs_map


# This function takes a working resource set, query function, and a mapping object
# that indicates how to get the primary key values out of the objects returned from
# the query function. These keys are compared to the working resource set. Keys not
# found in the working resource set are determined to be orphaned.
def get_api_orphaned_resources(
    ctx, working_resource_set, query_func, primary_key_mapping, **kwargs
):
    obj_list = query_func(ctx, **kwargs)
    return (
        get_orphaned_resources(working_resource_set, obj_list, primary_key_mapping),
        obj_list,
    )


def output_orphan_info(ctx, collection_name, orphan_tuple, format_func):
    orphans = orphan_tuple[0]
    num_orphans = len(orphans)
    total = len(orphan_tuple[1])

    if context.output_console(ctx):
        print(f"There are {total} {collection_name}")
        print(f"There are {num_orphans} orphanded {collection_name}")
    print(format_func(ctx, orphans))


RESOURCE_TO_FORMATTER_MAP = {
    "applications": apps.format_apps_for_garbage_collection,
    "issuers": _issuers.format_issuers_for_garbage_collection,
    "resources": _resources.format_permissions,
    "users": _users.format_users_for_garbage_collection,
    "roles": _users.format_org_user_roles,
    "connectors": _connectors.format_for_gc,
}


def output_orphaned_resources(ctx, result_table):
    for k, v in result_table.items():
        output_orphan_info(ctx, k, v, RESOURCE_TO_FORMATTER_MAP[k])


def get_all_orphaned_resources(
    ctx,
    applications=None,
    issuers=None,
    users=None,
    resources=None,
    connectors=None,
    roles=None,
    **kwargs,
):

    result = {}
    if any([applications, issuers, users, resources, connectors]):
        result.update(
            get_org_orphaned_resources(
                ctx,
                applications=applications,
                issuers=issuers,
                users=users,
                resources=resources,
                connectors=connectors,
                **kwargs,
            )
        )

    if roles:
        result.update(get_app_orphaned_resources(ctx, roles=roles, **kwargs))
    return result


def get_org_orphaned_resources(
    ctx,
    applications=None,
    issuers=None,
    users=None,
    resources=None,
    connectors=None,
    mark_connectors_deleted=None,
    only_org_enabled=None,
    dry_run=False,
    **kwargs,
):
    enabled = None
    if only_org_enabled:
        enabled = True

    # retrieve a map of all orgs, so we know the name of things
    # that may be deleted
    org_id_map = get_org_id_map(ctx, **kwargs)
    org_id_list = get_org_id_list(ctx, enabled=enabled, **kwargs)

    result = {}

    output.output_if_console(ctx, f"Total Organisations: {len(org_id_list)}")

    if applications:
        result["applications"] = get_api_orphaned_resources(
            ctx, org_id_list, apps.query, [PrimaryKeyMapping("org_id")], **kwargs
        )

    if issuers:
        result["issuers"] = get_api_orphaned_resources(
            ctx, org_id_list, _issuers.query, [PrimaryKeyMapping("org_id")], **kwargs
        )

    if connectors:
        result["connectors"] = get_api_orphaned_resources(
            ctx,
            org_id_list,
            _connectors.query,
            [PrimaryKeyMapping("org_id", collection="spec")],
            **kwargs,
        )
        if mark_connectors_deleted:
            for connector in result["connectors"][0]:
                org = org_id_map.get(connector["spec"]["org_id"])
                if not org:
                    org_name = "deleted"
                else:
                    org_name = org.get("organisation")
                if dry_run:
                    output.output_if_console(
                        ctx,
                        "would mark connector deleted: "
                        f"{connector['metadata']['id']}, org {org_name}",
                    )
                else:
                    output.output_if_console(
                        ctx,
                        "marking connector deleted: "
                        f"{connector['metadata']['id']}, org {org_name}",
                    )
                    _connectors.replace_agent(
                        ctx,
                        connector["metadata"]["id"],
                        org_id=connector["spec"]["org_id"],
                        admin_status="deleted",
                    )

    if resources:
        result["resources"] = get_api_orphaned_resources(
            ctx,
            org_id_list,
            _resources.query_permissions,
            [PrimaryKeyMapping("org_id", collection="spec")],
            **kwargs,
        )

    if users:
        total = _users.query(ctx, **kwargs)["users"]
        orgless = _users.query(ctx, orgless_users=True, **kwargs)["users"]
        result["users"] = orgless, total

    return result


def get_app_orphaned_resources(ctx, roles=None, **kwargs):
    result = {}
    list_of_apps = apps.query(ctx, **kwargs)
    app_org_id_list = {(app.name, app.org_id) for app in list_of_apps}
    orphans = get_api_orphaned_resources(
        ctx,
        app_org_id_list,
        _users.list_org_user_roles,
        [PrimaryKeyMapping("application"), PrimaryKeyMapping("org_id")],
        **kwargs,
    )

    orphans = [
        orphan
        for orphan in orphans
        if not orphan.application.startswith("urn:api:agilicus")
    ]

    result["roles"] = orphans
    return result
