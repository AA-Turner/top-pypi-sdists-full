import base64
import json
import urllib.parse
import datetime
import jwt
import sys

import requests
import agilicus
from urllib.parse import urlparse
from .input_helpers import get_org_from_input_or_ctx
from .input_helpers import update_org_from_input_or_ctx
from .input_helpers import get_user_id_from_input_or_ctx
from .input_helpers import build_updated_model
from .input_helpers import strip_none
from .input_helpers import update_if_present
from .pagination import pagination

from .output import output_if_console

from . import context, response
from . import access

from .output.table import (
    spec_column,
    format_table,
    metadata_column,
    status_column,
)

api_key_oper_statuses = [
    "active",
    "disabled",
    "expired",
    "revoked",
]


def _create_token(
    ctx,
    user_id,
    duration,
    aud,
    hosts=[],
    roles={},
    org_id=None,
    scopes=None,
    inherit_session=False,
    create_refresh_token=None,
    get_user=None,
):
    obj = agilicus.CreateTokenRequest(
        sub=user_id,
        time_validity=agilicus.TimeValidity(duration=duration),
        audiences=aud,
        inherit_session=inherit_session,
        org=org_id,
    )
    if hosts:
        obj.hosts = hosts
    if roles:
        obj.roles = roles
    if scopes:
        obj.scopes = scopes
    if create_refresh_token:
        obj.create_refresh_token = create_refresh_token

    if get_user:
        obj.get_user = get_user

    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.tokens_api.create_token(obj)


