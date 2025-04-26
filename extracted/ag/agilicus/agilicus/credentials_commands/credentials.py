from .. import context
from ..input_helpers import (
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

    spec = agilicus.ObjectCredentialSpec(
        object_id=object_id,
        object_type=agilicus.ObjectType(object_type),
        purpose=agilicus.CredentialPurpose(purpose),
        **kwargs,
    )

    creds = agilicus.ObjectCredential(spec=spec)
    print(creds.to_dict())
    return apiclient.credentials_api.create_object_credential(creds).to_dict()


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
