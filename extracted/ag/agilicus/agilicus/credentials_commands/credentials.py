from .. import context
from ..input_helpers import (
    build_updated_model_from_dict,
    get_org_from_input_or_ctx,
    strip_none,
)
import agilicus
from ..output.table import (
    column,
    spec_column,
    format_table,
    metadata_column,
    status_column,
    constant_if_exists,
    summarize,
)

from .oauth2 import get_oauth2_auth


def make_secrets(private_key=None, **kwargs):
    private_key_data = None
    if private_key is not None:
        private_key_data = private_key.read()
    kwargs = strip_none(kwargs)

    if private_key_data is None and len(kwargs) == 0:
        # Nothing to do. Just return.
        return None

    result = agilicus.ObjectCredentialSecrets(**kwargs)
    if private_key_data is not None:
        result.private_key = private_key_data
    return result


def add_object_credentials(ctx, object_id, object_type, purpose, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs = strip_none(kwargs)

    oauth2_auth = get_oauth2_auth({}, kwargs, pop=True)

    spec = agilicus.ObjectCredentialSpec(
        object_id=object_id,
        object_type=agilicus.ObjectType(object_type),
        purpose=agilicus.CredentialPurpose(purpose),
        **kwargs,
    )

    if oauth2_auth:
        spec.oauth2 = oauth2_auth

    creds = agilicus.ObjectCredential(spec=spec)
    return apiclient.credentials_api.create_object_credential(creds).to_dict()


def replace_object_credentials(ctx, object_credential_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs = strip_none(kwargs)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    credential = apiclient.credentials_api.get_object_credential(
        object_credential_id, org_id=org_id
    )
    kwargs = strip_none(kwargs)
    oauth2 = get_oauth2_auth(credential.spec.oauth2 or {}, kwargs, pop=True)
    credential.spec = build_updated_model_from_dict(
        agilicus.ObjectCredentialSpec, credential.spec, kwargs
    )
    if oauth2:
        credential.spec.oauth2 = oauth2

    return apiclient.credentials_api.replace_object_credential(
        object_credential_id, object_credential=credential
    ).to_dict()


def get_object_credential(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs = strip_none(kwargs)

    return apiclient.credentials_api.get_object_credential(**kwargs)


def delete_object_credential(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs = strip_none(kwargs)

    return apiclient.credentials_api.delete_object_credential(**kwargs)


def list_object_credentials(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs = strip_none(kwargs)

    return apiclient.credentials_api.list_object_credentials(**kwargs).object_credentials


def format_object_credentials(ctx, labels):
    columns = [
        metadata_column("id"),
        spec_column("org_id"),
        spec_column("object_type"),
        spec_column("object_id"),
        spec_column("purpose"),
        spec_column("description"),
        status_column("is_encrypted", "enc"),
        summarize(status_column("encryption_key_id"), max_length=16),
        constant_if_exists(status_column("password"), "✓"),
        constant_if_exists(status_column("private_key", "pk"), "✓"),
        constant_if_exists(
            status_column("private_key_passphrase", "pk_passphrase"), "✓"
        ),
    ]

    return format_table(ctx, labels, columns)


def list_existence_info(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs = strip_none(kwargs)

    return apiclient.credentials_api.list_object_credential_existence_info(
        **kwargs
    ).object_credential_existence_info


def format_object_credential_existence_info(ctx, labels):
    columns = [
        column("credential_id"),
        column("org_id"),
        column("object_type"),
        column("object_id"),
        column("purpose"),
    ]

    return format_table(ctx, labels, columns)
