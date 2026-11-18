"""
Type annotations for elementalinference service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_elementalinference.client import ElementalInferenceClient

    session = Session()
    client: ElementalInferenceClient = session.client("elementalinference")
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
    ListDictionariesPaginator,
    ListFeedsPaginator,
    ListFunctionsPaginator,
    ListQuestionSetsPaginator,
    ListQuestionSetVersionsPaginator,
    ListScheduleActionsPaginator,
    SearchFixturesPaginator,
)
from .type_defs import (
    AssociateFeedRequestTypeDef,
    AssociateFeedResponseTypeDef,
    CreateDictionaryRequestTypeDef,
    CreateDictionaryResponseTypeDef,
    CreateFeedRequestTypeDef,
    CreateFeedResponseTypeDef,
    CreateFunctionRequestTypeDef,
    CreateFunctionResponseTypeDef,
    CreateQuestionSetRequestTypeDef,
    CreateQuestionSetResponseTypeDef,
    CreateQuestionSetVersionRequestTypeDef,
    CreateQuestionSetVersionResponseTypeDef,
    CreateScheduleActionRequestTypeDef,
    CreateScheduleActionResponseTypeDef,
    DeleteDictionaryRequestTypeDef,
    DeleteDictionaryResponseTypeDef,
    DeleteFeedPolicyRequestTypeDef,
    DeleteFeedRequestTypeDef,
    DeleteFeedResponseTypeDef,
    DeleteFunctionRequestTypeDef,
    DeleteFunctionResponseTypeDef,
    DeleteQuestionSetRequestTypeDef,
    DeleteQuestionSetResponseTypeDef,
    DeleteQuestionSetVersionRequestTypeDef,
    DeleteScheduleActionRequestTypeDef,
    DeleteScheduleActionResponseTypeDef,
    DisassociateFeedRequestTypeDef,
    DisassociateFeedResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ExportDictionaryEntriesRequestTypeDef,
    ExportDictionaryEntriesResponseTypeDef,
    GetDictionaryRequestTypeDef,
    GetDictionaryResponseTypeDef,
    GetFeedPolicyRequestTypeDef,
    GetFeedPolicyResponseTypeDef,
    GetFeedRequestTypeDef,
    GetFeedResponseTypeDef,
    GetFixtureRequestTypeDef,
    GetFixtureResponseTypeDef,
    GetFunctionRequestTypeDef,
    GetFunctionResponseTypeDef,
    GetQuestionSetRequestTypeDef,
    GetQuestionSetResponseTypeDef,
    ListDictionariesRequestTypeDef,
    ListDictionariesResponseTypeDef,
    ListFeedsRequestTypeDef,
    ListFeedsResponseTypeDef,
    ListFunctionsRequestTypeDef,
    ListFunctionsResponseTypeDef,
    ListQuestionSetsRequestTypeDef,
    ListQuestionSetsResponseTypeDef,
    ListQuestionSetVersionsRequestTypeDef,
    ListQuestionSetVersionsResponseTypeDef,
    ListScheduleActionsRequestTypeDef,
    ListScheduleActionsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutFeedPolicyRequestTypeDef,
    SearchFixturesRequestTypeDef,
    SearchFixturesResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateDictionaryRequestTypeDef,
    UpdateDictionaryResponseTypeDef,
    UpdateFeedRequestTypeDef,
    UpdateFeedResponseTypeDef,
    UpdateFunctionRequestTypeDef,
    UpdateFunctionResponseTypeDef,
    UpdateQuestionSetRequestTypeDef,
    UpdateQuestionSetResponseTypeDef,
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
    GatewayTimedOutException: type[BotocoreClientError]
    InternalServerErrorException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ServiceUnavailableException: type[BotocoreClientError]
    TooManyRequestException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class ElementalInferenceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference.html#ElementalInference.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ElementalInferenceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference.html#ElementalInference.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#can_paginate)
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
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#generate_presigned_url)
        """

    def associate_feed(
        self, **kwargs: Unpack[AssociateFeedRequestTypeDef]
    ) -> AssociateFeedResponseTypeDef:
        """
        Associates a resource with the feed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/associate_feed.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#associate_feed)
        """

    def create_dictionary(
        self, **kwargs: Unpack[CreateDictionaryRequestTypeDef]
    ) -> CreateDictionaryResponseTypeDef:
        """
        Creates a custom dictionary for improving transcription accuracy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/create_dictionary.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#create_dictionary)
        """

    def create_feed(self, **kwargs: Unpack[CreateFeedRequestTypeDef]) -> CreateFeedResponseTypeDef:
        """
        Creates a feed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/create_feed.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#create_feed)
        """

    def create_function(
        self, **kwargs: Unpack[CreateFunctionRequestTypeDef]
    ) -> CreateFunctionResponseTypeDef:
        """
        Creates a function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/create_function.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#create_function)
        """

    def create_question_set(
        self, **kwargs: Unpack[CreateQuestionSetRequestTypeDef]
    ) -> CreateQuestionSetResponseTypeDef:
        """
        Creates a question set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/create_question_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#create_question_set)
        """

    def create_question_set_version(
        self, **kwargs: Unpack[CreateQuestionSetVersionRequestTypeDef]
    ) -> CreateQuestionSetVersionResponseTypeDef:
        """
        Publishes the DRAFT version of the specified question set as a new version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/create_question_set_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#create_question_set_version)
        """

    def create_schedule_action(
        self, **kwargs: Unpack[CreateScheduleActionRequestTypeDef]
    ) -> CreateScheduleActionResponseTypeDef:
        """
        Creates a schedule action on a feed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/create_schedule_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#create_schedule_action)
        """

    def delete_dictionary(
        self, **kwargs: Unpack[DeleteDictionaryRequestTypeDef]
    ) -> DeleteDictionaryResponseTypeDef:
        """
        Deletes the specified dictionary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/delete_dictionary.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#delete_dictionary)
        """

    def delete_feed(self, **kwargs: Unpack[DeleteFeedRequestTypeDef]) -> DeleteFeedResponseTypeDef:
        """
        Deletes the specified feed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/delete_feed.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#delete_feed)
        """

    def delete_feed_policy(
        self, **kwargs: Unpack[DeleteFeedPolicyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the resource-based policy attached to the specified feed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/delete_feed_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#delete_feed_policy)
        """

    def delete_function(
        self, **kwargs: Unpack[DeleteFunctionRequestTypeDef]
    ) -> DeleteFunctionResponseTypeDef:
        """
        Deletes a function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/delete_function.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#delete_function)
        """

    def delete_question_set(
        self, **kwargs: Unpack[DeleteQuestionSetRequestTypeDef]
    ) -> DeleteQuestionSetResponseTypeDef:
        """
        Deletes the specified question set, including its DRAFT version and all its
        published versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/delete_question_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#delete_question_set)
        """

    def delete_question_set_version(
        self, **kwargs: Unpack[DeleteQuestionSetVersionRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes a published version of the specified question set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/delete_question_set_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#delete_question_set_version)
        """

    def delete_schedule_action(
        self, **kwargs: Unpack[DeleteScheduleActionRequestTypeDef]
    ) -> DeleteScheduleActionResponseTypeDef:
        """
        Deletes a schedule action from a feed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/delete_schedule_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#delete_schedule_action)
        """

    def disassociate_feed(
        self, **kwargs: Unpack[DisassociateFeedRequestTypeDef]
    ) -> DisassociateFeedResponseTypeDef:
        """
        Releases the resource (the source media) that is associated with this feed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/disassociate_feed.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#disassociate_feed)
        """

    def export_dictionary_entries(
        self, **kwargs: Unpack[ExportDictionaryEntriesRequestTypeDef]
    ) -> ExportDictionaryEntriesResponseTypeDef:
        """
        Exports the entries from the specified dictionary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/export_dictionary_entries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#export_dictionary_entries)
        """

    def get_dictionary(
        self, **kwargs: Unpack[GetDictionaryRequestTypeDef]
    ) -> GetDictionaryResponseTypeDef:
        """
        Retrieves information about the specified dictionary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/get_dictionary.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#get_dictionary)
        """

    def get_feed(self, **kwargs: Unpack[GetFeedRequestTypeDef]) -> GetFeedResponseTypeDef:
        """
        Retrieves information about the specified feed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/get_feed.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#get_feed)
        """

    def get_feed_policy(
        self, **kwargs: Unpack[GetFeedPolicyRequestTypeDef]
    ) -> GetFeedPolicyResponseTypeDef:
        """
        Retrieves the resource-based policy attached to the specified feed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/get_feed_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#get_feed_policy)
        """

    def get_fixture(self, **kwargs: Unpack[GetFixtureRequestTypeDef]) -> GetFixtureResponseTypeDef:
        """
        Retrieves information about the specified fixture (a sports event, such as a
        specific basketball game).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/get_fixture.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#get_fixture)
        """

    def get_function(
        self, **kwargs: Unpack[GetFunctionRequestTypeDef]
    ) -> GetFunctionResponseTypeDef:
        """
        Retrieves the details of a function, including its expressions, the media
        context that Elemental Inference derived from the request expression, and the
        feeds that currently reference it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/get_function.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#get_function)
        """

    def get_question_set(
        self, **kwargs: Unpack[GetQuestionSetRequestTypeDef]
    ) -> GetQuestionSetResponseTypeDef:
        """
        Retrieves information about the specified question set at one version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/get_question_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#get_question_set)
        """

    def list_dictionaries(
        self, **kwargs: Unpack[ListDictionariesRequestTypeDef]
    ) -> ListDictionariesResponseTypeDef:
        """
        Lists the dictionaries in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/list_dictionaries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#list_dictionaries)
        """

    def list_feeds(self, **kwargs: Unpack[ListFeedsRequestTypeDef]) -> ListFeedsResponseTypeDef:
        """
        Displays a list of feeds that belong to this AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/list_feeds.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#list_feeds)
        """

    def list_functions(
        self, **kwargs: Unpack[ListFunctionsRequestTypeDef]
    ) -> ListFunctionsResponseTypeDef:
        """
        Lists the functions in this account, in this Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/list_functions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#list_functions)
        """

    def list_question_set_versions(
        self, **kwargs: Unpack[ListQuestionSetVersionsRequestTypeDef]
    ) -> ListQuestionSetVersionsResponseTypeDef:
        """
        Lists the versions of the specified question set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/list_question_set_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#list_question_set_versions)
        """

    def list_question_sets(
        self, **kwargs: Unpack[ListQuestionSetsRequestTypeDef]
    ) -> ListQuestionSetsResponseTypeDef:
        """
        Lists the question sets in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/list_question_sets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#list_question_sets)
        """

    def list_schedule_actions(
        self, **kwargs: Unpack[ListScheduleActionsRequestTypeDef]
    ) -> ListScheduleActionsResponseTypeDef:
        """
        Displays a list of the schedule actions on a feed, including the status of each
        action and, for a failed action, information about why it failed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/list_schedule_actions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#list_schedule_actions)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List all tags that are on an Elemental Inference resource in the current region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#list_tags_for_resource)
        """

    def put_feed_policy(self, **kwargs: Unpack[PutFeedPolicyRequestTypeDef]) -> dict[str, Any]:
        """
        Attaches or replaces a resource-based policy on the specified feed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/put_feed_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#put_feed_policy)
        """

    def search_fixtures(
        self, **kwargs: Unpack[SearchFixturesRequestTypeDef]
    ) -> SearchFixturesResponseTypeDef:
        """
        Searches for the fixtures (sports events, such as a specific basketball game)
        that are available for a sport in a date window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/search_fixtures.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#search_fixtures)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates the specified tags to the resource identified by the specified
        resourceArn in the current region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes specified tags from the specified resource in the current region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#untag_resource)
        """

    def update_dictionary(
        self, **kwargs: Unpack[UpdateDictionaryRequestTypeDef]
    ) -> UpdateDictionaryResponseTypeDef:
        """
        Updates the specified dictionary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/update_dictionary.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#update_dictionary)
        """

    def update_feed(self, **kwargs: Unpack[UpdateFeedRequestTypeDef]) -> UpdateFeedResponseTypeDef:
        """
        Updates the name and/or outputs in a feed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/update_feed.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#update_feed)
        """

    def update_function(
        self, **kwargs: Unpack[UpdateFunctionRequestTypeDef]
    ) -> UpdateFunctionResponseTypeDef:
        """
        Updates a function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/update_function.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#update_function)
        """

    def update_question_set(
        self, **kwargs: Unpack[UpdateQuestionSetRequestTypeDef]
    ) -> UpdateQuestionSetResponseTypeDef:
        """
        Updates the DRAFT version of the specified question set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/update_question_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#update_question_set)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_dictionaries"]
    ) -> ListDictionariesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_feeds"]
    ) -> ListFeedsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_functions"]
    ) -> ListFunctionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_question_set_versions"]
    ) -> ListQuestionSetVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_question_sets"]
    ) -> ListQuestionSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_schedule_actions"]
    ) -> ListScheduleActionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_fixtures"]
    ) -> SearchFixturesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#get_paginator)
        """

    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["feed_deleted"]
    ) -> FeedDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/client/#get_waiter)
        """
