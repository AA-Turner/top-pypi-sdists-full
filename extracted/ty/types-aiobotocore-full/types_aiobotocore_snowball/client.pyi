"""
Type annotations for snowball service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_snowball.client import SnowballClient

    session = get_session()
    async with session.create_client("snowball") as client:
        client: SnowballClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    DescribeAddressesPaginator,
    ListClusterJobsPaginator,
    ListClustersPaginator,
    ListCompatibleImagesPaginator,
    ListJobsPaginator,
    ListLongTermPricingPaginator,
)
from .type_defs import (
    CancelClusterRequestTypeDef,
    CancelJobRequestTypeDef,
    CreateAddressRequestTypeDef,
    CreateAddressResultTypeDef,
    CreateClusterRequestTypeDef,
    CreateClusterResultTypeDef,
    CreateJobRequestTypeDef,
    CreateJobResultTypeDef,
    CreateLongTermPricingRequestTypeDef,
    CreateLongTermPricingResultTypeDef,
    CreateReturnShippingLabelRequestTypeDef,
    CreateReturnShippingLabelResultTypeDef,
    DescribeAddressesRequestTypeDef,
    DescribeAddressesResultTypeDef,
    DescribeAddressRequestTypeDef,
    DescribeAddressResultTypeDef,
    DescribeClusterRequestTypeDef,
    DescribeClusterResultTypeDef,
    DescribeJobRequestTypeDef,
    DescribeJobResultTypeDef,
    DescribeReturnShippingLabelRequestTypeDef,
    DescribeReturnShippingLabelResultTypeDef,
    GetJobManifestRequestTypeDef,
    GetJobManifestResultTypeDef,
    GetJobUnlockCodeRequestTypeDef,
    GetJobUnlockCodeResultTypeDef,
    GetSnowballUsageResultTypeDef,
    GetSoftwareUpdatesRequestTypeDef,
    GetSoftwareUpdatesResultTypeDef,
    ListClusterJobsRequestTypeDef,
    ListClusterJobsResultTypeDef,
    ListClustersRequestTypeDef,
    ListClustersResultTypeDef,
    ListCompatibleImagesRequestTypeDef,
    ListCompatibleImagesResultTypeDef,
    ListJobsRequestTypeDef,
    ListJobsResultTypeDef,
    ListLongTermPricingRequestTypeDef,
    ListLongTermPricingResultTypeDef,
    ListPickupLocationsRequestTypeDef,
    ListPickupLocationsResultTypeDef,
    ListServiceVersionsRequestTypeDef,
    ListServiceVersionsResultTypeDef,
    UpdateClusterRequestTypeDef,
    UpdateJobRequestTypeDef,
    UpdateJobShipmentStateRequestTypeDef,
    UpdateLongTermPricingRequestTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("SnowballClient",)

class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    ClusterLimitExceededException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    Ec2RequestFailedException: Type[BotocoreClientError]
    InvalidAddressException: Type[BotocoreClientError]
    InvalidInputCombinationException: Type[BotocoreClientError]
    InvalidJobStateException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidResourceException: Type[BotocoreClientError]
    KMSRequestFailedException: Type[BotocoreClientError]
    ReturnShippingLabelAlreadyExistsException: Type[BotocoreClientError]
    UnsupportedAddressException: Type[BotocoreClientError]

class SnowballClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SnowballClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#generate_presigned_url)
        """

    async def cancel_cluster(self, **kwargs: Unpack[CancelClusterRequestTypeDef]) -> Dict[str, Any]:
        """
        Cancels a cluster job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/cancel_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#cancel_cluster)
        """

    async def cancel_job(self, **kwargs: Unpack[CancelJobRequestTypeDef]) -> Dict[str, Any]:
        """
        Cancels the specified job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/cancel_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#cancel_job)
        """

    async def create_address(
        self, **kwargs: Unpack[CreateAddressRequestTypeDef]
    ) -> CreateAddressResultTypeDef:
        """
        Creates an address for a Snow device to be shipped to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/create_address.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#create_address)
        """

    async def create_cluster(
        self, **kwargs: Unpack[CreateClusterRequestTypeDef]
    ) -> CreateClusterResultTypeDef:
        """
        Creates an empty cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/create_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#create_cluster)
        """

    async def create_job(self, **kwargs: Unpack[CreateJobRequestTypeDef]) -> CreateJobResultTypeDef:
        """
        Creates a job to import or export data between Amazon S3 and your on-premises
        data center.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/create_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#create_job)
        """

    async def create_long_term_pricing(
        self, **kwargs: Unpack[CreateLongTermPricingRequestTypeDef]
    ) -> CreateLongTermPricingResultTypeDef:
        """
        Creates a job with the long-term usage option for a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/create_long_term_pricing.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#create_long_term_pricing)
        """

    async def create_return_shipping_label(
        self, **kwargs: Unpack[CreateReturnShippingLabelRequestTypeDef]
    ) -> CreateReturnShippingLabelResultTypeDef:
        """
        Creates a shipping label that will be used to return the Snow device to Amazon
        Web Services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/create_return_shipping_label.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#create_return_shipping_label)
        """

    async def describe_address(
        self, **kwargs: Unpack[DescribeAddressRequestTypeDef]
    ) -> DescribeAddressResultTypeDef:
        """
        Takes an <code>AddressId</code> and returns specific details about that address
        in the form of an <code>Address</code> object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/describe_address.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#describe_address)
        """

    async def describe_addresses(
        self, **kwargs: Unpack[DescribeAddressesRequestTypeDef]
    ) -> DescribeAddressesResultTypeDef:
        """
        Returns a specified number of <code>ADDRESS</code> objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/describe_addresses.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#describe_addresses)
        """

    async def describe_cluster(
        self, **kwargs: Unpack[DescribeClusterRequestTypeDef]
    ) -> DescribeClusterResultTypeDef:
        """
        Returns information about a specific cluster including shipping information,
        cluster status, and other important metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/describe_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#describe_cluster)
        """

    async def describe_job(
        self, **kwargs: Unpack[DescribeJobRequestTypeDef]
    ) -> DescribeJobResultTypeDef:
        """
        Returns information about a specific job including shipping information, job
        status, and other important metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/describe_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#describe_job)
        """

    async def describe_return_shipping_label(
        self, **kwargs: Unpack[DescribeReturnShippingLabelRequestTypeDef]
    ) -> DescribeReturnShippingLabelResultTypeDef:
        """
        Information on the shipping label of a Snow device that is being returned to
        Amazon Web Services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/describe_return_shipping_label.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#describe_return_shipping_label)
        """

    async def get_job_manifest(
        self, **kwargs: Unpack[GetJobManifestRequestTypeDef]
    ) -> GetJobManifestResultTypeDef:
        """
        Returns a link to an Amazon S3 presigned URL for the manifest file associated
        with the specified <code>JobId</code> value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/get_job_manifest.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#get_job_manifest)
        """

    async def get_job_unlock_code(
        self, **kwargs: Unpack[GetJobUnlockCodeRequestTypeDef]
    ) -> GetJobUnlockCodeResultTypeDef:
        """
        Returns the <code>UnlockCode</code> code value for the specified job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/get_job_unlock_code.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#get_job_unlock_code)
        """

    async def get_snowball_usage(self) -> GetSnowballUsageResultTypeDef:
        """
        Returns information about the Snow Family service limit for your account, and
        also the number of Snow devices your account has in use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/get_snowball_usage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#get_snowball_usage)
        """

    async def get_software_updates(
        self, **kwargs: Unpack[GetSoftwareUpdatesRequestTypeDef]
    ) -> GetSoftwareUpdatesResultTypeDef:
        """
        Returns an Amazon S3 presigned URL for an update file associated with a
        specified <code>JobId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/get_software_updates.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#get_software_updates)
        """

    async def list_cluster_jobs(
        self, **kwargs: Unpack[ListClusterJobsRequestTypeDef]
    ) -> ListClusterJobsResultTypeDef:
        """
        Returns an array of <code>JobListEntry</code> objects of the specified length.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/list_cluster_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#list_cluster_jobs)
        """

    async def list_clusters(
        self, **kwargs: Unpack[ListClustersRequestTypeDef]
    ) -> ListClustersResultTypeDef:
        """
        Returns an array of <code>ClusterListEntry</code> objects of the specified
        length.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/list_clusters.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#list_clusters)
        """

    async def list_compatible_images(
        self, **kwargs: Unpack[ListCompatibleImagesRequestTypeDef]
    ) -> ListCompatibleImagesResultTypeDef:
        """
        This action returns a list of the different Amazon EC2-compatible Amazon
        Machine Images (AMIs) that are owned by your Amazon Web Services accountthat
        would be supported for use on a Snow device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/list_compatible_images.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#list_compatible_images)
        """

    async def list_jobs(self, **kwargs: Unpack[ListJobsRequestTypeDef]) -> ListJobsResultTypeDef:
        """
        Returns an array of <code>JobListEntry</code> objects of the specified length.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/list_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#list_jobs)
        """

    async def list_long_term_pricing(
        self, **kwargs: Unpack[ListLongTermPricingRequestTypeDef]
    ) -> ListLongTermPricingResultTypeDef:
        """
        Lists all long-term pricing types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/list_long_term_pricing.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#list_long_term_pricing)
        """

    async def list_pickup_locations(
        self, **kwargs: Unpack[ListPickupLocationsRequestTypeDef]
    ) -> ListPickupLocationsResultTypeDef:
        """
        A list of locations from which the customer can choose to pickup a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/list_pickup_locations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#list_pickup_locations)
        """

    async def list_service_versions(
        self, **kwargs: Unpack[ListServiceVersionsRequestTypeDef]
    ) -> ListServiceVersionsResultTypeDef:
        """
        Lists all supported versions for Snow on-device services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/list_service_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#list_service_versions)
        """

    async def update_cluster(self, **kwargs: Unpack[UpdateClusterRequestTypeDef]) -> Dict[str, Any]:
        """
        While a cluster's <code>ClusterState</code> value is in the
        <code>AwaitingQuorum</code> state, you can update some of the information
        associated with a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/update_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#update_cluster)
        """

    async def update_job(self, **kwargs: Unpack[UpdateJobRequestTypeDef]) -> Dict[str, Any]:
        """
        While a job's <code>JobState</code> value is <code>New</code>, you can update
        some of the information associated with a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/update_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#update_job)
        """

    async def update_job_shipment_state(
        self, **kwargs: Unpack[UpdateJobShipmentStateRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the state when a shipment state changes to a different state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/update_job_shipment_state.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#update_job_shipment_state)
        """

    async def update_long_term_pricing(
        self, **kwargs: Unpack[UpdateLongTermPricingRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the long-term pricing type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/update_long_term_pricing.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#update_long_term_pricing)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_addresses"]
    ) -> DescribeAddressesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_cluster_jobs"]
    ) -> ListClusterJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_clusters"]
    ) -> ListClustersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_compatible_images"]
    ) -> ListCompatibleImagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_jobs"]
    ) -> ListJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_long_term_pricing"]
    ) -> ListLongTermPricingPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/)
        """
