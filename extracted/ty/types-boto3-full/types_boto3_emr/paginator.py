"""
Type annotations for emr service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_emr/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_emr.client import EMRClient
    from types_boto3_emr.paginator import (
        ListBootstrapActionsPaginator,
        ListClustersPaginator,
        ListInstanceFleetsPaginator,
        ListInstanceGroupsPaginator,
        ListInstancesPaginator,
        ListNotebookExecutionsPaginator,
        ListSecurityConfigurationsPaginator,
        ListStepsPaginator,
        ListStudioSessionMappingsPaginator,
        ListStudiosPaginator,
    )

    session = Session()
    client: EMRClient = session.client("emr")

    list_bootstrap_actions_paginator: ListBootstrapActionsPaginator = client.get_paginator("list_bootstrap_actions")
    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    list_instance_fleets_paginator: ListInstanceFleetsPaginator = client.get_paginator("list_instance_fleets")
    list_instance_groups_paginator: ListInstanceGroupsPaginator = client.get_paginator("list_instance_groups")
    list_instances_paginator: ListInstancesPaginator = client.get_paginator("list_instances")
    list_notebook_executions_paginator: ListNotebookExecutionsPaginator = client.get_paginator("list_notebook_executions")
    list_security_configurations_paginator: ListSecurityConfigurationsPaginator = client.get_paginator("list_security_configurations")
    list_steps_paginator: ListStepsPaginator = client.get_paginator("list_steps")
    list_studio_session_mappings_paginator: ListStudioSessionMappingsPaginator = client.get_paginator("list_studio_session_mappings")
    list_studios_paginator: ListStudiosPaginator = client.get_paginator("list_studios")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListBootstrapActionsInputPaginateTypeDef,
    ListBootstrapActionsOutputTypeDef,
    ListClustersInputPaginateTypeDef,
    ListClustersOutputTypeDef,
    ListInstanceFleetsInputPaginateTypeDef,
    ListInstanceFleetsOutputPaginatorTypeDef,
    ListInstanceGroupsInputPaginateTypeDef,
    ListInstanceGroupsOutputPaginatorTypeDef,
    ListInstancesInputPaginateTypeDef,
    ListInstancesOutputTypeDef,
    ListNotebookExecutionsInputPaginateTypeDef,
    ListNotebookExecutionsOutputTypeDef,
    ListSecurityConfigurationsInputPaginateTypeDef,
    ListSecurityConfigurationsOutputTypeDef,
    ListStepsInputPaginateTypeDef,
    ListStepsOutputTypeDef,
    ListStudioSessionMappingsInputPaginateTypeDef,
    ListStudioSessionMappingsOutputTypeDef,
    ListStudiosInputPaginateTypeDef,
    ListStudiosOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListBootstrapActionsPaginator",
    "ListClustersPaginator",
    "ListInstanceFleetsPaginator",
    "ListInstanceGroupsPaginator",
    "ListInstancesPaginator",
    "ListNotebookExecutionsPaginator",
    "ListSecurityConfigurationsPaginator",
    "ListStepsPaginator",
    "ListStudioSessionMappingsPaginator",
    "ListStudiosPaginator",
)


if TYPE_CHECKING:
    _ListBootstrapActionsPaginatorBase = Paginator[ListBootstrapActionsOutputTypeDef]
else:
    _ListBootstrapActionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListBootstrapActionsPaginator(_ListBootstrapActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListBootstrapActions.html#EMR.Paginator.ListBootstrapActions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_emr/paginators/#listbootstrapactionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBootstrapActionsInputPaginateTypeDef]
    ) -> PageIterator[ListBootstrapActionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListBootstrapActions.html#EMR.Paginator.ListBootstrapActions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_emr/paginators/#listbootstrapactionspaginator)
        """


if TYPE_CHECKING:
    _ListClustersPaginatorBase = Paginator[ListClustersOutputTypeDef]
else:
    _ListClustersPaginatorBase = Paginator  # type: ignore[assignment]


