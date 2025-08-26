import json
import urllib.parse

import requests
import agilicus
import operator
import dateparser
import datetime
from . import get_many_entries

from dataclasses import dataclass

from . import context, response
from . import input_helpers
from .input_helpers import build_updated_model
from .input_helpers import parse_csv_input
from .input_helpers import get_org_from_input_or_ctx
from .input_helpers import get_user_id_from_input_or_ctx
from .input_helpers import strip_none
from .input_helpers import update_if_present, update_if_not_none
from .input_helpers import update_org_from_input_or_ctx
from .output.table import (
    column,
    format_table,
    mapped_column,
    metadata_column,
    spec_column,
    status_column,
    subtable,
)

USERS_BASE_URI = "/users"
GROUPS_BASE_URI = "/v1/groups"
STATUS_OPTIONS = ["active", "pending", "disabled", "default"]
USER_TYPES = ["user", "group", "sysgroup", "bigroup", "service_account"]


def handle_inheritable_configs(d):
    description = d.pop("description", None)

    d["inheritable_config"] = agilicus.InheritableUserConfig()
    if description is not None:
        d["inheritable_config"].description = description


def get_uri(type):
    if "user" == type:
        return USERS_BASE_URI
    if "service_account" == type:
        return USERS_BASE_URI
    elif "group" == type:
        return GROUPS_BASE_URI
    elif "sysgroup" == type:
        return GROUPS_BASE_URI
    elif "bigroup" == type:
        return GROUPS_BASE_URI


def _construct_query(
    ctx,
    org_id=None,
    type=None,
    email=None,
    previous_email=None,
    limit=None,
    search_params=None,
    **kwargs,
):
    params = {}

    if not type:
        type = ["user"]
    elif isinstance(type, tuple):
        type = list(type)

    params["type"] = type
    update_org_from_input_or_ctx(params, ctx, org_id=org_id)

    if email:
        params["email"] = email
    if previous_email is not None:
        params["previous_email"] = previous_email
    if limit:
        params["limit"] = limit
    if search_params is not None and len(search_params):
        params["search_params"] = [*search_params]

    update_if_not_none(params, kwargs)
    return params


