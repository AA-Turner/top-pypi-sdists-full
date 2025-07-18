"""
Type annotations for imagebuilder service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_imagebuilder.client import ImagebuilderClient
    from types_aiobotocore_imagebuilder.paginator import (
        ListComponentBuildVersionsPaginator,
        ListComponentsPaginator,
        ListContainerRecipesPaginator,
        ListDistributionConfigurationsPaginator,
        ListImageBuildVersionsPaginator,
        ListImagePackagesPaginator,
        ListImagePipelineImagesPaginator,
        ListImagePipelinesPaginator,
        ListImageRecipesPaginator,
        ListImageScanFindingAggregationsPaginator,
        ListImageScanFindingsPaginator,
        ListImagesPaginator,
        ListInfrastructureConfigurationsPaginator,
        ListLifecycleExecutionResourcesPaginator,
        ListLifecycleExecutionsPaginator,
        ListLifecyclePoliciesPaginator,
        ListWaitingWorkflowStepsPaginator,
        ListWorkflowBuildVersionsPaginator,
        ListWorkflowExecutionsPaginator,
        ListWorkflowStepExecutionsPaginator,
        ListWorkflowsPaginator,
    )

    session = get_session()
    with session.create_client("imagebuilder") as client:
        client: ImagebuilderClient

        list_component_build_versions_paginator: ListComponentBuildVersionsPaginator = client.get_paginator("list_component_build_versions")
        list_components_paginator: ListComponentsPaginator = client.get_paginator("list_components")
        list_container_recipes_paginator: ListContainerRecipesPaginator = client.get_paginator("list_container_recipes")
        list_distribution_configurations_paginator: ListDistributionConfigurationsPaginator = client.get_paginator("list_distribution_configurations")
        list_image_build_versions_paginator: ListImageBuildVersionsPaginator = client.get_paginator("list_image_build_versions")
        list_image_packages_paginator: ListImagePackagesPaginator = client.get_paginator("list_image_packages")
        list_image_pipeline_images_paginator: ListImagePipelineImagesPaginator = client.get_paginator("list_image_pipeline_images")
        list_image_pipelines_paginator: ListImagePipelinesPaginator = client.get_paginator("list_image_pipelines")
        list_image_recipes_paginator: ListImageRecipesPaginator = client.get_paginator("list_image_recipes")
        list_image_scan_finding_aggregations_paginator: ListImageScanFindingAggregationsPaginator = client.get_paginator("list_image_scan_finding_aggregations")
        list_image_scan_findings_paginator: ListImageScanFindingsPaginator = client.get_paginator("list_image_scan_findings")
        list_images_paginator: ListImagesPaginator = client.get_paginator("list_images")
        list_infrastructure_configurations_paginator: ListInfrastructureConfigurationsPaginator = client.get_paginator("list_infrastructure_configurations")
        list_lifecycle_execution_resources_paginator: ListLifecycleExecutionResourcesPaginator = client.get_paginator("list_lifecycle_execution_resources")
        list_lifecycle_executions_paginator: ListLifecycleExecutionsPaginator = client.get_paginator("list_lifecycle_executions")
        list_lifecycle_policies_paginator: ListLifecyclePoliciesPaginator = client.get_paginator("list_lifecycle_policies")
        list_waiting_workflow_steps_paginator: ListWaitingWorkflowStepsPaginator = client.get_paginator("list_waiting_workflow_steps")
        list_workflow_build_versions_paginator: ListWorkflowBuildVersionsPaginator = client.get_paginator("list_workflow_build_versions")
        list_workflow_executions_paginator: ListWorkflowExecutionsPaginator = client.get_paginator("list_workflow_executions")
        list_workflow_step_executions_paginator: ListWorkflowStepExecutionsPaginator = client.get_paginator("list_workflow_step_executions")
        list_workflows_paginator: ListWorkflowsPaginator = client.get_paginator("list_workflows")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListComponentBuildVersionsRequestPaginateTypeDef,
    ListComponentBuildVersionsResponseTypeDef,
    ListComponentsRequestPaginateTypeDef,
    ListComponentsResponseTypeDef,
    ListContainerRecipesRequestPaginateTypeDef,
    ListContainerRecipesResponseTypeDef,
    ListDistributionConfigurationsRequestPaginateTypeDef,
    ListDistributionConfigurationsResponseTypeDef,
    ListImageBuildVersionsRequestPaginateTypeDef,
    ListImageBuildVersionsResponseTypeDef,
    ListImagePackagesRequestPaginateTypeDef,
    ListImagePackagesResponseTypeDef,
    ListImagePipelineImagesRequestPaginateTypeDef,
    ListImagePipelineImagesResponseTypeDef,
    ListImagePipelinesRequestPaginateTypeDef,
    ListImagePipelinesResponseTypeDef,
    ListImageRecipesRequestPaginateTypeDef,
    ListImageRecipesResponseTypeDef,
    ListImageScanFindingAggregationsRequestPaginateTypeDef,
    ListImageScanFindingAggregationsResponseTypeDef,
    ListImageScanFindingsRequestPaginateTypeDef,
    ListImageScanFindingsResponseTypeDef,
    ListImagesRequestPaginateTypeDef,
    ListImagesResponseTypeDef,
    ListInfrastructureConfigurationsRequestPaginateTypeDef,
    ListInfrastructureConfigurationsResponseTypeDef,
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
    ListWorkflowExecutionsRequestPaginateTypeDef,
    ListWorkflowExecutionsResponseTypeDef,
    ListWorkflowsRequestPaginateTypeDef,
    ListWorkflowsResponseTypeDef,
    ListWorkflowStepExecutionsRequestPaginateTypeDef,
    ListWorkflowStepExecutionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListComponentBuildVersionsPaginator",
    "ListComponentsPaginator",
    "ListContainerRecipesPaginator",
    "ListDistributionConfigurationsPaginator",
    "ListImageBuildVersionsPaginator",
    "ListImagePackagesPaginator",
    "ListImagePipelineImagesPaginator",
    "ListImagePipelinesPaginator",
    "ListImageRecipesPaginator",
    "ListImageScanFindingAggregationsPaginator",
    "ListImageScanFindingsPaginator",
    "ListImagesPaginator",
    "ListInfrastructureConfigurationsPaginator",
    "ListLifecycleExecutionResourcesPaginator",
    "ListLifecycleExecutionsPaginator",
    "ListLifecyclePoliciesPaginator",
    "ListWaitingWorkflowStepsPaginator",
    "ListWorkflowBuildVersionsPaginator",
    "ListWorkflowExecutionsPaginator",
    "ListWorkflowStepExecutionsPaginator",
    "ListWorkflowsPaginator",
)

if TYPE_CHECKING:
    _ListComponentBuildVersionsPaginatorBase = AioPaginator[
        ListComponentBuildVersionsResponseTypeDef
    ]
else:
    _ListComponentBuildVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListComponentBuildVersionsPaginator(_ListComponentBuildVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListComponentBuildVersions.html#Imagebuilder.Paginator.ListComponentBuildVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listcomponentbuildversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListComponentBuildVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListComponentBuildVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListComponentBuildVersions.html#Imagebuilder.Paginator.ListComponentBuildVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listcomponentbuildversionspaginator)
        """

