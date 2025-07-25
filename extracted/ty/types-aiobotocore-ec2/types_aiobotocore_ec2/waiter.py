"""
Type annotations for ec2 service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ec2.client import EC2Client
    from types_aiobotocore_ec2.waiter import (
        BundleTaskCompleteWaiter,
        ConversionTaskCancelledWaiter,
        ConversionTaskCompletedWaiter,
        ConversionTaskDeletedWaiter,
        CustomerGatewayAvailableWaiter,
        ExportTaskCancelledWaiter,
        ExportTaskCompletedWaiter,
        ImageAvailableWaiter,
        ImageExistsWaiter,
        InstanceExistsWaiter,
        InstanceRunningWaiter,
        InstanceStatusOkWaiter,
        InstanceStoppedWaiter,
        InstanceTerminatedWaiter,
        InternetGatewayExistsWaiter,
        KeyPairExistsWaiter,
        NatGatewayAvailableWaiter,
        NatGatewayDeletedWaiter,
        NetworkInterfaceAvailableWaiter,
        PasswordDataAvailableWaiter,
        SecurityGroupExistsWaiter,
        SecurityGroupVpcAssociationAssociatedWaiter,
        SecurityGroupVpcAssociationDisassociatedWaiter,
        SnapshotCompletedWaiter,
        SnapshotImportedWaiter,
        SpotInstanceRequestFulfilledWaiter,
        StoreImageTaskCompleteWaiter,
        SubnetAvailableWaiter,
        SystemStatusOkWaiter,
        VolumeAvailableWaiter,
        VolumeDeletedWaiter,
        VolumeInUseWaiter,
        VpcAvailableWaiter,
        VpcExistsWaiter,
        VpcPeeringConnectionDeletedWaiter,
        VpcPeeringConnectionExistsWaiter,
        VpnConnectionAvailableWaiter,
        VpnConnectionDeletedWaiter,
    )

    session = get_session()
    async with session.create_client("ec2") as client:
        client: EC2Client

        bundle_task_complete_waiter: BundleTaskCompleteWaiter = client.get_waiter("bundle_task_complete")
        conversion_task_cancelled_waiter: ConversionTaskCancelledWaiter = client.get_waiter("conversion_task_cancelled")
        conversion_task_completed_waiter: ConversionTaskCompletedWaiter = client.get_waiter("conversion_task_completed")
        conversion_task_deleted_waiter: ConversionTaskDeletedWaiter = client.get_waiter("conversion_task_deleted")
        customer_gateway_available_waiter: CustomerGatewayAvailableWaiter = client.get_waiter("customer_gateway_available")
        export_task_cancelled_waiter: ExportTaskCancelledWaiter = client.get_waiter("export_task_cancelled")
        export_task_completed_waiter: ExportTaskCompletedWaiter = client.get_waiter("export_task_completed")
        image_available_waiter: ImageAvailableWaiter = client.get_waiter("image_available")
        image_exists_waiter: ImageExistsWaiter = client.get_waiter("image_exists")
        instance_exists_waiter: InstanceExistsWaiter = client.get_waiter("instance_exists")
        instance_running_waiter: InstanceRunningWaiter = client.get_waiter("instance_running")
        instance_status_ok_waiter: InstanceStatusOkWaiter = client.get_waiter("instance_status_ok")
        instance_stopped_waiter: InstanceStoppedWaiter = client.get_waiter("instance_stopped")
        instance_terminated_waiter: InstanceTerminatedWaiter = client.get_waiter("instance_terminated")
        internet_gateway_exists_waiter: InternetGatewayExistsWaiter = client.get_waiter("internet_gateway_exists")
        key_pair_exists_waiter: KeyPairExistsWaiter = client.get_waiter("key_pair_exists")
        nat_gateway_available_waiter: NatGatewayAvailableWaiter = client.get_waiter("nat_gateway_available")
        nat_gateway_deleted_waiter: NatGatewayDeletedWaiter = client.get_waiter("nat_gateway_deleted")
        network_interface_available_waiter: NetworkInterfaceAvailableWaiter = client.get_waiter("network_interface_available")
        password_data_available_waiter: PasswordDataAvailableWaiter = client.get_waiter("password_data_available")
        security_group_exists_waiter: SecurityGroupExistsWaiter = client.get_waiter("security_group_exists")
        security_group_vpc_association_associated_waiter: SecurityGroupVpcAssociationAssociatedWaiter = client.get_waiter("security_group_vpc_association_associated")
        security_group_vpc_association_disassociated_waiter: SecurityGroupVpcAssociationDisassociatedWaiter = client.get_waiter("security_group_vpc_association_disassociated")
        snapshot_completed_waiter: SnapshotCompletedWaiter = client.get_waiter("snapshot_completed")
        snapshot_imported_waiter: SnapshotImportedWaiter = client.get_waiter("snapshot_imported")
        spot_instance_request_fulfilled_waiter: SpotInstanceRequestFulfilledWaiter = client.get_waiter("spot_instance_request_fulfilled")
        store_image_task_complete_waiter: StoreImageTaskCompleteWaiter = client.get_waiter("store_image_task_complete")
        subnet_available_waiter: SubnetAvailableWaiter = client.get_waiter("subnet_available")
        system_status_ok_waiter: SystemStatusOkWaiter = client.get_waiter("system_status_ok")
        volume_available_waiter: VolumeAvailableWaiter = client.get_waiter("volume_available")
        volume_deleted_waiter: VolumeDeletedWaiter = client.get_waiter("volume_deleted")
        volume_in_use_waiter: VolumeInUseWaiter = client.get_waiter("volume_in_use")
        vpc_available_waiter: VpcAvailableWaiter = client.get_waiter("vpc_available")
        vpc_exists_waiter: VpcExistsWaiter = client.get_waiter("vpc_exists")
        vpc_peering_connection_deleted_waiter: VpcPeeringConnectionDeletedWaiter = client.get_waiter("vpc_peering_connection_deleted")
        vpc_peering_connection_exists_waiter: VpcPeeringConnectionExistsWaiter = client.get_waiter("vpc_peering_connection_exists")
        vpn_connection_available_waiter: VpnConnectionAvailableWaiter = client.get_waiter("vpn_connection_available")
        vpn_connection_deleted_waiter: VpnConnectionDeletedWaiter = client.get_waiter("vpn_connection_deleted")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeBundleTasksRequestWaitTypeDef,
    DescribeConversionTasksRequestWaitExtraExtraTypeDef,
    DescribeConversionTasksRequestWaitExtraTypeDef,
    DescribeConversionTasksRequestWaitTypeDef,
    DescribeCustomerGatewaysRequestWaitTypeDef,
    DescribeExportTasksRequestWaitExtraTypeDef,
    DescribeExportTasksRequestWaitTypeDef,
    DescribeImagesRequestWaitExtraTypeDef,
    DescribeImagesRequestWaitTypeDef,
    DescribeImportSnapshotTasksRequestWaitTypeDef,
    DescribeInstancesRequestWaitExtraExtraExtraTypeDef,
    DescribeInstancesRequestWaitExtraExtraTypeDef,
    DescribeInstancesRequestWaitExtraTypeDef,
    DescribeInstancesRequestWaitTypeDef,
    DescribeInstanceStatusRequestWaitExtraTypeDef,
    DescribeInstanceStatusRequestWaitTypeDef,
    DescribeInternetGatewaysRequestWaitTypeDef,
    DescribeKeyPairsRequestWaitTypeDef,
    DescribeNatGatewaysRequestWaitExtraTypeDef,
    DescribeNatGatewaysRequestWaitTypeDef,
    DescribeNetworkInterfacesRequestWaitTypeDef,
    DescribeSecurityGroupsRequestWaitTypeDef,
    DescribeSecurityGroupVpcAssociationsRequestWaitExtraTypeDef,
    DescribeSecurityGroupVpcAssociationsRequestWaitTypeDef,
    DescribeSnapshotsRequestWaitTypeDef,
    DescribeSpotInstanceRequestsRequestWaitTypeDef,
    DescribeStoreImageTasksRequestWaitTypeDef,
    DescribeSubnetsRequestWaitTypeDef,
    DescribeVolumesRequestWaitExtraExtraTypeDef,
    DescribeVolumesRequestWaitExtraTypeDef,
    DescribeVolumesRequestWaitTypeDef,
    DescribeVpcPeeringConnectionsRequestWaitExtraTypeDef,
    DescribeVpcPeeringConnectionsRequestWaitTypeDef,
    DescribeVpcsRequestWaitExtraTypeDef,
    DescribeVpcsRequestWaitTypeDef,
    DescribeVpnConnectionsRequestWaitExtraTypeDef,
    DescribeVpnConnectionsRequestWaitTypeDef,
    GetPasswordDataRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "BundleTaskCompleteWaiter",
    "ConversionTaskCancelledWaiter",
    "ConversionTaskCompletedWaiter",
    "ConversionTaskDeletedWaiter",
    "CustomerGatewayAvailableWaiter",
    "ExportTaskCancelledWaiter",
    "ExportTaskCompletedWaiter",
    "ImageAvailableWaiter",
    "ImageExistsWaiter",
    "InstanceExistsWaiter",
    "InstanceRunningWaiter",
    "InstanceStatusOkWaiter",
    "InstanceStoppedWaiter",
    "InstanceTerminatedWaiter",
    "InternetGatewayExistsWaiter",
    "KeyPairExistsWaiter",
    "NatGatewayAvailableWaiter",
    "NatGatewayDeletedWaiter",
    "NetworkInterfaceAvailableWaiter",
    "PasswordDataAvailableWaiter",
    "SecurityGroupExistsWaiter",
    "SecurityGroupVpcAssociationAssociatedWaiter",
    "SecurityGroupVpcAssociationDisassociatedWaiter",
    "SnapshotCompletedWaiter",
    "SnapshotImportedWaiter",
    "SpotInstanceRequestFulfilledWaiter",
    "StoreImageTaskCompleteWaiter",
    "SubnetAvailableWaiter",
    "SystemStatusOkWaiter",
    "VolumeAvailableWaiter",
    "VolumeDeletedWaiter",
    "VolumeInUseWaiter",
    "VpcAvailableWaiter",
    "VpcExistsWaiter",
    "VpcPeeringConnectionDeletedWaiter",
    "VpcPeeringConnectionExistsWaiter",
    "VpnConnectionAvailableWaiter",
    "VpnConnectionDeletedWaiter",
)


class BundleTaskCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/BundleTaskComplete.html#EC2.Waiter.BundleTaskComplete)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#bundletaskcompletewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeBundleTasksRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/BundleTaskComplete.html#EC2.Waiter.BundleTaskComplete.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#bundletaskcompletewaiter)
        """


class ConversionTaskCancelledWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/ConversionTaskCancelled.html#EC2.Waiter.ConversionTaskCancelled)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#conversiontaskcancelledwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeConversionTasksRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/ConversionTaskCancelled.html#EC2.Waiter.ConversionTaskCancelled.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#conversiontaskcancelledwaiter)
        """


class ConversionTaskCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/ConversionTaskCompleted.html#EC2.Waiter.ConversionTaskCompleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#conversiontaskcompletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeConversionTasksRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/ConversionTaskCompleted.html#EC2.Waiter.ConversionTaskCompleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#conversiontaskcompletedwaiter)
        """


class ConversionTaskDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/ConversionTaskDeleted.html#EC2.Waiter.ConversionTaskDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#conversiontaskdeletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeConversionTasksRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/ConversionTaskDeleted.html#EC2.Waiter.ConversionTaskDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#conversiontaskdeletedwaiter)
        """


class CustomerGatewayAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/CustomerGatewayAvailable.html#EC2.Waiter.CustomerGatewayAvailable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#customergatewayavailablewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeCustomerGatewaysRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/CustomerGatewayAvailable.html#EC2.Waiter.CustomerGatewayAvailable.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#customergatewayavailablewaiter)
        """


class ExportTaskCancelledWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/ExportTaskCancelled.html#EC2.Waiter.ExportTaskCancelled)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#exporttaskcancelledwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeExportTasksRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/ExportTaskCancelled.html#EC2.Waiter.ExportTaskCancelled.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#exporttaskcancelledwaiter)
        """


class ExportTaskCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/ExportTaskCompleted.html#EC2.Waiter.ExportTaskCompleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#exporttaskcompletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeExportTasksRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/ExportTaskCompleted.html#EC2.Waiter.ExportTaskCompleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#exporttaskcompletedwaiter)
        """


class ImageAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/ImageAvailable.html#EC2.Waiter.ImageAvailable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#imageavailablewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeImagesRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/ImageAvailable.html#EC2.Waiter.ImageAvailable.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#imageavailablewaiter)
        """


class ImageExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/ImageExists.html#EC2.Waiter.ImageExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#imageexistswaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeImagesRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/ImageExists.html#EC2.Waiter.ImageExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#imageexistswaiter)
        """


class InstanceExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/InstanceExists.html#EC2.Waiter.InstanceExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#instanceexistswaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeInstancesRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/InstanceExists.html#EC2.Waiter.InstanceExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#instanceexistswaiter)
        """


class InstanceRunningWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/InstanceRunning.html#EC2.Waiter.InstanceRunning)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#instancerunningwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeInstancesRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/InstanceRunning.html#EC2.Waiter.InstanceRunning.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#instancerunningwaiter)
        """


class InstanceStatusOkWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/InstanceStatusOk.html#EC2.Waiter.InstanceStatusOk)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#instancestatusokwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeInstanceStatusRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/InstanceStatusOk.html#EC2.Waiter.InstanceStatusOk.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#instancestatusokwaiter)
        """


class InstanceStoppedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/InstanceStopped.html#EC2.Waiter.InstanceStopped)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#instancestoppedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeInstancesRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/InstanceStopped.html#EC2.Waiter.InstanceStopped.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#instancestoppedwaiter)
        """


class InstanceTerminatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/InstanceTerminated.html#EC2.Waiter.InstanceTerminated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#instanceterminatedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeInstancesRequestWaitExtraExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/InstanceTerminated.html#EC2.Waiter.InstanceTerminated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#instanceterminatedwaiter)
        """


class InternetGatewayExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/InternetGatewayExists.html#EC2.Waiter.InternetGatewayExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#internetgatewayexistswaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeInternetGatewaysRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/InternetGatewayExists.html#EC2.Waiter.InternetGatewayExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#internetgatewayexistswaiter)
        """


class KeyPairExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/KeyPairExists.html#EC2.Waiter.KeyPairExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#keypairexistswaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeKeyPairsRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/KeyPairExists.html#EC2.Waiter.KeyPairExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#keypairexistswaiter)
        """


class NatGatewayAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/NatGatewayAvailable.html#EC2.Waiter.NatGatewayAvailable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#natgatewayavailablewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeNatGatewaysRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/NatGatewayAvailable.html#EC2.Waiter.NatGatewayAvailable.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#natgatewayavailablewaiter)
        """


class NatGatewayDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/NatGatewayDeleted.html#EC2.Waiter.NatGatewayDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#natgatewaydeletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeNatGatewaysRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/NatGatewayDeleted.html#EC2.Waiter.NatGatewayDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#natgatewaydeletedwaiter)
        """


class NetworkInterfaceAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/NetworkInterfaceAvailable.html#EC2.Waiter.NetworkInterfaceAvailable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#networkinterfaceavailablewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeNetworkInterfacesRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/NetworkInterfaceAvailable.html#EC2.Waiter.NetworkInterfaceAvailable.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#networkinterfaceavailablewaiter)
        """


class PasswordDataAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/PasswordDataAvailable.html#EC2.Waiter.PasswordDataAvailable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#passworddataavailablewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetPasswordDataRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/PasswordDataAvailable.html#EC2.Waiter.PasswordDataAvailable.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#passworddataavailablewaiter)
        """


class SecurityGroupExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/SecurityGroupExists.html#EC2.Waiter.SecurityGroupExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#securitygroupexistswaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSecurityGroupsRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/SecurityGroupExists.html#EC2.Waiter.SecurityGroupExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#securitygroupexistswaiter)
        """


class SecurityGroupVpcAssociationAssociatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/SecurityGroupVpcAssociationAssociated.html#EC2.Waiter.SecurityGroupVpcAssociationAssociated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#securitygroupvpcassociationassociatedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSecurityGroupVpcAssociationsRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/SecurityGroupVpcAssociationAssociated.html#EC2.Waiter.SecurityGroupVpcAssociationAssociated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#securitygroupvpcassociationassociatedwaiter)
        """


class SecurityGroupVpcAssociationDisassociatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/SecurityGroupVpcAssociationDisassociated.html#EC2.Waiter.SecurityGroupVpcAssociationDisassociated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#securitygroupvpcassociationdisassociatedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSecurityGroupVpcAssociationsRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/SecurityGroupVpcAssociationDisassociated.html#EC2.Waiter.SecurityGroupVpcAssociationDisassociated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#securitygroupvpcassociationdisassociatedwaiter)
        """


class SnapshotCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/SnapshotCompleted.html#EC2.Waiter.SnapshotCompleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#snapshotcompletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSnapshotsRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/SnapshotCompleted.html#EC2.Waiter.SnapshotCompleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#snapshotcompletedwaiter)
        """


class SnapshotImportedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/SnapshotImported.html#EC2.Waiter.SnapshotImported)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#snapshotimportedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeImportSnapshotTasksRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/SnapshotImported.html#EC2.Waiter.SnapshotImported.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#snapshotimportedwaiter)
        """


class SpotInstanceRequestFulfilledWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/SpotInstanceRequestFulfilled.html#EC2.Waiter.SpotInstanceRequestFulfilled)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#spotinstancerequestfulfilledwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSpotInstanceRequestsRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/SpotInstanceRequestFulfilled.html#EC2.Waiter.SpotInstanceRequestFulfilled.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#spotinstancerequestfulfilledwaiter)
        """


class StoreImageTaskCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/StoreImageTaskComplete.html#EC2.Waiter.StoreImageTaskComplete)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#storeimagetaskcompletewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeStoreImageTasksRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/StoreImageTaskComplete.html#EC2.Waiter.StoreImageTaskComplete.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#storeimagetaskcompletewaiter)
        """


class SubnetAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/SubnetAvailable.html#EC2.Waiter.SubnetAvailable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#subnetavailablewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSubnetsRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/SubnetAvailable.html#EC2.Waiter.SubnetAvailable.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#subnetavailablewaiter)
        """


class SystemStatusOkWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/SystemStatusOk.html#EC2.Waiter.SystemStatusOk)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#systemstatusokwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeInstanceStatusRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/SystemStatusOk.html#EC2.Waiter.SystemStatusOk.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#systemstatusokwaiter)
        """


class VolumeAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/VolumeAvailable.html#EC2.Waiter.VolumeAvailable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#volumeavailablewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeVolumesRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/VolumeAvailable.html#EC2.Waiter.VolumeAvailable.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#volumeavailablewaiter)
        """


class VolumeDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/VolumeDeleted.html#EC2.Waiter.VolumeDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#volumedeletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeVolumesRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/VolumeDeleted.html#EC2.Waiter.VolumeDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#volumedeletedwaiter)
        """


class VolumeInUseWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/VolumeInUse.html#EC2.Waiter.VolumeInUse)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#volumeinusewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeVolumesRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/VolumeInUse.html#EC2.Waiter.VolumeInUse.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#volumeinusewaiter)
        """


class VpcAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/VpcAvailable.html#EC2.Waiter.VpcAvailable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#vpcavailablewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeVpcsRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/VpcAvailable.html#EC2.Waiter.VpcAvailable.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#vpcavailablewaiter)
        """


class VpcExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/VpcExists.html#EC2.Waiter.VpcExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#vpcexistswaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeVpcsRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/VpcExists.html#EC2.Waiter.VpcExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#vpcexistswaiter)
        """


class VpcPeeringConnectionDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/VpcPeeringConnectionDeleted.html#EC2.Waiter.VpcPeeringConnectionDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#vpcpeeringconnectiondeletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeVpcPeeringConnectionsRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/VpcPeeringConnectionDeleted.html#EC2.Waiter.VpcPeeringConnectionDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#vpcpeeringconnectiondeletedwaiter)
        """


class VpcPeeringConnectionExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/VpcPeeringConnectionExists.html#EC2.Waiter.VpcPeeringConnectionExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#vpcpeeringconnectionexistswaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeVpcPeeringConnectionsRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/VpcPeeringConnectionExists.html#EC2.Waiter.VpcPeeringConnectionExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#vpcpeeringconnectionexistswaiter)
        """


class VpnConnectionAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/VpnConnectionAvailable.html#EC2.Waiter.VpnConnectionAvailable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#vpnconnectionavailablewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeVpnConnectionsRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/VpnConnectionAvailable.html#EC2.Waiter.VpnConnectionAvailable.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#vpnconnectionavailablewaiter)
        """


class VpnConnectionDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/VpnConnectionDeleted.html#EC2.Waiter.VpnConnectionDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#vpnconnectiondeletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeVpnConnectionsRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/VpnConnectionDeleted.html#EC2.Waiter.VpnConnectionDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/waiters/#vpnconnectiondeletedwaiter)
        """
