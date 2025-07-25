"""
Type annotations for ec2 service ServiceResource.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ec2.service_resource import EC2ServiceResource
    import types_aiobotocore_ec2.service_resource as ec2_resources

    session = get_session()
    async with session.resource("ec2") as resource:
        resource: EC2ServiceResource

        my_classic_address: ec2_resources.ClassicAddress = resource.ClassicAddress(...)
        my_dhcp_options: ec2_resources.DhcpOptions = resource.DhcpOptions(...)
        my_image: ec2_resources.Image = resource.Image(...)
        my_instance: ec2_resources.Instance = resource.Instance(...)
        my_internet_gateway: ec2_resources.InternetGateway = resource.InternetGateway(...)
        my_key_pair: ec2_resources.KeyPair = resource.KeyPair(...)
        my_key_pair_info: ec2_resources.KeyPairInfo = resource.KeyPairInfo(...)
        my_network_acl: ec2_resources.NetworkAcl = resource.NetworkAcl(...)
        my_network_interface: ec2_resources.NetworkInterface = resource.NetworkInterface(...)
        my_network_interface_association: ec2_resources.NetworkInterfaceAssociation = resource.NetworkInterfaceAssociation(...)
        my_placement_group: ec2_resources.PlacementGroup = resource.PlacementGroup(...)
        my_route: ec2_resources.Route = resource.Route(...)
        my_route_table: ec2_resources.RouteTable = resource.RouteTable(...)
        my_route_table_association: ec2_resources.RouteTableAssociation = resource.RouteTableAssociation(...)
        my_security_group: ec2_resources.SecurityGroup = resource.SecurityGroup(...)
        my_snapshot: ec2_resources.Snapshot = resource.Snapshot(...)
        my_subnet: ec2_resources.Subnet = resource.Subnet(...)
        my_tag: ec2_resources.Tag = resource.Tag(...)
        my_volume: ec2_resources.Volume = resource.Volume(...)
        my_vpc: ec2_resources.Vpc = resource.Vpc(...)
        my_vpc_peering_connection: ec2_resources.VpcPeeringConnection = resource.VpcPeeringConnection(...)
        my_vpc_address: ec2_resources.VpcAddress = resource.VpcAddress(...)
```
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import NoReturn

from aioboto3.resources.base import AIOBoto3ServiceResource
from aioboto3.resources.collection import AIOResourceCollection

from .client import EC2Client
from .literals import (
    ArchitectureValuesType,
    BootModeValuesType,
    DeviceTypeType,
    DomainTypeType,
    HypervisorTypeType,
    ImageStateType,
    ImageTypeValuesType,
    InstanceBootModeValuesType,
    InstanceLifecycleTypeType,
    InstanceTypeType,
    KeyTypeType,
    NetworkInterfaceStatusType,
    NetworkInterfaceTypeType,
    PlacementGroupStateType,
    PlacementStrategyType,
    ResourceTypeType,
    RouteOriginType,
    RouteStateType,
    ServiceManagedType,
    SnapshotStateType,
    SpreadLevelType,
    SSETypeType,
    StorageTierType,
    SubnetStateType,
    TenancyType,
    TransferTypeType,
    VirtualizationTypeType,
    VolumeStateType,
    VolumeTypeType,
    VpcStateType,
)
from .type_defs import (
    AcceptVpcPeeringConnectionRequestVpcPeeringConnectionAcceptTypeDef,
    AcceptVpcPeeringConnectionResultTypeDef,
    AssignPrivateIpAddressesRequestNetworkInterfaceAssignPrivateIpAddressesTypeDef,
    AssignPrivateIpAddressesResultTypeDef,
    AssociateAddressRequestClassicAddressAssociateTypeDef,
    AssociateAddressRequestVpcAddressAssociateTypeDef,
    AssociateAddressResultTypeDef,
    AssociateDhcpOptionsRequestDhcpOptionsAssociateWithVpcTypeDef,
    AssociateDhcpOptionsRequestVpcAssociateDhcpOptionsTypeDef,
    AssociateRouteTableRequestRouteTableAssociateWithSubnetTypeDef,
    AttachClassicLinkVpcRequestInstanceAttachClassicLinkVpcTypeDef,
    AttachClassicLinkVpcRequestVpcAttachClassicLinkInstanceTypeDef,
    AttachClassicLinkVpcResultTypeDef,
    AttachInternetGatewayRequestInternetGatewayAttachToVpcTypeDef,
    AttachInternetGatewayRequestVpcAttachInternetGatewayTypeDef,
    AttachNetworkInterfaceRequestNetworkInterfaceAttachTypeDef,
    AttachNetworkInterfaceResultTypeDef,
    AttachVolumeRequestInstanceAttachVolumeTypeDef,
    AttachVolumeRequestVolumeAttachToInstanceTypeDef,
    AuthorizeSecurityGroupEgressRequestSecurityGroupAuthorizeEgressTypeDef,
    AuthorizeSecurityGroupEgressResultTypeDef,
    AuthorizeSecurityGroupIngressRequestSecurityGroupAuthorizeIngressTypeDef,
    AuthorizeSecurityGroupIngressResultTypeDef,
    BlockDeviceMappingTypeDef,
    BlockPublicAccessStatesTypeDef,
    CapacityReservationSpecificationResponseTypeDef,
    ConnectionTrackingConfigurationTypeDef,
    CopySnapshotRequestSnapshotCopyTypeDef,
    CopySnapshotResultTypeDef,
    CpuOptionsTypeDef,
    CreateDhcpOptionsRequestServiceResourceCreateDhcpOptionsTypeDef,
    CreateImageRequestInstanceCreateImageTypeDef,
    CreateInternetGatewayRequestServiceResourceCreateInternetGatewayTypeDef,
    CreateKeyPairRequestServiceResourceCreateKeyPairTypeDef,
    CreateNetworkAclEntryRequestNetworkAclCreateEntryTypeDef,
    CreateNetworkAclRequestServiceResourceCreateNetworkAclTypeDef,
    CreateNetworkAclRequestVpcCreateNetworkAclTypeDef,
    CreateNetworkInterfaceRequestServiceResourceCreateNetworkInterfaceTypeDef,
    CreateNetworkInterfaceRequestSubnetCreateNetworkInterfaceTypeDef,
    CreatePlacementGroupRequestServiceResourceCreatePlacementGroupTypeDef,
    CreateRouteRequestRouteTableCreateRouteTypeDef,
    CreateRouteTableRequestServiceResourceCreateRouteTableTypeDef,
    CreateRouteTableRequestVpcCreateRouteTableTypeDef,
    CreateSecurityGroupRequestServiceResourceCreateSecurityGroupTypeDef,
    CreateSecurityGroupRequestVpcCreateSecurityGroupTypeDef,
    CreateSnapshotRequestServiceResourceCreateSnapshotTypeDef,
    CreateSnapshotRequestVolumeCreateSnapshotTypeDef,
    CreateSubnetRequestServiceResourceCreateSubnetTypeDef,
    CreateSubnetRequestVpcCreateSubnetTypeDef,
    CreateTagsRequestServiceResourceCreateTagsTypeDef,
    CreateVolumeRequestServiceResourceCreateVolumeTypeDef,
    CreateVpcPeeringConnectionRequestServiceResourceCreateVpcPeeringConnectionTypeDef,
    CreateVpcPeeringConnectionRequestVpcRequestVpcPeeringConnectionTypeDef,
    CreateVpcRequestServiceResourceCreateVpcTypeDef,
    DeleteDhcpOptionsRequestDhcpOptionsDeleteTypeDef,
    DeleteInternetGatewayRequestInternetGatewayDeleteTypeDef,
    DeleteKeyPairRequestKeyPairDeleteTypeDef,
    DeleteKeyPairRequestKeyPairInfoDeleteTypeDef,
    DeleteKeyPairResultTypeDef,
    DeleteNetworkAclEntryRequestNetworkAclDeleteEntryTypeDef,
    DeleteNetworkAclRequestNetworkAclDeleteTypeDef,
    DeleteNetworkInterfaceRequestNetworkInterfaceDeleteTypeDef,
    DeletePlacementGroupRequestPlacementGroupDeleteTypeDef,
    DeleteRouteRequestRouteDeleteTypeDef,
    DeleteRouteTableRequestRouteTableDeleteTypeDef,
    DeleteSecurityGroupRequestSecurityGroupDeleteTypeDef,
    DeleteSecurityGroupResultTypeDef,
    DeleteSnapshotRequestSnapshotDeleteTypeDef,
    DeleteSubnetRequestSubnetDeleteTypeDef,
    DeleteTagsRequestTagDeleteTypeDef,
    DeleteVolumeRequestVolumeDeleteTypeDef,
    DeleteVpcPeeringConnectionRequestVpcPeeringConnectionDeleteTypeDef,
    DeleteVpcPeeringConnectionResultTypeDef,
    DeleteVpcRequestVpcDeleteTypeDef,
    DeregisterImageRequestImageDeregisterTypeDef,
    DeregisterImageResultTypeDef,
    DescribeImageAttributeRequestImageDescribeAttributeTypeDef,
    DescribeInstanceAttributeRequestInstanceDescribeAttributeTypeDef,
    DescribeNetworkInterfaceAttributeRequestNetworkInterfaceDescribeAttributeTypeDef,
    DescribeNetworkInterfaceAttributeResultTypeDef,
    DescribeSnapshotAttributeRequestSnapshotDescribeAttributeTypeDef,
    DescribeSnapshotAttributeResultTypeDef,
    DescribeVolumeAttributeRequestVolumeDescribeAttributeTypeDef,
    DescribeVolumeAttributeResultTypeDef,
    DescribeVolumeStatusRequestVolumeDescribeStatusTypeDef,
    DescribeVolumeStatusResultTypeDef,
    DescribeVpcAttributeRequestVpcDescribeAttributeTypeDef,
    DescribeVpcAttributeResultTypeDef,
    DetachClassicLinkVpcRequestInstanceDetachClassicLinkVpcTypeDef,
    DetachClassicLinkVpcRequestVpcDetachClassicLinkInstanceTypeDef,
    DetachClassicLinkVpcResultTypeDef,
    DetachInternetGatewayRequestInternetGatewayDetachFromVpcTypeDef,
    DetachInternetGatewayRequestVpcDetachInternetGatewayTypeDef,
    DetachNetworkInterfaceRequestNetworkInterfaceDetachTypeDef,
    DetachVolumeRequestInstanceDetachVolumeTypeDef,
    DetachVolumeRequestVolumeDetachFromInstanceTypeDef,
    DhcpConfigurationTypeDef,
    DhcpOptionsCreateTagsRequestTypeDef,
    DisableVpcClassicLinkRequestVpcDisableClassicLinkTypeDef,
    DisableVpcClassicLinkResultTypeDef,
    DisassociateAddressRequestClassicAddressDisassociateTypeDef,
    DisassociateAddressRequestNetworkInterfaceAssociationDeleteTypeDef,
    DisassociateRouteTableRequestRouteTableAssociationDeleteTypeDef,
    DisassociateRouteTableRequestServiceResourceDisassociateRouteTableTypeDef,
    ElasticGpuAssociationTypeDef,
    ElasticInferenceAcceleratorAssociationTypeDef,
    EnableVolumeIORequestVolumeEnableIoTypeDef,
    EnableVpcClassicLinkRequestVpcEnableClassicLinkTypeDef,
    EnableVpcClassicLinkResultTypeDef,
    EnclaveOptionsTypeDef,
    FilterTypeDef,
    GetConsoleOutputRequestInstanceConsoleOutputTypeDef,
    GetConsoleOutputResultTypeDef,
    GetPasswordDataRequestInstancePasswordDataTypeDef,
    GetPasswordDataResultTypeDef,
    GroupIdentifierTypeDef,
    HibernationOptionsTypeDef,
    IamInstanceProfileTypeDef,
    ImageAttributeTypeDef,
    ImageCreateTagsRequestTypeDef,
    ImportKeyPairRequestServiceResourceImportKeyPairTypeDef,
    InstanceAttributeTypeDef,
    InstanceBlockDeviceMappingTypeDef,
    InstanceCreateTagsRequestTypeDef,
    InstanceDeleteTagsRequestTypeDef,
    InstanceMaintenanceOptionsTypeDef,
    InstanceMetadataOptionsResponseTypeDef,
    InstanceNetworkInterfaceTypeDef,
    InstanceNetworkPerformanceOptionsTypeDef,
    InstanceStateTypeDef,
    InternetGatewayAttachmentTypeDef,
    InternetGatewayCreateTagsRequestTypeDef,
    IpPermissionOutputTypeDef,
    Ipv4PrefixSpecificationTypeDef,
    Ipv6PrefixSpecificationTypeDef,
    LicenseConfigurationTypeDef,
    ModifyImageAttributeRequestImageModifyAttributeTypeDef,
    ModifyInstanceAttributeRequestInstanceModifyAttributeTypeDef,
    ModifyNetworkInterfaceAttributeRequestNetworkInterfaceModifyAttributeTypeDef,
    ModifySnapshotAttributeRequestSnapshotModifyAttributeTypeDef,
    ModifyVolumeAttributeRequestVolumeModifyAttributeTypeDef,
    ModifyVpcAttributeRequestVpcModifyAttributeTypeDef,
    MonitoringTypeDef,
    MonitorInstancesRequestInstanceMonitorTypeDef,
    MonitorInstancesResultTypeDef,
    NetworkAclAssociationTypeDef,
    NetworkAclCreateTagsRequestTypeDef,
    NetworkAclEntryTypeDef,
    NetworkInterfaceAssociationTypeDef,
    NetworkInterfaceAttachmentTypeDef,
    NetworkInterfaceCreateTagsRequestTypeDef,
    NetworkInterfaceIpv6AddressTypeDef,
    NetworkInterfacePrivateIpAddressTypeDef,
    OperatorResponseTypeDef,
    PlacementTypeDef,
    PrivateDnsNameOptionsOnLaunchTypeDef,
    PrivateDnsNameOptionsResponseTypeDef,
    ProductCodeTypeDef,
    PropagatingVgwTypeDef,
    PublicIpDnsNameOptionsTypeDef,
    RebootInstancesRequestInstanceRebootTypeDef,
    RegisterImageRequestServiceResourceRegisterImageTypeDef,
    RejectVpcPeeringConnectionRequestVpcPeeringConnectionRejectTypeDef,
    RejectVpcPeeringConnectionResultTypeDef,
    ReleaseAddressRequestClassicAddressReleaseTypeDef,
    ReleaseAddressRequestVpcAddressReleaseTypeDef,
    ReplaceNetworkAclAssociationRequestNetworkAclReplaceAssociationTypeDef,
    ReplaceNetworkAclAssociationResultTypeDef,
    ReplaceNetworkAclEntryRequestNetworkAclReplaceEntryTypeDef,
    ReplaceRouteRequestRouteReplaceTypeDef,
    ReplaceRouteTableAssociationRequestRouteTableAssociationReplaceSubnetTypeDef,
    ReportInstanceStatusRequestInstanceReportStatusTypeDef,
    ResetImageAttributeRequestImageResetAttributeTypeDef,
    ResetInstanceAttributeRequestInstanceResetAttributeTypeDef,
    ResetInstanceAttributeRequestInstanceResetKernelTypeDef,
    ResetInstanceAttributeRequestInstanceResetRamdiskTypeDef,
    ResetInstanceAttributeRequestInstanceResetSourceDestCheckTypeDef,
    ResetNetworkInterfaceAttributeRequestNetworkInterfaceResetAttributeTypeDef,
    ResetSnapshotAttributeRequestSnapshotResetAttributeTypeDef,
    RevokeSecurityGroupEgressRequestSecurityGroupRevokeEgressTypeDef,
    RevokeSecurityGroupEgressResultTypeDef,
    RevokeSecurityGroupIngressRequestSecurityGroupRevokeIngressTypeDef,
    RevokeSecurityGroupIngressResultTypeDef,
    RouteTableAssociationStateTypeDef,
    RouteTableAssociationTypeDef,
    RouteTableCreateTagsRequestTypeDef,
    RouteTypeDef,
    RunInstancesRequestServiceResourceCreateInstancesTypeDef,
    RunInstancesRequestSubnetCreateInstancesTypeDef,
    SecurityGroupCreateTagsRequestTypeDef,
    SnapshotCreateTagsRequestTypeDef,
    StartInstancesRequestInstanceStartTypeDef,
    StartInstancesResultTypeDef,
    StateReasonTypeDef,
    StopInstancesRequestInstanceStopTypeDef,
    StopInstancesResultTypeDef,
    SubnetCreateTagsRequestTypeDef,
    SubnetIpv6CidrBlockAssociationTypeDef,
    TagTypeDef,
    TerminateInstancesRequestInstanceTerminateTypeDef,
    TerminateInstancesResultTypeDef,
    UnassignPrivateIpAddressesRequestNetworkInterfaceUnassignPrivateIpAddressesTypeDef,
    UnmonitorInstancesRequestInstanceUnmonitorTypeDef,
    UnmonitorInstancesResultTypeDef,
    VolumeAttachmentResponseTypeDef,
    VolumeAttachmentTypeDef,
    VolumeCreateTagsRequestTypeDef,
    VpcCidrBlockAssociationTypeDef,
    VpcCreateTagsRequestTypeDef,
    VpcEncryptionControlTypeDef,
    VpcIpv6CidrBlockAssociationTypeDef,
    VpcPeeringConnectionStateReasonTypeDef,
    VpcPeeringConnectionVpcInfoTypeDef,
)

try:
    from boto3.resources.base import ResourceMeta
except ImportError:
    from builtins import object as ResourceMeta  # type: ignore[assignment]
if sys.version_info >= (3, 9):
    from builtins import list as List
    from collections.abc import AsyncIterator, Awaitable, Sequence
else:
    from typing import AsyncIterator, Awaitable, List, Sequence
if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = (
    "ClassicAddress",
    "DhcpOptions",
    "EC2ServiceResource",
    "Image",
    "Instance",
    "InstanceVolumesCollection",
    "InstanceVpcAddressesCollection",
    "InternetGateway",
    "KeyPair",
    "KeyPairInfo",
    "NetworkAcl",
    "NetworkInterface",
    "NetworkInterfaceAssociation",
    "PlacementGroup",
    "PlacementGroupInstancesCollection",
    "Route",
    "RouteTable",
    "RouteTableAssociation",
    "SecurityGroup",
    "ServiceResourceClassicAddressesCollection",
    "ServiceResourceDhcpOptionsSetsCollection",
    "ServiceResourceImagesCollection",
    "ServiceResourceInstancesCollection",
    "ServiceResourceInternetGatewaysCollection",
    "ServiceResourceKeyPairsCollection",
    "ServiceResourceNetworkAclsCollection",
    "ServiceResourceNetworkInterfacesCollection",
    "ServiceResourcePlacementGroupsCollection",
    "ServiceResourceRouteTablesCollection",
    "ServiceResourceSecurityGroupsCollection",
    "ServiceResourceSnapshotsCollection",
    "ServiceResourceSubnetsCollection",
    "ServiceResourceVolumesCollection",
    "ServiceResourceVpcAddressesCollection",
    "ServiceResourceVpcPeeringConnectionsCollection",
    "ServiceResourceVpcsCollection",
    "Snapshot",
    "Subnet",
    "SubnetInstancesCollection",
    "SubnetNetworkInterfacesCollection",
    "Tag",
    "Volume",
    "VolumeSnapshotsCollection",
    "Vpc",
    "VpcAcceptedVpcPeeringConnectionsCollection",
    "VpcAddress",
    "VpcInstancesCollection",
    "VpcInternetGatewaysCollection",
    "VpcNetworkAclsCollection",
    "VpcNetworkInterfacesCollection",
    "VpcPeeringConnection",
    "VpcRequestedVpcPeeringConnectionsCollection",
    "VpcRouteTablesCollection",
    "VpcSecurityGroupsCollection",
    "VpcSubnetsCollection",
)


class ServiceResourceClassicAddressesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/classic_addresses.html#EC2.ServiceResource.classic_addresses)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceclassicaddressescollection)
    """

    def all(self) -> ServiceResourceClassicAddressesCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/classic_addresses.html#EC2.ServiceResource.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceclassicaddressescollection)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        PublicIps: Sequence[str] = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        AllocationIds: Sequence[str] = ...,
    ) -> ServiceResourceClassicAddressesCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/classic_addresses.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceclassicaddressescollection)
        """

    def limit(self, count: int) -> ServiceResourceClassicAddressesCollection:
        """
        Return at most this many ClassicAddresss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/classic_addresses.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceclassicaddressescollection)
        """

    def page_size(self, count: int) -> ServiceResourceClassicAddressesCollection:
        """
        Fetch at most this many ClassicAddresss per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/classic_addresses.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceclassicaddressescollection)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[ClassicAddress]]:
        """
        A generator which yields pages of ClassicAddresss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/classic_addresses.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceclassicaddressescollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields ClassicAddresss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/classic_addresses.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceclassicaddressescollection)
        """

    def __aiter__(self) -> AsyncIterator[ClassicAddress]:
        """
        A generator which yields ClassicAddresss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/classic_addresses.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceclassicaddressescollection)
        """


class ServiceResourceDhcpOptionsSetsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/dhcp_options_sets.html#EC2.ServiceResource.dhcp_options_sets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcedhcpoptionssetscollection)
    """

    def all(self) -> ServiceResourceDhcpOptionsSetsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/dhcp_options_sets.html#EC2.ServiceResource.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcedhcpoptionssetscollection)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        DhcpOptionsIds: Sequence[str] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> ServiceResourceDhcpOptionsSetsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/dhcp_options_sets.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcedhcpoptionssetscollection)
        """

    def limit(self, count: int) -> ServiceResourceDhcpOptionsSetsCollection:
        """
        Return at most this many DhcpOptionss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/dhcp_options_sets.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcedhcpoptionssetscollection)
        """

    def page_size(self, count: int) -> ServiceResourceDhcpOptionsSetsCollection:
        """
        Fetch at most this many DhcpOptionss per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/dhcp_options_sets.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcedhcpoptionssetscollection)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[DhcpOptions]]:
        """
        A generator which yields pages of DhcpOptionss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/dhcp_options_sets.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcedhcpoptionssetscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields DhcpOptionss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/dhcp_options_sets.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcedhcpoptionssetscollection)
        """

    def __aiter__(self) -> AsyncIterator[DhcpOptions]:
        """
        A generator which yields DhcpOptionss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/dhcp_options_sets.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcedhcpoptionssetscollection)
        """


class ServiceResourceImagesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/images.html#EC2.ServiceResource.images)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceimagescollection)
    """

    def all(self) -> ServiceResourceImagesCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/images.html#EC2.ServiceResource.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceimagescollection)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        ExecutableUsers: Sequence[str] = ...,
        ImageIds: Sequence[str] = ...,
        Owners: Sequence[str] = ...,
        IncludeDeprecated: bool = ...,
        IncludeDisabled: bool = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> ServiceResourceImagesCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/images.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceimagescollection)
        """

    def limit(self, count: int) -> ServiceResourceImagesCollection:
        """
        Return at most this many Images.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/images.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceimagescollection)
        """

    def page_size(self, count: int) -> ServiceResourceImagesCollection:
        """
        Fetch at most this many Images per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/images.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceimagescollection)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[Image]]:
        """
        A generator which yields pages of Images.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/images.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceimagescollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Images.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/images.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceimagescollection)
        """

    def __aiter__(self) -> AsyncIterator[Image]:
        """
        A generator which yields Images.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/images.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceimagescollection)
        """


class ServiceResourceInstancesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/instances.html#EC2.ServiceResource.instances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
    """

    def all(self) -> ServiceResourceInstancesCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/instances.html#EC2.ServiceResource.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        InstanceIds: Sequence[str] = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ServiceResourceInstancesCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/instances.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    async def create_tags(self, *, DryRun: bool = ...) -> None:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/instances.html#create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    async def monitor(self, *, DryRun: bool = ...) -> List[MonitorInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/instances.html#monitor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    async def reboot(self, *, DryRun: bool = ...) -> None:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/instances.html#reboot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    async def start(
        self, *, AdditionalInfo: str = ..., DryRun: bool = ...
    ) -> List[StartInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/instances.html#start)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    async def stop(
        self, *, Hibernate: bool = ..., DryRun: bool = ..., Force: bool = ...
    ) -> List[StopInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/instances.html#stop)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    async def terminate(self, *, DryRun: bool = ...) -> List[TerminateInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/instances.html#terminate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    async def unmonitor(self, *, DryRun: bool = ...) -> List[UnmonitorInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/instances.html#unmonitor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    def limit(self, count: int) -> ServiceResourceInstancesCollection:
        """
        Return at most this many Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/instances.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    def page_size(self, count: int) -> ServiceResourceInstancesCollection:
        """
        Fetch at most this many Instances per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/instances.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[Instance]]:
        """
        A generator which yields pages of Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/instances.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/instances.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    def __aiter__(self) -> AsyncIterator[Instance]:
        """
        A generator which yields Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/instances.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """


class ServiceResourceInternetGatewaysCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/internet_gateways.html#EC2.ServiceResource.internet_gateways)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinternetgatewayscollection)
    """

    def all(self) -> ServiceResourceInternetGatewaysCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/internet_gateways.html#EC2.ServiceResource.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinternetgatewayscollection)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        InternetGatewayIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> ServiceResourceInternetGatewaysCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/internet_gateways.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinternetgatewayscollection)
        """

    def limit(self, count: int) -> ServiceResourceInternetGatewaysCollection:
        """
        Return at most this many InternetGateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/internet_gateways.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinternetgatewayscollection)
        """

    def page_size(self, count: int) -> ServiceResourceInternetGatewaysCollection:
        """
        Fetch at most this many InternetGateways per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/internet_gateways.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinternetgatewayscollection)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[InternetGateway]]:
        """
        A generator which yields pages of InternetGateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/internet_gateways.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinternetgatewayscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields InternetGateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/internet_gateways.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinternetgatewayscollection)
        """

    def __aiter__(self) -> AsyncIterator[InternetGateway]:
        """
        A generator which yields InternetGateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/internet_gateways.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinternetgatewayscollection)
        """


class ServiceResourceKeyPairsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/key_pairs.html#EC2.ServiceResource.key_pairs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcekeypairscollection)
    """

    def all(self) -> ServiceResourceKeyPairsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/key_pairs.html#EC2.ServiceResource.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcekeypairscollection)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        KeyNames: Sequence[str] = ...,
        KeyPairIds: Sequence[str] = ...,
        IncludePublicKey: bool = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> ServiceResourceKeyPairsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/key_pairs.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcekeypairscollection)
        """

    def limit(self, count: int) -> ServiceResourceKeyPairsCollection:
        """
        Return at most this many KeyPairInfos.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/key_pairs.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcekeypairscollection)
        """

    def page_size(self, count: int) -> ServiceResourceKeyPairsCollection:
        """
        Fetch at most this many KeyPairInfos per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/key_pairs.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcekeypairscollection)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[KeyPairInfo]]:
        """
        A generator which yields pages of KeyPairInfos.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/key_pairs.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcekeypairscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields KeyPairInfos.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/key_pairs.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcekeypairscollection)
        """

    def __aiter__(self) -> AsyncIterator[KeyPairInfo]:
        """
        A generator which yields KeyPairInfos.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/key_pairs.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcekeypairscollection)
        """


class ServiceResourceNetworkAclsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/network_acls.html#EC2.ServiceResource.network_acls)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkaclscollection)
    """

    def all(self) -> ServiceResourceNetworkAclsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/network_acls.html#EC2.ServiceResource.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkaclscollection)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        NetworkAclIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> ServiceResourceNetworkAclsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/network_acls.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkaclscollection)
        """

    def limit(self, count: int) -> ServiceResourceNetworkAclsCollection:
        """
        Return at most this many NetworkAcls.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/network_acls.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkaclscollection)
        """

    def page_size(self, count: int) -> ServiceResourceNetworkAclsCollection:
        """
        Fetch at most this many NetworkAcls per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/network_acls.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkaclscollection)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[NetworkAcl]]:
        """
        A generator which yields pages of NetworkAcls.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/network_acls.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkaclscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields NetworkAcls.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/network_acls.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkaclscollection)
        """

    def __aiter__(self) -> AsyncIterator[NetworkAcl]:
        """
        A generator which yields NetworkAcls.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/network_acls.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkaclscollection)
        """


class ServiceResourceNetworkInterfacesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/network_interfaces.html#EC2.ServiceResource.network_interfaces)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkinterfacescollection)
    """

    def all(self) -> ServiceResourceNetworkInterfacesCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/network_interfaces.html#EC2.ServiceResource.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkinterfacescollection)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        NetworkInterfaceIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> ServiceResourceNetworkInterfacesCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/network_interfaces.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkinterfacescollection)
        """

    def limit(self, count: int) -> ServiceResourceNetworkInterfacesCollection:
        """
        Return at most this many NetworkInterfaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/network_interfaces.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkinterfacescollection)
        """

    def page_size(self, count: int) -> ServiceResourceNetworkInterfacesCollection:
        """
        Fetch at most this many NetworkInterfaces per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/network_interfaces.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkinterfacescollection)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[NetworkInterface]]:
        """
        A generator which yields pages of NetworkInterfaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/network_interfaces.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkinterfacescollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields NetworkInterfaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/network_interfaces.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkinterfacescollection)
        """

    def __aiter__(self) -> AsyncIterator[NetworkInterface]:
        """
        A generator which yields NetworkInterfaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/network_interfaces.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkinterfacescollection)
        """


class ServiceResourcePlacementGroupsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/placement_groups.html#EC2.ServiceResource.placement_groups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceplacementgroupscollection)
    """

    def all(self) -> ServiceResourcePlacementGroupsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/placement_groups.html#EC2.ServiceResource.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceplacementgroupscollection)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        GroupIds: Sequence[str] = ...,
        DryRun: bool = ...,
        GroupNames: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> ServiceResourcePlacementGroupsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/placement_groups.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceplacementgroupscollection)
        """

    def limit(self, count: int) -> ServiceResourcePlacementGroupsCollection:
        """
        Return at most this many PlacementGroups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/placement_groups.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceplacementgroupscollection)
        """

    def page_size(self, count: int) -> ServiceResourcePlacementGroupsCollection:
        """
        Fetch at most this many PlacementGroups per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/placement_groups.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceplacementgroupscollection)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[PlacementGroup]]:
        """
        A generator which yields pages of PlacementGroups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/placement_groups.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceplacementgroupscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields PlacementGroups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/placement_groups.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceplacementgroupscollection)
        """

    def __aiter__(self) -> AsyncIterator[PlacementGroup]:
        """
        A generator which yields PlacementGroups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/placement_groups.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceplacementgroupscollection)
        """


class ServiceResourceRouteTablesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/route_tables.html#EC2.ServiceResource.route_tables)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceroutetablescollection)
    """

    def all(self) -> ServiceResourceRouteTablesCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/route_tables.html#EC2.ServiceResource.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceroutetablescollection)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        RouteTableIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> ServiceResourceRouteTablesCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/route_tables.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceroutetablescollection)
        """

    def limit(self, count: int) -> ServiceResourceRouteTablesCollection:
        """
        Return at most this many RouteTables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/route_tables.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceroutetablescollection)
        """

    def page_size(self, count: int) -> ServiceResourceRouteTablesCollection:
        """
        Fetch at most this many RouteTables per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/route_tables.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceroutetablescollection)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[RouteTable]]:
        """
        A generator which yields pages of RouteTables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/route_tables.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceroutetablescollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields RouteTables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/route_tables.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceroutetablescollection)
        """

    def __aiter__(self) -> AsyncIterator[RouteTable]:
        """
        A generator which yields RouteTables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/route_tables.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceroutetablescollection)
        """


class ServiceResourceSecurityGroupsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/security_groups.html#EC2.ServiceResource.security_groups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesecuritygroupscollection)
    """

    def all(self) -> ServiceResourceSecurityGroupsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/security_groups.html#EC2.ServiceResource.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesecuritygroupscollection)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        GroupIds: Sequence[str] = ...,
        GroupNames: Sequence[str] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> ServiceResourceSecurityGroupsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/security_groups.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesecuritygroupscollection)
        """

    def limit(self, count: int) -> ServiceResourceSecurityGroupsCollection:
        """
        Return at most this many SecurityGroups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/security_groups.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesecuritygroupscollection)
        """

    def page_size(self, count: int) -> ServiceResourceSecurityGroupsCollection:
        """
        Fetch at most this many SecurityGroups per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/security_groups.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesecuritygroupscollection)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[SecurityGroup]]:
        """
        A generator which yields pages of SecurityGroups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/security_groups.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesecuritygroupscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields SecurityGroups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/security_groups.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesecuritygroupscollection)
        """

    def __aiter__(self) -> AsyncIterator[SecurityGroup]:
        """
        A generator which yields SecurityGroups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/security_groups.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesecuritygroupscollection)
        """


class ServiceResourceSnapshotsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/snapshots.html#EC2.ServiceResource.snapshots)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesnapshotscollection)
    """

    def all(self) -> ServiceResourceSnapshotsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/snapshots.html#EC2.ServiceResource.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesnapshotscollection)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        MaxResults: int = ...,
        NextToken: str = ...,
        OwnerIds: Sequence[str] = ...,
        RestorableByUserIds: Sequence[str] = ...,
        SnapshotIds: Sequence[str] = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> ServiceResourceSnapshotsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/snapshots.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesnapshotscollection)
        """

    def limit(self, count: int) -> ServiceResourceSnapshotsCollection:
        """
        Return at most this many Snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/snapshots.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesnapshotscollection)
        """

    def page_size(self, count: int) -> ServiceResourceSnapshotsCollection:
        """
        Fetch at most this many Snapshots per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/snapshots.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesnapshotscollection)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[Snapshot]]:
        """
        A generator which yields pages of Snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/snapshots.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesnapshotscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/snapshots.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesnapshotscollection)
        """

    def __aiter__(self) -> AsyncIterator[Snapshot]:
        """
        A generator which yields Snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/snapshots.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesnapshotscollection)
        """


class ServiceResourceSubnetsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/subnets.html#EC2.ServiceResource.subnets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesubnetscollection)
    """

    def all(self) -> ServiceResourceSubnetsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/subnets.html#EC2.ServiceResource.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesubnetscollection)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        Filters: Sequence[FilterTypeDef] = ...,
        SubnetIds: Sequence[str] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
    ) -> ServiceResourceSubnetsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/subnets.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesubnetscollection)
        """

    def limit(self, count: int) -> ServiceResourceSubnetsCollection:
        """
        Return at most this many Subnets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/subnets.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesubnetscollection)
        """

    def page_size(self, count: int) -> ServiceResourceSubnetsCollection:
        """
        Fetch at most this many Subnets per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/subnets.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesubnetscollection)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[Subnet]]:
        """
        A generator which yields pages of Subnets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/subnets.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesubnetscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Subnets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/subnets.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesubnetscollection)
        """

    def __aiter__(self) -> AsyncIterator[Subnet]:
        """
        A generator which yields Subnets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/subnets.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesubnetscollection)
        """


class ServiceResourceVolumesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/volumes.html#EC2.ServiceResource.volumes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevolumescollection)
    """

    def all(self) -> ServiceResourceVolumesCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/volumes.html#EC2.ServiceResource.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevolumescollection)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        VolumeIds: Sequence[str] = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ServiceResourceVolumesCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/volumes.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevolumescollection)
        """

    def limit(self, count: int) -> ServiceResourceVolumesCollection:
        """
        Return at most this many Volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/volumes.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevolumescollection)
        """

    def page_size(self, count: int) -> ServiceResourceVolumesCollection:
        """
        Fetch at most this many Volumes per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/volumes.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevolumescollection)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[Volume]]:
        """
        A generator which yields pages of Volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/volumes.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevolumescollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/volumes.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevolumescollection)
        """

    def __aiter__(self) -> AsyncIterator[Volume]:
        """
        A generator which yields Volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/volumes.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevolumescollection)
        """


class ServiceResourceVpcAddressesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpc_addresses.html#EC2.ServiceResource.vpc_addresses)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcaddressescollection)
    """

    def all(self) -> ServiceResourceVpcAddressesCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpc_addresses.html#EC2.ServiceResource.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcaddressescollection)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        PublicIps: Sequence[str] = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        AllocationIds: Sequence[str] = ...,
    ) -> ServiceResourceVpcAddressesCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpc_addresses.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcaddressescollection)
        """

    def limit(self, count: int) -> ServiceResourceVpcAddressesCollection:
        """
        Return at most this many VpcAddresss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpc_addresses.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcaddressescollection)
        """

    def page_size(self, count: int) -> ServiceResourceVpcAddressesCollection:
        """
        Fetch at most this many VpcAddresss per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpc_addresses.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcaddressescollection)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[VpcAddress]]:
        """
        A generator which yields pages of VpcAddresss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpc_addresses.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcaddressescollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields VpcAddresss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpc_addresses.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcaddressescollection)
        """

    def __aiter__(self) -> AsyncIterator[VpcAddress]:
        """
        A generator which yields VpcAddresss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpc_addresses.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcaddressescollection)
        """


class ServiceResourceVpcPeeringConnectionsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpc_peering_connections.html#EC2.ServiceResource.vpc_peering_connections)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcpeeringconnectionscollection)
    """

    def all(self) -> ServiceResourceVpcPeeringConnectionsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpc_peering_connections.html#EC2.ServiceResource.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcpeeringconnectionscollection)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        VpcPeeringConnectionIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> ServiceResourceVpcPeeringConnectionsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpc_peering_connections.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcpeeringconnectionscollection)
        """

    def limit(self, count: int) -> ServiceResourceVpcPeeringConnectionsCollection:
        """
        Return at most this many VpcPeeringConnections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpc_peering_connections.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcpeeringconnectionscollection)
        """

    def page_size(self, count: int) -> ServiceResourceVpcPeeringConnectionsCollection:
        """
        Fetch at most this many VpcPeeringConnections per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpc_peering_connections.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcpeeringconnectionscollection)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[VpcPeeringConnection]]:
        """
        A generator which yields pages of VpcPeeringConnections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpc_peering_connections.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcpeeringconnectionscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields VpcPeeringConnections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpc_peering_connections.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcpeeringconnectionscollection)
        """

    def __aiter__(self) -> AsyncIterator[VpcPeeringConnection]:
        """
        A generator which yields VpcPeeringConnections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpc_peering_connections.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcpeeringconnectionscollection)
        """


class ServiceResourceVpcsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpcs.html#EC2.ServiceResource.vpcs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcscollection)
    """

    def all(self) -> ServiceResourceVpcsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpcs.html#EC2.ServiceResource.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcscollection)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        Filters: Sequence[FilterTypeDef] = ...,
        VpcIds: Sequence[str] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
    ) -> ServiceResourceVpcsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpcs.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcscollection)
        """

    def limit(self, count: int) -> ServiceResourceVpcsCollection:
        """
        Return at most this many Vpcs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpcs.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcscollection)
        """

    def page_size(self, count: int) -> ServiceResourceVpcsCollection:
        """
        Fetch at most this many Vpcs per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpcs.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcscollection)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[Vpc]]:
        """
        A generator which yields pages of Vpcs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpcs.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Vpcs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpcs.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcscollection)
        """

    def __aiter__(self) -> AsyncIterator[Vpc]:
        """
        A generator which yields Vpcs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/vpcs.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcscollection)
        """


class InstanceVolumesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/volumes.html#EC2.Instance.volumes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancevolumes)
    """

    def all(self) -> InstanceVolumesCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/volumes.html#EC2.Instance.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancevolumes)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        VolumeIds: Sequence[str] = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> InstanceVolumesCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/volumes.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancevolumes)
        """

    def limit(self, count: int) -> InstanceVolumesCollection:
        """
        Return at most this many Volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/volumes.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancevolumes)
        """

    def page_size(self, count: int) -> InstanceVolumesCollection:
        """
        Fetch at most this many Volumes per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/volumes.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancevolumes)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[Volume]]:
        """
        A generator which yields pages of Volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/volumes.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancevolumes)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/volumes.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancevolumes)
        """

    def __aiter__(self) -> AsyncIterator[Volume]:
        """
        A generator which yields Volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/volumes.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancevolumes)
        """


class InstanceVpcAddressesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/vpc_addresses.html#EC2.Instance.vpc_addresses)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancevpc_addresses)
    """

    def all(self) -> InstanceVpcAddressesCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/vpc_addresses.html#EC2.Instance.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancevpc_addresses)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        PublicIps: Sequence[str] = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        AllocationIds: Sequence[str] = ...,
    ) -> InstanceVpcAddressesCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/vpc_addresses.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancevpc_addresses)
        """

    def limit(self, count: int) -> InstanceVpcAddressesCollection:
        """
        Return at most this many VpcAddresss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/vpc_addresses.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancevpc_addresses)
        """

    def page_size(self, count: int) -> InstanceVpcAddressesCollection:
        """
        Fetch at most this many VpcAddresss per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/vpc_addresses.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancevpc_addresses)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[VpcAddress]]:
        """
        A generator which yields pages of VpcAddresss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/vpc_addresses.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancevpc_addresses)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields VpcAddresss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/vpc_addresses.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancevpc_addresses)
        """

    def __aiter__(self) -> AsyncIterator[VpcAddress]:
        """
        A generator which yields VpcAddresss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/vpc_addresses.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancevpc_addresses)
        """


class PlacementGroupInstancesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/placementgroup/instances.html#EC2.PlacementGroup.instances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroupinstances)
    """

    def all(self) -> PlacementGroupInstancesCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/placementgroup/instances.html#EC2.PlacementGroup.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroupinstances)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        InstanceIds: Sequence[str] = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> PlacementGroupInstancesCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/placementgroup/instances.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroupinstances)
        """

    async def create_tags(self, *, DryRun: bool = ...) -> None:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/placementgroup/instances.html#create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroupinstances)
        """

    async def monitor(self, *, DryRun: bool = ...) -> List[MonitorInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/placementgroup/instances.html#monitor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroupinstances)
        """

    async def reboot(self, *, DryRun: bool = ...) -> None:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/placementgroup/instances.html#reboot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroupinstances)
        """

    async def start(
        self, *, AdditionalInfo: str = ..., DryRun: bool = ...
    ) -> List[StartInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/placementgroup/instances.html#start)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroupinstances)
        """

    async def stop(
        self, *, Hibernate: bool = ..., DryRun: bool = ..., Force: bool = ...
    ) -> List[StopInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/placementgroup/instances.html#stop)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroupinstances)
        """

    async def terminate(self, *, DryRun: bool = ...) -> List[TerminateInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/placementgroup/instances.html#terminate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroupinstances)
        """

    async def unmonitor(self, *, DryRun: bool = ...) -> List[UnmonitorInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/placementgroup/instances.html#unmonitor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroupinstances)
        """

    def limit(self, count: int) -> PlacementGroupInstancesCollection:
        """
        Return at most this many Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/placementgroup/instances.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroupinstances)
        """

    def page_size(self, count: int) -> PlacementGroupInstancesCollection:
        """
        Fetch at most this many Instances per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/placementgroup/instances.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroupinstances)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[Instance]]:
        """
        A generator which yields pages of Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/placementgroup/instances.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroupinstances)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/placementgroup/instances.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroupinstances)
        """

    def __aiter__(self) -> AsyncIterator[Instance]:
        """
        A generator which yields Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/placementgroup/instances.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroupinstances)
        """


class SubnetInstancesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/instances.html#EC2.Subnet.instances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetinstances)
    """

    def all(self) -> SubnetInstancesCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/instances.html#EC2.Subnet.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetinstances)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        InstanceIds: Sequence[str] = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> SubnetInstancesCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/instances.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetinstances)
        """

    async def create_tags(self, *, DryRun: bool = ...) -> None:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/instances.html#create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetinstances)
        """

    async def monitor(self, *, DryRun: bool = ...) -> List[MonitorInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/instances.html#monitor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetinstances)
        """

    async def reboot(self, *, DryRun: bool = ...) -> None:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/instances.html#reboot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetinstances)
        """

    async def start(
        self, *, AdditionalInfo: str = ..., DryRun: bool = ...
    ) -> List[StartInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/instances.html#start)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetinstances)
        """

    async def stop(
        self, *, Hibernate: bool = ..., DryRun: bool = ..., Force: bool = ...
    ) -> List[StopInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/instances.html#stop)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetinstances)
        """

    async def terminate(self, *, DryRun: bool = ...) -> List[TerminateInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/instances.html#terminate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetinstances)
        """

    async def unmonitor(self, *, DryRun: bool = ...) -> List[UnmonitorInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/instances.html#unmonitor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetinstances)
        """

    def limit(self, count: int) -> SubnetInstancesCollection:
        """
        Return at most this many Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/instances.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetinstances)
        """

    def page_size(self, count: int) -> SubnetInstancesCollection:
        """
        Fetch at most this many Instances per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/instances.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetinstances)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[Instance]]:
        """
        A generator which yields pages of Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/instances.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetinstances)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/instances.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetinstances)
        """

    def __aiter__(self) -> AsyncIterator[Instance]:
        """
        A generator which yields Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/instances.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetinstances)
        """


class SubnetNetworkInterfacesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/network_interfaces.html#EC2.Subnet.network_interfaces)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetnetwork_interfaces)
    """

    def all(self) -> SubnetNetworkInterfacesCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/network_interfaces.html#EC2.Subnet.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetnetwork_interfaces)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        NetworkInterfaceIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> SubnetNetworkInterfacesCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/network_interfaces.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetnetwork_interfaces)
        """

    def limit(self, count: int) -> SubnetNetworkInterfacesCollection:
        """
        Return at most this many NetworkInterfaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/network_interfaces.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetnetwork_interfaces)
        """

    def page_size(self, count: int) -> SubnetNetworkInterfacesCollection:
        """
        Fetch at most this many NetworkInterfaces per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/network_interfaces.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetnetwork_interfaces)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[NetworkInterface]]:
        """
        A generator which yields pages of NetworkInterfaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/network_interfaces.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetnetwork_interfaces)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields NetworkInterfaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/network_interfaces.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetnetwork_interfaces)
        """

    def __aiter__(self) -> AsyncIterator[NetworkInterface]:
        """
        A generator which yields NetworkInterfaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/network_interfaces.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetnetwork_interfaces)
        """


class VolumeSnapshotsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/volume/snapshots.html#EC2.Volume.snapshots)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumesnapshots)
    """

    def all(self) -> VolumeSnapshotsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/volume/snapshots.html#EC2.Volume.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumesnapshots)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        MaxResults: int = ...,
        NextToken: str = ...,
        OwnerIds: Sequence[str] = ...,
        RestorableByUserIds: Sequence[str] = ...,
        SnapshotIds: Sequence[str] = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> VolumeSnapshotsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/volume/snapshots.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumesnapshots)
        """

    def limit(self, count: int) -> VolumeSnapshotsCollection:
        """
        Return at most this many Snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/volume/snapshots.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumesnapshots)
        """

    def page_size(self, count: int) -> VolumeSnapshotsCollection:
        """
        Fetch at most this many Snapshots per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/volume/snapshots.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumesnapshots)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[Snapshot]]:
        """
        A generator which yields pages of Snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/volume/snapshots.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumesnapshots)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/volume/snapshots.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumesnapshots)
        """

    def __aiter__(self) -> AsyncIterator[Snapshot]:
        """
        A generator which yields Snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/volume/snapshots.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumesnapshots)
        """


class VpcAcceptedVpcPeeringConnectionsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/accepted_vpc_peering_connections.html#EC2.Vpc.accepted_vpc_peering_connections)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcaccepted_vpc_peering_connections)
    """

    def all(self) -> VpcAcceptedVpcPeeringConnectionsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/accepted_vpc_peering_connections.html#EC2.Vpc.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcaccepted_vpc_peering_connections)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        VpcPeeringConnectionIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> VpcAcceptedVpcPeeringConnectionsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/accepted_vpc_peering_connections.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcaccepted_vpc_peering_connections)
        """

    def limit(self, count: int) -> VpcAcceptedVpcPeeringConnectionsCollection:
        """
        Return at most this many VpcPeeringConnections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/accepted_vpc_peering_connections.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcaccepted_vpc_peering_connections)
        """

    def page_size(self, count: int) -> VpcAcceptedVpcPeeringConnectionsCollection:
        """
        Fetch at most this many VpcPeeringConnections per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/accepted_vpc_peering_connections.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcaccepted_vpc_peering_connections)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[VpcPeeringConnection]]:
        """
        A generator which yields pages of VpcPeeringConnections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/accepted_vpc_peering_connections.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcaccepted_vpc_peering_connections)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields VpcPeeringConnections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/accepted_vpc_peering_connections.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcaccepted_vpc_peering_connections)
        """

    def __aiter__(self) -> AsyncIterator[VpcPeeringConnection]:
        """
        A generator which yields VpcPeeringConnections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/accepted_vpc_peering_connections.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcaccepted_vpc_peering_connections)
        """


class VpcInstancesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/instances.html#EC2.Vpc.instances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcinstances)
    """

    def all(self) -> VpcInstancesCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/instances.html#EC2.Vpc.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcinstances)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        InstanceIds: Sequence[str] = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> VpcInstancesCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/instances.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcinstances)
        """

    async def create_tags(self, *, DryRun: bool = ...) -> None:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/instances.html#create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcinstances)
        """

    async def monitor(self, *, DryRun: bool = ...) -> List[MonitorInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/instances.html#monitor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcinstances)
        """

    async def reboot(self, *, DryRun: bool = ...) -> None:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/instances.html#reboot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcinstances)
        """

    async def start(
        self, *, AdditionalInfo: str = ..., DryRun: bool = ...
    ) -> List[StartInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/instances.html#start)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcinstances)
        """

    async def stop(
        self, *, Hibernate: bool = ..., DryRun: bool = ..., Force: bool = ...
    ) -> List[StopInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/instances.html#stop)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcinstances)
        """

    async def terminate(self, *, DryRun: bool = ...) -> List[TerminateInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/instances.html#terminate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcinstances)
        """

    async def unmonitor(self, *, DryRun: bool = ...) -> List[UnmonitorInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/instances.html#unmonitor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcinstances)
        """

    def limit(self, count: int) -> VpcInstancesCollection:
        """
        Return at most this many Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/instances.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcinstances)
        """

    def page_size(self, count: int) -> VpcInstancesCollection:
        """
        Fetch at most this many Instances per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/instances.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcinstances)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[Instance]]:
        """
        A generator which yields pages of Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/instances.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcinstances)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/instances.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcinstances)
        """

    def __aiter__(self) -> AsyncIterator[Instance]:
        """
        A generator which yields Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/instances.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcinstances)
        """


class VpcInternetGatewaysCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/internet_gateways.html#EC2.Vpc.internet_gateways)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcinternet_gateways)
    """

    def all(self) -> VpcInternetGatewaysCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/internet_gateways.html#EC2.Vpc.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcinternet_gateways)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        InternetGatewayIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> VpcInternetGatewaysCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/internet_gateways.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcinternet_gateways)
        """

    def limit(self, count: int) -> VpcInternetGatewaysCollection:
        """
        Return at most this many InternetGateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/internet_gateways.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcinternet_gateways)
        """

    def page_size(self, count: int) -> VpcInternetGatewaysCollection:
        """
        Fetch at most this many InternetGateways per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/internet_gateways.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcinternet_gateways)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[InternetGateway]]:
        """
        A generator which yields pages of InternetGateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/internet_gateways.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcinternet_gateways)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields InternetGateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/internet_gateways.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcinternet_gateways)
        """

    def __aiter__(self) -> AsyncIterator[InternetGateway]:
        """
        A generator which yields InternetGateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/internet_gateways.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcinternet_gateways)
        """


class VpcNetworkAclsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/network_acls.html#EC2.Vpc.network_acls)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcnetwork_acls)
    """

    def all(self) -> VpcNetworkAclsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/network_acls.html#EC2.Vpc.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcnetwork_acls)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        NetworkAclIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> VpcNetworkAclsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/network_acls.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcnetwork_acls)
        """

    def limit(self, count: int) -> VpcNetworkAclsCollection:
        """
        Return at most this many NetworkAcls.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/network_acls.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcnetwork_acls)
        """

    def page_size(self, count: int) -> VpcNetworkAclsCollection:
        """
        Fetch at most this many NetworkAcls per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/network_acls.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcnetwork_acls)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[NetworkAcl]]:
        """
        A generator which yields pages of NetworkAcls.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/network_acls.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcnetwork_acls)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields NetworkAcls.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/network_acls.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcnetwork_acls)
        """

    def __aiter__(self) -> AsyncIterator[NetworkAcl]:
        """
        A generator which yields NetworkAcls.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/network_acls.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcnetwork_acls)
        """


class VpcNetworkInterfacesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/network_interfaces.html#EC2.Vpc.network_interfaces)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcnetwork_interfaces)
    """

    def all(self) -> VpcNetworkInterfacesCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/network_interfaces.html#EC2.Vpc.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcnetwork_interfaces)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        NetworkInterfaceIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> VpcNetworkInterfacesCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/network_interfaces.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcnetwork_interfaces)
        """

    def limit(self, count: int) -> VpcNetworkInterfacesCollection:
        """
        Return at most this many NetworkInterfaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/network_interfaces.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcnetwork_interfaces)
        """

    def page_size(self, count: int) -> VpcNetworkInterfacesCollection:
        """
        Fetch at most this many NetworkInterfaces per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/network_interfaces.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcnetwork_interfaces)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[NetworkInterface]]:
        """
        A generator which yields pages of NetworkInterfaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/network_interfaces.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcnetwork_interfaces)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields NetworkInterfaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/network_interfaces.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcnetwork_interfaces)
        """

    def __aiter__(self) -> AsyncIterator[NetworkInterface]:
        """
        A generator which yields NetworkInterfaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/network_interfaces.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcnetwork_interfaces)
        """


class VpcRequestedVpcPeeringConnectionsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/requested_vpc_peering_connections.html#EC2.Vpc.requested_vpc_peering_connections)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcrequested_vpc_peering_connections)
    """

    def all(self) -> VpcRequestedVpcPeeringConnectionsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/requested_vpc_peering_connections.html#EC2.Vpc.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcrequested_vpc_peering_connections)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        VpcPeeringConnectionIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> VpcRequestedVpcPeeringConnectionsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/requested_vpc_peering_connections.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcrequested_vpc_peering_connections)
        """

    def limit(self, count: int) -> VpcRequestedVpcPeeringConnectionsCollection:
        """
        Return at most this many VpcPeeringConnections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/requested_vpc_peering_connections.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcrequested_vpc_peering_connections)
        """

    def page_size(self, count: int) -> VpcRequestedVpcPeeringConnectionsCollection:
        """
        Fetch at most this many VpcPeeringConnections per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/requested_vpc_peering_connections.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcrequested_vpc_peering_connections)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[VpcPeeringConnection]]:
        """
        A generator which yields pages of VpcPeeringConnections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/requested_vpc_peering_connections.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcrequested_vpc_peering_connections)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields VpcPeeringConnections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/requested_vpc_peering_connections.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcrequested_vpc_peering_connections)
        """

    def __aiter__(self) -> AsyncIterator[VpcPeeringConnection]:
        """
        A generator which yields VpcPeeringConnections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/requested_vpc_peering_connections.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcrequested_vpc_peering_connections)
        """


class VpcRouteTablesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/route_tables.html#EC2.Vpc.route_tables)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcroute_tables)
    """

    def all(self) -> VpcRouteTablesCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/route_tables.html#EC2.Vpc.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcroute_tables)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        RouteTableIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> VpcRouteTablesCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/route_tables.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcroute_tables)
        """

    def limit(self, count: int) -> VpcRouteTablesCollection:
        """
        Return at most this many RouteTables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/route_tables.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcroute_tables)
        """

    def page_size(self, count: int) -> VpcRouteTablesCollection:
        """
        Fetch at most this many RouteTables per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/route_tables.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcroute_tables)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[RouteTable]]:
        """
        A generator which yields pages of RouteTables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/route_tables.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcroute_tables)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields RouteTables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/route_tables.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcroute_tables)
        """

    def __aiter__(self) -> AsyncIterator[RouteTable]:
        """
        A generator which yields RouteTables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/route_tables.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcroute_tables)
        """


class VpcSecurityGroupsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/security_groups.html#EC2.Vpc.security_groups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcsecurity_groups)
    """

    def all(self) -> VpcSecurityGroupsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/security_groups.html#EC2.Vpc.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcsecurity_groups)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        GroupIds: Sequence[str] = ...,
        GroupNames: Sequence[str] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> VpcSecurityGroupsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/security_groups.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcsecurity_groups)
        """

    def limit(self, count: int) -> VpcSecurityGroupsCollection:
        """
        Return at most this many SecurityGroups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/security_groups.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcsecurity_groups)
        """

    def page_size(self, count: int) -> VpcSecurityGroupsCollection:
        """
        Fetch at most this many SecurityGroups per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/security_groups.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcsecurity_groups)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[SecurityGroup]]:
        """
        A generator which yields pages of SecurityGroups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/security_groups.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcsecurity_groups)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields SecurityGroups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/security_groups.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcsecurity_groups)
        """

    def __aiter__(self) -> AsyncIterator[SecurityGroup]:
        """
        A generator which yields SecurityGroups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/security_groups.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcsecurity_groups)
        """


class VpcSubnetsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/subnets.html#EC2.Vpc.subnets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcsubnets)
    """

    def all(self) -> VpcSubnetsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/subnets.html#EC2.Vpc.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcsubnets)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        Filters: Sequence[FilterTypeDef] = ...,
        SubnetIds: Sequence[str] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
    ) -> VpcSubnetsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/subnets.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcsubnets)
        """

    def limit(self, count: int) -> VpcSubnetsCollection:
        """
        Return at most this many Subnets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/subnets.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcsubnets)
        """

    def page_size(self, count: int) -> VpcSubnetsCollection:
        """
        Fetch at most this many Subnets per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/subnets.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcsubnets)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[Subnet]]:
        """
        A generator which yields pages of Subnets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/subnets.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcsubnets)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Subnets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/subnets.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcsubnets)
        """

    def __aiter__(self) -> AsyncIterator[Subnet]:
        """
        A generator which yields Subnets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/subnets.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcsubnets)
        """


class ClassicAddress(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/classicaddress/index.html#EC2.ClassicAddress)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#classicaddress)
    """

    public_ip: str
    allocation_id: Awaitable[str]
    association_id: Awaitable[str]
    domain: Awaitable[DomainTypeType]
    network_interface_id: Awaitable[str]
    network_interface_owner_id: Awaitable[str]
    private_ip_address: Awaitable[str]
    tags: Awaitable[List[TagTypeDef]]
    public_ipv4_pool: Awaitable[str]
    network_border_group: Awaitable[str]
    customer_owned_ip: Awaitable[str]
    customer_owned_ipv4_pool: Awaitable[str]
    carrier_ip: Awaitable[str]
    subnet_id: Awaitable[str]
    service_managed: Awaitable[ServiceManagedType]
    instance_id: Awaitable[str]
    meta: EC2ResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this ClassicAddress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/classicaddress/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#classicaddressget_available_subresources-method)
        """

    async def associate(
        self, **kwargs: Unpack[AssociateAddressRequestClassicAddressAssociateTypeDef]
    ) -> AssociateAddressResultTypeDef:
        """
        Associates an Elastic IP address, or carrier IP address (for instances that are
        in subnets in Wavelength Zones) with an instance or a network interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/classicaddress/associate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#classicaddressassociate-method)
        """

    async def disassociate(
        self, **kwargs: Unpack[DisassociateAddressRequestClassicAddressDisassociateTypeDef]
    ) -> None:
        """
        Disassociates an Elastic IP address from the instance or network interface it's
        associated with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/classicaddress/disassociate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#classicaddressdisassociate-method)
        """

    async def release(
        self, **kwargs: Unpack[ReleaseAddressRequestClassicAddressReleaseTypeDef]
    ) -> None:
        """
        Releases the specified Elastic IP address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/classicaddress/release.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#classicaddressrelease-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/classicaddress/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#classicaddressload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/classicaddress/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#classicaddressreload-method)
        """


_ClassicAddress = ClassicAddress


class DhcpOptions(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/dhcpoptions/index.html#EC2.DhcpOptions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptions)
    """

    id: str
    owner_id: Awaitable[str]
    tags: Awaitable[List[TagTypeDef]]
    dhcp_options_id: Awaitable[str]
    dhcp_configurations: Awaitable[List[DhcpConfigurationTypeDef]]
    meta: EC2ResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this DhcpOptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/dhcpoptions/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptionsget_available_subresources-method)
        """

    async def associate_with_vpc(
        self, **kwargs: Unpack[AssociateDhcpOptionsRequestDhcpOptionsAssociateWithVpcTypeDef]
    ) -> None:
        """
        Associates a set of DHCP options (that you've previously created) with the
        specified VPC, or associates no DHCP options with the VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/dhcpoptions/associate_with_vpc.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptionsassociate_with_vpc-method)
        """

    async def create_tags(self, **kwargs: Unpack[DhcpOptionsCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/dhcpoptions/create_tags.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptionscreate_tags-method)
        """

    async def delete(
        self, **kwargs: Unpack[DeleteDhcpOptionsRequestDhcpOptionsDeleteTypeDef]
    ) -> None:
        """
        Deletes the specified set of DHCP options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/dhcpoptions/delete.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptionsdelete-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/dhcpoptions/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptionsload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/dhcpoptions/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptionsreload-method)
        """


_DhcpOptions = DhcpOptions


