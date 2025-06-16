"""
Type annotations for marketplacecommerceanalytics service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplacecommerceanalytics/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_marketplacecommerceanalytics.client import MarketplaceCommerceAnalyticsClient

    session = get_session()
    async with session.create_client("marketplacecommerceanalytics") as client:
        client: MarketplaceCommerceAnalyticsClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    GenerateDataSetRequestTypeDef,
    GenerateDataSetResultTypeDef,
    StartSupportDataExportRequestTypeDef,
    StartSupportDataExportResultTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Self, Unpack
else:
    from typing_extensions import Self, Unpack


__all__ = ("MarketplaceCommerceAnalyticsClient",)


class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    MarketplaceCommerceAnalyticsException: Type[BotocoreClientError]


class MarketplaceCommerceAnalyticsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplacecommerceanalytics.html#MarketplaceCommerceAnalytics.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplacecommerceanalytics/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MarketplaceCommerceAnalyticsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplacecommerceanalytics.html#MarketplaceCommerceAnalytics.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplacecommerceanalytics/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplacecommerceanalytics/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplacecommerceanalytics/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplacecommerceanalytics/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplacecommerceanalytics/client/#generate_presigned_url)
        """

    async def generate_data_set(
        self, **kwargs: Unpack[GenerateDataSetRequestTypeDef]
    ) -> GenerateDataSetResultTypeDef:
        """
        Given a data set type and data set publication date, asynchronously publishes
        the requested data set to the specified S3 bucket and notifies the specified
        SNS topic once the data is available.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplacecommerceanalytics/client/generate_data_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplacecommerceanalytics/client/#generate_data_set)
        """

    async def start_support_data_export(
        self, **kwargs: Unpack[StartSupportDataExportRequestTypeDef]
    ) -> StartSupportDataExportResultTypeDef:
        """
        <i>This target has been deprecated.</i> Given a data set type and a from date,
        asynchronously publishes the requested customer support data to the specified
        S3 bucket and notifies the specified SNS topic once the data is available.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplacecommerceanalytics/client/start_support_data_export.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplacecommerceanalytics/client/#start_support_data_export)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplacecommerceanalytics.html#MarketplaceCommerceAnalytics.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplacecommerceanalytics/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplacecommerceanalytics.html#MarketplaceCommerceAnalytics.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplacecommerceanalytics/client/)
        """
