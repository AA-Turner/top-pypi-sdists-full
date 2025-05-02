"""
Type annotations for proton service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_proton.client import ProtonClient
    from types_aiobotocore_proton.paginator import (
        ListComponentOutputsPaginator,
        ListComponentProvisionedResourcesPaginator,
        ListComponentsPaginator,
        ListDeploymentsPaginator,
        ListEnvironmentAccountConnectionsPaginator,
        ListEnvironmentOutputsPaginator,
        ListEnvironmentProvisionedResourcesPaginator,
        ListEnvironmentTemplateVersionsPaginator,
        ListEnvironmentTemplatesPaginator,
        ListEnvironmentsPaginator,
        ListRepositoriesPaginator,
        ListRepositorySyncDefinitionsPaginator,
        ListServiceInstanceOutputsPaginator,
        ListServiceInstanceProvisionedResourcesPaginator,
        ListServiceInstancesPaginator,
        ListServicePipelineOutputsPaginator,
        ListServicePipelineProvisionedResourcesPaginator,
        ListServiceTemplateVersionsPaginator,
        ListServiceTemplatesPaginator,
        ListServicesPaginator,
        ListTagsForResourcePaginator,
    )

    session = get_session()
    with session.create_client("proton") as client:
        client: ProtonClient

        list_component_outputs_paginator: ListComponentOutputsPaginator = client.get_paginator("list_component_outputs")
        list_component_provisioned_resources_paginator: ListComponentProvisionedResourcesPaginator = client.get_paginator("list_component_provisioned_resources")
        list_components_paginator: ListComponentsPaginator = client.get_paginator("list_components")
        list_deployments_paginator: ListDeploymentsPaginator = client.get_paginator("list_deployments")
        list_environment_account_connections_paginator: ListEnvironmentAccountConnectionsPaginator = client.get_paginator("list_environment_account_connections")
        list_environment_outputs_paginator: ListEnvironmentOutputsPaginator = client.get_paginator("list_environment_outputs")
        list_environment_provisioned_resources_paginator: ListEnvironmentProvisionedResourcesPaginator = client.get_paginator("list_environment_provisioned_resources")
        list_environment_template_versions_paginator: ListEnvironmentTemplateVersionsPaginator = client.get_paginator("list_environment_template_versions")
        list_environment_templates_paginator: ListEnvironmentTemplatesPaginator = client.get_paginator("list_environment_templates")
        list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
        list_repositories_paginator: ListRepositoriesPaginator = client.get_paginator("list_repositories")
        list_repository_sync_definitions_paginator: ListRepositorySyncDefinitionsPaginator = client.get_paginator("list_repository_sync_definitions")
        list_service_instance_outputs_paginator: ListServiceInstanceOutputsPaginator = client.get_paginator("list_service_instance_outputs")
        list_service_instance_provisioned_resources_paginator: ListServiceInstanceProvisionedResourcesPaginator = client.get_paginator("list_service_instance_provisioned_resources")
        list_service_instances_paginator: ListServiceInstancesPaginator = client.get_paginator("list_service_instances")
        list_service_pipeline_outputs_paginator: ListServicePipelineOutputsPaginator = client.get_paginator("list_service_pipeline_outputs")
        list_service_pipeline_provisioned_resources_paginator: ListServicePipelineProvisionedResourcesPaginator = client.get_paginator("list_service_pipeline_provisioned_resources")
        list_service_template_versions_paginator: ListServiceTemplateVersionsPaginator = client.get_paginator("list_service_template_versions")
        list_service_templates_paginator: ListServiceTemplatesPaginator = client.get_paginator("list_service_templates")
        list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListComponentOutputsInputPaginateTypeDef,
    ListComponentOutputsOutputTypeDef,
    ListComponentProvisionedResourcesInputPaginateTypeDef,
    ListComponentProvisionedResourcesOutputTypeDef,
    ListComponentsInputPaginateTypeDef,
    ListComponentsOutputTypeDef,
    ListDeploymentsInputPaginateTypeDef,
    ListDeploymentsOutputTypeDef,
    ListEnvironmentAccountConnectionsInputPaginateTypeDef,
    ListEnvironmentAccountConnectionsOutputTypeDef,
    ListEnvironmentOutputsInputPaginateTypeDef,
    ListEnvironmentOutputsOutputTypeDef,
    ListEnvironmentProvisionedResourcesInputPaginateTypeDef,
    ListEnvironmentProvisionedResourcesOutputTypeDef,
    ListEnvironmentsInputPaginateTypeDef,
    ListEnvironmentsOutputTypeDef,
    ListEnvironmentTemplatesInputPaginateTypeDef,
    ListEnvironmentTemplatesOutputTypeDef,
    ListEnvironmentTemplateVersionsInputPaginateTypeDef,
    ListEnvironmentTemplateVersionsOutputTypeDef,
    ListRepositoriesInputPaginateTypeDef,
    ListRepositoriesOutputTypeDef,
    ListRepositorySyncDefinitionsInputPaginateTypeDef,
    ListRepositorySyncDefinitionsOutputTypeDef,
    ListServiceInstanceOutputsInputPaginateTypeDef,
    ListServiceInstanceOutputsOutputTypeDef,
    ListServiceInstanceProvisionedResourcesInputPaginateTypeDef,
    ListServiceInstanceProvisionedResourcesOutputTypeDef,
    ListServiceInstancesInputPaginateTypeDef,
    ListServiceInstancesOutputTypeDef,
    ListServicePipelineOutputsInputPaginateTypeDef,
    ListServicePipelineOutputsOutputTypeDef,
    ListServicePipelineProvisionedResourcesInputPaginateTypeDef,
    ListServicePipelineProvisionedResourcesOutputTypeDef,
    ListServicesInputPaginateTypeDef,
    ListServicesOutputTypeDef,
    ListServiceTemplatesInputPaginateTypeDef,
    ListServiceTemplatesOutputTypeDef,
    ListServiceTemplateVersionsInputPaginateTypeDef,
    ListServiceTemplateVersionsOutputTypeDef,
    ListTagsForResourceInputPaginateTypeDef,
    ListTagsForResourceOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListComponentOutputsPaginator",
    "ListComponentProvisionedResourcesPaginator",
    "ListComponentsPaginator",
    "ListDeploymentsPaginator",
    "ListEnvironmentAccountConnectionsPaginator",
    "ListEnvironmentOutputsPaginator",
    "ListEnvironmentProvisionedResourcesPaginator",
    "ListEnvironmentTemplateVersionsPaginator",
    "ListEnvironmentTemplatesPaginator",
    "ListEnvironmentsPaginator",
    "ListRepositoriesPaginator",
    "ListRepositorySyncDefinitionsPaginator",
    "ListServiceInstanceOutputsPaginator",
    "ListServiceInstanceProvisionedResourcesPaginator",
    "ListServiceInstancesPaginator",
    "ListServicePipelineOutputsPaginator",
    "ListServicePipelineProvisionedResourcesPaginator",
    "ListServiceTemplateVersionsPaginator",
    "ListServiceTemplatesPaginator",
    "ListServicesPaginator",
    "ListTagsForResourcePaginator",
)


if TYPE_CHECKING:
    _ListComponentOutputsPaginatorBase = AioPaginator[ListComponentOutputsOutputTypeDef]
else:
    _ListComponentOutputsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListComponentOutputsPaginator(_ListComponentOutputsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListComponentOutputs.html#Proton.Paginator.ListComponentOutputs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listcomponentoutputspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListComponentOutputsInputPaginateTypeDef]
    ) -> AioPageIterator[ListComponentOutputsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListComponentOutputs.html#Proton.Paginator.ListComponentOutputs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listcomponentoutputspaginator)
        """