class Image(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/image/index.html#EC2.Image)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#image)
    """

    id: str
    platform_details: Awaitable[str]
    usage_operation: Awaitable[str]
    block_device_mappings: Awaitable[List[BlockDeviceMappingTypeDef]]
    description: Awaitable[str]
    ena_support: Awaitable[bool]
    hypervisor: Awaitable[HypervisorTypeType]
    image_owner_alias: Awaitable[str]
    name: Awaitable[str]
    root_device_name: Awaitable[str]
    root_device_type: Awaitable[DeviceTypeType]
    sriov_net_support: Awaitable[str]
    state_reason: Awaitable[StateReasonTypeDef]
    tags: Awaitable[List[TagTypeDef]]
    virtualization_type: Awaitable[VirtualizationTypeType]
    boot_mode: Awaitable[BootModeValuesType]
    tpm_support: Awaitable[Literal["v2.0"]]
    deprecation_time: Awaitable[str]
    imds_support: Awaitable[Literal["v2.0"]]
    source_instance_id: Awaitable[str]
    deregistration_protection: Awaitable[str]
    last_launched_time: Awaitable[str]
    image_allowed: Awaitable[bool]
    source_image_id: Awaitable[str]
    source_image_region: Awaitable[str]
    free_tier_eligible: Awaitable[bool]
    image_id: Awaitable[str]
    image_location: Awaitable[str]
    state: Awaitable[ImageStateType]
    owner_id: Awaitable[str]
    creation_date: Awaitable[str]
    public: Awaitable[bool]
    product_codes: Awaitable[List[ProductCodeTypeDef]]
    architecture: Awaitable[ArchitectureValuesType]
    image_type: Awaitable[ImageTypeValuesType]
    kernel_id: Awaitable[str]
    ramdisk_id: Awaitable[str]
    platform: Awaitable[Literal["windows"]]
    meta: EC2ResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/image/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imageget_available_subresources-method)
        """

    async def create_tags(self, **kwargs: Unpack[ImageCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/image/create_tags.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagecreate_tags-method)
        """

    async def deregister(
        self, **kwargs: Unpack[DeregisterImageRequestImageDeregisterTypeDef]
    ) -> DeregisterImageResultTypeDef:
        """
        Deregisters the specified AMI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/image/deregister.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagederegister-method)
        """

    async def describe_attribute(
        self, **kwargs: Unpack[DescribeImageAttributeRequestImageDescribeAttributeTypeDef]
    ) -> ImageAttributeTypeDef:
        """
        Describes the specified attribute of the specified AMI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/image/describe_attribute.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagedescribe_attribute-method)
        """

    async def modify_attribute(
        self, **kwargs: Unpack[ModifyImageAttributeRequestImageModifyAttributeTypeDef]
    ) -> None:
        """
        Modifies the specified attribute of the specified AMI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/image/modify_attribute.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagemodify_attribute-method)
        """

    async def reset_attribute(
        self, **kwargs: Unpack[ResetImageAttributeRequestImageResetAttributeTypeDef]
    ) -> None:
        """
        Resets an attribute of an AMI to its default value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/image/reset_attribute.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagereset_attribute-method)
        """

    async def wait_until_exists(self) -> None:
        """
        Waits until Image is exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/image/wait_until_exists.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagewait_until_exists-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/image/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imageload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/image/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagereload-method)
        """


_Image = Image


class Instance(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/index.html#EC2.Instance)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instance)
    """

    id: str
    classic_address: ClassicAddress
    image: Image
    key_pair: KeyPairInfo
    network_interfaces: List[NetworkInterface]
    placement_group: PlacementGroup
    subnet: Subnet
    vpc: Vpc
    volumes: InstanceVolumesCollection
    vpc_addresses: InstanceVpcAddressesCollection
    architecture: Awaitable[ArchitectureValuesType]
    block_device_mappings: Awaitable[List[InstanceBlockDeviceMappingTypeDef]]
    client_token: Awaitable[str]
    ebs_optimized: Awaitable[bool]
    ena_support: Awaitable[bool]
    hypervisor: Awaitable[HypervisorTypeType]
    iam_instance_profile: Awaitable[IamInstanceProfileTypeDef]
    instance_lifecycle: Awaitable[InstanceLifecycleTypeType]
    elastic_gpu_associations: Awaitable[List[ElasticGpuAssociationTypeDef]]
    elastic_inference_accelerator_associations: Awaitable[
        List[ElasticInferenceAcceleratorAssociationTypeDef]
    ]
    network_interfaces_attribute: Awaitable[List[InstanceNetworkInterfaceTypeDef]]
    outpost_arn: Awaitable[str]
    root_device_name: Awaitable[str]
    root_device_type: Awaitable[DeviceTypeType]
    security_groups: Awaitable[List[GroupIdentifierTypeDef]]
    source_dest_check: Awaitable[bool]
    spot_instance_request_id: Awaitable[str]
    sriov_net_support: Awaitable[str]
    state_reason: Awaitable[StateReasonTypeDef]
    tags: Awaitable[List[TagTypeDef]]
    virtualization_type: Awaitable[VirtualizationTypeType]
    cpu_options: Awaitable[CpuOptionsTypeDef]
    capacity_block_id: Awaitable[str]
    capacity_reservation_id: Awaitable[str]
    capacity_reservation_specification: Awaitable[CapacityReservationSpecificationResponseTypeDef]
    hibernation_options: Awaitable[HibernationOptionsTypeDef]
    licenses: Awaitable[List[LicenseConfigurationTypeDef]]
    metadata_options: Awaitable[InstanceMetadataOptionsResponseTypeDef]
    enclave_options: Awaitable[EnclaveOptionsTypeDef]
    boot_mode: Awaitable[BootModeValuesType]
    platform_details: Awaitable[str]
    usage_operation: Awaitable[str]
    usage_operation_update_time: Awaitable[datetime]
    private_dns_name_options: Awaitable[PrivateDnsNameOptionsResponseTypeDef]
    ipv6_address: Awaitable[str]
    tpm_support: Awaitable[str]
    maintenance_options: Awaitable[InstanceMaintenanceOptionsTypeDef]
    current_instance_boot_mode: Awaitable[InstanceBootModeValuesType]
    network_performance_options: Awaitable[InstanceNetworkPerformanceOptionsTypeDef]
    operator: Awaitable[OperatorResponseTypeDef]
    instance_id: Awaitable[str]
    image_id: Awaitable[str]
    state: Awaitable[InstanceStateTypeDef]
    private_dns_name: Awaitable[str]
    public_dns_name: Awaitable[str]
    state_transition_reason: Awaitable[str]
    key_name: Awaitable[str]
    ami_launch_index: Awaitable[int]
    product_codes: Awaitable[List[ProductCodeTypeDef]]
    instance_type: Awaitable[InstanceTypeType]
    launch_time: Awaitable[datetime]
    placement: Awaitable[PlacementTypeDef]
    kernel_id: Awaitable[str]
    ramdisk_id: Awaitable[str]
    platform: Awaitable[Literal["windows"]]
    monitoring: Awaitable[MonitoringTypeDef]
    subnet_id: Awaitable[str]
    vpc_id: Awaitable[str]
    private_ip_address: Awaitable[str]
    public_ip_address: Awaitable[str]
    meta: EC2ResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instanceget_available_subresources-method)
        """

    async def attach_classic_link_vpc(
        self, **kwargs: Unpack[AttachClassicLinkVpcRequestInstanceAttachClassicLinkVpcTypeDef]
    ) -> AttachClassicLinkVpcResultTypeDef:
        """
        This action is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/attach_classic_link_vpc.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instanceattach_classic_link_vpc-method)
        """

    async def attach_volume(
        self, **kwargs: Unpack[AttachVolumeRequestInstanceAttachVolumeTypeDef]
    ) -> VolumeAttachmentResponseTypeDef:
        """
        Attaches an Amazon EBS volume to a <code>running</code> or <code>stopped</code>
        instance, and exposes it to the instance with the specified device name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/attach_volume.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instanceattach_volume-method)
        """

    async def console_output(
        self, **kwargs: Unpack[GetConsoleOutputRequestInstanceConsoleOutputTypeDef]
    ) -> GetConsoleOutputResultTypeDef:
        """
        Gets the console output for the specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/console_output.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instanceconsole_output-method)
        """

    async def create_image(
        self, **kwargs: Unpack[CreateImageRequestInstanceCreateImageTypeDef]
    ) -> _Image:
        """
        Creates an Amazon EBS-backed AMI from an Amazon EBS-backed instance that is
        either running or stopped.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/create_image.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancecreate_image-method)
        """

    async def create_tags(self, **kwargs: Unpack[InstanceCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/create_tags.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancecreate_tags-method)
        """

    async def describe_attribute(
        self, **kwargs: Unpack[DescribeInstanceAttributeRequestInstanceDescribeAttributeTypeDef]
    ) -> InstanceAttributeTypeDef:
        """
        Describes the specified attribute of the specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/describe_attribute.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancedescribe_attribute-method)
        """

    async def detach_classic_link_vpc(
        self, **kwargs: Unpack[DetachClassicLinkVpcRequestInstanceDetachClassicLinkVpcTypeDef]
    ) -> DetachClassicLinkVpcResultTypeDef:
        """
        This action is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/detach_classic_link_vpc.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancedetach_classic_link_vpc-method)
        """

    async def detach_volume(
        self, **kwargs: Unpack[DetachVolumeRequestInstanceDetachVolumeTypeDef]
    ) -> VolumeAttachmentResponseTypeDef:
        """
        Detaches an EBS volume from an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/detach_volume.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancedetach_volume-method)
        """

    async def modify_attribute(
        self, **kwargs: Unpack[ModifyInstanceAttributeRequestInstanceModifyAttributeTypeDef]
    ) -> None:
        """
        Modifies the specified attribute of the specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/modify_attribute.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancemodify_attribute-method)
        """

    async def monitor(
        self, **kwargs: Unpack[MonitorInstancesRequestInstanceMonitorTypeDef]
    ) -> MonitorInstancesResultTypeDef:
        """
        Enables detailed monitoring for a running instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/monitor.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancemonitor-method)
        """

    async def password_data(
        self, **kwargs: Unpack[GetPasswordDataRequestInstancePasswordDataTypeDef]
    ) -> GetPasswordDataResultTypeDef:
        """
        Retrieves the encrypted administrator password for a running Windows instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/password_data.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancepassword_data-method)
        """

    async def reboot(self, **kwargs: Unpack[RebootInstancesRequestInstanceRebootTypeDef]) -> None:
        """
        Requests a reboot of the specified instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/reboot.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancereboot-method)
        """

    async def report_status(
        self, **kwargs: Unpack[ReportInstanceStatusRequestInstanceReportStatusTypeDef]
    ) -> None:
        """
        Submits feedback about the status of an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/report_status.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancereport_status-method)
        """

    async def reset_attribute(
        self, **kwargs: Unpack[ResetInstanceAttributeRequestInstanceResetAttributeTypeDef]
    ) -> None:
        """
        Resets an attribute of an instance to its default value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/reset_attribute.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancereset_attribute-method)
        """

    async def reset_kernel(
        self, **kwargs: Unpack[ResetInstanceAttributeRequestInstanceResetKernelTypeDef]
    ) -> None:
        """
        Resets an attribute of an instance to its default value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/reset_kernel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancereset_kernel-method)
        """

    async def reset_ramdisk(
        self, **kwargs: Unpack[ResetInstanceAttributeRequestInstanceResetRamdiskTypeDef]
    ) -> None:
        """
        Resets an attribute of an instance to its default value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/reset_ramdisk.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancereset_ramdisk-method)
        """

    async def reset_source_dest_check(
        self, **kwargs: Unpack[ResetInstanceAttributeRequestInstanceResetSourceDestCheckTypeDef]
    ) -> None:
        """
        Resets an attribute of an instance to its default value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/reset_source_dest_check.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancereset_source_dest_check-method)
        """

    async def start(
        self, **kwargs: Unpack[StartInstancesRequestInstanceStartTypeDef]
    ) -> StartInstancesResultTypeDef:
        """
        Starts an Amazon EBS-backed instance that you've previously stopped.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/start.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancestart-method)
        """

    async def stop(
        self, **kwargs: Unpack[StopInstancesRequestInstanceStopTypeDef]
    ) -> StopInstancesResultTypeDef:
        """
        Stops an Amazon EBS-backed instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/stop.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancestop-method)
        """

    async def terminate(
        self, **kwargs: Unpack[TerminateInstancesRequestInstanceTerminateTypeDef]
    ) -> TerminateInstancesResultTypeDef:
        """
        Shuts down the specified instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/terminate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instanceterminate-method)
        """

    async def unmonitor(
        self, **kwargs: Unpack[UnmonitorInstancesRequestInstanceUnmonitorTypeDef]
    ) -> UnmonitorInstancesResultTypeDef:
        """
        Disables detailed monitoring for a running instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/unmonitor.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instanceunmonitor-method)
        """

    async def wait_until_exists(self) -> None:
        """
        Waits until Instance is exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/wait_until_exists.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancewait_until_exists-method)
        """

    async def wait_until_running(self) -> None:
        """
        Waits until Instance is running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/wait_until_running.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancewait_until_running-method)
        """

    async def wait_until_stopped(self) -> None:
        """
        Waits until Instance is stopped.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/wait_until_stopped.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancewait_until_stopped-method)
        """

    async def wait_until_terminated(self) -> None:
        """
        Waits until Instance is terminated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/wait_until_terminated.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancewait_until_terminated-method)
        """

    async def delete_tags(self, **kwargs: Unpack[InstanceDeleteTagsRequestTypeDef]) -> None:
        """
        Deletes the specified set of tags from the specified set of resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/delete_tags.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancedelete_tags-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instanceload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancereload-method)
        """


_Instance = Instance