if TYPE_CHECKING:
    _ListComponentsPaginatorBase = AioPaginator[ListComponentsResponseTypeDef]
else:
    _ListComponentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListComponentsPaginator(_ListComponentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListComponents.html#Imagebuilder.Paginator.ListComponents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listcomponentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListComponentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListComponents.html#Imagebuilder.Paginator.ListComponents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listcomponentspaginator)
        """

if TYPE_CHECKING:
    _ListContainerRecipesPaginatorBase = AioPaginator[ListContainerRecipesResponseTypeDef]
else:
    _ListContainerRecipesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListContainerRecipesPaginator(_ListContainerRecipesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListContainerRecipes.html#Imagebuilder.Paginator.ListContainerRecipes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listcontainerrecipespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListContainerRecipesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListContainerRecipesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListContainerRecipes.html#Imagebuilder.Paginator.ListContainerRecipes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listcontainerrecipespaginator)
        """

if TYPE_CHECKING:
    _ListDistributionConfigurationsPaginatorBase = AioPaginator[
        ListDistributionConfigurationsResponseTypeDef
    ]
else:
    _ListDistributionConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDistributionConfigurationsPaginator(_ListDistributionConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListDistributionConfigurations.html#Imagebuilder.Paginator.ListDistributionConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listdistributionconfigurationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDistributionConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDistributionConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListDistributionConfigurations.html#Imagebuilder.Paginator.ListDistributionConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listdistributionconfigurationspaginator)
        """

if TYPE_CHECKING:
    _ListImageBuildVersionsPaginatorBase = AioPaginator[ListImageBuildVersionsResponseTypeDef]
else:
    _ListImageBuildVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListImageBuildVersionsPaginator(_ListImageBuildVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImageBuildVersions.html#Imagebuilder.Paginator.ListImageBuildVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listimagebuildversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImageBuildVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListImageBuildVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImageBuildVersions.html#Imagebuilder.Paginator.ListImageBuildVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listimagebuildversionspaginator)
        """

if TYPE_CHECKING:
    _ListImagePackagesPaginatorBase = AioPaginator[ListImagePackagesResponseTypeDef]
else:
    _ListImagePackagesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListImagePackagesPaginator(_ListImagePackagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImagePackages.html#Imagebuilder.Paginator.ListImagePackages)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listimagepackagespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImagePackagesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListImagePackagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImagePackages.html#Imagebuilder.Paginator.ListImagePackages.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listimagepackagespaginator)
        """

if TYPE_CHECKING:
    _ListImagePipelineImagesPaginatorBase = AioPaginator[ListImagePipelineImagesResponseTypeDef]
else:
    _ListImagePipelineImagesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListImagePipelineImagesPaginator(_ListImagePipelineImagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImagePipelineImages.html#Imagebuilder.Paginator.ListImagePipelineImages)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listimagepipelineimagespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImagePipelineImagesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListImagePipelineImagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImagePipelineImages.html#Imagebuilder.Paginator.ListImagePipelineImages.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listimagepipelineimagespaginator)
        """

if TYPE_CHECKING:
    _ListImagePipelinesPaginatorBase = AioPaginator[ListImagePipelinesResponseTypeDef]
else:
    _ListImagePipelinesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListImagePipelinesPaginator(_ListImagePipelinesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImagePipelines.html#Imagebuilder.Paginator.ListImagePipelines)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listimagepipelinespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImagePipelinesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListImagePipelinesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImagePipelines.html#Imagebuilder.Paginator.ListImagePipelines.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listimagepipelinespaginator)
        """

if TYPE_CHECKING:
    _ListImageRecipesPaginatorBase = AioPaginator[ListImageRecipesResponseTypeDef]
else:
    _ListImageRecipesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListImageRecipesPaginator(_ListImageRecipesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImageRecipes.html#Imagebuilder.Paginator.ListImageRecipes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listimagerecipespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImageRecipesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListImageRecipesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImageRecipes.html#Imagebuilder.Paginator.ListImageRecipes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listimagerecipespaginator)
        """

if TYPE_CHECKING:
    _ListImageScanFindingAggregationsPaginatorBase = AioPaginator[
        ListImageScanFindingAggregationsResponseTypeDef
    ]
else:
    _ListImageScanFindingAggregationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListImageScanFindingAggregationsPaginator(_ListImageScanFindingAggregationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImageScanFindingAggregations.html#Imagebuilder.Paginator.ListImageScanFindingAggregations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listimagescanfindingaggregationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImageScanFindingAggregationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListImageScanFindingAggregationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImageScanFindingAggregations.html#Imagebuilder.Paginator.ListImageScanFindingAggregations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listimagescanfindingaggregationspaginator)
        """

if TYPE_CHECKING:
    _ListImageScanFindingsPaginatorBase = AioPaginator[ListImageScanFindingsResponseTypeDef]
else:
    _ListImageScanFindingsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListImageScanFindingsPaginator(_ListImageScanFindingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImageScanFindings.html#Imagebuilder.Paginator.ListImageScanFindings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listimagescanfindingspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImageScanFindingsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListImageScanFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImageScanFindings.html#Imagebuilder.Paginator.ListImageScanFindings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listimagescanfindingspaginator)
        """

if TYPE_CHECKING:
    _ListImagesPaginatorBase = AioPaginator[ListImagesResponseTypeDef]
else:
    _ListImagesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListImagesPaginator(_ListImagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImages.html#Imagebuilder.Paginator.ListImages)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listimagespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImagesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListImagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImages.html#Imagebuilder.Paginator.ListImages.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listimagespaginator)
        """

if TYPE_CHECKING:
    _ListInfrastructureConfigurationsPaginatorBase = AioPaginator[
        ListInfrastructureConfigurationsResponseTypeDef
    ]
else:
    _ListInfrastructureConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListInfrastructureConfigurationsPaginator(_ListInfrastructureConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListInfrastructureConfigurations.html#Imagebuilder.Paginator.ListInfrastructureConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listinfrastructureconfigurationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInfrastructureConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInfrastructureConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListInfrastructureConfigurations.html#Imagebuilder.Paginator.ListInfrastructureConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listinfrastructureconfigurationspaginator)
        """

if TYPE_CHECKING:
    _ListLifecycleExecutionResourcesPaginatorBase = AioPaginator[
        ListLifecycleExecutionResourcesResponseTypeDef
    ]
else:
    _ListLifecycleExecutionResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLifecycleExecutionResourcesPaginator(_ListLifecycleExecutionResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListLifecycleExecutionResources.html#Imagebuilder.Paginator.ListLifecycleExecutionResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listlifecycleexecutionresourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLifecycleExecutionResourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLifecycleExecutionResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListLifecycleExecutionResources.html#Imagebuilder.Paginator.ListLifecycleExecutionResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listlifecycleexecutionresourcespaginator)
        """

if TYPE_CHECKING:
    _ListLifecycleExecutionsPaginatorBase = AioPaginator[ListLifecycleExecutionsResponseTypeDef]
else:
    _ListLifecycleExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLifecycleExecutionsPaginator(_ListLifecycleExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListLifecycleExecutions.html#Imagebuilder.Paginator.ListLifecycleExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listlifecycleexecutionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLifecycleExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLifecycleExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListLifecycleExecutions.html#Imagebuilder.Paginator.ListLifecycleExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listlifecycleexecutionspaginator)
        """

if TYPE_CHECKING:
    _ListLifecyclePoliciesPaginatorBase = AioPaginator[ListLifecyclePoliciesResponseTypeDef]
else:
    _ListLifecyclePoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLifecyclePoliciesPaginator(_ListLifecyclePoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListLifecyclePolicies.html#Imagebuilder.Paginator.ListLifecyclePolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listlifecyclepoliciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLifecyclePoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLifecyclePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListLifecyclePolicies.html#Imagebuilder.Paginator.ListLifecyclePolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listlifecyclepoliciespaginator)
        """

if TYPE_CHECKING:
    _ListWaitingWorkflowStepsPaginatorBase = AioPaginator[ListWaitingWorkflowStepsResponseTypeDef]
else:
    _ListWaitingWorkflowStepsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListWaitingWorkflowStepsPaginator(_ListWaitingWorkflowStepsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWaitingWorkflowSteps.html#Imagebuilder.Paginator.ListWaitingWorkflowSteps)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listwaitingworkflowstepspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWaitingWorkflowStepsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWaitingWorkflowStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWaitingWorkflowSteps.html#Imagebuilder.Paginator.ListWaitingWorkflowSteps.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listwaitingworkflowstepspaginator)
        """

if TYPE_CHECKING:
    _ListWorkflowBuildVersionsPaginatorBase = AioPaginator[ListWorkflowBuildVersionsResponseTypeDef]
else:
    _ListWorkflowBuildVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListWorkflowBuildVersionsPaginator(_ListWorkflowBuildVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWorkflowBuildVersions.html#Imagebuilder.Paginator.ListWorkflowBuildVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listworkflowbuildversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkflowBuildVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkflowBuildVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWorkflowBuildVersions.html#Imagebuilder.Paginator.ListWorkflowBuildVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listworkflowbuildversionspaginator)
        """

if TYPE_CHECKING:
    _ListWorkflowExecutionsPaginatorBase = AioPaginator[ListWorkflowExecutionsResponseTypeDef]
else:
    _ListWorkflowExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListWorkflowExecutionsPaginator(_ListWorkflowExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWorkflowExecutions.html#Imagebuilder.Paginator.ListWorkflowExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listworkflowexecutionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkflowExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkflowExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWorkflowExecutions.html#Imagebuilder.Paginator.ListWorkflowExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listworkflowexecutionspaginator)
        """

if TYPE_CHECKING:
    _ListWorkflowStepExecutionsPaginatorBase = AioPaginator[
        ListWorkflowStepExecutionsResponseTypeDef
    ]
else:
    _ListWorkflowStepExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListWorkflowStepExecutionsPaginator(_ListWorkflowStepExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWorkflowStepExecutions.html#Imagebuilder.Paginator.ListWorkflowStepExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listworkflowstepexecutionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkflowStepExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkflowStepExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWorkflowStepExecutions.html#Imagebuilder.Paginator.ListWorkflowStepExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listworkflowstepexecutionspaginator)
        """

if TYPE_CHECKING:
    _ListWorkflowsPaginatorBase = AioPaginator[ListWorkflowsResponseTypeDef]
else:
    _ListWorkflowsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListWorkflowsPaginator(_ListWorkflowsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWorkflows.html#Imagebuilder.Paginator.ListWorkflows)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listworkflowspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkflowsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkflowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWorkflows.html#Imagebuilder.Paginator.ListWorkflows.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/paginators/#listworkflowspaginator)
        """
