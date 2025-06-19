"""
Type annotations for imagebuilder service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_imagebuilder.client import ImagebuilderClient
    from mypy_boto3_imagebuilder.paginator import (
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

    session = Session()
    client: ImagebuilderClient = session.client("imagebuilder")

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

from botocore.paginate import PageIterator, Paginator

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
    _ListComponentBuildVersionsPaginatorBase = Paginator[ListComponentBuildVersionsResponseTypeDef]
else:
    _ListComponentBuildVersionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListComponentBuildVersionsPaginator(_ListComponentBuildVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListComponentBuildVersions.html#Imagebuilder.Paginator.ListComponentBuildVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listcomponentbuildversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListComponentBuildVersionsRequestPaginateTypeDef]
    ) -> PageIterator[ListComponentBuildVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListComponentBuildVersions.html#Imagebuilder.Paginator.ListComponentBuildVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listcomponentbuildversionspaginator)
        """


if TYPE_CHECKING:
    _ListComponentsPaginatorBase = Paginator[ListComponentsResponseTypeDef]
else:
    _ListComponentsPaginatorBase = Paginator  # type: ignore[assignment]


class ListComponentsPaginator(_ListComponentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListComponents.html#Imagebuilder.Paginator.ListComponents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listcomponentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListComponentsRequestPaginateTypeDef]
    ) -> PageIterator[ListComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListComponents.html#Imagebuilder.Paginator.ListComponents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listcomponentspaginator)
        """


if TYPE_CHECKING:
    _ListContainerRecipesPaginatorBase = Paginator[ListContainerRecipesResponseTypeDef]
else:
    _ListContainerRecipesPaginatorBase = Paginator  # type: ignore[assignment]


class ListContainerRecipesPaginator(_ListContainerRecipesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListContainerRecipes.html#Imagebuilder.Paginator.ListContainerRecipes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listcontainerrecipespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListContainerRecipesRequestPaginateTypeDef]
    ) -> PageIterator[ListContainerRecipesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListContainerRecipes.html#Imagebuilder.Paginator.ListContainerRecipes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listcontainerrecipespaginator)
        """


if TYPE_CHECKING:
    _ListDistributionConfigurationsPaginatorBase = Paginator[
        ListDistributionConfigurationsResponseTypeDef
    ]
else:
    _ListDistributionConfigurationsPaginatorBase = Paginator  # type: ignore[assignment]


class ListDistributionConfigurationsPaginator(_ListDistributionConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListDistributionConfigurations.html#Imagebuilder.Paginator.ListDistributionConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listdistributionconfigurationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDistributionConfigurationsRequestPaginateTypeDef]
    ) -> PageIterator[ListDistributionConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListDistributionConfigurations.html#Imagebuilder.Paginator.ListDistributionConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listdistributionconfigurationspaginator)
        """


if TYPE_CHECKING:
    _ListImageBuildVersionsPaginatorBase = Paginator[ListImageBuildVersionsResponseTypeDef]
else:
    _ListImageBuildVersionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListImageBuildVersionsPaginator(_ListImageBuildVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImageBuildVersions.html#Imagebuilder.Paginator.ListImageBuildVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listimagebuildversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImageBuildVersionsRequestPaginateTypeDef]
    ) -> PageIterator[ListImageBuildVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImageBuildVersions.html#Imagebuilder.Paginator.ListImageBuildVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listimagebuildversionspaginator)
        """


if TYPE_CHECKING:
    _ListImagePackagesPaginatorBase = Paginator[ListImagePackagesResponseTypeDef]
else:
    _ListImagePackagesPaginatorBase = Paginator  # type: ignore[assignment]


class ListImagePackagesPaginator(_ListImagePackagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImagePackages.html#Imagebuilder.Paginator.ListImagePackages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listimagepackagespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImagePackagesRequestPaginateTypeDef]
    ) -> PageIterator[ListImagePackagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImagePackages.html#Imagebuilder.Paginator.ListImagePackages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listimagepackagespaginator)
        """


if TYPE_CHECKING:
    _ListImagePipelineImagesPaginatorBase = Paginator[ListImagePipelineImagesResponseTypeDef]
else:
    _ListImagePipelineImagesPaginatorBase = Paginator  # type: ignore[assignment]


class ListImagePipelineImagesPaginator(_ListImagePipelineImagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImagePipelineImages.html#Imagebuilder.Paginator.ListImagePipelineImages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listimagepipelineimagespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImagePipelineImagesRequestPaginateTypeDef]
    ) -> PageIterator[ListImagePipelineImagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImagePipelineImages.html#Imagebuilder.Paginator.ListImagePipelineImages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listimagepipelineimagespaginator)
        """


if TYPE_CHECKING:
    _ListImagePipelinesPaginatorBase = Paginator[ListImagePipelinesResponseTypeDef]
else:
    _ListImagePipelinesPaginatorBase = Paginator  # type: ignore[assignment]


class ListImagePipelinesPaginator(_ListImagePipelinesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImagePipelines.html#Imagebuilder.Paginator.ListImagePipelines)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listimagepipelinespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImagePipelinesRequestPaginateTypeDef]
    ) -> PageIterator[ListImagePipelinesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImagePipelines.html#Imagebuilder.Paginator.ListImagePipelines.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listimagepipelinespaginator)
        """


if TYPE_CHECKING:
    _ListImageRecipesPaginatorBase = Paginator[ListImageRecipesResponseTypeDef]
else:
    _ListImageRecipesPaginatorBase = Paginator  # type: ignore[assignment]


class ListImageRecipesPaginator(_ListImageRecipesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImageRecipes.html#Imagebuilder.Paginator.ListImageRecipes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listimagerecipespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImageRecipesRequestPaginateTypeDef]
    ) -> PageIterator[ListImageRecipesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImageRecipes.html#Imagebuilder.Paginator.ListImageRecipes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listimagerecipespaginator)
        """


if TYPE_CHECKING:
    _ListImageScanFindingAggregationsPaginatorBase = Paginator[
        ListImageScanFindingAggregationsResponseTypeDef
    ]
else:
    _ListImageScanFindingAggregationsPaginatorBase = Paginator  # type: ignore[assignment]


class ListImageScanFindingAggregationsPaginator(_ListImageScanFindingAggregationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImageScanFindingAggregations.html#Imagebuilder.Paginator.ListImageScanFindingAggregations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listimagescanfindingaggregationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImageScanFindingAggregationsRequestPaginateTypeDef]
    ) -> PageIterator[ListImageScanFindingAggregationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImageScanFindingAggregations.html#Imagebuilder.Paginator.ListImageScanFindingAggregations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listimagescanfindingaggregationspaginator)
        """


if TYPE_CHECKING:
    _ListImageScanFindingsPaginatorBase = Paginator[ListImageScanFindingsResponseTypeDef]
else:
    _ListImageScanFindingsPaginatorBase = Paginator  # type: ignore[assignment]


class ListImageScanFindingsPaginator(_ListImageScanFindingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImageScanFindings.html#Imagebuilder.Paginator.ListImageScanFindings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listimagescanfindingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImageScanFindingsRequestPaginateTypeDef]
    ) -> PageIterator[ListImageScanFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImageScanFindings.html#Imagebuilder.Paginator.ListImageScanFindings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listimagescanfindingspaginator)
        """


if TYPE_CHECKING:
    _ListImagesPaginatorBase = Paginator[ListImagesResponseTypeDef]
else:
    _ListImagesPaginatorBase = Paginator  # type: ignore[assignment]


class ListImagesPaginator(_ListImagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImages.html#Imagebuilder.Paginator.ListImages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listimagespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImagesRequestPaginateTypeDef]
    ) -> PageIterator[ListImagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListImages.html#Imagebuilder.Paginator.ListImages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listimagespaginator)
        """


if TYPE_CHECKING:
    _ListInfrastructureConfigurationsPaginatorBase = Paginator[
        ListInfrastructureConfigurationsResponseTypeDef
    ]
else:
    _ListInfrastructureConfigurationsPaginatorBase = Paginator  # type: ignore[assignment]


class ListInfrastructureConfigurationsPaginator(_ListInfrastructureConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListInfrastructureConfigurations.html#Imagebuilder.Paginator.ListInfrastructureConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listinfrastructureconfigurationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInfrastructureConfigurationsRequestPaginateTypeDef]
    ) -> PageIterator[ListInfrastructureConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListInfrastructureConfigurations.html#Imagebuilder.Paginator.ListInfrastructureConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listinfrastructureconfigurationspaginator)
        """


if TYPE_CHECKING:
    _ListLifecycleExecutionResourcesPaginatorBase = Paginator[
        ListLifecycleExecutionResourcesResponseTypeDef
    ]
else:
    _ListLifecycleExecutionResourcesPaginatorBase = Paginator  # type: ignore[assignment]


class ListLifecycleExecutionResourcesPaginator(_ListLifecycleExecutionResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListLifecycleExecutionResources.html#Imagebuilder.Paginator.ListLifecycleExecutionResources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listlifecycleexecutionresourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLifecycleExecutionResourcesRequestPaginateTypeDef]
    ) -> PageIterator[ListLifecycleExecutionResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListLifecycleExecutionResources.html#Imagebuilder.Paginator.ListLifecycleExecutionResources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listlifecycleexecutionresourcespaginator)
        """


if TYPE_CHECKING:
    _ListLifecycleExecutionsPaginatorBase = Paginator[ListLifecycleExecutionsResponseTypeDef]
else:
    _ListLifecycleExecutionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListLifecycleExecutionsPaginator(_ListLifecycleExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListLifecycleExecutions.html#Imagebuilder.Paginator.ListLifecycleExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listlifecycleexecutionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLifecycleExecutionsRequestPaginateTypeDef]
    ) -> PageIterator[ListLifecycleExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListLifecycleExecutions.html#Imagebuilder.Paginator.ListLifecycleExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listlifecycleexecutionspaginator)
        """


if TYPE_CHECKING:
    _ListLifecyclePoliciesPaginatorBase = Paginator[ListLifecyclePoliciesResponseTypeDef]
else:
    _ListLifecyclePoliciesPaginatorBase = Paginator  # type: ignore[assignment]


class ListLifecyclePoliciesPaginator(_ListLifecyclePoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListLifecyclePolicies.html#Imagebuilder.Paginator.ListLifecyclePolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listlifecyclepoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLifecyclePoliciesRequestPaginateTypeDef]
    ) -> PageIterator[ListLifecyclePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListLifecyclePolicies.html#Imagebuilder.Paginator.ListLifecyclePolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listlifecyclepoliciespaginator)
        """


if TYPE_CHECKING:
    _ListWaitingWorkflowStepsPaginatorBase = Paginator[ListWaitingWorkflowStepsResponseTypeDef]
else:
    _ListWaitingWorkflowStepsPaginatorBase = Paginator  # type: ignore[assignment]


class ListWaitingWorkflowStepsPaginator(_ListWaitingWorkflowStepsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWaitingWorkflowSteps.html#Imagebuilder.Paginator.ListWaitingWorkflowSteps)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listwaitingworkflowstepspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWaitingWorkflowStepsRequestPaginateTypeDef]
    ) -> PageIterator[ListWaitingWorkflowStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWaitingWorkflowSteps.html#Imagebuilder.Paginator.ListWaitingWorkflowSteps.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listwaitingworkflowstepspaginator)
        """


if TYPE_CHECKING:
    _ListWorkflowBuildVersionsPaginatorBase = Paginator[ListWorkflowBuildVersionsResponseTypeDef]
else:
    _ListWorkflowBuildVersionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListWorkflowBuildVersionsPaginator(_ListWorkflowBuildVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWorkflowBuildVersions.html#Imagebuilder.Paginator.ListWorkflowBuildVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listworkflowbuildversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkflowBuildVersionsRequestPaginateTypeDef]
    ) -> PageIterator[ListWorkflowBuildVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWorkflowBuildVersions.html#Imagebuilder.Paginator.ListWorkflowBuildVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listworkflowbuildversionspaginator)
        """


if TYPE_CHECKING:
    _ListWorkflowExecutionsPaginatorBase = Paginator[ListWorkflowExecutionsResponseTypeDef]
else:
    _ListWorkflowExecutionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListWorkflowExecutionsPaginator(_ListWorkflowExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWorkflowExecutions.html#Imagebuilder.Paginator.ListWorkflowExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listworkflowexecutionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkflowExecutionsRequestPaginateTypeDef]
    ) -> PageIterator[ListWorkflowExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWorkflowExecutions.html#Imagebuilder.Paginator.ListWorkflowExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listworkflowexecutionspaginator)
        """


if TYPE_CHECKING:
    _ListWorkflowStepExecutionsPaginatorBase = Paginator[ListWorkflowStepExecutionsResponseTypeDef]
else:
    _ListWorkflowStepExecutionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListWorkflowStepExecutionsPaginator(_ListWorkflowStepExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWorkflowStepExecutions.html#Imagebuilder.Paginator.ListWorkflowStepExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listworkflowstepexecutionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkflowStepExecutionsRequestPaginateTypeDef]
    ) -> PageIterator[ListWorkflowStepExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWorkflowStepExecutions.html#Imagebuilder.Paginator.ListWorkflowStepExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listworkflowstepexecutionspaginator)
        """


if TYPE_CHECKING:
    _ListWorkflowsPaginatorBase = Paginator[ListWorkflowsResponseTypeDef]
else:
    _ListWorkflowsPaginatorBase = Paginator  # type: ignore[assignment]


class ListWorkflowsPaginator(_ListWorkflowsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWorkflows.html#Imagebuilder.Paginator.ListWorkflows)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listworkflowspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkflowsRequestPaginateTypeDef]
    ) -> PageIterator[ListWorkflowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/paginator/ListWorkflows.html#Imagebuilder.Paginator.ListWorkflows.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/paginators/#listworkflowspaginator)
        """
