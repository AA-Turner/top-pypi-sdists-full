"""State module for managing EC2 Launch Template."""
import copy
import datetime
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]

from dict_tools import differ


async def present(
    hub,
    ctx,
    name: str,
    launch_template_data: make_dataclass(
        "RequestLaunchTemplateData",
        [
            ("KernelId", str, field(default=None)),
            ("EbsOptimized", bool, field(default=None)),
            (
                "IamInstanceProfile",
                make_dataclass(
                    "LaunchTemplateIamInstanceProfileSpecificationRequest",
                    [
                        ("Arn", str, field(default=None)),
                        ("Name", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "BlockDeviceMappings",
                List[
                    make_dataclass(
                        "LaunchTemplateBlockDeviceMappingRequest",
                        [
                            ("DeviceName", str, field(default=None)),
                            ("VirtualName", str, field(default=None)),
                            (
                                "Ebs",
                                make_dataclass(
                                    "LaunchTemplateEbsBlockDeviceRequest",
                                    [
                                        ("Encrypted", bool, field(default=None)),
                                        (
                                            "DeleteOnTermination",
                                            bool,
                                            field(default=None),
                                        ),
                                        ("Iops", int, field(default=None)),
                                        ("KmsKeyId", str, field(default=None)),
                                        ("SnapshotId", str, field(default=None)),
                                        ("VolumeSize", int, field(default=None)),
                                        ("VolumeType", str, field(default=None)),
                                        ("Throughput", int, field(default=None)),
                                    ],
                                ),
                                field(default=None),
                            ),
                            ("NoDevice", str, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
            (
                "NetworkInterfaces",
                List[
                    make_dataclass(
                        "LaunchTemplateInstanceNetworkInterfaceSpecificationRequest",
                        [
                            ("AssociateCarrierIpAddress", bool, field(default=None)),
                            ("AssociatePublicIpAddress", bool, field(default=None)),
                            ("DeleteOnTermination", bool, field(default=None)),
                            ("Description", str, field(default=None)),
                            ("DeviceIndex", int, field(default=None)),
                            ("Groups", List[str], field(default=None)),
                            ("InterfaceType", str, field(default=None)),
                            ("Ipv6AddressCount", int, field(default=None)),
                            (
                                "Ipv6Addresses",
                                List[
                                    make_dataclass(
                                        "InstanceIpv6AddressRequest",
                                        [("Ipv6Address", str, field(default=None))],
                                    )
                                ],
                                field(default=None),
                            ),
                            ("NetworkInterfaceId", str, field(default=None)),
                            ("PrivateIpAddress", str, field(default=None)),
                            (
                                "PrivateIpAddresses",
                                List[
                                    make_dataclass(
                                        "PrivateIpAddressSpecification",
                                        [
                                            ("Primary", bool, field(default=None)),
                                            (
                                                "PrivateIpAddress",
                                                str,
                                                field(default=None),
                                            ),
                                        ],
                                    )
                                ],
                                field(default=None),
                            ),
                            (
                                "SecondaryPrivateIpAddressCount",
                                int,
                                field(default=None),
                            ),
                            ("SubnetId", str, field(default=None)),
                            ("NetworkCardIndex", int, field(default=None)),
                            (
                                "Ipv4Prefixes",
                                List[
                                    make_dataclass(
                                        "Ipv4PrefixSpecificationRequest",
                                        [("Ipv4Prefix", str, field(default=None))],
                                    )
                                ],
                                field(default=None),
                            ),
                            ("Ipv4PrefixCount", int, field(default=None)),
                            (
                                "Ipv6Prefixes",
                                List[
                                    make_dataclass(
                                        "Ipv6PrefixSpecificationRequest",
                                        [("Ipv6Prefix", str, field(default=None))],
                                    )
                                ],
                                field(default=None),
                            ),
                            ("Ipv6PrefixCount", int, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
            ("ImageId", str, field(default=None)),
            ("InstanceType", str, field(default=None)),
            ("KeyName", str, field(default=None)),
            (
                "Monitoring",
                make_dataclass(
                    "LaunchTemplatesMonitoringRequest",
                    [("Enabled", bool, field(default=None))],
                ),
                field(default=None),
            ),
            (
                "Placement",
                make_dataclass(
                    "LaunchTemplatePlacementRequest",
                    [
                        ("AvailabilityZone", str, field(default=None)),
                        ("Affinity", str, field(default=None)),
                        ("GroupName", str, field(default=None)),
                        ("HostId", str, field(default=None)),
                        ("Tenancy", str, field(default=None)),
                        ("SpreadDomain", str, field(default=None)),
                        ("HostResourceGroupArn", str, field(default=None)),
                        ("PartitionNumber", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("RamDiskId", str, field(default=None)),
            ("DisableApiTermination", bool, field(default=None)),
            ("InstanceInitiatedShutdownBehavior", str, field(default=None)),
            ("UserData", str, field(default=None)),
            (
                "TagSpecifications",
                List[
                    make_dataclass(
                        "LaunchTemplateTagSpecificationRequest",
                        [
                            ("ResourceType", str, field(default=None)),
                            (
                                "Tags",
                                List[
                                    make_dataclass(
                                        "Tag",
                                        [
                                            ("Key", str, field(default=None)),
                                            ("Value", str, field(default=None)),
                                        ],
                                    )
                                ],
                                field(default=None),
                            ),
                        ],
                    )
                ],
                field(default=None),
            ),
            (
                "ElasticGpuSpecifications",
                List[make_dataclass("ElasticGpuSpecification", [("Type", str)])],
                field(default=None),
            ),
            (
                "ElasticInferenceAccelerators",
                List[
                    make_dataclass(
                        "LaunchTemplateElasticInferenceAccelerator",
                        [("Type", str), ("Count", int, field(default=None))],
                    )
                ],
                field(default=None),
            ),
            ("SecurityGroupIds", List[str], field(default=None)),
            ("SecurityGroups", List[str], field(default=None)),
            (
                "InstanceMarketOptions",
                make_dataclass(
                    "LaunchTemplateInstanceMarketOptionsRequest",
                    [
                        ("MarketType", str, field(default=None)),
                        (
                            "SpotOptions",
                            make_dataclass(
                                "LaunchTemplateSpotMarketOptionsRequest",
                                [
                                    ("MaxPrice", str, field(default=None)),
                                    ("SpotInstanceType", str, field(default=None)),
                                    ("BlockDurationMinutes", int, field(default=None)),
                                    ("ValidUntil", datetime, field(default=None)),
                                    (
                                        "InstanceInterruptionBehavior",
                                        str,
                                        field(default=None),
                                    ),
                                ],
                            ),
                            field(default=None),
                        ),
                    ],
                ),
                field(default=None),
            ),
            (
                "CreditSpecification",
                make_dataclass("CreditSpecificationRequest", [("CpuCredits", str)]),
                field(default=None),
            ),
            (
                "CpuOptions",
                make_dataclass(
                    "LaunchTemplateCpuOptionsRequest",
                    [
                        ("CoreCount", int, field(default=None)),
                        ("ThreadsPerCore", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "CapacityReservationSpecification",
                make_dataclass(
                    "LaunchTemplateCapacityReservationSpecificationRequest",
                    [
                        ("CapacityReservationPreference", str, field(default=None)),
                        (
                            "CapacityReservationTarget",
                            make_dataclass(
                                "CapacityReservationTarget",
                                [
                                    ("CapacityReservationId", str, field(default=None)),
                                    (
                                        "CapacityReservationResourceGroupArn",
                                        str,
                                        field(default=None),
                                    ),
                                ],
                            ),
                            field(default=None),
                        ),
                    ],
                ),
                field(default=None),
            ),
            (
                "LicenseSpecifications",
                List[
                    make_dataclass(
                        "LaunchTemplateLicenseConfigurationRequest",
                        [("LicenseConfigurationArn", str, field(default=None))],
                    )
                ],
                field(default=None),
            ),
            (
                "HibernationOptions",
                make_dataclass(
                    "LaunchTemplateHibernationOptionsRequest",
                    [("Configured", bool, field(default=None))],
                ),
                field(default=None),
            ),
            (
                "MetadataOptions",
                make_dataclass(
                    "LaunchTemplateInstanceMetadataOptionsRequest",
                    [
                        ("HttpTokens", str, field(default=None)),
                        ("HttpPutResponseHopLimit", int, field(default=None)),
                        ("HttpEndpoint", str, field(default=None)),
                        ("HttpProtocolIpv6", str, field(default=None)),
                        ("InstanceMetadataTags", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "EnclaveOptions",
                make_dataclass(
                    "LaunchTemplateEnclaveOptionsRequest",
                    [("Enabled", bool, field(default=None))],
                ),
                field(default=None),
            ),
            (
                "InstanceRequirements",
                make_dataclass(
                    "InstanceRequirementsRequest",
                    [
                        (
                            "VCpuCount",
                            make_dataclass(
                                "VCpuCountRangeRequest",
                                [("Min", int), ("Max", int, field(default=None))],
                            ),
                        ),
                        (
                            "MemoryMiB",
                            make_dataclass(
                                "MemoryMiBRequest",
                                [("Min", int), ("Max", int, field(default=None))],
                            ),
                        ),
                        ("CpuManufacturers", List[str], field(default=None)),
                        (
                            "MemoryGiBPerVCpu",
                            make_dataclass(
                                "MemoryGiBPerVCpuRequest",
                                [
                                    ("Min", float, field(default=None)),
                                    ("Max", float, field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                        ("ExcludedInstanceTypes", List[str], field(default=None)),
                        ("InstanceGenerations", List[str], field(default=None)),
                        (
                            "SpotMaxPricePercentageOverLowestPrice",
                            int,
                            field(default=None),
                        ),
                        (
                            "OnDemandMaxPricePercentageOverLowestPrice",
                            int,
                            field(default=None),
                        ),
                        ("BareMetal", str, field(default=None)),
                        ("BurstablePerformance", str, field(default=None)),
                        ("RequireHibernateSupport", bool, field(default=None)),
                        (
                            "NetworkInterfaceCount",
                            make_dataclass(
                                "NetworkInterfaceCountRequest",
                                [
                                    ("Min", int, field(default=None)),
                                    ("Max", int, field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                        ("LocalStorage", str, field(default=None)),
                        ("LocalStorageTypes", List[str], field(default=None)),
                        (
                            "TotalLocalStorageGB",
                            make_dataclass(
                                "TotalLocalStorageGBRequest",
                                [
                                    ("Min", float, field(default=None)),
                                    ("Max", float, field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                        (
                            "BaselineEbsBandwidthMbps",
                            make_dataclass(
                                "BaselineEbsBandwidthMbpsRequest",
                                [
                                    ("Min", int, field(default=None)),
                                    ("Max", int, field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                        ("AcceleratorTypes", List[str], field(default=None)),
                        (
                            "AcceleratorCount",
                            make_dataclass(
                                "AcceleratorCountRequest",
                                [
                                    ("Min", int, field(default=None)),
                                    ("Max", int, field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                        ("AcceleratorManufacturers", List[str], field(default=None)),
                        ("AcceleratorNames", List[str], field(default=None)),
                        (
                            "AcceleratorTotalMemoryMiB",
                            make_dataclass(
                                "AcceleratorTotalMemoryMiBRequest",
                                [
                                    ("Min", int, field(default=None)),
                                    ("Max", int, field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                    ],
                ),
                field(default=None),
            ),
            (
                "PrivateDnsNameOptions",
                make_dataclass(
                    "LaunchTemplatePrivateDnsNameOptionsRequest",
                    [
                        ("HostnameType", str, field(default=None)),
                        ("EnableResourceNameDnsARecord", bool, field(default=None)),
                        ("EnableResourceNameDnsAAAARecord", bool, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "MaintenanceOptions",
                make_dataclass(
                    "LaunchTemplateInstanceMaintenanceOptionsRequest",
                    [("AutoRecovery", str, field(default=None))],
                ),
                field(default=None),
            ),
            ("DisableApiStop", bool, field(default=None)),
        ],
    ),
    name_prefix: str = None,
    resource_id: str = None,
    dry_run: bool = None,
    version_description: str = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass("Tag", [("Key", str), ("Value", str, field(default=None))])
    ] = None,
) -> Dict[str, Any]:
    """Creates a launch template.

    A launch template contains the parameters to launch an instance. When you launch an
    instance using RunInstances, you can specify a launch template instead of providing the launch parameters in the
    request. For more information, see Launch an instance from a launch template in the Amazon Elastic Compute Cloud
    User Guide. If you want to clone an existing launch template as the basis for creating a new launch template,
    you can use the Amazon EC2 console. The API, SDKs, and CLI do not support cloning a template. For more
    information, see Create a launch template from an existing launch template in the Amazon Elastic Compute Cloud
    User Guide.

    Args:
        name(str):
            An Idem name of the resource.
        name_prefix(str, Optional):
            Creates a unique name beginning with the specified prefix.

            .. Note::
                Either `name` or `name_prefix` should be specified.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.
        dry_run(bool, Optional):
            Checks whether you have the required permissions for the action, without actually making the
            request, and provides an error response. If you have the required permissions, the error
            response is DryRunOperation. Otherwise, it is UnauthorizedOperation. Defaults to None.
        version_description(str, Optional):
            A description for the first version of the launch template. Defaults to None.
        launch_template_data(Dict[str, Any]):
            The information for the launch template.
                * KernelId (str, Optional):
                    The ID of the kernel.  We recommend that you use PV-GRUB instead of kernels and RAM disks. For
                    more information, see User provided kernels in the Amazon Elastic Compute Cloud User Guide.
                * EbsOptimized (bool, Optional):
                    Indicates whether the instance is optimized for Amazon EBS I/O. This optimization provides
                    dedicated throughput to Amazon EBS and an optimized configuration stack to provide optimal
                    Amazon EBS I/O performance. This optimization isn't available with all instance types.
                    Additional usage charges apply when using an EBS-optimized instance.
                * IamInstanceProfile (dict[str, Any], Optional):
                    The name or Amazon Resource Name (ARN) of an IAM instance profile.
                        * Arn (str, Optional):
                            The Amazon Resource Name (ARN) of the instance profile.
                        * Name (str, Optional):
                            The name of the instance profile.
                * BlockDeviceMappings (list[dict[str, Any]], Optional):
                    The block device mapping.
                        * DeviceName (str, Optional):
                            The device name (for example, /dev/sdh or xvdh).
                        * VirtualName (str, Optional):
                            The virtual device name (ephemeralN). Instance store volumes are numbered starting from 0. An
                            instance type with 2 available instance store volumes can specify mappings for ephemeral0 and
                            ephemeral1. The number of available instance store volumes depends on the instance type. After
                            you connect to the instance, you must mount the volume.
                        * Ebs (dict[str, Any], Optional):
                            Parameters used to automatically set up EBS volumes when the instance is launched.
                                * Encrypted (bool, Optional):
                                    Indicates whether the EBS volume is encrypted. Encrypted volumes can only be attached to
                                    instances that support Amazon EBS encryption. If you are creating a volume from a snapshot, you
                                    can't specify an encryption value.
                                * DeleteOnTermination (bool, Optional):
                                    Indicates whether the EBS volume is deleted on instance termination.
                                * Iops (int, Optional):
                                    The number of I/O operations per second (IOPS). For gp3, io1, and io2 volumes, this represents
                                    the number of IOPS that are provisioned for the volume. For gp2 volumes, this represents the
                                    baseline performance of the volume and the rate at which the volume accumulates I/O credits for
                                    bursting. The following are the supported values for each volume type:    gp3: 3,000-16,000 IOPS
                                    io1: 100-64,000 IOPS    io2: 100-64,000 IOPS   For io1 and io2 volumes, we guarantee 64,000 IOPS
                                    only for Instances built on the Nitro System. Other instance families guarantee performance up
                                    to 32,000 IOPS. This parameter is supported for io1, io2, and gp3 volumes only. This parameter
                                    is not supported for gp2, st1, sc1, or standard volumes.
                                * KmsKeyId (str, Optional):
                                    The ARN of the symmetric Key Management Service (KMS) CMK used for encryption.
                                * SnapshotId (str, Optional):
                                    The ID of the snapshot.
                                * VolumeSize (int, Optional):
                                    The size of the volume, in GiBs. You must specify either a snapshot ID or a volume size. The
                                    following are the supported volumes sizes for each volume type: gp2 and gp3: 1-16,384    io1
                                    and io2: 4-16,384 st1 and sc1: 125-16,384 standard: 1-1,024
                                * VolumeType (str, Optional):
                                    The volume type. For more information, see Amazon EBS volume types in the Amazon Elastic Compute
                                    Cloud User Guide.
                                * Throughput (int, Optional):
                                    The throughput to provision for a gp3 volume, with a maximum of 1,000 MiB/s. Valid Range:
                                    Minimum value of 125. Maximum value of 1000.
                        * NoDevice (str, Optional):
                            To omit the device from the block device mapping, specify an empty string.
            * NetworkInterfaces (list[dict[str, Any]], Optional):
                One or more network interfaces. If you specify a network interface, you must specify any
                security groups and subnets as part of the network interface.

                * AssociateCarrierIpAddress (bool, Optional):
                        Associates a Carrier IP address with eth0 for a new network interface. Use this option when you
                        launch an instance in a Wavelength Zone and want to associate a Carrier IP address with the
                        network interface. For more information about Carrier IP addresses, see Carrier IP addresses in
                        the Wavelength Developer Guide.
                * AssociatePublicIpAddress (bool, Optional):
                        Associates a public IPv4 address with eth0 for a new network interface.

                * DeleteOnTermination (bool, Optional):
                        Indicates whether the network interface is deleted when the instance is terminated.

                * Description (str, Optional):
                    A description for the network interface.

                    * DeviceIndex (int, Optional):
                        The device index for the network interface attachment.

                    * Groups (list[str], Optional):
                        The IDs of one or more security groups.

                    * InterfaceType (str, Optional):
                        The type of network interface. To create an Elastic Fabric Adapter (EFA), specify efa. For more
                        information, see Elastic Fabric Adapter in the Amazon Elastic Compute Cloud User Guide. If you
                        are not creating an EFA, specify interface or omit this parameter. Valid values: interface | efa

                    * Ipv6AddressCount (int, Optional):
                        The number of IPv6 addresses to assign to a network interface. Amazon EC2 automatically selects
                        the IPv6 addresses from the subnet range. You can't use this option if specifying specific IPv6
                        addresses.

                    * Ipv6Addresses (list[dict[str, Any]], Optional):
                        One or more specific IPv6 addresses from the IPv6 CIDR block range of your subnet. You can't use
                        this option if you're specifying a number of IPv6 addresses.

                        * Ipv6Address (str, Optional):
                                The IPv6 address.

                    * NetworkInterfaceId (str, Optional):
                        The ID of the network interface.
                    * PrivateIpAddress (str, Optional):
                        The primary private IPv4 address of the network interface.
                    * PrivateIpAddresses (list[dict[str, Any]], Optional):
                        One or more private IPv4 addresses.
                            * Primary (bool, Optional):
                                Indicates whether the private IPv4 address is the primary private IPv4 address. Only one IPv4
                                address can be designated as primary.
                            * PrivateIpAddress (str, Optional):
                                The private IPv4 address.
                    * SecondaryPrivateIpAddressCount (int, Optional):
                        The number of secondary private IPv4 addresses to assign to a network interface.
                    * SubnetId (str, Optional):
                        The ID of the subnet for the network interface.
                    * NetworkCardIndex (int, Optional):
                        The index of the network card. Some instance types support multiple network cards. The primary
                        network interface must be assigned to network card index 0. The default is network card index 0.
                    * Ipv4Prefixes (list[dict[str, Any]], Optional):
                        One or more IPv4 prefixes to be assigned to the network interface. You cannot use this option if
                        you use the Ipv4PrefixCount option.

                        * Ipv4Prefix (str, Optional):
                                The IPv4 prefix. For information, see  Assigning prefixes to Amazon EC2 network interfaces in
                                the Amazon Elastic Compute Cloud User Guide.

                    * Ipv4PrefixCount (int, Optional):
                        The number of IPv4 prefixes to be automatically assigned to the network interface. You cannot
                        use this option if you use the Ipv4Prefix option.
                    * Ipv6Prefixes (list[dict[str, Any]], Optional):
                        One or more IPv6 prefixes to be assigned to the network interface. You cannot use this option if
                        you use the Ipv6PrefixCount option.

                        * Ipv6Prefix (str, Optional):
                                The IPv6 prefix.

                    * Ipv6PrefixCount (int, Optional):
                        The number of IPv6 prefixes to be automatically assigned to the network interface. You cannot
                        use this option if you use the Ipv6Prefix option.
            * ImageId (str, Optional):
                The ID of the AMI.
            * InstanceType (str, Optional):
                The instance type. For more information, see Instance types in the Amazon Elastic Compute Cloud
                User Guide. If you specify InstanceType, you can't specify InstanceRequirements.
            * KeyName (str, Optional):
                The name of the key pair. You can create a key pair using CreateKeyPair or ImportKeyPair.  If
                you do not specify a key pair, you can't connect to the instance unless you choose an AMI that
                is configured to allow users another way to log in.
            * Monitoring (dict[str, Any], Optional):
                The monitoring for the instance.
                    * Enabled (bool, Optional):
                        Specify true to enable detailed monitoring. Otherwise, basic monitoring is enabled.
            * Placement (dict[str, Any], Optional):
                The placement for the instance.
                    * AvailabilityZone (str, Optional):
                        The Availability Zone for the instance.
                    * Affinity (str, Optional):
                        The affinity setting for an instance on a Dedicated Host.
                    * GroupName (str, Optional):
                        The name of the placement group for the instance.
                    * HostId (str, Optional):
                        The ID of the Dedicated Host for the instance.
                    * Tenancy (str, Optional):
                        The tenancy of the instance (if the instance is running in a VPC). An instance with a tenancy of
                        dedicated runs on single-tenant hardware.
                    * SpreadDomain (str, Optional):
                        Reserved for future use.
                    * HostResourceGroupArn (str, Optional):
                        The ARN of the host resource group in which to launch the instances. If you specify a host
                        resource group ARN, omit the Tenancy parameter or set it to host.
                    * PartitionNumber (int, Optional):
                        The number of the partition the instance should launch in. Valid only if the placement group
                        strategy is set to partition.
            * RamDiskId (str, Optional):
                The ID of the RAM disk.  We recommend that you use PV-GRUB instead of kernels and RAM disks. For
                more information, see User provided kernels in the Amazon Elastic Compute Cloud User Guide.
            * DisableApiTermination (bool, Optional):
                If you set this parameter to true, you can't terminate the instance using the Amazon EC2
                console, CLI, or API; otherwise, you can. To change this attribute after launch, use
                ModifyInstanceAttribute. Alternatively, if you set InstanceInitiatedShutdownBehavior to
                terminate, you can terminate the instance by running the shutdown command from the instance.
            * InstanceInitiatedShutdownBehavior (str, Optional):
                Indicates whether an instance stops or terminates when you initiate shutdown from the instance
                (using the operating system command for system shutdown). Default: stop
            * UserData (str, Optional):
                The user data to make available to the instance. You must provide base64-encoded str. User data
                is limited to 16 KB. For more information, see Run commands on your Linux instance at launch
                (Linux) or Work with instance user data (Windows) in the Amazon Elastic Compute Cloud User
                Guide. If you are creating the launch template for use with Batch, the user data must be
                provided in the  MIME multi-part archive format. For more information, see Amazon EC2 user data
                in launch templates in the Batch User Guide.
            * TagSpecifications (list[dict[str, Any]], Optional):
                The tags to apply to the resources that are created during instance launch. You can specify tags
                for the following resources only:   Instances   Volumes   Elastic graphics   Spot Instance
                requests   Network interfaces   To tag a resource after it has been created, see CreateTags.  To
                tag the launch template itself, you must use the TagSpecification parameter.

                * ResourceType (str, Optional):
                        The type of resource to tag. The Valid Values are all the resource types that can be tagged.
                        However, when creating a launch template, you can specify tags for the following resource types
                        only: instance | volume | elastic-gpu | network-interface | spot-instances-request  To tag a
                        resource after it has been created, see CreateTags.
                * Tags (list[dict[str, Any]], Optional):
                        The tags to apply to the resource.

                        * Key (str, Optional):
                                The key of the tag. Constraints: Tag keys are case-sensitive and accept a maximum of 127 Unicode
                                characters. May not begin with aws:.

                        * Value (str, Optional):
                                The value of the tag. Constraints: Tag values are case-sensitive and accept a maximum of 256
                                Unicode characters.
            * ElasticGpuSpecifications (list[dict[str, Any]], Optional):
                An elastic GPU to associate with the instance.

                * Type (str):
                    The type of Elastic Graphics accelerator. For more information about the values to specify for
                    Type, see Elastic Graphics Basics, specifically the Elastic Graphics accelerator column, in the
                    Amazon Elastic Compute Cloud User Guide for Windows Instances.

            * ElasticInferenceAccelerators (list[dict[str, Any]], Optional):
                The elastic inference accelerator for the instance.

                * Type (str):
                    The type of elastic inference accelerator. The possible values are eia1.medium, eia1.large, and
                    eia1.xlarge.

                * Count (int, Optional):
                    The number of elastic inference accelerators to attach to the instance.

                    Default: 1

            * SecurityGroupIds (list[str], Optional):
                One or more security group IDs. You can create a security group using CreateSecurityGroup. You
                cannot specify both a security group ID and security name in the same request.
            * SecurityGroups (list[str], Optional):
                One or more security group names. For a nondefault VPC, you must use security group IDs instead.
                You cannot specify both a security group ID and security name in the same request.
            * InstanceMarketOptions (dict[str, Any], Optional):
                The market (purchasing) option for the instances.

                * MarketType (str, Optional):
                    The market type.

                * SpotOptions (Dict[str, Any], Optional):
                    The options for Spot Instances.

                    * MaxPrice (str, Optional):
                        The maximum hourly price you're willing to pay for the Spot Instances. We do not recommend using
                        this parameter because it can lead to increased interruptions. If you do not specify this
                        parameter, you will pay the current Spot price.  If you specify a maximum price, your Spot
                        Instances will be interrupted more frequently than if you do not specify this parameter.

                    * SpotInstanceType (str, Optional):
                        The Spot Instance request type.

                    * BlockDurationMinutes (int, Optional):
                        Deprecated.

                    * ValidUntil (datetime, Optional):
                        The end date of the request, in UTC format (YYYY-MM-DDTHH:MM:SSZ). Supported only for persistent
                        requests.   For a persistent request, the request remains active until the ValidUntil date and
                        time is reached. Otherwise, the request remains active until you cancel it.   For a one-time
                        request, ValidUntil is not supported. The request remains active until all instances launch or
                        you cancel the request.   Default: 7 days from the current date

                    * InstanceInterruptionBehavior (str, Optional):
                        The behavior when a Spot Instance is interrupted. The default is terminate.

            * CreditSpecification (dict[str, Any], Optional):
                The credit option for CPU usage of the instance. Valid only for T instances.
                * CpuCredits (str):
                    The credit option for CPU usage of a T instance. Valid values: standard | unlimited
            * CpuOptions (dict[str, Any], Optional):
                The CPU options for the instance. For more information, see Optimizing CPU Options in the Amazon
            Elastic Compute Cloud User Guide.
                * CoreCount (int, Optional):
                    The number of CPU cores for the instance.
                * ThreadsPerCore (int, Optional):
                    The number of threads per CPU core. To disable multithreading for the instance, specify a value
                    of 1. Otherwise, specify the default value of 2.
            * CapacityReservationSpecification (dict[str, Any], Optional):
                The Capacity Reservation targeting option. If you do not specify this parameter, the instance's
                Capacity Reservation preference defaults to open, which enables it to run in any open Capacity
                Reservation that has matching attributes (instance type, platform, Availability Zone).
                * CapacityReservationPreference (str, Optional):
                    Indicates the instance's Capacity Reservation preferences. Possible preferences include:
                     open - The instance can run in any open Capacity Reservation that has matching attributes (instance
                            type, platform, Availability Zone).
                     none - The instance avoids running in a Capacity Reservation even if one is available.
                            The instance runs in On-Demand capacity.
                * CapacityReservationTarget (dict[str, Any], Optional):
                    Information about the target Capacity Reservation or Capacity Reservation group.
                    * CapacityReservationId (str, Optional):
                        The ID of the Capacity Reservation in which to run the instance.
                    * CapacityReservationResourceGroupArn (str, Optional):
                        The ARN of the Capacity Reservation resource group in which to run the instance.
            * LicenseSpecifications (list[dict[str, Any]], Optional):
                The license configurations.
                * LicenseConfigurationArn (str, Optional):
                    The Amazon Resource Name (ARN) of the license configuration.
            * HibernationOptions (dict[str, Any], Optional):
                Indicates whether an instance is enabled for hibernation. This parameter is valid only if the
                instance meets the hibernation prerequisites. For more information, see Hibernate your instance
                in the Amazon Elastic Compute Cloud User Guide.
                * Configured (bool, Optional):
                    If you set this parameter to true, the instance is enabled for hibernation. Default: false
            * MetadataOptions (dict[str, Any], Optional):
                The metadata options for the instance. For more information, see Instance metadata and user data
                in the Amazon Elastic Compute Cloud User Guide.
                * HttpTokens (str, Optional):
                    The state of token usage for your instance metadata requests. If the parameter is not specified
                    in the request, the default state is Optional. If the state is Optional, you can choose to
                    retrieve instance metadata with or without a signed token header on your request. If you
                    retrieve the IAM role credentials without a token, the version 1.0 role credentials are
                    returned. If you retrieve the IAM role credentials using a valid signed token, the version 2.0
                    role credentials are returned. If the state is required, you must send a signed token header
                    with any instance metadata retrieval requests. In this state, retrieving the IAM role
                    credentials always returns the version 2.0 credentials; the version 1.0 credentials are not
                    available.
                * HttpPutResponseHopLimit (int, Optional):
                    The desired HTTP PUT response hop limit for instance metadata requests. The larger the number,
                    the further instance metadata requests can travel. Default: 1  Possible values: Integers from 1
                    to 64
                * HttpEndpoint (str, Optional):
                    Enables or disables the HTTP metadata endpoint on your instances. If the parameter is not
                    specified, the default state is enabled.  If you specify a value of disabled, you will not be
                    able to access your instance metadata.
                * HttpProtocolIpv6 (str, Optional):
                    Enables or disables the IPv6 endpoint for the instance metadata service. Default: disabled
                * InstanceMetadataTags (str, Optional):
                    Set to enabled to allow access to instance tags from the instance metadata. Set to disabled to
                    turn off access to instance tags from the instance metadata. For more information, see Work with
                    instance tags using the instance metadata. Default: disabled
            * EnclaveOptions (dict[str, Any], Optional):
                Indicates whether the instance is enabled for Amazon Web Services Nitro Enclaves. For more
                information, see  What is Amazon Web Services Nitro Enclaves? in the Amazon Web Services Nitro
                Enclaves User Guide. You can't enable Amazon Web Services Nitro Enclaves and hibernation on the
                same instance.
                * Enabled (bool, Optional):
                    To enable the instance for Amazon Web Services Nitro Enclaves, set this parameter to true.
            * InstanceRequirements (dict[str, Any], Optional):
                The attributes for the instance types. When you specify instance attributes, Amazon EC2 will
                identify instance types with these attributes. If you specify InstanceRequirements, you can't
                specify InstanceType.
                * VCpuCount (dict[str, Any]):
                    The minimum and maximum number of vCPUs.
                    * Min (int):
                        The minimum number of vCPUs. To specify no minimum limit, specify 0.
                    * Max (int, Optional): The maximum number of vCPUs. To specify no maximum limit, omit this parameter.
                * MemoryMiB (dict[str, Any]):
                    The minimum and maximum amount of memory, in MiB.
                    * Min (int):
                        The minimum amount of memory, in MiB. To specify no minimum limit, specify 0.
                    * Max (int, Optional):
                        The maximum amount of memory, in MiB. To specify no maximum limit, omit this parameter.
                * CpuManufacturers (list[str], Optional):
                    The CPU manufacturers to include. For instance types with Intel CPUs, specify intel. For
                    instance types with AMD CPUs, specify amd. For instance types with Amazon Web Services CPUs,
                    specify amazon-web-services. Don't confuse the CPU manufacturer with the CPU architecture.
                    Instances will be launched with a compatible CPU architecture based on the Amazon Machine Image
                    (AMI) that you specify in your launch template. Default: Any manufacturer
                * MemoryGiBPerVCpu (dict[str, Any], Optional):
                    The minimum and maximum amount of memory per vCPU, in GiB. Default: No minimum or maximum limits
                    * Min (float, Optional):
                        The minimum amount of memory per vCPU, in GiB. To specify no minimum limit, omit this parameter.
                    * Max (float, Optional):
                        The maximum amount of memory per vCPU, in GiB. To specify no maximum limit, omit this parameter.
                * ExcludedInstanceTypes (list[str], Optional):
                    The instance types to exclude. You can use strings with one or more wild cards, represented by
                    an asterisk (*), to exclude an instance family, type, size, or generation. The following are
                    examples: m5.8xlarge, c5*.*, m5a.*, r*, *3*. For example, if you specify c5*,Amazon EC2 will
                    exclude the entire C5 instance family, which includes all C5a and C5n instance types. If you
                    specify m5a.*, Amazon EC2 will exclude all the M5a instance types, but not the M5n instance
                    types. Default: No excluded instance types
                * InstanceGenerations (list[str], Optional):
                    Indicates whether current or previous generation instance types are included. The current
                    generation instance types are recommended for use. Current generation instance types are
                    typically the latest two to three generations in each instance family. For more information, see
                    Instance types in the Amazon EC2 User Guide. For current generation instance types, specify
                    current. For previous generation instance types, specify previous. Default: Current and previous
                    generation instance types
                * SpotMaxPricePercentageOverLowestPrice (int, Optional):
                    The price protection threshold for Spot Instance. This is the maximum you’ll pay for an Spot
                    Instance, expressed as a percentage above the least expensive current generation M, C, or R
                    instance type with your specified attributes. When Amazon EC2 selects instance types with your
                    attributes, it excludes instance types priced above your threshold. The parameter accepts an
                    integer, which Amazon EC2 interprets as a percentage. To turn off price protection, specify a
                    high value, such as 999999. This parameter is not supported for GetSpotPlacementScores and
                    GetInstanceTypesFromInstanceRequirements.  If you set TargetCapacityUnitType to vcpu or memory-
                    mib, the price protection threshold is applied based on the per-vCPU or per-memory price instead
                    of the per-instance price.  Default: 100
                * OnDemandMaxPricePercentageOverLowestPrice (int, Optional):
                    The price protection threshold for On-Demand Instances. This is the maximum you’ll pay for an
                On-Demand Instance, expressed as a percentage above the least expensive current generation M, C,
                or R instance type with your specified attributes. When Amazon EC2 selects instance types with
                your attributes, it excludes instance types priced above your threshold. The parameter accepts
                an integer, which Amazon EC2 interprets as a percentage. To turn off price protection, specify a
                high value, such as 999999. This parameter is not supported for GetSpotPlacementScores and
                GetInstanceTypesFromInstanceRequirements.  If you set TargetCapacityUnitType to vcpu or memory-
                mib, the price protection threshold is applied based on the per-vCPU or per-memory price instead
                of the per-instance price.  Default: 20
                * BareMetal (str, Optional):
                    Indicates whether bare metal instance types must be included, excluded, or required.   To
                    include bare metal instance types, specify included.   To require only bare metal instance
                    types, specify required.   To exclude bare metal instance types, specify excluded.   Default:
                    excluded
                * BurstablePerformance (str, Optional):
                    Indicates whether burstable performance T instance types are included, excluded, or required.
                    For more information, see Burstable performance instances.   To include burstable performance
                    instance types, specify included.   To require only burstable performance instance types,
                    specify required.   To exclude burstable performance instance types, specify excluded.
                    Default: excluded
                * RequireHibernateSupport (bool, Optional):
                    Indicates whether instance types must support hibernation for On-Demand Instances. This
                    parameter is not supported for GetSpotPlacementScores. Default: false
                * NetworkInterfaceCount (dict[str, Any], Optional):
                    The minimum and maximum number of network interfaces. Default: No minimum or maximum limits

                    * Min (int, Optional):
                        The minimum number of network interfaces. To specify no minimum limit, omit this parameter.

                    * Max (int, Optional):
                        The maximum number of network interfaces. To specify no maximum limit, omit this parameter.

                * LocalStorage (str, Optional):
                    Indicates whether instance types with instance store volumes are included, excluded, or
                    required. For more information, Amazon EC2 instance store in the Amazon EC2 User Guide.   To
                    include instance types with instance store volumes, specify included.   To require only instance
                    types with instance store volumes, specify required.   To exclude instance types with instance
                    store volumes, specify excluded.   Default: included
                * LocalStorageTypes (list[str], Optional):
                    The type of local storage that is required. For instance types with hard disk drive (HDD)
                    storage, specify hdd. For instance types with solid state drive (SSD) storage, specify ssd.
                    Default: hdd and ssd
                * TotalLocalStorageGB (dict[str, Any], Optional):
                    The minimum and maximum amount of total local storage, in GB. Default: No minimum or maximum
                    limits

                    * Min (float, Optional):
                        The minimum amount of total local storage, in GB. To specify no minimum limit, omit this
                        parameter.

                    * Max (float, Optional):
                        The maximum amount of total local storage, in GB. To specify no maximum limit, omit this
                        parameter.

                * BaselineEbsBandwidthMbps (dict[str, Any], Optional):
                    The minimum and maximum baseline bandwidth to Amazon EBS, in Mbps. For more information, see
                    Amazon EBS–optimized instances in the Amazon EC2 User Guide. Default: No minimum or maximum
                    limits

                    * Min (int, Optional):
                        The minimum baseline bandwidth, in Mbps. To specify no minimum limit, omit this parameter.

                    * Max (int, Optional):
                        The maximum baseline bandwidth, in Mbps. To specify no maximum limit, omit this parameter.

                * AcceleratorTypes (list[str], Optional):
                    The accelerator types that must be on the instance type.   To include instance types with GPU
                    hardware, specify gpu.   To include instance types with FPGA hardware, specify fpga.   To
                    include instance types with inference hardware, specify inference.   Default: Any accelerator
                    type
                * AcceleratorCount (dict[str, Any], Optional):
                    The minimum and maximum number of accelerators (GPUs, FPGAs, or Amazon Web Services Inferentia
                    chips) on an instance. To exclude accelerator-enabled instance types, set Max to 0. Default: No
                    minimum or maximum limits

                    * Min (int, Optional):
                        The minimum number of accelerators. To specify no minimum limit, omit this parameter.

                    * Max (int, Optional):
                        The maximum number of accelerators. To specify no maximum limit, omit this parameter. To exclude
                        accelerator-enabled instance types, set Max to 0.

                * AcceleratorManufacturers (list[str], Optional):
                    Indicates whether instance types must have accelerators by specific manufacturers.   For
                    instance types with NVIDIA devices, specify nvidia.   For instance types with AMD devices,
                    specify amd.   For instance types with Amazon Web Services devices, specify amazon-web-services.
                    For instance types with Xilinx devices, specify xilinx.   Default: Any manufacturer

                * AcceleratorNames (list[str], Optional):
                    The accelerators that must be on the instance type.   For instance types with NVIDIA A100 GPUs,
                    specify a100.   For instance types with NVIDIA V100 GPUs, specify v100.   For instance types
                    with NVIDIA K80 GPUs, specify k80.   For instance types with NVIDIA T4 GPUs, specify t4.   For
                    instance types with NVIDIA M60 GPUs, specify m60.   For instance types with AMD Radeon Pro V520
                    GPUs, specify radeon-pro-v520.   For instance types with Xilinx VU9P FPGAs, specify  vu9p.   For
                    instance types with Amazon Web Services Inferentia chips, specify inferentia.   For instance
                    types with NVIDIA GRID K520 GPUs, specify k520.   Default: Any accelerator

                * AcceleratorTotalMemoryMiB (dict[str, Any], Optional):
                    The minimum and maximum amount of total accelerator memory, in MiB. Default: No minimum or
                    maximum limits

                    * Min (int, Optional):
                        The minimum amount of accelerator memory, in MiB. To specify no minimum limit, omit this
                        parameter.

                    * Max (int, Optional):
                        The maximum amount of accelerator memory, in MiB. To specify no maximum limit, omit this
                        parameter.

            * PrivateDnsNameOptions (dict[str, Any], Optional):
                The options for the instance hostname. The default values are inherited from the subnet.

                * HostnameType (str, Optional):
                    The type of hostname for Amazon EC2 instances. For IPv4 only subnets, an instance DNS name must
                    be based on the instance IPv4 address. For IPv6 native subnets, an instance DNS name must be
                    based on the instance ID. For dual-stack subnets, you can specify whether DNS names use the
                    instance IPv4 address or the instance ID.

                * EnableResourceNameDnsARecord (bool, Optional):
                    Indicates whether to respond to DNS queries for instance hostnames with DNS A records.

                * EnableResourceNameDnsAAAARecord (bool, Optional):
                    Indicates whether to respond to DNS queries for instance hostnames with DNS AAAA records.

            * MaintenanceOptions (dict[str, Any], Optional):
                The maintenance options for the instance.

                * AutoRecovery (str, Optional):
                    Disables the automatic recovery behavior of your instance or sets it to default. For more
                    information, see Simplified automatic recovery.

            * DisableApiStop (bool, Optional):
                Indicates whether to enable the instance for stop protection. For more information, see Stop
                Protection.

        tags(Dict or List, Optional): Dict in the format of {tag-key: tag-value} or List of tags in the format of
            [{"Key": tag-key, "Value": tag-value}] to associate with the VPC.
            Each tag consists of a key name and an associated value. Defaults to None.
            * Key (str, Optional): The key of the tag. Constraints: Tag keys are case-sensitive and accept a maximum of 127 Unicode
                characters. May not begin with aws:.
            * Value(str, Optional): The value of the tag. Constraints: Tag values are case-sensitive and accept a maximum of 256
                Unicode characters.

    Request Syntax:
       .. code-block:: sls

          [launch-template-resource-id]:
              aws.ec2.launch_template.present:
                - name: string
                - name_prefix: string
                - dry_run: boolean
                - version_description: string
                - launch_template_data: dict
                - tags: dict or list

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            my_resource:
                aws.ec2.launch_template.present:
                  - name: Testversions
                  - resource_id: lt-08467ebddfaed30ad
                  - launch_template_name: Testversions
                  - create_time: '2022-11-08T08:55:48Z'
                  - tags:
                      Name: Testversions
                  - created_by: arn:aws:iam::746014882121:user/photonautomation
                  - default_version_number: 1
                  - latest_version_number: 4
                  - version_description: latest
                  - launch_template_data:
                      DisableApiTermination: false
                      HibernationOptions:
                        Configured: false
                      IamInstanceProfile:
                        Arn: arn:aws:iam::746014882121:instance-profile/bootstrap-idem-test-rs-terraform-eks
                      ImageId: ami-074b543ee210b32e7
                      InstanceInitiatedShutdownBehavior: terminate
                      InstanceRequirements:
                        MemoryMiB:
                          Max: 60
                          Min: 60
                        VCpuCount:
                          Max: 1
                          Min: 1
                      MaintenanceOptions:
                        AutoRecovery: default
                      MetadataOptions:
                        HttpEndpoint: enabled
                        HttpTokens: optional
                        InstanceMetadataTags: disabled
                      Monitoring:
                        Enabled: false
                      NetworkInterfaces:
                      - DeviceIndex: 0
                        Groups:
                        - sg-0ab44a7b6b855692f
                        SubnetId: subnet-0e15343bc21685b42
                      Placement:
                        Tenancy: dedicated
                      PrivateDnsNameOptions:
                        HostnameType: ip-name
                      TagSpecifications:
                      - ResourceType: instance
                        Tags:
                        - Key: name
                          Value: my_resource
                      - ResourceType: volume
                        Tags:
                        - Key: name
                          Value: bootstrap-idem-test-rs-fin
                      UserData: bHM=
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    if isinstance(tags, Dict):
        tags = hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
    if resource_id:
        before = await hub.exec.aws.ec2.launch_template.get(
            ctx, name=name, resource_id=resource_id
        )
    if before:
        if not before.get("result") and not before.get("ret"):
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = copy.deepcopy(before["ret"])
        result["old_state"]["name_prefix"] = name_prefix
        plan_state = copy.deepcopy(result["old_state"])
        old_tags = result["old_state"].get("tags")
        old_tags_list = hub.tool.aws.tag_utils.convert_tag_dict_to_list(old_tags)
        # Update tags
        if not hub.tool.aws.state_comparison_utils.are_lists_identical(
            tags, old_tags_list
        ):
            update_ret = await hub.tool.aws.ec2.tag.update_tags(
                ctx,
                resource_id=resource_id,
                old_tags=old_tags,
                new_tags=tags,
            )
            result["result"] = result["result"] and update_ret["result"]
            result["comment"] = update_ret["comment"]
            resource_updated = resource_updated or bool(update_ret["result"])
            if ctx.get("test", False) and update_ret["result"]:
                plan_state["tags"] = update_ret["ret"]

        # Compare current (existing) launch_template_data with desired state
        # If there is anything to be added or updated or removed then it should run create new version
        changes = differ.deep_diff(
            result["old_state"].get("launch_template_data", {}), launch_template_data
        )
        if bool(changes.get("new")) or bool(changes.get("old")):
            update_version_ret = (
                await hub.tool.aws.ec2.launch_template.update_launch_template_version(
                    ctx=ctx,
                    launch_template_id=resource_id,
                    new_launch_template_data=launch_template_data,
                )
            )
            if ctx.get("test", False) and update_version_ret["ret"]:
                plan_state["launch_template_data"] = update_version_ret["ret"]
                # version will always be updated by AWS in real mode
                plan_state["default_version_number"] = (
                    plan_state["default_version_number"] + 1
                )
                plan_state["latest_version_number"] = (
                    plan_state["latest_version_number"] + 1
                )
            result["comment"] += update_version_ret["comment"]
            resource_updated = resource_updated or bool(update_version_ret["ret"])
            result["result"] = result["result"] and update_version_ret["result"]

        if ctx.get("test", False) and resource_updated:
            result["new_state"] = plan_state
            result["comment"] = hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.ec2.launch_template", name=name
            )
            return result
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "name_prefix": name_prefix,
                    "dry_run": dry_run,
                    "version_description": version_description,
                    "tags": tags,
                    "launch_template_data": launch_template_data,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.ec2.launch_template", name=name
            )
            return result
        ret = await hub.exec.boto3.client.ec2.create_launch_template(
            ctx,
            ClientToken=name,
            DryRun=dry_run,
            LaunchTemplateName=name,
            VersionDescription=version_description,
            LaunchTemplateData=hub.tool.aws.ec2.launch_template.pre_process_launch_template_data(
                chunk=launch_template_data
            ),
            TagSpecifications=(
                [
                    {
                        "ResourceType": "launch-template",
                        "Tags": tags,
                    }
                ]
                if tags
                else None
            ),
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        resource_id = ret["ret"]["LaunchTemplate"]["LaunchTemplateId"]
        # This makes sure the created launch template is saved to esm regardless if the subsequent update call fails or not.
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.ec2.launch_template", name=name
        )
    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif (not result["old_state"]) or resource_updated:
        after = await hub.exec.aws.ec2.launch_template.get(
            ctx=ctx, name=name, resource_id=resource_id
        )

        if not after["result"]:
            result["result"] = False
            result["comment"] = after["comment"]
            return result
        result["new_state"] = copy.deepcopy(after["ret"])
        result["new_state"]["name_prefix"] = name_prefix
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes a launch template.

    Deleting a launch template deletes all of its versions.

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str, Optional):
            An identifier of the resource in the provider.

    Request Syntax:
       .. code-block:: sls

          [launch_template-id]:
              aws.ec2.launch_template.absent:
                - name: 'string'
                - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.ec2.launch_template.absent:
                - name: value
                - resource_id: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.launch_template", name=name
        )
        return result
    before = await hub.exec.aws.ec2.launch_template.get(
        ctx=ctx, name=name, resource_id=resource_id
    )

    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result
    elif not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.launch_template", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.ec2.launch_template", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]
        ret = await hub.exec.boto3.client.ec2.delete_launch_template(
            ctx, LaunchTemplateId=resource_id
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            result["result"] = False
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.ec2.launch_template", name=name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describes one or more launch templates.

    Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.ec2.launch_template
    """
    result = {}
    ret = await hub.exec.aws.ec2.launch_template.list(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not describe launch_template {ret['comment']}")
        return {}

    for resource in ret["ret"]:
        result[resource["resource_id"]] = {
            "aws.ec2.launch_template.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }

    return result
