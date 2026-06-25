from esi.openapi_clients import ESIClientProvider

from . import (
    __app_name_ua__ as app_name_ua,
)
from . import (
    __esi_compatibility_date__ as esi_compatibility_date,
)
from . import (
    __github_url__ as github_url,
)
from . import (
    __version__ as app_version,
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
