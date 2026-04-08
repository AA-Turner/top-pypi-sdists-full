"""
Type annotations for bedrock-data-automation service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_bedrock_data_automation.client import DataAutomationforBedrockClient
    from types_aiobotocore_bedrock_data_automation.paginator import (
        ListBlueprintsPaginator,
        ListDataAutomationLibrariesPaginator,
        ListDataAutomationLibraryEntitiesPaginator,
        ListDataAutomationLibraryIngestionJobsPaginator,
        ListDataAutomationProjectsPaginator,
    )

    session = get_session()
    with session.create_client("bedrock-data-automation") as client:
        client: DataAutomationforBedrockClient

        list_blueprints_paginator: ListBlueprintsPaginator = client.get_paginator("list_blueprints")
        list_data_automation_libraries_paginator: ListDataAutomationLibrariesPaginator = client.get_paginator("list_data_automation_libraries")
        list_data_automation_library_entities_paginator: ListDataAutomationLibraryEntitiesPaginator = client.get_paginator("list_data_automation_library_entities")
        list_data_automation_library_ingestion_jobs_paginator: ListDataAutomationLibraryIngestionJobsPaginator = client.get_paginator("list_data_automation_library_ingestion_jobs")
        list_data_automation_projects_paginator: ListDataAutomationProjectsPaginator = client.get_paginator("list_data_automation_projects")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListBlueprintsRequestPaginateTypeDef,
    ListBlueprintsResponseTypeDef,
    ListDataAutomationLibrariesRequestPaginateTypeDef,
    ListDataAutomationLibrariesResponseTypeDef,
    ListDataAutomationLibraryEntitiesRequestPaginateTypeDef,
    ListDataAutomationLibraryEntitiesResponseTypeDef,
    ListDataAutomationLibraryIngestionJobsRequestPaginateTypeDef,
    ListDataAutomationLibraryIngestionJobsResponseTypeDef,
    ListDataAutomationProjectsRequestPaginateTypeDef,
    ListDataAutomationProjectsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListBlueprintsPaginator",
    "ListDataAutomationLibrariesPaginator",
    "ListDataAutomationLibraryEntitiesPaginator",
    "ListDataAutomationLibraryIngestionJobsPaginator",
    "ListDataAutomationProjectsPaginator",
)

if TYPE_CHECKING:
    _ListBlueprintsPaginatorBase = AioPaginator[ListBlueprintsResponseTypeDef]
else:
    _ListBlueprintsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBlueprintsPaginator(_ListBlueprintsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListBlueprints.html#DataAutomationforBedrock.Paginator.ListBlueprints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/paginators/#listblueprintspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBlueprintsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBlueprintsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListBlueprints.html#DataAutomationforBedrock.Paginator.ListBlueprints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/paginators/#listblueprintspaginator)
        """

if TYPE_CHECKING:
    _ListDataAutomationLibrariesPaginatorBase = AioPaginator[
        ListDataAutomationLibrariesResponseTypeDef
    ]
else:
    _ListDataAutomationLibrariesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataAutomationLibrariesPaginator(_ListDataAutomationLibrariesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListDataAutomationLibraries.html#DataAutomationforBedrock.Paginator.ListDataAutomationLibraries)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/paginators/#listdataautomationlibrariespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataAutomationLibrariesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataAutomationLibrariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListDataAutomationLibraries.html#DataAutomationforBedrock.Paginator.ListDataAutomationLibraries.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/paginators/#listdataautomationlibrariespaginator)
        """

if TYPE_CHECKING:
    _ListDataAutomationLibraryEntitiesPaginatorBase = AioPaginator[
        ListDataAutomationLibraryEntitiesResponseTypeDef
    ]
else:
    _ListDataAutomationLibraryEntitiesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataAutomationLibraryEntitiesPaginator(_ListDataAutomationLibraryEntitiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListDataAutomationLibraryEntities.html#DataAutomationforBedrock.Paginator.ListDataAutomationLibraryEntities)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/paginators/#listdataautomationlibraryentitiespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataAutomationLibraryEntitiesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataAutomationLibraryEntitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListDataAutomationLibraryEntities.html#DataAutomationforBedrock.Paginator.ListDataAutomationLibraryEntities.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/paginators/#listdataautomationlibraryentitiespaginator)
        """

if TYPE_CHECKING:
    _ListDataAutomationLibraryIngestionJobsPaginatorBase = AioPaginator[
        ListDataAutomationLibraryIngestionJobsResponseTypeDef
    ]
else:
    _ListDataAutomationLibraryIngestionJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataAutomationLibraryIngestionJobsPaginator(
    _ListDataAutomationLibraryIngestionJobsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListDataAutomationLibraryIngestionJobs.html#DataAutomationforBedrock.Paginator.ListDataAutomationLibraryIngestionJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/paginators/#listdataautomationlibraryingestionjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataAutomationLibraryIngestionJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataAutomationLibraryIngestionJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListDataAutomationLibraryIngestionJobs.html#DataAutomationforBedrock.Paginator.ListDataAutomationLibraryIngestionJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/paginators/#listdataautomationlibraryingestionjobspaginator)
        """

if TYPE_CHECKING:
    _ListDataAutomationProjectsPaginatorBase = AioPaginator[
        ListDataAutomationProjectsResponseTypeDef
    ]
else:
    _ListDataAutomationProjectsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataAutomationProjectsPaginator(_ListDataAutomationProjectsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListDataAutomationProjects.html#DataAutomationforBedrock.Paginator.ListDataAutomationProjects)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/paginators/#listdataautomationprojectspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataAutomationProjectsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataAutomationProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListDataAutomationProjects.html#DataAutomationforBedrock.Paginator.ListDataAutomationProjects.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/paginators/#listdataautomationprojectspaginator)
        """
