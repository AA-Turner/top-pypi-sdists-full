r'''
# `google_gkeonprem_vmware_cluster`

Refer to the Terraform Registry for docs: [`google_gkeonprem_vmware_cluster`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster).
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


class GoogleGkeonpremVmwareCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster google_gkeonprem_vmware_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        admin_cluster_membership: builtins.str,
        control_plane_node: typing.Union["GoogleGkeonpremVmwareClusterControlPlaneNode", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        on_prem_version: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        anti_affinity_groups: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterAntiAffinityGroups", typing.Dict[builtins.str, typing.Any]]] = None,
        authorization: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_repair_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterAutoRepairConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        dataplane_v2: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterDataplaneV2", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disable_bundled_ingress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_advanced_cluster: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_control_plane_v2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        load_balancer: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterLoadBalancer", typing.Dict[builtins.str, typing.Any]]] = None,
        network_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        storage: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        upgrade_policy: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterUpgradePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        vcenter: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterVcenter", typing.Dict[builtins.str, typing.Any]]] = None,
        vm_tracking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster google_gkeonprem_vmware_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param admin_cluster_membership: The admin cluster this VMware User Cluster belongs to. This is the full resource name of the admin cluster's hub membership. In the future, references to other resource types might be allowed if admin clusters are modeled as their own resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#admin_cluster_membership GoogleGkeonpremVmwareCluster#admin_cluster_membership}
        :param control_plane_node: control_plane_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#control_plane_node GoogleGkeonpremVmwareCluster#control_plane_node}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#location GoogleGkeonpremVmwareCluster#location}
        :param name: The VMware cluster name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#name GoogleGkeonpremVmwareCluster#name}
        :param on_prem_version: The Anthos clusters on the VMware version for your user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#on_prem_version GoogleGkeonpremVmwareCluster#on_prem_version}
        :param annotations: Annotations on the VMware User Cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#annotations GoogleGkeonpremVmwareCluster#annotations}
        :param anti_affinity_groups: anti_affinity_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#anti_affinity_groups GoogleGkeonpremVmwareCluster#anti_affinity_groups}
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#authorization GoogleGkeonpremVmwareCluster#authorization}
        :param auto_repair_config: auto_repair_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#auto_repair_config GoogleGkeonpremVmwareCluster#auto_repair_config}
        :param dataplane_v2: dataplane_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#dataplane_v2 GoogleGkeonpremVmwareCluster#dataplane_v2}
        :param description: A human readable description of this VMware User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#description GoogleGkeonpremVmwareCluster#description}
        :param disable_bundled_ingress: Disable bundled ingress. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#disable_bundled_ingress GoogleGkeonpremVmwareCluster#disable_bundled_ingress}
        :param enable_advanced_cluster: Enable advanced cluster. Default to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#enable_advanced_cluster GoogleGkeonpremVmwareCluster#enable_advanced_cluster}
        :param enable_control_plane_v2: Enable control plane V2. Default to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#enable_control_plane_v2 GoogleGkeonpremVmwareCluster#enable_control_plane_v2}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#id GoogleGkeonpremVmwareCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#load_balancer GoogleGkeonpremVmwareCluster#load_balancer}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#network_config GoogleGkeonpremVmwareCluster#network_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#project GoogleGkeonpremVmwareCluster#project}.
        :param storage: storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#storage GoogleGkeonpremVmwareCluster#storage}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#timeouts GoogleGkeonpremVmwareCluster#timeouts}
        :param upgrade_policy: upgrade_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#upgrade_policy GoogleGkeonpremVmwareCluster#upgrade_policy}
        :param vcenter: vcenter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#vcenter GoogleGkeonpremVmwareCluster#vcenter}
        :param vm_tracking_enabled: Enable VM tracking. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#vm_tracking_enabled GoogleGkeonpremVmwareCluster#vm_tracking_enabled}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86420fdab41dff2762e83f3fdf2b14401292efd0e9eab7e97231d74f032f02b8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleGkeonpremVmwareClusterConfig(
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
        '''Generates CDKTF code for importing a GoogleGkeonpremVmwareCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleGkeonpremVmwareCluster to import.
        :param import_from_id: The id of the existing GoogleGkeonpremVmwareCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleGkeonpremVmwareCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0f8ba31208e73a02de5cdfa4ff547d329eb6243ac52d7e1884b66816b622b65)
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
        :param aag_config_disabled: Spread nodes across at least three physical hosts (requires at least three hosts). Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#aag_config_disabled GoogleGkeonpremVmwareCluster#aag_config_disabled}
        '''
        value = GoogleGkeonpremVmwareClusterAntiAffinityGroups(
            aag_config_disabled=aag_config_disabled
        )

        return typing.cast(None, jsii.invoke(self, "putAntiAffinityGroups", [value]))

    @jsii.member(jsii_name="putAuthorization")
    def put_authorization(
        self,
        *,
        admin_users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremVmwareClusterAuthorizationAdminUsers", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#admin_users GoogleGkeonpremVmwareCluster#admin_users}
        '''
        value = GoogleGkeonpremVmwareClusterAuthorization(admin_users=admin_users)

        return typing.cast(None, jsii.invoke(self, "putAuthorization", [value]))

    @jsii.member(jsii_name="putAutoRepairConfig")
    def put_auto_repair_config(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether auto repair is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#enabled GoogleGkeonpremVmwareCluster#enabled}
        '''
        value = GoogleGkeonpremVmwareClusterAutoRepairConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putAutoRepairConfig", [value]))

    @jsii.member(jsii_name="putControlPlaneNode")
    def put_control_plane_node(
        self,
        *,
        auto_resize_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        cpus: typing.Optional[jsii.Number] = None,
        memory: typing.Optional[jsii.Number] = None,
        replicas: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param auto_resize_config: auto_resize_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#auto_resize_config GoogleGkeonpremVmwareCluster#auto_resize_config}
        :param cpus: The number of CPUs for each admin cluster node that serve as control planes for this VMware User Cluster. (default: 4 CPUs) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#cpus GoogleGkeonpremVmwareCluster#cpus}
        :param memory: The megabytes of memory for each admin cluster node that serves as a control plane for this VMware User Cluster (default: 8192 MB memory). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#memory GoogleGkeonpremVmwareCluster#memory}
        :param replicas: The number of control plane nodes for this VMware User Cluster. (default: 1 replica). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#replicas GoogleGkeonpremVmwareCluster#replicas}
        '''
        value = GoogleGkeonpremVmwareClusterControlPlaneNode(
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
        :param advanced_networking: Enable advanced networking which requires dataplane_v2_enabled to be set true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#advanced_networking GoogleGkeonpremVmwareCluster#advanced_networking}
        :param dataplane_v2_enabled: Enables Dataplane V2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#dataplane_v2_enabled GoogleGkeonpremVmwareCluster#dataplane_v2_enabled}
        :param windows_dataplane_v2_enabled: Enable Dataplane V2 for clusters with Windows nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#windows_dataplane_v2_enabled GoogleGkeonpremVmwareCluster#windows_dataplane_v2_enabled}
        '''
        value = GoogleGkeonpremVmwareClusterDataplaneV2(
            advanced_networking=advanced_networking,
            dataplane_v2_enabled=dataplane_v2_enabled,
            windows_dataplane_v2_enabled=windows_dataplane_v2_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putDataplaneV2", [value]))

    @jsii.member(jsii_name="putLoadBalancer")
    def put_load_balancer(
        self,
        *,
        f5_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterLoadBalancerF5Config", typing.Dict[builtins.str, typing.Any]]] = None,
        manual_lb_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterLoadBalancerManualLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        metal_lb_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        vip_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterLoadBalancerVipConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param f5_config: f5_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#f5_config GoogleGkeonpremVmwareCluster#f5_config}
        :param manual_lb_config: manual_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#manual_lb_config GoogleGkeonpremVmwareCluster#manual_lb_config}
        :param metal_lb_config: metal_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#metal_lb_config GoogleGkeonpremVmwareCluster#metal_lb_config}
        :param vip_config: vip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#vip_config GoogleGkeonpremVmwareCluster#vip_config}
        '''
        value = GoogleGkeonpremVmwareClusterLoadBalancer(
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
        control_plane_v2_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2Config", typing.Dict[builtins.str, typing.Any]]] = None,
        dhcp_ip_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterNetworkConfigDhcpIpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        host_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterNetworkConfigHostConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        static_ip_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        vcenter_network: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pod_address_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#pod_address_cidr_blocks GoogleGkeonpremVmwareCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported.. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#service_address_cidr_blocks GoogleGkeonpremVmwareCluster#service_address_cidr_blocks}
        :param control_plane_v2_config: control_plane_v2_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#control_plane_v2_config GoogleGkeonpremVmwareCluster#control_plane_v2_config}
        :param dhcp_ip_config: dhcp_ip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#dhcp_ip_config GoogleGkeonpremVmwareCluster#dhcp_ip_config}
        :param host_config: host_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#host_config GoogleGkeonpremVmwareCluster#host_config}
        :param static_ip_config: static_ip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#static_ip_config GoogleGkeonpremVmwareCluster#static_ip_config}
        :param vcenter_network: vcenter_network specifies vCenter network name. Inherited from the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#vcenter_network GoogleGkeonpremVmwareCluster#vcenter_network}
        '''
        value = GoogleGkeonpremVmwareClusterNetworkConfig(
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
        :param vsphere_csi_disabled: Whether or not to deploy vSphere CSI components in the VMware User Cluster. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#vsphere_csi_disabled GoogleGkeonpremVmwareCluster#vsphere_csi_disabled}
        '''
        value = GoogleGkeonpremVmwareClusterStorage(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#create GoogleGkeonpremVmwareCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#delete GoogleGkeonpremVmwareCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#update GoogleGkeonpremVmwareCluster#update}.
        '''
        value = GoogleGkeonpremVmwareClusterTimeouts(
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
        :param control_plane_only: Controls whether the upgrade applies to the control plane only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#control_plane_only GoogleGkeonpremVmwareCluster#control_plane_only}
        '''
        value = GoogleGkeonpremVmwareClusterUpgradePolicy(
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
        :param ca_cert_data: Contains the vCenter CA certificate public key for SSL verification. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ca_cert_data GoogleGkeonpremVmwareCluster#ca_cert_data}
        :param cluster: The name of the vCenter cluster for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#cluster GoogleGkeonpremVmwareCluster#cluster}
        :param datacenter: The name of the vCenter datacenter for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#datacenter GoogleGkeonpremVmwareCluster#datacenter}
        :param datastore: The name of the vCenter datastore for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#datastore GoogleGkeonpremVmwareCluster#datastore}
        :param folder: The name of the vCenter folder for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#folder GoogleGkeonpremVmwareCluster#folder}
        :param resource_pool: The name of the vCenter resource pool for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#resource_pool GoogleGkeonpremVmwareCluster#resource_pool}
        :param storage_policy_name: The name of the vCenter storage policy for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#storage_policy_name GoogleGkeonpremVmwareCluster#storage_policy_name}
        '''
        value = GoogleGkeonpremVmwareClusterVcenter(
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
    ) -> "GoogleGkeonpremVmwareClusterAntiAffinityGroupsOutputReference":
        return typing.cast("GoogleGkeonpremVmwareClusterAntiAffinityGroupsOutputReference", jsii.get(self, "antiAffinityGroups"))

    @builtins.property
    @jsii.member(jsii_name="authorization")
    def authorization(
        self,
    ) -> "GoogleGkeonpremVmwareClusterAuthorizationOutputReference":
        return typing.cast("GoogleGkeonpremVmwareClusterAuthorizationOutputReference", jsii.get(self, "authorization"))

    @builtins.property
    @jsii.member(jsii_name="autoRepairConfig")
    def auto_repair_config(
        self,
    ) -> "GoogleGkeonpremVmwareClusterAutoRepairConfigOutputReference":
        return typing.cast("GoogleGkeonpremVmwareClusterAutoRepairConfigOutputReference", jsii.get(self, "autoRepairConfig"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneNode")
    def control_plane_node(
        self,
    ) -> "GoogleGkeonpremVmwareClusterControlPlaneNodeOutputReference":
        return typing.cast("GoogleGkeonpremVmwareClusterControlPlaneNodeOutputReference", jsii.get(self, "controlPlaneNode"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="dataplaneV2")
    def dataplane_v2(self) -> "GoogleGkeonpremVmwareClusterDataplaneV2OutputReference":
        return typing.cast("GoogleGkeonpremVmwareClusterDataplaneV2OutputReference", jsii.get(self, "dataplaneV2"))

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
    def fleet(self) -> "GoogleGkeonpremVmwareClusterFleetList":
        return typing.cast("GoogleGkeonpremVmwareClusterFleetList", jsii.get(self, "fleet"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(
        self,
    ) -> "GoogleGkeonpremVmwareClusterLoadBalancerOutputReference":
        return typing.cast("GoogleGkeonpremVmwareClusterLoadBalancerOutputReference", jsii.get(self, "loadBalancer"))

    @builtins.property
    @jsii.member(jsii_name="localName")
    def local_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localName"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(
        self,
    ) -> "GoogleGkeonpremVmwareClusterNetworkConfigOutputReference":
        return typing.cast("GoogleGkeonpremVmwareClusterNetworkConfigOutputReference", jsii.get(self, "networkConfig"))

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
    def status(self) -> "GoogleGkeonpremVmwareClusterStatusList":
        return typing.cast("GoogleGkeonpremVmwareClusterStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="storage")
    def storage(self) -> "GoogleGkeonpremVmwareClusterStorageOutputReference":
        return typing.cast("GoogleGkeonpremVmwareClusterStorageOutputReference", jsii.get(self, "storage"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleGkeonpremVmwareClusterTimeoutsOutputReference":
        return typing.cast("GoogleGkeonpremVmwareClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    def upgrade_policy(
        self,
    ) -> "GoogleGkeonpremVmwareClusterUpgradePolicyOutputReference":
        return typing.cast("GoogleGkeonpremVmwareClusterUpgradePolicyOutputReference", jsii.get(self, "upgradePolicy"))

    @builtins.property
    @jsii.member(jsii_name="validationCheck")
    def validation_check(self) -> "GoogleGkeonpremVmwareClusterValidationCheckList":
        return typing.cast("GoogleGkeonpremVmwareClusterValidationCheckList", jsii.get(self, "validationCheck"))

    @builtins.property
    @jsii.member(jsii_name="vcenter")
    def vcenter(self) -> "GoogleGkeonpremVmwareClusterVcenterOutputReference":
        return typing.cast("GoogleGkeonpremVmwareClusterVcenterOutputReference", jsii.get(self, "vcenter"))

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
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterAntiAffinityGroups"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterAntiAffinityGroups"], jsii.get(self, "antiAffinityGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationInput")
    def authorization_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterAuthorization"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterAuthorization"], jsii.get(self, "authorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="autoRepairConfigInput")
    def auto_repair_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterAutoRepairConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterAutoRepairConfig"], jsii.get(self, "autoRepairConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneNodeInput")
    def control_plane_node_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterControlPlaneNode"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterControlPlaneNode"], jsii.get(self, "controlPlaneNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="dataplaneV2Input")
    def dataplane_v2_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterDataplaneV2"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterDataplaneV2"], jsii.get(self, "dataplaneV2Input"))

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
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterLoadBalancer"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterLoadBalancer"], jsii.get(self, "loadBalancerInput"))

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
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterNetworkConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterNetworkConfig"], jsii.get(self, "networkConfigInput"))

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
    def storage_input(self) -> typing.Optional["GoogleGkeonpremVmwareClusterStorage"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterStorage"], jsii.get(self, "storageInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleGkeonpremVmwareClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleGkeonpremVmwareClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="upgradePolicyInput")
    def upgrade_policy_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterUpgradePolicy"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterUpgradePolicy"], jsii.get(self, "upgradePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="vcenterInput")
    def vcenter_input(self) -> typing.Optional["GoogleGkeonpremVmwareClusterVcenter"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterVcenter"], jsii.get(self, "vcenterInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__487d75aaff6510c9ad62463eff2a3207d220d73fa63fb6a8254225a8354a6632)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminClusterMembership", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1d3d7943bb0a079575434a31fb4d6537317c6faa7d793979c085a099c55563d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__301e8e5f5f773aede850fd9411f071e5dd15c94c44a7931e2c9c3207529390d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa135ba8f30f45fe8b3e20b0bc1c280ea98d5133db1948166a1b811b32e32674)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5af5a2d9590b65d45479f930700050416c33be4c4cfb1a58cb1d2745a737d570)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2be2154a3e9e6ff2573a30e4142d4f1442b29961aef355ca2b330e829d904cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableControlPlaneV2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1fcc27b5eb93fe9e0b6e8047d323bf6d63f85d97afc104c2fe824be65425109)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2372fc84cde5c02244d1b44bd829e9d70227c311ef051fb08f8bcd3d6c53cdc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b18a462965ff6cbd22da94d6a042802d7e7046a24fdc8f2bce0400d8c86779)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onPremVersion")
    def on_prem_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onPremVersion"))

    @on_prem_version.setter
    def on_prem_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__561b501e45c9a1d73cbf1b561cbd3256ab89f2e2a45208758e1cdc5f6377c7e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onPremVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a570b0e316733ab5c4d8f5255360e9078f29eeaf1dcc0ff29523a48859c1cb65)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7322bc27bf8b7de584501281f1b94788adbe51e91346e4c879958e210831bff8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmTrackingEnabled", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterAntiAffinityGroups",
    jsii_struct_bases=[],
    name_mapping={"aag_config_disabled": "aagConfigDisabled"},
)
class GoogleGkeonpremVmwareClusterAntiAffinityGroups:
    def __init__(
        self,
        *,
        aag_config_disabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param aag_config_disabled: Spread nodes across at least three physical hosts (requires at least three hosts). Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#aag_config_disabled GoogleGkeonpremVmwareCluster#aag_config_disabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b4ab249f2e88878143a060fcc3a90d74e768a06bfc3983ba114117895b02f04)
            check_type(argname="argument aag_config_disabled", value=aag_config_disabled, expected_type=type_hints["aag_config_disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aag_config_disabled": aag_config_disabled,
        }

    @builtins.property
    def aag_config_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Spread nodes across at least three physical hosts (requires at least three hosts). Enabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#aag_config_disabled GoogleGkeonpremVmwareCluster#aag_config_disabled}
        '''
        result = self._values.get("aag_config_disabled")
        assert result is not None, "Required property 'aag_config_disabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterAntiAffinityGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareClusterAntiAffinityGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterAntiAffinityGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fda6aa394cd5f688f5897e959d2a57a2e88e04c9b3a96372e10a1226392a499f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e21ad2a0c4807b3f1f366dc126b3653e5b5ad50ac508861acd0c4ed8478131a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aagConfigDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterAntiAffinityGroups]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterAntiAffinityGroups], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterAntiAffinityGroups],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38ded6d5657e306d9a3e1226d5c54a5ba14ac49ca1a7f2f82ab523c817323102)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterAuthorization",
    jsii_struct_bases=[],
    name_mapping={"admin_users": "adminUsers"},
)
class GoogleGkeonpremVmwareClusterAuthorization:
    def __init__(
        self,
        *,
        admin_users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremVmwareClusterAuthorizationAdminUsers", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#admin_users GoogleGkeonpremVmwareCluster#admin_users}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__873c73a188918c48f5d195752b3ccf2291558ea9345130c1440398f5c0c35e22)
            check_type(argname="argument admin_users", value=admin_users, expected_type=type_hints["admin_users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if admin_users is not None:
            self._values["admin_users"] = admin_users

    @builtins.property
    def admin_users(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremVmwareClusterAuthorizationAdminUsers"]]]:
        '''admin_users block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#admin_users GoogleGkeonpremVmwareCluster#admin_users}
        '''
        result = self._values.get("admin_users")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremVmwareClusterAuthorizationAdminUsers"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterAuthorizationAdminUsers",
    jsii_struct_bases=[],
    name_mapping={"username": "username"},
)
class GoogleGkeonpremVmwareClusterAuthorizationAdminUsers:
    def __init__(self, *, username: builtins.str) -> None:
        '''
        :param username: The name of the user, e.g. 'my-gcp-id@gmail.com'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#username GoogleGkeonpremVmwareCluster#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee06517fd84049a0db43a933bcd086879e512d7f5af68c329344dc225ae97a27)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
        }

    @builtins.property
    def username(self) -> builtins.str:
        '''The name of the user, e.g. 'my-gcp-id@gmail.com'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#username GoogleGkeonpremVmwareCluster#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterAuthorizationAdminUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareClusterAuthorizationAdminUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterAuthorizationAdminUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ac72a11aec2d2b03599fa88b2ed6808bb9f6d3421f63962898f206eab1ab7f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareClusterAuthorizationAdminUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dad57d8c57ca9ec60419740b1711c1eeb37214461b1587b5547edbbf2f4c53f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareClusterAuthorizationAdminUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d223a294844fe8e4a87316bef9cf2fe36c2375073f5703c7d2c056246e77576)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9221664457374004554cd3a9b0bdef87e51a6dfb916a442b7eef859838d1d2d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9ac712006d144e1fc25223b8ea00f82ad18a1fe4d7e978e37d55ef47144e5af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterAuthorizationAdminUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterAuthorizationAdminUsers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterAuthorizationAdminUsers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c25014bdb2f9686b43874ecfc125ae405bc9a618ffbaf45e28e5a1d58fbef030)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareClusterAuthorizationAdminUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterAuthorizationAdminUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__234965f7715361d354c30abebc8f7bdd0ed4d76202a97b13a027f8f423390d85)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73ce34b2b6ec650294d45a8a374ca1bede15aaaf3dc9f03095a043740ce592a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterAuthorizationAdminUsers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterAuthorizationAdminUsers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterAuthorizationAdminUsers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8b85b252f9e3635912a7358862389f33ea5133c0a00efc83891dd27c58de551)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareClusterAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90a8d95b736b2ea3882ca873d3b8cbab0151b05d6f89f9e4e9fee7d02540c2f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdminUsers")
    def put_admin_users(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareClusterAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d27646eefdd31c823e7d2467ea82342f3617691ae6083b9513411d045c5e1310)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdminUsers", [value]))

    @jsii.member(jsii_name="resetAdminUsers")
    def reset_admin_users(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminUsers", []))

    @builtins.property
    @jsii.member(jsii_name="adminUsers")
    def admin_users(self) -> GoogleGkeonpremVmwareClusterAuthorizationAdminUsersList:
        return typing.cast(GoogleGkeonpremVmwareClusterAuthorizationAdminUsersList, jsii.get(self, "adminUsers"))

    @builtins.property
    @jsii.member(jsii_name="adminUsersInput")
    def admin_users_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterAuthorizationAdminUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterAuthorizationAdminUsers]]], jsii.get(self, "adminUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterAuthorization]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df20338a179877239d95a7ee2144618552637b94043b71f55548afcf07155fc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterAutoRepairConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleGkeonpremVmwareClusterAutoRepairConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether auto repair is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#enabled GoogleGkeonpremVmwareCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21838d6652f43b51c1b3f7dde57f92dff82b6a869c7829a5970b3ccd5da9cf8c)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether auto repair is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#enabled GoogleGkeonpremVmwareCluster#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterAutoRepairConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareClusterAutoRepairConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterAutoRepairConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f892f9c828ffe5f44829e200d9f14d569ec9b2d6e482a6062bbf0ba1984c6c88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__429e20a7778e2673e28af8aa6d108730bfc5aa1f81540757c969f0ab719fd441)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterAutoRepairConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterAutoRepairConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterAutoRepairConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43b61644b1c094de2e7ba5a11c93db8e0086d9361141ba00b3b74b5e039a0c78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterConfig",
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
class GoogleGkeonpremVmwareClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        control_plane_node: typing.Union["GoogleGkeonpremVmwareClusterControlPlaneNode", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        on_prem_version: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        anti_affinity_groups: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterAntiAffinityGroups, typing.Dict[builtins.str, typing.Any]]] = None,
        authorization: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_repair_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterAutoRepairConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        dataplane_v2: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterDataplaneV2", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disable_bundled_ingress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_advanced_cluster: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_control_plane_v2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        load_balancer: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterLoadBalancer", typing.Dict[builtins.str, typing.Any]]] = None,
        network_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        storage: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        upgrade_policy: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterUpgradePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        vcenter: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterVcenter", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param admin_cluster_membership: The admin cluster this VMware User Cluster belongs to. This is the full resource name of the admin cluster's hub membership. In the future, references to other resource types might be allowed if admin clusters are modeled as their own resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#admin_cluster_membership GoogleGkeonpremVmwareCluster#admin_cluster_membership}
        :param control_plane_node: control_plane_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#control_plane_node GoogleGkeonpremVmwareCluster#control_plane_node}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#location GoogleGkeonpremVmwareCluster#location}
        :param name: The VMware cluster name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#name GoogleGkeonpremVmwareCluster#name}
        :param on_prem_version: The Anthos clusters on the VMware version for your user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#on_prem_version GoogleGkeonpremVmwareCluster#on_prem_version}
        :param annotations: Annotations on the VMware User Cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#annotations GoogleGkeonpremVmwareCluster#annotations}
        :param anti_affinity_groups: anti_affinity_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#anti_affinity_groups GoogleGkeonpremVmwareCluster#anti_affinity_groups}
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#authorization GoogleGkeonpremVmwareCluster#authorization}
        :param auto_repair_config: auto_repair_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#auto_repair_config GoogleGkeonpremVmwareCluster#auto_repair_config}
        :param dataplane_v2: dataplane_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#dataplane_v2 GoogleGkeonpremVmwareCluster#dataplane_v2}
        :param description: A human readable description of this VMware User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#description GoogleGkeonpremVmwareCluster#description}
        :param disable_bundled_ingress: Disable bundled ingress. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#disable_bundled_ingress GoogleGkeonpremVmwareCluster#disable_bundled_ingress}
        :param enable_advanced_cluster: Enable advanced cluster. Default to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#enable_advanced_cluster GoogleGkeonpremVmwareCluster#enable_advanced_cluster}
        :param enable_control_plane_v2: Enable control plane V2. Default to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#enable_control_plane_v2 GoogleGkeonpremVmwareCluster#enable_control_plane_v2}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#id GoogleGkeonpremVmwareCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#load_balancer GoogleGkeonpremVmwareCluster#load_balancer}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#network_config GoogleGkeonpremVmwareCluster#network_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#project GoogleGkeonpremVmwareCluster#project}.
        :param storage: storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#storage GoogleGkeonpremVmwareCluster#storage}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#timeouts GoogleGkeonpremVmwareCluster#timeouts}
        :param upgrade_policy: upgrade_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#upgrade_policy GoogleGkeonpremVmwareCluster#upgrade_policy}
        :param vcenter: vcenter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#vcenter GoogleGkeonpremVmwareCluster#vcenter}
        :param vm_tracking_enabled: Enable VM tracking. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#vm_tracking_enabled GoogleGkeonpremVmwareCluster#vm_tracking_enabled}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(control_plane_node, dict):
            control_plane_node = GoogleGkeonpremVmwareClusterControlPlaneNode(**control_plane_node)
        if isinstance(anti_affinity_groups, dict):
            anti_affinity_groups = GoogleGkeonpremVmwareClusterAntiAffinityGroups(**anti_affinity_groups)
        if isinstance(authorization, dict):
            authorization = GoogleGkeonpremVmwareClusterAuthorization(**authorization)
        if isinstance(auto_repair_config, dict):
            auto_repair_config = GoogleGkeonpremVmwareClusterAutoRepairConfig(**auto_repair_config)
        if isinstance(dataplane_v2, dict):
            dataplane_v2 = GoogleGkeonpremVmwareClusterDataplaneV2(**dataplane_v2)
        if isinstance(load_balancer, dict):
            load_balancer = GoogleGkeonpremVmwareClusterLoadBalancer(**load_balancer)
        if isinstance(network_config, dict):
            network_config = GoogleGkeonpremVmwareClusterNetworkConfig(**network_config)
        if isinstance(storage, dict):
            storage = GoogleGkeonpremVmwareClusterStorage(**storage)
        if isinstance(timeouts, dict):
            timeouts = GoogleGkeonpremVmwareClusterTimeouts(**timeouts)
        if isinstance(upgrade_policy, dict):
            upgrade_policy = GoogleGkeonpremVmwareClusterUpgradePolicy(**upgrade_policy)
        if isinstance(vcenter, dict):
            vcenter = GoogleGkeonpremVmwareClusterVcenter(**vcenter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd6195c5b1b87631c0536545cd449ce4c51af9dfcb98c51cfe475ab2d5ffafc3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#admin_cluster_membership GoogleGkeonpremVmwareCluster#admin_cluster_membership}
        '''
        result = self._values.get("admin_cluster_membership")
        assert result is not None, "Required property 'admin_cluster_membership' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def control_plane_node(self) -> "GoogleGkeonpremVmwareClusterControlPlaneNode":
        '''control_plane_node block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#control_plane_node GoogleGkeonpremVmwareCluster#control_plane_node}
        '''
        result = self._values.get("control_plane_node")
        assert result is not None, "Required property 'control_plane_node' is missing"
        return typing.cast("GoogleGkeonpremVmwareClusterControlPlaneNode", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#location GoogleGkeonpremVmwareCluster#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The VMware cluster name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#name GoogleGkeonpremVmwareCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def on_prem_version(self) -> builtins.str:
        '''The Anthos clusters on the VMware version for your user cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#on_prem_version GoogleGkeonpremVmwareCluster#on_prem_version}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#annotations GoogleGkeonpremVmwareCluster#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def anti_affinity_groups(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterAntiAffinityGroups]:
        '''anti_affinity_groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#anti_affinity_groups GoogleGkeonpremVmwareCluster#anti_affinity_groups}
        '''
        result = self._values.get("anti_affinity_groups")
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterAntiAffinityGroups], result)

    @builtins.property
    def authorization(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterAuthorization]:
        '''authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#authorization GoogleGkeonpremVmwareCluster#authorization}
        '''
        result = self._values.get("authorization")
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterAuthorization], result)

    @builtins.property
    def auto_repair_config(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterAutoRepairConfig]:
        '''auto_repair_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#auto_repair_config GoogleGkeonpremVmwareCluster#auto_repair_config}
        '''
        result = self._values.get("auto_repair_config")
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterAutoRepairConfig], result)

    @builtins.property
    def dataplane_v2(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterDataplaneV2"]:
        '''dataplane_v2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#dataplane_v2 GoogleGkeonpremVmwareCluster#dataplane_v2}
        '''
        result = self._values.get("dataplane_v2")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterDataplaneV2"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human readable description of this VMware User Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#description GoogleGkeonpremVmwareCluster#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_bundled_ingress(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable bundled ingress.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#disable_bundled_ingress GoogleGkeonpremVmwareCluster#disable_bundled_ingress}
        '''
        result = self._values.get("disable_bundled_ingress")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_advanced_cluster(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable advanced cluster. Default to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#enable_advanced_cluster GoogleGkeonpremVmwareCluster#enable_advanced_cluster}
        '''
        result = self._values.get("enable_advanced_cluster")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_control_plane_v2(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable control plane V2. Default to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#enable_control_plane_v2 GoogleGkeonpremVmwareCluster#enable_control_plane_v2}
        '''
        result = self._values.get("enable_control_plane_v2")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#id GoogleGkeonpremVmwareCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterLoadBalancer"]:
        '''load_balancer block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#load_balancer GoogleGkeonpremVmwareCluster#load_balancer}
        '''
        result = self._values.get("load_balancer")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterLoadBalancer"], result)

    @builtins.property
    def network_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterNetworkConfig"]:
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#network_config GoogleGkeonpremVmwareCluster#network_config}
        '''
        result = self._values.get("network_config")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterNetworkConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#project GoogleGkeonpremVmwareCluster#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage(self) -> typing.Optional["GoogleGkeonpremVmwareClusterStorage"]:
        '''storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#storage GoogleGkeonpremVmwareCluster#storage}
        '''
        result = self._values.get("storage")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterStorage"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleGkeonpremVmwareClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#timeouts GoogleGkeonpremVmwareCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterTimeouts"], result)

    @builtins.property
    def upgrade_policy(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterUpgradePolicy"]:
        '''upgrade_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#upgrade_policy GoogleGkeonpremVmwareCluster#upgrade_policy}
        '''
        result = self._values.get("upgrade_policy")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterUpgradePolicy"], result)

    @builtins.property
    def vcenter(self) -> typing.Optional["GoogleGkeonpremVmwareClusterVcenter"]:
        '''vcenter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#vcenter GoogleGkeonpremVmwareCluster#vcenter}
        '''
        result = self._values.get("vcenter")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterVcenter"], result)

    @builtins.property
    def vm_tracking_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable VM tracking.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#vm_tracking_enabled GoogleGkeonpremVmwareCluster#vm_tracking_enabled}
        '''
        result = self._values.get("vm_tracking_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterControlPlaneNode",
    jsii_struct_bases=[],
    name_mapping={
        "auto_resize_config": "autoResizeConfig",
        "cpus": "cpus",
        "memory": "memory",
        "replicas": "replicas",
    },
)
class GoogleGkeonpremVmwareClusterControlPlaneNode:
    def __init__(
        self,
        *,
        auto_resize_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        cpus: typing.Optional[jsii.Number] = None,
        memory: typing.Optional[jsii.Number] = None,
        replicas: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param auto_resize_config: auto_resize_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#auto_resize_config GoogleGkeonpremVmwareCluster#auto_resize_config}
        :param cpus: The number of CPUs for each admin cluster node that serve as control planes for this VMware User Cluster. (default: 4 CPUs) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#cpus GoogleGkeonpremVmwareCluster#cpus}
        :param memory: The megabytes of memory for each admin cluster node that serves as a control plane for this VMware User Cluster (default: 8192 MB memory). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#memory GoogleGkeonpremVmwareCluster#memory}
        :param replicas: The number of control plane nodes for this VMware User Cluster. (default: 1 replica). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#replicas GoogleGkeonpremVmwareCluster#replicas}
        '''
        if isinstance(auto_resize_config, dict):
            auto_resize_config = GoogleGkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig(**auto_resize_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22eaffa880a77736fb8f0819b9181f77fc1af579f672d16624643410a92cd204)
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
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig"]:
        '''auto_resize_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#auto_resize_config GoogleGkeonpremVmwareCluster#auto_resize_config}
        '''
        result = self._values.get("auto_resize_config")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig"], result)

    @builtins.property
    def cpus(self) -> typing.Optional[jsii.Number]:
        '''The number of CPUs for each admin cluster node that serve as control planes for this VMware User Cluster.

        (default: 4 CPUs)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#cpus GoogleGkeonpremVmwareCluster#cpus}
        '''
        result = self._values.get("cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory(self) -> typing.Optional[jsii.Number]:
        '''The megabytes of memory for each admin cluster node that serves as a control plane for this VMware User Cluster (default: 8192 MB memory).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#memory GoogleGkeonpremVmwareCluster#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def replicas(self) -> typing.Optional[jsii.Number]:
        '''The number of control plane nodes for this VMware User Cluster. (default: 1 replica).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#replicas GoogleGkeonpremVmwareCluster#replicas}
        '''
        result = self._values.get("replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterControlPlaneNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleGkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether to enable control plane node auto resizing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#enabled GoogleGkeonpremVmwareCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c219b3f8be581d95c1426d836c6e7e11242715500b6f430b52cccc4b4ed393e)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether to enable control plane node auto resizing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#enabled GoogleGkeonpremVmwareCluster#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareClusterControlPlaneNodeAutoResizeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterControlPlaneNodeAutoResizeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42d0b3606582d25c80d7fdddb1573bec6804557a8f091c899495af598f85cb4e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdc1c87ff43c3abb6fc8d76af7f7077edd3d4836643d4023e595617f248806ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf09813cd5240840e9709ce92c2d7c962314f03d997baa4415b19dff12260cbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareClusterControlPlaneNodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterControlPlaneNodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe922d24be72e2c658666cb0c02fc760bb7b1765626a70a450b2885d417f08fa)
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
        :param enabled: Whether to enable control plane node auto resizing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#enabled GoogleGkeonpremVmwareCluster#enabled}
        '''
        value = GoogleGkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig(
            enabled=enabled
        )

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
    ) -> GoogleGkeonpremVmwareClusterControlPlaneNodeAutoResizeConfigOutputReference:
        return typing.cast(GoogleGkeonpremVmwareClusterControlPlaneNodeAutoResizeConfigOutputReference, jsii.get(self, "autoResizeConfig"))

    @builtins.property
    @jsii.member(jsii_name="vsphereConfig")
    def vsphere_config(
        self,
    ) -> "GoogleGkeonpremVmwareClusterControlPlaneNodeVsphereConfigList":
        return typing.cast("GoogleGkeonpremVmwareClusterControlPlaneNodeVsphereConfigList", jsii.get(self, "vsphereConfig"))

    @builtins.property
    @jsii.member(jsii_name="autoResizeConfigInput")
    def auto_resize_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig], jsii.get(self, "autoResizeConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__061491782d5d7474afc85c1787ffee4f43f391937f8eb76d8ebe8fae581ee830)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecee1505823e3106324ed8f1c0228e214f983f6a57fb7d1c1241a7ef1119c7d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicas")
    def replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicas"))

    @replicas.setter
    def replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a254fdfdf578aef7fc4140d1b426b703799e16abbaece7ce621f12625bc961c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterControlPlaneNode]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterControlPlaneNode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterControlPlaneNode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67a84dff571fced7564b6f8dcdd5f4a93c295402fb69d74b2d2b310f00d90829)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterControlPlaneNodeVsphereConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremVmwareClusterControlPlaneNodeVsphereConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterControlPlaneNodeVsphereConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareClusterControlPlaneNodeVsphereConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterControlPlaneNodeVsphereConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f464d428793516357776688b3c71587079bbdd42234b63cca602f97936bd6b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareClusterControlPlaneNodeVsphereConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7397f9204d9cedb2b87ec83aa5e68bda471114f2207efc33105f028330c6be2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareClusterControlPlaneNodeVsphereConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54318b4b195822c9700f4b10355eb9f6193d7d1bc7a7fec8ea0b4b05e1e2888b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a28b892d4254e1e28c7027da1615e1c6894838dd1cd352ebfeb52c16ceeb2cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f494ad100fe49719310c802f817d901c4da2749afc072b6907b4f4f56f89bc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareClusterControlPlaneNodeVsphereConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterControlPlaneNodeVsphereConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee5f8766a889d26a252e2379f1ee2063d173499c8efe8606882dcf5fdb228f95)
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
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterControlPlaneNodeVsphereConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterControlPlaneNodeVsphereConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterControlPlaneNodeVsphereConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7356a2ebe6916e01f87dbbe6e9de71cf36f5ceead19d41f3220742df9e66c9de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterDataplaneV2",
    jsii_struct_bases=[],
    name_mapping={
        "advanced_networking": "advancedNetworking",
        "dataplane_v2_enabled": "dataplaneV2Enabled",
        "windows_dataplane_v2_enabled": "windowsDataplaneV2Enabled",
    },
)
class GoogleGkeonpremVmwareClusterDataplaneV2:
    def __init__(
        self,
        *,
        advanced_networking: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dataplane_v2_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        windows_dataplane_v2_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param advanced_networking: Enable advanced networking which requires dataplane_v2_enabled to be set true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#advanced_networking GoogleGkeonpremVmwareCluster#advanced_networking}
        :param dataplane_v2_enabled: Enables Dataplane V2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#dataplane_v2_enabled GoogleGkeonpremVmwareCluster#dataplane_v2_enabled}
        :param windows_dataplane_v2_enabled: Enable Dataplane V2 for clusters with Windows nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#windows_dataplane_v2_enabled GoogleGkeonpremVmwareCluster#windows_dataplane_v2_enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4afee76698869fd2fa3b86d41ff1a40d3a0e9900b71270fa686e0c44ae82dfff)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#advanced_networking GoogleGkeonpremVmwareCluster#advanced_networking}
        '''
        result = self._values.get("advanced_networking")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dataplane_v2_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables Dataplane V2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#dataplane_v2_enabled GoogleGkeonpremVmwareCluster#dataplane_v2_enabled}
        '''
        result = self._values.get("dataplane_v2_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def windows_dataplane_v2_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable Dataplane V2 for clusters with Windows nodes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#windows_dataplane_v2_enabled GoogleGkeonpremVmwareCluster#windows_dataplane_v2_enabled}
        '''
        result = self._values.get("windows_dataplane_v2_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterDataplaneV2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareClusterDataplaneV2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterDataplaneV2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44f37fdb825b7eb21af6e6c2d2231e8eb2f25a66eec0626e906090a06519c145)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9514a90f5e8d20f5b9d337150019e4d9a83f95970f728ad3d98392966a8e9e68)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91a0b4b300ad422a286761d24c5abc067e9d8b13e093197bc19275a4404830db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f5ecda78b7e59a778a8f7f2d6b48fab4fb654e9cb85c0d9311dad5a70228a9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowsDataplaneV2Enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterDataplaneV2]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterDataplaneV2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterDataplaneV2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e78f0f58eaf3288c3c6c9da9ed3d6f86806204708d1514ef6e29ca3c738ca57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterFleet",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremVmwareClusterFleet:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterFleet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareClusterFleetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterFleetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dff6b6f966c3d8eebf7e69197e704ca4f882526a43ded7daa53d50647bfed2f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareClusterFleetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bda85a310c6d356a6ccf295ce74b5c402e5e4d151819da8b1e651693d72f7e1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareClusterFleetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9681b76aef1bcc026c41b52fa3c5ef64eb2bf7c68f673aeaf1bd3d19ffa00b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8718fb0d8336d698b64b8b82f9a513c481910646e8080774a13ea2a4069640e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b368ffebaa78925db39b39300f0f1db32916b192be0c74aa0b7b5d2afc55ead)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareClusterFleetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterFleetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebe118e67e7afcbe3ab472f37b67a55c2849fcd88bf73f6284f597762668908a)
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
    def internal_value(self) -> typing.Optional[GoogleGkeonpremVmwareClusterFleet]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterFleet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterFleet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bd3530acf43e2e553a89455672b0625ccdd51889e978977531b7bb2cc812e9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterLoadBalancer",
    jsii_struct_bases=[],
    name_mapping={
        "f5_config": "f5Config",
        "manual_lb_config": "manualLbConfig",
        "metal_lb_config": "metalLbConfig",
        "vip_config": "vipConfig",
    },
)
class GoogleGkeonpremVmwareClusterLoadBalancer:
    def __init__(
        self,
        *,
        f5_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterLoadBalancerF5Config", typing.Dict[builtins.str, typing.Any]]] = None,
        manual_lb_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterLoadBalancerManualLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        metal_lb_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        vip_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterLoadBalancerVipConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param f5_config: f5_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#f5_config GoogleGkeonpremVmwareCluster#f5_config}
        :param manual_lb_config: manual_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#manual_lb_config GoogleGkeonpremVmwareCluster#manual_lb_config}
        :param metal_lb_config: metal_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#metal_lb_config GoogleGkeonpremVmwareCluster#metal_lb_config}
        :param vip_config: vip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#vip_config GoogleGkeonpremVmwareCluster#vip_config}
        '''
        if isinstance(f5_config, dict):
            f5_config = GoogleGkeonpremVmwareClusterLoadBalancerF5Config(**f5_config)
        if isinstance(manual_lb_config, dict):
            manual_lb_config = GoogleGkeonpremVmwareClusterLoadBalancerManualLbConfig(**manual_lb_config)
        if isinstance(metal_lb_config, dict):
            metal_lb_config = GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfig(**metal_lb_config)
        if isinstance(vip_config, dict):
            vip_config = GoogleGkeonpremVmwareClusterLoadBalancerVipConfig(**vip_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ac7c13aa95a45273c6cc6deedf6fab7be22314bf5111b5d2c019174aa437d59)
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
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterLoadBalancerF5Config"]:
        '''f5_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#f5_config GoogleGkeonpremVmwareCluster#f5_config}
        '''
        result = self._values.get("f5_config")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterLoadBalancerF5Config"], result)

    @builtins.property
    def manual_lb_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterLoadBalancerManualLbConfig"]:
        '''manual_lb_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#manual_lb_config GoogleGkeonpremVmwareCluster#manual_lb_config}
        '''
        result = self._values.get("manual_lb_config")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterLoadBalancerManualLbConfig"], result)

    @builtins.property
    def metal_lb_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfig"]:
        '''metal_lb_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#metal_lb_config GoogleGkeonpremVmwareCluster#metal_lb_config}
        '''
        result = self._values.get("metal_lb_config")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfig"], result)

    @builtins.property
    def vip_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterLoadBalancerVipConfig"]:
        '''vip_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#vip_config GoogleGkeonpremVmwareCluster#vip_config}
        '''
        result = self._values.get("vip_config")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterLoadBalancerVipConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterLoadBalancer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterLoadBalancerF5Config",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "partition": "partition",
        "snat_pool": "snatPool",
    },
)
class GoogleGkeonpremVmwareClusterLoadBalancerF5Config:
    def __init__(
        self,
        *,
        address: typing.Optional[builtins.str] = None,
        partition: typing.Optional[builtins.str] = None,
        snat_pool: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: The load balancer's IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#address GoogleGkeonpremVmwareCluster#address}
        :param partition: he preexisting partition to be used by the load balancer. T his partition is usually created for the admin cluster for example: 'my-f5-admin-partition'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#partition GoogleGkeonpremVmwareCluster#partition}
        :param snat_pool: The pool name. Only necessary, if using SNAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#snat_pool GoogleGkeonpremVmwareCluster#snat_pool}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10be6a176461f2f0391dc3a1d3b5b5c118693e1b03b82c5e8a03d0c12215907c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#address GoogleGkeonpremVmwareCluster#address}
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partition(self) -> typing.Optional[builtins.str]:
        '''he preexisting partition to be used by the load balancer.

        T
        his partition is usually created for the admin cluster for example:
        'my-f5-admin-partition'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#partition GoogleGkeonpremVmwareCluster#partition}
        '''
        result = self._values.get("partition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snat_pool(self) -> typing.Optional[builtins.str]:
        '''The pool name. Only necessary, if using SNAT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#snat_pool GoogleGkeonpremVmwareCluster#snat_pool}
        '''
        result = self._values.get("snat_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterLoadBalancerF5Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareClusterLoadBalancerF5ConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterLoadBalancerF5ConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73303c038efee5359822aef4a5c2760705e62909732b4844439bd4c65821df4e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78cd1263ab5ea8b461950a2f9e1c950eebb4258bb0333179c9d9204ecfa5a6bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partition")
    def partition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partition"))

    @partition.setter
    def partition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca856830614ae7c0c6c3ceb4fd8ee70dccd96b7a1370d171e9bedcf2464426cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snatPool")
    def snat_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snatPool"))

    @snat_pool.setter
    def snat_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fd401b5f9f097df308a86b2c68ef172322d152f7671f7318173d1687083f9c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snatPool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancerF5Config]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancerF5Config], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancerF5Config],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb7f1d3256913a08d95860fc89cf543c328c19c13bb8f86f37213a10888b6eb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterLoadBalancerManualLbConfig",
    jsii_struct_bases=[],
    name_mapping={
        "control_plane_node_port": "controlPlaneNodePort",
        "ingress_http_node_port": "ingressHttpNodePort",
        "ingress_https_node_port": "ingressHttpsNodePort",
        "konnectivity_server_node_port": "konnectivityServerNodePort",
    },
)
class GoogleGkeonpremVmwareClusterLoadBalancerManualLbConfig:
    def __init__(
        self,
        *,
        control_plane_node_port: typing.Optional[jsii.Number] = None,
        ingress_http_node_port: typing.Optional[jsii.Number] = None,
        ingress_https_node_port: typing.Optional[jsii.Number] = None,
        konnectivity_server_node_port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param control_plane_node_port: NodePort for control plane service. The Kubernetes API server in the admin cluster is implemented as a Service of type NodePort (ex. 30968). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#control_plane_node_port GoogleGkeonpremVmwareCluster#control_plane_node_port}
        :param ingress_http_node_port: NodePort for ingress service's http. The ingress service in the admin cluster is implemented as a Service of type NodePort (ex. 32527). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ingress_http_node_port GoogleGkeonpremVmwareCluster#ingress_http_node_port}
        :param ingress_https_node_port: NodePort for ingress service's https. The ingress service in the admin cluster is implemented as a Service of type NodePort (ex. 30139). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ingress_https_node_port GoogleGkeonpremVmwareCluster#ingress_https_node_port}
        :param konnectivity_server_node_port: NodePort for konnectivity server service running as a sidecar in each kube-apiserver pod (ex. 30564). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#konnectivity_server_node_port GoogleGkeonpremVmwareCluster#konnectivity_server_node_port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ce291fe00e367da84f97756699d2e1392e89a206a14c29efcf38bb1571a5e00)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#control_plane_node_port GoogleGkeonpremVmwareCluster#control_plane_node_port}
        '''
        result = self._values.get("control_plane_node_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ingress_http_node_port(self) -> typing.Optional[jsii.Number]:
        '''NodePort for ingress service's http.

        The ingress service in the admin
        cluster is implemented as a Service of type NodePort (ex. 32527).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ingress_http_node_port GoogleGkeonpremVmwareCluster#ingress_http_node_port}
        '''
        result = self._values.get("ingress_http_node_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ingress_https_node_port(self) -> typing.Optional[jsii.Number]:
        '''NodePort for ingress service's https.

        The ingress service in the admin
        cluster is implemented as a Service of type NodePort (ex. 30139).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ingress_https_node_port GoogleGkeonpremVmwareCluster#ingress_https_node_port}
        '''
        result = self._values.get("ingress_https_node_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def konnectivity_server_node_port(self) -> typing.Optional[jsii.Number]:
        '''NodePort for konnectivity server service running as a sidecar in each kube-apiserver pod (ex. 30564).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#konnectivity_server_node_port GoogleGkeonpremVmwareCluster#konnectivity_server_node_port}
        '''
        result = self._values.get("konnectivity_server_node_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterLoadBalancerManualLbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareClusterLoadBalancerManualLbConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterLoadBalancerManualLbConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3969c935bb0b0dcc734393e3bbb0fd32cd4a3d1516d51fa68e6fa8c223d472c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d07ca9e960edb72e35f06d2abea210d73e44ceee203af5948b1279514d0e5ae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneNodePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingressHttpNodePort")
    def ingress_http_node_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ingressHttpNodePort"))

    @ingress_http_node_port.setter
    def ingress_http_node_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16dddc70641c55866203a6b52b184e5763c3e132fa760139dd9e601e1184ecf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingressHttpNodePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingressHttpsNodePort")
    def ingress_https_node_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ingressHttpsNodePort"))

    @ingress_https_node_port.setter
    def ingress_https_node_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1451ccc50d4581260e09848da8a209cbb51d891687a793e1795066f5c6517fb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingressHttpsNodePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="konnectivityServerNodePort")
    def konnectivity_server_node_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "konnectivityServerNodePort"))

    @konnectivity_server_node_port.setter
    def konnectivity_server_node_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79e2c387271616749f55a4c7bf7de8517c9a85531aa105f8f52b257f1fa17f30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "konnectivityServerNodePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancerManualLbConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancerManualLbConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancerManualLbConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92df6417573a4b99f9db6874494fae9dad3126d42ddbb2939a1ac634ea5d425f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfig",
    jsii_struct_bases=[],
    name_mapping={"address_pools": "addressPools"},
)
class GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfig:
    def __init__(
        self,
        *,
        address_pools: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param address_pools: address_pools block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#address_pools GoogleGkeonpremVmwareCluster#address_pools}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6edf57cf692898156095ffca422157dc946e91416c268903811317c474de8816)
            check_type(argname="argument address_pools", value=address_pools, expected_type=type_hints["address_pools"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address_pools": address_pools,
        }

    @builtins.property
    def address_pools(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools"]]:
        '''address_pools block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#address_pools GoogleGkeonpremVmwareCluster#address_pools}
        '''
        result = self._values.get("address_pools")
        assert result is not None, "Required property 'address_pools' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools",
    jsii_struct_bases=[],
    name_mapping={
        "addresses": "addresses",
        "pool": "pool",
        "avoid_buggy_ips": "avoidBuggyIps",
        "manual_assign": "manualAssign",
    },
)
class GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools:
    def __init__(
        self,
        *,
        addresses: typing.Sequence[builtins.str],
        pool: builtins.str,
        avoid_buggy_ips: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        manual_assign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param addresses: The addresses that are part of this pool. Each address must be either in the CIDR form (1.2.3.0/24) or range form (1.2.3.1-1.2.3.5). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#addresses GoogleGkeonpremVmwareCluster#addresses}
        :param pool: The name of the address pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#pool GoogleGkeonpremVmwareCluster#pool}
        :param avoid_buggy_ips: If true, avoid using IPs ending in .0 or .255. This avoids buggy consumer devices mistakenly dropping IPv4 traffic for those special IP addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#avoid_buggy_ips GoogleGkeonpremVmwareCluster#avoid_buggy_ips}
        :param manual_assign: If true, prevent IP addresses from being automatically assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#manual_assign GoogleGkeonpremVmwareCluster#manual_assign}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ca63a22af008a19ab656a26434ed97ae38e097806a099b6905d3fcbd8d6a40d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#addresses GoogleGkeonpremVmwareCluster#addresses}
        '''
        result = self._values.get("addresses")
        assert result is not None, "Required property 'addresses' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def pool(self) -> builtins.str:
        '''The name of the address pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#pool GoogleGkeonpremVmwareCluster#pool}
        '''
        result = self._values.get("pool")
        assert result is not None, "Required property 'pool' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def avoid_buggy_ips(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, avoid using IPs ending in .0 or .255. This avoids buggy consumer devices mistakenly dropping IPv4 traffic for those special IP addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#avoid_buggy_ips GoogleGkeonpremVmwareCluster#avoid_buggy_ips}
        '''
        result = self._values.get("avoid_buggy_ips")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def manual_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, prevent IP addresses from being automatically assigned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#manual_assign GoogleGkeonpremVmwareCluster#manual_assign}
        '''
        result = self._values.get("manual_assign")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPoolsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPoolsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d7e7f2ad98b471dee77880d0108433acb4603a792beae3f4f6f054c2d09ba6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPoolsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1376977cd093b00e65b4bcf629d283b538d6e406a6077507fd5afd40afc99817)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPoolsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bf858083c4e3b49b58fe8ac453b98c9197c81daea7b9c2cb2f389ecaa5b472c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af7a72ba51e12ead4c0831f6b92d558ee5e950a49f0d472e106e9f6a1f27709a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e8674efbe36627afeb2dd8b0af0a156441eea77249a1159155d3b43e39323cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f868ca42f25c5c1452cada3c788a167ddeba1ce541dbe7a1203ba72de0eab229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPoolsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPoolsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35b7472e40e8c6344e767e8849b86fa34a84c1c5ae7fb08de7f5a7b99130db8a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5b2f4fdb4e165fa1637af36e165eb12fb2129f6486afc87eb7d60a588408bfa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__733836881dcf1b473d89893c852953b23731c04a6ceff134b9923cf2b5a60b07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8553b6eb9d9997cf741e0c1e2eb4372b0f20867d4ea1095d664f0fc79d7b835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manualAssign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pool")
    def pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pool"))

    @pool.setter
    def pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b1b461264f60ac9e3695aaa046d2316180360a807b08f1dbb1e344e796186a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bf2707a6788bba203bef7d21e6d9b3616024a35899df27a3d052623f5149ced)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea928cd24fe48fcf4ffef92388fa8b091cd733fa850812d4942604e108f7154b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAddressPools")
    def put_address_pools(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8820d3f92f72457da78afa572285a63473f51e4e43278638d81029b55a78104d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAddressPools", [value]))

    @builtins.property
    @jsii.member(jsii_name="addressPools")
    def address_pools(
        self,
    ) -> GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPoolsList:
        return typing.cast(GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPoolsList, jsii.get(self, "addressPools"))

    @builtins.property
    @jsii.member(jsii_name="addressPoolsInput")
    def address_pools_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools]]], jsii.get(self, "addressPoolsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a11b43a16951dd69a655a3adf3338ee03bda8c8ae77173724c6e5a7a3a03042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareClusterLoadBalancerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterLoadBalancerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5418edbd0a82f2754d584ce05b18bd7617e6be0570b07f25fee2318308ffbac)
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
        :param address: The load balancer's IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#address GoogleGkeonpremVmwareCluster#address}
        :param partition: he preexisting partition to be used by the load balancer. T his partition is usually created for the admin cluster for example: 'my-f5-admin-partition'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#partition GoogleGkeonpremVmwareCluster#partition}
        :param snat_pool: The pool name. Only necessary, if using SNAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#snat_pool GoogleGkeonpremVmwareCluster#snat_pool}
        '''
        value = GoogleGkeonpremVmwareClusterLoadBalancerF5Config(
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
        :param control_plane_node_port: NodePort for control plane service. The Kubernetes API server in the admin cluster is implemented as a Service of type NodePort (ex. 30968). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#control_plane_node_port GoogleGkeonpremVmwareCluster#control_plane_node_port}
        :param ingress_http_node_port: NodePort for ingress service's http. The ingress service in the admin cluster is implemented as a Service of type NodePort (ex. 32527). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ingress_http_node_port GoogleGkeonpremVmwareCluster#ingress_http_node_port}
        :param ingress_https_node_port: NodePort for ingress service's https. The ingress service in the admin cluster is implemented as a Service of type NodePort (ex. 30139). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ingress_https_node_port GoogleGkeonpremVmwareCluster#ingress_https_node_port}
        :param konnectivity_server_node_port: NodePort for konnectivity server service running as a sidecar in each kube-apiserver pod (ex. 30564). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#konnectivity_server_node_port GoogleGkeonpremVmwareCluster#konnectivity_server_node_port}
        '''
        value = GoogleGkeonpremVmwareClusterLoadBalancerManualLbConfig(
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
        address_pools: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param address_pools: address_pools block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#address_pools GoogleGkeonpremVmwareCluster#address_pools}
        '''
        value = GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfig(
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
        :param control_plane_vip: The VIP which you previously set aside for the Kubernetes API of this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#control_plane_vip GoogleGkeonpremVmwareCluster#control_plane_vip}
        :param ingress_vip: The VIP which you previously set aside for ingress traffic into this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ingress_vip GoogleGkeonpremVmwareCluster#ingress_vip}
        '''
        value = GoogleGkeonpremVmwareClusterLoadBalancerVipConfig(
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
    def f5_config(
        self,
    ) -> GoogleGkeonpremVmwareClusterLoadBalancerF5ConfigOutputReference:
        return typing.cast(GoogleGkeonpremVmwareClusterLoadBalancerF5ConfigOutputReference, jsii.get(self, "f5Config"))

    @builtins.property
    @jsii.member(jsii_name="manualLbConfig")
    def manual_lb_config(
        self,
    ) -> GoogleGkeonpremVmwareClusterLoadBalancerManualLbConfigOutputReference:
        return typing.cast(GoogleGkeonpremVmwareClusterLoadBalancerManualLbConfigOutputReference, jsii.get(self, "manualLbConfig"))

    @builtins.property
    @jsii.member(jsii_name="metalLbConfig")
    def metal_lb_config(
        self,
    ) -> GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigOutputReference:
        return typing.cast(GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigOutputReference, jsii.get(self, "metalLbConfig"))

    @builtins.property
    @jsii.member(jsii_name="vipConfig")
    def vip_config(
        self,
    ) -> "GoogleGkeonpremVmwareClusterLoadBalancerVipConfigOutputReference":
        return typing.cast("GoogleGkeonpremVmwareClusterLoadBalancerVipConfigOutputReference", jsii.get(self, "vipConfig"))

    @builtins.property
    @jsii.member(jsii_name="f5ConfigInput")
    def f5_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancerF5Config]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancerF5Config], jsii.get(self, "f5ConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="manualLbConfigInput")
    def manual_lb_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancerManualLbConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancerManualLbConfig], jsii.get(self, "manualLbConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="metalLbConfigInput")
    def metal_lb_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfig], jsii.get(self, "metalLbConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="vipConfigInput")
    def vip_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterLoadBalancerVipConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterLoadBalancerVipConfig"], jsii.get(self, "vipConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancer]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90aeca80d667877fd9b10b0f9d2a3fa4acaaa35f3a068ac2ccb59783b5aad333)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterLoadBalancerVipConfig",
    jsii_struct_bases=[],
    name_mapping={"control_plane_vip": "controlPlaneVip", "ingress_vip": "ingressVip"},
)
class GoogleGkeonpremVmwareClusterLoadBalancerVipConfig:
    def __init__(
        self,
        *,
        control_plane_vip: typing.Optional[builtins.str] = None,
        ingress_vip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param control_plane_vip: The VIP which you previously set aside for the Kubernetes API of this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#control_plane_vip GoogleGkeonpremVmwareCluster#control_plane_vip}
        :param ingress_vip: The VIP which you previously set aside for ingress traffic into this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ingress_vip GoogleGkeonpremVmwareCluster#ingress_vip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d87e5654868920641cf07630c86a523471dd3a93fff305a70ef82c74078e34b3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#control_plane_vip GoogleGkeonpremVmwareCluster#control_plane_vip}
        '''
        result = self._values.get("control_plane_vip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ingress_vip(self) -> typing.Optional[builtins.str]:
        '''The VIP which you previously set aside for ingress traffic into this cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ingress_vip GoogleGkeonpremVmwareCluster#ingress_vip}
        '''
        result = self._values.get("ingress_vip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterLoadBalancerVipConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareClusterLoadBalancerVipConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterLoadBalancerVipConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c7cd613754362941fb3161a520fd412f01323f6aa13020c1fc4b168b70e6c18)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2df02d7f3096327aea79e8e1d7df01c44f9edeb5f31003dbc21ddbdc3a531d20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneVip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingressVip")
    def ingress_vip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ingressVip"))

    @ingress_vip.setter
    def ingress_vip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54c6332a5e9986db945e9c9b9d5336713336a0d859a4932b6810baac2cf2a76d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingressVip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancerVipConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancerVipConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancerVipConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fede1828d790961f9ad219e3ab5c701886d767c722c5ccb80e07623454b484e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterNetworkConfig",
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
class GoogleGkeonpremVmwareClusterNetworkConfig:
    def __init__(
        self,
        *,
        pod_address_cidr_blocks: typing.Sequence[builtins.str],
        service_address_cidr_blocks: typing.Sequence[builtins.str],
        control_plane_v2_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2Config", typing.Dict[builtins.str, typing.Any]]] = None,
        dhcp_ip_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterNetworkConfigDhcpIpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        host_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterNetworkConfigHostConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        static_ip_config: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        vcenter_network: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pod_address_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#pod_address_cidr_blocks GoogleGkeonpremVmwareCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported.. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#service_address_cidr_blocks GoogleGkeonpremVmwareCluster#service_address_cidr_blocks}
        :param control_plane_v2_config: control_plane_v2_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#control_plane_v2_config GoogleGkeonpremVmwareCluster#control_plane_v2_config}
        :param dhcp_ip_config: dhcp_ip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#dhcp_ip_config GoogleGkeonpremVmwareCluster#dhcp_ip_config}
        :param host_config: host_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#host_config GoogleGkeonpremVmwareCluster#host_config}
        :param static_ip_config: static_ip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#static_ip_config GoogleGkeonpremVmwareCluster#static_ip_config}
        :param vcenter_network: vcenter_network specifies vCenter network name. Inherited from the admin cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#vcenter_network GoogleGkeonpremVmwareCluster#vcenter_network}
        '''
        if isinstance(control_plane_v2_config, dict):
            control_plane_v2_config = GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2Config(**control_plane_v2_config)
        if isinstance(dhcp_ip_config, dict):
            dhcp_ip_config = GoogleGkeonpremVmwareClusterNetworkConfigDhcpIpConfig(**dhcp_ip_config)
        if isinstance(host_config, dict):
            host_config = GoogleGkeonpremVmwareClusterNetworkConfigHostConfig(**host_config)
        if isinstance(static_ip_config, dict):
            static_ip_config = GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfig(**static_ip_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53f8ef60f9fc7111722b79f0d1d5ff26c075cd2e8e6bd17d12c2e4e95067b0f2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#pod_address_cidr_blocks GoogleGkeonpremVmwareCluster#pod_address_cidr_blocks}
        '''
        result = self._values.get("pod_address_cidr_blocks")
        assert result is not None, "Required property 'pod_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        '''All services in the cluster are assigned an RFC1918 IPv4 address from these ranges.

        Only a single range is supported.. This field
        cannot be changed after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#service_address_cidr_blocks GoogleGkeonpremVmwareCluster#service_address_cidr_blocks}
        '''
        result = self._values.get("service_address_cidr_blocks")
        assert result is not None, "Required property 'service_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def control_plane_v2_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2Config"]:
        '''control_plane_v2_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#control_plane_v2_config GoogleGkeonpremVmwareCluster#control_plane_v2_config}
        '''
        result = self._values.get("control_plane_v2_config")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2Config"], result)

    @builtins.property
    def dhcp_ip_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterNetworkConfigDhcpIpConfig"]:
        '''dhcp_ip_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#dhcp_ip_config GoogleGkeonpremVmwareCluster#dhcp_ip_config}
        '''
        result = self._values.get("dhcp_ip_config")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterNetworkConfigDhcpIpConfig"], result)

    @builtins.property
    def host_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterNetworkConfigHostConfig"]:
        '''host_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#host_config GoogleGkeonpremVmwareCluster#host_config}
        '''
        result = self._values.get("host_config")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterNetworkConfigHostConfig"], result)

    @builtins.property
    def static_ip_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfig"]:
        '''static_ip_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#static_ip_config GoogleGkeonpremVmwareCluster#static_ip_config}
        '''
        result = self._values.get("static_ip_config")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfig"], result)

    @builtins.property
    def vcenter_network(self) -> typing.Optional[builtins.str]:
        '''vcenter_network specifies vCenter network name. Inherited from the admin cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#vcenter_network GoogleGkeonpremVmwareCluster#vcenter_network}
        '''
        result = self._values.get("vcenter_network")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2Config",
    jsii_struct_bases=[],
    name_mapping={"control_plane_ip_block": "controlPlaneIpBlock"},
)
class GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2Config:
    def __init__(
        self,
        *,
        control_plane_ip_block: typing.Optional[typing.Union["GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param control_plane_ip_block: control_plane_ip_block block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#control_plane_ip_block GoogleGkeonpremVmwareCluster#control_plane_ip_block}
        '''
        if isinstance(control_plane_ip_block, dict):
            control_plane_ip_block = GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock(**control_plane_ip_block)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c65ff656002100dd1140b06bbe397d5c7fdc18c2e6d17cb80e24cc8c3241bec)
            check_type(argname="argument control_plane_ip_block", value=control_plane_ip_block, expected_type=type_hints["control_plane_ip_block"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if control_plane_ip_block is not None:
            self._values["control_plane_ip_block"] = control_plane_ip_block

    @builtins.property
    def control_plane_ip_block(
        self,
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock"]:
        '''control_plane_ip_block block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#control_plane_ip_block GoogleGkeonpremVmwareCluster#control_plane_ip_block}
        '''
        result = self._values.get("control_plane_ip_block")
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock",
    jsii_struct_bases=[],
    name_mapping={"gateway": "gateway", "ips": "ips", "netmask": "netmask"},
)
class GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock:
    def __init__(
        self,
        *,
        gateway: typing.Optional[builtins.str] = None,
        ips: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps", typing.Dict[builtins.str, typing.Any]]]]] = None,
        netmask: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gateway: The network gateway used by the VMware User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#gateway GoogleGkeonpremVmwareCluster#gateway}
        :param ips: ips block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ips GoogleGkeonpremVmwareCluster#ips}
        :param netmask: The netmask used by the VMware User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#netmask GoogleGkeonpremVmwareCluster#netmask}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80ea7af5191352e0dde19d42b67807baf921b7a5c03da9900a76f5eed8ba3d62)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#gateway GoogleGkeonpremVmwareCluster#gateway}
        '''
        result = self._values.get("gateway")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ips(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps"]]]:
        '''ips block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ips GoogleGkeonpremVmwareCluster#ips}
        '''
        result = self._values.get("ips")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps"]]], result)

    @builtins.property
    def netmask(self) -> typing.Optional[builtins.str]:
        '''The netmask used by the VMware User Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#netmask GoogleGkeonpremVmwareCluster#netmask}
        '''
        result = self._values.get("netmask")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps",
    jsii_struct_bases=[],
    name_mapping={"hostname": "hostname", "ip": "ip"},
)
class GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps:
    def __init__(
        self,
        *,
        hostname: typing.Optional[builtins.str] = None,
        ip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hostname: Hostname of the machine. VM's name will be used if this field is empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#hostname GoogleGkeonpremVmwareCluster#hostname}
        :param ip: IP could be an IP address (like 1.2.3.4) or a CIDR (like 1.2.3.0/24). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ip GoogleGkeonpremVmwareCluster#ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1015b168e5478deacb989015cabff975287f3be1f6105b975b9314464afe403c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#hostname GoogleGkeonpremVmwareCluster#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip(self) -> typing.Optional[builtins.str]:
        '''IP could be an IP address (like 1.2.3.4) or a CIDR (like 1.2.3.0/24).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ip GoogleGkeonpremVmwareCluster#ip}
        '''
        result = self._values.get("ip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIpsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIpsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5aaef58c8e331197e6ad6215fd82a25f2f108c16b872fd1aeca69bc4202d6621)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIpsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6de99d04406cc71c43bdc0abc3780485ae4a09cafa316b5ccad1776727b94b1c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIpsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__080f479d2506c91007ccee2ff547de9ed5dc014f449cf98f785e2aff5c57f6f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1a42c54fcf8547a370ed465c5e0c5613219ef624ab0b6e0d9fac2ac8f9eba05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__602b27c63bfbd4476d823a907916f71ef130794dcd9b58dd4ebefa791930291d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__918df7e831b0910c2c5b519a4365a4dd3edc5fc9562a64a3571cb36287ca58c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIpsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIpsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11e1059ffc39cb2859b29810b35952a4a87130a13402a0d79233029090d40ca4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__600723251edf2da1348249208c610c906cd01bf9c0a0f290c7044ba950c9aa0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61fdecd881875adcd3051a963af4dd54f9637caa0ac937fab1039af84a9232d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__158faceb5e4494bdb7f519a5e2c5dae238635480cd6164991c2a100c641cf54e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7a01c57de90b1e9cc7eab038089134641d5f71fa5f62cf01c5205ffd347d280)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIps")
    def put_ips(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a305944cfdc88e1c0c42f2f561fbd9e19b8d407f22588207b95424cd87df6887)
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
    ) -> GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIpsList:
        return typing.cast(GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIpsList, jsii.get(self, "ips"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="ipsInput")
    def ips_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps]]], jsii.get(self, "ipsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__20f3cc6cf4a747bda70c985f42778fa4c4bd3cfcd8a7faf845c59c64ffe88007)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateway", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netmask")
    def netmask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netmask"))

    @netmask.setter
    def netmask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52a9d65727736a263d1c8df7df7caa9331d624d90431a03b89e602628b3219d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netmask", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e81d18ef23bb8fbac9eb2e2ee77dbe187928ca60e64b5a0cc5b4b492bb96d145)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd5a9588931cbe0386b87ce00017b3d338de4d91fbf73f84d3270713afb96c78)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putControlPlaneIpBlock")
    def put_control_plane_ip_block(
        self,
        *,
        gateway: typing.Optional[builtins.str] = None,
        ips: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps, typing.Dict[builtins.str, typing.Any]]]]] = None,
        netmask: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gateway: The network gateway used by the VMware User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#gateway GoogleGkeonpremVmwareCluster#gateway}
        :param ips: ips block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ips GoogleGkeonpremVmwareCluster#ips}
        :param netmask: The netmask used by the VMware User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#netmask GoogleGkeonpremVmwareCluster#netmask}
        '''
        value = GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock(
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
    ) -> GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockOutputReference:
        return typing.cast(GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockOutputReference, jsii.get(self, "controlPlaneIpBlock"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneIpBlockInput")
    def control_plane_ip_block_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock], jsii.get(self, "controlPlaneIpBlockInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2Config]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2Config], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2Config],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e438e29726cdc15d38dd11df1e06266220df182cf881e4df3e2d8cc5ff8197b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterNetworkConfigDhcpIpConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleGkeonpremVmwareClusterNetworkConfigDhcpIpConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: enabled is a flag to mark if DHCP IP allocation is used for VMware user clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#enabled GoogleGkeonpremVmwareCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3514f6decd7a2f540b06d79048f1b2442485a1858514cc0c04026e1cdaa5649c)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''enabled is a flag to mark if DHCP IP allocation is used for VMware user clusters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#enabled GoogleGkeonpremVmwareCluster#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterNetworkConfigDhcpIpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareClusterNetworkConfigDhcpIpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterNetworkConfigDhcpIpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37f53425eb73ed28dab20cee3e9b0a437ec361ac452f50a7a7efb007405cd898)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3ce6edc5e56a223c84b868cb3c66eb77c5e380489216a4eae1ac2acf19cbe19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigDhcpIpConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigDhcpIpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigDhcpIpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48a7ee33e684fe8c6b6d311d1a433d3b75ceac48148a8a074437beaffaa86250)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterNetworkConfigHostConfig",
    jsii_struct_bases=[],
    name_mapping={
        "dns_search_domains": "dnsSearchDomains",
        "dns_servers": "dnsServers",
        "ntp_servers": "ntpServers",
    },
)
class GoogleGkeonpremVmwareClusterNetworkConfigHostConfig:
    def __init__(
        self,
        *,
        dns_search_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        ntp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param dns_search_domains: DNS search domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#dns_search_domains GoogleGkeonpremVmwareCluster#dns_search_domains}
        :param dns_servers: DNS servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#dns_servers GoogleGkeonpremVmwareCluster#dns_servers}
        :param ntp_servers: NTP servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ntp_servers GoogleGkeonpremVmwareCluster#ntp_servers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1162ceedda499b68e65cf7e2c3447d56b65daead7766c91c15f7be0e2f1764bd)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#dns_search_domains GoogleGkeonpremVmwareCluster#dns_search_domains}
        '''
        result = self._values.get("dns_search_domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dns_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''DNS servers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#dns_servers GoogleGkeonpremVmwareCluster#dns_servers}
        '''
        result = self._values.get("dns_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ntp_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''NTP servers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ntp_servers GoogleGkeonpremVmwareCluster#ntp_servers}
        '''
        result = self._values.get("ntp_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterNetworkConfigHostConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareClusterNetworkConfigHostConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterNetworkConfigHostConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a058d14093f4cf2201c6c62444df6aa6ccbb50e5e9df54d866aa5d102bd4765)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a55db63472496c58a6fc5de2281af73116937306d3f397cf46518613273a96e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsSearchDomains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsServers")
    def dns_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dnsServers"))

    @dns_servers.setter
    def dns_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa03245f88ab951e23e7828c63e15524ad6c3e0eb46e26f027e509e3764831bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ntpServers")
    def ntp_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ntpServers"))

    @ntp_servers.setter
    def ntp_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f372ce7589176a9780386653fcd6ad3b4ef475e0435313601ef3ab5b3f00ca36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ntpServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigHostConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigHostConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigHostConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64727fd88964b2f3737fb9bbc524cec563c1874a894449d9a15d6bb1ac15c45a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareClusterNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__281aebe6e7582b8f7eb6d142ac2a924a665d8684bb29c2be12be499c8e1ed52b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putControlPlaneV2Config")
    def put_control_plane_v2_config(
        self,
        *,
        control_plane_ip_block: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param control_plane_ip_block: control_plane_ip_block block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#control_plane_ip_block GoogleGkeonpremVmwareCluster#control_plane_ip_block}
        '''
        value = GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2Config(
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
        :param enabled: enabled is a flag to mark if DHCP IP allocation is used for VMware user clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#enabled GoogleGkeonpremVmwareCluster#enabled}
        '''
        value = GoogleGkeonpremVmwareClusterNetworkConfigDhcpIpConfig(enabled=enabled)

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
        :param dns_search_domains: DNS search domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#dns_search_domains GoogleGkeonpremVmwareCluster#dns_search_domains}
        :param dns_servers: DNS servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#dns_servers GoogleGkeonpremVmwareCluster#dns_servers}
        :param ntp_servers: NTP servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ntp_servers GoogleGkeonpremVmwareCluster#ntp_servers}
        '''
        value = GoogleGkeonpremVmwareClusterNetworkConfigHostConfig(
            dns_search_domains=dns_search_domains,
            dns_servers=dns_servers,
            ntp_servers=ntp_servers,
        )

        return typing.cast(None, jsii.invoke(self, "putHostConfig", [value]))

    @jsii.member(jsii_name="putStaticIpConfig")
    def put_static_ip_config(
        self,
        *,
        ip_blocks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param ip_blocks: ip_blocks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ip_blocks GoogleGkeonpremVmwareCluster#ip_blocks}
        '''
        value = GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfig(
            ip_blocks=ip_blocks
        )

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
    ) -> GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigOutputReference:
        return typing.cast(GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigOutputReference, jsii.get(self, "controlPlaneV2Config"))

    @builtins.property
    @jsii.member(jsii_name="dhcpIpConfig")
    def dhcp_ip_config(
        self,
    ) -> GoogleGkeonpremVmwareClusterNetworkConfigDhcpIpConfigOutputReference:
        return typing.cast(GoogleGkeonpremVmwareClusterNetworkConfigDhcpIpConfigOutputReference, jsii.get(self, "dhcpIpConfig"))

    @builtins.property
    @jsii.member(jsii_name="hostConfig")
    def host_config(
        self,
    ) -> GoogleGkeonpremVmwareClusterNetworkConfigHostConfigOutputReference:
        return typing.cast(GoogleGkeonpremVmwareClusterNetworkConfigHostConfigOutputReference, jsii.get(self, "hostConfig"))

    @builtins.property
    @jsii.member(jsii_name="staticIpConfig")
    def static_ip_config(
        self,
    ) -> "GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigOutputReference":
        return typing.cast("GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigOutputReference", jsii.get(self, "staticIpConfig"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneV2ConfigInput")
    def control_plane_v2_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2Config]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2Config], jsii.get(self, "controlPlaneV2ConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="dhcpIpConfigInput")
    def dhcp_ip_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigDhcpIpConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigDhcpIpConfig], jsii.get(self, "dhcpIpConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="hostConfigInput")
    def host_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigHostConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigHostConfig], jsii.get(self, "hostConfigInput"))

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
    ) -> typing.Optional["GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfig"], jsii.get(self, "staticIpConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__eb7354f0589de06e47f62ec219e913c35515addf6b6a0717590986d3eaa13d87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAddressCidrBlocks")
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceAddressCidrBlocks"))

    @service_address_cidr_blocks.setter
    def service_address_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0dcf34facebd9e112603b643775ac3c0da48f5b7bcbf6e8908f118d70655d0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vcenterNetwork")
    def vcenter_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vcenterNetwork"))

    @vcenter_network.setter
    def vcenter_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e43e3aa1f0bb9b750091fa6b3e2eaadc1e9d43d8418cfac7f860c7d76b84f2c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vcenterNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27b5546e2db7ad56d096508d33096eb46d83cc86bc64d4b1e418fafcfab9ac2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfig",
    jsii_struct_bases=[],
    name_mapping={"ip_blocks": "ipBlocks"},
)
class GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfig:
    def __init__(
        self,
        *,
        ip_blocks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param ip_blocks: ip_blocks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ip_blocks GoogleGkeonpremVmwareCluster#ip_blocks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d4998090ec82491e59685f357c7b0c26e3c419d6ce4a9f7a3eb60e848face93)
            check_type(argname="argument ip_blocks", value=ip_blocks, expected_type=type_hints["ip_blocks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip_blocks": ip_blocks,
        }

    @builtins.property
    def ip_blocks(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks"]]:
        '''ip_blocks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ip_blocks GoogleGkeonpremVmwareCluster#ip_blocks}
        '''
        result = self._values.get("ip_blocks")
        assert result is not None, "Required property 'ip_blocks' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks",
    jsii_struct_bases=[],
    name_mapping={"gateway": "gateway", "ips": "ips", "netmask": "netmask"},
)
class GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks:
    def __init__(
        self,
        *,
        gateway: builtins.str,
        ips: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps", typing.Dict[builtins.str, typing.Any]]]],
        netmask: builtins.str,
    ) -> None:
        '''
        :param gateway: The network gateway used by the VMware User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#gateway GoogleGkeonpremVmwareCluster#gateway}
        :param ips: ips block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ips GoogleGkeonpremVmwareCluster#ips}
        :param netmask: The netmask used by the VMware User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#netmask GoogleGkeonpremVmwareCluster#netmask}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7c731d42484fdb7b04a0cea6bc6d796139de73afb9d671cdad8a57ea3b3ad5f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#gateway GoogleGkeonpremVmwareCluster#gateway}
        '''
        result = self._values.get("gateway")
        assert result is not None, "Required property 'gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ips(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps"]]:
        '''ips block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ips GoogleGkeonpremVmwareCluster#ips}
        '''
        result = self._values.get("ips")
        assert result is not None, "Required property 'ips' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps"]], result)

    @builtins.property
    def netmask(self) -> builtins.str:
        '''The netmask used by the VMware User Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#netmask GoogleGkeonpremVmwareCluster#netmask}
        '''
        result = self._values.get("netmask")
        assert result is not None, "Required property 'netmask' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps",
    jsii_struct_bases=[],
    name_mapping={"ip": "ip", "hostname": "hostname"},
)
class GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps:
    def __init__(
        self,
        *,
        ip: builtins.str,
        hostname: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip: IP could be an IP address (like 1.2.3.4) or a CIDR (like 1.2.3.0/24). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ip GoogleGkeonpremVmwareCluster#ip}
        :param hostname: Hostname of the machine. VM's name will be used if this field is empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#hostname GoogleGkeonpremVmwareCluster#hostname}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41b7e1f2ab793471d7fc9efc9cb794cada6b00a64960931aea883d38f26277f3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ip GoogleGkeonpremVmwareCluster#ip}
        '''
        result = self._values.get("ip")
        assert result is not None, "Required property 'ip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''Hostname of the machine. VM's name will be used if this field is empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#hostname GoogleGkeonpremVmwareCluster#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIpsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIpsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30e90e9fc4efc302ba5e6e8ae67ce03249f7eb37eaae534ef9d5d5a93cab5b36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIpsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81455b0dd03c3975e85699b7754bce3dbf182b09f394406f44f4fe9576ee126d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIpsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed973a07d1a05840669f1524c356ffb342cdf401d7729b73c27e889c0083abf5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd7eb4e8a18b20f6d33d53f302dc5ae8a92b94daff3ad27428392ed3f3c0eec8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3927d27446377721aea7fe88945e59c08500349bb6487b6b6583b8e0bfb4ffcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d755966acd25e68c062394c26fcb08af1fe2b655573e8aeef7ca390c4ec9dc09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIpsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIpsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c0fca9359b2b62666fe2306fd925bf24fe98ccb8cc73410a1c680bdd9d67145)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e907ca914d00484425cd438fe2105f3e329341574c24506336998dc22a02bdf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea406737e9f1a68f31bca4d5254e9ad4c6ca8a657bd70056eca616f781ce1222)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__350346522ed66bf7169b5c817de9cc7fcf9df01d816c0f6584c1b064de76ba76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93835245c5c73db342be4b46cc4f4694243e59e2158e614606e19f869c7eb0a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53cef29495a1efeb7ce8085e53505352c92dd8937e9daa75b654b38c7780bdc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c6c2ec16db61c7ed66baa334d7426e29165b0ac06331de8dbcee60386c94f55)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61f30fe922844f84f5a0b42a44afc67f2c49436888499ab0a247ce535bded876)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6930d8fa11e523e81ba5333f030acb459a1c87b1ac9f072b967fffd319c5a79b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a899f92e6473a0fff976ce24661fd0362b8bb17462f2f775d9b3f3b927ba66d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d79269a5142eaaf84769108f949a15bd1987273ae9acecb50fcbabc8cc5ee693)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIps")
    def put_ips(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6842e526b2f7466a45060466171992704ac7fd7a8861415532684ffd1f950d89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIps", [value]))

    @builtins.property
    @jsii.member(jsii_name="ips")
    def ips(
        self,
    ) -> GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIpsList:
        return typing.cast(GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIpsList, jsii.get(self, "ips"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="ipsInput")
    def ips_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps]]], jsii.get(self, "ipsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__61c836b1c2d5772fe571349a747d7fa4cdfb0eb9624df7da119fa58040e48d7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateway", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netmask")
    def netmask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netmask"))

    @netmask.setter
    def netmask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d8aa5385d0fe589f381f6c183aa16104ed513900c33118233ff054946e95dd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netmask", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5b677a25612168e50f401a033c362c8c99f7137b3772410574297c86845d000)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__449ceeab16ea6e89775c39e1f716153bc50d0b5119327bf172c42b324fcc216b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIpBlocks")
    def put_ip_blocks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06063f11fc9b5f69facde596e2b4ac6bedfff7b8fac60dd7bdedd87adfb077eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpBlocks", [value]))

    @builtins.property
    @jsii.member(jsii_name="ipBlocks")
    def ip_blocks(
        self,
    ) -> GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksList:
        return typing.cast(GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksList, jsii.get(self, "ipBlocks"))

    @builtins.property
    @jsii.member(jsii_name="ipBlocksInput")
    def ip_blocks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks]]], jsii.get(self, "ipBlocksInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72306d06f144cb471c7ae86cdc627d2167406de5cf96ec6286f4357f7d01086c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremVmwareClusterStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterStatusConditions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremVmwareClusterStatusConditions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterStatusConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareClusterStatusConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterStatusConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a5c726c7bc4c77348458d70afe6e5902efcc84979d10f580bdc946efd57f317)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareClusterStatusConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fdf4073150c8d7f14b7112157fe21dfb93dce34abc53e9870dc761c28e72e61)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareClusterStatusConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a0a8ff004e9dee38f94b8cf9b50beca6657d842bd28fd81282beeeef0358315)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f71a292a2b41fb744b8ea0924e84418aca1d8fff67a3f8e4f79f141f88f08f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__531c42292eef8cb6bad65bf16875e2cc7d4ccb6807287aaf4de787519d665c99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareClusterStatusConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterStatusConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e3a70ccb8d797746360928bf8606896dbaa3d5b59b4008d9cf9bfb53a802850)
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
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterStatusConditions]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterStatusConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterStatusConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f069289a3b406871780049ed85b83b3350d2ad9f380843daf92ca009d2719c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareClusterStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27b2c93e574dc05e2a5e63b72dfcdfb69438b7d1c6ab4ae32df1283dd4ad1c0d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareClusterStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b445a090ad9d205533fd0aab46e1eaf22d98f5610cac9fbfbb761df889e8f0d1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareClusterStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ea34860cd2a8357e5b2456ced404f899a2a82015a59b78d7cc46603de64daf9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbe9c0118c6403704108c123b189eb0c53e3f28c585804434ec49cc15f6ae877)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d08d55a0b108fbf08622931259c25e16d57325a1bcd574183ecd381970233442)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareClusterStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77eedf0f8cee804c195c7702c9d2e5afa03241063c66fe31bbaf6354473bdd1f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> GoogleGkeonpremVmwareClusterStatusConditionsList:
        return typing.cast(GoogleGkeonpremVmwareClusterStatusConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleGkeonpremVmwareClusterStatus]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc67278af24e470c8b439c1e242f62c7baff765a9c6e809792b175a1986b7df9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterStorage",
    jsii_struct_bases=[],
    name_mapping={"vsphere_csi_disabled": "vsphereCsiDisabled"},
)
class GoogleGkeonpremVmwareClusterStorage:
    def __init__(
        self,
        *,
        vsphere_csi_disabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param vsphere_csi_disabled: Whether or not to deploy vSphere CSI components in the VMware User Cluster. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#vsphere_csi_disabled GoogleGkeonpremVmwareCluster#vsphere_csi_disabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00f885203589490a0256456032db8231fb691c749329f06dce1ada70622e7f83)
            check_type(argname="argument vsphere_csi_disabled", value=vsphere_csi_disabled, expected_type=type_hints["vsphere_csi_disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vsphere_csi_disabled": vsphere_csi_disabled,
        }

    @builtins.property
    def vsphere_csi_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether or not to deploy vSphere CSI components in the VMware User Cluster. Enabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#vsphere_csi_disabled GoogleGkeonpremVmwareCluster#vsphere_csi_disabled}
        '''
        result = self._values.get("vsphere_csi_disabled")
        assert result is not None, "Required property 'vsphere_csi_disabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareClusterStorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterStorageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c07d62f920121fbc5ba89c5e696bd3d6a0d62b5010b2743d2040b1e689890ee2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c3eb7d12197fe7119dab4f5cde1bbedc75d0007516a11bd5b5fbbf516ddc87e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vsphereCsiDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleGkeonpremVmwareClusterStorage]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterStorage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterStorage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17e276281554f8d9752a7f2084d6dfccdee428d23be490c613dce3366ba5c56b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleGkeonpremVmwareClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#create GoogleGkeonpremVmwareCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#delete GoogleGkeonpremVmwareCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#update GoogleGkeonpremVmwareCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__412efaac85e14b0f45c9c7c38e706dc0bbe3c45d3e744f264512ce4385b5e3e5)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#create GoogleGkeonpremVmwareCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#delete GoogleGkeonpremVmwareCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#update GoogleGkeonpremVmwareCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0346c3aa315906cb99c56d6ee07eda08fe8d228cd60f36f44ba3f9a7c4a8a81)
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
            type_hints = typing.get_type_hints(_typecheckingstub__25ccb9da87cda1b6e6e20546a74dc76e85f6ab1bb9d1270026068bf08d0a0ca3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4134c5b91030d251d6f67050e14dc8bbdd2b5ebd2b611536b3893261b70bc800)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71308bcd8fc0a69812722d289ac5eafdeaaa0971550b2d9762ec1f219927a999)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5d1db60812e9d1b95e59b20c53da0cd9394940202dd98c1a73fe0e151406076)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterUpgradePolicy",
    jsii_struct_bases=[],
    name_mapping={"control_plane_only": "controlPlaneOnly"},
)
class GoogleGkeonpremVmwareClusterUpgradePolicy:
    def __init__(
        self,
        *,
        control_plane_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param control_plane_only: Controls whether the upgrade applies to the control plane only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#control_plane_only GoogleGkeonpremVmwareCluster#control_plane_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__059abed1b7898d96b76f0a6261c3af62477d90e54daf06082eb3ff318585784f)
            check_type(argname="argument control_plane_only", value=control_plane_only, expected_type=type_hints["control_plane_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if control_plane_only is not None:
            self._values["control_plane_only"] = control_plane_only

    @builtins.property
    def control_plane_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Controls whether the upgrade applies to the control plane only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#control_plane_only GoogleGkeonpremVmwareCluster#control_plane_only}
        '''
        result = self._values.get("control_plane_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterUpgradePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareClusterUpgradePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterUpgradePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d74598ba177c37f096fb940a779f0f38641d80eace6a71ac0fe1885ef1852259)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15778a524e7452bda995d0b323ab4eea7c22e7de92024913f894a38d5547d067)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterUpgradePolicy]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterUpgradePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterUpgradePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2296ade18f1aeaf8e542dfdd0e006e337eb9b51b666641965983fa8adfb8ebc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterValidationCheck",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremVmwareClusterValidationCheck:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterValidationCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareClusterValidationCheckList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterValidationCheckList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f510759e0d3ef9a35c7433148f372eb73c37dfe0b525481a983d77ac654344d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareClusterValidationCheckOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1089f66ff8ebf57d5ad341e608e7e53819dde296593a14ff276ad8692e06180c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareClusterValidationCheckOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b60d26ef34083b2a530f7c8c96f1066c7be6f1719e3bd0ddef70e1ccec6a8f7e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32c61ceea835070c654b098a3a2bc377e761c10f759b0a1001b4a13854207538)
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
            type_hints = typing.get_type_hints(_typecheckingstub__27a1e2b6d1d903ec0f7ec155dbbaca66da5631824f623aaf0c8c552d7a923370)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareClusterValidationCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterValidationCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3538babf7fc0dacb0ab6012a9e4d268a50aa6c1cff9272cae3595c15951ab8a)
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
    def status(self) -> "GoogleGkeonpremVmwareClusterValidationCheckStatusList":
        return typing.cast("GoogleGkeonpremVmwareClusterValidationCheckStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterValidationCheck]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterValidationCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterValidationCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b8c1381915104612b9c45e8887122ad441b716b6a035d87d790634b888cd30d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterValidationCheckStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremVmwareClusterValidationCheckStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterValidationCheckStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareClusterValidationCheckStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterValidationCheckStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da2b870c0f761c5d4d779919cef71d69b72b3c7b2729a5d2e90da54c101e583b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareClusterValidationCheckStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6343f62639ac7e1d3587bb7835e7a49d2fa74992a542f12552aaeaf0d3aca56)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareClusterValidationCheckStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa8997dd7793eaa71c3d5ca2bf2ac6deea4371dad2a5a881b71f5f891148aeae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0880bf4efc1dcfd7fd52107a8d4e1d16c7f4e448586992d5de2cca3d4ec8ab19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5631595246e3800c3f86a45dd0ead256b421fde91e90aa28cc11f4bb3323c323)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareClusterValidationCheckStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterValidationCheckStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb840f0316f362bf2fc7b192569d5e27b7620e21fe9eb1edfae35c23e9c71136)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="result")
    def result(self) -> "GoogleGkeonpremVmwareClusterValidationCheckStatusResultList":
        return typing.cast("GoogleGkeonpremVmwareClusterValidationCheckStatusResultList", jsii.get(self, "result"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterValidationCheckStatus]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterValidationCheckStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterValidationCheckStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e67df63de762f82ad11ba8b2e1e88dc2a677cbafa07dc7bd146b94283a167ed9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterValidationCheckStatusResult",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremVmwareClusterValidationCheckStatusResult:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterValidationCheckStatusResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareClusterValidationCheckStatusResultList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterValidationCheckStatusResultList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__770646c19d180c4485864bea120df8bf6a5306a4b44a0f1db0d727a50beee0f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremVmwareClusterValidationCheckStatusResultOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a44d93e9d646f6d05a6f2fd593972fe8e0364427aa1ccb8e424a50dced429f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremVmwareClusterValidationCheckStatusResultOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b62ec716e8473f54d22decee5c6839ad4b2f91240160f3efa009e96e8371aba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3da8aeca1122425698a3723abb83c221a2db5d5fd13e94c8eff3bb4916ed0811)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1595496e8e90e97723f684803235cf7e5b2e85020923c8b04544251a9c8b3bac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremVmwareClusterValidationCheckStatusResultOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterValidationCheckStatusResultOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__774db7f4a2412eb6ea45559d0475c7a184c8526d0dc8c01add114aeca8c3fcd6)
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
    ) -> typing.Optional[GoogleGkeonpremVmwareClusterValidationCheckStatusResult]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterValidationCheckStatusResult], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterValidationCheckStatusResult],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__184b62b4f97e849d4b03f07f5c210e6bd7fb8a9ac1731c0d698eb082f08b2706)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterVcenter",
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
class GoogleGkeonpremVmwareClusterVcenter:
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
        :param ca_cert_data: Contains the vCenter CA certificate public key for SSL verification. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ca_cert_data GoogleGkeonpremVmwareCluster#ca_cert_data}
        :param cluster: The name of the vCenter cluster for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#cluster GoogleGkeonpremVmwareCluster#cluster}
        :param datacenter: The name of the vCenter datacenter for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#datacenter GoogleGkeonpremVmwareCluster#datacenter}
        :param datastore: The name of the vCenter datastore for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#datastore GoogleGkeonpremVmwareCluster#datastore}
        :param folder: The name of the vCenter folder for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#folder GoogleGkeonpremVmwareCluster#folder}
        :param resource_pool: The name of the vCenter resource pool for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#resource_pool GoogleGkeonpremVmwareCluster#resource_pool}
        :param storage_policy_name: The name of the vCenter storage policy for the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#storage_policy_name GoogleGkeonpremVmwareCluster#storage_policy_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb509053abe32b853764c168bd1606ecf165095baa5e38d2ad5d8a671859ad22)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#ca_cert_data GoogleGkeonpremVmwareCluster#ca_cert_data}
        '''
        result = self._values.get("ca_cert_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter cluster for the user cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#cluster GoogleGkeonpremVmwareCluster#cluster}
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datacenter(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter datacenter for the user cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#datacenter GoogleGkeonpremVmwareCluster#datacenter}
        '''
        result = self._values.get("datacenter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datastore(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter datastore for the user cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#datastore GoogleGkeonpremVmwareCluster#datastore}
        '''
        result = self._values.get("datastore")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def folder(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter folder for the user cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#folder GoogleGkeonpremVmwareCluster#folder}
        '''
        result = self._values.get("folder")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_pool(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter resource pool for the user cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#resource_pool GoogleGkeonpremVmwareCluster#resource_pool}
        '''
        result = self._values.get("resource_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_policy_name(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter storage policy for the user cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_vmware_cluster#storage_policy_name GoogleGkeonpremVmwareCluster#storage_policy_name}
        '''
        result = self._values.get("storage_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremVmwareClusterVcenter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremVmwareClusterVcenterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremVmwareCluster.GoogleGkeonpremVmwareClusterVcenterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d5b31853b310fe3bf30d4283df2c8bf198b67ea5b84a9fd495f0990001e429f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17e5a22204b913d076c694b1e39eaad7acd4d80f10be85f14c6a03f53a480747)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caCertData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f840bc45f01ce7dd32e3f2658b4534535c4e4dae350dd832f00b523dc4169aec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="datacenter")
    def datacenter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datacenter"))

    @datacenter.setter
    def datacenter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3e745945aa0a2dbfa39c1a0ff764c58c76770fb8121454efc90b67686a9efa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datacenter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="datastore")
    def datastore(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datastore"))

    @datastore.setter
    def datastore(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe52c009b373c9ad99b27f3a20024886f8c673e0b496024a8298fe9d62a11493)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datastore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="folder")
    def folder(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "folder"))

    @folder.setter
    def folder(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23d70118cd7be5605fa7aaa6843928c2a8c5808889a9fe3571f61ce4fb2ca161)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "folder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourcePool")
    def resource_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourcePool"))

    @resource_pool.setter
    def resource_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed62f8dd1d50ef28b546c99530cfe4cbd963a972155363395f10c4f4b8269b45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storagePolicyName")
    def storage_policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storagePolicyName"))

    @storage_policy_name.setter
    def storage_policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7db35baafcafed7cd0e629e7913e8996b78561030727605be920d26707738869)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storagePolicyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleGkeonpremVmwareClusterVcenter]:
        return typing.cast(typing.Optional[GoogleGkeonpremVmwareClusterVcenter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremVmwareClusterVcenter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef524e56721ecc11073bc05303274f36b46bd6c50c61fa757d864d10d1add1c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleGkeonpremVmwareCluster",
    "GoogleGkeonpremVmwareClusterAntiAffinityGroups",
    "GoogleGkeonpremVmwareClusterAntiAffinityGroupsOutputReference",
    "GoogleGkeonpremVmwareClusterAuthorization",
    "GoogleGkeonpremVmwareClusterAuthorizationAdminUsers",
    "GoogleGkeonpremVmwareClusterAuthorizationAdminUsersList",
    "GoogleGkeonpremVmwareClusterAuthorizationAdminUsersOutputReference",
    "GoogleGkeonpremVmwareClusterAuthorizationOutputReference",
    "GoogleGkeonpremVmwareClusterAutoRepairConfig",
    "GoogleGkeonpremVmwareClusterAutoRepairConfigOutputReference",
    "GoogleGkeonpremVmwareClusterConfig",
    "GoogleGkeonpremVmwareClusterControlPlaneNode",
    "GoogleGkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig",
    "GoogleGkeonpremVmwareClusterControlPlaneNodeAutoResizeConfigOutputReference",
    "GoogleGkeonpremVmwareClusterControlPlaneNodeOutputReference",
    "GoogleGkeonpremVmwareClusterControlPlaneNodeVsphereConfig",
    "GoogleGkeonpremVmwareClusterControlPlaneNodeVsphereConfigList",
    "GoogleGkeonpremVmwareClusterControlPlaneNodeVsphereConfigOutputReference",
    "GoogleGkeonpremVmwareClusterDataplaneV2",
    "GoogleGkeonpremVmwareClusterDataplaneV2OutputReference",
    "GoogleGkeonpremVmwareClusterFleet",
    "GoogleGkeonpremVmwareClusterFleetList",
    "GoogleGkeonpremVmwareClusterFleetOutputReference",
    "GoogleGkeonpremVmwareClusterLoadBalancer",
    "GoogleGkeonpremVmwareClusterLoadBalancerF5Config",
    "GoogleGkeonpremVmwareClusterLoadBalancerF5ConfigOutputReference",
    "GoogleGkeonpremVmwareClusterLoadBalancerManualLbConfig",
    "GoogleGkeonpremVmwareClusterLoadBalancerManualLbConfigOutputReference",
    "GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfig",
    "GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools",
    "GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPoolsList",
    "GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPoolsOutputReference",
    "GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigOutputReference",
    "GoogleGkeonpremVmwareClusterLoadBalancerOutputReference",
    "GoogleGkeonpremVmwareClusterLoadBalancerVipConfig",
    "GoogleGkeonpremVmwareClusterLoadBalancerVipConfigOutputReference",
    "GoogleGkeonpremVmwareClusterNetworkConfig",
    "GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2Config",
    "GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock",
    "GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps",
    "GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIpsList",
    "GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIpsOutputReference",
    "GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockOutputReference",
    "GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigOutputReference",
    "GoogleGkeonpremVmwareClusterNetworkConfigDhcpIpConfig",
    "GoogleGkeonpremVmwareClusterNetworkConfigDhcpIpConfigOutputReference",
    "GoogleGkeonpremVmwareClusterNetworkConfigHostConfig",
    "GoogleGkeonpremVmwareClusterNetworkConfigHostConfigOutputReference",
    "GoogleGkeonpremVmwareClusterNetworkConfigOutputReference",
    "GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfig",
    "GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks",
    "GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps",
    "GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIpsList",
    "GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIpsOutputReference",
    "GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksList",
    "GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksOutputReference",
    "GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigOutputReference",
    "GoogleGkeonpremVmwareClusterStatus",
    "GoogleGkeonpremVmwareClusterStatusConditions",
    "GoogleGkeonpremVmwareClusterStatusConditionsList",
    "GoogleGkeonpremVmwareClusterStatusConditionsOutputReference",
    "GoogleGkeonpremVmwareClusterStatusList",
    "GoogleGkeonpremVmwareClusterStatusOutputReference",
    "GoogleGkeonpremVmwareClusterStorage",
    "GoogleGkeonpremVmwareClusterStorageOutputReference",
    "GoogleGkeonpremVmwareClusterTimeouts",
    "GoogleGkeonpremVmwareClusterTimeoutsOutputReference",
    "GoogleGkeonpremVmwareClusterUpgradePolicy",
    "GoogleGkeonpremVmwareClusterUpgradePolicyOutputReference",
    "GoogleGkeonpremVmwareClusterValidationCheck",
    "GoogleGkeonpremVmwareClusterValidationCheckList",
    "GoogleGkeonpremVmwareClusterValidationCheckOutputReference",
    "GoogleGkeonpremVmwareClusterValidationCheckStatus",
    "GoogleGkeonpremVmwareClusterValidationCheckStatusList",
    "GoogleGkeonpremVmwareClusterValidationCheckStatusOutputReference",
    "GoogleGkeonpremVmwareClusterValidationCheckStatusResult",
    "GoogleGkeonpremVmwareClusterValidationCheckStatusResultList",
    "GoogleGkeonpremVmwareClusterValidationCheckStatusResultOutputReference",
    "GoogleGkeonpremVmwareClusterVcenter",
    "GoogleGkeonpremVmwareClusterVcenterOutputReference",
]

publication.publish()

def _typecheckingstub__86420fdab41dff2762e83f3fdf2b14401292efd0e9eab7e97231d74f032f02b8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    admin_cluster_membership: builtins.str,
    control_plane_node: typing.Union[GoogleGkeonpremVmwareClusterControlPlaneNode, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    on_prem_version: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    anti_affinity_groups: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterAntiAffinityGroups, typing.Dict[builtins.str, typing.Any]]] = None,
    authorization: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_repair_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterAutoRepairConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    dataplane_v2: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterDataplaneV2, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disable_bundled_ingress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_advanced_cluster: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_control_plane_v2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    load_balancer: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterLoadBalancer, typing.Dict[builtins.str, typing.Any]]] = None,
    network_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    storage: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    upgrade_policy: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterUpgradePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    vcenter: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterVcenter, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d0f8ba31208e73a02de5cdfa4ff547d329eb6243ac52d7e1884b66816b622b65(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487d75aaff6510c9ad62463eff2a3207d220d73fa63fb6a8254225a8354a6632(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1d3d7943bb0a079575434a31fb4d6537317c6faa7d793979c085a099c55563d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__301e8e5f5f773aede850fd9411f071e5dd15c94c44a7931e2c9c3207529390d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa135ba8f30f45fe8b3e20b0bc1c280ea98d5133db1948166a1b811b32e32674(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af5a2d9590b65d45479f930700050416c33be4c4cfb1a58cb1d2745a737d570(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2be2154a3e9e6ff2573a30e4142d4f1442b29961aef355ca2b330e829d904cc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1fcc27b5eb93fe9e0b6e8047d323bf6d63f85d97afc104c2fe824be65425109(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2372fc84cde5c02244d1b44bd829e9d70227c311ef051fb08f8bcd3d6c53cdc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b18a462965ff6cbd22da94d6a042802d7e7046a24fdc8f2bce0400d8c86779(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__561b501e45c9a1d73cbf1b561cbd3256ab89f2e2a45208758e1cdc5f6377c7e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a570b0e316733ab5c4d8f5255360e9078f29eeaf1dcc0ff29523a48859c1cb65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7322bc27bf8b7de584501281f1b94788adbe51e91346e4c879958e210831bff8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b4ab249f2e88878143a060fcc3a90d74e768a06bfc3983ba114117895b02f04(
    *,
    aag_config_disabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fda6aa394cd5f688f5897e959d2a57a2e88e04c9b3a96372e10a1226392a499f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e21ad2a0c4807b3f1f366dc126b3653e5b5ad50ac508861acd0c4ed8478131a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ded6d5657e306d9a3e1226d5c54a5ba14ac49ca1a7f2f82ab523c817323102(
    value: typing.Optional[GoogleGkeonpremVmwareClusterAntiAffinityGroups],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873c73a188918c48f5d195752b3ccf2291558ea9345130c1440398f5c0c35e22(
    *,
    admin_users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareClusterAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee06517fd84049a0db43a933bcd086879e512d7f5af68c329344dc225ae97a27(
    *,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac72a11aec2d2b03599fa88b2ed6808bb9f6d3421f63962898f206eab1ab7f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dad57d8c57ca9ec60419740b1711c1eeb37214461b1587b5547edbbf2f4c53f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d223a294844fe8e4a87316bef9cf2fe36c2375073f5703c7d2c056246e77576(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9221664457374004554cd3a9b0bdef87e51a6dfb916a442b7eef859838d1d2d0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9ac712006d144e1fc25223b8ea00f82ad18a1fe4d7e978e37d55ef47144e5af(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c25014bdb2f9686b43874ecfc125ae405bc9a618ffbaf45e28e5a1d58fbef030(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterAuthorizationAdminUsers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__234965f7715361d354c30abebc8f7bdd0ed4d76202a97b13a027f8f423390d85(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73ce34b2b6ec650294d45a8a374ca1bede15aaaf3dc9f03095a043740ce592a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8b85b252f9e3635912a7358862389f33ea5133c0a00efc83891dd27c58de551(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterAuthorizationAdminUsers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90a8d95b736b2ea3882ca873d3b8cbab0151b05d6f89f9e4e9fee7d02540c2f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d27646eefdd31c823e7d2467ea82342f3617691ae6083b9513411d045c5e1310(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareClusterAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df20338a179877239d95a7ee2144618552637b94043b71f55548afcf07155fc7(
    value: typing.Optional[GoogleGkeonpremVmwareClusterAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21838d6652f43b51c1b3f7dde57f92dff82b6a869c7829a5970b3ccd5da9cf8c(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f892f9c828ffe5f44829e200d9f14d569ec9b2d6e482a6062bbf0ba1984c6c88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__429e20a7778e2673e28af8aa6d108730bfc5aa1f81540757c969f0ab719fd441(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b61644b1c094de2e7ba5a11c93db8e0086d9361141ba00b3b74b5e039a0c78(
    value: typing.Optional[GoogleGkeonpremVmwareClusterAutoRepairConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd6195c5b1b87631c0536545cd449ce4c51af9dfcb98c51cfe475ab2d5ffafc3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    admin_cluster_membership: builtins.str,
    control_plane_node: typing.Union[GoogleGkeonpremVmwareClusterControlPlaneNode, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    on_prem_version: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    anti_affinity_groups: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterAntiAffinityGroups, typing.Dict[builtins.str, typing.Any]]] = None,
    authorization: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_repair_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterAutoRepairConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    dataplane_v2: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterDataplaneV2, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disable_bundled_ingress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_advanced_cluster: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_control_plane_v2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    load_balancer: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterLoadBalancer, typing.Dict[builtins.str, typing.Any]]] = None,
    network_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    storage: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    upgrade_policy: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterUpgradePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    vcenter: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterVcenter, typing.Dict[builtins.str, typing.Any]]] = None,
    vm_tracking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22eaffa880a77736fb8f0819b9181f77fc1af579f672d16624643410a92cd204(
    *,
    auto_resize_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    cpus: typing.Optional[jsii.Number] = None,
    memory: typing.Optional[jsii.Number] = None,
    replicas: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c219b3f8be581d95c1426d836c6e7e11242715500b6f430b52cccc4b4ed393e(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42d0b3606582d25c80d7fdddb1573bec6804557a8f091c899495af598f85cb4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdc1c87ff43c3abb6fc8d76af7f7077edd3d4836643d4023e595617f248806ee(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf09813cd5240840e9709ce92c2d7c962314f03d997baa4415b19dff12260cbd(
    value: typing.Optional[GoogleGkeonpremVmwareClusterControlPlaneNodeAutoResizeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe922d24be72e2c658666cb0c02fc760bb7b1765626a70a450b2885d417f08fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__061491782d5d7474afc85c1787ffee4f43f391937f8eb76d8ebe8fae581ee830(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecee1505823e3106324ed8f1c0228e214f983f6a57fb7d1c1241a7ef1119c7d5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a254fdfdf578aef7fc4140d1b426b703799e16abbaece7ce621f12625bc961c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67a84dff571fced7564b6f8dcdd5f4a93c295402fb69d74b2d2b310f00d90829(
    value: typing.Optional[GoogleGkeonpremVmwareClusterControlPlaneNode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f464d428793516357776688b3c71587079bbdd42234b63cca602f97936bd6b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7397f9204d9cedb2b87ec83aa5e68bda471114f2207efc33105f028330c6be2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54318b4b195822c9700f4b10355eb9f6193d7d1bc7a7fec8ea0b4b05e1e2888b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a28b892d4254e1e28c7027da1615e1c6894838dd1cd352ebfeb52c16ceeb2cd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f494ad100fe49719310c802f817d901c4da2749afc072b6907b4f4f56f89bc4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee5f8766a889d26a252e2379f1ee2063d173499c8efe8606882dcf5fdb228f95(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7356a2ebe6916e01f87dbbe6e9de71cf36f5ceead19d41f3220742df9e66c9de(
    value: typing.Optional[GoogleGkeonpremVmwareClusterControlPlaneNodeVsphereConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4afee76698869fd2fa3b86d41ff1a40d3a0e9900b71270fa686e0c44ae82dfff(
    *,
    advanced_networking: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dataplane_v2_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    windows_dataplane_v2_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44f37fdb825b7eb21af6e6c2d2231e8eb2f25a66eec0626e906090a06519c145(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9514a90f5e8d20f5b9d337150019e4d9a83f95970f728ad3d98392966a8e9e68(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91a0b4b300ad422a286761d24c5abc067e9d8b13e093197bc19275a4404830db(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f5ecda78b7e59a778a8f7f2d6b48fab4fb654e9cb85c0d9311dad5a70228a9f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e78f0f58eaf3288c3c6c9da9ed3d6f86806204708d1514ef6e29ca3c738ca57(
    value: typing.Optional[GoogleGkeonpremVmwareClusterDataplaneV2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff6b6f966c3d8eebf7e69197e704ca4f882526a43ded7daa53d50647bfed2f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bda85a310c6d356a6ccf295ce74b5c402e5e4d151819da8b1e651693d72f7e1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9681b76aef1bcc026c41b52fa3c5ef64eb2bf7c68f673aeaf1bd3d19ffa00b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8718fb0d8336d698b64b8b82f9a513c481910646e8080774a13ea2a4069640e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b368ffebaa78925db39b39300f0f1db32916b192be0c74aa0b7b5d2afc55ead(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe118e67e7afcbe3ab472f37b67a55c2849fcd88bf73f6284f597762668908a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd3530acf43e2e553a89455672b0625ccdd51889e978977531b7bb2cc812e9f(
    value: typing.Optional[GoogleGkeonpremVmwareClusterFleet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac7c13aa95a45273c6cc6deedf6fab7be22314bf5111b5d2c019174aa437d59(
    *,
    f5_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterLoadBalancerF5Config, typing.Dict[builtins.str, typing.Any]]] = None,
    manual_lb_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterLoadBalancerManualLbConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    metal_lb_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    vip_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterLoadBalancerVipConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10be6a176461f2f0391dc3a1d3b5b5c118693e1b03b82c5e8a03d0c12215907c(
    *,
    address: typing.Optional[builtins.str] = None,
    partition: typing.Optional[builtins.str] = None,
    snat_pool: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73303c038efee5359822aef4a5c2760705e62909732b4844439bd4c65821df4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78cd1263ab5ea8b461950a2f9e1c950eebb4258bb0333179c9d9204ecfa5a6bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca856830614ae7c0c6c3ceb4fd8ee70dccd96b7a1370d171e9bedcf2464426cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fd401b5f9f097df308a86b2c68ef172322d152f7671f7318173d1687083f9c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb7f1d3256913a08d95860fc89cf543c328c19c13bb8f86f37213a10888b6eb4(
    value: typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancerF5Config],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ce291fe00e367da84f97756699d2e1392e89a206a14c29efcf38bb1571a5e00(
    *,
    control_plane_node_port: typing.Optional[jsii.Number] = None,
    ingress_http_node_port: typing.Optional[jsii.Number] = None,
    ingress_https_node_port: typing.Optional[jsii.Number] = None,
    konnectivity_server_node_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3969c935bb0b0dcc734393e3bbb0fd32cd4a3d1516d51fa68e6fa8c223d472c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d07ca9e960edb72e35f06d2abea210d73e44ceee203af5948b1279514d0e5ae0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16dddc70641c55866203a6b52b184e5763c3e132fa760139dd9e601e1184ecf2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1451ccc50d4581260e09848da8a209cbb51d891687a793e1795066f5c6517fb5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e2c387271616749f55a4c7bf7de8517c9a85531aa105f8f52b257f1fa17f30(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92df6417573a4b99f9db6874494fae9dad3126d42ddbb2939a1ac634ea5d425f(
    value: typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancerManualLbConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6edf57cf692898156095ffca422157dc946e91416c268903811317c474de8816(
    *,
    address_pools: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ca63a22af008a19ab656a26434ed97ae38e097806a099b6905d3fcbd8d6a40d(
    *,
    addresses: typing.Sequence[builtins.str],
    pool: builtins.str,
    avoid_buggy_ips: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    manual_assign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d7e7f2ad98b471dee77880d0108433acb4603a792beae3f4f6f054c2d09ba6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1376977cd093b00e65b4bcf629d283b538d6e406a6077507fd5afd40afc99817(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bf858083c4e3b49b58fe8ac453b98c9197c81daea7b9c2cb2f389ecaa5b472c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7a72ba51e12ead4c0831f6b92d558ee5e950a49f0d472e106e9f6a1f27709a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e8674efbe36627afeb2dd8b0af0a156441eea77249a1159155d3b43e39323cb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f868ca42f25c5c1452cada3c788a167ddeba1ce541dbe7a1203ba72de0eab229(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35b7472e40e8c6344e767e8849b86fa34a84c1c5ae7fb08de7f5a7b99130db8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5b2f4fdb4e165fa1637af36e165eb12fb2129f6486afc87eb7d60a588408bfa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__733836881dcf1b473d89893c852953b23731c04a6ceff134b9923cf2b5a60b07(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8553b6eb9d9997cf741e0c1e2eb4372b0f20867d4ea1095d664f0fc79d7b835(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b1b461264f60ac9e3695aaa046d2316180360a807b08f1dbb1e344e796186a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bf2707a6788bba203bef7d21e6d9b3616024a35899df27a3d052623f5149ced(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea928cd24fe48fcf4ffef92388fa8b091cd733fa850812d4942604e108f7154b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8820d3f92f72457da78afa572285a63473f51e4e43278638d81029b55a78104d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a11b43a16951dd69a655a3adf3338ee03bda8c8ae77173724c6e5a7a3a03042(
    value: typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancerMetalLbConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5418edbd0a82f2754d584ce05b18bd7617e6be0570b07f25fee2318308ffbac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90aeca80d667877fd9b10b0f9d2a3fa4acaaa35f3a068ac2ccb59783b5aad333(
    value: typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87e5654868920641cf07630c86a523471dd3a93fff305a70ef82c74078e34b3(
    *,
    control_plane_vip: typing.Optional[builtins.str] = None,
    ingress_vip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c7cd613754362941fb3161a520fd412f01323f6aa13020c1fc4b168b70e6c18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2df02d7f3096327aea79e8e1d7df01c44f9edeb5f31003dbc21ddbdc3a531d20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c6332a5e9986db945e9c9b9d5336713336a0d859a4932b6810baac2cf2a76d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fede1828d790961f9ad219e3ab5c701886d767c722c5ccb80e07623454b484e2(
    value: typing.Optional[GoogleGkeonpremVmwareClusterLoadBalancerVipConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f8ef60f9fc7111722b79f0d1d5ff26c075cd2e8e6bd17d12c2e4e95067b0f2(
    *,
    pod_address_cidr_blocks: typing.Sequence[builtins.str],
    service_address_cidr_blocks: typing.Sequence[builtins.str],
    control_plane_v2_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2Config, typing.Dict[builtins.str, typing.Any]]] = None,
    dhcp_ip_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterNetworkConfigDhcpIpConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    host_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterNetworkConfigHostConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    static_ip_config: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    vcenter_network: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c65ff656002100dd1140b06bbe397d5c7fdc18c2e6d17cb80e24cc8c3241bec(
    *,
    control_plane_ip_block: typing.Optional[typing.Union[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80ea7af5191352e0dde19d42b67807baf921b7a5c03da9900a76f5eed8ba3d62(
    *,
    gateway: typing.Optional[builtins.str] = None,
    ips: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps, typing.Dict[builtins.str, typing.Any]]]]] = None,
    netmask: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1015b168e5478deacb989015cabff975287f3be1f6105b975b9314464afe403c(
    *,
    hostname: typing.Optional[builtins.str] = None,
    ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aaef58c8e331197e6ad6215fd82a25f2f108c16b872fd1aeca69bc4202d6621(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de99d04406cc71c43bdc0abc3780485ae4a09cafa316b5ccad1776727b94b1c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__080f479d2506c91007ccee2ff547de9ed5dc014f449cf98f785e2aff5c57f6f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a42c54fcf8547a370ed465c5e0c5613219ef624ab0b6e0d9fac2ac8f9eba05(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602b27c63bfbd4476d823a907916f71ef130794dcd9b58dd4ebefa791930291d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__918df7e831b0910c2c5b519a4365a4dd3edc5fc9562a64a3571cb36287ca58c3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e1059ffc39cb2859b29810b35952a4a87130a13402a0d79233029090d40ca4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__600723251edf2da1348249208c610c906cd01bf9c0a0f290c7044ba950c9aa0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61fdecd881875adcd3051a963af4dd54f9637caa0ac937fab1039af84a9232d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__158faceb5e4494bdb7f519a5e2c5dae238635480cd6164991c2a100c641cf54e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7a01c57de90b1e9cc7eab038089134641d5f71fa5f62cf01c5205ffd347d280(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a305944cfdc88e1c0c42f2f561fbd9e19b8d407f22588207b95424cd87df6887(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlockIps, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f3cc6cf4a747bda70c985f42778fa4c4bd3cfcd8a7faf845c59c64ffe88007(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52a9d65727736a263d1c8df7df7caa9331d624d90431a03b89e602628b3219d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e81d18ef23bb8fbac9eb2e2ee77dbe187928ca60e64b5a0cc5b4b492bb96d145(
    value: typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2ConfigControlPlaneIpBlock],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd5a9588931cbe0386b87ce00017b3d338de4d91fbf73f84d3270713afb96c78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e438e29726cdc15d38dd11df1e06266220df182cf881e4df3e2d8cc5ff8197b(
    value: typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigControlPlaneV2Config],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3514f6decd7a2f540b06d79048f1b2442485a1858514cc0c04026e1cdaa5649c(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f53425eb73ed28dab20cee3e9b0a437ec361ac452f50a7a7efb007405cd898(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ce6edc5e56a223c84b868cb3c66eb77c5e380489216a4eae1ac2acf19cbe19(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48a7ee33e684fe8c6b6d311d1a433d3b75ceac48148a8a074437beaffaa86250(
    value: typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigDhcpIpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1162ceedda499b68e65cf7e2c3447d56b65daead7766c91c15f7be0e2f1764bd(
    *,
    dns_search_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ntp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a058d14093f4cf2201c6c62444df6aa6ccbb50e5e9df54d866aa5d102bd4765(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a55db63472496c58a6fc5de2281af73116937306d3f397cf46518613273a96e0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa03245f88ab951e23e7828c63e15524ad6c3e0eb46e26f027e509e3764831bb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f372ce7589176a9780386653fcd6ad3b4ef475e0435313601ef3ab5b3f00ca36(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64727fd88964b2f3737fb9bbc524cec563c1874a894449d9a15d6bb1ac15c45a(
    value: typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigHostConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__281aebe6e7582b8f7eb6d142ac2a924a665d8684bb29c2be12be499c8e1ed52b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb7354f0589de06e47f62ec219e913c35515addf6b6a0717590986d3eaa13d87(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0dcf34facebd9e112603b643775ac3c0da48f5b7bcbf6e8908f118d70655d0b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e43e3aa1f0bb9b750091fa6b3e2eaadc1e9d43d8418cfac7f860c7d76b84f2c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b5546e2db7ad56d096508d33096eb46d83cc86bc64d4b1e418fafcfab9ac2c(
    value: typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d4998090ec82491e59685f357c7b0c26e3c419d6ce4a9f7a3eb60e848face93(
    *,
    ip_blocks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7c731d42484fdb7b04a0cea6bc6d796139de73afb9d671cdad8a57ea3b3ad5f(
    *,
    gateway: builtins.str,
    ips: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps, typing.Dict[builtins.str, typing.Any]]]],
    netmask: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b7e1f2ab793471d7fc9efc9cb794cada6b00a64960931aea883d38f26277f3(
    *,
    ip: builtins.str,
    hostname: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e90e9fc4efc302ba5e6e8ae67ce03249f7eb37eaae534ef9d5d5a93cab5b36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81455b0dd03c3975e85699b7754bce3dbf182b09f394406f44f4fe9576ee126d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed973a07d1a05840669f1524c356ffb342cdf401d7729b73c27e889c0083abf5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7eb4e8a18b20f6d33d53f302dc5ae8a92b94daff3ad27428392ed3f3c0eec8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3927d27446377721aea7fe88945e59c08500349bb6487b6b6583b8e0bfb4ffcd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d755966acd25e68c062394c26fcb08af1fe2b655573e8aeef7ca390c4ec9dc09(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c0fca9359b2b62666fe2306fd925bf24fe98ccb8cc73410a1c680bdd9d67145(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e907ca914d00484425cd438fe2105f3e329341574c24506336998dc22a02bdf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea406737e9f1a68f31bca4d5254e9ad4c6ca8a657bd70056eca616f781ce1222(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__350346522ed66bf7169b5c817de9cc7fcf9df01d816c0f6584c1b064de76ba76(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93835245c5c73db342be4b46cc4f4694243e59e2158e614606e19f869c7eb0a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53cef29495a1efeb7ce8085e53505352c92dd8937e9daa75b654b38c7780bdc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c6c2ec16db61c7ed66baa334d7426e29165b0ac06331de8dbcee60386c94f55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f30fe922844f84f5a0b42a44afc67f2c49436888499ab0a247ce535bded876(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6930d8fa11e523e81ba5333f030acb459a1c87b1ac9f072b967fffd319c5a79b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a899f92e6473a0fff976ce24661fd0362b8bb17462f2f775d9b3f3b927ba66d8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d79269a5142eaaf84769108f949a15bd1987273ae9acecb50fcbabc8cc5ee693(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6842e526b2f7466a45060466171992704ac7fd7a8861415532684ffd1f950d89(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocksIps, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61c836b1c2d5772fe571349a747d7fa4cdfb0eb9624df7da119fa58040e48d7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d8aa5385d0fe589f381f6c183aa16104ed513900c33118233ff054946e95dd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b677a25612168e50f401a033c362c8c99f7137b3772410574297c86845d000(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__449ceeab16ea6e89775c39e1f716153bc50d0b5119327bf172c42b324fcc216b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06063f11fc9b5f69facde596e2b4ac6bedfff7b8fac60dd7bdedd87adfb077eb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfigIpBlocks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72306d06f144cb471c7ae86cdc627d2167406de5cf96ec6286f4357f7d01086c(
    value: typing.Optional[GoogleGkeonpremVmwareClusterNetworkConfigStaticIpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a5c726c7bc4c77348458d70afe6e5902efcc84979d10f580bdc946efd57f317(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fdf4073150c8d7f14b7112157fe21dfb93dce34abc53e9870dc761c28e72e61(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a0a8ff004e9dee38f94b8cf9b50beca6657d842bd28fd81282beeeef0358315(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f71a292a2b41fb744b8ea0924e84418aca1d8fff67a3f8e4f79f141f88f08f4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__531c42292eef8cb6bad65bf16875e2cc7d4ccb6807287aaf4de787519d665c99(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e3a70ccb8d797746360928bf8606896dbaa3d5b59b4008d9cf9bfb53a802850(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f069289a3b406871780049ed85b83b3350d2ad9f380843daf92ca009d2719c0(
    value: typing.Optional[GoogleGkeonpremVmwareClusterStatusConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b2c93e574dc05e2a5e63b72dfcdfb69438b7d1c6ab4ae32df1283dd4ad1c0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b445a090ad9d205533fd0aab46e1eaf22d98f5610cac9fbfbb761df889e8f0d1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ea34860cd2a8357e5b2456ced404f899a2a82015a59b78d7cc46603de64daf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe9c0118c6403704108c123b189eb0c53e3f28c585804434ec49cc15f6ae877(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d08d55a0b108fbf08622931259c25e16d57325a1bcd574183ecd381970233442(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77eedf0f8cee804c195c7702c9d2e5afa03241063c66fe31bbaf6354473bdd1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc67278af24e470c8b439c1e242f62c7baff765a9c6e809792b175a1986b7df9(
    value: typing.Optional[GoogleGkeonpremVmwareClusterStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00f885203589490a0256456032db8231fb691c749329f06dce1ada70622e7f83(
    *,
    vsphere_csi_disabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c07d62f920121fbc5ba89c5e696bd3d6a0d62b5010b2743d2040b1e689890ee2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c3eb7d12197fe7119dab4f5cde1bbedc75d0007516a11bd5b5fbbf516ddc87e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17e276281554f8d9752a7f2084d6dfccdee428d23be490c613dce3366ba5c56b(
    value: typing.Optional[GoogleGkeonpremVmwareClusterStorage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__412efaac85e14b0f45c9c7c38e706dc0bbe3c45d3e744f264512ce4385b5e3e5(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0346c3aa315906cb99c56d6ee07eda08fe8d228cd60f36f44ba3f9a7c4a8a81(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ccb9da87cda1b6e6e20546a74dc76e85f6ab1bb9d1270026068bf08d0a0ca3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4134c5b91030d251d6f67050e14dc8bbdd2b5ebd2b611536b3893261b70bc800(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71308bcd8fc0a69812722d289ac5eafdeaaa0971550b2d9762ec1f219927a999(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d1db60812e9d1b95e59b20c53da0cd9394940202dd98c1a73fe0e151406076(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremVmwareClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__059abed1b7898d96b76f0a6261c3af62477d90e54daf06082eb3ff318585784f(
    *,
    control_plane_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d74598ba177c37f096fb940a779f0f38641d80eace6a71ac0fe1885ef1852259(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15778a524e7452bda995d0b323ab4eea7c22e7de92024913f894a38d5547d067(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2296ade18f1aeaf8e542dfdd0e006e337eb9b51b666641965983fa8adfb8ebc1(
    value: typing.Optional[GoogleGkeonpremVmwareClusterUpgradePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f510759e0d3ef9a35c7433148f372eb73c37dfe0b525481a983d77ac654344d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1089f66ff8ebf57d5ad341e608e7e53819dde296593a14ff276ad8692e06180c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b60d26ef34083b2a530f7c8c96f1066c7be6f1719e3bd0ddef70e1ccec6a8f7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32c61ceea835070c654b098a3a2bc377e761c10f759b0a1001b4a13854207538(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27a1e2b6d1d903ec0f7ec155dbbaca66da5631824f623aaf0c8c552d7a923370(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3538babf7fc0dacb0ab6012a9e4d268a50aa6c1cff9272cae3595c15951ab8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b8c1381915104612b9c45e8887122ad441b716b6a035d87d790634b888cd30d(
    value: typing.Optional[GoogleGkeonpremVmwareClusterValidationCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da2b870c0f761c5d4d779919cef71d69b72b3c7b2729a5d2e90da54c101e583b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6343f62639ac7e1d3587bb7835e7a49d2fa74992a542f12552aaeaf0d3aca56(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa8997dd7793eaa71c3d5ca2bf2ac6deea4371dad2a5a881b71f5f891148aeae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0880bf4efc1dcfd7fd52107a8d4e1d16c7f4e448586992d5de2cca3d4ec8ab19(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5631595246e3800c3f86a45dd0ead256b421fde91e90aa28cc11f4bb3323c323(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb840f0316f362bf2fc7b192569d5e27b7620e21fe9eb1edfae35c23e9c71136(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67df63de762f82ad11ba8b2e1e88dc2a677cbafa07dc7bd146b94283a167ed9(
    value: typing.Optional[GoogleGkeonpremVmwareClusterValidationCheckStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__770646c19d180c4485864bea120df8bf6a5306a4b44a0f1db0d727a50beee0f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a44d93e9d646f6d05a6f2fd593972fe8e0364427aa1ccb8e424a50dced429f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b62ec716e8473f54d22decee5c6839ad4b2f91240160f3efa009e96e8371aba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da8aeca1122425698a3723abb83c221a2db5d5fd13e94c8eff3bb4916ed0811(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1595496e8e90e97723f684803235cf7e5b2e85020923c8b04544251a9c8b3bac(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__774db7f4a2412eb6ea45559d0475c7a184c8526d0dc8c01add114aeca8c3fcd6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__184b62b4f97e849d4b03f07f5c210e6bd7fb8a9ac1731c0d698eb082f08b2706(
    value: typing.Optional[GoogleGkeonpremVmwareClusterValidationCheckStatusResult],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb509053abe32b853764c168bd1606ecf165095baa5e38d2ad5d8a671859ad22(
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

def _typecheckingstub__3d5b31853b310fe3bf30d4283df2c8bf198b67ea5b84a9fd495f0990001e429f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17e5a22204b913d076c694b1e39eaad7acd4d80f10be85f14c6a03f53a480747(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f840bc45f01ce7dd32e3f2658b4534535c4e4dae350dd832f00b523dc4169aec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3e745945aa0a2dbfa39c1a0ff764c58c76770fb8121454efc90b67686a9efa5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe52c009b373c9ad99b27f3a20024886f8c673e0b496024a8298fe9d62a11493(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23d70118cd7be5605fa7aaa6843928c2a8c5808889a9fe3571f61ce4fb2ca161(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed62f8dd1d50ef28b546c99530cfe4cbd963a972155363395f10c4f4b8269b45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7db35baafcafed7cd0e629e7913e8996b78561030727605be920d26707738869(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef524e56721ecc11073bc05303274f36b46bd6c50c61fa757d864d10d1add1c8(
    value: typing.Optional[GoogleGkeonpremVmwareClusterVcenter],
) -> None:
    """Type checking stubs"""
    pass
