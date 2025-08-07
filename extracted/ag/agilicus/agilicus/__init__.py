# flake8: noqa
from typing import Callable
import json
import os
import sys
import dataclasses
from . import context
from . import scopes
from . import credentials
from . import tokens
import jwt

from .version import __version__  # noqa

sys.path.append(os.path.dirname(__file__))  # noqa

from .agilicus_api import *  # noqa
from .agilicus_api import exceptions  # noqa
from . import patches  # noqa
from .pagination.pagination import get_many_entries

from .create import create_or_update, add_list_resources, AddInfo, AddResult, find_guid

ApiClient = patches.patched_api_client()


@dataclasses.dataclass
class AgilicusAPIHelper:
    default_org_id: str
    users: UsersApi
    billing: BillingApi
    organisations: OrganisationsApi
    policies: PolicyApi
    certificates: CertificatesApi
    applications: ApplicationsApi
    groups: GroupsApi
    connectors: ConnectorsApi
    resources: ResourcesApi
    resouces: ResourcesApi
    catalogues: CataloguesApi
    permissions: PermissionsApi
    audits: AuditsApi
    files: FilesApi
    tokens: TokensApi
    diagnostics: DiagnosticsApi
    metrics: MetricsApi
    challenges: ChallengesApi
    application_services: ApplicationServicesApi
    issuers: IssuersApi
    messages: MessagesApi
    lookups: LookupsApi
    trusted_certs: TrustedCertsApi
    rules: RulesApi
    policy_config: PolicyConfigApi
    licensing: LicensingApi


def GetClient(
    issuer=context.ISSUER_DEFAULT,
    cacert=None,
    client_id="agilicus-builtin-cli",
    authentication_document=None,
    agilicus_scopes=scopes.DEFAULT_SCOPES,
    auth_local_webserver=True,
    api_url=None,
    expiry=None,
    admin=False,
):

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
