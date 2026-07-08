"""
Type annotations for partnercentral-revenue-measurement service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_partnercentral_revenue_measurement.client import PartnerCentralRevenueMeasurementAPIClient

    session = Session()
    client: PartnerCentralRevenueMeasurementAPIClient = session.client("partnercentral-revenue-measurement")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListMarketplaceRevenueShareAllocationsPaginator,
    ListMarketplaceRevenueSharesPaginator,
    ListRevenueAttributionAllocationsPaginator,
    ListRevenueAttributionsPaginator,
)
from .type_defs import (
    CreateMarketplaceRevenueShareAllocationInputTypeDef,
    CreateMarketplaceRevenueShareAllocationOutputTypeDef,
    CreateMarketplaceRevenueShareInputTypeDef,
    CreateMarketplaceRevenueShareOutputTypeDef,
    CreateRevenueAttributionInputTypeDef,
    CreateRevenueAttributionOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    GetMarketplaceRevenueShareAllocationInputTypeDef,
    GetMarketplaceRevenueShareAllocationOutputTypeDef,
    GetMarketplaceRevenueShareInputTypeDef,
    GetMarketplaceRevenueShareOutputTypeDef,
    GetRevenueAttributionAllocationInputTypeDef,
    GetRevenueAttributionAllocationOutputTypeDef,
    GetRevenueAttributionAllocationsTaskInputTypeDef,
    GetRevenueAttributionAllocationsTaskOutputTypeDef,
    GetRevenueAttributionInputTypeDef,
    GetRevenueAttributionOutputTypeDef,
    ListMarketplaceRevenueShareAllocationsInputTypeDef,
    ListMarketplaceRevenueShareAllocationsOutputTypeDef,
    ListMarketplaceRevenueSharesInputTypeDef,
    ListMarketplaceRevenueSharesOutputTypeDef,
    ListRevenueAttributionAllocationsInputTypeDef,
    ListRevenueAttributionAllocationsOutputTypeDef,
    ListRevenueAttributionsInputTypeDef,
    ListRevenueAttributionsOutputTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    StartRevenueAttributionAllocationsTaskInputTypeDef,
    StartRevenueAttributionAllocationsTaskOutputTypeDef,
    TagResourceInputTypeDef,
    UntagResourceInputTypeDef,
    UpdateMarketplaceRevenueShareAllocationInputTypeDef,
    UpdateMarketplaceRevenueShareAllocationOutputTypeDef,
    UpdateRevenueAttributionInputTypeDef,
    UpdateRevenueAttributionOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("PartnerCentralRevenueMeasurementAPIClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class PartnerCentralRevenueMeasurementAPIClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement.html#PartnerCentralRevenueMeasurementAPI.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PartnerCentralRevenueMeasurementAPIClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement.html#PartnerCentralRevenueMeasurementAPI.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#generate_presigned_url)
        """

    def create_marketplace_revenue_share(
        self, **kwargs: Unpack[CreateMarketplaceRevenueShareInputTypeDef]
    ) -> CreateMarketplaceRevenueShareOutputTypeDef:
        """
        Creates a new marketplace revenue share resource in the specified catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/create_marketplace_revenue_share.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#create_marketplace_revenue_share)
        """

    def create_marketplace_revenue_share_allocation(
        self, **kwargs: Unpack[CreateMarketplaceRevenueShareAllocationInputTypeDef]
    ) -> CreateMarketplaceRevenueShareAllocationOutputTypeDef:
        """
        Creates a new marketplace revenue share allocation for the specified product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/create_marketplace_revenue_share_allocation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#create_marketplace_revenue_share_allocation)
        """

    def create_revenue_attribution(
        self, **kwargs: Unpack[CreateRevenueAttributionInputTypeDef]
    ) -> CreateRevenueAttributionOutputTypeDef:
        """
        Creates a new revenue attribution record in the specified catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/create_revenue_attribution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#create_revenue_attribution)
        """

    def get_marketplace_revenue_share(
        self, **kwargs: Unpack[GetMarketplaceRevenueShareInputTypeDef]
    ) -> GetMarketplaceRevenueShareOutputTypeDef:
        """
        Retrieves the details of a specific marketplace revenue share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/get_marketplace_revenue_share.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#get_marketplace_revenue_share)
        """

    def get_marketplace_revenue_share_allocation(
        self, **kwargs: Unpack[GetMarketplaceRevenueShareAllocationInputTypeDef]
    ) -> GetMarketplaceRevenueShareAllocationOutputTypeDef:
        """
        Retrieves the details of a specific marketplace revenue share allocation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/get_marketplace_revenue_share_allocation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#get_marketplace_revenue_share_allocation)
        """

    def get_revenue_attribution(
        self, **kwargs: Unpack[GetRevenueAttributionInputTypeDef]
    ) -> GetRevenueAttributionOutputTypeDef:
        """
        Retrieves the details of a specific revenue attribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/get_revenue_attribution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#get_revenue_attribution)
        """

    def get_revenue_attribution_allocation(
        self, **kwargs: Unpack[GetRevenueAttributionAllocationInputTypeDef]
    ) -> GetRevenueAttributionAllocationOutputTypeDef:
        """
        Retrieves a single allocation by its RevenueAttributionAllocationId.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/get_revenue_attribution_allocation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#get_revenue_attribution_allocation)
        """

    def get_revenue_attribution_allocations_task(
        self, **kwargs: Unpack[GetRevenueAttributionAllocationsTaskInputTypeDef]
    ) -> GetRevenueAttributionAllocationsTaskOutputTypeDef:
        """
        Retrieves the current status of a previously submitted allocations task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/get_revenue_attribution_allocations_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#get_revenue_attribution_allocations_task)
        """

    def list_marketplace_revenue_share_allocations(
        self, **kwargs: Unpack[ListMarketplaceRevenueShareAllocationsInputTypeDef]
    ) -> ListMarketplaceRevenueShareAllocationsOutputTypeDef:
        """
        Returns a paginated list of allocations under a marketplace revenue share, with
        optional filtering by status and effective date range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/list_marketplace_revenue_share_allocations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#list_marketplace_revenue_share_allocations)
        """

    def list_marketplace_revenue_shares(
        self, **kwargs: Unpack[ListMarketplaceRevenueSharesInputTypeDef]
    ) -> ListMarketplaceRevenueSharesOutputTypeDef:
        """
        Returns a paginated list of marketplace revenue shares with optional filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/list_marketplace_revenue_shares.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#list_marketplace_revenue_shares)
        """

    def list_revenue_attribution_allocations(
        self, **kwargs: Unpack[ListRevenueAttributionAllocationsInputTypeDef]
    ) -> ListRevenueAttributionAllocationsOutputTypeDef:
        """
        Returns a paginated list of committed allocations with support for filtering by
        entity, customer, status, or date range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/list_revenue_attribution_allocations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#list_revenue_attribution_allocations)
        """

    def list_revenue_attributions(
        self, **kwargs: Unpack[ListRevenueAttributionsInputTypeDef]
    ) -> ListRevenueAttributionsOutputTypeDef:
        """
        Returns a paginated list of revenue attributions with optional filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/list_revenue_attributions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#list_revenue_attributions)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Returns the tags associated with the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#list_tags_for_resource)
        """

    def start_revenue_attribution_allocations_task(
        self, **kwargs: Unpack[StartRevenueAttributionAllocationsTaskInputTypeDef]
    ) -> StartRevenueAttributionAllocationsTaskOutputTypeDef:
        """
        Submits a batch of up to 250 allocation changes (CREATE and/or UPDATE) for
        asynchronous processing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/start_revenue_attribution_allocations_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#start_revenue_attribution_allocations_task)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or overwrites one or more tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#untag_resource)
        """

    def update_marketplace_revenue_share_allocation(
        self, **kwargs: Unpack[UpdateMarketplaceRevenueShareAllocationInputTypeDef]
    ) -> UpdateMarketplaceRevenueShareAllocationOutputTypeDef:
        """
        Updates an existing marketplace revenue share allocation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/update_marketplace_revenue_share_allocation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#update_marketplace_revenue_share_allocation)
        """

    def update_revenue_attribution(
        self, **kwargs: Unpack[UpdateRevenueAttributionInputTypeDef]
    ) -> UpdateRevenueAttributionOutputTypeDef:
        """
        Updates an existing revenue attribution record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/update_revenue_attribution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#update_revenue_attribution)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_marketplace_revenue_share_allocations"]
    ) -> ListMarketplaceRevenueShareAllocationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_marketplace_revenue_shares"]
    ) -> ListMarketplaceRevenueSharesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_revenue_attribution_allocations"]
    ) -> ListRevenueAttributionAllocationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_revenue_attributions"]
    ) -> ListRevenueAttributionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/client/#get_paginator)
        """
