"""
Type annotations for opensearchmemory service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_opensearchmemory.client import OpenSearchMemoryClient

    session = Session()
    client: OpenSearchMemoryClient = session.client("opensearchmemory")
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
    ListEventsPaginator,
    ListMemoriesPaginator,
    ListSpacesPaginator,
    SearchEventsPaginator,
    SearchMemoriesPaginator,
)
from .type_defs import (
    BatchGetEventInputTypeDef,
    BatchGetEventOutputTypeDef,
    CreateEventInputTypeDef,
    CreateEventOutputTypeDef,
    CreateMemoryInputTypeDef,
    CreateMemoryOutputTypeDef,
    CreateSpaceRequestTypeDef,
    CreateSpaceResponseTypeDef,
    DeleteEventInputTypeDef,
    DeleteEventOutputTypeDef,
    DeleteMemoryInputTypeDef,
    DeleteMemoryOutputTypeDef,
    DeleteSpaceRequestTypeDef,
    DeleteSpaceResponseTypeDef,
    GetEventInputTypeDef,
    GetEventOutputTypeDef,
    GetMemoryInputTypeDef,
    GetMemoryOutputTypeDef,
    GetSpaceRequestTypeDef,
    GetSpaceResponseTypeDef,
    ListEventsInputTypeDef,
    ListEventsOutputTypeDef,
    ListMemoriesInputTypeDef,
    ListMemoriesOutputTypeDef,
    ListSpacesRequestTypeDef,
    ListSpacesResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    SearchEventsInputTypeDef,
    SearchEventsOutputTypeDef,
    SearchMemoriesInputTypeDef,
    SearchMemoriesOutputTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateMemoryInputTypeDef,
    UpdateMemoryOutputTypeDef,
    UpdateSpaceRequestTypeDef,
    UpdateSpaceResponseTypeDef,
)
from .waiter import SpaceActiveWaiter, SpaceDeletedWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("OpenSearchMemoryClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class OpenSearchMemoryClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory.html#OpenSearchMemory.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        OpenSearchMemoryClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory.html#OpenSearchMemory.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#generate_presigned_url)
        """

    def batch_get_event(
        self, **kwargs: Unpack[BatchGetEventInputTypeDef]
    ) -> BatchGetEventOutputTypeDef:
        """
        Gets up to 10 events by ID, each as <code>GetEvent</code> returns it, including
        its payload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/batch_get_event.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#batch_get_event)
        """

    def create_event(self, **kwargs: Unpack[CreateEventInputTypeDef]) -> CreateEventOutputTypeDef:
        """
        Submits an event (conversation turns, structured data, or a PDF document stored
        in Amazon S3) to a session in a space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/create_event.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#create_event)
        """

    def create_memory(
        self, **kwargs: Unpack[CreateMemoryInputTypeDef]
    ) -> CreateMemoryOutputTypeDef:
        """
        Writes a memory that you have already formed, without extracting it from events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/create_memory.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#create_memory)
        """

    def create_space(
        self, **kwargs: Unpack[CreateSpaceRequestTypeDef]
    ) -> CreateSpaceResponseTypeDef:
        """
        Creates a space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/create_space.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#create_space)
        """

    def delete_event(self, **kwargs: Unpack[DeleteEventInputTypeDef]) -> DeleteEventOutputTypeDef:
        """
        Deletes an event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/delete_event.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#delete_event)
        """

    def delete_memory(
        self, **kwargs: Unpack[DeleteMemoryInputTypeDef]
    ) -> DeleteMemoryOutputTypeDef:
        """
        Deletes a memory, including its content and embedding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/delete_memory.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#delete_memory)
        """

    def delete_space(
        self, **kwargs: Unpack[DeleteSpaceRequestTypeDef]
    ) -> DeleteSpaceResponseTypeDef:
        """
        Deletes a space and its memories.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/delete_space.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#delete_space)
        """

    def get_event(self, **kwargs: Unpack[GetEventInputTypeDef]) -> GetEventOutputTypeDef:
        """
        Gets an event by ID, including its payload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/get_event.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#get_event)
        """

    def get_memory(self, **kwargs: Unpack[GetMemoryInputTypeDef]) -> GetMemoryOutputTypeDef:
        """
        Gets a memory by ID, as returned by <code>SearchMemories</code> or
        <code>ListMemories</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/get_memory.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#get_memory)
        """

    def get_space(self, **kwargs: Unpack[GetSpaceRequestTypeDef]) -> GetSpaceResponseTypeDef:
        """
        Returns a space's configuration and status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/get_space.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#get_space)
        """

    def list_events(self, **kwargs: Unpack[ListEventsInputTypeDef]) -> ListEventsOutputTypeDef:
        """
        Lists the events in a session, sorted by time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/list_events.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#list_events)
        """

    def list_memories(
        self, **kwargs: Unpack[ListMemoriesInputTypeDef]
    ) -> ListMemoriesOutputTypeDef:
        """
        Lists a space's memories without a query, for example the most recent memories
        or the memories of one strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/list_memories.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#list_memories)
        """

    def list_spaces(self, **kwargs: Unpack[ListSpacesRequestTypeDef]) -> ListSpacesResponseTypeDef:
        """
        Lists the spaces in your account in the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/list_spaces.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#list_spaces)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for the specified space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#list_tags_for_resource)
        """

    def search_events(
        self, **kwargs: Unpack[SearchEventsInputTypeDef]
    ) -> SearchEventsOutputTypeDef:
        """
        Searches a space's events by relevance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/search_events.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#search_events)
        """

    def search_memories(
        self, **kwargs: Unpack[SearchMemoriesInputTypeDef]
    ) -> SearchMemoriesOutputTypeDef:
        """
        Searches a space's memories by relevance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/search_memories.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#search_memories)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Adds the specified tags to the specified space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Removes the specified tags from the specified space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#untag_resource)
        """

    def update_memory(
        self, **kwargs: Unpack[UpdateMemoryInputTypeDef]
    ) -> UpdateMemoryOutputTypeDef:
        """
        Updates a memory in place.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/update_memory.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#update_memory)
        """

    def update_space(
        self, **kwargs: Unpack[UpdateSpaceRequestTypeDef]
    ) -> UpdateSpaceResponseTypeDef:
        """
        Updates a space's memory strategies, retention settings, or extraction model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/update_space.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#update_space)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_events"]
    ) -> ListEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_memories"]
    ) -> ListMemoriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_spaces"]
    ) -> ListSpacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_events"]
    ) -> SearchEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_memories"]
    ) -> SearchMemoriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["space_active"]
    ) -> SpaceActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["space_deleted"]
    ) -> SpaceDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/client/#get_waiter)
        """
