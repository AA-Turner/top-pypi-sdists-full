"""
Type annotations for bedrock-agent service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_bedrock_agent.client import AgentsforBedrockClient
    from types_aiobotocore_bedrock_agent.paginator import (
        ListAgentActionGroupsPaginator,
        ListAgentAliasesPaginator,
        ListAgentCollaboratorsPaginator,
        ListAgentKnowledgeBasesPaginator,
        ListAgentVersionsPaginator,
        ListAgentsPaginator,
        ListDataSourcesPaginator,
        ListFlowAliasesPaginator,
        ListFlowVersionsPaginator,
        ListFlowsPaginator,
        ListIngestionJobsPaginator,
        ListKnowledgeBaseDocumentsPaginator,
        ListKnowledgeBasesPaginator,
        ListPromptsPaginator,
    )

    session = get_session()
    with session.create_client("bedrock-agent") as client:
        client: AgentsforBedrockClient

        list_agent_action_groups_paginator: ListAgentActionGroupsPaginator = client.get_paginator("list_agent_action_groups")
        list_agent_aliases_paginator: ListAgentAliasesPaginator = client.get_paginator("list_agent_aliases")
        list_agent_collaborators_paginator: ListAgentCollaboratorsPaginator = client.get_paginator("list_agent_collaborators")
        list_agent_knowledge_bases_paginator: ListAgentKnowledgeBasesPaginator = client.get_paginator("list_agent_knowledge_bases")
        list_agent_versions_paginator: ListAgentVersionsPaginator = client.get_paginator("list_agent_versions")
        list_agents_paginator: ListAgentsPaginator = client.get_paginator("list_agents")
        list_data_sources_paginator: ListDataSourcesPaginator = client.get_paginator("list_data_sources")
        list_flow_aliases_paginator: ListFlowAliasesPaginator = client.get_paginator("list_flow_aliases")
        list_flow_versions_paginator: ListFlowVersionsPaginator = client.get_paginator("list_flow_versions")
        list_flows_paginator: ListFlowsPaginator = client.get_paginator("list_flows")
        list_ingestion_jobs_paginator: ListIngestionJobsPaginator = client.get_paginator("list_ingestion_jobs")
        list_knowledge_base_documents_paginator: ListKnowledgeBaseDocumentsPaginator = client.get_paginator("list_knowledge_base_documents")
        list_knowledge_bases_paginator: ListKnowledgeBasesPaginator = client.get_paginator("list_knowledge_bases")
        list_prompts_paginator: ListPromptsPaginator = client.get_paginator("list_prompts")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAgentActionGroupsRequestPaginateTypeDef,
    ListAgentActionGroupsResponseTypeDef,
    ListAgentAliasesRequestPaginateTypeDef,
    ListAgentAliasesResponseTypeDef,
    ListAgentCollaboratorsRequestPaginateTypeDef,
    ListAgentCollaboratorsResponseTypeDef,
    ListAgentKnowledgeBasesRequestPaginateTypeDef,
    ListAgentKnowledgeBasesResponseTypeDef,
    ListAgentsRequestPaginateTypeDef,
    ListAgentsResponseTypeDef,
    ListAgentVersionsRequestPaginateTypeDef,
    ListAgentVersionsResponseTypeDef,
    ListDataSourcesRequestPaginateTypeDef,
    ListDataSourcesResponseTypeDef,
    ListFlowAliasesRequestPaginateTypeDef,
    ListFlowAliasesResponseTypeDef,
    ListFlowsRequestPaginateTypeDef,
    ListFlowsResponseTypeDef,
    ListFlowVersionsRequestPaginateTypeDef,
    ListFlowVersionsResponseTypeDef,
    ListIngestionJobsRequestPaginateTypeDef,
    ListIngestionJobsResponseTypeDef,
    ListKnowledgeBaseDocumentsRequestPaginateTypeDef,
    ListKnowledgeBaseDocumentsResponseTypeDef,
    ListKnowledgeBasesRequestPaginateTypeDef,
    ListKnowledgeBasesResponseTypeDef,
    ListPromptsRequestPaginateTypeDef,
    ListPromptsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAgentActionGroupsPaginator",
    "ListAgentAliasesPaginator",
    "ListAgentCollaboratorsPaginator",
    "ListAgentKnowledgeBasesPaginator",
    "ListAgentVersionsPaginator",
    "ListAgentsPaginator",
    "ListDataSourcesPaginator",
    "ListFlowAliasesPaginator",
    "ListFlowVersionsPaginator",
    "ListFlowsPaginator",
    "ListIngestionJobsPaginator",
    "ListKnowledgeBaseDocumentsPaginator",
    "ListKnowledgeBasesPaginator",
    "ListPromptsPaginator",
)

if TYPE_CHECKING:
    _ListAgentActionGroupsPaginatorBase = AioPaginator[ListAgentActionGroupsResponseTypeDef]
else:
    _ListAgentActionGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAgentActionGroupsPaginator(_ListAgentActionGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgentActionGroups.html#AgentsforBedrock.Paginator.ListAgentActionGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listagentactiongroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentActionGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAgentActionGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgentActionGroups.html#AgentsforBedrock.Paginator.ListAgentActionGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listagentactiongroupspaginator)
        """

