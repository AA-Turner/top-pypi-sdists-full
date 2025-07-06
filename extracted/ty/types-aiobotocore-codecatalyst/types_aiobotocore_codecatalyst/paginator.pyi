"""
Type annotations for codecatalyst service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_codecatalyst.client import CodeCatalystClient
    from types_aiobotocore_codecatalyst.paginator import (
        ListAccessTokensPaginator,
        ListDevEnvironmentSessionsPaginator,
        ListDevEnvironmentsPaginator,
        ListEventLogsPaginator,
        ListProjectsPaginator,
        ListSourceRepositoriesPaginator,
        ListSourceRepositoryBranchesPaginator,
        ListSpacesPaginator,
        ListWorkflowRunsPaginator,
        ListWorkflowsPaginator,
    )

    session = get_session()
    with session.create_client("codecatalyst") as client:
        client: CodeCatalystClient

        list_access_tokens_paginator: ListAccessTokensPaginator = client.get_paginator("list_access_tokens")
        list_dev_environment_sessions_paginator: ListDevEnvironmentSessionsPaginator = client.get_paginator("list_dev_environment_sessions")
        list_dev_environments_paginator: ListDevEnvironmentsPaginator = client.get_paginator("list_dev_environments")
        list_event_logs_paginator: ListEventLogsPaginator = client.get_paginator("list_event_logs")
        list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
        list_source_repositories_paginator: ListSourceRepositoriesPaginator = client.get_paginator("list_source_repositories")
        list_source_repository_branches_paginator: ListSourceRepositoryBranchesPaginator = client.get_paginator("list_source_repository_branches")
        list_spaces_paginator: ListSpacesPaginator = client.get_paginator("list_spaces")
        list_workflow_runs_paginator: ListWorkflowRunsPaginator = client.get_paginator("list_workflow_runs")
        list_workflows_paginator: ListWorkflowsPaginator = client.get_paginator("list_workflows")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAccessTokensRequestPaginateTypeDef,
    ListAccessTokensResponseTypeDef,
    ListDevEnvironmentSessionsRequestPaginateTypeDef,
    ListDevEnvironmentSessionsResponseTypeDef,
    ListDevEnvironmentsRequestPaginateTypeDef,
    ListDevEnvironmentsResponseTypeDef,
    ListEventLogsRequestPaginateTypeDef,
    ListEventLogsResponseTypeDef,
    ListProjectsRequestPaginateTypeDef,
    ListProjectsResponseTypeDef,
    ListSourceRepositoriesRequestPaginateTypeDef,
    ListSourceRepositoriesResponseTypeDef,
    ListSourceRepositoryBranchesRequestPaginateTypeDef,
    ListSourceRepositoryBranchesResponseTypeDef,
    ListSpacesRequestPaginateTypeDef,
    ListSpacesResponseTypeDef,
    ListWorkflowRunsRequestPaginateTypeDef,
    ListWorkflowRunsResponseTypeDef,
    ListWorkflowsRequestPaginateTypeDef,
    ListWorkflowsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAccessTokensPaginator",
    "ListDevEnvironmentSessionsPaginator",
    "ListDevEnvironmentsPaginator",
    "ListEventLogsPaginator",
    "ListProjectsPaginator",
    "ListSourceRepositoriesPaginator",
    "ListSourceRepositoryBranchesPaginator",
    "ListSpacesPaginator",
    "ListWorkflowRunsPaginator",
    "ListWorkflowsPaginator",
)

if TYPE_CHECKING:
    _ListAccessTokensPaginatorBase = AioPaginator[ListAccessTokensResponseTypeDef]
else:
    _ListAccessTokensPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAccessTokensPaginator(_ListAccessTokensPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListAccessTokens.html#CodeCatalyst.Paginator.ListAccessTokens)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listaccesstokenspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccessTokensRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAccessTokensResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListAccessTokens.html#CodeCatalyst.Paginator.ListAccessTokens.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listaccesstokenspaginator)
        """

if TYPE_CHECKING:
    _ListDevEnvironmentSessionsPaginatorBase = AioPaginator[
        ListDevEnvironmentSessionsResponseTypeDef
    ]
