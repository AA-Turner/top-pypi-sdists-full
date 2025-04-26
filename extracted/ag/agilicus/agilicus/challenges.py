import agilicus

from typing import Optional

from . import context
from . import input_helpers
from .input_helpers import strip_none
from .output.table import (
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
    spec = agilicus.TOTPEnrollmentSpec(user_id=user_id, **kwargs)
    model = agilicus.TOTPEnrollment(spec=spec)

    resp = apiclient.challenges_api.create_totp_enrollment(model)
    return resp


def update_challenge_enrollment(ctx, enrollment_id, user_id, answer, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    model = agilicus.TOTPEnrollmentAnswer(user_id=user_id, answer=answer)
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
