r'''
# `google_edgecontainer_cluster`

Refer to the Terraform Registry for docs: [`google_edgecontainer_cluster`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster).
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


class EdgecontainerCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster google_edgecontainer_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        authorization: typing.Union["EdgecontainerClusterAuthorization", typing.Dict[builtins.str, typing.Any]],
        fleet: typing.Union["EdgecontainerClusterFleet", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        networking: typing.Union["EdgecontainerClusterNetworking", typing.Dict[builtins.str, typing.Any]],
        control_plane: typing.Optional[typing.Union["EdgecontainerClusterControlPlane", typing.Dict[builtins.str, typing.Any]]] = None,
        control_plane_encryption: typing.Optional[typing.Union["EdgecontainerClusterControlPlaneEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
        default_max_pods_per_node: typing.Optional[jsii.Number] = None,
        external_load_balancer_ipv4_address_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        maintenance_policy: typing.Optional[typing.Union["EdgecontainerClusterMaintenancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        release_channel: typing.Optional[builtins.str] = None,
        system_addons_config: typing.Optional[typing.Union["EdgecontainerClusterSystemAddonsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        target_version: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["EdgecontainerClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster google_edgecontainer_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#authorization EdgecontainerCluster#authorization}
        :param fleet: fleet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#fleet EdgecontainerCluster#fleet}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#location EdgecontainerCluster#location}
        :param name: The GDCE cluster name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#name EdgecontainerCluster#name}
        :param networking: networking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#networking EdgecontainerCluster#networking}
        :param control_plane: control_plane block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#control_plane EdgecontainerCluster#control_plane}
        :param control_plane_encryption: control_plane_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#control_plane_encryption EdgecontainerCluster#control_plane_encryption}
        :param default_max_pods_per_node: The default maximum number of pods per node used if a maximum value is not specified explicitly for a node pool in this cluster. If unspecified, the Kubernetes default value will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#default_max_pods_per_node EdgecontainerCluster#default_max_pods_per_node}
        :param external_load_balancer_ipv4_address_pools: Address pools for cluster data plane external load balancing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#external_load_balancer_ipv4_address_pools EdgecontainerCluster#external_load_balancer_ipv4_address_pools}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#id EdgecontainerCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for the edgecloud cluster. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#labels EdgecontainerCluster#labels}
        :param maintenance_policy: maintenance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#maintenance_policy EdgecontainerCluster#maintenance_policy}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#project EdgecontainerCluster#project}.
        :param release_channel: The release channel a cluster is subscribed to. Possible values: ["RELEASE_CHANNEL_UNSPECIFIED", "NONE", "REGULAR"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#release_channel EdgecontainerCluster#release_channel}
        :param system_addons_config: system_addons_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#system_addons_config EdgecontainerCluster#system_addons_config}
        :param target_version: The target cluster version. For example: "1.5.0". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#target_version EdgecontainerCluster#target_version}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#timeouts EdgecontainerCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__557451deba8d70d6cb5a87b46e0d33bcc69b3e35f1ba1bdb1559edc2759c3af9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EdgecontainerClusterConfig(
            authorization=authorization,
            fleet=fleet,
            location=location,
            name=name,
            networking=networking,
            control_plane=control_plane,
            control_plane_encryption=control_plane_encryption,
            default_max_pods_per_node=default_max_pods_per_node,
            external_load_balancer_ipv4_address_pools=external_load_balancer_ipv4_address_pools,
            id=id,
            labels=labels,
            maintenance_policy=maintenance_policy,
            project=project,
            release_channel=release_channel,
            system_addons_config=system_addons_config,
            target_version=target_version,
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
        '''Generates CDKTF code for importing a EdgecontainerCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EdgecontainerCluster to import.
        :param import_from_id: The id of the existing EdgecontainerCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EdgecontainerCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d69b07ee3f454caf1ff0f937619a16708ef57ce528e17e43ef5e579d03cc3d1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAuthorization")
    def put_authorization(
        self,
        *,
        admin_users: typing.Union["EdgecontainerClusterAuthorizationAdminUsers", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#admin_users EdgecontainerCluster#admin_users}
        '''
        value = EdgecontainerClusterAuthorization(admin_users=admin_users)

        return typing.cast(None, jsii.invoke(self, "putAuthorization", [value]))

    @jsii.member(jsii_name="putControlPlane")
    def put_control_plane(
        self,
        *,
        local: typing.Optional[typing.Union["EdgecontainerClusterControlPlaneLocal", typing.Dict[builtins.str, typing.Any]]] = None,
        remote: typing.Optional[typing.Union["EdgecontainerClusterControlPlaneRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param local: local block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#local EdgecontainerCluster#local}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#remote EdgecontainerCluster#remote}
        '''
        value = EdgecontainerClusterControlPlane(local=local, remote=remote)

        return typing.cast(None, jsii.invoke(self, "putControlPlane", [value]))

    @jsii.member(jsii_name="putControlPlaneEncryption")
    def put_control_plane_encryption(
        self,
        *,
        kms_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key: The Cloud KMS CryptoKey e.g. projects/{project}/locations/{location}/keyRings/{keyRing}/cryptoKeys/{cryptoKey} to use for protecting control plane disks. If not specified, a Google-managed key will be used instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#kms_key EdgecontainerCluster#kms_key}
        '''
        value = EdgecontainerClusterControlPlaneEncryption(kms_key=kms_key)

        return typing.cast(None, jsii.invoke(self, "putControlPlaneEncryption", [value]))

    @jsii.member(jsii_name="putFleet")
    def put_fleet(self, *, project: builtins.str) -> None:
        '''
        :param project: The name of the Fleet host project where this cluster will be registered. Project names are formatted as 'projects/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#project EdgecontainerCluster#project}
        '''
        value = EdgecontainerClusterFleet(project=project)

        return typing.cast(None, jsii.invoke(self, "putFleet", [value]))

    @jsii.member(jsii_name="putMaintenancePolicy")
    def put_maintenance_policy(
        self,
        *,
        window: typing.Union["EdgecontainerClusterMaintenancePolicyWindow", typing.Dict[builtins.str, typing.Any]],
        maintenance_exclusions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EdgecontainerClusterMaintenancePolicyMaintenanceExclusions", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param window: window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#window EdgecontainerCluster#window}
        :param maintenance_exclusions: maintenance_exclusions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#maintenance_exclusions EdgecontainerCluster#maintenance_exclusions}
        '''
        value = EdgecontainerClusterMaintenancePolicy(
            window=window, maintenance_exclusions=maintenance_exclusions
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenancePolicy", [value]))

    @jsii.member(jsii_name="putNetworking")
    def put_networking(
        self,
        *,
        cluster_ipv4_cidr_blocks: typing.Sequence[builtins.str],
        services_ipv4_cidr_blocks: typing.Sequence[builtins.str],
        cluster_ipv6_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        services_ipv6_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cluster_ipv4_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these blocks. Only a single block is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#cluster_ipv4_cidr_blocks EdgecontainerCluster#cluster_ipv4_cidr_blocks}
        :param services_ipv4_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these blocks. Only a single block is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#services_ipv4_cidr_blocks EdgecontainerCluster#services_ipv4_cidr_blocks}
        :param cluster_ipv6_cidr_blocks: If specified, dual stack mode is enabled and all pods in the cluster are assigned an IPv6 address from these blocks alongside from an IPv4 address. Only a single block is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#cluster_ipv6_cidr_blocks EdgecontainerCluster#cluster_ipv6_cidr_blocks}
        :param services_ipv6_cidr_blocks: If specified, dual stack mode is enabled and all services in the cluster are assigned an IPv6 address from these blocks alongside from an IPv4 address. Only a single block is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#services_ipv6_cidr_blocks EdgecontainerCluster#services_ipv6_cidr_blocks}
        '''
        value = EdgecontainerClusterNetworking(
            cluster_ipv4_cidr_blocks=cluster_ipv4_cidr_blocks,
            services_ipv4_cidr_blocks=services_ipv4_cidr_blocks,
            cluster_ipv6_cidr_blocks=cluster_ipv6_cidr_blocks,
            services_ipv6_cidr_blocks=services_ipv6_cidr_blocks,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworking", [value]))

    @jsii.member(jsii_name="putSystemAddonsConfig")
    def put_system_addons_config(
        self,
        *,
        ingress: typing.Optional[typing.Union["EdgecontainerClusterSystemAddonsConfigIngress", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ingress: ingress block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#ingress EdgecontainerCluster#ingress}
        '''
        value = EdgecontainerClusterSystemAddonsConfig(ingress=ingress)

        return typing.cast(None, jsii.invoke(self, "putSystemAddonsConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#create EdgecontainerCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#delete EdgecontainerCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#update EdgecontainerCluster#update}.
        '''
        value = EdgecontainerClusterTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetControlPlane")
    def reset_control_plane(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControlPlane", []))

    @jsii.member(jsii_name="resetControlPlaneEncryption")
    def reset_control_plane_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControlPlaneEncryption", []))

    @jsii.member(jsii_name="resetDefaultMaxPodsPerNode")
    def reset_default_max_pods_per_node(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultMaxPodsPerNode", []))

    @jsii.member(jsii_name="resetExternalLoadBalancerIpv4AddressPools")
    def reset_external_load_balancer_ipv4_address_pools(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalLoadBalancerIpv4AddressPools", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMaintenancePolicy")
    def reset_maintenance_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenancePolicy", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetReleaseChannel")
    def reset_release_channel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReleaseChannel", []))

    @jsii.member(jsii_name="resetSystemAddonsConfig")
    def reset_system_addons_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemAddonsConfig", []))

    @jsii.member(jsii_name="resetTargetVersion")
    def reset_target_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetVersion", []))

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
    @jsii.member(jsii_name="authorization")
    def authorization(self) -> "EdgecontainerClusterAuthorizationOutputReference":
        return typing.cast("EdgecontainerClusterAuthorizationOutputReference", jsii.get(self, "authorization"))

    @builtins.property
    @jsii.member(jsii_name="clusterCaCertificate")
    def cluster_ca_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterCaCertificate"))

    @builtins.property
    @jsii.member(jsii_name="controlPlane")
    def control_plane(self) -> "EdgecontainerClusterControlPlaneOutputReference":
        return typing.cast("EdgecontainerClusterControlPlaneOutputReference", jsii.get(self, "controlPlane"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneEncryption")
    def control_plane_encryption(
        self,
    ) -> "EdgecontainerClusterControlPlaneEncryptionOutputReference":
        return typing.cast("EdgecontainerClusterControlPlaneEncryptionOutputReference", jsii.get(self, "controlPlaneEncryption"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneVersion")
    def control_plane_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "controlPlaneVersion"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="fleet")
    def fleet(self) -> "EdgecontainerClusterFleetOutputReference":
        return typing.cast("EdgecontainerClusterFleetOutputReference", jsii.get(self, "fleet"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceEvents")
    def maintenance_events(self) -> "EdgecontainerClusterMaintenanceEventsList":
        return typing.cast("EdgecontainerClusterMaintenanceEventsList", jsii.get(self, "maintenanceEvents"))

    @builtins.property
    @jsii.member(jsii_name="maintenancePolicy")
    def maintenance_policy(
        self,
    ) -> "EdgecontainerClusterMaintenancePolicyOutputReference":
        return typing.cast("EdgecontainerClusterMaintenancePolicyOutputReference", jsii.get(self, "maintenancePolicy"))

    @builtins.property
    @jsii.member(jsii_name="networking")
    def networking(self) -> "EdgecontainerClusterNetworkingOutputReference":
        return typing.cast("EdgecontainerClusterNetworkingOutputReference", jsii.get(self, "networking"))

    @builtins.property
    @jsii.member(jsii_name="nodeVersion")
    def node_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeVersion"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="systemAddonsConfig")
    def system_addons_config(
        self,
    ) -> "EdgecontainerClusterSystemAddonsConfigOutputReference":
        return typing.cast("EdgecontainerClusterSystemAddonsConfigOutputReference", jsii.get(self, "systemAddonsConfig"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "EdgecontainerClusterTimeoutsOutputReference":
        return typing.cast("EdgecontainerClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="authorizationInput")
    def authorization_input(
        self,
    ) -> typing.Optional["EdgecontainerClusterAuthorization"]:
        return typing.cast(typing.Optional["EdgecontainerClusterAuthorization"], jsii.get(self, "authorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneEncryptionInput")
    def control_plane_encryption_input(
        self,
    ) -> typing.Optional["EdgecontainerClusterControlPlaneEncryption"]:
        return typing.cast(typing.Optional["EdgecontainerClusterControlPlaneEncryption"], jsii.get(self, "controlPlaneEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneInput")
    def control_plane_input(
        self,
    ) -> typing.Optional["EdgecontainerClusterControlPlane"]:
        return typing.cast(typing.Optional["EdgecontainerClusterControlPlane"], jsii.get(self, "controlPlaneInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultMaxPodsPerNodeInput")
    def default_max_pods_per_node_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultMaxPodsPerNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="externalLoadBalancerIpv4AddressPoolsInput")
    def external_load_balancer_ipv4_address_pools_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalLoadBalancerIpv4AddressPoolsInput"))

    @builtins.property
    @jsii.member(jsii_name="fleetInput")
    def fleet_input(self) -> typing.Optional["EdgecontainerClusterFleet"]:
        return typing.cast(typing.Optional["EdgecontainerClusterFleet"], jsii.get(self, "fleetInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenancePolicyInput")
    def maintenance_policy_input(
        self,
    ) -> typing.Optional["EdgecontainerClusterMaintenancePolicy"]:
        return typing.cast(typing.Optional["EdgecontainerClusterMaintenancePolicy"], jsii.get(self, "maintenancePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkingInput")
    def networking_input(self) -> typing.Optional["EdgecontainerClusterNetworking"]:
        return typing.cast(typing.Optional["EdgecontainerClusterNetworking"], jsii.get(self, "networkingInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="releaseChannelInput")
    def release_channel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "releaseChannelInput"))

    @builtins.property
    @jsii.member(jsii_name="systemAddonsConfigInput")
    def system_addons_config_input(
        self,
    ) -> typing.Optional["EdgecontainerClusterSystemAddonsConfig"]:
        return typing.cast(typing.Optional["EdgecontainerClusterSystemAddonsConfig"], jsii.get(self, "systemAddonsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="targetVersionInput")
    def target_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EdgecontainerClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EdgecontainerClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultMaxPodsPerNode")
    def default_max_pods_per_node(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultMaxPodsPerNode"))

    @default_max_pods_per_node.setter
    def default_max_pods_per_node(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4895560f89154d12416feffe0c2371af4409e8261643f40310e434780727aa85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultMaxPodsPerNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalLoadBalancerIpv4AddressPools")
    def external_load_balancer_ipv4_address_pools(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalLoadBalancerIpv4AddressPools"))

    @external_load_balancer_ipv4_address_pools.setter
    def external_load_balancer_ipv4_address_pools(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23634877988ff809b8a0846af6993a5b7a36e57d53f310c80e3a51f55869841b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalLoadBalancerIpv4AddressPools", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b293ff9366dad623005873a6d47eac98b364f8f8c27122ff34042d332a50abc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64ba874758e379d09c28d671623b1294ec624c78f0762aaaabd658e36377ef21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f177e337271597f3e534d866de2d5097cf3ea6ba3bd711ab41361521817f3f8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e46c53b205f12f3c05ab1f27e00b01ff1f24785b4a37a792b4bbe6f1e2551c8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0840c960528c1ec89dad93911840c858baf2aeb0bcaab9d03cf3f265307aefaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="releaseChannel")
    def release_channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "releaseChannel"))

    @release_channel.setter
    def release_channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccf3104fb174abeece9ab7835738ff252a62e29d6c472b052c06676271431dfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "releaseChannel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetVersion")
    def target_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetVersion"))

    @target_version.setter
    def target_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__420f4dc8299083fd6ce138bea1ca086ff76eea0a7b4b005dd2ed81bcccc1e465)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetVersion", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterAuthorization",
    jsii_struct_bases=[],
    name_mapping={"admin_users": "adminUsers"},
)
class EdgecontainerClusterAuthorization:
    def __init__(
        self,
        *,
        admin_users: typing.Union["EdgecontainerClusterAuthorizationAdminUsers", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#admin_users EdgecontainerCluster#admin_users}
        '''
        if isinstance(admin_users, dict):
            admin_users = EdgecontainerClusterAuthorizationAdminUsers(**admin_users)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbe51abb8ad23bab4a3e8b94ab4c7c8883b009cf5517ce9651f4994aba83cdcc)
            check_type(argname="argument admin_users", value=admin_users, expected_type=type_hints["admin_users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_users": admin_users,
        }

    @builtins.property
    def admin_users(self) -> "EdgecontainerClusterAuthorizationAdminUsers":
        '''admin_users block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#admin_users EdgecontainerCluster#admin_users}
        '''
        result = self._values.get("admin_users")
        assert result is not None, "Required property 'admin_users' is missing"
        return typing.cast("EdgecontainerClusterAuthorizationAdminUsers", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgecontainerClusterAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterAuthorizationAdminUsers",
    jsii_struct_bases=[],
    name_mapping={"username": "username"},
)
class EdgecontainerClusterAuthorizationAdminUsers:
    def __init__(self, *, username: builtins.str) -> None:
        '''
        :param username: An active Google username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#username EdgecontainerCluster#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94aeb0215a287f2745fd85983f86631f4073aeb8fdd89ce99a814ac7ca0509de)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
        }

    @builtins.property
    def username(self) -> builtins.str:
        '''An active Google username.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#username EdgecontainerCluster#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgecontainerClusterAuthorizationAdminUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EdgecontainerClusterAuthorizationAdminUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterAuthorizationAdminUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a6d95f3d66110da92b7f160b9cd58068ba02979b2525b3434fca6fccd0e7253)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__a25de055b6e2e50b1492f8224e58b1e9bce826fb3ffe718fae0bfe732d76589f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EdgecontainerClusterAuthorizationAdminUsers]:
        return typing.cast(typing.Optional[EdgecontainerClusterAuthorizationAdminUsers], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EdgecontainerClusterAuthorizationAdminUsers],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1851de96a2512adae32b8084fc7561fa65614760dd4d248d7973c75b70bce57f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EdgecontainerClusterAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e651d58c933fd965074392b0b3bbd89d4d47b35b9422f41c38350a3e4809ff37)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdminUsers")
    def put_admin_users(self, *, username: builtins.str) -> None:
        '''
        :param username: An active Google username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#username EdgecontainerCluster#username}
        '''
        value = EdgecontainerClusterAuthorizationAdminUsers(username=username)

        return typing.cast(None, jsii.invoke(self, "putAdminUsers", [value]))

    @builtins.property
    @jsii.member(jsii_name="adminUsers")
    def admin_users(self) -> EdgecontainerClusterAuthorizationAdminUsersOutputReference:
        return typing.cast(EdgecontainerClusterAuthorizationAdminUsersOutputReference, jsii.get(self, "adminUsers"))

    @builtins.property
    @jsii.member(jsii_name="adminUsersInput")
    def admin_users_input(
        self,
    ) -> typing.Optional[EdgecontainerClusterAuthorizationAdminUsers]:
        return typing.cast(typing.Optional[EdgecontainerClusterAuthorizationAdminUsers], jsii.get(self, "adminUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EdgecontainerClusterAuthorization]:
        return typing.cast(typing.Optional[EdgecontainerClusterAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EdgecontainerClusterAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2238b5c36a3f00e59c8f054df23b35fb35bef5e34cecb1c076d57a57960e2f6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "authorization": "authorization",
        "fleet": "fleet",
        "location": "location",
        "name": "name",
        "networking": "networking",
        "control_plane": "controlPlane",
        "control_plane_encryption": "controlPlaneEncryption",
        "default_max_pods_per_node": "defaultMaxPodsPerNode",
        "external_load_balancer_ipv4_address_pools": "externalLoadBalancerIpv4AddressPools",
        "id": "id",
        "labels": "labels",
        "maintenance_policy": "maintenancePolicy",
        "project": "project",
        "release_channel": "releaseChannel",
        "system_addons_config": "systemAddonsConfig",
        "target_version": "targetVersion",
        "timeouts": "timeouts",
    },
)
class EdgecontainerClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        authorization: typing.Union[EdgecontainerClusterAuthorization, typing.Dict[builtins.str, typing.Any]],
        fleet: typing.Union["EdgecontainerClusterFleet", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        networking: typing.Union["EdgecontainerClusterNetworking", typing.Dict[builtins.str, typing.Any]],
        control_plane: typing.Optional[typing.Union["EdgecontainerClusterControlPlane", typing.Dict[builtins.str, typing.Any]]] = None,
        control_plane_encryption: typing.Optional[typing.Union["EdgecontainerClusterControlPlaneEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
        default_max_pods_per_node: typing.Optional[jsii.Number] = None,
        external_load_balancer_ipv4_address_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        maintenance_policy: typing.Optional[typing.Union["EdgecontainerClusterMaintenancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        release_channel: typing.Optional[builtins.str] = None,
        system_addons_config: typing.Optional[typing.Union["EdgecontainerClusterSystemAddonsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        target_version: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["EdgecontainerClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#authorization EdgecontainerCluster#authorization}
        :param fleet: fleet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#fleet EdgecontainerCluster#fleet}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#location EdgecontainerCluster#location}
        :param name: The GDCE cluster name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#name EdgecontainerCluster#name}
        :param networking: networking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#networking EdgecontainerCluster#networking}
        :param control_plane: control_plane block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#control_plane EdgecontainerCluster#control_plane}
        :param control_plane_encryption: control_plane_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#control_plane_encryption EdgecontainerCluster#control_plane_encryption}
        :param default_max_pods_per_node: The default maximum number of pods per node used if a maximum value is not specified explicitly for a node pool in this cluster. If unspecified, the Kubernetes default value will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#default_max_pods_per_node EdgecontainerCluster#default_max_pods_per_node}
        :param external_load_balancer_ipv4_address_pools: Address pools for cluster data plane external load balancing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#external_load_balancer_ipv4_address_pools EdgecontainerCluster#external_load_balancer_ipv4_address_pools}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#id EdgecontainerCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for the edgecloud cluster. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#labels EdgecontainerCluster#labels}
        :param maintenance_policy: maintenance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#maintenance_policy EdgecontainerCluster#maintenance_policy}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#project EdgecontainerCluster#project}.
        :param release_channel: The release channel a cluster is subscribed to. Possible values: ["RELEASE_CHANNEL_UNSPECIFIED", "NONE", "REGULAR"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#release_channel EdgecontainerCluster#release_channel}
        :param system_addons_config: system_addons_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#system_addons_config EdgecontainerCluster#system_addons_config}
        :param target_version: The target cluster version. For example: "1.5.0". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#target_version EdgecontainerCluster#target_version}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#timeouts EdgecontainerCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(authorization, dict):
            authorization = EdgecontainerClusterAuthorization(**authorization)
        if isinstance(fleet, dict):
            fleet = EdgecontainerClusterFleet(**fleet)
        if isinstance(networking, dict):
            networking = EdgecontainerClusterNetworking(**networking)
        if isinstance(control_plane, dict):
            control_plane = EdgecontainerClusterControlPlane(**control_plane)
        if isinstance(control_plane_encryption, dict):
            control_plane_encryption = EdgecontainerClusterControlPlaneEncryption(**control_plane_encryption)
        if isinstance(maintenance_policy, dict):
            maintenance_policy = EdgecontainerClusterMaintenancePolicy(**maintenance_policy)
        if isinstance(system_addons_config, dict):
            system_addons_config = EdgecontainerClusterSystemAddonsConfig(**system_addons_config)
        if isinstance(timeouts, dict):
            timeouts = EdgecontainerClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6af49bc985f95ec5dda81d63e19dd55d432d04887be212aed5edd30afc0f524c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument authorization", value=authorization, expected_type=type_hints["authorization"])
            check_type(argname="argument fleet", value=fleet, expected_type=type_hints["fleet"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument networking", value=networking, expected_type=type_hints["networking"])
            check_type(argname="argument control_plane", value=control_plane, expected_type=type_hints["control_plane"])
            check_type(argname="argument control_plane_encryption", value=control_plane_encryption, expected_type=type_hints["control_plane_encryption"])
            check_type(argname="argument default_max_pods_per_node", value=default_max_pods_per_node, expected_type=type_hints["default_max_pods_per_node"])
            check_type(argname="argument external_load_balancer_ipv4_address_pools", value=external_load_balancer_ipv4_address_pools, expected_type=type_hints["external_load_balancer_ipv4_address_pools"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument maintenance_policy", value=maintenance_policy, expected_type=type_hints["maintenance_policy"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument release_channel", value=release_channel, expected_type=type_hints["release_channel"])
            check_type(argname="argument system_addons_config", value=system_addons_config, expected_type=type_hints["system_addons_config"])
            check_type(argname="argument target_version", value=target_version, expected_type=type_hints["target_version"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorization": authorization,
            "fleet": fleet,
            "location": location,
            "name": name,
            "networking": networking,
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
        if control_plane is not None:
            self._values["control_plane"] = control_plane
        if control_plane_encryption is not None:
            self._values["control_plane_encryption"] = control_plane_encryption
        if default_max_pods_per_node is not None:
            self._values["default_max_pods_per_node"] = default_max_pods_per_node
        if external_load_balancer_ipv4_address_pools is not None:
            self._values["external_load_balancer_ipv4_address_pools"] = external_load_balancer_ipv4_address_pools
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if maintenance_policy is not None:
            self._values["maintenance_policy"] = maintenance_policy
        if project is not None:
            self._values["project"] = project
        if release_channel is not None:
            self._values["release_channel"] = release_channel
        if system_addons_config is not None:
            self._values["system_addons_config"] = system_addons_config
        if target_version is not None:
            self._values["target_version"] = target_version
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
    def authorization(self) -> EdgecontainerClusterAuthorization:
        '''authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#authorization EdgecontainerCluster#authorization}
        '''
        result = self._values.get("authorization")
        assert result is not None, "Required property 'authorization' is missing"
        return typing.cast(EdgecontainerClusterAuthorization, result)

    @builtins.property
    def fleet(self) -> "EdgecontainerClusterFleet":
        '''fleet block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#fleet EdgecontainerCluster#fleet}
        '''
        result = self._values.get("fleet")
        assert result is not None, "Required property 'fleet' is missing"
        return typing.cast("EdgecontainerClusterFleet", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#location EdgecontainerCluster#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The GDCE cluster name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#name EdgecontainerCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def networking(self) -> "EdgecontainerClusterNetworking":
        '''networking block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#networking EdgecontainerCluster#networking}
        '''
        result = self._values.get("networking")
        assert result is not None, "Required property 'networking' is missing"
        return typing.cast("EdgecontainerClusterNetworking", result)

    @builtins.property
    def control_plane(self) -> typing.Optional["EdgecontainerClusterControlPlane"]:
        '''control_plane block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#control_plane EdgecontainerCluster#control_plane}
        '''
        result = self._values.get("control_plane")
        return typing.cast(typing.Optional["EdgecontainerClusterControlPlane"], result)

    @builtins.property
    def control_plane_encryption(
        self,
    ) -> typing.Optional["EdgecontainerClusterControlPlaneEncryption"]:
        '''control_plane_encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#control_plane_encryption EdgecontainerCluster#control_plane_encryption}
        '''
        result = self._values.get("control_plane_encryption")
        return typing.cast(typing.Optional["EdgecontainerClusterControlPlaneEncryption"], result)

    @builtins.property
    def default_max_pods_per_node(self) -> typing.Optional[jsii.Number]:
        '''The default maximum number of pods per node used if a maximum value is not specified explicitly for a node pool in this cluster.

        If unspecified, the
        Kubernetes default value will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#default_max_pods_per_node EdgecontainerCluster#default_max_pods_per_node}
        '''
        result = self._values.get("default_max_pods_per_node")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def external_load_balancer_ipv4_address_pools(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Address pools for cluster data plane external load balancing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#external_load_balancer_ipv4_address_pools EdgecontainerCluster#external_load_balancer_ipv4_address_pools}
        '''
        result = self._values.get("external_load_balancer_ipv4_address_pools")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#id EdgecontainerCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-defined labels for the edgecloud cluster.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#labels EdgecontainerCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def maintenance_policy(
        self,
    ) -> typing.Optional["EdgecontainerClusterMaintenancePolicy"]:
        '''maintenance_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#maintenance_policy EdgecontainerCluster#maintenance_policy}
        '''
        result = self._values.get("maintenance_policy")
        return typing.cast(typing.Optional["EdgecontainerClusterMaintenancePolicy"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#project EdgecontainerCluster#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_channel(self) -> typing.Optional[builtins.str]:
        '''The release channel a cluster is subscribed to. Possible values: ["RELEASE_CHANNEL_UNSPECIFIED", "NONE", "REGULAR"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#release_channel EdgecontainerCluster#release_channel}
        '''
        result = self._values.get("release_channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def system_addons_config(
        self,
    ) -> typing.Optional["EdgecontainerClusterSystemAddonsConfig"]:
        '''system_addons_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#system_addons_config EdgecontainerCluster#system_addons_config}
        '''
        result = self._values.get("system_addons_config")
        return typing.cast(typing.Optional["EdgecontainerClusterSystemAddonsConfig"], result)

    @builtins.property
    def target_version(self) -> typing.Optional[builtins.str]:
        '''The target cluster version. For example: "1.5.0".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#target_version EdgecontainerCluster#target_version}
        '''
        result = self._values.get("target_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["EdgecontainerClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#timeouts EdgecontainerCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["EdgecontainerClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgecontainerClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterControlPlane",
    jsii_struct_bases=[],
    name_mapping={"local": "local", "remote": "remote"},
)
class EdgecontainerClusterControlPlane:
    def __init__(
        self,
        *,
        local: typing.Optional[typing.Union["EdgecontainerClusterControlPlaneLocal", typing.Dict[builtins.str, typing.Any]]] = None,
        remote: typing.Optional[typing.Union["EdgecontainerClusterControlPlaneRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param local: local block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#local EdgecontainerCluster#local}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#remote EdgecontainerCluster#remote}
        '''
        if isinstance(local, dict):
            local = EdgecontainerClusterControlPlaneLocal(**local)
        if isinstance(remote, dict):
            remote = EdgecontainerClusterControlPlaneRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9daca5c3029019cd555e01be7d94ee9f3f2086fbf8293800e8a0bd2eea7409f4)
            check_type(argname="argument local", value=local, expected_type=type_hints["local"])
            check_type(argname="argument remote", value=remote, expected_type=type_hints["remote"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if local is not None:
            self._values["local"] = local
        if remote is not None:
            self._values["remote"] = remote

    @builtins.property
    def local(self) -> typing.Optional["EdgecontainerClusterControlPlaneLocal"]:
        '''local block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#local EdgecontainerCluster#local}
        '''
        result = self._values.get("local")
        return typing.cast(typing.Optional["EdgecontainerClusterControlPlaneLocal"], result)

    @builtins.property
    def remote(self) -> typing.Optional["EdgecontainerClusterControlPlaneRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#remote EdgecontainerCluster#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["EdgecontainerClusterControlPlaneRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgecontainerClusterControlPlane(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterControlPlaneEncryption",
    jsii_struct_bases=[],
    name_mapping={"kms_key": "kmsKey"},
)
class EdgecontainerClusterControlPlaneEncryption:
    def __init__(self, *, kms_key: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key: The Cloud KMS CryptoKey e.g. projects/{project}/locations/{location}/keyRings/{keyRing}/cryptoKeys/{cryptoKey} to use for protecting control plane disks. If not specified, a Google-managed key will be used instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#kms_key EdgecontainerCluster#kms_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6ab462416f75f716cd454346aa83defc98f7f2db6c68600d1c3a728fe108572)
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The Cloud KMS CryptoKey e.g. projects/{project}/locations/{location}/keyRings/{keyRing}/cryptoKeys/{cryptoKey} to use for protecting control plane disks. If not specified, a Google-managed key will be used instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#kms_key EdgecontainerCluster#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgecontainerClusterControlPlaneEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterControlPlaneEncryptionKmsStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class EdgecontainerClusterControlPlaneEncryptionKmsStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgecontainerClusterControlPlaneEncryptionKmsStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EdgecontainerClusterControlPlaneEncryptionKmsStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterControlPlaneEncryptionKmsStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54740dcccae7fefd4b8b5bee1a3fd3a89ca296a2249a2277e626d10f0045884a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EdgecontainerClusterControlPlaneEncryptionKmsStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d513bdcc2d48e674324ad0b0a26b5f903860901edf1c51741980096603bdb23)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EdgecontainerClusterControlPlaneEncryptionKmsStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99eef90cd60ede8b2abced5cd7bb11886aeb29949024c0dd7a7b150a7c67fd6d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbd3e87a31715b9f304627823c27490659bf417b859f6ea15ae863d872bb0e9a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__adca4e845ee2272da1bbfce5a138d7f99b1d761f9f6eafe9ea9dd5dc3673fcdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class EdgecontainerClusterControlPlaneEncryptionKmsStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterControlPlaneEncryptionKmsStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcb0547a36b790efa1adc718dc98b74a022b457d459c3d694afa27446a4cb30b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "code"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EdgecontainerClusterControlPlaneEncryptionKmsStatus]:
        return typing.cast(typing.Optional[EdgecontainerClusterControlPlaneEncryptionKmsStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EdgecontainerClusterControlPlaneEncryptionKmsStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ffcabd44aa1965ce1a94cc2299faf6d7ed4a530f5ef3c4a98f98bfa8a968e63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EdgecontainerClusterControlPlaneEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterControlPlaneEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b27b329584930d4abd058be58acd352d444e0a79c407b74a364aff9c60f9a36b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyActiveVersion")
    def kms_key_active_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyActiveVersion"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyState")
    def kms_key_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyState"))

    @builtins.property
    @jsii.member(jsii_name="kmsStatus")
    def kms_status(self) -> EdgecontainerClusterControlPlaneEncryptionKmsStatusList:
        return typing.cast(EdgecontainerClusterControlPlaneEncryptionKmsStatusList, jsii.get(self, "kmsStatus"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60ff65ab6e7176a76a5193c8af2b9269301959bd3425884c94c99a4fd9d4827e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EdgecontainerClusterControlPlaneEncryption]:
        return typing.cast(typing.Optional[EdgecontainerClusterControlPlaneEncryption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EdgecontainerClusterControlPlaneEncryption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2be8044629002e09938eccc364b21a948ff0783d4cf421cc2b297c28784908e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterControlPlaneLocal",
    jsii_struct_bases=[],
    name_mapping={
        "machine_filter": "machineFilter",
        "node_count": "nodeCount",
        "node_location": "nodeLocation",
        "shared_deployment_policy": "sharedDeploymentPolicy",
    },
)
class EdgecontainerClusterControlPlaneLocal:
    def __init__(
        self,
        *,
        machine_filter: typing.Optional[builtins.str] = None,
        node_count: typing.Optional[jsii.Number] = None,
        node_location: typing.Optional[builtins.str] = None,
        shared_deployment_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param machine_filter: Only machines matching this filter will be allowed to host control plane nodes. The filtering language accepts strings like "name=", and is documented here: `AIP-160 <https://google.aip.dev/160>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#machine_filter EdgecontainerCluster#machine_filter}
        :param node_count: The number of nodes to serve as replicas of the Control Plane. Only 1 and 3 are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#node_count EdgecontainerCluster#node_count}
        :param node_location: Name of the Google Distributed Cloud Edge zones where this node pool will be created. For example: 'us-central1-edge-customer-a'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#node_location EdgecontainerCluster#node_location}
        :param shared_deployment_policy: Policy configuration about how user applications are deployed. Possible values: ["SHARED_DEPLOYMENT_POLICY_UNSPECIFIED", "ALLOWED", "DISALLOWED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#shared_deployment_policy EdgecontainerCluster#shared_deployment_policy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ed66a878a51a19d10bfe4852ee65f6cc3e2dd670ee9b962f931bd0f1ddefac1)
            check_type(argname="argument machine_filter", value=machine_filter, expected_type=type_hints["machine_filter"])
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
            check_type(argname="argument node_location", value=node_location, expected_type=type_hints["node_location"])
            check_type(argname="argument shared_deployment_policy", value=shared_deployment_policy, expected_type=type_hints["shared_deployment_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if machine_filter is not None:
            self._values["machine_filter"] = machine_filter
        if node_count is not None:
            self._values["node_count"] = node_count
        if node_location is not None:
            self._values["node_location"] = node_location
        if shared_deployment_policy is not None:
            self._values["shared_deployment_policy"] = shared_deployment_policy

    @builtins.property
    def machine_filter(self) -> typing.Optional[builtins.str]:
        '''Only machines matching this filter will be allowed to host control plane nodes.

        The filtering language accepts strings like "name=",
        and is documented here: `AIP-160 <https://google.aip.dev/160>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#machine_filter EdgecontainerCluster#machine_filter}
        '''
        result = self._values.get("machine_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_count(self) -> typing.Optional[jsii.Number]:
        '''The number of nodes to serve as replicas of the Control Plane. Only 1 and 3 are supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#node_count EdgecontainerCluster#node_count}
        '''
        result = self._values.get("node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def node_location(self) -> typing.Optional[builtins.str]:
        '''Name of the Google Distributed Cloud Edge zones where this node pool will be created. For example: 'us-central1-edge-customer-a'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#node_location EdgecontainerCluster#node_location}
        '''
        result = self._values.get("node_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shared_deployment_policy(self) -> typing.Optional[builtins.str]:
        '''Policy configuration about how user applications are deployed. Possible values: ["SHARED_DEPLOYMENT_POLICY_UNSPECIFIED", "ALLOWED", "DISALLOWED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#shared_deployment_policy EdgecontainerCluster#shared_deployment_policy}
        '''
        result = self._values.get("shared_deployment_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgecontainerClusterControlPlaneLocal(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EdgecontainerClusterControlPlaneLocalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterControlPlaneLocalOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bc6eaa0510cbe42441c0dc1552af020f7ceff7a7d28f82f3cb330d1c6f00bdb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMachineFilter")
    def reset_machine_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineFilter", []))

    @jsii.member(jsii_name="resetNodeCount")
    def reset_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeCount", []))

    @jsii.member(jsii_name="resetNodeLocation")
    def reset_node_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeLocation", []))

    @jsii.member(jsii_name="resetSharedDeploymentPolicy")
    def reset_shared_deployment_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedDeploymentPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="machineFilterInput")
    def machine_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeCountInput")
    def node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeLocationInput")
    def node_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedDeploymentPolicyInput")
    def shared_deployment_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sharedDeploymentPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="machineFilter")
    def machine_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineFilter"))

    @machine_filter.setter
    def machine_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b75d78e18d47c3e0ad01fddc16b964548062c69110f9dc5375da41891fc3a197)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b4717c68f42c5c6aaca15ab06638917afd7c7cba66b3bedbe47e8d1097394d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeLocation")
    def node_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeLocation"))

    @node_location.setter
    def node_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13e5e43d20ace03f17a741edc3f9d6ecabeb2214fb33643a851d783ecc6ffc02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sharedDeploymentPolicy")
    def shared_deployment_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sharedDeploymentPolicy"))

    @shared_deployment_policy.setter
    def shared_deployment_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd1b04ef4c6a9f6c25d09238897edb9986d264234395f6da300b6c47e8f8d412)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedDeploymentPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EdgecontainerClusterControlPlaneLocal]:
        return typing.cast(typing.Optional[EdgecontainerClusterControlPlaneLocal], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EdgecontainerClusterControlPlaneLocal],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a0443fc2f82cb1f27a84934200514823c470f34cf9d9a22a7b69976a0f8d665)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EdgecontainerClusterControlPlaneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterControlPlaneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1290f0083b7ecb2ebf0758dd376c8a6ba65eb10129280c6b0b6dae4750043df4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLocal")
    def put_local(
        self,
        *,
        machine_filter: typing.Optional[builtins.str] = None,
        node_count: typing.Optional[jsii.Number] = None,
        node_location: typing.Optional[builtins.str] = None,
        shared_deployment_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param machine_filter: Only machines matching this filter will be allowed to host control plane nodes. The filtering language accepts strings like "name=", and is documented here: `AIP-160 <https://google.aip.dev/160>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#machine_filter EdgecontainerCluster#machine_filter}
        :param node_count: The number of nodes to serve as replicas of the Control Plane. Only 1 and 3 are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#node_count EdgecontainerCluster#node_count}
        :param node_location: Name of the Google Distributed Cloud Edge zones where this node pool will be created. For example: 'us-central1-edge-customer-a'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#node_location EdgecontainerCluster#node_location}
        :param shared_deployment_policy: Policy configuration about how user applications are deployed. Possible values: ["SHARED_DEPLOYMENT_POLICY_UNSPECIFIED", "ALLOWED", "DISALLOWED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#shared_deployment_policy EdgecontainerCluster#shared_deployment_policy}
        '''
        value = EdgecontainerClusterControlPlaneLocal(
            machine_filter=machine_filter,
            node_count=node_count,
            node_location=node_location,
            shared_deployment_policy=shared_deployment_policy,
        )

        return typing.cast(None, jsii.invoke(self, "putLocal", [value]))

    @jsii.member(jsii_name="putRemote")
    def put_remote(
        self,
        *,
        node_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param node_location: Name of the Google Distributed Cloud Edge zones where this node pool will be created. For example: 'us-central1-edge-customer-a'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#node_location EdgecontainerCluster#node_location}
        '''
        value = EdgecontainerClusterControlPlaneRemote(node_location=node_location)

        return typing.cast(None, jsii.invoke(self, "putRemote", [value]))

    @jsii.member(jsii_name="resetLocal")
    def reset_local(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocal", []))

    @jsii.member(jsii_name="resetRemote")
    def reset_remote(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemote", []))

    @builtins.property
    @jsii.member(jsii_name="local")
    def local(self) -> EdgecontainerClusterControlPlaneLocalOutputReference:
        return typing.cast(EdgecontainerClusterControlPlaneLocalOutputReference, jsii.get(self, "local"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(self) -> "EdgecontainerClusterControlPlaneRemoteOutputReference":
        return typing.cast("EdgecontainerClusterControlPlaneRemoteOutputReference", jsii.get(self, "remote"))

    @builtins.property
    @jsii.member(jsii_name="localInput")
    def local_input(self) -> typing.Optional[EdgecontainerClusterControlPlaneLocal]:
        return typing.cast(typing.Optional[EdgecontainerClusterControlPlaneLocal], jsii.get(self, "localInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(self) -> typing.Optional["EdgecontainerClusterControlPlaneRemote"]:
        return typing.cast(typing.Optional["EdgecontainerClusterControlPlaneRemote"], jsii.get(self, "remoteInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EdgecontainerClusterControlPlane]:
        return typing.cast(typing.Optional[EdgecontainerClusterControlPlane], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EdgecontainerClusterControlPlane],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd426ed4c01291c3efa3b05e2bc59bfa74d094f34b1332806117f14830b1560f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterControlPlaneRemote",
    jsii_struct_bases=[],
    name_mapping={"node_location": "nodeLocation"},
)
class EdgecontainerClusterControlPlaneRemote:
    def __init__(self, *, node_location: typing.Optional[builtins.str] = None) -> None:
        '''
        :param node_location: Name of the Google Distributed Cloud Edge zones where this node pool will be created. For example: 'us-central1-edge-customer-a'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#node_location EdgecontainerCluster#node_location}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3a8f51c9d3496c55cf83e1234983c1f75f546b786c765d9e712c471056a81a8)
            check_type(argname="argument node_location", value=node_location, expected_type=type_hints["node_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if node_location is not None:
            self._values["node_location"] = node_location

    @builtins.property
    def node_location(self) -> typing.Optional[builtins.str]:
        '''Name of the Google Distributed Cloud Edge zones where this node pool will be created. For example: 'us-central1-edge-customer-a'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#node_location EdgecontainerCluster#node_location}
        '''
        result = self._values.get("node_location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgecontainerClusterControlPlaneRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EdgecontainerClusterControlPlaneRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterControlPlaneRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae45e41410a481da630d0c662aea00d9d9b4de51f9d23369ca0d03717c15bca9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNodeLocation")
    def reset_node_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeLocation", []))

    @builtins.property
    @jsii.member(jsii_name="nodeLocationInput")
    def node_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeLocation")
    def node_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeLocation"))

    @node_location.setter
    def node_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0545cb7326474830c49f48133fd5da4b7d814a21fa196eb757af60e29614370)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EdgecontainerClusterControlPlaneRemote]:
        return typing.cast(typing.Optional[EdgecontainerClusterControlPlaneRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EdgecontainerClusterControlPlaneRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d24a621bf601441f280117ebf178348faf73cbf9daf6d742ae6f462fc0b4a758)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterFleet",
    jsii_struct_bases=[],
    name_mapping={"project": "project"},
)
class EdgecontainerClusterFleet:
    def __init__(self, *, project: builtins.str) -> None:
        '''
        :param project: The name of the Fleet host project where this cluster will be registered. Project names are formatted as 'projects/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#project EdgecontainerCluster#project}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f342ef9c43f860c3a0c7d66ebfefaf6ad48b90d02d7a0af4c2355ccfb363925b)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project": project,
        }

    @builtins.property
    def project(self) -> builtins.str:
        '''The name of the Fleet host project where this cluster will be registered. Project names are formatted as 'projects/'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#project EdgecontainerCluster#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgecontainerClusterFleet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EdgecontainerClusterFleetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterFleetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c72a71b615db1ad9676c51c1d2946c0c222e55ae42d566cf9fe87c8999f5d83a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="membership")
    def membership(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "membership"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ced0583bb60720da0b51c50745106551b0c593cbd6ad5e7d1dbd5c18296ebafb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EdgecontainerClusterFleet]:
        return typing.cast(typing.Optional[EdgecontainerClusterFleet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EdgecontainerClusterFleet]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bab4f220f44f4ed405fbd2c958692a6c7557e7869cdcc5f35c0cbe835b454ce6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterMaintenanceEvents",
    jsii_struct_bases=[],
    name_mapping={},
)
class EdgecontainerClusterMaintenanceEvents:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgecontainerClusterMaintenanceEvents(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EdgecontainerClusterMaintenanceEventsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterMaintenanceEventsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d6067c857007ee07215205685e932934c4d1993c77f7b493f018999e0038528)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EdgecontainerClusterMaintenanceEventsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7110e5d96007bd2a6ad5370ea284c1aa6fe6a351be1d91acf97ad0be2dd049f5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EdgecontainerClusterMaintenanceEventsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bc265395b50cea56d968ca62ed942a71393fc2542ea5afb4bc0e1b0c3e7b930)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70fe307c8989a17e093d48198fe8e47da4f00d50b57c26318786062e86366fd3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2edf8693bcf17b5eb576df1454a271bf46b888345a87c3d2d7d08fe2c7f0222)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class EdgecontainerClusterMaintenanceEventsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterMaintenanceEventsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca2c06acff7e2f5e77e02eb20f98a7cd92477540349ba01df9474328ac143245)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @builtins.property
    @jsii.member(jsii_name="operation")
    def operation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operation"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="targetVersion")
    def target_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetVersion"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uuid"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EdgecontainerClusterMaintenanceEvents]:
        return typing.cast(typing.Optional[EdgecontainerClusterMaintenanceEvents], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EdgecontainerClusterMaintenanceEvents],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73cb311441089e21776388942903c26f8cdb52481ce550d5e8a5ffda6a4a0964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterMaintenancePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "window": "window",
        "maintenance_exclusions": "maintenanceExclusions",
    },
)
class EdgecontainerClusterMaintenancePolicy:
    def __init__(
        self,
        *,
        window: typing.Union["EdgecontainerClusterMaintenancePolicyWindow", typing.Dict[builtins.str, typing.Any]],
        maintenance_exclusions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EdgecontainerClusterMaintenancePolicyMaintenanceExclusions", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param window: window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#window EdgecontainerCluster#window}
        :param maintenance_exclusions: maintenance_exclusions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#maintenance_exclusions EdgecontainerCluster#maintenance_exclusions}
        '''
        if isinstance(window, dict):
            window = EdgecontainerClusterMaintenancePolicyWindow(**window)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99524251cc7f976e2b79d58fa662e99cb1c9b71def8bbf00617be1a69d45cfe1)
            check_type(argname="argument window", value=window, expected_type=type_hints["window"])
            check_type(argname="argument maintenance_exclusions", value=maintenance_exclusions, expected_type=type_hints["maintenance_exclusions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "window": window,
        }
        if maintenance_exclusions is not None:
            self._values["maintenance_exclusions"] = maintenance_exclusions

    @builtins.property
    def window(self) -> "EdgecontainerClusterMaintenancePolicyWindow":
        '''window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#window EdgecontainerCluster#window}
        '''
        result = self._values.get("window")
        assert result is not None, "Required property 'window' is missing"
        return typing.cast("EdgecontainerClusterMaintenancePolicyWindow", result)

    @builtins.property
    def maintenance_exclusions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EdgecontainerClusterMaintenancePolicyMaintenanceExclusions"]]]:
        '''maintenance_exclusions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#maintenance_exclusions EdgecontainerCluster#maintenance_exclusions}
        '''
        result = self._values.get("maintenance_exclusions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EdgecontainerClusterMaintenancePolicyMaintenanceExclusions"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgecontainerClusterMaintenancePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterMaintenancePolicyMaintenanceExclusions",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "window": "window"},
)
class EdgecontainerClusterMaintenancePolicyMaintenanceExclusions:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        window: typing.Optional[typing.Union["EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: A unique (per cluster) id for the window. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#id EdgecontainerCluster#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param window: window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#window EdgecontainerCluster#window}
        '''
        if isinstance(window, dict):
            window = EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow(**window)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78f00c493f4d4d0ef52d9563e541d44b170acf3275b0fc7145f730ab4d0562d7)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument window", value=window, expected_type=type_hints["window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id
        if window is not None:
            self._values["window"] = window

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''A unique (per cluster) id for the window.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#id EdgecontainerCluster#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def window(
        self,
    ) -> typing.Optional["EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow"]:
        '''window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#window EdgecontainerCluster#window}
        '''
        result = self._values.get("window")
        return typing.cast(typing.Optional["EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgecontainerClusterMaintenancePolicyMaintenanceExclusions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aecdc2f5a0d8bd56165d35026c1dc00b823206db7b98d2b893ecadc8569eb53e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fb9a7b0433d8fb2d2ceda9a53d7f4b8752abf8db628c66deca50f1ef425e2e0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65cf147b30bbeb4dbdaac9549c9f82677205cd30283f934b0c63f2605ba5eff8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d6a4e8100b54b0129c69ed3966baa6e70ea428fc431240721a2bb93370f8142)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43551a2a2a445db675df1e0ed7f8973516466e70fa6c7d11622b251ee06dd686)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgecontainerClusterMaintenancePolicyMaintenanceExclusions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgecontainerClusterMaintenancePolicyMaintenanceExclusions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgecontainerClusterMaintenancePolicyMaintenanceExclusions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afd785f37b294b5c25850a0e1865da2d62d47d285f630cdc5a6b4a21f02434ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__667e7950ade5520d23ce9a34f55a909175f0993cc7b14d92846e4ab298cfe489)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putWindow")
    def put_window(
        self,
        *,
        end_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param end_time: The time that the window ends. The end time must take place after the start time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#end_time EdgecontainerCluster#end_time}
        :param start_time: The time that the window first starts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#start_time EdgecontainerCluster#start_time}
        '''
        value = EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow(
            end_time=end_time, start_time=start_time
        )

        return typing.cast(None, jsii.invoke(self, "putWindow", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetWindow")
    def reset_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindow", []))

    @builtins.property
    @jsii.member(jsii_name="window")
    def window(
        self,
    ) -> "EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindowOutputReference":
        return typing.cast("EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindowOutputReference", jsii.get(self, "window"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="windowInput")
    def window_input(
        self,
    ) -> typing.Optional["EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow"]:
        return typing.cast(typing.Optional["EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow"], jsii.get(self, "windowInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e038a4db2f743c25fa1df2837e1b1e42a97e7d91f9f92e57cd5009d3e50c1c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgecontainerClusterMaintenancePolicyMaintenanceExclusions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgecontainerClusterMaintenancePolicyMaintenanceExclusions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgecontainerClusterMaintenancePolicyMaintenanceExclusions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__589effc6bc4ba1ca256c02d91c3871b16ba05ff4ebc53952ef362a66fd1756b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow",
    jsii_struct_bases=[],
    name_mapping={"end_time": "endTime", "start_time": "startTime"},
)
class EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow:
    def __init__(
        self,
        *,
        end_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param end_time: The time that the window ends. The end time must take place after the start time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#end_time EdgecontainerCluster#end_time}
        :param start_time: The time that the window first starts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#start_time EdgecontainerCluster#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cc4d699d4431df5c26af7f4102618d366c5c8d08bbe3120a0559748f1534c3e)
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if end_time is not None:
            self._values["end_time"] = end_time
        if start_time is not None:
            self._values["start_time"] = start_time

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''The time that the window ends. The end time must take place after the start time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#end_time EdgecontainerCluster#end_time}
        '''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''The time that the window first starts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#start_time EdgecontainerCluster#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f12365d26c288d662af3c4f5e83132bdba8ab8c6a594efb205fbfc52ef1d5cd0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEndTime")
    def reset_end_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndTime", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72884e76a3b44a02506975f3b810ab1d8e8dce023c0922ad0b530766b7ae7f9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aba132eff208aa7be232a6eb6ab431e5773470ff4331bcd1019c24ca4a880fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow]:
        return typing.cast(typing.Optional[EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2c680d1aeadea4051abf92c7596a09ba0bc7b6268631e69940d96effb82e9f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EdgecontainerClusterMaintenancePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterMaintenancePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34ed0969401cc9269dc364621d895eb33d63fd849f985b361ce9cf648dcd9d1c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMaintenanceExclusions")
    def put_maintenance_exclusions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EdgecontainerClusterMaintenancePolicyMaintenanceExclusions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f63f90fd221dece72046e07078f7488b69edaf9fcfbfdc2ee44ca8bb4e90cfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMaintenanceExclusions", [value]))

    @jsii.member(jsii_name="putWindow")
    def put_window(
        self,
        *,
        recurring_window: typing.Union["EdgecontainerClusterMaintenancePolicyWindowRecurringWindow", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param recurring_window: recurring_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#recurring_window EdgecontainerCluster#recurring_window}
        '''
        value = EdgecontainerClusterMaintenancePolicyWindow(
            recurring_window=recurring_window
        )

        return typing.cast(None, jsii.invoke(self, "putWindow", [value]))

    @jsii.member(jsii_name="resetMaintenanceExclusions")
    def reset_maintenance_exclusions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceExclusions", []))

    @builtins.property
    @jsii.member(jsii_name="maintenanceExclusions")
    def maintenance_exclusions(
        self,
    ) -> EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsList:
        return typing.cast(EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsList, jsii.get(self, "maintenanceExclusions"))

    @builtins.property
    @jsii.member(jsii_name="window")
    def window(self) -> "EdgecontainerClusterMaintenancePolicyWindowOutputReference":
        return typing.cast("EdgecontainerClusterMaintenancePolicyWindowOutputReference", jsii.get(self, "window"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceExclusionsInput")
    def maintenance_exclusions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgecontainerClusterMaintenancePolicyMaintenanceExclusions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgecontainerClusterMaintenancePolicyMaintenanceExclusions]]], jsii.get(self, "maintenanceExclusionsInput"))

    @builtins.property
    @jsii.member(jsii_name="windowInput")
    def window_input(
        self,
    ) -> typing.Optional["EdgecontainerClusterMaintenancePolicyWindow"]:
        return typing.cast(typing.Optional["EdgecontainerClusterMaintenancePolicyWindow"], jsii.get(self, "windowInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EdgecontainerClusterMaintenancePolicy]:
        return typing.cast(typing.Optional[EdgecontainerClusterMaintenancePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EdgecontainerClusterMaintenancePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__330875f5400664cfcfc263c31e5e3889e18e5934ecb6c81aa6c42841dab7d457)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterMaintenancePolicyWindow",
    jsii_struct_bases=[],
    name_mapping={"recurring_window": "recurringWindow"},
)
class EdgecontainerClusterMaintenancePolicyWindow:
    def __init__(
        self,
        *,
        recurring_window: typing.Union["EdgecontainerClusterMaintenancePolicyWindowRecurringWindow", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param recurring_window: recurring_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#recurring_window EdgecontainerCluster#recurring_window}
        '''
        if isinstance(recurring_window, dict):
            recurring_window = EdgecontainerClusterMaintenancePolicyWindowRecurringWindow(**recurring_window)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00642e12b864001e987841df23f5febf260d826a3426b285f5bf24ece94c4124)
            check_type(argname="argument recurring_window", value=recurring_window, expected_type=type_hints["recurring_window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "recurring_window": recurring_window,
        }

    @builtins.property
    def recurring_window(
        self,
    ) -> "EdgecontainerClusterMaintenancePolicyWindowRecurringWindow":
        '''recurring_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#recurring_window EdgecontainerCluster#recurring_window}
        '''
        result = self._values.get("recurring_window")
        assert result is not None, "Required property 'recurring_window' is missing"
        return typing.cast("EdgecontainerClusterMaintenancePolicyWindowRecurringWindow", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgecontainerClusterMaintenancePolicyWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EdgecontainerClusterMaintenancePolicyWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterMaintenancePolicyWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94a59b35972adaaf4c452173f3bba1362b5737f7115dfacd4475d5fa78e5e47b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRecurringWindow")
    def put_recurring_window(
        self,
        *,
        recurrence: typing.Optional[builtins.str] = None,
        window: typing.Optional[typing.Union["EdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param recurrence: An RRULE (https://tools.ietf.org/html/rfc5545#section-3.8.5.3) for how this window recurs. They go on for the span of time between the start and end time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#recurrence EdgecontainerCluster#recurrence}
        :param window: window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#window EdgecontainerCluster#window}
        '''
        value = EdgecontainerClusterMaintenancePolicyWindowRecurringWindow(
            recurrence=recurrence, window=window
        )

        return typing.cast(None, jsii.invoke(self, "putRecurringWindow", [value]))

    @builtins.property
    @jsii.member(jsii_name="recurringWindow")
    def recurring_window(
        self,
    ) -> "EdgecontainerClusterMaintenancePolicyWindowRecurringWindowOutputReference":
        return typing.cast("EdgecontainerClusterMaintenancePolicyWindowRecurringWindowOutputReference", jsii.get(self, "recurringWindow"))

    @builtins.property
    @jsii.member(jsii_name="recurringWindowInput")
    def recurring_window_input(
        self,
    ) -> typing.Optional["EdgecontainerClusterMaintenancePolicyWindowRecurringWindow"]:
        return typing.cast(typing.Optional["EdgecontainerClusterMaintenancePolicyWindowRecurringWindow"], jsii.get(self, "recurringWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EdgecontainerClusterMaintenancePolicyWindow]:
        return typing.cast(typing.Optional[EdgecontainerClusterMaintenancePolicyWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EdgecontainerClusterMaintenancePolicyWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2d795773579532bc8f2bca4c450aaf76d9428580860d42590a916a798967522)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterMaintenancePolicyWindowRecurringWindow",
    jsii_struct_bases=[],
    name_mapping={"recurrence": "recurrence", "window": "window"},
)
class EdgecontainerClusterMaintenancePolicyWindowRecurringWindow:
    def __init__(
        self,
        *,
        recurrence: typing.Optional[builtins.str] = None,
        window: typing.Optional[typing.Union["EdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param recurrence: An RRULE (https://tools.ietf.org/html/rfc5545#section-3.8.5.3) for how this window recurs. They go on for the span of time between the start and end time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#recurrence EdgecontainerCluster#recurrence}
        :param window: window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#window EdgecontainerCluster#window}
        '''
        if isinstance(window, dict):
            window = EdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow(**window)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d35682fe8f1f43e65001c5069d8f03ad025ed64e18641b1e7cd121ebe07ccf79)
            check_type(argname="argument recurrence", value=recurrence, expected_type=type_hints["recurrence"])
            check_type(argname="argument window", value=window, expected_type=type_hints["window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if recurrence is not None:
            self._values["recurrence"] = recurrence
        if window is not None:
            self._values["window"] = window

    @builtins.property
    def recurrence(self) -> typing.Optional[builtins.str]:
        '''An RRULE (https://tools.ietf.org/html/rfc5545#section-3.8.5.3) for how this window recurs. They go on for the span of time between the start and end time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#recurrence EdgecontainerCluster#recurrence}
        '''
        result = self._values.get("recurrence")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def window(
        self,
    ) -> typing.Optional["EdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow"]:
        '''window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#window EdgecontainerCluster#window}
        '''
        result = self._values.get("window")
        return typing.cast(typing.Optional["EdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgecontainerClusterMaintenancePolicyWindowRecurringWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EdgecontainerClusterMaintenancePolicyWindowRecurringWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterMaintenancePolicyWindowRecurringWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c6336f2fb2962a6ba053abd33d2628e539b7dddadc980687695ad94dfb61ce5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putWindow")
    def put_window(
        self,
        *,
        end_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param end_time: The time that the window ends. The end time must take place after the start time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#end_time EdgecontainerCluster#end_time}
        :param start_time: The time that the window first starts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#start_time EdgecontainerCluster#start_time}
        '''
        value = EdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow(
            end_time=end_time, start_time=start_time
        )

        return typing.cast(None, jsii.invoke(self, "putWindow", [value]))

    @jsii.member(jsii_name="resetRecurrence")
    def reset_recurrence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecurrence", []))

    @jsii.member(jsii_name="resetWindow")
    def reset_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindow", []))

    @builtins.property
    @jsii.member(jsii_name="window")
    def window(
        self,
    ) -> "EdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindowOutputReference":
        return typing.cast("EdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindowOutputReference", jsii.get(self, "window"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceInput")
    def recurrence_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recurrenceInput"))

    @builtins.property
    @jsii.member(jsii_name="windowInput")
    def window_input(
        self,
    ) -> typing.Optional["EdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow"]:
        return typing.cast(typing.Optional["EdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow"], jsii.get(self, "windowInput"))

    @builtins.property
    @jsii.member(jsii_name="recurrence")
    def recurrence(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recurrence"))

    @recurrence.setter
    def recurrence(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c9a05d3f09b9d2787a6f4f7921c837f061cac7d57f231ab4b94db528026222)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recurrence", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EdgecontainerClusterMaintenancePolicyWindowRecurringWindow]:
        return typing.cast(typing.Optional[EdgecontainerClusterMaintenancePolicyWindowRecurringWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EdgecontainerClusterMaintenancePolicyWindowRecurringWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c168711ac8ab30ccf4c0088b952c628bd8d74e46aa83898cb58e5c9f649fbf25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow",
    jsii_struct_bases=[],
    name_mapping={"end_time": "endTime", "start_time": "startTime"},
)
class EdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow:
    def __init__(
        self,
        *,
        end_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param end_time: The time that the window ends. The end time must take place after the start time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#end_time EdgecontainerCluster#end_time}
        :param start_time: The time that the window first starts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#start_time EdgecontainerCluster#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aeec8302bded9fb3055ef3fb707da34661ff7b65dfc585c95b2051628813a50)
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if end_time is not None:
            self._values["end_time"] = end_time
        if start_time is not None:
            self._values["start_time"] = start_time

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''The time that the window ends. The end time must take place after the start time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#end_time EdgecontainerCluster#end_time}
        '''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''The time that the window first starts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#start_time EdgecontainerCluster#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__975e70264b3c507df9dd0cb90950b9cac28a6de944971e8c2ee120f94d7b11ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEndTime")
    def reset_end_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndTime", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be06bc1f6efb2d05a646591ca4e6af3cd4fd903587cfc798b404920409fdbdf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__309f96fd412c2cf945afe80a64dfd20a4e37f4939f1b81a33a8974cfba238da5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow]:
        return typing.cast(typing.Optional[EdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a82f9e80824292847cfed3686739d9888260c4eb74614923dcb4cc37b034f35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterNetworking",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_ipv4_cidr_blocks": "clusterIpv4CidrBlocks",
        "services_ipv4_cidr_blocks": "servicesIpv4CidrBlocks",
        "cluster_ipv6_cidr_blocks": "clusterIpv6CidrBlocks",
        "services_ipv6_cidr_blocks": "servicesIpv6CidrBlocks",
    },
)
class EdgecontainerClusterNetworking:
    def __init__(
        self,
        *,
        cluster_ipv4_cidr_blocks: typing.Sequence[builtins.str],
        services_ipv4_cidr_blocks: typing.Sequence[builtins.str],
        cluster_ipv6_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        services_ipv6_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cluster_ipv4_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these blocks. Only a single block is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#cluster_ipv4_cidr_blocks EdgecontainerCluster#cluster_ipv4_cidr_blocks}
        :param services_ipv4_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these blocks. Only a single block is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#services_ipv4_cidr_blocks EdgecontainerCluster#services_ipv4_cidr_blocks}
        :param cluster_ipv6_cidr_blocks: If specified, dual stack mode is enabled and all pods in the cluster are assigned an IPv6 address from these blocks alongside from an IPv4 address. Only a single block is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#cluster_ipv6_cidr_blocks EdgecontainerCluster#cluster_ipv6_cidr_blocks}
        :param services_ipv6_cidr_blocks: If specified, dual stack mode is enabled and all services in the cluster are assigned an IPv6 address from these blocks alongside from an IPv4 address. Only a single block is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#services_ipv6_cidr_blocks EdgecontainerCluster#services_ipv6_cidr_blocks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cecee04e938003fbe834ff81c4481c1426e055380b361c061119801f73bbc86)
            check_type(argname="argument cluster_ipv4_cidr_blocks", value=cluster_ipv4_cidr_blocks, expected_type=type_hints["cluster_ipv4_cidr_blocks"])
            check_type(argname="argument services_ipv4_cidr_blocks", value=services_ipv4_cidr_blocks, expected_type=type_hints["services_ipv4_cidr_blocks"])
            check_type(argname="argument cluster_ipv6_cidr_blocks", value=cluster_ipv6_cidr_blocks, expected_type=type_hints["cluster_ipv6_cidr_blocks"])
            check_type(argname="argument services_ipv6_cidr_blocks", value=services_ipv6_cidr_blocks, expected_type=type_hints["services_ipv6_cidr_blocks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_ipv4_cidr_blocks": cluster_ipv4_cidr_blocks,
            "services_ipv4_cidr_blocks": services_ipv4_cidr_blocks,
        }
        if cluster_ipv6_cidr_blocks is not None:
            self._values["cluster_ipv6_cidr_blocks"] = cluster_ipv6_cidr_blocks
        if services_ipv6_cidr_blocks is not None:
            self._values["services_ipv6_cidr_blocks"] = services_ipv6_cidr_blocks

    @builtins.property
    def cluster_ipv4_cidr_blocks(self) -> typing.List[builtins.str]:
        '''All pods in the cluster are assigned an RFC1918 IPv4 address from these blocks.

        Only a single block is supported. This field cannot be changed
        after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#cluster_ipv4_cidr_blocks EdgecontainerCluster#cluster_ipv4_cidr_blocks}
        '''
        result = self._values.get("cluster_ipv4_cidr_blocks")
        assert result is not None, "Required property 'cluster_ipv4_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def services_ipv4_cidr_blocks(self) -> typing.List[builtins.str]:
        '''All services in the cluster are assigned an RFC1918 IPv4 address from these blocks.

        Only a single block is supported. This field cannot be changed
        after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#services_ipv4_cidr_blocks EdgecontainerCluster#services_ipv4_cidr_blocks}
        '''
        result = self._values.get("services_ipv4_cidr_blocks")
        assert result is not None, "Required property 'services_ipv4_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cluster_ipv6_cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If specified, dual stack mode is enabled and all pods in the cluster are assigned an IPv6 address from these blocks alongside from an IPv4 address.

        Only a single block is supported. This field cannot be changed
        after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#cluster_ipv6_cidr_blocks EdgecontainerCluster#cluster_ipv6_cidr_blocks}
        '''
        result = self._values.get("cluster_ipv6_cidr_blocks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def services_ipv6_cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If specified, dual stack mode is enabled and all services in the cluster are assigned an IPv6 address from these blocks alongside from an IPv4 address.

        Only a single block is supported. This field cannot be changed
        after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#services_ipv6_cidr_blocks EdgecontainerCluster#services_ipv6_cidr_blocks}
        '''
        result = self._values.get("services_ipv6_cidr_blocks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgecontainerClusterNetworking(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EdgecontainerClusterNetworkingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterNetworkingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57cd9f0fbd8f967f7eefa17f13937b5ab7579895e24999fba059a404aa838876)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClusterIpv6CidrBlocks")
    def reset_cluster_ipv6_cidr_blocks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterIpv6CidrBlocks", []))

    @jsii.member(jsii_name="resetServicesIpv6CidrBlocks")
    def reset_services_ipv6_cidr_blocks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServicesIpv6CidrBlocks", []))

    @builtins.property
    @jsii.member(jsii_name="networkType")
    def network_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkType"))

    @builtins.property
    @jsii.member(jsii_name="clusterIpv4CidrBlocksInput")
    def cluster_ipv4_cidr_blocks_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "clusterIpv4CidrBlocksInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIpv6CidrBlocksInput")
    def cluster_ipv6_cidr_blocks_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "clusterIpv6CidrBlocksInput"))

    @builtins.property
    @jsii.member(jsii_name="servicesIpv4CidrBlocksInput")
    def services_ipv4_cidr_blocks_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "servicesIpv4CidrBlocksInput"))

    @builtins.property
    @jsii.member(jsii_name="servicesIpv6CidrBlocksInput")
    def services_ipv6_cidr_blocks_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "servicesIpv6CidrBlocksInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIpv4CidrBlocks")
    def cluster_ipv4_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "clusterIpv4CidrBlocks"))

    @cluster_ipv4_cidr_blocks.setter
    def cluster_ipv4_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__262f704b1484cc84eb7fc45af2a1a8067b418a948707e706feb253f8b7e79a6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterIpv4CidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterIpv6CidrBlocks")
    def cluster_ipv6_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "clusterIpv6CidrBlocks"))

    @cluster_ipv6_cidr_blocks.setter
    def cluster_ipv6_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb74dadbf149c1d451f3e9338eb257fa767dce4f1e05a446cc81d3197a2dc763)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterIpv6CidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servicesIpv4CidrBlocks")
    def services_ipv4_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "servicesIpv4CidrBlocks"))

    @services_ipv4_cidr_blocks.setter
    def services_ipv4_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d5063788b125e0fb72df64a96bd4d3acd45be564878c5bd56994dca712c6bae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servicesIpv4CidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servicesIpv6CidrBlocks")
    def services_ipv6_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "servicesIpv6CidrBlocks"))

    @services_ipv6_cidr_blocks.setter
    def services_ipv6_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccdcc51d5ab65d4359cd297ea58b884730c28de16d7395a762b74bf24bf03b5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servicesIpv6CidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EdgecontainerClusterNetworking]:
        return typing.cast(typing.Optional[EdgecontainerClusterNetworking], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EdgecontainerClusterNetworking],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__685e587d68ddbf798fc91bee61f70ed990c8d1fe45703eb00ffe27ea01611cf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterSystemAddonsConfig",
    jsii_struct_bases=[],
    name_mapping={"ingress": "ingress"},
)
class EdgecontainerClusterSystemAddonsConfig:
    def __init__(
        self,
        *,
        ingress: typing.Optional[typing.Union["EdgecontainerClusterSystemAddonsConfigIngress", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ingress: ingress block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#ingress EdgecontainerCluster#ingress}
        '''
        if isinstance(ingress, dict):
            ingress = EdgecontainerClusterSystemAddonsConfigIngress(**ingress)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a60704573d07284b9d0b72e4d01e0f80843947c16e5ec57e04a6125cfa08421c)
            check_type(argname="argument ingress", value=ingress, expected_type=type_hints["ingress"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ingress is not None:
            self._values["ingress"] = ingress

    @builtins.property
    def ingress(
        self,
    ) -> typing.Optional["EdgecontainerClusterSystemAddonsConfigIngress"]:
        '''ingress block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#ingress EdgecontainerCluster#ingress}
        '''
        result = self._values.get("ingress")
        return typing.cast(typing.Optional["EdgecontainerClusterSystemAddonsConfigIngress"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgecontainerClusterSystemAddonsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterSystemAddonsConfigIngress",
    jsii_struct_bases=[],
    name_mapping={"disabled": "disabled", "ipv4_vip": "ipv4Vip"},
)
class EdgecontainerClusterSystemAddonsConfigIngress:
    def __init__(
        self,
        *,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ipv4_vip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disabled: Whether Ingress is disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#disabled EdgecontainerCluster#disabled}
        :param ipv4_vip: Ingress VIP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#ipv4_vip EdgecontainerCluster#ipv4_vip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b99457226d2f806577cc422efdc60295c4883b288f5df75d1ddf1b9ffb613583)
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument ipv4_vip", value=ipv4_vip, expected_type=type_hints["ipv4_vip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disabled is not None:
            self._values["disabled"] = disabled
        if ipv4_vip is not None:
            self._values["ipv4_vip"] = ipv4_vip

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Ingress is disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#disabled EdgecontainerCluster#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ipv4_vip(self) -> typing.Optional[builtins.str]:
        '''Ingress VIP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#ipv4_vip EdgecontainerCluster#ipv4_vip}
        '''
        result = self._values.get("ipv4_vip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgecontainerClusterSystemAddonsConfigIngress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EdgecontainerClusterSystemAddonsConfigIngressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterSystemAddonsConfigIngressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79cb324ba994fb3b593f167908a3b8ae1c6d5b1d5f753eeb43eff9c8f08f7a21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetIpv4Vip")
    def reset_ipv4_vip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv4Vip", []))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv4VipInput")
    def ipv4_vip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv4VipInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__8f534d840bf0895b00df90f97e7b8f0a4e4214e8a64d05f073ff77cbc7511a43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv4Vip")
    def ipv4_vip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv4Vip"))

    @ipv4_vip.setter
    def ipv4_vip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__301393472df1246816036c796d60ae6eaa2b86195fe6becdbd1cfb31568bdb01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv4Vip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EdgecontainerClusterSystemAddonsConfigIngress]:
        return typing.cast(typing.Optional[EdgecontainerClusterSystemAddonsConfigIngress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EdgecontainerClusterSystemAddonsConfigIngress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df825a9675d48cf9bf539d953c40865d2e432a9e6ad17753809883b5215db48b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EdgecontainerClusterSystemAddonsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterSystemAddonsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71e232a7e268affc38914dafe23c6e087df3228d88eaabf020fd0281cbc02c70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIngress")
    def put_ingress(
        self,
        *,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ipv4_vip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disabled: Whether Ingress is disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#disabled EdgecontainerCluster#disabled}
        :param ipv4_vip: Ingress VIP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#ipv4_vip EdgecontainerCluster#ipv4_vip}
        '''
        value = EdgecontainerClusterSystemAddonsConfigIngress(
            disabled=disabled, ipv4_vip=ipv4_vip
        )

        return typing.cast(None, jsii.invoke(self, "putIngress", [value]))

    @jsii.member(jsii_name="resetIngress")
    def reset_ingress(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngress", []))

    @builtins.property
    @jsii.member(jsii_name="ingress")
    def ingress(self) -> EdgecontainerClusterSystemAddonsConfigIngressOutputReference:
        return typing.cast(EdgecontainerClusterSystemAddonsConfigIngressOutputReference, jsii.get(self, "ingress"))

    @builtins.property
    @jsii.member(jsii_name="ingressInput")
    def ingress_input(
        self,
    ) -> typing.Optional[EdgecontainerClusterSystemAddonsConfigIngress]:
        return typing.cast(typing.Optional[EdgecontainerClusterSystemAddonsConfigIngress], jsii.get(self, "ingressInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EdgecontainerClusterSystemAddonsConfig]:
        return typing.cast(typing.Optional[EdgecontainerClusterSystemAddonsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EdgecontainerClusterSystemAddonsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08dd9595c837eb34a36030de4a9e9ebf0b1348f94c17c25f533f55086c4cc4dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class EdgecontainerClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#create EdgecontainerCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#delete EdgecontainerCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#update EdgecontainerCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19f1fb663790e03b94dd742df3c8524ed71ded0ae35764b6ba66307150f23740)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#create EdgecontainerCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#delete EdgecontainerCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/edgecontainer_cluster#update EdgecontainerCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgecontainerClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EdgecontainerClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.edgecontainerCluster.EdgecontainerClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c69f496bd232d96f9a9aba9c8f7d19fee785e04d03a899e5fe26556ae0e34309)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15dcc9dbf8d77e06d11f56010fa36f963cf6543b306f798baa1332d16a7d2b6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1134290a40a7388726aff969b781d606fc360f9e9cc01fbd6b08b652df0fb0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2caedb3c4e5ccc13c7cb23dd94624d638669cbd00c2f031b12d7779f48cd942e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgecontainerClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgecontainerClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgecontainerClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bf31c911c5274db974d07b6abf7eb710230ffa9809446558f477a7daca8bd41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "EdgecontainerCluster",
    "EdgecontainerClusterAuthorization",
    "EdgecontainerClusterAuthorizationAdminUsers",
    "EdgecontainerClusterAuthorizationAdminUsersOutputReference",
    "EdgecontainerClusterAuthorizationOutputReference",
    "EdgecontainerClusterConfig",
    "EdgecontainerClusterControlPlane",
    "EdgecontainerClusterControlPlaneEncryption",
    "EdgecontainerClusterControlPlaneEncryptionKmsStatus",
    "EdgecontainerClusterControlPlaneEncryptionKmsStatusList",
    "EdgecontainerClusterControlPlaneEncryptionKmsStatusOutputReference",
    "EdgecontainerClusterControlPlaneEncryptionOutputReference",
    "EdgecontainerClusterControlPlaneLocal",
    "EdgecontainerClusterControlPlaneLocalOutputReference",
    "EdgecontainerClusterControlPlaneOutputReference",
    "EdgecontainerClusterControlPlaneRemote",
    "EdgecontainerClusterControlPlaneRemoteOutputReference",
    "EdgecontainerClusterFleet",
    "EdgecontainerClusterFleetOutputReference",
    "EdgecontainerClusterMaintenanceEvents",
    "EdgecontainerClusterMaintenanceEventsList",
    "EdgecontainerClusterMaintenanceEventsOutputReference",
    "EdgecontainerClusterMaintenancePolicy",
    "EdgecontainerClusterMaintenancePolicyMaintenanceExclusions",
    "EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsList",
    "EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsOutputReference",
    "EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow",
    "EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindowOutputReference",
    "EdgecontainerClusterMaintenancePolicyOutputReference",
    "EdgecontainerClusterMaintenancePolicyWindow",
    "EdgecontainerClusterMaintenancePolicyWindowOutputReference",
    "EdgecontainerClusterMaintenancePolicyWindowRecurringWindow",
    "EdgecontainerClusterMaintenancePolicyWindowRecurringWindowOutputReference",
    "EdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow",
    "EdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindowOutputReference",
    "EdgecontainerClusterNetworking",
    "EdgecontainerClusterNetworkingOutputReference",
    "EdgecontainerClusterSystemAddonsConfig",
    "EdgecontainerClusterSystemAddonsConfigIngress",
    "EdgecontainerClusterSystemAddonsConfigIngressOutputReference",
    "EdgecontainerClusterSystemAddonsConfigOutputReference",
    "EdgecontainerClusterTimeouts",
    "EdgecontainerClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__557451deba8d70d6cb5a87b46e0d33bcc69b3e35f1ba1bdb1559edc2759c3af9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    authorization: typing.Union[EdgecontainerClusterAuthorization, typing.Dict[builtins.str, typing.Any]],
    fleet: typing.Union[EdgecontainerClusterFleet, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    networking: typing.Union[EdgecontainerClusterNetworking, typing.Dict[builtins.str, typing.Any]],
    control_plane: typing.Optional[typing.Union[EdgecontainerClusterControlPlane, typing.Dict[builtins.str, typing.Any]]] = None,
    control_plane_encryption: typing.Optional[typing.Union[EdgecontainerClusterControlPlaneEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    default_max_pods_per_node: typing.Optional[jsii.Number] = None,
    external_load_balancer_ipv4_address_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    maintenance_policy: typing.Optional[typing.Union[EdgecontainerClusterMaintenancePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    release_channel: typing.Optional[builtins.str] = None,
    system_addons_config: typing.Optional[typing.Union[EdgecontainerClusterSystemAddonsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    target_version: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[EdgecontainerClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4d69b07ee3f454caf1ff0f937619a16708ef57ce528e17e43ef5e579d03cc3d1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4895560f89154d12416feffe0c2371af4409e8261643f40310e434780727aa85(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23634877988ff809b8a0846af6993a5b7a36e57d53f310c80e3a51f55869841b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b293ff9366dad623005873a6d47eac98b364f8f8c27122ff34042d332a50abc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ba874758e379d09c28d671623b1294ec624c78f0762aaaabd658e36377ef21(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f177e337271597f3e534d866de2d5097cf3ea6ba3bd711ab41361521817f3f8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e46c53b205f12f3c05ab1f27e00b01ff1f24785b4a37a792b4bbe6f1e2551c8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0840c960528c1ec89dad93911840c858baf2aeb0bcaab9d03cf3f265307aefaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf3104fb174abeece9ab7835738ff252a62e29d6c472b052c06676271431dfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__420f4dc8299083fd6ce138bea1ca086ff76eea0a7b4b005dd2ed81bcccc1e465(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbe51abb8ad23bab4a3e8b94ab4c7c8883b009cf5517ce9651f4994aba83cdcc(
    *,
    admin_users: typing.Union[EdgecontainerClusterAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94aeb0215a287f2745fd85983f86631f4073aeb8fdd89ce99a814ac7ca0509de(
    *,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a6d95f3d66110da92b7f160b9cd58068ba02979b2525b3434fca6fccd0e7253(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a25de055b6e2e50b1492f8224e58b1e9bce826fb3ffe718fae0bfe732d76589f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1851de96a2512adae32b8084fc7561fa65614760dd4d248d7973c75b70bce57f(
    value: typing.Optional[EdgecontainerClusterAuthorizationAdminUsers],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e651d58c933fd965074392b0b3bbd89d4d47b35b9422f41c38350a3e4809ff37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2238b5c36a3f00e59c8f054df23b35fb35bef5e34cecb1c076d57a57960e2f6f(
    value: typing.Optional[EdgecontainerClusterAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6af49bc985f95ec5dda81d63e19dd55d432d04887be212aed5edd30afc0f524c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    authorization: typing.Union[EdgecontainerClusterAuthorization, typing.Dict[builtins.str, typing.Any]],
    fleet: typing.Union[EdgecontainerClusterFleet, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    networking: typing.Union[EdgecontainerClusterNetworking, typing.Dict[builtins.str, typing.Any]],
    control_plane: typing.Optional[typing.Union[EdgecontainerClusterControlPlane, typing.Dict[builtins.str, typing.Any]]] = None,
    control_plane_encryption: typing.Optional[typing.Union[EdgecontainerClusterControlPlaneEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    default_max_pods_per_node: typing.Optional[jsii.Number] = None,
    external_load_balancer_ipv4_address_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    maintenance_policy: typing.Optional[typing.Union[EdgecontainerClusterMaintenancePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    release_channel: typing.Optional[builtins.str] = None,
    system_addons_config: typing.Optional[typing.Union[EdgecontainerClusterSystemAddonsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    target_version: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[EdgecontainerClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9daca5c3029019cd555e01be7d94ee9f3f2086fbf8293800e8a0bd2eea7409f4(
    *,
    local: typing.Optional[typing.Union[EdgecontainerClusterControlPlaneLocal, typing.Dict[builtins.str, typing.Any]]] = None,
    remote: typing.Optional[typing.Union[EdgecontainerClusterControlPlaneRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6ab462416f75f716cd454346aa83defc98f7f2db6c68600d1c3a728fe108572(
    *,
    kms_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54740dcccae7fefd4b8b5bee1a3fd3a89ca296a2249a2277e626d10f0045884a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d513bdcc2d48e674324ad0b0a26b5f903860901edf1c51741980096603bdb23(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99eef90cd60ede8b2abced5cd7bb11886aeb29949024c0dd7a7b150a7c67fd6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbd3e87a31715b9f304627823c27490659bf417b859f6ea15ae863d872bb0e9a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adca4e845ee2272da1bbfce5a138d7f99b1d761f9f6eafe9ea9dd5dc3673fcdd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcb0547a36b790efa1adc718dc98b74a022b457d459c3d694afa27446a4cb30b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ffcabd44aa1965ce1a94cc2299faf6d7ed4a530f5ef3c4a98f98bfa8a968e63(
    value: typing.Optional[EdgecontainerClusterControlPlaneEncryptionKmsStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b27b329584930d4abd058be58acd352d444e0a79c407b74a364aff9c60f9a36b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60ff65ab6e7176a76a5193c8af2b9269301959bd3425884c94c99a4fd9d4827e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2be8044629002e09938eccc364b21a948ff0783d4cf421cc2b297c28784908e(
    value: typing.Optional[EdgecontainerClusterControlPlaneEncryption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed66a878a51a19d10bfe4852ee65f6cc3e2dd670ee9b962f931bd0f1ddefac1(
    *,
    machine_filter: typing.Optional[builtins.str] = None,
    node_count: typing.Optional[jsii.Number] = None,
    node_location: typing.Optional[builtins.str] = None,
    shared_deployment_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bc6eaa0510cbe42441c0dc1552af020f7ceff7a7d28f82f3cb330d1c6f00bdb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b75d78e18d47c3e0ad01fddc16b964548062c69110f9dc5375da41891fc3a197(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b4717c68f42c5c6aaca15ab06638917afd7c7cba66b3bedbe47e8d1097394d6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e5e43d20ace03f17a741edc3f9d6ecabeb2214fb33643a851d783ecc6ffc02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd1b04ef4c6a9f6c25d09238897edb9986d264234395f6da300b6c47e8f8d412(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a0443fc2f82cb1f27a84934200514823c470f34cf9d9a22a7b69976a0f8d665(
    value: typing.Optional[EdgecontainerClusterControlPlaneLocal],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1290f0083b7ecb2ebf0758dd376c8a6ba65eb10129280c6b0b6dae4750043df4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd426ed4c01291c3efa3b05e2bc59bfa74d094f34b1332806117f14830b1560f(
    value: typing.Optional[EdgecontainerClusterControlPlane],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3a8f51c9d3496c55cf83e1234983c1f75f546b786c765d9e712c471056a81a8(
    *,
    node_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae45e41410a481da630d0c662aea00d9d9b4de51f9d23369ca0d03717c15bca9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0545cb7326474830c49f48133fd5da4b7d814a21fa196eb757af60e29614370(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d24a621bf601441f280117ebf178348faf73cbf9daf6d742ae6f462fc0b4a758(
    value: typing.Optional[EdgecontainerClusterControlPlaneRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f342ef9c43f860c3a0c7d66ebfefaf6ad48b90d02d7a0af4c2355ccfb363925b(
    *,
    project: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c72a71b615db1ad9676c51c1d2946c0c222e55ae42d566cf9fe87c8999f5d83a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced0583bb60720da0b51c50745106551b0c593cbd6ad5e7d1dbd5c18296ebafb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bab4f220f44f4ed405fbd2c958692a6c7557e7869cdcc5f35c0cbe835b454ce6(
    value: typing.Optional[EdgecontainerClusterFleet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d6067c857007ee07215205685e932934c4d1993c77f7b493f018999e0038528(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7110e5d96007bd2a6ad5370ea284c1aa6fe6a351be1d91acf97ad0be2dd049f5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bc265395b50cea56d968ca62ed942a71393fc2542ea5afb4bc0e1b0c3e7b930(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70fe307c8989a17e093d48198fe8e47da4f00d50b57c26318786062e86366fd3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2edf8693bcf17b5eb576df1454a271bf46b888345a87c3d2d7d08fe2c7f0222(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca2c06acff7e2f5e77e02eb20f98a7cd92477540349ba01df9474328ac143245(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73cb311441089e21776388942903c26f8cdb52481ce550d5e8a5ffda6a4a0964(
    value: typing.Optional[EdgecontainerClusterMaintenanceEvents],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99524251cc7f976e2b79d58fa662e99cb1c9b71def8bbf00617be1a69d45cfe1(
    *,
    window: typing.Union[EdgecontainerClusterMaintenancePolicyWindow, typing.Dict[builtins.str, typing.Any]],
    maintenance_exclusions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EdgecontainerClusterMaintenancePolicyMaintenanceExclusions, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f00c493f4d4d0ef52d9563e541d44b170acf3275b0fc7145f730ab4d0562d7(
    *,
    id: typing.Optional[builtins.str] = None,
    window: typing.Optional[typing.Union[EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aecdc2f5a0d8bd56165d35026c1dc00b823206db7b98d2b893ecadc8569eb53e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb9a7b0433d8fb2d2ceda9a53d7f4b8752abf8db628c66deca50f1ef425e2e0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65cf147b30bbeb4dbdaac9549c9f82677205cd30283f934b0c63f2605ba5eff8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d6a4e8100b54b0129c69ed3966baa6e70ea428fc431240721a2bb93370f8142(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43551a2a2a445db675df1e0ed7f8973516466e70fa6c7d11622b251ee06dd686(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd785f37b294b5c25850a0e1865da2d62d47d285f630cdc5a6b4a21f02434ae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EdgecontainerClusterMaintenancePolicyMaintenanceExclusions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__667e7950ade5520d23ce9a34f55a909175f0993cc7b14d92846e4ab298cfe489(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e038a4db2f743c25fa1df2837e1b1e42a97e7d91f9f92e57cd5009d3e50c1c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__589effc6bc4ba1ca256c02d91c3871b16ba05ff4ebc53952ef362a66fd1756b1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgecontainerClusterMaintenancePolicyMaintenanceExclusions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cc4d699d4431df5c26af7f4102618d366c5c8d08bbe3120a0559748f1534c3e(
    *,
    end_time: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f12365d26c288d662af3c4f5e83132bdba8ab8c6a594efb205fbfc52ef1d5cd0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72884e76a3b44a02506975f3b810ab1d8e8dce023c0922ad0b530766b7ae7f9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aba132eff208aa7be232a6eb6ab431e5773470ff4331bcd1019c24ca4a880fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2c680d1aeadea4051abf92c7596a09ba0bc7b6268631e69940d96effb82e9f0(
    value: typing.Optional[EdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ed0969401cc9269dc364621d895eb33d63fd849f985b361ce9cf648dcd9d1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f63f90fd221dece72046e07078f7488b69edaf9fcfbfdc2ee44ca8bb4e90cfb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EdgecontainerClusterMaintenancePolicyMaintenanceExclusions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__330875f5400664cfcfc263c31e5e3889e18e5934ecb6c81aa6c42841dab7d457(
    value: typing.Optional[EdgecontainerClusterMaintenancePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00642e12b864001e987841df23f5febf260d826a3426b285f5bf24ece94c4124(
    *,
    recurring_window: typing.Union[EdgecontainerClusterMaintenancePolicyWindowRecurringWindow, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a59b35972adaaf4c452173f3bba1362b5737f7115dfacd4475d5fa78e5e47b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2d795773579532bc8f2bca4c450aaf76d9428580860d42590a916a798967522(
    value: typing.Optional[EdgecontainerClusterMaintenancePolicyWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d35682fe8f1f43e65001c5069d8f03ad025ed64e18641b1e7cd121ebe07ccf79(
    *,
    recurrence: typing.Optional[builtins.str] = None,
    window: typing.Optional[typing.Union[EdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c6336f2fb2962a6ba053abd33d2628e539b7dddadc980687695ad94dfb61ce5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c9a05d3f09b9d2787a6f4f7921c837f061cac7d57f231ab4b94db528026222(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c168711ac8ab30ccf4c0088b952c628bd8d74e46aa83898cb58e5c9f649fbf25(
    value: typing.Optional[EdgecontainerClusterMaintenancePolicyWindowRecurringWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aeec8302bded9fb3055ef3fb707da34661ff7b65dfc585c95b2051628813a50(
    *,
    end_time: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975e70264b3c507df9dd0cb90950b9cac28a6de944971e8c2ee120f94d7b11ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be06bc1f6efb2d05a646591ca4e6af3cd4fd903587cfc798b404920409fdbdf5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__309f96fd412c2cf945afe80a64dfd20a4e37f4939f1b81a33a8974cfba238da5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a82f9e80824292847cfed3686739d9888260c4eb74614923dcb4cc37b034f35(
    value: typing.Optional[EdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cecee04e938003fbe834ff81c4481c1426e055380b361c061119801f73bbc86(
    *,
    cluster_ipv4_cidr_blocks: typing.Sequence[builtins.str],
    services_ipv4_cidr_blocks: typing.Sequence[builtins.str],
    cluster_ipv6_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
    services_ipv6_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57cd9f0fbd8f967f7eefa17f13937b5ab7579895e24999fba059a404aa838876(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262f704b1484cc84eb7fc45af2a1a8067b418a948707e706feb253f8b7e79a6b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb74dadbf149c1d451f3e9338eb257fa767dce4f1e05a446cc81d3197a2dc763(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d5063788b125e0fb72df64a96bd4d3acd45be564878c5bd56994dca712c6bae(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccdcc51d5ab65d4359cd297ea58b884730c28de16d7395a762b74bf24bf03b5c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__685e587d68ddbf798fc91bee61f70ed990c8d1fe45703eb00ffe27ea01611cf5(
    value: typing.Optional[EdgecontainerClusterNetworking],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a60704573d07284b9d0b72e4d01e0f80843947c16e5ec57e04a6125cfa08421c(
    *,
    ingress: typing.Optional[typing.Union[EdgecontainerClusterSystemAddonsConfigIngress, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b99457226d2f806577cc422efdc60295c4883b288f5df75d1ddf1b9ffb613583(
    *,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ipv4_vip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79cb324ba994fb3b593f167908a3b8ae1c6d5b1d5f753eeb43eff9c8f08f7a21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f534d840bf0895b00df90f97e7b8f0a4e4214e8a64d05f073ff77cbc7511a43(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__301393472df1246816036c796d60ae6eaa2b86195fe6becdbd1cfb31568bdb01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df825a9675d48cf9bf539d953c40865d2e432a9e6ad17753809883b5215db48b(
    value: typing.Optional[EdgecontainerClusterSystemAddonsConfigIngress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e232a7e268affc38914dafe23c6e087df3228d88eaabf020fd0281cbc02c70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08dd9595c837eb34a36030de4a9e9ebf0b1348f94c17c25f533f55086c4cc4dc(
    value: typing.Optional[EdgecontainerClusterSystemAddonsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f1fb663790e03b94dd742df3c8524ed71ded0ae35764b6ba66307150f23740(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c69f496bd232d96f9a9aba9c8f7d19fee785e04d03a899e5fe26556ae0e34309(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15dcc9dbf8d77e06d11f56010fa36f963cf6543b306f798baa1332d16a7d2b6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1134290a40a7388726aff969b781d606fc360f9e9cc01fbd6b08b652df0fb0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2caedb3c4e5ccc13c7cb23dd94624d638669cbd00c2f031b12d7779f48cd942e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bf31c911c5274db974d07b6abf7eb710230ffa9809446558f477a7daca8bd41(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EdgecontainerClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
