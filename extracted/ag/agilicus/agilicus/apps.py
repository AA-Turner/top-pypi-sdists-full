import os
import json
import urllib.parse
import agilicus
import requests

from . import context, response
from .general_helpers import find_item
from .input_helpers import (
    build_alternate_mode_setting,
    build_updated_model,
    get_org_from_input_or_ctx,
    strip_none,
    update_org_from_input_or_ctx,
    update_if_not_none,
)

from .output.table import (
    spec_column,
    format_table,
    column,
    metadata_column,
    status_column,
    subtable,
)


CONNECTION_MAPPING_OPTS = ("default", "one-to-one")


def _prepare_for_put(application):
    application.pop("id", None)
    application.pop("created", None)
    application.pop("updated", None)
    if "environments" in application:
        for env in application["environments"]:
            env.pop("application_services", None)


def query(
    ctx,
    org_id=None,
    maintained=None,
    updated_since=None,
    assigned=None,
    owned=None,
    **kwargs,
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)

    params = {}

    if org_id is not None:
        params["org_id"] = org_id
    if maintained is not None:
        params["maintained"] = maintained
    if assigned is not None:
        params["assigned"] = assigned
    if owned is not None:
        params["owned"] = owned
    if updated_since:
        params["updated_since"] = updated_since

    kwargs = strip_none(kwargs)
    params.update(kwargs)

    params["show_status"] = True

    query_results = apiclient.application_api.list_applications(**params)
    return query_results.applications


def format_apps_for_garbage_collection(ctx, issuers):
    columns = [
        column("id"),
        column("name"),
        column("org_id"),
        column("created"),
        column("updated"),
    ]
    return format_table(ctx, issuers, columns)


def get_app(ctx, org_id, application, **kwargs):
    for app in query(ctx, org_id, **kwargs):
        if app.id == application or app.name == application:
            return app.to_dict()


def _get_env_from_list(environments, name):
    for env in environments:
        if env["name"] == name:
            return env


def env_query(ctx, org_id, application, **kwargs):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)

    params = {}

    if org_id:
        params["org_id"] = org_id
    else:
        org_id = context.get_org_id(ctx, token)
        if org_id:
            params["org_id"] = org_id
    envs = []
    app = get_app(ctx, org_id, application)
    if not app:
        return envs
    environments = app.get("environments", envs)
    assignments = app.get("assignments", [])
    for assignment in assignments:
        _env = _get_env_from_list(environments, assignment["environment_name"])
        #  org = orgs.get(ctx, assignment['org_id'])
        _assignments = _env.get("assignments", [])
        _assignments.append(assignment["org_id"])
        # _assignments.append(org['organisation'])
        _env["assignments"] = _assignments
    return environments


def delete(ctx, id, org_id=None, **kwargs):
    token = context.get_token(ctx)

    params = {}
    if org_id:
        params["org_id"] = org_id
    else:
        org_id = context.get_org_id(ctx, token)
        if org_id:
            params["org_id"] = org_id
    query = urllib.parse.urlencode(params)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)

    uri = "/v2/applications/{}?{}".format(id, query)
    response = requests.delete(
        context.get_api(ctx) + uri,
        headers=headers,
        verify=context.get_cacert(ctx),
    )
    return response.text


def add(ctx, name, org_id, category, name_slug, **kwargs):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)

    application = {}
    application["name"] = name
    application["org_id"] = org_id
    application["category"] = category

    if name_slug is not None:
        application["name_slug"] = name_slug

    update_if_not_none(application, kwargs)
    uri = "/v2/applications"
    response = requests.post(
        context.get_api(ctx) + uri,
        headers=headers,
        json=application,
        verify=context.get_cacert(ctx),
    )
    return response.text


