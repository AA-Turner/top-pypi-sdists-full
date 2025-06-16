"""
Type annotations for organizations service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_organizations.client import OrganizationsClient
    from types_aiobotocore_organizations.paginator import (
        ListAWSServiceAccessForOrganizationPaginator,
        ListAccountsForParentPaginator,
        ListAccountsPaginator,
        ListChildrenPaginator,
        ListCreateAccountStatusPaginator,
        ListDelegatedAdministratorsPaginator,
        ListDelegatedServicesForAccountPaginator,
        ListHandshakesForAccountPaginator,
        ListHandshakesForOrganizationPaginator,
        ListOrganizationalUnitsForParentPaginator,
        ListParentsPaginator,
        ListPoliciesForTargetPaginator,
        ListPoliciesPaginator,
        ListRootsPaginator,
        ListTagsForResourcePaginator,
        ListTargetsForPolicyPaginator,
    )

    session = get_session()
    with session.create_client("organizations") as client:
        client: OrganizationsClient

        list_aws_service_access_for_organization_paginator: ListAWSServiceAccessForOrganizationPaginator = client.get_paginator("list_aws_service_access_for_organization")
        list_accounts_for_parent_paginator: ListAccountsForParentPaginator = client.get_paginator("list_accounts_for_parent")
        list_accounts_paginator: ListAccountsPaginator = client.get_paginator("list_accounts")
        list_children_paginator: ListChildrenPaginator = client.get_paginator("list_children")
        list_create_account_status_paginator: ListCreateAccountStatusPaginator = client.get_paginator("list_create_account_status")
        list_delegated_administrators_paginator: ListDelegatedAdministratorsPaginator = client.get_paginator("list_delegated_administrators")
        list_delegated_services_for_account_paginator: ListDelegatedServicesForAccountPaginator = client.get_paginator("list_delegated_services_for_account")
        list_handshakes_for_account_paginator: ListHandshakesForAccountPaginator = client.get_paginator("list_handshakes_for_account")
        list_handshakes_for_organization_paginator: ListHandshakesForOrganizationPaginator = client.get_paginator("list_handshakes_for_organization")
        list_organizational_units_for_parent_paginator: ListOrganizationalUnitsForParentPaginator = client.get_paginator("list_organizational_units_for_parent")
        list_parents_paginator: ListParentsPaginator = client.get_paginator("list_parents")
        list_policies_for_target_paginator: ListPoliciesForTargetPaginator = client.get_paginator("list_policies_for_target")
        list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
        list_roots_paginator: ListRootsPaginator = client.get_paginator("list_roots")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
        list_targets_for_policy_paginator: ListTargetsForPolicyPaginator = client.get_paginator("list_targets_for_policy")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAccountsForParentRequestPaginateTypeDef,
    ListAccountsForParentResponseTypeDef,
    ListAccountsRequestPaginateTypeDef,
    ListAccountsResponseTypeDef,
    ListAWSServiceAccessForOrganizationRequestPaginateTypeDef,
    ListAWSServiceAccessForOrganizationResponseTypeDef,
    ListChildrenRequestPaginateTypeDef,
    ListChildrenResponseTypeDef,
    ListCreateAccountStatusRequestPaginateTypeDef,
    ListCreateAccountStatusResponseTypeDef,
    ListDelegatedAdministratorsRequestPaginateTypeDef,
    ListDelegatedAdministratorsResponseTypeDef,
    ListDelegatedServicesForAccountRequestPaginateTypeDef,
    ListDelegatedServicesForAccountResponseTypeDef,
    ListHandshakesForAccountRequestPaginateTypeDef,
    ListHandshakesForAccountResponsePaginatorTypeDef,
    ListHandshakesForOrganizationRequestPaginateTypeDef,
    ListHandshakesForOrganizationResponsePaginatorTypeDef,
    ListOrganizationalUnitsForParentRequestPaginateTypeDef,
    ListOrganizationalUnitsForParentResponseTypeDef,
    ListParentsRequestPaginateTypeDef,
    ListParentsResponseTypeDef,
    ListPoliciesForTargetRequestPaginateTypeDef,
    ListPoliciesForTargetResponseTypeDef,
    ListPoliciesRequestPaginateTypeDef,
    ListPoliciesResponseTypeDef,
    ListRootsRequestPaginateTypeDef,
    ListRootsResponseTypeDef,
    ListTagsForResourceRequestPaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTargetsForPolicyRequestPaginateTypeDef,
    ListTargetsForPolicyResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAWSServiceAccessForOrganizationPaginator",
    "ListAccountsForParentPaginator",
    "ListAccountsPaginator",
    "ListChildrenPaginator",
    "ListCreateAccountStatusPaginator",
    "ListDelegatedAdministratorsPaginator",
    "ListDelegatedServicesForAccountPaginator",
    "ListHandshakesForAccountPaginator",
    "ListHandshakesForOrganizationPaginator",
    "ListOrganizationalUnitsForParentPaginator",
    "ListParentsPaginator",
    "ListPoliciesForTargetPaginator",
    "ListPoliciesPaginator",
    "ListRootsPaginator",
    "ListTagsForResourcePaginator",
    "ListTargetsForPolicyPaginator",
)


if TYPE_CHECKING:
    _ListAWSServiceAccessForOrganizationPaginatorBase = AioPaginator[
        ListAWSServiceAccessForOrganizationResponseTypeDef
    ]
else:
    _ListAWSServiceAccessForOrganizationPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAWSServiceAccessForOrganizationPaginator(
    _ListAWSServiceAccessForOrganizationPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListAWSServiceAccessForOrganization.html#Organizations.Paginator.ListAWSServiceAccessForOrganization)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listawsserviceaccessfororganizationpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAWSServiceAccessForOrganizationRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAWSServiceAccessForOrganizationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListAWSServiceAccessForOrganization.html#Organizations.Paginator.ListAWSServiceAccessForOrganization.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listawsserviceaccessfororganizationpaginator)
        """


