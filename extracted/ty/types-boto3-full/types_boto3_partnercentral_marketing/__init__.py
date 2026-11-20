"""
Main interface for partnercentral-marketing service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_marketing/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_partnercentral_marketing import (
        Client,
        ListCampaignAssetsPaginator,
        ListCampaignsPaginator,
        ListSocialConnectionsPaginator,
        PartnerCentralMarketingClient,
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

from .client import PartnerCentralMarketingClient
from .paginator import (
    ListCampaignAssetsPaginator,
    ListCampaignsPaginator,
    ListSocialConnectionsPaginator,
    SearchCampaignTemplatesPaginator,
)

Client = PartnerCentralMarketingClient


__all__ = (
    "Client",
    "ListCampaignAssetsPaginator",
    "ListCampaignsPaginator",
    "ListSocialConnectionsPaginator",
    "PartnerCentralMarketingClient",
    "SearchCampaignTemplatesPaginator",
)