def add_role(ctx, id, role_name):
    token = context.get_token(ctx)

    application = json.loads(get(ctx, id))
    # We can't put the id
    del application["id"]
    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)

    roles = application.get("roles")
    _prepare_for_put(application)

    if not find_item(roles, "name", role_name):
        roles.append({"name": role_name, "rules": []})

    uri = "/v2/applications/{}".format(id)
    resp = requests.put(
        context.get_api(ctx) + uri,
        headers=headers,
        json=application,
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return resp.text


def add_definition(ctx, id, key, path):
    token = context.get_token(ctx)

    application = json.loads(get(ctx, id))
    # We can't put the id
    del application["id"]
    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)

    definitions = application.get("definitions")
    definition = find_item(definitions, "key", key)
    if not definition:
        definition = {"key": key}
        definitions.append(definition)

    definition["value"] = path

    uri = "/v2/applications/{}".format(id)
    resp = requests.put(
        context.get_api(ctx) + uri,
        headers=headers,
        json=application,
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return resp.text


def _build_rule(
    rules,
    name,
    method,
    path,
    query_parameters: list,
    json_pointers: list,
    host=None,
    rule_name=None,
):
    rule = {}
    rule["name"] = name
    if host:
        rule["host"] = host
    rule["method"] = method
    rule["path"] = path
    rendered_params = []
    if query_parameters:
        for name, exact_match, match_type in query_parameters:
            rendered_params.append(
                {"name": name, "exact_match": exact_match, "match_type": match_type}
            )
        rule["query_parameters"] = rendered_params

    if json_pointers:
        body = rule.setdefault("body", {})
        json_pointer = body.setdefault("json", [])
        for pointer in json_pointers:
            json_pointer.append(
                {
                    "pointer": pointer[0],
                    "exact_match": pointer[1],
                    "name": str(len(json_pointer) + 1),
                    "match_type": "string",
                }
            )
        rule["body"] = body

    for existing_rule in rules:
        if existing_rule["name"] == name:
            rules.remove(existing_rule)

    return rule


def add_rule(
    ctx,
    app_name,
    role_name,
    method,
    path,
    query_parameters: list,
    json_pointers: list,
    rule_name=None,
    host=None,
    org_id=None,
):
    token = context.get_token(ctx)

    if not org_id:
        org_id = context.get_org_id(ctx, token)

    application = get_app(ctx, org_id, app_name)
    if not application:
        raise Exception(f"Application {app_name} not found")

    id = application["id"]
    # We can't put the id
    del application["id"]
    del application["created"]
    if "updated" in application:
        del application["updated"]
    # This is rather gross. We can't put the application_services
    # into the put request since it is read-only
    if "environments" in application:
        for env in application["environments"]:
            if "application_services" in env:
                del env["application_services"]

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)

    roles = application.get("roles")
    role = find_item(roles, "name", role_name)
    if not role:
        # Maybe we should not handle this case...
        role = {"name": role_name, "rules": []}
        roles.append(role)

    rules = role["rules"]
    if not rule_name:
        rule_name = str(len(rules) + 1)

    new_rule = _build_rule(
        rules,
        rule_name,
        method,
        path,
        query_parameters,
        json_pointers,
        host,
        rule_name,
    )
    rules.append(new_rule)

    uri = "/v2/applications/{}".format(id)
    resp = requests.put(
        context.get_api(ctx) + uri,
        headers=headers,
        json=application,
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return resp.text


def delete_rule(ctx, app, role_name, rule_name, org_id=None):
    token = context.get_token(ctx)

    if not org_id:
        org_id = context.get_org_id(ctx, token)

    application = get_app(ctx, org_id, app)
    if not application:
        raise Exception(f"Application {app} not found")

    _roles = []
    for role in application.get("roles", []):
        _rules = role.get("rules", [])
        if role["name"] == role_name:
            _update_rules = []
            for rule in _rules:
                if rule["name"] == rule_name:
                    continue
                _update_rules.append(rule)
            _rules = _update_rules
        role["rules"] = _rules
        _roles.append(role)
    application["roles"] = _roles

    id = application["id"]
    # We can't put the id
    del application["id"]
    del application["created"]
    if "updated" in application:
        del application["updated"]
    # This is rather gross. We can't put the application_services
    # into the put request since it is read-only
    if "environments" in application:
        for env in application["environments"]:
            if "application_services" in env:
                del env["application_services"]

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    uri = "/v2/applications/{}".format(id)
    resp = requests.put(
        context.get_api(ctx) + uri,
        headers=headers,
        json=application,
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return resp.text


def get_roles(ctx, app, org_id=None):
    token = context.get_token(ctx)

    if not org_id:
        org_id = context.get_org_id(ctx, token)

    _app = get_app(ctx, org_id, app)
    if not _app:
        raise Exception(f"Application {app} not found")

    _roles = _app.get("roles", [])
    for _role in _roles:
        _role["rules"] = sorted(_role["rules"], key=lambda k: k["name"])
    return _roles


def _get(ctx, id, org_id=None):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)

    uri = "/v2/applications/{}".format(id)
    if org_id:
        uri = f"{uri}?org_id={org_id}"
    else:
        org_id = context.get_org_id(ctx, token)
        if org_id:
            uri = f"{uri}?org_id={org_id}"

    resp = requests.get(
        context.get_api(ctx) + uri,
        headers=headers,
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return resp.json()


def get(ctx, id, **kwargs):
    return json.dumps(_get(ctx, id, **kwargs))


def get_env(ctx, application, env_name, org_id=None, **kwargs):
    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)

    app = get_app(ctx, org_id, application)
    if app is None:
        raise Exception(
            f"No such application found: org:{org_id}, app_name:{application}"
        )
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.application_api.get_environment(
        app["id"], env_name, org_id
    ).to_dict()


def update_application_cors_config(
    cors,
    http_cors_allow_resource_origins=None,
    http_cors_allow_origins=None,
    http_cors_allow_methods=None,
    http_cors_allow_headers=None,
    http_cors_enabled=None,
    http_cors_origin_matching=None,
    http_cors_mode=None,
    http_cors_expose_headers=None,
    http_cors_max_age_seconds=None,
    http_cors_allow_credentials=None,
):
    if http_cors_allow_resource_origins is not None:
        cors["allow_resource_origins"] = http_cors_allow_resource_origins

    cors.setdefault("allow_origins", [])
    if http_cors_allow_origins is not None:
        cors["allow_origins"] = http_cors_allow_origins

    cors.setdefault("allow_methods", [])
    if http_cors_allow_methods is not None:
        cors["allow_methods"] = http_cors_allow_methods

    cors.setdefault("allow_headers", [])
    if http_cors_allow_headers is not None:
        cors["allow_headers"] = http_cors_allow_headers

    cors.setdefault("enabled", False)
    if http_cors_enabled is not None:
        cors["enabled"] = http_cors_enabled

    cors.setdefault("origin_matching", "me")
    if http_cors_origin_matching is not None:
        cors["origin_matching"] = http_cors_origin_matching

    cors.setdefault("mode", "overwrite")
    if http_cors_mode is not None:
        cors["mode"] = http_cors_mode

    cors.setdefault("expose_headers", [])
    if http_cors_expose_headers is not None:
        cors["expose_headers"] = http_cors_expose_headers

    cors.setdefault("max_age_seconds", 3600)
    if http_cors_max_age_seconds is not None:
        cors["max_age_seconds"] = http_cors_max_age_seconds

    cors.setdefault("allow_credentials", False)
    if http_cors_allow_credentials is not None:
        cors["allow_credentials"] = http_cors_allow_credentials


def update_application_auth_config(
    auth,
    auth_enabled=None,
    auth_issuer=None,
    auth_redirect_after_signin_path=None,
    auth_redirect_subpath=None,
):

    if auth_enabled is not None:
        auth["auth_enabled"] = auth_enabled

    if auth_issuer is not None:
        auth["issuer"] = auth_issuer

    if auth_redirect_after_signin_path is not None:
        auth["redirect_after_signin_path"] = auth_redirect_after_signin_path

    if auth_redirect_subpath is not None:
        auth["redirect_subpath"] = auth_redirect_subpath


def update_application_configs(
    config,
    additional_include_user_context_headers=None,
    security_http_cors_allow_resource_origins=None,
    security_http_cors_enabled=None,
    security_http_cors_allow_origins=None,
    security_http_cors_allow_methods=None,
    security_http_cors_allow_headers=None,
    security_http_cors_origin_matching=None,
    security_http_cors_mode=None,
    security_http_cors_expose_headers=None,
    security_http_cors_max_age_seconds=None,
    security_http_cors_allow_credentials=None,
    oidc_config_auth_enabled=None,
    authentication_config_application_handles_authentication=None,
    authentication_config_upstream_ntlm_passthrough=None,
    oidc_config_auth_issuer=None,
    oidc_config_auth_redirect_after_signin_path=None,
    oidc_config_auth_redirect_subpath=None,
    oidc_config_recursive_replace=None,
    oidc_config_domain_path_replacement=None,
    oidc_proxy_header_response_replace=None,
    oidc_proxy_header_request_replace=None,
    oidc_config_rewrite_set_cookie=None,
    oidc_config_rewrite_cookie=None,
    **kwargs,
):
    additional_context = config.setdefault("additional_context", {})
    security = config.setdefault("security", {})
    http = security.setdefault("http", {})
    cors = http.setdefault("cors", {})
    oidc_config = config.setdefault("oidc_config", {})
    auth = oidc_config.setdefault("auth", {})
    authentication_config = config.setdefault("authentication_config", {})

    if additional_include_user_context_headers is not None:
        additional_context["include_user_context_headers"] = (
            additional_include_user_context_headers
        )

    update_application_cors_config(
        cors,
        http_cors_allow_resource_origins=security_http_cors_allow_resource_origins,
        http_cors_allow_origins=security_http_cors_allow_origins,
        http_cors_allow_methods=security_http_cors_allow_methods,
        http_cors_allow_headers=security_http_cors_allow_headers,
        http_cors_enabled=security_http_cors_enabled,
        http_cors_origin_matching=security_http_cors_origin_matching,
        http_cors_mode=security_http_cors_mode,
        http_cors_expose_headers=security_http_cors_expose_headers,
        http_cors_max_age_seconds=security_http_cors_max_age_seconds,
        http_cors_allow_credentials=security_http_cors_allow_credentials,
    )

    update_application_auth_config(
        auth,
        auth_enabled=oidc_config_auth_enabled,
        auth_issuer=oidc_config_auth_issuer,
        auth_redirect_after_signin_path=oidc_config_auth_redirect_after_signin_path,
        auth_redirect_subpath=oidc_config_auth_redirect_subpath,
    )

    update_oidc_standard_headers(
        oidc_config,
        oidc_config_rewrite_set_cookie=oidc_config_rewrite_set_cookie,
        oidc_config_rewrite_cookie=oidc_config_rewrite_cookie,
    )

    if oidc_config_recursive_replace is not None:
        domain_mapping_config = oidc_config.setdefault("domain_mapping", {})
        domain_mapping_config["use_recursive_replacement_system"] = (
            oidc_config_recursive_replace
        )

    if oidc_config_domain_path_replacement is not None:
        headers = oidc_config.setdefault("headers", {})
        domain_substitution = headers.get("domain_substitution", {})
        domain_substitution["path"] = True

    if authentication_config_application_handles_authentication is not None:
        authentication_config["application_handles_authentication"] = (
            authentication_config_application_handles_authentication
        )

    if authentication_config_upstream_ntlm_passthrough is not None:
        upstream_auth = authentication_config.setdefault("upstream", {})
        ntlm = upstream_auth.setdefault("ntlm", {})
        ntlm["ntlm_passthrough"] = authentication_config_upstream_ntlm_passthrough

    if oidc_proxy_header_response_replace:
        headers = oidc_config.setdefault("headers", {})
        header_overrides = headers.setdefault("header_overrides", {})
        response = header_overrides.setdefault("response", {})
        response["replace"] = _build_oidc_header_replace_from_tuple(
            oidc_proxy_header_response_replace
        )

    if oidc_proxy_header_request_replace:
        headers = oidc_config.setdefault("headers", {})
        header_overrides = headers.setdefault("header_overrides", {})
        request = header_overrides.setdefault("request", {})
        request["replace"] = _build_oidc_header_replace_from_tuple(
            oidc_proxy_header_request_replace
        )


def update_oidc_standard_headers(
    cfg,
    oidc_config_rewrite_set_cookie=None,
    oidc_config_rewrite_cookie=None,
):
    headers = cfg.setdefault("headers", {})
    domain_substitution = headers.setdefault("domain_substitution", {})
    standard_headers = domain_substitution.setdefault("standard_headers", {})
    if oidc_config_rewrite_cookie is not None:
        standard_headers["cookie"] = oidc_config_rewrite_cookie

    if oidc_config_rewrite_set_cookie is not None:
        standard_headers["set_cookie_header"] = oidc_config_rewrite_set_cookie


def _build_oidc_header_replace_from_tuple(input_header_replace):
    result = []
    if input_header_replace is None:
        return result
    for input_tuple in input_header_replace:
        replace = agilicus.OIDCProxyHeaderReplace(input_tuple[0], input_tuple[1])
        result.append(replace)
    return result


def update_env(
    ctx,
    id,
    env_name,
    org_id=None,
    version_tag=None,
    config_mount_path=None,
    config_as_mount=None,
    config_as_env=None,
    secrets_mount_path=None,
    secrets_as_mount=None,
    secrets_as_env=None,
    serverless_image=None,
    application_configs={},
    domain_aliases=None,
    name_slug=None,
    proxy_location=None,
    **kwargs,
):
    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)
    apiclient = context.get_apiclient(ctx, token)
    app_env = apiclient.application_api.get_environment(id, env_name, org_id)

    if version_tag is not None:
        app_env.version_tag = version_tag

    if config_mount_path is not None:
        app_env.config_mount_path = config_mount_path

    if config_as_mount is not None:
        app_env.config_as_mount = config_as_mount

    if config_as_env is not None:
        app_env.config_as_env = config_as_env

    if secrets_mount_path is not None:
        app_env.secrets_mount_path = secrets_mount_path

    if secrets_as_mount is not None:
        app_env.secrets_as_mount = secrets_as_mount

    if secrets_as_env is not None:
        app_env.secrets_as_env = secrets_as_env

    if serverless_image is not None:
        app_env.serverless_image = serverless_image

    if application_configs is not None:
        app_env.application_configs = application_configs

    if name_slug is not None:
        app_env.name_slug = name_slug

    if proxy_location is not None:
        app_env.proxy_location = proxy_location

    if kwargs.get("clear_aliases", False):
        app_env.domain_aliases = []

    if domain_aliases:
        app_env.domain_aliases = domain_aliases

    apiclient.application_api.replace_environment(id, env_name, environment=app_env)