class InternetGateway(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/internetgateway/index.html#EC2.InternetGateway)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgateway)
    """

    id: str
    attachments: Awaitable[List[InternetGatewayAttachmentTypeDef]]
    internet_gateway_id: Awaitable[str]
    owner_id: Awaitable[str]
    tags: Awaitable[List[TagTypeDef]]
    meta: EC2ResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this InternetGateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/internetgateway/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewayget_available_subresources-method)
        """

    async def attach_to_vpc(
        self, **kwargs: Unpack[AttachInternetGatewayRequestInternetGatewayAttachToVpcTypeDef]
    ) -> None:
        """
        Attaches an internet gateway or a virtual private gateway to a VPC, enabling
        connectivity between the internet and the VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/internetgateway/attach_to_vpc.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewayattach_to_vpc-method)
        """

    async def create_tags(self, **kwargs: Unpack[InternetGatewayCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/internetgateway/create_tags.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewaycreate_tags-method)
        """

    async def delete(
        self, **kwargs: Unpack[DeleteInternetGatewayRequestInternetGatewayDeleteTypeDef]
    ) -> None:
        """
        Deletes the specified internet gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/internetgateway/delete.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewaydelete-method)
        """

    async def detach_from_vpc(
        self, **kwargs: Unpack[DetachInternetGatewayRequestInternetGatewayDetachFromVpcTypeDef]
    ) -> None:
        """
        Detaches an internet gateway from a VPC, disabling connectivity between the
        internet and the VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/internetgateway/detach_from_vpc.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewaydetach_from_vpc-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/internetgateway/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewayload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/internetgateway/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewayreload-method)
        """


_InternetGateway = InternetGateway


class KeyPair(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/keypair/index.html#EC2.KeyPair)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#keypair)
    """

    name: str
    key_pair_id: Awaitable[str]
    tags: Awaitable[List[TagTypeDef]]
    key_name: Awaitable[str]
    key_fingerprint: Awaitable[str]
    key_material: Awaitable[str]
    meta: EC2ResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this KeyPair.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/keypair/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#keypairget_available_subresources-method)
        """

    async def delete(
        self, **kwargs: Unpack[DeleteKeyPairRequestKeyPairDeleteTypeDef]
    ) -> DeleteKeyPairResultTypeDef:
        """
        Deletes the specified key pair, by removing the public key from Amazon EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/keypair/delete.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#keypairdelete-method)
        """


_KeyPair = KeyPair


class KeyPairInfo(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/keypairinfo/index.html#EC2.KeyPairInfo)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#keypairinfo)
    """

    name: str
    key_pair_id: Awaitable[str]
    key_type: Awaitable[KeyTypeType]
    tags: Awaitable[List[TagTypeDef]]
    public_key: Awaitable[str]
    create_time: Awaitable[datetime]
    key_name: Awaitable[str]
    key_fingerprint: Awaitable[str]
    meta: EC2ResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this KeyPairInfo.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/keypairinfo/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#keypairinfoget_available_subresources-method)
        """

    async def delete(
        self, **kwargs: Unpack[DeleteKeyPairRequestKeyPairInfoDeleteTypeDef]
    ) -> DeleteKeyPairResultTypeDef:
        """
        Deletes the specified key pair, by removing the public key from Amazon EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/keypairinfo/delete.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#keypairinfodelete-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/keypairinfo/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#keypairinfoload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/keypairinfo/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#keypairinforeload-method)
        """


_KeyPairInfo = KeyPairInfo


class NetworkAcl(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkacl/index.html#EC2.NetworkAcl)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkacl)
    """

    id: str
    vpc: Vpc
    associations: Awaitable[List[NetworkAclAssociationTypeDef]]
    entries: Awaitable[List[NetworkAclEntryTypeDef]]
    is_default: Awaitable[bool]
    network_acl_id: Awaitable[str]
    tags: Awaitable[List[TagTypeDef]]
    vpc_id: Awaitable[str]
    owner_id: Awaitable[str]
    meta: EC2ResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this NetworkAcl.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkacl/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclget_available_subresources-method)
        """

    async def create_entry(
        self, **kwargs: Unpack[CreateNetworkAclEntryRequestNetworkAclCreateEntryTypeDef]
    ) -> None:
        """
        Creates an entry (a rule) in a network ACL with the specified rule number.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkacl/create_entry.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclcreate_entry-method)
        """

    async def create_tags(self, **kwargs: Unpack[NetworkAclCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkacl/create_tags.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclcreate_tags-method)
        """

    async def delete(
        self, **kwargs: Unpack[DeleteNetworkAclRequestNetworkAclDeleteTypeDef]
    ) -> None:
        """
        Deletes the specified network ACL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkacl/delete.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkacldelete-method)
        """

    async def delete_entry(
        self, **kwargs: Unpack[DeleteNetworkAclEntryRequestNetworkAclDeleteEntryTypeDef]
    ) -> None:
        """
        Deletes the specified ingress or egress entry (rule) from the specified network
        ACL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkacl/delete_entry.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkacldelete_entry-method)
        """

    async def replace_association(
        self,
        **kwargs: Unpack[ReplaceNetworkAclAssociationRequestNetworkAclReplaceAssociationTypeDef],
    ) -> ReplaceNetworkAclAssociationResultTypeDef:
        """
        Changes which network ACL a subnet is associated with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkacl/replace_association.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclreplace_association-method)
        """

    async def replace_entry(
        self, **kwargs: Unpack[ReplaceNetworkAclEntryRequestNetworkAclReplaceEntryTypeDef]
    ) -> None:
        """
        Replaces an entry (rule) in a network ACL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkacl/replace_entry.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclreplace_entry-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkacl/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkacl/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclreload-method)
        """


_NetworkAcl = NetworkAcl


class NetworkInterface(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkinterface/index.html#EC2.NetworkInterface)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterface)
    """

    id: str
    association: NetworkInterfaceAssociation
    subnet: Subnet
    vpc: Vpc
    association_attribute: Awaitable[NetworkInterfaceAssociationTypeDef]
    attachment: Awaitable[NetworkInterfaceAttachmentTypeDef]
    availability_zone: Awaitable[str]
    connection_tracking_configuration: Awaitable[ConnectionTrackingConfigurationTypeDef]
    description: Awaitable[str]
    groups: Awaitable[List[GroupIdentifierTypeDef]]
    interface_type: Awaitable[NetworkInterfaceTypeType]
    ipv6_addresses: Awaitable[List[NetworkInterfaceIpv6AddressTypeDef]]
    mac_address: Awaitable[str]
    network_interface_id: Awaitable[str]
    outpost_arn: Awaitable[str]
    owner_id: Awaitable[str]
    private_dns_name: Awaitable[str]
    public_dns_name: Awaitable[str]
    public_ip_dns_name_options: Awaitable[PublicIpDnsNameOptionsTypeDef]
    private_ip_address: Awaitable[str]
    private_ip_addresses: Awaitable[List[NetworkInterfacePrivateIpAddressTypeDef]]
    ipv4_prefixes: Awaitable[List[Ipv4PrefixSpecificationTypeDef]]
    ipv6_prefixes: Awaitable[List[Ipv6PrefixSpecificationTypeDef]]
    requester_id: Awaitable[str]
    requester_managed: Awaitable[bool]
    source_dest_check: Awaitable[bool]
    status: Awaitable[NetworkInterfaceStatusType]
    subnet_id: Awaitable[str]
    tag_set: Awaitable[List[TagTypeDef]]
    vpc_id: Awaitable[str]
    deny_all_igw_traffic: Awaitable[bool]
    ipv6_native: Awaitable[bool]
    ipv6_address: Awaitable[str]
    operator: Awaitable[OperatorResponseTypeDef]
    associated_subnets: Awaitable[List[str]]
    meta: EC2ResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this NetworkInterface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkinterface/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfaceget_available_subresources-method)
        """

    async def assign_private_ip_addresses(
        self,
        **kwargs: Unpack[
            AssignPrivateIpAddressesRequestNetworkInterfaceAssignPrivateIpAddressesTypeDef
        ],
    ) -> AssignPrivateIpAddressesResultTypeDef:
        """
        Assigns the specified secondary private IP addresses to the specified network
        interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkinterface/assign_private_ip_addresses.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfaceassign_private_ip_addresses-method)
        """

    async def attach(
        self, **kwargs: Unpack[AttachNetworkInterfaceRequestNetworkInterfaceAttachTypeDef]
    ) -> AttachNetworkInterfaceResultTypeDef:
        """
        Attaches a network interface to an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkinterface/attach.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfaceattach-method)
        """

    async def create_tags(self, **kwargs: Unpack[NetworkInterfaceCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkinterface/create_tags.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacecreate_tags-method)
        """

    async def delete(
        self, **kwargs: Unpack[DeleteNetworkInterfaceRequestNetworkInterfaceDeleteTypeDef]
    ) -> None:
        """
        Deletes the specified network interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkinterface/delete.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacedelete-method)
        """

    async def describe_attribute(
        self,
        **kwargs: Unpack[
            DescribeNetworkInterfaceAttributeRequestNetworkInterfaceDescribeAttributeTypeDef
        ],
    ) -> DescribeNetworkInterfaceAttributeResultTypeDef:
        """
        Describes a network interface attribute.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkinterface/describe_attribute.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacedescribe_attribute-method)
        """

    async def detach(
        self, **kwargs: Unpack[DetachNetworkInterfaceRequestNetworkInterfaceDetachTypeDef]
    ) -> None:
        """
        Detaches a network interface from an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkinterface/detach.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacedetach-method)
        """

    async def modify_attribute(
        self,
        **kwargs: Unpack[
            ModifyNetworkInterfaceAttributeRequestNetworkInterfaceModifyAttributeTypeDef
        ],
    ) -> None:
        """
        Modifies the specified network interface attribute.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkinterface/modify_attribute.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacemodify_attribute-method)
        """

    async def reset_attribute(
        self,
        **kwargs: Unpack[
            ResetNetworkInterfaceAttributeRequestNetworkInterfaceResetAttributeTypeDef
        ],
    ) -> None:
        """
        Resets a network interface attribute.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkinterface/reset_attribute.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacereset_attribute-method)
        """

    async def unassign_private_ip_addresses(
        self,
        **kwargs: Unpack[
            UnassignPrivateIpAddressesRequestNetworkInterfaceUnassignPrivateIpAddressesTypeDef
        ],
    ) -> None:
        """
        Unassigns the specified secondary private IP addresses or IPv4 Prefix
        Delegation prefixes from a network interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkinterface/unassign_private_ip_addresses.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfaceunassign_private_ip_addresses-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkinterface/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfaceload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkinterface/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacereload-method)
        """


_NetworkInterface = NetworkInterface


class NetworkInterfaceAssociation(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkinterfaceassociation/index.html#EC2.NetworkInterfaceAssociation)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfaceassociation)
    """

    id: str
    address: VpcAddress
    carrier_ip: Awaitable[str]
    customer_owned_ip: Awaitable[str]
    ip_owner_id: Awaitable[str]
    public_dns_name: Awaitable[str]
    public_ip: Awaitable[str]
    meta: EC2ResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this
        NetworkInterfaceAssociation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkinterfaceassociation/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfaceassociationget_available_subresources-method)
        """

    async def delete(
        self, **kwargs: Unpack[DisassociateAddressRequestNetworkInterfaceAssociationDeleteTypeDef]
    ) -> None:
        """
        Disassociates an Elastic IP address from the instance or network interface it's
        associated with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkinterfaceassociation/delete.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfaceassociationdelete-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkinterfaceassociation/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfaceassociationload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/networkinterfaceassociation/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfaceassociationreload-method)
        """


_NetworkInterfaceAssociation = NetworkInterfaceAssociation


class PlacementGroup(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/placementgroup/index.html#EC2.PlacementGroup)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroup)
    """

    name: str
    instances: PlacementGroupInstancesCollection
    group_name: Awaitable[str]
    state: Awaitable[PlacementGroupStateType]
    strategy: Awaitable[PlacementStrategyType]
    partition_count: Awaitable[int]
    group_id: Awaitable[str]
    tags: Awaitable[List[TagTypeDef]]
    group_arn: Awaitable[str]
    spread_level: Awaitable[SpreadLevelType]
    meta: EC2ResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this PlacementGroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/placementgroup/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroupget_available_subresources-method)
        """

    async def delete(
        self, **kwargs: Unpack[DeletePlacementGroupRequestPlacementGroupDeleteTypeDef]
    ) -> None:
        """
        Deletes the specified placement group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/placementgroup/delete.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroupdelete-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/placementgroup/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroupload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/placementgroup/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroupreload-method)
        """


_PlacementGroup = PlacementGroup


class Route(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/route/index.html#EC2.Route)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#route)
    """

    route_table_id: str
    destination_cidr_block: str
    destination_ipv6_cidr_block: Awaitable[str]
    destination_prefix_list_id: Awaitable[str]
    egress_only_internet_gateway_id: Awaitable[str]
    gateway_id: Awaitable[str]
    instance_id: Awaitable[str]
    instance_owner_id: Awaitable[str]
    nat_gateway_id: Awaitable[str]
    transit_gateway_id: Awaitable[str]
    local_gateway_id: Awaitable[str]
    carrier_gateway_id: Awaitable[str]
    network_interface_id: Awaitable[str]
    origin: Awaitable[RouteOriginType]
    state: Awaitable[RouteStateType]
    vpc_peering_connection_id: Awaitable[str]
    core_network_arn: Awaitable[str]
    odb_network_arn: Awaitable[str]
    meta: EC2ResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/route/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routeget_available_subresources-method)
        """

    async def delete(self, **kwargs: Unpack[DeleteRouteRequestRouteDeleteTypeDef]) -> None:
        """
        Deletes the specified route from the specified route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/route/delete.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routedelete-method)
        """

    async def replace(self, **kwargs: Unpack[ReplaceRouteRequestRouteReplaceTypeDef]) -> None:
        """
        Replaces an existing route within a route table in a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/route/replace.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routereplace-method)
        """

    async def RouteTable(self) -> _RouteTable:
        """
        Creates a RouteTable resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/route/RouteTable.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routeroutetable-method)
        """


_Route = Route


class RouteTable(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/routetable/index.html#EC2.RouteTable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetable)
    """

    id: str
    associations: List[RouteTableAssociation]
    routes: List[Route]
    vpc: Vpc
    associations_attribute: Awaitable[List[RouteTableAssociationTypeDef]]
    propagating_vgws: Awaitable[List[PropagatingVgwTypeDef]]
    route_table_id: Awaitable[str]
    routes_attribute: Awaitable[List[RouteTypeDef]]
    tags: Awaitable[List[TagTypeDef]]
    vpc_id: Awaitable[str]
    owner_id: Awaitable[str]
    meta: EC2ResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this RouteTable.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/routetable/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetableget_available_subresources-method)
        """

    async def associate_with_subnet(
        self, **kwargs: Unpack[AssociateRouteTableRequestRouteTableAssociateWithSubnetTypeDef]
    ) -> _RouteTableAssociation:
        """
        Associates a subnet in your VPC or an internet gateway or virtual private
        gateway attached to your VPC with a route table in your VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/routetable/associate_with_subnet.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetableassociate_with_subnet-method)
        """

    async def create_route(
        self, **kwargs: Unpack[CreateRouteRequestRouteTableCreateRouteTypeDef]
    ) -> _Route:
        """
        Creates a route in a route table within a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/routetable/create_route.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetablecreate_route-method)
        """

    async def create_tags(self, **kwargs: Unpack[RouteTableCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/routetable/create_tags.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetablecreate_tags-method)
        """

    async def delete(
        self, **kwargs: Unpack[DeleteRouteTableRequestRouteTableDeleteTypeDef]
    ) -> None:
        """
        Deletes the specified route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/routetable/delete.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetabledelete-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/routetable/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetableload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/routetable/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetablereload-method)
        """


_RouteTable = RouteTable


