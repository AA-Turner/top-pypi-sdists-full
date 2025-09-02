"""
State module for managing EC2 Spot instance request

.. note::

    The describe function uses the describe_spot_instance_requests to request spot instance details.
    The present function uses the request_spot_instances to request creation of a spot instance.
    The delete function uses the standard terminate_instances as the cancel_spot_requests does
    not terminate an instance that comes online.

    If you wish to delete or terminate an instance, and it's a spot instance, you must use the describe
    function here to obtain the InstanceID and then use ec2.instance.absent to fully terminate the instance.
"""
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List


__contracts__ = ["resource", "soft_fail"]


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    *,
    launch_specification: make_dataclass(
        "RequestSpotLaunchSpecification",
        [
            ("SecurityGroupIds", List[str], field(default=None)),
            ("SecurityGroups", List[str], field(default=None)),
            ("AddressingType", str, field(default=None)),
            (
                "BlockDeviceMappings",
                List[
                    make_dataclass(
                        "BlockDeviceMapping",
                        [
                            ("DeviceName", str, field(default=None)),
                            ("VirtualName", str, field(default=None)),
                            (
                                "Ebs",
                                make_dataclass(
                                    "EbsBlockDevice",
                                    [
                                        (
                                            "DeleteOnTermination",
                                            bool,
                                            field(default=None),
                                        ),
                                        ("Iops", int, field(default=None)),
                                        ("SnapshotId", str, field(default=None)),
                                        ("VolumeSize", int, field(default=None)),
                                        ("VolumeType", str, field(default=None)),
                                        ("KmsKeyId", str, field(default=None)),
                                        ("Throughput", int, field(default=None)),
                                        ("OutpostArn", str, field(default=None)),
                                        ("Encrypted", bool, field(default=None)),
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
            ("EbsOptimized", bool, field(default=None)),
            (
                "IamInstanceProfile",
                make_dataclass(
                    "IamInstanceProfileSpecification",
                    [
                        ("Arn", str, field(default=None)),
                        ("Name", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("ImageId", str, field(default=None)),
            ("InstanceType", str, field(default=None)),
            ("KernelId", str, field(default=None)),
            ("KeyName", str, field(default=None)),
            (
                "Monitoring",
                make_dataclass("RunInstancesMonitoringEnabled", [("Enabled", bool)]),
                field(default=None),
            ),
            (
                "NetworkInterfaces",
                List[
                    make_dataclass(
                        "InstanceNetworkInterfaceSpecification",
                        [
                            ("AssociatePublicIpAddress", bool, field(default=None)),
                            ("DeleteOnTermination", bool, field(default=None)),
                            ("Description", str, field(default=None)),
                            ("DeviceIndex", int, field(default=None)),
                            ("Groups", List[str], field(default=None)),
                            ("Ipv6AddressCount", int, field(default=None)),
                            (
                                "Ipv6Addresses",
                                List[
                                    make_dataclass(
                                        "InstanceIpv6Address",
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
                            ("AssociateCarrierIpAddress", bool, field(default=None)),
                            ("InterfaceType", str, field(default=None)),
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
            (
                "Placement",
                make_dataclass(
                    "SpotPlacement",
                    [
                        ("AvailabilityZone", str, field(default=None)),
                        ("GroupName", str, field(default=None)),
                        ("Tenancy", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("RamdiskId", str, field(default=None)),
            ("SubnetId", str, field(default=None)),
            ("UserData", str, field(default=None)),
        ],
    ) = None,
    launch_group: str = None,
    spot_price: str = None,
    type: str = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass(
            "Tag",
            [("Key", str, field(default=None)), ("Value", str, field(default=None))],
        )
    ] = None,
    # The following parameters can only be specified at creation
    availability_zone_group: str = None,
    instance_count: int = None,
    instance_interruption_behavior: str = None,
    valid_from: str = None,
    valid_until: str = None,
    **kwargs,
) -> Dict[str, Any]:
    """Creates a Spot Instance request.

    To use Spot Instances, you create a Spot Instance request that includes the desired number of instances, the instance
    type, and the Availability Zone. If capacity is available, Amazon EC2 fulfills your request immediately. Otherwise,
    Amazon EC2 waits until your request can be fulfilled or until you cancel the request.

    Args:

        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            The spot instance request id.

        availability_zone_group(str, Optional):
            The user-specified name for a logical grouping of requests.When you specify an Availability Zone group in a
            Spot Instance request, all Spot Instances in the request are launched in the same Availability Zone.Instance
            proximity is maintained with this parameter, but the choice of Availability Zone is not. The group applies
            only to requests for Spot Instances of the same instance type. Any additional Spot Instance requests that are
            specified with the same Availability Zone group name are launched in that same Availability Zone, as long as
            at least one instance from the group is still active.

            If there is no active instance running in the Availability Zone group that you specify for a new Spot Instance
            request (all instances are terminated, the request is expired, or the maximum price you specified falls below
            current Spot price), then Amazon EC2 launches the instance in any Availability Zone where the constraint can
            be met. Consequently, the subsequent set of Spot Instances could be placed in a different zone from the original
            request, even if you specified the same Availability Zone group.

            Default: Instances are launched in any available Availability Zone.

        instance_count(int, Optional):
            The maximum number of Spot Instances to launch.

        instance_interruption_behavior(str, Optional):
            The behavior when a Spot Instance is interrupted. The default is terminate.
            Valid Values: hibernate | stop | terminate
        launch_group(str, Optional):
            The instance launch group. Launch groups are Spot Instances that launch together and terminate together.
            Default: Instances are launched and terminated individually

        launch_specification(dict[str, Any], Optional):
            The launch specification. Defaults to None.

            * SecurityGroupIds (list[str], Optional):
                One or more security group IDs.

            * SecurityGroups (list[str], Optional):
                One or more security groups. When requesting instances in a VPC, you must specify the IDs of the
                security groups. When requesting instances in EC2-Classic, you can specify the names or the IDs
                of the security groups.

            * AddressingType (str, Optional):
                Deprecated.

            * BlockDeviceMappings (list[dict[str, Any]], Optional):
                One or more block device mapping entries. You can't specify both a snapshot ID and an encryption
                value. This is because only blank volumes can be encrypted on creation. If a snapshot is the
                basis for a volume, it is not blank and its encryption status is used for the volume encryption
                status.

                * DeviceName (str, Optional):
                    The device name (for example, /dev/sdh or xvdh).

                * VirtualName (str, Optional):
                    The virtual device name (ephemeralN). Instance store volumes are numbered starting from 0. An
                    instance type with 2 available instance store volumes can specify mappings for ephemeral0 and
                    ephemeral1. The number of available instance store volumes depends on the instance type. After
                    you connect to the instance, you must mount the volume. NVMe instance store volumes are
                    automatically enumerated and assigned a device name. Including them in your block device mapping
                    has no effect. Constraints: For M3 instances, you must specify instance store volumes in the
                    block device mapping for the instance. When you launch an M3 instance, we ignore any instance
                    store volumes specified in the block device mapping for the AMI.

                * Ebs (dict[str, Any], Optional):
                    Parameters used to automatically set up EBS volumes when the instance is launched.

                    * DeleteOnTermination (bool, Optional):
                        Indicates whether the EBS volume is deleted on instance termination. For more information, see
                        Preserving Amazon EBS volumes on instance termination in the Amazon EC2 User Guide.

                    * Iops (int, Optional): The number of I/O operations per second (IOPS). For gp3, io1, and io2 volumes,
                        this represents the number of IOPS that are provisioned for the volume. For gp2 volumes, this
                        represents the baseline performance of the volume and the rate at which the volume accumulates
                        I/O credits for bursting. The following are the supported values for each volume type:
                        gp3: 3,000-16,000 IOPS io1: 100-64,000 IOPS    io2: 100-64,000 IOPS   For io1 and io2 volumes,
                        we guarantee 64,000 IOPS only for Instances built on the Nitro System. Other instance families
                        guarantee performance up to 32,000 IOPS. This parameter is required for io1 and io2 volumes.
                        The default for gp3 volumes is 3,000 IOPS. This parameter is not supported for gp2, st1, sc1, or
                        standard volumes.

                    * SnapshotId (str, Optional): The ID of the snapshot.

                    * VolumeSize (int, Optional): The size of the volume, in GiBs. You must specify either a snapshot ID
                        or a volume size. If you specify a snapshot, the default is the snapshot size. You can specify a
                        volume size that is equal to or larger than the snapshot size. The following are the supported
                        volumes sizes for each volume type:    gp2 and gp3:1-16,384    io1 and io2: 4-16,384    st1 and
                        sc1: 125-16,384 standard: 1-1,024

                    * VolumeType (str, Optional): The volume type. For more information, see Amazon EBS volume types in
                        the Amazon EC2 User Guide. If the volume type is io1 or io2, you must specify the IOPS that the
                        volume supports.

                    * KmsKeyId (str, Optional): Identifier (key ID, key alias, ID ARN, or alias ARN) for a customer
                        managed CMK under which the EBS volume is encrypted. This parameter is only supported on
                        BlockDeviceMapping objects called by RunInstances, RequestSpotFleet, and RequestSpotInstances.

                    * Throughput (int, Optional): The throughput that the volume supports, in MiB/s. This parameter is
                        valid only for gp3 volumes. Valid Range: Minimum value of 125. Maximum value of 1000.

                    * OutpostArn (str, Optional): The ARN of the Outpost on which the snapshot is stored. This parameter
                        is only supported on BlockDeviceMapping objects called by  CreateImage.

                    * Encrypted (bool, Optional): Indicates whether the encryption state of an EBS volume is changed while
                        being restored from a backing snapshot. The effect of setting the encryption state to true depends
                        on the volume origin (new or from a snapshot), starting encryption state, ownership, and whether
                        encryption by default is enabled. For more information, see Amazon EBS encryption in the Amazon
                        EC2 User Guide. In no case can you remove encryption from an encrypted volume. Encrypted volumes
                        can only be attached to instances that support Amazon EBS encryption. For more information, see
                        Supported instance types. This parameter is not returned by DescribeImageAttribute.

                * NoDevice (str, Optional):
                    To omit the device from the block device mapping, specify an empty string. When this property is
                    specified, the device is removed from the block device mapping regardless of the assigned value.

            * EbsOptimized (bool, Optional):
                Indicates whether the instance is optimized for EBS I/O. This optimization provides dedicated
                throughput to Amazon EBS and an optimized configuration stack to provide optimal EBS I/O
                performance. This optimization isn't available with all instance types. Additional usage charges
                apply when using an EBS Optimized instance. Default: false

            * IamInstanceProfile (dict[str, Any], Optional):
                The IAM instance profile.

                * Arn (str, Optional): The Amazon Resource Name (ARN) of the instance profile.
                * Name (str, Optional): The name of the instance profile.

            * ImageId (str, Optional):
                The ID of the AMI.

            * InstanceType (str, Optional):
                The instance type. Only one instance type can be specified.

            * KernelId (str, Optional):
                The ID of the kernel.

            * KeyName (str, Optional):
                The name of the key pair.

            * Monitoring (dict[str, Any], Optional):
                Indicates whether basic or detailed monitoring is enabled for the instance. Default: Disabled

                * Enabled (bool): Indicates whether detailed monitoring is enabled. Otherwise, basic monitoring is enabled.

            * NetworkInterfaces (list[dict[str, Any]], Optional):
                One or more network interfaces. If you specify a network interface, you must specify subnet IDs
                and security group IDs using the network interface.

                * AssociatePublicIpAddress (bool, Optional): Indicates whether to assign a public IPv4 address to an
                    instance you launch in a VPC. The public IP address can only be assigned to a network interface for
                    eth0, and can only be assigned to a new network interface, not an existing one. You cannot specify
                    more than one network interface in the request. If launching into a default subnet, the default value
                    is true.

                * DeleteOnTermination (bool, Optional): If set to true, the interface is deleted when the instance is
                    terminated. You can specify true only if creating a new network interface when launching an instance.

                * Description (str, Optional): The description of the network interface. Applies only if creating a network
                    interface when launching an instance.

                * DeviceIndex (int, Optional): The position of the network interface in the attachment order. A primary
                    network interface has a device index of 0. If you specify a network interface when launching an instance,
                    you must specify the device index.

                * Groups (list[str], Optional): The IDs of the security groups for the network interface. Applies only
                    if creating a network interface when launching an instance.

                * Ipv6AddressCount (int, Optional): A number of IPv6 addresses to assign to the network interface. Amazon
                    EC2 chooses the IPv6 addresses from the range of the subnet. You cannot specify this option and the
                    option to assign specific IPv6 addresses in the same request. You can specify this option if you've
                    specified a minimum number of instances to launch.

                * Ipv6Addresses (list[dict[str, Any]], Optional): One or more IPv6 addresses to assign to the network
                    interface. You cannot specify this option and the option to assign a number of IPv6 addresses in the
                    same request. You cannot specify this option if you've specified a minimum number of instances to launch.

                    * Ipv6Address (str, Optional): The IPv6 address.

                * NetworkInterfaceId (str, Optional): The ID of the network interface. If you are creating a Spot Fleet,
                    omit this parameter because you can’t specify a network interface ID in a launch specification.

                * PrivateIpAddress (str, Optional): The private IPv4 address of the network interface. Applies only if
                    creating a network interface when launching an instance. You cannot specify this option if you're
                    launching more than one instance in a RunInstances request.

                * PrivateIpAddresses (list[dict[str, Any]], Optional): One or more private IPv4 addresses to assign to
                    the network interface. Only one private IPv4 address can be designated as primary. You cannot specify
                    this option if you're launching more than one instance in a RunInstances request.

                    * Primary (bool, Optional): Indicates whether the private IPv4 address is the primary private IPv4
                        address. Only one IPv4 address can be designated as primary.

                    * PrivateIpAddress (str, Optional): The private IPv4 addresses.

                * SecondaryPrivateIpAddressCount (int, Optional): The number of secondary private IPv4 addresses. You can't specify this option and specify more
                    than one private IP address using the private IP addresses option. You cannot specify this
                    option if you're launching more than one instance in a RunInstances request.

                * SubnetId (str, Optional): The ID of the subnet associated with the network interface. Applies only if creating a network
                    interface when launching an instance.

                * AssociateCarrierIpAddress (bool, Optional): Indicates whether to assign a carrier IP address to the network interface. You can only assign a
                    carrier IP address to a network interface that is in a subnet in a Wavelength Zone. For more
                    information about carrier IP addresses, see Carrier IP addresses in the Amazon Web Services
                    Wavelength Developer Guide.

                * InterfaceType (str, Optional): The type of network interface. Valid values: interface | efa

                * NetworkCardIndex (int, Optional): The index of the network card. Some instance types support multiple network cards. The primary
                    network interface must be assigned to network card index 0. The default is network card index 0.
                    If you are using RequestSpotInstances to create Spot Instances, omit this parameter because you
                    can’t specify the network card index when using this API. To specify the network card index, use
                    RunInstances.

                * Ipv4Prefixes (list[dict[str, Any]], Optional): One or more IPv4 delegated prefixes to be assigned to the network interface. You cannot use this
                    option if you use the Ipv4PrefixCount option.
                    * Ipv4Prefix (str, Optional): The IPv4 prefix. For information, see  Assigning prefixes to Amazon EC2 network interfaces in
                        the Amazon Elastic Compute Cloud User Guide.

                * Ipv4PrefixCount (int, Optional): The number of IPv4 delegated prefixes to be automatically assigned to the network interface. You
                    cannot use this option if you use the Ipv4Prefix option.

                * Ipv6Prefixes (list[dict[str, Any]], Optional): One or more IPv6 delegated prefixes to be assigned to the network interface. You cannot use this
                    option if you use the Ipv6PrefixCount option.
                    * Ipv6Prefix (str, Optional): The IPv6 prefix.

                * Ipv6PrefixCount (int, Optional): The number of IPv6 delegated prefixes to be automatically assigned to the network interface. You
                    cannot use this option if you use the Ipv6Prefix option.

            * Placement (dict[str, Any], Optional):
                The placement information for the instance.

                * AvailabilityZone (str, Optional): The Availability Zone. [Spot Fleet only] To specify multiple Availability Zones, separate them
                    using commas; for example, "us-west-2a, us-west-2b".

                * GroupName (str, Optional): The name of the placement group.

                * Tenancy (str, Optional): The tenancy of the instance (if the instance is running in a VPC). An instance with a tenancy of
                    dedicated runs on single-tenant hardware. The host tenancy is not supported for Spot Instances.

            * RamdiskId (str, Optional):
                The ID of the RAM disk.

            * SubnetId (str, Optional):
                The ID of the subnet in which to launch the instance.

            * UserData (str, Optional):
                The Base64-encoded user data for the instance. User data is limited to 16 KB.

        spot_price(str, Optional):
            The maximum price per hour that you are willing to pay for a Spot Instance.
            The default is the On-Demand price.

        tags(dict or list, Optional):
            Dict in the format of ``{tag-key: tag-value}`` or List of tags in the format of
            ``[{"Key": tag-key, "Value": tag-value}]`` to associate with the spot instance. Each tag consists of a key
            name and an associated value. Defaults to None.

            * Key (str, Optional):
                The key of the tag. Constraints: Tag keys are case-sensitive and accept a maximum of 127 Unicode
                characters. May not begin with aws:.

            * Value (str, Optional):
                The value of the tag. Constraints: Tag values are case-sensitive and accept a maximum of 256
                Unicode characters.

        type(str, Optional):
            The Spot Instance request type.
            Default: one-time
            Valid Values: one-time | persistent

        valid_from(str, Optional):
            The start date of the request. If this is a one-time request, the request becomes active at this date and
            time and remains active until all instances launch, the request expires, or the request is canceled. If the
            request is persistent, the request becomes active at this date and time and remains active until it expires
            or is canceled.

            The specified start date and time cannot be equal to the current date and time. You must specify a start date
            and time that occurs after the current date and time.

        valid_until(str, Optional):
            The end date of the request, in UTC format (YYYY-MM-DDTHH:MM:SSZ).

            For a persistent request, the request remains active until the ValidUntil date and time is reached. Otherwise,
            the request remains active until you cancel it.

            For a one-time request, the request remains active until all instances launch, the request is canceled, or
            the ValidUntil date and time is reached.
            By default, the request is valid for 7 days from the date the request was created.

            Type: Timestamp

            Required: No

    Request Syntax:
        .. code-block:: sls

            resource_is_present:
              aws.ec2.spot_instance.present:
                - name: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              aws.ec2.spot_instance.present:
                - name: value
                - instance_count: 5
                - launch_specification:
                    ImageId: ami-fce3c696
                    KeyName: awskey.pem
                    SecurityGroups: ['sg-709f8709']
                    InstanceType: m4.large
                    Placement:
                        AvailabilityZone: us-east-1a
                    BlockDeviceMappings:
                        Ebs:
                            SnapshotId: snap-f70deff0
                            VolumeSize: 100
                            DeleteOnTermination: True
                            VolumeType: gp2
                            Iops: 300
                            Encrypted: False
                    EbsOptimized: True
                    Monitoring:
                        Enabled: True
                    SecurityGroupIds: sg-709f8709
                - spot_price: 0.03
                - type: one-time
    """
    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "name", "resource_id", "kwargs")
    }
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    for key in kwargs:
        result["comment"] += [f"Not explicitly supported keyword argument: '{key}'"]

    # Get the resource_id from ESM
    if resource_id is None:
        resource_id = (ctx.old_state or {}).get("resource_id")

    if resource_id:
        # Assume that the spot_instance_request already exists since we have a resource_id
        result["old_state"] = await hub.tool.aws.ec2.spot_instance_request.get(
            ctx, resource_id=resource_id
        )

        if not result["old_state"]:
            result["comment"] += [
                f"Could not find spot_instance_request for '{name}' with existing id '{resource_id}'"
            ]
            return result
        result["comment"] += [f"Spot Instance Request '{name}' already exists"]
    else:
        if ctx.test:
            result["new_state"] = hub.tool.aws.ec2.instance.state.test(**desired_state)
            result["comment"] += [f"Would create aws.ec2.instance '{name}'"]
            return result
        if isinstance(tags, List):
            tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)
        tag_specification = (
            [
                {
                    "ResourceType": "instance",
                    "Tags": hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags),
                }
            ]
            if tags
            else None
        )
        # Although it's not specified in the API documentation,
        # apparently 'SecurityGroups' parameter requires the
        # names of the security groups, not the IDs, inside the
        # LaunchSpecification dict
        create_ret = await hub.exec.boto3.client.ec2.request_spot_instances(
            ctx,
            DryRun=False,
            AvailabilityZoneGroup=availability_zone_group,
            InstanceCount=instance_count,
            LaunchGroup=launch_group,
            LaunchSpecification=launch_specification,
            SpotPrice=spot_price,
            Type=type,
            ValidFrom=valid_from,
            ValidUntil=valid_until,
            TagSpecifications=tag_specification,
            InstanceInterruptionBehavior=instance_interruption_behavior,
        )
        result["result"] &= create_ret.result
        if not create_ret:
            result["comment"] += [create_ret.comment]
            return result

        result["comment"] += [f"Created '{name}'"]
        resource_id = create_ret.ret["SpotInstanceRequests"][0]["SpotInstanceRequestId"]

    # Update the spot_instance request now that it exists
    current_state = await hub.tool.aws.ec2.spot_instance_request.get(
        ctx, resource_id=resource_id
    )
    changes_made = False
    for attribute, new_value in desired_state.items():
        if new_value is None:
            # No value has been explicitly given, leave this parameter alone
            continue
        if attribute in (
            "availability_zone_group",
            "instance_count",
            "instance_interruption_behavior",
            "valid_from",
            "valid_until",
        ):
            result["comment"] += [
                f"'{attribute}' is only available on creation of a new spot instance request"
            ]
            continue
        if current_state.get(attribute) != new_value:
            changes_made = True
            if ctx.test:
                result["comment"] += [
                    f"Would update aws.ec2.instance '{name}': {attribute}"
                ]
                continue
            # TODO Update the spot instance request to match the changed parameters
            result["comment"] += [
                f"Currently unable to update aws.ec2.spot_instance_request attribute: {attribute}"
            ]

    # Get the final state of the resource
    if changes_made:
        if ctx.test:
            result["new_state"] = hub.tool.aws.ec2.spot_instance_request.test(
                **desired_state
            )
        else:
            result["new_state"] = await hub.tool.aws.ec2.spot_instance_request.get(
                ctx, resource_id=resource_id
            )
    else:
        result["new_state"] = current_state

    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """
    Cancels one or more Spot Instance requests.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            The spot instance request id

    Request Syntax:
        .. code-block:: sls

            [spot_instance-resource-id]:
              aws.ec2.spot_instance.absent:
                - name: "string"
                - resource_id: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.ec2.spot_instance.absent:
                - name: value
    """
    result = dict(
        comment=[], old_state=ctx.old_state, new_state=None, name=name, result=True
    )

    # Get the resource_id from ESM
    if resource_id is None:
        resource_id = (ctx.old_state or {}).get("resource_id")

    # If there still is no resource_id, the instance is gone
    if not resource_id:
        result["comment"] += [f"'{name}' already cancelled"]
        return result

    if ctx.test:
        result["comment"] += [f"Would cancel aws.ec2.spot_instance_request '{name}'"]
        return result

    ret = await hub.exec.boto3.client.ec2.cancel_spot_instance_requests(
        ctx,
        DryRun=False,
        SpotInstanceRequestIds=[resource_id],
    )

    result["result"] &= ret["result"]
    if not result["result"]:
        result["comment"].append(ret["comment"])
        return result
    result["comment"] += [f"cancelled spot instance request '{name}'"]

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.ec2.spot_instance_request
    """
    result = {}
    ret = await hub.exec.boto3.client.ec2.describe_spot_instance_requests(ctx)

    if not ret:
        hub.log.warning(f"Could not describe spot instance requests: {ret.comment}")
        return {}

    spot_instance_requests = hub.tool.aws.ec2.spot_instance_request.convert_to_present(
        ret.ret
    )

    for resource_id, present_state in spot_instance_requests.items():
        result[resource_id] = {
            "aws.ec2.spot_instance_request.present": [
                {k: v} for k, v in present_state.items()
            ]
        }

    return result
