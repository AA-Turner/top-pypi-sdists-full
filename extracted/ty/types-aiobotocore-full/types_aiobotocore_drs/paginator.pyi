"""
Type annotations for drs service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_drs.client import DrsClient
    from types_aiobotocore_drs.paginator import (
        DescribeJobLogItemsPaginator,
        DescribeJobsPaginator,
        DescribeLaunchConfigurationTemplatesPaginator,
        DescribeRecoveryInstancesPaginator,
        DescribeRecoverySnapshotsPaginator,
        DescribeReplicationConfigurationTemplatesPaginator,
        DescribeSourceNetworksPaginator,
        DescribeSourceServersPaginator,
        ListExtensibleSourceServersPaginator,
        ListLaunchActionsPaginator,
        ListRecoveryPlanExecutionStepsPaginator,
        ListRecoveryPlanExecutionsPaginator,
        ListRecoveryPlanStepsPaginator,
        ListRecoveryPlansPaginator,
        ListStagingAccountsPaginator,
    )

    session = get_session()
    with session.create_client("drs") as client:
        client: DrsClient

        describe_job_log_items_paginator: DescribeJobLogItemsPaginator = client.get_paginator("describe_job_log_items")
        describe_jobs_paginator: DescribeJobsPaginator = client.get_paginator("describe_jobs")
        describe_launch_configuration_templates_paginator: DescribeLaunchConfigurationTemplatesPaginator = client.get_paginator("describe_launch_configuration_templates")
        describe_recovery_instances_paginator: DescribeRecoveryInstancesPaginator = client.get_paginator("describe_recovery_instances")
        describe_recovery_snapshots_paginator: DescribeRecoverySnapshotsPaginator = client.get_paginator("describe_recovery_snapshots")
        describe_replication_configuration_templates_paginator: DescribeReplicationConfigurationTemplatesPaginator = client.get_paginator("describe_replication_configuration_templates")
        describe_source_networks_paginator: DescribeSourceNetworksPaginator = client.get_paginator("describe_source_networks")
        describe_source_servers_paginator: DescribeSourceServersPaginator = client.get_paginator("describe_source_servers")
        list_extensible_source_servers_paginator: ListExtensibleSourceServersPaginator = client.get_paginator("list_extensible_source_servers")
        list_launch_actions_paginator: ListLaunchActionsPaginator = client.get_paginator("list_launch_actions")
        list_recovery_plan_execution_steps_paginator: ListRecoveryPlanExecutionStepsPaginator = client.get_paginator("list_recovery_plan_execution_steps")
        list_recovery_plan_executions_paginator: ListRecoveryPlanExecutionsPaginator = client.get_paginator("list_recovery_plan_executions")
        list_recovery_plan_steps_paginator: ListRecoveryPlanStepsPaginator = client.get_paginator("list_recovery_plan_steps")
        list_recovery_plans_paginator: ListRecoveryPlansPaginator = client.get_paginator("list_recovery_plans")
        list_staging_accounts_paginator: ListStagingAccountsPaginator = client.get_paginator("list_staging_accounts")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeJobLogItemsRequestPaginateTypeDef,
    DescribeJobLogItemsResponseTypeDef,
    DescribeJobsRequestPaginateTypeDef,
    DescribeJobsResponseTypeDef,
    DescribeLaunchConfigurationTemplatesRequestPaginateTypeDef,
    DescribeLaunchConfigurationTemplatesResponseTypeDef,
    DescribeRecoveryInstancesRequestPaginateTypeDef,
    DescribeRecoveryInstancesResponseTypeDef,
    DescribeRecoverySnapshotsRequestPaginateTypeDef,
    DescribeRecoverySnapshotsResponseTypeDef,
    DescribeReplicationConfigurationTemplatesRequestPaginateTypeDef,
    DescribeReplicationConfigurationTemplatesResponseTypeDef,
    DescribeSourceNetworksRequestPaginateTypeDef,
    DescribeSourceNetworksResponseTypeDef,
    DescribeSourceServersRequestPaginateTypeDef,
    DescribeSourceServersResponseTypeDef,
    ListExtensibleSourceServersRequestPaginateTypeDef,
    ListExtensibleSourceServersResponseTypeDef,
    ListLaunchActionsRequestPaginateTypeDef,
    ListLaunchActionsResponseTypeDef,
    ListRecoveryPlanExecutionsRequestPaginateTypeDef,
    ListRecoveryPlanExecutionsResponseTypeDef,
    ListRecoveryPlanExecutionStepsRequestPaginateTypeDef,
    ListRecoveryPlanExecutionStepsResponseTypeDef,
    ListRecoveryPlansRequestPaginateTypeDef,
    ListRecoveryPlansResponseTypeDef,
    ListRecoveryPlanStepsRequestPaginateTypeDef,
    ListRecoveryPlanStepsResponseTypeDef,
    ListStagingAccountsRequestPaginateTypeDef,
    ListStagingAccountsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeJobLogItemsPaginator",
    "DescribeJobsPaginator",
    "DescribeLaunchConfigurationTemplatesPaginator",
    "DescribeRecoveryInstancesPaginator",
    "DescribeRecoverySnapshotsPaginator",
    "DescribeReplicationConfigurationTemplatesPaginator",
    "DescribeSourceNetworksPaginator",
    "DescribeSourceServersPaginator",
    "ListExtensibleSourceServersPaginator",
    "ListLaunchActionsPaginator",
    "ListRecoveryPlanExecutionStepsPaginator",
    "ListRecoveryPlanExecutionsPaginator",
    "ListRecoveryPlanStepsPaginator",
    "ListRecoveryPlansPaginator",
    "ListStagingAccountsPaginator",
)

if TYPE_CHECKING:
    _DescribeJobLogItemsPaginatorBase = AioPaginator[DescribeJobLogItemsResponseTypeDef]
else:
    _DescribeJobLogItemsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeJobLogItemsPaginator(_DescribeJobLogItemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeJobLogItems.html#Drs.Paginator.DescribeJobLogItems)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#describejoblogitemspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeJobLogItemsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeJobLogItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeJobLogItems.html#Drs.Paginator.DescribeJobLogItems.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#describejoblogitemspaginator)
        """