def update_env_runtime_status(
    ctx,
    id,
    env_name,
    org_id,
    **kwargs,
):
    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)
    apiclient = context.get_apiclient(ctx, token)

    status = agilicus.RuntimeStatus(org_id=org_id, **kwargs)

    resp = apiclient.application_api.replace_runtime_status(
        id, env_name, runtime_status=status
    )
    return resp


def get_env_runtime_status(
    ctx,
    id,
    env_name,
    org_id=None,
    version_tag=None,
    config_mount_path=None,
    config_as_mount=None,
    config_as_env=None,
    secrets_mount_path=None,
    secrets_as_mount=None,
    secrets_as_env=None,
    serverless_image=None,
    **kwargs,
):
    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)
    apiclient = context.get_apiclient(ctx, token)

    return apiclient.application_api.list_runtime_status(id, env_name, org_id).to_dict()


def add_basic_environment(app_object, env_name, admin_org_id=None):
    environs = app_object.setdefault("environments", [])
    for environ in environs:
        if environ["name"] == env_name:
            return

    environ = {}
    environ["name"] = env_name
    environ["version_tag"] = "latest"
    if admin_org_id:
        environ["maintenance_org_id"] = admin_org_id
    environs.append(environ)


def _remove_env(app_object, env_name):
    environs = app_object.setdefault("environments", [])
    new_environs = []
    for environ in environs:
        if environ["name"] == env_name:
            continue
        else:
            new_environs.append(environ)
    app_object["environments"] = new_environs


