"""State module for managing AWS Launch Configurations."""
import base64
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    name_prefix: str = None,
    resource_id: str = None,
    image_id: str = None,
    key_name: str = None,
    security_groups: List[str] = None,
    classic_link_vpc_id: str = None,
    classic_link_vpc_security_groups: List[str] = None,
    user_data: str = None,
    instance_id: str = None,
    instance_type: str = None,
    kernel_id: str = None,
    ramdisk_id: str = None,
    block_device_mappings: List[
        make_dataclass(
            "BlockDeviceMapping",
            [
                ("DeviceName", str),
                ("VirtualName", str, field(default=None)),
                (
                    "Ebs",
                    make_dataclass(
                        "Ebs",
                        [
                            ("SnapshotId", str, field(default=None)),
                            ("VolumeSize", int, field(default=None)),
                            ("VolumeType", str, field(default=None)),
                            ("DeleteOnTermination", bool, field(default=None)),
                            ("Iops", int, field(default=None)),
                            ("Encrypted", bool, field(default=None)),
                            ("Throughput", int, field(default=None)),
                        ],
                    ),
                    field(default=None),
                ),
                ("NoDevice", bool, field(default=None)),
            ],
        )
    ] = None,
    instance_monitoring: make_dataclass(
        "InstanceMonitoring", [("Enabled", bool, field(default=None))]
    ) = None,
    spot_price: str = None,
    iam_instance_profile: str = None,
    ebs_optimized: bool = None,
    associate_public_ip_address: bool = None,
    placement_tenancy: str = None,
    metadata_options: make_dataclass(
        "InstanceMetadataOptions",
        [
            ("HttpTokens", str, field(default=None)),
            ("HttpPutResponseHopLimit", int, field(default=None)),
            ("HttpEndpoint", str, field(default=None)),
        ],
    ) = None,
) -> Dict[str, Any]:
    """Creates an AWS Launch Configuration.

    If you exceed your maximum limit of launch configurations, the call fails. To query this limit, call the
    DescribeAccountLimits API. For information about updating this limit, see Amazon EC2 Auto Scaling service quotas in
    the Amazon EC2 Auto Scaling User Guide.

    .. Note::
        When using `aws.autoscaling.launch_configuration` with `aws.autoscaling.auto_scaling_group`, it is recommended
        to use the `name_prefix` instead of the `name` argument. This will allow Idem's `recreate_on_update` requisite
        to detect changes to the launch configuration and update the autoscaling group correctly.


    For more information, see Launch configurations in the Amazon EC2 Auto Scaling User Guide.

    Args:
        name(str):
            The name of the launch configuration. This name must be unique per Region per account.

        name_prefix(str, Optional):
            Creates a unique name beginning with the specified prefix.

            .. Note::
                Either `name` or `name_prefix` should be specified.

        resource_id(str, Optional):
            AWS Launch Configuration name.

        image_id(str, Optional):
            The ID of the Amazon Machine Image (AMI) that was assigned during registration. For more
            information, see Finding an AMI in the Amazon EC2 User Guide for Linux Instances. Defaults to None.

            If you do not specify instance_id, you must specify image_id.

        key_name(str, Optional):
            The name of the key pair. For more information, see Amazon EC2 Key Pairs in the Amazon EC2 User
            Guide for Linux Instances. Defaults to None.

        security_groups(list[str], Optional):
            A list that contains the security groups to assign to the instances in the Auto Scaling group.
            For more information, see Control traffic to resources using security groups in the Amazon Virtual Private
            Cloud User Guide. Defaults to None.

        classic_link_vpc_id(str, Optional):
            The ID of a ClassicLink-enabled VPC to link your EC2-Classic instances to. For more information,
            see ClassicLink in the Amazon EC2 User Guide for Linux Instances and Linking EC2-Classic
            instances to a VPC in the Amazon EC2 Auto Scaling User Guide. This parameter can only be used if
            you are launching EC2-Classic instances. Defaults to None.

        classic_link_vpc_security_groups(list[str], Optional):
            The IDs of one or more security groups for the specified ClassicLink-enabled VPC.
            If you specify the classic_link_vpc_id parameter, you must specify this parameter. Defaults to None.

        user_data(str, Optional):
            The user data to make available to the launched EC2 instances. For more information, see Instance metadata
            and user data (Linux) and Instance metadata and user data (Windows). If you are using a command line tool,
            base64-encoding is performed for you, and you can load the text from a file. Otherwise, you must provide
            base64-encoded text. User data is limited to 16 KB. Defaults to None.

        instance_id(str, Optional):
            The ID of the instance to use to create the launch configuration. The new launch configuration derives
            attributes from the instance, except for the block device mapping.

            To create a launch configuration with a block device mapping or override any other instance attributes,
            specify them as part of the same request.

            For more information, see Creating a launch configuration using an EC2 instance in the Amazon EC2 Auto
            Scaling User Guide.

            If you do not specify instance_id, you must specify both image_id and instance_type. Defaults to None.

        instance_type(str, Optional):
            Specifies the instance type of the EC2 instance. For information about available instance types,
            see Available Instance Types in the Amazon EC2 User Guide for Linux Instances.

            If you do not specify instance_id, you must specify instance_type. Defaults to None.

        kernel_id(str, Optional):
            The ID of the kernel associated with the AMI. Defaults to None.

        ramdisk_id(str, Optional):
            The ID of the RAM disk to select. Defaults to None.

        block_device_mappings(list[dict[str, Any]], Optional):
            A block device mapping, which specifies the block devices for the instance. You can specify
            virtual devices and EBS volumes. For more information, see Block Device Mapping in the Amazon
            EC2 User Guide for Linux Instances. Defaults to None.

            * VirtualName(str, Optional):
                The name of the virtual device (for example, ephemeral0). You can specify either VirtualName or Ebs,
                but not both.

            * DeviceName(str):
                The device name exposed to the EC2 instance (for example, /dev/sdh or xvdh). For more information, see
                Device Naming on Linux Instances in the Amazon EC2 User Guide for Linux Instances.

            * Ebs(dict[str, Any], Optional):
                Parameters used to automatically set up EBS volumes when an instance is launched. You can specify
                either VirtualName or Ebs, but not both.

                * SnapshotId(str, Optional):
                    The snapshot ID of the volume to use.
                    You must specify either a VolumeSize or a SnapshotId.

                * VolumeSize(int, Optional):
                    The volume size, in GiBs.

                    The following are the supported volumes sizes for each volume type:
                        * gp2 and gp3: 1-16,384
                        * io1: 4-16,384
                        * st1 and sc1: 125-16,384
                        * standard: 1-1,024

                    You must specify either a SnapshotId or a VolumeSize.
                    If you specify both SnapshotId and VolumeSize , the volume size must be equal or greater than the
                    size of the snapshot.

                * VolumeType(str, Optional):
                    The volume type. For more information, see Amazon EBS volume types in the Amazon EC2 User Guide for
                    Linux Instances.

                    Valid values: standard | io1 | gp2 | st1 | sc1 | gp3

                * DeleteOnTermination(bool, Optional):
                    Indicates whether the volume is deleted on instance termination. For Amazon EC2 Auto Scaling, the
                    default value is true.

                * Iops (int, Optional):
                    The number of input/output (I/O) operations per second (IOPS) to provision for the volume. For gp3
                    and io1 volumes, this represents the number of IOPS that are provisioned for the volume. For gp2
                    volumes, this represents the baseline performance of the volume and the rate at which the volume
                    accumulates I/O credits for bursting.

                    The following are the supported values for each volume type:
                        * gp3: 3,000-16,000 IOPS
                        * io1: 100-64,000 IOPS

                    For io1 volumes, we guarantee 64,000 IOPS only for Instances built on the Nitro System . Other
                    instance families guarantee performance up to 32,000 IOPS.

                    Iops is supported when the volume type is gp3 or io1 and required only when the volume type is io1.
                    (Not used with standard , gp2 , st1 , or sc1 volumes.)

                * Encrypted(bool, Optional):
                    Specifies whether the volume should be encrypted. Encrypted EBS volumes can only be attached to
                    instances that support Amazon EBS encryption. For more information, see Supported instance types.
                    If your AMI uses encrypted volumes, you can also only launch it on supported instance types.

                    .. Note::
                        If you are creating a volume from a snapshot, you cannot create an unencrypted volume from an
                        encrypted snapshot. Also, you cannot specify a KMS key ID when using a launch configuration.

                        If you enable encryption by default, the EBS volumes that you create are always encrypted,
                        either using the Amazon Web Services managed KMS key or a customer-managed KMS key, regardless
                        of whether the snapshot was encrypted.

                        For more information, see Use Amazon Web Services KMS keys to encrypt Amazon EBS volumes in the
                        Amazon EC2 Auto Scaling User Guide.

                * Throughput(int, Optional):
                    The throughput (MiBps) to provision for a gp3 volume.

            * NoDevice(bool, Optional):
                Setting this value to true suppresses the specified device included in the block device mapping of the
                AMI from being mapped to the specified device name at launch.

                If NoDevice is true for the root device, instances might fail the EC2 health check. In that case,
                Amazon EC2 Auto Scaling launches replacement instances.

                If you specify NoDevice, you cannot specify Ebs.

        instance_monitoring(dict[str, Any], Optional):
            Controls whether instances in this group are launched with detailed (true) or basic (false)
            monitoring.
            The default value is true (enabled).

            .. Warning::
                When detailed monitoring is enabled, Amazon CloudWatch generates metrics every minute and your account
                is charged a fee. When you disable detailed monitoring, CloudWatch generates metrics every 5 minutes.
                For more information, see Configure Monitoring for Auto Scaling Instances in the Amazon EC2 Auto
                Scaling User Guide.

            * Enabled(bool, Optional):
                If true, detailed monitoring is enabled. Otherwise, basic monitoring is enabled.

        spot_price(str, Optional):
            The maximum hourly price to be paid for any Spot Instance launched to fulfill the request. Spot
            Instances are launched when the price you specify exceeds the current Spot price. For more
            information, see Requesting Spot Instances in the Amazon EC2 Auto Scaling User Guide.

            Valid Range: Minimum value of 0.001

            .. Note::
                When you change your maximum price by creating a new launch configuration, running instances will
                continue to run as long as the maximum price for those running instances is higher than the current
                Spot price.

            Defaults to None.

        iam_instance_profile(str, Optional):
            The name or the Amazon Resource Name (ARN) of the instance profile associated with the IAM role for the
            instance. The instance profile contains the IAM role. For more information, see IAM role for applications
            that run on Amazon EC2 instances in the Amazon EC2 Auto Scaling User Guide. Defaults to None.

        ebs_optimized(bool, Optional):
            Specifies whether the launch configuration is optimized for EBS I/O (true) or not (false). The optimization
            provides dedicated throughput to Amazon EBS and an optimized configuration stack to provide optimal I/O
            performance. This optimization is not available with all instance types. Additional fees are incurred when
            you enable EBS optimization for an instance type that is not EBS-optimized by default. For more
            information, see Amazon EBS-optimized instances in the Amazon EC2 User Guide for Linux Instances.

            The default value is false.

        associate_public_ip_address(bool, Optional):
            Specifies whether to assign a public IPv4 address to the group's instances. If the instance is launched
            into a default subnet, the default is to assign a public IPv4 address, unless you disabled the option to
            assign a public IPv4 address on the subnet. If the instance is launched into a nondefault subnet, the
            default is not to assign a public IPv4 address, unless you enabled the option to assign a public IPv4
            address on the subnet.

            If you specify true , each instance in the Auto Scaling group receives a unique public IPv4 address. For
            more information, see Launching Auto Scaling instances in a VPC in the Amazon EC2 Auto Scaling User Guide.

            If you specify this property, you must specify at least one subnet for VPCZoneIdentifier when you create
            your group.

        placement_tenancy(str, Optional):
            The tenancy of the instance, either default or dedicated. An instance with dedicated tenancy runs on
            isolated, single-tenant hardware and can only be launched into a VPC. To launch dedicated instances into a
            shared tenancy VPC (a VPC with the instance placement tenancy attribute set to default), you must set
            the value of this parameter to dedicated. For more information, see Configuring instance tenancy with
            Amazon EC2 Auto Scaling in the Amazon EC2 Auto Scaling User Guide.

            If you specify PlacementTenancy, you must specify at least one subnet for VPCZoneIdentifier when you create
            your group.

            Valid Values: default | dedicated. Defaults to None.

        metadata_options(dict[str, Any], Optional):
            The metadata options for the instances. For more information, see Configuring the Instance
            Metadata Options in the Amazon EC2 Auto Scaling User Guide. Defaults to None.

            * HttpTokens(str, Optional):
                The state of token usage for your instance metadata requests. If the parameter is not specified in the
                request, the default state is `optional`.

                If the state is `optional`, you can choose to retrieve instance metadata with or without a signed token
                header on your request. If you retrieve the IAM role credentials without a token, the version 1.0 role
                credentials are returned. If you retrieve the IAM role credentials using a valid signed token, the
                version 2.0 role credentials are returned.

                If the state is `required`, you must send a signed token header with any instance metadata retrieval
                requests. In this state, retrieving the IAM role credentials always returns the version 2.0
                credentials; the version 1.0 credentials are not available.

            * HttpPutResponseHopLimit(int, Optional):
                The desired HTTP PUT response hop limit for instance metadata requests. The larger the number, the
                further instance metadata requests can travel.

                Default: 1

            * HttpEndpoint(str, Optional):
                This parameter enables or disables the HTTP metadata endpoint on your instances. If the parameter is
                not specified, the default state is enabled.

                .. Note::
                    If you specify a value of disabled, you will not be able to access your instance metadata.

    Request Syntax:
        .. code-block:: sls

            [launch_configuration-resource-id]:
              aws.autoscaling.launch_configuration.present:
                - name: 'string'
                - resource_id: 'string'
                - image_id: 'string'
                - key_name: 'string'
                - security_groups: List
                - classic_link_vpc_id: 'string'
                - classic_link_vpc_security_groups: List
                - user_data: 'string'
                - instance_type: 'string'
                - kernel_id: 'string'
                - ramdisk_id: 'string'
                - block_device_mappings: List
                - instance_monitoring: Dict
                - spot_price: 'string'
                - iam_instance_profile: 'string'
                - ebs_optimized: true/false
                - metadata_options: Dict
                - associate_public_ip_address: true/false

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem-test-launch_configuration:
              aws.autoscaling.launch_configuration.present:
                - name: idem-test-launch_configuration
                - resource_id: idem-test-launch_configuration
                - image_id: ami-73949613
                - key_name: test-n
                - security_groups:
                    - sg-00bbd7b8d31f6bcad
                    - sg-03064434ef6546344
                - classic_link_vpc_id: vpc-123456
                - classic_link_vpc_security_groups:
                    - sg-00bbd7b8d31f6abcd
                    - sg-03064434ef6541111
                - user_data: /etc/eks/bootstrap.sh
                - instance_type: t2.micro
                - kernel_id: aki-02b79b47
                - ramdisk_id: ari-177e2d52
                - block_device_mappings:
                    - DeviceName: /dev/sda1
                      Ebs:
                        DeleteOnTermination: false
                        Encrypted: false
                        SnapshotId: snap-0526fa8583b2ef05f
                        VolumeSize: 8
                        VolumeType: gp2
                    - DeviceName: /dev/sda
                      Ebs:
                        DeleteOnTermination: false
                        Encrypted: false
                        SnapshotId: snap-05cfe4be1b16a2e0f
                        VolumeSize: 8
                        VolumeType: gp2
                - instance_monitoring:
                    Enabled: true
                - spot_price: "0.045"
                - iam_instance_profile: arn:aws:iam::537227425989:instance-profile/aws-elasticbeanstalk-ec2-role
                - ebs_optimized: true
                - associate_public_ip_address: true
                - metadata_options:
                    HttpEndpoint: enabled
                    HttpPutResponseHopLimit: 64
                    HttpTokens: optional

    Using with AutoScaling Groups:
        Launch Configurations cannot be updated after creation with the Amazon Web Service API. In order to update a
        Launch Configuration, Idem will destroy the existing resource and create a replacement. In order to effectively
        use a Launch Configuration resource with an AutoScaling Group resource, it's recommended to specify
        `create_before_destroy` in `recreate_on_update` requisite and specify a partial name with `name_prefix`.

        Example:
            .. code-block:: sls

                idem-test-launch_configuration:
                  aws.autoscaling.launch_configuration.present:
                    - name_prefix: idem-test
                    - associate_public_ip_address: false
                    - iam_instance_profile: arn:aws:iam::537227425989:instance-profile/aws-elasticbeanstalk-ec2-role
                    - instance_type: t2.micro
                    - image_id: ami-73949613
                    - security_groups:
                      - sg-00bbd7b8d31f6bcad
                      - sg-03064434ef6546344
                    - user_data: /etc/eks/bootstrap.sh
                    - key_name: test-n
                    - block_device_mappings:
                        - DeviceName: /dev/sda
                          Ebs:
                            DeleteOnTermination: true
                            VolumeSize: 128
                            VolumeType: gp3
                            Encrypted: true
                    - ignore_changes: ["key_name"]
                    - recreate_on_update:
                        create_before_destroy: true

                idem-test-autoscaling_group:
                  aws.autoscaling.auto_scaling_group.present:
                    - name: idem-test-autoscaling_group
                    - launch_configuration_name: ${aws.autoscaling.launch_configuration:idem-test-launch_configuration:resource_id}
                    - min_size: 1
                    - max_size: 2
                    - desired_capacity: 1
                    - vpc_zone_identifier: subnet-09b9b12ccde1074ed

            With this setup Idem generates a unique name for your Launch Configuration and can then update the
            AutoScaling Group without conflict before destroying the previous Launch Configuration.

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    launch_configuration_created = False
    before = None
    desired_state = {
        "name": name,
        "resource_id": name,
        "name_prefix": name_prefix,
        "image_id": image_id,
        "key_name": key_name,
        "security_groups": security_groups,
        "classic_link_vpc_id": classic_link_vpc_id,
        "classic_link_vpc_security_groups": classic_link_vpc_security_groups,
        "user_data": user_data,
        "instance_id": instance_id,
        "instance_type": instance_type,
        "kernel_id": kernel_id,
        "ramdisk_id": ramdisk_id,
        "block_device_mappings": block_device_mappings,
        "instance_monitoring": instance_monitoring,
        "spot_price": spot_price,
        "iam_instance_profile": iam_instance_profile,
        "ebs_optimized": ebs_optimized,
        "associate_public_ip_address": associate_public_ip_address,
        "placement_tenancy": placement_tenancy,
        "metadata_options": metadata_options,
    }

    launch_conf_args = {
        "LaunchConfigurationName": name,
        "ImageId": image_id,
        "KeyName": key_name,
        "SecurityGroups": security_groups,
        "ClassicLinkVPCId": classic_link_vpc_id,
        "ClassicLinkVPCSecurityGroups": classic_link_vpc_security_groups,
        "UserData": user_data,
        "InstanceId": instance_id,
        "InstanceType": instance_type,
        "KernelId": kernel_id,
        "RamdiskId": ramdisk_id,
        "BlockDeviceMappings": block_device_mappings,
        "InstanceMonitoring": instance_monitoring,
        "SpotPrice": spot_price,
        "IamInstanceProfile": iam_instance_profile,
        "EbsOptimized": ebs_optimized,
        "AssociatePublicIpAddress": associate_public_ip_address,
        "PlacementTenancy": placement_tenancy,
        "MetadataOptions": metadata_options,
    }

    if resource_id:
        before = await hub.exec.boto3.client.autoscaling.describe_launch_configurations(
            ctx, LaunchConfigurationNames=[resource_id]
        )

    # Launch Configurations cannot be updated after creation with the Amazon Web Service API.
    if before and before["ret"].get("LaunchConfigurations"):  # resource present
        result[
            "old_state"
        ] = hub.tool.aws.autoscaling.conversion_utils.convert_raw_launch_configuration_to_present(
            raw_resource=before["ret"]["LaunchConfigurations"][0],
            idem_resource_name=name,
        )
        result["old_state"]["name_prefix"] = name_prefix
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.autoscaling.launch_configuration", name=resource_id
        )
        result["new_state"] = copy.deepcopy(result["old_state"])
        return result
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={}, desired_state=desired_state
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.autoscaling.launch_configuration", name=name
            )
            return result

        try:
            ret = await hub.exec.boto3.client.autoscaling.create_launch_configuration(
                ctx,
                **launch_conf_args,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result

            result["comment"] = hub.tool.aws.comment_utils.create_comment(
                resource_type="aws.autoscaling.launch_configuration", name=name
            )
            launch_configuration_created = True
            resource_id = name
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False

    try:
        if launch_configuration_created:
            after = (
                await hub.exec.boto3.client.autoscaling.describe_launch_configurations(
                    ctx, LaunchConfigurationNames=[resource_id]
                )
            )
            result[
                "new_state"
            ] = hub.tool.aws.autoscaling.conversion_utils.convert_raw_launch_configuration_to_present(
                raw_resource=after["ret"]["LaunchConfigurations"][0],
                idem_resource_name=name,
            )
            result["new_state"]["name_prefix"] = name_prefix
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes the specified AWS Launch Configuration.

    The launch configuration must not be attached to an Auto Scaling group.
    When this call completes, the launch configuration is no longer available for use.

    Args:
        name(str): The name of the launch configuration.
        resource_id(str, Optional): AWS launch configuration name. Idem automatically considers this resource being absent if
         this field is not specified.

    Request Syntax:
        .. code-block:: sls

            [launch_configuration-resource-id]:
              aws.autoscaling.launch_configuration.absent:
                - name: 'string'
                - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem-test-launch_configuration:
              aws.autoscaling.launch_configuration.absent:
                - name: idem-test-launch_configuration
                - resource_id: idem-test-launch_configuration
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.autoscaling.launch_configuration", name=name
        )
        return result

    before = await hub.exec.boto3.client.autoscaling.describe_launch_configurations(
        ctx, LaunchConfigurationNames=[resource_id]
    )
    if not before["result"]:
        result["result"] = False
        result["comment"] = before["comment"]
        return result
    if not before["ret"].get("LaunchConfigurations"):
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.autoscaling.launch_configuration", name=name
        )
    else:
        result[
            "old_state"
        ] = hub.tool.aws.autoscaling.conversion_utils.convert_raw_launch_configuration_to_present(
            raw_resource=before["ret"]["LaunchConfigurations"][0],
            idem_resource_name=name,
        )

        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
                resource_type="aws.autoscaling.launch_configuration", name=name
            )
            return result

        try:
            ret = await hub.exec.boto3.client.autoscaling.delete_launch_configuration(
                ctx, LaunchConfigurationName=resource_id
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.autoscaling.launch_configuration", name=name
            )
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Lists AWS Launch Configurations in the account and Region.

    Describe the resource in a way that can be recreated/managed with the corresponding "present" function.


    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.autoscaling.launch_configuration
    """
    result = {}
    ret = await hub.exec.boto3.client.autoscaling.describe_launch_configurations(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not describe launch_configuration {ret['comment']}")
        return {}

    for launch_configuration in ret["ret"].get("LaunchConfigurations"):
        resource_id = launch_configuration.get("LaunchConfigurationName")
        resource_translated = hub.tool.aws.autoscaling.conversion_utils.convert_raw_launch_configuration_to_present(
            raw_resource=launch_configuration, idem_resource_name=resource_id
        )
        result[resource_id] = {
            "aws.autoscaling.launch_configuration.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }

    return result


def pre_process_desired_state(hub, chunk):
    desired_state = copy.deepcopy(chunk)
    if desired_state.get("user_data"):
        user_data = desired_state["user_data"]
        desired_state["user_data"] = base64.b64encode(user_data.encode()).decode()

    desired_state = hub.tool.aws.autoscaling.conversion_utils.handle_security_groups(
        resource=desired_state
    )
    return desired_state