if TYPE_CHECKING:
    _DescribeJobsPaginatorBase = AioPaginator[DescribeJobsResponseTypeDef]
else:
    _DescribeJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeJobsPaginator(_DescribeJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeJobs.html#Drs.Paginator.DescribeJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#describejobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeJobs.html#Drs.Paginator.DescribeJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#describejobspaginator)
        """

if TYPE_CHECKING:
    _DescribeLaunchConfigurationTemplatesPaginatorBase = AioPaginator[
        DescribeLaunchConfigurationTemplatesResponseTypeDef
    ]
else:
    _DescribeLaunchConfigurationTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeLaunchConfigurationTemplatesPaginator(
    _DescribeLaunchConfigurationTemplatesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeLaunchConfigurationTemplates.html#Drs.Paginator.DescribeLaunchConfigurationTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#describelaunchconfigurationtemplatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeLaunchConfigurationTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeLaunchConfigurationTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeLaunchConfigurationTemplates.html#Drs.Paginator.DescribeLaunchConfigurationTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#describelaunchconfigurationtemplatespaginator)
        """

if TYPE_CHECKING:
    _DescribeRecoveryInstancesPaginatorBase = AioPaginator[DescribeRecoveryInstancesResponseTypeDef]
else:
    _DescribeRecoveryInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeRecoveryInstancesPaginator(_DescribeRecoveryInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeRecoveryInstances.html#Drs.Paginator.DescribeRecoveryInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#describerecoveryinstancespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeRecoveryInstancesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeRecoveryInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeRecoveryInstances.html#Drs.Paginator.DescribeRecoveryInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#describerecoveryinstancespaginator)
        """

if TYPE_CHECKING:
    _DescribeRecoverySnapshotsPaginatorBase = AioPaginator[DescribeRecoverySnapshotsResponseTypeDef]
else:
    _DescribeRecoverySnapshotsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeRecoverySnapshotsPaginator(_DescribeRecoverySnapshotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeRecoverySnapshots.html#Drs.Paginator.DescribeRecoverySnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#describerecoverysnapshotspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeRecoverySnapshotsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeRecoverySnapshotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeRecoverySnapshots.html#Drs.Paginator.DescribeRecoverySnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#describerecoverysnapshotspaginator)
        """

if TYPE_CHECKING:
    _DescribeReplicationConfigurationTemplatesPaginatorBase = AioPaginator[
        DescribeReplicationConfigurationTemplatesResponseTypeDef
    ]
else:
    _DescribeReplicationConfigurationTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeReplicationConfigurationTemplatesPaginator(
    _DescribeReplicationConfigurationTemplatesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeReplicationConfigurationTemplates.html#Drs.Paginator.DescribeReplicationConfigurationTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#describereplicationconfigurationtemplatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReplicationConfigurationTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeReplicationConfigurationTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeReplicationConfigurationTemplates.html#Drs.Paginator.DescribeReplicationConfigurationTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#describereplicationconfigurationtemplatespaginator)
        """

if TYPE_CHECKING:
    _DescribeSourceNetworksPaginatorBase = AioPaginator[DescribeSourceNetworksResponseTypeDef]
else:
    _DescribeSourceNetworksPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeSourceNetworksPaginator(_DescribeSourceNetworksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeSourceNetworks.html#Drs.Paginator.DescribeSourceNetworks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#describesourcenetworkspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSourceNetworksRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeSourceNetworksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeSourceNetworks.html#Drs.Paginator.DescribeSourceNetworks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#describesourcenetworkspaginator)
        """

if TYPE_CHECKING:
    _DescribeSourceServersPaginatorBase = AioPaginator[DescribeSourceServersResponseTypeDef]
else:
    _DescribeSourceServersPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeSourceServersPaginator(_DescribeSourceServersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeSourceServers.html#Drs.Paginator.DescribeSourceServers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#describesourceserverspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSourceServersRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeSourceServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeSourceServers.html#Drs.Paginator.DescribeSourceServers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#describesourceserverspaginator)
        """

if TYPE_CHECKING:
    _ListExtensibleSourceServersPaginatorBase = AioPaginator[
        ListExtensibleSourceServersResponseTypeDef
    ]
else:
    _ListExtensibleSourceServersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListExtensibleSourceServersPaginator(_ListExtensibleSourceServersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/ListExtensibleSourceServers.html#Drs.Paginator.ListExtensibleSourceServers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#listextensiblesourceserverspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExtensibleSourceServersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListExtensibleSourceServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/ListExtensibleSourceServers.html#Drs.Paginator.ListExtensibleSourceServers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#listextensiblesourceserverspaginator)
        """

if TYPE_CHECKING:
    _ListLaunchActionsPaginatorBase = AioPaginator[ListLaunchActionsResponseTypeDef]
else:
    _ListLaunchActionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLaunchActionsPaginator(_ListLaunchActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/ListLaunchActions.html#Drs.Paginator.ListLaunchActions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#listlaunchactionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLaunchActionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLaunchActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/ListLaunchActions.html#Drs.Paginator.ListLaunchActions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#listlaunchactionspaginator)
        """

if TYPE_CHECKING:
    _ListRecoveryPlanExecutionStepsPaginatorBase = AioPaginator[
        ListRecoveryPlanExecutionStepsResponseTypeDef
    ]
else:
    _ListRecoveryPlanExecutionStepsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRecoveryPlanExecutionStepsPaginator(_ListRecoveryPlanExecutionStepsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/ListRecoveryPlanExecutionSteps.html#Drs.Paginator.ListRecoveryPlanExecutionSteps)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#listrecoveryplanexecutionstepspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRecoveryPlanExecutionStepsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRecoveryPlanExecutionStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/ListRecoveryPlanExecutionSteps.html#Drs.Paginator.ListRecoveryPlanExecutionSteps.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#listrecoveryplanexecutionstepspaginator)
        """

if TYPE_CHECKING:
    _ListRecoveryPlanExecutionsPaginatorBase = AioPaginator[
        ListRecoveryPlanExecutionsResponseTypeDef
    ]
else:
    _ListRecoveryPlanExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRecoveryPlanExecutionsPaginator(_ListRecoveryPlanExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/ListRecoveryPlanExecutions.html#Drs.Paginator.ListRecoveryPlanExecutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#listrecoveryplanexecutionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRecoveryPlanExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRecoveryPlanExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/ListRecoveryPlanExecutions.html#Drs.Paginator.ListRecoveryPlanExecutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#listrecoveryplanexecutionspaginator)
        """

if TYPE_CHECKING:
    _ListRecoveryPlanStepsPaginatorBase = AioPaginator[ListRecoveryPlanStepsResponseTypeDef]
else:
    _ListRecoveryPlanStepsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRecoveryPlanStepsPaginator(_ListRecoveryPlanStepsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/ListRecoveryPlanSteps.html#Drs.Paginator.ListRecoveryPlanSteps)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#listrecoveryplanstepspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRecoveryPlanStepsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRecoveryPlanStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/ListRecoveryPlanSteps.html#Drs.Paginator.ListRecoveryPlanSteps.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#listrecoveryplanstepspaginator)
        """

if TYPE_CHECKING:
    _ListRecoveryPlansPaginatorBase = AioPaginator[ListRecoveryPlansResponseTypeDef]
else:
    _ListRecoveryPlansPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRecoveryPlansPaginator(_ListRecoveryPlansPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/ListRecoveryPlans.html#Drs.Paginator.ListRecoveryPlans)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#listrecoveryplanspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRecoveryPlansRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRecoveryPlansResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/ListRecoveryPlans.html#Drs.Paginator.ListRecoveryPlans.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#listrecoveryplanspaginator)
        """

if TYPE_CHECKING:
    _ListStagingAccountsPaginatorBase = AioPaginator[ListStagingAccountsResponseTypeDef]
else:
    _ListStagingAccountsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListStagingAccountsPaginator(_ListStagingAccountsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/ListStagingAccounts.html#Drs.Paginator.ListStagingAccounts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#liststagingaccountspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStagingAccountsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListStagingAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/ListStagingAccounts.html#Drs.Paginator.ListStagingAccounts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/paginators/#liststagingaccountspaginator)
        """
