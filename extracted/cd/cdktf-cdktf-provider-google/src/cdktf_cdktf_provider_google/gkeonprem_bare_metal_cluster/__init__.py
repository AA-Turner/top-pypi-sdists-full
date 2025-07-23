r'''
# `google_gkeonprem_bare_metal_cluster`

Refer to the Terraform Registry for docs: [`google_gkeonprem_bare_metal_cluster`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster).
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


class GkeonpremBareMetalCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster google_gkeonprem_bare_metal_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        admin_cluster_membership: builtins.str,
        bare_metal_version: builtins.str,
        control_plane: typing.Union["GkeonpremBareMetalClusterControlPlane", typing.Dict[builtins.str, typing.Any]],
        load_balancer: typing.Union["GkeonpremBareMetalClusterLoadBalancer", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        network_config: typing.Union["GkeonpremBareMetalClusterNetworkConfig", typing.Dict[builtins.str, typing.Any]],
        storage: typing.Union["GkeonpremBareMetalClusterStorage", typing.Dict[builtins.str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        binary_authorization: typing.Optional[typing.Union["GkeonpremBareMetalClusterBinaryAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_operations: typing.Optional[typing.Union["GkeonpremBareMetalClusterClusterOperations", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        maintenance_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterMaintenanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_access_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterNodeAccessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        os_environment_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterOsEnvironmentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        proxy: typing.Optional[typing.Union["GkeonpremBareMetalClusterProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        security_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterSecurityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GkeonpremBareMetalClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        upgrade_policy: typing.Optional[typing.Union["GkeonpremBareMetalClusterUpgradePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster google_gkeonprem_bare_metal_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param admin_cluster_membership: The Admin Cluster this Bare Metal User Cluster belongs to. This is the full resource name of the Admin Cluster's hub membership. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#admin_cluster_membership GkeonpremBareMetalCluster#admin_cluster_membership}
        :param bare_metal_version: A human readable description of this Bare Metal User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#bare_metal_version GkeonpremBareMetalCluster#bare_metal_version}
        :param control_plane: control_plane block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#control_plane GkeonpremBareMetalCluster#control_plane}
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#load_balancer GkeonpremBareMetalCluster#load_balancer}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#location GkeonpremBareMetalCluster#location}
        :param name: The bare metal cluster name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#name GkeonpremBareMetalCluster#name}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#network_config GkeonpremBareMetalCluster#network_config}
        :param storage: storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#storage GkeonpremBareMetalCluster#storage}
        :param annotations: Annotations on the Bare Metal User Cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#annotations GkeonpremBareMetalCluster#annotations}
        :param binary_authorization: binary_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#binary_authorization GkeonpremBareMetalCluster#binary_authorization}
        :param cluster_operations: cluster_operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#cluster_operations GkeonpremBareMetalCluster#cluster_operations}
        :param description: A human readable description of this Bare Metal User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#description GkeonpremBareMetalCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#id GkeonpremBareMetalCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintenance_config: maintenance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#maintenance_config GkeonpremBareMetalCluster#maintenance_config}
        :param node_access_config: node_access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_access_config GkeonpremBareMetalCluster#node_access_config}
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_config GkeonpremBareMetalCluster#node_config}
        :param os_environment_config: os_environment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#os_environment_config GkeonpremBareMetalCluster#os_environment_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#project GkeonpremBareMetalCluster#project}.
        :param proxy: proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#proxy GkeonpremBareMetalCluster#proxy}
        :param security_config: security_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#security_config GkeonpremBareMetalCluster#security_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#timeouts GkeonpremBareMetalCluster#timeouts}
        :param upgrade_policy: upgrade_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#upgrade_policy GkeonpremBareMetalCluster#upgrade_policy}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7067342f098b2fa59dfe3a7ef7dc191c9fb14cc5ccd17bb35745d653e72234a1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GkeonpremBareMetalClusterConfig(
            admin_cluster_membership=admin_cluster_membership,
            bare_metal_version=bare_metal_version,
            control_plane=control_plane,
            load_balancer=load_balancer,
            location=location,
            name=name,
            network_config=network_config,
            storage=storage,
            annotations=annotations,
            binary_authorization=binary_authorization,
            cluster_operations=cluster_operations,
            description=description,
            id=id,
            maintenance_config=maintenance_config,
            node_access_config=node_access_config,
            node_config=node_config,
            os_environment_config=os_environment_config,
            project=project,
            proxy=proxy,
            security_config=security_config,
            timeouts=timeouts,
            upgrade_policy=upgrade_policy,
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
        '''Generates CDKTF code for importing a GkeonpremBareMetalCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GkeonpremBareMetalCluster to import.
        :param import_from_id: The id of the existing GkeonpremBareMetalCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GkeonpremBareMetalCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b799e8213ff8c89487f48080780f302be26720104fede372e389442b8cdc761)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBinaryAuthorization")
    def put_binary_authorization(
        self,
        *,
        evaluation_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param evaluation_mode: Mode of operation for binauthz policy evaluation. If unspecified, defaults to DISABLED. Possible values: ["DISABLED", "PROJECT_SINGLETON_POLICY_ENFORCE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#evaluation_mode GkeonpremBareMetalCluster#evaluation_mode}
        '''
        value = GkeonpremBareMetalClusterBinaryAuthorization(
            evaluation_mode=evaluation_mode
        )

        return typing.cast(None, jsii.invoke(self, "putBinaryAuthorization", [value]))

    @jsii.member(jsii_name="putClusterOperations")
    def put_cluster_operations(
        self,
        *,
        enable_application_logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_application_logs: Whether collection of application logs/metrics should be enabled (in addition to system logs/metrics). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#enable_application_logs GkeonpremBareMetalCluster#enable_application_logs}
        '''
        value = GkeonpremBareMetalClusterClusterOperations(
            enable_application_logs=enable_application_logs
        )

        return typing.cast(None, jsii.invoke(self, "putClusterOperations", [value]))

    @jsii.member(jsii_name="putControlPlane")
    def put_control_plane(
        self,
        *,
        control_plane_node_pool_config: typing.Union["GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig", typing.Dict[builtins.str, typing.Any]],
        api_server_args: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalClusterControlPlaneApiServerArgs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param control_plane_node_pool_config: control_plane_node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#control_plane_node_pool_config GkeonpremBareMetalCluster#control_plane_node_pool_config}
        :param api_server_args: api_server_args block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#api_server_args GkeonpremBareMetalCluster#api_server_args}
        '''
        value = GkeonpremBareMetalClusterControlPlane(
            control_plane_node_pool_config=control_plane_node_pool_config,
            api_server_args=api_server_args,
        )

        return typing.cast(None, jsii.invoke(self, "putControlPlane", [value]))

    @jsii.member(jsii_name="putLoadBalancer")
    def put_load_balancer(
        self,
        *,
        port_config: typing.Union["GkeonpremBareMetalClusterLoadBalancerPortConfig", typing.Dict[builtins.str, typing.Any]],
        vip_config: typing.Union["GkeonpremBareMetalClusterLoadBalancerVipConfig", typing.Dict[builtins.str, typing.Any]],
        bgp_lb_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterLoadBalancerBgpLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        manual_lb_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterLoadBalancerManualLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        metal_lb_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterLoadBalancerMetalLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param port_config: port_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#port_config GkeonpremBareMetalCluster#port_config}
        :param vip_config: vip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#vip_config GkeonpremBareMetalCluster#vip_config}
        :param bgp_lb_config: bgp_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#bgp_lb_config GkeonpremBareMetalCluster#bgp_lb_config}
        :param manual_lb_config: manual_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#manual_lb_config GkeonpremBareMetalCluster#manual_lb_config}
        :param metal_lb_config: metal_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#metal_lb_config GkeonpremBareMetalCluster#metal_lb_config}
        '''
        value = GkeonpremBareMetalClusterLoadBalancer(
            port_config=port_config,
            vip_config=vip_config,
            bgp_lb_config=bgp_lb_config,
            manual_lb_config=manual_lb_config,
            metal_lb_config=metal_lb_config,
        )

        return typing.cast(None, jsii.invoke(self, "putLoadBalancer", [value]))

    @jsii.member(jsii_name="putMaintenanceConfig")
    def put_maintenance_config(
        self,
        *,
        maintenance_address_cidr_blocks: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param maintenance_address_cidr_blocks: All IPv4 address from these ranges will be placed into maintenance mode. Nodes in maintenance mode will be cordoned and drained. When both of these are true, the "baremetal.cluster.gke.io/maintenance" annotation will be set on the node resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#maintenance_address_cidr_blocks GkeonpremBareMetalCluster#maintenance_address_cidr_blocks}
        '''
        value = GkeonpremBareMetalClusterMaintenanceConfig(
            maintenance_address_cidr_blocks=maintenance_address_cidr_blocks
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenanceConfig", [value]))

    @jsii.member(jsii_name="putNetworkConfig")
    def put_network_config(
        self,
        *,
        advanced_networking: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        island_mode_cidr: typing.Optional[typing.Union["GkeonpremBareMetalClusterNetworkConfigIslandModeCidr", typing.Dict[builtins.str, typing.Any]]] = None,
        multiple_network_interfaces_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        sr_iov_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterNetworkConfigSrIovConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_networking: Enables the use of advanced Anthos networking features, such as Bundled Load Balancing with BGP or the egress NAT gateway. Setting configuration for advanced networking features will automatically set this flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#advanced_networking GkeonpremBareMetalCluster#advanced_networking}
        :param island_mode_cidr: island_mode_cidr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#island_mode_cidr GkeonpremBareMetalCluster#island_mode_cidr}
        :param multiple_network_interfaces_config: multiple_network_interfaces_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#multiple_network_interfaces_config GkeonpremBareMetalCluster#multiple_network_interfaces_config}
        :param sr_iov_config: sr_iov_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#sr_iov_config GkeonpremBareMetalCluster#sr_iov_config}
        '''
        value = GkeonpremBareMetalClusterNetworkConfig(
            advanced_networking=advanced_networking,
            island_mode_cidr=island_mode_cidr,
            multiple_network_interfaces_config=multiple_network_interfaces_config,
            sr_iov_config=sr_iov_config,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfig", [value]))

    @jsii.member(jsii_name="putNodeAccessConfig")
    def put_node_access_config(
        self,
        *,
        login_user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param login_user: LoginUser is the user name used to access node machines. It defaults to "root" if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#login_user GkeonpremBareMetalCluster#login_user}
        '''
        value = GkeonpremBareMetalClusterNodeAccessConfig(login_user=login_user)

        return typing.cast(None, jsii.invoke(self, "putNodeAccessConfig", [value]))

    @jsii.member(jsii_name="putNodeConfig")
    def put_node_config(
        self,
        *,
        container_runtime: typing.Optional[builtins.str] = None,
        max_pods_per_node: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param container_runtime: The available runtimes that can be used to run containers in a Bare Metal User Cluster. Possible values: ["CONTAINER_RUNTIME_UNSPECIFIED", "DOCKER", "CONTAINERD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#container_runtime GkeonpremBareMetalCluster#container_runtime}
        :param max_pods_per_node: The maximum number of pods a node can run. The size of the CIDR range assigned to the node will be derived from this parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#max_pods_per_node GkeonpremBareMetalCluster#max_pods_per_node}
        '''
        value = GkeonpremBareMetalClusterNodeConfig(
            container_runtime=container_runtime, max_pods_per_node=max_pods_per_node
        )

        return typing.cast(None, jsii.invoke(self, "putNodeConfig", [value]))

    @jsii.member(jsii_name="putOsEnvironmentConfig")
    def put_os_environment_config(
        self,
        *,
        package_repo_excluded: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param package_repo_excluded: Whether the package repo should not be included when initializing bare metal machines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#package_repo_excluded GkeonpremBareMetalCluster#package_repo_excluded}
        '''
        value = GkeonpremBareMetalClusterOsEnvironmentConfig(
            package_repo_excluded=package_repo_excluded
        )

        return typing.cast(None, jsii.invoke(self, "putOsEnvironmentConfig", [value]))

    @jsii.member(jsii_name="putProxy")
    def put_proxy(
        self,
        *,
        uri: builtins.str,
        no_proxy: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param uri: Specifies the address of your proxy server. For example: http://domain WARNING: Do not provide credentials in the format of http://(username:password@)domain these will be rejected by the server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#uri GkeonpremBareMetalCluster#uri}
        :param no_proxy: A list of IPs, hostnames, and domains that should skip the proxy. For example ["127.0.0.1", "example.com", ".corp", "localhost"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#no_proxy GkeonpremBareMetalCluster#no_proxy}
        '''
        value = GkeonpremBareMetalClusterProxy(uri=uri, no_proxy=no_proxy)

        return typing.cast(None, jsii.invoke(self, "putProxy", [value]))

    @jsii.member(jsii_name="putSecurityConfig")
    def put_security_config(
        self,
        *,
        authorization: typing.Optional[typing.Union["GkeonpremBareMetalClusterSecurityConfigAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#authorization GkeonpremBareMetalCluster#authorization}
        '''
        value = GkeonpremBareMetalClusterSecurityConfig(authorization=authorization)

        return typing.cast(None, jsii.invoke(self, "putSecurityConfig", [value]))

    @jsii.member(jsii_name="putStorage")
    def put_storage(
        self,
        *,
        lvp_node_mounts_config: typing.Union["GkeonpremBareMetalClusterStorageLvpNodeMountsConfig", typing.Dict[builtins.str, typing.Any]],
        lvp_share_config: typing.Union["GkeonpremBareMetalClusterStorageLvpShareConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param lvp_node_mounts_config: lvp_node_mounts_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#lvp_node_mounts_config GkeonpremBareMetalCluster#lvp_node_mounts_config}
        :param lvp_share_config: lvp_share_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#lvp_share_config GkeonpremBareMetalCluster#lvp_share_config}
        '''
        value = GkeonpremBareMetalClusterStorage(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#create GkeonpremBareMetalCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#delete GkeonpremBareMetalCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#update GkeonpremBareMetalCluster#update}.
        '''
        value = GkeonpremBareMetalClusterTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUpgradePolicy")
    def put_upgrade_policy(
        self,
        *,
        policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param policy: Specifies which upgrade policy to use. Possible values: ["SERIAL", "CONCURRENT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#policy GkeonpremBareMetalCluster#policy}
        '''
        value = GkeonpremBareMetalClusterUpgradePolicy(policy=policy)

        return typing.cast(None, jsii.invoke(self, "putUpgradePolicy", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetBinaryAuthorization")
    def reset_binary_authorization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBinaryAuthorization", []))

    @jsii.member(jsii_name="resetClusterOperations")
    def reset_cluster_operations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterOperations", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaintenanceConfig")
    def reset_maintenance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceConfig", []))

    @jsii.member(jsii_name="resetNodeAccessConfig")
    def reset_node_access_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeAccessConfig", []))

    @jsii.member(jsii_name="resetNodeConfig")
    def reset_node_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeConfig", []))

    @jsii.member(jsii_name="resetOsEnvironmentConfig")
    def reset_os_environment_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsEnvironmentConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetProxy")
    def reset_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxy", []))

    @jsii.member(jsii_name="resetSecurityConfig")
    def reset_security_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityConfig", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUpgradePolicy")
    def reset_upgrade_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpgradePolicy", []))

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
    @jsii.member(jsii_name="binaryAuthorization")
    def binary_authorization(
        self,
    ) -> "GkeonpremBareMetalClusterBinaryAuthorizationOutputReference":
        return typing.cast("GkeonpremBareMetalClusterBinaryAuthorizationOutputReference", jsii.get(self, "binaryAuthorization"))

    @builtins.property
    @jsii.member(jsii_name="clusterOperations")
    def cluster_operations(
        self,
    ) -> "GkeonpremBareMetalClusterClusterOperationsOutputReference":
        return typing.cast("GkeonpremBareMetalClusterClusterOperationsOutputReference", jsii.get(self, "clusterOperations"))

    @builtins.property
    @jsii.member(jsii_name="controlPlane")
    def control_plane(self) -> "GkeonpremBareMetalClusterControlPlaneOutputReference":
        return typing.cast("GkeonpremBareMetalClusterControlPlaneOutputReference", jsii.get(self, "controlPlane"))

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
    def fleet(self) -> "GkeonpremBareMetalClusterFleetList":
        return typing.cast("GkeonpremBareMetalClusterFleetList", jsii.get(self, "fleet"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> "GkeonpremBareMetalClusterLoadBalancerOutputReference":
        return typing.cast("GkeonpremBareMetalClusterLoadBalancerOutputReference", jsii.get(self, "loadBalancer"))

    @builtins.property
    @jsii.member(jsii_name="localName")
    def local_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localName"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceConfig")
    def maintenance_config(
        self,
    ) -> "GkeonpremBareMetalClusterMaintenanceConfigOutputReference":
        return typing.cast("GkeonpremBareMetalClusterMaintenanceConfigOutputReference", jsii.get(self, "maintenanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(self) -> "GkeonpremBareMetalClusterNetworkConfigOutputReference":
        return typing.cast("GkeonpremBareMetalClusterNetworkConfigOutputReference", jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodeAccessConfig")
    def node_access_config(
        self,
    ) -> "GkeonpremBareMetalClusterNodeAccessConfigOutputReference":
        return typing.cast("GkeonpremBareMetalClusterNodeAccessConfigOutputReference", jsii.get(self, "nodeAccessConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfig")
    def node_config(self) -> "GkeonpremBareMetalClusterNodeConfigOutputReference":
        return typing.cast("GkeonpremBareMetalClusterNodeConfigOutputReference", jsii.get(self, "nodeConfig"))

    @builtins.property
    @jsii.member(jsii_name="osEnvironmentConfig")
    def os_environment_config(
        self,
    ) -> "GkeonpremBareMetalClusterOsEnvironmentConfigOutputReference":
        return typing.cast("GkeonpremBareMetalClusterOsEnvironmentConfigOutputReference", jsii.get(self, "osEnvironmentConfig"))

    @builtins.property
    @jsii.member(jsii_name="proxy")
    def proxy(self) -> "GkeonpremBareMetalClusterProxyOutputReference":
        return typing.cast("GkeonpremBareMetalClusterProxyOutputReference", jsii.get(self, "proxy"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="securityConfig")
    def security_config(
        self,
    ) -> "GkeonpremBareMetalClusterSecurityConfigOutputReference":
        return typing.cast("GkeonpremBareMetalClusterSecurityConfigOutputReference", jsii.get(self, "securityConfig"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "GkeonpremBareMetalClusterStatusList":
        return typing.cast("GkeonpremBareMetalClusterStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="storage")
    def storage(self) -> "GkeonpremBareMetalClusterStorageOutputReference":
        return typing.cast("GkeonpremBareMetalClusterStorageOutputReference", jsii.get(self, "storage"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GkeonpremBareMetalClusterTimeoutsOutputReference":
        return typing.cast("GkeonpremBareMetalClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    def upgrade_policy(self) -> "GkeonpremBareMetalClusterUpgradePolicyOutputReference":
        return typing.cast("GkeonpremBareMetalClusterUpgradePolicyOutputReference", jsii.get(self, "upgradePolicy"))

    @builtins.property
    @jsii.member(jsii_name="validationCheck")
    def validation_check(self) -> "GkeonpremBareMetalClusterValidationCheckList":
        return typing.cast("GkeonpremBareMetalClusterValidationCheckList", jsii.get(self, "validationCheck"))

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
    @jsii.member(jsii_name="bareMetalVersionInput")
    def bare_metal_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bareMetalVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="binaryAuthorizationInput")
    def binary_authorization_input(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterBinaryAuthorization"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterBinaryAuthorization"], jsii.get(self, "binaryAuthorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterOperationsInput")
    def cluster_operations_input(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterClusterOperations"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterClusterOperations"], jsii.get(self, "clusterOperationsInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneInput")
    def control_plane_input(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterControlPlane"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterControlPlane"], jsii.get(self, "controlPlaneInput"))

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
    ) -> typing.Optional["GkeonpremBareMetalClusterLoadBalancer"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterLoadBalancer"], jsii.get(self, "loadBalancerInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceConfigInput")
    def maintenance_config_input(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterMaintenanceConfig"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterMaintenanceConfig"], jsii.get(self, "maintenanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigInput")
    def network_config_input(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterNetworkConfig"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterNetworkConfig"], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeAccessConfigInput")
    def node_access_config_input(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterNodeAccessConfig"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterNodeAccessConfig"], jsii.get(self, "nodeAccessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfigInput")
    def node_config_input(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterNodeConfig"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterNodeConfig"], jsii.get(self, "nodeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="osEnvironmentConfigInput")
    def os_environment_config_input(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterOsEnvironmentConfig"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterOsEnvironmentConfig"], jsii.get(self, "osEnvironmentConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyInput")
    def proxy_input(self) -> typing.Optional["GkeonpremBareMetalClusterProxy"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterProxy"], jsii.get(self, "proxyInput"))

    @builtins.property
    @jsii.member(jsii_name="securityConfigInput")
    def security_config_input(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterSecurityConfig"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterSecurityConfig"], jsii.get(self, "securityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="storageInput")
    def storage_input(self) -> typing.Optional["GkeonpremBareMetalClusterStorage"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterStorage"], jsii.get(self, "storageInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeonpremBareMetalClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeonpremBareMetalClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="upgradePolicyInput")
    def upgrade_policy_input(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterUpgradePolicy"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterUpgradePolicy"], jsii.get(self, "upgradePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="adminClusterMembership")
    def admin_cluster_membership(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminClusterMembership"))

    @admin_cluster_membership.setter
    def admin_cluster_membership(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c39ae4ac474d27ffa0371c41aa2a327a1cca99c03371af56ad9d822bc3757fcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminClusterMembership", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98175ac62cd809bb9a0b5b9695370c7596083ae37eef4196e8477732f9fe6d23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bareMetalVersion")
    def bare_metal_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bareMetalVersion"))

    @bare_metal_version.setter
    def bare_metal_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f90d733df01aa4685a2907a8ff2ea19a735a4834c2ef7c06375b58601de68934)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bareMetalVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9175a4bf3165a2161bbd624d6d4e818b297a171a03a64a40ddda72e2e463c61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bfaf1d2861a170c8e896be57e2496dd37a5f1f997f61586020632c8913da014)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01a4844b7c8e584bd0ee384199e0660ba6ca628ca306e0764093bf06b30447f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15505bfbf5bcad7835b3d0d78b7e22966624e5a67c3100864286dfbc0ef81d4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b034d1c7fccccc85a682725b60a603a1141ebf4848d89d6ee86d33e27f5ee02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterBinaryAuthorization",
    jsii_struct_bases=[],
    name_mapping={"evaluation_mode": "evaluationMode"},
)
class GkeonpremBareMetalClusterBinaryAuthorization:
    def __init__(
        self,
        *,
        evaluation_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param evaluation_mode: Mode of operation for binauthz policy evaluation. If unspecified, defaults to DISABLED. Possible values: ["DISABLED", "PROJECT_SINGLETON_POLICY_ENFORCE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#evaluation_mode GkeonpremBareMetalCluster#evaluation_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00e634687f672871c9f4500f38b0f6628d553c14798da81869d7efc3907405ae)
            check_type(argname="argument evaluation_mode", value=evaluation_mode, expected_type=type_hints["evaluation_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if evaluation_mode is not None:
            self._values["evaluation_mode"] = evaluation_mode

    @builtins.property
    def evaluation_mode(self) -> typing.Optional[builtins.str]:
        '''Mode of operation for binauthz policy evaluation. If unspecified, defaults to DISABLED. Possible values: ["DISABLED", "PROJECT_SINGLETON_POLICY_ENFORCE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#evaluation_mode GkeonpremBareMetalCluster#evaluation_mode}
        '''
        result = self._values.get("evaluation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterBinaryAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterBinaryAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterBinaryAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__455a86462162ea5289cbbc96c7ea7b35347426b3da946ed9b98bd1ba230c9398)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEvaluationMode")
    def reset_evaluation_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvaluationMode", []))

    @builtins.property
    @jsii.member(jsii_name="evaluationModeInput")
    def evaluation_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "evaluationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluationMode")
    def evaluation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "evaluationMode"))

    @evaluation_mode.setter
    def evaluation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eab41abc6904554fbe61bc630e78a88293583a62111620604f89083461877473)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterBinaryAuthorization]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterBinaryAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterBinaryAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__110f5c35cd2596cc68ccbdcb70ea501dee76f04c9e67d56ba33282afffc8ff68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterClusterOperations",
    jsii_struct_bases=[],
    name_mapping={"enable_application_logs": "enableApplicationLogs"},
)
class GkeonpremBareMetalClusterClusterOperations:
    def __init__(
        self,
        *,
        enable_application_logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_application_logs: Whether collection of application logs/metrics should be enabled (in addition to system logs/metrics). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#enable_application_logs GkeonpremBareMetalCluster#enable_application_logs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27f6b319b9bf532677fd1cf76993e6ebd68b57118ed8ece2d5511f40517feb4a)
            check_type(argname="argument enable_application_logs", value=enable_application_logs, expected_type=type_hints["enable_application_logs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_application_logs is not None:
            self._values["enable_application_logs"] = enable_application_logs

    @builtins.property
    def enable_application_logs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether collection of application logs/metrics should be enabled (in addition to system logs/metrics).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#enable_application_logs GkeonpremBareMetalCluster#enable_application_logs}
        '''
        result = self._values.get("enable_application_logs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterClusterOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterClusterOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterClusterOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdf338c6102ffa7fc2cdb61f3d36e9ee33f9851c7497b36134cb095b9561615d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31e2f6a513c591aa43547c328f2365cb7151bade111d8fb0780693c6b3b2a097)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableApplicationLogs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterClusterOperations]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterClusterOperations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterClusterOperations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8671d4b5239e73b9b3b8154fad8302934c944f782afccc1494831d90ddb57833)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterConfig",
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
        "bare_metal_version": "bareMetalVersion",
        "control_plane": "controlPlane",
        "load_balancer": "loadBalancer",
        "location": "location",
        "name": "name",
        "network_config": "networkConfig",
        "storage": "storage",
        "annotations": "annotations",
        "binary_authorization": "binaryAuthorization",
        "cluster_operations": "clusterOperations",
        "description": "description",
        "id": "id",
        "maintenance_config": "maintenanceConfig",
        "node_access_config": "nodeAccessConfig",
        "node_config": "nodeConfig",
        "os_environment_config": "osEnvironmentConfig",
        "project": "project",
        "proxy": "proxy",
        "security_config": "securityConfig",
        "timeouts": "timeouts",
        "upgrade_policy": "upgradePolicy",
    },
)
class GkeonpremBareMetalClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bare_metal_version: builtins.str,
        control_plane: typing.Union["GkeonpremBareMetalClusterControlPlane", typing.Dict[builtins.str, typing.Any]],
        load_balancer: typing.Union["GkeonpremBareMetalClusterLoadBalancer", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        network_config: typing.Union["GkeonpremBareMetalClusterNetworkConfig", typing.Dict[builtins.str, typing.Any]],
        storage: typing.Union["GkeonpremBareMetalClusterStorage", typing.Dict[builtins.str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        binary_authorization: typing.Optional[typing.Union[GkeonpremBareMetalClusterBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_operations: typing.Optional[typing.Union[GkeonpremBareMetalClusterClusterOperations, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        maintenance_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterMaintenanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_access_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterNodeAccessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        os_environment_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterOsEnvironmentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        proxy: typing.Optional[typing.Union["GkeonpremBareMetalClusterProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        security_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterSecurityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GkeonpremBareMetalClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        upgrade_policy: typing.Optional[typing.Union["GkeonpremBareMetalClusterUpgradePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param admin_cluster_membership: The Admin Cluster this Bare Metal User Cluster belongs to. This is the full resource name of the Admin Cluster's hub membership. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#admin_cluster_membership GkeonpremBareMetalCluster#admin_cluster_membership}
        :param bare_metal_version: A human readable description of this Bare Metal User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#bare_metal_version GkeonpremBareMetalCluster#bare_metal_version}
        :param control_plane: control_plane block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#control_plane GkeonpremBareMetalCluster#control_plane}
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#load_balancer GkeonpremBareMetalCluster#load_balancer}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#location GkeonpremBareMetalCluster#location}
        :param name: The bare metal cluster name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#name GkeonpremBareMetalCluster#name}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#network_config GkeonpremBareMetalCluster#network_config}
        :param storage: storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#storage GkeonpremBareMetalCluster#storage}
        :param annotations: Annotations on the Bare Metal User Cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#annotations GkeonpremBareMetalCluster#annotations}
        :param binary_authorization: binary_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#binary_authorization GkeonpremBareMetalCluster#binary_authorization}
        :param cluster_operations: cluster_operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#cluster_operations GkeonpremBareMetalCluster#cluster_operations}
        :param description: A human readable description of this Bare Metal User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#description GkeonpremBareMetalCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#id GkeonpremBareMetalCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintenance_config: maintenance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#maintenance_config GkeonpremBareMetalCluster#maintenance_config}
        :param node_access_config: node_access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_access_config GkeonpremBareMetalCluster#node_access_config}
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_config GkeonpremBareMetalCluster#node_config}
        :param os_environment_config: os_environment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#os_environment_config GkeonpremBareMetalCluster#os_environment_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#project GkeonpremBareMetalCluster#project}.
        :param proxy: proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#proxy GkeonpremBareMetalCluster#proxy}
        :param security_config: security_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#security_config GkeonpremBareMetalCluster#security_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#timeouts GkeonpremBareMetalCluster#timeouts}
        :param upgrade_policy: upgrade_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#upgrade_policy GkeonpremBareMetalCluster#upgrade_policy}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(control_plane, dict):
            control_plane = GkeonpremBareMetalClusterControlPlane(**control_plane)
        if isinstance(load_balancer, dict):
            load_balancer = GkeonpremBareMetalClusterLoadBalancer(**load_balancer)
        if isinstance(network_config, dict):
            network_config = GkeonpremBareMetalClusterNetworkConfig(**network_config)
        if isinstance(storage, dict):
            storage = GkeonpremBareMetalClusterStorage(**storage)
        if isinstance(binary_authorization, dict):
            binary_authorization = GkeonpremBareMetalClusterBinaryAuthorization(**binary_authorization)
        if isinstance(cluster_operations, dict):
            cluster_operations = GkeonpremBareMetalClusterClusterOperations(**cluster_operations)
        if isinstance(maintenance_config, dict):
            maintenance_config = GkeonpremBareMetalClusterMaintenanceConfig(**maintenance_config)
        if isinstance(node_access_config, dict):
            node_access_config = GkeonpremBareMetalClusterNodeAccessConfig(**node_access_config)
        if isinstance(node_config, dict):
            node_config = GkeonpremBareMetalClusterNodeConfig(**node_config)
        if isinstance(os_environment_config, dict):
            os_environment_config = GkeonpremBareMetalClusterOsEnvironmentConfig(**os_environment_config)
        if isinstance(proxy, dict):
            proxy = GkeonpremBareMetalClusterProxy(**proxy)
        if isinstance(security_config, dict):
            security_config = GkeonpremBareMetalClusterSecurityConfig(**security_config)
        if isinstance(timeouts, dict):
            timeouts = GkeonpremBareMetalClusterTimeouts(**timeouts)
        if isinstance(upgrade_policy, dict):
            upgrade_policy = GkeonpremBareMetalClusterUpgradePolicy(**upgrade_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdc7624c94fd6869aa0f3346bf6d292584fffdef72bc5e0cc82e62ce370a0da4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument admin_cluster_membership", value=admin_cluster_membership, expected_type=type_hints["admin_cluster_membership"])
            check_type(argname="argument bare_metal_version", value=bare_metal_version, expected_type=type_hints["bare_metal_version"])
            check_type(argname="argument control_plane", value=control_plane, expected_type=type_hints["control_plane"])
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_config", value=network_config, expected_type=type_hints["network_config"])
            check_type(argname="argument storage", value=storage, expected_type=type_hints["storage"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument binary_authorization", value=binary_authorization, expected_type=type_hints["binary_authorization"])
            check_type(argname="argument cluster_operations", value=cluster_operations, expected_type=type_hints["cluster_operations"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument maintenance_config", value=maintenance_config, expected_type=type_hints["maintenance_config"])
            check_type(argname="argument node_access_config", value=node_access_config, expected_type=type_hints["node_access_config"])
            check_type(argname="argument node_config", value=node_config, expected_type=type_hints["node_config"])
            check_type(argname="argument os_environment_config", value=os_environment_config, expected_type=type_hints["os_environment_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument proxy", value=proxy, expected_type=type_hints["proxy"])
            check_type(argname="argument security_config", value=security_config, expected_type=type_hints["security_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument upgrade_policy", value=upgrade_policy, expected_type=type_hints["upgrade_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_cluster_membership": admin_cluster_membership,
            "bare_metal_version": bare_metal_version,
            "control_plane": control_plane,
            "load_balancer": load_balancer,
            "location": location,
            "name": name,
            "network_config": network_config,
            "storage": storage,
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
        if binary_authorization is not None:
            self._values["binary_authorization"] = binary_authorization
        if cluster_operations is not None:
            self._values["cluster_operations"] = cluster_operations
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if maintenance_config is not None:
            self._values["maintenance_config"] = maintenance_config
        if node_access_config is not None:
            self._values["node_access_config"] = node_access_config
        if node_config is not None:
            self._values["node_config"] = node_config
        if os_environment_config is not None:
            self._values["os_environment_config"] = os_environment_config
        if project is not None:
            self._values["project"] = project
        if proxy is not None:
            self._values["proxy"] = proxy
        if security_config is not None:
            self._values["security_config"] = security_config
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if upgrade_policy is not None:
            self._values["upgrade_policy"] = upgrade_policy

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
        '''The Admin Cluster this Bare Metal User Cluster belongs to.

        This is the full resource name of the Admin Cluster's hub membership.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#admin_cluster_membership GkeonpremBareMetalCluster#admin_cluster_membership}
        '''
        result = self._values.get("admin_cluster_membership")
        assert result is not None, "Required property 'admin_cluster_membership' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bare_metal_version(self) -> builtins.str:
        '''A human readable description of this Bare Metal User Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#bare_metal_version GkeonpremBareMetalCluster#bare_metal_version}
        '''
        result = self._values.get("bare_metal_version")
        assert result is not None, "Required property 'bare_metal_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def control_plane(self) -> "GkeonpremBareMetalClusterControlPlane":
        '''control_plane block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#control_plane GkeonpremBareMetalCluster#control_plane}
        '''
        result = self._values.get("control_plane")
        assert result is not None, "Required property 'control_plane' is missing"
        return typing.cast("GkeonpremBareMetalClusterControlPlane", result)

    @builtins.property
    def load_balancer(self) -> "GkeonpremBareMetalClusterLoadBalancer":
        '''load_balancer block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#load_balancer GkeonpremBareMetalCluster#load_balancer}
        '''
        result = self._values.get("load_balancer")
        assert result is not None, "Required property 'load_balancer' is missing"
        return typing.cast("GkeonpremBareMetalClusterLoadBalancer", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#location GkeonpremBareMetalCluster#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The bare metal cluster name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#name GkeonpremBareMetalCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_config(self) -> "GkeonpremBareMetalClusterNetworkConfig":
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#network_config GkeonpremBareMetalCluster#network_config}
        '''
        result = self._values.get("network_config")
        assert result is not None, "Required property 'network_config' is missing"
        return typing.cast("GkeonpremBareMetalClusterNetworkConfig", result)

    @builtins.property
    def storage(self) -> "GkeonpremBareMetalClusterStorage":
        '''storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#storage GkeonpremBareMetalCluster#storage}
        '''
        result = self._values.get("storage")
        assert result is not None, "Required property 'storage' is missing"
        return typing.cast("GkeonpremBareMetalClusterStorage", result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Annotations on the Bare Metal User Cluster.

        This field has the same restrictions as Kubernetes annotations.
        The total size of all keys and values combined is limited to 256k.
        Key can have 2 segments: prefix (optional) and name (required),
        separated by a slash (/).
        Prefix must be a DNS subdomain.
        Name must be 63 characters or less, begin and end with alphanumerics,
        with dashes (-), underscores (_), dots (.), and alphanumerics between.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#annotations GkeonpremBareMetalCluster#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def binary_authorization(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterBinaryAuthorization]:
        '''binary_authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#binary_authorization GkeonpremBareMetalCluster#binary_authorization}
        '''
        result = self._values.get("binary_authorization")
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterBinaryAuthorization], result)

    @builtins.property
    def cluster_operations(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterClusterOperations]:
        '''cluster_operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#cluster_operations GkeonpremBareMetalCluster#cluster_operations}
        '''
        result = self._values.get("cluster_operations")
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterClusterOperations], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human readable description of this Bare Metal User Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#description GkeonpremBareMetalCluster#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#id GkeonpremBareMetalCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_config(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterMaintenanceConfig"]:
        '''maintenance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#maintenance_config GkeonpremBareMetalCluster#maintenance_config}
        '''
        result = self._values.get("maintenance_config")
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterMaintenanceConfig"], result)

    @builtins.property
    def node_access_config(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterNodeAccessConfig"]:
        '''node_access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_access_config GkeonpremBareMetalCluster#node_access_config}
        '''
        result = self._values.get("node_access_config")
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterNodeAccessConfig"], result)

    @builtins.property
    def node_config(self) -> typing.Optional["GkeonpremBareMetalClusterNodeConfig"]:
        '''node_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_config GkeonpremBareMetalCluster#node_config}
        '''
        result = self._values.get("node_config")
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterNodeConfig"], result)

    @builtins.property
    def os_environment_config(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterOsEnvironmentConfig"]:
        '''os_environment_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#os_environment_config GkeonpremBareMetalCluster#os_environment_config}
        '''
        result = self._values.get("os_environment_config")
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterOsEnvironmentConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#project GkeonpremBareMetalCluster#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy(self) -> typing.Optional["GkeonpremBareMetalClusterProxy"]:
        '''proxy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#proxy GkeonpremBareMetalCluster#proxy}
        '''
        result = self._values.get("proxy")
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterProxy"], result)

    @builtins.property
    def security_config(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterSecurityConfig"]:
        '''security_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#security_config GkeonpremBareMetalCluster#security_config}
        '''
        result = self._values.get("security_config")
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterSecurityConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GkeonpremBareMetalClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#timeouts GkeonpremBareMetalCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterTimeouts"], result)

    @builtins.property
    def upgrade_policy(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterUpgradePolicy"]:
        '''upgrade_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#upgrade_policy GkeonpremBareMetalCluster#upgrade_policy}
        '''
        result = self._values.get("upgrade_policy")
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterUpgradePolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterControlPlane",
    jsii_struct_bases=[],
    name_mapping={
        "control_plane_node_pool_config": "controlPlaneNodePoolConfig",
        "api_server_args": "apiServerArgs",
    },
)
class GkeonpremBareMetalClusterControlPlane:
    def __init__(
        self,
        *,
        control_plane_node_pool_config: typing.Union["GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig", typing.Dict[builtins.str, typing.Any]],
        api_server_args: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalClusterControlPlaneApiServerArgs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param control_plane_node_pool_config: control_plane_node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#control_plane_node_pool_config GkeonpremBareMetalCluster#control_plane_node_pool_config}
        :param api_server_args: api_server_args block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#api_server_args GkeonpremBareMetalCluster#api_server_args}
        '''
        if isinstance(control_plane_node_pool_config, dict):
            control_plane_node_pool_config = GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig(**control_plane_node_pool_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eaaa5c906a290f1d786453ca271072a21e23bc29a3eb5b70832f739fdc35dc3)
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
    ) -> "GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig":
        '''control_plane_node_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#control_plane_node_pool_config GkeonpremBareMetalCluster#control_plane_node_pool_config}
        '''
        result = self._values.get("control_plane_node_pool_config")
        assert result is not None, "Required property 'control_plane_node_pool_config' is missing"
        return typing.cast("GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig", result)

    @builtins.property
    def api_server_args(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterControlPlaneApiServerArgs"]]]:
        '''api_server_args block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#api_server_args GkeonpremBareMetalCluster#api_server_args}
        '''
        result = self._values.get("api_server_args")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterControlPlaneApiServerArgs"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterControlPlane(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterControlPlaneApiServerArgs",
    jsii_struct_bases=[],
    name_mapping={"argument": "argument", "value": "value"},
)
class GkeonpremBareMetalClusterControlPlaneApiServerArgs:
    def __init__(self, *, argument: builtins.str, value: builtins.str) -> None:
        '''
        :param argument: The argument name as it appears on the API Server command line please make sure to remove the leading dashes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#argument GkeonpremBareMetalCluster#argument}
        :param value: The value of the arg as it will be passed to the API Server command line. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#value GkeonpremBareMetalCluster#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b82718ab650f538aedbff3b24071e95c221113a2eaf8b228af28ed7f607abf13)
            check_type(argname="argument argument", value=argument, expected_type=type_hints["argument"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "argument": argument,
            "value": value,
        }

    @builtins.property
    def argument(self) -> builtins.str:
        '''The argument name as it appears on the API Server command line please make sure to remove the leading dashes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#argument GkeonpremBareMetalCluster#argument}
        '''
        result = self._values.get("argument")
        assert result is not None, "Required property 'argument' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value of the arg as it will be passed to the API Server command line.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#value GkeonpremBareMetalCluster#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterControlPlaneApiServerArgs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterControlPlaneApiServerArgsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterControlPlaneApiServerArgsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f92df5a2362a862a1c9317b4238758a1276e45a71839bdb921f6eb05d328bb5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalClusterControlPlaneApiServerArgsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__531246a4004466e8de2533b785c471c732b0e8bbbae15c2469ad587822297b78)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalClusterControlPlaneApiServerArgsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30f016bbabfaefaf31060ebd3987f1e68c5ef133f4028cdaabcc6ca5b891579b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4363f77e7e3a79ab450155b897be46dc66658d8984f02a23aa74b2bac0064ed0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__693827ff86652a33f3a95bb95f3a08ec21c4ebed22971447955fc0603fff1b75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterControlPlaneApiServerArgs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterControlPlaneApiServerArgs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterControlPlaneApiServerArgs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__333d77096de00320b87e4bb4bdd8475498990ce282cf95c1becf60e756086635)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterControlPlaneApiServerArgsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterControlPlaneApiServerArgsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb63686a0523889c9fe3c3f44b2cfcf03b65f1296421b3592ccfe156a3203ed8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6da33ac818d704401646091b68eb53d3751e09b405ab505a91e9dcbeb20d5bac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "argument", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e8ee33da4728a8cae0733bb51ebee238bf5a165fcfe1bd1ebf0b692cfb4e26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterControlPlaneApiServerArgs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterControlPlaneApiServerArgs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterControlPlaneApiServerArgs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24e3f4e20aa893610eed7a17f3e6ea16f2486a18478774703cabca28ba5e17a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig",
    jsii_struct_bases=[],
    name_mapping={"node_pool_config": "nodePoolConfig"},
)
class GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig:
    def __init__(
        self,
        *,
        node_pool_config: typing.Union["GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param node_pool_config: node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_pool_config GkeonpremBareMetalCluster#node_pool_config}
        '''
        if isinstance(node_pool_config, dict):
            node_pool_config = GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig(**node_pool_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3fce94bd2de88af7b9ea278dfb9acbd49b81b1b7d9179d4b2a72bb9c4152c9f)
            check_type(argname="argument node_pool_config", value=node_pool_config, expected_type=type_hints["node_pool_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "node_pool_config": node_pool_config,
        }

    @builtins.property
    def node_pool_config(
        self,
    ) -> "GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig":
        '''node_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_pool_config GkeonpremBareMetalCluster#node_pool_config}
        '''
        result = self._values.get("node_pool_config")
        assert result is not None, "Required property 'node_pool_config' is missing"
        return typing.cast("GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig",
    jsii_struct_bases=[],
    name_mapping={
        "labels": "labels",
        "node_configs": "nodeConfigs",
        "operating_system": "operatingSystem",
        "taints": "taints",
    },
)
class GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operating_system: typing.Optional[builtins.str] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#labels GkeonpremBareMetalCluster#labels}
        :param node_configs: node_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_configs GkeonpremBareMetalCluster#node_configs}
        :param operating_system: Specifies the nodes operating system (default: LINUX). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#operating_system GkeonpremBareMetalCluster#operating_system}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#taints GkeonpremBareMetalCluster#taints}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cd0f9fa3826d14eb55993f837085a59506d386622c5505cf796e522bc41f839)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#labels GkeonpremBareMetalCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def node_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs"]]]:
        '''node_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_configs GkeonpremBareMetalCluster#node_configs}
        '''
        result = self._values.get("node_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs"]]], result)

    @builtins.property
    def operating_system(self) -> typing.Optional[builtins.str]:
        '''Specifies the nodes operating system (default: LINUX).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#operating_system GkeonpremBareMetalCluster#operating_system}
        '''
        result = self._values.get("operating_system")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def taints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints"]]]:
        '''taints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#taints GkeonpremBareMetalCluster#taints}
        '''
        result = self._values.get("taints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels", "node_ip": "nodeIp"},
)
class GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_ip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#labels GkeonpremBareMetalCluster#labels}
        :param node_ip: The default IPv4 address for SSH access and Kubernetes node. Example: 192.168.0.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_ip GkeonpremBareMetalCluster#node_ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__552d1190d1054d5bbde3fd0c502cc286b917498f5d9ca8d254e8f62478d8f0b8)
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
          Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#labels GkeonpremBareMetalCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def node_ip(self) -> typing.Optional[builtins.str]:
        '''The default IPv4 address for SSH access and Kubernetes node. Example: 192.168.0.1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_ip GkeonpremBareMetalCluster#node_ip}
        '''
        result = self._values.get("node_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ac8a27360a0683719bc8103d4ba55ce4378e0c484fd9c60513371e26cd00a3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf5bb09229b1dce4da130543535c2beb100142b78d7e290b9cf0fad949565f7e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__953a525e85b90d619ea7af49da83d5b5ad5eaee6c814fbdc2870fd04e67e59db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a198cfa649ab62f7c48b4ab61676e12c47cdc4cf8c3cbc522f058f157960269)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d116cd012ddb024ad730f424bb39803692d1a51c4fb60c40ecd8a3cde376af7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c578de02edf756390c7a44ba35fd2a2cfbe5c059101ba647b06e366534223aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__120fec270da460f1e24311ef53be7bc823ad3563477c0808b6aebe944964d520)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b201e4a7363d9d1b7705dcba5b2acfc3d189393985bc75a6f780d8fd6de2a62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeIp")
    def node_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeIp"))

    @node_ip.setter
    def node_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3019e45b9e711a877f722decd7d3059eca67bbb084bef646afad3ad67c7ae4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05fb5115e04301a1eb54ca7e4a979a4591b2e702ffd94b489a94002634a276d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f7dc95475033e6ed7768b0e4107acbbae422af41e63b199fe10e9d35faeddbb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodeConfigs")
    def put_node_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__645c977aae16659111c75567b2773d84c3bb15897ceb16e6eee6133e9e95ef2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeConfigs", [value]))

    @jsii.member(jsii_name="putTaints")
    def put_taints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb98c7510dbfb519b1b588d0c154f5cb6873eade0735edb21e059858d8bbde9a)
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
    ) -> GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsList:
        return typing.cast(GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsList, jsii.get(self, "nodeConfigs"))

    @builtins.property
    @jsii.member(jsii_name="taints")
    def taints(
        self,
    ) -> "GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsList":
        return typing.cast("GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsList", jsii.get(self, "taints"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]], jsii.get(self, "nodeConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="operatingSystemInput")
    def operating_system_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatingSystemInput"))

    @builtins.property
    @jsii.member(jsii_name="taintsInput")
    def taints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints"]]], jsii.get(self, "taintsInput"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da6abbef4dd2faba39321abbdfdad023de31291d1bc09102edcfb296654e6a6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operatingSystem")
    def operating_system(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operatingSystem"))

    @operating_system.setter
    def operating_system(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2421939812a540759e1b20c8b81dbe1a55e2b79daef1d8c485db3694bb43666c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operatingSystem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5804d9887e3435d0af9bd4f6b23835cc343d460a712082fde7521546aafb54fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints",
    jsii_struct_bases=[],
    name_mapping={"effect": "effect", "key": "key", "value": "value"},
)
class GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints:
    def __init__(
        self,
        *,
        effect: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param effect: Specifies the nodes operating system (default: LINUX). Possible values: ["EFFECT_UNSPECIFIED", "PREFER_NO_SCHEDULE", "NO_EXECUTE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#effect GkeonpremBareMetalCluster#effect}
        :param key: Key associated with the effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#key GkeonpremBareMetalCluster#key}
        :param value: Value associated with the effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#value GkeonpremBareMetalCluster#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__115171690762f0e3a6ed020f7626ad7b684214f2a9439cc2a3e452d0ffa05df7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#effect GkeonpremBareMetalCluster#effect}
        '''
        result = self._values.get("effect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Key associated with the effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#key GkeonpremBareMetalCluster#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value associated with the effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#value GkeonpremBareMetalCluster#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__057feb378f6d5c0a99f7817199a968a0fd987e6d8bf18c0cf945ed059aafc604)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be91595cd7db01e0e813caf97e07977fc25f18e00e4cd75344c3fb91973b36d1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fe986f9270f0f44e51165287c7f9f35965610916bf6e0c434ae360c7a907c1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1aaa0903d50ffe4ff47837475c2778bb223f2d48284e96b26d68e61f72f9287)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb8ba94cd72b67fed189ac6e093e598711d47ae5cf8bda55c100c244bcadaf67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96e7f820a9818a7abee83a762f961eaafdb6f8bb46170ffcf48692bef4a664a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3692adcdb308f673b2df7ae29b52b3478658b837a28be725be924a42206b77b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c112d57514bc1073f0cfc1ba21beccf22ef438f766dcac446ca7a946d7878a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__173a7a10c43caa311fd9100e60278bed28af92c2db5e3a24f834ee576a1831dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bd3d19971551239630d999f086a8df2019478db09bad72ea5f8fcc00aef6c1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7599819daed4d1788be79275a133bfc917bb1efb0bdd7409e350a65b791ed936)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__258e5d6121db5e4a27ca6b5182e4fba272dcfabcf9611da2a05c2727e91d5f08)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodePoolConfig")
    def put_node_pool_config(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
        operating_system: typing.Optional[builtins.str] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#labels GkeonpremBareMetalCluster#labels}
        :param node_configs: node_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_configs GkeonpremBareMetalCluster#node_configs}
        :param operating_system: Specifies the nodes operating system (default: LINUX). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#operating_system GkeonpremBareMetalCluster#operating_system}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#taints GkeonpremBareMetalCluster#taints}
        '''
        value = GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig(
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
    ) -> GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigOutputReference:
        return typing.cast(GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigOutputReference, jsii.get(self, "nodePoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodePoolConfigInput")
    def node_pool_config_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig], jsii.get(self, "nodePoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d83b5a1cffb9448d54266352eb29b0c58a2dbb3fe37ff6401c7b473f96519251)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterControlPlaneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterControlPlaneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__330dac634063240a28bd60776c272c804213e89d65d816f5134632691685beb3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApiServerArgs")
    def put_api_server_args(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterControlPlaneApiServerArgs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b939a4b9b1907716717bdaaa36fb48a0ac91a8504ceea817cb1f528f618db77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putApiServerArgs", [value]))

    @jsii.member(jsii_name="putControlPlaneNodePoolConfig")
    def put_control_plane_node_pool_config(
        self,
        *,
        node_pool_config: typing.Union[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param node_pool_config: node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_pool_config GkeonpremBareMetalCluster#node_pool_config}
        '''
        value = GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig(
            node_pool_config=node_pool_config
        )

        return typing.cast(None, jsii.invoke(self, "putControlPlaneNodePoolConfig", [value]))

    @jsii.member(jsii_name="resetApiServerArgs")
    def reset_api_server_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiServerArgs", []))

    @builtins.property
    @jsii.member(jsii_name="apiServerArgs")
    def api_server_args(self) -> GkeonpremBareMetalClusterControlPlaneApiServerArgsList:
        return typing.cast(GkeonpremBareMetalClusterControlPlaneApiServerArgsList, jsii.get(self, "apiServerArgs"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneNodePoolConfig")
    def control_plane_node_pool_config(
        self,
    ) -> GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigOutputReference:
        return typing.cast(GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigOutputReference, jsii.get(self, "controlPlaneNodePoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="apiServerArgsInput")
    def api_server_args_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterControlPlaneApiServerArgs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterControlPlaneApiServerArgs]]], jsii.get(self, "apiServerArgsInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneNodePoolConfigInput")
    def control_plane_node_pool_config_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig], jsii.get(self, "controlPlaneNodePoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremBareMetalClusterControlPlane]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterControlPlane], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterControlPlane],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b3eff0e54786a58aa37ca142cf5b2bbb59511a98cbad1ef923355e880244bb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterFleet",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremBareMetalClusterFleet:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterFleet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterFleetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterFleetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dad12c10fb23f08389a2dab84f81f0739803cf47c3b4dddb17eaae7a7184f6ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalClusterFleetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ce28a1d21a0e05f3f590a35c7659f65580a894129fc5a5df0e8ff14847a3cb2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalClusterFleetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f426e6ab0a279a0f6aa7c6a55555ed876aa1d27a996afaf321f2d9976fc836e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dab7f9e78d70c462f1f3246b699a3e96b1ee219d9c3ddf39874ec2e3e85c4642)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef73bd3f381053839cd15a87c0edb55bea33419c42f4c599ccee064942932a82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterFleetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterFleetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7dae14a0e309b4772a8a61e8b2caf04e010750f467a9ff4441454017cbd98f6a)
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
    def internal_value(self) -> typing.Optional[GkeonpremBareMetalClusterFleet]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterFleet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterFleet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e9349279b9c317c8af860d24c91353fba6d19d137f39f83f8ee7876f059b2a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancer",
    jsii_struct_bases=[],
    name_mapping={
        "port_config": "portConfig",
        "vip_config": "vipConfig",
        "bgp_lb_config": "bgpLbConfig",
        "manual_lb_config": "manualLbConfig",
        "metal_lb_config": "metalLbConfig",
    },
)
class GkeonpremBareMetalClusterLoadBalancer:
    def __init__(
        self,
        *,
        port_config: typing.Union["GkeonpremBareMetalClusterLoadBalancerPortConfig", typing.Dict[builtins.str, typing.Any]],
        vip_config: typing.Union["GkeonpremBareMetalClusterLoadBalancerVipConfig", typing.Dict[builtins.str, typing.Any]],
        bgp_lb_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterLoadBalancerBgpLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        manual_lb_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterLoadBalancerManualLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        metal_lb_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterLoadBalancerMetalLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param port_config: port_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#port_config GkeonpremBareMetalCluster#port_config}
        :param vip_config: vip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#vip_config GkeonpremBareMetalCluster#vip_config}
        :param bgp_lb_config: bgp_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#bgp_lb_config GkeonpremBareMetalCluster#bgp_lb_config}
        :param manual_lb_config: manual_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#manual_lb_config GkeonpremBareMetalCluster#manual_lb_config}
        :param metal_lb_config: metal_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#metal_lb_config GkeonpremBareMetalCluster#metal_lb_config}
        '''
        if isinstance(port_config, dict):
            port_config = GkeonpremBareMetalClusterLoadBalancerPortConfig(**port_config)
        if isinstance(vip_config, dict):
            vip_config = GkeonpremBareMetalClusterLoadBalancerVipConfig(**vip_config)
        if isinstance(bgp_lb_config, dict):
            bgp_lb_config = GkeonpremBareMetalClusterLoadBalancerBgpLbConfig(**bgp_lb_config)
        if isinstance(manual_lb_config, dict):
            manual_lb_config = GkeonpremBareMetalClusterLoadBalancerManualLbConfig(**manual_lb_config)
        if isinstance(metal_lb_config, dict):
            metal_lb_config = GkeonpremBareMetalClusterLoadBalancerMetalLbConfig(**metal_lb_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbba1e8b32379e0001383bd17f63a5c2b03287e586c2b8f38625254964386d26)
            check_type(argname="argument port_config", value=port_config, expected_type=type_hints["port_config"])
            check_type(argname="argument vip_config", value=vip_config, expected_type=type_hints["vip_config"])
            check_type(argname="argument bgp_lb_config", value=bgp_lb_config, expected_type=type_hints["bgp_lb_config"])
            check_type(argname="argument manual_lb_config", value=manual_lb_config, expected_type=type_hints["manual_lb_config"])
            check_type(argname="argument metal_lb_config", value=metal_lb_config, expected_type=type_hints["metal_lb_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port_config": port_config,
            "vip_config": vip_config,
        }
        if bgp_lb_config is not None:
            self._values["bgp_lb_config"] = bgp_lb_config
        if manual_lb_config is not None:
            self._values["manual_lb_config"] = manual_lb_config
        if metal_lb_config is not None:
            self._values["metal_lb_config"] = metal_lb_config

    @builtins.property
    def port_config(self) -> "GkeonpremBareMetalClusterLoadBalancerPortConfig":
        '''port_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#port_config GkeonpremBareMetalCluster#port_config}
        '''
        result = self._values.get("port_config")
        assert result is not None, "Required property 'port_config' is missing"
        return typing.cast("GkeonpremBareMetalClusterLoadBalancerPortConfig", result)

    @builtins.property
    def vip_config(self) -> "GkeonpremBareMetalClusterLoadBalancerVipConfig":
        '''vip_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#vip_config GkeonpremBareMetalCluster#vip_config}
        '''
        result = self._values.get("vip_config")
        assert result is not None, "Required property 'vip_config' is missing"
        return typing.cast("GkeonpremBareMetalClusterLoadBalancerVipConfig", result)

    @builtins.property
    def bgp_lb_config(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterLoadBalancerBgpLbConfig"]:
        '''bgp_lb_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#bgp_lb_config GkeonpremBareMetalCluster#bgp_lb_config}
        '''
        result = self._values.get("bgp_lb_config")
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterLoadBalancerBgpLbConfig"], result)

    @builtins.property
    def manual_lb_config(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterLoadBalancerManualLbConfig"]:
        '''manual_lb_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#manual_lb_config GkeonpremBareMetalCluster#manual_lb_config}
        '''
        result = self._values.get("manual_lb_config")
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterLoadBalancerManualLbConfig"], result)

    @builtins.property
    def metal_lb_config(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterLoadBalancerMetalLbConfig"]:
        '''metal_lb_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#metal_lb_config GkeonpremBareMetalCluster#metal_lb_config}
        '''
        result = self._values.get("metal_lb_config")
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterLoadBalancerMetalLbConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterLoadBalancer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerBgpLbConfig",
    jsii_struct_bases=[],
    name_mapping={
        "address_pools": "addressPools",
        "asn": "asn",
        "bgp_peer_configs": "bgpPeerConfigs",
        "load_balancer_node_pool_config": "loadBalancerNodePoolConfig",
    },
)
class GkeonpremBareMetalClusterLoadBalancerBgpLbConfig:
    def __init__(
        self,
        *,
        address_pools: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools", typing.Dict[builtins.str, typing.Any]]]],
        asn: jsii.Number,
        bgp_peer_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs", typing.Dict[builtins.str, typing.Any]]]],
        load_balancer_node_pool_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param address_pools: address_pools block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#address_pools GkeonpremBareMetalCluster#address_pools}
        :param asn: BGP autonomous system number (ASN) of the cluster. This field can be updated after cluster creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#asn GkeonpremBareMetalCluster#asn}
        :param bgp_peer_configs: bgp_peer_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#bgp_peer_configs GkeonpremBareMetalCluster#bgp_peer_configs}
        :param load_balancer_node_pool_config: load_balancer_node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#load_balancer_node_pool_config GkeonpremBareMetalCluster#load_balancer_node_pool_config}
        '''
        if isinstance(load_balancer_node_pool_config, dict):
            load_balancer_node_pool_config = GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig(**load_balancer_node_pool_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a79ec60a50df9ec9a8ad9baa09b70e9c73b6c852b3c392100789adbb8733029)
            check_type(argname="argument address_pools", value=address_pools, expected_type=type_hints["address_pools"])
            check_type(argname="argument asn", value=asn, expected_type=type_hints["asn"])
            check_type(argname="argument bgp_peer_configs", value=bgp_peer_configs, expected_type=type_hints["bgp_peer_configs"])
            check_type(argname="argument load_balancer_node_pool_config", value=load_balancer_node_pool_config, expected_type=type_hints["load_balancer_node_pool_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address_pools": address_pools,
            "asn": asn,
            "bgp_peer_configs": bgp_peer_configs,
        }
        if load_balancer_node_pool_config is not None:
            self._values["load_balancer_node_pool_config"] = load_balancer_node_pool_config

    @builtins.property
    def address_pools(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools"]]:
        '''address_pools block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#address_pools GkeonpremBareMetalCluster#address_pools}
        '''
        result = self._values.get("address_pools")
        assert result is not None, "Required property 'address_pools' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools"]], result)

    @builtins.property
    def asn(self) -> jsii.Number:
        '''BGP autonomous system number (ASN) of the cluster. This field can be updated after cluster creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#asn GkeonpremBareMetalCluster#asn}
        '''
        result = self._values.get("asn")
        assert result is not None, "Required property 'asn' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def bgp_peer_configs(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs"]]:
        '''bgp_peer_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#bgp_peer_configs GkeonpremBareMetalCluster#bgp_peer_configs}
        '''
        result = self._values.get("bgp_peer_configs")
        assert result is not None, "Required property 'bgp_peer_configs' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs"]], result)

    @builtins.property
    def load_balancer_node_pool_config(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig"]:
        '''load_balancer_node_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#load_balancer_node_pool_config GkeonpremBareMetalCluster#load_balancer_node_pool_config}
        '''
        result = self._values.get("load_balancer_node_pool_config")
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterLoadBalancerBgpLbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools",
    jsii_struct_bases=[],
    name_mapping={
        "addresses": "addresses",
        "pool": "pool",
        "avoid_buggy_ips": "avoidBuggyIps",
        "manual_assign": "manualAssign",
    },
)
class GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools:
    def __init__(
        self,
        *,
        addresses: typing.Sequence[builtins.str],
        pool: builtins.str,
        avoid_buggy_ips: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        manual_assign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param addresses: The addresses that are part of this pool. Each address must be either in the CIDR form (1.2.3.0/24) or range form (1.2.3.1-1.2.3.5). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#addresses GkeonpremBareMetalCluster#addresses}
        :param pool: The name of the address pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#pool GkeonpremBareMetalCluster#pool}
        :param avoid_buggy_ips: If true, avoid using IPs ending in .0 or .255. This avoids buggy consumer devices mistakenly dropping IPv4 traffic for those special IP addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#avoid_buggy_ips GkeonpremBareMetalCluster#avoid_buggy_ips}
        :param manual_assign: If true, prevent IP addresses from being automatically assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#manual_assign GkeonpremBareMetalCluster#manual_assign}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__391f9512743e6f8bb5e06db2487cfffd7fe19c8244863492da28bbd6081691da)
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

        Each address must be either in the CIDR form (1.2.3.0/24) or range form (1.2.3.1-1.2.3.5).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#addresses GkeonpremBareMetalCluster#addresses}
        '''
        result = self._values.get("addresses")
        assert result is not None, "Required property 'addresses' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def pool(self) -> builtins.str:
        '''The name of the address pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#pool GkeonpremBareMetalCluster#pool}
        '''
        result = self._values.get("pool")
        assert result is not None, "Required property 'pool' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def avoid_buggy_ips(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, avoid using IPs ending in .0 or .255. This avoids buggy consumer devices mistakenly dropping IPv4 traffic for those special IP addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#avoid_buggy_ips GkeonpremBareMetalCluster#avoid_buggy_ips}
        '''
        result = self._values.get("avoid_buggy_ips")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def manual_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, prevent IP addresses from being automatically assigned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#manual_assign GkeonpremBareMetalCluster#manual_assign}
        '''
        result = self._values.get("manual_assign")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPoolsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPoolsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c428ac965fca760652066b85ae15aa905e279f5f9a70db9a7ed3a186c2a76525)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPoolsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5c6b4450d6f9c6fc9a5cc9341bfab530195f0c246b1fe0684fd3848dd5fe8e8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPoolsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b79d8f157a0e84c83529b38623e12d3b6ffa47527c9f7d6be81168ced7624cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a68aaec309bed22cde9b6393ae9e5dabd6771c97e2ec6beb37d19ddbb9a1994)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26dc9863bcfb9ceb107b1e1891b95626a915d77a34dc7243f58065016d901dba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a33b8c232827798df71e6761e8d3dc7f55be3f332704514eb723e3de911dff40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPoolsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPoolsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71c36bb3e1d1529487bc05b238297a21e51ef54ade9843ac6fc444d75eee0af7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ccfd3ee6e0507af5a9b4845d0b13a423e3dab5dc154567f60f34d1027b279f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b39094360536596e068f30c5d70151901add36cd286ae9e5ce720b8198d2ed54)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae37be4c320f997cbbbd83560c59d7673b8f3645607b02d6cb3b61a0b8e9b368)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manualAssign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pool")
    def pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pool"))

    @pool.setter
    def pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc4b25366bd8d4036d9180698b6e555ac3c3b537226d8cb20fa74aedc57fdefa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e3005f473ddd47804f10cbc82b6d2d89ef3632e97f39a4f4d708ab52b56dd7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "asn": "asn",
        "ip_address": "ipAddress",
        "control_plane_nodes": "controlPlaneNodes",
    },
)
class GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs:
    def __init__(
        self,
        *,
        asn: jsii.Number,
        ip_address: builtins.str,
        control_plane_nodes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param asn: BGP autonomous system number (ASN) for the network that contains the external peer device. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#asn GkeonpremBareMetalCluster#asn}
        :param ip_address: The IP address of the external peer device. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#ip_address GkeonpremBareMetalCluster#ip_address}
        :param control_plane_nodes: The IP address of the control plane node that connects to the external peer. If you don't specify any control plane nodes, all control plane nodes can connect to the external peer. If you specify one or more IP addresses, only the nodes specified participate in peering sessions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#control_plane_nodes GkeonpremBareMetalCluster#control_plane_nodes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1901dbd3f98933c6d29f4f8fda3638e168eede552a581654326f90a8f3b5cfc8)
            check_type(argname="argument asn", value=asn, expected_type=type_hints["asn"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument control_plane_nodes", value=control_plane_nodes, expected_type=type_hints["control_plane_nodes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "asn": asn,
            "ip_address": ip_address,
        }
        if control_plane_nodes is not None:
            self._values["control_plane_nodes"] = control_plane_nodes

    @builtins.property
    def asn(self) -> jsii.Number:
        '''BGP autonomous system number (ASN) for the network that contains the external peer device.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#asn GkeonpremBareMetalCluster#asn}
        '''
        result = self._values.get("asn")
        assert result is not None, "Required property 'asn' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def ip_address(self) -> builtins.str:
        '''The IP address of the external peer device.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#ip_address GkeonpremBareMetalCluster#ip_address}
        '''
        result = self._values.get("ip_address")
        assert result is not None, "Required property 'ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def control_plane_nodes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IP address of the control plane node that connects to the external peer.

        If you don't specify any control plane nodes, all control plane nodes
        can connect to the external peer. If you specify one or more IP addresses,
        only the nodes specified participate in peering sessions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#control_plane_nodes GkeonpremBareMetalCluster#control_plane_nodes}
        '''
        result = self._values.get("control_plane_nodes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ce562b36d3ed3533c3704189a2ab573bb5a95a4f822f40c848f022a232e75c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04eca7ad56ed500f41fdb60dda3ed99f0e641b5a6c33427dffad583a870e9290)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38239acb7f798f7e9355e4eb46bd064a7f08c167fed5fe78e053be16c0b36a2b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5d2d444914b6b214f5de53f72abcbcff25bca734a80712c4748f0f819213b9c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c30dc9280aef71de321a299af9d7cbcbf65aa9312bd409afef6d0c1d84a0ac2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__828b9c5344a61081e0cbbe4a654500356b54d9cfdfc35d1a37c9754153027c28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70914022b6ddf80690a6b0a8fee2cc7da2cddf23666dc3daa53fd5f0477b2b39)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetControlPlaneNodes")
    def reset_control_plane_nodes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControlPlaneNodes", []))

    @builtins.property
    @jsii.member(jsii_name="asnInput")
    def asn_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "asnInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneNodesInput")
    def control_plane_nodes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "controlPlaneNodesInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="asn")
    def asn(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "asn"))

    @asn.setter
    def asn(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2c024f7de722ee6413c0b4480e0533dcbdbb8705a59dc8e66682c823fcd65b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "asn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="controlPlaneNodes")
    def control_plane_nodes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "controlPlaneNodes"))

    @control_plane_nodes.setter
    def control_plane_nodes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7ee2459eec54c43e5d157d0ec0836ccecf8b7a7e74a6cb07aed16252f3d3c4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneNodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a4f880da4c34d34db7c4f83041469c86ee28ad212c8288faa8034b16416cfe9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96d3dd6f1c0d9e87f4759c344da027feee6d89bcff8b0b6cfc67791958fa547e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig",
    jsii_struct_bases=[],
    name_mapping={"node_pool_config": "nodePoolConfig"},
)
class GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig:
    def __init__(
        self,
        *,
        node_pool_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param node_pool_config: node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_pool_config GkeonpremBareMetalCluster#node_pool_config}
        '''
        if isinstance(node_pool_config, dict):
            node_pool_config = GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig(**node_pool_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f1564f80139fc932f790981b4455db0cdc96e005d62913488bf48b3363d45f)
            check_type(argname="argument node_pool_config", value=node_pool_config, expected_type=type_hints["node_pool_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if node_pool_config is not None:
            self._values["node_pool_config"] = node_pool_config

    @builtins.property
    def node_pool_config(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig"]:
        '''node_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_pool_config GkeonpremBareMetalCluster#node_pool_config}
        '''
        result = self._values.get("node_pool_config")
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig",
    jsii_struct_bases=[],
    name_mapping={
        "kubelet_config": "kubeletConfig",
        "labels": "labels",
        "node_configs": "nodeConfigs",
        "operating_system": "operatingSystem",
        "taints": "taints",
    },
)
class GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig:
    def __init__(
        self,
        *,
        kubelet_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operating_system: typing.Optional[builtins.str] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param kubelet_config: kubelet_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#kubelet_config GkeonpremBareMetalCluster#kubelet_config}
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#labels GkeonpremBareMetalCluster#labels}
        :param node_configs: node_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_configs GkeonpremBareMetalCluster#node_configs}
        :param operating_system: Specifies the nodes operating system (default: LINUX). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#operating_system GkeonpremBareMetalCluster#operating_system}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#taints GkeonpremBareMetalCluster#taints}
        '''
        if isinstance(kubelet_config, dict):
            kubelet_config = GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig(**kubelet_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23caf1a0e1d5bbbfc83665eb114f3fe9b28d5bf29c0f3ee73f2263effad6ae13)
            check_type(argname="argument kubelet_config", value=kubelet_config, expected_type=type_hints["kubelet_config"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument node_configs", value=node_configs, expected_type=type_hints["node_configs"])
            check_type(argname="argument operating_system", value=operating_system, expected_type=type_hints["operating_system"])
            check_type(argname="argument taints", value=taints, expected_type=type_hints["taints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kubelet_config is not None:
            self._values["kubelet_config"] = kubelet_config
        if labels is not None:
            self._values["labels"] = labels
        if node_configs is not None:
            self._values["node_configs"] = node_configs
        if operating_system is not None:
            self._values["operating_system"] = operating_system
        if taints is not None:
            self._values["taints"] = taints

    @builtins.property
    def kubelet_config(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig"]:
        '''kubelet_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#kubelet_config GkeonpremBareMetalCluster#kubelet_config}
        '''
        result = self._values.get("kubelet_config")
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig"], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#labels GkeonpremBareMetalCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def node_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs"]]]:
        '''node_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_configs GkeonpremBareMetalCluster#node_configs}
        '''
        result = self._values.get("node_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs"]]], result)

    @builtins.property
    def operating_system(self) -> typing.Optional[builtins.str]:
        '''Specifies the nodes operating system (default: LINUX).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#operating_system GkeonpremBareMetalCluster#operating_system}
        '''
        result = self._values.get("operating_system")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def taints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints"]]]:
        '''taints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#taints GkeonpremBareMetalCluster#taints}
        '''
        result = self._values.get("taints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig",
    jsii_struct_bases=[],
    name_mapping={
        "registry_burst": "registryBurst",
        "registry_pull_qps": "registryPullQps",
        "serialize_image_pulls_disabled": "serializeImagePullsDisabled",
    },
)
class GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig:
    def __init__(
        self,
        *,
        registry_burst: typing.Optional[jsii.Number] = None,
        registry_pull_qps: typing.Optional[jsii.Number] = None,
        serialize_image_pulls_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param registry_burst: The maximum size of bursty pulls, temporarily allows pulls to burst to this number, while still not exceeding registry_pull_qps. The value must not be a negative number. Updating this field may impact scalability by changing the amount of traffic produced by image pulls. Defaults to 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#registry_burst GkeonpremBareMetalCluster#registry_burst}
        :param registry_pull_qps: The limit of registry pulls per second. Setting this value to 0 means no limit. Updating this field may impact scalability by changing the amount of traffic produced by image pulls. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#registry_pull_qps GkeonpremBareMetalCluster#registry_pull_qps}
        :param serialize_image_pulls_disabled: Prevents the Kubelet from pulling multiple images at a time. We recommend *not* changing the default value on nodes that run docker daemon with version < 1.9 or an Another Union File System (Aufs) storage backend. Issue https://github.com/kubernetes/kubernetes/issues/10959 has more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#serialize_image_pulls_disabled GkeonpremBareMetalCluster#serialize_image_pulls_disabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37ec516c494a0e9bf6f091fe7c5cd2dc932462b9ca7c7cbeb4d1fef075e03af4)
            check_type(argname="argument registry_burst", value=registry_burst, expected_type=type_hints["registry_burst"])
            check_type(argname="argument registry_pull_qps", value=registry_pull_qps, expected_type=type_hints["registry_pull_qps"])
            check_type(argname="argument serialize_image_pulls_disabled", value=serialize_image_pulls_disabled, expected_type=type_hints["serialize_image_pulls_disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if registry_burst is not None:
            self._values["registry_burst"] = registry_burst
        if registry_pull_qps is not None:
            self._values["registry_pull_qps"] = registry_pull_qps
        if serialize_image_pulls_disabled is not None:
            self._values["serialize_image_pulls_disabled"] = serialize_image_pulls_disabled

    @builtins.property
    def registry_burst(self) -> typing.Optional[jsii.Number]:
        '''The maximum size of bursty pulls, temporarily allows pulls to burst to this number, while still not exceeding registry_pull_qps.

        The value must not be a negative number.
        Updating this field may impact scalability by changing the amount of
        traffic produced by image pulls.
        Defaults to 10.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#registry_burst GkeonpremBareMetalCluster#registry_burst}
        '''
        result = self._values.get("registry_burst")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def registry_pull_qps(self) -> typing.Optional[jsii.Number]:
        '''The limit of registry pulls per second.

        Setting this value to 0 means no limit.
        Updating this field may impact scalability by changing the amount of
        traffic produced by image pulls.
        Defaults to 5.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#registry_pull_qps GkeonpremBareMetalCluster#registry_pull_qps}
        '''
        result = self._values.get("registry_pull_qps")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def serialize_image_pulls_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Prevents the Kubelet from pulling multiple images at a time.

        We recommend *not* changing the default value on nodes that run docker
        daemon with version  < 1.9 or an Another Union File System (Aufs) storage
        backend. Issue https://github.com/kubernetes/kubernetes/issues/10959 has
        more details.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#serialize_image_pulls_disabled GkeonpremBareMetalCluster#serialize_image_pulls_disabled}
        '''
        result = self._values.get("serialize_image_pulls_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1f51ca1d5b50b5d7bc0e559707913146a7e79043a424e3b6220aa064fed0f5a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRegistryBurst")
    def reset_registry_burst(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegistryBurst", []))

    @jsii.member(jsii_name="resetRegistryPullQps")
    def reset_registry_pull_qps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegistryPullQps", []))

    @jsii.member(jsii_name="resetSerializeImagePullsDisabled")
    def reset_serialize_image_pulls_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSerializeImagePullsDisabled", []))

    @builtins.property
    @jsii.member(jsii_name="registryBurstInput")
    def registry_burst_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "registryBurstInput"))

    @builtins.property
    @jsii.member(jsii_name="registryPullQpsInput")
    def registry_pull_qps_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "registryPullQpsInput"))

    @builtins.property
    @jsii.member(jsii_name="serializeImagePullsDisabledInput")
    def serialize_image_pulls_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "serializeImagePullsDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="registryBurst")
    def registry_burst(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "registryBurst"))

    @registry_burst.setter
    def registry_burst(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eada670194f994e26665a389170c4330f30d7f8a9ef844184b9a2c4d5137ac24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registryBurst", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="registryPullQps")
    def registry_pull_qps(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "registryPullQps"))

    @registry_pull_qps.setter
    def registry_pull_qps(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__663c927522de7d8e1780e625293bd09497c0ea36142396ce15675ea580b14b82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registryPullQps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serializeImagePullsDisabled")
    def serialize_image_pulls_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "serializeImagePullsDisabled"))

    @serialize_image_pulls_disabled.setter
    def serialize_image_pulls_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed7e77d0de27a2c74b25bd782e6022cec97cc43534b86c8e0ce8b6f01de7613c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serializeImagePullsDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40b71335308738a61e1b9da312ce6120cf5e78b848b9da296d9a35ee77f09791)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels", "node_ip": "nodeIp"},
)
class GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_ip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#labels GkeonpremBareMetalCluster#labels}
        :param node_ip: The default IPv4 address for SSH access and Kubernetes node. Example: 192.168.0.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_ip GkeonpremBareMetalCluster#node_ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2d45773caded0c477a91f0e02c82c3da9e35823d3e2968beb5078b6a4f0429)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#labels GkeonpremBareMetalCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def node_ip(self) -> typing.Optional[builtins.str]:
        '''The default IPv4 address for SSH access and Kubernetes node. Example: 192.168.0.1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_ip GkeonpremBareMetalCluster#node_ip}
        '''
        result = self._values.get("node_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0dc8f3546e756664c31efd3acd2faf734feb1926b89e74f94d2835eaccd8ce7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__187c941085541ab2bdcf682e9c4b83d4075b8c60325ba5d9eb5b92cb3d312f41)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__007c05a742150c4efaae51cdce020dab55f79857c80232530dcc9ec78fc93cb5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d8119b14f0214446381bab1b35d47cac87d088027491249fa551b9d5a89b9fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eae1f4aba28d5e5da10ad6340e4ba4fdd1ae4be31617d3a04ae6ad9e208b3516)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28cfa1dd7bcf6dde68e98f47a732bdd127d8702f1808a504d59f5294ffda9bac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11c854c47caeab538af218098420fc3564bdcc444cd3be8cc0a8d7eb5affbc10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73ab926a050be8cb74f6586718ddba8000e016b75589b800095d4436beb69bdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeIp")
    def node_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeIp"))

    @node_ip.setter
    def node_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8467b82a158f9bbd36edab667b3d5a228dd681544f16d4ac7efbe007fa4c4ff3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b035f35664df0486481228aadcb4d3b54d78565fba19369a3cc84798cdbe632)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88cd344151baa28c4dcbaff13027df1aabdfe5775b1e95bfdfd2fdb0dc25dae4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putKubeletConfig")
    def put_kubelet_config(
        self,
        *,
        registry_burst: typing.Optional[jsii.Number] = None,
        registry_pull_qps: typing.Optional[jsii.Number] = None,
        serialize_image_pulls_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param registry_burst: The maximum size of bursty pulls, temporarily allows pulls to burst to this number, while still not exceeding registry_pull_qps. The value must not be a negative number. Updating this field may impact scalability by changing the amount of traffic produced by image pulls. Defaults to 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#registry_burst GkeonpremBareMetalCluster#registry_burst}
        :param registry_pull_qps: The limit of registry pulls per second. Setting this value to 0 means no limit. Updating this field may impact scalability by changing the amount of traffic produced by image pulls. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#registry_pull_qps GkeonpremBareMetalCluster#registry_pull_qps}
        :param serialize_image_pulls_disabled: Prevents the Kubelet from pulling multiple images at a time. We recommend *not* changing the default value on nodes that run docker daemon with version < 1.9 or an Another Union File System (Aufs) storage backend. Issue https://github.com/kubernetes/kubernetes/issues/10959 has more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#serialize_image_pulls_disabled GkeonpremBareMetalCluster#serialize_image_pulls_disabled}
        '''
        value = GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig(
            registry_burst=registry_burst,
            registry_pull_qps=registry_pull_qps,
            serialize_image_pulls_disabled=serialize_image_pulls_disabled,
        )

        return typing.cast(None, jsii.invoke(self, "putKubeletConfig", [value]))

    @jsii.member(jsii_name="putNodeConfigs")
    def put_node_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be99e2cdf503d07a772951c8a03697407d3532825949d5dcda592892448a8d14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeConfigs", [value]))

    @jsii.member(jsii_name="putTaints")
    def put_taints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99a4f50940bb07a6e9602ee54f1f9d14e4152cf52c4c1d96d41043137c0ebc55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTaints", [value]))

    @jsii.member(jsii_name="resetKubeletConfig")
    def reset_kubelet_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubeletConfig", []))

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
    @jsii.member(jsii_name="kubeletConfig")
    def kubelet_config(
        self,
    ) -> GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfigOutputReference:
        return typing.cast(GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfigOutputReference, jsii.get(self, "kubeletConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfigs")
    def node_configs(
        self,
    ) -> GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsList:
        return typing.cast(GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsList, jsii.get(self, "nodeConfigs"))

    @builtins.property
    @jsii.member(jsii_name="taints")
    def taints(
        self,
    ) -> "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsList":
        return typing.cast("GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsList", jsii.get(self, "taints"))

    @builtins.property
    @jsii.member(jsii_name="kubeletConfigInput")
    def kubelet_config_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig], jsii.get(self, "kubeletConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]], jsii.get(self, "nodeConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="operatingSystemInput")
    def operating_system_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatingSystemInput"))

    @builtins.property
    @jsii.member(jsii_name="taintsInput")
    def taints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints"]]], jsii.get(self, "taintsInput"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98fe4ae45a067a99d51c79f6c619ff60bf6dc68a0a6fe0170b7908a1b021fe7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operatingSystem")
    def operating_system(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operatingSystem"))

    @operating_system.setter
    def operating_system(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6310e497038c746da3603efb0ddee8370e62cf7c919b3317b22409d460e0124a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operatingSystem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3322a9b68e0a31f8edd61416ee103b8675956fe9c655123d4395eea54cf3a57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints",
    jsii_struct_bases=[],
    name_mapping={"effect": "effect", "key": "key", "value": "value"},
)
class GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints:
    def __init__(
        self,
        *,
        effect: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param effect: Specifies the nodes operating system (default: LINUX). Possible values: ["EFFECT_UNSPECIFIED", "PREFER_NO_SCHEDULE", "NO_EXECUTE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#effect GkeonpremBareMetalCluster#effect}
        :param key: Key associated with the effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#key GkeonpremBareMetalCluster#key}
        :param value: Value associated with the effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#value GkeonpremBareMetalCluster#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdb5fc700549a4ed85ad92f06dd402ad5752d13a8ba630c01be461121f2919ee)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#effect GkeonpremBareMetalCluster#effect}
        '''
        result = self._values.get("effect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Key associated with the effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#key GkeonpremBareMetalCluster#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value associated with the effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#value GkeonpremBareMetalCluster#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c58f151e2e772b827f7eede4087479f47365e744c5d46de2fda8a68b640e0ca5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cee14f25d4a960fc4aaaa753267d136ec5efbe3c0f21a632267860192d6d1dcf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eff3491bdbed3fe46f3069ca8010a96160663d5eddcebe8b347ce79713b00a96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__521537c4c70fd2316d8a2bbe4c22bd0dfa42899e1ef7abeae7254a749a4d3ad4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f54abfc3df237b03003aa34b33d959bc866dd0c01b03b785d7939a74f47e84e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d276ba8f30fc1fae7a13116f2ae218ae5e54417daa0a6b0243fc436fa740e2dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1045665c2e123ac8df1e24b4d9615a97d64e027ef2dd70b8a59e27b877cf8700)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f2c209fc7c9910dcf8d9ca48dcd9dbc23c002bea3550b04b6acbe7803ea7e0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43c224519178a9223a3df276d19555fd53a30d9733b9a881a8d1adef9f691d21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddc1eb0efe3ad6cd90d14edd4f41ea94ee75fd909422092bbbf17162df2d53dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffa4854a02c67a527eafd4d0d2ab9580d6ab6b07752f90ab87f9076ac57fa88f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbd09e98d273b5a613d84daa2057fbcb36b7f2a85143a2189a713703e395a91b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodePoolConfig")
    def put_node_pool_config(
        self,
        *,
        kubelet_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
        operating_system: typing.Optional[builtins.str] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param kubelet_config: kubelet_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#kubelet_config GkeonpremBareMetalCluster#kubelet_config}
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#labels GkeonpremBareMetalCluster#labels}
        :param node_configs: node_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_configs GkeonpremBareMetalCluster#node_configs}
        :param operating_system: Specifies the nodes operating system (default: LINUX). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#operating_system GkeonpremBareMetalCluster#operating_system}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#taints GkeonpremBareMetalCluster#taints}
        '''
        value = GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig(
            kubelet_config=kubelet_config,
            labels=labels,
            node_configs=node_configs,
            operating_system=operating_system,
            taints=taints,
        )

        return typing.cast(None, jsii.invoke(self, "putNodePoolConfig", [value]))

    @jsii.member(jsii_name="resetNodePoolConfig")
    def reset_node_pool_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodePoolConfig", []))

    @builtins.property
    @jsii.member(jsii_name="nodePoolConfig")
    def node_pool_config(
        self,
    ) -> GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigOutputReference:
        return typing.cast(GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigOutputReference, jsii.get(self, "nodePoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodePoolConfigInput")
    def node_pool_config_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig], jsii.get(self, "nodePoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13ed83e6a45c85fe65aa3375e9faccb1b4e8e06942c7eff0179a601514e0db1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterLoadBalancerBgpLbConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerBgpLbConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ef075ace539f964b5771bbfaa88a6c3f111be6c72eb9035c1afd1436f1313e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAddressPools")
    def put_address_pools(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38f0bf0fb899f5d484a5cb4006131a972ef0c76162a63db6a661890f9dc6b8f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAddressPools", [value]))

    @jsii.member(jsii_name="putBgpPeerConfigs")
    def put_bgp_peer_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9abb970e750c8e51b6c3e80f81af97bfca83661e7612102afdfa2f3f6443ab94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBgpPeerConfigs", [value]))

    @jsii.member(jsii_name="putLoadBalancerNodePoolConfig")
    def put_load_balancer_node_pool_config(
        self,
        *,
        node_pool_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param node_pool_config: node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_pool_config GkeonpremBareMetalCluster#node_pool_config}
        '''
        value = GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig(
            node_pool_config=node_pool_config
        )

        return typing.cast(None, jsii.invoke(self, "putLoadBalancerNodePoolConfig", [value]))

    @jsii.member(jsii_name="resetLoadBalancerNodePoolConfig")
    def reset_load_balancer_node_pool_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancerNodePoolConfig", []))

    @builtins.property
    @jsii.member(jsii_name="addressPools")
    def address_pools(
        self,
    ) -> GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPoolsList:
        return typing.cast(GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPoolsList, jsii.get(self, "addressPools"))

    @builtins.property
    @jsii.member(jsii_name="bgpPeerConfigs")
    def bgp_peer_configs(
        self,
    ) -> GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigsList:
        return typing.cast(GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigsList, jsii.get(self, "bgpPeerConfigs"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerNodePoolConfig")
    def load_balancer_node_pool_config(
        self,
    ) -> GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigOutputReference:
        return typing.cast(GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigOutputReference, jsii.get(self, "loadBalancerNodePoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="addressPoolsInput")
    def address_pools_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools]]], jsii.get(self, "addressPoolsInput"))

    @builtins.property
    @jsii.member(jsii_name="asnInput")
    def asn_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "asnInput"))

    @builtins.property
    @jsii.member(jsii_name="bgpPeerConfigsInput")
    def bgp_peer_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs]]], jsii.get(self, "bgpPeerConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerNodePoolConfigInput")
    def load_balancer_node_pool_config_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig], jsii.get(self, "loadBalancerNodePoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="asn")
    def asn(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "asn"))

    @asn.setter
    def asn(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__608fb39081a579962d2c24e0bb9a4bdaeeb56401ef4d237ed86ad0f3f4b0452f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "asn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b288a764972a6cf42519e7f6ad4865f2b2a3edd7c20005a78d84706223b646d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerManualLbConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GkeonpremBareMetalClusterLoadBalancerManualLbConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether manual load balancing is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#enabled GkeonpremBareMetalCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7e663463f51bcb9858cc888900d593183511e20538bb75237f2a73e541905fc)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether manual load balancing is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#enabled GkeonpremBareMetalCluster#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterLoadBalancerManualLbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterLoadBalancerManualLbConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerManualLbConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__befa13d3c08b1b3ca2f7d47ac565c16fe3c809dd19f034fd55ca21aa66393d3e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc31ba25bcd6ef9a23867a061a049b7a010e9e983bb181d7ce9007f0710a4296)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterLoadBalancerManualLbConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterLoadBalancerManualLbConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterLoadBalancerManualLbConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d8ad3830fb0cf52fe589cd849a44358d37f1142347ff8415b56658a50f42ae7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerMetalLbConfig",
    jsii_struct_bases=[],
    name_mapping={
        "address_pools": "addressPools",
        "load_balancer_node_pool_config": "loadBalancerNodePoolConfig",
    },
)
class GkeonpremBareMetalClusterLoadBalancerMetalLbConfig:
    def __init__(
        self,
        *,
        address_pools: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools", typing.Dict[builtins.str, typing.Any]]]],
        load_balancer_node_pool_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param address_pools: address_pools block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#address_pools GkeonpremBareMetalCluster#address_pools}
        :param load_balancer_node_pool_config: load_balancer_node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#load_balancer_node_pool_config GkeonpremBareMetalCluster#load_balancer_node_pool_config}
        '''
        if isinstance(load_balancer_node_pool_config, dict):
            load_balancer_node_pool_config = GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig(**load_balancer_node_pool_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f366b7b9737cf1f4a0c580909499fbd58fa91841cf1d7f84305fc98146cffe2)
            check_type(argname="argument address_pools", value=address_pools, expected_type=type_hints["address_pools"])
            check_type(argname="argument load_balancer_node_pool_config", value=load_balancer_node_pool_config, expected_type=type_hints["load_balancer_node_pool_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address_pools": address_pools,
        }
        if load_balancer_node_pool_config is not None:
            self._values["load_balancer_node_pool_config"] = load_balancer_node_pool_config

    @builtins.property
    def address_pools(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools"]]:
        '''address_pools block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#address_pools GkeonpremBareMetalCluster#address_pools}
        '''
        result = self._values.get("address_pools")
        assert result is not None, "Required property 'address_pools' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools"]], result)

    @builtins.property
    def load_balancer_node_pool_config(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig"]:
        '''load_balancer_node_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#load_balancer_node_pool_config GkeonpremBareMetalCluster#load_balancer_node_pool_config}
        '''
        result = self._values.get("load_balancer_node_pool_config")
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterLoadBalancerMetalLbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools",
    jsii_struct_bases=[],
    name_mapping={
        "addresses": "addresses",
        "pool": "pool",
        "avoid_buggy_ips": "avoidBuggyIps",
        "manual_assign": "manualAssign",
    },
)
class GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools:
    def __init__(
        self,
        *,
        addresses: typing.Sequence[builtins.str],
        pool: builtins.str,
        avoid_buggy_ips: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        manual_assign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param addresses: The addresses that are part of this pool. Each address must be either in the CIDR form (1.2.3.0/24) or range form (1.2.3.1-1.2.3.5). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#addresses GkeonpremBareMetalCluster#addresses}
        :param pool: The name of the address pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#pool GkeonpremBareMetalCluster#pool}
        :param avoid_buggy_ips: If true, avoid using IPs ending in .0 or .255. This avoids buggy consumer devices mistakenly dropping IPv4 traffic for those special IP addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#avoid_buggy_ips GkeonpremBareMetalCluster#avoid_buggy_ips}
        :param manual_assign: If true, prevent IP addresses from being automatically assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#manual_assign GkeonpremBareMetalCluster#manual_assign}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edc60ba5a8c9ff08503241de995b75dd2d5453a4cc1f440a2dde1c99737a2990)
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

        Each address must be either in the CIDR form (1.2.3.0/24) or range form (1.2.3.1-1.2.3.5).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#addresses GkeonpremBareMetalCluster#addresses}
        '''
        result = self._values.get("addresses")
        assert result is not None, "Required property 'addresses' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def pool(self) -> builtins.str:
        '''The name of the address pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#pool GkeonpremBareMetalCluster#pool}
        '''
        result = self._values.get("pool")
        assert result is not None, "Required property 'pool' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def avoid_buggy_ips(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, avoid using IPs ending in .0 or .255. This avoids buggy consumer devices mistakenly dropping IPv4 traffic for those special IP addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#avoid_buggy_ips GkeonpremBareMetalCluster#avoid_buggy_ips}
        '''
        result = self._values.get("avoid_buggy_ips")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def manual_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, prevent IP addresses from being automatically assigned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#manual_assign GkeonpremBareMetalCluster#manual_assign}
        '''
        result = self._values.get("manual_assign")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPoolsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPoolsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aecd3a86487fb6cf458e289fcebfb604ca36b34fe837ce9d7ce9493848d55739)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPoolsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f034c907edacfb0e7f5f990cdd0b752d1c1492ffd9c30c438399b4b55df4e47)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPoolsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcb1b7099159c70eecb98d9ff6f36a7f02192d66c156f9b183c003b4a55f1df5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6f4e87a110a7add5bf9f6e37d0b4f8a5d4d8a155d9a3e7ef9350f6bc1dab57d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0f1246e7b54488d8433cccded5ecfed3b900eec85b15dbf3f948a3acf71a81e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c85cb2b5ea2ee6e99619a32e5b6daed6629660e04f735c1a0e7d5b1cc47cde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPoolsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPoolsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28da6c0d8a46adb1ac9af1ae95d5c0d6d30bf6442fbe818840878958e2fd330d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__056470b17f115e16aadd5b785af6cfde4a470eeea0698d4a4229cb1897b9c0e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d04c11bf32dcb8fd27a3fa0cf6bcc625066c0c5e8bb8011144da42a8e8f72dc8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90c07aeef87859257499240481e2f6df04f08908b8080cf5625267ed363901a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manualAssign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pool")
    def pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pool"))

    @pool.setter
    def pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d109ebd88e90afee413992c218e4a28e1dcd93370d988fafdca03c3bfe9224d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f87addf9107ebea857f6b39c400a98ab9bf3df0f25b276a28dea86bcdbfbc13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig",
    jsii_struct_bases=[],
    name_mapping={"node_pool_config": "nodePoolConfig"},
)
class GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig:
    def __init__(
        self,
        *,
        node_pool_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param node_pool_config: node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_pool_config GkeonpremBareMetalCluster#node_pool_config}
        '''
        if isinstance(node_pool_config, dict):
            node_pool_config = GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig(**node_pool_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af2fc90c6888f489e470a3d0017be2f5e559dac88daa9a8452a123f982203aa5)
            check_type(argname="argument node_pool_config", value=node_pool_config, expected_type=type_hints["node_pool_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if node_pool_config is not None:
            self._values["node_pool_config"] = node_pool_config

    @builtins.property
    def node_pool_config(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig"]:
        '''node_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_pool_config GkeonpremBareMetalCluster#node_pool_config}
        '''
        result = self._values.get("node_pool_config")
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig",
    jsii_struct_bases=[],
    name_mapping={
        "labels": "labels",
        "node_configs": "nodeConfigs",
        "operating_system": "operatingSystem",
        "taints": "taints",
    },
)
class GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operating_system: typing.Optional[builtins.str] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#labels GkeonpremBareMetalCluster#labels}
        :param node_configs: node_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_configs GkeonpremBareMetalCluster#node_configs}
        :param operating_system: Specifies the nodes operating system (default: LINUX). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#operating_system GkeonpremBareMetalCluster#operating_system}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#taints GkeonpremBareMetalCluster#taints}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeca46ab3fecd5cf5139de22702b6de74052e9a3ed98a9f211b24edbcc18dd2c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#labels GkeonpremBareMetalCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def node_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs"]]]:
        '''node_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_configs GkeonpremBareMetalCluster#node_configs}
        '''
        result = self._values.get("node_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs"]]], result)

    @builtins.property
    def operating_system(self) -> typing.Optional[builtins.str]:
        '''Specifies the nodes operating system (default: LINUX).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#operating_system GkeonpremBareMetalCluster#operating_system}
        '''
        result = self._values.get("operating_system")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def taints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints"]]]:
        '''taints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#taints GkeonpremBareMetalCluster#taints}
        '''
        result = self._values.get("taints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels", "node_ip": "nodeIp"},
)
class GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_ip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#labels GkeonpremBareMetalCluster#labels}
        :param node_ip: The default IPv4 address for SSH access and Kubernetes node. Example: 192.168.0.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_ip GkeonpremBareMetalCluster#node_ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7931f8f5aea6f29ac45a09a21c20d11489e1c77c493884e34105beb90516c066)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#labels GkeonpremBareMetalCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def node_ip(self) -> typing.Optional[builtins.str]:
        '''The default IPv4 address for SSH access and Kubernetes node. Example: 192.168.0.1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_ip GkeonpremBareMetalCluster#node_ip}
        '''
        result = self._values.get("node_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8272e689cef0a328f7e1282875b17fd4f877bf4bf47205537a33337663f04580)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1b30528d75027882001fa2a5298d704d8f8ca1b803a19ecddf7a57cb7b7b51c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__850410eb098eccb8798ebece1d3694f7ba8accbbd78f868835df239732a1a962)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69bc2a20e33c3ebc6a0e68040d76fa62867a7e71592b794b603c686577a8d6cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__383b3d0c53007b9badef71c5aabf6ed097dfc5a2d64c8da55a9c33a32838047f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c39e5562414ba4f1e5bddeb0a861096b0cb834b7b183a47dbb9b443fa9b581d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c3048b28ef6fdd709782267361fa808c6f6b9df5c3e6de7100b1154cd7e7852)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f91da5f6928e330a9b91b24b2e8ae24c82abf7c3ab8368bc323b55dd8b49200c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeIp")
    def node_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeIp"))

    @node_ip.setter
    def node_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__067712a7bd6513e61ea3734545d757d91e67a6f7c1e5ee02cac9e4901f2e4887)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34db100287b186c7ce5f7762dca88f312a0e2195d504caf77835c118e5feceb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e151435248f24cb46d9f59392ca200bcc4d948e3c796316cd335612ecb142409)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodeConfigs")
    def put_node_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ba45ba325d5d8c4e63b18c9e0c570e45437a55af161f4b88ac663faf3c2be28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeConfigs", [value]))

    @jsii.member(jsii_name="putTaints")
    def put_taints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2e22990265addf38c33b43dcc23d5f71709a8c2c1264073ee30f9eba68301f9)
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
    ) -> GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsList:
        return typing.cast(GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsList, jsii.get(self, "nodeConfigs"))

    @builtins.property
    @jsii.member(jsii_name="taints")
    def taints(
        self,
    ) -> "GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsList":
        return typing.cast("GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsList", jsii.get(self, "taints"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]], jsii.get(self, "nodeConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="operatingSystemInput")
    def operating_system_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatingSystemInput"))

    @builtins.property
    @jsii.member(jsii_name="taintsInput")
    def taints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints"]]], jsii.get(self, "taintsInput"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48d6fb1edfa68cdb2afd91f21c954902018eecfd12cecde12893897e1297ab97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operatingSystem")
    def operating_system(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operatingSystem"))

    @operating_system.setter
    def operating_system(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5e67c66ef28a2dcf8f8dc792ef1127f0c8f40cd1df5879a7181ffec8e387dfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operatingSystem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e2400c4adc08a31490628bc4e8785deb8d827f3bd72bd316d23d02582ea6f18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints",
    jsii_struct_bases=[],
    name_mapping={"effect": "effect", "key": "key", "value": "value"},
)
class GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints:
    def __init__(
        self,
        *,
        effect: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param effect: Specifies the nodes operating system (default: LINUX). Possible values: ["EFFECT_UNSPECIFIED", "PREFER_NO_SCHEDULE", "NO_EXECUTE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#effect GkeonpremBareMetalCluster#effect}
        :param key: Key associated with the effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#key GkeonpremBareMetalCluster#key}
        :param value: Value associated with the effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#value GkeonpremBareMetalCluster#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1161e2d406cb86151341a307a92bfff1d07bf37a083110e53219dacbba6cf4aa)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#effect GkeonpremBareMetalCluster#effect}
        '''
        result = self._values.get("effect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Key associated with the effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#key GkeonpremBareMetalCluster#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value associated with the effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#value GkeonpremBareMetalCluster#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8de53f5a381c8e1d4cdece0b821f2a5251b46fbff0f39b637ebd4edb43b2f5a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1780b1de61336796df2255efaf9825a28d8a931754a8cb3c09c6b5d697baa4c1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89d0ce5c78f5803ebe4a145bf7530c9b46dbcb5b1e136401ee5cedc7180fa224)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e16a7d1a99b047dce5c4522a39da93b3a878ddc6f83305807c433574947c80e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a617706262418dd449b29b09bf761c8ec50a0a8fc702c9c73c72d3a66dc19e88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd8ea025cdd6ff363b9eb95b3e7310487f54953efacf62d967d98dc90786a5c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36737d9685f359f983334557ac9275bfb1fb2a04368ce339be6b1ced9dd21be6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9abf9e2390b9d0d01a299f7d9e7eb599449ff071372657e86a1f6f20f51dd640)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b98a2e0d18163911d1ab4239afbe2dc503dcdec85ae68391c8b05fdbed67f749)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75940181e478b9ff93745779f3c5fcfe409db82ef933db602390efe678d55736)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b631b607a5f77fe62d6b1399dd41311a2d763aad2db27e8bb69ecc36dd09a07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__899029eb510006ff9712f5139c3bdbf1fbe3c09ad5dcddf1af0aa3ccf118a61d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodePoolConfig")
    def put_node_pool_config(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
        operating_system: typing.Optional[builtins.str] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#labels GkeonpremBareMetalCluster#labels}
        :param node_configs: node_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_configs GkeonpremBareMetalCluster#node_configs}
        :param operating_system: Specifies the nodes operating system (default: LINUX). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#operating_system GkeonpremBareMetalCluster#operating_system}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#taints GkeonpremBareMetalCluster#taints}
        '''
        value = GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig(
            labels=labels,
            node_configs=node_configs,
            operating_system=operating_system,
            taints=taints,
        )

        return typing.cast(None, jsii.invoke(self, "putNodePoolConfig", [value]))

    @jsii.member(jsii_name="resetNodePoolConfig")
    def reset_node_pool_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodePoolConfig", []))

    @builtins.property
    @jsii.member(jsii_name="nodePoolConfig")
    def node_pool_config(
        self,
    ) -> GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigOutputReference:
        return typing.cast(GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigOutputReference, jsii.get(self, "nodePoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodePoolConfigInput")
    def node_pool_config_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig], jsii.get(self, "nodePoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e14feafce86273d9f6613e9c306913666e82369f3171e657219037454160d06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterLoadBalancerMetalLbConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerMetalLbConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2e7a4424432c292a14d003f7cdee4a73f02f2e255f5e83566540383221f8654)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAddressPools")
    def put_address_pools(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2010bb412a87df87e0097f5c106ef0fe85b0cfb799332ca2a2a9e378d136923)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAddressPools", [value]))

    @jsii.member(jsii_name="putLoadBalancerNodePoolConfig")
    def put_load_balancer_node_pool_config(
        self,
        *,
        node_pool_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param node_pool_config: node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#node_pool_config GkeonpremBareMetalCluster#node_pool_config}
        '''
        value = GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig(
            node_pool_config=node_pool_config
        )

        return typing.cast(None, jsii.invoke(self, "putLoadBalancerNodePoolConfig", [value]))

    @jsii.member(jsii_name="resetLoadBalancerNodePoolConfig")
    def reset_load_balancer_node_pool_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancerNodePoolConfig", []))

    @builtins.property
    @jsii.member(jsii_name="addressPools")
    def address_pools(
        self,
    ) -> GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPoolsList:
        return typing.cast(GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPoolsList, jsii.get(self, "addressPools"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerNodePoolConfig")
    def load_balancer_node_pool_config(
        self,
    ) -> GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigOutputReference:
        return typing.cast(GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigOutputReference, jsii.get(self, "loadBalancerNodePoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="addressPoolsInput")
    def address_pools_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools]]], jsii.get(self, "addressPoolsInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerNodePoolConfigInput")
    def load_balancer_node_pool_config_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig], jsii.get(self, "loadBalancerNodePoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterLoadBalancerMetalLbConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterLoadBalancerMetalLbConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterLoadBalancerMetalLbConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf78a36d418776874bdd2747cf1aa9cbe4e0745149104aed6c8c28a8ae138b0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterLoadBalancerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c0e2d198e904368ae3a84c7e216079d5cd0410d1faaef22d5b556c8a27e8da7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBgpLbConfig")
    def put_bgp_lb_config(
        self,
        *,
        address_pools: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
        asn: jsii.Number,
        bgp_peer_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs, typing.Dict[builtins.str, typing.Any]]]],
        load_balancer_node_pool_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param address_pools: address_pools block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#address_pools GkeonpremBareMetalCluster#address_pools}
        :param asn: BGP autonomous system number (ASN) of the cluster. This field can be updated after cluster creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#asn GkeonpremBareMetalCluster#asn}
        :param bgp_peer_configs: bgp_peer_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#bgp_peer_configs GkeonpremBareMetalCluster#bgp_peer_configs}
        :param load_balancer_node_pool_config: load_balancer_node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#load_balancer_node_pool_config GkeonpremBareMetalCluster#load_balancer_node_pool_config}
        '''
        value = GkeonpremBareMetalClusterLoadBalancerBgpLbConfig(
            address_pools=address_pools,
            asn=asn,
            bgp_peer_configs=bgp_peer_configs,
            load_balancer_node_pool_config=load_balancer_node_pool_config,
        )

        return typing.cast(None, jsii.invoke(self, "putBgpLbConfig", [value]))

    @jsii.member(jsii_name="putManualLbConfig")
    def put_manual_lb_config(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether manual load balancing is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#enabled GkeonpremBareMetalCluster#enabled}
        '''
        value = GkeonpremBareMetalClusterLoadBalancerManualLbConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putManualLbConfig", [value]))

    @jsii.member(jsii_name="putMetalLbConfig")
    def put_metal_lb_config(
        self,
        *,
        address_pools: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
        load_balancer_node_pool_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param address_pools: address_pools block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#address_pools GkeonpremBareMetalCluster#address_pools}
        :param load_balancer_node_pool_config: load_balancer_node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#load_balancer_node_pool_config GkeonpremBareMetalCluster#load_balancer_node_pool_config}
        '''
        value = GkeonpremBareMetalClusterLoadBalancerMetalLbConfig(
            address_pools=address_pools,
            load_balancer_node_pool_config=load_balancer_node_pool_config,
        )

        return typing.cast(None, jsii.invoke(self, "putMetalLbConfig", [value]))

    @jsii.member(jsii_name="putPortConfig")
    def put_port_config(self, *, control_plane_load_balancer_port: jsii.Number) -> None:
        '''
        :param control_plane_load_balancer_port: The port that control plane hosted load balancers will listen on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#control_plane_load_balancer_port GkeonpremBareMetalCluster#control_plane_load_balancer_port}
        '''
        value = GkeonpremBareMetalClusterLoadBalancerPortConfig(
            control_plane_load_balancer_port=control_plane_load_balancer_port
        )

        return typing.cast(None, jsii.invoke(self, "putPortConfig", [value]))

    @jsii.member(jsii_name="putVipConfig")
    def put_vip_config(
        self,
        *,
        control_plane_vip: builtins.str,
        ingress_vip: builtins.str,
    ) -> None:
        '''
        :param control_plane_vip: The VIP which you previously set aside for the Kubernetes API of this Bare Metal User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#control_plane_vip GkeonpremBareMetalCluster#control_plane_vip}
        :param ingress_vip: The VIP which you previously set aside for ingress traffic into this Bare Metal User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#ingress_vip GkeonpremBareMetalCluster#ingress_vip}
        '''
        value = GkeonpremBareMetalClusterLoadBalancerVipConfig(
            control_plane_vip=control_plane_vip, ingress_vip=ingress_vip
        )

        return typing.cast(None, jsii.invoke(self, "putVipConfig", [value]))

    @jsii.member(jsii_name="resetBgpLbConfig")
    def reset_bgp_lb_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBgpLbConfig", []))

    @jsii.member(jsii_name="resetManualLbConfig")
    def reset_manual_lb_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManualLbConfig", []))

    @jsii.member(jsii_name="resetMetalLbConfig")
    def reset_metal_lb_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetalLbConfig", []))

    @builtins.property
    @jsii.member(jsii_name="bgpLbConfig")
    def bgp_lb_config(
        self,
    ) -> GkeonpremBareMetalClusterLoadBalancerBgpLbConfigOutputReference:
        return typing.cast(GkeonpremBareMetalClusterLoadBalancerBgpLbConfigOutputReference, jsii.get(self, "bgpLbConfig"))

    @builtins.property
    @jsii.member(jsii_name="manualLbConfig")
    def manual_lb_config(
        self,
    ) -> GkeonpremBareMetalClusterLoadBalancerManualLbConfigOutputReference:
        return typing.cast(GkeonpremBareMetalClusterLoadBalancerManualLbConfigOutputReference, jsii.get(self, "manualLbConfig"))

    @builtins.property
    @jsii.member(jsii_name="metalLbConfig")
    def metal_lb_config(
        self,
    ) -> GkeonpremBareMetalClusterLoadBalancerMetalLbConfigOutputReference:
        return typing.cast(GkeonpremBareMetalClusterLoadBalancerMetalLbConfigOutputReference, jsii.get(self, "metalLbConfig"))

    @builtins.property
    @jsii.member(jsii_name="portConfig")
    def port_config(
        self,
    ) -> "GkeonpremBareMetalClusterLoadBalancerPortConfigOutputReference":
        return typing.cast("GkeonpremBareMetalClusterLoadBalancerPortConfigOutputReference", jsii.get(self, "portConfig"))

    @builtins.property
    @jsii.member(jsii_name="vipConfig")
    def vip_config(
        self,
    ) -> "GkeonpremBareMetalClusterLoadBalancerVipConfigOutputReference":
        return typing.cast("GkeonpremBareMetalClusterLoadBalancerVipConfigOutputReference", jsii.get(self, "vipConfig"))

    @builtins.property
    @jsii.member(jsii_name="bgpLbConfigInput")
    def bgp_lb_config_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfig], jsii.get(self, "bgpLbConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="manualLbConfigInput")
    def manual_lb_config_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterLoadBalancerManualLbConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterLoadBalancerManualLbConfig], jsii.get(self, "manualLbConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="metalLbConfigInput")
    def metal_lb_config_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterLoadBalancerMetalLbConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterLoadBalancerMetalLbConfig], jsii.get(self, "metalLbConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="portConfigInput")
    def port_config_input(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterLoadBalancerPortConfig"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterLoadBalancerPortConfig"], jsii.get(self, "portConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="vipConfigInput")
    def vip_config_input(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterLoadBalancerVipConfig"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterLoadBalancerVipConfig"], jsii.get(self, "vipConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremBareMetalClusterLoadBalancer]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterLoadBalancer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterLoadBalancer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59ba50de5661ad16c9c1e0a86e3710547befab6abb317d7c627f86775dc4e8d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerPortConfig",
    jsii_struct_bases=[],
    name_mapping={"control_plane_load_balancer_port": "controlPlaneLoadBalancerPort"},
)
class GkeonpremBareMetalClusterLoadBalancerPortConfig:
    def __init__(self, *, control_plane_load_balancer_port: jsii.Number) -> None:
        '''
        :param control_plane_load_balancer_port: The port that control plane hosted load balancers will listen on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#control_plane_load_balancer_port GkeonpremBareMetalCluster#control_plane_load_balancer_port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__312e6a9ee18617a01ca16fca8b4de3c86d386290c677f3793d2d47358970102b)
            check_type(argname="argument control_plane_load_balancer_port", value=control_plane_load_balancer_port, expected_type=type_hints["control_plane_load_balancer_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "control_plane_load_balancer_port": control_plane_load_balancer_port,
        }

    @builtins.property
    def control_plane_load_balancer_port(self) -> jsii.Number:
        '''The port that control plane hosted load balancers will listen on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#control_plane_load_balancer_port GkeonpremBareMetalCluster#control_plane_load_balancer_port}
        '''
        result = self._values.get("control_plane_load_balancer_port")
        assert result is not None, "Required property 'control_plane_load_balancer_port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterLoadBalancerPortConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterLoadBalancerPortConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerPortConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c12d6154fc67b0d653128645795b95955834b383bd3440990d00d97590ac868)
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
            type_hints = typing.get_type_hints(_typecheckingstub__383c6539c22dd4aeac3b369512c3104ef915de9d70f8bdd82d53a4ca8ffd16fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneLoadBalancerPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterLoadBalancerPortConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterLoadBalancerPortConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterLoadBalancerPortConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b41b39d931b48c25dff2599bca3f8d6ad3b436f3e32b0f8778ef2e8fab2581d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerVipConfig",
    jsii_struct_bases=[],
    name_mapping={"control_plane_vip": "controlPlaneVip", "ingress_vip": "ingressVip"},
)
class GkeonpremBareMetalClusterLoadBalancerVipConfig:
    def __init__(
        self,
        *,
        control_plane_vip: builtins.str,
        ingress_vip: builtins.str,
    ) -> None:
        '''
        :param control_plane_vip: The VIP which you previously set aside for the Kubernetes API of this Bare Metal User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#control_plane_vip GkeonpremBareMetalCluster#control_plane_vip}
        :param ingress_vip: The VIP which you previously set aside for ingress traffic into this Bare Metal User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#ingress_vip GkeonpremBareMetalCluster#ingress_vip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e7da560f21d74b93a60a91f697e10add218d82ab2296d90164570b209d7dd91)
            check_type(argname="argument control_plane_vip", value=control_plane_vip, expected_type=type_hints["control_plane_vip"])
            check_type(argname="argument ingress_vip", value=ingress_vip, expected_type=type_hints["ingress_vip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "control_plane_vip": control_plane_vip,
            "ingress_vip": ingress_vip,
        }

    @builtins.property
    def control_plane_vip(self) -> builtins.str:
        '''The VIP which you previously set aside for the Kubernetes API of this Bare Metal User Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#control_plane_vip GkeonpremBareMetalCluster#control_plane_vip}
        '''
        result = self._values.get("control_plane_vip")
        assert result is not None, "Required property 'control_plane_vip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ingress_vip(self) -> builtins.str:
        '''The VIP which you previously set aside for ingress traffic into this Bare Metal User Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#ingress_vip GkeonpremBareMetalCluster#ingress_vip}
        '''
        result = self._values.get("ingress_vip")
        assert result is not None, "Required property 'ingress_vip' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterLoadBalancerVipConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterLoadBalancerVipConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterLoadBalancerVipConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39d36ec219d6696a7bc64aa10940d30ab8b6a672f18871142d2b8dff8323f686)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__314bf994d8be2085229f095d0ea1042dca4f3659fc703de1fd747d224b3f4bad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneVip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingressVip")
    def ingress_vip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ingressVip"))

    @ingress_vip.setter
    def ingress_vip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0a4013cc6ddf3cb5f2440c458df7dc70c04e3428ac7324b1dcef2a009f90680)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingressVip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterLoadBalancerVipConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterLoadBalancerVipConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterLoadBalancerVipConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33e41f600d6a6aff42ee70754d9e50a3934567fa9035013c16a59d1468189bef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterMaintenanceConfig",
    jsii_struct_bases=[],
    name_mapping={"maintenance_address_cidr_blocks": "maintenanceAddressCidrBlocks"},
)
class GkeonpremBareMetalClusterMaintenanceConfig:
    def __init__(
        self,
        *,
        maintenance_address_cidr_blocks: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param maintenance_address_cidr_blocks: All IPv4 address from these ranges will be placed into maintenance mode. Nodes in maintenance mode will be cordoned and drained. When both of these are true, the "baremetal.cluster.gke.io/maintenance" annotation will be set on the node resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#maintenance_address_cidr_blocks GkeonpremBareMetalCluster#maintenance_address_cidr_blocks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1871e97979320770d73508ced0c667d9634ded5ff38da39c1b2d8ad1e4191da)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#maintenance_address_cidr_blocks GkeonpremBareMetalCluster#maintenance_address_cidr_blocks}
        '''
        result = self._values.get("maintenance_address_cidr_blocks")
        assert result is not None, "Required property 'maintenance_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterMaintenanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterMaintenanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterMaintenanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc562542ec410cb62db9753d9c29380b3b3d444390b61bd1cc55037e7d27ea75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c54a1728082a5b0749039f1b49b10d335b8d69f9a2dee047f2129ba2a3de8f4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterMaintenanceConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterMaintenanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterMaintenanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__705820854fca5c1c80e4eb6119daf45bb559e1c34747dc3147480105845795ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={
        "advanced_networking": "advancedNetworking",
        "island_mode_cidr": "islandModeCidr",
        "multiple_network_interfaces_config": "multipleNetworkInterfacesConfig",
        "sr_iov_config": "srIovConfig",
    },
)
class GkeonpremBareMetalClusterNetworkConfig:
    def __init__(
        self,
        *,
        advanced_networking: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        island_mode_cidr: typing.Optional[typing.Union["GkeonpremBareMetalClusterNetworkConfigIslandModeCidr", typing.Dict[builtins.str, typing.Any]]] = None,
        multiple_network_interfaces_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        sr_iov_config: typing.Optional[typing.Union["GkeonpremBareMetalClusterNetworkConfigSrIovConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_networking: Enables the use of advanced Anthos networking features, such as Bundled Load Balancing with BGP or the egress NAT gateway. Setting configuration for advanced networking features will automatically set this flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#advanced_networking GkeonpremBareMetalCluster#advanced_networking}
        :param island_mode_cidr: island_mode_cidr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#island_mode_cidr GkeonpremBareMetalCluster#island_mode_cidr}
        :param multiple_network_interfaces_config: multiple_network_interfaces_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#multiple_network_interfaces_config GkeonpremBareMetalCluster#multiple_network_interfaces_config}
        :param sr_iov_config: sr_iov_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#sr_iov_config GkeonpremBareMetalCluster#sr_iov_config}
        '''
        if isinstance(island_mode_cidr, dict):
            island_mode_cidr = GkeonpremBareMetalClusterNetworkConfigIslandModeCidr(**island_mode_cidr)
        if isinstance(multiple_network_interfaces_config, dict):
            multiple_network_interfaces_config = GkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig(**multiple_network_interfaces_config)
        if isinstance(sr_iov_config, dict):
            sr_iov_config = GkeonpremBareMetalClusterNetworkConfigSrIovConfig(**sr_iov_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__241ca04deec36fde0120b2be3d19277270a2f45f955f9ed7eee68dbb4e567588)
            check_type(argname="argument advanced_networking", value=advanced_networking, expected_type=type_hints["advanced_networking"])
            check_type(argname="argument island_mode_cidr", value=island_mode_cidr, expected_type=type_hints["island_mode_cidr"])
            check_type(argname="argument multiple_network_interfaces_config", value=multiple_network_interfaces_config, expected_type=type_hints["multiple_network_interfaces_config"])
            check_type(argname="argument sr_iov_config", value=sr_iov_config, expected_type=type_hints["sr_iov_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if advanced_networking is not None:
            self._values["advanced_networking"] = advanced_networking
        if island_mode_cidr is not None:
            self._values["island_mode_cidr"] = island_mode_cidr
        if multiple_network_interfaces_config is not None:
            self._values["multiple_network_interfaces_config"] = multiple_network_interfaces_config
        if sr_iov_config is not None:
            self._values["sr_iov_config"] = sr_iov_config

    @builtins.property
    def advanced_networking(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables the use of advanced Anthos networking features, such as Bundled Load Balancing with BGP or the egress NAT gateway.

        Setting configuration for advanced networking features will automatically
        set this flag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#advanced_networking GkeonpremBareMetalCluster#advanced_networking}
        '''
        result = self._values.get("advanced_networking")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def island_mode_cidr(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterNetworkConfigIslandModeCidr"]:
        '''island_mode_cidr block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#island_mode_cidr GkeonpremBareMetalCluster#island_mode_cidr}
        '''
        result = self._values.get("island_mode_cidr")
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterNetworkConfigIslandModeCidr"], result)

    @builtins.property
    def multiple_network_interfaces_config(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig"]:
        '''multiple_network_interfaces_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#multiple_network_interfaces_config GkeonpremBareMetalCluster#multiple_network_interfaces_config}
        '''
        result = self._values.get("multiple_network_interfaces_config")
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig"], result)

    @builtins.property
    def sr_iov_config(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterNetworkConfigSrIovConfig"]:
        '''sr_iov_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#sr_iov_config GkeonpremBareMetalCluster#sr_iov_config}
        '''
        result = self._values.get("sr_iov_config")
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterNetworkConfigSrIovConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterNetworkConfigIslandModeCidr",
    jsii_struct_bases=[],
    name_mapping={
        "pod_address_cidr_blocks": "podAddressCidrBlocks",
        "service_address_cidr_blocks": "serviceAddressCidrBlocks",
    },
)
class GkeonpremBareMetalClusterNetworkConfigIslandModeCidr:
    def __init__(
        self,
        *,
        pod_address_cidr_blocks: typing.Sequence[builtins.str],
        service_address_cidr_blocks: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param pod_address_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these ranges. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#pod_address_cidr_blocks GkeonpremBareMetalCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these ranges. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#service_address_cidr_blocks GkeonpremBareMetalCluster#service_address_cidr_blocks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da5f430b6b2e4da26687c1be6775b5ce6cee97bb23e820a8f9cde6d61b3a0fbb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#pod_address_cidr_blocks GkeonpremBareMetalCluster#pod_address_cidr_blocks}
        '''
        result = self._values.get("pod_address_cidr_blocks")
        assert result is not None, "Required property 'pod_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        '''All services in the cluster are assigned an RFC1918 IPv4 address from these ranges.

        This field cannot be changed after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#service_address_cidr_blocks GkeonpremBareMetalCluster#service_address_cidr_blocks}
        '''
        result = self._values.get("service_address_cidr_blocks")
        assert result is not None, "Required property 'service_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterNetworkConfigIslandModeCidr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterNetworkConfigIslandModeCidrOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterNetworkConfigIslandModeCidrOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a59f7bf3061a783d08361cb9dc6517dabe88f5d9f06d3aad3deb1a90c2236d3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fc084d41211b778acbf4827f2f7f0f1868b9c4aa62a10efbdb36c17676569e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAddressCidrBlocks")
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceAddressCidrBlocks"))

    @service_address_cidr_blocks.setter
    def service_address_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d84a8e575875356844c56b13dc2da14e5e19a22c5951aefa93f03d72959b055)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterNetworkConfigIslandModeCidr]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterNetworkConfigIslandModeCidr], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterNetworkConfigIslandModeCidr],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e607966811fff2aec910678f70f6451f05492c6e607e4bbeea96711d7f3a00b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether to enable multiple network interfaces for your pods. When set network_config.advanced_networking is automatically set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#enabled GkeonpremBareMetalCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73a803de835364cb01d06fcff9ca3436fc7287898c6137500575f801be873f16)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to enable multiple network interfaces for your pods. When set network_config.advanced_networking is automatically set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#enabled GkeonpremBareMetalCluster#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8bfd550d51f4180cb5a822a8779055b9d814c177a8f324007f03310fcfda3e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67747189923dcc233a6dc730d6291417801432b3bb973e17c903fd4d5c051381)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__105e9d6fe7214875a440695e9ae08cb9a8a1438396565d02de89810e59605b46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6f62ffb965e7b3227e60ccda944eed623bcc0eee6189282144ec30b7c16d406)
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
        :param pod_address_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these ranges. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#pod_address_cidr_blocks GkeonpremBareMetalCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these ranges. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#service_address_cidr_blocks GkeonpremBareMetalCluster#service_address_cidr_blocks}
        '''
        value = GkeonpremBareMetalClusterNetworkConfigIslandModeCidr(
            pod_address_cidr_blocks=pod_address_cidr_blocks,
            service_address_cidr_blocks=service_address_cidr_blocks,
        )

        return typing.cast(None, jsii.invoke(self, "putIslandModeCidr", [value]))

    @jsii.member(jsii_name="putMultipleNetworkInterfacesConfig")
    def put_multiple_network_interfaces_config(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether to enable multiple network interfaces for your pods. When set network_config.advanced_networking is automatically set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#enabled GkeonpremBareMetalCluster#enabled}
        '''
        value = GkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putMultipleNetworkInterfacesConfig", [value]))

    @jsii.member(jsii_name="putSrIovConfig")
    def put_sr_iov_config(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether to install the SR-IOV operator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#enabled GkeonpremBareMetalCluster#enabled}
        '''
        value = GkeonpremBareMetalClusterNetworkConfigSrIovConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putSrIovConfig", [value]))

    @jsii.member(jsii_name="resetAdvancedNetworking")
    def reset_advanced_networking(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedNetworking", []))

    @jsii.member(jsii_name="resetIslandModeCidr")
    def reset_island_mode_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIslandModeCidr", []))

    @jsii.member(jsii_name="resetMultipleNetworkInterfacesConfig")
    def reset_multiple_network_interfaces_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultipleNetworkInterfacesConfig", []))

    @jsii.member(jsii_name="resetSrIovConfig")
    def reset_sr_iov_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrIovConfig", []))

    @builtins.property
    @jsii.member(jsii_name="islandModeCidr")
    def island_mode_cidr(
        self,
    ) -> GkeonpremBareMetalClusterNetworkConfigIslandModeCidrOutputReference:
        return typing.cast(GkeonpremBareMetalClusterNetworkConfigIslandModeCidrOutputReference, jsii.get(self, "islandModeCidr"))

    @builtins.property
    @jsii.member(jsii_name="multipleNetworkInterfacesConfig")
    def multiple_network_interfaces_config(
        self,
    ) -> GkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfigOutputReference:
        return typing.cast(GkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfigOutputReference, jsii.get(self, "multipleNetworkInterfacesConfig"))

    @builtins.property
    @jsii.member(jsii_name="srIovConfig")
    def sr_iov_config(
        self,
    ) -> "GkeonpremBareMetalClusterNetworkConfigSrIovConfigOutputReference":
        return typing.cast("GkeonpremBareMetalClusterNetworkConfigSrIovConfigOutputReference", jsii.get(self, "srIovConfig"))

    @builtins.property
    @jsii.member(jsii_name="advancedNetworkingInput")
    def advanced_networking_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "advancedNetworkingInput"))

    @builtins.property
    @jsii.member(jsii_name="islandModeCidrInput")
    def island_mode_cidr_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterNetworkConfigIslandModeCidr]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterNetworkConfigIslandModeCidr], jsii.get(self, "islandModeCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="multipleNetworkInterfacesConfigInput")
    def multiple_network_interfaces_config_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig], jsii.get(self, "multipleNetworkInterfacesConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="srIovConfigInput")
    def sr_iov_config_input(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterNetworkConfigSrIovConfig"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterNetworkConfigSrIovConfig"], jsii.get(self, "srIovConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c1b2fb7e0a3b9beae5032b7d0daab2db7ae244890d06ca0a0f0006875f81ec3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advancedNetworking", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremBareMetalClusterNetworkConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5164daf4e5a0b53a5bd65411970402971eb1e82ead766ddffb7100a79cfb8b9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterNetworkConfigSrIovConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GkeonpremBareMetalClusterNetworkConfigSrIovConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether to install the SR-IOV operator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#enabled GkeonpremBareMetalCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ad8ab5df0e1d36992d407b1e4382d2e4ea7186b90f37917d278c6c20e4d13fe)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to install the SR-IOV operator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#enabled GkeonpremBareMetalCluster#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterNetworkConfigSrIovConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterNetworkConfigSrIovConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterNetworkConfigSrIovConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__014da7a7726293a3001dda8ce50063be68248118503ccc68666b638d1fa31a20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b400660e65850a03527aba33e31d3e3803a77b9955608ccf534131821ef8aec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterNetworkConfigSrIovConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterNetworkConfigSrIovConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterNetworkConfigSrIovConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45d7551755cd9f480f548767f1a5634280b210c352f15b0dd2d41704581e7442)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterNodeAccessConfig",
    jsii_struct_bases=[],
    name_mapping={"login_user": "loginUser"},
)
class GkeonpremBareMetalClusterNodeAccessConfig:
    def __init__(self, *, login_user: typing.Optional[builtins.str] = None) -> None:
        '''
        :param login_user: LoginUser is the user name used to access node machines. It defaults to "root" if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#login_user GkeonpremBareMetalCluster#login_user}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f99eb7bfb41ddaf0e59a57034aed967252d7afb90a7b7bdc2ca613eed88c30b)
            check_type(argname="argument login_user", value=login_user, expected_type=type_hints["login_user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if login_user is not None:
            self._values["login_user"] = login_user

    @builtins.property
    def login_user(self) -> typing.Optional[builtins.str]:
        '''LoginUser is the user name used to access node machines. It defaults to "root" if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#login_user GkeonpremBareMetalCluster#login_user}
        '''
        result = self._values.get("login_user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterNodeAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterNodeAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterNodeAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bb29abb60287c5fece9e33378fa18f4f220484bf1f577c24657c6a87f9f7ea6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__185ca0559130ab3c5d954f36a24b0c6ac2135049c0d7200f4d50401ca121d74b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterNodeAccessConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterNodeAccessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterNodeAccessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__febe29de259b2c260b20f37d057692c4e693e46a3a1fe8e1e3d340d198beb723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterNodeConfig",
    jsii_struct_bases=[],
    name_mapping={
        "container_runtime": "containerRuntime",
        "max_pods_per_node": "maxPodsPerNode",
    },
)
class GkeonpremBareMetalClusterNodeConfig:
    def __init__(
        self,
        *,
        container_runtime: typing.Optional[builtins.str] = None,
        max_pods_per_node: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param container_runtime: The available runtimes that can be used to run containers in a Bare Metal User Cluster. Possible values: ["CONTAINER_RUNTIME_UNSPECIFIED", "DOCKER", "CONTAINERD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#container_runtime GkeonpremBareMetalCluster#container_runtime}
        :param max_pods_per_node: The maximum number of pods a node can run. The size of the CIDR range assigned to the node will be derived from this parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#max_pods_per_node GkeonpremBareMetalCluster#max_pods_per_node}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1333b9d5e1a67abbb7ff29e77451339f73bdaf3ec4368ff71fa5cf660e3e7964)
            check_type(argname="argument container_runtime", value=container_runtime, expected_type=type_hints["container_runtime"])
            check_type(argname="argument max_pods_per_node", value=max_pods_per_node, expected_type=type_hints["max_pods_per_node"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_runtime is not None:
            self._values["container_runtime"] = container_runtime
        if max_pods_per_node is not None:
            self._values["max_pods_per_node"] = max_pods_per_node

    @builtins.property
    def container_runtime(self) -> typing.Optional[builtins.str]:
        '''The available runtimes that can be used to run containers in a Bare Metal User Cluster.

        Possible values: ["CONTAINER_RUNTIME_UNSPECIFIED", "DOCKER", "CONTAINERD"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#container_runtime GkeonpremBareMetalCluster#container_runtime}
        '''
        result = self._values.get("container_runtime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_pods_per_node(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of pods a node can run.

        The size of the CIDR range
        assigned to the node will be derived from this parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#max_pods_per_node GkeonpremBareMetalCluster#max_pods_per_node}
        '''
        result = self._values.get("max_pods_per_node")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterNodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterNodeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterNodeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b37be0312dc5e0b9aac4352ea5d6958ad4fcf8798fc7a340ae47acbc8da1dec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContainerRuntime")
    def reset_container_runtime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerRuntime", []))

    @jsii.member(jsii_name="resetMaxPodsPerNode")
    def reset_max_pods_per_node(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxPodsPerNode", []))

    @builtins.property
    @jsii.member(jsii_name="containerRuntimeInput")
    def container_runtime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerRuntimeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPodsPerNodeInput")
    def max_pods_per_node_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPodsPerNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="containerRuntime")
    def container_runtime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerRuntime"))

    @container_runtime.setter
    def container_runtime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b3b23093566d0b7f93539fb89dc2f13ad5af00b806f74c2f2b6f0452583a7f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerRuntime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxPodsPerNode")
    def max_pods_per_node(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPodsPerNode"))

    @max_pods_per_node.setter
    def max_pods_per_node(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__378f316f27562575ec83f90bfedffb32591ddcefc5cbdca5c1409d3bb898485c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPodsPerNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremBareMetalClusterNodeConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterNodeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterNodeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__171a744b5cdeaed551681f6f0218e86702619d18dce578e55c8d690d831fcf19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterOsEnvironmentConfig",
    jsii_struct_bases=[],
    name_mapping={"package_repo_excluded": "packageRepoExcluded"},
)
class GkeonpremBareMetalClusterOsEnvironmentConfig:
    def __init__(
        self,
        *,
        package_repo_excluded: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param package_repo_excluded: Whether the package repo should not be included when initializing bare metal machines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#package_repo_excluded GkeonpremBareMetalCluster#package_repo_excluded}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7742ff5e3fd4e6b0bf02c199ba4cc6d3e1708572d0a977c770d9098f8703b2dc)
            check_type(argname="argument package_repo_excluded", value=package_repo_excluded, expected_type=type_hints["package_repo_excluded"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "package_repo_excluded": package_repo_excluded,
        }

    @builtins.property
    def package_repo_excluded(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether the package repo should not be included when initializing bare metal machines.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#package_repo_excluded GkeonpremBareMetalCluster#package_repo_excluded}
        '''
        result = self._values.get("package_repo_excluded")
        assert result is not None, "Required property 'package_repo_excluded' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterOsEnvironmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterOsEnvironmentConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterOsEnvironmentConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__128f2db492bb542f57a61ed0de206ca956fb38f985c3064a40680ac04cd4859e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="packageRepoExcludedInput")
    def package_repo_excluded_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "packageRepoExcludedInput"))

    @builtins.property
    @jsii.member(jsii_name="packageRepoExcluded")
    def package_repo_excluded(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "packageRepoExcluded"))

    @package_repo_excluded.setter
    def package_repo_excluded(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ded4a30d50e6006a997be2bb1662da582ac017b1dd3e846c7178b9d67b7c700f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packageRepoExcluded", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterOsEnvironmentConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterOsEnvironmentConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterOsEnvironmentConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__845846514115030701c71702549dd8ab7ce2d0e8567d46ba86ad20a8574b5596)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterProxy",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "no_proxy": "noProxy"},
)
class GkeonpremBareMetalClusterProxy:
    def __init__(
        self,
        *,
        uri: builtins.str,
        no_proxy: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param uri: Specifies the address of your proxy server. For example: http://domain WARNING: Do not provide credentials in the format of http://(username:password@)domain these will be rejected by the server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#uri GkeonpremBareMetalCluster#uri}
        :param no_proxy: A list of IPs, hostnames, and domains that should skip the proxy. For example ["127.0.0.1", "example.com", ".corp", "localhost"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#no_proxy GkeonpremBareMetalCluster#no_proxy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb4e308b038ed571246d1c5becbeae8270581938cb000c87e50dcb8e4c5564ce)
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

        For example: http://domain
        WARNING: Do not provide credentials in the format
        of http://(username:password@)domain these will be rejected by the server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#uri GkeonpremBareMetalCluster#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def no_proxy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IPs, hostnames, and domains that should skip the proxy. For example ["127.0.0.1", "example.com", ".corp", "localhost"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#no_proxy GkeonpremBareMetalCluster#no_proxy}
        '''
        result = self._values.get("no_proxy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterProxy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterProxyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterProxyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5aae552c56265ea7d37764c1b383605e6eef666dac0f8168fcf03319b17637cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a7165e8bddd14d82e715119fd34f9534ec85dde0c4cc276080eb6be9ca4d337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noProxy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c451eda9e4125c849a88c76191d1bde2acb74bb30d885b75768cc9c47580e751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremBareMetalClusterProxy]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterProxy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterProxy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f97a87ed55d5d0856a2280041e4fe5b802487e6396630397fb3c13c560715f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterSecurityConfig",
    jsii_struct_bases=[],
    name_mapping={"authorization": "authorization"},
)
class GkeonpremBareMetalClusterSecurityConfig:
    def __init__(
        self,
        *,
        authorization: typing.Optional[typing.Union["GkeonpremBareMetalClusterSecurityConfigAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#authorization GkeonpremBareMetalCluster#authorization}
        '''
        if isinstance(authorization, dict):
            authorization = GkeonpremBareMetalClusterSecurityConfigAuthorization(**authorization)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaa8ec79127b2f3e079bf04d8ff7dab83f015ba27c43789dd3dd916384f65e0e)
            check_type(argname="argument authorization", value=authorization, expected_type=type_hints["authorization"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authorization is not None:
            self._values["authorization"] = authorization

    @builtins.property
    def authorization(
        self,
    ) -> typing.Optional["GkeonpremBareMetalClusterSecurityConfigAuthorization"]:
        '''authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#authorization GkeonpremBareMetalCluster#authorization}
        '''
        result = self._values.get("authorization")
        return typing.cast(typing.Optional["GkeonpremBareMetalClusterSecurityConfigAuthorization"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterSecurityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterSecurityConfigAuthorization",
    jsii_struct_bases=[],
    name_mapping={"admin_users": "adminUsers"},
)
class GkeonpremBareMetalClusterSecurityConfigAuthorization:
    def __init__(
        self,
        *,
        admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#admin_users GkeonpremBareMetalCluster#admin_users}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc21d2f85c2aeeec04c703eea36a5a6dbd7f60174261bbe41250cf92295b0708)
            check_type(argname="argument admin_users", value=admin_users, expected_type=type_hints["admin_users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_users": admin_users,
        }

    @builtins.property
    def admin_users(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers"]]:
        '''admin_users block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#admin_users GkeonpremBareMetalCluster#admin_users}
        '''
        result = self._values.get("admin_users")
        assert result is not None, "Required property 'admin_users' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterSecurityConfigAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers",
    jsii_struct_bases=[],
    name_mapping={"username": "username"},
)
class GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers:
    def __init__(self, *, username: builtins.str) -> None:
        '''
        :param username: The name of the user, e.g. 'my-gcp-id@gmail.com'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#username GkeonpremBareMetalCluster#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ee27aeff052ed5876cbee012d798b09affbc3db14ca4a72ffc005d8abf6a1cf)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
        }

    @builtins.property
    def username(self) -> builtins.str:
        '''The name of the user, e.g. 'my-gcp-id@gmail.com'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#username GkeonpremBareMetalCluster#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71f1e43846252a9244aa4308d47bc7d8b82f3115532ff69e62e1ddb3607d034e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a5cb0daefe60cb24d977d717ba4708e72fe321470841d1b7e11a4cfd5b2fee)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d7a4098019dcfc06b340262187c5722726506ebb527b000c4e09e16afd6b5a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67cdb4721fac08d3489ba793c2c0ed496916e309c6b95c2346bda4993f0dbc9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c4ddcef89a27d74a196f3034a1571d5d16e25a5d234e9f3563223fc90ff5acd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fb5de7ceabcc48e2d0d1a72a6e29203244e2d42b44ea4e6f6dbcc76d2d62369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad87968ed032115d8ee7f50ca79505f7dd1a74e6e0b2b379c756f99087d85ba1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__42717ce4373612ba8bb88391adb5fcc6ec998da04366b9faf300ab36a6e78ad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61b47b77a8646fb0da141a15e9522f4c59c42dfeff78476510d9cd47dc758466)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterSecurityConfigAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterSecurityConfigAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92edbb521412634ce71f31a02a54635fae03219a906e361d1b4184a5a3f0ad97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdminUsers")
    def put_admin_users(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b19979566593929325cfc71edeb69175afa4b5ba0594501acd96c766231381b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdminUsers", [value]))

    @builtins.property
    @jsii.member(jsii_name="adminUsers")
    def admin_users(
        self,
    ) -> GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsersList:
        return typing.cast(GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsersList, jsii.get(self, "adminUsers"))

    @builtins.property
    @jsii.member(jsii_name="adminUsersInput")
    def admin_users_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers]]], jsii.get(self, "adminUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterSecurityConfigAuthorization]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterSecurityConfigAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterSecurityConfigAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64b619b40458ef2db11684a91bc9f70cf060111a12b811d95ff5fffe6332c73f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterSecurityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterSecurityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a67d7069bf4810697f75e62d829bda322c3bd8321b49eb8a752a7d063ca5df41)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthorization")
    def put_authorization(
        self,
        *,
        admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#admin_users GkeonpremBareMetalCluster#admin_users}
        '''
        value = GkeonpremBareMetalClusterSecurityConfigAuthorization(
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
    ) -> GkeonpremBareMetalClusterSecurityConfigAuthorizationOutputReference:
        return typing.cast(GkeonpremBareMetalClusterSecurityConfigAuthorizationOutputReference, jsii.get(self, "authorization"))

    @builtins.property
    @jsii.member(jsii_name="authorizationInput")
    def authorization_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterSecurityConfigAuthorization]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterSecurityConfigAuthorization], jsii.get(self, "authorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterSecurityConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterSecurityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterSecurityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__576341916a0d1490628c837c1802e60ed498526f3d10252f79728c8ad2a7056a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremBareMetalClusterStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterStatusConditions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremBareMetalClusterStatusConditions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterStatusConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterStatusConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterStatusConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f92f5c0baf1aac254084ba0c11fa3ceeea946c799f79ca73a3d3f4c6de944342)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalClusterStatusConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0ae3c7c59de45cb57fd207e3ab9b70e1c07ecaa45db21a480233fb9939e93f4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalClusterStatusConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__497c2fbd1d7309ccd3212686efbe2b4b70539b57aaac506afafb37137094b764)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e44e96ce83fb88fb9e5b026a5cd59228e46e22509e6b98b898fe715e15c45478)
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
            type_hints = typing.get_type_hints(_typecheckingstub__881ea6bbcf0343fb4475914797dbde8f43caaa1a2a5b551f814faed541a715b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterStatusConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterStatusConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__827ef58020195e6c08b24bdb45eabc311370d03d010598a38e2e2b592972b301)
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
    ) -> typing.Optional[GkeonpremBareMetalClusterStatusConditions]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterStatusConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterStatusConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df97b004b587d44b94ff4d0cfd339072c17bcf9bb200abd6effa0c3567a1ef8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a72bb346c43d7ac87fb5d8465346f37829a81303830c106ae72476a6baf4aff8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalClusterStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67b5dc054c30e06dadfd83636e5763fe1c9d2c47835c2fe2343297d69d1f35ae)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalClusterStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33c2f8765f69c5eecb4672c9be0d0fcdd3c6fb879baf2e9e13c3f2ba10778e68)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a491170cee8be5163f7286f3c24f567679d0e9fb2cf333caafbbdd43f4883014)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1134a2a19510b53a26e9a845e3de4e8aeeafd5b4e046401bfe5fcbc5b99469e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b673804315f231111f4c45ad99e2732692c87a12e398fdcb25c8524c001b94f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> GkeonpremBareMetalClusterStatusConditionsList:
        return typing.cast(GkeonpremBareMetalClusterStatusConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremBareMetalClusterStatus]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7a2cbcf873bd20ec62e0ce9c926399ab5ed47c6122cf06c1eb0a0ae87d48796)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterStorage",
    jsii_struct_bases=[],
    name_mapping={
        "lvp_node_mounts_config": "lvpNodeMountsConfig",
        "lvp_share_config": "lvpShareConfig",
    },
)
class GkeonpremBareMetalClusterStorage:
    def __init__(
        self,
        *,
        lvp_node_mounts_config: typing.Union["GkeonpremBareMetalClusterStorageLvpNodeMountsConfig", typing.Dict[builtins.str, typing.Any]],
        lvp_share_config: typing.Union["GkeonpremBareMetalClusterStorageLvpShareConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param lvp_node_mounts_config: lvp_node_mounts_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#lvp_node_mounts_config GkeonpremBareMetalCluster#lvp_node_mounts_config}
        :param lvp_share_config: lvp_share_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#lvp_share_config GkeonpremBareMetalCluster#lvp_share_config}
        '''
        if isinstance(lvp_node_mounts_config, dict):
            lvp_node_mounts_config = GkeonpremBareMetalClusterStorageLvpNodeMountsConfig(**lvp_node_mounts_config)
        if isinstance(lvp_share_config, dict):
            lvp_share_config = GkeonpremBareMetalClusterStorageLvpShareConfig(**lvp_share_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76f9f725ed54f80fbf4d2a9a544d1ef9c5e393382c717467c18fde909fdacd54)
            check_type(argname="argument lvp_node_mounts_config", value=lvp_node_mounts_config, expected_type=type_hints["lvp_node_mounts_config"])
            check_type(argname="argument lvp_share_config", value=lvp_share_config, expected_type=type_hints["lvp_share_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lvp_node_mounts_config": lvp_node_mounts_config,
            "lvp_share_config": lvp_share_config,
        }

    @builtins.property
    def lvp_node_mounts_config(
        self,
    ) -> "GkeonpremBareMetalClusterStorageLvpNodeMountsConfig":
        '''lvp_node_mounts_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#lvp_node_mounts_config GkeonpremBareMetalCluster#lvp_node_mounts_config}
        '''
        result = self._values.get("lvp_node_mounts_config")
        assert result is not None, "Required property 'lvp_node_mounts_config' is missing"
        return typing.cast("GkeonpremBareMetalClusterStorageLvpNodeMountsConfig", result)

    @builtins.property
    def lvp_share_config(self) -> "GkeonpremBareMetalClusterStorageLvpShareConfig":
        '''lvp_share_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#lvp_share_config GkeonpremBareMetalCluster#lvp_share_config}
        '''
        result = self._values.get("lvp_share_config")
        assert result is not None, "Required property 'lvp_share_config' is missing"
        return typing.cast("GkeonpremBareMetalClusterStorageLvpShareConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterStorageLvpNodeMountsConfig",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "storage_class": "storageClass"},
)
class GkeonpremBareMetalClusterStorageLvpNodeMountsConfig:
    def __init__(self, *, path: builtins.str, storage_class: builtins.str) -> None:
        '''
        :param path: The host machine path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#path GkeonpremBareMetalCluster#path}
        :param storage_class: The StorageClass name that PVs will be created with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#storage_class GkeonpremBareMetalCluster#storage_class}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f76a8e911934a00023b332986a5873f340d95fcbef05221dffffbf6a55ead24)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "storage_class": storage_class,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''The host machine path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#path GkeonpremBareMetalCluster#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_class(self) -> builtins.str:
        '''The StorageClass name that PVs will be created with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#storage_class GkeonpremBareMetalCluster#storage_class}
        '''
        result = self._values.get("storage_class")
        assert result is not None, "Required property 'storage_class' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterStorageLvpNodeMountsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterStorageLvpNodeMountsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterStorageLvpNodeMountsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ce61c7a78e370f276f9df11d692c64c2e476ec38db7caaa6cc6cc61cb7bfbd5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77f65e987d14d5bde4c3c10ae633b9235768d58ca7a35de89251fb49b3574dd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageClass")
    def storage_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageClass"))

    @storage_class.setter
    def storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b04a8e0bd2da800c4de27b62583a85c0cfc6cb98b3f7d4d6ae639491102e5f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterStorageLvpNodeMountsConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterStorageLvpNodeMountsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterStorageLvpNodeMountsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7a2bd68f2d844c16a61bd009115b8fb86bc726cc3ab37915cf60973f0a523b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterStorageLvpShareConfig",
    jsii_struct_bases=[],
    name_mapping={
        "lvp_config": "lvpConfig",
        "shared_path_pv_count": "sharedPathPvCount",
    },
)
class GkeonpremBareMetalClusterStorageLvpShareConfig:
    def __init__(
        self,
        *,
        lvp_config: typing.Union["GkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig", typing.Dict[builtins.str, typing.Any]],
        shared_path_pv_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param lvp_config: lvp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#lvp_config GkeonpremBareMetalCluster#lvp_config}
        :param shared_path_pv_count: The number of subdirectories to create under path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#shared_path_pv_count GkeonpremBareMetalCluster#shared_path_pv_count}
        '''
        if isinstance(lvp_config, dict):
            lvp_config = GkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig(**lvp_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1814ac8bac5e7f38bdb6ff1c09e58b839d79c9a55d7557beeebee48477e9204e)
            check_type(argname="argument lvp_config", value=lvp_config, expected_type=type_hints["lvp_config"])
            check_type(argname="argument shared_path_pv_count", value=shared_path_pv_count, expected_type=type_hints["shared_path_pv_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lvp_config": lvp_config,
        }
        if shared_path_pv_count is not None:
            self._values["shared_path_pv_count"] = shared_path_pv_count

    @builtins.property
    def lvp_config(self) -> "GkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig":
        '''lvp_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#lvp_config GkeonpremBareMetalCluster#lvp_config}
        '''
        result = self._values.get("lvp_config")
        assert result is not None, "Required property 'lvp_config' is missing"
        return typing.cast("GkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig", result)

    @builtins.property
    def shared_path_pv_count(self) -> typing.Optional[jsii.Number]:
        '''The number of subdirectories to create under path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#shared_path_pv_count GkeonpremBareMetalCluster#shared_path_pv_count}
        '''
        result = self._values.get("shared_path_pv_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterStorageLvpShareConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "storage_class": "storageClass"},
)
class GkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig:
    def __init__(self, *, path: builtins.str, storage_class: builtins.str) -> None:
        '''
        :param path: The host machine path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#path GkeonpremBareMetalCluster#path}
        :param storage_class: The StorageClass name that PVs will be created with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#storage_class GkeonpremBareMetalCluster#storage_class}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb7d58022569387950c09f5fb638dc047ebdc59be9e180840a73279435295f1a)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "storage_class": storage_class,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''The host machine path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#path GkeonpremBareMetalCluster#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_class(self) -> builtins.str:
        '''The StorageClass name that PVs will be created with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#storage_class GkeonpremBareMetalCluster#storage_class}
        '''
        result = self._values.get("storage_class")
        assert result is not None, "Required property 'storage_class' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterStorageLvpShareConfigLvpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterStorageLvpShareConfigLvpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b91bfd22bfc4f9c2abde48a2a4a1cb878a9723eb72c51ba4136a179a9c217853)
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
            type_hints = typing.get_type_hints(_typecheckingstub__08e9b127b3f28947f5f11279a6f9f8535758e083e53b8e4745b7f177cd9627f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageClass")
    def storage_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageClass"))

    @storage_class.setter
    def storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ffe53bf53e32137d32496f1ba6030606f32330430961fa7122e97e2998503ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5039b4ddf5dae80052f5e2d350ff963dc6b378bf7d9c034aa2672af1bb694ca5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterStorageLvpShareConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterStorageLvpShareConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f264bbd6b7cf0edd44e03458086232d292b172a87c18ba87ea539c9820996c2)
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
        :param path: The host machine path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#path GkeonpremBareMetalCluster#path}
        :param storage_class: The StorageClass name that PVs will be created with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#storage_class GkeonpremBareMetalCluster#storage_class}
        '''
        value = GkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig(
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
    ) -> GkeonpremBareMetalClusterStorageLvpShareConfigLvpConfigOutputReference:
        return typing.cast(GkeonpremBareMetalClusterStorageLvpShareConfigLvpConfigOutputReference, jsii.get(self, "lvpConfig"))

    @builtins.property
    @jsii.member(jsii_name="lvpConfigInput")
    def lvp_config_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig], jsii.get(self, "lvpConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c94ed27f7a9921b18d20c715ef906eda5bea6785157b1cc3b18595d3803c4e98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedPathPvCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterStorageLvpShareConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterStorageLvpShareConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterStorageLvpShareConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33a8641ef055fa955de36362f8bff90383d45d6ec207f99a1d823ab0e19c5af6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterStorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterStorageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65c4ffb0e55028a3af48b91741765a2dac60e5ea63a8f47d73346d72f588c43f)
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
        :param path: The host machine path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#path GkeonpremBareMetalCluster#path}
        :param storage_class: The StorageClass name that PVs will be created with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#storage_class GkeonpremBareMetalCluster#storage_class}
        '''
        value = GkeonpremBareMetalClusterStorageLvpNodeMountsConfig(
            path=path, storage_class=storage_class
        )

        return typing.cast(None, jsii.invoke(self, "putLvpNodeMountsConfig", [value]))

    @jsii.member(jsii_name="putLvpShareConfig")
    def put_lvp_share_config(
        self,
        *,
        lvp_config: typing.Union[GkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig, typing.Dict[builtins.str, typing.Any]],
        shared_path_pv_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param lvp_config: lvp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#lvp_config GkeonpremBareMetalCluster#lvp_config}
        :param shared_path_pv_count: The number of subdirectories to create under path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#shared_path_pv_count GkeonpremBareMetalCluster#shared_path_pv_count}
        '''
        value = GkeonpremBareMetalClusterStorageLvpShareConfig(
            lvp_config=lvp_config, shared_path_pv_count=shared_path_pv_count
        )

        return typing.cast(None, jsii.invoke(self, "putLvpShareConfig", [value]))

    @builtins.property
    @jsii.member(jsii_name="lvpNodeMountsConfig")
    def lvp_node_mounts_config(
        self,
    ) -> GkeonpremBareMetalClusterStorageLvpNodeMountsConfigOutputReference:
        return typing.cast(GkeonpremBareMetalClusterStorageLvpNodeMountsConfigOutputReference, jsii.get(self, "lvpNodeMountsConfig"))

    @builtins.property
    @jsii.member(jsii_name="lvpShareConfig")
    def lvp_share_config(
        self,
    ) -> GkeonpremBareMetalClusterStorageLvpShareConfigOutputReference:
        return typing.cast(GkeonpremBareMetalClusterStorageLvpShareConfigOutputReference, jsii.get(self, "lvpShareConfig"))

    @builtins.property
    @jsii.member(jsii_name="lvpNodeMountsConfigInput")
    def lvp_node_mounts_config_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterStorageLvpNodeMountsConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterStorageLvpNodeMountsConfig], jsii.get(self, "lvpNodeMountsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="lvpShareConfigInput")
    def lvp_share_config_input(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterStorageLvpShareConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterStorageLvpShareConfig], jsii.get(self, "lvpShareConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremBareMetalClusterStorage]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterStorage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterStorage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d1cc6f6021cff98de960ded61339b15af92e01e7a0d07bb6fc4efbb7c1df69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GkeonpremBareMetalClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#create GkeonpremBareMetalCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#delete GkeonpremBareMetalCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#update GkeonpremBareMetalCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dddc46f8e09db9c26861399c2985c3a8041417bc2cd6b31adf415d6443dbc051)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#create GkeonpremBareMetalCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#delete GkeonpremBareMetalCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#update GkeonpremBareMetalCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30e629c97a2f6660c367265e9c975b0fd1d5d9c886690b6f6e08cb3131660890)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c31941651a3d941c78246bb480b5e751848a8b8c3c9d94bae6e36912db12a46e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd290d97a04c00ce3b7dfa794d68e748ca41fce070c218e04b4db244db8b799e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fdb14bc9c7e3f9014a6e98d8af32053ce1c9c37f9cc33333a00d4944e14f38a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5337f6346c0e2ea82bbfec6c791dc1e220a51e05ad12143cc0616ac29d57670)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterUpgradePolicy",
    jsii_struct_bases=[],
    name_mapping={"policy": "policy"},
)
class GkeonpremBareMetalClusterUpgradePolicy:
    def __init__(self, *, policy: typing.Optional[builtins.str] = None) -> None:
        '''
        :param policy: Specifies which upgrade policy to use. Possible values: ["SERIAL", "CONCURRENT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#policy GkeonpremBareMetalCluster#policy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7028f6a470bd951cd2dc4ce5fe3232c58fec3249ad412a7348b0c867cbde7cd)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy is not None:
            self._values["policy"] = policy

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''Specifies which upgrade policy to use. Possible values: ["SERIAL", "CONCURRENT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_cluster#policy GkeonpremBareMetalCluster#policy}
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterUpgradePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterUpgradePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterUpgradePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c86e99fbd4d91cadb1a5389f92c7c24d3617beb63499e580d5d4147d5ba37c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPolicy")
    def reset_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="policyInput")
    def policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyInput"))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3733fc5bb8ab089b9b61f2b5dd1a9b0648ab28b2733b13ec2acc30d325ece3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremBareMetalClusterUpgradePolicy]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterUpgradePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterUpgradePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de064e6289cf817d904000664b2e3f337cff31394f075552e8a021b69b2287a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterValidationCheck",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremBareMetalClusterValidationCheck:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterValidationCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterValidationCheckList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterValidationCheckList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ba500b0d68c7aacff6504be3ebfd747dcdbaab5db85e125c0ee39fd989020bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalClusterValidationCheckOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c494fa68e3fc63dc91c7cab7777bd121c597123b3596eb1c9c207e94648934de)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalClusterValidationCheckOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73a5a3c905c0f2a60f346d885cbc909b6673bee7e95cd2b6a2bb289002caf48e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2439ea329baa36748b005e37ea588822003836c7f674bcc04e3f608a6be68561)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8b11566b88236c9ef872ae2173adfd498941eaa1c013cffc313ae70ea3041a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterValidationCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterValidationCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1373d815a0d139c0d73add92a3dffd03e041a832992a376a79eed944d0a0e078)
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
    def status(self) -> "GkeonpremBareMetalClusterValidationCheckStatusList":
        return typing.cast("GkeonpremBareMetalClusterValidationCheckStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterValidationCheck]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterValidationCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterValidationCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d38958394e446d9f93f8679b28445431cd173e42b0dad79ab318e2378b98c75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterValidationCheckStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremBareMetalClusterValidationCheckStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterValidationCheckStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterValidationCheckStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterValidationCheckStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5d63804193095134b9ee255058a9f40e96bc55d4e2b8279ea5b9d4179a4b17c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalClusterValidationCheckStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a36008820096069aaf27b0987dddb1c0dd36145c53c3382c62a6667039c80a00)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalClusterValidationCheckStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e234e12911857b15313085fdabb8bb85c61674f97aa907c1dab9a54e0da076d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66d0744c7cbec7d1e95591d2f8b4914ce3cca5faa37af8fc68ec805a84bb115c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a51ebcd54305786c2e4a00c07b60d02d7350100099b7e6b3c9ed643d2a6430b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterValidationCheckStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterValidationCheckStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__967bc0c19fe21d7d6da805f4f917e42add6ce4eb126f4c94e983bb04ab204ca8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="result")
    def result(self) -> "GkeonpremBareMetalClusterValidationCheckStatusResultList":
        return typing.cast("GkeonpremBareMetalClusterValidationCheckStatusResultList", jsii.get(self, "result"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalClusterValidationCheckStatus]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterValidationCheckStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterValidationCheckStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b293f7c39a13a4b30fa3d96fe3871e258a4f6e96308b0f1ecbce2a56aa1599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterValidationCheckStatusResult",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremBareMetalClusterValidationCheckStatusResult:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalClusterValidationCheckStatusResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalClusterValidationCheckStatusResultList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterValidationCheckStatusResultList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a4efd72427d39a9d5b38ed7f95863a3fcbddec036c9f5a5af22ef54608e0d64)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalClusterValidationCheckStatusResultOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6f797dac7ccf596b64370337dcf476f6ef998ee5bfb992a4d817425c9f91861)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalClusterValidationCheckStatusResultOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9bd63f182fcf49fdc93183b68298ca3539b606a66f85c2ebe226a706b759436)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29701cfe89caf03b9c911865cc55324bd5e7942c0e68b44a8786bf9ed4762755)
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
            type_hints = typing.get_type_hints(_typecheckingstub__838974888ac3144c8d98619ec7210ee0b05d69d3806e65479a5b43c204c89bbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalClusterValidationCheckStatusResultOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalCluster.GkeonpremBareMetalClusterValidationCheckStatusResultOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__099fba7a4ac17123510e7ae8676be8716b6715722a8e5496fb6d134e85eba820)
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
    ) -> typing.Optional[GkeonpremBareMetalClusterValidationCheckStatusResult]:
        return typing.cast(typing.Optional[GkeonpremBareMetalClusterValidationCheckStatusResult], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalClusterValidationCheckStatusResult],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a1ced248061329020e34a0cef8579b178dcab9c61aff80f1fc398ea9d73468c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GkeonpremBareMetalCluster",
    "GkeonpremBareMetalClusterBinaryAuthorization",
    "GkeonpremBareMetalClusterBinaryAuthorizationOutputReference",
    "GkeonpremBareMetalClusterClusterOperations",
    "GkeonpremBareMetalClusterClusterOperationsOutputReference",
    "GkeonpremBareMetalClusterConfig",
    "GkeonpremBareMetalClusterControlPlane",
    "GkeonpremBareMetalClusterControlPlaneApiServerArgs",
    "GkeonpremBareMetalClusterControlPlaneApiServerArgsList",
    "GkeonpremBareMetalClusterControlPlaneApiServerArgsOutputReference",
    "GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig",
    "GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig",
    "GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs",
    "GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsList",
    "GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsOutputReference",
    "GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigOutputReference",
    "GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints",
    "GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsList",
    "GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsOutputReference",
    "GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigOutputReference",
    "GkeonpremBareMetalClusterControlPlaneOutputReference",
    "GkeonpremBareMetalClusterFleet",
    "GkeonpremBareMetalClusterFleetList",
    "GkeonpremBareMetalClusterFleetOutputReference",
    "GkeonpremBareMetalClusterLoadBalancer",
    "GkeonpremBareMetalClusterLoadBalancerBgpLbConfig",
    "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools",
    "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPoolsList",
    "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPoolsOutputReference",
    "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs",
    "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigsList",
    "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigsOutputReference",
    "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig",
    "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig",
    "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig",
    "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfigOutputReference",
    "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs",
    "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsList",
    "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsOutputReference",
    "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigOutputReference",
    "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints",
    "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsList",
    "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsOutputReference",
    "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigOutputReference",
    "GkeonpremBareMetalClusterLoadBalancerBgpLbConfigOutputReference",
    "GkeonpremBareMetalClusterLoadBalancerManualLbConfig",
    "GkeonpremBareMetalClusterLoadBalancerManualLbConfigOutputReference",
    "GkeonpremBareMetalClusterLoadBalancerMetalLbConfig",
    "GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools",
    "GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPoolsList",
    "GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPoolsOutputReference",
    "GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig",
    "GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig",
    "GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs",
    "GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsList",
    "GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsOutputReference",
    "GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigOutputReference",
    "GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints",
    "GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsList",
    "GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsOutputReference",
    "GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigOutputReference",
    "GkeonpremBareMetalClusterLoadBalancerMetalLbConfigOutputReference",
    "GkeonpremBareMetalClusterLoadBalancerOutputReference",
    "GkeonpremBareMetalClusterLoadBalancerPortConfig",
    "GkeonpremBareMetalClusterLoadBalancerPortConfigOutputReference",
    "GkeonpremBareMetalClusterLoadBalancerVipConfig",
    "GkeonpremBareMetalClusterLoadBalancerVipConfigOutputReference",
    "GkeonpremBareMetalClusterMaintenanceConfig",
    "GkeonpremBareMetalClusterMaintenanceConfigOutputReference",
    "GkeonpremBareMetalClusterNetworkConfig",
    "GkeonpremBareMetalClusterNetworkConfigIslandModeCidr",
    "GkeonpremBareMetalClusterNetworkConfigIslandModeCidrOutputReference",
    "GkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig",
    "GkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfigOutputReference",
    "GkeonpremBareMetalClusterNetworkConfigOutputReference",
    "GkeonpremBareMetalClusterNetworkConfigSrIovConfig",
    "GkeonpremBareMetalClusterNetworkConfigSrIovConfigOutputReference",
    "GkeonpremBareMetalClusterNodeAccessConfig",
    "GkeonpremBareMetalClusterNodeAccessConfigOutputReference",
    "GkeonpremBareMetalClusterNodeConfig",
    "GkeonpremBareMetalClusterNodeConfigOutputReference",
    "GkeonpremBareMetalClusterOsEnvironmentConfig",
    "GkeonpremBareMetalClusterOsEnvironmentConfigOutputReference",
    "GkeonpremBareMetalClusterProxy",
    "GkeonpremBareMetalClusterProxyOutputReference",
    "GkeonpremBareMetalClusterSecurityConfig",
    "GkeonpremBareMetalClusterSecurityConfigAuthorization",
    "GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers",
    "GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsersList",
    "GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsersOutputReference",
    "GkeonpremBareMetalClusterSecurityConfigAuthorizationOutputReference",
    "GkeonpremBareMetalClusterSecurityConfigOutputReference",
    "GkeonpremBareMetalClusterStatus",
    "GkeonpremBareMetalClusterStatusConditions",
    "GkeonpremBareMetalClusterStatusConditionsList",
    "GkeonpremBareMetalClusterStatusConditionsOutputReference",
    "GkeonpremBareMetalClusterStatusList",
    "GkeonpremBareMetalClusterStatusOutputReference",
    "GkeonpremBareMetalClusterStorage",
    "GkeonpremBareMetalClusterStorageLvpNodeMountsConfig",
    "GkeonpremBareMetalClusterStorageLvpNodeMountsConfigOutputReference",
    "GkeonpremBareMetalClusterStorageLvpShareConfig",
    "GkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig",
    "GkeonpremBareMetalClusterStorageLvpShareConfigLvpConfigOutputReference",
    "GkeonpremBareMetalClusterStorageLvpShareConfigOutputReference",
    "GkeonpremBareMetalClusterStorageOutputReference",
    "GkeonpremBareMetalClusterTimeouts",
    "GkeonpremBareMetalClusterTimeoutsOutputReference",
    "GkeonpremBareMetalClusterUpgradePolicy",
    "GkeonpremBareMetalClusterUpgradePolicyOutputReference",
    "GkeonpremBareMetalClusterValidationCheck",
    "GkeonpremBareMetalClusterValidationCheckList",
    "GkeonpremBareMetalClusterValidationCheckOutputReference",
    "GkeonpremBareMetalClusterValidationCheckStatus",
    "GkeonpremBareMetalClusterValidationCheckStatusList",
    "GkeonpremBareMetalClusterValidationCheckStatusOutputReference",
    "GkeonpremBareMetalClusterValidationCheckStatusResult",
    "GkeonpremBareMetalClusterValidationCheckStatusResultList",
    "GkeonpremBareMetalClusterValidationCheckStatusResultOutputReference",
]

publication.publish()

def _typecheckingstub__7067342f098b2fa59dfe3a7ef7dc191c9fb14cc5ccd17bb35745d653e72234a1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    admin_cluster_membership: builtins.str,
    bare_metal_version: builtins.str,
    control_plane: typing.Union[GkeonpremBareMetalClusterControlPlane, typing.Dict[builtins.str, typing.Any]],
    load_balancer: typing.Union[GkeonpremBareMetalClusterLoadBalancer, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    network_config: typing.Union[GkeonpremBareMetalClusterNetworkConfig, typing.Dict[builtins.str, typing.Any]],
    storage: typing.Union[GkeonpremBareMetalClusterStorage, typing.Dict[builtins.str, typing.Any]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    binary_authorization: typing.Optional[typing.Union[GkeonpremBareMetalClusterBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_operations: typing.Optional[typing.Union[GkeonpremBareMetalClusterClusterOperations, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    maintenance_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterMaintenanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_access_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterNodeAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    os_environment_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterOsEnvironmentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    proxy: typing.Optional[typing.Union[GkeonpremBareMetalClusterProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    security_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterSecurityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GkeonpremBareMetalClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    upgrade_policy: typing.Optional[typing.Union[GkeonpremBareMetalClusterUpgradePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4b799e8213ff8c89487f48080780f302be26720104fede372e389442b8cdc761(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c39ae4ac474d27ffa0371c41aa2a327a1cca99c03371af56ad9d822bc3757fcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98175ac62cd809bb9a0b5b9695370c7596083ae37eef4196e8477732f9fe6d23(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f90d733df01aa4685a2907a8ff2ea19a735a4834c2ef7c06375b58601de68934(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9175a4bf3165a2161bbd624d6d4e818b297a171a03a64a40ddda72e2e463c61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bfaf1d2861a170c8e896be57e2496dd37a5f1f997f61586020632c8913da014(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a4844b7c8e584bd0ee384199e0660ba6ca628ca306e0764093bf06b30447f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15505bfbf5bcad7835b3d0d78b7e22966624e5a67c3100864286dfbc0ef81d4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b034d1c7fccccc85a682725b60a603a1141ebf4848d89d6ee86d33e27f5ee02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00e634687f672871c9f4500f38b0f6628d553c14798da81869d7efc3907405ae(
    *,
    evaluation_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__455a86462162ea5289cbbc96c7ea7b35347426b3da946ed9b98bd1ba230c9398(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eab41abc6904554fbe61bc630e78a88293583a62111620604f89083461877473(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__110f5c35cd2596cc68ccbdcb70ea501dee76f04c9e67d56ba33282afffc8ff68(
    value: typing.Optional[GkeonpremBareMetalClusterBinaryAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27f6b319b9bf532677fd1cf76993e6ebd68b57118ed8ece2d5511f40517feb4a(
    *,
    enable_application_logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf338c6102ffa7fc2cdb61f3d36e9ee33f9851c7497b36134cb095b9561615d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31e2f6a513c591aa43547c328f2365cb7151bade111d8fb0780693c6b3b2a097(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8671d4b5239e73b9b3b8154fad8302934c944f782afccc1494831d90ddb57833(
    value: typing.Optional[GkeonpremBareMetalClusterClusterOperations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdc7624c94fd6869aa0f3346bf6d292584fffdef72bc5e0cc82e62ce370a0da4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    admin_cluster_membership: builtins.str,
    bare_metal_version: builtins.str,
    control_plane: typing.Union[GkeonpremBareMetalClusterControlPlane, typing.Dict[builtins.str, typing.Any]],
    load_balancer: typing.Union[GkeonpremBareMetalClusterLoadBalancer, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    network_config: typing.Union[GkeonpremBareMetalClusterNetworkConfig, typing.Dict[builtins.str, typing.Any]],
    storage: typing.Union[GkeonpremBareMetalClusterStorage, typing.Dict[builtins.str, typing.Any]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    binary_authorization: typing.Optional[typing.Union[GkeonpremBareMetalClusterBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_operations: typing.Optional[typing.Union[GkeonpremBareMetalClusterClusterOperations, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    maintenance_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterMaintenanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_access_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterNodeAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    os_environment_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterOsEnvironmentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    proxy: typing.Optional[typing.Union[GkeonpremBareMetalClusterProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    security_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterSecurityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GkeonpremBareMetalClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    upgrade_policy: typing.Optional[typing.Union[GkeonpremBareMetalClusterUpgradePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eaaa5c906a290f1d786453ca271072a21e23bc29a3eb5b70832f739fdc35dc3(
    *,
    control_plane_node_pool_config: typing.Union[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig, typing.Dict[builtins.str, typing.Any]],
    api_server_args: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterControlPlaneApiServerArgs, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b82718ab650f538aedbff3b24071e95c221113a2eaf8b228af28ed7f607abf13(
    *,
    argument: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f92df5a2362a862a1c9317b4238758a1276e45a71839bdb921f6eb05d328bb5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__531246a4004466e8de2533b785c471c732b0e8bbbae15c2469ad587822297b78(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f016bbabfaefaf31060ebd3987f1e68c5ef133f4028cdaabcc6ca5b891579b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4363f77e7e3a79ab450155b897be46dc66658d8984f02a23aa74b2bac0064ed0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__693827ff86652a33f3a95bb95f3a08ec21c4ebed22971447955fc0603fff1b75(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__333d77096de00320b87e4bb4bdd8475498990ce282cf95c1becf60e756086635(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterControlPlaneApiServerArgs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb63686a0523889c9fe3c3f44b2cfcf03b65f1296421b3592ccfe156a3203ed8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da33ac818d704401646091b68eb53d3751e09b405ab505a91e9dcbeb20d5bac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e8ee33da4728a8cae0733bb51ebee238bf5a165fcfe1bd1ebf0b692cfb4e26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e3f4e20aa893610eed7a17f3e6ea16f2486a18478774703cabca28ba5e17a7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterControlPlaneApiServerArgs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3fce94bd2de88af7b9ea278dfb9acbd49b81b1b7d9179d4b2a72bb9c4152c9f(
    *,
    node_pool_config: typing.Union[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cd0f9fa3826d14eb55993f837085a59506d386622c5505cf796e522bc41f839(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    operating_system: typing.Optional[builtins.str] = None,
    taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552d1190d1054d5bbde3fd0c502cc286b917498f5d9ca8d254e8f62478d8f0b8(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac8a27360a0683719bc8103d4ba55ce4378e0c484fd9c60513371e26cd00a3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf5bb09229b1dce4da130543535c2beb100142b78d7e290b9cf0fad949565f7e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__953a525e85b90d619ea7af49da83d5b5ad5eaee6c814fbdc2870fd04e67e59db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a198cfa649ab62f7c48b4ab61676e12c47cdc4cf8c3cbc522f058f157960269(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d116cd012ddb024ad730f424bb39803692d1a51c4fb60c40ecd8a3cde376af7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c578de02edf756390c7a44ba35fd2a2cfbe5c059101ba647b06e366534223aa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__120fec270da460f1e24311ef53be7bc823ad3563477c0808b6aebe944964d520(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b201e4a7363d9d1b7705dcba5b2acfc3d189393985bc75a6f780d8fd6de2a62(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3019e45b9e711a877f722decd7d3059eca67bbb084bef646afad3ad67c7ae4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05fb5115e04301a1eb54ca7e4a979a4591b2e702ffd94b489a94002634a276d6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f7dc95475033e6ed7768b0e4107acbbae422af41e63b199fe10e9d35faeddbb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645c977aae16659111c75567b2773d84c3bb15897ceb16e6eee6133e9e95ef2b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb98c7510dbfb519b1b588d0c154f5cb6873eade0735edb21e059858d8bbde9a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da6abbef4dd2faba39321abbdfdad023de31291d1bc09102edcfb296654e6a6d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2421939812a540759e1b20c8b81dbe1a55e2b79daef1d8c485db3694bb43666c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5804d9887e3435d0af9bd4f6b23835cc343d460a712082fde7521546aafb54fd(
    value: typing.Optional[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__115171690762f0e3a6ed020f7626ad7b684214f2a9439cc2a3e452d0ffa05df7(
    *,
    effect: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__057feb378f6d5c0a99f7817199a968a0fd987e6d8bf18c0cf945ed059aafc604(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be91595cd7db01e0e813caf97e07977fc25f18e00e4cd75344c3fb91973b36d1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe986f9270f0f44e51165287c7f9f35965610916bf6e0c434ae360c7a907c1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1aaa0903d50ffe4ff47837475c2778bb223f2d48284e96b26d68e61f72f9287(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb8ba94cd72b67fed189ac6e093e598711d47ae5cf8bda55c100c244bcadaf67(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e7f820a9818a7abee83a762f961eaafdb6f8bb46170ffcf48692bef4a664a1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3692adcdb308f673b2df7ae29b52b3478658b837a28be725be924a42206b77b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c112d57514bc1073f0cfc1ba21beccf22ef438f766dcac446ca7a946d7878a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__173a7a10c43caa311fd9100e60278bed28af92c2db5e3a24f834ee576a1831dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd3d19971551239630d999f086a8df2019478db09bad72ea5f8fcc00aef6c1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7599819daed4d1788be79275a133bfc917bb1efb0bdd7409e350a65b791ed936(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__258e5d6121db5e4a27ca6b5182e4fba272dcfabcf9611da2a05c2727e91d5f08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83b5a1cffb9448d54266352eb29b0c58a2dbb3fe37ff6401c7b473f96519251(
    value: typing.Optional[GkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__330dac634063240a28bd60776c272c804213e89d65d816f5134632691685beb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b939a4b9b1907716717bdaaa36fb48a0ac91a8504ceea817cb1f528f618db77(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterControlPlaneApiServerArgs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3eff0e54786a58aa37ca142cf5b2bbb59511a98cbad1ef923355e880244bb8(
    value: typing.Optional[GkeonpremBareMetalClusterControlPlane],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dad12c10fb23f08389a2dab84f81f0739803cf47c3b4dddb17eaae7a7184f6ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce28a1d21a0e05f3f590a35c7659f65580a894129fc5a5df0e8ff14847a3cb2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f426e6ab0a279a0f6aa7c6a55555ed876aa1d27a996afaf321f2d9976fc836e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab7f9e78d70c462f1f3246b699a3e96b1ee219d9c3ddf39874ec2e3e85c4642(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef73bd3f381053839cd15a87c0edb55bea33419c42f4c599ccee064942932a82(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dae14a0e309b4772a8a61e8b2caf04e010750f467a9ff4441454017cbd98f6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e9349279b9c317c8af860d24c91353fba6d19d137f39f83f8ee7876f059b2a7(
    value: typing.Optional[GkeonpremBareMetalClusterFleet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbba1e8b32379e0001383bd17f63a5c2b03287e586c2b8f38625254964386d26(
    *,
    port_config: typing.Union[GkeonpremBareMetalClusterLoadBalancerPortConfig, typing.Dict[builtins.str, typing.Any]],
    vip_config: typing.Union[GkeonpremBareMetalClusterLoadBalancerVipConfig, typing.Dict[builtins.str, typing.Any]],
    bgp_lb_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterLoadBalancerBgpLbConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    manual_lb_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterLoadBalancerManualLbConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    metal_lb_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterLoadBalancerMetalLbConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a79ec60a50df9ec9a8ad9baa09b70e9c73b6c852b3c392100789adbb8733029(
    *,
    address_pools: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
    asn: jsii.Number,
    bgp_peer_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs, typing.Dict[builtins.str, typing.Any]]]],
    load_balancer_node_pool_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__391f9512743e6f8bb5e06db2487cfffd7fe19c8244863492da28bbd6081691da(
    *,
    addresses: typing.Sequence[builtins.str],
    pool: builtins.str,
    avoid_buggy_ips: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    manual_assign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c428ac965fca760652066b85ae15aa905e279f5f9a70db9a7ed3a186c2a76525(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c6b4450d6f9c6fc9a5cc9341bfab530195f0c246b1fe0684fd3848dd5fe8e8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b79d8f157a0e84c83529b38623e12d3b6ffa47527c9f7d6be81168ced7624cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a68aaec309bed22cde9b6393ae9e5dabd6771c97e2ec6beb37d19ddbb9a1994(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26dc9863bcfb9ceb107b1e1891b95626a915d77a34dc7243f58065016d901dba(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a33b8c232827798df71e6761e8d3dc7f55be3f332704514eb723e3de911dff40(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c36bb3e1d1529487bc05b238297a21e51ef54ade9843ac6fc444d75eee0af7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ccfd3ee6e0507af5a9b4845d0b13a423e3dab5dc154567f60f34d1027b279f0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39094360536596e068f30c5d70151901add36cd286ae9e5ce720b8198d2ed54(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae37be4c320f997cbbbd83560c59d7673b8f3645607b02d6cb3b61a0b8e9b368(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4b25366bd8d4036d9180698b6e555ac3c3b537226d8cb20fa74aedc57fdefa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e3005f473ddd47804f10cbc82b6d2d89ef3632e97f39a4f4d708ab52b56dd7d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1901dbd3f98933c6d29f4f8fda3638e168eede552a581654326f90a8f3b5cfc8(
    *,
    asn: jsii.Number,
    ip_address: builtins.str,
    control_plane_nodes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce562b36d3ed3533c3704189a2ab573bb5a95a4f822f40c848f022a232e75c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04eca7ad56ed500f41fdb60dda3ed99f0e641b5a6c33427dffad583a870e9290(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38239acb7f798f7e9355e4eb46bd064a7f08c167fed5fe78e053be16c0b36a2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5d2d444914b6b214f5de53f72abcbcff25bca734a80712c4748f0f819213b9c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c30dc9280aef71de321a299af9d7cbcbf65aa9312bd409afef6d0c1d84a0ac2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828b9c5344a61081e0cbbe4a654500356b54d9cfdfc35d1a37c9754153027c28(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70914022b6ddf80690a6b0a8fee2cc7da2cddf23666dc3daa53fd5f0477b2b39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c024f7de722ee6413c0b4480e0533dcbdbb8705a59dc8e66682c823fcd65b1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7ee2459eec54c43e5d157d0ec0836ccecf8b7a7e74a6cb07aed16252f3d3c4b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a4f880da4c34d34db7c4f83041469c86ee28ad212c8288faa8034b16416cfe9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d3dd6f1c0d9e87f4759c344da027feee6d89bcff8b0b6cfc67791958fa547e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f1564f80139fc932f790981b4455db0cdc96e005d62913488bf48b3363d45f(
    *,
    node_pool_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23caf1a0e1d5bbbfc83665eb114f3fe9b28d5bf29c0f3ee73f2263effad6ae13(
    *,
    kubelet_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    operating_system: typing.Optional[builtins.str] = None,
    taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37ec516c494a0e9bf6f091fe7c5cd2dc932462b9ca7c7cbeb4d1fef075e03af4(
    *,
    registry_burst: typing.Optional[jsii.Number] = None,
    registry_pull_qps: typing.Optional[jsii.Number] = None,
    serialize_image_pulls_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f51ca1d5b50b5d7bc0e559707913146a7e79043a424e3b6220aa064fed0f5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eada670194f994e26665a389170c4330f30d7f8a9ef844184b9a2c4d5137ac24(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__663c927522de7d8e1780e625293bd09497c0ea36142396ce15675ea580b14b82(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed7e77d0de27a2c74b25bd782e6022cec97cc43534b86c8e0ce8b6f01de7613c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40b71335308738a61e1b9da312ce6120cf5e78b848b9da296d9a35ee77f09791(
    value: typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2d45773caded0c477a91f0e02c82c3da9e35823d3e2968beb5078b6a4f0429(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dc8f3546e756664c31efd3acd2faf734feb1926b89e74f94d2835eaccd8ce7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__187c941085541ab2bdcf682e9c4b83d4075b8c60325ba5d9eb5b92cb3d312f41(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__007c05a742150c4efaae51cdce020dab55f79857c80232530dcc9ec78fc93cb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d8119b14f0214446381bab1b35d47cac87d088027491249fa551b9d5a89b9fa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eae1f4aba28d5e5da10ad6340e4ba4fdd1ae4be31617d3a04ae6ad9e208b3516(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28cfa1dd7bcf6dde68e98f47a732bdd127d8702f1808a504d59f5294ffda9bac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11c854c47caeab538af218098420fc3564bdcc444cd3be8cc0a8d7eb5affbc10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73ab926a050be8cb74f6586718ddba8000e016b75589b800095d4436beb69bdf(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8467b82a158f9bbd36edab667b3d5a228dd681544f16d4ac7efbe007fa4c4ff3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b035f35664df0486481228aadcb4d3b54d78565fba19369a3cc84798cdbe632(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88cd344151baa28c4dcbaff13027df1aabdfe5775b1e95bfdfd2fdb0dc25dae4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be99e2cdf503d07a772951c8a03697407d3532825949d5dcda592892448a8d14(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a4f50940bb07a6e9602ee54f1f9d14e4152cf52c4c1d96d41043137c0ebc55(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98fe4ae45a067a99d51c79f6c619ff60bf6dc68a0a6fe0170b7908a1b021fe7a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6310e497038c746da3603efb0ddee8370e62cf7c919b3317b22409d460e0124a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3322a9b68e0a31f8edd61416ee103b8675956fe9c655123d4395eea54cf3a57(
    value: typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdb5fc700549a4ed85ad92f06dd402ad5752d13a8ba630c01be461121f2919ee(
    *,
    effect: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58f151e2e772b827f7eede4087479f47365e744c5d46de2fda8a68b640e0ca5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cee14f25d4a960fc4aaaa753267d136ec5efbe3c0f21a632267860192d6d1dcf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eff3491bdbed3fe46f3069ca8010a96160663d5eddcebe8b347ce79713b00a96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__521537c4c70fd2316d8a2bbe4c22bd0dfa42899e1ef7abeae7254a749a4d3ad4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f54abfc3df237b03003aa34b33d959bc866dd0c01b03b785d7939a74f47e84e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d276ba8f30fc1fae7a13116f2ae218ae5e54417daa0a6b0243fc436fa740e2dc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1045665c2e123ac8df1e24b4d9615a97d64e027ef2dd70b8a59e27b877cf8700(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f2c209fc7c9910dcf8d9ca48dcd9dbc23c002bea3550b04b6acbe7803ea7e0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43c224519178a9223a3df276d19555fd53a30d9733b9a881a8d1adef9f691d21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddc1eb0efe3ad6cd90d14edd4f41ea94ee75fd909422092bbbf17162df2d53dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa4854a02c67a527eafd4d0d2ab9580d6ab6b07752f90ab87f9076ac57fa88f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbd09e98d273b5a613d84daa2057fbcb36b7f2a85143a2189a713703e395a91b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ed83e6a45c85fe65aa3375e9faccb1b4e8e06942c7eff0179a601514e0db1f(
    value: typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef075ace539f964b5771bbfaa88a6c3f111be6c72eb9035c1afd1436f1313e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38f0bf0fb899f5d484a5cb4006131a972ef0c76162a63db6a661890f9dc6b8f9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9abb970e750c8e51b6c3e80f81af97bfca83661e7612102afdfa2f3f6443ab94(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__608fb39081a579962d2c24e0bb9a4bdaeeb56401ef4d237ed86ad0f3f4b0452f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b288a764972a6cf42519e7f6ad4865f2b2a3edd7c20005a78d84706223b646d(
    value: typing.Optional[GkeonpremBareMetalClusterLoadBalancerBgpLbConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7e663463f51bcb9858cc888900d593183511e20538bb75237f2a73e541905fc(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__befa13d3c08b1b3ca2f7d47ac565c16fe3c809dd19f034fd55ca21aa66393d3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc31ba25bcd6ef9a23867a061a049b7a010e9e983bb181d7ce9007f0710a4296(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d8ad3830fb0cf52fe589cd849a44358d37f1142347ff8415b56658a50f42ae7(
    value: typing.Optional[GkeonpremBareMetalClusterLoadBalancerManualLbConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f366b7b9737cf1f4a0c580909499fbd58fa91841cf1d7f84305fc98146cffe2(
    *,
    address_pools: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
    load_balancer_node_pool_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edc60ba5a8c9ff08503241de995b75dd2d5453a4cc1f440a2dde1c99737a2990(
    *,
    addresses: typing.Sequence[builtins.str],
    pool: builtins.str,
    avoid_buggy_ips: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    manual_assign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aecd3a86487fb6cf458e289fcebfb604ca36b34fe837ce9d7ce9493848d55739(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f034c907edacfb0e7f5f990cdd0b752d1c1492ffd9c30c438399b4b55df4e47(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcb1b7099159c70eecb98d9ff6f36a7f02192d66c156f9b183c003b4a55f1df5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6f4e87a110a7add5bf9f6e37d0b4f8a5d4d8a155d9a3e7ef9350f6bc1dab57d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f1246e7b54488d8433cccded5ecfed3b900eec85b15dbf3f948a3acf71a81e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c85cb2b5ea2ee6e99619a32e5b6daed6629660e04f735c1a0e7d5b1cc47cde(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28da6c0d8a46adb1ac9af1ae95d5c0d6d30bf6442fbe818840878958e2fd330d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056470b17f115e16aadd5b785af6cfde4a470eeea0698d4a4229cb1897b9c0e8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04c11bf32dcb8fd27a3fa0cf6bcc625066c0c5e8bb8011144da42a8e8f72dc8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90c07aeef87859257499240481e2f6df04f08908b8080cf5625267ed363901a7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d109ebd88e90afee413992c218e4a28e1dcd93370d988fafdca03c3bfe9224d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f87addf9107ebea857f6b39c400a98ab9bf3df0f25b276a28dea86bcdbfbc13(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af2fc90c6888f489e470a3d0017be2f5e559dac88daa9a8452a123f982203aa5(
    *,
    node_pool_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeca46ab3fecd5cf5139de22702b6de74052e9a3ed98a9f211b24edbcc18dd2c(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    operating_system: typing.Optional[builtins.str] = None,
    taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7931f8f5aea6f29ac45a09a21c20d11489e1c77c493884e34105beb90516c066(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8272e689cef0a328f7e1282875b17fd4f877bf4bf47205537a33337663f04580(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1b30528d75027882001fa2a5298d704d8f8ca1b803a19ecddf7a57cb7b7b51c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__850410eb098eccb8798ebece1d3694f7ba8accbbd78f868835df239732a1a962(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69bc2a20e33c3ebc6a0e68040d76fa62867a7e71592b794b603c686577a8d6cb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__383b3d0c53007b9badef71c5aabf6ed097dfc5a2d64c8da55a9c33a32838047f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c39e5562414ba4f1e5bddeb0a861096b0cb834b7b183a47dbb9b443fa9b581d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c3048b28ef6fdd709782267361fa808c6f6b9df5c3e6de7100b1154cd7e7852(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f91da5f6928e330a9b91b24b2e8ae24c82abf7c3ab8368bc323b55dd8b49200c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__067712a7bd6513e61ea3734545d757d91e67a6f7c1e5ee02cac9e4901f2e4887(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34db100287b186c7ce5f7762dca88f312a0e2195d504caf77835c118e5feceb6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e151435248f24cb46d9f59392ca200bcc4d948e3c796316cd335612ecb142409(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba45ba325d5d8c4e63b18c9e0c570e45437a55af161f4b88ac663faf3c2be28(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2e22990265addf38c33b43dcc23d5f71709a8c2c1264073ee30f9eba68301f9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d6fb1edfa68cdb2afd91f21c954902018eecfd12cecde12893897e1297ab97(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e67c66ef28a2dcf8f8dc792ef1127f0c8f40cd1df5879a7181ffec8e387dfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e2400c4adc08a31490628bc4e8785deb8d827f3bd72bd316d23d02582ea6f18(
    value: typing.Optional[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1161e2d406cb86151341a307a92bfff1d07bf37a083110e53219dacbba6cf4aa(
    *,
    effect: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8de53f5a381c8e1d4cdece0b821f2a5251b46fbff0f39b637ebd4edb43b2f5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1780b1de61336796df2255efaf9825a28d8a931754a8cb3c09c6b5d697baa4c1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89d0ce5c78f5803ebe4a145bf7530c9b46dbcb5b1e136401ee5cedc7180fa224(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e16a7d1a99b047dce5c4522a39da93b3a878ddc6f83305807c433574947c80e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a617706262418dd449b29b09bf761c8ec50a0a8fc702c9c73c72d3a66dc19e88(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd8ea025cdd6ff363b9eb95b3e7310487f54953efacf62d967d98dc90786a5c1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36737d9685f359f983334557ac9275bfb1fb2a04368ce339be6b1ced9dd21be6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9abf9e2390b9d0d01a299f7d9e7eb599449ff071372657e86a1f6f20f51dd640(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b98a2e0d18163911d1ab4239afbe2dc503dcdec85ae68391c8b05fdbed67f749(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75940181e478b9ff93745779f3c5fcfe409db82ef933db602390efe678d55736(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b631b607a5f77fe62d6b1399dd41311a2d763aad2db27e8bb69ecc36dd09a07(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__899029eb510006ff9712f5139c3bdbf1fbe3c09ad5dcddf1af0aa3ccf118a61d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e14feafce86273d9f6613e9c306913666e82369f3171e657219037454160d06(
    value: typing.Optional[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2e7a4424432c292a14d003f7cdee4a73f02f2e255f5e83566540383221f8654(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2010bb412a87df87e0097f5c106ef0fe85b0cfb799332ca2a2a9e378d136923(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf78a36d418776874bdd2747cf1aa9cbe4e0745149104aed6c8c28a8ae138b0d(
    value: typing.Optional[GkeonpremBareMetalClusterLoadBalancerMetalLbConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c0e2d198e904368ae3a84c7e216079d5cd0410d1faaef22d5b556c8a27e8da7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ba50de5661ad16c9c1e0a86e3710547befab6abb317d7c627f86775dc4e8d4(
    value: typing.Optional[GkeonpremBareMetalClusterLoadBalancer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__312e6a9ee18617a01ca16fca8b4de3c86d386290c677f3793d2d47358970102b(
    *,
    control_plane_load_balancer_port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c12d6154fc67b0d653128645795b95955834b383bd3440990d00d97590ac868(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__383c6539c22dd4aeac3b369512c3104ef915de9d70f8bdd82d53a4ca8ffd16fa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b41b39d931b48c25dff2599bca3f8d6ad3b436f3e32b0f8778ef2e8fab2581d4(
    value: typing.Optional[GkeonpremBareMetalClusterLoadBalancerPortConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e7da560f21d74b93a60a91f697e10add218d82ab2296d90164570b209d7dd91(
    *,
    control_plane_vip: builtins.str,
    ingress_vip: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d36ec219d6696a7bc64aa10940d30ab8b6a672f18871142d2b8dff8323f686(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__314bf994d8be2085229f095d0ea1042dca4f3659fc703de1fd747d224b3f4bad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a4013cc6ddf3cb5f2440c458df7dc70c04e3428ac7324b1dcef2a009f90680(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e41f600d6a6aff42ee70754d9e50a3934567fa9035013c16a59d1468189bef(
    value: typing.Optional[GkeonpremBareMetalClusterLoadBalancerVipConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1871e97979320770d73508ced0c667d9634ded5ff38da39c1b2d8ad1e4191da(
    *,
    maintenance_address_cidr_blocks: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc562542ec410cb62db9753d9c29380b3b3d444390b61bd1cc55037e7d27ea75(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c54a1728082a5b0749039f1b49b10d335b8d69f9a2dee047f2129ba2a3de8f4f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__705820854fca5c1c80e4eb6119daf45bb559e1c34747dc3147480105845795ff(
    value: typing.Optional[GkeonpremBareMetalClusterMaintenanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241ca04deec36fde0120b2be3d19277270a2f45f955f9ed7eee68dbb4e567588(
    *,
    advanced_networking: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    island_mode_cidr: typing.Optional[typing.Union[GkeonpremBareMetalClusterNetworkConfigIslandModeCidr, typing.Dict[builtins.str, typing.Any]]] = None,
    multiple_network_interfaces_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    sr_iov_config: typing.Optional[typing.Union[GkeonpremBareMetalClusterNetworkConfigSrIovConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da5f430b6b2e4da26687c1be6775b5ce6cee97bb23e820a8f9cde6d61b3a0fbb(
    *,
    pod_address_cidr_blocks: typing.Sequence[builtins.str],
    service_address_cidr_blocks: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a59f7bf3061a783d08361cb9dc6517dabe88f5d9f06d3aad3deb1a90c2236d3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc084d41211b778acbf4827f2f7f0f1868b9c4aa62a10efbdb36c17676569e6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d84a8e575875356844c56b13dc2da14e5e19a22c5951aefa93f03d72959b055(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e607966811fff2aec910678f70f6451f05492c6e607e4bbeea96711d7f3a00b2(
    value: typing.Optional[GkeonpremBareMetalClusterNetworkConfigIslandModeCidr],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73a803de835364cb01d06fcff9ca3436fc7287898c6137500575f801be873f16(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8bfd550d51f4180cb5a822a8779055b9d814c177a8f324007f03310fcfda3e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67747189923dcc233a6dc730d6291417801432b3bb973e17c903fd4d5c051381(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__105e9d6fe7214875a440695e9ae08cb9a8a1438396565d02de89810e59605b46(
    value: typing.Optional[GkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f62ffb965e7b3227e60ccda944eed623bcc0eee6189282144ec30b7c16d406(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1b2fb7e0a3b9beae5032b7d0daab2db7ae244890d06ca0a0f0006875f81ec3f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5164daf4e5a0b53a5bd65411970402971eb1e82ead766ddffb7100a79cfb8b9f(
    value: typing.Optional[GkeonpremBareMetalClusterNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ad8ab5df0e1d36992d407b1e4382d2e4ea7186b90f37917d278c6c20e4d13fe(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__014da7a7726293a3001dda8ce50063be68248118503ccc68666b638d1fa31a20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b400660e65850a03527aba33e31d3e3803a77b9955608ccf534131821ef8aec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45d7551755cd9f480f548767f1a5634280b210c352f15b0dd2d41704581e7442(
    value: typing.Optional[GkeonpremBareMetalClusterNetworkConfigSrIovConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f99eb7bfb41ddaf0e59a57034aed967252d7afb90a7b7bdc2ca613eed88c30b(
    *,
    login_user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb29abb60287c5fece9e33378fa18f4f220484bf1f577c24657c6a87f9f7ea6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__185ca0559130ab3c5d954f36a24b0c6ac2135049c0d7200f4d50401ca121d74b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__febe29de259b2c260b20f37d057692c4e693e46a3a1fe8e1e3d340d198beb723(
    value: typing.Optional[GkeonpremBareMetalClusterNodeAccessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1333b9d5e1a67abbb7ff29e77451339f73bdaf3ec4368ff71fa5cf660e3e7964(
    *,
    container_runtime: typing.Optional[builtins.str] = None,
    max_pods_per_node: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b37be0312dc5e0b9aac4352ea5d6958ad4fcf8798fc7a340ae47acbc8da1dec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b3b23093566d0b7f93539fb89dc2f13ad5af00b806f74c2f2b6f0452583a7f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__378f316f27562575ec83f90bfedffb32591ddcefc5cbdca5c1409d3bb898485c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171a744b5cdeaed551681f6f0218e86702619d18dce578e55c8d690d831fcf19(
    value: typing.Optional[GkeonpremBareMetalClusterNodeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7742ff5e3fd4e6b0bf02c199ba4cc6d3e1708572d0a977c770d9098f8703b2dc(
    *,
    package_repo_excluded: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__128f2db492bb542f57a61ed0de206ca956fb38f985c3064a40680ac04cd4859e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ded4a30d50e6006a997be2bb1662da582ac017b1dd3e846c7178b9d67b7c700f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__845846514115030701c71702549dd8ab7ce2d0e8567d46ba86ad20a8574b5596(
    value: typing.Optional[GkeonpremBareMetalClusterOsEnvironmentConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb4e308b038ed571246d1c5becbeae8270581938cb000c87e50dcb8e4c5564ce(
    *,
    uri: builtins.str,
    no_proxy: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aae552c56265ea7d37764c1b383605e6eef666dac0f8168fcf03319b17637cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a7165e8bddd14d82e715119fd34f9534ec85dde0c4cc276080eb6be9ca4d337(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c451eda9e4125c849a88c76191d1bde2acb74bb30d885b75768cc9c47580e751(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f97a87ed55d5d0856a2280041e4fe5b802487e6396630397fb3c13c560715f1(
    value: typing.Optional[GkeonpremBareMetalClusterProxy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaa8ec79127b2f3e079bf04d8ff7dab83f015ba27c43789dd3dd916384f65e0e(
    *,
    authorization: typing.Optional[typing.Union[GkeonpremBareMetalClusterSecurityConfigAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc21d2f85c2aeeec04c703eea36a5a6dbd7f60174261bbe41250cf92295b0708(
    *,
    admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee27aeff052ed5876cbee012d798b09affbc3db14ca4a72ffc005d8abf6a1cf(
    *,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f1e43846252a9244aa4308d47bc7d8b82f3115532ff69e62e1ddb3607d034e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a5cb0daefe60cb24d977d717ba4708e72fe321470841d1b7e11a4cfd5b2fee(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d7a4098019dcfc06b340262187c5722726506ebb527b000c4e09e16afd6b5a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67cdb4721fac08d3489ba793c2c0ed496916e309c6b95c2346bda4993f0dbc9b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c4ddcef89a27d74a196f3034a1571d5d16e25a5d234e9f3563223fc90ff5acd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fb5de7ceabcc48e2d0d1a72a6e29203244e2d42b44ea4e6f6dbcc76d2d62369(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad87968ed032115d8ee7f50ca79505f7dd1a74e6e0b2b379c756f99087d85ba1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42717ce4373612ba8bb88391adb5fcc6ec998da04366b9faf300ab36a6e78ad9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61b47b77a8646fb0da141a15e9522f4c59c42dfeff78476510d9cd47dc758466(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92edbb521412634ce71f31a02a54635fae03219a906e361d1b4184a5a3f0ad97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b19979566593929325cfc71edeb69175afa4b5ba0594501acd96c766231381b5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b619b40458ef2db11684a91bc9f70cf060111a12b811d95ff5fffe6332c73f(
    value: typing.Optional[GkeonpremBareMetalClusterSecurityConfigAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a67d7069bf4810697f75e62d829bda322c3bd8321b49eb8a752a7d063ca5df41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__576341916a0d1490628c837c1802e60ed498526f3d10252f79728c8ad2a7056a(
    value: typing.Optional[GkeonpremBareMetalClusterSecurityConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f92f5c0baf1aac254084ba0c11fa3ceeea946c799f79ca73a3d3f4c6de944342(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ae3c7c59de45cb57fd207e3ab9b70e1c07ecaa45db21a480233fb9939e93f4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__497c2fbd1d7309ccd3212686efbe2b4b70539b57aaac506afafb37137094b764(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e44e96ce83fb88fb9e5b026a5cd59228e46e22509e6b98b898fe715e15c45478(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__881ea6bbcf0343fb4475914797dbde8f43caaa1a2a5b551f814faed541a715b9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827ef58020195e6c08b24bdb45eabc311370d03d010598a38e2e2b592972b301(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df97b004b587d44b94ff4d0cfd339072c17bcf9bb200abd6effa0c3567a1ef8f(
    value: typing.Optional[GkeonpremBareMetalClusterStatusConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a72bb346c43d7ac87fb5d8465346f37829a81303830c106ae72476a6baf4aff8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67b5dc054c30e06dadfd83636e5763fe1c9d2c47835c2fe2343297d69d1f35ae(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c2f8765f69c5eecb4672c9be0d0fcdd3c6fb879baf2e9e13c3f2ba10778e68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a491170cee8be5163f7286f3c24f567679d0e9fb2cf333caafbbdd43f4883014(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1134a2a19510b53a26e9a845e3de4e8aeeafd5b4e046401bfe5fcbc5b99469e8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b673804315f231111f4c45ad99e2732692c87a12e398fdcb25c8524c001b94f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7a2cbcf873bd20ec62e0ce9c926399ab5ed47c6122cf06c1eb0a0ae87d48796(
    value: typing.Optional[GkeonpremBareMetalClusterStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f9f725ed54f80fbf4d2a9a544d1ef9c5e393382c717467c18fde909fdacd54(
    *,
    lvp_node_mounts_config: typing.Union[GkeonpremBareMetalClusterStorageLvpNodeMountsConfig, typing.Dict[builtins.str, typing.Any]],
    lvp_share_config: typing.Union[GkeonpremBareMetalClusterStorageLvpShareConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f76a8e911934a00023b332986a5873f340d95fcbef05221dffffbf6a55ead24(
    *,
    path: builtins.str,
    storage_class: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce61c7a78e370f276f9df11d692c64c2e476ec38db7caaa6cc6cc61cb7bfbd5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f65e987d14d5bde4c3c10ae633b9235768d58ca7a35de89251fb49b3574dd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b04a8e0bd2da800c4de27b62583a85c0cfc6cb98b3f7d4d6ae639491102e5f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7a2bd68f2d844c16a61bd009115b8fb86bc726cc3ab37915cf60973f0a523b4(
    value: typing.Optional[GkeonpremBareMetalClusterStorageLvpNodeMountsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1814ac8bac5e7f38bdb6ff1c09e58b839d79c9a55d7557beeebee48477e9204e(
    *,
    lvp_config: typing.Union[GkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig, typing.Dict[builtins.str, typing.Any]],
    shared_path_pv_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7d58022569387950c09f5fb638dc047ebdc59be9e180840a73279435295f1a(
    *,
    path: builtins.str,
    storage_class: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91bfd22bfc4f9c2abde48a2a4a1cb878a9723eb72c51ba4136a179a9c217853(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08e9b127b3f28947f5f11279a6f9f8535758e083e53b8e4745b7f177cd9627f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ffe53bf53e32137d32496f1ba6030606f32330430961fa7122e97e2998503ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5039b4ddf5dae80052f5e2d350ff963dc6b378bf7d9c034aa2672af1bb694ca5(
    value: typing.Optional[GkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f264bbd6b7cf0edd44e03458086232d292b172a87c18ba87ea539c9820996c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c94ed27f7a9921b18d20c715ef906eda5bea6785157b1cc3b18595d3803c4e98(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a8641ef055fa955de36362f8bff90383d45d6ec207f99a1d823ab0e19c5af6(
    value: typing.Optional[GkeonpremBareMetalClusterStorageLvpShareConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c4ffb0e55028a3af48b91741765a2dac60e5ea63a8f47d73346d72f588c43f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d1cc6f6021cff98de960ded61339b15af92e01e7a0d07bb6fc4efbb7c1df69(
    value: typing.Optional[GkeonpremBareMetalClusterStorage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dddc46f8e09db9c26861399c2985c3a8041417bc2cd6b31adf415d6443dbc051(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e629c97a2f6660c367265e9c975b0fd1d5d9c886690b6f6e08cb3131660890(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c31941651a3d941c78246bb480b5e751848a8b8c3c9d94bae6e36912db12a46e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd290d97a04c00ce3b7dfa794d68e748ca41fce070c218e04b4db244db8b799e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fdb14bc9c7e3f9014a6e98d8af32053ce1c9c37f9cc33333a00d4944e14f38a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5337f6346c0e2ea82bbfec6c791dc1e220a51e05ad12143cc0616ac29d57670(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7028f6a470bd951cd2dc4ce5fe3232c58fec3249ad412a7348b0c867cbde7cd(
    *,
    policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c86e99fbd4d91cadb1a5389f92c7c24d3617beb63499e580d5d4147d5ba37c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3733fc5bb8ab089b9b61f2b5dd1a9b0648ab28b2733b13ec2acc30d325ece3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de064e6289cf817d904000664b2e3f337cff31394f075552e8a021b69b2287a3(
    value: typing.Optional[GkeonpremBareMetalClusterUpgradePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ba500b0d68c7aacff6504be3ebfd747dcdbaab5db85e125c0ee39fd989020bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c494fa68e3fc63dc91c7cab7777bd121c597123b3596eb1c9c207e94648934de(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73a5a3c905c0f2a60f346d885cbc909b6673bee7e95cd2b6a2bb289002caf48e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2439ea329baa36748b005e37ea588822003836c7f674bcc04e3f608a6be68561(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8b11566b88236c9ef872ae2173adfd498941eaa1c013cffc313ae70ea3041a6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1373d815a0d139c0d73add92a3dffd03e041a832992a376a79eed944d0a0e078(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d38958394e446d9f93f8679b28445431cd173e42b0dad79ab318e2378b98c75(
    value: typing.Optional[GkeonpremBareMetalClusterValidationCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5d63804193095134b9ee255058a9f40e96bc55d4e2b8279ea5b9d4179a4b17c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a36008820096069aaf27b0987dddb1c0dd36145c53c3382c62a6667039c80a00(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e234e12911857b15313085fdabb8bb85c61674f97aa907c1dab9a54e0da076d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66d0744c7cbec7d1e95591d2f8b4914ce3cca5faa37af8fc68ec805a84bb115c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a51ebcd54305786c2e4a00c07b60d02d7350100099b7e6b3c9ed643d2a6430b9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967bc0c19fe21d7d6da805f4f917e42add6ce4eb126f4c94e983bb04ab204ca8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b293f7c39a13a4b30fa3d96fe3871e258a4f6e96308b0f1ecbce2a56aa1599(
    value: typing.Optional[GkeonpremBareMetalClusterValidationCheckStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a4efd72427d39a9d5b38ed7f95863a3fcbddec036c9f5a5af22ef54608e0d64(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f797dac7ccf596b64370337dcf476f6ef998ee5bfb992a4d817425c9f91861(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9bd63f182fcf49fdc93183b68298ca3539b606a66f85c2ebe226a706b759436(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29701cfe89caf03b9c911865cc55324bd5e7942c0e68b44a8786bf9ed4762755(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__838974888ac3144c8d98619ec7210ee0b05d69d3806e65479a5b43c204c89bbe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__099fba7a4ac17123510e7ae8676be8716b6715722a8e5496fb6d134e85eba820(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a1ced248061329020e34a0cef8579b178dcab9c61aff80f1fc398ea9d73468c(
    value: typing.Optional[GkeonpremBareMetalClusterValidationCheckStatusResult],
) -> None:
    """Type checking stubs"""
    pass
