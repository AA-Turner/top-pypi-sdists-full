"""
Type annotations for appconfig service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_appconfig.client import AppConfigClient
    from types_aiobotocore_appconfig.paginator import (
        ListApplicationsPaginator,
        ListConfigurationProfilesPaginator,
        ListDeploymentStrategiesPaginator,
        ListDeploymentsPaginator,
        ListEnvironmentsPaginator,
        ListExperimentDefinitionsPaginator,
        ListExperimentRunEventsPaginator,
        ListExperimentRunsPaginator,
        ListExtensionAssociationsPaginator,
        ListExtensionsPaginator,
        ListHostedConfigurationVersionsPaginator,
    )

    session = get_session()
    with session.create_client("appconfig") as client:
        client: AppConfigClient

        list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
        list_configuration_profiles_paginator: ListConfigurationProfilesPaginator = client.get_paginator("list_configuration_profiles")
        list_deployment_strategies_paginator: ListDeploymentStrategiesPaginator = client.get_paginator("list_deployment_strategies")
        list_deployments_paginator: ListDeploymentsPaginator = client.get_paginator("list_deployments")
        list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
        list_experiment_definitions_paginator: ListExperimentDefinitionsPaginator = client.get_paginator("list_experiment_definitions")
        list_experiment_run_events_paginator: ListExperimentRunEventsPaginator = client.get_paginator("list_experiment_run_events")
        list_experiment_runs_paginator: ListExperimentRunsPaginator = client.get_paginator("list_experiment_runs")
        list_extension_associations_paginator: ListExtensionAssociationsPaginator = client.get_paginator("list_extension_associations")
        list_extensions_paginator: ListExtensionsPaginator = client.get_paginator("list_extensions")
        list_hosted_configuration_versions_paginator: ListHostedConfigurationVersionsPaginator = client.get_paginator("list_hosted_configuration_versions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ApplicationsTypeDef,
    ConfigurationProfilesTypeDef,
    DeploymentStrategiesTypeDef,
    DeploymentsTypeDef,
    EnvironmentsTypeDef,
    ExperimentDefinitionsTypeDef,
    ExperimentRunEventsTypeDef,
    ExperimentRunsTypeDef,
    ExtensionAssociationsTypeDef,
    ExtensionsTypeDef,
    HostedConfigurationVersionsTypeDef,
    ListApplicationsRequestPaginateTypeDef,
    ListConfigurationProfilesRequestPaginateTypeDef,
    ListDeploymentsRequestPaginateTypeDef,
    ListDeploymentStrategiesRequestPaginateTypeDef,
    ListEnvironmentsRequestPaginateTypeDef,
    ListExperimentDefinitionsRequestPaginateTypeDef,
    ListExperimentRunEventsRequestPaginateTypeDef,
    ListExperimentRunsRequestPaginateTypeDef,
    ListExtensionAssociationsRequestPaginateTypeDef,
    ListExtensionsRequestPaginateTypeDef,
    ListHostedConfigurationVersionsRequestPaginateTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListApplicationsPaginator",
    "ListConfigurationProfilesPaginator",
    "ListDeploymentStrategiesPaginator",
    "ListDeploymentsPaginator",
    "ListEnvironmentsPaginator",
    "ListExperimentDefinitionsPaginator",
    "ListExperimentRunEventsPaginator",
    "ListExperimentRunsPaginator",
    "ListExtensionAssociationsPaginator",
    "ListExtensionsPaginator",
    "ListHostedConfigurationVersionsPaginator",
)


if TYPE_CHECKING:
    _ListApplicationsPaginatorBase = AioPaginator[ApplicationsTypeDef]
else:
    _ListApplicationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListApplicationsPaginator(_ListApplicationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListApplications.html#AppConfig.Paginator.ListApplications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listapplicationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ApplicationsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListApplications.html#AppConfig.Paginator.ListApplications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listapplicationspaginator)
        """


if TYPE_CHECKING:
    _ListConfigurationProfilesPaginatorBase = AioPaginator[ConfigurationProfilesTypeDef]
