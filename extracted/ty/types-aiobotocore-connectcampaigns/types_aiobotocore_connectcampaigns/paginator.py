"""
Type annotations for connectcampaigns service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_connectcampaigns.client import ConnectCampaignServiceClient
    from types_aiobotocore_connectcampaigns.paginator import (
        ListCampaignsPaginator,
    )

    session = get_session()
    with session.create_client("connectcampaigns") as client:
        client: ConnectCampaignServiceClient

        list_campaigns_paginator: ListCampaignsPaginator = client.get_paginator("list_campaigns")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListCampaignsRequestPaginateTypeDef, ListCampaignsResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListCampaignsPaginator",)


if TYPE_CHECKING:
    _ListCampaignsPaginatorBase = AioPaginator[ListCampaignsResponseTypeDef]
else:
    _ListCampaignsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCampaignsPaginator(_ListCampaignsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/paginator/ListCampaigns.html#ConnectCampaignService.Paginator.ListCampaigns)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/paginators/#listcampaignspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCampaignsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCampaignsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/paginator/ListCampaigns.html#ConnectCampaignService.Paginator.ListCampaigns.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/paginators/#listcampaignspaginator)
        """
