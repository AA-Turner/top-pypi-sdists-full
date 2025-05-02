"""
Type annotations for mgh service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mgh.client import MigrationHubClient
    from types_aiobotocore_mgh.paginator import (
        ListApplicationStatesPaginator,
        ListCreatedArtifactsPaginator,
        ListDiscoveredResourcesPaginator,
        ListMigrationTaskUpdatesPaginator,
        ListMigrationTasksPaginator,
        ListProgressUpdateStreamsPaginator,
        ListSourceResourcesPaginator,
    )

    session = get_session()
    with session.create_client("mgh") as client:
        client: MigrationHubClient

        list_application_states_paginator: ListApplicationStatesPaginator = client.get_paginator("list_application_states")
        list_created_artifacts_paginator: ListCreatedArtifactsPaginator = client.get_paginator("list_created_artifacts")
        list_discovered_resources_paginator: ListDiscoveredResourcesPaginator = client.get_paginator("list_discovered_resources")
        list_migration_task_updates_paginator: ListMigrationTaskUpdatesPaginator = client.get_paginator("list_migration_task_updates")
        list_migration_tasks_paginator: ListMigrationTasksPaginator = client.get_paginator("list_migration_tasks")
        list_progress_update_streams_paginator: ListProgressUpdateStreamsPaginator = client.get_paginator("list_progress_update_streams")
        list_source_resources_paginator: ListSourceResourcesPaginator = client.get_paginator("list_source_resources")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListApplicationStatesRequestPaginateTypeDef,
    ListApplicationStatesResultTypeDef,
    ListCreatedArtifactsRequestPaginateTypeDef,
    ListCreatedArtifactsResultTypeDef,
    ListDiscoveredResourcesRequestPaginateTypeDef,
    ListDiscoveredResourcesResultTypeDef,
    ListMigrationTasksRequestPaginateTypeDef,
    ListMigrationTasksResultTypeDef,
    ListMigrationTaskUpdatesRequestPaginateTypeDef,
    ListMigrationTaskUpdatesResultTypeDef,
    ListProgressUpdateStreamsRequestPaginateTypeDef,
    ListProgressUpdateStreamsResultTypeDef,
    ListSourceResourcesRequestPaginateTypeDef,
    ListSourceResourcesResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListApplicationStatesPaginator",
    "ListCreatedArtifactsPaginator",
    "ListDiscoveredResourcesPaginator",
    "ListMigrationTaskUpdatesPaginator",
    "ListMigrationTasksPaginator",
    "ListProgressUpdateStreamsPaginator",
    "ListSourceResourcesPaginator",
)

if TYPE_CHECKING:
    _ListApplicationStatesPaginatorBase = AioPaginator[ListApplicationStatesResultTypeDef]
else:
    _ListApplicationStatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListApplicationStatesPaginator(_ListApplicationStatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListApplicationStates.html#MigrationHub.Paginator.ListApplicationStates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listapplicationstatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationStatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListApplicationStatesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListApplicationStates.html#MigrationHub.Paginator.ListApplicationStates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listapplicationstatespaginator)
        """

if TYPE_CHECKING:
    _ListCreatedArtifactsPaginatorBase = AioPaginator[ListCreatedArtifactsResultTypeDef]
else:
    _ListCreatedArtifactsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCreatedArtifactsPaginator(_ListCreatedArtifactsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListCreatedArtifacts.html#MigrationHub.Paginator.ListCreatedArtifacts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listcreatedartifactspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCreatedArtifactsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCreatedArtifactsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListCreatedArtifacts.html#MigrationHub.Paginator.ListCreatedArtifacts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listcreatedartifactspaginator)
        """

if TYPE_CHECKING:
    _ListDiscoveredResourcesPaginatorBase = AioPaginator[ListDiscoveredResourcesResultTypeDef]
else:
    _ListDiscoveredResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDiscoveredResourcesPaginator(_ListDiscoveredResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListDiscoveredResources.html#MigrationHub.Paginator.ListDiscoveredResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listdiscoveredresourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDiscoveredResourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDiscoveredResourcesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListDiscoveredResources.html#MigrationHub.Paginator.ListDiscoveredResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listdiscoveredresourcespaginator)
        """

if TYPE_CHECKING:
    _ListMigrationTaskUpdatesPaginatorBase = AioPaginator[ListMigrationTaskUpdatesResultTypeDef]
else:
    _ListMigrationTaskUpdatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMigrationTaskUpdatesPaginator(_ListMigrationTaskUpdatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListMigrationTaskUpdates.html#MigrationHub.Paginator.ListMigrationTaskUpdates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listmigrationtaskupdatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMigrationTaskUpdatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMigrationTaskUpdatesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListMigrationTaskUpdates.html#MigrationHub.Paginator.ListMigrationTaskUpdates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listmigrationtaskupdatespaginator)
        """

if TYPE_CHECKING:
    _ListMigrationTasksPaginatorBase = AioPaginator[ListMigrationTasksResultTypeDef]
else:
    _ListMigrationTasksPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMigrationTasksPaginator(_ListMigrationTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListMigrationTasks.html#MigrationHub.Paginator.ListMigrationTasks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listmigrationtaskspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMigrationTasksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMigrationTasksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListMigrationTasks.html#MigrationHub.Paginator.ListMigrationTasks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listmigrationtaskspaginator)
        """

if TYPE_CHECKING:
    _ListProgressUpdateStreamsPaginatorBase = AioPaginator[ListProgressUpdateStreamsResultTypeDef]
else:
    _ListProgressUpdateStreamsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListProgressUpdateStreamsPaginator(_ListProgressUpdateStreamsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListProgressUpdateStreams.html#MigrationHub.Paginator.ListProgressUpdateStreams)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listprogressupdatestreamspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProgressUpdateStreamsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProgressUpdateStreamsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListProgressUpdateStreams.html#MigrationHub.Paginator.ListProgressUpdateStreams.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listprogressupdatestreamspaginator)
        """

if TYPE_CHECKING:
    _ListSourceResourcesPaginatorBase = AioPaginator[ListSourceResourcesResultTypeDef]
else:
    _ListSourceResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSourceResourcesPaginator(_ListSourceResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListSourceResources.html#MigrationHub.Paginator.ListSourceResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listsourceresourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSourceResourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSourceResourcesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListSourceResources.html#MigrationHub.Paginator.ListSourceResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listsourceresourcespaginator)
        """