class RouteTableAssociation(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/routetableassociation/index.html#EC2.RouteTableAssociation)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetableassociation)
    """

    id: str
    route_table: RouteTable
    subnet: Subnet
    main: Awaitable[bool]
    route_table_association_id: Awaitable[str]
    route_table_id: Awaitable[str]
    subnet_id: Awaitable[str]
    gateway_id: Awaitable[str]
    association_state: Awaitable[RouteTableAssociationStateTypeDef]
    meta: EC2ResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this
        RouteTableAssociation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/routetableassociation/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetableassociationget_available_subresources-method)
        """

    async def delete(
        self, **kwargs: Unpack[DisassociateRouteTableRequestRouteTableAssociationDeleteTypeDef]
    ) -> None:
        """
        Disassociates a subnet or gateway from a route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/routetableassociation/delete.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetableassociationdelete-method)
        """

    async def replace_subnet(
        self,
        **kwargs: Unpack[
            ReplaceRouteTableAssociationRequestRouteTableAssociationReplaceSubnetTypeDef
        ],
    ) -> _RouteTableAssociation:
        """
        Changes the route table associated with a given subnet, internet gateway, or
        virtual private gateway in a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/routetableassociation/replace_subnet.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetableassociationreplace_subnet-method)
        """


_RouteTableAssociation = RouteTableAssociation


class SecurityGroup(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/securitygroup/index.html#EC2.SecurityGroup)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroup)
    """

    id: str
    group_id: Awaitable[str]
    ip_permissions_egress: Awaitable[List[IpPermissionOutputTypeDef]]
    tags: Awaitable[List[TagTypeDef]]
    vpc_id: Awaitable[str]
    security_group_arn: Awaitable[str]
    owner_id: Awaitable[str]
    group_name: Awaitable[str]
    description: Awaitable[str]
    ip_permissions: Awaitable[List[IpPermissionOutputTypeDef]]
    meta: EC2ResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this SecurityGroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/securitygroup/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupget_available_subresources-method)
        """

    async def authorize_egress(
        self,
        **kwargs: Unpack[AuthorizeSecurityGroupEgressRequestSecurityGroupAuthorizeEgressTypeDef],
    ) -> AuthorizeSecurityGroupEgressResultTypeDef:
        """
        Adds the specified outbound (egress) rules to a security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/securitygroup/authorize_egress.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupauthorize_egress-method)
        """

    async def authorize_ingress(
        self,
        **kwargs: Unpack[AuthorizeSecurityGroupIngressRequestSecurityGroupAuthorizeIngressTypeDef],
    ) -> AuthorizeSecurityGroupIngressResultTypeDef:
        """
        Adds the specified inbound (ingress) rules to a security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/securitygroup/authorize_ingress.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupauthorize_ingress-method)
        """

    async def create_tags(self, **kwargs: Unpack[SecurityGroupCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/securitygroup/create_tags.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupcreate_tags-method)
        """

    async def delete(
        self, **kwargs: Unpack[DeleteSecurityGroupRequestSecurityGroupDeleteTypeDef]
    ) -> DeleteSecurityGroupResultTypeDef:
        """
        Deletes a security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/securitygroup/delete.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupdelete-method)
        """

    async def revoke_egress(
        self, **kwargs: Unpack[RevokeSecurityGroupEgressRequestSecurityGroupRevokeEgressTypeDef]
    ) -> RevokeSecurityGroupEgressResultTypeDef:
        """
        Removes the specified outbound (egress) rules from the specified security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/securitygroup/revoke_egress.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygrouprevoke_egress-method)
        """

    async def revoke_ingress(
        self, **kwargs: Unpack[RevokeSecurityGroupIngressRequestSecurityGroupRevokeIngressTypeDef]
    ) -> RevokeSecurityGroupIngressResultTypeDef:
        """
        Removes the specified inbound (ingress) rules from a security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/securitygroup/revoke_ingress.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygrouprevoke_ingress-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/securitygroup/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/securitygroup/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupreload-method)
        """


_SecurityGroup = SecurityGroup


class Snapshot(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/snapshot/index.html#EC2.Snapshot)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshot)
    """

    id: str
    volume: Volume
    owner_alias: Awaitable[str]
    outpost_arn: Awaitable[str]
    tags: Awaitable[List[TagTypeDef]]
    storage_tier: Awaitable[StorageTierType]
    restore_expiry_time: Awaitable[datetime]
    sse_type: Awaitable[SSETypeType]
    availability_zone: Awaitable[str]
    transfer_type: Awaitable[TransferTypeType]
    completion_duration_minutes: Awaitable[int]
    completion_time: Awaitable[datetime]
    full_snapshot_size_in_bytes: Awaitable[int]
    snapshot_id: Awaitable[str]
    volume_id: Awaitable[str]
    state: Awaitable[SnapshotStateType]
    state_message: Awaitable[str]
    start_time: Awaitable[datetime]
    progress: Awaitable[str]
    owner_id: Awaitable[str]
    description: Awaitable[str]
    volume_size: Awaitable[int]
    encrypted: Awaitable[bool]
    kms_key_id: Awaitable[str]
    data_encryption_key_id: Awaitable[str]
    meta: EC2ResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/snapshot/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotget_available_subresources-method)
        """

    async def copy(
        self, **kwargs: Unpack[CopySnapshotRequestSnapshotCopyTypeDef]
    ) -> CopySnapshotResultTypeDef:
        """
        Copies a point-in-time snapshot of an EBS volume and stores it in Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/snapshot/copy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotcopy-method)
        """

    async def create_tags(self, **kwargs: Unpack[SnapshotCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/snapshot/create_tags.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotcreate_tags-method)
        """

    async def delete(self, **kwargs: Unpack[DeleteSnapshotRequestSnapshotDeleteTypeDef]) -> None:
        """
        Deletes the specified snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/snapshot/delete.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotdelete-method)
        """

    async def describe_attribute(
        self, **kwargs: Unpack[DescribeSnapshotAttributeRequestSnapshotDescribeAttributeTypeDef]
    ) -> DescribeSnapshotAttributeResultTypeDef:
        """
        Describes the specified attribute of the specified snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/snapshot/describe_attribute.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotdescribe_attribute-method)
        """

    async def modify_attribute(
        self, **kwargs: Unpack[ModifySnapshotAttributeRequestSnapshotModifyAttributeTypeDef]
    ) -> None:
        """
        Adds or removes permission settings for the specified snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/snapshot/modify_attribute.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotmodify_attribute-method)
        """

    async def reset_attribute(
        self, **kwargs: Unpack[ResetSnapshotAttributeRequestSnapshotResetAttributeTypeDef]
    ) -> None:
        """
        Resets permission settings for the specified snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/snapshot/reset_attribute.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotreset_attribute-method)
        """

    async def wait_until_completed(self) -> None:
        """
        Waits until Snapshot is completed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/snapshot/wait_until_completed.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotwait_until_completed-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/snapshot/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/snapshot/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotreload-method)
        """


_Snapshot = Snapshot


class Subnet(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/index.html#EC2.Subnet)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnet)
    """

    id: str
    vpc: Vpc
    instances: SubnetInstancesCollection
    network_interfaces: SubnetNetworkInterfacesCollection
    availability_zone_id: Awaitable[str]
    enable_lni_at_device_index: Awaitable[int]
    map_customer_owned_ip_on_launch: Awaitable[bool]
    customer_owned_ipv4_pool: Awaitable[str]
    owner_id: Awaitable[str]
    assign_ipv6_address_on_creation: Awaitable[bool]
    ipv6_cidr_block_association_set: Awaitable[List[SubnetIpv6CidrBlockAssociationTypeDef]]
    tags: Awaitable[List[TagTypeDef]]
    subnet_arn: Awaitable[str]
    outpost_arn: Awaitable[str]
    enable_dns64: Awaitable[bool]
    ipv6_native: Awaitable[bool]
    private_dns_name_options_on_launch: Awaitable[PrivateDnsNameOptionsOnLaunchTypeDef]
    block_public_access_states: Awaitable[BlockPublicAccessStatesTypeDef]
    type: Awaitable[str]
    subnet_id: Awaitable[str]
    state: Awaitable[SubnetStateType]
    vpc_id: Awaitable[str]
    cidr_block: Awaitable[str]
    available_ip_address_count: Awaitable[int]
    availability_zone: Awaitable[str]
    default_for_az: Awaitable[bool]
    map_public_ip_on_launch: Awaitable[bool]
    meta: EC2ResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Subnet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetget_available_subresources-method)
        """

    async def create_instances(
        self, **kwargs: Unpack[RunInstancesRequestSubnetCreateInstancesTypeDef]
    ) -> List[_Instance]:
        """
        Launches the specified number of instances using an AMI for which you have
        permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/create_instances.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetcreate_instances-method)
        """

    async def create_network_interface(
        self, **kwargs: Unpack[CreateNetworkInterfaceRequestSubnetCreateNetworkInterfaceTypeDef]
    ) -> _NetworkInterface:
        """
        Creates a network interface in the specified subnet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/create_network_interface.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetcreate_network_interface-method)
        """

    async def create_tags(self, **kwargs: Unpack[SubnetCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/create_tags.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetcreate_tags-method)
        """

    async def delete(self, **kwargs: Unpack[DeleteSubnetRequestSubnetDeleteTypeDef]) -> None:
        """
        Deletes the specified subnet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/delete.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetdelete-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/subnet/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetreload-method)
        """


_Subnet = Subnet


class Tag(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/tag/index.html#EC2.Tag)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#tag)
    """

    resource_id: str
    key: str
    value: str
    resource_type: Awaitable[ResourceTypeType]
    meta: EC2ResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/tag/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#tagget_available_subresources-method)
        """

    async def delete(self, **kwargs: Unpack[DeleteTagsRequestTagDeleteTypeDef]) -> None:
        """
        Deletes the specified set of tags from the specified set of resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/tag/delete.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#tagdelete-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/tag/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#tagload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/tag/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#tagreload-method)
        """


_Tag = Tag


class Volume(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/volume/index.html#EC2.Volume)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volume)
    """

    id: str
    snapshots: VolumeSnapshotsCollection
    outpost_arn: Awaitable[str]
    iops: Awaitable[int]
    tags: Awaitable[List[TagTypeDef]]
    volume_type: Awaitable[VolumeTypeType]
    fast_restored: Awaitable[bool]
    multi_attach_enabled: Awaitable[bool]
    throughput: Awaitable[int]
    sse_type: Awaitable[SSETypeType]
    operator: Awaitable[OperatorResponseTypeDef]
    volume_initialization_rate: Awaitable[int]
    volume_id: Awaitable[str]
    size: Awaitable[int]
    snapshot_id: Awaitable[str]
    availability_zone: Awaitable[str]
    state: Awaitable[VolumeStateType]
    create_time: Awaitable[datetime]
    attachments: Awaitable[List[VolumeAttachmentTypeDef]]
    encrypted: Awaitable[bool]
    kms_key_id: Awaitable[str]
    meta: EC2ResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/volume/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumeget_available_subresources-method)
        """

    async def attach_to_instance(
        self, **kwargs: Unpack[AttachVolumeRequestVolumeAttachToInstanceTypeDef]
    ) -> VolumeAttachmentResponseTypeDef:
        """
        Attaches an Amazon EBS volume to a <code>running</code> or <code>stopped</code>
        instance, and exposes it to the instance with the specified device name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/volume/attach_to_instance.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumeattach_to_instance-method)
        """

    async def create_snapshot(
        self, **kwargs: Unpack[CreateSnapshotRequestVolumeCreateSnapshotTypeDef]
    ) -> _Snapshot:
        """
        Creates a snapshot of an EBS volume and stores it in Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/volume/create_snapshot.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumecreate_snapshot-method)
        """

    async def create_tags(self, **kwargs: Unpack[VolumeCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/volume/create_tags.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumecreate_tags-method)
        """

    async def delete(self, **kwargs: Unpack[DeleteVolumeRequestVolumeDeleteTypeDef]) -> None:
        """
        Deletes the specified EBS volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/volume/delete.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumedelete-method)
        """

    async def describe_attribute(
        self, **kwargs: Unpack[DescribeVolumeAttributeRequestVolumeDescribeAttributeTypeDef]
    ) -> DescribeVolumeAttributeResultTypeDef:
        """
        Describes the specified attribute of the specified volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/volume/describe_attribute.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumedescribe_attribute-method)
        """

    async def describe_status(
        self, **kwargs: Unpack[DescribeVolumeStatusRequestVolumeDescribeStatusTypeDef]
    ) -> DescribeVolumeStatusResultTypeDef:
        """
        Describes the status of the specified volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/volume/describe_status.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumedescribe_status-method)
        """

    async def detach_from_instance(
        self, **kwargs: Unpack[DetachVolumeRequestVolumeDetachFromInstanceTypeDef]
    ) -> VolumeAttachmentResponseTypeDef:
        """
        Detaches an EBS volume from an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/volume/detach_from_instance.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumedetach_from_instance-method)
        """

    async def enable_io(self, **kwargs: Unpack[EnableVolumeIORequestVolumeEnableIoTypeDef]) -> None:
        """
        Enables I/O operations for a volume that had I/O operations disabled because
        the data on the volume was potentially inconsistent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/volume/enable_io.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumeenable_io-method)
        """

    async def modify_attribute(
        self, **kwargs: Unpack[ModifyVolumeAttributeRequestVolumeModifyAttributeTypeDef]
    ) -> None:
        """
        Modifies a volume attribute.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/volume/modify_attribute.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumemodify_attribute-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/volume/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumeload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/volume/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumereload-method)
        """


_Volume = Volume


