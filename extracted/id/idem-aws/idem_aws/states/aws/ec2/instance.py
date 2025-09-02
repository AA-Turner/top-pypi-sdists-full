import datetime
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

from dict_tools.typing import Computed

__contracts__ = ["resource", "allow_sync_sls_name_and_name_tag"]
__reconcile_wait__ = {"static": {"wait_in_seconds": 5}}

TREQ = {
    "present": {
        "require": [
            "aws.ec2.network_interface.present",
            "aws.ec2.vpc.present",
            "aws.ec2.subnet.present",
            "aws.iam.role.present",
        ],
    },
}


async def present(
    hub,
    ctx,
    name: str,
    image_id: str,
    *,
    resource_id: str = None,
    # From DescribeInstances
    instance_type: str = None,
    ebs_optimized: bool = None,
    kernel_id: str = None,
    subnet_id: str = None,
    security_group_ids: List[str] = None,
    network_interfaces: List[
        make_dataclass(
            "NetworkInterfaceAttachment",
            [
                ("device_index", int),
                ("network_interface_id", str, field(default=None)),
                ("network_card_index", int, field(default=None)),
                ("subnet_id", Computed[str], field(default=None)),
                ("public_ip_address", Computed[str], field(default=None)),
                ("private_ip_address", Computed[str], field(default=None)),
                ("mac_address", Computed[str], field(default=None)),
            ],
        )
    ] = None,
    monitoring_enabled: bool = None,
    source_dest_check: bool = None,
    running: bool = True,
    private_ip_address: str = None,
    owner_id: str = None,
    # Placement Options
    availability_zone: str = None,
    affinity: str = None,
    group_name: str = None,
    partition_number: int = None,
    host_id: str = None,
    tenancy: str = None,
    spread_domain: str = None,
    host_resource_group_arn: str = None,
    # From launchTemplate
    user_data: str = None,
    disable_api_termination: bool = None,
    ram_disk_id: str = None,
    tags: Dict[str, str] = None,
    iam_instance_profile_arn: str = None,
    instance_initiated_shutdown_behavior: str = None,
    elastic_inference_accelerators: List[
        make_dataclass(
            "ElasticInferenceAccelerator",
            [("Type", str), ("Count", int, field(default=None))],
        )
    ] = None,
    elastic_gpu_specifications: List[
        make_dataclass("ElasticGpuSpecification", [("Type", str)])
    ] = None,
    auto_recovery_enabled: bool = None,
    sriov_net_support: str = None,
    key_name: str = None,
    # Enclave options
    nitro_enclave_enabled: bool = None,
    # Can only be changed on initial creation of an instance as far as we know so far
    client_token: str = None,
    product_codes: List[Dict[str, str]] = None,
    reservation_id: str = None,
    block_device_mappings: List[
        make_dataclass(
            "BlockDeviceMapping",
            [
                ("device_name", str),
                ("volume_id", str, field(default=None)),
                ("delete_on_termination", bool, field(default=False)),
                # computed volume properties
                ("size", Computed[int], field(default=None)),
                ("type", Computed[str], field(default=None)),
                ("encrypted", Computed[bool], field(default=None)),
            ],
        )
    ] = None,
    license_arns: List[str] = None,
    hibernation_enabled: bool = None,
    # Instance Market Options
    market_type: str = None,
    # Spot Options
    max_price: str = None,
    spot_instance_type: str = None,
    block_duration_minutes: int = None,
    valid_until: str = None,
    instance_interruption_behavior: str = None,
    # Credit Specification
    cpu_credits: str = None,
    cpu_core_count: int = None,
    cpu_threads_per_core: int = None,
    # Metadata options
    http_tokens: str = None,
    http_put_response_hop_limit: int = None,
    http_endpoint_enabled: bool = None,
    http_protocol_ipv6_enabled: bool = None,
    metadata_tags_enabled: bool = None,
    # Private DNS Name options
    hostname_type: str = None,
    enable_resource_name_dns_a_record: bool = None,
    enable_resource_name_dns_aaaa_record: bool = None,
    # Capacity Reservation Options
    capacity_reservation_preference: str = None,
    instance_requirements: Dict[str, Any] = None,
    # computed properties
    instance_state: Computed[str] = None,
    public_ip_address: Computed[str] = None,
    root_device_name: Computed[str] = None,
    # idem-heist options
    bootstrap: List[Dict[str, str]] = None,
    **kwargs,
) -> Dict[str, Any]:
    """Launches an instance using an AMI for which you have permissions.

    You can specify a number of options, or leave the default options.

    The following rules apply:

        - [EC2-VPC] If you don't specify a subnet ID, we choose a default subnet from your default VPC for you.
            If you don't have a default VPC, you must specify a subnet ID in the request.
        - [EC2-Classic] If don't specify an Availability Zone, we choose one for you.
            Some instance types must be launched into a VPC.
            If you do not have a default VPC, or if you do not specify a subnet ID, the request fails.
            For more information, see Instance types available only in a VPC.
        - [EC2-VPC] All instances have a network interface with a primary private IPv4 address.
            If you don't specify this address, we choose one from the IPv4 range of your subnet.
            Not all instance types support IPv6 addresses.
            For more information, see Instance types.
        - If you don't specify a security group ID, we use the default security group.
            For more information, see Security groups.
        - If any of the AMIs have a product code attached for which the user has not subscribed, the request fails.
        - You can create a launch template, which is a resource that contains the parameters to launch an instance.
            You can specify the launch template instead of specifying the launch parameters.
            An instance is ready for you to use when it's in the running state.
        - You can tag instances and EBS volumes during launch, after launch, or both.
        - Linux instances have access to the public key of the key pair at boot.
            You can use this key to provide secure access to the instance.
            Amazon EC2 public images use this feature to provide secure access without passwords.
            For more information, see Key pairs.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str):
            AWS Ec2 Instance ID.

        image_id(str):
            The ID of an AMI.

        instance_type(str, Optional):
            The instance type to use for this instance on creation.

        ebs_optimized(bool, Optional):
            Indicates whether the instance is optimized ofr Amazon EBS I/O.

        kernel_id(str, Optional):
            The kernel associated with this instance, if applicable.

        subnet_id(str, Optional):
            The ID of the subnet in which the instance is running.

        security_group_ids(List[str], Optional):
            The IDs of the security groups. If you specify a network interface, you must specify any security
            groups as part of the network interface. Default: Amazon EC2 uses the default security group.

        network_interfaces(list[dict[str, Any]], Optional):
            The network interfaces to associate with the instance. This manages the network interface attachment
            to the instance, network interfaces themselves are managed in a separate state. Defaults to None.

            * network_interface_id (str, Optional):
                The ID of the network interface. If you are creating a Spot Fleet, omit this parameter because
                you can’t specify a network interface ID in a launch specification.

            * device_index (int, Optional):
                The position of the network interface in the attachment order. A primary network interface has a
                device index of 0. If you specify a network interface when launching an instance, you must
                specify the device index.

            * network_card_index (int, Optional):
                The index of the network card. Some instance types support multiple network cards. The primary
                network interface must be assigned to network card index 0. The default is network card index 0.
                If you are using RequestSpotInstances to create Spot Instances, omit this parameter because you
                can’t specify the network card index when using this API. To specify the network card index, use
                RunInstances.

            * subnet_id (Computed[str]):
                The ID of the subnet.

            * public_ip_address (Computed[str]):
                The public IP address or Elastic IP address bound to the network interface.

            * private_ip_address (Computed[str]):
                The IPv4 address of the network interface within the subnet.

            * mac_address (Computed[str]):
                The MAC address.

        monitoring_enabled(bool, Optional):
            Indicates whether detailed monitoring is enabled.

        source_dest_check(bool, Optional):
            Indicates whether source/destination checking is enabled.

        running(bool, Optional):
            Indicates whether the instance should be in the "running" state.

        private_ip_address(str, Optional):
            The Ipv4 address of the network interface within the subnet.

        owner_id(str, Optional):
            The ID of the AWS account that owns the reservation.

        availability_zone(str, Optional):
            The Availability Zone of the instance.

        affinity(str, Optional):
            The affinity setting for the instance on the Dedicated Host.

        group_name(str, Optional):
            The affinity setting for the instance on the Dedicated Host.

        partition_number(int, Optional):
            The number of the partition that the instance is in.

        host_id(str, Optional):
            The ID of the Dedicated Host on which the instance resides.

        tenancy(str, Optional):
            The tenancy of the instance (if the instance is running in a VPC). An instance with a tenancy of dedicated runs on single-tenant hardware.

        spread_domain(str, Optional):
            Not yet documented by AWS.

        host_resource_group_arn(str, Optional):
            The ARN of the host resource group in which to launch the instances.

        user_data(str, Optional):
            The user data for the instance.

        disable_api_termination(bool, Optional):
            Indicates that an instance cannot be terminated using the Amazon Ec2 console, command line tool, or API.

        ram_disk_id(str, Optional):
            The ID of the RAM disk, if applicable.

        tags(dict, Optional, Optional):
            The tags to apply to the resource. Defaults to None.

        iam_instance_profile_arn(str, Optional):
            The IAM instance profile ARN.

        instance_initiated_shutdown_behavior(str, Optional): Indicates whether an instance stops or terminates when you initiate
            shutdown from the instance (using the operating system command for system shutdown).

        elastic_inference_accelerators(list[dict[str, Any]], Optional):
            An elastic inference accelerator to associate with the instance. Elastic inference accelerators
            are a resource you can attach to your Amazon EC2 instances to accelerate your Deep Learning (DL)
            inference workloads. You cannot specify accelerators from different generations in the same
            request. Defaults to None.

            * Type (str):
                The type of elastic inference accelerator. The possible values are eia1.medium, eia1.large,
                eia1.xlarge, eia2.medium, eia2.large, and eia2.xlarge.

            * Count (int, Optional):
                The number of elastic inference accelerators to attach to the instance.  Default: 1

        elastic_gpu_specifications(list[dict[str, Any]], Optional):
            An elastic GPU to associate with the instance. An Elastic GPU is a GPU resource that you can
            attach to your Windows instance to accelerate the graphics performance of your applications. For
            more information, see Amazon EC2 Elastic GPUs in the Amazon EC2 User Guide. Defaults to None.

            * Type (str): The type of Elastic Graphics accelerator. For more information about the values to specify for
                Type, see Elastic Graphics Basics, specifically the Elastic Graphics accelerator column, in the
                Amazon Elastic Compute Cloud User Guide for Windows Instances.

        auto_recovery_enabled(bool, Optional):
            Disables the automatic recovery behavior of your instance or sets it to default.

        sriov_net_support(str, Optional):
            Specifies whether enhanced networking with the Intel 82599 Virtual Function interface is enabled.

        key_name(str, Optional):
            The name of the keypair.

        nitro_enclave_enabled(bool, Optional):
            Indicates whether the instance is enabled for AWS Nitro Enclaves.

        client_token(str, Optional):
            The idempotency token for the instance.

        root_device_name(str, Optional):
            The device name of the root device (for example, /dev/sda1).

        product_codes(list[dict[str, str]]:
            The product codes attached to the instance, if applicable.

        reservation_id(str, Optional):
            The ID of the reservation

        block_device_mappings(list[dict[str, Any]], Optional):
            The block device mapping, which defines the EBS volumes and instance store volumes to attach to
            the instance at launch. For more information, see Block device mappings in the Amazon EC2 User
            Guide. Defaults to None.

            * device_name (str, Optional):
                The device name (for example, /dev/sdh or xvdh).

            * volume_id: (str):
                The resource_id of the volume to attach to the instance.

            * virtual_name (str, Optional):
                The virtual device name (ephemeralN). Instance store volumes are numbered starting from 0. An
                instance type with 2 available instance store volumes can specify mappings for ephemeral0 and
                ephemeral1. The number of available instance store volumes depends on the instance type. After
                you connect to the instance, you must mount the volume. NVMe instance store volumes are
                automatically enumerated and assigned a device name. Including them in your block device mapping
                has no effect. Constraints: For M3 instances, you must specify instance store volumes in the
                block device mapping for the instance. When you launch an M3 instance, we ignore any instance
                store volumes specified in the block device mapping for the AMI.

            * delete_on_termination (bool, Optional):
                Indicates whether the EBS volume is deleted on instance termination. For more information, see
                Preserving Amazon EBS volumes on instance termination in the Amazon EC2 User Guide.

        license_arns(list[str], Optional):
            The license configuration arns.

        hibernation_enabled(bool, Optional):
            Indicates whether the instance is configured for hibernation.

        market_type(str, Optional):
            The market (purchasing) option for the instance.

        max_price(str, Optional):
            The maximum hourly price you're willing to pay for the Spot Instances.

        spot_instance_type(str, Optional):
            The Spot Instance request type. Persistent Spot Instance requests are only supported when the instance
            interruption behavior is either hibernate or stop.

        block_duration_minutes(int, Optional):
            Deprecated.

        valid_until(str, Optional):
            The end date of the request, in UTC format (YYYY -MM -DD T*HH* :MM :SS Z). Supported only for persistent requests.

        instance_interruption_behavior(str, Optional):
            The behavior when a Spot Instance is interrupted. The default is terminate.

        cpu_credits(str, Optional):
            The credit option for CPU usage of a T2, T3, or T3a instance. Valid values are standard and unlimited.

        cpu_core_count(int, Optional):
            The number of CPU cores for the instance.

        cpu_threads_per_core(int, Optional):
            The number of threads per CPU core. To disable multithreading for the instance, specify a value of1 .
            Otherwise, specify the default value of 2.

        http_tokens(str, Optional):
            The state of token usage for your instance metadata requests. If the state is optional, you can
            choose to retrieve instance metadata with or without a signed token header on your request. If
            you retrieve the IAM role credentials without a token, the version 1.0 role credentials are
            returned. If you retrieve the IAM role credentials using a valid signed token, the version 2.0
            role credentials are returned. If the state is required, you must send a signed token header
            with any instance metadata retrieval requests. In this state, retrieving the IAM role
            credentials always returns the version 2.0 credentials; the version 1.0 credentials are not
            available. Default: Optional.

        http_put_response_hop_limit(int, Optional):
            The desired HTTP PUT response hop limit for instance metadata requests. The larger the number,
            the further instance metadata requests can travel. Default: 1 Possible values: Integers from 1
            to 64.

        http_endpoint_enabled(bool, Optional):
            Enables or disables the HTTP metadata endpoint on your instances. If you specify a value of
            disabled, you cannot access your instance metadata. Default: enabled.

        http_protocol_ipv6_enabled(str, Optional):
            Enables or disables the IPv6 endpoint for the instance metadata service.

        metadata_tags_enabled(bool, Optional):
            Set to enabled to allow access to instance tags from the instance metadata. Set to disabled to
            turn off access to instance tags from the instance metadata. For more information, see Work with
            instance tags using the instance metadata. Default: disabled.

        hostname_type(str, Optional):
            The type of hostname for EC2 instances.
            For IPv4 only subnets, an instance DNS name must be based on the instance IPv4 address.
            For IPv6 only subnets, an instance DNS name must be based on the instance ID.
            For dual-stack subnets, you can specify whether DNS names use the instance IPv4 address or the instance ID.

        enable_resource_name_dns_a_record(bool, Optional):
            Indicates whether to respond to DNS queries for instance hostnames with DNS A records.

        enable_resource_name_dns_aaaa_record(bool, Optional):
            Indicates whether to respond to DNS queries for instance hostnames with DNS A records.

        capacity_reservation_preference(str, Optional):
            Indicates the instance's Capacity Reservation preferences.

        instance_requirements(dict[str, Any], Optional):
            The attributes for the instance type. When you specify instance attributes, Amazon EC2 will identify
            instance types with these attributes.

        instance_state(Computed[str]):
            The reported state of the instance, possible values are:
            pending, running, shutting-down, terminated, stopping, stopped

        public_ip_address(Computed[str]):
            The public IPv4 address, or the Carrier IP address assigned to the instance, if applicable.
            A Carrier IP address only applies to an instance launched in a subnet associated with a Wavelength Zone.

        bootstrap(list[dict[str, Any]], Optional):
            Bootstr options for provisioning an instance with "heist".

    Request Syntax:
       .. code-block:: sls

          [instance-resource-id]:
            aws.ec2.instance.present:
              - name: "string"
              - image_id: "string"
              - tags:
                  - Key: "string"
                    Value: "string"
              - bootstrap:
                    - heist_manager: "string"
                      artifact_version: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            default_vpc:
              exec.run:
                - path: aws.ec2.vpc.get
                - kwargs:
                    default: "true"

            default_subnet:
              exec.run:
                - path: aws.ec2.subnet.get
                - kwargs:
                    filters:
                      - name: vpc-id
                        values:
                          - ${exec:default_vpc:resource_id}

            small_image:
              exec.run:
                - path: aws.ec2.ami.get
                - kwargs:
                    owners:
                      - amazon
                    most_recent: True
                    filters:
                      - name: image-type
                        values:
                          - machine
                      - name: state
                        values:
                          - available
                      - name: hypervisor
                        values:
                          - xen
                      - name: architecture
                        values:
                          - x86_64
                      - name: root-device-type
                        values:
                          - ebs
                      - name: virtualization-type
                        values:
                          - hvm

            small_instance_type:
              exec.run:
                - path: aws.ec2.instance_type.get
                - kwargs:
                    filters:
                      - name: instance-type
                        values:
                          - '*.nano'
                      - name: hypervisor
                        values:
                          - xen
                      - name: processor-info.supported-architecture
                        values:
                          - x86_64

            my_network_interface:
              aws.ec2.network_interface.present:
                - subnet_id: ${exec:default_subnet:resource_id}

            create_instance:
              aws.ec2.instance.present:
                - image_id: ${exec:small_image:resource_id}
                - instance_type: ${exec:small_instance_type:resource_id}
                - client_token: optional-idempotence-token
                - network_interfaces:
                  - network_interface_id: ${aws.ec2.network_interface:my_network_interface:resource_id}
                    device_index: 0
                    network_card_index: 0
                - tags:
                    Name: test-idem-cloud-demo
                - bootstrap:
                  - heist_manager: salt.minion
    """
    # Convert a list of dictionaries to a plain dictionary before calculating desired_state
    if isinstance(tags, list):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    # Due to a bug, the default value populated to ESM is {}, for idem-aws versions <= 3.0.0
    if iam_instance_profile_arn == {}:
        iam_instance_profile_arn = None

    # Get all the parameters passed to this function as a single dictionary
    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "kwargs") and v is not None
    }

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    current_state = None
    if resource_id:
        get = await hub.exec.aws.ec2.instance.get(
            ctx, name=name, resource_id=resource_id
        )
        current_state = result["old_state"] = get.ret

        if not result["old_state"]:
            result["comment"] += [
                f"Could not find instance for '{name}' with existing id '{resource_id}'"
            ]
            return result

        result["comment"] += [f"Instance '{name}' already exists"]
    elif client_token:
        get = await hub.exec.aws.ec2.instance.get(
            ctx, name=name, filters=[{"Name": "client-token", "Values": [client_token]}]
        )

        if get.result is True:
            if get.ret is None:
                result["comment"] += [
                    f"Could not find Instance for '{name}' with existing idempotence token '{client_token}'"
                ]
            else:
                current_state = result["old_state"] = get.ret
                resource_id = current_state.resource_id
                result["comment"] += [f"Instance '{name}' already exists"]

    if not resource_id:
        if ctx.test:
            result["new_state"] = hub.tool.aws.ec2.instance.state.test(**desired_state)
            result["comment"] += [f"Would create aws.ec2.instance '{name}'"]
            return result

        # Prepare options that are grouped in the request

        # Prepare instance market options
        spot_options = {}
        if max_price:
            spot_options["MaxPrice"] = max_price
        if spot_instance_type:
            spot_options["SpotInstanceType"] = spot_instance_type
        if block_duration_minutes:
            spot_options["BlockDurationMinutes"] = block_duration_minutes
        if valid_until:
            spot_options["ValidUntil"] = datetime.datetime(valid_until)
        if instance_initiated_shutdown_behavior:
            spot_options[
                "InstanceInterruptionBehavior"
            ] = instance_interruption_behavior
        if market_type:
            instance_market_options = {
                "MarketType": market_type,
                "SpotOptions": spot_options,
            }
        elif spot_options:
            instance_market_options = {"SpotOptions": spot_options}
        else:
            instance_market_options = None

        # Prepare Metadata options
        metadata_options = {}
        if http_tokens:
            metadata_options["HttpTokens"] = http_tokens
        if http_put_response_hop_limit:
            metadata_options["HttpPutResponseHopLimit"] = http_put_response_hop_limit
        if http_endpoint_enabled is not None:
            metadata_options["HttpEndpoint"] = (
                "enabled" if http_endpoint_enabled else "disabled"
            )
        if http_protocol_ipv6_enabled is not None:
            metadata_options["HttpProtocolIpv6"] = (
                "enabled" if http_protocol_ipv6_enabled else "disabled"
            )
        if metadata_tags_enabled is not None:
            metadata_options["InstanceMetadataTags"] = (
                "enabled" if metadata_tags_enabled else "disabled"
            )

        # Prepare Private DNS Name Options
        private_dns_name_options = {}
        if hostname_type:
            private_dns_name_options["HostnameType"] = hostname_type
        if enable_resource_name_dns_a_record is not None:
            private_dns_name_options[
                "EnableResourceNameDnsARecord"
            ] = enable_resource_name_dns_a_record
        if enable_resource_name_dns_aaaa_record is not None:
            private_dns_name_options[
                "EnableResourceNameDnsAAAARecord"
            ] = enable_resource_name_dns_aaaa_record

        # Prepare Cpu Options
        cpu_options = {}
        if cpu_core_count:
            cpu_options["CoreCount"] = cpu_core_count
        if cpu_threads_per_core:
            cpu_options["ThreadsPerCore"] = cpu_threads_per_core

        # Prepare Placement Options
        placement = {}
        if availability_zone:
            placement["AvailabilityZone"] = availability_zone
        if affinity:
            placement["Affinity"] = affinity
        if group_name:
            placement["GroupName"] = group_name
        if partition_number:
            placement["PartitionNumber"] = partition_number
        if host_id:
            placement["HostId"] = host_id
        if tenancy:
            placement["Tenancy"] = tenancy
        if spread_domain:
            placement["SpreadDomain"] = spread_domain
        if host_resource_group_arn:
            placement["HostResourceGroupArn"] = host_resource_group_arn

        # Prepare TagSpecifications
        if tags:
            tag_specifications = [
                {
                    "ResourceType": "instance",
                    "Tags": [{"Key": k, "Value": v} for k, v in tags.items()],
                }
            ]
        else:
            tag_specifications = None

        # Prepare Maintenance Options
        maintenance_options = {}
        if auto_recovery_enabled is not None:
            maintenance_options["AutoRecovery"] = (
                "disabled" if auto_recovery_enabled is False else "default"
            )

        # Prepare Hibernation Options
        hibernation_options = {}
        if hibernation_enabled is not None:
            hibernation_options["Configured"] = hibernation_enabled

        # Prepare Credit Specifications
        credit_specifications = {}
        if cpu_credits is not None:
            credit_specifications["CpuCredits"] = cpu_credits

        # Prepare Enclave Options
        enclave_options = {}
        if nitro_enclave_enabled:
            enclave_options["Enabled"] = nitro_enclave_enabled

        # Prepare Monitoring Options
        monitoring_options = {}
        if monitoring_enabled:
            monitoring_options["Enabled"] = monitoring_enabled

        # Prepare Capacity Reservation Specification
        capacity_reservation_specification = {}
        if capacity_reservation_preference:
            capacity_reservation_specification[
                "CapacityReservationPreference"
            ] = capacity_reservation_preference

        network_interface_attachment_specification = []
        if subnet_id:
            # Subnet id and network interfaces cannot be specified together
            # The network interfaces will be handled in the update process
            network_interface_attachment_specification = None
        elif network_interfaces:
            for network_interface_attachment in network_interfaces:
                network_interface_attachment_specification.append(
                    {
                        "NetworkInterfaceId": network_interface_attachment.get(
                            "network_interface_id"
                        ),
                        "DeviceIndex": network_interface_attachment.get("device_index"),
                        "NetworkCardIndex": network_interface_attachment.get(
                            "network_card_index"
                        ),
                    }
                )

        new_block_device_mappings = None
        if block_device_mappings:
            new_block_device_mappings = list()
            for bd in block_device_mappings:
                device_name = bd.get("device_name")
                if not device_name:
                    continue
                # Create an empty mapping while the instance is starting -- it will be connected on update
                new_bd = dict(DeviceName=device_name, NoDevice="")
                if bd.get("virtual_name"):
                    new_bd["VirtualName"] = bd["virtual_name"]
                new_block_device_mappings.append(new_bd)

        # Create a brand new instance with minimal arguments, it will be updated after creation
        create_ret = await hub.exec.boto3.client.ec2.run_instances(
            ctx,
            ClientToken=client_token,
            MaxCount=1,
            MinCount=1,
            ImageId=image_id,
            InstanceType=instance_type,
            EbsOptimized=ebs_optimized,
            BlockDeviceMappings=new_block_device_mappings,
            KernelId=kernel_id,
            Placement=placement or None,
            SubnetId=subnet_id,
            NetworkInterfaces=network_interface_attachment_specification,
            Monitoring=monitoring_options or None,
            PrivateIpAddress=private_ip_address,
            UserData=user_data,
            DisableApiTermination=disable_api_termination,
            InstanceInitiatedShutdownBehavior=instance_initiated_shutdown_behavior,
            EnclaveOptions=enclave_options or None,
            RamDiskId=ram_disk_id,
            TagSpecifications=tag_specifications,
            ElasticGpuSpecification=elastic_gpu_specifications,
            ElasticInferenceAccelerators=elastic_inference_accelerators,
            IamInstanceProfile={"Arn": iam_instance_profile_arn}
            if iam_instance_profile_arn
            else None,
            KeyName=key_name,
            InstanceMarketOptions=instance_market_options,
            CreditSpecification=credit_specifications or None,
            CpuOptions=cpu_options or None,
            CapacityReservationSpecification=capacity_reservation_specification or None,
            LicenseSpecifications=[
                {"LicenseConfigurationArn": license_arn}
                for license_arn in license_arns or []
            ],
            HibernationOptions=hibernation_options or None,
            MetadataOptions=metadata_options or None,
            PrivateDnsNameOptions=private_dns_name_options or None,
            MaintenanceOptions=maintenance_options or None,
            SecurityGroupIds=security_group_ids,
        )

        result["result"] &= create_ret.result
        if not create_ret:
            result["comment"] += [create_ret.comment]
            return result

        result["comment"] += [f"Created '{name}'"]
        resource_id = create_ret.ret["Instances"][0]["InstanceId"]
        # This makes sure the created Instance is saved to esm regardless if the subsequent update call fails or not.
        result["new_state"] = dict(name=name, resource_id=resource_id)
        result["force_save"] = True

        present_ret = (
            await hub.tool.aws.ec2.instance.state.convert_instance_to_present_async(
                ctx, {"Reservations": [create_ret.ret]}, name=name
            )
        )
        current_state = present_ret[resource_id]

    if not current_state:
        result["comment"] += [
            f"Unable to get the current_state, instance may still be undergoing creation: '{name}'"
        ]
        result["result"] = False
        return result

    # Modify all the attributes that need modification
    if ctx.test:
        result["new_state"] = hub.tool.aws.ec2.instance.state.test(**desired_state)
        return result

    resource = await hub.tool.boto3.resource.create(
        ctx, "ec2", "Instance", id=resource_id
    )

    # TODO: Remove waiters across the board in this flow
    if resource.state["Name"] == "pending":
        await hub.tool.boto3.resource.exec(resource, "wait_until_running")
    elif resource.state["Name"] == "stopping":
        await hub.tool.boto3.resource.exec(resource, "wait_until_stopped")

    try:
        result["result"] &= await hub.tool.aws.ec2.instance.update.init.apply(
            ctx,
            resource,
            old_value=current_state,
            new_value=desired_state,
            comments=result["comment"],
        )
    except Exception as apply_config_error:
        err_msg = f"Failed to apply configuration on the resource {resource_id}: {apply_config_error.__class__.__name__}"
        hub.log.error(err_msg)
        result["comment"].append(err_msg)
        result["result"] = False

    get = await hub.exec.aws.ec2.instance.get(ctx, resource_id=resource_id, name=name)
    if get.result:
        current_state = get.ret
    result["new_state"] = current_state

    if running:
        # If running is set to True then it goes to reconciler and makes sure current state is running
        hub.log.debug(f"Waiting for instance '{resource_id}' to be running")
        result["rerun_data"] = dict(target_instance_state="running")
    else:
        hub.log.debug(f"Waiting for instance '{resource_id}' to be stopped")
        result["rerun_data"] = dict(target_instance_state="stopped")

    return result


