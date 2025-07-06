"""
Type annotations for codedeploy service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_codedeploy.client import CodeDeployClient
    from types_aiobotocore_codedeploy.paginator import (
        ListApplicationRevisionsPaginator,
        ListApplicationsPaginator,
        ListDeploymentConfigsPaginator,
        ListDeploymentGroupsPaginator,
        ListDeploymentInstancesPaginator,
        ListDeploymentTargetsPaginator,
        ListDeploymentsPaginator,
        ListGitHubAccountTokenNamesPaginator,
        ListOnPremisesInstancesPaginator,
    )

    session = get_session()
    with session.create_client("codedeploy") as client:
        client: CodeDeployClient

        list_application_revisions_paginator: ListApplicationRevisionsPaginator = client.get_paginator("list_application_revisions")
        list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
        list_deployment_configs_paginator: ListDeploymentConfigsPaginator = client.get_paginator("list_deployment_configs")
        list_deployment_groups_paginator: ListDeploymentGroupsPaginator = client.get_paginator("list_deployment_groups")
        list_deployment_instances_paginator: ListDeploymentInstancesPaginator = client.get_paginator("list_deployment_instances")
        list_deployment_targets_paginator: ListDeploymentTargetsPaginator = client.get_paginator("list_deployment_targets")
        list_deployments_paginator: ListDeploymentsPaginator = client.get_paginator("list_deployments")
        list_git_hub_account_token_names_paginator: ListGitHubAccountTokenNamesPaginator = client.get_paginator("list_git_hub_account_token_names")
        list_on_premises_instances_paginator: ListOnPremisesInstancesPaginator = client.get_paginator("list_on_premises_instances")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListApplicationRevisionsInputPaginateTypeDef,
    ListApplicationRevisionsOutputTypeDef,
    ListApplicationsInputPaginateTypeDef,
    ListApplicationsOutputTypeDef,
    ListDeploymentConfigsInputPaginateTypeDef,
    ListDeploymentConfigsOutputTypeDef,
    ListDeploymentGroupsInputPaginateTypeDef,
    ListDeploymentGroupsOutputTypeDef,
    ListDeploymentInstancesInputPaginateTypeDef,
    ListDeploymentInstancesOutputTypeDef,
    ListDeploymentsInputPaginateTypeDef,
    ListDeploymentsOutputTypeDef,
    ListDeploymentTargetsInputPaginateTypeDef,
    ListDeploymentTargetsOutputTypeDef,
    ListGitHubAccountTokenNamesInputPaginateTypeDef,
    ListGitHubAccountTokenNamesOutputTypeDef,
    ListOnPremisesInstancesInputPaginateTypeDef,
    ListOnPremisesInstancesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListApplicationRevisionsPaginator",
    "ListApplicationsPaginator",
    "ListDeploymentConfigsPaginator",
    "ListDeploymentGroupsPaginator",
    "ListDeploymentInstancesPaginator",
    "ListDeploymentTargetsPaginator",
    "ListDeploymentsPaginator",
    "ListGitHubAccountTokenNamesPaginator",
    "ListOnPremisesInstancesPaginator",
)


if TYPE_CHECKING:
    _ListApplicationRevisionsPaginatorBase = AioPaginator[ListApplicationRevisionsOutputTypeDef]
else:
    _ListApplicationRevisionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListApplicationRevisionsPaginator(_ListApplicationRevisionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListApplicationRevisions.html#CodeDeploy.Paginator.ListApplicationRevisions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listapplicationrevisionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationRevisionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListApplicationRevisionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListApplicationRevisions.html#CodeDeploy.Paginator.ListApplicationRevisions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listapplicationrevisionspaginator)
        """


if TYPE_CHECKING:
    _ListApplicationsPaginatorBase = AioPaginator[ListApplicationsOutputTypeDef]
