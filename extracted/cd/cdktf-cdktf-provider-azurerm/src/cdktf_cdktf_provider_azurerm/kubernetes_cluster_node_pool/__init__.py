r'''
# `azurerm_kubernetes_cluster_node_pool`

Refer to the Terraform Registry for docs: [`azurerm_kubernetes_cluster_node_pool`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool).
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


class KubernetesClusterNodePool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesClusterNodePool.KubernetesClusterNodePool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool azurerm_kubernetes_cluster_node_pool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        kubernetes_cluster_id: builtins.str,
        name: builtins.str,
        auto_scaling_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        capacity_reservation_group_id: typing.Optional[builtins.str] = None,
        eviction_policy: typing.Optional[builtins.str] = None,
        fips_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gpu_instance: typing.Optional[builtins.str] = None,
        host_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_group_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kubelet_config: typing.Optional[typing.Union["KubernetesClusterNodePoolKubeletConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        kubelet_disk_type: typing.Optional[builtins.str] = None,
        linux_os_config: typing.Optional[typing.Union["KubernetesClusterNodePoolLinuxOsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        max_count: typing.Optional[jsii.Number] = None,
        max_pods: typing.Optional[jsii.Number] = None,
        min_count: typing.Optional[jsii.Number] = None,
        mode: typing.Optional[builtins.str] = None,
        node_count: typing.Optional[jsii.Number] = None,
        node_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_network_profile: typing.Optional[typing.Union["KubernetesClusterNodePoolNodeNetworkProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        node_public_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        node_public_ip_prefix_id: typing.Optional[builtins.str] = None,
        node_taints: typing.Optional[typing.Sequence[builtins.str]] = None,
        orchestrator_version: typing.Optional[builtins.str] = None,
        os_disk_size_gb: typing.Optional[jsii.Number] = None,
        os_disk_type: typing.Optional[builtins.str] = None,
        os_sku: typing.Optional[builtins.str] = None,
        os_type: typing.Optional[builtins.str] = None,
        pod_subnet_id: typing.Optional[builtins.str] = None,
        priority: typing.Optional[builtins.str] = None,
        proximity_placement_group_id: typing.Optional[builtins.str] = None,
        scale_down_mode: typing.Optional[builtins.str] = None,
        snapshot_id: typing.Optional[builtins.str] = None,
        spot_max_price: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        temporary_name_for_rotation: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["KubernetesClusterNodePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        ultra_ssd_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        upgrade_settings: typing.Optional[typing.Union["KubernetesClusterNodePoolUpgradeSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        vm_size: typing.Optional[builtins.str] = None,
        vnet_subnet_id: typing.Optional[builtins.str] = None,
        windows_profile: typing.Optional[typing.Union["KubernetesClusterNodePoolWindowsProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        workload_runtime: typing.Optional[builtins.str] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool azurerm_kubernetes_cluster_node_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param kubernetes_cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#kubernetes_cluster_id KubernetesClusterNodePool#kubernetes_cluster_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#name KubernetesClusterNodePool#name}.
        :param auto_scaling_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#auto_scaling_enabled KubernetesClusterNodePool#auto_scaling_enabled}.
        :param capacity_reservation_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#capacity_reservation_group_id KubernetesClusterNodePool#capacity_reservation_group_id}.
        :param eviction_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#eviction_policy KubernetesClusterNodePool#eviction_policy}.
        :param fips_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#fips_enabled KubernetesClusterNodePool#fips_enabled}.
        :param gpu_instance: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#gpu_instance KubernetesClusterNodePool#gpu_instance}.
        :param host_encryption_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#host_encryption_enabled KubernetesClusterNodePool#host_encryption_enabled}.
        :param host_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#host_group_id KubernetesClusterNodePool#host_group_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#id KubernetesClusterNodePool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kubelet_config: kubelet_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#kubelet_config KubernetesClusterNodePool#kubelet_config}
        :param kubelet_disk_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#kubelet_disk_type KubernetesClusterNodePool#kubelet_disk_type}.
        :param linux_os_config: linux_os_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#linux_os_config KubernetesClusterNodePool#linux_os_config}
        :param max_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#max_count KubernetesClusterNodePool#max_count}.
        :param max_pods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#max_pods KubernetesClusterNodePool#max_pods}.
        :param min_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#min_count KubernetesClusterNodePool#min_count}.
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#mode KubernetesClusterNodePool#mode}.
        :param node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_count KubernetesClusterNodePool#node_count}.
        :param node_labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_labels KubernetesClusterNodePool#node_labels}.
        :param node_network_profile: node_network_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_network_profile KubernetesClusterNodePool#node_network_profile}
        :param node_public_ip_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_public_ip_enabled KubernetesClusterNodePool#node_public_ip_enabled}.
        :param node_public_ip_prefix_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_public_ip_prefix_id KubernetesClusterNodePool#node_public_ip_prefix_id}.
        :param node_taints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_taints KubernetesClusterNodePool#node_taints}.
        :param orchestrator_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#orchestrator_version KubernetesClusterNodePool#orchestrator_version}.
        :param os_disk_size_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#os_disk_size_gb KubernetesClusterNodePool#os_disk_size_gb}.
        :param os_disk_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#os_disk_type KubernetesClusterNodePool#os_disk_type}.
        :param os_sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#os_sku KubernetesClusterNodePool#os_sku}.
        :param os_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#os_type KubernetesClusterNodePool#os_type}.
        :param pod_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#pod_subnet_id KubernetesClusterNodePool#pod_subnet_id}.
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#priority KubernetesClusterNodePool#priority}.
        :param proximity_placement_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#proximity_placement_group_id KubernetesClusterNodePool#proximity_placement_group_id}.
        :param scale_down_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#scale_down_mode KubernetesClusterNodePool#scale_down_mode}.
        :param snapshot_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#snapshot_id KubernetesClusterNodePool#snapshot_id}.
        :param spot_max_price: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#spot_max_price KubernetesClusterNodePool#spot_max_price}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#tags KubernetesClusterNodePool#tags}.
        :param temporary_name_for_rotation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#temporary_name_for_rotation KubernetesClusterNodePool#temporary_name_for_rotation}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#timeouts KubernetesClusterNodePool#timeouts}
        :param ultra_ssd_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#ultra_ssd_enabled KubernetesClusterNodePool#ultra_ssd_enabled}.
        :param upgrade_settings: upgrade_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#upgrade_settings KubernetesClusterNodePool#upgrade_settings}
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#vm_size KubernetesClusterNodePool#vm_size}.
        :param vnet_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#vnet_subnet_id KubernetesClusterNodePool#vnet_subnet_id}.
        :param windows_profile: windows_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#windows_profile KubernetesClusterNodePool#windows_profile}
        :param workload_runtime: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#workload_runtime KubernetesClusterNodePool#workload_runtime}.
        :param zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#zones KubernetesClusterNodePool#zones}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0bd62d7b5f759647639a7cb4635a5600065706b12c089287fa9579360cd8b7e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = KubernetesClusterNodePoolConfig(
            kubernetes_cluster_id=kubernetes_cluster_id,
            name=name,
            auto_scaling_enabled=auto_scaling_enabled,
            capacity_reservation_group_id=capacity_reservation_group_id,
            eviction_policy=eviction_policy,
            fips_enabled=fips_enabled,
            gpu_instance=gpu_instance,
            host_encryption_enabled=host_encryption_enabled,
            host_group_id=host_group_id,
            id=id,
            kubelet_config=kubelet_config,
            kubelet_disk_type=kubelet_disk_type,
            linux_os_config=linux_os_config,
            max_count=max_count,
            max_pods=max_pods,
            min_count=min_count,
            mode=mode,
            node_count=node_count,
            node_labels=node_labels,
            node_network_profile=node_network_profile,
            node_public_ip_enabled=node_public_ip_enabled,
            node_public_ip_prefix_id=node_public_ip_prefix_id,
            node_taints=node_taints,
            orchestrator_version=orchestrator_version,
            os_disk_size_gb=os_disk_size_gb,
            os_disk_type=os_disk_type,
            os_sku=os_sku,
            os_type=os_type,
            pod_subnet_id=pod_subnet_id,
            priority=priority,
            proximity_placement_group_id=proximity_placement_group_id,
            scale_down_mode=scale_down_mode,
            snapshot_id=snapshot_id,
            spot_max_price=spot_max_price,
            tags=tags,
            temporary_name_for_rotation=temporary_name_for_rotation,
            timeouts=timeouts,
            ultra_ssd_enabled=ultra_ssd_enabled,
            upgrade_settings=upgrade_settings,
            vm_size=vm_size,
            vnet_subnet_id=vnet_subnet_id,
            windows_profile=windows_profile,
            workload_runtime=workload_runtime,
            zones=zones,
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
        '''Generates CDKTF code for importing a KubernetesClusterNodePool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the KubernetesClusterNodePool to import.
        :param import_from_id: The id of the existing KubernetesClusterNodePool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the KubernetesClusterNodePool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__223e65c859bb70ae8d5eed2a0cc86d59d5a7dc1a12bd909c3890ba2f8478eabf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putKubeletConfig")
    def put_kubelet_config(
        self,
        *,
        allowed_unsafe_sysctls: typing.Optional[typing.Sequence[builtins.str]] = None,
        container_log_max_line: typing.Optional[jsii.Number] = None,
        container_log_max_size_mb: typing.Optional[jsii.Number] = None,
        cpu_cfs_quota_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cpu_cfs_quota_period: typing.Optional[builtins.str] = None,
        cpu_manager_policy: typing.Optional[builtins.str] = None,
        image_gc_high_threshold: typing.Optional[jsii.Number] = None,
        image_gc_low_threshold: typing.Optional[jsii.Number] = None,
        pod_max_pid: typing.Optional[jsii.Number] = None,
        topology_manager_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_unsafe_sysctls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#allowed_unsafe_sysctls KubernetesClusterNodePool#allowed_unsafe_sysctls}.
        :param container_log_max_line: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#container_log_max_line KubernetesClusterNodePool#container_log_max_line}.
        :param container_log_max_size_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#container_log_max_size_mb KubernetesClusterNodePool#container_log_max_size_mb}.
        :param cpu_cfs_quota_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#cpu_cfs_quota_enabled KubernetesClusterNodePool#cpu_cfs_quota_enabled}.
        :param cpu_cfs_quota_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#cpu_cfs_quota_period KubernetesClusterNodePool#cpu_cfs_quota_period}.
        :param cpu_manager_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#cpu_manager_policy KubernetesClusterNodePool#cpu_manager_policy}.
        :param image_gc_high_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#image_gc_high_threshold KubernetesClusterNodePool#image_gc_high_threshold}.
        :param image_gc_low_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#image_gc_low_threshold KubernetesClusterNodePool#image_gc_low_threshold}.
        :param pod_max_pid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#pod_max_pid KubernetesClusterNodePool#pod_max_pid}.
        :param topology_manager_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#topology_manager_policy KubernetesClusterNodePool#topology_manager_policy}.
        '''
        value = KubernetesClusterNodePoolKubeletConfig(
            allowed_unsafe_sysctls=allowed_unsafe_sysctls,
            container_log_max_line=container_log_max_line,
            container_log_max_size_mb=container_log_max_size_mb,
            cpu_cfs_quota_enabled=cpu_cfs_quota_enabled,
            cpu_cfs_quota_period=cpu_cfs_quota_period,
            cpu_manager_policy=cpu_manager_policy,
            image_gc_high_threshold=image_gc_high_threshold,
            image_gc_low_threshold=image_gc_low_threshold,
            pod_max_pid=pod_max_pid,
            topology_manager_policy=topology_manager_policy,
        )

        return typing.cast(None, jsii.invoke(self, "putKubeletConfig", [value]))

    @jsii.member(jsii_name="putLinuxOsConfig")
    def put_linux_os_config(
        self,
        *,
        swap_file_size_mb: typing.Optional[jsii.Number] = None,
        sysctl_config: typing.Optional[typing.Union["KubernetesClusterNodePoolLinuxOsConfigSysctlConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        transparent_huge_page_defrag: typing.Optional[builtins.str] = None,
        transparent_huge_page_enabled: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param swap_file_size_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#swap_file_size_mb KubernetesClusterNodePool#swap_file_size_mb}.
        :param sysctl_config: sysctl_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#sysctl_config KubernetesClusterNodePool#sysctl_config}
        :param transparent_huge_page_defrag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#transparent_huge_page_defrag KubernetesClusterNodePool#transparent_huge_page_defrag}.
        :param transparent_huge_page_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#transparent_huge_page_enabled KubernetesClusterNodePool#transparent_huge_page_enabled}.
        '''
        value = KubernetesClusterNodePoolLinuxOsConfig(
            swap_file_size_mb=swap_file_size_mb,
            sysctl_config=sysctl_config,
            transparent_huge_page_defrag=transparent_huge_page_defrag,
            transparent_huge_page_enabled=transparent_huge_page_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putLinuxOsConfig", [value]))

    @jsii.member(jsii_name="putNodeNetworkProfile")
    def put_node_network_profile(
        self,
        *,
        allowed_host_ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPorts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        application_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        node_public_ip_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_host_ports: allowed_host_ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#allowed_host_ports KubernetesClusterNodePool#allowed_host_ports}
        :param application_security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#application_security_group_ids KubernetesClusterNodePool#application_security_group_ids}.
        :param node_public_ip_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_public_ip_tags KubernetesClusterNodePool#node_public_ip_tags}.
        '''
        value = KubernetesClusterNodePoolNodeNetworkProfile(
            allowed_host_ports=allowed_host_ports,
            application_security_group_ids=application_security_group_ids,
            node_public_ip_tags=node_public_ip_tags,
        )

        return typing.cast(None, jsii.invoke(self, "putNodeNetworkProfile", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#create KubernetesClusterNodePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#delete KubernetesClusterNodePool#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#read KubernetesClusterNodePool#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#update KubernetesClusterNodePool#update}.
        '''
        value = KubernetesClusterNodePoolTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUpgradeSettings")
    def put_upgrade_settings(
        self,
        *,
        max_surge: builtins.str,
        drain_timeout_in_minutes: typing.Optional[jsii.Number] = None,
        node_soak_duration_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_surge: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#max_surge KubernetesClusterNodePool#max_surge}.
        :param drain_timeout_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#drain_timeout_in_minutes KubernetesClusterNodePool#drain_timeout_in_minutes}.
        :param node_soak_duration_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_soak_duration_in_minutes KubernetesClusterNodePool#node_soak_duration_in_minutes}.
        '''
        value = KubernetesClusterNodePoolUpgradeSettings(
            max_surge=max_surge,
            drain_timeout_in_minutes=drain_timeout_in_minutes,
            node_soak_duration_in_minutes=node_soak_duration_in_minutes,
        )

        return typing.cast(None, jsii.invoke(self, "putUpgradeSettings", [value]))

    @jsii.member(jsii_name="putWindowsProfile")
    def put_windows_profile(
        self,
        *,
        outbound_nat_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param outbound_nat_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#outbound_nat_enabled KubernetesClusterNodePool#outbound_nat_enabled}.
        '''
        value = KubernetesClusterNodePoolWindowsProfile(
            outbound_nat_enabled=outbound_nat_enabled
        )

        return typing.cast(None, jsii.invoke(self, "putWindowsProfile", [value]))

    @jsii.member(jsii_name="resetAutoScalingEnabled")
    def reset_auto_scaling_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoScalingEnabled", []))

    @jsii.member(jsii_name="resetCapacityReservationGroupId")
    def reset_capacity_reservation_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapacityReservationGroupId", []))

    @jsii.member(jsii_name="resetEvictionPolicy")
    def reset_eviction_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvictionPolicy", []))

    @jsii.member(jsii_name="resetFipsEnabled")
    def reset_fips_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFipsEnabled", []))

    @jsii.member(jsii_name="resetGpuInstance")
    def reset_gpu_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGpuInstance", []))

    @jsii.member(jsii_name="resetHostEncryptionEnabled")
    def reset_host_encryption_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostEncryptionEnabled", []))

    @jsii.member(jsii_name="resetHostGroupId")
    def reset_host_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostGroupId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKubeletConfig")
    def reset_kubelet_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubeletConfig", []))

    @jsii.member(jsii_name="resetKubeletDiskType")
    def reset_kubelet_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubeletDiskType", []))

    @jsii.member(jsii_name="resetLinuxOsConfig")
    def reset_linux_os_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinuxOsConfig", []))

    @jsii.member(jsii_name="resetMaxCount")
    def reset_max_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxCount", []))

    @jsii.member(jsii_name="resetMaxPods")
    def reset_max_pods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxPods", []))

    @jsii.member(jsii_name="resetMinCount")
    def reset_min_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinCount", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetNodeCount")
    def reset_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeCount", []))

    @jsii.member(jsii_name="resetNodeLabels")
    def reset_node_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeLabels", []))

    @jsii.member(jsii_name="resetNodeNetworkProfile")
    def reset_node_network_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeNetworkProfile", []))

    @jsii.member(jsii_name="resetNodePublicIpEnabled")
    def reset_node_public_ip_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodePublicIpEnabled", []))

    @jsii.member(jsii_name="resetNodePublicIpPrefixId")
    def reset_node_public_ip_prefix_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodePublicIpPrefixId", []))

    @jsii.member(jsii_name="resetNodeTaints")
    def reset_node_taints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeTaints", []))

    @jsii.member(jsii_name="resetOrchestratorVersion")
    def reset_orchestrator_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrchestratorVersion", []))

    @jsii.member(jsii_name="resetOsDiskSizeGb")
    def reset_os_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsDiskSizeGb", []))

    @jsii.member(jsii_name="resetOsDiskType")
    def reset_os_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsDiskType", []))

    @jsii.member(jsii_name="resetOsSku")
    def reset_os_sku(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsSku", []))

    @jsii.member(jsii_name="resetOsType")
    def reset_os_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsType", []))

    @jsii.member(jsii_name="resetPodSubnetId")
    def reset_pod_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPodSubnetId", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetProximityPlacementGroupId")
    def reset_proximity_placement_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProximityPlacementGroupId", []))

    @jsii.member(jsii_name="resetScaleDownMode")
    def reset_scale_down_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaleDownMode", []))

    @jsii.member(jsii_name="resetSnapshotId")
    def reset_snapshot_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshotId", []))

    @jsii.member(jsii_name="resetSpotMaxPrice")
    def reset_spot_max_price(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpotMaxPrice", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTemporaryNameForRotation")
    def reset_temporary_name_for_rotation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemporaryNameForRotation", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUltraSsdEnabled")
    def reset_ultra_ssd_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUltraSsdEnabled", []))

    @jsii.member(jsii_name="resetUpgradeSettings")
    def reset_upgrade_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpgradeSettings", []))

    @jsii.member(jsii_name="resetVmSize")
    def reset_vm_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmSize", []))

    @jsii.member(jsii_name="resetVnetSubnetId")
    def reset_vnet_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVnetSubnetId", []))

    @jsii.member(jsii_name="resetWindowsProfile")
    def reset_windows_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowsProfile", []))

    @jsii.member(jsii_name="resetWorkloadRuntime")
    def reset_workload_runtime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkloadRuntime", []))

    @jsii.member(jsii_name="resetZones")
    def reset_zones(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZones", []))

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
    @jsii.member(jsii_name="kubeletConfig")
    def kubelet_config(self) -> "KubernetesClusterNodePoolKubeletConfigOutputReference":
        return typing.cast("KubernetesClusterNodePoolKubeletConfigOutputReference", jsii.get(self, "kubeletConfig"))

    @builtins.property
    @jsii.member(jsii_name="linuxOsConfig")
    def linux_os_config(
        self,
    ) -> "KubernetesClusterNodePoolLinuxOsConfigOutputReference":
        return typing.cast("KubernetesClusterNodePoolLinuxOsConfigOutputReference", jsii.get(self, "linuxOsConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodeNetworkProfile")
    def node_network_profile(
        self,
    ) -> "KubernetesClusterNodePoolNodeNetworkProfileOutputReference":
        return typing.cast("KubernetesClusterNodePoolNodeNetworkProfileOutputReference", jsii.get(self, "nodeNetworkProfile"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "KubernetesClusterNodePoolTimeoutsOutputReference":
        return typing.cast("KubernetesClusterNodePoolTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="upgradeSettings")
    def upgrade_settings(
        self,
    ) -> "KubernetesClusterNodePoolUpgradeSettingsOutputReference":
        return typing.cast("KubernetesClusterNodePoolUpgradeSettingsOutputReference", jsii.get(self, "upgradeSettings"))

    @builtins.property
    @jsii.member(jsii_name="windowsProfile")
    def windows_profile(
        self,
    ) -> "KubernetesClusterNodePoolWindowsProfileOutputReference":
        return typing.cast("KubernetesClusterNodePoolWindowsProfileOutputReference", jsii.get(self, "windowsProfile"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingEnabledInput")
    def auto_scaling_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoScalingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityReservationGroupIdInput")
    def capacity_reservation_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "capacityReservationGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="evictionPolicyInput")
    def eviction_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "evictionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="fipsEnabledInput")
    def fips_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fipsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="gpuInstanceInput")
    def gpu_instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gpuInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="hostEncryptionEnabledInput")
    def host_encryption_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hostEncryptionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="hostGroupIdInput")
    def host_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kubeletConfigInput")
    def kubelet_config_input(
        self,
    ) -> typing.Optional["KubernetesClusterNodePoolKubeletConfig"]:
        return typing.cast(typing.Optional["KubernetesClusterNodePoolKubeletConfig"], jsii.get(self, "kubeletConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="kubeletDiskTypeInput")
    def kubelet_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubeletDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesClusterIdInput")
    def kubernetes_cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubernetesClusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="linuxOsConfigInput")
    def linux_os_config_input(
        self,
    ) -> typing.Optional["KubernetesClusterNodePoolLinuxOsConfig"]:
        return typing.cast(typing.Optional["KubernetesClusterNodePoolLinuxOsConfig"], jsii.get(self, "linuxOsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="maxCountInput")
    def max_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPodsInput")
    def max_pods_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPodsInput"))

    @builtins.property
    @jsii.member(jsii_name="minCountInput")
    def min_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minCountInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeCountInput")
    def node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeLabelsInput")
    def node_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "nodeLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeNetworkProfileInput")
    def node_network_profile_input(
        self,
    ) -> typing.Optional["KubernetesClusterNodePoolNodeNetworkProfile"]:
        return typing.cast(typing.Optional["KubernetesClusterNodePoolNodeNetworkProfile"], jsii.get(self, "nodeNetworkProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="nodePublicIpEnabledInput")
    def node_public_ip_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nodePublicIpEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nodePublicIpPrefixIdInput")
    def node_public_ip_prefix_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodePublicIpPrefixIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTaintsInput")
    def node_taints_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "nodeTaintsInput"))

    @builtins.property
    @jsii.member(jsii_name="orchestratorVersionInput")
    def orchestrator_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orchestratorVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="osDiskSizeGbInput")
    def os_disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "osDiskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="osDiskTypeInput")
    def os_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="osSkuInput")
    def os_sku_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osSkuInput"))

    @builtins.property
    @jsii.member(jsii_name="osTypeInput")
    def os_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="podSubnetIdInput")
    def pod_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "podSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="proximityPlacementGroupIdInput")
    def proximity_placement_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proximityPlacementGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleDownModeInput")
    def scale_down_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scaleDownModeInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotIdInput")
    def snapshot_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotIdInput"))

    @builtins.property
    @jsii.member(jsii_name="spotMaxPriceInput")
    def spot_max_price_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "spotMaxPriceInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="temporaryNameForRotationInput")
    def temporary_name_for_rotation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "temporaryNameForRotationInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KubernetesClusterNodePoolTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KubernetesClusterNodePoolTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="ultraSsdEnabledInput")
    def ultra_ssd_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ultraSsdEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="upgradeSettingsInput")
    def upgrade_settings_input(
        self,
    ) -> typing.Optional["KubernetesClusterNodePoolUpgradeSettings"]:
        return typing.cast(typing.Optional["KubernetesClusterNodePoolUpgradeSettings"], jsii.get(self, "upgradeSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="vmSizeInput")
    def vm_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="vnetSubnetIdInput")
    def vnet_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vnetSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="windowsProfileInput")
    def windows_profile_input(
        self,
    ) -> typing.Optional["KubernetesClusterNodePoolWindowsProfile"]:
        return typing.cast(typing.Optional["KubernetesClusterNodePoolWindowsProfile"], jsii.get(self, "windowsProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadRuntimeInput")
    def workload_runtime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workloadRuntimeInput"))

    @builtins.property
    @jsii.member(jsii_name="zonesInput")
    def zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "zonesInput"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingEnabled")
    def auto_scaling_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoScalingEnabled"))

    @auto_scaling_enabled.setter
    def auto_scaling_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__167864874165cfff64977fa215d5b2f42ccd00fdc5e38889ed6f5b1f63a722e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoScalingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="capacityReservationGroupId")
    def capacity_reservation_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "capacityReservationGroupId"))

    @capacity_reservation_group_id.setter
    def capacity_reservation_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89c34f6c96f7bd779ba2f99fea1b20d0e5d3647c76a041c57d79e91f20844313)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityReservationGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="evictionPolicy")
    def eviction_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "evictionPolicy"))

    @eviction_policy.setter
    def eviction_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6378be86b341bb4e1a4d5cbb3ac0607b18429a1c81b58605f7a7b16ae2acd80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evictionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fipsEnabled")
    def fips_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fipsEnabled"))

    @fips_enabled.setter
    def fips_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b917aa6a1f15723d3793483d2f617c2237a43308c808689a3889673ace1a3f7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fipsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpuInstance")
    def gpu_instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gpuInstance"))

    @gpu_instance.setter
    def gpu_instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24968835fa86b6172e59adfc6866cb769b19bb52ef20bcb8d1b44e20be82797e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpuInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostEncryptionEnabled")
    def host_encryption_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hostEncryptionEnabled"))

    @host_encryption_enabled.setter
    def host_encryption_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4991d9f7d90c9dfd2fe0ce156086dfd78f9b51c4fc838de58a7e43cc0906af83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostEncryptionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostGroupId")
    def host_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostGroupId"))

    @host_group_id.setter
    def host_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f5f522c670879d0c619a12270cef86883d6d8a6f1720efc83ba29ba3bf1b35e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__245b86c17dda364f5f03e235f86d208861da27826643357335dead4f9a3c7904)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kubeletDiskType")
    def kubelet_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubeletDiskType"))

    @kubelet_disk_type.setter
    def kubelet_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60ce3c0a59f4d1884c8544121b98ab13ed3452d658837f8bfb70eb08228d2f09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubeletDiskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kubernetesClusterId")
    def kubernetes_cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesClusterId"))

    @kubernetes_cluster_id.setter
    def kubernetes_cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4b9811cca28bf984b19fe6ec2f0a3cb421b62da89f8ed802d6b81007d85c975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubernetesClusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxCount")
    def max_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxCount"))

    @max_count.setter
    def max_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43bb452be8aeee0ab247171b47fd8894b4e83a7e221e10ac29f72fe41f4d83e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxPods")
    def max_pods(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPods"))

    @max_pods.setter
    def max_pods(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__551f794a57c4c15ab406b4c49eff0b9b90ae12e0998910b648541136c7809023)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minCount")
    def min_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minCount"))

    @min_count.setter
    def min_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3af0291b8c89839477e78c74e6a7d0536b2968c1eb91da09d7bbd8f1d972b5da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a736bfe65d1b125732b2c3bf6f65c100606f603b2a3205d30990edf0871fa841)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__827676f3929d5c4593096446958aa882ef10dd1b8e06dfea60ea6a77615c380d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__003068d88a2b600306da583d699a396df9a6a3e62462df65c0043e753c2acddd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeLabels")
    def node_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "nodeLabels"))

    @node_labels.setter
    def node_labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0b1a881cd4f99c63ee8a9d31a89c2845097fb4d6958fa9a4863f827d923d574)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodePublicIpEnabled")
    def node_public_ip_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nodePublicIpEnabled"))

    @node_public_ip_enabled.setter
    def node_public_ip_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea2ee568cb937ed11e70d22dbf05f77b104ec8521f87a8c068f9e92b17ed3824)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodePublicIpEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodePublicIpPrefixId")
    def node_public_ip_prefix_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodePublicIpPrefixId"))

    @node_public_ip_prefix_id.setter
    def node_public_ip_prefix_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81c800dc05c93e76d519b0d967160bce1ffcd76fda511ea53b6d2ad77f0cf4f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodePublicIpPrefixId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeTaints")
    def node_taints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "nodeTaints"))

    @node_taints.setter
    def node_taints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f4b8e1a78d1de0033f118c4420202a8482f9943c7f96851845b1625746e700a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeTaints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orchestratorVersion")
    def orchestrator_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orchestratorVersion"))

    @orchestrator_version.setter
    def orchestrator_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1734413818bbe4e135b76b4f39883fbb557eae6d663e9cff6eddff5499cf16b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orchestratorVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osDiskSizeGb")
    def os_disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "osDiskSizeGb"))

    @os_disk_size_gb.setter
    def os_disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e333d4a3de77a72a6ee6d2f4d8ab0cc366adfa5b8d8234ca94f9124c2ea10d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osDiskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osDiskType")
    def os_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osDiskType"))

    @os_disk_type.setter
    def os_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f9566e5d6918ebb9e19890f5dafa2e13dbdbd1b6ebf7144a2d5bb145aecd617)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osDiskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osSku")
    def os_sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osSku"))

    @os_sku.setter
    def os_sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3481c96ee62507b18a5cf4161a201206d27ed1199cc49a231f675ed921276461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osSku", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osType"))

    @os_type.setter
    def os_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1019b6c18c885deb2c7d025829eb3c749bbece311f606f4e7f27ed670f8a367)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="podSubnetId")
    def pod_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "podSubnetId"))

    @pod_subnet_id.setter
    def pod_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__432bc065df3a862261baae4027e912d266a8824e6d532815f68b7dd440d13cfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podSubnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ee6f64deb03916e11a8fd38210055b9dd72935e2a0e5c4249ed8458cb270fd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proximityPlacementGroupId")
    def proximity_placement_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proximityPlacementGroupId"))

    @proximity_placement_group_id.setter
    def proximity_placement_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9900d99f5116f7034f8d96951f9d10e9170964bf63bf322cd7cc94fb694c7c32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proximityPlacementGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleDownMode")
    def scale_down_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scaleDownMode"))

    @scale_down_mode.setter
    def scale_down_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c7b2918ca56a4a1ad192c984d53c98f127b93bb53501b7d3e030673ecf901cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleDownMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotId")
    def snapshot_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snapshotId"))

    @snapshot_id.setter
    def snapshot_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d324c38872acc50f857805b3eb5c82fb854ab1e7f63e201f9793a0949057837)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="spotMaxPrice")
    def spot_max_price(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "spotMaxPrice"))

    @spot_max_price.setter
    def spot_max_price(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7c5485ae3346a677dc66f44f18e24b3a2e641ceaaf419fbb2f8bbfb8f03fd05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spotMaxPrice", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91622fb844d261232dedbc0862c653857b52f6a267b1a717ae06d5de78d5f7a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="temporaryNameForRotation")
    def temporary_name_for_rotation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "temporaryNameForRotation"))

    @temporary_name_for_rotation.setter
    def temporary_name_for_rotation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51307bbe0bbf03160430b73860c224570db509cb1c6c139f43e18f8881d6950f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "temporaryNameForRotation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ultraSsdEnabled")
    def ultra_ssd_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ultraSsdEnabled"))

    @ultra_ssd_enabled.setter
    def ultra_ssd_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd92f95fac9b1591a8116e1ac45ad7363c25864e87b4b7d3f85f812c46acf9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ultraSsdEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7cd92dd811d547087e26d8ab71207498cc5c5f50e12a2d411ab5f4f087ee77f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vnetSubnetId")
    def vnet_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vnetSubnetId"))

    @vnet_subnet_id.setter
    def vnet_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25d1e125e1b90431a1c2dca15424b4206d261d66db6240d55388dba97478c486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vnetSubnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workloadRuntime")
    def workload_runtime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workloadRuntime"))

    @workload_runtime.setter
    def workload_runtime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19d425137d149bba9ad06f799be81914e803a64ef1b08a7115d4c4eba50e8e7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadRuntime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zones")
    def zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "zones"))

    @zones.setter
    def zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfbf2864c2a2e9f5f1ca47d8d9d14459401d7f2b521fde02d4fa6f96b1c79d57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zones", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesClusterNodePool.KubernetesClusterNodePoolConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "kubernetes_cluster_id": "kubernetesClusterId",
        "name": "name",
        "auto_scaling_enabled": "autoScalingEnabled",
        "capacity_reservation_group_id": "capacityReservationGroupId",
        "eviction_policy": "evictionPolicy",
        "fips_enabled": "fipsEnabled",
        "gpu_instance": "gpuInstance",
        "host_encryption_enabled": "hostEncryptionEnabled",
        "host_group_id": "hostGroupId",
        "id": "id",
        "kubelet_config": "kubeletConfig",
        "kubelet_disk_type": "kubeletDiskType",
        "linux_os_config": "linuxOsConfig",
        "max_count": "maxCount",
        "max_pods": "maxPods",
        "min_count": "minCount",
        "mode": "mode",
        "node_count": "nodeCount",
        "node_labels": "nodeLabels",
        "node_network_profile": "nodeNetworkProfile",
        "node_public_ip_enabled": "nodePublicIpEnabled",
        "node_public_ip_prefix_id": "nodePublicIpPrefixId",
        "node_taints": "nodeTaints",
        "orchestrator_version": "orchestratorVersion",
        "os_disk_size_gb": "osDiskSizeGb",
        "os_disk_type": "osDiskType",
        "os_sku": "osSku",
        "os_type": "osType",
        "pod_subnet_id": "podSubnetId",
        "priority": "priority",
        "proximity_placement_group_id": "proximityPlacementGroupId",
        "scale_down_mode": "scaleDownMode",
        "snapshot_id": "snapshotId",
        "spot_max_price": "spotMaxPrice",
        "tags": "tags",
        "temporary_name_for_rotation": "temporaryNameForRotation",
        "timeouts": "timeouts",
        "ultra_ssd_enabled": "ultraSsdEnabled",
        "upgrade_settings": "upgradeSettings",
        "vm_size": "vmSize",
        "vnet_subnet_id": "vnetSubnetId",
        "windows_profile": "windowsProfile",
        "workload_runtime": "workloadRuntime",
        "zones": "zones",
    },
)
class KubernetesClusterNodePoolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        kubernetes_cluster_id: builtins.str,
        name: builtins.str,
        auto_scaling_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        capacity_reservation_group_id: typing.Optional[builtins.str] = None,
        eviction_policy: typing.Optional[builtins.str] = None,
        fips_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gpu_instance: typing.Optional[builtins.str] = None,
        host_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_group_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kubelet_config: typing.Optional[typing.Union["KubernetesClusterNodePoolKubeletConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        kubelet_disk_type: typing.Optional[builtins.str] = None,
        linux_os_config: typing.Optional[typing.Union["KubernetesClusterNodePoolLinuxOsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        max_count: typing.Optional[jsii.Number] = None,
        max_pods: typing.Optional[jsii.Number] = None,
        min_count: typing.Optional[jsii.Number] = None,
        mode: typing.Optional[builtins.str] = None,
        node_count: typing.Optional[jsii.Number] = None,
        node_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_network_profile: typing.Optional[typing.Union["KubernetesClusterNodePoolNodeNetworkProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        node_public_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        node_public_ip_prefix_id: typing.Optional[builtins.str] = None,
        node_taints: typing.Optional[typing.Sequence[builtins.str]] = None,
        orchestrator_version: typing.Optional[builtins.str] = None,
        os_disk_size_gb: typing.Optional[jsii.Number] = None,
        os_disk_type: typing.Optional[builtins.str] = None,
        os_sku: typing.Optional[builtins.str] = None,
        os_type: typing.Optional[builtins.str] = None,
        pod_subnet_id: typing.Optional[builtins.str] = None,
        priority: typing.Optional[builtins.str] = None,
        proximity_placement_group_id: typing.Optional[builtins.str] = None,
        scale_down_mode: typing.Optional[builtins.str] = None,
        snapshot_id: typing.Optional[builtins.str] = None,
        spot_max_price: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        temporary_name_for_rotation: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["KubernetesClusterNodePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        ultra_ssd_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        upgrade_settings: typing.Optional[typing.Union["KubernetesClusterNodePoolUpgradeSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        vm_size: typing.Optional[builtins.str] = None,
        vnet_subnet_id: typing.Optional[builtins.str] = None,
        windows_profile: typing.Optional[typing.Union["KubernetesClusterNodePoolWindowsProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        workload_runtime: typing.Optional[builtins.str] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param kubernetes_cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#kubernetes_cluster_id KubernetesClusterNodePool#kubernetes_cluster_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#name KubernetesClusterNodePool#name}.
        :param auto_scaling_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#auto_scaling_enabled KubernetesClusterNodePool#auto_scaling_enabled}.
        :param capacity_reservation_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#capacity_reservation_group_id KubernetesClusterNodePool#capacity_reservation_group_id}.
        :param eviction_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#eviction_policy KubernetesClusterNodePool#eviction_policy}.
        :param fips_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#fips_enabled KubernetesClusterNodePool#fips_enabled}.
        :param gpu_instance: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#gpu_instance KubernetesClusterNodePool#gpu_instance}.
        :param host_encryption_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#host_encryption_enabled KubernetesClusterNodePool#host_encryption_enabled}.
        :param host_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#host_group_id KubernetesClusterNodePool#host_group_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#id KubernetesClusterNodePool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kubelet_config: kubelet_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#kubelet_config KubernetesClusterNodePool#kubelet_config}
        :param kubelet_disk_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#kubelet_disk_type KubernetesClusterNodePool#kubelet_disk_type}.
        :param linux_os_config: linux_os_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#linux_os_config KubernetesClusterNodePool#linux_os_config}
        :param max_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#max_count KubernetesClusterNodePool#max_count}.
        :param max_pods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#max_pods KubernetesClusterNodePool#max_pods}.
        :param min_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#min_count KubernetesClusterNodePool#min_count}.
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#mode KubernetesClusterNodePool#mode}.
        :param node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_count KubernetesClusterNodePool#node_count}.
        :param node_labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_labels KubernetesClusterNodePool#node_labels}.
        :param node_network_profile: node_network_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_network_profile KubernetesClusterNodePool#node_network_profile}
        :param node_public_ip_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_public_ip_enabled KubernetesClusterNodePool#node_public_ip_enabled}.
        :param node_public_ip_prefix_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_public_ip_prefix_id KubernetesClusterNodePool#node_public_ip_prefix_id}.
        :param node_taints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_taints KubernetesClusterNodePool#node_taints}.
        :param orchestrator_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#orchestrator_version KubernetesClusterNodePool#orchestrator_version}.
        :param os_disk_size_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#os_disk_size_gb KubernetesClusterNodePool#os_disk_size_gb}.
        :param os_disk_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#os_disk_type KubernetesClusterNodePool#os_disk_type}.
        :param os_sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#os_sku KubernetesClusterNodePool#os_sku}.
        :param os_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#os_type KubernetesClusterNodePool#os_type}.
        :param pod_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#pod_subnet_id KubernetesClusterNodePool#pod_subnet_id}.
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#priority KubernetesClusterNodePool#priority}.
        :param proximity_placement_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#proximity_placement_group_id KubernetesClusterNodePool#proximity_placement_group_id}.
        :param scale_down_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#scale_down_mode KubernetesClusterNodePool#scale_down_mode}.
        :param snapshot_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#snapshot_id KubernetesClusterNodePool#snapshot_id}.
        :param spot_max_price: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#spot_max_price KubernetesClusterNodePool#spot_max_price}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#tags KubernetesClusterNodePool#tags}.
        :param temporary_name_for_rotation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#temporary_name_for_rotation KubernetesClusterNodePool#temporary_name_for_rotation}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#timeouts KubernetesClusterNodePool#timeouts}
        :param ultra_ssd_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#ultra_ssd_enabled KubernetesClusterNodePool#ultra_ssd_enabled}.
        :param upgrade_settings: upgrade_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#upgrade_settings KubernetesClusterNodePool#upgrade_settings}
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#vm_size KubernetesClusterNodePool#vm_size}.
        :param vnet_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#vnet_subnet_id KubernetesClusterNodePool#vnet_subnet_id}.
        :param windows_profile: windows_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#windows_profile KubernetesClusterNodePool#windows_profile}
        :param workload_runtime: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#workload_runtime KubernetesClusterNodePool#workload_runtime}.
        :param zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#zones KubernetesClusterNodePool#zones}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(kubelet_config, dict):
            kubelet_config = KubernetesClusterNodePoolKubeletConfig(**kubelet_config)
        if isinstance(linux_os_config, dict):
            linux_os_config = KubernetesClusterNodePoolLinuxOsConfig(**linux_os_config)
        if isinstance(node_network_profile, dict):
            node_network_profile = KubernetesClusterNodePoolNodeNetworkProfile(**node_network_profile)
        if isinstance(timeouts, dict):
            timeouts = KubernetesClusterNodePoolTimeouts(**timeouts)
        if isinstance(upgrade_settings, dict):
            upgrade_settings = KubernetesClusterNodePoolUpgradeSettings(**upgrade_settings)
        if isinstance(windows_profile, dict):
            windows_profile = KubernetesClusterNodePoolWindowsProfile(**windows_profile)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c2d91fe666235d7809d5d2b18e809ed38c78296d1653d0cf628ecd4ab1dd42)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument kubernetes_cluster_id", value=kubernetes_cluster_id, expected_type=type_hints["kubernetes_cluster_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument auto_scaling_enabled", value=auto_scaling_enabled, expected_type=type_hints["auto_scaling_enabled"])
            check_type(argname="argument capacity_reservation_group_id", value=capacity_reservation_group_id, expected_type=type_hints["capacity_reservation_group_id"])
            check_type(argname="argument eviction_policy", value=eviction_policy, expected_type=type_hints["eviction_policy"])
            check_type(argname="argument fips_enabled", value=fips_enabled, expected_type=type_hints["fips_enabled"])
            check_type(argname="argument gpu_instance", value=gpu_instance, expected_type=type_hints["gpu_instance"])
            check_type(argname="argument host_encryption_enabled", value=host_encryption_enabled, expected_type=type_hints["host_encryption_enabled"])
            check_type(argname="argument host_group_id", value=host_group_id, expected_type=type_hints["host_group_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kubelet_config", value=kubelet_config, expected_type=type_hints["kubelet_config"])
            check_type(argname="argument kubelet_disk_type", value=kubelet_disk_type, expected_type=type_hints["kubelet_disk_type"])
            check_type(argname="argument linux_os_config", value=linux_os_config, expected_type=type_hints["linux_os_config"])
            check_type(argname="argument max_count", value=max_count, expected_type=type_hints["max_count"])
            check_type(argname="argument max_pods", value=max_pods, expected_type=type_hints["max_pods"])
            check_type(argname="argument min_count", value=min_count, expected_type=type_hints["min_count"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
            check_type(argname="argument node_labels", value=node_labels, expected_type=type_hints["node_labels"])
            check_type(argname="argument node_network_profile", value=node_network_profile, expected_type=type_hints["node_network_profile"])
            check_type(argname="argument node_public_ip_enabled", value=node_public_ip_enabled, expected_type=type_hints["node_public_ip_enabled"])
            check_type(argname="argument node_public_ip_prefix_id", value=node_public_ip_prefix_id, expected_type=type_hints["node_public_ip_prefix_id"])
            check_type(argname="argument node_taints", value=node_taints, expected_type=type_hints["node_taints"])
            check_type(argname="argument orchestrator_version", value=orchestrator_version, expected_type=type_hints["orchestrator_version"])
            check_type(argname="argument os_disk_size_gb", value=os_disk_size_gb, expected_type=type_hints["os_disk_size_gb"])
            check_type(argname="argument os_disk_type", value=os_disk_type, expected_type=type_hints["os_disk_type"])
            check_type(argname="argument os_sku", value=os_sku, expected_type=type_hints["os_sku"])
            check_type(argname="argument os_type", value=os_type, expected_type=type_hints["os_type"])
            check_type(argname="argument pod_subnet_id", value=pod_subnet_id, expected_type=type_hints["pod_subnet_id"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument proximity_placement_group_id", value=proximity_placement_group_id, expected_type=type_hints["proximity_placement_group_id"])
            check_type(argname="argument scale_down_mode", value=scale_down_mode, expected_type=type_hints["scale_down_mode"])
            check_type(argname="argument snapshot_id", value=snapshot_id, expected_type=type_hints["snapshot_id"])
            check_type(argname="argument spot_max_price", value=spot_max_price, expected_type=type_hints["spot_max_price"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument temporary_name_for_rotation", value=temporary_name_for_rotation, expected_type=type_hints["temporary_name_for_rotation"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument ultra_ssd_enabled", value=ultra_ssd_enabled, expected_type=type_hints["ultra_ssd_enabled"])
            check_type(argname="argument upgrade_settings", value=upgrade_settings, expected_type=type_hints["upgrade_settings"])
            check_type(argname="argument vm_size", value=vm_size, expected_type=type_hints["vm_size"])
            check_type(argname="argument vnet_subnet_id", value=vnet_subnet_id, expected_type=type_hints["vnet_subnet_id"])
            check_type(argname="argument windows_profile", value=windows_profile, expected_type=type_hints["windows_profile"])
            check_type(argname="argument workload_runtime", value=workload_runtime, expected_type=type_hints["workload_runtime"])
            check_type(argname="argument zones", value=zones, expected_type=type_hints["zones"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kubernetes_cluster_id": kubernetes_cluster_id,
            "name": name,
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
        if auto_scaling_enabled is not None:
            self._values["auto_scaling_enabled"] = auto_scaling_enabled
        if capacity_reservation_group_id is not None:
            self._values["capacity_reservation_group_id"] = capacity_reservation_group_id
        if eviction_policy is not None:
            self._values["eviction_policy"] = eviction_policy
        if fips_enabled is not None:
            self._values["fips_enabled"] = fips_enabled
        if gpu_instance is not None:
            self._values["gpu_instance"] = gpu_instance
        if host_encryption_enabled is not None:
            self._values["host_encryption_enabled"] = host_encryption_enabled
        if host_group_id is not None:
            self._values["host_group_id"] = host_group_id
        if id is not None:
            self._values["id"] = id
        if kubelet_config is not None:
            self._values["kubelet_config"] = kubelet_config
        if kubelet_disk_type is not None:
            self._values["kubelet_disk_type"] = kubelet_disk_type
        if linux_os_config is not None:
            self._values["linux_os_config"] = linux_os_config
        if max_count is not None:
            self._values["max_count"] = max_count
        if max_pods is not None:
            self._values["max_pods"] = max_pods
        if min_count is not None:
            self._values["min_count"] = min_count
        if mode is not None:
            self._values["mode"] = mode
        if node_count is not None:
            self._values["node_count"] = node_count
        if node_labels is not None:
            self._values["node_labels"] = node_labels
        if node_network_profile is not None:
            self._values["node_network_profile"] = node_network_profile
        if node_public_ip_enabled is not None:
            self._values["node_public_ip_enabled"] = node_public_ip_enabled
        if node_public_ip_prefix_id is not None:
            self._values["node_public_ip_prefix_id"] = node_public_ip_prefix_id
        if node_taints is not None:
            self._values["node_taints"] = node_taints
        if orchestrator_version is not None:
            self._values["orchestrator_version"] = orchestrator_version
        if os_disk_size_gb is not None:
            self._values["os_disk_size_gb"] = os_disk_size_gb
        if os_disk_type is not None:
            self._values["os_disk_type"] = os_disk_type
        if os_sku is not None:
            self._values["os_sku"] = os_sku
        if os_type is not None:
            self._values["os_type"] = os_type
        if pod_subnet_id is not None:
            self._values["pod_subnet_id"] = pod_subnet_id
        if priority is not None:
            self._values["priority"] = priority
        if proximity_placement_group_id is not None:
            self._values["proximity_placement_group_id"] = proximity_placement_group_id
        if scale_down_mode is not None:
            self._values["scale_down_mode"] = scale_down_mode
        if snapshot_id is not None:
            self._values["snapshot_id"] = snapshot_id
        if spot_max_price is not None:
            self._values["spot_max_price"] = spot_max_price
        if tags is not None:
            self._values["tags"] = tags
        if temporary_name_for_rotation is not None:
            self._values["temporary_name_for_rotation"] = temporary_name_for_rotation
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if ultra_ssd_enabled is not None:
            self._values["ultra_ssd_enabled"] = ultra_ssd_enabled
        if upgrade_settings is not None:
            self._values["upgrade_settings"] = upgrade_settings
        if vm_size is not None:
            self._values["vm_size"] = vm_size
        if vnet_subnet_id is not None:
            self._values["vnet_subnet_id"] = vnet_subnet_id
        if windows_profile is not None:
            self._values["windows_profile"] = windows_profile
        if workload_runtime is not None:
            self._values["workload_runtime"] = workload_runtime
        if zones is not None:
            self._values["zones"] = zones

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
    def kubernetes_cluster_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#kubernetes_cluster_id KubernetesClusterNodePool#kubernetes_cluster_id}.'''
        result = self._values.get("kubernetes_cluster_id")
        assert result is not None, "Required property 'kubernetes_cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#name KubernetesClusterNodePool#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_scaling_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#auto_scaling_enabled KubernetesClusterNodePool#auto_scaling_enabled}.'''
        result = self._values.get("auto_scaling_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def capacity_reservation_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#capacity_reservation_group_id KubernetesClusterNodePool#capacity_reservation_group_id}.'''
        result = self._values.get("capacity_reservation_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eviction_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#eviction_policy KubernetesClusterNodePool#eviction_policy}.'''
        result = self._values.get("eviction_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fips_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#fips_enabled KubernetesClusterNodePool#fips_enabled}.'''
        result = self._values.get("fips_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gpu_instance(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#gpu_instance KubernetesClusterNodePool#gpu_instance}.'''
        result = self._values.get("gpu_instance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#host_encryption_enabled KubernetesClusterNodePool#host_encryption_enabled}.'''
        result = self._values.get("host_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def host_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#host_group_id KubernetesClusterNodePool#host_group_id}.'''
        result = self._values.get("host_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#id KubernetesClusterNodePool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kubelet_config(
        self,
    ) -> typing.Optional["KubernetesClusterNodePoolKubeletConfig"]:
        '''kubelet_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#kubelet_config KubernetesClusterNodePool#kubelet_config}
        '''
        result = self._values.get("kubelet_config")
        return typing.cast(typing.Optional["KubernetesClusterNodePoolKubeletConfig"], result)

    @builtins.property
    def kubelet_disk_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#kubelet_disk_type KubernetesClusterNodePool#kubelet_disk_type}.'''
        result = self._values.get("kubelet_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def linux_os_config(
        self,
    ) -> typing.Optional["KubernetesClusterNodePoolLinuxOsConfig"]:
        '''linux_os_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#linux_os_config KubernetesClusterNodePool#linux_os_config}
        '''
        result = self._values.get("linux_os_config")
        return typing.cast(typing.Optional["KubernetesClusterNodePoolLinuxOsConfig"], result)

    @builtins.property
    def max_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#max_count KubernetesClusterNodePool#max_count}.'''
        result = self._values.get("max_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_pods(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#max_pods KubernetesClusterNodePool#max_pods}.'''
        result = self._values.get("max_pods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#min_count KubernetesClusterNodePool#min_count}.'''
        result = self._values.get("min_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#mode KubernetesClusterNodePool#mode}.'''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_count KubernetesClusterNodePool#node_count}.'''
        result = self._values.get("node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def node_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_labels KubernetesClusterNodePool#node_labels}.'''
        result = self._values.get("node_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def node_network_profile(
        self,
    ) -> typing.Optional["KubernetesClusterNodePoolNodeNetworkProfile"]:
        '''node_network_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_network_profile KubernetesClusterNodePool#node_network_profile}
        '''
        result = self._values.get("node_network_profile")
        return typing.cast(typing.Optional["KubernetesClusterNodePoolNodeNetworkProfile"], result)

    @builtins.property
    def node_public_ip_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_public_ip_enabled KubernetesClusterNodePool#node_public_ip_enabled}.'''
        result = self._values.get("node_public_ip_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def node_public_ip_prefix_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_public_ip_prefix_id KubernetesClusterNodePool#node_public_ip_prefix_id}.'''
        result = self._values.get("node_public_ip_prefix_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_taints(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_taints KubernetesClusterNodePool#node_taints}.'''
        result = self._values.get("node_taints")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def orchestrator_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#orchestrator_version KubernetesClusterNodePool#orchestrator_version}.'''
        result = self._values.get("orchestrator_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#os_disk_size_gb KubernetesClusterNodePool#os_disk_size_gb}.'''
        result = self._values.get("os_disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def os_disk_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#os_disk_type KubernetesClusterNodePool#os_disk_type}.'''
        result = self._values.get("os_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_sku(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#os_sku KubernetesClusterNodePool#os_sku}.'''
        result = self._values.get("os_sku")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#os_type KubernetesClusterNodePool#os_type}.'''
        result = self._values.get("os_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pod_subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#pod_subnet_id KubernetesClusterNodePool#pod_subnet_id}.'''
        result = self._values.get("pod_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#priority KubernetesClusterNodePool#priority}.'''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proximity_placement_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#proximity_placement_group_id KubernetesClusterNodePool#proximity_placement_group_id}.'''
        result = self._values.get("proximity_placement_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scale_down_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#scale_down_mode KubernetesClusterNodePool#scale_down_mode}.'''
        result = self._values.get("scale_down_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#snapshot_id KubernetesClusterNodePool#snapshot_id}.'''
        result = self._values.get("snapshot_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spot_max_price(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#spot_max_price KubernetesClusterNodePool#spot_max_price}.'''
        result = self._values.get("spot_max_price")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#tags KubernetesClusterNodePool#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def temporary_name_for_rotation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#temporary_name_for_rotation KubernetesClusterNodePool#temporary_name_for_rotation}.'''
        result = self._values.get("temporary_name_for_rotation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["KubernetesClusterNodePoolTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#timeouts KubernetesClusterNodePool#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["KubernetesClusterNodePoolTimeouts"], result)

    @builtins.property
    def ultra_ssd_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#ultra_ssd_enabled KubernetesClusterNodePool#ultra_ssd_enabled}.'''
        result = self._values.get("ultra_ssd_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def upgrade_settings(
        self,
    ) -> typing.Optional["KubernetesClusterNodePoolUpgradeSettings"]:
        '''upgrade_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#upgrade_settings KubernetesClusterNodePool#upgrade_settings}
        '''
        result = self._values.get("upgrade_settings")
        return typing.cast(typing.Optional["KubernetesClusterNodePoolUpgradeSettings"], result)

    @builtins.property
    def vm_size(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#vm_size KubernetesClusterNodePool#vm_size}.'''
        result = self._values.get("vm_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vnet_subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#vnet_subnet_id KubernetesClusterNodePool#vnet_subnet_id}.'''
        result = self._values.get("vnet_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def windows_profile(
        self,
    ) -> typing.Optional["KubernetesClusterNodePoolWindowsProfile"]:
        '''windows_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#windows_profile KubernetesClusterNodePool#windows_profile}
        '''
        result = self._values.get("windows_profile")
        return typing.cast(typing.Optional["KubernetesClusterNodePoolWindowsProfile"], result)

    @builtins.property
    def workload_runtime(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#workload_runtime KubernetesClusterNodePool#workload_runtime}.'''
        result = self._values.get("workload_runtime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#zones KubernetesClusterNodePool#zones}.'''
        result = self._values.get("zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesClusterNodePool.KubernetesClusterNodePoolKubeletConfig",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_unsafe_sysctls": "allowedUnsafeSysctls",
        "container_log_max_line": "containerLogMaxLine",
        "container_log_max_size_mb": "containerLogMaxSizeMb",
        "cpu_cfs_quota_enabled": "cpuCfsQuotaEnabled",
        "cpu_cfs_quota_period": "cpuCfsQuotaPeriod",
        "cpu_manager_policy": "cpuManagerPolicy",
        "image_gc_high_threshold": "imageGcHighThreshold",
        "image_gc_low_threshold": "imageGcLowThreshold",
        "pod_max_pid": "podMaxPid",
        "topology_manager_policy": "topologyManagerPolicy",
    },
)
class KubernetesClusterNodePoolKubeletConfig:
    def __init__(
        self,
        *,
        allowed_unsafe_sysctls: typing.Optional[typing.Sequence[builtins.str]] = None,
        container_log_max_line: typing.Optional[jsii.Number] = None,
        container_log_max_size_mb: typing.Optional[jsii.Number] = None,
        cpu_cfs_quota_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cpu_cfs_quota_period: typing.Optional[builtins.str] = None,
        cpu_manager_policy: typing.Optional[builtins.str] = None,
        image_gc_high_threshold: typing.Optional[jsii.Number] = None,
        image_gc_low_threshold: typing.Optional[jsii.Number] = None,
        pod_max_pid: typing.Optional[jsii.Number] = None,
        topology_manager_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_unsafe_sysctls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#allowed_unsafe_sysctls KubernetesClusterNodePool#allowed_unsafe_sysctls}.
        :param container_log_max_line: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#container_log_max_line KubernetesClusterNodePool#container_log_max_line}.
        :param container_log_max_size_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#container_log_max_size_mb KubernetesClusterNodePool#container_log_max_size_mb}.
        :param cpu_cfs_quota_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#cpu_cfs_quota_enabled KubernetesClusterNodePool#cpu_cfs_quota_enabled}.
        :param cpu_cfs_quota_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#cpu_cfs_quota_period KubernetesClusterNodePool#cpu_cfs_quota_period}.
        :param cpu_manager_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#cpu_manager_policy KubernetesClusterNodePool#cpu_manager_policy}.
        :param image_gc_high_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#image_gc_high_threshold KubernetesClusterNodePool#image_gc_high_threshold}.
        :param image_gc_low_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#image_gc_low_threshold KubernetesClusterNodePool#image_gc_low_threshold}.
        :param pod_max_pid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#pod_max_pid KubernetesClusterNodePool#pod_max_pid}.
        :param topology_manager_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#topology_manager_policy KubernetesClusterNodePool#topology_manager_policy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80db6d0bd0628ec2dd4c3ad2299c4100098950630fae16cd4894d00fd617f4ce)
            check_type(argname="argument allowed_unsafe_sysctls", value=allowed_unsafe_sysctls, expected_type=type_hints["allowed_unsafe_sysctls"])
            check_type(argname="argument container_log_max_line", value=container_log_max_line, expected_type=type_hints["container_log_max_line"])
            check_type(argname="argument container_log_max_size_mb", value=container_log_max_size_mb, expected_type=type_hints["container_log_max_size_mb"])
            check_type(argname="argument cpu_cfs_quota_enabled", value=cpu_cfs_quota_enabled, expected_type=type_hints["cpu_cfs_quota_enabled"])
            check_type(argname="argument cpu_cfs_quota_period", value=cpu_cfs_quota_period, expected_type=type_hints["cpu_cfs_quota_period"])
            check_type(argname="argument cpu_manager_policy", value=cpu_manager_policy, expected_type=type_hints["cpu_manager_policy"])
            check_type(argname="argument image_gc_high_threshold", value=image_gc_high_threshold, expected_type=type_hints["image_gc_high_threshold"])
            check_type(argname="argument image_gc_low_threshold", value=image_gc_low_threshold, expected_type=type_hints["image_gc_low_threshold"])
            check_type(argname="argument pod_max_pid", value=pod_max_pid, expected_type=type_hints["pod_max_pid"])
            check_type(argname="argument topology_manager_policy", value=topology_manager_policy, expected_type=type_hints["topology_manager_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_unsafe_sysctls is not None:
            self._values["allowed_unsafe_sysctls"] = allowed_unsafe_sysctls
        if container_log_max_line is not None:
            self._values["container_log_max_line"] = container_log_max_line
        if container_log_max_size_mb is not None:
            self._values["container_log_max_size_mb"] = container_log_max_size_mb
        if cpu_cfs_quota_enabled is not None:
            self._values["cpu_cfs_quota_enabled"] = cpu_cfs_quota_enabled
        if cpu_cfs_quota_period is not None:
            self._values["cpu_cfs_quota_period"] = cpu_cfs_quota_period
        if cpu_manager_policy is not None:
            self._values["cpu_manager_policy"] = cpu_manager_policy
        if image_gc_high_threshold is not None:
            self._values["image_gc_high_threshold"] = image_gc_high_threshold
        if image_gc_low_threshold is not None:
            self._values["image_gc_low_threshold"] = image_gc_low_threshold
        if pod_max_pid is not None:
            self._values["pod_max_pid"] = pod_max_pid
        if topology_manager_policy is not None:
            self._values["topology_manager_policy"] = topology_manager_policy

    @builtins.property
    def allowed_unsafe_sysctls(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#allowed_unsafe_sysctls KubernetesClusterNodePool#allowed_unsafe_sysctls}.'''
        result = self._values.get("allowed_unsafe_sysctls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def container_log_max_line(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#container_log_max_line KubernetesClusterNodePool#container_log_max_line}.'''
        result = self._values.get("container_log_max_line")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def container_log_max_size_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#container_log_max_size_mb KubernetesClusterNodePool#container_log_max_size_mb}.'''
        result = self._values.get("container_log_max_size_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu_cfs_quota_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#cpu_cfs_quota_enabled KubernetesClusterNodePool#cpu_cfs_quota_enabled}.'''
        result = self._values.get("cpu_cfs_quota_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cpu_cfs_quota_period(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#cpu_cfs_quota_period KubernetesClusterNodePool#cpu_cfs_quota_period}.'''
        result = self._values.get("cpu_cfs_quota_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_manager_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#cpu_manager_policy KubernetesClusterNodePool#cpu_manager_policy}.'''
        result = self._values.get("cpu_manager_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_gc_high_threshold(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#image_gc_high_threshold KubernetesClusterNodePool#image_gc_high_threshold}.'''
        result = self._values.get("image_gc_high_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def image_gc_low_threshold(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#image_gc_low_threshold KubernetesClusterNodePool#image_gc_low_threshold}.'''
        result = self._values.get("image_gc_low_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pod_max_pid(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#pod_max_pid KubernetesClusterNodePool#pod_max_pid}.'''
        result = self._values.get("pod_max_pid")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def topology_manager_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#topology_manager_policy KubernetesClusterNodePool#topology_manager_policy}.'''
        result = self._values.get("topology_manager_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterNodePoolKubeletConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterNodePoolKubeletConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesClusterNodePool.KubernetesClusterNodePoolKubeletConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4ae2165e4474a3e4ed73a47fc1d32d009eda2cb8ad5736c6b40ea3bda36a1bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedUnsafeSysctls")
    def reset_allowed_unsafe_sysctls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedUnsafeSysctls", []))

    @jsii.member(jsii_name="resetContainerLogMaxLine")
    def reset_container_log_max_line(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerLogMaxLine", []))

    @jsii.member(jsii_name="resetContainerLogMaxSizeMb")
    def reset_container_log_max_size_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerLogMaxSizeMb", []))

    @jsii.member(jsii_name="resetCpuCfsQuotaEnabled")
    def reset_cpu_cfs_quota_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuCfsQuotaEnabled", []))

    @jsii.member(jsii_name="resetCpuCfsQuotaPeriod")
    def reset_cpu_cfs_quota_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuCfsQuotaPeriod", []))

    @jsii.member(jsii_name="resetCpuManagerPolicy")
    def reset_cpu_manager_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuManagerPolicy", []))

    @jsii.member(jsii_name="resetImageGcHighThreshold")
    def reset_image_gc_high_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageGcHighThreshold", []))

    @jsii.member(jsii_name="resetImageGcLowThreshold")
    def reset_image_gc_low_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageGcLowThreshold", []))

    @jsii.member(jsii_name="resetPodMaxPid")
    def reset_pod_max_pid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPodMaxPid", []))

    @jsii.member(jsii_name="resetTopologyManagerPolicy")
    def reset_topology_manager_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopologyManagerPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="allowedUnsafeSysctlsInput")
    def allowed_unsafe_sysctls_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedUnsafeSysctlsInput"))

    @builtins.property
    @jsii.member(jsii_name="containerLogMaxLineInput")
    def container_log_max_line_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "containerLogMaxLineInput"))

    @builtins.property
    @jsii.member(jsii_name="containerLogMaxSizeMbInput")
    def container_log_max_size_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "containerLogMaxSizeMbInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuCfsQuotaEnabledInput")
    def cpu_cfs_quota_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cpuCfsQuotaEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuCfsQuotaPeriodInput")
    def cpu_cfs_quota_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuCfsQuotaPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuManagerPolicyInput")
    def cpu_manager_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuManagerPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="imageGcHighThresholdInput")
    def image_gc_high_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "imageGcHighThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="imageGcLowThresholdInput")
    def image_gc_low_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "imageGcLowThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="podMaxPidInput")
    def pod_max_pid_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "podMaxPidInput"))

    @builtins.property
    @jsii.member(jsii_name="topologyManagerPolicyInput")
    def topology_manager_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topologyManagerPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedUnsafeSysctls")
    def allowed_unsafe_sysctls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedUnsafeSysctls"))

    @allowed_unsafe_sysctls.setter
    def allowed_unsafe_sysctls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__103633604dab466059805eeae75a555365cdb4a541fe7744a14de2a86d271284)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedUnsafeSysctls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerLogMaxLine")
    def container_log_max_line(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "containerLogMaxLine"))

    @container_log_max_line.setter
    def container_log_max_line(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e41c07e05fe4ba18549f6966985d6a5550c4265029753da06a79650e623cfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerLogMaxLine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerLogMaxSizeMb")
    def container_log_max_size_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "containerLogMaxSizeMb"))

    @container_log_max_size_mb.setter
    def container_log_max_size_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__172eee9556ae066c9e3d7d7ae0343dd776119691d8a6c0eb9d22bc485cbae026)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerLogMaxSizeMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuCfsQuotaEnabled")
    def cpu_cfs_quota_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cpuCfsQuotaEnabled"))

    @cpu_cfs_quota_enabled.setter
    def cpu_cfs_quota_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f1e53b16305f39c5d375ca4b33c2a93166e6774fa2989b7d1df864dafa01bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCfsQuotaEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuCfsQuotaPeriod")
    def cpu_cfs_quota_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuCfsQuotaPeriod"))

    @cpu_cfs_quota_period.setter
    def cpu_cfs_quota_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e722b5e2ebb5f7a82a7ecd6397ddf974ba1e3293695913eae206cc99f49f9f01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCfsQuotaPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuManagerPolicy")
    def cpu_manager_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuManagerPolicy"))

    @cpu_manager_policy.setter
    def cpu_manager_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cf84cf3c4089c3bcf8c39dd15df92fd42fc96e91cabc0d7af70ad989208659d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuManagerPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageGcHighThreshold")
    def image_gc_high_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "imageGcHighThreshold"))

    @image_gc_high_threshold.setter
    def image_gc_high_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b196b47ecb03a59b683e2c102ab8abbfae57bbd7938ef9dbfec5699aca9d4b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageGcHighThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageGcLowThreshold")
    def image_gc_low_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "imageGcLowThreshold"))

    @image_gc_low_threshold.setter
    def image_gc_low_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1977779b05a200b46c7e7766fbd99b9bc9ac58a529ac5721f02924f85b811942)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageGcLowThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="podMaxPid")
    def pod_max_pid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "podMaxPid"))

    @pod_max_pid.setter
    def pod_max_pid(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bec4b86b8444af2b840df7ac5f92a3aa0f751f160713c2ae46765347af16c79e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podMaxPid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topologyManagerPolicy")
    def topology_manager_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topologyManagerPolicy"))

    @topology_manager_policy.setter
    def topology_manager_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e2462156de9fe00c7d9279f1ca274a7814ab12d4a0a87f109b944cd2e92cc5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topologyManagerPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesClusterNodePoolKubeletConfig]:
        return typing.cast(typing.Optional[KubernetesClusterNodePoolKubeletConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterNodePoolKubeletConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4fd99100d43698d8b3fe0203693e5753dab9455d73ed04e1b7766f47f58f4ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesClusterNodePool.KubernetesClusterNodePoolLinuxOsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "swap_file_size_mb": "swapFileSizeMb",
        "sysctl_config": "sysctlConfig",
        "transparent_huge_page_defrag": "transparentHugePageDefrag",
        "transparent_huge_page_enabled": "transparentHugePageEnabled",
    },
)
class KubernetesClusterNodePoolLinuxOsConfig:
    def __init__(
        self,
        *,
        swap_file_size_mb: typing.Optional[jsii.Number] = None,
        sysctl_config: typing.Optional[typing.Union["KubernetesClusterNodePoolLinuxOsConfigSysctlConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        transparent_huge_page_defrag: typing.Optional[builtins.str] = None,
        transparent_huge_page_enabled: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param swap_file_size_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#swap_file_size_mb KubernetesClusterNodePool#swap_file_size_mb}.
        :param sysctl_config: sysctl_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#sysctl_config KubernetesClusterNodePool#sysctl_config}
        :param transparent_huge_page_defrag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#transparent_huge_page_defrag KubernetesClusterNodePool#transparent_huge_page_defrag}.
        :param transparent_huge_page_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#transparent_huge_page_enabled KubernetesClusterNodePool#transparent_huge_page_enabled}.
        '''
        if isinstance(sysctl_config, dict):
            sysctl_config = KubernetesClusterNodePoolLinuxOsConfigSysctlConfig(**sysctl_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95107ed3ab8204d158ea8f2472e574d0a7182e57f1bf40c60ce99169e7fe0502)
            check_type(argname="argument swap_file_size_mb", value=swap_file_size_mb, expected_type=type_hints["swap_file_size_mb"])
            check_type(argname="argument sysctl_config", value=sysctl_config, expected_type=type_hints["sysctl_config"])
            check_type(argname="argument transparent_huge_page_defrag", value=transparent_huge_page_defrag, expected_type=type_hints["transparent_huge_page_defrag"])
            check_type(argname="argument transparent_huge_page_enabled", value=transparent_huge_page_enabled, expected_type=type_hints["transparent_huge_page_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if swap_file_size_mb is not None:
            self._values["swap_file_size_mb"] = swap_file_size_mb
        if sysctl_config is not None:
            self._values["sysctl_config"] = sysctl_config
        if transparent_huge_page_defrag is not None:
            self._values["transparent_huge_page_defrag"] = transparent_huge_page_defrag
        if transparent_huge_page_enabled is not None:
            self._values["transparent_huge_page_enabled"] = transparent_huge_page_enabled

    @builtins.property
    def swap_file_size_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#swap_file_size_mb KubernetesClusterNodePool#swap_file_size_mb}.'''
        result = self._values.get("swap_file_size_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sysctl_config(
        self,
    ) -> typing.Optional["KubernetesClusterNodePoolLinuxOsConfigSysctlConfig"]:
        '''sysctl_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#sysctl_config KubernetesClusterNodePool#sysctl_config}
        '''
        result = self._values.get("sysctl_config")
        return typing.cast(typing.Optional["KubernetesClusterNodePoolLinuxOsConfigSysctlConfig"], result)

    @builtins.property
    def transparent_huge_page_defrag(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#transparent_huge_page_defrag KubernetesClusterNodePool#transparent_huge_page_defrag}.'''
        result = self._values.get("transparent_huge_page_defrag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transparent_huge_page_enabled(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#transparent_huge_page_enabled KubernetesClusterNodePool#transparent_huge_page_enabled}.'''
        result = self._values.get("transparent_huge_page_enabled")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterNodePoolLinuxOsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterNodePoolLinuxOsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesClusterNodePool.KubernetesClusterNodePoolLinuxOsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62bb57f3342831ab5521b5dd02dca3b051796669d600da76aba2f05117cabe58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSysctlConfig")
    def put_sysctl_config(
        self,
        *,
        fs_aio_max_nr: typing.Optional[jsii.Number] = None,
        fs_file_max: typing.Optional[jsii.Number] = None,
        fs_inotify_max_user_watches: typing.Optional[jsii.Number] = None,
        fs_nr_open: typing.Optional[jsii.Number] = None,
        kernel_threads_max: typing.Optional[jsii.Number] = None,
        net_core_netdev_max_backlog: typing.Optional[jsii.Number] = None,
        net_core_optmem_max: typing.Optional[jsii.Number] = None,
        net_core_rmem_default: typing.Optional[jsii.Number] = None,
        net_core_rmem_max: typing.Optional[jsii.Number] = None,
        net_core_somaxconn: typing.Optional[jsii.Number] = None,
        net_core_wmem_default: typing.Optional[jsii.Number] = None,
        net_core_wmem_max: typing.Optional[jsii.Number] = None,
        net_ipv4_ip_local_port_range_max: typing.Optional[jsii.Number] = None,
        net_ipv4_ip_local_port_range_min: typing.Optional[jsii.Number] = None,
        net_ipv4_neigh_default_gc_thresh1: typing.Optional[jsii.Number] = None,
        net_ipv4_neigh_default_gc_thresh2: typing.Optional[jsii.Number] = None,
        net_ipv4_neigh_default_gc_thresh3: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_fin_timeout: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_keepalive_intvl: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_keepalive_probes: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_keepalive_time: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_max_syn_backlog: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_max_tw_buckets: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_tw_reuse: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        net_netfilter_nf_conntrack_buckets: typing.Optional[jsii.Number] = None,
        net_netfilter_nf_conntrack_max: typing.Optional[jsii.Number] = None,
        vm_max_map_count: typing.Optional[jsii.Number] = None,
        vm_swappiness: typing.Optional[jsii.Number] = None,
        vm_vfs_cache_pressure: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fs_aio_max_nr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#fs_aio_max_nr KubernetesClusterNodePool#fs_aio_max_nr}.
        :param fs_file_max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#fs_file_max KubernetesClusterNodePool#fs_file_max}.
        :param fs_inotify_max_user_watches: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#fs_inotify_max_user_watches KubernetesClusterNodePool#fs_inotify_max_user_watches}.
        :param fs_nr_open: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#fs_nr_open KubernetesClusterNodePool#fs_nr_open}.
        :param kernel_threads_max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#kernel_threads_max KubernetesClusterNodePool#kernel_threads_max}.
        :param net_core_netdev_max_backlog: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_core_netdev_max_backlog KubernetesClusterNodePool#net_core_netdev_max_backlog}.
        :param net_core_optmem_max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_core_optmem_max KubernetesClusterNodePool#net_core_optmem_max}.
        :param net_core_rmem_default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_core_rmem_default KubernetesClusterNodePool#net_core_rmem_default}.
        :param net_core_rmem_max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_core_rmem_max KubernetesClusterNodePool#net_core_rmem_max}.
        :param net_core_somaxconn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_core_somaxconn KubernetesClusterNodePool#net_core_somaxconn}.
        :param net_core_wmem_default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_core_wmem_default KubernetesClusterNodePool#net_core_wmem_default}.
        :param net_core_wmem_max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_core_wmem_max KubernetesClusterNodePool#net_core_wmem_max}.
        :param net_ipv4_ip_local_port_range_max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_ip_local_port_range_max KubernetesClusterNodePool#net_ipv4_ip_local_port_range_max}.
        :param net_ipv4_ip_local_port_range_min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_ip_local_port_range_min KubernetesClusterNodePool#net_ipv4_ip_local_port_range_min}.
        :param net_ipv4_neigh_default_gc_thresh1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_neigh_default_gc_thresh1 KubernetesClusterNodePool#net_ipv4_neigh_default_gc_thresh1}.
        :param net_ipv4_neigh_default_gc_thresh2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_neigh_default_gc_thresh2 KubernetesClusterNodePool#net_ipv4_neigh_default_gc_thresh2}.
        :param net_ipv4_neigh_default_gc_thresh3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_neigh_default_gc_thresh3 KubernetesClusterNodePool#net_ipv4_neigh_default_gc_thresh3}.
        :param net_ipv4_tcp_fin_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_tcp_fin_timeout KubernetesClusterNodePool#net_ipv4_tcp_fin_timeout}.
        :param net_ipv4_tcp_keepalive_intvl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_tcp_keepalive_intvl KubernetesClusterNodePool#net_ipv4_tcp_keepalive_intvl}.
        :param net_ipv4_tcp_keepalive_probes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_tcp_keepalive_probes KubernetesClusterNodePool#net_ipv4_tcp_keepalive_probes}.
        :param net_ipv4_tcp_keepalive_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_tcp_keepalive_time KubernetesClusterNodePool#net_ipv4_tcp_keepalive_time}.
        :param net_ipv4_tcp_max_syn_backlog: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_tcp_max_syn_backlog KubernetesClusterNodePool#net_ipv4_tcp_max_syn_backlog}.
        :param net_ipv4_tcp_max_tw_buckets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_tcp_max_tw_buckets KubernetesClusterNodePool#net_ipv4_tcp_max_tw_buckets}.
        :param net_ipv4_tcp_tw_reuse: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_tcp_tw_reuse KubernetesClusterNodePool#net_ipv4_tcp_tw_reuse}.
        :param net_netfilter_nf_conntrack_buckets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_netfilter_nf_conntrack_buckets KubernetesClusterNodePool#net_netfilter_nf_conntrack_buckets}.
        :param net_netfilter_nf_conntrack_max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_netfilter_nf_conntrack_max KubernetesClusterNodePool#net_netfilter_nf_conntrack_max}.
        :param vm_max_map_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#vm_max_map_count KubernetesClusterNodePool#vm_max_map_count}.
        :param vm_swappiness: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#vm_swappiness KubernetesClusterNodePool#vm_swappiness}.
        :param vm_vfs_cache_pressure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#vm_vfs_cache_pressure KubernetesClusterNodePool#vm_vfs_cache_pressure}.
        '''
        value = KubernetesClusterNodePoolLinuxOsConfigSysctlConfig(
            fs_aio_max_nr=fs_aio_max_nr,
            fs_file_max=fs_file_max,
            fs_inotify_max_user_watches=fs_inotify_max_user_watches,
            fs_nr_open=fs_nr_open,
            kernel_threads_max=kernel_threads_max,
            net_core_netdev_max_backlog=net_core_netdev_max_backlog,
            net_core_optmem_max=net_core_optmem_max,
            net_core_rmem_default=net_core_rmem_default,
            net_core_rmem_max=net_core_rmem_max,
            net_core_somaxconn=net_core_somaxconn,
            net_core_wmem_default=net_core_wmem_default,
            net_core_wmem_max=net_core_wmem_max,
            net_ipv4_ip_local_port_range_max=net_ipv4_ip_local_port_range_max,
            net_ipv4_ip_local_port_range_min=net_ipv4_ip_local_port_range_min,
            net_ipv4_neigh_default_gc_thresh1=net_ipv4_neigh_default_gc_thresh1,
            net_ipv4_neigh_default_gc_thresh2=net_ipv4_neigh_default_gc_thresh2,
            net_ipv4_neigh_default_gc_thresh3=net_ipv4_neigh_default_gc_thresh3,
            net_ipv4_tcp_fin_timeout=net_ipv4_tcp_fin_timeout,
            net_ipv4_tcp_keepalive_intvl=net_ipv4_tcp_keepalive_intvl,
            net_ipv4_tcp_keepalive_probes=net_ipv4_tcp_keepalive_probes,
            net_ipv4_tcp_keepalive_time=net_ipv4_tcp_keepalive_time,
            net_ipv4_tcp_max_syn_backlog=net_ipv4_tcp_max_syn_backlog,
            net_ipv4_tcp_max_tw_buckets=net_ipv4_tcp_max_tw_buckets,
            net_ipv4_tcp_tw_reuse=net_ipv4_tcp_tw_reuse,
            net_netfilter_nf_conntrack_buckets=net_netfilter_nf_conntrack_buckets,
            net_netfilter_nf_conntrack_max=net_netfilter_nf_conntrack_max,
            vm_max_map_count=vm_max_map_count,
            vm_swappiness=vm_swappiness,
            vm_vfs_cache_pressure=vm_vfs_cache_pressure,
        )

        return typing.cast(None, jsii.invoke(self, "putSysctlConfig", [value]))

    @jsii.member(jsii_name="resetSwapFileSizeMb")
    def reset_swap_file_size_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSwapFileSizeMb", []))

    @jsii.member(jsii_name="resetSysctlConfig")
    def reset_sysctl_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSysctlConfig", []))

    @jsii.member(jsii_name="resetTransparentHugePageDefrag")
    def reset_transparent_huge_page_defrag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransparentHugePageDefrag", []))

    @jsii.member(jsii_name="resetTransparentHugePageEnabled")
    def reset_transparent_huge_page_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransparentHugePageEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="sysctlConfig")
    def sysctl_config(
        self,
    ) -> "KubernetesClusterNodePoolLinuxOsConfigSysctlConfigOutputReference":
        return typing.cast("KubernetesClusterNodePoolLinuxOsConfigSysctlConfigOutputReference", jsii.get(self, "sysctlConfig"))

    @builtins.property
    @jsii.member(jsii_name="swapFileSizeMbInput")
    def swap_file_size_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "swapFileSizeMbInput"))

    @builtins.property
    @jsii.member(jsii_name="sysctlConfigInput")
    def sysctl_config_input(
        self,
    ) -> typing.Optional["KubernetesClusterNodePoolLinuxOsConfigSysctlConfig"]:
        return typing.cast(typing.Optional["KubernetesClusterNodePoolLinuxOsConfigSysctlConfig"], jsii.get(self, "sysctlConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="transparentHugePageDefragInput")
    def transparent_huge_page_defrag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transparentHugePageDefragInput"))

    @builtins.property
    @jsii.member(jsii_name="transparentHugePageEnabledInput")
    def transparent_huge_page_enabled_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transparentHugePageEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="swapFileSizeMb")
    def swap_file_size_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "swapFileSizeMb"))

    @swap_file_size_mb.setter
    def swap_file_size_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05bb32dd303936eaa66457cc2907ee8242faf1880f1c38168ac9aaa49d2820d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "swapFileSizeMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transparentHugePageDefrag")
    def transparent_huge_page_defrag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transparentHugePageDefrag"))

    @transparent_huge_page_defrag.setter
    def transparent_huge_page_defrag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59d8c6c93e2c7ca901deafc874c487756453839329cee9f77f1b8789e01b9727)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transparentHugePageDefrag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transparentHugePageEnabled")
    def transparent_huge_page_enabled(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transparentHugePageEnabled"))

    @transparent_huge_page_enabled.setter
    def transparent_huge_page_enabled(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c31c79da72563df716d6a02b00943fa13b962a7976e8613a503b1f2f102f1b49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transparentHugePageEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesClusterNodePoolLinuxOsConfig]:
        return typing.cast(typing.Optional[KubernetesClusterNodePoolLinuxOsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterNodePoolLinuxOsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a205c3846455b306d5bcb43760d76145fd8b77fb2b7ba5a64ba8661801e16c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesClusterNodePool.KubernetesClusterNodePoolLinuxOsConfigSysctlConfig",
    jsii_struct_bases=[],
    name_mapping={
        "fs_aio_max_nr": "fsAioMaxNr",
        "fs_file_max": "fsFileMax",
        "fs_inotify_max_user_watches": "fsInotifyMaxUserWatches",
        "fs_nr_open": "fsNrOpen",
        "kernel_threads_max": "kernelThreadsMax",
        "net_core_netdev_max_backlog": "netCoreNetdevMaxBacklog",
        "net_core_optmem_max": "netCoreOptmemMax",
        "net_core_rmem_default": "netCoreRmemDefault",
        "net_core_rmem_max": "netCoreRmemMax",
        "net_core_somaxconn": "netCoreSomaxconn",
        "net_core_wmem_default": "netCoreWmemDefault",
        "net_core_wmem_max": "netCoreWmemMax",
        "net_ipv4_ip_local_port_range_max": "netIpv4IpLocalPortRangeMax",
        "net_ipv4_ip_local_port_range_min": "netIpv4IpLocalPortRangeMin",
        "net_ipv4_neigh_default_gc_thresh1": "netIpv4NeighDefaultGcThresh1",
        "net_ipv4_neigh_default_gc_thresh2": "netIpv4NeighDefaultGcThresh2",
        "net_ipv4_neigh_default_gc_thresh3": "netIpv4NeighDefaultGcThresh3",
        "net_ipv4_tcp_fin_timeout": "netIpv4TcpFinTimeout",
        "net_ipv4_tcp_keepalive_intvl": "netIpv4TcpKeepaliveIntvl",
        "net_ipv4_tcp_keepalive_probes": "netIpv4TcpKeepaliveProbes",
        "net_ipv4_tcp_keepalive_time": "netIpv4TcpKeepaliveTime",
        "net_ipv4_tcp_max_syn_backlog": "netIpv4TcpMaxSynBacklog",
        "net_ipv4_tcp_max_tw_buckets": "netIpv4TcpMaxTwBuckets",
        "net_ipv4_tcp_tw_reuse": "netIpv4TcpTwReuse",
        "net_netfilter_nf_conntrack_buckets": "netNetfilterNfConntrackBuckets",
        "net_netfilter_nf_conntrack_max": "netNetfilterNfConntrackMax",
        "vm_max_map_count": "vmMaxMapCount",
        "vm_swappiness": "vmSwappiness",
        "vm_vfs_cache_pressure": "vmVfsCachePressure",
    },
)
class KubernetesClusterNodePoolLinuxOsConfigSysctlConfig:
    def __init__(
        self,
        *,
        fs_aio_max_nr: typing.Optional[jsii.Number] = None,
        fs_file_max: typing.Optional[jsii.Number] = None,
        fs_inotify_max_user_watches: typing.Optional[jsii.Number] = None,
        fs_nr_open: typing.Optional[jsii.Number] = None,
        kernel_threads_max: typing.Optional[jsii.Number] = None,
        net_core_netdev_max_backlog: typing.Optional[jsii.Number] = None,
        net_core_optmem_max: typing.Optional[jsii.Number] = None,
        net_core_rmem_default: typing.Optional[jsii.Number] = None,
        net_core_rmem_max: typing.Optional[jsii.Number] = None,
        net_core_somaxconn: typing.Optional[jsii.Number] = None,
        net_core_wmem_default: typing.Optional[jsii.Number] = None,
        net_core_wmem_max: typing.Optional[jsii.Number] = None,
        net_ipv4_ip_local_port_range_max: typing.Optional[jsii.Number] = None,
        net_ipv4_ip_local_port_range_min: typing.Optional[jsii.Number] = None,
        net_ipv4_neigh_default_gc_thresh1: typing.Optional[jsii.Number] = None,
        net_ipv4_neigh_default_gc_thresh2: typing.Optional[jsii.Number] = None,
        net_ipv4_neigh_default_gc_thresh3: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_fin_timeout: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_keepalive_intvl: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_keepalive_probes: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_keepalive_time: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_max_syn_backlog: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_max_tw_buckets: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_tw_reuse: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        net_netfilter_nf_conntrack_buckets: typing.Optional[jsii.Number] = None,
        net_netfilter_nf_conntrack_max: typing.Optional[jsii.Number] = None,
        vm_max_map_count: typing.Optional[jsii.Number] = None,
        vm_swappiness: typing.Optional[jsii.Number] = None,
        vm_vfs_cache_pressure: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fs_aio_max_nr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#fs_aio_max_nr KubernetesClusterNodePool#fs_aio_max_nr}.
        :param fs_file_max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#fs_file_max KubernetesClusterNodePool#fs_file_max}.
        :param fs_inotify_max_user_watches: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#fs_inotify_max_user_watches KubernetesClusterNodePool#fs_inotify_max_user_watches}.
        :param fs_nr_open: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#fs_nr_open KubernetesClusterNodePool#fs_nr_open}.
        :param kernel_threads_max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#kernel_threads_max KubernetesClusterNodePool#kernel_threads_max}.
        :param net_core_netdev_max_backlog: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_core_netdev_max_backlog KubernetesClusterNodePool#net_core_netdev_max_backlog}.
        :param net_core_optmem_max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_core_optmem_max KubernetesClusterNodePool#net_core_optmem_max}.
        :param net_core_rmem_default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_core_rmem_default KubernetesClusterNodePool#net_core_rmem_default}.
        :param net_core_rmem_max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_core_rmem_max KubernetesClusterNodePool#net_core_rmem_max}.
        :param net_core_somaxconn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_core_somaxconn KubernetesClusterNodePool#net_core_somaxconn}.
        :param net_core_wmem_default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_core_wmem_default KubernetesClusterNodePool#net_core_wmem_default}.
        :param net_core_wmem_max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_core_wmem_max KubernetesClusterNodePool#net_core_wmem_max}.
        :param net_ipv4_ip_local_port_range_max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_ip_local_port_range_max KubernetesClusterNodePool#net_ipv4_ip_local_port_range_max}.
        :param net_ipv4_ip_local_port_range_min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_ip_local_port_range_min KubernetesClusterNodePool#net_ipv4_ip_local_port_range_min}.
        :param net_ipv4_neigh_default_gc_thresh1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_neigh_default_gc_thresh1 KubernetesClusterNodePool#net_ipv4_neigh_default_gc_thresh1}.
        :param net_ipv4_neigh_default_gc_thresh2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_neigh_default_gc_thresh2 KubernetesClusterNodePool#net_ipv4_neigh_default_gc_thresh2}.
        :param net_ipv4_neigh_default_gc_thresh3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_neigh_default_gc_thresh3 KubernetesClusterNodePool#net_ipv4_neigh_default_gc_thresh3}.
        :param net_ipv4_tcp_fin_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_tcp_fin_timeout KubernetesClusterNodePool#net_ipv4_tcp_fin_timeout}.
        :param net_ipv4_tcp_keepalive_intvl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_tcp_keepalive_intvl KubernetesClusterNodePool#net_ipv4_tcp_keepalive_intvl}.
        :param net_ipv4_tcp_keepalive_probes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_tcp_keepalive_probes KubernetesClusterNodePool#net_ipv4_tcp_keepalive_probes}.
        :param net_ipv4_tcp_keepalive_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_tcp_keepalive_time KubernetesClusterNodePool#net_ipv4_tcp_keepalive_time}.
        :param net_ipv4_tcp_max_syn_backlog: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_tcp_max_syn_backlog KubernetesClusterNodePool#net_ipv4_tcp_max_syn_backlog}.
        :param net_ipv4_tcp_max_tw_buckets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_tcp_max_tw_buckets KubernetesClusterNodePool#net_ipv4_tcp_max_tw_buckets}.
        :param net_ipv4_tcp_tw_reuse: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_tcp_tw_reuse KubernetesClusterNodePool#net_ipv4_tcp_tw_reuse}.
        :param net_netfilter_nf_conntrack_buckets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_netfilter_nf_conntrack_buckets KubernetesClusterNodePool#net_netfilter_nf_conntrack_buckets}.
        :param net_netfilter_nf_conntrack_max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_netfilter_nf_conntrack_max KubernetesClusterNodePool#net_netfilter_nf_conntrack_max}.
        :param vm_max_map_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#vm_max_map_count KubernetesClusterNodePool#vm_max_map_count}.
        :param vm_swappiness: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#vm_swappiness KubernetesClusterNodePool#vm_swappiness}.
        :param vm_vfs_cache_pressure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#vm_vfs_cache_pressure KubernetesClusterNodePool#vm_vfs_cache_pressure}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30f54347769cb63b60e5a5a8a49a21b3147c2bbffb6e6b2a11b2719ceb16666e)
            check_type(argname="argument fs_aio_max_nr", value=fs_aio_max_nr, expected_type=type_hints["fs_aio_max_nr"])
            check_type(argname="argument fs_file_max", value=fs_file_max, expected_type=type_hints["fs_file_max"])
            check_type(argname="argument fs_inotify_max_user_watches", value=fs_inotify_max_user_watches, expected_type=type_hints["fs_inotify_max_user_watches"])
            check_type(argname="argument fs_nr_open", value=fs_nr_open, expected_type=type_hints["fs_nr_open"])
            check_type(argname="argument kernel_threads_max", value=kernel_threads_max, expected_type=type_hints["kernel_threads_max"])
            check_type(argname="argument net_core_netdev_max_backlog", value=net_core_netdev_max_backlog, expected_type=type_hints["net_core_netdev_max_backlog"])
            check_type(argname="argument net_core_optmem_max", value=net_core_optmem_max, expected_type=type_hints["net_core_optmem_max"])
            check_type(argname="argument net_core_rmem_default", value=net_core_rmem_default, expected_type=type_hints["net_core_rmem_default"])
            check_type(argname="argument net_core_rmem_max", value=net_core_rmem_max, expected_type=type_hints["net_core_rmem_max"])
            check_type(argname="argument net_core_somaxconn", value=net_core_somaxconn, expected_type=type_hints["net_core_somaxconn"])
            check_type(argname="argument net_core_wmem_default", value=net_core_wmem_default, expected_type=type_hints["net_core_wmem_default"])
            check_type(argname="argument net_core_wmem_max", value=net_core_wmem_max, expected_type=type_hints["net_core_wmem_max"])
            check_type(argname="argument net_ipv4_ip_local_port_range_max", value=net_ipv4_ip_local_port_range_max, expected_type=type_hints["net_ipv4_ip_local_port_range_max"])
            check_type(argname="argument net_ipv4_ip_local_port_range_min", value=net_ipv4_ip_local_port_range_min, expected_type=type_hints["net_ipv4_ip_local_port_range_min"])
            check_type(argname="argument net_ipv4_neigh_default_gc_thresh1", value=net_ipv4_neigh_default_gc_thresh1, expected_type=type_hints["net_ipv4_neigh_default_gc_thresh1"])
            check_type(argname="argument net_ipv4_neigh_default_gc_thresh2", value=net_ipv4_neigh_default_gc_thresh2, expected_type=type_hints["net_ipv4_neigh_default_gc_thresh2"])
            check_type(argname="argument net_ipv4_neigh_default_gc_thresh3", value=net_ipv4_neigh_default_gc_thresh3, expected_type=type_hints["net_ipv4_neigh_default_gc_thresh3"])
            check_type(argname="argument net_ipv4_tcp_fin_timeout", value=net_ipv4_tcp_fin_timeout, expected_type=type_hints["net_ipv4_tcp_fin_timeout"])
            check_type(argname="argument net_ipv4_tcp_keepalive_intvl", value=net_ipv4_tcp_keepalive_intvl, expected_type=type_hints["net_ipv4_tcp_keepalive_intvl"])
            check_type(argname="argument net_ipv4_tcp_keepalive_probes", value=net_ipv4_tcp_keepalive_probes, expected_type=type_hints["net_ipv4_tcp_keepalive_probes"])
            check_type(argname="argument net_ipv4_tcp_keepalive_time", value=net_ipv4_tcp_keepalive_time, expected_type=type_hints["net_ipv4_tcp_keepalive_time"])
            check_type(argname="argument net_ipv4_tcp_max_syn_backlog", value=net_ipv4_tcp_max_syn_backlog, expected_type=type_hints["net_ipv4_tcp_max_syn_backlog"])
            check_type(argname="argument net_ipv4_tcp_max_tw_buckets", value=net_ipv4_tcp_max_tw_buckets, expected_type=type_hints["net_ipv4_tcp_max_tw_buckets"])
            check_type(argname="argument net_ipv4_tcp_tw_reuse", value=net_ipv4_tcp_tw_reuse, expected_type=type_hints["net_ipv4_tcp_tw_reuse"])
            check_type(argname="argument net_netfilter_nf_conntrack_buckets", value=net_netfilter_nf_conntrack_buckets, expected_type=type_hints["net_netfilter_nf_conntrack_buckets"])
            check_type(argname="argument net_netfilter_nf_conntrack_max", value=net_netfilter_nf_conntrack_max, expected_type=type_hints["net_netfilter_nf_conntrack_max"])
            check_type(argname="argument vm_max_map_count", value=vm_max_map_count, expected_type=type_hints["vm_max_map_count"])
            check_type(argname="argument vm_swappiness", value=vm_swappiness, expected_type=type_hints["vm_swappiness"])
            check_type(argname="argument vm_vfs_cache_pressure", value=vm_vfs_cache_pressure, expected_type=type_hints["vm_vfs_cache_pressure"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fs_aio_max_nr is not None:
            self._values["fs_aio_max_nr"] = fs_aio_max_nr
        if fs_file_max is not None:
            self._values["fs_file_max"] = fs_file_max
        if fs_inotify_max_user_watches is not None:
            self._values["fs_inotify_max_user_watches"] = fs_inotify_max_user_watches
        if fs_nr_open is not None:
            self._values["fs_nr_open"] = fs_nr_open
        if kernel_threads_max is not None:
            self._values["kernel_threads_max"] = kernel_threads_max
        if net_core_netdev_max_backlog is not None:
            self._values["net_core_netdev_max_backlog"] = net_core_netdev_max_backlog
        if net_core_optmem_max is not None:
            self._values["net_core_optmem_max"] = net_core_optmem_max
        if net_core_rmem_default is not None:
            self._values["net_core_rmem_default"] = net_core_rmem_default
        if net_core_rmem_max is not None:
            self._values["net_core_rmem_max"] = net_core_rmem_max
        if net_core_somaxconn is not None:
            self._values["net_core_somaxconn"] = net_core_somaxconn
        if net_core_wmem_default is not None:
            self._values["net_core_wmem_default"] = net_core_wmem_default
        if net_core_wmem_max is not None:
            self._values["net_core_wmem_max"] = net_core_wmem_max
        if net_ipv4_ip_local_port_range_max is not None:
            self._values["net_ipv4_ip_local_port_range_max"] = net_ipv4_ip_local_port_range_max
        if net_ipv4_ip_local_port_range_min is not None:
            self._values["net_ipv4_ip_local_port_range_min"] = net_ipv4_ip_local_port_range_min
        if net_ipv4_neigh_default_gc_thresh1 is not None:
            self._values["net_ipv4_neigh_default_gc_thresh1"] = net_ipv4_neigh_default_gc_thresh1
        if net_ipv4_neigh_default_gc_thresh2 is not None:
            self._values["net_ipv4_neigh_default_gc_thresh2"] = net_ipv4_neigh_default_gc_thresh2
        if net_ipv4_neigh_default_gc_thresh3 is not None:
            self._values["net_ipv4_neigh_default_gc_thresh3"] = net_ipv4_neigh_default_gc_thresh3
        if net_ipv4_tcp_fin_timeout is not None:
            self._values["net_ipv4_tcp_fin_timeout"] = net_ipv4_tcp_fin_timeout
        if net_ipv4_tcp_keepalive_intvl is not None:
            self._values["net_ipv4_tcp_keepalive_intvl"] = net_ipv4_tcp_keepalive_intvl
        if net_ipv4_tcp_keepalive_probes is not None:
            self._values["net_ipv4_tcp_keepalive_probes"] = net_ipv4_tcp_keepalive_probes
        if net_ipv4_tcp_keepalive_time is not None:
            self._values["net_ipv4_tcp_keepalive_time"] = net_ipv4_tcp_keepalive_time
        if net_ipv4_tcp_max_syn_backlog is not None:
            self._values["net_ipv4_tcp_max_syn_backlog"] = net_ipv4_tcp_max_syn_backlog
        if net_ipv4_tcp_max_tw_buckets is not None:
            self._values["net_ipv4_tcp_max_tw_buckets"] = net_ipv4_tcp_max_tw_buckets
        if net_ipv4_tcp_tw_reuse is not None:
            self._values["net_ipv4_tcp_tw_reuse"] = net_ipv4_tcp_tw_reuse
        if net_netfilter_nf_conntrack_buckets is not None:
            self._values["net_netfilter_nf_conntrack_buckets"] = net_netfilter_nf_conntrack_buckets
        if net_netfilter_nf_conntrack_max is not None:
            self._values["net_netfilter_nf_conntrack_max"] = net_netfilter_nf_conntrack_max
        if vm_max_map_count is not None:
            self._values["vm_max_map_count"] = vm_max_map_count
        if vm_swappiness is not None:
            self._values["vm_swappiness"] = vm_swappiness
        if vm_vfs_cache_pressure is not None:
            self._values["vm_vfs_cache_pressure"] = vm_vfs_cache_pressure

    @builtins.property
    def fs_aio_max_nr(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#fs_aio_max_nr KubernetesClusterNodePool#fs_aio_max_nr}.'''
        result = self._values.get("fs_aio_max_nr")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fs_file_max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#fs_file_max KubernetesClusterNodePool#fs_file_max}.'''
        result = self._values.get("fs_file_max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fs_inotify_max_user_watches(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#fs_inotify_max_user_watches KubernetesClusterNodePool#fs_inotify_max_user_watches}.'''
        result = self._values.get("fs_inotify_max_user_watches")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fs_nr_open(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#fs_nr_open KubernetesClusterNodePool#fs_nr_open}.'''
        result = self._values.get("fs_nr_open")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def kernel_threads_max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#kernel_threads_max KubernetesClusterNodePool#kernel_threads_max}.'''
        result = self._values.get("kernel_threads_max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_core_netdev_max_backlog(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_core_netdev_max_backlog KubernetesClusterNodePool#net_core_netdev_max_backlog}.'''
        result = self._values.get("net_core_netdev_max_backlog")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_core_optmem_max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_core_optmem_max KubernetesClusterNodePool#net_core_optmem_max}.'''
        result = self._values.get("net_core_optmem_max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_core_rmem_default(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_core_rmem_default KubernetesClusterNodePool#net_core_rmem_default}.'''
        result = self._values.get("net_core_rmem_default")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_core_rmem_max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_core_rmem_max KubernetesClusterNodePool#net_core_rmem_max}.'''
        result = self._values.get("net_core_rmem_max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_core_somaxconn(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_core_somaxconn KubernetesClusterNodePool#net_core_somaxconn}.'''
        result = self._values.get("net_core_somaxconn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_core_wmem_default(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_core_wmem_default KubernetesClusterNodePool#net_core_wmem_default}.'''
        result = self._values.get("net_core_wmem_default")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_core_wmem_max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_core_wmem_max KubernetesClusterNodePool#net_core_wmem_max}.'''
        result = self._values.get("net_core_wmem_max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_ip_local_port_range_max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_ip_local_port_range_max KubernetesClusterNodePool#net_ipv4_ip_local_port_range_max}.'''
        result = self._values.get("net_ipv4_ip_local_port_range_max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_ip_local_port_range_min(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_ip_local_port_range_min KubernetesClusterNodePool#net_ipv4_ip_local_port_range_min}.'''
        result = self._values.get("net_ipv4_ip_local_port_range_min")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_neigh_default_gc_thresh1(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_neigh_default_gc_thresh1 KubernetesClusterNodePool#net_ipv4_neigh_default_gc_thresh1}.'''
        result = self._values.get("net_ipv4_neigh_default_gc_thresh1")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_neigh_default_gc_thresh2(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_neigh_default_gc_thresh2 KubernetesClusterNodePool#net_ipv4_neigh_default_gc_thresh2}.'''
        result = self._values.get("net_ipv4_neigh_default_gc_thresh2")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_neigh_default_gc_thresh3(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_neigh_default_gc_thresh3 KubernetesClusterNodePool#net_ipv4_neigh_default_gc_thresh3}.'''
        result = self._values.get("net_ipv4_neigh_default_gc_thresh3")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_tcp_fin_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_tcp_fin_timeout KubernetesClusterNodePool#net_ipv4_tcp_fin_timeout}.'''
        result = self._values.get("net_ipv4_tcp_fin_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_tcp_keepalive_intvl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_tcp_keepalive_intvl KubernetesClusterNodePool#net_ipv4_tcp_keepalive_intvl}.'''
        result = self._values.get("net_ipv4_tcp_keepalive_intvl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_tcp_keepalive_probes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_tcp_keepalive_probes KubernetesClusterNodePool#net_ipv4_tcp_keepalive_probes}.'''
        result = self._values.get("net_ipv4_tcp_keepalive_probes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_tcp_keepalive_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_tcp_keepalive_time KubernetesClusterNodePool#net_ipv4_tcp_keepalive_time}.'''
        result = self._values.get("net_ipv4_tcp_keepalive_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_tcp_max_syn_backlog(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_tcp_max_syn_backlog KubernetesClusterNodePool#net_ipv4_tcp_max_syn_backlog}.'''
        result = self._values.get("net_ipv4_tcp_max_syn_backlog")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_tcp_max_tw_buckets(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_tcp_max_tw_buckets KubernetesClusterNodePool#net_ipv4_tcp_max_tw_buckets}.'''
        result = self._values.get("net_ipv4_tcp_max_tw_buckets")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_tcp_tw_reuse(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_ipv4_tcp_tw_reuse KubernetesClusterNodePool#net_ipv4_tcp_tw_reuse}.'''
        result = self._values.get("net_ipv4_tcp_tw_reuse")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def net_netfilter_nf_conntrack_buckets(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_netfilter_nf_conntrack_buckets KubernetesClusterNodePool#net_netfilter_nf_conntrack_buckets}.'''
        result = self._values.get("net_netfilter_nf_conntrack_buckets")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_netfilter_nf_conntrack_max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#net_netfilter_nf_conntrack_max KubernetesClusterNodePool#net_netfilter_nf_conntrack_max}.'''
        result = self._values.get("net_netfilter_nf_conntrack_max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vm_max_map_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#vm_max_map_count KubernetesClusterNodePool#vm_max_map_count}.'''
        result = self._values.get("vm_max_map_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vm_swappiness(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#vm_swappiness KubernetesClusterNodePool#vm_swappiness}.'''
        result = self._values.get("vm_swappiness")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vm_vfs_cache_pressure(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#vm_vfs_cache_pressure KubernetesClusterNodePool#vm_vfs_cache_pressure}.'''
        result = self._values.get("vm_vfs_cache_pressure")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterNodePoolLinuxOsConfigSysctlConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterNodePoolLinuxOsConfigSysctlConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesClusterNodePool.KubernetesClusterNodePoolLinuxOsConfigSysctlConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__acbe16c22fb32f6df7f14c7149ff1c6f717ee1750a4b2cfdbd73e1f4d4a537bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFsAioMaxNr")
    def reset_fs_aio_max_nr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFsAioMaxNr", []))

    @jsii.member(jsii_name="resetFsFileMax")
    def reset_fs_file_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFsFileMax", []))

    @jsii.member(jsii_name="resetFsInotifyMaxUserWatches")
    def reset_fs_inotify_max_user_watches(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFsInotifyMaxUserWatches", []))

    @jsii.member(jsii_name="resetFsNrOpen")
    def reset_fs_nr_open(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFsNrOpen", []))

    @jsii.member(jsii_name="resetKernelThreadsMax")
    def reset_kernel_threads_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKernelThreadsMax", []))

    @jsii.member(jsii_name="resetNetCoreNetdevMaxBacklog")
    def reset_net_core_netdev_max_backlog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetCoreNetdevMaxBacklog", []))

    @jsii.member(jsii_name="resetNetCoreOptmemMax")
    def reset_net_core_optmem_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetCoreOptmemMax", []))

    @jsii.member(jsii_name="resetNetCoreRmemDefault")
    def reset_net_core_rmem_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetCoreRmemDefault", []))

    @jsii.member(jsii_name="resetNetCoreRmemMax")
    def reset_net_core_rmem_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetCoreRmemMax", []))

    @jsii.member(jsii_name="resetNetCoreSomaxconn")
    def reset_net_core_somaxconn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetCoreSomaxconn", []))

    @jsii.member(jsii_name="resetNetCoreWmemDefault")
    def reset_net_core_wmem_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetCoreWmemDefault", []))

    @jsii.member(jsii_name="resetNetCoreWmemMax")
    def reset_net_core_wmem_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetCoreWmemMax", []))

    @jsii.member(jsii_name="resetNetIpv4IpLocalPortRangeMax")
    def reset_net_ipv4_ip_local_port_range_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4IpLocalPortRangeMax", []))

    @jsii.member(jsii_name="resetNetIpv4IpLocalPortRangeMin")
    def reset_net_ipv4_ip_local_port_range_min(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4IpLocalPortRangeMin", []))

    @jsii.member(jsii_name="resetNetIpv4NeighDefaultGcThresh1")
    def reset_net_ipv4_neigh_default_gc_thresh1(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4NeighDefaultGcThresh1", []))

    @jsii.member(jsii_name="resetNetIpv4NeighDefaultGcThresh2")
    def reset_net_ipv4_neigh_default_gc_thresh2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4NeighDefaultGcThresh2", []))

    @jsii.member(jsii_name="resetNetIpv4NeighDefaultGcThresh3")
    def reset_net_ipv4_neigh_default_gc_thresh3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4NeighDefaultGcThresh3", []))

    @jsii.member(jsii_name="resetNetIpv4TcpFinTimeout")
    def reset_net_ipv4_tcp_fin_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4TcpFinTimeout", []))

    @jsii.member(jsii_name="resetNetIpv4TcpKeepaliveIntvl")
    def reset_net_ipv4_tcp_keepalive_intvl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4TcpKeepaliveIntvl", []))

    @jsii.member(jsii_name="resetNetIpv4TcpKeepaliveProbes")
    def reset_net_ipv4_tcp_keepalive_probes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4TcpKeepaliveProbes", []))

    @jsii.member(jsii_name="resetNetIpv4TcpKeepaliveTime")
    def reset_net_ipv4_tcp_keepalive_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4TcpKeepaliveTime", []))

    @jsii.member(jsii_name="resetNetIpv4TcpMaxSynBacklog")
    def reset_net_ipv4_tcp_max_syn_backlog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4TcpMaxSynBacklog", []))

    @jsii.member(jsii_name="resetNetIpv4TcpMaxTwBuckets")
    def reset_net_ipv4_tcp_max_tw_buckets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4TcpMaxTwBuckets", []))

    @jsii.member(jsii_name="resetNetIpv4TcpTwReuse")
    def reset_net_ipv4_tcp_tw_reuse(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4TcpTwReuse", []))

    @jsii.member(jsii_name="resetNetNetfilterNfConntrackBuckets")
    def reset_net_netfilter_nf_conntrack_buckets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetNetfilterNfConntrackBuckets", []))

    @jsii.member(jsii_name="resetNetNetfilterNfConntrackMax")
    def reset_net_netfilter_nf_conntrack_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetNetfilterNfConntrackMax", []))

    @jsii.member(jsii_name="resetVmMaxMapCount")
    def reset_vm_max_map_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmMaxMapCount", []))

    @jsii.member(jsii_name="resetVmSwappiness")
    def reset_vm_swappiness(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmSwappiness", []))

    @jsii.member(jsii_name="resetVmVfsCachePressure")
    def reset_vm_vfs_cache_pressure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmVfsCachePressure", []))

    @builtins.property
    @jsii.member(jsii_name="fsAioMaxNrInput")
    def fs_aio_max_nr_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fsAioMaxNrInput"))

    @builtins.property
    @jsii.member(jsii_name="fsFileMaxInput")
    def fs_file_max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fsFileMaxInput"))

    @builtins.property
    @jsii.member(jsii_name="fsInotifyMaxUserWatchesInput")
    def fs_inotify_max_user_watches_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fsInotifyMaxUserWatchesInput"))

    @builtins.property
    @jsii.member(jsii_name="fsNrOpenInput")
    def fs_nr_open_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fsNrOpenInput"))

    @builtins.property
    @jsii.member(jsii_name="kernelThreadsMaxInput")
    def kernel_threads_max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "kernelThreadsMaxInput"))

    @builtins.property
    @jsii.member(jsii_name="netCoreNetdevMaxBacklogInput")
    def net_core_netdev_max_backlog_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netCoreNetdevMaxBacklogInput"))

    @builtins.property
    @jsii.member(jsii_name="netCoreOptmemMaxInput")
    def net_core_optmem_max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netCoreOptmemMaxInput"))

    @builtins.property
    @jsii.member(jsii_name="netCoreRmemDefaultInput")
    def net_core_rmem_default_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netCoreRmemDefaultInput"))

    @builtins.property
    @jsii.member(jsii_name="netCoreRmemMaxInput")
    def net_core_rmem_max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netCoreRmemMaxInput"))

    @builtins.property
    @jsii.member(jsii_name="netCoreSomaxconnInput")
    def net_core_somaxconn_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netCoreSomaxconnInput"))

    @builtins.property
    @jsii.member(jsii_name="netCoreWmemDefaultInput")
    def net_core_wmem_default_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netCoreWmemDefaultInput"))

    @builtins.property
    @jsii.member(jsii_name="netCoreWmemMaxInput")
    def net_core_wmem_max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netCoreWmemMaxInput"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4IpLocalPortRangeMaxInput")
    def net_ipv4_ip_local_port_range_max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netIpv4IpLocalPortRangeMaxInput"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4IpLocalPortRangeMinInput")
    def net_ipv4_ip_local_port_range_min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netIpv4IpLocalPortRangeMinInput"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4NeighDefaultGcThresh1Input")
    def net_ipv4_neigh_default_gc_thresh1_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netIpv4NeighDefaultGcThresh1Input"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4NeighDefaultGcThresh2Input")
    def net_ipv4_neigh_default_gc_thresh2_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netIpv4NeighDefaultGcThresh2Input"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4NeighDefaultGcThresh3Input")
    def net_ipv4_neigh_default_gc_thresh3_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netIpv4NeighDefaultGcThresh3Input"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpFinTimeoutInput")
    def net_ipv4_tcp_fin_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netIpv4TcpFinTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpKeepaliveIntvlInput")
    def net_ipv4_tcp_keepalive_intvl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netIpv4TcpKeepaliveIntvlInput"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpKeepaliveProbesInput")
    def net_ipv4_tcp_keepalive_probes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netIpv4TcpKeepaliveProbesInput"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpKeepaliveTimeInput")
    def net_ipv4_tcp_keepalive_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netIpv4TcpKeepaliveTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpMaxSynBacklogInput")
    def net_ipv4_tcp_max_syn_backlog_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netIpv4TcpMaxSynBacklogInput"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpMaxTwBucketsInput")
    def net_ipv4_tcp_max_tw_buckets_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netIpv4TcpMaxTwBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpTwReuseInput")
    def net_ipv4_tcp_tw_reuse_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "netIpv4TcpTwReuseInput"))

    @builtins.property
    @jsii.member(jsii_name="netNetfilterNfConntrackBucketsInput")
    def net_netfilter_nf_conntrack_buckets_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netNetfilterNfConntrackBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="netNetfilterNfConntrackMaxInput")
    def net_netfilter_nf_conntrack_max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netNetfilterNfConntrackMaxInput"))

    @builtins.property
    @jsii.member(jsii_name="vmMaxMapCountInput")
    def vm_max_map_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vmMaxMapCountInput"))

    @builtins.property
    @jsii.member(jsii_name="vmSwappinessInput")
    def vm_swappiness_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vmSwappinessInput"))

    @builtins.property
    @jsii.member(jsii_name="vmVfsCachePressureInput")
    def vm_vfs_cache_pressure_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vmVfsCachePressureInput"))

    @builtins.property
    @jsii.member(jsii_name="fsAioMaxNr")
    def fs_aio_max_nr(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fsAioMaxNr"))

    @fs_aio_max_nr.setter
    def fs_aio_max_nr(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ef0798213f6760b5b0c0673ffaf4adb3060d454df5af975d4dfd67e79d564c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsAioMaxNr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fsFileMax")
    def fs_file_max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fsFileMax"))

    @fs_file_max.setter
    def fs_file_max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae39ab0dec3709871665bf830df38620ed805e9e11c3da8fc776b7a8f2ae753f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsFileMax", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fsInotifyMaxUserWatches")
    def fs_inotify_max_user_watches(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fsInotifyMaxUserWatches"))

    @fs_inotify_max_user_watches.setter
    def fs_inotify_max_user_watches(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35b2e08a92e210c21d17437971dafe14189a3471869ca742d17d038c405e592a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsInotifyMaxUserWatches", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fsNrOpen")
    def fs_nr_open(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fsNrOpen"))

    @fs_nr_open.setter
    def fs_nr_open(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f9537fab7b51975f9263b7f267f0be1d7c4760733a68abe865a8f37a5493fd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsNrOpen", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kernelThreadsMax")
    def kernel_threads_max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "kernelThreadsMax"))

    @kernel_threads_max.setter
    def kernel_threads_max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b789fa7c4a16b34f923229f16fe83a38b23655023d323d9aa96ad2d42748534c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kernelThreadsMax", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netCoreNetdevMaxBacklog")
    def net_core_netdev_max_backlog(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netCoreNetdevMaxBacklog"))

    @net_core_netdev_max_backlog.setter
    def net_core_netdev_max_backlog(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36cb59b745c732bde404a3eca420972c4c32dfab2e9da1d3f76b1579652d114b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netCoreNetdevMaxBacklog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netCoreOptmemMax")
    def net_core_optmem_max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netCoreOptmemMax"))

    @net_core_optmem_max.setter
    def net_core_optmem_max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7c44edee6d6f3079c85855cd8ed4c7c2468392e8c75ab9e03a5ba4029d26ea7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netCoreOptmemMax", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netCoreRmemDefault")
    def net_core_rmem_default(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netCoreRmemDefault"))

    @net_core_rmem_default.setter
    def net_core_rmem_default(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08f88cc2c1347d74d3c879535028420394d2fb8a6dd4d7e3408bfbd27b9f5939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netCoreRmemDefault", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netCoreRmemMax")
    def net_core_rmem_max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netCoreRmemMax"))

    @net_core_rmem_max.setter
    def net_core_rmem_max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b76e45a05cd005f3d3d633615ad6437f6651196b70ad5136c8a9042e586a6eda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netCoreRmemMax", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netCoreSomaxconn")
    def net_core_somaxconn(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netCoreSomaxconn"))

    @net_core_somaxconn.setter
    def net_core_somaxconn(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a9af2ed5d7a8bd6b10c66ed70e239227d85a9c605aa6ad3cf773555a21fb91b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netCoreSomaxconn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netCoreWmemDefault")
    def net_core_wmem_default(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netCoreWmemDefault"))

    @net_core_wmem_default.setter
    def net_core_wmem_default(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7142ac7e2272a56552cba2510539b272d9c2d5bca24243b69b598c8d4c9bac9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netCoreWmemDefault", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netCoreWmemMax")
    def net_core_wmem_max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netCoreWmemMax"))

    @net_core_wmem_max.setter
    def net_core_wmem_max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f011dc323323c76783bdaf55330023d15ca852b9e9b1eeef6e396e6f53c5d85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netCoreWmemMax", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netIpv4IpLocalPortRangeMax")
    def net_ipv4_ip_local_port_range_max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netIpv4IpLocalPortRangeMax"))

    @net_ipv4_ip_local_port_range_max.setter
    def net_ipv4_ip_local_port_range_max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05c5a69f8fd5c423c2604e377eee8d43d04fdc36d0a8827806295c557e92814a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4IpLocalPortRangeMax", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netIpv4IpLocalPortRangeMin")
    def net_ipv4_ip_local_port_range_min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netIpv4IpLocalPortRangeMin"))

    @net_ipv4_ip_local_port_range_min.setter
    def net_ipv4_ip_local_port_range_min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ea994a4115a6bed7a7c40c242710c3065ca0213565ed6a13b82cc540df5c257)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4IpLocalPortRangeMin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netIpv4NeighDefaultGcThresh1")
    def net_ipv4_neigh_default_gc_thresh1(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netIpv4NeighDefaultGcThresh1"))

    @net_ipv4_neigh_default_gc_thresh1.setter
    def net_ipv4_neigh_default_gc_thresh1(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5607d573224d93ebd58ba06997485e90c1c8d2d16ee426c2e8363739e827f3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4NeighDefaultGcThresh1", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netIpv4NeighDefaultGcThresh2")
    def net_ipv4_neigh_default_gc_thresh2(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netIpv4NeighDefaultGcThresh2"))

    @net_ipv4_neigh_default_gc_thresh2.setter
    def net_ipv4_neigh_default_gc_thresh2(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c3e62b30862b0a98bd2738a82979445beb41a20e9848c37b16f7ae4471cef1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4NeighDefaultGcThresh2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netIpv4NeighDefaultGcThresh3")
    def net_ipv4_neigh_default_gc_thresh3(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netIpv4NeighDefaultGcThresh3"))

    @net_ipv4_neigh_default_gc_thresh3.setter
    def net_ipv4_neigh_default_gc_thresh3(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6932437dcbe2934677c03ad081d8b9772bdea0a1f83ad62090be81a0e266bc8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4NeighDefaultGcThresh3", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpFinTimeout")
    def net_ipv4_tcp_fin_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netIpv4TcpFinTimeout"))

    @net_ipv4_tcp_fin_timeout.setter
    def net_ipv4_tcp_fin_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf82c490e54563e4218b52d7c14804bdb50860c50f9b6538114a4442262480d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4TcpFinTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpKeepaliveIntvl")
    def net_ipv4_tcp_keepalive_intvl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netIpv4TcpKeepaliveIntvl"))

    @net_ipv4_tcp_keepalive_intvl.setter
    def net_ipv4_tcp_keepalive_intvl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50ad6b664e138996aad6a9f064e3e76a6bd52fdc87c9e36704c00e39cfa376b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4TcpKeepaliveIntvl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpKeepaliveProbes")
    def net_ipv4_tcp_keepalive_probes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netIpv4TcpKeepaliveProbes"))

    @net_ipv4_tcp_keepalive_probes.setter
    def net_ipv4_tcp_keepalive_probes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed454c7a7e4d34e194fe84e25cc4cbd616cb259a748c788122579fe8887f44b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4TcpKeepaliveProbes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpKeepaliveTime")
    def net_ipv4_tcp_keepalive_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netIpv4TcpKeepaliveTime"))

    @net_ipv4_tcp_keepalive_time.setter
    def net_ipv4_tcp_keepalive_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0df3a915bd549d3e3e3e30edb5f08f0e646fb90f855ab10a105ad40ac91e25b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4TcpKeepaliveTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpMaxSynBacklog")
    def net_ipv4_tcp_max_syn_backlog(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netIpv4TcpMaxSynBacklog"))

    @net_ipv4_tcp_max_syn_backlog.setter
    def net_ipv4_tcp_max_syn_backlog(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dcd09bd3ad1867295e94f723c5f32daa8c02d310ab12fecf670102bf6391358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4TcpMaxSynBacklog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpMaxTwBuckets")
    def net_ipv4_tcp_max_tw_buckets(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netIpv4TcpMaxTwBuckets"))

    @net_ipv4_tcp_max_tw_buckets.setter
    def net_ipv4_tcp_max_tw_buckets(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c928f1b4b45550ef8efdba6dbfab4449b104b4288828774d2a14d7e5457a093)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4TcpMaxTwBuckets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpTwReuse")
    def net_ipv4_tcp_tw_reuse(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "netIpv4TcpTwReuse"))

    @net_ipv4_tcp_tw_reuse.setter
    def net_ipv4_tcp_tw_reuse(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__985fb15e9ad6f8a5cae66e0978817dd62709286c63abcb06d5655a0f8d0599b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4TcpTwReuse", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netNetfilterNfConntrackBuckets")
    def net_netfilter_nf_conntrack_buckets(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netNetfilterNfConntrackBuckets"))

    @net_netfilter_nf_conntrack_buckets.setter
    def net_netfilter_nf_conntrack_buckets(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00978639027c69d22728d8162b91617dd9d285a3662e6c8a5d45983afef7aa60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netNetfilterNfConntrackBuckets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netNetfilterNfConntrackMax")
    def net_netfilter_nf_conntrack_max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netNetfilterNfConntrackMax"))

    @net_netfilter_nf_conntrack_max.setter
    def net_netfilter_nf_conntrack_max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b87c7c44c49e0a29c45d3c40464ff7b08390a1bca7d4f37d18f019cde120b067)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netNetfilterNfConntrackMax", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmMaxMapCount")
    def vm_max_map_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vmMaxMapCount"))

    @vm_max_map_count.setter
    def vm_max_map_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__466368803b84539932ffce540162249d0317344b58bd278949e815f3ca895df8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmMaxMapCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSwappiness")
    def vm_swappiness(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vmSwappiness"))

    @vm_swappiness.setter
    def vm_swappiness(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d84bff48dc8f260f18a38b97d44a8e8af546fec99981ae0812644dac01ef7669)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSwappiness", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmVfsCachePressure")
    def vm_vfs_cache_pressure(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vmVfsCachePressure"))

    @vm_vfs_cache_pressure.setter
    def vm_vfs_cache_pressure(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea83a0eedf9235892cc22a019be8442306c402bb533942cf7772ae2dca4b1038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmVfsCachePressure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesClusterNodePoolLinuxOsConfigSysctlConfig]:
        return typing.cast(typing.Optional[KubernetesClusterNodePoolLinuxOsConfigSysctlConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterNodePoolLinuxOsConfigSysctlConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b636cd30e04953337b93a5a48a692f2ac19ef8e443a64ce8741e6fa5663a3b31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesClusterNodePool.KubernetesClusterNodePoolNodeNetworkProfile",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_host_ports": "allowedHostPorts",
        "application_security_group_ids": "applicationSecurityGroupIds",
        "node_public_ip_tags": "nodePublicIpTags",
    },
)
class KubernetesClusterNodePoolNodeNetworkProfile:
    def __init__(
        self,
        *,
        allowed_host_ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPorts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        application_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        node_public_ip_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_host_ports: allowed_host_ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#allowed_host_ports KubernetesClusterNodePool#allowed_host_ports}
        :param application_security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#application_security_group_ids KubernetesClusterNodePool#application_security_group_ids}.
        :param node_public_ip_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_public_ip_tags KubernetesClusterNodePool#node_public_ip_tags}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e8b7efc36677826b72e2d473b125633f7f07906f50f5f661b1db04bb1879746)
            check_type(argname="argument allowed_host_ports", value=allowed_host_ports, expected_type=type_hints["allowed_host_ports"])
            check_type(argname="argument application_security_group_ids", value=application_security_group_ids, expected_type=type_hints["application_security_group_ids"])
            check_type(argname="argument node_public_ip_tags", value=node_public_ip_tags, expected_type=type_hints["node_public_ip_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_host_ports is not None:
            self._values["allowed_host_ports"] = allowed_host_ports
        if application_security_group_ids is not None:
            self._values["application_security_group_ids"] = application_security_group_ids
        if node_public_ip_tags is not None:
            self._values["node_public_ip_tags"] = node_public_ip_tags

    @builtins.property
    def allowed_host_ports(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPorts"]]]:
        '''allowed_host_ports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#allowed_host_ports KubernetesClusterNodePool#allowed_host_ports}
        '''
        result = self._values.get("allowed_host_ports")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPorts"]]], result)

    @builtins.property
    def application_security_group_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#application_security_group_ids KubernetesClusterNodePool#application_security_group_ids}.'''
        result = self._values.get("application_security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def node_public_ip_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_public_ip_tags KubernetesClusterNodePool#node_public_ip_tags}.'''
        result = self._values.get("node_public_ip_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterNodePoolNodeNetworkProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesClusterNodePool.KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPorts",
    jsii_struct_bases=[],
    name_mapping={
        "port_end": "portEnd",
        "port_start": "portStart",
        "protocol": "protocol",
    },
)
class KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPorts:
    def __init__(
        self,
        *,
        port_end: typing.Optional[jsii.Number] = None,
        port_start: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port_end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#port_end KubernetesClusterNodePool#port_end}.
        :param port_start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#port_start KubernetesClusterNodePool#port_start}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#protocol KubernetesClusterNodePool#protocol}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2c9b34e2b2e73fb2fe0e169b91874604074a04a875fb61d2db99b8054b42b5a)
            check_type(argname="argument port_end", value=port_end, expected_type=type_hints["port_end"])
            check_type(argname="argument port_start", value=port_start, expected_type=type_hints["port_start"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if port_end is not None:
            self._values["port_end"] = port_end
        if port_start is not None:
            self._values["port_start"] = port_start
        if protocol is not None:
            self._values["protocol"] = protocol

    @builtins.property
    def port_end(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#port_end KubernetesClusterNodePool#port_end}.'''
        result = self._values.get("port_end")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_start(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#port_start KubernetesClusterNodePool#port_start}.'''
        result = self._values.get("port_start")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#protocol KubernetesClusterNodePool#protocol}.'''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPortsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesClusterNodePool.KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPortsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1c91ff26ac0d56e062783ec61b6f523430952ab07995bdd767dbec276560cda)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPortsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d1f46d95ae3fe71fc6a62e16dd88080d01f5f1ca6f3da6c7769cc9ef03e57c6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPortsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a967c3adab72feeb341451c343d99872a8b51dc00348fd6c7b7fca0b6c5654b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aca6b77516e8b35ae585d88598141de0748a01e6e89f94ce1e7e517dc055a5a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db4516bf3a750edacb2a3def70836f37a5bcc7470283f778003f94b54920d2b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPorts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPorts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPorts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b25f00824f383429fa72a79893fe846ae08dc25dd2a24af4e94a36097a94293b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPortsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesClusterNodePool.KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPortsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b58cd5b4983b23c32a87466ee404956ddabea74e6f41a52fbcb86f2dd43adf78)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPortEnd")
    def reset_port_end(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortEnd", []))

    @jsii.member(jsii_name="resetPortStart")
    def reset_port_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortStart", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @builtins.property
    @jsii.member(jsii_name="portEndInput")
    def port_end_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portEndInput"))

    @builtins.property
    @jsii.member(jsii_name="portStartInput")
    def port_start_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portStartInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="portEnd")
    def port_end(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "portEnd"))

    @port_end.setter
    def port_end(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55a8ba8080def2f766f2776e68b63f910b5fa121cf1eb19a4ec67a8c5577968c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portEnd", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portStart")
    def port_start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "portStart"))

    @port_start.setter
    def port_start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a30390613f4b55cc70acadaa9b77c63f9acebe64e0db29d82567a052de39128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portStart", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea583f96779bf97e03cb9969790662b10db8e61533750947ac58607ad5123e2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPorts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPorts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPorts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61b88db040a34e3f4855d15e80efc40e1b4a6ccfbcbdb5c12b64c386dcd48f2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KubernetesClusterNodePoolNodeNetworkProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesClusterNodePool.KubernetesClusterNodePoolNodeNetworkProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a0f72d068d36f3cf5c7d7be2684ecfff76336441d7f10ad9e403c6d2c299a3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAllowedHostPorts")
    def put_allowed_host_ports(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPorts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23ef0719eed183226aa5288a5584221ca39c570cb7d1ab1096daa15b860e3ba3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllowedHostPorts", [value]))

    @jsii.member(jsii_name="resetAllowedHostPorts")
    def reset_allowed_host_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedHostPorts", []))

    @jsii.member(jsii_name="resetApplicationSecurityGroupIds")
    def reset_application_security_group_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationSecurityGroupIds", []))

    @jsii.member(jsii_name="resetNodePublicIpTags")
    def reset_node_public_ip_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodePublicIpTags", []))

    @builtins.property
    @jsii.member(jsii_name="allowedHostPorts")
    def allowed_host_ports(
        self,
    ) -> KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPortsList:
        return typing.cast(KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPortsList, jsii.get(self, "allowedHostPorts"))

    @builtins.property
    @jsii.member(jsii_name="allowedHostPortsInput")
    def allowed_host_ports_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPorts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPorts]]], jsii.get(self, "allowedHostPortsInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationSecurityGroupIdsInput")
    def application_security_group_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "applicationSecurityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="nodePublicIpTagsInput")
    def node_public_ip_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "nodePublicIpTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationSecurityGroupIds")
    def application_security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "applicationSecurityGroupIds"))

    @application_security_group_ids.setter
    def application_security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b654fc050ee2d40d3434192ba4ed0ee228158c1ac811b745ef4d4a1f2b2317ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationSecurityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodePublicIpTags")
    def node_public_ip_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "nodePublicIpTags"))

    @node_public_ip_tags.setter
    def node_public_ip_tags(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc6741b11980fe9680cdf74cb0b75549345401bd788ed2cf1ffe1580bc76719d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodePublicIpTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesClusterNodePoolNodeNetworkProfile]:
        return typing.cast(typing.Optional[KubernetesClusterNodePoolNodeNetworkProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterNodePoolNodeNetworkProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5efae05489cdecd2a726f93777268892f5acf9b2f085ce42a22ffdff08cd0940)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesClusterNodePool.KubernetesClusterNodePoolTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class KubernetesClusterNodePoolTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#create KubernetesClusterNodePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#delete KubernetesClusterNodePool#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#read KubernetesClusterNodePool#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#update KubernetesClusterNodePool#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71bd060ef987d357ac06939eb259d744fc024013e8766322815e9daedc44e177)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#create KubernetesClusterNodePool#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#delete KubernetesClusterNodePool#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#read KubernetesClusterNodePool#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#update KubernetesClusterNodePool#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterNodePoolTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterNodePoolTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesClusterNodePool.KubernetesClusterNodePoolTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7af117bad2117253f6538630702592ae6859fda1da7357663e8c3442591c9b2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__69b7e3eaf080ff6a1dcde1b14537eaeee891733df9846fb6291af4625f75faf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4334e65542deb23fe4d2fe55a7afb578d4569dc695604d212834e9fe11d8d2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43f0a3a68581fede504a122da5534e1cfb6f9b3e17014db0c1546ad8d710d10a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ad4e1dfd0f4e63d2a3bf2864bd756df56d462c0f44ac7d47a99a162e1a0d103)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesClusterNodePoolTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesClusterNodePoolTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesClusterNodePoolTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21936f3773606dc1547bcceaa5ad4158159a5d8817b7b0ca60f9e072fe9d5965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesClusterNodePool.KubernetesClusterNodePoolUpgradeSettings",
    jsii_struct_bases=[],
    name_mapping={
        "max_surge": "maxSurge",
        "drain_timeout_in_minutes": "drainTimeoutInMinutes",
        "node_soak_duration_in_minutes": "nodeSoakDurationInMinutes",
    },
)
class KubernetesClusterNodePoolUpgradeSettings:
    def __init__(
        self,
        *,
        max_surge: builtins.str,
        drain_timeout_in_minutes: typing.Optional[jsii.Number] = None,
        node_soak_duration_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_surge: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#max_surge KubernetesClusterNodePool#max_surge}.
        :param drain_timeout_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#drain_timeout_in_minutes KubernetesClusterNodePool#drain_timeout_in_minutes}.
        :param node_soak_duration_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_soak_duration_in_minutes KubernetesClusterNodePool#node_soak_duration_in_minutes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__817b7bf9975f86719026dd8b63ccae540e40be10cd5846fab03abc2614401cac)
            check_type(argname="argument max_surge", value=max_surge, expected_type=type_hints["max_surge"])
            check_type(argname="argument drain_timeout_in_minutes", value=drain_timeout_in_minutes, expected_type=type_hints["drain_timeout_in_minutes"])
            check_type(argname="argument node_soak_duration_in_minutes", value=node_soak_duration_in_minutes, expected_type=type_hints["node_soak_duration_in_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_surge": max_surge,
        }
        if drain_timeout_in_minutes is not None:
            self._values["drain_timeout_in_minutes"] = drain_timeout_in_minutes
        if node_soak_duration_in_minutes is not None:
            self._values["node_soak_duration_in_minutes"] = node_soak_duration_in_minutes

    @builtins.property
    def max_surge(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#max_surge KubernetesClusterNodePool#max_surge}.'''
        result = self._values.get("max_surge")
        assert result is not None, "Required property 'max_surge' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def drain_timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#drain_timeout_in_minutes KubernetesClusterNodePool#drain_timeout_in_minutes}.'''
        result = self._values.get("drain_timeout_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def node_soak_duration_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#node_soak_duration_in_minutes KubernetesClusterNodePool#node_soak_duration_in_minutes}.'''
        result = self._values.get("node_soak_duration_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterNodePoolUpgradeSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterNodePoolUpgradeSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesClusterNodePool.KubernetesClusterNodePoolUpgradeSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9849f8ed41ed16d40bf628ad07ae65301cc74c1c27fc55c7888681e56c40d6e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDrainTimeoutInMinutes")
    def reset_drain_timeout_in_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDrainTimeoutInMinutes", []))

    @jsii.member(jsii_name="resetNodeSoakDurationInMinutes")
    def reset_node_soak_duration_in_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeSoakDurationInMinutes", []))

    @builtins.property
    @jsii.member(jsii_name="drainTimeoutInMinutesInput")
    def drain_timeout_in_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "drainTimeoutInMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="maxSurgeInput")
    def max_surge_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxSurgeInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeSoakDurationInMinutesInput")
    def node_soak_duration_in_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeSoakDurationInMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="drainTimeoutInMinutes")
    def drain_timeout_in_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "drainTimeoutInMinutes"))

    @drain_timeout_in_minutes.setter
    def drain_timeout_in_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55a4a83a584ffeb0fdeec2c920e90c3bb78735d6b20e91c582af0534cb50e092)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "drainTimeoutInMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxSurge")
    def max_surge(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxSurge"))

    @max_surge.setter
    def max_surge(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bbdae63cb665050f84381e32a3e12d43dad0dc81ac6f3b4c4ec56d79331db68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSurge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeSoakDurationInMinutes")
    def node_soak_duration_in_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeSoakDurationInMinutes"))

    @node_soak_duration_in_minutes.setter
    def node_soak_duration_in_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86d071551df742d512c5c1d6a1cc3c98a3e03f0ab5a22e4bd0a2f67b6fd3522f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeSoakDurationInMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesClusterNodePoolUpgradeSettings]:
        return typing.cast(typing.Optional[KubernetesClusterNodePoolUpgradeSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterNodePoolUpgradeSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d9868f096466c0bd1206964e0698a8069bfaf854eeac56815e471086bf6b1c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesClusterNodePool.KubernetesClusterNodePoolWindowsProfile",
    jsii_struct_bases=[],
    name_mapping={"outbound_nat_enabled": "outboundNatEnabled"},
)
class KubernetesClusterNodePoolWindowsProfile:
    def __init__(
        self,
        *,
        outbound_nat_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param outbound_nat_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#outbound_nat_enabled KubernetesClusterNodePool#outbound_nat_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a1ce4370a82cb5899dbd3f13abb23aed73e6f17f0c09c4cdb62c46b42819ea5)
            check_type(argname="argument outbound_nat_enabled", value=outbound_nat_enabled, expected_type=type_hints["outbound_nat_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if outbound_nat_enabled is not None:
            self._values["outbound_nat_enabled"] = outbound_nat_enabled

    @builtins.property
    def outbound_nat_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_cluster_node_pool#outbound_nat_enabled KubernetesClusterNodePool#outbound_nat_enabled}.'''
        result = self._values.get("outbound_nat_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterNodePoolWindowsProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterNodePoolWindowsProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesClusterNodePool.KubernetesClusterNodePoolWindowsProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f060b99a0f57e1db54ad7638c1a96ddd780856ba20621107a0668cdcecf1a70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOutboundNatEnabled")
    def reset_outbound_nat_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutboundNatEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="outboundNatEnabledInput")
    def outbound_nat_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "outboundNatEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="outboundNatEnabled")
    def outbound_nat_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "outboundNatEnabled"))

    @outbound_nat_enabled.setter
    def outbound_nat_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09e9eb1bbe128b2fd2cebbb29871fdfc18644b5b62174a2b97bc6ce81fc78338)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outboundNatEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesClusterNodePoolWindowsProfile]:
        return typing.cast(typing.Optional[KubernetesClusterNodePoolWindowsProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterNodePoolWindowsProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0ee4291b4170a30562575706466861f0a4a51f00adce38f4a305a8283737664)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "KubernetesClusterNodePool",
    "KubernetesClusterNodePoolConfig",
    "KubernetesClusterNodePoolKubeletConfig",
    "KubernetesClusterNodePoolKubeletConfigOutputReference",
    "KubernetesClusterNodePoolLinuxOsConfig",
    "KubernetesClusterNodePoolLinuxOsConfigOutputReference",
    "KubernetesClusterNodePoolLinuxOsConfigSysctlConfig",
    "KubernetesClusterNodePoolLinuxOsConfigSysctlConfigOutputReference",
    "KubernetesClusterNodePoolNodeNetworkProfile",
    "KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPorts",
    "KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPortsList",
    "KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPortsOutputReference",
    "KubernetesClusterNodePoolNodeNetworkProfileOutputReference",
    "KubernetesClusterNodePoolTimeouts",
    "KubernetesClusterNodePoolTimeoutsOutputReference",
    "KubernetesClusterNodePoolUpgradeSettings",
    "KubernetesClusterNodePoolUpgradeSettingsOutputReference",
    "KubernetesClusterNodePoolWindowsProfile",
    "KubernetesClusterNodePoolWindowsProfileOutputReference",
]

publication.publish()

def _typecheckingstub__d0bd62d7b5f759647639a7cb4635a5600065706b12c089287fa9579360cd8b7e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    kubernetes_cluster_id: builtins.str,
    name: builtins.str,
    auto_scaling_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    capacity_reservation_group_id: typing.Optional[builtins.str] = None,
    eviction_policy: typing.Optional[builtins.str] = None,
    fips_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gpu_instance: typing.Optional[builtins.str] = None,
    host_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    host_group_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kubelet_config: typing.Optional[typing.Union[KubernetesClusterNodePoolKubeletConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    kubelet_disk_type: typing.Optional[builtins.str] = None,
    linux_os_config: typing.Optional[typing.Union[KubernetesClusterNodePoolLinuxOsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    max_count: typing.Optional[jsii.Number] = None,
    max_pods: typing.Optional[jsii.Number] = None,
    min_count: typing.Optional[jsii.Number] = None,
    mode: typing.Optional[builtins.str] = None,
    node_count: typing.Optional[jsii.Number] = None,
    node_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_network_profile: typing.Optional[typing.Union[KubernetesClusterNodePoolNodeNetworkProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    node_public_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    node_public_ip_prefix_id: typing.Optional[builtins.str] = None,
    node_taints: typing.Optional[typing.Sequence[builtins.str]] = None,
    orchestrator_version: typing.Optional[builtins.str] = None,
    os_disk_size_gb: typing.Optional[jsii.Number] = None,
    os_disk_type: typing.Optional[builtins.str] = None,
    os_sku: typing.Optional[builtins.str] = None,
    os_type: typing.Optional[builtins.str] = None,
    pod_subnet_id: typing.Optional[builtins.str] = None,
    priority: typing.Optional[builtins.str] = None,
    proximity_placement_group_id: typing.Optional[builtins.str] = None,
    scale_down_mode: typing.Optional[builtins.str] = None,
    snapshot_id: typing.Optional[builtins.str] = None,
    spot_max_price: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    temporary_name_for_rotation: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[KubernetesClusterNodePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    ultra_ssd_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    upgrade_settings: typing.Optional[typing.Union[KubernetesClusterNodePoolUpgradeSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    vm_size: typing.Optional[builtins.str] = None,
    vnet_subnet_id: typing.Optional[builtins.str] = None,
    windows_profile: typing.Optional[typing.Union[KubernetesClusterNodePoolWindowsProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    workload_runtime: typing.Optional[builtins.str] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__223e65c859bb70ae8d5eed2a0cc86d59d5a7dc1a12bd909c3890ba2f8478eabf(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__167864874165cfff64977fa215d5b2f42ccd00fdc5e38889ed6f5b1f63a722e5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c34f6c96f7bd779ba2f99fea1b20d0e5d3647c76a041c57d79e91f20844313(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6378be86b341bb4e1a4d5cbb3ac0607b18429a1c81b58605f7a7b16ae2acd80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b917aa6a1f15723d3793483d2f617c2237a43308c808689a3889673ace1a3f7b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24968835fa86b6172e59adfc6866cb769b19bb52ef20bcb8d1b44e20be82797e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4991d9f7d90c9dfd2fe0ce156086dfd78f9b51c4fc838de58a7e43cc0906af83(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f5f522c670879d0c619a12270cef86883d6d8a6f1720efc83ba29ba3bf1b35e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__245b86c17dda364f5f03e235f86d208861da27826643357335dead4f9a3c7904(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60ce3c0a59f4d1884c8544121b98ab13ed3452d658837f8bfb70eb08228d2f09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b9811cca28bf984b19fe6ec2f0a3cb421b62da89f8ed802d6b81007d85c975(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43bb452be8aeee0ab247171b47fd8894b4e83a7e221e10ac29f72fe41f4d83e2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__551f794a57c4c15ab406b4c49eff0b9b90ae12e0998910b648541136c7809023(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af0291b8c89839477e78c74e6a7d0536b2968c1eb91da09d7bbd8f1d972b5da(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a736bfe65d1b125732b2c3bf6f65c100606f603b2a3205d30990edf0871fa841(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827676f3929d5c4593096446958aa882ef10dd1b8e06dfea60ea6a77615c380d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__003068d88a2b600306da583d699a396df9a6a3e62462df65c0043e753c2acddd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0b1a881cd4f99c63ee8a9d31a89c2845097fb4d6958fa9a4863f827d923d574(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea2ee568cb937ed11e70d22dbf05f77b104ec8521f87a8c068f9e92b17ed3824(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81c800dc05c93e76d519b0d967160bce1ffcd76fda511ea53b6d2ad77f0cf4f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f4b8e1a78d1de0033f118c4420202a8482f9943c7f96851845b1625746e700a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1734413818bbe4e135b76b4f39883fbb557eae6d663e9cff6eddff5499cf16b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e333d4a3de77a72a6ee6d2f4d8ab0cc366adfa5b8d8234ca94f9124c2ea10d8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f9566e5d6918ebb9e19890f5dafa2e13dbdbd1b6ebf7144a2d5bb145aecd617(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3481c96ee62507b18a5cf4161a201206d27ed1199cc49a231f675ed921276461(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1019b6c18c885deb2c7d025829eb3c749bbece311f606f4e7f27ed670f8a367(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__432bc065df3a862261baae4027e912d266a8824e6d532815f68b7dd440d13cfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ee6f64deb03916e11a8fd38210055b9dd72935e2a0e5c4249ed8458cb270fd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9900d99f5116f7034f8d96951f9d10e9170964bf63bf322cd7cc94fb694c7c32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c7b2918ca56a4a1ad192c984d53c98f127b93bb53501b7d3e030673ecf901cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d324c38872acc50f857805b3eb5c82fb854ab1e7f63e201f9793a0949057837(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7c5485ae3346a677dc66f44f18e24b3a2e641ceaaf419fbb2f8bbfb8f03fd05(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91622fb844d261232dedbc0862c653857b52f6a267b1a717ae06d5de78d5f7a9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51307bbe0bbf03160430b73860c224570db509cb1c6c139f43e18f8881d6950f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd92f95fac9b1591a8116e1ac45ad7363c25864e87b4b7d3f85f812c46acf9a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7cd92dd811d547087e26d8ab71207498cc5c5f50e12a2d411ab5f4f087ee77f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d1e125e1b90431a1c2dca15424b4206d261d66db6240d55388dba97478c486(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19d425137d149bba9ad06f799be81914e803a64ef1b08a7115d4c4eba50e8e7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfbf2864c2a2e9f5f1ca47d8d9d14459401d7f2b521fde02d4fa6f96b1c79d57(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c2d91fe666235d7809d5d2b18e809ed38c78296d1653d0cf628ecd4ab1dd42(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    kubernetes_cluster_id: builtins.str,
    name: builtins.str,
    auto_scaling_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    capacity_reservation_group_id: typing.Optional[builtins.str] = None,
    eviction_policy: typing.Optional[builtins.str] = None,
    fips_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gpu_instance: typing.Optional[builtins.str] = None,
    host_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    host_group_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kubelet_config: typing.Optional[typing.Union[KubernetesClusterNodePoolKubeletConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    kubelet_disk_type: typing.Optional[builtins.str] = None,
    linux_os_config: typing.Optional[typing.Union[KubernetesClusterNodePoolLinuxOsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    max_count: typing.Optional[jsii.Number] = None,
    max_pods: typing.Optional[jsii.Number] = None,
    min_count: typing.Optional[jsii.Number] = None,
    mode: typing.Optional[builtins.str] = None,
    node_count: typing.Optional[jsii.Number] = None,
    node_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_network_profile: typing.Optional[typing.Union[KubernetesClusterNodePoolNodeNetworkProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    node_public_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    node_public_ip_prefix_id: typing.Optional[builtins.str] = None,
    node_taints: typing.Optional[typing.Sequence[builtins.str]] = None,
    orchestrator_version: typing.Optional[builtins.str] = None,
    os_disk_size_gb: typing.Optional[jsii.Number] = None,
    os_disk_type: typing.Optional[builtins.str] = None,
    os_sku: typing.Optional[builtins.str] = None,
    os_type: typing.Optional[builtins.str] = None,
    pod_subnet_id: typing.Optional[builtins.str] = None,
    priority: typing.Optional[builtins.str] = None,
    proximity_placement_group_id: typing.Optional[builtins.str] = None,
    scale_down_mode: typing.Optional[builtins.str] = None,
    snapshot_id: typing.Optional[builtins.str] = None,
    spot_max_price: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    temporary_name_for_rotation: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[KubernetesClusterNodePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    ultra_ssd_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    upgrade_settings: typing.Optional[typing.Union[KubernetesClusterNodePoolUpgradeSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    vm_size: typing.Optional[builtins.str] = None,
    vnet_subnet_id: typing.Optional[builtins.str] = None,
    windows_profile: typing.Optional[typing.Union[KubernetesClusterNodePoolWindowsProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    workload_runtime: typing.Optional[builtins.str] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80db6d0bd0628ec2dd4c3ad2299c4100098950630fae16cd4894d00fd617f4ce(
    *,
    allowed_unsafe_sysctls: typing.Optional[typing.Sequence[builtins.str]] = None,
    container_log_max_line: typing.Optional[jsii.Number] = None,
    container_log_max_size_mb: typing.Optional[jsii.Number] = None,
    cpu_cfs_quota_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cpu_cfs_quota_period: typing.Optional[builtins.str] = None,
    cpu_manager_policy: typing.Optional[builtins.str] = None,
    image_gc_high_threshold: typing.Optional[jsii.Number] = None,
    image_gc_low_threshold: typing.Optional[jsii.Number] = None,
    pod_max_pid: typing.Optional[jsii.Number] = None,
    topology_manager_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4ae2165e4474a3e4ed73a47fc1d32d009eda2cb8ad5736c6b40ea3bda36a1bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__103633604dab466059805eeae75a555365cdb4a541fe7744a14de2a86d271284(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e41c07e05fe4ba18549f6966985d6a5550c4265029753da06a79650e623cfe(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__172eee9556ae066c9e3d7d7ae0343dd776119691d8a6c0eb9d22bc485cbae026(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f1e53b16305f39c5d375ca4b33c2a93166e6774fa2989b7d1df864dafa01bb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e722b5e2ebb5f7a82a7ecd6397ddf974ba1e3293695913eae206cc99f49f9f01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf84cf3c4089c3bcf8c39dd15df92fd42fc96e91cabc0d7af70ad989208659d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b196b47ecb03a59b683e2c102ab8abbfae57bbd7938ef9dbfec5699aca9d4b5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1977779b05a200b46c7e7766fbd99b9bc9ac58a529ac5721f02924f85b811942(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec4b86b8444af2b840df7ac5f92a3aa0f751f160713c2ae46765347af16c79e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e2462156de9fe00c7d9279f1ca274a7814ab12d4a0a87f109b944cd2e92cc5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4fd99100d43698d8b3fe0203693e5753dab9455d73ed04e1b7766f47f58f4ff(
    value: typing.Optional[KubernetesClusterNodePoolKubeletConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95107ed3ab8204d158ea8f2472e574d0a7182e57f1bf40c60ce99169e7fe0502(
    *,
    swap_file_size_mb: typing.Optional[jsii.Number] = None,
    sysctl_config: typing.Optional[typing.Union[KubernetesClusterNodePoolLinuxOsConfigSysctlConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    transparent_huge_page_defrag: typing.Optional[builtins.str] = None,
    transparent_huge_page_enabled: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62bb57f3342831ab5521b5dd02dca3b051796669d600da76aba2f05117cabe58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05bb32dd303936eaa66457cc2907ee8242faf1880f1c38168ac9aaa49d2820d6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59d8c6c93e2c7ca901deafc874c487756453839329cee9f77f1b8789e01b9727(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c31c79da72563df716d6a02b00943fa13b962a7976e8613a503b1f2f102f1b49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a205c3846455b306d5bcb43760d76145fd8b77fb2b7ba5a64ba8661801e16c9(
    value: typing.Optional[KubernetesClusterNodePoolLinuxOsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f54347769cb63b60e5a5a8a49a21b3147c2bbffb6e6b2a11b2719ceb16666e(
    *,
    fs_aio_max_nr: typing.Optional[jsii.Number] = None,
    fs_file_max: typing.Optional[jsii.Number] = None,
    fs_inotify_max_user_watches: typing.Optional[jsii.Number] = None,
    fs_nr_open: typing.Optional[jsii.Number] = None,
    kernel_threads_max: typing.Optional[jsii.Number] = None,
    net_core_netdev_max_backlog: typing.Optional[jsii.Number] = None,
    net_core_optmem_max: typing.Optional[jsii.Number] = None,
    net_core_rmem_default: typing.Optional[jsii.Number] = None,
    net_core_rmem_max: typing.Optional[jsii.Number] = None,
    net_core_somaxconn: typing.Optional[jsii.Number] = None,
    net_core_wmem_default: typing.Optional[jsii.Number] = None,
    net_core_wmem_max: typing.Optional[jsii.Number] = None,
    net_ipv4_ip_local_port_range_max: typing.Optional[jsii.Number] = None,
    net_ipv4_ip_local_port_range_min: typing.Optional[jsii.Number] = None,
    net_ipv4_neigh_default_gc_thresh1: typing.Optional[jsii.Number] = None,
    net_ipv4_neigh_default_gc_thresh2: typing.Optional[jsii.Number] = None,
    net_ipv4_neigh_default_gc_thresh3: typing.Optional[jsii.Number] = None,
    net_ipv4_tcp_fin_timeout: typing.Optional[jsii.Number] = None,
    net_ipv4_tcp_keepalive_intvl: typing.Optional[jsii.Number] = None,
    net_ipv4_tcp_keepalive_probes: typing.Optional[jsii.Number] = None,
    net_ipv4_tcp_keepalive_time: typing.Optional[jsii.Number] = None,
    net_ipv4_tcp_max_syn_backlog: typing.Optional[jsii.Number] = None,
    net_ipv4_tcp_max_tw_buckets: typing.Optional[jsii.Number] = None,
    net_ipv4_tcp_tw_reuse: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    net_netfilter_nf_conntrack_buckets: typing.Optional[jsii.Number] = None,
    net_netfilter_nf_conntrack_max: typing.Optional[jsii.Number] = None,
    vm_max_map_count: typing.Optional[jsii.Number] = None,
    vm_swappiness: typing.Optional[jsii.Number] = None,
    vm_vfs_cache_pressure: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acbe16c22fb32f6df7f14c7149ff1c6f717ee1750a4b2cfdbd73e1f4d4a537bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef0798213f6760b5b0c0673ffaf4adb3060d454df5af975d4dfd67e79d564c5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae39ab0dec3709871665bf830df38620ed805e9e11c3da8fc776b7a8f2ae753f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35b2e08a92e210c21d17437971dafe14189a3471869ca742d17d038c405e592a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f9537fab7b51975f9263b7f267f0be1d7c4760733a68abe865a8f37a5493fd1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b789fa7c4a16b34f923229f16fe83a38b23655023d323d9aa96ad2d42748534c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36cb59b745c732bde404a3eca420972c4c32dfab2e9da1d3f76b1579652d114b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c44edee6d6f3079c85855cd8ed4c7c2468392e8c75ab9e03a5ba4029d26ea7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08f88cc2c1347d74d3c879535028420394d2fb8a6dd4d7e3408bfbd27b9f5939(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b76e45a05cd005f3d3d633615ad6437f6651196b70ad5136c8a9042e586a6eda(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a9af2ed5d7a8bd6b10c66ed70e239227d85a9c605aa6ad3cf773555a21fb91b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7142ac7e2272a56552cba2510539b272d9c2d5bca24243b69b598c8d4c9bac9a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f011dc323323c76783bdaf55330023d15ca852b9e9b1eeef6e396e6f53c5d85(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c5a69f8fd5c423c2604e377eee8d43d04fdc36d0a8827806295c557e92814a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ea994a4115a6bed7a7c40c242710c3065ca0213565ed6a13b82cc540df5c257(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5607d573224d93ebd58ba06997485e90c1c8d2d16ee426c2e8363739e827f3c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c3e62b30862b0a98bd2738a82979445beb41a20e9848c37b16f7ae4471cef1f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6932437dcbe2934677c03ad081d8b9772bdea0a1f83ad62090be81a0e266bc8b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf82c490e54563e4218b52d7c14804bdb50860c50f9b6538114a4442262480d1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ad6b664e138996aad6a9f064e3e76a6bd52fdc87c9e36704c00e39cfa376b6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed454c7a7e4d34e194fe84e25cc4cbd616cb259a748c788122579fe8887f44b1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0df3a915bd549d3e3e3e30edb5f08f0e646fb90f855ab10a105ad40ac91e25b7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dcd09bd3ad1867295e94f723c5f32daa8c02d310ab12fecf670102bf6391358(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c928f1b4b45550ef8efdba6dbfab4449b104b4288828774d2a14d7e5457a093(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__985fb15e9ad6f8a5cae66e0978817dd62709286c63abcb06d5655a0f8d0599b1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00978639027c69d22728d8162b91617dd9d285a3662e6c8a5d45983afef7aa60(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b87c7c44c49e0a29c45d3c40464ff7b08390a1bca7d4f37d18f019cde120b067(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466368803b84539932ffce540162249d0317344b58bd278949e815f3ca895df8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d84bff48dc8f260f18a38b97d44a8e8af546fec99981ae0812644dac01ef7669(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea83a0eedf9235892cc22a019be8442306c402bb533942cf7772ae2dca4b1038(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b636cd30e04953337b93a5a48a692f2ac19ef8e443a64ce8741e6fa5663a3b31(
    value: typing.Optional[KubernetesClusterNodePoolLinuxOsConfigSysctlConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e8b7efc36677826b72e2d473b125633f7f07906f50f5f661b1db04bb1879746(
    *,
    allowed_host_ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPorts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    application_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    node_public_ip_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c9b34e2b2e73fb2fe0e169b91874604074a04a875fb61d2db99b8054b42b5a(
    *,
    port_end: typing.Optional[jsii.Number] = None,
    port_start: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1c91ff26ac0d56e062783ec61b6f523430952ab07995bdd767dbec276560cda(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d1f46d95ae3fe71fc6a62e16dd88080d01f5f1ca6f3da6c7769cc9ef03e57c6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a967c3adab72feeb341451c343d99872a8b51dc00348fd6c7b7fca0b6c5654b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aca6b77516e8b35ae585d88598141de0748a01e6e89f94ce1e7e517dc055a5a0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db4516bf3a750edacb2a3def70836f37a5bcc7470283f778003f94b54920d2b5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b25f00824f383429fa72a79893fe846ae08dc25dd2a24af4e94a36097a94293b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPorts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b58cd5b4983b23c32a87466ee404956ddabea74e6f41a52fbcb86f2dd43adf78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55a8ba8080def2f766f2776e68b63f910b5fa121cf1eb19a4ec67a8c5577968c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a30390613f4b55cc70acadaa9b77c63f9acebe64e0db29d82567a052de39128(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea583f96779bf97e03cb9969790662b10db8e61533750947ac58607ad5123e2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61b88db040a34e3f4855d15e80efc40e1b4a6ccfbcbdb5c12b64c386dcd48f2f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPorts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a0f72d068d36f3cf5c7d7be2684ecfff76336441d7f10ad9e403c6d2c299a3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ef0719eed183226aa5288a5584221ca39c570cb7d1ab1096daa15b860e3ba3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KubernetesClusterNodePoolNodeNetworkProfileAllowedHostPorts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b654fc050ee2d40d3434192ba4ed0ee228158c1ac811b745ef4d4a1f2b2317ba(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6741b11980fe9680cdf74cb0b75549345401bd788ed2cf1ffe1580bc76719d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5efae05489cdecd2a726f93777268892f5acf9b2f085ce42a22ffdff08cd0940(
    value: typing.Optional[KubernetesClusterNodePoolNodeNetworkProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71bd060ef987d357ac06939eb259d744fc024013e8766322815e9daedc44e177(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af117bad2117253f6538630702592ae6859fda1da7357663e8c3442591c9b2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b7e3eaf080ff6a1dcde1b14537eaeee891733df9846fb6291af4625f75faf5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4334e65542deb23fe4d2fe55a7afb578d4569dc695604d212834e9fe11d8d2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43f0a3a68581fede504a122da5534e1cfb6f9b3e17014db0c1546ad8d710d10a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad4e1dfd0f4e63d2a3bf2864bd756df56d462c0f44ac7d47a99a162e1a0d103(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21936f3773606dc1547bcceaa5ad4158159a5d8817b7b0ca60f9e072fe9d5965(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesClusterNodePoolTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__817b7bf9975f86719026dd8b63ccae540e40be10cd5846fab03abc2614401cac(
    *,
    max_surge: builtins.str,
    drain_timeout_in_minutes: typing.Optional[jsii.Number] = None,
    node_soak_duration_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9849f8ed41ed16d40bf628ad07ae65301cc74c1c27fc55c7888681e56c40d6e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55a4a83a584ffeb0fdeec2c920e90c3bb78735d6b20e91c582af0534cb50e092(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bbdae63cb665050f84381e32a3e12d43dad0dc81ac6f3b4c4ec56d79331db68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d071551df742d512c5c1d6a1cc3c98a3e03f0ab5a22e4bd0a2f67b6fd3522f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d9868f096466c0bd1206964e0698a8069bfaf854eeac56815e471086bf6b1c7(
    value: typing.Optional[KubernetesClusterNodePoolUpgradeSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a1ce4370a82cb5899dbd3f13abb23aed73e6f17f0c09c4cdb62c46b42819ea5(
    *,
    outbound_nat_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f060b99a0f57e1db54ad7638c1a96ddd780856ba20621107a0668cdcecf1a70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09e9eb1bbe128b2fd2cebbb29871fdfc18644b5b62174a2b97bc6ce81fc78338(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0ee4291b4170a30562575706466861f0a4a51f00adce38f4a305a8283737664(
    value: typing.Optional[KubernetesClusterNodePoolWindowsProfile],
) -> None:
    """Type checking stubs"""
    pass
