"""
Type annotations for mwaa-serverless service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa_serverless/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mwaa_serverless.client import MWAAServerlessClient
    from types_aiobotocore_mwaa_serverless.paginator import (
        ListTaskInstancesPaginator,
        ListWorkflowRunsPaginator,
        ListWorkflowVersionsPaginator,
        ListWorkflowsPaginator,
    )

    session = get_session()
    with session.create_client("mwaa-serverless") as client:
        client: MWAAServerlessClient

        list_task_instances_paginator: ListTaskInstancesPaginator = client.get_paginator("list_task_instances")
        list_workflow_runs_paginator: ListWorkflowRunsPaginator = client.get_paginator("list_workflow_runs")
        list_workflow_versions_paginator: ListWorkflowVersionsPaginator = client.get_paginator("list_workflow_versions")
        list_workflows_paginator: ListWorkflowsPaginator = client.get_paginator("list_workflows")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListTaskInstancesRequestPaginateTypeDef,
    ListTaskInstancesResponseTypeDef,
    ListWorkflowRunsRequestPaginateTypeDef,
    ListWorkflowRunsResponseTypeDef,
    ListWorkflowsRequestPaginateTypeDef,
    ListWorkflowsResponseTypeDef,
    ListWorkflowVersionsRequestPaginateTypeDef,
    ListWorkflowVersionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListTaskInstancesPaginator",
    "ListWorkflowRunsPaginator",
    "ListWorkflowVersionsPaginator",
    "ListWorkflowsPaginator",
)


if TYPE_CHECKING:
    _ListTaskInstancesPaginatorBase = AioPaginator[ListTaskInstancesResponseTypeDef]
else:
    _ListTaskInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTaskInstancesPaginator(_ListTaskInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa-serverless/paginator/ListTaskInstances.html#MWAAServerless.Paginator.ListTaskInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa_serverless/paginators/#listtaskinstancespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTaskInstancesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTaskInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa-serverless/paginator/ListTaskInstances.html#MWAAServerless.Paginator.ListTaskInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa_serverless/paginators/#listtaskinstancespaginator)
        """


if TYPE_CHECKING:
    _ListWorkflowRunsPaginatorBase = AioPaginator[ListWorkflowRunsResponseTypeDef]
else:
    _ListWorkflowRunsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWorkflowRunsPaginator(_ListWorkflowRunsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa-serverless/paginator/ListWorkflowRuns.html#MWAAServerless.Paginator.ListWorkflowRuns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa_serverless/paginators/#listworkflowrunspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkflowRunsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkflowRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa-serverless/paginator/ListWorkflowRuns.html#MWAAServerless.Paginator.ListWorkflowRuns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa_serverless/paginators/#listworkflowrunspaginator)
        """


if TYPE_CHECKING:
    _ListWorkflowVersionsPaginatorBase = AioPaginator[ListWorkflowVersionsResponseTypeDef]
else:
    _ListWorkflowVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWorkflowVersionsPaginator(_ListWorkflowVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa-serverless/paginator/ListWorkflowVersions.html#MWAAServerless.Paginator.ListWorkflowVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa_serverless/paginators/#listworkflowversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkflowVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkflowVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa-serverless/paginator/ListWorkflowVersions.html#MWAAServerless.Paginator.ListWorkflowVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa_serverless/paginators/#listworkflowversionspaginator)
        """


if TYPE_CHECKING:
    _ListWorkflowsPaginatorBase = AioPaginator[ListWorkflowsResponseTypeDef]
else:
    _ListWorkflowsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWorkflowsPaginator(_ListWorkflowsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa-serverless/paginator/ListWorkflows.html#MWAAServerless.Paginator.ListWorkflows)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa_serverless/paginators/#listworkflowspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkflowsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkflowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa-serverless/paginator/ListWorkflows.html#MWAAServerless.Paginator.ListWorkflows.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa_serverless/paginators/#listworkflowspaginator)
        """
