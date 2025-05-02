"""
Type annotations for fms service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_fms.client import FMSClient
    from types_aiobotocore_fms.paginator import (
        ListAdminAccountsForOrganizationPaginator,
        ListAdminsManagingAccountPaginator,
        ListAppsListsPaginator,
        ListComplianceStatusPaginator,
        ListMemberAccountsPaginator,
        ListPoliciesPaginator,
        ListProtocolsListsPaginator,
        ListThirdPartyFirewallFirewallPoliciesPaginator,
    )

    session = get_session()
    with session.create_client("fms") as client:
        client: FMSClient

        list_admin_accounts_for_organization_paginator: ListAdminAccountsForOrganizationPaginator = client.get_paginator("list_admin_accounts_for_organization")
        list_admins_managing_account_paginator: ListAdminsManagingAccountPaginator = client.get_paginator("list_admins_managing_account")
        list_apps_lists_paginator: ListAppsListsPaginator = client.get_paginator("list_apps_lists")
        list_compliance_status_paginator: ListComplianceStatusPaginator = client.get_paginator("list_compliance_status")
        list_member_accounts_paginator: ListMemberAccountsPaginator = client.get_paginator("list_member_accounts")
        list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
        list_protocols_lists_paginator: ListProtocolsListsPaginator = client.get_paginator("list_protocols_lists")
        list_third_party_firewall_firewall_policies_paginator: ListThirdPartyFirewallFirewallPoliciesPaginator = client.get_paginator("list_third_party_firewall_firewall_policies")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAdminAccountsForOrganizationRequestPaginateTypeDef,
    ListAdminAccountsForOrganizationResponseTypeDef,
    ListAdminsManagingAccountRequestPaginateTypeDef,
    ListAdminsManagingAccountResponseTypeDef,
    ListAppsListsRequestPaginateTypeDef,
    ListAppsListsResponseTypeDef,
    ListComplianceStatusRequestPaginateTypeDef,
    ListComplianceStatusResponseTypeDef,
    ListMemberAccountsRequestPaginateTypeDef,
    ListMemberAccountsResponseTypeDef,
    ListPoliciesRequestPaginateTypeDef,
    ListPoliciesResponseTypeDef,
    ListProtocolsListsRequestPaginateTypeDef,
    ListProtocolsListsResponseTypeDef,
    ListThirdPartyFirewallFirewallPoliciesRequestPaginateTypeDef,
    ListThirdPartyFirewallFirewallPoliciesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAdminAccountsForOrganizationPaginator",
    "ListAdminsManagingAccountPaginator",
    "ListAppsListsPaginator",
    "ListComplianceStatusPaginator",
    "ListMemberAccountsPaginator",
    "ListPoliciesPaginator",
    "ListProtocolsListsPaginator",
    "ListThirdPartyFirewallFirewallPoliciesPaginator",
)

if TYPE_CHECKING:
    _ListAdminAccountsForOrganizationPaginatorBase = AioPaginator[
        ListAdminAccountsForOrganizationResponseTypeDef
    ]
else:
    _ListAdminAccountsForOrganizationPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAdminAccountsForOrganizationPaginator(_ListAdminAccountsForOrganizationPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListAdminAccountsForOrganization.html#FMS.Paginator.ListAdminAccountsForOrganization)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listadminaccountsfororganizationpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAdminAccountsForOrganizationRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAdminAccountsForOrganizationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListAdminAccountsForOrganization.html#FMS.Paginator.ListAdminAccountsForOrganization.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listadminaccountsfororganizationpaginator)
        """

if TYPE_CHECKING:
    _ListAdminsManagingAccountPaginatorBase = AioPaginator[ListAdminsManagingAccountResponseTypeDef]
else:
    _ListAdminsManagingAccountPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAdminsManagingAccountPaginator(_ListAdminsManagingAccountPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListAdminsManagingAccount.html#FMS.Paginator.ListAdminsManagingAccount)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listadminsmanagingaccountpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAdminsManagingAccountRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAdminsManagingAccountResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListAdminsManagingAccount.html#FMS.Paginator.ListAdminsManagingAccount.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listadminsmanagingaccountpaginator)
        """

if TYPE_CHECKING:
    _ListAppsListsPaginatorBase = AioPaginator[ListAppsListsResponseTypeDef]
else:
    _ListAppsListsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAppsListsPaginator(_ListAppsListsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListAppsLists.html#FMS.Paginator.ListAppsLists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listappslistspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAppsListsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAppsListsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListAppsLists.html#FMS.Paginator.ListAppsLists.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listappslistspaginator)
        """

if TYPE_CHECKING:
    _ListComplianceStatusPaginatorBase = AioPaginator[ListComplianceStatusResponseTypeDef]
else:
    _ListComplianceStatusPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListComplianceStatusPaginator(_ListComplianceStatusPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListComplianceStatus.html#FMS.Paginator.ListComplianceStatus)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listcompliancestatuspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListComplianceStatusRequestPaginateTypeDef]
    ) -> AioPageIterator[ListComplianceStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListComplianceStatus.html#FMS.Paginator.ListComplianceStatus.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listcompliancestatuspaginator)
        """

if TYPE_CHECKING:
    _ListMemberAccountsPaginatorBase = AioPaginator[ListMemberAccountsResponseTypeDef]
else:
    _ListMemberAccountsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMemberAccountsPaginator(_ListMemberAccountsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListMemberAccounts.html#FMS.Paginator.ListMemberAccounts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listmemberaccountspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMemberAccountsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMemberAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListMemberAccounts.html#FMS.Paginator.ListMemberAccounts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listmemberaccountspaginator)
        """

if TYPE_CHECKING:
    _ListPoliciesPaginatorBase = AioPaginator[ListPoliciesResponseTypeDef]
else:
    _ListPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPoliciesPaginator(_ListPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListPolicies.html#FMS.Paginator.ListPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listpoliciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListPolicies.html#FMS.Paginator.ListPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listpoliciespaginator)
        """

if TYPE_CHECKING:
    _ListProtocolsListsPaginatorBase = AioPaginator[ListProtocolsListsResponseTypeDef]
else:
    _ListProtocolsListsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListProtocolsListsPaginator(_ListProtocolsListsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListProtocolsLists.html#FMS.Paginator.ListProtocolsLists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listprotocolslistspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProtocolsListsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProtocolsListsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListProtocolsLists.html#FMS.Paginator.ListProtocolsLists.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listprotocolslistspaginator)
        """

if TYPE_CHECKING:
    _ListThirdPartyFirewallFirewallPoliciesPaginatorBase = AioPaginator[
        ListThirdPartyFirewallFirewallPoliciesResponseTypeDef
    ]
else:
    _ListThirdPartyFirewallFirewallPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListThirdPartyFirewallFirewallPoliciesPaginator(
    _ListThirdPartyFirewallFirewallPoliciesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListThirdPartyFirewallFirewallPolicies.html#FMS.Paginator.ListThirdPartyFirewallFirewallPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listthirdpartyfirewallfirewallpoliciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListThirdPartyFirewallFirewallPoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListThirdPartyFirewallFirewallPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/paginator/ListThirdPartyFirewallFirewallPolicies.html#FMS.Paginator.ListThirdPartyFirewallFirewallPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/paginators/#listthirdpartyfirewallfirewallpoliciespaginator)
        """
