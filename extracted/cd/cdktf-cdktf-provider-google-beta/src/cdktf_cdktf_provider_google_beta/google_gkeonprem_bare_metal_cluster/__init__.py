r'''
# `google_gkeonprem_bare_metal_cluster`

Refer to the Terraform Registry for docs: [`google_gkeonprem_bare_metal_cluster`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster).
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


class GoogleGkeonpremBareMetalCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster google_gkeonprem_bare_metal_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        admin_cluster_membership: builtins.str,
        bare_metal_version: builtins.str,
        control_plane: typing.Union["GoogleGkeonpremBareMetalClusterControlPlane", typing.Dict[builtins.str, typing.Any]],
        load_balancer: typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancer", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        network_config: typing.Union["GoogleGkeonpremBareMetalClusterNetworkConfig", typing.Dict[builtins.str, typing.Any]],
        storage: typing.Union["GoogleGkeonpremBareMetalClusterStorage", typing.Dict[builtins.str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        binary_authorization: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterBinaryAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_operations: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterClusterOperations", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        maintenance_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterMaintenanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_access_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterNodeAccessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        os_environment_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterOsEnvironmentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        proxy: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        security_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterSecurityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        upgrade_policy: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterUpgradePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster google_gkeonprem_bare_metal_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param admin_cluster_membership: The Admin Cluster this Bare Metal User Cluster belongs to. This is the full resource name of the Admin Cluster's hub membership. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#admin_cluster_membership GoogleGkeonpremBareMetalCluster#admin_cluster_membership}
        :param bare_metal_version: A human readable description of this Bare Metal User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#bare_metal_version GoogleGkeonpremBareMetalCluster#bare_metal_version}
        :param control_plane: control_plane block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#control_plane GoogleGkeonpremBareMetalCluster#control_plane}
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#load_balancer GoogleGkeonpremBareMetalCluster#load_balancer}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#location GoogleGkeonpremBareMetalCluster#location}
        :param name: The bare metal cluster name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#name GoogleGkeonpremBareMetalCluster#name}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#network_config GoogleGkeonpremBareMetalCluster#network_config}
        :param storage: storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#storage GoogleGkeonpremBareMetalCluster#storage}
        :param annotations: Annotations on the Bare Metal User Cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#annotations GoogleGkeonpremBareMetalCluster#annotations}
        :param binary_authorization: binary_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#binary_authorization GoogleGkeonpremBareMetalCluster#binary_authorization}
        :param cluster_operations: cluster_operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#cluster_operations GoogleGkeonpremBareMetalCluster#cluster_operations}
        :param description: A human readable description of this Bare Metal User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#description GoogleGkeonpremBareMetalCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#id GoogleGkeonpremBareMetalCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintenance_config: maintenance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#maintenance_config GoogleGkeonpremBareMetalCluster#maintenance_config}
        :param node_access_config: node_access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_access_config GoogleGkeonpremBareMetalCluster#node_access_config}
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_config GoogleGkeonpremBareMetalCluster#node_config}
        :param os_environment_config: os_environment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#os_environment_config GoogleGkeonpremBareMetalCluster#os_environment_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#project GoogleGkeonpremBareMetalCluster#project}.
        :param proxy: proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#proxy GoogleGkeonpremBareMetalCluster#proxy}
        :param security_config: security_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#security_config GoogleGkeonpremBareMetalCluster#security_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#timeouts GoogleGkeonpremBareMetalCluster#timeouts}
        :param upgrade_policy: upgrade_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#upgrade_policy GoogleGkeonpremBareMetalCluster#upgrade_policy}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c92b632ac8feae48e420ffc3ca1905bca79f48e5c362b3c91359050e75b8f780)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleGkeonpremBareMetalClusterConfig(
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
        '''Generates CDKTF code for importing a GoogleGkeonpremBareMetalCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleGkeonpremBareMetalCluster to import.
        :param import_from_id: The id of the existing GoogleGkeonpremBareMetalCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleGkeonpremBareMetalCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e81f811311e8da189db7e2e75b8b99a440ab73c03bd7a00ef82ad275a71bcd9)
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
        :param evaluation_mode: Mode of operation for binauthz policy evaluation. If unspecified, defaults to DISABLED. Possible values: ["DISABLED", "PROJECT_SINGLETON_POLICY_ENFORCE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#evaluation_mode GoogleGkeonpremBareMetalCluster#evaluation_mode}
        '''
        value = GoogleGkeonpremBareMetalClusterBinaryAuthorization(
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
        :param enable_application_logs: Whether collection of application logs/metrics should be enabled (in addition to system logs/metrics). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#enable_application_logs GoogleGkeonpremBareMetalCluster#enable_application_logs}
        '''
        value = GoogleGkeonpremBareMetalClusterClusterOperations(
            enable_application_logs=enable_application_logs
        )

        return typing.cast(None, jsii.invoke(self, "putClusterOperations", [value]))

    @jsii.member(jsii_name="putControlPlane")
    def put_control_plane(
        self,
        *,
        control_plane_node_pool_config: typing.Union["GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig", typing.Dict[builtins.str, typing.Any]],
        api_server_args: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param control_plane_node_pool_config: control_plane_node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#control_plane_node_pool_config GoogleGkeonpremBareMetalCluster#control_plane_node_pool_config}
        :param api_server_args: api_server_args block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#api_server_args GoogleGkeonpremBareMetalCluster#api_server_args}
        '''
        value = GoogleGkeonpremBareMetalClusterControlPlane(
            control_plane_node_pool_config=control_plane_node_pool_config,
            api_server_args=api_server_args,
        )

        return typing.cast(None, jsii.invoke(self, "putControlPlane", [value]))

    @jsii.member(jsii_name="putLoadBalancer")
    def put_load_balancer(
        self,
        *,
        port_config: typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerPortConfig", typing.Dict[builtins.str, typing.Any]],
        vip_config: typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerVipConfig", typing.Dict[builtins.str, typing.Any]],
        bgp_lb_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        manual_lb_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerManualLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        metal_lb_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param port_config: port_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#port_config GoogleGkeonpremBareMetalCluster#port_config}
        :param vip_config: vip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#vip_config GoogleGkeonpremBareMetalCluster#vip_config}
        :param bgp_lb_config: bgp_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#bgp_lb_config GoogleGkeonpremBareMetalCluster#bgp_lb_config}
        :param manual_lb_config: manual_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#manual_lb_config GoogleGkeonpremBareMetalCluster#manual_lb_config}
        :param metal_lb_config: metal_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#metal_lb_config GoogleGkeonpremBareMetalCluster#metal_lb_config}
        '''
        value = GoogleGkeonpremBareMetalClusterLoadBalancer(
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
        :param maintenance_address_cidr_blocks: All IPv4 address from these ranges will be placed into maintenance mode. Nodes in maintenance mode will be cordoned and drained. When both of these are true, the "baremetal.cluster.gke.io/maintenance" annotation will be set on the node resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#maintenance_address_cidr_blocks GoogleGkeonpremBareMetalCluster#maintenance_address_cidr_blocks}
        '''
        value = GoogleGkeonpremBareMetalClusterMaintenanceConfig(
            maintenance_address_cidr_blocks=maintenance_address_cidr_blocks
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenanceConfig", [value]))

    @jsii.member(jsii_name="putNetworkConfig")
    def put_network_config(
        self,
        *,
        advanced_networking: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        island_mode_cidr: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterNetworkConfigIslandModeCidr", typing.Dict[builtins.str, typing.Any]]] = None,
        multiple_network_interfaces_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        sr_iov_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterNetworkConfigSrIovConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_networking: Enables the use of advanced Anthos networking features, such as Bundled Load Balancing with BGP or the egress NAT gateway. Setting configuration for advanced networking features will automatically set this flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#advanced_networking GoogleGkeonpremBareMetalCluster#advanced_networking}
        :param island_mode_cidr: island_mode_cidr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#island_mode_cidr GoogleGkeonpremBareMetalCluster#island_mode_cidr}
        :param multiple_network_interfaces_config: multiple_network_interfaces_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#multiple_network_interfaces_config GoogleGkeonpremBareMetalCluster#multiple_network_interfaces_config}
        :param sr_iov_config: sr_iov_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#sr_iov_config GoogleGkeonpremBareMetalCluster#sr_iov_config}
        '''
        value = GoogleGkeonpremBareMetalClusterNetworkConfig(
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
        :param login_user: LoginUser is the user name used to access node machines. It defaults to "root" if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#login_user GoogleGkeonpremBareMetalCluster#login_user}
        '''
        value = GoogleGkeonpremBareMetalClusterNodeAccessConfig(login_user=login_user)

        return typing.cast(None, jsii.invoke(self, "putNodeAccessConfig", [value]))

    @jsii.member(jsii_name="putNodeConfig")
    def put_node_config(
        self,
        *,
        container_runtime: typing.Optional[builtins.str] = None,
        max_pods_per_node: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param container_runtime: The available runtimes that can be used to run containers in a Bare Metal User Cluster. Possible values: ["CONTAINER_RUNTIME_UNSPECIFIED", "DOCKER", "CONTAINERD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#container_runtime GoogleGkeonpremBareMetalCluster#container_runtime}
        :param max_pods_per_node: The maximum number of pods a node can run. The size of the CIDR range assigned to the node will be derived from this parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#max_pods_per_node GoogleGkeonpremBareMetalCluster#max_pods_per_node}
        '''
        value = GoogleGkeonpremBareMetalClusterNodeConfig(
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
        :param package_repo_excluded: Whether the package repo should not be included when initializing bare metal machines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#package_repo_excluded GoogleGkeonpremBareMetalCluster#package_repo_excluded}
        '''
        value = GoogleGkeonpremBareMetalClusterOsEnvironmentConfig(
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
        :param uri: Specifies the address of your proxy server. For example: http://domain WARNING: Do not provide credentials in the format of http://(username:password@)domain these will be rejected by the server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#uri GoogleGkeonpremBareMetalCluster#uri}
        :param no_proxy: A list of IPs, hostnames, and domains that should skip the proxy. For example ["127.0.0.1", "example.com", ".corp", "localhost"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#no_proxy GoogleGkeonpremBareMetalCluster#no_proxy}
        '''
        value = GoogleGkeonpremBareMetalClusterProxy(uri=uri, no_proxy=no_proxy)

        return typing.cast(None, jsii.invoke(self, "putProxy", [value]))

    @jsii.member(jsii_name="putSecurityConfig")
    def put_security_config(
        self,
        *,
        authorization: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterSecurityConfigAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#authorization GoogleGkeonpremBareMetalCluster#authorization}
        '''
        value = GoogleGkeonpremBareMetalClusterSecurityConfig(
            authorization=authorization
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityConfig", [value]))

    @jsii.member(jsii_name="putStorage")
    def put_storage(
        self,
        *,
        lvp_node_mounts_config: typing.Union["GoogleGkeonpremBareMetalClusterStorageLvpNodeMountsConfig", typing.Dict[builtins.str, typing.Any]],
        lvp_share_config: typing.Union["GoogleGkeonpremBareMetalClusterStorageLvpShareConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param lvp_node_mounts_config: lvp_node_mounts_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#lvp_node_mounts_config GoogleGkeonpremBareMetalCluster#lvp_node_mounts_config}
        :param lvp_share_config: lvp_share_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#lvp_share_config GoogleGkeonpremBareMetalCluster#lvp_share_config}
        '''
        value = GoogleGkeonpremBareMetalClusterStorage(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#create GoogleGkeonpremBareMetalCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#delete GoogleGkeonpremBareMetalCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#update GoogleGkeonpremBareMetalCluster#update}.
        '''
        value = GoogleGkeonpremBareMetalClusterTimeouts(
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
        :param policy: Specifies which upgrade policy to use. Possible values: ["SERIAL", "CONCURRENT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#policy GoogleGkeonpremBareMetalCluster#policy}
        '''
        value = GoogleGkeonpremBareMetalClusterUpgradePolicy(policy=policy)

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
    ) -> "GoogleGkeonpremBareMetalClusterBinaryAuthorizationOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalClusterBinaryAuthorizationOutputReference", jsii.get(self, "binaryAuthorization"))

    @builtins.property
    @jsii.member(jsii_name="clusterOperations")
    def cluster_operations(
        self,
    ) -> "GoogleGkeonpremBareMetalClusterClusterOperationsOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalClusterClusterOperationsOutputReference", jsii.get(self, "clusterOperations"))

    @builtins.property
    @jsii.member(jsii_name="controlPlane")
    def control_plane(
        self,
    ) -> "GoogleGkeonpremBareMetalClusterControlPlaneOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalClusterControlPlaneOutputReference", jsii.get(self, "controlPlane"))

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
    def fleet(self) -> "GoogleGkeonpremBareMetalClusterFleetList":
        return typing.cast("GoogleGkeonpremBareMetalClusterFleetList", jsii.get(self, "fleet"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(
        self,
    ) -> "GoogleGkeonpremBareMetalClusterLoadBalancerOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalClusterLoadBalancerOutputReference", jsii.get(self, "loadBalancer"))

    @builtins.property
    @jsii.member(jsii_name="localName")
    def local_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localName"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceConfig")
    def maintenance_config(
        self,
    ) -> "GoogleGkeonpremBareMetalClusterMaintenanceConfigOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalClusterMaintenanceConfigOutputReference", jsii.get(self, "maintenanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(
        self,
    ) -> "GoogleGkeonpremBareMetalClusterNetworkConfigOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalClusterNetworkConfigOutputReference", jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodeAccessConfig")
    def node_access_config(
        self,
    ) -> "GoogleGkeonpremBareMetalClusterNodeAccessConfigOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalClusterNodeAccessConfigOutputReference", jsii.get(self, "nodeAccessConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfig")
    def node_config(self) -> "GoogleGkeonpremBareMetalClusterNodeConfigOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalClusterNodeConfigOutputReference", jsii.get(self, "nodeConfig"))

    @builtins.property
    @jsii.member(jsii_name="osEnvironmentConfig")
    def os_environment_config(
        self,
    ) -> "GoogleGkeonpremBareMetalClusterOsEnvironmentConfigOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalClusterOsEnvironmentConfigOutputReference", jsii.get(self, "osEnvironmentConfig"))

    @builtins.property
    @jsii.member(jsii_name="proxy")
    def proxy(self) -> "GoogleGkeonpremBareMetalClusterProxyOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalClusterProxyOutputReference", jsii.get(self, "proxy"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="securityConfig")
    def security_config(
        self,
    ) -> "GoogleGkeonpremBareMetalClusterSecurityConfigOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalClusterSecurityConfigOutputReference", jsii.get(self, "securityConfig"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "GoogleGkeonpremBareMetalClusterStatusList":
        return typing.cast("GoogleGkeonpremBareMetalClusterStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="storage")
    def storage(self) -> "GoogleGkeonpremBareMetalClusterStorageOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalClusterStorageOutputReference", jsii.get(self, "storage"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleGkeonpremBareMetalClusterTimeoutsOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> "GoogleGkeonpremBareMetalClusterUpgradePolicyOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalClusterUpgradePolicyOutputReference", jsii.get(self, "upgradePolicy"))

    @builtins.property
    @jsii.member(jsii_name="validationCheck")
    def validation_check(self) -> "GoogleGkeonpremBareMetalClusterValidationCheckList":
        return typing.cast("GoogleGkeonpremBareMetalClusterValidationCheckList", jsii.get(self, "validationCheck"))

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
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterBinaryAuthorization"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterBinaryAuthorization"], jsii.get(self, "binaryAuthorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterOperationsInput")
    def cluster_operations_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterClusterOperations"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterClusterOperations"], jsii.get(self, "clusterOperationsInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneInput")
    def control_plane_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterControlPlane"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterControlPlane"], jsii.get(self, "controlPlaneInput"))

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
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterLoadBalancer"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterLoadBalancer"], jsii.get(self, "loadBalancerInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceConfigInput")
    def maintenance_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterMaintenanceConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterMaintenanceConfig"], jsii.get(self, "maintenanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigInput")
    def network_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterNetworkConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterNetworkConfig"], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeAccessConfigInput")
    def node_access_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterNodeAccessConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterNodeAccessConfig"], jsii.get(self, "nodeAccessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfigInput")
    def node_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterNodeConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterNodeConfig"], jsii.get(self, "nodeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="osEnvironmentConfigInput")
    def os_environment_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterOsEnvironmentConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterOsEnvironmentConfig"], jsii.get(self, "osEnvironmentConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyInput")
    def proxy_input(self) -> typing.Optional["GoogleGkeonpremBareMetalClusterProxy"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterProxy"], jsii.get(self, "proxyInput"))

    @builtins.property
    @jsii.member(jsii_name="securityConfigInput")
    def security_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterSecurityConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterSecurityConfig"], jsii.get(self, "securityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="storageInput")
    def storage_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterStorage"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterStorage"], jsii.get(self, "storageInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleGkeonpremBareMetalClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleGkeonpremBareMetalClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="upgradePolicyInput")
    def upgrade_policy_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterUpgradePolicy"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterUpgradePolicy"], jsii.get(self, "upgradePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="adminClusterMembership")
    def admin_cluster_membership(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminClusterMembership"))

    @admin_cluster_membership.setter
    def admin_cluster_membership(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f40457303082d5a005bc1cf4fcb73e12ba75ff4f75eb8de2d0694e0e50c1c05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminClusterMembership", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5a55dbd95fd9db05ca56d4cd4f01930d0e60692456ca01361edf6a87198c637)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bareMetalVersion")
    def bare_metal_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bareMetalVersion"))

    @bare_metal_version.setter
    def bare_metal_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db1ba2ff65d66995a11902dd5af67b26d3bddfe04e86b0fb4381ef0bf5f8344b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bareMetalVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6d9bf832b2c22a5f90f443d07700af07d957815123288e33228b88c636720f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c01c6f89522eeec1ca893222acb109dd2166e2d209c19eca68323fedbc5a1c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3ffcd13a90b2a8550f15a02abb295b7f987ba357149a99943090cd27dfbf6ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__435e0bb21ea3f2b4e106c1437261cf451fa1822d7bfa57ce89dd907cda58ae11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__713eff543b463eb44b57c71091d909ba1051c80b88fe0e00238bc934975d8855)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterBinaryAuthorization",
    jsii_struct_bases=[],
    name_mapping={"evaluation_mode": "evaluationMode"},
)
class GoogleGkeonpremBareMetalClusterBinaryAuthorization:
    def __init__(
        self,
        *,
        evaluation_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param evaluation_mode: Mode of operation for binauthz policy evaluation. If unspecified, defaults to DISABLED. Possible values: ["DISABLED", "PROJECT_SINGLETON_POLICY_ENFORCE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#evaluation_mode GoogleGkeonpremBareMetalCluster#evaluation_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9c6a6e0e49e4a87120e6ef0aa43a1e9a3784e022402ae6b4da0d848cedc0884)
            check_type(argname="argument evaluation_mode", value=evaluation_mode, expected_type=type_hints["evaluation_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if evaluation_mode is not None:
            self._values["evaluation_mode"] = evaluation_mode

    @builtins.property
    def evaluation_mode(self) -> typing.Optional[builtins.str]:
        '''Mode of operation for binauthz policy evaluation. If unspecified, defaults to DISABLED. Possible values: ["DISABLED", "PROJECT_SINGLETON_POLICY_ENFORCE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#evaluation_mode GoogleGkeonpremBareMetalCluster#evaluation_mode}
        '''
        result = self._values.get("evaluation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterBinaryAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterBinaryAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterBinaryAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a7a97bdbe20c8094c676a436ae57131d0e365db603e1281bd9b2c4f98092f0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e71c468412913dfa84611a1dc0cd6a3e26f553eacba5c7562da781140c7d1c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterBinaryAuthorization]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterBinaryAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterBinaryAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3ebd821718e2ca8d10713b300d61d059d91d474489fe5c1afc97fc5e494a3a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterClusterOperations",
    jsii_struct_bases=[],
    name_mapping={"enable_application_logs": "enableApplicationLogs"},
)
class GoogleGkeonpremBareMetalClusterClusterOperations:
    def __init__(
        self,
        *,
        enable_application_logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_application_logs: Whether collection of application logs/metrics should be enabled (in addition to system logs/metrics). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#enable_application_logs GoogleGkeonpremBareMetalCluster#enable_application_logs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b44b60c802fa12280f045f2a6327408629756b653388eb9d14590042ad40c700)
            check_type(argname="argument enable_application_logs", value=enable_application_logs, expected_type=type_hints["enable_application_logs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_application_logs is not None:
            self._values["enable_application_logs"] = enable_application_logs

    @builtins.property
    def enable_application_logs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether collection of application logs/metrics should be enabled (in addition to system logs/metrics).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#enable_application_logs GoogleGkeonpremBareMetalCluster#enable_application_logs}
        '''
        result = self._values.get("enable_application_logs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterClusterOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterClusterOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterClusterOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb3d9333ba783787329ccc3448a4f0650cb7011d91383cefa302f48d7b27bde3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f08c3b70b1cb00f3ff0d46fc21114d57c73d2cc8a22c5cabdad359fe9b759c3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableApplicationLogs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterClusterOperations]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterClusterOperations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterClusterOperations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c5be093a5db84c454ea0e8073e5c00f81f1dde780737d3ed33ea7ea3356cc10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterConfig",
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
class GoogleGkeonpremBareMetalClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        control_plane: typing.Union["GoogleGkeonpremBareMetalClusterControlPlane", typing.Dict[builtins.str, typing.Any]],
        load_balancer: typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancer", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        network_config: typing.Union["GoogleGkeonpremBareMetalClusterNetworkConfig", typing.Dict[builtins.str, typing.Any]],
        storage: typing.Union["GoogleGkeonpremBareMetalClusterStorage", typing.Dict[builtins.str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        binary_authorization: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_operations: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterClusterOperations, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        maintenance_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterMaintenanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_access_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterNodeAccessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        os_environment_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterOsEnvironmentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        proxy: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        security_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterSecurityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        upgrade_policy: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterUpgradePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param admin_cluster_membership: The Admin Cluster this Bare Metal User Cluster belongs to. This is the full resource name of the Admin Cluster's hub membership. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#admin_cluster_membership GoogleGkeonpremBareMetalCluster#admin_cluster_membership}
        :param bare_metal_version: A human readable description of this Bare Metal User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#bare_metal_version GoogleGkeonpremBareMetalCluster#bare_metal_version}
        :param control_plane: control_plane block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#control_plane GoogleGkeonpremBareMetalCluster#control_plane}
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#load_balancer GoogleGkeonpremBareMetalCluster#load_balancer}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#location GoogleGkeonpremBareMetalCluster#location}
        :param name: The bare metal cluster name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#name GoogleGkeonpremBareMetalCluster#name}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#network_config GoogleGkeonpremBareMetalCluster#network_config}
        :param storage: storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#storage GoogleGkeonpremBareMetalCluster#storage}
        :param annotations: Annotations on the Bare Metal User Cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#annotations GoogleGkeonpremBareMetalCluster#annotations}
        :param binary_authorization: binary_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#binary_authorization GoogleGkeonpremBareMetalCluster#binary_authorization}
        :param cluster_operations: cluster_operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#cluster_operations GoogleGkeonpremBareMetalCluster#cluster_operations}
        :param description: A human readable description of this Bare Metal User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#description GoogleGkeonpremBareMetalCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#id GoogleGkeonpremBareMetalCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintenance_config: maintenance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#maintenance_config GoogleGkeonpremBareMetalCluster#maintenance_config}
        :param node_access_config: node_access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_access_config GoogleGkeonpremBareMetalCluster#node_access_config}
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_config GoogleGkeonpremBareMetalCluster#node_config}
        :param os_environment_config: os_environment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#os_environment_config GoogleGkeonpremBareMetalCluster#os_environment_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#project GoogleGkeonpremBareMetalCluster#project}.
        :param proxy: proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#proxy GoogleGkeonpremBareMetalCluster#proxy}
        :param security_config: security_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#security_config GoogleGkeonpremBareMetalCluster#security_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#timeouts GoogleGkeonpremBareMetalCluster#timeouts}
        :param upgrade_policy: upgrade_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#upgrade_policy GoogleGkeonpremBareMetalCluster#upgrade_policy}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(control_plane, dict):
            control_plane = GoogleGkeonpremBareMetalClusterControlPlane(**control_plane)
        if isinstance(load_balancer, dict):
            load_balancer = GoogleGkeonpremBareMetalClusterLoadBalancer(**load_balancer)
        if isinstance(network_config, dict):
            network_config = GoogleGkeonpremBareMetalClusterNetworkConfig(**network_config)
        if isinstance(storage, dict):
            storage = GoogleGkeonpremBareMetalClusterStorage(**storage)
        if isinstance(binary_authorization, dict):
            binary_authorization = GoogleGkeonpremBareMetalClusterBinaryAuthorization(**binary_authorization)
        if isinstance(cluster_operations, dict):
            cluster_operations = GoogleGkeonpremBareMetalClusterClusterOperations(**cluster_operations)
        if isinstance(maintenance_config, dict):
            maintenance_config = GoogleGkeonpremBareMetalClusterMaintenanceConfig(**maintenance_config)
        if isinstance(node_access_config, dict):
            node_access_config = GoogleGkeonpremBareMetalClusterNodeAccessConfig(**node_access_config)
        if isinstance(node_config, dict):
            node_config = GoogleGkeonpremBareMetalClusterNodeConfig(**node_config)
        if isinstance(os_environment_config, dict):
            os_environment_config = GoogleGkeonpremBareMetalClusterOsEnvironmentConfig(**os_environment_config)
        if isinstance(proxy, dict):
            proxy = GoogleGkeonpremBareMetalClusterProxy(**proxy)
        if isinstance(security_config, dict):
            security_config = GoogleGkeonpremBareMetalClusterSecurityConfig(**security_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleGkeonpremBareMetalClusterTimeouts(**timeouts)
        if isinstance(upgrade_policy, dict):
            upgrade_policy = GoogleGkeonpremBareMetalClusterUpgradePolicy(**upgrade_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e57135b72ab24d98c14b4365df6e969b59e98126675d51a9faf4c0f83262799)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#admin_cluster_membership GoogleGkeonpremBareMetalCluster#admin_cluster_membership}
        '''
        result = self._values.get("admin_cluster_membership")
        assert result is not None, "Required property 'admin_cluster_membership' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bare_metal_version(self) -> builtins.str:
        '''A human readable description of this Bare Metal User Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#bare_metal_version GoogleGkeonpremBareMetalCluster#bare_metal_version}
        '''
        result = self._values.get("bare_metal_version")
        assert result is not None, "Required property 'bare_metal_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def control_plane(self) -> "GoogleGkeonpremBareMetalClusterControlPlane":
        '''control_plane block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#control_plane GoogleGkeonpremBareMetalCluster#control_plane}
        '''
        result = self._values.get("control_plane")
        assert result is not None, "Required property 'control_plane' is missing"
        return typing.cast("GoogleGkeonpremBareMetalClusterControlPlane", result)

    @builtins.property
    def load_balancer(self) -> "GoogleGkeonpremBareMetalClusterLoadBalancer":
        '''load_balancer block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#load_balancer GoogleGkeonpremBareMetalCluster#load_balancer}
        '''
        result = self._values.get("load_balancer")
        assert result is not None, "Required property 'load_balancer' is missing"
        return typing.cast("GoogleGkeonpremBareMetalClusterLoadBalancer", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#location GoogleGkeonpremBareMetalCluster#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The bare metal cluster name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#name GoogleGkeonpremBareMetalCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_config(self) -> "GoogleGkeonpremBareMetalClusterNetworkConfig":
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#network_config GoogleGkeonpremBareMetalCluster#network_config}
        '''
        result = self._values.get("network_config")
        assert result is not None, "Required property 'network_config' is missing"
        return typing.cast("GoogleGkeonpremBareMetalClusterNetworkConfig", result)

    @builtins.property
    def storage(self) -> "GoogleGkeonpremBareMetalClusterStorage":
        '''storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#storage GoogleGkeonpremBareMetalCluster#storage}
        '''
        result = self._values.get("storage")
        assert result is not None, "Required property 'storage' is missing"
        return typing.cast("GoogleGkeonpremBareMetalClusterStorage", result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#annotations GoogleGkeonpremBareMetalCluster#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def binary_authorization(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterBinaryAuthorization]:
        '''binary_authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#binary_authorization GoogleGkeonpremBareMetalCluster#binary_authorization}
        '''
        result = self._values.get("binary_authorization")
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterBinaryAuthorization], result)

    @builtins.property
    def cluster_operations(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterClusterOperations]:
        '''cluster_operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#cluster_operations GoogleGkeonpremBareMetalCluster#cluster_operations}
        '''
        result = self._values.get("cluster_operations")
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterClusterOperations], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human readable description of this Bare Metal User Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#description GoogleGkeonpremBareMetalCluster#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#id GoogleGkeonpremBareMetalCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterMaintenanceConfig"]:
        '''maintenance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#maintenance_config GoogleGkeonpremBareMetalCluster#maintenance_config}
        '''
        result = self._values.get("maintenance_config")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterMaintenanceConfig"], result)

    @builtins.property
    def node_access_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterNodeAccessConfig"]:
        '''node_access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_access_config GoogleGkeonpremBareMetalCluster#node_access_config}
        '''
        result = self._values.get("node_access_config")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterNodeAccessConfig"], result)

    @builtins.property
    def node_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterNodeConfig"]:
        '''node_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_config GoogleGkeonpremBareMetalCluster#node_config}
        '''
        result = self._values.get("node_config")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterNodeConfig"], result)

    @builtins.property
    def os_environment_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterOsEnvironmentConfig"]:
        '''os_environment_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#os_environment_config GoogleGkeonpremBareMetalCluster#os_environment_config}
        '''
        result = self._values.get("os_environment_config")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterOsEnvironmentConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#project GoogleGkeonpremBareMetalCluster#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy(self) -> typing.Optional["GoogleGkeonpremBareMetalClusterProxy"]:
        '''proxy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#proxy GoogleGkeonpremBareMetalCluster#proxy}
        '''
        result = self._values.get("proxy")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterProxy"], result)

    @builtins.property
    def security_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterSecurityConfig"]:
        '''security_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#security_config GoogleGkeonpremBareMetalCluster#security_config}
        '''
        result = self._values.get("security_config")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterSecurityConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleGkeonpremBareMetalClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#timeouts GoogleGkeonpremBareMetalCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterTimeouts"], result)

    @builtins.property
    def upgrade_policy(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterUpgradePolicy"]:
        '''upgrade_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#upgrade_policy GoogleGkeonpremBareMetalCluster#upgrade_policy}
        '''
        result = self._values.get("upgrade_policy")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterUpgradePolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterControlPlane",
    jsii_struct_bases=[],
    name_mapping={
        "control_plane_node_pool_config": "controlPlaneNodePoolConfig",
        "api_server_args": "apiServerArgs",
    },
)
class GoogleGkeonpremBareMetalClusterControlPlane:
    def __init__(
        self,
        *,
        control_plane_node_pool_config: typing.Union["GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig", typing.Dict[builtins.str, typing.Any]],
        api_server_args: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param control_plane_node_pool_config: control_plane_node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#control_plane_node_pool_config GoogleGkeonpremBareMetalCluster#control_plane_node_pool_config}
        :param api_server_args: api_server_args block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#api_server_args GoogleGkeonpremBareMetalCluster#api_server_args}
        '''
        if isinstance(control_plane_node_pool_config, dict):
            control_plane_node_pool_config = GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig(**control_plane_node_pool_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0671b966ed627b4e240b80e807ea5ff9eec9e5bd61b2e8e1199e5b84f17fe55)
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
    ) -> "GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig":
        '''control_plane_node_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#control_plane_node_pool_config GoogleGkeonpremBareMetalCluster#control_plane_node_pool_config}
        '''
        result = self._values.get("control_plane_node_pool_config")
        assert result is not None, "Required property 'control_plane_node_pool_config' is missing"
        return typing.cast("GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig", result)

    @builtins.property
    def api_server_args(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgs"]]]:
        '''api_server_args block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#api_server_args GoogleGkeonpremBareMetalCluster#api_server_args}
        '''
        result = self._values.get("api_server_args")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgs"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterControlPlane(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgs",
    jsii_struct_bases=[],
    name_mapping={"argument": "argument", "value": "value"},
)
class GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgs:
    def __init__(self, *, argument: builtins.str, value: builtins.str) -> None:
        '''
        :param argument: The argument name as it appears on the API Server command line please make sure to remove the leading dashes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#argument GoogleGkeonpremBareMetalCluster#argument}
        :param value: The value of the arg as it will be passed to the API Server command line. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#value GoogleGkeonpremBareMetalCluster#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96e0d6333e314c17c3d2e5139a437e854bc16526be051f6b86d8c432a88178e3)
            check_type(argname="argument argument", value=argument, expected_type=type_hints["argument"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "argument": argument,
            "value": value,
        }

    @builtins.property
    def argument(self) -> builtins.str:
        '''The argument name as it appears on the API Server command line please make sure to remove the leading dashes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#argument GoogleGkeonpremBareMetalCluster#argument}
        '''
        result = self._values.get("argument")
        assert result is not None, "Required property 'argument' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value of the arg as it will be passed to the API Server command line.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#value GoogleGkeonpremBareMetalCluster#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9199153fbe641f2857b6af73d11605eeb61ebef95e6ef95814b2256ec0e4b5c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cda8d167522b928ce8e5f4bcb8438f3d1bb9d805edfb6d58810e3827a81c9b5b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4075543c0398c2f7813102bba4fa807a4a0fe37e3b6a110499f9f79725f4433c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6514b05a7716128ad8e09baf7790b477d14fd93fd1a46bf0a26214923ee8a59b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8f6ce95adcc1b3c7db08e8c8ea13dfcdac87b3e11868fb6d2ad8661a08906cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92e45ed49a2085a664be0317edc5960f5d91de32db351d9db5f9ff130a55283b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e489e365658959a851d538da8f7f03716fe6bca79965d3fc8cdad8a6aff22423)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9692e33603b43033f6d4b7ee1816cea967f00e0ca025d1c4a06b22d5ca565de7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "argument", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b700515a4446545c1ffeafd6b3eb44c801c30785a58f64854ec8ad2fba9a334b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfadc4e510afef6793a53fb58ec1014f84b9f62f0900857961bcc835cc87a022)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig",
    jsii_struct_bases=[],
    name_mapping={"node_pool_config": "nodePoolConfig"},
)
class GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig:
    def __init__(
        self,
        *,
        node_pool_config: typing.Union["GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param node_pool_config: node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_pool_config GoogleGkeonpremBareMetalCluster#node_pool_config}
        '''
        if isinstance(node_pool_config, dict):
            node_pool_config = GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig(**node_pool_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db0dd7bfec9f46cd270d15b627d3373ed8155478e5d75523c98bae47809d2782)
            check_type(argname="argument node_pool_config", value=node_pool_config, expected_type=type_hints["node_pool_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "node_pool_config": node_pool_config,
        }

    @builtins.property
    def node_pool_config(
        self,
    ) -> "GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig":
        '''node_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_pool_config GoogleGkeonpremBareMetalCluster#node_pool_config}
        '''
        result = self._values.get("node_pool_config")
        assert result is not None, "Required property 'node_pool_config' is missing"
        return typing.cast("GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig",
    jsii_struct_bases=[],
    name_mapping={
        "labels": "labels",
        "node_configs": "nodeConfigs",
        "operating_system": "operatingSystem",
        "taints": "taints",
    },
)
class GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operating_system: typing.Optional[builtins.str] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#labels GoogleGkeonpremBareMetalCluster#labels}
        :param node_configs: node_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_configs GoogleGkeonpremBareMetalCluster#node_configs}
        :param operating_system: Specifies the nodes operating system (default: LINUX). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#operating_system GoogleGkeonpremBareMetalCluster#operating_system}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#taints GoogleGkeonpremBareMetalCluster#taints}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f2812487a9c42ecd4dbfeb7670f5fdb8f32728abb8a25fba35961b0339b7020)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#labels GoogleGkeonpremBareMetalCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def node_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs"]]]:
        '''node_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_configs GoogleGkeonpremBareMetalCluster#node_configs}
        '''
        result = self._values.get("node_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs"]]], result)

    @builtins.property
    def operating_system(self) -> typing.Optional[builtins.str]:
        '''Specifies the nodes operating system (default: LINUX).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#operating_system GoogleGkeonpremBareMetalCluster#operating_system}
        '''
        result = self._values.get("operating_system")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def taints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints"]]]:
        '''taints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#taints GoogleGkeonpremBareMetalCluster#taints}
        '''
        result = self._values.get("taints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels", "node_ip": "nodeIp"},
)
class GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_ip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#labels GoogleGkeonpremBareMetalCluster#labels}
        :param node_ip: The default IPv4 address for SSH access and Kubernetes node. Example: 192.168.0.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_ip GoogleGkeonpremBareMetalCluster#node_ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21fee69fe10deb8278249bac4ca78be98881a882e0ffc7535f873fbf24258e26)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#labels GoogleGkeonpremBareMetalCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def node_ip(self) -> typing.Optional[builtins.str]:
        '''The default IPv4 address for SSH access and Kubernetes node. Example: 192.168.0.1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_ip GoogleGkeonpremBareMetalCluster#node_ip}
        '''
        result = self._values.get("node_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb8c3270610cc1469c2150dc539c58ea6dda2ceadb7376df427a13e4d2f3b717)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bf84ddb06b21af5c368bb1f821b33b576fb4b44e5c71a109bd6f162080bb60f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ee3a2a4e7a16ecde3d349db460bd0ed8e6d0eab4febcaa9f30eafca27d806a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a046144a6194d2d8bac35979e178816f1b7e96feafa9de8a3744552487d673a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3473f36ddc49f495b7e18240e3c724a92aeadf01f4395ec4ba592c415965536)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f93568d3c9b2cd50291aad96ba3fe27e7a382a4cea4f0046cefd5393e31fbca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1fa94043467cd235ce99c92446e89688b49a3676ba81e32d3d1a10d58504666)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06de931c6bdc057a9af30fb1df595cd2a83a4e0caffae8dac65e5a3d969c9701)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeIp")
    def node_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeIp"))

    @node_ip.setter
    def node_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8bb89a1a6d858b1114d65e3b293c01e33fb806f354e25afb1bd76a19424d967)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__411ca47691cd871bb1f4138ab7e423c53dafbb973146deaddaa6d02ac02a061f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f83002c8b9cf2c6dd6e052b9206963d1e26a1959078e70a8bf9578db19e69f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodeConfigs")
    def put_node_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c52044b218c1e3580d89ddd1c5bb289d3759def3097980518d5f1317a4add1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeConfigs", [value]))

    @jsii.member(jsii_name="putTaints")
    def put_taints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__594537130a8e8784de579207827f1ee8fc8e4406b8a74963cf658c7e698339ea)
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
    ) -> GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsList:
        return typing.cast(GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsList, jsii.get(self, "nodeConfigs"))

    @builtins.property
    @jsii.member(jsii_name="taints")
    def taints(
        self,
    ) -> "GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsList":
        return typing.cast("GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsList", jsii.get(self, "taints"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]], jsii.get(self, "nodeConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="operatingSystemInput")
    def operating_system_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatingSystemInput"))

    @builtins.property
    @jsii.member(jsii_name="taintsInput")
    def taints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints"]]], jsii.get(self, "taintsInput"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ae3bcd0fd160c068a3b1bb2a5466f1fae0f24ea8e3585040b6f99339b036e2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operatingSystem")
    def operating_system(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operatingSystem"))

    @operating_system.setter
    def operating_system(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc1e858aa41289b6c1e993e5bcb8c1f46566a8a99c29081e960901c9a5046f84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operatingSystem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__109b2d9b6f9a9ba065034931a28e7776c6c8b3f8a76c976eef2b0d96d4deed1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints",
    jsii_struct_bases=[],
    name_mapping={"effect": "effect", "key": "key", "value": "value"},
)
class GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints:
    def __init__(
        self,
        *,
        effect: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param effect: Specifies the nodes operating system (default: LINUX). Possible values: ["EFFECT_UNSPECIFIED", "PREFER_NO_SCHEDULE", "NO_EXECUTE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#effect GoogleGkeonpremBareMetalCluster#effect}
        :param key: Key associated with the effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#key GoogleGkeonpremBareMetalCluster#key}
        :param value: Value associated with the effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#value GoogleGkeonpremBareMetalCluster#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b4e619f5c7702356a70d1560631d856222643782b9851ae6e57da8469801452)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#effect GoogleGkeonpremBareMetalCluster#effect}
        '''
        result = self._values.get("effect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Key associated with the effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#key GoogleGkeonpremBareMetalCluster#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value associated with the effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#value GoogleGkeonpremBareMetalCluster#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f069f41928ebfc9591d36b3ed0e9d03d4e0722c587852af68105f4cd4e25589)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58bc33ed346272a3c922f59aeba2af0d0700ce3c2a616c558ebeab3e189556a1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8329ee3236000646ec2f4d82ca804b10f8793bab0e46a0820e069ed745bd6ce9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02f61025c5cca6fdc1b2cbdec192b7c25bf7bc44aedd3d4857d8148e1dc87e91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c458c6265362daaa85a019eae69f3ebdbe312c6a8f313a75d224d55360f6ff45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af5cf1c65e025b8bac9d9df8152c0f50e9916e801960db68494d6cce81914216)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__707e22b2648e6cda005ee4fe9e3d392d66364c9a9a8bacde5ce257fff5d03720)
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
            type_hints = typing.get_type_hints(_typecheckingstub__791c6d612137cd9ac380d0082ef8160292f4fee4dca73de33ecdb033b058eb03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__769a270f449c1c1a5796b3c8699990510e960b4284d898db422d48f6ba896321)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b080db73b46f74b686e099812db28d1c801b2e6d1ade2dd4f29b6c29bb884b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b928db085dc98f4bc2dcb1e982c2086b52a9a14ea934a02577df2b6dac3beb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11aa3ca28ea51da1548e2f1449102fc72b2c2afe1b773d0eae2d97e500437335)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodePoolConfig")
    def put_node_pool_config(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
        operating_system: typing.Optional[builtins.str] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#labels GoogleGkeonpremBareMetalCluster#labels}
        :param node_configs: node_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_configs GoogleGkeonpremBareMetalCluster#node_configs}
        :param operating_system: Specifies the nodes operating system (default: LINUX). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#operating_system GoogleGkeonpremBareMetalCluster#operating_system}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#taints GoogleGkeonpremBareMetalCluster#taints}
        '''
        value = GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig(
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
    ) -> GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigOutputReference, jsii.get(self, "nodePoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodePoolConfigInput")
    def node_pool_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig], jsii.get(self, "nodePoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dbb639a323ebae16d4861642eaaa218bb04fefb903568dec9acce57f8e0c522)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterControlPlaneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterControlPlaneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a4658390850e18df81082215134d1448b1b79fcfc890127b1f515533d894860)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApiServerArgs")
    def put_api_server_args(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4efadee33fe8de04bd66e158711c897c53e5bc5def9aed7724c3d9f4c4a56b12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putApiServerArgs", [value]))

    @jsii.member(jsii_name="putControlPlaneNodePoolConfig")
    def put_control_plane_node_pool_config(
        self,
        *,
        node_pool_config: typing.Union[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param node_pool_config: node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_pool_config GoogleGkeonpremBareMetalCluster#node_pool_config}
        '''
        value = GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig(
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
    ) -> GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgsList:
        return typing.cast(GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgsList, jsii.get(self, "apiServerArgs"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneNodePoolConfig")
    def control_plane_node_pool_config(
        self,
    ) -> GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigOutputReference, jsii.get(self, "controlPlaneNodePoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="apiServerArgsInput")
    def api_server_args_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgs]]], jsii.get(self, "apiServerArgsInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneNodePoolConfigInput")
    def control_plane_node_pool_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig], jsii.get(self, "controlPlaneNodePoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterControlPlane]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterControlPlane], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterControlPlane],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8371dc3d6489b130362069bed4f608c0084f8537e6de983772f90bd3463e2cd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterFleet",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremBareMetalClusterFleet:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterFleet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterFleetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterFleetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22279408a8b5f24d79ba4748b7e93bdf9060f528cf2a994fceb59879d6067a03)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalClusterFleetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4285cc6fa5c299cd44ece314e3b12f7a7898f145cb2d852b38f12e36be59838)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalClusterFleetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dff0359e5677ec2ad39ce0af17a3c2b6545a0c23a15db3fba1dce54fc7d4c8bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a54442a51f3b88ec3199dfa9c932ff1ea2b73e3023560380e9c63edc4bd108a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdca7a316a5806facc1b42ca21e71602f8652751f472be3c2d88250abe3c6176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterFleetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterFleetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5f0c54eaf1c4a0e846aded1e8802d91c34f35a424232a8461313c237af31ddc)
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
    def internal_value(self) -> typing.Optional[GoogleGkeonpremBareMetalClusterFleet]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterFleet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterFleet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bd9dada5f44c4c902ead604d5577e5dcffaf8b7cc57eb5acf03b86d06fbe0d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancer",
    jsii_struct_bases=[],
    name_mapping={
        "port_config": "portConfig",
        "vip_config": "vipConfig",
        "bgp_lb_config": "bgpLbConfig",
        "manual_lb_config": "manualLbConfig",
        "metal_lb_config": "metalLbConfig",
    },
)
class GoogleGkeonpremBareMetalClusterLoadBalancer:
    def __init__(
        self,
        *,
        port_config: typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerPortConfig", typing.Dict[builtins.str, typing.Any]],
        vip_config: typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerVipConfig", typing.Dict[builtins.str, typing.Any]],
        bgp_lb_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        manual_lb_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerManualLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        metal_lb_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param port_config: port_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#port_config GoogleGkeonpremBareMetalCluster#port_config}
        :param vip_config: vip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#vip_config GoogleGkeonpremBareMetalCluster#vip_config}
        :param bgp_lb_config: bgp_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#bgp_lb_config GoogleGkeonpremBareMetalCluster#bgp_lb_config}
        :param manual_lb_config: manual_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#manual_lb_config GoogleGkeonpremBareMetalCluster#manual_lb_config}
        :param metal_lb_config: metal_lb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#metal_lb_config GoogleGkeonpremBareMetalCluster#metal_lb_config}
        '''
        if isinstance(port_config, dict):
            port_config = GoogleGkeonpremBareMetalClusterLoadBalancerPortConfig(**port_config)
        if isinstance(vip_config, dict):
            vip_config = GoogleGkeonpremBareMetalClusterLoadBalancerVipConfig(**vip_config)
        if isinstance(bgp_lb_config, dict):
            bgp_lb_config = GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfig(**bgp_lb_config)
        if isinstance(manual_lb_config, dict):
            manual_lb_config = GoogleGkeonpremBareMetalClusterLoadBalancerManualLbConfig(**manual_lb_config)
        if isinstance(metal_lb_config, dict):
            metal_lb_config = GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfig(**metal_lb_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d855bca14c376091eff156e16b603e97bc6c09eb9e18259de2a2b1aef1fd66dc)
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
    def port_config(self) -> "GoogleGkeonpremBareMetalClusterLoadBalancerPortConfig":
        '''port_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#port_config GoogleGkeonpremBareMetalCluster#port_config}
        '''
        result = self._values.get("port_config")
        assert result is not None, "Required property 'port_config' is missing"
        return typing.cast("GoogleGkeonpremBareMetalClusterLoadBalancerPortConfig", result)

    @builtins.property
    def vip_config(self) -> "GoogleGkeonpremBareMetalClusterLoadBalancerVipConfig":
        '''vip_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#vip_config GoogleGkeonpremBareMetalCluster#vip_config}
        '''
        result = self._values.get("vip_config")
        assert result is not None, "Required property 'vip_config' is missing"
        return typing.cast("GoogleGkeonpremBareMetalClusterLoadBalancerVipConfig", result)

    @builtins.property
    def bgp_lb_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfig"]:
        '''bgp_lb_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#bgp_lb_config GoogleGkeonpremBareMetalCluster#bgp_lb_config}
        '''
        result = self._values.get("bgp_lb_config")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfig"], result)

    @builtins.property
    def manual_lb_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterLoadBalancerManualLbConfig"]:
        '''manual_lb_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#manual_lb_config GoogleGkeonpremBareMetalCluster#manual_lb_config}
        '''
        result = self._values.get("manual_lb_config")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterLoadBalancerManualLbConfig"], result)

    @builtins.property
    def metal_lb_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfig"]:
        '''metal_lb_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#metal_lb_config GoogleGkeonpremBareMetalCluster#metal_lb_config}
        '''
        result = self._values.get("metal_lb_config")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterLoadBalancer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfig",
    jsii_struct_bases=[],
    name_mapping={
        "address_pools": "addressPools",
        "asn": "asn",
        "bgp_peer_configs": "bgpPeerConfigs",
        "load_balancer_node_pool_config": "loadBalancerNodePoolConfig",
    },
)
class GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfig:
    def __init__(
        self,
        *,
        address_pools: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools", typing.Dict[builtins.str, typing.Any]]]],
        asn: jsii.Number,
        bgp_peer_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs", typing.Dict[builtins.str, typing.Any]]]],
        load_balancer_node_pool_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param address_pools: address_pools block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#address_pools GoogleGkeonpremBareMetalCluster#address_pools}
        :param asn: BGP autonomous system number (ASN) of the cluster. This field can be updated after cluster creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#asn GoogleGkeonpremBareMetalCluster#asn}
        :param bgp_peer_configs: bgp_peer_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#bgp_peer_configs GoogleGkeonpremBareMetalCluster#bgp_peer_configs}
        :param load_balancer_node_pool_config: load_balancer_node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#load_balancer_node_pool_config GoogleGkeonpremBareMetalCluster#load_balancer_node_pool_config}
        '''
        if isinstance(load_balancer_node_pool_config, dict):
            load_balancer_node_pool_config = GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig(**load_balancer_node_pool_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be7ffeb00433c163d93c5c4129c1d6d9f07ea05d1cf2a4065d116bb56cd69e21)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools"]]:
        '''address_pools block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#address_pools GoogleGkeonpremBareMetalCluster#address_pools}
        '''
        result = self._values.get("address_pools")
        assert result is not None, "Required property 'address_pools' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools"]], result)

    @builtins.property
    def asn(self) -> jsii.Number:
        '''BGP autonomous system number (ASN) of the cluster. This field can be updated after cluster creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#asn GoogleGkeonpremBareMetalCluster#asn}
        '''
        result = self._values.get("asn")
        assert result is not None, "Required property 'asn' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def bgp_peer_configs(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs"]]:
        '''bgp_peer_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#bgp_peer_configs GoogleGkeonpremBareMetalCluster#bgp_peer_configs}
        '''
        result = self._values.get("bgp_peer_configs")
        assert result is not None, "Required property 'bgp_peer_configs' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs"]], result)

    @builtins.property
    def load_balancer_node_pool_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig"]:
        '''load_balancer_node_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#load_balancer_node_pool_config GoogleGkeonpremBareMetalCluster#load_balancer_node_pool_config}
        '''
        result = self._values.get("load_balancer_node_pool_config")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools",
    jsii_struct_bases=[],
    name_mapping={
        "addresses": "addresses",
        "pool": "pool",
        "avoid_buggy_ips": "avoidBuggyIps",
        "manual_assign": "manualAssign",
    },
)
class GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools:
    def __init__(
        self,
        *,
        addresses: typing.Sequence[builtins.str],
        pool: builtins.str,
        avoid_buggy_ips: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        manual_assign: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param addresses: The addresses that are part of this pool. Each address must be either in the CIDR form (1.2.3.0/24) or range form (1.2.3.1-1.2.3.5). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#addresses GoogleGkeonpremBareMetalCluster#addresses}
        :param pool: The name of the address pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#pool GoogleGkeonpremBareMetalCluster#pool}
        :param avoid_buggy_ips: If true, avoid using IPs ending in .0 or .255. This avoids buggy consumer devices mistakenly dropping IPv4 traffic for those special IP addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#avoid_buggy_ips GoogleGkeonpremBareMetalCluster#avoid_buggy_ips}
        :param manual_assign: If true, prevent IP addresses from being automatically assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#manual_assign GoogleGkeonpremBareMetalCluster#manual_assign}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d304c97fff7acbfe19df5bde5feda498c71ac25e54141dcc122ac96e1325fcb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#addresses GoogleGkeonpremBareMetalCluster#addresses}
        '''
        result = self._values.get("addresses")
        assert result is not None, "Required property 'addresses' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def pool(self) -> builtins.str:
        '''The name of the address pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#pool GoogleGkeonpremBareMetalCluster#pool}
        '''
        result = self._values.get("pool")
        assert result is not None, "Required property 'pool' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def avoid_buggy_ips(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, avoid using IPs ending in .0 or .255. This avoids buggy consumer devices mistakenly dropping IPv4 traffic for those special IP addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#avoid_buggy_ips GoogleGkeonpremBareMetalCluster#avoid_buggy_ips}
        '''
        result = self._values.get("avoid_buggy_ips")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def manual_assign(self) -> typing.Optional[builtins.str]:
        '''If true, prevent IP addresses from being automatically assigned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#manual_assign GoogleGkeonpremBareMetalCluster#manual_assign}
        '''
        result = self._values.get("manual_assign")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPoolsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPoolsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb4eba457d64ae2363406a05e820977c21c0de27702d3b960d8176171e74a61b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPoolsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5635e88bc6756f4f979c22fd30520654f3afb78815630f37d86c91028faba2a2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPoolsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb02bba5f6c27b0f261cee82347a0e5abcc13d52e5da57ca08caf5239675a835)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6841d92728488a40fbd807b3ddbf9b660c4961d2ec1268c84994cda1d33d6466)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2753ff01833e882a853934a070845f3f6dfa2ef9f660fb350aea71875d97ed42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dd99c410ea3692ea8e94e241280289ef6f3c03558791c7248b92ae183cdbde7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPoolsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPoolsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b308d2c0f56308dd9163706859cf530da6a264708707d55e1ec09e09a3ad720)
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
    def manual_assign_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "manualAssignInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d04b412e5db1f43606636818bba1afecefde3ba7376322dc5e250f2af3476847)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b59f0a30e7228fc0ede28c1a89a567385c49b0e3bb643cbbae44cc03c325baf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "avoidBuggyIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="manualAssign")
    def manual_assign(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "manualAssign"))

    @manual_assign.setter
    def manual_assign(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20e4e5e3f9d2251c2ae883b2390c8688a3be4461b7876a0251eafcbea60bae83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manualAssign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pool")
    def pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pool"))

    @pool.setter
    def pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59c9029e5111613555090ba81dfc832c4682bb329e6e05308dc1fe4be6222622)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32e2b7bd68345b9e10c0dc89830dfcf13ec264f3bdc15578f74b81d91f02dfb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "asn": "asn",
        "ip_address": "ipAddress",
        "control_plane_nodes": "controlPlaneNodes",
    },
)
class GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs:
    def __init__(
        self,
        *,
        asn: jsii.Number,
        ip_address: builtins.str,
        control_plane_nodes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param asn: BGP autonomous system number (ASN) for the network that contains the external peer device. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#asn GoogleGkeonpremBareMetalCluster#asn}
        :param ip_address: The IP address of the external peer device. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#ip_address GoogleGkeonpremBareMetalCluster#ip_address}
        :param control_plane_nodes: The IP address of the control plane node that connects to the external peer. If you don't specify any control plane nodes, all control plane nodes can connect to the external peer. If you specify one or more IP addresses, only the nodes specified participate in peering sessions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#control_plane_nodes GoogleGkeonpremBareMetalCluster#control_plane_nodes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__723b92ad16b1e9e554edc991ec438ebfca7f35275cc93ef7c21196766456b13c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#asn GoogleGkeonpremBareMetalCluster#asn}
        '''
        result = self._values.get("asn")
        assert result is not None, "Required property 'asn' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def ip_address(self) -> builtins.str:
        '''The IP address of the external peer device.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#ip_address GoogleGkeonpremBareMetalCluster#ip_address}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#control_plane_nodes GoogleGkeonpremBareMetalCluster#control_plane_nodes}
        '''
        result = self._values.get("control_plane_nodes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe5ace4a066aac7ffb8c35e27f2341e839e2a589ca40046e66f11b0bf95e1523)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbfec941e164c31d4e607dce9068b99fe61ed3124d58cad1b91c9bee65833dad)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3fdb0a332653a41502df0cc2103c78c33366188aece403d1abf09cb9795736a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69cd091275b18821db4d64ad881e25b904930401f517dab59cc1402658fc8c2f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cce88a891ed2690c4730d5ae15478a0b78d563ba43a0b23ca3f6e0820312277)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ba194fc3e6d3c66cfd9023b2a30438c7b1f8caa0fa1bd415bef0a16ead901b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87d9c2fa3a9d846693cb911bfe190048441841d01c881c556be3a6c72291b2ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b18944f2f48a5c02ba3bc43fba428fd2db59b22e1f0ddc3108cf7dfbebc25522)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "asn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="controlPlaneNodes")
    def control_plane_nodes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "controlPlaneNodes"))

    @control_plane_nodes.setter
    def control_plane_nodes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7ac6aef3e2ef6ab78c43dbb1f33aa0fbc8f37f38cc7f3093a16dd3a616e36db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneNodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dd61dcab9f652f00ae91f7a2b80cf1407f2edca0148a2e55186e0cdf4fa8865)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cad854122b565810d2d2d7c1876e1d44b5ea3f6b3459fd7a5a7dec94c49140ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig",
    jsii_struct_bases=[],
    name_mapping={"node_pool_config": "nodePoolConfig"},
)
class GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig:
    def __init__(
        self,
        *,
        node_pool_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param node_pool_config: node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_pool_config GoogleGkeonpremBareMetalCluster#node_pool_config}
        '''
        if isinstance(node_pool_config, dict):
            node_pool_config = GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig(**node_pool_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b0f7a02f7b7a00ede73b37b8f58d40aab0d62b7ed4f37353b4c1443bce25e2b)
            check_type(argname="argument node_pool_config", value=node_pool_config, expected_type=type_hints["node_pool_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if node_pool_config is not None:
            self._values["node_pool_config"] = node_pool_config

    @builtins.property
    def node_pool_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig"]:
        '''node_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_pool_config GoogleGkeonpremBareMetalCluster#node_pool_config}
        '''
        result = self._values.get("node_pool_config")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig",
    jsii_struct_bases=[],
    name_mapping={
        "kubelet_config": "kubeletConfig",
        "labels": "labels",
        "node_configs": "nodeConfigs",
        "operating_system": "operatingSystem",
        "taints": "taints",
    },
)
class GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig:
    def __init__(
        self,
        *,
        kubelet_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operating_system: typing.Optional[builtins.str] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param kubelet_config: kubelet_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#kubelet_config GoogleGkeonpremBareMetalCluster#kubelet_config}
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#labels GoogleGkeonpremBareMetalCluster#labels}
        :param node_configs: node_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_configs GoogleGkeonpremBareMetalCluster#node_configs}
        :param operating_system: Specifies the nodes operating system (default: LINUX). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#operating_system GoogleGkeonpremBareMetalCluster#operating_system}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#taints GoogleGkeonpremBareMetalCluster#taints}
        '''
        if isinstance(kubelet_config, dict):
            kubelet_config = GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig(**kubelet_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e7c3c370de39cfcd10ef0bb9871bac334799556923a0739dfba62f09c3afa26)
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
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig"]:
        '''kubelet_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#kubelet_config GoogleGkeonpremBareMetalCluster#kubelet_config}
        '''
        result = self._values.get("kubelet_config")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig"], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#labels GoogleGkeonpremBareMetalCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def node_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs"]]]:
        '''node_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_configs GoogleGkeonpremBareMetalCluster#node_configs}
        '''
        result = self._values.get("node_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs"]]], result)

    @builtins.property
    def operating_system(self) -> typing.Optional[builtins.str]:
        '''Specifies the nodes operating system (default: LINUX).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#operating_system GoogleGkeonpremBareMetalCluster#operating_system}
        '''
        result = self._values.get("operating_system")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def taints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints"]]]:
        '''taints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#taints GoogleGkeonpremBareMetalCluster#taints}
        '''
        result = self._values.get("taints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig",
    jsii_struct_bases=[],
    name_mapping={
        "registry_burst": "registryBurst",
        "registry_pull_qps": "registryPullQps",
        "serialize_image_pulls_disabled": "serializeImagePullsDisabled",
    },
)
class GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig:
    def __init__(
        self,
        *,
        registry_burst: typing.Optional[jsii.Number] = None,
        registry_pull_qps: typing.Optional[jsii.Number] = None,
        serialize_image_pulls_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param registry_burst: The maximum size of bursty pulls, temporarily allows pulls to burst to this number, while still not exceeding registry_pull_qps. The value must not be a negative number. Updating this field may impact scalability by changing the amount of traffic produced by image pulls. Defaults to 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#registry_burst GoogleGkeonpremBareMetalCluster#registry_burst}
        :param registry_pull_qps: The limit of registry pulls per second. Setting this value to 0 means no limit. Updating this field may impact scalability by changing the amount of traffic produced by image pulls. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#registry_pull_qps GoogleGkeonpremBareMetalCluster#registry_pull_qps}
        :param serialize_image_pulls_disabled: Prevents the Kubelet from pulling multiple images at a time. We recommend *not* changing the default value on nodes that run docker daemon with version < 1.9 or an Another Union File System (Aufs) storage backend. Issue https://github.com/kubernetes/kubernetes/issues/10959 has more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#serialize_image_pulls_disabled GoogleGkeonpremBareMetalCluster#serialize_image_pulls_disabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64f0ff29c5f108a5adcc2238b068e64025e5223e71d9c1cbcda26175a46655c0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#registry_burst GoogleGkeonpremBareMetalCluster#registry_burst}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#registry_pull_qps GoogleGkeonpremBareMetalCluster#registry_pull_qps}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#serialize_image_pulls_disabled GoogleGkeonpremBareMetalCluster#serialize_image_pulls_disabled}
        '''
        result = self._values.get("serialize_image_pulls_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ca65614485c3443e093341ff96db6877e8a1f372bd27b39ed90e75beb8efd14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__560dbbaff2a4d4ff23e63c552c3502e2bd804b00d7148019239d11c3f53d81c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registryBurst", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="registryPullQps")
    def registry_pull_qps(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "registryPullQps"))

    @registry_pull_qps.setter
    def registry_pull_qps(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cbf179a875ee38e015dd966b3fa5bafcab20b9f647d9c981db43eb187278fd7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2a3b8d13cfda718f63a282d4f00cbbc8ffa19fabd6b042288f6dfacb04720c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serializeImagePullsDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d143eb4e8b72518bafda4773a736403cc9c56c8959bf3603718fb1a8e226946a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels", "node_ip": "nodeIp"},
)
class GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_ip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#labels GoogleGkeonpremBareMetalCluster#labels}
        :param node_ip: The default IPv4 address for SSH access and Kubernetes node. Example: 192.168.0.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_ip GoogleGkeonpremBareMetalCluster#node_ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__895729f2f8823d9de5f9a516cc3ddcbf47391a268df45197abb619fd7675bdc0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#labels GoogleGkeonpremBareMetalCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def node_ip(self) -> typing.Optional[builtins.str]:
        '''The default IPv4 address for SSH access and Kubernetes node. Example: 192.168.0.1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_ip GoogleGkeonpremBareMetalCluster#node_ip}
        '''
        result = self._values.get("node_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18681dc0b543dadb47e63ba97b8f83dcebaf1b70df0cc0a817887af8c8a4f6fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a264b8bd820979ad7ccf8824b163809370101019db0067e2c54ed1a166abea35)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41169e65e60a7f3d457e91506636961758c4dbb4cfecad81ecb6d9ea9ad5ae3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65e160c3f6cf93ef485eca8ebca1b3c6b37bcdf21deb098cf95399e6ee5a8cf3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__99e6b65cd683a831e7b2102ff4a0555156428a3267229b121be7f4f6d1f95b64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72a23cbbe7c4e3436bd3d6322cd3775d812d81248c87612041a480abf423cb25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53d98fb2fcf65fb6f1796cccba773569d6a5b82958267a43d99b64c2e0c48d52)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1eea615e9ee87dda18fd15a3d203345e96cfd9666dada68275679012a8b3507a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeIp")
    def node_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeIp"))

    @node_ip.setter
    def node_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efd8c6d9cb201c6766d4619d93aa16a985f24649f1b2741a12d170c7b0cbdf3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f89025b70decf4ed2cb2e6adfea23d1acfb8240849ebb7e5b5cd0e9d812277)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e866a8c0c34fb91cc639f63f3cc3e2d82743a07ed3d97bfbee90841df932e7b)
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
        :param registry_burst: The maximum size of bursty pulls, temporarily allows pulls to burst to this number, while still not exceeding registry_pull_qps. The value must not be a negative number. Updating this field may impact scalability by changing the amount of traffic produced by image pulls. Defaults to 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#registry_burst GoogleGkeonpremBareMetalCluster#registry_burst}
        :param registry_pull_qps: The limit of registry pulls per second. Setting this value to 0 means no limit. Updating this field may impact scalability by changing the amount of traffic produced by image pulls. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#registry_pull_qps GoogleGkeonpremBareMetalCluster#registry_pull_qps}
        :param serialize_image_pulls_disabled: Prevents the Kubelet from pulling multiple images at a time. We recommend *not* changing the default value on nodes that run docker daemon with version < 1.9 or an Another Union File System (Aufs) storage backend. Issue https://github.com/kubernetes/kubernetes/issues/10959 has more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#serialize_image_pulls_disabled GoogleGkeonpremBareMetalCluster#serialize_image_pulls_disabled}
        '''
        value = GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig(
            registry_burst=registry_burst,
            registry_pull_qps=registry_pull_qps,
            serialize_image_pulls_disabled=serialize_image_pulls_disabled,
        )

        return typing.cast(None, jsii.invoke(self, "putKubeletConfig", [value]))

    @jsii.member(jsii_name="putNodeConfigs")
    def put_node_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579a22421bae9a5af4a0d5f620465a4cd62719f525f0178dd054451907a08b1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeConfigs", [value]))

    @jsii.member(jsii_name="putTaints")
    def put_taints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6047a7ce9f5c065e65ce48ac61097ca93d128341c6e814f8432c5029cbcc23e5)
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
    ) -> GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfigOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfigOutputReference, jsii.get(self, "kubeletConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfigs")
    def node_configs(
        self,
    ) -> GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsList:
        return typing.cast(GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsList, jsii.get(self, "nodeConfigs"))

    @builtins.property
    @jsii.member(jsii_name="taints")
    def taints(
        self,
    ) -> "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsList":
        return typing.cast("GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsList", jsii.get(self, "taints"))

    @builtins.property
    @jsii.member(jsii_name="kubeletConfigInput")
    def kubelet_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig], jsii.get(self, "kubeletConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]], jsii.get(self, "nodeConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="operatingSystemInput")
    def operating_system_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatingSystemInput"))

    @builtins.property
    @jsii.member(jsii_name="taintsInput")
    def taints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints"]]], jsii.get(self, "taintsInput"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f23ef65e2f88ccc379def9d731360920fbd36cfed27474f936ac643aadb6a50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operatingSystem")
    def operating_system(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operatingSystem"))

    @operating_system.setter
    def operating_system(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ba658d86c01cd3f4e3d0dbc22b710b8ee6c13c853bb2637d930a6dc0357eda3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operatingSystem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e628a15a0ade9bff2d85dde0a609c5bf01dad9b6a2b287b61491ffa7cc24ec36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints",
    jsii_struct_bases=[],
    name_mapping={"effect": "effect", "key": "key", "value": "value"},
)
class GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints:
    def __init__(
        self,
        *,
        effect: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param effect: Specifies the nodes operating system (default: LINUX). Possible values: ["EFFECT_UNSPECIFIED", "PREFER_NO_SCHEDULE", "NO_EXECUTE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#effect GoogleGkeonpremBareMetalCluster#effect}
        :param key: Key associated with the effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#key GoogleGkeonpremBareMetalCluster#key}
        :param value: Value associated with the effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#value GoogleGkeonpremBareMetalCluster#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2126f2f0f6314a52ea00e2cd101d5ef071d6ead7b5f2e995a81a35a9ed61154)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#effect GoogleGkeonpremBareMetalCluster#effect}
        '''
        result = self._values.get("effect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Key associated with the effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#key GoogleGkeonpremBareMetalCluster#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value associated with the effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#value GoogleGkeonpremBareMetalCluster#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50f9954d5d360fa79ab25e5357bb70bb6a974e733c150e111f11539a537ed4bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11ab82c55005c65b100abd9f8ff5977750696b6ab3e29575660cb61fc738645f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed79692107c5087bf53e301b9bafc40e4dc06924b13c87a1213dee05235c811d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e67812ffb3412943026b8f2b1f40edb630b9159a0f87286f392bb753526ffad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6dab0efce4c40f1c4bdc9bd62a3a7677904bbe79580cd747d318a13a3b83c09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0889762c980e9a230b124b96a82178176c51d738a87ea736e408bc45368ddb12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ed2756a8539e555fbb41aebe4f74f037656f4f1adff9e6bad6bd833c411d570)
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
            type_hints = typing.get_type_hints(_typecheckingstub__250a5a5c9e39fc7fb47a69aa4dfb16104bbb42aa85ebb61ff22161b9726847ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__443ef3a7238c2264b7833336351041192a508ed97426903164c8a47c19a94d98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0476c9fab66fc33b0266cb0ee8be867ae60372f9e5cb39753e7fe8e38d1d26f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fa3ee2900b68738ce08c9cff8475c0613ac6e5f302c23f18be83ea565423b17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b98c2a878074cc365f527ea6b7b6e58441cd099d20da7cc8603cf2c3778d257f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodePoolConfig")
    def put_node_pool_config(
        self,
        *,
        kubelet_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
        operating_system: typing.Optional[builtins.str] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param kubelet_config: kubelet_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#kubelet_config GoogleGkeonpremBareMetalCluster#kubelet_config}
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#labels GoogleGkeonpremBareMetalCluster#labels}
        :param node_configs: node_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_configs GoogleGkeonpremBareMetalCluster#node_configs}
        :param operating_system: Specifies the nodes operating system (default: LINUX). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#operating_system GoogleGkeonpremBareMetalCluster#operating_system}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#taints GoogleGkeonpremBareMetalCluster#taints}
        '''
        value = GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig(
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
    ) -> GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigOutputReference, jsii.get(self, "nodePoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodePoolConfigInput")
    def node_pool_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig], jsii.get(self, "nodePoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17d9c9e7ad32cd6001a98ca1912e5c2070bb3e3a49351c395987d3a8172a6c14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93319d1f1fea3a629368a2bf3bf5790a64c5688577e5a9a8682acc368a98faeb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAddressPools")
    def put_address_pools(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c6853e1b417d005ab339af4c56bb568261a9ce60b5b34b15f0c975d3cf5d7ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAddressPools", [value]))

    @jsii.member(jsii_name="putBgpPeerConfigs")
    def put_bgp_peer_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84cf1950569c75eec27a075c01eecc5db13fdb9db77f0163af07d8b5028ebc15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBgpPeerConfigs", [value]))

    @jsii.member(jsii_name="putLoadBalancerNodePoolConfig")
    def put_load_balancer_node_pool_config(
        self,
        *,
        node_pool_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param node_pool_config: node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_pool_config GoogleGkeonpremBareMetalCluster#node_pool_config}
        '''
        value = GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig(
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
    ) -> GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPoolsList:
        return typing.cast(GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPoolsList, jsii.get(self, "addressPools"))

    @builtins.property
    @jsii.member(jsii_name="bgpPeerConfigs")
    def bgp_peer_configs(
        self,
    ) -> GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigsList:
        return typing.cast(GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigsList, jsii.get(self, "bgpPeerConfigs"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerNodePoolConfig")
    def load_balancer_node_pool_config(
        self,
    ) -> GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigOutputReference, jsii.get(self, "loadBalancerNodePoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="addressPoolsInput")
    def address_pools_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools]]], jsii.get(self, "addressPoolsInput"))

    @builtins.property
    @jsii.member(jsii_name="asnInput")
    def asn_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "asnInput"))

    @builtins.property
    @jsii.member(jsii_name="bgpPeerConfigsInput")
    def bgp_peer_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs]]], jsii.get(self, "bgpPeerConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerNodePoolConfigInput")
    def load_balancer_node_pool_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig], jsii.get(self, "loadBalancerNodePoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="asn")
    def asn(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "asn"))

    @asn.setter
    def asn(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9cd5d95221a6d28473297876afb3c8412913b291e5d80d6b539ddfd7c5875a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "asn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7553e6c9812609886b5811053a5ed57c2c4155a0d81239753b69a94fc48286c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerManualLbConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleGkeonpremBareMetalClusterLoadBalancerManualLbConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether manual load balancing is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#enabled GoogleGkeonpremBareMetalCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d43ad893b0309dbc091651ea286f50c1dd77af915ee980926f51dce2ec48ff12)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether manual load balancing is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#enabled GoogleGkeonpremBareMetalCluster#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterLoadBalancerManualLbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterLoadBalancerManualLbConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerManualLbConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__958b2dfde134d336e25b8ad7a3d275e459c5e268170b3fa1ef088daed2f12c17)
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
            type_hints = typing.get_type_hints(_typecheckingstub__980eaa7eb0c1c64ae4a180584450f423fd6c7030da0bc846cd30e70f6db8ed04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerManualLbConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerManualLbConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerManualLbConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4d2ef11282875fdfc9f0abce6dab210bd44a8ab7f01bbdef3a9958f9b4bd84f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfig",
    jsii_struct_bases=[],
    name_mapping={
        "address_pools": "addressPools",
        "load_balancer_node_pool_config": "loadBalancerNodePoolConfig",
    },
)
class GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfig:
    def __init__(
        self,
        *,
        address_pools: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools", typing.Dict[builtins.str, typing.Any]]]],
        load_balancer_node_pool_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param address_pools: address_pools block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#address_pools GoogleGkeonpremBareMetalCluster#address_pools}
        :param load_balancer_node_pool_config: load_balancer_node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#load_balancer_node_pool_config GoogleGkeonpremBareMetalCluster#load_balancer_node_pool_config}
        '''
        if isinstance(load_balancer_node_pool_config, dict):
            load_balancer_node_pool_config = GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig(**load_balancer_node_pool_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25cee9680c23abaf06c224eecb97c6052474b6d2c4671540c628e63875075d09)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools"]]:
        '''address_pools block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#address_pools GoogleGkeonpremBareMetalCluster#address_pools}
        '''
        result = self._values.get("address_pools")
        assert result is not None, "Required property 'address_pools' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools"]], result)

    @builtins.property
    def load_balancer_node_pool_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig"]:
        '''load_balancer_node_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#load_balancer_node_pool_config GoogleGkeonpremBareMetalCluster#load_balancer_node_pool_config}
        '''
        result = self._values.get("load_balancer_node_pool_config")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools",
    jsii_struct_bases=[],
    name_mapping={
        "addresses": "addresses",
        "pool": "pool",
        "avoid_buggy_ips": "avoidBuggyIps",
        "manual_assign": "manualAssign",
    },
)
class GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools:
    def __init__(
        self,
        *,
        addresses: typing.Sequence[builtins.str],
        pool: builtins.str,
        avoid_buggy_ips: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        manual_assign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param addresses: The addresses that are part of this pool. Each address must be either in the CIDR form (1.2.3.0/24) or range form (1.2.3.1-1.2.3.5). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#addresses GoogleGkeonpremBareMetalCluster#addresses}
        :param pool: The name of the address pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#pool GoogleGkeonpremBareMetalCluster#pool}
        :param avoid_buggy_ips: If true, avoid using IPs ending in .0 or .255. This avoids buggy consumer devices mistakenly dropping IPv4 traffic for those special IP addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#avoid_buggy_ips GoogleGkeonpremBareMetalCluster#avoid_buggy_ips}
        :param manual_assign: If true, prevent IP addresses from being automatically assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#manual_assign GoogleGkeonpremBareMetalCluster#manual_assign}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bea8fac4b1c38260b701dc2b6173d555d42507338503e48095f4480efffd6215)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#addresses GoogleGkeonpremBareMetalCluster#addresses}
        '''
        result = self._values.get("addresses")
        assert result is not None, "Required property 'addresses' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def pool(self) -> builtins.str:
        '''The name of the address pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#pool GoogleGkeonpremBareMetalCluster#pool}
        '''
        result = self._values.get("pool")
        assert result is not None, "Required property 'pool' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def avoid_buggy_ips(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, avoid using IPs ending in .0 or .255. This avoids buggy consumer devices mistakenly dropping IPv4 traffic for those special IP addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#avoid_buggy_ips GoogleGkeonpremBareMetalCluster#avoid_buggy_ips}
        '''
        result = self._values.get("avoid_buggy_ips")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def manual_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, prevent IP addresses from being automatically assigned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#manual_assign GoogleGkeonpremBareMetalCluster#manual_assign}
        '''
        result = self._values.get("manual_assign")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPoolsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPoolsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53089bbd1d94ef8ea8bd3eb0989fd8efc1149c34550ebcb1b3816d428bc5af40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPoolsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eebe6f984713d18cea1bb22d63f9e9c304ea83187b511d88c2cc29137d799957)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPoolsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fca6a6c2f22862e4501e2a8f7bd075f782d6493a6cc55a77ba3b4c4ff23a5f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8ba596e0cbf15d6d791ffade0a1cd1d44046f49890c5c0f54ea5139fc92a4df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20d4aa9cad4107e999588c48bc6a3197dd0e39ca989f9041de035fed70c4579a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06173b64e0dd4171ed1057c6fe2afe71761b961f4b040c6b0e427209155f863b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPoolsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPoolsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__869ccaebd509f7e2b9e51b7cc4d0e41c9bc5b7305e6210f50fb20c2a885c746f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9db322bed31c2ab9b8119b3cdf386b3c4d921a33fb4229d291f75cf049d3cc5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a592b2ac51997c812db4d4e0d44e635ff616a630bd973c50e4bf8debb893a4ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f90986e5e1149fb1344359770c156288b218120ff0b998233a300f5798ccbdb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manualAssign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pool")
    def pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pool"))

    @pool.setter
    def pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23787282a7eb607e13e5e65ce997846c3d8d18dad724235064557807dc0541dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67e06696f49a2bbd383847deb4b8ec0642123545a260e2e3fa6f145e7a202ab9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig",
    jsii_struct_bases=[],
    name_mapping={"node_pool_config": "nodePoolConfig"},
)
class GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig:
    def __init__(
        self,
        *,
        node_pool_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param node_pool_config: node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_pool_config GoogleGkeonpremBareMetalCluster#node_pool_config}
        '''
        if isinstance(node_pool_config, dict):
            node_pool_config = GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig(**node_pool_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95177e6ebf4efbab8604701cd09876b0ae2fc6c6878cfed14a518a3f4fb0e949)
            check_type(argname="argument node_pool_config", value=node_pool_config, expected_type=type_hints["node_pool_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if node_pool_config is not None:
            self._values["node_pool_config"] = node_pool_config

    @builtins.property
    def node_pool_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig"]:
        '''node_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_pool_config GoogleGkeonpremBareMetalCluster#node_pool_config}
        '''
        result = self._values.get("node_pool_config")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig",
    jsii_struct_bases=[],
    name_mapping={
        "labels": "labels",
        "node_configs": "nodeConfigs",
        "operating_system": "operatingSystem",
        "taints": "taints",
    },
)
class GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operating_system: typing.Optional[builtins.str] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#labels GoogleGkeonpremBareMetalCluster#labels}
        :param node_configs: node_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_configs GoogleGkeonpremBareMetalCluster#node_configs}
        :param operating_system: Specifies the nodes operating system (default: LINUX). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#operating_system GoogleGkeonpremBareMetalCluster#operating_system}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#taints GoogleGkeonpremBareMetalCluster#taints}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0c9ee4298d2d73b8c81954089b964bef13b047b59e2a40dd50f51f4e1386f06)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#labels GoogleGkeonpremBareMetalCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def node_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs"]]]:
        '''node_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_configs GoogleGkeonpremBareMetalCluster#node_configs}
        '''
        result = self._values.get("node_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs"]]], result)

    @builtins.property
    def operating_system(self) -> typing.Optional[builtins.str]:
        '''Specifies the nodes operating system (default: LINUX).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#operating_system GoogleGkeonpremBareMetalCluster#operating_system}
        '''
        result = self._values.get("operating_system")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def taints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints"]]]:
        '''taints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#taints GoogleGkeonpremBareMetalCluster#taints}
        '''
        result = self._values.get("taints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels", "node_ip": "nodeIp"},
)
class GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_ip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#labels GoogleGkeonpremBareMetalCluster#labels}
        :param node_ip: The default IPv4 address for SSH access and Kubernetes node. Example: 192.168.0.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_ip GoogleGkeonpremBareMetalCluster#node_ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8abd57bc1a0f81cfddd704e9c6522700cb18de09d2b3528bded01599d5aab41d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#labels GoogleGkeonpremBareMetalCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def node_ip(self) -> typing.Optional[builtins.str]:
        '''The default IPv4 address for SSH access and Kubernetes node. Example: 192.168.0.1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_ip GoogleGkeonpremBareMetalCluster#node_ip}
        '''
        result = self._values.get("node_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d2d8251254504efb9b44361ccd1fffdbcd2f299427b10407143fd130931598e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc5b61b4ed593b8cb92a17d88d76a73cdadf2af52feeb2f92633f15b0a3c0001)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6949bcaf782e9763659a8c9d1efb611bb754b5035ef4795ebfeebdb00a0212a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__672e8422a761f922e39d1952c82a60d213041e7607e2824bfa1876ac1c55c2c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ff99183d05a31cb0b54697e8b37dc97f4c3e2e05e7cd13f033f7b30770f258d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11c67d8bec15fc9fce77843137d9a13bc5014ed442e8c397d081e5bcf75233c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb2fa85f34a4a700d5a1ad1c8a619d745bed5ad2aefbbfc00dac878340bf2451)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b2fe8cf6bb4fde7128af0a3beefead8c5e6010871c4c6a3e8764032d675a707)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeIp")
    def node_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeIp"))

    @node_ip.setter
    def node_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0804cf27e97c57041ae5cb85f0a19c912d860737bc805a84c04e25e5631d33ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b3b9109a7ddaf453f9f767ccc9cd09f39881d7deacb2f942d266066717e31e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__837a9d486c4ab65705e15ba4ff9cd07699d1048c7eebcb60f5e10175355af0b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodeConfigs")
    def put_node_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e42f58b7d8b5334fda934dec9e0d20efc5f4e9134a4bd43a8a934acb38d6e415)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeConfigs", [value]))

    @jsii.member(jsii_name="putTaints")
    def put_taints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__474ed85ab422ecf75b4dfaae110a8c72e0008a377d4eb5bfcfbedbcfa909f18d)
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
    ) -> GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsList:
        return typing.cast(GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsList, jsii.get(self, "nodeConfigs"))

    @builtins.property
    @jsii.member(jsii_name="taints")
    def taints(
        self,
    ) -> "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsList":
        return typing.cast("GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsList", jsii.get(self, "taints"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]], jsii.get(self, "nodeConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="operatingSystemInput")
    def operating_system_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatingSystemInput"))

    @builtins.property
    @jsii.member(jsii_name="taintsInput")
    def taints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints"]]], jsii.get(self, "taintsInput"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17596c0914c185c36629d4c59a212ef9f4c6c9305c76cb9b18b2dfa6d36f4beb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operatingSystem")
    def operating_system(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operatingSystem"))

    @operating_system.setter
    def operating_system(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__852b55b84d2965dab551785e9f6b835302c5369341ddc1b0d0be7ea3859906c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operatingSystem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0799974094eee4e87c60461698498813bc16f1cbec16dc72767de30af0da7b9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints",
    jsii_struct_bases=[],
    name_mapping={"effect": "effect", "key": "key", "value": "value"},
)
class GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints:
    def __init__(
        self,
        *,
        effect: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param effect: Specifies the nodes operating system (default: LINUX). Possible values: ["EFFECT_UNSPECIFIED", "PREFER_NO_SCHEDULE", "NO_EXECUTE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#effect GoogleGkeonpremBareMetalCluster#effect}
        :param key: Key associated with the effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#key GoogleGkeonpremBareMetalCluster#key}
        :param value: Value associated with the effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#value GoogleGkeonpremBareMetalCluster#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5557945deed44740d9bb66ad37d33e75fcd4d3837a1be60ebba79dc7ee8730f2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#effect GoogleGkeonpremBareMetalCluster#effect}
        '''
        result = self._values.get("effect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Key associated with the effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#key GoogleGkeonpremBareMetalCluster#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value associated with the effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#value GoogleGkeonpremBareMetalCluster#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ca8b1b64b9d185503d54f766bb4bc3e91c85b8625d3fad208d535c4ef56bc72)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7107d3b203296e440a547cc9504dab4c5139b771c12d681ba5fbf8f74a41b285)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5556ee9c0abdf220291a8c0c98be13ba1fc5a4de624d4e28cf54e1d88a7e887)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31bb2207de4a6f258d67f833a9b99e9de0c45402c42a3ec2a3732558dfbf53fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__282951ff7bbfc206da364d0f1b15672a934df032e41e227187bed89bee4bff73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd47fdb71017772b6da062c02ce1af13c1821776993e6fa0bfbe5c6b05e2ed8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61f9c4c62b2f65e934de82206c664f1df83d834b633ba7a964aa23352d1e1073)
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
            type_hints = typing.get_type_hints(_typecheckingstub__756d6c256f3b59636cf20aa8422b76d8d6ad723e76098ae33110b410e096f496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f37a0e79d1471145cbe07b535b627037d14cba9acee66c9d363c12e7affc8ce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84e14c69f00a5acfca60cfd967ce8466ee6e6bd22c38d48137eecf7edeae5b70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78850d81da3729ad5bed7faf25b10eb5ed79181feae7fdc724e15924eafc24f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c5a594c868453c13b82923f3486bc716bda3262ed14676856570de63aeedc6c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodePoolConfig")
    def put_node_pool_config(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
        operating_system: typing.Optional[builtins.str] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#labels GoogleGkeonpremBareMetalCluster#labels}
        :param node_configs: node_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_configs GoogleGkeonpremBareMetalCluster#node_configs}
        :param operating_system: Specifies the nodes operating system (default: LINUX). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#operating_system GoogleGkeonpremBareMetalCluster#operating_system}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#taints GoogleGkeonpremBareMetalCluster#taints}
        '''
        value = GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig(
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
    ) -> GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigOutputReference, jsii.get(self, "nodePoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodePoolConfigInput")
    def node_pool_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig], jsii.get(self, "nodePoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68d5cc18bffa4b105947c18363215e76d567657315a00f49bab936366b69a39c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf41010f355c2aab9350c312c7be83b53cb228ea4a39da0937beb9defc6ea402)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAddressPools")
    def put_address_pools(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01e4671d285d92af178088ac5c7cb746fab62bf880e4a8b574ade45c7d4b0419)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAddressPools", [value]))

    @jsii.member(jsii_name="putLoadBalancerNodePoolConfig")
    def put_load_balancer_node_pool_config(
        self,
        *,
        node_pool_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param node_pool_config: node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#node_pool_config GoogleGkeonpremBareMetalCluster#node_pool_config}
        '''
        value = GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig(
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
    ) -> GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPoolsList:
        return typing.cast(GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPoolsList, jsii.get(self, "addressPools"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerNodePoolConfig")
    def load_balancer_node_pool_config(
        self,
    ) -> GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigOutputReference, jsii.get(self, "loadBalancerNodePoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="addressPoolsInput")
    def address_pools_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools]]], jsii.get(self, "addressPoolsInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerNodePoolConfigInput")
    def load_balancer_node_pool_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig], jsii.get(self, "loadBalancerNodePoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e1f1ce8ccce8139f509cba1cf46475044e84a8fbf07ce92463391bc2f7434bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterLoadBalancerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c0c880cf10fe8475ec436824eb3f9bd6b0877f2659a4f2284d56a6912d789a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBgpLbConfig")
    def put_bgp_lb_config(
        self,
        *,
        address_pools: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
        asn: jsii.Number,
        bgp_peer_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs, typing.Dict[builtins.str, typing.Any]]]],
        load_balancer_node_pool_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param address_pools: address_pools block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#address_pools GoogleGkeonpremBareMetalCluster#address_pools}
        :param asn: BGP autonomous system number (ASN) of the cluster. This field can be updated after cluster creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#asn GoogleGkeonpremBareMetalCluster#asn}
        :param bgp_peer_configs: bgp_peer_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#bgp_peer_configs GoogleGkeonpremBareMetalCluster#bgp_peer_configs}
        :param load_balancer_node_pool_config: load_balancer_node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#load_balancer_node_pool_config GoogleGkeonpremBareMetalCluster#load_balancer_node_pool_config}
        '''
        value = GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfig(
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
        :param enabled: Whether manual load balancing is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#enabled GoogleGkeonpremBareMetalCluster#enabled}
        '''
        value = GoogleGkeonpremBareMetalClusterLoadBalancerManualLbConfig(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putManualLbConfig", [value]))

    @jsii.member(jsii_name="putMetalLbConfig")
    def put_metal_lb_config(
        self,
        *,
        address_pools: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
        load_balancer_node_pool_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param address_pools: address_pools block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#address_pools GoogleGkeonpremBareMetalCluster#address_pools}
        :param load_balancer_node_pool_config: load_balancer_node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#load_balancer_node_pool_config GoogleGkeonpremBareMetalCluster#load_balancer_node_pool_config}
        '''
        value = GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfig(
            address_pools=address_pools,
            load_balancer_node_pool_config=load_balancer_node_pool_config,
        )

        return typing.cast(None, jsii.invoke(self, "putMetalLbConfig", [value]))

    @jsii.member(jsii_name="putPortConfig")
    def put_port_config(self, *, control_plane_load_balancer_port: jsii.Number) -> None:
        '''
        :param control_plane_load_balancer_port: The port that control plane hosted load balancers will listen on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#control_plane_load_balancer_port GoogleGkeonpremBareMetalCluster#control_plane_load_balancer_port}
        '''
        value = GoogleGkeonpremBareMetalClusterLoadBalancerPortConfig(
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
        :param control_plane_vip: The VIP which you previously set aside for the Kubernetes API of this Bare Metal User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#control_plane_vip GoogleGkeonpremBareMetalCluster#control_plane_vip}
        :param ingress_vip: The VIP which you previously set aside for ingress traffic into this Bare Metal User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#ingress_vip GoogleGkeonpremBareMetalCluster#ingress_vip}
        '''
        value = GoogleGkeonpremBareMetalClusterLoadBalancerVipConfig(
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
    ) -> GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigOutputReference, jsii.get(self, "bgpLbConfig"))

    @builtins.property
    @jsii.member(jsii_name="manualLbConfig")
    def manual_lb_config(
        self,
    ) -> GoogleGkeonpremBareMetalClusterLoadBalancerManualLbConfigOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalClusterLoadBalancerManualLbConfigOutputReference, jsii.get(self, "manualLbConfig"))

    @builtins.property
    @jsii.member(jsii_name="metalLbConfig")
    def metal_lb_config(
        self,
    ) -> GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigOutputReference, jsii.get(self, "metalLbConfig"))

    @builtins.property
    @jsii.member(jsii_name="portConfig")
    def port_config(
        self,
    ) -> "GoogleGkeonpremBareMetalClusterLoadBalancerPortConfigOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalClusterLoadBalancerPortConfigOutputReference", jsii.get(self, "portConfig"))

    @builtins.property
    @jsii.member(jsii_name="vipConfig")
    def vip_config(
        self,
    ) -> "GoogleGkeonpremBareMetalClusterLoadBalancerVipConfigOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalClusterLoadBalancerVipConfigOutputReference", jsii.get(self, "vipConfig"))

    @builtins.property
    @jsii.member(jsii_name="bgpLbConfigInput")
    def bgp_lb_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfig], jsii.get(self, "bgpLbConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="manualLbConfigInput")
    def manual_lb_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerManualLbConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerManualLbConfig], jsii.get(self, "manualLbConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="metalLbConfigInput")
    def metal_lb_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfig], jsii.get(self, "metalLbConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="portConfigInput")
    def port_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterLoadBalancerPortConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterLoadBalancerPortConfig"], jsii.get(self, "portConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="vipConfigInput")
    def vip_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterLoadBalancerVipConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterLoadBalancerVipConfig"], jsii.get(self, "vipConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancer]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbec04eb5e7f691993ba9700ab0c29b12696f341fd4b4e045566a003f47f6a11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerPortConfig",
    jsii_struct_bases=[],
    name_mapping={"control_plane_load_balancer_port": "controlPlaneLoadBalancerPort"},
)
class GoogleGkeonpremBareMetalClusterLoadBalancerPortConfig:
    def __init__(self, *, control_plane_load_balancer_port: jsii.Number) -> None:
        '''
        :param control_plane_load_balancer_port: The port that control plane hosted load balancers will listen on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#control_plane_load_balancer_port GoogleGkeonpremBareMetalCluster#control_plane_load_balancer_port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46a8b81d7c556ed9a187559437d4ae3f8b7bcfa61124cf41c86b93e56f62f9bc)
            check_type(argname="argument control_plane_load_balancer_port", value=control_plane_load_balancer_port, expected_type=type_hints["control_plane_load_balancer_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "control_plane_load_balancer_port": control_plane_load_balancer_port,
        }

    @builtins.property
    def control_plane_load_balancer_port(self) -> jsii.Number:
        '''The port that control plane hosted load balancers will listen on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#control_plane_load_balancer_port GoogleGkeonpremBareMetalCluster#control_plane_load_balancer_port}
        '''
        result = self._values.get("control_plane_load_balancer_port")
        assert result is not None, "Required property 'control_plane_load_balancer_port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterLoadBalancerPortConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterLoadBalancerPortConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerPortConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e1dbca87acabeaab14d05acd47fbafd6e41ff50697043cd69edc0a57b870630)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e6bd609e36f0d62b443eeec1c4870a2429fc969710a4fc6e5ee93d9dab8f392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneLoadBalancerPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerPortConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerPortConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerPortConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__139cc13d4b7eac22141c6cb47eb026148c48cbd40d74a68bfc740f490cd80dac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerVipConfig",
    jsii_struct_bases=[],
    name_mapping={"control_plane_vip": "controlPlaneVip", "ingress_vip": "ingressVip"},
)
class GoogleGkeonpremBareMetalClusterLoadBalancerVipConfig:
    def __init__(
        self,
        *,
        control_plane_vip: builtins.str,
        ingress_vip: builtins.str,
    ) -> None:
        '''
        :param control_plane_vip: The VIP which you previously set aside for the Kubernetes API of this Bare Metal User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#control_plane_vip GoogleGkeonpremBareMetalCluster#control_plane_vip}
        :param ingress_vip: The VIP which you previously set aside for ingress traffic into this Bare Metal User Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#ingress_vip GoogleGkeonpremBareMetalCluster#ingress_vip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6586189e6fb70544a028769822e75e11b3528dc95ff22440e6d3fc3ee93b370d)
            check_type(argname="argument control_plane_vip", value=control_plane_vip, expected_type=type_hints["control_plane_vip"])
            check_type(argname="argument ingress_vip", value=ingress_vip, expected_type=type_hints["ingress_vip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "control_plane_vip": control_plane_vip,
            "ingress_vip": ingress_vip,
        }

    @builtins.property
    def control_plane_vip(self) -> builtins.str:
        '''The VIP which you previously set aside for the Kubernetes API of this Bare Metal User Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#control_plane_vip GoogleGkeonpremBareMetalCluster#control_plane_vip}
        '''
        result = self._values.get("control_plane_vip")
        assert result is not None, "Required property 'control_plane_vip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ingress_vip(self) -> builtins.str:
        '''The VIP which you previously set aside for ingress traffic into this Bare Metal User Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#ingress_vip GoogleGkeonpremBareMetalCluster#ingress_vip}
        '''
        result = self._values.get("ingress_vip")
        assert result is not None, "Required property 'ingress_vip' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterLoadBalancerVipConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterLoadBalancerVipConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterLoadBalancerVipConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd37c8444f1da74a85b30bcec6e4232a0b50a76b35007d9fd6bc82906c850945)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c89d40840ef940cd5f3f99b8de30783302922da6d27745fb5c93513b672d178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneVip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingressVip")
    def ingress_vip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ingressVip"))

    @ingress_vip.setter
    def ingress_vip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbb4b6e5af24d79b36791fa77ca74649fe60b99db77861fab15831e9656b0d1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingressVip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerVipConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerVipConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerVipConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68ffbe7be7bb5873af1598b0974e2192f11b2bdc25e85d48a4ac54062e7ff2a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterMaintenanceConfig",
    jsii_struct_bases=[],
    name_mapping={"maintenance_address_cidr_blocks": "maintenanceAddressCidrBlocks"},
)
class GoogleGkeonpremBareMetalClusterMaintenanceConfig:
    def __init__(
        self,
        *,
        maintenance_address_cidr_blocks: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param maintenance_address_cidr_blocks: All IPv4 address from these ranges will be placed into maintenance mode. Nodes in maintenance mode will be cordoned and drained. When both of these are true, the "baremetal.cluster.gke.io/maintenance" annotation will be set on the node resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#maintenance_address_cidr_blocks GoogleGkeonpremBareMetalCluster#maintenance_address_cidr_blocks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c24561c1f568604f07179629158bdd3e6dcc7182b8913777d56f059663657c0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#maintenance_address_cidr_blocks GoogleGkeonpremBareMetalCluster#maintenance_address_cidr_blocks}
        '''
        result = self._values.get("maintenance_address_cidr_blocks")
        assert result is not None, "Required property 'maintenance_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterMaintenanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterMaintenanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterMaintenanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7046898fa4b8ef43bd8bde09d03967844f3b741732b46fc00a6fd448c5647688)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50adb55cbf8927e960d6ab8b6379a8cbb5b0658f36ac02dff994a288768bc55a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterMaintenanceConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterMaintenanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterMaintenanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__564fd4308fd54d1a62e8a09436824e9cfc9606fc3b3060792574078e19e1d128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={
        "advanced_networking": "advancedNetworking",
        "island_mode_cidr": "islandModeCidr",
        "multiple_network_interfaces_config": "multipleNetworkInterfacesConfig",
        "sr_iov_config": "srIovConfig",
    },
)
class GoogleGkeonpremBareMetalClusterNetworkConfig:
    def __init__(
        self,
        *,
        advanced_networking: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        island_mode_cidr: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterNetworkConfigIslandModeCidr", typing.Dict[builtins.str, typing.Any]]] = None,
        multiple_network_interfaces_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        sr_iov_config: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterNetworkConfigSrIovConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_networking: Enables the use of advanced Anthos networking features, such as Bundled Load Balancing with BGP or the egress NAT gateway. Setting configuration for advanced networking features will automatically set this flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#advanced_networking GoogleGkeonpremBareMetalCluster#advanced_networking}
        :param island_mode_cidr: island_mode_cidr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#island_mode_cidr GoogleGkeonpremBareMetalCluster#island_mode_cidr}
        :param multiple_network_interfaces_config: multiple_network_interfaces_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#multiple_network_interfaces_config GoogleGkeonpremBareMetalCluster#multiple_network_interfaces_config}
        :param sr_iov_config: sr_iov_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#sr_iov_config GoogleGkeonpremBareMetalCluster#sr_iov_config}
        '''
        if isinstance(island_mode_cidr, dict):
            island_mode_cidr = GoogleGkeonpremBareMetalClusterNetworkConfigIslandModeCidr(**island_mode_cidr)
        if isinstance(multiple_network_interfaces_config, dict):
            multiple_network_interfaces_config = GoogleGkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig(**multiple_network_interfaces_config)
        if isinstance(sr_iov_config, dict):
            sr_iov_config = GoogleGkeonpremBareMetalClusterNetworkConfigSrIovConfig(**sr_iov_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edeb0597d0913b87bfac2400a90b7810911efe2574218d3fbe1b59162062b515)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#advanced_networking GoogleGkeonpremBareMetalCluster#advanced_networking}
        '''
        result = self._values.get("advanced_networking")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def island_mode_cidr(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterNetworkConfigIslandModeCidr"]:
        '''island_mode_cidr block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#island_mode_cidr GoogleGkeonpremBareMetalCluster#island_mode_cidr}
        '''
        result = self._values.get("island_mode_cidr")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterNetworkConfigIslandModeCidr"], result)

    @builtins.property
    def multiple_network_interfaces_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig"]:
        '''multiple_network_interfaces_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#multiple_network_interfaces_config GoogleGkeonpremBareMetalCluster#multiple_network_interfaces_config}
        '''
        result = self._values.get("multiple_network_interfaces_config")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig"], result)

    @builtins.property
    def sr_iov_config(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterNetworkConfigSrIovConfig"]:
        '''sr_iov_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#sr_iov_config GoogleGkeonpremBareMetalCluster#sr_iov_config}
        '''
        result = self._values.get("sr_iov_config")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterNetworkConfigSrIovConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterNetworkConfigIslandModeCidr",
    jsii_struct_bases=[],
    name_mapping={
        "pod_address_cidr_blocks": "podAddressCidrBlocks",
        "service_address_cidr_blocks": "serviceAddressCidrBlocks",
    },
)
class GoogleGkeonpremBareMetalClusterNetworkConfigIslandModeCidr:
    def __init__(
        self,
        *,
        pod_address_cidr_blocks: typing.Sequence[builtins.str],
        service_address_cidr_blocks: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param pod_address_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these ranges. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#pod_address_cidr_blocks GoogleGkeonpremBareMetalCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these ranges. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#service_address_cidr_blocks GoogleGkeonpremBareMetalCluster#service_address_cidr_blocks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee0e1f162eb21e1c8b65f2783435b092fdd482234d96a4849ac038ec14c64431)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#pod_address_cidr_blocks GoogleGkeonpremBareMetalCluster#pod_address_cidr_blocks}
        '''
        result = self._values.get("pod_address_cidr_blocks")
        assert result is not None, "Required property 'pod_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        '''All services in the cluster are assigned an RFC1918 IPv4 address from these ranges.

        This field cannot be changed after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#service_address_cidr_blocks GoogleGkeonpremBareMetalCluster#service_address_cidr_blocks}
        '''
        result = self._values.get("service_address_cidr_blocks")
        assert result is not None, "Required property 'service_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterNetworkConfigIslandModeCidr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterNetworkConfigIslandModeCidrOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterNetworkConfigIslandModeCidrOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__add918a5d286b57ad42f0de2db0fb122d700356cfdea1b366cb5b540c82de24a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70d66aa5ffb67fd6f068b5afdc6a6097aa7503a8d6b05cd70fb3eb3a6a88bebb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAddressCidrBlocks")
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceAddressCidrBlocks"))

    @service_address_cidr_blocks.setter
    def service_address_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bcd9c2c0d672d084018d09fa8ae71ae930b6a1693fe1e4a6e9bfd5bf6d29ec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterNetworkConfigIslandModeCidr]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterNetworkConfigIslandModeCidr], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterNetworkConfigIslandModeCidr],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af16330bd85273e02978dc9bcea61f85a2f4648c521423133718c32a86134df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleGkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether to enable multiple network interfaces for your pods. When set network_config.advanced_networking is automatically set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#enabled GoogleGkeonpremBareMetalCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51140896f17b16576b941409c5642857e89e43234c20b09e829c0d4e822dbe72)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to enable multiple network interfaces for your pods. When set network_config.advanced_networking is automatically set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#enabled GoogleGkeonpremBareMetalCluster#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f93da8b0786f3ea212f57377ecefe1df56314140dce3b5e17bba2f5e2d91f55)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d6c2f1534bf1161ef050abedc56f655666dd3a67ae6fd3d536b0ea0339da8e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3620ee7acb652e93f5f982f1c98d9214bed54aa28d5dce443f4b9e0eaa6e3b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4dec635ef6c3c3c9434356d6cfd5d926af21837f03f5ee38541270939bcbf14f)
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
        :param pod_address_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these ranges. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#pod_address_cidr_blocks GoogleGkeonpremBareMetalCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these ranges. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#service_address_cidr_blocks GoogleGkeonpremBareMetalCluster#service_address_cidr_blocks}
        '''
        value = GoogleGkeonpremBareMetalClusterNetworkConfigIslandModeCidr(
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
        :param enabled: Whether to enable multiple network interfaces for your pods. When set network_config.advanced_networking is automatically set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#enabled GoogleGkeonpremBareMetalCluster#enabled}
        '''
        value = GoogleGkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig(
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
        :param enabled: Whether to install the SR-IOV operator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#enabled GoogleGkeonpremBareMetalCluster#enabled}
        '''
        value = GoogleGkeonpremBareMetalClusterNetworkConfigSrIovConfig(
            enabled=enabled
        )

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
    ) -> GoogleGkeonpremBareMetalClusterNetworkConfigIslandModeCidrOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalClusterNetworkConfigIslandModeCidrOutputReference, jsii.get(self, "islandModeCidr"))

    @builtins.property
    @jsii.member(jsii_name="multipleNetworkInterfacesConfig")
    def multiple_network_interfaces_config(
        self,
    ) -> GoogleGkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfigOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfigOutputReference, jsii.get(self, "multipleNetworkInterfacesConfig"))

    @builtins.property
    @jsii.member(jsii_name="srIovConfig")
    def sr_iov_config(
        self,
    ) -> "GoogleGkeonpremBareMetalClusterNetworkConfigSrIovConfigOutputReference":
        return typing.cast("GoogleGkeonpremBareMetalClusterNetworkConfigSrIovConfigOutputReference", jsii.get(self, "srIovConfig"))

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
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterNetworkConfigIslandModeCidr]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterNetworkConfigIslandModeCidr], jsii.get(self, "islandModeCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="multipleNetworkInterfacesConfigInput")
    def multiple_network_interfaces_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig], jsii.get(self, "multipleNetworkInterfacesConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="srIovConfigInput")
    def sr_iov_config_input(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterNetworkConfigSrIovConfig"]:
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterNetworkConfigSrIovConfig"], jsii.get(self, "srIovConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__62cc73e26bf1292daf1faa280349e01076b6c14115a2789261c8fa9f3f648a79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advancedNetworking", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterNetworkConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c239dc5cca9e16747bfb9b55d8d67895c50507ea139f2da2cc442a7c3ac1d470)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterNetworkConfigSrIovConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleGkeonpremBareMetalClusterNetworkConfigSrIovConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether to install the SR-IOV operator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#enabled GoogleGkeonpremBareMetalCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90123c20bb573ae9d58bc007261c96a5d0a42daeb64ae89d923335b051875246)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to install the SR-IOV operator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#enabled GoogleGkeonpremBareMetalCluster#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterNetworkConfigSrIovConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterNetworkConfigSrIovConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterNetworkConfigSrIovConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3059924cbb5a593c4871e846f0e4c891a1fd2607cc54283d9ae9a63b9ed9cc0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c57655287d9bf7c62b1ec5e925b0b24898f7e87f9edd6ef7503100b19adf8f56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterNetworkConfigSrIovConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterNetworkConfigSrIovConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterNetworkConfigSrIovConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4802965f7fdf0a2513c73fcd33b7146a89c1cdfefc7ac1670891cbef9178d9f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterNodeAccessConfig",
    jsii_struct_bases=[],
    name_mapping={"login_user": "loginUser"},
)
class GoogleGkeonpremBareMetalClusterNodeAccessConfig:
    def __init__(self, *, login_user: typing.Optional[builtins.str] = None) -> None:
        '''
        :param login_user: LoginUser is the user name used to access node machines. It defaults to "root" if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#login_user GoogleGkeonpremBareMetalCluster#login_user}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e3ee7686008c562e7d700ca72c11ef7e8cb17fb464ca2b1bd2fdedb444bfd7a)
            check_type(argname="argument login_user", value=login_user, expected_type=type_hints["login_user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if login_user is not None:
            self._values["login_user"] = login_user

    @builtins.property
    def login_user(self) -> typing.Optional[builtins.str]:
        '''LoginUser is the user name used to access node machines. It defaults to "root" if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#login_user GoogleGkeonpremBareMetalCluster#login_user}
        '''
        result = self._values.get("login_user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterNodeAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterNodeAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterNodeAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5383e09a46f928ba66e0872756384442ee8adee78e3b4e1cebe0e11403f68f36)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09b6c3be164e8980a09437aef00cc7a65b19f94819b79924bc4d35a423a07641)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterNodeAccessConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterNodeAccessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterNodeAccessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d4c43cc918f8c5a64a07f9a4539658b30932522ac2054e15b2286859e6bbd1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterNodeConfig",
    jsii_struct_bases=[],
    name_mapping={
        "container_runtime": "containerRuntime",
        "max_pods_per_node": "maxPodsPerNode",
    },
)
class GoogleGkeonpremBareMetalClusterNodeConfig:
    def __init__(
        self,
        *,
        container_runtime: typing.Optional[builtins.str] = None,
        max_pods_per_node: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param container_runtime: The available runtimes that can be used to run containers in a Bare Metal User Cluster. Possible values: ["CONTAINER_RUNTIME_UNSPECIFIED", "DOCKER", "CONTAINERD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#container_runtime GoogleGkeonpremBareMetalCluster#container_runtime}
        :param max_pods_per_node: The maximum number of pods a node can run. The size of the CIDR range assigned to the node will be derived from this parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#max_pods_per_node GoogleGkeonpremBareMetalCluster#max_pods_per_node}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89c3b7948db134cfc574695d2b889681b62f0050d14c57c12c716b38afe21248)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#container_runtime GoogleGkeonpremBareMetalCluster#container_runtime}
        '''
        result = self._values.get("container_runtime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_pods_per_node(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of pods a node can run.

        The size of the CIDR range
        assigned to the node will be derived from this parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#max_pods_per_node GoogleGkeonpremBareMetalCluster#max_pods_per_node}
        '''
        result = self._values.get("max_pods_per_node")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterNodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterNodeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterNodeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73e8e6ca6dbd2711fe88c6ffeb97d94d7853aa49a0829a3d652679a8e3b3baf0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__302932c4f924e9403cd2d3145463b4498af01bbaac30eded3c16156627eb4dc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerRuntime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxPodsPerNode")
    def max_pods_per_node(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPodsPerNode"))

    @max_pods_per_node.setter
    def max_pods_per_node(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5876c8730f600722d76a2470cc6955ec3ddff5c2a821b6a10f22902fcbd20a38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPodsPerNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterNodeConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterNodeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterNodeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07b73f112fadfb7549e9a573f046b06447928903cc75f165a1d578bfd2bb89e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterOsEnvironmentConfig",
    jsii_struct_bases=[],
    name_mapping={"package_repo_excluded": "packageRepoExcluded"},
)
class GoogleGkeonpremBareMetalClusterOsEnvironmentConfig:
    def __init__(
        self,
        *,
        package_repo_excluded: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param package_repo_excluded: Whether the package repo should not be included when initializing bare metal machines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#package_repo_excluded GoogleGkeonpremBareMetalCluster#package_repo_excluded}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d60d098bbfd82d86e4a633f4fde5f6ce0545ec50b246d596f5590c1460a0d852)
            check_type(argname="argument package_repo_excluded", value=package_repo_excluded, expected_type=type_hints["package_repo_excluded"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "package_repo_excluded": package_repo_excluded,
        }

    @builtins.property
    def package_repo_excluded(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether the package repo should not be included when initializing bare metal machines.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#package_repo_excluded GoogleGkeonpremBareMetalCluster#package_repo_excluded}
        '''
        result = self._values.get("package_repo_excluded")
        assert result is not None, "Required property 'package_repo_excluded' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterOsEnvironmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterOsEnvironmentConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterOsEnvironmentConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dab879d9bdf6548d416e2d32cfaedf1e63fd7ec952619adff74c377c5c8280b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__329be9635343834e06ac1f6435e191314ec6cbf27d3824b8ed7d806e077d76ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packageRepoExcluded", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterOsEnvironmentConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterOsEnvironmentConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterOsEnvironmentConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b53fb178f6dc20c036514076a5e71ca333fe43db4596b66e11edb8ea183abeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterProxy",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "no_proxy": "noProxy"},
)
class GoogleGkeonpremBareMetalClusterProxy:
    def __init__(
        self,
        *,
        uri: builtins.str,
        no_proxy: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param uri: Specifies the address of your proxy server. For example: http://domain WARNING: Do not provide credentials in the format of http://(username:password@)domain these will be rejected by the server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#uri GoogleGkeonpremBareMetalCluster#uri}
        :param no_proxy: A list of IPs, hostnames, and domains that should skip the proxy. For example ["127.0.0.1", "example.com", ".corp", "localhost"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#no_proxy GoogleGkeonpremBareMetalCluster#no_proxy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5321aec0ce28d6203c072c17bef5227f4d2a60675922d6c0bb1b2efd51920c4c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#uri GoogleGkeonpremBareMetalCluster#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def no_proxy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IPs, hostnames, and domains that should skip the proxy. For example ["127.0.0.1", "example.com", ".corp", "localhost"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#no_proxy GoogleGkeonpremBareMetalCluster#no_proxy}
        '''
        result = self._values.get("no_proxy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterProxy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterProxyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterProxyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d32631d372d9b13d03ffca4f8e240d631b8399ddc780e9bbf22bc2c49dc8f12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f274bfe0ea767ac6fe29f90ef9635670d63d5c4e3c596b8cad6eacc0a87c5a06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noProxy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__388d68823583b33990ec466353eb90bbbb61efabb8733a14d773620a50bb54ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleGkeonpremBareMetalClusterProxy]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterProxy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterProxy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43468f0abd247d79bd2793e345ea6d1d8bf85f0560cd02b4404e5bcd6fa04d65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterSecurityConfig",
    jsii_struct_bases=[],
    name_mapping={"authorization": "authorization"},
)
class GoogleGkeonpremBareMetalClusterSecurityConfig:
    def __init__(
        self,
        *,
        authorization: typing.Optional[typing.Union["GoogleGkeonpremBareMetalClusterSecurityConfigAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#authorization GoogleGkeonpremBareMetalCluster#authorization}
        '''
        if isinstance(authorization, dict):
            authorization = GoogleGkeonpremBareMetalClusterSecurityConfigAuthorization(**authorization)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__589eec8265976c0a9c794eeedf1d8a02097eb84e7a2eeba9a92f7fa599b61c9a)
            check_type(argname="argument authorization", value=authorization, expected_type=type_hints["authorization"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authorization is not None:
            self._values["authorization"] = authorization

    @builtins.property
    def authorization(
        self,
    ) -> typing.Optional["GoogleGkeonpremBareMetalClusterSecurityConfigAuthorization"]:
        '''authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#authorization GoogleGkeonpremBareMetalCluster#authorization}
        '''
        result = self._values.get("authorization")
        return typing.cast(typing.Optional["GoogleGkeonpremBareMetalClusterSecurityConfigAuthorization"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterSecurityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterSecurityConfigAuthorization",
    jsii_struct_bases=[],
    name_mapping={"admin_users": "adminUsers"},
)
class GoogleGkeonpremBareMetalClusterSecurityConfigAuthorization:
    def __init__(
        self,
        *,
        admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#admin_users GoogleGkeonpremBareMetalCluster#admin_users}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d23a2cac0fdb5e3246dd516058cd00dda470b6b31803e7a3c858445c42e84b7)
            check_type(argname="argument admin_users", value=admin_users, expected_type=type_hints["admin_users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_users": admin_users,
        }

    @builtins.property
    def admin_users(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers"]]:
        '''admin_users block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#admin_users GoogleGkeonpremBareMetalCluster#admin_users}
        '''
        result = self._values.get("admin_users")
        assert result is not None, "Required property 'admin_users' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterSecurityConfigAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers",
    jsii_struct_bases=[],
    name_mapping={"username": "username"},
)
class GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers:
    def __init__(self, *, username: builtins.str) -> None:
        '''
        :param username: The name of the user, e.g. 'my-gcp-id@gmail.com'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#username GoogleGkeonpremBareMetalCluster#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96befd2d34fd12cd2c252686ed5af5bbb60a81d2a5f0b067e70fac89a8728a4e)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
        }

    @builtins.property
    def username(self) -> builtins.str:
        '''The name of the user, e.g. 'my-gcp-id@gmail.com'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#username GoogleGkeonpremBareMetalCluster#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c80f8b60730fdbfb42ba10be4ba94ef9d76763629ca80a23be3e98ebaf0de48)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62fc9460b59e8070a930b82a284e2cba1a1244e614adee8ad676189cae41fefc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5bd6d442ec024c7bcd99f5a85956d52dba18ce529d632057766144ebf0c45c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4477cb88bca9b486f2a5bde1c450a9d8d69cfb0fb8fff3a57b7af0084642c84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2edff9966ca9e15908d341fa18bbe90f566349e8293d468448c273311ee83c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7e1d1335e9c00f757872d78d3797b53cbb06ffee2fa2be720e8c8f1c54d4501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4a4f83bf151497600503219b2fd93563edffb7663478d8fd6b2688bc2ebe160)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8501f28e6dc35ac3fe500b13f55047d7f7dcaca13897ee6379ef4b352508da16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e5a43c02a857824d62b9b4a51f47b69dd4c275c28ade0cf2198cc711da6e30c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc863ceffff4f058c934ac20d5fb73a98b0f6793465ae85c830bb14ab7cbd68d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdminUsers")
    def put_admin_users(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67c220374e96cae09ed408a465cd5a1da09402df553f795d38389b6459c55e93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdminUsers", [value]))

    @builtins.property
    @jsii.member(jsii_name="adminUsers")
    def admin_users(
        self,
    ) -> GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsersList:
        return typing.cast(GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsersList, jsii.get(self, "adminUsers"))

    @builtins.property
    @jsii.member(jsii_name="adminUsersInput")
    def admin_users_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers]]], jsii.get(self, "adminUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterSecurityConfigAuthorization]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterSecurityConfigAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterSecurityConfigAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dffd715344eacede7018ba90088b5ff79f0fdac268a98a606e4f7011040f3cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterSecurityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterSecurityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__561f567c20280e05a9ac6a8d67ac5ebe391efae35b430ed308214579f7c29017)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthorization")
    def put_authorization(
        self,
        *,
        admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#admin_users GoogleGkeonpremBareMetalCluster#admin_users}
        '''
        value = GoogleGkeonpremBareMetalClusterSecurityConfigAuthorization(
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
    ) -> GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationOutputReference, jsii.get(self, "authorization"))

    @builtins.property
    @jsii.member(jsii_name="authorizationInput")
    def authorization_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterSecurityConfigAuthorization]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterSecurityConfigAuthorization], jsii.get(self, "authorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterSecurityConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterSecurityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterSecurityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0fd31f9b90ec9bf6ac46cf770cafa23db4977936616d3bda65dfd6917286a2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremBareMetalClusterStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterStatusConditions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremBareMetalClusterStatusConditions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterStatusConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterStatusConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterStatusConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8ffa288b49b594ae9654d684187de929f9bd643a7a82838370ea1067f73deec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalClusterStatusConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c196d01ac32735fba52de05c0165afdeb8ac9808de93ca2a8663ceff70ac5219)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalClusterStatusConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78f449beacfcc18f9950a81af4d8ccd82ee816d6d2974349b9a2e6a653ed6d84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66ceae606a6979b59021805ae1c266147a956dd6b59d57c0c13cdf9c6378397d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fa509cc421f226dbb29073c11341679d405fa06c5fc63cff1ce5a937c58e488)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterStatusConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterStatusConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7147d1dc23da403b3ee218ecfde666e298fa9b7b89e4a3255f0531f7501c3be1)
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
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterStatusConditions]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterStatusConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterStatusConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__787722d6b7b08fb825d55ef59dd0b6391dcd49aff8fc8460ad0047358a0faec3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d33000f6bd7c5e2bf38077e70972fb5035b49bbe99a2df893d69a11ee16a5d88)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalClusterStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e99cc6dfe64380047dd9c84e61349f698bb0398746504d421123dc2d4caa158)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalClusterStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e8ca6d4640ce76c13f7be5dd6075373912814b0f3be41ea73885cb0dd369c68)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e35e9631b66d22afede92413a83f97a0caf1c4e57afbeed48630cdd53d569dcd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f04a00559bf84bb4b7e5f1e736e0316c7fef865896d963d379cabdb8fea40581)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e75bdfa6cd10b1bd89cab0feb10687dedade338ba62e18510099f99a5fe16c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> GoogleGkeonpremBareMetalClusterStatusConditionsList:
        return typing.cast(GoogleGkeonpremBareMetalClusterStatusConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleGkeonpremBareMetalClusterStatus]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59814935b16157fb988f2cb192de4092a5d589e9ab08c39a0f72936c30b3f286)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterStorage",
    jsii_struct_bases=[],
    name_mapping={
        "lvp_node_mounts_config": "lvpNodeMountsConfig",
        "lvp_share_config": "lvpShareConfig",
    },
)
class GoogleGkeonpremBareMetalClusterStorage:
    def __init__(
        self,
        *,
        lvp_node_mounts_config: typing.Union["GoogleGkeonpremBareMetalClusterStorageLvpNodeMountsConfig", typing.Dict[builtins.str, typing.Any]],
        lvp_share_config: typing.Union["GoogleGkeonpremBareMetalClusterStorageLvpShareConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param lvp_node_mounts_config: lvp_node_mounts_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#lvp_node_mounts_config GoogleGkeonpremBareMetalCluster#lvp_node_mounts_config}
        :param lvp_share_config: lvp_share_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#lvp_share_config GoogleGkeonpremBareMetalCluster#lvp_share_config}
        '''
        if isinstance(lvp_node_mounts_config, dict):
            lvp_node_mounts_config = GoogleGkeonpremBareMetalClusterStorageLvpNodeMountsConfig(**lvp_node_mounts_config)
        if isinstance(lvp_share_config, dict):
            lvp_share_config = GoogleGkeonpremBareMetalClusterStorageLvpShareConfig(**lvp_share_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7845dd8d94ef0e180322d7aa12d596a1794e21ce9c4165d3ff994527a07eec3e)
            check_type(argname="argument lvp_node_mounts_config", value=lvp_node_mounts_config, expected_type=type_hints["lvp_node_mounts_config"])
            check_type(argname="argument lvp_share_config", value=lvp_share_config, expected_type=type_hints["lvp_share_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lvp_node_mounts_config": lvp_node_mounts_config,
            "lvp_share_config": lvp_share_config,
        }

    @builtins.property
    def lvp_node_mounts_config(
        self,
    ) -> "GoogleGkeonpremBareMetalClusterStorageLvpNodeMountsConfig":
        '''lvp_node_mounts_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#lvp_node_mounts_config GoogleGkeonpremBareMetalCluster#lvp_node_mounts_config}
        '''
        result = self._values.get("lvp_node_mounts_config")
        assert result is not None, "Required property 'lvp_node_mounts_config' is missing"
        return typing.cast("GoogleGkeonpremBareMetalClusterStorageLvpNodeMountsConfig", result)

    @builtins.property
    def lvp_share_config(
        self,
    ) -> "GoogleGkeonpremBareMetalClusterStorageLvpShareConfig":
        '''lvp_share_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#lvp_share_config GoogleGkeonpremBareMetalCluster#lvp_share_config}
        '''
        result = self._values.get("lvp_share_config")
        assert result is not None, "Required property 'lvp_share_config' is missing"
        return typing.cast("GoogleGkeonpremBareMetalClusterStorageLvpShareConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterStorageLvpNodeMountsConfig",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "storage_class": "storageClass"},
)
class GoogleGkeonpremBareMetalClusterStorageLvpNodeMountsConfig:
    def __init__(self, *, path: builtins.str, storage_class: builtins.str) -> None:
        '''
        :param path: The host machine path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#path GoogleGkeonpremBareMetalCluster#path}
        :param storage_class: The StorageClass name that PVs will be created with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#storage_class GoogleGkeonpremBareMetalCluster#storage_class}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48727c5e182ab68381253ec34dda9685596e6c483de5555e43b5e202ccf491d3)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "storage_class": storage_class,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''The host machine path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#path GoogleGkeonpremBareMetalCluster#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_class(self) -> builtins.str:
        '''The StorageClass name that PVs will be created with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#storage_class GoogleGkeonpremBareMetalCluster#storage_class}
        '''
        result = self._values.get("storage_class")
        assert result is not None, "Required property 'storage_class' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterStorageLvpNodeMountsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterStorageLvpNodeMountsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterStorageLvpNodeMountsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__941884b99cea72fda3a8a45528a4fbe18a0bcf0e0f38e5ff01fdbf470d1345bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f750f8e88dda340bc0b69760a6ebbb8df5aa4b988cc09e3aef1387b02460779e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageClass")
    def storage_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageClass"))

    @storage_class.setter
    def storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b97289f8299e24a9c63049b137cbfa049aa4b3cfaaa61e1705353fb520e05ab3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterStorageLvpNodeMountsConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterStorageLvpNodeMountsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterStorageLvpNodeMountsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45d3cd634b7bdd39704626ab5faaaef4e0116760fe893666228529ce12d2ca8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterStorageLvpShareConfig",
    jsii_struct_bases=[],
    name_mapping={
        "lvp_config": "lvpConfig",
        "shared_path_pv_count": "sharedPathPvCount",
    },
)
class GoogleGkeonpremBareMetalClusterStorageLvpShareConfig:
    def __init__(
        self,
        *,
        lvp_config: typing.Union["GoogleGkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig", typing.Dict[builtins.str, typing.Any]],
        shared_path_pv_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param lvp_config: lvp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#lvp_config GoogleGkeonpremBareMetalCluster#lvp_config}
        :param shared_path_pv_count: The number of subdirectories to create under path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#shared_path_pv_count GoogleGkeonpremBareMetalCluster#shared_path_pv_count}
        '''
        if isinstance(lvp_config, dict):
            lvp_config = GoogleGkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig(**lvp_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fd65dada97ea989ca852a0d0d1c93097382fa2fb98a2b3a98973140733c6430)
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
    ) -> "GoogleGkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig":
        '''lvp_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#lvp_config GoogleGkeonpremBareMetalCluster#lvp_config}
        '''
        result = self._values.get("lvp_config")
        assert result is not None, "Required property 'lvp_config' is missing"
        return typing.cast("GoogleGkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig", result)

    @builtins.property
    def shared_path_pv_count(self) -> typing.Optional[jsii.Number]:
        '''The number of subdirectories to create under path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#shared_path_pv_count GoogleGkeonpremBareMetalCluster#shared_path_pv_count}
        '''
        result = self._values.get("shared_path_pv_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterStorageLvpShareConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "storage_class": "storageClass"},
)
class GoogleGkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig:
    def __init__(self, *, path: builtins.str, storage_class: builtins.str) -> None:
        '''
        :param path: The host machine path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#path GoogleGkeonpremBareMetalCluster#path}
        :param storage_class: The StorageClass name that PVs will be created with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#storage_class GoogleGkeonpremBareMetalCluster#storage_class}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be8ffbc7adecb77f4e97b1869f0679ba5204835bc79387e8dd45b1e8177db2b2)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "storage_class": storage_class,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''The host machine path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#path GoogleGkeonpremBareMetalCluster#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_class(self) -> builtins.str:
        '''The StorageClass name that PVs will be created with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#storage_class GoogleGkeonpremBareMetalCluster#storage_class}
        '''
        result = self._values.get("storage_class")
        assert result is not None, "Required property 'storage_class' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterStorageLvpShareConfigLvpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterStorageLvpShareConfigLvpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c65074e4cbdb4d4d37ee72b7eb68cc50108f93b1a63e177e553825fa973b3b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b542997f8450ab88d4af8f46fdec57eb08d984057665011a28f14153fe3e660d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageClass")
    def storage_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageClass"))

    @storage_class.setter
    def storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdbacde9c9c07589dac8f3ee583f56aa361b5cb5b73956c183c094022e677605)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9750039a0d83daa01580f8214a6f7c932d6feb858f3358df04dac0094dbebed8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterStorageLvpShareConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterStorageLvpShareConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__261e8cf8fae5c0d3a1a4323eb60a8ea1e0d897fb25db6e313f6f2c699f195f19)
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
        :param path: The host machine path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#path GoogleGkeonpremBareMetalCluster#path}
        :param storage_class: The StorageClass name that PVs will be created with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#storage_class GoogleGkeonpremBareMetalCluster#storage_class}
        '''
        value = GoogleGkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig(
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
    ) -> GoogleGkeonpremBareMetalClusterStorageLvpShareConfigLvpConfigOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalClusterStorageLvpShareConfigLvpConfigOutputReference, jsii.get(self, "lvpConfig"))

    @builtins.property
    @jsii.member(jsii_name="lvpConfigInput")
    def lvp_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig], jsii.get(self, "lvpConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3445f64eeafcdc19167dce373be516f4c435b362b93013314684dd1804623004)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedPathPvCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterStorageLvpShareConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterStorageLvpShareConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterStorageLvpShareConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a422699c8f3409a718fd6b76fbf793513e06aace45acb78540c3e60cc45657c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterStorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterStorageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c5318d2f875a32405b27d8aec94f8fee43353e74fc1e53c762df9c8dc36796a)
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
        :param path: The host machine path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#path GoogleGkeonpremBareMetalCluster#path}
        :param storage_class: The StorageClass name that PVs will be created with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#storage_class GoogleGkeonpremBareMetalCluster#storage_class}
        '''
        value = GoogleGkeonpremBareMetalClusterStorageLvpNodeMountsConfig(
            path=path, storage_class=storage_class
        )

        return typing.cast(None, jsii.invoke(self, "putLvpNodeMountsConfig", [value]))

    @jsii.member(jsii_name="putLvpShareConfig")
    def put_lvp_share_config(
        self,
        *,
        lvp_config: typing.Union[GoogleGkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig, typing.Dict[builtins.str, typing.Any]],
        shared_path_pv_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param lvp_config: lvp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#lvp_config GoogleGkeonpremBareMetalCluster#lvp_config}
        :param shared_path_pv_count: The number of subdirectories to create under path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#shared_path_pv_count GoogleGkeonpremBareMetalCluster#shared_path_pv_count}
        '''
        value = GoogleGkeonpremBareMetalClusterStorageLvpShareConfig(
            lvp_config=lvp_config, shared_path_pv_count=shared_path_pv_count
        )

        return typing.cast(None, jsii.invoke(self, "putLvpShareConfig", [value]))

    @builtins.property
    @jsii.member(jsii_name="lvpNodeMountsConfig")
    def lvp_node_mounts_config(
        self,
    ) -> GoogleGkeonpremBareMetalClusterStorageLvpNodeMountsConfigOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalClusterStorageLvpNodeMountsConfigOutputReference, jsii.get(self, "lvpNodeMountsConfig"))

    @builtins.property
    @jsii.member(jsii_name="lvpShareConfig")
    def lvp_share_config(
        self,
    ) -> GoogleGkeonpremBareMetalClusterStorageLvpShareConfigOutputReference:
        return typing.cast(GoogleGkeonpremBareMetalClusterStorageLvpShareConfigOutputReference, jsii.get(self, "lvpShareConfig"))

    @builtins.property
    @jsii.member(jsii_name="lvpNodeMountsConfigInput")
    def lvp_node_mounts_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterStorageLvpNodeMountsConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterStorageLvpNodeMountsConfig], jsii.get(self, "lvpNodeMountsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="lvpShareConfigInput")
    def lvp_share_config_input(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterStorageLvpShareConfig]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterStorageLvpShareConfig], jsii.get(self, "lvpShareConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleGkeonpremBareMetalClusterStorage]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterStorage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterStorage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f62c520ebb6133b0b30cc2b32e436c82556141b51cebf165fd726a687d10e32e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleGkeonpremBareMetalClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#create GoogleGkeonpremBareMetalCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#delete GoogleGkeonpremBareMetalCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#update GoogleGkeonpremBareMetalCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__545cfca03968b979fbe2de91c7a53af4c3ac461e2e93cbeb1f6a35768316b5f9)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#create GoogleGkeonpremBareMetalCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#delete GoogleGkeonpremBareMetalCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#update GoogleGkeonpremBareMetalCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5311a3823cc799c21cceaf3fcde5a35ae8437cd68bb817224cf3fcb631d2bd28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78bcbbbeadb0ac16beabf3d50ef89c7f9d87e2ce333a47cca2ad8b38b9d11336)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__023f2fc58454afd473881545d97a453e404ddc0ed36bc0f8266c9a84ee380ac4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87b486dd08b39e31272119412e204c034d828ab4739e15a77b0d4d7d82dd7e1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a99c5589d35fb02324204b0986ac0318a4e3a811bfc0ab9ed90eb11624ec10bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterUpgradePolicy",
    jsii_struct_bases=[],
    name_mapping={"policy": "policy"},
)
class GoogleGkeonpremBareMetalClusterUpgradePolicy:
    def __init__(self, *, policy: typing.Optional[builtins.str] = None) -> None:
        '''
        :param policy: Specifies which upgrade policy to use. Possible values: ["SERIAL", "CONCURRENT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#policy GoogleGkeonpremBareMetalCluster#policy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da27391b45619f050a3e687c07b9dca8ee692d0340642bffcec95f81199d2f8a)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy is not None:
            self._values["policy"] = policy

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''Specifies which upgrade policy to use. Possible values: ["SERIAL", "CONCURRENT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gkeonprem_bare_metal_cluster#policy GoogleGkeonpremBareMetalCluster#policy}
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterUpgradePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterUpgradePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterUpgradePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd1a2e5bb139ae05f8facd15ab9abb0fc087428dcabf77b41daf11ae04d5dab1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44060993cf8c89602d89a9d834463300d4cac2bf2cabdc5e1e421a385d0132ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterUpgradePolicy]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterUpgradePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterUpgradePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2f8b5a9a70f5d7a4dabc755fa5c81e3c989fed202177a3872c1a432fbace31b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterValidationCheck",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremBareMetalClusterValidationCheck:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterValidationCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterValidationCheckList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterValidationCheckList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8a539b2744cdf1578b998b87be6f8d932147fc9b29c57615c583e9f5c1894bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalClusterValidationCheckOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9464e390da70d96345e9b4d85636ec7514763cb9e3aa32b0e6da42dde91aa3fb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalClusterValidationCheckOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a00e9b712305f310f4aaefed7e4ef2b55cf064ac4f01a68ea3bfab1bdc7677cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d27c0280edfcf940cce4897a28b926a977c92bc738f6ffe2802822421152802c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ce9edd36a921507a49d39427ccaaafcc03798f15018c496f64863b400dfea63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterValidationCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterValidationCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2261a9dcca5cddb8f63fe2eee699da152a79a77ebbbad3327dfd4be9e1b18fa)
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
    def status(self) -> "GoogleGkeonpremBareMetalClusterValidationCheckStatusList":
        return typing.cast("GoogleGkeonpremBareMetalClusterValidationCheckStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterValidationCheck]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterValidationCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterValidationCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f28d0d15dd72babc269f23cfa86a0d64dc2b79204bf32673618ad0c88fcf2db1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterValidationCheckStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremBareMetalClusterValidationCheckStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterValidationCheckStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterValidationCheckStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterValidationCheckStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef721ac4e2b13ce8cf1322f1238983360af1b9e655748683c4bb4fb285cdfced)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalClusterValidationCheckStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c9fd2a889629da54c3c622cd7108c55ed57fd1b8578ee0c6753499103ab0e94)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalClusterValidationCheckStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0da2a8e7c05254da25037a2f9eaf0254daec20727ad5d3d5889de4c2c422e628)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d591c18e8b17665b706092a04fddb46f64146f1cfb8a5a8ae5a9825752b62e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32d6ee870213429dab49ae7c8f9d42a78135bac211d5c8f5aa1e2e5dbc19188c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterValidationCheckStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterValidationCheckStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c3c7db0f663d9d56716ec3246b9cb51acd79507753d62c6f28854c9b406c52f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="result")
    def result(
        self,
    ) -> "GoogleGkeonpremBareMetalClusterValidationCheckStatusResultList":
        return typing.cast("GoogleGkeonpremBareMetalClusterValidationCheckStatusResultList", jsii.get(self, "result"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterValidationCheckStatus]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterValidationCheckStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterValidationCheckStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__776c65d4af5ff9fdb9ee37e745152704f109b14ebefc375472a119cea3abb9a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterValidationCheckStatusResult",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeonpremBareMetalClusterValidationCheckStatusResult:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeonpremBareMetalClusterValidationCheckStatusResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeonpremBareMetalClusterValidationCheckStatusResultList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterValidationCheckStatusResultList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96b3a2363ce99764807c6ed038f8d74e4801c219ac0bd64484b8aa4521eb499e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeonpremBareMetalClusterValidationCheckStatusResultOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__668f2a6f45e13ca1fcca4d8d80f2630feafb8dbe0519eb6ff622a5098030bedd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeonpremBareMetalClusterValidationCheckStatusResultOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba9cc1a07760513af494a4142d456182921c969a53412ebf5434acb21ea4f13c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2002ca50b048aca3a4bdad50269b0bc9aebe455a4eedbcec2b8d2000c21b87e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__290e07b72d3ee42a0bceb4c8f98a540e965ac575e8a21e52e049960ba852f040)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeonpremBareMetalClusterValidationCheckStatusResultOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeonpremBareMetalCluster.GoogleGkeonpremBareMetalClusterValidationCheckStatusResultOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63cf9143c80c4bd8f4bf4566763cb0ec1038e2d68615b46266646b46a45ed8ae)
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
    ) -> typing.Optional[GoogleGkeonpremBareMetalClusterValidationCheckStatusResult]:
        return typing.cast(typing.Optional[GoogleGkeonpremBareMetalClusterValidationCheckStatusResult], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeonpremBareMetalClusterValidationCheckStatusResult],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15380316880f35151b76da6bcec3fc9c2a2b8ec5fbf4522265c771aabfcac954)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleGkeonpremBareMetalCluster",
    "GoogleGkeonpremBareMetalClusterBinaryAuthorization",
    "GoogleGkeonpremBareMetalClusterBinaryAuthorizationOutputReference",
    "GoogleGkeonpremBareMetalClusterClusterOperations",
    "GoogleGkeonpremBareMetalClusterClusterOperationsOutputReference",
    "GoogleGkeonpremBareMetalClusterConfig",
    "GoogleGkeonpremBareMetalClusterControlPlane",
    "GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgs",
    "GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgsList",
    "GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgsOutputReference",
    "GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig",
    "GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig",
    "GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs",
    "GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsList",
    "GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigsOutputReference",
    "GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigOutputReference",
    "GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints",
    "GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsList",
    "GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaintsOutputReference",
    "GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigOutputReference",
    "GoogleGkeonpremBareMetalClusterControlPlaneOutputReference",
    "GoogleGkeonpremBareMetalClusterFleet",
    "GoogleGkeonpremBareMetalClusterFleetList",
    "GoogleGkeonpremBareMetalClusterFleetOutputReference",
    "GoogleGkeonpremBareMetalClusterLoadBalancer",
    "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfig",
    "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools",
    "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPoolsList",
    "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPoolsOutputReference",
    "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs",
    "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigsList",
    "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigsOutputReference",
    "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig",
    "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig",
    "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig",
    "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfigOutputReference",
    "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs",
    "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsList",
    "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsOutputReference",
    "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigOutputReference",
    "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints",
    "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsList",
    "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsOutputReference",
    "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigOutputReference",
    "GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigOutputReference",
    "GoogleGkeonpremBareMetalClusterLoadBalancerManualLbConfig",
    "GoogleGkeonpremBareMetalClusterLoadBalancerManualLbConfigOutputReference",
    "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfig",
    "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools",
    "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPoolsList",
    "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPoolsOutputReference",
    "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig",
    "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig",
    "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs",
    "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsList",
    "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigsOutputReference",
    "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigOutputReference",
    "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints",
    "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsList",
    "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaintsOutputReference",
    "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigOutputReference",
    "GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigOutputReference",
    "GoogleGkeonpremBareMetalClusterLoadBalancerOutputReference",
    "GoogleGkeonpremBareMetalClusterLoadBalancerPortConfig",
    "GoogleGkeonpremBareMetalClusterLoadBalancerPortConfigOutputReference",
    "GoogleGkeonpremBareMetalClusterLoadBalancerVipConfig",
    "GoogleGkeonpremBareMetalClusterLoadBalancerVipConfigOutputReference",
    "GoogleGkeonpremBareMetalClusterMaintenanceConfig",
    "GoogleGkeonpremBareMetalClusterMaintenanceConfigOutputReference",
    "GoogleGkeonpremBareMetalClusterNetworkConfig",
    "GoogleGkeonpremBareMetalClusterNetworkConfigIslandModeCidr",
    "GoogleGkeonpremBareMetalClusterNetworkConfigIslandModeCidrOutputReference",
    "GoogleGkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig",
    "GoogleGkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfigOutputReference",
    "GoogleGkeonpremBareMetalClusterNetworkConfigOutputReference",
    "GoogleGkeonpremBareMetalClusterNetworkConfigSrIovConfig",
    "GoogleGkeonpremBareMetalClusterNetworkConfigSrIovConfigOutputReference",
    "GoogleGkeonpremBareMetalClusterNodeAccessConfig",
    "GoogleGkeonpremBareMetalClusterNodeAccessConfigOutputReference",
    "GoogleGkeonpremBareMetalClusterNodeConfig",
    "GoogleGkeonpremBareMetalClusterNodeConfigOutputReference",
    "GoogleGkeonpremBareMetalClusterOsEnvironmentConfig",
    "GoogleGkeonpremBareMetalClusterOsEnvironmentConfigOutputReference",
    "GoogleGkeonpremBareMetalClusterProxy",
    "GoogleGkeonpremBareMetalClusterProxyOutputReference",
    "GoogleGkeonpremBareMetalClusterSecurityConfig",
    "GoogleGkeonpremBareMetalClusterSecurityConfigAuthorization",
    "GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers",
    "GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsersList",
    "GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsersOutputReference",
    "GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationOutputReference",
    "GoogleGkeonpremBareMetalClusterSecurityConfigOutputReference",
    "GoogleGkeonpremBareMetalClusterStatus",
    "GoogleGkeonpremBareMetalClusterStatusConditions",
    "GoogleGkeonpremBareMetalClusterStatusConditionsList",
    "GoogleGkeonpremBareMetalClusterStatusConditionsOutputReference",
    "GoogleGkeonpremBareMetalClusterStatusList",
    "GoogleGkeonpremBareMetalClusterStatusOutputReference",
    "GoogleGkeonpremBareMetalClusterStorage",
    "GoogleGkeonpremBareMetalClusterStorageLvpNodeMountsConfig",
    "GoogleGkeonpremBareMetalClusterStorageLvpNodeMountsConfigOutputReference",
    "GoogleGkeonpremBareMetalClusterStorageLvpShareConfig",
    "GoogleGkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig",
    "GoogleGkeonpremBareMetalClusterStorageLvpShareConfigLvpConfigOutputReference",
    "GoogleGkeonpremBareMetalClusterStorageLvpShareConfigOutputReference",
    "GoogleGkeonpremBareMetalClusterStorageOutputReference",
    "GoogleGkeonpremBareMetalClusterTimeouts",
    "GoogleGkeonpremBareMetalClusterTimeoutsOutputReference",
    "GoogleGkeonpremBareMetalClusterUpgradePolicy",
    "GoogleGkeonpremBareMetalClusterUpgradePolicyOutputReference",
    "GoogleGkeonpremBareMetalClusterValidationCheck",
    "GoogleGkeonpremBareMetalClusterValidationCheckList",
    "GoogleGkeonpremBareMetalClusterValidationCheckOutputReference",
    "GoogleGkeonpremBareMetalClusterValidationCheckStatus",
    "GoogleGkeonpremBareMetalClusterValidationCheckStatusList",
    "GoogleGkeonpremBareMetalClusterValidationCheckStatusOutputReference",
    "GoogleGkeonpremBareMetalClusterValidationCheckStatusResult",
    "GoogleGkeonpremBareMetalClusterValidationCheckStatusResultList",
    "GoogleGkeonpremBareMetalClusterValidationCheckStatusResultOutputReference",
]

publication.publish()

def _typecheckingstub__c92b632ac8feae48e420ffc3ca1905bca79f48e5c362b3c91359050e75b8f780(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    admin_cluster_membership: builtins.str,
    bare_metal_version: builtins.str,
    control_plane: typing.Union[GoogleGkeonpremBareMetalClusterControlPlane, typing.Dict[builtins.str, typing.Any]],
    load_balancer: typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancer, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    network_config: typing.Union[GoogleGkeonpremBareMetalClusterNetworkConfig, typing.Dict[builtins.str, typing.Any]],
    storage: typing.Union[GoogleGkeonpremBareMetalClusterStorage, typing.Dict[builtins.str, typing.Any]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    binary_authorization: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_operations: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterClusterOperations, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    maintenance_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterMaintenanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_access_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterNodeAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    os_environment_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterOsEnvironmentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    proxy: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    security_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterSecurityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    upgrade_policy: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterUpgradePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__5e81f811311e8da189db7e2e75b8b99a440ab73c03bd7a00ef82ad275a71bcd9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f40457303082d5a005bc1cf4fcb73e12ba75ff4f75eb8de2d0694e0e50c1c05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a55dbd95fd9db05ca56d4cd4f01930d0e60692456ca01361edf6a87198c637(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1ba2ff65d66995a11902dd5af67b26d3bddfe04e86b0fb4381ef0bf5f8344b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6d9bf832b2c22a5f90f443d07700af07d957815123288e33228b88c636720f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c01c6f89522eeec1ca893222acb109dd2166e2d209c19eca68323fedbc5a1c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ffcd13a90b2a8550f15a02abb295b7f987ba357149a99943090cd27dfbf6ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__435e0bb21ea3f2b4e106c1437261cf451fa1822d7bfa57ce89dd907cda58ae11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__713eff543b463eb44b57c71091d909ba1051c80b88fe0e00238bc934975d8855(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c6a6e0e49e4a87120e6ef0aa43a1e9a3784e022402ae6b4da0d848cedc0884(
    *,
    evaluation_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a7a97bdbe20c8094c676a436ae57131d0e365db603e1281bd9b2c4f98092f0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e71c468412913dfa84611a1dc0cd6a3e26f553eacba5c7562da781140c7d1c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ebd821718e2ca8d10713b300d61d059d91d474489fe5c1afc97fc5e494a3a3(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterBinaryAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b44b60c802fa12280f045f2a6327408629756b653388eb9d14590042ad40c700(
    *,
    enable_application_logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb3d9333ba783787329ccc3448a4f0650cb7011d91383cefa302f48d7b27bde3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f08c3b70b1cb00f3ff0d46fc21114d57c73d2cc8a22c5cabdad359fe9b759c3d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c5be093a5db84c454ea0e8073e5c00f81f1dde780737d3ed33ea7ea3356cc10(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterClusterOperations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e57135b72ab24d98c14b4365df6e969b59e98126675d51a9faf4c0f83262799(
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
    control_plane: typing.Union[GoogleGkeonpremBareMetalClusterControlPlane, typing.Dict[builtins.str, typing.Any]],
    load_balancer: typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancer, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    network_config: typing.Union[GoogleGkeonpremBareMetalClusterNetworkConfig, typing.Dict[builtins.str, typing.Any]],
    storage: typing.Union[GoogleGkeonpremBareMetalClusterStorage, typing.Dict[builtins.str, typing.Any]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    binary_authorization: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_operations: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterClusterOperations, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    maintenance_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterMaintenanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_access_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterNodeAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    os_environment_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterOsEnvironmentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    proxy: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    security_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterSecurityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    upgrade_policy: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterUpgradePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0671b966ed627b4e240b80e807ea5ff9eec9e5bd61b2e8e1199e5b84f17fe55(
    *,
    control_plane_node_pool_config: typing.Union[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig, typing.Dict[builtins.str, typing.Any]],
    api_server_args: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgs, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e0d6333e314c17c3d2e5139a437e854bc16526be051f6b86d8c432a88178e3(
    *,
    argument: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9199153fbe641f2857b6af73d11605eeb61ebef95e6ef95814b2256ec0e4b5c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda8d167522b928ce8e5f4bcb8438f3d1bb9d805edfb6d58810e3827a81c9b5b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4075543c0398c2f7813102bba4fa807a4a0fe37e3b6a110499f9f79725f4433c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6514b05a7716128ad8e09baf7790b477d14fd93fd1a46bf0a26214923ee8a59b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f6ce95adcc1b3c7db08e8c8ea13dfcdac87b3e11868fb6d2ad8661a08906cc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e45ed49a2085a664be0317edc5960f5d91de32db351d9db5f9ff130a55283b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e489e365658959a851d538da8f7f03716fe6bca79965d3fc8cdad8a6aff22423(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9692e33603b43033f6d4b7ee1816cea967f00e0ca025d1c4a06b22d5ca565de7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b700515a4446545c1ffeafd6b3eb44c801c30785a58f64854ec8ad2fba9a334b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfadc4e510afef6793a53fb58ec1014f84b9f62f0900857961bcc835cc87a022(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0dd7bfec9f46cd270d15b627d3373ed8155478e5d75523c98bae47809d2782(
    *,
    node_pool_config: typing.Union[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2812487a9c42ecd4dbfeb7670f5fdb8f32728abb8a25fba35961b0339b7020(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    operating_system: typing.Optional[builtins.str] = None,
    taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21fee69fe10deb8278249bac4ca78be98881a882e0ffc7535f873fbf24258e26(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb8c3270610cc1469c2150dc539c58ea6dda2ceadb7376df427a13e4d2f3b717(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bf84ddb06b21af5c368bb1f821b33b576fb4b44e5c71a109bd6f162080bb60f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ee3a2a4e7a16ecde3d349db460bd0ed8e6d0eab4febcaa9f30eafca27d806a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a046144a6194d2d8bac35979e178816f1b7e96feafa9de8a3744552487d673a1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3473f36ddc49f495b7e18240e3c724a92aeadf01f4395ec4ba592c415965536(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f93568d3c9b2cd50291aad96ba3fe27e7a382a4cea4f0046cefd5393e31fbca4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1fa94043467cd235ce99c92446e89688b49a3676ba81e32d3d1a10d58504666(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06de931c6bdc057a9af30fb1df595cd2a83a4e0caffae8dac65e5a3d969c9701(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8bb89a1a6d858b1114d65e3b293c01e33fb806f354e25afb1bd76a19424d967(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__411ca47691cd871bb1f4138ab7e423c53dafbb973146deaddaa6d02ac02a061f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f83002c8b9cf2c6dd6e052b9206963d1e26a1959078e70a8bf9578db19e69f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c52044b218c1e3580d89ddd1c5bb289d3759def3097980518d5f1317a4add1f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__594537130a8e8784de579207827f1ee8fc8e4406b8a74963cf658c7e698339ea(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae3bcd0fd160c068a3b1bb2a5466f1fae0f24ea8e3585040b6f99339b036e2c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc1e858aa41289b6c1e993e5bcb8c1f46566a8a99c29081e960901c9a5046f84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__109b2d9b6f9a9ba065034931a28e7776c6c8b3f8a76c976eef2b0d96d4deed1b(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b4e619f5c7702356a70d1560631d856222643782b9851ae6e57da8469801452(
    *,
    effect: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f069f41928ebfc9591d36b3ed0e9d03d4e0722c587852af68105f4cd4e25589(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58bc33ed346272a3c922f59aeba2af0d0700ce3c2a616c558ebeab3e189556a1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8329ee3236000646ec2f4d82ca804b10f8793bab0e46a0820e069ed745bd6ce9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f61025c5cca6fdc1b2cbdec192b7c25bf7bc44aedd3d4857d8148e1dc87e91(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c458c6265362daaa85a019eae69f3ebdbe312c6a8f313a75d224d55360f6ff45(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af5cf1c65e025b8bac9d9df8152c0f50e9916e801960db68494d6cce81914216(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__707e22b2648e6cda005ee4fe9e3d392d66364c9a9a8bacde5ce257fff5d03720(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__791c6d612137cd9ac380d0082ef8160292f4fee4dca73de33ecdb033b058eb03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__769a270f449c1c1a5796b3c8699990510e960b4284d898db422d48f6ba896321(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b080db73b46f74b686e099812db28d1c801b2e6d1ade2dd4f29b6c29bb884b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b928db085dc98f4bc2dcb1e982c2086b52a9a14ea934a02577df2b6dac3beb3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfigNodePoolConfigTaints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11aa3ca28ea51da1548e2f1449102fc72b2c2afe1b773d0eae2d97e500437335(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dbb639a323ebae16d4861642eaaa218bb04fefb903568dec9acce57f8e0c522(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterControlPlaneControlPlaneNodePoolConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a4658390850e18df81082215134d1448b1b79fcfc890127b1f515533d894860(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4efadee33fe8de04bd66e158711c897c53e5bc5def9aed7724c3d9f4c4a56b12(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterControlPlaneApiServerArgs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8371dc3d6489b130362069bed4f608c0084f8537e6de983772f90bd3463e2cd8(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterControlPlane],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22279408a8b5f24d79ba4748b7e93bdf9060f528cf2a994fceb59879d6067a03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4285cc6fa5c299cd44ece314e3b12f7a7898f145cb2d852b38f12e36be59838(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff0359e5677ec2ad39ce0af17a3c2b6545a0c23a15db3fba1dce54fc7d4c8bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54442a51f3b88ec3199dfa9c932ff1ea2b73e3023560380e9c63edc4bd108a1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdca7a316a5806facc1b42ca21e71602f8652751f472be3c2d88250abe3c6176(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f0c54eaf1c4a0e846aded1e8802d91c34f35a424232a8461313c237af31ddc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bd9dada5f44c4c902ead604d5577e5dcffaf8b7cc57eb5acf03b86d06fbe0d1(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterFleet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d855bca14c376091eff156e16b603e97bc6c09eb9e18259de2a2b1aef1fd66dc(
    *,
    port_config: typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerPortConfig, typing.Dict[builtins.str, typing.Any]],
    vip_config: typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerVipConfig, typing.Dict[builtins.str, typing.Any]],
    bgp_lb_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    manual_lb_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerManualLbConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    metal_lb_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be7ffeb00433c163d93c5c4129c1d6d9f07ea05d1cf2a4065d116bb56cd69e21(
    *,
    address_pools: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
    asn: jsii.Number,
    bgp_peer_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs, typing.Dict[builtins.str, typing.Any]]]],
    load_balancer_node_pool_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d304c97fff7acbfe19df5bde5feda498c71ac25e54141dcc122ac96e1325fcb(
    *,
    addresses: typing.Sequence[builtins.str],
    pool: builtins.str,
    avoid_buggy_ips: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    manual_assign: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb4eba457d64ae2363406a05e820977c21c0de27702d3b960d8176171e74a61b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5635e88bc6756f4f979c22fd30520654f3afb78815630f37d86c91028faba2a2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb02bba5f6c27b0f261cee82347a0e5abcc13d52e5da57ca08caf5239675a835(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6841d92728488a40fbd807b3ddbf9b660c4961d2ec1268c84994cda1d33d6466(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2753ff01833e882a853934a070845f3f6dfa2ef9f660fb350aea71875d97ed42(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd99c410ea3692ea8e94e241280289ef6f3c03558791c7248b92ae183cdbde7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b308d2c0f56308dd9163706859cf530da6a264708707d55e1ec09e09a3ad720(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04b412e5db1f43606636818bba1afecefde3ba7376322dc5e250f2af3476847(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b59f0a30e7228fc0ede28c1a89a567385c49b0e3bb643cbbae44cc03c325baf0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20e4e5e3f9d2251c2ae883b2390c8688a3be4461b7876a0251eafcbea60bae83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c9029e5111613555090ba81dfc832c4682bb329e6e05308dc1fe4be6222622(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32e2b7bd68345b9e10c0dc89830dfcf13ec264f3bdc15578f74b81d91f02dfb8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__723b92ad16b1e9e554edc991ec438ebfca7f35275cc93ef7c21196766456b13c(
    *,
    asn: jsii.Number,
    ip_address: builtins.str,
    control_plane_nodes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe5ace4a066aac7ffb8c35e27f2341e839e2a589ca40046e66f11b0bf95e1523(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbfec941e164c31d4e607dce9068b99fe61ed3124d58cad1b91c9bee65833dad(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3fdb0a332653a41502df0cc2103c78c33366188aece403d1abf09cb9795736a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69cd091275b18821db4d64ad881e25b904930401f517dab59cc1402658fc8c2f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cce88a891ed2690c4730d5ae15478a0b78d563ba43a0b23ca3f6e0820312277(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba194fc3e6d3c66cfd9023b2a30438c7b1f8caa0fa1bd415bef0a16ead901b7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d9c2fa3a9d846693cb911bfe190048441841d01c881c556be3a6c72291b2ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18944f2f48a5c02ba3bc43fba428fd2db59b22e1f0ddc3108cf7dfbebc25522(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ac6aef3e2ef6ab78c43dbb1f33aa0fbc8f37f38cc7f3093a16dd3a616e36db(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd61dcab9f652f00ae91f7a2b80cf1407f2edca0148a2e55186e0cdf4fa8865(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cad854122b565810d2d2d7c1876e1d44b5ea3f6b3459fd7a5a7dec94c49140ce(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b0f7a02f7b7a00ede73b37b8f58d40aab0d62b7ed4f37353b4c1443bce25e2b(
    *,
    node_pool_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e7c3c370de39cfcd10ef0bb9871bac334799556923a0739dfba62f09c3afa26(
    *,
    kubelet_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    operating_system: typing.Optional[builtins.str] = None,
    taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f0ff29c5f108a5adcc2238b068e64025e5223e71d9c1cbcda26175a46655c0(
    *,
    registry_burst: typing.Optional[jsii.Number] = None,
    registry_pull_qps: typing.Optional[jsii.Number] = None,
    serialize_image_pulls_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca65614485c3443e093341ff96db6877e8a1f372bd27b39ed90e75beb8efd14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__560dbbaff2a4d4ff23e63c552c3502e2bd804b00d7148019239d11c3f53d81c0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cbf179a875ee38e015dd966b3fa5bafcab20b9f647d9c981db43eb187278fd7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2a3b8d13cfda718f63a282d4f00cbbc8ffa19fabd6b042288f6dfacb04720c2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d143eb4e8b72518bafda4773a736403cc9c56c8959bf3603718fb1a8e226946a(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigKubeletConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__895729f2f8823d9de5f9a516cc3ddcbf47391a268df45197abb619fd7675bdc0(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18681dc0b543dadb47e63ba97b8f83dcebaf1b70df0cc0a817887af8c8a4f6fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a264b8bd820979ad7ccf8824b163809370101019db0067e2c54ed1a166abea35(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41169e65e60a7f3d457e91506636961758c4dbb4cfecad81ecb6d9ea9ad5ae3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65e160c3f6cf93ef485eca8ebca1b3c6b37bcdf21deb098cf95399e6ee5a8cf3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e6b65cd683a831e7b2102ff4a0555156428a3267229b121be7f4f6d1f95b64(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72a23cbbe7c4e3436bd3d6322cd3775d812d81248c87612041a480abf423cb25(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53d98fb2fcf65fb6f1796cccba773569d6a5b82958267a43d99b64c2e0c48d52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eea615e9ee87dda18fd15a3d203345e96cfd9666dada68275679012a8b3507a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd8c6d9cb201c6766d4619d93aa16a985f24649f1b2741a12d170c7b0cbdf3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f89025b70decf4ed2cb2e6adfea23d1acfb8240849ebb7e5b5cd0e9d812277(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e866a8c0c34fb91cc639f63f3cc3e2d82743a07ed3d97bfbee90841df932e7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579a22421bae9a5af4a0d5f620465a4cd62719f525f0178dd054451907a08b1e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6047a7ce9f5c065e65ce48ac61097ca93d128341c6e814f8432c5029cbcc23e5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f23ef65e2f88ccc379def9d731360920fbd36cfed27474f936ac643aadb6a50(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ba658d86c01cd3f4e3d0dbc22b710b8ee6c13c853bb2637d930a6dc0357eda3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e628a15a0ade9bff2d85dde0a609c5bf01dad9b6a2b287b61491ffa7cc24ec36(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2126f2f0f6314a52ea00e2cd101d5ef071d6ead7b5f2e995a81a35a9ed61154(
    *,
    effect: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50f9954d5d360fa79ab25e5357bb70bb6a974e733c150e111f11539a537ed4bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11ab82c55005c65b100abd9f8ff5977750696b6ab3e29575660cb61fc738645f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed79692107c5087bf53e301b9bafc40e4dc06924b13c87a1213dee05235c811d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e67812ffb3412943026b8f2b1f40edb630b9159a0f87286f392bb753526ffad(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6dab0efce4c40f1c4bdc9bd62a3a7677904bbe79580cd747d318a13a3b83c09(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0889762c980e9a230b124b96a82178176c51d738a87ea736e408bc45368ddb12(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ed2756a8539e555fbb41aebe4f74f037656f4f1adff9e6bad6bd833c411d570(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__250a5a5c9e39fc7fb47a69aa4dfb16104bbb42aa85ebb61ff22161b9726847ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__443ef3a7238c2264b7833336351041192a508ed97426903164c8a47c19a94d98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0476c9fab66fc33b0266cb0ee8be867ae60372f9e5cb39753e7fe8e38d1d26f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa3ee2900b68738ce08c9cff8475c0613ac6e5f302c23f18be83ea565423b17(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b98c2a878074cc365f527ea6b7b6e58441cd099d20da7cc8603cf2c3778d257f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17d9c9e7ad32cd6001a98ca1912e5c2070bb3e3a49351c395987d3a8172a6c14(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigLoadBalancerNodePoolConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93319d1f1fea3a629368a2bf3bf5790a64c5688577e5a9a8682acc368a98faeb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c6853e1b417d005ab339af4c56bb568261a9ce60b5b34b15f0c975d3cf5d7ef(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84cf1950569c75eec27a075c01eecc5db13fdb9db77f0163af07d8b5028ebc15(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfigBgpPeerConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9cd5d95221a6d28473297876afb3c8412913b291e5d80d6b539ddfd7c5875a2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7553e6c9812609886b5811053a5ed57c2c4155a0d81239753b69a94fc48286c1(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerBgpLbConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d43ad893b0309dbc091651ea286f50c1dd77af915ee980926f51dce2ec48ff12(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958b2dfde134d336e25b8ad7a3d275e459c5e268170b3fa1ef088daed2f12c17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980eaa7eb0c1c64ae4a180584450f423fd6c7030da0bc846cd30e70f6db8ed04(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d2ef11282875fdfc9f0abce6dab210bd44a8ab7f01bbdef3a9958f9b4bd84f(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerManualLbConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25cee9680c23abaf06c224eecb97c6052474b6d2c4671540c628e63875075d09(
    *,
    address_pools: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
    load_balancer_node_pool_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bea8fac4b1c38260b701dc2b6173d555d42507338503e48095f4480efffd6215(
    *,
    addresses: typing.Sequence[builtins.str],
    pool: builtins.str,
    avoid_buggy_ips: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    manual_assign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53089bbd1d94ef8ea8bd3eb0989fd8efc1149c34550ebcb1b3816d428bc5af40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eebe6f984713d18cea1bb22d63f9e9c304ea83187b511d88c2cc29137d799957(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fca6a6c2f22862e4501e2a8f7bd075f782d6493a6cc55a77ba3b4c4ff23a5f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ba596e0cbf15d6d791ffade0a1cd1d44046f49890c5c0f54ea5139fc92a4df(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20d4aa9cad4107e999588c48bc6a3197dd0e39ca989f9041de035fed70c4579a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06173b64e0dd4171ed1057c6fe2afe71761b961f4b040c6b0e427209155f863b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__869ccaebd509f7e2b9e51b7cc4d0e41c9bc5b7305e6210f50fb20c2a885c746f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9db322bed31c2ab9b8119b3cdf386b3c4d921a33fb4229d291f75cf049d3cc5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a592b2ac51997c812db4d4e0d44e635ff616a630bd973c50e4bf8debb893a4ff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f90986e5e1149fb1344359770c156288b218120ff0b998233a300f5798ccbdb6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23787282a7eb607e13e5e65ce997846c3d8d18dad724235064557807dc0541dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67e06696f49a2bbd383847deb4b8ec0642123545a260e2e3fa6f145e7a202ab9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95177e6ebf4efbab8604701cd09876b0ae2fc6c6878cfed14a518a3f4fb0e949(
    *,
    node_pool_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c9ee4298d2d73b8c81954089b964bef13b047b59e2a40dd50f51f4e1386f06(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    operating_system: typing.Optional[builtins.str] = None,
    taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8abd57bc1a0f81cfddd704e9c6522700cb18de09d2b3528bded01599d5aab41d(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d2d8251254504efb9b44361ccd1fffdbcd2f299427b10407143fd130931598e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc5b61b4ed593b8cb92a17d88d76a73cdadf2af52feeb2f92633f15b0a3c0001(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6949bcaf782e9763659a8c9d1efb611bb754b5035ef4795ebfeebdb00a0212a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__672e8422a761f922e39d1952c82a60d213041e7607e2824bfa1876ac1c55c2c0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff99183d05a31cb0b54697e8b37dc97f4c3e2e05e7cd13f033f7b30770f258d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11c67d8bec15fc9fce77843137d9a13bc5014ed442e8c397d081e5bcf75233c0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb2fa85f34a4a700d5a1ad1c8a619d745bed5ad2aefbbfc00dac878340bf2451(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b2fe8cf6bb4fde7128af0a3beefead8c5e6010871c4c6a3e8764032d675a707(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0804cf27e97c57041ae5cb85f0a19c912d860737bc805a84c04e25e5631d33ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b3b9109a7ddaf453f9f767ccc9cd09f39881d7deacb2f942d266066717e31e9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__837a9d486c4ab65705e15ba4ff9cd07699d1048c7eebcb60f5e10175355af0b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e42f58b7d8b5334fda934dec9e0d20efc5f4e9134a4bd43a8a934acb38d6e415(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__474ed85ab422ecf75b4dfaae110a8c72e0008a377d4eb5bfcfbedbcfa909f18d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17596c0914c185c36629d4c59a212ef9f4c6c9305c76cb9b18b2dfa6d36f4beb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__852b55b84d2965dab551785e9f6b835302c5369341ddc1b0d0be7ea3859906c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0799974094eee4e87c60461698498813bc16f1cbec16dc72767de30af0da7b9b(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5557945deed44740d9bb66ad37d33e75fcd4d3837a1be60ebba79dc7ee8730f2(
    *,
    effect: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ca8b1b64b9d185503d54f766bb4bc3e91c85b8625d3fad208d535c4ef56bc72(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7107d3b203296e440a547cc9504dab4c5139b771c12d681ba5fbf8f74a41b285(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5556ee9c0abdf220291a8c0c98be13ba1fc5a4de624d4e28cf54e1d88a7e887(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31bb2207de4a6f258d67f833a9b99e9de0c45402c42a3ec2a3732558dfbf53fb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__282951ff7bbfc206da364d0f1b15672a934df032e41e227187bed89bee4bff73(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd47fdb71017772b6da062c02ce1af13c1821776993e6fa0bfbe5c6b05e2ed8c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f9c4c62b2f65e934de82206c664f1df83d834b633ba7a964aa23352d1e1073(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__756d6c256f3b59636cf20aa8422b76d8d6ad723e76098ae33110b410e096f496(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37a0e79d1471145cbe07b535b627037d14cba9acee66c9d363c12e7affc8ce7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e14c69f00a5acfca60cfd967ce8466ee6e6bd22c38d48137eecf7edeae5b70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78850d81da3729ad5bed7faf25b10eb5ed79181feae7fdc724e15924eafc24f7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfigNodePoolConfigTaints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c5a594c868453c13b82923f3486bc716bda3262ed14676856570de63aeedc6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68d5cc18bffa4b105947c18363215e76d567657315a00f49bab936366b69a39c(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigLoadBalancerNodePoolConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf41010f355c2aab9350c312c7be83b53cb228ea4a39da0937beb9defc6ea402(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01e4671d285d92af178088ac5c7cb746fab62bf880e4a8b574ade45c7d4b0419(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfigAddressPools, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e1f1ce8ccce8139f509cba1cf46475044e84a8fbf07ce92463391bc2f7434bf(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerMetalLbConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c0c880cf10fe8475ec436824eb3f9bd6b0877f2659a4f2284d56a6912d789a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbec04eb5e7f691993ba9700ab0c29b12696f341fd4b4e045566a003f47f6a11(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a8b81d7c556ed9a187559437d4ae3f8b7bcfa61124cf41c86b93e56f62f9bc(
    *,
    control_plane_load_balancer_port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e1dbca87acabeaab14d05acd47fbafd6e41ff50697043cd69edc0a57b870630(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e6bd609e36f0d62b443eeec1c4870a2429fc969710a4fc6e5ee93d9dab8f392(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__139cc13d4b7eac22141c6cb47eb026148c48cbd40d74a68bfc740f490cd80dac(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerPortConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6586189e6fb70544a028769822e75e11b3528dc95ff22440e6d3fc3ee93b370d(
    *,
    control_plane_vip: builtins.str,
    ingress_vip: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd37c8444f1da74a85b30bcec6e4232a0b50a76b35007d9fd6bc82906c850945(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c89d40840ef940cd5f3f99b8de30783302922da6d27745fb5c93513b672d178(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbb4b6e5af24d79b36791fa77ca74649fe60b99db77861fab15831e9656b0d1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ffbe7be7bb5873af1598b0974e2192f11b2bdc25e85d48a4ac54062e7ff2a2(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterLoadBalancerVipConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c24561c1f568604f07179629158bdd3e6dcc7182b8913777d56f059663657c0(
    *,
    maintenance_address_cidr_blocks: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7046898fa4b8ef43bd8bde09d03967844f3b741732b46fc00a6fd448c5647688(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50adb55cbf8927e960d6ab8b6379a8cbb5b0658f36ac02dff994a288768bc55a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__564fd4308fd54d1a62e8a09436824e9cfc9606fc3b3060792574078e19e1d128(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterMaintenanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edeb0597d0913b87bfac2400a90b7810911efe2574218d3fbe1b59162062b515(
    *,
    advanced_networking: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    island_mode_cidr: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterNetworkConfigIslandModeCidr, typing.Dict[builtins.str, typing.Any]]] = None,
    multiple_network_interfaces_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    sr_iov_config: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterNetworkConfigSrIovConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee0e1f162eb21e1c8b65f2783435b092fdd482234d96a4849ac038ec14c64431(
    *,
    pod_address_cidr_blocks: typing.Sequence[builtins.str],
    service_address_cidr_blocks: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__add918a5d286b57ad42f0de2db0fb122d700356cfdea1b366cb5b540c82de24a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70d66aa5ffb67fd6f068b5afdc6a6097aa7503a8d6b05cd70fb3eb3a6a88bebb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bcd9c2c0d672d084018d09fa8ae71ae930b6a1693fe1e4a6e9bfd5bf6d29ec7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af16330bd85273e02978dc9bcea61f85a2f4648c521423133718c32a86134df(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterNetworkConfigIslandModeCidr],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51140896f17b16576b941409c5642857e89e43234c20b09e829c0d4e822dbe72(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f93da8b0786f3ea212f57377ecefe1df56314140dce3b5e17bba2f5e2d91f55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d6c2f1534bf1161ef050abedc56f655666dd3a67ae6fd3d536b0ea0339da8e0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3620ee7acb652e93f5f982f1c98d9214bed54aa28d5dce443f4b9e0eaa6e3b9(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterNetworkConfigMultipleNetworkInterfacesConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dec635ef6c3c3c9434356d6cfd5d926af21837f03f5ee38541270939bcbf14f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62cc73e26bf1292daf1faa280349e01076b6c14115a2789261c8fa9f3f648a79(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c239dc5cca9e16747bfb9b55d8d67895c50507ea139f2da2cc442a7c3ac1d470(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90123c20bb573ae9d58bc007261c96a5d0a42daeb64ae89d923335b051875246(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3059924cbb5a593c4871e846f0e4c891a1fd2607cc54283d9ae9a63b9ed9cc0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c57655287d9bf7c62b1ec5e925b0b24898f7e87f9edd6ef7503100b19adf8f56(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4802965f7fdf0a2513c73fcd33b7146a89c1cdfefc7ac1670891cbef9178d9f5(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterNetworkConfigSrIovConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e3ee7686008c562e7d700ca72c11ef7e8cb17fb464ca2b1bd2fdedb444bfd7a(
    *,
    login_user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5383e09a46f928ba66e0872756384442ee8adee78e3b4e1cebe0e11403f68f36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b6c3be164e8980a09437aef00cc7a65b19f94819b79924bc4d35a423a07641(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d4c43cc918f8c5a64a07f9a4539658b30932522ac2054e15b2286859e6bbd1b(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterNodeAccessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c3b7948db134cfc574695d2b889681b62f0050d14c57c12c716b38afe21248(
    *,
    container_runtime: typing.Optional[builtins.str] = None,
    max_pods_per_node: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e8e6ca6dbd2711fe88c6ffeb97d94d7853aa49a0829a3d652679a8e3b3baf0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__302932c4f924e9403cd2d3145463b4498af01bbaac30eded3c16156627eb4dc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5876c8730f600722d76a2470cc6955ec3ddff5c2a821b6a10f22902fcbd20a38(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07b73f112fadfb7549e9a573f046b06447928903cc75f165a1d578bfd2bb89e9(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterNodeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d60d098bbfd82d86e4a633f4fde5f6ce0545ec50b246d596f5590c1460a0d852(
    *,
    package_repo_excluded: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dab879d9bdf6548d416e2d32cfaedf1e63fd7ec952619adff74c377c5c8280b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__329be9635343834e06ac1f6435e191314ec6cbf27d3824b8ed7d806e077d76ac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b53fb178f6dc20c036514076a5e71ca333fe43db4596b66e11edb8ea183abeb(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterOsEnvironmentConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5321aec0ce28d6203c072c17bef5227f4d2a60675922d6c0bb1b2efd51920c4c(
    *,
    uri: builtins.str,
    no_proxy: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d32631d372d9b13d03ffca4f8e240d631b8399ddc780e9bbf22bc2c49dc8f12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f274bfe0ea767ac6fe29f90ef9635670d63d5c4e3c596b8cad6eacc0a87c5a06(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388d68823583b33990ec466353eb90bbbb61efabb8733a14d773620a50bb54ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43468f0abd247d79bd2793e345ea6d1d8bf85f0560cd02b4404e5bcd6fa04d65(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterProxy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__589eec8265976c0a9c794eeedf1d8a02097eb84e7a2eeba9a92f7fa599b61c9a(
    *,
    authorization: typing.Optional[typing.Union[GoogleGkeonpremBareMetalClusterSecurityConfigAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d23a2cac0fdb5e3246dd516058cd00dda470b6b31803e7a3c858445c42e84b7(
    *,
    admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96befd2d34fd12cd2c252686ed5af5bbb60a81d2a5f0b067e70fac89a8728a4e(
    *,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c80f8b60730fdbfb42ba10be4ba94ef9d76763629ca80a23be3e98ebaf0de48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62fc9460b59e8070a930b82a284e2cba1a1244e614adee8ad676189cae41fefc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5bd6d442ec024c7bcd99f5a85956d52dba18ce529d632057766144ebf0c45c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4477cb88bca9b486f2a5bde1c450a9d8d69cfb0fb8fff3a57b7af0084642c84(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2edff9966ca9e15908d341fa18bbe90f566349e8293d468448c273311ee83c1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7e1d1335e9c00f757872d78d3797b53cbb06ffee2fa2be720e8c8f1c54d4501(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a4f83bf151497600503219b2fd93563edffb7663478d8fd6b2688bc2ebe160(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8501f28e6dc35ac3fe500b13f55047d7f7dcaca13897ee6379ef4b352508da16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e5a43c02a857824d62b9b4a51f47b69dd4c275c28ade0cf2198cc711da6e30c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc863ceffff4f058c934ac20d5fb73a98b0f6793465ae85c830bb14ab7cbd68d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67c220374e96cae09ed408a465cd5a1da09402df553f795d38389b6459c55e93(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeonpremBareMetalClusterSecurityConfigAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dffd715344eacede7018ba90088b5ff79f0fdac268a98a606e4f7011040f3cf(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterSecurityConfigAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__561f567c20280e05a9ac6a8d67ac5ebe391efae35b430ed308214579f7c29017(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0fd31f9b90ec9bf6ac46cf770cafa23db4977936616d3bda65dfd6917286a2d(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterSecurityConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8ffa288b49b594ae9654d684187de929f9bd643a7a82838370ea1067f73deec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c196d01ac32735fba52de05c0165afdeb8ac9808de93ca2a8663ceff70ac5219(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f449beacfcc18f9950a81af4d8ccd82ee816d6d2974349b9a2e6a653ed6d84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66ceae606a6979b59021805ae1c266147a956dd6b59d57c0c13cdf9c6378397d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fa509cc421f226dbb29073c11341679d405fa06c5fc63cff1ce5a937c58e488(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7147d1dc23da403b3ee218ecfde666e298fa9b7b89e4a3255f0531f7501c3be1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787722d6b7b08fb825d55ef59dd0b6391dcd49aff8fc8460ad0047358a0faec3(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterStatusConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d33000f6bd7c5e2bf38077e70972fb5035b49bbe99a2df893d69a11ee16a5d88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e99cc6dfe64380047dd9c84e61349f698bb0398746504d421123dc2d4caa158(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e8ca6d4640ce76c13f7be5dd6075373912814b0f3be41ea73885cb0dd369c68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e35e9631b66d22afede92413a83f97a0caf1c4e57afbeed48630cdd53d569dcd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f04a00559bf84bb4b7e5f1e736e0316c7fef865896d963d379cabdb8fea40581(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e75bdfa6cd10b1bd89cab0feb10687dedade338ba62e18510099f99a5fe16c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59814935b16157fb988f2cb192de4092a5d589e9ab08c39a0f72936c30b3f286(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7845dd8d94ef0e180322d7aa12d596a1794e21ce9c4165d3ff994527a07eec3e(
    *,
    lvp_node_mounts_config: typing.Union[GoogleGkeonpremBareMetalClusterStorageLvpNodeMountsConfig, typing.Dict[builtins.str, typing.Any]],
    lvp_share_config: typing.Union[GoogleGkeonpremBareMetalClusterStorageLvpShareConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48727c5e182ab68381253ec34dda9685596e6c483de5555e43b5e202ccf491d3(
    *,
    path: builtins.str,
    storage_class: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__941884b99cea72fda3a8a45528a4fbe18a0bcf0e0f38e5ff01fdbf470d1345bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f750f8e88dda340bc0b69760a6ebbb8df5aa4b988cc09e3aef1387b02460779e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b97289f8299e24a9c63049b137cbfa049aa4b3cfaaa61e1705353fb520e05ab3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45d3cd634b7bdd39704626ab5faaaef4e0116760fe893666228529ce12d2ca8c(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterStorageLvpNodeMountsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fd65dada97ea989ca852a0d0d1c93097382fa2fb98a2b3a98973140733c6430(
    *,
    lvp_config: typing.Union[GoogleGkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig, typing.Dict[builtins.str, typing.Any]],
    shared_path_pv_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be8ffbc7adecb77f4e97b1869f0679ba5204835bc79387e8dd45b1e8177db2b2(
    *,
    path: builtins.str,
    storage_class: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c65074e4cbdb4d4d37ee72b7eb68cc50108f93b1a63e177e553825fa973b3b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b542997f8450ab88d4af8f46fdec57eb08d984057665011a28f14153fe3e660d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdbacde9c9c07589dac8f3ee583f56aa361b5cb5b73956c183c094022e677605(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9750039a0d83daa01580f8214a6f7c932d6feb858f3358df04dac0094dbebed8(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterStorageLvpShareConfigLvpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__261e8cf8fae5c0d3a1a4323eb60a8ea1e0d897fb25db6e313f6f2c699f195f19(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3445f64eeafcdc19167dce373be516f4c435b362b93013314684dd1804623004(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a422699c8f3409a718fd6b76fbf793513e06aace45acb78540c3e60cc45657c7(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterStorageLvpShareConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c5318d2f875a32405b27d8aec94f8fee43353e74fc1e53c762df9c8dc36796a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62c520ebb6133b0b30cc2b32e436c82556141b51cebf165fd726a687d10e32e(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterStorage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__545cfca03968b979fbe2de91c7a53af4c3ac461e2e93cbeb1f6a35768316b5f9(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5311a3823cc799c21cceaf3fcde5a35ae8437cd68bb817224cf3fcb631d2bd28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78bcbbbeadb0ac16beabf3d50ef89c7f9d87e2ce333a47cca2ad8b38b9d11336(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__023f2fc58454afd473881545d97a453e404ddc0ed36bc0f8266c9a84ee380ac4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b486dd08b39e31272119412e204c034d828ab4739e15a77b0d4d7d82dd7e1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a99c5589d35fb02324204b0986ac0318a4e3a811bfc0ab9ed90eb11624ec10bd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeonpremBareMetalClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da27391b45619f050a3e687c07b9dca8ee692d0340642bffcec95f81199d2f8a(
    *,
    policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd1a2e5bb139ae05f8facd15ab9abb0fc087428dcabf77b41daf11ae04d5dab1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44060993cf8c89602d89a9d834463300d4cac2bf2cabdc5e1e421a385d0132ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2f8b5a9a70f5d7a4dabc755fa5c81e3c989fed202177a3872c1a432fbace31b(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterUpgradePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8a539b2744cdf1578b998b87be6f8d932147fc9b29c57615c583e9f5c1894bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9464e390da70d96345e9b4d85636ec7514763cb9e3aa32b0e6da42dde91aa3fb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a00e9b712305f310f4aaefed7e4ef2b55cf064ac4f01a68ea3bfab1bdc7677cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d27c0280edfcf940cce4897a28b926a977c92bc738f6ffe2802822421152802c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce9edd36a921507a49d39427ccaaafcc03798f15018c496f64863b400dfea63(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2261a9dcca5cddb8f63fe2eee699da152a79a77ebbbad3327dfd4be9e1b18fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f28d0d15dd72babc269f23cfa86a0d64dc2b79204bf32673618ad0c88fcf2db1(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterValidationCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef721ac4e2b13ce8cf1322f1238983360af1b9e655748683c4bb4fb285cdfced(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9fd2a889629da54c3c622cd7108c55ed57fd1b8578ee0c6753499103ab0e94(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0da2a8e7c05254da25037a2f9eaf0254daec20727ad5d3d5889de4c2c422e628(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d591c18e8b17665b706092a04fddb46f64146f1cfb8a5a8ae5a9825752b62e7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32d6ee870213429dab49ae7c8f9d42a78135bac211d5c8f5aa1e2e5dbc19188c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c3c7db0f663d9d56716ec3246b9cb51acd79507753d62c6f28854c9b406c52f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__776c65d4af5ff9fdb9ee37e745152704f109b14ebefc375472a119cea3abb9a5(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterValidationCheckStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96b3a2363ce99764807c6ed038f8d74e4801c219ac0bd64484b8aa4521eb499e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__668f2a6f45e13ca1fcca4d8d80f2630feafb8dbe0519eb6ff622a5098030bedd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba9cc1a07760513af494a4142d456182921c969a53412ebf5434acb21ea4f13c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2002ca50b048aca3a4bdad50269b0bc9aebe455a4eedbcec2b8d2000c21b87e0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__290e07b72d3ee42a0bceb4c8f98a540e965ac575e8a21e52e049960ba852f040(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63cf9143c80c4bd8f4bf4566763cb0ec1038e2d68615b46266646b46a45ed8ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15380316880f35151b76da6bcec3fc9c2a2b8ec5fbf4522265c771aabfcac954(
    value: typing.Optional[GoogleGkeonpremBareMetalClusterValidationCheckStatusResult],
) -> None:
    """Type checking stubs"""
    pass
