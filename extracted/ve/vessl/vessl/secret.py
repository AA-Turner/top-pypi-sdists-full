

from vessl import vessl_api
from vessl.organization import _get_organization_name


def list_generic_secrets():
    organization_name = _get_organization_name()

    secrets_resp = vessl_api.secret_list_api(
        organization_name=organization_name,
        kind="generic-secret"
    )
    return secrets_resp.secrets