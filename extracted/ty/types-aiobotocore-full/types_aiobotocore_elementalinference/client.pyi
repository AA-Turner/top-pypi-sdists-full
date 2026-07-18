"""
Type annotations for elementalinference service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_elementalinference.client import ElementalInferenceClient

    session = get_session()
    async with session.create_client("elementalinference") as client:
        client: ElementalInferenceClient
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListDictionariesPaginator, ListFeedsPaginator
from .type_defs import (
    AssociateFeedRequestTypeDef,
    AssociateFeedResponseTypeDef,
    CreateDictionaryRequestTypeDef,
    CreateDictionaryResponseTypeDef,
    CreateFeedRequestTypeDef,
    CreateFeedResponseTypeDef,
    DeleteDictionaryRequestTypeDef,
    DeleteDictionaryResponseTypeDef,
    DeleteFeedRequestTypeDef,
    DeleteFeedResponseTypeDef,
    DisassociateFeedRequestTypeDef,
    DisassociateFeedResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ExportDictionaryEntriesRequestTypeDef,
    ExportDictionaryEntriesResponseTypeDef,
    GetDictionaryRequestTypeDef,
    GetDictionaryResponseTypeDef,
    GetFeedRequestTypeDef,
    GetFeedResponseTypeDef,
    ListDictionariesRequestTypeDef,
    ListDictionariesResponseTypeDef,
    ListFeedsRequestTypeDef,
    ListFeedsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateDictionaryRequestTypeDef,
    UpdateDictionaryResponseTypeDef,
    UpdateFeedRequestTypeDef,
    UpdateFeedResponseTypeDef,
)
from .waiter import FeedDeletedWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("ElementalInferenceClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerErrorException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    TooManyRequestException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class ElementalInferenceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference.html#ElementalInference.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ElementalInferenceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference.html#ElementalInference.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/#generate_presigned_url)
        """

    async def associate_feed(
        self, **kwargs: Unpack[AssociateFeedRequestTypeDef]
    ) -> AssociateFeedResponseTypeDef:
        """
        Associates a resource with the feed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/associate_feed.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/#associate_feed)
        """

    async def create_dictionary(
        self, **kwargs: Unpack[CreateDictionaryRequestTypeDef]
    ) -> CreateDictionaryResponseTypeDef:
        """
        Creates a custom dictionary for improving transcription accuracy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/create_dictionary.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/#create_dictionary)
        """

    async def create_feed(
        self, **kwargs: Unpack[CreateFeedRequestTypeDef]
    ) -> CreateFeedResponseTypeDef:
        """
        Creates a feed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/create_feed.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/#create_feed)
        """

    async def delete_dictionary(
        self, **kwargs: Unpack[DeleteDictionaryRequestTypeDef]
    ) -> DeleteDictionaryResponseTypeDef:
        """
        Deletes the specified dictionary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/delete_dictionary.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/#delete_dictionary)
        """

    async def delete_feed(
        self, **kwargs: Unpack[DeleteFeedRequestTypeDef]
    ) -> DeleteFeedResponseTypeDef:
        """
        Deletes the specified feed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/delete_feed.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/#delete_feed)
        """

    async def disassociate_feed(
        self, **kwargs: Unpack[DisassociateFeedRequestTypeDef]
    ) -> DisassociateFeedResponseTypeDef:
        """
        Releases the resource (the source media) that is associated with this feed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/disassociate_feed.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/#disassociate_feed)
        """

    async def export_dictionary_entries(
        self, **kwargs: Unpack[ExportDictionaryEntriesRequestTypeDef]
    ) -> ExportDictionaryEntriesResponseTypeDef:
        """
        Exports the entries from the specified dictionary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/export_dictionary_entries.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/#export_dictionary_entries)
        """

    async def get_dictionary(
        self, **kwargs: Unpack[GetDictionaryRequestTypeDef]
    ) -> GetDictionaryResponseTypeDef:
        """
        Retrieves information about the specified dictionary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/get_dictionary.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/#get_dictionary)
        """

    async def get_feed(self, **kwargs: Unpack[GetFeedRequestTypeDef]) -> GetFeedResponseTypeDef:
        """
        Retrieves information about the specified feed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/get_feed.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/#get_feed)
        """

    async def list_dictionaries(
        self, **kwargs: Unpack[ListDictionariesRequestTypeDef]
    ) -> ListDictionariesResponseTypeDef:
        """
        Lists the dictionaries in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/list_dictionaries.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/#list_dictionaries)
        """

    async def list_feeds(
        self, **kwargs: Unpack[ListFeedsRequestTypeDef]
    ) -> ListFeedsResponseTypeDef:
        """
        Displays a list of feeds that belong to this AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/list_feeds.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/#list_feeds)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List all tags that are on an Elemental Inference resource in the current region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/#list_tags_for_resource)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates the specified tags to the resource identified by the specified
        resourceArn in the current region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes specified tags from the specified resource in the current region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/#untag_resource)
        """

    async def update_dictionary(
        self, **kwargs: Unpack[UpdateDictionaryRequestTypeDef]
    ) -> UpdateDictionaryResponseTypeDef:
        """
        Updates the specified dictionary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/update_dictionary.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/#update_dictionary)
        """

    async def update_feed(
        self, **kwargs: Unpack[UpdateFeedRequestTypeDef]
    ) -> UpdateFeedResponseTypeDef:
        """
        Updates the name and/or outputs in a feed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/update_feed.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/#update_feed)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_dictionaries"]
    ) -> ListDictionariesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_feeds"]
    ) -> ListFeedsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/#get_paginator)
        """

    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["feed_deleted"]
    ) -> FeedDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/#get_waiter)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference.html#ElementalInference.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference.html#ElementalInference.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/client/)
        """
