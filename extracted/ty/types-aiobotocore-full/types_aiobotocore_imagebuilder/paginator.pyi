"""
Type annotations for imagebuilder service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_imagebuilder.client import ImagebuilderClient
    from types_aiobotocore_imagebuilder.paginator import (
        ListLifecycleExecutionResourcesPaginator,
        ListLifecycleExecutionsPaginator,
        ListLifecyclePoliciesPaginator,
        ListWaitingWorkflowStepsPaginator,
        ListWorkflowBuildVersionsPaginator,
        ListWorkflowsPaginator,
    )

    session = get_session()
    with session.create_client("imagebuilder") as client:
        client: ImagebuilderClient

        list_lifecycle_execution_resources_paginator: ListLifecycleExecutionResourcesPaginator = client.get_paginator("list_lifecycle_execution_resources")
        list_lifecycle_executions_paginator: ListLifecycleExecutionsPaginator = client.get_paginator("list_lifecycle_executions")
        list_lifecycle_policies_paginator: ListLifecyclePoliciesPaginator = client.get_paginator("list_lifecycle_policies")
        list_waiting_workflow_steps_paginator: ListWaitingWorkflowStepsPaginator = client.get_paginator("list_waiting_workflow_steps")
        list_workflow_build_versions_paginator: ListWorkflowBuildVersionsPaginator = client.get_paginator("list_workflow_build_versions")
        list_workflows_paginator: ListWorkflowsPaginator = client.get_paginator("list_workflows")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListLifecycleExecutionResourcesRequestPaginateTypeDef,
    ListLifecycleExecutionResourcesResponseTypeDef,
    ListLifecycleExecutionsRequestPaginateTypeDef,
    ListLifecycleExecutionsResponseTypeDef,
    ListLifecyclePoliciesRequestPaginateTypeDef,
    ListLifecyclePoliciesResponseTypeDef,
    ListWaitingWorkflowStepsRequestPaginateTypeDef,
    ListWaitingWorkflowStepsResponseTypeDef,
    ListWorkflowBuildVersionsRequestPaginateTypeDef,
    ListWorkflowBuildVersionsResponseTypeDef,
    ListWorkflowsRequestPaginateTypeDef,
    ListWorkflowsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListLifecycleExecutionResourcesPaginator",
    "ListLifecycleExecutionsPaginator",
    "ListLifecyclePoliciesPaginator",
    "ListWaitingWorkflowStepsPaginator",
    "ListWorkflowBuildVersionsPaginator",
    "ListWorkflowsPaginator",
)

if TYPE_CHECKING:
    _ListLifecycleExecutionResourcesPaginatorBase = AioPaginator[
        ListLifecycleExecutionResourcesResponseTypeDef
    ]
else:
    _ListLifecycleExecutionResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLifecycleExecutionResourcesPaginator(_ListLifecycleExecutionResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListLifecycleExecutionResources.html#Imagebuilder.Paginator.ListLifecycleExecutionResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listlifecycleexecutionresourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLifecycleExecutionResourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLifecycleExecutionResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListLifecycleExecutionResources.html#Imagebuilder.Paginator.ListLifecycleExecutionResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listlifecycleexecutionresourcespaginator)
        """

if TYPE_CHECKING:
    _ListLifecycleExecutionsPaginatorBase = AioPaginator[ListLifecycleExecutionsResponseTypeDef]
else:
    _ListLifecycleExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLifecycleExecutionsPaginator(_ListLifecycleExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListLifecycleExecutions.html#Imagebuilder.Paginator.ListLifecycleExecutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listlifecycleexecutionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLifecycleExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLifecycleExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListLifecycleExecutions.html#Imagebuilder.Paginator.ListLifecycleExecutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listlifecycleexecutionspaginator)
        """

if TYPE_CHECKING:
    _ListLifecyclePoliciesPaginatorBase = AioPaginator[ListLifecyclePoliciesResponseTypeDef]
else:
    _ListLifecyclePoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLifecyclePoliciesPaginator(_ListLifecyclePoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListLifecyclePolicies.html#Imagebuilder.Paginator.ListLifecyclePolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listlifecyclepoliciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLifecyclePoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLifecyclePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListLifecyclePolicies.html#Imagebuilder.Paginator.ListLifecyclePolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listlifecyclepoliciespaginator)
        """

if TYPE_CHECKING:
    _ListWaitingWorkflowStepsPaginatorBase = AioPaginator[ListWaitingWorkflowStepsResponseTypeDef]
else:
    _ListWaitingWorkflowStepsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListWaitingWorkflowStepsPaginator(_ListWaitingWorkflowStepsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWaitingWorkflowSteps.html#Imagebuilder.Paginator.ListWaitingWorkflowSteps)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listwaitingworkflowstepspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWaitingWorkflowStepsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWaitingWorkflowStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWaitingWorkflowSteps.html#Imagebuilder.Paginator.ListWaitingWorkflowSteps.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listwaitingworkflowstepspaginator)
        """

if TYPE_CHECKING:
    _ListWorkflowBuildVersionsPaginatorBase = AioPaginator[ListWorkflowBuildVersionsResponseTypeDef]
else:
    _ListWorkflowBuildVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListWorkflowBuildVersionsPaginator(_ListWorkflowBuildVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWorkflowBuildVersions.html#Imagebuilder.Paginator.ListWorkflowBuildVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listworkflowbuildversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkflowBuildVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkflowBuildVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWorkflowBuildVersions.html#Imagebuilder.Paginator.ListWorkflowBuildVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listworkflowbuildversionspaginator)
        """

if TYPE_CHECKING:
    _ListWorkflowsPaginatorBase = AioPaginator[ListWorkflowsResponseTypeDef]
else:
    _ListWorkflowsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListWorkflowsPaginator(_ListWorkflowsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWorkflows.html#Imagebuilder.Paginator.ListWorkflows)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listworkflowspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkflowsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkflowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWorkflows.html#Imagebuilder.Paginator.ListWorkflows.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listworkflowspaginator)
        """