def _update_env_assignment(app_object, env_name, org_id, unassign=False):
    assignments = app_object.setdefault("assignments", [])
    update_assignments = []
    for assignment in assignments:
        name = assignment["environment_name"]
        id = assignment["org_id"]
        if name == env_name and id == org_id:
            if unassign:
                continue
            else:
                return
        else:
            update_assignments.append(assignment)

    if not unassign:
        assignment = {}
        assignment["environment_name"] = env_name
        assignment["org_id"] = org_id
        update_assignments.append(assignment)
    app_object["assignments"] = update_assignments


def update_assignment(
    ctx,
    env_name,
    app_id,
    org_id,
    sub_org_id,
    unassign=False,
    admin_org_id=None,
):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)

    application = _get(ctx, app_id, org_id=org_id)
    add_basic_environment(application, env_name, admin_org_id)
    _update_env_assignment(application, env_name, sub_org_id, unassign)
    _prepare_for_put(application)

    uri = f"/v2/applications/{app_id}"
    response = requests.put(
        context.get_api(ctx) + uri,
        headers=headers,
        json=application,
        verify=context.get_cacert(ctx),
    )
    return response.text


def delete_environment(ctx, env_name, app_id, org_id):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)

    application = _get(ctx, app_id, org_id=org_id)
    _remove_env(application, env_name)
    _prepare_for_put(application)

    uri = f"/v2/applications/{app_id}"
    response = requests.put(
        context.get_api(ctx) + uri,
        headers=headers,
        json=application,
        verify=context.get_cacert(ctx),
    )
    return response.text


def update_application(ctx, app_id, org_id, image=None, port=None, **kwargs):
    token = context.get_token(ctx)

    if not org_id:
        org_id = context.get_org_id(ctx, token)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)

    application = _get(ctx, app_id, org_id=org_id)

    if image:
        application["image"] = image
    if port:
        application["port"] = port

    update_if_not_none(application, kwargs)
    _prepare_for_put(application)

    uri = f"/v2/applications/{app_id}"
    resp = requests.put(
        context.get_api(ctx) + uri,
        headers=headers,
        json=application,
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return resp.text


def get_application_services(ctx, org_id=None, **kwargs):
    token = context.get_token(ctx)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, org_id=org_id)
    apiclient = context.get_apiclient(ctx, token)
    params = {}
    update_if_not_none(params, kwargs)
    return apiclient.app_services_api.list_application_services(
        **params,
    ).application_services


def get_application_service(ctx, id, org_id=None, **kwargs):
    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.app_services_api.get_application_service(id, org_id)