else:
    _ListApplicationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListApplicationsPaginator(_ListApplicationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListApplications.html#CodeDeploy.Paginator.ListApplications)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listapplicationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListApplicationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListApplications.html#CodeDeploy.Paginator.ListApplications.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listapplicationspaginator)
        """


if TYPE_CHECKING:
    _ListDeploymentConfigsPaginatorBase = AioPaginator[ListDeploymentConfigsOutputTypeDef]
else:
    _ListDeploymentConfigsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDeploymentConfigsPaginator(_ListDeploymentConfigsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentConfigs.html#CodeDeploy.Paginator.ListDeploymentConfigs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listdeploymentconfigspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeploymentConfigsInputPaginateTypeDef]
    ) -> AioPageIterator[ListDeploymentConfigsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentConfigs.html#CodeDeploy.Paginator.ListDeploymentConfigs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listdeploymentconfigspaginator)
        """


if TYPE_CHECKING:
    _ListDeploymentGroupsPaginatorBase = AioPaginator[ListDeploymentGroupsOutputTypeDef]
else:
    _ListDeploymentGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDeploymentGroupsPaginator(_ListDeploymentGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentGroups.html#CodeDeploy.Paginator.ListDeploymentGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listdeploymentgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeploymentGroupsInputPaginateTypeDef]
    ) -> AioPageIterator[ListDeploymentGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentGroups.html#CodeDeploy.Paginator.ListDeploymentGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listdeploymentgroupspaginator)
        """


if TYPE_CHECKING:
    _ListDeploymentInstancesPaginatorBase = AioPaginator[ListDeploymentInstancesOutputTypeDef]
else:
    _ListDeploymentInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDeploymentInstancesPaginator(_ListDeploymentInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentInstances.html#CodeDeploy.Paginator.ListDeploymentInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listdeploymentinstancespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeploymentInstancesInputPaginateTypeDef]
    ) -> AioPageIterator[ListDeploymentInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentInstances.html#CodeDeploy.Paginator.ListDeploymentInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listdeploymentinstancespaginator)
        """


if TYPE_CHECKING:
    _ListDeploymentTargetsPaginatorBase = AioPaginator[ListDeploymentTargetsOutputTypeDef]
else:
    _ListDeploymentTargetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDeploymentTargetsPaginator(_ListDeploymentTargetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentTargets.html#CodeDeploy.Paginator.ListDeploymentTargets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listdeploymenttargetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeploymentTargetsInputPaginateTypeDef]
    ) -> AioPageIterator[ListDeploymentTargetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentTargets.html#CodeDeploy.Paginator.ListDeploymentTargets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listdeploymenttargetspaginator)
        """


if TYPE_CHECKING:
    _ListDeploymentsPaginatorBase = AioPaginator[ListDeploymentsOutputTypeDef]
else:
    _ListDeploymentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDeploymentsPaginator(_ListDeploymentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeployments.html#CodeDeploy.Paginator.ListDeployments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listdeploymentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeploymentsInputPaginateTypeDef]
    ) -> AioPageIterator[ListDeploymentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeployments.html#CodeDeploy.Paginator.ListDeployments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listdeploymentspaginator)
        """


if TYPE_CHECKING:
    _ListGitHubAccountTokenNamesPaginatorBase = AioPaginator[
        ListGitHubAccountTokenNamesOutputTypeDef
    ]
else:
    _ListGitHubAccountTokenNamesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListGitHubAccountTokenNamesPaginator(_ListGitHubAccountTokenNamesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListGitHubAccountTokenNames.html#CodeDeploy.Paginator.ListGitHubAccountTokenNames)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listgithubaccounttokennamespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGitHubAccountTokenNamesInputPaginateTypeDef]
    ) -> AioPageIterator[ListGitHubAccountTokenNamesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListGitHubAccountTokenNames.html#CodeDeploy.Paginator.ListGitHubAccountTokenNames.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listgithubaccounttokennamespaginator)
        """


if TYPE_CHECKING:
    _ListOnPremisesInstancesPaginatorBase = AioPaginator[ListOnPremisesInstancesOutputTypeDef]
else:
    _ListOnPremisesInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListOnPremisesInstancesPaginator(_ListOnPremisesInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListOnPremisesInstances.html#CodeDeploy.Paginator.ListOnPremisesInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listonpremisesinstancespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOnPremisesInstancesInputPaginateTypeDef]
    ) -> AioPageIterator[ListOnPremisesInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListOnPremisesInstances.html#CodeDeploy.Paginator.ListOnPremisesInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listonpremisesinstancespaginator)
        """
