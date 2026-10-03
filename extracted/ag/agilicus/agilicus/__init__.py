# flake8: noqa
from typing import Callable
import dataclasses
import importlib as _importlib
import json
import os
import sys

from .version import __version__  # noqa

sys.path.append(os.path.dirname(__file__))  # noqa

from .agilicus_api import exceptions  # noqa
from .agilicus_api.api_client import Endpoint
import agilicus_api.api_client

from . import patches  # noqa
from pagination.pagination import get_many_entries

endpoint_class = agilicus_api.api_client.Endpoint

ApiClient = patches.patched_api_client()
patches.patch_endpoint_class(endpoint_class)


# Import-on-first-use for everything that used to be imported eagerly here.
# ``import agilicus`` no longer pulls the whole generated client (1030 API and
# model classes), the CLI stack, or their dependencies (dateparser,
# oauth2client, ...).  ``agilicus.X`` and ``from agilicus import X`` keep
# working for every previously importable X; the first access pays the load.
_LAZY_SUBMODULES = {
    "access": "agilicus.access",
    "context": "agilicus.context",
    "credentials": "agilicus.credentials",
    "create": "agilicus.create",
    "input_helpers": "agilicus.input_helpers",
    "scopes": "agilicus.scopes",
    "tokens": "agilicus.tokens",
}

_LAZY_CREATE_NAMES = {
    "AddInfo",
    "AddResult",
    "add_list_resources",
    "create_or_update",
    "find_guid",
}


def __getattr__(name):
    if name.startswith("__") and name.endswith("__"):
        raise AttributeError("module %r has no attribute %r" % (__name__, name))
    module_name = _LAZY_SUBMODULES.get(name)
    if module_name is not None:
        value = _importlib.import_module(module_name)
    elif name in _LAZY_CREATE_NAMES:
        value = getattr(_importlib.import_module("agilicus.create"), name)
    else:
        value = getattr(_importlib.import_module("agilicus_api"), name)
    globals()[name] = value
    return value


def __dir__():
    return sorted(set(globals()) | set(_LAZY_SUBMODULES) | _LAZY_CREATE_NAMES)


@dataclasses.dataclass
class AgilicusAPIHelper:
    default_org_id: str
    users: "UsersApi"
    billing: "BillingApi"
    organisations: "OrganisationsApi"
    policies: "PolicyApi"
    certificates: "CertificatesApi"
    applications: "ApplicationsApi"
    groups: "GroupsApi"
    connectors: "ConnectorsApi"
    resources: "ResourcesApi"
    resouces: "ResourcesApi"
    catalogues: "CataloguesApi"
    permissions: "PermissionsApi"
    audits: "AuditsApi"
    files: "FilesApi"
    tokens: "TokensApi"
    diagnostics: "DiagnosticsApi"
    metrics: "MetricsApi"
    challenges: "ChallengesApi"
    application_services: "ApplicationServicesApi"
    issuers: "IssuersApi"
    messages: "MessagesApi"
    lookups: "LookupsApi"
    trusted_certs: "TrustedCertsApi"
    rules: "RulesApi"
    policy_config: "PolicyConfigApi"
    licensing: "LicensingApi"


_UNSET = object()


def GetClient(
    issuer=_UNSET,
    cacert=None,
    client_id="agilicus-builtin-cli",
    authentication_document=None,
    agilicus_scopes=_UNSET,
    auth_local_webserver=True,
    api_url=None,
    expiry=None,
    admin=False,
):
    if issuer is _UNSET:
        issuer = context.ISSUER_DEFAULT
    if agilicus_scopes is _UNSET:
        agilicus_scopes = scopes.DEFAULT_SCOPES

    import jwt

    config = Configuration(host=api_url, ssl_ca_cert=cacert, discard_unknown_keys=True)
    if authentication_document:
        creds = {}
        with open(authentication_document) as fd:
            ad = json.load(fd)
        token = tokens.create_service_token(
            auth_doc=ad,
            scope=agilicus_scopes,
            client_id=client_id,
            expiry=expiry,
            verify=cacert,
        )
        config.access_token = token.get("access_token")
    else:
        creds = credentials.get_credentials(
            issuer=issuer,
            cacert=cacert,
            client_id=client_id,
            agilicus_scopes=agilicus_scopes,
            auth_local_webserver=auth_local_webserver,
            admin=admin,
        )
        config.access_token = creds.access_token

    _default_org_id = None
    access_token = jwt.decode(
        config.access_token,
        algorithms=["ES256"],
        options={"verify_signature": False},
        leeway=60,
    )
    if "org" in access_token:
        _default_org_id = access_token["org"]

    return AgilicusAPIHelper(
        default_org_id=_default_org_id,
        users=UsersApi(ApiClient(config)),
        billing=BillingApi(ApiClient(config)),
        organisations=OrganisationsApi(ApiClient(config)),
        policies=PolicyApi(ApiClient(config)),
        certificates=CertificatesApi(ApiClient(config)),
        applications=ApplicationsApi(ApiClient(config)),
        groups=GroupsApi(ApiClient(config)),
        connectors=ConnectorsApi(ApiClient(config)),
        resouces=ResourcesApi(ApiClient(config)),
        resources=ResourcesApi(ApiClient(config)),
        catalogues=CataloguesApi(ApiClient(config)),
        permissions=PermissionsApi(ApiClient(config)),
        audits=AuditsApi(ApiClient(config)),
        files=FilesApi(ApiClient(config)),
        tokens=TokensApi(ApiClient(config)),
        diagnostics=DiagnosticsApi(ApiClient(config)),
        metrics=MetricsApi(ApiClient(config)),
        challenges=ChallengesApi(ApiClient(config)),
        application_services=ApplicationServicesApi(ApiClient(config)),
        issuers=IssuersApi(ApiClient(config)),
        messages=MessagesApi(ApiClient(config)),
        lookups=LookupsApi(ApiClient(config)),
        trusted_certs=TrustedCertsApi(ApiClient(config)),
        rules=RulesApi(ApiClient(config)),
        policy_config=PolicyConfigApi(ApiClient(config)),
        licensing=LicensingApi(ApiClient(config)),
    )
