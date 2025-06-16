"""
Type annotations for ram service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ram.client import RAMClient
    from types_aiobotocore_ram.paginator import (
        GetResourcePoliciesPaginator,
        GetResourceShareAssociationsPaginator,
        GetResourceShareInvitationsPaginator,
        GetResourceSharesPaginator,
        ListPrincipalsPaginator,
        ListResourcesPaginator,
    )

    session = get_session()
    with session.create_client("ram") as client:
        client: RAMClient

        get_resource_policies_paginator: GetResourcePoliciesPaginator = client.get_paginator("get_resource_policies")
        get_resource_share_associations_paginator: GetResourceShareAssociationsPaginator = client.get_paginator("get_resource_share_associations")
        get_resource_share_invitations_paginator: GetResourceShareInvitationsPaginator = client.get_paginator("get_resource_share_invitations")
        get_resource_shares_paginator: GetResourceSharesPaginator = client.get_paginator("get_resource_shares")
        list_principals_paginator: ListPrincipalsPaginator = client.get_paginator("list_principals")
        list_resources_paginator: ListResourcesPaginator = client.get_paginator("list_resources")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetResourcePoliciesRequestPaginateTypeDef,
    GetResourcePoliciesResponseTypeDef,
    GetResourceShareAssociationsRequestPaginateTypeDef,
    GetResourceShareAssociationsResponseTypeDef,
    GetResourceShareInvitationsRequestPaginateTypeDef,
    GetResourceShareInvitationsResponseTypeDef,
    GetResourceSharesRequestPaginateTypeDef,
    GetResourceSharesResponseTypeDef,
    ListPrincipalsRequestPaginateTypeDef,
    ListPrincipalsResponseTypeDef,
    ListResourcesRequestPaginateTypeDef,
    ListResourcesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetResourcePoliciesPaginator",
    "GetResourceShareAssociationsPaginator",
    "GetResourceShareInvitationsPaginator",
    "GetResourceSharesPaginator",
    "ListPrincipalsPaginator",
    "ListResourcesPaginator",
)

if TYPE_CHECKING:
    _GetResourcePoliciesPaginatorBase = AioPaginator[GetResourcePoliciesResponseTypeDef]
else:
    _GetResourcePoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetResourcePoliciesPaginator(_GetResourcePoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/GetResourcePolicies.html#RAM.Paginator.GetResourcePolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#getresourcepoliciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetResourcePoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetResourcePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/GetResourcePolicies.html#RAM.Paginator.GetResourcePolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#getresourcepoliciespaginator)
        """

if TYPE_CHECKING:
    _GetResourceShareAssociationsPaginatorBase = AioPaginator[
        GetResourceShareAssociationsResponseTypeDef
    ]
else:
    _GetResourceShareAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetResourceShareAssociationsPaginator(_GetResourceShareAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/GetResourceShareAssociations.html#RAM.Paginator.GetResourceShareAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#getresourceshareassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetResourceShareAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetResourceShareAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/GetResourceShareAssociations.html#RAM.Paginator.GetResourceShareAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#getresourceshareassociationspaginator)
        """

if TYPE_CHECKING:
    _GetResourceShareInvitationsPaginatorBase = AioPaginator[
        GetResourceShareInvitationsResponseTypeDef
    ]
else:
    _GetResourceShareInvitationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetResourceShareInvitationsPaginator(_GetResourceShareInvitationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/GetResourceShareInvitations.html#RAM.Paginator.GetResourceShareInvitations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#getresourceshareinvitationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetResourceShareInvitationsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetResourceShareInvitationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/GetResourceShareInvitations.html#RAM.Paginator.GetResourceShareInvitations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#getresourceshareinvitationspaginator)
        """

if TYPE_CHECKING:
    _GetResourceSharesPaginatorBase = AioPaginator[GetResourceSharesResponseTypeDef]
else:
    _GetResourceSharesPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetResourceSharesPaginator(_GetResourceSharesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/GetResourceShares.html#RAM.Paginator.GetResourceShares)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#getresourcesharespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetResourceSharesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetResourceSharesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/GetResourceShares.html#RAM.Paginator.GetResourceShares.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#getresourcesharespaginator)
        """

if TYPE_CHECKING:
    _ListPrincipalsPaginatorBase = AioPaginator[ListPrincipalsResponseTypeDef]
else:
    _ListPrincipalsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPrincipalsPaginator(_ListPrincipalsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/ListPrincipals.html#RAM.Paginator.ListPrincipals)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#listprincipalspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPrincipalsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPrincipalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/ListPrincipals.html#RAM.Paginator.ListPrincipals.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#listprincipalspaginator)
        """

if TYPE_CHECKING:
    _ListResourcesPaginatorBase = AioPaginator[ListResourcesResponseTypeDef]
else:
    _ListResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListResourcesPaginator(_ListResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/ListResources.html#RAM.Paginator.ListResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#listresourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram/paginator/ListResources.html#RAM.Paginator.ListResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#listresourcespaginator)
        """
