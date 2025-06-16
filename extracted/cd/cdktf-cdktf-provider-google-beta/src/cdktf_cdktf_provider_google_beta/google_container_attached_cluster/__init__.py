r'''
# `google_container_attached_cluster`

Refer to the Terraform Registry for docs: [`google_container_attached_cluster`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster).
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


class GoogleContainerAttachedCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster google_container_attached_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        distribution: builtins.str,
        fleet: typing.Union["GoogleContainerAttachedClusterFleet", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        oidc_config: typing.Union["GoogleContainerAttachedClusterOidcConfig", typing.Dict[builtins.str, typing.Any]],
        platform_version: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        authorization: typing.Optional[typing.Union["GoogleContainerAttachedClusterAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
        binary_authorization: typing.Optional[typing.Union["GoogleContainerAttachedClusterBinaryAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_policy: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union["GoogleContainerAttachedClusterLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        monitoring_config: typing.Optional[typing.Union["GoogleContainerAttachedClusterMonitoringConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        proxy_config: typing.Optional[typing.Union["GoogleContainerAttachedClusterProxyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        security_posture_config: typing.Optional[typing.Union["GoogleContainerAttachedClusterSecurityPostureConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleContainerAttachedClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster google_container_attached_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param distribution: The Kubernetes distribution of the underlying attached cluster. Supported values: "eks", "aks", "generic". The generic distribution provides the ability to register or migrate any CNCF conformant cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#distribution GoogleContainerAttachedCluster#distribution}
        :param fleet: fleet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#fleet GoogleContainerAttachedCluster#fleet}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#location GoogleContainerAttachedCluster#location}
        :param name: The name of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#name GoogleContainerAttachedCluster#name}
        :param oidc_config: oidc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#oidc_config GoogleContainerAttachedCluster#oidc_config}
        :param platform_version: The platform version for the cluster (e.g. '1.23.0-gke.1'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#platform_version GoogleContainerAttachedCluster#platform_version}
        :param annotations: Optional. Annotations on the cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#annotations GoogleContainerAttachedCluster#annotations}
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#authorization GoogleContainerAttachedCluster#authorization}
        :param binary_authorization: binary_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#binary_authorization GoogleContainerAttachedCluster#binary_authorization}
        :param deletion_policy: Policy to determine what flags to send on delete. Possible values: DELETE, DELETE_IGNORE_ERRORS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#deletion_policy GoogleContainerAttachedCluster#deletion_policy}
        :param description: A human readable description of this attached cluster. Cannot be longer than 255 UTF-8 encoded bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#description GoogleContainerAttachedCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#id GoogleContainerAttachedCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#logging_config GoogleContainerAttachedCluster#logging_config}
        :param monitoring_config: monitoring_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#monitoring_config GoogleContainerAttachedCluster#monitoring_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#project GoogleContainerAttachedCluster#project}.
        :param proxy_config: proxy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#proxy_config GoogleContainerAttachedCluster#proxy_config}
        :param security_posture_config: security_posture_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#security_posture_config GoogleContainerAttachedCluster#security_posture_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#timeouts GoogleContainerAttachedCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b77a9eb206309da5d06344a29351268d5b6f5fbdc80e2c8468c2dc94d1baabb5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleContainerAttachedClusterConfig(
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
        '''Generates CDKTF code for importing a GoogleContainerAttachedCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleContainerAttachedCluster to import.
        :param import_from_id: The id of the existing GoogleContainerAttachedCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleContainerAttachedCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a38145bf831926872df598ef994725bf3891ce3df81039e3c524f2868a8ab07)
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
        :param admin_groups: Groups that can perform operations as a cluster admin. A managed ClusterRoleBinding will be created to grant the 'cluster-admin' ClusterRole to the groups. Up to ten admin groups can be provided. For more info on RBAC, see https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#admin_groups GoogleContainerAttachedCluster#admin_groups}
        :param admin_users: Users that can perform operations as a cluster admin. A managed ClusterRoleBinding will be created to grant the 'cluster-admin' ClusterRole to the users. Up to ten admin users can be provided. For more info on RBAC, see https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#admin_users GoogleContainerAttachedCluster#admin_users}
        '''
        value = GoogleContainerAttachedClusterAuthorization(
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
        :param evaluation_mode: Configure Binary Authorization evaluation mode. Possible values: ["DISABLED", "PROJECT_SINGLETON_POLICY_ENFORCE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#evaluation_mode GoogleContainerAttachedCluster#evaluation_mode}
        '''
        value = GoogleContainerAttachedClusterBinaryAuthorization(
            evaluation_mode=evaluation_mode
        )

        return typing.cast(None, jsii.invoke(self, "putBinaryAuthorization", [value]))

    @jsii.member(jsii_name="putFleet")
    def put_fleet(self, *, project: builtins.str) -> None:
        '''
        :param project: The number of the Fleet host project where this cluster will be registered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#project GoogleContainerAttachedCluster#project}
        '''
        value = GoogleContainerAttachedClusterFleet(project=project)

        return typing.cast(None, jsii.invoke(self, "putFleet", [value]))

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        component_config: typing.Optional[typing.Union["GoogleContainerAttachedClusterLoggingConfigComponentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param component_config: component_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#component_config GoogleContainerAttachedCluster#component_config}
        '''
        value = GoogleContainerAttachedClusterLoggingConfig(
            component_config=component_config
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

    @jsii.member(jsii_name="putMonitoringConfig")
    def put_monitoring_config(
        self,
        *,
        managed_prometheus_config: typing.Optional[typing.Union["GoogleContainerAttachedClusterMonitoringConfigManagedPrometheusConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param managed_prometheus_config: managed_prometheus_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#managed_prometheus_config GoogleContainerAttachedCluster#managed_prometheus_config}
        '''
        value = GoogleContainerAttachedClusterMonitoringConfig(
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
        :param issuer_url: A JSON Web Token (JWT) issuer URI. 'issuer' must start with 'https://'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#issuer_url GoogleContainerAttachedCluster#issuer_url}
        :param jwks: OIDC verification keys in JWKS format (RFC 7517). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#jwks GoogleContainerAttachedCluster#jwks}
        '''
        value = GoogleContainerAttachedClusterOidcConfig(
            issuer_url=issuer_url, jwks=jwks
        )

        return typing.cast(None, jsii.invoke(self, "putOidcConfig", [value]))

    @jsii.member(jsii_name="putProxyConfig")
    def put_proxy_config(
        self,
        *,
        kubernetes_secret: typing.Optional[typing.Union["GoogleContainerAttachedClusterProxyConfigKubernetesSecret", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param kubernetes_secret: kubernetes_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#kubernetes_secret GoogleContainerAttachedCluster#kubernetes_secret}
        '''
        value = GoogleContainerAttachedClusterProxyConfig(
            kubernetes_secret=kubernetes_secret
        )

        return typing.cast(None, jsii.invoke(self, "putProxyConfig", [value]))

    @jsii.member(jsii_name="putSecurityPostureConfig")
    def put_security_posture_config(self, *, vulnerability_mode: builtins.str) -> None:
        '''
        :param vulnerability_mode: Sets the mode of the Kubernetes security posture API's workload vulnerability scanning. Possible values: ["VULNERABILITY_DISABLED", "VULNERABILITY_ENTERPRISE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#vulnerability_mode GoogleContainerAttachedCluster#vulnerability_mode}
        '''
        value = GoogleContainerAttachedClusterSecurityPostureConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#create GoogleContainerAttachedCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#delete GoogleContainerAttachedCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#update GoogleContainerAttachedCluster#update}.
        '''
        value = GoogleContainerAttachedClusterTimeouts(
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
    def authorization(
        self,
    ) -> "GoogleContainerAttachedClusterAuthorizationOutputReference":
        return typing.cast("GoogleContainerAttachedClusterAuthorizationOutputReference", jsii.get(self, "authorization"))

    @builtins.property
    @jsii.member(jsii_name="binaryAuthorization")
    def binary_authorization(
        self,
    ) -> "GoogleContainerAttachedClusterBinaryAuthorizationOutputReference":
        return typing.cast("GoogleContainerAttachedClusterBinaryAuthorizationOutputReference", jsii.get(self, "binaryAuthorization"))

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
    def errors(self) -> "GoogleContainerAttachedClusterErrorsList":
        return typing.cast("GoogleContainerAttachedClusterErrorsList", jsii.get(self, "errors"))

    @builtins.property
    @jsii.member(jsii_name="fleet")
    def fleet(self) -> "GoogleContainerAttachedClusterFleetOutputReference":
        return typing.cast("GoogleContainerAttachedClusterFleetOutputReference", jsii.get(self, "fleet"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesVersion")
    def kubernetes_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesVersion"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(
        self,
    ) -> "GoogleContainerAttachedClusterLoggingConfigOutputReference":
        return typing.cast("GoogleContainerAttachedClusterLoggingConfigOutputReference", jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="monitoringConfig")
    def monitoring_config(
        self,
    ) -> "GoogleContainerAttachedClusterMonitoringConfigOutputReference":
        return typing.cast("GoogleContainerAttachedClusterMonitoringConfigOutputReference", jsii.get(self, "monitoringConfig"))

    @builtins.property
    @jsii.member(jsii_name="oidcConfig")
    def oidc_config(self) -> "GoogleContainerAttachedClusterOidcConfigOutputReference":
        return typing.cast("GoogleContainerAttachedClusterOidcConfigOutputReference", jsii.get(self, "oidcConfig"))

    @builtins.property
    @jsii.member(jsii_name="proxyConfig")
    def proxy_config(
        self,
    ) -> "GoogleContainerAttachedClusterProxyConfigOutputReference":
        return typing.cast("GoogleContainerAttachedClusterProxyConfigOutputReference", jsii.get(self, "proxyConfig"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="securityPostureConfig")
    def security_posture_config(
        self,
    ) -> "GoogleContainerAttachedClusterSecurityPostureConfigOutputReference":
        return typing.cast("GoogleContainerAttachedClusterSecurityPostureConfigOutputReference", jsii.get(self, "securityPostureConfig"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleContainerAttachedClusterTimeoutsOutputReference":
        return typing.cast("GoogleContainerAttachedClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> "GoogleContainerAttachedClusterWorkloadIdentityConfigList":
        return typing.cast("GoogleContainerAttachedClusterWorkloadIdentityConfigList", jsii.get(self, "workloadIdentityConfig"))

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
    ) -> typing.Optional["GoogleContainerAttachedClusterAuthorization"]:
        return typing.cast(typing.Optional["GoogleContainerAttachedClusterAuthorization"], jsii.get(self, "authorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="binaryAuthorizationInput")
    def binary_authorization_input(
        self,
    ) -> typing.Optional["GoogleContainerAttachedClusterBinaryAuthorization"]:
        return typing.cast(typing.Optional["GoogleContainerAttachedClusterBinaryAuthorization"], jsii.get(self, "binaryAuthorizationInput"))

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
    def fleet_input(self) -> typing.Optional["GoogleContainerAttachedClusterFleet"]:
        return typing.cast(typing.Optional["GoogleContainerAttachedClusterFleet"], jsii.get(self, "fleetInput"))

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
    ) -> typing.Optional["GoogleContainerAttachedClusterLoggingConfig"]:
        return typing.cast(typing.Optional["GoogleContainerAttachedClusterLoggingConfig"], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="monitoringConfigInput")
    def monitoring_config_input(
        self,
    ) -> typing.Optional["GoogleContainerAttachedClusterMonitoringConfig"]:
        return typing.cast(typing.Optional["GoogleContainerAttachedClusterMonitoringConfig"], jsii.get(self, "monitoringConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="oidcConfigInput")
    def oidc_config_input(
        self,
    ) -> typing.Optional["GoogleContainerAttachedClusterOidcConfig"]:
        return typing.cast(typing.Optional["GoogleContainerAttachedClusterOidcConfig"], jsii.get(self, "oidcConfigInput"))

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
    ) -> typing.Optional["GoogleContainerAttachedClusterProxyConfig"]:
        return typing.cast(typing.Optional["GoogleContainerAttachedClusterProxyConfig"], jsii.get(self, "proxyConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="securityPostureConfigInput")
    def security_posture_config_input(
        self,
    ) -> typing.Optional["GoogleContainerAttachedClusterSecurityPostureConfig"]:
        return typing.cast(typing.Optional["GoogleContainerAttachedClusterSecurityPostureConfig"], jsii.get(self, "securityPostureConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleContainerAttachedClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleContainerAttachedClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fbd2abb4607d49701d6a0e6f72bde2e838cb71f5b1e2eff9cd52fbc3c50c6ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionPolicy")
    def deletion_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deletionPolicy"))

    @deletion_policy.setter
    def deletion_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3bb226562d99eaf062c1ae32c048d878281d0c2b8eb85f6e470f40b1ce1770f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0eb432c6775424af3ece3b351e1f53b4dba49d2292bf1136b8c445a3e68f408)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="distribution")
    def distribution(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "distribution"))

    @distribution.setter
    def distribution(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21128f12a7858d2f0d9880190ec05762ed842a1446a11e668fa2642b752e52fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distribution", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__032fd87a0bbe562dd265eaa3646b4e561597c4127b7da6989b123ad1b84cec8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5defe3e2fbabf058bf7168329a73db28284205ffde3b20f7220fd539909fa9be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87125695ebc47577beca4fc4eec6c379133fa9c537b86924e1b899229a9c640b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="platformVersion")
    def platform_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platformVersion"))

    @platform_version.setter
    def platform_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5aeb905c2522cc56beb74c951c57a1e564bb72ac179d3b2fe113a561c866a42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platformVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579091bff89141db51175dcb699ba144ee89627df1f261e866ca914908dd9a75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterAuthorization",
    jsii_struct_bases=[],
    name_mapping={"admin_groups": "adminGroups", "admin_users": "adminUsers"},
)
class GoogleContainerAttachedClusterAuthorization:
    def __init__(
        self,
        *,
        admin_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        admin_users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param admin_groups: Groups that can perform operations as a cluster admin. A managed ClusterRoleBinding will be created to grant the 'cluster-admin' ClusterRole to the groups. Up to ten admin groups can be provided. For more info on RBAC, see https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#admin_groups GoogleContainerAttachedCluster#admin_groups}
        :param admin_users: Users that can perform operations as a cluster admin. A managed ClusterRoleBinding will be created to grant the 'cluster-admin' ClusterRole to the users. Up to ten admin users can be provided. For more info on RBAC, see https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#admin_users GoogleContainerAttachedCluster#admin_users}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51b93b324ee95f41690dd7f1bf7b6c9f15a58184219b419cfd6e0e1b7a2e249b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#admin_groups GoogleContainerAttachedCluster#admin_groups}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#admin_users GoogleContainerAttachedCluster#admin_users}
        '''
        result = self._values.get("admin_users")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAttachedClusterAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAttachedClusterAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc6eda6b0f3520d5b4ea64e003b551cc52b512e2c26599ce590d6ab708acf7e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac7abeac3676088040065eb2073021f71fde58536ba7ef2da06e8f65ac06f327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="adminUsers")
    def admin_users(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "adminUsers"))

    @admin_users.setter
    def admin_users(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c67c96b479245a8f37c7f1069f762f793af2c99dba5d139254f2b156e2cb7483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminUsers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAttachedClusterAuthorization]:
        return typing.cast(typing.Optional[GoogleContainerAttachedClusterAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAttachedClusterAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f070acc0b9d009bd2bccb659bf9391588f1f3366ee443d0db3c09ef117168db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterBinaryAuthorization",
    jsii_struct_bases=[],
    name_mapping={"evaluation_mode": "evaluationMode"},
)
class GoogleContainerAttachedClusterBinaryAuthorization:
    def __init__(
        self,
        *,
        evaluation_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param evaluation_mode: Configure Binary Authorization evaluation mode. Possible values: ["DISABLED", "PROJECT_SINGLETON_POLICY_ENFORCE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#evaluation_mode GoogleContainerAttachedCluster#evaluation_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3579b08d1b238468d83b2180e0feb1d8c1a8a90dc6c3e1c7886677d35ce047a1)
            check_type(argname="argument evaluation_mode", value=evaluation_mode, expected_type=type_hints["evaluation_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if evaluation_mode is not None:
            self._values["evaluation_mode"] = evaluation_mode

    @builtins.property
    def evaluation_mode(self) -> typing.Optional[builtins.str]:
        '''Configure Binary Authorization evaluation mode. Possible values: ["DISABLED", "PROJECT_SINGLETON_POLICY_ENFORCE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#evaluation_mode GoogleContainerAttachedCluster#evaluation_mode}
        '''
        result = self._values.get("evaluation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAttachedClusterBinaryAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAttachedClusterBinaryAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterBinaryAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b3d2c437670a00d787faa3c689f665a57230f455d49d628ace754ec3d4de127)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c26f882d61a4c81d0ef51c6017111af2eb30e05b7cda15144efd58fdfc793cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAttachedClusterBinaryAuthorization]:
        return typing.cast(typing.Optional[GoogleContainerAttachedClusterBinaryAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAttachedClusterBinaryAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__431dd21111b28772841a1a3ef55fc6600ca96f610c524d07bd9afe2eedf7d7b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterConfig",
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
class GoogleContainerAttachedClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        fleet: typing.Union["GoogleContainerAttachedClusterFleet", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        oidc_config: typing.Union["GoogleContainerAttachedClusterOidcConfig", typing.Dict[builtins.str, typing.Any]],
        platform_version: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        authorization: typing.Optional[typing.Union[GoogleContainerAttachedClusterAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
        binary_authorization: typing.Optional[typing.Union[GoogleContainerAttachedClusterBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_policy: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union["GoogleContainerAttachedClusterLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        monitoring_config: typing.Optional[typing.Union["GoogleContainerAttachedClusterMonitoringConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        proxy_config: typing.Optional[typing.Union["GoogleContainerAttachedClusterProxyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        security_posture_config: typing.Optional[typing.Union["GoogleContainerAttachedClusterSecurityPostureConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleContainerAttachedClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param distribution: The Kubernetes distribution of the underlying attached cluster. Supported values: "eks", "aks", "generic". The generic distribution provides the ability to register or migrate any CNCF conformant cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#distribution GoogleContainerAttachedCluster#distribution}
        :param fleet: fleet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#fleet GoogleContainerAttachedCluster#fleet}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#location GoogleContainerAttachedCluster#location}
        :param name: The name of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#name GoogleContainerAttachedCluster#name}
        :param oidc_config: oidc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#oidc_config GoogleContainerAttachedCluster#oidc_config}
        :param platform_version: The platform version for the cluster (e.g. '1.23.0-gke.1'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#platform_version GoogleContainerAttachedCluster#platform_version}
        :param annotations: Optional. Annotations on the cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#annotations GoogleContainerAttachedCluster#annotations}
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#authorization GoogleContainerAttachedCluster#authorization}
        :param binary_authorization: binary_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#binary_authorization GoogleContainerAttachedCluster#binary_authorization}
        :param deletion_policy: Policy to determine what flags to send on delete. Possible values: DELETE, DELETE_IGNORE_ERRORS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#deletion_policy GoogleContainerAttachedCluster#deletion_policy}
        :param description: A human readable description of this attached cluster. Cannot be longer than 255 UTF-8 encoded bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#description GoogleContainerAttachedCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#id GoogleContainerAttachedCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#logging_config GoogleContainerAttachedCluster#logging_config}
        :param monitoring_config: monitoring_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#monitoring_config GoogleContainerAttachedCluster#monitoring_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#project GoogleContainerAttachedCluster#project}.
        :param proxy_config: proxy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#proxy_config GoogleContainerAttachedCluster#proxy_config}
        :param security_posture_config: security_posture_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#security_posture_config GoogleContainerAttachedCluster#security_posture_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#timeouts GoogleContainerAttachedCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(fleet, dict):
            fleet = GoogleContainerAttachedClusterFleet(**fleet)
        if isinstance(oidc_config, dict):
            oidc_config = GoogleContainerAttachedClusterOidcConfig(**oidc_config)
        if isinstance(authorization, dict):
            authorization = GoogleContainerAttachedClusterAuthorization(**authorization)
        if isinstance(binary_authorization, dict):
            binary_authorization = GoogleContainerAttachedClusterBinaryAuthorization(**binary_authorization)
        if isinstance(logging_config, dict):
            logging_config = GoogleContainerAttachedClusterLoggingConfig(**logging_config)
        if isinstance(monitoring_config, dict):
            monitoring_config = GoogleContainerAttachedClusterMonitoringConfig(**monitoring_config)
        if isinstance(proxy_config, dict):
            proxy_config = GoogleContainerAttachedClusterProxyConfig(**proxy_config)
        if isinstance(security_posture_config, dict):
            security_posture_config = GoogleContainerAttachedClusterSecurityPostureConfig(**security_posture_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleContainerAttachedClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b910ba135fcf06d73fb278ae640c1518fd231389d818b86ee696c5cca55a1861)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#distribution GoogleContainerAttachedCluster#distribution}
        '''
        result = self._values.get("distribution")
        assert result is not None, "Required property 'distribution' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fleet(self) -> "GoogleContainerAttachedClusterFleet":
        '''fleet block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#fleet GoogleContainerAttachedCluster#fleet}
        '''
        result = self._values.get("fleet")
        assert result is not None, "Required property 'fleet' is missing"
        return typing.cast("GoogleContainerAttachedClusterFleet", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#location GoogleContainerAttachedCluster#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#name GoogleContainerAttachedCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oidc_config(self) -> "GoogleContainerAttachedClusterOidcConfig":
        '''oidc_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#oidc_config GoogleContainerAttachedCluster#oidc_config}
        '''
        result = self._values.get("oidc_config")
        assert result is not None, "Required property 'oidc_config' is missing"
        return typing.cast("GoogleContainerAttachedClusterOidcConfig", result)

    @builtins.property
    def platform_version(self) -> builtins.str:
        '''The platform version for the cluster (e.g. '1.23.0-gke.1').

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#platform_version GoogleContainerAttachedCluster#platform_version}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#annotations GoogleContainerAttachedCluster#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def authorization(
        self,
    ) -> typing.Optional[GoogleContainerAttachedClusterAuthorization]:
        '''authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#authorization GoogleContainerAttachedCluster#authorization}
        '''
        result = self._values.get("authorization")
        return typing.cast(typing.Optional[GoogleContainerAttachedClusterAuthorization], result)

    @builtins.property
    def binary_authorization(
        self,
    ) -> typing.Optional[GoogleContainerAttachedClusterBinaryAuthorization]:
        '''binary_authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#binary_authorization GoogleContainerAttachedCluster#binary_authorization}
        '''
        result = self._values.get("binary_authorization")
        return typing.cast(typing.Optional[GoogleContainerAttachedClusterBinaryAuthorization], result)

    @builtins.property
    def deletion_policy(self) -> typing.Optional[builtins.str]:
        '''Policy to determine what flags to send on delete. Possible values: DELETE, DELETE_IGNORE_ERRORS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#deletion_policy GoogleContainerAttachedCluster#deletion_policy}
        '''
        result = self._values.get("deletion_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human readable description of this attached cluster. Cannot be longer than 255 UTF-8 encoded bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#description GoogleContainerAttachedCluster#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#id GoogleContainerAttachedCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional["GoogleContainerAttachedClusterLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#logging_config GoogleContainerAttachedCluster#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["GoogleContainerAttachedClusterLoggingConfig"], result)

    @builtins.property
    def monitoring_config(
        self,
    ) -> typing.Optional["GoogleContainerAttachedClusterMonitoringConfig"]:
        '''monitoring_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#monitoring_config GoogleContainerAttachedCluster#monitoring_config}
        '''
        result = self._values.get("monitoring_config")
        return typing.cast(typing.Optional["GoogleContainerAttachedClusterMonitoringConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#project GoogleContainerAttachedCluster#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_config(
        self,
    ) -> typing.Optional["GoogleContainerAttachedClusterProxyConfig"]:
        '''proxy_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#proxy_config GoogleContainerAttachedCluster#proxy_config}
        '''
        result = self._values.get("proxy_config")
        return typing.cast(typing.Optional["GoogleContainerAttachedClusterProxyConfig"], result)

    @builtins.property
    def security_posture_config(
        self,
    ) -> typing.Optional["GoogleContainerAttachedClusterSecurityPostureConfig"]:
        '''security_posture_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#security_posture_config GoogleContainerAttachedCluster#security_posture_config}
        '''
        result = self._values.get("security_posture_config")
        return typing.cast(typing.Optional["GoogleContainerAttachedClusterSecurityPostureConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleContainerAttachedClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#timeouts GoogleContainerAttachedCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleContainerAttachedClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAttachedClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterErrors",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleContainerAttachedClusterErrors:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAttachedClusterErrors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAttachedClusterErrorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterErrorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__459e018cce1628c9dc99d6c096bc8a63885eab04e77faa46d6310d115c921500)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleContainerAttachedClusterErrorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dbf71294941bac606c056361b6d8d922b982b6cfd7203fa9c3c211516faa202)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleContainerAttachedClusterErrorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaae05abe5a5b25b8177a2dbf077e3917de1d07ad4ca15b2777ef57c08e3667d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__587b05b381635a9edf2fa945c741a81c721fbd26c7971e25fa8ea9eb7eae369d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__624b07582e1bf5c2333d237c9ceec6ebe7195970abaadba747acddc5f2981652)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleContainerAttachedClusterErrorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterErrorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34053a4715e294c520abf3b1d62165c6c8a8283dd7da7786c2112fee8f1be620)
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
    def internal_value(self) -> typing.Optional[GoogleContainerAttachedClusterErrors]:
        return typing.cast(typing.Optional[GoogleContainerAttachedClusterErrors], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAttachedClusterErrors],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f4a5fdb3c5a07b1013fac641a5a46b40d99e7199bfa331b8e42aebc12286b44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterFleet",
    jsii_struct_bases=[],
    name_mapping={"project": "project"},
)
class GoogleContainerAttachedClusterFleet:
    def __init__(self, *, project: builtins.str) -> None:
        '''
        :param project: The number of the Fleet host project where this cluster will be registered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#project GoogleContainerAttachedCluster#project}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a82920ef3bbbf68eccfafcb09435f4196090258c6e2ad7964bbf4dfbc42cde05)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project": project,
        }

    @builtins.property
    def project(self) -> builtins.str:
        '''The number of the Fleet host project where this cluster will be registered.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#project GoogleContainerAttachedCluster#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAttachedClusterFleet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAttachedClusterFleetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterFleetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d995edba4b753f58412bf47efbeb97e530bf7cc02fa1d5a0b4ddc7b88b1019d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b4c7dc3f8308736650238bbd86838185db0e6d55f34ca38cda230996b2b46d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleContainerAttachedClusterFleet]:
        return typing.cast(typing.Optional[GoogleContainerAttachedClusterFleet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAttachedClusterFleet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39a9935fcb24ac7c4dcba4048321e830eb38d9a6f13873fb4b2e33ac34801b40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"component_config": "componentConfig"},
)
class GoogleContainerAttachedClusterLoggingConfig:
    def __init__(
        self,
        *,
        component_config: typing.Optional[typing.Union["GoogleContainerAttachedClusterLoggingConfigComponentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param component_config: component_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#component_config GoogleContainerAttachedCluster#component_config}
        '''
        if isinstance(component_config, dict):
            component_config = GoogleContainerAttachedClusterLoggingConfigComponentConfig(**component_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__070e8e09a89fcf794164af27afd2c9a19b96c3c7e896f2cc8330d0ae94a87541)
            check_type(argname="argument component_config", value=component_config, expected_type=type_hints["component_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if component_config is not None:
            self._values["component_config"] = component_config

    @builtins.property
    def component_config(
        self,
    ) -> typing.Optional["GoogleContainerAttachedClusterLoggingConfigComponentConfig"]:
        '''component_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#component_config GoogleContainerAttachedCluster#component_config}
        '''
        result = self._values.get("component_config")
        return typing.cast(typing.Optional["GoogleContainerAttachedClusterLoggingConfigComponentConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAttachedClusterLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterLoggingConfigComponentConfig",
    jsii_struct_bases=[],
    name_mapping={"enable_components": "enableComponents"},
)
class GoogleContainerAttachedClusterLoggingConfigComponentConfig:
    def __init__(
        self,
        *,
        enable_components: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enable_components: The components to be enabled. Possible values: ["SYSTEM_COMPONENTS", "WORKLOADS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#enable_components GoogleContainerAttachedCluster#enable_components}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417f4b3c0d6cb728036ee4e4d771392f5870869fedd7976ad4e902ee9596b0b6)
            check_type(argname="argument enable_components", value=enable_components, expected_type=type_hints["enable_components"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_components is not None:
            self._values["enable_components"] = enable_components

    @builtins.property
    def enable_components(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The components to be enabled. Possible values: ["SYSTEM_COMPONENTS", "WORKLOADS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#enable_components GoogleContainerAttachedCluster#enable_components}
        '''
        result = self._values.get("enable_components")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAttachedClusterLoggingConfigComponentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAttachedClusterLoggingConfigComponentConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterLoggingConfigComponentConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4b042132e7a77c030fedcb07ad8e847fe9cbcd819120cac7ddf114af0c13135)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4f14ac83220fff3706c7de12362d9b20ddb0946d57f12d0aeee12001b6e4916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableComponents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAttachedClusterLoggingConfigComponentConfig]:
        return typing.cast(typing.Optional[GoogleContainerAttachedClusterLoggingConfigComponentConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAttachedClusterLoggingConfigComponentConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6be399e3fa659fe309c17755ab0273a2b2044f0ad804b4b00f87a192be2baa48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerAttachedClusterLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa0f8c694f4d402568a5d0edb5d6bc8dfb5b3dcc9fa538e6c8dec9bce8502fbc)
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
        :param enable_components: The components to be enabled. Possible values: ["SYSTEM_COMPONENTS", "WORKLOADS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#enable_components GoogleContainerAttachedCluster#enable_components}
        '''
        value = GoogleContainerAttachedClusterLoggingConfigComponentConfig(
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
    ) -> GoogleContainerAttachedClusterLoggingConfigComponentConfigOutputReference:
        return typing.cast(GoogleContainerAttachedClusterLoggingConfigComponentConfigOutputReference, jsii.get(self, "componentConfig"))

    @builtins.property
    @jsii.member(jsii_name="componentConfigInput")
    def component_config_input(
        self,
    ) -> typing.Optional[GoogleContainerAttachedClusterLoggingConfigComponentConfig]:
        return typing.cast(typing.Optional[GoogleContainerAttachedClusterLoggingConfigComponentConfig], jsii.get(self, "componentConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAttachedClusterLoggingConfig]:
        return typing.cast(typing.Optional[GoogleContainerAttachedClusterLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAttachedClusterLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca1742c25fa7d2fa2b55301eac9c832b5c0abb62e7dbbc47b17c346f0fe524b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterMonitoringConfig",
    jsii_struct_bases=[],
    name_mapping={"managed_prometheus_config": "managedPrometheusConfig"},
)
class GoogleContainerAttachedClusterMonitoringConfig:
    def __init__(
        self,
        *,
        managed_prometheus_config: typing.Optional[typing.Union["GoogleContainerAttachedClusterMonitoringConfigManagedPrometheusConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param managed_prometheus_config: managed_prometheus_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#managed_prometheus_config GoogleContainerAttachedCluster#managed_prometheus_config}
        '''
        if isinstance(managed_prometheus_config, dict):
            managed_prometheus_config = GoogleContainerAttachedClusterMonitoringConfigManagedPrometheusConfig(**managed_prometheus_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52f7396535727634ea332f571a66557e9abd3157b18d52a0825684fc64b01bfc)
            check_type(argname="argument managed_prometheus_config", value=managed_prometheus_config, expected_type=type_hints["managed_prometheus_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if managed_prometheus_config is not None:
            self._values["managed_prometheus_config"] = managed_prometheus_config

    @builtins.property
    def managed_prometheus_config(
        self,
    ) -> typing.Optional["GoogleContainerAttachedClusterMonitoringConfigManagedPrometheusConfig"]:
        '''managed_prometheus_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#managed_prometheus_config GoogleContainerAttachedCluster#managed_prometheus_config}
        '''
        result = self._values.get("managed_prometheus_config")
        return typing.cast(typing.Optional["GoogleContainerAttachedClusterMonitoringConfigManagedPrometheusConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAttachedClusterMonitoringConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterMonitoringConfigManagedPrometheusConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleContainerAttachedClusterMonitoringConfigManagedPrometheusConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Enable Managed Collection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#enabled GoogleContainerAttachedCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e60a9cb18d2dd7d61f01501faf8b2f768d8cfecd75c17f4f88bf515d75d7260f)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable Managed Collection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#enabled GoogleContainerAttachedCluster#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAttachedClusterMonitoringConfigManagedPrometheusConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAttachedClusterMonitoringConfigManagedPrometheusConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterMonitoringConfigManagedPrometheusConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9c0744f8d43410459c99bbed1306f04ab9752bb510e701345e797ba2bead77a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0201478b099e9536471e80e799b1393c85690822bedc4bbdc0d42b812253c7bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAttachedClusterMonitoringConfigManagedPrometheusConfig]:
        return typing.cast(typing.Optional[GoogleContainerAttachedClusterMonitoringConfigManagedPrometheusConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAttachedClusterMonitoringConfigManagedPrometheusConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42a2bbb5f52d33160744a121a5e550bda32fc0d5a96c913e872148ef9dcacedb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerAttachedClusterMonitoringConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterMonitoringConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93544097fce4b5627663afb9d72f9821e096b09fa7f2bdae80c7514134dca435)
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
        :param enabled: Enable Managed Collection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#enabled GoogleContainerAttachedCluster#enabled}
        '''
        value = GoogleContainerAttachedClusterMonitoringConfigManagedPrometheusConfig(
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
    ) -> GoogleContainerAttachedClusterMonitoringConfigManagedPrometheusConfigOutputReference:
        return typing.cast(GoogleContainerAttachedClusterMonitoringConfigManagedPrometheusConfigOutputReference, jsii.get(self, "managedPrometheusConfig"))

    @builtins.property
    @jsii.member(jsii_name="managedPrometheusConfigInput")
    def managed_prometheus_config_input(
        self,
    ) -> typing.Optional[GoogleContainerAttachedClusterMonitoringConfigManagedPrometheusConfig]:
        return typing.cast(typing.Optional[GoogleContainerAttachedClusterMonitoringConfigManagedPrometheusConfig], jsii.get(self, "managedPrometheusConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAttachedClusterMonitoringConfig]:
        return typing.cast(typing.Optional[GoogleContainerAttachedClusterMonitoringConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAttachedClusterMonitoringConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce1b913220c1ba5174439d1e55f8f43fdd5558885ce5ab54a9b31e406b722e40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterOidcConfig",
    jsii_struct_bases=[],
    name_mapping={"issuer_url": "issuerUrl", "jwks": "jwks"},
)
class GoogleContainerAttachedClusterOidcConfig:
    def __init__(
        self,
        *,
        issuer_url: builtins.str,
        jwks: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param issuer_url: A JSON Web Token (JWT) issuer URI. 'issuer' must start with 'https://'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#issuer_url GoogleContainerAttachedCluster#issuer_url}
        :param jwks: OIDC verification keys in JWKS format (RFC 7517). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#jwks GoogleContainerAttachedCluster#jwks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a6e87eb89e63d91c7f94bf53173470f8c236630784b0ba98c16b34db28b2ab0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#issuer_url GoogleContainerAttachedCluster#issuer_url}
        '''
        result = self._values.get("issuer_url")
        assert result is not None, "Required property 'issuer_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def jwks(self) -> typing.Optional[builtins.str]:
        '''OIDC verification keys in JWKS format (RFC 7517).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#jwks GoogleContainerAttachedCluster#jwks}
        '''
        result = self._values.get("jwks")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAttachedClusterOidcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAttachedClusterOidcConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterOidcConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56a2ebe8e314accd0a45eb7d91af144aae50413463ee31bc840aaa97da5d2064)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd9aab8e2ec081506b9b9a324940b4177ba06cf242cc5d0436692262d5989d03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jwks")
    def jwks(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jwks"))

    @jwks.setter
    def jwks(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdcf23f586a17ba236a913a59c402e07a34caf08a42bf4b657a6996f7a2fcbb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAttachedClusterOidcConfig]:
        return typing.cast(typing.Optional[GoogleContainerAttachedClusterOidcConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAttachedClusterOidcConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35bef6df5735280e7aca32523599c2487ddce427f3197f0c2c0bcd53c7b585a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterProxyConfig",
    jsii_struct_bases=[],
    name_mapping={"kubernetes_secret": "kubernetesSecret"},
)
class GoogleContainerAttachedClusterProxyConfig:
    def __init__(
        self,
        *,
        kubernetes_secret: typing.Optional[typing.Union["GoogleContainerAttachedClusterProxyConfigKubernetesSecret", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param kubernetes_secret: kubernetes_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#kubernetes_secret GoogleContainerAttachedCluster#kubernetes_secret}
        '''
        if isinstance(kubernetes_secret, dict):
            kubernetes_secret = GoogleContainerAttachedClusterProxyConfigKubernetesSecret(**kubernetes_secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2f0727a5268759415a89b48a1bd354b688da3cf7b033a5e537bf7f19aadb9c9)
            check_type(argname="argument kubernetes_secret", value=kubernetes_secret, expected_type=type_hints["kubernetes_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kubernetes_secret is not None:
            self._values["kubernetes_secret"] = kubernetes_secret

    @builtins.property
    def kubernetes_secret(
        self,
    ) -> typing.Optional["GoogleContainerAttachedClusterProxyConfigKubernetesSecret"]:
        '''kubernetes_secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#kubernetes_secret GoogleContainerAttachedCluster#kubernetes_secret}
        '''
        result = self._values.get("kubernetes_secret")
        return typing.cast(typing.Optional["GoogleContainerAttachedClusterProxyConfigKubernetesSecret"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAttachedClusterProxyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterProxyConfigKubernetesSecret",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "namespace": "namespace"},
)
class GoogleContainerAttachedClusterProxyConfigKubernetesSecret:
    def __init__(self, *, name: builtins.str, namespace: builtins.str) -> None:
        '''
        :param name: Name of the kubernetes secret containing the proxy config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#name GoogleContainerAttachedCluster#name}
        :param namespace: Namespace of the kubernetes secret containing the proxy config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#namespace GoogleContainerAttachedCluster#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7990d613183bc74d1ca4758762a63cff22f4d9db4d051356b1ef39a3629b7d01)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "namespace": namespace,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the kubernetes secret containing the proxy config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#name GoogleContainerAttachedCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> builtins.str:
        '''Namespace of the kubernetes secret containing the proxy config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#namespace GoogleContainerAttachedCluster#namespace}
        '''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAttachedClusterProxyConfigKubernetesSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAttachedClusterProxyConfigKubernetesSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterProxyConfigKubernetesSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cb473d7a382ede6501b4d2ff0de4834782dd8027472b006d67786c80bcf025f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7029488ae82b502d22991a179b9c5b94a97fe1638fa60f221351a97c0ac79ba0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64a24e5807fd64ddef150d40e77d6639ab87c39428d58df60b51b0ad130b03aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAttachedClusterProxyConfigKubernetesSecret]:
        return typing.cast(typing.Optional[GoogleContainerAttachedClusterProxyConfigKubernetesSecret], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAttachedClusterProxyConfigKubernetesSecret],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59835db127a44fdd971aadf47a304cb582269a494a7b6980dd26a20fcf5ceab9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerAttachedClusterProxyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterProxyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bcd5b625a520af9421db96660838c10fb74324a536025a5c30545ccdd9106bb)
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
        :param name: Name of the kubernetes secret containing the proxy config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#name GoogleContainerAttachedCluster#name}
        :param namespace: Namespace of the kubernetes secret containing the proxy config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#namespace GoogleContainerAttachedCluster#namespace}
        '''
        value = GoogleContainerAttachedClusterProxyConfigKubernetesSecret(
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
    ) -> GoogleContainerAttachedClusterProxyConfigKubernetesSecretOutputReference:
        return typing.cast(GoogleContainerAttachedClusterProxyConfigKubernetesSecretOutputReference, jsii.get(self, "kubernetesSecret"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesSecretInput")
    def kubernetes_secret_input(
        self,
    ) -> typing.Optional[GoogleContainerAttachedClusterProxyConfigKubernetesSecret]:
        return typing.cast(typing.Optional[GoogleContainerAttachedClusterProxyConfigKubernetesSecret], jsii.get(self, "kubernetesSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAttachedClusterProxyConfig]:
        return typing.cast(typing.Optional[GoogleContainerAttachedClusterProxyConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAttachedClusterProxyConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50775372dbb6fc5b6cfae2645bb7cd1d734d81f84ac41e42320619a55ae89051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterSecurityPostureConfig",
    jsii_struct_bases=[],
    name_mapping={"vulnerability_mode": "vulnerabilityMode"},
)
class GoogleContainerAttachedClusterSecurityPostureConfig:
    def __init__(self, *, vulnerability_mode: builtins.str) -> None:
        '''
        :param vulnerability_mode: Sets the mode of the Kubernetes security posture API's workload vulnerability scanning. Possible values: ["VULNERABILITY_DISABLED", "VULNERABILITY_ENTERPRISE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#vulnerability_mode GoogleContainerAttachedCluster#vulnerability_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1ed70c3c9562356110485e265bd942b0050ec5a50895fc354b2fd31d6524d1)
            check_type(argname="argument vulnerability_mode", value=vulnerability_mode, expected_type=type_hints["vulnerability_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vulnerability_mode": vulnerability_mode,
        }

    @builtins.property
    def vulnerability_mode(self) -> builtins.str:
        '''Sets the mode of the Kubernetes security posture API's workload vulnerability scanning. Possible values: ["VULNERABILITY_DISABLED", "VULNERABILITY_ENTERPRISE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#vulnerability_mode GoogleContainerAttachedCluster#vulnerability_mode}
        '''
        result = self._values.get("vulnerability_mode")
        assert result is not None, "Required property 'vulnerability_mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAttachedClusterSecurityPostureConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAttachedClusterSecurityPostureConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterSecurityPostureConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc0b0ce6f9d3a261b966597128de6d04d80de5f3e09304b80aad846ecc7ba1cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8931b9de346adfc568ad7fa8935165d69fe89a8e912680ce478087e54d9ed6ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vulnerabilityMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAttachedClusterSecurityPostureConfig]:
        return typing.cast(typing.Optional[GoogleContainerAttachedClusterSecurityPostureConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAttachedClusterSecurityPostureConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24bb6ad2f2a292f96f2acb368689c70a21c9d6055e9c0feff4dd4a7dc8a1f39c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleContainerAttachedClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#create GoogleContainerAttachedCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#delete GoogleContainerAttachedCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#update GoogleContainerAttachedCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ea6629ef3dd8b8d7f6f19c7a0d2bcef4cbd413d38c8d5c974d453467adff4b9)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#create GoogleContainerAttachedCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#delete GoogleContainerAttachedCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_attached_cluster#update GoogleContainerAttachedCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAttachedClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAttachedClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1244dfdf617ad93d97475d7ced481d993d84805353f9a6c91b89d5e97fc32cf6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5e5088834c18f3ab96b3c8aac68f335b3b610a3110c93f7d0a29b8a074e382d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c25f6e6974a33746b98d09d548cd2b5a92d84fcd5403423163e129ba0520ee3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a20cac69ca2558957e84cc412a646cfb1fd76873eb5e0a2398377bed2853027)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAttachedClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAttachedClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAttachedClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4511f82320ef4faf9c05c3b1175cf28a3287c2a5e16b29f65904866a07670aeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterWorkloadIdentityConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleContainerAttachedClusterWorkloadIdentityConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAttachedClusterWorkloadIdentityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAttachedClusterWorkloadIdentityConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterWorkloadIdentityConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdd040a02f56fc5ec8f450c16bd9f28c78e4beb986789fce30a5e02cb53445c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleContainerAttachedClusterWorkloadIdentityConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e69fc3740075d92528036802eaa7fdf56987f245b6d895e052de9b0c846509c1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleContainerAttachedClusterWorkloadIdentityConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b522cbd88d30c8ffecff7bc0b28da67bbaab40d0fbd513ca1a8c8b253c35798)
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
            type_hints = typing.get_type_hints(_typecheckingstub__88cec7d810a2f3cd53dfa927af20ccb482ca0ef892f11727eed92991a25013d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c361417d75c1583367c8f2ff9efa07a891411f0f726dd3dfc6969794d647f8b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleContainerAttachedClusterWorkloadIdentityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAttachedCluster.GoogleContainerAttachedClusterWorkloadIdentityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6602bfff8b2056ace636c45f0baaa205f33203db65433b67fa00809914bc0198)
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
    ) -> typing.Optional[GoogleContainerAttachedClusterWorkloadIdentityConfig]:
        return typing.cast(typing.Optional[GoogleContainerAttachedClusterWorkloadIdentityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAttachedClusterWorkloadIdentityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eb33b84abeec66c4f158f992c98b35d445341c50932e22184d6cf1ec037f757)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleContainerAttachedCluster",
    "GoogleContainerAttachedClusterAuthorization",
    "GoogleContainerAttachedClusterAuthorizationOutputReference",
    "GoogleContainerAttachedClusterBinaryAuthorization",
    "GoogleContainerAttachedClusterBinaryAuthorizationOutputReference",
    "GoogleContainerAttachedClusterConfig",
    "GoogleContainerAttachedClusterErrors",
    "GoogleContainerAttachedClusterErrorsList",
    "GoogleContainerAttachedClusterErrorsOutputReference",
    "GoogleContainerAttachedClusterFleet",
    "GoogleContainerAttachedClusterFleetOutputReference",
    "GoogleContainerAttachedClusterLoggingConfig",
    "GoogleContainerAttachedClusterLoggingConfigComponentConfig",
    "GoogleContainerAttachedClusterLoggingConfigComponentConfigOutputReference",
    "GoogleContainerAttachedClusterLoggingConfigOutputReference",
    "GoogleContainerAttachedClusterMonitoringConfig",
    "GoogleContainerAttachedClusterMonitoringConfigManagedPrometheusConfig",
    "GoogleContainerAttachedClusterMonitoringConfigManagedPrometheusConfigOutputReference",
    "GoogleContainerAttachedClusterMonitoringConfigOutputReference",
    "GoogleContainerAttachedClusterOidcConfig",
    "GoogleContainerAttachedClusterOidcConfigOutputReference",
    "GoogleContainerAttachedClusterProxyConfig",
    "GoogleContainerAttachedClusterProxyConfigKubernetesSecret",
    "GoogleContainerAttachedClusterProxyConfigKubernetesSecretOutputReference",
    "GoogleContainerAttachedClusterProxyConfigOutputReference",
    "GoogleContainerAttachedClusterSecurityPostureConfig",
    "GoogleContainerAttachedClusterSecurityPostureConfigOutputReference",
    "GoogleContainerAttachedClusterTimeouts",
    "GoogleContainerAttachedClusterTimeoutsOutputReference",
    "GoogleContainerAttachedClusterWorkloadIdentityConfig",
    "GoogleContainerAttachedClusterWorkloadIdentityConfigList",
    "GoogleContainerAttachedClusterWorkloadIdentityConfigOutputReference",
]

publication.publish()

def _typecheckingstub__b77a9eb206309da5d06344a29351268d5b6f5fbdc80e2c8468c2dc94d1baabb5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    distribution: builtins.str,
    fleet: typing.Union[GoogleContainerAttachedClusterFleet, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    oidc_config: typing.Union[GoogleContainerAttachedClusterOidcConfig, typing.Dict[builtins.str, typing.Any]],
    platform_version: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    authorization: typing.Optional[typing.Union[GoogleContainerAttachedClusterAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    binary_authorization: typing.Optional[typing.Union[GoogleContainerAttachedClusterBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_policy: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    logging_config: typing.Optional[typing.Union[GoogleContainerAttachedClusterLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    monitoring_config: typing.Optional[typing.Union[GoogleContainerAttachedClusterMonitoringConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    proxy_config: typing.Optional[typing.Union[GoogleContainerAttachedClusterProxyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    security_posture_config: typing.Optional[typing.Union[GoogleContainerAttachedClusterSecurityPostureConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleContainerAttachedClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2a38145bf831926872df598ef994725bf3891ce3df81039e3c524f2868a8ab07(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fbd2abb4607d49701d6a0e6f72bde2e838cb71f5b1e2eff9cd52fbc3c50c6ac(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3bb226562d99eaf062c1ae32c048d878281d0c2b8eb85f6e470f40b1ce1770f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0eb432c6775424af3ece3b351e1f53b4dba49d2292bf1136b8c445a3e68f408(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21128f12a7858d2f0d9880190ec05762ed842a1446a11e668fa2642b752e52fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__032fd87a0bbe562dd265eaa3646b4e561597c4127b7da6989b123ad1b84cec8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5defe3e2fbabf058bf7168329a73db28284205ffde3b20f7220fd539909fa9be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87125695ebc47577beca4fc4eec6c379133fa9c537b86924e1b899229a9c640b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5aeb905c2522cc56beb74c951c57a1e564bb72ac179d3b2fe113a561c866a42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579091bff89141db51175dcb699ba144ee89627df1f261e866ca914908dd9a75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51b93b324ee95f41690dd7f1bf7b6c9f15a58184219b419cfd6e0e1b7a2e249b(
    *,
    admin_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    admin_users: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6eda6b0f3520d5b4ea64e003b551cc52b512e2c26599ce590d6ab708acf7e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac7abeac3676088040065eb2073021f71fde58536ba7ef2da06e8f65ac06f327(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c67c96b479245a8f37c7f1069f762f793af2c99dba5d139254f2b156e2cb7483(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f070acc0b9d009bd2bccb659bf9391588f1f3366ee443d0db3c09ef117168db(
    value: typing.Optional[GoogleContainerAttachedClusterAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3579b08d1b238468d83b2180e0feb1d8c1a8a90dc6c3e1c7886677d35ce047a1(
    *,
    evaluation_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b3d2c437670a00d787faa3c689f665a57230f455d49d628ace754ec3d4de127(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c26f882d61a4c81d0ef51c6017111af2eb30e05b7cda15144efd58fdfc793cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__431dd21111b28772841a1a3ef55fc6600ca96f610c524d07bd9afe2eedf7d7b4(
    value: typing.Optional[GoogleContainerAttachedClusterBinaryAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b910ba135fcf06d73fb278ae640c1518fd231389d818b86ee696c5cca55a1861(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    distribution: builtins.str,
    fleet: typing.Union[GoogleContainerAttachedClusterFleet, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    oidc_config: typing.Union[GoogleContainerAttachedClusterOidcConfig, typing.Dict[builtins.str, typing.Any]],
    platform_version: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    authorization: typing.Optional[typing.Union[GoogleContainerAttachedClusterAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    binary_authorization: typing.Optional[typing.Union[GoogleContainerAttachedClusterBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_policy: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    logging_config: typing.Optional[typing.Union[GoogleContainerAttachedClusterLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    monitoring_config: typing.Optional[typing.Union[GoogleContainerAttachedClusterMonitoringConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    proxy_config: typing.Optional[typing.Union[GoogleContainerAttachedClusterProxyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    security_posture_config: typing.Optional[typing.Union[GoogleContainerAttachedClusterSecurityPostureConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleContainerAttachedClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__459e018cce1628c9dc99d6c096bc8a63885eab04e77faa46d6310d115c921500(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dbf71294941bac606c056361b6d8d922b982b6cfd7203fa9c3c211516faa202(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaae05abe5a5b25b8177a2dbf077e3917de1d07ad4ca15b2777ef57c08e3667d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__587b05b381635a9edf2fa945c741a81c721fbd26c7971e25fa8ea9eb7eae369d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624b07582e1bf5c2333d237c9ceec6ebe7195970abaadba747acddc5f2981652(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34053a4715e294c520abf3b1d62165c6c8a8283dd7da7786c2112fee8f1be620(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f4a5fdb3c5a07b1013fac641a5a46b40d99e7199bfa331b8e42aebc12286b44(
    value: typing.Optional[GoogleContainerAttachedClusterErrors],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a82920ef3bbbf68eccfafcb09435f4196090258c6e2ad7964bbf4dfbc42cde05(
    *,
    project: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d995edba4b753f58412bf47efbeb97e530bf7cc02fa1d5a0b4ddc7b88b1019d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b4c7dc3f8308736650238bbd86838185db0e6d55f34ca38cda230996b2b46d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a9935fcb24ac7c4dcba4048321e830eb38d9a6f13873fb4b2e33ac34801b40(
    value: typing.Optional[GoogleContainerAttachedClusterFleet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__070e8e09a89fcf794164af27afd2c9a19b96c3c7e896f2cc8330d0ae94a87541(
    *,
    component_config: typing.Optional[typing.Union[GoogleContainerAttachedClusterLoggingConfigComponentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417f4b3c0d6cb728036ee4e4d771392f5870869fedd7976ad4e902ee9596b0b6(
    *,
    enable_components: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b042132e7a77c030fedcb07ad8e847fe9cbcd819120cac7ddf114af0c13135(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4f14ac83220fff3706c7de12362d9b20ddb0946d57f12d0aeee12001b6e4916(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be399e3fa659fe309c17755ab0273a2b2044f0ad804b4b00f87a192be2baa48(
    value: typing.Optional[GoogleContainerAttachedClusterLoggingConfigComponentConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0f8c694f4d402568a5d0edb5d6bc8dfb5b3dcc9fa538e6c8dec9bce8502fbc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca1742c25fa7d2fa2b55301eac9c832b5c0abb62e7dbbc47b17c346f0fe524b0(
    value: typing.Optional[GoogleContainerAttachedClusterLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f7396535727634ea332f571a66557e9abd3157b18d52a0825684fc64b01bfc(
    *,
    managed_prometheus_config: typing.Optional[typing.Union[GoogleContainerAttachedClusterMonitoringConfigManagedPrometheusConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e60a9cb18d2dd7d61f01501faf8b2f768d8cfecd75c17f4f88bf515d75d7260f(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9c0744f8d43410459c99bbed1306f04ab9752bb510e701345e797ba2bead77a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0201478b099e9536471e80e799b1393c85690822bedc4bbdc0d42b812253c7bf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42a2bbb5f52d33160744a121a5e550bda32fc0d5a96c913e872148ef9dcacedb(
    value: typing.Optional[GoogleContainerAttachedClusterMonitoringConfigManagedPrometheusConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93544097fce4b5627663afb9d72f9821e096b09fa7f2bdae80c7514134dca435(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce1b913220c1ba5174439d1e55f8f43fdd5558885ce5ab54a9b31e406b722e40(
    value: typing.Optional[GoogleContainerAttachedClusterMonitoringConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a6e87eb89e63d91c7f94bf53173470f8c236630784b0ba98c16b34db28b2ab0(
    *,
    issuer_url: builtins.str,
    jwks: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a2ebe8e314accd0a45eb7d91af144aae50413463ee31bc840aaa97da5d2064(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd9aab8e2ec081506b9b9a324940b4177ba06cf242cc5d0436692262d5989d03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdcf23f586a17ba236a913a59c402e07a34caf08a42bf4b657a6996f7a2fcbb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35bef6df5735280e7aca32523599c2487ddce427f3197f0c2c0bcd53c7b585a2(
    value: typing.Optional[GoogleContainerAttachedClusterOidcConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f0727a5268759415a89b48a1bd354b688da3cf7b033a5e537bf7f19aadb9c9(
    *,
    kubernetes_secret: typing.Optional[typing.Union[GoogleContainerAttachedClusterProxyConfigKubernetesSecret, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7990d613183bc74d1ca4758762a63cff22f4d9db4d051356b1ef39a3629b7d01(
    *,
    name: builtins.str,
    namespace: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cb473d7a382ede6501b4d2ff0de4834782dd8027472b006d67786c80bcf025f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7029488ae82b502d22991a179b9c5b94a97fe1638fa60f221351a97c0ac79ba0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a24e5807fd64ddef150d40e77d6639ab87c39428d58df60b51b0ad130b03aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59835db127a44fdd971aadf47a304cb582269a494a7b6980dd26a20fcf5ceab9(
    value: typing.Optional[GoogleContainerAttachedClusterProxyConfigKubernetesSecret],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bcd5b625a520af9421db96660838c10fb74324a536025a5c30545ccdd9106bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50775372dbb6fc5b6cfae2645bb7cd1d734d81f84ac41e42320619a55ae89051(
    value: typing.Optional[GoogleContainerAttachedClusterProxyConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1ed70c3c9562356110485e265bd942b0050ec5a50895fc354b2fd31d6524d1(
    *,
    vulnerability_mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc0b0ce6f9d3a261b966597128de6d04d80de5f3e09304b80aad846ecc7ba1cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8931b9de346adfc568ad7fa8935165d69fe89a8e912680ce478087e54d9ed6ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24bb6ad2f2a292f96f2acb368689c70a21c9d6055e9c0feff4dd4a7dc8a1f39c(
    value: typing.Optional[GoogleContainerAttachedClusterSecurityPostureConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ea6629ef3dd8b8d7f6f19c7a0d2bcef4cbd413d38c8d5c974d453467adff4b9(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1244dfdf617ad93d97475d7ced481d993d84805353f9a6c91b89d5e97fc32cf6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5e5088834c18f3ab96b3c8aac68f335b3b610a3110c93f7d0a29b8a074e382d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c25f6e6974a33746b98d09d548cd2b5a92d84fcd5403423163e129ba0520ee3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a20cac69ca2558957e84cc412a646cfb1fd76873eb5e0a2398377bed2853027(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4511f82320ef4faf9c05c3b1175cf28a3287c2a5e16b29f65904866a07670aeb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAttachedClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd040a02f56fc5ec8f450c16bd9f28c78e4beb986789fce30a5e02cb53445c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e69fc3740075d92528036802eaa7fdf56987f245b6d895e052de9b0c846509c1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b522cbd88d30c8ffecff7bc0b28da67bbaab40d0fbd513ca1a8c8b253c35798(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88cec7d810a2f3cd53dfa927af20ccb482ca0ef892f11727eed92991a25013d2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c361417d75c1583367c8f2ff9efa07a891411f0f726dd3dfc6969794d647f8b5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6602bfff8b2056ace636c45f0baaa205f33203db65433b67fa00809914bc0198(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb33b84abeec66c4f158f992c98b35d445341c50932e22184d6cf1ec037f757(
    value: typing.Optional[GoogleContainerAttachedClusterWorkloadIdentityConfig],
) -> None:
    """Type checking stubs"""
    pass
