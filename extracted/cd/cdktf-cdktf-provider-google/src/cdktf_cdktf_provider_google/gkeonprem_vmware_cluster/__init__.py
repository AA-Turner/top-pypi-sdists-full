r'''
# `google_gkeonprem_vmware_cluster`

Refer to the Terraform Registry for docs: [`google_gkeonprem_vmware_cluster`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster).
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


class GkeonpremVmwareCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster google_gkeonprem_vmware_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        admin_cluster_membership: builtins.str,
        control_plane_node: typing.Union["GkeonpremVmwareClusterControlPlaneNode", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        on_prem_version: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        anti_affinity_groups: typing.Optional[typing.Union["GkeonpremVmwareClusterAntiAffinityGroups", typing.Dict[builtins.str, typing.Any]]] = None,
        authorization: typing.Optional[typing.Union["GkeonpremVmwareClusterAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_repair_config: typing.Optional[typing.Union["GkeonpremVmwareClusterAutoRepairConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        dataplane_v2: typing.Optional[typing.Union["GkeonpremVmwareClusterDataplaneV2", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disable_bundled_ingress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_advanced_cluster: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_control_plane_v2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        load_balancer: typing.Optional[typing.Union["GkeonpremVmwareClusterLoadBalancer", typing.Dict[builtins.str, typing.Any]]] = None,
        network_config: typing.Optional[typing.Union["GkeonpremVmwareClusterNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        storage: typing.Optional[typing.Union["GkeonpremVmwareClusterStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GkeonpremVmwareClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        upgrade_policy: typing.Optional[typing.Union["GkeonpremVmwareClusterUpgradePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        vcenter: typing.Optional[typing.Union["GkeonpremVmwareClusterVcenter", typing.Dict[builtins.str, typing.Any]]] = None,
        vm_tracking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster google_gkeonprem_vmware_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param admin_cluster_membership: The admin cluster this VMware User Cluster belongs to. This is the full resource name of the admin cluster's hub membership. In the future, references to other resource types might be allowed if admin clusters are modeled as their own resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#admin_cluster_membership GkeonpremVmwareCluster#admin_cluster_membership}
        :param control_plane_node: control_plane_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#control_plane_node GkeonpremVmwareCluster#control_plane_node}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#location GkeonpremVmwareCluster#location}
        :param name: The VMware cluster name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#name GkeonpremVmwareCluster#name}
        :param on_prem_version: The Anthos clusters on the VMware version for your user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#on_prem_version GkeonpremVmwareCluster#on_prem_version}
        :param annotations: Annotations on the VMware User Cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#annotations GkeonpremVmwareCluster#annotations}
        :param anti_affinity_groups: anti_affinity_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#anti_affinity_groups GkeonpremVmwareCluster#anti_affinity_groups}
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#authorization GkeonpremVmwareCluster#authorization}
        :param auto_repair_config: auto_repair_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#auto_repair_config GkeonpremVmwareCluster#auto_repair_config}
        :param dataplane_v2: dataplane_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#dataplane_v2 GkeonpremVmwareCluster#dataplane_v2}
        :param description: A human readable description of this VMware User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#description GkeonpremVmwareCluster#description}
        :param disable_bundled_ingress: Disable bundled ingress. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#disable_bundled_ingress GkeonpremVmwareCluster#disable_bundled_ingress}
        :param enable_advanced_cluster: Enable advanced cluster. Default to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#enable_advanced_cluster GkeonpremVmwareCluster#enable_advanced_cluster}
        :param enable_control_plane_v2: Enable control plane V2. Default to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#enable_control_plane_v2 GkeonpremVmwareCluster#enable_control_plane_v2}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#id GkeonpremVmwareCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#load_balancer GkeonpremVmwareCluster#load_balancer}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#network_config GkeonpremVmwareCluster#network_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#project GkeonpremVmwareCluster#project}.
        :param storage: storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#storage GkeonpremVmwareCluster#storage}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#timeouts GkeonpremVmwareCluster#timeouts}
        :param upgrade_policy: upgrade_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#upgrade_policy GkeonpremVmwareCluster#upgrade_policy}
        :param vcenter: vcenter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#vcenter GkeonpremVmwareCluster#vcenter}
        :param vm_tracking_enabled: Enable VM tracking. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#vm_tracking_enabled GkeonpremVmwareCluster#vm_tracking_enabled}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ef6463a8c37cc2f184f5cb04f538d7eefb06762ed5e14a6daf41fa40094a477)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GkeonpremVmwareClusterConfig(
            admin_cluster_membership=admin_cluster_membership,
            control_plane_node=control_plane_node,
            location=location,
            name=name,
            on_prem_version=on_prem_version,
            annotations=annotations,
            anti_affinity_groups=anti_affinity_groups,
            authorization=authorization,
            auto_repair_config=auto_repair_config,
            dataplane_v2=dataplane_v2,
            description=description,
            disable_bundled_ingress=disable_bundled_ingress,
            enable_advanced_cluster=enable_advanced_cluster,
            enable_control_plane_v2=enable_control_plane_v2,
            id=id,
            load_balancer=load_balancer,
            network_config=network_config,
            project=project,
            storage=storage,
            timeouts=timeouts,
            upgrade_policy=upgrade_policy,
            vcenter=vcenter,
            vm_tracking_enabled=vm_tracking_enabled,
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
        '''Generates CDKTF code for importing a GkeonpremVmwareCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GkeonpremVmwareCluster to import.
        :param import_from_id: The id of the existing GkeonpremVmwareCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GkeonpremVmwareCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__742d477fb07691bcc26204eabdf5d7d78c1a222ceab730c7d88de3818864ec78)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAntiAffinityGroups")
    def put_anti_affinity_groups(
        self,
        *,
        aag_config_disabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param aag_config_disabled: Spread nodes across at least three physical hosts (requires at least three hosts). Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#aag_config_disabled GkeonpremVmwareCluster#aag_config_disabled}
        '''
        value = GkeonpremVmwareClusterAntiAffinityGroups(
            aag_config_disabled=aag_config_disabled
        )

        return typing.cast(None, jsii.invoke(self, "putAntiAffinityGroups", [value]))

    @jsii.member(jsii_name="putAuthorization")
    def put_authorization(
        self,
        *,
        admin_users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremVmwareClusterAuthorizationAdminUsers", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#admin_users GkeonpremVmwareCluster#admin_users}
        '''
        value = GkeonpremVmwareClusterAuthorization(admin_users=admin_users)

        return typing.cast(None, jsii.invoke(self, "putAuthorization", [value]))

    @jsii.member(jsii_name="putAutoRepairConfig")
    def put_auto_repair_config(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether auto repair is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#enabled GkeonpremVmwareCluster#enabled}
        '''
        value = GkeonpremVmwareClusterAutoRepairConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putAutoRepairConfig", [value]))

    @jsii.member(jsii_name="putControlPlaneNode")
    def put_control_plane_node(
        self,
        *,
        auto_resize_config: typing.Optional[typing.Union["GkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        cpus: typing.Optional[jsii.Number] = None,
        memory: typing.Optional[jsii.Number] = None,
        replicas: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param auto_resize_config: auto_resize_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#auto_resize_config GkeonpremVmwareCluster#auto_resize_config}
        :param cpus: The number of CPUs for each admin cluster node that serve as control planes for this VMware User Cluster. (default: 4 CPUs) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#cpus GkeonpremVmwareCluster#cpus}
        :param memory: The megabytes of memory for each admin cluster node that serves as a control plane for this VMware User Cluster (default: 8192 MB memory). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#memory GkeonpremVmwareCluster#memory}
        :param replicas: The number of control plane nodes for this VMware User Cluster. (default: 1 replica). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#replicas GkeonpremVmwareCluster#replicas}
        '''
        value = GkeonpremVmwareClusterControlPlaneNode(
            auto_resize_config=auto_resize_config,
            cpus=cpus,
            memory=memory,
            replicas=replicas,
        )

        return typing.cast(None, jsii.invoke(self, "putControlPlaneNode", [value]))

    @jsii.member(jsii_name="putDataplaneV2")
    def put_dataplane_v2(
        self,
        *,
        advanced_networking: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dataplane_v2_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        windows_dataplane_v2_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param advanced_networking: Enable advanced networking which requires dataplane_v2_enabled to be set true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#advanced_networking GkeonpremVmwareCluster#advanced_networking}
        :param dataplane_v2_enabled: Enables Dataplane V2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#dataplane_v2_enabled GkeonpremVmwareCluster#dataplane_v2_enabled}
        :param windows_dataplane_v2_enabled: Enable Dataplane V2 for clusters with Windows nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#windows_dataplane_v2_enabled GkeonpremVmwareCluster#windows_dataplane_v2_enabled}
        '''
        value = GkeonpremVmwareClusterDataplaneV2(
            advanced_networking=advanced_networking,
            dataplane_v2_enabled=dataplane_v2_enabled,
            windows_dataplane_v2_enabled=windows_dataplane_v2_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putDataplaneV2", [value]))

    @jsii.member(jsii_name="putLoadBalancer")
    def put_load_balancer(
        self,
        *,
        f5_config: typing.Optional[typing.Union["GkeonpremVmwareClusterLoadBalancerF5Config", typing.Dict[builtins.str, typing.Any]]] = None,
        manual_lb_config: typing.Optional[typing.Union["GkeonpremVmwareClusterLoadBalancerManualLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        metal_lb_config: typing.Optional[typing.Union["GkeonpremVmwareClusterLoadBalancerMetalLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        vip_config: typing.Optional[typing.Union["GkeonpremVmwareClusterLoadBalancerVipConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param f5_config: f5_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#f5_config GkeonpremVmwareCluster#f5_config}
        :param manual_lb_config: manual_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#manual_lb_config GkeonpremVmwareCluster#manual_lb_config}
        :param metal_lb_config: metal_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#metal_lb_config GkeonpremVmwareCluster#metal_lb_config}
        :param vip_config: vip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#vip_config GkeonpremVmwareCluster#vip_config}
        '''
        value = GkeonpremVmwareClusterLoadBalancer(
            f5_config=f5_config,
            manual_lb_config=manual_lb_config,
            metal_lb_config=metal_lb_config,
            vip_config=vip_config,
        )

        return typing.cast(None, jsii.invoke(self, "putLoadBalancer", [value]))

    @jsii.member(jsii_name="putNetworkConfig")
    def put_network_config(
        self,
        *,
        pod_address_cidr_blocks: typing.Sequence[builtins.str],
        service_address_cidr_blocks: typing.Sequence[builtins.str],
        control_plane_v2_config: typing.Optional[typing.Union["GkeonpremVmwareClusterNetworkConfigControlPlaneV2Config", typing.Dict[builtins.str, typing.Any]]] = None,
        dhcp_ip_config: typing.Optional[typing.Union["GkeonpremVmwareClusterNetworkConfigDhcpIpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        host_config: typing.Optional[typing.Union["GkeonpremVmwareClusterNetworkConfigHostConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        static_ip_config: typing.Optional[typing.Union["GkeonpremVmwareClusterNetworkConfigStaticIpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        vcenter_network: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pod_address_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#pod_address_cidr_blocks GkeonpremVmwareCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported.. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#service_address_cidr_blocks GkeonpremVmwareCluster#service_address_cidr_blocks}
        :param control_plane_v2_config: control_plane_v2_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#control_plane_v2_config GkeonpremVmwareCluster#control_plane_v2_config}
        :param dhcp_ip_config: dhcp_ip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#dhcp_ip_config GkeonpremVmwareCluster#dhcp_ip_config}
        :param host_config: host_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#host_config GkeonpremVmwareCluster#host_config}
        :param static_ip_config: static_ip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#static_ip_config GkeonpremVmwareCluster#static_ip_config}
        :param vcenter_network: vcenter_network specifies vCenter network name. Inherited from the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#vcenter_network GkeonpremVmwareCluster#vcenter_network}
        '''
        value = GkeonpremVmwareClusterNetworkConfig(
            pod_address_cidr_blocks=pod_address_cidr_blocks,
            service_address_cidr_blocks=service_address_cidr_blocks,
            control_plane_v2_config=control_plane_v2_config,
            dhcp_ip_config=dhcp_ip_config,
            host_config=host_config,
            static_ip_config=static_ip_config,
            vcenter_network=vcenter_network,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfig", [value]))

    @jsii.member(jsii_name="putStorage")
    def put_storage(
        self,
        *,
        vsphere_csi_disabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param vsphere_csi_disabled: Whether or not to deploy vSphere CSI components in the VMware User Cluster. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#vsphere_csi_disabled GkeonpremVmwareCluster#vsphere_csi_disabled}
        '''
        value = GkeonpremVmwareClusterStorage(
            vsphere_csi_disabled=vsphere_csi_disabled
        )

        return typing.cast(None, jsii.invoke(self, "putStorage", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#create GkeonpremVmwareCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#delete GkeonpremVmwareCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#update GkeonpremVmwareCluster#update}.
        '''
        value = GkeonpremVmwareClusterTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUpgradePolicy")
    def put_upgrade_policy(
        self,
        *,
        control_plane_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param control_plane_only: Controls whether the upgrade applies to the control plane only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#control_plane_only GkeonpremVmwareCluster#control_plane_only}
        '''
        value = GkeonpremVmwareClusterUpgradePolicy(
            control_plane_only=control_plane_only
        )

        return typing.cast(None, jsii.invoke(self, "putUpgradePolicy", [value]))

    @jsii.member(jsii_name="putVcenter")
    def put_vcenter(
        self,
        *,
        ca_cert_data: typing.Optional[builtins.str] = None,
        cluster: typing.Optional[builtins.str] = None,
        datacenter: typing.Optional[builtins.str] = None,
        datastore: typing.Optional[builtins.str] = None,
        folder: typing.Optional[builtins.str] = None,
        resource_pool: typing.Optional[builtins.str] = None,
        storage_policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ca_cert_data: Contains the vCenter CA certificate public key for SSL verification. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ca_cert_data GkeonpremVmwareCluster#ca_cert_data}
        :param cluster: The name of the vCenter cluster for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#cluster GkeonpremVmwareCluster#cluster}
        :param datacenter: The name of the vCenter datacenter for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#datacenter GkeonpremVmwareCluster#datacenter}
        :param datastore: The name of the vCenter datastore for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#datastore GkeonpremVmwareCluster#datastore}
        :param folder: The name of the vCenter folder for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#folder GkeonpremVmwareCluster#folder}
        :param resource_pool: The name of the vCenter resource pool for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#resource_pool GkeonpremVmwareCluster#resource_pool}
        :param storage_policy_name: The name of the vCenter storage policy for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#storage_policy_name GkeonpremVmwareCluster#storage_policy_name}
        '''
        value = GkeonpremVmwareClusterVcenter(
            ca_cert_data=ca_cert_data,
            cluster=cluster,
            datacenter=datacenter,
            datastore=datastore,
            folder=folder,
            resource_pool=resource_pool,
            storage_policy_name=storage_policy_name,
        )

        return typing.cast(None, jsii.invoke(self, "putVcenter", [value]))

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

    @jsii.member(jsii_name="resetDataplaneV2")
    def reset_dataplane_v2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataplaneV2", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisableBundledIngress")
    def reset_disable_bundled_ingress(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableBundledIngress", []))

    @jsii.member(jsii_name="resetEnableAdvancedCluster")
    def reset_enable_advanced_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableAdvancedCluster", []))

    @jsii.member(jsii_name="resetEnableControlPlaneV2")
    def reset_enable_control_plane_v2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableControlPlaneV2", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLoadBalancer")
    def reset_load_balancer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancer", []))

    @jsii.member(jsii_name="resetNetworkConfig")
    def reset_network_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetStorage")
    def reset_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorage", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUpgradePolicy")
    def reset_upgrade_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpgradePolicy", []))

    @jsii.member(jsii_name="resetVcenter")
    def reset_vcenter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVcenter", []))

    @jsii.member(jsii_name="resetVmTrackingEnabled")
    def reset_vm_tracking_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmTrackingEnabled", []))

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
    @jsii.member(jsii_name="antiAffinityGroups")
    def anti_affinity_groups(
        self,
    ) -> "GkeonpremVmwareClusterAntiAffinityGroupsOutputReference":
        return typing.cast("GkeonpremVmwareClusterAntiAffinityGroupsOutputReference", jsii.get(self, "antiAffinityGroups"))

    @builtins.property
    @jsii.member(jsii_name="authorization")
    def authorization(self) -> "GkeonpremVmwareClusterAuthorizationOutputReference":
        return typing.cast("GkeonpremVmwareClusterAuthorizationOutputReference", jsii.get(self, "authorization"))

    @builtins.property
    @jsii.member(jsii_name="autoRepairConfig")
    def auto_repair_config(
        self,
    ) -> "GkeonpremVmwareClusterAutoRepairConfigOutputReference":
        return typing.cast("GkeonpremVmwareClusterAutoRepairConfigOutputReference", jsii.get(self, "autoRepairConfig"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneNode")
    def control_plane_node(
        self,
    ) -> "GkeonpremVmwareClusterControlPlaneNodeOutputReference":
        return typing.cast("GkeonpremVmwareClusterControlPlaneNodeOutputReference", jsii.get(self, "controlPlaneNode"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="dataplaneV2")
    def dataplane_v2(self) -> "GkeonpremVmwareClusterDataplaneV2OutputReference":
        return typing.cast("GkeonpremVmwareClusterDataplaneV2OutputReference", jsii.get(self, "dataplaneV2"))

    @builtins.property
    @jsii.member(jsii_name="deleteTime")
    def delete_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

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
    def fleet(self) -> "GkeonpremVmwareClusterFleetList":
        return typing.cast("GkeonpremVmwareClusterFleetList", jsii.get(self, "fleet"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> "GkeonpremVmwareClusterLoadBalancerOutputReference":
        return typing.cast("GkeonpremVmwareClusterLoadBalancerOutputReference", jsii.get(self, "loadBalancer"))

    @builtins.property
    @jsii.member(jsii_name="localName")
    def local_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localName"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(self) -> "GkeonpremVmwareClusterNetworkConfigOutputReference":
        return typing.cast("GkeonpremVmwareClusterNetworkConfigOutputReference", jsii.get(self, "networkConfig"))

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
    def status(self) -> "GkeonpremVmwareClusterStatusList":
        return typing.cast("GkeonpremVmwareClusterStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="storage")
    def storage(self) -> "GkeonpremVmwareClusterStorageOutputReference":
        return typing.cast("GkeonpremVmwareClusterStorageOutputReference", jsii.get(self, "storage"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GkeonpremVmwareClusterTimeoutsOutputReference":
        return typing.cast("GkeonpremVmwareClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="upgradePolicy")
    def upgrade_policy(self) -> "GkeonpremVmwareClusterUpgradePolicyOutputReference":
        return typing.cast("GkeonpremVmwareClusterUpgradePolicyOutputReference", jsii.get(self, "upgradePolicy"))

    @builtins.property
    @jsii.member(jsii_name="validationCheck")
    def validation_check(self) -> "GkeonpremVmwareClusterValidationCheckList":
        return typing.cast("GkeonpremVmwareClusterValidationCheckList", jsii.get(self, "validationCheck"))

    @builtins.property
    @jsii.member(jsii_name="vcenter")
    def vcenter(self) -> "GkeonpremVmwareClusterVcenterOutputReference":
        return typing.cast("GkeonpremVmwareClusterVcenterOutputReference", jsii.get(self, "vcenter"))

    @builtins.property
    @jsii.member(jsii_name="adminClusterMembershipInput")
    def admin_cluster_membership_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminClusterMembershipInput"))

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
    ) -> typing.Optional["GkeonpremVmwareClusterAntiAffinityGroups"]:
        return typing.cast(typing.Optional["GkeonpremVmwareClusterAntiAffinityGroups"], jsii.get(self, "antiAffinityGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationInput")
    def authorization_input(
        self,
    ) -> typing.Optional["GkeonpremVmwareClusterAuthorization"]:
        return typing.cast(typing.Optional["GkeonpremVmwareClusterAuthorization"], jsii.get(self, "authorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="autoRepairConfigInput")
    def auto_repair_config_input(
        self,
    ) -> typing.Optional["GkeonpremVmwareClusterAutoRepairConfig"]:
        return typing.cast(typing.Optional["GkeonpremVmwareClusterAutoRepairConfig"], jsii.get(self, "autoRepairConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneNodeInput")
    def control_plane_node_input(
        self,
    ) -> typing.Optional["GkeonpremVmwareClusterControlPlaneNode"]:
        return typing.cast(typing.Optional["GkeonpremVmwareClusterControlPlaneNode"], jsii.get(self, "controlPlaneNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="dataplaneV2Input")
    def dataplane_v2_input(
        self,
    ) -> typing.Optional["GkeonpremVmwareClusterDataplaneV2"]:
        return typing.cast(typing.Optional["GkeonpremVmwareClusterDataplaneV2"], jsii.get(self, "dataplaneV2Input"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="disableBundledIngressInput")
    def disable_bundled_ingress_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableBundledIngressInput"))

    @builtins.property
    @jsii.member(jsii_name="enableAdvancedClusterInput")
    def enable_advanced_cluster_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableAdvancedClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="enableControlPlaneV2Input")
    def enable_control_plane_v2_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableControlPlaneV2Input"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerInput")
    def load_balancer_input(
        self,
    ) -> typing.Optional["GkeonpremVmwareClusterLoadBalancer"]:
        return typing.cast(typing.Optional["GkeonpremVmwareClusterLoadBalancer"], jsii.get(self, "loadBalancerInput"))

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
    ) -> typing.Optional["GkeonpremVmwareClusterNetworkConfig"]:
        return typing.cast(typing.Optional["GkeonpremVmwareClusterNetworkConfig"], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="onPremVersionInput")
    def on_prem_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onPremVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="storageInput")
    def storage_input(self) -> typing.Optional["GkeonpremVmwareClusterStorage"]:
        return typing.cast(typing.Optional["GkeonpremVmwareClusterStorage"], jsii.get(self, "storageInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeonpremVmwareClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeonpremVmwareClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="upgradePolicyInput")
    def upgrade_policy_input(
        self,
    ) -> typing.Optional["GkeonpremVmwareClusterUpgradePolicy"]:
        return typing.cast(typing.Optional["GkeonpremVmwareClusterUpgradePolicy"], jsii.get(self, "upgradePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="vcenterInput")
    def vcenter_input(self) -> typing.Optional["GkeonpremVmwareClusterVcenter"]:
        return typing.cast(typing.Optional["GkeonpremVmwareClusterVcenter"], jsii.get(self, "vcenterInput"))

    @builtins.property
    @jsii.member(jsii_name="vmTrackingEnabledInput")
    def vm_tracking_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "vmTrackingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="adminClusterMembership")
    def admin_cluster_membership(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminClusterMembership"))

    @admin_cluster_membership.setter
    def admin_cluster_membership(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4b16f62da0c1dcb56b1473cd04eba4e9fd965e66622d5547dea5f4b8d6b059e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminClusterMembership", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3a73015150580f4e45171f779d45074dd86f531f10dc985d8efa8e3129831c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48a4833b8e103870bfce3e5a8b98d412002003951e66efa8219f91c0b828e1f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableBundledIngress")
    def disable_bundled_ingress(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableBundledIngress"))

    @disable_bundled_ingress.setter
    def disable_bundled_ingress(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__314b0ea6e3b02a35adb3a817823c3efb4fea615aff4a8118df8a5ac607ab02cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableBundledIngress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableAdvancedCluster")
    def enable_advanced_cluster(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableAdvancedCluster"))

    @enable_advanced_cluster.setter
    def enable_advanced_cluster(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79909f4d6b63f5ecf010daa6802d15b1edbff944b16a9d69319e4a221482dede)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAdvancedCluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableControlPlaneV2")
    def enable_control_plane_v2(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableControlPlaneV2"))

    @enable_control_plane_v2.setter
    def enable_control_plane_v2(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c35a61da5f1e5789ceeb4d4c7be0c28b07e082266b6a133d008e259c85f81b5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableControlPlaneV2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23b8f26e8791e29bcfb844a668934fbffeec7e2ae0d865da701978be2f6d4b12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d40e920824d947a1c9406e414d5c9dad651cf97af1a3536bc70d79fd100a7a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa39d6d369c1a785a2ce510e86d9b9279e0b9b08fa4bcbe0150c49f8bfc7de7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onPremVersion")
    def on_prem_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onPremVersion"))

    @on_prem_version.setter
    def on_prem_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98ea005d43c0f1e8640862f73d40ec2a07b9458b74a637c9eb296e4c7d9664ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onPremVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__066fa11fb7a3aa2285d80b3610389b0cea1b7f9e3c538c37566ca7a107cfadb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmTrackingEnabled")
    def vm_tracking_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "vmTrackingEnabled"))

    @vm_tracking_enabled.setter
    def vm_tracking_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a4ae147475d07cd3c1f813faa0d1457c6eb352d2334ae0289f9f6f1186ec14c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmTrackingEnabled", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterAntiAffinityGroups",
    jsii_struct_bases=[],
    name_mapping={"aag_config_disabled": "aagConfigDisabled"},
)
class GkeonpremVmwareClusterAntiAffinityGroups:
    def __init__(
        self,
        *,
        aag_config_disabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param aag_config_disabled: Spread nodes across at least three physical hosts (requires at least three hosts). Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#aag_config_disabled GkeonpremVmwareCluster#aag_config_disabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5e4a8ce20cdd5a6081ed2451a1ef2e02aa39a42d101ad080764edf8da81352e)
            check_type(argname="argument aag_config_disabled", value=aag_config_disabled, expected_type=type_hints["aag_config_disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aag_config_disabled": aag_config_disabled,
        }

    @builtins.property
    def aag_config_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Spread nodes across at least three physical hosts (requires at least three hosts). Enabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#aag_config_disabled GkeonpremVmwareCluster#aag_config_disabled}
        '''
        result = self._values.get("aag_config_disabled")
        assert result is not None, "Required property 'aag_config_disabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterAntiAffinityGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareClusterAntiAffinityGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterAntiAffinityGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d15d82645ea977862af85a8708c2a30392585ab29643b24ce82067e00562656)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7c59b3d1af760b0edeca1360aea02a2ccf55878093560c271e8c705eb5d9ce2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aagConfigDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterAntiAffinityGroups]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterAntiAffinityGroups], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterAntiAffinityGroups],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1d86ea6be10048405b6fb001f91335768923d765b7c215685c960fa00de966f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterAuthorization",
    jsii_struct_bases=[],
    name_mapping={"admin_users": "adminUsers"},
)
class GkeonpremVmwareClusterAuthorization:
    def __init__(
        self,
        *,
        admin_users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremVmwareClusterAuthorizationAdminUsers", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#admin_users GkeonpremVmwareCluster#admin_users}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24f654d203be9c8a3e90b5e4ed086390cbc4f6315fc2b10011e1c0e6cd756a4c)
            check_type(argname="argument admin_users", value=admin_users, expected_type=type_hints["admin_users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if admin_users is not None:
            self._values["admin_users"] = admin_users

    @builtins.property
    def admin_users(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareClusterAuthorizationAdminUsers"]]]:
        '''admin_users block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#admin_users GkeonpremVmwareCluster#admin_users}
        '''
        result = self._values.get("admin_users")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareClusterAuthorizationAdminUsers"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterAuthorizationAdminUsers",
    jsii_struct_bases=[],
    name_mapping={"username": "username"},
)
class GkeonpremVmwareClusterAuthorizationAdminUsers:
    def __init__(self, *, username: builtins.str) -> None:
        '''
        :param username: The name of the user, e.g. 'my-gcp-id@gmail.com'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#username GkeonpremVmwareCluster#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e436656bb36ba3ee75cedb596281a84383bc05f944b1afb2f2fcb7747153100d)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
        }

    @builtins.property
    def username(self) -> builtins.str:
        '''The name of the user, e.g. 'my-gcp-id@gmail.com'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#username GkeonpremVmwareCluster#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterAuthorizationAdminUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareClusterAuthorizationAdminUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterAuthorizationAdminUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ada0bc2c314b529626c7af8bb2a4051c2054fc76b909896fa6726cd149976aa4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareClusterAuthorizationAdminUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__836c5a6db9b9075c250512f18bc1466ab831e95e99699ec405c3b8556fdba8ec)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareClusterAuthorizationAdminUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e7f248a8ae83ba636d2b79cd664e6d512a0620c851bd5f1b3f76ab1422e2ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7595cfba3b331582d0a65278853a5589d32f0e3962d680498075e14c72da8b3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__89048136af455fa7a473cd4a2eef05f6abfaa385058c4572de4d01ca23fb78da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterAuthorizationAdminUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterAuthorizationAdminUsers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterAuthorizationAdminUsers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a6848c9511b8a7b5912f1378146411630bbd1c79e2defb043417a2f674c10ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareClusterAuthorizationAdminUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterAuthorizationAdminUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b953cf495a97eb461a5feae1ec098f766069c843d8b2121119fd098e680cd130)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3987dd5bd4a9bcfa7abda961ac1a512e37ae8e62c40fd905e1c8cb48fb80ecc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterAuthorizationAdminUsers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterAuthorizationAdminUsers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterAuthorizationAdminUsers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd893b4db3ae224501bff0a0644ab79044277d1d1c8bd8e01dab8cf5a95a9ee3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareClusterAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26879e9b014f240c3caccc35b4c7bbeaee2de4c7cdeca8e14b8050fdb49e1f80)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdminUsers")
    def put_admin_users(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareClusterAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0608957c3de730dc71e3b0d1cdc00887cf11a1acdf87239c19f984535d19776f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdminUsers", [value]))

    @jsii.member(jsii_name="resetAdminUsers")
    def reset_admin_users(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminUsers", []))

    @builtins.property
    @jsii.member(jsii_name="adminUsers")
    def admin_users(self) -> GkeonpremVmwareClusterAuthorizationAdminUsersList:
        return typing.cast(GkeonpremVmwareClusterAuthorizationAdminUsersList, jsii.get(self, "adminUsers"))

    @builtins.property
    @jsii.member(jsii_name="adminUsersInput")
    def admin_users_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterAuthorizationAdminUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterAuthorizationAdminUsers]]], jsii.get(self, "adminUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremVmwareClusterAuthorization]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__640b8aea39c6ae57f220070bf6df20594b2abc4a3dab4aea56df3a79723b9944)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterAutoRepairConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GkeonpremVmwareClusterAutoRepairConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether auto repair is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#enabled GkeonpremVmwareCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d59bf195303fe8d7e3b4aca3b7ed32f23e023238a6aeb9b89251b3df1518dfc0)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether auto repair is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#enabled GkeonpremVmwareCluster#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterAutoRepairConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareClusterAutoRepairConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterAutoRepairConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2549f6091af3da4cbae17c09418271f32f06d586153eae73141189023fcd845)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e96025a729792b3ef4150c42f03eb45a6de66ee365697444194b8dde32a8e781)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremVmwareClusterAutoRepairConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterAutoRepairConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterAutoRepairConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80de3c7e05944f8ea9d64343869d355dfb82fda54d2d87ec75bca0d8fad0725d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "admin_cluster_membership": "adminClusterMembership",
        "control_plane_node": "controlPlaneNode",
        "location": "location",
        "name": "name",
        "on_prem_version": "onPremVersion",
        "annotations": "annotations",
        "anti_affinity_groups": "antiAffinityGroups",
        "authorization": "authorization",
        "auto_repair_config": "autoRepairConfig",
        "dataplane_v2": "dataplaneV2",
        "description": "description",
        "disable_bundled_ingress": "disableBundledIngress",
        "enable_advanced_cluster": "enableAdvancedCluster",
        "enable_control_plane_v2": "enableControlPlaneV2",
        "id": "id",
        "load_balancer": "loadBalancer",
        "network_config": "networkConfig",
        "project": "project",
        "storage": "storage",
        "timeouts": "timeouts",
        "upgrade_policy": "upgradePolicy",
        "vcenter": "vcenter",
        "vm_tracking_enabled": "vmTrackingEnabled",
    },
)
class GkeonpremVmwareClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        admin_cluster_membership: builtins.str,
        control_plane_node: typing.Union["GkeonpremVmwareClusterControlPlaneNode", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        on_prem_version: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        anti_affinity_groups: typing.Optional[typing.Union[GkeonpremVmwareClusterAntiAffinityGroups, typing.Dict[builtins.str, typing.Any]]] = None,
        authorization: typing.Optional[typing.Union[GkeonpremVmwareClusterAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_repair_config: typing.Optional[typing.Union[GkeonpremVmwareClusterAutoRepairConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        dataplane_v2: typing.Optional[typing.Union["GkeonpremVmwareClusterDataplaneV2", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disable_bundled_ingress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_advanced_cluster: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_control_plane_v2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        load_balancer: typing.Optional[typing.Union["GkeonpremVmwareClusterLoadBalancer", typing.Dict[builtins.str, typing.Any]]] = None,
        network_config: typing.Optional[typing.Union["GkeonpremVmwareClusterNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        storage: typing.Optional[typing.Union["GkeonpremVmwareClusterStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GkeonpremVmwareClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        upgrade_policy: typing.Optional[typing.Union["GkeonpremVmwareClusterUpgradePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        vcenter: typing.Optional[typing.Union["GkeonpremVmwareClusterVcenter", typing.Dict[builtins.str, typing.Any]]] = None,
        vm_tracking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param admin_cluster_membership: The admin cluster this VMware User Cluster belongs to. This is the full resource name of the admin cluster's hub membership. In the future, references to other resource types might be allowed if admin clusters are modeled as their own resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#admin_cluster_membership GkeonpremVmwareCluster#admin_cluster_membership}
        :param control_plane_node: control_plane_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#control_plane_node GkeonpremVmwareCluster#control_plane_node}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#location GkeonpremVmwareCluster#location}
        :param name: The VMware cluster name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#name GkeonpremVmwareCluster#name}
        :param on_prem_version: The Anthos clusters on the VMware version for your user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#on_prem_version GkeonpremVmwareCluster#on_prem_version}
        :param annotations: Annotations on the VMware User Cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#annotations GkeonpremVmwareCluster#annotations}
        :param anti_affinity_groups: anti_affinity_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#anti_affinity_groups GkeonpremVmwareCluster#anti_affinity_groups}
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#authorization GkeonpremVmwareCluster#authorization}
        :param auto_repair_config: auto_repair_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#auto_repair_config GkeonpremVmwareCluster#auto_repair_config}
        :param dataplane_v2: dataplane_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#dataplane_v2 GkeonpremVmwareCluster#dataplane_v2}
        :param description: A human readable description of this VMware User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#description GkeonpremVmwareCluster#description}
        :param disable_bundled_ingress: Disable bundled ingress. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#disable_bundled_ingress GkeonpremVmwareCluster#disable_bundled_ingress}
        :param enable_advanced_cluster: Enable advanced cluster. Default to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#enable_advanced_cluster GkeonpremVmwareCluster#enable_advanced_cluster}
        :param enable_control_plane_v2: Enable control plane V2. Default to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#enable_control_plane_v2 GkeonpremVmwareCluster#enable_control_plane_v2}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#id GkeonpremVmwareCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#load_balancer GkeonpremVmwareCluster#load_balancer}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#network_config GkeonpremVmwareCluster#network_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#project GkeonpremVmwareCluster#project}.
        :param storage: storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#storage GkeonpremVmwareCluster#storage}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#timeouts GkeonpremVmwareCluster#timeouts}
        :param upgrade_policy: upgrade_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#upgrade_policy GkeonpremVmwareCluster#upgrade_policy}
        :param vcenter: vcenter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#vcenter GkeonpremVmwareCluster#vcenter}
        :param vm_tracking_enabled: Enable VM tracking. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#vm_tracking_enabled GkeonpremVmwareCluster#vm_tracking_enabled}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(control_plane_node, dict):
            control_plane_node = GkeonpremVmwareClusterControlPlaneNode(**control_plane_node)
        if isinstance(anti_affinity_groups, dict):
            anti_affinity_groups = GkeonpremVmwareClusterAntiAffinityGroups(**anti_affinity_groups)
        if isinstance(authorization, dict):
            authorization = GkeonpremVmwareClusterAuthorization(**authorization)
        if isinstance(auto_repair_config, dict):
            auto_repair_config = GkeonpremVmwareClusterAutoRepairConfig(**auto_repair_config)
        if isinstance(dataplane_v2, dict):
            dataplane_v2 = GkeonpremVmwareClusterDataplaneV2(**dataplane_v2)
        if isinstance(load_balancer, dict):
            load_balancer = GkeonpremVmwareClusterLoadBalancer(**load_balancer)
        if isinstance(network_config, dict):
            network_config = GkeonpremVmwareClusterNetworkConfig(**network_config)
        if isinstance(storage, dict):
            storage = GkeonpremVmwareClusterStorage(**storage)
        if isinstance(timeouts, dict):
            timeouts = GkeonpremVmwareClusterTimeouts(**timeouts)
        if isinstance(upgrade_policy, dict):
            upgrade_policy = GkeonpremVmwareClusterUpgradePolicy(**upgrade_policy)
        if isinstance(vcenter, dict):
            vcenter = GkeonpremVmwareClusterVcenter(**vcenter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf267676316e0f706fe6220fede15de8e6f45aa45c9065dc06b3d6738765c292)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument admin_cluster_membership", value=admin_cluster_membership, expected_type=type_hints["admin_cluster_membership"])
            check_type(argname="argument control_plane_node", value=control_plane_node, expected_type=type_hints["control_plane_node"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument on_prem_version", value=on_prem_version, expected_type=type_hints["on_prem_version"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument anti_affinity_groups", value=anti_affinity_groups, expected_type=type_hints["anti_affinity_groups"])
            check_type(argname="argument authorization", value=authorization, expected_type=type_hints["authorization"])
            check_type(argname="argument auto_repair_config", value=auto_repair_config, expected_type=type_hints["auto_repair_config"])
            check_type(argname="argument dataplane_v2", value=dataplane_v2, expected_type=type_hints["dataplane_v2"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disable_bundled_ingress", value=disable_bundled_ingress, expected_type=type_hints["disable_bundled_ingress"])
            check_type(argname="argument enable_advanced_cluster", value=enable_advanced_cluster, expected_type=type_hints["enable_advanced_cluster"])
            check_type(argname="argument enable_control_plane_v2", value=enable_control_plane_v2, expected_type=type_hints["enable_control_plane_v2"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
            check_type(argname="argument network_config", value=network_config, expected_type=type_hints["network_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument storage", value=storage, expected_type=type_hints["storage"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument upgrade_policy", value=upgrade_policy, expected_type=type_hints["upgrade_policy"])
            check_type(argname="argument vcenter", value=vcenter, expected_type=type_hints["vcenter"])
            check_type(argname="argument vm_tracking_enabled", value=vm_tracking_enabled, expected_type=type_hints["vm_tracking_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_cluster_membership": admin_cluster_membership,
            "control_plane_node": control_plane_node,
            "location": location,
            "name": name,
            "on_prem_version": on_prem_version,
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
        if annotations is not None:
            self._values["annotations"] = annotations
        if anti_affinity_groups is not None:
            self._values["anti_affinity_groups"] = anti_affinity_groups
        if authorization is not None:
            self._values["authorization"] = authorization
        if auto_repair_config is not None:
            self._values["auto_repair_config"] = auto_repair_config
        if dataplane_v2 is not None:
            self._values["dataplane_v2"] = dataplane_v2
        if description is not None:
            self._values["description"] = description
        if disable_bundled_ingress is not None:
            self._values["disable_bundled_ingress"] = disable_bundled_ingress
        if enable_advanced_cluster is not None:
            self._values["enable_advanced_cluster"] = enable_advanced_cluster
        if enable_control_plane_v2 is not None:
            self._values["enable_control_plane_v2"] = enable_control_plane_v2
        if id is not None:
            self._values["id"] = id
        if load_balancer is not None:
            self._values["load_balancer"] = load_balancer
        if network_config is not None:
            self._values["network_config"] = network_config
        if project is not None:
            self._values["project"] = project
        if storage is not None:
            self._values["storage"] = storage
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if upgrade_policy is not None:
            self._values["upgrade_policy"] = upgrade_policy
        if vcenter is not None:
            self._values["vcenter"] = vcenter
        if vm_tracking_enabled is not None:
            self._values["vm_tracking_enabled"] = vm_tracking_enabled

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
    def admin_cluster_membership(self) -> builtins.str:
        '''The admin cluster this VMware User Cluster belongs to.

        This is the full resource name of the admin cluster's hub membership.
        In the future, references to other resource types might be allowed if
        admin clusters are modeled as their own resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#admin_cluster_membership GkeonpremVmwareCluster#admin_cluster_membership}
        '''
        result = self._values.get("admin_cluster_membership")
        assert result is not None, "Required property 'admin_cluster_membership' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def control_plane_node(self) -> "GkeonpremVmwareClusterControlPlaneNode":
        '''control_plane_node block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#control_plane_node GkeonpremVmwareCluster#control_plane_node}
        '''
        result = self._values.get("control_plane_node")
        assert result is not None, "Required property 'control_plane_node' is missing"
        return typing.cast("GkeonpremVmwareClusterControlPlaneNode", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#location GkeonpremVmwareCluster#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The VMware cluster name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#name GkeonpremVmwareCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def on_prem_version(self) -> builtins.str:
        '''The Anthos clusters on the VMware version for your user cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#on_prem_version GkeonpremVmwareCluster#on_prem_version}
        '''
        result = self._values.get("on_prem_version")
        assert result is not None, "Required property 'on_prem_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Annotations on the VMware User Cluster.

        This field has the same restrictions as Kubernetes annotations.
        The total size of all keys and values combined is limited to 256k.
        Key can have 2 segments: prefix (optional) and name (required),
        separated by a slash (/).
        Prefix must be a DNS subdomain.
        Name must be 63 characters or less, begin and end with alphanumerics,
        with dashes (-), underscores (_), dots (.), and alphanumerics between.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#annotations GkeonpremVmwareCluster#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def anti_affinity_groups(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterAntiAffinityGroups]:
        '''anti_affinity_groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#anti_affinity_groups GkeonpremVmwareCluster#anti_affinity_groups}
        '''
        result = self._values.get("anti_affinity_groups")
        return typing.cast(typing.Optional[GkeonpremVmwareClusterAntiAffinityGroups], result)

    @builtins.property
    def authorization(self) -> typing.Optional[GkeonpremVmwareClusterAuthorization]:
        '''authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#authorization GkeonpremVmwareCluster#authorization}
        '''
        result = self._values.get("authorization")
        return typing.cast(typing.Optional[GkeonpremVmwareClusterAuthorization], result)

    @builtins.property
    def auto_repair_config(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterAutoRepairConfig]:
        '''auto_repair_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#auto_repair_config GkeonpremVmwareCluster#auto_repair_config}
        '''
        result = self._values.get("auto_repair_config")
        return typing.cast(typing.Optional[GkeonpremVmwareClusterAutoRepairConfig], result)

    @builtins.property
    def dataplane_v2(self) -> typing.Optional["GkeonpremVmwareClusterDataplaneV2"]:
        '''dataplane_v2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#dataplane_v2 GkeonpremVmwareCluster#dataplane_v2}
        '''
        result = self._values.get("dataplane_v2")
        return typing.cast(typing.Optional["GkeonpremVmwareClusterDataplaneV2"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human readable description of this VMware User Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#description GkeonpremVmwareCluster#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_bundled_ingress(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable bundled ingress.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#disable_bundled_ingress GkeonpremVmwareCluster#disable_bundled_ingress}
        '''
        result = self._values.get("disable_bundled_ingress")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_advanced_cluster(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable advanced cluster. Default to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#enable_advanced_cluster GkeonpremVmwareCluster#enable_advanced_cluster}
        '''
        result = self._values.get("enable_advanced_cluster")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_control_plane_v2(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable control plane V2. Default to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#enable_control_plane_v2 GkeonpremVmwareCluster#enable_control_plane_v2}
        '''
        result = self._values.get("enable_control_plane_v2")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#id GkeonpremVmwareCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer(self) -> typing.Optional["GkeonpremVmwareClusterLoadBalancer"]:
        '''load_balancer block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#load_balancer GkeonpremVmwareCluster#load_balancer}
        '''
        result = self._values.get("load_balancer")
        return typing.cast(typing.Optional["GkeonpremVmwareClusterLoadBalancer"], result)

    @builtins.property
    def network_config(self) -> typing.Optional["GkeonpremVmwareClusterNetworkConfig"]:
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#network_config GkeonpremVmwareCluster#network_config}
        '''
        result = self._values.get("network_config")
        return typing.cast(typing.Optional["GkeonpremVmwareClusterNetworkConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#project GkeonpremVmwareCluster#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage(self) -> typing.Optional["GkeonpremVmwareClusterStorage"]:
        '''storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#storage GkeonpremVmwareCluster#storage}
        '''
        result = self._values.get("storage")
        return typing.cast(typing.Optional["GkeonpremVmwareClusterStorage"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GkeonpremVmwareClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#timeouts GkeonpremVmwareCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GkeonpremVmwareClusterTimeouts"], result)

    @builtins.property
    def upgrade_policy(self) -> typing.Optional["GkeonpremVmwareClusterUpgradePolicy"]:
        '''upgrade_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#upgrade_policy GkeonpremVmwareCluster#upgrade_policy}
        '''
        result = self._values.get("upgrade_policy")
        return typing.cast(typing.Optional["GkeonpremVmwareClusterUpgradePolicy"], result)

    @builtins.property
    def vcenter(self) -> typing.Optional["GkeonpremVmwareClusterVcenter"]:
        '''vcenter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#vcenter GkeonpremVmwareCluster#vcenter}
        '''
        result = self._values.get("vcenter")
        return typing.cast(typing.Optional["GkeonpremVmwareClusterVcenter"], result)

    @builtins.property
    def vm_tracking_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable VM tracking.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#vm_tracking_enabled GkeonpremVmwareCluster#vm_tracking_enabled}
        '''
        result = self._values.get("vm_tracking_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterControlPlaneNode",
    jsii_struct_bases=[],
    name_mapping={
        "auto_resize_config": "autoResizeConfig",
        "cpus": "cpus",
        "memory": "memory",
        "replicas": "replicas",
    },
)
class GkeonpremVmwareClusterControlPlaneNode:
    def __init__(
        self,
        *,
        auto_resize_config: typing.Optional[typing.Union["GkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        cpus: typing.Optional[jsii.Number] = None,
        memory: typing.Optional[jsii.Number] = None,
        replicas: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param auto_resize_config: auto_resize_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#auto_resize_config GkeonpremVmwareCluster#auto_resize_config}
        :param cpus: The number of CPUs for each admin cluster node that serve as control planes for this VMware User Cluster. (default: 4 CPUs) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#cpus GkeonpremVmwareCluster#cpus}
        :param memory: The megabytes of memory for each admin cluster node that serves as a control plane for this VMware User Cluster (default: 8192 MB memory). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#memory GkeonpremVmwareCluster#memory}
        :param replicas: The number of control plane nodes for this VMware User Cluster. (default: 1 replica). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#replicas GkeonpremVmwareCluster#replicas}
        '''
        if isinstance(auto_resize_config, dict):
            auto_resize_config = GkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig(**auto_resize_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__036836c01487abb5860a1f6192cab8b31ba6eb68096417ed9c0d4a0d829f1cb6)
            check_type(argname="argument auto_resize_config", value=auto_resize_config, expected_type=type_hints["auto_resize_config"])
            check_type(argname="argument cpus", value=cpus, expected_type=type_hints["cpus"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument replicas", value=replicas, expected_type=type_hints["replicas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_resize_config is not None:
            self._values["auto_resize_config"] = auto_resize_config
        if cpus is not None:
            self._values["cpus"] = cpus
        if memory is not None:
            self._values["memory"] = memory
        if replicas is not None:
            self._values["replicas"] = replicas

    @builtins.property
    def auto_resize_config(
        self,
    ) -> typing.Optional["GkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig"]:
        '''auto_resize_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#auto_resize_config GkeonpremVmwareCluster#auto_resize_config}
        '''
        result = self._values.get("auto_resize_config")
        return typing.cast(typing.Optional["GkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig"], result)

    @builtins.property
    def cpus(self) -> typing.Optional[jsii.Number]:
        '''The number of CPUs for each admin cluster node that serve as control planes for this VMware User Cluster.

        (default: 4 CPUs)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#cpus GkeonpremVmwareCluster#cpus}
        '''
        result = self._values.get("cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory(self) -> typing.Optional[jsii.Number]:
        '''The megabytes of memory for each admin cluster node that serves as a control plane for this VMware User Cluster (default: 8192 MB memory).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#memory GkeonpremVmwareCluster#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def replicas(self) -> typing.Optional[jsii.Number]:
        '''The number of control plane nodes for this VMware User Cluster. (default: 1 replica).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#replicas GkeonpremVmwareCluster#replicas}
        '''
        result = self._values.get("replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterControlPlaneNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether to enable control plane node auto resizing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#enabled GkeonpremVmwareCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b781cfa3e8d7a607e116a1a31757f80a0719d76040dfdf0656f5f55117e36ae3)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether to enable control plane node auto resizing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#enabled GkeonpremVmwareCluster#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareClusterControlPlaneNodeAutoResizeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterControlPlaneNodeAutoResizeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5c0ac6c73cacac4159898c92d21b9002de4565f729b18d56c14c987be8656bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0a8293668adef521586ebe99979134f8e41c9108c6d6cf316e6d66bcb5d72ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8c891422d6d327804ca33f3e8b8fe2b31189d0c24f658563709ff8914d9c97f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareClusterControlPlaneNodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterControlPlaneNodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fe6fc760b88f2813d7d75c44fb152cc7f13a7a6785fada72e5d9c662048d70b)
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
        :param enabled: Whether to enable control plane node auto resizing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#enabled GkeonpremVmwareCluster#enabled}
        '''
        value = GkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putAutoResizeConfig", [value]))

    @jsii.member(jsii_name="resetAutoResizeConfig")
    def reset_auto_resize_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoResizeConfig", []))

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
    @jsii.member(jsii_name="autoResizeConfig")
    def auto_resize_config(
        self,
    ) -> GkeonpremVmwareClusterControlPlaneNodeAutoResizeConfigOutputReference:
        return typing.cast(GkeonpremVmwareClusterControlPlaneNodeAutoResizeConfigOutputReference, jsii.get(self, "autoResizeConfig"))

    @builtins.property
    @jsii.member(jsii_name="vsphereConfig")
    def vsphere_config(
        self,
    ) -> "GkeonpremVmwareClusterControlPlaneNodeVsphereConfigList":
        return typing.cast("GkeonpremVmwareClusterControlPlaneNodeVsphereConfigList", jsii.get(self, "vsphereConfig"))

    @builtins.property
    @jsii.member(jsii_name="autoResizeConfigInput")
    def auto_resize_config_input(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig], jsii.get(self, "autoResizeConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9c9582ed13c16547ad44d29b013b19df585ee23bbd564c45fd1d1e67277ef688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26980b36b8a6b9515a175cd2163246ca33843f5f5f7af7bb11193f5e6a716f66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicas")
    def replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicas"))

    @replicas.setter
    def replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b16c08a076136a5cb8f24d4f08f33faa4f2715753b0d9c0ff34e7a2683e6f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremVmwareClusterControlPlaneNode]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterControlPlaneNode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterControlPlaneNode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bd2777cd6aa12360c765f4164873ea4afc446a99c361d917960426249e9cd84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterControlPlaneNodeVsphereConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremVmwareClusterControlPlaneNodeVsphereConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterControlPlaneNodeVsphereConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareClusterControlPlaneNodeVsphereConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterControlPlaneNodeVsphereConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd34587fcb7821643362c2bed8ee03da91078351750129fef505b224a339be1f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareClusterControlPlaneNodeVsphereConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92f7cc80048348b97fd8b4f5e5a3637da6c9c6b1c0310c63dfec80618c38ef6e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareClusterControlPlaneNodeVsphereConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a16e911e9ed9d7d6eacc350c27dc4312a355b3519254b2018b4669a4aa9c7972)
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
            type_hints = typing.get_type_hints(_typecheckingstub__942beeac3aeaf796f33a86f187f05b194cc46ce0a4f523be7e7f01bfc552442c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18ad22fda6b610938e9e2cd388a7957cca0659752bde76d74a35f540eca3a47d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareClusterControlPlaneNodeVsphereConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterControlPlaneNodeVsphereConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8950a689375971ece06a11561db8e895b0c61f38c16c393fd2780d670774959f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="datastore")
    def datastore(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datastore"))

    @builtins.property
    @jsii.member(jsii_name="storagePolicyName")
    def storage_policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storagePolicyName"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterControlPlaneNodeVsphereConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterControlPlaneNodeVsphereConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterControlPlaneNodeVsphereConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80db33b753e04f229386c2d6855d30b9597dfc1dfcf7776fd9fa3f50d44ab713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterDataplaneV2",
    jsii_struct_bases=[],
    name_mapping={
        "advanced_networking": "advancedNetworking",
        "dataplane_v2_enabled": "dataplaneV2Enabled",
        "windows_dataplane_v2_enabled": "windowsDataplaneV2Enabled",
    },
)
class GkeonpremVmwareClusterDataplaneV2:
    def __init__(
        self,
        *,
        advanced_networking: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dataplane_v2_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        windows_dataplane_v2_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param advanced_networking: Enable advanced networking which requires dataplane_v2_enabled to be set true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#advanced_networking GkeonpremVmwareCluster#advanced_networking}
        :param dataplane_v2_enabled: Enables Dataplane V2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#dataplane_v2_enabled GkeonpremVmwareCluster#dataplane_v2_enabled}
        :param windows_dataplane_v2_enabled: Enable Dataplane V2 for clusters with Windows nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#windows_dataplane_v2_enabled GkeonpremVmwareCluster#windows_dataplane_v2_enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8033138e8ca56d041e0133e136805534a6174859fd8db68dfa1274821c1cf9a)
            check_type(argname="argument advanced_networking", value=advanced_networking, expected_type=type_hints["advanced_networking"])
            check_type(argname="argument dataplane_v2_enabled", value=dataplane_v2_enabled, expected_type=type_hints["dataplane_v2_enabled"])
            check_type(argname="argument windows_dataplane_v2_enabled", value=windows_dataplane_v2_enabled, expected_type=type_hints["windows_dataplane_v2_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if advanced_networking is not None:
            self._values["advanced_networking"] = advanced_networking
        if dataplane_v2_enabled is not None:
            self._values["dataplane_v2_enabled"] = dataplane_v2_enabled
        if windows_dataplane_v2_enabled is not None:
            self._values["windows_dataplane_v2_enabled"] = windows_dataplane_v2_enabled

    @builtins.property
    def advanced_networking(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable advanced networking which requires dataplane_v2_enabled to be set true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#advanced_networking GkeonpremVmwareCluster#advanced_networking}
        '''
        result = self._values.get("advanced_networking")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dataplane_v2_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables Dataplane V2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#dataplane_v2_enabled GkeonpremVmwareCluster#dataplane_v2_enabled}
        '''
        result = self._values.get("dataplane_v2_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def windows_dataplane_v2_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable Dataplane V2 for clusters with Windows nodes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#windows_dataplane_v2_enabled GkeonpremVmwareCluster#windows_dataplane_v2_enabled}
        '''
        result = self._values.get("windows_dataplane_v2_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterDataplaneV2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareClusterDataplaneV2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterDataplaneV2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d0c93511dd32bdde85787ee09d3e2b81ed8df9a6fda04c70d498075d0da2d6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdvancedNetworking")
    def reset_advanced_networking(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedNetworking", []))

    @jsii.member(jsii_name="resetDataplaneV2Enabled")
    def reset_dataplane_v2_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataplaneV2Enabled", []))

    @jsii.member(jsii_name="resetWindowsDataplaneV2Enabled")
    def reset_windows_dataplane_v2_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowsDataplaneV2Enabled", []))

    @builtins.property
    @jsii.member(jsii_name="advancedNetworkingInput")
    def advanced_networking_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "advancedNetworkingInput"))

    @builtins.property
    @jsii.member(jsii_name="dataplaneV2EnabledInput")
    def dataplane_v2_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dataplaneV2EnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="windowsDataplaneV2EnabledInput")
    def windows_dataplane_v2_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "windowsDataplaneV2EnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="advancedNetworking")
    def advanced_networking(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "advancedNetworking"))

    @advanced_networking.setter
    def advanced_networking(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c0d6d5131c656a06f2306e54ff0bc0d109a097bc7a08d2913c621223241b808)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advancedNetworking", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataplaneV2Enabled")
    def dataplane_v2_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dataplaneV2Enabled"))

    @dataplane_v2_enabled.setter
    def dataplane_v2_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5276dc651b73d75a1e3394d24d6c7e2cf9f1ad1728ef3d9ddf657780c8efc9ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataplaneV2Enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="windowsDataplaneV2Enabled")
    def windows_dataplane_v2_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "windowsDataplaneV2Enabled"))

    @windows_dataplane_v2_enabled.setter
    def windows_dataplane_v2_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__722a21d6b919fb0a78ca16d9c046523b71eabbad5d316b22bced2b3fd58bfd2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowsDataplaneV2Enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremVmwareClusterDataplaneV2]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterDataplaneV2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterDataplaneV2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ba6e1b2dd40e03fa45ae85a5852059ace0f0504d62811c18afee98f874370d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterFleet",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremVmwareClusterFleet:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterFleet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareClusterFleetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterFleetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f5957d858efe169af64ac8046e1446a59f1aeda8597323a7a4f8eab06558eaa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GkeonpremVmwareClusterFleetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be75bae75c32be7a56cd90e1f9f69146c7741e65ba211738fa502899863dc634)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareClusterFleetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b87fda12f812b04b764aae216e12a6da58edc00cfeed4d7c0b6c0074cb68b3b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ca26f9ef17b4b069157dfc013fded26af3fc4ff5e5c22edb6a84e5d777fb3eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9313a85c37e438f0ca805ced89ada73566f71e56dbcf1d86de7ee198eba8879a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareClusterFleetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterFleetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f91565c0e2aa6bc57eda3f0cf970a1a4d40a5e916d039298ec233d194c0e94e)
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
    def internal_value(self) -> typing.Optional[GkeonpremVmwareClusterFleet]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterFleet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterFleet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce5c3e546400aa25b261ed7066f3e357d4e792efc71f7a0ff7c145b5df51eeb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterLoadBalancer",
    jsii_struct_bases=[],
    name_mapping={
        "f5_config": "f5Config",
        "manual_lb_config": "manualLbConfig",
        "metal_lb_config": "metalLbConfig",
        "vip_config": "vipConfig",
    },
)
class GkeonpremVmwareClusterLoadBalancer:
    def __init__(
        self,
        *,
        f5_config: typing.Optional[typing.Union["GkeonpremVmwareClusterLoadBalancerF5Config", typing.Dict[builtins.str, typing.Any]]] = None,
        manual_lb_config: typing.Optional[typing.Union["GkeonpremVmwareClusterLoadBalancerManualLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        metal_lb_config: typing.Optional[typing.Union["GkeonpremVmwareClusterLoadBalancerMetalLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        vip_config: typing.Optional[typing.Union["GkeonpremVmwareClusterLoadBalancerVipConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param f5_config: f5_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#f5_config GkeonpremVmwareCluster#f5_config}
        :param manual_lb_config: manual_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#manual_lb_config GkeonpremVmwareCluster#manual_lb_config}
        :param metal_lb_config: metal_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#metal_lb_config GkeonpremVmwareCluster#metal_lb_config}
        :param vip_config: vip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#vip_config GkeonpremVmwareCluster#vip_config}
        '''
        if isinstance(f5_config, dict):
            f5_config = GkeonpremVmwareClusterLoadBalancerF5Config(**f5_config)
        if isinstance(manual_lb_config, dict):
            manual_lb_config = GkeonpremVmwareClusterLoadBalancerManualLbConfig(**manual_lb_config)
        if isinstance(metal_lb_config, dict):
            metal_lb_config = GkeonpremVmwareClusterLoadBalancerMetalLbConfig(**metal_lb_config)
        if isinstance(vip_config, dict):
            vip_config = GkeonpremVmwareClusterLoadBalancerVipConfig(**vip_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__385bd31358c395c69d12a8e10ca67b2863913df97887fb65fe23effa83de6177)
            check_type(argname="argument f5_config", value=f5_config, expected_type=type_hints["f5_config"])
            check_type(argname="argument manual_lb_config", value=manual_lb_config, expected_type=type_hints["manual_lb_config"])
            check_type(argname="argument metal_lb_config", value=metal_lb_config, expected_type=type_hints["metal_lb_config"])
            check_type(argname="argument vip_config", value=vip_config, expected_type=type_hints["vip_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if f5_config is not None:
            self._values["f5_config"] = f5_config
        if manual_lb_config is not None:
            self._values["manual_lb_config"] = manual_lb_config
        if metal_lb_config is not None:
            self._values["metal_lb_config"] = metal_lb_config
        if vip_config is not None:
            self._values["vip_config"] = vip_config

    @builtins.property
    def f5_config(
        self,
    ) -> typing.Optional["GkeonpremVmwareClusterLoadBalancerF5Config"]:
        '''f5_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#f5_config GkeonpremVmwareCluster#f5_config}
        '''
        result = self._values.get("f5_config")
        return typing.cast(typing.Optional["GkeonpremVmwareClusterLoadBalancerF5Config"], result)

    @builtins.property
    def manual_lb_config(
        self,
    ) -> typing.Optional["GkeonpremVmwareClusterLoadBalancerManualLbConfig"]:
        '''manual_lb_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#manual_lb_config GkeonpremVmwareCluster#manual_lb_config}
        '''
        result = self._values.get("manual_lb_config")
        return typing.cast(typing.Optional["GkeonpremVmwareClusterLoadBalancerManualLbConfig"], result)

    @builtins.property
    def metal_lb_config(
        self,
    ) -> typing.Optional["GkeonpremVmwareClusterLoadBalancerMetalLbConfig"]:
        '''metal_lb_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#metal_lb_config GkeonpremVmwareCluster#metal_lb_config}
        '''
        result = self._values.get("metal_lb_config")
        return typing.cast(typing.Optional["GkeonpremVmwareClusterLoadBalancerMetalLbConfig"], result)

    @builtins.property
    def vip_config(
        self,
    ) -> typing.Optional["GkeonpremVmwareClusterLoadBalancerVipConfig"]:
        '''vip_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#vip_config GkeonpremVmwareCluster#vip_config}
        '''
        result = self._values.get("vip_config")
        return typing.cast(typing.Optional["GkeonpremVmwareClusterLoadBalancerVipConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterLoadBalancer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterLoadBalancerF5Config",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "partition": "partition",
        "snat_pool": "snatPool",
    },
)
class GkeonpremVmwareClusterLoadBalancerF5Config:
    def __init__(
        self,
        *,
        address: typing.Optional[builtins.str] = None,
        partition: typing.Optional[builtins.str] = None,
        snat_pool: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: The load balancer's IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#address GkeonpremVmwareCluster#address}
        :param partition: he preexisting partition to be used by the load balancer. T his partition is usually created for the admin cluster for example: 'my-f5-admin-partition'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#partition GkeonpremVmwareCluster#partition}
        :param snat_pool: The pool name. Only necessary, if using SNAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#snat_pool GkeonpremVmwareCluster#snat_pool}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45791af81c5564a5a77e6780023b4a87d96d503938a52c88fef048eb61344a78)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#address GkeonpremVmwareCluster#address}
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partition(self) -> typing.Optional[builtins.str]:
        '''he preexisting partition to be used by the load balancer.

        T
        his partition is usually created for the admin cluster for example:
        'my-f5-admin-partition'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#partition GkeonpremVmwareCluster#partition}
        '''
        result = self._values.get("partition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snat_pool(self) -> typing.Optional[builtins.str]:
        '''The pool name. Only necessary, if using SNAT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#snat_pool GkeonpremVmwareCluster#snat_pool}
        '''
        result = self._values.get("snat_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterLoadBalancerF5Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareClusterLoadBalancerF5ConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterLoadBalancerF5ConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83b703aa54d96c18bf12f5dc800a953ccfa4efa7183589c207bf92ed11e9bac7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1176ff4ffb938cf62a391450c8712e2b28ef8f61c8e68211ec5a06a93c683351)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partition")
    def partition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partition"))

    @partition.setter
    def partition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdc3758fb7e1fa1a8e5fc7c340a3f657e81e1c99cbad8fcffc541031540887ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snatPool")
    def snat_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snatPool"))

    @snat_pool.setter
    def snat_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d06a5af73721cb19e9344241a17570b9e0f0610e8be7ecf4ab6344eabbbeca6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snatPool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterLoadBalancerF5Config]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterLoadBalancerF5Config], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterLoadBalancerF5Config],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a71f7cc177984579f0d0cba89044170ac5655cf0c187b43d2e6740e2ff44ae02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterLoadBalancerManualLbConfig",
    jsii_struct_bases=[],
    name_mapping={
        "control_plane_node_port": "controlPlaneNodePort",
        "ingress_http_node_port": "ingressHttpNodePort",
        "ingress_https_node_port": "ingressHttpsNodePort",
        "konnectivity_server_node_port": "konnectivityServerNodePort",
    },
)
class GkeonpremVmwareClusterLoadBalancerManualLbConfig:
    def __init__(
        self,
        *,
        control_plane_node_port: typing.Optional[jsii.Number] = None,
        ingress_http_node_port: typing.Optional[jsii.Number] = None,
        ingress_https_node_port: typing.Optional[jsii.Number] = None,
        konnectivity_server_node_port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param control_plane_node_port: NodePort for control plane service. The Kubernetes API server in the admin cluster is implemented as a Service of type NodePort (ex. 30968). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#control_plane_node_port GkeonpremVmwareCluster#control_plane_node_port}
        :param ingress_http_node_port: NodePort for ingress service's http. The ingress service in the admin cluster is implemented as a Service of type NodePort (ex. 32527). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ingress_http_node_port GkeonpremVmwareCluster#ingress_http_node_port}
        :param ingress_https_node_port: NodePort for ingress service's https. The ingress service in the admin cluster is implemented as a Service of type NodePort (ex. 30139). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ingress_https_node_port GkeonpremVmwareCluster#ingress_https_node_port}
        :param konnectivity_server_node_port: NodePort for konnectivity server service running as a sidecar in each kube-apiserver pod (ex. 30564). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#konnectivity_server_node_port GkeonpremVmwareCluster#konnectivity_server_node_port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6426981c6a21348236a770408e39fb4fb78f4fea7cf88db212820c0b53df85a5)
            check_type(argname="argument control_plane_node_port", value=control_plane_node_port, expected_type=type_hints["control_plane_node_port"])
            check_type(argname="argument ingress_http_node_port", value=ingress_http_node_port, expected_type=type_hints["ingress_http_node_port"])
            check_type(argname="argument ingress_https_node_port", value=ingress_https_node_port, expected_type=type_hints["ingress_https_node_port"])
            check_type(argname="argument konnectivity_server_node_port", value=konnectivity_server_node_port, expected_type=type_hints["konnectivity_server_node_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if control_plane_node_port is not None:
            self._values["control_plane_node_port"] = control_plane_node_port
        if ingress_http_node_port is not None:
            self._values["ingress_http_node_port"] = ingress_http_node_port
        if ingress_https_node_port is not None:
            self._values["ingress_https_node_port"] = ingress_https_node_port
        if konnectivity_server_node_port is not None:
            self._values["konnectivity_server_node_port"] = konnectivity_server_node_port

    @builtins.property
    def control_plane_node_port(self) -> typing.Optional[jsii.Number]:
        '''NodePort for control plane service.

        The Kubernetes API server in the admin
        cluster is implemented as a Service of type NodePort (ex. 30968).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#control_plane_node_port GkeonpremVmwareCluster#control_plane_node_port}
        '''
        result = self._values.get("control_plane_node_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ingress_http_node_port(self) -> typing.Optional[jsii.Number]:
        '''NodePort for ingress service's http.

        The ingress service in the admin
        cluster is implemented as a Service of type NodePort (ex. 32527).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ingress_http_node_port GkeonpremVmwareCluster#ingress_http_node_port}
        '''
        result = self._values.get("ingress_http_node_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ingress_https_node_port(self) -> typing.Optional[jsii.Number]:
        '''NodePort for ingress service's https.

        The ingress service in the admin
        cluster is implemented as a Service of type NodePort (ex. 30139).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ingress_https_node_port GkeonpremVmwareCluster#ingress_https_node_port}
        '''
        result = self._values.get("ingress_https_node_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def konnectivity_server_node_port(self) -> typing.Optional[jsii.Number]:
        '''NodePort for konnectivity server service running as a sidecar in each kube-apiserver pod (ex. 30564).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#konnectivity_server_node_port GkeonpremVmwareCluster#konnectivity_server_node_port}
        '''
        result = self._values.get("konnectivity_server_node_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterLoadBalancerManualLbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareClusterLoadBalancerManualLbConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterLoadBalancerManualLbConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0210af19126fe79ddcd4683d49a3a4ab0f58c134458d525b60489d1073650978)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
    @jsii.member(jsii_name="controlPlaneNodePort")
    def control_plane_node_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "controlPlaneNodePort"))

    @control_plane_node_port.setter
    def control_plane_node_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c4bd901b1ff8bfcc3d639500bbf3bcfbc2ff8827dbd780bceee1971a64c86a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneNodePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingressHttpNodePort")
    def ingress_http_node_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ingressHttpNodePort"))

    @ingress_http_node_port.setter
    def ingress_http_node_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5eb99ad36266a4d6f114888b2bf178f6bb65e3557b26a9f93ce49d6a417d4d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingressHttpNodePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingressHttpsNodePort")
    def ingress_https_node_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ingressHttpsNodePort"))

    @ingress_https_node_port.setter
    def ingress_https_node_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b333bdf1f2345d934104590f39ca946a386a02c88036b68e81fcf97f7974cefa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingressHttpsNodePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="konnectivityServerNodePort")
    def konnectivity_server_node_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "konnectivityServerNodePort"))

    @konnectivity_server_node_port.setter
    def konnectivity_server_node_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a83ab14953bf8d762b4213e5e4511cf5c7bd35dd0854fa9198c270d4b4e5b5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "konnectivityServerNodePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterLoadBalancerManualLbConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterLoadBalancerManualLbConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterLoadBalancerManualLbConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ed28cf0bc0567dc84bb4b6a51e7905276af2b02fd7f3cf84094bdc9119f6908)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterLoadBalancerMetalLbConfig",
    jsii_struct_bases=[],
    name_mapping={"address_pools": "addressPools"},
)
class GkeonpremVmwareClusterLoadBalancerMetalLbConfig:
    def __init__(
        self,
        *,
        address_pools: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param address_pools: address_pools block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#address_pools GkeonpremVmwareCluster#address_pools}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e02a92645463c74e5260591079dc41e1c76bc19806acc2a730d2ef8d26aef6)
            check_type(argname="argument address_pools", value=address_pools, expected_type=type_hints["address_pools"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address_pools": address_pools,
        }

    @builtins.property
    def address_pools(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools"]]:
        '''address_pools block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#address_pools GkeonpremVmwareCluster#address_pools}
        '''
        result = self._values.get("address_pools")
        assert result is not None, "Required property 'address_pools' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterLoadBalancerMetalLbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools",
    jsii_struct_bases=[],
    name_mapping={
        "addresses": "addresses",
        "pool": "pool",
        "avoid_buggy_ips": "avoidBuggyIps",
        "manual_assign": "manualAssign",
    },
)
class GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools:
    def __init__(
        self,
        *,
        addresses: typing.Sequence[builtins.str],
        pool: builtins.str,
        avoid_buggy_ips: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        manual_assign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param addresses: The addresses that are part of this pool. Each address must be either in the CIDR form (1.2.3.0/24) or range form (1.2.3.1-1.2.3.5). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#addresses GkeonpremVmwareCluster#addresses}
        :param pool: The name of the address pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#pool GkeonpremVmwareCluster#pool}
        :param avoid_buggy_ips: If true, avoid using IPs ending in .0 or .255. This avoids buggy consumer devices mistakenly dropping IPv4 traffic for those special IP addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#avoid_buggy_ips GkeonpremVmwareCluster#avoid_buggy_ips}
        :param manual_assign: If true, prevent IP addresses from being automatically assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#manual_assign GkeonpremVmwareCluster#manual_assign}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fecdc3b5a1c1f9542077fccb217694f3df796176dcce3a9e470cc9c7fa795cae)
            check_type(argname="argument addresses", value=addresses, expected_type=type_hints["addresses"])
            check_type(argname="argument pool", value=pool, expected_type=type_hints["pool"])
            check_type(argname="argument avoid_buggy_ips", value=avoid_buggy_ips, expected_type=type_hints["avoid_buggy_ips"])
            check_type(argname="argument manual_assign", value=manual_assign, expected_type=type_hints["manual_assign"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "addresses": addresses,
            "pool": pool,
        }
        if avoid_buggy_ips is not None:
            self._values["avoid_buggy_ips"] = avoid_buggy_ips
        if manual_assign is not None:
            self._values["manual_assign"] = manual_assign

    @builtins.property
    def addresses(self) -> typing.List[builtins.str]:
        '''The addresses that are part of this pool.

        Each address
        must be either in the CIDR form (1.2.3.0/24) or range
        form (1.2.3.1-1.2.3.5).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#addresses GkeonpremVmwareCluster#addresses}
        '''
        result = self._values.get("addresses")
        assert result is not None, "Required property 'addresses' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def pool(self) -> builtins.str:
        '''The name of the address pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#pool GkeonpremVmwareCluster#pool}
        '''
        result = self._values.get("pool")
        assert result is not None, "Required property 'pool' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def avoid_buggy_ips(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, avoid using IPs ending in .0 or .255. This avoids buggy consumer devices mistakenly dropping IPv4 traffic for those special IP addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#avoid_buggy_ips GkeonpremVmwareCluster#avoid_buggy_ips}
        '''
        result = self._values.get("avoid_buggy_ips")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def manual_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, prevent IP addresses from being automatically assigned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#manual_assign GkeonpremVmwareCluster#manual_assign}
        '''
        result = self._values.get("manual_assign")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPoolsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPoolsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc0eca5f0140ac5e6229a3edbc7cb59dfa4b7e9f9b5c149a6e95faca5d7933e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPoolsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__647307ef07b0b7824757730c6185d4c21ce6f14bb8fed679f60926d06ec42213)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPoolsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d721aa775ee80708ff450cb89e487d73ad9161a07d74c50c2498d124aea60a72)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d904a6e0e6a8a4e5f18eb8905ff4ba3383907f69ce3045f4c887ffb3e024877)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae33ed329faa34e8d306616edbb71bf69b1fe09f3094152db645780ab94fc246)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dd089d71e0e172e1f153665a480e0a54e3b0b3350962423cc835dd946df0c56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPoolsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPoolsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aaa0c4986b32a796133afebb11fef2961417422c9072a1b16e46f3d820ba7f0f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAvoidBuggyIps")
    def reset_avoid_buggy_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvoidBuggyIps", []))

    @jsii.member(jsii_name="resetManualAssign")
    def reset_manual_assign(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManualAssign", []))

    @builtins.property
    @jsii.member(jsii_name="addressesInput")
    def addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "addressesInput"))

    @builtins.property
    @jsii.member(jsii_name="avoidBuggyIpsInput")
    def avoid_buggy_ips_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "avoidBuggyIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="manualAssignInput")
    def manual_assign_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "manualAssignInput"))

    @builtins.property
    @jsii.member(jsii_name="poolInput")
    def pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "poolInput"))

    @builtins.property
    @jsii.member(jsii_name="addresses")
    def addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "addresses"))

    @addresses.setter
    def addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af61bdd39386286381fcfd27bed345109aa6496357cecbb8eaae6a57f4f838a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="avoidBuggyIps")
    def avoid_buggy_ips(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "avoidBuggyIps"))

    @avoid_buggy_ips.setter
    def avoid_buggy_ips(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__497f87850d7c7c77997e6700e3bbe116fc080c2704ab6ae16351760c5e11fd5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "avoidBuggyIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="manualAssign")
    def manual_assign(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "manualAssign"))

    @manual_assign.setter
    def manual_assign(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__233d46ee9f2d1521d5058e1e02ae15b57398430e210baa3cc50bada64bc5439d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manualAssign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pool")
    def pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pool"))

    @pool.setter
    def pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56303dea90effcd1e5f4c6f0f2054979a4f518a36e133e5da77f31322079051c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68201820d2754238d5fef3f3db4e5fac791bfe20674744cd3d05c7c69d619836)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareClusterLoadBalancerMetalLbConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterLoadBalancerMetalLbConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf9604237b2656dd99a4aab98f16daf513e70fdeffd7a8c3bf61194032bc6bb5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAddressPools")
    def put_address_pools(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54befca2e1c3b2e2f26f4aebb9a1a19a3ec625968a2e4b20bd17f86477558c59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAddressPools", [value]))

    @builtins.property
    @jsii.member(jsii_name="addressPools")
    def address_pools(
        self,
    ) -> GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPoolsList:
        return typing.cast(GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPoolsList, jsii.get(self, "addressPools"))

    @builtins.property
    @jsii.member(jsii_name="addressPoolsInput")
    def address_pools_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools]]], jsii.get(self, "addressPoolsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterLoadBalancerMetalLbConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterLoadBalancerMetalLbConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterLoadBalancerMetalLbConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d59f00f07b763bd969c9a817e6e8c9bb8d83a4a258eee6d16823ff1f59b69b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareClusterLoadBalancerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterLoadBalancerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44f8f98900030db4df59774569d989cab2d80acf729cbe1d9f1f2ad2c0fdb8a2)
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
        :param address: The load balancer's IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#address GkeonpremVmwareCluster#address}
        :param partition: he preexisting partition to be used by the load balancer. T his partition is usually created for the admin cluster for example: 'my-f5-admin-partition'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#partition GkeonpremVmwareCluster#partition}
        :param snat_pool: The pool name. Only necessary, if using SNAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#snat_pool GkeonpremVmwareCluster#snat_pool}
        '''
        value = GkeonpremVmwareClusterLoadBalancerF5Config(
            address=address, partition=partition, snat_pool=snat_pool
        )

        return typing.cast(None, jsii.invoke(self, "putF5Config", [value]))

    @jsii.member(jsii_name="putManualLbConfig")
    def put_manual_lb_config(
        self,
        *,
        control_plane_node_port: typing.Optional[jsii.Number] = None,
        ingress_http_node_port: typing.Optional[jsii.Number] = None,
        ingress_https_node_port: typing.Optional[jsii.Number] = None,
        konnectivity_server_node_port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param control_plane_node_port: NodePort for control plane service. The Kubernetes API server in the admin cluster is implemented as a Service of type NodePort (ex. 30968). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#control_plane_node_port GkeonpremVmwareCluster#control_plane_node_port}
        :param ingress_http_node_port: NodePort for ingress service's http. The ingress service in the admin cluster is implemented as a Service of type NodePort (ex. 32527). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ingress_http_node_port GkeonpremVmwareCluster#ingress_http_node_port}
        :param ingress_https_node_port: NodePort for ingress service's https. The ingress service in the admin cluster is implemented as a Service of type NodePort (ex. 30139). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ingress_https_node_port GkeonpremVmwareCluster#ingress_https_node_port}
        :param konnectivity_server_node_port: NodePort for konnectivity server service running as a sidecar in each kube-apiserver pod (ex. 30564). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#konnectivity_server_node_port GkeonpremVmwareCluster#konnectivity_server_node_port}
        '''
        value = GkeonpremVmwareClusterLoadBalancerManualLbConfig(
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
        address_pools: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param address_pools: address_pools block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#address_pools GkeonpremVmwareCluster#address_pools}
        '''
        value = GkeonpremVmwareClusterLoadBalancerMetalLbConfig(
            address_pools=address_pools
        )

        return typing.cast(None, jsii.invoke(self, "putMetalLbConfig", [value]))

    @jsii.member(jsii_name="putVipConfig")
    def put_vip_config(
        self,
        *,
        control_plane_vip: typing.Optional[builtins.str] = None,
        ingress_vip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param control_plane_vip: The VIP which you previously set aside for the Kubernetes API of this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#control_plane_vip GkeonpremVmwareCluster#control_plane_vip}
        :param ingress_vip: The VIP which you previously set aside for ingress traffic into this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ingress_vip GkeonpremVmwareCluster#ingress_vip}
        '''
        value = GkeonpremVmwareClusterLoadBalancerVipConfig(
            control_plane_vip=control_plane_vip, ingress_vip=ingress_vip
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

    @jsii.member(jsii_name="resetVipConfig")
    def reset_vip_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVipConfig", []))

    @builtins.property
    @jsii.member(jsii_name="f5Config")
    def f5_config(self) -> GkeonpremVmwareClusterLoadBalancerF5ConfigOutputReference:
        return typing.cast(GkeonpremVmwareClusterLoadBalancerF5ConfigOutputReference, jsii.get(self, "f5Config"))

    @builtins.property
    @jsii.member(jsii_name="manualLbConfig")
    def manual_lb_config(
        self,
    ) -> GkeonpremVmwareClusterLoadBalancerManualLbConfigOutputReference:
        return typing.cast(GkeonpremVmwareClusterLoadBalancerManualLbConfigOutputReference, jsii.get(self, "manualLbConfig"))

    @builtins.property
    @jsii.member(jsii_name="metalLbConfig")
    def metal_lb_config(
        self,
    ) -> GkeonpremVmwareClusterLoadBalancerMetalLbConfigOutputReference:
        return typing.cast(GkeonpremVmwareClusterLoadBalancerMetalLbConfigOutputReference, jsii.get(self, "metalLbConfig"))

    @builtins.property
    @jsii.member(jsii_name="vipConfig")
    def vip_config(
        self,
    ) -> "GkeonpremVmwareClusterLoadBalancerVipConfigOutputReference":
        return typing.cast("GkeonpremVmwareClusterLoadBalancerVipConfigOutputReference", jsii.get(self, "vipConfig"))

    @builtins.property
    @jsii.member(jsii_name="f5ConfigInput")
    def f5_config_input(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterLoadBalancerF5Config]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterLoadBalancerF5Config], jsii.get(self, "f5ConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="manualLbConfigInput")
    def manual_lb_config_input(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterLoadBalancerManualLbConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterLoadBalancerManualLbConfig], jsii.get(self, "manualLbConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="metalLbConfigInput")
    def metal_lb_config_input(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterLoadBalancerMetalLbConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterLoadBalancerMetalLbConfig], jsii.get(self, "metalLbConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="vipConfigInput")
    def vip_config_input(
        self,
    ) -> typing.Optional["GkeonpremVmwareClusterLoadBalancerVipConfig"]:
        return typing.cast(typing.Optional["GkeonpremVmwareClusterLoadBalancerVipConfig"], jsii.get(self, "vipConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremVmwareClusterLoadBalancer]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterLoadBalancer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterLoadBalancer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24aef73aed085fcad331b15f38fb23ca9166db84c67fc3714bd36420e85fd5e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterLoadBalancerVipConfig",
    jsii_struct_bases=[],
    name_mapping={"control_plane_vip": "controlPlaneVip", "ingress_vip": "ingressVip"},
)
class GkeonpremVmwareClusterLoadBalancerVipConfig:
    def __init__(
        self,
        *,
        control_plane_vip: typing.Optional[builtins.str] = None,
        ingress_vip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param control_plane_vip: The VIP which you previously set aside for the Kubernetes API of this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#control_plane_vip GkeonpremVmwareCluster#control_plane_vip}
        :param ingress_vip: The VIP which you previously set aside for ingress traffic into this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ingress_vip GkeonpremVmwareCluster#ingress_vip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcaa3472519161dd150a8a8153b9b54d2ed909bcbbfed01a6d5ee2ad39b45c8e)
            check_type(argname="argument control_plane_vip", value=control_plane_vip, expected_type=type_hints["control_plane_vip"])
            check_type(argname="argument ingress_vip", value=ingress_vip, expected_type=type_hints["ingress_vip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if control_plane_vip is not None:
            self._values["control_plane_vip"] = control_plane_vip
        if ingress_vip is not None:
            self._values["ingress_vip"] = ingress_vip

    @builtins.property
    def control_plane_vip(self) -> typing.Optional[builtins.str]:
        '''The VIP which you previously set aside for the Kubernetes API of this cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#control_plane_vip GkeonpremVmwareCluster#control_plane_vip}
        '''
        result = self._values.get("control_plane_vip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ingress_vip(self) -> typing.Optional[builtins.str]:
        '''The VIP which you previously set aside for ingress traffic into this cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ingress_vip GkeonpremVmwareCluster#ingress_vip}
        '''
        result = self._values.get("ingress_vip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterLoadBalancerVipConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareClusterLoadBalancerVipConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterLoadBalancerVipConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b6f9d0974ad85b782590e0032cf0374f537a42e0ae0f94b451b7ea9522a97f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetControlPlaneVip")
    def reset_control_plane_vip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControlPlaneVip", []))

    @jsii.member(jsii_name="resetIngressVip")
    def reset_ingress_vip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressVip", []))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneVipInput")
    def control_plane_vip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "controlPlaneVipInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressVipInput")
    def ingress_vip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ingressVipInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneVip")
    def control_plane_vip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "controlPlaneVip"))

    @control_plane_vip.setter
    def control_plane_vip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac5f1afccdae9bb0c9cecb235b116e920f7ce1cfdd9edf41ecc71a804a5e5898)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneVip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingressVip")
    def ingress_vip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ingressVip"))

    @ingress_vip.setter
    def ingress_vip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d731c5c082147d81d2f42f6c4fac70c37304fc78402e9740ccf8f5632debb90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingressVip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterLoadBalancerVipConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterLoadBalancerVipConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterLoadBalancerVipConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__326d282d86ce0e7b0d98bd34e0c0ff14a37036e7feaa540f7e048bb31e30fcc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={
        "pod_address_cidr_blocks": "podAddressCidrBlocks",
        "service_address_cidr_blocks": "serviceAddressCidrBlocks",
        "control_plane_v2_config": "controlPlaneV2Config",
        "dhcp_ip_config": "dhcpIpConfig",
        "host_config": "hostConfig",
        "static_ip_config": "staticIpConfig",
        "vcenter_network": "vcenterNetwork",
    },
)
class GkeonpremVmwareClusterNetworkConfig:
    def __init__(
        self,
        *,
        pod_address_cidr_blocks: typing.Sequence[builtins.str],
        service_address_cidr_blocks: typing.Sequence[builtins.str],
        control_plane_v2_config: typing.Optional[typing.Union["GkeonpremVmwareClusterNetworkConfigControlPlaneV2Config", typing.Dict[builtins.str, typing.Any]]] = None,
        dhcp_ip_config: typing.Optional[typing.Union["GkeonpremVmwareClusterNetworkConfigDhcpIpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        host_config: typing.Optional[typing.Union["GkeonpremVmwareClusterNetworkConfigHostConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        static_ip_config: typing.Optional[typing.Union["GkeonpremVmwareClusterNetworkConfigStaticIpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        vcenter_network: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pod_address_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#pod_address_cidr_blocks GkeonpremVmwareCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported.. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#service_address_cidr_blocks GkeonpremVmwareCluster#service_address_cidr_blocks}
        :param control_plane_v2_config: control_plane_v2_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#control_plane_v2_config GkeonpremVmwareCluster#control_plane_v2_config}
        :param dhcp_ip_config: dhcp_ip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#dhcp_ip_config GkeonpremVmwareCluster#dhcp_ip_config}
        :param host_config: host_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#host_config GkeonpremVmwareCluster#host_config}
        :param static_ip_config: static_ip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#static_ip_config GkeonpremVmwareCluster#static_ip_config}
        :param vcenter_network: vcenter_network specifies vCenter network name. Inherited from the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#vcenter_network GkeonpremVmwareCluster#vcenter_network}
        '''
        if isinstance(control_plane_v2_config, dict):
            control_plane_v2_config = GkeonpremVmwareClusterNetworkConfigControlPlaneV2Config(**control_plane_v2_config)
        if isinstance(dhcp_ip_config, dict):
            dhcp_ip_config = GkeonpremVmwareClusterNetworkConfigDhcpIpConfig(**dhcp_ip_config)
        if isinstance(host_config, dict):
            host_config = GkeonpremVmwareClusterNetworkConfigHostConfig(**host_config)
        if isinstance(static_ip_config, dict):
            static_ip_config = GkeonpremVmwareClusterNetworkConfigStaticIpConfig(**static_ip_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb7ccf4b01cf2237fdab8c7ea9b6a956a37779aa5b6e7395d0989a680cbe062a)
            check_type(argname="argument pod_address_cidr_blocks", value=pod_address_cidr_blocks, expected_type=type_hints["pod_address_cidr_blocks"])
            check_type(argname="argument service_address_cidr_blocks", value=service_address_cidr_blocks, expected_type=type_hints["service_address_cidr_blocks"])
            check_type(argname="argument control_plane_v2_config", value=control_plane_v2_config, expected_type=type_hints["control_plane_v2_config"])
            check_type(argname="argument dhcp_ip_config", value=dhcp_ip_config, expected_type=type_hints["dhcp_ip_config"])
            check_type(argname="argument host_config", value=host_config, expected_type=type_hints["host_config"])
            check_type(argname="argument static_ip_config", value=static_ip_config, expected_type=type_hints["static_ip_config"])
            check_type(argname="argument vcenter_network", value=vcenter_network, expected_type=type_hints["vcenter_network"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pod_address_cidr_blocks": pod_address_cidr_blocks,
            "service_address_cidr_blocks": service_address_cidr_blocks,
        }
        if control_plane_v2_config is not None:
            self._values["control_plane_v2_config"] = control_plane_v2_config
        if dhcp_ip_config is not None:
            self._values["dhcp_ip_config"] = dhcp_ip_config
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#pod_address_cidr_blocks GkeonpremVmwareCluster#pod_address_cidr_blocks}
        '''
        result = self._values.get("pod_address_cidr_blocks")
        assert result is not None, "Required property 'pod_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        '''All services in the cluster are assigned an RFC1918 IPv4 address from these ranges.

        Only a single range is supported.. This field
        cannot be changed after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#service_address_cidr_blocks GkeonpremVmwareCluster#service_address_cidr_blocks}
        '''
        result = self._values.get("service_address_cidr_blocks")
        assert result is not None, "Required property 'service_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def control_plane_v2_config(
        self,
    ) -> typing.Optional["GkeonpremVmwareClusterNetworkConfigControlPlaneV2Config"]:
        '''control_plane_v2_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#control_plane_v2_config GkeonpremVmwareCluster#control_plane_v2_config}
        '''
        result = self._values.get("control_plane_v2_config")
        return typing.cast(typing.Optional["GkeonpremVmwareClusterNetworkConfigControlPlaneV2Config"], result)

    @builtins.property
    def dhcp_ip_config(
        self,
    ) -> typing.Optional["GkeonpremVmwareClusterNetworkConfigDhcpIpConfig"]:
        '''dhcp_ip_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#dhcp_ip_config GkeonpremVmwareCluster#dhcp_ip_config}
        '''
        result = self._values.get("dhcp_ip_config")
        return typing.cast(typing.Optional["GkeonpremVmwareClusterNetworkConfigDhcpIpConfig"], result)

    @builtins.property
    def host_config(
        self,
    ) -> typing.Optional["GkeonpremVmwareClusterNetworkConfigHostConfig"]:
        '''host_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#host_config GkeonpremVmwareCluster#host_config}
        '''
        result = self._values.get("host_config")
        return typing.cast(typing.Optional["GkeonpremVmwareClusterNetworkConfigHostConfig"], result)

    @builtins.property
    def static_ip_config(
        self,
    ) -> typing.Optional["GkeonpremVmwareClusterNetworkConfigStaticIpConfig"]:
        '''static_ip_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#static_ip_config GkeonpremVmwareCluster#static_ip_config}
        '''
        result = self._values.get("static_ip_config")
        return typing.cast(typing.Optional["GkeonpremVmwareClusterNetworkConfigStaticIpConfig"], result)

    @builtins.property
    def vcenter_network(self) -> typing.Optional[builtins.str]:
        '''vcenter_network specifies vCenter network name. Inherited from the admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#vcenter_network GkeonpremVmwareCluster#vcenter_network}
        '''
        result = self._values.get("vcenter_network")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterNetworkConfigControlPlaneV2Config",
    jsii_struct_bases=[],
    name_mapping={"control_plane_ip_block": "controlPlaneIpBlock"},
)
class GkeonpremVmwareClusterNetworkConfigControlPlaneV2Config:
    def __init__(
        self,
        *,
        control_plane_ip_block: typing.Optional[typing.Union["GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param control_plane_ip_block: control_plane_ip_block block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#control_plane_ip_block GkeonpremVmwareCluster#control_plane_ip_block}
        '''
        if isinstance(control_plane_ip_block, dict):
            control_plane_ip_block = GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock(**control_plane_ip_block)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ffec5f1627aa55b6bafb05d0a7f42a275df426ff3775b108c0d3778c8f0b24e)
            check_type(argname="argument control_plane_ip_block", value=control_plane_ip_block, expected_type=type_hints["control_plane_ip_block"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if control_plane_ip_block is not None:
            self._values["control_plane_ip_block"] = control_plane_ip_block

    @builtins.property
    def control_plane_ip_block(
        self,
    ) -> typing.Optional["GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock"]:
        '''control_plane_ip_block block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#control_plane_ip_block GkeonpremVmwareCluster#control_plane_ip_block}
        '''
        result = self._values.get("control_plane_ip_block")
        return typing.cast(typing.Optional["GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterNetworkConfigControlPlaneV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock",
    jsii_struct_bases=[],
    name_mapping={"gateway": "gateway", "ips": "ips", "netmask": "netmask"},
)
class GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock:
    def __init__(
        self,
        *,
        gateway: typing.Optional[builtins.str] = None,
        ips: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps", typing.Dict[builtins.str, typing.Any]]]]] = None,
        netmask: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gateway: The network gateway used by the VMware User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#gateway GkeonpremVmwareCluster#gateway}
        :param ips: ips block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ips GkeonpremVmwareCluster#ips}
        :param netmask: The netmask used by the VMware User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#netmask GkeonpremVmwareCluster#netmask}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c284ff9c2b3b9c6f2ff51bfee5152c855c7c10c64f59eabe024241298c57d98d)
            check_type(argname="argument gateway", value=gateway, expected_type=type_hints["gateway"])
            check_type(argname="argument ips", value=ips, expected_type=type_hints["ips"])
            check_type(argname="argument netmask", value=netmask, expected_type=type_hints["netmask"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gateway is not None:
            self._values["gateway"] = gateway
        if ips is not None:
            self._values["ips"] = ips
        if netmask is not None:
            self._values["netmask"] = netmask

    @builtins.property
    def gateway(self) -> typing.Optional[builtins.str]:
        '''The network gateway used by the VMware User Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#gateway GkeonpremVmwareCluster#gateway}
        '''
        result = self._values.get("gateway")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ips(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps"]]]:
        '''ips block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ips GkeonpremVmwareCluster#ips}
        '''
        result = self._values.get("ips")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps"]]], result)

    @builtins.property
    def netmask(self) -> typing.Optional[builtins.str]:
        '''The netmask used by the VMware User Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#netmask GkeonpremVmwareCluster#netmask}
        '''
        result = self._values.get("netmask")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps",
    jsii_struct_bases=[],
    name_mapping={"hostname": "hostname", "ip": "ip"},
)
class GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps:
    def __init__(
        self,
        *,
        hostname: typing.Optional[builtins.str] = None,
        ip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hostname: Hostname of the machine. VM's name will be used if this field is empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#hostname GkeonpremVmwareCluster#hostname}
        :param ip: IP could be an IP address (like 1.2.3.4) or a CIDR (like 1.2.3.0/24). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ip GkeonpremVmwareCluster#ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fda6103187e645524b2d95224a8e3d1dc4dcbb30be217d79901bbc8304c3ccc8)
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hostname is not None:
            self._values["hostname"] = hostname
        if ip is not None:
            self._values["ip"] = ip

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''Hostname of the machine. VM's name will be used if this field is empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#hostname GkeonpremVmwareCluster#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip(self) -> typing.Optional[builtins.str]:
        '''IP could be an IP address (like 1.2.3.4) or a CIDR (like 1.2.3.0/24).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ip GkeonpremVmwareCluster#ip}
        '''
        result = self._values.get("ip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIpsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIpsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77111cdbd24e4902c89a7133c5fa753ea7b302949b77e41ac095b06a9c2a2913)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIpsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdfcdcad38c447388616cb1f47736fec0548957f0980184f39340b61ae6844e3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIpsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c53f2cbc9b918a78fd6a1f901e44d0204dde2d4542847dcb678683c17aca3ade)
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
            type_hints = typing.get_type_hints(_typecheckingstub__602ad97d65e85f0b733a8a03214774e07ff6b5faafd800860b02ecbb91b97e97)
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
            type_hints = typing.get_type_hints(_typecheckingstub__323840574298d4261d6b2da63edb566b9f41c016511ffb2d9feb84768725fbe9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a035108e9035c0e55b93ebd24302ef0d626b035746ffdd22d46ae24b2591cc30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIpsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIpsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38bdbe15d3baaa51964b58040420ef7526ace86ef3b6f00b3ba3ee96ec2ae375)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetHostname")
    def reset_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostname", []))

    @jsii.member(jsii_name="resetIp")
    def reset_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIp", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1c818559420fb4adf727479bb519224b3e436ec73c890d3c209e808503119285)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5dca2c26e70caa51a1febb4c2470cf1bab75fa78a699c555f8c32570c591597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d8b199d03e25dde06e0083782ea72c3c63fc8e43e413232666abf8478f349dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbb5f16b9141d8806fbc9d5744135d7815dff45e49627b4a63b148a1068a5806)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIps")
    def put_ips(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f68c21eb1250e77702db5252cdae353f35837d178ed6652b739bb9e25820c74d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIps", [value]))

    @jsii.member(jsii_name="resetGateway")
    def reset_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGateway", []))

    @jsii.member(jsii_name="resetIps")
    def reset_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIps", []))

    @jsii.member(jsii_name="resetNetmask")
    def reset_netmask(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetmask", []))

    @builtins.property
    @jsii.member(jsii_name="ips")
    def ips(
        self,
    ) -> GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIpsList:
        return typing.cast(GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIpsList, jsii.get(self, "ips"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="ipsInput")
    def ips_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps]]], jsii.get(self, "ipsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6d7910d1c0ca941e832ca499649a04f93f427cee0fc7079bd84dfb0fa6e8c892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateway", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netmask")
    def netmask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netmask"))

    @netmask.setter
    def netmask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4dcc67c538603d03095cfac7c6759e2a96af3bc525b49a8e11dd07dbfee8416)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netmask", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__933703632b48ee55172417ef4cce329be34b04b8bff6a54a6649ccc902da9645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37dddb62e42392efb8b91e89a3bda3479c155fd0d9907d89be654520a863143f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putControlPlaneIpBlock")
    def put_control_plane_ip_block(
        self,
        *,
        gateway: typing.Optional[builtins.str] = None,
        ips: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps, typing.Dict[builtins.str, typing.Any]]]]] = None,
        netmask: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gateway: The network gateway used by the VMware User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#gateway GkeonpremVmwareCluster#gateway}
        :param ips: ips block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ips GkeonpremVmwareCluster#ips}
        :param netmask: The netmask used by the VMware User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#netmask GkeonpremVmwareCluster#netmask}
        '''
        value = GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock(
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
    ) -> GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockOutputReference:
        return typing.cast(GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockOutputReference, jsii.get(self, "controlPlaneIpBlock"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneIpBlockInput")
    def control_plane_ip_block_input(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock], jsii.get(self, "controlPlaneIpBlockInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterNetworkConfigControlPlaneV2Config]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterNetworkConfigControlPlaneV2Config], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterNetworkConfigControlPlaneV2Config],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df749cd5b1c6f51852652bea2b840edffaa82c15b22047af452f5d2d56d3805d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterNetworkConfigDhcpIpConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GkeonpremVmwareClusterNetworkConfigDhcpIpConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: enabled is a flag to mark if DHCP IP allocation is used for VMware user clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#enabled GkeonpremVmwareCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a549e144a2f4c626331a05de1587127b72995ced179e39a62eb7debfbbcd9eb)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''enabled is a flag to mark if DHCP IP allocation is used for VMware user clusters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#enabled GkeonpremVmwareCluster#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterNetworkConfigDhcpIpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareClusterNetworkConfigDhcpIpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterNetworkConfigDhcpIpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3234cadd1f9ae4d3e0021ed933de8abd093ec17b176970d5a7c168c5a46d3654)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d1662ce7a224f4484f8c9b4c758c6a5ef3873fdf3a0729780b3dcd9b82c061b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterNetworkConfigDhcpIpConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterNetworkConfigDhcpIpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterNetworkConfigDhcpIpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bf3d424b26cb5b8071d488581f6f2d16c966da74503a20c0d5dfdd47a160b52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterNetworkConfigHostConfig",
    jsii_struct_bases=[],
    name_mapping={
        "dns_search_domains": "dnsSearchDomains",
        "dns_servers": "dnsServers",
        "ntp_servers": "ntpServers",
    },
)
class GkeonpremVmwareClusterNetworkConfigHostConfig:
    def __init__(
        self,
        *,
        dns_search_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        ntp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param dns_search_domains: DNS search domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#dns_search_domains GkeonpremVmwareCluster#dns_search_domains}
        :param dns_servers: DNS servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#dns_servers GkeonpremVmwareCluster#dns_servers}
        :param ntp_servers: NTP servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ntp_servers GkeonpremVmwareCluster#ntp_servers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dedaa27b8a60ffaffc015054587c49c688f02dbca9b6f0d64fb6e8c77b0d3f91)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#dns_search_domains GkeonpremVmwareCluster#dns_search_domains}
        '''
        result = self._values.get("dns_search_domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dns_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''DNS servers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#dns_servers GkeonpremVmwareCluster#dns_servers}
        '''
        result = self._values.get("dns_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ntp_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''NTP servers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ntp_servers GkeonpremVmwareCluster#ntp_servers}
        '''
        result = self._values.get("ntp_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterNetworkConfigHostConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareClusterNetworkConfigHostConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterNetworkConfigHostConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e209f17895fea9cc05e3c2d6f3cfe6ac3371eadedac178b4a6da3beba402d51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d880d7bca53f4468913bec19a8c909f7374013e496068808d68ad3cd67e096c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsSearchDomains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsServers")
    def dns_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dnsServers"))

    @dns_servers.setter
    def dns_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66cda2416e8ce03beef83545e11f214364701a1daa11d6a971b821c9ee9c989a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ntpServers")
    def ntp_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ntpServers"))

    @ntp_servers.setter
    def ntp_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bce3c2130f5ba4be7f0b1626c1f2996acc6fde45decc3ffedc641df1d9257010)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ntpServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterNetworkConfigHostConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterNetworkConfigHostConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterNetworkConfigHostConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67b51ed84d88d8ac9a1768ee7a1694ee5df7b3e468fd5e6518869fbe12dc430b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareClusterNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31b3328b995375f6b80b4ad27da3475966bd46e633d4ee097fb0a513b0c0080e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putControlPlaneV2Config")
    def put_control_plane_v2_config(
        self,
        *,
        control_plane_ip_block: typing.Optional[typing.Union[GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param control_plane_ip_block: control_plane_ip_block block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#control_plane_ip_block GkeonpremVmwareCluster#control_plane_ip_block}
        '''
        value = GkeonpremVmwareClusterNetworkConfigControlPlaneV2Config(
            control_plane_ip_block=control_plane_ip_block
        )

        return typing.cast(None, jsii.invoke(self, "putControlPlaneV2Config", [value]))

    @jsii.member(jsii_name="putDhcpIpConfig")
    def put_dhcp_ip_config(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: enabled is a flag to mark if DHCP IP allocation is used for VMware user clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#enabled GkeonpremVmwareCluster#enabled}
        '''
        value = GkeonpremVmwareClusterNetworkConfigDhcpIpConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putDhcpIpConfig", [value]))

    @jsii.member(jsii_name="putHostConfig")
    def put_host_config(
        self,
        *,
        dns_search_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        ntp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param dns_search_domains: DNS search domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#dns_search_domains GkeonpremVmwareCluster#dns_search_domains}
        :param dns_servers: DNS servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#dns_servers GkeonpremVmwareCluster#dns_servers}
        :param ntp_servers: NTP servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ntp_servers GkeonpremVmwareCluster#ntp_servers}
        '''
        value = GkeonpremVmwareClusterNetworkConfigHostConfig(
            dns_search_domains=dns_search_domains,
            dns_servers=dns_servers,
            ntp_servers=ntp_servers,
        )

        return typing.cast(None, jsii.invoke(self, "putHostConfig", [value]))

    @jsii.member(jsii_name="putStaticIpConfig")
    def put_static_ip_config(
        self,
        *,
        ip_blocks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param ip_blocks: ip_blocks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ip_blocks GkeonpremVmwareCluster#ip_blocks}
        '''
        value = GkeonpremVmwareClusterNetworkConfigStaticIpConfig(ip_blocks=ip_blocks)

        return typing.cast(None, jsii.invoke(self, "putStaticIpConfig", [value]))

    @jsii.member(jsii_name="resetControlPlaneV2Config")
    def reset_control_plane_v2_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControlPlaneV2Config", []))

    @jsii.member(jsii_name="resetDhcpIpConfig")
    def reset_dhcp_ip_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDhcpIpConfig", []))

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
    @jsii.member(jsii_name="controlPlaneV2Config")
    def control_plane_v2_config(
        self,
    ) -> GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigOutputReference:
        return typing.cast(GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigOutputReference, jsii.get(self, "controlPlaneV2Config"))

    @builtins.property
    @jsii.member(jsii_name="dhcpIpConfig")
    def dhcp_ip_config(
        self,
    ) -> GkeonpremVmwareClusterNetworkConfigDhcpIpConfigOutputReference:
        return typing.cast(GkeonpremVmwareClusterNetworkConfigDhcpIpConfigOutputReference, jsii.get(self, "dhcpIpConfig"))

    @builtins.property
    @jsii.member(jsii_name="hostConfig")
    def host_config(
        self,
    ) -> GkeonpremVmwareClusterNetworkConfigHostConfigOutputReference:
        return typing.cast(GkeonpremVmwareClusterNetworkConfigHostConfigOutputReference, jsii.get(self, "hostConfig"))

    @builtins.property
    @jsii.member(jsii_name="staticIpConfig")
    def static_ip_config(
        self,
    ) -> "GkeonpremVmwareClusterNetworkConfigStaticIpConfigOutputReference":
        return typing.cast("GkeonpremVmwareClusterNetworkConfigStaticIpConfigOutputReference", jsii.get(self, "staticIpConfig"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneV2ConfigInput")
    def control_plane_v2_config_input(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterNetworkConfigControlPlaneV2Config]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterNetworkConfigControlPlaneV2Config], jsii.get(self, "controlPlaneV2ConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="dhcpIpConfigInput")
    def dhcp_ip_config_input(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterNetworkConfigDhcpIpConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterNetworkConfigDhcpIpConfig], jsii.get(self, "dhcpIpConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="hostConfigInput")
    def host_config_input(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterNetworkConfigHostConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterNetworkConfigHostConfig], jsii.get(self, "hostConfigInput"))

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
    ) -> typing.Optional["GkeonpremVmwareClusterNetworkConfigStaticIpConfig"]:
        return typing.cast(typing.Optional["GkeonpremVmwareClusterNetworkConfigStaticIpConfig"], jsii.get(self, "staticIpConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__aa17e258516fb912da5e5356986d5da45a6447ce5a9f77f6865c0470c6b75975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAddressCidrBlocks")
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceAddressCidrBlocks"))

    @service_address_cidr_blocks.setter
    def service_address_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a756163df81164816c6eafacdea6404ce21a02e5b6f9297c8c0332cabbe8be3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vcenterNetwork")
    def vcenter_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vcenterNetwork"))

    @vcenter_network.setter
    def vcenter_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b3941292d71c2767af12a6b184a40c6b21ef34a70d4de70ccd6adaf651e8496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vcenterNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremVmwareClusterNetworkConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc69c247c1b3a7393145008ef18c25bfc0a9f805056e76c8015b6b23d061f01f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterNetworkConfigStaticIpConfig",
    jsii_struct_bases=[],
    name_mapping={"ip_blocks": "ipBlocks"},
)
class GkeonpremVmwareClusterNetworkConfigStaticIpConfig:
    def __init__(
        self,
        *,
        ip_blocks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param ip_blocks: ip_blocks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ip_blocks GkeonpremVmwareCluster#ip_blocks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13dfff66cbd877cb5cf01cae26306b5ed6a26bf58fcc8d4a2b471191b1b031de)
            check_type(argname="argument ip_blocks", value=ip_blocks, expected_type=type_hints["ip_blocks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip_blocks": ip_blocks,
        }

    @builtins.property
    def ip_blocks(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks"]]:
        '''ip_blocks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ip_blocks GkeonpremVmwareCluster#ip_blocks}
        '''
        result = self._values.get("ip_blocks")
        assert result is not None, "Required property 'ip_blocks' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterNetworkConfigStaticIpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks",
    jsii_struct_bases=[],
    name_mapping={"gateway": "gateway", "ips": "ips", "netmask": "netmask"},
)
class GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks:
    def __init__(
        self,
        *,
        gateway: builtins.str,
        ips: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps", typing.Dict[builtins.str, typing.Any]]]],
        netmask: builtins.str,
    ) -> None:
        '''
        :param gateway: The network gateway used by the VMware User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#gateway GkeonpremVmwareCluster#gateway}
        :param ips: ips block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ips GkeonpremVmwareCluster#ips}
        :param netmask: The netmask used by the VMware User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#netmask GkeonpremVmwareCluster#netmask}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c1782d3b007d3d434ddab5508b4594c47ef8841b44fa8310a2e9f18b4cd8532)
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
        '''The network gateway used by the VMware User Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#gateway GkeonpremVmwareCluster#gateway}
        '''
        result = self._values.get("gateway")
        assert result is not None, "Required property 'gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ips(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps"]]:
        '''ips block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ips GkeonpremVmwareCluster#ips}
        '''
        result = self._values.get("ips")
        assert result is not None, "Required property 'ips' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps"]], result)

    @builtins.property
    def netmask(self) -> builtins.str:
        '''The netmask used by the VMware User Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#netmask GkeonpremVmwareCluster#netmask}
        '''
        result = self._values.get("netmask")
        assert result is not None, "Required property 'netmask' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps",
    jsii_struct_bases=[],
    name_mapping={"ip": "ip", "hostname": "hostname"},
)
class GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps:
    def __init__(
        self,
        *,
        ip: builtins.str,
        hostname: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip: IP could be an IP address (like 1.2.3.4) or a CIDR (like 1.2.3.0/24). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ip GkeonpremVmwareCluster#ip}
        :param hostname: Hostname of the machine. VM's name will be used if this field is empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#hostname GkeonpremVmwareCluster#hostname}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__393ff9c6e713776ca3f604c34ef7f6d630378a7e95a7ade271d9cc6d1bb17036)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ip GkeonpremVmwareCluster#ip}
        '''
        result = self._values.get("ip")
        assert result is not None, "Required property 'ip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''Hostname of the machine. VM's name will be used if this field is empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#hostname GkeonpremVmwareCluster#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIpsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIpsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__075d04f717945332f1bf023dba2c4de2e551db6306faacf2957c01074e68ae6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIpsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__299713b949f7ad2dfbfb5511eb97360743376e61b8f1f2c1798181a56a4523de)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIpsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__258972f82e086775bcbc6f0f4adabe1ebba3daf20c83b60a329c08569e9458d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__732a95836a17b1e93265fcea640600a44fc524981dcb09c9414ce68ca5a2fce7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68d0f6675aa26f8d784f56c2b7047384a38a188d1b68d6de6ffdb8973eac9646)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac7ecca0e7845762704bf2a7ff024b6f09006cab94d498339412af79c07c2c0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIpsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIpsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f82c1bbdaab1652de873a44cefa0489faef35c13610dec42320c9ca1f7c7f47)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3508e77f88c6414ec9e00a65ba9ef76347f084189ce3a020273ab03a567564da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0993160b707c2f28942d739b043053d4f471a6f14b810d070c5fc12cc0f1d2fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bfd8b89bf1c4d8f8dcff9c52586eb7e3121e54d3361e76dc1b6f85027737b74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e807a5e81122d31d6e532d8a8408bcb1d3ad1fca74e3b910ce78ecdde60c1fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5622506436b98850996b8b384e0f554f46c09160993eca1a3428b1e6a04e654d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6cf1e7960bcf9cc86b81dcc0506426ca82e12ff6f31611bb6e6c0eadf7f3a14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cbb8d2543f9375f5a009c0a194a11f6ddad9299b30407f8026e06ab7de28c1d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05027d6a859d8de6769173c83a21d12deb834a98dd9aece47973e0cd1b2dc974)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b01abd1f2bf7f85e5aa858c83b8c53989b790240c09ab9264fcc2a16b1254499)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0af4095da12a09419a41c32011e616c79339b06c6e9f1372cf1ffabd245d77f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIps")
    def put_ips(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98a295aa17f2fcfddb02b09925936f7474748875a48318a0b11fd934fa3a6876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIps", [value]))

    @builtins.property
    @jsii.member(jsii_name="ips")
    def ips(self) -> GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIpsList:
        return typing.cast(GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIpsList, jsii.get(self, "ips"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="ipsInput")
    def ips_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps]]], jsii.get(self, "ipsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__da68a361a5e9318b5ffd8e853ba98730e53c5b36bb79427dca84773d4ddfdcba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateway", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netmask")
    def netmask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netmask"))

    @netmask.setter
    def netmask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e1998f7b14120cbf210d64159863c01f7824bbfc442ffdc0301256df3823cb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netmask", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14305c104d1f1681f5ed3f6e10c7cf7bbf4a1defaa7ca6c84bd9c0f1f3a7bbbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareClusterNetworkConfigStaticIpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterNetworkConfigStaticIpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa00da49aa275675c99476d1e07bf11a479ec0cc0b3da46e754436e92830882e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIpBlocks")
    def put_ip_blocks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16ab4eaa2a915ad5c060f0bf157fbc2404fd6821aa63d0ec88b620c2996bfff2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpBlocks", [value]))

    @builtins.property
    @jsii.member(jsii_name="ipBlocks")
    def ip_blocks(
        self,
    ) -> GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksList:
        return typing.cast(GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksList, jsii.get(self, "ipBlocks"))

    @builtins.property
    @jsii.member(jsii_name="ipBlocksInput")
    def ip_blocks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks]]], jsii.get(self, "ipBlocksInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterNetworkConfigStaticIpConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterNetworkConfigStaticIpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterNetworkConfigStaticIpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d554eda421ca64ca7d87806302572cec0cacd4d027c090c38fc85c4b3ecfda17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremVmwareClusterStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterStatusConditions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremVmwareClusterStatusConditions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterStatusConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareClusterStatusConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterStatusConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dca2349a63104402bb9230529f5572d41e1b008de2e3d12480811cee4f8d8e24)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareClusterStatusConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32803680537ca1a95ac3b4d0fa565f6569602aa5f2c0d67cc88e010af6aafc57)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareClusterStatusConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a624fa0e213d78fa74554e31736e14671e973b0dfa79e5b1b5a61f46067f6f9a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cf9b710f7bae1946e5e9b6efd68a3b5740bebcd4834b2e5342f389000d77cdb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__496843dbd732e955d84caa7701bb3e2df79997d582ee23076a9aa1394a25aad1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareClusterStatusConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterStatusConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d77a162f175b43ea9539175566a0d0104fd8145f9938658cc0d8fd52b4572a5)
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
    def internal_value(self) -> typing.Optional[GkeonpremVmwareClusterStatusConditions]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterStatusConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterStatusConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63f8ce6ad1bdb3d040a926a4cd0310590179ccb30f3180c7d6e616944871bd1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareClusterStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68c5c64ac28269e5f68bf6c967ed9c1df9c9cf65ce4bbdfe6607b569fb34b1b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GkeonpremVmwareClusterStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a482b6d777e5ec469e50e6b3efcc217b729929305c97f37b83ac6c3f16d932ae)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareClusterStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e07bc13142fc8cb55f4fc94caf2bba5f4ef41e42dd28654feab6ee24cf8575f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ebf8a6a1970b50e798885d5899143527d5d097b80d43a05d4191ef6649da9ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52bf5ad19072ede6bb3f284916302e7955d93d2530fbb35f9430346735a0feea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareClusterStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40803ff6da171f93f9a33625234d76717b5a28c3da3b11fbee3ece1cbfc66208)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> GkeonpremVmwareClusterStatusConditionsList:
        return typing.cast(GkeonpremVmwareClusterStatusConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremVmwareClusterStatus]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__089240e813a11f8fa03fd4464a635e5f2b056c0dcf58903bc165cd6fbe009114)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterStorage",
    jsii_struct_bases=[],
    name_mapping={"vsphere_csi_disabled": "vsphereCsiDisabled"},
)
class GkeonpremVmwareClusterStorage:
    def __init__(
        self,
        *,
        vsphere_csi_disabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param vsphere_csi_disabled: Whether or not to deploy vSphere CSI components in the VMware User Cluster. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#vsphere_csi_disabled GkeonpremVmwareCluster#vsphere_csi_disabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d0813ee16a873332041dcd063be24ca59d5fbc74237736f846f6d8f8066d4f5)
            check_type(argname="argument vsphere_csi_disabled", value=vsphere_csi_disabled, expected_type=type_hints["vsphere_csi_disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vsphere_csi_disabled": vsphere_csi_disabled,
        }

    @builtins.property
    def vsphere_csi_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether or not to deploy vSphere CSI components in the VMware User Cluster. Enabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#vsphere_csi_disabled GkeonpremVmwareCluster#vsphere_csi_disabled}
        '''
        result = self._values.get("vsphere_csi_disabled")
        assert result is not None, "Required property 'vsphere_csi_disabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareClusterStorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterStorageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8da50dbf8cb5ecf06f5c727bc6ebbb0d8da64cead0444278eac751aec8c8742)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="vsphereCsiDisabledInput")
    def vsphere_csi_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "vsphereCsiDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="vsphereCsiDisabled")
    def vsphere_csi_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "vsphereCsiDisabled"))

    @vsphere_csi_disabled.setter
    def vsphere_csi_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71dad2e4124cd3cf564e889428e7b1924ce398bcde428c981b88822d262d49d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vsphereCsiDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremVmwareClusterStorage]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterStorage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterStorage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad7aed00d095e690cd1e6e72c73fd8d24c1783a222fe00808922ccd41ed43e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GkeonpremVmwareClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#create GkeonpremVmwareCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#delete GkeonpremVmwareCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#update GkeonpremVmwareCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8222415770b39aa3a346e9f297c16aa4bcd9907e04bb43bb9e32ef13b9b9ed7)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#create GkeonpremVmwareCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#delete GkeonpremVmwareCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#update GkeonpremVmwareCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c99b67ed4511093ecd1ea1e19181548ad28bead09d42b260343df6779f16958e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__805fb96e7f73fe03e611e590f26adf9745f9f9cc5b1f1e6711af8bc354ebfd4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__280723a4c9a5b080039dfe79df477663e402874faec8bbac04265bc4897a386f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2649f20ab2cde4aa50adc5becdbc6e48f079ad3050c20c39b145c6aaffef6a30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__737ebe4dea2b89ad77d74a11f6d9c4dd2dc2befb22a61f1ded2e8c15afa2eeb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterUpgradePolicy",
    jsii_struct_bases=[],
    name_mapping={"control_plane_only": "controlPlaneOnly"},
)
class GkeonpremVmwareClusterUpgradePolicy:
    def __init__(
        self,
        *,
        control_plane_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param control_plane_only: Controls whether the upgrade applies to the control plane only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#control_plane_only GkeonpremVmwareCluster#control_plane_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc6f0f9d8d8c6da6e5e460f9369ec0fec364e8b1e7788aadcb653ba1816f3c28)
            check_type(argname="argument control_plane_only", value=control_plane_only, expected_type=type_hints["control_plane_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if control_plane_only is not None:
            self._values["control_plane_only"] = control_plane_only

    @builtins.property
    def control_plane_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Controls whether the upgrade applies to the control plane only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#control_plane_only GkeonpremVmwareCluster#control_plane_only}
        '''
        result = self._values.get("control_plane_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterUpgradePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareClusterUpgradePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterUpgradePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69400472ecdcd7c74e92c363fbe7c4f0120f35e2461f961fa723aff5f20fa542)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetControlPlaneOnly")
    def reset_control_plane_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControlPlaneOnly", []))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneOnlyInput")
    def control_plane_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "controlPlaneOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneOnly")
    def control_plane_only(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "controlPlaneOnly"))

    @control_plane_only.setter
    def control_plane_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3782b0a22c56d35d364db9e97f309e001bf0321401b97f68e55f06811ba19c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremVmwareClusterUpgradePolicy]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterUpgradePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterUpgradePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d132d3dd276983f12aec3fbb0c956907643aabff6fec8e219d6f0cf585c13453)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterValidationCheck",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremVmwareClusterValidationCheck:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterValidationCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareClusterValidationCheckList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterValidationCheckList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a5027470d96df6aefae799a907dccc59523beed9166b0cc30776147fc74b835)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareClusterValidationCheckOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04071e9a71580221e56f37b5c4b921a791b1c8493b4c3abda8bc191b5e57eacf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareClusterValidationCheckOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db33e716ceb0eb9e2db4c19866325f537db372df70ff7b9a953de5ab87e8d5b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d238351da642459767ac0d7120b010a8c3c53b596e5d99f456d484b47a29ae1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d76619cc2afb43cc2a51a5a3180c34b6c97e38055c878a0dfd1a96a241d0e5fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareClusterValidationCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterValidationCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a81e8d79b9eb35a9e0bac9b762960b46ad455cc6ed877ba17eb3c67ad594b5d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "options"))

    @builtins.property
    @jsii.member(jsii_name="scenario")
    def scenario(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scenario"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "GkeonpremVmwareClusterValidationCheckStatusList":
        return typing.cast("GkeonpremVmwareClusterValidationCheckStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremVmwareClusterValidationCheck]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterValidationCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterValidationCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11d01d91fcbddb1cc56e0d03c20fe4d7a72ec967aff27828b9d4afd45b68a3f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterValidationCheckStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremVmwareClusterValidationCheckStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterValidationCheckStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareClusterValidationCheckStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterValidationCheckStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__536be311f675dda0551ffb8e071a0b09168b8aa207fe934eeb9c207165928c68)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareClusterValidationCheckStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da557063eaf4f879fe9bc6e01563a273738c7df615b3c02d155ff688e4d94424)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareClusterValidationCheckStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e998539dbb88cc9cd45e08422c247aab529023b7e7ff93100b4879a6cb957ceb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f01ee5a43628b6c9c00bfb8bc6d883fecfb9477bf3bf647104149ac7a391d22a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe6714040ebcd30aa57cdf65f2eaeca8923d2fecc7abd606529c6553715a528c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareClusterValidationCheckStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterValidationCheckStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fff3df2eaf32cff1195ffb1038c67d53b66889c0266326dc0e396a511c44780)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="result")
    def result(self) -> "GkeonpremVmwareClusterValidationCheckStatusResultList":
        return typing.cast("GkeonpremVmwareClusterValidationCheckStatusResultList", jsii.get(self, "result"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterValidationCheckStatus]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterValidationCheckStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterValidationCheckStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b46efdb11830abebd07b2342cbd480d9c8fe96dbf8bfc747e79f89daaee4a0dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterValidationCheckStatusResult",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremVmwareClusterValidationCheckStatusResult:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterValidationCheckStatusResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareClusterValidationCheckStatusResultList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterValidationCheckStatusResultList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bef091eef61e3487fc051a6ecf5b970fcb5eac5f5daea3f4d8216b02f84b917)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareClusterValidationCheckStatusResultOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f88d328c038c3cb2ec75f6e118d339cc89cee9f88b2f62c76ad2477e1a54e791)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareClusterValidationCheckStatusResultOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33f6c6d747aba27a6ab9fe5f5e541bfc18ee6e76fea66d5f6af7629055f4d3b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6e79a05e243ba4cdc1bf8cef8e2d2a5d0df87318b751f179fbd9986e41a7b15)
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
            type_hints = typing.get_type_hints(_typecheckingstub__480119ff685b10d70364aa66e76a553b3d6f1ccdcbe19192ee1e8c1f23271fe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareClusterValidationCheckStatusResultOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterValidationCheckStatusResultOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be503e4f1cd42706def5fd6f3c6060f7af73d1545c17b1f67c94c67774f9d7d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="category")
    def category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "category"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="details")
    def details(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "options"))

    @builtins.property
    @jsii.member(jsii_name="reason")
    def reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reason"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareClusterValidationCheckStatusResult]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterValidationCheckStatusResult], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterValidationCheckStatusResult],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a31a82cad979bdcde9e0e7a75bfabb527a17cd0a5e7626663429ac9f57876df0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterVcenter",
    jsii_struct_bases=[],
    name_mapping={
        "ca_cert_data": "caCertData",
        "cluster": "cluster",
        "datacenter": "datacenter",
        "datastore": "datastore",
        "folder": "folder",
        "resource_pool": "resourcePool",
        "storage_policy_name": "storagePolicyName",
    },
)
class GkeonpremVmwareClusterVcenter:
    def __init__(
        self,
        *,
        ca_cert_data: typing.Optional[builtins.str] = None,
        cluster: typing.Optional[builtins.str] = None,
        datacenter: typing.Optional[builtins.str] = None,
        datastore: typing.Optional[builtins.str] = None,
        folder: typing.Optional[builtins.str] = None,
        resource_pool: typing.Optional[builtins.str] = None,
        storage_policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ca_cert_data: Contains the vCenter CA certificate public key for SSL verification. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ca_cert_data GkeonpremVmwareCluster#ca_cert_data}
        :param cluster: The name of the vCenter cluster for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#cluster GkeonpremVmwareCluster#cluster}
        :param datacenter: The name of the vCenter datacenter for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#datacenter GkeonpremVmwareCluster#datacenter}
        :param datastore: The name of the vCenter datastore for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#datastore GkeonpremVmwareCluster#datastore}
        :param folder: The name of the vCenter folder for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#folder GkeonpremVmwareCluster#folder}
        :param resource_pool: The name of the vCenter resource pool for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#resource_pool GkeonpremVmwareCluster#resource_pool}
        :param storage_policy_name: The name of the vCenter storage policy for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#storage_policy_name GkeonpremVmwareCluster#storage_policy_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8b7d41001800c6f17160ba5e0ce46933f2061186e9655096bde531ae508cbc2)
            check_type(argname="argument ca_cert_data", value=ca_cert_data, expected_type=type_hints["ca_cert_data"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument datacenter", value=datacenter, expected_type=type_hints["datacenter"])
            check_type(argname="argument datastore", value=datastore, expected_type=type_hints["datastore"])
            check_type(argname="argument folder", value=folder, expected_type=type_hints["folder"])
            check_type(argname="argument resource_pool", value=resource_pool, expected_type=type_hints["resource_pool"])
            check_type(argname="argument storage_policy_name", value=storage_policy_name, expected_type=type_hints["storage_policy_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ca_cert_data is not None:
            self._values["ca_cert_data"] = ca_cert_data
        if cluster is not None:
            self._values["cluster"] = cluster
        if datacenter is not None:
            self._values["datacenter"] = datacenter
        if datastore is not None:
            self._values["datastore"] = datastore
        if folder is not None:
            self._values["folder"] = folder
        if resource_pool is not None:
            self._values["resource_pool"] = resource_pool
        if storage_policy_name is not None:
            self._values["storage_policy_name"] = storage_policy_name

    @builtins.property
    def ca_cert_data(self) -> typing.Optional[builtins.str]:
        '''Contains the vCenter CA certificate public key for SSL verification.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#ca_cert_data GkeonpremVmwareCluster#ca_cert_data}
        '''
        result = self._values.get("ca_cert_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter cluster for the user cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#cluster GkeonpremVmwareCluster#cluster}
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datacenter(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter datacenter for the user cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#datacenter GkeonpremVmwareCluster#datacenter}
        '''
        result = self._values.get("datacenter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datastore(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter datastore for the user cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#datastore GkeonpremVmwareCluster#datastore}
        '''
        result = self._values.get("datastore")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def folder(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter folder for the user cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#folder GkeonpremVmwareCluster#folder}
        '''
        result = self._values.get("folder")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_pool(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter resource pool for the user cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#resource_pool GkeonpremVmwareCluster#resource_pool}
        '''
        result = self._values.get("resource_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_policy_name(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter storage policy for the user cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_cluster#storage_policy_name GkeonpremVmwareCluster#storage_policy_name}
        '''
        result = self._values.get("storage_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareClusterVcenter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareClusterVcenterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareCluster.GkeonpremVmwareClusterVcenterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7446e10bedade96c46a076cfdc2df25c8eae5f3131e1d45f61d61c60a18a7b0c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCaCertData")
    def reset_ca_cert_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaCertData", []))

    @jsii.member(jsii_name="resetCluster")
    def reset_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCluster", []))

    @jsii.member(jsii_name="resetDatacenter")
    def reset_datacenter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatacenter", []))

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
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

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
    @jsii.member(jsii_name="caCertData")
    def ca_cert_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caCertData"))

    @ca_cert_data.setter
    def ca_cert_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fb9595d46631226da2c155967b2947d8d05a98333cb78fc671236cab49e930b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caCertData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__436b44277b6aae25c793efac794bebcfe4d3cbf6214328a651e54f5a302b0280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="datacenter")
    def datacenter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datacenter"))

    @datacenter.setter
    def datacenter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8795a2c9f85efc21d54103808ce2b0b76675577a5b5c61a7d521122611355477)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datacenter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="datastore")
    def datastore(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datastore"))

    @datastore.setter
    def datastore(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc6c5aa62577d0d12c0fa0d7150b2a205bbae5062d57cdac013dbf7a26108ad5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datastore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="folder")
    def folder(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "folder"))

    @folder.setter
    def folder(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e2daf9a21f803f492ae6259709069d768f122c594e36136139865c9b2e5808f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "folder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourcePool")
    def resource_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourcePool"))

    @resource_pool.setter
    def resource_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__333de41f14602389cffdcd2683dc0b21b5715f3986a3c7b1f77babe3c2017081)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storagePolicyName")
    def storage_policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storagePolicyName"))

    @storage_policy_name.setter
    def storage_policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c9455839712a3d9140c729fe930541b1830915928b161ca773bf88121751d66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storagePolicyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremVmwareClusterVcenter]:
        return typing.cast(typing.Optional[GkeonpremVmwareClusterVcenter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareClusterVcenter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53e22ef901d519c833b16ca2d594556c47cf20900516bbbb6cb97ff4d037c00c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GkeonpremVmwareCluster",
    "GkeonpremVmwareClusterAntiAffinityGroups",
    "GkeonpremVmwareClusterAntiAffinityGroupsOutputReference",
    "GkeonpremVmwareClusterAuthorization",
    "GkeonpremVmwareClusterAuthorizationAdminUsers",
    "GkeonpremVmwareClusterAuthorizationAdminUsersList",
    "GkeonpremVmwareClusterAuthorizationAdminUsersOutputReference",
    "GkeonpremVmwareClusterAuthorizationOutputReference",
    "GkeonpremVmwareClusterAutoRepairConfig",
    "GkeonpremVmwareClusterAutoRepairConfigOutputReference",
    "GkeonpremVmwareClusterConfig",
    "GkeonpremVmwareClusterControlPlaneNode",
    "GkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig",
    "GkeonpremVmwareClusterControlPlaneNodeAutoResizeConfigOutputReference",
    "GkeonpremVmwareClusterControlPlaneNodeOutputReference",
    "GkeonpremVmwareClusterControlPlaneNodeVsphereConfig",
    "GkeonpremVmwareClusterControlPlaneNodeVsphereConfigList",
    "GkeonpremVmwareClusterControlPlaneNodeVsphereConfigOutputReference",
    "GkeonpremVmwareClusterDataplaneV2",
    "GkeonpremVmwareClusterDataplaneV2OutputReference",
    "GkeonpremVmwareClusterFleet",
    "GkeonpremVmwareClusterFleetList",
    "GkeonpremVmwareClusterFleetOutputReference",
    "GkeonpremVmwareClusterLoadBalancer",
    "GkeonpremVmwareClusterLoadBalancerF5Config",
    "GkeonpremVmwareClusterLoadBalancerF5ConfigOutputReference",
    "GkeonpremVmwareClusterLoadBalancerManualLbConfig",
    "GkeonpremVmwareClusterLoadBalancerManualLbConfigOutputReference",
    "GkeonpremVmwareClusterLoadBalancerMetalLbConfig",
    "GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools",
    "GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPoolsList",
    "GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPoolsOutputReference",
    "GkeonpremVmwareClusterLoadBalancerMetalLbConfigOutputReference",
    "GkeonpremVmwareClusterLoadBalancerOutputReference",
    "GkeonpremVmwareClusterLoadBalancerVipConfig",
    "GkeonpremVmwareClusterLoadBalancerVipConfigOutputReference",
    "GkeonpremVmwareClusterNetworkConfig",
    "GkeonpremVmwareClusterNetworkConfigControlPlaneV2Config",
    "GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock",
    "GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps",
    "GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIpsList",
    "GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIpsOutputReference",
    "GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockOutputReference",
    "GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigOutputReference",
    "GkeonpremVmwareClusterNetworkConfigDhcpIpConfig",
    "GkeonpremVmwareClusterNetworkConfigDhcpIpConfigOutputReference",
    "GkeonpremVmwareClusterNetworkConfigHostConfig",
    "GkeonpremVmwareClusterNetworkConfigHostConfigOutputReference",
    "GkeonpremVmwareClusterNetworkConfigOutputReference",
    "GkeonpremVmwareClusterNetworkConfigStaticIpConfig",
    "GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks",
    "GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps",
    "GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIpsList",
    "GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIpsOutputReference",
    "GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksList",
    "GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksOutputReference",
    "GkeonpremVmwareClusterNetworkConfigStaticIpConfigOutputReference",
    "GkeonpremVmwareClusterStatus",
    "GkeonpremVmwareClusterStatusConditions",
    "GkeonpremVmwareClusterStatusConditionsList",
    "GkeonpremVmwareClusterStatusConditionsOutputReference",
    "GkeonpremVmwareClusterStatusList",
    "GkeonpremVmwareClusterStatusOutputReference",
    "GkeonpremVmwareClusterStorage",
    "GkeonpremVmwareClusterStorageOutputReference",
    "GkeonpremVmwareClusterTimeouts",
    "GkeonpremVmwareClusterTimeoutsOutputReference",
    "GkeonpremVmwareClusterUpgradePolicy",
    "GkeonpremVmwareClusterUpgradePolicyOutputReference",
    "GkeonpremVmwareClusterValidationCheck",
    "GkeonpremVmwareClusterValidationCheckList",
    "GkeonpremVmwareClusterValidationCheckOutputReference",
    "GkeonpremVmwareClusterValidationCheckStatus",
    "GkeonpremVmwareClusterValidationCheckStatusList",
    "GkeonpremVmwareClusterValidationCheckStatusOutputReference",
    "GkeonpremVmwareClusterValidationCheckStatusResult",
    "GkeonpremVmwareClusterValidationCheckStatusResultList",
    "GkeonpremVmwareClusterValidationCheckStatusResultOutputReference",
    "GkeonpremVmwareClusterVcenter",
    "GkeonpremVmwareClusterVcenterOutputReference",
]

publication.publish()

def _typecheckingstub__0ef6463a8c37cc2f184f5cb04f538d7eefb06762ed5e14a6daf41fa40094a477(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    admin_cluster_membership: builtins.str,
    control_plane_node: typing.Union[GkeonpremVmwareClusterControlPlaneNode, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    on_prem_version: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    anti_affinity_groups: typing.Optional[typing.Union[GkeonpremVmwareClusterAntiAffinityGroups, typing.Dict[builtins.str, typing.Any]]] = None,
    authorization: typing.Optional[typing.Union[GkeonpremVmwareClusterAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_repair_config: typing.Optional[typing.Union[GkeonpremVmwareClusterAutoRepairConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    dataplane_v2: typing.Optional[typing.Union[GkeonpremVmwareClusterDataplaneV2, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disable_bundled_ingress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_advanced_cluster: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_control_plane_v2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    load_balancer: typing.Optional[typing.Union[GkeonpremVmwareClusterLoadBalancer, typing.Dict[builtins.str, typing.Any]]] = None,
    network_config: typing.Optional[typing.Union[GkeonpremVmwareClusterNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    storage: typing.Optional[typing.Union[GkeonpremVmwareClusterStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GkeonpremVmwareClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    upgrade_policy: typing.Optional[typing.Union[GkeonpremVmwareClusterUpgradePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    vcenter: typing.Optional[typing.Union[GkeonpremVmwareClusterVcenter, typing.Dict[builtins.str, typing.Any]]] = None,
    vm_tracking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__742d477fb07691bcc26204eabdf5d7d78c1a222ceab730c7d88de3818864ec78(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4b16f62da0c1dcb56b1473cd04eba4e9fd965e66622d5547dea5f4b8d6b059e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3a73015150580f4e45171f779d45074dd86f531f10dc985d8efa8e3129831c2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48a4833b8e103870bfce3e5a8b98d412002003951e66efa8219f91c0b828e1f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__314b0ea6e3b02a35adb3a817823c3efb4fea615aff4a8118df8a5ac607ab02cd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79909f4d6b63f5ecf010daa6802d15b1edbff944b16a9d69319e4a221482dede(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c35a61da5f1e5789ceeb4d4c7be0c28b07e082266b6a133d008e259c85f81b5e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b8f26e8791e29bcfb844a668934fbffeec7e2ae0d865da701978be2f6d4b12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d40e920824d947a1c9406e414d5c9dad651cf97af1a3536bc70d79fd100a7a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa39d6d369c1a785a2ce510e86d9b9279e0b9b08fa4bcbe0150c49f8bfc7de7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ea005d43c0f1e8640862f73d40ec2a07b9458b74a637c9eb296e4c7d9664ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__066fa11fb7a3aa2285d80b3610389b0cea1b7f9e3c538c37566ca7a107cfadb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a4ae147475d07cd3c1f813faa0d1457c6eb352d2334ae0289f9f6f1186ec14c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5e4a8ce20cdd5a6081ed2451a1ef2e02aa39a42d101ad080764edf8da81352e(
    *,
    aag_config_disabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d15d82645ea977862af85a8708c2a30392585ab29643b24ce82067e00562656(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7c59b3d1af760b0edeca1360aea02a2ccf55878093560c271e8c705eb5d9ce2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1d86ea6be10048405b6fb001f91335768923d765b7c215685c960fa00de966f(
    value: typing.Optional[GkeonpremVmwareClusterAntiAffinityGroups],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24f654d203be9c8a3e90b5e4ed086390cbc4f6315fc2b10011e1c0e6cd756a4c(
    *,
    admin_users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareClusterAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e436656bb36ba3ee75cedb596281a84383bc05f944b1afb2f2fcb7747153100d(
    *,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada0bc2c314b529626c7af8bb2a4051c2054fc76b909896fa6726cd149976aa4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836c5a6db9b9075c250512f18bc1466ab831e95e99699ec405c3b8556fdba8ec(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e7f248a8ae83ba636d2b79cd664e6d512a0620c851bd5f1b3f76ab1422e2ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7595cfba3b331582d0a65278853a5589d32f0e3962d680498075e14c72da8b3c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89048136af455fa7a473cd4a2eef05f6abfaa385058c4572de4d01ca23fb78da(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a6848c9511b8a7b5912f1378146411630bbd1c79e2defb043417a2f674c10ec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterAuthorizationAdminUsers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b953cf495a97eb461a5feae1ec098f766069c843d8b2121119fd098e680cd130(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3987dd5bd4a9bcfa7abda961ac1a512e37ae8e62c40fd905e1c8cb48fb80ecc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd893b4db3ae224501bff0a0644ab79044277d1d1c8bd8e01dab8cf5a95a9ee3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterAuthorizationAdminUsers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26879e9b014f240c3caccc35b4c7bbeaee2de4c7cdeca8e14b8050fdb49e1f80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0608957c3de730dc71e3b0d1cdc00887cf11a1acdf87239c19f984535d19776f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareClusterAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__640b8aea39c6ae57f220070bf6df20594b2abc4a3dab4aea56df3a79723b9944(
    value: typing.Optional[GkeonpremVmwareClusterAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d59bf195303fe8d7e3b4aca3b7ed32f23e023238a6aeb9b89251b3df1518dfc0(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2549f6091af3da4cbae17c09418271f32f06d586153eae73141189023fcd845(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e96025a729792b3ef4150c42f03eb45a6de66ee365697444194b8dde32a8e781(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80de3c7e05944f8ea9d64343869d355dfb82fda54d2d87ec75bca0d8fad0725d(
    value: typing.Optional[GkeonpremVmwareClusterAutoRepairConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf267676316e0f706fe6220fede15de8e6f45aa45c9065dc06b3d6738765c292(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    admin_cluster_membership: builtins.str,
    control_plane_node: typing.Union[GkeonpremVmwareClusterControlPlaneNode, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    on_prem_version: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    anti_affinity_groups: typing.Optional[typing.Union[GkeonpremVmwareClusterAntiAffinityGroups, typing.Dict[builtins.str, typing.Any]]] = None,
    authorization: typing.Optional[typing.Union[GkeonpremVmwareClusterAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_repair_config: typing.Optional[typing.Union[GkeonpremVmwareClusterAutoRepairConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    dataplane_v2: typing.Optional[typing.Union[GkeonpremVmwareClusterDataplaneV2, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disable_bundled_ingress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_advanced_cluster: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_control_plane_v2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    load_balancer: typing.Optional[typing.Union[GkeonpremVmwareClusterLoadBalancer, typing.Dict[builtins.str, typing.Any]]] = None,
    network_config: typing.Optional[typing.Union[GkeonpremVmwareClusterNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    storage: typing.Optional[typing.Union[GkeonpremVmwareClusterStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GkeonpremVmwareClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    upgrade_policy: typing.Optional[typing.Union[GkeonpremVmwareClusterUpgradePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    vcenter: typing.Optional[typing.Union[GkeonpremVmwareClusterVcenter, typing.Dict[builtins.str, typing.Any]]] = None,
    vm_tracking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__036836c01487abb5860a1f6192cab8b31ba6eb68096417ed9c0d4a0d829f1cb6(
    *,
    auto_resize_config: typing.Optional[typing.Union[GkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    cpus: typing.Optional[jsii.Number] = None,
    memory: typing.Optional[jsii.Number] = None,
    replicas: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b781cfa3e8d7a607e116a1a31757f80a0719d76040dfdf0656f5f55117e36ae3(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5c0ac6c73cacac4159898c92d21b9002de4565f729b18d56c14c987be8656bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a8293668adef521586ebe99979134f8e41c9108c6d6cf316e6d66bcb5d72ee(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8c891422d6d327804ca33f3e8b8fe2b31189d0c24f658563709ff8914d9c97f(
    value: typing.Optional[GkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe6fc760b88f2813d7d75c44fb152cc7f13a7a6785fada72e5d9c662048d70b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c9582ed13c16547ad44d29b013b19df585ee23bbd564c45fd1d1e67277ef688(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26980b36b8a6b9515a175cd2163246ca33843f5f5f7af7bb11193f5e6a716f66(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b16c08a076136a5cb8f24d4f08f33faa4f2715753b0d9c0ff34e7a2683e6f5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd2777cd6aa12360c765f4164873ea4afc446a99c361d917960426249e9cd84(
    value: typing.Optional[GkeonpremVmwareClusterControlPlaneNode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd34587fcb7821643362c2bed8ee03da91078351750129fef505b224a339be1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92f7cc80048348b97fd8b4f5e5a3637da6c9c6b1c0310c63dfec80618c38ef6e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a16e911e9ed9d7d6eacc350c27dc4312a355b3519254b2018b4669a4aa9c7972(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__942beeac3aeaf796f33a86f187f05b194cc46ce0a4f523be7e7f01bfc552442c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18ad22fda6b610938e9e2cd388a7957cca0659752bde76d74a35f540eca3a47d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8950a689375971ece06a11561db8e895b0c61f38c16c393fd2780d670774959f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80db33b753e04f229386c2d6855d30b9597dfc1dfcf7776fd9fa3f50d44ab713(
    value: typing.Optional[GkeonpremVmwareClusterControlPlaneNodeVsphereConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8033138e8ca56d041e0133e136805534a6174859fd8db68dfa1274821c1cf9a(
    *,
    advanced_networking: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dataplane_v2_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    windows_dataplane_v2_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d0c93511dd32bdde85787ee09d3e2b81ed8df9a6fda04c70d498075d0da2d6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c0d6d5131c656a06f2306e54ff0bc0d109a097bc7a08d2913c621223241b808(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5276dc651b73d75a1e3394d24d6c7e2cf9f1ad1728ef3d9ddf657780c8efc9ec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__722a21d6b919fb0a78ca16d9c046523b71eabbad5d316b22bced2b3fd58bfd2b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba6e1b2dd40e03fa45ae85a5852059ace0f0504d62811c18afee98f874370d5(
    value: typing.Optional[GkeonpremVmwareClusterDataplaneV2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f5957d858efe169af64ac8046e1446a59f1aeda8597323a7a4f8eab06558eaa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be75bae75c32be7a56cd90e1f9f69146c7741e65ba211738fa502899863dc634(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b87fda12f812b04b764aae216e12a6da58edc00cfeed4d7c0b6c0074cb68b3b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca26f9ef17b4b069157dfc013fded26af3fc4ff5e5c22edb6a84e5d777fb3eb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9313a85c37e438f0ca805ced89ada73566f71e56dbcf1d86de7ee198eba8879a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f91565c0e2aa6bc57eda3f0cf970a1a4d40a5e916d039298ec233d194c0e94e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce5c3e546400aa25b261ed7066f3e357d4e792efc71f7a0ff7c145b5df51eeb5(
    value: typing.Optional[GkeonpremVmwareClusterFleet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__385bd31358c395c69d12a8e10ca67b2863913df97887fb65fe23effa83de6177(
    *,
    f5_config: typing.Optional[typing.Union[GkeonpremVmwareClusterLoadBalancerF5Config, typing.Dict[builtins.str, typing.Any]]] = None,
    manual_lb_config: typing.Optional[typing.Union[GkeonpremVmwareClusterLoadBalancerManualLbConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    metal_lb_config: typing.Optional[typing.Union[GkeonpremVmwareClusterLoadBalancerMetalLbConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    vip_config: typing.Optional[typing.Union[GkeonpremVmwareClusterLoadBalancerVipConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45791af81c5564a5a77e6780023b4a87d96d503938a52c88fef048eb61344a78(
    *,
    address: typing.Optional[builtins.str] = None,
    partition: typing.Optional[builtins.str] = None,
    snat_pool: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b703aa54d96c18bf12f5dc800a953ccfa4efa7183589c207bf92ed11e9bac7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1176ff4ffb938cf62a391450c8712e2b28ef8f61c8e68211ec5a06a93c683351(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdc3758fb7e1fa1a8e5fc7c340a3f657e81e1c99cbad8fcffc541031540887ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d06a5af73721cb19e9344241a17570b9e0f0610e8be7ecf4ab6344eabbbeca6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71f7cc177984579f0d0cba89044170ac5655cf0c187b43d2e6740e2ff44ae02(
    value: typing.Optional[GkeonpremVmwareClusterLoadBalancerF5Config],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6426981c6a21348236a770408e39fb4fb78f4fea7cf88db212820c0b53df85a5(
    *,
    control_plane_node_port: typing.Optional[jsii.Number] = None,
    ingress_http_node_port: typing.Optional[jsii.Number] = None,
    ingress_https_node_port: typing.Optional[jsii.Number] = None,
    konnectivity_server_node_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0210af19126fe79ddcd4683d49a3a4ab0f58c134458d525b60489d1073650978(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c4bd901b1ff8bfcc3d639500bbf3bcfbc2ff8827dbd780bceee1971a64c86a0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5eb99ad36266a4d6f114888b2bf178f6bb65e3557b26a9f93ce49d6a417d4d5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b333bdf1f2345d934104590f39ca946a386a02c88036b68e81fcf97f7974cefa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a83ab14953bf8d762b4213e5e4511cf5c7bd35dd0854fa9198c270d4b4e5b5b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed28cf0bc0567dc84bb4b6a51e7905276af2b02fd7f3cf84094bdc9119f6908(
    value: typing.Optional[GkeonpremVmwareClusterLoadBalancerManualLbConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e02a92645463c74e5260591079dc41e1c76bc19806acc2a730d2ef8d26aef6(
    *,
    address_pools: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fecdc3b5a1c1f9542077fccb217694f3df796176dcce3a9e470cc9c7fa795cae(
    *,
    addresses: typing.Sequence[builtins.str],
    pool: builtins.str,
    avoid_buggy_ips: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    manual_assign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc0eca5f0140ac5e6229a3edbc7cb59dfa4b7e9f9b5c149a6e95faca5d7933e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__647307ef07b0b7824757730c6185d4c21ce6f14bb8fed679f60926d06ec42213(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d721aa775ee80708ff450cb89e487d73ad9161a07d74c50c2498d124aea60a72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d904a6e0e6a8a4e5f18eb8905ff4ba3383907f69ce3045f4c887ffb3e024877(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae33ed329faa34e8d306616edbb71bf69b1fe09f3094152db645780ab94fc246(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dd089d71e0e172e1f153665a480e0a54e3b0b3350962423cc835dd946df0c56(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaa0c4986b32a796133afebb11fef2961417422c9072a1b16e46f3d820ba7f0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af61bdd39386286381fcfd27bed345109aa6496357cecbb8eaae6a57f4f838a9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__497f87850d7c7c77997e6700e3bbe116fc080c2704ab6ae16351760c5e11fd5e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__233d46ee9f2d1521d5058e1e02ae15b57398430e210baa3cc50bada64bc5439d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56303dea90effcd1e5f4c6f0f2054979a4f518a36e133e5da77f31322079051c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68201820d2754238d5fef3f3db4e5fac791bfe20674744cd3d05c7c69d619836(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf9604237b2656dd99a4aab98f16daf513e70fdeffd7a8c3bf61194032bc6bb5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54befca2e1c3b2e2f26f4aebb9a1a19a3ec625968a2e4b20bd17f86477558c59(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d59f00f07b763bd969c9a817e6e8c9bb8d83a4a258eee6d16823ff1f59b69b6(
    value: typing.Optional[GkeonpremVmwareClusterLoadBalancerMetalLbConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44f8f98900030db4df59774569d989cab2d80acf729cbe1d9f1f2ad2c0fdb8a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24aef73aed085fcad331b15f38fb23ca9166db84c67fc3714bd36420e85fd5e1(
    value: typing.Optional[GkeonpremVmwareClusterLoadBalancer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcaa3472519161dd150a8a8153b9b54d2ed909bcbbfed01a6d5ee2ad39b45c8e(
    *,
    control_plane_vip: typing.Optional[builtins.str] = None,
    ingress_vip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b6f9d0974ad85b782590e0032cf0374f537a42e0ae0f94b451b7ea9522a97f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac5f1afccdae9bb0c9cecb235b116e920f7ce1cfdd9edf41ecc71a804a5e5898(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d731c5c082147d81d2f42f6c4fac70c37304fc78402e9740ccf8f5632debb90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__326d282d86ce0e7b0d98bd34e0c0ff14a37036e7feaa540f7e048bb31e30fcc5(
    value: typing.Optional[GkeonpremVmwareClusterLoadBalancerVipConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7ccf4b01cf2237fdab8c7ea9b6a956a37779aa5b6e7395d0989a680cbe062a(
    *,
    pod_address_cidr_blocks: typing.Sequence[builtins.str],
    service_address_cidr_blocks: typing.Sequence[builtins.str],
    control_plane_v2_config: typing.Optional[typing.Union[GkeonpremVmwareClusterNetworkConfigControlPlaneV2Config, typing.Dict[builtins.str, typing.Any]]] = None,
    dhcp_ip_config: typing.Optional[typing.Union[GkeonpremVmwareClusterNetworkConfigDhcpIpConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    host_config: typing.Optional[typing.Union[GkeonpremVmwareClusterNetworkConfigHostConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    static_ip_config: typing.Optional[typing.Union[GkeonpremVmwareClusterNetworkConfigStaticIpConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    vcenter_network: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ffec5f1627aa55b6bafb05d0a7f42a275df426ff3775b108c0d3778c8f0b24e(
    *,
    control_plane_ip_block: typing.Optional[typing.Union[GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c284ff9c2b3b9c6f2ff51bfee5152c855c7c10c64f59eabe024241298c57d98d(
    *,
    gateway: typing.Optional[builtins.str] = None,
    ips: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps, typing.Dict[builtins.str, typing.Any]]]]] = None,
    netmask: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fda6103187e645524b2d95224a8e3d1dc4dcbb30be217d79901bbc8304c3ccc8(
    *,
    hostname: typing.Optional[builtins.str] = None,
    ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77111cdbd24e4902c89a7133c5fa753ea7b302949b77e41ac095b06a9c2a2913(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdfcdcad38c447388616cb1f47736fec0548957f0980184f39340b61ae6844e3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c53f2cbc9b918a78fd6a1f901e44d0204dde2d4542847dcb678683c17aca3ade(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602ad97d65e85f0b733a8a03214774e07ff6b5faafd800860b02ecbb91b97e97(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__323840574298d4261d6b2da63edb566b9f41c016511ffb2d9feb84768725fbe9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a035108e9035c0e55b93ebd24302ef0d626b035746ffdd22d46ae24b2591cc30(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38bdbe15d3baaa51964b58040420ef7526ace86ef3b6f00b3ba3ee96ec2ae375(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c818559420fb4adf727479bb519224b3e436ec73c890d3c209e808503119285(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5dca2c26e70caa51a1febb4c2470cf1bab75fa78a699c555f8c32570c591597(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d8b199d03e25dde06e0083782ea72c3c63fc8e43e413232666abf8478f349dc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbb5f16b9141d8806fbc9d5744135d7815dff45e49627b4a63b148a1068a5806(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f68c21eb1250e77702db5252cdae353f35837d178ed6652b739bb9e25820c74d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d7910d1c0ca941e832ca499649a04f93f427cee0fc7079bd84dfb0fa6e8c892(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4dcc67c538603d03095cfac7c6759e2a96af3bc525b49a8e11dd07dbfee8416(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__933703632b48ee55172417ef4cce329be34b04b8bff6a54a6649ccc902da9645(
    value: typing.Optional[GkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37dddb62e42392efb8b91e89a3bda3479c155fd0d9907d89be654520a863143f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df749cd5b1c6f51852652bea2b840edffaa82c15b22047af452f5d2d56d3805d(
    value: typing.Optional[GkeonpremVmwareClusterNetworkConfigControlPlaneV2Config],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a549e144a2f4c626331a05de1587127b72995ced179e39a62eb7debfbbcd9eb(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3234cadd1f9ae4d3e0021ed933de8abd093ec17b176970d5a7c168c5a46d3654(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d1662ce7a224f4484f8c9b4c758c6a5ef3873fdf3a0729780b3dcd9b82c061b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bf3d424b26cb5b8071d488581f6f2d16c966da74503a20c0d5dfdd47a160b52(
    value: typing.Optional[GkeonpremVmwareClusterNetworkConfigDhcpIpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dedaa27b8a60ffaffc015054587c49c688f02dbca9b6f0d64fb6e8c77b0d3f91(
    *,
    dns_search_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ntp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e209f17895fea9cc05e3c2d6f3cfe6ac3371eadedac178b4a6da3beba402d51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d880d7bca53f4468913bec19a8c909f7374013e496068808d68ad3cd67e096c2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66cda2416e8ce03beef83545e11f214364701a1daa11d6a971b821c9ee9c989a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce3c2130f5ba4be7f0b1626c1f2996acc6fde45decc3ffedc641df1d9257010(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67b51ed84d88d8ac9a1768ee7a1694ee5df7b3e468fd5e6518869fbe12dc430b(
    value: typing.Optional[GkeonpremVmwareClusterNetworkConfigHostConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31b3328b995375f6b80b4ad27da3475966bd46e633d4ee097fb0a513b0c0080e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa17e258516fb912da5e5356986d5da45a6447ce5a9f77f6865c0470c6b75975(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a756163df81164816c6eafacdea6404ce21a02e5b6f9297c8c0332cabbe8be3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b3941292d71c2767af12a6b184a40c6b21ef34a70d4de70ccd6adaf651e8496(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc69c247c1b3a7393145008ef18c25bfc0a9f805056e76c8015b6b23d061f01f(
    value: typing.Optional[GkeonpremVmwareClusterNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13dfff66cbd877cb5cf01cae26306b5ed6a26bf58fcc8d4a2b471191b1b031de(
    *,
    ip_blocks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c1782d3b007d3d434ddab5508b4594c47ef8841b44fa8310a2e9f18b4cd8532(
    *,
    gateway: builtins.str,
    ips: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps, typing.Dict[builtins.str, typing.Any]]]],
    netmask: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__393ff9c6e713776ca3f604c34ef7f6d630378a7e95a7ade271d9cc6d1bb17036(
    *,
    ip: builtins.str,
    hostname: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__075d04f717945332f1bf023dba2c4de2e551db6306faacf2957c01074e68ae6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__299713b949f7ad2dfbfb5511eb97360743376e61b8f1f2c1798181a56a4523de(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__258972f82e086775bcbc6f0f4adabe1ebba3daf20c83b60a329c08569e9458d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__732a95836a17b1e93265fcea640600a44fc524981dcb09c9414ce68ca5a2fce7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68d0f6675aa26f8d784f56c2b7047384a38a188d1b68d6de6ffdb8973eac9646(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac7ecca0e7845762704bf2a7ff024b6f09006cab94d498339412af79c07c2c0e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f82c1bbdaab1652de873a44cefa0489faef35c13610dec42320c9ca1f7c7f47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3508e77f88c6414ec9e00a65ba9ef76347f084189ce3a020273ab03a567564da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0993160b707c2f28942d739b043053d4f471a6f14b810d070c5fc12cc0f1d2fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bfd8b89bf1c4d8f8dcff9c52586eb7e3121e54d3361e76dc1b6f85027737b74(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e807a5e81122d31d6e532d8a8408bcb1d3ad1fca74e3b910ce78ecdde60c1fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5622506436b98850996b8b384e0f554f46c09160993eca1a3428b1e6a04e654d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6cf1e7960bcf9cc86b81dcc0506426ca82e12ff6f31611bb6e6c0eadf7f3a14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cbb8d2543f9375f5a009c0a194a11f6ddad9299b30407f8026e06ab7de28c1d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05027d6a859d8de6769173c83a21d12deb834a98dd9aece47973e0cd1b2dc974(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b01abd1f2bf7f85e5aa858c83b8c53989b790240c09ab9264fcc2a16b1254499(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0af4095da12a09419a41c32011e616c79339b06c6e9f1372cf1ffabd245d77f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a295aa17f2fcfddb02b09925936f7474748875a48318a0b11fd934fa3a6876(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da68a361a5e9318b5ffd8e853ba98730e53c5b36bb79427dca84773d4ddfdcba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e1998f7b14120cbf210d64159863c01f7824bbfc442ffdc0301256df3823cb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14305c104d1f1681f5ed3f6e10c7cf7bbf4a1defaa7ca6c84bd9c0f1f3a7bbbc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa00da49aa275675c99476d1e07bf11a479ec0cc0b3da46e754436e92830882e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16ab4eaa2a915ad5c060f0bf157fbc2404fd6821aa63d0ec88b620c2996bfff2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d554eda421ca64ca7d87806302572cec0cacd4d027c090c38fc85c4b3ecfda17(
    value: typing.Optional[GkeonpremVmwareClusterNetworkConfigStaticIpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca2349a63104402bb9230529f5572d41e1b008de2e3d12480811cee4f8d8e24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32803680537ca1a95ac3b4d0fa565f6569602aa5f2c0d67cc88e010af6aafc57(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a624fa0e213d78fa74554e31736e14671e973b0dfa79e5b1b5a61f46067f6f9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf9b710f7bae1946e5e9b6efd68a3b5740bebcd4834b2e5342f389000d77cdb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__496843dbd732e955d84caa7701bb3e2df79997d582ee23076a9aa1394a25aad1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d77a162f175b43ea9539175566a0d0104fd8145f9938658cc0d8fd52b4572a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63f8ce6ad1bdb3d040a926a4cd0310590179ccb30f3180c7d6e616944871bd1d(
    value: typing.Optional[GkeonpremVmwareClusterStatusConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c5c64ac28269e5f68bf6c967ed9c1df9c9cf65ce4bbdfe6607b569fb34b1b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a482b6d777e5ec469e50e6b3efcc217b729929305c97f37b83ac6c3f16d932ae(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07bc13142fc8cb55f4fc94caf2bba5f4ef41e42dd28654feab6ee24cf8575f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ebf8a6a1970b50e798885d5899143527d5d097b80d43a05d4191ef6649da9ee(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52bf5ad19072ede6bb3f284916302e7955d93d2530fbb35f9430346735a0feea(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40803ff6da171f93f9a33625234d76717b5a28c3da3b11fbee3ece1cbfc66208(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__089240e813a11f8fa03fd4464a635e5f2b056c0dcf58903bc165cd6fbe009114(
    value: typing.Optional[GkeonpremVmwareClusterStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d0813ee16a873332041dcd063be24ca59d5fbc74237736f846f6d8f8066d4f5(
    *,
    vsphere_csi_disabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8da50dbf8cb5ecf06f5c727bc6ebbb0d8da64cead0444278eac751aec8c8742(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71dad2e4124cd3cf564e889428e7b1924ce398bcde428c981b88822d262d49d0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad7aed00d095e690cd1e6e72c73fd8d24c1783a222fe00808922ccd41ed43e8(
    value: typing.Optional[GkeonpremVmwareClusterStorage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8222415770b39aa3a346e9f297c16aa4bcd9907e04bb43bb9e32ef13b9b9ed7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c99b67ed4511093ecd1ea1e19181548ad28bead09d42b260343df6779f16958e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__805fb96e7f73fe03e611e590f26adf9745f9f9cc5b1f1e6711af8bc354ebfd4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__280723a4c9a5b080039dfe79df477663e402874faec8bbac04265bc4897a386f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2649f20ab2cde4aa50adc5becdbc6e48f079ad3050c20c39b145c6aaffef6a30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__737ebe4dea2b89ad77d74a11f6d9c4dd2dc2befb22a61f1ded2e8c15afa2eeb7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc6f0f9d8d8c6da6e5e460f9369ec0fec364e8b1e7788aadcb653ba1816f3c28(
    *,
    control_plane_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69400472ecdcd7c74e92c363fbe7c4f0120f35e2461f961fa723aff5f20fa542(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3782b0a22c56d35d364db9e97f309e001bf0321401b97f68e55f06811ba19c6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d132d3dd276983f12aec3fbb0c956907643aabff6fec8e219d6f0cf585c13453(
    value: typing.Optional[GkeonpremVmwareClusterUpgradePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a5027470d96df6aefae799a907dccc59523beed9166b0cc30776147fc74b835(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04071e9a71580221e56f37b5c4b921a791b1c8493b4c3abda8bc191b5e57eacf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db33e716ceb0eb9e2db4c19866325f537db372df70ff7b9a953de5ab87e8d5b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d238351da642459767ac0d7120b010a8c3c53b596e5d99f456d484b47a29ae1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76619cc2afb43cc2a51a5a3180c34b6c97e38055c878a0dfd1a96a241d0e5fe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a81e8d79b9eb35a9e0bac9b762960b46ad455cc6ed877ba17eb3c67ad594b5d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d01d91fcbddb1cc56e0d03c20fe4d7a72ec967aff27828b9d4afd45b68a3f4(
    value: typing.Optional[GkeonpremVmwareClusterValidationCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__536be311f675dda0551ffb8e071a0b09168b8aa207fe934eeb9c207165928c68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da557063eaf4f879fe9bc6e01563a273738c7df615b3c02d155ff688e4d94424(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e998539dbb88cc9cd45e08422c247aab529023b7e7ff93100b4879a6cb957ceb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f01ee5a43628b6c9c00bfb8bc6d883fecfb9477bf3bf647104149ac7a391d22a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe6714040ebcd30aa57cdf65f2eaeca8923d2fecc7abd606529c6553715a528c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fff3df2eaf32cff1195ffb1038c67d53b66889c0266326dc0e396a511c44780(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b46efdb11830abebd07b2342cbd480d9c8fe96dbf8bfc747e79f89daaee4a0dc(
    value: typing.Optional[GkeonpremVmwareClusterValidationCheckStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bef091eef61e3487fc051a6ecf5b970fcb5eac5f5daea3f4d8216b02f84b917(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f88d328c038c3cb2ec75f6e118d339cc89cee9f88b2f62c76ad2477e1a54e791(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33f6c6d747aba27a6ab9fe5f5e541bfc18ee6e76fea66d5f6af7629055f4d3b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6e79a05e243ba4cdc1bf8cef8e2d2a5d0df87318b751f179fbd9986e41a7b15(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480119ff685b10d70364aa66e76a553b3d6f1ccdcbe19192ee1e8c1f23271fe5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be503e4f1cd42706def5fd6f3c6060f7af73d1545c17b1f67c94c67774f9d7d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31a82cad979bdcde9e0e7a75bfabb527a17cd0a5e7626663429ac9f57876df0(
    value: typing.Optional[GkeonpremVmwareClusterValidationCheckStatusResult],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8b7d41001800c6f17160ba5e0ce46933f2061186e9655096bde531ae508cbc2(
    *,
    ca_cert_data: typing.Optional[builtins.str] = None,
    cluster: typing.Optional[builtins.str] = None,
    datacenter: typing.Optional[builtins.str] = None,
    datastore: typing.Optional[builtins.str] = None,
    folder: typing.Optional[builtins.str] = None,
    resource_pool: typing.Optional[builtins.str] = None,
    storage_policy_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7446e10bedade96c46a076cfdc2df25c8eae5f3131e1d45f61d61c60a18a7b0c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fb9595d46631226da2c155967b2947d8d05a98333cb78fc671236cab49e930b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__436b44277b6aae25c793efac794bebcfe4d3cbf6214328a651e54f5a302b0280(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8795a2c9f85efc21d54103808ce2b0b76675577a5b5c61a7d521122611355477(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc6c5aa62577d0d12c0fa0d7150b2a205bbae5062d57cdac013dbf7a26108ad5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e2daf9a21f803f492ae6259709069d768f122c594e36136139865c9b2e5808f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__333de41f14602389cffdcd2683dc0b21b5715f3986a3c7b1f77babe3c2017081(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9455839712a3d9140c729fe930541b1830915928b161ca773bf88121751d66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53e22ef901d519c833b16ca2d594556c47cf20900516bbbb6cb97ff4d037c00c(
    value: typing.Optional[GkeonpremVmwareClusterVcenter],
) -> None:
    """Type checking stubs"""
    pass
