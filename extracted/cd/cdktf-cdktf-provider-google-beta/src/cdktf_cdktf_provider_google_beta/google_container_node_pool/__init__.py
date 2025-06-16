r'''
# `google_container_node_pool`

Refer to the Terraform Registry for docs: [`google_container_node_pool`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool).
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


class GoogleContainerNodePool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool google_container_node_pool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster: builtins.str,
        autoscaling: typing.Optional[typing.Union["GoogleContainerNodePoolAutoscaling", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        initial_node_count: typing.Optional[jsii.Number] = None,
        location: typing.Optional[builtins.str] = None,
        management: typing.Optional[typing.Union["GoogleContainerNodePoolManagement", typing.Dict[builtins.str, typing.Any]]] = None,
        max_pods_per_node: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        network_config: typing.Optional[typing.Union["GoogleContainerNodePoolNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_count: typing.Optional[jsii.Number] = None,
        node_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
        placement_policy: typing.Optional[typing.Union["GoogleContainerNodePoolPlacementPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        queued_provisioning: typing.Optional[typing.Union["GoogleContainerNodePoolQueuedProvisioning", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleContainerNodePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        upgrade_settings: typing.Optional[typing.Union["GoogleContainerNodePoolUpgradeSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool google_container_node_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster: The cluster to create the node pool for. Cluster must be present in location provided for zonal clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#cluster GoogleContainerNodePool#cluster}
        :param autoscaling: autoscaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#autoscaling GoogleContainerNodePool#autoscaling}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#id GoogleContainerNodePool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_node_count: The initial number of nodes for the pool. In regional or multi-zonal clusters, this is the number of nodes per zone. Changing this will force recreation of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#initial_node_count GoogleContainerNodePool#initial_node_count}
        :param location: The location (region or zone) of the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#location GoogleContainerNodePool#location}
        :param management: management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#management GoogleContainerNodePool#management}
        :param max_pods_per_node: The maximum number of pods per node in this node pool. Note that this does not work on node pools which are "route-based" - that is, node pools belonging to clusters that do not have IP Aliasing enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#max_pods_per_node GoogleContainerNodePool#max_pods_per_node}
        :param name: The name of the node pool. If left blank, Terraform will auto-generate a unique name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#name GoogleContainerNodePool#name}
        :param name_prefix: Creates a unique name for the node pool beginning with the specified prefix. Conflicts with name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#name_prefix GoogleContainerNodePool#name_prefix}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#network_config GoogleContainerNodePool#network_config}
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#node_config GoogleContainerNodePool#node_config}
        :param node_count: The number of nodes per instance group. This field can be used to update the number of nodes per instance group but should not be used alongside autoscaling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#node_count GoogleContainerNodePool#node_count}
        :param node_locations: The list of zones in which the node pool's nodes should be located. Nodes must be in the region of their regional cluster or in the same region as their cluster's zone for zonal clusters. If unspecified, the cluster-level node_locations will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#node_locations GoogleContainerNodePool#node_locations}
        :param placement_policy: placement_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#placement_policy GoogleContainerNodePool#placement_policy}
        :param project: The ID of the project in which to create the node pool. If blank, the provider-configured project will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#project GoogleContainerNodePool#project}
        :param queued_provisioning: queued_provisioning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#queued_provisioning GoogleContainerNodePool#queued_provisioning}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#timeouts GoogleContainerNodePool#timeouts}
        :param upgrade_settings: upgrade_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#upgrade_settings GoogleContainerNodePool#upgrade_settings}
        :param version: The Kubernetes version for the nodes in this pool. Note that if this field and auto_upgrade are both specified, they will fight each other for what the node version should be, so setting both is highly discouraged. While a fuzzy version can be specified, it's recommended that you specify explicit versions as Terraform will see spurious diffs when fuzzy versions are used. See the google_container_engine_versions data source's version_prefix field to approximate fuzzy versions in a Terraform-compatible way. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#version GoogleContainerNodePool#version}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f75cf1f4c113470aebc6bebc3ac0bd156d49a6d1cd6f50e192de6ed4291c711f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleContainerNodePoolConfig(
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
        '''Generates CDKTF code for importing a GoogleContainerNodePool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleContainerNodePool to import.
        :param import_from_id: The id of the existing GoogleContainerNodePool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleContainerNodePool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f572c8394bbc47a068c4bf577944599f603d50621320dce758bec0dc25b02408)
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
        :param location_policy: Location policy specifies the algorithm used when scaling-up the node pool. "BALANCED" - Is a best effort policy that aims to balance the sizes of available zones. "ANY" - Instructs the cluster autoscaler to prioritize utilization of unused reservations, and reduces preemption risk for Spot VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#location_policy GoogleContainerNodePool#location_policy}
        :param max_node_count: Maximum number of nodes per zone in the node pool. Must be >= min_node_count. Cannot be used with total limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#max_node_count GoogleContainerNodePool#max_node_count}
        :param min_node_count: Minimum number of nodes per zone in the node pool. Must be >=0 and <= max_node_count. Cannot be used with total limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#min_node_count GoogleContainerNodePool#min_node_count}
        :param total_max_node_count: Maximum number of all nodes in the node pool. Must be >= total_min_node_count. Cannot be used with per zone limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#total_max_node_count GoogleContainerNodePool#total_max_node_count}
        :param total_min_node_count: Minimum number of all nodes in the node pool. Must be >=0 and <= total_max_node_count. Cannot be used with per zone limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#total_min_node_count GoogleContainerNodePool#total_min_node_count}
        '''
        value = GoogleContainerNodePoolAutoscaling(
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
        :param auto_repair: Whether the nodes will be automatically repaired. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#auto_repair GoogleContainerNodePool#auto_repair}
        :param auto_upgrade: Whether the nodes will be automatically upgraded. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#auto_upgrade GoogleContainerNodePool#auto_upgrade}
        '''
        value = GoogleContainerNodePoolManagement(
            auto_repair=auto_repair, auto_upgrade=auto_upgrade
        )

        return typing.cast(None, jsii.invoke(self, "putManagement", [value]))

    @jsii.member(jsii_name="putNetworkConfig")
    def put_network_config(
        self,
        *,
        additional_node_network_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        additional_pod_network_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        create_pod_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_private_nodes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network_performance_config: typing.Optional[typing.Union["GoogleContainerNodePoolNetworkConfigNetworkPerformanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        pod_cidr_overprovision_config: typing.Optional[typing.Union["GoogleContainerNodePoolNetworkConfigPodCidrOverprovisionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        pod_ipv4_cidr_block: typing.Optional[builtins.str] = None,
        pod_range: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param additional_node_network_configs: additional_node_network_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#additional_node_network_configs GoogleContainerNodePool#additional_node_network_configs}
        :param additional_pod_network_configs: additional_pod_network_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#additional_pod_network_configs GoogleContainerNodePool#additional_pod_network_configs}
        :param create_pod_range: Whether to create a new range for pod IPs in this node pool. Defaults are provided for pod_range and pod_ipv4_cidr_block if they are not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#create_pod_range GoogleContainerNodePool#create_pod_range}
        :param enable_private_nodes: Whether nodes have internal IP addresses only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enable_private_nodes GoogleContainerNodePool#enable_private_nodes}
        :param network_performance_config: network_performance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#network_performance_config GoogleContainerNodePool#network_performance_config}
        :param pod_cidr_overprovision_config: pod_cidr_overprovision_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#pod_cidr_overprovision_config GoogleContainerNodePool#pod_cidr_overprovision_config}
        :param pod_ipv4_cidr_block: The IP address range for pod IPs in this node pool. Only applicable if create_pod_range is true. Set to blank to have a range chosen with the default size. Set to /netmask (e.g. /14) to have a range chosen with a specific netmask. Set to a CIDR notation (e.g. 10.96.0.0/14) to pick a specific range to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#pod_ipv4_cidr_block GoogleContainerNodePool#pod_ipv4_cidr_block}
        :param pod_range: The ID of the secondary range for pod IPs. If create_pod_range is true, this ID is used for the new range. If create_pod_range is false, uses an existing secondary range with this ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#pod_range GoogleContainerNodePool#pod_range}
        '''
        value = GoogleContainerNodePoolNetworkConfig(
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
        advanced_machine_features: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigAdvancedMachineFeatures", typing.Dict[builtins.str, typing.Any]]] = None,
        boot_disk_kms_key: typing.Optional[builtins.str] = None,
        confidential_nodes: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigConfidentialNodes", typing.Dict[builtins.str, typing.Any]]] = None,
        containerd_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigContainerdConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        disk_type: typing.Optional[builtins.str] = None,
        enable_confidential_storage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ephemeral_storage_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigEphemeralStorageConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ephemeral_storage_local_ssd_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        fast_socket: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigFastSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        flex_start: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcfs_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigGcfsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        guest_accelerator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerNodePoolNodeConfigGuestAccelerator", typing.Dict[builtins.str, typing.Any]]]]] = None,
        gvnic: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigGvnic", typing.Dict[builtins.str, typing.Any]]] = None,
        host_maintenance_policy: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigHostMaintenancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        image_type: typing.Optional[builtins.str] = None,
        kubelet_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigKubeletConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        linux_node_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigLinuxNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        local_nvme_ssd_block_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig", typing.Dict[builtins.str, typing.Any]]] = None,
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
        reservation_affinity: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigReservationAffinity", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        sandbox_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigSandboxConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        secondary_boot_disks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerNodePoolNodeConfigSecondaryBootDisks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_account: typing.Optional[builtins.str] = None,
        shielded_instance_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        sole_tenant_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigSoleTenantConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        storage_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        taint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerNodePoolNodeConfigTaint", typing.Dict[builtins.str, typing.Any]]]]] = None,
        windows_node_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigWindowsNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        workload_metadata_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigWorkloadMetadataConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_machine_features: advanced_machine_features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#advanced_machine_features GoogleContainerNodePool#advanced_machine_features}
        :param boot_disk_kms_key: The Customer Managed Encryption Key used to encrypt the boot disk attached to each node in the node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#boot_disk_kms_key GoogleContainerNodePool#boot_disk_kms_key}
        :param confidential_nodes: confidential_nodes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#confidential_nodes GoogleContainerNodePool#confidential_nodes}
        :param containerd_config: containerd_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#containerd_config GoogleContainerNodePool#containerd_config}
        :param disk_size_gb: Size of the disk attached to each node, specified in GB. The smallest allowed disk size is 10GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#disk_size_gb GoogleContainerNodePool#disk_size_gb}
        :param disk_type: Type of the disk attached to each node. Such as pd-standard, pd-balanced or pd-ssd. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#disk_type GoogleContainerNodePool#disk_type}
        :param enable_confidential_storage: If enabled boot disks are configured with confidential mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enable_confidential_storage GoogleContainerNodePool#enable_confidential_storage}
        :param ephemeral_storage_config: ephemeral_storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#ephemeral_storage_config GoogleContainerNodePool#ephemeral_storage_config}
        :param ephemeral_storage_local_ssd_config: ephemeral_storage_local_ssd_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#ephemeral_storage_local_ssd_config GoogleContainerNodePool#ephemeral_storage_local_ssd_config}
        :param fast_socket: fast_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#fast_socket GoogleContainerNodePool#fast_socket}
        :param flex_start: Enables Flex Start provisioning model for the node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#flex_start GoogleContainerNodePool#flex_start}
        :param gcfs_config: gcfs_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#gcfs_config GoogleContainerNodePool#gcfs_config}
        :param guest_accelerator: guest_accelerator block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#guest_accelerator GoogleContainerNodePool#guest_accelerator}
        :param gvnic: gvnic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#gvnic GoogleContainerNodePool#gvnic}
        :param host_maintenance_policy: host_maintenance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#host_maintenance_policy GoogleContainerNodePool#host_maintenance_policy}
        :param image_type: The image type to use for this node. Note that for a given image type, the latest version of it will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#image_type GoogleContainerNodePool#image_type}
        :param kubelet_config: kubelet_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#kubelet_config GoogleContainerNodePool#kubelet_config}
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#labels GoogleContainerNodePool#labels}
        :param linux_node_config: linux_node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#linux_node_config GoogleContainerNodePool#linux_node_config}
        :param local_nvme_ssd_block_config: local_nvme_ssd_block_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#local_nvme_ssd_block_config GoogleContainerNodePool#local_nvme_ssd_block_config}
        :param local_ssd_count: The number of local SSD disks to be attached to the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#local_ssd_count GoogleContainerNodePool#local_ssd_count}
        :param local_ssd_encryption_mode: LocalSsdEncryptionMode specified the method used for encrypting the local SSDs attached to the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#local_ssd_encryption_mode GoogleContainerNodePool#local_ssd_encryption_mode}
        :param logging_variant: Type of logging agent that is used as the default value for node pools in the cluster. Valid values include DEFAULT and MAX_THROUGHPUT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#logging_variant GoogleContainerNodePool#logging_variant}
        :param machine_type: The name of a Google Compute Engine machine type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#machine_type GoogleContainerNodePool#machine_type}
        :param max_run_duration: The runtime of each node in the node pool in seconds, terminated by 's'. Example: "3600s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#max_run_duration GoogleContainerNodePool#max_run_duration}
        :param metadata: The metadata key/value pairs assigned to instances in the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#metadata GoogleContainerNodePool#metadata}
        :param min_cpu_platform: Minimum CPU platform to be used by this instance. The instance may be scheduled on the specified or newer CPU platform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#min_cpu_platform GoogleContainerNodePool#min_cpu_platform}
        :param node_group: Setting this field will assign instances of this pool to run on the specified node group. This is useful for running workloads on sole tenant nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#node_group GoogleContainerNodePool#node_group}
        :param oauth_scopes: The set of Google API scopes to be made available on all of the node VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#oauth_scopes GoogleContainerNodePool#oauth_scopes}
        :param preemptible: Whether the nodes are created as preemptible VM instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#preemptible GoogleContainerNodePool#preemptible}
        :param reservation_affinity: reservation_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#reservation_affinity GoogleContainerNodePool#reservation_affinity}
        :param resource_labels: The GCE resource labels (a map of key/value pairs) to be applied to the node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#resource_labels GoogleContainerNodePool#resource_labels}
        :param resource_manager_tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#resource_manager_tags GoogleContainerNodePool#resource_manager_tags}
        :param sandbox_config: sandbox_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#sandbox_config GoogleContainerNodePool#sandbox_config}
        :param secondary_boot_disks: secondary_boot_disks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#secondary_boot_disks GoogleContainerNodePool#secondary_boot_disks}
        :param service_account: The Google Cloud Platform Service Account to be used by the node VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#service_account GoogleContainerNodePool#service_account}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#shielded_instance_config GoogleContainerNodePool#shielded_instance_config}
        :param sole_tenant_config: sole_tenant_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#sole_tenant_config GoogleContainerNodePool#sole_tenant_config}
        :param spot: Whether the nodes are created as spot VM instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#spot GoogleContainerNodePool#spot}
        :param storage_pools: The list of Storage Pools where boot disks are provisioned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#storage_pools GoogleContainerNodePool#storage_pools}
        :param tags: The list of instance tags applied to all nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#tags GoogleContainerNodePool#tags}
        :param taint: taint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#taint GoogleContainerNodePool#taint}
        :param windows_node_config: windows_node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#windows_node_config GoogleContainerNodePool#windows_node_config}
        :param workload_metadata_config: workload_metadata_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#workload_metadata_config GoogleContainerNodePool#workload_metadata_config}
        '''
        value = GoogleContainerNodePoolNodeConfig(
            advanced_machine_features=advanced_machine_features,
            boot_disk_kms_key=boot_disk_kms_key,
            confidential_nodes=confidential_nodes,
            containerd_config=containerd_config,
            disk_size_gb=disk_size_gb,
            disk_type=disk_type,
            enable_confidential_storage=enable_confidential_storage,
            ephemeral_storage_config=ephemeral_storage_config,
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
            sandbox_config=sandbox_config,
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
        :param type: Type defines the type of placement policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#type GoogleContainerNodePool#type}
        :param policy_name: If set, refers to the name of a custom resource policy supplied by the user. The resource policy must be in the same project and region as the node pool. If not found, InvalidArgument error is returned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#policy_name GoogleContainerNodePool#policy_name}
        :param tpu_topology: The TPU topology like "2x4" or "2x2x2". https://cloud.google.com/kubernetes-engine/docs/concepts/plan-tpus#topology. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#tpu_topology GoogleContainerNodePool#tpu_topology}
        '''
        value = GoogleContainerNodePoolPlacementPolicy(
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
        :param enabled: Whether nodes in this node pool are obtainable solely through the ProvisioningRequest API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enabled GoogleContainerNodePool#enabled}
        '''
        value = GoogleContainerNodePoolQueuedProvisioning(enabled=enabled)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#create GoogleContainerNodePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#delete GoogleContainerNodePool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#update GoogleContainerNodePool#update}.
        '''
        value = GoogleContainerNodePoolTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUpgradeSettings")
    def put_upgrade_settings(
        self,
        *,
        blue_green_settings: typing.Optional[typing.Union["GoogleContainerNodePoolUpgradeSettingsBlueGreenSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        max_surge: typing.Optional[jsii.Number] = None,
        max_unavailable: typing.Optional[jsii.Number] = None,
        strategy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param blue_green_settings: blue_green_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#blue_green_settings GoogleContainerNodePool#blue_green_settings}
        :param max_surge: The number of additional nodes that can be added to the node pool during an upgrade. Increasing max_surge raises the number of nodes that can be upgraded simultaneously. Can be set to 0 or greater. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#max_surge GoogleContainerNodePool#max_surge}
        :param max_unavailable: The number of nodes that can be simultaneously unavailable during an upgrade. Increasing max_unavailable raises the number of nodes that can be upgraded in parallel. Can be set to 0 or greater. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#max_unavailable GoogleContainerNodePool#max_unavailable}
        :param strategy: Update strategy for the given nodepool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#strategy GoogleContainerNodePool#strategy}
        '''
        value = GoogleContainerNodePoolUpgradeSettings(
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
    def autoscaling(self) -> "GoogleContainerNodePoolAutoscalingOutputReference":
        return typing.cast("GoogleContainerNodePoolAutoscalingOutputReference", jsii.get(self, "autoscaling"))

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
    def management(self) -> "GoogleContainerNodePoolManagementOutputReference":
        return typing.cast("GoogleContainerNodePoolManagementOutputReference", jsii.get(self, "management"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(self) -> "GoogleContainerNodePoolNetworkConfigOutputReference":
        return typing.cast("GoogleContainerNodePoolNetworkConfigOutputReference", jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfig")
    def node_config(self) -> "GoogleContainerNodePoolNodeConfigOutputReference":
        return typing.cast("GoogleContainerNodePoolNodeConfigOutputReference", jsii.get(self, "nodeConfig"))

    @builtins.property
    @jsii.member(jsii_name="operation")
    def operation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operation"))

    @builtins.property
    @jsii.member(jsii_name="placementPolicy")
    def placement_policy(
        self,
    ) -> "GoogleContainerNodePoolPlacementPolicyOutputReference":
        return typing.cast("GoogleContainerNodePoolPlacementPolicyOutputReference", jsii.get(self, "placementPolicy"))

    @builtins.property
    @jsii.member(jsii_name="queuedProvisioning")
    def queued_provisioning(
        self,
    ) -> "GoogleContainerNodePoolQueuedProvisioningOutputReference":
        return typing.cast("GoogleContainerNodePoolQueuedProvisioningOutputReference", jsii.get(self, "queuedProvisioning"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleContainerNodePoolTimeoutsOutputReference":
        return typing.cast("GoogleContainerNodePoolTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="upgradeSettings")
    def upgrade_settings(
        self,
    ) -> "GoogleContainerNodePoolUpgradeSettingsOutputReference":
        return typing.cast("GoogleContainerNodePoolUpgradeSettingsOutputReference", jsii.get(self, "upgradeSettings"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingInput")
    def autoscaling_input(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolAutoscaling"]:
        return typing.cast(typing.Optional["GoogleContainerNodePoolAutoscaling"], jsii.get(self, "autoscalingInput"))

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
    def management_input(self) -> typing.Optional["GoogleContainerNodePoolManagement"]:
        return typing.cast(typing.Optional["GoogleContainerNodePoolManagement"], jsii.get(self, "managementInput"))

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
    def network_config_input(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNetworkConfig"]:
        return typing.cast(typing.Optional["GoogleContainerNodePoolNetworkConfig"], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfigInput")
    def node_config_input(self) -> typing.Optional["GoogleContainerNodePoolNodeConfig"]:
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfig"], jsii.get(self, "nodeConfigInput"))

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
    ) -> typing.Optional["GoogleContainerNodePoolPlacementPolicy"]:
        return typing.cast(typing.Optional["GoogleContainerNodePoolPlacementPolicy"], jsii.get(self, "placementPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="queuedProvisioningInput")
    def queued_provisioning_input(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolQueuedProvisioning"]:
        return typing.cast(typing.Optional["GoogleContainerNodePoolQueuedProvisioning"], jsii.get(self, "queuedProvisioningInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleContainerNodePoolTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleContainerNodePoolTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="upgradeSettingsInput")
    def upgrade_settings_input(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolUpgradeSettings"]:
        return typing.cast(typing.Optional["GoogleContainerNodePoolUpgradeSettings"], jsii.get(self, "upgradeSettingsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__81585b084a75592c5e3706d4af74e68f36aa22552975bfc892fabe709cd68a93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c48c4bf2a2e4b93438ccc44e9e308390e16c2f93480729af0864bf8fcdb7794)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialNodeCount")
    def initial_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialNodeCount"))

    @initial_node_count.setter
    def initial_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c61929a40bb8705acf4362b8eaf62f2baafd7567509c759af365e149731a020)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__704c1758a74418784eae7802f36846db75082e7402be0ebfa99e848d7f40c078)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxPodsPerNode")
    def max_pods_per_node(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPodsPerNode"))

    @max_pods_per_node.setter
    def max_pods_per_node(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c02dee5f56c3abdc39bb4e8bff7e7810c84b6b802fc3ad1ed11a0cdcd53bc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPodsPerNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__415f2d44014be5f55268a27092218cbdfa10c6db46eff6f23725b42d3d7b28f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namePrefix")
    def name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namePrefix"))

    @name_prefix.setter
    def name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d9c0c424628c611ef7cf1e04ee271b3e5085940c2d1ef9a8ee6ca572735e77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80ecfcd52d0067562ef6c905b0ce3c1cb7dce917af196328f8cf80bcffb9778b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeLocations")
    def node_locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "nodeLocations"))

    @node_locations.setter
    def node_locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__816e68d06296456ca033c553ee6656cb4a59fd19d5e07d2fe98f8620fab55da1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeLocations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfed50f56cb91855a1001533be060dc5ad6cbdd28d8308e6734de92794386f47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84e6080263da48bee69e742df775d7961bc11f1f69da78eca068c2632dfa54a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolAutoscaling",
    jsii_struct_bases=[],
    name_mapping={
        "location_policy": "locationPolicy",
        "max_node_count": "maxNodeCount",
        "min_node_count": "minNodeCount",
        "total_max_node_count": "totalMaxNodeCount",
        "total_min_node_count": "totalMinNodeCount",
    },
)
class GoogleContainerNodePoolAutoscaling:
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
        :param location_policy: Location policy specifies the algorithm used when scaling-up the node pool. "BALANCED" - Is a best effort policy that aims to balance the sizes of available zones. "ANY" - Instructs the cluster autoscaler to prioritize utilization of unused reservations, and reduces preemption risk for Spot VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#location_policy GoogleContainerNodePool#location_policy}
        :param max_node_count: Maximum number of nodes per zone in the node pool. Must be >= min_node_count. Cannot be used with total limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#max_node_count GoogleContainerNodePool#max_node_count}
        :param min_node_count: Minimum number of nodes per zone in the node pool. Must be >=0 and <= max_node_count. Cannot be used with total limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#min_node_count GoogleContainerNodePool#min_node_count}
        :param total_max_node_count: Maximum number of all nodes in the node pool. Must be >= total_min_node_count. Cannot be used with per zone limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#total_max_node_count GoogleContainerNodePool#total_max_node_count}
        :param total_min_node_count: Minimum number of all nodes in the node pool. Must be >=0 and <= total_max_node_count. Cannot be used with per zone limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#total_min_node_count GoogleContainerNodePool#total_min_node_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62328d6aae5eae7f3d514da0e78b03c79612e2e5f431951301ae48f85e56bab6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#location_policy GoogleContainerNodePool#location_policy}
        '''
        result = self._values.get("location_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_node_count(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of nodes per zone in the node pool.

        Must be >= min_node_count. Cannot be used with total limits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#max_node_count GoogleContainerNodePool#max_node_count}
        '''
        result = self._values.get("max_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_node_count(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of nodes per zone in the node pool.

        Must be >=0 and <= max_node_count. Cannot be used with total limits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#min_node_count GoogleContainerNodePool#min_node_count}
        '''
        result = self._values.get("min_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def total_max_node_count(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of all nodes in the node pool.

        Must be >= total_min_node_count. Cannot be used with per zone limits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#total_max_node_count GoogleContainerNodePool#total_max_node_count}
        '''
        result = self._values.get("total_max_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def total_min_node_count(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of all nodes in the node pool.

        Must be >=0 and <= total_max_node_count. Cannot be used with per zone limits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#total_min_node_count GoogleContainerNodePool#total_min_node_count}
        '''
        result = self._values.get("total_min_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolAutoscaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolAutoscalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolAutoscalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea6e7409413f0fc48829caa13d817fd8015042db5fadbbbdfe306cc470b16230)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0c15ce7b2fe3ff14ba262606cf60c325f83fa6c6553f7be2686039f8ea3b0f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locationPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxNodeCount")
    def max_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxNodeCount"))

    @max_node_count.setter
    def max_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91f7cb34e10e8a57ff9e3ba6c95adc6369aaf96b12061399856f9f6ace845e0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNodeCount")
    def min_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNodeCount"))

    @min_node_count.setter
    def min_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__487660a99f7c64d19c4190435a15b38388a4da154a4661c594e749bbb6bee17c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="totalMaxNodeCount")
    def total_max_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalMaxNodeCount"))

    @total_max_node_count.setter
    def total_max_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aaa234adc7ed238d1b00176d3cad8de2e782a4a36e27414cb0651b7f1f3ff75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "totalMaxNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="totalMinNodeCount")
    def total_min_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalMinNodeCount"))

    @total_min_node_count.setter
    def total_min_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__515d47a796a60062d7644cae62cb074d21be87201210aea0c046c701e5540a04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "totalMinNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleContainerNodePoolAutoscaling]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolAutoscaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolAutoscaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb9a1cc5dfd72df0873603c99766e896fdbe8dcf5f4aef19ba20980d351b4041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolConfig",
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
class GoogleContainerNodePoolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        autoscaling: typing.Optional[typing.Union[GoogleContainerNodePoolAutoscaling, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        initial_node_count: typing.Optional[jsii.Number] = None,
        location: typing.Optional[builtins.str] = None,
        management: typing.Optional[typing.Union["GoogleContainerNodePoolManagement", typing.Dict[builtins.str, typing.Any]]] = None,
        max_pods_per_node: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        network_config: typing.Optional[typing.Union["GoogleContainerNodePoolNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_count: typing.Optional[jsii.Number] = None,
        node_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
        placement_policy: typing.Optional[typing.Union["GoogleContainerNodePoolPlacementPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        queued_provisioning: typing.Optional[typing.Union["GoogleContainerNodePoolQueuedProvisioning", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleContainerNodePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        upgrade_settings: typing.Optional[typing.Union["GoogleContainerNodePoolUpgradeSettings", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param cluster: The cluster to create the node pool for. Cluster must be present in location provided for zonal clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#cluster GoogleContainerNodePool#cluster}
        :param autoscaling: autoscaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#autoscaling GoogleContainerNodePool#autoscaling}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#id GoogleContainerNodePool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_node_count: The initial number of nodes for the pool. In regional or multi-zonal clusters, this is the number of nodes per zone. Changing this will force recreation of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#initial_node_count GoogleContainerNodePool#initial_node_count}
        :param location: The location (region or zone) of the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#location GoogleContainerNodePool#location}
        :param management: management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#management GoogleContainerNodePool#management}
        :param max_pods_per_node: The maximum number of pods per node in this node pool. Note that this does not work on node pools which are "route-based" - that is, node pools belonging to clusters that do not have IP Aliasing enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#max_pods_per_node GoogleContainerNodePool#max_pods_per_node}
        :param name: The name of the node pool. If left blank, Terraform will auto-generate a unique name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#name GoogleContainerNodePool#name}
        :param name_prefix: Creates a unique name for the node pool beginning with the specified prefix. Conflicts with name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#name_prefix GoogleContainerNodePool#name_prefix}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#network_config GoogleContainerNodePool#network_config}
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#node_config GoogleContainerNodePool#node_config}
        :param node_count: The number of nodes per instance group. This field can be used to update the number of nodes per instance group but should not be used alongside autoscaling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#node_count GoogleContainerNodePool#node_count}
        :param node_locations: The list of zones in which the node pool's nodes should be located. Nodes must be in the region of their regional cluster or in the same region as their cluster's zone for zonal clusters. If unspecified, the cluster-level node_locations will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#node_locations GoogleContainerNodePool#node_locations}
        :param placement_policy: placement_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#placement_policy GoogleContainerNodePool#placement_policy}
        :param project: The ID of the project in which to create the node pool. If blank, the provider-configured project will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#project GoogleContainerNodePool#project}
        :param queued_provisioning: queued_provisioning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#queued_provisioning GoogleContainerNodePool#queued_provisioning}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#timeouts GoogleContainerNodePool#timeouts}
        :param upgrade_settings: upgrade_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#upgrade_settings GoogleContainerNodePool#upgrade_settings}
        :param version: The Kubernetes version for the nodes in this pool. Note that if this field and auto_upgrade are both specified, they will fight each other for what the node version should be, so setting both is highly discouraged. While a fuzzy version can be specified, it's recommended that you specify explicit versions as Terraform will see spurious diffs when fuzzy versions are used. See the google_container_engine_versions data source's version_prefix field to approximate fuzzy versions in a Terraform-compatible way. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#version GoogleContainerNodePool#version}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(autoscaling, dict):
            autoscaling = GoogleContainerNodePoolAutoscaling(**autoscaling)
        if isinstance(management, dict):
            management = GoogleContainerNodePoolManagement(**management)
        if isinstance(network_config, dict):
            network_config = GoogleContainerNodePoolNetworkConfig(**network_config)
        if isinstance(node_config, dict):
            node_config = GoogleContainerNodePoolNodeConfig(**node_config)
        if isinstance(placement_policy, dict):
            placement_policy = GoogleContainerNodePoolPlacementPolicy(**placement_policy)
        if isinstance(queued_provisioning, dict):
            queued_provisioning = GoogleContainerNodePoolQueuedProvisioning(**queued_provisioning)
        if isinstance(timeouts, dict):
            timeouts = GoogleContainerNodePoolTimeouts(**timeouts)
        if isinstance(upgrade_settings, dict):
            upgrade_settings = GoogleContainerNodePoolUpgradeSettings(**upgrade_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ea29e6dbff83ef660066146f8c46000f2e00cb18bdc726304a3af1ba3895fbe)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#cluster GoogleContainerNodePool#cluster}
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autoscaling(self) -> typing.Optional[GoogleContainerNodePoolAutoscaling]:
        '''autoscaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#autoscaling GoogleContainerNodePool#autoscaling}
        '''
        result = self._values.get("autoscaling")
        return typing.cast(typing.Optional[GoogleContainerNodePoolAutoscaling], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#id GoogleContainerNodePool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_node_count(self) -> typing.Optional[jsii.Number]:
        '''The initial number of nodes for the pool.

        In regional or multi-zonal clusters, this is the number of nodes per zone. Changing this will force recreation of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#initial_node_count GoogleContainerNodePool#initial_node_count}
        '''
        result = self._values.get("initial_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location (region or zone) of the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#location GoogleContainerNodePool#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def management(self) -> typing.Optional["GoogleContainerNodePoolManagement"]:
        '''management block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#management GoogleContainerNodePool#management}
        '''
        result = self._values.get("management")
        return typing.cast(typing.Optional["GoogleContainerNodePoolManagement"], result)

    @builtins.property
    def max_pods_per_node(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of pods per node in this node pool.

        Note that this does not work on node pools which are "route-based" - that is, node pools belonging to clusters that do not have IP Aliasing enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#max_pods_per_node GoogleContainerNodePool#max_pods_per_node}
        '''
        result = self._values.get("max_pods_per_node")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the node pool. If left blank, Terraform will auto-generate a unique name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#name GoogleContainerNodePool#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_prefix(self) -> typing.Optional[builtins.str]:
        '''Creates a unique name for the node pool beginning with the specified prefix. Conflicts with name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#name_prefix GoogleContainerNodePool#name_prefix}
        '''
        result = self._values.get("name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_config(self) -> typing.Optional["GoogleContainerNodePoolNetworkConfig"]:
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#network_config GoogleContainerNodePool#network_config}
        '''
        result = self._values.get("network_config")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNetworkConfig"], result)

    @builtins.property
    def node_config(self) -> typing.Optional["GoogleContainerNodePoolNodeConfig"]:
        '''node_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#node_config GoogleContainerNodePool#node_config}
        '''
        result = self._values.get("node_config")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfig"], result)

    @builtins.property
    def node_count(self) -> typing.Optional[jsii.Number]:
        '''The number of nodes per instance group.

        This field can be used to update the number of nodes per instance group but should not be used alongside autoscaling.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#node_count GoogleContainerNodePool#node_count}
        '''
        result = self._values.get("node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def node_locations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of zones in which the node pool's nodes should be located.

        Nodes must be in the region of their regional cluster or in the same region as their cluster's zone for zonal clusters. If unspecified, the cluster-level node_locations will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#node_locations GoogleContainerNodePool#node_locations}
        '''
        result = self._values.get("node_locations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def placement_policy(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolPlacementPolicy"]:
        '''placement_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#placement_policy GoogleContainerNodePool#placement_policy}
        '''
        result = self._values.get("placement_policy")
        return typing.cast(typing.Optional["GoogleContainerNodePoolPlacementPolicy"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which to create the node pool.

        If blank, the provider-configured project will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#project GoogleContainerNodePool#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def queued_provisioning(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolQueuedProvisioning"]:
        '''queued_provisioning block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#queued_provisioning GoogleContainerNodePool#queued_provisioning}
        '''
        result = self._values.get("queued_provisioning")
        return typing.cast(typing.Optional["GoogleContainerNodePoolQueuedProvisioning"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleContainerNodePoolTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#timeouts GoogleContainerNodePool#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleContainerNodePoolTimeouts"], result)

    @builtins.property
    def upgrade_settings(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolUpgradeSettings"]:
        '''upgrade_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#upgrade_settings GoogleContainerNodePool#upgrade_settings}
        '''
        result = self._values.get("upgrade_settings")
        return typing.cast(typing.Optional["GoogleContainerNodePoolUpgradeSettings"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The Kubernetes version for the nodes in this pool.

        Note that if this field and auto_upgrade are both specified, they will fight each other for what the node version should be, so setting both is highly discouraged. While a fuzzy version can be specified, it's recommended that you specify explicit versions as Terraform will see spurious diffs when fuzzy versions are used. See the google_container_engine_versions data source's version_prefix field to approximate fuzzy versions in a Terraform-compatible way.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#version GoogleContainerNodePool#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolManagement",
    jsii_struct_bases=[],
    name_mapping={"auto_repair": "autoRepair", "auto_upgrade": "autoUpgrade"},
)
class GoogleContainerNodePoolManagement:
    def __init__(
        self,
        *,
        auto_repair: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_upgrade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param auto_repair: Whether the nodes will be automatically repaired. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#auto_repair GoogleContainerNodePool#auto_repair}
        :param auto_upgrade: Whether the nodes will be automatically upgraded. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#auto_upgrade GoogleContainerNodePool#auto_upgrade}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf662b569af6c32395030e1a62cb8531d6641c45b30b92fe348b218de7658497)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#auto_repair GoogleContainerNodePool#auto_repair}
        '''
        result = self._values.get("auto_repair")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auto_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the nodes will be automatically upgraded. Enabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#auto_upgrade GoogleContainerNodePool#auto_upgrade}
        '''
        result = self._values.get("auto_upgrade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolManagement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolManagementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolManagementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aab11aa58f47591b5a7f082a3b5abeddb63a02a365fb84966dc36fd6654a8299)
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
            type_hints = typing.get_type_hints(_typecheckingstub__435f8fabeac9592a57908302f97e6e5268f60ac9d6b2be5802a49cbb3debed1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29fb9077729ae66d34d07b367bdea13e3cf79db36d53a7e0cacac9fb3106dc18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoUpgrade", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleContainerNodePoolManagement]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolManagement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolManagement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ed1eb8fc1eb08adaf661424db47ad79f9030d9dcb8d9e913a3c3c6f7d8f41ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNetworkConfig",
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
class GoogleContainerNodePoolNetworkConfig:
    def __init__(
        self,
        *,
        additional_node_network_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        additional_pod_network_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        create_pod_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_private_nodes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network_performance_config: typing.Optional[typing.Union["GoogleContainerNodePoolNetworkConfigNetworkPerformanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        pod_cidr_overprovision_config: typing.Optional[typing.Union["GoogleContainerNodePoolNetworkConfigPodCidrOverprovisionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        pod_ipv4_cidr_block: typing.Optional[builtins.str] = None,
        pod_range: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param additional_node_network_configs: additional_node_network_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#additional_node_network_configs GoogleContainerNodePool#additional_node_network_configs}
        :param additional_pod_network_configs: additional_pod_network_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#additional_pod_network_configs GoogleContainerNodePool#additional_pod_network_configs}
        :param create_pod_range: Whether to create a new range for pod IPs in this node pool. Defaults are provided for pod_range and pod_ipv4_cidr_block if they are not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#create_pod_range GoogleContainerNodePool#create_pod_range}
        :param enable_private_nodes: Whether nodes have internal IP addresses only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enable_private_nodes GoogleContainerNodePool#enable_private_nodes}
        :param network_performance_config: network_performance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#network_performance_config GoogleContainerNodePool#network_performance_config}
        :param pod_cidr_overprovision_config: pod_cidr_overprovision_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#pod_cidr_overprovision_config GoogleContainerNodePool#pod_cidr_overprovision_config}
        :param pod_ipv4_cidr_block: The IP address range for pod IPs in this node pool. Only applicable if create_pod_range is true. Set to blank to have a range chosen with the default size. Set to /netmask (e.g. /14) to have a range chosen with a specific netmask. Set to a CIDR notation (e.g. 10.96.0.0/14) to pick a specific range to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#pod_ipv4_cidr_block GoogleContainerNodePool#pod_ipv4_cidr_block}
        :param pod_range: The ID of the secondary range for pod IPs. If create_pod_range is true, this ID is used for the new range. If create_pod_range is false, uses an existing secondary range with this ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#pod_range GoogleContainerNodePool#pod_range}
        '''
        if isinstance(network_performance_config, dict):
            network_performance_config = GoogleContainerNodePoolNetworkConfigNetworkPerformanceConfig(**network_performance_config)
        if isinstance(pod_cidr_overprovision_config, dict):
            pod_cidr_overprovision_config = GoogleContainerNodePoolNetworkConfigPodCidrOverprovisionConfig(**pod_cidr_overprovision_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eed8a5d314ec03f5556cab7d069325b6923f0374080c64eb741ae1245cb45d5c)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs"]]]:
        '''additional_node_network_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#additional_node_network_configs GoogleContainerNodePool#additional_node_network_configs}
        '''
        result = self._values.get("additional_node_network_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs"]]], result)

    @builtins.property
    def additional_pod_network_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs"]]]:
        '''additional_pod_network_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#additional_pod_network_configs GoogleContainerNodePool#additional_pod_network_configs}
        '''
        result = self._values.get("additional_pod_network_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs"]]], result)

    @builtins.property
    def create_pod_range(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to create a new range for pod IPs in this node pool.

        Defaults are provided for pod_range and pod_ipv4_cidr_block if they are not specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#create_pod_range GoogleContainerNodePool#create_pod_range}
        '''
        result = self._values.get("create_pod_range")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_private_nodes(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether nodes have internal IP addresses only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enable_private_nodes GoogleContainerNodePool#enable_private_nodes}
        '''
        result = self._values.get("enable_private_nodes")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def network_performance_config(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNetworkConfigNetworkPerformanceConfig"]:
        '''network_performance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#network_performance_config GoogleContainerNodePool#network_performance_config}
        '''
        result = self._values.get("network_performance_config")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNetworkConfigNetworkPerformanceConfig"], result)

    @builtins.property
    def pod_cidr_overprovision_config(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNetworkConfigPodCidrOverprovisionConfig"]:
        '''pod_cidr_overprovision_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#pod_cidr_overprovision_config GoogleContainerNodePool#pod_cidr_overprovision_config}
        '''
        result = self._values.get("pod_cidr_overprovision_config")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNetworkConfigPodCidrOverprovisionConfig"], result)

    @builtins.property
    def pod_ipv4_cidr_block(self) -> typing.Optional[builtins.str]:
        '''The IP address range for pod IPs in this node pool.

        Only applicable if create_pod_range is true. Set to blank to have a range chosen with the default size. Set to /netmask (e.g. /14) to have a range chosen with a specific netmask. Set to a CIDR notation (e.g. 10.96.0.0/14) to pick a specific range to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#pod_ipv4_cidr_block GoogleContainerNodePool#pod_ipv4_cidr_block}
        '''
        result = self._values.get("pod_ipv4_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pod_range(self) -> typing.Optional[builtins.str]:
        '''The ID of the secondary range for pod IPs.

        If create_pod_range is true, this ID is used for the new range. If create_pod_range is false, uses an existing secondary range with this ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#pod_range GoogleContainerNodePool#pod_range}
        '''
        result = self._values.get("pod_range")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs",
    jsii_struct_bases=[],
    name_mapping={"network": "network", "subnetwork": "subnetwork"},
)
class GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs:
    def __init__(
        self,
        *,
        network: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param network: Name of the VPC where the additional interface belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#network GoogleContainerNodePool#network}
        :param subnetwork: Name of the subnetwork where the additional interface belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#subnetwork GoogleContainerNodePool#subnetwork}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69280f8038f3e51e8decfab988090ac457fee0010e5ebcbbefb7ec971036ec49)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#network GoogleContainerNodePool#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''Name of the subnetwork where the additional interface belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#subnetwork GoogleContainerNodePool#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9dbc237978655fa73187db4c1cb53cf298beb2cbf6d7de91566d61fd5021b55a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b43caea3e720458e059950f10eac719b65add90902dc0ef411694e1df0d37717)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a89c9167545d9848968422ddca3f5f5009f1224574f3c61e3c483a2154e0117a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e732e0faf6b3be5d6434d2ed758a6e053056b7b25eee45e80a78aad15c93f25c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__33525485b76a39aa69c71a59b0a47d8a3225b0cce8d02f8abbab18890cf62650)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3377d650a18991b89da7c1ee629727d221ad09505b7afd80d03e1cea238ef07a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a9864bc7eec4a09677a2ceb13bd9c9845d85639e8e9b75680a064c839385930)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec88a8cef2d916cc004abe9ba36fc7d4637c58e514b1a2bc507a70ecea239794)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e05364612cc35e1ba10065efd1a780aca91de26ac5703a656669ad7f4c8c2d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc237594c9f9c114117d4938da7ae5f55339f7a7a14bc8fed2d2b7ccd78de11e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "max_pods_per_node": "maxPodsPerNode",
        "secondary_pod_range": "secondaryPodRange",
        "subnetwork": "subnetwork",
    },
)
class GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs:
    def __init__(
        self,
        *,
        max_pods_per_node: typing.Optional[jsii.Number] = None,
        secondary_pod_range: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_pods_per_node: The maximum number of pods per node which use this pod network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#max_pods_per_node GoogleContainerNodePool#max_pods_per_node}
        :param secondary_pod_range: The name of the secondary range on the subnet which provides IP address for this pod range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#secondary_pod_range GoogleContainerNodePool#secondary_pod_range}
        :param subnetwork: Name of the subnetwork where the additional pod network belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#subnetwork GoogleContainerNodePool#subnetwork}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5593fb845ba5f92e05b5d61ad48e08e12cd9b918b57291b657cfbbfc32adbdb5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#max_pods_per_node GoogleContainerNodePool#max_pods_per_node}
        '''
        result = self._values.get("max_pods_per_node")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secondary_pod_range(self) -> typing.Optional[builtins.str]:
        '''The name of the secondary range on the subnet which provides IP address for this pod range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#secondary_pod_range GoogleContainerNodePool#secondary_pod_range}
        '''
        result = self._values.get("secondary_pod_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''Name of the subnetwork where the additional pod network belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#subnetwork GoogleContainerNodePool#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d30b87effd0d5902f3da770b8cd355d32f87a62810aba8600231fbcf7456bb52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be776c3e43cadf916675c7c3c6794e69282987e9bdad6cde62b9fd115c0c85e7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33d13f00757dd726e5258748ec17b0c5e7d827926d21a17a192ee24a639084fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e57a5cf3f32bfef5c73918ecdf6d15914a041422914896f605c993e379547a91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3e2e443223bdb40d4096074806552500ef79c31eb7a957a0ec18e511b7a4802)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__700f3178af7167db355d009359e4445edbe6fa284127ce9b3ea62cdbe30ad863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4ab55a5e7f7e4d8967218001377ebf143102e568244c569cf3da883e008332b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68485f3f826542f88d5fe8f219e2ba1ac59b06832d839b7dca15d036ac4cef55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPodsPerNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secondaryPodRange")
    def secondary_pod_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryPodRange"))

    @secondary_pod_range.setter
    def secondary_pod_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a63badd02d3fa89586d1a7cd8e1a70f7f6071a665a32990e03dc847eba08d349)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryPodRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c61703f7b2adf52e48366edc87fa29da1ea177fe23a1b1aa566ec7f268fa5468)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce0581388cd88fcaa86e8cc85e21009cb53454163502c68b4c71aec5084a3b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNetworkConfigNetworkPerformanceConfig",
    jsii_struct_bases=[],
    name_mapping={"total_egress_bandwidth_tier": "totalEgressBandwidthTier"},
)
class GoogleContainerNodePoolNetworkConfigNetworkPerformanceConfig:
    def __init__(self, *, total_egress_bandwidth_tier: builtins.str) -> None:
        '''
        :param total_egress_bandwidth_tier: Specifies the total network bandwidth tier for the NodePool. `Valid values <https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters.nodePools#NodePool.Tier>`_ include: "TIER_1" and "TIER_UNSPECIFIED". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#total_egress_bandwidth_tier GoogleContainerNodePool#total_egress_bandwidth_tier}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45fa85b320937fd850dad502f53a6152a77ffeaa5054e33350415b99ae55f6c1)
            check_type(argname="argument total_egress_bandwidth_tier", value=total_egress_bandwidth_tier, expected_type=type_hints["total_egress_bandwidth_tier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "total_egress_bandwidth_tier": total_egress_bandwidth_tier,
        }

    @builtins.property
    def total_egress_bandwidth_tier(self) -> builtins.str:
        '''Specifies the total network bandwidth tier for the NodePool. `Valid values <https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters.nodePools#NodePool.Tier>`_ include: "TIER_1" and "TIER_UNSPECIFIED".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#total_egress_bandwidth_tier GoogleContainerNodePool#total_egress_bandwidth_tier}
        '''
        result = self._values.get("total_egress_bandwidth_tier")
        assert result is not None, "Required property 'total_egress_bandwidth_tier' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNetworkConfigNetworkPerformanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNetworkConfigNetworkPerformanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNetworkConfigNetworkPerformanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e70e06fa6bf8f3116f05b8ec596f09ef579afc5909cd75076b475f3b8414f4b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40b936c3ed15c3bb7876b8dd090cc4076e7fa252e989e019e57cd4f5d35f2fa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "totalEgressBandwidthTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNetworkConfigNetworkPerformanceConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNetworkConfigNetworkPerformanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNetworkConfigNetworkPerformanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55ffa9eeca72d8ff6f31e6e98f605fc5462980acbc7f199d24432f294c963cd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerNodePoolNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86ab47c099914e4d193e3ce84817fba39f48f162ab5d644a8f692b1135d4eb49)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdditionalNodeNetworkConfigs")
    def put_additional_node_network_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d420e8ad7ee17de5d595c8f83097687c3611ebc66a78ed7578bdbbc367b92616)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalNodeNetworkConfigs", [value]))

    @jsii.member(jsii_name="putAdditionalPodNetworkConfigs")
    def put_additional_pod_network_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e3b1f27f5b41acdf70c95a775856332922d21efab06465f122bae94d8033670)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalPodNetworkConfigs", [value]))

    @jsii.member(jsii_name="putNetworkPerformanceConfig")
    def put_network_performance_config(
        self,
        *,
        total_egress_bandwidth_tier: builtins.str,
    ) -> None:
        '''
        :param total_egress_bandwidth_tier: Specifies the total network bandwidth tier for the NodePool. `Valid values <https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters.nodePools#NodePool.Tier>`_ include: "TIER_1" and "TIER_UNSPECIFIED". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#total_egress_bandwidth_tier GoogleContainerNodePool#total_egress_bandwidth_tier}
        '''
        value = GoogleContainerNodePoolNetworkConfigNetworkPerformanceConfig(
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
        :param disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#disabled GoogleContainerNodePool#disabled}.
        '''
        value = GoogleContainerNodePoolNetworkConfigPodCidrOverprovisionConfig(
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
    ) -> GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigsList:
        return typing.cast(GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigsList, jsii.get(self, "additionalNodeNetworkConfigs"))

    @builtins.property
    @jsii.member(jsii_name="additionalPodNetworkConfigs")
    def additional_pod_network_configs(
        self,
    ) -> GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigsList:
        return typing.cast(GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigsList, jsii.get(self, "additionalPodNetworkConfigs"))

    @builtins.property
    @jsii.member(jsii_name="networkPerformanceConfig")
    def network_performance_config(
        self,
    ) -> GoogleContainerNodePoolNetworkConfigNetworkPerformanceConfigOutputReference:
        return typing.cast(GoogleContainerNodePoolNetworkConfigNetworkPerformanceConfigOutputReference, jsii.get(self, "networkPerformanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="podCidrOverprovisionConfig")
    def pod_cidr_overprovision_config(
        self,
    ) -> "GoogleContainerNodePoolNetworkConfigPodCidrOverprovisionConfigOutputReference":
        return typing.cast("GoogleContainerNodePoolNetworkConfigPodCidrOverprovisionConfigOutputReference", jsii.get(self, "podCidrOverprovisionConfig"))

    @builtins.property
    @jsii.member(jsii_name="additionalNodeNetworkConfigsInput")
    def additional_node_network_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs]]], jsii.get(self, "additionalNodeNetworkConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalPodNetworkConfigsInput")
    def additional_pod_network_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs]]], jsii.get(self, "additionalPodNetworkConfigsInput"))

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
    ) -> typing.Optional[GoogleContainerNodePoolNetworkConfigNetworkPerformanceConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNetworkConfigNetworkPerformanceConfig], jsii.get(self, "networkPerformanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="podCidrOverprovisionConfigInput")
    def pod_cidr_overprovision_config_input(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNetworkConfigPodCidrOverprovisionConfig"]:
        return typing.cast(typing.Optional["GoogleContainerNodePoolNetworkConfigPodCidrOverprovisionConfig"], jsii.get(self, "podCidrOverprovisionConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1508f8ee2ce08b8323c5176b5638d953797d29df6548da0cf78e3e321de31b46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14a0cfca3262e83c0e154372d222247345ed04f4c2e2266f03b60acefaba6d3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePrivateNodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="podIpv4CidrBlock")
    def pod_ipv4_cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "podIpv4CidrBlock"))

    @pod_ipv4_cidr_block.setter
    def pod_ipv4_cidr_block(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7579b112e2f8956c9323cbde9c6225ba942280f541f9a94cf18adf7083cce62d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podIpv4CidrBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="podRange")
    def pod_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "podRange"))

    @pod_range.setter
    def pod_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8bd9618d182a54a7314488aeda425a360a6040213e325fab75b28b3562ce8bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleContainerNodePoolNetworkConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dede1c406015eb91bc1ef6b774a5c323f0705bb993708882c958e72423c6e2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNetworkConfigPodCidrOverprovisionConfig",
    jsii_struct_bases=[],
    name_mapping={"disabled": "disabled"},
)
class GoogleContainerNodePoolNetworkConfigPodCidrOverprovisionConfig:
    def __init__(
        self,
        *,
        disabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#disabled GoogleContainerNodePool#disabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e36914cd390f1683b1de7950c1106aca4c170f1b24808fedc3448a1615cd2ac)
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disabled": disabled,
        }

    @builtins.property
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#disabled GoogleContainerNodePool#disabled}.'''
        result = self._values.get("disabled")
        assert result is not None, "Required property 'disabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNetworkConfigPodCidrOverprovisionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNetworkConfigPodCidrOverprovisionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNetworkConfigPodCidrOverprovisionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d9ec034c869ca44025d8c6cb9c37e33f9f1ece8bfa4ac9cf5b0028576c5445a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__808f43410d2749934f7749b30fbe673b324b5e7d0c2668ec9055c888c41ef148)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNetworkConfigPodCidrOverprovisionConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNetworkConfigPodCidrOverprovisionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNetworkConfigPodCidrOverprovisionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c394a27920b53dd332d5a0ee1f7b8beee652a57f2f6accd4e88ed27204817b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfig",
    jsii_struct_bases=[],
    name_mapping={
        "advanced_machine_features": "advancedMachineFeatures",
        "boot_disk_kms_key": "bootDiskKmsKey",
        "confidential_nodes": "confidentialNodes",
        "containerd_config": "containerdConfig",
        "disk_size_gb": "diskSizeGb",
        "disk_type": "diskType",
        "enable_confidential_storage": "enableConfidentialStorage",
        "ephemeral_storage_config": "ephemeralStorageConfig",
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
        "sandbox_config": "sandboxConfig",
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
class GoogleContainerNodePoolNodeConfig:
    def __init__(
        self,
        *,
        advanced_machine_features: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigAdvancedMachineFeatures", typing.Dict[builtins.str, typing.Any]]] = None,
        boot_disk_kms_key: typing.Optional[builtins.str] = None,
        confidential_nodes: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigConfidentialNodes", typing.Dict[builtins.str, typing.Any]]] = None,
        containerd_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigContainerdConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        disk_type: typing.Optional[builtins.str] = None,
        enable_confidential_storage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ephemeral_storage_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigEphemeralStorageConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ephemeral_storage_local_ssd_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        fast_socket: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigFastSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        flex_start: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcfs_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigGcfsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        guest_accelerator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerNodePoolNodeConfigGuestAccelerator", typing.Dict[builtins.str, typing.Any]]]]] = None,
        gvnic: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigGvnic", typing.Dict[builtins.str, typing.Any]]] = None,
        host_maintenance_policy: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigHostMaintenancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        image_type: typing.Optional[builtins.str] = None,
        kubelet_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigKubeletConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        linux_node_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigLinuxNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        local_nvme_ssd_block_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig", typing.Dict[builtins.str, typing.Any]]] = None,
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
        reservation_affinity: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigReservationAffinity", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        sandbox_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigSandboxConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        secondary_boot_disks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerNodePoolNodeConfigSecondaryBootDisks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_account: typing.Optional[builtins.str] = None,
        shielded_instance_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        sole_tenant_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigSoleTenantConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        storage_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        taint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerNodePoolNodeConfigTaint", typing.Dict[builtins.str, typing.Any]]]]] = None,
        windows_node_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigWindowsNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        workload_metadata_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigWorkloadMetadataConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_machine_features: advanced_machine_features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#advanced_machine_features GoogleContainerNodePool#advanced_machine_features}
        :param boot_disk_kms_key: The Customer Managed Encryption Key used to encrypt the boot disk attached to each node in the node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#boot_disk_kms_key GoogleContainerNodePool#boot_disk_kms_key}
        :param confidential_nodes: confidential_nodes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#confidential_nodes GoogleContainerNodePool#confidential_nodes}
        :param containerd_config: containerd_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#containerd_config GoogleContainerNodePool#containerd_config}
        :param disk_size_gb: Size of the disk attached to each node, specified in GB. The smallest allowed disk size is 10GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#disk_size_gb GoogleContainerNodePool#disk_size_gb}
        :param disk_type: Type of the disk attached to each node. Such as pd-standard, pd-balanced or pd-ssd. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#disk_type GoogleContainerNodePool#disk_type}
        :param enable_confidential_storage: If enabled boot disks are configured with confidential mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enable_confidential_storage GoogleContainerNodePool#enable_confidential_storage}
        :param ephemeral_storage_config: ephemeral_storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#ephemeral_storage_config GoogleContainerNodePool#ephemeral_storage_config}
        :param ephemeral_storage_local_ssd_config: ephemeral_storage_local_ssd_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#ephemeral_storage_local_ssd_config GoogleContainerNodePool#ephemeral_storage_local_ssd_config}
        :param fast_socket: fast_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#fast_socket GoogleContainerNodePool#fast_socket}
        :param flex_start: Enables Flex Start provisioning model for the node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#flex_start GoogleContainerNodePool#flex_start}
        :param gcfs_config: gcfs_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#gcfs_config GoogleContainerNodePool#gcfs_config}
        :param guest_accelerator: guest_accelerator block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#guest_accelerator GoogleContainerNodePool#guest_accelerator}
        :param gvnic: gvnic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#gvnic GoogleContainerNodePool#gvnic}
        :param host_maintenance_policy: host_maintenance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#host_maintenance_policy GoogleContainerNodePool#host_maintenance_policy}
        :param image_type: The image type to use for this node. Note that for a given image type, the latest version of it will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#image_type GoogleContainerNodePool#image_type}
        :param kubelet_config: kubelet_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#kubelet_config GoogleContainerNodePool#kubelet_config}
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#labels GoogleContainerNodePool#labels}
        :param linux_node_config: linux_node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#linux_node_config GoogleContainerNodePool#linux_node_config}
        :param local_nvme_ssd_block_config: local_nvme_ssd_block_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#local_nvme_ssd_block_config GoogleContainerNodePool#local_nvme_ssd_block_config}
        :param local_ssd_count: The number of local SSD disks to be attached to the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#local_ssd_count GoogleContainerNodePool#local_ssd_count}
        :param local_ssd_encryption_mode: LocalSsdEncryptionMode specified the method used for encrypting the local SSDs attached to the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#local_ssd_encryption_mode GoogleContainerNodePool#local_ssd_encryption_mode}
        :param logging_variant: Type of logging agent that is used as the default value for node pools in the cluster. Valid values include DEFAULT and MAX_THROUGHPUT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#logging_variant GoogleContainerNodePool#logging_variant}
        :param machine_type: The name of a Google Compute Engine machine type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#machine_type GoogleContainerNodePool#machine_type}
        :param max_run_duration: The runtime of each node in the node pool in seconds, terminated by 's'. Example: "3600s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#max_run_duration GoogleContainerNodePool#max_run_duration}
        :param metadata: The metadata key/value pairs assigned to instances in the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#metadata GoogleContainerNodePool#metadata}
        :param min_cpu_platform: Minimum CPU platform to be used by this instance. The instance may be scheduled on the specified or newer CPU platform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#min_cpu_platform GoogleContainerNodePool#min_cpu_platform}
        :param node_group: Setting this field will assign instances of this pool to run on the specified node group. This is useful for running workloads on sole tenant nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#node_group GoogleContainerNodePool#node_group}
        :param oauth_scopes: The set of Google API scopes to be made available on all of the node VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#oauth_scopes GoogleContainerNodePool#oauth_scopes}
        :param preemptible: Whether the nodes are created as preemptible VM instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#preemptible GoogleContainerNodePool#preemptible}
        :param reservation_affinity: reservation_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#reservation_affinity GoogleContainerNodePool#reservation_affinity}
        :param resource_labels: The GCE resource labels (a map of key/value pairs) to be applied to the node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#resource_labels GoogleContainerNodePool#resource_labels}
        :param resource_manager_tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#resource_manager_tags GoogleContainerNodePool#resource_manager_tags}
        :param sandbox_config: sandbox_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#sandbox_config GoogleContainerNodePool#sandbox_config}
        :param secondary_boot_disks: secondary_boot_disks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#secondary_boot_disks GoogleContainerNodePool#secondary_boot_disks}
        :param service_account: The Google Cloud Platform Service Account to be used by the node VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#service_account GoogleContainerNodePool#service_account}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#shielded_instance_config GoogleContainerNodePool#shielded_instance_config}
        :param sole_tenant_config: sole_tenant_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#sole_tenant_config GoogleContainerNodePool#sole_tenant_config}
        :param spot: Whether the nodes are created as spot VM instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#spot GoogleContainerNodePool#spot}
        :param storage_pools: The list of Storage Pools where boot disks are provisioned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#storage_pools GoogleContainerNodePool#storage_pools}
        :param tags: The list of instance tags applied to all nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#tags GoogleContainerNodePool#tags}
        :param taint: taint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#taint GoogleContainerNodePool#taint}
        :param windows_node_config: windows_node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#windows_node_config GoogleContainerNodePool#windows_node_config}
        :param workload_metadata_config: workload_metadata_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#workload_metadata_config GoogleContainerNodePool#workload_metadata_config}
        '''
        if isinstance(advanced_machine_features, dict):
            advanced_machine_features = GoogleContainerNodePoolNodeConfigAdvancedMachineFeatures(**advanced_machine_features)
        if isinstance(confidential_nodes, dict):
            confidential_nodes = GoogleContainerNodePoolNodeConfigConfidentialNodes(**confidential_nodes)
        if isinstance(containerd_config, dict):
            containerd_config = GoogleContainerNodePoolNodeConfigContainerdConfig(**containerd_config)
        if isinstance(ephemeral_storage_config, dict):
            ephemeral_storage_config = GoogleContainerNodePoolNodeConfigEphemeralStorageConfig(**ephemeral_storage_config)
        if isinstance(ephemeral_storage_local_ssd_config, dict):
            ephemeral_storage_local_ssd_config = GoogleContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig(**ephemeral_storage_local_ssd_config)
        if isinstance(fast_socket, dict):
            fast_socket = GoogleContainerNodePoolNodeConfigFastSocket(**fast_socket)
        if isinstance(gcfs_config, dict):
            gcfs_config = GoogleContainerNodePoolNodeConfigGcfsConfig(**gcfs_config)
        if isinstance(gvnic, dict):
            gvnic = GoogleContainerNodePoolNodeConfigGvnic(**gvnic)
        if isinstance(host_maintenance_policy, dict):
            host_maintenance_policy = GoogleContainerNodePoolNodeConfigHostMaintenancePolicy(**host_maintenance_policy)
        if isinstance(kubelet_config, dict):
            kubelet_config = GoogleContainerNodePoolNodeConfigKubeletConfig(**kubelet_config)
        if isinstance(linux_node_config, dict):
            linux_node_config = GoogleContainerNodePoolNodeConfigLinuxNodeConfig(**linux_node_config)
        if isinstance(local_nvme_ssd_block_config, dict):
            local_nvme_ssd_block_config = GoogleContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig(**local_nvme_ssd_block_config)
        if isinstance(reservation_affinity, dict):
            reservation_affinity = GoogleContainerNodePoolNodeConfigReservationAffinity(**reservation_affinity)
        if isinstance(sandbox_config, dict):
            sandbox_config = GoogleContainerNodePoolNodeConfigSandboxConfig(**sandbox_config)
        if isinstance(shielded_instance_config, dict):
            shielded_instance_config = GoogleContainerNodePoolNodeConfigShieldedInstanceConfig(**shielded_instance_config)
        if isinstance(sole_tenant_config, dict):
            sole_tenant_config = GoogleContainerNodePoolNodeConfigSoleTenantConfig(**sole_tenant_config)
        if isinstance(windows_node_config, dict):
            windows_node_config = GoogleContainerNodePoolNodeConfigWindowsNodeConfig(**windows_node_config)
        if isinstance(workload_metadata_config, dict):
            workload_metadata_config = GoogleContainerNodePoolNodeConfigWorkloadMetadataConfig(**workload_metadata_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa1fcd02cbce130e12742899615c9eba8ee7c5fbe33fdb8aaf3b5ba306a4073c)
            check_type(argname="argument advanced_machine_features", value=advanced_machine_features, expected_type=type_hints["advanced_machine_features"])
            check_type(argname="argument boot_disk_kms_key", value=boot_disk_kms_key, expected_type=type_hints["boot_disk_kms_key"])
            check_type(argname="argument confidential_nodes", value=confidential_nodes, expected_type=type_hints["confidential_nodes"])
            check_type(argname="argument containerd_config", value=containerd_config, expected_type=type_hints["containerd_config"])
            check_type(argname="argument disk_size_gb", value=disk_size_gb, expected_type=type_hints["disk_size_gb"])
            check_type(argname="argument disk_type", value=disk_type, expected_type=type_hints["disk_type"])
            check_type(argname="argument enable_confidential_storage", value=enable_confidential_storage, expected_type=type_hints["enable_confidential_storage"])
            check_type(argname="argument ephemeral_storage_config", value=ephemeral_storage_config, expected_type=type_hints["ephemeral_storage_config"])
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
            check_type(argname="argument sandbox_config", value=sandbox_config, expected_type=type_hints["sandbox_config"])
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
        if ephemeral_storage_config is not None:
            self._values["ephemeral_storage_config"] = ephemeral_storage_config
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
        if sandbox_config is not None:
            self._values["sandbox_config"] = sandbox_config
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
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigAdvancedMachineFeatures"]:
        '''advanced_machine_features block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#advanced_machine_features GoogleContainerNodePool#advanced_machine_features}
        '''
        result = self._values.get("advanced_machine_features")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigAdvancedMachineFeatures"], result)

    @builtins.property
    def boot_disk_kms_key(self) -> typing.Optional[builtins.str]:
        '''The Customer Managed Encryption Key used to encrypt the boot disk attached to each node in the node pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#boot_disk_kms_key GoogleContainerNodePool#boot_disk_kms_key}
        '''
        result = self._values.get("boot_disk_kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def confidential_nodes(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigConfidentialNodes"]:
        '''confidential_nodes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#confidential_nodes GoogleContainerNodePool#confidential_nodes}
        '''
        result = self._values.get("confidential_nodes")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigConfidentialNodes"], result)

    @builtins.property
    def containerd_config(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigContainerdConfig"]:
        '''containerd_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#containerd_config GoogleContainerNodePool#containerd_config}
        '''
        result = self._values.get("containerd_config")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigContainerdConfig"], result)

    @builtins.property
    def disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Size of the disk attached to each node, specified in GB. The smallest allowed disk size is 10GB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#disk_size_gb GoogleContainerNodePool#disk_size_gb}
        '''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_type(self) -> typing.Optional[builtins.str]:
        '''Type of the disk attached to each node. Such as pd-standard, pd-balanced or pd-ssd.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#disk_type GoogleContainerNodePool#disk_type}
        '''
        result = self._values.get("disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_confidential_storage(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If enabled boot disks are configured with confidential mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enable_confidential_storage GoogleContainerNodePool#enable_confidential_storage}
        '''
        result = self._values.get("enable_confidential_storage")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ephemeral_storage_config(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigEphemeralStorageConfig"]:
        '''ephemeral_storage_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#ephemeral_storage_config GoogleContainerNodePool#ephemeral_storage_config}
        '''
        result = self._values.get("ephemeral_storage_config")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigEphemeralStorageConfig"], result)

    @builtins.property
    def ephemeral_storage_local_ssd_config(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig"]:
        '''ephemeral_storage_local_ssd_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#ephemeral_storage_local_ssd_config GoogleContainerNodePool#ephemeral_storage_local_ssd_config}
        '''
        result = self._values.get("ephemeral_storage_local_ssd_config")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig"], result)

    @builtins.property
    def fast_socket(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigFastSocket"]:
        '''fast_socket block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#fast_socket GoogleContainerNodePool#fast_socket}
        '''
        result = self._values.get("fast_socket")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigFastSocket"], result)

    @builtins.property
    def flex_start(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables Flex Start provisioning model for the node pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#flex_start GoogleContainerNodePool#flex_start}
        '''
        result = self._values.get("flex_start")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcfs_config(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigGcfsConfig"]:
        '''gcfs_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#gcfs_config GoogleContainerNodePool#gcfs_config}
        '''
        result = self._values.get("gcfs_config")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigGcfsConfig"], result)

    @builtins.property
    def guest_accelerator(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerNodePoolNodeConfigGuestAccelerator"]]]:
        '''guest_accelerator block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#guest_accelerator GoogleContainerNodePool#guest_accelerator}
        '''
        result = self._values.get("guest_accelerator")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerNodePoolNodeConfigGuestAccelerator"]]], result)

    @builtins.property
    def gvnic(self) -> typing.Optional["GoogleContainerNodePoolNodeConfigGvnic"]:
        '''gvnic block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#gvnic GoogleContainerNodePool#gvnic}
        '''
        result = self._values.get("gvnic")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigGvnic"], result)

    @builtins.property
    def host_maintenance_policy(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigHostMaintenancePolicy"]:
        '''host_maintenance_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#host_maintenance_policy GoogleContainerNodePool#host_maintenance_policy}
        '''
        result = self._values.get("host_maintenance_policy")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigHostMaintenancePolicy"], result)

    @builtins.property
    def image_type(self) -> typing.Optional[builtins.str]:
        '''The image type to use for this node.

        Note that for a given image type, the latest version of it will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#image_type GoogleContainerNodePool#image_type}
        '''
        result = self._values.get("image_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kubelet_config(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigKubeletConfig"]:
        '''kubelet_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#kubelet_config GoogleContainerNodePool#kubelet_config}
        '''
        result = self._values.get("kubelet_config")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigKubeletConfig"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The map of Kubernetes labels (key/value pairs) to be applied to each node.

        These will added in addition to any default label(s) that Kubernetes may apply to the node.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#labels GoogleContainerNodePool#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def linux_node_config(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigLinuxNodeConfig"]:
        '''linux_node_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#linux_node_config GoogleContainerNodePool#linux_node_config}
        '''
        result = self._values.get("linux_node_config")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigLinuxNodeConfig"], result)

    @builtins.property
    def local_nvme_ssd_block_config(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig"]:
        '''local_nvme_ssd_block_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#local_nvme_ssd_block_config GoogleContainerNodePool#local_nvme_ssd_block_config}
        '''
        result = self._values.get("local_nvme_ssd_block_config")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig"], result)

    @builtins.property
    def local_ssd_count(self) -> typing.Optional[jsii.Number]:
        '''The number of local SSD disks to be attached to the node.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#local_ssd_count GoogleContainerNodePool#local_ssd_count}
        '''
        result = self._values.get("local_ssd_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def local_ssd_encryption_mode(self) -> typing.Optional[builtins.str]:
        '''LocalSsdEncryptionMode specified the method used for encrypting the local SSDs attached to the node.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#local_ssd_encryption_mode GoogleContainerNodePool#local_ssd_encryption_mode}
        '''
        result = self._values.get("local_ssd_encryption_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_variant(self) -> typing.Optional[builtins.str]:
        '''Type of logging agent that is used as the default value for node pools in the cluster.

        Valid values include DEFAULT and MAX_THROUGHPUT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#logging_variant GoogleContainerNodePool#logging_variant}
        '''
        result = self._values.get("logging_variant")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The name of a Google Compute Engine machine type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#machine_type GoogleContainerNodePool#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_run_duration(self) -> typing.Optional[builtins.str]:
        '''The runtime of each node in the node pool in seconds, terminated by 's'. Example: "3600s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#max_run_duration GoogleContainerNodePool#max_run_duration}
        '''
        result = self._values.get("max_run_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The metadata key/value pairs assigned to instances in the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#metadata GoogleContainerNodePool#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def min_cpu_platform(self) -> typing.Optional[builtins.str]:
        '''Minimum CPU platform to be used by this instance.

        The instance may be scheduled on the specified or newer CPU platform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#min_cpu_platform GoogleContainerNodePool#min_cpu_platform}
        '''
        result = self._values.get("min_cpu_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_group(self) -> typing.Optional[builtins.str]:
        '''Setting this field will assign instances of this pool to run on the specified node group.

        This is useful for running workloads on sole tenant nodes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#node_group GoogleContainerNodePool#node_group}
        '''
        result = self._values.get("node_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of Google API scopes to be made available on all of the node VMs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#oauth_scopes GoogleContainerNodePool#oauth_scopes}
        '''
        result = self._values.get("oauth_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def preemptible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the nodes are created as preemptible VM instances.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#preemptible GoogleContainerNodePool#preemptible}
        '''
        result = self._values.get("preemptible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def reservation_affinity(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigReservationAffinity"]:
        '''reservation_affinity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#reservation_affinity GoogleContainerNodePool#reservation_affinity}
        '''
        result = self._values.get("reservation_affinity")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigReservationAffinity"], result)

    @builtins.property
    def resource_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The GCE resource labels (a map of key/value pairs) to be applied to the node pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#resource_labels GoogleContainerNodePool#resource_labels}
        '''
        result = self._values.get("resource_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def resource_manager_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of resource manager tags.

        Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#resource_manager_tags GoogleContainerNodePool#resource_manager_tags}
        '''
        result = self._values.get("resource_manager_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def sandbox_config(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigSandboxConfig"]:
        '''sandbox_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#sandbox_config GoogleContainerNodePool#sandbox_config}
        '''
        result = self._values.get("sandbox_config")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigSandboxConfig"], result)

    @builtins.property
    def secondary_boot_disks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerNodePoolNodeConfigSecondaryBootDisks"]]]:
        '''secondary_boot_disks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#secondary_boot_disks GoogleContainerNodePool#secondary_boot_disks}
        '''
        result = self._values.get("secondary_boot_disks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerNodePoolNodeConfigSecondaryBootDisks"]]], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''The Google Cloud Platform Service Account to be used by the node VMs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#service_account GoogleContainerNodePool#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shielded_instance_config(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigShieldedInstanceConfig"]:
        '''shielded_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#shielded_instance_config GoogleContainerNodePool#shielded_instance_config}
        '''
        result = self._values.get("shielded_instance_config")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigShieldedInstanceConfig"], result)

    @builtins.property
    def sole_tenant_config(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigSoleTenantConfig"]:
        '''sole_tenant_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#sole_tenant_config GoogleContainerNodePool#sole_tenant_config}
        '''
        result = self._values.get("sole_tenant_config")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigSoleTenantConfig"], result)

    @builtins.property
    def spot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the nodes are created as spot VM instances.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#spot GoogleContainerNodePool#spot}
        '''
        result = self._values.get("spot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def storage_pools(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of Storage Pools where boot disks are provisioned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#storage_pools GoogleContainerNodePool#storage_pools}
        '''
        result = self._values.get("storage_pools")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of instance tags applied to all nodes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#tags GoogleContainerNodePool#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def taint(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerNodePoolNodeConfigTaint"]]]:
        '''taint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#taint GoogleContainerNodePool#taint}
        '''
        result = self._values.get("taint")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerNodePoolNodeConfigTaint"]]], result)

    @builtins.property
    def windows_node_config(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigWindowsNodeConfig"]:
        '''windows_node_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#windows_node_config GoogleContainerNodePool#windows_node_config}
        '''
        result = self._values.get("windows_node_config")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigWindowsNodeConfig"], result)

    @builtins.property
    def workload_metadata_config(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigWorkloadMetadataConfig"]:
        '''workload_metadata_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#workload_metadata_config GoogleContainerNodePool#workload_metadata_config}
        '''
        result = self._values.get("workload_metadata_config")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigWorkloadMetadataConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigAdvancedMachineFeatures",
    jsii_struct_bases=[],
    name_mapping={
        "threads_per_core": "threadsPerCore",
        "enable_nested_virtualization": "enableNestedVirtualization",
    },
)
class GoogleContainerNodePoolNodeConfigAdvancedMachineFeatures:
    def __init__(
        self,
        *,
        threads_per_core: jsii.Number,
        enable_nested_virtualization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param threads_per_core: The number of threads per physical core. To disable simultaneous multithreading (SMT) set this to 1. If unset, the maximum number of threads supported per core by the underlying processor is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#threads_per_core GoogleContainerNodePool#threads_per_core}
        :param enable_nested_virtualization: Whether the node should have nested virtualization enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enable_nested_virtualization GoogleContainerNodePool#enable_nested_virtualization}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b84ff91dc1576bbc9fd54614b903df3470b664e8a73f1347af0ad77800bc5135)
            check_type(argname="argument threads_per_core", value=threads_per_core, expected_type=type_hints["threads_per_core"])
            check_type(argname="argument enable_nested_virtualization", value=enable_nested_virtualization, expected_type=type_hints["enable_nested_virtualization"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threads_per_core": threads_per_core,
        }
        if enable_nested_virtualization is not None:
            self._values["enable_nested_virtualization"] = enable_nested_virtualization

    @builtins.property
    def threads_per_core(self) -> jsii.Number:
        '''The number of threads per physical core.

        To disable simultaneous multithreading (SMT) set this to 1. If unset, the maximum number of threads supported per core by the underlying processor is assumed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#threads_per_core GoogleContainerNodePool#threads_per_core}
        '''
        result = self._values.get("threads_per_core")
        assert result is not None, "Required property 'threads_per_core' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def enable_nested_virtualization(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the node should have nested virtualization enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enable_nested_virtualization GoogleContainerNodePool#enable_nested_virtualization}
        '''
        result = self._values.get("enable_nested_virtualization")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigAdvancedMachineFeatures(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigAdvancedMachineFeaturesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigAdvancedMachineFeaturesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95636e02825a991f3f7147686878ebe9b25d0c3b188f89a60c85ccb4614c1853)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableNestedVirtualization")
    def reset_enable_nested_virtualization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableNestedVirtualization", []))

    @builtins.property
    @jsii.member(jsii_name="enableNestedVirtualizationInput")
    def enable_nested_virtualization_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableNestedVirtualizationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ca58f258a30281aa3abb57e3578ef76d20525330df9feb8cd537c6a1df05930e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableNestedVirtualization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threadsPerCore")
    def threads_per_core(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threadsPerCore"))

    @threads_per_core.setter
    def threads_per_core(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74676e8c91979e708130a472a888ecbae89c91d55b6e1369c462dbca994020a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threadsPerCore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigAdvancedMachineFeatures]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigAdvancedMachineFeatures], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigAdvancedMachineFeatures],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__889cd7e2fbed6269f4eca69f0e7c114ef45b06d265915c856e49d22849ceeecf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigConfidentialNodes",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleContainerNodePoolNodeConfigConfidentialNodes:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether Confidential Nodes feature is enabled for all nodes in this pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enabled GoogleContainerNodePool#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e772158230d40c8289e54ed2cf966b3b6ed2bd49b0788aea9c7898ab80c90c5)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether Confidential Nodes feature is enabled for all nodes in this pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enabled GoogleContainerNodePool#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigConfidentialNodes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigConfidentialNodesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigConfidentialNodesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e75312ab7191a22e2f0dae63aa9d8ed49065876708a96436bbb8f4d2e6e9daab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c98bf71a2c437d0181cf3ce3f859e06d5abb4ff0de4bcf9b1fb31db161b2d3bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigConfidentialNodes]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigConfidentialNodes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigConfidentialNodes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9339a3ce0d429e8193f318d4eb35a45025f57161b4a4cc2a64c1be4ae3dbeff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigContainerdConfig",
    jsii_struct_bases=[],
    name_mapping={"private_registry_access_config": "privateRegistryAccessConfig"},
)
class GoogleContainerNodePoolNodeConfigContainerdConfig:
    def __init__(
        self,
        *,
        private_registry_access_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param private_registry_access_config: private_registry_access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#private_registry_access_config GoogleContainerNodePool#private_registry_access_config}
        '''
        if isinstance(private_registry_access_config, dict):
            private_registry_access_config = GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig(**private_registry_access_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a43bebb0711ded537e3a7ede439858aa9cfee81c49de3d3a537163d5e1a94805)
            check_type(argname="argument private_registry_access_config", value=private_registry_access_config, expected_type=type_hints["private_registry_access_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if private_registry_access_config is not None:
            self._values["private_registry_access_config"] = private_registry_access_config

    @builtins.property
    def private_registry_access_config(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig"]:
        '''private_registry_access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#private_registry_access_config GoogleContainerNodePool#private_registry_access_config}
        '''
        result = self._values.get("private_registry_access_config")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigContainerdConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigContainerdConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigContainerdConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff8c6628f23731394b34903c900df9763bfc699b672d555ab7cc1e105d6a315a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPrivateRegistryAccessConfig")
    def put_private_registry_access_config(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        certificate_authority_domain_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Whether or not private registries are configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enabled GoogleContainerNodePool#enabled}
        :param certificate_authority_domain_config: certificate_authority_domain_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#certificate_authority_domain_config GoogleContainerNodePool#certificate_authority_domain_config}
        '''
        value = GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig(
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
    ) -> "GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigOutputReference":
        return typing.cast("GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigOutputReference", jsii.get(self, "privateRegistryAccessConfig"))

    @builtins.property
    @jsii.member(jsii_name="privateRegistryAccessConfigInput")
    def private_registry_access_config_input(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig"]:
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig"], jsii.get(self, "privateRegistryAccessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigContainerdConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigContainerdConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigContainerdConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9937b64dcde67eefae955c9acdc2935752a7923e32842dd9e7836320e85dd798)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "certificate_authority_domain_config": "certificateAuthorityDomainConfig",
    },
)
class GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        certificate_authority_domain_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Whether or not private registries are configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enabled GoogleContainerNodePool#enabled}
        :param certificate_authority_domain_config: certificate_authority_domain_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#certificate_authority_domain_config GoogleContainerNodePool#certificate_authority_domain_config}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a974befeb0377290bc4c276ed50036d9ebcfd6641d02653a1cb5fd1d6178a6f9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enabled GoogleContainerNodePool#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def certificate_authority_domain_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig"]]]:
        '''certificate_authority_domain_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#certificate_authority_domain_config GoogleContainerNodePool#certificate_authority_domain_config}
        '''
        result = self._values.get("certificate_authority_domain_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig",
    jsii_struct_bases=[],
    name_mapping={
        "fqdns": "fqdns",
        "gcp_secret_manager_certificate_config": "gcpSecretManagerCertificateConfig",
    },
)
class GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig:
    def __init__(
        self,
        *,
        fqdns: typing.Sequence[builtins.str],
        gcp_secret_manager_certificate_config: typing.Union["GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param fqdns: List of fully-qualified-domain-names. IPv4s and port specification are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#fqdns GoogleContainerNodePool#fqdns}
        :param gcp_secret_manager_certificate_config: gcp_secret_manager_certificate_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#gcp_secret_manager_certificate_config GoogleContainerNodePool#gcp_secret_manager_certificate_config}
        '''
        if isinstance(gcp_secret_manager_certificate_config, dict):
            gcp_secret_manager_certificate_config = GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig(**gcp_secret_manager_certificate_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ec4f0c3a07dc34da3cb7aa590b600000f24baa12387a982cb48f20e92787fc9)
            check_type(argname="argument fqdns", value=fqdns, expected_type=type_hints["fqdns"])
            check_type(argname="argument gcp_secret_manager_certificate_config", value=gcp_secret_manager_certificate_config, expected_type=type_hints["gcp_secret_manager_certificate_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fqdns": fqdns,
            "gcp_secret_manager_certificate_config": gcp_secret_manager_certificate_config,
        }

    @builtins.property
    def fqdns(self) -> typing.List[builtins.str]:
        '''List of fully-qualified-domain-names. IPv4s and port specification are supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#fqdns GoogleContainerNodePool#fqdns}
        '''
        result = self._values.get("fqdns")
        assert result is not None, "Required property 'fqdns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def gcp_secret_manager_certificate_config(
        self,
    ) -> "GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig":
        '''gcp_secret_manager_certificate_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#gcp_secret_manager_certificate_config GoogleContainerNodePool#gcp_secret_manager_certificate_config}
        '''
        result = self._values.get("gcp_secret_manager_certificate_config")
        assert result is not None, "Required property 'gcp_secret_manager_certificate_config' is missing"
        return typing.cast("GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig",
    jsii_struct_bases=[],
    name_mapping={"secret_uri": "secretUri"},
)
class GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig:
    def __init__(self, *, secret_uri: builtins.str) -> None:
        '''
        :param secret_uri: URI for the secret that hosts a certificate. Must be in the format 'projects/PROJECT_NUM/secrets/SECRET_NAME/versions/VERSION_OR_LATEST'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#secret_uri GoogleContainerNodePool#secret_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__466e4701426262db50e8ff5bbeb6f359e66e66becb055f1f2bca2ca47bd1dd48)
            check_type(argname="argument secret_uri", value=secret_uri, expected_type=type_hints["secret_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_uri": secret_uri,
        }

    @builtins.property
    def secret_uri(self) -> builtins.str:
        '''URI for the secret that hosts a certificate. Must be in the format 'projects/PROJECT_NUM/secrets/SECRET_NAME/versions/VERSION_OR_LATEST'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#secret_uri GoogleContainerNodePool#secret_uri}
        '''
        result = self._values.get("secret_uri")
        assert result is not None, "Required property 'secret_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c16d71637a85eb2fe9ec4bb2832e01946cd19bc59bad975c9ba10a99e9dd3aaf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f914fd5274a8b60713b0c5859ce1e5dff13e79050fca30d439f9222ac0fc3eaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac111ab21bb21914f6119325dd15aa3200ab844e824d32e714f9a350da43b1b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84e1c921d36aaf4c46e9515491c6f765825d743be1d465031b7d12b5a7f521db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0242325c6782f508a29a8abee63feaf4a5727b3058662d5cec8850766e18e70)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3727e3034bb9bd85399e5fb42671139147214642d1a60a2f4b5608c3b8b764b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfacb15e926de2e37528cc45d92ffa78d11173a4d8bb2e03bd2299d80d41f9e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7a938e5fb4749aa774aa2c25e18272ba61c91de2fa275db34f5319d3a256ea6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d791b795701d46eb922a38285e9caa5295ee90fcf4f160dd4946fa26777ac62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__972bcb668c0f1a391b2196a8c21d57fab429c6ffc20bf2017bf61bd6a92a3dd9)
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
        :param secret_uri: URI for the secret that hosts a certificate. Must be in the format 'projects/PROJECT_NUM/secrets/SECRET_NAME/versions/VERSION_OR_LATEST'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#secret_uri GoogleContainerNodePool#secret_uri}
        '''
        value = GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig(
            secret_uri=secret_uri
        )

        return typing.cast(None, jsii.invoke(self, "putGcpSecretManagerCertificateConfig", [value]))

    @builtins.property
    @jsii.member(jsii_name="gcpSecretManagerCertificateConfig")
    def gcp_secret_manager_certificate_config(
        self,
    ) -> GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfigOutputReference:
        return typing.cast(GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfigOutputReference, jsii.get(self, "gcpSecretManagerCertificateConfig"))

    @builtins.property
    @jsii.member(jsii_name="fqdnsInput")
    def fqdns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "fqdnsInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpSecretManagerCertificateConfigInput")
    def gcp_secret_manager_certificate_config_input(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig], jsii.get(self, "gcpSecretManagerCertificateConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fqdns")
    def fqdns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fqdns"))

    @fqdns.setter
    def fqdns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0be6fc9fe6bb048809b597a9523d273463ff528cc0f2b13c369aad8ead3d9ea3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fqdns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__756f64b72271cd969187273600a5b04f43756bd6fe059e2efa6386443aa5ac2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b421de9f82bce237ad088da2751981978a8d54b02e52b7ebe8358a4f6b16051)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCertificateAuthorityDomainConfig")
    def put_certificate_authority_domain_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63fbd198b2ba3669ec42f7e098e7efe8596383a68938cdc75aa30daac98cf6ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCertificateAuthorityDomainConfig", [value]))

    @jsii.member(jsii_name="resetCertificateAuthorityDomainConfig")
    def reset_certificate_authority_domain_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateAuthorityDomainConfig", []))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityDomainConfig")
    def certificate_authority_domain_config(
        self,
    ) -> GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigList:
        return typing.cast(GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigList, jsii.get(self, "certificateAuthorityDomainConfig"))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityDomainConfigInput")
    def certificate_authority_domain_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig]]], jsii.get(self, "certificateAuthorityDomainConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__716843f2c42276bc40b79b33613227a1ed7a370e24379e7f775c4600d3e0d14c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__340b4b3379685fbba5a62e879ecb2adb460b5296e2b6168e053269967718d910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigEffectiveTaints",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleContainerNodePoolNodeConfigEffectiveTaints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigEffectiveTaints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigEffectiveTaintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigEffectiveTaintsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aae321d3edcb049a5eef6207aecab51f9d77932da92a7420d8b3d5472c29af5c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleContainerNodePoolNodeConfigEffectiveTaintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d761a908436f3791ed08607f2b1c4e34f4428bee7012d8142e910884c8eefc0d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleContainerNodePoolNodeConfigEffectiveTaintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12044e40aa7a5cb7b4d7438cfdd039d17d26533c766d68638923550f6df5835f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23d360dbd5278ccc717212f7b58dd2f3c56e5905a56e37121c86cc015c736f83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__020f4fd06c54d6b3007a007011d2d7ec58cc9cd1f9dd028756096bcda31da8aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleContainerNodePoolNodeConfigEffectiveTaintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigEffectiveTaintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09a08cc90ffb4cddd61b06caa0d9f8d3fd52fa75a66d6749838d7831ae04be16)
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
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigEffectiveTaints]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigEffectiveTaints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigEffectiveTaints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c3dc61f11a88c4780b3b01acae8e5921a09ac9889ee15d0d3793d4b6c8dedf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigEphemeralStorageConfig",
    jsii_struct_bases=[],
    name_mapping={"local_ssd_count": "localSsdCount"},
)
class GoogleContainerNodePoolNodeConfigEphemeralStorageConfig:
    def __init__(self, *, local_ssd_count: jsii.Number) -> None:
        '''
        :param local_ssd_count: Number of local SSDs to use to back ephemeral storage. Uses NVMe interfaces. Each local SSD must be 375 or 3000 GB in size, and all local SSDs must share the same size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#local_ssd_count GoogleContainerNodePool#local_ssd_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e4de41b3a5eeca70b8a075b44132986bb2842de83e958f57914380eef48945d)
            check_type(argname="argument local_ssd_count", value=local_ssd_count, expected_type=type_hints["local_ssd_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "local_ssd_count": local_ssd_count,
        }

    @builtins.property
    def local_ssd_count(self) -> jsii.Number:
        '''Number of local SSDs to use to back ephemeral storage.

        Uses NVMe interfaces. Each local SSD must be 375 or 3000 GB in size, and all local SSDs must share the same size.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#local_ssd_count GoogleContainerNodePool#local_ssd_count}
        '''
        result = self._values.get("local_ssd_count")
        assert result is not None, "Required property 'local_ssd_count' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigEphemeralStorageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigEphemeralStorageConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigEphemeralStorageConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__344c60f8b220c63426f707c185c087ba749eed3c7c69515f211bddf3ef036e85)
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
            type_hints = typing.get_type_hints(_typecheckingstub__019b87e238833b05dc5c8fdac2040bebafbf42a3608f08329418747f6eb82e8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localSsdCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigEphemeralStorageConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigEphemeralStorageConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigEphemeralStorageConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6b4cfd6ade39b17c0cc0b5cd8ea7c183a365615a792af8a143710e1d207dfe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig",
    jsii_struct_bases=[],
    name_mapping={
        "local_ssd_count": "localSsdCount",
        "data_cache_count": "dataCacheCount",
    },
)
class GoogleContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig:
    def __init__(
        self,
        *,
        local_ssd_count: jsii.Number,
        data_cache_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param local_ssd_count: Number of local SSDs to use to back ephemeral storage. Uses NVMe interfaces. Each local SSD must be 375 or 3000 GB in size, and all local SSDs must share the same size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#local_ssd_count GoogleContainerNodePool#local_ssd_count}
        :param data_cache_count: Number of local SSDs to be utilized for GKE Data Cache. Uses NVMe interfaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#data_cache_count GoogleContainerNodePool#data_cache_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16f86c06e6e0824c95b22931800efe52d61eb7a619796f9ab47acacaefd1e8ad)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#local_ssd_count GoogleContainerNodePool#local_ssd_count}
        '''
        result = self._values.get("local_ssd_count")
        assert result is not None, "Required property 'local_ssd_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def data_cache_count(self) -> typing.Optional[jsii.Number]:
        '''Number of local SSDs to be utilized for GKE Data Cache. Uses NVMe interfaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#data_cache_count GoogleContainerNodePool#data_cache_count}
        '''
        result = self._values.get("data_cache_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c361a910c4fe586ff79b5e408ab5d99f937b3fc0a7eea74a353a81482e3b257)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ee53ced7c9d38407f3caf403b92c30c542ed4c0f89d766f281d8b32fd98f1a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataCacheCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localSsdCount")
    def local_ssd_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "localSsdCount"))

    @local_ssd_count.setter
    def local_ssd_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de62d4e33dc77e39b64c35b46020212d50e856c27edb4ba24487711d0c823d2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localSsdCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__766060da06bc707692bfb4f199f52c714ac03d1943bd05bdd4e6cd2e49956ed4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigFastSocket",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleContainerNodePoolNodeConfigFastSocket:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether or not NCCL Fast Socket is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enabled GoogleContainerNodePool#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09299d5aca2f4ea2902b5fe7e75bf014ca9c6326a178e4659f8aec0478a7918b)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether or not NCCL Fast Socket is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enabled GoogleContainerNodePool#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigFastSocket(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigFastSocketOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigFastSocketOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcc6af57a173f3f7b49718b1c45a17069e2365faf88351ff610bd53ebaa071a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6eeed41022c11a8abceb7919564ba6510edc2e726952303b1dafe6399016f577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigFastSocket]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigFastSocket], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigFastSocket],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f99f21a5402d0a5f02efe77ee3b1826f95ac2cd4c35dda7f1c3943ed327d005)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigGcfsConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleContainerNodePoolNodeConfigGcfsConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether or not GCFS is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enabled GoogleContainerNodePool#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1b709504c119dee33ef8ff6ab54d0395563750ab640de101fb3ead0f8d935e9)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether or not GCFS is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enabled GoogleContainerNodePool#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigGcfsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigGcfsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigGcfsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e48fa4e7df987f256ed87baef93dc10b06d7f67979a84d114596e6e99b251c37)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da39bf9303463707f2509086f4cb45679818c58710b7099c3d8405facb33cf03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigGcfsConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigGcfsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigGcfsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20727639c6efea9f563e4281e2802bbc316b01bd4f3541a4b0e1bf5537eecf2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigGuestAccelerator",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "type": "type",
        "gpu_driver_installation_config": "gpuDriverInstallationConfig",
        "gpu_partition_size": "gpuPartitionSize",
        "gpu_sharing_config": "gpuSharingConfig",
    },
)
class GoogleContainerNodePoolNodeConfigGuestAccelerator:
    def __init__(
        self,
        *,
        count: jsii.Number,
        type: builtins.str,
        gpu_driver_installation_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        gpu_partition_size: typing.Optional[builtins.str] = None,
        gpu_sharing_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param count: The number of the accelerator cards exposed to an instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#count GoogleContainerNodePool#count}
        :param type: The accelerator type resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#type GoogleContainerNodePool#type}
        :param gpu_driver_installation_config: gpu_driver_installation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#gpu_driver_installation_config GoogleContainerNodePool#gpu_driver_installation_config}
        :param gpu_partition_size: Size of partitions to create on the GPU. Valid values are described in the NVIDIA mig user guide (https://docs.nvidia.com/datacenter/tesla/mig-user-guide/#partitioning). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#gpu_partition_size GoogleContainerNodePool#gpu_partition_size}
        :param gpu_sharing_config: gpu_sharing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#gpu_sharing_config GoogleContainerNodePool#gpu_sharing_config}
        '''
        if isinstance(gpu_driver_installation_config, dict):
            gpu_driver_installation_config = GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig(**gpu_driver_installation_config)
        if isinstance(gpu_sharing_config, dict):
            gpu_sharing_config = GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig(**gpu_sharing_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5371a78d3348f7984f3252a3b413a231d4d0d94d0af67d13539e315d1941f3ce)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#count GoogleContainerNodePool#count}
        '''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The accelerator type resource name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#type GoogleContainerNodePool#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gpu_driver_installation_config(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig"]:
        '''gpu_driver_installation_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#gpu_driver_installation_config GoogleContainerNodePool#gpu_driver_installation_config}
        '''
        result = self._values.get("gpu_driver_installation_config")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig"], result)

    @builtins.property
    def gpu_partition_size(self) -> typing.Optional[builtins.str]:
        '''Size of partitions to create on the GPU. Valid values are described in the NVIDIA mig user guide (https://docs.nvidia.com/datacenter/tesla/mig-user-guide/#partitioning).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#gpu_partition_size GoogleContainerNodePool#gpu_partition_size}
        '''
        result = self._values.get("gpu_partition_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gpu_sharing_config(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig"]:
        '''gpu_sharing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#gpu_sharing_config GoogleContainerNodePool#gpu_sharing_config}
        '''
        result = self._values.get("gpu_sharing_config")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigGuestAccelerator(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig",
    jsii_struct_bases=[],
    name_mapping={"gpu_driver_version": "gpuDriverVersion"},
)
class GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig:
    def __init__(self, *, gpu_driver_version: builtins.str) -> None:
        '''
        :param gpu_driver_version: Mode for how the GPU driver is installed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#gpu_driver_version GoogleContainerNodePool#gpu_driver_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6da24334c663dd4353d24e2d2007f40b0552c1cdf3681de6d4ec103127ea6090)
            check_type(argname="argument gpu_driver_version", value=gpu_driver_version, expected_type=type_hints["gpu_driver_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gpu_driver_version": gpu_driver_version,
        }

    @builtins.property
    def gpu_driver_version(self) -> builtins.str:
        '''Mode for how the GPU driver is installed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#gpu_driver_version GoogleContainerNodePool#gpu_driver_version}
        '''
        result = self._values.get("gpu_driver_version")
        assert result is not None, "Required property 'gpu_driver_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f8651bd3cd1d2d27d20eeb3a0efa9312d870a92c6f67213efba17d51d027947)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6c467a966c9248fbf3973067980f92085df54d653eeb05eb6fe8f1f2890d56c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpuDriverVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__553888b672e1fc75c764972108f7f8f43cc4337a0939d958ebfa82c8f188512a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "gpu_sharing_strategy": "gpuSharingStrategy",
        "max_shared_clients_per_gpu": "maxSharedClientsPerGpu",
    },
)
class GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig:
    def __init__(
        self,
        *,
        gpu_sharing_strategy: builtins.str,
        max_shared_clients_per_gpu: jsii.Number,
    ) -> None:
        '''
        :param gpu_sharing_strategy: The type of GPU sharing strategy to enable on the GPU node. Possible values are described in the API package (https://pkg.go.dev/google.golang.org/api/container/v1#GPUSharingConfig) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#gpu_sharing_strategy GoogleContainerNodePool#gpu_sharing_strategy}
        :param max_shared_clients_per_gpu: The maximum number of containers that can share a GPU. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#max_shared_clients_per_gpu GoogleContainerNodePool#max_shared_clients_per_gpu}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__681761950d528de7826057d9ef1c2f105d6ede87838fa1e6c8a4d24479466885)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#gpu_sharing_strategy GoogleContainerNodePool#gpu_sharing_strategy}
        '''
        result = self._values.get("gpu_sharing_strategy")
        assert result is not None, "Required property 'gpu_sharing_strategy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_shared_clients_per_gpu(self) -> jsii.Number:
        '''The maximum number of containers that can share a GPU.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#max_shared_clients_per_gpu GoogleContainerNodePool#max_shared_clients_per_gpu}
        '''
        result = self._values.get("max_shared_clients_per_gpu")
        assert result is not None, "Required property 'max_shared_clients_per_gpu' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb760b365268447fe30cad3acfd57cf6c28dcb846a40eb7ee790c19e8a668024)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1db7dae7e97c577e68472b3506cb4ecb4c3d191569185d972803008ef790eb5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpuSharingStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxSharedClientsPerGpu")
    def max_shared_clients_per_gpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxSharedClientsPerGpu"))

    @max_shared_clients_per_gpu.setter
    def max_shared_clients_per_gpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cdef1c0518a7c9fdfde9088b5d7ddd782a3196c57ebb9fc8628a5711c824547)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSharedClientsPerGpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4b626e52af88754879d936808df10f9ce6fd33cb3fc20fc36b1f049bd8a27d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerNodePoolNodeConfigGuestAcceleratorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigGuestAcceleratorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd296edd6212e1afff0426f1b33eee419329d7f930e96bb23c33f053351f5ef9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleContainerNodePoolNodeConfigGuestAcceleratorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d6be7ca89367e72ecb1910247d2e24d9b35b970887843cecff78cd31831680)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleContainerNodePoolNodeConfigGuestAcceleratorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7ea263de560bb796241fbd1b0e58bf4605847182743e213dc72216ee43af68b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a0134108a27f693ae7d8fb8cddf87d44fa8bfd0714e153df56890d98d83eefe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b392f148eb02a59634e2119dbf341fd9b17c7098d58097200b4d2ec7150db008)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigGuestAccelerator]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigGuestAccelerator]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigGuestAccelerator]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6525e8399f8fa6ced47f29d699211eebeb5f8b114df9b7a05649df8c8ff2bc21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerNodePoolNodeConfigGuestAcceleratorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigGuestAcceleratorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce672a064851ab01a2bb45f73a5243a5686380cc0bff14f08e506404a46cfc7e)
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
        :param gpu_driver_version: Mode for how the GPU driver is installed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#gpu_driver_version GoogleContainerNodePool#gpu_driver_version}
        '''
        value = GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig(
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
        :param gpu_sharing_strategy: The type of GPU sharing strategy to enable on the GPU node. Possible values are described in the API package (https://pkg.go.dev/google.golang.org/api/container/v1#GPUSharingConfig) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#gpu_sharing_strategy GoogleContainerNodePool#gpu_sharing_strategy}
        :param max_shared_clients_per_gpu: The maximum number of containers that can share a GPU. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#max_shared_clients_per_gpu GoogleContainerNodePool#max_shared_clients_per_gpu}
        '''
        value = GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig(
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
    ) -> GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfigOutputReference:
        return typing.cast(GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfigOutputReference, jsii.get(self, "gpuDriverInstallationConfig"))

    @builtins.property
    @jsii.member(jsii_name="gpuSharingConfig")
    def gpu_sharing_config(
        self,
    ) -> GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfigOutputReference:
        return typing.cast(GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfigOutputReference, jsii.get(self, "gpuSharingConfig"))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="gpuDriverInstallationConfigInput")
    def gpu_driver_installation_config_input(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig], jsii.get(self, "gpuDriverInstallationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="gpuPartitionSizeInput")
    def gpu_partition_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gpuPartitionSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="gpuSharingConfigInput")
    def gpu_sharing_config_input(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig], jsii.get(self, "gpuSharingConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__11f02a0d59b4e0d4f71412b0fbe11b32913e0729875e3ceb3966acd60f13023d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpuPartitionSize")
    def gpu_partition_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gpuPartitionSize"))

    @gpu_partition_size.setter
    def gpu_partition_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b9ba13b7c6bc01e03cf3e8f07c920e343308d293a0fc5d618174d757c60175f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpuPartitionSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ec2dbd50590745f9d559e0e173dd0bc81d1b6c88a1c7d2e7e95018d4289df5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNodeConfigGuestAccelerator]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNodeConfigGuestAccelerator]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNodeConfigGuestAccelerator]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3250a4ba2d60a794d39355578b33a5271f4f826cb6e0d3a616c68298132b3013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigGvnic",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleContainerNodePoolNodeConfigGvnic:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether or not gvnic is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enabled GoogleContainerNodePool#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a784eba60afd6892f06ce6edd56de6874823ff2cd61e7ad7a3102dd310100cf2)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether or not gvnic is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enabled GoogleContainerNodePool#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigGvnic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigGvnicOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigGvnicOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a0d7ebc71ac66550adb434ded1f0aca8ddcb306ec0f62e42d97b842a24de60a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ca809342a91d202196945d7a5c097493b8a6e576ad3ec0a6b9fe3572f33b911)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleContainerNodePoolNodeConfigGvnic]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigGvnic], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigGvnic],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c85b741cbf8ae3ee9473ebbf2343cf8d2efa077678545556e8de91d7b4f628c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigHostMaintenancePolicy",
    jsii_struct_bases=[],
    name_mapping={"maintenance_interval": "maintenanceInterval"},
)
class GoogleContainerNodePoolNodeConfigHostMaintenancePolicy:
    def __init__(self, *, maintenance_interval: builtins.str) -> None:
        '''
        :param maintenance_interval: . Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#maintenance_interval GoogleContainerNodePool#maintenance_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fea261c59267508d57da1d60973390de92bfd8fa666b533e957db8798e003a8)
            check_type(argname="argument maintenance_interval", value=maintenance_interval, expected_type=type_hints["maintenance_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "maintenance_interval": maintenance_interval,
        }

    @builtins.property
    def maintenance_interval(self) -> builtins.str:
        '''.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#maintenance_interval GoogleContainerNodePool#maintenance_interval}
        '''
        result = self._values.get("maintenance_interval")
        assert result is not None, "Required property 'maintenance_interval' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigHostMaintenancePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigHostMaintenancePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigHostMaintenancePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e294b60cb695c1064a7b0dccaa42c55225ce9a4a3ca20f2b5bc81ce09ead58b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea0fdc56e1f35fa91e5526f32ae443f351182ace719ea7b30eb6d55b29947f60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigHostMaintenancePolicy]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigHostMaintenancePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigHostMaintenancePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e124a8bf2eedaf03e11fbdcc5941ef41edb97658beb9b724ba12258ff7f7ae5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigKubeletConfig",
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
class GoogleContainerNodePoolNodeConfigKubeletConfig:
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
        :param allowed_unsafe_sysctls: Defines a comma-separated allowlist of unsafe sysctls or sysctl patterns which can be set on the Pods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#allowed_unsafe_sysctls GoogleContainerNodePool#allowed_unsafe_sysctls}
        :param container_log_max_files: Defines the maximum number of container log files that can be present for a container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#container_log_max_files GoogleContainerNodePool#container_log_max_files}
        :param container_log_max_size: Defines the maximum size of the container log file before it is rotated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#container_log_max_size GoogleContainerNodePool#container_log_max_size}
        :param cpu_cfs_quota: Enable CPU CFS quota enforcement for containers that specify CPU limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#cpu_cfs_quota GoogleContainerNodePool#cpu_cfs_quota}
        :param cpu_cfs_quota_period: Set the CPU CFS quota period value 'cpu.cfs_period_us'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#cpu_cfs_quota_period GoogleContainerNodePool#cpu_cfs_quota_period}
        :param cpu_manager_policy: Control the CPU management policy on the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#cpu_manager_policy GoogleContainerNodePool#cpu_manager_policy}
        :param image_gc_high_threshold_percent: Defines the percent of disk usage after which image garbage collection is always run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#image_gc_high_threshold_percent GoogleContainerNodePool#image_gc_high_threshold_percent}
        :param image_gc_low_threshold_percent: Defines the percent of disk usage before which image garbage collection is never run. Lowest disk usage to garbage collect to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#image_gc_low_threshold_percent GoogleContainerNodePool#image_gc_low_threshold_percent}
        :param image_maximum_gc_age: Defines the maximum age an image can be unused before it is garbage collected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#image_maximum_gc_age GoogleContainerNodePool#image_maximum_gc_age}
        :param image_minimum_gc_age: Defines the minimum age for an unused image before it is garbage collected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#image_minimum_gc_age GoogleContainerNodePool#image_minimum_gc_age}
        :param insecure_kubelet_readonly_port_enabled: Controls whether the kubelet read-only port is enabled. It is strongly recommended to set this to ``FALSE``. Possible values: ``TRUE``, ``FALSE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#insecure_kubelet_readonly_port_enabled GoogleContainerNodePool#insecure_kubelet_readonly_port_enabled}
        :param pod_pids_limit: Controls the maximum number of processes allowed to run in a pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#pod_pids_limit GoogleContainerNodePool#pod_pids_limit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34db26051499479a18ff1e6dc64f594f6dcae2949fd17e7e3473c9b06d80726d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#allowed_unsafe_sysctls GoogleContainerNodePool#allowed_unsafe_sysctls}
        '''
        result = self._values.get("allowed_unsafe_sysctls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def container_log_max_files(self) -> typing.Optional[jsii.Number]:
        '''Defines the maximum number of container log files that can be present for a container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#container_log_max_files GoogleContainerNodePool#container_log_max_files}
        '''
        result = self._values.get("container_log_max_files")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def container_log_max_size(self) -> typing.Optional[builtins.str]:
        '''Defines the maximum size of the container log file before it is rotated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#container_log_max_size GoogleContainerNodePool#container_log_max_size}
        '''
        result = self._values.get("container_log_max_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_cfs_quota(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable CPU CFS quota enforcement for containers that specify CPU limits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#cpu_cfs_quota GoogleContainerNodePool#cpu_cfs_quota}
        '''
        result = self._values.get("cpu_cfs_quota")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cpu_cfs_quota_period(self) -> typing.Optional[builtins.str]:
        '''Set the CPU CFS quota period value 'cpu.cfs_period_us'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#cpu_cfs_quota_period GoogleContainerNodePool#cpu_cfs_quota_period}
        '''
        result = self._values.get("cpu_cfs_quota_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_manager_policy(self) -> typing.Optional[builtins.str]:
        '''Control the CPU management policy on the node.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#cpu_manager_policy GoogleContainerNodePool#cpu_manager_policy}
        '''
        result = self._values.get("cpu_manager_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_gc_high_threshold_percent(self) -> typing.Optional[jsii.Number]:
        '''Defines the percent of disk usage after which image garbage collection is always run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#image_gc_high_threshold_percent GoogleContainerNodePool#image_gc_high_threshold_percent}
        '''
        result = self._values.get("image_gc_high_threshold_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def image_gc_low_threshold_percent(self) -> typing.Optional[jsii.Number]:
        '''Defines the percent of disk usage before which image garbage collection is never run.

        Lowest disk usage to garbage collect to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#image_gc_low_threshold_percent GoogleContainerNodePool#image_gc_low_threshold_percent}
        '''
        result = self._values.get("image_gc_low_threshold_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def image_maximum_gc_age(self) -> typing.Optional[builtins.str]:
        '''Defines the maximum age an image can be unused before it is garbage collected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#image_maximum_gc_age GoogleContainerNodePool#image_maximum_gc_age}
        '''
        result = self._values.get("image_maximum_gc_age")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_minimum_gc_age(self) -> typing.Optional[builtins.str]:
        '''Defines the minimum age for an unused image before it is garbage collected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#image_minimum_gc_age GoogleContainerNodePool#image_minimum_gc_age}
        '''
        result = self._values.get("image_minimum_gc_age")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insecure_kubelet_readonly_port_enabled(self) -> typing.Optional[builtins.str]:
        '''Controls whether the kubelet read-only port is enabled.

        It is strongly recommended to set this to ``FALSE``. Possible values: ``TRUE``, ``FALSE``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#insecure_kubelet_readonly_port_enabled GoogleContainerNodePool#insecure_kubelet_readonly_port_enabled}
        '''
        result = self._values.get("insecure_kubelet_readonly_port_enabled")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pod_pids_limit(self) -> typing.Optional[jsii.Number]:
        '''Controls the maximum number of processes allowed to run in a pod.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#pod_pids_limit GoogleContainerNodePool#pod_pids_limit}
        '''
        result = self._values.get("pod_pids_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigKubeletConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigKubeletConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigKubeletConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6d0bf9edeb1c08edf2cfe8c2355ac0d7f0beb7abac47803138a966c6bb7be8c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01a166da2a964d885deb0c3f8bb6d4a9c0db4754de8b057d45da983ebb91a65b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedUnsafeSysctls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerLogMaxFiles")
    def container_log_max_files(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "containerLogMaxFiles"))

    @container_log_max_files.setter
    def container_log_max_files(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9edf9633ad8f6672d81a593b24d63bf1a5b6e94da47015b1f985507f966f9de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerLogMaxFiles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerLogMaxSize")
    def container_log_max_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerLogMaxSize"))

    @container_log_max_size.setter
    def container_log_max_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f87b5305f80f879412d270a3d8a977c71bad664f4dd503d70c6f3ece16ee216)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d6c6d46f20646f7da20479d097f77be95fd7ae9a5beb7af3e109cf2406eb758)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCfsQuota", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuCfsQuotaPeriod")
    def cpu_cfs_quota_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuCfsQuotaPeriod"))

    @cpu_cfs_quota_period.setter
    def cpu_cfs_quota_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0fa442bad972a2c29cb7b2e17328a1c0828f6a2fe63e66491143b4d5f6599df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCfsQuotaPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuManagerPolicy")
    def cpu_manager_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuManagerPolicy"))

    @cpu_manager_policy.setter
    def cpu_manager_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d56e058197a0ee50991ace50fac3578496896e48e24a819597e69b49bc730abe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuManagerPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageGcHighThresholdPercent")
    def image_gc_high_threshold_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "imageGcHighThresholdPercent"))

    @image_gc_high_threshold_percent.setter
    def image_gc_high_threshold_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b635a1655dd3c7f80454cad4fc7b140b72f7c08f9b28efa7d9db291e352f523)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageGcHighThresholdPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageGcLowThresholdPercent")
    def image_gc_low_threshold_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "imageGcLowThresholdPercent"))

    @image_gc_low_threshold_percent.setter
    def image_gc_low_threshold_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eb4b1689a8b33903f23bb9184a497b1d7541bed7cf33f027dc389fffab789c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageGcLowThresholdPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageMaximumGcAge")
    def image_maximum_gc_age(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageMaximumGcAge"))

    @image_maximum_gc_age.setter
    def image_maximum_gc_age(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__177beda3c6285c1952bf24787c45253e10f4f22cb47278be0c085e34192fd857)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageMaximumGcAge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageMinimumGcAge")
    def image_minimum_gc_age(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageMinimumGcAge"))

    @image_minimum_gc_age.setter
    def image_minimum_gc_age(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1c1668cde7b6dae6f95ff6ef5360f5e37dabd4b470ab7f1bde4091894d9c3ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageMinimumGcAge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="insecureKubeletReadonlyPortEnabled")
    def insecure_kubelet_readonly_port_enabled(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "insecureKubeletReadonlyPortEnabled"))

    @insecure_kubelet_readonly_port_enabled.setter
    def insecure_kubelet_readonly_port_enabled(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff613003539c9e2c8a5e980c0a69de5421ff3c1cd29e3c2a1706a9277a70b899)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecureKubeletReadonlyPortEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="podPidsLimit")
    def pod_pids_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "podPidsLimit"))

    @pod_pids_limit.setter
    def pod_pids_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07b7fc19584ec3afccf323cdbac7515a5e6fa1b908097cb4bf49316dfd0b080c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podPidsLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigKubeletConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigKubeletConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigKubeletConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d30880a0d548ca19268a3873ba14d341efcd3daa24050f2dd7826b406e5d0c89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigLinuxNodeConfig",
    jsii_struct_bases=[],
    name_mapping={
        "cgroup_mode": "cgroupMode",
        "hugepages_config": "hugepagesConfig",
        "sysctls": "sysctls",
    },
)
class GoogleContainerNodePoolNodeConfigLinuxNodeConfig:
    def __init__(
        self,
        *,
        cgroup_mode: typing.Optional[builtins.str] = None,
        hugepages_config: typing.Optional[typing.Union["GoogleContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        sysctls: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param cgroup_mode: cgroupMode specifies the cgroup mode to be used on the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#cgroup_mode GoogleContainerNodePool#cgroup_mode}
        :param hugepages_config: hugepages_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#hugepages_config GoogleContainerNodePool#hugepages_config}
        :param sysctls: The Linux kernel parameters to be applied to the nodes and all pods running on the nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#sysctls GoogleContainerNodePool#sysctls}
        '''
        if isinstance(hugepages_config, dict):
            hugepages_config = GoogleContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig(**hugepages_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a712ff524db4e52be373615e9bd7f1e34a126a9685238d1ef0a28b04661f4da)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#cgroup_mode GoogleContainerNodePool#cgroup_mode}
        '''
        result = self._values.get("cgroup_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hugepages_config(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig"]:
        '''hugepages_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#hugepages_config GoogleContainerNodePool#hugepages_config}
        '''
        result = self._values.get("hugepages_config")
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig"], result)

    @builtins.property
    def sysctls(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The Linux kernel parameters to be applied to the nodes and all pods running on the nodes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#sysctls GoogleContainerNodePool#sysctls}
        '''
        result = self._values.get("sysctls")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigLinuxNodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig",
    jsii_struct_bases=[],
    name_mapping={
        "hugepage_size1_g": "hugepageSize1G",
        "hugepage_size2_m": "hugepageSize2M",
    },
)
class GoogleContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig:
    def __init__(
        self,
        *,
        hugepage_size1_g: typing.Optional[jsii.Number] = None,
        hugepage_size2_m: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hugepage_size1_g: Amount of 1G hugepages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#hugepage_size_1g GoogleContainerNodePool#hugepage_size_1g}
        :param hugepage_size2_m: Amount of 2M hugepages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#hugepage_size_2m GoogleContainerNodePool#hugepage_size_2m}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__483ba27c4de3a3f4602022a1b9e1bd31df133a46b0d9df854d86c5e595b6b52f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#hugepage_size_1g GoogleContainerNodePool#hugepage_size_1g}
        '''
        result = self._values.get("hugepage_size1_g")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def hugepage_size2_m(self) -> typing.Optional[jsii.Number]:
        '''Amount of 2M hugepages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#hugepage_size_2m GoogleContainerNodePool#hugepage_size_2m}
        '''
        result = self._values.get("hugepage_size2_m")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9ebc305e946a049e1266fb530ae4c8e942e47aea6c4f5810d6637e2687bb24c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__673533f6bb61e6cff3ccc4fa1b5a6e9f7eeff345db656f7ec107bb60eac36671)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hugepageSize1G", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hugepageSize2M")
    def hugepage_size2_m(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hugepageSize2M"))

    @hugepage_size2_m.setter
    def hugepage_size2_m(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f67c2845221212d51b3383d0afd530ef4c62b77c27b14e4b7cae4bf17a318c0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hugepageSize2M", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__262a8af562c55c73b9387c010e46688deda86596d66b4da96be84756542b91ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerNodePoolNodeConfigLinuxNodeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigLinuxNodeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4478269cb6a32f3df965ffc117217f6f41204ca47b623cb874c6d5c106c2cfce)
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
        :param hugepage_size1_g: Amount of 1G hugepages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#hugepage_size_1g GoogleContainerNodePool#hugepage_size_1g}
        :param hugepage_size2_m: Amount of 2M hugepages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#hugepage_size_2m GoogleContainerNodePool#hugepage_size_2m}
        '''
        value = GoogleContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig(
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
    ) -> GoogleContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfigOutputReference:
        return typing.cast(GoogleContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfigOutputReference, jsii.get(self, "hugepagesConfig"))

    @builtins.property
    @jsii.member(jsii_name="cgroupModeInput")
    def cgroup_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cgroupModeInput"))

    @builtins.property
    @jsii.member(jsii_name="hugepagesConfigInput")
    def hugepages_config_input(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig], jsii.get(self, "hugepagesConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9fcfad400ccd7c53572778f369c6725e83bbe8f077b7adad29e0296ff96b6f83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cgroupMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sysctls")
    def sysctls(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "sysctls"))

    @sysctls.setter
    def sysctls(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9919da74f17a45705ac745cf25042d4fc5962c02aa38dfcd13375668fa424b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sysctls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigLinuxNodeConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigLinuxNodeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigLinuxNodeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a3daa46502f797d8e0408b364a42d8e8374bd42fd5bd93306d52f36c97d2bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig",
    jsii_struct_bases=[],
    name_mapping={"local_ssd_count": "localSsdCount"},
)
class GoogleContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig:
    def __init__(self, *, local_ssd_count: jsii.Number) -> None:
        '''
        :param local_ssd_count: Number of raw-block local NVMe SSD disks to be attached to the node. Each local SSD is 375 GB in size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#local_ssd_count GoogleContainerNodePool#local_ssd_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b66f8fbe3ccad3b2c26fce5e237aac42e3bc074d8f82d5e1f27974291c0e1e6)
            check_type(argname="argument local_ssd_count", value=local_ssd_count, expected_type=type_hints["local_ssd_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "local_ssd_count": local_ssd_count,
        }

    @builtins.property
    def local_ssd_count(self) -> jsii.Number:
        '''Number of raw-block local NVMe SSD disks to be attached to the node.

        Each local SSD is 375 GB in size.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#local_ssd_count GoogleContainerNodePool#local_ssd_count}
        '''
        result = self._values.get("local_ssd_count")
        assert result is not None, "Required property 'local_ssd_count' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigLocalNvmeSsdBlockConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigLocalNvmeSsdBlockConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4174179525e1718955c4632684e87241327af41738c23b2a82c322e4aa774425)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e2c25315c97caa3ba9207c9e1f197c9b0b356a05319ec7ba9e4d07461ab957d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localSsdCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__396b99327534902cb3bc9a74734f9e0988397785d403ef117fd30c83f23fefd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerNodePoolNodeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__083a2dc299fe6145c85bfe549560b3684f3c8c908254f492952cf089b05da164)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdvancedMachineFeatures")
    def put_advanced_machine_features(
        self,
        *,
        threads_per_core: jsii.Number,
        enable_nested_virtualization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param threads_per_core: The number of threads per physical core. To disable simultaneous multithreading (SMT) set this to 1. If unset, the maximum number of threads supported per core by the underlying processor is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#threads_per_core GoogleContainerNodePool#threads_per_core}
        :param enable_nested_virtualization: Whether the node should have nested virtualization enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enable_nested_virtualization GoogleContainerNodePool#enable_nested_virtualization}
        '''
        value = GoogleContainerNodePoolNodeConfigAdvancedMachineFeatures(
            threads_per_core=threads_per_core,
            enable_nested_virtualization=enable_nested_virtualization,
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedMachineFeatures", [value]))

    @jsii.member(jsii_name="putConfidentialNodes")
    def put_confidential_nodes(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether Confidential Nodes feature is enabled for all nodes in this pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enabled GoogleContainerNodePool#enabled}
        '''
        value = GoogleContainerNodePoolNodeConfigConfidentialNodes(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putConfidentialNodes", [value]))

    @jsii.member(jsii_name="putContainerdConfig")
    def put_containerd_config(
        self,
        *,
        private_registry_access_config: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param private_registry_access_config: private_registry_access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#private_registry_access_config GoogleContainerNodePool#private_registry_access_config}
        '''
        value = GoogleContainerNodePoolNodeConfigContainerdConfig(
            private_registry_access_config=private_registry_access_config
        )

        return typing.cast(None, jsii.invoke(self, "putContainerdConfig", [value]))

    @jsii.member(jsii_name="putEphemeralStorageConfig")
    def put_ephemeral_storage_config(self, *, local_ssd_count: jsii.Number) -> None:
        '''
        :param local_ssd_count: Number of local SSDs to use to back ephemeral storage. Uses NVMe interfaces. Each local SSD must be 375 or 3000 GB in size, and all local SSDs must share the same size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#local_ssd_count GoogleContainerNodePool#local_ssd_count}
        '''
        value = GoogleContainerNodePoolNodeConfigEphemeralStorageConfig(
            local_ssd_count=local_ssd_count
        )

        return typing.cast(None, jsii.invoke(self, "putEphemeralStorageConfig", [value]))

    @jsii.member(jsii_name="putEphemeralStorageLocalSsdConfig")
    def put_ephemeral_storage_local_ssd_config(
        self,
        *,
        local_ssd_count: jsii.Number,
        data_cache_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param local_ssd_count: Number of local SSDs to use to back ephemeral storage. Uses NVMe interfaces. Each local SSD must be 375 or 3000 GB in size, and all local SSDs must share the same size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#local_ssd_count GoogleContainerNodePool#local_ssd_count}
        :param data_cache_count: Number of local SSDs to be utilized for GKE Data Cache. Uses NVMe interfaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#data_cache_count GoogleContainerNodePool#data_cache_count}
        '''
        value = GoogleContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig(
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
        :param enabled: Whether or not NCCL Fast Socket is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enabled GoogleContainerNodePool#enabled}
        '''
        value = GoogleContainerNodePoolNodeConfigFastSocket(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putFastSocket", [value]))

    @jsii.member(jsii_name="putGcfsConfig")
    def put_gcfs_config(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether or not GCFS is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enabled GoogleContainerNodePool#enabled}
        '''
        value = GoogleContainerNodePoolNodeConfigGcfsConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putGcfsConfig", [value]))

    @jsii.member(jsii_name="putGuestAccelerator")
    def put_guest_accelerator(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerNodePoolNodeConfigGuestAccelerator, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__430914745b249e68eef82335fa5df4f1ec0f5c9c715cae42d0ef9564525c8856)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGuestAccelerator", [value]))

    @jsii.member(jsii_name="putGvnic")
    def put_gvnic(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether or not gvnic is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enabled GoogleContainerNodePool#enabled}
        '''
        value = GoogleContainerNodePoolNodeConfigGvnic(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putGvnic", [value]))

    @jsii.member(jsii_name="putHostMaintenancePolicy")
    def put_host_maintenance_policy(
        self,
        *,
        maintenance_interval: builtins.str,
    ) -> None:
        '''
        :param maintenance_interval: . Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#maintenance_interval GoogleContainerNodePool#maintenance_interval}
        '''
        value = GoogleContainerNodePoolNodeConfigHostMaintenancePolicy(
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
        :param allowed_unsafe_sysctls: Defines a comma-separated allowlist of unsafe sysctls or sysctl patterns which can be set on the Pods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#allowed_unsafe_sysctls GoogleContainerNodePool#allowed_unsafe_sysctls}
        :param container_log_max_files: Defines the maximum number of container log files that can be present for a container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#container_log_max_files GoogleContainerNodePool#container_log_max_files}
        :param container_log_max_size: Defines the maximum size of the container log file before it is rotated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#container_log_max_size GoogleContainerNodePool#container_log_max_size}
        :param cpu_cfs_quota: Enable CPU CFS quota enforcement for containers that specify CPU limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#cpu_cfs_quota GoogleContainerNodePool#cpu_cfs_quota}
        :param cpu_cfs_quota_period: Set the CPU CFS quota period value 'cpu.cfs_period_us'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#cpu_cfs_quota_period GoogleContainerNodePool#cpu_cfs_quota_period}
        :param cpu_manager_policy: Control the CPU management policy on the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#cpu_manager_policy GoogleContainerNodePool#cpu_manager_policy}
        :param image_gc_high_threshold_percent: Defines the percent of disk usage after which image garbage collection is always run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#image_gc_high_threshold_percent GoogleContainerNodePool#image_gc_high_threshold_percent}
        :param image_gc_low_threshold_percent: Defines the percent of disk usage before which image garbage collection is never run. Lowest disk usage to garbage collect to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#image_gc_low_threshold_percent GoogleContainerNodePool#image_gc_low_threshold_percent}
        :param image_maximum_gc_age: Defines the maximum age an image can be unused before it is garbage collected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#image_maximum_gc_age GoogleContainerNodePool#image_maximum_gc_age}
        :param image_minimum_gc_age: Defines the minimum age for an unused image before it is garbage collected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#image_minimum_gc_age GoogleContainerNodePool#image_minimum_gc_age}
        :param insecure_kubelet_readonly_port_enabled: Controls whether the kubelet read-only port is enabled. It is strongly recommended to set this to ``FALSE``. Possible values: ``TRUE``, ``FALSE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#insecure_kubelet_readonly_port_enabled GoogleContainerNodePool#insecure_kubelet_readonly_port_enabled}
        :param pod_pids_limit: Controls the maximum number of processes allowed to run in a pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#pod_pids_limit GoogleContainerNodePool#pod_pids_limit}
        '''
        value = GoogleContainerNodePoolNodeConfigKubeletConfig(
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
        hugepages_config: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        sysctls: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param cgroup_mode: cgroupMode specifies the cgroup mode to be used on the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#cgroup_mode GoogleContainerNodePool#cgroup_mode}
        :param hugepages_config: hugepages_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#hugepages_config GoogleContainerNodePool#hugepages_config}
        :param sysctls: The Linux kernel parameters to be applied to the nodes and all pods running on the nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#sysctls GoogleContainerNodePool#sysctls}
        '''
        value = GoogleContainerNodePoolNodeConfigLinuxNodeConfig(
            cgroup_mode=cgroup_mode, hugepages_config=hugepages_config, sysctls=sysctls
        )

        return typing.cast(None, jsii.invoke(self, "putLinuxNodeConfig", [value]))

    @jsii.member(jsii_name="putLocalNvmeSsdBlockConfig")
    def put_local_nvme_ssd_block_config(self, *, local_ssd_count: jsii.Number) -> None:
        '''
        :param local_ssd_count: Number of raw-block local NVMe SSD disks to be attached to the node. Each local SSD is 375 GB in size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#local_ssd_count GoogleContainerNodePool#local_ssd_count}
        '''
        value = GoogleContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig(
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
        :param consume_reservation_type: Corresponds to the type of reservation consumption. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#consume_reservation_type GoogleContainerNodePool#consume_reservation_type}
        :param key: The label key of a reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#key GoogleContainerNodePool#key}
        :param values: The label values of the reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#values GoogleContainerNodePool#values}
        '''
        value = GoogleContainerNodePoolNodeConfigReservationAffinity(
            consume_reservation_type=consume_reservation_type, key=key, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putReservationAffinity", [value]))

    @jsii.member(jsii_name="putSandboxConfig")
    def put_sandbox_config(self, *, sandbox_type: builtins.str) -> None:
        '''
        :param sandbox_type: Type of the sandbox to use for the node (e.g. 'gvisor'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#sandbox_type GoogleContainerNodePool#sandbox_type}
        '''
        value = GoogleContainerNodePoolNodeConfigSandboxConfig(
            sandbox_type=sandbox_type
        )

        return typing.cast(None, jsii.invoke(self, "putSandboxConfig", [value]))

    @jsii.member(jsii_name="putSecondaryBootDisks")
    def put_secondary_boot_disks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerNodePoolNodeConfigSecondaryBootDisks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__607b7584cce2a4e32ed18d742de21f4a5c502f3e1869442b45ee5a1ffeae3b36)
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
        :param enable_integrity_monitoring: Defines whether the instance has integrity monitoring enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enable_integrity_monitoring GoogleContainerNodePool#enable_integrity_monitoring}
        :param enable_secure_boot: Defines whether the instance has Secure Boot enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enable_secure_boot GoogleContainerNodePool#enable_secure_boot}
        '''
        value = GoogleContainerNodePoolNodeConfigShieldedInstanceConfig(
            enable_integrity_monitoring=enable_integrity_monitoring,
            enable_secure_boot=enable_secure_boot,
        )

        return typing.cast(None, jsii.invoke(self, "putShieldedInstanceConfig", [value]))

    @jsii.member(jsii_name="putSoleTenantConfig")
    def put_sole_tenant_config(
        self,
        *,
        node_affinity: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param node_affinity: node_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#node_affinity GoogleContainerNodePool#node_affinity}
        '''
        value = GoogleContainerNodePoolNodeConfigSoleTenantConfig(
            node_affinity=node_affinity
        )

        return typing.cast(None, jsii.invoke(self, "putSoleTenantConfig", [value]))

    @jsii.member(jsii_name="putTaint")
    def put_taint(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerNodePoolNodeConfigTaint", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fc7a8e8b61631a29f9319151abe11b15733da3854e6d474ad8a514e2097f3d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTaint", [value]))

    @jsii.member(jsii_name="putWindowsNodeConfig")
    def put_windows_node_config(
        self,
        *,
        osversion: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param osversion: The OS Version of the windows nodepool.Values are OS_VERSION_UNSPECIFIED,OS_VERSION_LTSC2019 and OS_VERSION_LTSC2022. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#osversion GoogleContainerNodePool#osversion}
        '''
        value = GoogleContainerNodePoolNodeConfigWindowsNodeConfig(osversion=osversion)

        return typing.cast(None, jsii.invoke(self, "putWindowsNodeConfig", [value]))

    @jsii.member(jsii_name="putWorkloadMetadataConfig")
    def put_workload_metadata_config(self, *, mode: builtins.str) -> None:
        '''
        :param mode: Mode is the configuration for how to expose metadata to workloads running on the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#mode GoogleContainerNodePool#mode}
        '''
        value = GoogleContainerNodePoolNodeConfigWorkloadMetadataConfig(mode=mode)

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

    @jsii.member(jsii_name="resetEphemeralStorageConfig")
    def reset_ephemeral_storage_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEphemeralStorageConfig", []))

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

    @jsii.member(jsii_name="resetSandboxConfig")
    def reset_sandbox_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSandboxConfig", []))

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
    ) -> GoogleContainerNodePoolNodeConfigAdvancedMachineFeaturesOutputReference:
        return typing.cast(GoogleContainerNodePoolNodeConfigAdvancedMachineFeaturesOutputReference, jsii.get(self, "advancedMachineFeatures"))

    @builtins.property
    @jsii.member(jsii_name="confidentialNodes")
    def confidential_nodes(
        self,
    ) -> GoogleContainerNodePoolNodeConfigConfidentialNodesOutputReference:
        return typing.cast(GoogleContainerNodePoolNodeConfigConfidentialNodesOutputReference, jsii.get(self, "confidentialNodes"))

    @builtins.property
    @jsii.member(jsii_name="containerdConfig")
    def containerd_config(
        self,
    ) -> GoogleContainerNodePoolNodeConfigContainerdConfigOutputReference:
        return typing.cast(GoogleContainerNodePoolNodeConfigContainerdConfigOutputReference, jsii.get(self, "containerdConfig"))

    @builtins.property
    @jsii.member(jsii_name="effectiveTaints")
    def effective_taints(self) -> GoogleContainerNodePoolNodeConfigEffectiveTaintsList:
        return typing.cast(GoogleContainerNodePoolNodeConfigEffectiveTaintsList, jsii.get(self, "effectiveTaints"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorageConfig")
    def ephemeral_storage_config(
        self,
    ) -> GoogleContainerNodePoolNodeConfigEphemeralStorageConfigOutputReference:
        return typing.cast(GoogleContainerNodePoolNodeConfigEphemeralStorageConfigOutputReference, jsii.get(self, "ephemeralStorageConfig"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorageLocalSsdConfig")
    def ephemeral_storage_local_ssd_config(
        self,
    ) -> GoogleContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfigOutputReference:
        return typing.cast(GoogleContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfigOutputReference, jsii.get(self, "ephemeralStorageLocalSsdConfig"))

    @builtins.property
    @jsii.member(jsii_name="fastSocket")
    def fast_socket(self) -> GoogleContainerNodePoolNodeConfigFastSocketOutputReference:
        return typing.cast(GoogleContainerNodePoolNodeConfigFastSocketOutputReference, jsii.get(self, "fastSocket"))

    @builtins.property
    @jsii.member(jsii_name="gcfsConfig")
    def gcfs_config(self) -> GoogleContainerNodePoolNodeConfigGcfsConfigOutputReference:
        return typing.cast(GoogleContainerNodePoolNodeConfigGcfsConfigOutputReference, jsii.get(self, "gcfsConfig"))

    @builtins.property
    @jsii.member(jsii_name="guestAccelerator")
    def guest_accelerator(
        self,
    ) -> GoogleContainerNodePoolNodeConfigGuestAcceleratorList:
        return typing.cast(GoogleContainerNodePoolNodeConfigGuestAcceleratorList, jsii.get(self, "guestAccelerator"))

    @builtins.property
    @jsii.member(jsii_name="gvnic")
    def gvnic(self) -> GoogleContainerNodePoolNodeConfigGvnicOutputReference:
        return typing.cast(GoogleContainerNodePoolNodeConfigGvnicOutputReference, jsii.get(self, "gvnic"))

    @builtins.property
    @jsii.member(jsii_name="hostMaintenancePolicy")
    def host_maintenance_policy(
        self,
    ) -> GoogleContainerNodePoolNodeConfigHostMaintenancePolicyOutputReference:
        return typing.cast(GoogleContainerNodePoolNodeConfigHostMaintenancePolicyOutputReference, jsii.get(self, "hostMaintenancePolicy"))

    @builtins.property
    @jsii.member(jsii_name="kubeletConfig")
    def kubelet_config(
        self,
    ) -> GoogleContainerNodePoolNodeConfigKubeletConfigOutputReference:
        return typing.cast(GoogleContainerNodePoolNodeConfigKubeletConfigOutputReference, jsii.get(self, "kubeletConfig"))

    @builtins.property
    @jsii.member(jsii_name="linuxNodeConfig")
    def linux_node_config(
        self,
    ) -> GoogleContainerNodePoolNodeConfigLinuxNodeConfigOutputReference:
        return typing.cast(GoogleContainerNodePoolNodeConfigLinuxNodeConfigOutputReference, jsii.get(self, "linuxNodeConfig"))

    @builtins.property
    @jsii.member(jsii_name="localNvmeSsdBlockConfig")
    def local_nvme_ssd_block_config(
        self,
    ) -> GoogleContainerNodePoolNodeConfigLocalNvmeSsdBlockConfigOutputReference:
        return typing.cast(GoogleContainerNodePoolNodeConfigLocalNvmeSsdBlockConfigOutputReference, jsii.get(self, "localNvmeSsdBlockConfig"))

    @builtins.property
    @jsii.member(jsii_name="reservationAffinity")
    def reservation_affinity(
        self,
    ) -> "GoogleContainerNodePoolNodeConfigReservationAffinityOutputReference":
        return typing.cast("GoogleContainerNodePoolNodeConfigReservationAffinityOutputReference", jsii.get(self, "reservationAffinity"))

    @builtins.property
    @jsii.member(jsii_name="sandboxConfig")
    def sandbox_config(
        self,
    ) -> "GoogleContainerNodePoolNodeConfigSandboxConfigOutputReference":
        return typing.cast("GoogleContainerNodePoolNodeConfigSandboxConfigOutputReference", jsii.get(self, "sandboxConfig"))

    @builtins.property
    @jsii.member(jsii_name="secondaryBootDisks")
    def secondary_boot_disks(
        self,
    ) -> "GoogleContainerNodePoolNodeConfigSecondaryBootDisksList":
        return typing.cast("GoogleContainerNodePoolNodeConfigSecondaryBootDisksList", jsii.get(self, "secondaryBootDisks"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfig")
    def shielded_instance_config(
        self,
    ) -> "GoogleContainerNodePoolNodeConfigShieldedInstanceConfigOutputReference":
        return typing.cast("GoogleContainerNodePoolNodeConfigShieldedInstanceConfigOutputReference", jsii.get(self, "shieldedInstanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="soleTenantConfig")
    def sole_tenant_config(
        self,
    ) -> "GoogleContainerNodePoolNodeConfigSoleTenantConfigOutputReference":
        return typing.cast("GoogleContainerNodePoolNodeConfigSoleTenantConfigOutputReference", jsii.get(self, "soleTenantConfig"))

    @builtins.property
    @jsii.member(jsii_name="taint")
    def taint(self) -> "GoogleContainerNodePoolNodeConfigTaintList":
        return typing.cast("GoogleContainerNodePoolNodeConfigTaintList", jsii.get(self, "taint"))

    @builtins.property
    @jsii.member(jsii_name="windowsNodeConfig")
    def windows_node_config(
        self,
    ) -> "GoogleContainerNodePoolNodeConfigWindowsNodeConfigOutputReference":
        return typing.cast("GoogleContainerNodePoolNodeConfigWindowsNodeConfigOutputReference", jsii.get(self, "windowsNodeConfig"))

    @builtins.property
    @jsii.member(jsii_name="workloadMetadataConfig")
    def workload_metadata_config(
        self,
    ) -> "GoogleContainerNodePoolNodeConfigWorkloadMetadataConfigOutputReference":
        return typing.cast("GoogleContainerNodePoolNodeConfigWorkloadMetadataConfigOutputReference", jsii.get(self, "workloadMetadataConfig"))

    @builtins.property
    @jsii.member(jsii_name="advancedMachineFeaturesInput")
    def advanced_machine_features_input(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigAdvancedMachineFeatures]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigAdvancedMachineFeatures], jsii.get(self, "advancedMachineFeaturesInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskKmsKeyInput")
    def boot_disk_kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootDiskKmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="confidentialNodesInput")
    def confidential_nodes_input(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigConfidentialNodes]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigConfidentialNodes], jsii.get(self, "confidentialNodesInput"))

    @builtins.property
    @jsii.member(jsii_name="containerdConfigInput")
    def containerd_config_input(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigContainerdConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigContainerdConfig], jsii.get(self, "containerdConfigInput"))

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
    @jsii.member(jsii_name="ephemeralStorageConfigInput")
    def ephemeral_storage_config_input(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigEphemeralStorageConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigEphemeralStorageConfig], jsii.get(self, "ephemeralStorageConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorageLocalSsdConfigInput")
    def ephemeral_storage_local_ssd_config_input(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig], jsii.get(self, "ephemeralStorageLocalSsdConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fastSocketInput")
    def fast_socket_input(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigFastSocket]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigFastSocket], jsii.get(self, "fastSocketInput"))

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
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigGcfsConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigGcfsConfig], jsii.get(self, "gcfsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="guestAcceleratorInput")
    def guest_accelerator_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigGuestAccelerator]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigGuestAccelerator]]], jsii.get(self, "guestAcceleratorInput"))

    @builtins.property
    @jsii.member(jsii_name="gvnicInput")
    def gvnic_input(self) -> typing.Optional[GoogleContainerNodePoolNodeConfigGvnic]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigGvnic], jsii.get(self, "gvnicInput"))

    @builtins.property
    @jsii.member(jsii_name="hostMaintenancePolicyInput")
    def host_maintenance_policy_input(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigHostMaintenancePolicy]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigHostMaintenancePolicy], jsii.get(self, "hostMaintenancePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="imageTypeInput")
    def image_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="kubeletConfigInput")
    def kubelet_config_input(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigKubeletConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigKubeletConfig], jsii.get(self, "kubeletConfigInput"))

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
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigLinuxNodeConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigLinuxNodeConfig], jsii.get(self, "linuxNodeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="localNvmeSsdBlockConfigInput")
    def local_nvme_ssd_block_config_input(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig], jsii.get(self, "localNvmeSsdBlockConfigInput"))

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
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigReservationAffinity"]:
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigReservationAffinity"], jsii.get(self, "reservationAffinityInput"))

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
    @jsii.member(jsii_name="sandboxConfigInput")
    def sandbox_config_input(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigSandboxConfig"]:
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigSandboxConfig"], jsii.get(self, "sandboxConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryBootDisksInput")
    def secondary_boot_disks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerNodePoolNodeConfigSecondaryBootDisks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerNodePoolNodeConfigSecondaryBootDisks"]]], jsii.get(self, "secondaryBootDisksInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfigInput")
    def shielded_instance_config_input(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigShieldedInstanceConfig"]:
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigShieldedInstanceConfig"], jsii.get(self, "shieldedInstanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="soleTenantConfigInput")
    def sole_tenant_config_input(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigSoleTenantConfig"]:
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigSoleTenantConfig"], jsii.get(self, "soleTenantConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerNodePoolNodeConfigTaint"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerNodePoolNodeConfigTaint"]]], jsii.get(self, "taintInput"))

    @builtins.property
    @jsii.member(jsii_name="windowsNodeConfigInput")
    def windows_node_config_input(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigWindowsNodeConfig"]:
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigWindowsNodeConfig"], jsii.get(self, "windowsNodeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadMetadataConfigInput")
    def workload_metadata_config_input(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolNodeConfigWorkloadMetadataConfig"]:
        return typing.cast(typing.Optional["GoogleContainerNodePoolNodeConfigWorkloadMetadataConfig"], jsii.get(self, "workloadMetadataConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskKmsKey")
    def boot_disk_kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootDiskKmsKey"))

    @boot_disk_kms_key.setter
    def boot_disk_kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e682e5865c527f5cb6077013cf771e1c350c2b1174b3fe861a44dd2ff99df6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskKmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c1fcb99d6f2f8b5faf70392de7d0e5b09973cdf838da97b37a3a66bfb3f0573)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskType")
    def disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskType"))

    @disk_type.setter
    def disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49cd5414ef90e98e356ed3fb10d95c614d01096c1780d1bccb8960bde4754c0d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf7cb0d8f198ecbca817aa93c50b649d29b997b0c29d4014caf92341f45ca95b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c45ad485fecaccc24fdc70364be932e222c9504d067cf0dc214c8581df2c74e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flexStart", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageType")
    def image_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageType"))

    @image_type.setter
    def image_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b7af0a4f9d15ba8b06f0307f00574b87fc4a24cfea1e2b9950ca456d2e8698f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ed1fc1e97d24235af2e23f59a2313b73a795fb82e35f86d683adba3c93603ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localSsdCount")
    def local_ssd_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "localSsdCount"))

    @local_ssd_count.setter
    def local_ssd_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd31ab7a7ed6e9b548d8610df0a3ad2e2746ae21d1e6745adef23db664b3539d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localSsdCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localSsdEncryptionMode")
    def local_ssd_encryption_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localSsdEncryptionMode"))

    @local_ssd_encryption_mode.setter
    def local_ssd_encryption_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9327250830f19920e3b1ed2d0186c95986730dd8bdba5fbc3181b332fac8c10f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localSsdEncryptionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loggingVariant")
    def logging_variant(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loggingVariant"))

    @logging_variant.setter
    def logging_variant(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d3be33935e83a6a3021fac7f119be8890231f4e5008bc3a448464d3f1889e38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingVariant", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2a5c3f62da835a37b7f31b5e4518552a60b06fd62f4f0c26551bb26ced75f5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRunDuration")
    def max_run_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxRunDuration"))

    @max_run_duration.setter
    def max_run_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__141ce6abafa9b018206619b69036d7a7510b556cef1aae13bed8ad91574d30cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRunDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ec81278e703260ace9aaa7665336a977da1a7214164dc04592374d584f44936)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatform")
    def min_cpu_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minCpuPlatform"))

    @min_cpu_platform.setter
    def min_cpu_platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88e24168b227957a66c71c7055f00119442e623f067ac50714a98c20b24419f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCpuPlatform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeGroup")
    def node_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeGroup"))

    @node_group.setter
    def node_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2dc69c0db50ecc53a733d01bf1759316d86abca0884cfbfb2f525fe60a54f77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthScopes")
    def oauth_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthScopes"))

    @oauth_scopes.setter
    def oauth_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96ff12302b86f1fb4480f4e08f109c82bd19972d642829c4338aeb99095580c3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26b2d8bbc6b9ee59ee1c0371c8927782bd89d1e227d9ca9348a07c938e0b1629)
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
            type_hints = typing.get_type_hints(_typecheckingstub__005c0f9f55ae67b0657c42b02946f51251557548c7dc54d8e85a54c84fcb2af7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9309a54b4b3e7fb2073b67916613c8bdcb13b3bdcf528fd4e5b23b4346344550)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceManagerTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f76c8a79c7be3e64990423d2732776e857502e27101127c6a64471b583f475e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a4da15d6e027e9d872b5f17fc10a9f77e4a515bd19fe4c4bbcd1ffb4fc408e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storagePools")
    def storage_pools(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "storagePools"))

    @storage_pools.setter
    def storage_pools(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c167a57fcbe581a798dbd82110ad6043956138466a9c2e86bf2f4cff265a404c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storagePools", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__172219d24714c011f42cf338aae3f37088bc119a31c76d00cf9d6c41ac217c88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleContainerNodePoolNodeConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17c3310f67f012f91ac82a292866e11ef88825d77e88ffc8b2f255c98a5949a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigReservationAffinity",
    jsii_struct_bases=[],
    name_mapping={
        "consume_reservation_type": "consumeReservationType",
        "key": "key",
        "values": "values",
    },
)
class GoogleContainerNodePoolNodeConfigReservationAffinity:
    def __init__(
        self,
        *,
        consume_reservation_type: builtins.str,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param consume_reservation_type: Corresponds to the type of reservation consumption. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#consume_reservation_type GoogleContainerNodePool#consume_reservation_type}
        :param key: The label key of a reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#key GoogleContainerNodePool#key}
        :param values: The label values of the reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#values GoogleContainerNodePool#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4da75a11d74f34a2d86b26a212ef59bbd6ba8b2d25fefa448a97b453892b385e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#consume_reservation_type GoogleContainerNodePool#consume_reservation_type}
        '''
        result = self._values.get("consume_reservation_type")
        assert result is not None, "Required property 'consume_reservation_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''The label key of a reservation resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#key GoogleContainerNodePool#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The label values of the reservation resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#values GoogleContainerNodePool#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigReservationAffinity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigReservationAffinityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigReservationAffinityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__170f0f021381907dbd31821afbf330731a41418450daac7a47860a9ebf6db740)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db0a63dd42155c563d781c8d5971df716f889a9bb96fddd2d06695fd9aeece75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumeReservationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc6bed937ed104aa55beafe6dfc3e9ccd423a6ef60082de6c1f74f6f2bdc3840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8a73ac024dadacc137c35e153b21d62269c06d82418a5c3e461057ca2f8201e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigReservationAffinity]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigReservationAffinity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigReservationAffinity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f01c015db06843e7ee7c3a12a5c88dadf2e09e1909d1229f0471861874a3ae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigSandboxConfig",
    jsii_struct_bases=[],
    name_mapping={"sandbox_type": "sandboxType"},
)
class GoogleContainerNodePoolNodeConfigSandboxConfig:
    def __init__(self, *, sandbox_type: builtins.str) -> None:
        '''
        :param sandbox_type: Type of the sandbox to use for the node (e.g. 'gvisor'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#sandbox_type GoogleContainerNodePool#sandbox_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d5c575f7ae9cea24a8a831a10c5e8a5e52e78f25b2f52987ac889ff8b42c7d8)
            check_type(argname="argument sandbox_type", value=sandbox_type, expected_type=type_hints["sandbox_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sandbox_type": sandbox_type,
        }

    @builtins.property
    def sandbox_type(self) -> builtins.str:
        '''Type of the sandbox to use for the node (e.g. 'gvisor').

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#sandbox_type GoogleContainerNodePool#sandbox_type}
        '''
        result = self._values.get("sandbox_type")
        assert result is not None, "Required property 'sandbox_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigSandboxConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigSandboxConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigSandboxConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f904bcfcc6edf5f3eea0738fee72edf59e1705299f0496d408a9ff62e5b372fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="sandboxTypeInput")
    def sandbox_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sandboxTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sandboxType")
    def sandbox_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sandboxType"))

    @sandbox_type.setter
    def sandbox_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01867d97bdc00764faf098c67627d1c7583763414db4169bd158606a719808eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sandboxType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigSandboxConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigSandboxConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigSandboxConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc5d8485307675a141340c8478c20b45ef37c503c7e29f2171d65d55e88e91c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigSecondaryBootDisks",
    jsii_struct_bases=[],
    name_mapping={"disk_image": "diskImage", "mode": "mode"},
)
class GoogleContainerNodePoolNodeConfigSecondaryBootDisks:
    def __init__(
        self,
        *,
        disk_image: builtins.str,
        mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_image: Disk image to create the secondary boot disk from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#disk_image GoogleContainerNodePool#disk_image}
        :param mode: Mode for how the secondary boot disk is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#mode GoogleContainerNodePool#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a3ca0b39fabc6d130717f1708a3b55fcb47e12d98b94a845a55129b6b3f5a47)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#disk_image GoogleContainerNodePool#disk_image}
        '''
        result = self._values.get("disk_image")
        assert result is not None, "Required property 'disk_image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Mode for how the secondary boot disk is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#mode GoogleContainerNodePool#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigSecondaryBootDisks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigSecondaryBootDisksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigSecondaryBootDisksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b982b10c4f763a45e6c88e59bdb22ee990224b0633e68a93fd8ec75914e7205)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleContainerNodePoolNodeConfigSecondaryBootDisksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da0b7e4798acdc0c8dbf58c0d54990e7d91d76796279cdab24261c8bbd6db3f6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleContainerNodePoolNodeConfigSecondaryBootDisksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f6cc20380e8541c7b217f6360f43202fed67c9b78d16ec143ca3d0ff312af2f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2c6c88014b678520b79710b7d3e64b9996f7b41fb97a4aa4d1c38b8658cd9cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__140f1455cf46e7ad63af9df7152f0f605d06d335ac1326b8fda7c6d2e98422df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigSecondaryBootDisks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigSecondaryBootDisks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigSecondaryBootDisks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e454f9fcebde51425137e024ed946d454b4473579f11423414dbec233ee29e6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerNodePoolNodeConfigSecondaryBootDisksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigSecondaryBootDisksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89841b581e87fb390179ab2a6835a8e3f599b119e4cb03d2be693988dbe412f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__992ef694e206f5602a3892013f17d817d43fd1f90a48c4a934c2ce5e092a3f87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskImage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77d263b650f230b10a2343c98010c7ef28dadc7d7480d3e5c855924f0250cd2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNodeConfigSecondaryBootDisks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNodeConfigSecondaryBootDisks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNodeConfigSecondaryBootDisks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2fa049bc34c3c7d456cf9b330dbf6a214d82d76f7a7acbd02f1248410c1a183)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigShieldedInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_integrity_monitoring": "enableIntegrityMonitoring",
        "enable_secure_boot": "enableSecureBoot",
    },
)
class GoogleContainerNodePoolNodeConfigShieldedInstanceConfig:
    def __init__(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Defines whether the instance has integrity monitoring enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enable_integrity_monitoring GoogleContainerNodePool#enable_integrity_monitoring}
        :param enable_secure_boot: Defines whether the instance has Secure Boot enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enable_secure_boot GoogleContainerNodePool#enable_secure_boot}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d30d3e12add344b754741b55e899c279f80b43f7669599fa42aa919b682a354)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enable_integrity_monitoring GoogleContainerNodePool#enable_integrity_monitoring}
        '''
        result = self._values.get("enable_integrity_monitoring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_secure_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether the instance has Secure Boot enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enable_secure_boot GoogleContainerNodePool#enable_secure_boot}
        '''
        result = self._values.get("enable_secure_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigShieldedInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigShieldedInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigShieldedInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__074a8824f4189fa0f3b487e51506232a56c64c138a54423f52de07a056d01695)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f12be696c4d1eb3739c5329fc1f57d52002af8d4b1cfe401e10b79038f59288)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92f10df846228f3951c9cce63b82187640b521dc7cac4a829bac6ce1673cbccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSecureBoot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigShieldedInstanceConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigShieldedInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigShieldedInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c89a29e3ff2cdffa5769dda9a58b9ff09afac4ba2712fe83ff9d0274a5a783b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigSoleTenantConfig",
    jsii_struct_bases=[],
    name_mapping={"node_affinity": "nodeAffinity"},
)
class GoogleContainerNodePoolNodeConfigSoleTenantConfig:
    def __init__(
        self,
        *,
        node_affinity: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param node_affinity: node_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#node_affinity GoogleContainerNodePool#node_affinity}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2ae0478176e7f4db4874d07c18ecda7da528b7dcf8c5ea47cd93b73940b34af)
            check_type(argname="argument node_affinity", value=node_affinity, expected_type=type_hints["node_affinity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "node_affinity": node_affinity,
        }

    @builtins.property
    def node_affinity(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity"]]:
        '''node_affinity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#node_affinity GoogleContainerNodePool#node_affinity}
        '''
        result = self._values.get("node_affinity")
        assert result is not None, "Required property 'node_affinity' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigSoleTenantConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "operator": "operator", "values": "values"},
)
class GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity:
    def __init__(
        self,
        *,
        key: builtins.str,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: . Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#key GoogleContainerNodePool#key}
        :param operator: . Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#operator GoogleContainerNodePool#operator}
        :param values: . Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#values GoogleContainerNodePool#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f94a27766ed8ae1f268d91b9c0c6fd2fe102a573dd2a5b5ce130f7a803c8ff8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#key GoogleContainerNodePool#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#operator GoogleContainerNodePool#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#values GoogleContainerNodePool#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7670aa0f12a38aa50a41ba2c640b818100f96a5bbda51932c3e203128f6a329e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcd7a0bc359eb767524376584aaab28d53d272e507f2699654b40b48aed485ff)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbe8732ca367f396ef0bc89fb325ad97e19a4fe0894edd8ecf3e926622f25309)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70ee7398fe7ebf9b55c3f7d11296fad54fb766b8808d9a3ac712c00bfcfd1ad4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf4484bfba9f3edf02c9a1e0183b3c56acdc6e7242548c786c71673fd4a42445)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f94989f89038738e89407086ec36b932936246cf4f9afd7e1a0b13e861a16966)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70e047c539401fdd0c78ce873cf463fb13df628af472acb82fda4eff0adf2a8c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc015749f0b85d684db8f87007d0a69ddd11891d3eb83f8613e7b122d9e33114)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d017d1668e655493881644f92e0ebc8b88ca77e6c74102a3515608dd3cdcd93e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad165a94965ca741be15811e1c747e2c4c4d790e57c006a9221981161f2d237)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fcab9fe9bb8960165d3f6e72377292ba85b38f05fe089a68c65e52e934f03c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerNodePoolNodeConfigSoleTenantConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigSoleTenantConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__140b10c29b444001cb277fb271d98c1ef9d7e39f32d3e4d84485e8db9077a8f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodeAffinity")
    def put_node_affinity(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21767b13a87e7dc8096154d7137864b56590652918328787a56643df8e70f3c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeAffinity", [value]))

    @builtins.property
    @jsii.member(jsii_name="nodeAffinity")
    def node_affinity(
        self,
    ) -> GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinityList:
        return typing.cast(GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinityList, jsii.get(self, "nodeAffinity"))

    @builtins.property
    @jsii.member(jsii_name="nodeAffinityInput")
    def node_affinity_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity]]], jsii.get(self, "nodeAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigSoleTenantConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigSoleTenantConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigSoleTenantConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c183a5c2ffe21862bd9d528949ff1a6c4c1688fb0b1d9412956583c9d43e376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigTaint",
    jsii_struct_bases=[],
    name_mapping={"effect": "effect", "key": "key", "value": "value"},
)
class GoogleContainerNodePoolNodeConfigTaint:
    def __init__(
        self,
        *,
        effect: builtins.str,
        key: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param effect: Effect for taint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#effect GoogleContainerNodePool#effect}
        :param key: Key for taint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#key GoogleContainerNodePool#key}
        :param value: Value for taint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#value GoogleContainerNodePool#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__224f81127254286dab77b4de47c1b26ca36daf23b5392f6fc288c9950e5e0749)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#effect GoogleContainerNodePool#effect}
        '''
        result = self._values.get("effect")
        assert result is not None, "Required property 'effect' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Key for taint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#key GoogleContainerNodePool#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Value for taint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#value GoogleContainerNodePool#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigTaint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigTaintList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigTaintList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61b5c54ce78178bdbc708afadf1345f2840914436d975a0a2a5d9290c1d8f4dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleContainerNodePoolNodeConfigTaintOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13320fcdeecd7c12e1b64d7da141bd0c2654a66f65ee4a0bb8fe80b2e354834b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleContainerNodePoolNodeConfigTaintOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5a518fc02367eedf6091f8e392af22576dca52e112c5d8af3c729b193974c8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51e3a8a32400b4de02b639ba4fd73b522133b6bbba25d2d8eb12b9173863e72f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d73f3ab06b109825a617fa3c0e0708763a56b6dfc99da76cde7c2a30c8885d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigTaint]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigTaint]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigTaint]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__487c4224289a73764532f09c809e9b861f987548be9e77f7b649dd1fd952b32d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerNodePoolNodeConfigTaintOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigTaintOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2563df036fc207ba1c691a321907288589907b1317b84369decb79173487458f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ed24bb5735290623c794efe56d216076fabc2dc99fc59d7a7ba69ea53dfabbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cac8133b2281a075a450179ee2621a4b67297454ae0e1c38486dc9c3420ce7a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d86242c967062aa108f0cdfd603457913714ec5e4f9fdc3a581d1562be2cf494)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNodeConfigTaint]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNodeConfigTaint]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNodeConfigTaint]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61614be0f0a57e9f3a0934ff5bf9c0c841e2a2462492fbdbce76cfd1993a00eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigWindowsNodeConfig",
    jsii_struct_bases=[],
    name_mapping={"osversion": "osversion"},
)
class GoogleContainerNodePoolNodeConfigWindowsNodeConfig:
    def __init__(self, *, osversion: typing.Optional[builtins.str] = None) -> None:
        '''
        :param osversion: The OS Version of the windows nodepool.Values are OS_VERSION_UNSPECIFIED,OS_VERSION_LTSC2019 and OS_VERSION_LTSC2022. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#osversion GoogleContainerNodePool#osversion}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41a5bf48cb6525e6525b18f21a989b089f8ba7491c8ad505113941344e508275)
            check_type(argname="argument osversion", value=osversion, expected_type=type_hints["osversion"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if osversion is not None:
            self._values["osversion"] = osversion

    @builtins.property
    def osversion(self) -> typing.Optional[builtins.str]:
        '''The OS Version of the windows nodepool.Values are OS_VERSION_UNSPECIFIED,OS_VERSION_LTSC2019 and OS_VERSION_LTSC2022.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#osversion GoogleContainerNodePool#osversion}
        '''
        result = self._values.get("osversion")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigWindowsNodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigWindowsNodeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigWindowsNodeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a6923790be3e6154633450f6a430f525fdb107771142804b973abb988e222cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb26668983afea395c57102d0f30e4b0906e582c3751a68ed1f4ed08d3f40bcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osversion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigWindowsNodeConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigWindowsNodeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigWindowsNodeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__874b12cd5a1201bb9e8edc06556fa2f994ebf0488bf364d5f49bf7dbb5d9f8a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigWorkloadMetadataConfig",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode"},
)
class GoogleContainerNodePoolNodeConfigWorkloadMetadataConfig:
    def __init__(self, *, mode: builtins.str) -> None:
        '''
        :param mode: Mode is the configuration for how to expose metadata to workloads running on the node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#mode GoogleContainerNodePool#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b83ab657230f1126004d64d5867a5f41647747550c6d00c4e9ed4c0e2050f56)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''Mode is the configuration for how to expose metadata to workloads running on the node.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#mode GoogleContainerNodePool#mode}
        '''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolNodeConfigWorkloadMetadataConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolNodeConfigWorkloadMetadataConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolNodeConfigWorkloadMetadataConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdbcb7e4fd2622518c403b6afdc63db8febc2d492867510537dc11868e123155)
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
            type_hints = typing.get_type_hints(_typecheckingstub__756f7dcf18b7a5d4e0f183746c7731145bc8035f07c5cceb75fca59e40a71029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolNodeConfigWorkloadMetadataConfig]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolNodeConfigWorkloadMetadataConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolNodeConfigWorkloadMetadataConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08ee79e7c3b541b59e59c16bdac5ae15619c863bc855ca42c577d530dde23f60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolPlacementPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "policy_name": "policyName",
        "tpu_topology": "tpuTopology",
    },
)
class GoogleContainerNodePoolPlacementPolicy:
    def __init__(
        self,
        *,
        type: builtins.str,
        policy_name: typing.Optional[builtins.str] = None,
        tpu_topology: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type defines the type of placement policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#type GoogleContainerNodePool#type}
        :param policy_name: If set, refers to the name of a custom resource policy supplied by the user. The resource policy must be in the same project and region as the node pool. If not found, InvalidArgument error is returned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#policy_name GoogleContainerNodePool#policy_name}
        :param tpu_topology: The TPU topology like "2x4" or "2x2x2". https://cloud.google.com/kubernetes-engine/docs/concepts/plan-tpus#topology. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#tpu_topology GoogleContainerNodePool#tpu_topology}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66829d3b46e9e34ed947a48c35f153bcb2495c283653c64d6722bad05fa65f60)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#type GoogleContainerNodePool#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''If set, refers to the name of a custom resource policy supplied by the user.

        The resource policy must be in the same project and region as the node pool. If not found, InvalidArgument error is returned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#policy_name GoogleContainerNodePool#policy_name}
        '''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpu_topology(self) -> typing.Optional[builtins.str]:
        '''The TPU topology like "2x4" or "2x2x2". https://cloud.google.com/kubernetes-engine/docs/concepts/plan-tpus#topology.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#tpu_topology GoogleContainerNodePool#tpu_topology}
        '''
        result = self._values.get("tpu_topology")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolPlacementPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolPlacementPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolPlacementPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b047ca53213df25a4d17647a6b862812aa7a87a2abb1832a1dcc198c4d934c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee9a332c844b1093c0a6b10089321ad0c1f47d2a4899c18f90bc4f582338c60f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tpuTopology")
    def tpu_topology(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpuTopology"))

    @tpu_topology.setter
    def tpu_topology(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9efa69ab76af0c873f28b0809f41177fde16af0bed222e58c5f61d7576370d45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpuTopology", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b43fbe4b3dbdd56b027a35c3c1b3c90592841311d6cdb068468ecc9d0c8a0624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleContainerNodePoolPlacementPolicy]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolPlacementPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolPlacementPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fd5a443fe462b4d296b11941668ef312731e9d206548caed64871f0ef51b2a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolQueuedProvisioning",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleContainerNodePoolQueuedProvisioning:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether nodes in this node pool are obtainable solely through the ProvisioningRequest API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enabled GoogleContainerNodePool#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d778a088e764622c77b7a6a9765085b0a051d37e7519385b82979564bff8c8f6)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether nodes in this node pool are obtainable solely through the ProvisioningRequest API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#enabled GoogleContainerNodePool#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolQueuedProvisioning(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolQueuedProvisioningOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolQueuedProvisioningOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__acd21d276258e05b48553b20cf8f45c95b214f41f8cc57c1ea8fd1ccca2a03b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f9abb498e4e36f6c64eb0e72a55cf8e98b5b9f199b42d7bb7298e3144f4655b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolQueuedProvisioning]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolQueuedProvisioning], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolQueuedProvisioning],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05201505b603204d09aa115b7d840cd7ece1c16adee349233cbbf75b25170751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleContainerNodePoolTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#create GoogleContainerNodePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#delete GoogleContainerNodePool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#update GoogleContainerNodePool#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1ef94cdeb888213f7213948ef71334530b24d3f312bba6b881e35f29e1149fa)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#create GoogleContainerNodePool#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#delete GoogleContainerNodePool#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#update GoogleContainerNodePool#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e39882dbed07a22399e5a8ef93f52663a5fb8fa2971465b8012d7d024c1808f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb7bedffbf2336aaa1d7db42da2c15e62993a9e6de13ebcfe46f1f2739a4f40c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27ac208a79f53e13719db31308600ca0e682bfa817f0e61161640a69b78de3e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88f22cbc5bdf0d5f8e61e1ad1f489a1d702259be99ac0bd10217b5132fbfa7ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71a28ef4528ea4129ad85a8eee4d552fea146af9634dfd6f190a7090d6ccfba6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolUpgradeSettings",
    jsii_struct_bases=[],
    name_mapping={
        "blue_green_settings": "blueGreenSettings",
        "max_surge": "maxSurge",
        "max_unavailable": "maxUnavailable",
        "strategy": "strategy",
    },
)
class GoogleContainerNodePoolUpgradeSettings:
    def __init__(
        self,
        *,
        blue_green_settings: typing.Optional[typing.Union["GoogleContainerNodePoolUpgradeSettingsBlueGreenSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        max_surge: typing.Optional[jsii.Number] = None,
        max_unavailable: typing.Optional[jsii.Number] = None,
        strategy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param blue_green_settings: blue_green_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#blue_green_settings GoogleContainerNodePool#blue_green_settings}
        :param max_surge: The number of additional nodes that can be added to the node pool during an upgrade. Increasing max_surge raises the number of nodes that can be upgraded simultaneously. Can be set to 0 or greater. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#max_surge GoogleContainerNodePool#max_surge}
        :param max_unavailable: The number of nodes that can be simultaneously unavailable during an upgrade. Increasing max_unavailable raises the number of nodes that can be upgraded in parallel. Can be set to 0 or greater. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#max_unavailable GoogleContainerNodePool#max_unavailable}
        :param strategy: Update strategy for the given nodepool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#strategy GoogleContainerNodePool#strategy}
        '''
        if isinstance(blue_green_settings, dict):
            blue_green_settings = GoogleContainerNodePoolUpgradeSettingsBlueGreenSettings(**blue_green_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceae5e61bc3cc59dc916e9a682f0c33b5f2ff9c057244f29f173d2f3c781cfcd)
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
    ) -> typing.Optional["GoogleContainerNodePoolUpgradeSettingsBlueGreenSettings"]:
        '''blue_green_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#blue_green_settings GoogleContainerNodePool#blue_green_settings}
        '''
        result = self._values.get("blue_green_settings")
        return typing.cast(typing.Optional["GoogleContainerNodePoolUpgradeSettingsBlueGreenSettings"], result)

    @builtins.property
    def max_surge(self) -> typing.Optional[jsii.Number]:
        '''The number of additional nodes that can be added to the node pool during an upgrade.

        Increasing max_surge raises the number of nodes that can be upgraded simultaneously. Can be set to 0 or greater.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#max_surge GoogleContainerNodePool#max_surge}
        '''
        result = self._values.get("max_surge")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_unavailable(self) -> typing.Optional[jsii.Number]:
        '''The number of nodes that can be simultaneously unavailable during an upgrade.

        Increasing max_unavailable raises the number of nodes that can be upgraded in parallel. Can be set to 0 or greater.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#max_unavailable GoogleContainerNodePool#max_unavailable}
        '''
        result = self._values.get("max_unavailable")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def strategy(self) -> typing.Optional[builtins.str]:
        '''Update strategy for the given nodepool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#strategy GoogleContainerNodePool#strategy}
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolUpgradeSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolUpgradeSettingsBlueGreenSettings",
    jsii_struct_bases=[],
    name_mapping={
        "standard_rollout_policy": "standardRolloutPolicy",
        "node_pool_soak_duration": "nodePoolSoakDuration",
    },
)
class GoogleContainerNodePoolUpgradeSettingsBlueGreenSettings:
    def __init__(
        self,
        *,
        standard_rollout_policy: typing.Union["GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy", typing.Dict[builtins.str, typing.Any]],
        node_pool_soak_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param standard_rollout_policy: standard_rollout_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#standard_rollout_policy GoogleContainerNodePool#standard_rollout_policy}
        :param node_pool_soak_duration: Time needed after draining entire blue pool. After this period, blue pool will be cleaned up. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#node_pool_soak_duration GoogleContainerNodePool#node_pool_soak_duration}
        '''
        if isinstance(standard_rollout_policy, dict):
            standard_rollout_policy = GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy(**standard_rollout_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cb7777d935afe680d1432b069a74170722f58d400c5d6bae8cf5ee83193c839)
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
    ) -> "GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy":
        '''standard_rollout_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#standard_rollout_policy GoogleContainerNodePool#standard_rollout_policy}
        '''
        result = self._values.get("standard_rollout_policy")
        assert result is not None, "Required property 'standard_rollout_policy' is missing"
        return typing.cast("GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy", result)

    @builtins.property
    def node_pool_soak_duration(self) -> typing.Optional[builtins.str]:
        '''Time needed after draining entire blue pool. After this period, blue pool will be cleaned up.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#node_pool_soak_duration GoogleContainerNodePool#node_pool_soak_duration}
        '''
        result = self._values.get("node_pool_soak_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolUpgradeSettingsBlueGreenSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__975413c35d8f76a098165bfb01a950161b321e0c75067cc05deacb7b1b885b0a)
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
        :param batch_node_count: Number of blue nodes to drain in a batch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#batch_node_count GoogleContainerNodePool#batch_node_count}
        :param batch_percentage: Percentage of the blue pool nodes to drain in a batch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#batch_percentage GoogleContainerNodePool#batch_percentage}
        :param batch_soak_duration: Soak time after each batch gets drained. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#batch_soak_duration GoogleContainerNodePool#batch_soak_duration}
        '''
        value = GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy(
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
    ) -> "GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicyOutputReference":
        return typing.cast("GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicyOutputReference", jsii.get(self, "standardRolloutPolicy"))

    @builtins.property
    @jsii.member(jsii_name="nodePoolSoakDurationInput")
    def node_pool_soak_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodePoolSoakDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="standardRolloutPolicyInput")
    def standard_rollout_policy_input(
        self,
    ) -> typing.Optional["GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy"]:
        return typing.cast(typing.Optional["GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy"], jsii.get(self, "standardRolloutPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="nodePoolSoakDuration")
    def node_pool_soak_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodePoolSoakDuration"))

    @node_pool_soak_duration.setter
    def node_pool_soak_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__080f086450b74f1812863fa7749452bd02f15e322c7e52607b7314c0827032a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodePoolSoakDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolUpgradeSettingsBlueGreenSettings]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolUpgradeSettingsBlueGreenSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolUpgradeSettingsBlueGreenSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a22fa033c158b27d69c924dca9fc4dcdbda6ee57f888e0b7b9cb1c783cdb0ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "batch_node_count": "batchNodeCount",
        "batch_percentage": "batchPercentage",
        "batch_soak_duration": "batchSoakDuration",
    },
)
class GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy:
    def __init__(
        self,
        *,
        batch_node_count: typing.Optional[jsii.Number] = None,
        batch_percentage: typing.Optional[jsii.Number] = None,
        batch_soak_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param batch_node_count: Number of blue nodes to drain in a batch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#batch_node_count GoogleContainerNodePool#batch_node_count}
        :param batch_percentage: Percentage of the blue pool nodes to drain in a batch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#batch_percentage GoogleContainerNodePool#batch_percentage}
        :param batch_soak_duration: Soak time after each batch gets drained. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#batch_soak_duration GoogleContainerNodePool#batch_soak_duration}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfdea5ffda802d3bbb187f7224742a81e717e91a5ac5633bd713ccf96777649a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#batch_node_count GoogleContainerNodePool#batch_node_count}
        '''
        result = self._values.get("batch_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def batch_percentage(self) -> typing.Optional[jsii.Number]:
        '''Percentage of the blue pool nodes to drain in a batch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#batch_percentage GoogleContainerNodePool#batch_percentage}
        '''
        result = self._values.get("batch_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def batch_soak_duration(self) -> typing.Optional[builtins.str]:
        '''Soak time after each batch gets drained.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#batch_soak_duration GoogleContainerNodePool#batch_soak_duration}
        '''
        result = self._values.get("batch_soak_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff7dd6f6285e246eac4553ab4fc1eabf036ab80023078edd608b44cfbaa3bf3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d914daea192bb1843251981f75ee70598065a4a112a213960d48dd358824e146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="batchPercentage")
    def batch_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "batchPercentage"))

    @batch_percentage.setter
    def batch_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__150e87eebd1e95c252804361d33c7a1e54ac7496da6382e90fc5d0f4fb80b9ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="batchSoakDuration")
    def batch_soak_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "batchSoakDuration"))

    @batch_soak_duration.setter
    def batch_soak_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f850a3f97a53065baa853ce3d75553b3b1865f6ca8bae624609e41ff81cc30b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchSoakDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae4472d403b2b910e73b907304d86a2587537c5fa185b9e88b2681be791bce06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerNodePoolUpgradeSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerNodePool.GoogleContainerNodePoolUpgradeSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e9cbb60d7267d7b5aad81fd5ac5f26206942d6efcb21601ab3851af01f971c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBlueGreenSettings")
    def put_blue_green_settings(
        self,
        *,
        standard_rollout_policy: typing.Union[GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy, typing.Dict[builtins.str, typing.Any]],
        node_pool_soak_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param standard_rollout_policy: standard_rollout_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#standard_rollout_policy GoogleContainerNodePool#standard_rollout_policy}
        :param node_pool_soak_duration: Time needed after draining entire blue pool. After this period, blue pool will be cleaned up. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_node_pool#node_pool_soak_duration GoogleContainerNodePool#node_pool_soak_duration}
        '''
        value = GoogleContainerNodePoolUpgradeSettingsBlueGreenSettings(
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
    ) -> GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsOutputReference:
        return typing.cast(GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsOutputReference, jsii.get(self, "blueGreenSettings"))

    @builtins.property
    @jsii.member(jsii_name="blueGreenSettingsInput")
    def blue_green_settings_input(
        self,
    ) -> typing.Optional[GoogleContainerNodePoolUpgradeSettingsBlueGreenSettings]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolUpgradeSettingsBlueGreenSettings], jsii.get(self, "blueGreenSettingsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0a0f76de9420c1b0da4ee7596557afa2b7ab40740872486c60e22a63302386db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSurge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUnavailable")
    def max_unavailable(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUnavailable"))

    @max_unavailable.setter
    def max_unavailable(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8a3c174eaed15632662bbf0c80e1277d7a274d7f9de61c12c53ccd30c0028a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUnavailable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "strategy"))

    @strategy.setter
    def strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e904f0c512e74ca592a65049e65941ad77f8ec9474837bc15446885effa1a290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleContainerNodePoolUpgradeSettings]:
        return typing.cast(typing.Optional[GoogleContainerNodePoolUpgradeSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerNodePoolUpgradeSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3e2aae4f43753f568b0caea8bdc1f1b7a226adcc5c592138e1e5c9756de06a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleContainerNodePool",
    "GoogleContainerNodePoolAutoscaling",
    "GoogleContainerNodePoolAutoscalingOutputReference",
    "GoogleContainerNodePoolConfig",
    "GoogleContainerNodePoolManagement",
    "GoogleContainerNodePoolManagementOutputReference",
    "GoogleContainerNodePoolNetworkConfig",
    "GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs",
    "GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigsList",
    "GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigsOutputReference",
    "GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs",
    "GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigsList",
    "GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigsOutputReference",
    "GoogleContainerNodePoolNetworkConfigNetworkPerformanceConfig",
    "GoogleContainerNodePoolNetworkConfigNetworkPerformanceConfigOutputReference",
    "GoogleContainerNodePoolNetworkConfigOutputReference",
    "GoogleContainerNodePoolNetworkConfigPodCidrOverprovisionConfig",
    "GoogleContainerNodePoolNetworkConfigPodCidrOverprovisionConfigOutputReference",
    "GoogleContainerNodePoolNodeConfig",
    "GoogleContainerNodePoolNodeConfigAdvancedMachineFeatures",
    "GoogleContainerNodePoolNodeConfigAdvancedMachineFeaturesOutputReference",
    "GoogleContainerNodePoolNodeConfigConfidentialNodes",
    "GoogleContainerNodePoolNodeConfigConfidentialNodesOutputReference",
    "GoogleContainerNodePoolNodeConfigContainerdConfig",
    "GoogleContainerNodePoolNodeConfigContainerdConfigOutputReference",
    "GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig",
    "GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig",
    "GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig",
    "GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfigOutputReference",
    "GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigList",
    "GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigOutputReference",
    "GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigOutputReference",
    "GoogleContainerNodePoolNodeConfigEffectiveTaints",
    "GoogleContainerNodePoolNodeConfigEffectiveTaintsList",
    "GoogleContainerNodePoolNodeConfigEffectiveTaintsOutputReference",
    "GoogleContainerNodePoolNodeConfigEphemeralStorageConfig",
    "GoogleContainerNodePoolNodeConfigEphemeralStorageConfigOutputReference",
    "GoogleContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig",
    "GoogleContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfigOutputReference",
    "GoogleContainerNodePoolNodeConfigFastSocket",
    "GoogleContainerNodePoolNodeConfigFastSocketOutputReference",
    "GoogleContainerNodePoolNodeConfigGcfsConfig",
    "GoogleContainerNodePoolNodeConfigGcfsConfigOutputReference",
    "GoogleContainerNodePoolNodeConfigGuestAccelerator",
    "GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig",
    "GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfigOutputReference",
    "GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig",
    "GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfigOutputReference",
    "GoogleContainerNodePoolNodeConfigGuestAcceleratorList",
    "GoogleContainerNodePoolNodeConfigGuestAcceleratorOutputReference",
    "GoogleContainerNodePoolNodeConfigGvnic",
    "GoogleContainerNodePoolNodeConfigGvnicOutputReference",
    "GoogleContainerNodePoolNodeConfigHostMaintenancePolicy",
    "GoogleContainerNodePoolNodeConfigHostMaintenancePolicyOutputReference",
    "GoogleContainerNodePoolNodeConfigKubeletConfig",
    "GoogleContainerNodePoolNodeConfigKubeletConfigOutputReference",
    "GoogleContainerNodePoolNodeConfigLinuxNodeConfig",
    "GoogleContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig",
    "GoogleContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfigOutputReference",
    "GoogleContainerNodePoolNodeConfigLinuxNodeConfigOutputReference",
    "GoogleContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig",
    "GoogleContainerNodePoolNodeConfigLocalNvmeSsdBlockConfigOutputReference",
    "GoogleContainerNodePoolNodeConfigOutputReference",
    "GoogleContainerNodePoolNodeConfigReservationAffinity",
    "GoogleContainerNodePoolNodeConfigReservationAffinityOutputReference",
    "GoogleContainerNodePoolNodeConfigSandboxConfig",
    "GoogleContainerNodePoolNodeConfigSandboxConfigOutputReference",
    "GoogleContainerNodePoolNodeConfigSecondaryBootDisks",
    "GoogleContainerNodePoolNodeConfigSecondaryBootDisksList",
    "GoogleContainerNodePoolNodeConfigSecondaryBootDisksOutputReference",
    "GoogleContainerNodePoolNodeConfigShieldedInstanceConfig",
    "GoogleContainerNodePoolNodeConfigShieldedInstanceConfigOutputReference",
    "GoogleContainerNodePoolNodeConfigSoleTenantConfig",
    "GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity",
    "GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinityList",
    "GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinityOutputReference",
    "GoogleContainerNodePoolNodeConfigSoleTenantConfigOutputReference",
    "GoogleContainerNodePoolNodeConfigTaint",
    "GoogleContainerNodePoolNodeConfigTaintList",
    "GoogleContainerNodePoolNodeConfigTaintOutputReference",
    "GoogleContainerNodePoolNodeConfigWindowsNodeConfig",
    "GoogleContainerNodePoolNodeConfigWindowsNodeConfigOutputReference",
    "GoogleContainerNodePoolNodeConfigWorkloadMetadataConfig",
    "GoogleContainerNodePoolNodeConfigWorkloadMetadataConfigOutputReference",
    "GoogleContainerNodePoolPlacementPolicy",
    "GoogleContainerNodePoolPlacementPolicyOutputReference",
    "GoogleContainerNodePoolQueuedProvisioning",
    "GoogleContainerNodePoolQueuedProvisioningOutputReference",
    "GoogleContainerNodePoolTimeouts",
    "GoogleContainerNodePoolTimeoutsOutputReference",
    "GoogleContainerNodePoolUpgradeSettings",
    "GoogleContainerNodePoolUpgradeSettingsBlueGreenSettings",
    "GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsOutputReference",
    "GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy",
    "GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicyOutputReference",
    "GoogleContainerNodePoolUpgradeSettingsOutputReference",
]

publication.publish()

def _typecheckingstub__f75cf1f4c113470aebc6bebc3ac0bd156d49a6d1cd6f50e192de6ed4291c711f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster: builtins.str,
    autoscaling: typing.Optional[typing.Union[GoogleContainerNodePoolAutoscaling, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    initial_node_count: typing.Optional[jsii.Number] = None,
    location: typing.Optional[builtins.str] = None,
    management: typing.Optional[typing.Union[GoogleContainerNodePoolManagement, typing.Dict[builtins.str, typing.Any]]] = None,
    max_pods_per_node: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    network_config: typing.Optional[typing.Union[GoogleContainerNodePoolNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_config: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_count: typing.Optional[jsii.Number] = None,
    node_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    placement_policy: typing.Optional[typing.Union[GoogleContainerNodePoolPlacementPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    queued_provisioning: typing.Optional[typing.Union[GoogleContainerNodePoolQueuedProvisioning, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleContainerNodePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    upgrade_settings: typing.Optional[typing.Union[GoogleContainerNodePoolUpgradeSettings, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f572c8394bbc47a068c4bf577944599f603d50621320dce758bec0dc25b02408(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81585b084a75592c5e3706d4af74e68f36aa22552975bfc892fabe709cd68a93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c48c4bf2a2e4b93438ccc44e9e308390e16c2f93480729af0864bf8fcdb7794(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c61929a40bb8705acf4362b8eaf62f2baafd7567509c759af365e149731a020(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__704c1758a74418784eae7802f36846db75082e7402be0ebfa99e848d7f40c078(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c02dee5f56c3abdc39bb4e8bff7e7810c84b6b802fc3ad1ed11a0cdcd53bc2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415f2d44014be5f55268a27092218cbdfa10c6db46eff6f23725b42d3d7b28f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d9c0c424628c611ef7cf1e04ee271b3e5085940c2d1ef9a8ee6ca572735e77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80ecfcd52d0067562ef6c905b0ce3c1cb7dce917af196328f8cf80bcffb9778b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__816e68d06296456ca033c553ee6656cb4a59fd19d5e07d2fe98f8620fab55da1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfed50f56cb91855a1001533be060dc5ad6cbdd28d8308e6734de92794386f47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e6080263da48bee69e742df775d7961bc11f1f69da78eca068c2632dfa54a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62328d6aae5eae7f3d514da0e78b03c79612e2e5f431951301ae48f85e56bab6(
    *,
    location_policy: typing.Optional[builtins.str] = None,
    max_node_count: typing.Optional[jsii.Number] = None,
    min_node_count: typing.Optional[jsii.Number] = None,
    total_max_node_count: typing.Optional[jsii.Number] = None,
    total_min_node_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea6e7409413f0fc48829caa13d817fd8015042db5fadbbbdfe306cc470b16230(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c15ce7b2fe3ff14ba262606cf60c325f83fa6c6553f7be2686039f8ea3b0f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91f7cb34e10e8a57ff9e3ba6c95adc6369aaf96b12061399856f9f6ace845e0d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487660a99f7c64d19c4190435a15b38388a4da154a4661c594e749bbb6bee17c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aaa234adc7ed238d1b00176d3cad8de2e782a4a36e27414cb0651b7f1f3ff75(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515d47a796a60062d7644cae62cb074d21be87201210aea0c046c701e5540a04(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb9a1cc5dfd72df0873603c99766e896fdbe8dcf5f4aef19ba20980d351b4041(
    value: typing.Optional[GoogleContainerNodePoolAutoscaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea29e6dbff83ef660066146f8c46000f2e00cb18bdc726304a3af1ba3895fbe(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster: builtins.str,
    autoscaling: typing.Optional[typing.Union[GoogleContainerNodePoolAutoscaling, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    initial_node_count: typing.Optional[jsii.Number] = None,
    location: typing.Optional[builtins.str] = None,
    management: typing.Optional[typing.Union[GoogleContainerNodePoolManagement, typing.Dict[builtins.str, typing.Any]]] = None,
    max_pods_per_node: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    network_config: typing.Optional[typing.Union[GoogleContainerNodePoolNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_config: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_count: typing.Optional[jsii.Number] = None,
    node_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    placement_policy: typing.Optional[typing.Union[GoogleContainerNodePoolPlacementPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    queued_provisioning: typing.Optional[typing.Union[GoogleContainerNodePoolQueuedProvisioning, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleContainerNodePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    upgrade_settings: typing.Optional[typing.Union[GoogleContainerNodePoolUpgradeSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf662b569af6c32395030e1a62cb8531d6641c45b30b92fe348b218de7658497(
    *,
    auto_repair: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_upgrade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aab11aa58f47591b5a7f082a3b5abeddb63a02a365fb84966dc36fd6654a8299(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__435f8fabeac9592a57908302f97e6e5268f60ac9d6b2be5802a49cbb3debed1c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29fb9077729ae66d34d07b367bdea13e3cf79db36d53a7e0cacac9fb3106dc18(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed1eb8fc1eb08adaf661424db47ad79f9030d9dcb8d9e913a3c3c6f7d8f41ad(
    value: typing.Optional[GoogleContainerNodePoolManagement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eed8a5d314ec03f5556cab7d069325b6923f0374080c64eb741ae1245cb45d5c(
    *,
    additional_node_network_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    additional_pod_network_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    create_pod_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_private_nodes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    network_performance_config: typing.Optional[typing.Union[GoogleContainerNodePoolNetworkConfigNetworkPerformanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    pod_cidr_overprovision_config: typing.Optional[typing.Union[GoogleContainerNodePoolNetworkConfigPodCidrOverprovisionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    pod_ipv4_cidr_block: typing.Optional[builtins.str] = None,
    pod_range: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69280f8038f3e51e8decfab988090ac457fee0010e5ebcbbefb7ec971036ec49(
    *,
    network: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dbc237978655fa73187db4c1cb53cf298beb2cbf6d7de91566d61fd5021b55a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43caea3e720458e059950f10eac719b65add90902dc0ef411694e1df0d37717(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89c9167545d9848968422ddca3f5f5009f1224574f3c61e3c483a2154e0117a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e732e0faf6b3be5d6434d2ed758a6e053056b7b25eee45e80a78aad15c93f25c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33525485b76a39aa69c71a59b0a47d8a3225b0cce8d02f8abbab18890cf62650(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3377d650a18991b89da7c1ee629727d221ad09505b7afd80d03e1cea238ef07a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a9864bc7eec4a09677a2ceb13bd9c9845d85639e8e9b75680a064c839385930(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec88a8cef2d916cc004abe9ba36fc7d4637c58e514b1a2bc507a70ecea239794(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e05364612cc35e1ba10065efd1a780aca91de26ac5703a656669ad7f4c8c2d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc237594c9f9c114117d4938da7ae5f55339f7a7a14bc8fed2d2b7ccd78de11e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5593fb845ba5f92e05b5d61ad48e08e12cd9b918b57291b657cfbbfc32adbdb5(
    *,
    max_pods_per_node: typing.Optional[jsii.Number] = None,
    secondary_pod_range: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30b87effd0d5902f3da770b8cd355d32f87a62810aba8600231fbcf7456bb52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be776c3e43cadf916675c7c3c6794e69282987e9bdad6cde62b9fd115c0c85e7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33d13f00757dd726e5258748ec17b0c5e7d827926d21a17a192ee24a639084fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e57a5cf3f32bfef5c73918ecdf6d15914a041422914896f605c993e379547a91(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e2e443223bdb40d4096074806552500ef79c31eb7a957a0ec18e511b7a4802(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__700f3178af7167db355d009359e4445edbe6fa284127ce9b3ea62cdbe30ad863(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4ab55a5e7f7e4d8967218001377ebf143102e568244c569cf3da883e008332b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68485f3f826542f88d5fe8f219e2ba1ac59b06832d839b7dca15d036ac4cef55(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a63badd02d3fa89586d1a7cd8e1a70f7f6071a665a32990e03dc847eba08d349(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c61703f7b2adf52e48366edc87fa29da1ea177fe23a1b1aa566ec7f268fa5468(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce0581388cd88fcaa86e8cc85e21009cb53454163502c68b4c71aec5084a3b9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45fa85b320937fd850dad502f53a6152a77ffeaa5054e33350415b99ae55f6c1(
    *,
    total_egress_bandwidth_tier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e70e06fa6bf8f3116f05b8ec596f09ef579afc5909cd75076b475f3b8414f4b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40b936c3ed15c3bb7876b8dd090cc4076e7fa252e989e019e57cd4f5d35f2fa2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55ffa9eeca72d8ff6f31e6e98f605fc5462980acbc7f199d24432f294c963cd3(
    value: typing.Optional[GoogleContainerNodePoolNetworkConfigNetworkPerformanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ab47c099914e4d193e3ce84817fba39f48f162ab5d644a8f692b1135d4eb49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d420e8ad7ee17de5d595c8f83097687c3611ebc66a78ed7578bdbbc367b92616(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerNodePoolNetworkConfigAdditionalNodeNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e3b1f27f5b41acdf70c95a775856332922d21efab06465f122bae94d8033670(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerNodePoolNetworkConfigAdditionalPodNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1508f8ee2ce08b8323c5176b5638d953797d29df6548da0cf78e3e321de31b46(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14a0cfca3262e83c0e154372d222247345ed04f4c2e2266f03b60acefaba6d3f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7579b112e2f8956c9323cbde9c6225ba942280f541f9a94cf18adf7083cce62d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8bd9618d182a54a7314488aeda425a360a6040213e325fab75b28b3562ce8bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dede1c406015eb91bc1ef6b774a5c323f0705bb993708882c958e72423c6e2e(
    value: typing.Optional[GoogleContainerNodePoolNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e36914cd390f1683b1de7950c1106aca4c170f1b24808fedc3448a1615cd2ac(
    *,
    disabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d9ec034c869ca44025d8c6cb9c37e33f9f1ece8bfa4ac9cf5b0028576c5445a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__808f43410d2749934f7749b30fbe673b324b5e7d0c2668ec9055c888c41ef148(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c394a27920b53dd332d5a0ee1f7b8beee652a57f2f6accd4e88ed27204817b4(
    value: typing.Optional[GoogleContainerNodePoolNetworkConfigPodCidrOverprovisionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa1fcd02cbce130e12742899615c9eba8ee7c5fbe33fdb8aaf3b5ba306a4073c(
    *,
    advanced_machine_features: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigAdvancedMachineFeatures, typing.Dict[builtins.str, typing.Any]]] = None,
    boot_disk_kms_key: typing.Optional[builtins.str] = None,
    confidential_nodes: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigConfidentialNodes, typing.Dict[builtins.str, typing.Any]]] = None,
    containerd_config: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigContainerdConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disk_size_gb: typing.Optional[jsii.Number] = None,
    disk_type: typing.Optional[builtins.str] = None,
    enable_confidential_storage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ephemeral_storage_config: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigEphemeralStorageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ephemeral_storage_local_ssd_config: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    fast_socket: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigFastSocket, typing.Dict[builtins.str, typing.Any]]] = None,
    flex_start: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcfs_config: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigGcfsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    guest_accelerator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerNodePoolNodeConfigGuestAccelerator, typing.Dict[builtins.str, typing.Any]]]]] = None,
    gvnic: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigGvnic, typing.Dict[builtins.str, typing.Any]]] = None,
    host_maintenance_policy: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigHostMaintenancePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    image_type: typing.Optional[builtins.str] = None,
    kubelet_config: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigKubeletConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    linux_node_config: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigLinuxNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    local_nvme_ssd_block_config: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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
    reservation_affinity: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigReservationAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    sandbox_config: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigSandboxConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    secondary_boot_disks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerNodePoolNodeConfigSecondaryBootDisks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_account: typing.Optional[builtins.str] = None,
    shielded_instance_config: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    sole_tenant_config: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigSoleTenantConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    storage_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    taint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerNodePoolNodeConfigTaint, typing.Dict[builtins.str, typing.Any]]]]] = None,
    windows_node_config: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigWindowsNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    workload_metadata_config: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigWorkloadMetadataConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b84ff91dc1576bbc9fd54614b903df3470b664e8a73f1347af0ad77800bc5135(
    *,
    threads_per_core: jsii.Number,
    enable_nested_virtualization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95636e02825a991f3f7147686878ebe9b25d0c3b188f89a60c85ccb4614c1853(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca58f258a30281aa3abb57e3578ef76d20525330df9feb8cd537c6a1df05930e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74676e8c91979e708130a472a888ecbae89c91d55b6e1369c462dbca994020a2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__889cd7e2fbed6269f4eca69f0e7c114ef45b06d265915c856e49d22849ceeecf(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigAdvancedMachineFeatures],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e772158230d40c8289e54ed2cf966b3b6ed2bd49b0788aea9c7898ab80c90c5(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e75312ab7191a22e2f0dae63aa9d8ed49065876708a96436bbb8f4d2e6e9daab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c98bf71a2c437d0181cf3ce3f859e06d5abb4ff0de4bcf9b1fb31db161b2d3bf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9339a3ce0d429e8193f318d4eb35a45025f57161b4a4cc2a64c1be4ae3dbeff(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigConfidentialNodes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a43bebb0711ded537e3a7ede439858aa9cfee81c49de3d3a537163d5e1a94805(
    *,
    private_registry_access_config: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff8c6628f23731394b34903c900df9763bfc699b672d555ab7cc1e105d6a315a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9937b64dcde67eefae955c9acdc2935752a7923e32842dd9e7836320e85dd798(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigContainerdConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a974befeb0377290bc4c276ed50036d9ebcfd6641d02653a1cb5fd1d6178a6f9(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    certificate_authority_domain_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ec4f0c3a07dc34da3cb7aa590b600000f24baa12387a982cb48f20e92787fc9(
    *,
    fqdns: typing.Sequence[builtins.str],
    gcp_secret_manager_certificate_config: typing.Union[GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466e4701426262db50e8ff5bbeb6f359e66e66becb055f1f2bca2ca47bd1dd48(
    *,
    secret_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16d71637a85eb2fe9ec4bb2832e01946cd19bc59bad975c9ba10a99e9dd3aaf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f914fd5274a8b60713b0c5859ce1e5dff13e79050fca30d439f9222ac0fc3eaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac111ab21bb21914f6119325dd15aa3200ab844e824d32e714f9a350da43b1b3(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfigGcpSecretManagerCertificateConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e1c921d36aaf4c46e9515491c6f765825d743be1d465031b7d12b5a7f521db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0242325c6782f508a29a8abee63feaf4a5727b3058662d5cec8850766e18e70(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3727e3034bb9bd85399e5fb42671139147214642d1a60a2f4b5608c3b8b764b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfacb15e926de2e37528cc45d92ffa78d11173a4d8bb2e03bd2299d80d41f9e8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a938e5fb4749aa774aa2c25e18272ba61c91de2fa275db34f5319d3a256ea6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d791b795701d46eb922a38285e9caa5295ee90fcf4f160dd4946fa26777ac62(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__972bcb668c0f1a391b2196a8c21d57fab429c6ffc20bf2017bf61bd6a92a3dd9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0be6fc9fe6bb048809b597a9523d273463ff528cc0f2b13c369aad8ead3d9ea3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__756f64b72271cd969187273600a5b04f43756bd6fe059e2efa6386443aa5ac2d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b421de9f82bce237ad088da2751981978a8d54b02e52b7ebe8358a4f6b16051(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63fbd198b2ba3669ec42f7e098e7efe8596383a68938cdc75aa30daac98cf6ef(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfigCertificateAuthorityDomainConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716843f2c42276bc40b79b33613227a1ed7a370e24379e7f775c4600d3e0d14c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__340b4b3379685fbba5a62e879ecb2adb460b5296e2b6168e053269967718d910(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigContainerdConfigPrivateRegistryAccessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aae321d3edcb049a5eef6207aecab51f9d77932da92a7420d8b3d5472c29af5c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d761a908436f3791ed08607f2b1c4e34f4428bee7012d8142e910884c8eefc0d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12044e40aa7a5cb7b4d7438cfdd039d17d26533c766d68638923550f6df5835f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23d360dbd5278ccc717212f7b58dd2f3c56e5905a56e37121c86cc015c736f83(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020f4fd06c54d6b3007a007011d2d7ec58cc9cd1f9dd028756096bcda31da8aa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a08cc90ffb4cddd61b06caa0d9f8d3fd52fa75a66d6749838d7831ae04be16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c3dc61f11a88c4780b3b01acae8e5921a09ac9889ee15d0d3793d4b6c8dedf8(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigEffectiveTaints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e4de41b3a5eeca70b8a075b44132986bb2842de83e958f57914380eef48945d(
    *,
    local_ssd_count: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__344c60f8b220c63426f707c185c087ba749eed3c7c69515f211bddf3ef036e85(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__019b87e238833b05dc5c8fdac2040bebafbf42a3608f08329418747f6eb82e8d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b4cfd6ade39b17c0cc0b5cd8ea7c183a365615a792af8a143710e1d207dfe4(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigEphemeralStorageConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f86c06e6e0824c95b22931800efe52d61eb7a619796f9ab47acacaefd1e8ad(
    *,
    local_ssd_count: jsii.Number,
    data_cache_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c361a910c4fe586ff79b5e408ab5d99f937b3fc0a7eea74a353a81482e3b257(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ee53ced7c9d38407f3caf403b92c30c542ed4c0f89d766f281d8b32fd98f1a4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de62d4e33dc77e39b64c35b46020212d50e856c27edb4ba24487711d0c823d2f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__766060da06bc707692bfb4f199f52c714ac03d1943bd05bdd4e6cd2e49956ed4(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigEphemeralStorageLocalSsdConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09299d5aca2f4ea2902b5fe7e75bf014ca9c6326a178e4659f8aec0478a7918b(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc6af57a173f3f7b49718b1c45a17069e2365faf88351ff610bd53ebaa071a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eeed41022c11a8abceb7919564ba6510edc2e726952303b1dafe6399016f577(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f99f21a5402d0a5f02efe77ee3b1826f95ac2cd4c35dda7f1c3943ed327d005(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigFastSocket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1b709504c119dee33ef8ff6ab54d0395563750ab640de101fb3ead0f8d935e9(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e48fa4e7df987f256ed87baef93dc10b06d7f67979a84d114596e6e99b251c37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da39bf9303463707f2509086f4cb45679818c58710b7099c3d8405facb33cf03(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20727639c6efea9f563e4281e2802bbc316b01bd4f3541a4b0e1bf5537eecf2e(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigGcfsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5371a78d3348f7984f3252a3b413a231d4d0d94d0af67d13539e315d1941f3ce(
    *,
    count: jsii.Number,
    type: builtins.str,
    gpu_driver_installation_config: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    gpu_partition_size: typing.Optional[builtins.str] = None,
    gpu_sharing_config: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da24334c663dd4353d24e2d2007f40b0552c1cdf3681de6d4ec103127ea6090(
    *,
    gpu_driver_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f8651bd3cd1d2d27d20eeb3a0efa9312d870a92c6f67213efba17d51d027947(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6c467a966c9248fbf3973067980f92085df54d653eeb05eb6fe8f1f2890d56c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553888b672e1fc75c764972108f7f8f43cc4337a0939d958ebfa82c8f188512a(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuDriverInstallationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__681761950d528de7826057d9ef1c2f105d6ede87838fa1e6c8a4d24479466885(
    *,
    gpu_sharing_strategy: builtins.str,
    max_shared_clients_per_gpu: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb760b365268447fe30cad3acfd57cf6c28dcb846a40eb7ee790c19e8a668024(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db7dae7e97c577e68472b3506cb4ecb4c3d191569185d972803008ef790eb5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cdef1c0518a7c9fdfde9088b5d7ddd782a3196c57ebb9fc8628a5711c824547(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b626e52af88754879d936808df10f9ce6fd33cb3fc20fc36b1f049bd8a27d3(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigGuestAcceleratorGpuSharingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd296edd6212e1afff0426f1b33eee419329d7f930e96bb23c33f053351f5ef9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d6be7ca89367e72ecb1910247d2e24d9b35b970887843cecff78cd31831680(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ea263de560bb796241fbd1b0e58bf4605847182743e213dc72216ee43af68b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a0134108a27f693ae7d8fb8cddf87d44fa8bfd0714e153df56890d98d83eefe(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b392f148eb02a59634e2119dbf341fd9b17c7098d58097200b4d2ec7150db008(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6525e8399f8fa6ced47f29d699211eebeb5f8b114df9b7a05649df8c8ff2bc21(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigGuestAccelerator]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce672a064851ab01a2bb45f73a5243a5686380cc0bff14f08e506404a46cfc7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f02a0d59b4e0d4f71412b0fbe11b32913e0729875e3ceb3966acd60f13023d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b9ba13b7c6bc01e03cf3e8f07c920e343308d293a0fc5d618174d757c60175f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ec2dbd50590745f9d559e0e173dd0bc81d1b6c88a1c7d2e7e95018d4289df5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3250a4ba2d60a794d39355578b33a5271f4f826cb6e0d3a616c68298132b3013(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNodeConfigGuestAccelerator]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a784eba60afd6892f06ce6edd56de6874823ff2cd61e7ad7a3102dd310100cf2(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a0d7ebc71ac66550adb434ded1f0aca8ddcb306ec0f62e42d97b842a24de60a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ca809342a91d202196945d7a5c097493b8a6e576ad3ec0a6b9fe3572f33b911(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c85b741cbf8ae3ee9473ebbf2343cf8d2efa077678545556e8de91d7b4f628c8(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigGvnic],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fea261c59267508d57da1d60973390de92bfd8fa666b533e957db8798e003a8(
    *,
    maintenance_interval: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e294b60cb695c1064a7b0dccaa42c55225ce9a4a3ca20f2b5bc81ce09ead58b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea0fdc56e1f35fa91e5526f32ae443f351182ace719ea7b30eb6d55b29947f60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e124a8bf2eedaf03e11fbdcc5941ef41edb97658beb9b724ba12258ff7f7ae5(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigHostMaintenancePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34db26051499479a18ff1e6dc64f594f6dcae2949fd17e7e3473c9b06d80726d(
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

def _typecheckingstub__c6d0bf9edeb1c08edf2cfe8c2355ac0d7f0beb7abac47803138a966c6bb7be8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a166da2a964d885deb0c3f8bb6d4a9c0db4754de8b057d45da983ebb91a65b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9edf9633ad8f6672d81a593b24d63bf1a5b6e94da47015b1f985507f966f9de(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f87b5305f80f879412d270a3d8a977c71bad664f4dd503d70c6f3ece16ee216(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d6c6d46f20646f7da20479d097f77be95fd7ae9a5beb7af3e109cf2406eb758(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0fa442bad972a2c29cb7b2e17328a1c0828f6a2fe63e66491143b4d5f6599df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d56e058197a0ee50991ace50fac3578496896e48e24a819597e69b49bc730abe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b635a1655dd3c7f80454cad4fc7b140b72f7c08f9b28efa7d9db291e352f523(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb4b1689a8b33903f23bb9184a497b1d7541bed7cf33f027dc389fffab789c9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177beda3c6285c1952bf24787c45253e10f4f22cb47278be0c085e34192fd857(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c1668cde7b6dae6f95ff6ef5360f5e37dabd4b470ab7f1bde4091894d9c3ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff613003539c9e2c8a5e980c0a69de5421ff3c1cd29e3c2a1706a9277a70b899(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07b7fc19584ec3afccf323cdbac7515a5e6fa1b908097cb4bf49316dfd0b080c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30880a0d548ca19268a3873ba14d341efcd3daa24050f2dd7826b406e5d0c89(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigKubeletConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a712ff524db4e52be373615e9bd7f1e34a126a9685238d1ef0a28b04661f4da(
    *,
    cgroup_mode: typing.Optional[builtins.str] = None,
    hugepages_config: typing.Optional[typing.Union[GoogleContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    sysctls: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__483ba27c4de3a3f4602022a1b9e1bd31df133a46b0d9df854d86c5e595b6b52f(
    *,
    hugepage_size1_g: typing.Optional[jsii.Number] = None,
    hugepage_size2_m: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9ebc305e946a049e1266fb530ae4c8e942e47aea6c4f5810d6637e2687bb24c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673533f6bb61e6cff3ccc4fa1b5a6e9f7eeff345db656f7ec107bb60eac36671(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f67c2845221212d51b3383d0afd530ef4c62b77c27b14e4b7cae4bf17a318c0b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262a8af562c55c73b9387c010e46688deda86596d66b4da96be84756542b91ef(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigLinuxNodeConfigHugepagesConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4478269cb6a32f3df965ffc117217f6f41204ca47b623cb874c6d5c106c2cfce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fcfad400ccd7c53572778f369c6725e83bbe8f077b7adad29e0296ff96b6f83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9919da74f17a45705ac745cf25042d4fc5962c02aa38dfcd13375668fa424b1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a3daa46502f797d8e0408b364a42d8e8374bd42fd5bd93306d52f36c97d2bb4(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigLinuxNodeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b66f8fbe3ccad3b2c26fce5e237aac42e3bc074d8f82d5e1f27974291c0e1e6(
    *,
    local_ssd_count: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4174179525e1718955c4632684e87241327af41738c23b2a82c322e4aa774425(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e2c25315c97caa3ba9207c9e1f197c9b0b356a05319ec7ba9e4d07461ab957d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__396b99327534902cb3bc9a74734f9e0988397785d403ef117fd30c83f23fefd2(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigLocalNvmeSsdBlockConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083a2dc299fe6145c85bfe549560b3684f3c8c908254f492952cf089b05da164(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__430914745b249e68eef82335fa5df4f1ec0f5c9c715cae42d0ef9564525c8856(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerNodePoolNodeConfigGuestAccelerator, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607b7584cce2a4e32ed18d742de21f4a5c502f3e1869442b45ee5a1ffeae3b36(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerNodePoolNodeConfigSecondaryBootDisks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fc7a8e8b61631a29f9319151abe11b15733da3854e6d474ad8a514e2097f3d0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerNodePoolNodeConfigTaint, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e682e5865c527f5cb6077013cf771e1c350c2b1174b3fe861a44dd2ff99df6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c1fcb99d6f2f8b5faf70392de7d0e5b09973cdf838da97b37a3a66bfb3f0573(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49cd5414ef90e98e356ed3fb10d95c614d01096c1780d1bccb8960bde4754c0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf7cb0d8f198ecbca817aa93c50b649d29b997b0c29d4014caf92341f45ca95b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c45ad485fecaccc24fdc70364be932e222c9504d067cf0dc214c8581df2c74e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b7af0a4f9d15ba8b06f0307f00574b87fc4a24cfea1e2b9950ca456d2e8698f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ed1fc1e97d24235af2e23f59a2313b73a795fb82e35f86d683adba3c93603ee(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd31ab7a7ed6e9b548d8610df0a3ad2e2746ae21d1e6745adef23db664b3539d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9327250830f19920e3b1ed2d0186c95986730dd8bdba5fbc3181b332fac8c10f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d3be33935e83a6a3021fac7f119be8890231f4e5008bc3a448464d3f1889e38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a5c3f62da835a37b7f31b5e4518552a60b06fd62f4f0c26551bb26ced75f5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__141ce6abafa9b018206619b69036d7a7510b556cef1aae13bed8ad91574d30cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ec81278e703260ace9aaa7665336a977da1a7214164dc04592374d584f44936(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88e24168b227957a66c71c7055f00119442e623f067ac50714a98c20b24419f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2dc69c0db50ecc53a733d01bf1759316d86abca0884cfbfb2f525fe60a54f77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ff12302b86f1fb4480f4e08f109c82bd19972d642829c4338aeb99095580c3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26b2d8bbc6b9ee59ee1c0371c8927782bd89d1e227d9ca9348a07c938e0b1629(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__005c0f9f55ae67b0657c42b02946f51251557548c7dc54d8e85a54c84fcb2af7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9309a54b4b3e7fb2073b67916613c8bdcb13b3bdcf528fd4e5b23b4346344550(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f76c8a79c7be3e64990423d2732776e857502e27101127c6a64471b583f475e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a4da15d6e027e9d872b5f17fc10a9f77e4a515bd19fe4c4bbcd1ffb4fc408e0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c167a57fcbe581a798dbd82110ad6043956138466a9c2e86bf2f4cff265a404c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__172219d24714c011f42cf338aae3f37088bc119a31c76d00cf9d6c41ac217c88(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17c3310f67f012f91ac82a292866e11ef88825d77e88ffc8b2f255c98a5949a8(
    value: typing.Optional[GoogleContainerNodePoolNodeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4da75a11d74f34a2d86b26a212ef59bbd6ba8b2d25fefa448a97b453892b385e(
    *,
    consume_reservation_type: builtins.str,
    key: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__170f0f021381907dbd31821afbf330731a41418450daac7a47860a9ebf6db740(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0a63dd42155c563d781c8d5971df716f889a9bb96fddd2d06695fd9aeece75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc6bed937ed104aa55beafe6dfc3e9ccd423a6ef60082de6c1f74f6f2bdc3840(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a73ac024dadacc137c35e153b21d62269c06d82418a5c3e461057ca2f8201e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f01c015db06843e7ee7c3a12a5c88dadf2e09e1909d1229f0471861874a3ae0(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigReservationAffinity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d5c575f7ae9cea24a8a831a10c5e8a5e52e78f25b2f52987ac889ff8b42c7d8(
    *,
    sandbox_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f904bcfcc6edf5f3eea0738fee72edf59e1705299f0496d408a9ff62e5b372fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01867d97bdc00764faf098c67627d1c7583763414db4169bd158606a719808eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5d8485307675a141340c8478c20b45ef37c503c7e29f2171d65d55e88e91c3(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigSandboxConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a3ca0b39fabc6d130717f1708a3b55fcb47e12d98b94a845a55129b6b3f5a47(
    *,
    disk_image: builtins.str,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b982b10c4f763a45e6c88e59bdb22ee990224b0633e68a93fd8ec75914e7205(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da0b7e4798acdc0c8dbf58c0d54990e7d91d76796279cdab24261c8bbd6db3f6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f6cc20380e8541c7b217f6360f43202fed67c9b78d16ec143ca3d0ff312af2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c6c88014b678520b79710b7d3e64b9996f7b41fb97a4aa4d1c38b8658cd9cb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140f1455cf46e7ad63af9df7152f0f605d06d335ac1326b8fda7c6d2e98422df(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e454f9fcebde51425137e024ed946d454b4473579f11423414dbec233ee29e6b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigSecondaryBootDisks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89841b581e87fb390179ab2a6835a8e3f599b119e4cb03d2be693988dbe412f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__992ef694e206f5602a3892013f17d817d43fd1f90a48c4a934c2ce5e092a3f87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d263b650f230b10a2343c98010c7ef28dadc7d7480d3e5c855924f0250cd2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2fa049bc34c3c7d456cf9b330dbf6a214d82d76f7a7acbd02f1248410c1a183(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNodeConfigSecondaryBootDisks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d30d3e12add344b754741b55e899c279f80b43f7669599fa42aa919b682a354(
    *,
    enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__074a8824f4189fa0f3b487e51506232a56c64c138a54423f52de07a056d01695(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f12be696c4d1eb3739c5329fc1f57d52002af8d4b1cfe401e10b79038f59288(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92f10df846228f3951c9cce63b82187640b521dc7cac4a829bac6ce1673cbccf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c89a29e3ff2cdffa5769dda9a58b9ff09afac4ba2712fe83ff9d0274a5a783b(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigShieldedInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ae0478176e7f4db4874d07c18ecda7da528b7dcf8c5ea47cd93b73940b34af(
    *,
    node_affinity: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f94a27766ed8ae1f268d91b9c0c6fd2fe102a573dd2a5b5ce130f7a803c8ff8(
    *,
    key: builtins.str,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7670aa0f12a38aa50a41ba2c640b818100f96a5bbda51932c3e203128f6a329e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcd7a0bc359eb767524376584aaab28d53d272e507f2699654b40b48aed485ff(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbe8732ca367f396ef0bc89fb325ad97e19a4fe0894edd8ecf3e926622f25309(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ee7398fe7ebf9b55c3f7d11296fad54fb766b8808d9a3ac712c00bfcfd1ad4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf4484bfba9f3edf02c9a1e0183b3c56acdc6e7242548c786c71673fd4a42445(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f94989f89038738e89407086ec36b932936246cf4f9afd7e1a0b13e861a16966(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e047c539401fdd0c78ce873cf463fb13df628af472acb82fda4eff0adf2a8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc015749f0b85d684db8f87007d0a69ddd11891d3eb83f8613e7b122d9e33114(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d017d1668e655493881644f92e0ebc8b88ca77e6c74102a3515608dd3cdcd93e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad165a94965ca741be15811e1c747e2c4c4d790e57c006a9221981161f2d237(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fcab9fe9bb8960165d3f6e72377292ba85b38f05fe089a68c65e52e934f03c6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140b10c29b444001cb277fb271d98c1ef9d7e39f32d3e4d84485e8db9077a8f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21767b13a87e7dc8096154d7137864b56590652918328787a56643df8e70f3c9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerNodePoolNodeConfigSoleTenantConfigNodeAffinity, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c183a5c2ffe21862bd9d528949ff1a6c4c1688fb0b1d9412956583c9d43e376(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigSoleTenantConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__224f81127254286dab77b4de47c1b26ca36daf23b5392f6fc288c9950e5e0749(
    *,
    effect: builtins.str,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61b5c54ce78178bdbc708afadf1345f2840914436d975a0a2a5d9290c1d8f4dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13320fcdeecd7c12e1b64d7da141bd0c2654a66f65ee4a0bb8fe80b2e354834b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5a518fc02367eedf6091f8e392af22576dca52e112c5d8af3c729b193974c8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e3a8a32400b4de02b639ba4fd73b522133b6bbba25d2d8eb12b9173863e72f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d73f3ab06b109825a617fa3c0e0708763a56b6dfc99da76cde7c2a30c8885d4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487c4224289a73764532f09c809e9b861f987548be9e77f7b649dd1fd952b32d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerNodePoolNodeConfigTaint]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2563df036fc207ba1c691a321907288589907b1317b84369decb79173487458f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed24bb5735290623c794efe56d216076fabc2dc99fc59d7a7ba69ea53dfabbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cac8133b2281a075a450179ee2621a4b67297454ae0e1c38486dc9c3420ce7a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d86242c967062aa108f0cdfd603457913714ec5e4f9fdc3a581d1562be2cf494(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61614be0f0a57e9f3a0934ff5bf9c0c841e2a2462492fbdbce76cfd1993a00eb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolNodeConfigTaint]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41a5bf48cb6525e6525b18f21a989b089f8ba7491c8ad505113941344e508275(
    *,
    osversion: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a6923790be3e6154633450f6a430f525fdb107771142804b973abb988e222cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb26668983afea395c57102d0f30e4b0906e582c3751a68ed1f4ed08d3f40bcd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__874b12cd5a1201bb9e8edc06556fa2f994ebf0488bf364d5f49bf7dbb5d9f8a7(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigWindowsNodeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b83ab657230f1126004d64d5867a5f41647747550c6d00c4e9ed4c0e2050f56(
    *,
    mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdbcb7e4fd2622518c403b6afdc63db8febc2d492867510537dc11868e123155(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__756f7dcf18b7a5d4e0f183746c7731145bc8035f07c5cceb75fca59e40a71029(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08ee79e7c3b541b59e59c16bdac5ae15619c863bc855ca42c577d530dde23f60(
    value: typing.Optional[GoogleContainerNodePoolNodeConfigWorkloadMetadataConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66829d3b46e9e34ed947a48c35f153bcb2495c283653c64d6722bad05fa65f60(
    *,
    type: builtins.str,
    policy_name: typing.Optional[builtins.str] = None,
    tpu_topology: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b047ca53213df25a4d17647a6b862812aa7a87a2abb1832a1dcc198c4d934c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9a332c844b1093c0a6b10089321ad0c1f47d2a4899c18f90bc4f582338c60f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9efa69ab76af0c873f28b0809f41177fde16af0bed222e58c5f61d7576370d45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43fbe4b3dbdd56b027a35c3c1b3c90592841311d6cdb068468ecc9d0c8a0624(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd5a443fe462b4d296b11941668ef312731e9d206548caed64871f0ef51b2a6(
    value: typing.Optional[GoogleContainerNodePoolPlacementPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d778a088e764622c77b7a6a9765085b0a051d37e7519385b82979564bff8c8f6(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acd21d276258e05b48553b20cf8f45c95b214f41f8cc57c1ea8fd1ccca2a03b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f9abb498e4e36f6c64eb0e72a55cf8e98b5b9f199b42d7bb7298e3144f4655b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05201505b603204d09aa115b7d840cd7ece1c16adee349233cbbf75b25170751(
    value: typing.Optional[GoogleContainerNodePoolQueuedProvisioning],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ef94cdeb888213f7213948ef71334530b24d3f312bba6b881e35f29e1149fa(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e39882dbed07a22399e5a8ef93f52663a5fb8fa2971465b8012d7d024c1808f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb7bedffbf2336aaa1d7db42da2c15e62993a9e6de13ebcfe46f1f2739a4f40c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27ac208a79f53e13719db31308600ca0e682bfa817f0e61161640a69b78de3e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88f22cbc5bdf0d5f8e61e1ad1f489a1d702259be99ac0bd10217b5132fbfa7ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71a28ef4528ea4129ad85a8eee4d552fea146af9634dfd6f190a7090d6ccfba6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerNodePoolTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceae5e61bc3cc59dc916e9a682f0c33b5f2ff9c057244f29f173d2f3c781cfcd(
    *,
    blue_green_settings: typing.Optional[typing.Union[GoogleContainerNodePoolUpgradeSettingsBlueGreenSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    max_surge: typing.Optional[jsii.Number] = None,
    max_unavailable: typing.Optional[jsii.Number] = None,
    strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cb7777d935afe680d1432b069a74170722f58d400c5d6bae8cf5ee83193c839(
    *,
    standard_rollout_policy: typing.Union[GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy, typing.Dict[builtins.str, typing.Any]],
    node_pool_soak_duration: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975413c35d8f76a098165bfb01a950161b321e0c75067cc05deacb7b1b885b0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__080f086450b74f1812863fa7749452bd02f15e322c7e52607b7314c0827032a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a22fa033c158b27d69c924dca9fc4dcdbda6ee57f888e0b7b9cb1c783cdb0ee(
    value: typing.Optional[GoogleContainerNodePoolUpgradeSettingsBlueGreenSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfdea5ffda802d3bbb187f7224742a81e717e91a5ac5633bd713ccf96777649a(
    *,
    batch_node_count: typing.Optional[jsii.Number] = None,
    batch_percentage: typing.Optional[jsii.Number] = None,
    batch_soak_duration: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff7dd6f6285e246eac4553ab4fc1eabf036ab80023078edd608b44cfbaa3bf3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d914daea192bb1843251981f75ee70598065a4a112a213960d48dd358824e146(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__150e87eebd1e95c252804361d33c7a1e54ac7496da6382e90fc5d0f4fb80b9ec(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f850a3f97a53065baa853ce3d75553b3b1865f6ca8bae624609e41ff81cc30b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae4472d403b2b910e73b907304d86a2587537c5fa185b9e88b2681be791bce06(
    value: typing.Optional[GoogleContainerNodePoolUpgradeSettingsBlueGreenSettingsStandardRolloutPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e9cbb60d7267d7b5aad81fd5ac5f26206942d6efcb21601ab3851af01f971c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a0f76de9420c1b0da4ee7596557afa2b7ab40740872486c60e22a63302386db(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a3c174eaed15632662bbf0c80e1277d7a274d7f9de61c12c53ccd30c0028a3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e904f0c512e74ca592a65049e65941ad77f8ec9474837bc15446885effa1a290(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3e2aae4f43753f568b0caea8bdc1f1b7a226adcc5c592138e1e5c9756de06a(
    value: typing.Optional[GoogleContainerNodePoolUpgradeSettings],
) -> None:
    """Type checking stubs"""
    pass
