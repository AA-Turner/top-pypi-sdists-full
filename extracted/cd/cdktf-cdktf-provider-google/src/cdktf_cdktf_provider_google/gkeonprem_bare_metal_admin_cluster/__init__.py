r'''
# `google_gkeonprem_bare_metal_admin_cluster`

Refer to the Terraform Registry for docs: [`google_gkeonprem_bare_metal_admin_cluster`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster).
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


class GkeonpremBareMetalAdminCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster google_gkeonprem_bare_metal_admin_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bare_metal_version: typing.Optional[builtins.str] = None,
        cluster_operations: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterClusterOperations", typing.Dict[builtins.str, typing.Any]]] = None,
        control_plane: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterControlPlane", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        load_balancer: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterLoadBalancer", typing.Dict[builtins.str, typing.Any]]] = None,
        maintenance_config: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterMaintenanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        network_config: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_access_config: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterNodeAccessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_config: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        proxy: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        security_config: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterSecurityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        storage: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster google_gkeonprem_bare_metal_admin_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#location GkeonpremBareMetalAdminCluster#location}
        :param name: The bare metal admin cluster name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#name GkeonpremBareMetalAdminCluster#name}
        :param annotations: Annotations on the Bare Metal Admin Cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#annotations GkeonpremBareMetalAdminCluster#annotations}
        :param bare_metal_version: A human readable description of this Bare Metal Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#bare_metal_version GkeonpremBareMetalAdminCluster#bare_metal_version}
        :param cluster_operations: cluster_operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#cluster_operations GkeonpremBareMetalAdminCluster#cluster_operations}
        :param control_plane: control_plane block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#control_plane GkeonpremBareMetalAdminCluster#control_plane}
        :param description: A human readable description of this Bare Metal Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#description GkeonpremBareMetalAdminCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#id GkeonpremBareMetalAdminCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#load_balancer GkeonpremBareMetalAdminCluster#load_balancer}
        :param maintenance_config: maintenance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#maintenance_config GkeonpremBareMetalAdminCluster#maintenance_config}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#network_config GkeonpremBareMetalAdminCluster#network_config}
        :param node_access_config: node_access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#node_access_config GkeonpremBareMetalAdminCluster#node_access_config}
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#node_config GkeonpremBareMetalAdminCluster#node_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#project GkeonpremBareMetalAdminCluster#project}.
        :param proxy: proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#proxy GkeonpremBareMetalAdminCluster#proxy}
        :param security_config: security_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#security_config GkeonpremBareMetalAdminCluster#security_config}
        :param storage: storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#storage GkeonpremBareMetalAdminCluster#storage}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#timeouts GkeonpremBareMetalAdminCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5feb19fae1abc7844e1a3c100bb8658b8633975a01ab3877720445962084a9e1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GkeonpremBareMetalAdminClusterConfig(
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
        '''Generates CDKTF code for importing a GkeonpremBareMetalAdminCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GkeonpremBareMetalAdminCluster to import.
        :param import_from_id: The id of the existing GkeonpremBareMetalAdminCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GkeonpremBareMetalAdminCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaf5a39f0e48049bc8155ab9c8c25f614f9f413940b1e1610e66cd348a37c142)
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
        :param enable_application_logs: Whether collection of application logs/metrics should be enabled (in addition to system logs/metrics). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#enable_application_logs GkeonpremBareMetalAdminCluster#enable_application_logs}
        '''
        value = GkeonpremBareMetalAdminClusterClusterOperations(
            enable_application_logs=enable_application_logs
        )

        return typing.cast(None, jsii.invoke(self, "putClusterOperations", [value]))

    @jsii.member(jsii_name="putControlPlane")
    def put_control_plane(
        self,
        *,
        control_plane_node_pool_config: typing.Union["GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig", typing.Dict[builtins.str, typing.Any]],
        api_server_args: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalAdminClusterControlPlaneApiServerArgs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param control_plane_node_pool_config: control_plane_node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#control_plane_node_pool_config GkeonpremBareMetalAdminCluster#control_plane_node_pool_config}
        :param api_server_args: api_server_args block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#api_server_args GkeonpremBareMetalAdminCluster#api_server_args}
        '''
        value = GkeonpremBareMetalAdminClusterControlPlane(
            control_plane_node_pool_config=control_plane_node_pool_config,
            api_server_args=api_server_args,
        )

        return typing.cast(None, jsii.invoke(self, "putControlPlane", [value]))

    @jsii.member(jsii_name="putLoadBalancer")
    def put_load_balancer(
        self,
        *,
        port_config: typing.Union["GkeonpremBareMetalAdminClusterLoadBalancerPortConfig", typing.Dict[builtins.str, typing.Any]],
        vip_config: typing.Union["GkeonpremBareMetalAdminClusterLoadBalancerVipConfig", typing.Dict[builtins.str, typing.Any]],
        manual_lb_config: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param port_config: port_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#port_config GkeonpremBareMetalAdminCluster#port_config}
        :param vip_config: vip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#vip_config GkeonpremBareMetalAdminCluster#vip_config}
        :param manual_lb_config: manual_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#manual_lb_config GkeonpremBareMetalAdminCluster#manual_lb_config}
        '''
        value = GkeonpremBareMetalAdminClusterLoadBalancer(
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
        :param maintenance_address_cidr_blocks: All IPv4 address from these ranges will be placed into maintenance mode. Nodes in maintenance mode will be cordoned and drained. When both of these are true, the "baremetal.cluster.gke.io/maintenance" annotation will be set on the node resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#maintenance_address_cidr_blocks GkeonpremBareMetalAdminCluster#maintenance_address_cidr_blocks}
        '''
        value = GkeonpremBareMetalAdminClusterMaintenanceConfig(
            maintenance_address_cidr_blocks=maintenance_address_cidr_blocks
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenanceConfig", [value]))

    @jsii.member(jsii_name="putNetworkConfig")
    def put_network_config(
        self,
        *,
        island_mode_cidr: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param island_mode_cidr: island_mode_cidr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#island_mode_cidr GkeonpremBareMetalAdminCluster#island_mode_cidr}
        '''
        value = GkeonpremBareMetalAdminClusterNetworkConfig(
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
        :param login_user: LoginUser is the user name used to access node machines. It defaults to "root" if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#login_user GkeonpremBareMetalAdminCluster#login_user}
        '''
        value = GkeonpremBareMetalAdminClusterNodeAccessConfig(login_user=login_user)

        return typing.cast(None, jsii.invoke(self, "putNodeAccessConfig", [value]))

    @jsii.member(jsii_name="putNodeConfig")
    def put_node_config(
        self,
        *,
        max_pods_per_node: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_pods_per_node: The maximum number of pods a node can run. The size of the CIDR range assigned to the node will be derived from this parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#max_pods_per_node GkeonpremBareMetalAdminCluster#max_pods_per_node}
        '''
        value = GkeonpremBareMetalAdminClusterNodeConfig(
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
        :param uri: Specifies the address of your proxy server. For Example: http://domain WARNING: Do not provide credentials in the format of http://(username:password@)domain these will be rejected by the server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#uri GkeonpremBareMetalAdminCluster#uri}
        :param no_proxy: A list of IPs, hostnames, and domains that should skip the proxy. For example: ["127.0.0.1", "example.com", ".corp", "localhost"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#no_proxy GkeonpremBareMetalAdminCluster#no_proxy}
        '''
        value = GkeonpremBareMetalAdminClusterProxy(uri=uri, no_proxy=no_proxy)

        return typing.cast(None, jsii.invoke(self, "putProxy", [value]))

    @jsii.member(jsii_name="putSecurityConfig")
    def put_security_config(
        self,
        *,
        authorization: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterSecurityConfigAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#authorization GkeonpremBareMetalAdminCluster#authorization}
        '''
        value = GkeonpremBareMetalAdminClusterSecurityConfig(
            authorization=authorization
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityConfig", [value]))

    @jsii.member(jsii_name="putStorage")
    def put_storage(
        self,
        *,
        lvp_node_mounts_config: typing.Union["GkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig", typing.Dict[builtins.str, typing.Any]],
        lvp_share_config: typing.Union["GkeonpremBareMetalAdminClusterStorageLvpShareConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param lvp_node_mounts_config: lvp_node_mounts_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#lvp_node_mounts_config GkeonpremBareMetalAdminCluster#lvp_node_mounts_config}
        :param lvp_share_config: lvp_share_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#lvp_share_config GkeonpremBareMetalAdminCluster#lvp_share_config}
        '''
        value = GkeonpremBareMetalAdminClusterStorage(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#create GkeonpremBareMetalAdminCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#delete GkeonpremBareMetalAdminCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#update GkeonpremBareMetalAdminCluster#update}.
        '''
        value = GkeonpremBareMetalAdminClusterTimeouts(
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
    ) -> "GkeonpremBareMetalAdminClusterClusterOperationsOutputReference":
        return typing.cast("GkeonpremBareMetalAdminClusterClusterOperationsOutputReference", jsii.get(self, "clusterOperations"))

    @builtins.property
    @jsii.member(jsii_name="controlPlane")
    def control_plane(
        self,
    ) -> "GkeonpremBareMetalAdminClusterControlPlaneOutputReference":
        return typing.cast("GkeonpremBareMetalAdminClusterControlPlaneOutputReference", jsii.get(self, "controlPlane"))

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
    def fleet(self) -> "GkeonpremBareMetalAdminClusterFleetList":
        return typing.cast("GkeonpremBareMetalAdminClusterFleetList", jsii.get(self, "fleet"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(
        self,
    ) -> "GkeonpremBareMetalAdminClusterLoadBalancerOutputReference":
        return typing.cast("GkeonpremBareMetalAdminClusterLoadBalancerOutputReference", jsii.get(self, "loadBalancer"))

    @builtins.property
    @jsii.member(jsii_name="localName")
    def local_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localName"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceConfig")
    def maintenance_config(
        self,
    ) -> "GkeonpremBareMetalAdminClusterMaintenanceConfigOutputReference":
        return typing.cast("GkeonpremBareMetalAdminClusterMaintenanceConfigOutputReference", jsii.get(self, "maintenanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(
        self,
    ) -> "GkeonpremBareMetalAdminClusterNetworkConfigOutputReference":
        return typing.cast("GkeonpremBareMetalAdminClusterNetworkConfigOutputReference", jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodeAccessConfig")
    def node_access_config(
        self,
    ) -> "GkeonpremBareMetalAdminClusterNodeAccessConfigOutputReference":
        return typing.cast("GkeonpremBareMetalAdminClusterNodeAccessConfigOutputReference", jsii.get(self, "nodeAccessConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfig")
    def node_config(self) -> "GkeonpremBareMetalAdminClusterNodeConfigOutputReference":
        return typing.cast("GkeonpremBareMetalAdminClusterNodeConfigOutputReference", jsii.get(self, "nodeConfig"))

    @builtins.property
    @jsii.member(jsii_name="proxy")
    def proxy(self) -> "GkeonpremBareMetalAdminClusterProxyOutputReference":
        return typing.cast("GkeonpremBareMetalAdminClusterProxyOutputReference", jsii.get(self, "proxy"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="securityConfig")
    def security_config(
        self,
    ) -> "GkeonpremBareMetalAdminClusterSecurityConfigOutputReference":
        return typing.cast("GkeonpremBareMetalAdminClusterSecurityConfigOutputReference", jsii.get(self, "securityConfig"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "GkeonpremBareMetalAdminClusterStatusList":
        return typing.cast("GkeonpremBareMetalAdminClusterStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="storage")
    def storage(self) -> "GkeonpremBareMetalAdminClusterStorageOutputReference":
        return typing.cast("GkeonpremBareMetalAdminClusterStorageOutputReference", jsii.get(self, "storage"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GkeonpremBareMetalAdminClusterTimeoutsOutputReference":
        return typing.cast("GkeonpremBareMetalAdminClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    def validation_check(self) -> "GkeonpremBareMetalAdminClusterValidationCheckList":
        return typing.cast("GkeonpremBareMetalAdminClusterValidationCheckList", jsii.get(self, "validationCheck"))

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
    ) -> typing.Optional["GkeonpremBareMetalAdminClusterClusterOperations"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterClusterOperations"], jsii.get(self, "clusterOperationsInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneInput")
    def control_plane_input(
        self,
    ) -> typing.Optional["GkeonpremBareMetalAdminClusterControlPlane"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterControlPlane"], jsii.get(self, "controlPlaneInput"))

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
    ) -> typing.Optional["GkeonpremBareMetalAdminClusterLoadBalancer"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterLoadBalancer"], jsii.get(self, "loadBalancerInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceConfigInput")
    def maintenance_config_input(
        self,
    ) -> typing.Optional["GkeonpremBareMetalAdminClusterMaintenanceConfig"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterMaintenanceConfig"], jsii.get(self, "maintenanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigInput")
    def network_config_input(
        self,
    ) -> typing.Optional["GkeonpremBareMetalAdminClusterNetworkConfig"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterNetworkConfig"], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeAccessConfigInput")
    def node_access_config_input(
        self,
    ) -> typing.Optional["GkeonpremBareMetalAdminClusterNodeAccessConfig"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterNodeAccessConfig"], jsii.get(self, "nodeAccessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfigInput")
    def node_config_input(
        self,
    ) -> typing.Optional["GkeonpremBareMetalAdminClusterNodeConfig"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterNodeConfig"], jsii.get(self, "nodeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyInput")
    def proxy_input(self) -> typing.Optional["GkeonpremBareMetalAdminClusterProxy"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterProxy"], jsii.get(self, "proxyInput"))

    @builtins.property
    @jsii.member(jsii_name="securityConfigInput")
    def security_config_input(
        self,
    ) -> typing.Optional["GkeonpremBareMetalAdminClusterSecurityConfig"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterSecurityConfig"], jsii.get(self, "securityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="storageInput")
    def storage_input(self) -> typing.Optional["GkeonpremBareMetalAdminClusterStorage"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterStorage"], jsii.get(self, "storageInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeonpremBareMetalAdminClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeonpremBareMetalAdminClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0287608077d8a5b30acd69553450cf6f4dc4739730a1d1c047047e6298ab3122)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bareMetalVersion")
    def bare_metal_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bareMetalVersion"))

    @bare_metal_version.setter
    def bare_metal_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1e086ca489c0cc59762aa3c535cc4f673162fd6b1caa94c0bbf1340fe98915)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bareMetalVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68c591cb407e45a48dd0c83b1805b741114c4baa083e5e0e6179f2e5722ca734)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69b58b75969cbff703ffba90ead1ea79e935e1030e3033f6a1ff10a9635fd5a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a70536729bac1da0569f15c93e95ee7157deffe573de7ca571cf3c0c5ea2493e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d35b7a74eeff72b9328226aed14f02bd7788bb4ab22deb16d56c9e20860df0ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58557b09b0b2448b8078239b827f71c5941765acce3d3040f7c3bc248f3c6da0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterClusterOperations",
    jsii_struct_bases=[],
    name_mapping={"enable_application_logs": "enableApplicationLogs"},
)
class GkeonpremBareMetalAdminClusterClusterOperations:
    def __init__(
        self,
        *,
        enable_application_logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_application_logs: Whether collection of application logs/metrics should be enabled (in addition to system logs/metrics). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#enable_application_logs GkeonpremBareMetalAdminCluster#enable_application_logs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e8122edb80e0b6b8201bbb45eac72e99fda5538db1f9d8bed661a6d925eef73)
            check_type(argname="argument enable_application_logs", value=enable_application_logs, expected_type=type_hints["enable_application_logs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_application_logs is not None:
            self._values["enable_application_logs"] = enable_application_logs

    @builtins.property
    def enable_application_logs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether collection of application logs/metrics should be enabled (in addition to system logs/metrics).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#enable_application_logs GkeonpremBareMetalAdminCluster#enable_application_logs}
        '''
        result = self._values.get("enable_application_logs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterClusterOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalAdminClusterClusterOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterClusterOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17768e663fb018620bda899f3a3bf2601f0e42a48180db48708ee3effed2ccd4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df62f4d0e8470d911bb94e3d491733e44c990ad59f2767d2926f990fe6020eba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableApplicationLogs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterClusterOperations]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterClusterOperations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterClusterOperations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63682ad082013f7799a58997d1f00083cc4dd50ff40afc164575c9070e5fa15c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterConfig",
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
class GkeonpremBareMetalAdminClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cluster_operations: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterClusterOperations, typing.Dict[builtins.str, typing.Any]]] = None,
        control_plane: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterControlPlane", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        load_balancer: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterLoadBalancer", typing.Dict[builtins.str, typing.Any]]] = None,
        maintenance_config: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterMaintenanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        network_config: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_access_config: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterNodeAccessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_config: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        proxy: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        security_config: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterSecurityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        storage: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#location GkeonpremBareMetalAdminCluster#location}
        :param name: The bare metal admin cluster name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#name GkeonpremBareMetalAdminCluster#name}
        :param annotations: Annotations on the Bare Metal Admin Cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#annotations GkeonpremBareMetalAdminCluster#annotations}
        :param bare_metal_version: A human readable description of this Bare Metal Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#bare_metal_version GkeonpremBareMetalAdminCluster#bare_metal_version}
        :param cluster_operations: cluster_operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#cluster_operations GkeonpremBareMetalAdminCluster#cluster_operations}
        :param control_plane: control_plane block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#control_plane GkeonpremBareMetalAdminCluster#control_plane}
        :param description: A human readable description of this Bare Metal Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#description GkeonpremBareMetalAdminCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#id GkeonpremBareMetalAdminCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#load_balancer GkeonpremBareMetalAdminCluster#load_balancer}
        :param maintenance_config: maintenance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#maintenance_config GkeonpremBareMetalAdminCluster#maintenance_config}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#network_config GkeonpremBareMetalAdminCluster#network_config}
        :param node_access_config: node_access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#node_access_config GkeonpremBareMetalAdminCluster#node_access_config}
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#node_config GkeonpremBareMetalAdminCluster#node_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#project GkeonpremBareMetalAdminCluster#project}.
        :param proxy: proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#proxy GkeonpremBareMetalAdminCluster#proxy}
        :param security_config: security_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#security_config GkeonpremBareMetalAdminCluster#security_config}
        :param storage: storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#storage GkeonpremBareMetalAdminCluster#storage}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#timeouts GkeonpremBareMetalAdminCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cluster_operations, dict):
            cluster_operations = GkeonpremBareMetalAdminClusterClusterOperations(**cluster_operations)
        if isinstance(control_plane, dict):
            control_plane = GkeonpremBareMetalAdminClusterControlPlane(**control_plane)
        if isinstance(load_balancer, dict):
            load_balancer = GkeonpremBareMetalAdminClusterLoadBalancer(**load_balancer)
        if isinstance(maintenance_config, dict):
            maintenance_config = GkeonpremBareMetalAdminClusterMaintenanceConfig(**maintenance_config)
        if isinstance(network_config, dict):
            network_config = GkeonpremBareMetalAdminClusterNetworkConfig(**network_config)
        if isinstance(node_access_config, dict):
            node_access_config = GkeonpremBareMetalAdminClusterNodeAccessConfig(**node_access_config)
        if isinstance(node_config, dict):
            node_config = GkeonpremBareMetalAdminClusterNodeConfig(**node_config)
        if isinstance(proxy, dict):
            proxy = GkeonpremBareMetalAdminClusterProxy(**proxy)
        if isinstance(security_config, dict):
            security_config = GkeonpremBareMetalAdminClusterSecurityConfig(**security_config)
        if isinstance(storage, dict):
            storage = GkeonpremBareMetalAdminClusterStorage(**storage)
        if isinstance(timeouts, dict):
            timeouts = GkeonpremBareMetalAdminClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0635e1e5a2aad5f62158b8ddba9b4822ef536936f0e8b4f54f7b7766482fe93b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#location GkeonpremBareMetalAdminCluster#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The bare metal admin cluster name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#name GkeonpremBareMetalAdminCluster#name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#annotations GkeonpremBareMetalAdminCluster#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def bare_metal_version(self) -> typing.Optional[builtins.str]:
        '''A human readable description of this Bare Metal Admin Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#bare_metal_version GkeonpremBareMetalAdminCluster#bare_metal_version}
        '''
        result = self._values.get("bare_metal_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_operations(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterClusterOperations]:
        '''cluster_operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#cluster_operations GkeonpremBareMetalAdminCluster#cluster_operations}
        '''
        result = self._values.get("cluster_operations")
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterClusterOperations], result)

    @builtins.property
    def control_plane(
        self,
    ) -> typing.Optional["GkeonpremBareMetalAdminClusterControlPlane"]:
        '''control_plane block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#control_plane GkeonpremBareMetalAdminCluster#control_plane}
        '''
        result = self._values.get("control_plane")
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterControlPlane"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human readable description of this Bare Metal Admin Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#description GkeonpremBareMetalAdminCluster#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#id GkeonpremBareMetalAdminCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer(
        self,
    ) -> typing.Optional["GkeonpremBareMetalAdminClusterLoadBalancer"]:
        '''load_balancer block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#load_balancer GkeonpremBareMetalAdminCluster#load_balancer}
        '''
        result = self._values.get("load_balancer")
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterLoadBalancer"], result)

    @builtins.property
    def maintenance_config(
        self,
    ) -> typing.Optional["GkeonpremBareMetalAdminClusterMaintenanceConfig"]:
        '''maintenance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#maintenance_config GkeonpremBareMetalAdminCluster#maintenance_config}
        '''
        result = self._values.get("maintenance_config")
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterMaintenanceConfig"], result)

    @builtins.property
    def network_config(
        self,
    ) -> typing.Optional["GkeonpremBareMetalAdminClusterNetworkConfig"]:
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#network_config GkeonpremBareMetalAdminCluster#network_config}
        '''
        result = self._values.get("network_config")
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterNetworkConfig"], result)

    @builtins.property
    def node_access_config(
        self,
    ) -> typing.Optional["GkeonpremBareMetalAdminClusterNodeAccessConfig"]:
        '''node_access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#node_access_config GkeonpremBareMetalAdminCluster#node_access_config}
        '''
        result = self._values.get("node_access_config")
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterNodeAccessConfig"], result)

    @builtins.property
    def node_config(
        self,
    ) -> typing.Optional["GkeonpremBareMetalAdminClusterNodeConfig"]:
        '''node_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#node_config GkeonpremBareMetalAdminCluster#node_config}
        '''
        result = self._values.get("node_config")
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterNodeConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#project GkeonpremBareMetalAdminCluster#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy(self) -> typing.Optional["GkeonpremBareMetalAdminClusterProxy"]:
        '''proxy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#proxy GkeonpremBareMetalAdminCluster#proxy}
        '''
        result = self._values.get("proxy")
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterProxy"], result)

    @builtins.property
    def security_config(
        self,
    ) -> typing.Optional["GkeonpremBareMetalAdminClusterSecurityConfig"]:
        '''security_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#security_config GkeonpremBareMetalAdminCluster#security_config}
        '''
        result = self._values.get("security_config")
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterSecurityConfig"], result)

    @builtins.property
    def storage(self) -> typing.Optional["GkeonpremBareMetalAdminClusterStorage"]:
        '''storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#storage GkeonpremBareMetalAdminCluster#storage}
        '''
        result = self._values.get("storage")
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterStorage"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GkeonpremBareMetalAdminClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#timeouts GkeonpremBareMetalAdminCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterControlPlane",
    jsii_struct_bases=[],
    name_mapping={
        "control_plane_node_pool_config": "controlPlaneNodePoolConfig",
        "api_server_args": "apiServerArgs",
    },
)
class GkeonpremBareMetalAdminClusterControlPlane:
    def __init__(
        self,
        *,
        control_plane_node_pool_config: typing.Union["GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig", typing.Dict[builtins.str, typing.Any]],
        api_server_args: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalAdminClusterControlPlaneApiServerArgs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param control_plane_node_pool_config: control_plane_node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#control_plane_node_pool_config GkeonpremBareMetalAdminCluster#control_plane_node_pool_config}
        :param api_server_args: api_server_args block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#api_server_args GkeonpremBareMetalAdminCluster#api_server_args}
        '''
        if isinstance(control_plane_node_pool_config, dict):
            control_plane_node_pool_config = GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig(**control_plane_node_pool_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f62644435a0e04aa0fb660980b3ba01053ebfb9682e8ac37c5895102bd4d03d)
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
    ) -> "GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig":
        '''control_plane_node_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#control_plane_node_pool_config GkeonpremBareMetalAdminCluster#control_plane_node_pool_config}
        '''
        result = self._values.get("control_plane_node_pool_config")
        assert result is not None, "Required property 'control_plane_node_pool_config' is missing"
        return typing.cast("GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig", result)

    @builtins.property
    def api_server_args(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalAdminClusterControlPlaneApiServerArgs"]]]:
        '''api_server_args block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#api_server_args GkeonpremBareMetalAdminCluster#api_server_args}
        '''
        result = self._values.get("api_server_args")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalAdminClusterControlPlaneApiServerArgs"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterControlPlane(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterControlPlaneApiServerArgs",
    jsii_struct_bases=[],
    name_mapping={"argument": "argument", "value": "value"},
)
class GkeonpremBareMetalAdminClusterControlPlaneApiServerArgs:
    def __init__(self, *, argument: builtins.str, value: builtins.str) -> None:
        '''
        :param argument: The argument name as it appears on the API Server command line please make sure to remove the leading dashes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#argument GkeonpremBareMetalAdminCluster#argument}
        :param value: The value of the arg as it will be passed to the API Server command line. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#value GkeonpremBareMetalAdminCluster#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__712400dfcbc510fff613ba370e406b74b35dad55cf5fc40812e71445017800b2)
            check_type(argname="argument argument", value=argument, expected_type=type_hints["argument"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "argument": argument,
            "value": value,
        }

    @builtins.property
    def argument(self) -> builtins.str:
        '''The argument name as it appears on the API Server command line please make sure to remove the leading dashes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#argument GkeonpremBareMetalAdminCluster#argument}
        '''
        result = self._values.get("argument")
        assert result is not None, "Required property 'argument' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value of the arg as it will be passed to the API Server command line.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#value GkeonpremBareMetalAdminCluster#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterControlPlaneApiServerArgs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalAdminClusterControlPlaneApiServerArgsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterControlPlaneApiServerArgsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45f5516b789c249d1942a544e43c238ed9e6315eda6fed2341d4f8663888d9f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalAdminClusterControlPlaneApiServerArgsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fec32baa997f94ea1c9b52e940074054ad64a52e86d8bf3c9522f76eab5207d9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalAdminClusterControlPlaneApiServerArgsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0acd7edab8141ee593855dc52a4c31d86ba029013f74db7876de0fa372a8fb3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37f0dba9bcbcde3bbae5e534cd917a9c4c4f10d8f7739fb3e8e710f832c69feb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0664548f8d1621b16cb59cf83e1635aab6dd9b20538cde43e4d11a4006fb7ea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalAdminClusterControlPlaneApiServerArgs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalAdminClusterControlPlaneApiServerArgs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalAdminClusterControlPlaneApiServerArgs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aad41b9228fbceb90c30aec68c30e9e38c510c18f317624734c1448a26d97e3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalAdminClusterControlPlaneApiServerArgsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterControlPlaneApiServerArgsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4c3844d7f43c335ac30a8c15bec34f9872c6f625c55b9b2c7499555ea78fed0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d913055866f6edc0fb6ec3bb6670a2540efccad77fc824ca406d148bd99319fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "argument", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a69affbc42766578111f4cfa7895243ee5602ed40e01ae867f5e638c46a357a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalAdminClusterControlPlaneApiServerArgs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalAdminClusterControlPlaneApiServerArgs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalAdminClusterControlPlaneApiServerArgs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80dbc2728f56986ca781206f56c6d1bb6f6662253787bdc549ef66f8e1355f97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig",
    jsii_struct_bases=[],
    name_mapping={"node_pool_config": "nodePoolConfig"},
)
class GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig:
    def __init__(
        self,
        *,
        node_pool_config: typing.Union["GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param node_pool_config: node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#node_pool_config GkeonpremBareMetalAdminCluster#node_pool_config}
        '''
        if isinstance(node_pool_config, dict):
            node_pool_config = GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig(**node_pool_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d42fb2b7f66a891859f34c3ed08b19ce59e19ff5c46794c4b9d4c817fd464df)
            check_type(argname="argument node_pool_config", value=node_pool_config, expected_type=type_hints["node_pool_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "node_pool_config": node_pool_config,
        }

    @builtins.property
    def node_pool_config(
        self,
    ) -> "GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig":
        '''node_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#node_pool_config GkeonpremBareMetalAdminCluster#node_pool_config}
        '''
        result = self._values.get("node_pool_config")
        assert result is not None, "Required property 'node_pool_config' is missing"
        return typing.cast("GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig",
    jsii_struct_bases=[],
    name_mapping={
        "labels": "labels",
        "node_configs": "nodeConfigs",
        "operating_system": "operatingSystem",
        "taints": "taints",
    },
)
class GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operating_system: typing.Optional[builtins.str] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#labels GkeonpremBareMetalAdminCluster#labels}
        :param node_configs: node_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#node_configs GkeonpremBareMetalAdminCluster#node_configs}
        :param operating_system: Specifies the nodes operating system (default: LINUX). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#operating_system GkeonpremBareMetalAdminCluster#operating_system}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#taints GkeonpremBareMetalAdminCluster#taints}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3598f2b61556a35c48ec8e66c1732e436b8934a7d5b8a2c104f6256579d16d1e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#labels GkeonpremBareMetalAdminCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def node_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs"]]]:
        '''node_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#node_configs GkeonpremBareMetalAdminCluster#node_configs}
        '''
        result = self._values.get("node_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs"]]], result)

    @builtins.property
    def operating_system(self) -> typing.Optional[builtins.str]:
        '''Specifies the nodes operating system (default: LINUX).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#operating_system GkeonpremBareMetalAdminCluster#operating_system}
        '''
        result = self._values.get("operating_system")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def taints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints"]]]:
        '''taints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#taints GkeonpremBareMetalAdminCluster#taints}
        '''
        result = self._values.get("taints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels", "node_ip": "nodeIp"},
)
class GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_ip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#labels GkeonpremBareMetalAdminCluster#labels}
        :param node_ip: The default IPv4 address for SSH access and Kubernetes node. Example: 192.168.0.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#node_ip GkeonpremBareMetalAdminCluster#node_ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb2443611d8a4eb5b919152e3a5f1c8762a914e040d4d002503c530361e64e13)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#labels GkeonpremBareMetalAdminCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def node_ip(self) -> typing.Optional[builtins.str]:
        '''The default IPv4 address for SSH access and Kubernetes node. Example: 192.168.0.1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#node_ip GkeonpremBareMetalAdminCluster#node_ip}
        '''
        result = self._values.get("node_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__521d0ddce154a24b418ae20a16d541437ccc0e647648ed0eaefe5aef0f7604f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c046b8a9af9a599b84eb5194fc0a9b2b9f95775eb107c06a56a41e27670e1e09)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f44dc43430eb7c72d107ef6c9f9af35ecc311a24668a685f081fc6060673835)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6902011013441b6396178cf462ea3c4334e4e979c02dc6c74a6766740f26a599)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae3fb656257f8205ac94acb9951e04818a31b791b2ccf9fb56e87cb96c2e9169)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1936bfccd5b1bd90990174ca09e3fa4acb4e05dca6926715a5d49607c10c88ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__424050747fd419f1944c17298d4a615ef27eafad635053bbfc297416a8f33b65)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19058c06ab0b3730d425544c8231d3e20ee99e2bb44b137d43997efa76722dd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeIp")
    def node_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeIp"))

    @node_ip.setter
    def node_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ed0a4257d83fe0fdfd3ae298afe6b69f16fc2f111aae6c7986139f9ef010c2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6d8a023c0eddf799c768a9a4a0901b933f1354b5b724ea9641cb5cc1a6d974a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f9a9278fa3f5ae4ea0c43012e2e5ee06a8d08c7cc7f0a12e442a7ef91d4e722)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodeConfigs")
    def put_node_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46800f22bed20d1cce71451de4271ff707f32adf4d58b321b23fa50a5dd1ee1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeConfigs", [value]))

    @jsii.member(jsii_name="putTaints")
    def put_taints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b22d3073674d66f4c78c4cb3eec1b935dd3da17b763bcdf6517dc01b4a865c4)
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
    ) -> GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsList:
        return typing.cast(GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsList, jsii.get(self, "nodeConfigs"))

    @builtins.property
    @jsii.member(jsii_name="taints")
    def taints(
        self,
    ) -> "GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsList":
        return typing.cast("GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsList", jsii.get(self, "taints"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]], jsii.get(self, "nodeConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="operatingSystemInput")
    def operating_system_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatingSystemInput"))

    @builtins.property
    @jsii.member(jsii_name="taintsInput")
    def taints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints"]]], jsii.get(self, "taintsInput"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeeae3fd09cf8808cd79a9a10fd623082bcc3575a5a3871eab8e32c448b80e1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operatingSystem")
    def operating_system(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operatingSystem"))

    @operating_system.setter
    def operating_system(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f00c3510d958f8824f26227ac3e0662f1d4d90babd3349824eb13df5d14430e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operatingSystem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac929d500c3dcab6cdeb5fd23790200298223a81c8b1471fa179450880ea1c0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints",
    jsii_struct_bases=[],
    name_mapping={"effect": "effect", "key": "key", "value": "value"},
)
class GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints:
    def __init__(
        self,
        *,
        effect: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param effect: Specifies the nodes operating system (default: LINUX). Possible values: ["EFFECT_UNSPECIFIED", "PREFER_NO_SCHEDULE", "NO_EXECUTE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#effect GkeonpremBareMetalAdminCluster#effect}
        :param key: Key associated with the effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#key GkeonpremBareMetalAdminCluster#key}
        :param value: Value associated with the effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#value GkeonpremBareMetalAdminCluster#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2a198c51f551812f521021eafa0a5095c89e92d229b4c1d26a27190331e599b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#effect GkeonpremBareMetalAdminCluster#effect}
        '''
        result = self._values.get("effect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Key associated with the effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#key GkeonpremBareMetalAdminCluster#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value associated with the effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#value GkeonpremBareMetalAdminCluster#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1f050f43bab23f29d79867602e3d92a72f53bc8a340838700fa43c0b9a4984f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__976c8f09fc30b65f786b72ebfcea8c1e8d0e17670a1888d3b9b2fadd6c64863a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bb7ce7d4ed014f1b2dfb66efc986f7096a7b5f458879776aa09038bc4435810)
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
            type_hints = typing.get_type_hints(_typecheckingstub__622d3642e3b3a3e73df5b247cdcef7baa979f5dc0d3a29fcd2eed0abd7365847)
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
            type_hints = typing.get_type_hints(_typecheckingstub__13839645157383b4aa982ad83932aed306307ad95f6ba04c4c72bcf7136960cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__705aee55b2dbff443c99b525265cc1e290bb5fbfca3bc97d970ef121d31c330a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24231655448139a293b21db07bab82e71e7683eb6e3a6891a3d470e8a0971bc1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3bdb7f597ef5d5f43fa6434296bd5313aa1514f19fc982d8fc1c86c54bbe9af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80289c952f28af2ffe4a10b760adb6fc75c38699f977c257b433d6e93e907a26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8acecc99258971565930f868a109b32bcff569397afcbb971daf34e0d651e39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6771a415669fa0b1b0e9bad63d6891c0d5a0a8c0c8d28435f932d82af03f340)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8421f827bf4e279f55469b72726423e0270fc6f457950f472673fc38d14e6610)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodePoolConfig")
    def put_node_pool_config(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
        operating_system: typing.Optional[builtins.str] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#labels GkeonpremBareMetalAdminCluster#labels}
        :param node_configs: node_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#node_configs GkeonpremBareMetalAdminCluster#node_configs}
        :param operating_system: Specifies the nodes operating system (default: LINUX). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#operating_system GkeonpremBareMetalAdminCluster#operating_system}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#taints GkeonpremBareMetalAdminCluster#taints}
        '''
        value = GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig(
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
    ) -> GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigOutputReference:
        return typing.cast(GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigOutputReference, jsii.get(self, "nodePoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodePoolConfigInput")
    def node_pool_config_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig], jsii.get(self, "nodePoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__826fcf7f6f274a47183799d27cf8ab887112acb0679b58c9c366d5ba23287770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalAdminClusterControlPlaneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterControlPlaneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6aaa63b883fbf4a24ad0a72edb6ab3c34ebc142eb1fa8d0c3fcfaafc4cefb2dc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApiServerArgs")
    def put_api_server_args(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalAdminClusterControlPlaneApiServerArgs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e87ad7f372c0aeb04ddf11168a2d95504ad5cefadc237a9cf9a83d30b8f234da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putApiServerArgs", [value]))

    @jsii.member(jsii_name="putControlPlaneNodePoolConfig")
    def put_control_plane_node_pool_config(
        self,
        *,
        node_pool_config: typing.Union[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param node_pool_config: node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#node_pool_config GkeonpremBareMetalAdminCluster#node_pool_config}
        '''
        value = GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig(
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
    ) -> GkeonpremBareMetalAdminClusterControlPlaneApiServerArgsList:
        return typing.cast(GkeonpremBareMetalAdminClusterControlPlaneApiServerArgsList, jsii.get(self, "apiServerArgs"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneNodePoolConfig")
    def control_plane_node_pool_config(
        self,
    ) -> GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigOutputReference:
        return typing.cast(GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigOutputReference, jsii.get(self, "controlPlaneNodePoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="apiServerArgsInput")
    def api_server_args_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalAdminClusterControlPlaneApiServerArgs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalAdminClusterControlPlaneApiServerArgs]]], jsii.get(self, "apiServerArgsInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneNodePoolConfigInput")
    def control_plane_node_pool_config_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig], jsii.get(self, "controlPlaneNodePoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterControlPlane]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterControlPlane], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterControlPlane],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea5bce35a8e3897f64a7646ff9beb4f28aa7e6f0a10ab77662dd10fdd72f072c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterFleet",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremBareMetalAdminClusterFleet:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterFleet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalAdminClusterFleetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterFleetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0458776545e7f0e4e3824cdf1ea60b7d1468109e311ba4a12d0a139c18a026f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalAdminClusterFleetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b30aa4e08fef1e38765c4032e033cee311af2497b07a4c2f4754732d5a74bf6c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalAdminClusterFleetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8635bb04a1e51f18d4ee60b152609d2bd8b2f617c80c6bbc8de5921ee28bce86)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed81263091c873c4f8d1b830f877a82f1e75f6922b25c0d53ed7457449fdf61b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2cd6c17dc89c033c072a6ff1f18483fa490cb1193489ddb465c6ae7f630135d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalAdminClusterFleetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterFleetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f7fac4909c0ee3829d533725cc5511de7066f92c6a0b1225922fd5a97d1219a)
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
    def internal_value(self) -> typing.Optional[GkeonpremBareMetalAdminClusterFleet]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterFleet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterFleet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb8a337ef4c5d5adb106e0b55e7c3bcda39f32f3a756ea524dad7b9e8dc3972d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterLoadBalancer",
    jsii_struct_bases=[],
    name_mapping={
        "port_config": "portConfig",
        "vip_config": "vipConfig",
        "manual_lb_config": "manualLbConfig",
    },
)
class GkeonpremBareMetalAdminClusterLoadBalancer:
    def __init__(
        self,
        *,
        port_config: typing.Union["GkeonpremBareMetalAdminClusterLoadBalancerPortConfig", typing.Dict[builtins.str, typing.Any]],
        vip_config: typing.Union["GkeonpremBareMetalAdminClusterLoadBalancerVipConfig", typing.Dict[builtins.str, typing.Any]],
        manual_lb_config: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param port_config: port_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#port_config GkeonpremBareMetalAdminCluster#port_config}
        :param vip_config: vip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#vip_config GkeonpremBareMetalAdminCluster#vip_config}
        :param manual_lb_config: manual_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#manual_lb_config GkeonpremBareMetalAdminCluster#manual_lb_config}
        '''
        if isinstance(port_config, dict):
            port_config = GkeonpremBareMetalAdminClusterLoadBalancerPortConfig(**port_config)
        if isinstance(vip_config, dict):
            vip_config = GkeonpremBareMetalAdminClusterLoadBalancerVipConfig(**vip_config)
        if isinstance(manual_lb_config, dict):
            manual_lb_config = GkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig(**manual_lb_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc7f8d487a74eaee85c22272a746532cb908eaca1121f697026a838f0fad9e0c)
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
    def port_config(self) -> "GkeonpremBareMetalAdminClusterLoadBalancerPortConfig":
        '''port_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#port_config GkeonpremBareMetalAdminCluster#port_config}
        '''
        result = self._values.get("port_config")
        assert result is not None, "Required property 'port_config' is missing"
        return typing.cast("GkeonpremBareMetalAdminClusterLoadBalancerPortConfig", result)

    @builtins.property
    def vip_config(self) -> "GkeonpremBareMetalAdminClusterLoadBalancerVipConfig":
        '''vip_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#vip_config GkeonpremBareMetalAdminCluster#vip_config}
        '''
        result = self._values.get("vip_config")
        assert result is not None, "Required property 'vip_config' is missing"
        return typing.cast("GkeonpremBareMetalAdminClusterLoadBalancerVipConfig", result)

    @builtins.property
    def manual_lb_config(
        self,
    ) -> typing.Optional["GkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig"]:
        '''manual_lb_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#manual_lb_config GkeonpremBareMetalAdminCluster#manual_lb_config}
        '''
        result = self._values.get("manual_lb_config")
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterLoadBalancer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether manual load balancing is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#enabled GkeonpremBareMetalAdminCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f52869586b9a453de34339c9cb48a82bf019189135e6192b34411161975c7fd)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether manual load balancing is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#enabled GkeonpremBareMetalAdminCluster#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalAdminClusterLoadBalancerManualLbConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterLoadBalancerManualLbConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30ecefffb70f30236b7d209a7d3b441d9746a8e3a8ee60bd9e290a1ca5677460)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fe1acc5a61be5b73378a5a9ff8079b6e964c3683ef97e11c9a8b1d553144e95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a91ce71d52532455a9e94a91b4842bc11d548782acddce31e89d0a1f4816cf24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalAdminClusterLoadBalancerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterLoadBalancerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44c12ac21ab8009976ee67475bf72261280047e8163239ade6da7956a95b2808)
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
        :param enabled: Whether manual load balancing is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#enabled GkeonpremBareMetalAdminCluster#enabled}
        '''
        value = GkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putManualLbConfig", [value]))

    @jsii.member(jsii_name="putPortConfig")
    def put_port_config(self, *, control_plane_load_balancer_port: jsii.Number) -> None:
        '''
        :param control_plane_load_balancer_port: The port that control plane hosted load balancers will listen on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#control_plane_load_balancer_port GkeonpremBareMetalAdminCluster#control_plane_load_balancer_port}
        '''
        value = GkeonpremBareMetalAdminClusterLoadBalancerPortConfig(
            control_plane_load_balancer_port=control_plane_load_balancer_port
        )

        return typing.cast(None, jsii.invoke(self, "putPortConfig", [value]))

    @jsii.member(jsii_name="putVipConfig")
    def put_vip_config(self, *, control_plane_vip: builtins.str) -> None:
        '''
        :param control_plane_vip: The VIP which you previously set aside for the Kubernetes API of this Bare Metal Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#control_plane_vip GkeonpremBareMetalAdminCluster#control_plane_vip}
        '''
        value = GkeonpremBareMetalAdminClusterLoadBalancerVipConfig(
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
    ) -> GkeonpremBareMetalAdminClusterLoadBalancerManualLbConfigOutputReference:
        return typing.cast(GkeonpremBareMetalAdminClusterLoadBalancerManualLbConfigOutputReference, jsii.get(self, "manualLbConfig"))

    @builtins.property
    @jsii.member(jsii_name="portConfig")
    def port_config(
        self,
    ) -> "GkeonpremBareMetalAdminClusterLoadBalancerPortConfigOutputReference":
        return typing.cast("GkeonpremBareMetalAdminClusterLoadBalancerPortConfigOutputReference", jsii.get(self, "portConfig"))

    @builtins.property
    @jsii.member(jsii_name="vipConfig")
    def vip_config(
        self,
    ) -> "GkeonpremBareMetalAdminClusterLoadBalancerVipConfigOutputReference":
        return typing.cast("GkeonpremBareMetalAdminClusterLoadBalancerVipConfigOutputReference", jsii.get(self, "vipConfig"))

    @builtins.property
    @jsii.member(jsii_name="manualLbConfigInput")
    def manual_lb_config_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig], jsii.get(self, "manualLbConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="portConfigInput")
    def port_config_input(
        self,
    ) -> typing.Optional["GkeonpremBareMetalAdminClusterLoadBalancerPortConfig"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterLoadBalancerPortConfig"], jsii.get(self, "portConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="vipConfigInput")
    def vip_config_input(
        self,
    ) -> typing.Optional["GkeonpremBareMetalAdminClusterLoadBalancerVipConfig"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterLoadBalancerVipConfig"], jsii.get(self, "vipConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterLoadBalancer]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterLoadBalancer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterLoadBalancer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b76d40b690d20b40c632f9f02f10c5b30fda625b4a85558f5108d2553970834a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterLoadBalancerPortConfig",
    jsii_struct_bases=[],
    name_mapping={"control_plane_load_balancer_port": "controlPlaneLoadBalancerPort"},
)
class GkeonpremBareMetalAdminClusterLoadBalancerPortConfig:
    def __init__(self, *, control_plane_load_balancer_port: jsii.Number) -> None:
        '''
        :param control_plane_load_balancer_port: The port that control plane hosted load balancers will listen on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#control_plane_load_balancer_port GkeonpremBareMetalAdminCluster#control_plane_load_balancer_port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a5b1939dd22cf91fdabd09e013976ef22635423d8959cb2f34bf2688ae60168)
            check_type(argname="argument control_plane_load_balancer_port", value=control_plane_load_balancer_port, expected_type=type_hints["control_plane_load_balancer_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "control_plane_load_balancer_port": control_plane_load_balancer_port,
        }

    @builtins.property
    def control_plane_load_balancer_port(self) -> jsii.Number:
        '''The port that control plane hosted load balancers will listen on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#control_plane_load_balancer_port GkeonpremBareMetalAdminCluster#control_plane_load_balancer_port}
        '''
        result = self._values.get("control_plane_load_balancer_port")
        assert result is not None, "Required property 'control_plane_load_balancer_port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterLoadBalancerPortConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalAdminClusterLoadBalancerPortConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterLoadBalancerPortConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b3d842186009d070370f359749f98c26f6dc785cc03d4f1241ab47b6f9a972a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5d7221a916195e7a6d519a1d694f8448daccd4325e5be5b181e67e813dee18e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneLoadBalancerPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterLoadBalancerPortConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterLoadBalancerPortConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterLoadBalancerPortConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96c8cde2ab0aa034079adad5f349455b97b5b16bdf919eec75737b6ae29d4a49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterLoadBalancerVipConfig",
    jsii_struct_bases=[],
    name_mapping={"control_plane_vip": "controlPlaneVip"},
)
class GkeonpremBareMetalAdminClusterLoadBalancerVipConfig:
    def __init__(self, *, control_plane_vip: builtins.str) -> None:
        '''
        :param control_plane_vip: The VIP which you previously set aside for the Kubernetes API of this Bare Metal Admin Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#control_plane_vip GkeonpremBareMetalAdminCluster#control_plane_vip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04f9ac7a0429da62ceae9991ddb2b7b9f91601afd38fc9d5c25dc86614ef573c)
            check_type(argname="argument control_plane_vip", value=control_plane_vip, expected_type=type_hints["control_plane_vip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "control_plane_vip": control_plane_vip,
        }

    @builtins.property
    def control_plane_vip(self) -> builtins.str:
        '''The VIP which you previously set aside for the Kubernetes API of this Bare Metal Admin Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#control_plane_vip GkeonpremBareMetalAdminCluster#control_plane_vip}
        '''
        result = self._values.get("control_plane_vip")
        assert result is not None, "Required property 'control_plane_vip' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterLoadBalancerVipConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalAdminClusterLoadBalancerVipConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterLoadBalancerVipConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1125b70ad62a7f1a5a34dde408916b40775e8bcedb95edea8f9409c0a68314d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1e91648aec10875f34dea8b818a1658c8b488c40f2485604451765ad5e20086)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneVip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterLoadBalancerVipConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterLoadBalancerVipConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterLoadBalancerVipConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0085c80fe9d6b02a0bdbf154759ed0f611e781da6a0371973261c6ffa077365d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterMaintenanceConfig",
    jsii_struct_bases=[],
    name_mapping={"maintenance_address_cidr_blocks": "maintenanceAddressCidrBlocks"},
)
class GkeonpremBareMetalAdminClusterMaintenanceConfig:
    def __init__(
        self,
        *,
        maintenance_address_cidr_blocks: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param maintenance_address_cidr_blocks: All IPv4 address from these ranges will be placed into maintenance mode. Nodes in maintenance mode will be cordoned and drained. When both of these are true, the "baremetal.cluster.gke.io/maintenance" annotation will be set on the node resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#maintenance_address_cidr_blocks GkeonpremBareMetalAdminCluster#maintenance_address_cidr_blocks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__333718a7e4a0e5cf6b3c91eaf16b06e35ee3198b555d2b844c42cf21f946f564)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#maintenance_address_cidr_blocks GkeonpremBareMetalAdminCluster#maintenance_address_cidr_blocks}
        '''
        result = self._values.get("maintenance_address_cidr_blocks")
        assert result is not None, "Required property 'maintenance_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterMaintenanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalAdminClusterMaintenanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterMaintenanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c4a303a6690ca9d150bfa11aef197645f6de7c95ee558dd7713f49bb449399b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af8e47d1524925b91b143bfb2e40383b8a1c74cd3742ab1406f284e366599ee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterMaintenanceConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterMaintenanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterMaintenanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa6c1d95de45372968dc856072b7379e7cbf5c321fc8a5a8ffc60025ed54092f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={"island_mode_cidr": "islandModeCidr"},
)
class GkeonpremBareMetalAdminClusterNetworkConfig:
    def __init__(
        self,
        *,
        island_mode_cidr: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param island_mode_cidr: island_mode_cidr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#island_mode_cidr GkeonpremBareMetalAdminCluster#island_mode_cidr}
        '''
        if isinstance(island_mode_cidr, dict):
            island_mode_cidr = GkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr(**island_mode_cidr)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a31a7280829c72f9679c6a018178d14bbedfbbc329f78d67bff6aefdfb2949d4)
            check_type(argname="argument island_mode_cidr", value=island_mode_cidr, expected_type=type_hints["island_mode_cidr"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if island_mode_cidr is not None:
            self._values["island_mode_cidr"] = island_mode_cidr

    @builtins.property
    def island_mode_cidr(
        self,
    ) -> typing.Optional["GkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr"]:
        '''island_mode_cidr block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#island_mode_cidr GkeonpremBareMetalAdminCluster#island_mode_cidr}
        '''
        result = self._values.get("island_mode_cidr")
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr",
    jsii_struct_bases=[],
    name_mapping={
        "pod_address_cidr_blocks": "podAddressCidrBlocks",
        "service_address_cidr_blocks": "serviceAddressCidrBlocks",
    },
)
class GkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr:
    def __init__(
        self,
        *,
        pod_address_cidr_blocks: typing.Sequence[builtins.str],
        service_address_cidr_blocks: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param pod_address_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these ranges. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#pod_address_cidr_blocks GkeonpremBareMetalAdminCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these ranges. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#service_address_cidr_blocks GkeonpremBareMetalAdminCluster#service_address_cidr_blocks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2a193fb5e2885bdfef79b70e4c3576e01f20a3c92bdb1f97decc8603bf960d4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#pod_address_cidr_blocks GkeonpremBareMetalAdminCluster#pod_address_cidr_blocks}
        '''
        result = self._values.get("pod_address_cidr_blocks")
        assert result is not None, "Required property 'pod_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        '''All services in the cluster are assigned an RFC1918 IPv4 address from these ranges.

        This field cannot be changed after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#service_address_cidr_blocks GkeonpremBareMetalAdminCluster#service_address_cidr_blocks}
        '''
        result = self._values.get("service_address_cidr_blocks")
        assert result is not None, "Required property 'service_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidrOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidrOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2875ae5ecc5b61506e7781e6e28b7968c71d79b30b87b263131fad0c5ce47e3b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8330d0dcaf49be7f1dcc3f0655f10c7bf3f8dde8dc590e6ff442bc444298136e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAddressCidrBlocks")
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceAddressCidrBlocks"))

    @service_address_cidr_blocks.setter
    def service_address_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c0928f0f11a92d25d8b4a8d4203f9a817da043282637a2cb171ed0b64e878da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e180c454f801e9105dd098f5c2d52bb5df2fa552e653bf797d584c5d2ceea72a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalAdminClusterNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7de08035b6830f165a2fe4d108b3089d2a2d4e05132168bb121d008d3e138f88)
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
        :param pod_address_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these ranges. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#pod_address_cidr_blocks GkeonpremBareMetalAdminCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these ranges. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#service_address_cidr_blocks GkeonpremBareMetalAdminCluster#service_address_cidr_blocks}
        '''
        value = GkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr(
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
    ) -> GkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidrOutputReference:
        return typing.cast(GkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidrOutputReference, jsii.get(self, "islandModeCidr"))

    @builtins.property
    @jsii.member(jsii_name="islandModeCidrInput")
    def island_mode_cidr_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr], jsii.get(self, "islandModeCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterNetworkConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea8bc3c73fc4d170db692c566ab5c27beba7a09e6293a4377860c4cf975f504a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterNodeAccessConfig",
    jsii_struct_bases=[],
    name_mapping={"login_user": "loginUser"},
)
class GkeonpremBareMetalAdminClusterNodeAccessConfig:
    def __init__(self, *, login_user: typing.Optional[builtins.str] = None) -> None:
        '''
        :param login_user: LoginUser is the user name used to access node machines. It defaults to "root" if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#login_user GkeonpremBareMetalAdminCluster#login_user}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e59907242c6798c730a160f1e8795522382182d066dba641310d6125c67b606a)
            check_type(argname="argument login_user", value=login_user, expected_type=type_hints["login_user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if login_user is not None:
            self._values["login_user"] = login_user

    @builtins.property
    def login_user(self) -> typing.Optional[builtins.str]:
        '''LoginUser is the user name used to access node machines. It defaults to "root" if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#login_user GkeonpremBareMetalAdminCluster#login_user}
        '''
        result = self._values.get("login_user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterNodeAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalAdminClusterNodeAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterNodeAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__323f5eb1504adecfbe5805529744a0f456b35d3a2182abbbe6b6c2a28bb9eb35)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da1ed1c5f30e29504ea29853c03bda92db6b42a6ff8eed73a7f7cc9636b28030)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterNodeAccessConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterNodeAccessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterNodeAccessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6f0dd4a0e626b49bcac11dfd45f1a3fc93ce65d641e0bb21d46ae43b08a97e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterNodeConfig",
    jsii_struct_bases=[],
    name_mapping={"max_pods_per_node": "maxPodsPerNode"},
)
class GkeonpremBareMetalAdminClusterNodeConfig:
    def __init__(
        self,
        *,
        max_pods_per_node: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_pods_per_node: The maximum number of pods a node can run. The size of the CIDR range assigned to the node will be derived from this parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#max_pods_per_node GkeonpremBareMetalAdminCluster#max_pods_per_node}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaa7c73b67729b969451393e3074d4e4f74dab10108a85a9a0094c8e48063e1c)
            check_type(argname="argument max_pods_per_node", value=max_pods_per_node, expected_type=type_hints["max_pods_per_node"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_pods_per_node is not None:
            self._values["max_pods_per_node"] = max_pods_per_node

    @builtins.property
    def max_pods_per_node(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of pods a node can run.

        The size of the CIDR range
        assigned to the node will be derived from this parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#max_pods_per_node GkeonpremBareMetalAdminCluster#max_pods_per_node}
        '''
        result = self._values.get("max_pods_per_node")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterNodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalAdminClusterNodeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterNodeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f309878ab59b95db76421ca24c7b983962654539644e3720de0a05aa4fb5cfa4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43cf6f00203dbe4daa80192a1d285177cb1dc91bac16a650288c4597ae51fdd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPodsPerNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterNodeConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterNodeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterNodeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0dcb11c18d8c471e1965dd8c80639457af93b174d31c355ba6f20cff5c8a9e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterProxy",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "no_proxy": "noProxy"},
)
class GkeonpremBareMetalAdminClusterProxy:
    def __init__(
        self,
        *,
        uri: builtins.str,
        no_proxy: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param uri: Specifies the address of your proxy server. For Example: http://domain WARNING: Do not provide credentials in the format of http://(username:password@)domain these will be rejected by the server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#uri GkeonpremBareMetalAdminCluster#uri}
        :param no_proxy: A list of IPs, hostnames, and domains that should skip the proxy. For example: ["127.0.0.1", "example.com", ".corp", "localhost"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#no_proxy GkeonpremBareMetalAdminCluster#no_proxy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd997a41f34b4a2de287f6fc9edadf4f89e20d3e09749fa54793333b1bf942b4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#uri GkeonpremBareMetalAdminCluster#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def no_proxy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IPs, hostnames, and domains that should skip the proxy. For example: ["127.0.0.1", "example.com", ".corp", "localhost"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#no_proxy GkeonpremBareMetalAdminCluster#no_proxy}
        '''
        result = self._values.get("no_proxy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterProxy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalAdminClusterProxyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterProxyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d32747a5c97d023617fbd139d5cc509358d497a630b5644ce2be132ed480851d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cca8707240ce48ebc058d3aa195babfffe2b97ab5827822a698dacd0f41668d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noProxy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__378a4ffbdb68c6429bc6dd1a3ca190ee5b20ecb22f9a4363382bda49135fdfb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremBareMetalAdminClusterProxy]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterProxy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterProxy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fe0bd3aeb5019cdf6b960a578d3ee81471bf930b92f2e7e6b2f1e279ea9f2fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterSecurityConfig",
    jsii_struct_bases=[],
    name_mapping={"authorization": "authorization"},
)
class GkeonpremBareMetalAdminClusterSecurityConfig:
    def __init__(
        self,
        *,
        authorization: typing.Optional[typing.Union["GkeonpremBareMetalAdminClusterSecurityConfigAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#authorization GkeonpremBareMetalAdminCluster#authorization}
        '''
        if isinstance(authorization, dict):
            authorization = GkeonpremBareMetalAdminClusterSecurityConfigAuthorization(**authorization)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c78cea93068a4efa4a4ff4a0892acde4ade9db75b8e8f9362224f7ee118b9325)
            check_type(argname="argument authorization", value=authorization, expected_type=type_hints["authorization"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authorization is not None:
            self._values["authorization"] = authorization

    @builtins.property
    def authorization(
        self,
    ) -> typing.Optional["GkeonpremBareMetalAdminClusterSecurityConfigAuthorization"]:
        '''authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#authorization GkeonpremBareMetalAdminCluster#authorization}
        '''
        result = self._values.get("authorization")
        return typing.cast(typing.Optional["GkeonpremBareMetalAdminClusterSecurityConfigAuthorization"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterSecurityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterSecurityConfigAuthorization",
    jsii_struct_bases=[],
    name_mapping={"admin_users": "adminUsers"},
)
class GkeonpremBareMetalAdminClusterSecurityConfigAuthorization:
    def __init__(
        self,
        *,
        admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#admin_users GkeonpremBareMetalAdminCluster#admin_users}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b94ba9a1b799c02d37a19034f27e1bda1ac180efdcedf9b9aba32d1690b6e52f)
            check_type(argname="argument admin_users", value=admin_users, expected_type=type_hints["admin_users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_users": admin_users,
        }

    @builtins.property
    def admin_users(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers"]]:
        '''admin_users block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#admin_users GkeonpremBareMetalAdminCluster#admin_users}
        '''
        result = self._values.get("admin_users")
        assert result is not None, "Required property 'admin_users' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterSecurityConfigAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers",
    jsii_struct_bases=[],
    name_mapping={"username": "username"},
)
class GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers:
    def __init__(self, *, username: builtins.str) -> None:
        '''
        :param username: The name of the user, e.g. 'my-gcp-id@gmail.com'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#username GkeonpremBareMetalAdminCluster#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3de164aa8dba32518723732381f4b0c4ca1d419c006684fc834b01c5b38f7332)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
        }

    @builtins.property
    def username(self) -> builtins.str:
        '''The name of the user, e.g. 'my-gcp-id@gmail.com'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#username GkeonpremBareMetalAdminCluster#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__468ce94ee4e659410b563365ce65e89ce8f50f244a94b6d7502d820500524c15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2ad9e2ab2107cf82bacd94b0171eb208415d2f70c3ee102d76eebb77791ff4b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd7f16a29ae0e0fe445ea77c6f974e83caa0e9df81b385b804588d490a6e4105)
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
            type_hints = typing.get_type_hints(_typecheckingstub__41614e4bfdc57ec02d0154771b9f4b618339b95dab097e3ce6ec05b58b3fd4e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__988525aa99545bf51ea9f9ff51ba8d823783b90d83478b00a15327ce371c2f6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__687641f45e4a3022ba4edf456b1adc2872cc9c396bae778d18113404add23084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45172e087dfbede8a563801298ed41260bcc2bf9fa8aa634e585df67ea6873c3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b6bf46840dad1943bb8e14e986bcf2729132b762ffda69679f66018ca3b5e83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20dd26f82f9f29ef6fc186b96cff03d805c28235aa254855d1424769564b6d13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e83c53cddd0b77a186ba1692e7aa8889a68799f621a478a65bb93fc046617ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdminUsers")
    def put_admin_users(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9d14a8b9dcf76f19d040a82cdb2b2e9ccf5b35072807c1176596c87e3fe21ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdminUsers", [value]))

    @builtins.property
    @jsii.member(jsii_name="adminUsers")
    def admin_users(
        self,
    ) -> GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsersList:
        return typing.cast(GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsersList, jsii.get(self, "adminUsers"))

    @builtins.property
    @jsii.member(jsii_name="adminUsersInput")
    def admin_users_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers]]], jsii.get(self, "adminUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterSecurityConfigAuthorization]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterSecurityConfigAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterSecurityConfigAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c2cd31e4be2e27859f7ede6e0fa05ef6be7570b694c646b8dee173c8d0a36f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalAdminClusterSecurityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterSecurityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__828810672a4f68594a69c4e78886a2a685ad594fc7322f650ae0e8082dc7339b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthorization")
    def put_authorization(
        self,
        *,
        admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#admin_users GkeonpremBareMetalAdminCluster#admin_users}
        '''
        value = GkeonpremBareMetalAdminClusterSecurityConfigAuthorization(
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
    ) -> GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationOutputReference:
        return typing.cast(GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationOutputReference, jsii.get(self, "authorization"))

    @builtins.property
    @jsii.member(jsii_name="authorizationInput")
    def authorization_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterSecurityConfigAuthorization]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterSecurityConfigAuthorization], jsii.get(self, "authorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterSecurityConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterSecurityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterSecurityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c90fdeac29df4a4a7de2c714cd7a05b27e71215560ebd84288475e7b82a42d17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremBareMetalAdminClusterStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterStatusConditions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremBareMetalAdminClusterStatusConditions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterStatusConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalAdminClusterStatusConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterStatusConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a34b3bc652c47d7030db98f5bba9938f40b7c7f7446d696e8638766461c9b13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalAdminClusterStatusConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0882c0b2a0d01f392b720a5fc20b7cac13d6ad1b0744d8d79859124486f6401d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalAdminClusterStatusConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b23019881acbbed74abcfa1a0dac11a597c2f5d7f6e982e758d5831d10019113)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22c1e1d606633dafbb9a7fed9ad5d7ee533ee7189b151398f7dacf8411c31074)
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
            type_hints = typing.get_type_hints(_typecheckingstub__822f3c912b2e2c62c32788611f5cc7664ebf9eb0f57420b2381a290456dafbfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalAdminClusterStatusConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterStatusConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9b2ee080b9664e2a63af14192bf59b0877b3a1b02b16eac02a28c6412ba9b50)
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
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterStatusConditions]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterStatusConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterStatusConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6970e80c6b8d2d317aaa7c772a01157caa62b6ac7371ae05c3a64f613a09d2e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalAdminClusterStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e75b1a22dfe5a10d537a6759beab6469e925368da375003ef43ff6b871f3d632)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalAdminClusterStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fa21a73a9c05da75c92444f01e6ea2b8e04ddf5d092628b803db9cd67d335ac)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalAdminClusterStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b64c2311ef656fa5fab68baa75b78c3bddab15787783c8f87dd54f9f94f785b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc4f98b716f1dbe73dd879f502a16937c7d18a32696efb7820ed7b665701276e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83e22f25b67fb8300ca18ebccf29285ffe94595a07a940b20531b8922347b872)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalAdminClusterStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b877d46d13b4556b6785cea4cc56f3610647c7686144470331c021ffa3a5f1ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> GkeonpremBareMetalAdminClusterStatusConditionsList:
        return typing.cast(GkeonpremBareMetalAdminClusterStatusConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremBareMetalAdminClusterStatus]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fea5f66c2732251ed7bd4c0deddbf8ce415826b02eb9ae713e54e387fc837a2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterStorage",
    jsii_struct_bases=[],
    name_mapping={
        "lvp_node_mounts_config": "lvpNodeMountsConfig",
        "lvp_share_config": "lvpShareConfig",
    },
)
class GkeonpremBareMetalAdminClusterStorage:
    def __init__(
        self,
        *,
        lvp_node_mounts_config: typing.Union["GkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig", typing.Dict[builtins.str, typing.Any]],
        lvp_share_config: typing.Union["GkeonpremBareMetalAdminClusterStorageLvpShareConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param lvp_node_mounts_config: lvp_node_mounts_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#lvp_node_mounts_config GkeonpremBareMetalAdminCluster#lvp_node_mounts_config}
        :param lvp_share_config: lvp_share_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#lvp_share_config GkeonpremBareMetalAdminCluster#lvp_share_config}
        '''
        if isinstance(lvp_node_mounts_config, dict):
            lvp_node_mounts_config = GkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig(**lvp_node_mounts_config)
        if isinstance(lvp_share_config, dict):
            lvp_share_config = GkeonpremBareMetalAdminClusterStorageLvpShareConfig(**lvp_share_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2993874fa923d1c95dc10a87ab19eb4f6e3f8ce500e0fd070a372439db8050b)
            check_type(argname="argument lvp_node_mounts_config", value=lvp_node_mounts_config, expected_type=type_hints["lvp_node_mounts_config"])
            check_type(argname="argument lvp_share_config", value=lvp_share_config, expected_type=type_hints["lvp_share_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lvp_node_mounts_config": lvp_node_mounts_config,
            "lvp_share_config": lvp_share_config,
        }

    @builtins.property
    def lvp_node_mounts_config(
        self,
    ) -> "GkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig":
        '''lvp_node_mounts_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#lvp_node_mounts_config GkeonpremBareMetalAdminCluster#lvp_node_mounts_config}
        '''
        result = self._values.get("lvp_node_mounts_config")
        assert result is not None, "Required property 'lvp_node_mounts_config' is missing"
        return typing.cast("GkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig", result)

    @builtins.property
    def lvp_share_config(self) -> "GkeonpremBareMetalAdminClusterStorageLvpShareConfig":
        '''lvp_share_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#lvp_share_config GkeonpremBareMetalAdminCluster#lvp_share_config}
        '''
        result = self._values.get("lvp_share_config")
        assert result is not None, "Required property 'lvp_share_config' is missing"
        return typing.cast("GkeonpremBareMetalAdminClusterStorageLvpShareConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "storage_class": "storageClass"},
)
class GkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig:
    def __init__(self, *, path: builtins.str, storage_class: builtins.str) -> None:
        '''
        :param path: The host machine path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#path GkeonpremBareMetalAdminCluster#path}
        :param storage_class: The StorageClass name that PVs will be created with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#storage_class GkeonpremBareMetalAdminCluster#storage_class}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ebd04a3df7e333bae0cb523cf7447d4a5164637afdb7c41c97e380bfc347aa8)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "storage_class": storage_class,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''The host machine path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#path GkeonpremBareMetalAdminCluster#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_class(self) -> builtins.str:
        '''The StorageClass name that PVs will be created with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#storage_class GkeonpremBareMetalAdminCluster#storage_class}
        '''
        result = self._values.get("storage_class")
        assert result is not None, "Required property 'storage_class' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fe6c91d4505291390b232789ef06391a8a2e2b3f6c865f4bedfda944c91ef15)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de0152720732ca0c35c76ce3c99da5ef7c450b2980a32eb33b9265777b61e85d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageClass")
    def storage_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageClass"))

    @storage_class.setter
    def storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2106e4392a545d9c4d8c1ada51b3a7948600673052dd7c4fb64461d2e3f1c204)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94d285faf7d784cb9a39913c988063a30a4db64fde85ce9254a5c26a49cf359d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterStorageLvpShareConfig",
    jsii_struct_bases=[],
    name_mapping={
        "lvp_config": "lvpConfig",
        "shared_path_pv_count": "sharedPathPvCount",
    },
)
class GkeonpremBareMetalAdminClusterStorageLvpShareConfig:
    def __init__(
        self,
        *,
        lvp_config: typing.Union["GkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig", typing.Dict[builtins.str, typing.Any]],
        shared_path_pv_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param lvp_config: lvp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#lvp_config GkeonpremBareMetalAdminCluster#lvp_config}
        :param shared_path_pv_count: The number of subdirectories to create under path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#shared_path_pv_count GkeonpremBareMetalAdminCluster#shared_path_pv_count}
        '''
        if isinstance(lvp_config, dict):
            lvp_config = GkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig(**lvp_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0c4e270242414de2f89ac525407669cff474acbe8c1e771274d80829f027df4)
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
    ) -> "GkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig":
        '''lvp_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#lvp_config GkeonpremBareMetalAdminCluster#lvp_config}
        '''
        result = self._values.get("lvp_config")
        assert result is not None, "Required property 'lvp_config' is missing"
        return typing.cast("GkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig", result)

    @builtins.property
    def shared_path_pv_count(self) -> typing.Optional[jsii.Number]:
        '''The number of subdirectories to create under path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#shared_path_pv_count GkeonpremBareMetalAdminCluster#shared_path_pv_count}
        '''
        result = self._values.get("shared_path_pv_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterStorageLvpShareConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "storage_class": "storageClass"},
)
class GkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig:
    def __init__(self, *, path: builtins.str, storage_class: builtins.str) -> None:
        '''
        :param path: The host machine path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#path GkeonpremBareMetalAdminCluster#path}
        :param storage_class: The StorageClass name that PVs will be created with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#storage_class GkeonpremBareMetalAdminCluster#storage_class}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b496152f8f335dd98d51c8f37285da7d6a6126afbd3d808fef3d530a8a1aefc)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "storage_class": storage_class,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''The host machine path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#path GkeonpremBareMetalAdminCluster#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_class(self) -> builtins.str:
        '''The StorageClass name that PVs will be created with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#storage_class GkeonpremBareMetalAdminCluster#storage_class}
        '''
        result = self._values.get("storage_class")
        assert result is not None, "Required property 'storage_class' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2404e82c1185836f632fb3b072e6bb5514744b7da6d0629a8e7165d21732d00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e0c1e89445c0958f7791e8ebf10d46951f6528abeecf709e7e8ac0208aa48dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageClass")
    def storage_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageClass"))

    @storage_class.setter
    def storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54c5d61253e7740f860f453b336d345ce6f5efdca827ac9873b97d235c56ff4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed5dfd20b50c838607885e9d9b3d74905739566bcc433c0f49cda333ab0f40ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalAdminClusterStorageLvpShareConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterStorageLvpShareConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b2906f0e9b544845b117919400b54d6c4cb56bb790e8c478913b4de22c3bb08)
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
        :param path: The host machine path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#path GkeonpremBareMetalAdminCluster#path}
        :param storage_class: The StorageClass name that PVs will be created with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#storage_class GkeonpremBareMetalAdminCluster#storage_class}
        '''
        value = GkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig(
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
    ) -> GkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfigOutputReference:
        return typing.cast(GkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfigOutputReference, jsii.get(self, "lvpConfig"))

    @builtins.property
    @jsii.member(jsii_name="lvpConfigInput")
    def lvp_config_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig], jsii.get(self, "lvpConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__bb14a9f8b71092f43a1c8c73fe737b612ec1daf2532d634035030d2e94c7de93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedPathPvCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterStorageLvpShareConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterStorageLvpShareConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterStorageLvpShareConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0da1dbfb6f212bace24592871ffc8650d27024e2e5efd1de3084a2cfdf57f202)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalAdminClusterStorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterStorageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42a50390057a46efeacc51eec4d4d95963386b2e36c51d1e04493f5d2c2e6d63)
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
        :param path: The host machine path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#path GkeonpremBareMetalAdminCluster#path}
        :param storage_class: The StorageClass name that PVs will be created with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#storage_class GkeonpremBareMetalAdminCluster#storage_class}
        '''
        value = GkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig(
            path=path, storage_class=storage_class
        )

        return typing.cast(None, jsii.invoke(self, "putLvpNodeMountsConfig", [value]))

    @jsii.member(jsii_name="putLvpShareConfig")
    def put_lvp_share_config(
        self,
        *,
        lvp_config: typing.Union[GkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig, typing.Dict[builtins.str, typing.Any]],
        shared_path_pv_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param lvp_config: lvp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#lvp_config GkeonpremBareMetalAdminCluster#lvp_config}
        :param shared_path_pv_count: The number of subdirectories to create under path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#shared_path_pv_count GkeonpremBareMetalAdminCluster#shared_path_pv_count}
        '''
        value = GkeonpremBareMetalAdminClusterStorageLvpShareConfig(
            lvp_config=lvp_config, shared_path_pv_count=shared_path_pv_count
        )

        return typing.cast(None, jsii.invoke(self, "putLvpShareConfig", [value]))

    @builtins.property
    @jsii.member(jsii_name="lvpNodeMountsConfig")
    def lvp_node_mounts_config(
        self,
    ) -> GkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfigOutputReference:
        return typing.cast(GkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfigOutputReference, jsii.get(self, "lvpNodeMountsConfig"))

    @builtins.property
    @jsii.member(jsii_name="lvpShareConfig")
    def lvp_share_config(
        self,
    ) -> GkeonpremBareMetalAdminClusterStorageLvpShareConfigOutputReference:
        return typing.cast(GkeonpremBareMetalAdminClusterStorageLvpShareConfigOutputReference, jsii.get(self, "lvpShareConfig"))

    @builtins.property
    @jsii.member(jsii_name="lvpNodeMountsConfigInput")
    def lvp_node_mounts_config_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig], jsii.get(self, "lvpNodeMountsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="lvpShareConfigInput")
    def lvp_share_config_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterStorageLvpShareConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterStorageLvpShareConfig], jsii.get(self, "lvpShareConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremBareMetalAdminClusterStorage]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterStorage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterStorage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa6f3f0498d0b0ecdb84d0a74c11c39ada70f0615c1029f94e557360e75443ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GkeonpremBareMetalAdminClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#create GkeonpremBareMetalAdminCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#delete GkeonpremBareMetalAdminCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#update GkeonpremBareMetalAdminCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b578bd0ed8e9100935442b191908eaac51ea7fddebfd3a83ea5aeb659a268ea)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#create GkeonpremBareMetalAdminCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#delete GkeonpremBareMetalAdminCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_admin_cluster#update GkeonpremBareMetalAdminCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalAdminClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__680892ce7f843b99e15ca6948ff4d45541c0309145147963235a18008e8b6659)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44229b4116600eee414f4c341adccb42f280234160945c054e0a921605b95308)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04a96f30dc1597b8c4b87cad457a5a20aa9427a9f19d513b64b54f4e96c0176e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab7193cbfd3b8533d5259b644b1b551190ca43832b7e962321fd36936fd3e180)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalAdminClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalAdminClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalAdminClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__438aaf7875c77550c57dc52972c60c2af34ece2a05f8c6c06d356f9b24d22c92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterValidationCheck",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremBareMetalAdminClusterValidationCheck:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterValidationCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalAdminClusterValidationCheckList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterValidationCheckList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__988bea3b3f200c524baddd7d9f333e5108340d049959b8005f14b7582b7bb182)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalAdminClusterValidationCheckOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__892220268f8f8ade74d7fbb5a529001890c6bd5688ec96e825a1b04b9d13fb6e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalAdminClusterValidationCheckOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0924548bf6cb5da30ac6652067d72c4a6d36b6e8c3ffe9be9c45c64cfae40a20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e41b99684d834752ab04c8a89e10bf9e6a83bec50ce1a255b1f5f3c3ecef5bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6e8e634d11e919a692b10baf3324528ae7d6bb9c5088efced9d65735dd07fc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalAdminClusterValidationCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterValidationCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d488efa9cf80630f230e39fc3a63e8211df5300cbb8013851eb872d40fcc2aac)
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
    def status(self) -> "GkeonpremBareMetalAdminClusterValidationCheckStatusList":
        return typing.cast("GkeonpremBareMetalAdminClusterValidationCheckStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterValidationCheck]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterValidationCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterValidationCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__519af003529ae2a3348d8a4dd4fe32a649e4da55da368dee6a36acbfa922b108)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterValidationCheckStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremBareMetalAdminClusterValidationCheckStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterValidationCheckStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalAdminClusterValidationCheckStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterValidationCheckStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c33d4fbc5ffe3edbfda2cb962b714571ae383c6dc0a9d2aa9430db1604d6d952)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalAdminClusterValidationCheckStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db1bc51b63045e380f6b37bd349499c5ef55bfab22f38f4f63b3ca4da50d4ddd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalAdminClusterValidationCheckStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed91f3aa31272359ae39438461a927bf92ddb7531acfa8144e4eb29aafb63c31)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2ac2930c1246b0c5b67a2e7a8e3501c0d1b76a58286925499e4867a6ba2ab37)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa826f7f092d3ac56f24abd586e5abe1fd229ca76a9778041bafb1501ef59369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalAdminClusterValidationCheckStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterValidationCheckStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3be9233ff87afeb719949332f53801a7067b3290ae9c956056e8622f4214613)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="result")
    def result(self) -> "GkeonpremBareMetalAdminClusterValidationCheckStatusResultList":
        return typing.cast("GkeonpremBareMetalAdminClusterValidationCheckStatusResultList", jsii.get(self, "result"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterValidationCheckStatus]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterValidationCheckStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterValidationCheckStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fff0fa0f89078d41702124963b5d281b3e3c79cb931cc6c61d66a2d8d4c18813)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterValidationCheckStatusResult",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremBareMetalAdminClusterValidationCheckStatusResult:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalAdminClusterValidationCheckStatusResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalAdminClusterValidationCheckStatusResultList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterValidationCheckStatusResultList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10bdff88e593842024833226aac305c3ef7efcd263b248559dafa03af7640633)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalAdminClusterValidationCheckStatusResultOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c1b3cb739946c3abd710bf785a60030e8cb06af7e40944a18a4fcba1999c9d1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalAdminClusterValidationCheckStatusResultOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d5e8f8f4c17c61c497e9423c46c2c9e0e4b63d35bc2c097f43c0ea421594f07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37d7a9ac84b27668d49b83bf4ea8f4f9bd94d88485e8eb078c2fe9ac16d79cbd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fe65849113421987262f9aad668119e1a78171d259ad3322812c36981265b89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalAdminClusterValidationCheckStatusResultOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalAdminCluster.GkeonpremBareMetalAdminClusterValidationCheckStatusResultOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf0447c968387fd5de28dcc6fb9dd2f6cb5eb60f17bdaebb116724f3ba16d3f3)
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
    ) -> typing.Optional[GkeonpremBareMetalAdminClusterValidationCheckStatusResult]:
        return typing.cast(typing.Optional[GkeonpremBareMetalAdminClusterValidationCheckStatusResult], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalAdminClusterValidationCheckStatusResult],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c6d4300feeacea7e51571e9a3ce6f271c0ca822d5ae0f77e78c2787bdd916e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GkeonpremBareMetalAdminCluster",
    "GkeonpremBareMetalAdminClusterClusterOperations",
    "GkeonpremBareMetalAdminClusterClusterOperationsOutputReference",
    "GkeonpremBareMetalAdminClusterConfig",
    "GkeonpremBareMetalAdminClusterControlPlane",
    "GkeonpremBareMetalAdminClusterControlPlaneApiServerArgs",
    "GkeonpremBareMetalAdminClusterControlPlaneApiServerArgsList",
    "GkeonpremBareMetalAdminClusterControlPlaneApiServerArgsOutputReference",
    "GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig",
    "GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig",
    "GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs",
    "GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsList",
    "GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsOutputReference",
    "GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigOutputReference",
    "GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints",
    "GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsList",
    "GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsOutputReference",
    "GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigOutputReference",
    "GkeonpremBareMetalAdminClusterControlPlaneOutputReference",
    "GkeonpremBareMetalAdminClusterFleet",
    "GkeonpremBareMetalAdminClusterFleetList",
    "GkeonpremBareMetalAdminClusterFleetOutputReference",
    "GkeonpremBareMetalAdminClusterLoadBalancer",
    "GkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig",
    "GkeonpremBareMetalAdminClusterLoadBalancerManualLbConfigOutputReference",
    "GkeonpremBareMetalAdminClusterLoadBalancerOutputReference",
    "GkeonpremBareMetalAdminClusterLoadBalancerPortConfig",
    "GkeonpremBareMetalAdminClusterLoadBalancerPortConfigOutputReference",
    "GkeonpremBareMetalAdminClusterLoadBalancerVipConfig",
    "GkeonpremBareMetalAdminClusterLoadBalancerVipConfigOutputReference",
    "GkeonpremBareMetalAdminClusterMaintenanceConfig",
    "GkeonpremBareMetalAdminClusterMaintenanceConfigOutputReference",
    "GkeonpremBareMetalAdminClusterNetworkConfig",
    "GkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr",
    "GkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidrOutputReference",
    "GkeonpremBareMetalAdminClusterNetworkConfigOutputReference",
    "GkeonpremBareMetalAdminClusterNodeAccessConfig",
    "GkeonpremBareMetalAdminClusterNodeAccessConfigOutputReference",
    "GkeonpremBareMetalAdminClusterNodeConfig",
    "GkeonpremBareMetalAdminClusterNodeConfigOutputReference",
    "GkeonpremBareMetalAdminClusterProxy",
    "GkeonpremBareMetalAdminClusterProxyOutputReference",
    "GkeonpremBareMetalAdminClusterSecurityConfig",
    "GkeonpremBareMetalAdminClusterSecurityConfigAuthorization",
    "GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers",
    "GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsersList",
    "GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsersOutputReference",
    "GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationOutputReference",
    "GkeonpremBareMetalAdminClusterSecurityConfigOutputReference",
    "GkeonpremBareMetalAdminClusterStatus",
    "GkeonpremBareMetalAdminClusterStatusConditions",
    "GkeonpremBareMetalAdminClusterStatusConditionsList",
    "GkeonpremBareMetalAdminClusterStatusConditionsOutputReference",
    "GkeonpremBareMetalAdminClusterStatusList",
    "GkeonpremBareMetalAdminClusterStatusOutputReference",
    "GkeonpremBareMetalAdminClusterStorage",
    "GkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig",
    "GkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfigOutputReference",
    "GkeonpremBareMetalAdminClusterStorageLvpShareConfig",
    "GkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig",
    "GkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfigOutputReference",
    "GkeonpremBareMetalAdminClusterStorageLvpShareConfigOutputReference",
    "GkeonpremBareMetalAdminClusterStorageOutputReference",
    "GkeonpremBareMetalAdminClusterTimeouts",
    "GkeonpremBareMetalAdminClusterTimeoutsOutputReference",
    "GkeonpremBareMetalAdminClusterValidationCheck",
    "GkeonpremBareMetalAdminClusterValidationCheckList",
    "GkeonpremBareMetalAdminClusterValidationCheckOutputReference",
    "GkeonpremBareMetalAdminClusterValidationCheckStatus",
    "GkeonpremBareMetalAdminClusterValidationCheckStatusList",
    "GkeonpremBareMetalAdminClusterValidationCheckStatusOutputReference",
    "GkeonpremBareMetalAdminClusterValidationCheckStatusResult",
    "GkeonpremBareMetalAdminClusterValidationCheckStatusResultList",
    "GkeonpremBareMetalAdminClusterValidationCheckStatusResultOutputReference",
]

publication.publish()

def _typecheckingstub__5feb19fae1abc7844e1a3c100bb8658b8633975a01ab3877720445962084a9e1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    bare_metal_version: typing.Optional[builtins.str] = None,
    cluster_operations: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterClusterOperations, typing.Dict[builtins.str, typing.Any]]] = None,
    control_plane: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterControlPlane, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    load_balancer: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterLoadBalancer, typing.Dict[builtins.str, typing.Any]]] = None,
    maintenance_config: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterMaintenanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    network_config: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_access_config: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterNodeAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_config: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    proxy: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    security_config: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterSecurityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    storage: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__aaf5a39f0e48049bc8155ab9c8c25f614f9f413940b1e1610e66cd348a37c142(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0287608077d8a5b30acd69553450cf6f4dc4739730a1d1c047047e6298ab3122(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1e086ca489c0cc59762aa3c535cc4f673162fd6b1caa94c0bbf1340fe98915(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c591cb407e45a48dd0c83b1805b741114c4baa083e5e0e6179f2e5722ca734(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b58b75969cbff703ffba90ead1ea79e935e1030e3033f6a1ff10a9635fd5a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a70536729bac1da0569f15c93e95ee7157deffe573de7ca571cf3c0c5ea2493e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d35b7a74eeff72b9328226aed14f02bd7788bb4ab22deb16d56c9e20860df0ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58557b09b0b2448b8078239b827f71c5941765acce3d3040f7c3bc248f3c6da0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8122edb80e0b6b8201bbb45eac72e99fda5538db1f9d8bed661a6d925eef73(
    *,
    enable_application_logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17768e663fb018620bda899f3a3bf2601f0e42a48180db48708ee3effed2ccd4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df62f4d0e8470d911bb94e3d491733e44c990ad59f2767d2926f990fe6020eba(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63682ad082013f7799a58997d1f00083cc4dd50ff40afc164575c9070e5fa15c(
    value: typing.Optional[GkeonpremBareMetalAdminClusterClusterOperations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0635e1e5a2aad5f62158b8ddba9b4822ef536936f0e8b4f54f7b7766482fe93b(
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
    cluster_operations: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterClusterOperations, typing.Dict[builtins.str, typing.Any]]] = None,
    control_plane: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterControlPlane, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    load_balancer: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterLoadBalancer, typing.Dict[builtins.str, typing.Any]]] = None,
    maintenance_config: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterMaintenanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    network_config: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_access_config: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterNodeAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_config: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    proxy: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    security_config: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterSecurityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    storage: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f62644435a0e04aa0fb660980b3ba01053ebfb9682e8ac37c5895102bd4d03d(
    *,
    control_plane_node_pool_config: typing.Union[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig, typing.Dict[builtins.str, typing.Any]],
    api_server_args: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalAdminClusterControlPlaneApiServerArgs, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__712400dfcbc510fff613ba370e406b74b35dad55cf5fc40812e71445017800b2(
    *,
    argument: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f5516b789c249d1942a544e43c238ed9e6315eda6fed2341d4f8663888d9f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec32baa997f94ea1c9b52e940074054ad64a52e86d8bf3c9522f76eab5207d9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0acd7edab8141ee593855dc52a4c31d86ba029013f74db7876de0fa372a8fb3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f0dba9bcbcde3bbae5e534cd917a9c4c4f10d8f7739fb3e8e710f832c69feb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0664548f8d1621b16cb59cf83e1635aab6dd9b20538cde43e4d11a4006fb7ea1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad41b9228fbceb90c30aec68c30e9e38c510c18f317624734c1448a26d97e3b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalAdminClusterControlPlaneApiServerArgs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4c3844d7f43c335ac30a8c15bec34f9872c6f625c55b9b2c7499555ea78fed0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d913055866f6edc0fb6ec3bb6670a2540efccad77fc824ca406d148bd99319fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a69affbc42766578111f4cfa7895243ee5602ed40e01ae867f5e638c46a357a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80dbc2728f56986ca781206f56c6d1bb6f6662253787bdc549ef66f8e1355f97(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalAdminClusterControlPlaneApiServerArgs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d42fb2b7f66a891859f34c3ed08b19ce59e19ff5c46794c4b9d4c817fd464df(
    *,
    node_pool_config: typing.Union[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3598f2b61556a35c48ec8e66c1732e436b8934a7d5b8a2c104f6256579d16d1e(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    operating_system: typing.Optional[builtins.str] = None,
    taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb2443611d8a4eb5b919152e3a5f1c8762a914e040d4d002503c530361e64e13(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__521d0ddce154a24b418ae20a16d541437ccc0e647648ed0eaefe5aef0f7604f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c046b8a9af9a599b84eb5194fc0a9b2b9f95775eb107c06a56a41e27670e1e09(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f44dc43430eb7c72d107ef6c9f9af35ecc311a24668a685f081fc6060673835(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6902011013441b6396178cf462ea3c4334e4e979c02dc6c74a6766740f26a599(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae3fb656257f8205ac94acb9951e04818a31b791b2ccf9fb56e87cb96c2e9169(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1936bfccd5b1bd90990174ca09e3fa4acb4e05dca6926715a5d49607c10c88ec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424050747fd419f1944c17298d4a615ef27eafad635053bbfc297416a8f33b65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19058c06ab0b3730d425544c8231d3e20ee99e2bb44b137d43997efa76722dd4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ed0a4257d83fe0fdfd3ae298afe6b69f16fc2f111aae6c7986139f9ef010c2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6d8a023c0eddf799c768a9a4a0901b933f1354b5b724ea9641cb5cc1a6d974a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f9a9278fa3f5ae4ea0c43012e2e5ee06a8d08c7cc7f0a12e442a7ef91d4e722(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46800f22bed20d1cce71451de4271ff707f32adf4d58b321b23fa50a5dd1ee1b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b22d3073674d66f4c78c4cb3eec1b935dd3da17b763bcdf6517dc01b4a865c4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeeae3fd09cf8808cd79a9a10fd623082bcc3575a5a3871eab8e32c448b80e1a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f00c3510d958f8824f26227ac3e0662f1d4d90babd3349824eb13df5d14430e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac929d500c3dcab6cdeb5fd23790200298223a81c8b1471fa179450880ea1c0c(
    value: typing.Optional[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2a198c51f551812f521021eafa0a5095c89e92d229b4c1d26a27190331e599b(
    *,
    effect: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f050f43bab23f29d79867602e3d92a72f53bc8a340838700fa43c0b9a4984f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__976c8f09fc30b65f786b72ebfcea8c1e8d0e17670a1888d3b9b2fadd6c64863a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb7ce7d4ed014f1b2dfb66efc986f7096a7b5f458879776aa09038bc4435810(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622d3642e3b3a3e73df5b247cdcef7baa979f5dc0d3a29fcd2eed0abd7365847(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13839645157383b4aa982ad83932aed306307ad95f6ba04c4c72bcf7136960cf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__705aee55b2dbff443c99b525265cc1e290bb5fbfca3bc97d970ef121d31c330a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24231655448139a293b21db07bab82e71e7683eb6e3a6891a3d470e8a0971bc1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3bdb7f597ef5d5f43fa6434296bd5313aa1514f19fc982d8fc1c86c54bbe9af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80289c952f28af2ffe4a10b760adb6fc75c38699f977c257b433d6e93e907a26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8acecc99258971565930f868a109b32bcff569397afcbb971daf34e0d651e39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6771a415669fa0b1b0e9bad63d6891c0d5a0a8c0c8d28435f932d82af03f340(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8421f827bf4e279f55469b72726423e0270fc6f457950f472673fc38d14e6610(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826fcf7f6f274a47183799d27cf8ab887112acb0679b58c9c366d5ba23287770(
    value: typing.Optional[GkeonpremBareMetalAdminClusterControlPlaneControlPlaneNodePoolConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aaa63b883fbf4a24ad0a72edb6ab3c34ebc142eb1fa8d0c3fcfaafc4cefb2dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e87ad7f372c0aeb04ddf11168a2d95504ad5cefadc237a9cf9a83d30b8f234da(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalAdminClusterControlPlaneApiServerArgs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea5bce35a8e3897f64a7646ff9beb4f28aa7e6f0a10ab77662dd10fdd72f072c(
    value: typing.Optional[GkeonpremBareMetalAdminClusterControlPlane],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0458776545e7f0e4e3824cdf1ea60b7d1468109e311ba4a12d0a139c18a026f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b30aa4e08fef1e38765c4032e033cee311af2497b07a4c2f4754732d5a74bf6c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8635bb04a1e51f18d4ee60b152609d2bd8b2f617c80c6bbc8de5921ee28bce86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed81263091c873c4f8d1b830f877a82f1e75f6922b25c0d53ed7457449fdf61b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2cd6c17dc89c033c072a6ff1f18483fa490cb1193489ddb465c6ae7f630135d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f7fac4909c0ee3829d533725cc5511de7066f92c6a0b1225922fd5a97d1219a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb8a337ef4c5d5adb106e0b55e7c3bcda39f32f3a756ea524dad7b9e8dc3972d(
    value: typing.Optional[GkeonpremBareMetalAdminClusterFleet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc7f8d487a74eaee85c22272a746532cb908eaca1121f697026a838f0fad9e0c(
    *,
    port_config: typing.Union[GkeonpremBareMetalAdminClusterLoadBalancerPortConfig, typing.Dict[builtins.str, typing.Any]],
    vip_config: typing.Union[GkeonpremBareMetalAdminClusterLoadBalancerVipConfig, typing.Dict[builtins.str, typing.Any]],
    manual_lb_config: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f52869586b9a453de34339c9cb48a82bf019189135e6192b34411161975c7fd(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ecefffb70f30236b7d209a7d3b441d9746a8e3a8ee60bd9e290a1ca5677460(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe1acc5a61be5b73378a5a9ff8079b6e964c3683ef97e11c9a8b1d553144e95(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a91ce71d52532455a9e94a91b4842bc11d548782acddce31e89d0a1f4816cf24(
    value: typing.Optional[GkeonpremBareMetalAdminClusterLoadBalancerManualLbConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44c12ac21ab8009976ee67475bf72261280047e8163239ade6da7956a95b2808(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b76d40b690d20b40c632f9f02f10c5b30fda625b4a85558f5108d2553970834a(
    value: typing.Optional[GkeonpremBareMetalAdminClusterLoadBalancer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a5b1939dd22cf91fdabd09e013976ef22635423d8959cb2f34bf2688ae60168(
    *,
    control_plane_load_balancer_port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b3d842186009d070370f359749f98c26f6dc785cc03d4f1241ab47b6f9a972a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d7221a916195e7a6d519a1d694f8448daccd4325e5be5b181e67e813dee18e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c8cde2ab0aa034079adad5f349455b97b5b16bdf919eec75737b6ae29d4a49(
    value: typing.Optional[GkeonpremBareMetalAdminClusterLoadBalancerPortConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f9ac7a0429da62ceae9991ddb2b7b9f91601afd38fc9d5c25dc86614ef573c(
    *,
    control_plane_vip: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1125b70ad62a7f1a5a34dde408916b40775e8bcedb95edea8f9409c0a68314d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e91648aec10875f34dea8b818a1658c8b488c40f2485604451765ad5e20086(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0085c80fe9d6b02a0bdbf154759ed0f611e781da6a0371973261c6ffa077365d(
    value: typing.Optional[GkeonpremBareMetalAdminClusterLoadBalancerVipConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__333718a7e4a0e5cf6b3c91eaf16b06e35ee3198b555d2b844c42cf21f946f564(
    *,
    maintenance_address_cidr_blocks: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c4a303a6690ca9d150bfa11aef197645f6de7c95ee558dd7713f49bb449399b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af8e47d1524925b91b143bfb2e40383b8a1c74cd3742ab1406f284e366599ee9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa6c1d95de45372968dc856072b7379e7cbf5c321fc8a5a8ffc60025ed54092f(
    value: typing.Optional[GkeonpremBareMetalAdminClusterMaintenanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31a7280829c72f9679c6a018178d14bbedfbbc329f78d67bff6aefdfb2949d4(
    *,
    island_mode_cidr: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2a193fb5e2885bdfef79b70e4c3576e01f20a3c92bdb1f97decc8603bf960d4(
    *,
    pod_address_cidr_blocks: typing.Sequence[builtins.str],
    service_address_cidr_blocks: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2875ae5ecc5b61506e7781e6e28b7968c71d79b30b87b263131fad0c5ce47e3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8330d0dcaf49be7f1dcc3f0655f10c7bf3f8dde8dc590e6ff442bc444298136e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0928f0f11a92d25d8b4a8d4203f9a817da043282637a2cb171ed0b64e878da(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e180c454f801e9105dd098f5c2d52bb5df2fa552e653bf797d584c5d2ceea72a(
    value: typing.Optional[GkeonpremBareMetalAdminClusterNetworkConfigIslandModeCidr],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de08035b6830f165a2fe4d108b3089d2a2d4e05132168bb121d008d3e138f88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea8bc3c73fc4d170db692c566ab5c27beba7a09e6293a4377860c4cf975f504a(
    value: typing.Optional[GkeonpremBareMetalAdminClusterNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e59907242c6798c730a160f1e8795522382182d066dba641310d6125c67b606a(
    *,
    login_user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__323f5eb1504adecfbe5805529744a0f456b35d3a2182abbbe6b6c2a28bb9eb35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1ed1c5f30e29504ea29853c03bda92db6b42a6ff8eed73a7f7cc9636b28030(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6f0dd4a0e626b49bcac11dfd45f1a3fc93ce65d641e0bb21d46ae43b08a97e5(
    value: typing.Optional[GkeonpremBareMetalAdminClusterNodeAccessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa7c73b67729b969451393e3074d4e4f74dab10108a85a9a0094c8e48063e1c(
    *,
    max_pods_per_node: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f309878ab59b95db76421ca24c7b983962654539644e3720de0a05aa4fb5cfa4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43cf6f00203dbe4daa80192a1d285177cb1dc91bac16a650288c4597ae51fdd2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0dcb11c18d8c471e1965dd8c80639457af93b174d31c355ba6f20cff5c8a9e8(
    value: typing.Optional[GkeonpremBareMetalAdminClusterNodeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd997a41f34b4a2de287f6fc9edadf4f89e20d3e09749fa54793333b1bf942b4(
    *,
    uri: builtins.str,
    no_proxy: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d32747a5c97d023617fbd139d5cc509358d497a630b5644ce2be132ed480851d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cca8707240ce48ebc058d3aa195babfffe2b97ab5827822a698dacd0f41668d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__378a4ffbdb68c6429bc6dd1a3ca190ee5b20ecb22f9a4363382bda49135fdfb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe0bd3aeb5019cdf6b960a578d3ee81471bf930b92f2e7e6b2f1e279ea9f2fc(
    value: typing.Optional[GkeonpremBareMetalAdminClusterProxy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c78cea93068a4efa4a4ff4a0892acde4ade9db75b8e8f9362224f7ee118b9325(
    *,
    authorization: typing.Optional[typing.Union[GkeonpremBareMetalAdminClusterSecurityConfigAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b94ba9a1b799c02d37a19034f27e1bda1ac180efdcedf9b9aba32d1690b6e52f(
    *,
    admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3de164aa8dba32518723732381f4b0c4ca1d419c006684fc834b01c5b38f7332(
    *,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468ce94ee4e659410b563365ce65e89ce8f50f244a94b6d7502d820500524c15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2ad9e2ab2107cf82bacd94b0171eb208415d2f70c3ee102d76eebb77791ff4b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd7f16a29ae0e0fe445ea77c6f974e83caa0e9df81b385b804588d490a6e4105(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41614e4bfdc57ec02d0154771b9f4b618339b95dab097e3ce6ec05b58b3fd4e7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__988525aa99545bf51ea9f9ff51ba8d823783b90d83478b00a15327ce371c2f6b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__687641f45e4a3022ba4edf456b1adc2872cc9c396bae778d18113404add23084(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45172e087dfbede8a563801298ed41260bcc2bf9fa8aa634e585df67ea6873c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b6bf46840dad1943bb8e14e986bcf2729132b762ffda69679f66018ca3b5e83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20dd26f82f9f29ef6fc186b96cff03d805c28235aa254855d1424769564b6d13(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e83c53cddd0b77a186ba1692e7aa8889a68799f621a478a65bb93fc046617ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d14a8b9dcf76f19d040a82cdb2b2e9ccf5b35072807c1176596c87e3fe21ff(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalAdminClusterSecurityConfigAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c2cd31e4be2e27859f7ede6e0fa05ef6be7570b694c646b8dee173c8d0a36f1(
    value: typing.Optional[GkeonpremBareMetalAdminClusterSecurityConfigAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828810672a4f68594a69c4e78886a2a685ad594fc7322f650ae0e8082dc7339b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c90fdeac29df4a4a7de2c714cd7a05b27e71215560ebd84288475e7b82a42d17(
    value: typing.Optional[GkeonpremBareMetalAdminClusterSecurityConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a34b3bc652c47d7030db98f5bba9938f40b7c7f7446d696e8638766461c9b13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0882c0b2a0d01f392b720a5fc20b7cac13d6ad1b0744d8d79859124486f6401d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b23019881acbbed74abcfa1a0dac11a597c2f5d7f6e982e758d5831d10019113(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22c1e1d606633dafbb9a7fed9ad5d7ee533ee7189b151398f7dacf8411c31074(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__822f3c912b2e2c62c32788611f5cc7664ebf9eb0f57420b2381a290456dafbfd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9b2ee080b9664e2a63af14192bf59b0877b3a1b02b16eac02a28c6412ba9b50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6970e80c6b8d2d317aaa7c772a01157caa62b6ac7371ae05c3a64f613a09d2e4(
    value: typing.Optional[GkeonpremBareMetalAdminClusterStatusConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e75b1a22dfe5a10d537a6759beab6469e925368da375003ef43ff6b871f3d632(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fa21a73a9c05da75c92444f01e6ea2b8e04ddf5d092628b803db9cd67d335ac(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b64c2311ef656fa5fab68baa75b78c3bddab15787783c8f87dd54f9f94f785b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc4f98b716f1dbe73dd879f502a16937c7d18a32696efb7820ed7b665701276e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e22f25b67fb8300ca18ebccf29285ffe94595a07a940b20531b8922347b872(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b877d46d13b4556b6785cea4cc56f3610647c7686144470331c021ffa3a5f1ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea5f66c2732251ed7bd4c0deddbf8ce415826b02eb9ae713e54e387fc837a2c(
    value: typing.Optional[GkeonpremBareMetalAdminClusterStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2993874fa923d1c95dc10a87ab19eb4f6e3f8ce500e0fd070a372439db8050b(
    *,
    lvp_node_mounts_config: typing.Union[GkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig, typing.Dict[builtins.str, typing.Any]],
    lvp_share_config: typing.Union[GkeonpremBareMetalAdminClusterStorageLvpShareConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ebd04a3df7e333bae0cb523cf7447d4a5164637afdb7c41c97e380bfc347aa8(
    *,
    path: builtins.str,
    storage_class: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe6c91d4505291390b232789ef06391a8a2e2b3f6c865f4bedfda944c91ef15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de0152720732ca0c35c76ce3c99da5ef7c450b2980a32eb33b9265777b61e85d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2106e4392a545d9c4d8c1ada51b3a7948600673052dd7c4fb64461d2e3f1c204(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d285faf7d784cb9a39913c988063a30a4db64fde85ce9254a5c26a49cf359d(
    value: typing.Optional[GkeonpremBareMetalAdminClusterStorageLvpNodeMountsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0c4e270242414de2f89ac525407669cff474acbe8c1e771274d80829f027df4(
    *,
    lvp_config: typing.Union[GkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig, typing.Dict[builtins.str, typing.Any]],
    shared_path_pv_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b496152f8f335dd98d51c8f37285da7d6a6126afbd3d808fef3d530a8a1aefc(
    *,
    path: builtins.str,
    storage_class: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2404e82c1185836f632fb3b072e6bb5514744b7da6d0629a8e7165d21732d00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0c1e89445c0958f7791e8ebf10d46951f6528abeecf709e7e8ac0208aa48dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c5d61253e7740f860f453b336d345ce6f5efdca827ac9873b97d235c56ff4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed5dfd20b50c838607885e9d9b3d74905739566bcc433c0f49cda333ab0f40ed(
    value: typing.Optional[GkeonpremBareMetalAdminClusterStorageLvpShareConfigLvpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b2906f0e9b544845b117919400b54d6c4cb56bb790e8c478913b4de22c3bb08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb14a9f8b71092f43a1c8c73fe737b612ec1daf2532d634035030d2e94c7de93(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0da1dbfb6f212bace24592871ffc8650d27024e2e5efd1de3084a2cfdf57f202(
    value: typing.Optional[GkeonpremBareMetalAdminClusterStorageLvpShareConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42a50390057a46efeacc51eec4d4d95963386b2e36c51d1e04493f5d2c2e6d63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa6f3f0498d0b0ecdb84d0a74c11c39ada70f0615c1029f94e557360e75443ac(
    value: typing.Optional[GkeonpremBareMetalAdminClusterStorage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b578bd0ed8e9100935442b191908eaac51ea7fddebfd3a83ea5aeb659a268ea(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__680892ce7f843b99e15ca6948ff4d45541c0309145147963235a18008e8b6659(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44229b4116600eee414f4c341adccb42f280234160945c054e0a921605b95308(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a96f30dc1597b8c4b87cad457a5a20aa9427a9f19d513b64b54f4e96c0176e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab7193cbfd3b8533d5259b644b1b551190ca43832b7e962321fd36936fd3e180(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__438aaf7875c77550c57dc52972c60c2af34ece2a05f8c6c06d356f9b24d22c92(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalAdminClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__988bea3b3f200c524baddd7d9f333e5108340d049959b8005f14b7582b7bb182(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__892220268f8f8ade74d7fbb5a529001890c6bd5688ec96e825a1b04b9d13fb6e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0924548bf6cb5da30ac6652067d72c4a6d36b6e8c3ffe9be9c45c64cfae40a20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e41b99684d834752ab04c8a89e10bf9e6a83bec50ce1a255b1f5f3c3ecef5bd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e8e634d11e919a692b10baf3324528ae7d6bb9c5088efced9d65735dd07fc8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d488efa9cf80630f230e39fc3a63e8211df5300cbb8013851eb872d40fcc2aac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519af003529ae2a3348d8a4dd4fe32a649e4da55da368dee6a36acbfa922b108(
    value: typing.Optional[GkeonpremBareMetalAdminClusterValidationCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33d4fbc5ffe3edbfda2cb962b714571ae383c6dc0a9d2aa9430db1604d6d952(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1bc51b63045e380f6b37bd349499c5ef55bfab22f38f4f63b3ca4da50d4ddd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed91f3aa31272359ae39438461a927bf92ddb7531acfa8144e4eb29aafb63c31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2ac2930c1246b0c5b67a2e7a8e3501c0d1b76a58286925499e4867a6ba2ab37(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa826f7f092d3ac56f24abd586e5abe1fd229ca76a9778041bafb1501ef59369(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3be9233ff87afeb719949332f53801a7067b3290ae9c956056e8622f4214613(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff0fa0f89078d41702124963b5d281b3e3c79cb931cc6c61d66a2d8d4c18813(
    value: typing.Optional[GkeonpremBareMetalAdminClusterValidationCheckStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10bdff88e593842024833226aac305c3ef7efcd263b248559dafa03af7640633(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c1b3cb739946c3abd710bf785a60030e8cb06af7e40944a18a4fcba1999c9d1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d5e8f8f4c17c61c497e9423c46c2c9e0e4b63d35bc2c097f43c0ea421594f07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d7a9ac84b27668d49b83bf4ea8f4f9bd94d88485e8eb078c2fe9ac16d79cbd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe65849113421987262f9aad668119e1a78171d259ad3322812c36981265b89(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf0447c968387fd5de28dcc6fb9dd2f6cb5eb60f17bdaebb116724f3ba16d3f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6d4300feeacea7e51571e9a3ce6f271c0ca822d5ae0f77e78c2787bdd916e9(
    value: typing.Optional[GkeonpremBareMetalAdminClusterValidationCheckStatusResult],
) -> None:
    """Type checking stubs"""
    pass
