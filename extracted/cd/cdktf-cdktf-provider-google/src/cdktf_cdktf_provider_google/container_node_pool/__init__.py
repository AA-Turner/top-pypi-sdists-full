r'''
# `google_container_node_pool`

Refer to the Terraform Registry for docs: [`google_container_node_pool`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class ContainerNodePool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool google_container_node_pool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster: builtins.str,
        autoscaling: typing.Optional[typing.Union["ContainerNodePoolAutoscaling", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        initial_node_count: typing.Optional[jsii.Number] = None,
        location: typing.Optional[builtins.str] = None,
        management: typing.Optional[typing.Union["ContainerNodePoolManagement", typing.Dict[builtins.str, typing.Any]]] = None,
        max_pods_per_node: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        network_config: typing.Optional[typing.Union["ContainerNodePoolNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_count: typing.Optional[jsii.Number] = None,
        node_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
        placement_policy: typing.Optional[typing.Union["ContainerNodePoolPlacementPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        queued_provisioning: typing.Optional[typing.Union["ContainerNodePoolQueuedProvisioning", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ContainerNodePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        upgrade_settings: typing.Optional[typing.Union["ContainerNodePoolUpgradeSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool google_container_node_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster: The cluster to create the node pool for. Cluster must be present in location provided for zonal clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#cluster ContainerNodePool#cluster}
        :param autoscaling: autoscaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#autoscaling ContainerNodePool#autoscaling}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#id ContainerNodePool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_node_count: The initial number of nodes for the pool. In regional or multi-zonal clusters, this is the number of nodes per zone. Changing this will force recreation of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#initial_node_count ContainerNodePool#initial_node_count}
        :param location: The location (region or zone) of the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#location ContainerNodePool#location}
        :param management: management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#management ContainerNodePool#management}
        :param max_pods_per_node: The maximum number of pods per node in this node pool. Note that this does not work on node pools which are "route-based" - that is, node pools belonging to clusters that do not have IP Aliasing enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#max_pods_per_node ContainerNodePool#max_pods_per_node}
        :param name: The name of the node pool. If left blank, Terraform will auto-generate a unique name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#name ContainerNodePool#name}
        :param name_prefix: Creates a unique name for the node pool beginning with the specified prefix. Conflicts with name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#name_prefix ContainerNodePool#name_prefix}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#network_config ContainerNodePool#network_config}
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#node_config ContainerNodePool#node_config}
        :param node_count: The number of nodes per instance group. This field can be used to update the number of nodes per instance group but should not be used alongside autoscaling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#node_count ContainerNodePool#node_count}
        :param node_locations: The list of zones in which the node pool's nodes should be located. Nodes must be in the region of their regional cluster or in the same region as their cluster's zone for zonal clusters. If unspecified, the cluster-level node_locations will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#node_locations ContainerNodePool#node_locations}
        :param placement_policy: placement_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#placement_policy ContainerNodePool#placement_policy}
        :param project: The ID of the project in which to create the node pool. If blank, the provider-configured project will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#project ContainerNodePool#project}
        :param queued_provisioning: queued_provisioning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#queued_provisioning ContainerNodePool#queued_provisioning}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#timeouts ContainerNodePool#timeouts}
        :param upgrade_settings: upgrade_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#upgrade_settings ContainerNodePool#upgrade_settings}
        :param version: The Kubernetes version for the nodes in this pool. Note that if this field and auto_upgrade are both specified, they will fight each other for what the node version should be, so setting both is highly discouraged. While a fuzzy version can be specified, it's recommended that you specify explicit versions as Terraform will see spurious diffs when fuzzy versions are used. See the google_container_engine_versions data source's version_prefix field to approximate fuzzy versions in a Terraform-compatible way. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#version ContainerNodePool#version}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca9abea3bd333b65f45372e99fa915899559f46dac335423a83703889f336bf2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ContainerNodePoolConfig(
            cluster=cluster,
            autoscaling=autoscaling,
            id=id,
            initial_node_count=initial_node_count,
            location=location,
            management=management,
            max_pods_per_node=max_pods_per_node,
            name=name,
            name_prefix=name_prefix,
            network_config=network_config,
            node_config=node_config,
            node_count=node_count,
            node_locations=node_locations,
            placement_policy=placement_policy,
            project=project,
            queued_provisioning=queued_provisioning,
            timeouts=timeouts,
            upgrade_settings=upgrade_settings,
            version=version,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a ContainerNodePool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ContainerNodePool to import.
        :param import_from_id: The id of the existing ContainerNodePool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ContainerNodePool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6967d132a175adacba6abc837e68bf46d55dc0908e3fd4b68cd845b3c85b0b95)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutoscaling")
    def put_autoscaling(
        self,
        *,
        location_policy: typing.Optional[builtins.str] = None,
        max_node_count: typing.Optional[jsii.Number] = None,
        min_node_count: typing.Optional[jsii.Number] = None,
        total_max_node_count: typing.Optional[jsii.Number] = None,
        total_min_node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param location_policy: Location policy specifies the algorithm used when scaling-up the node pool. "BALANCED" - Is a best effort policy that aims to balance the sizes of available zones. "ANY" - Instructs the cluster autoscaler to prioritize utilization of unused reservations, and reduces preemption risk for Spot VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#location_policy ContainerNodePool#location_policy}
        :param max_node_count: Maximum number of nodes per zone in the node pool. Must be >= min_node_count. Cannot be used with total limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#max_node_count ContainerNodePool#max_node_count}
        :param min_node_count: Minimum number of nodes per zone in the node pool. Must be >=0 and <= max_node_count. Cannot be used with total limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#min_node_count ContainerNodePool#min_node_count}
        :param total_max_node_count: Maximum number of all nodes in the node pool. Must be >= total_min_node_count. Cannot be used with per zone limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#total_max_node_count ContainerNodePool#total_max_node_count}
        :param total_min_node_count: Minimum number of all nodes in the node pool. Must be >=0 and <= total_max_node_count. Cannot be used with per zone limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#total_min_node_count ContainerNodePool#total_min_node_count}
        '''
        value = ContainerNodePoolAutoscaling(
            location_policy=location_policy,
            max_node_count=max_node_count,
            min_node_count=min_node_count,
            total_max_node_count=total_max_node_count,
            total_min_node_count=total_min_node_count,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscaling", [value]))

    @jsii.member(jsii_name="putManagement")
    def put_management(
        self,
        *,
        auto_repair: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_upgrade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param auto_repair: Whether the nodes will be automatically repaired. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#auto_repair ContainerNodePool#auto_repair}
        :param auto_upgrade: Whether the nodes will be automatically upgraded. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#auto_upgrade ContainerNodePool#auto_upgrade}
        '''
        value = ContainerNodePoolManagement(
            auto_repair=auto_repair, auto_upgrade=auto_upgrade
        )

        return typing.cast(None, jsii.invoke(self, "putManagement", [value]))

    @jsii.member(jsii_name="putNetworkConfig")
    def put_network_config(
        self,
        *,
        additional_node_network_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        additional_pod_network_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        create_pod_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_private_nodes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network_performance_config: typing.Optional[typing.Union["ContainerNodePoolNetworkConfigNetworkPerformanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        pod_cidr_overprovision_config: typing.Optional[typing.Union["ContainerNodePoolNetworkConfigPodCidrOverprovisionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        pod_ipv4_cidr_block: typing.Optional[builtins.str] = None,
        pod_range: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param additional_node_network_configs: additional_node_network_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#additional_node_network_configs ContainerNodePool#additional_node_network_configs}
        :param additional_pod_network_configs: additional_pod_network_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#additional_pod_network_configs ContainerNodePool#additional_pod_network_configs}
        :param create_pod_range: Whether to create a new range for pod IPs in this node pool. Defaults are provided for pod_range and pod_ipv4_cidr_block if they are not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#create_pod_range ContainerNodePool#create_pod_range}
        :param enable_private_nodes: Whether nodes have internal IP addresses only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enable_private_nodes ContainerNodePool#enable_private_nodes}
        :param network_performance_config: network_performance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#network_performance_config ContainerNodePool#network_performance_config}
        :param pod_cidr_overprovision_config: pod_cidr_overprovision_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#pod_cidr_overprovision_config ContainerNodePool#pod_cidr_overprovision_config}
        :param pod_ipv4_cidr_block: The IP address range for pod IPs in this node pool. Only applicable if create_pod_range is true. Set to blank to have a range chosen with the default size. Set to /netmask (e.g. /14) to have a range chosen with a specific netmask. Set to a CIDR notation (e.g. 10.96.0.0/14) to pick a specific range to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#pod_ipv4_cidr_block ContainerNodePool#pod_ipv4_cidr_block}
        :param pod_range: The ID of the secondary range for pod IPs. If create_pod_range is true, this ID is used for the new range. If create_pod_range is false, uses an existing secondary range with this ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#pod_range ContainerNodePool#pod_range}
        '''
        value = ContainerNodePoolNetworkConfig(
            additional_node_network_configs=additional_node_network_configs,
            additional_pod_network_configs=additional_pod_network_configs,
            create_pod_range=create_pod_range,
            enable_private_nodes=enable_private_nodes,
            network_performance_config=network_performance_config,
            pod_cidr_overprovision_config=pod_cidr_overprovision_config,
            pod_ipv4_cidr_block=pod_ipv4_cidr_block,
            pod_range=pod_range,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfig", [value]))

    @jsii.member(jsii_name="putNodeConfig")
    def put_node_config(
        self,
        *,
        advanced_machine_features: typing.Optional[typing.Union["ContainerNodePoolNodeConfigAdvancedMachineFeatures", typing.Dict[builtins.str, typing.Any]]] = None,
        boot_disk_kms_key: typing.Optional[builtins.str] = None,
        confidential_nodes: typing.Optional[typing.Union["ContainerNodePoolNodeConfigConfidentialNodes", typing.Dict[builtins.str, typing.Any]]] = None,
        containerd_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigContainerdConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        disk_type: typing.Optional[builtins.str] = None,
        enable_confidential_storage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ephemeral_storage_local_ssd_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        fast_socket: typing.Optional[typing.Union["ContainerNodePoolNodeConfigFastSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        flex_start: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcfs_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigGcfsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        guest_accelerator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerNodePoolNodeConfigGuestAccelerator", typing.Dict[builtins.str, typing.Any]]]]] = None,
        gvnic: typing.Optional[typing.Union["ContainerNodePoolNodeConfigGvnic", typing.Dict[builtins.str, typing.Any]]] = None,
        host_maintenance_policy: typing.Optional[typing.Union["ContainerNodePoolNodeConfigHostMaintenancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        image_type: typing.Optional[builtins.str] = None,
        kubelet_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigKubeletConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        linux_node_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigLinuxNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        local_nvme_ssd_block_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        local_ssd_count: typing.Optional[jsii.Number] = None,
        local_ssd_encryption_mode: typing.Optional[builtins.str] = None,
        logging_variant: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        max_run_duration: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        node_group: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        preemptible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reservation_affinity: typing.Optional[typing.Union["ContainerNodePoolNodeConfigReservationAffinity", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        secondary_boot_disks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerNodePoolNodeConfigSecondaryBootDisks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_account: typing.Optional[builtins.str] = None,
        shielded_instance_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        sole_tenant_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigSoleTenantConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        storage_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        taint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerNodePoolNodeConfigTaint", typing.Dict[builtins.str, typing.Any]]]]] = None,
        windows_node_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigWindowsNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        workload_metadata_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigWorkloadMetadataConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_machine_features: advanced_machine_features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#advanced_machine_features ContainerNodePool#advanced_machine_features}
        :param boot_disk_kms_key: The Customer Managed Encryption Key used to encrypt the boot disk attached to each node in the node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#boot_disk_kms_key ContainerNodePool#boot_disk_kms_key}
        :param confidential_nodes: confidential_nodes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#confidential_nodes ContainerNodePool#confidential_nodes}
        :param containerd_config: containerd_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#containerd_config ContainerNodePool#containerd_config}
        :param disk_size_gb: Size of the disk attached to each node, specified in GB. The smallest allowed disk size is 10GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#disk_size_gb ContainerNodePool#disk_size_gb}
        :param disk_type: Type of the disk attached to each node. Such as pd-standard, pd-balanced or pd-ssd. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#disk_type ContainerNodePool#disk_type}
        :param enable_confidential_storage: If enabled boot disks are configured with confidential mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enable_confidential_storage ContainerNodePool#enable_confidential_storage}
        :param ephemeral_storage_local_ssd_config: ephemeral_storage_local_ssd_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#ephemeral_storage_local_ssd_config ContainerNodePool#ephemeral_storage_local_ssd_config}
        :param fast_socket: fast_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#fast_socket ContainerNodePool#fast_socket}
        :param flex_start: Enables Flex Start provisioning model for the node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#flex_start ContainerNodePool#flex_start}
        :param gcfs_config: gcfs_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#gcfs_config ContainerNodePool#gcfs_config}
        :param guest_accelerator: guest_accelerator block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#guest_accelerator ContainerNodePool#guest_accelerator}
        :param gvnic: gvnic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#gvnic ContainerNodePool#gvnic}
        :param host_maintenance_policy: host_maintenance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#host_maintenance_policy ContainerNodePool#host_maintenance_policy}
        :param image_type: The image type to use for this node. Note that for a given image type, the latest version of it will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#image_type ContainerNodePool#image_type}
        :param kubelet_config: kubelet_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#kubelet_config ContainerNodePool#kubelet_config}
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#labels ContainerNodePool#labels}
        :param linux_node_config: linux_node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#linux_node_config ContainerNodePool#linux_node_config}
        :param local_nvme_ssd_block_config: local_nvme_ssd_block_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#local_nvme_ssd_block_config ContainerNodePool#local_nvme_ssd_block_config}
        :param local_ssd_count: The number of local SSD disks to be attached to the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#local_ssd_count ContainerNodePool#local_ssd_count}
        :param local_ssd_encryption_mode: LocalSsdEncryptionMode specified the method used for encrypting the local SSDs attached to the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#local_ssd_encryption_mode ContainerNodePool#local_ssd_encryption_mode}
        :param logging_variant: Type of logging agent that is used as the default value for node pools in the cluster. Valid values include DEFAULT and MAX_THROUGHPUT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#logging_variant ContainerNodePool#logging_variant}
        :param machine_type: The name of a Google Compute Engine machine type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#machine_type ContainerNodePool#machine_type}
        :param max_run_duration: The runtime of each node in the node pool in seconds, terminated by 's'. Example: "3600s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#max_run_duration ContainerNodePool#max_run_duration}
        :param metadata: The metadata key/value pairs assigned to instances in the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#metadata ContainerNodePool#metadata}
        :param min_cpu_platform: Minimum CPU platform to be used by this instance. The instance may be scheduled on the specified or newer CPU platform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#min_cpu_platform ContainerNodePool#min_cpu_platform}
        :param node_group: Setting this field will assign instances of this pool to run on the specified node group. This is useful for running workloads on sole tenant nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#node_group ContainerNodePool#node_group}
        :param oauth_scopes: The set of Google API scopes to be made available on all of the node VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#oauth_scopes ContainerNodePool#oauth_scopes}
        :param preemptible: Whether the nodes are created as preemptible VM instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#preemptible ContainerNodePool#preemptible}
        :param reservation_affinity: reservation_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#reservation_affinity ContainerNodePool#reservation_affinity}
        :param resource_labels: The GCE resource labels (a map of key/value pairs) to be applied to the node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#resource_labels ContainerNodePool#resource_labels}
        :param resource_manager_tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#resource_manager_tags ContainerNodePool#resource_manager_tags}
        :param secondary_boot_disks: secondary_boot_disks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#secondary_boot_disks ContainerNodePool#secondary_boot_disks}
        :param service_account: The Google Cloud Platform Service Account to be used by the node VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#service_account ContainerNodePool#service_account}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#shielded_instance_config ContainerNodePool#shielded_instance_config}
        :param sole_tenant_config: sole_tenant_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#sole_tenant_config ContainerNodePool#sole_tenant_config}
        :param spot: Whether the nodes are created as spot VM instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#spot ContainerNodePool#spot}
        :param storage_pools: The list of Storage Pools where boot disks are provisioned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#storage_pools ContainerNodePool#storage_pools}
        :param tags: The list of instance tags applied to all nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#tags ContainerNodePool#tags}
        :param taint: taint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#taint ContainerNodePool#taint}
        :param windows_node_config: windows_node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#windows_node_config ContainerNodePool#windows_node_config}
        :param workload_metadata_config: workload_metadata_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#workload_metadata_config ContainerNodePool#workload_metadata_config}
        '''
        value = ContainerNodePoolNodeConfig(
            advanced_machine_features=advanced_machine_features,
            boot_disk_kms_key=boot_disk_kms_key,
            confidential_nodes=confidential_nodes,
            containerd_config=containerd_config,
            disk_size_gb=disk_size_gb,
            disk_type=disk_type,
            enable_confidential_storage=enable_confidential_storage,
            ephemeral_storage_local_ssd_config=ephemeral_storage_local_ssd_config,
            fast_socket=fast_socket,
            flex_start=flex_start,
            gcfs_config=gcfs_config,
            guest_accelerator=guest_accelerator,
            gvnic=gvnic,
            host_maintenance_policy=host_maintenance_policy,
            image_type=image_type,
            kubelet_config=kubelet_config,
            labels=labels,
            linux_node_config=linux_node_config,
            local_nvme_ssd_block_config=local_nvme_ssd_block_config,
            local_ssd_count=local_ssd_count,
            local_ssd_encryption_mode=local_ssd_encryption_mode,
            logging_variant=logging_variant,
            machine_type=machine_type,
            max_run_duration=max_run_duration,
            metadata=metadata,
            min_cpu_platform=min_cpu_platform,
            node_group=node_group,
            oauth_scopes=oauth_scopes,
            preemptible=preemptible,
            reservation_affinity=reservation_affinity,
            resource_labels=resource_labels,
            resource_manager_tags=resource_manager_tags,
            secondary_boot_disks=secondary_boot_disks,
            service_account=service_account,
            shielded_instance_config=shielded_instance_config,
            sole_tenant_config=sole_tenant_config,
            spot=spot,
            storage_pools=storage_pools,
            tags=tags,
            taint=taint,
            windows_node_config=windows_node_config,
            workload_metadata_config=workload_metadata_config,
        )

        return typing.cast(None, jsii.invoke(self, "putNodeConfig", [value]))

    @jsii.member(jsii_name="putPlacementPolicy")
    def put_placement_policy(
        self,
        *,
        type: builtins.str,
        policy_name: typing.Optional[builtins.str] = None,
        tpu_topology: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type defines the type of placement policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#type ContainerNodePool#type}
        :param policy_name: If set, refers to the name of a custom resource policy supplied by the user. The resource policy must be in the same project and region as the node pool. If not found, InvalidArgument error is returned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#policy_name ContainerNodePool#policy_name}
        :param tpu_topology: The TPU topology like "2x4" or "2x2x2". https://cloud.google.com/kubernetes-engine/docs/concepts/plan-tpus#topology. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#tpu_topology ContainerNodePool#tpu_topology}
        '''
        value = ContainerNodePoolPlacementPolicy(
            type=type, policy_name=policy_name, tpu_topology=tpu_topology
        )

        return typing.cast(None, jsii.invoke(self, "putPlacementPolicy", [value]))

    @jsii.member(jsii_name="putQueuedProvisioning")
    def put_queued_provisioning(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether nodes in this node pool are obtainable solely through the ProvisioningRequest API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enabled ContainerNodePool#enabled}
        '''
        value = ContainerNodePoolQueuedProvisioning(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putQueuedProvisioning", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#create ContainerNodePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#delete ContainerNodePool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#update ContainerNodePool#update}.
        '''
        value = ContainerNodePoolTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUpgradeSettings")
    def put_upgrade_settings(
        self,
        *,
        blue_green_settings: typing.Optional[typing.Union["ContainerNodePoolUpgradeSettingsBlueGreenSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        max_surge: typing.Optional[jsii.Number] = None,
        max_unavailable: typing.Optional[jsii.Number] = None,
        strategy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param blue_green_settings: blue_green_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#blue_green_settings ContainerNodePool#blue_green_settings}
        :param max_surge: The number of additional nodes that can be added to the node pool during an upgrade. Increasing max_surge raises the number of nodes that can be upgraded simultaneously. Can be set to 0 or greater. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#max_surge ContainerNodePool#max_surge}
        :param max_unavailable: The number of nodes that can be simultaneously unavailable during an upgrade. Increasing max_unavailable raises the number of nodes that can be upgraded in parallel. Can be set to 0 or greater. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#max_unavailable ContainerNodePool#max_unavailable}
        :param strategy: Update strategy for the given nodepool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#strategy ContainerNodePool#strategy}
        '''
        value = ContainerNodePoolUpgradeSettings(
            blue_green_settings=blue_green_settings,
            max_surge=max_surge,
            max_unavailable=max_unavailable,
            strategy=strategy,
        )

        return typing.cast(None, jsii.invoke(self, "putUpgradeSettings", [value]))

    @jsii.member(jsii_name="resetAutoscaling")
    def reset_autoscaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscaling", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInitialNodeCount")
    def reset_initial_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialNodeCount", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetManagement")
    def reset_management(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagement", []))

    @jsii.member(jsii_name="resetMaxPodsPerNode")
    def reset_max_pods_per_node(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxPodsPerNode", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNamePrefix")
    def reset_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamePrefix", []))

    @jsii.member(jsii_name="resetNetworkConfig")
    def reset_network_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConfig", []))

    @jsii.member(jsii_name="resetNodeConfig")
    def reset_node_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeConfig", []))

    @jsii.member(jsii_name="resetNodeCount")
    def reset_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeCount", []))

    @jsii.member(jsii_name="resetNodeLocations")
    def reset_node_locations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeLocations", []))

    @jsii.member(jsii_name="resetPlacementPolicy")
    def reset_placement_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlacementPolicy", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetQueuedProvisioning")
    def reset_queued_provisioning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueuedProvisioning", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUpgradeSettings")
    def reset_upgrade_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpgradeSettings", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="autoscaling")
    def autoscaling(self) -> "ContainerNodePoolAutoscalingOutputReference":
        return typing.cast("ContainerNodePoolAutoscalingOutputReference", jsii.get(self, "autoscaling"))

    @builtins.property
    @jsii.member(jsii_name="instanceGroupUrls")
    def instance_group_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceGroupUrls"))

    @builtins.property
    @jsii.member(jsii_name="managedInstanceGroupUrls")
    def managed_instance_group_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "managedInstanceGroupUrls"))

    @builtins.property
    @jsii.member(jsii_name="management")
    def management(self) -> "ContainerNodePoolManagementOutputReference":
        return typing.cast("ContainerNodePoolManagementOutputReference", jsii.get(self, "management"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(self) -> "ContainerNodePoolNetworkConfigOutputReference":
        return typing.cast("ContainerNodePoolNetworkConfigOutputReference", jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfig")
    def node_config(self) -> "ContainerNodePoolNodeConfigOutputReference":
        return typing.cast("ContainerNodePoolNodeConfigOutputReference", jsii.get(self, "nodeConfig"))

    @builtins.property
    @jsii.member(jsii_name="operation")
    def operation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operation"))

    @builtins.property
    @jsii.member(jsii_name="placementPolicy")
    def placement_policy(self) -> "ContainerNodePoolPlacementPolicyOutputReference":
        return typing.cast("ContainerNodePoolPlacementPolicyOutputReference", jsii.get(self, "placementPolicy"))

    @builtins.property
    @jsii.member(jsii_name="queuedProvisioning")
    def queued_provisioning(
        self,
    ) -> "ContainerNodePoolQueuedProvisioningOutputReference":
        return typing.cast("ContainerNodePoolQueuedProvisioningOutputReference", jsii.get(self, "queuedProvisioning"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ContainerNodePoolTimeoutsOutputReference":
        return typing.cast("ContainerNodePoolTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="upgradeSettings")
    def upgrade_settings(self) -> "ContainerNodePoolUpgradeSettingsOutputReference":
        return typing.cast("ContainerNodePoolUpgradeSettingsOutputReference", jsii.get(self, "upgradeSettings"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingInput")
    def autoscaling_input(self) -> typing.Optional["ContainerNodePoolAutoscaling"]:
        return typing.cast(typing.Optional["ContainerNodePoolAutoscaling"], jsii.get(self, "autoscalingInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterInput")
    def cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="initialNodeCountInput")
    def initial_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="managementInput")
    def management_input(self) -> typing.Optional["ContainerNodePoolManagement"]:
        return typing.cast(typing.Optional["ContainerNodePoolManagement"], jsii.get(self, "managementInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPodsPerNodeInput")
    def max_pods_per_node_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPodsPerNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namePrefixInput")
    def name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigInput")
    def network_config_input(self) -> typing.Optional["ContainerNodePoolNetworkConfig"]:
        return typing.cast(typing.Optional["ContainerNodePoolNetworkConfig"], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfigInput")
    def node_config_input(self) -> typing.Optional["ContainerNodePoolNodeConfig"]:
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfig"], jsii.get(self, "nodeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeCountInput")
    def node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeLocationsInput")
    def node_locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "nodeLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="placementPolicyInput")
    def placement_policy_input(
        self,
    ) -> typing.Optional["ContainerNodePoolPlacementPolicy"]:
        return typing.cast(typing.Optional["ContainerNodePoolPlacementPolicy"], jsii.get(self, "placementPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="queuedProvisioningInput")
    def queued_provisioning_input(
        self,
    ) -> typing.Optional["ContainerNodePoolQueuedProvisioning"]:
        return typing.cast(typing.Optional["ContainerNodePoolQueuedProvisioning"], jsii.get(self, "queuedProvisioningInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerNodePoolTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerNodePoolTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="upgradeSettingsInput")
    def upgrade_settings_input(
        self,
    ) -> typing.Optional["ContainerNodePoolUpgradeSettings"]:
        return typing.cast(typing.Optional["ContainerNodePoolUpgradeSettings"], jsii.get(self, "upgradeSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bff5ba290576d142fcf32031b738150e663fa4e97d31d9d36a4c65a5188ccbbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86d34d72f51c9c7d7e897e4e4f091eacd2924400f8e3f959a42161f8957d9908)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialNodeCount")
    def initial_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialNodeCount"))

    @initial_node_count.setter
    def initial_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f24f87adb695ed60e7902dc3b71e9a349b50cfcb0f4f0a30f0274bc5ccd3f28f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89ecf4f8b859c78cbde0c69fa5d98922df5d77a5a11490803ddf16a9235a80b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxPodsPerNode")
    def max_pods_per_node(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPodsPerNode"))

    @max_pods_per_node.setter
    def max_pods_per_node(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4eeb7ca49c81028ae25d5481ead5632b9792ca5fd39281a38e71837d3ac1660)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPodsPerNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22aa633c9045af5a5b7699a64b1bd3801e89f692a4c40c4aa639f0d4d0cbd6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namePrefix")
    def name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namePrefix"))

    @name_prefix.setter
    def name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cd015913f8bde6e2020a18b3e0665c7ae70e1b007bc5bedda06d596d32199b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac7671d227ef4ff53317843b34c786357d279a4c8430a8c33215130ffbfba3d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeLocations")
    def node_locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "nodeLocations"))

    @node_locations.setter
    def node_locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ee4985ce84c9293be49ebcb5708b50ee5cb1a1fd0b50aa75eeea32c37c3a71c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeLocations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a35f3db4b76b142b2a636a863d1673fd934be8e00fef74a5f1e826822cc2efd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d2eacfe908a46590117dc8bb3411d62bcd40b5053c0b0f097d4b4891a60edf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolAutoscaling",
    jsii_struct_bases=[],
    name_mapping={
        "location_policy": "locationPolicy",
        "max_node_count": "maxNodeCount",
        "min_node_count": "minNodeCount",
        "total_max_node_count": "totalMaxNodeCount",
        "total_min_node_count": "totalMinNodeCount",
    },
)
class ContainerNodePoolAutoscaling:
    def __init__(
        self,
        *,
        location_policy: typing.Optional[builtins.str] = None,
        max_node_count: typing.Optional[jsii.Number] = None,
        min_node_count: typing.Optional[jsii.Number] = None,
        total_max_node_count: typing.Optional[jsii.Number] = None,
        total_min_node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param location_policy: Location policy specifies the algorithm used when scaling-up the node pool. "BALANCED" - Is a best effort policy that aims to balance the sizes of available zones. "ANY" - Instructs the cluster autoscaler to prioritize utilization of unused reservations, and reduces preemption risk for Spot VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#location_policy ContainerNodePool#location_policy}
        :param max_node_count: Maximum number of nodes per zone in the node pool. Must be >= min_node_count. Cannot be used with total limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#max_node_count ContainerNodePool#max_node_count}
        :param min_node_count: Minimum number of nodes per zone in the node pool. Must be >=0 and <= max_node_count. Cannot be used with total limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#min_node_count ContainerNodePool#min_node_count}
        :param total_max_node_count: Maximum number of all nodes in the node pool. Must be >= total_min_node_count. Cannot be used with per zone limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#total_max_node_count ContainerNodePool#total_max_node_count}
        :param total_min_node_count: Minimum number of all nodes in the node pool. Must be >=0 and <= total_max_node_count. Cannot be used with per zone limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#total_min_node_count ContainerNodePool#total_min_node_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e69a00ccd28bc7146a8e3e75397c3f4ad4a26d9503125e9e93e95c042677bbe)
            check_type(argname="argument location_policy", value=location_policy, expected_type=type_hints["location_policy"])
            check_type(argname="argument max_node_count", value=max_node_count, expected_type=type_hints["max_node_count"])
            check_type(argname="argument min_node_count", value=min_node_count, expected_type=type_hints["min_node_count"])
            check_type(argname="argument total_max_node_count", value=total_max_node_count, expected_type=type_hints["total_max_node_count"])
            check_type(argname="argument total_min_node_count", value=total_min_node_count, expected_type=type_hints["total_min_node_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if location_policy is not None:
            self._values["location_policy"] = location_policy
        if max_node_count is not None:
            self._values["max_node_count"] = max_node_count
        if min_node_count is not None:
            self._values["min_node_count"] = min_node_count
        if total_max_node_count is not None:
            self._values["total_max_node_count"] = total_max_node_count
        if total_min_node_count is not None:
            self._values["total_min_node_count"] = total_min_node_count

    @builtins.property
    def location_policy(self) -> typing.Optional[builtins.str]:
        '''Location policy specifies the algorithm used when scaling-up the node pool.

        "BALANCED" - Is a best effort policy that aims to balance the sizes of available zones. "ANY" - Instructs the cluster autoscaler to prioritize utilization of unused reservations, and reduces preemption risk for Spot VMs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#location_policy ContainerNodePool#location_policy}
        '''
        result = self._values.get("location_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_node_count(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of nodes per zone in the node pool.

        Must be >= min_node_count. Cannot be used with total limits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#max_node_count ContainerNodePool#max_node_count}
        '''
        result = self._values.get("max_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_node_count(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of nodes per zone in the node pool.

        Must be >=0 and <= max_node_count. Cannot be used with total limits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#min_node_count ContainerNodePool#min_node_count}
        '''
        result = self._values.get("min_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def total_max_node_count(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of all nodes in the node pool.

        Must be >= total_min_node_count. Cannot be used with per zone limits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#total_max_node_count ContainerNodePool#total_max_node_count}
        '''
        result = self._values.get("total_max_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def total_min_node_count(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of all nodes in the node pool.

        Must be >=0 and <= total_max_node_count. Cannot be used with per zone limits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#total_min_node_count ContainerNodePool#total_min_node_count}
        '''
        result = self._values.get("total_min_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolAutoscaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolAutoscalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolAutoscalingOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__139cc054b9ef89966c8893a134c656add40f339f0df0cbe65ad8493142ece246)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLocationPolicy")
    def reset_location_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocationPolicy", []))

    @jsii.member(jsii_name="resetMaxNodeCount")
    def reset_max_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxNodeCount", []))

    @jsii.member(jsii_name="resetMinNodeCount")
    def reset_min_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinNodeCount", []))

    @jsii.member(jsii_name="resetTotalMaxNodeCount")
    def reset_total_max_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTotalMaxNodeCount", []))

    @jsii.member(jsii_name="resetTotalMinNodeCount")
    def reset_total_min_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTotalMinNodeCount", []))

    @builtins.property
    @jsii.member(jsii_name="locationPolicyInput")
    def location_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="maxNodeCountInput")
    def max_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minNodeCountInput")
    def min_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="totalMaxNodeCountInput")
    def total_max_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "totalMaxNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="totalMinNodeCountInput")
    def total_min_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "totalMinNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="locationPolicy")
    def location_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locationPolicy"))

    @location_policy.setter
    def location_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a2c722bd7e0ce4a2e9daa6ee507b878f101e460711e6d5553c5d1543a3e3fd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locationPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxNodeCount")
    def max_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxNodeCount"))

    @max_node_count.setter
    def max_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56f54baddb21611356fb0d58575afbd56e580e609a5c2e2fa48b2426ded30c27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNodeCount")
    def min_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNodeCount"))

    @min_node_count.setter
    def min_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9a15a3ac8292d2455bb44d64346863fc36344e91fe06c2b499e5321bb56123)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="totalMaxNodeCount")
    def total_max_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalMaxNodeCount"))

    @total_max_node_count.setter
    def total_max_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9850ad92fff6d51e395773dcdb51d4d41e9f6c00f367cd4c6cfc4c6e802c12f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "totalMaxNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="totalMinNodeCount")
    def total_min_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalMinNodeCount"))

    @total_min_node_count.setter
    def total_min_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae60240cc93e735e2ff040e9f4a97431b93d93e1b2af92735fc8412bc41b35a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "totalMinNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerNodePoolAutoscaling]:
        return typing.cast(typing.Optional[ContainerNodePoolAutoscaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolAutoscaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c6c9e9cf9612368dbeee25a7230dc914a95bea16b7e73443b0d0747d3a20483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cluster": "cluster",
        "autoscaling": "autoscaling",
        "id": "id",
        "initial_node_count": "initialNodeCount",
        "location": "location",
        "management": "management",
        "max_pods_per_node": "maxPodsPerNode",
        "name": "name",
        "name_prefix": "namePrefix",
        "network_config": "networkConfig",
        "node_config": "nodeConfig",
        "node_count": "nodeCount",
        "node_locations": "nodeLocations",
        "placement_policy": "placementPolicy",
        "project": "project",
        "queued_provisioning": "queuedProvisioning",
        "timeouts": "timeouts",
        "upgrade_settings": "upgradeSettings",
        "version": "version",
    },
)
class ContainerNodePoolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cluster: builtins.str,
        autoscaling: typing.Optional[typing.Union[ContainerNodePoolAutoscaling, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        initial_node_count: typing.Optional[jsii.Number] = None,
        location: typing.Optional[builtins.str] = None,
        management: typing.Optional[typing.Union["ContainerNodePoolManagement", typing.Dict[builtins.str, typing.Any]]] = None,
        max_pods_per_node: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        network_config: typing.Optional[typing.Union["ContainerNodePoolNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_count: typing.Optional[jsii.Number] = None,
        node_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
        placement_policy: typing.Optional[typing.Union["ContainerNodePoolPlacementPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        queued_provisioning: typing.Optional[typing.Union["ContainerNodePoolQueuedProvisioning", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ContainerNodePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        upgrade_settings: typing.Optional[typing.Union["ContainerNodePoolUpgradeSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster: The cluster to create the node pool for. Cluster must be present in location provided for zonal clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#cluster ContainerNodePool#cluster}
        :param autoscaling: autoscaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#autoscaling ContainerNodePool#autoscaling}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#id ContainerNodePool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_node_count: The initial number of nodes for the pool. In regional or multi-zonal clusters, this is the number of nodes per zone. Changing this will force recreation of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#initial_node_count ContainerNodePool#initial_node_count}
        :param location: The location (region or zone) of the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#location ContainerNodePool#location}
        :param management: management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#management ContainerNodePool#management}
        :param max_pods_per_node: The maximum number of pods per node in this node pool. Note that this does not work on node pools which are "route-based" - that is, node pools belonging to clusters that do not have IP Aliasing enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#max_pods_per_node ContainerNodePool#max_pods_per_node}
        :param name: The name of the node pool. If left blank, Terraform will auto-generate a unique name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#name ContainerNodePool#name}
        :param name_prefix: Creates a unique name for the node pool beginning with the specified prefix. Conflicts with name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#name_prefix ContainerNodePool#name_prefix}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#network_config ContainerNodePool#network_config}
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#node_config ContainerNodePool#node_config}
        :param node_count: The number of nodes per instance group. This field can be used to update the number of nodes per instance group but should not be used alongside autoscaling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#node_count ContainerNodePool#node_count}
        :param node_locations: The list of zones in which the node pool's nodes should be located. Nodes must be in the region of their regional cluster or in the same region as their cluster's zone for zonal clusters. If unspecified, the cluster-level node_locations will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#node_locations ContainerNodePool#node_locations}
        :param placement_policy: placement_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#placement_policy ContainerNodePool#placement_policy}
        :param project: The ID of the project in which to create the node pool. If blank, the provider-configured project will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#project ContainerNodePool#project}
        :param queued_provisioning: queued_provisioning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#queued_provisioning ContainerNodePool#queued_provisioning}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#timeouts ContainerNodePool#timeouts}
        :param upgrade_settings: upgrade_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#upgrade_settings ContainerNodePool#upgrade_settings}
        :param version: The Kubernetes version for the nodes in this pool. Note that if this field and auto_upgrade are both specified, they will fight each other for what the node version should be, so setting both is highly discouraged. While a fuzzy version can be specified, it's recommended that you specify explicit versions as Terraform will see spurious diffs when fuzzy versions are used. See the google_container_engine_versions data source's version_prefix field to approximate fuzzy versions in a Terraform-compatible way. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#version ContainerNodePool#version}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(autoscaling, dict):
            autoscaling = ContainerNodePoolAutoscaling(**autoscaling)
        if isinstance(management, dict):
            management = ContainerNodePoolManagement(**management)
        if isinstance(network_config, dict):
            network_config = ContainerNodePoolNetworkConfig(**network_config)
        if isinstance(node_config, dict):
            node_config = ContainerNodePoolNodeConfig(**node_config)
        if isinstance(placement_policy, dict):
            placement_policy = ContainerNodePoolPlacementPolicy(**placement_policy)
        if isinstance(queued_provisioning, dict):
            queued_provisioning = ContainerNodePoolQueuedProvisioning(**queued_provisioning)
        if isinstance(timeouts, dict):
            timeouts = ContainerNodePoolTimeouts(**timeouts)
        if isinstance(upgrade_settings, dict):
            upgrade_settings = ContainerNodePoolUpgradeSettings(**upgrade_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b5b6bcb2c794aac413c6600fc6527e94c0489eeed9dc04e3576397641aead23)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument autoscaling", value=autoscaling, expected_type=type_hints["autoscaling"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument initial_node_count", value=initial_node_count, expected_type=type_hints["initial_node_count"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument management", value=management, expected_type=type_hints["management"])
            check_type(argname="argument max_pods_per_node", value=max_pods_per_node, expected_type=type_hints["max_pods_per_node"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument name_prefix", value=name_prefix, expected_type=type_hints["name_prefix"])
            check_type(argname="argument network_config", value=network_config, expected_type=type_hints["network_config"])
            check_type(argname="argument node_config", value=node_config, expected_type=type_hints["node_config"])
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
            check_type(argname="argument node_locations", value=node_locations, expected_type=type_hints["node_locations"])
            check_type(argname="argument placement_policy", value=placement_policy, expected_type=type_hints["placement_policy"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument queued_provisioning", value=queued_provisioning, expected_type=type_hints["queued_provisioning"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument upgrade_settings", value=upgrade_settings, expected_type=type_hints["upgrade_settings"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster": cluster,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if autoscaling is not None:
            self._values["autoscaling"] = autoscaling
        if id is not None:
            self._values["id"] = id
        if initial_node_count is not None:
            self._values["initial_node_count"] = initial_node_count
        if location is not None:
            self._values["location"] = location
        if management is not None:
            self._values["management"] = management
        if max_pods_per_node is not None:
            self._values["max_pods_per_node"] = max_pods_per_node
        if name is not None:
            self._values["name"] = name
        if name_prefix is not None:
            self._values["name_prefix"] = name_prefix
        if network_config is not None:
            self._values["network_config"] = network_config
        if node_config is not None:
            self._values["node_config"] = node_config
        if node_count is not None:
            self._values["node_count"] = node_count
        if node_locations is not None:
            self._values["node_locations"] = node_locations
        if placement_policy is not None:
            self._values["placement_policy"] = placement_policy
        if project is not None:
            self._values["project"] = project
        if queued_provisioning is not None:
            self._values["queued_provisioning"] = queued_provisioning
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if upgrade_settings is not None:
            self._values["upgrade_settings"] = upgrade_settings
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def cluster(self) -> builtins.str:
        '''The cluster to create the node pool for. Cluster must be present in location provided for zonal clusters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#cluster ContainerNodePool#cluster}
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autoscaling(self) -> typing.Optional[ContainerNodePoolAutoscaling]:
        '''autoscaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#autoscaling ContainerNodePool#autoscaling}
        '''
        result = self._values.get("autoscaling")
        return typing.cast(typing.Optional[ContainerNodePoolAutoscaling], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#id ContainerNodePool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_node_count(self) -> typing.Optional[jsii.Number]:
        '''The initial number of nodes for the pool.

        In regional or multi-zonal clusters, this is the number of nodes per zone. Changing this will force recreation of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#initial_node_count ContainerNodePool#initial_node_count}
        '''
        result = self._values.get("initial_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location (region or zone) of the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#location ContainerNodePool#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def management(self) -> typing.Optional["ContainerNodePoolManagement"]:
        '''management block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#management ContainerNodePool#management}
        '''
        result = self._values.get("management")
        return typing.cast(typing.Optional["ContainerNodePoolManagement"], result)

    @builtins.property
    def max_pods_per_node(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of pods per node in this node pool.

        Note that this does not work on node pools which are "route-based" - that is, node pools belonging to clusters that do not have IP Aliasing enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#max_pods_per_node ContainerNodePool#max_pods_per_node}
        '''
        result = self._values.get("max_pods_per_node")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the node pool. If left blank, Terraform will auto-generate a unique name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#name ContainerNodePool#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_prefix(self) -> typing.Optional[builtins.str]:
        '''Creates a unique name for the node pool beginning with the specified prefix. Conflicts with name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#name_prefix ContainerNodePool#name_prefix}
        '''
        result = self._values.get("name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_config(self) -> typing.Optional["ContainerNodePoolNetworkConfig"]:
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#network_config ContainerNodePool#network_config}
        '''
        result = self._values.get("network_config")
        return typing.cast(typing.Optional["ContainerNodePoolNetworkConfig"], result)

    @builtins.property
    def node_config(self) -> typing.Optional["ContainerNodePoolNodeConfig"]:
        '''node_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#node_config ContainerNodePool#node_config}
        '''
        result = self._values.get("node_config")
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfig"], result)

    @builtins.property
    def node_count(self) -> typing.Optional[jsii.Number]:
        '''The number of nodes per instance group.

        This field can be used to update the number of nodes per instance group but should not be used alongside autoscaling.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#node_count ContainerNodePool#node_count}
        '''
        result = self._values.get("node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def node_locations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of zones in which the node pool's nodes should be located.

        Nodes must be in the region of their regional cluster or in the same region as their cluster's zone for zonal clusters. If unspecified, the cluster-level node_locations will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#node_locations ContainerNodePool#node_locations}
        '''
        result = self._values.get("node_locations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def placement_policy(self) -> typing.Optional["ContainerNodePoolPlacementPolicy"]:
        '''placement_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#placement_policy ContainerNodePool#placement_policy}
        '''
        result = self._values.get("placement_policy")
        return typing.cast(typing.Optional["ContainerNodePoolPlacementPolicy"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which to create the node pool.

        If blank, the provider-configured project will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#project ContainerNodePool#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def queued_provisioning(
        self,
    ) -> typing.Optional["ContainerNodePoolQueuedProvisioning"]:
        '''queued_provisioning block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#queued_provisioning ContainerNodePool#queued_provisioning}
        '''
        result = self._values.get("queued_provisioning")
        return typing.cast(typing.Optional["ContainerNodePoolQueuedProvisioning"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ContainerNodePoolTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#timeouts ContainerNodePool#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ContainerNodePoolTimeouts"], result)

    @builtins.property
    def upgrade_settings(self) -> typing.Optional["ContainerNodePoolUpgradeSettings"]:
        '''upgrade_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#upgrade_settings ContainerNodePool#upgrade_settings}
        '''
        result = self._values.get("upgrade_settings")
        return typing.cast(typing.Optional["ContainerNodePoolUpgradeSettings"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The Kubernetes version for the nodes in this pool.

        Note that if this field and auto_upgrade are both specified, they will fight each other for what the node version should be, so setting both is highly discouraged. While a fuzzy version can be specified, it's recommended that you specify explicit versions as Terraform will see spurious diffs when fuzzy versions are used. See the google_container_engine_versions data source's version_prefix field to approximate fuzzy versions in a Terraform-compatible way.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#version ContainerNodePool#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolManagement",
    jsii_struct_bases=[],
    name_mapping={"auto_repair": "autoRepair", "auto_upgrade": "autoUpgrade"},
)
class ContainerNodePoolManagement:
    def __init__(
        self,
        *,
        auto_repair: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_upgrade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param auto_repair: Whether the nodes will be automatically repaired. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#auto_repair ContainerNodePool#auto_repair}
        :param auto_upgrade: Whether the nodes will be automatically upgraded. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#auto_upgrade ContainerNodePool#auto_upgrade}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae5fb0d3da25e65124e9e67126562a8e2c5a46ce209000e4f96f66e236b8a950)
            check_type(argname="argument auto_repair", value=auto_repair, expected_type=type_hints["auto_repair"])
            check_type(argname="argument auto_upgrade", value=auto_upgrade, expected_type=type_hints["auto_upgrade"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_repair is not None:
            self._values["auto_repair"] = auto_repair
        if auto_upgrade is not None:
            self._values["auto_upgrade"] = auto_upgrade

    @builtins.property
    def auto_repair(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the nodes will be automatically repaired. Enabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#auto_repair ContainerNodePool#auto_repair}
        '''
        result = self._values.get("auto_repair")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auto_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the nodes will be automatically upgraded. Enabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#auto_upgrade ContainerNodePool#auto_upgrade}
        '''
        result = self._values.get("auto_upgrade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolManagement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolManagementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolManagementOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c9562d994c6cd400f27f7839b9bd7da36dd0ec6c67331230eb30f90fc82a07a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAutoRepair")
    def reset_auto_repair(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoRepair", []))

    @jsii.member(jsii_name="resetAutoUpgrade")
    def reset_auto_upgrade(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoUpgrade", []))

    @builtins.property
    @jsii.member(jsii_name="autoRepairInput")
    def auto_repair_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoRepairInput"))

    @builtins.property
    @jsii.member(jsii_name="autoUpgradeInput")
    def auto_upgrade_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoUpgradeInput"))

    @builtins.property
    @jsii.member(jsii_name="autoRepair")
    def auto_repair(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoRepair"))

    @auto_repair.setter
    def auto_repair(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a31e2b8f0fcfb6376c20665e2b6242e4d75a74a91fc738b206864aba89af2046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoRepair", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoUpgrade")
    def auto_upgrade(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoUpgrade"))

    @auto_upgrade.setter
    def auto_upgrade(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ca589b0f57081fdf0b4fb5aa29378c7a8d6152e9437fe9e3cae0a1c891a6d79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoUpgrade", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerNodePoolManagement]:
        return typing.cast(typing.Optional[ContainerNodePoolManagement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolManagement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9cbc71a7868daa399a333e1e87b7a13c4a094f117e7eded551160c7904ba46f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={
        "additional_node_network_configs": "additionalNodeNetworkConfigs",
        "additional_pod_network_configs": "additionalPodNetworkConfigs",
        "create_pod_range": "createPodRange",
        "enable_private_nodes": "enablePrivateNodes",
        "network_performance_config": "networkPerformanceConfig",
        "pod_cidr_overprovision_config": "podCidrOverprovisionConfig",
        "pod_ipv4_cidr_block": "podIpv4CidrBlock",
        "pod_range": "podRange",
    },
)
class ContainerNodePoolNetworkConfig:
    def __init__(
        self,
        *,
        additional_node_network_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        additional_pod_network_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        create_pod_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_private_nodes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network_performance_config: typing.Optional[typing.Union["ContainerNodePoolNetworkConfigNetworkPerformanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        pod_cidr_overprovision_config: typing.Optional[typing.Union["ContainerNodePoolNetworkConfigPodCidrOverprovisionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        pod_ipv4_cidr_block: typing.Optional[builtins.str] = None,
        pod_range: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param additional_node_network_configs: additional_node_network_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#additional_node_network_configs ContainerNodePool#additional_node_network_configs}
        :param additional_pod_network_configs: additional_pod_network_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#additional_pod_network_configs ContainerNodePool#additional_pod_network_configs}
        :param create_pod_range: Whether to create a new range for pod IPs in this node pool. Defaults are provided for pod_range and pod_ipv4_cidr_block if they are not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#create_pod_range ContainerNodePool#create_pod_range}
        :param enable_private_nodes: Whether nodes have internal IP addresses only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enable_private_nodes ContainerNodePool#enable_private_nodes}
        :param network_performance_config: network_performance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#network_performance_config ContainerNodePool#network_performance_config}
        :param pod_cidr_overprovision_config: pod_cidr_overprovision_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#pod_cidr_overprovision_config ContainerNodePool#pod_cidr_overprovision_config}
        :param pod_ipv4_cidr_block: The IP address range for pod IPs in this node pool. Only applicable if create_pod_range is true. Set to blank to have a range chosen with the default size. Set to /netmask (e.g. /14) to have a range chosen with a specific netmask. Set to a CIDR notation (e.g. 10.96.0.0/14) to pick a specific range to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#pod_ipv4_cidr_block ContainerNodePool#pod_ipv4_cidr_block}
        :param pod_range: The ID of the secondary range for pod IPs. If create_pod_range is true, this ID is used for the new range. If create_pod_range is false, uses an existing secondary range with this ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#pod_range ContainerNodePool#pod_range}
        '''
        if isinstance(network_performance_config, dict):
            network_performance_config = ContainerNodePoolNetworkConfigNetworkPerformanceConfig(**network_performance_config)
        if isinstance(pod_cidr_overprovision_config, dict):
            pod_cidr_overprovision_config = ContainerNodePoolNetworkConfigPodCidrOverprovisionConfig(**pod_cidr_overprovision_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abbfb53fb9a1dde0675f3a0401175c08f385a25856b0a6a7c1ba60b6cfb64bbc)
            check_type(argname="argument additional_node_network_configs", value=additional_node_network_configs, expected_type=type_hints["additional_node_network_configs"])
            check_type(argname="argument additional_pod_network_configs", value=additional_pod_network_configs, expected_type=type_hints["additional_pod_network_configs"])
            check_type(argname="argument create_pod_range", value=create_pod_range, expected_type=type_hints["create_pod_range"])
            check_type(argname="argument enable_private_nodes", value=enable_private_nodes, expected_type=type_hints["enable_private_nodes"])
            check_type(argname="argument network_performance_config", value=network_performance_config, expected_type=type_hints["network_performance_config"])
            check_type(argname="argument pod_cidr_overprovision_config", value=pod_cidr_overprovision_config, expected_type=type_hints["pod_cidr_overprovision_config"])
            check_type(argname="argument pod_ipv4_cidr_block", value=pod_ipv4_cidr_block, expected_type=type_hints["pod_ipv4_cidr_block"])
            check_type(argname="argument pod_range", value=pod_range, expected_type=type_hints["pod_range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_node_network_configs is not None:
            self._values["additional_node_network_configs"] = additional_node_network_configs
        if additional_pod_network_configs is not None:
            self._values["additional_pod_network_configs"] = additional_pod_network_configs
        if create_pod_range is not None:
            self._values["create_pod_range"] = create_pod_range
        if enable_private_nodes is not None:
            self._values["enable_private_nodes"] = enable_private_nodes
        if network_performance_config is not None:
            self._values["network_performance_config"] = network_performance_config
        if pod_cidr_overprovision_config is not None:
            self._values["pod_cidr_overprovision_config"] = pod_cidr_overprovision_config
        if pod_ipv4_cidr_block is not None:
            self._values["pod_ipv4_cidr_block"] = pod_ipv4_cidr_block
        if pod_range is not None:
            self._values["pod_range"] = pod_range

    @builtins.property
    def additional_node_network_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs"]]]:
        '''additional_node_network_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#additional_node_network_configs ContainerNodePool#additional_node_network_configs}
        '''
        result = self._values.get("additional_node_network_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs"]]], result)

    @builtins.property
    def additional_pod_network_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs"]]]:
        '''additional_pod_network_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#additional_pod_network_configs ContainerNodePool#additional_pod_network_configs}
        '''
        result = self._values.get("additional_pod_network_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs"]]], result)

    @builtins.property
    def create_pod_range(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to create a new range for pod IPs in this node pool.

        Defaults are provided for pod_range and pod_ipv4_cidr_block if they are not specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#create_pod_range ContainerNodePool#create_pod_range}
        '''
        result = self._values.get("create_pod_range")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_private_nodes(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether nodes have internal IP addresses only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enable_private_nodes ContainerNodePool#enable_private_nodes}
        '''
        result = self._values.get("enable_private_nodes")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def network_performance_config(
        self,
    ) -> typing.Optional["ContainerNodePoolNetworkConfigNetworkPerformanceConfig"]:
        '''network_performance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#network_performance_config ContainerNodePool#network_performance_config}
        '''
        result = self._values.get("network_performance_config")
        return typing.cast(typing.Optional["ContainerNodePoolNetworkConfigNetworkPerformanceConfig"], result)

    @builtins.property
    def pod_cidr_overprovision_config(
        self,
    ) -> typing.Optional["ContainerNodePoolNetworkConfigPodCidrOverprovisionConfig"]:
        '''pod_cidr_overprovision_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#pod_cidr_overprovision_config ContainerNodePool#pod_cidr_overprovision_config}
        '''
        result = self._values.get("pod_cidr_overprovision_config")
        return typing.cast(typing.Optional["ContainerNodePoolNetworkConfigPodCidrOverprovisionConfig"], result)

    @builtins.property
    def pod_ipv4_cidr_block(self) -> typing.Optional[builtins.str]:
        '''The IP address range for pod IPs in this node pool.

        Only applicable if create_pod_range is true. Set to blank to have a range chosen with the default size. Set to /netmask (e.g. /14) to have a range chosen with a specific netmask. Set to a CIDR notation (e.g. 10.96.0.0/14) to pick a specific range to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#pod_ipv4_cidr_block ContainerNodePool#pod_ipv4_cidr_block}
        '''
        result = self._values.get("pod_ipv4_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pod_range(self) -> typing.Optional[builtins.str]:
        '''The ID of the secondary range for pod IPs.

        If create_pod_range is true, this ID is used for the new range. If create_pod_range is false, uses an existing secondary range with this ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#pod_range ContainerNodePool#pod_range}
        '''
        result = self._values.get("pod_range")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs",
    jsii_struct_bases=[],
    name_mapping={"network": "network", "subnetwork": "subnetwork"},
)
class ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs:
    def __init__(
        self,
        *,
        network: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param network: Name of the VPC where the additional interface belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#network ContainerNodePool#network}
        :param subnetwork: Name of the subnetwork where the additional interface belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#subnetwork ContainerNodePool#subnetwork}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6e317f25e78dbaf6222110e5e2eaa615f49056cc5f6fda2c248c51dbe250d97)
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument subnetwork", value=subnetwork, expected_type=type_hints["subnetwork"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if network is not None:
            self._values["network"] = network
        if subnetwork is not None:
            self._values["subnetwork"] = subnetwork

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''Name of the VPC where the additional interface belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#network ContainerNodePool#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''Name of the subnetwork where the additional interface belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#subnetwork ContainerNodePool#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f08b94c9c30d1f722c6ffc66e39880f6115526cb4125ce222d4e3b3d9161c726)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c79ac3f3d9d6d914bd3e1467196c4a5ca5fc8d416da2cf1d7a94d6d62b67f21)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4472781eaa237d97c9a841247fd0e8502b74b15275529644d35a219c75021042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__864ea332a77337a3ef008859be3ae009939ded50a19e6afa6f543363bc0e7e47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a90207bf61750c65d01736c8b2665de94ae0303f7bc9ade1cc0d2380195fdf94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75c8e80729854d17420fa561e1dfdc717f6a29a5ae4a8ccb0c05e2267fe3e827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6637e6210514ca11314f2d07dcc0cd1cef3d62f27dc51770385d329316270ec3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetSubnetwork")
    def reset_subnetwork(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetwork", []))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkInput")
    def subnetwork_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcb6d4faf6c27bda968f9cf54d59f8ba9181f785cdb69939315ceef7298aee8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c019cb47022bcc25bd7cc9fa55fa1b9557ceb0cb487acff36606ea80b180f263)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a9aa241e3258b24599ddc1c1c69af03829f6d4f44f89395d52e1cf306d6362a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "max_pods_per_node": "maxPodsPerNode",
        "secondary_pod_range": "secondaryPodRange",
        "subnetwork": "subnetwork",
    },
)
class ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs:
    def __init__(
        self,
        *,
        max_pods_per_node: typing.Optional[jsii.Number] = None,
        secondary_pod_range: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_pods_per_node: The maximum number of pods per node which use this pod network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#max_pods_per_node ContainerNodePool#max_pods_per_node}
        :param secondary_pod_range: The name of the secondary range on the subnet which provides IP address for this pod range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#secondary_pod_range ContainerNodePool#secondary_pod_range}
        :param subnetwork: Name of the subnetwork where the additional pod network belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#subnetwork ContainerNodePool#subnetwork}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f715e27736028e3be84e89c925de969cd88f3522188bbbde6159595831834f3a)
            check_type(argname="argument max_pods_per_node", value=max_pods_per_node, expected_type=type_hints["max_pods_per_node"])
            check_type(argname="argument secondary_pod_range", value=secondary_pod_range, expected_type=type_hints["secondary_pod_range"])
            check_type(argname="argument subnetwork", value=subnetwork, expected_type=type_hints["subnetwork"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_pods_per_node is not None:
            self._values["max_pods_per_node"] = max_pods_per_node
        if secondary_pod_range is not None:
            self._values["secondary_pod_range"] = secondary_pod_range
        if subnetwork is not None:
            self._values["subnetwork"] = subnetwork

    @builtins.property
    def max_pods_per_node(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of pods per node which use this pod network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#max_pods_per_node ContainerNodePool#max_pods_per_node}
        '''
        result = self._values.get("max_pods_per_node")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secondary_pod_range(self) -> typing.Optional[builtins.str]:
        '''The name of the secondary range on the subnet which provides IP address for this pod range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#secondary_pod_range ContainerNodePool#secondary_pod_range}
        '''
        result = self._values.get("secondary_pod_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''Name of the subnetwork where the additional pod network belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#subnetwork ContainerNodePool#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f30973022cb80904b9de8991de9c47b2f0abd593a370c4937398a65bb84e0818)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d338ca0522a5809644fbeb9265901b141140992445851a1b77a022dce2ffc55)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95d21642b3b812a4562c680aced11afad0fc1f76ef8a9fa8c6e8b1d855c39db1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8062e17ead7f519b55dc163e8561e79a6e1b406f31a4c5e32234e4717281dcb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dca7e6ef168ced4b8664f9f779e038e206cc08531aaca8862a597b3a58b29331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c70b772492c4b127fb19d57918aca4dfbee49bf8c41ae0547dae08b6fcf7e10c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__360e8eaf1387642f601fc5a0bfd5e21811d85f70a5b347a9d77be364128580d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMaxPodsPerNode")
    def reset_max_pods_per_node(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxPodsPerNode", []))

    @jsii.member(jsii_name="resetSecondaryPodRange")
    def reset_secondary_pod_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryPodRange", []))

    @jsii.member(jsii_name="resetSubnetwork")
    def reset_subnetwork(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetwork", []))

    @builtins.property
    @jsii.member(jsii_name="maxPodsPerNodeInput")
    def max_pods_per_node_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPodsPerNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryPodRangeInput")
    def secondary_pod_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secondaryPodRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkInput")
    def subnetwork_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPodsPerNode")
    def max_pods_per_node(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPodsPerNode"))

    @max_pods_per_node.setter
    def max_pods_per_node(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea7c6d2f8f829d36dfd43a3fa0526be28ac717419abfeeb46d3c84230e7adcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPodsPerNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secondaryPodRange")
    def secondary_pod_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryPodRange"))

    @secondary_pod_range.setter
    def secondary_pod_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29623a1b9019f044606ba4e4796ab329014f3b7ca4080e3f2b44844908076467)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryPodRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4bff11864fa449ebfe8ecd9e18699d7942beb3e3300c0386333eda8378b0c7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97c7529a516f326563f5fb0fc9f1bbcfd57d0f5186cc92e953bb9c88267de5a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNetworkConfigNetworkPerformanceConfig",
    jsii_struct_bases=[],
    name_mapping={"total_egress_bandwidth_tier": "totalEgressBandwidthTier"},
)
class ContainerNodePoolNetworkConfigNetworkPerformanceConfig:
    def __init__(self, *, total_egress_bandwidth_tier: builtins.str) -> None:
        '''
        :param total_egress_bandwidth_tier: Specifies the total network bandwidth tier for the NodePool. `Valid values <https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters.nodePools#NodePool.Tier>`_ include: "TIER_1" and "TIER_UNSPECIFIED". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#total_egress_bandwidth_tier ContainerNodePool#total_egress_bandwidth_tier}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__988cf913d91635960c4fd13d48fe53df3dc9c52d1b5402c0cf34e5349055046f)
            check_type(argname="argument total_egress_bandwidth_tier", value=total_egress_bandwidth_tier, expected_type=type_hints["total_egress_bandwidth_tier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "total_egress_bandwidth_tier": total_egress_bandwidth_tier,
        }

    @builtins.property
    def total_egress_bandwidth_tier(self) -> builtins.str:
        '''Specifies the total network bandwidth tier for the NodePool. `Valid values <https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters.nodePools#NodePool.Tier>`_ include: "TIER_1" and "TIER_UNSPECIFIED".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#total_egress_bandwidth_tier ContainerNodePool#total_egress_bandwidth_tier}
        '''
        result = self._values.get("total_egress_bandwidth_tier")
        assert result is not None, "Required property 'total_egress_bandwidth_tier' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNetworkConfigNetworkPerformanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNetworkConfigNetworkPerformanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNetworkConfigNetworkPerformanceConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef9b42f5e1482903e3e9f51395f366c5a9e0757ca892601ae000f6b0bda58592)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="totalEgressBandwidthTierInput")
    def total_egress_bandwidth_tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "totalEgressBandwidthTierInput"))

    @builtins.property
    @jsii.member(jsii_name="totalEgressBandwidthTier")
    def total_egress_bandwidth_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "totalEgressBandwidthTier"))

    @total_egress_bandwidth_tier.setter
    def total_egress_bandwidth_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df88508986984b431dfb6276b1037e78fcc406d15c7ba783ee94b717201c7b63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "totalEgressBandwidthTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerNodePoolNetworkConfigNetworkPerformanceConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNetworkConfigNetworkPerformanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNetworkConfigNetworkPerformanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__805a66c5a62dd290a2db6edd6f3aed4208d09678a6e56305bb62a5e1218349ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerNodePoolNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNetworkConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfa28393441632c82f009d0e2bba0bd79f9e6bc1ef61a36f768a222eabf78ae8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdditionalNodeNetworkConfigs")
    def put_additional_node_network_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f120328170db089c97f25f1643bec2765beafc58202ba3372795aa28fd6e4ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalNodeNetworkConfigs", [value]))

    @jsii.member(jsii_name="putAdditionalPodNetworkConfigs")
    def put_additional_pod_network_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28f5e053221540ee1582db2d5317c2cc285bfdf255146923f44ad3a210caff3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalPodNetworkConfigs", [value]))

    @jsii.member(jsii_name="putNetworkPerformanceConfig")
    def put_network_performance_config(
        self,
        *,
        total_egress_bandwidth_tier: builtins.str,
    ) -> None:
        '''
        :param total_egress_bandwidth_tier: Specifies the total network bandwidth tier for the NodePool. `Valid values <https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters.nodePools#NodePool.Tier>`_ include: "TIER_1" and "TIER_UNSPECIFIED". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#total_egress_bandwidth_tier ContainerNodePool#total_egress_bandwidth_tier}
        '''
        value = ContainerNodePoolNetworkConfigNetworkPerformanceConfig(
            total_egress_bandwidth_tier=total_egress_bandwidth_tier
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkPerformanceConfig", [value]))

    @jsii.member(jsii_name="putPodCidrOverprovisionConfig")
    def put_pod_cidr_overprovision_config(
        self,
        *,
        disabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#disabled ContainerNodePool#disabled}.
        '''
        value = ContainerNodePoolNetworkConfigPodCidrOverprovisionConfig(
            disabled=disabled
        )

        return typing.cast(None, jsii.invoke(self, "putPodCidrOverprovisionConfig", [value]))

    @jsii.member(jsii_name="resetAdditionalNodeNetworkConfigs")
    def reset_additional_node_network_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalNodeNetworkConfigs", []))

    @jsii.member(jsii_name="resetAdditionalPodNetworkConfigs")
    def reset_additional_pod_network_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalPodNetworkConfigs", []))

    @jsii.member(jsii_name="resetCreatePodRange")
    def reset_create_pod_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreatePodRange", []))

    @jsii.member(jsii_name="resetEnablePrivateNodes")
    def reset_enable_private_nodes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnablePrivateNodes", []))

    @jsii.member(jsii_name="resetNetworkPerformanceConfig")
    def reset_network_performance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkPerformanceConfig", []))

    @jsii.member(jsii_name="resetPodCidrOverprovisionConfig")
    def reset_pod_cidr_overprovision_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPodCidrOverprovisionConfig", []))

    @jsii.member(jsii_name="resetPodIpv4CidrBlock")
    def reset_pod_ipv4_cidr_block(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPodIpv4CidrBlock", []))

    @jsii.member(jsii_name="resetPodRange")
    def reset_pod_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPodRange", []))

    @builtins.property
    @jsii.member(jsii_name="additionalNodeNetworkConfigs")
    def additional_node_network_configs(
        self,
    ) -> ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigsList:
        return typing.cast(ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigsList, jsii.get(self, "additionalNodeNetworkConfigs"))

    @builtins.property
    @jsii.member(jsii_name="additionalPodNetworkConfigs")
    def additional_pod_network_configs(
        self,
    ) -> ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigsList:
        return typing.cast(ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigsList, jsii.get(self, "additionalPodNetworkConfigs"))

    @builtins.property
    @jsii.member(jsii_name="networkPerformanceConfig")
    def network_performance_config(
        self,
    ) -> ContainerNodePoolNetworkConfigNetworkPerformanceConfigOutputReference:
        return typing.cast(ContainerNodePoolNetworkConfigNetworkPerformanceConfigOutputReference, jsii.get(self, "networkPerformanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="podCidrOverprovisionConfig")
    def pod_cidr_overprovision_config(
        self,
    ) -> "ContainerNodePoolNetworkConfigPodCidrOverprovisionConfigOutputReference":
        return typing.cast("ContainerNodePoolNetworkConfigPodCidrOverprovisionConfigOutputReference", jsii.get(self, "podCidrOverprovisionConfig"))

    @builtins.property
    @jsii.member(jsii_name="additionalNodeNetworkConfigsInput")
    def additional_node_network_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs]]], jsii.get(self, "additionalNodeNetworkConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalPodNetworkConfigsInput")
    def additional_pod_network_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs]]], jsii.get(self, "additionalPodNetworkConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="createPodRangeInput")
    def create_pod_range_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "createPodRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="enablePrivateNodesInput")
    def enable_private_nodes_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enablePrivateNodesInput"))

    @builtins.property
    @jsii.member(jsii_name="networkPerformanceConfigInput")
    def network_performance_config_input(
        self,
    ) -> typing.Optional[ContainerNodePoolNetworkConfigNetworkPerformanceConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNetworkConfigNetworkPerformanceConfig], jsii.get(self, "networkPerformanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="podCidrOverprovisionConfigInput")
    def pod_cidr_overprovision_config_input(
        self,
    ) -> typing.Optional["ContainerNodePoolNetworkConfigPodCidrOverprovisionConfig"]:
        return typing.cast(typing.Optional["ContainerNodePoolNetworkConfigPodCidrOverprovisionConfig"], jsii.get(self, "podCidrOverprovisionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="podIpv4CidrBlockInput")
    def pod_ipv4_cidr_block_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "podIpv4CidrBlockInput"))

    @builtins.property
    @jsii.member(jsii_name="podRangeInput")
    def pod_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "podRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="createPodRange")
    def create_pod_range(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "createPodRange"))

    @create_pod_range.setter
    def create_pod_range(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b40fb1a0c346aca2b9adbfde60f56535afea1df971989773e0db9c6cefe53356)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createPodRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enablePrivateNodes")
    def enable_private_nodes(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enablePrivateNodes"))

    @enable_private_nodes.setter
    def enable_private_nodes(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__528fb63d4d6169e7fa67df8f888d1fd44a44ef2c0d4cb966d96e9fb955239779)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePrivateNodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="podIpv4CidrBlock")
    def pod_ipv4_cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "podIpv4CidrBlock"))

    @pod_ipv4_cidr_block.setter
    def pod_ipv4_cidr_block(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__172b5c507d7e298ab85834814ed79ff08b9617c08c3de11d6a39347af79879dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podIpv4CidrBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="podRange")
    def pod_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "podRange"))

    @pod_range.setter
    def pod_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec56e0a274f5b2b5ab75b952d082c8d6d1dc6e260b393a2e8a81b4ebe717f3e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerNodePoolNetworkConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8714794ad9790eb27d91aa38324158abbc781fb67e5de4fe75e1544ea78a37de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNetworkConfigPodCidrOverprovisionConfig",
    jsii_struct_bases=[],
    name_mapping={"disabled": "disabled"},
)
class ContainerNodePoolNetworkConfigPodCidrOverprovisionConfig:
    def __init__(
        self,
        *,
        disabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#disabled ContainerNodePool#disabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__890b871384eeb45ea20d1c79149edeac85e821cf7fcc6444357184e6e0b5eaf5)
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disabled": disabled,
        }

    @builtins.property
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#disabled ContainerNodePool#disabled}.'''
        result = self._values.get("disabled")
        assert result is not None, "Required property 'disabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNetworkConfigPodCidrOverprovisionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNetworkConfigPodCidrOverprovisionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNetworkConfigPodCidrOverprovisionConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88e581d74ae383f5a43a53e034760dde37e84f25b80eeb81a29c653cd05692b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b85feb090b8737dc565b5d11f77461076520dc0704a315fae9844cdd2aca9eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerNodePoolNetworkConfigPodCidrOverprovisionConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNetworkConfigPodCidrOverprovisionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNetworkConfigPodCidrOverprovisionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__481f78751ef8774f0366ecb626e2cf5ec4c62949e27c3c57e91fa6723048281e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfig",
    jsii_struct_bases=[],
    name_mapping={
        "advanced_machine_features": "advancedMachineFeatures",
        "boot_disk_kms_key": "bootDiskKmsKey",
        "confidential_nodes": "confidentialNodes",
        "containerd_config": "containerdConfig",
        "disk_size_gb": "diskSizeGb",
        "disk_type": "diskType",
        "enable_confidential_storage": "enableConfidentialStorage",
        "ephemeral_storage_local_ssd_config": "ephemeralStorageLocalSsdConfig",
        "fast_socket": "fastSocket",
        "flex_start": "flexStart",
        "gcfs_config": "gcfsConfig",
        "guest_accelerator": "guestAccelerator",
        "gvnic": "gvnic",
        "host_maintenance_policy": "hostMaintenancePolicy",
        "image_type": "imageType",
        "kubelet_config": "kubeletConfig",
        "labels": "labels",
        "linux_node_config": "linuxNodeConfig",
        "local_nvme_ssd_block_config": "localNvmeSsdBlockConfig",
        "local_ssd_count": "localSsdCount",
        "local_ssd_encryption_mode": "localSsdEncryptionMode",
        "logging_variant": "loggingVariant",
        "machine_type": "machineType",
        "max_run_duration": "maxRunDuration",
        "metadata": "metadata",
        "min_cpu_platform": "minCpuPlatform",
        "node_group": "nodeGroup",
        "oauth_scopes": "oauthScopes",
        "preemptible": "preemptible",
        "reservation_affinity": "reservationAffinity",
        "resource_labels": "resourceLabels",
        "resource_manager_tags": "resourceManagerTags",
        "secondary_boot_disks": "secondaryBootDisks",
        "service_account": "serviceAccount",
        "shielded_instance_config": "shieldedInstanceConfig",
        "sole_tenant_config": "soleTenantConfig",
        "spot": "spot",
        "storage_pools": "storagePools",
        "tags": "tags",
        "taint": "taint",
        "windows_node_config": "windowsNodeConfig",
        "workload_metadata_config": "workloadMetadataConfig",
    },
)
class ContainerNodePoolNodeConfig:
    def __init__(
        self,
        *,
        advanced_machine_features: typing.Optional[typing.Union["ContainerNodePoolNodeConfigAdvancedMachineFeatures", typing.Dict[builtins.str, typing.Any]]] = None,
        boot_disk_kms_key: typing.Optional[builtins.str] = None,
        confidential_nodes: typing.Optional[typing.Union["ContainerNodePoolNodeConfigConfidentialNodes", typing.Dict[builtins.str, typing.Any]]] = None,
        containerd_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigContainerdConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        disk_type: typing.Optional[builtins.str] = None,
        enable_confidential_storage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ephemeral_storage_local_ssd_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        fast_socket: typing.Optional[typing.Union["ContainerNodePoolNodeConfigFastSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        flex_start: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcfs_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigGcfsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        guest_accelerator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerNodePoolNodeConfigGuestAccelerator", typing.Dict[builtins.str, typing.Any]]]]] = None,
        gvnic: typing.Optional[typing.Union["ContainerNodePoolNodeConfigGvnic", typing.Dict[builtins.str, typing.Any]]] = None,
        host_maintenance_policy: typing.Optional[typing.Union["ContainerNodePoolNodeConfigHostMaintenancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        image_type: typing.Optional[builtins.str] = None,
        kubelet_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigKubeletConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        linux_node_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigLinuxNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        local_nvme_ssd_block_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        local_ssd_count: typing.Optional[jsii.Number] = None,
        local_ssd_encryption_mode: typing.Optional[builtins.str] = None,
        logging_variant: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        max_run_duration: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        node_group: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        preemptible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reservation_affinity: typing.Optional[typing.Union["ContainerNodePoolNodeConfigReservationAffinity", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        secondary_boot_disks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerNodePoolNodeConfigSecondaryBootDisks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_account: typing.Optional[builtins.str] = None,
        shielded_instance_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        sole_tenant_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigSoleTenantConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        storage_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        taint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerNodePoolNodeConfigTaint", typing.Dict[builtins.str, typing.Any]]]]] = None,
        windows_node_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigWindowsNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        workload_metadata_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigWorkloadMetadataConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_machine_features: advanced_machine_features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#advanced_machine_features ContainerNodePool#advanced_machine_features}
        :param boot_disk_kms_key: The Customer Managed Encryption Key used to encrypt the boot disk attached to each node in the node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#boot_disk_kms_key ContainerNodePool#boot_disk_kms_key}
        :param confidential_nodes: confidential_nodes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#confidential_nodes ContainerNodePool#confidential_nodes}
        :param containerd_config: containerd_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#containerd_config ContainerNodePool#containerd_config}
        :param disk_size_gb: Size of the disk attached to each node, specified in GB. The smallest allowed disk size is 10GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#disk_size_gb ContainerNodePool#disk_size_gb}
        :param disk_type: Type of the disk attached to each node. Such as pd-standard, pd-balanced or pd-ssd. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#disk_type ContainerNodePool#disk_type}
        :param enable_confidential_storage: If enabled boot disks are configured with confidential mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enable_confidential_storage ContainerNodePool#enable_confidential_storage}
        :param ephemeral_storage_local_ssd_config: ephemeral_storage_local_ssd_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#ephemeral_storage_local_ssd_config ContainerNodePool#ephemeral_storage_local_ssd_config}
        :param fast_socket: fast_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#fast_socket ContainerNodePool#fast_socket}
        :param flex_start: Enables Flex Start provisioning model for the node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#flex_start ContainerNodePool#flex_start}
        :param gcfs_config: gcfs_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#gcfs_config ContainerNodePool#gcfs_config}
        :param guest_accelerator: guest_accelerator block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#guest_accelerator ContainerNodePool#guest_accelerator}
        :param gvnic: gvnic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#gvnic ContainerNodePool#gvnic}
        :param host_maintenance_policy: host_maintenance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#host_maintenance_policy ContainerNodePool#host_maintenance_policy}
        :param image_type: The image type to use for this node. Note that for a given image type, the latest version of it will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#image_type ContainerNodePool#image_type}
        :param kubelet_config: kubelet_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#kubelet_config ContainerNodePool#kubelet_config}
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#labels ContainerNodePool#labels}
        :param linux_node_config: linux_node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#linux_node_config ContainerNodePool#linux_node_config}
        :param local_nvme_ssd_block_config: local_nvme_ssd_block_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#local_nvme_ssd_block_config ContainerNodePool#local_nvme_ssd_block_config}
        :param local_ssd_count: The number of local SSD disks to be attached to the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#local_ssd_count ContainerNodePool#local_ssd_count}
        :param local_ssd_encryption_mode: LocalSsdEncryptionMode specified the method used for encrypting the local SSDs attached to the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#local_ssd_encryption_mode ContainerNodePool#local_ssd_encryption_mode}
        :param logging_variant: Type of logging agent that is used as the default value for node pools in the cluster. Valid values include DEFAULT and MAX_THROUGHPUT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#logging_variant ContainerNodePool#logging_variant}
        :param machine_type: The name of a Google Compute Engine machine type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#machine_type ContainerNodePool#machine_type}
        :param max_run_duration: The runtime of each node in the node pool in seconds, terminated by 's'. Example: "3600s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#max_run_duration ContainerNodePool#max_run_duration}
        :param metadata: The metadata key/value pairs assigned to instances in the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#metadata ContainerNodePool#metadata}
        :param min_cpu_platform: Minimum CPU platform to be used by this instance. The instance may be scheduled on the specified or newer CPU platform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#min_cpu_platform ContainerNodePool#min_cpu_platform}
        :param node_group: Setting this field will assign instances of this pool to run on the specified node group. This is useful for running workloads on sole tenant nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#node_group ContainerNodePool#node_group}
        :param oauth_scopes: The set of Google API scopes to be made available on all of the node VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#oauth_scopes ContainerNodePool#oauth_scopes}
        :param preemptible: Whether the nodes are created as preemptible VM instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#preemptible ContainerNodePool#preemptible}
        :param reservation_affinity: reservation_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#reservation_affinity ContainerNodePool#reservation_affinity}
        :param resource_labels: The GCE resource labels (a map of key/value pairs) to be applied to the node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#resource_labels ContainerNodePool#resource_labels}
        :param resource_manager_tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#resource_manager_tags ContainerNodePool#resource_manager_tags}
        :param secondary_boot_disks: secondary_boot_disks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#secondary_boot_disks ContainerNodePool#secondary_boot_disks}
        :param service_account: The Google Cloud Platform Service Account to be used by the node VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#service_account ContainerNodePool#service_account}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#shielded_instance_config ContainerNodePool#shielded_instance_config}
        :param sole_tenant_config: sole_tenant_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#sole_tenant_config ContainerNodePool#sole_tenant_config}
        :param spot: Whether the nodes are created as spot VM instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#spot ContainerNodePool#spot}
        :param storage_pools: The list of Storage Pools where boot disks are provisioned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#storage_pools ContainerNodePool#storage_pools}
        :param tags: The list of instance tags applied to all nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#tags ContainerNodePool#tags}
        :param taint: taint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#taint ContainerNodePool#taint}
        :param windows_node_config: windows_node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#windows_node_config ContainerNodePool#windows_node_config}
        :param workload_metadata_config: workload_metadata_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#workload_metadata_config ContainerNodePool#workload_metadata_config}
        '''
        if isinstance(advanced_machine_features, dict):
            advanced_machine_features = ContainerNodePoolNodeConfigAdvancedMachineFeatures(**advanced_machine_features)
        if isinstance(confidential_nodes, dict):
            confidential_nodes = ContainerNodePoolNodeConfigConfidentialNodes(**confidential_nodes)
        if isinstance(containerd_config, dict):
            containerd_config = ContainerNodePoolNodeConfigContainerdConfig(**containerd_config)
        if isinstance(ephemeral_storage_local_ssd_config, dict):
            ephemeral_storage_local_ssd_config = ContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig(**ephemeral_storage_local_ssd_config)
        if isinstance(fast_socket, dict):
            fast_socket = ContainerNodePoolNodeConfigFastSocket(**fast_socket)
        if isinstance(gcfs_config, dict):
            gcfs_config = ContainerNodePoolNodeConfigGcfsConfig(**gcfs_config)
        if isinstance(gvnic, dict):
            gvnic = ContainerNodePoolNodeConfigGvnic(**gvnic)
        if isinstance(host_maintenance_policy, dict):
            host_maintenance_policy = ContainerNodePoolNodeConfigHostMaintenancePolicy(**host_maintenance_policy)
        if isinstance(kubelet_config, dict):
            kubelet_config = ContainerNodePoolNodeConfigKubeletConfig(**kubelet_config)
        if isinstance(linux_node_config, dict):
            linux_node_config = ContainerNodePoolNodeConfigLinuxNodeConfig(**linux_node_config)
        if isinstance(local_nvme_ssd_block_config, dict):
            local_nvme_ssd_block_config = ContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig(**local_nvme_ssd_block_config)
        if isinstance(reservation_affinity, dict):
            reservation_affinity = ContainerNodePoolNodeConfigReservationAffinity(**reservation_affinity)
        if isinstance(shielded_instance_config, dict):
            shielded_instance_config = ContainerNodePoolNodeConfigShieldedInstanceConfig(**shielded_instance_config)
        if isinstance(sole_tenant_config, dict):
            sole_tenant_config = ContainerNodePoolNodeConfigSoleTenantConfig(**sole_tenant_config)
        if isinstance(windows_node_config, dict):
            windows_node_config = ContainerNodePoolNodeConfigWindowsNodeConfig(**windows_node_config)
        if isinstance(workload_metadata_config, dict):
            workload_metadata_config = ContainerNodePoolNodeConfigWorkloadMetadataConfig(**workload_metadata_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__624d8a32216c09560115f6cfc0618bf44f0ee63f0c7cda1fb3cbe56171e3c79b)
            check_type(argname="argument advanced_machine_features", value=advanced_machine_features, expected_type=type_hints["advanced_machine_features"])
            check_type(argname="argument boot_disk_kms_key", value=boot_disk_kms_key, expected_type=type_hints["boot_disk_kms_key"])
            check_type(argname="argument confidential_nodes", value=confidential_nodes, expected_type=type_hints["confidential_nodes"])
            check_type(argname="argument containerd_config", value=containerd_config, expected_type=type_hints["containerd_config"])
            check_type(argname="argument disk_size_gb", value=disk_size_gb, expected_type=type_hints["disk_size_gb"])
            check_type(argname="argument disk_type", value=disk_type, expected_type=type_hints["disk_type"])
            check_type(argname="argument enable_confidential_storage", value=enable_confidential_storage, expected_type=type_hints["enable_confidential_storage"])
            check_type(argname="argument ephemeral_storage_local_ssd_config", value=ephemeral_storage_local_ssd_config, expected_type=type_hints["ephemeral_storage_local_ssd_config"])
            check_type(argname="argument fast_socket", value=fast_socket, expected_type=type_hints["fast_socket"])
            check_type(argname="argument flex_start", value=flex_start, expected_type=type_hints["flex_start"])
            check_type(argname="argument gcfs_config", value=gcfs_config, expected_type=type_hints["gcfs_config"])
            check_type(argname="argument guest_accelerator", value=guest_accelerator, expected_type=type_hints["guest_accelerator"])
            check_type(argname="argument gvnic", value=gvnic, expected_type=type_hints["gvnic"])
            check_type(argname="argument host_maintenance_policy", value=host_maintenance_policy, expected_type=type_hints["host_maintenance_policy"])
            check_type(argname="argument image_type", value=image_type, expected_type=type_hints["image_type"])
            check_type(argname="argument kubelet_config", value=kubelet_config, expected_type=type_hints["kubelet_config"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument linux_node_config", value=linux_node_config, expected_type=type_hints["linux_node_config"])
            check_type(argname="argument local_nvme_ssd_block_config", value=local_nvme_ssd_block_config, expected_type=type_hints["local_nvme_ssd_block_config"])
            check_type(argname="argument local_ssd_count", value=local_ssd_count, expected_type=type_hints["local_ssd_count"])
            check_type(argname="argument local_ssd_encryption_mode", value=local_ssd_encryption_mode, expected_type=type_hints["local_ssd_encryption_mode"])
            check_type(argname="argument logging_variant", value=logging_variant, expected_type=type_hints["logging_variant"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument max_run_duration", value=max_run_duration, expected_type=type_hints["max_run_duration"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument min_cpu_platform", value=min_cpu_platform, expected_type=type_hints["min_cpu_platform"])
            check_type(argname="argument node_group", value=node_group, expected_type=type_hints["node_group"])
            check_type(argname="argument oauth_scopes", value=oauth_scopes, expected_type=type_hints["oauth_scopes"])
            check_type(argname="argument preemptible", value=preemptible, expected_type=type_hints["preemptible"])
            check_type(argname="argument reservation_affinity", value=reservation_affinity, expected_type=type_hints["reservation_affinity"])
            check_type(argname="argument resource_labels", value=resource_labels, expected_type=type_hints["resource_labels"])
            check_type(argname="argument resource_manager_tags", value=resource_manager_tags, expected_type=type_hints["resource_manager_tags"])
            check_type(argname="argument secondary_boot_disks", value=secondary_boot_disks, expected_type=type_hints["secondary_boot_disks"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument shielded_instance_config", value=shielded_instance_config, expected_type=type_hints["shielded_instance_config"])
            check_type(argname="argument sole_tenant_config", value=sole_tenant_config, expected_type=type_hints["sole_tenant_config"])
            check_type(argname="argument spot", value=spot, expected_type=type_hints["spot"])
            check_type(argname="argument storage_pools", value=storage_pools, expected_type=type_hints["storage_pools"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument taint", value=taint, expected_type=type_hints["taint"])
            check_type(argname="argument windows_node_config", value=windows_node_config, expected_type=type_hints["windows_node_config"])
            check_type(argname="argument workload_metadata_config", value=workload_metadata_config, expected_type=type_hints["workload_metadata_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if advanced_machine_features is not None:
            self._values["advanced_machine_features"] = advanced_machine_features
        if boot_disk_kms_key is not None:
            self._values["boot_disk_kms_key"] = boot_disk_kms_key
        if confidential_nodes is not None:
            self._values["confidential_nodes"] = confidential_nodes
        if containerd_config is not None:
            self._values["containerd_config"] = containerd_config
        if disk_size_gb is not None:
            self._values["disk_size_gb"] = disk_size_gb
        if disk_type is not None:
            self._values["disk_type"] = disk_type
        if enable_confidential_storage is not None:
            self._values["enable_confidential_storage"] = enable_confidential_storage
        if ephemeral_storage_local_ssd_config is not None:
            self._values["ephemeral_storage_local_ssd_config"] = ephemeral_storage_local_ssd_config
        if fast_socket is not None:
            self._values["fast_socket"] = fast_socket
        if flex_start is not None:
            self._values["flex_start"] = flex_start
        if gcfs_config is not None:
            self._values["gcfs_config"] = gcfs_config
        if guest_accelerator is not None:
            self._values["guest_accelerator"] = guest_accelerator
        if gvnic is not None:
            self._values["gvnic"] = gvnic
        if host_maintenance_policy is not None:
            self._values["host_maintenance_policy"] = host_maintenance_policy
        if image_type is not None:
            self._values["image_type"] = image_type
        if kubelet_config is not None:
            self._values["kubelet_config"] = kubelet_config
        if labels is not None:
            self._values["labels"] = labels
        if linux_node_config is not None:
            self._values["linux_node_config"] = linux_node_config
        if local_nvme_ssd_block_config is not None:
            self._values["local_nvme_ssd_block_config"] = local_nvme_ssd_block_config
        if local_ssd_count is not None:
            self._values["local_ssd_count"] = local_ssd_count
        if local_ssd_encryption_mode is not None:
            self._values["local_ssd_encryption_mode"] = local_ssd_encryption_mode
        if logging_variant is not None:
            self._values["logging_variant"] = logging_variant
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if max_run_duration is not None:
            self._values["max_run_duration"] = max_run_duration
        if metadata is not None:
            self._values["metadata"] = metadata
        if min_cpu_platform is not None:
            self._values["min_cpu_platform"] = min_cpu_platform
        if node_group is not None:
            self._values["node_group"] = node_group
        if oauth_scopes is not None:
            self._values["oauth_scopes"] = oauth_scopes
        if preemptible is not None:
            self._values["preemptible"] = preemptible
        if reservation_affinity is not None:
            self._values["reservation_affinity"] = reservation_affinity
        if resource_labels is not None:
            self._values["resource_labels"] = resource_labels
        if resource_manager_tags is not None:
            self._values["resource_manager_tags"] = resource_manager_tags
        if secondary_boot_disks is not None:
            self._values["secondary_boot_disks"] = secondary_boot_disks
        if service_account is not None:
            self._values["service_account"] = service_account
        if shielded_instance_config is not None:
            self._values["shielded_instance_config"] = shielded_instance_config
        if sole_tenant_config is not None:
            self._values["sole_tenant_config"] = sole_tenant_config
        if spot is not None:
            self._values["spot"] = spot
        if storage_pools is not None:
            self._values["storage_pools"] = storage_pools
        if tags is not None:
            self._values["tags"] = tags
        if taint is not None:
            self._values["taint"] = taint
        if windows_node_config is not None:
            self._values["windows_node_config"] = windows_node_config
        if workload_metadata_config is not None:
            self._values["workload_metadata_config"] = workload_metadata_config

    @builtins.property
    def advanced_machine_features(
        self,
    ) -> typing.Optional["ContainerNodePoolNodeConfigAdvancedMachineFeatures"]:
        '''advanced_machine_features block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#advanced_machine_features ContainerNodePool#advanced_machine_features}
        '''
        result = self._values.get("advanced_machine_features")
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigAdvancedMachineFeatures"], result)

    @builtins.property
    def boot_disk_kms_key(self) -> typing.Optional[builtins.str]:
        '''The Customer Managed Encryption Key used to encrypt the boot disk attached to each node in the node pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#boot_disk_kms_key ContainerNodePool#boot_disk_kms_key}
        '''
        result = self._values.get("boot_disk_kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def confidential_nodes(
        self,
    ) -> typing.Optional["ContainerNodePoolNodeConfigConfidentialNodes"]:
        '''confidential_nodes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#confidential_nodes ContainerNodePool#confidential_nodes}
        '''
        result = self._values.get("confidential_nodes")
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigConfidentialNodes"], result)

    @builtins.property
    def containerd_config(
        self,
    ) -> typing.Optional["ContainerNodePoolNodeConfigContainerdConfig"]:
        '''containerd_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#containerd_config ContainerNodePool#containerd_config}
        '''
        result = self._values.get("containerd_config")
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigContainerdConfig"], result)

    @builtins.property
    def disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Size of the disk attached to each node, specified in GB. The smallest allowed disk size is 10GB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#disk_size_gb ContainerNodePool#disk_size_gb}
        '''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_type(self) -> typing.Optional[builtins.str]:
        '''Type of the disk attached to each node. Such as pd-standard, pd-balanced or pd-ssd.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#disk_type ContainerNodePool#disk_type}
        '''
        result = self._values.get("disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_confidential_storage(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If enabled boot disks are configured with confidential mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enable_confidential_storage ContainerNodePool#enable_confidential_storage}
        '''
        result = self._values.get("enable_confidential_storage")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ephemeral_storage_local_ssd_config(
        self,
    ) -> typing.Optional["ContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig"]:
        '''ephemeral_storage_local_ssd_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#ephemeral_storage_local_ssd_config ContainerNodePool#ephemeral_storage_local_ssd_config}
        '''
        result = self._values.get("ephemeral_storage_local_ssd_config")
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig"], result)

    @builtins.property
    def fast_socket(self) -> typing.Optional["ContainerNodePoolNodeConfigFastSocket"]:
        '''fast_socket block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#fast_socket ContainerNodePool#fast_socket}
        '''
        result = self._values.get("fast_socket")
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigFastSocket"], result)

    @builtins.property
    def flex_start(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables Flex Start provisioning model for the node pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#flex_start ContainerNodePool#flex_start}
        '''
        result = self._values.get("flex_start")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcfs_config(self) -> typing.Optional["ContainerNodePoolNodeConfigGcfsConfig"]:
        '''gcfs_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#gcfs_config ContainerNodePool#gcfs_config}
        '''
        result = self._values.get("gcfs_config")
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigGcfsConfig"], result)

    @builtins.property
    def guest_accelerator(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerNodePoolNodeConfigGuestAccelerator"]]]:
        '''guest_accelerator block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#guest_accelerator ContainerNodePool#guest_accelerator}
        '''
        result = self._values.get("guest_accelerator")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerNodePoolNodeConfigGuestAccelerator"]]], result)

    @builtins.property
    def gvnic(self) -> typing.Optional["ContainerNodePoolNodeConfigGvnic"]:
        '''gvnic block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#gvnic ContainerNodePool#gvnic}
        '''
        result = self._values.get("gvnic")
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigGvnic"], result)

    @builtins.property
    def host_maintenance_policy(
        self,
    ) -> typing.Optional["ContainerNodePoolNodeConfigHostMaintenancePolicy"]:
        '''host_maintenance_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#host_maintenance_policy ContainerNodePool#host_maintenance_policy}
        '''
        result = self._values.get("host_maintenance_policy")
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigHostMaintenancePolicy"], result)

    @builtins.property
    def image_type(self) -> typing.Optional[builtins.str]:
        '''The image type to use for this node.

        Note that for a given image type, the latest version of it will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#image_type ContainerNodePool#image_type}
        '''
        result = self._values.get("image_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kubelet_config(
        self,
    ) -> typing.Optional["ContainerNodePoolNodeConfigKubeletConfig"]:
        '''kubelet_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#kubelet_config ContainerNodePool#kubelet_config}
        '''
        result = self._values.get("kubelet_config")
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigKubeletConfig"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The map of Kubernetes labels (key/value pairs) to be applied to each node.

        These will added in addition to any default label(s) that Kubernetes may apply to the node.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#labels ContainerNodePool#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def linux_node_config(
        self,
    ) -> typing.Optional["ContainerNodePoolNodeConfigLinuxNodeConfig"]:
        '''linux_node_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#linux_node_config ContainerNodePool#linux_node_config}
        '''
        result = self._values.get("linux_node_config")
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigLinuxNodeConfig"], result)

    @builtins.property
    def local_nvme_ssd_block_config(
        self,
    ) -> typing.Optional["ContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig"]:
        '''local_nvme_ssd_block_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#local_nvme_ssd_block_config ContainerNodePool#local_nvme_ssd_block_config}
        '''
        result = self._values.get("local_nvme_ssd_block_config")
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig"], result)

    @builtins.property
    def local_ssd_count(self) -> typing.Optional[jsii.Number]:
        '''The number of local SSD disks to be attached to the node.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#local_ssd_count ContainerNodePool#local_ssd_count}
        '''
        result = self._values.get("local_ssd_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def local_ssd_encryption_mode(self) -> typing.Optional[builtins.str]:
        '''LocalSsdEncryptionMode specified the method used for encrypting the local SSDs attached to the node.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#local_ssd_encryption_mode ContainerNodePool#local_ssd_encryption_mode}
        '''
        result = self._values.get("local_ssd_encryption_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_variant(self) -> typing.Optional[builtins.str]:
        '''Type of logging agent that is used as the default value for node pools in the cluster.

        Valid values include DEFAULT and MAX_THROUGHPUT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#logging_variant ContainerNodePool#logging_variant}
        '''
        result = self._values.get("logging_variant")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The name of a Google Compute Engine machine type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#machine_type ContainerNodePool#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_run_duration(self) -> typing.Optional[builtins.str]:
        '''The runtime of each node in the node pool in seconds, terminated by 's'. Example: "3600s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#max_run_duration ContainerNodePool#max_run_duration}
        '''
        result = self._values.get("max_run_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The metadata key/value pairs assigned to instances in the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#metadata ContainerNodePool#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def min_cpu_platform(self) -> typing.Optional[builtins.str]:
        '''Minimum CPU platform to be used by this instance.

        The instance may be scheduled on the specified or newer CPU platform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#min_cpu_platform ContainerNodePool#min_cpu_platform}
        '''
        result = self._values.get("min_cpu_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_group(self) -> typing.Optional[builtins.str]:
        '''Setting this field will assign instances of this pool to run on the specified node group.

        This is useful for running workloads on sole tenant nodes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#node_group ContainerNodePool#node_group}
        '''
        result = self._values.get("node_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of Google API scopes to be made available on all of the node VMs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#oauth_scopes ContainerNodePool#oauth_scopes}
        '''
        result = self._values.get("oauth_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def preemptible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the nodes are created as preemptible VM instances.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#preemptible ContainerNodePool#preemptible}
        '''
        result = self._values.get("preemptible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def reservation_affinity(
        self,
    ) -> typing.Optional["ContainerNodePoolNodeConfigReservationAffinity"]:
        '''reservation_affinity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#reservation_affinity ContainerNodePool#reservation_affinity}
        '''
        result = self._values.get("reservation_affinity")
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigReservationAffinity"], result)

    @builtins.property
    def resource_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The GCE resource labels (a map of key/value pairs) to be applied to the node pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#resource_labels ContainerNodePool#resource_labels}
        '''
        result = self._values.get("resource_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def resource_manager_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of resource manager tags.

        Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#resource_manager_tags ContainerNodePool#resource_manager_tags}
        '''
        result = self._values.get("resource_manager_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def secondary_boot_disks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerNodePoolNodeConfigSecondaryBootDisks"]]]:
        '''secondary_boot_disks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#secondary_boot_disks ContainerNodePool#secondary_boot_disks}
        '''
        result = self._values.get("secondary_boot_disks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerNodePoolNodeConfigSecondaryBootDisks"]]], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''The Google Cloud Platform Service Account to be used by the node VMs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#service_account ContainerNodePool#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shielded_instance_config(
        self,
    ) -> typing.Optional["ContainerNodePoolNodeConfigShieldedInstanceConfig"]:
        '''shielded_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#shielded_instance_config ContainerNodePool#shielded_instance_config}
        '''
        result = self._values.get("shielded_instance_config")
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigShieldedInstanceConfig"], result)

    @builtins.property
    def sole_tenant_config(
        self,
    ) -> typing.Optional["ContainerNodePoolNodeConfigSoleTenantConfig"]:
        '''sole_tenant_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#sole_tenant_config ContainerNodePool#sole_tenant_config}
        '''
        result = self._values.get("sole_tenant_config")
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigSoleTenantConfig"], result)

    @builtins.property
    def spot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the nodes are created as spot VM instances.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#spot ContainerNodePool#spot}
        '''
        result = self._values.get("spot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def storage_pools(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of Storage Pools where boot disks are provisioned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#storage_pools ContainerNodePool#storage_pools}
        '''
        result = self._values.get("storage_pools")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of instance tags applied to all nodes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#tags ContainerNodePool#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def taint(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerNodePoolNodeConfigTaint"]]]:
        '''taint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#taint ContainerNodePool#taint}
        '''
        result = self._values.get("taint")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerNodePoolNodeConfigTaint"]]], result)

    @builtins.property
    def windows_node_config(
        self,
    ) -> typing.Optional["ContainerNodePoolNodeConfigWindowsNodeConfig"]:
        '''windows_node_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#windows_node_config ContainerNodePool#windows_node_config}
        '''
        result = self._values.get("windows_node_config")
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigWindowsNodeConfig"], result)

    @builtins.property
    def workload_metadata_config(
        self,
    ) -> typing.Optional["ContainerNodePoolNodeConfigWorkloadMetadataConfig"]:
        '''workload_metadata_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#workload_metadata_config ContainerNodePool#workload_metadata_config}
        '''
        result = self._values.get("workload_metadata_config")
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigWorkloadMetadataConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigAdvancedMachineFeatures",
    jsii_struct_bases=[],
    name_mapping={
        "threads_per_core": "threadsPerCore",
        "enable_nested_virtualization": "enableNestedVirtualization",
        "performance_monitoring_unit": "performanceMonitoringUnit",
    },
)
class ContainerNodePoolNodeConfigAdvancedMachineFeatures:
    def __init__(
        self,
        *,
        threads_per_core: jsii.Number,
        enable_nested_virtualization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        performance_monitoring_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param threads_per_core: The number of threads per physical core. To disable simultaneous multithreading (SMT) set this to 1. If unset, the maximum number of threads supported per core by the underlying processor is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#threads_per_core ContainerNodePool#threads_per_core}
        :param enable_nested_virtualization: Whether the node should have nested virtualization enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enable_nested_virtualization ContainerNodePool#enable_nested_virtualization}
        :param performance_monitoring_unit: Level of Performance Monitoring Unit (PMU) requested. If unset, no access to the PMU is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#performance_monitoring_unit ContainerNodePool#performance_monitoring_unit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__038c9a601363c15f56828a2ec1f0acc6f1ca14f133f87347af706e5541fd32f7)
            check_type(argname="argument threads_per_core", value=threads_per_core, expected_type=type_hints["threads_per_core"])
            check_type(argname="argument enable_nested_virtualization", value=enable_nested_virtualization, expected_type=type_hints["enable_nested_virtualization"])
            check_type(argname="argument performance_monitoring_unit", value=performance_monitoring_unit, expected_type=type_hints["performance_monitoring_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threads_per_core": threads_per_core,
        }
        if enable_nested_virtualization is not None:
            self._values["enable_nested_virtualization"] = enable_nested_virtualization
        if performance_monitoring_unit is not None:
            self._values["performance_monitoring_unit"] = performance_monitoring_unit

    @builtins.property
    def threads_per_core(self) -> jsii.Number:
        '''The number of threads per physical core.

        To disable simultaneous multithreading (SMT) set this to 1. If unset, the maximum number of threads supported per core by the underlying processor is assumed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#threads_per_core ContainerNodePool#threads_per_core}
        '''
        result = self._values.get("threads_per_core")
        assert result is not None, "Required property 'threads_per_core' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def enable_nested_virtualization(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the node should have nested virtualization enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enable_nested_virtualization ContainerNodePool#enable_nested_virtualization}
        '''
        result = self._values.get("enable_nested_virtualization")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def performance_monitoring_unit(self) -> typing.Optional[builtins.str]:
        '''Level of Performance Monitoring Unit (PMU) requested. If unset, no access to the PMU is assumed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#performance_monitoring_unit ContainerNodePool#performance_monitoring_unit}
        '''
        result = self._values.get("performance_monitoring_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigAdvancedMachineFeatures(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNodeConfigAdvancedMachineFeaturesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigAdvancedMachineFeaturesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b776be47e4d205ee48c9df6fad4c572f588bf9073ea871ba6f03462b8dbad9b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableNestedVirtualization")
    def reset_enable_nested_virtualization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableNestedVirtualization", []))

    @jsii.member(jsii_name="resetPerformanceMonitoringUnit")
    def reset_performance_monitoring_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerformanceMonitoringUnit", []))

    @builtins.property
    @jsii.member(jsii_name="enableNestedVirtualizationInput")
    def enable_nested_virtualization_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableNestedVirtualizationInput"))

    @builtins.property
    @jsii.member(jsii_name="performanceMonitoringUnitInput")
    def performance_monitoring_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "performanceMonitoringUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="threadsPerCoreInput")
    def threads_per_core_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "threadsPerCoreInput"))

    @builtins.property
    @jsii.member(jsii_name="enableNestedVirtualization")
    def enable_nested_virtualization(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableNestedVirtualization"))

    @enable_nested_virtualization.setter
    def enable_nested_virtualization(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ce9ed59586826e09734ebd9a2d76ed08602388f61a3203ff1ccbc34cea58880)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableNestedVirtualization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="performanceMonitoringUnit")
    def performance_monitoring_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "performanceMonitoringUnit"))

    @performance_monitoring_unit.setter
    def performance_monitoring_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a6c9d768855b5d8b6bd661ec7867e99c52dd072d664dbad3a15e16965fe26eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "performanceMonitoringUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threadsPerCore")
    def threads_per_core(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threadsPerCore"))

    @threads_per_core.setter
    def threads_per_core(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__259a5cba4783ff49952961d10f9bbdafd504d401e8d4d127ba17b5e243749623)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threadsPerCore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigAdvancedMachineFeatures]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigAdvancedMachineFeatures], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNodeConfigAdvancedMachineFeatures],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3397beb08baba0d69b29f5a5fb9261ce9cdc3ec775f69e81a3df61019bc61012)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigConfidentialNodes",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "confidential_instance_type": "confidentialInstanceType",
    },
)
class ContainerNodePoolNodeConfigConfidentialNodes:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        confidential_instance_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Whether Confidential Nodes feature is enabled for all nodes in this pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enabled ContainerNodePool#enabled}
        :param confidential_instance_type: Defines the type of technology used by the confidential node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#confidential_instance_type ContainerNodePool#confidential_instance_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53cf282a7b3f4c3213a1bc296099aa561d6d1817aa9bab22dfd52c6e8ff5b6f)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument confidential_instance_type", value=confidential_instance_type, expected_type=type_hints["confidential_instance_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if confidential_instance_type is not None:
            self._values["confidential_instance_type"] = confidential_instance_type

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether Confidential Nodes feature is enabled for all nodes in this pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enabled ContainerNodePool#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def confidential_instance_type(self) -> typing.Optional[builtins.str]:
        '''Defines the type of technology used by the confidential node.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#confidential_instance_type ContainerNodePool#confidential_instance_type}
        '''
        result = self._values.get("confidential_instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigConfidentialNodes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNodeConfigConfidentialNodesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigConfidentialNodesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54a587c32028e5f9335bbaee76d49254f74e77218dfacd732a02b3877cd35791)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConfidentialInstanceType")
    def reset_confidential_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidentialInstanceType", []))

    @builtins.property
    @jsii.member(jsii_name="confidentialInstanceTypeInput")
    def confidential_instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "confidentialInstanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="confidentialInstanceType")
    def confidential_instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "confidentialInstanceType"))

    @confidential_instance_type.setter
    def confidential_instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdffc30842d1e257dcae60fa6e4b2e6e4158aa96cd4def10a8ee650b16c45121)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidentialInstanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c284f960bf7442577bde1bf5f257de525cd6b310ff86ba85149977f2a553cc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigConfidentialNodes]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigConfidentialNodes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNodeConfigConfidentialNodes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f26248a672e38fc7a005b32e7e860bea1c16035d28870c17f835435cc72dcd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigContainerdConfig",
    jsii_struct_bases=[],
    name_mapping={"private_registry_access_config": "privateRegistryAccessConfig"},
)
class ContainerNodePoolNodeConfigContainerdConfig:
    def __init__(
        self,
        *,
        private_registry_access_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param private_registry_access_config: private_registry_access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#private_registry_access_config ContainerNodePool#private_registry_access_config}
        '''
        if isinstance(private_registry_access_config, dict):
            private_registry_access_config = ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig(**private_registry_access_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b39740ebdba0837d3bb6a7350c163fbcdd461a01bd77216b0dd1c6c224037761)
            check_type(argname="argument private_registry_access_config", value=private_registry_access_config, expected_type=type_hints["private_registry_access_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if private_registry_access_config is not None:
            self._values["private_registry_access_config"] = private_registry_access_config

    @builtins.property
    def private_registry_access_config(
        self,
    ) -> typing.Optional["ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig"]:
        '''private_registry_access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#private_registry_access_config ContainerNodePool#private_registry_access_config}
        '''
        result = self._values.get("private_registry_access_config")
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigContainerdConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNodeConfigContainerdConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigContainerdConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79032424f0b58ff4f82e54fd9d4d8ff8bb151f2380b436fce03b63d60772a4a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPrivateRegistryAccessConfig")
    def put_private_registry_access_config(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        certificate_authority_domain_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Whether or not private registries are configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enabled ContainerNodePool#enabled}
        :param certificate_authority_domain_config: certificate_authority_domain_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#certificate_authority_domain_config ContainerNodePool#certificate_authority_domain_config}
        '''
        value = ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig(
            enabled=enabled,
            certificate_authority_domain_config=certificate_authority_domain_config,
        )

        return typing.cast(None, jsii.invoke(self, "putPrivateRegistryAccessConfig", [value]))

    @jsii.member(jsii_name="resetPrivateRegistryAccessConfig")
    def reset_private_registry_access_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateRegistryAccessConfig", []))

    @builtins.property
    @jsii.member(jsii_name="privateRegistryAccessConfig")
    def private_registry_access_config(
        self,
    ) -> "ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigOutputReference":
        return typing.cast("ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigOutputReference", jsii.get(self, "privateRegistryAccessConfig"))

    @builtins.property
    @jsii.member(jsii_name="privateRegistryAccessConfigInput")
    def private_registry_access_config_input(
        self,
    ) -> typing.Optional["ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig"]:
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig"], jsii.get(self, "privateRegistryAccessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigContainerdConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigContainerdConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNodeConfigContainerdConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4383bd4b8be9ac98fc10ce6ade69bba9c08d2f2523c3f951adee25c73175b8c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "certificate_authority_domain_config": "certificateAuthorityDomainConfig",
    },
)
class ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        certificate_authority_domain_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Whether or not private registries are configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enabled ContainerNodePool#enabled}
        :param certificate_authority_domain_config: certificate_authority_domain_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#certificate_authority_domain_config ContainerNodePool#certificate_authority_domain_config}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__985fc8f22cba01d24a1aee5fe9ec1ec35433262b68c887feee46093f8ad61945)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument certificate_authority_domain_config", value=certificate_authority_domain_config, expected_type=type_hints["certificate_authority_domain_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if certificate_authority_domain_config is not None:
            self._values["certificate_authority_domain_config"] = certificate_authority_domain_config

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether or not private registries are configured.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enabled ContainerNodePool#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def certificate_authority_domain_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig"]]]:
        '''certificate_authority_domain_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#certificate_authority_domain_config ContainerNodePool#certificate_authority_domain_config}
        '''
        result = self._values.get("certificate_authority_domain_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig",
    jsii_struct_bases=[],
    name_mapping={
        "fqdns": "fqdns",
        "gcp_secret_manager_certificate_config": "gcpSecretManagerCertificateConfig",
    },
)
class ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig:
    def __init__(
        self,
        *,
        fqdns: typing.Sequence[builtins.str],
        gcp_secret_manager_certificate_config: typing.Union["ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param fqdns: List of fully-qualified-domain-names. IPv4s and port specification are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#fqdns ContainerNodePool#fqdns}
        :param gcp_secret_manager_certificate_config: gcp_secret_manager_certificate_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#gcp_secret_manager_certificate_config ContainerNodePool#gcp_secret_manager_certificate_config}
        '''
        if isinstance(gcp_secret_manager_certificate_config, dict):
            gcp_secret_manager_certificate_config = ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig(**gcp_secret_manager_certificate_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41b0a2f19b8428209e81064069a3f69953dd72a6fbd9818a2916b7c13e043a29)
            check_type(argname="argument fqdns", value=fqdns, expected_type=type_hints["fqdns"])
            check_type(argname="argument gcp_secret_manager_certificate_config", value=gcp_secret_manager_certificate_config, expected_type=type_hints["gcp_secret_manager_certificate_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fqdns": fqdns,
            "gcp_secret_manager_certificate_config": gcp_secret_manager_certificate_config,
        }

    @builtins.property
    def fqdns(self) -> typing.List[builtins.str]:
        '''List of fully-qualified-domain-names. IPv4s and port specification are supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#fqdns ContainerNodePool#fqdns}
        '''
        result = self._values.get("fqdns")
        assert result is not None, "Required property 'fqdns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def gcp_secret_manager_certificate_config(
        self,
    ) -> "ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig":
        '''gcp_secret_manager_certificate_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#gcp_secret_manager_certificate_config ContainerNodePool#gcp_secret_manager_certificate_config}
        '''
        result = self._values.get("gcp_secret_manager_certificate_config")
        assert result is not None, "Required property 'gcp_secret_manager_certificate_config' is missing"
        return typing.cast("ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig",
    jsii_struct_bases=[],
    name_mapping={"secret_uri": "secretUri"},
)
class ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig:
    def __init__(self, *, secret_uri: builtins.str) -> None:
        '''
        :param secret_uri: URI for the secret that hosts a certificate. Must be in the format 'projects/PROJECT_NUM/secrets/SECRET_NAME/versions/VERSION_OR_LATEST'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#secret_uri ContainerNodePool#secret_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8e49ef5dcf7472d653c4e8fe7a3e8349dd901f317ea2065ea1331638ca7d9fe)
            check_type(argname="argument secret_uri", value=secret_uri, expected_type=type_hints["secret_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_uri": secret_uri,
        }

    @builtins.property
    def secret_uri(self) -> builtins.str:
        '''URI for the secret that hosts a certificate. Must be in the format 'projects/PROJECT_NUM/secrets/SECRET_NAME/versions/VERSION_OR_LATEST'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#secret_uri ContainerNodePool#secret_uri}
        '''
        result = self._values.get("secret_uri")
        assert result is not None, "Required property 'secret_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96facd7ee5caa3dacbf05557106ad31e58471d6aa9ed508df3354525d2863e65)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretUriInput")
    def secret_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretUriInput"))

    @builtins.property
    @jsii.member(jsii_name="secretUri")
    def secret_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretUri"))

    @secret_uri.setter
    def secret_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__979231a8b125d11aebf4eead82887451cc2b7402f96307df519eaa8051c81896)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cefab438c5ad73bc78c4618643916312b5f3e72d0cbd96850130a1d95337e5b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e4310e1c887609f4b860533b6bc059e6b0c11ae5a5456dc88253b0aed2920fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c20009e1f3ff9fea3a7eb78fb4e792a41a1f10c4e7e61d22bfafb75013c544fc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f23467e33ef71fc03b0882c090bb65650bc984421b0c4d3989afd8751043b99a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c4b2ad127d461983c1210a9e76e785b67f64abd4f49684dba710754f67b8f54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46cb370e8f4f0cb47c5eb16c8fdd0af2564feaf182bd633de26c77d63cd4ca4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__605c447e174ce37d10a44e892bb7d8070d325963c6bb789a2dccfd958e1e588a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b837f51eccd3450c096b65c727b277aae54b4e0819beee34e246206a0fe4ce59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putGcpSecretManagerCertificateConfig")
    def put_gcp_secret_manager_certificate_config(
        self,
        *,
        secret_uri: builtins.str,
    ) -> None:
        '''
        :param secret_uri: URI for the secret that hosts a certificate. Must be in the format 'projects/PROJECT_NUM/secrets/SECRET_NAME/versions/VERSION_OR_LATEST'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#secret_uri ContainerNodePool#secret_uri}
        '''
        value = ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig(
            secret_uri=secret_uri
        )

        return typing.cast(None, jsii.invoke(self, "putGcpSecretManagerCertificateConfig", [value]))

    @builtins.property
    @jsii.member(jsii_name="gcpSecretManagerCertificateConfig")
    def gcp_secret_manager_certificate_config(
        self,
    ) -> ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfigOutputReference:
        return typing.cast(ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfigOutputReference, jsii.get(self, "gcpSecretManagerCertificateConfig"))

    @builtins.property
    @jsii.member(jsii_name="fqdnsInput")
    def fqdns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "fqdnsInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpSecretManagerCertificateConfigInput")
    def gcp_secret_manager_certificate_config_input(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig], jsii.get(self, "gcpSecretManagerCertificateConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fqdns")
    def fqdns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fqdns"))

    @fqdns.setter
    def fqdns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43612571fba3f30d52fb479103e7b8208bd3654c0abb5cf48e23d0b5e13fc5a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fqdns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7d89e4b304c687dd46f9ad8cb2aecc54a2569f462c30a0cbda088ecef8400ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c041eb242de485c090bece1e4960a03f1b8cc8780f331d31b19c1b2fd2c5910)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCertificateAuthorityDomainConfig")
    def put_certificate_authority_domain_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d43d4c8a0ad98d5fd7a820782913b509c8b63d242a4f0c0443952a4253c0d6e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCertificateAuthorityDomainConfig", [value]))

    @jsii.member(jsii_name="resetCertificateAuthorityDomainConfig")
    def reset_certificate_authority_domain_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateAuthorityDomainConfig", []))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityDomainConfig")
    def certificate_authority_domain_config(
        self,
    ) -> ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigList:
        return typing.cast(ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigList, jsii.get(self, "certificateAuthorityDomainConfig"))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityDomainConfigInput")
    def certificate_authority_domain_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig]]], jsii.get(self, "certificateAuthorityDomainConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8fd9c7e73f0eb0a60cea4707642756432260cffc85b11b4abddf0cc92f1d862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__408fb2a8d804db54bdde0a76a1d2bdff484681fc58e67654feffb0d6943e3874)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigEffectiveTaints",
    jsii_struct_bases=[],
    name_mapping={},
)
class ContainerNodePoolNodeConfigEffectiveTaints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigEffectiveTaints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNodeConfigEffectiveTaintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigEffectiveTaintsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f57f002ae261c592dc9c6c120f76b4395db4b68bf624a71ce93dc4519b4c952)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerNodePoolNodeConfigEffectiveTaintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a6fbf8583cd4348fec6242d1f0f02ab894286dd7bf4557ef78f5d1de844758f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerNodePoolNodeConfigEffectiveTaintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee50cb56acd8260255d2d41da3e382caac23e8356ec2242d2a3b00e0da9b5b02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e6499cf7711e2d3fce301a0ee1383919fec43e9d401dacd24782c51ccfa938)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__794c47c84c836a4bcdf94658d5fea9c76ce44f29fabaa476710f0214c26ceea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ContainerNodePoolNodeConfigEffectiveTaintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigEffectiveTaintsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e45791227ffbc621abc269ab82189d5038b0473b183e92e61a0555b37ae5b329)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="effect")
    def effect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effect"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigEffectiveTaints]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigEffectiveTaints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNodeConfigEffectiveTaints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c67e2fed0275096483cd4222fe360b4a2a9e92e68653e52c3626f69fd04b013d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig",
    jsii_struct_bases=[],
    name_mapping={
        "local_ssd_count": "localSsdCount",
        "data_cache_count": "dataCacheCount",
    },
)
class ContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig:
    def __init__(
        self,
        *,
        local_ssd_count: jsii.Number,
        data_cache_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param local_ssd_count: Number of local SSDs to use to back ephemeral storage. Uses NVMe interfaces. Each local SSD must be 375 or 3000 GB in size, and all local SSDs must share the same size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#local_ssd_count ContainerNodePool#local_ssd_count}
        :param data_cache_count: Number of local SSDs to be utilized for GKE Data Cache. Uses NVMe interfaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#data_cache_count ContainerNodePool#data_cache_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96a188e5167c88cf94b597447090b14745a4557a719fc4d664547de5858949ac)
            check_type(argname="argument local_ssd_count", value=local_ssd_count, expected_type=type_hints["local_ssd_count"])
            check_type(argname="argument data_cache_count", value=data_cache_count, expected_type=type_hints["data_cache_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "local_ssd_count": local_ssd_count,
        }
        if data_cache_count is not None:
            self._values["data_cache_count"] = data_cache_count

    @builtins.property
    def local_ssd_count(self) -> jsii.Number:
        '''Number of local SSDs to use to back ephemeral storage.

        Uses NVMe interfaces. Each local SSD must be 375 or 3000 GB in size, and all local SSDs must share the same size.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#local_ssd_count ContainerNodePool#local_ssd_count}
        '''
        result = self._values.get("local_ssd_count")
        assert result is not None, "Required property 'local_ssd_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def data_cache_count(self) -> typing.Optional[jsii.Number]:
        '''Number of local SSDs to be utilized for GKE Data Cache. Uses NVMe interfaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#data_cache_count ContainerNodePool#data_cache_count}
        '''
        result = self._values.get("data_cache_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e43eacce4fb1d41b116066d2098fbb94215f6676cd74783ccbb949b5f631aadd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDataCacheCount")
    def reset_data_cache_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataCacheCount", []))

    @builtins.property
    @jsii.member(jsii_name="dataCacheCountInput")
    def data_cache_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataCacheCountInput"))

    @builtins.property
    @jsii.member(jsii_name="localSsdCountInput")
    def local_ssd_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "localSsdCountInput"))

    @builtins.property
    @jsii.member(jsii_name="dataCacheCount")
    def data_cache_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataCacheCount"))

    @data_cache_count.setter
    def data_cache_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7be4c2d43771b7422235ee8f931901016694758c5c0d32fa8c4f0ee9c429f8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataCacheCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localSsdCount")
    def local_ssd_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "localSsdCount"))

    @local_ssd_count.setter
    def local_ssd_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40ab18c90f95146655100f462be636f58caf1f5cc09ae3508620ef1ae00221d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localSsdCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6325bd1636cd7ba12ac78acc1c03bea84dfedf51dd9a76316087b189c1545ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigFastSocket",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class ContainerNodePoolNodeConfigFastSocket:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether or not NCCL Fast Socket is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enabled ContainerNodePool#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5244a4a18a95bcbe02f47db1a602339491f1a817319853beeefe17ff406e0113)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether or not NCCL Fast Socket is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enabled ContainerNodePool#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigFastSocket(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNodeConfigFastSocketOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigFastSocketOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64f0ada489ee557a9f5d2e892c5e6e36eebfb9fe0a2e58cc30a7cd86c8ecc8b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3be3a9cc55d87d3ea44a51f21185c940eb0fc8c1433d8dd084901ca09f077372)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerNodePoolNodeConfigFastSocket]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigFastSocket], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNodeConfigFastSocket],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c153caaaa52be468904fced14b5090a0e64598bd2aea801f69ae4607b098ce1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigGcfsConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class ContainerNodePoolNodeConfigGcfsConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether or not GCFS is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enabled ContainerNodePool#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09b8b74f601eefff327c9378411729253b3cdcbfbe1d193444de384a0ed35822)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether or not GCFS is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enabled ContainerNodePool#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigGcfsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNodeConfigGcfsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigGcfsConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aff92f43b7e82bf39e8c75f1bf1f5be15302abdfd8e22a8de2eb273a53678c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fff317cbde6835756480aeb533c1add51c0791f9015bb77f70e6c2ff6e1af36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerNodePoolNodeConfigGcfsConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigGcfsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNodeConfigGcfsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__984185608b9c906f1782f4e2a646d1e37b57c195c42c1268aeb5e235d4b45190)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigGuestAccelerator",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "type": "type",
        "gpu_driver_installation_config": "gpuDriverInstallationConfig",
        "gpu_partition_size": "gpuPartitionSize",
        "gpu_sharing_config": "gpuSharingConfig",
    },
)
class ContainerNodePoolNodeConfigGuestAccelerator:
    def __init__(
        self,
        *,
        count: jsii.Number,
        type: builtins.str,
        gpu_driver_installation_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        gpu_partition_size: typing.Optional[builtins.str] = None,
        gpu_sharing_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param count: The number of the accelerator cards exposed to an instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#count ContainerNodePool#count}
        :param type: The accelerator type resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#type ContainerNodePool#type}
        :param gpu_driver_installation_config: gpu_driver_installation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#gpu_driver_installation_config ContainerNodePool#gpu_driver_installation_config}
        :param gpu_partition_size: Size of partitions to create on the GPU. Valid values are described in the NVIDIA mig user guide (https://docs.nvidia.com/datacenter/tesla/mig-user-guide/#partitioning). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#gpu_partition_size ContainerNodePool#gpu_partition_size}
        :param gpu_sharing_config: gpu_sharing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#gpu_sharing_config ContainerNodePool#gpu_sharing_config}
        '''
        if isinstance(gpu_driver_installation_config, dict):
            gpu_driver_installation_config = ContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig(**gpu_driver_installation_config)
        if isinstance(gpu_sharing_config, dict):
            gpu_sharing_config = ContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig(**gpu_sharing_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f30ac32d46d12017e0eeb590d01f391def5988006ed039bab3bc4474bdba26f9)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument gpu_driver_installation_config", value=gpu_driver_installation_config, expected_type=type_hints["gpu_driver_installation_config"])
            check_type(argname="argument gpu_partition_size", value=gpu_partition_size, expected_type=type_hints["gpu_partition_size"])
            check_type(argname="argument gpu_sharing_config", value=gpu_sharing_config, expected_type=type_hints["gpu_sharing_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "type": type,
        }
        if gpu_driver_installation_config is not None:
            self._values["gpu_driver_installation_config"] = gpu_driver_installation_config
        if gpu_partition_size is not None:
            self._values["gpu_partition_size"] = gpu_partition_size
        if gpu_sharing_config is not None:
            self._values["gpu_sharing_config"] = gpu_sharing_config

    @builtins.property
    def count(self) -> jsii.Number:
        '''The number of the accelerator cards exposed to an instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#count ContainerNodePool#count}
        '''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The accelerator type resource name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#type ContainerNodePool#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gpu_driver_installation_config(
        self,
    ) -> typing.Optional["ContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig"]:
        '''gpu_driver_installation_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#gpu_driver_installation_config ContainerNodePool#gpu_driver_installation_config}
        '''
        result = self._values.get("gpu_driver_installation_config")
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig"], result)

    @builtins.property
    def gpu_partition_size(self) -> typing.Optional[builtins.str]:
        '''Size of partitions to create on the GPU. Valid values are described in the NVIDIA mig user guide (https://docs.nvidia.com/datacenter/tesla/mig-user-guide/#partitioning).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#gpu_partition_size ContainerNodePool#gpu_partition_size}
        '''
        result = self._values.get("gpu_partition_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gpu_sharing_config(
        self,
    ) -> typing.Optional["ContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig"]:
        '''gpu_sharing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#gpu_sharing_config ContainerNodePool#gpu_sharing_config}
        '''
        result = self._values.get("gpu_sharing_config")
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigGuestAccelerator(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig",
    jsii_struct_bases=[],
    name_mapping={"gpu_driver_version": "gpuDriverVersion"},
)
class ContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig:
    def __init__(self, *, gpu_driver_version: builtins.str) -> None:
        '''
        :param gpu_driver_version: Mode for how the GPU driver is installed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#gpu_driver_version ContainerNodePool#gpu_driver_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce3318984671ac11c6550e3a977ea351fcec58006d3a53b833cbf41ff94cd9c8)
            check_type(argname="argument gpu_driver_version", value=gpu_driver_version, expected_type=type_hints["gpu_driver_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gpu_driver_version": gpu_driver_version,
        }

    @builtins.property
    def gpu_driver_version(self) -> builtins.str:
        '''Mode for how the GPU driver is installed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#gpu_driver_version ContainerNodePool#gpu_driver_version}
        '''
        result = self._values.get("gpu_driver_version")
        assert result is not None, "Required property 'gpu_driver_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97dd8e1665b143cd997ea44bfd4918193536cf146c86bee6090b7faa8c18ea90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="gpuDriverVersionInput")
    def gpu_driver_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gpuDriverVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="gpuDriverVersion")
    def gpu_driver_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gpuDriverVersion"))

    @gpu_driver_version.setter
    def gpu_driver_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8753a8e4780ac3dd2308cc597145cd4e70d06568c7dfe7e7edbfc4e416e553a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpuDriverVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e30664941914b1d5b31ba3d58e542c147cbc353a251f434f9827dec83ce0dd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "gpu_sharing_strategy": "gpuSharingStrategy",
        "max_shared_clients_per_gpu": "maxSharedClientsPerGpu",
    },
)
class ContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig:
    def __init__(
        self,
        *,
        gpu_sharing_strategy: builtins.str,
        max_shared_clients_per_gpu: jsii.Number,
    ) -> None:
        '''
        :param gpu_sharing_strategy: The type of GPU sharing strategy to enable on the GPU node. Possible values are described in the API package (https://pkg.go.dev/google.golang.org/api/container/v1#GPUSharingConfig) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#gpu_sharing_strategy ContainerNodePool#gpu_sharing_strategy}
        :param max_shared_clients_per_gpu: The maximum number of containers that can share a GPU. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#max_shared_clients_per_gpu ContainerNodePool#max_shared_clients_per_gpu}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aa4a423ead67dfc69d4e555095531f42430bf374fd08cee74d176e119d3cc14)
            check_type(argname="argument gpu_sharing_strategy", value=gpu_sharing_strategy, expected_type=type_hints["gpu_sharing_strategy"])
            check_type(argname="argument max_shared_clients_per_gpu", value=max_shared_clients_per_gpu, expected_type=type_hints["max_shared_clients_per_gpu"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gpu_sharing_strategy": gpu_sharing_strategy,
            "max_shared_clients_per_gpu": max_shared_clients_per_gpu,
        }

    @builtins.property
    def gpu_sharing_strategy(self) -> builtins.str:
        '''The type of GPU sharing strategy to enable on the GPU node.

        Possible values are described in the API package (https://pkg.go.dev/google.golang.org/api/container/v1#GPUSharingConfig)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#gpu_sharing_strategy ContainerNodePool#gpu_sharing_strategy}
        '''
        result = self._values.get("gpu_sharing_strategy")
        assert result is not None, "Required property 'gpu_sharing_strategy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_shared_clients_per_gpu(self) -> jsii.Number:
        '''The maximum number of containers that can share a GPU.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#max_shared_clients_per_gpu ContainerNodePool#max_shared_clients_per_gpu}
        '''
        result = self._values.get("max_shared_clients_per_gpu")
        assert result is not None, "Required property 'max_shared_clients_per_gpu' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8b38b74d6aa8d81c848694daff9a39e3accc4e02d50cdc346a557d5a7c81672)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="gpuSharingStrategyInput")
    def gpu_sharing_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gpuSharingStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="maxSharedClientsPerGpuInput")
    def max_shared_clients_per_gpu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxSharedClientsPerGpuInput"))

    @builtins.property
    @jsii.member(jsii_name="gpuSharingStrategy")
    def gpu_sharing_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gpuSharingStrategy"))

    @gpu_sharing_strategy.setter
    def gpu_sharing_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd6afbce62ae0a114d3ecb178ae787afe6f9e84d6d07fc740310e8fe97604c2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpuSharingStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxSharedClientsPerGpu")
    def max_shared_clients_per_gpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxSharedClientsPerGpu"))

    @max_shared_clients_per_gpu.setter
    def max_shared_clients_per_gpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c5d04f392020207c37d852ff9cf8fb3ccc222408190cc9f9956a7175ece76be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSharedClientsPerGpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd795e17f67eec9970af2829aa46fc74600a2d5f5405e74dcec5cc210b48b13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerNodePoolNodeConfigGuestAcceleratorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigGuestAcceleratorList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b76691c541f6c8638285486356d4b6c033d83039ed4fa13abff6d28ab2b051f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerNodePoolNodeConfigGuestAcceleratorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef213056406c08d6ae8e1100c9d7beaedccd909ad8789b1a5708ad2c4f349b19)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerNodePoolNodeConfigGuestAcceleratorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4161a997a8f93bb7faa3c05ddb3e8e332d210075c482cf6a33a0676259927bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__736ca78d4f73d65511e04be5dc2b621bddbadfc4c0eadd52458972b431b9d52a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__482ed8b1d1ddb4e7d9997427e8151f2d893735618325b7af12ccbca996aaf693)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigGuestAccelerator]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigGuestAccelerator]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigGuestAccelerator]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaadfade65ab71d9a79bc196ff59b484db2e0cd9b8849074f7992a78840efbbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerNodePoolNodeConfigGuestAcceleratorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigGuestAcceleratorOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e59f5acb116122ecfaa56e9ec06371eb7ebe7bfe359f7319157371985e116ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putGpuDriverInstallationConfig")
    def put_gpu_driver_installation_config(
        self,
        *,
        gpu_driver_version: builtins.str,
    ) -> None:
        '''
        :param gpu_driver_version: Mode for how the GPU driver is installed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#gpu_driver_version ContainerNodePool#gpu_driver_version}
        '''
        value = ContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig(
            gpu_driver_version=gpu_driver_version
        )

        return typing.cast(None, jsii.invoke(self, "putGpuDriverInstallationConfig", [value]))

    @jsii.member(jsii_name="putGpuSharingConfig")
    def put_gpu_sharing_config(
        self,
        *,
        gpu_sharing_strategy: builtins.str,
        max_shared_clients_per_gpu: jsii.Number,
    ) -> None:
        '''
        :param gpu_sharing_strategy: The type of GPU sharing strategy to enable on the GPU node. Possible values are described in the API package (https://pkg.go.dev/google.golang.org/api/container/v1#GPUSharingConfig) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#gpu_sharing_strategy ContainerNodePool#gpu_sharing_strategy}
        :param max_shared_clients_per_gpu: The maximum number of containers that can share a GPU. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#max_shared_clients_per_gpu ContainerNodePool#max_shared_clients_per_gpu}
        '''
        value = ContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig(
            gpu_sharing_strategy=gpu_sharing_strategy,
            max_shared_clients_per_gpu=max_shared_clients_per_gpu,
        )

        return typing.cast(None, jsii.invoke(self, "putGpuSharingConfig", [value]))

    @jsii.member(jsii_name="resetGpuDriverInstallationConfig")
    def reset_gpu_driver_installation_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGpuDriverInstallationConfig", []))

    @jsii.member(jsii_name="resetGpuPartitionSize")
    def reset_gpu_partition_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGpuPartitionSize", []))

    @jsii.member(jsii_name="resetGpuSharingConfig")
    def reset_gpu_sharing_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGpuSharingConfig", []))

    @builtins.property
    @jsii.member(jsii_name="gpuDriverInstallationConfig")
    def gpu_driver_installation_config(
        self,
    ) -> ContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfigOutputReference:
        return typing.cast(ContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfigOutputReference, jsii.get(self, "gpuDriverInstallationConfig"))

    @builtins.property
    @jsii.member(jsii_name="gpuSharingConfig")
    def gpu_sharing_config(
        self,
    ) -> ContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfigOutputReference:
        return typing.cast(ContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfigOutputReference, jsii.get(self, "gpuSharingConfig"))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="gpuDriverInstallationConfigInput")
    def gpu_driver_installation_config_input(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig], jsii.get(self, "gpuDriverInstallationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="gpuPartitionSizeInput")
    def gpu_partition_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gpuPartitionSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="gpuSharingConfigInput")
    def gpu_sharing_config_input(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig], jsii.get(self, "gpuSharingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85448f1a2612509436069b20d18028c465325e9db6796ed462dcd20003c53639)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpuPartitionSize")
    def gpu_partition_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gpuPartitionSize"))

    @gpu_partition_size.setter
    def gpu_partition_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4e71e53971282eaef18d251b73e4c628986fd117186c1ba1b2bc705deca4d55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpuPartitionSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cee90fce73a002616033ad053ebdd5bf6cf70ee9b9850f9cd2da55ca68af4599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNodeConfigGuestAccelerator]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNodeConfigGuestAccelerator]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNodeConfigGuestAccelerator]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9e8ee62a4a520859244b9c597a12b20be41364260f29197af8901ddde493cf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigGvnic",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class ContainerNodePoolNodeConfigGvnic:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether or not gvnic is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enabled ContainerNodePool#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e47d3bc40512a41cc51d7990d937743c3151685667c2db6170d85ebeb880899a)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether or not gvnic is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enabled ContainerNodePool#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigGvnic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNodeConfigGvnicOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigGvnicOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6796ff24e2aa2ebd5203b33802020f3684fb5ee1aa6112be97593d1e92eb057)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4047f846c25c883a1c05aef0b81284a35db9ebf0d5a91dfd5d0d81db517667b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerNodePoolNodeConfigGvnic]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigGvnic], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNodeConfigGvnic],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20383161e3e70c230d8420d7a577480befbd8ce3412a17cf1ca274569e21382c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigHostMaintenancePolicy",
    jsii_struct_bases=[],
    name_mapping={"maintenance_interval": "maintenanceInterval"},
)
class ContainerNodePoolNodeConfigHostMaintenancePolicy:
    def __init__(self, *, maintenance_interval: builtins.str) -> None:
        '''
        :param maintenance_interval: . Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#maintenance_interval ContainerNodePool#maintenance_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2a0f9d7139ba32901ab0ec356932d505a176abcb97ad6734e4a744686cef95d)
            check_type(argname="argument maintenance_interval", value=maintenance_interval, expected_type=type_hints["maintenance_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "maintenance_interval": maintenance_interval,
        }

    @builtins.property
    def maintenance_interval(self) -> builtins.str:
        '''.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#maintenance_interval ContainerNodePool#maintenance_interval}
        '''
        result = self._values.get("maintenance_interval")
        assert result is not None, "Required property 'maintenance_interval' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigHostMaintenancePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNodeConfigHostMaintenancePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigHostMaintenancePolicyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00b460bd465077ce399b0c79dcd01d4a90c9d18f4e3e8abd45708bfc2acbb6bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="maintenanceIntervalInput")
    def maintenance_interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maintenanceIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceInterval")
    def maintenance_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintenanceInterval"))

    @maintenance_interval.setter
    def maintenance_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__042ba9a71137b74563f9c07820e9a46100fa53b27a7d8da45406f333d5dab32e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigHostMaintenancePolicy]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigHostMaintenancePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNodeConfigHostMaintenancePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c48aa7a7dd6e16cd5424bd75ca44fdc57196d2dd469fe6f2ad40f5723f21200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigKubeletConfig",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_unsafe_sysctls": "allowedUnsafeSysctls",
        "container_log_max_files": "containerLogMaxFiles",
        "container_log_max_size": "containerLogMaxSize",
        "cpu_cfs_quota": "cpuCfsQuota",
        "cpu_cfs_quota_period": "cpuCfsQuotaPeriod",
        "cpu_manager_policy": "cpuManagerPolicy",
        "image_gc_high_threshold_percent": "imageGcHighThresholdPercent",
        "image_gc_low_threshold_percent": "imageGcLowThresholdPercent",
        "image_maximum_gc_age": "imageMaximumGcAge",
        "image_minimum_gc_age": "imageMinimumGcAge",
        "insecure_kubelet_readonly_port_enabled": "insecureKubeletReadonlyPortEnabled",
        "pod_pids_limit": "podPidsLimit",
    },
)
class ContainerNodePoolNodeConfigKubeletConfig:
    def __init__(
        self,
        *,
        allowed_unsafe_sysctls: typing.Optional[typing.Sequence[builtins.str]] = None,
        container_log_max_files: typing.Optional[jsii.Number] = None,
        container_log_max_size: typing.Optional[builtins.str] = None,
        cpu_cfs_quota: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cpu_cfs_quota_period: typing.Optional[builtins.str] = None,
        cpu_manager_policy: typing.Optional[builtins.str] = None,
        image_gc_high_threshold_percent: typing.Optional[jsii.Number] = None,
        image_gc_low_threshold_percent: typing.Optional[jsii.Number] = None,
        image_maximum_gc_age: typing.Optional[builtins.str] = None,
        image_minimum_gc_age: typing.Optional[builtins.str] = None,
        insecure_kubelet_readonly_port_enabled: typing.Optional[builtins.str] = None,
        pod_pids_limit: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param allowed_unsafe_sysctls: Defines a comma-separated allowlist of unsafe sysctls or sysctl patterns which can be set on the Pods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#allowed_unsafe_sysctls ContainerNodePool#allowed_unsafe_sysctls}
        :param container_log_max_files: Defines the maximum number of container log files that can be present for a container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#container_log_max_files ContainerNodePool#container_log_max_files}
        :param container_log_max_size: Defines the maximum size of the container log file before it is rotated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#container_log_max_size ContainerNodePool#container_log_max_size}
        :param cpu_cfs_quota: Enable CPU CFS quota enforcement for containers that specify CPU limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#cpu_cfs_quota ContainerNodePool#cpu_cfs_quota}
        :param cpu_cfs_quota_period: Set the CPU CFS quota period value 'cpu.cfs_period_us'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#cpu_cfs_quota_period ContainerNodePool#cpu_cfs_quota_period}
        :param cpu_manager_policy: Control the CPU management policy on the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#cpu_manager_policy ContainerNodePool#cpu_manager_policy}
        :param image_gc_high_threshold_percent: Defines the percent of disk usage after which image garbage collection is always run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#image_gc_high_threshold_percent ContainerNodePool#image_gc_high_threshold_percent}
        :param image_gc_low_threshold_percent: Defines the percent of disk usage before which image garbage collection is never run. Lowest disk usage to garbage collect to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#image_gc_low_threshold_percent ContainerNodePool#image_gc_low_threshold_percent}
        :param image_maximum_gc_age: Defines the maximum age an image can be unused before it is garbage collected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#image_maximum_gc_age ContainerNodePool#image_maximum_gc_age}
        :param image_minimum_gc_age: Defines the minimum age for an unused image before it is garbage collected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#image_minimum_gc_age ContainerNodePool#image_minimum_gc_age}
        :param insecure_kubelet_readonly_port_enabled: Controls whether the kubelet read-only port is enabled. It is strongly recommended to set this to ``FALSE``. Possible values: ``TRUE``, ``FALSE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#insecure_kubelet_readonly_port_enabled ContainerNodePool#insecure_kubelet_readonly_port_enabled}
        :param pod_pids_limit: Controls the maximum number of processes allowed to run in a pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#pod_pids_limit ContainerNodePool#pod_pids_limit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba35fbf8f2f5b8bedf5e350dde661105e29aa7385a444c7dab33b0385adff671)
            check_type(argname="argument allowed_unsafe_sysctls", value=allowed_unsafe_sysctls, expected_type=type_hints["allowed_unsafe_sysctls"])
            check_type(argname="argument container_log_max_files", value=container_log_max_files, expected_type=type_hints["container_log_max_files"])
            check_type(argname="argument container_log_max_size", value=container_log_max_size, expected_type=type_hints["container_log_max_size"])
            check_type(argname="argument cpu_cfs_quota", value=cpu_cfs_quota, expected_type=type_hints["cpu_cfs_quota"])
            check_type(argname="argument cpu_cfs_quota_period", value=cpu_cfs_quota_period, expected_type=type_hints["cpu_cfs_quota_period"])
            check_type(argname="argument cpu_manager_policy", value=cpu_manager_policy, expected_type=type_hints["cpu_manager_policy"])
            check_type(argname="argument image_gc_high_threshold_percent", value=image_gc_high_threshold_percent, expected_type=type_hints["image_gc_high_threshold_percent"])
            check_type(argname="argument image_gc_low_threshold_percent", value=image_gc_low_threshold_percent, expected_type=type_hints["image_gc_low_threshold_percent"])
            check_type(argname="argument image_maximum_gc_age", value=image_maximum_gc_age, expected_type=type_hints["image_maximum_gc_age"])
            check_type(argname="argument image_minimum_gc_age", value=image_minimum_gc_age, expected_type=type_hints["image_minimum_gc_age"])
            check_type(argname="argument insecure_kubelet_readonly_port_enabled", value=insecure_kubelet_readonly_port_enabled, expected_type=type_hints["insecure_kubelet_readonly_port_enabled"])
            check_type(argname="argument pod_pids_limit", value=pod_pids_limit, expected_type=type_hints["pod_pids_limit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_unsafe_sysctls is not None:
            self._values["allowed_unsafe_sysctls"] = allowed_unsafe_sysctls
        if container_log_max_files is not None:
            self._values["container_log_max_files"] = container_log_max_files
        if container_log_max_size is not None:
            self._values["container_log_max_size"] = container_log_max_size
        if cpu_cfs_quota is not None:
            self._values["cpu_cfs_quota"] = cpu_cfs_quota
        if cpu_cfs_quota_period is not None:
            self._values["cpu_cfs_quota_period"] = cpu_cfs_quota_period
        if cpu_manager_policy is not None:
            self._values["cpu_manager_policy"] = cpu_manager_policy
        if image_gc_high_threshold_percent is not None:
            self._values["image_gc_high_threshold_percent"] = image_gc_high_threshold_percent
        if image_gc_low_threshold_percent is not None:
            self._values["image_gc_low_threshold_percent"] = image_gc_low_threshold_percent
        if image_maximum_gc_age is not None:
            self._values["image_maximum_gc_age"] = image_maximum_gc_age
        if image_minimum_gc_age is not None:
            self._values["image_minimum_gc_age"] = image_minimum_gc_age
        if insecure_kubelet_readonly_port_enabled is not None:
            self._values["insecure_kubelet_readonly_port_enabled"] = insecure_kubelet_readonly_port_enabled
        if pod_pids_limit is not None:
            self._values["pod_pids_limit"] = pod_pids_limit

    @builtins.property
    def allowed_unsafe_sysctls(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Defines a comma-separated allowlist of unsafe sysctls or sysctl patterns which can be set on the Pods.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#allowed_unsafe_sysctls ContainerNodePool#allowed_unsafe_sysctls}
        '''
        result = self._values.get("allowed_unsafe_sysctls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def container_log_max_files(self) -> typing.Optional[jsii.Number]:
        '''Defines the maximum number of container log files that can be present for a container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#container_log_max_files ContainerNodePool#container_log_max_files}
        '''
        result = self._values.get("container_log_max_files")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def container_log_max_size(self) -> typing.Optional[builtins.str]:
        '''Defines the maximum size of the container log file before it is rotated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#container_log_max_size ContainerNodePool#container_log_max_size}
        '''
        result = self._values.get("container_log_max_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_cfs_quota(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable CPU CFS quota enforcement for containers that specify CPU limits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#cpu_cfs_quota ContainerNodePool#cpu_cfs_quota}
        '''
        result = self._values.get("cpu_cfs_quota")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cpu_cfs_quota_period(self) -> typing.Optional[builtins.str]:
        '''Set the CPU CFS quota period value 'cpu.cfs_period_us'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#cpu_cfs_quota_period ContainerNodePool#cpu_cfs_quota_period}
        '''
        result = self._values.get("cpu_cfs_quota_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_manager_policy(self) -> typing.Optional[builtins.str]:
        '''Control the CPU management policy on the node.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#cpu_manager_policy ContainerNodePool#cpu_manager_policy}
        '''
        result = self._values.get("cpu_manager_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_gc_high_threshold_percent(self) -> typing.Optional[jsii.Number]:
        '''Defines the percent of disk usage after which image garbage collection is always run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#image_gc_high_threshold_percent ContainerNodePool#image_gc_high_threshold_percent}
        '''
        result = self._values.get("image_gc_high_threshold_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def image_gc_low_threshold_percent(self) -> typing.Optional[jsii.Number]:
        '''Defines the percent of disk usage before which image garbage collection is never run.

        Lowest disk usage to garbage collect to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#image_gc_low_threshold_percent ContainerNodePool#image_gc_low_threshold_percent}
        '''
        result = self._values.get("image_gc_low_threshold_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def image_maximum_gc_age(self) -> typing.Optional[builtins.str]:
        '''Defines the maximum age an image can be unused before it is garbage collected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#image_maximum_gc_age ContainerNodePool#image_maximum_gc_age}
        '''
        result = self._values.get("image_maximum_gc_age")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_minimum_gc_age(self) -> typing.Optional[builtins.str]:
        '''Defines the minimum age for an unused image before it is garbage collected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#image_minimum_gc_age ContainerNodePool#image_minimum_gc_age}
        '''
        result = self._values.get("image_minimum_gc_age")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insecure_kubelet_readonly_port_enabled(self) -> typing.Optional[builtins.str]:
        '''Controls whether the kubelet read-only port is enabled.

        It is strongly recommended to set this to ``FALSE``. Possible values: ``TRUE``, ``FALSE``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#insecure_kubelet_readonly_port_enabled ContainerNodePool#insecure_kubelet_readonly_port_enabled}
        '''
        result = self._values.get("insecure_kubelet_readonly_port_enabled")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pod_pids_limit(self) -> typing.Optional[jsii.Number]:
        '''Controls the maximum number of processes allowed to run in a pod.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#pod_pids_limit ContainerNodePool#pod_pids_limit}
        '''
        result = self._values.get("pod_pids_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigKubeletConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNodeConfigKubeletConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigKubeletConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5f9fb292c0743b4076da0ae8d4b13dea9d24cb16c526cc8f437582310d76e9c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedUnsafeSysctls")
    def reset_allowed_unsafe_sysctls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedUnsafeSysctls", []))

    @jsii.member(jsii_name="resetContainerLogMaxFiles")
    def reset_container_log_max_files(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerLogMaxFiles", []))

    @jsii.member(jsii_name="resetContainerLogMaxSize")
    def reset_container_log_max_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerLogMaxSize", []))

    @jsii.member(jsii_name="resetCpuCfsQuota")
    def reset_cpu_cfs_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuCfsQuota", []))

    @jsii.member(jsii_name="resetCpuCfsQuotaPeriod")
    def reset_cpu_cfs_quota_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuCfsQuotaPeriod", []))

    @jsii.member(jsii_name="resetCpuManagerPolicy")
    def reset_cpu_manager_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuManagerPolicy", []))

    @jsii.member(jsii_name="resetImageGcHighThresholdPercent")
    def reset_image_gc_high_threshold_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageGcHighThresholdPercent", []))

    @jsii.member(jsii_name="resetImageGcLowThresholdPercent")
    def reset_image_gc_low_threshold_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageGcLowThresholdPercent", []))

    @jsii.member(jsii_name="resetImageMaximumGcAge")
    def reset_image_maximum_gc_age(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageMaximumGcAge", []))

    @jsii.member(jsii_name="resetImageMinimumGcAge")
    def reset_image_minimum_gc_age(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageMinimumGcAge", []))

    @jsii.member(jsii_name="resetInsecureKubeletReadonlyPortEnabled")
    def reset_insecure_kubelet_readonly_port_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsecureKubeletReadonlyPortEnabled", []))

    @jsii.member(jsii_name="resetPodPidsLimit")
    def reset_pod_pids_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPodPidsLimit", []))

    @builtins.property
    @jsii.member(jsii_name="allowedUnsafeSysctlsInput")
    def allowed_unsafe_sysctls_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedUnsafeSysctlsInput"))

    @builtins.property
    @jsii.member(jsii_name="containerLogMaxFilesInput")
    def container_log_max_files_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "containerLogMaxFilesInput"))

    @builtins.property
    @jsii.member(jsii_name="containerLogMaxSizeInput")
    def container_log_max_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerLogMaxSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuCfsQuotaInput")
    def cpu_cfs_quota_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cpuCfsQuotaInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuCfsQuotaPeriodInput")
    def cpu_cfs_quota_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuCfsQuotaPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuManagerPolicyInput")
    def cpu_manager_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuManagerPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="imageGcHighThresholdPercentInput")
    def image_gc_high_threshold_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "imageGcHighThresholdPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="imageGcLowThresholdPercentInput")
    def image_gc_low_threshold_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "imageGcLowThresholdPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="imageMaximumGcAgeInput")
    def image_maximum_gc_age_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageMaximumGcAgeInput"))

    @builtins.property
    @jsii.member(jsii_name="imageMinimumGcAgeInput")
    def image_minimum_gc_age_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageMinimumGcAgeInput"))

    @builtins.property
    @jsii.member(jsii_name="insecureKubeletReadonlyPortEnabledInput")
    def insecure_kubelet_readonly_port_enabled_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "insecureKubeletReadonlyPortEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="podPidsLimitInput")
    def pod_pids_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "podPidsLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedUnsafeSysctls")
    def allowed_unsafe_sysctls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedUnsafeSysctls"))

    @allowed_unsafe_sysctls.setter
    def allowed_unsafe_sysctls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__049f938abe2d60f7497ef8cd59965b140c4e154f88d4185ded98054bcb3dde7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedUnsafeSysctls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerLogMaxFiles")
    def container_log_max_files(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "containerLogMaxFiles"))

    @container_log_max_files.setter
    def container_log_max_files(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5477d7d70e82c906a216ecf3b39ce5401a3558341dbb000df5220202a9c05dc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerLogMaxFiles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerLogMaxSize")
    def container_log_max_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerLogMaxSize"))

    @container_log_max_size.setter
    def container_log_max_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a3cbd22c002fa6848a1056513255b455a5315698bebc79f03d861ee0d4c804)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerLogMaxSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuCfsQuota")
    def cpu_cfs_quota(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cpuCfsQuota"))

    @cpu_cfs_quota.setter
    def cpu_cfs_quota(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf55914796ef074e1d1a74c3d3a5b63fe4e093ee0ef8e02690850bb467704064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCfsQuota", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuCfsQuotaPeriod")
    def cpu_cfs_quota_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuCfsQuotaPeriod"))

    @cpu_cfs_quota_period.setter
    def cpu_cfs_quota_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55ef573369edf765b329cbd403bde6571a21a49e696159d6a84e72010fa923f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCfsQuotaPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuManagerPolicy")
    def cpu_manager_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuManagerPolicy"))

    @cpu_manager_policy.setter
    def cpu_manager_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4e169b5b2e241247e5558a93d16c9e941eda0dbc8d11d79890215b4e5d0f9a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuManagerPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageGcHighThresholdPercent")
    def image_gc_high_threshold_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "imageGcHighThresholdPercent"))

    @image_gc_high_threshold_percent.setter
    def image_gc_high_threshold_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__430b5018f363549178a4e68483e00c9bef2449409a1f793491f149bac1dd8f8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageGcHighThresholdPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageGcLowThresholdPercent")
    def image_gc_low_threshold_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "imageGcLowThresholdPercent"))

    @image_gc_low_threshold_percent.setter
    def image_gc_low_threshold_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac1004a20718eedc499b7240f1ac656e34c253d239310a54420258afe7aa0ceb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageGcLowThresholdPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageMaximumGcAge")
    def image_maximum_gc_age(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageMaximumGcAge"))

    @image_maximum_gc_age.setter
    def image_maximum_gc_age(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__596a76e214711c8d049d0c69c6efaf3f7a9fae561e51793aeb946fa99f42e4dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageMaximumGcAge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageMinimumGcAge")
    def image_minimum_gc_age(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageMinimumGcAge"))

    @image_minimum_gc_age.setter
    def image_minimum_gc_age(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1764c33d847d07505da712be10ead70d767d6fd304b28d258f3afc3adfc2afc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageMinimumGcAge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="insecureKubeletReadonlyPortEnabled")
    def insecure_kubelet_readonly_port_enabled(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "insecureKubeletReadonlyPortEnabled"))

    @insecure_kubelet_readonly_port_enabled.setter
    def insecure_kubelet_readonly_port_enabled(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65a713520d0250c4f99a546d716cc18a9fdb600c5cd90057abf49dc97fb11122)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecureKubeletReadonlyPortEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="podPidsLimit")
    def pod_pids_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "podPidsLimit"))

    @pod_pids_limit.setter
    def pod_pids_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417370ad149bd7e99953841a9b4f65088affa1c8376ce7cd5901246597e75992)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podPidsLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigKubeletConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigKubeletConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNodeConfigKubeletConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b58851cb84b1cd183e9f303cbbe398252fc0b554f73272e7b9fff0d02f12262)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigLinuxNodeConfig",
    jsii_struct_bases=[],
    name_mapping={
        "cgroup_mode": "cgroupMode",
        "hugepages_config": "hugepagesConfig",
        "sysctls": "sysctls",
    },
)
class ContainerNodePoolNodeConfigLinuxNodeConfig:
    def __init__(
        self,
        *,
        cgroup_mode: typing.Optional[builtins.str] = None,
        hugepages_config: typing.Optional[typing.Union["ContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        sysctls: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param cgroup_mode: cgroupMode specifies the cgroup mode to be used on the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#cgroup_mode ContainerNodePool#cgroup_mode}
        :param hugepages_config: hugepages_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#hugepages_config ContainerNodePool#hugepages_config}
        :param sysctls: The Linux kernel parameters to be applied to the nodes and all pods running on the nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#sysctls ContainerNodePool#sysctls}
        '''
        if isinstance(hugepages_config, dict):
            hugepages_config = ContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig(**hugepages_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16948441d4349ba63ed1b4710c36ed3e9de19ad2ec5116c02db8615cb1a10b06)
            check_type(argname="argument cgroup_mode", value=cgroup_mode, expected_type=type_hints["cgroup_mode"])
            check_type(argname="argument hugepages_config", value=hugepages_config, expected_type=type_hints["hugepages_config"])
            check_type(argname="argument sysctls", value=sysctls, expected_type=type_hints["sysctls"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cgroup_mode is not None:
            self._values["cgroup_mode"] = cgroup_mode
        if hugepages_config is not None:
            self._values["hugepages_config"] = hugepages_config
        if sysctls is not None:
            self._values["sysctls"] = sysctls

    @builtins.property
    def cgroup_mode(self) -> typing.Optional[builtins.str]:
        '''cgroupMode specifies the cgroup mode to be used on the node.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#cgroup_mode ContainerNodePool#cgroup_mode}
        '''
        result = self._values.get("cgroup_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hugepages_config(
        self,
    ) -> typing.Optional["ContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig"]:
        '''hugepages_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#hugepages_config ContainerNodePool#hugepages_config}
        '''
        result = self._values.get("hugepages_config")
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig"], result)

    @builtins.property
    def sysctls(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The Linux kernel parameters to be applied to the nodes and all pods running on the nodes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#sysctls ContainerNodePool#sysctls}
        '''
        result = self._values.get("sysctls")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigLinuxNodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig",
    jsii_struct_bases=[],
    name_mapping={
        "hugepage_size1_g": "hugepageSize1G",
        "hugepage_size2_m": "hugepageSize2M",
    },
)
class ContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig:
    def __init__(
        self,
        *,
        hugepage_size1_g: typing.Optional[jsii.Number] = None,
        hugepage_size2_m: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hugepage_size1_g: Amount of 1G hugepages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#hugepage_size_1g ContainerNodePool#hugepage_size_1g}
        :param hugepage_size2_m: Amount of 2M hugepages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#hugepage_size_2m ContainerNodePool#hugepage_size_2m}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a489ee8c4d58a71fe3574d56ad1784304ed38e113d774afecae2d8b491739cc)
            check_type(argname="argument hugepage_size1_g", value=hugepage_size1_g, expected_type=type_hints["hugepage_size1_g"])
            check_type(argname="argument hugepage_size2_m", value=hugepage_size2_m, expected_type=type_hints["hugepage_size2_m"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hugepage_size1_g is not None:
            self._values["hugepage_size1_g"] = hugepage_size1_g
        if hugepage_size2_m is not None:
            self._values["hugepage_size2_m"] = hugepage_size2_m

    @builtins.property
    def hugepage_size1_g(self) -> typing.Optional[jsii.Number]:
        '''Amount of 1G hugepages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#hugepage_size_1g ContainerNodePool#hugepage_size_1g}
        '''
        result = self._values.get("hugepage_size1_g")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def hugepage_size2_m(self) -> typing.Optional[jsii.Number]:
        '''Amount of 2M hugepages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#hugepage_size_2m ContainerNodePool#hugepage_size_2m}
        '''
        result = self._values.get("hugepage_size2_m")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f14f72c4e15ef679de121818408e5e95e6d8d6fb472f5e2e9a883a43f76ce955)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHugepageSize1G")
    def reset_hugepage_size1_g(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHugepageSize1G", []))

    @jsii.member(jsii_name="resetHugepageSize2M")
    def reset_hugepage_size2_m(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHugepageSize2M", []))

    @builtins.property
    @jsii.member(jsii_name="hugepageSize1GInput")
    def hugepage_size1_g_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hugepageSize1GInput"))

    @builtins.property
    @jsii.member(jsii_name="hugepageSize2MInput")
    def hugepage_size2_m_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hugepageSize2MInput"))

    @builtins.property
    @jsii.member(jsii_name="hugepageSize1G")
    def hugepage_size1_g(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hugepageSize1G"))

    @hugepage_size1_g.setter
    def hugepage_size1_g(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8539aeab70b22e2f4d8b53bf65c3f6f8823c85291131187c9a7a64a8056658c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hugepageSize1G", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hugepageSize2M")
    def hugepage_size2_m(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hugepageSize2M"))

    @hugepage_size2_m.setter
    def hugepage_size2_m(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__880ca37c2fc07ea4b717ad8f0bda499c1e6957a3e0f54f0bfa3f8a1b067de8fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hugepageSize2M", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33e9e8c5d444158635ed1ed8394f89ef2df2fc6574619b1d6fc5e8f5e30912aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerNodePoolNodeConfigLinuxNodeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigLinuxNodeConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0460ef1475f1ef6567e5169f475b7ceb38265d44a4565c990b3a685e9cab3a29)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHugepagesConfig")
    def put_hugepages_config(
        self,
        *,
        hugepage_size1_g: typing.Optional[jsii.Number] = None,
        hugepage_size2_m: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hugepage_size1_g: Amount of 1G hugepages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#hugepage_size_1g ContainerNodePool#hugepage_size_1g}
        :param hugepage_size2_m: Amount of 2M hugepages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#hugepage_size_2m ContainerNodePool#hugepage_size_2m}
        '''
        value = ContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig(
            hugepage_size1_g=hugepage_size1_g, hugepage_size2_m=hugepage_size2_m
        )

        return typing.cast(None, jsii.invoke(self, "putHugepagesConfig", [value]))

    @jsii.member(jsii_name="resetCgroupMode")
    def reset_cgroup_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCgroupMode", []))

    @jsii.member(jsii_name="resetHugepagesConfig")
    def reset_hugepages_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHugepagesConfig", []))

    @jsii.member(jsii_name="resetSysctls")
    def reset_sysctls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSysctls", []))

    @builtins.property
    @jsii.member(jsii_name="hugepagesConfig")
    def hugepages_config(
        self,
    ) -> ContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfigOutputReference:
        return typing.cast(ContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfigOutputReference, jsii.get(self, "hugepagesConfig"))

    @builtins.property
    @jsii.member(jsii_name="cgroupModeInput")
    def cgroup_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cgroupModeInput"))

    @builtins.property
    @jsii.member(jsii_name="hugepagesConfigInput")
    def hugepages_config_input(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig], jsii.get(self, "hugepagesConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sysctlsInput")
    def sysctls_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "sysctlsInput"))

    @builtins.property
    @jsii.member(jsii_name="cgroupMode")
    def cgroup_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cgroupMode"))

    @cgroup_mode.setter
    def cgroup_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca4dec1f95cd23ad879ccf7e5dc53bc670bc0fe6ca80ede5ce3623566943101f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cgroupMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sysctls")
    def sysctls(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "sysctls"))

    @sysctls.setter
    def sysctls(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f508b6be4bf1c1074acaed306517780fd016714139e866a1821151c7a2f604a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sysctls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigLinuxNodeConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigLinuxNodeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNodeConfigLinuxNodeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ac964f12ae2a74330e7063adce4389e7a53a1c4bc5bc491fa43ec9d620dfc3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig",
    jsii_struct_bases=[],
    name_mapping={"local_ssd_count": "localSsdCount"},
)
class ContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig:
    def __init__(self, *, local_ssd_count: jsii.Number) -> None:
        '''
        :param local_ssd_count: Number of raw-block local NVMe SSD disks to be attached to the node. Each local SSD is 375 GB in size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#local_ssd_count ContainerNodePool#local_ssd_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65981ffdb6e267ef9da5fd2280da58fae8ab4507b53d2bbd5c731b8d316388d6)
            check_type(argname="argument local_ssd_count", value=local_ssd_count, expected_type=type_hints["local_ssd_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "local_ssd_count": local_ssd_count,
        }

    @builtins.property
    def local_ssd_count(self) -> jsii.Number:
        '''Number of raw-block local NVMe SSD disks to be attached to the node.

        Each local SSD is 375 GB in size.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#local_ssd_count ContainerNodePool#local_ssd_count}
        '''
        result = self._values.get("local_ssd_count")
        assert result is not None, "Required property 'local_ssd_count' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNodeConfigLocalNvmeSsdBlockConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigLocalNvmeSsdBlockConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26f0196350b00d59c0f93e7f5651a49be6cfbe7f60720203ea9586900d5dafb1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="localSsdCountInput")
    def local_ssd_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "localSsdCountInput"))

    @builtins.property
    @jsii.member(jsii_name="localSsdCount")
    def local_ssd_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "localSsdCount"))

    @local_ssd_count.setter
    def local_ssd_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d56cbb6300045f8e1cda4f2abe33d48c7b5722c641d4aa1d7bc65168a75421e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localSsdCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd677fd3dad6718d717e6413e8076fbf5dc5653d9090839a6877308eb3ca825)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerNodePoolNodeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6955ee7a6cfb6a8c027acbc473ed7f645164620729aaeaadc57fe6a5b049337a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdvancedMachineFeatures")
    def put_advanced_machine_features(
        self,
        *,
        threads_per_core: jsii.Number,
        enable_nested_virtualization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        performance_monitoring_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param threads_per_core: The number of threads per physical core. To disable simultaneous multithreading (SMT) set this to 1. If unset, the maximum number of threads supported per core by the underlying processor is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#threads_per_core ContainerNodePool#threads_per_core}
        :param enable_nested_virtualization: Whether the node should have nested virtualization enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enable_nested_virtualization ContainerNodePool#enable_nested_virtualization}
        :param performance_monitoring_unit: Level of Performance Monitoring Unit (PMU) requested. If unset, no access to the PMU is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#performance_monitoring_unit ContainerNodePool#performance_monitoring_unit}
        '''
        value = ContainerNodePoolNodeConfigAdvancedMachineFeatures(
            threads_per_core=threads_per_core,
            enable_nested_virtualization=enable_nested_virtualization,
            performance_monitoring_unit=performance_monitoring_unit,
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedMachineFeatures", [value]))

    @jsii.member(jsii_name="putConfidentialNodes")
    def put_confidential_nodes(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        confidential_instance_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Whether Confidential Nodes feature is enabled for all nodes in this pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enabled ContainerNodePool#enabled}
        :param confidential_instance_type: Defines the type of technology used by the confidential node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#confidential_instance_type ContainerNodePool#confidential_instance_type}
        '''
        value = ContainerNodePoolNodeConfigConfidentialNodes(
            enabled=enabled, confidential_instance_type=confidential_instance_type
        )

        return typing.cast(None, jsii.invoke(self, "putConfidentialNodes", [value]))

    @jsii.member(jsii_name="putContainerdConfig")
    def put_containerd_config(
        self,
        *,
        private_registry_access_config: typing.Optional[typing.Union[ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param private_registry_access_config: private_registry_access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#private_registry_access_config ContainerNodePool#private_registry_access_config}
        '''
        value = ContainerNodePoolNodeConfigContainerdConfig(
            private_registry_access_config=private_registry_access_config
        )

        return typing.cast(None, jsii.invoke(self, "putContainerdConfig", [value]))

    @jsii.member(jsii_name="putEphemeralStorageLocalSsdConfig")
    def put_ephemeral_storage_local_ssd_config(
        self,
        *,
        local_ssd_count: jsii.Number,
        data_cache_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param local_ssd_count: Number of local SSDs to use to back ephemeral storage. Uses NVMe interfaces. Each local SSD must be 375 or 3000 GB in size, and all local SSDs must share the same size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#local_ssd_count ContainerNodePool#local_ssd_count}
        :param data_cache_count: Number of local SSDs to be utilized for GKE Data Cache. Uses NVMe interfaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#data_cache_count ContainerNodePool#data_cache_count}
        '''
        value = ContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig(
            local_ssd_count=local_ssd_count, data_cache_count=data_cache_count
        )

        return typing.cast(None, jsii.invoke(self, "putEphemeralStorageLocalSsdConfig", [value]))

    @jsii.member(jsii_name="putFastSocket")
    def put_fast_socket(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether or not NCCL Fast Socket is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enabled ContainerNodePool#enabled}
        '''
        value = ContainerNodePoolNodeConfigFastSocket(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putFastSocket", [value]))

    @jsii.member(jsii_name="putGcfsConfig")
    def put_gcfs_config(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether or not GCFS is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enabled ContainerNodePool#enabled}
        '''
        value = ContainerNodePoolNodeConfigGcfsConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putGcfsConfig", [value]))

    @jsii.member(jsii_name="putGuestAccelerator")
    def put_guest_accelerator(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerNodePoolNodeConfigGuestAccelerator, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13ae90f9fdff9da656a0d4d88632dc03b70545caec4dc7eeb7ed06062de89863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGuestAccelerator", [value]))

    @jsii.member(jsii_name="putGvnic")
    def put_gvnic(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether or not gvnic is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enabled ContainerNodePool#enabled}
        '''
        value = ContainerNodePoolNodeConfigGvnic(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putGvnic", [value]))

    @jsii.member(jsii_name="putHostMaintenancePolicy")
    def put_host_maintenance_policy(
        self,
        *,
        maintenance_interval: builtins.str,
    ) -> None:
        '''
        :param maintenance_interval: . Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#maintenance_interval ContainerNodePool#maintenance_interval}
        '''
        value = ContainerNodePoolNodeConfigHostMaintenancePolicy(
            maintenance_interval=maintenance_interval
        )

        return typing.cast(None, jsii.invoke(self, "putHostMaintenancePolicy", [value]))

    @jsii.member(jsii_name="putKubeletConfig")
    def put_kubelet_config(
        self,
        *,
        allowed_unsafe_sysctls: typing.Optional[typing.Sequence[builtins.str]] = None,
        container_log_max_files: typing.Optional[jsii.Number] = None,
        container_log_max_size: typing.Optional[builtins.str] = None,
        cpu_cfs_quota: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cpu_cfs_quota_period: typing.Optional[builtins.str] = None,
        cpu_manager_policy: typing.Optional[builtins.str] = None,
        image_gc_high_threshold_percent: typing.Optional[jsii.Number] = None,
        image_gc_low_threshold_percent: typing.Optional[jsii.Number] = None,
        image_maximum_gc_age: typing.Optional[builtins.str] = None,
        image_minimum_gc_age: typing.Optional[builtins.str] = None,
        insecure_kubelet_readonly_port_enabled: typing.Optional[builtins.str] = None,
        pod_pids_limit: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param allowed_unsafe_sysctls: Defines a comma-separated allowlist of unsafe sysctls or sysctl patterns which can be set on the Pods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#allowed_unsafe_sysctls ContainerNodePool#allowed_unsafe_sysctls}
        :param container_log_max_files: Defines the maximum number of container log files that can be present for a container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#container_log_max_files ContainerNodePool#container_log_max_files}
        :param container_log_max_size: Defines the maximum size of the container log file before it is rotated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#container_log_max_size ContainerNodePool#container_log_max_size}
        :param cpu_cfs_quota: Enable CPU CFS quota enforcement for containers that specify CPU limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#cpu_cfs_quota ContainerNodePool#cpu_cfs_quota}
        :param cpu_cfs_quota_period: Set the CPU CFS quota period value 'cpu.cfs_period_us'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#cpu_cfs_quota_period ContainerNodePool#cpu_cfs_quota_period}
        :param cpu_manager_policy: Control the CPU management policy on the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#cpu_manager_policy ContainerNodePool#cpu_manager_policy}
        :param image_gc_high_threshold_percent: Defines the percent of disk usage after which image garbage collection is always run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#image_gc_high_threshold_percent ContainerNodePool#image_gc_high_threshold_percent}
        :param image_gc_low_threshold_percent: Defines the percent of disk usage before which image garbage collection is never run. Lowest disk usage to garbage collect to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#image_gc_low_threshold_percent ContainerNodePool#image_gc_low_threshold_percent}
        :param image_maximum_gc_age: Defines the maximum age an image can be unused before it is garbage collected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#image_maximum_gc_age ContainerNodePool#image_maximum_gc_age}
        :param image_minimum_gc_age: Defines the minimum age for an unused image before it is garbage collected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#image_minimum_gc_age ContainerNodePool#image_minimum_gc_age}
        :param insecure_kubelet_readonly_port_enabled: Controls whether the kubelet read-only port is enabled. It is strongly recommended to set this to ``FALSE``. Possible values: ``TRUE``, ``FALSE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#insecure_kubelet_readonly_port_enabled ContainerNodePool#insecure_kubelet_readonly_port_enabled}
        :param pod_pids_limit: Controls the maximum number of processes allowed to run in a pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#pod_pids_limit ContainerNodePool#pod_pids_limit}
        '''
        value = ContainerNodePoolNodeConfigKubeletConfig(
            allowed_unsafe_sysctls=allowed_unsafe_sysctls,
            container_log_max_files=container_log_max_files,
            container_log_max_size=container_log_max_size,
            cpu_cfs_quota=cpu_cfs_quota,
            cpu_cfs_quota_period=cpu_cfs_quota_period,
            cpu_manager_policy=cpu_manager_policy,
            image_gc_high_threshold_percent=image_gc_high_threshold_percent,
            image_gc_low_threshold_percent=image_gc_low_threshold_percent,
            image_maximum_gc_age=image_maximum_gc_age,
            image_minimum_gc_age=image_minimum_gc_age,
            insecure_kubelet_readonly_port_enabled=insecure_kubelet_readonly_port_enabled,
            pod_pids_limit=pod_pids_limit,
        )

        return typing.cast(None, jsii.invoke(self, "putKubeletConfig", [value]))

    @jsii.member(jsii_name="putLinuxNodeConfig")
    def put_linux_node_config(
        self,
        *,
        cgroup_mode: typing.Optional[builtins.str] = None,
        hugepages_config: typing.Optional[typing.Union[ContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        sysctls: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param cgroup_mode: cgroupMode specifies the cgroup mode to be used on the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#cgroup_mode ContainerNodePool#cgroup_mode}
        :param hugepages_config: hugepages_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#hugepages_config ContainerNodePool#hugepages_config}
        :param sysctls: The Linux kernel parameters to be applied to the nodes and all pods running on the nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#sysctls ContainerNodePool#sysctls}
        '''
        value = ContainerNodePoolNodeConfigLinuxNodeConfig(
            cgroup_mode=cgroup_mode, hugepages_config=hugepages_config, sysctls=sysctls
        )

        return typing.cast(None, jsii.invoke(self, "putLinuxNodeConfig", [value]))

    @jsii.member(jsii_name="putLocalNvmeSsdBlockConfig")
    def put_local_nvme_ssd_block_config(self, *, local_ssd_count: jsii.Number) -> None:
        '''
        :param local_ssd_count: Number of raw-block local NVMe SSD disks to be attached to the node. Each local SSD is 375 GB in size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#local_ssd_count ContainerNodePool#local_ssd_count}
        '''
        value = ContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig(
            local_ssd_count=local_ssd_count
        )

        return typing.cast(None, jsii.invoke(self, "putLocalNvmeSsdBlockConfig", [value]))

    @jsii.member(jsii_name="putReservationAffinity")
    def put_reservation_affinity(
        self,
        *,
        consume_reservation_type: builtins.str,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param consume_reservation_type: Corresponds to the type of reservation consumption. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#consume_reservation_type ContainerNodePool#consume_reservation_type}
        :param key: The label key of a reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#key ContainerNodePool#key}
        :param values: The label values of the reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#values ContainerNodePool#values}
        '''
        value = ContainerNodePoolNodeConfigReservationAffinity(
            consume_reservation_type=consume_reservation_type, key=key, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putReservationAffinity", [value]))

    @jsii.member(jsii_name="putSecondaryBootDisks")
    def put_secondary_boot_disks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerNodePoolNodeConfigSecondaryBootDisks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4a9cc80442d07d5557d37fbd806eb6212760c6dd560f3ab03e07c6404ea9e72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecondaryBootDisks", [value]))

    @jsii.member(jsii_name="putShieldedInstanceConfig")
    def put_shielded_instance_config(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Defines whether the instance has integrity monitoring enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enable_integrity_monitoring ContainerNodePool#enable_integrity_monitoring}
        :param enable_secure_boot: Defines whether the instance has Secure Boot enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enable_secure_boot ContainerNodePool#enable_secure_boot}
        '''
        value = ContainerNodePoolNodeConfigShieldedInstanceConfig(
            enable_integrity_monitoring=enable_integrity_monitoring,
            enable_secure_boot=enable_secure_boot,
        )

        return typing.cast(None, jsii.invoke(self, "putShieldedInstanceConfig", [value]))

    @jsii.member(jsii_name="putSoleTenantConfig")
    def put_sole_tenant_config(
        self,
        *,
        node_affinity: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param node_affinity: node_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#node_affinity ContainerNodePool#node_affinity}
        '''
        value = ContainerNodePoolNodeConfigSoleTenantConfig(
            node_affinity=node_affinity
        )

        return typing.cast(None, jsii.invoke(self, "putSoleTenantConfig", [value]))

    @jsii.member(jsii_name="putTaint")
    def put_taint(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerNodePoolNodeConfigTaint", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4a9eb550fc41fae95eba9c1ae96e8dd8b89fb7a1e32733d03306886b471a4b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTaint", [value]))

    @jsii.member(jsii_name="putWindowsNodeConfig")
    def put_windows_node_config(
        self,
        *,
        osversion: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param osversion: The OS Version of the windows nodepool.Values are OS_VERSION_UNSPECIFIED,OS_VERSION_LTSC2019 and OS_VERSION_LTSC2022. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#osversion ContainerNodePool#osversion}
        '''
        value = ContainerNodePoolNodeConfigWindowsNodeConfig(osversion=osversion)

        return typing.cast(None, jsii.invoke(self, "putWindowsNodeConfig", [value]))

    @jsii.member(jsii_name="putWorkloadMetadataConfig")
    def put_workload_metadata_config(self, *, mode: builtins.str) -> None:
        '''
        :param mode: Mode is the configuration for how to expose metadata to workloads running on the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#mode ContainerNodePool#mode}
        '''
        value = ContainerNodePoolNodeConfigWorkloadMetadataConfig(mode=mode)

        return typing.cast(None, jsii.invoke(self, "putWorkloadMetadataConfig", [value]))

    @jsii.member(jsii_name="resetAdvancedMachineFeatures")
    def reset_advanced_machine_features(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedMachineFeatures", []))

    @jsii.member(jsii_name="resetBootDiskKmsKey")
    def reset_boot_disk_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskKmsKey", []))

    @jsii.member(jsii_name="resetConfidentialNodes")
    def reset_confidential_nodes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidentialNodes", []))

    @jsii.member(jsii_name="resetContainerdConfig")
    def reset_containerd_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerdConfig", []))

    @jsii.member(jsii_name="resetDiskSizeGb")
    def reset_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskSizeGb", []))

    @jsii.member(jsii_name="resetDiskType")
    def reset_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskType", []))

    @jsii.member(jsii_name="resetEnableConfidentialStorage")
    def reset_enable_confidential_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableConfidentialStorage", []))

    @jsii.member(jsii_name="resetEphemeralStorageLocalSsdConfig")
    def reset_ephemeral_storage_local_ssd_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEphemeralStorageLocalSsdConfig", []))

    @jsii.member(jsii_name="resetFastSocket")
    def reset_fast_socket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFastSocket", []))

    @jsii.member(jsii_name="resetFlexStart")
    def reset_flex_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlexStart", []))

    @jsii.member(jsii_name="resetGcfsConfig")
    def reset_gcfs_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcfsConfig", []))

    @jsii.member(jsii_name="resetGuestAccelerator")
    def reset_guest_accelerator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGuestAccelerator", []))

    @jsii.member(jsii_name="resetGvnic")
    def reset_gvnic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGvnic", []))

    @jsii.member(jsii_name="resetHostMaintenancePolicy")
    def reset_host_maintenance_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostMaintenancePolicy", []))

    @jsii.member(jsii_name="resetImageType")
    def reset_image_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageType", []))

    @jsii.member(jsii_name="resetKubeletConfig")
    def reset_kubelet_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubeletConfig", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLinuxNodeConfig")
    def reset_linux_node_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinuxNodeConfig", []))

    @jsii.member(jsii_name="resetLocalNvmeSsdBlockConfig")
    def reset_local_nvme_ssd_block_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalNvmeSsdBlockConfig", []))

    @jsii.member(jsii_name="resetLocalSsdCount")
    def reset_local_ssd_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalSsdCount", []))

    @jsii.member(jsii_name="resetLocalSsdEncryptionMode")
    def reset_local_ssd_encryption_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalSsdEncryptionMode", []))

    @jsii.member(jsii_name="resetLoggingVariant")
    def reset_logging_variant(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingVariant", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @jsii.member(jsii_name="resetMaxRunDuration")
    def reset_max_run_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRunDuration", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetMinCpuPlatform")
    def reset_min_cpu_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinCpuPlatform", []))

    @jsii.member(jsii_name="resetNodeGroup")
    def reset_node_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeGroup", []))

    @jsii.member(jsii_name="resetOauthScopes")
    def reset_oauth_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthScopes", []))

    @jsii.member(jsii_name="resetPreemptible")
    def reset_preemptible(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreemptible", []))

    @jsii.member(jsii_name="resetReservationAffinity")
    def reset_reservation_affinity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservationAffinity", []))

    @jsii.member(jsii_name="resetResourceLabels")
    def reset_resource_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceLabels", []))

    @jsii.member(jsii_name="resetResourceManagerTags")
    def reset_resource_manager_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceManagerTags", []))

    @jsii.member(jsii_name="resetSecondaryBootDisks")
    def reset_secondary_boot_disks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryBootDisks", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetShieldedInstanceConfig")
    def reset_shielded_instance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShieldedInstanceConfig", []))

    @jsii.member(jsii_name="resetSoleTenantConfig")
    def reset_sole_tenant_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSoleTenantConfig", []))

    @jsii.member(jsii_name="resetSpot")
    def reset_spot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpot", []))

    @jsii.member(jsii_name="resetStoragePools")
    def reset_storage_pools(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStoragePools", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTaint")
    def reset_taint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaint", []))

    @jsii.member(jsii_name="resetWindowsNodeConfig")
    def reset_windows_node_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowsNodeConfig", []))

    @jsii.member(jsii_name="resetWorkloadMetadataConfig")
    def reset_workload_metadata_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkloadMetadataConfig", []))

    @builtins.property
    @jsii.member(jsii_name="advancedMachineFeatures")
    def advanced_machine_features(
        self,
    ) -> ContainerNodePoolNodeConfigAdvancedMachineFeaturesOutputReference:
        return typing.cast(ContainerNodePoolNodeConfigAdvancedMachineFeaturesOutputReference, jsii.get(self, "advancedMachineFeatures"))

    @builtins.property
    @jsii.member(jsii_name="confidentialNodes")
    def confidential_nodes(
        self,
    ) -> ContainerNodePoolNodeConfigConfidentialNodesOutputReference:
        return typing.cast(ContainerNodePoolNodeConfigConfidentialNodesOutputReference, jsii.get(self, "confidentialNodes"))

    @builtins.property
    @jsii.member(jsii_name="containerdConfig")
    def containerd_config(
        self,
    ) -> ContainerNodePoolNodeConfigContainerdConfigOutputReference:
        return typing.cast(ContainerNodePoolNodeConfigContainerdConfigOutputReference, jsii.get(self, "containerdConfig"))

    @builtins.property
    @jsii.member(jsii_name="effectiveTaints")
    def effective_taints(self) -> ContainerNodePoolNodeConfigEffectiveTaintsList:
        return typing.cast(ContainerNodePoolNodeConfigEffectiveTaintsList, jsii.get(self, "effectiveTaints"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorageLocalSsdConfig")
    def ephemeral_storage_local_ssd_config(
        self,
    ) -> ContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfigOutputReference:
        return typing.cast(ContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfigOutputReference, jsii.get(self, "ephemeralStorageLocalSsdConfig"))

    @builtins.property
    @jsii.member(jsii_name="fastSocket")
    def fast_socket(self) -> ContainerNodePoolNodeConfigFastSocketOutputReference:
        return typing.cast(ContainerNodePoolNodeConfigFastSocketOutputReference, jsii.get(self, "fastSocket"))

    @builtins.property
    @jsii.member(jsii_name="gcfsConfig")
    def gcfs_config(self) -> ContainerNodePoolNodeConfigGcfsConfigOutputReference:
        return typing.cast(ContainerNodePoolNodeConfigGcfsConfigOutputReference, jsii.get(self, "gcfsConfig"))

    @builtins.property
    @jsii.member(jsii_name="guestAccelerator")
    def guest_accelerator(self) -> ContainerNodePoolNodeConfigGuestAcceleratorList:
        return typing.cast(ContainerNodePoolNodeConfigGuestAcceleratorList, jsii.get(self, "guestAccelerator"))

    @builtins.property
    @jsii.member(jsii_name="gvnic")
    def gvnic(self) -> ContainerNodePoolNodeConfigGvnicOutputReference:
        return typing.cast(ContainerNodePoolNodeConfigGvnicOutputReference, jsii.get(self, "gvnic"))

    @builtins.property
    @jsii.member(jsii_name="hostMaintenancePolicy")
    def host_maintenance_policy(
        self,
    ) -> ContainerNodePoolNodeConfigHostMaintenancePolicyOutputReference:
        return typing.cast(ContainerNodePoolNodeConfigHostMaintenancePolicyOutputReference, jsii.get(self, "hostMaintenancePolicy"))

    @builtins.property
    @jsii.member(jsii_name="kubeletConfig")
    def kubelet_config(self) -> ContainerNodePoolNodeConfigKubeletConfigOutputReference:
        return typing.cast(ContainerNodePoolNodeConfigKubeletConfigOutputReference, jsii.get(self, "kubeletConfig"))

    @builtins.property
    @jsii.member(jsii_name="linuxNodeConfig")
    def linux_node_config(
        self,
    ) -> ContainerNodePoolNodeConfigLinuxNodeConfigOutputReference:
        return typing.cast(ContainerNodePoolNodeConfigLinuxNodeConfigOutputReference, jsii.get(self, "linuxNodeConfig"))

    @builtins.property
    @jsii.member(jsii_name="localNvmeSsdBlockConfig")
    def local_nvme_ssd_block_config(
        self,
    ) -> ContainerNodePoolNodeConfigLocalNvmeSsdBlockConfigOutputReference:
        return typing.cast(ContainerNodePoolNodeConfigLocalNvmeSsdBlockConfigOutputReference, jsii.get(self, "localNvmeSsdBlockConfig"))

    @builtins.property
    @jsii.member(jsii_name="reservationAffinity")
    def reservation_affinity(
        self,
    ) -> "ContainerNodePoolNodeConfigReservationAffinityOutputReference":
        return typing.cast("ContainerNodePoolNodeConfigReservationAffinityOutputReference", jsii.get(self, "reservationAffinity"))

    @builtins.property
    @jsii.member(jsii_name="secondaryBootDisks")
    def secondary_boot_disks(
        self,
    ) -> "ContainerNodePoolNodeConfigSecondaryBootDisksList":
        return typing.cast("ContainerNodePoolNodeConfigSecondaryBootDisksList", jsii.get(self, "secondaryBootDisks"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfig")
    def shielded_instance_config(
        self,
    ) -> "ContainerNodePoolNodeConfigShieldedInstanceConfigOutputReference":
        return typing.cast("ContainerNodePoolNodeConfigShieldedInstanceConfigOutputReference", jsii.get(self, "shieldedInstanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="soleTenantConfig")
    def sole_tenant_config(
        self,
    ) -> "ContainerNodePoolNodeConfigSoleTenantConfigOutputReference":
        return typing.cast("ContainerNodePoolNodeConfigSoleTenantConfigOutputReference", jsii.get(self, "soleTenantConfig"))

    @builtins.property
    @jsii.member(jsii_name="taint")
    def taint(self) -> "ContainerNodePoolNodeConfigTaintList":
        return typing.cast("ContainerNodePoolNodeConfigTaintList", jsii.get(self, "taint"))

    @builtins.property
    @jsii.member(jsii_name="windowsNodeConfig")
    def windows_node_config(
        self,
    ) -> "ContainerNodePoolNodeConfigWindowsNodeConfigOutputReference":
        return typing.cast("ContainerNodePoolNodeConfigWindowsNodeConfigOutputReference", jsii.get(self, "windowsNodeConfig"))

    @builtins.property
    @jsii.member(jsii_name="workloadMetadataConfig")
    def workload_metadata_config(
        self,
    ) -> "ContainerNodePoolNodeConfigWorkloadMetadataConfigOutputReference":
        return typing.cast("ContainerNodePoolNodeConfigWorkloadMetadataConfigOutputReference", jsii.get(self, "workloadMetadataConfig"))

    @builtins.property
    @jsii.member(jsii_name="advancedMachineFeaturesInput")
    def advanced_machine_features_input(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigAdvancedMachineFeatures]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigAdvancedMachineFeatures], jsii.get(self, "advancedMachineFeaturesInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskKmsKeyInput")
    def boot_disk_kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootDiskKmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="confidentialNodesInput")
    def confidential_nodes_input(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigConfidentialNodes]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigConfidentialNodes], jsii.get(self, "confidentialNodesInput"))

    @builtins.property
    @jsii.member(jsii_name="containerdConfigInput")
    def containerd_config_input(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigContainerdConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigContainerdConfig], jsii.get(self, "containerdConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGbInput")
    def disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="diskTypeInput")
    def disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="enableConfidentialStorageInput")
    def enable_confidential_storage_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableConfidentialStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorageLocalSsdConfigInput")
    def ephemeral_storage_local_ssd_config_input(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig], jsii.get(self, "ephemeralStorageLocalSsdConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fastSocketInput")
    def fast_socket_input(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigFastSocket]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigFastSocket], jsii.get(self, "fastSocketInput"))

    @builtins.property
    @jsii.member(jsii_name="flexStartInput")
    def flex_start_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "flexStartInput"))

    @builtins.property
    @jsii.member(jsii_name="gcfsConfigInput")
    def gcfs_config_input(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigGcfsConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigGcfsConfig], jsii.get(self, "gcfsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="guestAcceleratorInput")
    def guest_accelerator_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigGuestAccelerator]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigGuestAccelerator]]], jsii.get(self, "guestAcceleratorInput"))

    @builtins.property
    @jsii.member(jsii_name="gvnicInput")
    def gvnic_input(self) -> typing.Optional[ContainerNodePoolNodeConfigGvnic]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigGvnic], jsii.get(self, "gvnicInput"))

    @builtins.property
    @jsii.member(jsii_name="hostMaintenancePolicyInput")
    def host_maintenance_policy_input(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigHostMaintenancePolicy]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigHostMaintenancePolicy], jsii.get(self, "hostMaintenancePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="imageTypeInput")
    def image_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="kubeletConfigInput")
    def kubelet_config_input(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigKubeletConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigKubeletConfig], jsii.get(self, "kubeletConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="linuxNodeConfigInput")
    def linux_node_config_input(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigLinuxNodeConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigLinuxNodeConfig], jsii.get(self, "linuxNodeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="localNvmeSsdBlockConfigInput")
    def local_nvme_ssd_block_config_input(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig], jsii.get(self, "localNvmeSsdBlockConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="localSsdCountInput")
    def local_ssd_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "localSsdCountInput"))

    @builtins.property
    @jsii.member(jsii_name="localSsdEncryptionModeInput")
    def local_ssd_encryption_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localSsdEncryptionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingVariantInput")
    def logging_variant_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loggingVariantInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRunDurationInput")
    def max_run_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxRunDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatformInput")
    def min_cpu_platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minCpuPlatformInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeGroupInput")
    def node_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthScopesInput")
    def oauth_scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "oauthScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="preemptibleInput")
    def preemptible_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preemptibleInput"))

    @builtins.property
    @jsii.member(jsii_name="reservationAffinityInput")
    def reservation_affinity_input(
        self,
    ) -> typing.Optional["ContainerNodePoolNodeConfigReservationAffinity"]:
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigReservationAffinity"], jsii.get(self, "reservationAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceLabelsInput")
    def resource_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "resourceLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceManagerTagsInput")
    def resource_manager_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "resourceManagerTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryBootDisksInput")
    def secondary_boot_disks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerNodePoolNodeConfigSecondaryBootDisks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerNodePoolNodeConfigSecondaryBootDisks"]]], jsii.get(self, "secondaryBootDisksInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfigInput")
    def shielded_instance_config_input(
        self,
    ) -> typing.Optional["ContainerNodePoolNodeConfigShieldedInstanceConfig"]:
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigShieldedInstanceConfig"], jsii.get(self, "shieldedInstanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="soleTenantConfigInput")
    def sole_tenant_config_input(
        self,
    ) -> typing.Optional["ContainerNodePoolNodeConfigSoleTenantConfig"]:
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigSoleTenantConfig"], jsii.get(self, "soleTenantConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="spotInput")
    def spot_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "spotInput"))

    @builtins.property
    @jsii.member(jsii_name="storagePoolsInput")
    def storage_pools_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "storagePoolsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="taintInput")
    def taint_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerNodePoolNodeConfigTaint"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerNodePoolNodeConfigTaint"]]], jsii.get(self, "taintInput"))

    @builtins.property
    @jsii.member(jsii_name="windowsNodeConfigInput")
    def windows_node_config_input(
        self,
    ) -> typing.Optional["ContainerNodePoolNodeConfigWindowsNodeConfig"]:
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigWindowsNodeConfig"], jsii.get(self, "windowsNodeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadMetadataConfigInput")
    def workload_metadata_config_input(
        self,
    ) -> typing.Optional["ContainerNodePoolNodeConfigWorkloadMetadataConfig"]:
        return typing.cast(typing.Optional["ContainerNodePoolNodeConfigWorkloadMetadataConfig"], jsii.get(self, "workloadMetadataConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskKmsKey")
    def boot_disk_kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootDiskKmsKey"))

    @boot_disk_kms_key.setter
    def boot_disk_kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c00eb286d3e6893dad5a267edbc41c9d18855c3772561890e6299afcad154bef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskKmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ee93eccaa32cf9cbb85623b4c858a278e08c6f4266cde03ad54c5ceea3885b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskType")
    def disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskType"))

    @disk_type.setter
    def disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5c2e9108b3abdc3bc7beef5eae561cbe84b85c072833973a8ad8136bae6cfc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableConfidentialStorage")
    def enable_confidential_storage(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableConfidentialStorage"))

    @enable_confidential_storage.setter
    def enable_confidential_storage(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f71a3285d4536b1082236a18e741adb3d1f5ceeb6f351a7d76a0b53a422d18c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableConfidentialStorage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flexStart")
    def flex_start(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "flexStart"))

    @flex_start.setter
    def flex_start(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a7fa3dfa7250237415876f14a6684c7aeb6b18a9bc1d4692d1183a705ff51c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flexStart", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageType")
    def image_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageType"))

    @image_type.setter
    def image_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67ac811a34dcc6f8b77cf0a91f76a3a3fb9eaf339231f04fd01d845942e4f2ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9f3c53632eb51e52290811042139da72dd98abc37666ed213ed66b376a4b327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localSsdCount")
    def local_ssd_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "localSsdCount"))

    @local_ssd_count.setter
    def local_ssd_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__339fc7b30e25660067113a4a2090e0dcb35253864b89048763d26123df7e64ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localSsdCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localSsdEncryptionMode")
    def local_ssd_encryption_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localSsdEncryptionMode"))

    @local_ssd_encryption_mode.setter
    def local_ssd_encryption_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e799e04921c80bc607c6bb8a9d247315d01037617ad7c0f8e9f15a867201540f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localSsdEncryptionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loggingVariant")
    def logging_variant(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loggingVariant"))

    @logging_variant.setter
    def logging_variant(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4a6aadb08ca6cb9b35056a341e8b7b91fd36eb43bf79c19ac48d844300521b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingVariant", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb0161bbe3e5f64ea516ea6e3abc134c47a7ae1c82575f1b55842ac5cc87ae00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRunDuration")
    def max_run_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxRunDuration"))

    @max_run_duration.setter
    def max_run_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d9ac0afc1dba66badcc62eb741d2178e296e25085c9fc967db808f2979168d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRunDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__831a1c9d624222f3b1bdf9eb93488e80333249f48dc558af7048c3f360deb5af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatform")
    def min_cpu_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minCpuPlatform"))

    @min_cpu_platform.setter
    def min_cpu_platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0655d66cbc4934d46aa1e11143c93fd5f5a910adaea72a5764a414a479763597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCpuPlatform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeGroup")
    def node_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeGroup"))

    @node_group.setter
    def node_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54e92cd9bafa0142dbb4902a8f9209a21b7b7a8e88b4c0daa0d2ba544c0c2a1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthScopes")
    def oauth_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthScopes"))

    @oauth_scopes.setter
    def oauth_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c983ba1dbc70a4dcebf6e2144b26b27de90d534f16119057f0d0630d14be4c61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preemptible")
    def preemptible(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preemptible"))

    @preemptible.setter
    def preemptible(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22a9a3f63e92a95f12c9eb15926f757148868b2516f3578745daf6e0bf1b1c34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preemptible", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceLabels")
    def resource_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "resourceLabels"))

    @resource_labels.setter
    def resource_labels(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__941f1b38a5b7e374e4d6513f0e54a23f063b3d8d487abdda9343daaf36fb2ea8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceManagerTags")
    def resource_manager_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "resourceManagerTags"))

    @resource_manager_tags.setter
    def resource_manager_tags(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3667df33d9eb8eae6c8c46a5ee54ac5a06bd0dd9817ac5ca64efd02701d3b49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceManagerTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67d35a8a96cadfdd89ea4377798c17945517bb2d074c90e1c4fd465fb246856e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="spot")
    def spot(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "spot"))

    @spot.setter
    def spot(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e93bbaeb821cda1f2fdb5721148276912ff0e95fc753d96d6cc71f730f967ae9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storagePools")
    def storage_pools(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "storagePools"))

    @storage_pools.setter
    def storage_pools(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__661626fcdcdd7b734ffe1390f33855d48d680f93a0d00acfcf98c5b9e37e8438)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storagePools", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__955aa32132f0c40b06ce7c723e0140da9caad79983aed185eb0c1796c347f978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerNodePoolNodeConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNodeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__351229fec65f01f2822233722ea04249a135f50dd7735cd72d4763ff527ad2c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigReservationAffinity",
    jsii_struct_bases=[],
    name_mapping={
        "consume_reservation_type": "consumeReservationType",
        "key": "key",
        "values": "values",
    },
)
class ContainerNodePoolNodeConfigReservationAffinity:
    def __init__(
        self,
        *,
        consume_reservation_type: builtins.str,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param consume_reservation_type: Corresponds to the type of reservation consumption. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#consume_reservation_type ContainerNodePool#consume_reservation_type}
        :param key: The label key of a reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#key ContainerNodePool#key}
        :param values: The label values of the reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#values ContainerNodePool#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__088da2d8e80cb55ead4282afb73e46f00dadf9e3d2bd4f45cb367e875f1673d2)
            check_type(argname="argument consume_reservation_type", value=consume_reservation_type, expected_type=type_hints["consume_reservation_type"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "consume_reservation_type": consume_reservation_type,
        }
        if key is not None:
            self._values["key"] = key
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def consume_reservation_type(self) -> builtins.str:
        '''Corresponds to the type of reservation consumption.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#consume_reservation_type ContainerNodePool#consume_reservation_type}
        '''
        result = self._values.get("consume_reservation_type")
        assert result is not None, "Required property 'consume_reservation_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''The label key of a reservation resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#key ContainerNodePool#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The label values of the reservation resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#values ContainerNodePool#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigReservationAffinity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNodeConfigReservationAffinityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigReservationAffinityOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7029c69ee592859f0782359f25b3e2ff512040dd308bc178f00ddd0039c2e6fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="consumeReservationTypeInput")
    def consume_reservation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumeReservationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="consumeReservationType")
    def consume_reservation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumeReservationType"))

    @consume_reservation_type.setter
    def consume_reservation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7427a98ea1b1239c15c0e0827b08c41f69b3e8dd22f13192395e1ea4417bea29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumeReservationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__918e04575214bec1185c71689b986834d560849bbfe3184afc6880ccc9bd8197)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f83d85a0ece0e057a0e49a178d248187f2f518255200a282fb575a5642814eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigReservationAffinity]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigReservationAffinity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNodeConfigReservationAffinity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0965988de54a6815b2ddad06e8b986a9751125cb17230f2e0eede337edaa8463)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigSecondaryBootDisks",
    jsii_struct_bases=[],
    name_mapping={"disk_image": "diskImage", "mode": "mode"},
)
class ContainerNodePoolNodeConfigSecondaryBootDisks:
    def __init__(
        self,
        *,
        disk_image: builtins.str,
        mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_image: Disk image to create the secondary boot disk from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#disk_image ContainerNodePool#disk_image}
        :param mode: Mode for how the secondary boot disk is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#mode ContainerNodePool#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eab58d8968489b23e5fd4018a4e483add0697d842c865ff064c355ce28ce165)
            check_type(argname="argument disk_image", value=disk_image, expected_type=type_hints["disk_image"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disk_image": disk_image,
        }
        if mode is not None:
            self._values["mode"] = mode

    @builtins.property
    def disk_image(self) -> builtins.str:
        '''Disk image to create the secondary boot disk from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#disk_image ContainerNodePool#disk_image}
        '''
        result = self._values.get("disk_image")
        assert result is not None, "Required property 'disk_image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Mode for how the secondary boot disk is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#mode ContainerNodePool#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigSecondaryBootDisks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNodeConfigSecondaryBootDisksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigSecondaryBootDisksList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02b38d5b0ea2c4cd8eaaeb55c0dceb09d5bed5e957aa5c32df56f551499e9311)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerNodePoolNodeConfigSecondaryBootDisksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cee597f5406c0478c312374dce8c920f49c43441db6268ea86102b374e8372a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerNodePoolNodeConfigSecondaryBootDisksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e9fa07f52849295ca3b5f9edaa40d28239d956c9bc1ef878e327c5d7e66b901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bf6620d06f8d1587180510b6c9977254d64c56a9b21edabfc3cf86b0efa57f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__819ad13c8d3425668001d08ee3136d21c3a93f7ceb949d7e8d127eeee0cdee6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigSecondaryBootDisks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigSecondaryBootDisks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigSecondaryBootDisks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed3ea369fa9c0bb50f1ef809f64e047d32d488f29382f07571fe643ba7b8b4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerNodePoolNodeConfigSecondaryBootDisksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigSecondaryBootDisksOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d7244b4640ce5d89d9ccc082229db1db0f698334143bbd73227deab4b5e4f5a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @builtins.property
    @jsii.member(jsii_name="diskImageInput")
    def disk_image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskImageInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="diskImage")
    def disk_image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskImage"))

    @disk_image.setter
    def disk_image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e60d29538a2491e2b762459bf8cdabf54bfe8b15bd3ce1b5f63e0d388b295eae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskImage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9111b0a2c0ea3583301bfc0f078fd4f0719aa5243a5946c52c5e9d29a496dcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNodeConfigSecondaryBootDisks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNodeConfigSecondaryBootDisks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNodeConfigSecondaryBootDisks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e935bee246778b938f506b8b674ed2b76e687a51c6406efc5d569c98eb0cd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigShieldedInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_integrity_monitoring": "enableIntegrityMonitoring",
        "enable_secure_boot": "enableSecureBoot",
    },
)
class ContainerNodePoolNodeConfigShieldedInstanceConfig:
    def __init__(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Defines whether the instance has integrity monitoring enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enable_integrity_monitoring ContainerNodePool#enable_integrity_monitoring}
        :param enable_secure_boot: Defines whether the instance has Secure Boot enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enable_secure_boot ContainerNodePool#enable_secure_boot}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bd4c5365f55d4bdcdaa43c31fc4b02241fb22d4b5dc84c4a9045a301deee8f7)
            check_type(argname="argument enable_integrity_monitoring", value=enable_integrity_monitoring, expected_type=type_hints["enable_integrity_monitoring"])
            check_type(argname="argument enable_secure_boot", value=enable_secure_boot, expected_type=type_hints["enable_secure_boot"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_integrity_monitoring is not None:
            self._values["enable_integrity_monitoring"] = enable_integrity_monitoring
        if enable_secure_boot is not None:
            self._values["enable_secure_boot"] = enable_secure_boot

    @builtins.property
    def enable_integrity_monitoring(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether the instance has integrity monitoring enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enable_integrity_monitoring ContainerNodePool#enable_integrity_monitoring}
        '''
        result = self._values.get("enable_integrity_monitoring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_secure_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether the instance has Secure Boot enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enable_secure_boot ContainerNodePool#enable_secure_boot}
        '''
        result = self._values.get("enable_secure_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigShieldedInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNodeConfigShieldedInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigShieldedInstanceConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e23b69d931b080e8470cc408b762f0fe5516a235ab283677c12003b004b5ae5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableIntegrityMonitoring")
    def reset_enable_integrity_monitoring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableIntegrityMonitoring", []))

    @jsii.member(jsii_name="resetEnableSecureBoot")
    def reset_enable_secure_boot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSecureBoot", []))

    @builtins.property
    @jsii.member(jsii_name="enableIntegrityMonitoringInput")
    def enable_integrity_monitoring_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableIntegrityMonitoringInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSecureBootInput")
    def enable_secure_boot_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSecureBootInput"))

    @builtins.property
    @jsii.member(jsii_name="enableIntegrityMonitoring")
    def enable_integrity_monitoring(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableIntegrityMonitoring"))

    @enable_integrity_monitoring.setter
    def enable_integrity_monitoring(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12cbf5e6ec7b49db2cc4c35263edd946dfda50593241c940030aeeaa0c164967)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableIntegrityMonitoring", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableSecureBoot")
    def enable_secure_boot(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSecureBoot"))

    @enable_secure_boot.setter
    def enable_secure_boot(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea69b37e8b4234d8d060f1c87229ec8874601c8265532a7cec67897c2ba15dc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSecureBoot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigShieldedInstanceConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigShieldedInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNodeConfigShieldedInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9ef156292c2a9d0d878e672ae2467574f9c8893156418bf2d8e241296cca664)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigSoleTenantConfig",
    jsii_struct_bases=[],
    name_mapping={"node_affinity": "nodeAffinity"},
)
class ContainerNodePoolNodeConfigSoleTenantConfig:
    def __init__(
        self,
        *,
        node_affinity: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param node_affinity: node_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#node_affinity ContainerNodePool#node_affinity}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f01db3ae9bc1942532dd9be66837c1ac53e0609e050fcfca7cc7d64d4f64976d)
            check_type(argname="argument node_affinity", value=node_affinity, expected_type=type_hints["node_affinity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "node_affinity": node_affinity,
        }

    @builtins.property
    def node_affinity(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity"]]:
        '''node_affinity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#node_affinity ContainerNodePool#node_affinity}
        '''
        result = self._values.get("node_affinity")
        assert result is not None, "Required property 'node_affinity' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigSoleTenantConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "operator": "operator", "values": "values"},
)
class ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity:
    def __init__(
        self,
        *,
        key: builtins.str,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: . Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#key ContainerNodePool#key}
        :param operator: . Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#operator ContainerNodePool#operator}
        :param values: . Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#values ContainerNodePool#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28b65e26105c363e9609cd55dcfed444420912892b520ffb3d025eeef0e65201)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#key ContainerNodePool#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#operator ContainerNodePool#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#values ContainerNodePool#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinityList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c14ffbb53166762893d254a1b8ac1a722e9805798a7228600ba890e4e6dab32c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07fda06f6965b024ef8593537c1a6cf562bcf74a934fd5c69a804d1ebfad1ea9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89f3774954be85b6fe251b4894f9a200985558d4cc13b40dc38c1a4614b29461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b0309c96ac515dc7c74d32a416892c1497a2d98ba08e23d1de6d8e635ed6886)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5bcb8b9453e0534f9f902d734a42d8d4d43d10853199b116d01e0e7a8a61a0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b6ed2bed07379aab04b981c4b3ab3472580dc0416fe7b3dcf59accad0957ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinityOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c49ddd8b0c13f0f50d5d58bc37d317ed4c57ea65157b8fbe85fd56e0d988399)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3c825c0a25110e271154e8b76a5997a461cc257ef9b8d60817dcb28493695bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8cf35e54a575c4f06eab0bacb50cc6b17da4ffe3ab78dfb1fd2bb8b7ea293a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4805160176a74baad41c8a3a0baab8b32e9a3c24ee01eb77de960b75ab63c61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86d1c81b4d090939fa0d9c86cd8f250f6c33f44c25a5ec0fa04c24d619875991)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerNodePoolNodeConfigSoleTenantConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigSoleTenantConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05c82808f909dadca9c92ab2bd308ca79cff911551c364cd9326bc09e0d1a901)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodeAffinity")
    def put_node_affinity(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3562adf12ca919893bfaf803b36585774ebd88b2c2a3a6be84f311bfe08a4a2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeAffinity", [value]))

    @builtins.property
    @jsii.member(jsii_name="nodeAffinity")
    def node_affinity(
        self,
    ) -> ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinityList:
        return typing.cast(ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinityList, jsii.get(self, "nodeAffinity"))

    @builtins.property
    @jsii.member(jsii_name="nodeAffinityInput")
    def node_affinity_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity]]], jsii.get(self, "nodeAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigSoleTenantConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigSoleTenantConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNodeConfigSoleTenantConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4f61d68a12e9f2dd65e43e22f3d522d307ca799e06fee7663e1f6933c93f2dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigTaint",
    jsii_struct_bases=[],
    name_mapping={"effect": "effect", "key": "key", "value": "value"},
)
class ContainerNodePoolNodeConfigTaint:
    def __init__(
        self,
        *,
        effect: builtins.str,
        key: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param effect: Effect for taint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#effect ContainerNodePool#effect}
        :param key: Key for taint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#key ContainerNodePool#key}
        :param value: Value for taint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#value ContainerNodePool#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0016f2b3e6f923bf4aafda4f4fcb84698611d975b253217eaa8988bd769ff342)
            check_type(argname="argument effect", value=effect, expected_type=type_hints["effect"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "effect": effect,
            "key": key,
            "value": value,
        }

    @builtins.property
    def effect(self) -> builtins.str:
        '''Effect for taint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#effect ContainerNodePool#effect}
        '''
        result = self._values.get("effect")
        assert result is not None, "Required property 'effect' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Key for taint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#key ContainerNodePool#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Value for taint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#value ContainerNodePool#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigTaint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNodeConfigTaintList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigTaintList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ff36a3028ba631c939419d797d77ad2107326b42ac7ec81d20bf22ac84af6f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerNodePoolNodeConfigTaintOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8de42ca62f8d4745ad644beb396b4ff6d7829935c23e449b318e8552eca31d7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerNodePoolNodeConfigTaintOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d62e940a5e77e61e8f6c3ad668945e0e2085b2cc2ef86502c150dd86ef84868)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f3caa69283592af3dacab34bd75924bd3262dcc5dc9bfbee391ae8eae5f547e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e24a867663a9b86fc8694b9aa88826f08b539e58d827e5e01092e07917ec070)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigTaint]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigTaint]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigTaint]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec99422975ba06b9c5b1ee9265fa7fdb1634b9967043d9fb526a0d0be16c9605)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerNodePoolNodeConfigTaintOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigTaintOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aea654ec628830b7ccf54274d3fc867cb84f98ddb5357dd92505f166550d52e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="effectInput")
    def effect_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "effectInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="effect")
    def effect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effect"))

    @effect.setter
    def effect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__176dec68eb891a03e4bcf1c8782ae4284f82e954b002cb57a109ea44fead872f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f59c2f2f06f06954b00f893aa9c5e2c7d3e5d450d1ee39e73a13e2c82bb19c11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19400fff3f53566e99bf1a1faa2a3599f41d0b848b4fab2bd37570dc8bf80fa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNodeConfigTaint]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNodeConfigTaint]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNodeConfigTaint]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53e5f500a6136a3667f96d7a012bb98c944c3665047e671e09fda862e600ed98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigWindowsNodeConfig",
    jsii_struct_bases=[],
    name_mapping={"osversion": "osversion"},
)
class ContainerNodePoolNodeConfigWindowsNodeConfig:
    def __init__(self, *, osversion: typing.Optional[builtins.str] = None) -> None:
        '''
        :param osversion: The OS Version of the windows nodepool.Values are OS_VERSION_UNSPECIFIED,OS_VERSION_LTSC2019 and OS_VERSION_LTSC2022. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#osversion ContainerNodePool#osversion}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ded0a6d5f90af61780a6dec7da9cf0735338931ec54c5586f01dbdf2bc90f318)
            check_type(argname="argument osversion", value=osversion, expected_type=type_hints["osversion"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if osversion is not None:
            self._values["osversion"] = osversion

    @builtins.property
    def osversion(self) -> typing.Optional[builtins.str]:
        '''The OS Version of the windows nodepool.Values are OS_VERSION_UNSPECIFIED,OS_VERSION_LTSC2019 and OS_VERSION_LTSC2022.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#osversion ContainerNodePool#osversion}
        '''
        result = self._values.get("osversion")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigWindowsNodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNodeConfigWindowsNodeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigWindowsNodeConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73853482cb03ab41f6d177bb29bb8b95b66d3e18fef029850ebb88567b580a1e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOsversion")
    def reset_osversion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsversion", []))

    @builtins.property
    @jsii.member(jsii_name="osversionInput")
    def osversion_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osversionInput"))

    @builtins.property
    @jsii.member(jsii_name="osversion")
    def osversion(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osversion"))

    @osversion.setter
    def osversion(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0718d5606662b51863bafde105ea8960e7ddecd98111a7c022d32a553e6512f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osversion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigWindowsNodeConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigWindowsNodeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNodeConfigWindowsNodeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78e959055bf1cc1403b434e4373b5643162d202ae0bb60eb9b1808479fed2d14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigWorkloadMetadataConfig",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode"},
)
class ContainerNodePoolNodeConfigWorkloadMetadataConfig:
    def __init__(self, *, mode: builtins.str) -> None:
        '''
        :param mode: Mode is the configuration for how to expose metadata to workloads running on the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#mode ContainerNodePool#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab9d9c2423d84eafa652f6e5531706f5eb79ba606d1e5853005903a69bb036ab)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''Mode is the configuration for how to expose metadata to workloads running on the node.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#mode ContainerNodePool#mode}
        '''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolNodeConfigWorkloadMetadataConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolNodeConfigWorkloadMetadataConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolNodeConfigWorkloadMetadataConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b88f03bca74ece14604b3458345bd9f0f0251c767118f20a4e5395d83dc4b3d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__377012a99660970a4a1bc85c5b54ecdf2050dc490f32aaa4e409468aeef8c5cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerNodePoolNodeConfigWorkloadMetadataConfig]:
        return typing.cast(typing.Optional[ContainerNodePoolNodeConfigWorkloadMetadataConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolNodeConfigWorkloadMetadataConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baf653d4d5774b609af62d22a96b52276860e5c38f9e5d57d2d4cc08e6d4365a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolPlacementPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "policy_name": "policyName",
        "tpu_topology": "tpuTopology",
    },
)
class ContainerNodePoolPlacementPolicy:
    def __init__(
        self,
        *,
        type: builtins.str,
        policy_name: typing.Optional[builtins.str] = None,
        tpu_topology: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type defines the type of placement policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#type ContainerNodePool#type}
        :param policy_name: If set, refers to the name of a custom resource policy supplied by the user. The resource policy must be in the same project and region as the node pool. If not found, InvalidArgument error is returned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#policy_name ContainerNodePool#policy_name}
        :param tpu_topology: The TPU topology like "2x4" or "2x2x2". https://cloud.google.com/kubernetes-engine/docs/concepts/plan-tpus#topology. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#tpu_topology ContainerNodePool#tpu_topology}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e6642538ef61b97bc1af6976ae9895e8312a74aa0446e5079055f2904b6e87)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument tpu_topology", value=tpu_topology, expected_type=type_hints["tpu_topology"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if policy_name is not None:
            self._values["policy_name"] = policy_name
        if tpu_topology is not None:
            self._values["tpu_topology"] = tpu_topology

    @builtins.property
    def type(self) -> builtins.str:
        '''Type defines the type of placement policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#type ContainerNodePool#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''If set, refers to the name of a custom resource policy supplied by the user.

        The resource policy must be in the same project and region as the node pool. If not found, InvalidArgument error is returned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#policy_name ContainerNodePool#policy_name}
        '''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpu_topology(self) -> typing.Optional[builtins.str]:
        '''The TPU topology like "2x4" or "2x2x2". https://cloud.google.com/kubernetes-engine/docs/concepts/plan-tpus#topology.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#tpu_topology ContainerNodePool#tpu_topology}
        '''
        result = self._values.get("tpu_topology")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolPlacementPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolPlacementPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolPlacementPolicyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9d753c011ca10d1ea912432a99be94156fce69370d4da61467f224077eae46d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPolicyName")
    def reset_policy_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyName", []))

    @jsii.member(jsii_name="resetTpuTopology")
    def reset_tpu_topology(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpuTopology", []))

    @builtins.property
    @jsii.member(jsii_name="policyNameInput")
    def policy_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tpuTopologyInput")
    def tpu_topology_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tpuTopologyInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyName"))

    @policy_name.setter
    def policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08e898baf46c4718917bf8218bdbdf9a7350e1097994fb471e92b2eb514109b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tpuTopology")
    def tpu_topology(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpuTopology"))

    @tpu_topology.setter
    def tpu_topology(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9568af32bb7c74c8dbc94511246069475a9b1d5e285014b19704d2d1bcb563b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpuTopology", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54f048f5d12c742dccba5daafef22b924f7cd07c2aac73ec22789bd6ecd8e6ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerNodePoolPlacementPolicy]:
        return typing.cast(typing.Optional[ContainerNodePoolPlacementPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolPlacementPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__867a1126ed2d9bb087c10601fc820a0fc9b6fae0a77e47b42ec70744649453f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolQueuedProvisioning",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class ContainerNodePoolQueuedProvisioning:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether nodes in this node pool are obtainable solely through the ProvisioningRequest API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enabled ContainerNodePool#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1113f9e174ebb0cebf604def927211546818d61c540071d104673bc71b5a9f68)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether nodes in this node pool are obtainable solely through the ProvisioningRequest API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#enabled ContainerNodePool#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolQueuedProvisioning(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolQueuedProvisioningOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolQueuedProvisioningOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed24557764b138ab3d46e0d026cb9bccaefab28bfd5a2f826a773b4988fd305f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed34a48759308fdb680d353e07e8f1608e332b13e5939fb22c7897ca4fe275e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerNodePoolQueuedProvisioning]:
        return typing.cast(typing.Optional[ContainerNodePoolQueuedProvisioning], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolQueuedProvisioning],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1468f539d2385b9a047fa40aeea57ede93f0e5adbacfa1b26633ea04f5d8564d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ContainerNodePoolTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#create ContainerNodePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#delete ContainerNodePool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#update ContainerNodePool#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00d50d647b29f1cf517fadb60788122d1f12bf6f635e803cdf353f3e4064b142)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#create ContainerNodePool#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#delete ContainerNodePool#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#update ContainerNodePool#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6751cef689cf9db2ddd2cc1879dda567c42792813e15509983349adcbafb965b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fca7952eec065e391ee5961fbd01121fa098845e6e560c372f5aac526ec56c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87b84dd4325f7e438db71081e747685a3cb1e4021dbf45ec1917f9af8265b676)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dea43a55eb0c78c4ab529257d775cf4c578f690370a632bacba4dd363c480c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbbec86c81a01f2b47afa8fe8030ccfe6e510da8b7cc17e30e836aaef9f59bb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolUpgradeSettings",
    jsii_struct_bases=[],
    name_mapping={
        "blue_green_settings": "blueGreenSettings",
        "max_surge": "maxSurge",
        "max_unavailable": "maxUnavailable",
        "strategy": "strategy",
    },
)
class ContainerNodePoolUpgradeSettings:
    def __init__(
        self,
        *,
        blue_green_settings: typing.Optional[typing.Union["ContainerNodePoolUpgradeSettingsBlueGreenSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        max_surge: typing.Optional[jsii.Number] = None,
        max_unavailable: typing.Optional[jsii.Number] = None,
        strategy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param blue_green_settings: blue_green_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#blue_green_settings ContainerNodePool#blue_green_settings}
        :param max_surge: The number of additional nodes that can be added to the node pool during an upgrade. Increasing max_surge raises the number of nodes that can be upgraded simultaneously. Can be set to 0 or greater. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#max_surge ContainerNodePool#max_surge}
        :param max_unavailable: The number of nodes that can be simultaneously unavailable during an upgrade. Increasing max_unavailable raises the number of nodes that can be upgraded in parallel. Can be set to 0 or greater. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#max_unavailable ContainerNodePool#max_unavailable}
        :param strategy: Update strategy for the given nodepool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#strategy ContainerNodePool#strategy}
        '''
        if isinstance(blue_green_settings, dict):
            blue_green_settings = ContainerNodePoolUpgradeSettingsBlueGreenSettings(**blue_green_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a02f38344473e92516fa2bacad720308fc5a9e1525dd040ad22e90b14709b32b)
            check_type(argname="argument blue_green_settings", value=blue_green_settings, expected_type=type_hints["blue_green_settings"])
            check_type(argname="argument max_surge", value=max_surge, expected_type=type_hints["max_surge"])
            check_type(argname="argument max_unavailable", value=max_unavailable, expected_type=type_hints["max_unavailable"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if blue_green_settings is not None:
            self._values["blue_green_settings"] = blue_green_settings
        if max_surge is not None:
            self._values["max_surge"] = max_surge
        if max_unavailable is not None:
            self._values["max_unavailable"] = max_unavailable
        if strategy is not None:
            self._values["strategy"] = strategy

    @builtins.property
    def blue_green_settings(
        self,
    ) -> typing.Optional["ContainerNodePoolUpgradeSettingsBlueGreenSettings"]:
        '''blue_green_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#blue_green_settings ContainerNodePool#blue_green_settings}
        '''
        result = self._values.get("blue_green_settings")
        return typing.cast(typing.Optional["ContainerNodePoolUpgradeSettingsBlueGreenSettings"], result)

    @builtins.property
    def max_surge(self) -> typing.Optional[jsii.Number]:
        '''The number of additional nodes that can be added to the node pool during an upgrade.

        Increasing max_surge raises the number of nodes that can be upgraded simultaneously. Can be set to 0 or greater.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#max_surge ContainerNodePool#max_surge}
        '''
        result = self._values.get("max_surge")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_unavailable(self) -> typing.Optional[jsii.Number]:
        '''The number of nodes that can be simultaneously unavailable during an upgrade.

        Increasing max_unavailable raises the number of nodes that can be upgraded in parallel. Can be set to 0 or greater.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#max_unavailable ContainerNodePool#max_unavailable}
        '''
        result = self._values.get("max_unavailable")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def strategy(self) -> typing.Optional[builtins.str]:
        '''Update strategy for the given nodepool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#strategy ContainerNodePool#strategy}
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolUpgradeSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolUpgradeSettingsBlueGreenSettings",
    jsii_struct_bases=[],
    name_mapping={
        "standard_rollout_policy": "standardRolloutPolicy",
        "node_pool_soak_duration": "nodePoolSoakDuration",
    },
)
class ContainerNodePoolUpgradeSettingsBlueGreenSettings:
    def __init__(
        self,
        *,
        standard_rollout_policy: typing.Union["ContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy", typing.Dict[builtins.str, typing.Any]],
        node_pool_soak_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param standard_rollout_policy: standard_rollout_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#standard_rollout_policy ContainerNodePool#standard_rollout_policy}
        :param node_pool_soak_duration: Time needed after draining entire blue pool. After this period, blue pool will be cleaned up. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#node_pool_soak_duration ContainerNodePool#node_pool_soak_duration}
        '''
        if isinstance(standard_rollout_policy, dict):
            standard_rollout_policy = ContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy(**standard_rollout_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d225c90e864edb72c84817010ebd10cda426c64bcf61807a35e8fb8bc3661477)
            check_type(argname="argument standard_rollout_policy", value=standard_rollout_policy, expected_type=type_hints["standard_rollout_policy"])
            check_type(argname="argument node_pool_soak_duration", value=node_pool_soak_duration, expected_type=type_hints["node_pool_soak_duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "standard_rollout_policy": standard_rollout_policy,
        }
        if node_pool_soak_duration is not None:
            self._values["node_pool_soak_duration"] = node_pool_soak_duration

    @builtins.property
    def standard_rollout_policy(
        self,
    ) -> "ContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy":
        '''standard_rollout_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#standard_rollout_policy ContainerNodePool#standard_rollout_policy}
        '''
        result = self._values.get("standard_rollout_policy")
        assert result is not None, "Required property 'standard_rollout_policy' is missing"
        return typing.cast("ContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy", result)

    @builtins.property
    def node_pool_soak_duration(self) -> typing.Optional[builtins.str]:
        '''Time needed after draining entire blue pool. After this period, blue pool will be cleaned up.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#node_pool_soak_duration ContainerNodePool#node_pool_soak_duration}
        '''
        result = self._values.get("node_pool_soak_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolUpgradeSettingsBlueGreenSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolUpgradeSettingsBlueGreenSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolUpgradeSettingsBlueGreenSettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c65c3281f99dfa16c1494670f51bd49f900cebd758d758f61fc15a2c11a8d52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putStandardRolloutPolicy")
    def put_standard_rollout_policy(
        self,
        *,
        batch_node_count: typing.Optional[jsii.Number] = None,
        batch_percentage: typing.Optional[jsii.Number] = None,
        batch_soak_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param batch_node_count: Number of blue nodes to drain in a batch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#batch_node_count ContainerNodePool#batch_node_count}
        :param batch_percentage: Percentage of the blue pool nodes to drain in a batch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#batch_percentage ContainerNodePool#batch_percentage}
        :param batch_soak_duration: Soak time after each batch gets drained. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#batch_soak_duration ContainerNodePool#batch_soak_duration}
        '''
        value = ContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy(
            batch_node_count=batch_node_count,
            batch_percentage=batch_percentage,
            batch_soak_duration=batch_soak_duration,
        )

        return typing.cast(None, jsii.invoke(self, "putStandardRolloutPolicy", [value]))

    @jsii.member(jsii_name="resetNodePoolSoakDuration")
    def reset_node_pool_soak_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodePoolSoakDuration", []))

    @builtins.property
    @jsii.member(jsii_name="standardRolloutPolicy")
    def standard_rollout_policy(
        self,
    ) -> "ContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicyOutputReference":
        return typing.cast("ContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicyOutputReference", jsii.get(self, "standardRolloutPolicy"))

    @builtins.property
    @jsii.member(jsii_name="nodePoolSoakDurationInput")
    def node_pool_soak_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodePoolSoakDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="standardRolloutPolicyInput")
    def standard_rollout_policy_input(
        self,
    ) -> typing.Optional["ContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy"]:
        return typing.cast(typing.Optional["ContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy"], jsii.get(self, "standardRolloutPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="nodePoolSoakDuration")
    def node_pool_soak_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodePoolSoakDuration"))

    @node_pool_soak_duration.setter
    def node_pool_soak_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb7404ece40b3f38ea99f4fd7c051843be348f68661a588aa1a2c0e83ac38ffb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodePoolSoakDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerNodePoolUpgradeSettingsBlueGreenSettings]:
        return typing.cast(typing.Optional[ContainerNodePoolUpgradeSettingsBlueGreenSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolUpgradeSettingsBlueGreenSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb0f66122bd4eeec8645552c9d2cd6b0851158106bb8588842210a94f4deb48c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "batch_node_count": "batchNodeCount",
        "batch_percentage": "batchPercentage",
        "batch_soak_duration": "batchSoakDuration",
    },
)
class ContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy:
    def __init__(
        self,
        *,
        batch_node_count: typing.Optional[jsii.Number] = None,
        batch_percentage: typing.Optional[jsii.Number] = None,
        batch_soak_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param batch_node_count: Number of blue nodes to drain in a batch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#batch_node_count ContainerNodePool#batch_node_count}
        :param batch_percentage: Percentage of the blue pool nodes to drain in a batch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#batch_percentage ContainerNodePool#batch_percentage}
        :param batch_soak_duration: Soak time after each batch gets drained. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#batch_soak_duration ContainerNodePool#batch_soak_duration}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f880fd10db6be0e44d38df6749b4bd32fb05552fbced7b29e37806325b7753bb)
            check_type(argname="argument batch_node_count", value=batch_node_count, expected_type=type_hints["batch_node_count"])
            check_type(argname="argument batch_percentage", value=batch_percentage, expected_type=type_hints["batch_percentage"])
            check_type(argname="argument batch_soak_duration", value=batch_soak_duration, expected_type=type_hints["batch_soak_duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if batch_node_count is not None:
            self._values["batch_node_count"] = batch_node_count
        if batch_percentage is not None:
            self._values["batch_percentage"] = batch_percentage
        if batch_soak_duration is not None:
            self._values["batch_soak_duration"] = batch_soak_duration

    @builtins.property
    def batch_node_count(self) -> typing.Optional[jsii.Number]:
        '''Number of blue nodes to drain in a batch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#batch_node_count ContainerNodePool#batch_node_count}
        '''
        result = self._values.get("batch_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def batch_percentage(self) -> typing.Optional[jsii.Number]:
        '''Percentage of the blue pool nodes to drain in a batch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#batch_percentage ContainerNodePool#batch_percentage}
        '''
        result = self._values.get("batch_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def batch_soak_duration(self) -> typing.Optional[builtins.str]:
        '''Soak time after each batch gets drained.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#batch_soak_duration ContainerNodePool#batch_soak_duration}
        '''
        result = self._values.get("batch_soak_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22a83f3b825ccc466524d067771b8ad51d89b09fc5cd6d252720a73516127942)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBatchNodeCount")
    def reset_batch_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchNodeCount", []))

    @jsii.member(jsii_name="resetBatchPercentage")
    def reset_batch_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchPercentage", []))

    @jsii.member(jsii_name="resetBatchSoakDuration")
    def reset_batch_soak_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchSoakDuration", []))

    @builtins.property
    @jsii.member(jsii_name="batchNodeCountInput")
    def batch_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "batchNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="batchPercentageInput")
    def batch_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "batchPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="batchSoakDurationInput")
    def batch_soak_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "batchSoakDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="batchNodeCount")
    def batch_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "batchNodeCount"))

    @batch_node_count.setter
    def batch_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__548fdfb6bf73a658b7e1354d8db185179eb3069fd8150754d7910063e86f36c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="batchPercentage")
    def batch_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "batchPercentage"))

    @batch_percentage.setter
    def batch_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3eef1d916c9a7c5a970c857c93e214a7fae7a8d62bdafcbf30ae2a0728684b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="batchSoakDuration")
    def batch_soak_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "batchSoakDuration"))

    @batch_soak_duration.setter
    def batch_soak_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cee43be0b9f43019ff58f3dbe5b7287952d49a42c5d8caf5ee703aa3a09a14a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchSoakDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy]:
        return typing.cast(typing.Optional[ContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1b64d4f07eaf087e734038dbe7c0d7f32ab53adda16a571fb83c5ee1384c662)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerNodePoolUpgradeSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerNodePool.ContainerNodePoolUpgradeSettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__898832cf47fc36bcc62d5fa833e94aca0f7333d4cfaaf5d29cb2bd64f79356ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBlueGreenSettings")
    def put_blue_green_settings(
        self,
        *,
        standard_rollout_policy: typing.Union[ContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy, typing.Dict[builtins.str, typing.Any]],
        node_pool_soak_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param standard_rollout_policy: standard_rollout_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#standard_rollout_policy ContainerNodePool#standard_rollout_policy}
        :param node_pool_soak_duration: Time needed after draining entire blue pool. After this period, blue pool will be cleaned up. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_node_pool#node_pool_soak_duration ContainerNodePool#node_pool_soak_duration}
        '''
        value = ContainerNodePoolUpgradeSettingsBlueGreenSettings(
            standard_rollout_policy=standard_rollout_policy,
            node_pool_soak_duration=node_pool_soak_duration,
        )

        return typing.cast(None, jsii.invoke(self, "putBlueGreenSettings", [value]))

    @jsii.member(jsii_name="resetBlueGreenSettings")
    def reset_blue_green_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlueGreenSettings", []))

    @jsii.member(jsii_name="resetMaxSurge")
    def reset_max_surge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxSurge", []))

    @jsii.member(jsii_name="resetMaxUnavailable")
    def reset_max_unavailable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxUnavailable", []))

    @jsii.member(jsii_name="resetStrategy")
    def reset_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStrategy", []))

    @builtins.property
    @jsii.member(jsii_name="blueGreenSettings")
    def blue_green_settings(
        self,
    ) -> ContainerNodePoolUpgradeSettingsBlueGreenSettingsOutputReference:
        return typing.cast(ContainerNodePoolUpgradeSettingsBlueGreenSettingsOutputReference, jsii.get(self, "blueGreenSettings"))

    @builtins.property
    @jsii.member(jsii_name="blueGreenSettingsInput")
    def blue_green_settings_input(
        self,
    ) -> typing.Optional[ContainerNodePoolUpgradeSettingsBlueGreenSettings]:
        return typing.cast(typing.Optional[ContainerNodePoolUpgradeSettingsBlueGreenSettings], jsii.get(self, "blueGreenSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxSurgeInput")
    def max_surge_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxSurgeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxUnavailableInput")
    def max_unavailable_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUnavailableInput"))

    @builtins.property
    @jsii.member(jsii_name="strategyInput")
    def strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "strategyInput"))

    @builtins.property
    @jsii.member(jsii_name="maxSurge")
    def max_surge(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxSurge"))

    @max_surge.setter
    def max_surge(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d48d4d54f6811cedfdacaeb3116177e9e3ab0ddcf3457f86a186163ed99ecc30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSurge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUnavailable")
    def max_unavailable(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUnavailable"))

    @max_unavailable.setter
    def max_unavailable(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d6d62667d8295eb2d864bd695e9242d4dca67491299933c7f1d9f5cae92ee38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUnavailable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "strategy"))

    @strategy.setter
    def strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__950b1e0c01f456486a57e25ba4afebf1dfb32735174e2851bba52f7eaa0293e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerNodePoolUpgradeSettings]:
        return typing.cast(typing.Optional[ContainerNodePoolUpgradeSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerNodePoolUpgradeSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__720d025b5be7dfb570dc48eb1cd0296b0e40367f77ed6a011717515fb232342d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ContainerNodePool",
    "ContainerNodePoolAutoscaling",
    "ContainerNodePoolAutoscalingOutputReference",
    "ContainerNodePoolConfig",
    "ContainerNodePoolManagement",
    "ContainerNodePoolManagementOutputReference",
    "ContainerNodePoolNetworkConfig",
    "ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs",
    "ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigsList",
    "ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigsOutputReference",
    "ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs",
    "ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigsList",
    "ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigsOutputReference",
    "ContainerNodePoolNetworkConfigNetworkPerformanceConfig",
    "ContainerNodePoolNetworkConfigNetworkPerformanceConfigOutputReference",
    "ContainerNodePoolNetworkConfigOutputReference",
    "ContainerNodePoolNetworkConfigPodCidrOverprovisionConfig",
    "ContainerNodePoolNetworkConfigPodCidrOverprovisionConfigOutputReference",
    "ContainerNodePoolNodeConfig",
    "ContainerNodePoolNodeConfigAdvancedMachineFeatures",
    "ContainerNodePoolNodeConfigAdvancedMachineFeaturesOutputReference",
    "ContainerNodePoolNodeConfigConfidentialNodes",
    "ContainerNodePoolNodeConfigConfidentialNodesOutputReference",
    "ContainerNodePoolNodeConfigContainerdConfig",
    "ContainerNodePoolNodeConfigContainerdConfigOutputReference",
    "ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig",
    "ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig",
    "ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig",
    "ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfigOutputReference",
    "ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigList",
    "ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigOutputReference",
    "ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigOutputReference",
    "ContainerNodePoolNodeConfigEffectiveTaints",
    "ContainerNodePoolNodeConfigEffectiveTaintsList",
    "ContainerNodePoolNodeConfigEffectiveTaintsOutputReference",
    "ContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig",
    "ContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfigOutputReference",
    "ContainerNodePoolNodeConfigFastSocket",
    "ContainerNodePoolNodeConfigFastSocketOutputReference",
    "ContainerNodePoolNodeConfigGcfsConfig",
    "ContainerNodePoolNodeConfigGcfsConfigOutputReference",
    "ContainerNodePoolNodeConfigGuestAccelerator",
    "ContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig",
    "ContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfigOutputReference",
    "ContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig",
    "ContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfigOutputReference",
    "ContainerNodePoolNodeConfigGuestAcceleratorList",
    "ContainerNodePoolNodeConfigGuestAcceleratorOutputReference",
    "ContainerNodePoolNodeConfigGvnic",
    "ContainerNodePoolNodeConfigGvnicOutputReference",
    "ContainerNodePoolNodeConfigHostMaintenancePolicy",
    "ContainerNodePoolNodeConfigHostMaintenancePolicyOutputReference",
    "ContainerNodePoolNodeConfigKubeletConfig",
    "ContainerNodePoolNodeConfigKubeletConfigOutputReference",
    "ContainerNodePoolNodeConfigLinuxNodeConfig",
    "ContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig",
    "ContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfigOutputReference",
    "ContainerNodePoolNodeConfigLinuxNodeConfigOutputReference",
    "ContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig",
    "ContainerNodePoolNodeConfigLocalNvmeSsdBlockConfigOutputReference",
    "ContainerNodePoolNodeConfigOutputReference",
    "ContainerNodePoolNodeConfigReservationAffinity",
    "ContainerNodePoolNodeConfigReservationAffinityOutputReference",
    "ContainerNodePoolNodeConfigSecondaryBootDisks",
    "ContainerNodePoolNodeConfigSecondaryBootDisksList",
    "ContainerNodePoolNodeConfigSecondaryBootDisksOutputReference",
    "ContainerNodePoolNodeConfigShieldedInstanceConfig",
    "ContainerNodePoolNodeConfigShieldedInstanceConfigOutputReference",
    "ContainerNodePoolNodeConfigSoleTenantConfig",
    "ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity",
    "ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinityList",
    "ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinityOutputReference",
    "ContainerNodePoolNodeConfigSoleTenantConfigOutputReference",
    "ContainerNodePoolNodeConfigTaint",
    "ContainerNodePoolNodeConfigTaintList",
    "ContainerNodePoolNodeConfigTaintOutputReference",
    "ContainerNodePoolNodeConfigWindowsNodeConfig",
    "ContainerNodePoolNodeConfigWindowsNodeConfigOutputReference",
    "ContainerNodePoolNodeConfigWorkloadMetadataConfig",
    "ContainerNodePoolNodeConfigWorkloadMetadataConfigOutputReference",
    "ContainerNodePoolPlacementPolicy",
    "ContainerNodePoolPlacementPolicyOutputReference",
    "ContainerNodePoolQueuedProvisioning",
    "ContainerNodePoolQueuedProvisioningOutputReference",
    "ContainerNodePoolTimeouts",
    "ContainerNodePoolTimeoutsOutputReference",
    "ContainerNodePoolUpgradeSettings",
    "ContainerNodePoolUpgradeSettingsBlueGreenSettings",
    "ContainerNodePoolUpgradeSettingsBlueGreenSettingsOutputReference",
    "ContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy",
    "ContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicyOutputReference",
    "ContainerNodePoolUpgradeSettingsOutputReference",
]

publication.publish()

def _typecheckingstub__ca9abea3bd333b65f45372e99fa915899559f46dac335423a83703889f336bf2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster: builtins.str,
    autoscaling: typing.Optional[typing.Union[ContainerNodePoolAutoscaling, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    initial_node_count: typing.Optional[jsii.Number] = None,
    location: typing.Optional[builtins.str] = None,
    management: typing.Optional[typing.Union[ContainerNodePoolManagement, typing.Dict[builtins.str, typing.Any]]] = None,
    max_pods_per_node: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    network_config: typing.Optional[typing.Union[ContainerNodePoolNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_config: typing.Optional[typing.Union[ContainerNodePoolNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_count: typing.Optional[jsii.Number] = None,
    node_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    placement_policy: typing.Optional[typing.Union[ContainerNodePoolPlacementPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    queued_provisioning: typing.Optional[typing.Union[ContainerNodePoolQueuedProvisioning, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ContainerNodePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    upgrade_settings: typing.Optional[typing.Union[ContainerNodePoolUpgradeSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6967d132a175adacba6abc837e68bf46d55dc0908e3fd4b68cd845b3c85b0b95(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bff5ba290576d142fcf32031b738150e663fa4e97d31d9d36a4c65a5188ccbbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d34d72f51c9c7d7e897e4e4f091eacd2924400f8e3f959a42161f8957d9908(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f24f87adb695ed60e7902dc3b71e9a349b50cfcb0f4f0a30f0274bc5ccd3f28f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ecf4f8b859c78cbde0c69fa5d98922df5d77a5a11490803ddf16a9235a80b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4eeb7ca49c81028ae25d5481ead5632b9792ca5fd39281a38e71837d3ac1660(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22aa633c9045af5a5b7699a64b1bd3801e89f692a4c40c4aa639f0d4d0cbd6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd015913f8bde6e2020a18b3e0665c7ae70e1b007bc5bedda06d596d32199b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac7671d227ef4ff53317843b34c786357d279a4c8430a8c33215130ffbfba3d0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee4985ce84c9293be49ebcb5708b50ee5cb1a1fd0b50aa75eeea32c37c3a71c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a35f3db4b76b142b2a636a863d1673fd934be8e00fef74a5f1e826822cc2efd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d2eacfe908a46590117dc8bb3411d62bcd40b5053c0b0f097d4b4891a60edf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e69a00ccd28bc7146a8e3e75397c3f4ad4a26d9503125e9e93e95c042677bbe(
    *,
    location_policy: typing.Optional[builtins.str] = None,
    max_node_count: typing.Optional[jsii.Number] = None,
    min_node_count: typing.Optional[jsii.Number] = None,
    total_max_node_count: typing.Optional[jsii.Number] = None,
    total_min_node_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__139cc054b9ef89966c8893a134c656add40f339f0df0cbe65ad8493142ece246(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2c722bd7e0ce4a2e9daa6ee507b878f101e460711e6d5553c5d1543a3e3fd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56f54baddb21611356fb0d58575afbd56e580e609a5c2e2fa48b2426ded30c27(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9a15a3ac8292d2455bb44d64346863fc36344e91fe06c2b499e5321bb56123(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9850ad92fff6d51e395773dcdb51d4d41e9f6c00f367cd4c6cfc4c6e802c12f7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae60240cc93e735e2ff040e9f4a97431b93d93e1b2af92735fc8412bc41b35a8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6c9e9cf9612368dbeee25a7230dc914a95bea16b7e73443b0d0747d3a20483(
    value: typing.Optional[ContainerNodePoolAutoscaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b5b6bcb2c794aac413c6600fc6527e94c0489eeed9dc04e3576397641aead23(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster: builtins.str,
    autoscaling: typing.Optional[typing.Union[ContainerNodePoolAutoscaling, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    initial_node_count: typing.Optional[jsii.Number] = None,
    location: typing.Optional[builtins.str] = None,
    management: typing.Optional[typing.Union[ContainerNodePoolManagement, typing.Dict[builtins.str, typing.Any]]] = None,
    max_pods_per_node: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    network_config: typing.Optional[typing.Union[ContainerNodePoolNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_config: typing.Optional[typing.Union[ContainerNodePoolNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_count: typing.Optional[jsii.Number] = None,
    node_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    placement_policy: typing.Optional[typing.Union[ContainerNodePoolPlacementPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    queued_provisioning: typing.Optional[typing.Union[ContainerNodePoolQueuedProvisioning, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ContainerNodePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    upgrade_settings: typing.Optional[typing.Union[ContainerNodePoolUpgradeSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae5fb0d3da25e65124e9e67126562a8e2c5a46ce209000e4f96f66e236b8a950(
    *,
    auto_repair: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_upgrade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9562d994c6cd400f27f7839b9bd7da36dd0ec6c67331230eb30f90fc82a07a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31e2b8f0fcfb6376c20665e2b6242e4d75a74a91fc738b206864aba89af2046(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ca589b0f57081fdf0b4fb5aa29378c7a8d6152e9437fe9e3cae0a1c891a6d79(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9cbc71a7868daa399a333e1e87b7a13c4a094f117e7eded551160c7904ba46f(
    value: typing.Optional[ContainerNodePoolManagement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abbfb53fb9a1dde0675f3a0401175c08f385a25856b0a6a7c1ba60b6cfb64bbc(
    *,
    additional_node_network_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    additional_pod_network_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    create_pod_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_private_nodes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    network_performance_config: typing.Optional[typing.Union[ContainerNodePoolNetworkConfigNetworkPerformanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    pod_cidr_overprovision_config: typing.Optional[typing.Union[ContainerNodePoolNetworkConfigPodCidrOverprovisionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    pod_ipv4_cidr_block: typing.Optional[builtins.str] = None,
    pod_range: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6e317f25e78dbaf6222110e5e2eaa615f49056cc5f6fda2c248c51dbe250d97(
    *,
    network: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f08b94c9c30d1f722c6ffc66e39880f6115526cb4125ce222d4e3b3d9161c726(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c79ac3f3d9d6d914bd3e1467196c4a5ca5fc8d416da2cf1d7a94d6d62b67f21(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4472781eaa237d97c9a841247fd0e8502b74b15275529644d35a219c75021042(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864ea332a77337a3ef008859be3ae009939ded50a19e6afa6f543363bc0e7e47(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90207bf61750c65d01736c8b2665de94ae0303f7bc9ade1cc0d2380195fdf94(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c8e80729854d17420fa561e1dfdc717f6a29a5ae4a8ccb0c05e2267fe3e827(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6637e6210514ca11314f2d07dcc0cd1cef3d62f27dc51770385d329316270ec3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcb6d4faf6c27bda968f9cf54d59f8ba9181f785cdb69939315ceef7298aee8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c019cb47022bcc25bd7cc9fa55fa1b9557ceb0cb487acff36606ea80b180f263(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9aa241e3258b24599ddc1c1c69af03829f6d4f44f89395d52e1cf306d6362a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f715e27736028e3be84e89c925de969cd88f3522188bbbde6159595831834f3a(
    *,
    max_pods_per_node: typing.Optional[jsii.Number] = None,
    secondary_pod_range: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f30973022cb80904b9de8991de9c47b2f0abd593a370c4937398a65bb84e0818(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d338ca0522a5809644fbeb9265901b141140992445851a1b77a022dce2ffc55(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d21642b3b812a4562c680aced11afad0fc1f76ef8a9fa8c6e8b1d855c39db1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8062e17ead7f519b55dc163e8561e79a6e1b406f31a4c5e32234e4717281dcb6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca7e6ef168ced4b8664f9f779e038e206cc08531aaca8862a597b3a58b29331(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c70b772492c4b127fb19d57918aca4dfbee49bf8c41ae0547dae08b6fcf7e10c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__360e8eaf1387642f601fc5a0bfd5e21811d85f70a5b347a9d77be364128580d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea7c6d2f8f829d36dfd43a3fa0526be28ac717419abfeeb46d3c84230e7adcb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29623a1b9019f044606ba4e4796ab329014f3b7ca4080e3f2b44844908076467(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4bff11864fa449ebfe8ecd9e18699d7942beb3e3300c0386333eda8378b0c7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97c7529a516f326563f5fb0fc9f1bbcfd57d0f5186cc92e953bb9c88267de5a4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__988cf913d91635960c4fd13d48fe53df3dc9c52d1b5402c0cf34e5349055046f(
    *,
    total_egress_bandwidth_tier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef9b42f5e1482903e3e9f51395f366c5a9e0757ca892601ae000f6b0bda58592(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df88508986984b431dfb6276b1037e78fcc406d15c7ba783ee94b717201c7b63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__805a66c5a62dd290a2db6edd6f3aed4208d09678a6e56305bb62a5e1218349ef(
    value: typing.Optional[ContainerNodePoolNetworkConfigNetworkPerformanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa28393441632c82f009d0e2bba0bd79f9e6bc1ef61a36f768a222eabf78ae8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f120328170db089c97f25f1643bec2765beafc58202ba3372795aa28fd6e4ff(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28f5e053221540ee1582db2d5317c2cc285bfdf255146923f44ad3a210caff3b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b40fb1a0c346aca2b9adbfde60f56535afea1df971989773e0db9c6cefe53356(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__528fb63d4d6169e7fa67df8f888d1fd44a44ef2c0d4cb966d96e9fb955239779(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__172b5c507d7e298ab85834814ed79ff08b9617c08c3de11d6a39347af79879dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec56e0a274f5b2b5ab75b952d082c8d6d1dc6e260b393a2e8a81b4ebe717f3e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8714794ad9790eb27d91aa38324158abbc781fb67e5de4fe75e1544ea78a37de(
    value: typing.Optional[ContainerNodePoolNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__890b871384eeb45ea20d1c79149edeac85e821cf7fcc6444357184e6e0b5eaf5(
    *,
    disabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88e581d74ae383f5a43a53e034760dde37e84f25b80eeb81a29c653cd05692b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b85feb090b8737dc565b5d11f77461076520dc0704a315fae9844cdd2aca9eb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__481f78751ef8774f0366ecb626e2cf5ec4c62949e27c3c57e91fa6723048281e(
    value: typing.Optional[ContainerNodePoolNetworkConfigPodCidrOverprovisionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624d8a32216c09560115f6cfc0618bf44f0ee63f0c7cda1fb3cbe56171e3c79b(
    *,
    advanced_machine_features: typing.Optional[typing.Union[ContainerNodePoolNodeConfigAdvancedMachineFeatures, typing.Dict[builtins.str, typing.Any]]] = None,
    boot_disk_kms_key: typing.Optional[builtins.str] = None,
    confidential_nodes: typing.Optional[typing.Union[ContainerNodePoolNodeConfigConfidentialNodes, typing.Dict[builtins.str, typing.Any]]] = None,
    containerd_config: typing.Optional[typing.Union[ContainerNodePoolNodeConfigContainerdConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disk_size_gb: typing.Optional[jsii.Number] = None,
    disk_type: typing.Optional[builtins.str] = None,
    enable_confidential_storage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ephemeral_storage_local_ssd_config: typing.Optional[typing.Union[ContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    fast_socket: typing.Optional[typing.Union[ContainerNodePoolNodeConfigFastSocket, typing.Dict[builtins.str, typing.Any]]] = None,
    flex_start: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcfs_config: typing.Optional[typing.Union[ContainerNodePoolNodeConfigGcfsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    guest_accelerator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerNodePoolNodeConfigGuestAccelerator, typing.Dict[builtins.str, typing.Any]]]]] = None,
    gvnic: typing.Optional[typing.Union[ContainerNodePoolNodeConfigGvnic, typing.Dict[builtins.str, typing.Any]]] = None,
    host_maintenance_policy: typing.Optional[typing.Union[ContainerNodePoolNodeConfigHostMaintenancePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    image_type: typing.Optional[builtins.str] = None,
    kubelet_config: typing.Optional[typing.Union[ContainerNodePoolNodeConfigKubeletConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    linux_node_config: typing.Optional[typing.Union[ContainerNodePoolNodeConfigLinuxNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    local_nvme_ssd_block_config: typing.Optional[typing.Union[ContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    local_ssd_count: typing.Optional[jsii.Number] = None,
    local_ssd_encryption_mode: typing.Optional[builtins.str] = None,
    logging_variant: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    max_run_duration: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    min_cpu_platform: typing.Optional[builtins.str] = None,
    node_group: typing.Optional[builtins.str] = None,
    oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    preemptible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reservation_affinity: typing.Optional[typing.Union[ContainerNodePoolNodeConfigReservationAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    secondary_boot_disks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerNodePoolNodeConfigSecondaryBootDisks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_account: typing.Optional[builtins.str] = None,
    shielded_instance_config: typing.Optional[typing.Union[ContainerNodePoolNodeConfigShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    sole_tenant_config: typing.Optional[typing.Union[ContainerNodePoolNodeConfigSoleTenantConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    storage_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    taint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerNodePoolNodeConfigTaint, typing.Dict[builtins.str, typing.Any]]]]] = None,
    windows_node_config: typing.Optional[typing.Union[ContainerNodePoolNodeConfigWindowsNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    workload_metadata_config: typing.Optional[typing.Union[ContainerNodePoolNodeConfigWorkloadMetadataConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__038c9a601363c15f56828a2ec1f0acc6f1ca14f133f87347af706e5541fd32f7(
    *,
    threads_per_core: jsii.Number,
    enable_nested_virtualization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    performance_monitoring_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b776be47e4d205ee48c9df6fad4c572f588bf9073ea871ba6f03462b8dbad9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ce9ed59586826e09734ebd9a2d76ed08602388f61a3203ff1ccbc34cea58880(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a6c9d768855b5d8b6bd661ec7867e99c52dd072d664dbad3a15e16965fe26eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__259a5cba4783ff49952961d10f9bbdafd504d401e8d4d127ba17b5e243749623(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3397beb08baba0d69b29f5a5fb9261ce9cdc3ec775f69e81a3df61019bc61012(
    value: typing.Optional[ContainerNodePoolNodeConfigAdvancedMachineFeatures],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53cf282a7b3f4c3213a1bc296099aa561d6d1817aa9bab22dfd52c6e8ff5b6f(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    confidential_instance_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54a587c32028e5f9335bbaee76d49254f74e77218dfacd732a02b3877cd35791(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdffc30842d1e257dcae60fa6e4b2e6e4158aa96cd4def10a8ee650b16c45121(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c284f960bf7442577bde1bf5f257de525cd6b310ff86ba85149977f2a553cc7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f26248a672e38fc7a005b32e7e860bea1c16035d28870c17f835435cc72dcd7(
    value: typing.Optional[ContainerNodePoolNodeConfigConfidentialNodes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39740ebdba0837d3bb6a7350c163fbcdd461a01bd77216b0dd1c6c224037761(
    *,
    private_registry_access_config: typing.Optional[typing.Union[ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79032424f0b58ff4f82e54fd9d4d8ff8bb151f2380b436fce03b63d60772a4a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4383bd4b8be9ac98fc10ce6ade69bba9c08d2f2523c3f951adee25c73175b8c6(
    value: typing.Optional[ContainerNodePoolNodeConfigContainerdConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__985fc8f22cba01d24a1aee5fe9ec1ec35433262b68c887feee46093f8ad61945(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    certificate_authority_domain_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b0a2f19b8428209e81064069a3f69953dd72a6fbd9818a2916b7c13e043a29(
    *,
    fqdns: typing.Sequence[builtins.str],
    gcp_secret_manager_certificate_config: typing.Union[ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8e49ef5dcf7472d653c4e8fe7a3e8349dd901f317ea2065ea1331638ca7d9fe(
    *,
    secret_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96facd7ee5caa3dacbf05557106ad31e58471d6aa9ed508df3354525d2863e65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__979231a8b125d11aebf4eead82887451cc2b7402f96307df519eaa8051c81896(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cefab438c5ad73bc78c4618643916312b5f3e72d0cbd96850130a1d95337e5b2(
    value: typing.Optional[ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e4310e1c887609f4b860533b6bc059e6b0c11ae5a5456dc88253b0aed2920fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c20009e1f3ff9fea3a7eb78fb4e792a41a1f10c4e7e61d22bfafb75013c544fc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f23467e33ef71fc03b0882c090bb65650bc984421b0c4d3989afd8751043b99a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c4b2ad127d461983c1210a9e76e785b67f64abd4f49684dba710754f67b8f54(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46cb370e8f4f0cb47c5eb16c8fdd0af2564feaf182bd633de26c77d63cd4ca4b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__605c447e174ce37d10a44e892bb7d8070d325963c6bb789a2dccfd958e1e588a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b837f51eccd3450c096b65c727b277aae54b4e0819beee34e246206a0fe4ce59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43612571fba3f30d52fb479103e7b8208bd3654c0abb5cf48e23d0b5e13fc5a1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7d89e4b304c687dd46f9ad8cb2aecc54a2569f462c30a0cbda088ecef8400ae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c041eb242de485c090bece1e4960a03f1b8cc8780f331d31b19c1b2fd2c5910(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d43d4c8a0ad98d5fd7a820782913b509c8b63d242a4f0c0443952a4253c0d6e8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8fd9c7e73f0eb0a60cea4707642756432260cffc85b11b4abddf0cc92f1d862(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__408fb2a8d804db54bdde0a76a1d2bdff484681fc58e67654feffb0d6943e3874(
    value: typing.Optional[ContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f57f002ae261c592dc9c6c120f76b4395db4b68bf624a71ce93dc4519b4c952(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a6fbf8583cd4348fec6242d1f0f02ab894286dd7bf4557ef78f5d1de844758f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee50cb56acd8260255d2d41da3e382caac23e8356ec2242d2a3b00e0da9b5b02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e6499cf7711e2d3fce301a0ee1383919fec43e9d401dacd24782c51ccfa938(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__794c47c84c836a4bcdf94658d5fea9c76ce44f29fabaa476710f0214c26ceea1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e45791227ffbc621abc269ab82189d5038b0473b183e92e61a0555b37ae5b329(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c67e2fed0275096483cd4222fe360b4a2a9e92e68653e52c3626f69fd04b013d(
    value: typing.Optional[ContainerNodePoolNodeConfigEffectiveTaints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96a188e5167c88cf94b597447090b14745a4557a719fc4d664547de5858949ac(
    *,
    local_ssd_count: jsii.Number,
    data_cache_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e43eacce4fb1d41b116066d2098fbb94215f6676cd74783ccbb949b5f631aadd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7be4c2d43771b7422235ee8f931901016694758c5c0d32fa8c4f0ee9c429f8f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ab18c90f95146655100f462be636f58caf1f5cc09ae3508620ef1ae00221d4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6325bd1636cd7ba12ac78acc1c03bea84dfedf51dd9a76316087b189c1545ed(
    value: typing.Optional[ContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5244a4a18a95bcbe02f47db1a602339491f1a817319853beeefe17ff406e0113(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f0ada489ee557a9f5d2e892c5e6e36eebfb9fe0a2e58cc30a7cd86c8ecc8b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3be3a9cc55d87d3ea44a51f21185c940eb0fc8c1433d8dd084901ca09f077372(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c153caaaa52be468904fced14b5090a0e64598bd2aea801f69ae4607b098ce1b(
    value: typing.Optional[ContainerNodePoolNodeConfigFastSocket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b8b74f601eefff327c9378411729253b3cdcbfbe1d193444de384a0ed35822(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aff92f43b7e82bf39e8c75f1bf1f5be15302abdfd8e22a8de2eb273a53678c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fff317cbde6835756480aeb533c1add51c0791f9015bb77f70e6c2ff6e1af36(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__984185608b9c906f1782f4e2a646d1e37b57c195c42c1268aeb5e235d4b45190(
    value: typing.Optional[ContainerNodePoolNodeConfigGcfsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f30ac32d46d12017e0eeb590d01f391def5988006ed039bab3bc4474bdba26f9(
    *,
    count: jsii.Number,
    type: builtins.str,
    gpu_driver_installation_config: typing.Optional[typing.Union[ContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    gpu_partition_size: typing.Optional[builtins.str] = None,
    gpu_sharing_config: typing.Optional[typing.Union[ContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce3318984671ac11c6550e3a977ea351fcec58006d3a53b833cbf41ff94cd9c8(
    *,
    gpu_driver_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97dd8e1665b143cd997ea44bfd4918193536cf146c86bee6090b7faa8c18ea90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8753a8e4780ac3dd2308cc597145cd4e70d06568c7dfe7e7edbfc4e416e553a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e30664941914b1d5b31ba3d58e542c147cbc353a251f434f9827dec83ce0dd7(
    value: typing.Optional[ContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aa4a423ead67dfc69d4e555095531f42430bf374fd08cee74d176e119d3cc14(
    *,
    gpu_sharing_strategy: builtins.str,
    max_shared_clients_per_gpu: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b38b74d6aa8d81c848694daff9a39e3accc4e02d50cdc346a557d5a7c81672(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd6afbce62ae0a114d3ecb178ae787afe6f9e84d6d07fc740310e8fe97604c2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c5d04f392020207c37d852ff9cf8fb3ccc222408190cc9f9956a7175ece76be(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd795e17f67eec9970af2829aa46fc74600a2d5f5405e74dcec5cc210b48b13(
    value: typing.Optional[ContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b76691c541f6c8638285486356d4b6c033d83039ed4fa13abff6d28ab2b051f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef213056406c08d6ae8e1100c9d7beaedccd909ad8789b1a5708ad2c4f349b19(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4161a997a8f93bb7faa3c05ddb3e8e332d210075c482cf6a33a0676259927bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__736ca78d4f73d65511e04be5dc2b621bddbadfc4c0eadd52458972b431b9d52a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__482ed8b1d1ddb4e7d9997427e8151f2d893735618325b7af12ccbca996aaf693(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaadfade65ab71d9a79bc196ff59b484db2e0cd9b8849074f7992a78840efbbc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigGuestAccelerator]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e59f5acb116122ecfaa56e9ec06371eb7ebe7bfe359f7319157371985e116ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85448f1a2612509436069b20d18028c465325e9db6796ed462dcd20003c53639(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4e71e53971282eaef18d251b73e4c628986fd117186c1ba1b2bc705deca4d55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cee90fce73a002616033ad053ebdd5bf6cf70ee9b9850f9cd2da55ca68af4599(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e8ee62a4a520859244b9c597a12b20be41364260f29197af8901ddde493cf0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNodeConfigGuestAccelerator]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47d3bc40512a41cc51d7990d937743c3151685667c2db6170d85ebeb880899a(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6796ff24e2aa2ebd5203b33802020f3684fb5ee1aa6112be97593d1e92eb057(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4047f846c25c883a1c05aef0b81284a35db9ebf0d5a91dfd5d0d81db517667b8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20383161e3e70c230d8420d7a577480befbd8ce3412a17cf1ca274569e21382c(
    value: typing.Optional[ContainerNodePoolNodeConfigGvnic],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2a0f9d7139ba32901ab0ec356932d505a176abcb97ad6734e4a744686cef95d(
    *,
    maintenance_interval: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b460bd465077ce399b0c79dcd01d4a90c9d18f4e3e8abd45708bfc2acbb6bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__042ba9a71137b74563f9c07820e9a46100fa53b27a7d8da45406f333d5dab32e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c48aa7a7dd6e16cd5424bd75ca44fdc57196d2dd469fe6f2ad40f5723f21200(
    value: typing.Optional[ContainerNodePoolNodeConfigHostMaintenancePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba35fbf8f2f5b8bedf5e350dde661105e29aa7385a444c7dab33b0385adff671(
    *,
    allowed_unsafe_sysctls: typing.Optional[typing.Sequence[builtins.str]] = None,
    container_log_max_files: typing.Optional[jsii.Number] = None,
    container_log_max_size: typing.Optional[builtins.str] = None,
    cpu_cfs_quota: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cpu_cfs_quota_period: typing.Optional[builtins.str] = None,
    cpu_manager_policy: typing.Optional[builtins.str] = None,
    image_gc_high_threshold_percent: typing.Optional[jsii.Number] = None,
    image_gc_low_threshold_percent: typing.Optional[jsii.Number] = None,
    image_maximum_gc_age: typing.Optional[builtins.str] = None,
    image_minimum_gc_age: typing.Optional[builtins.str] = None,
    insecure_kubelet_readonly_port_enabled: typing.Optional[builtins.str] = None,
    pod_pids_limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5f9fb292c0743b4076da0ae8d4b13dea9d24cb16c526cc8f437582310d76e9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__049f938abe2d60f7497ef8cd59965b140c4e154f88d4185ded98054bcb3dde7f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5477d7d70e82c906a216ecf3b39ce5401a3558341dbb000df5220202a9c05dc6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a3cbd22c002fa6848a1056513255b455a5315698bebc79f03d861ee0d4c804(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf55914796ef074e1d1a74c3d3a5b63fe4e093ee0ef8e02690850bb467704064(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55ef573369edf765b329cbd403bde6571a21a49e696159d6a84e72010fa923f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e169b5b2e241247e5558a93d16c9e941eda0dbc8d11d79890215b4e5d0f9a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__430b5018f363549178a4e68483e00c9bef2449409a1f793491f149bac1dd8f8e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac1004a20718eedc499b7240f1ac656e34c253d239310a54420258afe7aa0ceb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__596a76e214711c8d049d0c69c6efaf3f7a9fae561e51793aeb946fa99f42e4dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1764c33d847d07505da712be10ead70d767d6fd304b28d258f3afc3adfc2afc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a713520d0250c4f99a546d716cc18a9fdb600c5cd90057abf49dc97fb11122(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417370ad149bd7e99953841a9b4f65088affa1c8376ce7cd5901246597e75992(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b58851cb84b1cd183e9f303cbbe398252fc0b554f73272e7b9fff0d02f12262(
    value: typing.Optional[ContainerNodePoolNodeConfigKubeletConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16948441d4349ba63ed1b4710c36ed3e9de19ad2ec5116c02db8615cb1a10b06(
    *,
    cgroup_mode: typing.Optional[builtins.str] = None,
    hugepages_config: typing.Optional[typing.Union[ContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    sysctls: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a489ee8c4d58a71fe3574d56ad1784304ed38e113d774afecae2d8b491739cc(
    *,
    hugepage_size1_g: typing.Optional[jsii.Number] = None,
    hugepage_size2_m: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f14f72c4e15ef679de121818408e5e95e6d8d6fb472f5e2e9a883a43f76ce955(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8539aeab70b22e2f4d8b53bf65c3f6f8823c85291131187c9a7a64a8056658c7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880ca37c2fc07ea4b717ad8f0bda499c1e6957a3e0f54f0bfa3f8a1b067de8fe(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e9e8c5d444158635ed1ed8394f89ef2df2fc6574619b1d6fc5e8f5e30912aa(
    value: typing.Optional[ContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0460ef1475f1ef6567e5169f475b7ceb38265d44a4565c990b3a685e9cab3a29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca4dec1f95cd23ad879ccf7e5dc53bc670bc0fe6ca80ede5ce3623566943101f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f508b6be4bf1c1074acaed306517780fd016714139e866a1821151c7a2f604a6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ac964f12ae2a74330e7063adce4389e7a53a1c4bc5bc491fa43ec9d620dfc3e(
    value: typing.Optional[ContainerNodePoolNodeConfigLinuxNodeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65981ffdb6e267ef9da5fd2280da58fae8ab4507b53d2bbd5c731b8d316388d6(
    *,
    local_ssd_count: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26f0196350b00d59c0f93e7f5651a49be6cfbe7f60720203ea9586900d5dafb1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d56cbb6300045f8e1cda4f2abe33d48c7b5722c641d4aa1d7bc65168a75421e6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd677fd3dad6718d717e6413e8076fbf5dc5653d9090839a6877308eb3ca825(
    value: typing.Optional[ContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6955ee7a6cfb6a8c027acbc473ed7f645164620729aaeaadc57fe6a5b049337a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ae90f9fdff9da656a0d4d88632dc03b70545caec4dc7eeb7ed06062de89863(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerNodePoolNodeConfigGuestAccelerator, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a9cc80442d07d5557d37fbd806eb6212760c6dd560f3ab03e07c6404ea9e72(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerNodePoolNodeConfigSecondaryBootDisks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4a9eb550fc41fae95eba9c1ae96e8dd8b89fb7a1e32733d03306886b471a4b8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerNodePoolNodeConfigTaint, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c00eb286d3e6893dad5a267edbc41c9d18855c3772561890e6299afcad154bef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ee93eccaa32cf9cbb85623b4c858a278e08c6f4266cde03ad54c5ceea3885b4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c2e9108b3abdc3bc7beef5eae561cbe84b85c072833973a8ad8136bae6cfc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f71a3285d4536b1082236a18e741adb3d1f5ceeb6f351a7d76a0b53a422d18c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7fa3dfa7250237415876f14a6684c7aeb6b18a9bc1d4692d1183a705ff51c2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ac811a34dcc6f8b77cf0a91f76a3a3fb9eaf339231f04fd01d845942e4f2ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9f3c53632eb51e52290811042139da72dd98abc37666ed213ed66b376a4b327(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__339fc7b30e25660067113a4a2090e0dcb35253864b89048763d26123df7e64ad(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e799e04921c80bc607c6bb8a9d247315d01037617ad7c0f8e9f15a867201540f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a6aadb08ca6cb9b35056a341e8b7b91fd36eb43bf79c19ac48d844300521b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb0161bbe3e5f64ea516ea6e3abc134c47a7ae1c82575f1b55842ac5cc87ae00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d9ac0afc1dba66badcc62eb741d2178e296e25085c9fc967db808f2979168d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__831a1c9d624222f3b1bdf9eb93488e80333249f48dc558af7048c3f360deb5af(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0655d66cbc4934d46aa1e11143c93fd5f5a910adaea72a5764a414a479763597(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54e92cd9bafa0142dbb4902a8f9209a21b7b7a8e88b4c0daa0d2ba544c0c2a1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c983ba1dbc70a4dcebf6e2144b26b27de90d534f16119057f0d0630d14be4c61(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a9a3f63e92a95f12c9eb15926f757148868b2516f3578745daf6e0bf1b1c34(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__941f1b38a5b7e374e4d6513f0e54a23f063b3d8d487abdda9343daaf36fb2ea8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3667df33d9eb8eae6c8c46a5ee54ac5a06bd0dd9817ac5ca64efd02701d3b49(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d35a8a96cadfdd89ea4377798c17945517bb2d074c90e1c4fd465fb246856e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e93bbaeb821cda1f2fdb5721148276912ff0e95fc753d96d6cc71f730f967ae9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__661626fcdcdd7b734ffe1390f33855d48d680f93a0d00acfcf98c5b9e37e8438(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__955aa32132f0c40b06ce7c723e0140da9caad79983aed185eb0c1796c347f978(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__351229fec65f01f2822233722ea04249a135f50dd7735cd72d4763ff527ad2c9(
    value: typing.Optional[ContainerNodePoolNodeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088da2d8e80cb55ead4282afb73e46f00dadf9e3d2bd4f45cb367e875f1673d2(
    *,
    consume_reservation_type: builtins.str,
    key: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7029c69ee592859f0782359f25b3e2ff512040dd308bc178f00ddd0039c2e6fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7427a98ea1b1239c15c0e0827b08c41f69b3e8dd22f13192395e1ea4417bea29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__918e04575214bec1185c71689b986834d560849bbfe3184afc6880ccc9bd8197(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f83d85a0ece0e057a0e49a178d248187f2f518255200a282fb575a5642814eb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0965988de54a6815b2ddad06e8b986a9751125cb17230f2e0eede337edaa8463(
    value: typing.Optional[ContainerNodePoolNodeConfigReservationAffinity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eab58d8968489b23e5fd4018a4e483add0697d842c865ff064c355ce28ce165(
    *,
    disk_image: builtins.str,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02b38d5b0ea2c4cd8eaaeb55c0dceb09d5bed5e957aa5c32df56f551499e9311(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cee597f5406c0478c312374dce8c920f49c43441db6268ea86102b374e8372a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e9fa07f52849295ca3b5f9edaa40d28239d956c9bc1ef878e327c5d7e66b901(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bf6620d06f8d1587180510b6c9977254d64c56a9b21edabfc3cf86b0efa57f4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__819ad13c8d3425668001d08ee3136d21c3a93f7ceb949d7e8d127eeee0cdee6c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed3ea369fa9c0bb50f1ef809f64e047d32d488f29382f07571fe643ba7b8b4c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigSecondaryBootDisks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d7244b4640ce5d89d9ccc082229db1db0f698334143bbd73227deab4b5e4f5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e60d29538a2491e2b762459bf8cdabf54bfe8b15bd3ce1b5f63e0d388b295eae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9111b0a2c0ea3583301bfc0f078fd4f0719aa5243a5946c52c5e9d29a496dcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e935bee246778b938f506b8b674ed2b76e687a51c6406efc5d569c98eb0cd3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNodeConfigSecondaryBootDisks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bd4c5365f55d4bdcdaa43c31fc4b02241fb22d4b5dc84c4a9045a301deee8f7(
    *,
    enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e23b69d931b080e8470cc408b762f0fe5516a235ab283677c12003b004b5ae5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12cbf5e6ec7b49db2cc4c35263edd946dfda50593241c940030aeeaa0c164967(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea69b37e8b4234d8d060f1c87229ec8874601c8265532a7cec67897c2ba15dc8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9ef156292c2a9d0d878e672ae2467574f9c8893156418bf2d8e241296cca664(
    value: typing.Optional[ContainerNodePoolNodeConfigShieldedInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f01db3ae9bc1942532dd9be66837c1ac53e0609e050fcfca7cc7d64d4f64976d(
    *,
    node_affinity: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b65e26105c363e9609cd55dcfed444420912892b520ffb3d025eeef0e65201(
    *,
    key: builtins.str,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c14ffbb53166762893d254a1b8ac1a722e9805798a7228600ba890e4e6dab32c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07fda06f6965b024ef8593537c1a6cf562bcf74a934fd5c69a804d1ebfad1ea9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f3774954be85b6fe251b4894f9a200985558d4cc13b40dc38c1a4614b29461(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0309c96ac515dc7c74d32a416892c1497a2d98ba08e23d1de6d8e635ed6886(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5bcb8b9453e0534f9f902d734a42d8d4d43d10853199b116d01e0e7a8a61a0b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b6ed2bed07379aab04b981c4b3ab3472580dc0416fe7b3dcf59accad0957ae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c49ddd8b0c13f0f50d5d58bc37d317ed4c57ea65157b8fbe85fd56e0d988399(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c825c0a25110e271154e8b76a5997a461cc257ef9b8d60817dcb28493695bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8cf35e54a575c4f06eab0bacb50cc6b17da4ffe3ab78dfb1fd2bb8b7ea293a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4805160176a74baad41c8a3a0baab8b32e9a3c24ee01eb77de960b75ab63c61(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d1c81b4d090939fa0d9c86cd8f250f6c33f44c25a5ec0fa04c24d619875991(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c82808f909dadca9c92ab2bd308ca79cff911551c364cd9326bc09e0d1a901(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3562adf12ca919893bfaf803b36585774ebd88b2c2a3a6be84f311bfe08a4a2e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f61d68a12e9f2dd65e43e22f3d522d307ca799e06fee7663e1f6933c93f2dd(
    value: typing.Optional[ContainerNodePoolNodeConfigSoleTenantConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0016f2b3e6f923bf4aafda4f4fcb84698611d975b253217eaa8988bd769ff342(
    *,
    effect: builtins.str,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff36a3028ba631c939419d797d77ad2107326b42ac7ec81d20bf22ac84af6f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8de42ca62f8d4745ad644beb396b4ff6d7829935c23e449b318e8552eca31d7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d62e940a5e77e61e8f6c3ad668945e0e2085b2cc2ef86502c150dd86ef84868(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f3caa69283592af3dacab34bd75924bd3262dcc5dc9bfbee391ae8eae5f547e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e24a867663a9b86fc8694b9aa88826f08b539e58d827e5e01092e07917ec070(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec99422975ba06b9c5b1ee9265fa7fdb1634b9967043d9fb526a0d0be16c9605(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNodePoolNodeConfigTaint]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aea654ec628830b7ccf54274d3fc867cb84f98ddb5357dd92505f166550d52e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176dec68eb891a03e4bcf1c8782ae4284f82e954b002cb57a109ea44fead872f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f59c2f2f06f06954b00f893aa9c5e2c7d3e5d450d1ee39e73a13e2c82bb19c11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19400fff3f53566e99bf1a1faa2a3599f41d0b848b4fab2bd37570dc8bf80fa2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53e5f500a6136a3667f96d7a012bb98c944c3665047e671e09fda862e600ed98(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolNodeConfigTaint]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ded0a6d5f90af61780a6dec7da9cf0735338931ec54c5586f01dbdf2bc90f318(
    *,
    osversion: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73853482cb03ab41f6d177bb29bb8b95b66d3e18fef029850ebb88567b580a1e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0718d5606662b51863bafde105ea8960e7ddecd98111a7c022d32a553e6512f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e959055bf1cc1403b434e4373b5643162d202ae0bb60eb9b1808479fed2d14(
    value: typing.Optional[ContainerNodePoolNodeConfigWindowsNodeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab9d9c2423d84eafa652f6e5531706f5eb79ba606d1e5853005903a69bb036ab(
    *,
    mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88f03bca74ece14604b3458345bd9f0f0251c767118f20a4e5395d83dc4b3d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__377012a99660970a4a1bc85c5b54ecdf2050dc490f32aaa4e409468aeef8c5cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baf653d4d5774b609af62d22a96b52276860e5c38f9e5d57d2d4cc08e6d4365a(
    value: typing.Optional[ContainerNodePoolNodeConfigWorkloadMetadataConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e6642538ef61b97bc1af6976ae9895e8312a74aa0446e5079055f2904b6e87(
    *,
    type: builtins.str,
    policy_name: typing.Optional[builtins.str] = None,
    tpu_topology: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9d753c011ca10d1ea912432a99be94156fce69370d4da61467f224077eae46d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08e898baf46c4718917bf8218bdbdf9a7350e1097994fb471e92b2eb514109b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9568af32bb7c74c8dbc94511246069475a9b1d5e285014b19704d2d1bcb563b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f048f5d12c742dccba5daafef22b924f7cd07c2aac73ec22789bd6ecd8e6ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__867a1126ed2d9bb087c10601fc820a0fc9b6fae0a77e47b42ec70744649453f6(
    value: typing.Optional[ContainerNodePoolPlacementPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1113f9e174ebb0cebf604def927211546818d61c540071d104673bc71b5a9f68(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed24557764b138ab3d46e0d026cb9bccaefab28bfd5a2f826a773b4988fd305f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed34a48759308fdb680d353e07e8f1608e332b13e5939fb22c7897ca4fe275e2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1468f539d2385b9a047fa40aeea57ede93f0e5adbacfa1b26633ea04f5d8564d(
    value: typing.Optional[ContainerNodePoolQueuedProvisioning],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00d50d647b29f1cf517fadb60788122d1f12bf6f635e803cdf353f3e4064b142(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6751cef689cf9db2ddd2cc1879dda567c42792813e15509983349adcbafb965b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fca7952eec065e391ee5961fbd01121fa098845e6e560c372f5aac526ec56c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b84dd4325f7e438db71081e747685a3cb1e4021dbf45ec1917f9af8265b676(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dea43a55eb0c78c4ab529257d775cf4c578f690370a632bacba4dd363c480c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbbec86c81a01f2b47afa8fe8030ccfe6e510da8b7cc17e30e836aaef9f59bb6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNodePoolTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a02f38344473e92516fa2bacad720308fc5a9e1525dd040ad22e90b14709b32b(
    *,
    blue_green_settings: typing.Optional[typing.Union[ContainerNodePoolUpgradeSettingsBlueGreenSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    max_surge: typing.Optional[jsii.Number] = None,
    max_unavailable: typing.Optional[jsii.Number] = None,
    strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d225c90e864edb72c84817010ebd10cda426c64bcf61807a35e8fb8bc3661477(
    *,
    standard_rollout_policy: typing.Union[ContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy, typing.Dict[builtins.str, typing.Any]],
    node_pool_soak_duration: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c65c3281f99dfa16c1494670f51bd49f900cebd758d758f61fc15a2c11a8d52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7404ece40b3f38ea99f4fd7c051843be348f68661a588aa1a2c0e83ac38ffb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb0f66122bd4eeec8645552c9d2cd6b0851158106bb8588842210a94f4deb48c(
    value: typing.Optional[ContainerNodePoolUpgradeSettingsBlueGreenSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f880fd10db6be0e44d38df6749b4bd32fb05552fbced7b29e37806325b7753bb(
    *,
    batch_node_count: typing.Optional[jsii.Number] = None,
    batch_percentage: typing.Optional[jsii.Number] = None,
    batch_soak_duration: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a83f3b825ccc466524d067771b8ad51d89b09fc5cd6d252720a73516127942(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__548fdfb6bf73a658b7e1354d8db185179eb3069fd8150754d7910063e86f36c6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3eef1d916c9a7c5a970c857c93e214a7fae7a8d62bdafcbf30ae2a0728684b5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cee43be0b9f43019ff58f3dbe5b7287952d49a42c5d8caf5ee703aa3a09a14a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1b64d4f07eaf087e734038dbe7c0d7f32ab53adda16a571fb83c5ee1384c662(
    value: typing.Optional[ContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__898832cf47fc36bcc62d5fa833e94aca0f7333d4cfaaf5d29cb2bd64f79356ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d48d4d54f6811cedfdacaeb3116177e9e3ab0ddcf3457f86a186163ed99ecc30(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d6d62667d8295eb2d864bd695e9242d4dca67491299933c7f1d9f5cae92ee38(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__950b1e0c01f456486a57e25ba4afebf1dfb32735174e2851bba52f7eaa0293e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__720d025b5be7dfb570dc48eb1cd0296b0e40367f77ed6a011717515fb232342d(
    value: typing.Optional[ContainerNodePoolUpgradeSettings],
) -> None:
    """Type checking stubs"""
    pass
