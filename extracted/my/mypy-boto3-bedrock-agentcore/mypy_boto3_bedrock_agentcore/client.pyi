"""
Type annotations for bedrock-agentcore service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_bedrock_agentcore.client import BedrockAgentCoreClient

    session = Session()
    client: BedrockAgentCoreClient = session.client("bedrock-agentcore")
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
    ListABTestsPaginator,
    ListActorsPaginator,
    ListBatchEvaluationsPaginator,
    ListEventsPaginator,
    ListMemoryExtractionJobsPaginator,
    ListMemoryRecordsPaginator,
    ListPaymentInstrumentsPaginator,
    ListPaymentSessionsPaginator,
    ListRecommendationsPaginator,
    ListSessionsPaginator,
    RetrieveMemoryRecordsPaginator,
)
from .type_defs import (
    BatchCreateMemoryRecordsInputTypeDef,
    BatchCreateMemoryRecordsOutputTypeDef,
    BatchDeleteMemoryRecordsInputTypeDef,
    BatchDeleteMemoryRecordsOutputTypeDef,
    BatchUpdateMemoryRecordsInputTypeDef,
    BatchUpdateMemoryRecordsOutputTypeDef,
    CompleteResourceTokenAuthRequestTypeDef,
    CreateABTestRequestTypeDef,
    CreateABTestResponseTypeDef,
    CreateEventInputTypeDef,
    CreateEventOutputTypeDef,
    CreatePaymentInstrumentRequestTypeDef,
    CreatePaymentInstrumentResponseTypeDef,
    CreatePaymentSessionRequestTypeDef,
    CreatePaymentSessionResponseTypeDef,
    DeleteABTestRequestTypeDef,
    DeleteABTestResponseTypeDef,
    DeleteBatchEvaluationRequestTypeDef,
    DeleteBatchEvaluationResponseTypeDef,
    DeleteEventInputTypeDef,
    DeleteEventOutputTypeDef,
    DeleteMemoryRecordInputTypeDef,
    DeleteMemoryRecordOutputTypeDef,
    DeletePaymentInstrumentRequestTypeDef,
    DeletePaymentInstrumentResponseTypeDef,
    DeletePaymentSessionRequestTypeDef,
    DeletePaymentSessionResponseTypeDef,
    DeleteRecommendationRequestTypeDef,
    DeleteRecommendationResponseTypeDef,
    EvaluateRequestTypeDef,
    EvaluateResponseTypeDef,
    GetABTestRequestTypeDef,
    GetABTestResponseTypeDef,
    GetAgentCardRequestTypeDef,
    GetAgentCardResponseTypeDef,
    GetBatchEvaluationRequestTypeDef,
    GetBatchEvaluationResponseTypeDef,
    GetBrowserSessionRequestTypeDef,
    GetBrowserSessionResponseTypeDef,
    GetCodeInterpreterSessionRequestTypeDef,
    GetCodeInterpreterSessionResponseTypeDef,
    GetEventInputTypeDef,
    GetEventOutputTypeDef,
    GetMemoryRecordInputTypeDef,
    GetMemoryRecordOutputTypeDef,
    GetPaymentInstrumentBalanceRequestTypeDef,
    GetPaymentInstrumentBalanceResponseTypeDef,
    GetPaymentInstrumentRequestTypeDef,
    GetPaymentInstrumentResponseTypeDef,
    GetPaymentSessionRequestTypeDef,
    GetPaymentSessionResponseTypeDef,
    GetRecommendationRequestTypeDef,
    GetRecommendationResponseTypeDef,
    GetResourceApiKeyRequestTypeDef,
    GetResourceApiKeyResponseTypeDef,
    GetResourceOauth2TokenRequestTypeDef,
    GetResourceOauth2TokenResponseTypeDef,
    GetResourcePaymentTokenRequestTypeDef,
    GetResourcePaymentTokenResponseTypeDef,
    GetWorkloadAccessTokenForJWTRequestTypeDef,
    GetWorkloadAccessTokenForJWTResponseTypeDef,
    GetWorkloadAccessTokenForUserIdRequestTypeDef,
    GetWorkloadAccessTokenForUserIdResponseTypeDef,
    GetWorkloadAccessTokenRequestTypeDef,
    GetWorkloadAccessTokenResponseTypeDef,
    InvokeAgentRuntimeCommandRequestTypeDef,
    InvokeAgentRuntimeCommandResponseTypeDef,
    InvokeAgentRuntimeRequestTypeDef,
    InvokeAgentRuntimeResponseTypeDef,
    InvokeBrowserRequestTypeDef,
    InvokeBrowserResponseTypeDef,
    InvokeCodeInterpreterRequestTypeDef,
    InvokeCodeInterpreterResponseTypeDef,
    InvokeHarnessRequestTypeDef,
    InvokeHarnessResponseTypeDef,
    ListABTestsRequestTypeDef,
    ListABTestsResponseTypeDef,
    ListActorsInputTypeDef,
    ListActorsOutputTypeDef,
    ListBatchEvaluationsRequestTypeDef,
    ListBatchEvaluationsResponseTypeDef,
    ListBrowserSessionsRequestTypeDef,
    ListBrowserSessionsResponseTypeDef,
    ListCodeInterpreterSessionsRequestTypeDef,
    ListCodeInterpreterSessionsResponseTypeDef,
    ListEventsInputTypeDef,
    ListEventsOutputTypeDef,
    ListMemoryExtractionJobsInputTypeDef,
    ListMemoryExtractionJobsOutputTypeDef,
    ListMemoryRecordsInputTypeDef,
    ListMemoryRecordsOutputTypeDef,
    ListPaymentInstrumentsRequestTypeDef,
    ListPaymentInstrumentsResponseTypeDef,
    ListPaymentSessionsRequestTypeDef,
    ListPaymentSessionsResponseTypeDef,
    ListRecommendationsRequestTypeDef,
    ListRecommendationsResponseTypeDef,
    ListSessionsInputTypeDef,
    ListSessionsOutputTypeDef,
    ProcessPaymentRequestTypeDef,
    ProcessPaymentResponseTypeDef,
    RetrieveMemoryRecordsInputTypeDef,
    RetrieveMemoryRecordsOutputTypeDef,
    SaveBrowserSessionProfileRequestTypeDef,
    SaveBrowserSessionProfileResponseTypeDef,
    SearchRegistryRecordsRequestTypeDef,
    SearchRegistryRecordsResponseTypeDef,
    StartBatchEvaluationRequestTypeDef,
    StartBatchEvaluationResponseTypeDef,
    StartBrowserSessionRequestTypeDef,
    StartBrowserSessionResponseTypeDef,
    StartCodeInterpreterSessionRequestTypeDef,
    StartCodeInterpreterSessionResponseTypeDef,
    StartMemoryExtractionJobInputTypeDef,
    StartMemoryExtractionJobOutputTypeDef,
    StartRecommendationRequestTypeDef,
    StartRecommendationResponseTypeDef,
    StopBatchEvaluationRequestTypeDef,
    StopBatchEvaluationResponseTypeDef,
    StopBrowserSessionRequestTypeDef,
    StopBrowserSessionResponseTypeDef,
    StopCodeInterpreterSessionRequestTypeDef,
    StopCodeInterpreterSessionResponseTypeDef,
    StopRuntimeSessionRequestTypeDef,
    StopRuntimeSessionResponseTypeDef,
    UpdateABTestRequestTypeDef,
    UpdateABTestResponseTypeDef,
    UpdateBrowserStreamRequestTypeDef,
    UpdateBrowserStreamResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("BedrockAgentCoreClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    DuplicateIdException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    InvalidInputException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    RetryableConflictException: type[BotocoreClientError]
    RuntimeClientError: type[BotocoreClientError]
    ServiceException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottledException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    UnauthorizedException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class BedrockAgentCoreClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore.html#BedrockAgentCore.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BedrockAgentCoreClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore.html#BedrockAgentCore.Client)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/can_paginate.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/generate_presigned_url.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#generate_presigned_url)
        """

    def batch_create_memory_records(
        self, **kwargs: Unpack[BatchCreateMemoryRecordsInputTypeDef]
    ) -> BatchCreateMemoryRecordsOutputTypeDef:
        """
        Creates multiple memory records in a single batch operation for the specified
        memory with custom content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/batch_create_memory_records.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#batch_create_memory_records)
        """

    def batch_delete_memory_records(
        self, **kwargs: Unpack[BatchDeleteMemoryRecordsInputTypeDef]
    ) -> BatchDeleteMemoryRecordsOutputTypeDef:
        """
        Deletes multiple memory records in a single batch operation from the specified
        memory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/batch_delete_memory_records.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#batch_delete_memory_records)
        """

    def batch_update_memory_records(
        self, **kwargs: Unpack[BatchUpdateMemoryRecordsInputTypeDef]
    ) -> BatchUpdateMemoryRecordsOutputTypeDef:
        """
        Updates multiple memory records with custom content in a single batch operation
        within the specified memory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/batch_update_memory_records.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#batch_update_memory_records)
        """

    def complete_resource_token_auth(
        self, **kwargs: Unpack[CompleteResourceTokenAuthRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Confirms the user authentication session for obtaining OAuth2.0 tokens for a
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/complete_resource_token_auth.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#complete_resource_token_auth)
        """

    def create_ab_test(
        self, **kwargs: Unpack[CreateABTestRequestTypeDef]
    ) -> CreateABTestResponseTypeDef:
        """
        Creates an A/B test for comparing agent configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/create_ab_test.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#create_ab_test)
        """

    def create_event(self, **kwargs: Unpack[CreateEventInputTypeDef]) -> CreateEventOutputTypeDef:
        """
        Creates an event in an AgentCore Memory resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/create_event.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#create_event)
        """

    def create_payment_instrument(
        self, **kwargs: Unpack[CreatePaymentInstrumentRequestTypeDef]
    ) -> CreatePaymentInstrumentResponseTypeDef:
        """
        Create a new payment instrument for a connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/create_payment_instrument.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#create_payment_instrument)
        """

    def create_payment_session(
        self, **kwargs: Unpack[CreatePaymentSessionRequestTypeDef]
    ) -> CreatePaymentSessionResponseTypeDef:
        """
        Create a new payment manager session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/create_payment_session.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#create_payment_session)
        """

    def delete_ab_test(
        self, **kwargs: Unpack[DeleteABTestRequestTypeDef]
    ) -> DeleteABTestResponseTypeDef:
        """
        Deletes an A/B test and its associated gateway rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/delete_ab_test.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#delete_ab_test)
        """

    def delete_batch_evaluation(
        self, **kwargs: Unpack[DeleteBatchEvaluationRequestTypeDef]
    ) -> DeleteBatchEvaluationResponseTypeDef:
        """
        Deletes a batch evaluation and its associated results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/delete_batch_evaluation.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#delete_batch_evaluation)
        """

    def delete_event(self, **kwargs: Unpack[DeleteEventInputTypeDef]) -> DeleteEventOutputTypeDef:
        """
        Deletes an event from an AgentCore Memory resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/delete_event.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#delete_event)
        """

    def delete_memory_record(
        self, **kwargs: Unpack[DeleteMemoryRecordInputTypeDef]
    ) -> DeleteMemoryRecordOutputTypeDef:
        """
        Deletes a memory record from an AgentCore Memory resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/delete_memory_record.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#delete_memory_record)
        """

    def delete_payment_instrument(
        self, **kwargs: Unpack[DeletePaymentInstrumentRequestTypeDef]
    ) -> DeletePaymentInstrumentResponseTypeDef:
        """
        Delete a payment instrument.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/delete_payment_instrument.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#delete_payment_instrument)
        """

    def delete_payment_session(
        self, **kwargs: Unpack[DeletePaymentSessionRequestTypeDef]
    ) -> DeletePaymentSessionResponseTypeDef:
        """
        Delete a payment manager session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/delete_payment_session.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#delete_payment_session)
        """

    def delete_recommendation(
        self, **kwargs: Unpack[DeleteRecommendationRequestTypeDef]
    ) -> DeleteRecommendationResponseTypeDef:
        """
        Deletes a recommendation and its associated results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/delete_recommendation.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#delete_recommendation)
        """

    def evaluate(self, **kwargs: Unpack[EvaluateRequestTypeDef]) -> EvaluateResponseTypeDef:
        """
        Performs on-demand evaluation of agent traces using a specified evaluator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/evaluate.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#evaluate)
        """

    def get_ab_test(self, **kwargs: Unpack[GetABTestRequestTypeDef]) -> GetABTestResponseTypeDef:
        """
        Retrieves detailed information about an A/B test, including its configuration,
        status, and statistical results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_ab_test.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_ab_test)
        """

    def get_agent_card(
        self, **kwargs: Unpack[GetAgentCardRequestTypeDef]
    ) -> GetAgentCardResponseTypeDef:
        """
        Retrieves the A2A agent card associated with an AgentCore Runtime agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_agent_card.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_agent_card)
        """

    def get_batch_evaluation(
        self, **kwargs: Unpack[GetBatchEvaluationRequestTypeDef]
    ) -> GetBatchEvaluationResponseTypeDef:
        """
        Retrieves detailed information about a batch evaluation, including its status,
        configuration, results, and any error details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_batch_evaluation.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_batch_evaluation)
        """

    def get_browser_session(
        self, **kwargs: Unpack[GetBrowserSessionRequestTypeDef]
    ) -> GetBrowserSessionResponseTypeDef:
        """
        Retrieves detailed information about a specific browser session in Amazon
        Bedrock AgentCore.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_browser_session.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_browser_session)
        """

    def get_code_interpreter_session(
        self, **kwargs: Unpack[GetCodeInterpreterSessionRequestTypeDef]
    ) -> GetCodeInterpreterSessionResponseTypeDef:
        """
        Retrieves detailed information about a specific code interpreter session in
        Amazon Bedrock AgentCore.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_code_interpreter_session.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_code_interpreter_session)
        """

    def get_event(self, **kwargs: Unpack[GetEventInputTypeDef]) -> GetEventOutputTypeDef:
        """
        Retrieves information about a specific event in an AgentCore Memory resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_event.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_event)
        """

    def get_memory_record(
        self, **kwargs: Unpack[GetMemoryRecordInputTypeDef]
    ) -> GetMemoryRecordOutputTypeDef:
        """
        Retrieves a specific memory record from an AgentCore Memory resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_memory_record.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_memory_record)
        """

    def get_payment_instrument(
        self, **kwargs: Unpack[GetPaymentInstrumentRequestTypeDef]
    ) -> GetPaymentInstrumentResponseTypeDef:
        """
        Get a payment instrument by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_payment_instrument.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_payment_instrument)
        """

    def get_payment_instrument_balance(
        self, **kwargs: Unpack[GetPaymentInstrumentBalanceRequestTypeDef]
    ) -> GetPaymentInstrumentBalanceResponseTypeDef:
        """
        Get the balance of a payment instrument.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_payment_instrument_balance.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_payment_instrument_balance)
        """

    def get_payment_session(
        self, **kwargs: Unpack[GetPaymentSessionRequestTypeDef]
    ) -> GetPaymentSessionResponseTypeDef:
        """
        Get a payment session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_payment_session.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_payment_session)
        """

    def get_recommendation(
        self, **kwargs: Unpack[GetRecommendationRequestTypeDef]
    ) -> GetRecommendationResponseTypeDef:
        """
        Retrieves detailed information about a recommendation, including its
        configuration, status, and results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_recommendation.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_recommendation)
        """

    def get_resource_api_key(
        self, **kwargs: Unpack[GetResourceApiKeyRequestTypeDef]
    ) -> GetResourceApiKeyResponseTypeDef:
        """
        Retrieves the API key associated with an API key credential provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_resource_api_key.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_resource_api_key)
        """

    def get_resource_oauth2_token(
        self, **kwargs: Unpack[GetResourceOauth2TokenRequestTypeDef]
    ) -> GetResourceOauth2TokenResponseTypeDef:
        """
        Returns the OAuth 2.0 token of the provided resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_resource_oauth2_token.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_resource_oauth2_token)
        """

    def get_resource_payment_token(
        self, **kwargs: Unpack[GetResourcePaymentTokenRequestTypeDef]
    ) -> GetResourcePaymentTokenResponseTypeDef:
        """
        Generates authentication tokens for payment providers that use vendor-specific
        authentication mechanisms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_resource_payment_token.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_resource_payment_token)
        """

    def get_workload_access_token(
        self, **kwargs: Unpack[GetWorkloadAccessTokenRequestTypeDef]
    ) -> GetWorkloadAccessTokenResponseTypeDef:
        """
        Obtains a workload access token for agentic workloads not acting on behalf of a
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_workload_access_token.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_workload_access_token)
        """

    def get_workload_access_token_for_jwt(
        self, **kwargs: Unpack[GetWorkloadAccessTokenForJWTRequestTypeDef]
    ) -> GetWorkloadAccessTokenForJWTResponseTypeDef:
        """
        Obtains a workload access token for agentic workloads acting on behalf of a
        user, using a JWT token.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_workload_access_token_for_jwt.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_workload_access_token_for_jwt)
        """

    def get_workload_access_token_for_user_id(
        self, **kwargs: Unpack[GetWorkloadAccessTokenForUserIdRequestTypeDef]
    ) -> GetWorkloadAccessTokenForUserIdResponseTypeDef:
        """
        Obtains a workload access token for agentic workloads acting on behalf of a
        user, using the user's ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_workload_access_token_for_user_id.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_workload_access_token_for_user_id)
        """

    def invoke_agent_runtime(
        self, **kwargs: Unpack[InvokeAgentRuntimeRequestTypeDef]
    ) -> InvokeAgentRuntimeResponseTypeDef:
        """
        Sends a request to an agent or tool hosted in an Amazon Bedrock AgentCore
        Runtime and receives responses in real-time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/invoke_agent_runtime.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#invoke_agent_runtime)
        """

    def invoke_agent_runtime_command(
        self, **kwargs: Unpack[InvokeAgentRuntimeCommandRequestTypeDef]
    ) -> InvokeAgentRuntimeCommandResponseTypeDef:
        """
        Executes a command in a runtime session container and streams the output back
        to the caller.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/invoke_agent_runtime_command.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#invoke_agent_runtime_command)
        """

    def invoke_browser(
        self, **kwargs: Unpack[InvokeBrowserRequestTypeDef]
    ) -> InvokeBrowserResponseTypeDef:
        """
        Invokes an operating system-level action on a browser session in Amazon Bedrock
        AgentCore.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/invoke_browser.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#invoke_browser)
        """

    def invoke_code_interpreter(
        self, **kwargs: Unpack[InvokeCodeInterpreterRequestTypeDef]
    ) -> InvokeCodeInterpreterResponseTypeDef:
        """
        Executes code within an active code interpreter session in Amazon Bedrock
        AgentCore.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/invoke_code_interpreter.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#invoke_code_interpreter)
        """

    def invoke_harness(
        self, **kwargs: Unpack[InvokeHarnessRequestTypeDef]
    ) -> InvokeHarnessResponseTypeDef:
        """
        Operation to invoke a Harness.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/invoke_harness.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#invoke_harness)
        """

    def list_ab_tests(
        self, **kwargs: Unpack[ListABTestsRequestTypeDef]
    ) -> ListABTestsResponseTypeDef:
        """
        Lists all A/B tests in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/list_ab_tests.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#list_ab_tests)
        """

    def list_actors(self, **kwargs: Unpack[ListActorsInputTypeDef]) -> ListActorsOutputTypeDef:
        """
        Lists all actors in an AgentCore Memory resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/list_actors.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#list_actors)
        """

    def list_batch_evaluations(
        self, **kwargs: Unpack[ListBatchEvaluationsRequestTypeDef]
    ) -> ListBatchEvaluationsResponseTypeDef:
        """
        Lists all batch evaluations in the account, providing summary information about
        each evaluation's status and configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/list_batch_evaluations.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#list_batch_evaluations)
        """

    def list_browser_sessions(
        self, **kwargs: Unpack[ListBrowserSessionsRequestTypeDef]
    ) -> ListBrowserSessionsResponseTypeDef:
        """
        Retrieves a list of browser sessions in Amazon Bedrock AgentCore that match the
        specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/list_browser_sessions.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#list_browser_sessions)
        """

    def list_code_interpreter_sessions(
        self, **kwargs: Unpack[ListCodeInterpreterSessionsRequestTypeDef]
    ) -> ListCodeInterpreterSessionsResponseTypeDef:
        """
        Retrieves a list of code interpreter sessions in Amazon Bedrock AgentCore that
        match the specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/list_code_interpreter_sessions.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#list_code_interpreter_sessions)
        """

    def list_events(self, **kwargs: Unpack[ListEventsInputTypeDef]) -> ListEventsOutputTypeDef:
        """
        Lists events in an AgentCore Memory resource based on specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/list_events.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#list_events)
        """

    def list_memory_extraction_jobs(
        self, **kwargs: Unpack[ListMemoryExtractionJobsInputTypeDef]
    ) -> ListMemoryExtractionJobsOutputTypeDef:
        """
        Lists all long-term memory extraction jobs that are eligible to be started with
        optional filtering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/list_memory_extraction_jobs.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#list_memory_extraction_jobs)
        """

    def list_memory_records(
        self, **kwargs: Unpack[ListMemoryRecordsInputTypeDef]
    ) -> ListMemoryRecordsOutputTypeDef:
        """
        Lists memory records in an AgentCore Memory resource based on specified
        criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/list_memory_records.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#list_memory_records)
        """

    def list_payment_instruments(
        self, **kwargs: Unpack[ListPaymentInstrumentsRequestTypeDef]
    ) -> ListPaymentInstrumentsResponseTypeDef:
        """
        List payment instruments for a manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/list_payment_instruments.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#list_payment_instruments)
        """

    def list_payment_sessions(
        self, **kwargs: Unpack[ListPaymentSessionsRequestTypeDef]
    ) -> ListPaymentSessionsResponseTypeDef:
        """
        List payment manager sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/list_payment_sessions.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#list_payment_sessions)
        """

    def list_recommendations(
        self, **kwargs: Unpack[ListRecommendationsRequestTypeDef]
    ) -> ListRecommendationsResponseTypeDef:
        """
        Lists all recommendations in the account, with optional filtering by status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/list_recommendations.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#list_recommendations)
        """

    def list_sessions(
        self, **kwargs: Unpack[ListSessionsInputTypeDef]
    ) -> ListSessionsOutputTypeDef:
        """
        Lists sessions in an AgentCore Memory resource based on specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/list_sessions.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#list_sessions)
        """

    def process_payment(
        self, **kwargs: Unpack[ProcessPaymentRequestTypeDef]
    ) -> ProcessPaymentResponseTypeDef:
        """
        Process a payment transaction.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/process_payment.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#process_payment)
        """

    def retrieve_memory_records(
        self, **kwargs: Unpack[RetrieveMemoryRecordsInputTypeDef]
    ) -> RetrieveMemoryRecordsOutputTypeDef:
        """
        Searches for and retrieves memory records from an AgentCore Memory resource
        based on specified search criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/retrieve_memory_records.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#retrieve_memory_records)
        """

    def save_browser_session_profile(
        self, **kwargs: Unpack[SaveBrowserSessionProfileRequestTypeDef]
    ) -> SaveBrowserSessionProfileResponseTypeDef:
        """
        Saves the current state of a browser session as a reusable profile in Amazon
        Bedrock AgentCore.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/save_browser_session_profile.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#save_browser_session_profile)
        """

    def search_registry_records(
        self, **kwargs: Unpack[SearchRegistryRecordsRequestTypeDef]
    ) -> SearchRegistryRecordsResponseTypeDef:
        """
        Searches for registry records using semantic, lexical, or hybrid queries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/search_registry_records.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#search_registry_records)
        """

    def start_batch_evaluation(
        self, **kwargs: Unpack[StartBatchEvaluationRequestTypeDef]
    ) -> StartBatchEvaluationResponseTypeDef:
        """
        Starts a batch evaluation job that evaluates agent performance across multiple
        sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/start_batch_evaluation.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#start_batch_evaluation)
        """

    def start_browser_session(
        self, **kwargs: Unpack[StartBrowserSessionRequestTypeDef]
    ) -> StartBrowserSessionResponseTypeDef:
        """
        Creates and initializes a browser session in Amazon Bedrock AgentCore.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/start_browser_session.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#start_browser_session)
        """

    def start_code_interpreter_session(
        self, **kwargs: Unpack[StartCodeInterpreterSessionRequestTypeDef]
    ) -> StartCodeInterpreterSessionResponseTypeDef:
        """
        Creates and initializes a code interpreter session in Amazon Bedrock AgentCore.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/start_code_interpreter_session.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#start_code_interpreter_session)
        """

    def start_memory_extraction_job(
        self, **kwargs: Unpack[StartMemoryExtractionJobInputTypeDef]
    ) -> StartMemoryExtractionJobOutputTypeDef:
        """
        Starts a memory extraction job that processes events that failed extraction
        previously in an AgentCore Memory resource and produces structured memory
        records.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/start_memory_extraction_job.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#start_memory_extraction_job)
        """

    def start_recommendation(
        self, **kwargs: Unpack[StartRecommendationRequestTypeDef]
    ) -> StartRecommendationResponseTypeDef:
        """
        Starts a recommendation job that analyzes agent traces and generates
        optimization suggestions for system prompts or tool descriptions to improve
        agent performance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/start_recommendation.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#start_recommendation)
        """

    def stop_batch_evaluation(
        self, **kwargs: Unpack[StopBatchEvaluationRequestTypeDef]
    ) -> StopBatchEvaluationResponseTypeDef:
        """
        Stops a running batch evaluation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/stop_batch_evaluation.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#stop_batch_evaluation)
        """

    def stop_browser_session(
        self, **kwargs: Unpack[StopBrowserSessionRequestTypeDef]
    ) -> StopBrowserSessionResponseTypeDef:
        """
        Terminates an active browser session in Amazon Bedrock AgentCore.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/stop_browser_session.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#stop_browser_session)
        """

    def stop_code_interpreter_session(
        self, **kwargs: Unpack[StopCodeInterpreterSessionRequestTypeDef]
    ) -> StopCodeInterpreterSessionResponseTypeDef:
        """
        Terminates an active code interpreter session in Amazon Bedrock AgentCore.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/stop_code_interpreter_session.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#stop_code_interpreter_session)
        """

    def stop_runtime_session(
        self, **kwargs: Unpack[StopRuntimeSessionRequestTypeDef]
    ) -> StopRuntimeSessionResponseTypeDef:
        """
        Stops a session that is running in an running AgentCore Runtime agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/stop_runtime_session.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#stop_runtime_session)
        """

    def update_ab_test(
        self, **kwargs: Unpack[UpdateABTestRequestTypeDef]
    ) -> UpdateABTestResponseTypeDef:
        """
        Updates an A/B test's configuration, including variants, traffic allocation,
        evaluation settings, or execution status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/update_ab_test.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#update_ab_test)
        """

    def update_browser_stream(
        self, **kwargs: Unpack[UpdateBrowserStreamRequestTypeDef]
    ) -> UpdateBrowserStreamResponseTypeDef:
        """
        Updates a browser stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/update_browser_stream.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#update_browser_stream)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_ab_tests"]
    ) -> ListABTestsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_actors"]
    ) -> ListActorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_batch_evaluations"]
    ) -> ListBatchEvaluationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_events"]
    ) -> ListEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_memory_extraction_jobs"]
    ) -> ListMemoryExtractionJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_memory_records"]
    ) -> ListMemoryRecordsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_payment_instruments"]
    ) -> ListPaymentInstrumentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_payment_sessions"]
    ) -> ListPaymentSessionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_recommendations"]
    ) -> ListRecommendationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_sessions"]
    ) -> ListSessionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["retrieve_memory_records"]
    ) -> RetrieveMemoryRecordsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore/client/#get_paginator)
        """
