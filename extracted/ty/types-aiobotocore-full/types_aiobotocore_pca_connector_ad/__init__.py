"""
Main interface for pca-connector-ad service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pca_connector_ad/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_pca_connector_ad import (
        Client,
        ListConnectorsPaginator,
        ListDirectoryRegistrationsPaginator,
        ListServicePrincipalNamesPaginator,
        ListTemplateGroupAccessControlEntriesPaginator,
        ListTemplatesPaginator,
        PcaConnectorAdClient,
    )

    session = get_session()
    async with session.create_client("pca-connector-ad") as client:
        client: PcaConnectorAdClient
        ...


    list_connectors_paginator: ListConnectorsPaginator = client.get_paginator("list_connectors")
    list_directory_registrations_paginator: ListDirectoryRegistrationsPaginator = client.get_paginator("list_directory_registrations")
    list_service_principal_names_paginator: ListServicePrincipalNamesPaginator = client.get_paginator("list_service_principal_names")
    list_template_group_access_control_entries_paginator: ListTemplateGroupAccessControlEntriesPaginator = client.get_paginator("list_template_group_access_control_entries")
    list_templates_paginator: ListTemplatesPaginator = client.get_paginator("list_templates")
    ```
"""

from .client import PcaConnectorAdClient
from .paginator import (
    ListConnectorsPaginator,
    ListDirectoryRegistrationsPaginator,
    ListServicePrincipalNamesPaginator,
    ListTemplateGroupAccessControlEntriesPaginator,
    ListTemplatesPaginator,
)

Client = PcaConnectorAdClient


__all__ = (
    "Client",
    "ListConnectorsPaginator",
    "ListDirectoryRegistrationsPaginator",
    "ListServicePrincipalNamesPaginator",
    "ListTemplateGroupAccessControlEntriesPaginator",
    "ListTemplatesPaginator",
    "PcaConnectorAdClient",
)
