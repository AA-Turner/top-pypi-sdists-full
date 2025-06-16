"""
Type annotations for lexv2-models service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_lexv2_models.client import LexModelsV2Client

    session = get_session()
    async with session.create_client("lexv2-models") as client:
        client: LexModelsV2Client
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    BatchCreateCustomVocabularyItemRequestTypeDef,
    BatchCreateCustomVocabularyItemResponseTypeDef,
    BatchDeleteCustomVocabularyItemRequestTypeDef,
    BatchDeleteCustomVocabularyItemResponseTypeDef,
    BatchUpdateCustomVocabularyItemRequestTypeDef,
    BatchUpdateCustomVocabularyItemResponseTypeDef,
    BuildBotLocaleRequestTypeDef,
    BuildBotLocaleResponseTypeDef,
    CreateBotAliasRequestTypeDef,
    CreateBotAliasResponseTypeDef,
    CreateBotLocaleRequestTypeDef,
    CreateBotLocaleResponseTypeDef,
    CreateBotReplicaRequestTypeDef,
    CreateBotReplicaResponseTypeDef,
    CreateBotRequestTypeDef,
    CreateBotResponseTypeDef,
    CreateBotVersionRequestTypeDef,
    CreateBotVersionResponseTypeDef,
    CreateExportRequestTypeDef,
    CreateExportResponseTypeDef,
    CreateIntentRequestTypeDef,
    CreateIntentResponseTypeDef,
    CreateResourcePolicyRequestTypeDef,
    CreateResourcePolicyResponseTypeDef,
    CreateResourcePolicyStatementRequestTypeDef,
    CreateResourcePolicyStatementResponseTypeDef,
    CreateSlotRequestTypeDef,
    CreateSlotResponseTypeDef,
    CreateSlotTypeRequestTypeDef,
    CreateSlotTypeResponseTypeDef,
    CreateTestSetDiscrepancyReportRequestTypeDef,
    CreateTestSetDiscrepancyReportResponseTypeDef,
    CreateUploadUrlResponseTypeDef,
    DeleteBotAliasRequestTypeDef,
    DeleteBotAliasResponseTypeDef,
    DeleteBotLocaleRequestTypeDef,
    DeleteBotLocaleResponseTypeDef,
    DeleteBotReplicaRequestTypeDef,
    DeleteBotReplicaResponseTypeDef,
    DeleteBotRequestTypeDef,
    DeleteBotResponseTypeDef,
    DeleteBotVersionRequestTypeDef,
    DeleteBotVersionResponseTypeDef,
    DeleteCustomVocabularyRequestTypeDef,
    DeleteCustomVocabularyResponseTypeDef,
    DeleteExportRequestTypeDef,
    DeleteExportResponseTypeDef,
    DeleteImportRequestTypeDef,
    DeleteImportResponseTypeDef,
    DeleteIntentRequestTypeDef,
    DeleteResourcePolicyRequestTypeDef,
    DeleteResourcePolicyResponseTypeDef,
    DeleteResourcePolicyStatementRequestTypeDef,
    DeleteResourcePolicyStatementResponseTypeDef,
    DeleteSlotRequestTypeDef,
    DeleteSlotTypeRequestTypeDef,
    DeleteTestSetRequestTypeDef,
    DeleteUtterancesRequestTypeDef,
    DescribeBotAliasRequestTypeDef,
    DescribeBotAliasResponseTypeDef,
    DescribeBotLocaleRequestTypeDef,
    DescribeBotLocaleResponseTypeDef,
    DescribeBotRecommendationRequestTypeDef,
    DescribeBotRecommendationResponseTypeDef,
    DescribeBotReplicaRequestTypeDef,
    DescribeBotReplicaResponseTypeDef,
    DescribeBotRequestTypeDef,
    DescribeBotResourceGenerationRequestTypeDef,
    DescribeBotResourceGenerationResponseTypeDef,
    DescribeBotResponseTypeDef,
    DescribeBotVersionRequestTypeDef,
    DescribeBotVersionResponseTypeDef,
    DescribeCustomVocabularyMetadataRequestTypeDef,
    DescribeCustomVocabularyMetadataResponseTypeDef,
    DescribeExportRequestTypeDef,
    DescribeExportResponseTypeDef,
    DescribeImportRequestTypeDef,
    DescribeImportResponseTypeDef,
    DescribeIntentRequestTypeDef,
    DescribeIntentResponseTypeDef,
    DescribeResourcePolicyRequestTypeDef,
    DescribeResourcePolicyResponseTypeDef,
    DescribeSlotRequestTypeDef,
    DescribeSlotResponseTypeDef,
    DescribeSlotTypeRequestTypeDef,
    DescribeSlotTypeResponseTypeDef,
    DescribeTestExecutionRequestTypeDef,
    DescribeTestExecutionResponseTypeDef,
    DescribeTestSetDiscrepancyReportRequestTypeDef,
    DescribeTestSetDiscrepancyReportResponseTypeDef,
    DescribeTestSetGenerationRequestTypeDef,
    DescribeTestSetGenerationResponseTypeDef,
    DescribeTestSetRequestTypeDef,
    DescribeTestSetResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GenerateBotElementRequestTypeDef,
    GenerateBotElementResponseTypeDef,
    GetTestExecutionArtifactsUrlRequestTypeDef,
    GetTestExecutionArtifactsUrlResponseTypeDef,
    ListAggregatedUtterancesRequestTypeDef,
    ListAggregatedUtterancesResponseTypeDef,
    ListBotAliasesRequestTypeDef,
    ListBotAliasesResponseTypeDef,
    ListBotAliasReplicasRequestTypeDef,
    ListBotAliasReplicasResponseTypeDef,
    ListBotLocalesRequestTypeDef,
    ListBotLocalesResponseTypeDef,
    ListBotRecommendationsRequestTypeDef,
    ListBotRecommendationsResponseTypeDef,
    ListBotReplicasRequestTypeDef,
    ListBotReplicasResponseTypeDef,
    ListBotResourceGenerationsRequestTypeDef,
    ListBotResourceGenerationsResponseTypeDef,
    ListBotsRequestTypeDef,
    ListBotsResponseTypeDef,
    ListBotVersionReplicasRequestTypeDef,
    ListBotVersionReplicasResponseTypeDef,
    ListBotVersionsRequestTypeDef,
    ListBotVersionsResponseTypeDef,
    ListBuiltInIntentsRequestTypeDef,
    ListBuiltInIntentsResponseTypeDef,
    ListBuiltInSlotTypesRequestTypeDef,
    ListBuiltInSlotTypesResponseTypeDef,
    ListCustomVocabularyItemsRequestTypeDef,
    ListCustomVocabularyItemsResponseTypeDef,
    ListExportsRequestTypeDef,
    ListExportsResponseTypeDef,
    ListImportsRequestTypeDef,
    ListImportsResponseTypeDef,
    ListIntentMetricsRequestTypeDef,
    ListIntentMetricsResponseTypeDef,
    ListIntentPathsRequestTypeDef,
    ListIntentPathsResponseTypeDef,
    ListIntentsRequestTypeDef,
    ListIntentsResponseTypeDef,
    ListIntentStageMetricsRequestTypeDef,
    ListIntentStageMetricsResponseTypeDef,
    ListRecommendedIntentsRequestTypeDef,
    ListRecommendedIntentsResponseTypeDef,
    ListSessionAnalyticsDataRequestTypeDef,
    ListSessionAnalyticsDataResponseTypeDef,
    ListSessionMetricsRequestTypeDef,
    ListSessionMetricsResponseTypeDef,
    ListSlotsRequestTypeDef,
    ListSlotsResponseTypeDef,
    ListSlotTypesRequestTypeDef,
    ListSlotTypesResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTestExecutionResultItemsRequestTypeDef,
    ListTestExecutionResultItemsResponseTypeDef,
    ListTestExecutionsRequestTypeDef,
    ListTestExecutionsResponseTypeDef,
    ListTestSetRecordsRequestTypeDef,
    ListTestSetRecordsResponseTypeDef,
    ListTestSetsRequestTypeDef,
    ListTestSetsResponseTypeDef,
    ListUtteranceAnalyticsDataRequestTypeDef,
    ListUtteranceAnalyticsDataResponseTypeDef,
    ListUtteranceMetricsRequestTypeDef,
    ListUtteranceMetricsResponseTypeDef,
    SearchAssociatedTranscriptsRequestTypeDef,
    SearchAssociatedTranscriptsResponseTypeDef,
    StartBotRecommendationRequestTypeDef,
    StartBotRecommendationResponseTypeDef,
    StartBotResourceGenerationRequestTypeDef,
    StartBotResourceGenerationResponseTypeDef,
    StartImportRequestTypeDef,
    StartImportResponseTypeDef,
    StartTestExecutionRequestTypeDef,
    StartTestExecutionResponseTypeDef,
    StartTestSetGenerationRequestTypeDef,
    StartTestSetGenerationResponseTypeDef,
    StopBotRecommendationRequestTypeDef,
    StopBotRecommendationResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateBotAliasRequestTypeDef,
    UpdateBotAliasResponseTypeDef,
    UpdateBotLocaleRequestTypeDef,
    UpdateBotLocaleResponseTypeDef,
    UpdateBotRecommendationRequestTypeDef,
    UpdateBotRecommendationResponseTypeDef,
    UpdateBotRequestTypeDef,
    UpdateBotResponseTypeDef,
    UpdateExportRequestTypeDef,
    UpdateExportResponseTypeDef,
    UpdateIntentRequestTypeDef,
    UpdateIntentResponseTypeDef,
    UpdateResourcePolicyRequestTypeDef,
    UpdateResourcePolicyResponseTypeDef,
    UpdateSlotRequestTypeDef,
    UpdateSlotResponseTypeDef,
    UpdateSlotTypeRequestTypeDef,
    UpdateSlotTypeResponseTypeDef,
    UpdateTestSetRequestTypeDef,
    UpdateTestSetResponseTypeDef,
)
from .waiter import (
    BotAliasAvailableWaiter,
    BotAvailableWaiter,
    BotExportCompletedWaiter,
    BotImportCompletedWaiter,
    BotLocaleBuiltWaiter,
    BotLocaleCreatedWaiter,
    BotLocaleExpressTestingAvailableWaiter,
    BotVersionAvailableWaiter,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("LexModelsV2Client",)


class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    PreconditionFailedException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class LexModelsV2Client(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LexModelsV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#generate_presigned_url)
        """

    async def batch_create_custom_vocabulary_item(
        self, **kwargs: Unpack[BatchCreateCustomVocabularyItemRequestTypeDef]
    ) -> BatchCreateCustomVocabularyItemResponseTypeDef:
        """
        Create a batch of custom vocabulary items for a given bot locale's custom
        vocabulary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/batch_create_custom_vocabulary_item.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#batch_create_custom_vocabulary_item)
        """

    async def batch_delete_custom_vocabulary_item(
        self, **kwargs: Unpack[BatchDeleteCustomVocabularyItemRequestTypeDef]
    ) -> BatchDeleteCustomVocabularyItemResponseTypeDef:
        """
        Delete a batch of custom vocabulary items for a given bot locale's custom
        vocabulary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/batch_delete_custom_vocabulary_item.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#batch_delete_custom_vocabulary_item)
        """

    async def batch_update_custom_vocabulary_item(
        self, **kwargs: Unpack[BatchUpdateCustomVocabularyItemRequestTypeDef]
    ) -> BatchUpdateCustomVocabularyItemResponseTypeDef:
        """
        Update a batch of custom vocabulary items for a given bot locale's custom
        vocabulary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/batch_update_custom_vocabulary_item.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#batch_update_custom_vocabulary_item)
        """

    async def build_bot_locale(
        self, **kwargs: Unpack[BuildBotLocaleRequestTypeDef]
    ) -> BuildBotLocaleResponseTypeDef:
        """
        Builds a bot, its intents, and its slot types into a specific locale.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/build_bot_locale.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#build_bot_locale)
        """

    async def create_bot(
        self, **kwargs: Unpack[CreateBotRequestTypeDef]
    ) -> CreateBotResponseTypeDef:
        """
        Creates an Amazon Lex conversational bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/create_bot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#create_bot)
        """

    async def create_bot_alias(
        self, **kwargs: Unpack[CreateBotAliasRequestTypeDef]
    ) -> CreateBotAliasResponseTypeDef:
        """
        Creates an alias for the specified version of a bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/create_bot_alias.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#create_bot_alias)
        """

    async def create_bot_locale(
        self, **kwargs: Unpack[CreateBotLocaleRequestTypeDef]
    ) -> CreateBotLocaleResponseTypeDef:
        """
        Creates a locale in the bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/create_bot_locale.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#create_bot_locale)
        """

    async def create_bot_replica(
        self, **kwargs: Unpack[CreateBotReplicaRequestTypeDef]
    ) -> CreateBotReplicaResponseTypeDef:
        """
        Action to create a replication of the source bot in the secondary region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/create_bot_replica.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#create_bot_replica)
        """

    async def create_bot_version(
        self, **kwargs: Unpack[CreateBotVersionRequestTypeDef]
    ) -> CreateBotVersionResponseTypeDef:
        """
        Creates an immutable version of the bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/create_bot_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#create_bot_version)
        """

    async def create_export(
        self, **kwargs: Unpack[CreateExportRequestTypeDef]
    ) -> CreateExportResponseTypeDef:
        """
        Creates a zip archive containing the contents of a bot or a bot locale.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/create_export.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#create_export)
        """

    async def create_intent(
        self, **kwargs: Unpack[CreateIntentRequestTypeDef]
    ) -> CreateIntentResponseTypeDef:
        """
        Creates an intent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/create_intent.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#create_intent)
        """

    async def create_resource_policy(
        self, **kwargs: Unpack[CreateResourcePolicyRequestTypeDef]
    ) -> CreateResourcePolicyResponseTypeDef:
        """
        Creates a new resource policy with the specified policy statements.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/create_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#create_resource_policy)
        """

    async def create_resource_policy_statement(
        self, **kwargs: Unpack[CreateResourcePolicyStatementRequestTypeDef]
    ) -> CreateResourcePolicyStatementResponseTypeDef:
        """
        Adds a new resource policy statement to a bot or bot alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/create_resource_policy_statement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#create_resource_policy_statement)
        """

    async def create_slot(
        self, **kwargs: Unpack[CreateSlotRequestTypeDef]
    ) -> CreateSlotResponseTypeDef:
        """
        Creates a slot in an intent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/create_slot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#create_slot)
        """

    async def create_slot_type(
        self, **kwargs: Unpack[CreateSlotTypeRequestTypeDef]
    ) -> CreateSlotTypeResponseTypeDef:
        """
        Creates a custom slot type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/create_slot_type.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#create_slot_type)
        """

    async def create_test_set_discrepancy_report(
        self, **kwargs: Unpack[CreateTestSetDiscrepancyReportRequestTypeDef]
    ) -> CreateTestSetDiscrepancyReportResponseTypeDef:
        """
        Create a report that describes the differences between the bot and the test set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/create_test_set_discrepancy_report.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#create_test_set_discrepancy_report)
        """

    async def create_upload_url(self) -> CreateUploadUrlResponseTypeDef:
        """
        Gets a pre-signed S3 write URL that you use to upload the zip archive when
        importing a bot or a bot locale.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/create_upload_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#create_upload_url)
        """

    async def delete_bot(
        self, **kwargs: Unpack[DeleteBotRequestTypeDef]
    ) -> DeleteBotResponseTypeDef:
        """
        Deletes all versions of a bot, including the <code>Draft</code> version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/delete_bot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#delete_bot)
        """

    async def delete_bot_alias(
        self, **kwargs: Unpack[DeleteBotAliasRequestTypeDef]
    ) -> DeleteBotAliasResponseTypeDef:
        """
        Deletes the specified bot alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/delete_bot_alias.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#delete_bot_alias)
        """

    async def delete_bot_locale(
        self, **kwargs: Unpack[DeleteBotLocaleRequestTypeDef]
    ) -> DeleteBotLocaleResponseTypeDef:
        """
        Removes a locale from a bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/delete_bot_locale.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#delete_bot_locale)
        """

    async def delete_bot_replica(
        self, **kwargs: Unpack[DeleteBotReplicaRequestTypeDef]
    ) -> DeleteBotReplicaResponseTypeDef:
        """
        The action to delete the replicated bot in the secondary region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/delete_bot_replica.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#delete_bot_replica)
        """

    async def delete_bot_version(
        self, **kwargs: Unpack[DeleteBotVersionRequestTypeDef]
    ) -> DeleteBotVersionResponseTypeDef:
        """
        Deletes a specific version of a bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/delete_bot_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#delete_bot_version)
        """

    async def delete_custom_vocabulary(
        self, **kwargs: Unpack[DeleteCustomVocabularyRequestTypeDef]
    ) -> DeleteCustomVocabularyResponseTypeDef:
        """
        Removes a custom vocabulary from the specified locale in the specified bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/delete_custom_vocabulary.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#delete_custom_vocabulary)
        """

    async def delete_export(
        self, **kwargs: Unpack[DeleteExportRequestTypeDef]
    ) -> DeleteExportResponseTypeDef:
        """
        Removes a previous export and the associated files stored in an S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/delete_export.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#delete_export)
        """

    async def delete_import(
        self, **kwargs: Unpack[DeleteImportRequestTypeDef]
    ) -> DeleteImportResponseTypeDef:
        """
        Removes a previous import and the associated file stored in an S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/delete_import.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#delete_import)
        """

    async def delete_intent(
        self, **kwargs: Unpack[DeleteIntentRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified intent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/delete_intent.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#delete_intent)
        """

    async def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyRequestTypeDef]
    ) -> DeleteResourcePolicyResponseTypeDef:
        """
        Removes an existing policy from a bot or bot alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/delete_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#delete_resource_policy)
        """

    async def delete_resource_policy_statement(
        self, **kwargs: Unpack[DeleteResourcePolicyStatementRequestTypeDef]
    ) -> DeleteResourcePolicyStatementResponseTypeDef:
        """
        Deletes a policy statement from a resource policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/delete_resource_policy_statement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#delete_resource_policy_statement)
        """

    async def delete_slot(
        self, **kwargs: Unpack[DeleteSlotRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified slot from an intent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/delete_slot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#delete_slot)
        """

    async def delete_slot_type(
        self, **kwargs: Unpack[DeleteSlotTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a slot type from a bot locale.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/delete_slot_type.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#delete_slot_type)
        """

    async def delete_test_set(
        self, **kwargs: Unpack[DeleteTestSetRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        The action to delete the selected test set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/delete_test_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#delete_test_set)
        """

    async def delete_utterances(
        self, **kwargs: Unpack[DeleteUtterancesRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes stored utterances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/delete_utterances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#delete_utterances)
        """

    async def describe_bot(
        self, **kwargs: Unpack[DescribeBotRequestTypeDef]
    ) -> DescribeBotResponseTypeDef:
        """
        Provides metadata information about a bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/describe_bot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#describe_bot)
        """

    async def describe_bot_alias(
        self, **kwargs: Unpack[DescribeBotAliasRequestTypeDef]
    ) -> DescribeBotAliasResponseTypeDef:
        """
        Get information about a specific bot alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/describe_bot_alias.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#describe_bot_alias)
        """

    async def describe_bot_locale(
        self, **kwargs: Unpack[DescribeBotLocaleRequestTypeDef]
    ) -> DescribeBotLocaleResponseTypeDef:
        """
        Describes the settings that a bot has for a specific locale.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/describe_bot_locale.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#describe_bot_locale)
        """

    async def describe_bot_recommendation(
        self, **kwargs: Unpack[DescribeBotRecommendationRequestTypeDef]
    ) -> DescribeBotRecommendationResponseTypeDef:
        """
        Provides metadata information about a bot recommendation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/describe_bot_recommendation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#describe_bot_recommendation)
        """

    async def describe_bot_replica(
        self, **kwargs: Unpack[DescribeBotReplicaRequestTypeDef]
    ) -> DescribeBotReplicaResponseTypeDef:
        """
        Monitors the bot replication status through the UI console.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/describe_bot_replica.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#describe_bot_replica)
        """

    async def describe_bot_resource_generation(
        self, **kwargs: Unpack[DescribeBotResourceGenerationRequestTypeDef]
    ) -> DescribeBotResourceGenerationResponseTypeDef:
        """
        Returns information about a request to generate a bot through natural language
        description, made through the <code>StartBotResource</code> API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/describe_bot_resource_generation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#describe_bot_resource_generation)
        """

    async def describe_bot_version(
        self, **kwargs: Unpack[DescribeBotVersionRequestTypeDef]
    ) -> DescribeBotVersionResponseTypeDef:
        """
        Provides metadata about a version of a bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/describe_bot_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#describe_bot_version)
        """

    async def describe_custom_vocabulary_metadata(
        self, **kwargs: Unpack[DescribeCustomVocabularyMetadataRequestTypeDef]
    ) -> DescribeCustomVocabularyMetadataResponseTypeDef:
        """
        Provides metadata information about a custom vocabulary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/describe_custom_vocabulary_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#describe_custom_vocabulary_metadata)
        """

    async def describe_export(
        self, **kwargs: Unpack[DescribeExportRequestTypeDef]
    ) -> DescribeExportResponseTypeDef:
        """
        Gets information about a specific export.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/describe_export.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#describe_export)
        """

    async def describe_import(
        self, **kwargs: Unpack[DescribeImportRequestTypeDef]
    ) -> DescribeImportResponseTypeDef:
        """
        Gets information about a specific import.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/describe_import.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#describe_import)
        """

    async def describe_intent(
        self, **kwargs: Unpack[DescribeIntentRequestTypeDef]
    ) -> DescribeIntentResponseTypeDef:
        """
        Returns metadata about an intent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/describe_intent.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#describe_intent)
        """

    async def describe_resource_policy(
        self, **kwargs: Unpack[DescribeResourcePolicyRequestTypeDef]
    ) -> DescribeResourcePolicyResponseTypeDef:
        """
        Gets the resource policy and policy revision for a bot or bot alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/describe_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#describe_resource_policy)
        """

    async def describe_slot(
        self, **kwargs: Unpack[DescribeSlotRequestTypeDef]
    ) -> DescribeSlotResponseTypeDef:
        """
        Gets metadata information about a slot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/describe_slot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#describe_slot)
        """

    async def describe_slot_type(
        self, **kwargs: Unpack[DescribeSlotTypeRequestTypeDef]
    ) -> DescribeSlotTypeResponseTypeDef:
        """
        Gets metadata information about a slot type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/describe_slot_type.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#describe_slot_type)
        """

    async def describe_test_execution(
        self, **kwargs: Unpack[DescribeTestExecutionRequestTypeDef]
    ) -> DescribeTestExecutionResponseTypeDef:
        """
        Gets metadata information about the test execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/describe_test_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#describe_test_execution)
        """

    async def describe_test_set(
        self, **kwargs: Unpack[DescribeTestSetRequestTypeDef]
    ) -> DescribeTestSetResponseTypeDef:
        """
        Gets metadata information about the test set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/describe_test_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#describe_test_set)
        """

    async def describe_test_set_discrepancy_report(
        self, **kwargs: Unpack[DescribeTestSetDiscrepancyReportRequestTypeDef]
    ) -> DescribeTestSetDiscrepancyReportResponseTypeDef:
        """
        Gets metadata information about the test set discrepancy report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/describe_test_set_discrepancy_report.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#describe_test_set_discrepancy_report)
        """

    async def describe_test_set_generation(
        self, **kwargs: Unpack[DescribeTestSetGenerationRequestTypeDef]
    ) -> DescribeTestSetGenerationResponseTypeDef:
        """
        Gets metadata information about the test set generation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/describe_test_set_generation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#describe_test_set_generation)
        """

    async def generate_bot_element(
        self, **kwargs: Unpack[GenerateBotElementRequestTypeDef]
    ) -> GenerateBotElementResponseTypeDef:
        """
        Generates sample utterances for an intent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/generate_bot_element.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#generate_bot_element)
        """

    async def get_test_execution_artifacts_url(
        self, **kwargs: Unpack[GetTestExecutionArtifactsUrlRequestTypeDef]
    ) -> GetTestExecutionArtifactsUrlResponseTypeDef:
        """
        The pre-signed Amazon S3 URL to download the test execution result artifacts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/get_test_execution_artifacts_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#get_test_execution_artifacts_url)
        """

    async def list_aggregated_utterances(
        self, **kwargs: Unpack[ListAggregatedUtterancesRequestTypeDef]
    ) -> ListAggregatedUtterancesResponseTypeDef:
        """
        Provides a list of utterances that users have sent to the bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_aggregated_utterances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_aggregated_utterances)
        """

    async def list_bot_alias_replicas(
        self, **kwargs: Unpack[ListBotAliasReplicasRequestTypeDef]
    ) -> ListBotAliasReplicasResponseTypeDef:
        """
        The action to list the replicated bots created from the source bot alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_bot_alias_replicas.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_bot_alias_replicas)
        """

    async def list_bot_aliases(
        self, **kwargs: Unpack[ListBotAliasesRequestTypeDef]
    ) -> ListBotAliasesResponseTypeDef:
        """
        Gets a list of aliases for the specified bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_bot_aliases.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_bot_aliases)
        """

    async def list_bot_locales(
        self, **kwargs: Unpack[ListBotLocalesRequestTypeDef]
    ) -> ListBotLocalesResponseTypeDef:
        """
        Gets a list of locales for the specified bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_bot_locales.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_bot_locales)
        """

    async def list_bot_recommendations(
        self, **kwargs: Unpack[ListBotRecommendationsRequestTypeDef]
    ) -> ListBotRecommendationsResponseTypeDef:
        """
        Get a list of bot recommendations that meet the specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_bot_recommendations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_bot_recommendations)
        """

    async def list_bot_replicas(
        self, **kwargs: Unpack[ListBotReplicasRequestTypeDef]
    ) -> ListBotReplicasResponseTypeDef:
        """
        The action to list the replicated bots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_bot_replicas.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_bot_replicas)
        """

    async def list_bot_resource_generations(
        self, **kwargs: Unpack[ListBotResourceGenerationsRequestTypeDef]
    ) -> ListBotResourceGenerationsResponseTypeDef:
        """
        Lists the generation requests made for a bot locale.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_bot_resource_generations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_bot_resource_generations)
        """

    async def list_bot_version_replicas(
        self, **kwargs: Unpack[ListBotVersionReplicasRequestTypeDef]
    ) -> ListBotVersionReplicasResponseTypeDef:
        """
        Contains information about all the versions replication statuses applicable for
        Global Resiliency.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_bot_version_replicas.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_bot_version_replicas)
        """

    async def list_bot_versions(
        self, **kwargs: Unpack[ListBotVersionsRequestTypeDef]
    ) -> ListBotVersionsResponseTypeDef:
        """
        Gets information about all of the versions of a bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_bot_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_bot_versions)
        """

    async def list_bots(self, **kwargs: Unpack[ListBotsRequestTypeDef]) -> ListBotsResponseTypeDef:
        """
        Gets a list of available bots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_bots.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_bots)
        """

    async def list_built_in_intents(
        self, **kwargs: Unpack[ListBuiltInIntentsRequestTypeDef]
    ) -> ListBuiltInIntentsResponseTypeDef:
        """
        Gets a list of built-in intents provided by Amazon Lex that you can use in your
        bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_built_in_intents.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_built_in_intents)
        """

    async def list_built_in_slot_types(
        self, **kwargs: Unpack[ListBuiltInSlotTypesRequestTypeDef]
    ) -> ListBuiltInSlotTypesResponseTypeDef:
        """
        Gets a list of built-in slot types that meet the specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_built_in_slot_types.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_built_in_slot_types)
        """

    async def list_custom_vocabulary_items(
        self, **kwargs: Unpack[ListCustomVocabularyItemsRequestTypeDef]
    ) -> ListCustomVocabularyItemsResponseTypeDef:
        """
        Paginated list of custom vocabulary items for a given bot locale's custom
        vocabulary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_custom_vocabulary_items.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_custom_vocabulary_items)
        """

    async def list_exports(
        self, **kwargs: Unpack[ListExportsRequestTypeDef]
    ) -> ListExportsResponseTypeDef:
        """
        Lists the exports for a bot, bot locale, or custom vocabulary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_exports.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_exports)
        """

    async def list_imports(
        self, **kwargs: Unpack[ListImportsRequestTypeDef]
    ) -> ListImportsResponseTypeDef:
        """
        Lists the imports for a bot, bot locale, or custom vocabulary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_imports.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_imports)
        """

    async def list_intent_metrics(
        self, **kwargs: Unpack[ListIntentMetricsRequestTypeDef]
    ) -> ListIntentMetricsResponseTypeDef:
        """
        Retrieves summary metrics for the intents in your bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_intent_metrics.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_intent_metrics)
        """

    async def list_intent_paths(
        self, **kwargs: Unpack[ListIntentPathsRequestTypeDef]
    ) -> ListIntentPathsResponseTypeDef:
        """
        Retrieves summary statistics for a path of intents that users take over
        sessions with your bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_intent_paths.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_intent_paths)
        """

    async def list_intent_stage_metrics(
        self, **kwargs: Unpack[ListIntentStageMetricsRequestTypeDef]
    ) -> ListIntentStageMetricsResponseTypeDef:
        """
        Retrieves summary metrics for the stages within intents in your bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_intent_stage_metrics.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_intent_stage_metrics)
        """

    async def list_intents(
        self, **kwargs: Unpack[ListIntentsRequestTypeDef]
    ) -> ListIntentsResponseTypeDef:
        """
        Get a list of intents that meet the specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_intents.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_intents)
        """

    async def list_recommended_intents(
        self, **kwargs: Unpack[ListRecommendedIntentsRequestTypeDef]
    ) -> ListRecommendedIntentsResponseTypeDef:
        """
        Gets a list of recommended intents provided by the bot recommendation that you
        can use in your bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_recommended_intents.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_recommended_intents)
        """

    async def list_session_analytics_data(
        self, **kwargs: Unpack[ListSessionAnalyticsDataRequestTypeDef]
    ) -> ListSessionAnalyticsDataResponseTypeDef:
        """
        Retrieves a list of metadata for individual user sessions with your bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_session_analytics_data.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_session_analytics_data)
        """

    async def list_session_metrics(
        self, **kwargs: Unpack[ListSessionMetricsRequestTypeDef]
    ) -> ListSessionMetricsResponseTypeDef:
        """
        Retrieves summary metrics for the user sessions with your bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_session_metrics.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_session_metrics)
        """

    async def list_slot_types(
        self, **kwargs: Unpack[ListSlotTypesRequestTypeDef]
    ) -> ListSlotTypesResponseTypeDef:
        """
        Gets a list of slot types that match the specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_slot_types.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_slot_types)
        """

    async def list_slots(
        self, **kwargs: Unpack[ListSlotsRequestTypeDef]
    ) -> ListSlotsResponseTypeDef:
        """
        Gets a list of slots that match the specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_slots.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_slots)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Gets a list of tags associated with a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_tags_for_resource)
        """

    async def list_test_execution_result_items(
        self, **kwargs: Unpack[ListTestExecutionResultItemsRequestTypeDef]
    ) -> ListTestExecutionResultItemsResponseTypeDef:
        """
        Gets a list of test execution result items.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_test_execution_result_items.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_test_execution_result_items)
        """

    async def list_test_executions(
        self, **kwargs: Unpack[ListTestExecutionsRequestTypeDef]
    ) -> ListTestExecutionsResponseTypeDef:
        """
        The list of test set executions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_test_executions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_test_executions)
        """

    async def list_test_set_records(
        self, **kwargs: Unpack[ListTestSetRecordsRequestTypeDef]
    ) -> ListTestSetRecordsResponseTypeDef:
        """
        The list of test set records.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_test_set_records.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_test_set_records)
        """

    async def list_test_sets(
        self, **kwargs: Unpack[ListTestSetsRequestTypeDef]
    ) -> ListTestSetsResponseTypeDef:
        """
        The list of the test sets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_test_sets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_test_sets)
        """

    async def list_utterance_analytics_data(
        self, **kwargs: Unpack[ListUtteranceAnalyticsDataRequestTypeDef]
    ) -> ListUtteranceAnalyticsDataResponseTypeDef:
        """
        To use this API operation, your IAM role must have permissions to perform the
        <a
        href="https://docs.aws.amazon.com/lexv2/latest/APIReference/API_ListAggregatedUtterances.html">ListAggregatedUtterances</a>
        operation, which provides access to utterance-related analytics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_utterance_analytics_data.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_utterance_analytics_data)
        """

    async def list_utterance_metrics(
        self, **kwargs: Unpack[ListUtteranceMetricsRequestTypeDef]
    ) -> ListUtteranceMetricsResponseTypeDef:
        """
        To use this API operation, your IAM role must have permissions to perform the
        <a
        href="https://docs.aws.amazon.com/lexv2/latest/APIReference/API_ListAggregatedUtterances.html">ListAggregatedUtterances</a>
        operation, which provides access to utterance-related analytics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/list_utterance_metrics.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#list_utterance_metrics)
        """

    async def search_associated_transcripts(
        self, **kwargs: Unpack[SearchAssociatedTranscriptsRequestTypeDef]
    ) -> SearchAssociatedTranscriptsResponseTypeDef:
        """
        Search for associated transcripts that meet the specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/search_associated_transcripts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#search_associated_transcripts)
        """

    async def start_bot_recommendation(
        self, **kwargs: Unpack[StartBotRecommendationRequestTypeDef]
    ) -> StartBotRecommendationResponseTypeDef:
        """
        Use this to provide your transcript data, and to start the bot recommendation
        process.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/start_bot_recommendation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#start_bot_recommendation)
        """

    async def start_bot_resource_generation(
        self, **kwargs: Unpack[StartBotResourceGenerationRequestTypeDef]
    ) -> StartBotResourceGenerationResponseTypeDef:
        """
        Starts a request for the descriptive bot builder to generate a bot locale
        configuration based on the prompt you provide it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/start_bot_resource_generation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#start_bot_resource_generation)
        """

    async def start_import(
        self, **kwargs: Unpack[StartImportRequestTypeDef]
    ) -> StartImportResponseTypeDef:
        """
        Starts importing a bot, bot locale, or custom vocabulary from a zip archive
        that you uploaded to an S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/start_import.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#start_import)
        """

    async def start_test_execution(
        self, **kwargs: Unpack[StartTestExecutionRequestTypeDef]
    ) -> StartTestExecutionResponseTypeDef:
        """
        The action to start test set execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/start_test_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#start_test_execution)
        """

    async def start_test_set_generation(
        self, **kwargs: Unpack[StartTestSetGenerationRequestTypeDef]
    ) -> StartTestSetGenerationResponseTypeDef:
        """
        The action to start the generation of test set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/start_test_set_generation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#start_test_set_generation)
        """

    async def stop_bot_recommendation(
        self, **kwargs: Unpack[StopBotRecommendationRequestTypeDef]
    ) -> StopBotRecommendationResponseTypeDef:
        """
        Stop an already running Bot Recommendation request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/stop_bot_recommendation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#stop_bot_recommendation)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds the specified tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes tags from a bot, bot alias, or bot channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#untag_resource)
        """

    async def update_bot(
        self, **kwargs: Unpack[UpdateBotRequestTypeDef]
    ) -> UpdateBotResponseTypeDef:
        """
        Updates the configuration of an existing bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/update_bot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#update_bot)
        """

    async def update_bot_alias(
        self, **kwargs: Unpack[UpdateBotAliasRequestTypeDef]
    ) -> UpdateBotAliasResponseTypeDef:
        """
        Updates the configuration of an existing bot alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/update_bot_alias.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#update_bot_alias)
        """

    async def update_bot_locale(
        self, **kwargs: Unpack[UpdateBotLocaleRequestTypeDef]
    ) -> UpdateBotLocaleResponseTypeDef:
        """
        Updates the settings that a bot has for a specific locale.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/update_bot_locale.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#update_bot_locale)
        """

    async def update_bot_recommendation(
        self, **kwargs: Unpack[UpdateBotRecommendationRequestTypeDef]
    ) -> UpdateBotRecommendationResponseTypeDef:
        """
        Updates an existing bot recommendation request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/update_bot_recommendation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#update_bot_recommendation)
        """

    async def update_export(
        self, **kwargs: Unpack[UpdateExportRequestTypeDef]
    ) -> UpdateExportResponseTypeDef:
        """
        Updates the password used to protect an export zip archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/update_export.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#update_export)
        """

    async def update_intent(
        self, **kwargs: Unpack[UpdateIntentRequestTypeDef]
    ) -> UpdateIntentResponseTypeDef:
        """
        Updates the settings for an intent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/update_intent.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#update_intent)
        """

    async def update_resource_policy(
        self, **kwargs: Unpack[UpdateResourcePolicyRequestTypeDef]
    ) -> UpdateResourcePolicyResponseTypeDef:
        """
        Replaces the existing resource policy for a bot or bot alias with a new one.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/update_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#update_resource_policy)
        """

    async def update_slot(
        self, **kwargs: Unpack[UpdateSlotRequestTypeDef]
    ) -> UpdateSlotResponseTypeDef:
        """
        Updates the settings for a slot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/update_slot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#update_slot)
        """

    async def update_slot_type(
        self, **kwargs: Unpack[UpdateSlotTypeRequestTypeDef]
    ) -> UpdateSlotTypeResponseTypeDef:
        """
        Updates the configuration of an existing slot type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/update_slot_type.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#update_slot_type)
        """

    async def update_test_set(
        self, **kwargs: Unpack[UpdateTestSetRequestTypeDef]
    ) -> UpdateTestSetResponseTypeDef:
        """
        The action to update the test set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/update_test_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#update_test_set)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["bot_alias_available"]
    ) -> BotAliasAvailableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["bot_available"]
    ) -> BotAvailableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["bot_export_completed"]
    ) -> BotExportCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["bot_import_completed"]
    ) -> BotImportCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["bot_locale_built"]
    ) -> BotLocaleBuiltWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["bot_locale_created"]
    ) -> BotLocaleCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["bot_locale_express_testing_available"]
    ) -> BotLocaleExpressTestingAvailableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["bot_version_available"]
    ) -> BotVersionAvailableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/#get_waiter)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/client/)
        """