class Vpc(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/index.html#EC2.Vpc)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpc)
    """

    id: str
    dhcp_options: DhcpOptions
    accepted_vpc_peering_connections: VpcAcceptedVpcPeeringConnectionsCollection
    instances: VpcInstancesCollection
    internet_gateways: VpcInternetGatewaysCollection
    network_acls: VpcNetworkAclsCollection
    network_interfaces: VpcNetworkInterfacesCollection
    requested_vpc_peering_connections: VpcRequestedVpcPeeringConnectionsCollection
    route_tables: VpcRouteTablesCollection
    security_groups: VpcSecurityGroupsCollection
    subnets: VpcSubnetsCollection
    owner_id: Awaitable[str]
    instance_tenancy: Awaitable[TenancyType]
    ipv6_cidr_block_association_set: Awaitable[List[VpcIpv6CidrBlockAssociationTypeDef]]
    cidr_block_association_set: Awaitable[List[VpcCidrBlockAssociationTypeDef]]
    is_default: Awaitable[bool]
    encryption_control: Awaitable[VpcEncryptionControlTypeDef]
    tags: Awaitable[List[TagTypeDef]]
    block_public_access_states: Awaitable[BlockPublicAccessStatesTypeDef]
    vpc_id: Awaitable[str]
    state: Awaitable[VpcStateType]
    cidr_block: Awaitable[str]
    dhcp_options_id: Awaitable[str]
    meta: EC2ResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Vpc.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcget_available_subresources-method)
        """

    async def associate_dhcp_options(
        self, **kwargs: Unpack[AssociateDhcpOptionsRequestVpcAssociateDhcpOptionsTypeDef]
    ) -> None:
        """
        Associates a set of DHCP options (that you've previously created) with the
        specified VPC, or associates no DHCP options with the VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/associate_dhcp_options.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcassociate_dhcp_options-method)
        """

    async def attach_classic_link_instance(
        self, **kwargs: Unpack[AttachClassicLinkVpcRequestVpcAttachClassicLinkInstanceTypeDef]
    ) -> AttachClassicLinkVpcResultTypeDef:
        """
        This action is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/attach_classic_link_instance.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcattach_classic_link_instance-method)
        """

    async def attach_internet_gateway(
        self, **kwargs: Unpack[AttachInternetGatewayRequestVpcAttachInternetGatewayTypeDef]
    ) -> None:
        """
        Attaches an internet gateway or a virtual private gateway to a VPC, enabling
        connectivity between the internet and the VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/attach_internet_gateway.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcattach_internet_gateway-method)
        """

    async def create_network_acl(
        self, **kwargs: Unpack[CreateNetworkAclRequestVpcCreateNetworkAclTypeDef]
    ) -> _NetworkAcl:
        """
        Creates a network ACL in a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/create_network_acl.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpccreate_network_acl-method)
        """

    async def create_route_table(
        self, **kwargs: Unpack[CreateRouteTableRequestVpcCreateRouteTableTypeDef]
    ) -> _RouteTable:
        """
        Creates a route table for the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/create_route_table.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpccreate_route_table-method)
        """

    async def create_security_group(
        self, **kwargs: Unpack[CreateSecurityGroupRequestVpcCreateSecurityGroupTypeDef]
    ) -> _SecurityGroup:
        """
        Creates a security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/create_security_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpccreate_security_group-method)
        """

    async def create_subnet(
        self, **kwargs: Unpack[CreateSubnetRequestVpcCreateSubnetTypeDef]
    ) -> _Subnet:
        """
        Creates a subnet in the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/create_subnet.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpccreate_subnet-method)
        """

    async def create_tags(self, **kwargs: Unpack[VpcCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/create_tags.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpccreate_tags-method)
        """

    async def delete(self, **kwargs: Unpack[DeleteVpcRequestVpcDeleteTypeDef]) -> None:
        """
        Deletes the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/delete.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcdelete-method)
        """

    async def describe_attribute(
        self, **kwargs: Unpack[DescribeVpcAttributeRequestVpcDescribeAttributeTypeDef]
    ) -> DescribeVpcAttributeResultTypeDef:
        """
        Describes the specified attribute of the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/describe_attribute.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcdescribe_attribute-method)
        """

    async def detach_classic_link_instance(
        self, **kwargs: Unpack[DetachClassicLinkVpcRequestVpcDetachClassicLinkInstanceTypeDef]
    ) -> DetachClassicLinkVpcResultTypeDef:
        """
        This action is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/detach_classic_link_instance.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcdetach_classic_link_instance-method)
        """

    async def detach_internet_gateway(
        self, **kwargs: Unpack[DetachInternetGatewayRequestVpcDetachInternetGatewayTypeDef]
    ) -> None:
        """
        Detaches an internet gateway from a VPC, disabling connectivity between the
        internet and the VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/detach_internet_gateway.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcdetach_internet_gateway-method)
        """

    async def disable_classic_link(
        self, **kwargs: Unpack[DisableVpcClassicLinkRequestVpcDisableClassicLinkTypeDef]
    ) -> DisableVpcClassicLinkResultTypeDef:
        """
        This action is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/disable_classic_link.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcdisable_classic_link-method)
        """

    async def enable_classic_link(
        self, **kwargs: Unpack[EnableVpcClassicLinkRequestVpcEnableClassicLinkTypeDef]
    ) -> EnableVpcClassicLinkResultTypeDef:
        """
        This action is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/enable_classic_link.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcenable_classic_link-method)
        """

    async def modify_attribute(
        self, **kwargs: Unpack[ModifyVpcAttributeRequestVpcModifyAttributeTypeDef]
    ) -> None:
        """
        Modifies the specified attribute of the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/modify_attribute.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcmodify_attribute-method)
        """

    async def request_vpc_peering_connection(
        self,
        **kwargs: Unpack[CreateVpcPeeringConnectionRequestVpcRequestVpcPeeringConnectionTypeDef],
    ) -> _VpcPeeringConnection:
        """
        Requests a VPC peering connection between two VPCs: a requester VPC that you
        own and an accepter VPC with which to create the connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/request_vpc_peering_connection.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcrequest_vpc_peering_connection-method)
        """

    async def wait_until_available(self) -> None:
        """
        Waits until Vpc is available.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/wait_until_available.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcwait_until_available-method)
        """

    async def wait_until_exists(self) -> None:
        """
        Waits until Vpc is exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/wait_until_exists.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcwait_until_exists-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpc/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcreload-method)
        """


_Vpc = Vpc


class VpcPeeringConnection(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpcpeeringconnection/index.html#EC2.VpcPeeringConnection)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcpeeringconnection)
    """

    id: str
    accepter_vpc: Vpc
    requester_vpc: Vpc
    accepter_vpc_info: Awaitable[VpcPeeringConnectionVpcInfoTypeDef]
    expiration_time: Awaitable[datetime]
    requester_vpc_info: Awaitable[VpcPeeringConnectionVpcInfoTypeDef]
    status: Awaitable[VpcPeeringConnectionStateReasonTypeDef]
    tags: Awaitable[List[TagTypeDef]]
    vpc_peering_connection_id: Awaitable[str]
    meta: EC2ResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this VpcPeeringConnection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpcpeeringconnection/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcpeeringconnectionget_available_subresources-method)
        """

    async def accept(
        self, **kwargs: Unpack[AcceptVpcPeeringConnectionRequestVpcPeeringConnectionAcceptTypeDef]
    ) -> AcceptVpcPeeringConnectionResultTypeDef:
        """
        Accept a VPC peering connection request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpcpeeringconnection/accept.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcpeeringconnectionaccept-method)
        """

    async def delete(
        self, **kwargs: Unpack[DeleteVpcPeeringConnectionRequestVpcPeeringConnectionDeleteTypeDef]
    ) -> DeleteVpcPeeringConnectionResultTypeDef:
        """
        Deletes a VPC peering connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpcpeeringconnection/delete.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcpeeringconnectiondelete-method)
        """

    async def reject(
        self, **kwargs: Unpack[RejectVpcPeeringConnectionRequestVpcPeeringConnectionRejectTypeDef]
    ) -> RejectVpcPeeringConnectionResultTypeDef:
        """
        Rejects a VPC peering connection request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpcpeeringconnection/reject.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcpeeringconnectionreject-method)
        """

    async def wait_until_exists(self) -> None:
        """
        Waits until VpcPeeringConnection is exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpcpeeringconnection/wait_until_exists.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcpeeringconnectionwait_until_exists-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpcpeeringconnection/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcpeeringconnectionload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpcpeeringconnection/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcpeeringconnectionreload-method)
        """


_VpcPeeringConnection = VpcPeeringConnection


class VpcAddress(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpcaddress/index.html#EC2.VpcAddress)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcaddress)
    """

    allocation_id: str
    association: NetworkInterfaceAssociation
    association_id: Awaitable[str]
    domain: Awaitable[DomainTypeType]
    network_interface_id: Awaitable[str]
    network_interface_owner_id: Awaitable[str]
    private_ip_address: Awaitable[str]
    tags: Awaitable[List[TagTypeDef]]
    public_ipv4_pool: Awaitable[str]
    network_border_group: Awaitable[str]
    customer_owned_ip: Awaitable[str]
    customer_owned_ipv4_pool: Awaitable[str]
    carrier_ip: Awaitable[str]
    subnet_id: Awaitable[str]
    service_managed: Awaitable[ServiceManagedType]
    instance_id: Awaitable[str]
    public_ip: Awaitable[str]
    meta: EC2ResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this VpcAddress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpcaddress/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcaddressget_available_subresources-method)
        """

    async def associate(
        self, **kwargs: Unpack[AssociateAddressRequestVpcAddressAssociateTypeDef]
    ) -> AssociateAddressResultTypeDef:
        """
        Associates an Elastic IP address, or carrier IP address (for instances that are
        in subnets in Wavelength Zones) with an instance or a network interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpcaddress/associate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcaddressassociate-method)
        """

    async def release(
        self, **kwargs: Unpack[ReleaseAddressRequestVpcAddressReleaseTypeDef]
    ) -> None:
        """
        Releases the specified Elastic IP address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpcaddress/release.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcaddressrelease-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpcaddress/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcaddressload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpcaddress/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcaddressreload-method)
        """


_VpcAddress = VpcAddress


class EC2ResourceMeta(ResourceMeta):
    client: EC2Client  # type: ignore[override]


class EC2ServiceResource(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/index.html)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/)
    """

    meta: EC2ResourceMeta  # type: ignore[override]
    classic_addresses: ServiceResourceClassicAddressesCollection
    dhcp_options_sets: ServiceResourceDhcpOptionsSetsCollection
    images: ServiceResourceImagesCollection
    instances: ServiceResourceInstancesCollection
    internet_gateways: ServiceResourceInternetGatewaysCollection
    key_pairs: ServiceResourceKeyPairsCollection
    network_acls: ServiceResourceNetworkAclsCollection
    network_interfaces: ServiceResourceNetworkInterfacesCollection
    placement_groups: ServiceResourcePlacementGroupsCollection
    route_tables: ServiceResourceRouteTablesCollection
    security_groups: ServiceResourceSecurityGroupsCollection
    snapshots: ServiceResourceSnapshotsCollection
    subnets: ServiceResourceSubnetsCollection
    volumes: ServiceResourceVolumesCollection
    vpc_addresses: ServiceResourceVpcAddressesCollection
    vpc_peering_connections: ServiceResourceVpcPeeringConnectionsCollection
    vpcs: ServiceResourceVpcsCollection

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourceget_available_subresources-method)
        """

    async def create_dhcp_options(
        self, **kwargs: Unpack[CreateDhcpOptionsRequestServiceResourceCreateDhcpOptionsTypeDef]
    ) -> _DhcpOptions:
        """
        Creates a custom set of DHCP options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_dhcp_options.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_dhcp_options-method)
        """

    async def create_instances(
        self, **kwargs: Unpack[RunInstancesRequestServiceResourceCreateInstancesTypeDef]
    ) -> List[_Instance]:
        """
        Launches the specified number of instances using an AMI for which you have
        permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_instances.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_instances-method)
        """

    async def create_internet_gateway(
        self,
        **kwargs: Unpack[CreateInternetGatewayRequestServiceResourceCreateInternetGatewayTypeDef],
    ) -> _InternetGateway:
        """
        Creates an internet gateway for use with a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_internet_gateway.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_internet_gateway-method)
        """

    async def create_key_pair(
        self, **kwargs: Unpack[CreateKeyPairRequestServiceResourceCreateKeyPairTypeDef]
    ) -> _KeyPair:
        """
        Creates an ED25519 or 2048-bit RSA key pair with the specified name and in the
        specified format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_key_pair.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_key_pair-method)
        """

    async def create_network_acl(
        self, **kwargs: Unpack[CreateNetworkAclRequestServiceResourceCreateNetworkAclTypeDef]
    ) -> _NetworkAcl:
        """
        Creates a network ACL in a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_network_acl.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_network_acl-method)
        """

    async def create_network_interface(
        self,
        **kwargs: Unpack[CreateNetworkInterfaceRequestServiceResourceCreateNetworkInterfaceTypeDef],
    ) -> _NetworkInterface:
        """
        Creates a network interface in the specified subnet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_network_interface.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_network_interface-method)
        """

    async def create_placement_group(
        self,
        **kwargs: Unpack[CreatePlacementGroupRequestServiceResourceCreatePlacementGroupTypeDef],
    ) -> _PlacementGroup:
        """
        Creates a placement group in which to launch instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_placement_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_placement_group-method)
        """

    async def create_route_table(
        self, **kwargs: Unpack[CreateRouteTableRequestServiceResourceCreateRouteTableTypeDef]
    ) -> _RouteTable:
        """
        Creates a route table for the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_route_table.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_route_table-method)
        """

    async def create_security_group(
        self, **kwargs: Unpack[CreateSecurityGroupRequestServiceResourceCreateSecurityGroupTypeDef]
    ) -> _SecurityGroup:
        """
        Creates a security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_security_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_security_group-method)
        """

    async def create_snapshot(
        self, **kwargs: Unpack[CreateSnapshotRequestServiceResourceCreateSnapshotTypeDef]
    ) -> _Snapshot:
        """
        Creates a snapshot of an EBS volume and stores it in Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_snapshot.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_snapshot-method)
        """

    async def create_subnet(
        self, **kwargs: Unpack[CreateSubnetRequestServiceResourceCreateSubnetTypeDef]
    ) -> _Subnet:
        """
        Creates a subnet in the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_subnet.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_subnet-method)
        """

    async def create_tags(
        self, **kwargs: Unpack[CreateTagsRequestServiceResourceCreateTagsTypeDef]
    ) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_tags.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_tags-method)
        """

    async def create_volume(
        self, **kwargs: Unpack[CreateVolumeRequestServiceResourceCreateVolumeTypeDef]
    ) -> _Volume:
        """
        Creates an EBS volume that can be attached to an instance in the same
        Availability Zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_volume.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_volume-method)
        """

    async def create_vpc(
        self, **kwargs: Unpack[CreateVpcRequestServiceResourceCreateVpcTypeDef]
    ) -> _Vpc:
        """
        Creates a VPC with the specified CIDR blocks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_vpc.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_vpc-method)
        """

    async def create_vpc_peering_connection(
        self,
        **kwargs: Unpack[
            CreateVpcPeeringConnectionRequestServiceResourceCreateVpcPeeringConnectionTypeDef
        ],
    ) -> _VpcPeeringConnection:
        """
        Requests a VPC peering connection between two VPCs: a requester VPC that you
        own and an accepter VPC with which to create the connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_vpc_peering_connection.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_vpc_peering_connection-method)
        """

    async def disassociate_route_table(
        self,
        **kwargs: Unpack[DisassociateRouteTableRequestServiceResourceDisassociateRouteTableTypeDef],
    ) -> None:
        """
        Disassociates a subnet or gateway from a route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/disassociate_route_table.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcedisassociate_route_table-method)
        """

    async def import_key_pair(
        self, **kwargs: Unpack[ImportKeyPairRequestServiceResourceImportKeyPairTypeDef]
    ) -> _KeyPairInfo:
        """
        Imports the public key from an RSA or ED25519 key pair that you created using a
        third-party tool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/import_key_pair.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourceimport_key_pair-method)
        """

    async def register_image(
        self, **kwargs: Unpack[RegisterImageRequestServiceResourceRegisterImageTypeDef]
    ) -> _Image:
        """
        Registers an AMI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/register_image.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourceregister_image-method)
        """

    async def ClassicAddress(self, public_ip: str) -> _ClassicAddress:
        """
        Creates a ClassicAddress resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/ClassicAddress.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourceclassicaddress-method)
        """

    async def DhcpOptions(self, id: str) -> _DhcpOptions:
        """
        Creates a DhcpOptions resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/DhcpOptions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcedhcpoptions-method)
        """

    async def Image(self, id: str) -> _Image:
        """
        Creates a Image resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/Image.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourceimage-method)
        """

    async def Instance(self, id: str) -> _Instance:
        """
        Creates a Instance resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/Instance.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourceinstance-method)
        """

    async def InternetGateway(self, id: str) -> _InternetGateway:
        """
        Creates a InternetGateway resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/InternetGateway.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourceinternetgateway-method)
        """

    async def KeyPair(self, name: str) -> _KeyPair:
        """
        Creates a KeyPair resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/KeyPair.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcekeypair-method)
        """

    async def NetworkAcl(self, id: str) -> _NetworkAcl:
        """
        Creates a NetworkAcl resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/NetworkAcl.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcenetworkacl-method)
        """

    async def NetworkInterface(self, id: str) -> _NetworkInterface:
        """
        Creates a NetworkInterface resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/NetworkInterface.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcenetworkinterface-method)
        """

    async def NetworkInterfaceAssociation(self, id: str) -> _NetworkInterfaceAssociation:
        """
        Creates a NetworkInterfaceAssociation resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/NetworkInterfaceAssociation.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcenetworkinterfaceassociation-method)
        """

    async def PlacementGroup(self, name: str) -> _PlacementGroup:
        """
        Creates a PlacementGroup resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/PlacementGroup.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourceplacementgroup-method)
        """

    async def Route(self, route_table_id: str, destination_cidr_block: str) -> _Route:
        """
        Creates a Route resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/Route.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourceroute-method)
        """

    async def RouteTable(self, id: str) -> _RouteTable:
        """
        Creates a RouteTable resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/RouteTable.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourceroutetable-method)
        """

    async def RouteTableAssociation(self, id: str) -> _RouteTableAssociation:
        """
        Creates a RouteTableAssociation resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/RouteTableAssociation.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourceroutetableassociation-method)
        """

    async def SecurityGroup(self, id: str) -> _SecurityGroup:
        """
        Creates a SecurityGroup resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/SecurityGroup.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcesecuritygroup-method)
        """

    async def Snapshot(self, id: str) -> _Snapshot:
        """
        Creates a Snapshot resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/Snapshot.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcesnapshot-method)
        """

    async def Subnet(self, id: str) -> _Subnet:
        """
        Creates a Subnet resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/Subnet.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcesubnet-method)
        """

    async def Tag(self, resource_id: str, key: str, value: str) -> _Tag:
        """
        Creates a Tag resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/Tag.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcetag-method)
        """

    async def Volume(self, id: str) -> _Volume:
        """
        Creates a Volume resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/Volume.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcevolume-method)
        """

    async def Vpc(self, id: str) -> _Vpc:
        """
        Creates a Vpc resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/Vpc.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcevpc-method)
        """

    async def VpcPeeringConnection(self, id: str) -> _VpcPeeringConnection:
        """
        Creates a VpcPeeringConnection resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/VpcPeeringConnection.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcevpcpeeringconnection-method)
        """

    async def VpcAddress(self, allocation_id: str) -> _VpcAddress:
        """
        Creates a VpcAddress resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/VpcAddress.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcevpcaddress-method)
        """
