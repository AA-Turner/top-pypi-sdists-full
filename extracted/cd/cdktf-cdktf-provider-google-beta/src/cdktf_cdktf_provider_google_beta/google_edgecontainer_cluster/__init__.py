r'''
# `google_edgecontainer_cluster`

Refer to the Terraform Registry for docs: [`google_edgecontainer_cluster`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster).
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


class GoogleEdgecontainerCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster google_edgecontainer_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        authorization: typing.Union["GoogleEdgecontainerClusterAuthorization", typing.Dict[builtins.str, typing.Any]],
        fleet: typing.Union["GoogleEdgecontainerClusterFleet", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        networking: typing.Union["GoogleEdgecontainerClusterNetworking", typing.Dict[builtins.str, typing.Any]],
        control_plane: typing.Optional[typing.Union["GoogleEdgecontainerClusterControlPlane", typing.Dict[builtins.str, typing.Any]]] = None,
        control_plane_encryption: typing.Optional[typing.Union["GoogleEdgecontainerClusterControlPlaneEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
        default_max_pods_per_node: typing.Optional[jsii.Number] = None,
        external_load_balancer_ipv4_address_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        maintenance_policy: typing.Optional[typing.Union["GoogleEdgecontainerClusterMaintenancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        release_channel: typing.Optional[builtins.str] = None,
        system_addons_config: typing.Optional[typing.Union["GoogleEdgecontainerClusterSystemAddonsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        target_version: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleEdgecontainerClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster google_edgecontainer_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#authorization GoogleEdgecontainerCluster#authorization}
        :param fleet: fleet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#fleet GoogleEdgecontainerCluster#fleet}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#location GoogleEdgecontainerCluster#location}
        :param name: The GDCE cluster name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#name GoogleEdgecontainerCluster#name}
        :param networking: networking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#networking GoogleEdgecontainerCluster#networking}
        :param control_plane: control_plane block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#control_plane GoogleEdgecontainerCluster#control_plane}
        :param control_plane_encryption: control_plane_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#control_plane_encryption GoogleEdgecontainerCluster#control_plane_encryption}
        :param default_max_pods_per_node: The default maximum number of pods per node used if a maximum value is not specified explicitly for a node pool in this cluster. If unspecified, the Kubernetes default value will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#default_max_pods_per_node GoogleEdgecontainerCluster#default_max_pods_per_node}
        :param external_load_balancer_ipv4_address_pools: Address pools for cluster data plane external load balancing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#external_load_balancer_ipv4_address_pools GoogleEdgecontainerCluster#external_load_balancer_ipv4_address_pools}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#id GoogleEdgecontainerCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for the edgecloud cluster. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#labels GoogleEdgecontainerCluster#labels}
        :param maintenance_policy: maintenance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#maintenance_policy GoogleEdgecontainerCluster#maintenance_policy}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#project GoogleEdgecontainerCluster#project}.
        :param release_channel: The release channel a cluster is subscribed to. Possible values: ["RELEASE_CHANNEL_UNSPECIFIED", "NONE", "REGULAR"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#release_channel GoogleEdgecontainerCluster#release_channel}
        :param system_addons_config: system_addons_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#system_addons_config GoogleEdgecontainerCluster#system_addons_config}
        :param target_version: The target cluster version. For example: "1.5.0". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#target_version GoogleEdgecontainerCluster#target_version}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#timeouts GoogleEdgecontainerCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88d5b570f090931fbeb5942edac0b586bad0752f9efa7213966e01d8e7e01d48)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleEdgecontainerClusterConfig(
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
        '''Generates CDKTF code for importing a GoogleEdgecontainerCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleEdgecontainerCluster to import.
        :param import_from_id: The id of the existing GoogleEdgecontainerCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleEdgecontainerCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73da1cf9aa830023da7891c042367de927136e2a8a6ab07524378445fc402795)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAuthorization")
    def put_authorization(
        self,
        *,
        admin_users: typing.Union["GoogleEdgecontainerClusterAuthorizationAdminUsers", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#admin_users GoogleEdgecontainerCluster#admin_users}
        '''
        value = GoogleEdgecontainerClusterAuthorization(admin_users=admin_users)

        return typing.cast(None, jsii.invoke(self, "putAuthorization", [value]))

    @jsii.member(jsii_name="putControlPlane")
    def put_control_plane(
        self,
        *,
        local: typing.Optional[typing.Union["GoogleEdgecontainerClusterControlPlaneLocal", typing.Dict[builtins.str, typing.Any]]] = None,
        remote: typing.Optional[typing.Union["GoogleEdgecontainerClusterControlPlaneRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param local: local block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#local GoogleEdgecontainerCluster#local}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#remote GoogleEdgecontainerCluster#remote}
        '''
        value = GoogleEdgecontainerClusterControlPlane(local=local, remote=remote)

        return typing.cast(None, jsii.invoke(self, "putControlPlane", [value]))

    @jsii.member(jsii_name="putControlPlaneEncryption")
    def put_control_plane_encryption(
        self,
        *,
        kms_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key: The Cloud KMS CryptoKey e.g. projects/{project}/locations/{location}/keyRings/{keyRing}/cryptoKeys/{cryptoKey} to use for protecting control plane disks. If not specified, a Google-managed key will be used instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#kms_key GoogleEdgecontainerCluster#kms_key}
        '''
        value = GoogleEdgecontainerClusterControlPlaneEncryption(kms_key=kms_key)

        return typing.cast(None, jsii.invoke(self, "putControlPlaneEncryption", [value]))

    @jsii.member(jsii_name="putFleet")
    def put_fleet(self, *, project: builtins.str) -> None:
        '''
        :param project: The name of the Fleet host project where this cluster will be registered. Project names are formatted as 'projects/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#project GoogleEdgecontainerCluster#project}
        '''
        value = GoogleEdgecontainerClusterFleet(project=project)

        return typing.cast(None, jsii.invoke(self, "putFleet", [value]))

    @jsii.member(jsii_name="putMaintenancePolicy")
    def put_maintenance_policy(
        self,
        *,
        window: typing.Union["GoogleEdgecontainerClusterMaintenancePolicyWindow", typing.Dict[builtins.str, typing.Any]],
        maintenance_exclusions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusions", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param window: window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#window GoogleEdgecontainerCluster#window}
        :param maintenance_exclusions: maintenance_exclusions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#maintenance_exclusions GoogleEdgecontainerCluster#maintenance_exclusions}
        '''
        value = GoogleEdgecontainerClusterMaintenancePolicy(
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
        :param cluster_ipv4_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these blocks. Only a single block is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#cluster_ipv4_cidr_blocks GoogleEdgecontainerCluster#cluster_ipv4_cidr_blocks}
        :param services_ipv4_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these blocks. Only a single block is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#services_ipv4_cidr_blocks GoogleEdgecontainerCluster#services_ipv4_cidr_blocks}
        :param cluster_ipv6_cidr_blocks: If specified, dual stack mode is enabled and all pods in the cluster are assigned an IPv6 address from these blocks alongside from an IPv4 address. Only a single block is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#cluster_ipv6_cidr_blocks GoogleEdgecontainerCluster#cluster_ipv6_cidr_blocks}
        :param services_ipv6_cidr_blocks: If specified, dual stack mode is enabled and all services in the cluster are assigned an IPv6 address from these blocks alongside from an IPv4 address. Only a single block is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#services_ipv6_cidr_blocks GoogleEdgecontainerCluster#services_ipv6_cidr_blocks}
        '''
        value = GoogleEdgecontainerClusterNetworking(
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
        ingress: typing.Optional[typing.Union["GoogleEdgecontainerClusterSystemAddonsConfigIngress", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ingress: ingress block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#ingress GoogleEdgecontainerCluster#ingress}
        '''
        value = GoogleEdgecontainerClusterSystemAddonsConfig(ingress=ingress)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#create GoogleEdgecontainerCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#delete GoogleEdgecontainerCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#update GoogleEdgecontainerCluster#update}.
        '''
        value = GoogleEdgecontainerClusterTimeouts(
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
    def authorization(self) -> "GoogleEdgecontainerClusterAuthorizationOutputReference":
        return typing.cast("GoogleEdgecontainerClusterAuthorizationOutputReference", jsii.get(self, "authorization"))

    @builtins.property
    @jsii.member(jsii_name="clusterCaCertificate")
    def cluster_ca_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterCaCertificate"))

    @builtins.property
    @jsii.member(jsii_name="controlPlane")
    def control_plane(self) -> "GoogleEdgecontainerClusterControlPlaneOutputReference":
        return typing.cast("GoogleEdgecontainerClusterControlPlaneOutputReference", jsii.get(self, "controlPlane"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneEncryption")
    def control_plane_encryption(
        self,
    ) -> "GoogleEdgecontainerClusterControlPlaneEncryptionOutputReference":
        return typing.cast("GoogleEdgecontainerClusterControlPlaneEncryptionOutputReference", jsii.get(self, "controlPlaneEncryption"))

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
    def fleet(self) -> "GoogleEdgecontainerClusterFleetOutputReference":
        return typing.cast("GoogleEdgecontainerClusterFleetOutputReference", jsii.get(self, "fleet"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceEvents")
    def maintenance_events(self) -> "GoogleEdgecontainerClusterMaintenanceEventsList":
        return typing.cast("GoogleEdgecontainerClusterMaintenanceEventsList", jsii.get(self, "maintenanceEvents"))

    @builtins.property
    @jsii.member(jsii_name="maintenancePolicy")
    def maintenance_policy(
        self,
    ) -> "GoogleEdgecontainerClusterMaintenancePolicyOutputReference":
        return typing.cast("GoogleEdgecontainerClusterMaintenancePolicyOutputReference", jsii.get(self, "maintenancePolicy"))

    @builtins.property
    @jsii.member(jsii_name="networking")
    def networking(self) -> "GoogleEdgecontainerClusterNetworkingOutputReference":
        return typing.cast("GoogleEdgecontainerClusterNetworkingOutputReference", jsii.get(self, "networking"))

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
    ) -> "GoogleEdgecontainerClusterSystemAddonsConfigOutputReference":
        return typing.cast("GoogleEdgecontainerClusterSystemAddonsConfigOutputReference", jsii.get(self, "systemAddonsConfig"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleEdgecontainerClusterTimeoutsOutputReference":
        return typing.cast("GoogleEdgecontainerClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="authorizationInput")
    def authorization_input(
        self,
    ) -> typing.Optional["GoogleEdgecontainerClusterAuthorization"]:
        return typing.cast(typing.Optional["GoogleEdgecontainerClusterAuthorization"], jsii.get(self, "authorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneEncryptionInput")
    def control_plane_encryption_input(
        self,
    ) -> typing.Optional["GoogleEdgecontainerClusterControlPlaneEncryption"]:
        return typing.cast(typing.Optional["GoogleEdgecontainerClusterControlPlaneEncryption"], jsii.get(self, "controlPlaneEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneInput")
    def control_plane_input(
        self,
    ) -> typing.Optional["GoogleEdgecontainerClusterControlPlane"]:
        return typing.cast(typing.Optional["GoogleEdgecontainerClusterControlPlane"], jsii.get(self, "controlPlaneInput"))

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
    def fleet_input(self) -> typing.Optional["GoogleEdgecontainerClusterFleet"]:
        return typing.cast(typing.Optional["GoogleEdgecontainerClusterFleet"], jsii.get(self, "fleetInput"))

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
    ) -> typing.Optional["GoogleEdgecontainerClusterMaintenancePolicy"]:
        return typing.cast(typing.Optional["GoogleEdgecontainerClusterMaintenancePolicy"], jsii.get(self, "maintenancePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkingInput")
    def networking_input(
        self,
    ) -> typing.Optional["GoogleEdgecontainerClusterNetworking"]:
        return typing.cast(typing.Optional["GoogleEdgecontainerClusterNetworking"], jsii.get(self, "networkingInput"))

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
    ) -> typing.Optional["GoogleEdgecontainerClusterSystemAddonsConfig"]:
        return typing.cast(typing.Optional["GoogleEdgecontainerClusterSystemAddonsConfig"], jsii.get(self, "systemAddonsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="targetVersionInput")
    def target_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleEdgecontainerClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleEdgecontainerClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultMaxPodsPerNode")
    def default_max_pods_per_node(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultMaxPodsPerNode"))

    @default_max_pods_per_node.setter
    def default_max_pods_per_node(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e62a426e42f7efc17b42323d3fc2fc3b6819721e39b4b2c8d0c5557ca5eb5810)
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
            type_hints = typing.get_type_hints(_typecheckingstub__041b71046f4ef801aa2a9661c0f2bf553a6054fb832d67a9fad00446177de9d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalLoadBalancerIpv4AddressPools", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37e32469936715db08b0bd58a9426043f9d36958be806f9c2ef67ac54e464ac2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d9706fdfee54ded107a4448eed29a173a22812a872f1a5a1720dd21f8214447)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14cc96fd4453bfcb6e909e989544dd5cce69a9efb7199ad78612d792a0532e20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b1785233bfa0d36c3e38defed54b0854a35de7e9dedebb050ba679d688d4644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c17f8cf39f7c6d65ce5090fade2b6ddd8471d585efa6fde5ee3fdd1f9696863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="releaseChannel")
    def release_channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "releaseChannel"))

    @release_channel.setter
    def release_channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfb7e48d65c1568282755d8fd043575daf5887aa3db55d4d100f621213cb82c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "releaseChannel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetVersion")
    def target_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetVersion"))

    @target_version.setter
    def target_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c1a1481257bf3f3be7c6e0d6e580ddcadc4c2f88102d62a074186f7e31aa8ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetVersion", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterAuthorization",
    jsii_struct_bases=[],
    name_mapping={"admin_users": "adminUsers"},
)
class GoogleEdgecontainerClusterAuthorization:
    def __init__(
        self,
        *,
        admin_users: typing.Union["GoogleEdgecontainerClusterAuthorizationAdminUsers", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#admin_users GoogleEdgecontainerCluster#admin_users}
        '''
        if isinstance(admin_users, dict):
            admin_users = GoogleEdgecontainerClusterAuthorizationAdminUsers(**admin_users)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1c7f93a21bb62abaac6a3f3e4f7b9eaa0347247630ea99da288b309b731961e)
            check_type(argname="argument admin_users", value=admin_users, expected_type=type_hints["admin_users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_users": admin_users,
        }

    @builtins.property
    def admin_users(self) -> "GoogleEdgecontainerClusterAuthorizationAdminUsers":
        '''admin_users block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#admin_users GoogleEdgecontainerCluster#admin_users}
        '''
        result = self._values.get("admin_users")
        assert result is not None, "Required property 'admin_users' is missing"
        return typing.cast("GoogleEdgecontainerClusterAuthorizationAdminUsers", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEdgecontainerClusterAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterAuthorizationAdminUsers",
    jsii_struct_bases=[],
    name_mapping={"username": "username"},
)
class GoogleEdgecontainerClusterAuthorizationAdminUsers:
    def __init__(self, *, username: builtins.str) -> None:
        '''
        :param username: An active Google username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#username GoogleEdgecontainerCluster#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00e1eb3f0d365c762584ed1b173228599494f6bac22e7095f5aa74e957339a05)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
        }

    @builtins.property
    def username(self) -> builtins.str:
        '''An active Google username.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#username GoogleEdgecontainerCluster#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEdgecontainerClusterAuthorizationAdminUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEdgecontainerClusterAuthorizationAdminUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterAuthorizationAdminUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25be20ac08dd5ae00c22c6129e4f3b9aae71edf04ee224da6f5caf4d95119e12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f09d82025431c5603ae54387a2eb9e546636a2da55cc08228df81ccfb94d675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEdgecontainerClusterAuthorizationAdminUsers]:
        return typing.cast(typing.Optional[GoogleEdgecontainerClusterAuthorizationAdminUsers], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEdgecontainerClusterAuthorizationAdminUsers],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55462bf15fe4126b30280143ed110d10b81dbfdc7b84c3043e8c11c71134bb79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleEdgecontainerClusterAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38a9a2fe81d0f47abb437c10296c7e90e1c907a750c91605c3ee5c08f0cb9611)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdminUsers")
    def put_admin_users(self, *, username: builtins.str) -> None:
        '''
        :param username: An active Google username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#username GoogleEdgecontainerCluster#username}
        '''
        value = GoogleEdgecontainerClusterAuthorizationAdminUsers(username=username)

        return typing.cast(None, jsii.invoke(self, "putAdminUsers", [value]))

    @builtins.property
    @jsii.member(jsii_name="adminUsers")
    def admin_users(
        self,
    ) -> GoogleEdgecontainerClusterAuthorizationAdminUsersOutputReference:
        return typing.cast(GoogleEdgecontainerClusterAuthorizationAdminUsersOutputReference, jsii.get(self, "adminUsers"))

    @builtins.property
    @jsii.member(jsii_name="adminUsersInput")
    def admin_users_input(
        self,
    ) -> typing.Optional[GoogleEdgecontainerClusterAuthorizationAdminUsers]:
        return typing.cast(typing.Optional[GoogleEdgecontainerClusterAuthorizationAdminUsers], jsii.get(self, "adminUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEdgecontainerClusterAuthorization]:
        return typing.cast(typing.Optional[GoogleEdgecontainerClusterAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEdgecontainerClusterAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f5047eae177f197723a3d16c0b542ae9b7c89a0fe414dbabd547c2230871ce0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterConfig",
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
class GoogleEdgecontainerClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        authorization: typing.Union[GoogleEdgecontainerClusterAuthorization, typing.Dict[builtins.str, typing.Any]],
        fleet: typing.Union["GoogleEdgecontainerClusterFleet", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        networking: typing.Union["GoogleEdgecontainerClusterNetworking", typing.Dict[builtins.str, typing.Any]],
        control_plane: typing.Optional[typing.Union["GoogleEdgecontainerClusterControlPlane", typing.Dict[builtins.str, typing.Any]]] = None,
        control_plane_encryption: typing.Optional[typing.Union["GoogleEdgecontainerClusterControlPlaneEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
        default_max_pods_per_node: typing.Optional[jsii.Number] = None,
        external_load_balancer_ipv4_address_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        maintenance_policy: typing.Optional[typing.Union["GoogleEdgecontainerClusterMaintenancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        release_channel: typing.Optional[builtins.str] = None,
        system_addons_config: typing.Optional[typing.Union["GoogleEdgecontainerClusterSystemAddonsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        target_version: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleEdgecontainerClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#authorization GoogleEdgecontainerCluster#authorization}
        :param fleet: fleet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#fleet GoogleEdgecontainerCluster#fleet}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#location GoogleEdgecontainerCluster#location}
        :param name: The GDCE cluster name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#name GoogleEdgecontainerCluster#name}
        :param networking: networking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#networking GoogleEdgecontainerCluster#networking}
        :param control_plane: control_plane block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#control_plane GoogleEdgecontainerCluster#control_plane}
        :param control_plane_encryption: control_plane_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#control_plane_encryption GoogleEdgecontainerCluster#control_plane_encryption}
        :param default_max_pods_per_node: The default maximum number of pods per node used if a maximum value is not specified explicitly for a node pool in this cluster. If unspecified, the Kubernetes default value will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#default_max_pods_per_node GoogleEdgecontainerCluster#default_max_pods_per_node}
        :param external_load_balancer_ipv4_address_pools: Address pools for cluster data plane external load balancing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#external_load_balancer_ipv4_address_pools GoogleEdgecontainerCluster#external_load_balancer_ipv4_address_pools}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#id GoogleEdgecontainerCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for the edgecloud cluster. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#labels GoogleEdgecontainerCluster#labels}
        :param maintenance_policy: maintenance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#maintenance_policy GoogleEdgecontainerCluster#maintenance_policy}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#project GoogleEdgecontainerCluster#project}.
        :param release_channel: The release channel a cluster is subscribed to. Possible values: ["RELEASE_CHANNEL_UNSPECIFIED", "NONE", "REGULAR"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#release_channel GoogleEdgecontainerCluster#release_channel}
        :param system_addons_config: system_addons_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#system_addons_config GoogleEdgecontainerCluster#system_addons_config}
        :param target_version: The target cluster version. For example: "1.5.0". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#target_version GoogleEdgecontainerCluster#target_version}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#timeouts GoogleEdgecontainerCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(authorization, dict):
            authorization = GoogleEdgecontainerClusterAuthorization(**authorization)
        if isinstance(fleet, dict):
            fleet = GoogleEdgecontainerClusterFleet(**fleet)
        if isinstance(networking, dict):
            networking = GoogleEdgecontainerClusterNetworking(**networking)
        if isinstance(control_plane, dict):
            control_plane = GoogleEdgecontainerClusterControlPlane(**control_plane)
        if isinstance(control_plane_encryption, dict):
            control_plane_encryption = GoogleEdgecontainerClusterControlPlaneEncryption(**control_plane_encryption)
        if isinstance(maintenance_policy, dict):
            maintenance_policy = GoogleEdgecontainerClusterMaintenancePolicy(**maintenance_policy)
        if isinstance(system_addons_config, dict):
            system_addons_config = GoogleEdgecontainerClusterSystemAddonsConfig(**system_addons_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleEdgecontainerClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68ba66bdb12e944e8d3ea2e00e4f14f2a062fe21df8c08562315c02728946c47)
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
    def authorization(self) -> GoogleEdgecontainerClusterAuthorization:
        '''authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#authorization GoogleEdgecontainerCluster#authorization}
        '''
        result = self._values.get("authorization")
        assert result is not None, "Required property 'authorization' is missing"
        return typing.cast(GoogleEdgecontainerClusterAuthorization, result)

    @builtins.property
    def fleet(self) -> "GoogleEdgecontainerClusterFleet":
        '''fleet block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#fleet GoogleEdgecontainerCluster#fleet}
        '''
        result = self._values.get("fleet")
        assert result is not None, "Required property 'fleet' is missing"
        return typing.cast("GoogleEdgecontainerClusterFleet", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#location GoogleEdgecontainerCluster#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The GDCE cluster name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#name GoogleEdgecontainerCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def networking(self) -> "GoogleEdgecontainerClusterNetworking":
        '''networking block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#networking GoogleEdgecontainerCluster#networking}
        '''
        result = self._values.get("networking")
        assert result is not None, "Required property 'networking' is missing"
        return typing.cast("GoogleEdgecontainerClusterNetworking", result)

    @builtins.property
    def control_plane(
        self,
    ) -> typing.Optional["GoogleEdgecontainerClusterControlPlane"]:
        '''control_plane block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#control_plane GoogleEdgecontainerCluster#control_plane}
        '''
        result = self._values.get("control_plane")
        return typing.cast(typing.Optional["GoogleEdgecontainerClusterControlPlane"], result)

    @builtins.property
    def control_plane_encryption(
        self,
    ) -> typing.Optional["GoogleEdgecontainerClusterControlPlaneEncryption"]:
        '''control_plane_encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#control_plane_encryption GoogleEdgecontainerCluster#control_plane_encryption}
        '''
        result = self._values.get("control_plane_encryption")
        return typing.cast(typing.Optional["GoogleEdgecontainerClusterControlPlaneEncryption"], result)

    @builtins.property
    def default_max_pods_per_node(self) -> typing.Optional[jsii.Number]:
        '''The default maximum number of pods per node used if a maximum value is not specified explicitly for a node pool in this cluster.

        If unspecified, the
        Kubernetes default value will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#default_max_pods_per_node GoogleEdgecontainerCluster#default_max_pods_per_node}
        '''
        result = self._values.get("default_max_pods_per_node")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def external_load_balancer_ipv4_address_pools(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Address pools for cluster data plane external load balancing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#external_load_balancer_ipv4_address_pools GoogleEdgecontainerCluster#external_load_balancer_ipv4_address_pools}
        '''
        result = self._values.get("external_load_balancer_ipv4_address_pools")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#id GoogleEdgecontainerCluster#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#labels GoogleEdgecontainerCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def maintenance_policy(
        self,
    ) -> typing.Optional["GoogleEdgecontainerClusterMaintenancePolicy"]:
        '''maintenance_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#maintenance_policy GoogleEdgecontainerCluster#maintenance_policy}
        '''
        result = self._values.get("maintenance_policy")
        return typing.cast(typing.Optional["GoogleEdgecontainerClusterMaintenancePolicy"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#project GoogleEdgecontainerCluster#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_channel(self) -> typing.Optional[builtins.str]:
        '''The release channel a cluster is subscribed to. Possible values: ["RELEASE_CHANNEL_UNSPECIFIED", "NONE", "REGULAR"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#release_channel GoogleEdgecontainerCluster#release_channel}
        '''
        result = self._values.get("release_channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def system_addons_config(
        self,
    ) -> typing.Optional["GoogleEdgecontainerClusterSystemAddonsConfig"]:
        '''system_addons_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#system_addons_config GoogleEdgecontainerCluster#system_addons_config}
        '''
        result = self._values.get("system_addons_config")
        return typing.cast(typing.Optional["GoogleEdgecontainerClusterSystemAddonsConfig"], result)

    @builtins.property
    def target_version(self) -> typing.Optional[builtins.str]:
        '''The target cluster version. For example: "1.5.0".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#target_version GoogleEdgecontainerCluster#target_version}
        '''
        result = self._values.get("target_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleEdgecontainerClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#timeouts GoogleEdgecontainerCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleEdgecontainerClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEdgecontainerClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterControlPlane",
    jsii_struct_bases=[],
    name_mapping={"local": "local", "remote": "remote"},
)
class GoogleEdgecontainerClusterControlPlane:
    def __init__(
        self,
        *,
        local: typing.Optional[typing.Union["GoogleEdgecontainerClusterControlPlaneLocal", typing.Dict[builtins.str, typing.Any]]] = None,
        remote: typing.Optional[typing.Union["GoogleEdgecontainerClusterControlPlaneRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param local: local block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#local GoogleEdgecontainerCluster#local}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#remote GoogleEdgecontainerCluster#remote}
        '''
        if isinstance(local, dict):
            local = GoogleEdgecontainerClusterControlPlaneLocal(**local)
        if isinstance(remote, dict):
            remote = GoogleEdgecontainerClusterControlPlaneRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4737a6b8a58dadab7ba2a6a7541522de85e03c1141fd6e0488ee4042a7302456)
            check_type(argname="argument local", value=local, expected_type=type_hints["local"])
            check_type(argname="argument remote", value=remote, expected_type=type_hints["remote"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if local is not None:
            self._values["local"] = local
        if remote is not None:
            self._values["remote"] = remote

    @builtins.property
    def local(self) -> typing.Optional["GoogleEdgecontainerClusterControlPlaneLocal"]:
        '''local block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#local GoogleEdgecontainerCluster#local}
        '''
        result = self._values.get("local")
        return typing.cast(typing.Optional["GoogleEdgecontainerClusterControlPlaneLocal"], result)

    @builtins.property
    def remote(self) -> typing.Optional["GoogleEdgecontainerClusterControlPlaneRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#remote GoogleEdgecontainerCluster#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["GoogleEdgecontainerClusterControlPlaneRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEdgecontainerClusterControlPlane(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterControlPlaneEncryption",
    jsii_struct_bases=[],
    name_mapping={"kms_key": "kmsKey"},
)
class GoogleEdgecontainerClusterControlPlaneEncryption:
    def __init__(self, *, kms_key: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key: The Cloud KMS CryptoKey e.g. projects/{project}/locations/{location}/keyRings/{keyRing}/cryptoKeys/{cryptoKey} to use for protecting control plane disks. If not specified, a Google-managed key will be used instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#kms_key GoogleEdgecontainerCluster#kms_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e74351579b6def8329495bed21ee1c9a79a9c189c68c1e148a3dc8c2bcfc40cc)
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The Cloud KMS CryptoKey e.g. projects/{project}/locations/{location}/keyRings/{keyRing}/cryptoKeys/{cryptoKey} to use for protecting control plane disks. If not specified, a Google-managed key will be used instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#kms_key GoogleEdgecontainerCluster#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEdgecontainerClusterControlPlaneEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterControlPlaneEncryptionKmsStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleEdgecontainerClusterControlPlaneEncryptionKmsStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEdgecontainerClusterControlPlaneEncryptionKmsStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEdgecontainerClusterControlPlaneEncryptionKmsStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterControlPlaneEncryptionKmsStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea99f78c6ebb4213d26eaea30a87cb314255e7c4397a5cb7c375452e1ae53e0f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleEdgecontainerClusterControlPlaneEncryptionKmsStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ae19ac72a8837c3ee22970b1320af603de7aac87c595c220ea1e37f6db25760)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleEdgecontainerClusterControlPlaneEncryptionKmsStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e0a88a1a6c723fa55b5aea261e33e44a8a8c345fda845c0e93a7531bb6752f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c99eaa4af7462518a9a937bd27b7a49dbf66bdf01286fabedf59bbe597645d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__56c48c0d772ee53a902fec8873d97dcac1d898045840b3fd1b7dd4b21e1c7593)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleEdgecontainerClusterControlPlaneEncryptionKmsStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterControlPlaneEncryptionKmsStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bda3cea106ae47fb3fc0ca16835d76a3ce63fc3e5a5305d2a0300a12ad3e44b)
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
    ) -> typing.Optional[GoogleEdgecontainerClusterControlPlaneEncryptionKmsStatus]:
        return typing.cast(typing.Optional[GoogleEdgecontainerClusterControlPlaneEncryptionKmsStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEdgecontainerClusterControlPlaneEncryptionKmsStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b4b4b0e26643e592a7e94e20953d7e9c1b269bc473426b821de51028149fa46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleEdgecontainerClusterControlPlaneEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterControlPlaneEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__484b84415347b1d04427b390ae9cfd8ee75d8b80fa1e534843b69a3f19f718f5)
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
    def kms_status(
        self,
    ) -> GoogleEdgecontainerClusterControlPlaneEncryptionKmsStatusList:
        return typing.cast(GoogleEdgecontainerClusterControlPlaneEncryptionKmsStatusList, jsii.get(self, "kmsStatus"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__52ad2a82bb11d9db4a3c7c6ac227cea90fc0768df64092404436cd9f5ecf35e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEdgecontainerClusterControlPlaneEncryption]:
        return typing.cast(typing.Optional[GoogleEdgecontainerClusterControlPlaneEncryption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEdgecontainerClusterControlPlaneEncryption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b7041c94caa0f587847ba46b994721228903cf21174d981dbc01f6a88a267ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterControlPlaneLocal",
    jsii_struct_bases=[],
    name_mapping={
        "machine_filter": "machineFilter",
        "node_count": "nodeCount",
        "node_location": "nodeLocation",
        "shared_deployment_policy": "sharedDeploymentPolicy",
    },
)
class GoogleEdgecontainerClusterControlPlaneLocal:
    def __init__(
        self,
        *,
        machine_filter: typing.Optional[builtins.str] = None,
        node_count: typing.Optional[jsii.Number] = None,
        node_location: typing.Optional[builtins.str] = None,
        shared_deployment_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param machine_filter: Only machines matching this filter will be allowed to host control plane nodes. The filtering language accepts strings like "name=", and is documented here: `AIP-160 <https://google.aip.dev/160>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#machine_filter GoogleEdgecontainerCluster#machine_filter}
        :param node_count: The number of nodes to serve as replicas of the Control Plane. Only 1 and 3 are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#node_count GoogleEdgecontainerCluster#node_count}
        :param node_location: Name of the Google Distributed Cloud Edge zones where this node pool will be created. For example: 'us-central1-edge-customer-a'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#node_location GoogleEdgecontainerCluster#node_location}
        :param shared_deployment_policy: Policy configuration about how user applications are deployed. Possible values: ["SHARED_DEPLOYMENT_POLICY_UNSPECIFIED", "ALLOWED", "DISALLOWED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#shared_deployment_policy GoogleEdgecontainerCluster#shared_deployment_policy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5ffa8a1335c833dd8c046e20886f266429633f025abc2d6a16498858199d840)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#machine_filter GoogleEdgecontainerCluster#machine_filter}
        '''
        result = self._values.get("machine_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_count(self) -> typing.Optional[jsii.Number]:
        '''The number of nodes to serve as replicas of the Control Plane. Only 1 and 3 are supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#node_count GoogleEdgecontainerCluster#node_count}
        '''
        result = self._values.get("node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def node_location(self) -> typing.Optional[builtins.str]:
        '''Name of the Google Distributed Cloud Edge zones where this node pool will be created. For example: 'us-central1-edge-customer-a'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#node_location GoogleEdgecontainerCluster#node_location}
        '''
        result = self._values.get("node_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shared_deployment_policy(self) -> typing.Optional[builtins.str]:
        '''Policy configuration about how user applications are deployed. Possible values: ["SHARED_DEPLOYMENT_POLICY_UNSPECIFIED", "ALLOWED", "DISALLOWED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#shared_deployment_policy GoogleEdgecontainerCluster#shared_deployment_policy}
        '''
        result = self._values.get("shared_deployment_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEdgecontainerClusterControlPlaneLocal(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEdgecontainerClusterControlPlaneLocalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterControlPlaneLocalOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5f90226474c504d17d7103920cd0af294d8984fde8a29b94917df87aad1ae84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d41611451db3642cf366a7ea01fb97907a22999df83c2e5fdcccb70a20b88ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b9630b8acee0532a1b5813934751ac7aaf1e02ea4157d9d41a6ce51e5fd68ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeLocation")
    def node_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeLocation"))

    @node_location.setter
    def node_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40a0effc8413c7811129d7458e0206bf223c325f0ba8a22f54fada638aff99ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sharedDeploymentPolicy")
    def shared_deployment_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sharedDeploymentPolicy"))

    @shared_deployment_policy.setter
    def shared_deployment_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eba3e04ba87e717c28c5fd63394838656f3d5a8b9a69c6d08abbd1a38e4b0930)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedDeploymentPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEdgecontainerClusterControlPlaneLocal]:
        return typing.cast(typing.Optional[GoogleEdgecontainerClusterControlPlaneLocal], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEdgecontainerClusterControlPlaneLocal],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39b38f8de2bfd592f22f0a564b596f735099d5b68835a4018d6370e847e110b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleEdgecontainerClusterControlPlaneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterControlPlaneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f3b7edd99ae12bfa65e78127abffbccf801cb1cc468bc5e25f8ba002d41e153)
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
        :param machine_filter: Only machines matching this filter will be allowed to host control plane nodes. The filtering language accepts strings like "name=", and is documented here: `AIP-160 <https://google.aip.dev/160>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#machine_filter GoogleEdgecontainerCluster#machine_filter}
        :param node_count: The number of nodes to serve as replicas of the Control Plane. Only 1 and 3 are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#node_count GoogleEdgecontainerCluster#node_count}
        :param node_location: Name of the Google Distributed Cloud Edge zones where this node pool will be created. For example: 'us-central1-edge-customer-a'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#node_location GoogleEdgecontainerCluster#node_location}
        :param shared_deployment_policy: Policy configuration about how user applications are deployed. Possible values: ["SHARED_DEPLOYMENT_POLICY_UNSPECIFIED", "ALLOWED", "DISALLOWED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#shared_deployment_policy GoogleEdgecontainerCluster#shared_deployment_policy}
        '''
        value = GoogleEdgecontainerClusterControlPlaneLocal(
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
        :param node_location: Name of the Google Distributed Cloud Edge zones where this node pool will be created. For example: 'us-central1-edge-customer-a'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#node_location GoogleEdgecontainerCluster#node_location}
        '''
        value = GoogleEdgecontainerClusterControlPlaneRemote(
            node_location=node_location
        )

        return typing.cast(None, jsii.invoke(self, "putRemote", [value]))

    @jsii.member(jsii_name="resetLocal")
    def reset_local(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocal", []))

    @jsii.member(jsii_name="resetRemote")
    def reset_remote(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemote", []))

    @builtins.property
    @jsii.member(jsii_name="local")
    def local(self) -> GoogleEdgecontainerClusterControlPlaneLocalOutputReference:
        return typing.cast(GoogleEdgecontainerClusterControlPlaneLocalOutputReference, jsii.get(self, "local"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(self) -> "GoogleEdgecontainerClusterControlPlaneRemoteOutputReference":
        return typing.cast("GoogleEdgecontainerClusterControlPlaneRemoteOutputReference", jsii.get(self, "remote"))

    @builtins.property
    @jsii.member(jsii_name="localInput")
    def local_input(
        self,
    ) -> typing.Optional[GoogleEdgecontainerClusterControlPlaneLocal]:
        return typing.cast(typing.Optional[GoogleEdgecontainerClusterControlPlaneLocal], jsii.get(self, "localInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["GoogleEdgecontainerClusterControlPlaneRemote"]:
        return typing.cast(typing.Optional["GoogleEdgecontainerClusterControlPlaneRemote"], jsii.get(self, "remoteInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleEdgecontainerClusterControlPlane]:
        return typing.cast(typing.Optional[GoogleEdgecontainerClusterControlPlane], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEdgecontainerClusterControlPlane],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__583cdebad68eb685639fdccccea2d5cc5de2da2ffce883778cabb2fbfbb76be5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterControlPlaneRemote",
    jsii_struct_bases=[],
    name_mapping={"node_location": "nodeLocation"},
)
class GoogleEdgecontainerClusterControlPlaneRemote:
    def __init__(self, *, node_location: typing.Optional[builtins.str] = None) -> None:
        '''
        :param node_location: Name of the Google Distributed Cloud Edge zones where this node pool will be created. For example: 'us-central1-edge-customer-a'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#node_location GoogleEdgecontainerCluster#node_location}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f79b2444adf5bfb6c9e0e4e4ee754579d5a995822c8ec9d2a05dd7d59a785882)
            check_type(argname="argument node_location", value=node_location, expected_type=type_hints["node_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if node_location is not None:
            self._values["node_location"] = node_location

    @builtins.property
    def node_location(self) -> typing.Optional[builtins.str]:
        '''Name of the Google Distributed Cloud Edge zones where this node pool will be created. For example: 'us-central1-edge-customer-a'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#node_location GoogleEdgecontainerCluster#node_location}
        '''
        result = self._values.get("node_location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEdgecontainerClusterControlPlaneRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEdgecontainerClusterControlPlaneRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterControlPlaneRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35ea78b2f3b4900680bb51a3eaab35827de35219bc08194569cfb6678b09fabb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad5a5684dbe683afc02c2a4dc150bf240ef086b4785e13f3ffb7d62fab2c4699)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEdgecontainerClusterControlPlaneRemote]:
        return typing.cast(typing.Optional[GoogleEdgecontainerClusterControlPlaneRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEdgecontainerClusterControlPlaneRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61c54ddd068029dd63bac9fd8893887fddb6ae92a500175026b48575851355e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterFleet",
    jsii_struct_bases=[],
    name_mapping={"project": "project"},
)
class GoogleEdgecontainerClusterFleet:
    def __init__(self, *, project: builtins.str) -> None:
        '''
        :param project: The name of the Fleet host project where this cluster will be registered. Project names are formatted as 'projects/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#project GoogleEdgecontainerCluster#project}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fbedfca4e5572c2aa1df94877cbd277ab3108e74a4cbba9b7dcc41edbe166a2)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project": project,
        }

    @builtins.property
    def project(self) -> builtins.str:
        '''The name of the Fleet host project where this cluster will be registered. Project names are formatted as 'projects/'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#project GoogleEdgecontainerCluster#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEdgecontainerClusterFleet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEdgecontainerClusterFleetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterFleetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e6f511e7b694311e09aae744012303c6e8940588e0182b5509584525ed7aa19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44aeb99c04fde45246fd512f89b76820b04c901e9e08dc278df2cb69712a46e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleEdgecontainerClusterFleet]:
        return typing.cast(typing.Optional[GoogleEdgecontainerClusterFleet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEdgecontainerClusterFleet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417059a1e1da756699886b77aa60dafff0b4762fea7c4bec974ccd32edeecbe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterMaintenanceEvents",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleEdgecontainerClusterMaintenanceEvents:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEdgecontainerClusterMaintenanceEvents(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEdgecontainerClusterMaintenanceEventsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterMaintenanceEventsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35d21e9044507a1f02b57083148261bec2c5b6ef8320600f36a3cabb488397f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleEdgecontainerClusterMaintenanceEventsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f2d583617ba12a6f3033553f1d7771ea8d2a90d1499e5d551b9b2b2a43179ba)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleEdgecontainerClusterMaintenanceEventsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbc9f0651d1be79b0b4ced3be8005b9e5808be761945abc80aaba437e657206e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a20396c091e79db2ae55b6ea2f4473f70424943af787dde218399da97819a6d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2b3c685cbe749ca606a654121c77110d52343d854eaaee4fcd2f567695d8b5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleEdgecontainerClusterMaintenanceEventsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterMaintenanceEventsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b85337692f8056a1af628ffb6e4e72cd0fbbed06212083a40715fc2f46ba3972)
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
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEdgecontainerClusterMaintenanceEvents]:
        return typing.cast(typing.Optional[GoogleEdgecontainerClusterMaintenanceEvents], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEdgecontainerClusterMaintenanceEvents],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13e1668e9719d2f6519d01777c3f460f3825e1ca7c52e9a02fad360a161cbb7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterMaintenancePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "window": "window",
        "maintenance_exclusions": "maintenanceExclusions",
    },
)
class GoogleEdgecontainerClusterMaintenancePolicy:
    def __init__(
        self,
        *,
        window: typing.Union["GoogleEdgecontainerClusterMaintenancePolicyWindow", typing.Dict[builtins.str, typing.Any]],
        maintenance_exclusions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusions", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param window: window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#window GoogleEdgecontainerCluster#window}
        :param maintenance_exclusions: maintenance_exclusions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#maintenance_exclusions GoogleEdgecontainerCluster#maintenance_exclusions}
        '''
        if isinstance(window, dict):
            window = GoogleEdgecontainerClusterMaintenancePolicyWindow(**window)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cdaf111bcf9729292645c2ad7b86f0066abe002053535ea2337d5fccea0618f)
            check_type(argname="argument window", value=window, expected_type=type_hints["window"])
            check_type(argname="argument maintenance_exclusions", value=maintenance_exclusions, expected_type=type_hints["maintenance_exclusions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "window": window,
        }
        if maintenance_exclusions is not None:
            self._values["maintenance_exclusions"] = maintenance_exclusions

    @builtins.property
    def window(self) -> "GoogleEdgecontainerClusterMaintenancePolicyWindow":
        '''window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#window GoogleEdgecontainerCluster#window}
        '''
        result = self._values.get("window")
        assert result is not None, "Required property 'window' is missing"
        return typing.cast("GoogleEdgecontainerClusterMaintenancePolicyWindow", result)

    @builtins.property
    def maintenance_exclusions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusions"]]]:
        '''maintenance_exclusions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#maintenance_exclusions GoogleEdgecontainerCluster#maintenance_exclusions}
        '''
        result = self._values.get("maintenance_exclusions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusions"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEdgecontainerClusterMaintenancePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusions",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "window": "window"},
)
class GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusions:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        window: typing.Optional[typing.Union["GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: A unique (per cluster) id for the window. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#id GoogleEdgecontainerCluster#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param window: window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#window GoogleEdgecontainerCluster#window}
        '''
        if isinstance(window, dict):
            window = GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow(**window)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__211fd0e5d4b89de369e4cfc0b56a0f6796d2637526bab298f64fa4a9a44cb444)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#id GoogleEdgecontainerCluster#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def window(
        self,
    ) -> typing.Optional["GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow"]:
        '''window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#window GoogleEdgecontainerCluster#window}
        '''
        result = self._values.get("window")
        return typing.cast(typing.Optional["GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04d9f8eddd43cbd83d205b625b162980220b9fca52200fe0e93447cd1698bdf8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e663a334fcfe88f2007e83ef5f560b531834db3a238febbf35c06171527068c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e75b5e8bbe5b32e6543bd5b58688f0836547f1da3d69acc41c285c581c6b7a98)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc0e5ab4785840d7804cea8dfb7ff7c3be5ba2b5b452c8e406b6e565fe6a7c7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd41f7127fb8c62a36a3771c8b27ba15333c344e6c39a3f872c3b6920eb83321)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__903a9daf74cf428389e255eb8a5189e8a4e9e72a1e699ac890cd1889476595d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__255bda1b18f310b2eb1d22423de669022cbea2263293f4548585b4ca00714483)
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
        :param end_time: The time that the window ends. The end time must take place after the start time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#end_time GoogleEdgecontainerCluster#end_time}
        :param start_time: The time that the window first starts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#start_time GoogleEdgecontainerCluster#start_time}
        '''
        value = GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow(
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
    ) -> "GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindowOutputReference":
        return typing.cast("GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindowOutputReference", jsii.get(self, "window"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="windowInput")
    def window_input(
        self,
    ) -> typing.Optional["GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow"]:
        return typing.cast(typing.Optional["GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow"], jsii.get(self, "windowInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c3b851c60ac3595716ba708468fc2c8eac370ecf39c0b183e1d64ff1e5d677c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feba6e457f0698aa2d2d8b8b142f5bf818b95961b52045ac038579169aaf0196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow",
    jsii_struct_bases=[],
    name_mapping={"end_time": "endTime", "start_time": "startTime"},
)
class GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow:
    def __init__(
        self,
        *,
        end_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param end_time: The time that the window ends. The end time must take place after the start time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#end_time GoogleEdgecontainerCluster#end_time}
        :param start_time: The time that the window first starts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#start_time GoogleEdgecontainerCluster#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aaea1fc6f5e0a61076ef17a123e691c50ca963d86f7ebf734d40f04d7324d2b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#end_time GoogleEdgecontainerCluster#end_time}
        '''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''The time that the window first starts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#start_time GoogleEdgecontainerCluster#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e1e24b7e1b595ca67e2b083ba7fb97633183483bf54dd518ad03256ae6f4856)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc6a17356895595af4f4a3472097c220207b8f9c73d8b80433c936533963c432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__883dc02112d8f1514cf7d1e013a64b48928077d3ab969be6d764f4d1a5b7225b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow]:
        return typing.cast(typing.Optional[GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6f1d69fe1167768698ff0bfe18818d9fe9f53edfa8cc62d385acfa48b26d51a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleEdgecontainerClusterMaintenancePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterMaintenancePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac2d63442798d2a9eeeb3b9d3b186497e42f1e81f410160d15d31242c3718f3d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMaintenanceExclusions")
    def put_maintenance_exclusions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39e53b161ea57de6bf9b036c9421633cf10c67ff03254115db5a66406e990bd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMaintenanceExclusions", [value]))

    @jsii.member(jsii_name="putWindow")
    def put_window(
        self,
        *,
        recurring_window: typing.Union["GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindow", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param recurring_window: recurring_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#recurring_window GoogleEdgecontainerCluster#recurring_window}
        '''
        value = GoogleEdgecontainerClusterMaintenancePolicyWindow(
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
    ) -> GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsList:
        return typing.cast(GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsList, jsii.get(self, "maintenanceExclusions"))

    @builtins.property
    @jsii.member(jsii_name="window")
    def window(
        self,
    ) -> "GoogleEdgecontainerClusterMaintenancePolicyWindowOutputReference":
        return typing.cast("GoogleEdgecontainerClusterMaintenancePolicyWindowOutputReference", jsii.get(self, "window"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceExclusionsInput")
    def maintenance_exclusions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusions]]], jsii.get(self, "maintenanceExclusionsInput"))

    @builtins.property
    @jsii.member(jsii_name="windowInput")
    def window_input(
        self,
    ) -> typing.Optional["GoogleEdgecontainerClusterMaintenancePolicyWindow"]:
        return typing.cast(typing.Optional["GoogleEdgecontainerClusterMaintenancePolicyWindow"], jsii.get(self, "windowInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEdgecontainerClusterMaintenancePolicy]:
        return typing.cast(typing.Optional[GoogleEdgecontainerClusterMaintenancePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEdgecontainerClusterMaintenancePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d30150c7ac1bb3a7418f4e5aa768049d71bf4255ecc7bcbaeb259566ecd8c2e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterMaintenancePolicyWindow",
    jsii_struct_bases=[],
    name_mapping={"recurring_window": "recurringWindow"},
)
class GoogleEdgecontainerClusterMaintenancePolicyWindow:
    def __init__(
        self,
        *,
        recurring_window: typing.Union["GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindow", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param recurring_window: recurring_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#recurring_window GoogleEdgecontainerCluster#recurring_window}
        '''
        if isinstance(recurring_window, dict):
            recurring_window = GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindow(**recurring_window)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46837c12c1bccbf05be933e1dac3d57e64af1674e254a0010f30dfb59a15b4a9)
            check_type(argname="argument recurring_window", value=recurring_window, expected_type=type_hints["recurring_window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "recurring_window": recurring_window,
        }

    @builtins.property
    def recurring_window(
        self,
    ) -> "GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindow":
        '''recurring_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#recurring_window GoogleEdgecontainerCluster#recurring_window}
        '''
        result = self._values.get("recurring_window")
        assert result is not None, "Required property 'recurring_window' is missing"
        return typing.cast("GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindow", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEdgecontainerClusterMaintenancePolicyWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEdgecontainerClusterMaintenancePolicyWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterMaintenancePolicyWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__333bd12de730ca9188c9e2c94960c57dca068d9904ce98c1035b4bc167e7361d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRecurringWindow")
    def put_recurring_window(
        self,
        *,
        recurrence: typing.Optional[builtins.str] = None,
        window: typing.Optional[typing.Union["GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param recurrence: An RRULE (https://tools.ietf.org/html/rfc5545#section-3.8.5.3) for how this window recurs. They go on for the span of time between the start and end time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#recurrence GoogleEdgecontainerCluster#recurrence}
        :param window: window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#window GoogleEdgecontainerCluster#window}
        '''
        value = GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindow(
            recurrence=recurrence, window=window
        )

        return typing.cast(None, jsii.invoke(self, "putRecurringWindow", [value]))

    @builtins.property
    @jsii.member(jsii_name="recurringWindow")
    def recurring_window(
        self,
    ) -> "GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowOutputReference":
        return typing.cast("GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowOutputReference", jsii.get(self, "recurringWindow"))

    @builtins.property
    @jsii.member(jsii_name="recurringWindowInput")
    def recurring_window_input(
        self,
    ) -> typing.Optional["GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindow"]:
        return typing.cast(typing.Optional["GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindow"], jsii.get(self, "recurringWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEdgecontainerClusterMaintenancePolicyWindow]:
        return typing.cast(typing.Optional[GoogleEdgecontainerClusterMaintenancePolicyWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEdgecontainerClusterMaintenancePolicyWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57c331a984d631f7e087b203a42918d2d65c61556070331ea7c332d648d45047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindow",
    jsii_struct_bases=[],
    name_mapping={"recurrence": "recurrence", "window": "window"},
)
class GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindow:
    def __init__(
        self,
        *,
        recurrence: typing.Optional[builtins.str] = None,
        window: typing.Optional[typing.Union["GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param recurrence: An RRULE (https://tools.ietf.org/html/rfc5545#section-3.8.5.3) for how this window recurs. They go on for the span of time between the start and end time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#recurrence GoogleEdgecontainerCluster#recurrence}
        :param window: window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#window GoogleEdgecontainerCluster#window}
        '''
        if isinstance(window, dict):
            window = GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow(**window)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e545a44b38d1bb410d3d43743d9aa8f00516bb8e336dc9696e0dba243a23825)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#recurrence GoogleEdgecontainerCluster#recurrence}
        '''
        result = self._values.get("recurrence")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def window(
        self,
    ) -> typing.Optional["GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow"]:
        '''window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#window GoogleEdgecontainerCluster#window}
        '''
        result = self._values.get("window")
        return typing.cast(typing.Optional["GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff56cbfd6fdd263ee4360bd60f118dcff488da570ce1279e6282f25bebf76d65)
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
        :param end_time: The time that the window ends. The end time must take place after the start time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#end_time GoogleEdgecontainerCluster#end_time}
        :param start_time: The time that the window first starts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#start_time GoogleEdgecontainerCluster#start_time}
        '''
        value = GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow(
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
    ) -> "GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindowOutputReference":
        return typing.cast("GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindowOutputReference", jsii.get(self, "window"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceInput")
    def recurrence_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recurrenceInput"))

    @builtins.property
    @jsii.member(jsii_name="windowInput")
    def window_input(
        self,
    ) -> typing.Optional["GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow"]:
        return typing.cast(typing.Optional["GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow"], jsii.get(self, "windowInput"))

    @builtins.property
    @jsii.member(jsii_name="recurrence")
    def recurrence(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recurrence"))

    @recurrence.setter
    def recurrence(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c387e7ac512008951def0314ad6ca5fe39233f5b390c21ac59f02effd02315d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recurrence", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindow]:
        return typing.cast(typing.Optional[GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e54854081b28f8f3cf365fc1c26f57392f9db6d7b8bd80d32a3f9263988f3704)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow",
    jsii_struct_bases=[],
    name_mapping={"end_time": "endTime", "start_time": "startTime"},
)
class GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow:
    def __init__(
        self,
        *,
        end_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param end_time: The time that the window ends. The end time must take place after the start time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#end_time GoogleEdgecontainerCluster#end_time}
        :param start_time: The time that the window first starts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#start_time GoogleEdgecontainerCluster#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ba80854534eefb374a6e0f4fadb9b8a349448a8b1b98797c2fffa1961675bfb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#end_time GoogleEdgecontainerCluster#end_time}
        '''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''The time that the window first starts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#start_time GoogleEdgecontainerCluster#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02615d96371c4b0370babf36c4762b79bee2b92521dc117e589434eb4e17530f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab866fd23d9a225a9b331aa75e8f8a3e37a7ee1ba13c15962d07524868cd4bc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7051989bd4a45cd18976282dde2b41f0ea7f43a065612498126cacabe6da381d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow]:
        return typing.cast(typing.Optional[GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da14a886d2cf9cbd9076c8db6a4eb18a38b97017932f95d2101a366d74ca63d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterNetworking",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_ipv4_cidr_blocks": "clusterIpv4CidrBlocks",
        "services_ipv4_cidr_blocks": "servicesIpv4CidrBlocks",
        "cluster_ipv6_cidr_blocks": "clusterIpv6CidrBlocks",
        "services_ipv6_cidr_blocks": "servicesIpv6CidrBlocks",
    },
)
class GoogleEdgecontainerClusterNetworking:
    def __init__(
        self,
        *,
        cluster_ipv4_cidr_blocks: typing.Sequence[builtins.str],
        services_ipv4_cidr_blocks: typing.Sequence[builtins.str],
        cluster_ipv6_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        services_ipv6_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cluster_ipv4_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these blocks. Only a single block is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#cluster_ipv4_cidr_blocks GoogleEdgecontainerCluster#cluster_ipv4_cidr_blocks}
        :param services_ipv4_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these blocks. Only a single block is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#services_ipv4_cidr_blocks GoogleEdgecontainerCluster#services_ipv4_cidr_blocks}
        :param cluster_ipv6_cidr_blocks: If specified, dual stack mode is enabled and all pods in the cluster are assigned an IPv6 address from these blocks alongside from an IPv4 address. Only a single block is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#cluster_ipv6_cidr_blocks GoogleEdgecontainerCluster#cluster_ipv6_cidr_blocks}
        :param services_ipv6_cidr_blocks: If specified, dual stack mode is enabled and all services in the cluster are assigned an IPv6 address from these blocks alongside from an IPv4 address. Only a single block is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#services_ipv6_cidr_blocks GoogleEdgecontainerCluster#services_ipv6_cidr_blocks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__097d3b738c01e336800715e24cd3e0116e0ec625d4f691216d917e8a59bd053a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#cluster_ipv4_cidr_blocks GoogleEdgecontainerCluster#cluster_ipv4_cidr_blocks}
        '''
        result = self._values.get("cluster_ipv4_cidr_blocks")
        assert result is not None, "Required property 'cluster_ipv4_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def services_ipv4_cidr_blocks(self) -> typing.List[builtins.str]:
        '''All services in the cluster are assigned an RFC1918 IPv4 address from these blocks.

        Only a single block is supported. This field cannot be changed
        after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#services_ipv4_cidr_blocks GoogleEdgecontainerCluster#services_ipv4_cidr_blocks}
        '''
        result = self._values.get("services_ipv4_cidr_blocks")
        assert result is not None, "Required property 'services_ipv4_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cluster_ipv6_cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If specified, dual stack mode is enabled and all pods in the cluster are assigned an IPv6 address from these blocks alongside from an IPv4 address.

        Only a single block is supported. This field cannot be changed
        after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#cluster_ipv6_cidr_blocks GoogleEdgecontainerCluster#cluster_ipv6_cidr_blocks}
        '''
        result = self._values.get("cluster_ipv6_cidr_blocks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def services_ipv6_cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If specified, dual stack mode is enabled and all services in the cluster are assigned an IPv6 address from these blocks alongside from an IPv4 address.

        Only a single block is supported. This field cannot be changed
        after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#services_ipv6_cidr_blocks GoogleEdgecontainerCluster#services_ipv6_cidr_blocks}
        '''
        result = self._values.get("services_ipv6_cidr_blocks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEdgecontainerClusterNetworking(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEdgecontainerClusterNetworkingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterNetworkingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbcfae32fcd3f8211cdc832ca8ac5f42ea673970d0c791f85630f296d41a30da)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91cfc7b64dfd779e89f96e06d62436a90f216fe7dfb974b35c6cd2f6728be4fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterIpv4CidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterIpv6CidrBlocks")
    def cluster_ipv6_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "clusterIpv6CidrBlocks"))

    @cluster_ipv6_cidr_blocks.setter
    def cluster_ipv6_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__694817f3a3d1866659421f7afc8420d4f7670ec35f38ada8b16b70b2eedf8a37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterIpv6CidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servicesIpv4CidrBlocks")
    def services_ipv4_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "servicesIpv4CidrBlocks"))

    @services_ipv4_cidr_blocks.setter
    def services_ipv4_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1d80bda9fdcbfe8fa26a679b25268d641cb4de15a95d120543fedc081f42e2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servicesIpv4CidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servicesIpv6CidrBlocks")
    def services_ipv6_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "servicesIpv6CidrBlocks"))

    @services_ipv6_cidr_blocks.setter
    def services_ipv6_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc482d9ddcee95bd8c75e237bed7be1a9fcff6eb39356f183f071e7880ad0127)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servicesIpv6CidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleEdgecontainerClusterNetworking]:
        return typing.cast(typing.Optional[GoogleEdgecontainerClusterNetworking], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEdgecontainerClusterNetworking],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ab7ae354ab873a5f63b86e75c7216ca11c4fc1ab1d32b31e3580c902d023470)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterSystemAddonsConfig",
    jsii_struct_bases=[],
    name_mapping={"ingress": "ingress"},
)
class GoogleEdgecontainerClusterSystemAddonsConfig:
    def __init__(
        self,
        *,
        ingress: typing.Optional[typing.Union["GoogleEdgecontainerClusterSystemAddonsConfigIngress", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ingress: ingress block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#ingress GoogleEdgecontainerCluster#ingress}
        '''
        if isinstance(ingress, dict):
            ingress = GoogleEdgecontainerClusterSystemAddonsConfigIngress(**ingress)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e74a0f794f24acb10577bb777761d5dfe31895403ecff5b5c1627ef931f8cda)
            check_type(argname="argument ingress", value=ingress, expected_type=type_hints["ingress"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ingress is not None:
            self._values["ingress"] = ingress

    @builtins.property
    def ingress(
        self,
    ) -> typing.Optional["GoogleEdgecontainerClusterSystemAddonsConfigIngress"]:
        '''ingress block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#ingress GoogleEdgecontainerCluster#ingress}
        '''
        result = self._values.get("ingress")
        return typing.cast(typing.Optional["GoogleEdgecontainerClusterSystemAddonsConfigIngress"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEdgecontainerClusterSystemAddonsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterSystemAddonsConfigIngress",
    jsii_struct_bases=[],
    name_mapping={"disabled": "disabled", "ipv4_vip": "ipv4Vip"},
)
class GoogleEdgecontainerClusterSystemAddonsConfigIngress:
    def __init__(
        self,
        *,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ipv4_vip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disabled: Whether Ingress is disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#disabled GoogleEdgecontainerCluster#disabled}
        :param ipv4_vip: Ingress VIP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#ipv4_vip GoogleEdgecontainerCluster#ipv4_vip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7c9204e4ffbc9951df916a6e76e029462f0cb306f8cae689d281a5a53eadfbd)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#disabled GoogleEdgecontainerCluster#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ipv4_vip(self) -> typing.Optional[builtins.str]:
        '''Ingress VIP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#ipv4_vip GoogleEdgecontainerCluster#ipv4_vip}
        '''
        result = self._values.get("ipv4_vip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEdgecontainerClusterSystemAddonsConfigIngress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEdgecontainerClusterSystemAddonsConfigIngressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterSystemAddonsConfigIngressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__237b01ec115efaa9be78b746e161cda1d7e558a54e5a82c2a1c1078e3bd9e32e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b6ceca0130d6c96040016e2105922789e11b08b59b0e843ef901537d8c483c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv4Vip")
    def ipv4_vip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv4Vip"))

    @ipv4_vip.setter
    def ipv4_vip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__767d07dac9192efeaa186122e990bfbc334993da3356660658604152cc4a8b2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv4Vip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEdgecontainerClusterSystemAddonsConfigIngress]:
        return typing.cast(typing.Optional[GoogleEdgecontainerClusterSystemAddonsConfigIngress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEdgecontainerClusterSystemAddonsConfigIngress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f6511c3aa9289ac43c684ce91e4c16286ea3cdeea8fe763921492673fd27b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleEdgecontainerClusterSystemAddonsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterSystemAddonsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1177c2e4263dbe7e81d91904a083bea2544b291efb86420d5042f77ca1511edb)
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
        :param disabled: Whether Ingress is disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#disabled GoogleEdgecontainerCluster#disabled}
        :param ipv4_vip: Ingress VIP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#ipv4_vip GoogleEdgecontainerCluster#ipv4_vip}
        '''
        value = GoogleEdgecontainerClusterSystemAddonsConfigIngress(
            disabled=disabled, ipv4_vip=ipv4_vip
        )

        return typing.cast(None, jsii.invoke(self, "putIngress", [value]))

    @jsii.member(jsii_name="resetIngress")
    def reset_ingress(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngress", []))

    @builtins.property
    @jsii.member(jsii_name="ingress")
    def ingress(
        self,
    ) -> GoogleEdgecontainerClusterSystemAddonsConfigIngressOutputReference:
        return typing.cast(GoogleEdgecontainerClusterSystemAddonsConfigIngressOutputReference, jsii.get(self, "ingress"))

    @builtins.property
    @jsii.member(jsii_name="ingressInput")
    def ingress_input(
        self,
    ) -> typing.Optional[GoogleEdgecontainerClusterSystemAddonsConfigIngress]:
        return typing.cast(typing.Optional[GoogleEdgecontainerClusterSystemAddonsConfigIngress], jsii.get(self, "ingressInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEdgecontainerClusterSystemAddonsConfig]:
        return typing.cast(typing.Optional[GoogleEdgecontainerClusterSystemAddonsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEdgecontainerClusterSystemAddonsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__833b9d42b28afbd1805e6d16a47826e4e811675dd5f284d55955fcbd09f0978f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleEdgecontainerClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#create GoogleEdgecontainerCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#delete GoogleEdgecontainerCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#update GoogleEdgecontainerCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7d2da0907ff41d7819c3e92f3c87ff9f8af0210afb9ccb494cf78cfd73616b0)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#create GoogleEdgecontainerCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#delete GoogleEdgecontainerCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_edgecontainer_cluster#update GoogleEdgecontainerCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEdgecontainerClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEdgecontainerClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEdgecontainerCluster.GoogleEdgecontainerClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a134759e03313ec80e2042fc14bf8c7389210aaf346ff4b86f9813c001b39e95)
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
            type_hints = typing.get_type_hints(_typecheckingstub__234b78a176b8ac370b70c12d980025333783323d46a05513062e650fa7198a55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f432e11b0f01b3e161dbc01aace1237e06609e0e077d679ceabb389e0d80785)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16a0b42821e368a4cdd4d046ea04791806acf574b328729e836a4d1a6c1245c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEdgecontainerClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEdgecontainerClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEdgecontainerClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06550acef2a2ce2ea9bee5c707aa206e6710f79bf1cd08b7e64b5c5e2edd9e9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleEdgecontainerCluster",
    "GoogleEdgecontainerClusterAuthorization",
    "GoogleEdgecontainerClusterAuthorizationAdminUsers",
    "GoogleEdgecontainerClusterAuthorizationAdminUsersOutputReference",
    "GoogleEdgecontainerClusterAuthorizationOutputReference",
    "GoogleEdgecontainerClusterConfig",
    "GoogleEdgecontainerClusterControlPlane",
    "GoogleEdgecontainerClusterControlPlaneEncryption",
    "GoogleEdgecontainerClusterControlPlaneEncryptionKmsStatus",
    "GoogleEdgecontainerClusterControlPlaneEncryptionKmsStatusList",
    "GoogleEdgecontainerClusterControlPlaneEncryptionKmsStatusOutputReference",
    "GoogleEdgecontainerClusterControlPlaneEncryptionOutputReference",
    "GoogleEdgecontainerClusterControlPlaneLocal",
    "GoogleEdgecontainerClusterControlPlaneLocalOutputReference",
    "GoogleEdgecontainerClusterControlPlaneOutputReference",
    "GoogleEdgecontainerClusterControlPlaneRemote",
    "GoogleEdgecontainerClusterControlPlaneRemoteOutputReference",
    "GoogleEdgecontainerClusterFleet",
    "GoogleEdgecontainerClusterFleetOutputReference",
    "GoogleEdgecontainerClusterMaintenanceEvents",
    "GoogleEdgecontainerClusterMaintenanceEventsList",
    "GoogleEdgecontainerClusterMaintenanceEventsOutputReference",
    "GoogleEdgecontainerClusterMaintenancePolicy",
    "GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusions",
    "GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsList",
    "GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsOutputReference",
    "GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow",
    "GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindowOutputReference",
    "GoogleEdgecontainerClusterMaintenancePolicyOutputReference",
    "GoogleEdgecontainerClusterMaintenancePolicyWindow",
    "GoogleEdgecontainerClusterMaintenancePolicyWindowOutputReference",
    "GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindow",
    "GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowOutputReference",
    "GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow",
    "GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindowOutputReference",
    "GoogleEdgecontainerClusterNetworking",
    "GoogleEdgecontainerClusterNetworkingOutputReference",
    "GoogleEdgecontainerClusterSystemAddonsConfig",
    "GoogleEdgecontainerClusterSystemAddonsConfigIngress",
    "GoogleEdgecontainerClusterSystemAddonsConfigIngressOutputReference",
    "GoogleEdgecontainerClusterSystemAddonsConfigOutputReference",
    "GoogleEdgecontainerClusterTimeouts",
    "GoogleEdgecontainerClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__88d5b570f090931fbeb5942edac0b586bad0752f9efa7213966e01d8e7e01d48(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    authorization: typing.Union[GoogleEdgecontainerClusterAuthorization, typing.Dict[builtins.str, typing.Any]],
    fleet: typing.Union[GoogleEdgecontainerClusterFleet, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    networking: typing.Union[GoogleEdgecontainerClusterNetworking, typing.Dict[builtins.str, typing.Any]],
    control_plane: typing.Optional[typing.Union[GoogleEdgecontainerClusterControlPlane, typing.Dict[builtins.str, typing.Any]]] = None,
    control_plane_encryption: typing.Optional[typing.Union[GoogleEdgecontainerClusterControlPlaneEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    default_max_pods_per_node: typing.Optional[jsii.Number] = None,
    external_load_balancer_ipv4_address_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    maintenance_policy: typing.Optional[typing.Union[GoogleEdgecontainerClusterMaintenancePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    release_channel: typing.Optional[builtins.str] = None,
    system_addons_config: typing.Optional[typing.Union[GoogleEdgecontainerClusterSystemAddonsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    target_version: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleEdgecontainerClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__73da1cf9aa830023da7891c042367de927136e2a8a6ab07524378445fc402795(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e62a426e42f7efc17b42323d3fc2fc3b6819721e39b4b2c8d0c5557ca5eb5810(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__041b71046f4ef801aa2a9661c0f2bf553a6054fb832d67a9fad00446177de9d2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e32469936715db08b0bd58a9426043f9d36958be806f9c2ef67ac54e464ac2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d9706fdfee54ded107a4448eed29a173a22812a872f1a5a1720dd21f8214447(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14cc96fd4453bfcb6e909e989544dd5cce69a9efb7199ad78612d792a0532e20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b1785233bfa0d36c3e38defed54b0854a35de7e9dedebb050ba679d688d4644(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c17f8cf39f7c6d65ce5090fade2b6ddd8471d585efa6fde5ee3fdd1f9696863(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfb7e48d65c1568282755d8fd043575daf5887aa3db55d4d100f621213cb82c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c1a1481257bf3f3be7c6e0d6e580ddcadc4c2f88102d62a074186f7e31aa8ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c7f93a21bb62abaac6a3f3e4f7b9eaa0347247630ea99da288b309b731961e(
    *,
    admin_users: typing.Union[GoogleEdgecontainerClusterAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00e1eb3f0d365c762584ed1b173228599494f6bac22e7095f5aa74e957339a05(
    *,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25be20ac08dd5ae00c22c6129e4f3b9aae71edf04ee224da6f5caf4d95119e12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f09d82025431c5603ae54387a2eb9e546636a2da55cc08228df81ccfb94d675(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55462bf15fe4126b30280143ed110d10b81dbfdc7b84c3043e8c11c71134bb79(
    value: typing.Optional[GoogleEdgecontainerClusterAuthorizationAdminUsers],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a9a2fe81d0f47abb437c10296c7e90e1c907a750c91605c3ee5c08f0cb9611(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f5047eae177f197723a3d16c0b542ae9b7c89a0fe414dbabd547c2230871ce0(
    value: typing.Optional[GoogleEdgecontainerClusterAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ba66bdb12e944e8d3ea2e00e4f14f2a062fe21df8c08562315c02728946c47(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    authorization: typing.Union[GoogleEdgecontainerClusterAuthorization, typing.Dict[builtins.str, typing.Any]],
    fleet: typing.Union[GoogleEdgecontainerClusterFleet, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    networking: typing.Union[GoogleEdgecontainerClusterNetworking, typing.Dict[builtins.str, typing.Any]],
    control_plane: typing.Optional[typing.Union[GoogleEdgecontainerClusterControlPlane, typing.Dict[builtins.str, typing.Any]]] = None,
    control_plane_encryption: typing.Optional[typing.Union[GoogleEdgecontainerClusterControlPlaneEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    default_max_pods_per_node: typing.Optional[jsii.Number] = None,
    external_load_balancer_ipv4_address_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    maintenance_policy: typing.Optional[typing.Union[GoogleEdgecontainerClusterMaintenancePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    release_channel: typing.Optional[builtins.str] = None,
    system_addons_config: typing.Optional[typing.Union[GoogleEdgecontainerClusterSystemAddonsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    target_version: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleEdgecontainerClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4737a6b8a58dadab7ba2a6a7541522de85e03c1141fd6e0488ee4042a7302456(
    *,
    local: typing.Optional[typing.Union[GoogleEdgecontainerClusterControlPlaneLocal, typing.Dict[builtins.str, typing.Any]]] = None,
    remote: typing.Optional[typing.Union[GoogleEdgecontainerClusterControlPlaneRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e74351579b6def8329495bed21ee1c9a79a9c189c68c1e148a3dc8c2bcfc40cc(
    *,
    kms_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea99f78c6ebb4213d26eaea30a87cb314255e7c4397a5cb7c375452e1ae53e0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ae19ac72a8837c3ee22970b1320af603de7aac87c595c220ea1e37f6db25760(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0a88a1a6c723fa55b5aea261e33e44a8a8c345fda845c0e93a7531bb6752f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c99eaa4af7462518a9a937bd27b7a49dbf66bdf01286fabedf59bbe597645d7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56c48c0d772ee53a902fec8873d97dcac1d898045840b3fd1b7dd4b21e1c7593(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bda3cea106ae47fb3fc0ca16835d76a3ce63fc3e5a5305d2a0300a12ad3e44b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4b4b0e26643e592a7e94e20953d7e9c1b269bc473426b821de51028149fa46(
    value: typing.Optional[GoogleEdgecontainerClusterControlPlaneEncryptionKmsStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__484b84415347b1d04427b390ae9cfd8ee75d8b80fa1e534843b69a3f19f718f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ad2a82bb11d9db4a3c7c6ac227cea90fc0768df64092404436cd9f5ecf35e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b7041c94caa0f587847ba46b994721228903cf21174d981dbc01f6a88a267ca(
    value: typing.Optional[GoogleEdgecontainerClusterControlPlaneEncryption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5ffa8a1335c833dd8c046e20886f266429633f025abc2d6a16498858199d840(
    *,
    machine_filter: typing.Optional[builtins.str] = None,
    node_count: typing.Optional[jsii.Number] = None,
    node_location: typing.Optional[builtins.str] = None,
    shared_deployment_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f90226474c504d17d7103920cd0af294d8984fde8a29b94917df87aad1ae84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d41611451db3642cf366a7ea01fb97907a22999df83c2e5fdcccb70a20b88ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b9630b8acee0532a1b5813934751ac7aaf1e02ea4157d9d41a6ce51e5fd68ee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a0effc8413c7811129d7458e0206bf223c325f0ba8a22f54fada638aff99ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eba3e04ba87e717c28c5fd63394838656f3d5a8b9a69c6d08abbd1a38e4b0930(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b38f8de2bfd592f22f0a564b596f735099d5b68835a4018d6370e847e110b7(
    value: typing.Optional[GoogleEdgecontainerClusterControlPlaneLocal],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f3b7edd99ae12bfa65e78127abffbccf801cb1cc468bc5e25f8ba002d41e153(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__583cdebad68eb685639fdccccea2d5cc5de2da2ffce883778cabb2fbfbb76be5(
    value: typing.Optional[GoogleEdgecontainerClusterControlPlane],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f79b2444adf5bfb6c9e0e4e4ee754579d5a995822c8ec9d2a05dd7d59a785882(
    *,
    node_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35ea78b2f3b4900680bb51a3eaab35827de35219bc08194569cfb6678b09fabb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad5a5684dbe683afc02c2a4dc150bf240ef086b4785e13f3ffb7d62fab2c4699(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61c54ddd068029dd63bac9fd8893887fddb6ae92a500175026b48575851355e0(
    value: typing.Optional[GoogleEdgecontainerClusterControlPlaneRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fbedfca4e5572c2aa1df94877cbd277ab3108e74a4cbba9b7dcc41edbe166a2(
    *,
    project: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e6f511e7b694311e09aae744012303c6e8940588e0182b5509584525ed7aa19(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44aeb99c04fde45246fd512f89b76820b04c901e9e08dc278df2cb69712a46e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417059a1e1da756699886b77aa60dafff0b4762fea7c4bec974ccd32edeecbe0(
    value: typing.Optional[GoogleEdgecontainerClusterFleet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35d21e9044507a1f02b57083148261bec2c5b6ef8320600f36a3cabb488397f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f2d583617ba12a6f3033553f1d7771ea8d2a90d1499e5d551b9b2b2a43179ba(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc9f0651d1be79b0b4ced3be8005b9e5808be761945abc80aaba437e657206e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a20396c091e79db2ae55b6ea2f4473f70424943af787dde218399da97819a6d7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2b3c685cbe749ca606a654121c77110d52343d854eaaee4fcd2f567695d8b5e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b85337692f8056a1af628ffb6e4e72cd0fbbed06212083a40715fc2f46ba3972(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e1668e9719d2f6519d01777c3f460f3825e1ca7c52e9a02fad360a161cbb7f(
    value: typing.Optional[GoogleEdgecontainerClusterMaintenanceEvents],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cdaf111bcf9729292645c2ad7b86f0066abe002053535ea2337d5fccea0618f(
    *,
    window: typing.Union[GoogleEdgecontainerClusterMaintenancePolicyWindow, typing.Dict[builtins.str, typing.Any]],
    maintenance_exclusions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusions, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211fd0e5d4b89de369e4cfc0b56a0f6796d2637526bab298f64fa4a9a44cb444(
    *,
    id: typing.Optional[builtins.str] = None,
    window: typing.Optional[typing.Union[GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04d9f8eddd43cbd83d205b625b162980220b9fca52200fe0e93447cd1698bdf8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e663a334fcfe88f2007e83ef5f560b531834db3a238febbf35c06171527068c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e75b5e8bbe5b32e6543bd5b58688f0836547f1da3d69acc41c285c581c6b7a98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc0e5ab4785840d7804cea8dfb7ff7c3be5ba2b5b452c8e406b6e565fe6a7c7d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd41f7127fb8c62a36a3771c8b27ba15333c344e6c39a3f872c3b6920eb83321(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__903a9daf74cf428389e255eb8a5189e8a4e9e72a1e699ac890cd1889476595d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__255bda1b18f310b2eb1d22423de669022cbea2263293f4548585b4ca00714483(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c3b851c60ac3595716ba708468fc2c8eac370ecf39c0b183e1d64ff1e5d677c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feba6e457f0698aa2d2d8b8b142f5bf818b95961b52045ac038579169aaf0196(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aaea1fc6f5e0a61076ef17a123e691c50ca963d86f7ebf734d40f04d7324d2b(
    *,
    end_time: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e1e24b7e1b595ca67e2b083ba7fb97633183483bf54dd518ad03256ae6f4856(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc6a17356895595af4f4a3472097c220207b8f9c73d8b80433c936533963c432(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__883dc02112d8f1514cf7d1e013a64b48928077d3ab969be6d764f4d1a5b7225b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f1d69fe1167768698ff0bfe18818d9fe9f53edfa8cc62d385acfa48b26d51a(
    value: typing.Optional[GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusionsWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac2d63442798d2a9eeeb3b9d3b186497e42f1e81f410160d15d31242c3718f3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39e53b161ea57de6bf9b036c9421633cf10c67ff03254115db5a66406e990bd0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleEdgecontainerClusterMaintenancePolicyMaintenanceExclusions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30150c7ac1bb3a7418f4e5aa768049d71bf4255ecc7bcbaeb259566ecd8c2e5(
    value: typing.Optional[GoogleEdgecontainerClusterMaintenancePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46837c12c1bccbf05be933e1dac3d57e64af1674e254a0010f30dfb59a15b4a9(
    *,
    recurring_window: typing.Union[GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindow, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__333bd12de730ca9188c9e2c94960c57dca068d9904ce98c1035b4bc167e7361d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c331a984d631f7e087b203a42918d2d65c61556070331ea7c332d648d45047(
    value: typing.Optional[GoogleEdgecontainerClusterMaintenancePolicyWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e545a44b38d1bb410d3d43743d9aa8f00516bb8e336dc9696e0dba243a23825(
    *,
    recurrence: typing.Optional[builtins.str] = None,
    window: typing.Optional[typing.Union[GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff56cbfd6fdd263ee4360bd60f118dcff488da570ce1279e6282f25bebf76d65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c387e7ac512008951def0314ad6ca5fe39233f5b390c21ac59f02effd02315d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e54854081b28f8f3cf365fc1c26f57392f9db6d7b8bd80d32a3f9263988f3704(
    value: typing.Optional[GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ba80854534eefb374a6e0f4fadb9b8a349448a8b1b98797c2fffa1961675bfb(
    *,
    end_time: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02615d96371c4b0370babf36c4762b79bee2b92521dc117e589434eb4e17530f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab866fd23d9a225a9b331aa75e8f8a3e37a7ee1ba13c15962d07524868cd4bc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7051989bd4a45cd18976282dde2b41f0ea7f43a065612498126cacabe6da381d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da14a886d2cf9cbd9076c8db6a4eb18a38b97017932f95d2101a366d74ca63d0(
    value: typing.Optional[GoogleEdgecontainerClusterMaintenancePolicyWindowRecurringWindowWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__097d3b738c01e336800715e24cd3e0116e0ec625d4f691216d917e8a59bd053a(
    *,
    cluster_ipv4_cidr_blocks: typing.Sequence[builtins.str],
    services_ipv4_cidr_blocks: typing.Sequence[builtins.str],
    cluster_ipv6_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
    services_ipv6_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbcfae32fcd3f8211cdc832ca8ac5f42ea673970d0c791f85630f296d41a30da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91cfc7b64dfd779e89f96e06d62436a90f216fe7dfb974b35c6cd2f6728be4fd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__694817f3a3d1866659421f7afc8420d4f7670ec35f38ada8b16b70b2eedf8a37(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d80bda9fdcbfe8fa26a679b25268d641cb4de15a95d120543fedc081f42e2f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc482d9ddcee95bd8c75e237bed7be1a9fcff6eb39356f183f071e7880ad0127(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab7ae354ab873a5f63b86e75c7216ca11c4fc1ab1d32b31e3580c902d023470(
    value: typing.Optional[GoogleEdgecontainerClusterNetworking],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e74a0f794f24acb10577bb777761d5dfe31895403ecff5b5c1627ef931f8cda(
    *,
    ingress: typing.Optional[typing.Union[GoogleEdgecontainerClusterSystemAddonsConfigIngress, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7c9204e4ffbc9951df916a6e76e029462f0cb306f8cae689d281a5a53eadfbd(
    *,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ipv4_vip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__237b01ec115efaa9be78b746e161cda1d7e558a54e5a82c2a1c1078e3bd9e32e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6ceca0130d6c96040016e2105922789e11b08b59b0e843ef901537d8c483c0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__767d07dac9192efeaa186122e990bfbc334993da3356660658604152cc4a8b2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f6511c3aa9289ac43c684ce91e4c16286ea3cdeea8fe763921492673fd27b4(
    value: typing.Optional[GoogleEdgecontainerClusterSystemAddonsConfigIngress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1177c2e4263dbe7e81d91904a083bea2544b291efb86420d5042f77ca1511edb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__833b9d42b28afbd1805e6d16a47826e4e811675dd5f284d55955fcbd09f0978f(
    value: typing.Optional[GoogleEdgecontainerClusterSystemAddonsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d2da0907ff41d7819c3e92f3c87ff9f8af0210afb9ccb494cf78cfd73616b0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a134759e03313ec80e2042fc14bf8c7389210aaf346ff4b86f9813c001b39e95(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__234b78a176b8ac370b70c12d980025333783323d46a05513062e650fa7198a55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f432e11b0f01b3e161dbc01aace1237e06609e0e077d679ceabb389e0d80785(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a0b42821e368a4cdd4d046ea04791806acf574b328729e836a4d1a6c1245c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06550acef2a2ce2ea9bee5c707aa206e6710f79bf1cd08b7e64b5c5e2edd9e9c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEdgecontainerClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
