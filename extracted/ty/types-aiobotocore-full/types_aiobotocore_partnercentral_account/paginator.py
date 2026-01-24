"""
Type annotations for partnercentral-account service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_account/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_partnercentral_account.client import PartnerCentralAccountAPIClient
    from types_aiobotocore_partnercentral_account.paginator import (
        ListConnectionInvitationsPaginator,
        ListConnectionsPaginator,
        ListPartnersPaginator,
    )

    session = get_session()
    with session.create_client("partnercentral-account") as client:
        client: PartnerCentralAccountAPIClient

        list_connection_invitations_paginator: ListConnectionInvitationsPaginator = client.get_paginator("list_connection_invitations")
        list_connections_paginator: ListConnectionsPaginator = client.get_paginator("list_connections")
        list_partners_paginator: ListPartnersPaginator = client.get_paginator("list_partners")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListConnectionInvitationsRequestPaginateTypeDef,
    ListConnectionInvitationsResponseTypeDef,
    ListConnectionsRequestPaginateTypeDef,
    ListConnectionsResponseTypeDef,
    ListPartnersRequestPaginateTypeDef,
    ListPartnersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListConnectionInvitationsPaginator",
    "ListConnectionsPaginator",
    "ListPartnersPaginator",
)


if TYPE_CHECKING:
    _ListConnectionInvitationsPaginatorBase = AioPaginator[ListConnectionInvitationsResponseTypeDef]
else:
    _ListConnectionInvitationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListConnectionInvitationsPaginator(_ListConnectionInvitationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-account/paginator/ListConnectionInvitations.html#PartnerCentralAccountAPI.Paginator.ListConnectionInvitations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_account/paginators/#listconnectioninvitationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConnectionInvitationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListConnectionInvitationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-account/paginator/ListConnectionInvitations.html#PartnerCentralAccountAPI.Paginator.ListConnectionInvitations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_account/paginators/#listconnectioninvitationspaginator)
        """


if TYPE_CHECKING:
    _ListConnectionsPaginatorBase = AioPaginator[ListConnectionsResponseTypeDef]
else:
    _ListConnectionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListConnectionsPaginator(_ListConnectionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-account/paginator/ListConnections.html#PartnerCentralAccountAPI.Paginator.ListConnections)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_account/paginators/#listconnectionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConnectionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListConnectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-account/paginator/ListConnections.html#PartnerCentralAccountAPI.Paginator.ListConnections.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_account/paginators/#listconnectionspaginator)
        """


if TYPE_CHECKING:
    _ListPartnersPaginatorBase = AioPaginator[ListPartnersResponseTypeDef]
else:
    _ListPartnersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPartnersPaginator(_ListPartnersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-account/paginator/ListPartners.html#PartnerCentralAccountAPI.Paginator.ListPartners)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_account/paginators/#listpartnerspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPartnersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPartnersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-account/paginator/ListPartners.html#PartnerCentralAccountAPI.Paginator.ListPartners.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_account/paginators/#listpartnerspaginator)
        """
