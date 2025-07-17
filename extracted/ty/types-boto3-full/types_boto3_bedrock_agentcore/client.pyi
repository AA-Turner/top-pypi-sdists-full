"""
Type annotations for bedrock-agentcore service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_bedrock_agentcore.client import BedrockAgentCoreDataPlaneFrontingLayerClient

    session = Session()
    client: BedrockAgentCoreDataPlaneFrontingLayerClient = session.client("bedrock-agentcore")
    ```
"""

from __future__ import annotations

import sys
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListActorsPaginator,
    ListEventsPaginator,
    ListMemoryRecordsPaginator,
    ListSessionsPaginator,
    RetrieveMemoryRecordsPaginator,
)
from .type_defs import (
    CreateEventInputTypeDef,
    CreateEventOutputTypeDef,
    DeleteEventInputTypeDef,
    DeleteEventOutputTypeDef,
    DeleteMemoryRecordInputTypeDef,
    DeleteMemoryRecordOutputTypeDef,
    GetBrowserSessionRequestTypeDef,
    GetBrowserSessionResponseTypeDef,
    GetCodeInterpreterSessionRequestTypeDef,
    GetCodeInterpreterSessionResponseTypeDef,
    GetEventInputTypeDef,
    GetEventOutputTypeDef,
    GetMemoryRecordInputTypeDef,
    GetMemoryRecordOutputTypeDef,
    GetResourceApiKeyRequestTypeDef,
    GetResourceApiKeyResponseTypeDef,
    GetResourceOauth2TokenRequestTypeDef,
    GetResourceOauth2TokenResponseTypeDef,
    GetWorkloadAccessTokenForJWTRequestTypeDef,
    GetWorkloadAccessTokenForJWTResponseTypeDef,
    GetWorkloadAccessTokenForUserIdRequestTypeDef,
    GetWorkloadAccessTokenForUserIdResponseTypeDef,
    GetWorkloadAccessTokenRequestTypeDef,
    GetWorkloadAccessTokenResponseTypeDef,
    InvokeAgentRuntimeRequestTypeDef,
    InvokeAgentRuntimeResponseTypeDef,
    InvokeCodeInterpreterRequestTypeDef,
    InvokeCodeInterpreterResponseTypeDef,
    ListActorsInputTypeDef,
    ListActorsOutputTypeDef,
    ListBrowserSessionsRequestTypeDef,
    ListBrowserSessionsResponseTypeDef,
    ListCodeInterpreterSessionsRequestTypeDef,
    ListCodeInterpreterSessionsResponseTypeDef,
    ListEventsInputTypeDef,
    ListEventsOutputTypeDef,
    ListMemoryRecordsInputTypeDef,
    ListMemoryRecordsOutputTypeDef,
    ListSessionsInputTypeDef,
    ListSessionsOutputTypeDef,
    RetrieveMemoryRecordsInputTypeDef,
    RetrieveMemoryRecordsOutputTypeDef,
    StartBrowserSessionRequestTypeDef,
    StartBrowserSessionResponseTypeDef,
    StartCodeInterpreterSessionRequestTypeDef,
    StartCodeInterpreterSessionResponseTypeDef,
    StopBrowserSessionRequestTypeDef,
    StopBrowserSessionResponseTypeDef,
    StopCodeInterpreterSessionRequestTypeDef,
    StopCodeInterpreterSessionResponseTypeDef,
    UpdateBrowserStreamRequestTypeDef,
    UpdateBrowserStreamResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("BedrockAgentCoreDataPlaneFrontingLayerClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    RuntimeClientError: Type[BotocoreClientError]
    ServiceException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottledException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class BedrockAgentCoreDataPlaneFrontingLayerClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore.html#BedrockAgentCoreDataPlaneFrontingLayer.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BedrockAgentCoreDataPlaneFrontingLayerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore.html#BedrockAgentCoreDataPlaneFrontingLayer.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#can_paginate)
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
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#generate_presigned_url)
        """

    def create_event(self, **kwargs: Unpack[CreateEventInputTypeDef]) -> CreateEventOutputTypeDef:
        """
        Creates an event in a memory store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/create_event.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#create_event)
        """

    def delete_event(self, **kwargs: Unpack[DeleteEventInputTypeDef]) -> DeleteEventOutputTypeDef:
        """
        Deletes an event from a memory store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/delete_event.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#delete_event)
        """

    def delete_memory_record(
        self, **kwargs: Unpack[DeleteMemoryRecordInputTypeDef]
    ) -> DeleteMemoryRecordOutputTypeDef:
        """
        Deletes a memory record from a memory store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/delete_memory_record.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#delete_memory_record)
        """

    def get_browser_session(
        self, **kwargs: Unpack[GetBrowserSessionRequestTypeDef]
    ) -> GetBrowserSessionResponseTypeDef:
        """
        Retrieves detailed information about a specific browser session in Amazon
        Bedrock.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_browser_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#get_browser_session)
        """

    def get_code_interpreter_session(
        self, **kwargs: Unpack[GetCodeInterpreterSessionRequestTypeDef]
    ) -> GetCodeInterpreterSessionResponseTypeDef:
        """
        Retrieves detailed information about a specific code interpreter session in
        Amazon Bedrock.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_code_interpreter_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#get_code_interpreter_session)
        """

    def get_event(self, **kwargs: Unpack[GetEventInputTypeDef]) -> GetEventOutputTypeDef:
        """
        Retrieves information about a specific event in a memory store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_event.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#get_event)
        """

    def get_memory_record(
        self, **kwargs: Unpack[GetMemoryRecordInputTypeDef]
    ) -> GetMemoryRecordOutputTypeDef:
        """
        Retrieves a specific memory record from a memory store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_memory_record.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#get_memory_record)
        """

    def get_resource_api_key(
        self, **kwargs: Unpack[GetResourceApiKeyRequestTypeDef]
    ) -> GetResourceApiKeyResponseTypeDef:
        """
        Retrieves an API Key associated with an API Key Credential Provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_resource_api_key.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#get_resource_api_key)
        """

    def get_resource_oauth2_token(
        self, **kwargs: Unpack[GetResourceOauth2TokenRequestTypeDef]
    ) -> GetResourceOauth2TokenResponseTypeDef:
        """
        Reaturns the Oauth2Token of the provided resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_resource_oauth2_token.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#get_resource_oauth2_token)
        """

    def get_workload_access_token(
        self, **kwargs: Unpack[GetWorkloadAccessTokenRequestTypeDef]
    ) -> GetWorkloadAccessTokenResponseTypeDef:
        """
        Obtains an Workload access token for agentic workloads not acting on behalf of
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_workload_access_token.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#get_workload_access_token)
        """

    def get_workload_access_token_for_jwt(
        self, **kwargs: Unpack[GetWorkloadAccessTokenForJWTRequestTypeDef]
    ) -> GetWorkloadAccessTokenForJWTResponseTypeDef:
        """
        Obtains an Workload access token for agentic workloads acting on behalf of user
        with JWT token.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_workload_access_token_for_jwt.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#get_workload_access_token_for_jwt)
        """

    def get_workload_access_token_for_user_id(
        self, **kwargs: Unpack[GetWorkloadAccessTokenForUserIdRequestTypeDef]
    ) -> GetWorkloadAccessTokenForUserIdResponseTypeDef:
        """
        Obtains an Workload access token for agentic workloads acting on behalf of user
        with User Id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_workload_access_token_for_user_id.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#get_workload_access_token_for_user_id)
        """

    def invoke_agent_runtime(
        self, **kwargs: Unpack[InvokeAgentRuntimeRequestTypeDef]
    ) -> InvokeAgentRuntimeResponseTypeDef:
        """
        Sends a request to an agent runtime in Amazon Bedrock and receives responses in
        real-time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/invoke_agent_runtime.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#invoke_agent_runtime)
        """

    def invoke_code_interpreter(
        self, **kwargs: Unpack[InvokeCodeInterpreterRequestTypeDef]
    ) -> InvokeCodeInterpreterResponseTypeDef:
        """
        Executes code within an active code interpreter session in Amazon Bedrock.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/invoke_code_interpreter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#invoke_code_interpreter)
        """

    def list_actors(self, **kwargs: Unpack[ListActorsInputTypeDef]) -> ListActorsOutputTypeDef:
        """
        Lists all actors in a memory store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/list_actors.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#list_actors)
        """

    def list_browser_sessions(
        self, **kwargs: Unpack[ListBrowserSessionsRequestTypeDef]
    ) -> ListBrowserSessionsResponseTypeDef:
        """
        Retrieves a list of browser sessions in Amazon Bedrock that match the specified
        criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/list_browser_sessions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#list_browser_sessions)
        """

    def list_code_interpreter_sessions(
        self, **kwargs: Unpack[ListCodeInterpreterSessionsRequestTypeDef]
    ) -> ListCodeInterpreterSessionsResponseTypeDef:
        """
        Retrieves a list of code interpreter sessions in Amazon Bedrock that match the
        specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/list_code_interpreter_sessions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#list_code_interpreter_sessions)
        """

    def list_events(self, **kwargs: Unpack[ListEventsInputTypeDef]) -> ListEventsOutputTypeDef:
        """
        Lists events in a memory store based on specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/list_events.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#list_events)
        """

    def list_memory_records(
        self, **kwargs: Unpack[ListMemoryRecordsInputTypeDef]
    ) -> ListMemoryRecordsOutputTypeDef:
        """
        Lists memory records in a memory store based on specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/list_memory_records.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#list_memory_records)
        """

    def list_sessions(
        self, **kwargs: Unpack[ListSessionsInputTypeDef]
    ) -> ListSessionsOutputTypeDef:
        """
        Lists sessions in a memory store based on specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/list_sessions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#list_sessions)
        """

    def retrieve_memory_records(
        self, **kwargs: Unpack[RetrieveMemoryRecordsInputTypeDef]
    ) -> RetrieveMemoryRecordsOutputTypeDef:
        """
        Searches for and retrieves memory records from a memory store based on
        specified search criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/retrieve_memory_records.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#retrieve_memory_records)
        """

    def start_browser_session(
        self, **kwargs: Unpack[StartBrowserSessionRequestTypeDef]
    ) -> StartBrowserSessionResponseTypeDef:
        """
        Creates and initializes a browser session in Amazon Bedrock.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/start_browser_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#start_browser_session)
        """

    def start_code_interpreter_session(
        self, **kwargs: Unpack[StartCodeInterpreterSessionRequestTypeDef]
    ) -> StartCodeInterpreterSessionResponseTypeDef:
        """
        Creates and initializes a code interpreter session in Amazon Bedrock.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/start_code_interpreter_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#start_code_interpreter_session)
        """

    def stop_browser_session(
        self, **kwargs: Unpack[StopBrowserSessionRequestTypeDef]
    ) -> StopBrowserSessionResponseTypeDef:
        """
        Terminates an active browser session in Amazon Bedrock.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/stop_browser_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#stop_browser_session)
        """

    def stop_code_interpreter_session(
        self, **kwargs: Unpack[StopCodeInterpreterSessionRequestTypeDef]
    ) -> StopCodeInterpreterSessionResponseTypeDef:
        """
        Terminates an active code interpreter session in Amazon Bedrock.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/stop_code_interpreter_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#stop_code_interpreter_session)
        """

    def update_browser_stream(
        self, **kwargs: Unpack[UpdateBrowserStreamRequestTypeDef]
    ) -> UpdateBrowserStreamResponseTypeDef:
        """
        Updates a browser stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/update_browser_stream.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#update_browser_stream)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_actors"]
    ) -> ListActorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_events"]
    ) -> ListEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_memory_records"]
    ) -> ListMemoryRecordsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_sessions"]
    ) -> ListSessionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["retrieve_memory_records"]
    ) -> RetrieveMemoryRecordsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/client/#get_paginator)
        """
