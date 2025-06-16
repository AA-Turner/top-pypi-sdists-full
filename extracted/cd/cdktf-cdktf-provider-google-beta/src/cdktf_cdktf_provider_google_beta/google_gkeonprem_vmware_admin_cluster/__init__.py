r'''
# `google_gkeonprem_vmware_admin_cluster`

Refer to the Terraform Registry for docs: [`google_gkeonprem_vmware_admin_cluster`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster).
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


class GoogleGkeonpremVmwareAdminCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster google_gkeonprem_vmware_admin_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        network_config: typing.Union["GoogleGkeonpremVmwareAdminClusterNetworkConfig", typing.Dict[builtins.str, typing.Any]],
        addon_node: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterAddonNode", typing.Dict[builtins.str, typing.Any]]] = None,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        anti_affinity_groups: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterAntiAffinityGroups", typing.Dict[builtins.str, typing.Any]]] = None,
        authorization: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_repair_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterAutoRepairConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        bootstrap_cluster_membership: typing.Optional[builtins.str] = None,
        control_plane_node: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterControlPlaneNode", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_type: typing.Optional[builtins.str] = None,
        load_balancer: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterLoadBalancer", typing.Dict[builtins.str, typing.Any]]] = None,
        on_prem_version: typing.Optional[builtins.str] = None,
        platform_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterPlatformConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        private_registry_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterPrivateRegistryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vcenter: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterVcenter", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster google_gkeonprem_vmware_admin_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#location GoogleGkeonpremVmwareAdminCluster#location}
        :param name: The VMware admin cluster resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#name GoogleGkeonpremVmwareAdminCluster#name}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#network_config GoogleGkeonpremVmwareAdminCluster#network_config}
        :param addon_node: addon_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#addon_node GoogleGkeonpremVmwareAdminCluster#addon_node}
        :param annotations: Annotations on the VMware Admin Cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#annotations GoogleGkeonpremVmwareAdminCluster#annotations}
        :param anti_affinity_groups: anti_affinity_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#anti_affinity_groups GoogleGkeonpremVmwareAdminCluster#anti_affinity_groups}
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#authorization GoogleGkeonpremVmwareAdminCluster#authorization}
        :param auto_repair_config: auto_repair_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#auto_repair_config GoogleGkeonpremVmwareAdminCluster#auto_repair_config}
        :param bootstrap_cluster_membership: The bootstrap cluster this VMware admin cluster belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#bootstrap_cluster_membership GoogleGkeonpremVmwareAdminCluster#bootstrap_cluster_membership}
        :param control_plane_node: control_plane_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#control_plane_node GoogleGkeonpremVmwareAdminCluster#control_plane_node}
        :param description: A human readable description of this VMware admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#description GoogleGkeonpremVmwareAdminCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#id GoogleGkeonpremVmwareAdminCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_type: The OS image type for the VMware admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#image_type GoogleGkeonpremVmwareAdminCluster#image_type}
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#load_balancer GoogleGkeonpremVmwareAdminCluster#load_balancer}
        :param on_prem_version: The Anthos clusters on the VMware version for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#on_prem_version GoogleGkeonpremVmwareAdminCluster#on_prem_version}
        :param platform_config: platform_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#platform_config GoogleGkeonpremVmwareAdminCluster#platform_config}
        :param private_registry_config: private_registry_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#private_registry_config GoogleGkeonpremVmwareAdminCluster#private_registry_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#project GoogleGkeonpremVmwareAdminCluster#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#timeouts GoogleGkeonpremVmwareAdminCluster#timeouts}
        :param vcenter: vcenter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#vcenter GoogleGkeonpremVmwareAdminCluster#vcenter}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56da4fc7adbb210da0bfccebe4181d1526c1d9cc61269dc916d33b676a4dc09d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleGkeonpremVmwareAdminClusterConfig(
            location=location,
            name=name,
            network_config=network_config,
            addon_node=addon_node,
            annotations=annotations,
            anti_affinity_groups=anti_affinity_groups,
            authorization=authorization,
            auto_repair_config=auto_repair_config,
            bootstrap_cluster_membership=bootstrap_cluster_membership,
            control_plane_node=control_plane_node,
            description=description,
            id=id,
            image_type=image_type,
            load_balancer=load_balancer,
            on_prem_version=on_prem_version,
            platform_config=platform_config,
            private_registry_config=private_registry_config,
            project=project,
            timeouts=timeouts,
            vcenter=vcenter,
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
        '''Generates CDKTF code for importing a GoogleGkeonpremVmwareAdminCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleGkeonpremVmwareAdminCluster to import.
        :param import_from_id: The id of the existing GoogleGkeonpremVmwareAdminCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleGkeonpremVmwareAdminCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c67ed89b4c0052c981f9534e3e8b7df0a62af8d562c9ec996161e2a5ae186a0c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAddonNode")
    def put_addon_node(
        self,
        *,
        auto_resize_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auto_resize_config: auto_resize_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#auto_resize_config GoogleGkeonpremVmwareAdminCluster#auto_resize_config}
        '''
        value = GoogleGkeonpremVmwareAdminClusterAddonNode(
            auto_resize_config=auto_resize_config
        )

        return typing.cast(None, jsii.invoke(self, "putAddonNode", [value]))

    @jsii.member(jsii_name="putAntiAffinityGroups")
    def put_anti_affinity_groups(
        self,
        *,
        aag_config_disabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param aag_config_disabled: Spread nodes across at least three physical hosts (requires at least three hosts). Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#aag_config_disabled GoogleGkeonpremVmwareAdminCluster#aag_config_disabled}
        '''
        value = GoogleGkeonpremVmwareAdminClusterAntiAffinityGroups(
            aag_config_disabled=aag_config_disabled
        )

        return typing.cast(None, jsii.invoke(self, "putAntiAffinityGroups", [value]))

    @jsii.member(jsii_name="putAuthorization")
    def put_authorization(
        self,
        *,
        viewer_users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsers", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param viewer_users: viewer_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#viewer_users GoogleGkeonpremVmwareAdminCluster#viewer_users}
        '''
        value = GoogleGkeonpremVmwareAdminClusterAuthorization(
            viewer_users=viewer_users
        )

        return typing.cast(None, jsii.invoke(self, "putAuthorization", [value]))

    @jsii.member(jsii_name="putAutoRepairConfig")
    def put_auto_repair_config(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether auto repair is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#enabled GoogleGkeonpremVmwareAdminCluster#enabled}
        '''
        value = GoogleGkeonpremVmwareAdminClusterAutoRepairConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putAutoRepairConfig", [value]))

    @jsii.member(jsii_name="putControlPlaneNode")
    def put_control_plane_node(
        self,
        *,
        cpus: typing.Optional[jsii.Number] = None,
        memory: typing.Optional[jsii.Number] = None,
        replicas: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpus: The number of vCPUs for the control-plane node of the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#cpus GoogleGkeonpremVmwareAdminCluster#cpus}
        :param memory: The number of mebibytes of memory for the control-plane node of the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#memory GoogleGkeonpremVmwareAdminCluster#memory}
        :param replicas: The number of control plane nodes for this VMware admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#replicas GoogleGkeonpremVmwareAdminCluster#replicas}
        '''
        value = GoogleGkeonpremVmwareAdminClusterControlPlaneNode(
            cpus=cpus, memory=memory, replicas=replicas
        )

        return typing.cast(None, jsii.invoke(self, "putControlPlaneNode", [value]))

    @jsii.member(jsii_name="putLoadBalancer")
    def put_load_balancer(
        self,
        *,
        vip_config: typing.Union["GoogleGkeonpremVmwareAdminClusterLoadBalancerVipConfig", typing.Dict[builtins.str, typing.Any]],
        f5_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterLoadBalancerF5Config", typing.Dict[builtins.str, typing.Any]]] = None,
        manual_lb_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterLoadBalancerManualLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        metal_lb_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param vip_config: vip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#vip_config GoogleGkeonpremVmwareAdminCluster#vip_config}
        :param f5_config: f5_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#f5_config GoogleGkeonpremVmwareAdminCluster#f5_config}
        :param manual_lb_config: manual_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#manual_lb_config GoogleGkeonpremVmwareAdminCluster#manual_lb_config}
        :param metal_lb_config: metal_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#metal_lb_config GoogleGkeonpremVmwareAdminCluster#metal_lb_config}
        '''
        value = GoogleGkeonpremVmwareAdminClusterLoadBalancer(
            vip_config=vip_config,
            f5_config=f5_config,
            manual_lb_config=manual_lb_config,
            metal_lb_config=metal_lb_config,
        )

        return typing.cast(None, jsii.invoke(self, "putLoadBalancer", [value]))

    @jsii.member(jsii_name="putNetworkConfig")
    def put_network_config(
        self,
        *,
        pod_address_cidr_blocks: typing.Sequence[builtins.str],
        service_address_cidr_blocks: typing.Sequence[builtins.str],
        dhcp_ip_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ha_control_plane_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        host_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterNetworkConfigHostConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        static_ip_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        vcenter_network: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pod_address_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#pod_address_cidr_blocks GoogleGkeonpremVmwareAdminCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported.. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#service_address_cidr_blocks GoogleGkeonpremVmwareAdminCluster#service_address_cidr_blocks}
        :param dhcp_ip_config: dhcp_ip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#dhcp_ip_config GoogleGkeonpremVmwareAdminCluster#dhcp_ip_config}
        :param ha_control_plane_config: ha_control_plane_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ha_control_plane_config GoogleGkeonpremVmwareAdminCluster#ha_control_plane_config}
        :param host_config: host_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#host_config GoogleGkeonpremVmwareAdminCluster#host_config}
        :param static_ip_config: static_ip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#static_ip_config GoogleGkeonpremVmwareAdminCluster#static_ip_config}
        :param vcenter_network: vcenter_network specifies vCenter network name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#vcenter_network GoogleGkeonpremVmwareAdminCluster#vcenter_network}
        '''
        value = GoogleGkeonpremVmwareAdminClusterNetworkConfig(
            pod_address_cidr_blocks=pod_address_cidr_blocks,
            service_address_cidr_blocks=service_address_cidr_blocks,
            dhcp_ip_config=dhcp_ip_config,
            ha_control_plane_config=ha_control_plane_config,
            host_config=host_config,
            static_ip_config=static_ip_config,
            vcenter_network=vcenter_network,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfig", [value]))

    @jsii.member(jsii_name="putPlatformConfig")
    def put_platform_config(
        self,
        *,
        required_platform_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param required_platform_version: The required platform version e.g. 1.13.1. If the current platform version is lower than the target version, the platform version will be updated to the target version. If the target version is not installed in the platform (bundle versions), download the target version bundle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#required_platform_version GoogleGkeonpremVmwareAdminCluster#required_platform_version}
        '''
        value = GoogleGkeonpremVmwareAdminClusterPlatformConfig(
            required_platform_version=required_platform_version
        )

        return typing.cast(None, jsii.invoke(self, "putPlatformConfig", [value]))

    @jsii.member(jsii_name="putPrivateRegistryConfig")
    def put_private_registry_config(
        self,
        *,
        address: typing.Optional[builtins.str] = None,
        ca_cert: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: The registry address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#address GoogleGkeonpremVmwareAdminCluster#address}
        :param ca_cert: The CA certificate public key for private registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ca_cert GoogleGkeonpremVmwareAdminCluster#ca_cert}
        '''
        value = GoogleGkeonpremVmwareAdminClusterPrivateRegistryConfig(
            address=address, ca_cert=ca_cert
        )

        return typing.cast(None, jsii.invoke(self, "putPrivateRegistryConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#create GoogleGkeonpremVmwareAdminCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#delete GoogleGkeonpremVmwareAdminCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#update GoogleGkeonpremVmwareAdminCluster#update}.
        '''
        value = GoogleGkeonpremVmwareAdminClusterTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVcenter")
    def put_vcenter(
        self,
        *,
        address: typing.Optional[builtins.str] = None,
        ca_cert_data: typing.Optional[builtins.str] = None,
        cluster: typing.Optional[builtins.str] = None,
        datacenter: typing.Optional[builtins.str] = None,
        data_disk: typing.Optional[builtins.str] = None,
        datastore: typing.Optional[builtins.str] = None,
        folder: typing.Optional[builtins.str] = None,
        resource_pool: typing.Optional[builtins.str] = None,
        storage_policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: The vCenter IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#address GoogleGkeonpremVmwareAdminCluster#address}
        :param ca_cert_data: Contains the vCenter CA certificate public key for SSL verification. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ca_cert_data GoogleGkeonpremVmwareAdminCluster#ca_cert_data}
        :param cluster: The name of the vCenter cluster for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#cluster GoogleGkeonpremVmwareAdminCluster#cluster}
        :param datacenter: The name of the vCenter datacenter for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#datacenter GoogleGkeonpremVmwareAdminCluster#datacenter}
        :param data_disk: The name of the virtual machine disk (VMDK) for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#data_disk GoogleGkeonpremVmwareAdminCluster#data_disk}
        :param datastore: The name of the vCenter datastore for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#datastore GoogleGkeonpremVmwareAdminCluster#datastore}
        :param folder: The name of the vCenter folder for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#folder GoogleGkeonpremVmwareAdminCluster#folder}
        :param resource_pool: The name of the vCenter resource pool for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#resource_pool GoogleGkeonpremVmwareAdminCluster#resource_pool}
        :param storage_policy_name: The name of the vCenter storage policy for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#storage_policy_name GoogleGkeonpremVmwareAdminCluster#storage_policy_name}
        '''
        value = GoogleGkeonpremVmwareAdminClusterVcenter(
            address=address,
            ca_cert_data=ca_cert_data,
            cluster=cluster,
            datacenter=datacenter,
            data_disk=data_disk,
            datastore=datastore,
            folder=folder,
            resource_pool=resource_pool,
            storage_policy_name=storage_policy_name,
        )

        return typing.cast(None, jsii.invoke(self, "putVcenter", [value]))

    @jsii.member(jsii_name="resetAddonNode")
    def reset_addon_node(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddonNode", []))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetAntiAffinityGroups")
    def reset_anti_affinity_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAntiAffinityGroups", []))

    @jsii.member(jsii_name="resetAuthorization")
    def reset_authorization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorization", []))

    @jsii.member(jsii_name="resetAutoRepairConfig")
    def reset_auto_repair_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoRepairConfig", []))

    @jsii.member(jsii_name="resetBootstrapClusterMembership")
    def reset_bootstrap_cluster_membership(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootstrapClusterMembership", []))

    @jsii.member(jsii_name="resetControlPlaneNode")
    def reset_control_plane_node(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControlPlaneNode", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImageType")
    def reset_image_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageType", []))

    @jsii.member(jsii_name="resetLoadBalancer")
    def reset_load_balancer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancer", []))

    @jsii.member(jsii_name="resetOnPremVersion")
    def reset_on_prem_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnPremVersion", []))

    @jsii.member(jsii_name="resetPlatformConfig")
    def reset_platform_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatformConfig", []))

    @jsii.member(jsii_name="resetPrivateRegistryConfig")
    def reset_private_registry_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateRegistryConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVcenter")
    def reset_vcenter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVcenter", []))

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
    @jsii.member(jsii_name="addonNode")
    def addon_node(self) -> "GoogleGkeonpremVmwareAdminClusterAddonNodeOutputReference":
        return typing.cast("GoogleGkeonpremVmwareAdminClusterAddonNodeOutputReference", jsii.get(self, "addonNode"))

    @builtins.property
    @jsii.member(jsii_name="antiAffinityGroups")
    def anti_affinity_groups(
        self,
    ) -> "GoogleGkeonpremVmwareAdminClusterAntiAffinityGroupsOutputReference":
        return typing.cast("GoogleGkeonpremVmwareAdminClusterAntiAffinityGroupsOutputReference", jsii.get(self, "antiAffinityGroups"))

    @builtins.property
    @jsii.member(jsii_name="authorization")
    def authorization(
        self,
    ) -> "GoogleGkeonpremVmwareAdminClusterAuthorizationOutputReference":
        return typing.cast("GoogleGkeonpremVmwareAdminClusterAuthorizationOutputReference", jsii.get(self, "authorization"))

    @builtins.property
    @jsii.member(jsii_name="autoRepairConfig")
    def auto_repair_config(
        self,
    ) -> "GoogleGkeonpremVmwareAdminClusterAutoRepairConfigOutputReference":
        return typing.cast("GoogleGkeonpremVmwareAdminClusterAutoRepairConfigOutputReference", jsii.get(self, "autoRepairConfig"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneNode")
    def control_plane_node(
        self,
    ) -> "GoogleGkeonpremVmwareAdminClusterControlPlaneNodeOutputReference":
        return typing.cast("GoogleGkeonpremVmwareAdminClusterControlPlaneNodeOutputReference", jsii.get(self, "controlPlaneNode"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="enableAdvancedCluster")
    def enable_advanced_cluster(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enableAdvancedCluster"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="fleet")
    def fleet(self) -> "GoogleGkeonpremVmwareAdminClusterFleetList":
        return typing.cast("GoogleGkeonpremVmwareAdminClusterFleetList", jsii.get(self, "fleet"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(
        self,
    ) -> "GoogleGkeonpremVmwareAdminClusterLoadBalancerOutputReference":
        return typing.cast("GoogleGkeonpremVmwareAdminClusterLoadBalancerOutputReference", jsii.get(self, "loadBalancer"))

    @builtins.property
    @jsii.member(jsii_name="localName")
    def local_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localName"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(
        self,
    ) -> "GoogleGkeonpremVmwareAdminClusterNetworkConfigOutputReference":
        return typing.cast("GoogleGkeonpremVmwareAdminClusterNetworkConfigOutputReference", jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="platformConfig")
    def platform_config(
        self,
    ) -> "GoogleGkeonpremVmwareAdminClusterPlatformConfigOutputReference":
        return typing.cast("GoogleGkeonpremVmwareAdminClusterPlatformConfigOutputReference", jsii.get(self, "platformConfig"))

    @builtins.property
    @jsii.member(jsii_name="privateRegistryConfig")
    def private_registry_config(
        self,
    ) -> "GoogleGkeonpremVmwareAdminClusterPrivateRegistryConfigOutputReference":
        return typing.cast("GoogleGkeonpremVmwareAdminClusterPrivateRegistryConfigOutputReference", jsii.get(self, "privateRegistryConfig"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "GoogleGkeonpremVmwareAdminClusterStatusList":
        return typing.cast("GoogleGkeonpremVmwareAdminClusterStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleGkeonpremVmwareAdminClusterTimeoutsOutputReference":
        return typing.cast("GoogleGkeonpremVmwareAdminClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="vcenter")
    def vcenter(self) -> "GoogleGkeonpremVmwareAdminClusterVcenterOutputReference":
        return typing.cast("GoogleGkeonpremVmwareAdminClusterVcenterOutputReference", jsii.get(self, "vcenter"))

    @builtins.property
    @jsii.member(jsii_name="addonNodeInput")
    def addon_node_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterAddonNode"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterAddonNode"], jsii.get(self, "addonNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="antiAffinityGroupsInput")
    def anti_affinity_groups_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterAntiAffinityGroups"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterAntiAffinityGroups"], jsii.get(self, "antiAffinityGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationInput")
    def authorization_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterAuthorization"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterAuthorization"], jsii.get(self, "authorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="autoRepairConfigInput")
    def auto_repair_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterAutoRepairConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterAutoRepairConfig"], jsii.get(self, "autoRepairConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bootstrapClusterMembershipInput")
    def bootstrap_cluster_membership_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootstrapClusterMembershipInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneNodeInput")
    def control_plane_node_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterControlPlaneNode"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterControlPlaneNode"], jsii.get(self, "controlPlaneNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageTypeInput")
    def image_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerInput")
    def load_balancer_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterLoadBalancer"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterLoadBalancer"], jsii.get(self, "loadBalancerInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigInput")
    def network_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterNetworkConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterNetworkConfig"], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="onPremVersionInput")
    def on_prem_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onPremVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="platformConfigInput")
    def platform_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterPlatformConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterPlatformConfig"], jsii.get(self, "platformConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="privateRegistryConfigInput")
    def private_registry_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterPrivateRegistryConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterPrivateRegistryConfig"], jsii.get(self, "privateRegistryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleGkeonpremVmwareAdminClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleGkeonpremVmwareAdminClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vcenterInput")
    def vcenter_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterVcenter"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterVcenter"], jsii.get(self, "vcenterInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17990b576eb7072b2cf85dd542c37d8cb9439d62c760f114e26e2c405090fbbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bootstrapClusterMembership")
    def bootstrap_cluster_membership(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootstrapClusterMembership"))

    @bootstrap_cluster_membership.setter
    def bootstrap_cluster_membership(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6a51989798254dd83b53236de92fc611a2b3162f3826b44a7762cc99a6140a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootstrapClusterMembership", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df3726f56fab387b9ee9219c2adf46b93699669dc80c3bc143535890a022aed2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363f31f0cfdf1b5941ded9dbfd634fac089d93950cf9e72fe82062f3f6aba294)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageType")
    def image_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageType"))

    @image_type.setter
    def image_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e6ba905fda0b6979b96bfa6657adf206835443e4be7b24fd0da7736476f9417)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__576b4f176a10df65f97b7e60717f225cf3a6911b5d342b95fa7a7801daec4261)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa27090977481a75165086daf6446a1addda66b97f50cf9549b6fd1fd5a2d3f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onPremVersion")
    def on_prem_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onPremVersion"))

    @on_prem_version.setter
    def on_prem_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd59fa4136dde4280ba47cf8ffd3f51ec50a6d59bb24e2fb90dff00cf7df70ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onPremVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a2a9c470cf561126a8fb8e7abb4af44a143f55a6a0c8b3548216ad8770e8ab0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterAddonNode",
    jsii_struct_bases=[],
    name_mapping={"auto_resize_config": "autoResizeConfig"},
)
class GoogleGkeonpremVmwareAdminClusterAddonNode:
    def __init__(
        self,
        *,
        auto_resize_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auto_resize_config: auto_resize_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#auto_resize_config GoogleGkeonpremVmwareAdminCluster#auto_resize_config}
        '''
        if isinstance(auto_resize_config, dict):
            auto_resize_config = GoogleGkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig(**auto_resize_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04a8a4769689fe0913314fd6804392f6a38ed8a48257da95e40a71270042d22b)
            check_type(argname="argument auto_resize_config", value=auto_resize_config, expected_type=type_hints["auto_resize_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_resize_config is not None:
            self._values["auto_resize_config"] = auto_resize_config

    @builtins.property
    def auto_resize_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig"]:
        '''auto_resize_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#auto_resize_config GoogleGkeonpremVmwareAdminCluster#auto_resize_config}
        '''
        result = self._values.get("auto_resize_config")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterAddonNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleGkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether to enable controle plane node auto resizing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#enabled GoogleGkeonpremVmwareAdminCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9147e4692f85c5677a9cbf2f033b3ee4e8caf052f277e139b627a8b69e45fd1a)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether to enable controle plane node auto resizing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#enabled GoogleGkeonpremVmwareAdminCluster#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareAdminClusterAddonNodeAutoResizeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterAddonNodeAutoResizeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0613c69af2fe68b4ce73de9842bf4147e45960784ff1a9ff8ba623a14c86acb7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d5067ad7743a1ee5870382a6df7a3f31788cd1bf7dd246f65fb3fd69e0dd615)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cabbb96aa949e1262a4ae73142faa31c6b34dcf99ef8d6aa4f365ea6c25441d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareAdminClusterAddonNodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterAddonNodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02a5a9ce311d6692c60ea442698e0a83169878979366bd9987e05ded10f9d983)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoResizeConfig")
    def put_auto_resize_config(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether to enable controle plane node auto resizing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#enabled GoogleGkeonpremVmwareAdminCluster#enabled}
        '''
        value = GoogleGkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putAutoResizeConfig", [value]))

    @jsii.member(jsii_name="resetAutoResizeConfig")
    def reset_auto_resize_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoResizeConfig", []))

    @builtins.property
    @jsii.member(jsii_name="autoResizeConfig")
    def auto_resize_config(
        self,
    ) -> GoogleGkeonpremVmwareAdminClusterAddonNodeAutoResizeConfigOutputReference:
        return typing.cast(GoogleGkeonpremVmwareAdminClusterAddonNodeAutoResizeConfigOutputReference, jsii.get(self, "autoResizeConfig"))

    @builtins.property
    @jsii.member(jsii_name="autoResizeConfigInput")
    def auto_resize_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig], jsii.get(self, "autoResizeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterAddonNode]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterAddonNode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterAddonNode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f04225db66b108b4840b1a48825927b06e7b95a27eedbcf6b7a85994caad7e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterAntiAffinityGroups",
    jsii_struct_bases=[],
    name_mapping={"aag_config_disabled": "aagConfigDisabled"},
)
class GoogleGkeonpremVmwareAdminClusterAntiAffinityGroups:
    def __init__(
        self,
        *,
        aag_config_disabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param aag_config_disabled: Spread nodes across at least three physical hosts (requires at least three hosts). Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#aag_config_disabled GoogleGkeonpremVmwareAdminCluster#aag_config_disabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78e1a2d69c9d9b242c72f9853bd738c45063a24dd7ab1a05565f583bf706e0d3)
            check_type(argname="argument aag_config_disabled", value=aag_config_disabled, expected_type=type_hints["aag_config_disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aag_config_disabled": aag_config_disabled,
        }

    @builtins.property
    def aag_config_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Spread nodes across at least three physical hosts (requires at least three hosts). Enabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#aag_config_disabled GoogleGkeonpremVmwareAdminCluster#aag_config_disabled}
        '''
        result = self._values.get("aag_config_disabled")
        assert result is not None, "Required property 'aag_config_disabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterAntiAffinityGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareAdminClusterAntiAffinityGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterAntiAffinityGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54db0578a651ac2b9e12d9959ffc2b25cf1b0ba05badcce32f3b98d299702c53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="aagConfigDisabledInput")
    def aag_config_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "aagConfigDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="aagConfigDisabled")
    def aag_config_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "aagConfigDisabled"))

    @aag_config_disabled.setter
    def aag_config_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76927fde0308ea5ffbac1538200dd39efe840c43352db66b60a2d2c720a291ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aagConfigDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterAntiAffinityGroups]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterAntiAffinityGroups], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterAntiAffinityGroups],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b78ecd7e7dc45f20164a5adb37dac13dba9db954929e35d65686e2cc91161de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterAuthorization",
    jsii_struct_bases=[],
    name_mapping={"viewer_users": "viewerUsers"},
)
class GoogleGkeonpremVmwareAdminClusterAuthorization:
    def __init__(
        self,
        *,
        viewer_users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsers", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param viewer_users: viewer_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#viewer_users GoogleGkeonpremVmwareAdminCluster#viewer_users}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab9260766fcb0626dbdd4281e97327f70f7ac372361471b5894390e09c14190a)
            check_type(argname="argument viewer_users", value=viewer_users, expected_type=type_hints["viewer_users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if viewer_users is not None:
            self._values["viewer_users"] = viewer_users

    @builtins.property
    def viewer_users(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsers"]]]:
        '''viewer_users block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#viewer_users GoogleGkeonpremVmwareAdminCluster#viewer_users}
        '''
        result = self._values.get("viewer_users")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsers"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareAdminClusterAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d91343c5a239b481e36d18415ed435014cafd57252554d3ad104bfdb35a2711)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putViewerUsers")
    def put_viewer_users(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e3d31aab97031ecb1001ca905e6db1b648ea19f18ba0198e6e4cc0cffaf08b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putViewerUsers", [value]))

    @jsii.member(jsii_name="resetViewerUsers")
    def reset_viewer_users(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetViewerUsers", []))

    @builtins.property
    @jsii.member(jsii_name="viewerUsers")
    def viewer_users(
        self,
    ) -> "GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsersList":
        return typing.cast("GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsersList", jsii.get(self, "viewerUsers"))

    @builtins.property
    @jsii.member(jsii_name="viewerUsersInput")
    def viewer_users_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsers"]]], jsii.get(self, "viewerUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterAuthorization]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d371a9ae6a0907ed6b889f6c2737e3fd5e2fcc17088f974b5f6fc954f12e3dc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsers",
    jsii_struct_bases=[],
    name_mapping={"username": "username"},
)
class GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsers:
    def __init__(self, *, username: builtins.str) -> None:
        '''
        :param username: The name of the user, e.g. 'my-gcp-id@gmail.com'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#username GoogleGkeonpremVmwareAdminCluster#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d35e4087ab809aa9a5dcb72e0fc67aad3b5f65e7b3e8dd3c1dbe3453feb3fcc0)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
        }

    @builtins.property
    def username(self) -> builtins.str:
        '''The name of the user, e.g. 'my-gcp-id@gmail.com'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#username GoogleGkeonpremVmwareAdminCluster#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de8bd93591be7b81f0498e2559748429f60ce96ca371cdcd741ae8ab7aea4933)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39977bafd427732e85cfb1ebc088a3c13b2cac6b84ebcb9eaed0751da617a9b2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bfab0ebb3b07b7c871d2b3d3089f96b98df0015f2d95b2071d9465e0a874982)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19fc197404dfc9c8112ba0c1ca1000316238279f2c9f9364a2292589bf408726)
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
            type_hints = typing.get_type_hints(_typecheckingstub__840403f3237c1e1e43ca3f0ef35efef343c90bb49c77dab71a6fa4ed3d1b2fbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca7872e942899c35923295e8f77889c55c6b2b3b76eae885d238c206e03c5e09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe3abef4db384e8fe832e2b0631a208c24816b511ecd346dabf0648377b61ea7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea729fe300793012c45e53e6ea3dfc036868ff47da1f3adca3e24fc48b5120d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adb4d595fc0a4610e37f032a908952de1964b7b7308a4cb86348f297bff65b78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterAutoRepairConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleGkeonpremVmwareAdminClusterAutoRepairConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether auto repair is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#enabled GoogleGkeonpremVmwareAdminCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d02b4f8ef13970359c7daae7f81490cd4447b129aa5fc5489ad7580aefdf7f30)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether auto repair is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#enabled GoogleGkeonpremVmwareAdminCluster#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterAutoRepairConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareAdminClusterAutoRepairConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterAutoRepairConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__340e5bc2eff24653f89ea9f8fd23a049d44c9a044630463dba586eb7ef31d964)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28c3db74048fb05c3a0bf66e8c2d9d7c449ea479a1e5690048eabed73c79fdae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterAutoRepairConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterAutoRepairConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterAutoRepairConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__696fded15667c5c95b9775e412708c91a541af6aed97544c9a97cd7eed33eabd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "network_config": "networkConfig",
        "addon_node": "addonNode",
        "annotations": "annotations",
        "anti_affinity_groups": "antiAffinityGroups",
        "authorization": "authorization",
        "auto_repair_config": "autoRepairConfig",
        "bootstrap_cluster_membership": "bootstrapClusterMembership",
        "control_plane_node": "controlPlaneNode",
        "description": "description",
        "id": "id",
        "image_type": "imageType",
        "load_balancer": "loadBalancer",
        "on_prem_version": "onPremVersion",
        "platform_config": "platformConfig",
        "private_registry_config": "privateRegistryConfig",
        "project": "project",
        "timeouts": "timeouts",
        "vcenter": "vcenter",
    },
)
class GoogleGkeonpremVmwareAdminClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        name: builtins.str,
        network_config: typing.Union["GoogleGkeonpremVmwareAdminClusterNetworkConfig", typing.Dict[builtins.str, typing.Any]],
        addon_node: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterAddonNode, typing.Dict[builtins.str, typing.Any]]] = None,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        anti_affinity_groups: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterAntiAffinityGroups, typing.Dict[builtins.str, typing.Any]]] = None,
        authorization: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_repair_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterAutoRepairConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        bootstrap_cluster_membership: typing.Optional[builtins.str] = None,
        control_plane_node: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterControlPlaneNode", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_type: typing.Optional[builtins.str] = None,
        load_balancer: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterLoadBalancer", typing.Dict[builtins.str, typing.Any]]] = None,
        on_prem_version: typing.Optional[builtins.str] = None,
        platform_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterPlatformConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        private_registry_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterPrivateRegistryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vcenter: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterVcenter", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#location GoogleGkeonpremVmwareAdminCluster#location}
        :param name: The VMware admin cluster resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#name GoogleGkeonpremVmwareAdminCluster#name}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#network_config GoogleGkeonpremVmwareAdminCluster#network_config}
        :param addon_node: addon_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#addon_node GoogleGkeonpremVmwareAdminCluster#addon_node}
        :param annotations: Annotations on the VMware Admin Cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#annotations GoogleGkeonpremVmwareAdminCluster#annotations}
        :param anti_affinity_groups: anti_affinity_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#anti_affinity_groups GoogleGkeonpremVmwareAdminCluster#anti_affinity_groups}
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#authorization GoogleGkeonpremVmwareAdminCluster#authorization}
        :param auto_repair_config: auto_repair_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#auto_repair_config GoogleGkeonpremVmwareAdminCluster#auto_repair_config}
        :param bootstrap_cluster_membership: The bootstrap cluster this VMware admin cluster belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#bootstrap_cluster_membership GoogleGkeonpremVmwareAdminCluster#bootstrap_cluster_membership}
        :param control_plane_node: control_plane_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#control_plane_node GoogleGkeonpremVmwareAdminCluster#control_plane_node}
        :param description: A human readable description of this VMware admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#description GoogleGkeonpremVmwareAdminCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#id GoogleGkeonpremVmwareAdminCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_type: The OS image type for the VMware admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#image_type GoogleGkeonpremVmwareAdminCluster#image_type}
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#load_balancer GoogleGkeonpremVmwareAdminCluster#load_balancer}
        :param on_prem_version: The Anthos clusters on the VMware version for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#on_prem_version GoogleGkeonpremVmwareAdminCluster#on_prem_version}
        :param platform_config: platform_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#platform_config GoogleGkeonpremVmwareAdminCluster#platform_config}
        :param private_registry_config: private_registry_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#private_registry_config GoogleGkeonpremVmwareAdminCluster#private_registry_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#project GoogleGkeonpremVmwareAdminCluster#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#timeouts GoogleGkeonpremVmwareAdminCluster#timeouts}
        :param vcenter: vcenter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#vcenter GoogleGkeonpremVmwareAdminCluster#vcenter}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(network_config, dict):
            network_config = GoogleGkeonpremVmwareAdminClusterNetworkConfig(**network_config)
        if isinstance(addon_node, dict):
            addon_node = GoogleGkeonpremVmwareAdminClusterAddonNode(**addon_node)
        if isinstance(anti_affinity_groups, dict):
            anti_affinity_groups = GoogleGkeonpremVmwareAdminClusterAntiAffinityGroups(**anti_affinity_groups)
        if isinstance(authorization, dict):
            authorization = GoogleGkeonpremVmwareAdminClusterAuthorization(**authorization)
        if isinstance(auto_repair_config, dict):
            auto_repair_config = GoogleGkeonpremVmwareAdminClusterAutoRepairConfig(**auto_repair_config)
        if isinstance(control_plane_node, dict):
            control_plane_node = GoogleGkeonpremVmwareAdminClusterControlPlaneNode(**control_plane_node)
        if isinstance(load_balancer, dict):
            load_balancer = GoogleGkeonpremVmwareAdminClusterLoadBalancer(**load_balancer)
        if isinstance(platform_config, dict):
            platform_config = GoogleGkeonpremVmwareAdminClusterPlatformConfig(**platform_config)
        if isinstance(private_registry_config, dict):
            private_registry_config = GoogleGkeonpremVmwareAdminClusterPrivateRegistryConfig(**private_registry_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleGkeonpremVmwareAdminClusterTimeouts(**timeouts)
        if isinstance(vcenter, dict):
            vcenter = GoogleGkeonpremVmwareAdminClusterVcenter(**vcenter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf6b4297ef3d2690ab700af6228b56e821b643e4fc1bbceb4092d58d1b0d16d3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_config", value=network_config, expected_type=type_hints["network_config"])
            check_type(argname="argument addon_node", value=addon_node, expected_type=type_hints["addon_node"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument anti_affinity_groups", value=anti_affinity_groups, expected_type=type_hints["anti_affinity_groups"])
            check_type(argname="argument authorization", value=authorization, expected_type=type_hints["authorization"])
            check_type(argname="argument auto_repair_config", value=auto_repair_config, expected_type=type_hints["auto_repair_config"])
            check_type(argname="argument bootstrap_cluster_membership", value=bootstrap_cluster_membership, expected_type=type_hints["bootstrap_cluster_membership"])
            check_type(argname="argument control_plane_node", value=control_plane_node, expected_type=type_hints["control_plane_node"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_type", value=image_type, expected_type=type_hints["image_type"])
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
            check_type(argname="argument on_prem_version", value=on_prem_version, expected_type=type_hints["on_prem_version"])
            check_type(argname="argument platform_config", value=platform_config, expected_type=type_hints["platform_config"])
            check_type(argname="argument private_registry_config", value=private_registry_config, expected_type=type_hints["private_registry_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument vcenter", value=vcenter, expected_type=type_hints["vcenter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "network_config": network_config,
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
        if addon_node is not None:
            self._values["addon_node"] = addon_node
        if annotations is not None:
            self._values["annotations"] = annotations
        if anti_affinity_groups is not None:
            self._values["anti_affinity_groups"] = anti_affinity_groups
        if authorization is not None:
            self._values["authorization"] = authorization
        if auto_repair_config is not None:
            self._values["auto_repair_config"] = auto_repair_config
        if bootstrap_cluster_membership is not None:
            self._values["bootstrap_cluster_membership"] = bootstrap_cluster_membership
        if control_plane_node is not None:
            self._values["control_plane_node"] = control_plane_node
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if image_type is not None:
            self._values["image_type"] = image_type
        if load_balancer is not None:
            self._values["load_balancer"] = load_balancer
        if on_prem_version is not None:
            self._values["on_prem_version"] = on_prem_version
        if platform_config is not None:
            self._values["platform_config"] = platform_config
        if private_registry_config is not None:
            self._values["private_registry_config"] = private_registry_config
        if project is not None:
            self._values["project"] = project
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if vcenter is not None:
            self._values["vcenter"] = vcenter

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
    def location(self) -> builtins.str:
        '''The location of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#location GoogleGkeonpremVmwareAdminCluster#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The VMware admin cluster resource name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#name GoogleGkeonpremVmwareAdminCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_config(self) -> "GoogleGkeonpremVmwareAdminClusterNetworkConfig":
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#network_config GoogleGkeonpremVmwareAdminCluster#network_config}
        '''
        result = self._values.get("network_config")
        assert result is not None, "Required property 'network_config' is missing"
        return typing.cast("GoogleGkeonpremVmwareAdminClusterNetworkConfig", result)

    @builtins.property
    def addon_node(self) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterAddonNode]:
        '''addon_node block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#addon_node GoogleGkeonpremVmwareAdminCluster#addon_node}
        '''
        result = self._values.get("addon_node")
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterAddonNode], result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Annotations on the VMware Admin Cluster.

        This field has the same restrictions as Kubernetes annotations.
        The total size of all keys and values combined is limited to 256k.
        Key can have 2 segments: prefix (optional) and name (required),
        separated by a slash (/).
        Prefix must be a DNS subdomain.
        Name must be 63 characters or less, begin and end with alphanumerics,
        with dashes (-), underscores (_), dots (.), and alphanumerics between.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#annotations GoogleGkeonpremVmwareAdminCluster#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def anti_affinity_groups(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterAntiAffinityGroups]:
        '''anti_affinity_groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#anti_affinity_groups GoogleGkeonpremVmwareAdminCluster#anti_affinity_groups}
        '''
        result = self._values.get("anti_affinity_groups")
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterAntiAffinityGroups], result)

    @builtins.property
    def authorization(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterAuthorization]:
        '''authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#authorization GoogleGkeonpremVmwareAdminCluster#authorization}
        '''
        result = self._values.get("authorization")
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterAuthorization], result)

    @builtins.property
    def auto_repair_config(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterAutoRepairConfig]:
        '''auto_repair_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#auto_repair_config GoogleGkeonpremVmwareAdminCluster#auto_repair_config}
        '''
        result = self._values.get("auto_repair_config")
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterAutoRepairConfig], result)

    @builtins.property
    def bootstrap_cluster_membership(self) -> typing.Optional[builtins.str]:
        '''The bootstrap cluster this VMware admin cluster belongs to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#bootstrap_cluster_membership GoogleGkeonpremVmwareAdminCluster#bootstrap_cluster_membership}
        '''
        result = self._values.get("bootstrap_cluster_membership")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def control_plane_node(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterControlPlaneNode"]:
        '''control_plane_node block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#control_plane_node GoogleGkeonpremVmwareAdminCluster#control_plane_node}
        '''
        result = self._values.get("control_plane_node")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterControlPlaneNode"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human readable description of this VMware admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#description GoogleGkeonpremVmwareAdminCluster#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#id GoogleGkeonpremVmwareAdminCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_type(self) -> typing.Optional[builtins.str]:
        '''The OS image type for the VMware admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#image_type GoogleGkeonpremVmwareAdminCluster#image_type}
        '''
        result = self._values.get("image_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterLoadBalancer"]:
        '''load_balancer block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#load_balancer GoogleGkeonpremVmwareAdminCluster#load_balancer}
        '''
        result = self._values.get("load_balancer")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterLoadBalancer"], result)

    @builtins.property
    def on_prem_version(self) -> typing.Optional[builtins.str]:
        '''The Anthos clusters on the VMware version for the admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#on_prem_version GoogleGkeonpremVmwareAdminCluster#on_prem_version}
        '''
        result = self._values.get("on_prem_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platform_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterPlatformConfig"]:
        '''platform_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#platform_config GoogleGkeonpremVmwareAdminCluster#platform_config}
        '''
        result = self._values.get("platform_config")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterPlatformConfig"], result)

    @builtins.property
    def private_registry_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterPrivateRegistryConfig"]:
        '''private_registry_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#private_registry_config GoogleGkeonpremVmwareAdminCluster#private_registry_config}
        '''
        result = self._values.get("private_registry_config")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterPrivateRegistryConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#project GoogleGkeonpremVmwareAdminCluster#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#timeouts GoogleGkeonpremVmwareAdminCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterTimeouts"], result)

    @builtins.property
    def vcenter(self) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterVcenter"]:
        '''vcenter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#vcenter GoogleGkeonpremVmwareAdminCluster#vcenter}
        '''
        result = self._values.get("vcenter")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterVcenter"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterControlPlaneNode",
    jsii_struct_bases=[],
    name_mapping={"cpus": "cpus", "memory": "memory", "replicas": "replicas"},
)
class GoogleGkeonpremVmwareAdminClusterControlPlaneNode:
    def __init__(
        self,
        *,
        cpus: typing.Optional[jsii.Number] = None,
        memory: typing.Optional[jsii.Number] = None,
        replicas: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpus: The number of vCPUs for the control-plane node of the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#cpus GoogleGkeonpremVmwareAdminCluster#cpus}
        :param memory: The number of mebibytes of memory for the control-plane node of the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#memory GoogleGkeonpremVmwareAdminCluster#memory}
        :param replicas: The number of control plane nodes for this VMware admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#replicas GoogleGkeonpremVmwareAdminCluster#replicas}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a066765a7dd1e91e4f13d609752858bb680e49003435002cffc75a71dcb5e0e)
            check_type(argname="argument cpus", value=cpus, expected_type=type_hints["cpus"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument replicas", value=replicas, expected_type=type_hints["replicas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpus is not None:
            self._values["cpus"] = cpus
        if memory is not None:
            self._values["memory"] = memory
        if replicas is not None:
            self._values["replicas"] = replicas

    @builtins.property
    def cpus(self) -> typing.Optional[jsii.Number]:
        '''The number of vCPUs for the control-plane node of the admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#cpus GoogleGkeonpremVmwareAdminCluster#cpus}
        '''
        result = self._values.get("cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory(self) -> typing.Optional[jsii.Number]:
        '''The number of mebibytes of memory for the control-plane node of the admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#memory GoogleGkeonpremVmwareAdminCluster#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def replicas(self) -> typing.Optional[jsii.Number]:
        '''The number of control plane nodes for this VMware admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#replicas GoogleGkeonpremVmwareAdminCluster#replicas}
        '''
        result = self._values.get("replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterControlPlaneNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareAdminClusterControlPlaneNodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterControlPlaneNodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c018cb71498b5d3eb9abd98655ebce3b6ecc444eef35a28a7268ad17992c3ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCpus")
    def reset_cpus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpus", []))

    @jsii.member(jsii_name="resetMemory")
    def reset_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemory", []))

    @jsii.member(jsii_name="resetReplicas")
    def reset_replicas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicas", []))

    @builtins.property
    @jsii.member(jsii_name="cpusInput")
    def cpus_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpusInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="replicasInput")
    def replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicasInput"))

    @builtins.property
    @jsii.member(jsii_name="cpus")
    def cpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpus"))

    @cpus.setter
    def cpus(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1251e2dc34a47235d99477efce2f82efd5b0f7c258c0525cbd8fe187baa39e07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf4a5fba657cb37623604829b6eab5239c83262f8de17bd00cf1698a05028047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicas")
    def replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicas"))

    @replicas.setter
    def replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7a68810fe0d441411eaee2e4c23b0496c20d29a41bbbd907d8df2b9464893b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterControlPlaneNode]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterControlPlaneNode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterControlPlaneNode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68718bdb8e5f5ac031f84648469fe29662d53910f129d9bf07738c6c3e724097)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterFleet",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremVmwareAdminClusterFleet:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterFleet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareAdminClusterFleetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterFleetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fbac2934875da50ab45bdb024da99fdecddb1b1800e7d3ef74d4a55410c1c4d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareAdminClusterFleetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0922395cae1b6db58b03d812f4d618092c2a3017d5bd369de0f31d62da411f4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareAdminClusterFleetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ae05db6e81b58eba0ed555a390acf76e5ca5b265f38a88f402eb94d2e50b3e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dea96367651447f7ef9991c3dcdb309ca2873e4732cf396f642e3adf01604f4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97217e8bac2a9c3840495f12efed1204fd4c43b9533c657985e4a0b10430565c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareAdminClusterFleetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterFleetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e0dd195e62fd72423f9e5ee2c22f94c069efda84f081df4a656783e6a762ec0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="membership")
    def membership(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "membership"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterFleet]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterFleet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterFleet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcea13f72a2a5ff633c52b0d11cebf661460fc3df491c59a1c18f2cfc8241503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterLoadBalancer",
    jsii_struct_bases=[],
    name_mapping={
        "vip_config": "vipConfig",
        "f5_config": "f5Config",
        "manual_lb_config": "manualLbConfig",
        "metal_lb_config": "metalLbConfig",
    },
)
class GoogleGkeonpremVmwareAdminClusterLoadBalancer:
    def __init__(
        self,
        *,
        vip_config: typing.Union["GoogleGkeonpremVmwareAdminClusterLoadBalancerVipConfig", typing.Dict[builtins.str, typing.Any]],
        f5_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterLoadBalancerF5Config", typing.Dict[builtins.str, typing.Any]]] = None,
        manual_lb_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterLoadBalancerManualLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        metal_lb_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param vip_config: vip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#vip_config GoogleGkeonpremVmwareAdminCluster#vip_config}
        :param f5_config: f5_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#f5_config GoogleGkeonpremVmwareAdminCluster#f5_config}
        :param manual_lb_config: manual_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#manual_lb_config GoogleGkeonpremVmwareAdminCluster#manual_lb_config}
        :param metal_lb_config: metal_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#metal_lb_config GoogleGkeonpremVmwareAdminCluster#metal_lb_config}
        '''
        if isinstance(vip_config, dict):
            vip_config = GoogleGkeonpremVmwareAdminClusterLoadBalancerVipConfig(**vip_config)
        if isinstance(f5_config, dict):
            f5_config = GoogleGkeonpremVmwareAdminClusterLoadBalancerF5Config(**f5_config)
        if isinstance(manual_lb_config, dict):
            manual_lb_config = GoogleGkeonpremVmwareAdminClusterLoadBalancerManualLbConfig(**manual_lb_config)
        if isinstance(metal_lb_config, dict):
            metal_lb_config = GoogleGkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig(**metal_lb_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88be2923c9265313598e87918ab15aedbb3a63b072c7d0763663e6f1629d3b7e)
            check_type(argname="argument vip_config", value=vip_config, expected_type=type_hints["vip_config"])
            check_type(argname="argument f5_config", value=f5_config, expected_type=type_hints["f5_config"])
            check_type(argname="argument manual_lb_config", value=manual_lb_config, expected_type=type_hints["manual_lb_config"])
            check_type(argname="argument metal_lb_config", value=metal_lb_config, expected_type=type_hints["metal_lb_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vip_config": vip_config,
        }
        if f5_config is not None:
            self._values["f5_config"] = f5_config
        if manual_lb_config is not None:
            self._values["manual_lb_config"] = manual_lb_config
        if metal_lb_config is not None:
            self._values["metal_lb_config"] = metal_lb_config

    @builtins.property
    def vip_config(self) -> "GoogleGkeonpremVmwareAdminClusterLoadBalancerVipConfig":
        '''vip_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#vip_config GoogleGkeonpremVmwareAdminCluster#vip_config}
        '''
        result = self._values.get("vip_config")
        assert result is not None, "Required property 'vip_config' is missing"
        return typing.cast("GoogleGkeonpremVmwareAdminClusterLoadBalancerVipConfig", result)

    @builtins.property
    def f5_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterLoadBalancerF5Config"]:
        '''f5_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#f5_config GoogleGkeonpremVmwareAdminCluster#f5_config}
        '''
        result = self._values.get("f5_config")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterLoadBalancerF5Config"], result)

    @builtins.property
    def manual_lb_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterLoadBalancerManualLbConfig"]:
        '''manual_lb_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#manual_lb_config GoogleGkeonpremVmwareAdminCluster#manual_lb_config}
        '''
        result = self._values.get("manual_lb_config")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterLoadBalancerManualLbConfig"], result)

    @builtins.property
    def metal_lb_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig"]:
        '''metal_lb_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#metal_lb_config GoogleGkeonpremVmwareAdminCluster#metal_lb_config}
        '''
        result = self._values.get("metal_lb_config")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterLoadBalancer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterLoadBalancerF5Config",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "partition": "partition",
        "snat_pool": "snatPool",
    },
)
class GoogleGkeonpremVmwareAdminClusterLoadBalancerF5Config:
    def __init__(
        self,
        *,
        address: typing.Optional[builtins.str] = None,
        partition: typing.Optional[builtins.str] = None,
        snat_pool: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: The load balancer's IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#address GoogleGkeonpremVmwareAdminCluster#address}
        :param partition: he preexisting partition to be used by the load balancer. T his partition is usually created for the admin cluster for example: 'my-f5-admin-partition'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#partition GoogleGkeonpremVmwareAdminCluster#partition}
        :param snat_pool: The pool name. Only necessary, if using SNAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#snat_pool GoogleGkeonpremVmwareAdminCluster#snat_pool}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72a84a9659d9a6aa838c7981cecc8a99803b2a1e7010e82de4bf9d1fecfd72d7)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument partition", value=partition, expected_type=type_hints["partition"])
            check_type(argname="argument snat_pool", value=snat_pool, expected_type=type_hints["snat_pool"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address is not None:
            self._values["address"] = address
        if partition is not None:
            self._values["partition"] = partition
        if snat_pool is not None:
            self._values["snat_pool"] = snat_pool

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''The load balancer's IP address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#address GoogleGkeonpremVmwareAdminCluster#address}
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partition(self) -> typing.Optional[builtins.str]:
        '''he preexisting partition to be used by the load balancer.

        T
        his partition is usually created for the admin cluster for example:
        'my-f5-admin-partition'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#partition GoogleGkeonpremVmwareAdminCluster#partition}
        '''
        result = self._values.get("partition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snat_pool(self) -> typing.Optional[builtins.str]:
        '''The pool name. Only necessary, if using SNAT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#snat_pool GoogleGkeonpremVmwareAdminCluster#snat_pool}
        '''
        result = self._values.get("snat_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterLoadBalancerF5Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareAdminClusterLoadBalancerF5ConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterLoadBalancerF5ConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f815aedc3d69caafc2734533cc0db838477f4a566ff86d50355c401018d3317)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @jsii.member(jsii_name="resetPartition")
    def reset_partition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartition", []))

    @jsii.member(jsii_name="resetSnatPool")
    def reset_snat_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnatPool", []))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionInput")
    def partition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partitionInput"))

    @builtins.property
    @jsii.member(jsii_name="snatPoolInput")
    def snat_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snatPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbc9db69b94c0a19be0ef89fd2675b480a5c3a761511e2687765679a325d4b7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partition")
    def partition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partition"))

    @partition.setter
    def partition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3e550c486359a1f3d7976675b2c95c2ec3c1013fe5ce0ef0700186edb63befc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snatPool")
    def snat_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snatPool"))

    @snat_pool.setter
    def snat_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d661791ebc07d7d69595ee270e0509e53dab6449d490c0e97c39e83d115af116)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snatPool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancerF5Config]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancerF5Config], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancerF5Config],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__631ccac68e79bd61f1c7f83cc3317befd99cfbe6624d0233252f0b56af335429)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterLoadBalancerManualLbConfig",
    jsii_struct_bases=[],
    name_mapping={
        "addons_node_port": "addonsNodePort",
        "control_plane_node_port": "controlPlaneNodePort",
        "ingress_http_node_port": "ingressHttpNodePort",
        "ingress_https_node_port": "ingressHttpsNodePort",
        "konnectivity_server_node_port": "konnectivityServerNodePort",
    },
)
class GoogleGkeonpremVmwareAdminClusterLoadBalancerManualLbConfig:
    def __init__(
        self,
        *,
        addons_node_port: typing.Optional[jsii.Number] = None,
        control_plane_node_port: typing.Optional[jsii.Number] = None,
        ingress_http_node_port: typing.Optional[jsii.Number] = None,
        ingress_https_node_port: typing.Optional[jsii.Number] = None,
        konnectivity_server_node_port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param addons_node_port: NodePort for add-ons server in the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#addons_node_port GoogleGkeonpremVmwareAdminCluster#addons_node_port}
        :param control_plane_node_port: NodePort for control plane service. The Kubernetes API server in the admin cluster is implemented as a Service of type NodePort (ex. 30968). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#control_plane_node_port GoogleGkeonpremVmwareAdminCluster#control_plane_node_port}
        :param ingress_http_node_port: NodePort for ingress service's http. The ingress service in the admin cluster is implemented as a Service of type NodePort (ex. 32527). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ingress_http_node_port GoogleGkeonpremVmwareAdminCluster#ingress_http_node_port}
        :param ingress_https_node_port: NodePort for ingress service's https. The ingress service in the admin cluster is implemented as a Service of type NodePort (ex. 30139). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ingress_https_node_port GoogleGkeonpremVmwareAdminCluster#ingress_https_node_port}
        :param konnectivity_server_node_port: NodePort for konnectivity server service running as a sidecar in each kube-apiserver pod (ex. 30564). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#konnectivity_server_node_port GoogleGkeonpremVmwareAdminCluster#konnectivity_server_node_port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e80377f93f5d03975e63a98fb8780f7f9d3ff14e6d024f623d6d9aef03543925)
            check_type(argname="argument addons_node_port", value=addons_node_port, expected_type=type_hints["addons_node_port"])
            check_type(argname="argument control_plane_node_port", value=control_plane_node_port, expected_type=type_hints["control_plane_node_port"])
            check_type(argname="argument ingress_http_node_port", value=ingress_http_node_port, expected_type=type_hints["ingress_http_node_port"])
            check_type(argname="argument ingress_https_node_port", value=ingress_https_node_port, expected_type=type_hints["ingress_https_node_port"])
            check_type(argname="argument konnectivity_server_node_port", value=konnectivity_server_node_port, expected_type=type_hints["konnectivity_server_node_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if addons_node_port is not None:
            self._values["addons_node_port"] = addons_node_port
        if control_plane_node_port is not None:
            self._values["control_plane_node_port"] = control_plane_node_port
        if ingress_http_node_port is not None:
            self._values["ingress_http_node_port"] = ingress_http_node_port
        if ingress_https_node_port is not None:
            self._values["ingress_https_node_port"] = ingress_https_node_port
        if konnectivity_server_node_port is not None:
            self._values["konnectivity_server_node_port"] = konnectivity_server_node_port

    @builtins.property
    def addons_node_port(self) -> typing.Optional[jsii.Number]:
        '''NodePort for add-ons server in the admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#addons_node_port GoogleGkeonpremVmwareAdminCluster#addons_node_port}
        '''
        result = self._values.get("addons_node_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def control_plane_node_port(self) -> typing.Optional[jsii.Number]:
        '''NodePort for control plane service.

        The Kubernetes API server in the admin
        cluster is implemented as a Service of type NodePort (ex. 30968).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#control_plane_node_port GoogleGkeonpremVmwareAdminCluster#control_plane_node_port}
        '''
        result = self._values.get("control_plane_node_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ingress_http_node_port(self) -> typing.Optional[jsii.Number]:
        '''NodePort for ingress service's http.

        The ingress service in the admin
        cluster is implemented as a Service of type NodePort (ex. 32527).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ingress_http_node_port GoogleGkeonpremVmwareAdminCluster#ingress_http_node_port}
        '''
        result = self._values.get("ingress_http_node_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ingress_https_node_port(self) -> typing.Optional[jsii.Number]:
        '''NodePort for ingress service's https.

        The ingress service in the admin
        cluster is implemented as a Service of type NodePort (ex. 30139).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ingress_https_node_port GoogleGkeonpremVmwareAdminCluster#ingress_https_node_port}
        '''
        result = self._values.get("ingress_https_node_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def konnectivity_server_node_port(self) -> typing.Optional[jsii.Number]:
        '''NodePort for konnectivity server service running as a sidecar in each kube-apiserver pod (ex. 30564).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#konnectivity_server_node_port GoogleGkeonpremVmwareAdminCluster#konnectivity_server_node_port}
        '''
        result = self._values.get("konnectivity_server_node_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterLoadBalancerManualLbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareAdminClusterLoadBalancerManualLbConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterLoadBalancerManualLbConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7daf3a255fca4e1635c00c0e247b7926c3acb58c1f4f1b07416c2b4ac2b2e17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddonsNodePort")
    def reset_addons_node_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddonsNodePort", []))

    @jsii.member(jsii_name="resetControlPlaneNodePort")
    def reset_control_plane_node_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControlPlaneNodePort", []))

    @jsii.member(jsii_name="resetIngressHttpNodePort")
    def reset_ingress_http_node_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressHttpNodePort", []))

    @jsii.member(jsii_name="resetIngressHttpsNodePort")
    def reset_ingress_https_node_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressHttpsNodePort", []))

    @jsii.member(jsii_name="resetKonnectivityServerNodePort")
    def reset_konnectivity_server_node_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKonnectivityServerNodePort", []))

    @builtins.property
    @jsii.member(jsii_name="addonsNodePortInput")
    def addons_node_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "addonsNodePortInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneNodePortInput")
    def control_plane_node_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "controlPlaneNodePortInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressHttpNodePortInput")
    def ingress_http_node_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ingressHttpNodePortInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressHttpsNodePortInput")
    def ingress_https_node_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ingressHttpsNodePortInput"))

    @builtins.property
    @jsii.member(jsii_name="konnectivityServerNodePortInput")
    def konnectivity_server_node_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "konnectivityServerNodePortInput"))

    @builtins.property
    @jsii.member(jsii_name="addonsNodePort")
    def addons_node_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "addonsNodePort"))

    @addons_node_port.setter
    def addons_node_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07cd5bfaaf27d157d3075cb08b4abece176faa7e236abdddf95f1dbeff935200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addonsNodePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="controlPlaneNodePort")
    def control_plane_node_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "controlPlaneNodePort"))

    @control_plane_node_port.setter
    def control_plane_node_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faaf42e8eb25f67c89a2c81a5979b4da3d2b43c406331716a3666100132183ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneNodePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingressHttpNodePort")
    def ingress_http_node_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ingressHttpNodePort"))

    @ingress_http_node_port.setter
    def ingress_http_node_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56692e2fe6d744b48f6ab2a58c7c355e88608c713d71b610de21a6c909a596a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingressHttpNodePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingressHttpsNodePort")
    def ingress_https_node_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ingressHttpsNodePort"))

    @ingress_https_node_port.setter
    def ingress_https_node_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad58b01fedc33c2df7eb70fbf1a25574410ee6740552152046f1efa5a4f4896a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingressHttpsNodePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="konnectivityServerNodePort")
    def konnectivity_server_node_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "konnectivityServerNodePort"))

    @konnectivity_server_node_port.setter
    def konnectivity_server_node_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c972a9daa4b1688c98cab9a31a9aac3ccf0adcebee3c4a8a4103788425c60cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "konnectivityServerNodePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancerManualLbConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancerManualLbConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancerManualLbConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__061cabeb365485c208be3af9503599d849f4edfb0311716c79aec99c5e37e8bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleGkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Metal LB is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#enabled GoogleGkeonpremVmwareAdminCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c5638e864531b37659840e7d38b15e75c3a0608231e321256400b1ca23e0e60)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Metal LB is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#enabled GoogleGkeonpremVmwareAdminCluster#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareAdminClusterLoadBalancerMetalLbConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterLoadBalancerMetalLbConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0a998a78432ab52dedd4f088b3c4823f2b862fc17a654d5f473ad3ab7bc0c5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f73e7542a423dc36dcf96345535630a53e9870fae8b7713e3d4f6281913cf0aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d161cfcd596f5a7f95c25e0cfab0884c5c090aeb63ee33c15ce42eeaa650db19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareAdminClusterLoadBalancerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterLoadBalancerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__768fc07f6d032b6f00919f1772f274052a2acf5ccfc6c47362b6c0eac5e6f7b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putF5Config")
    def put_f5_config(
        self,
        *,
        address: typing.Optional[builtins.str] = None,
        partition: typing.Optional[builtins.str] = None,
        snat_pool: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: The load balancer's IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#address GoogleGkeonpremVmwareAdminCluster#address}
        :param partition: he preexisting partition to be used by the load balancer. T his partition is usually created for the admin cluster for example: 'my-f5-admin-partition'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#partition GoogleGkeonpremVmwareAdminCluster#partition}
        :param snat_pool: The pool name. Only necessary, if using SNAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#snat_pool GoogleGkeonpremVmwareAdminCluster#snat_pool}
        '''
        value = GoogleGkeonpremVmwareAdminClusterLoadBalancerF5Config(
            address=address, partition=partition, snat_pool=snat_pool
        )

        return typing.cast(None, jsii.invoke(self, "putF5Config", [value]))

    @jsii.member(jsii_name="putManualLbConfig")
    def put_manual_lb_config(
        self,
        *,
        addons_node_port: typing.Optional[jsii.Number] = None,
        control_plane_node_port: typing.Optional[jsii.Number] = None,
        ingress_http_node_port: typing.Optional[jsii.Number] = None,
        ingress_https_node_port: typing.Optional[jsii.Number] = None,
        konnectivity_server_node_port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param addons_node_port: NodePort for add-ons server in the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#addons_node_port GoogleGkeonpremVmwareAdminCluster#addons_node_port}
        :param control_plane_node_port: NodePort for control plane service. The Kubernetes API server in the admin cluster is implemented as a Service of type NodePort (ex. 30968). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#control_plane_node_port GoogleGkeonpremVmwareAdminCluster#control_plane_node_port}
        :param ingress_http_node_port: NodePort for ingress service's http. The ingress service in the admin cluster is implemented as a Service of type NodePort (ex. 32527). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ingress_http_node_port GoogleGkeonpremVmwareAdminCluster#ingress_http_node_port}
        :param ingress_https_node_port: NodePort for ingress service's https. The ingress service in the admin cluster is implemented as a Service of type NodePort (ex. 30139). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ingress_https_node_port GoogleGkeonpremVmwareAdminCluster#ingress_https_node_port}
        :param konnectivity_server_node_port: NodePort for konnectivity server service running as a sidecar in each kube-apiserver pod (ex. 30564). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#konnectivity_server_node_port GoogleGkeonpremVmwareAdminCluster#konnectivity_server_node_port}
        '''
        value = GoogleGkeonpremVmwareAdminClusterLoadBalancerManualLbConfig(
            addons_node_port=addons_node_port,
            control_plane_node_port=control_plane_node_port,
            ingress_http_node_port=ingress_http_node_port,
            ingress_https_node_port=ingress_https_node_port,
            konnectivity_server_node_port=konnectivity_server_node_port,
        )

        return typing.cast(None, jsii.invoke(self, "putManualLbConfig", [value]))

    @jsii.member(jsii_name="putMetalLbConfig")
    def put_metal_lb_config(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Metal LB is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#enabled GoogleGkeonpremVmwareAdminCluster#enabled}
        '''
        value = GoogleGkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putMetalLbConfig", [value]))

    @jsii.member(jsii_name="putVipConfig")
    def put_vip_config(
        self,
        *,
        control_plane_vip: builtins.str,
        addons_vip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param control_plane_vip: The VIP which you previously set aside for the Kubernetes API of this VMware Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#control_plane_vip GoogleGkeonpremVmwareAdminCluster#control_plane_vip}
        :param addons_vip: The VIP to configure the load balancer for add-ons. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#addons_vip GoogleGkeonpremVmwareAdminCluster#addons_vip}
        '''
        value = GoogleGkeonpremVmwareAdminClusterLoadBalancerVipConfig(
            control_plane_vip=control_plane_vip, addons_vip=addons_vip
        )

        return typing.cast(None, jsii.invoke(self, "putVipConfig", [value]))

    @jsii.member(jsii_name="resetF5Config")
    def reset_f5_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetF5Config", []))

    @jsii.member(jsii_name="resetManualLbConfig")
    def reset_manual_lb_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManualLbConfig", []))

    @jsii.member(jsii_name="resetMetalLbConfig")
    def reset_metal_lb_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetalLbConfig", []))

    @builtins.property
    @jsii.member(jsii_name="f5Config")
    def f5_config(
        self,
    ) -> GoogleGkeonpremVmwareAdminClusterLoadBalancerF5ConfigOutputReference:
        return typing.cast(GoogleGkeonpremVmwareAdminClusterLoadBalancerF5ConfigOutputReference, jsii.get(self, "f5Config"))

    @builtins.property
    @jsii.member(jsii_name="manualLbConfig")
    def manual_lb_config(
        self,
    ) -> GoogleGkeonpremVmwareAdminClusterLoadBalancerManualLbConfigOutputReference:
        return typing.cast(GoogleGkeonpremVmwareAdminClusterLoadBalancerManualLbConfigOutputReference, jsii.get(self, "manualLbConfig"))

    @builtins.property
    @jsii.member(jsii_name="metalLbConfig")
    def metal_lb_config(
        self,
    ) -> GoogleGkeonpremVmwareAdminClusterLoadBalancerMetalLbConfigOutputReference:
        return typing.cast(GoogleGkeonpremVmwareAdminClusterLoadBalancerMetalLbConfigOutputReference, jsii.get(self, "metalLbConfig"))

    @builtins.property
    @jsii.member(jsii_name="vipConfig")
    def vip_config(
        self,
    ) -> "GoogleGkeonpremVmwareAdminClusterLoadBalancerVipConfigOutputReference":
        return typing.cast("GoogleGkeonpremVmwareAdminClusterLoadBalancerVipConfigOutputReference", jsii.get(self, "vipConfig"))

    @builtins.property
    @jsii.member(jsii_name="f5ConfigInput")
    def f5_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancerF5Config]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancerF5Config], jsii.get(self, "f5ConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="manualLbConfigInput")
    def manual_lb_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancerManualLbConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancerManualLbConfig], jsii.get(self, "manualLbConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="metalLbConfigInput")
    def metal_lb_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig], jsii.get(self, "metalLbConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="vipConfigInput")
    def vip_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterLoadBalancerVipConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterLoadBalancerVipConfig"], jsii.get(self, "vipConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancer]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7029f1bf50faeb5e5b57fe17e419f0e416793499dfd55ec2b21ed0a3bbe4d526)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterLoadBalancerVipConfig",
    jsii_struct_bases=[],
    name_mapping={"control_plane_vip": "controlPlaneVip", "addons_vip": "addonsVip"},
)
class GoogleGkeonpremVmwareAdminClusterLoadBalancerVipConfig:
    def __init__(
        self,
        *,
        control_plane_vip: builtins.str,
        addons_vip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param control_plane_vip: The VIP which you previously set aside for the Kubernetes API of this VMware Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#control_plane_vip GoogleGkeonpremVmwareAdminCluster#control_plane_vip}
        :param addons_vip: The VIP to configure the load balancer for add-ons. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#addons_vip GoogleGkeonpremVmwareAdminCluster#addons_vip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96a202040fe549f3c97343565cd86cd82300afeaa983f0c9d3ad56915dbcd16f)
            check_type(argname="argument control_plane_vip", value=control_plane_vip, expected_type=type_hints["control_plane_vip"])
            check_type(argname="argument addons_vip", value=addons_vip, expected_type=type_hints["addons_vip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "control_plane_vip": control_plane_vip,
        }
        if addons_vip is not None:
            self._values["addons_vip"] = addons_vip

    @builtins.property
    def control_plane_vip(self) -> builtins.str:
        '''The VIP which you previously set aside for the Kubernetes API of this VMware Admin Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#control_plane_vip GoogleGkeonpremVmwareAdminCluster#control_plane_vip}
        '''
        result = self._values.get("control_plane_vip")
        assert result is not None, "Required property 'control_plane_vip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def addons_vip(self) -> typing.Optional[builtins.str]:
        '''The VIP to configure the load balancer for add-ons.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#addons_vip GoogleGkeonpremVmwareAdminCluster#addons_vip}
        '''
        result = self._values.get("addons_vip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterLoadBalancerVipConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareAdminClusterLoadBalancerVipConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterLoadBalancerVipConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dba20c9a891a3896e6a1be400cb9e46eabb56e4dfa3009be2de4d0d2b9bda3d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddonsVip")
    def reset_addons_vip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddonsVip", []))

    @builtins.property
    @jsii.member(jsii_name="addonsVipInput")
    def addons_vip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addonsVipInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneVipInput")
    def control_plane_vip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "controlPlaneVipInput"))

    @builtins.property
    @jsii.member(jsii_name="addonsVip")
    def addons_vip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "addonsVip"))

    @addons_vip.setter
    def addons_vip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83b784f760ae7cbd46f1d42940150f8b714d0338c6f5c5beefd197a0b7212d2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addonsVip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="controlPlaneVip")
    def control_plane_vip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "controlPlaneVip"))

    @control_plane_vip.setter
    def control_plane_vip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b260b22bcaa7e0b996bc1aca8a92f6466b6a58276d1f091cbb1cfd5ab3980ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneVip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancerVipConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancerVipConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancerVipConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e56f731b857af5408217cbd96dd96929beb15c345918d711bcfeb05b23657c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={
        "pod_address_cidr_blocks": "podAddressCidrBlocks",
        "service_address_cidr_blocks": "serviceAddressCidrBlocks",
        "dhcp_ip_config": "dhcpIpConfig",
        "ha_control_plane_config": "haControlPlaneConfig",
        "host_config": "hostConfig",
        "static_ip_config": "staticIpConfig",
        "vcenter_network": "vcenterNetwork",
    },
)
class GoogleGkeonpremVmwareAdminClusterNetworkConfig:
    def __init__(
        self,
        *,
        pod_address_cidr_blocks: typing.Sequence[builtins.str],
        service_address_cidr_blocks: typing.Sequence[builtins.str],
        dhcp_ip_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ha_control_plane_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        host_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterNetworkConfigHostConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        static_ip_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        vcenter_network: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pod_address_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#pod_address_cidr_blocks GoogleGkeonpremVmwareAdminCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported.. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#service_address_cidr_blocks GoogleGkeonpremVmwareAdminCluster#service_address_cidr_blocks}
        :param dhcp_ip_config: dhcp_ip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#dhcp_ip_config GoogleGkeonpremVmwareAdminCluster#dhcp_ip_config}
        :param ha_control_plane_config: ha_control_plane_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ha_control_plane_config GoogleGkeonpremVmwareAdminCluster#ha_control_plane_config}
        :param host_config: host_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#host_config GoogleGkeonpremVmwareAdminCluster#host_config}
        :param static_ip_config: static_ip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#static_ip_config GoogleGkeonpremVmwareAdminCluster#static_ip_config}
        :param vcenter_network: vcenter_network specifies vCenter network name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#vcenter_network GoogleGkeonpremVmwareAdminCluster#vcenter_network}
        '''
        if isinstance(dhcp_ip_config, dict):
            dhcp_ip_config = GoogleGkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig(**dhcp_ip_config)
        if isinstance(ha_control_plane_config, dict):
            ha_control_plane_config = GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig(**ha_control_plane_config)
        if isinstance(host_config, dict):
            host_config = GoogleGkeonpremVmwareAdminClusterNetworkConfigHostConfig(**host_config)
        if isinstance(static_ip_config, dict):
            static_ip_config = GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig(**static_ip_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__167e56c2c4e1d96f0c3f8919a9db31e640c2292fdde0fb8e2bb0c0ee1bf268d0)
            check_type(argname="argument pod_address_cidr_blocks", value=pod_address_cidr_blocks, expected_type=type_hints["pod_address_cidr_blocks"])
            check_type(argname="argument service_address_cidr_blocks", value=service_address_cidr_blocks, expected_type=type_hints["service_address_cidr_blocks"])
            check_type(argname="argument dhcp_ip_config", value=dhcp_ip_config, expected_type=type_hints["dhcp_ip_config"])
            check_type(argname="argument ha_control_plane_config", value=ha_control_plane_config, expected_type=type_hints["ha_control_plane_config"])
            check_type(argname="argument host_config", value=host_config, expected_type=type_hints["host_config"])
            check_type(argname="argument static_ip_config", value=static_ip_config, expected_type=type_hints["static_ip_config"])
            check_type(argname="argument vcenter_network", value=vcenter_network, expected_type=type_hints["vcenter_network"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pod_address_cidr_blocks": pod_address_cidr_blocks,
            "service_address_cidr_blocks": service_address_cidr_blocks,
        }
        if dhcp_ip_config is not None:
            self._values["dhcp_ip_config"] = dhcp_ip_config
        if ha_control_plane_config is not None:
            self._values["ha_control_plane_config"] = ha_control_plane_config
        if host_config is not None:
            self._values["host_config"] = host_config
        if static_ip_config is not None:
            self._values["static_ip_config"] = static_ip_config
        if vcenter_network is not None:
            self._values["vcenter_network"] = vcenter_network

    @builtins.property
    def pod_address_cidr_blocks(self) -> typing.List[builtins.str]:
        '''All pods in the cluster are assigned an RFC1918 IPv4 address from these ranges.

        Only a single range is supported. This field cannot be changed after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#pod_address_cidr_blocks GoogleGkeonpremVmwareAdminCluster#pod_address_cidr_blocks}
        '''
        result = self._values.get("pod_address_cidr_blocks")
        assert result is not None, "Required property 'pod_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        '''All services in the cluster are assigned an RFC1918 IPv4 address from these ranges.

        Only a single range is supported.. This field
        cannot be changed after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#service_address_cidr_blocks GoogleGkeonpremVmwareAdminCluster#service_address_cidr_blocks}
        '''
        result = self._values.get("service_address_cidr_blocks")
        assert result is not None, "Required property 'service_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def dhcp_ip_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig"]:
        '''dhcp_ip_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#dhcp_ip_config GoogleGkeonpremVmwareAdminCluster#dhcp_ip_config}
        '''
        result = self._values.get("dhcp_ip_config")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig"], result)

    @builtins.property
    def ha_control_plane_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig"]:
        '''ha_control_plane_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ha_control_plane_config GoogleGkeonpremVmwareAdminCluster#ha_control_plane_config}
        '''
        result = self._values.get("ha_control_plane_config")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig"], result)

    @builtins.property
    def host_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterNetworkConfigHostConfig"]:
        '''host_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#host_config GoogleGkeonpremVmwareAdminCluster#host_config}
        '''
        result = self._values.get("host_config")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterNetworkConfigHostConfig"], result)

    @builtins.property
    def static_ip_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig"]:
        '''static_ip_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#static_ip_config GoogleGkeonpremVmwareAdminCluster#static_ip_config}
        '''
        result = self._values.get("static_ip_config")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig"], result)

    @builtins.property
    def vcenter_network(self) -> typing.Optional[builtins.str]:
        '''vcenter_network specifies vCenter network name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#vcenter_network GoogleGkeonpremVmwareAdminCluster#vcenter_network}
        '''
        result = self._values.get("vcenter_network")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleGkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: enabled is a flag to mark if DHCP IP allocation is used for VMware admin clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#enabled GoogleGkeonpremVmwareAdminCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0806230e801e56ee5dc27372bd451e45118b5b905b148f807415e43842e966df)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''enabled is a flag to mark if DHCP IP allocation is used for VMware admin clusters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#enabled GoogleGkeonpremVmwareAdminCluster#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc4c3243f0831b1b44123aa700e02de09c7205eba6b437336d6147e333d77a16)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73b95f223d0b30523dde0655ba77db49cd42d4955b31831af313e89f635963cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6457c9f3536519c232d84e290ed617ca67b4ddbf7c7ffd6ec2b1cb4f385994f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig",
    jsii_struct_bases=[],
    name_mapping={"control_plane_ip_block": "controlPlaneIpBlock"},
)
class GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig:
    def __init__(
        self,
        *,
        control_plane_ip_block: typing.Optional[typing.Union["GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param control_plane_ip_block: control_plane_ip_block block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#control_plane_ip_block GoogleGkeonpremVmwareAdminCluster#control_plane_ip_block}
        '''
        if isinstance(control_plane_ip_block, dict):
            control_plane_ip_block = GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock(**control_plane_ip_block)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__814e633bfa5ff00faeea1e79c41308c8e6c14ac3ac6959a401636f51cec38e58)
            check_type(argname="argument control_plane_ip_block", value=control_plane_ip_block, expected_type=type_hints["control_plane_ip_block"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if control_plane_ip_block is not None:
            self._values["control_plane_ip_block"] = control_plane_ip_block

    @builtins.property
    def control_plane_ip_block(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock"]:
        '''control_plane_ip_block block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#control_plane_ip_block GoogleGkeonpremVmwareAdminCluster#control_plane_ip_block}
        '''
        result = self._values.get("control_plane_ip_block")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock",
    jsii_struct_bases=[],
    name_mapping={"gateway": "gateway", "ips": "ips", "netmask": "netmask"},
)
class GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock:
    def __init__(
        self,
        *,
        gateway: builtins.str,
        ips: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps", typing.Dict[builtins.str, typing.Any]]]],
        netmask: builtins.str,
    ) -> None:
        '''
        :param gateway: The network gateway used by the VMware Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#gateway GoogleGkeonpremVmwareAdminCluster#gateway}
        :param ips: ips block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ips GoogleGkeonpremVmwareAdminCluster#ips}
        :param netmask: The netmask used by the VMware Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#netmask GoogleGkeonpremVmwareAdminCluster#netmask}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff4b718db0c0d911ee23d8f4e12c27feb6e5c57f6dd63f3f0d70babda8a20939)
            check_type(argname="argument gateway", value=gateway, expected_type=type_hints["gateway"])
            check_type(argname="argument ips", value=ips, expected_type=type_hints["ips"])
            check_type(argname="argument netmask", value=netmask, expected_type=type_hints["netmask"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gateway": gateway,
            "ips": ips,
            "netmask": netmask,
        }

    @builtins.property
    def gateway(self) -> builtins.str:
        '''The network gateway used by the VMware Admin Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#gateway GoogleGkeonpremVmwareAdminCluster#gateway}
        '''
        result = self._values.get("gateway")
        assert result is not None, "Required property 'gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ips(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps"]]:
        '''ips block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ips GoogleGkeonpremVmwareAdminCluster#ips}
        '''
        result = self._values.get("ips")
        assert result is not None, "Required property 'ips' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps"]], result)

    @builtins.property
    def netmask(self) -> builtins.str:
        '''The netmask used by the VMware Admin Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#netmask GoogleGkeonpremVmwareAdminCluster#netmask}
        '''
        result = self._values.get("netmask")
        assert result is not None, "Required property 'netmask' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps",
    jsii_struct_bases=[],
    name_mapping={"ip": "ip", "hostname": "hostname"},
)
class GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps:
    def __init__(
        self,
        *,
        ip: builtins.str,
        hostname: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip: IP could be an IP address (like 1.2.3.4) or a CIDR (like 1.2.3.0/24). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ip GoogleGkeonpremVmwareAdminCluster#ip}
        :param hostname: Hostname of the machine. VM's name will be used if this field is empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#hostname GoogleGkeonpremVmwareAdminCluster#hostname}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__834edbe1f8dc81e826f43e6cbfd6c81aabeffb5ae8f3590aa15b1324fd4e5760)
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip": ip,
        }
        if hostname is not None:
            self._values["hostname"] = hostname

    @builtins.property
    def ip(self) -> builtins.str:
        '''IP could be an IP address (like 1.2.3.4) or a CIDR (like 1.2.3.0/24).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ip GoogleGkeonpremVmwareAdminCluster#ip}
        '''
        result = self._values.get("ip")
        assert result is not None, "Required property 'ip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''Hostname of the machine. VM's name will be used if this field is empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#hostname GoogleGkeonpremVmwareAdminCluster#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIpsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIpsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e25b63e539f94dfb3231b28d5dd4378d90d3630d8003ddf77e81baed95a86931)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIpsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c762511b2ee9368a8a6876c232e077261ba03a88cd3cfd3516cd676ea132c39a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIpsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c104aeea8323ba34f31a174fadace8bd13468b8e715a3883b51e85d314404e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc6e9408c7b25bb10d92b679f356374e1f553b68287dd8369b441b7e159efe58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3a5321b3a9684323e22705136368e6e0248e29320688ef7f70f1e8faa94909e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6833303c76a79712159c375fe0fd7a3bf22ee3860d679bf72bb235a028539f9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIpsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIpsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__248c0c809e86a346a66b50966371af64246cdbd054a2c242efc98e2bacadf1e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetHostname")
    def reset_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostname", []))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="ipInput")
    def ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipInput"))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__546ee89c0230667c570db4702bf1d1d12d32cc4bb79a17a666aa143f88ee589e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc4846ee1cd5661ccc57869f4a242dd99f850bd44dd9089ff8951b40eb6fd85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7579556172043b0c8b6253c7b87479eefa6999e30b17fe35c8884a2dc324fc8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__025d947d071e935cb9251efd029c69f171802bc4e422b8f976d7ab5a2e92c9c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIps")
    def put_ips(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcfe5bf48a116160b63ae27f32c4221b6ebbe1682ab7ed380ce583b04fb27dbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIps", [value]))

    @builtins.property
    @jsii.member(jsii_name="ips")
    def ips(
        self,
    ) -> GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIpsList:
        return typing.cast(GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIpsList, jsii.get(self, "ips"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="ipsInput")
    def ips_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps]]], jsii.get(self, "ipsInput"))

    @builtins.property
    @jsii.member(jsii_name="netmaskInput")
    def netmask_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "netmaskInput"))

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gateway"))

    @gateway.setter
    def gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__444e377f5401ed6872f2ba51344d636e209e53843c051625c637e8fbfd03656c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateway", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netmask")
    def netmask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netmask"))

    @netmask.setter
    def netmask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__961c44965232180aa657f618d07c806e06d73333bceab5c591a03932fd391a54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netmask", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ded06549e2113f545659d9221f09c65a7a1e97c0c4ce71dae1d85041d3179f2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0b9b23fd3beafb3f92c5ff2d2a22fcb1bbda27c8330a4e3cf6c2ac1ef6aa710)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putControlPlaneIpBlock")
    def put_control_plane_ip_block(
        self,
        *,
        gateway: builtins.str,
        ips: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps, typing.Dict[builtins.str, typing.Any]]]],
        netmask: builtins.str,
    ) -> None:
        '''
        :param gateway: The network gateway used by the VMware Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#gateway GoogleGkeonpremVmwareAdminCluster#gateway}
        :param ips: ips block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ips GoogleGkeonpremVmwareAdminCluster#ips}
        :param netmask: The netmask used by the VMware Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#netmask GoogleGkeonpremVmwareAdminCluster#netmask}
        '''
        value = GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock(
            gateway=gateway, ips=ips, netmask=netmask
        )

        return typing.cast(None, jsii.invoke(self, "putControlPlaneIpBlock", [value]))

    @jsii.member(jsii_name="resetControlPlaneIpBlock")
    def reset_control_plane_ip_block(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControlPlaneIpBlock", []))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneIpBlock")
    def control_plane_ip_block(
        self,
    ) -> GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockOutputReference:
        return typing.cast(GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockOutputReference, jsii.get(self, "controlPlaneIpBlock"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneIpBlockInput")
    def control_plane_ip_block_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock], jsii.get(self, "controlPlaneIpBlockInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc352383c3139dd1f7c00970edbc0928529c1f1c7c5725238648554078981911)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterNetworkConfigHostConfig",
    jsii_struct_bases=[],
    name_mapping={
        "dns_search_domains": "dnsSearchDomains",
        "dns_servers": "dnsServers",
        "ntp_servers": "ntpServers",
    },
)
class GoogleGkeonpremVmwareAdminClusterNetworkConfigHostConfig:
    def __init__(
        self,
        *,
        dns_search_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        ntp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param dns_search_domains: DNS search domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#dns_search_domains GoogleGkeonpremVmwareAdminCluster#dns_search_domains}
        :param dns_servers: DNS servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#dns_servers GoogleGkeonpremVmwareAdminCluster#dns_servers}
        :param ntp_servers: NTP servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ntp_servers GoogleGkeonpremVmwareAdminCluster#ntp_servers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65906c3c0e8fe5135afb766e5bc40a23c8444c8f9839059a756f5f943514e9ec)
            check_type(argname="argument dns_search_domains", value=dns_search_domains, expected_type=type_hints["dns_search_domains"])
            check_type(argname="argument dns_servers", value=dns_servers, expected_type=type_hints["dns_servers"])
            check_type(argname="argument ntp_servers", value=ntp_servers, expected_type=type_hints["ntp_servers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dns_search_domains is not None:
            self._values["dns_search_domains"] = dns_search_domains
        if dns_servers is not None:
            self._values["dns_servers"] = dns_servers
        if ntp_servers is not None:
            self._values["ntp_servers"] = ntp_servers

    @builtins.property
    def dns_search_domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''DNS search domains.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#dns_search_domains GoogleGkeonpremVmwareAdminCluster#dns_search_domains}
        '''
        result = self._values.get("dns_search_domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dns_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''DNS servers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#dns_servers GoogleGkeonpremVmwareAdminCluster#dns_servers}
        '''
        result = self._values.get("dns_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ntp_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''NTP servers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ntp_servers GoogleGkeonpremVmwareAdminCluster#ntp_servers}
        '''
        result = self._values.get("ntp_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterNetworkConfigHostConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareAdminClusterNetworkConfigHostConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterNetworkConfigHostConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8acb07facba350797db310dd3c24232d3114d890f6839433584336dcd4916be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDnsSearchDomains")
    def reset_dns_search_domains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsSearchDomains", []))

    @jsii.member(jsii_name="resetDnsServers")
    def reset_dns_servers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsServers", []))

    @jsii.member(jsii_name="resetNtpServers")
    def reset_ntp_servers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNtpServers", []))

    @builtins.property
    @jsii.member(jsii_name="dnsSearchDomainsInput")
    def dns_search_domains_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dnsSearchDomainsInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsServersInput")
    def dns_servers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dnsServersInput"))

    @builtins.property
    @jsii.member(jsii_name="ntpServersInput")
    def ntp_servers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ntpServersInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsSearchDomains")
    def dns_search_domains(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dnsSearchDomains"))

    @dns_search_domains.setter
    def dns_search_domains(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be979a7198cdac0c31cb2cc652c6316cd1b14728c233bb838a5b0751a206b19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsSearchDomains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsServers")
    def dns_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dnsServers"))

    @dns_servers.setter
    def dns_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a1f586fbfca5ec7dd96131a9e579678d86d56ac3f932ce32d4bee5c20802453)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ntpServers")
    def ntp_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ntpServers"))

    @ntp_servers.setter
    def ntp_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e377358cc2049e974bcb5e371d6776309239760b4cd4a277e5a9d82bacb3fc6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ntpServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigHostConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigHostConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigHostConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6feac3255e803ca2274d87582ff0ae2e9d19d75165e6e5463335b76e7891cfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareAdminClusterNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c2a9f24b7bcf55fe6ce2796259afd78f66b0655f9f6d8d65ce16fb24b6fb28a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDhcpIpConfig")
    def put_dhcp_ip_config(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: enabled is a flag to mark if DHCP IP allocation is used for VMware admin clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#enabled GoogleGkeonpremVmwareAdminCluster#enabled}
        '''
        value = GoogleGkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putDhcpIpConfig", [value]))

    @jsii.member(jsii_name="putHaControlPlaneConfig")
    def put_ha_control_plane_config(
        self,
        *,
        control_plane_ip_block: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param control_plane_ip_block: control_plane_ip_block block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#control_plane_ip_block GoogleGkeonpremVmwareAdminCluster#control_plane_ip_block}
        '''
        value = GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig(
            control_plane_ip_block=control_plane_ip_block
        )

        return typing.cast(None, jsii.invoke(self, "putHaControlPlaneConfig", [value]))

    @jsii.member(jsii_name="putHostConfig")
    def put_host_config(
        self,
        *,
        dns_search_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        ntp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param dns_search_domains: DNS search domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#dns_search_domains GoogleGkeonpremVmwareAdminCluster#dns_search_domains}
        :param dns_servers: DNS servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#dns_servers GoogleGkeonpremVmwareAdminCluster#dns_servers}
        :param ntp_servers: NTP servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ntp_servers GoogleGkeonpremVmwareAdminCluster#ntp_servers}
        '''
        value = GoogleGkeonpremVmwareAdminClusterNetworkConfigHostConfig(
            dns_search_domains=dns_search_domains,
            dns_servers=dns_servers,
            ntp_servers=ntp_servers,
        )

        return typing.cast(None, jsii.invoke(self, "putHostConfig", [value]))

    @jsii.member(jsii_name="putStaticIpConfig")
    def put_static_ip_config(
        self,
        *,
        ip_blocks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param ip_blocks: ip_blocks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ip_blocks GoogleGkeonpremVmwareAdminCluster#ip_blocks}
        '''
        value = GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig(
            ip_blocks=ip_blocks
        )

        return typing.cast(None, jsii.invoke(self, "putStaticIpConfig", [value]))

    @jsii.member(jsii_name="resetDhcpIpConfig")
    def reset_dhcp_ip_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDhcpIpConfig", []))

    @jsii.member(jsii_name="resetHaControlPlaneConfig")
    def reset_ha_control_plane_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaControlPlaneConfig", []))

    @jsii.member(jsii_name="resetHostConfig")
    def reset_host_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostConfig", []))

    @jsii.member(jsii_name="resetStaticIpConfig")
    def reset_static_ip_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStaticIpConfig", []))

    @jsii.member(jsii_name="resetVcenterNetwork")
    def reset_vcenter_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVcenterNetwork", []))

    @builtins.property
    @jsii.member(jsii_name="dhcpIpConfig")
    def dhcp_ip_config(
        self,
    ) -> GoogleGkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfigOutputReference:
        return typing.cast(GoogleGkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfigOutputReference, jsii.get(self, "dhcpIpConfig"))

    @builtins.property
    @jsii.member(jsii_name="haControlPlaneConfig")
    def ha_control_plane_config(
        self,
    ) -> GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigOutputReference:
        return typing.cast(GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigOutputReference, jsii.get(self, "haControlPlaneConfig"))

    @builtins.property
    @jsii.member(jsii_name="hostConfig")
    def host_config(
        self,
    ) -> GoogleGkeonpremVmwareAdminClusterNetworkConfigHostConfigOutputReference:
        return typing.cast(GoogleGkeonpremVmwareAdminClusterNetworkConfigHostConfigOutputReference, jsii.get(self, "hostConfig"))

    @builtins.property
    @jsii.member(jsii_name="staticIpConfig")
    def static_ip_config(
        self,
    ) -> "GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigOutputReference":
        return typing.cast("GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigOutputReference", jsii.get(self, "staticIpConfig"))

    @builtins.property
    @jsii.member(jsii_name="dhcpIpConfigInput")
    def dhcp_ip_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig], jsii.get(self, "dhcpIpConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="haControlPlaneConfigInput")
    def ha_control_plane_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig], jsii.get(self, "haControlPlaneConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="hostConfigInput")
    def host_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigHostConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigHostConfig], jsii.get(self, "hostConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="podAddressCidrBlocksInput")
    def pod_address_cidr_blocks_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "podAddressCidrBlocksInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAddressCidrBlocksInput")
    def service_address_cidr_blocks_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "serviceAddressCidrBlocksInput"))

    @builtins.property
    @jsii.member(jsii_name="staticIpConfigInput")
    def static_ip_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig"], jsii.get(self, "staticIpConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="vcenterNetworkInput")
    def vcenter_network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vcenterNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="podAddressCidrBlocks")
    def pod_address_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "podAddressCidrBlocks"))

    @pod_address_cidr_blocks.setter
    def pod_address_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72d516de39c0129f7bfa1df1d130f7b756edc316c9813f2c8696ebfb2775bbe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAddressCidrBlocks")
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceAddressCidrBlocks"))

    @service_address_cidr_blocks.setter
    def service_address_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfff3287aae32cd5606810c5b1e446b72c084acbc45120a42566fce175823162)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vcenterNetwork")
    def vcenter_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vcenterNetwork"))

    @vcenter_network.setter
    def vcenter_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17442819239d1250ad640e682e9268ebaa82e549349069482e38e9baeacf3b85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vcenterNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90bf0d18e3336190ae63d9d61e38d026f6d00a11015986d8f2190f480654ed95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig",
    jsii_struct_bases=[],
    name_mapping={"ip_blocks": "ipBlocks"},
)
class GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig:
    def __init__(
        self,
        *,
        ip_blocks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param ip_blocks: ip_blocks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ip_blocks GoogleGkeonpremVmwareAdminCluster#ip_blocks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac8c11a6f8bb0d2e6cc386042d7e05d5b0f5b2fda4a765f1165773d4da6ea6e9)
            check_type(argname="argument ip_blocks", value=ip_blocks, expected_type=type_hints["ip_blocks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ip_blocks is not None:
            self._values["ip_blocks"] = ip_blocks

    @builtins.property
    def ip_blocks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks"]]]:
        '''ip_blocks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ip_blocks GoogleGkeonpremVmwareAdminCluster#ip_blocks}
        '''
        result = self._values.get("ip_blocks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks",
    jsii_struct_bases=[],
    name_mapping={"gateway": "gateway", "ips": "ips", "netmask": "netmask"},
)
class GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks:
    def __init__(
        self,
        *,
        gateway: builtins.str,
        ips: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps", typing.Dict[builtins.str, typing.Any]]]],
        netmask: builtins.str,
    ) -> None:
        '''
        :param gateway: The network gateway used by the VMware Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#gateway GoogleGkeonpremVmwareAdminCluster#gateway}
        :param ips: ips block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ips GoogleGkeonpremVmwareAdminCluster#ips}
        :param netmask: The netmask used by the VMware Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#netmask GoogleGkeonpremVmwareAdminCluster#netmask}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e52f6a17af40be2a22e8708b90d903382d4d8d280c54d95caeb7666a1c978a50)
            check_type(argname="argument gateway", value=gateway, expected_type=type_hints["gateway"])
            check_type(argname="argument ips", value=ips, expected_type=type_hints["ips"])
            check_type(argname="argument netmask", value=netmask, expected_type=type_hints["netmask"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gateway": gateway,
            "ips": ips,
            "netmask": netmask,
        }

    @builtins.property
    def gateway(self) -> builtins.str:
        '''The network gateway used by the VMware Admin Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#gateway GoogleGkeonpremVmwareAdminCluster#gateway}
        '''
        result = self._values.get("gateway")
        assert result is not None, "Required property 'gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ips(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps"]]:
        '''ips block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ips GoogleGkeonpremVmwareAdminCluster#ips}
        '''
        result = self._values.get("ips")
        assert result is not None, "Required property 'ips' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps"]], result)

    @builtins.property
    def netmask(self) -> builtins.str:
        '''The netmask used by the VMware Admin Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#netmask GoogleGkeonpremVmwareAdminCluster#netmask}
        '''
        result = self._values.get("netmask")
        assert result is not None, "Required property 'netmask' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps",
    jsii_struct_bases=[],
    name_mapping={"ip": "ip", "hostname": "hostname"},
)
class GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps:
    def __init__(
        self,
        *,
        ip: builtins.str,
        hostname: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip: IP could be an IP address (like 1.2.3.4) or a CIDR (like 1.2.3.0/24). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ip GoogleGkeonpremVmwareAdminCluster#ip}
        :param hostname: Hostname of the machine. VM's name will be used if this field is empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#hostname GoogleGkeonpremVmwareAdminCluster#hostname}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09571110b18a8de90682c286bf50b8e4316e6046453d1eb492774888fb8974cd)
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip": ip,
        }
        if hostname is not None:
            self._values["hostname"] = hostname

    @builtins.property
    def ip(self) -> builtins.str:
        '''IP could be an IP address (like 1.2.3.4) or a CIDR (like 1.2.3.0/24).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ip GoogleGkeonpremVmwareAdminCluster#ip}
        '''
        result = self._values.get("ip")
        assert result is not None, "Required property 'ip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''Hostname of the machine. VM's name will be used if this field is empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#hostname GoogleGkeonpremVmwareAdminCluster#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIpsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIpsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1edbdac4dd81a4a37241682b17e47012325b9fbb5cb022d77186293d079a2221)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIpsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3802902b54eee27fd3cd2d836d659c6b5a7ec6342ea7023d7a85011520b92130)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIpsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a0ee4bc40fb8c4579907042849a2fee401b436f283aaa5336e47949aa572216)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cebac142230cc72c4ccfd3f54c7fcb3a6a0c9d1e9584419e9daa6172521e919)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8b3a4870cfbf5497f6826fbadcdd906bf276ba5245ec0f110c1200a08e59b87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae51bba5eb73e42ca81da771112013f6c0dbdf35996dd95b3113c49767ef8872)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIpsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIpsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d5b7dcb057f4ce810b2fd8795e5adf03cd3c80bb431e8764c0c699ea6c512d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetHostname")
    def reset_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostname", []))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="ipInput")
    def ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipInput"))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2912c0379464aaf3116a60843b43b453bbe51fe4b5649da2def0a7f91878a4f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8db8749d7d9f6535d8a5f77c839196d88869e2f0f245e28a0eb006d5121bdfb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__132db781d612c1fae80b5f0f11365f830d9a286ad08268488a4b5c305bb0cbe9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c8770316069e9bba1fa7166373034f137b4b84ce670b0d53de925ec3be636c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25894c94d91c2db02bc052fed4d01010eba5de3195f6ffb8818d612eef711546)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7269719c08bfb8496cbd163f8150a09a4d3d36078a25b2cd431bce9500a63916)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d40b8e267fcc845539b3d3500c04217cb580aa18224f01c8f922a30cd2a3078)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7fbfa69315ec0990529b281847a15b8d4b4c7813a93ac4e508ae7a460c43384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0f4f7d1d6354888e8230c604fae9657cff3950a68ab6be392aae5d38c852036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c40676b6111c2346fcddf2e6e830673820cda296079bc358f2dba9246ce0b36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIps")
    def put_ips(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e66fc248c01c6f4b89978c0df42d044730384d28fad5b604943df3b7d78b64f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIps", [value]))

    @builtins.property
    @jsii.member(jsii_name="ips")
    def ips(
        self,
    ) -> GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIpsList:
        return typing.cast(GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIpsList, jsii.get(self, "ips"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="ipsInput")
    def ips_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps]]], jsii.get(self, "ipsInput"))

    @builtins.property
    @jsii.member(jsii_name="netmaskInput")
    def netmask_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "netmaskInput"))

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gateway"))

    @gateway.setter
    def gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a70038ce0c72045c1e855a3ebf9767a2c4604f6df5a8a20d0cff42401292cce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateway", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netmask")
    def netmask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netmask"))

    @netmask.setter
    def netmask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a50476a966578587f6b06ab1208cd34d9ce4a5e74687ad9521304472bdfdbff8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netmask", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2788dfa0b813f4a15f73db4b02ebc07f40cde1b14770f9c2c7cef7aae1f8c8d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__829332215ac45a52fb23149b54b16d943b482ecee0684b1ed1cce362185b0d3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIpBlocks")
    def put_ip_blocks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db5991df89d43e78c3b6505a2374bf2b68b8380e50ca1cc0c1f704a6153eecc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpBlocks", [value]))

    @jsii.member(jsii_name="resetIpBlocks")
    def reset_ip_blocks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpBlocks", []))

    @builtins.property
    @jsii.member(jsii_name="ipBlocks")
    def ip_blocks(
        self,
    ) -> GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksList:
        return typing.cast(GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksList, jsii.get(self, "ipBlocks"))

    @builtins.property
    @jsii.member(jsii_name="ipBlocksInput")
    def ip_blocks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks]]], jsii.get(self, "ipBlocksInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6723925e5d8127508392146f883932fd052d700ed2f47e35375c5ad25bea9688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterPlatformConfig",
    jsii_struct_bases=[],
    name_mapping={"required_platform_version": "requiredPlatformVersion"},
)
class GoogleGkeonpremVmwareAdminClusterPlatformConfig:
    def __init__(
        self,
        *,
        required_platform_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param required_platform_version: The required platform version e.g. 1.13.1. If the current platform version is lower than the target version, the platform version will be updated to the target version. If the target version is not installed in the platform (bundle versions), download the target version bundle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#required_platform_version GoogleGkeonpremVmwareAdminCluster#required_platform_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f52583dde948153ba6ddbdefe3ba4380d183ca8a018c86b261f41149d92d1179)
            check_type(argname="argument required_platform_version", value=required_platform_version, expected_type=type_hints["required_platform_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if required_platform_version is not None:
            self._values["required_platform_version"] = required_platform_version

    @builtins.property
    def required_platform_version(self) -> typing.Optional[builtins.str]:
        '''The required platform version e.g. 1.13.1. If the current platform version is lower than the target version, the platform version will be updated to the target version. If the target version is not installed in the platform (bundle versions), download the target version bundle.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#required_platform_version GoogleGkeonpremVmwareAdminCluster#required_platform_version}
        '''
        result = self._values.get("required_platform_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterPlatformConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterPlatformConfigBundles",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremVmwareAdminClusterPlatformConfigBundles:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterPlatformConfigBundles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d78d815186d4b291123244f0ba5b267a6f69d9990758fe919f60fb8bfcbb585)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c81e31fa280d528adf2dd9252c1498069db918b8d20d9765fd7c5782a2dbb70)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e44331cc4592c387f54efa708e172c1d5f85e0ac2947d61dd2c4e204b9a0b5b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c6c6e6557099ffc0951e51a71395516255a8524be769a14fa5a0190a86a2972)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f572f1a7423e9024e6fe94e048852013ce73116a7daa44588d86729f89bae919)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41a160fd82ebce769ae9daab1bbe8e05e65aa1c4afa13dbb62983917f37af20f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(
        self,
    ) -> "GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusList":
        return typing.cast("GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfigBundles]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfigBundles], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfigBundles],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e95e5ecb11892b37c0631e21abc64a7cb950f3e3f5123c572fba35c78c4ccd0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddc88ed8febfd639055d83e2cfd770d44bf1f458776bacf688324866d3a82e48)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8a021476164b470f84206ed4b57fb1501c1e48ecaed055ebd06661f0416a844)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42723048bd1c07ef162b12287470d087ccd42bf9caa0b2fa7ad80ed6c13538c3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c3b90bd243df73e834aa6c09cb37c1e2725b1810518572263c753fb1486663b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d221db8b040d1b2bb31fef653285e46eab1ba39e6894273f8fd70f41d5fbd66b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f1052fe3b01c581113d565cdd0c2920bb1a1a57dc7654a7ef258604437986f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="lastTransitionTime")
    def last_transition_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastTransitionTime"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="reason")
    def reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reason"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditions]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01996d73f29ba251be7c17da21c31a985d784dd682e72f6eed2802d6a782ce5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__58152858f75f7d2229b126fddc56749ca8f97b011bcb21a0c01c84b586984a1c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f9a722782582ae4c3383f4aa04e642a4e33aa1c23e3502bb6609613716dd91)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a783093b383d64a5ea34a3848b803026645a6c0156e2808122a89a2b486800e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d42dce080de68b61fdf50d95b33b76f157946990b7d5e5282fa018ce80a4f0d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85f566eed680e0fc16888ecc30f90e94e76f4d6c826aa9ab4a8031bb754f0c86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__417d40d632d18dd6e4941cd4b64a6aa827eb34c9e82b235912040257e08a1592)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(
        self,
    ) -> GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditionsList:
        return typing.cast(GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatus]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51540231fa9487a1ba41c840c88d6a31066a7b39193ecaf8faea322548e4a10f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareAdminClusterPlatformConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterPlatformConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7af400205682ea7635ff92e62106bfa8c927c57723a43a8825a1ab5dee80894a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRequiredPlatformVersion")
    def reset_required_platform_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredPlatformVersion", []))

    @builtins.property
    @jsii.member(jsii_name="bundles")
    def bundles(self) -> GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesList:
        return typing.cast(GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesList, jsii.get(self, "bundles"))

    @builtins.property
    @jsii.member(jsii_name="platformVersion")
    def platform_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platformVersion"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusList":
        return typing.cast("GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="requiredPlatformVersionInput")
    def required_platform_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requiredPlatformVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredPlatformVersion")
    def required_platform_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requiredPlatformVersion"))

    @required_platform_version.setter
    def required_platform_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5962adbb8d7a95ec901b3193d93cdcd4a52a93c60c2b4d2ec2071a7a775f7b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requiredPlatformVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6c5af02bfb6a8ee492c64c911dbdaca6b3686de5ad4029298f46b8e36995a5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterPlatformConfigStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremVmwareAdminClusterPlatformConfigStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterPlatformConfigStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusConditions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusConditions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2f2b45bec8f321e321cd9209cd4b3ca00d0f23970ff0295d757b9f9ed43d84b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f5b2b7400ffec7704d82795e42e5ea144aa0b997b06d736ca7cf218099fd0be)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e32c2640fc02c847b149dcca7acf3aba91f39ff7db6474b7793c4994432620)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d99c36ca9726d942ddf9d418c819d9811e9f0fbc7f2b490301ec6396245480de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__41d83fea1ae6ac0a5cc1ec2adf84174714428e8b72e1ee44b40745c5278978ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__460e30fc1f1fba459f381f3b01f93273396b6d0956d1809846a2547e9d1491e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="lastTransitionTime")
    def last_transition_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastTransitionTime"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="reason")
    def reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reason"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusConditions]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9cfff92aeccf75cb773e1830f9cfbfc5a0cd4d4bee7f70173b03ced3894e167)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6150060539fda63c7407c2c7ce43dc0be6ccc7cd74900ee093cf89c82e07dbc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b38161cba6fc6b0d006a5b5e45d68b26b76282281c5068fda8b8f5836977a2c3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93f682f88a7af63fe079ff5f8106c45f5561b5fd3475b365febe4502a7bffc79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b70f633ab9e9201d1ab190dac0b799b5ff0739be8f8fe265dcafd47d2cc0b4e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5501c5abc30cc28c9eeb5e5666006568401f177310568907bf14656ec30bf308)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__beb6cbbf33a9b46ac6c2103f4a1163780d142fa41f2201b8a0726628075b4061)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(
        self,
    ) -> GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusConditionsList:
        return typing.cast(GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfigStatus]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfigStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfigStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad6e24deff614bb35953225e17a0c4d3669ddbbcdda5b2317bd0f574444aec6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterPrivateRegistryConfig",
    jsii_struct_bases=[],
    name_mapping={"address": "address", "ca_cert": "caCert"},
)
class GoogleGkeonpremVmwareAdminClusterPrivateRegistryConfig:
    def __init__(
        self,
        *,
        address: typing.Optional[builtins.str] = None,
        ca_cert: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: The registry address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#address GoogleGkeonpremVmwareAdminCluster#address}
        :param ca_cert: The CA certificate public key for private registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ca_cert GoogleGkeonpremVmwareAdminCluster#ca_cert}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__230753e315e10e54dbd6558d987f28b0ca0195575d49b80df744a1fb547c4ac2)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument ca_cert", value=ca_cert, expected_type=type_hints["ca_cert"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address is not None:
            self._values["address"] = address
        if ca_cert is not None:
            self._values["ca_cert"] = ca_cert

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''The registry address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#address GoogleGkeonpremVmwareAdminCluster#address}
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ca_cert(self) -> typing.Optional[builtins.str]:
        '''The CA certificate public key for private registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ca_cert GoogleGkeonpremVmwareAdminCluster#ca_cert}
        '''
        result = self._values.get("ca_cert")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterPrivateRegistryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareAdminClusterPrivateRegistryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterPrivateRegistryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cc7d21ece891a44c598eec81b88f46e0ca7eb20a54423361438f258638354cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @jsii.member(jsii_name="resetCaCert")
    def reset_ca_cert(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaCert", []))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="caCertInput")
    def ca_cert_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caCertInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1ddaf448adcd906c8f8bc00879d694e63564c3d3889fe2a2117e291a2e19dba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="caCert")
    def ca_cert(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caCert"))

    @ca_cert.setter
    def ca_cert(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6941c87637e7ec75f305c83b717aee55c1d8d50efd33f4b28a0f3dbd784c163a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caCert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterPrivateRegistryConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterPrivateRegistryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterPrivateRegistryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aee9c00ed34fdc975beb8a27a841a667084ac7ea24b787867e641f9c39b32cdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremVmwareAdminClusterStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterStatusConditions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremVmwareAdminClusterStatusConditions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterStatusConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareAdminClusterStatusConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterStatusConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb356359f0138262f9a8ed3fe80c7bef6f73d4fb179d10abfe1d246cf9e605fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareAdminClusterStatusConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d54dd9ac42390212095c4e05e4da2eff41eb592378fd1126bafd164bb0cedb9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareAdminClusterStatusConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7d6ad319e87f40adf649ba46cc4ef79211b533fb68e81e964160b2dc7e8bb1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ca092bdd7adf1f629de526cae1f8a4c75026dcd761e6ceaf153c9db78f78d6d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__898a9f0b9e85664abe2c8dcebeb3d48890b8eb15db8c45a0436fcc4d0ada9528)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareAdminClusterStatusConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterStatusConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__764eeff1853f17bf7b002715fe3161f1c64d84c20cb87c6753661b77d340ab1b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="lastTransitionTime")
    def last_transition_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastTransitionTime"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="reason")
    def reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reason"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterStatusConditions]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterStatusConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterStatusConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__799a56e86d3687f4b743e264327d79403c97122b009af818aaf35990baa24aa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareAdminClusterStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd47801cb5c3f9b5b6ad8aec9ec2ddb7caec69d328e42328191d2d2d5be428f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareAdminClusterStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54e5c0fa18c54dd1623762a901634677cd5980ac13783c276d078ea5c35008b3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareAdminClusterStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63fc4816b9198ce934837843c4d7d1225bc05608af20b3fd8a34d5ac19e36d0e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__836f4898367780e21f4db73e5689e2cac56c629048e3d1cd78f342f711f6f42c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19640c08fcb9c69a62cc9907c926442ba65fc413cbf3e13e760a556ffa25fd45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareAdminClusterStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d929be67bf43588ae302d064bad23ca400e5b248e6ed870e1fccdb35713de94f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> GoogleGkeonpremVmwareAdminClusterStatusConditionsList:
        return typing.cast(GoogleGkeonpremVmwareAdminClusterStatusConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterStatus]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d917d41d1738a50a9f98f9f1594ad3e9f816ceab06cc3a4a5add52dfd2ae117d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleGkeonpremVmwareAdminClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#create GoogleGkeonpremVmwareAdminCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#delete GoogleGkeonpremVmwareAdminCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#update GoogleGkeonpremVmwareAdminCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f28238de09019ca7a020ab55c689fb354993dcaab87cb269bb9865a7e6b70ff)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#create GoogleGkeonpremVmwareAdminCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#delete GoogleGkeonpremVmwareAdminCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#update GoogleGkeonpremVmwareAdminCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareAdminClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06042b021c636479c78c7256980206d228a7312cc8ffdd68500e07073e7187d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9d09d2850d59b5fa8c9582b0c207ab3304ff1a6a33077a0efd4da7b1fadcf20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3152389d554ae433e3a5eafff12a8a5fa4e352752ee33ecf44a6c2df090b93f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76f342c8855d13a782f0ee495125eca3d9bcdc5f188bfec14ddff05c64bf6aaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareAdminClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareAdminClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareAdminClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a77d115c935bfcb07a78c9d5a44b4a92c66a85c9ba994fe59c09008a7a9ec98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterVcenter",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "ca_cert_data": "caCertData",
        "cluster": "cluster",
        "datacenter": "datacenter",
        "data_disk": "dataDisk",
        "datastore": "datastore",
        "folder": "folder",
        "resource_pool": "resourcePool",
        "storage_policy_name": "storagePolicyName",
    },
)
class GoogleGkeonpremVmwareAdminClusterVcenter:
    def __init__(
        self,
        *,
        address: typing.Optional[builtins.str] = None,
        ca_cert_data: typing.Optional[builtins.str] = None,
        cluster: typing.Optional[builtins.str] = None,
        datacenter: typing.Optional[builtins.str] = None,
        data_disk: typing.Optional[builtins.str] = None,
        datastore: typing.Optional[builtins.str] = None,
        folder: typing.Optional[builtins.str] = None,
        resource_pool: typing.Optional[builtins.str] = None,
        storage_policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: The vCenter IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#address GoogleGkeonpremVmwareAdminCluster#address}
        :param ca_cert_data: Contains the vCenter CA certificate public key for SSL verification. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ca_cert_data GoogleGkeonpremVmwareAdminCluster#ca_cert_data}
        :param cluster: The name of the vCenter cluster for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#cluster GoogleGkeonpremVmwareAdminCluster#cluster}
        :param datacenter: The name of the vCenter datacenter for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#datacenter GoogleGkeonpremVmwareAdminCluster#datacenter}
        :param data_disk: The name of the virtual machine disk (VMDK) for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#data_disk GoogleGkeonpremVmwareAdminCluster#data_disk}
        :param datastore: The name of the vCenter datastore for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#datastore GoogleGkeonpremVmwareAdminCluster#datastore}
        :param folder: The name of the vCenter folder for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#folder GoogleGkeonpremVmwareAdminCluster#folder}
        :param resource_pool: The name of the vCenter resource pool for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#resource_pool GoogleGkeonpremVmwareAdminCluster#resource_pool}
        :param storage_policy_name: The name of the vCenter storage policy for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#storage_policy_name GoogleGkeonpremVmwareAdminCluster#storage_policy_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eea491353290c2b77c5d7d11a295ec57982b785d227570a541332c3098d29b2d)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument ca_cert_data", value=ca_cert_data, expected_type=type_hints["ca_cert_data"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument datacenter", value=datacenter, expected_type=type_hints["datacenter"])
            check_type(argname="argument data_disk", value=data_disk, expected_type=type_hints["data_disk"])
            check_type(argname="argument datastore", value=datastore, expected_type=type_hints["datastore"])
            check_type(argname="argument folder", value=folder, expected_type=type_hints["folder"])
            check_type(argname="argument resource_pool", value=resource_pool, expected_type=type_hints["resource_pool"])
            check_type(argname="argument storage_policy_name", value=storage_policy_name, expected_type=type_hints["storage_policy_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address is not None:
            self._values["address"] = address
        if ca_cert_data is not None:
            self._values["ca_cert_data"] = ca_cert_data
        if cluster is not None:
            self._values["cluster"] = cluster
        if datacenter is not None:
            self._values["datacenter"] = datacenter
        if data_disk is not None:
            self._values["data_disk"] = data_disk
        if datastore is not None:
            self._values["datastore"] = datastore
        if folder is not None:
            self._values["folder"] = folder
        if resource_pool is not None:
            self._values["resource_pool"] = resource_pool
        if storage_policy_name is not None:
            self._values["storage_policy_name"] = storage_policy_name

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''The vCenter IP address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#address GoogleGkeonpremVmwareAdminCluster#address}
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ca_cert_data(self) -> typing.Optional[builtins.str]:
        '''Contains the vCenter CA certificate public key for SSL verification.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#ca_cert_data GoogleGkeonpremVmwareAdminCluster#ca_cert_data}
        '''
        result = self._values.get("ca_cert_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter cluster for the admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#cluster GoogleGkeonpremVmwareAdminCluster#cluster}
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datacenter(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter datacenter for the admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#datacenter GoogleGkeonpremVmwareAdminCluster#datacenter}
        '''
        result = self._values.get("datacenter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_disk(self) -> typing.Optional[builtins.str]:
        '''The name of the virtual machine disk (VMDK) for the admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#data_disk GoogleGkeonpremVmwareAdminCluster#data_disk}
        '''
        result = self._values.get("data_disk")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datastore(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter datastore for the admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#datastore GoogleGkeonpremVmwareAdminCluster#datastore}
        '''
        result = self._values.get("datastore")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def folder(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter folder for the admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#folder GoogleGkeonpremVmwareAdminCluster#folder}
        '''
        result = self._values.get("folder")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_pool(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter resource pool for the admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#resource_pool GoogleGkeonpremVmwareAdminCluster#resource_pool}
        '''
        result = self._values.get("resource_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_policy_name(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter storage policy for the user cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_admin_cluster#storage_policy_name GoogleGkeonpremVmwareAdminCluster#storage_policy_name}
        '''
        result = self._values.get("storage_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareAdminClusterVcenter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareAdminClusterVcenterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareAdminCluster.GoogleGkeonpremVmwareAdminClusterVcenterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e46e272da6bc7622cefe491b5736d2003b9b6530213ca4aefca0f7c463c1a447)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @jsii.member(jsii_name="resetCaCertData")
    def reset_ca_cert_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaCertData", []))

    @jsii.member(jsii_name="resetCluster")
    def reset_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCluster", []))

    @jsii.member(jsii_name="resetDatacenter")
    def reset_datacenter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatacenter", []))

    @jsii.member(jsii_name="resetDataDisk")
    def reset_data_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataDisk", []))

    @jsii.member(jsii_name="resetDatastore")
    def reset_datastore(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatastore", []))

    @jsii.member(jsii_name="resetFolder")
    def reset_folder(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFolder", []))

    @jsii.member(jsii_name="resetResourcePool")
    def reset_resource_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourcePool", []))

    @jsii.member(jsii_name="resetStoragePolicyName")
    def reset_storage_policy_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStoragePolicyName", []))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="caCertDataInput")
    def ca_cert_data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caCertDataInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterInput")
    def cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterInput"))

    @builtins.property
    @jsii.member(jsii_name="datacenterInput")
    def datacenter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datacenterInput"))

    @builtins.property
    @jsii.member(jsii_name="dataDiskInput")
    def data_disk_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="datastoreInput")
    def datastore_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datastoreInput"))

    @builtins.property
    @jsii.member(jsii_name="folderInput")
    def folder_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "folderInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcePoolInput")
    def resource_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourcePoolInput"))

    @builtins.property
    @jsii.member(jsii_name="storagePolicyNameInput")
    def storage_policy_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storagePolicyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__317f9af974112f4acc4ce6b8968f37d78889ce54d330b767b6e93fc6108f4077)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="caCertData")
    def ca_cert_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caCertData"))

    @ca_cert_data.setter
    def ca_cert_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7534338abf3bfc8f187477d6daa84777df38fb43c29acc65f429e84fbd04219)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caCertData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9af23e87117ea9e0cebb32da792ef198a124fdb20342c01619e959fe22996205)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="datacenter")
    def datacenter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datacenter"))

    @datacenter.setter
    def datacenter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3aefe7841a50d5ef9aa38aed505c59c104c2319288b215626ab3a39dd4da4f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datacenter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataDisk")
    def data_disk(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataDisk"))

    @data_disk.setter
    def data_disk(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c756b2dbf9097a00e0c27a26cdfe9aed913b596727dcaf01f7dbf08168fad3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataDisk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="datastore")
    def datastore(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datastore"))

    @datastore.setter
    def datastore(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__937f8d347b86581ccf2790e4be83c34fe2796c834a4fe3b562712c148b73441a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datastore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="folder")
    def folder(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "folder"))

    @folder.setter
    def folder(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa0ebeae65aac40326c35553e33d3af5cafb89c46ea634db42347751d3d3fea5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "folder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourcePool")
    def resource_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourcePool"))

    @resource_pool.setter
    def resource_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afd26e747bfa0cf7457efee1a43cbe9ac30299e365b4ee3de14275342a4f6089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storagePolicyName")
    def storage_policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storagePolicyName"))

    @storage_policy_name.setter
    def storage_policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3119764a1f52880723799120ef9caf6794a2bb263e0ab80eb20a132701916fdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storagePolicyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareAdminClusterVcenter]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareAdminClusterVcenter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareAdminClusterVcenter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df4efe9361a5804313d313180e1ecfffb109511feef2088e075c105681f83f6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleGkeonpremVmwareAdminCluster",
    "GoogleGkeonpremVmwareAdminClusterAddonNode",
    "GoogleGkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig",
    "GoogleGkeonpremVmwareAdminClusterAddonNodeAutoResizeConfigOutputReference",
    "GoogleGkeonpremVmwareAdminClusterAddonNodeOutputReference",
    "GoogleGkeonpremVmwareAdminClusterAntiAffinityGroups",
    "GoogleGkeonpremVmwareAdminClusterAntiAffinityGroupsOutputReference",
    "GoogleGkeonpremVmwareAdminClusterAuthorization",
    "GoogleGkeonpremVmwareAdminClusterAuthorizationOutputReference",
    "GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsers",
    "GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsersList",
    "GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsersOutputReference",
    "GoogleGkeonpremVmwareAdminClusterAutoRepairConfig",
    "GoogleGkeonpremVmwareAdminClusterAutoRepairConfigOutputReference",
    "GoogleGkeonpremVmwareAdminClusterConfig",
    "GoogleGkeonpremVmwareAdminClusterControlPlaneNode",
    "GoogleGkeonpremVmwareAdminClusterControlPlaneNodeOutputReference",
    "GoogleGkeonpremVmwareAdminClusterFleet",
    "GoogleGkeonpremVmwareAdminClusterFleetList",
    "GoogleGkeonpremVmwareAdminClusterFleetOutputReference",
    "GoogleGkeonpremVmwareAdminClusterLoadBalancer",
    "GoogleGkeonpremVmwareAdminClusterLoadBalancerF5Config",
    "GoogleGkeonpremVmwareAdminClusterLoadBalancerF5ConfigOutputReference",
    "GoogleGkeonpremVmwareAdminClusterLoadBalancerManualLbConfig",
    "GoogleGkeonpremVmwareAdminClusterLoadBalancerManualLbConfigOutputReference",
    "GoogleGkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig",
    "GoogleGkeonpremVmwareAdminClusterLoadBalancerMetalLbConfigOutputReference",
    "GoogleGkeonpremVmwareAdminClusterLoadBalancerOutputReference",
    "GoogleGkeonpremVmwareAdminClusterLoadBalancerVipConfig",
    "GoogleGkeonpremVmwareAdminClusterLoadBalancerVipConfigOutputReference",
    "GoogleGkeonpremVmwareAdminClusterNetworkConfig",
    "GoogleGkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig",
    "GoogleGkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfigOutputReference",
    "GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig",
    "GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock",
    "GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps",
    "GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIpsList",
    "GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIpsOutputReference",
    "GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockOutputReference",
    "GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigOutputReference",
    "GoogleGkeonpremVmwareAdminClusterNetworkConfigHostConfig",
    "GoogleGkeonpremVmwareAdminClusterNetworkConfigHostConfigOutputReference",
    "GoogleGkeonpremVmwareAdminClusterNetworkConfigOutputReference",
    "GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig",
    "GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks",
    "GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps",
    "GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIpsList",
    "GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIpsOutputReference",
    "GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksList",
    "GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksOutputReference",
    "GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigOutputReference",
    "GoogleGkeonpremVmwareAdminClusterPlatformConfig",
    "GoogleGkeonpremVmwareAdminClusterPlatformConfigBundles",
    "GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesList",
    "GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesOutputReference",
    "GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatus",
    "GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditions",
    "GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditionsList",
    "GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditionsOutputReference",
    "GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusList",
    "GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusOutputReference",
    "GoogleGkeonpremVmwareAdminClusterPlatformConfigOutputReference",
    "GoogleGkeonpremVmwareAdminClusterPlatformConfigStatus",
    "GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusConditions",
    "GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusConditionsList",
    "GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusConditionsOutputReference",
    "GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusList",
    "GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusOutputReference",
    "GoogleGkeonpremVmwareAdminClusterPrivateRegistryConfig",
    "GoogleGkeonpremVmwareAdminClusterPrivateRegistryConfigOutputReference",
    "GoogleGkeonpremVmwareAdminClusterStatus",
    "GoogleGkeonpremVmwareAdminClusterStatusConditions",
    "GoogleGkeonpremVmwareAdminClusterStatusConditionsList",
    "GoogleGkeonpremVmwareAdminClusterStatusConditionsOutputReference",
    "GoogleGkeonpremVmwareAdminClusterStatusList",
    "GoogleGkeonpremVmwareAdminClusterStatusOutputReference",
    "GoogleGkeonpremVmwareAdminClusterTimeouts",
    "GoogleGkeonpremVmwareAdminClusterTimeoutsOutputReference",
    "GoogleGkeonpremVmwareAdminClusterVcenter",
    "GoogleGkeonpremVmwareAdminClusterVcenterOutputReference",
]

publication.publish()

def _typecheckingstub__56da4fc7adbb210da0bfccebe4181d1526c1d9cc61269dc916d33b676a4dc09d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    network_config: typing.Union[GoogleGkeonpremVmwareAdminClusterNetworkConfig, typing.Dict[builtins.str, typing.Any]],
    addon_node: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterAddonNode, typing.Dict[builtins.str, typing.Any]]] = None,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    anti_affinity_groups: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterAntiAffinityGroups, typing.Dict[builtins.str, typing.Any]]] = None,
    authorization: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_repair_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterAutoRepairConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    bootstrap_cluster_membership: typing.Optional[builtins.str] = None,
    control_plane_node: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterControlPlaneNode, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    image_type: typing.Optional[builtins.str] = None,
    load_balancer: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterLoadBalancer, typing.Dict[builtins.str, typing.Any]]] = None,
    on_prem_version: typing.Optional[builtins.str] = None,
    platform_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterPlatformConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    private_registry_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterPrivateRegistryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vcenter: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterVcenter, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c67ed89b4c0052c981f9534e3e8b7df0a62af8d562c9ec996161e2a5ae186a0c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17990b576eb7072b2cf85dd542c37d8cb9439d62c760f114e26e2c405090fbbe(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a51989798254dd83b53236de92fc611a2b3162f3826b44a7762cc99a6140a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df3726f56fab387b9ee9219c2adf46b93699669dc80c3bc143535890a022aed2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363f31f0cfdf1b5941ded9dbfd634fac089d93950cf9e72fe82062f3f6aba294(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e6ba905fda0b6979b96bfa6657adf206835443e4be7b24fd0da7736476f9417(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__576b4f176a10df65f97b7e60717f225cf3a6911b5d342b95fa7a7801daec4261(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa27090977481a75165086daf6446a1addda66b97f50cf9549b6fd1fd5a2d3f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd59fa4136dde4280ba47cf8ffd3f51ec50a6d59bb24e2fb90dff00cf7df70ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a2a9c470cf561126a8fb8e7abb4af44a143f55a6a0c8b3548216ad8770e8ab0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a8a4769689fe0913314fd6804392f6a38ed8a48257da95e40a71270042d22b(
    *,
    auto_resize_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9147e4692f85c5677a9cbf2f033b3ee4e8caf052f277e139b627a8b69e45fd1a(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0613c69af2fe68b4ce73de9842bf4147e45960784ff1a9ff8ba623a14c86acb7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d5067ad7743a1ee5870382a6df7a3f31788cd1bf7dd246f65fb3fd69e0dd615(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cabbb96aa949e1262a4ae73142faa31c6b34dcf99ef8d6aa4f365ea6c25441d2(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02a5a9ce311d6692c60ea442698e0a83169878979366bd9987e05ded10f9d983(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f04225db66b108b4840b1a48825927b06e7b95a27eedbcf6b7a85994caad7e0(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterAddonNode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e1a2d69c9d9b242c72f9853bd738c45063a24dd7ab1a05565f583bf706e0d3(
    *,
    aag_config_disabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54db0578a651ac2b9e12d9959ffc2b25cf1b0ba05badcce32f3b98d299702c53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76927fde0308ea5ffbac1538200dd39efe840c43352db66b60a2d2c720a291ab(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b78ecd7e7dc45f20164a5adb37dac13dba9db954929e35d65686e2cc91161de(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterAntiAffinityGroups],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab9260766fcb0626dbdd4281e97327f70f7ac372361471b5894390e09c14190a(
    *,
    viewer_users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsers, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d91343c5a239b481e36d18415ed435014cafd57252554d3ad104bfdb35a2711(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e3d31aab97031ecb1001ca905e6db1b648ea19f18ba0198e6e4cc0cffaf08b9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d371a9ae6a0907ed6b889f6c2737e3fd5e2fcc17088f974b5f6fc954f12e3dc9(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d35e4087ab809aa9a5dcb72e0fc67aad3b5f65e7b3e8dd3c1dbe3453feb3fcc0(
    *,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de8bd93591be7b81f0498e2559748429f60ce96ca371cdcd741ae8ab7aea4933(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39977bafd427732e85cfb1ebc088a3c13b2cac6b84ebcb9eaed0751da617a9b2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bfab0ebb3b07b7c871d2b3d3089f96b98df0015f2d95b2071d9465e0a874982(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19fc197404dfc9c8112ba0c1ca1000316238279f2c9f9364a2292589bf408726(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__840403f3237c1e1e43ca3f0ef35efef343c90bb49c77dab71a6fa4ed3d1b2fbd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca7872e942899c35923295e8f77889c55c6b2b3b76eae885d238c206e03c5e09(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe3abef4db384e8fe832e2b0631a208c24816b511ecd346dabf0648377b61ea7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea729fe300793012c45e53e6ea3dfc036868ff47da1f3adca3e24fc48b5120d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adb4d595fc0a4610e37f032a908952de1964b7b7308a4cb86348f297bff65b78(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareAdminClusterAuthorizationViewerUsers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d02b4f8ef13970359c7daae7f81490cd4447b129aa5fc5489ad7580aefdf7f30(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__340e5bc2eff24653f89ea9f8fd23a049d44c9a044630463dba586eb7ef31d964(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c3db74048fb05c3a0bf66e8c2d9d7c449ea479a1e5690048eabed73c79fdae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__696fded15667c5c95b9775e412708c91a541af6aed97544c9a97cd7eed33eabd(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterAutoRepairConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf6b4297ef3d2690ab700af6228b56e821b643e4fc1bbceb4092d58d1b0d16d3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    network_config: typing.Union[GoogleGkeonpremVmwareAdminClusterNetworkConfig, typing.Dict[builtins.str, typing.Any]],
    addon_node: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterAddonNode, typing.Dict[builtins.str, typing.Any]]] = None,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    anti_affinity_groups: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterAntiAffinityGroups, typing.Dict[builtins.str, typing.Any]]] = None,
    authorization: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_repair_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterAutoRepairConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    bootstrap_cluster_membership: typing.Optional[builtins.str] = None,
    control_plane_node: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterControlPlaneNode, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    image_type: typing.Optional[builtins.str] = None,
    load_balancer: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterLoadBalancer, typing.Dict[builtins.str, typing.Any]]] = None,
    on_prem_version: typing.Optional[builtins.str] = None,
    platform_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterPlatformConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    private_registry_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterPrivateRegistryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vcenter: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterVcenter, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a066765a7dd1e91e4f13d609752858bb680e49003435002cffc75a71dcb5e0e(
    *,
    cpus: typing.Optional[jsii.Number] = None,
    memory: typing.Optional[jsii.Number] = None,
    replicas: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c018cb71498b5d3eb9abd98655ebce3b6ecc444eef35a28a7268ad17992c3ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1251e2dc34a47235d99477efce2f82efd5b0f7c258c0525cbd8fe187baa39e07(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf4a5fba657cb37623604829b6eab5239c83262f8de17bd00cf1698a05028047(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7a68810fe0d441411eaee2e4c23b0496c20d29a41bbbd907d8df2b9464893b2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68718bdb8e5f5ac031f84648469fe29662d53910f129d9bf07738c6c3e724097(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterControlPlaneNode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fbac2934875da50ab45bdb024da99fdecddb1b1800e7d3ef74d4a55410c1c4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0922395cae1b6db58b03d812f4d618092c2a3017d5bd369de0f31d62da411f4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ae05db6e81b58eba0ed555a390acf76e5ca5b265f38a88f402eb94d2e50b3e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dea96367651447f7ef9991c3dcdb309ca2873e4732cf396f642e3adf01604f4c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97217e8bac2a9c3840495f12efed1204fd4c43b9533c657985e4a0b10430565c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e0dd195e62fd72423f9e5ee2c22f94c069efda84f081df4a656783e6a762ec0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcea13f72a2a5ff633c52b0d11cebf661460fc3df491c59a1c18f2cfc8241503(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterFleet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88be2923c9265313598e87918ab15aedbb3a63b072c7d0763663e6f1629d3b7e(
    *,
    vip_config: typing.Union[GoogleGkeonpremVmwareAdminClusterLoadBalancerVipConfig, typing.Dict[builtins.str, typing.Any]],
    f5_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterLoadBalancerF5Config, typing.Dict[builtins.str, typing.Any]]] = None,
    manual_lb_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterLoadBalancerManualLbConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    metal_lb_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72a84a9659d9a6aa838c7981cecc8a99803b2a1e7010e82de4bf9d1fecfd72d7(
    *,
    address: typing.Optional[builtins.str] = None,
    partition: typing.Optional[builtins.str] = None,
    snat_pool: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f815aedc3d69caafc2734533cc0db838477f4a566ff86d50355c401018d3317(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbc9db69b94c0a19be0ef89fd2675b480a5c3a761511e2687765679a325d4b7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3e550c486359a1f3d7976675b2c95c2ec3c1013fe5ce0ef0700186edb63befc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d661791ebc07d7d69595ee270e0509e53dab6449d490c0e97c39e83d115af116(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631ccac68e79bd61f1c7f83cc3317befd99cfbe6624d0233252f0b56af335429(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancerF5Config],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e80377f93f5d03975e63a98fb8780f7f9d3ff14e6d024f623d6d9aef03543925(
    *,
    addons_node_port: typing.Optional[jsii.Number] = None,
    control_plane_node_port: typing.Optional[jsii.Number] = None,
    ingress_http_node_port: typing.Optional[jsii.Number] = None,
    ingress_https_node_port: typing.Optional[jsii.Number] = None,
    konnectivity_server_node_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7daf3a255fca4e1635c00c0e247b7926c3acb58c1f4f1b07416c2b4ac2b2e17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07cd5bfaaf27d157d3075cb08b4abece176faa7e236abdddf95f1dbeff935200(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faaf42e8eb25f67c89a2c81a5979b4da3d2b43c406331716a3666100132183ef(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56692e2fe6d744b48f6ab2a58c7c355e88608c713d71b610de21a6c909a596a9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad58b01fedc33c2df7eb70fbf1a25574410ee6740552152046f1efa5a4f4896a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c972a9daa4b1688c98cab9a31a9aac3ccf0adcebee3c4a8a4103788425c60cf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__061cabeb365485c208be3af9503599d849f4edfb0311716c79aec99c5e37e8bd(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancerManualLbConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c5638e864531b37659840e7d38b15e75c3a0608231e321256400b1ca23e0e60(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a998a78432ab52dedd4f088b3c4823f2b862fc17a654d5f473ad3ab7bc0c5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73e7542a423dc36dcf96345535630a53e9870fae8b7713e3d4f6281913cf0aa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d161cfcd596f5a7f95c25e0cfab0884c5c090aeb63ee33c15ce42eeaa650db19(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__768fc07f6d032b6f00919f1772f274052a2acf5ccfc6c47362b6c0eac5e6f7b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7029f1bf50faeb5e5b57fe17e419f0e416793499dfd55ec2b21ed0a3bbe4d526(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96a202040fe549f3c97343565cd86cd82300afeaa983f0c9d3ad56915dbcd16f(
    *,
    control_plane_vip: builtins.str,
    addons_vip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dba20c9a891a3896e6a1be400cb9e46eabb56e4dfa3009be2de4d0d2b9bda3d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b784f760ae7cbd46f1d42940150f8b714d0338c6f5c5beefd197a0b7212d2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b260b22bcaa7e0b996bc1aca8a92f6466b6a58276d1f091cbb1cfd5ab3980ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e56f731b857af5408217cbd96dd96929beb15c345918d711bcfeb05b23657c2(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterLoadBalancerVipConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__167e56c2c4e1d96f0c3f8919a9db31e640c2292fdde0fb8e2bb0c0ee1bf268d0(
    *,
    pod_address_cidr_blocks: typing.Sequence[builtins.str],
    service_address_cidr_blocks: typing.Sequence[builtins.str],
    dhcp_ip_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ha_control_plane_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    host_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterNetworkConfigHostConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    static_ip_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    vcenter_network: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0806230e801e56ee5dc27372bd451e45118b5b905b148f807415e43842e966df(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc4c3243f0831b1b44123aa700e02de09c7205eba6b437336d6147e333d77a16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73b95f223d0b30523dde0655ba77db49cd42d4955b31831af313e89f635963cc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6457c9f3536519c232d84e290ed617ca67b4ddbf7c7ffd6ec2b1cb4f385994f2(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__814e633bfa5ff00faeea1e79c41308c8e6c14ac3ac6959a401636f51cec38e58(
    *,
    control_plane_ip_block: typing.Optional[typing.Union[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff4b718db0c0d911ee23d8f4e12c27feb6e5c57f6dd63f3f0d70babda8a20939(
    *,
    gateway: builtins.str,
    ips: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps, typing.Dict[builtins.str, typing.Any]]]],
    netmask: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__834edbe1f8dc81e826f43e6cbfd6c81aabeffb5ae8f3590aa15b1324fd4e5760(
    *,
    ip: builtins.str,
    hostname: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25b63e539f94dfb3231b28d5dd4378d90d3630d8003ddf77e81baed95a86931(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c762511b2ee9368a8a6876c232e077261ba03a88cd3cfd3516cd676ea132c39a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c104aeea8323ba34f31a174fadace8bd13468b8e715a3883b51e85d314404e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6e9408c7b25bb10d92b679f356374e1f553b68287dd8369b441b7e159efe58(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3a5321b3a9684323e22705136368e6e0248e29320688ef7f70f1e8faa94909e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6833303c76a79712159c375fe0fd7a3bf22ee3860d679bf72bb235a028539f9c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248c0c809e86a346a66b50966371af64246cdbd054a2c242efc98e2bacadf1e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__546ee89c0230667c570db4702bf1d1d12d32cc4bb79a17a666aa143f88ee589e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc4846ee1cd5661ccc57869f4a242dd99f850bd44dd9089ff8951b40eb6fd85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7579556172043b0c8b6253c7b87479eefa6999e30b17fe35c8884a2dc324fc8d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__025d947d071e935cb9251efd029c69f171802bc4e422b8f976d7ab5a2e92c9c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcfe5bf48a116160b63ae27f32c4221b6ebbe1682ab7ed380ce583b04fb27dbf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__444e377f5401ed6872f2ba51344d636e209e53843c051625c637e8fbfd03656c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__961c44965232180aa657f618d07c806e06d73333bceab5c591a03932fd391a54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ded06549e2113f545659d9221f09c65a7a1e97c0c4ce71dae1d85041d3179f2e(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b9b23fd3beafb3f92c5ff2d2a22fcb1bbda27c8330a4e3cf6c2ac1ef6aa710(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc352383c3139dd1f7c00970edbc0928529c1f1c7c5725238648554078981911(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65906c3c0e8fe5135afb766e5bc40a23c8444c8f9839059a756f5f943514e9ec(
    *,
    dns_search_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ntp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8acb07facba350797db310dd3c24232d3114d890f6839433584336dcd4916be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be979a7198cdac0c31cb2cc652c6316cd1b14728c233bb838a5b0751a206b19(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a1f586fbfca5ec7dd96131a9e579678d86d56ac3f932ce32d4bee5c20802453(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e377358cc2049e974bcb5e371d6776309239760b4cd4a277e5a9d82bacb3fc6b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6feac3255e803ca2274d87582ff0ae2e9d19d75165e6e5463335b76e7891cfd(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigHostConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2a9f24b7bcf55fe6ce2796259afd78f66b0655f9f6d8d65ce16fb24b6fb28a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72d516de39c0129f7bfa1df1d130f7b756edc316c9813f2c8696ebfb2775bbe1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfff3287aae32cd5606810c5b1e446b72c084acbc45120a42566fce175823162(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17442819239d1250ad640e682e9268ebaa82e549349069482e38e9baeacf3b85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90bf0d18e3336190ae63d9d61e38d026f6d00a11015986d8f2190f480654ed95(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac8c11a6f8bb0d2e6cc386042d7e05d5b0f5b2fda4a765f1165773d4da6ea6e9(
    *,
    ip_blocks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e52f6a17af40be2a22e8708b90d903382d4d8d280c54d95caeb7666a1c978a50(
    *,
    gateway: builtins.str,
    ips: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps, typing.Dict[builtins.str, typing.Any]]]],
    netmask: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09571110b18a8de90682c286bf50b8e4316e6046453d1eb492774888fb8974cd(
    *,
    ip: builtins.str,
    hostname: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1edbdac4dd81a4a37241682b17e47012325b9fbb5cb022d77186293d079a2221(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3802902b54eee27fd3cd2d836d659c6b5a7ec6342ea7023d7a85011520b92130(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a0ee4bc40fb8c4579907042849a2fee401b436f283aaa5336e47949aa572216(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cebac142230cc72c4ccfd3f54c7fcb3a6a0c9d1e9584419e9daa6172521e919(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b3a4870cfbf5497f6826fbadcdd906bf276ba5245ec0f110c1200a08e59b87(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae51bba5eb73e42ca81da771112013f6c0dbdf35996dd95b3113c49767ef8872(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d5b7dcb057f4ce810b2fd8795e5adf03cd3c80bb431e8764c0c699ea6c512d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2912c0379464aaf3116a60843b43b453bbe51fe4b5649da2def0a7f91878a4f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db8749d7d9f6535d8a5f77c839196d88869e2f0f245e28a0eb006d5121bdfb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__132db781d612c1fae80b5f0f11365f830d9a286ad08268488a4b5c305bb0cbe9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c8770316069e9bba1fa7166373034f137b4b84ce670b0d53de925ec3be636c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25894c94d91c2db02bc052fed4d01010eba5de3195f6ffb8818d612eef711546(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7269719c08bfb8496cbd163f8150a09a4d3d36078a25b2cd431bce9500a63916(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d40b8e267fcc845539b3d3500c04217cb580aa18224f01c8f922a30cd2a3078(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7fbfa69315ec0990529b281847a15b8d4b4c7813a93ac4e508ae7a460c43384(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0f4f7d1d6354888e8230c604fae9657cff3950a68ab6be392aae5d38c852036(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c40676b6111c2346fcddf2e6e830673820cda296079bc358f2dba9246ce0b36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e66fc248c01c6f4b89978c0df42d044730384d28fad5b604943df3b7d78b64f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a70038ce0c72045c1e855a3ebf9767a2c4604f6df5a8a20d0cff42401292cce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a50476a966578587f6b06ab1208cd34d9ce4a5e74687ad9521304472bdfdbff8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2788dfa0b813f4a15f73db4b02ebc07f40cde1b14770f9c2c7cef7aae1f8c8d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__829332215ac45a52fb23149b54b16d943b482ecee0684b1ed1cce362185b0d3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db5991df89d43e78c3b6505a2374bf2b68b8380e50ca1cc0c1f704a6153eecc2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6723925e5d8127508392146f883932fd052d700ed2f47e35375c5ad25bea9688(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52583dde948153ba6ddbdefe3ba4380d183ca8a018c86b261f41149d92d1179(
    *,
    required_platform_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d78d815186d4b291123244f0ba5b267a6f69d9990758fe919f60fb8bfcbb585(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c81e31fa280d528adf2dd9252c1498069db918b8d20d9765fd7c5782a2dbb70(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e44331cc4592c387f54efa708e172c1d5f85e0ac2947d61dd2c4e204b9a0b5b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c6c6e6557099ffc0951e51a71395516255a8524be769a14fa5a0190a86a2972(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f572f1a7423e9024e6fe94e048852013ce73116a7daa44588d86729f89bae919(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41a160fd82ebce769ae9daab1bbe8e05e65aa1c4afa13dbb62983917f37af20f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e95e5ecb11892b37c0631e21abc64a7cb950f3e3f5123c572fba35c78c4ccd0b(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfigBundles],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddc88ed8febfd639055d83e2cfd770d44bf1f458776bacf688324866d3a82e48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a021476164b470f84206ed4b57fb1501c1e48ecaed055ebd06661f0416a844(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42723048bd1c07ef162b12287470d087ccd42bf9caa0b2fa7ad80ed6c13538c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c3b90bd243df73e834aa6c09cb37c1e2725b1810518572263c753fb1486663b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d221db8b040d1b2bb31fef653285e46eab1ba39e6894273f8fd70f41d5fbd66b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f1052fe3b01c581113d565cdd0c2920bb1a1a57dc7654a7ef258604437986f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01996d73f29ba251be7c17da21c31a985d784dd682e72f6eed2802d6a782ce5b(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58152858f75f7d2229b126fddc56749ca8f97b011bcb21a0c01c84b586984a1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f9a722782582ae4c3383f4aa04e642a4e33aa1c23e3502bb6609613716dd91(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a783093b383d64a5ea34a3848b803026645a6c0156e2808122a89a2b486800e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d42dce080de68b61fdf50d95b33b76f157946990b7d5e5282fa018ce80a4f0d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85f566eed680e0fc16888ecc30f90e94e76f4d6c826aa9ab4a8031bb754f0c86(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417d40d632d18dd6e4941cd4b64a6aa827eb34c9e82b235912040257e08a1592(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51540231fa9487a1ba41c840c88d6a31066a7b39193ecaf8faea322548e4a10f(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfigBundlesStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af400205682ea7635ff92e62106bfa8c927c57723a43a8825a1ab5dee80894a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5962adbb8d7a95ec901b3193d93cdcd4a52a93c60c2b4d2ec2071a7a775f7b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c5af02bfb6a8ee492c64c911dbdaca6b3686de5ad4029298f46b8e36995a5f(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f2b45bec8f321e321cd9209cd4b3ca00d0f23970ff0295d757b9f9ed43d84b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5b2b7400ffec7704d82795e42e5ea144aa0b997b06d736ca7cf218099fd0be(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e32c2640fc02c847b149dcca7acf3aba91f39ff7db6474b7793c4994432620(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d99c36ca9726d942ddf9d418c819d9811e9f0fbc7f2b490301ec6396245480de(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41d83fea1ae6ac0a5cc1ec2adf84174714428e8b72e1ee44b40745c5278978ae(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__460e30fc1f1fba459f381f3b01f93273396b6d0956d1809846a2547e9d1491e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9cfff92aeccf75cb773e1830f9cfbfc5a0cd4d4bee7f70173b03ced3894e167(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfigStatusConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6150060539fda63c7407c2c7ce43dc0be6ccc7cd74900ee093cf89c82e07dbc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b38161cba6fc6b0d006a5b5e45d68b26b76282281c5068fda8b8f5836977a2c3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f682f88a7af63fe079ff5f8106c45f5561b5fd3475b365febe4502a7bffc79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b70f633ab9e9201d1ab190dac0b799b5ff0739be8f8fe265dcafd47d2cc0b4e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5501c5abc30cc28c9eeb5e5666006568401f177310568907bf14656ec30bf308(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb6cbbf33a9b46ac6c2103f4a1163780d142fa41f2201b8a0726628075b4061(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad6e24deff614bb35953225e17a0c4d3669ddbbcdda5b2317bd0f574444aec6d(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterPlatformConfigStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230753e315e10e54dbd6558d987f28b0ca0195575d49b80df744a1fb547c4ac2(
    *,
    address: typing.Optional[builtins.str] = None,
    ca_cert: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc7d21ece891a44c598eec81b88f46e0ca7eb20a54423361438f258638354cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ddaf448adcd906c8f8bc00879d694e63564c3d3889fe2a2117e291a2e19dba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6941c87637e7ec75f305c83b717aee55c1d8d50efd33f4b28a0f3dbd784c163a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee9c00ed34fdc975beb8a27a841a667084ac7ea24b787867e641f9c39b32cdf(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterPrivateRegistryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb356359f0138262f9a8ed3fe80c7bef6f73d4fb179d10abfe1d246cf9e605fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d54dd9ac42390212095c4e05e4da2eff41eb592378fd1126bafd164bb0cedb9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7d6ad319e87f40adf649ba46cc4ef79211b533fb68e81e964160b2dc7e8bb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ca092bdd7adf1f629de526cae1f8a4c75026dcd761e6ceaf153c9db78f78d6d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__898a9f0b9e85664abe2c8dcebeb3d48890b8eb15db8c45a0436fcc4d0ada9528(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__764eeff1853f17bf7b002715fe3161f1c64d84c20cb87c6753661b77d340ab1b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__799a56e86d3687f4b743e264327d79403c97122b009af818aaf35990baa24aa3(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterStatusConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd47801cb5c3f9b5b6ad8aec9ec2ddb7caec69d328e42328191d2d2d5be428f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54e5c0fa18c54dd1623762a901634677cd5980ac13783c276d078ea5c35008b3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63fc4816b9198ce934837843c4d7d1225bc05608af20b3fd8a34d5ac19e36d0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836f4898367780e21f4db73e5689e2cac56c629048e3d1cd78f342f711f6f42c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19640c08fcb9c69a62cc9907c926442ba65fc413cbf3e13e760a556ffa25fd45(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d929be67bf43588ae302d064bad23ca400e5b248e6ed870e1fccdb35713de94f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d917d41d1738a50a9f98f9f1594ad3e9f816ceab06cc3a4a5add52dfd2ae117d(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f28238de09019ca7a020ab55c689fb354993dcaab87cb269bb9865a7e6b70ff(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06042b021c636479c78c7256980206d228a7312cc8ffdd68500e07073e7187d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d09d2850d59b5fa8c9582b0c207ab3304ff1a6a33077a0efd4da7b1fadcf20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3152389d554ae433e3a5eafff12a8a5fa4e352752ee33ecf44a6c2df090b93f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f342c8855d13a782f0ee495125eca3d9bcdc5f188bfec14ddff05c64bf6aaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a77d115c935bfcb07a78c9d5a44b4a92c66a85c9ba994fe59c09008a7a9ec98(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareAdminClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea491353290c2b77c5d7d11a295ec57982b785d227570a541332c3098d29b2d(
    *,
    address: typing.Optional[builtins.str] = None,
    ca_cert_data: typing.Optional[builtins.str] = None,
    cluster: typing.Optional[builtins.str] = None,
    datacenter: typing.Optional[builtins.str] = None,
    data_disk: typing.Optional[builtins.str] = None,
    datastore: typing.Optional[builtins.str] = None,
    folder: typing.Optional[builtins.str] = None,
    resource_pool: typing.Optional[builtins.str] = None,
    storage_policy_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e46e272da6bc7622cefe491b5736d2003b9b6530213ca4aefca0f7c463c1a447(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__317f9af974112f4acc4ce6b8968f37d78889ce54d330b767b6e93fc6108f4077(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7534338abf3bfc8f187477d6daa84777df38fb43c29acc65f429e84fbd04219(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9af23e87117ea9e0cebb32da792ef198a124fdb20342c01619e959fe22996205(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3aefe7841a50d5ef9aa38aed505c59c104c2319288b215626ab3a39dd4da4f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c756b2dbf9097a00e0c27a26cdfe9aed913b596727dcaf01f7dbf08168fad3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937f8d347b86581ccf2790e4be83c34fe2796c834a4fe3b562712c148b73441a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa0ebeae65aac40326c35553e33d3af5cafb89c46ea634db42347751d3d3fea5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd26e747bfa0cf7457efee1a43cbe9ac30299e365b4ee3de14275342a4f6089(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3119764a1f52880723799120ef9caf6794a2bb263e0ab80eb20a132701916fdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df4efe9361a5804313d313180e1ecfffb109511feef2088e075c105681f83f6a(
    value: typing.Optional[GoogleGkeonpremVmwareAdminClusterVcenter],
) -> None:
    """Type checking stubs"""
    pass
