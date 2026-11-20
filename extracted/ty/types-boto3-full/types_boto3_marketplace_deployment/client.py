"""
Type annotations for marketplace-deployment service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_deployment/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_marketplace_deployment.client import MarketplaceDeploymentServiceClient

    session = Session()
    client: MarketplaceDeploymentServiceClient = session.client("marketplace-deployment")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListDeploymentConfigurationJobsPaginator
from .type_defs import (
    GetDeploymentConfigurationJobRequestTypeDef,
    GetDeploymentConfigurationJobResponseTypeDef,
    GetDeploymentConfigurationRequestTypeDef,
    GetDeploymentConfigurationResponseTypeDef,
    ListDeploymentConfigurationJobsRequestTypeDef,
    ListDeploymentConfigurationJobsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutDeploymentParameterRequestTypeDef,
    PutDeploymentParameterResponseTypeDef,
    StartDeploymentConfigurationJobRequestTypeDef,
    StartDeploymentConfigurationJobResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("MarketplaceDeploymentServiceClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class MarketplaceDeploymentServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-deployment.html#MarketplaceDeploymentService.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_deployment/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MarketplaceDeploymentServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-deployment.html#MarketplaceDeploymentService.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_deployment/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-deployment/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_deployment/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-deployment/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_deployment/client/#generate_presigned_url)
        """

    def get_deployment_configuration(
        self, **kwargs: Unpack[GetDeploymentConfigurationRequestTypeDef]
    ) -> GetDeploymentConfigurationResponseTypeDef:
        """
        Returns the active deployment configuration for a product and delivery option.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-deployment/client/get_deployment_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_deployment/client/#get_deployment_configuration)
        """

    def get_deployment_configuration_job(
        self, **kwargs: Unpack[GetDeploymentConfigurationJobRequestTypeDef]
    ) -> GetDeploymentConfigurationJobResponseTypeDef:
        """
        Returns the details of a deployment configuration job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-deployment/client/get_deployment_configuration_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_deployment/client/#get_deployment_configuration_job)
        """

    def list_deployment_configuration_jobs(
        self, **kwargs: Unpack[ListDeploymentConfigurationJobsRequestTypeDef]
    ) -> ListDeploymentConfigurationJobsResponseTypeDef:
        """
        Lists the deployment configuration jobs that you started for a product and
        delivery option, ordered from newest to oldest.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-deployment/client/list_deployment_configuration_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_deployment/client/#list_deployment_configuration_jobs)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags that have been added to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-deployment/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_deployment/client/#list_tags_for_resource)
        """

    def put_deployment_parameter(
        self, **kwargs: Unpack[PutDeploymentParameterRequestTypeDef]
    ) -> PutDeploymentParameterResponseTypeDef:
        """
        Creates or updates a deployment parameter and is targeted by
        <code>catalog</code> and <code>agreementId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-deployment/client/put_deployment_parameter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_deployment/client/#put_deployment_parameter)
        """

    def start_deployment_configuration_job(
        self, **kwargs: Unpack[StartDeploymentConfigurationJobRequestTypeDef]
    ) -> StartDeploymentConfigurationJobResponseTypeDef:
        """
        Starts a job that publishes a deployment configuration for a product and
        delivery option.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-deployment/client/start_deployment_configuration_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_deployment/client/#start_deployment_configuration_job)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Tags a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-deployment/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_deployment/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Removes a tag or list of tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-deployment/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_deployment/client/#untag_resource)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_deployment_configuration_jobs"]
    ) -> ListDeploymentConfigurationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-deployment/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_deployment/client/#get_paginator)
        """