else:
    _ListDevEnvironmentSessionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDevEnvironmentSessionsPaginator(_ListDevEnvironmentSessionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListDevEnvironmentSessions.html#CodeCatalyst.Paginator.ListDevEnvironmentSessions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listdevenvironmentsessionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDevEnvironmentSessionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDevEnvironmentSessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListDevEnvironmentSessions.html#CodeCatalyst.Paginator.ListDevEnvironmentSessions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listdevenvironmentsessionspaginator)
        """

if TYPE_CHECKING:
    _ListDevEnvironmentsPaginatorBase = AioPaginator[ListDevEnvironmentsResponseTypeDef]
else:
    _ListDevEnvironmentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDevEnvironmentsPaginator(_ListDevEnvironmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListDevEnvironments.html#CodeCatalyst.Paginator.ListDevEnvironments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listdevenvironmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDevEnvironmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDevEnvironmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListDevEnvironments.html#CodeCatalyst.Paginator.ListDevEnvironments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listdevenvironmentspaginator)
        """

if TYPE_CHECKING:
    _ListEventLogsPaginatorBase = AioPaginator[ListEventLogsResponseTypeDef]
else:
    _ListEventLogsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEventLogsPaginator(_ListEventLogsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListEventLogs.html#CodeCatalyst.Paginator.ListEventLogs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listeventlogspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEventLogsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEventLogsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListEventLogs.html#CodeCatalyst.Paginator.ListEventLogs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listeventlogspaginator)
        """

if TYPE_CHECKING:
    _ListProjectsPaginatorBase = AioPaginator[ListProjectsResponseTypeDef]
else:
    _ListProjectsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListProjectsPaginator(_ListProjectsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListProjects.html#CodeCatalyst.Paginator.ListProjects)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listprojectspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProjectsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListProjects.html#CodeCatalyst.Paginator.ListProjects.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listprojectspaginator)
        """

if TYPE_CHECKING:
    _ListSourceRepositoriesPaginatorBase = AioPaginator[ListSourceRepositoriesResponseTypeDef]
else:
    _ListSourceRepositoriesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSourceRepositoriesPaginator(_ListSourceRepositoriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListSourceRepositories.html#CodeCatalyst.Paginator.ListSourceRepositories)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listsourcerepositoriespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSourceRepositoriesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSourceRepositoriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListSourceRepositories.html#CodeCatalyst.Paginator.ListSourceRepositories.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listsourcerepositoriespaginator)
        """

if TYPE_CHECKING:
    _ListSourceRepositoryBranchesPaginatorBase = AioPaginator[
        ListSourceRepositoryBranchesResponseTypeDef
    ]
else:
    _ListSourceRepositoryBranchesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSourceRepositoryBranchesPaginator(_ListSourceRepositoryBranchesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListSourceRepositoryBranches.html#CodeCatalyst.Paginator.ListSourceRepositoryBranches)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listsourcerepositorybranchespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSourceRepositoryBranchesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSourceRepositoryBranchesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListSourceRepositoryBranches.html#CodeCatalyst.Paginator.ListSourceRepositoryBranches.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listsourcerepositorybranchespaginator)
        """

if TYPE_CHECKING:
    _ListSpacesPaginatorBase = AioPaginator[ListSpacesResponseTypeDef]
else:
    _ListSpacesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSpacesPaginator(_ListSpacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListSpaces.html#CodeCatalyst.Paginator.ListSpaces)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listspacespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSpacesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSpacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListSpaces.html#CodeCatalyst.Paginator.ListSpaces.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listspacespaginator)
        """

if TYPE_CHECKING:
    _ListWorkflowRunsPaginatorBase = AioPaginator[ListWorkflowRunsResponseTypeDef]
else:
    _ListWorkflowRunsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListWorkflowRunsPaginator(_ListWorkflowRunsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListWorkflowRuns.html#CodeCatalyst.Paginator.ListWorkflowRuns)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listworkflowrunspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkflowRunsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkflowRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListWorkflowRuns.html#CodeCatalyst.Paginator.ListWorkflowRuns.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listworkflowrunspaginator)
        """

if TYPE_CHECKING:
    _ListWorkflowsPaginatorBase = AioPaginator[ListWorkflowsResponseTypeDef]
else:
    _ListWorkflowsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListWorkflowsPaginator(_ListWorkflowsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListWorkflows.html#CodeCatalyst.Paginator.ListWorkflows)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listworkflowspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkflowsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkflowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/paginator/ListWorkflows.html#CodeCatalyst.Paginator.ListWorkflows.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecatalyst/paginators/#listworkflowspaginator)
        """