if TYPE_CHECKING:
    _ListAgentAliasesPaginatorBase = AioPaginator[ListAgentAliasesResponseTypeDef]
else:
    _ListAgentAliasesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAgentAliasesPaginator(_ListAgentAliasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgentAliases.html#AgentsforBedrock.Paginator.ListAgentAliases)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listagentaliasespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentAliasesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAgentAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgentAliases.html#AgentsforBedrock.Paginator.ListAgentAliases.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listagentaliasespaginator)
        """

if TYPE_CHECKING:
    _ListAgentCollaboratorsPaginatorBase = AioPaginator[ListAgentCollaboratorsResponseTypeDef]
else:
    _ListAgentCollaboratorsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAgentCollaboratorsPaginator(_ListAgentCollaboratorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgentCollaborators.html#AgentsforBedrock.Paginator.ListAgentCollaborators)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listagentcollaboratorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentCollaboratorsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAgentCollaboratorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgentCollaborators.html#AgentsforBedrock.Paginator.ListAgentCollaborators.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listagentcollaboratorspaginator)
        """

if TYPE_CHECKING:
    _ListAgentKnowledgeBasesPaginatorBase = AioPaginator[ListAgentKnowledgeBasesResponseTypeDef]
else:
    _ListAgentKnowledgeBasesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAgentKnowledgeBasesPaginator(_ListAgentKnowledgeBasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgentKnowledgeBases.html#AgentsforBedrock.Paginator.ListAgentKnowledgeBases)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listagentknowledgebasespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentKnowledgeBasesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAgentKnowledgeBasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgentKnowledgeBases.html#AgentsforBedrock.Paginator.ListAgentKnowledgeBases.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listagentknowledgebasespaginator)
        """

if TYPE_CHECKING:
    _ListAgentVersionsPaginatorBase = AioPaginator[ListAgentVersionsResponseTypeDef]
else:
    _ListAgentVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAgentVersionsPaginator(_ListAgentVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgentVersions.html#AgentsforBedrock.Paginator.ListAgentVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listagentversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAgentVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgentVersions.html#AgentsforBedrock.Paginator.ListAgentVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listagentversionspaginator)
        """

if TYPE_CHECKING:
    _ListAgentsPaginatorBase = AioPaginator[ListAgentsResponseTypeDef]
else:
    _ListAgentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAgentsPaginator(_ListAgentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgents.html#AgentsforBedrock.Paginator.ListAgents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listagentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAgentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgents.html#AgentsforBedrock.Paginator.ListAgents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listagentspaginator)
        """

if TYPE_CHECKING:
    _ListDataSourcesPaginatorBase = AioPaginator[ListDataSourcesResponseTypeDef]
else:
    _ListDataSourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataSourcesPaginator(_ListDataSourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListDataSources.html#AgentsforBedrock.Paginator.ListDataSources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listdatasourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataSourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListDataSources.html#AgentsforBedrock.Paginator.ListDataSources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listdatasourcespaginator)
        """

if TYPE_CHECKING:
    _ListFlowAliasesPaginatorBase = AioPaginator[ListFlowAliasesResponseTypeDef]
else:
    _ListFlowAliasesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFlowAliasesPaginator(_ListFlowAliasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListFlowAliases.html#AgentsforBedrock.Paginator.ListFlowAliases)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listflowaliasespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFlowAliasesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFlowAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListFlowAliases.html#AgentsforBedrock.Paginator.ListFlowAliases.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listflowaliasespaginator)
        """

if TYPE_CHECKING:
    _ListFlowVersionsPaginatorBase = AioPaginator[ListFlowVersionsResponseTypeDef]
else:
    _ListFlowVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFlowVersionsPaginator(_ListFlowVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListFlowVersions.html#AgentsforBedrock.Paginator.ListFlowVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listflowversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFlowVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFlowVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListFlowVersions.html#AgentsforBedrock.Paginator.ListFlowVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listflowversionspaginator)
        """

if TYPE_CHECKING:
    _ListFlowsPaginatorBase = AioPaginator[ListFlowsResponseTypeDef]
else:
    _ListFlowsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFlowsPaginator(_ListFlowsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListFlows.html#AgentsforBedrock.Paginator.ListFlows)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listflowspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFlowsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFlowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListFlows.html#AgentsforBedrock.Paginator.ListFlows.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listflowspaginator)
        """

if TYPE_CHECKING:
    _ListIngestionJobsPaginatorBase = AioPaginator[ListIngestionJobsResponseTypeDef]
else:
    _ListIngestionJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListIngestionJobsPaginator(_ListIngestionJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListIngestionJobs.html#AgentsforBedrock.Paginator.ListIngestionJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listingestionjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIngestionJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListIngestionJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListIngestionJobs.html#AgentsforBedrock.Paginator.ListIngestionJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listingestionjobspaginator)
        """

if TYPE_CHECKING:
    _ListKnowledgeBaseDocumentsPaginatorBase = AioPaginator[
        ListKnowledgeBaseDocumentsResponseTypeDef
    ]
else:
    _ListKnowledgeBaseDocumentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListKnowledgeBaseDocumentsPaginator(_ListKnowledgeBaseDocumentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListKnowledgeBaseDocuments.html#AgentsforBedrock.Paginator.ListKnowledgeBaseDocuments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listknowledgebasedocumentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListKnowledgeBaseDocumentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListKnowledgeBaseDocumentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListKnowledgeBaseDocuments.html#AgentsforBedrock.Paginator.ListKnowledgeBaseDocuments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listknowledgebasedocumentspaginator)
        """

if TYPE_CHECKING:
    _ListKnowledgeBasesPaginatorBase = AioPaginator[ListKnowledgeBasesResponseTypeDef]
else:
    _ListKnowledgeBasesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListKnowledgeBasesPaginator(_ListKnowledgeBasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListKnowledgeBases.html#AgentsforBedrock.Paginator.ListKnowledgeBases)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listknowledgebasespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListKnowledgeBasesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListKnowledgeBasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListKnowledgeBases.html#AgentsforBedrock.Paginator.ListKnowledgeBases.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listknowledgebasespaginator)
        """

if TYPE_CHECKING:
    _ListPromptsPaginatorBase = AioPaginator[ListPromptsResponseTypeDef]
else:
    _ListPromptsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPromptsPaginator(_ListPromptsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListPrompts.html#AgentsforBedrock.Paginator.ListPrompts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listpromptspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPromptsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPromptsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListPrompts.html#AgentsforBedrock.Paginator.ListPrompts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listpromptspaginator)
        """
