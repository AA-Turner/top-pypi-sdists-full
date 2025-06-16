"""
Type annotations for connectcampaignsv2 service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_connectcampaignsv2.client import ConnectCampaignServiceV2Client
    from types_aiobotocore_connectcampaignsv2.paginator import (
        ListCampaignsPaginator,
        ListConnectInstanceIntegrationsPaginator,
    )

    session = get_session()
    with session.create_client("connectcampaignsv2") as client:
        client: ConnectCampaignServiceV2Client

        list_campaigns_paginator: ListCampaignsPaginator = client.get_paginator("list_campaigns")
        list_connect_instance_integrations_paginator: ListConnectInstanceIntegrationsPaginator = client.get_paginator("list_connect_instance_integrations")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListCampaignsRequestPaginateTypeDef,
    ListCampaignsResponseTypeDef,
    ListConnectInstanceIntegrationsRequestPaginateTypeDef,
    ListConnectInstanceIntegrationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListCampaignsPaginator", "ListConnectInstanceIntegrationsPaginator")


if TYPE_CHECKING:
    _ListCampaignsPaginatorBase = AioPaginator[ListCampaignsResponseTypeDef]
else:
    _ListCampaignsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCampaignsPaginator(_ListCampaignsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/paginator/ListCampaigns.html#ConnectCampaignServiceV2.Paginator.ListCampaigns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/paginators/#listcampaignspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCampaignsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCampaignsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/paginator/ListCampaigns.html#ConnectCampaignServiceV2.Paginator.ListCampaigns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/paginators/#listcampaignspaginator)
        """


if TYPE_CHECKING:
    _ListConnectInstanceIntegrationsPaginatorBase = AioPaginator[
        ListConnectInstanceIntegrationsResponseTypeDef
    ]
else:
    _ListConnectInstanceIntegrationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListConnectInstanceIntegrationsPaginator(_ListConnectInstanceIntegrationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/paginator/ListConnectInstanceIntegrations.html#ConnectCampaignServiceV2.Paginator.ListConnectInstanceIntegrations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/paginators/#listconnectinstanceintegrationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConnectInstanceIntegrationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListConnectInstanceIntegrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/paginator/ListConnectInstanceIntegrations.html#ConnectCampaignServiceV2.Paginator.ListConnectInstanceIntegrations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/paginators/#listconnectinstanceintegrationspaginator)
        """
