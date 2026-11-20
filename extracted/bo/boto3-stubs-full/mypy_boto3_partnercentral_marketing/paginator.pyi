"""
Type annotations for partnercentral-marketing service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_marketing/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_partnercentral_marketing.client import PartnerCentralMarketingClient
    from mypy_boto3_partnercentral_marketing.paginator import (
        ListCampaignAssetsPaginator,
        ListCampaignsPaginator,
        ListSocialConnectionsPaginator,
        SearchCampaignTemplatesPaginator,
    )

    session = Session()
    client: PartnerCentralMarketingClient = session.client("partnercentral-marketing")

    list_campaign_assets_paginator: ListCampaignAssetsPaginator = client.get_paginator("list_campaign_assets")
    list_campaigns_paginator: ListCampaignsPaginator = client.get_paginator("list_campaigns")
    list_social_connections_paginator: ListSocialConnectionsPaginator = client.get_paginator("list_social_connections")
    search_campaign_templates_paginator: SearchCampaignTemplatesPaginator = client.get_paginator("search_campaign_templates")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListCampaignAssetsRequestPaginateTypeDef,
    ListCampaignAssetsResponseTypeDef,
    ListCampaignsRequestPaginateTypeDef,
    ListCampaignsResponseTypeDef,
    ListSocialConnectionsRequestPaginateTypeDef,
    ListSocialConnectionsResponseTypeDef,
    SearchCampaignTemplatesRequestPaginateTypeDef,
    SearchCampaignTemplatesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListCampaignAssetsPaginator",
    "ListCampaignsPaginator",
    "ListSocialConnectionsPaginator",
    "SearchCampaignTemplatesPaginator",
)

if TYPE_CHECKING:
    _ListCampaignAssetsPaginatorBase = Paginator[ListCampaignAssetsResponseTypeDef]
else:
    _ListCampaignAssetsPaginatorBase = Paginator  # type: ignore[assignment]

class ListCampaignAssetsPaginator(_ListCampaignAssetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/paginator/ListCampaignAssets.html#PartnerCentralMarketing.Paginator.ListCampaignAssets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_marketing/paginators/#listcampaignassetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCampaignAssetsRequestPaginateTypeDef]
    ) -> PageIterator[ListCampaignAssetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/paginator/ListCampaignAssets.html#PartnerCentralMarketing.Paginator.ListCampaignAssets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_marketing/paginators/#listcampaignassetspaginator)
        """

if TYPE_CHECKING:
    _ListCampaignsPaginatorBase = Paginator[ListCampaignsResponseTypeDef]
else:
    _ListCampaignsPaginatorBase = Paginator  # type: ignore[assignment]

class ListCampaignsPaginator(_ListCampaignsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/paginator/ListCampaigns.html#PartnerCentralMarketing.Paginator.ListCampaigns)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_marketing/paginators/#listcampaignspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCampaignsRequestPaginateTypeDef]
    ) -> PageIterator[ListCampaignsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/paginator/ListCampaigns.html#PartnerCentralMarketing.Paginator.ListCampaigns.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_marketing/paginators/#listcampaignspaginator)
        """

if TYPE_CHECKING:
    _ListSocialConnectionsPaginatorBase = Paginator[ListSocialConnectionsResponseTypeDef]
else:
    _ListSocialConnectionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListSocialConnectionsPaginator(_ListSocialConnectionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/paginator/ListSocialConnections.html#PartnerCentralMarketing.Paginator.ListSocialConnections)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_marketing/paginators/#listsocialconnectionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSocialConnectionsRequestPaginateTypeDef]
    ) -> PageIterator[ListSocialConnectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/paginator/ListSocialConnections.html#PartnerCentralMarketing.Paginator.ListSocialConnections.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_marketing/paginators/#listsocialconnectionspaginator)
        """

if TYPE_CHECKING:
    _SearchCampaignTemplatesPaginatorBase = Paginator[SearchCampaignTemplatesResponseTypeDef]
else:
    _SearchCampaignTemplatesPaginatorBase = Paginator  # type: ignore[assignment]

class SearchCampaignTemplatesPaginator(_SearchCampaignTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/paginator/SearchCampaignTemplates.html#PartnerCentralMarketing.Paginator.SearchCampaignTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_marketing/paginators/#searchcampaigntemplatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchCampaignTemplatesRequestPaginateTypeDef]
    ) -> PageIterator[SearchCampaignTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-marketing/paginator/SearchCampaignTemplates.html#PartnerCentralMarketing.Paginator.SearchCampaignTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_marketing/paginators/#searchcampaigntemplatespaginator)
        """
