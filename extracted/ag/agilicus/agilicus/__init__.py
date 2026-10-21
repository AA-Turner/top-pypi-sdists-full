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
    policy_templates: "PolicyTemplatesApi"
    certificates: "CertificatesApi"
    applications: "ApplicationsApi"
    groups: "GroupsApi"
    connectors: "ConnectorsApi"
    resources: "ResourcesApi"
    # Deprecated typo of ``resources``, kept so existing callers keep working.
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
    credentials: "CredentialsApi"
    deployments: "DeploymentsApi"
    features: "FeaturesApi"
    hosts: "HostsApi"
    labels: "LabelsApi"
    launchers: "LaunchersApi"
    regions: "RegionsApi"

    # CLI-compatible aliases.
    #
    # ``context.get_apiclient()`` returns an ``ApiHelper`` whose services are
    # named with an ``_api`` suffix (``metrics_api``, ``audits_api``, ...),
    # while ``GetClient()`` has always used short names (``metrics``,
    # ``audits``, ...).  Both are public enough that code gets written against
    # one and reused with the other, so expose the CLI names here too.  These
    # are plain properties: they add no imports and keep ``import agilicus``
    # lazy.
    @property
    def metrics_api(self):
        return self.metrics

    @property
    def audits_api(self):
        return self.audits

    @property
    def org_api(self):
        return self.organisations

    @property
    def organisations_api(self):
        return self.organisations

    @property
    def user_api(self):
        return self.users

    @property
    def users_api(self):
        return self.users

    @property
    def application_api(self):
        return self.applications

    @property
    def applications_api(self):
        return self.applications

    @property
    def app_services_api(self):
        return self.application_services

    @property
    def application_services_api(self):
        return self.application_services

    @property
    def logs_api(self):
        return self.diagnostics

    @property
    def diagnostics_api(self):
        return self.diagnostics

    @property
    def policy_api(self):
        return self.policies

    @property
    def policies_api(self):
        return self.policies

    @property
    def resources_api(self):
        return self.resources

    @property
    def billing_api(self):
        return self.billing

    @property
    def catalogues_api(self):
        return self.catalogues

    @property
    def certificates_api(self):
        return self.certificates

    @property
    def challenges_api(self):
        return self.challenges

    @property
    def connectors_api(self):
        return self.connectors

    @property
    def credentials_api(self):
        return self.credentials

    @property
    def deployments_api(self):
        return self.deployments

    @property
    def features_api(self):
        return self.features

    @property
    def files_api(self):
        return self.files

    @property
    def groups_api(self):
        return self.groups

    @property
    def hosts_api(self):
        return self.hosts

    @property
    def issuers_api(self):
        return self.issuers

    @property
    def labels_api(self):
        return self.labels

    @property
    def launchers_api(self):
        return self.launchers

    @property
    def licensing_api(self):
        return self.licensing

    @property
    def lookups_api(self):
        return self.lookups

    @property
    def messages_api(self):
        return self.messages

    @property
    def permissions_api(self):
        return self.permissions

    @property
    def policy_config_api(self):
        return self.policy_config

    @property
    def policy_templates_api(self):
        return self.policy_templates

    @property
    def regions_api(self):
        return self.regions

    @property
    def rules_api(self):
        return self.rules

    @property
    def tokens_api(self):
        return self.tokens

    @property
    def trusted_certs_api(self):
        return self.trusted_certs


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
    token=None,
):
    import jwt

    # PEP 562 ``__getattr__`` only fires for attribute access on the module;
    # a bare-name global lookup inside a function in this module bypasses it.
    # Resolve everything this function touches here (still deferred until the
    # first ``GetClient`` call, so ``import agilicus`` stays lazy).
    from .agilicus_api import (
        ApplicationServicesApi,
        ApplicationsApi,
        AuditsApi,
        BillingApi,
        CataloguesApi,
        CertificatesApi,
        ChallengesApi,
        Configuration,
        ConnectorsApi,
        CredentialsApi,
        DeploymentsApi,
        DiagnosticsApi,
        FeaturesApi,
        FilesApi,
        GroupsApi,
        HostsApi,
        IssuersApi,
        LabelsApi,
        LaunchersApi,
        LicensingApi,
        LookupsApi,
        MessagesApi,
        MetricsApi,
        OrganisationsApi,
        PermissionsApi,
        PolicyApi,
        PolicyConfigApi,
        PolicyTemplatesApi,
        RegionsApi,
        ResourcesApi,
        RulesApi,
        TokensApi,
        TrustedCertsApi,
        UsersApi,
    )

    config = Configuration(host=api_url, ssl_ca_cert=cacert, discard_unknown_keys=True)
    if token is not None:
        # The caller already holds an access token (for example from a
        # browserless OIDC flow); use it directly and skip the interactive and
        # authentication-document credential paths.
        config.access_token = token
    elif authentication_document:
        from . import scopes, tokens

        if agilicus_scopes is _UNSET:
            agilicus_scopes = scopes.DEFAULT_SCOPES
        creds = {}
        with open(authentication_document) as fd:
            ad = json.load(fd)
        service_token = tokens.create_service_token(
            auth_doc=ad,
            scope=agilicus_scopes,
            client_id=client_id,
            expiry=expiry,
            verify=cacert,
        )
        config.access_token = service_token.get("access_token")
    else:
        from . import context, credentials, scopes

        if issuer is _UNSET:
            issuer = context.ISSUER_DEFAULT
        if agilicus_scopes is _UNSET:
            agilicus_scopes = scopes.DEFAULT_SCOPES
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

    # One ResourcesApi instance shared by ``resources`` and the historical
    # ``resouces`` typo, so both names refer to the same client.
    resources = ResourcesApi(ApiClient(config))

    return AgilicusAPIHelper(
        default_org_id=_default_org_id,
        users=UsersApi(ApiClient(config)),
        billing=BillingApi(ApiClient(config)),
        organisations=OrganisationsApi(ApiClient(config)),
        policies=PolicyApi(ApiClient(config)),
        policy_templates=PolicyTemplatesApi(ApiClient(config)),
        certificates=CertificatesApi(ApiClient(config)),
        applications=ApplicationsApi(ApiClient(config)),
        groups=GroupsApi(ApiClient(config)),
        connectors=ConnectorsApi(ApiClient(config)),
        resouces=resources,
        resources=resources,
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
        credentials=CredentialsApi(ApiClient(config)),
        deployments=DeploymentsApi(ApiClient(config)),
        features=FeaturesApi(ApiClient(config)),
        hosts=HostsApi(ApiClient(config)),
        labels=LabelsApi(ApiClient(config)),
        launchers=LaunchersApi(ApiClient(config)),
        regions=RegionsApi(ApiClient(config)),
    )
