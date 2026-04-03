"""
Type annotations for bedrock-data-automation service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_data_automation/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_bedrock_data_automation.client import DataAutomationforBedrockClient
    from mypy_boto3_bedrock_data_automation.paginator import (
        ListBlueprintsPaginator,
        ListDataAutomationLibrariesPaginator,
        ListDataAutomationLibraryEntitiesPaginator,
        ListDataAutomationLibraryIngestionJobsPaginator,
        ListDataAutomationProjectsPaginator,
    )

    session = Session()
    client: DataAutomationforBedrockClient = session.client("bedrock-data-automation")

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

from botocore.paginate import PageIterator, Paginator

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
    _ListBlueprintsPaginatorBase = Paginator[ListBlueprintsResponseTypeDef]
else:
    _ListBlueprintsPaginatorBase = Paginator  # type: ignore[assignment]

class ListBlueprintsPaginator(_ListBlueprintsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListBlueprints.html#DataAutomationforBedrock.Paginator.ListBlueprints)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_data_automation/paginators/#listblueprintspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBlueprintsRequestPaginateTypeDef]
    ) -> PageIterator[ListBlueprintsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListBlueprints.html#DataAutomationforBedrock.Paginator.ListBlueprints.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_data_automation/paginators/#listblueprintspaginator)
        """

if TYPE_CHECKING:
    _ListDataAutomationLibrariesPaginatorBase = Paginator[
        ListDataAutomationLibrariesResponseTypeDef
    ]
else:
    _ListDataAutomationLibrariesPaginatorBase = Paginator  # type: ignore[assignment]

class ListDataAutomationLibrariesPaginator(_ListDataAutomationLibrariesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListDataAutomationLibraries.html#DataAutomationforBedrock.Paginator.ListDataAutomationLibraries)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_data_automation/paginators/#listdataautomationlibrariespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataAutomationLibrariesRequestPaginateTypeDef]
    ) -> PageIterator[ListDataAutomationLibrariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListDataAutomationLibraries.html#DataAutomationforBedrock.Paginator.ListDataAutomationLibraries.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_data_automation/paginators/#listdataautomationlibrariespaginator)
        """

if TYPE_CHECKING:
    _ListDataAutomationLibraryEntitiesPaginatorBase = Paginator[
        ListDataAutomationLibraryEntitiesResponseTypeDef
    ]
else:
    _ListDataAutomationLibraryEntitiesPaginatorBase = Paginator  # type: ignore[assignment]

class ListDataAutomationLibraryEntitiesPaginator(_ListDataAutomationLibraryEntitiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListDataAutomationLibraryEntities.html#DataAutomationforBedrock.Paginator.ListDataAutomationLibraryEntities)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_data_automation/paginators/#listdataautomationlibraryentitiespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataAutomationLibraryEntitiesRequestPaginateTypeDef]
    ) -> PageIterator[ListDataAutomationLibraryEntitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListDataAutomationLibraryEntities.html#DataAutomationforBedrock.Paginator.ListDataAutomationLibraryEntities.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_data_automation/paginators/#listdataautomationlibraryentitiespaginator)
        """

if TYPE_CHECKING:
    _ListDataAutomationLibraryIngestionJobsPaginatorBase = Paginator[
        ListDataAutomationLibraryIngestionJobsResponseTypeDef
    ]
else:
    _ListDataAutomationLibraryIngestionJobsPaginatorBase = Paginator  # type: ignore[assignment]

class ListDataAutomationLibraryIngestionJobsPaginator(
    _ListDataAutomationLibraryIngestionJobsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListDataAutomationLibraryIngestionJobs.html#DataAutomationforBedrock.Paginator.ListDataAutomationLibraryIngestionJobs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_data_automation/paginators/#listdataautomationlibraryingestionjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataAutomationLibraryIngestionJobsRequestPaginateTypeDef]
    ) -> PageIterator[ListDataAutomationLibraryIngestionJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListDataAutomationLibraryIngestionJobs.html#DataAutomationforBedrock.Paginator.ListDataAutomationLibraryIngestionJobs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_data_automation/paginators/#listdataautomationlibraryingestionjobspaginator)
        """

if TYPE_CHECKING:
    _ListDataAutomationProjectsPaginatorBase = Paginator[ListDataAutomationProjectsResponseTypeDef]
else:
    _ListDataAutomationProjectsPaginatorBase = Paginator  # type: ignore[assignment]

class ListDataAutomationProjectsPaginator(_ListDataAutomationProjectsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListDataAutomationProjects.html#DataAutomationforBedrock.Paginator.ListDataAutomationProjects)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_data_automation/paginators/#listdataautomationprojectspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataAutomationProjectsRequestPaginateTypeDef]
    ) -> PageIterator[ListDataAutomationProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListDataAutomationProjects.html#DataAutomationforBedrock.Paginator.ListDataAutomationProjects.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_data_automation/paginators/#listdataautomationprojectspaginator)
        """
