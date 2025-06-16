"""
Main interface for taxsettings service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_taxsettings import (
        Client,
        ListSupplementalTaxRegistrationsPaginator,
        ListTaxExemptionsPaginator,
        ListTaxRegistrationsPaginator,
        TaxSettingsClient,
    )

    session = get_session()
    async with session.create_client("taxsettings") as client:
        client: TaxSettingsClient
        ...


    list_supplemental_tax_registrations_paginator: ListSupplementalTaxRegistrationsPaginator = client.get_paginator("list_supplemental_tax_registrations")
    list_tax_exemptions_paginator: ListTaxExemptionsPaginator = client.get_paginator("list_tax_exemptions")
    list_tax_registrations_paginator: ListTaxRegistrationsPaginator = client.get_paginator("list_tax_registrations")
    ```
"""

from .client import TaxSettingsClient
from .paginator import (
    ListSupplementalTaxRegistrationsPaginator,
    ListTaxExemptionsPaginator,
    ListTaxRegistrationsPaginator,
)

Client = TaxSettingsClient


__all__ = (
    "Client",
    "ListSupplementalTaxRegistrationsPaginator",
    "ListTaxExemptionsPaginator",
    "ListTaxRegistrationsPaginator",
    "TaxSettingsClient",
)
