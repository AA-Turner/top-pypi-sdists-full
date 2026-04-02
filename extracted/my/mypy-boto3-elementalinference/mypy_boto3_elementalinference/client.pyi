"""
Type annotations for elementalinference service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_elementalinference.client import ElementalInferenceClient

    session = Session()
    client: ElementalInferenceClient = session.client("elementalinference")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListFeedsPaginator
from .type_defs import (
    AssociateFeedRequestTypeDef,
    AssociateFeedResponseTypeDef,
    CreateFeedRequestTypeDef,
    CreateFeedResponseTypeDef,
    DeleteFeedRequestTypeDef,
    DeleteFeedResponseTypeDef,
    DisassociateFeedRequestTypeDef,
    DisassociateFeedResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetFeedRequestTypeDef,
    GetFeedResponseTypeDef,
    ListFeedsRequestTypeDef,
    ListFeedsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateFeedRequestTypeDef,
    UpdateFeedResponseTypeDef,
)
from .waiter import FeedDeletedWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

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

class ElementalInferenceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference.html#ElementalInference.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ElementalInferenceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference.html#ElementalInference.Client)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/can_paginate.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/generate_presigned_url.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/client/#generate_presigned_url)
        """

    def associate_feed(
        self, **kwargs: Unpack[AssociateFeedRequestTypeDef]
    ) -> AssociateFeedResponseTypeDef:
        """
        Associates a resource with the feed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/associate_feed.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/client/#associate_feed)
        """

    def create_feed(self, **kwargs: Unpack[CreateFeedRequestTypeDef]) -> CreateFeedResponseTypeDef:
        """
        Creates a feed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/create_feed.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/client/#create_feed)
        """

    def delete_feed(self, **kwargs: Unpack[DeleteFeedRequestTypeDef]) -> DeleteFeedResponseTypeDef:
        """
        Deletes the specified feed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/delete_feed.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/client/#delete_feed)
        """

    def disassociate_feed(
        self, **kwargs: Unpack[DisassociateFeedRequestTypeDef]
    ) -> DisassociateFeedResponseTypeDef:
        """
        Releases the resource (for example, an MediaLive channel) that is associated
        with this feed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/disassociate_feed.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/client/#disassociate_feed)
        """

    def get_feed(self, **kwargs: Unpack[GetFeedRequestTypeDef]) -> GetFeedResponseTypeDef:
        """
        Retrieves information about the specified feed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/get_feed.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/client/#get_feed)
        """

    def list_feeds(self, **kwargs: Unpack[ListFeedsRequestTypeDef]) -> ListFeedsResponseTypeDef:
        """
        Displays a list of feeds that belong to this AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/list_feeds.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/client/#list_feeds)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List all tags that are on an Elemental Inference resource in the current region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/list_tags_for_resource.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/client/#list_tags_for_resource)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates the specified tags to the resource identified by the specified
        resourceArn in the current region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/tag_resource.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes specified tags from the specified resource in the current region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/untag_resource.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/client/#untag_resource)
        """

    def update_feed(self, **kwargs: Unpack[UpdateFeedRequestTypeDef]) -> UpdateFeedResponseTypeDef:
        """
        Updates the name and/or outputs in a feed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/update_feed.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/client/#update_feed)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_feeds"]
    ) -> ListFeedsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/client/#get_paginator)
        """

    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["feed_deleted"]
    ) -> FeedDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/get_waiter.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/client/#get_waiter)
        """
