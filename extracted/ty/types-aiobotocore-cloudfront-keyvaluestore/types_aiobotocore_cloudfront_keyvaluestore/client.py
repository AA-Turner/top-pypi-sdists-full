"""
Type annotations for cloudfront-keyvaluestore service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront_keyvaluestore/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudfront_keyvaluestore.client import CloudFrontKeyValueStoreClient

    session = get_session()
    async with session.create_client("cloudfront-keyvaluestore") as client:
        client: CloudFrontKeyValueStoreClient
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

from .paginator import ListKeysPaginator
from .type_defs import (
    DeleteKeyRequestTypeDef,
    DeleteKeyResponseTypeDef,
    DescribeKeyValueStoreRequestTypeDef,
    DescribeKeyValueStoreResponseTypeDef,
    GetKeyRequestTypeDef,
    GetKeyResponseTypeDef,
    ListKeysRequestTypeDef,
    ListKeysResponseTypeDef,
    PutKeyRequestTypeDef,
    PutKeyResponseTypeDef,
    UpdateKeysRequestTypeDef,
    UpdateKeysResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("CloudFrontKeyValueStoreClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class CloudFrontKeyValueStoreClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore.html#CloudFrontKeyValueStore.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront_keyvaluestore/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudFrontKeyValueStoreClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore.html#CloudFrontKeyValueStore.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront_keyvaluestore/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront_keyvaluestore/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront_keyvaluestore/client/#generate_presigned_url)
        """

    async def delete_key(
        self, **kwargs: Unpack[DeleteKeyRequestTypeDef]
    ) -> DeleteKeyResponseTypeDef:
        """
        Deletes the key value pair specified by the key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore/client/delete_key.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront_keyvaluestore/client/#delete_key)
        """

    async def describe_key_value_store(
        self, **kwargs: Unpack[DescribeKeyValueStoreRequestTypeDef]
    ) -> DescribeKeyValueStoreResponseTypeDef:
        """
        Returns metadata information about Key Value Store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore/client/describe_key_value_store.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront_keyvaluestore/client/#describe_key_value_store)
        """

    async def get_key(self, **kwargs: Unpack[GetKeyRequestTypeDef]) -> GetKeyResponseTypeDef:
        """
        Returns a key value pair.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore/client/get_key.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront_keyvaluestore/client/#get_key)
        """

    async def list_keys(self, **kwargs: Unpack[ListKeysRequestTypeDef]) -> ListKeysResponseTypeDef:
        """
        Returns a list of key value pairs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore/client/list_keys.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront_keyvaluestore/client/#list_keys)
        """

    async def put_key(self, **kwargs: Unpack[PutKeyRequestTypeDef]) -> PutKeyResponseTypeDef:
        """
        Creates a new key value pair or replaces the value of an existing key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore/client/put_key.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront_keyvaluestore/client/#put_key)
        """

    async def update_keys(
        self, **kwargs: Unpack[UpdateKeysRequestTypeDef]
    ) -> UpdateKeysResponseTypeDef:
        """
        Puts or Deletes multiple key value pairs in a single, all-or-nothing operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore/client/update_keys.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront_keyvaluestore/client/#update_keys)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_keys"]
    ) -> ListKeysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront_keyvaluestore/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore.html#CloudFrontKeyValueStore.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront_keyvaluestore/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore.html#CloudFrontKeyValueStore.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront_keyvaluestore/client/)
        """