def add_application_service(
    ctx, name, hostname, port, org_id=None, ipv4_addresses=None, **kwargs
):
    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)
    apiclient = context.get_apiclient(ctx, token)
    kwargs = strip_none(kwargs)
    if ipv4_addresses:
        ipv4_addresses = ipv4_addresses.split(",")
        kwargs["ipv4_addresses"] = ipv4_addresses

    learning_mode = kwargs.get("learning_mode")
    kwargs.pop("learning_mode", None)
    learning_mode_expiry = kwargs.get("learning_mode_expiry")
    kwargs.pop("learning_mode_expiry", None)
    diagnostic_mode = kwargs.get("diagnostic_mode")
    kwargs.pop("diagnostic_mode", None)

    service = agilicus.ApplicationService(
        name=name,
        org_id=org_id,
        hostname=hostname,
        port=port,
        **kwargs,
    )

    service.alternate_mode_setting = build_alternate_mode_setting(
        None,
        learning_mode=learning_mode,
        learning_mode_expiry=learning_mode_expiry,
        diagnostic_mode=diagnostic_mode,
    )

    return apiclient.app_services_api.create_application_service(service)


def update_application_service(  # noqa: C901
    ctx,
    id,
    name=None,
    hostname=None,
    port=None,
    org_id=None,
    ipv4_addresses=None,
    name_resolution=None,
    protocol=None,
    connector_id=None,
    service_type=None,
    tls_enabled=None,
    tls_verify=None,
    disable_http2=None,
    expose_as_hostname=None,
    learning_mode=None,
    learning_mode_expiry=None,
    port_range=None,
    source_port_override=None,
    source_address_override=None,
    dynamic_source_port_override=None,
    diagnostic_mode=None,
    connector_instance_id=None,
):

    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)
    apiclient = context.get_apiclient(ctx, token)
    service = apiclient.app_services_api.get_application_service(id, org_id)

    if name:
        service.name = name
    if hostname:
        service.hostname = hostname
    if port:
        service.port = port
    if ipv4_addresses:
        service.ipv4_addresses = ipv4_addresses.split(",")
    if name_resolution:
        service.name_resolution = name_resolution
    if protocol:
        service.protocol = protocol
    if connector_id is not None:
        service.connector_id = connector_id
    if connector_instance_id is not None:
        service.connector_instance_id = connector_instance_id
    if service_type:
        service.service_type = service_type
    if tls_enabled is not None:
        service.tls_enabled = tls_enabled
    if tls_verify is not None:
        service.tls_verify = tls_verify
    if disable_http2 is not None:
        if not service.protocol_config:
            service.protocol_config = agilicus.ServiceProtocolConfig()
        if not service.protocol_config.http_config:
            service.protocol_config.http_config = agilicus.ServiceHttpConfig()
        service.protocol_config.http_config.disable_http2 = disable_http2
    if expose_as_hostname is not None:
        if not service.protocol_config:
            service.protocol_config = agilicus.ServiceProtocolConfig()
        if not service.protocol_config.expose_config:
            service.protocol_config.expose_config = agilicus.ServiceExposeConfig()
        service.protocol_config.expose_config.expose_as_hostname = expose_as_hostname

    service.config = _configure_port(service.config, port_range)
    if source_port_override is not None:
        service.config.source_port_override = source_port_override
    if source_address_override is not None:
        service.config.source_address_override = source_address_override
    if dynamic_source_port_override is not None:
        service.config.dynamic_source_port_override = dynamic_source_port_override
    service.alternate_mode_setting = build_alternate_mode_setting(
        service.alternate_mode_setting,
        learning_mode=learning_mode,
        learning_mode_expiry=learning_mode_expiry,
        diagnostic_mode=diagnostic_mode,
    )

    return apiclient.app_services_api.replace_application_service(
        id, application_service=service
    ).to_dict()


def _configure_port(config, port_range):
    if port_range is None:
        return config

    if not config:
        config = agilicus.NetworkServiceConfig()

    config.ports = _parse_ports(port_range)
    return config


def _parse_ports(ports):
    port_ranges = ports.split(",")

    result = []
    for port_range in port_ranges:
        parts = port_range.split("-")
        if len(parts) > 2:
            raise ValueError("each port range must be a or a-b")
        result.append(agilicus.NetworkPortRange(port=agilicus.NetworkPort(port_range)))

    return result


def create_application_service_token(
    ctx,
    id,
    # duration_seconds,
    org_id=None,
):

    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)
    apiclient = context.get_apiclient(ctx, token)
    token = apiclient.app_services_api.create_application_service_token(
        app_service_id=id, org_id=org_id
    )
    return token


def _get_app_service(ctx, org_id, name):
    for _service in get_application_services(ctx, org_id):
        if _service.name == name:
            return _service


def _make_load_balancing(assignment, connection_mapping=None, **kwargs):
    if connection_mapping is None:
        return

    existing_lb = assignment.load_balancing
    if existing_lb is None:
        existing_lb = agilicus.ApplicationServiceLoadBalancing(
            connection_mapping="default"
        )

    existing_lb.connection_mapping = connection_mapping
    return existing_lb


def add_application_service_assignment(
    ctx,
    app_service_name,
    app,
    environment_name,
    org_id=None,
    expose_type=None,
    expose_as_hostname=None,
    **kwargs,
):
    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)
    apiclient = context.get_apiclient(ctx, token)

    service = _get_app_service(ctx, org_id, app_service_name)
    if not service:
        raise Exception(f"Application service {app_service_name} not found")

    _app = get_app(ctx, org_id, app)
    if not _app:
        raise Exception(f"Application {app} not found")

    id = service.id
    assignment = agilicus.ApplicationServiceAssignment(
        app_id=_app["id"],
        environment_name=environment_name,
        org_id=_app["org_id"],
        expose_type=expose_type,
    )
    if expose_as_hostname:
        if assignment.expose_as_hostnames is None:
            assignment.expose_as_hostnames = []
        assignment.expose_as_hostnames.append(agilicus.Domain(expose_as_hostname))

    lb = _make_load_balancing(assignment, **kwargs)
    if lb is not None:
        assignment.load_balancing = lb

    service.assignments.append(assignment)
    return apiclient.app_services_api.replace_application_service(
        id, application_service=service
    ).to_dict()


