r'''
# `google_gkeonprem_vmware_admin_cluster`

Refer to the Terraform Registry for docs: [`google_gkeonprem_vmware_admin_cluster`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster).
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


class GkeonpremVmwareAdminCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster google_gkeonprem_vmware_admin_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        network_config: typing.Union["GkeonpremVmwareAdminClusterNetworkConfig", typing.Dict[builtins.str, typing.Any]],
        addon_node: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterAddonNode", typing.Dict[builtins.str, typing.Any]]] = None,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        anti_affinity_groups: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterAntiAffinityGroups", typing.Dict[builtins.str, typing.Any]]] = None,
        authorization: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_repair_config: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterAutoRepairConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        bootstrap_cluster_membership: typing.Optional[builtins.str] = None,
        control_plane_node: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterControlPlaneNode", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_type: typing.Optional[builtins.str] = None,
        load_balancer: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterLoadBalancer", typing.Dict[builtins.str, typing.Any]]] = None,
        on_prem_version: typing.Optional[builtins.str] = None,
        platform_config: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterPlatformConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        private_registry_config: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterPrivateRegistryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vcenter: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterVcenter", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster google_gkeonprem_vmware_admin_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#location GkeonpremVmwareAdminCluster#location}
        :param name: The VMware admin cluster resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#name GkeonpremVmwareAdminCluster#name}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#network_config GkeonpremVmwareAdminCluster#network_config}
        :param addon_node: addon_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#addon_node GkeonpremVmwareAdminCluster#addon_node}
        :param annotations: Annotations on the VMware Admin Cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#annotations GkeonpremVmwareAdminCluster#annotations}
        :param anti_affinity_groups: anti_affinity_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#anti_affinity_groups GkeonpremVmwareAdminCluster#anti_affinity_groups}
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#authorization GkeonpremVmwareAdminCluster#authorization}
        :param auto_repair_config: auto_repair_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#auto_repair_config GkeonpremVmwareAdminCluster#auto_repair_config}
        :param bootstrap_cluster_membership: The bootstrap cluster this VMware admin cluster belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#bootstrap_cluster_membership GkeonpremVmwareAdminCluster#bootstrap_cluster_membership}
        :param control_plane_node: control_plane_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#control_plane_node GkeonpremVmwareAdminCluster#control_plane_node}
        :param description: A human readable description of this VMware admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#description GkeonpremVmwareAdminCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#id GkeonpremVmwareAdminCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_type: The OS image type for the VMware admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#image_type GkeonpremVmwareAdminCluster#image_type}
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#load_balancer GkeonpremVmwareAdminCluster#load_balancer}
        :param on_prem_version: The Anthos clusters on the VMware version for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#on_prem_version GkeonpremVmwareAdminCluster#on_prem_version}
        :param platform_config: platform_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#platform_config GkeonpremVmwareAdminCluster#platform_config}
        :param private_registry_config: private_registry_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#private_registry_config GkeonpremVmwareAdminCluster#private_registry_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#project GkeonpremVmwareAdminCluster#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#timeouts GkeonpremVmwareAdminCluster#timeouts}
        :param vcenter: vcenter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#vcenter GkeonpremVmwareAdminCluster#vcenter}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__673a0031ef1cf98ceb08d0a1c77119edd30db3ee3b5002d4dbe4e073bdf398a4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GkeonpremVmwareAdminClusterConfig(
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
        '''Generates CDKTF code for importing a GkeonpremVmwareAdminCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GkeonpremVmwareAdminCluster to import.
        :param import_from_id: The id of the existing GkeonpremVmwareAdminCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GkeonpremVmwareAdminCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ab7dd11b72e7a215e428d53840dd559b931b93bf26aae84f706b6c580a974f6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAddonNode")
    def put_addon_node(
        self,
        *,
        auto_resize_config: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auto_resize_config: auto_resize_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#auto_resize_config GkeonpremVmwareAdminCluster#auto_resize_config}
        '''
        value = GkeonpremVmwareAdminClusterAddonNode(
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
        :param aag_config_disabled: Spread nodes across at least three physical hosts (requires at least three hosts). Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#aag_config_disabled GkeonpremVmwareAdminCluster#aag_config_disabled}
        '''
        value = GkeonpremVmwareAdminClusterAntiAffinityGroups(
            aag_config_disabled=aag_config_disabled
        )

        return typing.cast(None, jsii.invoke(self, "putAntiAffinityGroups", [value]))

    @jsii.member(jsii_name="putAuthorization")
    def put_authorization(
        self,
        *,
        viewer_users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremVmwareAdminClusterAuthorizationViewerUsers", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param viewer_users: viewer_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#viewer_users GkeonpremVmwareAdminCluster#viewer_users}
        '''
        value = GkeonpremVmwareAdminClusterAuthorization(viewer_users=viewer_users)

        return typing.cast(None, jsii.invoke(self, "putAuthorization", [value]))

    @jsii.member(jsii_name="putAutoRepairConfig")
    def put_auto_repair_config(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether auto repair is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#enabled GkeonpremVmwareAdminCluster#enabled}
        '''
        value = GkeonpremVmwareAdminClusterAutoRepairConfig(enabled=enabled)

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
        :param cpus: The number of vCPUs for the control-plane node of the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#cpus GkeonpremVmwareAdminCluster#cpus}
        :param memory: The number of mebibytes of memory for the control-plane node of the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#memory GkeonpremVmwareAdminCluster#memory}
        :param replicas: The number of control plane nodes for this VMware admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#replicas GkeonpremVmwareAdminCluster#replicas}
        '''
        value = GkeonpremVmwareAdminClusterControlPlaneNode(
            cpus=cpus, memory=memory, replicas=replicas
        )

        return typing.cast(None, jsii.invoke(self, "putControlPlaneNode", [value]))

    @jsii.member(jsii_name="putLoadBalancer")
    def put_load_balancer(
        self,
        *,
        vip_config: typing.Union["GkeonpremVmwareAdminClusterLoadBalancerVipConfig", typing.Dict[builtins.str, typing.Any]],
        f5_config: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterLoadBalancerF5Config", typing.Dict[builtins.str, typing.Any]]] = None,
        manual_lb_config: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterLoadBalancerManualLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        metal_lb_config: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param vip_config: vip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#vip_config GkeonpremVmwareAdminCluster#vip_config}
        :param f5_config: f5_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#f5_config GkeonpremVmwareAdminCluster#f5_config}
        :param manual_lb_config: manual_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#manual_lb_config GkeonpremVmwareAdminCluster#manual_lb_config}
        :param metal_lb_config: metal_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#metal_lb_config GkeonpremVmwareAdminCluster#metal_lb_config}
        '''
        value = GkeonpremVmwareAdminClusterLoadBalancer(
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
        dhcp_ip_config: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ha_control_plane_config: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        host_config: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterNetworkConfigHostConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        static_ip_config: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        vcenter_network: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pod_address_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#pod_address_cidr_blocks GkeonpremVmwareAdminCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported.. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#service_address_cidr_blocks GkeonpremVmwareAdminCluster#service_address_cidr_blocks}
        :param dhcp_ip_config: dhcp_ip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#dhcp_ip_config GkeonpremVmwareAdminCluster#dhcp_ip_config}
        :param ha_control_plane_config: ha_control_plane_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ha_control_plane_config GkeonpremVmwareAdminCluster#ha_control_plane_config}
        :param host_config: host_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#host_config GkeonpremVmwareAdminCluster#host_config}
        :param static_ip_config: static_ip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#static_ip_config GkeonpremVmwareAdminCluster#static_ip_config}
        :param vcenter_network: vcenter_network specifies vCenter network name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#vcenter_network GkeonpremVmwareAdminCluster#vcenter_network}
        '''
        value = GkeonpremVmwareAdminClusterNetworkConfig(
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
        :param required_platform_version: The required platform version e.g. 1.13.1. If the current platform version is lower than the target version, the platform version will be updated to the target version. If the target version is not installed in the platform (bundle versions), download the target version bundle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#required_platform_version GkeonpremVmwareAdminCluster#required_platform_version}
        '''
        value = GkeonpremVmwareAdminClusterPlatformConfig(
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
        :param address: The registry address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#address GkeonpremVmwareAdminCluster#address}
        :param ca_cert: The CA certificate public key for private registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ca_cert GkeonpremVmwareAdminCluster#ca_cert}
        '''
        value = GkeonpremVmwareAdminClusterPrivateRegistryConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#create GkeonpremVmwareAdminCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#delete GkeonpremVmwareAdminCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#update GkeonpremVmwareAdminCluster#update}.
        '''
        value = GkeonpremVmwareAdminClusterTimeouts(
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
        :param address: The vCenter IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#address GkeonpremVmwareAdminCluster#address}
        :param ca_cert_data: Contains the vCenter CA certificate public key for SSL verification. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ca_cert_data GkeonpremVmwareAdminCluster#ca_cert_data}
        :param cluster: The name of the vCenter cluster for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#cluster GkeonpremVmwareAdminCluster#cluster}
        :param datacenter: The name of the vCenter datacenter for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#datacenter GkeonpremVmwareAdminCluster#datacenter}
        :param data_disk: The name of the virtual machine disk (VMDK) for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#data_disk GkeonpremVmwareAdminCluster#data_disk}
        :param datastore: The name of the vCenter datastore for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#datastore GkeonpremVmwareAdminCluster#datastore}
        :param folder: The name of the vCenter folder for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#folder GkeonpremVmwareAdminCluster#folder}
        :param resource_pool: The name of the vCenter resource pool for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#resource_pool GkeonpremVmwareAdminCluster#resource_pool}
        :param storage_policy_name: The name of the vCenter storage policy for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#storage_policy_name GkeonpremVmwareAdminCluster#storage_policy_name}
        '''
        value = GkeonpremVmwareAdminClusterVcenter(
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
    def addon_node(self) -> "GkeonpremVmwareAdminClusterAddonNodeOutputReference":
        return typing.cast("GkeonpremVmwareAdminClusterAddonNodeOutputReference", jsii.get(self, "addonNode"))

    @builtins.property
    @jsii.member(jsii_name="antiAffinityGroups")
    def anti_affinity_groups(
        self,
    ) -> "GkeonpremVmwareAdminClusterAntiAffinityGroupsOutputReference":
        return typing.cast("GkeonpremVmwareAdminClusterAntiAffinityGroupsOutputReference", jsii.get(self, "antiAffinityGroups"))

    @builtins.property
    @jsii.member(jsii_name="authorization")
    def authorization(
        self,
    ) -> "GkeonpremVmwareAdminClusterAuthorizationOutputReference":
        return typing.cast("GkeonpremVmwareAdminClusterAuthorizationOutputReference", jsii.get(self, "authorization"))

    @builtins.property
    @jsii.member(jsii_name="autoRepairConfig")
    def auto_repair_config(
        self,
    ) -> "GkeonpremVmwareAdminClusterAutoRepairConfigOutputReference":
        return typing.cast("GkeonpremVmwareAdminClusterAutoRepairConfigOutputReference", jsii.get(self, "autoRepairConfig"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneNode")
    def control_plane_node(
        self,
    ) -> "GkeonpremVmwareAdminClusterControlPlaneNodeOutputReference":
        return typing.cast("GkeonpremVmwareAdminClusterControlPlaneNodeOutputReference", jsii.get(self, "controlPlaneNode"))

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
    def fleet(self) -> "GkeonpremVmwareAdminClusterFleetList":
        return typing.cast("GkeonpremVmwareAdminClusterFleetList", jsii.get(self, "fleet"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> "GkeonpremVmwareAdminClusterLoadBalancerOutputReference":
        return typing.cast("GkeonpremVmwareAdminClusterLoadBalancerOutputReference", jsii.get(self, "loadBalancer"))

    @builtins.property
    @jsii.member(jsii_name="localName")
    def local_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localName"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(
        self,
    ) -> "GkeonpremVmwareAdminClusterNetworkConfigOutputReference":
        return typing.cast("GkeonpremVmwareAdminClusterNetworkConfigOutputReference", jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="platformConfig")
    def platform_config(
        self,
    ) -> "GkeonpremVmwareAdminClusterPlatformConfigOutputReference":
        return typing.cast("GkeonpremVmwareAdminClusterPlatformConfigOutputReference", jsii.get(self, "platformConfig"))

    @builtins.property
    @jsii.member(jsii_name="privateRegistryConfig")
    def private_registry_config(
        self,
    ) -> "GkeonpremVmwareAdminClusterPrivateRegistryConfigOutputReference":
        return typing.cast("GkeonpremVmwareAdminClusterPrivateRegistryConfigOutputReference", jsii.get(self, "privateRegistryConfig"))

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
    def status(self) -> "GkeonpremVmwareAdminClusterStatusList":
        return typing.cast("GkeonpremVmwareAdminClusterStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GkeonpremVmwareAdminClusterTimeoutsOutputReference":
        return typing.cast("GkeonpremVmwareAdminClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    def vcenter(self) -> "GkeonpremVmwareAdminClusterVcenterOutputReference":
        return typing.cast("GkeonpremVmwareAdminClusterVcenterOutputReference", jsii.get(self, "vcenter"))

    @builtins.property
    @jsii.member(jsii_name="addonNodeInput")
    def addon_node_input(
        self,
    ) -> typing.Optional["GkeonpremVmwareAdminClusterAddonNode"]:
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterAddonNode"], jsii.get(self, "addonNodeInput"))

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
    ) -> typing.Optional["GkeonpremVmwareAdminClusterAntiAffinityGroups"]:
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterAntiAffinityGroups"], jsii.get(self, "antiAffinityGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationInput")
    def authorization_input(
        self,
    ) -> typing.Optional["GkeonpremVmwareAdminClusterAuthorization"]:
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterAuthorization"], jsii.get(self, "authorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="autoRepairConfigInput")
    def auto_repair_config_input(
        self,
    ) -> typing.Optional["GkeonpremVmwareAdminClusterAutoRepairConfig"]:
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterAutoRepairConfig"], jsii.get(self, "autoRepairConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bootstrapClusterMembershipInput")
    def bootstrap_cluster_membership_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootstrapClusterMembershipInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneNodeInput")
    def control_plane_node_input(
        self,
    ) -> typing.Optional["GkeonpremVmwareAdminClusterControlPlaneNode"]:
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterControlPlaneNode"], jsii.get(self, "controlPlaneNodeInput"))

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
    ) -> typing.Optional["GkeonpremVmwareAdminClusterLoadBalancer"]:
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterLoadBalancer"], jsii.get(self, "loadBalancerInput"))

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
    ) -> typing.Optional["GkeonpremVmwareAdminClusterNetworkConfig"]:
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterNetworkConfig"], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="onPremVersionInput")
    def on_prem_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onPremVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="platformConfigInput")
    def platform_config_input(
        self,
    ) -> typing.Optional["GkeonpremVmwareAdminClusterPlatformConfig"]:
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterPlatformConfig"], jsii.get(self, "platformConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="privateRegistryConfigInput")
    def private_registry_config_input(
        self,
    ) -> typing.Optional["GkeonpremVmwareAdminClusterPrivateRegistryConfig"]:
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterPrivateRegistryConfig"], jsii.get(self, "privateRegistryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeonpremVmwareAdminClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeonpremVmwareAdminClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vcenterInput")
    def vcenter_input(self) -> typing.Optional["GkeonpremVmwareAdminClusterVcenter"]:
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterVcenter"], jsii.get(self, "vcenterInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__715624e290ade7fcd4efb8af441a1f475bb175b4a0ee6c212fe5e2a217b3326b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bootstrapClusterMembership")
    def bootstrap_cluster_membership(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootstrapClusterMembership"))

    @bootstrap_cluster_membership.setter
    def bootstrap_cluster_membership(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef186ef01b8bcb848e9ff4ea44412d2804b8a605a04aa578dbb555f670e29091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootstrapClusterMembership", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2440816f6ad63936af6115c7f08b4d9b2274b7e26e757c3784ee3a432bc7105c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2145d29940d34805a9a917cb229a7ac7f0b3adfdc8c1aab8ef0c7090183f12c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageType")
    def image_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageType"))

    @image_type.setter
    def image_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__102f0f38d6d07ff98065b2ab67c311ba1e715aa4f501c8cef72a8d23fa781761)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__959224c3688f7b0744a0e54b695870fbd6bb95563e5af995835a1679cbc1aa2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc2eeecb5b924aedef0f113f6bbbe226262d464dba65cde4c5e30f6f161e8758)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onPremVersion")
    def on_prem_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onPremVersion"))

    @on_prem_version.setter
    def on_prem_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9913d13adb844deb509594228847965ee1421ac19453fcfa828ba46f0bb53409)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onPremVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baf0d45226964da302433fcd88610dbfc3ce087366bb280c225da6a5d45e6e64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterAddonNode",
    jsii_struct_bases=[],
    name_mapping={"auto_resize_config": "autoResizeConfig"},
)
class GkeonpremVmwareAdminClusterAddonNode:
    def __init__(
        self,
        *,
        auto_resize_config: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auto_resize_config: auto_resize_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#auto_resize_config GkeonpremVmwareAdminCluster#auto_resize_config}
        '''
        if isinstance(auto_resize_config, dict):
            auto_resize_config = GkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig(**auto_resize_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0eea16e510f79275461eee2762c7e139831e4f5a84c18e436d55cef3a4ea250)
            check_type(argname="argument auto_resize_config", value=auto_resize_config, expected_type=type_hints["auto_resize_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_resize_config is not None:
            self._values["auto_resize_config"] = auto_resize_config

    @builtins.property
    def auto_resize_config(
        self,
    ) -> typing.Optional["GkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig"]:
        '''auto_resize_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#auto_resize_config GkeonpremVmwareAdminCluster#auto_resize_config}
        '''
        result = self._values.get("auto_resize_config")
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterAddonNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether to enable controle plane node auto resizing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#enabled GkeonpremVmwareAdminCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8734eaf195ee778426c58ef86cd995aa664ba427c3b6cb3e81e7fcdaa0fed21)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether to enable controle plane node auto resizing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#enabled GkeonpremVmwareAdminCluster#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareAdminClusterAddonNodeAutoResizeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterAddonNodeAutoResizeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8106426b3cea5c3554df7287c7e108ed1df8a2e8b0203279590c0b8cc4b10c8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b83afd72f5508725f57fd165b1bd9af0d32d2133dfb7676d78379c6c04323865)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00cb5bd3786d59be2b37f50312e778e7d39abad46e936eadcde81bf84d500c32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareAdminClusterAddonNodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterAddonNodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f71259eb77d7c0e261c92c6a031ec8bdfacdd91ea649084e7fc75d00164ec0c6)
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
        :param enabled: Whether to enable controle plane node auto resizing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#enabled GkeonpremVmwareAdminCluster#enabled}
        '''
        value = GkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putAutoResizeConfig", [value]))

    @jsii.member(jsii_name="resetAutoResizeConfig")
    def reset_auto_resize_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoResizeConfig", []))

    @builtins.property
    @jsii.member(jsii_name="autoResizeConfig")
    def auto_resize_config(
        self,
    ) -> GkeonpremVmwareAdminClusterAddonNodeAutoResizeConfigOutputReference:
        return typing.cast(GkeonpremVmwareAdminClusterAddonNodeAutoResizeConfigOutputReference, jsii.get(self, "autoResizeConfig"))

    @builtins.property
    @jsii.member(jsii_name="autoResizeConfigInput")
    def auto_resize_config_input(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig], jsii.get(self, "autoResizeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremVmwareAdminClusterAddonNode]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterAddonNode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterAddonNode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acb68f2c9a03cea1c406ff0c3c65b95716e8bb1a3336c5119d15de01ec0bb53e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterAntiAffinityGroups",
    jsii_struct_bases=[],
    name_mapping={"aag_config_disabled": "aagConfigDisabled"},
)
class GkeonpremVmwareAdminClusterAntiAffinityGroups:
    def __init__(
        self,
        *,
        aag_config_disabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param aag_config_disabled: Spread nodes across at least three physical hosts (requires at least three hosts). Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#aag_config_disabled GkeonpremVmwareAdminCluster#aag_config_disabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__567b53519794edbf4fefcd3ee9b0dcb415814d0ee6776292c3672403bf7e23b2)
            check_type(argname="argument aag_config_disabled", value=aag_config_disabled, expected_type=type_hints["aag_config_disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aag_config_disabled": aag_config_disabled,
        }

    @builtins.property
    def aag_config_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Spread nodes across at least three physical hosts (requires at least three hosts). Enabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#aag_config_disabled GkeonpremVmwareAdminCluster#aag_config_disabled}
        '''
        result = self._values.get("aag_config_disabled")
        assert result is not None, "Required property 'aag_config_disabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterAntiAffinityGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareAdminClusterAntiAffinityGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterAntiAffinityGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0e5b3e33e6242c3310940404f139dcb10c490747449d8e7867f8f6b55af204f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__066a74874513bd66aaff19815c4fe4e7582318e299ef74f74584b51e9018ccbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aagConfigDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterAntiAffinityGroups]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterAntiAffinityGroups], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterAntiAffinityGroups],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e45dca08fc5922a5e148365c24810462a2906d0250f14ae186691abcc2862a68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterAuthorization",
    jsii_struct_bases=[],
    name_mapping={"viewer_users": "viewerUsers"},
)
class GkeonpremVmwareAdminClusterAuthorization:
    def __init__(
        self,
        *,
        viewer_users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremVmwareAdminClusterAuthorizationViewerUsers", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param viewer_users: viewer_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#viewer_users GkeonpremVmwareAdminCluster#viewer_users}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebeaedbe974c3a5e159d1ad570b9d6c46bd1c6bb6eefd5ab461d6cf51b2c3352)
            check_type(argname="argument viewer_users", value=viewer_users, expected_type=type_hints["viewer_users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if viewer_users is not None:
            self._values["viewer_users"] = viewer_users

    @builtins.property
    def viewer_users(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareAdminClusterAuthorizationViewerUsers"]]]:
        '''viewer_users block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#viewer_users GkeonpremVmwareAdminCluster#viewer_users}
        '''
        result = self._values.get("viewer_users")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareAdminClusterAuthorizationViewerUsers"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareAdminClusterAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96707cad6ee4540195abec4482813636e28cd5f9fe0f8872da4cc05b36320ca8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putViewerUsers")
    def put_viewer_users(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremVmwareAdminClusterAuthorizationViewerUsers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45983a0a7f740697f8324787ab55b7bb9fa268512cf4af9a071329b60b1f301f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putViewerUsers", [value]))

    @jsii.member(jsii_name="resetViewerUsers")
    def reset_viewer_users(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetViewerUsers", []))

    @builtins.property
    @jsii.member(jsii_name="viewerUsers")
    def viewer_users(self) -> "GkeonpremVmwareAdminClusterAuthorizationViewerUsersList":
        return typing.cast("GkeonpremVmwareAdminClusterAuthorizationViewerUsersList", jsii.get(self, "viewerUsers"))

    @builtins.property
    @jsii.member(jsii_name="viewerUsersInput")
    def viewer_users_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareAdminClusterAuthorizationViewerUsers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareAdminClusterAuthorizationViewerUsers"]]], jsii.get(self, "viewerUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterAuthorization]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3be79b30461ed079c17ddab6d2b469d011965a8661894481bd04b391bedd7c7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterAuthorizationViewerUsers",
    jsii_struct_bases=[],
    name_mapping={"username": "username"},
)
class GkeonpremVmwareAdminClusterAuthorizationViewerUsers:
    def __init__(self, *, username: builtins.str) -> None:
        '''
        :param username: The name of the user, e.g. 'my-gcp-id@gmail.com'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#username GkeonpremVmwareAdminCluster#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69add56521f14ef2f4618fe37d5e93aab959b599de540abbcbb33df3b916ea5d)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
        }

    @builtins.property
    def username(self) -> builtins.str:
        '''The name of the user, e.g. 'my-gcp-id@gmail.com'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#username GkeonpremVmwareAdminCluster#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterAuthorizationViewerUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareAdminClusterAuthorizationViewerUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterAuthorizationViewerUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48b56182c6df673642d4aa6a2993983dfc4b2f194cb2509c5cd5922c361fd81b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareAdminClusterAuthorizationViewerUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce066c920c72f467246d4613a8a09e33687bd72afabb76f5122ec2985f23d05c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareAdminClusterAuthorizationViewerUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f01e053685a576442ab3adb202ba042432c75d49628ef181b9135aaf25cc1ab7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__568c6cda8b1c0a81c098312ac41f1bfa1567107d46a7b26dc5415c6d73069852)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a8efe53603b8d7981f09066a3b2a30bb0614fd1da45ec0d8930541f874ae922)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareAdminClusterAuthorizationViewerUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareAdminClusterAuthorizationViewerUsers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareAdminClusterAuthorizationViewerUsers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__832b1be76c68bb8ff1d0780d0473efc664db4bc7960b053edd9c307833d1e138)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareAdminClusterAuthorizationViewerUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterAuthorizationViewerUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__485053e10492ddac83988152daca87b38da80bab4cc24d7a5053170cadec926f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ab2d7161371dafdbfcbeaf451423f52e17d24919032ce1ffc972285b0cec0c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareAdminClusterAuthorizationViewerUsers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareAdminClusterAuthorizationViewerUsers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareAdminClusterAuthorizationViewerUsers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a185210e05af8a4249aadcee9b2ad594ba066ac779b8a8da6ccf95da2260f34d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterAutoRepairConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GkeonpremVmwareAdminClusterAutoRepairConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether auto repair is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#enabled GkeonpremVmwareAdminCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd4b54b50dbb3d670b534a0ceae211869b52499ee526c1fd130f1e633db6a233)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether auto repair is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#enabled GkeonpremVmwareAdminCluster#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterAutoRepairConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareAdminClusterAutoRepairConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterAutoRepairConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba06f7dc22dfa4d7e8ed593b304394539cdaf0ec1e608fd883e9ecf401ad2e4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca7c8ee423e93b2e55c6367b2ea8d2ee5dbfde8cc3d7b437bcaccd195a32f6b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterAutoRepairConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterAutoRepairConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterAutoRepairConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__035f2c4c06f953678d235f7aa45b32eb94c7948efb98517d740db2d543e46d34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterConfig",
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
class GkeonpremVmwareAdminClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        network_config: typing.Union["GkeonpremVmwareAdminClusterNetworkConfig", typing.Dict[builtins.str, typing.Any]],
        addon_node: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterAddonNode, typing.Dict[builtins.str, typing.Any]]] = None,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        anti_affinity_groups: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterAntiAffinityGroups, typing.Dict[builtins.str, typing.Any]]] = None,
        authorization: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_repair_config: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterAutoRepairConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        bootstrap_cluster_membership: typing.Optional[builtins.str] = None,
        control_plane_node: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterControlPlaneNode", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_type: typing.Optional[builtins.str] = None,
        load_balancer: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterLoadBalancer", typing.Dict[builtins.str, typing.Any]]] = None,
        on_prem_version: typing.Optional[builtins.str] = None,
        platform_config: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterPlatformConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        private_registry_config: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterPrivateRegistryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vcenter: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterVcenter", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#location GkeonpremVmwareAdminCluster#location}
        :param name: The VMware admin cluster resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#name GkeonpremVmwareAdminCluster#name}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#network_config GkeonpremVmwareAdminCluster#network_config}
        :param addon_node: addon_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#addon_node GkeonpremVmwareAdminCluster#addon_node}
        :param annotations: Annotations on the VMware Admin Cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#annotations GkeonpremVmwareAdminCluster#annotations}
        :param anti_affinity_groups: anti_affinity_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#anti_affinity_groups GkeonpremVmwareAdminCluster#anti_affinity_groups}
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#authorization GkeonpremVmwareAdminCluster#authorization}
        :param auto_repair_config: auto_repair_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#auto_repair_config GkeonpremVmwareAdminCluster#auto_repair_config}
        :param bootstrap_cluster_membership: The bootstrap cluster this VMware admin cluster belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#bootstrap_cluster_membership GkeonpremVmwareAdminCluster#bootstrap_cluster_membership}
        :param control_plane_node: control_plane_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#control_plane_node GkeonpremVmwareAdminCluster#control_plane_node}
        :param description: A human readable description of this VMware admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#description GkeonpremVmwareAdminCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#id GkeonpremVmwareAdminCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_type: The OS image type for the VMware admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#image_type GkeonpremVmwareAdminCluster#image_type}
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#load_balancer GkeonpremVmwareAdminCluster#load_balancer}
        :param on_prem_version: The Anthos clusters on the VMware version for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#on_prem_version GkeonpremVmwareAdminCluster#on_prem_version}
        :param platform_config: platform_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#platform_config GkeonpremVmwareAdminCluster#platform_config}
        :param private_registry_config: private_registry_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#private_registry_config GkeonpremVmwareAdminCluster#private_registry_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#project GkeonpremVmwareAdminCluster#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#timeouts GkeonpremVmwareAdminCluster#timeouts}
        :param vcenter: vcenter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#vcenter GkeonpremVmwareAdminCluster#vcenter}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(network_config, dict):
            network_config = GkeonpremVmwareAdminClusterNetworkConfig(**network_config)
        if isinstance(addon_node, dict):
            addon_node = GkeonpremVmwareAdminClusterAddonNode(**addon_node)
        if isinstance(anti_affinity_groups, dict):
            anti_affinity_groups = GkeonpremVmwareAdminClusterAntiAffinityGroups(**anti_affinity_groups)
        if isinstance(authorization, dict):
            authorization = GkeonpremVmwareAdminClusterAuthorization(**authorization)
        if isinstance(auto_repair_config, dict):
            auto_repair_config = GkeonpremVmwareAdminClusterAutoRepairConfig(**auto_repair_config)
        if isinstance(control_plane_node, dict):
            control_plane_node = GkeonpremVmwareAdminClusterControlPlaneNode(**control_plane_node)
        if isinstance(load_balancer, dict):
            load_balancer = GkeonpremVmwareAdminClusterLoadBalancer(**load_balancer)
        if isinstance(platform_config, dict):
            platform_config = GkeonpremVmwareAdminClusterPlatformConfig(**platform_config)
        if isinstance(private_registry_config, dict):
            private_registry_config = GkeonpremVmwareAdminClusterPrivateRegistryConfig(**private_registry_config)
        if isinstance(timeouts, dict):
            timeouts = GkeonpremVmwareAdminClusterTimeouts(**timeouts)
        if isinstance(vcenter, dict):
            vcenter = GkeonpremVmwareAdminClusterVcenter(**vcenter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc915f2c6b82352f149dc2cebbaa970aef102a7aba321dceaffd98c160589225)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#location GkeonpremVmwareAdminCluster#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The VMware admin cluster resource name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#name GkeonpremVmwareAdminCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_config(self) -> "GkeonpremVmwareAdminClusterNetworkConfig":
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#network_config GkeonpremVmwareAdminCluster#network_config}
        '''
        result = self._values.get("network_config")
        assert result is not None, "Required property 'network_config' is missing"
        return typing.cast("GkeonpremVmwareAdminClusterNetworkConfig", result)

    @builtins.property
    def addon_node(self) -> typing.Optional[GkeonpremVmwareAdminClusterAddonNode]:
        '''addon_node block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#addon_node GkeonpremVmwareAdminCluster#addon_node}
        '''
        result = self._values.get("addon_node")
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterAddonNode], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#annotations GkeonpremVmwareAdminCluster#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def anti_affinity_groups(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterAntiAffinityGroups]:
        '''anti_affinity_groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#anti_affinity_groups GkeonpremVmwareAdminCluster#anti_affinity_groups}
        '''
        result = self._values.get("anti_affinity_groups")
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterAntiAffinityGroups], result)

    @builtins.property
    def authorization(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterAuthorization]:
        '''authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#authorization GkeonpremVmwareAdminCluster#authorization}
        '''
        result = self._values.get("authorization")
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterAuthorization], result)

    @builtins.property
    def auto_repair_config(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterAutoRepairConfig]:
        '''auto_repair_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#auto_repair_config GkeonpremVmwareAdminCluster#auto_repair_config}
        '''
        result = self._values.get("auto_repair_config")
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterAutoRepairConfig], result)

    @builtins.property
    def bootstrap_cluster_membership(self) -> typing.Optional[builtins.str]:
        '''The bootstrap cluster this VMware admin cluster belongs to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#bootstrap_cluster_membership GkeonpremVmwareAdminCluster#bootstrap_cluster_membership}
        '''
        result = self._values.get("bootstrap_cluster_membership")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def control_plane_node(
        self,
    ) -> typing.Optional["GkeonpremVmwareAdminClusterControlPlaneNode"]:
        '''control_plane_node block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#control_plane_node GkeonpremVmwareAdminCluster#control_plane_node}
        '''
        result = self._values.get("control_plane_node")
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterControlPlaneNode"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human readable description of this VMware admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#description GkeonpremVmwareAdminCluster#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#id GkeonpremVmwareAdminCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_type(self) -> typing.Optional[builtins.str]:
        '''The OS image type for the VMware admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#image_type GkeonpremVmwareAdminCluster#image_type}
        '''
        result = self._values.get("image_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer(
        self,
    ) -> typing.Optional["GkeonpremVmwareAdminClusterLoadBalancer"]:
        '''load_balancer block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#load_balancer GkeonpremVmwareAdminCluster#load_balancer}
        '''
        result = self._values.get("load_balancer")
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterLoadBalancer"], result)

    @builtins.property
    def on_prem_version(self) -> typing.Optional[builtins.str]:
        '''The Anthos clusters on the VMware version for the admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#on_prem_version GkeonpremVmwareAdminCluster#on_prem_version}
        '''
        result = self._values.get("on_prem_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platform_config(
        self,
    ) -> typing.Optional["GkeonpremVmwareAdminClusterPlatformConfig"]:
        '''platform_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#platform_config GkeonpremVmwareAdminCluster#platform_config}
        '''
        result = self._values.get("platform_config")
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterPlatformConfig"], result)

    @builtins.property
    def private_registry_config(
        self,
    ) -> typing.Optional["GkeonpremVmwareAdminClusterPrivateRegistryConfig"]:
        '''private_registry_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#private_registry_config GkeonpremVmwareAdminCluster#private_registry_config}
        '''
        result = self._values.get("private_registry_config")
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterPrivateRegistryConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#project GkeonpremVmwareAdminCluster#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GkeonpremVmwareAdminClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#timeouts GkeonpremVmwareAdminCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterTimeouts"], result)

    @builtins.property
    def vcenter(self) -> typing.Optional["GkeonpremVmwareAdminClusterVcenter"]:
        '''vcenter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#vcenter GkeonpremVmwareAdminCluster#vcenter}
        '''
        result = self._values.get("vcenter")
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterVcenter"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterControlPlaneNode",
    jsii_struct_bases=[],
    name_mapping={"cpus": "cpus", "memory": "memory", "replicas": "replicas"},
)
class GkeonpremVmwareAdminClusterControlPlaneNode:
    def __init__(
        self,
        *,
        cpus: typing.Optional[jsii.Number] = None,
        memory: typing.Optional[jsii.Number] = None,
        replicas: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpus: The number of vCPUs for the control-plane node of the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#cpus GkeonpremVmwareAdminCluster#cpus}
        :param memory: The number of mebibytes of memory for the control-plane node of the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#memory GkeonpremVmwareAdminCluster#memory}
        :param replicas: The number of control plane nodes for this VMware admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#replicas GkeonpremVmwareAdminCluster#replicas}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95fccc5c2c65edfe1e04b0f989c2f4dba32f0aa33324646b86c41e85ba636ccc)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#cpus GkeonpremVmwareAdminCluster#cpus}
        '''
        result = self._values.get("cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory(self) -> typing.Optional[jsii.Number]:
        '''The number of mebibytes of memory for the control-plane node of the admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#memory GkeonpremVmwareAdminCluster#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def replicas(self) -> typing.Optional[jsii.Number]:
        '''The number of control plane nodes for this VMware admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#replicas GkeonpremVmwareAdminCluster#replicas}
        '''
        result = self._values.get("replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterControlPlaneNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareAdminClusterControlPlaneNodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterControlPlaneNodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36b6df98b030c04c3905dbd7eed1e5aeec60b56da857a9fdaeef62eb35870281)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f203680a1f5f7a9653f0328fed7629df02e9b6af42c9ec17e463a3c1957f5bee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__642510aa39b4b4481ca35cd0e0bac7df4b6c1081551147bb0be9513e2f7cc5d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicas")
    def replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicas"))

    @replicas.setter
    def replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e996d322f169b45d0841ef191190aac6ac9b7c9a943371f44ceaa604673cfd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterControlPlaneNode]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterControlPlaneNode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterControlPlaneNode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9deba1f7137b275f181a1eb87e41267e3a8637b824f07b37e5762a604e5406)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterFleet",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremVmwareAdminClusterFleet:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterFleet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareAdminClusterFleetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterFleetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__edec75f7c9c96faae110b3517af4eaf029dd632ddec1790d10796b6e7e2afe4f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareAdminClusterFleetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e75b2d957fafeadc1671f4e5c8e91ebc870dc0d9d4b40429885e9d2fb984d0df)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareAdminClusterFleetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b802d02a5cd16dcf11cb325f044b6228c16947a65b73c1fe6b0dff42c6ee4b6b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c43e36a4ae551790f77e524d9dbf685104c2a2b75e2e80f748c735964778f8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93dc00157ddcabda7d28833d0509a6746e1bbdcdc506bda445250f43eed94dfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareAdminClusterFleetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterFleetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12154629f4f532d4442772a6e50971ea325d9c928f94fce5e08413923340c556)
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
    def internal_value(self) -> typing.Optional[GkeonpremVmwareAdminClusterFleet]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterFleet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterFleet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57ee4ca84927202eacac09d0c4b71828b544e98f2ef1ca4da3ccadfb6bdc5497)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterLoadBalancer",
    jsii_struct_bases=[],
    name_mapping={
        "vip_config": "vipConfig",
        "f5_config": "f5Config",
        "manual_lb_config": "manualLbConfig",
        "metal_lb_config": "metalLbConfig",
    },
)
class GkeonpremVmwareAdminClusterLoadBalancer:
    def __init__(
        self,
        *,
        vip_config: typing.Union["GkeonpremVmwareAdminClusterLoadBalancerVipConfig", typing.Dict[builtins.str, typing.Any]],
        f5_config: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterLoadBalancerF5Config", typing.Dict[builtins.str, typing.Any]]] = None,
        manual_lb_config: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterLoadBalancerManualLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        metal_lb_config: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param vip_config: vip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#vip_config GkeonpremVmwareAdminCluster#vip_config}
        :param f5_config: f5_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#f5_config GkeonpremVmwareAdminCluster#f5_config}
        :param manual_lb_config: manual_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#manual_lb_config GkeonpremVmwareAdminCluster#manual_lb_config}
        :param metal_lb_config: metal_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#metal_lb_config GkeonpremVmwareAdminCluster#metal_lb_config}
        '''
        if isinstance(vip_config, dict):
            vip_config = GkeonpremVmwareAdminClusterLoadBalancerVipConfig(**vip_config)
        if isinstance(f5_config, dict):
            f5_config = GkeonpremVmwareAdminClusterLoadBalancerF5Config(**f5_config)
        if isinstance(manual_lb_config, dict):
            manual_lb_config = GkeonpremVmwareAdminClusterLoadBalancerManualLbConfig(**manual_lb_config)
        if isinstance(metal_lb_config, dict):
            metal_lb_config = GkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig(**metal_lb_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ac64c927de04ce28c789d0efea1d2cf2a09d162d00780d87c7acb8fe340f271)
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
    def vip_config(self) -> "GkeonpremVmwareAdminClusterLoadBalancerVipConfig":
        '''vip_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#vip_config GkeonpremVmwareAdminCluster#vip_config}
        '''
        result = self._values.get("vip_config")
        assert result is not None, "Required property 'vip_config' is missing"
        return typing.cast("GkeonpremVmwareAdminClusterLoadBalancerVipConfig", result)

    @builtins.property
    def f5_config(
        self,
    ) -> typing.Optional["GkeonpremVmwareAdminClusterLoadBalancerF5Config"]:
        '''f5_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#f5_config GkeonpremVmwareAdminCluster#f5_config}
        '''
        result = self._values.get("f5_config")
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterLoadBalancerF5Config"], result)

    @builtins.property
    def manual_lb_config(
        self,
    ) -> typing.Optional["GkeonpremVmwareAdminClusterLoadBalancerManualLbConfig"]:
        '''manual_lb_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#manual_lb_config GkeonpremVmwareAdminCluster#manual_lb_config}
        '''
        result = self._values.get("manual_lb_config")
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterLoadBalancerManualLbConfig"], result)

    @builtins.property
    def metal_lb_config(
        self,
    ) -> typing.Optional["GkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig"]:
        '''metal_lb_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#metal_lb_config GkeonpremVmwareAdminCluster#metal_lb_config}
        '''
        result = self._values.get("metal_lb_config")
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterLoadBalancer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterLoadBalancerF5Config",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "partition": "partition",
        "snat_pool": "snatPool",
    },
)
class GkeonpremVmwareAdminClusterLoadBalancerF5Config:
    def __init__(
        self,
        *,
        address: typing.Optional[builtins.str] = None,
        partition: typing.Optional[builtins.str] = None,
        snat_pool: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: The load balancer's IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#address GkeonpremVmwareAdminCluster#address}
        :param partition: he preexisting partition to be used by the load balancer. T his partition is usually created for the admin cluster for example: 'my-f5-admin-partition'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#partition GkeonpremVmwareAdminCluster#partition}
        :param snat_pool: The pool name. Only necessary, if using SNAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#snat_pool GkeonpremVmwareAdminCluster#snat_pool}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a689230e25f3f9553e707acdaf1c10c617efb3e1af0d7471b37b003c8335926a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#address GkeonpremVmwareAdminCluster#address}
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partition(self) -> typing.Optional[builtins.str]:
        '''he preexisting partition to be used by the load balancer.

        T
        his partition is usually created for the admin cluster for example:
        'my-f5-admin-partition'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#partition GkeonpremVmwareAdminCluster#partition}
        '''
        result = self._values.get("partition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snat_pool(self) -> typing.Optional[builtins.str]:
        '''The pool name. Only necessary, if using SNAT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#snat_pool GkeonpremVmwareAdminCluster#snat_pool}
        '''
        result = self._values.get("snat_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterLoadBalancerF5Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareAdminClusterLoadBalancerF5ConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterLoadBalancerF5ConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5bf5e739bfa44f7254693fc734558b724252b5b7dde67844275b34ef831ab7f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7d4f4625a7e7ed14017cfc808a664f97a93e44edb34ff72cf7dc036299e8d22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partition")
    def partition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partition"))

    @partition.setter
    def partition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0534f0a6dfe128461e95dd94ae675aacfdf03d4737f9b668b99f64abb588e83f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snatPool")
    def snat_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snatPool"))

    @snat_pool.setter
    def snat_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dc6fb2304d464c906a1b24e5cd98d3801e79bb7e51f1ee122441b37a7057026)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snatPool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterLoadBalancerF5Config]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterLoadBalancerF5Config], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterLoadBalancerF5Config],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bb3b4783d182ed2ca6cd5cfebc4ffd7086faf471cd4987609e6155a487db25b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterLoadBalancerManualLbConfig",
    jsii_struct_bases=[],
    name_mapping={
        "addons_node_port": "addonsNodePort",
        "control_plane_node_port": "controlPlaneNodePort",
        "ingress_http_node_port": "ingressHttpNodePort",
        "ingress_https_node_port": "ingressHttpsNodePort",
        "konnectivity_server_node_port": "konnectivityServerNodePort",
    },
)
class GkeonpremVmwareAdminClusterLoadBalancerManualLbConfig:
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
        :param addons_node_port: NodePort for add-ons server in the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#addons_node_port GkeonpremVmwareAdminCluster#addons_node_port}
        :param control_plane_node_port: NodePort for control plane service. The Kubernetes API server in the admin cluster is implemented as a Service of type NodePort (ex. 30968). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#control_plane_node_port GkeonpremVmwareAdminCluster#control_plane_node_port}
        :param ingress_http_node_port: NodePort for ingress service's http. The ingress service in the admin cluster is implemented as a Service of type NodePort (ex. 32527). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ingress_http_node_port GkeonpremVmwareAdminCluster#ingress_http_node_port}
        :param ingress_https_node_port: NodePort for ingress service's https. The ingress service in the admin cluster is implemented as a Service of type NodePort (ex. 30139). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ingress_https_node_port GkeonpremVmwareAdminCluster#ingress_https_node_port}
        :param konnectivity_server_node_port: NodePort for konnectivity server service running as a sidecar in each kube-apiserver pod (ex. 30564). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#konnectivity_server_node_port GkeonpremVmwareAdminCluster#konnectivity_server_node_port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bb0849721409c447107eb769fb08626e01d5be794957d3afff9263d84c11a09)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#addons_node_port GkeonpremVmwareAdminCluster#addons_node_port}
        '''
        result = self._values.get("addons_node_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def control_plane_node_port(self) -> typing.Optional[jsii.Number]:
        '''NodePort for control plane service.

        The Kubernetes API server in the admin
        cluster is implemented as a Service of type NodePort (ex. 30968).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#control_plane_node_port GkeonpremVmwareAdminCluster#control_plane_node_port}
        '''
        result = self._values.get("control_plane_node_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ingress_http_node_port(self) -> typing.Optional[jsii.Number]:
        '''NodePort for ingress service's http.

        The ingress service in the admin
        cluster is implemented as a Service of type NodePort (ex. 32527).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ingress_http_node_port GkeonpremVmwareAdminCluster#ingress_http_node_port}
        '''
        result = self._values.get("ingress_http_node_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ingress_https_node_port(self) -> typing.Optional[jsii.Number]:
        '''NodePort for ingress service's https.

        The ingress service in the admin
        cluster is implemented as a Service of type NodePort (ex. 30139).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ingress_https_node_port GkeonpremVmwareAdminCluster#ingress_https_node_port}
        '''
        result = self._values.get("ingress_https_node_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def konnectivity_server_node_port(self) -> typing.Optional[jsii.Number]:
        '''NodePort for konnectivity server service running as a sidecar in each kube-apiserver pod (ex. 30564).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#konnectivity_server_node_port GkeonpremVmwareAdminCluster#konnectivity_server_node_port}
        '''
        result = self._values.get("konnectivity_server_node_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterLoadBalancerManualLbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareAdminClusterLoadBalancerManualLbConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterLoadBalancerManualLbConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39099b3abdafdf66b850c8b7084052e38c15814e4d21bd0531cae79f763c68f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f54d0f713bf0648007f46b37d229b95503a9890b4a2c77c9f49bf8dfa91dd653)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addonsNodePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="controlPlaneNodePort")
    def control_plane_node_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "controlPlaneNodePort"))

    @control_plane_node_port.setter
    def control_plane_node_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8683265b13fea38b32b1189e12680845f8999508122347e801af162dd7def7d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneNodePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingressHttpNodePort")
    def ingress_http_node_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ingressHttpNodePort"))

    @ingress_http_node_port.setter
    def ingress_http_node_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8675f73a666ef488c10ef184547ad685cae68a7821b1d7312bd6596a702c97a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingressHttpNodePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingressHttpsNodePort")
    def ingress_https_node_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ingressHttpsNodePort"))

    @ingress_https_node_port.setter
    def ingress_https_node_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f78493a187aa93f89f88f1056d013b3867b59e600be984f1d1e9b8419d4d372a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingressHttpsNodePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="konnectivityServerNodePort")
    def konnectivity_server_node_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "konnectivityServerNodePort"))

    @konnectivity_server_node_port.setter
    def konnectivity_server_node_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f99d165ebe89058b23b1ac8c18f1d8b3a513c2bf982d079bf3c60b2e9708b55a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "konnectivityServerNodePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterLoadBalancerManualLbConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterLoadBalancerManualLbConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterLoadBalancerManualLbConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adabcde8f8ffed6dd1d3a692f9fbd95cf2c9c2db4b2da18663d7ddb59e95ccfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Metal LB is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#enabled GkeonpremVmwareAdminCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32478c3a4d7d29855ae9149cc0fa699ae2dd1e542b28f77a8194cc309108fba2)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Metal LB is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#enabled GkeonpremVmwareAdminCluster#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareAdminClusterLoadBalancerMetalLbConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterLoadBalancerMetalLbConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__671002dd629094d0f96d72b9f2fa09f8c6e2b498f1d43433ada85c2e4c526bae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c86878fd6fffbdcdb567afd0792b4f94a5aa19f2c91cd65a72a996dd448f1576)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__582dae19b687aa3787c5d8f704cbd350e97ab2b7a22445a9ebe30786d9c437bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareAdminClusterLoadBalancerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterLoadBalancerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3433999d6bedbeb8f0df9d8c59a414df27eeee4b5910ad31252b6663a5e85212)
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
        :param address: The load balancer's IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#address GkeonpremVmwareAdminCluster#address}
        :param partition: he preexisting partition to be used by the load balancer. T his partition is usually created for the admin cluster for example: 'my-f5-admin-partition'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#partition GkeonpremVmwareAdminCluster#partition}
        :param snat_pool: The pool name. Only necessary, if using SNAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#snat_pool GkeonpremVmwareAdminCluster#snat_pool}
        '''
        value = GkeonpremVmwareAdminClusterLoadBalancerF5Config(
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
        :param addons_node_port: NodePort for add-ons server in the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#addons_node_port GkeonpremVmwareAdminCluster#addons_node_port}
        :param control_plane_node_port: NodePort for control plane service. The Kubernetes API server in the admin cluster is implemented as a Service of type NodePort (ex. 30968). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#control_plane_node_port GkeonpremVmwareAdminCluster#control_plane_node_port}
        :param ingress_http_node_port: NodePort for ingress service's http. The ingress service in the admin cluster is implemented as a Service of type NodePort (ex. 32527). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ingress_http_node_port GkeonpremVmwareAdminCluster#ingress_http_node_port}
        :param ingress_https_node_port: NodePort for ingress service's https. The ingress service in the admin cluster is implemented as a Service of type NodePort (ex. 30139). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ingress_https_node_port GkeonpremVmwareAdminCluster#ingress_https_node_port}
        :param konnectivity_server_node_port: NodePort for konnectivity server service running as a sidecar in each kube-apiserver pod (ex. 30564). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#konnectivity_server_node_port GkeonpremVmwareAdminCluster#konnectivity_server_node_port}
        '''
        value = GkeonpremVmwareAdminClusterLoadBalancerManualLbConfig(
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
        :param enabled: Metal LB is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#enabled GkeonpremVmwareAdminCluster#enabled}
        '''
        value = GkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putMetalLbConfig", [value]))

    @jsii.member(jsii_name="putVipConfig")
    def put_vip_config(
        self,
        *,
        control_plane_vip: builtins.str,
        addons_vip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param control_plane_vip: The VIP which you previously set aside for the Kubernetes API of this VMware Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#control_plane_vip GkeonpremVmwareAdminCluster#control_plane_vip}
        :param addons_vip: The VIP to configure the load balancer for add-ons. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#addons_vip GkeonpremVmwareAdminCluster#addons_vip}
        '''
        value = GkeonpremVmwareAdminClusterLoadBalancerVipConfig(
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
    ) -> GkeonpremVmwareAdminClusterLoadBalancerF5ConfigOutputReference:
        return typing.cast(GkeonpremVmwareAdminClusterLoadBalancerF5ConfigOutputReference, jsii.get(self, "f5Config"))

    @builtins.property
    @jsii.member(jsii_name="manualLbConfig")
    def manual_lb_config(
        self,
    ) -> GkeonpremVmwareAdminClusterLoadBalancerManualLbConfigOutputReference:
        return typing.cast(GkeonpremVmwareAdminClusterLoadBalancerManualLbConfigOutputReference, jsii.get(self, "manualLbConfig"))

    @builtins.property
    @jsii.member(jsii_name="metalLbConfig")
    def metal_lb_config(
        self,
    ) -> GkeonpremVmwareAdminClusterLoadBalancerMetalLbConfigOutputReference:
        return typing.cast(GkeonpremVmwareAdminClusterLoadBalancerMetalLbConfigOutputReference, jsii.get(self, "metalLbConfig"))

    @builtins.property
    @jsii.member(jsii_name="vipConfig")
    def vip_config(
        self,
    ) -> "GkeonpremVmwareAdminClusterLoadBalancerVipConfigOutputReference":
        return typing.cast("GkeonpremVmwareAdminClusterLoadBalancerVipConfigOutputReference", jsii.get(self, "vipConfig"))

    @builtins.property
    @jsii.member(jsii_name="f5ConfigInput")
    def f5_config_input(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterLoadBalancerF5Config]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterLoadBalancerF5Config], jsii.get(self, "f5ConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="manualLbConfigInput")
    def manual_lb_config_input(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterLoadBalancerManualLbConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterLoadBalancerManualLbConfig], jsii.get(self, "manualLbConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="metalLbConfigInput")
    def metal_lb_config_input(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig], jsii.get(self, "metalLbConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="vipConfigInput")
    def vip_config_input(
        self,
    ) -> typing.Optional["GkeonpremVmwareAdminClusterLoadBalancerVipConfig"]:
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterLoadBalancerVipConfig"], jsii.get(self, "vipConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterLoadBalancer]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterLoadBalancer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterLoadBalancer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4198af4fd601fc164919bf09038b5769da6bf38818b31d18055ba426d9f6961)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterLoadBalancerVipConfig",
    jsii_struct_bases=[],
    name_mapping={"control_plane_vip": "controlPlaneVip", "addons_vip": "addonsVip"},
)
class GkeonpremVmwareAdminClusterLoadBalancerVipConfig:
    def __init__(
        self,
        *,
        control_plane_vip: builtins.str,
        addons_vip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param control_plane_vip: The VIP which you previously set aside for the Kubernetes API of this VMware Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#control_plane_vip GkeonpremVmwareAdminCluster#control_plane_vip}
        :param addons_vip: The VIP to configure the load balancer for add-ons. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#addons_vip GkeonpremVmwareAdminCluster#addons_vip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0bc3806131338b02144f598e75e1153e244c3d3010d36997cf4ef1e8fb22cb7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#control_plane_vip GkeonpremVmwareAdminCluster#control_plane_vip}
        '''
        result = self._values.get("control_plane_vip")
        assert result is not None, "Required property 'control_plane_vip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def addons_vip(self) -> typing.Optional[builtins.str]:
        '''The VIP to configure the load balancer for add-ons.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#addons_vip GkeonpremVmwareAdminCluster#addons_vip}
        '''
        result = self._values.get("addons_vip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterLoadBalancerVipConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareAdminClusterLoadBalancerVipConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterLoadBalancerVipConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f5d2a0b87e2e96c2faad701ccf3ff8e3d4e75302dc1e3fd98995c499a161e04)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b78f2468a6f18b560178a2edad5096bef17401597d4a981478473d56b45a76ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addonsVip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="controlPlaneVip")
    def control_plane_vip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "controlPlaneVip"))

    @control_plane_vip.setter
    def control_plane_vip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0c7271e6be10946c257604019464350390c895249429f1953935f08ed1761a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneVip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterLoadBalancerVipConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterLoadBalancerVipConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterLoadBalancerVipConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90d02e858b1fc21abd8355074d43c162e799a07d52a9b3fe499371bb947aefb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterNetworkConfig",
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
class GkeonpremVmwareAdminClusterNetworkConfig:
    def __init__(
        self,
        *,
        pod_address_cidr_blocks: typing.Sequence[builtins.str],
        service_address_cidr_blocks: typing.Sequence[builtins.str],
        dhcp_ip_config: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ha_control_plane_config: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        host_config: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterNetworkConfigHostConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        static_ip_config: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        vcenter_network: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pod_address_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#pod_address_cidr_blocks GkeonpremVmwareAdminCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported.. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#service_address_cidr_blocks GkeonpremVmwareAdminCluster#service_address_cidr_blocks}
        :param dhcp_ip_config: dhcp_ip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#dhcp_ip_config GkeonpremVmwareAdminCluster#dhcp_ip_config}
        :param ha_control_plane_config: ha_control_plane_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ha_control_plane_config GkeonpremVmwareAdminCluster#ha_control_plane_config}
        :param host_config: host_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#host_config GkeonpremVmwareAdminCluster#host_config}
        :param static_ip_config: static_ip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#static_ip_config GkeonpremVmwareAdminCluster#static_ip_config}
        :param vcenter_network: vcenter_network specifies vCenter network name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#vcenter_network GkeonpremVmwareAdminCluster#vcenter_network}
        '''
        if isinstance(dhcp_ip_config, dict):
            dhcp_ip_config = GkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig(**dhcp_ip_config)
        if isinstance(ha_control_plane_config, dict):
            ha_control_plane_config = GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig(**ha_control_plane_config)
        if isinstance(host_config, dict):
            host_config = GkeonpremVmwareAdminClusterNetworkConfigHostConfig(**host_config)
        if isinstance(static_ip_config, dict):
            static_ip_config = GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig(**static_ip_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6ee7bac7159d4286e9bfd1c30197994b6c3006f9c82e057d7c29302f60b7a3e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#pod_address_cidr_blocks GkeonpremVmwareAdminCluster#pod_address_cidr_blocks}
        '''
        result = self._values.get("pod_address_cidr_blocks")
        assert result is not None, "Required property 'pod_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        '''All services in the cluster are assigned an RFC1918 IPv4 address from these ranges.

        Only a single range is supported.. This field
        cannot be changed after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#service_address_cidr_blocks GkeonpremVmwareAdminCluster#service_address_cidr_blocks}
        '''
        result = self._values.get("service_address_cidr_blocks")
        assert result is not None, "Required property 'service_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def dhcp_ip_config(
        self,
    ) -> typing.Optional["GkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig"]:
        '''dhcp_ip_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#dhcp_ip_config GkeonpremVmwareAdminCluster#dhcp_ip_config}
        '''
        result = self._values.get("dhcp_ip_config")
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig"], result)

    @builtins.property
    def ha_control_plane_config(
        self,
    ) -> typing.Optional["GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig"]:
        '''ha_control_plane_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ha_control_plane_config GkeonpremVmwareAdminCluster#ha_control_plane_config}
        '''
        result = self._values.get("ha_control_plane_config")
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig"], result)

    @builtins.property
    def host_config(
        self,
    ) -> typing.Optional["GkeonpremVmwareAdminClusterNetworkConfigHostConfig"]:
        '''host_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#host_config GkeonpremVmwareAdminCluster#host_config}
        '''
        result = self._values.get("host_config")
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterNetworkConfigHostConfig"], result)

    @builtins.property
    def static_ip_config(
        self,
    ) -> typing.Optional["GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig"]:
        '''static_ip_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#static_ip_config GkeonpremVmwareAdminCluster#static_ip_config}
        '''
        result = self._values.get("static_ip_config")
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig"], result)

    @builtins.property
    def vcenter_network(self) -> typing.Optional[builtins.str]:
        '''vcenter_network specifies vCenter network name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#vcenter_network GkeonpremVmwareAdminCluster#vcenter_network}
        '''
        result = self._values.get("vcenter_network")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: enabled is a flag to mark if DHCP IP allocation is used for VMware admin clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#enabled GkeonpremVmwareAdminCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9e1fca293bc7bb83345244abb4b3b3ff36eb26ce93d73bbd4c6bbdfd0d75b9d)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''enabled is a flag to mark if DHCP IP allocation is used for VMware admin clusters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#enabled GkeonpremVmwareAdminCluster#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbe091ccb341fe8de3949f92b89ca305421f2aabf8f2d4b1b405d65c00037967)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5751c0a32bcd50cc2d55113472f98e61d3b920af9434d95427ab614a78ac93bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cca1f77382cf6f0ce1a57e5e1414907dfb1902f8ce922854305b76de8a9dec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig",
    jsii_struct_bases=[],
    name_mapping={"control_plane_ip_block": "controlPlaneIpBlock"},
)
class GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig:
    def __init__(
        self,
        *,
        control_plane_ip_block: typing.Optional[typing.Union["GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param control_plane_ip_block: control_plane_ip_block block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#control_plane_ip_block GkeonpremVmwareAdminCluster#control_plane_ip_block}
        '''
        if isinstance(control_plane_ip_block, dict):
            control_plane_ip_block = GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock(**control_plane_ip_block)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5672abdf63dc728bfc10fcc8db94b18eb382cc2ce985fbc5110290c5f00da9a5)
            check_type(argname="argument control_plane_ip_block", value=control_plane_ip_block, expected_type=type_hints["control_plane_ip_block"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if control_plane_ip_block is not None:
            self._values["control_plane_ip_block"] = control_plane_ip_block

    @builtins.property
    def control_plane_ip_block(
        self,
    ) -> typing.Optional["GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock"]:
        '''control_plane_ip_block block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#control_plane_ip_block GkeonpremVmwareAdminCluster#control_plane_ip_block}
        '''
        result = self._values.get("control_plane_ip_block")
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock",
    jsii_struct_bases=[],
    name_mapping={"gateway": "gateway", "ips": "ips", "netmask": "netmask"},
)
class GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock:
    def __init__(
        self,
        *,
        gateway: builtins.str,
        ips: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps", typing.Dict[builtins.str, typing.Any]]]],
        netmask: builtins.str,
    ) -> None:
        '''
        :param gateway: The network gateway used by the VMware Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#gateway GkeonpremVmwareAdminCluster#gateway}
        :param ips: ips block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ips GkeonpremVmwareAdminCluster#ips}
        :param netmask: The netmask used by the VMware Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#netmask GkeonpremVmwareAdminCluster#netmask}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6645a056d24126f37f38894649f3fa45571ec2e3bc87aec00ced184c58eaf1d6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#gateway GkeonpremVmwareAdminCluster#gateway}
        '''
        result = self._values.get("gateway")
        assert result is not None, "Required property 'gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ips(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps"]]:
        '''ips block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ips GkeonpremVmwareAdminCluster#ips}
        '''
        result = self._values.get("ips")
        assert result is not None, "Required property 'ips' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps"]], result)

    @builtins.property
    def netmask(self) -> builtins.str:
        '''The netmask used by the VMware Admin Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#netmask GkeonpremVmwareAdminCluster#netmask}
        '''
        result = self._values.get("netmask")
        assert result is not None, "Required property 'netmask' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps",
    jsii_struct_bases=[],
    name_mapping={"ip": "ip", "hostname": "hostname"},
)
class GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps:
    def __init__(
        self,
        *,
        ip: builtins.str,
        hostname: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip: IP could be an IP address (like 1.2.3.4) or a CIDR (like 1.2.3.0/24). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ip GkeonpremVmwareAdminCluster#ip}
        :param hostname: Hostname of the machine. VM's name will be used if this field is empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#hostname GkeonpremVmwareAdminCluster#hostname}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77bc0bf570d44974eb09ecc68315b57257e576f45180a74cd6fb5eee0f2fb012)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ip GkeonpremVmwareAdminCluster#ip}
        '''
        result = self._values.get("ip")
        assert result is not None, "Required property 'ip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''Hostname of the machine. VM's name will be used if this field is empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#hostname GkeonpremVmwareAdminCluster#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIpsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIpsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3cae63e147b983ee6f4591aac2fbbc24a5b3a72613c47247565ff0af365f3b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIpsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce0ab3f11e8667133382a79ccf933233533aa38fc3a36c78741e29efa12d2b91)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIpsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfa93e975e3b84816cd4592e458b66ee3e42d52ef504d9504ef49984379cb87b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea57b988edb23ddad8c8e6530e03631a96d4ecec21b8c25555e0a85034532ca7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2824b71230112a22f824f883ac3cabe70dd13bb7f4f200a0d0a811916c3fa966)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b4754655dd73d3b2f2599dacb4dc73e09e6cc36d445864d3895c1aa9f16d914)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIpsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIpsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fcbb7dde2ddc0c197072e1adf8044db641f0187a5926ef85dc7e98cce60e9e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eff5c15496b582dd53cf055fd4fb11d75f25f62f472df1a53b9f367c63bf9ddd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__661bd1e7a55b10bb581993a8d532504eb71b8a206190b17695b1469129f59813)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60f19172b2cdf0f3346c985e4431511cc0003405b616ab6cfe476f8fe23fac54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa7b4ecc39ad3a9ae545cc3e8cf121a046e5d4bc5770a37a95614d62f696784c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIps")
    def put_ips(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e4d0963747a4555ea246de1cd50261451322faa0bd5a4fbaed2ac66e7a497ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIps", [value]))

    @builtins.property
    @jsii.member(jsii_name="ips")
    def ips(
        self,
    ) -> GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIpsList:
        return typing.cast(GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIpsList, jsii.get(self, "ips"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="ipsInput")
    def ips_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps]]], jsii.get(self, "ipsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6c286a57c42218ee5346bea64a2703b4b5525f591840e3f138611e483969e941)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateway", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netmask")
    def netmask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netmask"))

    @netmask.setter
    def netmask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aec27409e3d134bb50b15c573a43542a25dab1f88fed51592e3705c24fdfc00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netmask", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48be2129214df7497b96d191b737365892e44c025870ee5f7b3b87a65aa6082a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29f555f99d36c1a5f4ba81187d9933389a0679c5bc1087fb5d61f487e5e17c60)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putControlPlaneIpBlock")
    def put_control_plane_ip_block(
        self,
        *,
        gateway: builtins.str,
        ips: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps, typing.Dict[builtins.str, typing.Any]]]],
        netmask: builtins.str,
    ) -> None:
        '''
        :param gateway: The network gateway used by the VMware Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#gateway GkeonpremVmwareAdminCluster#gateway}
        :param ips: ips block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ips GkeonpremVmwareAdminCluster#ips}
        :param netmask: The netmask used by the VMware Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#netmask GkeonpremVmwareAdminCluster#netmask}
        '''
        value = GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock(
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
    ) -> GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockOutputReference:
        return typing.cast(GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockOutputReference, jsii.get(self, "controlPlaneIpBlock"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneIpBlockInput")
    def control_plane_ip_block_input(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock], jsii.get(self, "controlPlaneIpBlockInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3cda0c5f247389fdbb7f8c0b9e2e303b5f676c7c71c65ab025db04e6dbf5ade)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterNetworkConfigHostConfig",
    jsii_struct_bases=[],
    name_mapping={
        "dns_search_domains": "dnsSearchDomains",
        "dns_servers": "dnsServers",
        "ntp_servers": "ntpServers",
    },
)
class GkeonpremVmwareAdminClusterNetworkConfigHostConfig:
    def __init__(
        self,
        *,
        dns_search_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        ntp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param dns_search_domains: DNS search domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#dns_search_domains GkeonpremVmwareAdminCluster#dns_search_domains}
        :param dns_servers: DNS servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#dns_servers GkeonpremVmwareAdminCluster#dns_servers}
        :param ntp_servers: NTP servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ntp_servers GkeonpremVmwareAdminCluster#ntp_servers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dcd67431b8e62c2f0e7745c10a125410009d8c449b45ac9f4f5613f0ebf06f8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#dns_search_domains GkeonpremVmwareAdminCluster#dns_search_domains}
        '''
        result = self._values.get("dns_search_domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dns_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''DNS servers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#dns_servers GkeonpremVmwareAdminCluster#dns_servers}
        '''
        result = self._values.get("dns_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ntp_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''NTP servers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ntp_servers GkeonpremVmwareAdminCluster#ntp_servers}
        '''
        result = self._values.get("ntp_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterNetworkConfigHostConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareAdminClusterNetworkConfigHostConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterNetworkConfigHostConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cbd4afb40ed5e79dcc901a678d00db334429a61911694d3423ad09346ff6c15)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c499ab75998e61de2e3774036a0109a00b71c94c8e438d864277394df80c458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsSearchDomains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsServers")
    def dns_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dnsServers"))

    @dns_servers.setter
    def dns_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc0d999460e29c7c96d4b785a8087cbef82fa54c66fadf4a38c0eb3c9d4db153)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ntpServers")
    def ntp_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ntpServers"))

    @ntp_servers.setter
    def ntp_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52468504d2ff121a9bef07a84cd4dd6d9912624ce0e5e675401cd817e1dbd0ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ntpServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigHostConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigHostConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigHostConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d7d136dc1295d49f97bbb56c5355bcc5b66c7462df4ffe6b31bd86ab66e1fa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareAdminClusterNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26d5acf60543142541d830911d265087bc7ac08853324d73e0b8d8c4a6331f36)
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
        :param enabled: enabled is a flag to mark if DHCP IP allocation is used for VMware admin clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#enabled GkeonpremVmwareAdminCluster#enabled}
        '''
        value = GkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putDhcpIpConfig", [value]))

    @jsii.member(jsii_name="putHaControlPlaneConfig")
    def put_ha_control_plane_config(
        self,
        *,
        control_plane_ip_block: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param control_plane_ip_block: control_plane_ip_block block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#control_plane_ip_block GkeonpremVmwareAdminCluster#control_plane_ip_block}
        '''
        value = GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig(
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
        :param dns_search_domains: DNS search domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#dns_search_domains GkeonpremVmwareAdminCluster#dns_search_domains}
        :param dns_servers: DNS servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#dns_servers GkeonpremVmwareAdminCluster#dns_servers}
        :param ntp_servers: NTP servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ntp_servers GkeonpremVmwareAdminCluster#ntp_servers}
        '''
        value = GkeonpremVmwareAdminClusterNetworkConfigHostConfig(
            dns_search_domains=dns_search_domains,
            dns_servers=dns_servers,
            ntp_servers=ntp_servers,
        )

        return typing.cast(None, jsii.invoke(self, "putHostConfig", [value]))

    @jsii.member(jsii_name="putStaticIpConfig")
    def put_static_ip_config(
        self,
        *,
        ip_blocks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param ip_blocks: ip_blocks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ip_blocks GkeonpremVmwareAdminCluster#ip_blocks}
        '''
        value = GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig(
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
    ) -> GkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfigOutputReference:
        return typing.cast(GkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfigOutputReference, jsii.get(self, "dhcpIpConfig"))

    @builtins.property
    @jsii.member(jsii_name="haControlPlaneConfig")
    def ha_control_plane_config(
        self,
    ) -> GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigOutputReference:
        return typing.cast(GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigOutputReference, jsii.get(self, "haControlPlaneConfig"))

    @builtins.property
    @jsii.member(jsii_name="hostConfig")
    def host_config(
        self,
    ) -> GkeonpremVmwareAdminClusterNetworkConfigHostConfigOutputReference:
        return typing.cast(GkeonpremVmwareAdminClusterNetworkConfigHostConfigOutputReference, jsii.get(self, "hostConfig"))

    @builtins.property
    @jsii.member(jsii_name="staticIpConfig")
    def static_ip_config(
        self,
    ) -> "GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigOutputReference":
        return typing.cast("GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigOutputReference", jsii.get(self, "staticIpConfig"))

    @builtins.property
    @jsii.member(jsii_name="dhcpIpConfigInput")
    def dhcp_ip_config_input(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig], jsii.get(self, "dhcpIpConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="haControlPlaneConfigInput")
    def ha_control_plane_config_input(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig], jsii.get(self, "haControlPlaneConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="hostConfigInput")
    def host_config_input(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigHostConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigHostConfig], jsii.get(self, "hostConfigInput"))

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
    ) -> typing.Optional["GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig"]:
        return typing.cast(typing.Optional["GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig"], jsii.get(self, "staticIpConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e8f32a35912b38d4d16a672bb631fe5f96b4d40680f8f48eaf74813acaf70629)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAddressCidrBlocks")
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceAddressCidrBlocks"))

    @service_address_cidr_blocks.setter
    def service_address_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__510a3cb4c82c41c4a877c5ea841afffa75098055a36b23fcde97e9eb68111d65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vcenterNetwork")
    def vcenter_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vcenterNetwork"))

    @vcenter_network.setter
    def vcenter_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcf4f47df9bf63ee468eed7bc6ce2ab11eb18c8bf40f34ae5d8ac8e7cac34aed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vcenterNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterNetworkConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__924d1ca203567c4ff8e79cfcf577010d16a738aa8b112aaec244fd887dc486ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig",
    jsii_struct_bases=[],
    name_mapping={"ip_blocks": "ipBlocks"},
)
class GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig:
    def __init__(
        self,
        *,
        ip_blocks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param ip_blocks: ip_blocks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ip_blocks GkeonpremVmwareAdminCluster#ip_blocks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c59ad611d306285e360e05c4c7541655d367c71a335c199a3c1c125d692fda8)
            check_type(argname="argument ip_blocks", value=ip_blocks, expected_type=type_hints["ip_blocks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ip_blocks is not None:
            self._values["ip_blocks"] = ip_blocks

    @builtins.property
    def ip_blocks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks"]]]:
        '''ip_blocks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ip_blocks GkeonpremVmwareAdminCluster#ip_blocks}
        '''
        result = self._values.get("ip_blocks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks",
    jsii_struct_bases=[],
    name_mapping={"gateway": "gateway", "ips": "ips", "netmask": "netmask"},
)
class GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks:
    def __init__(
        self,
        *,
        gateway: builtins.str,
        ips: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps", typing.Dict[builtins.str, typing.Any]]]],
        netmask: builtins.str,
    ) -> None:
        '''
        :param gateway: The network gateway used by the VMware Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#gateway GkeonpremVmwareAdminCluster#gateway}
        :param ips: ips block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ips GkeonpremVmwareAdminCluster#ips}
        :param netmask: The netmask used by the VMware Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#netmask GkeonpremVmwareAdminCluster#netmask}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3c802a23366b62807e78b6e27da77038d55980d70d0a42fb8a815c902a01581)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#gateway GkeonpremVmwareAdminCluster#gateway}
        '''
        result = self._values.get("gateway")
        assert result is not None, "Required property 'gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ips(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps"]]:
        '''ips block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ips GkeonpremVmwareAdminCluster#ips}
        '''
        result = self._values.get("ips")
        assert result is not None, "Required property 'ips' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps"]], result)

    @builtins.property
    def netmask(self) -> builtins.str:
        '''The netmask used by the VMware Admin Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#netmask GkeonpremVmwareAdminCluster#netmask}
        '''
        result = self._values.get("netmask")
        assert result is not None, "Required property 'netmask' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps",
    jsii_struct_bases=[],
    name_mapping={"ip": "ip", "hostname": "hostname"},
)
class GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps:
    def __init__(
        self,
        *,
        ip: builtins.str,
        hostname: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip: IP could be an IP address (like 1.2.3.4) or a CIDR (like 1.2.3.0/24). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ip GkeonpremVmwareAdminCluster#ip}
        :param hostname: Hostname of the machine. VM's name will be used if this field is empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#hostname GkeonpremVmwareAdminCluster#hostname}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1546a0bb7d3dd39b31687295501357a633c85afe11afd75f0a9b765490ef3452)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ip GkeonpremVmwareAdminCluster#ip}
        '''
        result = self._values.get("ip")
        assert result is not None, "Required property 'ip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''Hostname of the machine. VM's name will be used if this field is empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#hostname GkeonpremVmwareAdminCluster#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIpsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIpsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e689a0803b4b76b5a5feebffb127f7d43108ae80255dc008c52315d3de27109e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIpsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa5e4ffbdd95d5d1e65021ae879409e1a2011114c946f1c90a14b8dcb3a5bf2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIpsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9ccc023fab67830a52f50f4a79b6da38252c44241e44cd9dd33894dba3fc6bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6fc14e54a0e19f88052f8bdc39829b719691f90d2c4a6ee4cb39809f551aff5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a24203912165086ecca6b1d4bff0ff33b401e17ca6ba000af99407471622916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__435c5f92b11ef7dba51516c30ea33c19be75edd90401231d769237f562f16d6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIpsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIpsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba729e6054daa95ce9205687f7a4138de0b3522e5850c5e2e353b840c2060678)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f19854b2dbe3e73a6c22bbabfdda11d360d6567f2afea2f558b144cda7ae6ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3247b6999f1b4aca5d850f18f4a4f81de867f2d3bdcb6b463a02b5f2882f71c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78bb2434a3ff4b9ae1a1a03d920508ab2471c0ff1c1ab1cab569b59f0286923c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d26fba0300fb10a2b73f55e98f1c73233b744e1dde7c74ce924a93e089b3b7b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e572f29c4c8b4ff0b7418d93736e20e670fffe8af21446c2aae91fc3db517810)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6fe75a8773d0d0b70085534e3eb0b910adee087b7d51a60b67cae25efe7a676)
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
            type_hints = typing.get_type_hints(_typecheckingstub__211163680ffd95e1b1c1868422163acc8869521e80ee923a74af6e4b2e306e99)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c73d9f604a3e1a8733a9795b2f4a4b3f0cc70a1acc2e9f8786ea448ef354cb9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edc5ab74583376400f7b3e029fb1e1fea26f9c7073b8534f7240e64934228203)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cadf63cffb285b8c89ad815248795a13e9fc2ca581c09069642f9584a646493c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIps")
    def put_ips(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dd203ac1eb2656edebdc714dafbd2478726b6d0c4f05025b6eec393eeda48e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIps", [value]))

    @builtins.property
    @jsii.member(jsii_name="ips")
    def ips(
        self,
    ) -> GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIpsList:
        return typing.cast(GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIpsList, jsii.get(self, "ips"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="ipsInput")
    def ips_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps]]], jsii.get(self, "ipsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0cfeeeaeb227179d1edcadc0cf2fd94dba153f508329437f612ceca1e47a4310)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateway", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netmask")
    def netmask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netmask"))

    @netmask.setter
    def netmask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e77d7aa1bfec7137453c12d766348155a104f6b493908d6769eebd095e6d6d0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netmask", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd69121db712be98f732a9f42d05a6823da0c2f60349103105b96d45d0f65381)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f839863beb0059860ee1d5fb2c0fbe00860a1facdf8eb0f3c01a31c40d819345)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIpBlocks")
    def put_ip_blocks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce60ff4ebc4899553f401070abce8767b73ee195fd444b7a42ff91ec61ebe246)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpBlocks", [value]))

    @jsii.member(jsii_name="resetIpBlocks")
    def reset_ip_blocks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpBlocks", []))

    @builtins.property
    @jsii.member(jsii_name="ipBlocks")
    def ip_blocks(
        self,
    ) -> GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksList:
        return typing.cast(GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksList, jsii.get(self, "ipBlocks"))

    @builtins.property
    @jsii.member(jsii_name="ipBlocksInput")
    def ip_blocks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks]]], jsii.get(self, "ipBlocksInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c05da628900d941c05d94c9da01b0358cb6c755424d0b5dc3f2c688dc54263d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterPlatformConfig",
    jsii_struct_bases=[],
    name_mapping={"required_platform_version": "requiredPlatformVersion"},
)
class GkeonpremVmwareAdminClusterPlatformConfig:
    def __init__(
        self,
        *,
        required_platform_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param required_platform_version: The required platform version e.g. 1.13.1. If the current platform version is lower than the target version, the platform version will be updated to the target version. If the target version is not installed in the platform (bundle versions), download the target version bundle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#required_platform_version GkeonpremVmwareAdminCluster#required_platform_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__895158fa4d0979ce1ce30b233f06225098ff63b89112446cdd2c9467696b9629)
            check_type(argname="argument required_platform_version", value=required_platform_version, expected_type=type_hints["required_platform_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if required_platform_version is not None:
            self._values["required_platform_version"] = required_platform_version

    @builtins.property
    def required_platform_version(self) -> typing.Optional[builtins.str]:
        '''The required platform version e.g. 1.13.1. If the current platform version is lower than the target version, the platform version will be updated to the target version. If the target version is not installed in the platform (bundle versions), download the target version bundle.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#required_platform_version GkeonpremVmwareAdminCluster#required_platform_version}
        '''
        result = self._values.get("required_platform_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterPlatformConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterPlatformConfigBundles",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremVmwareAdminClusterPlatformConfigBundles:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterPlatformConfigBundles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareAdminClusterPlatformConfigBundlesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterPlatformConfigBundlesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2d60a2c55818884639a107c1a96a60d559b90b6edb0d5bbff153b10bf3c8ded)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareAdminClusterPlatformConfigBundlesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc87a3ae9b187578af0b3f96e7df93cc986af1ce9b394a736be9e6380c6756f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareAdminClusterPlatformConfigBundlesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4942bdef44aff9753350a41b6b9e426a001e39a1bdec2f99976f4ee176d4565)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb32b3df60b3908092f689b7fca35cdc34f4ed3b74bcf0b77b50a1d79ef9e565)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b9f3b7c9b165fa5e3981cad65864ac1f330be4d85de32fbfb95f077cb12e060)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareAdminClusterPlatformConfigBundlesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterPlatformConfigBundlesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99792cd246b2cba69deaf8ee5badd2320d143b4406b4523ecc24848636efdf14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusList":
        return typing.cast("GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterPlatformConfigBundles]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterPlatformConfigBundles], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterPlatformConfigBundles],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b062b6511e36c8767993c5033045d52855bd829cc67486fb5948370fcd45aae1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterPlatformConfigBundlesStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremVmwareAdminClusterPlatformConfigBundlesStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterPlatformConfigBundlesStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1dc59f6224f3b8bf7fef4a166cdf9e5b7e98fa684017506819e5f7e69b90186)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__badf8156eb1532769e2faa8d9ae626331129b31f4f8c5fcb7283efb8ea792781)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74cd105eeaad52f103e9a2b4fe0cc0505173902996b48798ca1dc7c73fc88a02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e36605c90776643b010db11af405bc8bf9f99c8dcecc77bc5005d4c184b949ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67811f5adfa1299a42aa5b16f31766bdb31714aac65dfbbb0839ab6e102db60c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1b7983d982afc2882f6bd79ddfb850d89c7d9c819a24152810f88fa27b4edff)
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
    ) -> typing.Optional[GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditions]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4674b771a3f778296d75d1c2c5eff15beb5730d3b90271ffdf05722d6bead32a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1ed1bbdfff969f34ab802eab3b8d97a240968f40b38624194eabd01b110687b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2735415446b72593d87ccded87860ac92b00ea48e0961a7de3567b8e5e6b947a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d967307807fcafd0c25006867c5643b7b78035d25958f57857a4b230ff545d95)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a94833fc06b6277a1de207a6ae8c96d8fe02d2703a43f659d71848d744fcd15)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f28038a80816a3a2e045c94815dddf9cdd33cf1c9d1adc5f2fb0b72d5dbb7b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db31ddad428fcc4690ab5c9246fbacb625fd89bb7b1e1005a190aef7c1a8672c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(
        self,
    ) -> GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditionsList:
        return typing.cast(GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterPlatformConfigBundlesStatus]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterPlatformConfigBundlesStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterPlatformConfigBundlesStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bd80f6dc74e50220090ad70b7ae418552f56ea9bef246f1075bf91433248fa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareAdminClusterPlatformConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterPlatformConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfea9ebaee2fd15eaf03a5df582134b532b781c913760d931ca8bc7ea8e87c8b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRequiredPlatformVersion")
    def reset_required_platform_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredPlatformVersion", []))

    @builtins.property
    @jsii.member(jsii_name="bundles")
    def bundles(self) -> GkeonpremVmwareAdminClusterPlatformConfigBundlesList:
        return typing.cast(GkeonpremVmwareAdminClusterPlatformConfigBundlesList, jsii.get(self, "bundles"))

    @builtins.property
    @jsii.member(jsii_name="platformVersion")
    def platform_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platformVersion"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "GkeonpremVmwareAdminClusterPlatformConfigStatusList":
        return typing.cast("GkeonpremVmwareAdminClusterPlatformConfigStatusList", jsii.get(self, "status"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__db10d2ba99af6b2e5f9d5e770e51406052f9b310ad5ed491c6c0f75edd49cb6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requiredPlatformVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterPlatformConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterPlatformConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterPlatformConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaadd39bf583c3c87e9618fb658948054aab52885fb470010ce0c305a66af824)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterPlatformConfigStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremVmwareAdminClusterPlatformConfigStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterPlatformConfigStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterPlatformConfigStatusConditions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremVmwareAdminClusterPlatformConfigStatusConditions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterPlatformConfigStatusConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareAdminClusterPlatformConfigStatusConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterPlatformConfigStatusConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62faf00f3472671e48ce83b2a51c7537eb174847808bd4bb4c64f723522c07c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareAdminClusterPlatformConfigStatusConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a43ac3c05cbdbb5de8631378a2845197161e0600092802f6794122eb006a0d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareAdminClusterPlatformConfigStatusConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d71f5b3d2ac379c96f006967e143e4ca8ef3f6a732613f045a9c2e71e02ad1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fccd054bff4c014d78399d1c7b4040203038c696bb77bf749f033527f6fe9e69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7823e8c00e84da5c3eea8ddf2dfc580864027af0a5b342bca4711a4dff29f697)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareAdminClusterPlatformConfigStatusConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterPlatformConfigStatusConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__198da0d13160098f98a09fb5f4d88f60be186bc5108f4565632cd4629426ea98)
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
    ) -> typing.Optional[GkeonpremVmwareAdminClusterPlatformConfigStatusConditions]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterPlatformConfigStatusConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterPlatformConfigStatusConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79e038b51174983eea636b65d77beab8d79834b226201c8fda1d12c95ead7cd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareAdminClusterPlatformConfigStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterPlatformConfigStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c69846d05edbd7f3bdcbc79859c2330f351881e5d09197d7633b59809f96058)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareAdminClusterPlatformConfigStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60986cd94a9cfed4f858e3a98f4eaf1cc8bc81135130e83b129f5132da9658cf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareAdminClusterPlatformConfigStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dec02e364bfa12ee5bbd86dc4e34765b6b63f99914cbb178a6548f47e803783)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb8141c6e0c5533e9d1ddf33e5c13335ccd7182936a2b4fca6e0c1e53e2e19b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87b355cf517e67835c2a329320d01fe0e74ef4531745d7fc6ffa4db43c7c3ae9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareAdminClusterPlatformConfigStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterPlatformConfigStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74e616a31b67cd9436e91641911b399dfb0303353dca7dcdc3b09bca22c0d19d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(
        self,
    ) -> GkeonpremVmwareAdminClusterPlatformConfigStatusConditionsList:
        return typing.cast(GkeonpremVmwareAdminClusterPlatformConfigStatusConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterPlatformConfigStatus]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterPlatformConfigStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterPlatformConfigStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40278e4831bd1d2a5e7481d4c61f2b9f3ba4ca9b24f4a6a145c540cf66f36777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterPrivateRegistryConfig",
    jsii_struct_bases=[],
    name_mapping={"address": "address", "ca_cert": "caCert"},
)
class GkeonpremVmwareAdminClusterPrivateRegistryConfig:
    def __init__(
        self,
        *,
        address: typing.Optional[builtins.str] = None,
        ca_cert: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: The registry address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#address GkeonpremVmwareAdminCluster#address}
        :param ca_cert: The CA certificate public key for private registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ca_cert GkeonpremVmwareAdminCluster#ca_cert}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdf3313ff462938c721dfa0a8254f77b699d5472af425310f4bf242e50d99a03)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#address GkeonpremVmwareAdminCluster#address}
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ca_cert(self) -> typing.Optional[builtins.str]:
        '''The CA certificate public key for private registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ca_cert GkeonpremVmwareAdminCluster#ca_cert}
        '''
        result = self._values.get("ca_cert")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterPrivateRegistryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareAdminClusterPrivateRegistryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterPrivateRegistryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdff9a3a7769d23b7cfabba00d2c5985f54a16b9189e39443e40968df9945c7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78d1388227f5ab20ba762c73b0e0aac0841436c13ae46efb9274fca9f822399b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="caCert")
    def ca_cert(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caCert"))

    @ca_cert.setter
    def ca_cert(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0710f6e2e36bc7bc91501a7b3a4a76e26decdf7fab493e1038fa4080a607671)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caCert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareAdminClusterPrivateRegistryConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterPrivateRegistryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterPrivateRegistryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67fe37d1253efd18ca436ca7c789bfe0de2c7a25394a180f085847a15ac32444)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremVmwareAdminClusterStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterStatusConditions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremVmwareAdminClusterStatusConditions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterStatusConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareAdminClusterStatusConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterStatusConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d99cf9378b85bc6d7cdbf6e061ea72db8b18ead86bb046b9f3c9047976d30524)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareAdminClusterStatusConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cb7ee2d0c41f579ae5bccfe8ae5d470e6e42ec3a6cb59b630026e988ceb2b1b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareAdminClusterStatusConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a15ab719d1badd07b288891d41d38b19c2a79e6450b0ed2bc15a8610ea95ba9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa0b94f1c54948cceef7d838b9311d41c51430e25c5d3b4d26704b5c1aa14650)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac1bff8be972ebb2818d4d7d974e23ee14b410058450c75c597b9a9bfdfc2da8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareAdminClusterStatusConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterStatusConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__157aa6569a0466d6a5a01bbf81c6dc6029ff43cf0f7a9098250068d7e96d1c06)
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
    ) -> typing.Optional[GkeonpremVmwareAdminClusterStatusConditions]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterStatusConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterStatusConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bff500b583e2bc3eeb286ca4b78cc192fc6556b507ec93410e32e430d3b54393)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareAdminClusterStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52945818b37cab56c308818f84ac38430b4a4ed685421e08dc4ad8ee9c4503c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareAdminClusterStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2025dd8413412ad6d6efd5349f6ee4a2c13ba9ea9abb8b6f788ebf65cf79f91f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareAdminClusterStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0909b51fe876dbdf19f1853412fa63d640e7ada7ed5b6debe24986d53fdfbf10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c45f67b848fc688e0d39cf1f8975eec32843244a45f7cc948d524eeaac19eac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__359b3130b4133b814cebde9942a08058b538f1fc0064e5732c662a5ef7d4e470)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareAdminClusterStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fe08e0df9769b32049eaf3b79a50b74a0c3dc2a8047c468a93f8189bbb23754)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> GkeonpremVmwareAdminClusterStatusConditionsList:
        return typing.cast(GkeonpremVmwareAdminClusterStatusConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremVmwareAdminClusterStatus]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89d40a69bc4497a13f44ead25b41d2009667133f7cf5efaadb11fd1a965d61a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GkeonpremVmwareAdminClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#create GkeonpremVmwareAdminCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#delete GkeonpremVmwareAdminCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#update GkeonpremVmwareAdminCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17ee5e223600f07a8d03ec2fea357e426237d717e188f711e5df0f2db2469dd9)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#create GkeonpremVmwareAdminCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#delete GkeonpremVmwareAdminCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#update GkeonpremVmwareAdminCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareAdminClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__552894e0e58ddeb9a8cd03f2de875b86eb2f8c9ca5da1737f3000f29deb0c06e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__082348f9e76b1c6c4b73df70d8fc0d5d1a02a35cc30a344a02a4446ce396d5f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea19e37a55949c4d42178841aea51a6ef12e7af83f43fab8a2dee0d3ba8186bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa4cc5a4bf28fb99220766594faccf749aece1160b30a22fbd661c16a01f0f17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareAdminClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareAdminClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareAdminClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cd3087a87f89acacf46d244c25c02e41c565971a679bcd91b3938cc2312b512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterVcenter",
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
class GkeonpremVmwareAdminClusterVcenter:
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
        :param address: The vCenter IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#address GkeonpremVmwareAdminCluster#address}
        :param ca_cert_data: Contains the vCenter CA certificate public key for SSL verification. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ca_cert_data GkeonpremVmwareAdminCluster#ca_cert_data}
        :param cluster: The name of the vCenter cluster for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#cluster GkeonpremVmwareAdminCluster#cluster}
        :param datacenter: The name of the vCenter datacenter for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#datacenter GkeonpremVmwareAdminCluster#datacenter}
        :param data_disk: The name of the virtual machine disk (VMDK) for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#data_disk GkeonpremVmwareAdminCluster#data_disk}
        :param datastore: The name of the vCenter datastore for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#datastore GkeonpremVmwareAdminCluster#datastore}
        :param folder: The name of the vCenter folder for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#folder GkeonpremVmwareAdminCluster#folder}
        :param resource_pool: The name of the vCenter resource pool for the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#resource_pool GkeonpremVmwareAdminCluster#resource_pool}
        :param storage_policy_name: The name of the vCenter storage policy for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#storage_policy_name GkeonpremVmwareAdminCluster#storage_policy_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15995ab5818a40b47623fe05320fb8008ddd3996923d77780f7e185ee3fab40a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#address GkeonpremVmwareAdminCluster#address}
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ca_cert_data(self) -> typing.Optional[builtins.str]:
        '''Contains the vCenter CA certificate public key for SSL verification.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#ca_cert_data GkeonpremVmwareAdminCluster#ca_cert_data}
        '''
        result = self._values.get("ca_cert_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter cluster for the admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#cluster GkeonpremVmwareAdminCluster#cluster}
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datacenter(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter datacenter for the admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#datacenter GkeonpremVmwareAdminCluster#datacenter}
        '''
        result = self._values.get("datacenter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_disk(self) -> typing.Optional[builtins.str]:
        '''The name of the virtual machine disk (VMDK) for the admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#data_disk GkeonpremVmwareAdminCluster#data_disk}
        '''
        result = self._values.get("data_disk")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datastore(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter datastore for the admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#datastore GkeonpremVmwareAdminCluster#datastore}
        '''
        result = self._values.get("datastore")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def folder(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter folder for the admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#folder GkeonpremVmwareAdminCluster#folder}
        '''
        result = self._values.get("folder")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_pool(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter resource pool for the admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#resource_pool GkeonpremVmwareAdminCluster#resource_pool}
        '''
        result = self._values.get("resource_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_policy_name(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter storage policy for the user cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_admin_cluster#storage_policy_name GkeonpremVmwareAdminCluster#storage_policy_name}
        '''
        result = self._values.get("storage_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareAdminClusterVcenter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareAdminClusterVcenterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareAdminCluster.GkeonpremVmwareAdminClusterVcenterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__adf2f4b3255007196382366841f98ed1d585d7753377a42c850c971a5a5b5ba6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__512e1e804f6588332d59e28476f1a5610312e44734aafe2b1d1a42a0f7087983)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="caCertData")
    def ca_cert_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caCertData"))

    @ca_cert_data.setter
    def ca_cert_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed9e70325864fe634533fedd5c66fec02d4347544aa96d3ed77344778f55364d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caCertData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e88eb7fa226caa556cb785ffdb5642199c9607cad95417723671863bc08be7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="datacenter")
    def datacenter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datacenter"))

    @datacenter.setter
    def datacenter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c15d55eed9e5335bef842fd75d0bac5af1da7ea1713321b0fb7254840e86b876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datacenter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataDisk")
    def data_disk(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataDisk"))

    @data_disk.setter
    def data_disk(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c23a9e5a929dad1566285219ae29f1d501a42c4ca41afcb4086caac7b335795d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataDisk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="datastore")
    def datastore(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datastore"))

    @datastore.setter
    def datastore(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d43ecb6e6005b3630aac2abbf1d929d80a727f6866620e72f7955c154d092da9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datastore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="folder")
    def folder(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "folder"))

    @folder.setter
    def folder(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84d1a6bdd8dbbfeeba8062389d26793ac4e8de1bf46966f331066affb56522dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "folder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourcePool")
    def resource_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourcePool"))

    @resource_pool.setter
    def resource_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1be2ee1da6a194f9f7488babc562f43eb28fe36f4bbcc6a6504b382a309f21f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storagePolicyName")
    def storage_policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storagePolicyName"))

    @storage_policy_name.setter
    def storage_policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8392fb96961a739c25bea344575da3223c8f578903396fef321e0d865c13d711)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storagePolicyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremVmwareAdminClusterVcenter]:
        return typing.cast(typing.Optional[GkeonpremVmwareAdminClusterVcenter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareAdminClusterVcenter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__033182f0b8c118b5f952ccf81fbb7eb79fdd1b380a45da3193dc3fdd5bd77474)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GkeonpremVmwareAdminCluster",
    "GkeonpremVmwareAdminClusterAddonNode",
    "GkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig",
    "GkeonpremVmwareAdminClusterAddonNodeAutoResizeConfigOutputReference",
    "GkeonpremVmwareAdminClusterAddonNodeOutputReference",
    "GkeonpremVmwareAdminClusterAntiAffinityGroups",
    "GkeonpremVmwareAdminClusterAntiAffinityGroupsOutputReference",
    "GkeonpremVmwareAdminClusterAuthorization",
    "GkeonpremVmwareAdminClusterAuthorizationOutputReference",
    "GkeonpremVmwareAdminClusterAuthorizationViewerUsers",
    "GkeonpremVmwareAdminClusterAuthorizationViewerUsersList",
    "GkeonpremVmwareAdminClusterAuthorizationViewerUsersOutputReference",
    "GkeonpremVmwareAdminClusterAutoRepairConfig",
    "GkeonpremVmwareAdminClusterAutoRepairConfigOutputReference",
    "GkeonpremVmwareAdminClusterConfig",
    "GkeonpremVmwareAdminClusterControlPlaneNode",
    "GkeonpremVmwareAdminClusterControlPlaneNodeOutputReference",
    "GkeonpremVmwareAdminClusterFleet",
    "GkeonpremVmwareAdminClusterFleetList",
    "GkeonpremVmwareAdminClusterFleetOutputReference",
    "GkeonpremVmwareAdminClusterLoadBalancer",
    "GkeonpremVmwareAdminClusterLoadBalancerF5Config",
    "GkeonpremVmwareAdminClusterLoadBalancerF5ConfigOutputReference",
    "GkeonpremVmwareAdminClusterLoadBalancerManualLbConfig",
    "GkeonpremVmwareAdminClusterLoadBalancerManualLbConfigOutputReference",
    "GkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig",
    "GkeonpremVmwareAdminClusterLoadBalancerMetalLbConfigOutputReference",
    "GkeonpremVmwareAdminClusterLoadBalancerOutputReference",
    "GkeonpremVmwareAdminClusterLoadBalancerVipConfig",
    "GkeonpremVmwareAdminClusterLoadBalancerVipConfigOutputReference",
    "GkeonpremVmwareAdminClusterNetworkConfig",
    "GkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig",
    "GkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfigOutputReference",
    "GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig",
    "GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock",
    "GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps",
    "GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIpsList",
    "GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIpsOutputReference",
    "GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockOutputReference",
    "GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigOutputReference",
    "GkeonpremVmwareAdminClusterNetworkConfigHostConfig",
    "GkeonpremVmwareAdminClusterNetworkConfigHostConfigOutputReference",
    "GkeonpremVmwareAdminClusterNetworkConfigOutputReference",
    "GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig",
    "GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks",
    "GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps",
    "GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIpsList",
    "GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIpsOutputReference",
    "GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksList",
    "GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksOutputReference",
    "GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigOutputReference",
    "GkeonpremVmwareAdminClusterPlatformConfig",
    "GkeonpremVmwareAdminClusterPlatformConfigBundles",
    "GkeonpremVmwareAdminClusterPlatformConfigBundlesList",
    "GkeonpremVmwareAdminClusterPlatformConfigBundlesOutputReference",
    "GkeonpremVmwareAdminClusterPlatformConfigBundlesStatus",
    "GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditions",
    "GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditionsList",
    "GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditionsOutputReference",
    "GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusList",
    "GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusOutputReference",
    "GkeonpremVmwareAdminClusterPlatformConfigOutputReference",
    "GkeonpremVmwareAdminClusterPlatformConfigStatus",
    "GkeonpremVmwareAdminClusterPlatformConfigStatusConditions",
    "GkeonpremVmwareAdminClusterPlatformConfigStatusConditionsList",
    "GkeonpremVmwareAdminClusterPlatformConfigStatusConditionsOutputReference",
    "GkeonpremVmwareAdminClusterPlatformConfigStatusList",
    "GkeonpremVmwareAdminClusterPlatformConfigStatusOutputReference",
    "GkeonpremVmwareAdminClusterPrivateRegistryConfig",
    "GkeonpremVmwareAdminClusterPrivateRegistryConfigOutputReference",
    "GkeonpremVmwareAdminClusterStatus",
    "GkeonpremVmwareAdminClusterStatusConditions",
    "GkeonpremVmwareAdminClusterStatusConditionsList",
    "GkeonpremVmwareAdminClusterStatusConditionsOutputReference",
    "GkeonpremVmwareAdminClusterStatusList",
    "GkeonpremVmwareAdminClusterStatusOutputReference",
    "GkeonpremVmwareAdminClusterTimeouts",
    "GkeonpremVmwareAdminClusterTimeoutsOutputReference",
    "GkeonpremVmwareAdminClusterVcenter",
    "GkeonpremVmwareAdminClusterVcenterOutputReference",
]

publication.publish()

def _typecheckingstub__673a0031ef1cf98ceb08d0a1c77119edd30db3ee3b5002d4dbe4e073bdf398a4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    network_config: typing.Union[GkeonpremVmwareAdminClusterNetworkConfig, typing.Dict[builtins.str, typing.Any]],
    addon_node: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterAddonNode, typing.Dict[builtins.str, typing.Any]]] = None,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    anti_affinity_groups: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterAntiAffinityGroups, typing.Dict[builtins.str, typing.Any]]] = None,
    authorization: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_repair_config: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterAutoRepairConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    bootstrap_cluster_membership: typing.Optional[builtins.str] = None,
    control_plane_node: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterControlPlaneNode, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    image_type: typing.Optional[builtins.str] = None,
    load_balancer: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterLoadBalancer, typing.Dict[builtins.str, typing.Any]]] = None,
    on_prem_version: typing.Optional[builtins.str] = None,
    platform_config: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterPlatformConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    private_registry_config: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterPrivateRegistryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vcenter: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterVcenter, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__1ab7dd11b72e7a215e428d53840dd559b931b93bf26aae84f706b6c580a974f6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__715624e290ade7fcd4efb8af441a1f475bb175b4a0ee6c212fe5e2a217b3326b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef186ef01b8bcb848e9ff4ea44412d2804b8a605a04aa578dbb555f670e29091(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2440816f6ad63936af6115c7f08b4d9b2274b7e26e757c3784ee3a432bc7105c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2145d29940d34805a9a917cb229a7ac7f0b3adfdc8c1aab8ef0c7090183f12c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__102f0f38d6d07ff98065b2ab67c311ba1e715aa4f501c8cef72a8d23fa781761(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__959224c3688f7b0744a0e54b695870fbd6bb95563e5af995835a1679cbc1aa2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2eeecb5b924aedef0f113f6bbbe226262d464dba65cde4c5e30f6f161e8758(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9913d13adb844deb509594228847965ee1421ac19453fcfa828ba46f0bb53409(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baf0d45226964da302433fcd88610dbfc3ce087366bb280c225da6a5d45e6e64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0eea16e510f79275461eee2762c7e139831e4f5a84c18e436d55cef3a4ea250(
    *,
    auto_resize_config: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8734eaf195ee778426c58ef86cd995aa664ba427c3b6cb3e81e7fcdaa0fed21(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8106426b3cea5c3554df7287c7e108ed1df8a2e8b0203279590c0b8cc4b10c8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83afd72f5508725f57fd165b1bd9af0d32d2133dfb7676d78379c6c04323865(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00cb5bd3786d59be2b37f50312e778e7d39abad46e936eadcde81bf84d500c32(
    value: typing.Optional[GkeonpremVmwareAdminClusterAddonNodeAutoResizeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f71259eb77d7c0e261c92c6a031ec8bdfacdd91ea649084e7fc75d00164ec0c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acb68f2c9a03cea1c406ff0c3c65b95716e8bb1a3336c5119d15de01ec0bb53e(
    value: typing.Optional[GkeonpremVmwareAdminClusterAddonNode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567b53519794edbf4fefcd3ee9b0dcb415814d0ee6776292c3672403bf7e23b2(
    *,
    aag_config_disabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0e5b3e33e6242c3310940404f139dcb10c490747449d8e7867f8f6b55af204f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__066a74874513bd66aaff19815c4fe4e7582318e299ef74f74584b51e9018ccbe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e45dca08fc5922a5e148365c24810462a2906d0250f14ae186691abcc2862a68(
    value: typing.Optional[GkeonpremVmwareAdminClusterAntiAffinityGroups],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebeaedbe974c3a5e159d1ad570b9d6c46bd1c6bb6eefd5ab461d6cf51b2c3352(
    *,
    viewer_users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareAdminClusterAuthorizationViewerUsers, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96707cad6ee4540195abec4482813636e28cd5f9fe0f8872da4cc05b36320ca8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45983a0a7f740697f8324787ab55b7bb9fa268512cf4af9a071329b60b1f301f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareAdminClusterAuthorizationViewerUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3be79b30461ed079c17ddab6d2b469d011965a8661894481bd04b391bedd7c7a(
    value: typing.Optional[GkeonpremVmwareAdminClusterAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69add56521f14ef2f4618fe37d5e93aab959b599de540abbcbb33df3b916ea5d(
    *,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48b56182c6df673642d4aa6a2993983dfc4b2f194cb2509c5cd5922c361fd81b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce066c920c72f467246d4613a8a09e33687bd72afabb76f5122ec2985f23d05c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f01e053685a576442ab3adb202ba042432c75d49628ef181b9135aaf25cc1ab7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__568c6cda8b1c0a81c098312ac41f1bfa1567107d46a7b26dc5415c6d73069852(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a8efe53603b8d7981f09066a3b2a30bb0614fd1da45ec0d8930541f874ae922(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__832b1be76c68bb8ff1d0780d0473efc664db4bc7960b053edd9c307833d1e138(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareAdminClusterAuthorizationViewerUsers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__485053e10492ddac83988152daca87b38da80bab4cc24d7a5053170cadec926f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab2d7161371dafdbfcbeaf451423f52e17d24919032ce1ffc972285b0cec0c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a185210e05af8a4249aadcee9b2ad594ba066ac779b8a8da6ccf95da2260f34d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareAdminClusterAuthorizationViewerUsers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd4b54b50dbb3d670b534a0ceae211869b52499ee526c1fd130f1e633db6a233(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba06f7dc22dfa4d7e8ed593b304394539cdaf0ec1e608fd883e9ecf401ad2e4c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca7c8ee423e93b2e55c6367b2ea8d2ee5dbfde8cc3d7b437bcaccd195a32f6b6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__035f2c4c06f953678d235f7aa45b32eb94c7948efb98517d740db2d543e46d34(
    value: typing.Optional[GkeonpremVmwareAdminClusterAutoRepairConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc915f2c6b82352f149dc2cebbaa970aef102a7aba321dceaffd98c160589225(
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
    network_config: typing.Union[GkeonpremVmwareAdminClusterNetworkConfig, typing.Dict[builtins.str, typing.Any]],
    addon_node: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterAddonNode, typing.Dict[builtins.str, typing.Any]]] = None,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    anti_affinity_groups: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterAntiAffinityGroups, typing.Dict[builtins.str, typing.Any]]] = None,
    authorization: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_repair_config: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterAutoRepairConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    bootstrap_cluster_membership: typing.Optional[builtins.str] = None,
    control_plane_node: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterControlPlaneNode, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    image_type: typing.Optional[builtins.str] = None,
    load_balancer: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterLoadBalancer, typing.Dict[builtins.str, typing.Any]]] = None,
    on_prem_version: typing.Optional[builtins.str] = None,
    platform_config: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterPlatformConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    private_registry_config: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterPrivateRegistryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vcenter: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterVcenter, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95fccc5c2c65edfe1e04b0f989c2f4dba32f0aa33324646b86c41e85ba636ccc(
    *,
    cpus: typing.Optional[jsii.Number] = None,
    memory: typing.Optional[jsii.Number] = None,
    replicas: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b6df98b030c04c3905dbd7eed1e5aeec60b56da857a9fdaeef62eb35870281(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f203680a1f5f7a9653f0328fed7629df02e9b6af42c9ec17e463a3c1957f5bee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__642510aa39b4b4481ca35cd0e0bac7df4b6c1081551147bb0be9513e2f7cc5d5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e996d322f169b45d0841ef191190aac6ac9b7c9a943371f44ceaa604673cfd4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9deba1f7137b275f181a1eb87e41267e3a8637b824f07b37e5762a604e5406(
    value: typing.Optional[GkeonpremVmwareAdminClusterControlPlaneNode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edec75f7c9c96faae110b3517af4eaf029dd632ddec1790d10796b6e7e2afe4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e75b2d957fafeadc1671f4e5c8e91ebc870dc0d9d4b40429885e9d2fb984d0df(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b802d02a5cd16dcf11cb325f044b6228c16947a65b73c1fe6b0dff42c6ee4b6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c43e36a4ae551790f77e524d9dbf685104c2a2b75e2e80f748c735964778f8b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93dc00157ddcabda7d28833d0509a6746e1bbdcdc506bda445250f43eed94dfa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12154629f4f532d4442772a6e50971ea325d9c928f94fce5e08413923340c556(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57ee4ca84927202eacac09d0c4b71828b544e98f2ef1ca4da3ccadfb6bdc5497(
    value: typing.Optional[GkeonpremVmwareAdminClusterFleet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ac64c927de04ce28c789d0efea1d2cf2a09d162d00780d87c7acb8fe340f271(
    *,
    vip_config: typing.Union[GkeonpremVmwareAdminClusterLoadBalancerVipConfig, typing.Dict[builtins.str, typing.Any]],
    f5_config: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterLoadBalancerF5Config, typing.Dict[builtins.str, typing.Any]]] = None,
    manual_lb_config: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterLoadBalancerManualLbConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    metal_lb_config: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a689230e25f3f9553e707acdaf1c10c617efb3e1af0d7471b37b003c8335926a(
    *,
    address: typing.Optional[builtins.str] = None,
    partition: typing.Optional[builtins.str] = None,
    snat_pool: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5bf5e739bfa44f7254693fc734558b724252b5b7dde67844275b34ef831ab7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7d4f4625a7e7ed14017cfc808a664f97a93e44edb34ff72cf7dc036299e8d22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0534f0a6dfe128461e95dd94ae675aacfdf03d4737f9b668b99f64abb588e83f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dc6fb2304d464c906a1b24e5cd98d3801e79bb7e51f1ee122441b37a7057026(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb3b4783d182ed2ca6cd5cfebc4ffd7086faf471cd4987609e6155a487db25b(
    value: typing.Optional[GkeonpremVmwareAdminClusterLoadBalancerF5Config],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb0849721409c447107eb769fb08626e01d5be794957d3afff9263d84c11a09(
    *,
    addons_node_port: typing.Optional[jsii.Number] = None,
    control_plane_node_port: typing.Optional[jsii.Number] = None,
    ingress_http_node_port: typing.Optional[jsii.Number] = None,
    ingress_https_node_port: typing.Optional[jsii.Number] = None,
    konnectivity_server_node_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39099b3abdafdf66b850c8b7084052e38c15814e4d21bd0531cae79f763c68f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f54d0f713bf0648007f46b37d229b95503a9890b4a2c77c9f49bf8dfa91dd653(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8683265b13fea38b32b1189e12680845f8999508122347e801af162dd7def7d9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8675f73a666ef488c10ef184547ad685cae68a7821b1d7312bd6596a702c97a9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f78493a187aa93f89f88f1056d013b3867b59e600be984f1d1e9b8419d4d372a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f99d165ebe89058b23b1ac8c18f1d8b3a513c2bf982d079bf3c60b2e9708b55a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adabcde8f8ffed6dd1d3a692f9fbd95cf2c9c2db4b2da18663d7ddb59e95ccfb(
    value: typing.Optional[GkeonpremVmwareAdminClusterLoadBalancerManualLbConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32478c3a4d7d29855ae9149cc0fa699ae2dd1e542b28f77a8194cc309108fba2(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__671002dd629094d0f96d72b9f2fa09f8c6e2b498f1d43433ada85c2e4c526bae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c86878fd6fffbdcdb567afd0792b4f94a5aa19f2c91cd65a72a996dd448f1576(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__582dae19b687aa3787c5d8f704cbd350e97ab2b7a22445a9ebe30786d9c437bb(
    value: typing.Optional[GkeonpremVmwareAdminClusterLoadBalancerMetalLbConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3433999d6bedbeb8f0df9d8c59a414df27eeee4b5910ad31252b6663a5e85212(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4198af4fd601fc164919bf09038b5769da6bf38818b31d18055ba426d9f6961(
    value: typing.Optional[GkeonpremVmwareAdminClusterLoadBalancer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0bc3806131338b02144f598e75e1153e244c3d3010d36997cf4ef1e8fb22cb7(
    *,
    control_plane_vip: builtins.str,
    addons_vip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f5d2a0b87e2e96c2faad701ccf3ff8e3d4e75302dc1e3fd98995c499a161e04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b78f2468a6f18b560178a2edad5096bef17401597d4a981478473d56b45a76ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c7271e6be10946c257604019464350390c895249429f1953935f08ed1761a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90d02e858b1fc21abd8355074d43c162e799a07d52a9b3fe499371bb947aefb0(
    value: typing.Optional[GkeonpremVmwareAdminClusterLoadBalancerVipConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ee7bac7159d4286e9bfd1c30197994b6c3006f9c82e057d7c29302f60b7a3e(
    *,
    pod_address_cidr_blocks: typing.Sequence[builtins.str],
    service_address_cidr_blocks: typing.Sequence[builtins.str],
    dhcp_ip_config: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ha_control_plane_config: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    host_config: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterNetworkConfigHostConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    static_ip_config: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    vcenter_network: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e1fca293bc7bb83345244abb4b3b3ff36eb26ce93d73bbd4c6bbdfd0d75b9d(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbe091ccb341fe8de3949f92b89ca305421f2aabf8f2d4b1b405d65c00037967(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5751c0a32bcd50cc2d55113472f98e61d3b920af9434d95427ab614a78ac93bf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cca1f77382cf6f0ce1a57e5e1414907dfb1902f8ce922854305b76de8a9dec5(
    value: typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigDhcpIpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5672abdf63dc728bfc10fcc8db94b18eb382cc2ce985fbc5110290c5f00da9a5(
    *,
    control_plane_ip_block: typing.Optional[typing.Union[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6645a056d24126f37f38894649f3fa45571ec2e3bc87aec00ced184c58eaf1d6(
    *,
    gateway: builtins.str,
    ips: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps, typing.Dict[builtins.str, typing.Any]]]],
    netmask: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77bc0bf570d44974eb09ecc68315b57257e576f45180a74cd6fb5eee0f2fb012(
    *,
    ip: builtins.str,
    hostname: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3cae63e147b983ee6f4591aac2fbbc24a5b3a72613c47247565ff0af365f3b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce0ab3f11e8667133382a79ccf933233533aa38fc3a36c78741e29efa12d2b91(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfa93e975e3b84816cd4592e458b66ee3e42d52ef504d9504ef49984379cb87b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea57b988edb23ddad8c8e6530e03631a96d4ecec21b8c25555e0a85034532ca7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2824b71230112a22f824f883ac3cabe70dd13bb7f4f200a0d0a811916c3fa966(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b4754655dd73d3b2f2599dacb4dc73e09e6cc36d445864d3895c1aa9f16d914(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fcbb7dde2ddc0c197072e1adf8044db641f0187a5926ef85dc7e98cce60e9e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eff5c15496b582dd53cf055fd4fb11d75f25f62f472df1a53b9f367c63bf9ddd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__661bd1e7a55b10bb581993a8d532504eb71b8a206190b17695b1469129f59813(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f19172b2cdf0f3346c985e4431511cc0003405b616ab6cfe476f8fe23fac54(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa7b4ecc39ad3a9ae545cc3e8cf121a046e5d4bc5770a37a95614d62f696784c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e4d0963747a4555ea246de1cd50261451322faa0bd5a4fbaed2ac66e7a497ab(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlockIps, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c286a57c42218ee5346bea64a2703b4b5525f591840e3f138611e483969e941(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aec27409e3d134bb50b15c573a43542a25dab1f88fed51592e3705c24fdfc00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48be2129214df7497b96d191b737365892e44c025870ee5f7b3b87a65aa6082a(
    value: typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfigControlPlaneIpBlock],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f555f99d36c1a5f4ba81187d9933389a0679c5bc1087fb5d61f487e5e17c60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3cda0c5f247389fdbb7f8c0b9e2e303b5f676c7c71c65ab025db04e6dbf5ade(
    value: typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigHaControlPlaneConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dcd67431b8e62c2f0e7745c10a125410009d8c449b45ac9f4f5613f0ebf06f8(
    *,
    dns_search_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ntp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cbd4afb40ed5e79dcc901a678d00db334429a61911694d3423ad09346ff6c15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c499ab75998e61de2e3774036a0109a00b71c94c8e438d864277394df80c458(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc0d999460e29c7c96d4b785a8087cbef82fa54c66fadf4a38c0eb3c9d4db153(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52468504d2ff121a9bef07a84cd4dd6d9912624ce0e5e675401cd817e1dbd0ac(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d7d136dc1295d49f97bbb56c5355bcc5b66c7462df4ffe6b31bd86ab66e1fa6(
    value: typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigHostConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26d5acf60543142541d830911d265087bc7ac08853324d73e0b8d8c4a6331f36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8f32a35912b38d4d16a672bb631fe5f96b4d40680f8f48eaf74813acaf70629(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__510a3cb4c82c41c4a877c5ea841afffa75098055a36b23fcde97e9eb68111d65(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcf4f47df9bf63ee468eed7bc6ce2ab11eb18c8bf40f34ae5d8ac8e7cac34aed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__924d1ca203567c4ff8e79cfcf577010d16a738aa8b112aaec244fd887dc486ff(
    value: typing.Optional[GkeonpremVmwareAdminClusterNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c59ad611d306285e360e05c4c7541655d367c71a335c199a3c1c125d692fda8(
    *,
    ip_blocks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3c802a23366b62807e78b6e27da77038d55980d70d0a42fb8a815c902a01581(
    *,
    gateway: builtins.str,
    ips: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps, typing.Dict[builtins.str, typing.Any]]]],
    netmask: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1546a0bb7d3dd39b31687295501357a633c85afe11afd75f0a9b765490ef3452(
    *,
    ip: builtins.str,
    hostname: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e689a0803b4b76b5a5feebffb127f7d43108ae80255dc008c52315d3de27109e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa5e4ffbdd95d5d1e65021ae879409e1a2011114c946f1c90a14b8dcb3a5bf2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9ccc023fab67830a52f50f4a79b6da38252c44241e44cd9dd33894dba3fc6bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6fc14e54a0e19f88052f8bdc39829b719691f90d2c4a6ee4cb39809f551aff5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a24203912165086ecca6b1d4bff0ff33b401e17ca6ba000af99407471622916(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__435c5f92b11ef7dba51516c30ea33c19be75edd90401231d769237f562f16d6b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba729e6054daa95ce9205687f7a4138de0b3522e5850c5e2e353b840c2060678(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f19854b2dbe3e73a6c22bbabfdda11d360d6567f2afea2f558b144cda7ae6ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3247b6999f1b4aca5d850f18f4a4f81de867f2d3bdcb6b463a02b5f2882f71c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78bb2434a3ff4b9ae1a1a03d920508ab2471c0ff1c1ab1cab569b59f0286923c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d26fba0300fb10a2b73f55e98f1c73233b744e1dde7c74ce924a93e089b3b7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e572f29c4c8b4ff0b7418d93736e20e670fffe8af21446c2aae91fc3db517810(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6fe75a8773d0d0b70085534e3eb0b910adee087b7d51a60b67cae25efe7a676(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211163680ffd95e1b1c1868422163acc8869521e80ee923a74af6e4b2e306e99(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c73d9f604a3e1a8733a9795b2f4a4b3f0cc70a1acc2e9f8786ea448ef354cb9e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edc5ab74583376400f7b3e029fb1e1fea26f9c7073b8534f7240e64934228203(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cadf63cffb285b8c89ad815248795a13e9fc2ca581c09069642f9584a646493c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd203ac1eb2656edebdc714dafbd2478726b6d0c4f05025b6eec393eeda48e9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocksIps, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cfeeeaeb227179d1edcadc0cf2fd94dba153f508329437f612ceca1e47a4310(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e77d7aa1bfec7137453c12d766348155a104f6b493908d6769eebd095e6d6d0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd69121db712be98f732a9f42d05a6823da0c2f60349103105b96d45d0f65381(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f839863beb0059860ee1d5fb2c0fbe00860a1facdf8eb0f3c01a31c40d819345(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce60ff4ebc4899553f401070abce8767b73ee195fd444b7a42ff91ec61ebe246(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfigIpBlocks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05da628900d941c05d94c9da01b0358cb6c755424d0b5dc3f2c688dc54263d1(
    value: typing.Optional[GkeonpremVmwareAdminClusterNetworkConfigStaticIpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__895158fa4d0979ce1ce30b233f06225098ff63b89112446cdd2c9467696b9629(
    *,
    required_platform_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d60a2c55818884639a107c1a96a60d559b90b6edb0d5bbff153b10bf3c8ded(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc87a3ae9b187578af0b3f96e7df93cc986af1ce9b394a736be9e6380c6756f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4942bdef44aff9753350a41b6b9e426a001e39a1bdec2f99976f4ee176d4565(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb32b3df60b3908092f689b7fca35cdc34f4ed3b74bcf0b77b50a1d79ef9e565(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b9f3b7c9b165fa5e3981cad65864ac1f330be4d85de32fbfb95f077cb12e060(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99792cd246b2cba69deaf8ee5badd2320d143b4406b4523ecc24848636efdf14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b062b6511e36c8767993c5033045d52855bd829cc67486fb5948370fcd45aae1(
    value: typing.Optional[GkeonpremVmwareAdminClusterPlatformConfigBundles],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1dc59f6224f3b8bf7fef4a166cdf9e5b7e98fa684017506819e5f7e69b90186(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__badf8156eb1532769e2faa8d9ae626331129b31f4f8c5fcb7283efb8ea792781(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74cd105eeaad52f103e9a2b4fe0cc0505173902996b48798ca1dc7c73fc88a02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e36605c90776643b010db11af405bc8bf9f99c8dcecc77bc5005d4c184b949ef(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67811f5adfa1299a42aa5b16f31766bdb31714aac65dfbbb0839ab6e102db60c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1b7983d982afc2882f6bd79ddfb850d89c7d9c819a24152810f88fa27b4edff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4674b771a3f778296d75d1c2c5eff15beb5730d3b90271ffdf05722d6bead32a(
    value: typing.Optional[GkeonpremVmwareAdminClusterPlatformConfigBundlesStatusConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1ed1bbdfff969f34ab802eab3b8d97a240968f40b38624194eabd01b110687b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2735415446b72593d87ccded87860ac92b00ea48e0961a7de3567b8e5e6b947a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d967307807fcafd0c25006867c5643b7b78035d25958f57857a4b230ff545d95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a94833fc06b6277a1de207a6ae8c96d8fe02d2703a43f659d71848d744fcd15(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f28038a80816a3a2e045c94815dddf9cdd33cf1c9d1adc5f2fb0b72d5dbb7b9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db31ddad428fcc4690ab5c9246fbacb625fd89bb7b1e1005a190aef7c1a8672c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bd80f6dc74e50220090ad70b7ae418552f56ea9bef246f1075bf91433248fa0(
    value: typing.Optional[GkeonpremVmwareAdminClusterPlatformConfigBundlesStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfea9ebaee2fd15eaf03a5df582134b532b781c913760d931ca8bc7ea8e87c8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db10d2ba99af6b2e5f9d5e770e51406052f9b310ad5ed491c6c0f75edd49cb6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaadd39bf583c3c87e9618fb658948054aab52885fb470010ce0c305a66af824(
    value: typing.Optional[GkeonpremVmwareAdminClusterPlatformConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62faf00f3472671e48ce83b2a51c7537eb174847808bd4bb4c64f723522c07c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a43ac3c05cbdbb5de8631378a2845197161e0600092802f6794122eb006a0d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d71f5b3d2ac379c96f006967e143e4ca8ef3f6a732613f045a9c2e71e02ad1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fccd054bff4c014d78399d1c7b4040203038c696bb77bf749f033527f6fe9e69(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7823e8c00e84da5c3eea8ddf2dfc580864027af0a5b342bca4711a4dff29f697(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198da0d13160098f98a09fb5f4d88f60be186bc5108f4565632cd4629426ea98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e038b51174983eea636b65d77beab8d79834b226201c8fda1d12c95ead7cd9(
    value: typing.Optional[GkeonpremVmwareAdminClusterPlatformConfigStatusConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c69846d05edbd7f3bdcbc79859c2330f351881e5d09197d7633b59809f96058(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60986cd94a9cfed4f858e3a98f4eaf1cc8bc81135130e83b129f5132da9658cf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dec02e364bfa12ee5bbd86dc4e34765b6b63f99914cbb178a6548f47e803783(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb8141c6e0c5533e9d1ddf33e5c13335ccd7182936a2b4fca6e0c1e53e2e19b6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b355cf517e67835c2a329320d01fe0e74ef4531745d7fc6ffa4db43c7c3ae9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74e616a31b67cd9436e91641911b399dfb0303353dca7dcdc3b09bca22c0d19d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40278e4831bd1d2a5e7481d4c61f2b9f3ba4ca9b24f4a6a145c540cf66f36777(
    value: typing.Optional[GkeonpremVmwareAdminClusterPlatformConfigStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf3313ff462938c721dfa0a8254f77b699d5472af425310f4bf242e50d99a03(
    *,
    address: typing.Optional[builtins.str] = None,
    ca_cert: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdff9a3a7769d23b7cfabba00d2c5985f54a16b9189e39443e40968df9945c7d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78d1388227f5ab20ba762c73b0e0aac0841436c13ae46efb9274fca9f822399b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0710f6e2e36bc7bc91501a7b3a4a76e26decdf7fab493e1038fa4080a607671(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67fe37d1253efd18ca436ca7c789bfe0de2c7a25394a180f085847a15ac32444(
    value: typing.Optional[GkeonpremVmwareAdminClusterPrivateRegistryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d99cf9378b85bc6d7cdbf6e061ea72db8b18ead86bb046b9f3c9047976d30524(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb7ee2d0c41f579ae5bccfe8ae5d470e6e42ec3a6cb59b630026e988ceb2b1b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a15ab719d1badd07b288891d41d38b19c2a79e6450b0ed2bc15a8610ea95ba9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0b94f1c54948cceef7d838b9311d41c51430e25c5d3b4d26704b5c1aa14650(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac1bff8be972ebb2818d4d7d974e23ee14b410058450c75c597b9a9bfdfc2da8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__157aa6569a0466d6a5a01bbf81c6dc6029ff43cf0f7a9098250068d7e96d1c06(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bff500b583e2bc3eeb286ca4b78cc192fc6556b507ec93410e32e430d3b54393(
    value: typing.Optional[GkeonpremVmwareAdminClusterStatusConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52945818b37cab56c308818f84ac38430b4a4ed685421e08dc4ad8ee9c4503c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2025dd8413412ad6d6efd5349f6ee4a2c13ba9ea9abb8b6f788ebf65cf79f91f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0909b51fe876dbdf19f1853412fa63d640e7ada7ed5b6debe24986d53fdfbf10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c45f67b848fc688e0d39cf1f8975eec32843244a45f7cc948d524eeaac19eac(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__359b3130b4133b814cebde9942a08058b538f1fc0064e5732c662a5ef7d4e470(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fe08e0df9769b32049eaf3b79a50b74a0c3dc2a8047c468a93f8189bbb23754(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89d40a69bc4497a13f44ead25b41d2009667133f7cf5efaadb11fd1a965d61a8(
    value: typing.Optional[GkeonpremVmwareAdminClusterStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17ee5e223600f07a8d03ec2fea357e426237d717e188f711e5df0f2db2469dd9(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552894e0e58ddeb9a8cd03f2de875b86eb2f8c9ca5da1737f3000f29deb0c06e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__082348f9e76b1c6c4b73df70d8fc0d5d1a02a35cc30a344a02a4446ce396d5f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea19e37a55949c4d42178841aea51a6ef12e7af83f43fab8a2dee0d3ba8186bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa4cc5a4bf28fb99220766594faccf749aece1160b30a22fbd661c16a01f0f17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd3087a87f89acacf46d244c25c02e41c565971a679bcd91b3938cc2312b512(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareAdminClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15995ab5818a40b47623fe05320fb8008ddd3996923d77780f7e185ee3fab40a(
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

def _typecheckingstub__adf2f4b3255007196382366841f98ed1d585d7753377a42c850c971a5a5b5ba6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__512e1e804f6588332d59e28476f1a5610312e44734aafe2b1d1a42a0f7087983(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed9e70325864fe634533fedd5c66fec02d4347544aa96d3ed77344778f55364d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e88eb7fa226caa556cb785ffdb5642199c9607cad95417723671863bc08be7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c15d55eed9e5335bef842fd75d0bac5af1da7ea1713321b0fb7254840e86b876(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c23a9e5a929dad1566285219ae29f1d501a42c4ca41afcb4086caac7b335795d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d43ecb6e6005b3630aac2abbf1d929d80a727f6866620e72f7955c154d092da9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84d1a6bdd8dbbfeeba8062389d26793ac4e8de1bf46966f331066affb56522dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1be2ee1da6a194f9f7488babc562f43eb28fe36f4bbcc6a6504b382a309f21f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8392fb96961a739c25bea344575da3223c8f578903396fef321e0d865c13d711(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__033182f0b8c118b5f952ccf81fbb7eb79fdd1b380a45da3193dc3fdd5bd77474(
    value: typing.Optional[GkeonpremVmwareAdminClusterVcenter],
) -> None:
    """Type checking stubs"""
    pass
