"""
Main interface for mailmanager service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mailmanager import (
        Client,
        ListAddonInstancesPaginator,
        ListAddonSubscriptionsPaginator,
        ListAddressListImportJobsPaginator,
        ListAddressListsPaginator,
        ListArchiveExportsPaginator,
        ListArchiveSearchesPaginator,
        ListArchivesPaginator,
        ListIngressPointsPaginator,
        ListMembersOfAddressListPaginator,
        ListRelaysPaginator,
        ListRuleSetsPaginator,
        ListTrafficPoliciesPaginator,
        MailManagerClient,
    )

    session = get_session()
    async with session.create_client("mailmanager") as client:
        client: MailManagerClient
        ...


    list_addon_instances_paginator: ListAddonInstancesPaginator = client.get_paginator("list_addon_instances")
    list_addon_subscriptions_paginator: ListAddonSubscriptionsPaginator = client.get_paginator("list_addon_subscriptions")
    list_address_list_import_jobs_paginator: ListAddressListImportJobsPaginator = client.get_paginator("list_address_list_import_jobs")
    list_address_lists_paginator: ListAddressListsPaginator = client.get_paginator("list_address_lists")
    list_archive_exports_paginator: ListArchiveExportsPaginator = client.get_paginator("list_archive_exports")
    list_archive_searches_paginator: ListArchiveSearchesPaginator = client.get_paginator("list_archive_searches")
    list_archives_paginator: ListArchivesPaginator = client.get_paginator("list_archives")
    list_ingress_points_paginator: ListIngressPointsPaginator = client.get_paginator("list_ingress_points")
    list_members_of_address_list_paginator: ListMembersOfAddressListPaginator = client.get_paginator("list_members_of_address_list")
    list_relays_paginator: ListRelaysPaginator = client.get_paginator("list_relays")
    list_rule_sets_paginator: ListRuleSetsPaginator = client.get_paginator("list_rule_sets")
    list_traffic_policies_paginator: ListTrafficPoliciesPaginator = client.get_paginator("list_traffic_policies")
    ```
"""

from .client import MailManagerClient
from .paginator import (
    ListAddonInstancesPaginator,
    ListAddonSubscriptionsPaginator,
    ListAddressListImportJobsPaginator,
    ListAddressListsPaginator,
    ListArchiveExportsPaginator,
    ListArchiveSearchesPaginator,
    ListArchivesPaginator,
    ListIngressPointsPaginator,
    ListMembersOfAddressListPaginator,
    ListRelaysPaginator,
    ListRuleSetsPaginator,
    ListTrafficPoliciesPaginator,
)

Client = MailManagerClient

__all__ = (
    "Client",
    "ListAddonInstancesPaginator",
    "ListAddonSubscriptionsPaginator",
    "ListAddressListImportJobsPaginator",
    "ListAddressListsPaginator",
    "ListArchiveExportsPaginator",
    "ListArchiveSearchesPaginator",
    "ListArchivesPaginator",
    "ListIngressPointsPaginator",
    "ListMembersOfAddressListPaginator",
    "ListRelaysPaginator",
    "ListRuleSetsPaginator",
    "ListTrafficPoliciesPaginator",
    "MailManagerClient",
)