if TYPE_CHECKING:
    _ListAccountsForParentPaginatorBase = AioPaginator[ListAccountsForParentResponseTypeDef]
else:
    _ListAccountsForParentPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAccountsForParentPaginator(_ListAccountsForParentPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListAccountsForParent.html#Organizations.Paginator.ListAccountsForParent)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listaccountsforparentpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccountsForParentRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAccountsForParentResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListAccountsForParent.html#Organizations.Paginator.ListAccountsForParent.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listaccountsforparentpaginator)
        """


if TYPE_CHECKING:
    _ListAccountsPaginatorBase = AioPaginator[ListAccountsResponseTypeDef]
else:
    _ListAccountsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAccountsPaginator(_ListAccountsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListAccounts.html#Organizations.Paginator.ListAccounts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listaccountspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccountsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListAccounts.html#Organizations.Paginator.ListAccounts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listaccountspaginator)
        """


if TYPE_CHECKING:
    _ListChildrenPaginatorBase = AioPaginator[ListChildrenResponseTypeDef]
else:
    _ListChildrenPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListChildrenPaginator(_ListChildrenPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListChildren.html#Organizations.Paginator.ListChildren)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listchildrenpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListChildrenRequestPaginateTypeDef]
    ) -> AioPageIterator[ListChildrenResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListChildren.html#Organizations.Paginator.ListChildren.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listchildrenpaginator)
        """


if TYPE_CHECKING:
    _ListCreateAccountStatusPaginatorBase = AioPaginator[ListCreateAccountStatusResponseTypeDef]
else:
    _ListCreateAccountStatusPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCreateAccountStatusPaginator(_ListCreateAccountStatusPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListCreateAccountStatus.html#Organizations.Paginator.ListCreateAccountStatus)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listcreateaccountstatuspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCreateAccountStatusRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCreateAccountStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListCreateAccountStatus.html#Organizations.Paginator.ListCreateAccountStatus.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listcreateaccountstatuspaginator)
        """


if TYPE_CHECKING:
    _ListDelegatedAdministratorsPaginatorBase = AioPaginator[
        ListDelegatedAdministratorsResponseTypeDef
    ]
else:
    _ListDelegatedAdministratorsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDelegatedAdministratorsPaginator(_ListDelegatedAdministratorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListDelegatedAdministrators.html#Organizations.Paginator.ListDelegatedAdministrators)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listdelegatedadministratorspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDelegatedAdministratorsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDelegatedAdministratorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListDelegatedAdministrators.html#Organizations.Paginator.ListDelegatedAdministrators.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listdelegatedadministratorspaginator)
        """


if TYPE_CHECKING:
    _ListDelegatedServicesForAccountPaginatorBase = AioPaginator[
        ListDelegatedServicesForAccountResponseTypeDef
    ]
else:
    _ListDelegatedServicesForAccountPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDelegatedServicesForAccountPaginator(_ListDelegatedServicesForAccountPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListDelegatedServicesForAccount.html#Organizations.Paginator.ListDelegatedServicesForAccount)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listdelegatedservicesforaccountpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDelegatedServicesForAccountRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDelegatedServicesForAccountResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListDelegatedServicesForAccount.html#Organizations.Paginator.ListDelegatedServicesForAccount.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listdelegatedservicesforaccountpaginator)
        """


if TYPE_CHECKING:
    _ListHandshakesForAccountPaginatorBase = AioPaginator[
        ListHandshakesForAccountResponsePaginatorTypeDef
    ]
else:
    _ListHandshakesForAccountPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListHandshakesForAccountPaginator(_ListHandshakesForAccountPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListHandshakesForAccount.html#Organizations.Paginator.ListHandshakesForAccount)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listhandshakesforaccountpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListHandshakesForAccountRequestPaginateTypeDef]
    ) -> AioPageIterator[ListHandshakesForAccountResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListHandshakesForAccount.html#Organizations.Paginator.ListHandshakesForAccount.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listhandshakesforaccountpaginator)
        """


if TYPE_CHECKING:
    _ListHandshakesForOrganizationPaginatorBase = AioPaginator[
        ListHandshakesForOrganizationResponsePaginatorTypeDef
    ]
else:
    _ListHandshakesForOrganizationPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListHandshakesForOrganizationPaginator(_ListHandshakesForOrganizationPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListHandshakesForOrganization.html#Organizations.Paginator.ListHandshakesForOrganization)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listhandshakesfororganizationpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListHandshakesForOrganizationRequestPaginateTypeDef]
    ) -> AioPageIterator[ListHandshakesForOrganizationResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListHandshakesForOrganization.html#Organizations.Paginator.ListHandshakesForOrganization.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listhandshakesfororganizationpaginator)
        """


if TYPE_CHECKING:
    _ListOrganizationalUnitsForParentPaginatorBase = AioPaginator[
        ListOrganizationalUnitsForParentResponseTypeDef
    ]
else:
    _ListOrganizationalUnitsForParentPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListOrganizationalUnitsForParentPaginator(_ListOrganizationalUnitsForParentPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListOrganizationalUnitsForParent.html#Organizations.Paginator.ListOrganizationalUnitsForParent)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listorganizationalunitsforparentpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOrganizationalUnitsForParentRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOrganizationalUnitsForParentResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListOrganizationalUnitsForParent.html#Organizations.Paginator.ListOrganizationalUnitsForParent.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listorganizationalunitsforparentpaginator)
        """


if TYPE_CHECKING:
    _ListParentsPaginatorBase = AioPaginator[ListParentsResponseTypeDef]
else:
    _ListParentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListParentsPaginator(_ListParentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListParents.html#Organizations.Paginator.ListParents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listparentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListParentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListParentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListParents.html#Organizations.Paginator.ListParents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listparentspaginator)
        """


if TYPE_CHECKING:
    _ListPoliciesForTargetPaginatorBase = AioPaginator[ListPoliciesForTargetResponseTypeDef]
else:
    _ListPoliciesForTargetPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPoliciesForTargetPaginator(_ListPoliciesForTargetPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListPoliciesForTarget.html#Organizations.Paginator.ListPoliciesForTarget)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listpoliciesfortargetpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPoliciesForTargetRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPoliciesForTargetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListPoliciesForTarget.html#Organizations.Paginator.ListPoliciesForTarget.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listpoliciesfortargetpaginator)
        """


if TYPE_CHECKING:
    _ListPoliciesPaginatorBase = AioPaginator[ListPoliciesResponseTypeDef]
else:
    _ListPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPoliciesPaginator(_ListPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListPolicies.html#Organizations.Paginator.ListPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listpoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListPolicies.html#Organizations.Paginator.ListPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listpoliciespaginator)
        """


if TYPE_CHECKING:
    _ListRootsPaginatorBase = AioPaginator[ListRootsResponseTypeDef]
else:
    _ListRootsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRootsPaginator(_ListRootsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListRoots.html#Organizations.Paginator.ListRoots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listrootspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRootsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRootsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListRoots.html#Organizations.Paginator.ListRoots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listrootspaginator)
        """


if TYPE_CHECKING:
    _ListTagsForResourcePaginatorBase = AioPaginator[ListTagsForResourceResponseTypeDef]
else:
    _ListTagsForResourcePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTagsForResourcePaginator(_ListTagsForResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListTagsForResource.html#Organizations.Paginator.ListTagsForResource)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listtagsforresourcepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsForResourceRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListTagsForResource.html#Organizations.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listtagsforresourcepaginator)
        """


if TYPE_CHECKING:
    _ListTargetsForPolicyPaginatorBase = AioPaginator[ListTargetsForPolicyResponseTypeDef]
else:
    _ListTargetsForPolicyPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTargetsForPolicyPaginator(_ListTargetsForPolicyPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListTargetsForPolicy.html#Organizations.Paginator.ListTargetsForPolicy)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listtargetsforpolicypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTargetsForPolicyRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTargetsForPolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/paginator/ListTargetsForPolicy.html#Organizations.Paginator.ListTargetsForPolicy.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listtargetsforpolicypaginator)
        """
