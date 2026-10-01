"""
Type annotations for imagebuilder service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_imagebuilder.client import ImagebuilderClient

    session = get_session()
    async with session.create_client("imagebuilder") as client:
        client: ImagebuilderClient
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
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
    ListWorkflowsPaginator,
    ListWorkflowStepExecutionsPaginator,
)
from .type_defs import (
    CancelImageCreationRequestTypeDef,
    CancelImageCreationResponseTypeDef,
    CancelLifecycleExecutionRequestTypeDef,
    CancelLifecycleExecutionResponseTypeDef,
    CreateComponentRequestTypeDef,
    CreateComponentResponseTypeDef,
    CreateContainerRecipeRequestTypeDef,
    CreateContainerRecipeResponseTypeDef,
    CreateDistributionConfigurationRequestTypeDef,
    CreateDistributionConfigurationResponseTypeDef,
    CreateImagePipelineRequestTypeDef,
    CreateImagePipelineResponseTypeDef,
    CreateImageRecipeRequestTypeDef,
    CreateImageRecipeResponseTypeDef,
    CreateImageRequestTypeDef,
    CreateImageResponseTypeDef,
    CreateInfrastructureConfigurationRequestTypeDef,
    CreateInfrastructureConfigurationResponseTypeDef,
    CreateLifecyclePolicyRequestTypeDef,
    CreateLifecyclePolicyResponseTypeDef,
    CreateWorkflowRequestTypeDef,
    CreateWorkflowResponseTypeDef,
    DeleteComponentRequestTypeDef,
    DeleteComponentResponseTypeDef,
    DeleteContainerRecipeRequestTypeDef,
    DeleteContainerRecipeResponseTypeDef,
    DeleteDistributionConfigurationRequestTypeDef,
    DeleteDistributionConfigurationResponseTypeDef,
    DeleteImagePipelineRequestTypeDef,
    DeleteImagePipelineResponseTypeDef,
    DeleteImageRecipeRequestTypeDef,
    DeleteImageRecipeResponseTypeDef,
    DeleteImageRequestTypeDef,
    DeleteImageResponseTypeDef,
    DeleteInfrastructureConfigurationRequestTypeDef,
    DeleteInfrastructureConfigurationResponseTypeDef,
    DeleteLifecyclePolicyRequestTypeDef,
    DeleteLifecyclePolicyResponseTypeDef,
    DeleteWorkflowRequestTypeDef,
    DeleteWorkflowResponseTypeDef,
    DistributeImageRequestTypeDef,
    DistributeImageResponseTypeDef,
    GetComponentPolicyRequestTypeDef,
    GetComponentPolicyResponseTypeDef,
    GetComponentRequestTypeDef,
    GetComponentResponseTypeDef,
    GetContainerRecipePolicyRequestTypeDef,
    GetContainerRecipePolicyResponseTypeDef,
    GetContainerRecipeRequestTypeDef,
    GetContainerRecipeResponseTypeDef,
    GetDistributionConfigurationRequestTypeDef,
    GetDistributionConfigurationResponseTypeDef,
    GetImagePipelineRequestTypeDef,
    GetImagePipelineResponseTypeDef,
    GetImagePolicyRequestTypeDef,
    GetImagePolicyResponseTypeDef,
    GetImageRecipePolicyRequestTypeDef,
    GetImageRecipePolicyResponseTypeDef,
    GetImageRecipeRequestTypeDef,
    GetImageRecipeResponseTypeDef,
    GetImageRequestTypeDef,
    GetImageResponseTypeDef,
    GetInfrastructureConfigurationRequestTypeDef,
    GetInfrastructureConfigurationResponseTypeDef,
    GetLifecycleExecutionRequestTypeDef,
    GetLifecycleExecutionResponseTypeDef,
    GetLifecyclePolicyRequestTypeDef,
    GetLifecyclePolicyResponseTypeDef,
    GetMarketplaceResourceRequestTypeDef,
    GetMarketplaceResourceResponseTypeDef,
    GetWorkflowExecutionRequestTypeDef,
    GetWorkflowExecutionResponseTypeDef,
    GetWorkflowRequestTypeDef,
    GetWorkflowResponseTypeDef,
    GetWorkflowStepExecutionRequestTypeDef,
    GetWorkflowStepExecutionResponseTypeDef,
    ImportComponentRequestTypeDef,
    ImportComponentResponseTypeDef,
    ImportDiskImageRequestTypeDef,
    ImportDiskImageResponseTypeDef,
    ImportVmImageRequestTypeDef,
    ImportVmImageResponseTypeDef,
    ListComponentBuildVersionsRequestTypeDef,
    ListComponentBuildVersionsResponseTypeDef,
    ListComponentsRequestTypeDef,
    ListComponentsResponseTypeDef,
    ListContainerRecipesRequestTypeDef,
    ListContainerRecipesResponseTypeDef,
    ListDistributionConfigurationsRequestTypeDef,
    ListDistributionConfigurationsResponseTypeDef,
    ListImageBuildVersionsRequestTypeDef,
    ListImageBuildVersionsResponseTypeDef,
    ListImagePackagesRequestTypeDef,
    ListImagePackagesResponseTypeDef,
    ListImagePipelineImagesRequestTypeDef,
    ListImagePipelineImagesResponseTypeDef,
    ListImagePipelinesRequestTypeDef,
    ListImagePipelinesResponseTypeDef,
    ListImageRecipesRequestTypeDef,
    ListImageRecipesResponseTypeDef,
    ListImageScanFindingAggregationsRequestTypeDef,
    ListImageScanFindingAggregationsResponseTypeDef,
    ListImageScanFindingsRequestTypeDef,
    ListImageScanFindingsResponseTypeDef,
    ListImagesRequestTypeDef,
    ListImagesResponseTypeDef,
    ListInfrastructureConfigurationsRequestTypeDef,
    ListInfrastructureConfigurationsResponseTypeDef,
    ListLifecycleExecutionResourcesRequestTypeDef,
    ListLifecycleExecutionResourcesResponseTypeDef,
    ListLifecycleExecutionsRequestTypeDef,
    ListLifecycleExecutionsResponseTypeDef,
    ListLifecyclePoliciesRequestTypeDef,
    ListLifecyclePoliciesResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWaitingWorkflowStepsRequestTypeDef,
    ListWaitingWorkflowStepsResponseTypeDef,
    ListWorkflowBuildVersionsRequestTypeDef,
    ListWorkflowBuildVersionsResponseTypeDef,
    ListWorkflowExecutionsRequestTypeDef,
    ListWorkflowExecutionsResponseTypeDef,
    ListWorkflowsRequestTypeDef,
    ListWorkflowsResponseTypeDef,
    ListWorkflowStepExecutionsRequestTypeDef,
    ListWorkflowStepExecutionsResponseTypeDef,
    PutComponentPolicyRequestTypeDef,
    PutComponentPolicyResponseTypeDef,
    PutContainerRecipePolicyRequestTypeDef,
    PutContainerRecipePolicyResponseTypeDef,
    PutImagePolicyRequestTypeDef,
    PutImagePolicyResponseTypeDef,
    PutImageRecipePolicyRequestTypeDef,
    PutImageRecipePolicyResponseTypeDef,
    RetryImageRequestTypeDef,
    RetryImageResponseTypeDef,
    SendWorkflowStepActionRequestTypeDef,
    SendWorkflowStepActionResponseTypeDef,
    StartImagePipelineExecutionRequestTypeDef,
    StartImagePipelineExecutionResponseTypeDef,
    StartResourceStateUpdateRequestTypeDef,
    StartResourceStateUpdateResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateDistributionConfigurationRequestTypeDef,
    UpdateDistributionConfigurationResponseTypeDef,
    UpdateImagePipelineRequestTypeDef,
    UpdateImagePipelineResponseTypeDef,
    UpdateInfrastructureConfigurationRequestTypeDef,
    UpdateInfrastructureConfigurationResponseTypeDef,
    UpdateLifecyclePolicyRequestTypeDef,
    UpdateLifecyclePolicyResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("ImagebuilderClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    CallRateLimitExceededException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ClientException: type[BotocoreClientError]
    DryRunOperationException: type[BotocoreClientError]
    ForbiddenException: type[BotocoreClientError]
    IdempotentParameterMismatchException: type[BotocoreClientError]
    InvalidPaginationTokenException: type[BotocoreClientError]
    InvalidParameterCombinationException: type[BotocoreClientError]
    InvalidParameterException: type[BotocoreClientError]
    InvalidParameterValueException: type[BotocoreClientError]
    InvalidRequestException: type[BotocoreClientError]
    InvalidVersionNumberException: type[BotocoreClientError]
    ResourceAlreadyExistsException: type[BotocoreClientError]
    ResourceDependencyException: type[BotocoreClientError]
    ResourceInUseException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ServiceUnavailableException: type[BotocoreClientError]
    TooManyRequestsException: type[BotocoreClientError]


class ImagebuilderClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ImagebuilderClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#generate_presigned_url)
        """

    async def cancel_image_creation(
        self, **kwargs: Unpack[CancelImageCreationRequestTypeDef]
    ) -> CancelImageCreationResponseTypeDef:
        """
        Cancels the creation of an image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/cancel_image_creation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#cancel_image_creation)
        """

    async def cancel_lifecycle_execution(
        self, **kwargs: Unpack[CancelLifecycleExecutionRequestTypeDef]
    ) -> CancelLifecycleExecutionResponseTypeDef:
        """
        Cancels a lifecycle execution - a single run of lifecycle actions that a
        lifecycle policy or a <a>StartResourceStateUpdate</a> request started.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/cancel_lifecycle_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#cancel_lifecycle_execution)
        """

    async def create_component(
        self, **kwargs: Unpack[CreateComponentRequestTypeDef]
    ) -> CreateComponentResponseTypeDef:
        """
        Creates a new component that can be used to build, validate, test, and assess
        your image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/create_component.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_component)
        """

    async def create_container_recipe(
        self, **kwargs: Unpack[CreateContainerRecipeRequestTypeDef]
    ) -> CreateContainerRecipeResponseTypeDef:
        """
        Creates a new container recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/create_container_recipe.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_container_recipe)
        """

    async def create_distribution_configuration(
        self, **kwargs: Unpack[CreateDistributionConfigurationRequestTypeDef]
    ) -> CreateDistributionConfigurationResponseTypeDef:
        """
        Creates a new distribution configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/create_distribution_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_distribution_configuration)
        """

    async def create_image(
        self, **kwargs: Unpack[CreateImageRequestTypeDef]
    ) -> CreateImageResponseTypeDef:
        """
        Creates a new image along with all configured output resources defined in the
        distribution configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/create_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_image)
        """

    async def create_image_pipeline(
        self, **kwargs: Unpack[CreateImagePipelineRequestTypeDef]
    ) -> CreateImagePipelineResponseTypeDef:
        """
        Creates a new image pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/create_image_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_image_pipeline)
        """

    async def create_image_recipe(
        self, **kwargs: Unpack[CreateImageRecipeRequestTypeDef]
    ) -> CreateImageRecipeResponseTypeDef:
        """
        Creates a new image recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/create_image_recipe.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_image_recipe)
        """

    async def create_infrastructure_configuration(
        self, **kwargs: Unpack[CreateInfrastructureConfigurationRequestTypeDef]
    ) -> CreateInfrastructureConfigurationResponseTypeDef:
        """
        Creates a new infrastructure configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/create_infrastructure_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_infrastructure_configuration)
        """

    async def create_lifecycle_policy(
        self, **kwargs: Unpack[CreateLifecyclePolicyRequestTypeDef]
    ) -> CreateLifecyclePolicyResponseTypeDef:
        """
        Creates a lifecycle policy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/create_lifecycle_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_lifecycle_policy)
        """

    async def create_workflow(
        self, **kwargs: Unpack[CreateWorkflowRequestTypeDef]
    ) -> CreateWorkflowResponseTypeDef:
        """
        Creates a new workflow or a new version of an existing workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/create_workflow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_workflow)
        """

    async def delete_component(
        self, **kwargs: Unpack[DeleteComponentRequestTypeDef]
    ) -> DeleteComponentResponseTypeDef:
        """
        Deletes a component build version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/delete_component.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_component)
        """

    async def delete_container_recipe(
        self, **kwargs: Unpack[DeleteContainerRecipeRequestTypeDef]
    ) -> DeleteContainerRecipeResponseTypeDef:
        """
        Deletes a container recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/delete_container_recipe.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_container_recipe)
        """

    async def delete_distribution_configuration(
        self, **kwargs: Unpack[DeleteDistributionConfigurationRequestTypeDef]
    ) -> DeleteDistributionConfigurationResponseTypeDef:
        """
        Deletes a distribution configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/delete_distribution_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_distribution_configuration)
        """

    async def delete_image(
        self, **kwargs: Unpack[DeleteImageRequestTypeDef]
    ) -> DeleteImageResponseTypeDef:
        """
        Deletes an Image Builder image resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/delete_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_image)
        """

    async def delete_image_pipeline(
        self, **kwargs: Unpack[DeleteImagePipelineRequestTypeDef]
    ) -> DeleteImagePipelineResponseTypeDef:
        """
        Deletes an image pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/delete_image_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_image_pipeline)
        """

    async def delete_image_recipe(
        self, **kwargs: Unpack[DeleteImageRecipeRequestTypeDef]
    ) -> DeleteImageRecipeResponseTypeDef:
        """
        Deletes an image recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/delete_image_recipe.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_image_recipe)
        """

    async def delete_infrastructure_configuration(
        self, **kwargs: Unpack[DeleteInfrastructureConfigurationRequestTypeDef]
    ) -> DeleteInfrastructureConfigurationResponseTypeDef:
        """
        Deletes an infrastructure configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/delete_infrastructure_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_infrastructure_configuration)
        """

    async def delete_lifecycle_policy(
        self, **kwargs: Unpack[DeleteLifecyclePolicyRequestTypeDef]
    ) -> DeleteLifecyclePolicyResponseTypeDef:
        """
        Deletes the specified lifecycle policy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/delete_lifecycle_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_lifecycle_policy)
        """

    async def delete_workflow(
        self, **kwargs: Unpack[DeleteWorkflowRequestTypeDef]
    ) -> DeleteWorkflowResponseTypeDef:
        """
        Deletes a specific workflow resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/delete_workflow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_workflow)
        """

    async def distribute_image(
        self, **kwargs: Unpack[DistributeImageRequestTypeDef]
    ) -> DistributeImageResponseTypeDef:
        """
        Distributes an existing AMI to target Regions and accounts without running the
        full image build process.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/distribute_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#distribute_image)
        """

    async def get_component(
        self, **kwargs: Unpack[GetComponentRequestTypeDef]
    ) -> GetComponentResponseTypeDef:
        """
        Retrieves a component object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_component.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_component)
        """

    async def get_component_policy(
        self, **kwargs: Unpack[GetComponentPolicyRequestTypeDef]
    ) -> GetComponentPolicyResponseTypeDef:
        """
        Retrieves a component policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_component_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_component_policy)
        """

    async def get_container_recipe(
        self, **kwargs: Unpack[GetContainerRecipeRequestTypeDef]
    ) -> GetContainerRecipeResponseTypeDef:
        """
        Retrieves a container recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_container_recipe.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_container_recipe)
        """

    async def get_container_recipe_policy(
        self, **kwargs: Unpack[GetContainerRecipePolicyRequestTypeDef]
    ) -> GetContainerRecipePolicyResponseTypeDef:
        """
        Retrieves the policy for a container recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_container_recipe_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_container_recipe_policy)
        """

    async def get_distribution_configuration(
        self, **kwargs: Unpack[GetDistributionConfigurationRequestTypeDef]
    ) -> GetDistributionConfigurationResponseTypeDef:
        """
        Retrieves a distribution configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_distribution_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_distribution_configuration)
        """

    async def get_image(self, **kwargs: Unpack[GetImageRequestTypeDef]) -> GetImageResponseTypeDef:
        """
        Retrieves an image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_image)
        """

    async def get_image_pipeline(
        self, **kwargs: Unpack[GetImagePipelineRequestTypeDef]
    ) -> GetImagePipelineResponseTypeDef:
        """
        Retrieves an image pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_image_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_image_pipeline)
        """

    async def get_image_policy(
        self, **kwargs: Unpack[GetImagePolicyRequestTypeDef]
    ) -> GetImagePolicyResponseTypeDef:
        """
        Retrieves an image policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_image_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_image_policy)
        """

    async def get_image_recipe(
        self, **kwargs: Unpack[GetImageRecipeRequestTypeDef]
    ) -> GetImageRecipeResponseTypeDef:
        """
        Retrieves an image recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_image_recipe.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_image_recipe)
        """

    async def get_image_recipe_policy(
        self, **kwargs: Unpack[GetImageRecipePolicyRequestTypeDef]
    ) -> GetImageRecipePolicyResponseTypeDef:
        """
        Retrieves an image recipe policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_image_recipe_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_image_recipe_policy)
        """

    async def get_infrastructure_configuration(
        self, **kwargs: Unpack[GetInfrastructureConfigurationRequestTypeDef]
    ) -> GetInfrastructureConfigurationResponseTypeDef:
        """
        Retrieves an infrastructure configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_infrastructure_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_infrastructure_configuration)
        """

    async def get_lifecycle_execution(
        self, **kwargs: Unpack[GetLifecycleExecutionRequestTypeDef]
    ) -> GetLifecycleExecutionResponseTypeDef:
        """
        Retrieves runtime information for a lifecycle execution - a single run of
        lifecycle actions that a lifecycle policy or a <a>StartResourceStateUpdate</a>
        request started.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_lifecycle_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_lifecycle_execution)
        """

    async def get_lifecycle_policy(
        self, **kwargs: Unpack[GetLifecyclePolicyRequestTypeDef]
    ) -> GetLifecyclePolicyResponseTypeDef:
        """
        Retrieves details for the specified image lifecycle policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_lifecycle_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_lifecycle_policy)
        """

    async def get_marketplace_resource(
        self, **kwargs: Unpack[GetMarketplaceResourceRequestTypeDef]
    ) -> GetMarketplaceResourceResponseTypeDef:
        """
        Verifies the subscription and performs resource dependency checks on the
        requested Amazon Web Services Marketplace resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_marketplace_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_marketplace_resource)
        """

    async def get_workflow(
        self, **kwargs: Unpack[GetWorkflowRequestTypeDef]
    ) -> GetWorkflowResponseTypeDef:
        """
        Retrieves a workflow resource object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_workflow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_workflow)
        """

    async def get_workflow_execution(
        self, **kwargs: Unpack[GetWorkflowExecutionRequestTypeDef]
    ) -> GetWorkflowExecutionResponseTypeDef:
        """
        Retrieves runtime information for a specific runtime instance of the workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_workflow_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_workflow_execution)
        """

    async def get_workflow_step_execution(
        self, **kwargs: Unpack[GetWorkflowStepExecutionRequestTypeDef]
    ) -> GetWorkflowStepExecutionResponseTypeDef:
        """
        Retrieves runtime information for a specific runtime instance of the workflow
        step.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_workflow_step_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_workflow_step_execution)
        """

    async def import_component(
        self, **kwargs: Unpack[ImportComponentRequestTypeDef]
    ) -> ImportComponentResponseTypeDef:
        """
        Imports a component and transforms its data into a component document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/import_component.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#import_component)
        """

    async def import_disk_image(
        self, **kwargs: Unpack[ImportDiskImageRequestTypeDef]
    ) -> ImportDiskImageResponseTypeDef:
        """
        Imports a Windows operating system image from a verified Microsoft ISO disk
        file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/import_disk_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#import_disk_image)
        """

    async def import_vm_image(
        self, **kwargs: Unpack[ImportVmImageRequestTypeDef]
    ) -> ImportVmImageResponseTypeDef:
        """
        Creates an Image Builder image resource from an Amazon EC2 VM import task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/import_vm_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#import_vm_image)
        """

    async def list_component_build_versions(
        self, **kwargs: Unpack[ListComponentBuildVersionsRequestTypeDef]
    ) -> ListComponentBuildVersionsResponseTypeDef:
        """
        Returns a list of component build versions for the specified component version
        ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_component_build_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_component_build_versions)
        """

    async def list_components(
        self, **kwargs: Unpack[ListComponentsRequestTypeDef]
    ) -> ListComponentsResponseTypeDef:
        """
        Returns the list of components that you have access to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_components.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_components)
        """

    async def list_container_recipes(
        self, **kwargs: Unpack[ListContainerRecipesRequestTypeDef]
    ) -> ListContainerRecipesResponseTypeDef:
        """
        Returns a list of container recipes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_container_recipes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_container_recipes)
        """

    async def list_distribution_configurations(
        self, **kwargs: Unpack[ListDistributionConfigurationsRequestTypeDef]
    ) -> ListDistributionConfigurationsResponseTypeDef:
        """
        Returns a list of distribution configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_distribution_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_distribution_configurations)
        """

    async def list_image_build_versions(
        self, **kwargs: Unpack[ListImageBuildVersionsRequestTypeDef]
    ) -> ListImageBuildVersionsResponseTypeDef:
        """
        Returns a list of image build versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_image_build_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_image_build_versions)
        """

    async def list_image_packages(
        self, **kwargs: Unpack[ListImagePackagesRequestTypeDef]
    ) -> ListImagePackagesResponseTypeDef:
        """
        Lists the packages that are associated with an image build version, as
        determined by Amazon Web Services Systems Manager Inventory at build time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_image_packages.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_image_packages)
        """

    async def list_image_pipeline_images(
        self, **kwargs: Unpack[ListImagePipelineImagesRequestTypeDef]
    ) -> ListImagePipelineImagesResponseTypeDef:
        """
        Returns a list of images created by the specified pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_image_pipeline_images.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_image_pipeline_images)
        """

    async def list_image_pipelines(
        self, **kwargs: Unpack[ListImagePipelinesRequestTypeDef]
    ) -> ListImagePipelinesResponseTypeDef:
        """
        Returns a list of image pipelines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_image_pipelines.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_image_pipelines)
        """

    async def list_image_recipes(
        self, **kwargs: Unpack[ListImageRecipesRequestTypeDef]
    ) -> ListImageRecipesResponseTypeDef:
        """
        Returns a list of image recipes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_image_recipes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_image_recipes)
        """

    async def list_image_scan_finding_aggregations(
        self, **kwargs: Unpack[ListImageScanFindingAggregationsRequestTypeDef]
    ) -> ListImageScanFindingAggregationsResponseTypeDef:
        """
        Returns a list of image scan aggregations for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_image_scan_finding_aggregations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_image_scan_finding_aggregations)
        """

    async def list_image_scan_findings(
        self, **kwargs: Unpack[ListImageScanFindingsRequestTypeDef]
    ) -> ListImageScanFindingsResponseTypeDef:
        """
        Returns a list of image scan findings for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_image_scan_findings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_image_scan_findings)
        """

    async def list_images(
        self, **kwargs: Unpack[ListImagesRequestTypeDef]
    ) -> ListImagesResponseTypeDef:
        """
        Returns the list of images that you have access to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_images.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_images)
        """

    async def list_infrastructure_configurations(
        self, **kwargs: Unpack[ListInfrastructureConfigurationsRequestTypeDef]
    ) -> ListInfrastructureConfigurationsResponseTypeDef:
        """
        Returns a list of infrastructure configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_infrastructure_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_infrastructure_configurations)
        """

    async def list_lifecycle_execution_resources(
        self, **kwargs: Unpack[ListLifecycleExecutionResourcesRequestTypeDef]
    ) -> ListLifecycleExecutionResourcesResponseTypeDef:
        """
        Lists resources that the runtime instance of the image lifecycle identified for
        lifecycle actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_lifecycle_execution_resources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_lifecycle_execution_resources)
        """

    async def list_lifecycle_executions(
        self, **kwargs: Unpack[ListLifecycleExecutionsRequestTypeDef]
    ) -> ListLifecycleExecutionsResponseTypeDef:
        """
        Retrieves the lifecycle runtime history for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_lifecycle_executions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_lifecycle_executions)
        """

    async def list_lifecycle_policies(
        self, **kwargs: Unpack[ListLifecyclePoliciesRequestTypeDef]
    ) -> ListLifecyclePoliciesResponseTypeDef:
        """
        Retrieves a list of lifecycle policies in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_lifecycle_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_lifecycle_policies)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns the list of tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_tags_for_resource)
        """

    async def list_waiting_workflow_steps(
        self, **kwargs: Unpack[ListWaitingWorkflowStepsRequestTypeDef]
    ) -> ListWaitingWorkflowStepsResponseTypeDef:
        """
        Lists the workflow steps in your Amazon Web Services account that have paused
        at a <code>WaitForAction</code> step, and are waiting for you to respond.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_waiting_workflow_steps.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_waiting_workflow_steps)
        """

    async def list_workflow_build_versions(
        self, **kwargs: Unpack[ListWorkflowBuildVersionsRequestTypeDef]
    ) -> ListWorkflowBuildVersionsResponseTypeDef:
        """
        Returns a list of build versions for a specific workflow resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_workflow_build_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_workflow_build_versions)
        """

    async def list_workflow_executions(
        self, **kwargs: Unpack[ListWorkflowExecutionsRequestTypeDef]
    ) -> ListWorkflowExecutionsResponseTypeDef:
        """
        Returns a list of workflow runtime instance metadata objects for a specific
        image build version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_workflow_executions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_workflow_executions)
        """

    async def list_workflow_step_executions(
        self, **kwargs: Unpack[ListWorkflowStepExecutionsRequestTypeDef]
    ) -> ListWorkflowStepExecutionsResponseTypeDef:
        """
        Returns runtime data for each step in a runtime instance of the workflow that
        you specify in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_workflow_step_executions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_workflow_step_executions)
        """

    async def list_workflows(
        self, **kwargs: Unpack[ListWorkflowsRequestTypeDef]
    ) -> ListWorkflowsResponseTypeDef:
        """
        Lists workflow versions based on filtering parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/list_workflows.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_workflows)
        """

    async def put_component_policy(
        self, **kwargs: Unpack[PutComponentPolicyRequestTypeDef]
    ) -> PutComponentPolicyResponseTypeDef:
        """
        Applies a policy to a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/put_component_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#put_component_policy)
        """

    async def put_container_recipe_policy(
        self, **kwargs: Unpack[PutContainerRecipePolicyRequestTypeDef]
    ) -> PutContainerRecipePolicyResponseTypeDef:
        """
        Applies a policy to a container recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/put_container_recipe_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#put_container_recipe_policy)
        """

    async def put_image_policy(
        self, **kwargs: Unpack[PutImagePolicyRequestTypeDef]
    ) -> PutImagePolicyResponseTypeDef:
        """
        Applies a policy to an image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/put_image_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#put_image_policy)
        """

    async def put_image_recipe_policy(
        self, **kwargs: Unpack[PutImageRecipePolicyRequestTypeDef]
    ) -> PutImageRecipePolicyResponseTypeDef:
        """
        Applies a policy to an image recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/put_image_recipe_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#put_image_recipe_policy)
        """

    async def retry_image(
        self, **kwargs: Unpack[RetryImageRequestTypeDef]
    ) -> RetryImageResponseTypeDef:
        """
        Retries a failed or canceled image build without rebuilding the phases that
        already completed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/retry_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#retry_image)
        """

    async def send_workflow_step_action(
        self, **kwargs: Unpack[SendWorkflowStepActionRequestTypeDef]
    ) -> SendWorkflowStepActionResponseTypeDef:
        """
        Sends an action to a workflow step that has paused at a
        <code>WaitForAction</code> step, so that image creation can continue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/send_workflow_step_action.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#send_workflow_step_action)
        """

    async def start_image_pipeline_execution(
        self, **kwargs: Unpack[StartImagePipelineExecutionRequestTypeDef]
    ) -> StartImagePipelineExecutionResponseTypeDef:
        """
        Manually triggers a pipeline to create an image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/start_image_pipeline_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#start_image_pipeline_execution)
        """

    async def start_resource_state_update(
        self, **kwargs: Unpack[StartResourceStateUpdateRequestTypeDef]
    ) -> StartResourceStateUpdateResponseTypeDef:
        """
        Begins an ad-hoc state change for the specified image build version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/start_resource_state_update.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#start_resource_state_update)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Adds a tag to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Removes a tag from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#untag_resource)
        """

    async def update_distribution_configuration(
        self, **kwargs: Unpack[UpdateDistributionConfigurationRequestTypeDef]
    ) -> UpdateDistributionConfigurationResponseTypeDef:
        """
        Updates a distribution configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/update_distribution_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#update_distribution_configuration)
        """

    async def update_image_pipeline(
        self, **kwargs: Unpack[UpdateImagePipelineRequestTypeDef]
    ) -> UpdateImagePipelineResponseTypeDef:
        """
        Updates an image pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/update_image_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#update_image_pipeline)
        """

    async def update_infrastructure_configuration(
        self, **kwargs: Unpack[UpdateInfrastructureConfigurationRequestTypeDef]
    ) -> UpdateInfrastructureConfigurationResponseTypeDef:
        """
        Updates an infrastructure configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/update_infrastructure_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#update_infrastructure_configuration)
        """

    async def update_lifecycle_policy(
        self, **kwargs: Unpack[UpdateLifecyclePolicyRequestTypeDef]
    ) -> UpdateLifecyclePolicyResponseTypeDef:
        """
        Updates the specified lifecycle policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/update_lifecycle_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#update_lifecycle_policy)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_component_build_versions"]
    ) -> ListComponentBuildVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_components"]
    ) -> ListComponentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_container_recipes"]
    ) -> ListContainerRecipesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_distribution_configurations"]
    ) -> ListDistributionConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_image_build_versions"]
    ) -> ListImageBuildVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_image_packages"]
    ) -> ListImagePackagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_image_pipeline_images"]
    ) -> ListImagePipelineImagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_image_pipelines"]
    ) -> ListImagePipelinesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_image_recipes"]
    ) -> ListImageRecipesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_image_scan_finding_aggregations"]
    ) -> ListImageScanFindingAggregationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_image_scan_findings"]
    ) -> ListImageScanFindingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_images"]
    ) -> ListImagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_infrastructure_configurations"]
    ) -> ListInfrastructureConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_lifecycle_execution_resources"]
    ) -> ListLifecycleExecutionResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_lifecycle_executions"]
    ) -> ListLifecycleExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_lifecycle_policies"]
    ) -> ListLifecyclePoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_waiting_workflow_steps"]
    ) -> ListWaitingWorkflowStepsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_workflow_build_versions"]
    ) -> ListWorkflowBuildVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_workflow_executions"]
    ) -> ListWorkflowExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_workflow_step_executions"]
    ) -> ListWorkflowStepExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_workflows"]
    ) -> ListWorkflowsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/)
        """