def delete_application_service_assignment(
    ctx, app_service_name, app, environment_name, org_id=None
):
    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)
    apiclient = context.get_apiclient(ctx, token)

    service = _get_app_service(ctx, org_id, app_service_name)
    if not service:
        raise Exception(f"Application service {app_service_name} not found")

    _app = get_app(ctx, org_id, app)
    if not _app:
        raise Exception(f"Application {app} not found")
    id = service.id
    new_list = []
    for assignment in service.assignments:
        if (
            assignment.app_id == _app["id"]
            and assignment.environment_name == environment_name
            and assignment.org_id == _app["org_id"]
        ):
            pass
        else:
            new_list.append(assignment)

    service.assignments = new_list
    return apiclient.app_services_api.replace_application_service(
        id, application_service=service
    )


def delete_application_service(ctx, name, org_id=None, **kwargs):
    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.app_services_api.delete_application_service(name, org_id)


def update_application_service_assignment(
    ctx,
    app_service_name,
    app,
    environment_name,
    org_id=None,
    expose_type=None,
    expose_as_hostname=None,
    expose_as_hostname_list=None,
    **kwargs,
):
    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)
    apiclient = context.get_apiclient(ctx, token)

    service = _get_app_service(ctx, org_id, app_service_name)
    if not service:
        raise Exception(f"Application service {app_service_name} not found")

    _app = get_app(ctx, org_id, app)
    if not _app:
        raise Exception(f"Application {app} not found")

    found = False
    for assignment in service.assignments:
        if (
            assignment.app_id == _app["id"]
            and assignment.environment_name == environment_name
        ):
            found = True
            break

    id = service.id
    if found:
        if expose_type is not None:
            assignment.expose_type = expose_type
        if expose_as_hostname is not None:
            assignment.expose_as_hostnames.append(agilicus.Domain(expose_as_hostname))
        if expose_as_hostname_list is not None:
            assignment.expose_as_hostnames = [
                agilicus.Domain(hostname) for hostname in expose_as_hostname_list
            ]
        lb = _make_load_balancing(assignment, **kwargs)
        if lb is not None:
            assignment.load_balancing = lb
        return apiclient.app_services_api.replace_application_service(
            id, application_service=service
        ).to_dict()
    else:
        raise Exception("assignment not found")


def format_application_services(ctx, app_services):
    location_columns = [column("hostname")]
    port_columns = [column("ports", optional=True)]
    assigments_columns = [
        column("app_id"),
        column("environment_name"),
        column("assigned_org_ids"),
        column("expose_type"),
        column("expose_as_hostnames"),
    ]

    app_service_columns = [
        column("id"),
        column("name"),
        column("hostname"),
        column("ipv4_addresses", optional=True),
        column("connector_id"),
        column("service_type"),
        subtable(
            ctx, "locations", location_columns, subobject_name="status.routing_info"
        ),
        subtable(ctx, "config", port_columns),
        subtable(ctx, "assignments", assigments_columns),
    ]
    return format_table(ctx, app_services, app_service_columns)