def get_introspect(
    ctx,
    raw_token,
    exclude_roles=False,
    include_suborgs=False,
    support_http_matchers=True,
    target_domain=None,
    no_cache=False,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    options = agilicus.TokenIntrospectOptions(
        exclude_roles=exclude_roles,
        support_http_matchers=support_http_matchers,
        no_cache=no_cache,
    )

    if target_domain is not None:
        options.target_org_info = agilicus.OrgInfo(target_domain=target_domain)

    token_obj = agilicus.TokenIntrospect(token=raw_token, introspect_options=options)

    if not include_suborgs:
        resp = apiclient.tokens_api.create_introspect_token(
            token_obj, **strip_none(kwargs)
        )
    else:
        resp = apiclient.tokens_api.create_introspect_token_all_sub_orgs(
            token_obj, **strip_none(kwargs)
        )

    return resp


def introspect_self(
    ctx,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.tokens_api.get_token()


def get_token(ctx, user_id, org_id, duration, hosts, aud):
    hosts = json.loads(hosts)
    if not aud:
        aud = [
            "urn:api:agilicus:gateway",
            "urn:api:agilicus:users",
            "urn:api:agilicus:applications",
        ]
    return _create_token(
        ctx,
        user_id,
        duration,
        aud=aud,
        hosts=hosts,
        org_id=org_id,
    )


def create_token(
    ctx,
    user_id,
    roles,
    duration,
    audiences,
    org_id,
    scopes=None,
    inherit_session=False,
    **kwargs,
):
    return _create_token(
        ctx,
        user_id,
        duration,
        aud=audiences,
        roles=roles,
        org_id=org_id,
        scopes=scopes,
        inherit_session=inherit_session,
        **kwargs,
    )


def _get_service_access_token(auth_doc, expiry=None):
    doc_id = auth_doc["metadata"]["id"]
    iss = f"urn:agilicus:authentication_documents:{doc_id}"

    if expiry is None:
        expiry = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    else:
        expiry = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiry)

    token = {
        "audience": "urn:api:agilicus:tokens",
        "issuer": iss,
        "user_id": auth_doc["spec"]["user_id"],
        "org_id": auth_doc["spec"]["org_id"],
        "expiry": str(expiry),
    }

    return jwt.encode(token, key=auth_doc["status"]["key"], algorithm="ES256")


def create_service_token(
    auth_doc, expiry=None, ctx=None, verify=None, scope=None, **kwargs
):
    token = _get_service_access_token(auth_doc, expiry=expiry)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers["Content-type"] = "application/x-www-form-urlencoded"

    update_if_present(headers, "referer", **kwargs)

    data = {}
    data["grant_type"] = "urn:agilicus:params:oauth:grant-type:identity_statement"

    _verify = verify

    if ctx:
        data["client_id"] = context.get_client_id(ctx)
        _verify = context.get_cacert(ctx)

    update_if_present(data, "client_id", **kwargs)
    if scope:
        # space separated list for scopes
        data["scope"] = " ".join(scope)

    data["authentication_document_id"] = auth_doc["metadata"]["id"]
    data["identity_assertion"] = token
    url = auth_doc["spec"]["auth_issuer_url"]
    if url[-1] != "/":
        url += "/"
    resp = requests.post(url + "token", headers=headers, data=data, verify=_verify)
    if resp.status_code >= 400:
        raise Exception(f"Failed to create service token: {resp.text}")
    return json.loads(resp.text)


def query_tokens(
    ctx,
    limit=None,
    expired_from=None,
    expired_to=None,
    issued_from=None,
    issued_to=None,
    org_id=None,
    jti=None,
    sub=None,
    session=None,
):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)

    params = {}
    if limit:
        params["limit"] = limit
    if expired_from:
        params["exp_from"] = expired_from
    if expired_to:
        params["exp_to"] = expired_to
    if issued_from:
        params["iat_from"] = issued_from
    if issued_to:
        params["iat_to"] = issued_to
    if jti:
        params["jti"] = jti
    if sub:
        params["sub"] = sub
    if org_id is not None:
        params["org"] = org_id
    else:
        org_id = context.get_org_id(ctx, token)
        if org_id:
            params["org"] = org_id
    if session is not None:
        params["session"] = session

    query = urllib.parse.urlencode(params)
    uri = "/v1/tokens?{}".format(query)
    resp = requests.get(
        context.get_api(ctx) + uri,
        headers=headers,
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return resp.text


def format_authentication_document_as_text(ctx, info):
    columns = [
        metadata_column("id"),
        spec_column("user_id"),
        spec_column("org_id"),
        spec_column("expiry"),
        status_column("issuer"),
    ]

    return format_table(ctx, info, columns)


def list_authentication_documents(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    query_results = apiclient.tokens_api.list_authentication_documents(
        **strip_none(kwargs)
    )
    return query_results.authentication_documents


def add_authentication_document(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    spec = agilicus.AuthenticationDocumentSpec(**strip_none(kwargs))
    model = agilicus.AuthenticationDocument(spec=spec)
    return apiclient.tokens_api.create_authentication_document(model).to_dict()


def _get_auth_doc(ctx, apiclient, document_id, **kwargs):
    keyword_args = {}
    update_org_from_input_or_ctx(keyword_args, ctx, **kwargs)
    return apiclient.tokens_api.get_authentication_document(document_id, **keyword_args)


def show_authentication_document(ctx, document_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return _get_auth_doc(ctx, apiclient, document_id, **kwargs).to_dict()


def delete_authentication_document(ctx, document_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    return apiclient.tokens_api.delete_authentication_document(
        document_id, **strip_none(kwargs)
    )


def validate_identity_assertion(ctx, document_id, token, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    model = agilicus.IdentityAssertion(
        authentication_document_id=document_id, token=token
    )
    return apiclient.tokens_api.validate_identity_assertion(model).to_dict()


def add_api_key(ctx, duration, scopes, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    user_id = get_user_id_from_input_or_ctx(ctx, **kwargs)
    kwargs["user_id"] = user_id
    kwargs["org_id"] = org_id
    expiry = None
    if duration:
        expiry = datetime.datetime.utcnow() + datetime.timedelta(seconds=duration)

    params = {}
    params["scopes"] = [agilicus.TokenScope(scope) for scope in scopes]
    params["expiry"] = expiry
    params.update(**kwargs)
    spec = agilicus.APIKeySpec(**strip_none(params))
    model = agilicus.APIKey(spec=spec)
    return apiclient.tokens_api.create_api_key(model)


def delete_api_key(ctx, api_key_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs["user_id"] = get_user_id_from_input_or_ctx(ctx, **kwargs)
    return apiclient.tokens_api.delete_api_key(api_key_id, **strip_none(kwargs))


def get_api_key(ctx, api_key_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs["user_id"] = get_user_id_from_input_or_ctx(ctx, **kwargs)
    return apiclient.tokens_api.get_api_key(api_key_id, **strip_none(kwargs))


def list_api_keys(ctx, next_created_date, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs["user_id"] = get_user_id_from_input_or_ctx(ctx, **kwargs)
    kwargs = strip_none(kwargs)
    if next_created_date is not None:
        if next_created_date == "":
            next_created_date = None
        kwargs["page_at_created_date"] = next_created_date
    return apiclient.tokens_api.list_api_keys(**kwargs)


def get_api_key_introspect(ctx, email, api_key, include_suborgs, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    auth_info = agilicus.APIKeyIntrospectAuthorizationInfo(username=email, key=api_key)
    introspect = agilicus.APIKeyIntrospect(
        api_key_auth_info=auth_info, multi_org=include_suborgs
    )
    return apiclient.tokens_api.create_api_key_introspection(introspect)


def replace_api_key(ctx, api_key_id, expiry, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs["user_id"] = get_user_id_from_input_or_ctx(ctx, **kwargs)
    api_key = apiclient.tokens_api.get_api_key(api_key_id, **strip_none(kwargs))
    if expiry is not None:
        api_key["spec"]["expiry"] = expiry
    return apiclient.tokens_api.replace_api_key(api_key_id, api_key)


def format_api_keys_as_text(ctx, api_keys):
    columns = [
        metadata_column("created"),
        metadata_column("id"),
        spec_column("user_id"),
        spec_column("org_id"),
        spec_column("expiry"),
        spec_column("scopes"),
        spec_column("session"),
        status_column("token_id"),
    ]

    return format_table(ctx, api_keys, columns)


def bulk_revoke_token(ctx, user_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    model = agilicus.BulkTokenRevoke(user_id=user_id, **strip_none(kwargs))
    return apiclient.tokens_api.create_bulk_revoke_token_task(model).to_dict()


def add_session(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs["user_id"] = get_user_id_from_input_or_ctx(ctx, **kwargs)
    spec = agilicus.SessionsSpec(**strip_none(kwargs))
    model = agilicus.Session(spec=spec)
    return apiclient.tokens_api.create_session(model)


def update_session(ctx, session_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs["user_id"] = get_user_id_from_input_or_ctx(ctx, **kwargs)
    session = apiclient.tokens_api.get_session(
        session_id, user_id=kwargs["user_id"], org_id=kwargs["org_id"]
    )
    session.spec = build_updated_model(agilicus.SessionsSpec, session.spec, kwargs)
    return apiclient.tokens_api.replace_session(session_id, session=session)


def delete_session(ctx, session_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs["user_id"] = get_user_id_from_input_or_ctx(ctx, **kwargs)
    return apiclient.tokens_api.delete_session(session_id, **strip_none(kwargs))


def get_session(ctx, session_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs["user_id"] = get_user_id_from_input_or_ctx(ctx, **kwargs)
    return apiclient.tokens_api.get_session(session_id, **strip_none(kwargs))


def list_sessions(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs["user_id"] = get_user_id_from_input_or_ctx(ctx, **kwargs)
    return apiclient.tokens_api.list_sessions(**strip_none(kwargs)).sessions


def format_sessions_as_text(ctx, sessions):
    columns = [
        metadata_column("id"),
        spec_column("user_id"),
        spec_column("org_id"),
        spec_column("revoked"),
        spec_column("number_of_logins"),
        spec_column(
            "number_of_failed_multi_factor_challenges", out_name="failed challenges"
        ),
        metadata_column("created"),
        metadata_column("updated"),
    ]

    return format_table(ctx, sessions, columns)


def bulk_revoke_sessions(ctx, user_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    model = agilicus.UserSessionIdentifiers(user_id=user_id, **strip_none(kwargs))
    return apiclient.tokens_api.create_bulk_revoke_session_task(model).to_dict()


def bulk_delete_sessions(ctx, user_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    model = agilicus.UserSessionIdentifiers(user_id=user_id, **strip_none(kwargs))
    return apiclient.tokens_api.create_bulk_delete_session_task(model).to_dict()


def reissue_token(ctx, org_id, original_token):
    apiclient = context.get_apiclient_from_ctx(ctx, token=original_token)
    reissue = agilicus.TokenReissueRequest(token=original_token, org_id=org_id)
    result = apiclient.tokens_api.create_reissued_token(reissue)
    return result.token


def create_user_data_token(ctx, aud=None, user_data=None, duration=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs["user_id"] = get_user_id_from_input_or_ctx(ctx, **kwargs)
    userDataToken = agilicus.CreateUserDataTokenRequest()
    if aud:
        userDataToken.audiences = aud

    if user_data:
        userDataToken.user_data = json.loads(user_data)

    if duration:
        userDataToken.token_validity = agilicus.TokenValidity()
        userDataToken.token_validity.start = datetime.datetime.utcnow()
        userDataToken.token_validity.duration = duration
    return apiclient.tokens_api.create_user_data_token(userDataToken)


class RefreshableAccessToken:
    def __init__(self):
        pass

    def get_token(self, ctx, refresh=None, token_refresh=None):
        token = context.get_value(ctx, "TOKEN")

        if token and access.is_token_expired(token):
            token_refresh = True
        if not token or refresh or token_refresh:
            if token_refresh:
                refresh = True
            access_token = access.get_access_token(ctx, refresh=refresh)
            token = access_token.get()
            ctx.obj["TOKEN"] = token
            context.save(ctx)
        return token


class RefreshableServiceToken(RefreshableAccessToken):
    def __init__(self, ctx, auth_doc, scope_list):
        super().__init__()
        self.issuer = auth_doc.get("spec", {}).get("auth_issuer_url")
        org_id = auth_doc.get("spec", {}).get("org_id")
        ctx.obj["ISSUER"] = self.issuer
        ctx.obj["ORG_ID"] = org_id
        ctx.obj["REFRESHABLE_TOKEN"] = self
        self.auth_doc = auth_doc
        self.scope_list = scope_list
        self.get_token(ctx)

    def get_token(self, ctx, refresh=None, token_refresh=None):
        token = context.get_value(ctx, "TOKEN")

        if token:
            if access.is_token_expired(token):
                token_refresh = True

        if not token or refresh or token_refresh:
            service_token = create_service_token(
                auth_doc=self.auth_doc,
                ctx=ctx,
                scope=self.scope_list,
            )
            token = service_token.get("access_token")
            ctx.obj["TOKEN"] = token
        return token


def create_session_challenge(
    ctx, token=None, open_profile=None, description=None, profile_uri=None, webpush=None
):
    apiclient = context.get_apiclient_from_ctx(ctx, token=token)
    spec = agilicus.SessionChallengeSpec()
    if webpush:
        spec.webpush = webpush

    if description:
        spec.description = description
    body = agilicus.SessionChallenge(spec=spec)
    result = apiclient.tokens_api.create_session_challenge(body)
    result.status.description = description
    if not open_profile:
        return result

    if not profile_uri:
        profile_parts = urlparse(context.get_issuer(ctx))
        if not profile_parts.netloc:
            raise ValueError("hostname must be present in issuer")
        host_parts = ["profile"] + profile_parts.netloc.split(".")[1:]
        host = ".".join(host_parts)
        profile_parts = profile_parts._replace(netloc=host)
    else:
        profile_parts = urlparse(profile_uri)

    fragment = base64.b64encode(
        json.dumps(result.status.to_dict(), default=str).encode()
    ).decode()
    profile_uri = profile_parts._replace(
        fragment=fragment, path="/handle_launcher_mfa"
    ).geturl()
    try:
        # Only do the import here so we can run the challenge on systems without profile
        import webbrowser

        webbrowser.open(profile_uri, new=1, autoraise=True)
    except Exception:
        output_if_console(ctx, "Failed to open browser")
        output_if_console(ctx, "Please visit the following link to answer the challenge")
        output_if_console(ctx, profile_uri)

    return result


def update_session_challenge(ctx, token=None):
    apiclient = context.get_apiclient_from_ctx(ctx, token=token)
    body = agilicus.SessionChallenge()
    return apiclient.tokens_api.update_session_challenge(body)


def clean_api_keys(
    ctx, expires_at=None, no_expiry=False, older_than=None, max_failures=5, **kwargs
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs["user_id"] = get_user_id_from_input_or_ctx(ctx, **kwargs)
    kwargs = strip_none(kwargs)
    to_delete = []

    def should_delete(api_key):
        if older_than is not None and api_key.metadata.created >= older_than:
            return False

        if api_key.spec.expiry is None:
            return no_expiry

        if expires_at is not None:
            return api_key.spec.expiry < expires_at

        return False

    def deleter(page: list):
        for api_key in page:
            if should_delete(api_key):
                to_delete.append(api_key)

    pagination.get_many_entries(
        apiclient.tokens_api.list_api_keys,
        "api_keys",
        100,
        None,
        page_callback=deleter,
        page_key="page_at_created_date",
        page_at_created_date=None,
        sort_order="descending",
        search_direction="forwards",
        **kwargs,
    )
    failures = 0
    deleted = []
    for key in to_delete:
        token_id = key.metadata.id
        org_id = key.spec.org_id
        try:
            apiclient.tokens_api.delete_api_key(token_id, org_id=org_id)
        except Exception as exc:
            print(f"failed deleting {token_id}: {exc}", file=sys.stderr)
            failures += 1
        if failures >= max_failures:
            print("too many failures. Exiting early", file=sys.stderr)
            return
        deleted.append(key)

    return deleted
