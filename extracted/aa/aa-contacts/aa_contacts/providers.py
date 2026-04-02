from esi.openapi_clients import ESIClientProvider

from . import (
    __version__ as app_version,
    __app_name_ua__ as app_name_ua,
    __github_url__ as github_url,
    __esi_compatibility_date__ as esi_compatibility_date,
)

esi = ESIClientProvider(
    compatibility_date=esi_compatibility_date,
    ua_appname=app_name_ua,
    ua_version=app_version,
    ua_url=github_url,
    operations=[
        "GetAlliancesAllianceIdContacts",
        "GetAlliancesAllianceIdContactsLabels",
        "GetCorporationsCorporationIdContacts",
        "GetCorporationsCorporationIdContactsLabels",
    ],
)
