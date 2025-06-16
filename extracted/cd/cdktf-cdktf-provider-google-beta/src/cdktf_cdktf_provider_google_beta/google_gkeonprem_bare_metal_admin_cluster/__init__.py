r'''
# `google_gkeonprem_bare_metal_admin_cluster`

Refer to the Terraform Registry for docs: [`google_gkeonprem_bare_metal_admin_cluster`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster).
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


class GoogleGkeonpremBareMetalAdminCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster google_gkeonprem_bare_metal_admin_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bare_metal_version: typing.Optional[builtins.str] = None,
        cluster_operations: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterClusterOperations", typing.Dict[builtins.str, typing.Any]]] = None,
        control_plane: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterControlPlane", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        load_balancer: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterLoadBalancer", typing.Dict[builtins.str, typing.Any]]] = None,
        maintenance_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterMaintenanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        network_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_access_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterNodeAccessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        proxy: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        security_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterSecurityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        storage: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster google_gkeonprem_bare_metal_admin_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#location GoogleGkeonpremBareMetalAdminCluster#location}
        :param name: The bare metal admin cluster name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#name GoogleGkeonpremBareMetalAdminCluster#name}
        :param annotations: Annotations on the Bare Metal Admin Cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#annotations GoogleGkeonpremBareMetalAdminCluster#annotations}
        :param bare_metal_version: A human readable description of this Bare Metal Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#bare_metal_version GoogleGkeonpremBareMetalAdminCluster#bare_metal_version}
        :param cluster_operations: cluster_operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#cluster_operations GoogleGkeonpremBareMetalAdminCluster#cluster_operations}
        :param control_plane: control_plane block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#control_plane GoogleGkeonpremBareMetalAdminCluster#control_plane}
        :param description: A human readable description of this Bare Metal Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#description GoogleGkeonpremBareMetalAdminCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#id GoogleGkeonpremBareMetalAdminCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#load_balancer GoogleGkeonpremBareMetalAdminCluster#load_balancer}
        :param maintenance_config: maintenance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#maintenance_config GoogleGkeonpremBareMetalAdminCluster#maintenance_config}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#network_config GoogleGkeonpremBareMetalAdminCluster#network_config}
        :param node_access_config: node_access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#node_access_config GoogleGkeonpremBareMetalAdminCluster#node_access_config}
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#node_config GoogleGkeonpremBareMetalAdminCluster#node_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#project GoogleGkeonpremBareMetalAdminCluster#project}.
        :param proxy: proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#proxy GoogleGkeonpremBareMetalAdminCluster#proxy}
        :param security_config: security_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#security_config GoogleGkeonpremBareMetalAdminCluster#security_config}
        :param storage: storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#storage GoogleGkeonpremBareMetalAdminCluster#storage}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#timeouts GoogleGkeonpremBareMetalAdminCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82f6af80fc09edba4dee7869829a9e37a75ca87950437cb7485aed5a92f17c0d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleGkeonpremBareMetalAdminClusterConfig(
            location=location,
            name=name,
            annotations=annotations,
            bare_metal_version=bare_metal_version,
            cluster_operations=cluster_operations,
            control_plane=control_plane,
            description=description,
            id=id,
            load_balancer=load_balancer,
            maintenance_config=maintenance_config,
            network_config=network_config,
            node_access_config=node_access_config,
            node_config=node_config,
            project=project,
            proxy=proxy,
            security_config=security_config,
            storage=storage,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a GoogleGkeonpremBareMetalAdminCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleGkeonpremBareMetalAdminCluster to import.
        :param import_from_id: The id of the existing GoogleGkeonpremBareMetalAdminCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleGkeonpremBareMetalAdminCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44d58927d246e69d24b2ba7b5e91f3da2cb9f16bac367f9fab70abe431a1b417)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putClusterOperations")
    def put_cluster_operations(
        self,
        *,
        enable_application_logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_application_logs: Whether collection of application logs/metrics should be enabled (in addition to system logs/metrics). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#enable_application_logs GoogleGkeonpremBareMetalAdminCluster#enable_application_logs}
        '''
        value = GoogleGkeonpremBareMetalAdminClusterClusterOperations(
            enable_application_logs=enable_application_logs
        )

        return typing.cast(None, jsii.invoke(self, "putClusterOperations", [value]))

    @jsii.member(jsii_name="putControlPlane")
    def put_control_plane(
        self,
        *,
        control_plane_node_pool_config: typing.Union["GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig", typing.Dict[builtins.str, typing.Any]],
        api_server_args: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param control_plane_node_pool_config: control_plane_node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#control_plane_node_pool_config GoogleGkeonpremBareMetalAdminCluster#control_plane_node_pool_config}
        :param api_server_args: api_server_args block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#api_server_args GoogleGkeonpremBareMetalAdminCluster#api_server_args}
        '''
        value = GoogleGkeonpremBareMetalAdminClusterControlPlane(
            control_plane_node_pool_config=control_plane_node_pool_config,
            api_server_args=api_server_args,
        )

        return typing.cast(None, jsii.invoke(self, "putControlPlane", [value]))

    @jsii.member(jsii_name="putLoadBalancer")
    def put_load_balancer(
        self,
        *,
        port_config: typing.Union["GoogleGkeonpremBareMetalAdminClusterLoadBalancerPortConfig", typing.Dict[builtins.str, typing.Any]],
        vip_config: typing.Union["GoogleGkeonpremBareMetalAdminClusterLoadBalancerVipConfig", typing.Dict[builtins.str, typing.Any]],
        manual_lb_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param port_config: port_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#port_config GoogleGkeonpremBareMetalAdminCluster#port_config}
        :param vip_config: vip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#vip_config GoogleGkeonpremBareMetalAdminCluster#vip_config}
        :param manual_lb_config: manual_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#manual_lb_config GoogleGkeonpremBareMetalAdminCluster#manual_lb_config}
        '''
        value = GoogleGkeonpremBareMetalAdminClusterLoadBalancer(
            port_config=port_config,
            vip_config=vip_config,
            manual_lb_config=manual_lb_config,
        )

        return typing.cast(None, jsii.invoke(self, "putLoadBalancer", [value]))

    @jsii.member(jsii_name="putMaintenanceConfig")
    def put_maintenance_config(
        self,
        *,
        maintenance_address_cidr_blocks: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param maintenance_address_cidr_blocks: All IPv4 address from these ranges will be placed into maintenance mode. Nodes in maintenance mode will be cordoned and drained. When both of these are true, the "baremetal.cluster.gke.io/maintenance" annotation will be set on the node resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#maintenance_address_cidr_blocks GoogleGkeonpremBareMetalAdminCluster#maintenance_address_cidr_blocks}
        '''
        value = GoogleGkeonpremBareMetalAdminClusterMaintenanceConfig(
            maintenance_address_cidr_blocks=maintenance_address_cidr_blocks
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenanceConfig", [value]))

    @jsii.member(jsii_name="putNetworkConfig")
    def put_network_config(
        self,
        *,
        island_mode_cidr: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param island_mode_cidr: island_mode_cidr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#island_mode_cidr GoogleGkeonpremBareMetalAdminCluster#island_mode_cidr}
        '''
        value = GoogleGkeonpremBareMetalAdminClusterNetworkConfig(
            island_mode_cidr=island_mode_cidr
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfig", [value]))

    @jsii.member(jsii_name="putNodeAccessConfig")
    def put_node_access_config(
        self,
        *,
        login_user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param login_user: LoginUser is the user name used to access node machines. It defaults to "root" if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#login_user GoogleGkeonpremBareMetalAdminCluster#login_user}
        '''
        value = GoogleGkeonpremBareMetalAdminClusterNodeAccessConfig(
            login_user=login_user
        )

        return typing.cast(None, jsii.invoke(self, "putNodeAccessConfig", [value]))

    @jsii.member(jsii_name="putNodeConfig")
    def put_node_config(
        self,
        *,
        max_pods_per_node: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_pods_per_node: The maximum number of pods a node can run. The size of the CIDR range assigned to the node will be derived from this parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#max_pods_per_node GoogleGkeonpremBareMetalAdminCluster#max_pods_per_node}
        '''
        value = GoogleGkeonpremBareMetalAdminClusterNodeConfig(
            max_pods_per_node=max_pods_per_node
        )

        return typing.cast(None, jsii.invoke(self, "putNodeConfig", [value]))

    @jsii.member(jsii_name="putProxy")
    def put_proxy(
        self,
        *,
        uri: builtins.str,
        no_proxy: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param uri: Specifies the address of your proxy server. For Example: http://domain WARNING: Do not provide credentials in the format of http://(username:password@)domain these will be rejected by the server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#uri GoogleGkeonpremBareMetalAdminCluster#uri}
        :param no_proxy: A list of IPs, hostnames, and domains that should skip the proxy. For example: ["127.0.0.1", "example.com", ".corp", "localhost"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#no_proxy GoogleGkeonpremBareMetalAdminCluster#no_proxy}
        '''
        value = GoogleGkeonpremBareMetalAdminClusterProxy(uri=uri, no_proxy=no_proxy)

        return typing.cast(None, jsii.invoke(self, "putProxy", [value]))

    @jsii.member(jsii_name="putSecurityConfig")
    def put_security_config(
        self,
        *,
        authorization: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#authorization GoogleGkeonpremBareMetalAdminCluster#authorization}
        '''
        value = GoogleGkeonpremBareMetalAdminClusterSecurityConfig(
            authorization=authorization
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityConfig", [value]))

    @jsii.member(jsii_name="putStorage")
    def put_storage(
        self,
        *,
        lvp_node_mounts_config: typing.Union["GoogleGkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig", typing.Dict[builtins.str, typing.Any]],
        lvp_share_config: typing.Union["GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param lvp_node_mounts_config: lvp_node_mounts_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#lvp_node_mounts_config GoogleGkeonpremBareMetalAdminCluster#lvp_node_mounts_config}
        :param lvp_share_config: lvp_share_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#lvp_share_config GoogleGkeonpremBareMetalAdminCluster#lvp_share_config}
        '''
        value = GoogleGkeonpremBareMetalAdminClusterStorage(
            lvp_node_mounts_config=lvp_node_mounts_config,
            lvp_share_config=lvp_share_config,
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#create GoogleGkeonpremBareMetalAdminCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#delete GoogleGkeonpremBareMetalAdminCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#update GoogleGkeonpremBareMetalAdminCluster#update}.
        '''
        value = GoogleGkeonpremBareMetalAdminClusterTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetBareMetalVersion")
    def reset_bare_metal_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBareMetalVersion", []))

    @jsii.member(jsii_name="resetClusterOperations")
    def reset_cluster_operations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterOperations", []))

    @jsii.member(jsii_name="resetControlPlane")
    def reset_control_plane(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControlPlane", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLoadBalancer")
    def reset_load_balancer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancer", []))

    @jsii.member(jsii_name="resetMaintenanceConfig")
    def reset_maintenance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceConfig", []))

    @jsii.member(jsii_name="resetNetworkConfig")
    def reset_network_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConfig", []))

    @jsii.member(jsii_name="resetNodeAccessConfig")
    def reset_node_access_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeAccessConfig", []))

    @jsii.member(jsii_name="resetNodeConfig")
    def reset_node_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetProxy")
    def reset_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxy", []))

    @jsii.member(jsii_name="resetSecurityConfig")
    def reset_security_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityConfig", []))

    @jsii.member(jsii_name="resetStorage")
    def reset_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorage", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="clusterOperations")
    def cluster_operations(
        self,
    ) -> "GoogleGkeonpremBareMetalAdminClusterClusterOperationsOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterClusterOperationsOutputReference", jsii.get(self, "clusterOperations"))

    @builtins.property
    @jsii.member(jsii_name="controlPlane")
    def control_plane(
        self,
    ) -> "GoogleGkeonpremBareMetalAdminClusterControlPlaneOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterControlPlaneOutputReference", jsii.get(self, "controlPlane"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

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
    def fleet(self) -> "GoogleGkeonpremBareMetalAdminClusterFleetList":
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterFleetList", jsii.get(self, "fleet"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(
        self,
    ) -> "GoogleGkeonpremBareMetalAdminClusterLoadBalancerOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterLoadBalancerOutputReference", jsii.get(self, "loadBalancer"))

    @builtins.property
    @jsii.member(jsii_name="localName")
    def local_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localName"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceConfig")
    def maintenance_config(
        self,
    ) -> "GoogleGkeonpremBareMetalAdminClusterMaintenanceConfigOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterMaintenanceConfigOutputReference", jsii.get(self, "maintenanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(
        self,
    ) -> "GoogleGkeonpremBareMetalAdminClusterNetworkConfigOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterNetworkConfigOutputReference", jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodeAccessConfig")
    def node_access_config(
        self,
    ) -> "GoogleGkeonpremBareMetalAdminClusterNodeAccessConfigOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterNodeAccessConfigOutputReference", jsii.get(self, "nodeAccessConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfig")
    def node_config(
        self,
    ) -> "GoogleGkeonpremBareMetalAdminClusterNodeConfigOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterNodeConfigOutputReference", jsii.get(self, "nodeConfig"))

    @builtins.property
    @jsii.member(jsii_name="proxy")
    def proxy(self) -> "GoogleGkeonpremBareMetalAdminClusterProxyOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterProxyOutputReference", jsii.get(self, "proxy"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="securityConfig")
    def security_config(
        self,
    ) -> "GoogleGkeonpremBareMetalAdminClusterSecurityConfigOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterSecurityConfigOutputReference", jsii.get(self, "securityConfig"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "GoogleGkeonpremBareMetalAdminClusterStatusList":
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="storage")
    def storage(self) -> "GoogleGkeonpremBareMetalAdminClusterStorageOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterStorageOutputReference", jsii.get(self, "storage"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleGkeonpremBareMetalAdminClusterTimeoutsOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="validationCheck")
    def validation_check(
        self,
    ) -> "GoogleGkeonpremBareMetalAdminClusterValidationCheckList":
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterValidationCheckList", jsii.get(self, "validationCheck"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="bareMetalVersionInput")
    def bare_metal_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bareMetalVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterOperationsInput")
    def cluster_operations_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterClusterOperations"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterClusterOperations"], jsii.get(self, "clusterOperationsInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneInput")
    def control_plane_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterControlPlane"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterControlPlane"], jsii.get(self, "controlPlaneInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerInput")
    def load_balancer_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterLoadBalancer"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterLoadBalancer"], jsii.get(self, "loadBalancerInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceConfigInput")
    def maintenance_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterMaintenanceConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterMaintenanceConfig"], jsii.get(self, "maintenanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigInput")
    def network_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterNetworkConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterNetworkConfig"], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeAccessConfigInput")
    def node_access_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterNodeAccessConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterNodeAccessConfig"], jsii.get(self, "nodeAccessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfigInput")
    def node_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterNodeConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterNodeConfig"], jsii.get(self, "nodeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyInput")
    def proxy_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterProxy"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterProxy"], jsii.get(self, "proxyInput"))

    @builtins.property
    @jsii.member(jsii_name="securityConfigInput")
    def security_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterSecurityConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterSecurityConfig"], jsii.get(self, "securityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="storageInput")
    def storage_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterStorage"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterStorage"], jsii.get(self, "storageInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleGkeonpremBareMetalAdminClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleGkeonpremBareMetalAdminClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08c40377f9e7f5c21b183403f4412bcb91b287a8baa75e0da1b3985f16b952c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bareMetalVersion")
    def bare_metal_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bareMetalVersion"))

    @bare_metal_version.setter
    def bare_metal_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c17398224c6bf4025753c52175daffade0bbba615b769c1e7f9860f88d33c9e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bareMetalVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbacea1ba4f5201c848a76a363a045386dd3a95082c542398ef4bdd4ad14198d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d9a76cc3f364e1537d0f7984d9915b29b1760e9d6f00d2427c158bbcbd2e4c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea60c753ad11041a70fce10784bb15e891a527b0b645ad410e8685f8702d9044)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__732c560e584d276e471db3699efe1072ce68577eae12b4d0864aad1b1370b371)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cef220aeecf12e45e6b6eaccfd03ffe0f098e46a7674877184fd6705c1eca761)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterClusterOperations",
    jsii_struct_bases=[],
    name_mapping={"enable_application_logs": "enableApplicationLogs"},
)
class GoogleGkeonpremBareMetalAdminClusterClusterOperations:
    def __init__(
        self,
        *,
        enable_application_logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_application_logs: Whether collection of application logs/metrics should be enabled (in addition to system logs/metrics). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#enable_application_logs GoogleGkeonpremBareMetalAdminCluster#enable_application_logs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf62f39278a3634a44f4ef436c19bea2fd51a4c5adf4639bd2d19ac78804b7e7)
            check_type(argname="argument enable_application_logs", value=enable_application_logs, expected_type=type_hints["enable_application_logs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_application_logs is not None:
            self._values["enable_application_logs"] = enable_application_logs

    @builtins.property
    def enable_application_logs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether collection of application logs/metrics should be enabled (in addition to system logs/metrics).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#enable_application_logs GoogleGkeonpremBareMetalAdminCluster#enable_application_logs}
        '''
        result = self._values.get("enable_application_logs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterClusterOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalAdminClusterClusterOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterClusterOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb7936b9cfd79876cf0f41c420f21978ecfb5c54e71249f9d77559c6e0f6b7c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableApplicationLogs")
    def reset_enable_application_logs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableApplicationLogs", []))

    @builtins.property
    @jsii.member(jsii_name="enableApplicationLogsInput")
    def enable_application_logs_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableApplicationLogsInput"))

    @builtins.property
    @jsii.member(jsii_name="enableApplicationLogs")
    def enable_application_logs(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableApplicationLogs"))

    @enable_application_logs.setter
    def enable_application_logs(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbf09734ab332d73901a6c8f6f1b00d517b94296d70ac8698eba5a8f1b7fab91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableApplicationLogs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterClusterOperations]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterClusterOperations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterClusterOperations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b4a061a51e7968339c9fd1283957c3a1dc140d861f1940b56ec19846aee5d07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterConfig",
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
        "annotations": "annotations",
        "bare_metal_version": "bareMetalVersion",
        "cluster_operations": "clusterOperations",
        "control_plane": "controlPlane",
        "description": "description",
        "id": "id",
        "load_balancer": "loadBalancer",
        "maintenance_config": "maintenanceConfig",
        "network_config": "networkConfig",
        "node_access_config": "nodeAccessConfig",
        "node_config": "nodeConfig",
        "project": "project",
        "proxy": "proxy",
        "security_config": "securityConfig",
        "storage": "storage",
        "timeouts": "timeouts",
    },
)
class GoogleGkeonpremBareMetalAdminClusterConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bare_metal_version: typing.Optional[builtins.str] = None,
        cluster_operations: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterClusterOperations, typing.Dict[builtins.str, typing.Any]]] = None,
        control_plane: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterControlPlane", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        load_balancer: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterLoadBalancer", typing.Dict[builtins.str, typing.Any]]] = None,
        maintenance_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterMaintenanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        network_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_access_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterNodeAccessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        proxy: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        security_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterSecurityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        storage: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#location GoogleGkeonpremBareMetalAdminCluster#location}
        :param name: The bare metal admin cluster name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#name GoogleGkeonpremBareMetalAdminCluster#name}
        :param annotations: Annotations on the Bare Metal Admin Cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#annotations GoogleGkeonpremBareMetalAdminCluster#annotations}
        :param bare_metal_version: A human readable description of this Bare Metal Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#bare_metal_version GoogleGkeonpremBareMetalAdminCluster#bare_metal_version}
        :param cluster_operations: cluster_operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#cluster_operations GoogleGkeonpremBareMetalAdminCluster#cluster_operations}
        :param control_plane: control_plane block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#control_plane GoogleGkeonpremBareMetalAdminCluster#control_plane}
        :param description: A human readable description of this Bare Metal Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#description GoogleGkeonpremBareMetalAdminCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#id GoogleGkeonpremBareMetalAdminCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#load_balancer GoogleGkeonpremBareMetalAdminCluster#load_balancer}
        :param maintenance_config: maintenance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#maintenance_config GoogleGkeonpremBareMetalAdminCluster#maintenance_config}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#network_config GoogleGkeonpremBareMetalAdminCluster#network_config}
        :param node_access_config: node_access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#node_access_config GoogleGkeonpremBareMetalAdminCluster#node_access_config}
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#node_config GoogleGkeonpremBareMetalAdminCluster#node_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#project GoogleGkeonpremBareMetalAdminCluster#project}.
        :param proxy: proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#proxy GoogleGkeonpremBareMetalAdminCluster#proxy}
        :param security_config: security_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#security_config GoogleGkeonpremBareMetalAdminCluster#security_config}
        :param storage: storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#storage GoogleGkeonpremBareMetalAdminCluster#storage}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#timeouts GoogleGkeonpremBareMetalAdminCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cluster_operations, dict):
            cluster_operations = GoogleGkeonpremBareMetalAdminClusterClusterOperations(**cluster_operations)
        if isinstance(control_plane, dict):
            control_plane = GoogleGkeonpremBareMetalAdminClusterControlPlane(**control_plane)
        if isinstance(load_balancer, dict):
            load_balancer = GoogleGkeonpremBareMetalAdminClusterLoadBalancer(**load_balancer)
        if isinstance(maintenance_config, dict):
            maintenance_config = GoogleGkeonpremBareMetalAdminClusterMaintenanceConfig(**maintenance_config)
        if isinstance(network_config, dict):
            network_config = GoogleGkeonpremBareMetalAdminClusterNetworkConfig(**network_config)
        if isinstance(node_access_config, dict):
            node_access_config = GoogleGkeonpremBareMetalAdminClusterNodeAccessConfig(**node_access_config)
        if isinstance(node_config, dict):
            node_config = GoogleGkeonpremBareMetalAdminClusterNodeConfig(**node_config)
        if isinstance(proxy, dict):
            proxy = GoogleGkeonpremBareMetalAdminClusterProxy(**proxy)
        if isinstance(security_config, dict):
            security_config = GoogleGkeonpremBareMetalAdminClusterSecurityConfig(**security_config)
        if isinstance(storage, dict):
            storage = GoogleGkeonpremBareMetalAdminClusterStorage(**storage)
        if isinstance(timeouts, dict):
            timeouts = GoogleGkeonpremBareMetalAdminClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfff2fa322c17fcc3cd84c0f4b5921865d6698dbbd288b6334c6962bf3189d72)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument bare_metal_version", value=bare_metal_version, expected_type=type_hints["bare_metal_version"])
            check_type(argname="argument cluster_operations", value=cluster_operations, expected_type=type_hints["cluster_operations"])
            check_type(argname="argument control_plane", value=control_plane, expected_type=type_hints["control_plane"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
            check_type(argname="argument maintenance_config", value=maintenance_config, expected_type=type_hints["maintenance_config"])
            check_type(argname="argument network_config", value=network_config, expected_type=type_hints["network_config"])
            check_type(argname="argument node_access_config", value=node_access_config, expected_type=type_hints["node_access_config"])
            check_type(argname="argument node_config", value=node_config, expected_type=type_hints["node_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument proxy", value=proxy, expected_type=type_hints["proxy"])
            check_type(argname="argument security_config", value=security_config, expected_type=type_hints["security_config"])
            check_type(argname="argument storage", value=storage, expected_type=type_hints["storage"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
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
        if annotations is not None:
            self._values["annotations"] = annotations
        if bare_metal_version is not None:
            self._values["bare_metal_version"] = bare_metal_version
        if cluster_operations is not None:
            self._values["cluster_operations"] = cluster_operations
        if control_plane is not None:
            self._values["control_plane"] = control_plane
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if load_balancer is not None:
            self._values["load_balancer"] = load_balancer
        if maintenance_config is not None:
            self._values["maintenance_config"] = maintenance_config
        if network_config is not None:
            self._values["network_config"] = network_config
        if node_access_config is not None:
            self._values["node_access_config"] = node_access_config
        if node_config is not None:
            self._values["node_config"] = node_config
        if project is not None:
            self._values["project"] = project
        if proxy is not None:
            self._values["proxy"] = proxy
        if security_config is not None:
            self._values["security_config"] = security_config
        if storage is not None:
            self._values["storage"] = storage
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#location GoogleGkeonpremBareMetalAdminCluster#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The bare metal admin cluster name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#name GoogleGkeonpremBareMetalAdminCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Annotations on the Bare Metal Admin Cluster.

        This field has the same restrictions as Kubernetes annotations.
        The total size of all keys and values combined is limited to 256k.
        Key can have 2 segments: prefix (optional) and name (required),
        separated by a slash (/).
        Prefix must be a DNS subdomain.
        Name must be 63 characters or less, begin and end with alphanumerics,
        with dashes (-), underscores (_), dots (.), and alphanumerics between.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#annotations GoogleGkeonpremBareMetalAdminCluster#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def bare_metal_version(self) -> typing.Optional[builtins.str]:
        '''A human readable description of this Bare Metal Admin Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#bare_metal_version GoogleGkeonpremBareMetalAdminCluster#bare_metal_version}
        '''
        result = self._values.get("bare_metal_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_operations(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterClusterOperations]:
        '''cluster_operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#cluster_operations GoogleGkeonpremBareMetalAdminCluster#cluster_operations}
        '''
        result = self._values.get("cluster_operations")
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterClusterOperations], result)

    @builtins.property
    def control_plane(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterControlPlane"]:
        '''control_plane block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#control_plane GoogleGkeonpremBareMetalAdminCluster#control_plane}
        '''
        result = self._values.get("control_plane")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterControlPlane"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human readable description of this Bare Metal Admin Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#description GoogleGkeonpremBareMetalAdminCluster#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#id GoogleGkeonpremBareMetalAdminCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterLoadBalancer"]:
        '''load_balancer block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#load_balancer GoogleGkeonpremBareMetalAdminCluster#load_balancer}
        '''
        result = self._values.get("load_balancer")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterLoadBalancer"], result)

    @builtins.property
    def maintenance_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterMaintenanceConfig"]:
        '''maintenance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#maintenance_config GoogleGkeonpremBareMetalAdminCluster#maintenance_config}
        '''
        result = self._values.get("maintenance_config")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterMaintenanceConfig"], result)

    @builtins.property
    def network_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterNetworkConfig"]:
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#network_config GoogleGkeonpremBareMetalAdminCluster#network_config}
        '''
        result = self._values.get("network_config")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterNetworkConfig"], result)

    @builtins.property
    def node_access_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterNodeAccessConfig"]:
        '''node_access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#node_access_config GoogleGkeonpremBareMetalAdminCluster#node_access_config}
        '''
        result = self._values.get("node_access_config")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterNodeAccessConfig"], result)

    @builtins.property
    def node_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterNodeConfig"]:
        '''node_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#node_config GoogleGkeonpremBareMetalAdminCluster#node_config}
        '''
        result = self._values.get("node_config")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterNodeConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#project GoogleGkeonpremBareMetalAdminCluster#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy(self) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterProxy"]:
        '''proxy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#proxy GoogleGkeonpremBareMetalAdminCluster#proxy}
        '''
        result = self._values.get("proxy")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterProxy"], result)

    @builtins.property
    def security_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterSecurityConfig"]:
        '''security_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#security_config GoogleGkeonpremBareMetalAdminCluster#security_config}
        '''
        result = self._values.get("security_config")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterSecurityConfig"], result)

    @builtins.property
    def storage(self) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterStorage"]:
        '''storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#storage GoogleGkeonpremBareMetalAdminCluster#storage}
        '''
        result = self._values.get("storage")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterStorage"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#timeouts GoogleGkeonpremBareMetalAdminCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterControlPlane",
    jsii_struct_bases=[],
    name_mapping={
        "control_plane_node_pool_config": "controlPlaneNodePoolConfig",
        "api_server_args": "apiServerArgs",
    },
)
class GoogleGkeonpremBareMetalAdminClusterControlPlane:
    def __init__(
        self,
        *,
        control_plane_node_pool_config: typing.Union["GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig", typing.Dict[builtins.str, typing.Any]],
        api_server_args: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param control_plane_node_pool_config: control_plane_node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#control_plane_node_pool_config GoogleGkeonpremBareMetalAdminCluster#control_plane_node_pool_config}
        :param api_server_args: api_server_args block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#api_server_args GoogleGkeonpremBareMetalAdminCluster#api_server_args}
        '''
        if isinstance(control_plane_node_pool_config, dict):
            control_plane_node_pool_config = GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig(**control_plane_node_pool_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5a54391e4d5ce3404b953979da9873dc3dc6555dd23dab3f0c59682a04b4b5a)
            check_type(argname="argument control_plane_node_pool_config", value=control_plane_node_pool_config, expected_type=type_hints["control_plane_node_pool_config"])
            check_type(argname="argument api_server_args", value=api_server_args, expected_type=type_hints["api_server_args"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "control_plane_node_pool_config": control_plane_node_pool_config,
        }
        if api_server_args is not None:
            self._values["api_server_args"] = api_server_args

    @builtins.property
    def control_plane_node_pool_config(
        self,
    ) -> "GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig":
        '''control_plane_node_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#control_plane_node_pool_config GoogleGkeonpremBareMetalAdminCluster#control_plane_node_pool_config}
        '''
        result = self._values.get("control_plane_node_pool_config")
        assert result is not None, "Required property 'control_plane_node_pool_config' is missing"
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig", result)

    @builtins.property
    def api_server_args(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgs"]]]:
        '''api_server_args block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#api_server_args GoogleGkeonpremBareMetalAdminCluster#api_server_args}
        '''
        result = self._values.get("api_server_args")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgs"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterControlPlane(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgs",
    jsii_struct_bases=[],
    name_mapping={"argument": "argument", "value": "value"},
)
class GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgs:
    def __init__(self, *, argument: builtins.str, value: builtins.str) -> None:
        '''
        :param argument: The argument name as it appears on the API Server command line please make sure to remove the leading dashes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#argument GoogleGkeonpremBareMetalAdminCluster#argument}
        :param value: The value of the arg as it will be passed to the API Server command line. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#value GoogleGkeonpremBareMetalAdminCluster#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b9366e52aeec1fe5f75cff0a859ea3a28c8ec24e2b8e47a15d44a05add7d0f2)
            check_type(argname="argument argument", value=argument, expected_type=type_hints["argument"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "argument": argument,
            "value": value,
        }

    @builtins.property
    def argument(self) -> builtins.str:
        '''The argument name as it appears on the API Server command line please make sure to remove the leading dashes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#argument GoogleGkeonpremBareMetalAdminCluster#argument}
        '''
        result = self._values.get("argument")
        assert result is not None, "Required property 'argument' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value of the arg as it will be passed to the API Server command line.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#value GoogleGkeonpremBareMetalAdminCluster#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__204ce0623efbd7df4473aad5d34a51bf2d34c7c8736127c54c630d7c7c8364ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19552d8584915cb628953a59a7df5dd3d963647f2f9dcaba677d35544dac657b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f6214d73c9419fb65cc79b290b7c0e6d374a3675e8e2db9b07a2152f1db2ee3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7ddbf5c44f781e72cf6ae03e6939f96952f9ca09f85b5784fc16636ee2a5662)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14b7fa6dd954f46a3c05f8ba66b67adf96e941e5135062d688b57e775fd9c075)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__902fe714fe86ed22031a7c224501874c76149621c0bd1f8cb669e8706d70984f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d4e8f2411f3ce7f381df9c91d07138539dc61888224bc64130a684c9f668243)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="argumentInput")
    def argument_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "argumentInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="argument")
    def argument(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "argument"))

    @argument.setter
    def argument(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98ca5f867cfd02578ab7bf97e52c550e99afadfc5763bd2c16fd10f149702975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "argument", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__122023ffae63c30a28a403e99981d1179fed1b955a2f79b65e21143f732042dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25773acfe53ddee466493c965d77bdee985162d23c72cb173cf27a28581698ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig",
    jsii_struct_bases=[],
    name_mapping={"node_pool_config": "nodePoolConfig"},
)
class GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig:
    def __init__(
        self,
        *,
        node_pool_config: typing.Union["GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param node_pool_config: node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#node_pool_config GoogleGkeonpremBareMetalAdminCluster#node_pool_config}
        '''
        if isinstance(node_pool_config, dict):
            node_pool_config = GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig(**node_pool_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cca7a99e4b1941ea0d0f137a56fed7a01b6538e5ce36848758d98aa48152b8a8)
            check_type(argname="argument node_pool_config", value=node_pool_config, expected_type=type_hints["node_pool_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "node_pool_config": node_pool_config,
        }

    @builtins.property
    def node_pool_config(
        self,
    ) -> "GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig":
        '''node_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#node_pool_config GoogleGkeonpremBareMetalAdminCluster#node_pool_config}
        '''
        result = self._values.get("node_pool_config")
        assert result is not None, "Required property 'node_pool_config' is missing"
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig",
    jsii_struct_bases=[],
    name_mapping={
        "labels": "labels",
        "node_configs": "nodeConfigs",
        "operating_system": "operatingSystem",
        "taints": "taints",
    },
)
class GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operating_system: typing.Optional[builtins.str] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#labels GoogleGkeonpremBareMetalAdminCluster#labels}
        :param node_configs: node_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#node_configs GoogleGkeonpremBareMetalAdminCluster#node_configs}
        :param operating_system: Specifies the nodes operating system (default: LINUX). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#operating_system GoogleGkeonpremBareMetalAdminCluster#operating_system}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#taints GoogleGkeonpremBareMetalAdminCluster#taints}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fbeaa49f936a244448b2a4b249c8be39173c6b148abd8daef40f17152852875)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument node_configs", value=node_configs, expected_type=type_hints["node_configs"])
            check_type(argname="argument operating_system", value=operating_system, expected_type=type_hints["operating_system"])
            check_type(argname="argument taints", value=taints, expected_type=type_hints["taints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if labels is not None:
            self._values["labels"] = labels
        if node_configs is not None:
            self._values["node_configs"] = node_configs
        if operating_system is not None:
            self._values["operating_system"] = operating_system
        if taints is not None:
            self._values["taints"] = taints

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The map of Kubernetes labels (key/value pairs) to be applied to each node.

        These will added in addition to any default label(s)
        that Kubernetes may apply to the node. In case of conflict in
        label keys, the applied set may differ depending on the Kubernetes
        version -- it's best to assume the behavior is undefined and
        conflicts should be avoided. For more information, including usage
        and the valid values, see:

        - http://kubernetes.io/v1.1/docs/user-guide/labels.html
          An object containing a list of "key": value pairs.
          For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#labels GoogleGkeonpremBareMetalAdminCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def node_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs"]]]:
        '''node_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#node_configs GoogleGkeonpremBareMetalAdminCluster#node_configs}
        '''
        result = self._values.get("node_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs"]]], result)

    @builtins.property
    def operating_system(self) -> typing.Optional[builtins.str]:
        '''Specifies the nodes operating system (default: LINUX).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#operating_system GoogleGkeonpremBareMetalAdminCluster#operating_system}
        '''
        result = self._values.get("operating_system")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def taints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints"]]]:
        '''taints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#taints GoogleGkeonpremBareMetalAdminCluster#taints}
        '''
        result = self._values.get("taints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels", "node_ip": "nodeIp"},
)
class GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_ip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#labels GoogleGkeonpremBareMetalAdminCluster#labels}
        :param node_ip: The default IPv4 address for SSH access and Kubernetes node. Example: 192.168.0.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#node_ip GoogleGkeonpremBareMetalAdminCluster#node_ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__913fe24b1c8dfa4fdde5724ade77aaae733c0573fe20e80ae181db9bdfe5c2ea)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument node_ip", value=node_ip, expected_type=type_hints["node_ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if labels is not None:
            self._values["labels"] = labels
        if node_ip is not None:
            self._values["node_ip"] = node_ip

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The map of Kubernetes labels (key/value pairs) to be applied to each node.

        These will added in addition to any default label(s)
        that Kubernetes may apply to the node. In case of conflict in
        label keys, the applied set may differ depending on the Kubernetes
        version -- it's best to assume the behavior is undefined and
        conflicts should be avoided. For more information, including usage
        and the valid values, see:

        - http://kubernetes.io/v1.1/docs/user-guide/labels.html
          An object containing a list of "key": value pairs.
          For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#labels GoogleGkeonpremBareMetalAdminCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def node_ip(self) -> typing.Optional[builtins.str]:
        '''The default IPv4 address for SSH access and Kubernetes node. Example: 192.168.0.1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#node_ip GoogleGkeonpremBareMetalAdminCluster#node_ip}
        '''
        result = self._values.get("node_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5058cff1714545d8fa8df8f6fc54e8e06e7d7e9c42bad16c04dd1bb751201f3d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb06f8b79952c5239febd4f58a3b5e176bb6c77d8b511383f9a4d8904e3bdeb5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bd6e7fae5f5580ab8fd793b3e24e7416c4cedcd6d2e586df4c2afa2bbadb7c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fea92e5e464297f7db92243a44875cd1a9ef240f6dd1aa815dcc1e5ec7eef16)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09451be2ad6095bc699bb83ada1268e00d29617396cdb50f07215d21e9502f71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51390e75e6a70f8d3d4fc5d95c1789103b102a3fb928fd24dc6984c4151431de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86f62022b1fad523af549c9ee1eb59595b47293541c21f12ce848c424c967bce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetNodeIp")
    def reset_node_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeIp", []))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeIpInput")
    def node_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeIpInput"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9d7589466042f57bad04858e83d5259aaffbe80bc343138739ce8d3bfc90817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeIp")
    def node_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeIp"))

    @node_ip.setter
    def node_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ddd3d86f0948572085a30cb624ce43dcac0e7aa2c81a9a2eb672eab6b752be2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c743b4484ce64932bb9b039156e158b60e11adad1b350f3a5aba097b85cc6514)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d59446c0dff9027cc024e72a8839a18c3f97fe2d4adb889be7196cc07182929)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodeConfigs")
    def put_node_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af71e3fa9c395e49510d16791d857bfdb73222bb7687eefa4e8e32560cf70206)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeConfigs", [value]))

    @jsii.member(jsii_name="putTaints")
    def put_taints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40fa05b77f28cd3510a9d7cfbb86d491f52296043a29186d6de7b60e6985cf54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTaints", [value]))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetNodeConfigs")
    def reset_node_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeConfigs", []))

    @jsii.member(jsii_name="resetOperatingSystem")
    def reset_operating_system(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperatingSystem", []))

    @jsii.member(jsii_name="resetTaints")
    def reset_taints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaints", []))

    @builtins.property
    @jsii.member(jsii_name="nodeConfigs")
    def node_configs(
        self,
    ) -> GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsList:
        return typing.cast(GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsList, jsii.get(self, "nodeConfigs"))

    @builtins.property
    @jsii.member(jsii_name="taints")
    def taints(
        self,
    ) -> "GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsList":
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsList", jsii.get(self, "taints"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfigsInput")
    def node_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]], jsii.get(self, "nodeConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="operatingSystemInput")
    def operating_system_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatingSystemInput"))

    @builtins.property
    @jsii.member(jsii_name="taintsInput")
    def taints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints"]]], jsii.get(self, "taintsInput"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7b8347f70972f7e1a4b082cecaee8c5bb6170244568bd9c60d9d47d9c32a97e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operatingSystem")
    def operating_system(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operatingSystem"))

    @operating_system.setter
    def operating_system(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eece15c53dab21f2404492006dc8dc5da5c925cdb26c702f189c1a42617098ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operatingSystem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c500b14140c5157237b5b4a77ddeee2a1f4abd5f65ab1167f61f99699c5fdc89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints",
    jsii_struct_bases=[],
    name_mapping={"effect": "effect", "key": "key", "value": "value"},
)
class GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints:
    def __init__(
        self,
        *,
        effect: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param effect: Specifies the nodes operating system (default: LINUX). Possible values: ["EFFECT_UNSPECIFIED", "PREFER_NO_SCHEDULE", "NO_EXECUTE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#effect GoogleGkeonpremBareMetalAdminCluster#effect}
        :param key: Key associated with the effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#key GoogleGkeonpremBareMetalAdminCluster#key}
        :param value: Value associated with the effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#value GoogleGkeonpremBareMetalAdminCluster#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8f8eba7cfcf56e0b39181b301d3d01429f61a6e1371be3cbea6d1aa4171ba9b)
            check_type(argname="argument effect", value=effect, expected_type=type_hints["effect"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if effect is not None:
            self._values["effect"] = effect
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def effect(self) -> typing.Optional[builtins.str]:
        '''Specifies the nodes operating system (default: LINUX). Possible values: ["EFFECT_UNSPECIFIED", "PREFER_NO_SCHEDULE", "NO_EXECUTE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#effect GoogleGkeonpremBareMetalAdminCluster#effect}
        '''
        result = self._values.get("effect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Key associated with the effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#key GoogleGkeonpremBareMetalAdminCluster#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value associated with the effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#value GoogleGkeonpremBareMetalAdminCluster#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ff6a186c1df1153d8223a7e2f0f2926e56a74bcf06c1fe554b0304b68d55191)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29a50d159724ce6a8276d600f9386ad7f0338dedfe8f82dcc72e0e2f2a3b66dd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__088507ad230c4808ef9b2b5e1f84b3852d35704eef4e689a4f31dfb51eab73e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0eb73489c79a20357ca79f729c4c7d627bbb91bae9b51e6cd6abff4eaf5dbe7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1644a451fc7a05e35bed81630ed5d4a6ddbda377ff1386200847daf03dcb259)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bfd43d13f3c6fdb70a3c59a7526bbe727fc6910a0e4f2bb49c8b2304ca34051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ac7863dbe15473c7bd0ad792caffd29b111236ba99b22ec8e24a59f125a14c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEffect")
    def reset_effect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEffect", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__932845fe10e1ce3ff5b4ec22060aba3029d693c6b382a2a5b083fc15dcc2d6a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83714010060bf2fe1f2a21c7249e4b6d6be74db279ee2bc0261869319c7bb24d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9de719bf0ec219dd75e484285366d4f9c539d2d54b4b90966ba02c504a32a77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e83cfb989ed60b283fc510a6f2bef35b50e7ddeddc33793cd2bc0f2a1ac97be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0c8441a97640654eaa774c820e313c0c7c7b866f171f592f111355805538374)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodePoolConfig")
    def put_node_pool_config(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
        operating_system: typing.Optional[builtins.str] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#labels GoogleGkeonpremBareMetalAdminCluster#labels}
        :param node_configs: node_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#node_configs GoogleGkeonpremBareMetalAdminCluster#node_configs}
        :param operating_system: Specifies the nodes operating system (default: LINUX). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#operating_system GoogleGkeonpremBareMetalAdminCluster#operating_system}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#taints GoogleGkeonpremBareMetalAdminCluster#taints}
        '''
        value = GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig(
            labels=labels,
            node_configs=node_configs,
            operating_system=operating_system,
            taints=taints,
        )

        return typing.cast(None, jsii.invoke(self, "putNodePoolConfig", [value]))

    @builtins.property
    @jsii.member(jsii_name="nodePoolConfig")
    def node_pool_config(
        self,
    ) -> GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigOutputReference, jsii.get(self, "nodePoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodePoolConfigInput")
    def node_pool_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig], jsii.get(self, "nodePoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__008d6e8ce5b5a2fd9cf33b7f3190d43b98c36abf741a13f6a3a9a51b95f12a08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalAdminClusterControlPlaneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterControlPlaneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a63615deab81ff907445314cd39eb9ecc406d0280fd44f40f1547bab248a8da2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApiServerArgs")
    def put_api_server_args(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab26cf1b05c990bba1d4a96d873604e0cef2035af36855b0422e8363acc8167)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putApiServerArgs", [value]))

    @jsii.member(jsii_name="putControlPlaneNodePoolConfig")
    def put_control_plane_node_pool_config(
        self,
        *,
        node_pool_config: typing.Union[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param node_pool_config: node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#node_pool_config GoogleGkeonpremBareMetalAdminCluster#node_pool_config}
        '''
        value = GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig(
            node_pool_config=node_pool_config
        )

        return typing.cast(None, jsii.invoke(self, "putControlPlaneNodePoolConfig", [value]))

    @jsii.member(jsii_name="resetApiServerArgs")
    def reset_api_server_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiServerArgs", []))

    @builtins.property
    @jsii.member(jsii_name="apiServerArgs")
    def api_server_args(
        self,
    ) -> GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgsList:
        return typing.cast(GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgsList, jsii.get(self, "apiServerArgs"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneNodePoolConfig")
    def control_plane_node_pool_config(
        self,
    ) -> GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigOutputReference, jsii.get(self, "controlPlaneNodePoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="apiServerArgsInput")
    def api_server_args_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgs]]], jsii.get(self, "apiServerArgsInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneNodePoolConfigInput")
    def control_plane_node_pool_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig], jsii.get(self, "controlPlaneNodePoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterControlPlane]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterControlPlane], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterControlPlane],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e07a0f90a477502f9f7c610e8cad80c3c70b65174cae801c98c02259d8e60622)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterFleet",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremBareMetalAdminClusterFleet:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterFleet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalAdminClusterFleetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterFleetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aff6665c50a5951b1eb5e1563086af96e5fecf820c11a6641ac9ce3e4ed9b2d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalAdminClusterFleetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__183f13f629984045150e4fbec594924594ea2e110cc2f44b16438f7d74a98c8c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterFleetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81ad36d2e205f4c4f9fae960a420cbe85c3d13eade60c61c9b0eb8f1b60d2cd4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d8cf312570ecf07d0d2aaddffbd58b9636f8aaa3f726c5e7eabd5d0ca72a651)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4807a71c0d842925c188fb1af27408d70397a448eb2f7e65a94b858501ea79f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalAdminClusterFleetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterFleetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e4259a864b65919171e2f9dc98e1270d901a689a4484bb251411f373120f3e1)
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
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterFleet]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterFleet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterFleet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b0c26f2341dcb439ec00d1125bd71dc5135b08faadeb71717f329b95fc1789d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterLoadBalancer",
    jsii_struct_bases=[],
    name_mapping={
        "port_config": "portConfig",
        "vip_config": "vipConfig",
        "manual_lb_config": "manualLbConfig",
    },
)
class GoogleGkeonpremBareMetalAdminClusterLoadBalancer:
    def __init__(
        self,
        *,
        port_config: typing.Union["GoogleGkeonpremBareMetalAdminClusterLoadBalancerPortConfig", typing.Dict[builtins.str, typing.Any]],
        vip_config: typing.Union["GoogleGkeonpremBareMetalAdminClusterLoadBalancerVipConfig", typing.Dict[builtins.str, typing.Any]],
        manual_lb_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param port_config: port_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#port_config GoogleGkeonpremBareMetalAdminCluster#port_config}
        :param vip_config: vip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#vip_config GoogleGkeonpremBareMetalAdminCluster#vip_config}
        :param manual_lb_config: manual_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#manual_lb_config GoogleGkeonpremBareMetalAdminCluster#manual_lb_config}
        '''
        if isinstance(port_config, dict):
            port_config = GoogleGkeonpremBareMetalAdminClusterLoadBalancerPortConfig(**port_config)
        if isinstance(vip_config, dict):
            vip_config = GoogleGkeonpremBareMetalAdminClusterLoadBalancerVipConfig(**vip_config)
        if isinstance(manual_lb_config, dict):
            manual_lb_config = GoogleGkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig(**manual_lb_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4299278fa16f325f368ca3daa09ce5d3a09e1c5d07ad70f17553efd28a2aad3)
            check_type(argname="argument port_config", value=port_config, expected_type=type_hints["port_config"])
            check_type(argname="argument vip_config", value=vip_config, expected_type=type_hints["vip_config"])
            check_type(argname="argument manual_lb_config", value=manual_lb_config, expected_type=type_hints["manual_lb_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port_config": port_config,
            "vip_config": vip_config,
        }
        if manual_lb_config is not None:
            self._values["manual_lb_config"] = manual_lb_config

    @builtins.property
    def port_config(
        self,
    ) -> "GoogleGkeonpremBareMetalAdminClusterLoadBalancerPortConfig":
        '''port_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#port_config GoogleGkeonpremBareMetalAdminCluster#port_config}
        '''
        result = self._values.get("port_config")
        assert result is not None, "Required property 'port_config' is missing"
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterLoadBalancerPortConfig", result)

    @builtins.property
    def vip_config(self) -> "GoogleGkeonpremBareMetalAdminClusterLoadBalancerVipConfig":
        '''vip_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#vip_config GoogleGkeonpremBareMetalAdminCluster#vip_config}
        '''
        result = self._values.get("vip_config")
        assert result is not None, "Required property 'vip_config' is missing"
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterLoadBalancerVipConfig", result)

    @builtins.property
    def manual_lb_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig"]:
        '''manual_lb_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#manual_lb_config GoogleGkeonpremBareMetalAdminCluster#manual_lb_config}
        '''
        result = self._values.get("manual_lb_config")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterLoadBalancer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleGkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether manual load balancing is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#enabled GoogleGkeonpremBareMetalAdminCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87f629f37164f4b63ad7fef04b10389697487bd01dac2c98bc142de3447de4e1)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether manual load balancing is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#enabled GoogleGkeonpremBareMetalAdminCluster#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalAdminClusterLoadBalancerManualLbConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterLoadBalancerManualLbConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88b1cbcaf9e7b2aeb7c5a8849971d8d1b02defa9042c42bae0dcf4982228675e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba613279b93ec62f3e3b397b75b2669240411721bce7594930a7cb4c66a1860f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdb74c1b034c037033ccb5a420e6cdc893ff9a3879f26f46c1d20f8262a92b0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalAdminClusterLoadBalancerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterLoadBalancerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7873e23dfb78ef3a3acb7742e0b8baba6595d9a91aaae024a0ec73cd48e73126)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putManualLbConfig")
    def put_manual_lb_config(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether manual load balancing is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#enabled GoogleGkeonpremBareMetalAdminCluster#enabled}
        '''
        value = GoogleGkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putManualLbConfig", [value]))

    @jsii.member(jsii_name="putPortConfig")
    def put_port_config(self, *, control_plane_load_balancer_port: jsii.Number) -> None:
        '''
        :param control_plane_load_balancer_port: The port that control plane hosted load balancers will listen on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#control_plane_load_balancer_port GoogleGkeonpremBareMetalAdminCluster#control_plane_load_balancer_port}
        '''
        value = GoogleGkeonpremBareMetalAdminClusterLoadBalancerPortConfig(
            control_plane_load_balancer_port=control_plane_load_balancer_port
        )

        return typing.cast(None, jsii.invoke(self, "putPortConfig", [value]))

    @jsii.member(jsii_name="putVipConfig")
    def put_vip_config(self, *, control_plane_vip: builtins.str) -> None:
        '''
        :param control_plane_vip: The VIP which you previously set aside for the Kubernetes API of this Bare Metal Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#control_plane_vip GoogleGkeonpremBareMetalAdminCluster#control_plane_vip}
        '''
        value = GoogleGkeonpremBareMetalAdminClusterLoadBalancerVipConfig(
            control_plane_vip=control_plane_vip
        )

        return typing.cast(None, jsii.invoke(self, "putVipConfig", [value]))

    @jsii.member(jsii_name="resetManualLbConfig")
    def reset_manual_lb_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManualLbConfig", []))

    @builtins.property
    @jsii.member(jsii_name="manualLbConfig")
    def manual_lb_config(
        self,
    ) -> GoogleGkeonpremBareMetalAdminClusterLoadBalancerManualLbConfigOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalAdminClusterLoadBalancerManualLbConfigOutputReference, jsii.get(self, "manualLbConfig"))

    @builtins.property
    @jsii.member(jsii_name="portConfig")
    def port_config(
        self,
    ) -> "GoogleGkeonpremBareMetalAdminClusterLoadBalancerPortConfigOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterLoadBalancerPortConfigOutputReference", jsii.get(self, "portConfig"))

    @builtins.property
    @jsii.member(jsii_name="vipConfig")
    def vip_config(
        self,
    ) -> "GoogleGkeonpremBareMetalAdminClusterLoadBalancerVipConfigOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterLoadBalancerVipConfigOutputReference", jsii.get(self, "vipConfig"))

    @builtins.property
    @jsii.member(jsii_name="manualLbConfigInput")
    def manual_lb_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig], jsii.get(self, "manualLbConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="portConfigInput")
    def port_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterLoadBalancerPortConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterLoadBalancerPortConfig"], jsii.get(self, "portConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="vipConfigInput")
    def vip_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterLoadBalancerVipConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterLoadBalancerVipConfig"], jsii.get(self, "vipConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterLoadBalancer]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterLoadBalancer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterLoadBalancer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86b4bc038058c725d16cee462f68634efc5e17089b3e37ad85a853b7d16f7973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterLoadBalancerPortConfig",
    jsii_struct_bases=[],
    name_mapping={"control_plane_load_balancer_port": "controlPlaneLoadBalancerPort"},
)
class GoogleGkeonpremBareMetalAdminClusterLoadBalancerPortConfig:
    def __init__(self, *, control_plane_load_balancer_port: jsii.Number) -> None:
        '''
        :param control_plane_load_balancer_port: The port that control plane hosted load balancers will listen on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#control_plane_load_balancer_port GoogleGkeonpremBareMetalAdminCluster#control_plane_load_balancer_port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffa13121bf3e0078406c876bb08365d2d8f50bc8450f653ec8fa00ca4bcf7d51)
            check_type(argname="argument control_plane_load_balancer_port", value=control_plane_load_balancer_port, expected_type=type_hints["control_plane_load_balancer_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "control_plane_load_balancer_port": control_plane_load_balancer_port,
        }

    @builtins.property
    def control_plane_load_balancer_port(self) -> jsii.Number:
        '''The port that control plane hosted load balancers will listen on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#control_plane_load_balancer_port GoogleGkeonpremBareMetalAdminCluster#control_plane_load_balancer_port}
        '''
        result = self._values.get("control_plane_load_balancer_port")
        assert result is not None, "Required property 'control_plane_load_balancer_port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterLoadBalancerPortConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalAdminClusterLoadBalancerPortConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterLoadBalancerPortConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__772bfb73c1dc10ed8ee5d0cd2b88122e4b53a21e799770c47b044a6211be9f0b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="controlPlaneLoadBalancerPortInput")
    def control_plane_load_balancer_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "controlPlaneLoadBalancerPortInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneLoadBalancerPort")
    def control_plane_load_balancer_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "controlPlaneLoadBalancerPort"))

    @control_plane_load_balancer_port.setter
    def control_plane_load_balancer_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd8ef628a24134dbbc16b94e701801798e7c97e8190d443389f971d2894ddc3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneLoadBalancerPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterLoadBalancerPortConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterLoadBalancerPortConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterLoadBalancerPortConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dae42ae730caa3c8512c1d3ea4342a8760d3c7988324ab4186d3010cbbd0b6d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterLoadBalancerVipConfig",
    jsii_struct_bases=[],
    name_mapping={"control_plane_vip": "controlPlaneVip"},
)
class GoogleGkeonpremBareMetalAdminClusterLoadBalancerVipConfig:
    def __init__(self, *, control_plane_vip: builtins.str) -> None:
        '''
        :param control_plane_vip: The VIP which you previously set aside for the Kubernetes API of this Bare Metal Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#control_plane_vip GoogleGkeonpremBareMetalAdminCluster#control_plane_vip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d32eb209e60af015e3de61b1902bf71f784aa68fa79ad4a0d7880b7010fdbd99)
            check_type(argname="argument control_plane_vip", value=control_plane_vip, expected_type=type_hints["control_plane_vip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "control_plane_vip": control_plane_vip,
        }

    @builtins.property
    def control_plane_vip(self) -> builtins.str:
        '''The VIP which you previously set aside for the Kubernetes API of this Bare Metal Admin Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#control_plane_vip GoogleGkeonpremBareMetalAdminCluster#control_plane_vip}
        '''
        result = self._values.get("control_plane_vip")
        assert result is not None, "Required property 'control_plane_vip' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterLoadBalancerVipConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalAdminClusterLoadBalancerVipConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterLoadBalancerVipConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26cc5cd3f38d4c5926cea94005df8411b9b2b2262ac4a60868dffb74813eb5d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="controlPlaneVipInput")
    def control_plane_vip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "controlPlaneVipInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneVip")
    def control_plane_vip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "controlPlaneVip"))

    @control_plane_vip.setter
    def control_plane_vip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98eaaba22f12d84ae08b5f0de0b78240d53250c8e8df256073669a25911e7395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneVip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterLoadBalancerVipConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterLoadBalancerVipConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterLoadBalancerVipConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef54fa569d8e038fb2606b47d578d5268ed094ead88b53c2a4585ab7214c6124)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterMaintenanceConfig",
    jsii_struct_bases=[],
    name_mapping={"maintenance_address_cidr_blocks": "maintenanceAddressCidrBlocks"},
)
class GoogleGkeonpremBareMetalAdminClusterMaintenanceConfig:
    def __init__(
        self,
        *,
        maintenance_address_cidr_blocks: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param maintenance_address_cidr_blocks: All IPv4 address from these ranges will be placed into maintenance mode. Nodes in maintenance mode will be cordoned and drained. When both of these are true, the "baremetal.cluster.gke.io/maintenance" annotation will be set on the node resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#maintenance_address_cidr_blocks GoogleGkeonpremBareMetalAdminCluster#maintenance_address_cidr_blocks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b09dae7657ac322ed54184395da17bbe0299cd9990fcf9e881282eff659722b)
            check_type(argname="argument maintenance_address_cidr_blocks", value=maintenance_address_cidr_blocks, expected_type=type_hints["maintenance_address_cidr_blocks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "maintenance_address_cidr_blocks": maintenance_address_cidr_blocks,
        }

    @builtins.property
    def maintenance_address_cidr_blocks(self) -> typing.List[builtins.str]:
        '''All IPv4 address from these ranges will be placed into maintenance mode.

        Nodes in maintenance mode will be cordoned and drained. When both of these
        are true, the "baremetal.cluster.gke.io/maintenance" annotation will be set
        on the node resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#maintenance_address_cidr_blocks GoogleGkeonpremBareMetalAdminCluster#maintenance_address_cidr_blocks}
        '''
        result = self._values.get("maintenance_address_cidr_blocks")
        assert result is not None, "Required property 'maintenance_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterMaintenanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalAdminClusterMaintenanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterMaintenanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fa4b9323ecd5949063714199c82a1cb13a875c53fb02fdfe19a0eeea3b92f9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="maintenanceAddressCidrBlocksInput")
    def maintenance_address_cidr_blocks_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "maintenanceAddressCidrBlocksInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceAddressCidrBlocks")
    def maintenance_address_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "maintenanceAddressCidrBlocks"))

    @maintenance_address_cidr_blocks.setter
    def maintenance_address_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a6fbab2c5c4130526b27b2081182af5751fdee06f41c27e2a12f8418ae8f3b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterMaintenanceConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterMaintenanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterMaintenanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ba0d622e437c10911b2a389cdb69fb503f13d8b93c3fab33d9503919e0e8be0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={"island_mode_cidr": "islandModeCidr"},
)
class GoogleGkeonpremBareMetalAdminClusterNetworkConfig:
    def __init__(
        self,
        *,
        island_mode_cidr: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param island_mode_cidr: island_mode_cidr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#island_mode_cidr GoogleGkeonpremBareMetalAdminCluster#island_mode_cidr}
        '''
        if isinstance(island_mode_cidr, dict):
            island_mode_cidr = GoogleGkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr(**island_mode_cidr)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0dd566f2ae27cbb67c3de103fef083516b30dba6a0c4a9468b6a2b98e335557)
            check_type(argname="argument island_mode_cidr", value=island_mode_cidr, expected_type=type_hints["island_mode_cidr"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if island_mode_cidr is not None:
            self._values["island_mode_cidr"] = island_mode_cidr

    @builtins.property
    def island_mode_cidr(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr"]:
        '''island_mode_cidr block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#island_mode_cidr GoogleGkeonpremBareMetalAdminCluster#island_mode_cidr}
        '''
        result = self._values.get("island_mode_cidr")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr",
    jsii_struct_bases=[],
    name_mapping={
        "pod_address_cidr_blocks": "podAddressCidrBlocks",
        "service_address_cidr_blocks": "serviceAddressCidrBlocks",
    },
)
class GoogleGkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr:
    def __init__(
        self,
        *,
        pod_address_cidr_blocks: typing.Sequence[builtins.str],
        service_address_cidr_blocks: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param pod_address_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these ranges. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#pod_address_cidr_blocks GoogleGkeonpremBareMetalAdminCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these ranges. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#service_address_cidr_blocks GoogleGkeonpremBareMetalAdminCluster#service_address_cidr_blocks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b7a44b4c112243cb95ca88c3fa5a964d350bde2f94d7aa63a309e3c4b15c4fe)
            check_type(argname="argument pod_address_cidr_blocks", value=pod_address_cidr_blocks, expected_type=type_hints["pod_address_cidr_blocks"])
            check_type(argname="argument service_address_cidr_blocks", value=service_address_cidr_blocks, expected_type=type_hints["service_address_cidr_blocks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pod_address_cidr_blocks": pod_address_cidr_blocks,
            "service_address_cidr_blocks": service_address_cidr_blocks,
        }

    @builtins.property
    def pod_address_cidr_blocks(self) -> typing.List[builtins.str]:
        '''All pods in the cluster are assigned an RFC1918 IPv4 address from these ranges.

        This field cannot be changed after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#pod_address_cidr_blocks GoogleGkeonpremBareMetalAdminCluster#pod_address_cidr_blocks}
        '''
        result = self._values.get("pod_address_cidr_blocks")
        assert result is not None, "Required property 'pod_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        '''All services in the cluster are assigned an RFC1918 IPv4 address from these ranges.

        This field cannot be changed after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#service_address_cidr_blocks GoogleGkeonpremBareMetalAdminCluster#service_address_cidr_blocks}
        '''
        result = self._values.get("service_address_cidr_blocks")
        assert result is not None, "Required property 'service_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidrOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidrOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3604158e52cd6eed2af87c607baee11998d53e36cb9434ad6a38300e41f355e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
    @jsii.member(jsii_name="podAddressCidrBlocks")
    def pod_address_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "podAddressCidrBlocks"))

    @pod_address_cidr_blocks.setter
    def pod_address_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65a5352bafe191d55aa78f7c13bc0df047e34d910170930f8bd1f5e55907815c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAddressCidrBlocks")
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceAddressCidrBlocks"))

    @service_address_cidr_blocks.setter
    def service_address_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85e7f7cec6c6e0b80d1565e2ccac0fe354e4a77b2aa454ae1b431e73e5fb0e95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a734ac2cd76c43ea7fcfe66e5baec36a801502c1dd87b4fdba63661750154c91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalAdminClusterNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4b21ff319cf1a6c5c762fb481f28d9b32c6e0143fe2447757a99a52c881f79e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIslandModeCidr")
    def put_island_mode_cidr(
        self,
        *,
        pod_address_cidr_blocks: typing.Sequence[builtins.str],
        service_address_cidr_blocks: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param pod_address_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these ranges. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#pod_address_cidr_blocks GoogleGkeonpremBareMetalAdminCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these ranges. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#service_address_cidr_blocks GoogleGkeonpremBareMetalAdminCluster#service_address_cidr_blocks}
        '''
        value = GoogleGkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr(
            pod_address_cidr_blocks=pod_address_cidr_blocks,
            service_address_cidr_blocks=service_address_cidr_blocks,
        )

        return typing.cast(None, jsii.invoke(self, "putIslandModeCidr", [value]))

    @jsii.member(jsii_name="resetIslandModeCidr")
    def reset_island_mode_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIslandModeCidr", []))

    @builtins.property
    @jsii.member(jsii_name="islandModeCidr")
    def island_mode_cidr(
        self,
    ) -> GoogleGkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidrOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidrOutputReference, jsii.get(self, "islandModeCidr"))

    @builtins.property
    @jsii.member(jsii_name="islandModeCidrInput")
    def island_mode_cidr_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr], jsii.get(self, "islandModeCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterNetworkConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__194e7be5f3861f6c6f09b2ea7b94d4dba491f6f712c5765a91da40179318cb24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterNodeAccessConfig",
    jsii_struct_bases=[],
    name_mapping={"login_user": "loginUser"},
)
class GoogleGkeonpremBareMetalAdminClusterNodeAccessConfig:
    def __init__(self, *, login_user: typing.Optional[builtins.str] = None) -> None:
        '''
        :param login_user: LoginUser is the user name used to access node machines. It defaults to "root" if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#login_user GoogleGkeonpremBareMetalAdminCluster#login_user}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42a2563ec214513d88f3e0034a472ccfa18e73dc49053a251557c1781a5eeaca)
            check_type(argname="argument login_user", value=login_user, expected_type=type_hints["login_user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if login_user is not None:
            self._values["login_user"] = login_user

    @builtins.property
    def login_user(self) -> typing.Optional[builtins.str]:
        '''LoginUser is the user name used to access node machines. It defaults to "root" if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#login_user GoogleGkeonpremBareMetalAdminCluster#login_user}
        '''
        result = self._values.get("login_user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterNodeAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalAdminClusterNodeAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterNodeAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f97f45f43992028fbf05bd305a64be3b673bb2c02878f3e2002374dcd3aa59b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLoginUser")
    def reset_login_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoginUser", []))

    @builtins.property
    @jsii.member(jsii_name="loginUserInput")
    def login_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loginUserInput"))

    @builtins.property
    @jsii.member(jsii_name="loginUser")
    def login_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loginUser"))

    @login_user.setter
    def login_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a3f09367aaf20ae1f89ad31c43df58c5b0fc3f524e4902d724b62fdd77c76e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterNodeAccessConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterNodeAccessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterNodeAccessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a68099b2ad1a4e0f1a64ae4504d0f65b4aaf204b72432675aef374aac77ac56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterNodeConfig",
    jsii_struct_bases=[],
    name_mapping={"max_pods_per_node": "maxPodsPerNode"},
)
class GoogleGkeonpremBareMetalAdminClusterNodeConfig:
    def __init__(
        self,
        *,
        max_pods_per_node: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_pods_per_node: The maximum number of pods a node can run. The size of the CIDR range assigned to the node will be derived from this parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#max_pods_per_node GoogleGkeonpremBareMetalAdminCluster#max_pods_per_node}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4847e46a437c077fc0a4aa2a907d91e846ebaf455321067e1b24c89c2586a2b7)
            check_type(argname="argument max_pods_per_node", value=max_pods_per_node, expected_type=type_hints["max_pods_per_node"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_pods_per_node is not None:
            self._values["max_pods_per_node"] = max_pods_per_node

    @builtins.property
    def max_pods_per_node(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of pods a node can run.

        The size of the CIDR range
        assigned to the node will be derived from this parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#max_pods_per_node GoogleGkeonpremBareMetalAdminCluster#max_pods_per_node}
        '''
        result = self._values.get("max_pods_per_node")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterNodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalAdminClusterNodeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterNodeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f57603db35cf7ae1241dc8e53954c98ef692d43efd4fada22453eed88fafe004)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxPodsPerNode")
    def reset_max_pods_per_node(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxPodsPerNode", []))

    @builtins.property
    @jsii.member(jsii_name="maxPodsPerNodeInput")
    def max_pods_per_node_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPodsPerNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPodsPerNode")
    def max_pods_per_node(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPodsPerNode"))

    @max_pods_per_node.setter
    def max_pods_per_node(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a18b1f0b84d0d6a21436317374b2813014c4d715f014dd31f5fa9f47f7bf28f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPodsPerNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterNodeConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterNodeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterNodeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b626665ed30094796c4ca18a5fd2df8d6285189fedf9e89b247471874436ea2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterProxy",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "no_proxy": "noProxy"},
)
class GoogleGkeonpremBareMetalAdminClusterProxy:
    def __init__(
        self,
        *,
        uri: builtins.str,
        no_proxy: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param uri: Specifies the address of your proxy server. For Example: http://domain WARNING: Do not provide credentials in the format of http://(username:password@)domain these will be rejected by the server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#uri GoogleGkeonpremBareMetalAdminCluster#uri}
        :param no_proxy: A list of IPs, hostnames, and domains that should skip the proxy. For example: ["127.0.0.1", "example.com", ".corp", "localhost"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#no_proxy GoogleGkeonpremBareMetalAdminCluster#no_proxy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa57212928b415b89937d531e3706fa6caff00ad3764c6405bf6701a2426e50d)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument no_proxy", value=no_proxy, expected_type=type_hints["no_proxy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }
        if no_proxy is not None:
            self._values["no_proxy"] = no_proxy

    @builtins.property
    def uri(self) -> builtins.str:
        '''Specifies the address of your proxy server.

        For Example: http://domain
        WARNING: Do not provide credentials in the format
        of http://(username:password@)domain these will be rejected by the server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#uri GoogleGkeonpremBareMetalAdminCluster#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def no_proxy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IPs, hostnames, and domains that should skip the proxy. For example: ["127.0.0.1", "example.com", ".corp", "localhost"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#no_proxy GoogleGkeonpremBareMetalAdminCluster#no_proxy}
        '''
        result = self._values.get("no_proxy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterProxy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalAdminClusterProxyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterProxyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31d63b034070b6e310f886f05d518edbfa8cabde8c2c065173ae93c85bb27e6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNoProxy")
    def reset_no_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoProxy", []))

    @builtins.property
    @jsii.member(jsii_name="noProxyInput")
    def no_proxy_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "noProxyInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="noProxy")
    def no_proxy(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "noProxy"))

    @no_proxy.setter
    def no_proxy(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2309cdcc0f3570a4b66327f8afd83076a89db0e11bfc331a407f3709e773024b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noProxy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0136dc6d7a8a56f5a8a2737065f99a349b7e8eb1f2b568561d9c52ec6aac840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterProxy]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterProxy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterProxy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9691dc8721647bbf46f596a1dd4ae7bc68494d0178fa6c1b250efefd4e96e051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterSecurityConfig",
    jsii_struct_bases=[],
    name_mapping={"authorization": "authorization"},
)
class GoogleGkeonpremBareMetalAdminClusterSecurityConfig:
    def __init__(
        self,
        *,
        authorization: typing.Optional[typing.Union["GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#authorization GoogleGkeonpremBareMetalAdminCluster#authorization}
        '''
        if isinstance(authorization, dict):
            authorization = GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorization(**authorization)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__941bd78d619aad1828801b72ff670f374e60cebfa52d91fc8a59fbc2c3660ba1)
            check_type(argname="argument authorization", value=authorization, expected_type=type_hints["authorization"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authorization is not None:
            self._values["authorization"] = authorization

    @builtins.property
    def authorization(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorization"]:
        '''authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#authorization GoogleGkeonpremBareMetalAdminCluster#authorization}
        '''
        result = self._values.get("authorization")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorization"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterSecurityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorization",
    jsii_struct_bases=[],
    name_mapping={"admin_users": "adminUsers"},
)
class GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorization:
    def __init__(
        self,
        *,
        admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#admin_users GoogleGkeonpremBareMetalAdminCluster#admin_users}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0536826ac75e2f75b9e6fb92979a3c093860797ffd162bf497b7ff14db93b464)
            check_type(argname="argument admin_users", value=admin_users, expected_type=type_hints["admin_users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_users": admin_users,
        }

    @builtins.property
    def admin_users(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers"]]:
        '''admin_users block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#admin_users GoogleGkeonpremBareMetalAdminCluster#admin_users}
        '''
        result = self._values.get("admin_users")
        assert result is not None, "Required property 'admin_users' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers",
    jsii_struct_bases=[],
    name_mapping={"username": "username"},
)
class GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers:
    def __init__(self, *, username: builtins.str) -> None:
        '''
        :param username: The name of the user, e.g. 'my-gcp-id@gmail.com'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#username GoogleGkeonpremBareMetalAdminCluster#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cac31115dbce6e3fa52602dcfdb1a5f1b1bde9a577ce444f4faca46e5d54514e)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
        }

    @builtins.property
    def username(self) -> builtins.str:
        '''The name of the user, e.g. 'my-gcp-id@gmail.com'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#username GoogleGkeonpremBareMetalAdminCluster#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d00b90e5cd3c081383057135892cea15cb7ec3017d807cf2583442c76367f5a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38fd15a1af06d5ed0175a7a8db93d7839b1903eff101923e346daf1164a853d5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42cf1530455087caf022782a885ff5371bde6db67a0fdd9912990bbcad093b4f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c55bac7556dedd9b1e17bbae148cf403dc38e00ac3fcefe978bbb6dc4d409e1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1e4b0cdc821b07740cddd4fe1ec001d898d27de84a6869f5c4619c7df0ae0d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f145b3cf6f15d4c09976ebf3a65a4da31a6f10f40418cca0bfa55a0c3a070aff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1107f106945159d33b472cbab1a90041e8f25dc53240ba2375f54852cdaa92e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3add069b5fc34693f647493faee7de050dfb6d306d278a20c007aee30b7f7cb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__279c7993eb42c4769d9ced0af275c228ac61436faa4ad4108192cc546af69401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__309d8587c82aad45a898dadfa9e41d624d4e30a6ffedfa4e0d3d2aa3816c345c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdminUsers")
    def put_admin_users(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a18e2ad1c67627b300fdf8c5ae261aba35971b96eac7f3c345ca2ada283fc1a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdminUsers", [value]))

    @builtins.property
    @jsii.member(jsii_name="adminUsers")
    def admin_users(
        self,
    ) -> GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsersList:
        return typing.cast(GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsersList, jsii.get(self, "adminUsers"))

    @builtins.property
    @jsii.member(jsii_name="adminUsersInput")
    def admin_users_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers]]], jsii.get(self, "adminUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorization]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f31779f4e5c1c3cf13ccfebe02fb852f201b97f41f431052087c6b266b149a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalAdminClusterSecurityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterSecurityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcb0a18856fa60a1cf73e09a69f051e2a8cf460975329f1e200f41ea774e41e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthorization")
    def put_authorization(
        self,
        *,
        admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#admin_users GoogleGkeonpremBareMetalAdminCluster#admin_users}
        '''
        value = GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorization(
            admin_users=admin_users
        )

        return typing.cast(None, jsii.invoke(self, "putAuthorization", [value]))

    @jsii.member(jsii_name="resetAuthorization")
    def reset_authorization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorization", []))

    @builtins.property
    @jsii.member(jsii_name="authorization")
    def authorization(
        self,
    ) -> GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationOutputReference, jsii.get(self, "authorization"))

    @builtins.property
    @jsii.member(jsii_name="authorizationInput")
    def authorization_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorization]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorization], jsii.get(self, "authorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterSecurityConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterSecurityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterSecurityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aa23c9742f0aa7788262c78830a531fdc59a49a6774a19f22495669ba15d2c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremBareMetalAdminClusterStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterStatusConditions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremBareMetalAdminClusterStatusConditions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterStatusConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalAdminClusterStatusConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterStatusConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb31cf1c08108b359cf1068b6c046802e60af9fa12a3c1497b2f3c38ab5cfa33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalAdminClusterStatusConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0437b325b090243687a4714889dd83ef77b460740cba2b5106f0aef7b31d8462)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterStatusConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__077fa0a8f01b50ac526a691921541f9882658cf0a4ac70566cd7d27a36e38c4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0c77c4f2691d56392b5fe51f71caf158d0bc51eb7cc8cb20e6d4d5a8616c8d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c1dca689cc0ffacd90448a9a86b9ec2c68955021600567642301eee006a6474)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalAdminClusterStatusConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterStatusConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec72ae40e60eb3ec1a99ecf2c4c3158efea13e7912610a60078c0148c5490ab9)
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
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterStatusConditions]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterStatusConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterStatusConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fb88550eaba4c3dd48dd07351d2c447eda2ef27cbfdddea20f15deac1855814)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalAdminClusterStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e666274226fea25bb41870fb06b6ec223b6e59c7e938837ec01a75b4617d07a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalAdminClusterStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9253b75de12a9d4090aaebdf5d665034be9c5dab97a36c7ef80b20759634d101)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da1fb30e2319f47c4063f723e4e74b9647fef965a4c1092cdc886f6f44443966)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a29cea34d8857251f9a243b745d1d10b6cb66497574197671d41f29b8f63e9a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc15a3ee2cde1d2455522ec43b4689363cb1ccfbeff8ccf6a1589bca6bcd0c41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalAdminClusterStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c02fd27aeb45d3eaeecb2f8be93f6d42bc51e4f011251eab040b3cd5e5ab1882)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> GoogleGkeonpremBareMetalAdminClusterStatusConditionsList:
        return typing.cast(GoogleGkeonpremBareMetalAdminClusterStatusConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterStatus]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9bc41b504577661eb71e9f384e17411a0c7017bb61aeaee84c725bdf9e13520)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterStorage",
    jsii_struct_bases=[],
    name_mapping={
        "lvp_node_mounts_config": "lvpNodeMountsConfig",
        "lvp_share_config": "lvpShareConfig",
    },
)
class GoogleGkeonpremBareMetalAdminClusterStorage:
    def __init__(
        self,
        *,
        lvp_node_mounts_config: typing.Union["GoogleGkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig", typing.Dict[builtins.str, typing.Any]],
        lvp_share_config: typing.Union["GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param lvp_node_mounts_config: lvp_node_mounts_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#lvp_node_mounts_config GoogleGkeonpremBareMetalAdminCluster#lvp_node_mounts_config}
        :param lvp_share_config: lvp_share_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#lvp_share_config GoogleGkeonpremBareMetalAdminCluster#lvp_share_config}
        '''
        if isinstance(lvp_node_mounts_config, dict):
            lvp_node_mounts_config = GoogleGkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig(**lvp_node_mounts_config)
        if isinstance(lvp_share_config, dict):
            lvp_share_config = GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfig(**lvp_share_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__851c2e54309274707c82c958e1a8a55ebc1ad92450842b2af73be3fb48a88488)
            check_type(argname="argument lvp_node_mounts_config", value=lvp_node_mounts_config, expected_type=type_hints["lvp_node_mounts_config"])
            check_type(argname="argument lvp_share_config", value=lvp_share_config, expected_type=type_hints["lvp_share_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lvp_node_mounts_config": lvp_node_mounts_config,
            "lvp_share_config": lvp_share_config,
        }

    @builtins.property
    def lvp_node_mounts_config(
        self,
    ) -> "GoogleGkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig":
        '''lvp_node_mounts_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#lvp_node_mounts_config GoogleGkeonpremBareMetalAdminCluster#lvp_node_mounts_config}
        '''
        result = self._values.get("lvp_node_mounts_config")
        assert result is not None, "Required property 'lvp_node_mounts_config' is missing"
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig", result)

    @builtins.property
    def lvp_share_config(
        self,
    ) -> "GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfig":
        '''lvp_share_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#lvp_share_config GoogleGkeonpremBareMetalAdminCluster#lvp_share_config}
        '''
        result = self._values.get("lvp_share_config")
        assert result is not None, "Required property 'lvp_share_config' is missing"
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "storage_class": "storageClass"},
)
class GoogleGkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig:
    def __init__(self, *, path: builtins.str, storage_class: builtins.str) -> None:
        '''
        :param path: The host machine path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#path GoogleGkeonpremBareMetalAdminCluster#path}
        :param storage_class: The StorageClass name that PVs will be created with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#storage_class GoogleGkeonpremBareMetalAdminCluster#storage_class}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e50d255dda86198554eaf2d61f6b7567818252261919166c9ae284a4c5e61cd2)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "storage_class": storage_class,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''The host machine path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#path GoogleGkeonpremBareMetalAdminCluster#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_class(self) -> builtins.str:
        '''The StorageClass name that PVs will be created with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#storage_class GoogleGkeonpremBareMetalAdminCluster#storage_class}
        '''
        result = self._values.get("storage_class")
        assert result is not None, "Required property 'storage_class' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f126196637eb0736c8979a7e3ae0da4ee4b9b615cbf35ad870346c528b4d02e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="storageClassInput")
    def storage_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageClassInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c57448abdb58f6165f32f530b91f5bedf8600f39eb0a305fa7bdc1d75867ea4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageClass")
    def storage_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageClass"))

    @storage_class.setter
    def storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ebb0b29edac157c5dc6fa28d9be736eac02d22671960c25be050f41fa622dea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea4d2d02e05346ef885b23f5cc3ce7abeae958a444503d48e8ec4084d49ec7e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfig",
    jsii_struct_bases=[],
    name_mapping={
        "lvp_config": "lvpConfig",
        "shared_path_pv_count": "sharedPathPvCount",
    },
)
class GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfig:
    def __init__(
        self,
        *,
        lvp_config: typing.Union["GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig", typing.Dict[builtins.str, typing.Any]],
        shared_path_pv_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param lvp_config: lvp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#lvp_config GoogleGkeonpremBareMetalAdminCluster#lvp_config}
        :param shared_path_pv_count: The number of subdirectories to create under path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#shared_path_pv_count GoogleGkeonpremBareMetalAdminCluster#shared_path_pv_count}
        '''
        if isinstance(lvp_config, dict):
            lvp_config = GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig(**lvp_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c66e1db4c41e6aa88374a5d98f950703f696f4bf2a901fc3fa08882a5539339)
            check_type(argname="argument lvp_config", value=lvp_config, expected_type=type_hints["lvp_config"])
            check_type(argname="argument shared_path_pv_count", value=shared_path_pv_count, expected_type=type_hints["shared_path_pv_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lvp_config": lvp_config,
        }
        if shared_path_pv_count is not None:
            self._values["shared_path_pv_count"] = shared_path_pv_count

    @builtins.property
    def lvp_config(
        self,
    ) -> "GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig":
        '''lvp_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#lvp_config GoogleGkeonpremBareMetalAdminCluster#lvp_config}
        '''
        result = self._values.get("lvp_config")
        assert result is not None, "Required property 'lvp_config' is missing"
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig", result)

    @builtins.property
    def shared_path_pv_count(self) -> typing.Optional[jsii.Number]:
        '''The number of subdirectories to create under path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#shared_path_pv_count GoogleGkeonpremBareMetalAdminCluster#shared_path_pv_count}
        '''
        result = self._values.get("shared_path_pv_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "storage_class": "storageClass"},
)
class GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig:
    def __init__(self, *, path: builtins.str, storage_class: builtins.str) -> None:
        '''
        :param path: The host machine path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#path GoogleGkeonpremBareMetalAdminCluster#path}
        :param storage_class: The StorageClass name that PVs will be created with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#storage_class GoogleGkeonpremBareMetalAdminCluster#storage_class}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33be7e6bda92264526eb3f6c039835b5d2858a958f5776d1507c9290e0634717)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "storage_class": storage_class,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''The host machine path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#path GoogleGkeonpremBareMetalAdminCluster#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_class(self) -> builtins.str:
        '''The StorageClass name that PVs will be created with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#storage_class GoogleGkeonpremBareMetalAdminCluster#storage_class}
        '''
        result = self._values.get("storage_class")
        assert result is not None, "Required property 'storage_class' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c51ffab033ced1ec80e6ab7d9f4bda9c2b0d296f62163c0135459606675c9d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="storageClassInput")
    def storage_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageClassInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__614d72dd396b53a422eb4ddbcf215d4eda4f27a79cffbfef9910afaefb160988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageClass")
    def storage_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageClass"))

    @storage_class.setter
    def storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__739f657fb35c94e1d06f6069ad55841d219ef56dcc8e293ab9523b92faa55aee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e36531bcafb20b9ffb33817ad4173a1280fa1a1e70e167f57cc8b62e1467e41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__827563063c72d9e01a718057674e18831f59268cb04d1d8366006fef94ef2f82)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLvpConfig")
    def put_lvp_config(
        self,
        *,
        path: builtins.str,
        storage_class: builtins.str,
    ) -> None:
        '''
        :param path: The host machine path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#path GoogleGkeonpremBareMetalAdminCluster#path}
        :param storage_class: The StorageClass name that PVs will be created with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#storage_class GoogleGkeonpremBareMetalAdminCluster#storage_class}
        '''
        value = GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig(
            path=path, storage_class=storage_class
        )

        return typing.cast(None, jsii.invoke(self, "putLvpConfig", [value]))

    @jsii.member(jsii_name="resetSharedPathPvCount")
    def reset_shared_path_pv_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedPathPvCount", []))

    @builtins.property
    @jsii.member(jsii_name="lvpConfig")
    def lvp_config(
        self,
    ) -> GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfigOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfigOutputReference, jsii.get(self, "lvpConfig"))

    @builtins.property
    @jsii.member(jsii_name="lvpConfigInput")
    def lvp_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig], jsii.get(self, "lvpConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedPathPvCountInput")
    def shared_path_pv_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sharedPathPvCountInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedPathPvCount")
    def shared_path_pv_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sharedPathPvCount"))

    @shared_path_pv_count.setter
    def shared_path_pv_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ecb0fe679e602daa6ac1207d0a6ac37bca88ae0f2500e197ce4926e0367ce9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedPathPvCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fac5a647f7918f66aeb49af1b4b2becd40cf3cfd0177997fb8d6a178cfd809d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalAdminClusterStorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterStorageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c29d733567917d3a9f199c1c77463dca5a92bd041d548720ba60987f9740a9a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLvpNodeMountsConfig")
    def put_lvp_node_mounts_config(
        self,
        *,
        path: builtins.str,
        storage_class: builtins.str,
    ) -> None:
        '''
        :param path: The host machine path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#path GoogleGkeonpremBareMetalAdminCluster#path}
        :param storage_class: The StorageClass name that PVs will be created with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#storage_class GoogleGkeonpremBareMetalAdminCluster#storage_class}
        '''
        value = GoogleGkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig(
            path=path, storage_class=storage_class
        )

        return typing.cast(None, jsii.invoke(self, "putLvpNodeMountsConfig", [value]))

    @jsii.member(jsii_name="putLvpShareConfig")
    def put_lvp_share_config(
        self,
        *,
        lvp_config: typing.Union[GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig, typing.Dict[builtins.str, typing.Any]],
        shared_path_pv_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param lvp_config: lvp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#lvp_config GoogleGkeonpremBareMetalAdminCluster#lvp_config}
        :param shared_path_pv_count: The number of subdirectories to create under path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#shared_path_pv_count GoogleGkeonpremBareMetalAdminCluster#shared_path_pv_count}
        '''
        value = GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfig(
            lvp_config=lvp_config, shared_path_pv_count=shared_path_pv_count
        )

        return typing.cast(None, jsii.invoke(self, "putLvpShareConfig", [value]))

    @builtins.property
    @jsii.member(jsii_name="lvpNodeMountsConfig")
    def lvp_node_mounts_config(
        self,
    ) -> GoogleGkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfigOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfigOutputReference, jsii.get(self, "lvpNodeMountsConfig"))

    @builtins.property
    @jsii.member(jsii_name="lvpShareConfig")
    def lvp_share_config(
        self,
    ) -> GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigOutputReference, jsii.get(self, "lvpShareConfig"))

    @builtins.property
    @jsii.member(jsii_name="lvpNodeMountsConfigInput")
    def lvp_node_mounts_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig], jsii.get(self, "lvpNodeMountsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="lvpShareConfigInput")
    def lvp_share_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfig], jsii.get(self, "lvpShareConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterStorage]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterStorage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterStorage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd62bfb5eb1480fe2fc3f4d1b38bf1e4bfddc0bf702f454d74a59a812523aa2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleGkeonpremBareMetalAdminClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#create GoogleGkeonpremBareMetalAdminCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#delete GoogleGkeonpremBareMetalAdminCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#update GoogleGkeonpremBareMetalAdminCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68a0efbf45e9c5adc756c0d9ca1deb40ff0a4fc8f4eb4f812632b317f55a2e39)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#create GoogleGkeonpremBareMetalAdminCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#delete GoogleGkeonpremBareMetalAdminCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_admin_cluster#update GoogleGkeonpremBareMetalAdminCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalAdminClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c61a0c3b0ce77c5dad60ec1609aea34cecfc2635eab1b6de0c0afe3798acadc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eaf7418e2562d78a64892456c2fe00a5f169267c0f79e87ff37a61cc3f74370f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ee0523eb4b2326a91b75236e105b6b8e5370d6f2b5a1a0d42149e0e85195149)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d756c4d8339cfc6a681a97a959d5c0fbca438da14a355fcc4bda8533bc065d54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalAdminClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalAdminClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalAdminClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82fbde8038abfb58f60d5db8c8fbc8bdeb1cc1f7979b61ac0638150d66779ed9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterValidationCheck",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremBareMetalAdminClusterValidationCheck:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterValidationCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalAdminClusterValidationCheckList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterValidationCheckList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__848a2c1fb923da93aa42bd3fd720331065734385e00452dfb6de9333478f32f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalAdminClusterValidationCheckOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8711a79a913cb67550395d2b1f23d12dd43572fed1b81a65cb1d30a429181dc9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterValidationCheckOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__228d4cc4c0c4531c49ca17957c5811b7e0801fe7b06ece6a3a98fbbce3c1ab97)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8dbb1c21072ebad1257f69f2ddca84af9f531ca1447400ec1be342aedb65f2c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9ea64c3782c06da390bda5cd744b9cbdb984cc5bb4e87d5135c7fd3153b195b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalAdminClusterValidationCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterValidationCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f90decef1d3f4a5a7ffd031e6b30f798d5da3690423229175e9e7af5028af5b7)
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
    def status(self) -> "GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusList":
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterValidationCheck]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterValidationCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterValidationCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaa0009728ff02da45aac51f359be5fc1a24e37afbd1ee955c1abcab7864fb73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterValidationCheckStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremBareMetalAdminClusterValidationCheckStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterValidationCheckStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97628a5e80d08d89a47d905744c2e1a93ac2a2b4bf12c290b396f4f19da8acd1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__779af1d73e370ea38a61ea4ea28bfe991183fbba3d5811fb28ea5b7115e61981)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5c62083a8909842e73dda84e062f52e96977a9b662463a9f8d6d2fb0067105e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34c533f900e1335a5030f69e3a5a4c29e50fd52f1eb97237f5f8d925cf93a840)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc1f8807bcac58f49bf959cb31141edc1de7444f81b266d27c244f88e335c31a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63c6ec3761f6a47c564ef3e449dad892e08bba2fa9a20816c2ca3d53d38d33c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="result")
    def result(
        self,
    ) -> "GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusResultList":
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusResultList", jsii.get(self, "result"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterValidationCheckStatus]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterValidationCheckStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterValidationCheckStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2ebbde2a6f2bb5128c844861d50f0132a285e240986c23ed2e6c93a05c1e050)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusResult",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusResult:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusResultList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusResultList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89851adc89a0f862e13083a8acd9d0d703c94b4c994e6f1a98dfccb739149ea6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusResultOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94beabe25810cfd5c046ffa44519c21d0ec08d346f8540e92d2b2c423b15d33e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusResultOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcf6781dd211b43772d52bf022b49d1deec97786b4a4177a2f0d50ce6499bb0d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de5ff36186ca90fdd90f148d3ca0f365e0a7a5b9334cf5b8d40ad9b5b79b2e88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28450bd972debfba77983a70963dee43a06221e6e60256edeffa255f3d52b54a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusResultOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalAdminCluster.GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusResultOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5cfd91c1b21158d3904aae182681fcd20582c3d9bba4cf3d799600b0e451691)
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
    ) -> typing.Optional[GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusResult]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusResult], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusResult],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b096514efac660498b25872b36adccbb62d2e1894a0d6d6f2d3176af04c04d8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleGkeonpremBareMetalAdminCluster",
    "GoogleGkeonpremBareMetalAdminClusterClusterOperations",
    "GoogleGkeonpremBareMetalAdminClusterClusterOperationsOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterConfig",
    "GoogleGkeonpremBareMetalAdminClusterControlPlane",
    "GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgs",
    "GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgsList",
    "GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgsOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig",
    "GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig",
    "GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs",
    "GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsList",
    "GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints",
    "GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsList",
    "GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterControlPlaneOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterFleet",
    "GoogleGkeonpremBareMetalAdminClusterFleetList",
    "GoogleGkeonpremBareMetalAdminClusterFleetOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterLoadBalancer",
    "GoogleGkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig",
    "GoogleGkeonpremBareMetalAdminClusterLoadBalancerManualLbConfigOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterLoadBalancerOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterLoadBalancerPortConfig",
    "GoogleGkeonpremBareMetalAdminClusterLoadBalancerPortConfigOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterLoadBalancerVipConfig",
    "GoogleGkeonpremBareMetalAdminClusterLoadBalancerVipConfigOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterMaintenanceConfig",
    "GoogleGkeonpremBareMetalAdminClusterMaintenanceConfigOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterNetworkConfig",
    "GoogleGkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr",
    "GoogleGkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidrOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterNetworkConfigOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterNodeAccessConfig",
    "GoogleGkeonpremBareMetalAdminClusterNodeAccessConfigOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterNodeConfig",
    "GoogleGkeonpremBareMetalAdminClusterNodeConfigOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterProxy",
    "GoogleGkeonpremBareMetalAdminClusterProxyOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterSecurityConfig",
    "GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorization",
    "GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers",
    "GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsersList",
    "GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsersOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterSecurityConfigOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterStatus",
    "GoogleGkeonpremBareMetalAdminClusterStatusConditions",
    "GoogleGkeonpremBareMetalAdminClusterStatusConditionsList",
    "GoogleGkeonpremBareMetalAdminClusterStatusConditionsOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterStatusList",
    "GoogleGkeonpremBareMetalAdminClusterStatusOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterStorage",
    "GoogleGkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig",
    "GoogleGkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfigOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfig",
    "GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig",
    "GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfigOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterStorageOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterTimeouts",
    "GoogleGkeonpremBareMetalAdminClusterTimeoutsOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterValidationCheck",
    "GoogleGkeonpremBareMetalAdminClusterValidationCheckList",
    "GoogleGkeonpremBareMetalAdminClusterValidationCheckOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterValidationCheckStatus",
    "GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusList",
    "GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusOutputReference",
    "GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusResult",
    "GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusResultList",
    "GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusResultOutputReference",
]

publication.publish()

def _typecheckingstub__82f6af80fc09edba4dee7869829a9e37a75ca87950437cb7485aed5a92f17c0d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    bare_metal_version: typing.Optional[builtins.str] = None,
    cluster_operations: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterClusterOperations, typing.Dict[builtins.str, typing.Any]]] = None,
    control_plane: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterControlPlane, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    load_balancer: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterLoadBalancer, typing.Dict[builtins.str, typing.Any]]] = None,
    maintenance_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterMaintenanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    network_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_access_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterNodeAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    proxy: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    security_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterSecurityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    storage: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__44d58927d246e69d24b2ba7b5e91f3da2cb9f16bac367f9fab70abe431a1b417(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08c40377f9e7f5c21b183403f4412bcb91b287a8baa75e0da1b3985f16b952c2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c17398224c6bf4025753c52175daffade0bbba615b769c1e7f9860f88d33c9e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbacea1ba4f5201c848a76a363a045386dd3a95082c542398ef4bdd4ad14198d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d9a76cc3f364e1537d0f7984d9915b29b1760e9d6f00d2427c158bbcbd2e4c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea60c753ad11041a70fce10784bb15e891a527b0b645ad410e8685f8702d9044(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__732c560e584d276e471db3699efe1072ce68577eae12b4d0864aad1b1370b371(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef220aeecf12e45e6b6eaccfd03ffe0f098e46a7674877184fd6705c1eca761(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf62f39278a3634a44f4ef436c19bea2fd51a4c5adf4639bd2d19ac78804b7e7(
    *,
    enable_application_logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb7936b9cfd79876cf0f41c420f21978ecfb5c54e71249f9d77559c6e0f6b7c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbf09734ab332d73901a6c8f6f1b00d517b94296d70ac8698eba5a8f1b7fab91(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4a061a51e7968339c9fd1283957c3a1dc140d861f1940b56ec19846aee5d07(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterClusterOperations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfff2fa322c17fcc3cd84c0f4b5921865d6698dbbd288b6334c6962bf3189d72(
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
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    bare_metal_version: typing.Optional[builtins.str] = None,
    cluster_operations: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterClusterOperations, typing.Dict[builtins.str, typing.Any]]] = None,
    control_plane: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterControlPlane, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    load_balancer: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterLoadBalancer, typing.Dict[builtins.str, typing.Any]]] = None,
    maintenance_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterMaintenanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    network_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_access_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterNodeAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    proxy: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    security_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterSecurityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    storage: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5a54391e4d5ce3404b953979da9873dc3dc6555dd23dab3f0c59682a04b4b5a(
    *,
    control_plane_node_pool_config: typing.Union[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig, typing.Dict[builtins.str, typing.Any]],
    api_server_args: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgs, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b9366e52aeec1fe5f75cff0a859ea3a28c8ec24e2b8e47a15d44a05add7d0f2(
    *,
    argument: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__204ce0623efbd7df4473aad5d34a51bf2d34c7c8736127c54c630d7c7c8364ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19552d8584915cb628953a59a7df5dd3d963647f2f9dcaba677d35544dac657b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f6214d73c9419fb65cc79b290b7c0e6d374a3675e8e2db9b07a2152f1db2ee3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7ddbf5c44f781e72cf6ae03e6939f96952f9ca09f85b5784fc16636ee2a5662(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b7fa6dd954f46a3c05f8ba66b67adf96e941e5135062d688b57e775fd9c075(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__902fe714fe86ed22031a7c224501874c76149621c0bd1f8cb669e8706d70984f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d4e8f2411f3ce7f381df9c91d07138539dc61888224bc64130a684c9f668243(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ca5f867cfd02578ab7bf97e52c550e99afadfc5763bd2c16fd10f149702975(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__122023ffae63c30a28a403e99981d1179fed1b955a2f79b65e21143f732042dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25773acfe53ddee466493c965d77bdee985162d23c72cb173cf27a28581698ba(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cca7a99e4b1941ea0d0f137a56fed7a01b6538e5ce36848758d98aa48152b8a8(
    *,
    node_pool_config: typing.Union[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fbeaa49f936a244448b2a4b249c8be39173c6b148abd8daef40f17152852875(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    operating_system: typing.Optional[builtins.str] = None,
    taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__913fe24b1c8dfa4fdde5724ade77aaae733c0573fe20e80ae181db9bdfe5c2ea(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5058cff1714545d8fa8df8f6fc54e8e06e7d7e9c42bad16c04dd1bb751201f3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb06f8b79952c5239febd4f58a3b5e176bb6c77d8b511383f9a4d8904e3bdeb5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd6e7fae5f5580ab8fd793b3e24e7416c4cedcd6d2e586df4c2afa2bbadb7c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fea92e5e464297f7db92243a44875cd1a9ef240f6dd1aa815dcc1e5ec7eef16(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09451be2ad6095bc699bb83ada1268e00d29617396cdb50f07215d21e9502f71(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51390e75e6a70f8d3d4fc5d95c1789103b102a3fb928fd24dc6984c4151431de(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86f62022b1fad523af549c9ee1eb59595b47293541c21f12ce848c424c967bce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d7589466042f57bad04858e83d5259aaffbe80bc343138739ce8d3bfc90817(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ddd3d86f0948572085a30cb624ce43dcac0e7aa2c81a9a2eb672eab6b752be2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c743b4484ce64932bb9b039156e158b60e11adad1b350f3a5aba097b85cc6514(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d59446c0dff9027cc024e72a8839a18c3f97fe2d4adb889be7196cc07182929(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af71e3fa9c395e49510d16791d857bfdb73222bb7687eefa4e8e32560cf70206(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40fa05b77f28cd3510a9d7cfbb86d491f52296043a29186d6de7b60e6985cf54(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b8347f70972f7e1a4b082cecaee8c5bb6170244568bd9c60d9d47d9c32a97e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eece15c53dab21f2404492006dc8dc5da5c925cdb26c702f189c1a42617098ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c500b14140c5157237b5b4a77ddeee2a1f4abd5f65ab1167f61f99699c5fdc89(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f8eba7cfcf56e0b39181b301d3d01429f61a6e1371be3cbea6d1aa4171ba9b(
    *,
    effect: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ff6a186c1df1153d8223a7e2f0f2926e56a74bcf06c1fe554b0304b68d55191(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29a50d159724ce6a8276d600f9386ad7f0338dedfe8f82dcc72e0e2f2a3b66dd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088507ad230c4808ef9b2b5e1f84b3852d35704eef4e689a4f31dfb51eab73e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0eb73489c79a20357ca79f729c4c7d627bbb91bae9b51e6cd6abff4eaf5dbe7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1644a451fc7a05e35bed81630ed5d4a6ddbda377ff1386200847daf03dcb259(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bfd43d13f3c6fdb70a3c59a7526bbe727fc6910a0e4f2bb49c8b2304ca34051(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ac7863dbe15473c7bd0ad792caffd29b111236ba99b22ec8e24a59f125a14c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__932845fe10e1ce3ff5b4ec22060aba3029d693c6b382a2a5b083fc15dcc2d6a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83714010060bf2fe1f2a21c7249e4b6d6be74db279ee2bc0261869319c7bb24d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9de719bf0ec219dd75e484285366d4f9c539d2d54b4b90966ba02c504a32a77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e83cfb989ed60b283fc510a6f2bef35b50e7ddeddc33793cd2bc0f2a1ac97be(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c8441a97640654eaa774c820e313c0c7c7b866f171f592f111355805538374(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__008d6e8ce5b5a2fd9cf33b7f3190d43b98c36abf741a13f6a3a9a51b95f12a08(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a63615deab81ff907445314cd39eb9ecc406d0280fd44f40f1547bab248a8da2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab26cf1b05c990bba1d4a96d873604e0cef2035af36855b0422e8363acc8167(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalAdminClusterControlPlaneApiServerArgs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07a0f90a477502f9f7c610e8cad80c3c70b65174cae801c98c02259d8e60622(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterControlPlane],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aff6665c50a5951b1eb5e1563086af96e5fecf820c11a6641ac9ce3e4ed9b2d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__183f13f629984045150e4fbec594924594ea2e110cc2f44b16438f7d74a98c8c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81ad36d2e205f4c4f9fae960a420cbe85c3d13eade60c61c9b0eb8f1b60d2cd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d8cf312570ecf07d0d2aaddffbd58b9636f8aaa3f726c5e7eabd5d0ca72a651(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4807a71c0d842925c188fb1af27408d70397a448eb2f7e65a94b858501ea79f4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e4259a864b65919171e2f9dc98e1270d901a689a4484bb251411f373120f3e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b0c26f2341dcb439ec00d1125bd71dc5135b08faadeb71717f329b95fc1789d(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterFleet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4299278fa16f325f368ca3daa09ce5d3a09e1c5d07ad70f17553efd28a2aad3(
    *,
    port_config: typing.Union[GoogleGkeonpremBareMetalAdminClusterLoadBalancerPortConfig, typing.Dict[builtins.str, typing.Any]],
    vip_config: typing.Union[GoogleGkeonpremBareMetalAdminClusterLoadBalancerVipConfig, typing.Dict[builtins.str, typing.Any]],
    manual_lb_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f629f37164f4b63ad7fef04b10389697487bd01dac2c98bc142de3447de4e1(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b1cbcaf9e7b2aeb7c5a8849971d8d1b02defa9042c42bae0dcf4982228675e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba613279b93ec62f3e3b397b75b2669240411721bce7594930a7cb4c66a1860f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdb74c1b034c037033ccb5a420e6cdc893ff9a3879f26f46c1d20f8262a92b0b(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7873e23dfb78ef3a3acb7742e0b8baba6595d9a91aaae024a0ec73cd48e73126(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86b4bc038058c725d16cee462f68634efc5e17089b3e37ad85a853b7d16f7973(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterLoadBalancer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa13121bf3e0078406c876bb08365d2d8f50bc8450f653ec8fa00ca4bcf7d51(
    *,
    control_plane_load_balancer_port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__772bfb73c1dc10ed8ee5d0cd2b88122e4b53a21e799770c47b044a6211be9f0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd8ef628a24134dbbc16b94e701801798e7c97e8190d443389f971d2894ddc3d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dae42ae730caa3c8512c1d3ea4342a8760d3c7988324ab4186d3010cbbd0b6d5(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterLoadBalancerPortConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d32eb209e60af015e3de61b1902bf71f784aa68fa79ad4a0d7880b7010fdbd99(
    *,
    control_plane_vip: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26cc5cd3f38d4c5926cea94005df8411b9b2b2262ac4a60868dffb74813eb5d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98eaaba22f12d84ae08b5f0de0b78240d53250c8e8df256073669a25911e7395(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef54fa569d8e038fb2606b47d578d5268ed094ead88b53c2a4585ab7214c6124(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterLoadBalancerVipConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b09dae7657ac322ed54184395da17bbe0299cd9990fcf9e881282eff659722b(
    *,
    maintenance_address_cidr_blocks: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa4b9323ecd5949063714199c82a1cb13a875c53fb02fdfe19a0eeea3b92f9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a6fbab2c5c4130526b27b2081182af5751fdee06f41c27e2a12f8418ae8f3b0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ba0d622e437c10911b2a389cdb69fb503f13d8b93c3fab33d9503919e0e8be0(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterMaintenanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0dd566f2ae27cbb67c3de103fef083516b30dba6a0c4a9468b6a2b98e335557(
    *,
    island_mode_cidr: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b7a44b4c112243cb95ca88c3fa5a964d350bde2f94d7aa63a309e3c4b15c4fe(
    *,
    pod_address_cidr_blocks: typing.Sequence[builtins.str],
    service_address_cidr_blocks: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3604158e52cd6eed2af87c607baee11998d53e36cb9434ad6a38300e41f355e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a5352bafe191d55aa78f7c13bc0df047e34d910170930f8bd1f5e55907815c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e7f7cec6c6e0b80d1565e2ccac0fe354e4a77b2aa454ae1b431e73e5fb0e95(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a734ac2cd76c43ea7fcfe66e5baec36a801502c1dd87b4fdba63661750154c91(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b21ff319cf1a6c5c762fb481f28d9b32c6e0143fe2447757a99a52c881f79e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__194e7be5f3861f6c6f09b2ea7b94d4dba491f6f712c5765a91da40179318cb24(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42a2563ec214513d88f3e0034a472ccfa18e73dc49053a251557c1781a5eeaca(
    *,
    login_user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f97f45f43992028fbf05bd305a64be3b673bb2c02878f3e2002374dcd3aa59b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a3f09367aaf20ae1f89ad31c43df58c5b0fc3f524e4902d724b62fdd77c76e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a68099b2ad1a4e0f1a64ae4504d0f65b4aaf204b72432675aef374aac77ac56(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterNodeAccessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4847e46a437c077fc0a4aa2a907d91e846ebaf455321067e1b24c89c2586a2b7(
    *,
    max_pods_per_node: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f57603db35cf7ae1241dc8e53954c98ef692d43efd4fada22453eed88fafe004(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a18b1f0b84d0d6a21436317374b2813014c4d715f014dd31f5fa9f47f7bf28f0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b626665ed30094796c4ca18a5fd2df8d6285189fedf9e89b247471874436ea2(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterNodeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa57212928b415b89937d531e3706fa6caff00ad3764c6405bf6701a2426e50d(
    *,
    uri: builtins.str,
    no_proxy: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31d63b034070b6e310f886f05d518edbfa8cabde8c2c065173ae93c85bb27e6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2309cdcc0f3570a4b66327f8afd83076a89db0e11bfc331a407f3709e773024b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0136dc6d7a8a56f5a8a2737065f99a349b7e8eb1f2b568561d9c52ec6aac840(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9691dc8721647bbf46f596a1dd4ae7bc68494d0178fa6c1b250efefd4e96e051(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterProxy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__941bd78d619aad1828801b72ff670f374e60cebfa52d91fc8a59fbc2c3660ba1(
    *,
    authorization: typing.Optional[typing.Union[GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0536826ac75e2f75b9e6fb92979a3c093860797ffd162bf497b7ff14db93b464(
    *,
    admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cac31115dbce6e3fa52602dcfdb1a5f1b1bde9a577ce444f4faca46e5d54514e(
    *,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d00b90e5cd3c081383057135892cea15cb7ec3017d807cf2583442c76367f5a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38fd15a1af06d5ed0175a7a8db93d7839b1903eff101923e346daf1164a853d5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42cf1530455087caf022782a885ff5371bde6db67a0fdd9912990bbcad093b4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55bac7556dedd9b1e17bbae148cf403dc38e00ac3fcefe978bbb6dc4d409e1a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e4b0cdc821b07740cddd4fe1ec001d898d27de84a6869f5c4619c7df0ae0d2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f145b3cf6f15d4c09976ebf3a65a4da31a6f10f40418cca0bfa55a0c3a070aff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1107f106945159d33b472cbab1a90041e8f25dc53240ba2375f54852cdaa92e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3add069b5fc34693f647493faee7de050dfb6d306d278a20c007aee30b7f7cb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__279c7993eb42c4769d9ced0af275c228ac61436faa4ad4108192cc546af69401(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__309d8587c82aad45a898dadfa9e41d624d4e30a6ffedfa4e0d3d2aa3816c345c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a18e2ad1c67627b300fdf8c5ae261aba35971b96eac7f3c345ca2ada283fc1a8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f31779f4e5c1c3cf13ccfebe02fb852f201b97f41f431052087c6b266b149a2(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterSecurityConfigAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcb0a18856fa60a1cf73e09a69f051e2a8cf460975329f1e200f41ea774e41e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aa23c9742f0aa7788262c78830a531fdc59a49a6774a19f22495669ba15d2c3(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterSecurityConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb31cf1c08108b359cf1068b6c046802e60af9fa12a3c1497b2f3c38ab5cfa33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0437b325b090243687a4714889dd83ef77b460740cba2b5106f0aef7b31d8462(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077fa0a8f01b50ac526a691921541f9882658cf0a4ac70566cd7d27a36e38c4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c77c4f2691d56392b5fe51f71caf158d0bc51eb7cc8cb20e6d4d5a8616c8d1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c1dca689cc0ffacd90448a9a86b9ec2c68955021600567642301eee006a6474(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec72ae40e60eb3ec1a99ecf2c4c3158efea13e7912610a60078c0148c5490ab9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb88550eaba4c3dd48dd07351d2c447eda2ef27cbfdddea20f15deac1855814(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterStatusConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e666274226fea25bb41870fb06b6ec223b6e59c7e938837ec01a75b4617d07a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9253b75de12a9d4090aaebdf5d665034be9c5dab97a36c7ef80b20759634d101(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1fb30e2319f47c4063f723e4e74b9647fef965a4c1092cdc886f6f44443966(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a29cea34d8857251f9a243b745d1d10b6cb66497574197671d41f29b8f63e9a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc15a3ee2cde1d2455522ec43b4689363cb1ccfbeff8ccf6a1589bca6bcd0c41(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c02fd27aeb45d3eaeecb2f8be93f6d42bc51e4f011251eab040b3cd5e5ab1882(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9bc41b504577661eb71e9f384e17411a0c7017bb61aeaee84c725bdf9e13520(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__851c2e54309274707c82c958e1a8a55ebc1ad92450842b2af73be3fb48a88488(
    *,
    lvp_node_mounts_config: typing.Union[GoogleGkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig, typing.Dict[builtins.str, typing.Any]],
    lvp_share_config: typing.Union[GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e50d255dda86198554eaf2d61f6b7567818252261919166c9ae284a4c5e61cd2(
    *,
    path: builtins.str,
    storage_class: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f126196637eb0736c8979a7e3ae0da4ee4b9b615cbf35ad870346c528b4d02e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c57448abdb58f6165f32f530b91f5bedf8600f39eb0a305fa7bdc1d75867ea4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ebb0b29edac157c5dc6fa28d9be736eac02d22671960c25be050f41fa622dea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea4d2d02e05346ef885b23f5cc3ce7abeae958a444503d48e8ec4084d49ec7e2(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c66e1db4c41e6aa88374a5d98f950703f696f4bf2a901fc3fa08882a5539339(
    *,
    lvp_config: typing.Union[GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig, typing.Dict[builtins.str, typing.Any]],
    shared_path_pv_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33be7e6bda92264526eb3f6c039835b5d2858a958f5776d1507c9290e0634717(
    *,
    path: builtins.str,
    storage_class: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c51ffab033ced1ec80e6ab7d9f4bda9c2b0d296f62163c0135459606675c9d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__614d72dd396b53a422eb4ddbcf215d4eda4f27a79cffbfef9910afaefb160988(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__739f657fb35c94e1d06f6069ad55841d219ef56dcc8e293ab9523b92faa55aee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e36531bcafb20b9ffb33817ad4173a1280fa1a1e70e167f57cc8b62e1467e41(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827563063c72d9e01a718057674e18831f59268cb04d1d8366006fef94ef2f82(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ecb0fe679e602daa6ac1207d0a6ac37bca88ae0f2500e197ce4926e0367ce9a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fac5a647f7918f66aeb49af1b4b2becd40cf3cfd0177997fb8d6a178cfd809d(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterStorageLvpShareConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c29d733567917d3a9f199c1c77463dca5a92bd041d548720ba60987f9740a9a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd62bfb5eb1480fe2fc3f4d1b38bf1e4bfddc0bf702f454d74a59a812523aa2c(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterStorage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68a0efbf45e9c5adc756c0d9ca1deb40ff0a4fc8f4eb4f812632b317f55a2e39(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c61a0c3b0ce77c5dad60ec1609aea34cecfc2635eab1b6de0c0afe3798acadc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaf7418e2562d78a64892456c2fe00a5f169267c0f79e87ff37a61cc3f74370f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee0523eb4b2326a91b75236e105b6b8e5370d6f2b5a1a0d42149e0e85195149(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d756c4d8339cfc6a681a97a959d5c0fbca438da14a355fcc4bda8533bc065d54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82fbde8038abfb58f60d5db8c8fbc8bdeb1cc1f7979b61ac0638150d66779ed9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalAdminClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__848a2c1fb923da93aa42bd3fd720331065734385e00452dfb6de9333478f32f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8711a79a913cb67550395d2b1f23d12dd43572fed1b81a65cb1d30a429181dc9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__228d4cc4c0c4531c49ca17957c5811b7e0801fe7b06ece6a3a98fbbce3c1ab97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dbb1c21072ebad1257f69f2ddca84af9f531ca1447400ec1be342aedb65f2c7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9ea64c3782c06da390bda5cd744b9cbdb984cc5bb4e87d5135c7fd3153b195b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f90decef1d3f4a5a7ffd031e6b30f798d5da3690423229175e9e7af5028af5b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa0009728ff02da45aac51f359be5fc1a24e37afbd1ee955c1abcab7864fb73(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterValidationCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97628a5e80d08d89a47d905744c2e1a93ac2a2b4bf12c290b396f4f19da8acd1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__779af1d73e370ea38a61ea4ea28bfe991183fbba3d5811fb28ea5b7115e61981(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c62083a8909842e73dda84e062f52e96977a9b662463a9f8d6d2fb0067105e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34c533f900e1335a5030f69e3a5a4c29e50fd52f1eb97237f5f8d925cf93a840(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc1f8807bcac58f49bf959cb31141edc1de7444f81b266d27c244f88e335c31a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c6ec3761f6a47c564ef3e449dad892e08bba2fa9a20816c2ca3d53d38d33c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ebbde2a6f2bb5128c844861d50f0132a285e240986c23ed2e6c93a05c1e050(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterValidationCheckStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89851adc89a0f862e13083a8acd9d0d703c94b4c994e6f1a98dfccb739149ea6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94beabe25810cfd5c046ffa44519c21d0ec08d346f8540e92d2b2c423b15d33e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf6781dd211b43772d52bf022b49d1deec97786b4a4177a2f0d50ce6499bb0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de5ff36186ca90fdd90f148d3ca0f365e0a7a5b9334cf5b8d40ad9b5b79b2e88(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28450bd972debfba77983a70963dee43a06221e6e60256edeffa255f3d52b54a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5cfd91c1b21158d3904aae182681fcd20582c3d9bba4cf3d799600b0e451691(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b096514efac660498b25872b36adccbb62d2e1894a0d6d6f2d3176af04c04d8d(
    value: typing.Optional[GoogleGkeonpremBareMetalAdminClusterValidationCheckStatusResult],
) -> None:
    """Type checking stubs"""
    pass