class ListClustersPaginator(_ListClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListClusters.html#EMR.Paginator.ListClusters)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_emr/paginators/#listclusterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListClustersInputPaginateTypeDef]
    ) -> PageIterator[ListClustersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListClusters.html#EMR.Paginator.ListClusters.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_emr/paginators/#listclusterspaginator)
        """


if TYPE_CHECKING:
    _ListInstanceFleetsPaginatorBase = Paginator[ListInstanceFleetsOutputPaginatorTypeDef]
else:
    _ListInstanceFleetsPaginatorBase = Paginator  # type: ignore[assignment]


class ListInstanceFleetsPaginator(_ListInstanceFleetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListInstanceFleets.html#EMR.Paginator.ListInstanceFleets)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_emr/paginators/#listinstancefleetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInstanceFleetsInputPaginateTypeDef]
    ) -> PageIterator[ListInstanceFleetsOutputPaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListInstanceFleets.html#EMR.Paginator.ListInstanceFleets.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_emr/paginators/#listinstancefleetspaginator)
        """


if TYPE_CHECKING:
    _ListInstanceGroupsPaginatorBase = Paginator[ListInstanceGroupsOutputPaginatorTypeDef]
else:
    _ListInstanceGroupsPaginatorBase = Paginator  # type: ignore[assignment]


class ListInstanceGroupsPaginator(_ListInstanceGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListInstanceGroups.html#EMR.Paginator.ListInstanceGroups)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_emr/paginators/#listinstancegroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInstanceGroupsInputPaginateTypeDef]
    ) -> PageIterator[ListInstanceGroupsOutputPaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListInstanceGroups.html#EMR.Paginator.ListInstanceGroups.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_emr/paginators/#listinstancegroupspaginator)
        """


if TYPE_CHECKING:
    _ListInstancesPaginatorBase = Paginator[ListInstancesOutputTypeDef]
else:
    _ListInstancesPaginatorBase = Paginator  # type: ignore[assignment]


class ListInstancesPaginator(_ListInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListInstances.html#EMR.Paginator.ListInstances)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_emr/paginators/#listinstancespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInstancesInputPaginateTypeDef]
    ) -> PageIterator[ListInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListInstances.html#EMR.Paginator.ListInstances.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_emr/paginators/#listinstancespaginator)
        """


if TYPE_CHECKING:
    _ListNotebookExecutionsPaginatorBase = Paginator[ListNotebookExecutionsOutputTypeDef]
else:
    _ListNotebookExecutionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListNotebookExecutionsPaginator(_ListNotebookExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListNotebookExecutions.html#EMR.Paginator.ListNotebookExecutions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_emr/paginators/#listnotebookexecutionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNotebookExecutionsInputPaginateTypeDef]
    ) -> PageIterator[ListNotebookExecutionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListNotebookExecutions.html#EMR.Paginator.ListNotebookExecutions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_emr/paginators/#listnotebookexecutionspaginator)
        """


if TYPE_CHECKING:
    _ListSecurityConfigurationsPaginatorBase = Paginator[ListSecurityConfigurationsOutputTypeDef]
else:
    _ListSecurityConfigurationsPaginatorBase = Paginator  # type: ignore[assignment]


class ListSecurityConfigurationsPaginator(_ListSecurityConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListSecurityConfigurations.html#EMR.Paginator.ListSecurityConfigurations)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_emr/paginators/#listsecurityconfigurationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSecurityConfigurationsInputPaginateTypeDef]
    ) -> PageIterator[ListSecurityConfigurationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListSecurityConfigurations.html#EMR.Paginator.ListSecurityConfigurations.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_emr/paginators/#listsecurityconfigurationspaginator)
        """


if TYPE_CHECKING:
    _ListStepsPaginatorBase = Paginator[ListStepsOutputTypeDef]
else:
    _ListStepsPaginatorBase = Paginator  # type: ignore[assignment]


class ListStepsPaginator(_ListStepsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListSteps.html#EMR.Paginator.ListSteps)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_emr/paginators/#liststepspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStepsInputPaginateTypeDef]
    ) -> PageIterator[ListStepsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListSteps.html#EMR.Paginator.ListSteps.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_emr/paginators/#liststepspaginator)
        """


if TYPE_CHECKING:
    _ListStudioSessionMappingsPaginatorBase = Paginator[ListStudioSessionMappingsOutputTypeDef]
else:
    _ListStudioSessionMappingsPaginatorBase = Paginator  # type: ignore[assignment]


class ListStudioSessionMappingsPaginator(_ListStudioSessionMappingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListStudioSessionMappings.html#EMR.Paginator.ListStudioSessionMappings)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_emr/paginators/#liststudiosessionmappingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStudioSessionMappingsInputPaginateTypeDef]
    ) -> PageIterator[ListStudioSessionMappingsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListStudioSessionMappings.html#EMR.Paginator.ListStudioSessionMappings.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_emr/paginators/#liststudiosessionmappingspaginator)
        """


if TYPE_CHECKING:
    _ListStudiosPaginatorBase = Paginator[ListStudiosOutputTypeDef]
else:
    _ListStudiosPaginatorBase = Paginator  # type: ignore[assignment]


class ListStudiosPaginator(_ListStudiosPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListStudios.html#EMR.Paginator.ListStudios)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_emr/paginators/#liststudiospaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStudiosInputPaginateTypeDef]
    ) -> PageIterator[ListStudiosOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/paginator/ListStudios.html#EMR.Paginator.ListStudios.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_emr/paginators/#liststudiospaginator)
        """
