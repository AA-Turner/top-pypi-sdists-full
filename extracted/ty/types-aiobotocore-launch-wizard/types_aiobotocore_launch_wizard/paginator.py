"""
Type annotations for launch-wizard service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_launch_wizard.client import LaunchWizardClient
    from types_aiobotocore_launch_wizard.paginator import (
        ListDeploymentEventsPaginator,
        ListDeploymentsPaginator,
        ListWorkloadDeploymentPatternsPaginator,
        ListWorkloadsPaginator,
    )

    session = get_session()
    with session.create_client("launch-wizard") as client:
        client: LaunchWizardClient

        list_deployment_events_paginator: ListDeploymentEventsPaginator = client.get_paginator("list_deployment_events")
        list_deployments_paginator: ListDeploymentsPaginator = client.get_paginator("list_deployments")
        list_workload_deployment_patterns_paginator: ListWorkloadDeploymentPatternsPaginator = client.get_paginator("list_workload_deployment_patterns")
        list_workloads_paginator: ListWorkloadsPaginator = client.get_paginator("list_workloads")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListDeploymentEventsInputPaginateTypeDef,
    ListDeploymentEventsOutputTypeDef,
    ListDeploymentsInputPaginateTypeDef,
    ListDeploymentsOutputTypeDef,
    ListWorkloadDeploymentPatternsInputPaginateTypeDef,
    ListWorkloadDeploymentPatternsOutputTypeDef,
    ListWorkloadsInputPaginateTypeDef,
    ListWorkloadsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListDeploymentEventsPaginator",
    "ListDeploymentsPaginator",
    "ListWorkloadDeploymentPatternsPaginator",
    "ListWorkloadsPaginator",
)


if TYPE_CHECKING:
    _ListDeploymentEventsPaginatorBase = AioPaginator[ListDeploymentEventsOutputTypeDef]
else:
    _ListDeploymentEventsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDeploymentEventsPaginator(_ListDeploymentEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/paginator/ListDeploymentEvents.html#LaunchWizard.Paginator.ListDeploymentEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/paginators/#listdeploymenteventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeploymentEventsInputPaginateTypeDef]
    ) -> AioPageIterator[ListDeploymentEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/paginator/ListDeploymentEvents.html#LaunchWizard.Paginator.ListDeploymentEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/paginators/#listdeploymenteventspaginator)
        """


if TYPE_CHECKING:
    _ListDeploymentsPaginatorBase = AioPaginator[ListDeploymentsOutputTypeDef]
else:
    _ListDeploymentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDeploymentsPaginator(_ListDeploymentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/paginator/ListDeployments.html#LaunchWizard.Paginator.ListDeployments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/paginators/#listdeploymentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeploymentsInputPaginateTypeDef]
    ) -> AioPageIterator[ListDeploymentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/paginator/ListDeployments.html#LaunchWizard.Paginator.ListDeployments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/paginators/#listdeploymentspaginator)
        """


if TYPE_CHECKING:
    _ListWorkloadDeploymentPatternsPaginatorBase = AioPaginator[
        ListWorkloadDeploymentPatternsOutputTypeDef
    ]
else:
    _ListWorkloadDeploymentPatternsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWorkloadDeploymentPatternsPaginator(_ListWorkloadDeploymentPatternsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/paginator/ListWorkloadDeploymentPatterns.html#LaunchWizard.Paginator.ListWorkloadDeploymentPatterns)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/paginators/#listworkloaddeploymentpatternspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkloadDeploymentPatternsInputPaginateTypeDef]
    ) -> AioPageIterator[ListWorkloadDeploymentPatternsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/paginator/ListWorkloadDeploymentPatterns.html#LaunchWizard.Paginator.ListWorkloadDeploymentPatterns.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/paginators/#listworkloaddeploymentpatternspaginator)
        """


if TYPE_CHECKING:
    _ListWorkloadsPaginatorBase = AioPaginator[ListWorkloadsOutputTypeDef]
else:
    _ListWorkloadsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWorkloadsPaginator(_ListWorkloadsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/paginator/ListWorkloads.html#LaunchWizard.Paginator.ListWorkloads)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/paginators/#listworkloadspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkloadsInputPaginateTypeDef]
    ) -> AioPageIterator[ListWorkloadsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/paginator/ListWorkloads.html#LaunchWizard.Paginator.ListWorkloads.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/paginators/#listworkloadspaginator)
        """
