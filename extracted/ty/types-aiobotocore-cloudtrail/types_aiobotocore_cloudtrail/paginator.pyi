"""
Type annotations for cloudtrail service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudtrail.client import CloudTrailClient
    from types_aiobotocore_cloudtrail.paginator import (
        ListImportFailuresPaginator,
        ListImportsPaginator,
        ListPublicKeysPaginator,
        ListTagsPaginator,
        ListTrailsPaginator,
        LookupEventsPaginator,
    )

    session = get_session()
    with session.create_client("cloudtrail") as client:
        client: CloudTrailClient

        list_import_failures_paginator: ListImportFailuresPaginator = client.get_paginator("list_import_failures")
        list_imports_paginator: ListImportsPaginator = client.get_paginator("list_imports")
        list_public_keys_paginator: ListPublicKeysPaginator = client.get_paginator("list_public_keys")
        list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
        list_trails_paginator: ListTrailsPaginator = client.get_paginator("list_trails")
        lookup_events_paginator: LookupEventsPaginator = client.get_paginator("lookup_events")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListImportFailuresRequestPaginateTypeDef,
    ListImportFailuresResponseTypeDef,
    ListImportsRequestPaginateTypeDef,
    ListImportsResponseTypeDef,
    ListPublicKeysRequestPaginateTypeDef,
    ListPublicKeysResponseTypeDef,
    ListTagsRequestPaginateTypeDef,
    ListTagsResponseTypeDef,
    ListTrailsRequestPaginateTypeDef,
    ListTrailsResponseTypeDef,
    LookupEventsRequestPaginateTypeDef,
    LookupEventsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListImportFailuresPaginator",
    "ListImportsPaginator",
    "ListPublicKeysPaginator",
    "ListTagsPaginator",
    "ListTrailsPaginator",
    "LookupEventsPaginator",
)

if TYPE_CHECKING:
    _ListImportFailuresPaginatorBase = AioPaginator[ListImportFailuresResponseTypeDef]
else:
    _ListImportFailuresPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListImportFailuresPaginator(_ListImportFailuresPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/ListImportFailures.html#CloudTrail.Paginator.ListImportFailures)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#listimportfailurespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImportFailuresRequestPaginateTypeDef]
    ) -> AioPageIterator[ListImportFailuresResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/ListImportFailures.html#CloudTrail.Paginator.ListImportFailures.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#listimportfailurespaginator)
        """

if TYPE_CHECKING:
    _ListImportsPaginatorBase = AioPaginator[ListImportsResponseTypeDef]
else:
    _ListImportsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListImportsPaginator(_ListImportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/ListImports.html#CloudTrail.Paginator.ListImports)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#listimportspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImportsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListImportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/ListImports.html#CloudTrail.Paginator.ListImports.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#listimportspaginator)
        """

if TYPE_CHECKING:
    _ListPublicKeysPaginatorBase = AioPaginator[ListPublicKeysResponseTypeDef]
else:
    _ListPublicKeysPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPublicKeysPaginator(_ListPublicKeysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/ListPublicKeys.html#CloudTrail.Paginator.ListPublicKeys)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#listpublickeyspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPublicKeysRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPublicKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/ListPublicKeys.html#CloudTrail.Paginator.ListPublicKeys.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#listpublickeyspaginator)
        """

if TYPE_CHECKING:
    _ListTagsPaginatorBase = AioPaginator[ListTagsResponseTypeDef]
else:
    _ListTagsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTagsPaginator(_ListTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/ListTags.html#CloudTrail.Paginator.ListTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#listtagspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/ListTags.html#CloudTrail.Paginator.ListTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#listtagspaginator)
        """

if TYPE_CHECKING:
    _ListTrailsPaginatorBase = AioPaginator[ListTrailsResponseTypeDef]
else:
    _ListTrailsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTrailsPaginator(_ListTrailsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/ListTrails.html#CloudTrail.Paginator.ListTrails)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#listtrailspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTrailsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTrailsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/ListTrails.html#CloudTrail.Paginator.ListTrails.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#listtrailspaginator)
        """

if TYPE_CHECKING:
    _LookupEventsPaginatorBase = AioPaginator[LookupEventsResponseTypeDef]
else:
    _LookupEventsPaginatorBase = AioPaginator  # type: ignore[assignment]

class LookupEventsPaginator(_LookupEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/LookupEvents.html#CloudTrail.Paginator.LookupEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#lookupeventspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[LookupEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[LookupEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/LookupEvents.html#CloudTrail.Paginator.LookupEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#lookupeventspaginator)
        """
