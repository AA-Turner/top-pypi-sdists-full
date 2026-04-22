"""
Type annotations for devops-agent service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_devops_agent.client import DevOpsAgentServiceClient

    session = get_session()
    async with session.create_client("devops-agent") as client:
        client: DevOpsAgentServiceClient
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

from .paginator import (
    ListAgentSpacesPaginator,
    ListAssociationsPaginator,
    ListBacklogTasksPaginator,
    ListExecutionsPaginator,
    ListGoalsPaginator,
    ListJournalRecordsPaginator,
    ListServicesPaginator,
)
from .type_defs import (
    AssociateServiceInputTypeDef,
    AssociateServiceOutputTypeDef,
    CreateAgentSpaceInputTypeDef,
    CreateAgentSpaceOutputTypeDef,
    CreateBacklogTaskRequestTypeDef,
    CreateBacklogTaskResponseTypeDef,
    CreateChatRequestTypeDef,
    CreateChatResponseTypeDef,
    CreatePrivateConnectionInputTypeDef,
    CreatePrivateConnectionOutputTypeDef,
    DeleteAgentSpaceInputTypeDef,
    DeletePrivateConnectionInputTypeDef,
    DeletePrivateConnectionOutputTypeDef,
    DeregisterServiceInputTypeDef,
    DescribePrivateConnectionInputTypeDef,
    DescribePrivateConnectionOutputTypeDef,
    DisableOperatorAppInputTypeDef,
    DisassociateServiceInputTypeDef,
    EmptyResponseMetadataTypeDef,
    EnableOperatorAppInputTypeDef,
    EnableOperatorAppOutputTypeDef,
    GetAccountUsageOutputTypeDef,
    GetAgentSpaceInputTypeDef,
    GetAgentSpaceOutputTypeDef,
    GetAssociationInputTypeDef,
    GetAssociationOutputTypeDef,
    GetBacklogTaskRequestTypeDef,
    GetBacklogTaskResponseTypeDef,
    GetOperatorAppInputTypeDef,
    GetOperatorAppOutputTypeDef,
    GetRecommendationRequestTypeDef,
    GetRecommendationResponseTypeDef,
    GetServiceInputTypeDef,
    GetServiceOutputTypeDef,
    ListAgentSpacesInputTypeDef,
    ListAgentSpacesOutputTypeDef,
    ListAssociationsInputTypeDef,
    ListAssociationsOutputTypeDef,
    ListBacklogTasksRequestTypeDef,
    ListBacklogTasksResponseTypeDef,
    ListChatsRequestTypeDef,
    ListChatsResponseTypeDef,
    ListExecutionsRequestTypeDef,
    ListExecutionsResponseTypeDef,
    ListGoalsRequestTypeDef,
    ListGoalsResponseTypeDef,
    ListJournalRecordsRequestTypeDef,
    ListJournalRecordsResponseTypeDef,
    ListPendingMessagesRequestTypeDef,
    ListPendingMessagesResponseTypeDef,
    ListPrivateConnectionsOutputTypeDef,
    ListRecommendationsRequestTypeDef,
    ListRecommendationsResponseTypeDef,
    ListServicesInputTypeDef,
    ListServicesOutputTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWebhooksInputTypeDef,
    ListWebhooksOutputTypeDef,
    RegisterServiceInputTypeDef,
    RegisterServiceOutputTypeDef,
    SendMessageRequestTypeDef,
    SendMessageResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateAgentSpaceInputTypeDef,
    UpdateAgentSpaceOutputTypeDef,
    UpdateAssociationInputTypeDef,
    UpdateAssociationOutputTypeDef,
    UpdateBacklogTaskRequestTypeDef,
    UpdateBacklogTaskResponseTypeDef,
    UpdateGoalRequestTypeDef,
    UpdateGoalResponseTypeDef,
    UpdateOperatorAppIdpConfigInputTypeDef,
    UpdateOperatorAppIdpConfigOutputTypeDef,
    UpdatePrivateConnectionCertificateInputTypeDef,
    UpdatePrivateConnectionCertificateOutputTypeDef,
    UpdateRecommendationRequestTypeDef,
    UpdateRecommendationResponseTypeDef,
    ValidateAwsAssociationsInputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("DevOpsAgentServiceClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    ContentSizeExceededException: type[BotocoreClientError]
    IdentityCenterServiceException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    InvalidParameterException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class DevOpsAgentServiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent.html#DevOpsAgentService.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DevOpsAgentServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent.html#DevOpsAgentService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#generate_presigned_url)
        """

    async def associate_service(
        self, **kwargs: Unpack[AssociateServiceInputTypeDef]
    ) -> AssociateServiceOutputTypeDef:
        """
        Adds a specific service association to an AgentSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/associate_service.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#associate_service)
        """

    async def create_agent_space(
        self, **kwargs: Unpack[CreateAgentSpaceInputTypeDef]
    ) -> CreateAgentSpaceOutputTypeDef:
        """
        Creates a new AgentSpace with the specified name and description.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/create_agent_space.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#create_agent_space)
        """

    async def create_backlog_task(
        self, **kwargs: Unpack[CreateBacklogTaskRequestTypeDef]
    ) -> CreateBacklogTaskResponseTypeDef:
        """
        Creates a new backlog task in the specified agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/create_backlog_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#create_backlog_task)
        """

    async def create_chat(
        self, **kwargs: Unpack[CreateChatRequestTypeDef]
    ) -> CreateChatResponseTypeDef:
        """
        Creates a new chat execution in the specified agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/create_chat.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#create_chat)
        """

    async def create_private_connection(
        self, **kwargs: Unpack[CreatePrivateConnectionInputTypeDef]
    ) -> CreatePrivateConnectionOutputTypeDef:
        """
        Creates a Private Connection to a target resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/create_private_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#create_private_connection)
        """

    async def delete_agent_space(
        self, **kwargs: Unpack[DeleteAgentSpaceInputTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes an AgentSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/delete_agent_space.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#delete_agent_space)
        """

    async def delete_private_connection(
        self, **kwargs: Unpack[DeletePrivateConnectionInputTypeDef]
    ) -> DeletePrivateConnectionOutputTypeDef:
        """
        Deletes a Private Connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/delete_private_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#delete_private_connection)
        """

    async def deregister_service(
        self, **kwargs: Unpack[DeregisterServiceInputTypeDef]
    ) -> dict[str, Any]:
        """
        Deregister a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/deregister_service.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#deregister_service)
        """

    async def describe_private_connection(
        self, **kwargs: Unpack[DescribePrivateConnectionInputTypeDef]
    ) -> DescribePrivateConnectionOutputTypeDef:
        """
        Retrieves details of an existing Private Connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/describe_private_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#describe_private_connection)
        """

    async def disable_operator_app(
        self, **kwargs: Unpack[DisableOperatorAppInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disable the Operator App for the specified AgentSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/disable_operator_app.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#disable_operator_app)
        """

    async def disassociate_service(
        self, **kwargs: Unpack[DisassociateServiceInputTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes a specific service association from an AgentSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/disassociate_service.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#disassociate_service)
        """

    async def enable_operator_app(
        self, **kwargs: Unpack[EnableOperatorAppInputTypeDef]
    ) -> EnableOperatorAppOutputTypeDef:
        """
        Enable the Operator App to access the given AgentSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/enable_operator_app.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#enable_operator_app)
        """

    async def get_account_usage(self) -> GetAccountUsageOutputTypeDef:
        """
        Retrieves monthly account usage metrics and limits for the AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/get_account_usage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#get_account_usage)
        """

    async def get_agent_space(
        self, **kwargs: Unpack[GetAgentSpaceInputTypeDef]
    ) -> GetAgentSpaceOutputTypeDef:
        """
        Retrieves detailed information about a specific AgentSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/get_agent_space.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#get_agent_space)
        """

    async def get_association(
        self, **kwargs: Unpack[GetAssociationInputTypeDef]
    ) -> GetAssociationOutputTypeDef:
        """
        Retrieves given associations configured for a specific AgentSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/get_association.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#get_association)
        """

    async def get_backlog_task(
        self, **kwargs: Unpack[GetBacklogTaskRequestTypeDef]
    ) -> GetBacklogTaskResponseTypeDef:
        """
        Gets a backlog task for the specified agent space and task id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/get_backlog_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#get_backlog_task)
        """

    async def get_operator_app(
        self, **kwargs: Unpack[GetOperatorAppInputTypeDef]
    ) -> GetOperatorAppOutputTypeDef:
        """
        Get the full auth configuration of operator including any enabled auth flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/get_operator_app.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#get_operator_app)
        """

    async def get_recommendation(
        self, **kwargs: Unpack[GetRecommendationRequestTypeDef]
    ) -> GetRecommendationResponseTypeDef:
        """
        Retrieves a specific recommendation by its ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/get_recommendation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#get_recommendation)
        """

    async def get_service(
        self, **kwargs: Unpack[GetServiceInputTypeDef]
    ) -> GetServiceOutputTypeDef:
        """
        Retrieves given service by it's unique identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/get_service.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#get_service)
        """

    async def list_agent_spaces(
        self, **kwargs: Unpack[ListAgentSpacesInputTypeDef]
    ) -> ListAgentSpacesOutputTypeDef:
        """
        Lists all AgentSpaces with optional pagination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/list_agent_spaces.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#list_agent_spaces)
        """

    async def list_associations(
        self, **kwargs: Unpack[ListAssociationsInputTypeDef]
    ) -> ListAssociationsOutputTypeDef:
        """
        List all associations for given AgentSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/list_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#list_associations)
        """

    async def list_backlog_tasks(
        self, **kwargs: Unpack[ListBacklogTasksRequestTypeDef]
    ) -> ListBacklogTasksResponseTypeDef:
        """
        Lists backlog tasks in the specified agent space with optional filtering and
        sorting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/list_backlog_tasks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#list_backlog_tasks)
        """

    async def list_chats(
        self, **kwargs: Unpack[ListChatsRequestTypeDef]
    ) -> ListChatsResponseTypeDef:
        """
        Retrieves a paginated list of the user's recent chat executions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/list_chats.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#list_chats)
        """

    async def list_executions(
        self, **kwargs: Unpack[ListExecutionsRequestTypeDef]
    ) -> ListExecutionsResponseTypeDef:
        """
        List executions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/list_executions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#list_executions)
        """

    async def list_goals(
        self, **kwargs: Unpack[ListGoalsRequestTypeDef]
    ) -> ListGoalsResponseTypeDef:
        """
        Lists goals in the specified agent space with optional filtering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/list_goals.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#list_goals)
        """

    async def list_journal_records(
        self, **kwargs: Unpack[ListJournalRecordsRequestTypeDef]
    ) -> ListJournalRecordsResponseTypeDef:
        """
        List journal records for a specific execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/list_journal_records.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#list_journal_records)
        """

    async def list_pending_messages(
        self, **kwargs: Unpack[ListPendingMessagesRequestTypeDef]
    ) -> ListPendingMessagesResponseTypeDef:
        """
        List pending messages for a specific execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/list_pending_messages.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#list_pending_messages)
        """

    async def list_private_connections(self) -> ListPrivateConnectionsOutputTypeDef:
        """
        Lists all Private Connections in the caller's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/list_private_connections.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#list_private_connections)
        """

    async def list_recommendations(
        self, **kwargs: Unpack[ListRecommendationsRequestTypeDef]
    ) -> ListRecommendationsResponseTypeDef:
        """
        Lists recommendations for the specified agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/list_recommendations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#list_recommendations)
        """

    async def list_services(
        self, **kwargs: Unpack[ListServicesInputTypeDef]
    ) -> ListServicesOutputTypeDef:
        """
        List a list of registered service on the account level.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/list_services.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#list_services)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists tags for the specified AWS DevOps Agent resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#list_tags_for_resource)
        """

    async def list_webhooks(
        self, **kwargs: Unpack[ListWebhooksInputTypeDef]
    ) -> ListWebhooksOutputTypeDef:
        """
        List all webhooks for given Association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/list_webhooks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#list_webhooks)
        """

    async def register_service(
        self, **kwargs: Unpack[RegisterServiceInputTypeDef]
    ) -> RegisterServiceOutputTypeDef:
        """
        This operation registers the specified service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/register_service.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#register_service)
        """

    async def send_message(
        self, **kwargs: Unpack[SendMessageRequestTypeDef]
    ) -> SendMessageResponseTypeDef:
        """
        Sends a chat message and streams the response for the specified agent space
        execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/send_message.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#send_message)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Adds or overwrites tags for the specified AWS DevOps Agent resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Removes tags from the specified AWS DevOps Agent resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#untag_resource)
        """

    async def update_agent_space(
        self, **kwargs: Unpack[UpdateAgentSpaceInputTypeDef]
    ) -> UpdateAgentSpaceOutputTypeDef:
        """
        Updates the information of an existing AgentSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/update_agent_space.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#update_agent_space)
        """

    async def update_association(
        self, **kwargs: Unpack[UpdateAssociationInputTypeDef]
    ) -> UpdateAssociationOutputTypeDef:
        """
        Partially updates the configuration of an existing service association for an
        AgentSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/update_association.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#update_association)
        """

    async def update_backlog_task(
        self, **kwargs: Unpack[UpdateBacklogTaskRequestTypeDef]
    ) -> UpdateBacklogTaskResponseTypeDef:
        """
        Update an existing backlog task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/update_backlog_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#update_backlog_task)
        """

    async def update_goal(
        self, **kwargs: Unpack[UpdateGoalRequestTypeDef]
    ) -> UpdateGoalResponseTypeDef:
        """
        Update an existing goal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/update_goal.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#update_goal)
        """

    async def update_operator_app_idp_config(
        self, **kwargs: Unpack[UpdateOperatorAppIdpConfigInputTypeDef]
    ) -> UpdateOperatorAppIdpConfigOutputTypeDef:
        """
        Update the external Identity Provider configuration for the Operator App.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/update_operator_app_idp_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#update_operator_app_idp_config)
        """

    async def update_private_connection_certificate(
        self, **kwargs: Unpack[UpdatePrivateConnectionCertificateInputTypeDef]
    ) -> UpdatePrivateConnectionCertificateOutputTypeDef:
        """
        Updates the certificate associated with a Private Connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/update_private_connection_certificate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#update_private_connection_certificate)
        """

    async def update_recommendation(
        self, **kwargs: Unpack[UpdateRecommendationRequestTypeDef]
    ) -> UpdateRecommendationResponseTypeDef:
        """
        Updates an existing recommendation with new content, status, or metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/update_recommendation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#update_recommendation)
        """

    async def validate_aws_associations(
        self, **kwargs: Unpack[ValidateAwsAssociationsInputTypeDef]
    ) -> dict[str, Any]:
        """
        Validates an aws association and set status and returns a 204 No Content
        response on success.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/validate_aws_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#validate_aws_associations)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_agent_spaces"]
    ) -> ListAgentSpacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_associations"]
    ) -> ListAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_backlog_tasks"]
    ) -> ListBacklogTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_executions"]
    ) -> ListExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_goals"]
    ) -> ListGoalsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_journal_records"]
    ) -> ListJournalRecordsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_services"]
    ) -> ListServicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent.html#DevOpsAgentService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent.html#DevOpsAgentService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/client/)
        """
