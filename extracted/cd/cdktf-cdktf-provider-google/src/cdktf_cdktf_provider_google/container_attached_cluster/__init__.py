r'''
# `google_container_attached_cluster`

Refer to the Terraform Registry for docs: [`google_container_attached_cluster`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster).
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


class ContainerAttachedCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster google_container_attached_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        distribution: builtins.str,
        fleet: typing.Union["ContainerAttachedClusterFleet", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        oidc_config: typing.Union["ContainerAttachedClusterOidcConfig", typing.Dict[builtins.str, typing.Any]],
        platform_version: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        authorization: typing.Optional[typing.Union["ContainerAttachedClusterAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
        binary_authorization: typing.Optional[typing.Union["ContainerAttachedClusterBinaryAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_policy: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union["ContainerAttachedClusterLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        monitoring_config: typing.Optional[typing.Union["ContainerAttachedClusterMonitoringConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        proxy_config: typing.Optional[typing.Union["ContainerAttachedClusterProxyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        security_posture_config: typing.Optional[typing.Union["ContainerAttachedClusterSecurityPostureConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ContainerAttachedClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster google_container_attached_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param distribution: The Kubernetes distribution of the underlying attached cluster. Supported values: "eks", "aks", "generic". The generic distribution provides the ability to register or migrate any CNCF conformant cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#distribution ContainerAttachedCluster#distribution}
        :param fleet: fleet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#fleet ContainerAttachedCluster#fleet}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#location ContainerAttachedCluster#location}
        :param name: The name of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#name ContainerAttachedCluster#name}
        :param oidc_config: oidc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#oidc_config ContainerAttachedCluster#oidc_config}
        :param platform_version: The platform version for the cluster (e.g. '1.23.0-gke.1'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#platform_version ContainerAttachedCluster#platform_version}
        :param annotations: Optional. Annotations on the cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#annotations ContainerAttachedCluster#annotations}
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#authorization ContainerAttachedCluster#authorization}
        :param binary_authorization: binary_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#binary_authorization ContainerAttachedCluster#binary_authorization}
        :param deletion_policy: Policy to determine what flags to send on delete. Possible values: DELETE, DELETE_IGNORE_ERRORS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#deletion_policy ContainerAttachedCluster#deletion_policy}
        :param description: A human readable description of this attached cluster. Cannot be longer than 255 UTF-8 encoded bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#description ContainerAttachedCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#id ContainerAttachedCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#logging_config ContainerAttachedCluster#logging_config}
        :param monitoring_config: monitoring_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#monitoring_config ContainerAttachedCluster#monitoring_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#project ContainerAttachedCluster#project}.
        :param proxy_config: proxy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#proxy_config ContainerAttachedCluster#proxy_config}
        :param security_posture_config: security_posture_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#security_posture_config ContainerAttachedCluster#security_posture_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#timeouts ContainerAttachedCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8020a75e6ece36ba51905b5e491fd97b4a3c3ba930d1537b8fc78f6d3ca7e639)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ContainerAttachedClusterConfig(
            distribution=distribution,
            fleet=fleet,
            location=location,
            name=name,
            oidc_config=oidc_config,
            platform_version=platform_version,
            annotations=annotations,
            authorization=authorization,
            binary_authorization=binary_authorization,
            deletion_policy=deletion_policy,
            description=description,
            id=id,
            logging_config=logging_config,
            monitoring_config=monitoring_config,
            project=project,
            proxy_config=proxy_config,
            security_posture_config=security_posture_config,
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
        '''Generates CDKTF code for importing a ContainerAttachedCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ContainerAttachedCluster to import.
        :param import_from_id: The id of the existing ContainerAttachedCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ContainerAttachedCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ed214955aeca4d16affe1f14262f54fb9fbb002558a389542296d56426d1808)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAuthorization")
    def put_authorization(
        self,
        *,
        admin_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        admin_users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param admin_groups: Groups that can perform operations as a cluster admin. A managed ClusterRoleBinding will be created to grant the 'cluster-admin' ClusterRole to the groups. Up to ten admin groups can be provided. For more info on RBAC, see https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#admin_groups ContainerAttachedCluster#admin_groups}
        :param admin_users: Users that can perform operations as a cluster admin. A managed ClusterRoleBinding will be created to grant the 'cluster-admin' ClusterRole to the users. Up to ten admin users can be provided. For more info on RBAC, see https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#admin_users ContainerAttachedCluster#admin_users}
        '''
        value = ContainerAttachedClusterAuthorization(
            admin_groups=admin_groups, admin_users=admin_users
        )

        return typing.cast(None, jsii.invoke(self, "putAuthorization", [value]))

    @jsii.member(jsii_name="putBinaryAuthorization")
    def put_binary_authorization(
        self,
        *,
        evaluation_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param evaluation_mode: Configure Binary Authorization evaluation mode. Possible values: ["DISABLED", "PROJECT_SINGLETON_POLICY_ENFORCE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#evaluation_mode ContainerAttachedCluster#evaluation_mode}
        '''
        value = ContainerAttachedClusterBinaryAuthorization(
            evaluation_mode=evaluation_mode
        )

        return typing.cast(None, jsii.invoke(self, "putBinaryAuthorization", [value]))

    @jsii.member(jsii_name="putFleet")
    def put_fleet(self, *, project: builtins.str) -> None:
        '''
        :param project: The number of the Fleet host project where this cluster will be registered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#project ContainerAttachedCluster#project}
        '''
        value = ContainerAttachedClusterFleet(project=project)

        return typing.cast(None, jsii.invoke(self, "putFleet", [value]))

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        component_config: typing.Optional[typing.Union["ContainerAttachedClusterLoggingConfigComponentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param component_config: component_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#component_config ContainerAttachedCluster#component_config}
        '''
        value = ContainerAttachedClusterLoggingConfig(
            component_config=component_config
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

    @jsii.member(jsii_name="putMonitoringConfig")
    def put_monitoring_config(
        self,
        *,
        managed_prometheus_config: typing.Optional[typing.Union["ContainerAttachedClusterMonitoringConfigManagedPrometheusConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param managed_prometheus_config: managed_prometheus_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#managed_prometheus_config ContainerAttachedCluster#managed_prometheus_config}
        '''
        value = ContainerAttachedClusterMonitoringConfig(
            managed_prometheus_config=managed_prometheus_config
        )

        return typing.cast(None, jsii.invoke(self, "putMonitoringConfig", [value]))

    @jsii.member(jsii_name="putOidcConfig")
    def put_oidc_config(
        self,
        *,
        issuer_url: builtins.str,
        jwks: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param issuer_url: A JSON Web Token (JWT) issuer URI. 'issuer' must start with 'https://'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#issuer_url ContainerAttachedCluster#issuer_url}
        :param jwks: OIDC verification keys in JWKS format (RFC 7517). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#jwks ContainerAttachedCluster#jwks}
        '''
        value = ContainerAttachedClusterOidcConfig(issuer_url=issuer_url, jwks=jwks)

        return typing.cast(None, jsii.invoke(self, "putOidcConfig", [value]))

    @jsii.member(jsii_name="putProxyConfig")
    def put_proxy_config(
        self,
        *,
        kubernetes_secret: typing.Optional[typing.Union["ContainerAttachedClusterProxyConfigKubernetesSecret", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param kubernetes_secret: kubernetes_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#kubernetes_secret ContainerAttachedCluster#kubernetes_secret}
        '''
        value = ContainerAttachedClusterProxyConfig(
            kubernetes_secret=kubernetes_secret
        )

        return typing.cast(None, jsii.invoke(self, "putProxyConfig", [value]))

    @jsii.member(jsii_name="putSecurityPostureConfig")
    def put_security_posture_config(self, *, vulnerability_mode: builtins.str) -> None:
        '''
        :param vulnerability_mode: Sets the mode of the Kubernetes security posture API's workload vulnerability scanning. Possible values: ["VULNERABILITY_DISABLED", "VULNERABILITY_ENTERPRISE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#vulnerability_mode ContainerAttachedCluster#vulnerability_mode}
        '''
        value = ContainerAttachedClusterSecurityPostureConfig(
            vulnerability_mode=vulnerability_mode
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityPostureConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#create ContainerAttachedCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#delete ContainerAttachedCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#update ContainerAttachedCluster#update}.
        '''
        value = ContainerAttachedClusterTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetAuthorization")
    def reset_authorization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorization", []))

    @jsii.member(jsii_name="resetBinaryAuthorization")
    def reset_binary_authorization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBinaryAuthorization", []))

    @jsii.member(jsii_name="resetDeletionPolicy")
    def reset_deletion_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionPolicy", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLoggingConfig")
    def reset_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfig", []))

    @jsii.member(jsii_name="resetMonitoringConfig")
    def reset_monitoring_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitoringConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetProxyConfig")
    def reset_proxy_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyConfig", []))

    @jsii.member(jsii_name="resetSecurityPostureConfig")
    def reset_security_posture_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityPostureConfig", []))

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
    def authorization(self) -> "ContainerAttachedClusterAuthorizationOutputReference":
        return typing.cast("ContainerAttachedClusterAuthorizationOutputReference", jsii.get(self, "authorization"))

    @builtins.property
    @jsii.member(jsii_name="binaryAuthorization")
    def binary_authorization(
        self,
    ) -> "ContainerAttachedClusterBinaryAuthorizationOutputReference":
        return typing.cast("ContainerAttachedClusterBinaryAuthorizationOutputReference", jsii.get(self, "binaryAuthorization"))

    @builtins.property
    @jsii.member(jsii_name="clusterRegion")
    def cluster_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterRegion"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="errors")
    def errors(self) -> "ContainerAttachedClusterErrorsList":
        return typing.cast("ContainerAttachedClusterErrorsList", jsii.get(self, "errors"))

    @builtins.property
    @jsii.member(jsii_name="fleet")
    def fleet(self) -> "ContainerAttachedClusterFleetOutputReference":
        return typing.cast("ContainerAttachedClusterFleetOutputReference", jsii.get(self, "fleet"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesVersion")
    def kubernetes_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesVersion"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(self) -> "ContainerAttachedClusterLoggingConfigOutputReference":
        return typing.cast("ContainerAttachedClusterLoggingConfigOutputReference", jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="monitoringConfig")
    def monitoring_config(
        self,
    ) -> "ContainerAttachedClusterMonitoringConfigOutputReference":
        return typing.cast("ContainerAttachedClusterMonitoringConfigOutputReference", jsii.get(self, "monitoringConfig"))

    @builtins.property
    @jsii.member(jsii_name="oidcConfig")
    def oidc_config(self) -> "ContainerAttachedClusterOidcConfigOutputReference":
        return typing.cast("ContainerAttachedClusterOidcConfigOutputReference", jsii.get(self, "oidcConfig"))

    @builtins.property
    @jsii.member(jsii_name="proxyConfig")
    def proxy_config(self) -> "ContainerAttachedClusterProxyConfigOutputReference":
        return typing.cast("ContainerAttachedClusterProxyConfigOutputReference", jsii.get(self, "proxyConfig"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="securityPostureConfig")
    def security_posture_config(
        self,
    ) -> "ContainerAttachedClusterSecurityPostureConfigOutputReference":
        return typing.cast("ContainerAttachedClusterSecurityPostureConfigOutputReference", jsii.get(self, "securityPostureConfig"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ContainerAttachedClusterTimeoutsOutputReference":
        return typing.cast("ContainerAttachedClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="workloadIdentityConfig")
    def workload_identity_config(
        self,
    ) -> "ContainerAttachedClusterWorkloadIdentityConfigList":
        return typing.cast("ContainerAttachedClusterWorkloadIdentityConfigList", jsii.get(self, "workloadIdentityConfig"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationInput")
    def authorization_input(
        self,
    ) -> typing.Optional["ContainerAttachedClusterAuthorization"]:
        return typing.cast(typing.Optional["ContainerAttachedClusterAuthorization"], jsii.get(self, "authorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="binaryAuthorizationInput")
    def binary_authorization_input(
        self,
    ) -> typing.Optional["ContainerAttachedClusterBinaryAuthorization"]:
        return typing.cast(typing.Optional["ContainerAttachedClusterBinaryAuthorization"], jsii.get(self, "binaryAuthorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionPolicyInput")
    def deletion_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deletionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="distributionInput")
    def distribution_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "distributionInput"))

    @builtins.property
    @jsii.member(jsii_name="fleetInput")
    def fleet_input(self) -> typing.Optional["ContainerAttachedClusterFleet"]:
        return typing.cast(typing.Optional["ContainerAttachedClusterFleet"], jsii.get(self, "fleetInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfigInput")
    def logging_config_input(
        self,
    ) -> typing.Optional["ContainerAttachedClusterLoggingConfig"]:
        return typing.cast(typing.Optional["ContainerAttachedClusterLoggingConfig"], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="monitoringConfigInput")
    def monitoring_config_input(
        self,
    ) -> typing.Optional["ContainerAttachedClusterMonitoringConfig"]:
        return typing.cast(typing.Optional["ContainerAttachedClusterMonitoringConfig"], jsii.get(self, "monitoringConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="oidcConfigInput")
    def oidc_config_input(
        self,
    ) -> typing.Optional["ContainerAttachedClusterOidcConfig"]:
        return typing.cast(typing.Optional["ContainerAttachedClusterOidcConfig"], jsii.get(self, "oidcConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="platformVersionInput")
    def platform_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "platformVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyConfigInput")
    def proxy_config_input(
        self,
    ) -> typing.Optional["ContainerAttachedClusterProxyConfig"]:
        return typing.cast(typing.Optional["ContainerAttachedClusterProxyConfig"], jsii.get(self, "proxyConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="securityPostureConfigInput")
    def security_posture_config_input(
        self,
    ) -> typing.Optional["ContainerAttachedClusterSecurityPostureConfig"]:
        return typing.cast(typing.Optional["ContainerAttachedClusterSecurityPostureConfig"], jsii.get(self, "securityPostureConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerAttachedClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerAttachedClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5510a81fd4933d0778b7b6b54b095654bfba12364969d3d7b5349bf427bd00d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionPolicy")
    def deletion_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deletionPolicy"))

    @deletion_policy.setter
    def deletion_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__006e4236961c6137a52a1d08c01fbec2d576de77a209c6ac42831ad3fdd57fe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8b8e083ccbd07ed32c3d1182f13772d0a2a64749337e13e7c5123dc158c1774)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="distribution")
    def distribution(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "distribution"))

    @distribution.setter
    def distribution(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b48ce1d564311c5f2a76a3e2c824786da658e35be84a68c995327c22a117405)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distribution", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5c7a7be5de943fe315eccb8d966ac214e7b729e38d09c575b6a43ee18054d86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e3df3c7dee3be5a589591de1ccafda3cb99a57f1f12318fe418f64d3995eb88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc46355f0f5d047122b16912045b608b7cfe60cb999517a31c6bf5113eb0a904)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="platformVersion")
    def platform_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platformVersion"))

    @platform_version.setter
    def platform_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4fae87080dea04f20d7e3da67151fc8848105852cfdc8f37faf8ade0cee6780)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platformVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dffc16efe720f04be0e0491ec16221348d929d4b7a7eef92e653b1316cc443bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterAuthorization",
    jsii_struct_bases=[],
    name_mapping={"admin_groups": "adminGroups", "admin_users": "adminUsers"},
)
class ContainerAttachedClusterAuthorization:
    def __init__(
        self,
        *,
        admin_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        admin_users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param admin_groups: Groups that can perform operations as a cluster admin. A managed ClusterRoleBinding will be created to grant the 'cluster-admin' ClusterRole to the groups. Up to ten admin groups can be provided. For more info on RBAC, see https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#admin_groups ContainerAttachedCluster#admin_groups}
        :param admin_users: Users that can perform operations as a cluster admin. A managed ClusterRoleBinding will be created to grant the 'cluster-admin' ClusterRole to the users. Up to ten admin users can be provided. For more info on RBAC, see https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#admin_users ContainerAttachedCluster#admin_users}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80f99900324de47d090408cec3c25daed41224e0a6a11a5bae0021b86335e0a6)
            check_type(argname="argument admin_groups", value=admin_groups, expected_type=type_hints["admin_groups"])
            check_type(argname="argument admin_users", value=admin_users, expected_type=type_hints["admin_users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if admin_groups is not None:
            self._values["admin_groups"] = admin_groups
        if admin_users is not None:
            self._values["admin_users"] = admin_users

    @builtins.property
    def admin_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Groups that can perform operations as a cluster admin.

        A managed
        ClusterRoleBinding will be created to grant the 'cluster-admin' ClusterRole
        to the groups. Up to ten admin groups can be provided.

        For more info on RBAC, see
        https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#admin_groups ContainerAttachedCluster#admin_groups}
        '''
        result = self._values.get("admin_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def admin_users(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Users that can perform operations as a cluster admin.

        A managed
        ClusterRoleBinding will be created to grant the 'cluster-admin' ClusterRole
        to the users. Up to ten admin users can be provided.

        For more info on RBAC, see
        https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#admin_users ContainerAttachedCluster#admin_users}
        '''
        result = self._values.get("admin_users")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAttachedClusterAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAttachedClusterAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66e926f078a4989d43de33833e60e728853f71853ed15e5e16d4bed689141d87)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdminGroups")
    def reset_admin_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminGroups", []))

    @jsii.member(jsii_name="resetAdminUsers")
    def reset_admin_users(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminUsers", []))

    @builtins.property
    @jsii.member(jsii_name="adminGroupsInput")
    def admin_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "adminGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="adminUsersInput")
    def admin_users_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "adminUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="adminGroups")
    def admin_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "adminGroups"))

    @admin_groups.setter
    def admin_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0089812f2a89fcb22ccc3a3f168b01d63e50dc3f19a27fb21518edd6532ded83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="adminUsers")
    def admin_users(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "adminUsers"))

    @admin_users.setter
    def admin_users(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd8c26be379d803668dc0a3d3663b7c65382964d427020bcfc4b47db2bce48fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminUsers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAttachedClusterAuthorization]:
        return typing.cast(typing.Optional[ContainerAttachedClusterAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAttachedClusterAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d1d429a9098733d9ffb39a3c52730ca1a41838d7271f1065d8ec9c46a48dc72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterBinaryAuthorization",
    jsii_struct_bases=[],
    name_mapping={"evaluation_mode": "evaluationMode"},
)
class ContainerAttachedClusterBinaryAuthorization:
    def __init__(
        self,
        *,
        evaluation_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param evaluation_mode: Configure Binary Authorization evaluation mode. Possible values: ["DISABLED", "PROJECT_SINGLETON_POLICY_ENFORCE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#evaluation_mode ContainerAttachedCluster#evaluation_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01a46a44887952d85ec3adcdc990e3ba002d8cbe7e342d516f6a47a2b1a24d78)
            check_type(argname="argument evaluation_mode", value=evaluation_mode, expected_type=type_hints["evaluation_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if evaluation_mode is not None:
            self._values["evaluation_mode"] = evaluation_mode

    @builtins.property
    def evaluation_mode(self) -> typing.Optional[builtins.str]:
        '''Configure Binary Authorization evaluation mode. Possible values: ["DISABLED", "PROJECT_SINGLETON_POLICY_ENFORCE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#evaluation_mode ContainerAttachedCluster#evaluation_mode}
        '''
        result = self._values.get("evaluation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAttachedClusterBinaryAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAttachedClusterBinaryAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterBinaryAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ed4b92e0b7fd23d98def456413bec8c9250a91d66e7774bd9ba9c2cdf5769d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__35995794b6e48bff9560e8316b74a7af6b39494a63e5463a2528172d1e0e359e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAttachedClusterBinaryAuthorization]:
        return typing.cast(typing.Optional[ContainerAttachedClusterBinaryAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAttachedClusterBinaryAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c8447a42d39559989702685a65094f978f931d84212db24356719c75154bc0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "distribution": "distribution",
        "fleet": "fleet",
        "location": "location",
        "name": "name",
        "oidc_config": "oidcConfig",
        "platform_version": "platformVersion",
        "annotations": "annotations",
        "authorization": "authorization",
        "binary_authorization": "binaryAuthorization",
        "deletion_policy": "deletionPolicy",
        "description": "description",
        "id": "id",
        "logging_config": "loggingConfig",
        "monitoring_config": "monitoringConfig",
        "project": "project",
        "proxy_config": "proxyConfig",
        "security_posture_config": "securityPostureConfig",
        "timeouts": "timeouts",
    },
)
class ContainerAttachedClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        distribution: builtins.str,
        fleet: typing.Union["ContainerAttachedClusterFleet", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        oidc_config: typing.Union["ContainerAttachedClusterOidcConfig", typing.Dict[builtins.str, typing.Any]],
        platform_version: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        authorization: typing.Optional[typing.Union[ContainerAttachedClusterAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
        binary_authorization: typing.Optional[typing.Union[ContainerAttachedClusterBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_policy: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union["ContainerAttachedClusterLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        monitoring_config: typing.Optional[typing.Union["ContainerAttachedClusterMonitoringConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        proxy_config: typing.Optional[typing.Union["ContainerAttachedClusterProxyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        security_posture_config: typing.Optional[typing.Union["ContainerAttachedClusterSecurityPostureConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ContainerAttachedClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param distribution: The Kubernetes distribution of the underlying attached cluster. Supported values: "eks", "aks", "generic". The generic distribution provides the ability to register or migrate any CNCF conformant cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#distribution ContainerAttachedCluster#distribution}
        :param fleet: fleet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#fleet ContainerAttachedCluster#fleet}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#location ContainerAttachedCluster#location}
        :param name: The name of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#name ContainerAttachedCluster#name}
        :param oidc_config: oidc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#oidc_config ContainerAttachedCluster#oidc_config}
        :param platform_version: The platform version for the cluster (e.g. '1.23.0-gke.1'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#platform_version ContainerAttachedCluster#platform_version}
        :param annotations: Optional. Annotations on the cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#annotations ContainerAttachedCluster#annotations}
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#authorization ContainerAttachedCluster#authorization}
        :param binary_authorization: binary_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#binary_authorization ContainerAttachedCluster#binary_authorization}
        :param deletion_policy: Policy to determine what flags to send on delete. Possible values: DELETE, DELETE_IGNORE_ERRORS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#deletion_policy ContainerAttachedCluster#deletion_policy}
        :param description: A human readable description of this attached cluster. Cannot be longer than 255 UTF-8 encoded bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#description ContainerAttachedCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#id ContainerAttachedCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#logging_config ContainerAttachedCluster#logging_config}
        :param monitoring_config: monitoring_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#monitoring_config ContainerAttachedCluster#monitoring_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#project ContainerAttachedCluster#project}.
        :param proxy_config: proxy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#proxy_config ContainerAttachedCluster#proxy_config}
        :param security_posture_config: security_posture_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#security_posture_config ContainerAttachedCluster#security_posture_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#timeouts ContainerAttachedCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(fleet, dict):
            fleet = ContainerAttachedClusterFleet(**fleet)
        if isinstance(oidc_config, dict):
            oidc_config = ContainerAttachedClusterOidcConfig(**oidc_config)
        if isinstance(authorization, dict):
            authorization = ContainerAttachedClusterAuthorization(**authorization)
        if isinstance(binary_authorization, dict):
            binary_authorization = ContainerAttachedClusterBinaryAuthorization(**binary_authorization)
        if isinstance(logging_config, dict):
            logging_config = ContainerAttachedClusterLoggingConfig(**logging_config)
        if isinstance(monitoring_config, dict):
            monitoring_config = ContainerAttachedClusterMonitoringConfig(**monitoring_config)
        if isinstance(proxy_config, dict):
            proxy_config = ContainerAttachedClusterProxyConfig(**proxy_config)
        if isinstance(security_posture_config, dict):
            security_posture_config = ContainerAttachedClusterSecurityPostureConfig(**security_posture_config)
        if isinstance(timeouts, dict):
            timeouts = ContainerAttachedClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59ab3374d43c9b669abe5973dbe2e073b60745b3c780a0ccb12b19238a7eebad)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument distribution", value=distribution, expected_type=type_hints["distribution"])
            check_type(argname="argument fleet", value=fleet, expected_type=type_hints["fleet"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument oidc_config", value=oidc_config, expected_type=type_hints["oidc_config"])
            check_type(argname="argument platform_version", value=platform_version, expected_type=type_hints["platform_version"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument authorization", value=authorization, expected_type=type_hints["authorization"])
            check_type(argname="argument binary_authorization", value=binary_authorization, expected_type=type_hints["binary_authorization"])
            check_type(argname="argument deletion_policy", value=deletion_policy, expected_type=type_hints["deletion_policy"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument monitoring_config", value=monitoring_config, expected_type=type_hints["monitoring_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument proxy_config", value=proxy_config, expected_type=type_hints["proxy_config"])
            check_type(argname="argument security_posture_config", value=security_posture_config, expected_type=type_hints["security_posture_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "distribution": distribution,
            "fleet": fleet,
            "location": location,
            "name": name,
            "oidc_config": oidc_config,
            "platform_version": platform_version,
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
        if authorization is not None:
            self._values["authorization"] = authorization
        if binary_authorization is not None:
            self._values["binary_authorization"] = binary_authorization
        if deletion_policy is not None:
            self._values["deletion_policy"] = deletion_policy
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if monitoring_config is not None:
            self._values["monitoring_config"] = monitoring_config
        if project is not None:
            self._values["project"] = project
        if proxy_config is not None:
            self._values["proxy_config"] = proxy_config
        if security_posture_config is not None:
            self._values["security_posture_config"] = security_posture_config
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
    def distribution(self) -> builtins.str:
        '''The Kubernetes distribution of the underlying attached cluster.

        Supported values:
        "eks", "aks", "generic". The generic distribution provides the ability to register
        or migrate any CNCF conformant cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#distribution ContainerAttachedCluster#distribution}
        '''
        result = self._values.get("distribution")
        assert result is not None, "Required property 'distribution' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fleet(self) -> "ContainerAttachedClusterFleet":
        '''fleet block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#fleet ContainerAttachedCluster#fleet}
        '''
        result = self._values.get("fleet")
        assert result is not None, "Required property 'fleet' is missing"
        return typing.cast("ContainerAttachedClusterFleet", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#location ContainerAttachedCluster#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#name ContainerAttachedCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oidc_config(self) -> "ContainerAttachedClusterOidcConfig":
        '''oidc_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#oidc_config ContainerAttachedCluster#oidc_config}
        '''
        result = self._values.get("oidc_config")
        assert result is not None, "Required property 'oidc_config' is missing"
        return typing.cast("ContainerAttachedClusterOidcConfig", result)

    @builtins.property
    def platform_version(self) -> builtins.str:
        '''The platform version for the cluster (e.g. '1.23.0-gke.1').

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#platform_version ContainerAttachedCluster#platform_version}
        '''
        result = self._values.get("platform_version")
        assert result is not None, "Required property 'platform_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        Annotations on the cluster. This field has the same
        restrictions as Kubernetes annotations. The total size of all keys and
        values combined is limited to 256k. Key can have 2 segments: prefix (optional)
        and name (required), separated by a slash (/). Prefix must be a DNS subdomain.
        Name must be 63 characters or less, begin and end with alphanumerics,
        with dashes (-), underscores (_), dots (.), and alphanumerics between.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#annotations ContainerAttachedCluster#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def authorization(self) -> typing.Optional[ContainerAttachedClusterAuthorization]:
        '''authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#authorization ContainerAttachedCluster#authorization}
        '''
        result = self._values.get("authorization")
        return typing.cast(typing.Optional[ContainerAttachedClusterAuthorization], result)

    @builtins.property
    def binary_authorization(
        self,
    ) -> typing.Optional[ContainerAttachedClusterBinaryAuthorization]:
        '''binary_authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#binary_authorization ContainerAttachedCluster#binary_authorization}
        '''
        result = self._values.get("binary_authorization")
        return typing.cast(typing.Optional[ContainerAttachedClusterBinaryAuthorization], result)

    @builtins.property
    def deletion_policy(self) -> typing.Optional[builtins.str]:
        '''Policy to determine what flags to send on delete. Possible values: DELETE, DELETE_IGNORE_ERRORS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#deletion_policy ContainerAttachedCluster#deletion_policy}
        '''
        result = self._values.get("deletion_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human readable description of this attached cluster. Cannot be longer than 255 UTF-8 encoded bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#description ContainerAttachedCluster#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#id ContainerAttachedCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional["ContainerAttachedClusterLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#logging_config ContainerAttachedCluster#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["ContainerAttachedClusterLoggingConfig"], result)

    @builtins.property
    def monitoring_config(
        self,
    ) -> typing.Optional["ContainerAttachedClusterMonitoringConfig"]:
        '''monitoring_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#monitoring_config ContainerAttachedCluster#monitoring_config}
        '''
        result = self._values.get("monitoring_config")
        return typing.cast(typing.Optional["ContainerAttachedClusterMonitoringConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#project ContainerAttachedCluster#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_config(self) -> typing.Optional["ContainerAttachedClusterProxyConfig"]:
        '''proxy_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#proxy_config ContainerAttachedCluster#proxy_config}
        '''
        result = self._values.get("proxy_config")
        return typing.cast(typing.Optional["ContainerAttachedClusterProxyConfig"], result)

    @builtins.property
    def security_posture_config(
        self,
    ) -> typing.Optional["ContainerAttachedClusterSecurityPostureConfig"]:
        '''security_posture_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#security_posture_config ContainerAttachedCluster#security_posture_config}
        '''
        result = self._values.get("security_posture_config")
        return typing.cast(typing.Optional["ContainerAttachedClusterSecurityPostureConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ContainerAttachedClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#timeouts ContainerAttachedCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ContainerAttachedClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAttachedClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterErrors",
    jsii_struct_bases=[],
    name_mapping={},
)
class ContainerAttachedClusterErrors:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAttachedClusterErrors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAttachedClusterErrorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterErrorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b2ca3db965935929c4cfd9954c0ff339ffbeb0ef0bed27a00eb9a37b4c53b7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAttachedClusterErrorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1993afd0edbe0472d2c6fea96d2c1da0148165611749403df6113d9e17bd08f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAttachedClusterErrorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d98a82c855db7ac836b2374f72f83128affe47e91e242a6f8ee6aff387de7f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1f113c3dfea09d0a27292ac574fd809fdd7e0708b0a414469a901e415c30ce4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d361ffadffe331a5ea86bf14d4385270385bfdb9491f3b9d589391d0a13414f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ContainerAttachedClusterErrorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterErrorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0e73721a16a671a73348c4f5c5a4377a12d2c90b407de45d76e23fc55e6dbcc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAttachedClusterErrors]:
        return typing.cast(typing.Optional[ContainerAttachedClusterErrors], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAttachedClusterErrors],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5adcddb6b70e01128cfa8597da97b7742089a5386b76543b561224226360cd71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterFleet",
    jsii_struct_bases=[],
    name_mapping={"project": "project"},
)
class ContainerAttachedClusterFleet:
    def __init__(self, *, project: builtins.str) -> None:
        '''
        :param project: The number of the Fleet host project where this cluster will be registered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#project ContainerAttachedCluster#project}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7bd744d62b9a6ef16045fd118a3b77831ba94291e5841a0db21fc689b9327c3)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project": project,
        }

    @builtins.property
    def project(self) -> builtins.str:
        '''The number of the Fleet host project where this cluster will be registered.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#project ContainerAttachedCluster#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAttachedClusterFleet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAttachedClusterFleetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterFleetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdaf53b6ad0cd940c8c91297fed76e140bbec33ee66c6848a7e1c33c99a4a2e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a590bf076c0bcc39e176aebe22663c5f0ef466c1494c741c929be8983bdf91d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAttachedClusterFleet]:
        return typing.cast(typing.Optional[ContainerAttachedClusterFleet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAttachedClusterFleet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df4e7d7f8d01cb321b1a811fe6cff6bf3e52d1a2440a5a921da03239fff7246d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"component_config": "componentConfig"},
)
class ContainerAttachedClusterLoggingConfig:
    def __init__(
        self,
        *,
        component_config: typing.Optional[typing.Union["ContainerAttachedClusterLoggingConfigComponentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param component_config: component_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#component_config ContainerAttachedCluster#component_config}
        '''
        if isinstance(component_config, dict):
            component_config = ContainerAttachedClusterLoggingConfigComponentConfig(**component_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d885813ea1f2266f266beed44fdb7f0a6e8560714fa137222e6d23975368e8f3)
            check_type(argname="argument component_config", value=component_config, expected_type=type_hints["component_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if component_config is not None:
            self._values["component_config"] = component_config

    @builtins.property
    def component_config(
        self,
    ) -> typing.Optional["ContainerAttachedClusterLoggingConfigComponentConfig"]:
        '''component_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#component_config ContainerAttachedCluster#component_config}
        '''
        result = self._values.get("component_config")
        return typing.cast(typing.Optional["ContainerAttachedClusterLoggingConfigComponentConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAttachedClusterLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterLoggingConfigComponentConfig",
    jsii_struct_bases=[],
    name_mapping={"enable_components": "enableComponents"},
)
class ContainerAttachedClusterLoggingConfigComponentConfig:
    def __init__(
        self,
        *,
        enable_components: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enable_components: The components to be enabled. Possible values: ["SYSTEM_COMPONENTS", "WORKLOADS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#enable_components ContainerAttachedCluster#enable_components}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e9a2fda3d8cc3794544c251031b5ed432d5e2edc3c3a28fdd4e1ab4709484bd)
            check_type(argname="argument enable_components", value=enable_components, expected_type=type_hints["enable_components"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_components is not None:
            self._values["enable_components"] = enable_components

    @builtins.property
    def enable_components(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The components to be enabled. Possible values: ["SYSTEM_COMPONENTS", "WORKLOADS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#enable_components ContainerAttachedCluster#enable_components}
        '''
        result = self._values.get("enable_components")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAttachedClusterLoggingConfigComponentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAttachedClusterLoggingConfigComponentConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterLoggingConfigComponentConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42f3a788737bf40b6504ce226a976b2c16e7d7cb55879e4fa6e438a8e674a5e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableComponents")
    def reset_enable_components(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableComponents", []))

    @builtins.property
    @jsii.member(jsii_name="enableComponentsInput")
    def enable_components_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "enableComponentsInput"))

    @builtins.property
    @jsii.member(jsii_name="enableComponents")
    def enable_components(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "enableComponents"))

    @enable_components.setter
    def enable_components(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__551fae061ef96525f4bf246406f7120f8ce0edeac6cfa50ca8f6d5bf8cfb2d1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableComponents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAttachedClusterLoggingConfigComponentConfig]:
        return typing.cast(typing.Optional[ContainerAttachedClusterLoggingConfigComponentConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAttachedClusterLoggingConfigComponentConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60e79acb4e7da1c3dc51edf7b73ad3d7cef470dc1fd70a43904e2b2019deeb91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAttachedClusterLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9055b7c3d082cd9ea4ec54491299d0fdfd0e8b5cfbfe77c83ec5c7da629764d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putComponentConfig")
    def put_component_config(
        self,
        *,
        enable_components: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enable_components: The components to be enabled. Possible values: ["SYSTEM_COMPONENTS", "WORKLOADS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#enable_components ContainerAttachedCluster#enable_components}
        '''
        value = ContainerAttachedClusterLoggingConfigComponentConfig(
            enable_components=enable_components
        )

        return typing.cast(None, jsii.invoke(self, "putComponentConfig", [value]))

    @jsii.member(jsii_name="resetComponentConfig")
    def reset_component_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComponentConfig", []))

    @builtins.property
    @jsii.member(jsii_name="componentConfig")
    def component_config(
        self,
    ) -> ContainerAttachedClusterLoggingConfigComponentConfigOutputReference:
        return typing.cast(ContainerAttachedClusterLoggingConfigComponentConfigOutputReference, jsii.get(self, "componentConfig"))

    @builtins.property
    @jsii.member(jsii_name="componentConfigInput")
    def component_config_input(
        self,
    ) -> typing.Optional[ContainerAttachedClusterLoggingConfigComponentConfig]:
        return typing.cast(typing.Optional[ContainerAttachedClusterLoggingConfigComponentConfig], jsii.get(self, "componentConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAttachedClusterLoggingConfig]:
        return typing.cast(typing.Optional[ContainerAttachedClusterLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAttachedClusterLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b43dabc800aa254bb69baf52bb2770a15e71eeabd9615eb77a09270d7775e238)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterMonitoringConfig",
    jsii_struct_bases=[],
    name_mapping={"managed_prometheus_config": "managedPrometheusConfig"},
)
class ContainerAttachedClusterMonitoringConfig:
    def __init__(
        self,
        *,
        managed_prometheus_config: typing.Optional[typing.Union["ContainerAttachedClusterMonitoringConfigManagedPrometheusConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param managed_prometheus_config: managed_prometheus_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#managed_prometheus_config ContainerAttachedCluster#managed_prometheus_config}
        '''
        if isinstance(managed_prometheus_config, dict):
            managed_prometheus_config = ContainerAttachedClusterMonitoringConfigManagedPrometheusConfig(**managed_prometheus_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de9c9af2aac525ce6fd42ea8194540492da4866037141ff3c69314c6f23aa46d)
            check_type(argname="argument managed_prometheus_config", value=managed_prometheus_config, expected_type=type_hints["managed_prometheus_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if managed_prometheus_config is not None:
            self._values["managed_prometheus_config"] = managed_prometheus_config

    @builtins.property
    def managed_prometheus_config(
        self,
    ) -> typing.Optional["ContainerAttachedClusterMonitoringConfigManagedPrometheusConfig"]:
        '''managed_prometheus_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#managed_prometheus_config ContainerAttachedCluster#managed_prometheus_config}
        '''
        result = self._values.get("managed_prometheus_config")
        return typing.cast(typing.Optional["ContainerAttachedClusterMonitoringConfigManagedPrometheusConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAttachedClusterMonitoringConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterMonitoringConfigManagedPrometheusConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class ContainerAttachedClusterMonitoringConfigManagedPrometheusConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Enable Managed Collection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#enabled ContainerAttachedCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2878f2cfcea86046d53e1dcd7399e86fe77d27c6d4f6beb54de1cfa87127762e)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable Managed Collection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#enabled ContainerAttachedCluster#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAttachedClusterMonitoringConfigManagedPrometheusConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAttachedClusterMonitoringConfigManagedPrometheusConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterMonitoringConfigManagedPrometheusConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fa12f311a48782a3c2dba2751161bbb9e670a11f3c0269aed5a09bba2f210cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a3c9eb3154a51bb0f25c1179a530653b2510e38ec01141bd5ab4e34c3d6f5aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAttachedClusterMonitoringConfigManagedPrometheusConfig]:
        return typing.cast(typing.Optional[ContainerAttachedClusterMonitoringConfigManagedPrometheusConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAttachedClusterMonitoringConfigManagedPrometheusConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45a6fb84134a34fb0f7989b589a6eb9f4c94a8558e9cd96571af77ef774ce640)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAttachedClusterMonitoringConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterMonitoringConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1037d6e76fcbd10af991928076d65689f9a01d428fc5d73960514d907c530b7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putManagedPrometheusConfig")
    def put_managed_prometheus_config(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Enable Managed Collection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#enabled ContainerAttachedCluster#enabled}
        '''
        value = ContainerAttachedClusterMonitoringConfigManagedPrometheusConfig(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putManagedPrometheusConfig", [value]))

    @jsii.member(jsii_name="resetManagedPrometheusConfig")
    def reset_managed_prometheus_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedPrometheusConfig", []))

    @builtins.property
    @jsii.member(jsii_name="managedPrometheusConfig")
    def managed_prometheus_config(
        self,
    ) -> ContainerAttachedClusterMonitoringConfigManagedPrometheusConfigOutputReference:
        return typing.cast(ContainerAttachedClusterMonitoringConfigManagedPrometheusConfigOutputReference, jsii.get(self, "managedPrometheusConfig"))

    @builtins.property
    @jsii.member(jsii_name="managedPrometheusConfigInput")
    def managed_prometheus_config_input(
        self,
    ) -> typing.Optional[ContainerAttachedClusterMonitoringConfigManagedPrometheusConfig]:
        return typing.cast(typing.Optional[ContainerAttachedClusterMonitoringConfigManagedPrometheusConfig], jsii.get(self, "managedPrometheusConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAttachedClusterMonitoringConfig]:
        return typing.cast(typing.Optional[ContainerAttachedClusterMonitoringConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAttachedClusterMonitoringConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae1496864cb1091950734cb31e29e16e9615f46b581274e56b58399621b05917)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterOidcConfig",
    jsii_struct_bases=[],
    name_mapping={"issuer_url": "issuerUrl", "jwks": "jwks"},
)
class ContainerAttachedClusterOidcConfig:
    def __init__(
        self,
        *,
        issuer_url: builtins.str,
        jwks: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param issuer_url: A JSON Web Token (JWT) issuer URI. 'issuer' must start with 'https://'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#issuer_url ContainerAttachedCluster#issuer_url}
        :param jwks: OIDC verification keys in JWKS format (RFC 7517). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#jwks ContainerAttachedCluster#jwks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e627a7a13d8542be1454f37dfa9d155760e6978483eaac55b99e957c2682006)
            check_type(argname="argument issuer_url", value=issuer_url, expected_type=type_hints["issuer_url"])
            check_type(argname="argument jwks", value=jwks, expected_type=type_hints["jwks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "issuer_url": issuer_url,
        }
        if jwks is not None:
            self._values["jwks"] = jwks

    @builtins.property
    def issuer_url(self) -> builtins.str:
        '''A JSON Web Token (JWT) issuer URI. 'issuer' must start with 'https://'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#issuer_url ContainerAttachedCluster#issuer_url}
        '''
        result = self._values.get("issuer_url")
        assert result is not None, "Required property 'issuer_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def jwks(self) -> typing.Optional[builtins.str]:
        '''OIDC verification keys in JWKS format (RFC 7517).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#jwks ContainerAttachedCluster#jwks}
        '''
        result = self._values.get("jwks")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAttachedClusterOidcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAttachedClusterOidcConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterOidcConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1600bd9bd149c8948c097498c900ddf73648ac87045d9e043238b07aec0380d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetJwks")
    def reset_jwks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJwks", []))

    @builtins.property
    @jsii.member(jsii_name="issuerUrlInput")
    def issuer_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="jwksInput")
    def jwks_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jwksInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerUrl")
    def issuer_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerUrl"))

    @issuer_url.setter
    def issuer_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d8cfec1248a9bce0f5a1849f0abba7d801079bfe4c9ff849d435561aedee4f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jwks")
    def jwks(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jwks"))

    @jwks.setter
    def jwks(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c09d189a58e12a28674b3888fbd30536c6a62ff9e27dbd4c70c3cb83106c15ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAttachedClusterOidcConfig]:
        return typing.cast(typing.Optional[ContainerAttachedClusterOidcConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAttachedClusterOidcConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ca778bffc75e5a4a8ddcb588cb18c1f98a800061a4aa8e07c598f45d43d5b16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterProxyConfig",
    jsii_struct_bases=[],
    name_mapping={"kubernetes_secret": "kubernetesSecret"},
)
class ContainerAttachedClusterProxyConfig:
    def __init__(
        self,
        *,
        kubernetes_secret: typing.Optional[typing.Union["ContainerAttachedClusterProxyConfigKubernetesSecret", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param kubernetes_secret: kubernetes_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#kubernetes_secret ContainerAttachedCluster#kubernetes_secret}
        '''
        if isinstance(kubernetes_secret, dict):
            kubernetes_secret = ContainerAttachedClusterProxyConfigKubernetesSecret(**kubernetes_secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2034ccef64bc9b3238642dc86011a31feebdd5c3c210422f5fc63ffb1ce1f328)
            check_type(argname="argument kubernetes_secret", value=kubernetes_secret, expected_type=type_hints["kubernetes_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kubernetes_secret is not None:
            self._values["kubernetes_secret"] = kubernetes_secret

    @builtins.property
    def kubernetes_secret(
        self,
    ) -> typing.Optional["ContainerAttachedClusterProxyConfigKubernetesSecret"]:
        '''kubernetes_secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#kubernetes_secret ContainerAttachedCluster#kubernetes_secret}
        '''
        result = self._values.get("kubernetes_secret")
        return typing.cast(typing.Optional["ContainerAttachedClusterProxyConfigKubernetesSecret"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAttachedClusterProxyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterProxyConfigKubernetesSecret",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "namespace": "namespace"},
)
class ContainerAttachedClusterProxyConfigKubernetesSecret:
    def __init__(self, *, name: builtins.str, namespace: builtins.str) -> None:
        '''
        :param name: Name of the kubernetes secret containing the proxy config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#name ContainerAttachedCluster#name}
        :param namespace: Namespace of the kubernetes secret containing the proxy config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#namespace ContainerAttachedCluster#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f664f10e2daea050cce544474e4a214a87032c0683bd5a89cbd945e4985685e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "namespace": namespace,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the kubernetes secret containing the proxy config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#name ContainerAttachedCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> builtins.str:
        '''Namespace of the kubernetes secret containing the proxy config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#namespace ContainerAttachedCluster#namespace}
        '''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAttachedClusterProxyConfigKubernetesSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAttachedClusterProxyConfigKubernetesSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterProxyConfigKubernetesSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db811b47aa587fbd99aae05d378b9a27e334631b51cf07a29992ec595d3f7dfb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d2437a8325a00eee71bae8b7ecf32515146cfd0362cd48a3ccbaad6fe89e4d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0428a377aed25ff9a7ce4a2c8033da43fc9015670d8654cee62befe9e1b2e652)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAttachedClusterProxyConfigKubernetesSecret]:
        return typing.cast(typing.Optional[ContainerAttachedClusterProxyConfigKubernetesSecret], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAttachedClusterProxyConfigKubernetesSecret],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b44fec8b8c34c938c274e73a40a5a4b8a25dadfbceb2a25294fe6a7beef13eff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAttachedClusterProxyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterProxyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f3cae3f4558d0d26a10811f26edf33dcf620831068c5b8c7f19e6c725f7b0fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putKubernetesSecret")
    def put_kubernetes_secret(
        self,
        *,
        name: builtins.str,
        namespace: builtins.str,
    ) -> None:
        '''
        :param name: Name of the kubernetes secret containing the proxy config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#name ContainerAttachedCluster#name}
        :param namespace: Namespace of the kubernetes secret containing the proxy config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#namespace ContainerAttachedCluster#namespace}
        '''
        value = ContainerAttachedClusterProxyConfigKubernetesSecret(
            name=name, namespace=namespace
        )

        return typing.cast(None, jsii.invoke(self, "putKubernetesSecret", [value]))

    @jsii.member(jsii_name="resetKubernetesSecret")
    def reset_kubernetes_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubernetesSecret", []))

    @builtins.property
    @jsii.member(jsii_name="kubernetesSecret")
    def kubernetes_secret(
        self,
    ) -> ContainerAttachedClusterProxyConfigKubernetesSecretOutputReference:
        return typing.cast(ContainerAttachedClusterProxyConfigKubernetesSecretOutputReference, jsii.get(self, "kubernetesSecret"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesSecretInput")
    def kubernetes_secret_input(
        self,
    ) -> typing.Optional[ContainerAttachedClusterProxyConfigKubernetesSecret]:
        return typing.cast(typing.Optional[ContainerAttachedClusterProxyConfigKubernetesSecret], jsii.get(self, "kubernetesSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAttachedClusterProxyConfig]:
        return typing.cast(typing.Optional[ContainerAttachedClusterProxyConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAttachedClusterProxyConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55e6a3d3a028722ed839b7131a56d14861372be4064b65e75b00fdf4cd312f9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterSecurityPostureConfig",
    jsii_struct_bases=[],
    name_mapping={"vulnerability_mode": "vulnerabilityMode"},
)
class ContainerAttachedClusterSecurityPostureConfig:
    def __init__(self, *, vulnerability_mode: builtins.str) -> None:
        '''
        :param vulnerability_mode: Sets the mode of the Kubernetes security posture API's workload vulnerability scanning. Possible values: ["VULNERABILITY_DISABLED", "VULNERABILITY_ENTERPRISE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#vulnerability_mode ContainerAttachedCluster#vulnerability_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94c359ab9fbac31cb18a597c667a9f061075e38800f0ac4c2d1c6cf2f88c7bcf)
            check_type(argname="argument vulnerability_mode", value=vulnerability_mode, expected_type=type_hints["vulnerability_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vulnerability_mode": vulnerability_mode,
        }

    @builtins.property
    def vulnerability_mode(self) -> builtins.str:
        '''Sets the mode of the Kubernetes security posture API's workload vulnerability scanning. Possible values: ["VULNERABILITY_DISABLED", "VULNERABILITY_ENTERPRISE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#vulnerability_mode ContainerAttachedCluster#vulnerability_mode}
        '''
        result = self._values.get("vulnerability_mode")
        assert result is not None, "Required property 'vulnerability_mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAttachedClusterSecurityPostureConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAttachedClusterSecurityPostureConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterSecurityPostureConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea778113a25b14593e99b7cda4cf43004a1b2ea7fc8152d4aa363c3ed9c8fe6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="vulnerabilityModeInput")
    def vulnerability_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vulnerabilityModeInput"))

    @builtins.property
    @jsii.member(jsii_name="vulnerabilityMode")
    def vulnerability_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vulnerabilityMode"))

    @vulnerability_mode.setter
    def vulnerability_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9573496fa5346a58e1cddc51d28d590fd935323d18e308c729a175d8b7dfa1ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vulnerabilityMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAttachedClusterSecurityPostureConfig]:
        return typing.cast(typing.Optional[ContainerAttachedClusterSecurityPostureConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAttachedClusterSecurityPostureConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3af4f0dd1702ff635c85fc904996f1abff165dc2075d362fa22bed105ba09e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ContainerAttachedClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#create ContainerAttachedCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#delete ContainerAttachedCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#update ContainerAttachedCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ea25963ea57429533019de34755d82f633aa4f62be71528cf4ddb1c82d536c8)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#create ContainerAttachedCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#delete ContainerAttachedCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_attached_cluster#update ContainerAttachedCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAttachedClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAttachedClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9abcca9af95ea7a9aa6a3152b609b4b75fe4cdd226e62a4269e928b2d1a134cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71983da0350b25858edccd8996689e844529dae65943feb89c19b529ac63aa70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0c4ad43e0326a049f80ab111b0d2bfdb2777f1764edc7fd19633a842e9a9696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f574fc66845a88d85df06adeab55b6135c3cb26394e3b898d3f28a582c22bded)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAttachedClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAttachedClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAttachedClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b26cfaf6aa588f886923febd13141dffd048841b87ac26cc5af159544b315ad2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterWorkloadIdentityConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class ContainerAttachedClusterWorkloadIdentityConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAttachedClusterWorkloadIdentityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAttachedClusterWorkloadIdentityConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterWorkloadIdentityConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb0fe40eaddd5995292788a4422247c85f1695577568e94cf1e7394b22f19028)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAttachedClusterWorkloadIdentityConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93c1aabde6b26749268d85d099241a92056138bd9685e69b32944e6beea74256)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAttachedClusterWorkloadIdentityConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81ed12562171635b31e78b5eeb802e915408e24ad937a654753336b3b0a039d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fe994b53aa226dc370981b6a9bb4c477ec7daff500b4000b8e1ae36c52dd687)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb7629e6ba1a435ddbdea84354bdbaec303fdb98ecee15bc22d189bf7c2adfba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ContainerAttachedClusterWorkloadIdentityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAttachedCluster.ContainerAttachedClusterWorkloadIdentityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4ece429308a501ab0905fb528f2c54dfa9caed54311c348a96d911b96efd7da)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="identityProvider")
    def identity_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityProvider"))

    @builtins.property
    @jsii.member(jsii_name="issuerUri")
    def issuer_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerUri"))

    @builtins.property
    @jsii.member(jsii_name="workloadPool")
    def workload_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workloadPool"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAttachedClusterWorkloadIdentityConfig]:
        return typing.cast(typing.Optional[ContainerAttachedClusterWorkloadIdentityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAttachedClusterWorkloadIdentityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2cce947e4d70a62aaf9cc64ad6eb9b4a9d65a5735f47b950398ea70eebcbd14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ContainerAttachedCluster",
    "ContainerAttachedClusterAuthorization",
    "ContainerAttachedClusterAuthorizationOutputReference",
    "ContainerAttachedClusterBinaryAuthorization",
    "ContainerAttachedClusterBinaryAuthorizationOutputReference",
    "ContainerAttachedClusterConfig",
    "ContainerAttachedClusterErrors",
    "ContainerAttachedClusterErrorsList",
    "ContainerAttachedClusterErrorsOutputReference",
    "ContainerAttachedClusterFleet",
    "ContainerAttachedClusterFleetOutputReference",
    "ContainerAttachedClusterLoggingConfig",
    "ContainerAttachedClusterLoggingConfigComponentConfig",
    "ContainerAttachedClusterLoggingConfigComponentConfigOutputReference",
    "ContainerAttachedClusterLoggingConfigOutputReference",
    "ContainerAttachedClusterMonitoringConfig",
    "ContainerAttachedClusterMonitoringConfigManagedPrometheusConfig",
    "ContainerAttachedClusterMonitoringConfigManagedPrometheusConfigOutputReference",
    "ContainerAttachedClusterMonitoringConfigOutputReference",
    "ContainerAttachedClusterOidcConfig",
    "ContainerAttachedClusterOidcConfigOutputReference",
    "ContainerAttachedClusterProxyConfig",
    "ContainerAttachedClusterProxyConfigKubernetesSecret",
    "ContainerAttachedClusterProxyConfigKubernetesSecretOutputReference",
    "ContainerAttachedClusterProxyConfigOutputReference",
    "ContainerAttachedClusterSecurityPostureConfig",
    "ContainerAttachedClusterSecurityPostureConfigOutputReference",
    "ContainerAttachedClusterTimeouts",
    "ContainerAttachedClusterTimeoutsOutputReference",
    "ContainerAttachedClusterWorkloadIdentityConfig",
    "ContainerAttachedClusterWorkloadIdentityConfigList",
    "ContainerAttachedClusterWorkloadIdentityConfigOutputReference",
]

publication.publish()

def _typecheckingstub__8020a75e6ece36ba51905b5e491fd97b4a3c3ba930d1537b8fc78f6d3ca7e639(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    distribution: builtins.str,
    fleet: typing.Union[ContainerAttachedClusterFleet, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    oidc_config: typing.Union[ContainerAttachedClusterOidcConfig, typing.Dict[builtins.str, typing.Any]],
    platform_version: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    authorization: typing.Optional[typing.Union[ContainerAttachedClusterAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    binary_authorization: typing.Optional[typing.Union[ContainerAttachedClusterBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_policy: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    logging_config: typing.Optional[typing.Union[ContainerAttachedClusterLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    monitoring_config: typing.Optional[typing.Union[ContainerAttachedClusterMonitoringConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    proxy_config: typing.Optional[typing.Union[ContainerAttachedClusterProxyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    security_posture_config: typing.Optional[typing.Union[ContainerAttachedClusterSecurityPostureConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ContainerAttachedClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8ed214955aeca4d16affe1f14262f54fb9fbb002558a389542296d56426d1808(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5510a81fd4933d0778b7b6b54b095654bfba12364969d3d7b5349bf427bd00d9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__006e4236961c6137a52a1d08c01fbec2d576de77a209c6ac42831ad3fdd57fe1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8b8e083ccbd07ed32c3d1182f13772d0a2a64749337e13e7c5123dc158c1774(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b48ce1d564311c5f2a76a3e2c824786da658e35be84a68c995327c22a117405(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c7a7be5de943fe315eccb8d966ac214e7b729e38d09c575b6a43ee18054d86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e3df3c7dee3be5a589591de1ccafda3cb99a57f1f12318fe418f64d3995eb88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc46355f0f5d047122b16912045b608b7cfe60cb999517a31c6bf5113eb0a904(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4fae87080dea04f20d7e3da67151fc8848105852cfdc8f37faf8ade0cee6780(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dffc16efe720f04be0e0491ec16221348d929d4b7a7eef92e653b1316cc443bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80f99900324de47d090408cec3c25daed41224e0a6a11a5bae0021b86335e0a6(
    *,
    admin_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    admin_users: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66e926f078a4989d43de33833e60e728853f71853ed15e5e16d4bed689141d87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0089812f2a89fcb22ccc3a3f168b01d63e50dc3f19a27fb21518edd6532ded83(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd8c26be379d803668dc0a3d3663b7c65382964d427020bcfc4b47db2bce48fd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d1d429a9098733d9ffb39a3c52730ca1a41838d7271f1065d8ec9c46a48dc72(
    value: typing.Optional[ContainerAttachedClusterAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a46a44887952d85ec3adcdc990e3ba002d8cbe7e342d516f6a47a2b1a24d78(
    *,
    evaluation_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed4b92e0b7fd23d98def456413bec8c9250a91d66e7774bd9ba9c2cdf5769d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35995794b6e48bff9560e8316b74a7af6b39494a63e5463a2528172d1e0e359e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c8447a42d39559989702685a65094f978f931d84212db24356719c75154bc0d(
    value: typing.Optional[ContainerAttachedClusterBinaryAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ab3374d43c9b669abe5973dbe2e073b60745b3c780a0ccb12b19238a7eebad(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    distribution: builtins.str,
    fleet: typing.Union[ContainerAttachedClusterFleet, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    oidc_config: typing.Union[ContainerAttachedClusterOidcConfig, typing.Dict[builtins.str, typing.Any]],
    platform_version: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    authorization: typing.Optional[typing.Union[ContainerAttachedClusterAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    binary_authorization: typing.Optional[typing.Union[ContainerAttachedClusterBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_policy: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    logging_config: typing.Optional[typing.Union[ContainerAttachedClusterLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    monitoring_config: typing.Optional[typing.Union[ContainerAttachedClusterMonitoringConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    proxy_config: typing.Optional[typing.Union[ContainerAttachedClusterProxyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    security_posture_config: typing.Optional[typing.Union[ContainerAttachedClusterSecurityPostureConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ContainerAttachedClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b2ca3db965935929c4cfd9954c0ff339ffbeb0ef0bed27a00eb9a37b4c53b7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1993afd0edbe0472d2c6fea96d2c1da0148165611749403df6113d9e17bd08f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d98a82c855db7ac836b2374f72f83128affe47e91e242a6f8ee6aff387de7f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1f113c3dfea09d0a27292ac574fd809fdd7e0708b0a414469a901e415c30ce4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d361ffadffe331a5ea86bf14d4385270385bfdb9491f3b9d589391d0a13414f0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0e73721a16a671a73348c4f5c5a4377a12d2c90b407de45d76e23fc55e6dbcc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5adcddb6b70e01128cfa8597da97b7742089a5386b76543b561224226360cd71(
    value: typing.Optional[ContainerAttachedClusterErrors],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7bd744d62b9a6ef16045fd118a3b77831ba94291e5841a0db21fc689b9327c3(
    *,
    project: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdaf53b6ad0cd940c8c91297fed76e140bbec33ee66c6848a7e1c33c99a4a2e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a590bf076c0bcc39e176aebe22663c5f0ef466c1494c741c929be8983bdf91d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df4e7d7f8d01cb321b1a811fe6cff6bf3e52d1a2440a5a921da03239fff7246d(
    value: typing.Optional[ContainerAttachedClusterFleet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d885813ea1f2266f266beed44fdb7f0a6e8560714fa137222e6d23975368e8f3(
    *,
    component_config: typing.Optional[typing.Union[ContainerAttachedClusterLoggingConfigComponentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e9a2fda3d8cc3794544c251031b5ed432d5e2edc3c3a28fdd4e1ab4709484bd(
    *,
    enable_components: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f3a788737bf40b6504ce226a976b2c16e7d7cb55879e4fa6e438a8e674a5e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__551fae061ef96525f4bf246406f7120f8ce0edeac6cfa50ca8f6d5bf8cfb2d1f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e79acb4e7da1c3dc51edf7b73ad3d7cef470dc1fd70a43904e2b2019deeb91(
    value: typing.Optional[ContainerAttachedClusterLoggingConfigComponentConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9055b7c3d082cd9ea4ec54491299d0fdfd0e8b5cfbfe77c83ec5c7da629764d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43dabc800aa254bb69baf52bb2770a15e71eeabd9615eb77a09270d7775e238(
    value: typing.Optional[ContainerAttachedClusterLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de9c9af2aac525ce6fd42ea8194540492da4866037141ff3c69314c6f23aa46d(
    *,
    managed_prometheus_config: typing.Optional[typing.Union[ContainerAttachedClusterMonitoringConfigManagedPrometheusConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2878f2cfcea86046d53e1dcd7399e86fe77d27c6d4f6beb54de1cfa87127762e(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa12f311a48782a3c2dba2751161bbb9e670a11f3c0269aed5a09bba2f210cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a3c9eb3154a51bb0f25c1179a530653b2510e38ec01141bd5ab4e34c3d6f5aa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a6fb84134a34fb0f7989b589a6eb9f4c94a8558e9cd96571af77ef774ce640(
    value: typing.Optional[ContainerAttachedClusterMonitoringConfigManagedPrometheusConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1037d6e76fcbd10af991928076d65689f9a01d428fc5d73960514d907c530b7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae1496864cb1091950734cb31e29e16e9615f46b581274e56b58399621b05917(
    value: typing.Optional[ContainerAttachedClusterMonitoringConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e627a7a13d8542be1454f37dfa9d155760e6978483eaac55b99e957c2682006(
    *,
    issuer_url: builtins.str,
    jwks: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1600bd9bd149c8948c097498c900ddf73648ac87045d9e043238b07aec0380d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d8cfec1248a9bce0f5a1849f0abba7d801079bfe4c9ff849d435561aedee4f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c09d189a58e12a28674b3888fbd30536c6a62ff9e27dbd4c70c3cb83106c15ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca778bffc75e5a4a8ddcb588cb18c1f98a800061a4aa8e07c598f45d43d5b16(
    value: typing.Optional[ContainerAttachedClusterOidcConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2034ccef64bc9b3238642dc86011a31feebdd5c3c210422f5fc63ffb1ce1f328(
    *,
    kubernetes_secret: typing.Optional[typing.Union[ContainerAttachedClusterProxyConfigKubernetesSecret, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f664f10e2daea050cce544474e4a214a87032c0683bd5a89cbd945e4985685e(
    *,
    name: builtins.str,
    namespace: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db811b47aa587fbd99aae05d378b9a27e334631b51cf07a29992ec595d3f7dfb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d2437a8325a00eee71bae8b7ecf32515146cfd0362cd48a3ccbaad6fe89e4d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0428a377aed25ff9a7ce4a2c8033da43fc9015670d8654cee62befe9e1b2e652(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b44fec8b8c34c938c274e73a40a5a4b8a25dadfbceb2a25294fe6a7beef13eff(
    value: typing.Optional[ContainerAttachedClusterProxyConfigKubernetesSecret],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f3cae3f4558d0d26a10811f26edf33dcf620831068c5b8c7f19e6c725f7b0fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e6a3d3a028722ed839b7131a56d14861372be4064b65e75b00fdf4cd312f9e(
    value: typing.Optional[ContainerAttachedClusterProxyConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94c359ab9fbac31cb18a597c667a9f061075e38800f0ac4c2d1c6cf2f88c7bcf(
    *,
    vulnerability_mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea778113a25b14593e99b7cda4cf43004a1b2ea7fc8152d4aa363c3ed9c8fe6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9573496fa5346a58e1cddc51d28d590fd935323d18e308c729a175d8b7dfa1ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3af4f0dd1702ff635c85fc904996f1abff165dc2075d362fa22bed105ba09e1(
    value: typing.Optional[ContainerAttachedClusterSecurityPostureConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ea25963ea57429533019de34755d82f633aa4f62be71528cf4ddb1c82d536c8(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9abcca9af95ea7a9aa6a3152b609b4b75fe4cdd226e62a4269e928b2d1a134cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71983da0350b25858edccd8996689e844529dae65943feb89c19b529ac63aa70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c4ad43e0326a049f80ab111b0d2bfdb2777f1764edc7fd19633a842e9a9696(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f574fc66845a88d85df06adeab55b6135c3cb26394e3b898d3f28a582c22bded(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b26cfaf6aa588f886923febd13141dffd048841b87ac26cc5af159544b315ad2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAttachedClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0fe40eaddd5995292788a4422247c85f1695577568e94cf1e7394b22f19028(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93c1aabde6b26749268d85d099241a92056138bd9685e69b32944e6beea74256(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81ed12562171635b31e78b5eeb802e915408e24ad937a654753336b3b0a039d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe994b53aa226dc370981b6a9bb4c477ec7daff500b4000b8e1ae36c52dd687(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb7629e6ba1a435ddbdea84354bdbaec303fdb98ecee15bc22d189bf7c2adfba(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4ece429308a501ab0905fb528f2c54dfa9caed54311c348a96d911b96efd7da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2cce947e4d70a62aaf9cc64ad6eb9b4a9d65a5735f47b950398ea70eebcbd14(
    value: typing.Optional[ContainerAttachedClusterWorkloadIdentityConfig],
) -> None:
    """Type checking stubs"""
    pass