def list_app_rules(ctx, app_id, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs = strip_none(kwargs)
    kwargs["org_id"] = org_id
    query_results = apiclient.application_api.list_rules(app_id, **kwargs)
    if query_results:
        return query_results.rules
    return []


def filter_dict(input, *keys):
    result = {}
    for key in keys:
        name = key
        if type(key) is tuple:
            name = key[1]
            key = key[0]

        if key in input:
            result[name] = input[key]

    return result


def construct_rule_model(app_id, **kwargs):
    methods = kwargs.get("methods", None)
    if methods is not None:
        kwargs["methods"] = list(methods)

    condition = agilicus.HttpRule(
        **filter_dict(kwargs, "rule_type", "methods", "path_regex")
    )

    scope = kwargs.get("rule_scope", None)
    if scope is not None:
        kwargs["rule_scope"] = agilicus.RuleScopeEnum(scope)
    spec = agilicus.RuleSpec(
        app_id=app_id,
        condition=condition,
        **filter_dict(kwargs, "comments", "org_id", ("rule_scope", "scope")),
    )
    model = agilicus.RuleV2(spec=spec)
    return model


def add_http_rule(ctx, app_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs = strip_none(kwargs)
    model = construct_rule_model(app_id, **kwargs)
    return apiclient.application_api.add_rule(app_id, model).to_dict()


def _get_rule_v2(ctx, apiclient, app_id, rule_id, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    return apiclient.application_api.get_rule(app_id, rule_id, org_id=org_id)


def show_rule_v2(ctx, app_id, rule_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return _get_rule_v2(ctx, apiclient, app_id, rule_id, **kwargs).to_dict()


def delete_rule_v2(ctx, app_id, rule_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    return apiclient.application_api.delete_rule(app_id, rule_id, org_id=org_id)


def update_conditions(rule, kwargs):
    updates_to_apply = {}
    updates_to_apply["path_regex"] = kwargs.pop("path_regex", None)
    updates_to_apply["rule_type"] = kwargs.pop("rule_type", None)
    return build_updated_model(agilicus.HttpRule, rule.spec.condition, updates_to_apply)


def _build_rule_query_from_tuple(input_query_params):
    result = []
    if input_query_params is None:
        return result

    for input_tuple in input_query_params:
        query = agilicus.RuleQueryParameter(input_tuple[0])
        query.exact_match = input_tuple[1]
        query.match_type = input_tuple[2]
        result.append(query)
    return result


def update_http_rule(
    ctx, app_id, rule_id, query_params=None, body_params=None, methods=None, **kwargs
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    rule = _get_rule_v2(ctx, apiclient, app_id, rule_id, **kwargs)
    # rule.spec.condition = update_conditions(rule, kwargs)
    # rule.spec = build_updated_model(agilicus.RuleSpec, rule.spec, kwargs)
    rule.spec.condition["query_parameters"] = _build_rule_query_from_tuple(query_params)
    if body_params is not None:
        rule.spec.condition["body"]["json"] = [
            agilicus.RuleQueryBodyJSON(*tup) for tup in body_params
        ]
    if methods is not None:
        rule.spec.condition["methods"] = [method for method in methods]
    return apiclient.application_api.replace_rule(
        app_id, rule_id, rule_v2=rule
    ).to_dict()


def list_combined_rules(ctx, org_id=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    if "app_id" in kwargs and kwargs["app_id"] is None:
        kwargs.pop("app_id")
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id, **kwargs)
    query_results = apiclient.application_api.list_combined_rules(
        org_id=org_id, **kwargs
    )
    if query_results:
        return query_results.combined_rules
    return []


def list_roles(ctx, app_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs = strip_none(kwargs)
    query_results = apiclient.application_api.list_roles(app_id, **kwargs)
    if query_results:
        return query_results.roles
    return []


def add_role_v2(ctx, app_id, name, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    included = kwargs.pop("included", None)
    included_model = None
    if included:
        included_model = [agilicus.IncludedRole(role_id=id) for id in included]
    spec = agilicus.RoleSpec(app_id, name, included=included_model, **kwargs)
    model = agilicus.RoleV2(spec=spec)
    return apiclient.application_api.add_role(app_id, model).to_dict()


def _get_role_by_id(ctx, apiclient, app_id, role_id, **kwargs):
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    return apiclient.application_api.get_role(app_id, role_id, **kwargs)


def show_role_v2(ctx, app_id, role_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return _get_role_by_id(ctx, apiclient, app_id, role_id, **kwargs).to_dict()


def delete_role_v2(ctx, app_id, role_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    return apiclient.application_api.delete_role(app_id, role_id, **kwargs)


def update_role_v2(ctx, app_id, role_id, included=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    role = _get_role_by_id(ctx, apiclient, app_id, role_id)
    role.spec = build_updated_model(agilicus.RoleSpec, role.spec, kwargs)
    if included is not None:
        role.spec.included = [agilicus.IncludedRole(role_id=id) for id in included]
    return apiclient.application_api.replace_role(
        app_id, role_id, role_v2=role
    ).to_dict()


def list_roles_to_rules(ctx, app_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs = strip_none(kwargs)
    query_results = apiclient.application_api.list_role_to_rule_entries(app_id, **kwargs)
    if query_results:
        return query_results.role_to_rule_entries
    return []


def add_role_to_rule(ctx, app_id, role_id, rule_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    spec = agilicus.RoleToRuleEntrySpec(
        app_id=app_id, role_id=role_id, rule_id=rule_id, **kwargs
    )
    model = agilicus.RoleToRuleEntry(spec=spec)
    return apiclient.application_api.add_role_to_rule_entry(app_id, model).to_dict()


def _get_role_to_rule(ctx, apiclient, app_id, role_to_rule_id, **kwargs):
    keyword_args = {}
    update_org_from_input_or_ctx(keyword_args, ctx, **kwargs)
    return apiclient.application_api.get_role_to_rule_entry(
        app_id, role_to_rule_id, **keyword_args
    )


def show_role_to_rule(ctx, app_id, role_to_rule_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return _get_role_to_rule(ctx, apiclient, app_id, role_to_rule_id, **kwargs).to_dict()


def delete_role_to_rule(ctx, app_id, role_to_rule_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    return apiclient.application_api.delete_role_to_rule_entry(
        app_id, role_to_rule_id, **kwargs
    )


def update_role_to_rule(ctx, app_id, role_to_rule_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    mapping = _get_role_to_rule(ctx, apiclient, app_id, role_to_rule_id, **kwargs)

    mapping.spec = build_updated_model(
        agilicus.RoleToRuleEntrySpec, mapping.spec, kwargs
    )
    return apiclient.application_api.replace_role_to_rule_entry(
        app_id, role_to_rule_id, role_to_rule_entry=mapping
    ).to_dict()


def format_application_summaries_as_text(ctx, summaries):
    columns = [
        status_column("application_id"),
        status_column("application_name"),
        status_column("assigned_org_id"),
        status_column("published"),
        status_column("description"),
        status_column("category"),
        status_column("icon_url"),
        status_column("default_role_name"),
        status_column("default_role_id"),
    ]

    return format_table(ctx, summaries, columns)


def list_application_summaries(ctx, org_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs = strip_none(kwargs)
    query_results = apiclient.application_api.list_application_summaries(**kwargs)
    return query_results.application_summaries


def format_secure_agent_as_text(ctx, info):
    app_service_columns = [
        column("id"),
        column("hostname"),
        column("port"),
        column("protocol"),
        column("service_type"),
    ]
    connector_info_columns = [column("connection_uri"), column("max_number_connections")]
    columns = [
        metadata_column("id"),
        spec_column("name"),
        subtable(
            ctx, "application_services", app_service_columns, subobject_name="status"
        ),
        subtable(ctx, "connector_info", connector_info_columns, subobject_name="status"),
    ]

    return format_table(ctx, info, columns)


def list_secure_agents(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    query_results = apiclient.application_api.list_agents(**kwargs)
    return query_results.secure_agents


def add_secure_agent(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    spec = agilicus.SecureAgentSpec(**kwargs)
    model = agilicus.SecureAgent(spec=spec)
    return apiclient.application_api.create_agent(model).to_dict()


def _get_agent(ctx, apiclient, agent_id, **kwargs):
    keyword_args = {}
    update_org_from_input_or_ctx(keyword_args, ctx, **kwargs)
    return apiclient.application_api.get_agent(agent_id, **keyword_args)


def show_secure_agent(ctx, agent_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return _get_agent(ctx, apiclient, agent_id, **kwargs).to_dict()


def delete_secure_agent(ctx, agent_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    return apiclient.application_api.delete_agent(agent_id, **kwargs)


def update_secure_agent(ctx, agent_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    mapping = _get_agent(ctx, apiclient, agent_id, **kwargs)

    mapping.spec = build_updated_model(agilicus.SecureAgentSpec, mapping.spec, kwargs)
    return apiclient.application_api.replace_agent(
        agent_id, secure_agent=mapping
    ).to_dict()


def set_connector_to_agent(ctx, agent_id, connection_uri, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    mapping = _get_agent(ctx, apiclient, agent_id, **kwargs)
    connector, idx = _get_connector_from_agent_or_add(mapping, connection_uri)
    # Not needed for connector config
    kwargs.pop("org_id", None)

    mapping.spec.connectors[idx] = build_updated_model(
        agilicus.SecureAgentConnector, connector, kwargs
    )
    return apiclient.application_api.replace_agent(
        agent_id, secure_agent=mapping
    ).to_dict()


def delete_connector_from_agent(ctx, agent_id, connection_uri, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    mapping = _get_agent(ctx, apiclient, agent_id, **kwargs)
    connector, idx = _get_connector_from_agent(mapping, connection_uri)
    if not connector:
        return mapping.to_dict()

    del mapping.spec.connectors[idx]

    return apiclient.application_api.replace_agent(
        agent_id, secure_agent=mapping
    ).to_dict()


def _get_connector_from_agent(agent, connection_uri):
    for idx, connector in enumerate(agent.spec.connectors):
        if connector.connection_uri == connection_uri:
            return connector, idx
    return None, -1


def _get_connector_from_agent_or_add(agent, connection_uri):
    connector, idx = _get_connector_from_agent(agent, connection_uri)
    if connector:
        return connector, idx

    connector = agilicus.SecureAgentConnector(max_number_connections=1)
    connector.connection_uri = connection_uri
    agent.spec.connectors.append(connector)
    return connector, len(agent.spec.connectors) - 1


def format_usage_metrics(ctx, info):
    measurement_cols = [
        column("peak"),
        column("current"),
    ]
    columns = [
        column("type"),
        column("org_id"),
        subtable(ctx, "provisioned", measurement_cols),
        subtable(ctx, "active", measurement_cols),
    ]

    return format_table(ctx, info, columns)


def show_application_api_usage_metrics(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    return apiclient.application_api.get_all_usage_metrics(org_id=org_id).metrics


def show_application_usage_metrics(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    return apiclient.application_api.get_application_usage_metrics(org_id=org_id)


def show_application_service_usage_metrics(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    return apiclient.app_services_api.get_application_service_usage_metrics(
        org_id=org_id
    )


def show_file_share_usage_metrics(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    return apiclient.app_services_api.get_file_share_usage_metrics(org_id=org_id)


def set_http_config(
    ctx,
    service_id,
    org_id=None,
    set_token_cookie=False,
    rewrite_hostname=False,
    rewrite_hostname_with_port=False,
    rewrite_hostname_override="",
    **kwargs,
):
    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)
    apiclient = context.get_apiclient(ctx, token)

    service = apiclient.app_services_api.get_application_service(service_id, org_id)
    config = service.protocol_config
    if not config:
        service.protocol_config = agilicus.ServiceProtocolConfig()
        config = service.protocol_config

    if not config.http_config:
        config.http_config = agilicus.ServiceHttpConfig()

    config.http_config.set_token_cookie = set_token_cookie
    config.http_config.rewrite_hostname = rewrite_hostname
    config.http_config.rewrite_hostname_with_port = rewrite_hostname_with_port
    config.http_config.rewrite_hostname_override = rewrite_hostname_override

    return apiclient.app_services_api.replace_application_service(
        service_id, application_service=service
    )


def add_js_injection(
    ctx,
    service_id,
    org_id=None,
    inject_script=None,
    **kwargs,
):
    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)
    apiclient = context.get_apiclient(ctx, token)

    service = apiclient.app_services_api.get_application_service(service_id, org_id)
    config = service.protocol_config
    if not config:
        service.protocol_config = agilicus.ServiceProtocolConfig()
        config = service.protocol_config

    if not config.http_config:
        config.http_config = agilicus.ServiceHttpConfig()

    if not config.http_config.js_injections:
        config.http_config.js_injections = []

    js_inject = agilicus.JSInject(**kwargs)
    if inject_script:
        js_inject.inject_script = open(inject_script, "r").read()
        js_inject.script_name = os.path.basename(inject_script)

    config.http_config.js_injections.append(js_inject)

    return apiclient.app_services_api.replace_application_service(
        service_id, application_service=service
    )


def delete_js_injection(
    ctx,
    service_id,
    index,
    org_id=None,
    **kwargs,
):
    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)
    apiclient = context.get_apiclient(ctx, token)

    service = apiclient.app_services_api.get_application_service(service_id, org_id)
    config = service.protocol_config
    if not config:
        return service

    if not config.http_config:
        return service

    if not config.http_config.js_injections:
        return service

    if index > (len(config.http_config.js_injections) - 1):
        raise Exception("No such entry exists")

    del config.http_config.js_injections[index]
    return apiclient.app_services_api.replace_application_service(
        service_id, application_service=service
    )