async def absent(
    hub, ctx, name: str, resource_id: str = None, client_token: str = None, **kwargs
) -> Dict[str, Any]:
    """Shuts down the specified instance.

    Terminated instances remain visible after termination (for approximately one hour).

    Args:
        name(str): The name of the state.
        resource_id(str): An instance id.
        client_token(str): An idempotence token that was used with the instance creation

    Request Syntax:
        .. code-block:: sls

            [instance-resource-id]:
              aws.ec2.instance.absent:
                - name: "string"
                - resource_id: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.ec2.instance.absent:
                - name: value
    """
    result = dict(
        comment=[],
        old_state=ctx.old_state,
        new_state=None,
        name=name,
        result=True,
        rerun_data=dict(target_instance_state="terminated"),
    )

    # Get the resource_id from ESM
    if not resource_id:
        resource_id = (ctx.old_state or {}).get("resource_id")

    if not resource_id and client_token:
        get = await hub.exec.aws.ec2.instance.get(
            ctx, name=name, filters=[{"Name": "client-token", "Values": [client_token]}]
        )
        resource_id = get.ret.resource_id

    # If there still is no resource_id, the instance is gone
    if not resource_id:
        result["comment"] += [f"'{name}' already terminated"]
        return result

    if ctx.test:
        result["comment"] += [f"Would terminate aws.ec2.instance '{name}'"]
        return result

    get = await hub.exec.aws.ec2.instance.get(ctx, name=name, resource_id=resource_id)
    if get.get("ret") is not None:
        result["old_state"] = get["ret"]
        current_status = result["old_state"].get("instance_state")
        if current_status == "terminated":
            result["comment"] += [
                f"Terminated instance '{name}', it will still be visible for about 60 minutes"
            ]
            return result

    ret = await hub.exec.boto3.client.ec2.terminate_instances(
        ctx, InstanceIds=[resource_id]
    )

    if ret.comment:
        result["comment"].append(ret.comment)

    if not ret.result and any("does not exist" in c for c in ret.comment):
        # The command failed because the instance no longer exists
        return result
    elif not ret.result:
        # The failure is some other reason we need to examine
        result["result"] &= ret.result
    else:
        get = await hub.exec.aws.ec2.instance.get(
            ctx, resource_id=resource_id, name=name
        )
        result["new_state"] = get.ret
        result["comment"] += [
            f"Terminated instance '{name}', it will still be visible for about 60 minutes"
        ]

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.ec2.instance
    """
    result = {}
    ret = await hub.exec.boto3.client.ec2.describe_instances(ctx)

    if not ret:
        hub.log.warning(f"Could not describe Instances: {ret.comment}")
        return {}

    instances = await hub.tool.aws.ec2.instance.state.convert_instance_to_present_async(
        ctx, ret.ret
    )

    for instance_id, present_state in instances.items():
        result[instance_id] = {
            "aws.ec2.instance.present": [{k: v} for k, v in present_state.items()]
        }

    return result


def is_pending(hub, ret):
    new_state = ret.get("new_state", None)
    rerun_data = ret.get("rerun_data", None)
    if new_state and rerun_data:
        current_status = new_state.get("instance_state")
        resource_id = new_state.get("resource_id")
        if current_status and isinstance(current_status, str):
            if current_status.casefold() == rerun_data.get("target_instance_state"):
                hub.log.debug(
                    f"No need to reconcile new state for instance '{resource_id}' with current status {current_status}"
                )
                # Cleanup new_state to make sure instance is removed from ESM
                if (
                    rerun_data.get("target_instance_state") == "terminated"
                    and ret["new_state"]
                ):
                    return True
                return False
            else:
                hub.log.debug(
                    f"Reconcile new state for instance '{resource_id}' with current status {current_status}"
                )
                return True
    if (
        not new_state
        and rerun_data
        and rerun_data.get("target_instance_state") == "terminated"
    ):
        # No need to reconcile terminated state
        return False

    return (not ret["result"]) or bool(ret["changes"])
