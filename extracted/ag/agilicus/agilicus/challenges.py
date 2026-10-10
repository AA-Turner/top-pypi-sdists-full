import agilicus

from typing import Optional

from . import context
from . import input_helpers
from .input_helpers import strip_none
from .output.json import output_json
from .output.table import (
    column,
    format_table,
    metadata_column,
    spec_column,
    status_column,
)

CHALLENGE_TYPES = ["web_push", "totp", "webauthn", "code"]


def create_challenge(ctx, user_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    challenge_endpoints = [
        agilicus.ChallengeEndpoint(endpoint=endpoint[0], type=endpoint[1])
        for endpoint in kwargs.pop("challenge_endpoint", [])
    ]
    challenge_types = [t for t in kwargs.pop("challenge_types", [])]
    kwargs = strip_none(kwargs)
    spec = agilicus.ChallengeSpec._from_openapi_data(
        user_id=user_id,
        challenge_endpoints=challenge_endpoints,
        challenge_types=challenge_types,
        **kwargs,
    )
    challenge = agilicus.Challenge(spec=spec)
    resp = apiclient.challenges_api.create_challenge(challenge)
    return resp


def replace_challenge(ctx, challenge_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    existing = apiclient.challenges_api.get_challenge(challenge_id)

    spec_as_dict = existing.spec.to_dict()
    spec_as_dict.update(kwargs)
    spec = agilicus.ChallengeSpec(**spec_as_dict)
    existing.spec = spec

    resp = apiclient.challenges_api.replace_challenge(challenge_id, existing)
    return resp


def get_challenge(ctx, challenge_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    kwargs = strip_none(kwargs)
    resp = apiclient.challenges_api.get_challenge(challenge_id)
    return resp


def delete_challenge(ctx, challenge_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    resp = apiclient.challenges_api.delete_challenge(challenge_id)
    return resp


def get_challenge_answer(
    ctx, challenge_id, challenge_answer, challenge_uid, allowed, challenge_type, **kwargs
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    params = {}
    if challenge_uid is not None:
        params["challenge_uid"] = challenge_uid
    else:
        params["challenge_uid"] = context.get_user_id(ctx)
    resp = apiclient.challenges_api.get_answer(
        challenge_id=challenge_id,
        challenge_answer=challenge_answer,
        allowed=allowed,
        challenge_type=challenge_type,
        **params,
    )
    return resp


def create_challenge_enrollment(ctx, user_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    # The generated TOTPEnrollmentSpec marks user_id read-only (it comes from
    # the schema's GUID_readonly), but the server requires it in the request
    # body. _from_openapi_data bypasses the read_only_vars guard by writing
    # straight into _data_store; once the SDK is regenerated from the fixed
    # schema (GUID instead of GUID_readonly) the plain constructor is correct.
    spec = agilicus.TOTPEnrollmentSpec._from_openapi_data(user_id=user_id, **kwargs)
    model = agilicus.TOTPEnrollment(spec=spec)

    resp = apiclient.challenges_api.create_totp_enrollment(model)
    return resp


def update_challenge_enrollment(ctx, enrollment_id, user_id, answer, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    # See create_challenge_enrollment: user_id is read-only in the generated
    # model until the SDK is regenerated from the fixed schema.
    model = agilicus.TOTPEnrollmentAnswer._from_openapi_data(
        user_id=user_id, answer=answer
    )
    resp = apiclient.challenges_api.update_totp_enrollment(enrollment_id, model)
    return resp


def get_challenge_enrollment(ctx, enrollment_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs = strip_none(kwargs)
    resp = apiclient.challenges_api.get_totp_enrollment(enrollment_id, **kwargs)
    return resp


def delete_challenge_enrollment(ctx, enrollment_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    resp = apiclient.challenges_api.delete_totp_enrollment(enrollment_id, **kwargs)
    return resp


def list_totp_enrollments(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs = strip_none(kwargs)
    results = apiclient.challenges_api.list_totp_enrollment(**kwargs)
    return results.totp


def format_totp_enrollments(ctx, details):
    columns = [
        metadata_column("id", "ID"),
        metadata_column("created", "Created"),
        metadata_column("updated", "Updated"),
        spec_column("user_id", "User ID"),
        status_column("state", "State"),
    ]
    return format_table(ctx, details, columns)


def list_webauthn_enrollments(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs = strip_none(kwargs)
    results = apiclient.challenges_api.list_webauthn_enrollments(**kwargs)
    return results.webauthn


def format_webauthn_enrollments(ctx, details):
    columns = [
        metadata_column("id", "ID"),
        metadata_column("created", "Created"),
        metadata_column("updated", "Updated"),
        spec_column("user_id", "User ID"),
        spec_column("relying_party_id", "Relying Party ID"),
        spec_column("attestation_format", "Attestation Format"),
        spec_column("attestation_conveyance", "Attestation Conveyance"),
        spec_column("user_verification", "User Verification"),
        status_column("transports", "Transports"),
    ]
    return format_table(ctx, details, columns)


def _org_mfa_api_call(ctx, path, method, path_params, body=None):
    """Invoke an org-scoped MFA endpoint not in the pinned generated SDK.

    The reconcile endpoint is newer than the generated client, so the call
    goes through the generated organisation client's ``api_client`` (same
    token, host and CA as every other call) rather than a typed method that
    does not exist yet. Mirrors platform/smoke/smoke/sdk.py.
    """
    apiclient = context.get_apiclient_from_ctx(ctx)
    headers = {"Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    return apiclient.org_api.api_client.call_api(
        path,
        method,
        path_params=path_params,
        query_params=[],
        header_params=headers,
        body=body,
        response_type=(dict,),
        auth_settings=["token-valid"],
        _return_http_data_only=True,
        _check_type=False,
    )


def reconcile_org_mfa_origins(
    ctx, org_id, new_origin=None, old_origin=None, dry_run=False, **kwargs
):
    """Rewrite safe MFA challenge-method origins for an org.

    Calls ``POST /v1/orgs/{org_id}/reconcile_mfa_origins``. Stale
    ``totp``/``web_push``/``sms``/``code`` origins are rewritten to the org
    origin; WebAuthn methods are never repointed, only reported and disabled
    (their ``relying_party_id`` is bound at registration and cannot be moved).
    ``new_origin`` defaults server-side to the org's issuer origin; ``dry_run``
    returns the report without writing.
    """
    body = {"dry_run": bool(dry_run)}
    if new_origin is not None:
        body["new_origin"] = new_origin
    if old_origin is not None:
        body["old_origin"] = old_origin
    return _org_mfa_api_call(
        ctx,
        "/v1/orgs/{org_id}/reconcile_mfa_origins",
        "POST",
        {"org_id": org_id},
        body,
    )


def report_org_webauthn_enrollments(ctx, org_id, user_id=None, **kwargs):
    """Report the WebAuthn methods bound to a stale origin (never writes).

    This is the dry-run form of :func:`reconcile_org_mfa_origins`: the users
    service is authoritative for which WebAuthn method belongs to which org
    user, and the challenges service holds the credential record. The report
    is optionally joined with ``list_webauthn_enrollments`` so the enrollment
    id in ``endpoint`` carries its created/updated/transports detail.
    """
    report = reconcile_org_mfa_origins(ctx, org_id, dry_run=True, **kwargs)
    affected = list(report.get("webauthn_affected") or [])
    if user_id is not None:
        affected = [entry for entry in affected if entry.get("user_id") == user_id]

    enrollments_by_user = {}
    for entry in affected:
        affected_user_id = entry.get("user_id")
        if affected_user_id and affected_user_id not in enrollments_by_user:
            try:
                enrollments_by_user[affected_user_id] = (
                    list_webauthn_enrollments(ctx, user_id=affected_user_id) or []
                )
            except agilicus.ApiException:
                enrollments_by_user[affected_user_id] = []
    for entry in affected:
        for enrollment in enrollments_by_user.get(entry.get("user_id"), []):
            if enrollment.metadata.id == entry.get("endpoint"):
                entry["enrollment"] = enrollment.to_dict()
                break

    report["webauthn_affected"] = affected
    report["webauthn_affected_count"] = len(affected)
    report["users_affected_count"] = len({e.get("user_id") for e in affected})
    return report


def format_reconcile_org_mfa_origins(ctx, report):
    """Print a reconcile report: summary table, then the affected WebAuthn rows.

    ``--output-format json`` emits the report verbatim for scripting.
    """
    if context.output_json(ctx):
        output_json(ctx, report)
        return
    summary_columns = [
        column("org_id", "Org ID", itemgetter=True),
        column("origin", "Origin", itemgetter=True),
        column("dry_run", "Dry Run", itemgetter=True),
        column("totp_updated", "TOTP Updated", itemgetter=True),
        column("web_push_updated", "Web Push Updated", itemgetter=True),
        column("webauthn_affected_count", "WebAuthn Affected", itemgetter=True),
        column("users_affected_count", "Users Affected", itemgetter=True),
    ]
    print(format_table(ctx, [report], summary_columns))
    affected_columns = [
        column("user_id", "User ID", itemgetter=True),
        column("challenge_method_id", "Challenge Method ID", itemgetter=True),
        column("endpoint", "Enrollment ID", itemgetter=True),
        column("origin", "Origin", itemgetter=True),
    ]
    affected = report.get("webauthn_affected") or []
    if affected:
        print(format_table(ctx, affected, affected_columns))


def format_org_webauthn_enrollments_report(ctx, report):
    """Print the per-user WebAuthn re-enrollment report (JSON when requested)."""
    if context.output_json(ctx):
        output_json(ctx, report)
        return
    columns = [
        column("user_id", "User ID", itemgetter=True),
        column("challenge_method_id", "Challenge Method ID", itemgetter=True),
        column("endpoint", "Enrollment ID", itemgetter=True),
        column("origin", "Origin", itemgetter=True),
        column("enrollment", "Enrollment", itemgetter=True, optional=True),
    ]
    affected = report.get("webauthn_affected") or []
    print(format_table(ctx, affected, columns))
    print(
        f"{report.get('webauthn_affected_count', 0)} WebAuthn method(s) across "
        f"{report.get('users_affected_count', 0)} user(s) require re-enrollment"
    )


def create_one_time_use_challenge(
    ctx,
    actor_id: list,
    action_url,
    action_method,
    timeout_seconds,
    user_id=None,
    org_id=None,
    approve_action_body=None,
    decline_action_body=None,
    action_content_type=None,
    scope: Optional[list] = None,
    **kwargs,
):
    org_id = input_helpers.get_org_from_input_or_ctx(ctx, org_id, **kwargs)
    actors = [
        agilicus.ChallengeActor(user_id=actor, org_id=org_id) for actor in actor_id
    ]

    approve_action = agilicus.HTTPChallengeAction(
        challenge_action_type="http_action",
        method=action_method,
        uri=action_url,
    )

    decline_action = agilicus.HTTPChallengeAction(
        challenge_action_type="http_action",
        method=action_method,
        uri=action_url,
    )

    if action_content_type is not None:
        approve_action.content_type = action_content_type
        decline_action.content_type = action_content_type

    if scope is not None:
        scopes = [agilicus.TokenScope(scope_str) for scope_str in scope]
        approve_action.scopes = scopes
        decline_action.scopes = scopes

    if approve_action_body is not None:
        approve_action.body = approve_action_body

    if decline_action_body is not None:
        decline_action.body = decline_action_body

    spec = agilicus.OneTimeUseActionChallengeSpec(
        org_id=org_id,
        approved_actions=[approve_action],
        declined_actions=[decline_action],
        actors=actors,
        timeout_seconds=timeout_seconds,
    )
    if user_id is not None:
        spec.user_id = user_id

    challenge = agilicus.OneTimeUseActionChallenge(spec=spec)

    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.challenges_api.create_one_time_use_action(challenge)
