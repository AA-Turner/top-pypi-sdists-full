"""State module for managing AWS Auto Scaling groups."""
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
    min_size: int,
    max_size: int,
    resource_id: str = None,
    launch_configuration_name: str = None,
    launch_template: make_dataclass(
        "LaunchTemplateSpecification",
        [
            ("LaunchTemplateId", str, field(default=None)),
            ("LaunchTemplateName", str, field(default=None)),
            ("Version", str, field(default=None)),
        ],
    ) = None,
    mixed_instances_policy: make_dataclass(
        "MixedInstancesPolicy",
        [
            (
                "LaunchTemplate",
                make_dataclass(
                    "LaunchTemplate",
                    [
                        (
                            "LaunchTemplateSpecification",
                            make_dataclass(
                                "LaunchTemplateSpecification",
                                [
                                    ("LaunchTemplateId", str, field(default=None)),
                                    ("LaunchTemplateName", str, field(default=None)),
                                    ("Version", str, field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                        (
                            "Overrides",
                            List[
                                make_dataclass(
                                    "LaunchTemplateOverrides",
                                    [
                                        ("InstanceType", str, field(default=None)),
                                        ("WeightedCapacity", str, field(default=None)),
                                        (
                                            "LaunchTemplateSpecification",
                                            make_dataclass(
                                                "LaunchTemplateSpecification",
                                                [
                                                    (
                                                        "LaunchTemplateId",
                                                        str,
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "LaunchTemplateName",
                                                        str,
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "Version",
                                                        str,
                                                        field(default=None),
                                                    ),
                                                ],
                                            ),
                                            field(default=None),
                                        ),
                                        (
                                            "InstanceRequirements",
                                            make_dataclass(
                                                "InstanceRequirements",
                                                [
                                                    (
                                                        "VCpuCount",
                                                        make_dataclass(
                                                            "VCpuCountRequest",
                                                            [
                                                                ("Min", int),
                                                                (
                                                                    "Max",
                                                                    int,
                                                                    field(default=None),
                                                                ),
                                                            ],
                                                        ),
                                                    ),
                                                    (
                                                        "MemoryMiB",
                                                        make_dataclass(
                                                            "MemoryMiBRequest",
                                                            [
                                                                ("Min", int),
                                                                (
                                                                    "Max",
                                                                    int,
                                                                    field(default=None),
                                                                ),
                                                            ],
                                                        ),
                                                    ),
                                                    (
                                                        "CpuManufacturers",
                                                        List[str],
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "MemoryGiBPerVCpu",
                                                        make_dataclass(
                                                            "MemoryGiBPerVCpuRequest",
                                                            [
                                                                (
                                                                    "Min",
                                                                    float,
                                                                    field(default=None),
                                                                ),
                                                                (
                                                                    "Max",
                                                                    float,
                                                                    field(default=None),
                                                                ),
                                                            ],
                                                        ),
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "ExcludedInstanceTypes",
                                                        List[str],
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "InstanceGenerations",
                                                        List[str],
                                                        field(default=None),
                                                    ),
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
                                                    (
                                                        "BareMetal",
                                                        str,
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "BurstablePerformance",
                                                        str,
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "RequireHibernateSupport",
                                                        bool,
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "NetworkInterfaceCount",
                                                        make_dataclass(
                                                            "NetworkInterfaceCountRequest",
                                                            [
                                                                (
                                                                    "Min",
                                                                    int,
                                                                    field(default=None),
                                                                ),
                                                                (
                                                                    "Max",
                                                                    int,
                                                                    field(default=None),
                                                                ),
                                                            ],
                                                        ),
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "LocalStorage",
                                                        str,
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "LocalStorageTypes",
                                                        List[str],
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "TotalLocalStorageGB",
                                                        make_dataclass(
                                                            "TotalLocalStorageGBRequest",
                                                            [
                                                                (
                                                                    "Min",
                                                                    float,
                                                                    field(default=None),
                                                                ),
                                                                (
                                                                    "Max",
                                                                    float,
                                                                    field(default=None),
                                                                ),
                                                            ],
                                                        ),
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "BaselineEbsBandwidthMbps",
                                                        make_dataclass(
                                                            "BaselineEbsBandwidthMbpsRequest",
                                                            [
                                                                (
                                                                    "Min",
                                                                    int,
                                                                    field(default=None),
                                                                ),
                                                                (
                                                                    "Max",
                                                                    int,
                                                                    field(default=None),
                                                                ),
                                                            ],
                                                        ),
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "AcceleratorTypes",
                                                        List[str],
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "AcceleratorCount",
                                                        make_dataclass(
                                                            "AcceleratorCountRequest",
                                                            [
                                                                (
                                                                    "Min",
                                                                    int,
                                                                    field(default=None),
                                                                ),
                                                                (
                                                                    "Max",
                                                                    int,
                                                                    field(default=None),
                                                                ),
                                                            ],
                                                        ),
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "AcceleratorManufacturers",
                                                        List[str],
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "AcceleratorNames",
                                                        List[str],
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "AcceleratorTotalMemoryMiB",
                                                        make_dataclass(
                                                            "AcceleratorTotalMemoryMiBRequest",
                                                            [
                                                                (
                                                                    "Min",
                                                                    int,
                                                                    field(default=None),
                                                                ),
                                                                (
                                                                    "Max",
                                                                    int,
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
                                    ],
                                )
                            ],
                            field(default=None),
                        ),
                    ],
                ),
                field(default=None),
            ),
            (
                "InstancesDistribution",
                make_dataclass(
                    "InstancesDistribution",
                    [
                        ("OnDemandAllocationStrategy", str, field(default=None)),
                        ("OnDemandBaseCapacity", int, field(default=None)),
                        (
                            "OnDemandPercentageAboveBaseCapacity",
                            int,
                            field(default=None),
                        ),
                        ("SpotAllocationStrategy", str, field(default=None)),
                        ("SpotInstancePools", int, field(default=None)),
                        ("SpotMaxPrice", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    instance_id: str = None,
    desired_capacity: int = None,
    default_cooldown: int = None,
    availability_zones: List[str] = None,
    load_balancer_names: List[str] = None,
    target_group_ar_ns: List[str] = None,
    health_check_type: str = None,
    health_check_grace_period: int = None,
    placement_group: str = None,
    vpc_zone_identifier: str = None,
    termination_policies: List[str] = None,
    new_instances_protected_from_scale_in: bool = None,
    capacity_rebalance: bool = None,
    lifecycle_hook_specification_list: List[
        make_dataclass(
            "LifecycleHookSpecification",
            [
                ("LifecycleHookName", str, field(default=None)),
                ("LifecycleTransition", str, field(default=None)),
                ("NotificationMetadata", str, field(default=None)),
                ("HeartbeatTimeout", int, field(default=None)),
                ("DefaultResult", str, field(default=None)),
                ("NotificationTargetARN", str, field(default=None)),
                ("RoleARN", str, field(default=None)),
            ],
        )
    ] = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass(
            "Tag",
            [
                ("key", str, field(default=None)),
                ("value", str, field(default=None)),
                ("propagate_at_launch", bool, field(default=None)),
            ],
        )
    ] = None,
    service_linked_role_arn: str = None,
    max_instance_lifetime: int = None,
    desired_capacity_type: str = None,
) -> Dict[str, Any]:
    """Creates an Auto Scaling group with the specified name and attributes.

    We strongly recommend using a launch template when calling this operation to ensure full functionality for Amazon
    EC2 Auto Scaling and Amazon EC2.

    If you exceed your maximum limit of Auto Scaling groups, the call fails. To query this limit, call the
    DescribeAccountLimits API. For information about updating this limit, see Amazon EC2 Auto Scaling service quotas in
    the Amazon EC2 Auto Scaling User Guide.

    For introductory exercises for creating an Auto Scaling group, see Getting started with Amazon EC2 Auto Scaling and
    Tutorial: Set up a scaled and load-balanced application in the Amazon EC2 Auto Scaling User Guide.

    For more information, see Auto Scaling groups in the Amazon EC2 Auto Scaling User Guide. Every Auto Scaling group
    has three size parameters (`DesiredCapacity`, `MaxSize`, and `MinSize`). Usually, you set these sizes based on a
    specific number of instances. However, if you configure a mixed instances policy that defines weights for the
    instance types, you must specify these sizes with the same units that you use for weighting instances.

    Args:
        resource_id(str, Optional):
            The name of the Auto Scaling group. This name must be unique per Region per account.

        name(str):
            An Idem name of the resource. This is also used as the AutoScaling Group Name during resource creation.

        launch_configuration_name(str, Optional):
            The name of the launch configuration to use to launch instances.

            Conditional: You must specify either a launch template (launch_template or mixed_instances_policy) or a
            launch configuration (launch_configuration_name or instance_id).

            Defaults to None.

        launch_template(dict[str, Any], Optional):
            Information used to specify the launch template and version to use to launch instances.

            Conditional: You must specify either a launch template (launch_template or mixed_instances_policy) or a
            launch configuration (launch_configuration_name or instance_id).

            .. Note::
                The launch template that is specified must be configured for use with an Auto Scaling group. For more
                information, see Creating a launch template for an Auto Scaling group in the Amazon EC2 Auto Scaling
                User Guide.

            Defaults to None.

            * LaunchTemplateId (str, Optional):
                The ID of the launch template. To get the template ID, use the Amazon EC2
                DescribeLaunchTemplates API operation. New launch templates can be created using the Amazon EC2
                CreateLaunchTemplate API.

                Conditional: You must specify either a LaunchTemplateId or a LaunchTemplateName.

            * LaunchTemplateName (str, Optional):
                The name of the launch template. To get the template name, use the Amazon EC2 DescribeLaunchTemplates
                API operation. New launch templates can be created using the Amazon EC2 CreateLaunchTemplate API.

                Conditional: You must specify either a LaunchTemplateId or a LaunchTemplateName.

            * Version (str, Optional):
                The version number, `$Latest`, or `$Default`. To get the version number, use the Amazon EC2
                DescribeLaunchTemplateVersions API operation. New launch template versions can be created using
                the Amazon EC2 CreateLaunchTemplateVersion API. If the value is `$Latest`, Amazon EC2 Auto Scaling
                selects the latest version of the launch template when launching instances. If the value is
                `$Default`, Amazon EC2 Auto Scaling selects the default version of the launch template when
                launching instances. The default value is `$Default`.

        mixed_instances_policy(dict[str, Any], Optional):
            An embedded object that specifies a mixed instances policy.

            For more information, see Auto Scaling groups with multiple instance types and purchase options in the
            Amazon EC2 Auto Scaling User Guide.

            Defaults to None.

            * LaunchTemplate (dict[str, Any], Optional):
                Specifies the launch template to use and the instance types (overrides) that are used to launch EC2
                instances to fulfill On-Demand and Spot capacities.

                Required when creating a mixed instances policy.

                * LaunchTemplateSpecification (dict[str, Any], Optional):
                    The launch template to use.

                    * LaunchTemplateId (str, Optional):
                        The ID of the launch template. To get the template ID, use the Amazon EC2
                        DescribeLaunchTemplates API operation. New launch templates can be created using the Amazon EC2
                        CreateLaunchTemplate API.

                        Conditional: You must specify either a LaunchTemplateId or a LaunchTemplateName.

                    * LaunchTemplateName (str, Optional):
                        The name of the launch template. To get the template name, use the Amazon EC2
                        DescribeLaunchTemplates API operation. New launch templates can be created using the Amazon EC2
                        CreateLaunchTemplate API.

                        Conditional: You must specify either a LaunchTemplateId or a LaunchTemplateName.

                    * Version (str, Optional):
                        The version number, `$Latest`, or `$Default`. To get the version number, use the Amazon EC2
                        DescribeLaunchTemplateVersions API operation. New launch template versions can be created using
                        the Amazon EC2 CreateLaunchTemplateVersion API. If the value is `$Latest`, Amazon EC2 Auto
                        Scaling selects the latest version of the launch template when launching instances. If the
                        value is `$Default`, Amazon EC2 Auto Scaling selects the default version of the launch template
                        when launching instances. The default value is `$Default`.

                * Overrides (list[dict[str, Any]], Optional):
                    Any properties that you specify override the same properties in the launch template. If not
                    provided, Amazon EC2 Auto Scaling uses the instance type or instance type requirements specified
                    in the launch template when it launches an instance.

                    The overrides can include either one or more instance types or a set of instance requirements, but
                    not both.

                    * InstanceType (str, Optional):
                        The instance type, such as m3.xlarge. You must use an instance type that is supported in your
                        requested Region and Availability Zones. For more information, see Instance types in the Amazon
                        Elastic Compute Cloud User Guide.

                    * WeightedCapacity (str, Optional):
                        The number of capacity units provided by the instance type specified in InstanceType in terms of
                        virtual CPUs, memory, storage, throughput, or other relative performance characteristic. When a
                        Spot or On-Demand Instance is launched, the capacity units count toward the desired capacity.
                        Amazon EC2 Auto Scaling launches instances until the desired capacity is totally fulfilled, even
                        if this results in an overage. For example, if there are two units remaining to fulfill
                        capacity, and Amazon EC2 Auto Scaling can only launch an instance with a WeightedCapacity of
                        five units, the instance is launched, and the desired capacity is exceeded by three units. For
                        more information, see Configuring instance weighting for Amazon EC2 Auto Scaling in the Amazon
                        EC2 Auto Scaling User Guide. Value must be in the range of 1–999.

                    * LaunchTemplateSpecification (dict[str, Any], Optional):
                        Provides a launch template for the specified instance type or instance requirements. For
                        example, some instance types might require a launch template with a different AMI. If not
                        provided, Amazon EC2 Auto Scaling uses the launch template that's defined for your mixed
                        instances policy. For more information, see Specifying a different launch template for an
                        instance type in the Amazon EC2 Auto Scaling User Guide.

                        * LaunchTemplateId (str, Optional):
                            The ID of the launch template. To get the template ID, use the Amazon EC2
                            DescribeLaunchTemplates API operation. New launch templates can be created using the Amazon
                            EC2 CreateLaunchTemplate API.

                            Conditional: You must specify either a LaunchTemplateId or a LaunchTemplateName.

                        * LaunchTemplateName (str, Optional):
                            The name of the launch template. To get the template name, use the Amazon EC2
                            DescribeLaunchTemplates API operation. New launch templates can be created using the Amazon
                            EC2 CreateLaunchTemplate API.

                            Conditional: You must specify either a LaunchTemplateId or a LaunchTemplateName.

                        * Version (str, Optional):
                            The version number, `$Latest`, or `$Default`. To get the version number, use the Amazon EC2
                            DescribeLaunchTemplateVersions API operation. New launch template versions can be created
                            using the Amazon EC2 CreateLaunchTemplateVersion API. If the value is `$Latest`, Amazon EC2
                            Auto Scaling selects the latest version of the launch template when launching instances. If
                            the value is `$Default`, Amazon EC2 Auto Scaling selects the default version of the launch
                            template when launching instances. The default value is `$Default`.

                    * InstanceRequirements (dict[str, Any], Optional):
                        The instance requirements. When you specify instance requirements, Amazon EC2 Auto Scaling finds
                        instance types that satisfy your requirements, and then uses your On-Demand and Spot allocation
                        strategies to launch instances from these instance types, in the same way as when you specify a
                        list of specific instance types.

                        * VCpuCount (dict[str, Any]):
                            The minimum and maximum number of vCPUs for an instance type.

                            * Min (int): The minimum number of vCPUs.
                            * Max (int, Optional): The maximum number of vCPUs.

                        * MemoryMiB (dict[str, Any]):
                            The minimum and maximum instance memory size for an instance type, in MiB.

                            * Min (int): The memory minimum in MiB.
                            * Max (int, Optional): The memory maximum in MiB.

                        * CpuManufacturers (list[str], Optional):
                            Lists which specific CPU manufacturers to include.

                            * For instance types with Intel CPUs, specify intel.
                            * For instance types with AMD CPUs, specify amd.
                            * For instance types with Amazon Web Services CPUs, specify amazon-web-services.

                            .. Note::
                                Don't confuse the CPU hardware manufacturer with the CPU hardware architecture.
                                Instances will be launched with a compatible CPU architecture based on the Amazon
                                Machine Image (AMI) that you specify in your launch template.

                            Default: Any manufacturer

                        * MemoryGiBPerVCpu (dict[str, Any], Optional):
                            The minimum and maximum amount of memory per vCPU for an instance type, in GiB.

                            Default: No minimum or maximum

                            * Min (float, Optional): The memory minimum in GiB.
                            * Max (float, Optional): The memory maximum in GiB.

                        * ExcludedInstanceTypes (list[str], Optional):
                            Lists which instance types to exclude. You can use strings with one or more wild cards,
                            represented by an asterisk (*). The following are examples: c5*, m5a.*, r*, *3*.

                            For example, if you specify c5*, you are excluding the entire C5 instance family, which
                            includes all C5a and C5n instance types. If you specify m5a.*, you are excluding all the
                            M5a instance types, but not the M5n instance types.

                            Default: No excluded instance types

                        * InstanceGenerations (list[str], Optional):
                            Indicates whether current or previous generation instance types are included.

                            * For current generation instance types, specify current.
                            The current generation includes EC2 instance types currently recommended for use. This
                            typically includes the latest two to three generations in each instance family.
                            For more information, see Instance types in the Amazon EC2 User Guide for Linux Instances.

                            * For previous generation instance types, specify previous.

                            Default: Any current or previous generation

                        * SpotMaxPricePercentageOverLowestPrice (int, Optional):
                            The price protection threshold for Spot Instances. This is the maximum you’ll pay for a Spot
                            Instance, expressed as a percentage higher than the cheapest M, C, or R instance type with
                            your specified attributes. When Amazon EC2 Auto Scaling selects instance types with your
                            attributes, we will exclude instance types whose price is higher than your threshold. The
                            parameter accepts an integer, which Amazon EC2 Auto Scaling interprets as a percentage. To
                            turn off price protection, specify a high value, such as 999999.

                            If you set DesiredCapacityType to vcpu or memory-mib, the price protection threshold is
                            applied based on the per vCPU or per memory price instead of the per instance price.

                            Default: 100

                        * OnDemandMaxPricePercentageOverLowestPrice (int, Optional):
                            The price protection threshold for On-Demand Instances. This is the maximum you’ll pay for
                            an On-Demand Instance, expressed as a percentage higher than the cheapest M, C, or R
                            instance type with your specified attributes. When Amazon EC2 Auto Scaling selects instance
                            types with your attributes, we will exclude instance types whose price is higher than your
                            threshold. The parameter accepts an integer, which Amazon EC2 Auto Scaling interprets as a
                            percentage. To turn off price protection, specify a high value, such as 999999.

                            If you set DesiredCapacityType to vcpu or memory-mib, the price protection threshold is
                            applied based on the per vCPU or per memory price instead of the per instance price.

                            Default: 20

                        * BareMetal (str, Optional):
                            Indicates whether bare metal instance types are included, excluded, or required.

                            Default: excluded

                        * BurstablePerformance (str, Optional):
                            Indicates whether burstable performance instance types are included, excluded, or required.
                            For more information, see Burstable performance instances in the Amazon EC2 User Guide for
                            Linux Instances.

                            Default: excluded

                        * RequireHibernateSupport (bool, Optional):
                            Indicates whether instance types must provide On-Demand Instance hibernation support.

                            Default: false

                        * NetworkInterfaceCount (dict[str, Any], Optional):
                            The minimum and maximum number of network interfaces for an instance type.

                            Default: No minimum or maximum

                            * Min (int, Optional): The minimum number of network interfaces.
                            * Max (int, Optional): The maximum number of network interfaces.

                        * LocalStorage (str, Optional):
                            Indicates whether instance types with instance store volumes are included, excluded, or
                            required. For more information, see Amazon EC2 instance store in the Amazon EC2 User Guide
                            for Linux Instances.

                            Default: included

                        * LocalStorageTypes (list[str], Optional):
                            Indicates the type of local storage that is required.

                            * For instance types with hard disk drive (HDD) storage, specify hdd.
                            * For instance types with solid state drive (SSD) storage, specify sdd.

                            Default: Any local storage type

                        * TotalLocalStorageGB (dict[str, Any], Optional):
                            The minimum and maximum total local storage size for an instance type, in GB.

                            Default: No minimum or maximum

                            * Min (float, Optional): The storage minimum in GB.
                            * Max (float, Optional): The storage maximum in GB.

                        * BaselineEbsBandwidthMbps (dict[str, Any], Optional):
                            The minimum and maximum baseline bandwidth performance for an instance type, in Mbps. For
                            more information, see Amazon EBS–optimized instances in the Amazon EC2 User Guide for Linux
                            Instances.

                            Default: No minimum or maximum

                            * Min (int, Optional): The minimum value in Mbps.
                            * Max (int, Optional): The maximum value in Mbps.

                        * AcceleratorTypes (list[str], Optional):
                            Lists the accelerator types that must be on an instance type.

                            * For instance types with GPU accelerators, specify gpu.
                            * For instance types with FPGA accelerators, specify fpga.
                            * For instance types with inference accelerators, specify inference.

                            Default: Any accelerator type

                        * AcceleratorCount (dict[str, Any], Optional):
                            The minimum and maximum number of accelerators (GPUs, FPGAs, or Amazon Web Services
                            Inferentia chips) for an instance type.

                            To exclude accelerator-enabled instance types, set Max to 0.

                            Default: No minimum or maximum

                            * Min (int, Optional): The minimum value.
                            * Max (int, Optional): The maximum value.

                        * AcceleratorManufacturers (list[str], Optional):
                            Indicates whether instance types must have accelerators by specific manufacturers.

                            * For instance types with NVIDIA devices, specify nvidia.
                            * For instance types with AMD devices, specify amd.
                            * For instance types with Amazon Web Services devices, specify amazon-web-services.
                            * For instance types with Xilinx devices, specify xilinx.

                            Default: Any manufacturer

                        * AcceleratorNames (list[str], Optional):
                            Lists the accelerators that must be on an instance type.

                            * For instance types with NVIDIA A100 GPUs, specify a100.
                            * For instance types with NVIDIA V100 GPUs, specify v100.
                            * For instance types with NVIDIA K80 GPUs, specify k80.
                            * For instance types with NVIDIA T4 GPUs, specify t4.
                            * For instance types with NVIDIA M60 GPUs, specify m60.
                            * For instance types with AMD Radeon Pro V520 GPUs, specify radeon-pro-v520.
                            * For instance types with Xilinx VU9P FPGAs, specify vu9p.

                            Default: Any accelerator

                        * AcceleratorTotalMemoryMiB (dict[str, Any], Optional):
                            The minimum and maximum total memory size for the accelerators on an instance type, in MiB.

                            Default: No minimum or maximum

                            * Min (int, Optional): The memory minimum in MiB.
                            * Max (int, Optional): The memory maximum in MiB.

            * InstancesDistribution (dict[str, Any], Optional):
                Specifies the instances distribution.

                * OnDemandAllocationStrategy (str, Optional):
                    The order of the launch template overrides to use in fulfilling On-Demand capacity.

                    If you specify lowest-price, Amazon EC2 Auto Scaling uses price to determine the order, launching
                    the lowest price first.

                    If you specify prioritized, Amazon EC2 Auto Scaling uses the priority that you assigned to each
                    launch template override, launching the highest priority first. If all your On-Demand capacity
                    cannot be fulfilled using your highest priority instance, then Amazon EC2 Auto Scaling launches the
                    remaining capacity using the second priority instance type, and so on.

                    Default: lowest-price for Auto Scaling groups that specify InstanceRequirements in the overrides
                    and prioritized for Auto Scaling groups that don't.

                    Valid values: lowest-price | prioritized

                * OnDemandBaseCapacity (int, Optional):
                    The minimum amount of the Auto Scaling group's capacity that must be fulfilled by On-Demand
                    Instances. This base portion is launched first as your group scales.

                    If you specify weights for the instance types in the overrides, the base capacity is measured in
                    the same unit of measurement as the instance types. If you specify InstanceRequirements in the
                    overrides, the base capacity is measured in the same unit of measurement as your group's desired
                    capacity.

                    Default: 0

                * OnDemandPercentageAboveBaseCapacity (int, Optional):
                    Controls the percentages of On-Demand Instances and Spot Instances for your additional capacity
                    beyond OnDemandBaseCapacity. Expressed as a number (for example, 20 specifies 20% On-Demand
                    Instances, 80% Spot Instances). If set to 100, only On-Demand Instances are used.

                    Default: 100

                * SpotAllocationStrategy (str, Optional):
                    Indicates how to allocate instances across Spot Instance pools.

                    If the allocation strategy is lowest-price, the Auto Scaling group launches instances using the
                    Spot pools with the lowest price, and evenly allocates your instances across the number of Spot
                    pools that you specify.

                    If the allocation strategy is capacity-optimized (recommended), the Auto Scaling group launches
                    instances using Spot pools that are optimally chosen based on the available Spot capacity.
                    Alternatively, you can use capacity-optimized-prioritized and set the order of instance types in
                    the list of launch template overrides from highest to lowest priority (from first to last in the
                    list). Amazon EC2 Auto Scaling honors the instance type priorities on a best-effort basis but
                    optimizes for capacity first.

                    Default: lowest-price

                    Valid values: lowest-price | capacity-optimized | capacity-optimized-prioritized

                * SpotInstancePools (int, Optional):
                    The number of Spot Instance pools across which to allocate your Spot Instances. The Spot pools
                    are determined from the different instance types in the overrides. Valid only when the Spot
                    allocation strategy is lowest-price. Value must be in the range of 1–20.

                    Default: 2

                * SpotMaxPrice (str, Optional):
                    The maximum price per unit hour that you are willing to pay for a Spot Instance. If you keep the
                    value at its default (unspecified), Amazon EC2 Auto Scaling uses the On-Demand price as the
                    maximum Spot price. To remove a value that you previously set, include the property but specify
                    an empty string ("") for the value.

                    .. Warning::
                        If your maximum price is lower than the Spot price for the instance types that you selected,
                        your Spot Instances are not launched.

                    Valid Range: Minimum value of 0.001

        instance_id(str, Optional):
            The ID of the instance used to base the launch configuration on. If specified, Amazon EC2 Auto
            Scaling uses the configuration values from the specified instance to create a new launch configuration. To
            get the instance ID, use the Amazon EC2 DescribeInstances API operation. For more information, see Creating
            an Auto Scaling group using an EC2 instance in the Amazon EC2 Auto Scaling User Guide.

            Defaults to None.

        min_size(int):
            The minimum size of the group.

        max_size(int):
            The maximum size of the group.

            .. Note::
                With a mixed instances policy that uses instance weighting, Amazon EC2 Auto Scaling may need to go
                above MaxSize to meet your capacity requirements. In this event, Amazon EC2 Auto Scaling will never go
                above MaxSize by more than your largest instance weight (weights that define how many units each
                instance contributes to the desired capacity of the group).

        desired_capacity(int, Optional):
            The desired capacity is the initial capacity of the Auto Scaling group at the time of its
            creation and the capacity it attempts to maintain. It can scale beyond this capacity if you
            configure auto scaling. This number must be greater than or equal to the minimum size of the
            group and less than or equal to the maximum size of the group. If you do not specify a desired
            capacity, the default is the minimum size of the group. Defaults to None.

        default_cooldown(int, Optional):
            The amount of time, in seconds, after a scaling activity completes before another scaling
            activity can start. The default value is 300. This setting applies when using simple scaling
            policies, but not when using other scaling policies or scheduled scaling. For more information,
            see Scaling cooldowns for Amazon EC2 Auto Scaling in the Amazon EC2 Auto Scaling User Guide.

            Default: 300 seconds

        availability_zones(list, Optional):
            A list of Availability Zones where instances in the Auto Scaling group can be created. Used for launching
            into the default VPC subnet in each Availability Zone when not using the VPCZoneIdentifier property, or for
            attaching a network interface when an existing network interface ID is specified in a launch template.
            Defaults to None.

        load_balancer_names(list, Optional):
            A list of Classic Load Balancers associated with this Auto Scaling group. For Application Load
            Balancers, Network Load Balancers, and Gateway Load Balancers, specify the TargetGroupARNs
            property instead. Defaults to None.

        target_group_ar_ns(list, Optional):
            The Amazon Resource Names (ARN) of the target groups to associate with the Auto Scaling group.
            Instances are registered as targets in a target group, and traffic is routed to the target
            group. For more information, see Elastic Load Balancing and Amazon EC2 Auto Scaling in the
            Amazon EC2 Auto Scaling User Guide. Defaults to None.

        health_check_type(str, Optional):
            The service to use for the health checks. The valid values are EC2 (default) and ELB. If you
            configure an Auto Scaling group to use load balancer (ELB) health checks, it considers the
            instance unhealthy if it fails either the EC2 status checks or the load balancer health checks.
            For more information, see Health checks for Auto Scaling instances in the Amazon EC2 Auto
            Scaling User Guide. Defaults to None.

        health_check_grace_period(int, Optional):
            The amount of time, in seconds, that Amazon EC2 Auto Scaling waits before checking the health
            status of an EC2 instance that has come into service and marking it unhealthy due to a failed
            health check. The default value is 0. For more information, see Health check grace period in the
            Amazon EC2 Auto Scaling User Guide. Required if you are adding an ELB health check.

            Default: 0 seconds

        placement_group(str, Optional):
            The name of the placement group into which to launch your instances. For more information,
            see Placement Groups in the Amazon EC2 User Guide for Linux Instances.

            .. Note::
                A placement group is a logical grouping of instances within a single Availability Zone. You cannot
                specify multiple Availability Zones and a placement group.

            Defaults to None.

        vpc_zone_identifier(str, Optional):
            A comma-separated list of subnet IDs for a virtual private cloud (VPC) where instances in the
            Auto Scaling group can be created. If you specify VPCZoneIdentifier with AvailabilityZones, the
            subnets that you specify must reside in those Availability Zones.

        termination_policies(list[str], Optional):
            A policy or a list of policies that are used to select the instance to terminate. These policies
            are executed in the order that you list them. For more information, see Controlling which Auto
            Scaling instances terminate during scale in the Amazon EC2 Auto Scaling User Guide. Defaults to None.

            Valid values: Default | AllocationStrategy | ClosestToNextInstanceHour | NewestInstance
            | OldestInstance | OldestLaunchConfiguration | OldestLaunchTemplate
            | arn:aws:lambda:region:account-id:function:my-function:my-alias

        new_instances_protected_from_scale_in(bool, Optional):
            Indicates whether newly launched instances are protected from termination by Amazon EC2 Auto
            Scaling when scaling in. For more information about preventing instances from terminating on
            scale in, see Using instance scale-in protection in the Amazon EC2 Auto Scaling User Guide.
            Defaults to None.

        capacity_rebalance(bool, Optional):
            Indicates whether Capacity Rebalancing is enabled. Otherwise, Capacity Rebalancing is disabled.
            When you turn on Capacity Rebalancing, Amazon EC2 Auto Scaling attempts to launch a Spot
            Instance whenever Amazon EC2 notifies that a Spot Instance is at an elevated risk of
            interruption. After launching a new instance, it then terminates an old instance. For more
            information, see Amazon EC2 Auto Scaling Capacity Rebalancing in the Amazon EC2 Auto Scaling
            User Guide. Defaults to None.

        lifecycle_hook_specification_list(list[dict[str, Any]], Optional):
            One or more lifecycle hooks for the group, which specify actions to perform when Amazon EC2 Auto
            Scaling launches or terminates instances. Defaults to None.

            * LifecycleHookName (str):
                The name of the lifecycle hook.

            * LifecycleTransition (str):
                The state of the EC2 instance to which you want to attach the lifecycle hook. For Auto Scaling groups,
                there are two major lifecycle transitions.

                * To create a lifecycle hook for scale-out events, specify autoscaling:EC2_INSTANCE_LAUNCHING.
                * To create a lifecycle hook for scale-in events, specify autoscaling:EC2_INSTANCE_TERMINATING.

            * NotificationMetadata (str, Optional):
                Additional information that you want to include any time Amazon EC2 Auto Scaling sends a message
                to the notification target.

            * HeartbeatTimeout (int, Optional):
                The maximum time, in seconds, that can elapse before the lifecycle hook times out.
                The range is from 30 to 7200 seconds. The default value is 3600 seconds (1 hour).

            * DefaultResult (str, Optional):
                Defines the action the Auto Scaling group should take when the lifecycle hook timeout elapses or
                if an unexpected failure occurs. The valid values are CONTINUE and ABANDON. The default value is
                ABANDON.

            * NotificationTargetARN (str, Optional):
                The ARN of the target that Amazon EC2 Auto Scaling sends notifications to when an instance is in
                the transition state for the lifecycle hook. The notification target can be either an SQS queue
                or an SNS topic.

            * RoleARN (str, Optional):
                The ARN of the IAM role that allows the Auto Scaling group to publish to the specified
                notification target. Valid only if the notification target is an Amazon SNS topic or an Amazon
                SQS queue. Required for new lifecycle hooks, but optional when updating existing hooks.

        tags(dict or list, Optional):
            Dict in the format of {tag-key: tag-value, propagate_at_launch-{tag-key}: value}
            or list of tags in the format of [{"key": tag-key, "value": tag-value, "propagate_at_launch": value}].

            One or more tags. You can tag your Auto Scaling group and propagate the tags to the Amazon EC2
            instances it launches. Tags are not propagated to Amazon EBS volumes. To add tags to Amazon EBS
            volumes, specify the tags in a launch template but use caution. If the launch template specifies
            an instance tag with a key that is also specified for the Auto Scaling group, Amazon EC2 Auto
            Scaling overrides the value of that instance tag with the value specified by the Auto Scaling
            group. For more information, see Tagging Auto Scaling groups and instances in the Amazon EC2
            Auto Scaling User Guide. Defaults to None.

            * (key):
                The tag key.
            * (value, Optional):
                The tag value.
            * (propagate_at_launch, Optional):
                Determines whether the tag is added to new instances as they are launched in the group.

        service_linked_role_arn(str, Optional):
            The Amazon Resource Name (ARN) of the service-linked role that the Auto Scaling group uses to
            call other Amazon Web Services on your behalf. By default, Amazon EC2 Auto Scaling uses a
            service-linked role named AWSServiceRoleForAutoScaling, which it creates if it does not exist.
            For more information, see Service-linked roles in the Amazon EC2 Auto Scaling User Guide. Defaults to None.

        max_instance_lifetime(int, Optional):
            The maximum amount of time, in seconds, that an instance can be in service. The default is null.
            If specified, the value must be either 0 or a number equal to or greater than 86,400 seconds (1
            day). For more information, see Replacing Auto Scaling instances based on maximum instance
            lifetime in the Amazon EC2 Auto Scaling User Guide. Defaults to None.

        desired_capacity_type(str, Optional):
            The unit of measurement for the value specified for desired capacity. Amazon EC2 Auto Scaling
            supports DesiredCapacityType for attribute-based instance type selection only. For more
            information, see Creating an Auto Scaling group using attribute-based instance type selection in
            the Amazon EC2 Auto Scaling User Guide.

            By default, Amazon EC2 Auto Scaling specifies units, which translates into number of instances.

            Valid values: units | vcpu | memory-mib. Defaults to None.

    Request Syntax:
        .. code-block:: sls

            [auto-scaling-group-resource-id]:
              aws.autoscaling.auto_scaling_group.present:
                - resource_id: "string"
                - name: "string"
                - launch_configuration_name: "string"
                - min_size: "int"
                - max_size: "int"
                - desired_capacity: "int"
                - default_cooldown: "int"
                - availability_zones: List
                - health_check_type: "string"
                - health_check_grace_period: "int"
                - vpc_zone_identifier: "string"
                - termination_policies: List
                - new_instances_protected_from_scale_in: "bool"
                - tags: Dict or List


    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem-scaling-group:
              aws.autoscaling.auto_scaling_group.present:
                - resource_id: idem-scaling-group
                - name: idem-scaling-group
                - launch_configuration_name: idem-launch_configuration
                - min_size: 2
                - max_size: 4
                - desired_capacity: 2
                - default_cooldown: 300
                - availability_zones:
                    - us-west-1b
                    - us-west-1c
                - health_check_type: EC2
                - health_check_grace_period: 300
                - vpc_zone_identifier: subnet-xxxxxxx,subnet-xxxxxxx,subnet-xxxxxx
                - termination_policies:
                    - Default
                - new_instances_protected_from_scale_in: false
                - tags(tags in list format):
                    - key: Identifier
                      value: idem-aws
                      propagate_at_launch: true
                - key: Name
                  propagate_at_launch: false
                  value: idem-scaling-group
              - tags(or in dict format):
                  Identifier: idem-aws
                  propagate_at_launch-Identifier: true
                  Name: idem-scaling-group
                  propagate_at_launch-Name: false
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if launch_template and "Version" in launch_template:
        launch_template["Version"] = str(launch_template["Version"])

    if mixed_instances_policy:
        # Version field of LaunchTemplateSpecification should be string, but idem is considering it as int
        # while passing through sls, so handling the Version field accordingly.

        template = mixed_instances_policy.get("LaunchTemplate", {})
        launch_template_specification = template.get("LaunchTemplateSpecification", {})
        if launch_template_specification and "Version" in launch_template_specification:
            launch_template_specification["Version"] = str(
                launch_template_specification["Version"]
            )

        overrides = template.get("Overrides", [])
        for item in overrides:
            lts = item.get("LaunchTemplateSpecification", {})
            if lts and "Version" in lts:
                lts["Version"] = str(lts["Version"])

    if launch_configuration_name == "":
        launch_configuration_name = None

    if (
        not launch_template
        and not launch_configuration_name
        and not mixed_instances_policy
    ):
        result["comment"] += [
            "Either launch_template or launch_configuration_name or mixed_instances_policy must be provided"
        ]
        result["result"] = False
        return result

    # Query for auto scaling groups
    auto_scaling_group = None
    if resource_id:
        auto_scaling_group = (
            await hub.exec.boto3.client.autoscaling.describe_auto_scaling_groups(
                ctx, AutoScalingGroupNames=[resource_id]
            )
        )
        if not auto_scaling_group["result"]:
            result["comment"] = auto_scaling_group["comment"]
            result["result"] = auto_scaling_group["result"]
            return result
    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_auto_scaling_tag_list_to_dict(tags)

    # Check for existing auto scaling group
    before = None
    if auto_scaling_group and auto_scaling_group["ret"]["AutoScalingGroups"]:
        before = auto_scaling_group["ret"]["AutoScalingGroups"][0]

    # Update current state
    current_state = hub.tool.aws.autoscaling.auto_scaling_group_utils.convert_raw_auto_scaling_group_to_present(
        auto_scaling_group=before
    )
    result["old_state"] = current_state

    # Handle No change behaviour
    desired_state = {
        "name": name,
        "resource_id": resource_id,
        "launch_configuration_name": launch_configuration_name,
        "launch_template": launch_template,
        "instance_id": instance_id,
        "min_size": min_size,
        "max_size": max_size,
        "desired_capacity": desired_capacity,
        "default_cooldown": default_cooldown,
        "availability_zones": availability_zones,
        "load_balancer_names": load_balancer_names,
        "target_group_ar_ns": target_group_ar_ns,
        "health_check_type": health_check_type,
        "health_check_grace_period": health_check_grace_period,
        "placement_group": placement_group,
        "mixed_instances_policy": mixed_instances_policy,
        "vpc_zone_identifier": vpc_zone_identifier,
        "termination_policies": termination_policies,
        "new_instances_protected_from_scale_in": new_instances_protected_from_scale_in,
        "capacity_rebalance": capacity_rebalance,
        "lifecycle_hook_specification_list": lifecycle_hook_specification_list,
        "tags": tags,
        "max_instance_lifetime": max_instance_lifetime,
        "desired_capacity_type": desired_capacity_type,
    }

    desired_state = hub.tool.aws.state_utils.merge_arguments(
        desire_state=copy.deepcopy(desired_state), current_state=current_state
    )

    is_auto_scaling_group_updated = (
        hub.tool.aws.autoscaling.auto_scaling_group_utils.is_update_required(
            current_state=current_state, desired_state=desired_state
        )
    )

    is_tags_updated = current_state.get("tags") != desired_state.get("tags")

    is_change_detected = (
        before is None or is_auto_scaling_group_updated or is_tags_updated
    )

    if not is_change_detected:
        result["comment"] += [
            f"aws.autoscaling.auto_scaling_group '{name}' already exists"
        ]
        result["new_state"] = copy.deepcopy(result["old_state"])
        return result

    # Handle test behaviour
    if ctx.get("test", False):
        result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
            enforced_state=current_state,
            desired_state=desired_state,
        )
        result["new_state"]["launch_configuration_name"] = launch_configuration_name
        result["new_state"]["launch_template"] = launch_template
        result["comment"] = (
            hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.autoscaling.auto_scaling_group", name=name
            )
            if before
            else hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.autoscaling.auto_scaling_group", name=name
            )
        )
        return result

    # Handle actual resource create or update
    if before:
        # Update auto scaling group
        if is_auto_scaling_group_updated:
            ret = await hub.exec.boto3.client.autoscaling.update_auto_scaling_group(
                ctx,
                **{
                    "AutoScalingGroupName": name,
                    "LaunchConfigurationName": launch_configuration_name,
                    "LaunchTemplate": launch_template,
                    "MixedInstancesPolicy": mixed_instances_policy,
                    "InstanceId": instance_id,
                    "MinSize": min_size,
                    "MaxSize": max_size,
                    "DesiredCapacity": desired_capacity,
                    "DefaultCooldown": default_cooldown,
                    "AvailabilityZones": availability_zones,
                    "HealthCheckType": health_check_type,
                    "HealthCheckGracePeriod": health_check_grace_period,
                    "PlacementGroup": placement_group,
                    "VPCZoneIdentifier": vpc_zone_identifier,
                    "TerminationPolicies": termination_policies,
                    "NewInstancesProtectedFromScaleIn": new_instances_protected_from_scale_in,
                    "CapacityRebalance": capacity_rebalance,
                    "LifecycleHookSpecificationList": lifecycle_hook_specification_list,
                    "ServiceLinkedRoleARN": service_linked_role_arn,
                    "MaxInstanceLifetime": max_instance_lifetime,
                    "DesiredCapacityType": desired_capacity_type,
                },
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            result["comment"] = hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.autoscaling.auto_scaling_group", name=name
            )

        # Update tags
        if is_tags_updated:
            update_tags = await hub.tool.aws.autoscaling.tag.update_tags(
                ctx,
                old_tags=current_state["tags"],
                new_tags=desired_state["tags"],
                resource_id=resource_id,
            )
            result["comment"] += update_tags["comment"]
            result["result"] = result["result"] and update_tags["result"]
            if not result["result"]:
                result["comment"] = update_tags["comment"]
                return result
    else:
        # Handle actual resource creation
        tags_list = hub.tool.aws.tag_utils.convert_auto_scaling_tag_dict_to_list(tags)
        translated_tags = hub.tool.aws.autoscaling.auto_scaling_group_utils.convert_present_tags_to_raw_tags(
            resource_id=name, tags=tags_list
        )
        ret = await hub.exec.boto3.client.autoscaling.create_auto_scaling_group(
            ctx,
            **{
                "AutoScalingGroupName": name,
                "LaunchConfigurationName": launch_configuration_name,
                "LaunchTemplate": launch_template,
                "MixedInstancesPolicy": mixed_instances_policy,
                "InstanceId": instance_id,
                "MinSize": min_size,
                "MaxSize": max_size,
                "DesiredCapacity": desired_capacity,
                "DefaultCooldown": default_cooldown,
                "AvailabilityZones": availability_zones,
                "LoadBalancerNames": load_balancer_names,
                "TargetGroupARNs": target_group_ar_ns,
                "HealthCheckType": health_check_type,
                "HealthCheckGracePeriod": health_check_grace_period,
                "PlacementGroup": placement_group,
                "VPCZoneIdentifier": vpc_zone_identifier,
                "TerminationPolicies": termination_policies,
                "NewInstancesProtectedFromScaleIn": new_instances_protected_from_scale_in,
                "CapacityRebalance": capacity_rebalance,
                "LifecycleHookSpecificationList": lifecycle_hook_specification_list,
                "Tags": translated_tags,
                "ServiceLinkedRoleARN": service_linked_role_arn,
                "MaxInstanceLifetime": max_instance_lifetime,
                "DesiredCapacityType": desired_capacity_type,
            },
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.autoscaling.auto_scaling_group", name=name
        )
        resource_id = name

    # Populate new state
    new_auto_scaling_groups = (
        await hub.exec.boto3.client.autoscaling.describe_auto_scaling_groups(
            ctx, AutoScalingGroupNames=[resource_id]
        )
    )
    if not new_auto_scaling_groups["result"]:
        result["comment"] += new_auto_scaling_groups["comment"]
        result["result"] = new_auto_scaling_groups["result"]
        return result

    after = new_auto_scaling_groups["ret"]["AutoScalingGroups"][0]
    result[
        "new_state"
    ] = hub.tool.aws.autoscaling.auto_scaling_group_utils.convert_raw_auto_scaling_group_to_present(
        auto_scaling_group=after
    )
    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    timeout: Dict = None,
) -> Dict[str, Any]:
    """Deletes the specified Auto Scaling group.

    If the group has instances or scaling activities in progress, you must specify the option to force the deletion
    in order for it to succeed.

    If the group has policies, deleting the group deletes the policies, the underlying alarm actions, and any alarm
    that no longer has an associated action.

    To remove instances from the Auto Scaling group before deleting it, call the DetachInstances API with the list
    of instances and the option to decrement the desired capacity. This ensures that Amazon EC2 Auto Scaling does
    not launch replacement instances.

    To terminate all instances before deleting the Auto Scaling group, call the UpdateAutoScalingGroup API and set the
    minimum size and desired capacity of the Auto Scaling group to zero.

    Args:
        resource_id(str, Optional):
            The name of the Auto Scaling group.
        name(str):
            An Idem name of the resource.
        timeout(dict, Optional):
            Timeout configuration for deletion of AWS auto scaling group.

            * delete (dict) -- Timeout configuration for deletion of an auto scaling group.
                * delay -- The amount of time in seconds to wait between attempts. Defaults to 15
                * max_attempts -- Customized timeout configuration containing delay and max attempts. Defaults to 40

    Request Syntax:
        .. code-block:: sls

            [auto-scaling-group-resource-id]:
              aws.autoscaling.auto_scaling_group.absent:
                - resource_id: "string"
                - name: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem-scaling-group:
              aws.autoscaling.auto_scaling_group.absent:
                - resource_id: idem-scaling-group
                - name: idem-scaling-group
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    # Query for auto scaling groups
    auto_scaling_group = None
    if resource_id:
        auto_scaling_group = (
            await hub.exec.boto3.client.autoscaling.describe_auto_scaling_groups(
                ctx, AutoScalingGroupNames=[resource_id]
            )
        )

    # Check for existing auto scaling group
    before = None
    if (
        auto_scaling_group
        and auto_scaling_group["result"]
        and auto_scaling_group["ret"]["AutoScalingGroups"]
    ):
        before = auto_scaling_group["ret"]["AutoScalingGroups"][0]
        result[
            "old_state"
        ] = hub.tool.aws.autoscaling.auto_scaling_group_utils.convert_raw_auto_scaling_group_to_present(
            auto_scaling_group=before
        )

    if not before:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.autoscaling.auto_scaling_group", name=name
        )

    elif ctx.get("test", False):
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.autoscaling.auto_scaling_group", name=name
        )

    else:
        ret = await hub.exec.boto3.client.autoscaling.delete_auto_scaling_group(
            ctx,
            AutoScalingGroupName=resource_id,
            ForceDelete=True,
        )
        if not ret["result"]:
            result["result"] = ret["result"]
            result["comment"] = ret["comment"]
            return result

        # Custom waiter for delete
        waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
            default_delay=15,
            default_max_attempts=40,
            timeout_config=timeout.get("delete") if timeout else None,
        )
        delete_waiter_acceptors = [
            {
                "matcher": "path",
                "expected": True,
                "state": "success",
                "argument": "length(AutoScalingGroups) == `0`",
            },
            {
                "matcher": "path",
                "expected": True,
                "state": "retry",
                "argument": "length(AutoScalingGroups) > `0`",
            },
        ]
        auto_scaling_group_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
            name="AutoScalingGroupDelete",
            operation="DescribeAutoScalingGroups",
            argument=["AutoScalingGroups"],
            acceptors=delete_waiter_acceptors,
            client=await hub.tool.boto3.client.get_client(ctx, "autoscaling"),
        )
        try:
            await hub.tool.boto3.client.wait(
                ctx,
                "autoscaling",
                "AutoScalingGroupDelete",
                auto_scaling_group_waiter,
                AutoScalingGroupNames=[
                    resource_id,
                ],
                WaiterConfig=waiter_config,
            )
        except Exception as e:
            result["comment"] += [str(e)]
            result["result"] = False
            return result

        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.autoscaling.auto_scaling_group", name=name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Gets information about the Auto Scaling groups in the account and Region.

    Describe the resource in a way that can be recreated/managed with the corresponding "present" function.


    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.autoscaling.auto_scaling_group
    """
    result = {}
    ret = await hub.exec.boto3.client.autoscaling.describe_auto_scaling_groups(ctx)
    if not ret["result"]:
        hub.log.warning(f"Could not describe auto_scaling_group {ret['comment']}")
        return {}

    for auto_scaling_group in ret["ret"]["AutoScalingGroups"]:
        resource_id = auto_scaling_group["AutoScalingGroupName"]
        resource = hub.tool.aws.autoscaling.auto_scaling_group_utils.convert_raw_auto_scaling_group_to_present(
            auto_scaling_group=auto_scaling_group
        )
        result[resource_id] = {
            "aws.autoscaling.auto_scaling_group.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }
    return result
