"""
Type annotations for resourcegroupstaggingapi service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resourcegroupstaggingapi/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_resourcegroupstaggingapi.client import ResourceGroupsTaggingAPIClient
    from types_aiobotocore_resourcegroupstaggingapi.paginator import (
        GetComplianceSummaryPaginator,
        GetResourcesPaginator,
        GetTagKeysPaginator,
        GetTagValuesPaginator,
        ListRequiredTagsPaginator,
    )

    session = get_session()
    with session.create_client("resourcegroupstaggingapi") as client:
        client: ResourceGroupsTaggingAPIClient

        get_compliance_summary_paginator: GetComplianceSummaryPaginator = client.get_paginator("get_compliance_summary")
        get_resources_paginator: GetResourcesPaginator = client.get_paginator("get_resources")
        get_tag_keys_paginator: GetTagKeysPaginator = client.get_paginator("get_tag_keys")
        get_tag_values_paginator: GetTagValuesPaginator = client.get_paginator("get_tag_values")
        list_required_tags_paginator: ListRequiredTagsPaginator = client.get_paginator("list_required_tags")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetComplianceSummaryInputPaginateTypeDef,
    GetComplianceSummaryOutputTypeDef,
    GetResourcesInputPaginateTypeDef,
    GetResourcesOutputTypeDef,
    GetTagKeysInputPaginateTypeDef,
    GetTagKeysOutputTypeDef,
    GetTagValuesInputPaginateTypeDef,
    GetTagValuesOutputTypeDef,
    ListRequiredTagsInputPaginateTypeDef,
    ListRequiredTagsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetComplianceSummaryPaginator",
    "GetResourcesPaginator",
    "GetTagKeysPaginator",
    "GetTagValuesPaginator",
    "ListRequiredTagsPaginator",
)


if TYPE_CHECKING:
    _GetComplianceSummaryPaginatorBase = AioPaginator[GetComplianceSummaryOutputTypeDef]
else:
    _GetComplianceSummaryPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetComplianceSummaryPaginator(_GetComplianceSummaryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/paginator/GetComplianceSummary.html#ResourceGroupsTaggingAPI.Paginator.GetComplianceSummary)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resourcegroupstaggingapi/paginators/#getcompliancesummarypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetComplianceSummaryInputPaginateTypeDef]
    ) -> AioPageIterator[GetComplianceSummaryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/paginator/GetComplianceSummary.html#ResourceGroupsTaggingAPI.Paginator.GetComplianceSummary.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resourcegroupstaggingapi/paginators/#getcompliancesummarypaginator)
        """


if TYPE_CHECKING:
    _GetResourcesPaginatorBase = AioPaginator[GetResourcesOutputTypeDef]
else:
    _GetResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetResourcesPaginator(_GetResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/paginator/GetResources.html#ResourceGroupsTaggingAPI.Paginator.GetResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resourcegroupstaggingapi/paginators/#getresourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetResourcesInputPaginateTypeDef]
    ) -> AioPageIterator[GetResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/paginator/GetResources.html#ResourceGroupsTaggingAPI.Paginator.GetResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resourcegroupstaggingapi/paginators/#getresourcespaginator)
        """


if TYPE_CHECKING:
    _GetTagKeysPaginatorBase = AioPaginator[GetTagKeysOutputTypeDef]
else:
    _GetTagKeysPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetTagKeysPaginator(_GetTagKeysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/paginator/GetTagKeys.html#ResourceGroupsTaggingAPI.Paginator.GetTagKeys)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resourcegroupstaggingapi/paginators/#gettagkeyspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetTagKeysInputPaginateTypeDef]
    ) -> AioPageIterator[GetTagKeysOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/paginator/GetTagKeys.html#ResourceGroupsTaggingAPI.Paginator.GetTagKeys.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resourcegroupstaggingapi/paginators/#gettagkeyspaginator)
        """


if TYPE_CHECKING:
    _GetTagValuesPaginatorBase = AioPaginator[GetTagValuesOutputTypeDef]
else:
    _GetTagValuesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetTagValuesPaginator(_GetTagValuesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/paginator/GetTagValues.html#ResourceGroupsTaggingAPI.Paginator.GetTagValues)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resourcegroupstaggingapi/paginators/#gettagvaluespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetTagValuesInputPaginateTypeDef]
    ) -> AioPageIterator[GetTagValuesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/paginator/GetTagValues.html#ResourceGroupsTaggingAPI.Paginator.GetTagValues.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resourcegroupstaggingapi/paginators/#gettagvaluespaginator)
        """


if TYPE_CHECKING:
    _ListRequiredTagsPaginatorBase = AioPaginator[ListRequiredTagsOutputTypeDef]
else:
    _ListRequiredTagsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRequiredTagsPaginator(_ListRequiredTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/paginator/ListRequiredTags.html#ResourceGroupsTaggingAPI.Paginator.ListRequiredTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resourcegroupstaggingapi/paginators/#listrequiredtagspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRequiredTagsInputPaginateTypeDef]
    ) -> AioPageIterator[ListRequiredTagsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/paginator/ListRequiredTags.html#ResourceGroupsTaggingAPI.Paginator.ListRequiredTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resourcegroupstaggingapi/paginators/#listrequiredtagspaginator)
        """
