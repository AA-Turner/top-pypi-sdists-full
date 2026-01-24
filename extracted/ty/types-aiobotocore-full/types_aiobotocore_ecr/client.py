"""
Type annotations for ecr service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ecr.client import ECRClient

    session = get_session()
    async with session.create_client("ecr") as client:
        client: ECRClient
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
    DescribeImageScanFindingsPaginator,
    DescribeImagesPaginator,
    DescribePullThroughCacheRulesPaginator,
    DescribeRepositoriesPaginator,
    DescribeRepositoryCreationTemplatesPaginator,
    GetLifecyclePolicyPreviewPaginator,
    ListImagesPaginator,
)
from .type_defs import (
    BatchCheckLayerAvailabilityRequestTypeDef,
    BatchCheckLayerAvailabilityResponseTypeDef,
    BatchDeleteImageRequestTypeDef,
    BatchDeleteImageResponseTypeDef,
    BatchGetImageRequestTypeDef,
    BatchGetImageResponseTypeDef,
    BatchGetRepositoryScanningConfigurationRequestTypeDef,
    BatchGetRepositoryScanningConfigurationResponseTypeDef,
    CompleteLayerUploadRequestTypeDef,
    CompleteLayerUploadResponseTypeDef,
    CreatePullThroughCacheRuleRequestTypeDef,
    CreatePullThroughCacheRuleResponseTypeDef,
    CreateRepositoryCreationTemplateRequestTypeDef,
    CreateRepositoryCreationTemplateResponseTypeDef,
    CreateRepositoryRequestTypeDef,
    CreateRepositoryResponseTypeDef,
    DeleteLifecyclePolicyRequestTypeDef,
    DeleteLifecyclePolicyResponseTypeDef,
    DeletePullThroughCacheRuleRequestTypeDef,
    DeletePullThroughCacheRuleResponseTypeDef,
    DeleteRegistryPolicyResponseTypeDef,
    DeleteRepositoryCreationTemplateRequestTypeDef,
    DeleteRepositoryCreationTemplateResponseTypeDef,
    DeleteRepositoryPolicyRequestTypeDef,
    DeleteRepositoryPolicyResponseTypeDef,
    DeleteRepositoryRequestTypeDef,
    DeleteRepositoryResponseTypeDef,
    DeleteSigningConfigurationResponseTypeDef,
    DeregisterPullTimeUpdateExclusionRequestTypeDef,
    DeregisterPullTimeUpdateExclusionResponseTypeDef,
    DescribeImageReplicationStatusRequestTypeDef,
    DescribeImageReplicationStatusResponseTypeDef,
    DescribeImageScanFindingsRequestTypeDef,
    DescribeImageScanFindingsResponseTypeDef,
    DescribeImageSigningStatusRequestTypeDef,
    DescribeImageSigningStatusResponseTypeDef,
    DescribeImagesRequestTypeDef,
    DescribeImagesResponseTypeDef,
    DescribePullThroughCacheRulesRequestTypeDef,
    DescribePullThroughCacheRulesResponseTypeDef,
    DescribeRegistryResponseTypeDef,
    DescribeRepositoriesRequestTypeDef,
    DescribeRepositoriesResponseTypeDef,
    DescribeRepositoryCreationTemplatesRequestTypeDef,
    DescribeRepositoryCreationTemplatesResponseTypeDef,
    GetAccountSettingRequestTypeDef,
    GetAccountSettingResponseTypeDef,
    GetAuthorizationTokenRequestTypeDef,
    GetAuthorizationTokenResponseTypeDef,
    GetDownloadUrlForLayerRequestTypeDef,
    GetDownloadUrlForLayerResponseTypeDef,
    GetLifecyclePolicyPreviewRequestTypeDef,
    GetLifecyclePolicyPreviewResponseTypeDef,
    GetLifecyclePolicyRequestTypeDef,
    GetLifecyclePolicyResponseTypeDef,
    GetRegistryPolicyResponseTypeDef,
    GetRegistryScanningConfigurationResponseTypeDef,
    GetRepositoryPolicyRequestTypeDef,
    GetRepositoryPolicyResponseTypeDef,
    GetSigningConfigurationResponseTypeDef,
    InitiateLayerUploadRequestTypeDef,
    InitiateLayerUploadResponseTypeDef,
    ListImageReferrersRequestTypeDef,
    ListImageReferrersResponseTypeDef,
    ListImagesRequestTypeDef,
    ListImagesResponseTypeDef,
    ListPullTimeUpdateExclusionsRequestTypeDef,
    ListPullTimeUpdateExclusionsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutAccountSettingRequestTypeDef,
    PutAccountSettingResponseTypeDef,
    PutImageRequestTypeDef,
    PutImageResponseTypeDef,
    PutImageScanningConfigurationRequestTypeDef,
    PutImageScanningConfigurationResponseTypeDef,
    PutImageTagMutabilityRequestTypeDef,
    PutImageTagMutabilityResponseTypeDef,
    PutLifecyclePolicyRequestTypeDef,
    PutLifecyclePolicyResponseTypeDef,
    PutRegistryPolicyRequestTypeDef,
    PutRegistryPolicyResponseTypeDef,
    PutRegistryScanningConfigurationRequestTypeDef,
    PutRegistryScanningConfigurationResponseTypeDef,
    PutReplicationConfigurationRequestTypeDef,
    PutReplicationConfigurationResponseTypeDef,
    PutSigningConfigurationRequestTypeDef,
    PutSigningConfigurationResponseTypeDef,
    RegisterPullTimeUpdateExclusionRequestTypeDef,
    RegisterPullTimeUpdateExclusionResponseTypeDef,
    SetRepositoryPolicyRequestTypeDef,
    SetRepositoryPolicyResponseTypeDef,
    StartImageScanRequestTypeDef,
    StartImageScanResponseTypeDef,
    StartLifecyclePolicyPreviewRequestTypeDef,
    StartLifecyclePolicyPreviewResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateImageStorageClassRequestTypeDef,
    UpdateImageStorageClassResponseTypeDef,
    UpdatePullThroughCacheRuleRequestTypeDef,
    UpdatePullThroughCacheRuleResponseTypeDef,
    UpdateRepositoryCreationTemplateRequestTypeDef,
    UpdateRepositoryCreationTemplateResponseTypeDef,
    UploadLayerPartRequestTypeDef,
    UploadLayerPartResponseTypeDef,
    ValidatePullThroughCacheRuleRequestTypeDef,
    ValidatePullThroughCacheRuleResponseTypeDef,
)
from .waiter import ImageScanCompleteWaiter, LifecyclePolicyPreviewCompleteWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("ECRClient",)


class Exceptions(BaseClientExceptions):
    BlockedByOrganizationPolicyException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    EmptyUploadException: type[BotocoreClientError]
    ExclusionAlreadyExistsException: type[BotocoreClientError]
    ExclusionNotFoundException: type[BotocoreClientError]
    ImageAlreadyExistsException: type[BotocoreClientError]
    ImageArchivedException: type[BotocoreClientError]
    ImageDigestDoesNotMatchException: type[BotocoreClientError]
    ImageNotFoundException: type[BotocoreClientError]
    ImageStorageClassUpdateNotSupportedException: type[BotocoreClientError]
    ImageTagAlreadyExistsException: type[BotocoreClientError]
    InvalidLayerException: type[BotocoreClientError]
    InvalidLayerPartException: type[BotocoreClientError]
    InvalidParameterException: type[BotocoreClientError]
    InvalidTagParameterException: type[BotocoreClientError]
    KmsException: type[BotocoreClientError]
    LayerAlreadyExistsException: type[BotocoreClientError]
    LayerInaccessibleException: type[BotocoreClientError]
    LayerPartTooSmallException: type[BotocoreClientError]
    LayersNotFoundException: type[BotocoreClientError]
    LifecyclePolicyNotFoundException: type[BotocoreClientError]
    LifecyclePolicyPreviewInProgressException: type[BotocoreClientError]
    LifecyclePolicyPreviewNotFoundException: type[BotocoreClientError]
    LimitExceededException: type[BotocoreClientError]
    PullThroughCacheRuleAlreadyExistsException: type[BotocoreClientError]
    PullThroughCacheRuleNotFoundException: type[BotocoreClientError]
    ReferencedImagesNotFoundException: type[BotocoreClientError]
    RegistryPolicyNotFoundException: type[BotocoreClientError]
    RepositoryAlreadyExistsException: type[BotocoreClientError]
    RepositoryNotEmptyException: type[BotocoreClientError]
    RepositoryNotFoundException: type[BotocoreClientError]
    RepositoryPolicyNotFoundException: type[BotocoreClientError]
    ScanNotFoundException: type[BotocoreClientError]
    SecretNotFoundException: type[BotocoreClientError]
    ServerException: type[BotocoreClientError]
    SigningConfigurationNotFoundException: type[BotocoreClientError]
    TemplateAlreadyExistsException: type[BotocoreClientError]
    TemplateNotFoundException: type[BotocoreClientError]
    TooManyTagsException: type[BotocoreClientError]
    UnableToAccessSecretException: type[BotocoreClientError]
    UnableToDecryptSecretValueException: type[BotocoreClientError]
    UnableToGetUpstreamImageException: type[BotocoreClientError]
    UnableToGetUpstreamLayerException: type[BotocoreClientError]
    UnsupportedImageTypeException: type[BotocoreClientError]
    UnsupportedUpstreamRegistryException: type[BotocoreClientError]
    UploadNotFoundException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class ECRClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr.html#ECR.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ECRClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr.html#ECR.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#generate_presigned_url)
        """

    async def batch_check_layer_availability(
        self, **kwargs: Unpack[BatchCheckLayerAvailabilityRequestTypeDef]
    ) -> BatchCheckLayerAvailabilityResponseTypeDef:
        """
        Checks the availability of one or more image layers in a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/batch_check_layer_availability.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#batch_check_layer_availability)
        """

    async def batch_delete_image(
        self, **kwargs: Unpack[BatchDeleteImageRequestTypeDef]
    ) -> BatchDeleteImageResponseTypeDef:
        """
        Deletes a list of specified images within a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/batch_delete_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#batch_delete_image)
        """

    async def batch_get_image(
        self, **kwargs: Unpack[BatchGetImageRequestTypeDef]
    ) -> BatchGetImageResponseTypeDef:
        """
        Gets detailed information for an image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/batch_get_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#batch_get_image)
        """

    async def batch_get_repository_scanning_configuration(
        self, **kwargs: Unpack[BatchGetRepositoryScanningConfigurationRequestTypeDef]
    ) -> BatchGetRepositoryScanningConfigurationResponseTypeDef:
        """
        Gets the scanning configuration for one or more repositories.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/batch_get_repository_scanning_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#batch_get_repository_scanning_configuration)
        """

    async def complete_layer_upload(
        self, **kwargs: Unpack[CompleteLayerUploadRequestTypeDef]
    ) -> CompleteLayerUploadResponseTypeDef:
        """
        Informs Amazon ECR that the image layer upload has completed for a specified
        registry, repository name, and upload ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/complete_layer_upload.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#complete_layer_upload)
        """

    async def create_pull_through_cache_rule(
        self, **kwargs: Unpack[CreatePullThroughCacheRuleRequestTypeDef]
    ) -> CreatePullThroughCacheRuleResponseTypeDef:
        """
        Creates a pull through cache rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/create_pull_through_cache_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#create_pull_through_cache_rule)
        """

    async def create_repository(
        self, **kwargs: Unpack[CreateRepositoryRequestTypeDef]
    ) -> CreateRepositoryResponseTypeDef:
        """
        Creates a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/create_repository.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#create_repository)
        """

    async def create_repository_creation_template(
        self, **kwargs: Unpack[CreateRepositoryCreationTemplateRequestTypeDef]
    ) -> CreateRepositoryCreationTemplateResponseTypeDef:
        """
        Creates a repository creation template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/create_repository_creation_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#create_repository_creation_template)
        """

    async def delete_lifecycle_policy(
        self, **kwargs: Unpack[DeleteLifecyclePolicyRequestTypeDef]
    ) -> DeleteLifecyclePolicyResponseTypeDef:
        """
        Deletes the lifecycle policy associated with the specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/delete_lifecycle_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#delete_lifecycle_policy)
        """

    async def delete_pull_through_cache_rule(
        self, **kwargs: Unpack[DeletePullThroughCacheRuleRequestTypeDef]
    ) -> DeletePullThroughCacheRuleResponseTypeDef:
        """
        Deletes a pull through cache rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/delete_pull_through_cache_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#delete_pull_through_cache_rule)
        """

    async def delete_registry_policy(self) -> DeleteRegistryPolicyResponseTypeDef:
        """
        Deletes the registry permissions policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/delete_registry_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#delete_registry_policy)
        """

    async def delete_repository(
        self, **kwargs: Unpack[DeleteRepositoryRequestTypeDef]
    ) -> DeleteRepositoryResponseTypeDef:
        """
        Deletes a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/delete_repository.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#delete_repository)
        """

    async def delete_repository_creation_template(
        self, **kwargs: Unpack[DeleteRepositoryCreationTemplateRequestTypeDef]
    ) -> DeleteRepositoryCreationTemplateResponseTypeDef:
        """
        Deletes a repository creation template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/delete_repository_creation_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#delete_repository_creation_template)
        """

    async def delete_repository_policy(
        self, **kwargs: Unpack[DeleteRepositoryPolicyRequestTypeDef]
    ) -> DeleteRepositoryPolicyResponseTypeDef:
        """
        Deletes the repository policy associated with the specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/delete_repository_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#delete_repository_policy)
        """

    async def delete_signing_configuration(self) -> DeleteSigningConfigurationResponseTypeDef:
        """
        Deletes the registry's signing configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/delete_signing_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#delete_signing_configuration)
        """

    async def deregister_pull_time_update_exclusion(
        self, **kwargs: Unpack[DeregisterPullTimeUpdateExclusionRequestTypeDef]
    ) -> DeregisterPullTimeUpdateExclusionResponseTypeDef:
        """
        Removes a principal from the pull time update exclusion list for a registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/deregister_pull_time_update_exclusion.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#deregister_pull_time_update_exclusion)
        """

    async def describe_image_replication_status(
        self, **kwargs: Unpack[DescribeImageReplicationStatusRequestTypeDef]
    ) -> DescribeImageReplicationStatusResponseTypeDef:
        """
        Returns the replication status for a specified image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/describe_image_replication_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#describe_image_replication_status)
        """

    async def describe_image_scan_findings(
        self, **kwargs: Unpack[DescribeImageScanFindingsRequestTypeDef]
    ) -> DescribeImageScanFindingsResponseTypeDef:
        """
        Returns the scan findings for the specified image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/describe_image_scan_findings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#describe_image_scan_findings)
        """

    async def describe_image_signing_status(
        self, **kwargs: Unpack[DescribeImageSigningStatusRequestTypeDef]
    ) -> DescribeImageSigningStatusResponseTypeDef:
        """
        Returns the signing status for a specified image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/describe_image_signing_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#describe_image_signing_status)
        """

    async def describe_images(
        self, **kwargs: Unpack[DescribeImagesRequestTypeDef]
    ) -> DescribeImagesResponseTypeDef:
        """
        Returns metadata about the images in a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/describe_images.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#describe_images)
        """

    async def describe_pull_through_cache_rules(
        self, **kwargs: Unpack[DescribePullThroughCacheRulesRequestTypeDef]
    ) -> DescribePullThroughCacheRulesResponseTypeDef:
        """
        Returns the pull through cache rules for a registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/describe_pull_through_cache_rules.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#describe_pull_through_cache_rules)
        """

    async def describe_registry(self) -> DescribeRegistryResponseTypeDef:
        """
        Describes the settings for a registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/describe_registry.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#describe_registry)
        """

    async def describe_repositories(
        self, **kwargs: Unpack[DescribeRepositoriesRequestTypeDef]
    ) -> DescribeRepositoriesResponseTypeDef:
        """
        Describes image repositories in a registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/describe_repositories.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#describe_repositories)
        """

    async def describe_repository_creation_templates(
        self, **kwargs: Unpack[DescribeRepositoryCreationTemplatesRequestTypeDef]
    ) -> DescribeRepositoryCreationTemplatesResponseTypeDef:
        """
        Returns details about the repository creation templates in a registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/describe_repository_creation_templates.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#describe_repository_creation_templates)
        """

    async def get_account_setting(
        self, **kwargs: Unpack[GetAccountSettingRequestTypeDef]
    ) -> GetAccountSettingResponseTypeDef:
        """
        Retrieves the account setting value for the specified setting name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/get_account_setting.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#get_account_setting)
        """

    async def get_authorization_token(
        self, **kwargs: Unpack[GetAuthorizationTokenRequestTypeDef]
    ) -> GetAuthorizationTokenResponseTypeDef:
        """
        Retrieves an authorization token.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/get_authorization_token.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#get_authorization_token)
        """

    async def get_download_url_for_layer(
        self, **kwargs: Unpack[GetDownloadUrlForLayerRequestTypeDef]
    ) -> GetDownloadUrlForLayerResponseTypeDef:
        """
        Retrieves the pre-signed Amazon S3 download URL corresponding to an image layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/get_download_url_for_layer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#get_download_url_for_layer)
        """

    async def get_lifecycle_policy(
        self, **kwargs: Unpack[GetLifecyclePolicyRequestTypeDef]
    ) -> GetLifecyclePolicyResponseTypeDef:
        """
        Retrieves the lifecycle policy for the specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/get_lifecycle_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#get_lifecycle_policy)
        """

    async def get_lifecycle_policy_preview(
        self, **kwargs: Unpack[GetLifecyclePolicyPreviewRequestTypeDef]
    ) -> GetLifecyclePolicyPreviewResponseTypeDef:
        """
        Retrieves the results of the lifecycle policy preview request for the specified
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/get_lifecycle_policy_preview.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#get_lifecycle_policy_preview)
        """

    async def get_registry_policy(self) -> GetRegistryPolicyResponseTypeDef:
        """
        Retrieves the permissions policy for a registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/get_registry_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#get_registry_policy)
        """

    async def get_registry_scanning_configuration(
        self,
    ) -> GetRegistryScanningConfigurationResponseTypeDef:
        """
        Retrieves the scanning configuration for a registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/get_registry_scanning_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#get_registry_scanning_configuration)
        """

    async def get_repository_policy(
        self, **kwargs: Unpack[GetRepositoryPolicyRequestTypeDef]
    ) -> GetRepositoryPolicyResponseTypeDef:
        """
        Retrieves the repository policy for the specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/get_repository_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#get_repository_policy)
        """

    async def get_signing_configuration(self) -> GetSigningConfigurationResponseTypeDef:
        """
        Retrieves the registry's signing configuration, which defines rules for
        automatically signing images using Amazon Web Services Signer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/get_signing_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#get_signing_configuration)
        """

    async def initiate_layer_upload(
        self, **kwargs: Unpack[InitiateLayerUploadRequestTypeDef]
    ) -> InitiateLayerUploadResponseTypeDef:
        """
        Notifies Amazon ECR that you intend to upload an image layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/initiate_layer_upload.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#initiate_layer_upload)
        """

    async def list_image_referrers(
        self, **kwargs: Unpack[ListImageReferrersRequestTypeDef]
    ) -> ListImageReferrersResponseTypeDef:
        """
        Lists the artifacts associated with a specified subject image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/list_image_referrers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#list_image_referrers)
        """

    async def list_images(
        self, **kwargs: Unpack[ListImagesRequestTypeDef]
    ) -> ListImagesResponseTypeDef:
        """
        Lists all the image IDs for the specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/list_images.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#list_images)
        """

    async def list_pull_time_update_exclusions(
        self, **kwargs: Unpack[ListPullTimeUpdateExclusionsRequestTypeDef]
    ) -> ListPullTimeUpdateExclusionsResponseTypeDef:
        """
        Lists the IAM principals that are excluded from having their image pull times
        recorded.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/list_pull_time_update_exclusions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#list_pull_time_update_exclusions)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List the tags for an Amazon ECR resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#list_tags_for_resource)
        """

    async def put_account_setting(
        self, **kwargs: Unpack[PutAccountSettingRequestTypeDef]
    ) -> PutAccountSettingResponseTypeDef:
        """
        Allows you to change the basic scan type version or registry policy scope.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/put_account_setting.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#put_account_setting)
        """

    async def put_image(self, **kwargs: Unpack[PutImageRequestTypeDef]) -> PutImageResponseTypeDef:
        """
        Creates or updates the image manifest and tags associated with an image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/put_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#put_image)
        """

    async def put_image_scanning_configuration(
        self, **kwargs: Unpack[PutImageScanningConfigurationRequestTypeDef]
    ) -> PutImageScanningConfigurationResponseTypeDef:
        """
        The <code>PutImageScanningConfiguration</code> API is being deprecated, in
        favor of specifying the image scanning configuration at the registry level.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/put_image_scanning_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#put_image_scanning_configuration)
        """

    async def put_image_tag_mutability(
        self, **kwargs: Unpack[PutImageTagMutabilityRequestTypeDef]
    ) -> PutImageTagMutabilityResponseTypeDef:
        """
        Updates the image tag mutability settings for the specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/put_image_tag_mutability.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#put_image_tag_mutability)
        """

    async def put_lifecycle_policy(
        self, **kwargs: Unpack[PutLifecyclePolicyRequestTypeDef]
    ) -> PutLifecyclePolicyResponseTypeDef:
        """
        Creates or updates the lifecycle policy for the specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/put_lifecycle_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#put_lifecycle_policy)
        """

    async def put_registry_policy(
        self, **kwargs: Unpack[PutRegistryPolicyRequestTypeDef]
    ) -> PutRegistryPolicyResponseTypeDef:
        """
        Creates or updates the permissions policy for your registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/put_registry_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#put_registry_policy)
        """

    async def put_registry_scanning_configuration(
        self, **kwargs: Unpack[PutRegistryScanningConfigurationRequestTypeDef]
    ) -> PutRegistryScanningConfigurationResponseTypeDef:
        """
        Creates or updates the scanning configuration for your private registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/put_registry_scanning_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#put_registry_scanning_configuration)
        """

    async def put_replication_configuration(
        self, **kwargs: Unpack[PutReplicationConfigurationRequestTypeDef]
    ) -> PutReplicationConfigurationResponseTypeDef:
        """
        Creates or updates the replication configuration for a registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/put_replication_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#put_replication_configuration)
        """

    async def put_signing_configuration(
        self, **kwargs: Unpack[PutSigningConfigurationRequestTypeDef]
    ) -> PutSigningConfigurationResponseTypeDef:
        """
        Creates or updates the registry's signing configuration, which defines rules
        for automatically signing images with Amazon Web Services Signer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/put_signing_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#put_signing_configuration)
        """

    async def register_pull_time_update_exclusion(
        self, **kwargs: Unpack[RegisterPullTimeUpdateExclusionRequestTypeDef]
    ) -> RegisterPullTimeUpdateExclusionResponseTypeDef:
        """
        Adds an IAM principal to the pull time update exclusion list for a registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/register_pull_time_update_exclusion.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#register_pull_time_update_exclusion)
        """

    async def set_repository_policy(
        self, **kwargs: Unpack[SetRepositoryPolicyRequestTypeDef]
    ) -> SetRepositoryPolicyResponseTypeDef:
        """
        Applies a repository policy to the specified repository to control access
        permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/set_repository_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#set_repository_policy)
        """

    async def start_image_scan(
        self, **kwargs: Unpack[StartImageScanRequestTypeDef]
    ) -> StartImageScanResponseTypeDef:
        """
        Starts a basic image vulnerability scan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/start_image_scan.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#start_image_scan)
        """

    async def start_lifecycle_policy_preview(
        self, **kwargs: Unpack[StartLifecyclePolicyPreviewRequestTypeDef]
    ) -> StartLifecyclePolicyPreviewResponseTypeDef:
        """
        Starts a preview of a lifecycle policy for the specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/start_lifecycle_policy_preview.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#start_lifecycle_policy_preview)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Adds specified tags to a resource with the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Deletes specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#untag_resource)
        """

    async def update_image_storage_class(
        self, **kwargs: Unpack[UpdateImageStorageClassRequestTypeDef]
    ) -> UpdateImageStorageClassResponseTypeDef:
        """
        Transitions an image between storage classes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/update_image_storage_class.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#update_image_storage_class)
        """

    async def update_pull_through_cache_rule(
        self, **kwargs: Unpack[UpdatePullThroughCacheRuleRequestTypeDef]
    ) -> UpdatePullThroughCacheRuleResponseTypeDef:
        """
        Updates an existing pull through cache rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/update_pull_through_cache_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#update_pull_through_cache_rule)
        """

    async def update_repository_creation_template(
        self, **kwargs: Unpack[UpdateRepositoryCreationTemplateRequestTypeDef]
    ) -> UpdateRepositoryCreationTemplateResponseTypeDef:
        """
        Updates an existing repository creation template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/update_repository_creation_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#update_repository_creation_template)
        """

    async def upload_layer_part(
        self, **kwargs: Unpack[UploadLayerPartRequestTypeDef]
    ) -> UploadLayerPartResponseTypeDef:
        """
        Uploads an image layer part to Amazon ECR.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/upload_layer_part.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#upload_layer_part)
        """

    async def validate_pull_through_cache_rule(
        self, **kwargs: Unpack[ValidatePullThroughCacheRuleRequestTypeDef]
    ) -> ValidatePullThroughCacheRuleResponseTypeDef:
        """
        Validates an existing pull through cache rule for an upstream registry that
        requires authentication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/validate_pull_through_cache_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#validate_pull_through_cache_rule)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_image_scan_findings"]
    ) -> DescribeImageScanFindingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_images"]
    ) -> DescribeImagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_pull_through_cache_rules"]
    ) -> DescribePullThroughCacheRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_repositories"]
    ) -> DescribeRepositoriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_repository_creation_templates"]
    ) -> DescribeRepositoryCreationTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_lifecycle_policy_preview"]
    ) -> GetLifecyclePolicyPreviewPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_images"]
    ) -> ListImagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["image_scan_complete"]
    ) -> ImageScanCompleteWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["lifecycle_policy_preview_complete"]
    ) -> LifecyclePolicyPreviewCompleteWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/#get_waiter)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr.html#ECR.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr.html#ECR.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/client/)
        """
