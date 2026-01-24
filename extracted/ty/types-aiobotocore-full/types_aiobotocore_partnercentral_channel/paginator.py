"""
Type annotations for partnercentral-channel service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_channel/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_partnercentral_channel.client import PartnerCentralChannelAPIClient
    from types_aiobotocore_partnercentral_channel.paginator import (
        ListChannelHandshakesPaginator,
        ListProgramManagementAccountsPaginator,
        ListRelationshipsPaginator,
    )

    session = get_session()
    with session.create_client("partnercentral-channel") as client:
        client: PartnerCentralChannelAPIClient

        list_channel_handshakes_paginator: ListChannelHandshakesPaginator = client.get_paginator("list_channel_handshakes")
        list_program_management_accounts_paginator: ListProgramManagementAccountsPaginator = client.get_paginator("list_program_management_accounts")
        list_relationships_paginator: ListRelationshipsPaginator = client.get_paginator("list_relationships")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListChannelHandshakesRequestPaginateTypeDef,
    ListChannelHandshakesResponseTypeDef,
    ListProgramManagementAccountsRequestPaginateTypeDef,
    ListProgramManagementAccountsResponseTypeDef,
    ListRelationshipsRequestPaginateTypeDef,
    ListRelationshipsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListChannelHandshakesPaginator",
    "ListProgramManagementAccountsPaginator",
    "ListRelationshipsPaginator",
)


if TYPE_CHECKING:
    _ListChannelHandshakesPaginatorBase = AioPaginator[ListChannelHandshakesResponseTypeDef]
else:
    _ListChannelHandshakesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListChannelHandshakesPaginator(_ListChannelHandshakesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-channel/paginator/ListChannelHandshakes.html#PartnerCentralChannelAPI.Paginator.ListChannelHandshakes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_channel/paginators/#listchannelhandshakespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListChannelHandshakesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListChannelHandshakesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-channel/paginator/ListChannelHandshakes.html#PartnerCentralChannelAPI.Paginator.ListChannelHandshakes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_channel/paginators/#listchannelhandshakespaginator)
        """


if TYPE_CHECKING:
    _ListProgramManagementAccountsPaginatorBase = AioPaginator[
        ListProgramManagementAccountsResponseTypeDef
    ]
else:
    _ListProgramManagementAccountsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListProgramManagementAccountsPaginator(_ListProgramManagementAccountsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-channel/paginator/ListProgramManagementAccounts.html#PartnerCentralChannelAPI.Paginator.ListProgramManagementAccounts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_channel/paginators/#listprogrammanagementaccountspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProgramManagementAccountsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProgramManagementAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-channel/paginator/ListProgramManagementAccounts.html#PartnerCentralChannelAPI.Paginator.ListProgramManagementAccounts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_channel/paginators/#listprogrammanagementaccountspaginator)
        """


if TYPE_CHECKING:
    _ListRelationshipsPaginatorBase = AioPaginator[ListRelationshipsResponseTypeDef]
else:
    _ListRelationshipsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRelationshipsPaginator(_ListRelationshipsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-channel/paginator/ListRelationships.html#PartnerCentralChannelAPI.Paginator.ListRelationships)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_channel/paginators/#listrelationshipspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRelationshipsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRelationshipsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-channel/paginator/ListRelationships.html#PartnerCentralChannelAPI.Paginator.ListRelationships.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_channel/paginators/#listrelationshipspaginator)
        """