else:
    _ListConfigurationProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListConfigurationProfilesPaginator(_ListConfigurationProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListConfigurationProfiles.html#AppConfig.Paginator.ListConfigurationProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listconfigurationprofilespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConfigurationProfilesRequestPaginateTypeDef]
    ) -> AioPageIterator[ConfigurationProfilesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListConfigurationProfiles.html#AppConfig.Paginator.ListConfigurationProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listconfigurationprofilespaginator)
        """


if TYPE_CHECKING:
    _ListDeploymentStrategiesPaginatorBase = AioPaginator[DeploymentStrategiesTypeDef]
else:
    _ListDeploymentStrategiesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDeploymentStrategiesPaginator(_ListDeploymentStrategiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListDeploymentStrategies.html#AppConfig.Paginator.ListDeploymentStrategies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listdeploymentstrategiespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeploymentStrategiesRequestPaginateTypeDef]
    ) -> AioPageIterator[DeploymentStrategiesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListDeploymentStrategies.html#AppConfig.Paginator.ListDeploymentStrategies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listdeploymentstrategiespaginator)
        """


if TYPE_CHECKING:
    _ListDeploymentsPaginatorBase = AioPaginator[DeploymentsTypeDef]
else:
    _ListDeploymentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDeploymentsPaginator(_ListDeploymentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListDeployments.html#AppConfig.Paginator.ListDeployments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listdeploymentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeploymentsRequestPaginateTypeDef]
    ) -> AioPageIterator[DeploymentsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListDeployments.html#AppConfig.Paginator.ListDeployments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listdeploymentspaginator)
        """


if TYPE_CHECKING:
    _ListEnvironmentsPaginatorBase = AioPaginator[EnvironmentsTypeDef]
else:
    _ListEnvironmentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEnvironmentsPaginator(_ListEnvironmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListEnvironments.html#AppConfig.Paginator.ListEnvironments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listenvironmentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[EnvironmentsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListEnvironments.html#AppConfig.Paginator.ListEnvironments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listenvironmentspaginator)
        """


if TYPE_CHECKING:
    _ListExperimentDefinitionsPaginatorBase = AioPaginator[ExperimentDefinitionsTypeDef]
else:
    _ListExperimentDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListExperimentDefinitionsPaginator(_ListExperimentDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListExperimentDefinitions.html#AppConfig.Paginator.ListExperimentDefinitions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listexperimentdefinitionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExperimentDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ExperimentDefinitionsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListExperimentDefinitions.html#AppConfig.Paginator.ListExperimentDefinitions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listexperimentdefinitionspaginator)
        """


if TYPE_CHECKING:
    _ListExperimentRunEventsPaginatorBase = AioPaginator[ExperimentRunEventsTypeDef]
else:
    _ListExperimentRunEventsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListExperimentRunEventsPaginator(_ListExperimentRunEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListExperimentRunEvents.html#AppConfig.Paginator.ListExperimentRunEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listexperimentruneventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExperimentRunEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[ExperimentRunEventsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListExperimentRunEvents.html#AppConfig.Paginator.ListExperimentRunEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listexperimentruneventspaginator)
        """


if TYPE_CHECKING:
    _ListExperimentRunsPaginatorBase = AioPaginator[ExperimentRunsTypeDef]
else:
    _ListExperimentRunsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListExperimentRunsPaginator(_ListExperimentRunsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListExperimentRuns.html#AppConfig.Paginator.ListExperimentRuns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listexperimentrunspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExperimentRunsRequestPaginateTypeDef]
    ) -> AioPageIterator[ExperimentRunsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListExperimentRuns.html#AppConfig.Paginator.ListExperimentRuns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listexperimentrunspaginator)
        """


if TYPE_CHECKING:
    _ListExtensionAssociationsPaginatorBase = AioPaginator[ExtensionAssociationsTypeDef]
else:
    _ListExtensionAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListExtensionAssociationsPaginator(_ListExtensionAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListExtensionAssociations.html#AppConfig.Paginator.ListExtensionAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listextensionassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExtensionAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ExtensionAssociationsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListExtensionAssociations.html#AppConfig.Paginator.ListExtensionAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listextensionassociationspaginator)
        """


if TYPE_CHECKING:
    _ListExtensionsPaginatorBase = AioPaginator[ExtensionsTypeDef]
else:
    _ListExtensionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListExtensionsPaginator(_ListExtensionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListExtensions.html#AppConfig.Paginator.ListExtensions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listextensionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExtensionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ExtensionsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListExtensions.html#AppConfig.Paginator.ListExtensions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listextensionspaginator)
        """


if TYPE_CHECKING:
    _ListHostedConfigurationVersionsPaginatorBase = AioPaginator[HostedConfigurationVersionsTypeDef]
else:
    _ListHostedConfigurationVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListHostedConfigurationVersionsPaginator(_ListHostedConfigurationVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListHostedConfigurationVersions.html#AppConfig.Paginator.ListHostedConfigurationVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listhostedconfigurationversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListHostedConfigurationVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[HostedConfigurationVersionsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListHostedConfigurationVersions.html#AppConfig.Paginator.ListHostedConfigurationVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/paginators/#listhostedconfigurationversionspaginator)
        """