def query_raw(
    ctx, org_id=None, type=None, email=None, previous_email=None, limit=None, **kwargs
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    params = _construct_query(
        ctx,
        org_id=org_id,
        type=type,
        email=email,
        previous_email=previous_email,
        limit=limit,
        **kwargs,
    )
    return apiclient.user_api.list_users(**params)


def get_user(ctx, user_id, org_id=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, org_id=org_id)
    return apiclient.user_api.get_user(user_id, **kwargs)


def query(
    ctx, org_id=None, type=None, email=None, previous_email=None, limit=None, **kwargs
):
    return query_raw(
        ctx,
        org_id=org_id,
        type=type,
        email=email,
        previous_email=previous_email,
        limit=limit,
        **kwargs,
    )


def format_users_for_garbage_collection(ctx, users):
    columns = [
        column("id"),
        column("first_name", optional=True),
        column("last_name", optional=True),
        column("email", optional=True),
        column("provider", optional=True),
        column("type", optional=True),
        column("created", optional=True),
        column("updated", optional=True),
    ]
    return format_table(ctx, users, columns, getter=operator.itemgetter)


def query_groups(
    ctx, org_id=None, type=None, email=None, previous_email=None, limit=None, **kwargs
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    params = _construct_query(
        ctx,
        org_id=org_id,
        type=type,
        email=email,
        previous_email=previous_email,
        limit=limit,
        **kwargs,
    )
    return apiclient.groups_api.list_groups(**params).to_dict()


def get_group(ctx, group_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    return apiclient.groups_api.get_group(group_id, **kwargs).to_dict()


def _get_roles_for_user(ctx, user_id, org_id):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    user = get_user(ctx, user_id, org_id)
    return user.get("roles", {})


def add_user_role(ctx, user_id, application, roles, org_id=None, update=False):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers["content-type"] = "application/json"
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    data = {}
    apps = {}
    if update:
        apps = _get_roles_for_user(ctx, user_id, org_id)

    existing = apps.setdefault(application, [])
    apps[application] = list(set(existing + roles))

    data["roles"] = apps
    data["org_id"] = org_id
    params = {}
    params["org_id"] = org_id
    query = urllib.parse.urlencode(params)

    uri = "{}/{}/roles?{}".format(get_uri("user"), user_id, query)
    resp = requests.put(
        context.get_api(ctx) + uri,
        headers=headers,
        data=json.dumps(data),
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return resp.text


def list_user_roles(ctx, user_id, org_id=None):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers["content-type"] = "application/json"

    if org_id is None:
        org_id = context.get_org_id(ctx, token)

    params = {}
    params["org_id"] = org_id
    query = urllib.parse.urlencode(params)
    uri = "{}/{}/render_roles?{}".format(get_uri("user"), user_id, query)
    resp = requests.get(
        context.get_api(ctx) + uri,
        headers=headers,
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return resp.text


def delete_user(ctx, user_id, org_id=None, type="user"):
    token = context.get_token(ctx)

    if org_id is None:
        org_id = context.get_org_id(ctx, token)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)

    uri = "/v1/orgs/{}/users/{}".format(org_id, user_id)
    resp = requests.delete(
        context.get_api(ctx) + uri,
        headers=headers,
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return resp.text


def add_group(ctx, first_name=None, org_id=None, **kwargs):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers["content-type"] = "application/json"

    user = {}
    if org_id is None:
        org_id = context.get_org_id(ctx, token)

    user["org_id"] = org_id
    user["first_name"] = first_name
    update_if_not_none(user, kwargs)
    if user.get("type") == "group":
        # The default is group in the backend. We restrict normal users from defining
        # other types of groups through this endpoint, so delete it.
        del user["type"]

    uri = "{}".format(get_uri("group"))
    resp = requests.post(
        context.get_api(ctx) + uri,
        headers=headers,
        data=json.dumps(user),
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return json.loads(resp.text)


def add_group_member(
    ctx, group_id, member=None, org_id=None, member_org_id=None, email=None
):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers["content-type"] = "application/json"

    if org_id is None:
        org_id = context.get_org_id(ctx, token)

    for id in member:
        member = {}
        member["id"] = id
        member["member_id"] = id
        member["org_id"] = org_id
        if member_org_id:
            member["member_org_id"] = member_org_id
        uri = "{}/{}/members".format(get_uri("group"), group_id)
        resp = requests.post(
            context.get_api(ctx) + uri,
            headers=headers,
            data=json.dumps(member),
            verify=context.get_cacert(ctx),
        )
        response.validate(resp)

    for user_email in email:
        member = {}
        member["email"] = user_email
        member["org_id"] = org_id
        if member_org_id:
            member["member_org_id"] = member_org_id
        uri = "{}/{}/members".format(get_uri("group"), group_id)
        resp = requests.post(
            context.get_api(ctx) + uri,
            headers=headers,
            data=json.dumps(member),
            verify=context.get_cacert(ctx),
        )
        response.validate(resp)


def delete_group_member(ctx, group_id, member, org_id=None):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers["content-type"] = "application/json"

    params = {}
    if org_id is None:
        org_id = context.get_org_id(ctx, token)

    params = {}
    params["org_id"] = org_id
    query = urllib.parse.urlencode(params)
    for id in member:
        uri = "{}/{}/members/{}?{}".format(get_uri("group"), group_id, id, query)
        resp = requests.delete(
            context.get_api(ctx) + uri,
            headers=headers,
            data=json.dumps(member),
            verify=context.get_cacert(ctx),
        )
        response.validate(resp)


def add_user(ctx, first_name, last_name, email, org_id, **kwargs):
    token = context.get_token(ctx)

    if org_id is None:
        org_id = context.get_org_id(ctx, token)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers["content-type"] = "application/json"

    user = {}
    user["org_id"] = org_id
    user["first_name"] = first_name
    user["last_name"] = last_name
    user["email"] = email
    update_if_present(user, "external_id", **kwargs)
    update_if_present(user, "status", **kwargs)
    update_if_present(user, "enabled", **kwargs)

    uri = "/users"
    resp = requests.post(
        context.get_api(ctx) + uri,
        headers=headers,
        data=json.dumps(user),
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return json.loads(resp.text)


def update_user_with_user(ctx, user, disabled_at_time=None, **kwargs):
    if disabled_at_time is not None:
        if disabled_at_time:
            user["disabled_at_time"] = (
                dateparser.parse(disabled_at_time)
                .replace(tzinfo=datetime.timezone.utc)
                .isoformat()
            )
        else:
            # user is clearing it (none)
            user["disabled_at_time"] = None

    update_if_present(user, "first_name", **kwargs)
    update_if_present(user, "last_name", **kwargs)
    update_if_present(user, "email", **kwargs)
    update_if_present(user, "external_id", **kwargs)
    update_if_present(user, "auto_created", **kwargs)
    update_if_present(user, "status", **kwargs)
    update_if_present(user, "enabled", **kwargs)
    update_if_present(user, "cascade", **kwargs)

    user["inheritable_config"] = {}
    if kwargs.get("description", None) is not None:
        user["inheritable_config"]["description"] = kwargs["description"]

    attributes = kwargs.get("attribute", None)
    if attributes is not None:
        formatted_attributes = [
            {"name": attr[0], "value": attr[1]} for attr in attributes
        ]
        user["configured_attributes"] = {"attributes": formatted_attributes}

    remove_attributes = set(kwargs.get("remove_attribute", []))
    if remove_attributes is not None:
        updated_attrs = [
            attr
            for attr in user.get("configured_attributes", {}).get("attributes")
            if attr not in remove_attributes
        ]
        user["configured_attributes"] = {"attributes": updated_attrs}

    apiclient = context.get_apiclient_from_ctx(ctx)
    return apiclient.user_api.replace_user(user["id"], user=user)


def update_user(ctx, user_id, org_id=None, **kwargs):
    user = get_user(ctx, user_id, org_id=org_id).to_dict()
    return update_user_with_user(ctx, user, **kwargs)


def list_mfa_challenge_methods(ctx, user_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs = strip_none(kwargs)
    query_results = apiclient.user_api.list_challenge_methods(user_id, **kwargs)
    if query_results:
        return query_results.mfa_challenge_methods
    return []


def add_mfa_challenge_method(ctx, user_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs = strip_none(kwargs)
    spec = agilicus.MFAChallengeMethodSpec(**kwargs)
    model = agilicus.MFAChallengeMethod(spec=spec)
    return apiclient.user_api.create_challenge_method(user_id, model).to_dict()


def _get_mfa_challenge_method(apiclient, user_id, challenge_method_id):
    return apiclient.user_api.get_challenge_method(user_id, challenge_method_id)


def show_mfa_challenge_method(ctx, user_id, challenge_method_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return _get_mfa_challenge_method(apiclient, user_id, challenge_method_id).to_dict()


def delete_mfa_challenge_method(ctx, user_id, challenge_method_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return apiclient.user_api.delete_challenge_method(
        user_id, challenge_method_id, **kwargs
    )


def update_mfa_challenge_method(ctx, user_id, challenge_method_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    method = _get_mfa_challenge_method(apiclient, user_id, challenge_method_id)
    kwargs = strip_none(kwargs)
    method.spec = build_updated_model(
        agilicus.MFAChallengeMethodSpec, method.spec, kwargs
    )
    return apiclient.user_api.replace_challenge_method(
        user_id, challenge_method_id, mfa_challenge_method=method
    ).to_dict()


def reset_user_mfa_challenge_methods(ctx, user_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id_input = kwargs.pop("org_id", None)
    org_id = get_org_from_input_or_ctx(ctx, org_id_input)
    model = agilicus.ResetMFAChallengeMethod(org_id=org_id)
    return apiclient.user_api.reset_user_mfa_challenge_methods(user_id, model, **kwargs)


def reset_user_identity(ctx, user_id, identifier, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id_input = kwargs.pop("org_id", None)
    org_id = get_org_from_input_or_ctx(ctx, org_id_input)
    model = agilicus.ResetUserIdentityRequest(
        org_id=org_id,
        new_identifier=agilicus.Email(identifier),
    )
    return apiclient.user_api.reset_user_identity(user_id, model, **kwargs)


def list_combined_user_details(ctx, org_id=None, **kwargs):
    org_id = input_helpers.get_org_from_input_or_ctx(ctx, org_id=org_id, **kwargs)
    apiclient = context.get_apiclient_from_ctx(ctx)
    input_helpers.pop_item_if_none(kwargs)
    kwargs["type"] = "user"
    if kwargs.get("search_params", None):
        kwargs["search_params"] = [*kwargs["search_params"]]
    results = apiclient.user_api.list_combined_user_details(org_id=org_id, **kwargs)
    return results.combined_user_details


def make_flat_user_detail(detail):
    base = detail.status.user
    methods = detail.status.mfa_challenge_methods
    base.mfa_methods = methods
    return base


def format_combined_user_details_as_text(ctx, details):
    flattened = [make_flat_user_detail(detail) for detail in details]
    mfa_columns = [
        metadata_column("id"),
        spec_column("challenge_type"),
        spec_column("priority"),
        spec_column("endpoint"),
        spec_column("origin"),
        spec_column("enabled"),
    ]
    columns = [
        column("id"),
        mapped_column("first_name", "First Name"),
        mapped_column("last_name", "Last Name"),
        column("email"),
        mapped_column("org_id", "Organisation"),
        subtable(ctx, "mfa_methods", mfa_columns),
    ]

    return format_table(ctx, flattened, columns)


def format_upstream_user_identities_as_text(ctx, ids):
    columns = [
        metadata_column("id"),
        spec_column("local_user_id"),
        spec_column("upstream_user_id"),
        spec_column("upstream_idp_id"),
    ]

    return format_table(ctx, ids, columns)


def list_upstream_user_identities(ctx, user_id=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    user_id = input_helpers.get_user_id_from_input_or_ctx(ctx, user_id)
    query_results = apiclient.user_api.list_upstream_user_identities(user_id, **kwargs)
    if query_results:
        return query_results.upstream_user_identities
    return []


def update_user_identity(ctx, user_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    spec = agilicus.UserIdentityUpdateSpec(**kwargs)
    model = agilicus.UserIdentityUpdate(spec=spec)
    return apiclient.user_api.create_user_identity_update(user_id, model).to_dict()


def add_upstream_user_identity(ctx, user_id=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    user_id = input_helpers.get_user_id_from_input_or_ctx(ctx, user_id)
    spec = agilicus.UpstreamUserIdentitySpec(local_user_id=user_id, **kwargs)
    model = agilicus.UpstreamUserIdentity(spec=spec)
    return apiclient.user_api.create_upstream_user_identity(user_id, model).to_dict()


def _get_upstream_user_identity(apiclient, user_id, upstream_user_identity_id):
    return apiclient.user_api.get_upstream_user_identity(
        user_id, upstream_user_identity_id
    )


def show_upstream_user_identity(ctx, upstream_user_identity_id, user_id=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    user_id = input_helpers.get_user_id_from_input_or_ctx(ctx, user_id)
    return _get_upstream_user_identity(
        apiclient, user_id, upstream_user_identity_id
    ).to_dict()


def delete_upstream_user_identity(
    ctx, upstream_user_identity_id, user_id=None, **kwargs
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    user_id = input_helpers.get_user_id_from_input_or_ctx(ctx, user_id)
    return apiclient.user_api.delete_upstream_user_identity(
        user_id, upstream_user_identity_id, **kwargs
    )


def update_upstream_user_identity(
    ctx, upstream_user_identity_id, user_id=None, **kwargs
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    user_id = input_helpers.get_user_id_from_input_or_ctx(ctx, user_id)
    model = _get_upstream_user_identity(apiclient, user_id, upstream_user_identity_id)
    model.spec = build_updated_model(
        agilicus.UpstreamUserIdentitySpec, model.spec, kwargs
    )
    model.spec.local_user_id = user_id
    return apiclient.user_api.replace_upstream_user_identity(
        user_id, upstream_user_identity_id, upstream_user_identity=model
    ).to_dict()


@dataclass
class EmailMapping:
    email: str
    upstream_user_id: str

    @classmethod
    def from_dict(cls, info: dict):
        return cls(email=info["email"], upstream_user_id=info["upstream_user_id"])


def find_mapping(user: agilicus.User, upstream_user_id: str, upstream_idp_id: str):
    for upstream_info in user.upstream_user_identities or []:
        if all(
            [
                upstream_info.spec.upstream_user_id == upstream_user_id,
                upstream_info.spec.upstream_idp_id == upstream_idp_id,
            ]
        ):
            return upstream_info

    return None


def upload_upstream_user_identity_list(ctx, org_id, upstream_idp_id, email_mapping_file):
    users = query_raw(ctx, org_id=org_id, type=["user"]).users
    user_mapping = parse_csv_input(email_mapping_file, EmailMapping.from_dict)
    user_mapping_dict = {
        mapping.email: mapping.upstream_user_id for mapping in user_mapping
    }

    count = 0
    for user in users:
        upstream_user_id = user_mapping_dict.get(user.email, None)
        # If the mapping doesn't exist, or it's blank (i.e. no id)
        if not upstream_user_id:
            continue

        existing_mapping = find_mapping(user, upstream_user_id, upstream_idp_id)
        if existing_mapping:
            continue

        add_upstream_user_identity(
            ctx,
            user.id,
            upstream_user_id=upstream_user_id,
            upstream_idp_id=upstream_idp_id,
        )
        count += 1

    print(f"Added identity to {count} users")


def format_user_application_access_info_as_text(ctx, info):
    columns = [
        status_column("org_id"),
        status_column("org_name"),
        status_column("user_id"),
        status_column("application_name"),
        status_column("application_url"),
        status_column("application_description"),
        status_column("application_category"),
        status_column("application_default_role_name"),
        status_column("application_default_role_id"),
        status_column("icon_url"),
        status_column("access_level"),
        status_column("parent_org_name"),
        status_column("parent_org_id"),
        status_column("roles"),
    ]

    return format_table(ctx, info, columns)


def format_user_fileshare_access_info_as_text(ctx, info):
    columns = [
        status_column("org_id"),
        status_column("org_name"),
        status_column("user_id"),
        status_column("share_name"),
        status_column("share_url"),
        status_column("access_level"),
        status_column("parent_org_name"),
        status_column("parent_org_id"),
        status_column("roles"),
    ]

    return format_table(ctx, info, columns)


def list_user_application_access_info(ctx, user_id, org_id=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs = strip_none(kwargs)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    query_results = apiclient.user_api.list_user_application_access_info(
        org_id=org_id, user_id=user_id, **kwargs
    )
    return query_results.user_application_access_info


def list_user_fileshare_access_info(ctx, user_id, org_id=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    kwargs = strip_none(kwargs)
    query_results = apiclient.user_api.list_user_file_share_access_info(
        org_id=org_id, user_id=user_id, **kwargs
    )
    return query_results.user_file_share_access_info


def format_user_resource_access_info_as_text(ctx, info):
    columns = [
        status_column("org_id"),
        status_column("org_name"),
        status_column("user_id"),
        status_column("resource_type"),
        status_column("resource_name"),
        status_column("access_level"),
        status_column("parent_org_name"),
        status_column("parent_org_id"),
        status_column("roles"),
    ]

    return format_table(ctx, info, columns)


def list_user_desktop_access_info(ctx, user_id, org_id=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)

    desktop_type = kwargs.get("desktop_type", object())
    if desktop_type is None:
        kwargs.pop("desktop_type")

    kwargs = strip_none(kwargs)
    query_results = apiclient.user_api.list_desktop_access_info(
        org_id=org_id, user_id=user_id, **kwargs
    )
    return query_results.user_desktop_access_info


def format_user_desktop_access_info_as_text(ctx, info):
    columns = [
        status_column("org_id"),
        status_column("org_name"),
        status_column("user_id"),
        status_column("resource_name"),
        status_column("desktop_type"),
        status_column("access_level"),
        status_column("parent_org_name"),
        status_column("parent_org_id"),
        status_column("roles"),
        status_column("resource_uri"),
        status_column("remote_app.is_remote_app", out_name="is_remote_app"),
    ]

    return format_table(ctx, info, columns)


def list_user_resource_access_info(ctx, user_id, org_id=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)

    kwargs = strip_none(kwargs)
    query_results = apiclient.user_api.list_user_resource_access_info(
        org_id=org_id, user_id=user_id, **kwargs
    )
    return query_results.user_resource_access_info


def format_user_requests_as_text(ctx, info):
    columns = [
        metadata_column("id"),
        spec_column("org_id"),
        spec_column("user_id"),
        status_column("email"),
        spec_column("requested_resource", "resource"),
        spec_column("requested_sub_resource", "sub_resource"),
        spec_column("requested_resource_type", "type"),
        spec_column("state"),
        status_column("challenge_id"),
    ]

    return format_table(ctx, info, columns)


def list_user_requests(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs = strip_none(kwargs)
    query_results = apiclient.user_api.list_user_requests(**kwargs)
    return query_results.user_requests


def _get_user_request(apiclient, request_id, user_id=None, org_id=None):
    return apiclient.user_api.get_user_request(
        request_id, user_id=user_id, org_id=org_id
    )


def add_user_request(
    ctx, user_id, org_id, requested_resource, requested_resource_type, **kwargs
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs = strip_none(kwargs)
    spec = agilicus.UserRequestInfoSpec(
        user_id=user_id,
        org_id=org_id,
        requested_resource=requested_resource,
        requested_resource_type=requested_resource_type,
        **kwargs,
    )
    model = agilicus.UserRequestInfo(spec=spec)
    return apiclient.user_api.create_user_request(model).to_dict()


def update_user_request(ctx, user_request_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["user_id"] = input_helpers.get_user_id_from_input_or_ctx(ctx, **kwargs)
    input_helpers.update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    model = _get_user_request(
        apiclient, user_request_id, user_id=kwargs["user_id"], org_id=kwargs["org_id"]
    )
    model.spec = build_updated_model(agilicus.UserRequestInfoSpec, model.spec, kwargs)
    return apiclient.user_api.replace_user_request(
        user_request_id, user_request_info=model
    ).to_dict()


def action_user_request(ctx, user_request_id, state, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    input_helpers.update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    model = _get_user_request(apiclient, user_request_id, org_id=kwargs["org_id"])
    kwargs["state"] = state
    model.spec = build_updated_model(agilicus.UserRequestInfoSpec, model.spec, kwargs)
    return apiclient.user_api.update_user_request(
        user_request_id, user_request_info=model
    ).to_dict()


def bulk_action_user_request(
    ctx, user_id, state, org_id, user_status, reset_user, **kwargs
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = input_helpers.get_org_from_input_or_ctx(ctx, org_id)
    kwargs = strip_none(kwargs)
    requests = []
    if state is not None:
        query_results = []
        reqs = apiclient.user_api.list_access_requests(
            user_id=user_id, org_id=org_id, request_state="pending"
        ).access_requests
        for req in reqs:
            query_results.extend(req.status.user_requests)
        for result in query_results:
            result.spec.state = state
        requests = query_results
    user_updates = []
    if user_status is not None:
        update = agilicus.UserRequestUserUpdate(
            user_id=user_id,
            org_id=org_id,
            new_status=agilicus.UserStatusEnum(user_status),
            reset_permissions=reset_user,
        )
        user_updates.append(update)

    approval = agilicus.BulkUserRequestApproval(
        org_id=org_id, user_updates=user_updates, user_requests=requests
    )
    return apiclient.user_api.bulk_approve_requests(approval).to_dict()


def show_user_request(ctx, user_request_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["user_id"] = input_helpers.get_user_id_from_input_or_ctx(ctx, **kwargs)
    input_helpers.update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    return _get_user_request(
        apiclient, user_request_id, user_id=kwargs["user_id"], org_id=kwargs["org_id"]
    ).to_dict()


def delete_user_request(ctx, user_request_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["user_id"] = input_helpers.get_user_id_from_input_or_ctx(ctx, **kwargs)
    input_helpers.update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    return apiclient.user_api.delete_user_request(user_request_id, **kwargs)


def list_access_requests(ctx, org_id=None, **kwargs):
    org_id = input_helpers.get_org_from_input_or_ctx(ctx, org_id=org_id, **kwargs)
    apiclient = context.get_apiclient_from_ctx(ctx)
    input_helpers.pop_item_if_none(kwargs)
    query_results = apiclient.user_api.list_access_requests(org_id, **kwargs)
    return query_results.access_requests


def format_user_metadata_as_text(ctx, info):
    columns = [
        metadata_column("id"),
        spec_column("name"),
        spec_column("user_id"),
        spec_column("org_id"),
        spec_column("app_id"),
        spec_column("data_type"),
        spec_column("data"),
    ]

    return format_table(ctx, info, columns)


def _get_user_metadata(apiclient, request_id, user_id=None, org_id=None, **kwargs):
    return apiclient.user_api.get_user_metadata(
        request_id, user_id=user_id, org_id=org_id
    )


def list_user_metadata(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    input_helpers.pop_item_if_none(kwargs)
    query_results = apiclient.user_api.list_user_metadata(**kwargs)
    return query_results.user_metadata


def add_user_metadata(ctx, user_id, org_id, data_type, data, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs = strip_none(kwargs)
    spec = agilicus.UserMetadataSpec(
        user_id=user_id,
        org_id=org_id,
        data_type=data_type,
        data=data,
        **kwargs,
    )
    model = agilicus.UserMetadata(spec=spec)
    return apiclient.user_api.create_user_metadata(model).to_dict()


def update_user_metadata(ctx, user_metadata_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["user_id"] = input_helpers.get_user_id_from_input_or_ctx(ctx, **kwargs)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs = strip_none(kwargs)
    model = _get_user_metadata(apiclient, user_metadata_id, **kwargs)
    model.spec = build_updated_model(agilicus.UserMetadataSpec, model.spec, kwargs)
    return apiclient.user_api.replace_user_metadata(
        user_metadata_id, user_metadata=model
    ).to_dict()


def show_user_metadata(ctx, user_metadata_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["user_id"] = input_helpers.get_user_id_from_input_or_ctx(ctx, **kwargs)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs = strip_none(kwargs)
    return _get_user_metadata(apiclient, user_metadata_id, **kwargs).to_dict()


def delete_user_metadata(ctx, user_metadata_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["user_id"] = input_helpers.get_user_id_from_input_or_ctx(ctx, **kwargs)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs = strip_none(kwargs)
    return apiclient.user_api.delete_user_metadata(user_metadata_id, **kwargs)


def bulk_set_user_metadata(ctx, org_id, data_type, data, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    model = agilicus.BulkUserMetadata(
        org_id=org_id,
        data_type=data_type,
        data=data,
        **kwargs,
    )
    return apiclient.user_api.bulk_update_metadata(bulk_user_metadata=model)


def format_service_account_as_text(ctx, info):
    columns = [
        metadata_column("id"),
        spec_column("name"),
        spec_column("org_id"),
        spec_column("enabled"),
        spec_column("allowed_sub_orgs"),
        spec_column("protected_by_id", optional=True),
        status_column("user"),
    ]

    return format_table(ctx, info, columns)


def _get_service_account(apiclient, request_id, org_id=None, **kwargs):
    return apiclient.user_api.get_service_account(request_id, org_id=org_id)


def list_service_accounts(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    input_helpers.pop_item_if_none(kwargs)
    query_results = apiclient.user_api.list_service_accounts(**kwargs)
    return query_results.service_accounts


def add_service_account(ctx, org_id, name, **kwargs):
    handle_inheritable_configs(kwargs)

    apiclient = context.get_apiclient_from_ctx(ctx)
    spec = agilicus.ServiceAccountSpec(
        org_id=org_id,
        name=name,
        **input_helpers.strip_none(kwargs),
    )
    model = agilicus.ServiceAccount(spec=spec)
    return apiclient.user_api.create_service_account(model).to_dict()


def update_service_account(ctx, service_account_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    handle_inheritable_configs(kwargs)

    model = _get_service_account(apiclient, service_account_id, **kwargs)
    model.spec = build_updated_model(agilicus.ServiceAccountSpec, model.spec, kwargs)

    return apiclient.user_api.replace_service_account(
        service_account_id, service_account=model
    ).to_dict()


def show_service_account(ctx, service_account_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    return _get_service_account(apiclient, service_account_id, **kwargs).to_dict()


def delete_service_account(ctx, service_account_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    return apiclient.user_api.delete_service_account(service_account_id, **kwargs)


def list_org_user_roles(ctx, paginate=True, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs["user_id"] = get_user_id_from_input_or_ctx(ctx, **kwargs)

    query_results = apiclient.user_api.list_org_user_roles(**kwargs)
    results = []
    results.extend(query_results.org_user_roles)

    if paginate:
        while query_results.org_user_roles:
            kwargs["offset"] = query_results.offset
            query_results = apiclient.user_api.list_org_user_roles(**kwargs)
            results.extend(query_results.org_user_roles)

    return results


def format_org_user_roles(ctx, data):
    columns = [
        mapped_column("user_id", "user id"),
        mapped_column("org_id", "org id"),
        column("application"),
        column("role"),
    ]
    return format_table(ctx, data, columns)


def simulate_upstream_group_reconcile(ctx, mapping, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs["user_id"] = get_user_id_from_input_or_ctx(ctx, **kwargs)
    model = agilicus.UpstreamGroupReconcile(mapping=mapping, **kwargs)
    return apiclient.groups_api.create_upstream_group_reconcile_sim(model).to_dict()


def run_upstream_group_reconcile(ctx, mapping, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs["user_id"] = get_user_id_from_input_or_ctx(ctx, **kwargs)
    model = agilicus.UpstreamGroupReconcile(mapping=mapping, **kwargs)
    return apiclient.groups_api.create_upstream_group_reconcile(model).to_dict()


def show_org_usage_metrics(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    return apiclient.org_api.get_usage_metrics(org_id=org_id).metrics


def list_user_ssh_access_info(ctx, user_id, org_id=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    kwargs = strip_none(kwargs)
    query_results = apiclient.user_api.list_ssh_access_info(
        org_id=org_id, user_id=user_id, **kwargs
    )
    return query_results.user_ssh_access_info


def get_user_ssh_access_info(ctx, user_id, org_id=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    kwargs = strip_none(kwargs)
    return apiclient.user_api.list_user_access_info(
        org_id=org_id, user_id=user_id, _return_http_data_only=False, **kwargs
    )


def format_user_ssh_access_info_as_text(ctx, info):
    columns = [
        status_column("org_id"),
        status_column("org_name"),
        status_column("user_id"),
        status_column("resource_name"),
        status_column("access_level"),
        status_column("parent_org_name"),
        status_column("parent_org_id"),
        status_column("roles"),
        status_column("resource_uri"),
    ]

    return format_table(ctx, info, columns)


def list_user_launcher_access_info(ctx, user_id, org_id=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    kwargs = strip_none(kwargs)

    query_results = apiclient.user_api.list_user_launcher_access_info(
        org_id=org_id, user_id=user_id, **kwargs
    )
    return query_results.user_launcher_access_info


def format_user_launcher_access_info_as_text(ctx, info):
    columns = [
        status_column("org_id"),
        status_column("org_name"),
        status_column("user_id"),
        status_column("resource_name"),
        status_column("access_level"),
        status_column("parent_org_name"),
        status_column("parent_org_id"),
        status_column("roles"),
        status_column("resource_uri"),
    ]

    return format_table(ctx, info, columns)


def list_user_orgs(ctx, user_id=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    user_id = get_user_id_from_input_or_ctx(ctx, user_id=user_id)
    kwargs = strip_none(kwargs)

    result = apiclient.user_api.list_all_user_orgs(user_id=user_id, **kwargs).orgs
    return result


def format_user_orgs(ctx, orgs):
    columns = [
        column("id"),
        column("organisation", "name"),
        column("status.current_state", "state"),
    ]

    return format_table(ctx, orgs, columns)


def list_user_guids(ctx, page_size=100, **kwargs):
    client = context.get_apiclient_from_ctx(ctx)
    kwargs = strip_none(kwargs)

    return get_many_entries(
        client.user_api.list_user_guid_mapping,
        "guid_to_name_list",
        maximum=kwargs.get("limit", None),
        page_size=page_size,
        **kwargs,
    )


def format_support_request_as_text(ctx, info):
    columns = [
        metadata_column("id"),
        metadata_column("created"),
        metadata_column("updated"),
        spec_column("supporting_user_email"),
        spec_column("org_id"),
        spec_column("supporting_user_org_id"),
        spec_column("expiry"),
        spec_column("admin_state"),
        status_column("supporting_user_id"),
        status_column("support_request_group"),
        status_column("acknowledgements"),
    ]

    return format_table(ctx, info, columns)


def _get_support_request(apiclient, request_id, org_id=None, **kwargs):
    return apiclient.user_api.get_support_request(request_id, org_id=org_id)


def list_support_requests(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    if kwargs.get("supporting_user_org_id", None) is None:
        update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    input_helpers.pop_item_if_none(kwargs)
    query_results = apiclient.user_api.list_support_requests(**kwargs)
    return query_results.support_requests


def create_support_request(ctx, org_id=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    token = context.get_token(ctx)
    if org_id is None:
        org_id = context.get_org_id(ctx, token)
    spec = agilicus.SupportRequestSpec(
        org_id=org_id,
        **input_helpers.strip_none(kwargs),
    )
    model = agilicus.SupportRequest(spec=spec)
    return apiclient.user_api.create_support_request(model).to_dict()


def update_support_request(ctx, support_request_id, expiry=None, **kwargs):
    if not input_helpers.is_tz_aware(expiry):
        expiry = expiry.astimezone(datetime.timezone.utc)
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    handle_inheritable_configs(kwargs)

    model = _get_support_request(apiclient, support_request_id, **kwargs)
    kwargs = strip_none(kwargs)
    kwargs["expiry"] = expiry
    model.spec = build_updated_model(
        agilicus.SupportRequestSpec, model.spec, kwargs, False
    )

    return apiclient.user_api.update_support_request(
        support_request_id, support_request=model
    ).to_dict()


def show_support_request(ctx, support_request_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    return _get_support_request(apiclient, support_request_id, **kwargs).to_dict()


def delete_support_request(ctx, support_request_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    return apiclient.user_api.delete_support_request(support_request_id, **kwargs)


def create_support_request_message(
    ctx, target_user_id, target_org_id, duration=86400, **kwargs
):
    token = context.get_token(ctx)
    org_id = context.get_org_id(ctx, token)
    user_id = get_user_id_from_input_or_ctx(ctx, **kwargs)
    apiclient = context.get_apiclient_from_ctx(ctx)
    body = agilicus.SupportRequestMessage(
        user_id=user_id,
        org_id=org_id,
        target_user_id=target_user_id,
        target_org_id=target_org_id,
        duration=duration,
        **input_helpers.strip_none(kwargs),
    )
    return apiclient.user_api.create_support_request_message(body)


def format_support_request_acknowledgement_as_text(ctx, info):
    columns = [
        metadata_column("id"),
        metadata_column("created"),
        metadata_column("updated"),
        spec_column("supporting_user_id"),
        spec_column("support_request_id"),
        spec_column("org_id"),
        status_column("supporting_user_email"),
        status_column("expiry"),
    ]
    return format_table(ctx, info, columns)


def _get_support_request_acknowledgement(
    apiclient, acknowledgement_id, org_id=None, **kwargs
):
    return apiclient.user_api.get_support_request_acknowledgement(
        acknowledgement_id, org_id=org_id
    )


def list_support_request_acknowledgements(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    input_helpers.pop_item_if_none(kwargs)
    query_results = apiclient.user_api.list_support_request_acknowledgements(**kwargs)
    return query_results.support_request_acknowledgements


def create_support_request_acknowledgement(
    ctx, org_id=None, supporting_user_id=None, support_request_id=None, **kwargs
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, org_id)
    spec = agilicus.SupportRequestAcknowledgementSpec(
        org_id=org_id,
        supporting_user_id=supporting_user_id,
        support_request_id=support_request_id,
        **input_helpers.strip_none(kwargs),
    )
    model = agilicus.SupportRequestAcknowledgement(spec=spec)
    return apiclient.user_api.create_support_request_acknowledgement(model).to_dict()


def show_support_request_acknowledgement(
    ctx, support_request_acknowledgement_id, **kwargs
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    return _get_support_request_acknowledgement(
        apiclient, support_request_acknowledgement_id, **kwargs
    ).to_dict()


def delete_support_request_acknowledgement(
    ctx, support_request_acknowledgement_id, **kwargs
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return apiclient.user_api.delete_support_request_acknowledgement(
        support_request_acknowledgement_id, **kwargs
    )


def list_org_upstream_user_identities(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    query_results = apiclient.user_api.list_org_upstream_user_identity(**kwargs)
    if query_results:
        return query_results.org_upstream_user_identities
    return []