if TYPE_CHECKING:
    _ListComponentProvisionedResourcesPaginatorBase = AioPaginator[
        ListComponentProvisionedResourcesOutputTypeDef
    ]
else:
    _ListComponentProvisionedResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListComponentProvisionedResourcesPaginator(_ListComponentProvisionedResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListComponentProvisionedResources.html#Proton.Paginator.ListComponentProvisionedResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listcomponentprovisionedresourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListComponentProvisionedResourcesInputPaginateTypeDef]
    ) -> AioPageIterator[ListComponentProvisionedResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListComponentProvisionedResources.html#Proton.Paginator.ListComponentProvisionedResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listcomponentprovisionedresourcespaginator)
        """


if TYPE_CHECKING:
    _ListComponentsPaginatorBase = AioPaginator[ListComponentsOutputTypeDef]
else:
    _ListComponentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListComponentsPaginator(_ListComponentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListComponents.html#Proton.Paginator.ListComponents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listcomponentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListComponentsInputPaginateTypeDef]
    ) -> AioPageIterator[ListComponentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListComponents.html#Proton.Paginator.ListComponents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listcomponentspaginator)
        """


if TYPE_CHECKING:
    _ListDeploymentsPaginatorBase = AioPaginator[ListDeploymentsOutputTypeDef]
else:
    _ListDeploymentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDeploymentsPaginator(_ListDeploymentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListDeployments.html#Proton.Paginator.ListDeployments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listdeploymentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeploymentsInputPaginateTypeDef]
    ) -> AioPageIterator[ListDeploymentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListDeployments.html#Proton.Paginator.ListDeployments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listdeploymentspaginator)
        """


if TYPE_CHECKING:
    _ListEnvironmentAccountConnectionsPaginatorBase = AioPaginator[
        ListEnvironmentAccountConnectionsOutputTypeDef
    ]
else:
    _ListEnvironmentAccountConnectionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEnvironmentAccountConnectionsPaginator(_ListEnvironmentAccountConnectionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironmentAccountConnections.html#Proton.Paginator.ListEnvironmentAccountConnections)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmentaccountconnectionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentAccountConnectionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListEnvironmentAccountConnectionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironmentAccountConnections.html#Proton.Paginator.ListEnvironmentAccountConnections.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmentaccountconnectionspaginator)
        """


if TYPE_CHECKING:
    _ListEnvironmentOutputsPaginatorBase = AioPaginator[ListEnvironmentOutputsOutputTypeDef]
else:
    _ListEnvironmentOutputsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEnvironmentOutputsPaginator(_ListEnvironmentOutputsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironmentOutputs.html#Proton.Paginator.ListEnvironmentOutputs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmentoutputspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentOutputsInputPaginateTypeDef]
    ) -> AioPageIterator[ListEnvironmentOutputsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironmentOutputs.html#Proton.Paginator.ListEnvironmentOutputs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmentoutputspaginator)
        """


if TYPE_CHECKING:
    _ListEnvironmentProvisionedResourcesPaginatorBase = AioPaginator[
        ListEnvironmentProvisionedResourcesOutputTypeDef
    ]
else:
    _ListEnvironmentProvisionedResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEnvironmentProvisionedResourcesPaginator(
    _ListEnvironmentProvisionedResourcesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironmentProvisionedResources.html#Proton.Paginator.ListEnvironmentProvisionedResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmentprovisionedresourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentProvisionedResourcesInputPaginateTypeDef]
    ) -> AioPageIterator[ListEnvironmentProvisionedResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironmentProvisionedResources.html#Proton.Paginator.ListEnvironmentProvisionedResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmentprovisionedresourcespaginator)
        """


if TYPE_CHECKING:
    _ListEnvironmentTemplateVersionsPaginatorBase = AioPaginator[
        ListEnvironmentTemplateVersionsOutputTypeDef
    ]
else:
    _ListEnvironmentTemplateVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEnvironmentTemplateVersionsPaginator(_ListEnvironmentTemplateVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironmentTemplateVersions.html#Proton.Paginator.ListEnvironmentTemplateVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmenttemplateversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentTemplateVersionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListEnvironmentTemplateVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironmentTemplateVersions.html#Proton.Paginator.ListEnvironmentTemplateVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmenttemplateversionspaginator)
        """


if TYPE_CHECKING:
    _ListEnvironmentTemplatesPaginatorBase = AioPaginator[ListEnvironmentTemplatesOutputTypeDef]
else:
    _ListEnvironmentTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEnvironmentTemplatesPaginator(_ListEnvironmentTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironmentTemplates.html#Proton.Paginator.ListEnvironmentTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmenttemplatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentTemplatesInputPaginateTypeDef]
    ) -> AioPageIterator[ListEnvironmentTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironmentTemplates.html#Proton.Paginator.ListEnvironmentTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmenttemplatespaginator)
        """


if TYPE_CHECKING:
    _ListEnvironmentsPaginatorBase = AioPaginator[ListEnvironmentsOutputTypeDef]
else:
    _ListEnvironmentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEnvironmentsPaginator(_ListEnvironmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironments.html#Proton.Paginator.ListEnvironments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentsInputPaginateTypeDef]
    ) -> AioPageIterator[ListEnvironmentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironments.html#Proton.Paginator.ListEnvironments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmentspaginator)
        """


if TYPE_CHECKING:
    _ListRepositoriesPaginatorBase = AioPaginator[ListRepositoriesOutputTypeDef]
else:
    _ListRepositoriesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRepositoriesPaginator(_ListRepositoriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListRepositories.html#Proton.Paginator.ListRepositories)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listrepositoriespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRepositoriesInputPaginateTypeDef]
    ) -> AioPageIterator[ListRepositoriesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListRepositories.html#Proton.Paginator.ListRepositories.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listrepositoriespaginator)
        """


if TYPE_CHECKING:
    _ListRepositorySyncDefinitionsPaginatorBase = AioPaginator[
        ListRepositorySyncDefinitionsOutputTypeDef
    ]
else:
    _ListRepositorySyncDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRepositorySyncDefinitionsPaginator(_ListRepositorySyncDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListRepositorySyncDefinitions.html#Proton.Paginator.ListRepositorySyncDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listrepositorysyncdefinitionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRepositorySyncDefinitionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListRepositorySyncDefinitionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListRepositorySyncDefinitions.html#Proton.Paginator.ListRepositorySyncDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listrepositorysyncdefinitionspaginator)
        """


if TYPE_CHECKING:
    _ListServiceInstanceOutputsPaginatorBase = AioPaginator[ListServiceInstanceOutputsOutputTypeDef]
else:
    _ListServiceInstanceOutputsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListServiceInstanceOutputsPaginator(_ListServiceInstanceOutputsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServiceInstanceOutputs.html#Proton.Paginator.ListServiceInstanceOutputs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listserviceinstanceoutputspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceInstanceOutputsInputPaginateTypeDef]
    ) -> AioPageIterator[ListServiceInstanceOutputsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServiceInstanceOutputs.html#Proton.Paginator.ListServiceInstanceOutputs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listserviceinstanceoutputspaginator)
        """


if TYPE_CHECKING:
    _ListServiceInstanceProvisionedResourcesPaginatorBase = AioPaginator[
        ListServiceInstanceProvisionedResourcesOutputTypeDef
    ]
else:
    _ListServiceInstanceProvisionedResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListServiceInstanceProvisionedResourcesPaginator(
    _ListServiceInstanceProvisionedResourcesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServiceInstanceProvisionedResources.html#Proton.Paginator.ListServiceInstanceProvisionedResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listserviceinstanceprovisionedresourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceInstanceProvisionedResourcesInputPaginateTypeDef]
    ) -> AioPageIterator[ListServiceInstanceProvisionedResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServiceInstanceProvisionedResources.html#Proton.Paginator.ListServiceInstanceProvisionedResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listserviceinstanceprovisionedresourcespaginator)
        """


if TYPE_CHECKING:
    _ListServiceInstancesPaginatorBase = AioPaginator[ListServiceInstancesOutputTypeDef]
else:
    _ListServiceInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListServiceInstancesPaginator(_ListServiceInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServiceInstances.html#Proton.Paginator.ListServiceInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listserviceinstancespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceInstancesInputPaginateTypeDef]
    ) -> AioPageIterator[ListServiceInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServiceInstances.html#Proton.Paginator.ListServiceInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listserviceinstancespaginator)
        """


if TYPE_CHECKING:
    _ListServicePipelineOutputsPaginatorBase = AioPaginator[ListServicePipelineOutputsOutputTypeDef]
else:
    _ListServicePipelineOutputsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListServicePipelineOutputsPaginator(_ListServicePipelineOutputsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServicePipelineOutputs.html#Proton.Paginator.ListServicePipelineOutputs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listservicepipelineoutputspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServicePipelineOutputsInputPaginateTypeDef]
    ) -> AioPageIterator[ListServicePipelineOutputsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServicePipelineOutputs.html#Proton.Paginator.ListServicePipelineOutputs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listservicepipelineoutputspaginator)
        """


if TYPE_CHECKING:
    _ListServicePipelineProvisionedResourcesPaginatorBase = AioPaginator[
        ListServicePipelineProvisionedResourcesOutputTypeDef
    ]
else:
    _ListServicePipelineProvisionedResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListServicePipelineProvisionedResourcesPaginator(
    _ListServicePipelineProvisionedResourcesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServicePipelineProvisionedResources.html#Proton.Paginator.ListServicePipelineProvisionedResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listservicepipelineprovisionedresourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServicePipelineProvisionedResourcesInputPaginateTypeDef]
    ) -> AioPageIterator[ListServicePipelineProvisionedResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServicePipelineProvisionedResources.html#Proton.Paginator.ListServicePipelineProvisionedResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listservicepipelineprovisionedresourcespaginator)
        """


if TYPE_CHECKING:
    _ListServiceTemplateVersionsPaginatorBase = AioPaginator[
        ListServiceTemplateVersionsOutputTypeDef
    ]
else:
    _ListServiceTemplateVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListServiceTemplateVersionsPaginator(_ListServiceTemplateVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServiceTemplateVersions.html#Proton.Paginator.ListServiceTemplateVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listservicetemplateversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceTemplateVersionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListServiceTemplateVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServiceTemplateVersions.html#Proton.Paginator.ListServiceTemplateVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listservicetemplateversionspaginator)
        """


if TYPE_CHECKING:
    _ListServiceTemplatesPaginatorBase = AioPaginator[ListServiceTemplatesOutputTypeDef]
else:
    _ListServiceTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListServiceTemplatesPaginator(_ListServiceTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServiceTemplates.html#Proton.Paginator.ListServiceTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listservicetemplatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceTemplatesInputPaginateTypeDef]
    ) -> AioPageIterator[ListServiceTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServiceTemplates.html#Proton.Paginator.ListServiceTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listservicetemplatespaginator)
        """


if TYPE_CHECKING:
    _ListServicesPaginatorBase = AioPaginator[ListServicesOutputTypeDef]
else:
    _ListServicesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListServicesPaginator(_ListServicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServices.html#Proton.Paginator.ListServices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listservicespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServicesInputPaginateTypeDef]
    ) -> AioPageIterator[ListServicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServices.html#Proton.Paginator.ListServices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listservicespaginator)
        """


if TYPE_CHECKING:
    _ListTagsForResourcePaginatorBase = AioPaginator[ListTagsForResourceOutputTypeDef]
else:
    _ListTagsForResourcePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTagsForResourcePaginator(_ListTagsForResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListTagsForResource.html#Proton.Paginator.ListTagsForResource)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listtagsforresourcepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsForResourceInputPaginateTypeDef]
    ) -> AioPageIterator[ListTagsForResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListTagsForResource.html#Proton.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listtagsforresourcepaginator)
        """
