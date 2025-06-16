"""
Type annotations for panorama service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_panorama.client import PanoramaClient

    session = get_session()
    async with session.create_client("panorama") as client:
        client: PanoramaClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    CreateApplicationInstanceRequestTypeDef,
    CreateApplicationInstanceResponseTypeDef,
    CreateJobForDevicesRequestTypeDef,
    CreateJobForDevicesResponseTypeDef,
    CreateNodeFromTemplateJobRequestTypeDef,
    CreateNodeFromTemplateJobResponseTypeDef,
    CreatePackageImportJobRequestTypeDef,
    CreatePackageImportJobResponseTypeDef,
    CreatePackageRequestTypeDef,
    CreatePackageResponseTypeDef,
    DeleteDeviceRequestTypeDef,
    DeleteDeviceResponseTypeDef,
    DeletePackageRequestTypeDef,
    DeregisterPackageVersionRequestTypeDef,
    DescribeApplicationInstanceDetailsRequestTypeDef,
    DescribeApplicationInstanceDetailsResponseTypeDef,
    DescribeApplicationInstanceRequestTypeDef,
    DescribeApplicationInstanceResponseTypeDef,
    DescribeDeviceJobRequestTypeDef,
    DescribeDeviceJobResponseTypeDef,
    DescribeDeviceRequestTypeDef,
    DescribeDeviceResponseTypeDef,
    DescribeNodeFromTemplateJobRequestTypeDef,
    DescribeNodeFromTemplateJobResponseTypeDef,
    DescribeNodeRequestTypeDef,
    DescribeNodeResponseTypeDef,
    DescribePackageImportJobRequestTypeDef,
    DescribePackageImportJobResponseTypeDef,
    DescribePackageRequestTypeDef,
    DescribePackageResponseTypeDef,
    DescribePackageVersionRequestTypeDef,
    DescribePackageVersionResponseTypeDef,
    ListApplicationInstanceDependenciesRequestTypeDef,
    ListApplicationInstanceDependenciesResponseTypeDef,
    ListApplicationInstanceNodeInstancesRequestTypeDef,
    ListApplicationInstanceNodeInstancesResponseTypeDef,
    ListApplicationInstancesRequestTypeDef,
    ListApplicationInstancesResponseTypeDef,
    ListDevicesJobsRequestTypeDef,
    ListDevicesJobsResponseTypeDef,
    ListDevicesRequestTypeDef,
    ListDevicesResponseTypeDef,
    ListNodeFromTemplateJobsRequestTypeDef,
    ListNodeFromTemplateJobsResponseTypeDef,
    ListNodesRequestTypeDef,
    ListNodesResponseTypeDef,
    ListPackageImportJobsRequestTypeDef,
    ListPackageImportJobsResponseTypeDef,
    ListPackagesRequestTypeDef,
    ListPackagesResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ProvisionDeviceRequestTypeDef,
    ProvisionDeviceResponseTypeDef,
    RegisterPackageVersionRequestTypeDef,
    RemoveApplicationInstanceRequestTypeDef,
    SignalApplicationInstanceNodeInstancesRequestTypeDef,
    SignalApplicationInstanceNodeInstancesResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateDeviceMetadataRequestTypeDef,
    UpdateDeviceMetadataResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Self, Unpack
else:
    from typing_extensions import Self, Unpack


__all__ = ("PanoramaClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class PanoramaClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PanoramaClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#generate_presigned_url)
        """

    async def create_application_instance(
        self, **kwargs: Unpack[CreateApplicationInstanceRequestTypeDef]
    ) -> CreateApplicationInstanceResponseTypeDef:
        """
        Creates an application instance and deploys it to a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/create_application_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#create_application_instance)
        """

    async def create_job_for_devices(
        self, **kwargs: Unpack[CreateJobForDevicesRequestTypeDef]
    ) -> CreateJobForDevicesResponseTypeDef:
        """
        Creates a job to run on a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/create_job_for_devices.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#create_job_for_devices)
        """

    async def create_node_from_template_job(
        self, **kwargs: Unpack[CreateNodeFromTemplateJobRequestTypeDef]
    ) -> CreateNodeFromTemplateJobResponseTypeDef:
        """
        Creates a camera stream node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/create_node_from_template_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#create_node_from_template_job)
        """

    async def create_package(
        self, **kwargs: Unpack[CreatePackageRequestTypeDef]
    ) -> CreatePackageResponseTypeDef:
        """
        Creates a package and storage location in an Amazon S3 access point.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/create_package.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#create_package)
        """

    async def create_package_import_job(
        self, **kwargs: Unpack[CreatePackageImportJobRequestTypeDef]
    ) -> CreatePackageImportJobResponseTypeDef:
        """
        Imports a node package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/create_package_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#create_package_import_job)
        """

    async def delete_device(
        self, **kwargs: Unpack[DeleteDeviceRequestTypeDef]
    ) -> DeleteDeviceResponseTypeDef:
        """
        Deletes a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/delete_device.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#delete_device)
        """

    async def delete_package(self, **kwargs: Unpack[DeletePackageRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/delete_package.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#delete_package)
        """

    async def deregister_package_version(
        self, **kwargs: Unpack[DeregisterPackageVersionRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deregisters a package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/deregister_package_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#deregister_package_version)
        """

    async def describe_application_instance(
        self, **kwargs: Unpack[DescribeApplicationInstanceRequestTypeDef]
    ) -> DescribeApplicationInstanceResponseTypeDef:
        """
        Returns information about an application instance on a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/describe_application_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#describe_application_instance)
        """

    async def describe_application_instance_details(
        self, **kwargs: Unpack[DescribeApplicationInstanceDetailsRequestTypeDef]
    ) -> DescribeApplicationInstanceDetailsResponseTypeDef:
        """
        Returns information about an application instance's configuration manifest.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/describe_application_instance_details.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#describe_application_instance_details)
        """

    async def describe_device(
        self, **kwargs: Unpack[DescribeDeviceRequestTypeDef]
    ) -> DescribeDeviceResponseTypeDef:
        """
        Returns information about a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/describe_device.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#describe_device)
        """

    async def describe_device_job(
        self, **kwargs: Unpack[DescribeDeviceJobRequestTypeDef]
    ) -> DescribeDeviceJobResponseTypeDef:
        """
        Returns information about a device job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/describe_device_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#describe_device_job)
        """

    async def describe_node(
        self, **kwargs: Unpack[DescribeNodeRequestTypeDef]
    ) -> DescribeNodeResponseTypeDef:
        """
        Returns information about a node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/describe_node.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#describe_node)
        """

    async def describe_node_from_template_job(
        self, **kwargs: Unpack[DescribeNodeFromTemplateJobRequestTypeDef]
    ) -> DescribeNodeFromTemplateJobResponseTypeDef:
        """
        Returns information about a job to create a camera stream node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/describe_node_from_template_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#describe_node_from_template_job)
        """

    async def describe_package(
        self, **kwargs: Unpack[DescribePackageRequestTypeDef]
    ) -> DescribePackageResponseTypeDef:
        """
        Returns information about a package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/describe_package.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#describe_package)
        """

    async def describe_package_import_job(
        self, **kwargs: Unpack[DescribePackageImportJobRequestTypeDef]
    ) -> DescribePackageImportJobResponseTypeDef:
        """
        Returns information about a package import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/describe_package_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#describe_package_import_job)
        """

    async def describe_package_version(
        self, **kwargs: Unpack[DescribePackageVersionRequestTypeDef]
    ) -> DescribePackageVersionResponseTypeDef:
        """
        Returns information about a package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/describe_package_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#describe_package_version)
        """

    async def list_application_instance_dependencies(
        self, **kwargs: Unpack[ListApplicationInstanceDependenciesRequestTypeDef]
    ) -> ListApplicationInstanceDependenciesResponseTypeDef:
        """
        Returns a list of application instance dependencies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/list_application_instance_dependencies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#list_application_instance_dependencies)
        """

    async def list_application_instance_node_instances(
        self, **kwargs: Unpack[ListApplicationInstanceNodeInstancesRequestTypeDef]
    ) -> ListApplicationInstanceNodeInstancesResponseTypeDef:
        """
        Returns a list of application node instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/list_application_instance_node_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#list_application_instance_node_instances)
        """

    async def list_application_instances(
        self, **kwargs: Unpack[ListApplicationInstancesRequestTypeDef]
    ) -> ListApplicationInstancesResponseTypeDef:
        """
        Returns a list of application instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/list_application_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#list_application_instances)
        """

    async def list_devices(
        self, **kwargs: Unpack[ListDevicesRequestTypeDef]
    ) -> ListDevicesResponseTypeDef:
        """
        Returns a list of devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/list_devices.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#list_devices)
        """

    async def list_devices_jobs(
        self, **kwargs: Unpack[ListDevicesJobsRequestTypeDef]
    ) -> ListDevicesJobsResponseTypeDef:
        """
        Returns a list of jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/list_devices_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#list_devices_jobs)
        """

    async def list_node_from_template_jobs(
        self, **kwargs: Unpack[ListNodeFromTemplateJobsRequestTypeDef]
    ) -> ListNodeFromTemplateJobsResponseTypeDef:
        """
        Returns a list of camera stream node jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/list_node_from_template_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#list_node_from_template_jobs)
        """

    async def list_nodes(
        self, **kwargs: Unpack[ListNodesRequestTypeDef]
    ) -> ListNodesResponseTypeDef:
        """
        Returns a list of nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/list_nodes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#list_nodes)
        """

    async def list_package_import_jobs(
        self, **kwargs: Unpack[ListPackageImportJobsRequestTypeDef]
    ) -> ListPackageImportJobsResponseTypeDef:
        """
        Returns a list of package import jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/list_package_import_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#list_package_import_jobs)
        """

    async def list_packages(
        self, **kwargs: Unpack[ListPackagesRequestTypeDef]
    ) -> ListPackagesResponseTypeDef:
        """
        Returns a list of packages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/list_packages.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#list_packages)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#list_tags_for_resource)
        """

    async def provision_device(
        self, **kwargs: Unpack[ProvisionDeviceRequestTypeDef]
    ) -> ProvisionDeviceResponseTypeDef:
        """
        Creates a device and returns a configuration archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/provision_device.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#provision_device)
        """

    async def register_package_version(
        self, **kwargs: Unpack[RegisterPackageVersionRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Registers a package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/register_package_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#register_package_version)
        """

    async def remove_application_instance(
        self, **kwargs: Unpack[RemoveApplicationInstanceRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes an application instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/remove_application_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#remove_application_instance)
        """

    async def signal_application_instance_node_instances(
        self, **kwargs: Unpack[SignalApplicationInstanceNodeInstancesRequestTypeDef]
    ) -> SignalApplicationInstanceNodeInstancesResponseTypeDef:
        """
        Signal camera nodes to stop or resume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/signal_application_instance_node_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#signal_application_instance_node_instances)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Tags a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#untag_resource)
        """

    async def update_device_metadata(
        self, **kwargs: Unpack[UpdateDeviceMetadataRequestTypeDef]
    ) -> UpdateDeviceMetadataResponseTypeDef:
        """
        Updates a device's metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/update_device_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#update_device_metadata)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/)
        """
