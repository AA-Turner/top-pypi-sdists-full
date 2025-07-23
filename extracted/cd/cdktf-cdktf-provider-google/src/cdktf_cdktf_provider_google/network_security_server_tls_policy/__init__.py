r'''
# `google_network_security_server_tls_policy`

Refer to the Terraform Registry for docs: [`google_network_security_server_tls_policy`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy).
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


class NetworkSecurityServerTlsPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityServerTlsPolicy.NetworkSecurityServerTlsPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy google_network_security_server_tls_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        allow_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        mtls_policy: typing.Optional[typing.Union["NetworkSecurityServerTlsPolicyMtlsPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        server_certificate: typing.Optional[typing.Union["NetworkSecurityServerTlsPolicyServerCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["NetworkSecurityServerTlsPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy google_network_security_server_tls_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the ServerTlsPolicy resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#name NetworkSecurityServerTlsPolicy#name}
        :param allow_open: This field applies only for Traffic Director policies. It is must be set to false for external HTTPS load balancer policies. Determines if server allows plaintext connections. If set to true, server allows plain text connections. By default, it is set to false. This setting is not exclusive of other encryption modes. For example, if allowOpen and mtlsPolicy are set, server allows both plain text and mTLS connections. See documentation of other encryption modes to confirm compatibility. Consider using it if you wish to upgrade in place your deployment to TLS while having mixed TLS and non-TLS traffic reaching port :80. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#allow_open NetworkSecurityServerTlsPolicy#allow_open}
        :param description: A free-text description of the resource. Max length 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#description NetworkSecurityServerTlsPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#id NetworkSecurityServerTlsPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the ServerTlsPolicy resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#labels NetworkSecurityServerTlsPolicy#labels}
        :param location: The location of the server tls policy. The default value is 'global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#location NetworkSecurityServerTlsPolicy#location}
        :param mtls_policy: mtls_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#mtls_policy NetworkSecurityServerTlsPolicy#mtls_policy}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#project NetworkSecurityServerTlsPolicy#project}.
        :param server_certificate: server_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#server_certificate NetworkSecurityServerTlsPolicy#server_certificate}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#timeouts NetworkSecurityServerTlsPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__427864b3affbe282e2d390aabb9f1fa42be724c955fc3017097915ed42d0ca0d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkSecurityServerTlsPolicyConfig(
            name=name,
            allow_open=allow_open,
            description=description,
            id=id,
            labels=labels,
            location=location,
            mtls_policy=mtls_policy,
            project=project,
            server_certificate=server_certificate,
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
        '''Generates CDKTF code for importing a NetworkSecurityServerTlsPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkSecurityServerTlsPolicy to import.
        :param import_from_id: The id of the existing NetworkSecurityServerTlsPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkSecurityServerTlsPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71e3fbb64a11a482938b67d20b8b22e8bf68f57eed0bed9b81441370d8c5b5f8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMtlsPolicy")
    def put_mtls_policy(
        self,
        *,
        client_validation_ca: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa", typing.Dict[builtins.str, typing.Any]]]]] = None,
        client_validation_mode: typing.Optional[builtins.str] = None,
        client_validation_trust_config: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_validation_ca: client_validation_ca block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#client_validation_ca NetworkSecurityServerTlsPolicy#client_validation_ca}
        :param client_validation_mode: When the client presents an invalid certificate or no certificate to the load balancer, the clientValidationMode specifies how the client connection is handled. Required if the policy is to be used with the external HTTPS load balancing. For Traffic Director it must be empty. Possible values: ["CLIENT_VALIDATION_MODE_UNSPECIFIED", "ALLOW_INVALID_OR_MISSING_CLIENT_CERT", "REJECT_INVALID"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#client_validation_mode NetworkSecurityServerTlsPolicy#client_validation_mode}
        :param client_validation_trust_config: Reference to the TrustConfig from certificatemanager.googleapis.com namespace. If specified, the chain validation will be performed against certificates configured in the given TrustConfig. Allowed only if the policy is to be used with external HTTPS load balancers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#client_validation_trust_config NetworkSecurityServerTlsPolicy#client_validation_trust_config}
        '''
        value = NetworkSecurityServerTlsPolicyMtlsPolicy(
            client_validation_ca=client_validation_ca,
            client_validation_mode=client_validation_mode,
            client_validation_trust_config=client_validation_trust_config,
        )

        return typing.cast(None, jsii.invoke(self, "putMtlsPolicy", [value]))

    @jsii.member(jsii_name="putServerCertificate")
    def put_server_certificate(
        self,
        *,
        certificate_provider_instance: typing.Optional[typing.Union["NetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        grpc_endpoint: typing.Optional[typing.Union["NetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param certificate_provider_instance: certificate_provider_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#certificate_provider_instance NetworkSecurityServerTlsPolicy#certificate_provider_instance}
        :param grpc_endpoint: grpc_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#grpc_endpoint NetworkSecurityServerTlsPolicy#grpc_endpoint}
        '''
        value = NetworkSecurityServerTlsPolicyServerCertificate(
            certificate_provider_instance=certificate_provider_instance,
            grpc_endpoint=grpc_endpoint,
        )

        return typing.cast(None, jsii.invoke(self, "putServerCertificate", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#create NetworkSecurityServerTlsPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#delete NetworkSecurityServerTlsPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#update NetworkSecurityServerTlsPolicy#update}.
        '''
        value = NetworkSecurityServerTlsPolicyTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAllowOpen")
    def reset_allow_open(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowOpen", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetMtlsPolicy")
    def reset_mtls_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMtlsPolicy", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetServerCertificate")
    def reset_server_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerCertificate", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="mtlsPolicy")
    def mtls_policy(self) -> "NetworkSecurityServerTlsPolicyMtlsPolicyOutputReference":
        return typing.cast("NetworkSecurityServerTlsPolicyMtlsPolicyOutputReference", jsii.get(self, "mtlsPolicy"))

    @builtins.property
    @jsii.member(jsii_name="serverCertificate")
    def server_certificate(
        self,
    ) -> "NetworkSecurityServerTlsPolicyServerCertificateOutputReference":
        return typing.cast("NetworkSecurityServerTlsPolicyServerCertificateOutputReference", jsii.get(self, "serverCertificate"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetworkSecurityServerTlsPolicyTimeoutsOutputReference":
        return typing.cast("NetworkSecurityServerTlsPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="allowOpenInput")
    def allow_open_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowOpenInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

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
    @jsii.member(jsii_name="mtlsPolicyInput")
    def mtls_policy_input(
        self,
    ) -> typing.Optional["NetworkSecurityServerTlsPolicyMtlsPolicy"]:
        return typing.cast(typing.Optional["NetworkSecurityServerTlsPolicyMtlsPolicy"], jsii.get(self, "mtlsPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="serverCertificateInput")
    def server_certificate_input(
        self,
    ) -> typing.Optional["NetworkSecurityServerTlsPolicyServerCertificate"]:
        return typing.cast(typing.Optional["NetworkSecurityServerTlsPolicyServerCertificate"], jsii.get(self, "serverCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkSecurityServerTlsPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkSecurityServerTlsPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowOpen")
    def allow_open(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowOpen"))

    @allow_open.setter
    def allow_open(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f2ea14012857a48513f68d59cae8104ce23bb8f74ecff72fee917b8223efd61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowOpen", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec40f91c8a418122fa3eefe744b3b751a56dbd24cba8e590ec23b73e4032a5f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1bbec92584eb02af2e6f54142daf8aeff62fae31f7169e9b0b3c018a1ce012e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d96ddaffc4a681739eec9d3ac5dc4ddc185a8f29d87755e9fe1b6b1acacf27ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__488dc7b59e63da50627701258a5b32acb86cd95a1e9b576d6089380872804777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7df934a271e3324d32213a8e1cbac56b4e7fcc9b1bf4706bfaf5071399a9e699)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08b4a144f7d2656d5d10f0b97668d4680212f8a739bfaadd3d1eab8356be66a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityServerTlsPolicy.NetworkSecurityServerTlsPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "allow_open": "allowOpen",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "location": "location",
        "mtls_policy": "mtlsPolicy",
        "project": "project",
        "server_certificate": "serverCertificate",
        "timeouts": "timeouts",
    },
)
class NetworkSecurityServerTlsPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        allow_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        mtls_policy: typing.Optional[typing.Union["NetworkSecurityServerTlsPolicyMtlsPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        server_certificate: typing.Optional[typing.Union["NetworkSecurityServerTlsPolicyServerCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["NetworkSecurityServerTlsPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the ServerTlsPolicy resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#name NetworkSecurityServerTlsPolicy#name}
        :param allow_open: This field applies only for Traffic Director policies. It is must be set to false for external HTTPS load balancer policies. Determines if server allows plaintext connections. If set to true, server allows plain text connections. By default, it is set to false. This setting is not exclusive of other encryption modes. For example, if allowOpen and mtlsPolicy are set, server allows both plain text and mTLS connections. See documentation of other encryption modes to confirm compatibility. Consider using it if you wish to upgrade in place your deployment to TLS while having mixed TLS and non-TLS traffic reaching port :80. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#allow_open NetworkSecurityServerTlsPolicy#allow_open}
        :param description: A free-text description of the resource. Max length 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#description NetworkSecurityServerTlsPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#id NetworkSecurityServerTlsPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the ServerTlsPolicy resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#labels NetworkSecurityServerTlsPolicy#labels}
        :param location: The location of the server tls policy. The default value is 'global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#location NetworkSecurityServerTlsPolicy#location}
        :param mtls_policy: mtls_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#mtls_policy NetworkSecurityServerTlsPolicy#mtls_policy}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#project NetworkSecurityServerTlsPolicy#project}.
        :param server_certificate: server_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#server_certificate NetworkSecurityServerTlsPolicy#server_certificate}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#timeouts NetworkSecurityServerTlsPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(mtls_policy, dict):
            mtls_policy = NetworkSecurityServerTlsPolicyMtlsPolicy(**mtls_policy)
        if isinstance(server_certificate, dict):
            server_certificate = NetworkSecurityServerTlsPolicyServerCertificate(**server_certificate)
        if isinstance(timeouts, dict):
            timeouts = NetworkSecurityServerTlsPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2be049cdeed2676af3c176d2a1aa35ec9472f9c2fbacc78e2619545ea6c6efc)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allow_open", value=allow_open, expected_type=type_hints["allow_open"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument mtls_policy", value=mtls_policy, expected_type=type_hints["mtls_policy"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument server_certificate", value=server_certificate, expected_type=type_hints["server_certificate"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if allow_open is not None:
            self._values["allow_open"] = allow_open
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if location is not None:
            self._values["location"] = location
        if mtls_policy is not None:
            self._values["mtls_policy"] = mtls_policy
        if project is not None:
            self._values["project"] = project
        if server_certificate is not None:
            self._values["server_certificate"] = server_certificate
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
    def name(self) -> builtins.str:
        '''Name of the ServerTlsPolicy resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#name NetworkSecurityServerTlsPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_open(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This field applies only for Traffic Director policies.

        It is must be set to false for external HTTPS load balancer policies.
        Determines if server allows plaintext connections. If set to true, server allows plain text connections. By default, it is set to false. This setting is not exclusive of other encryption modes. For example, if allowOpen and mtlsPolicy are set, server allows both plain text and mTLS connections. See documentation of other encryption modes to confirm compatibility.
        Consider using it if you wish to upgrade in place your deployment to TLS while having mixed TLS and non-TLS traffic reaching port :80.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#allow_open NetworkSecurityServerTlsPolicy#allow_open}
        '''
        result = self._values.get("allow_open")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A free-text description of the resource. Max length 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#description NetworkSecurityServerTlsPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#id NetworkSecurityServerTlsPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Set of label tags associated with the ServerTlsPolicy resource.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#labels NetworkSecurityServerTlsPolicy#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location of the server tls policy. The default value is 'global'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#location NetworkSecurityServerTlsPolicy#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mtls_policy(
        self,
    ) -> typing.Optional["NetworkSecurityServerTlsPolicyMtlsPolicy"]:
        '''mtls_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#mtls_policy NetworkSecurityServerTlsPolicy#mtls_policy}
        '''
        result = self._values.get("mtls_policy")
        return typing.cast(typing.Optional["NetworkSecurityServerTlsPolicyMtlsPolicy"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#project NetworkSecurityServerTlsPolicy#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_certificate(
        self,
    ) -> typing.Optional["NetworkSecurityServerTlsPolicyServerCertificate"]:
        '''server_certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#server_certificate NetworkSecurityServerTlsPolicy#server_certificate}
        '''
        result = self._values.get("server_certificate")
        return typing.cast(typing.Optional["NetworkSecurityServerTlsPolicyServerCertificate"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetworkSecurityServerTlsPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#timeouts NetworkSecurityServerTlsPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetworkSecurityServerTlsPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityServerTlsPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityServerTlsPolicy.NetworkSecurityServerTlsPolicyMtlsPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "client_validation_ca": "clientValidationCa",
        "client_validation_mode": "clientValidationMode",
        "client_validation_trust_config": "clientValidationTrustConfig",
    },
)
class NetworkSecurityServerTlsPolicyMtlsPolicy:
    def __init__(
        self,
        *,
        client_validation_ca: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa", typing.Dict[builtins.str, typing.Any]]]]] = None,
        client_validation_mode: typing.Optional[builtins.str] = None,
        client_validation_trust_config: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_validation_ca: client_validation_ca block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#client_validation_ca NetworkSecurityServerTlsPolicy#client_validation_ca}
        :param client_validation_mode: When the client presents an invalid certificate or no certificate to the load balancer, the clientValidationMode specifies how the client connection is handled. Required if the policy is to be used with the external HTTPS load balancing. For Traffic Director it must be empty. Possible values: ["CLIENT_VALIDATION_MODE_UNSPECIFIED", "ALLOW_INVALID_OR_MISSING_CLIENT_CERT", "REJECT_INVALID"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#client_validation_mode NetworkSecurityServerTlsPolicy#client_validation_mode}
        :param client_validation_trust_config: Reference to the TrustConfig from certificatemanager.googleapis.com namespace. If specified, the chain validation will be performed against certificates configured in the given TrustConfig. Allowed only if the policy is to be used with external HTTPS load balancers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#client_validation_trust_config NetworkSecurityServerTlsPolicy#client_validation_trust_config}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b367a566d87eddb65b9d885dd22644e1c42fbb72a239f1c0e8f14fa33a695d4)
            check_type(argname="argument client_validation_ca", value=client_validation_ca, expected_type=type_hints["client_validation_ca"])
            check_type(argname="argument client_validation_mode", value=client_validation_mode, expected_type=type_hints["client_validation_mode"])
            check_type(argname="argument client_validation_trust_config", value=client_validation_trust_config, expected_type=type_hints["client_validation_trust_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_validation_ca is not None:
            self._values["client_validation_ca"] = client_validation_ca
        if client_validation_mode is not None:
            self._values["client_validation_mode"] = client_validation_mode
        if client_validation_trust_config is not None:
            self._values["client_validation_trust_config"] = client_validation_trust_config

    @builtins.property
    def client_validation_ca(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa"]]]:
        '''client_validation_ca block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#client_validation_ca NetworkSecurityServerTlsPolicy#client_validation_ca}
        '''
        result = self._values.get("client_validation_ca")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa"]]], result)

    @builtins.property
    def client_validation_mode(self) -> typing.Optional[builtins.str]:
        '''When the client presents an invalid certificate or no certificate to the load balancer, the clientValidationMode specifies how the client connection is handled.

        Required if the policy is to be used with the external HTTPS load balancing. For Traffic Director it must be empty. Possible values: ["CLIENT_VALIDATION_MODE_UNSPECIFIED", "ALLOW_INVALID_OR_MISSING_CLIENT_CERT", "REJECT_INVALID"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#client_validation_mode NetworkSecurityServerTlsPolicy#client_validation_mode}
        '''
        result = self._values.get("client_validation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_validation_trust_config(self) -> typing.Optional[builtins.str]:
        '''Reference to the TrustConfig from certificatemanager.googleapis.com namespace. If specified, the chain validation will be performed against certificates configured in the given TrustConfig. Allowed only if the policy is to be used with external HTTPS load balancers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#client_validation_trust_config NetworkSecurityServerTlsPolicy#client_validation_trust_config}
        '''
        result = self._values.get("client_validation_trust_config")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityServerTlsPolicyMtlsPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityServerTlsPolicy.NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_provider_instance": "certificateProviderInstance",
        "grpc_endpoint": "grpcEndpoint",
    },
)
class NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa:
    def __init__(
        self,
        *,
        certificate_provider_instance: typing.Optional[typing.Union["NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        grpc_endpoint: typing.Optional[typing.Union["NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param certificate_provider_instance: certificate_provider_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#certificate_provider_instance NetworkSecurityServerTlsPolicy#certificate_provider_instance}
        :param grpc_endpoint: grpc_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#grpc_endpoint NetworkSecurityServerTlsPolicy#grpc_endpoint}
        '''
        if isinstance(certificate_provider_instance, dict):
            certificate_provider_instance = NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance(**certificate_provider_instance)
        if isinstance(grpc_endpoint, dict):
            grpc_endpoint = NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint(**grpc_endpoint)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b14d7eb90f132815e88c22dba314d3a7a49b2c6d3ca696a64836ab4b7edc06e)
            check_type(argname="argument certificate_provider_instance", value=certificate_provider_instance, expected_type=type_hints["certificate_provider_instance"])
            check_type(argname="argument grpc_endpoint", value=grpc_endpoint, expected_type=type_hints["grpc_endpoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_provider_instance is not None:
            self._values["certificate_provider_instance"] = certificate_provider_instance
        if grpc_endpoint is not None:
            self._values["grpc_endpoint"] = grpc_endpoint

    @builtins.property
    def certificate_provider_instance(
        self,
    ) -> typing.Optional["NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance"]:
        '''certificate_provider_instance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#certificate_provider_instance NetworkSecurityServerTlsPolicy#certificate_provider_instance}
        '''
        result = self._values.get("certificate_provider_instance")
        return typing.cast(typing.Optional["NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance"], result)

    @builtins.property
    def grpc_endpoint(
        self,
    ) -> typing.Optional["NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint"]:
        '''grpc_endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#grpc_endpoint NetworkSecurityServerTlsPolicy#grpc_endpoint}
        '''
        result = self._values.get("grpc_endpoint")
        return typing.cast(typing.Optional["NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityServerTlsPolicy.NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance",
    jsii_struct_bases=[],
    name_mapping={"plugin_instance": "pluginInstance"},
)
class NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance:
    def __init__(self, *, plugin_instance: builtins.str) -> None:
        '''
        :param plugin_instance: Plugin instance name, used to locate and load CertificateProvider instance configuration. Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#plugin_instance NetworkSecurityServerTlsPolicy#plugin_instance}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4034fda14d999589c06d482d3ccf4013d3efb74742c6ae0cfadb40d5a05fe5ce)
            check_type(argname="argument plugin_instance", value=plugin_instance, expected_type=type_hints["plugin_instance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "plugin_instance": plugin_instance,
        }

    @builtins.property
    def plugin_instance(self) -> builtins.str:
        '''Plugin instance name, used to locate and load CertificateProvider instance configuration.

        Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#plugin_instance NetworkSecurityServerTlsPolicy#plugin_instance}
        '''
        result = self._values.get("plugin_instance")
        assert result is not None, "Required property 'plugin_instance' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityServerTlsPolicy.NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07f0e9c526e646a65357ea9c448c7e4a06e474935c3f3b70931efc52f28af40c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="pluginInstanceInput")
    def plugin_instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginInstance")
    def plugin_instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginInstance"))

    @plugin_instance.setter
    def plugin_instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a14101ff4def439571848498af7e147a47d3fedc1a9f1d0f51fc988f98639973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance]:
        return typing.cast(typing.Optional[NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__454f99b2d5510b77f6cd14a05db38aef91b38c47c3959cd3abf9d4bfe4d3877e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityServerTlsPolicy.NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint",
    jsii_struct_bases=[],
    name_mapping={"target_uri": "targetUri"},
)
class NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint:
    def __init__(self, *, target_uri: builtins.str) -> None:
        '''
        :param target_uri: The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#target_uri NetworkSecurityServerTlsPolicy#target_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5b11f01a3c119e7def9d116a660bff1359cade62c047c7a894e375df4774f01)
            check_type(argname="argument target_uri", value=target_uri, expected_type=type_hints["target_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_uri": target_uri,
        }

    @builtins.property
    def target_uri(self) -> builtins.str:
        '''The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#target_uri NetworkSecurityServerTlsPolicy#target_uri}
        '''
        result = self._values.get("target_uri")
        assert result is not None, "Required property 'target_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityServerTlsPolicy.NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9399104fe6f148a7be3f128440d09b2c3bc0becbc32dcac43f66887ae4047fbc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="targetUriInput")
    def target_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetUriInput"))

    @builtins.property
    @jsii.member(jsii_name="targetUri")
    def target_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetUri"))

    @target_uri.setter
    def target_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ef0a5d43fbcc2a993849bed0b14387d7df84cbb5e72e9b183b0026598799398)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint]:
        return typing.cast(typing.Optional[NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8eb0613045a40429a9dfea2386b61d7db36155f08eec7f92cc7ce9c927adc90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityServerTlsPolicy.NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbcdc6a33bcdfa805ea7c93ced44461ec068a4266b22e2243b78a52a0899cc5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45c4151667f911432378e1c95138f4c49a73a3d6ca9f6c19377be24a98abc72e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c2be70ffeb4bebd773f9763fc4f4e615a1e5752b5bc3907de9883463c60fd51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d6e022d4807cbbd03d48f16a97dfc89ae6d3f2ef7858901da13f44075a49a8e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4b3e4f8da32104e0accdf2084870e4a6a56e138f9f7cd900b617378e512fd94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__091a9f1c4ff926bb3023443caf58cafa047827799b7b94a22eaf9fd0ead4d4b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityServerTlsPolicy.NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__196badd5ce0516acd29061b3619a01378e6bd5741fd551dec4d9063c4453ad64)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCertificateProviderInstance")
    def put_certificate_provider_instance(
        self,
        *,
        plugin_instance: builtins.str,
    ) -> None:
        '''
        :param plugin_instance: Plugin instance name, used to locate and load CertificateProvider instance configuration. Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#plugin_instance NetworkSecurityServerTlsPolicy#plugin_instance}
        '''
        value = NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance(
            plugin_instance=plugin_instance
        )

        return typing.cast(None, jsii.invoke(self, "putCertificateProviderInstance", [value]))

    @jsii.member(jsii_name="putGrpcEndpoint")
    def put_grpc_endpoint(self, *, target_uri: builtins.str) -> None:
        '''
        :param target_uri: The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#target_uri NetworkSecurityServerTlsPolicy#target_uri}
        '''
        value = NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint(
            target_uri=target_uri
        )

        return typing.cast(None, jsii.invoke(self, "putGrpcEndpoint", [value]))

    @jsii.member(jsii_name="resetCertificateProviderInstance")
    def reset_certificate_provider_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateProviderInstance", []))

    @jsii.member(jsii_name="resetGrpcEndpoint")
    def reset_grpc_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpcEndpoint", []))

    @builtins.property
    @jsii.member(jsii_name="certificateProviderInstance")
    def certificate_provider_instance(
        self,
    ) -> NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstanceOutputReference:
        return typing.cast(NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstanceOutputReference, jsii.get(self, "certificateProviderInstance"))

    @builtins.property
    @jsii.member(jsii_name="grpcEndpoint")
    def grpc_endpoint(
        self,
    ) -> NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpointOutputReference:
        return typing.cast(NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpointOutputReference, jsii.get(self, "grpcEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="certificateProviderInstanceInput")
    def certificate_provider_instance_input(
        self,
    ) -> typing.Optional[NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance]:
        return typing.cast(typing.Optional[NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance], jsii.get(self, "certificateProviderInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcEndpointInput")
    def grpc_endpoint_input(
        self,
    ) -> typing.Optional[NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint]:
        return typing.cast(typing.Optional[NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint], jsii.get(self, "grpcEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a6be54d8db5825a51bb0c359c4193f4a212884983412304042b05ab1afa7f4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityServerTlsPolicyMtlsPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityServerTlsPolicy.NetworkSecurityServerTlsPolicyMtlsPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b098256fdab8b1466e4dc7d4a21bf59a3ada464b6a89fe001c124c13572f033)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientValidationCa")
    def put_client_validation_ca(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6959ec3d0f0e3acc258b57fdc5fe794db19b8d3354208a8170397cf5aaeea70a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putClientValidationCa", [value]))

    @jsii.member(jsii_name="resetClientValidationCa")
    def reset_client_validation_ca(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientValidationCa", []))

    @jsii.member(jsii_name="resetClientValidationMode")
    def reset_client_validation_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientValidationMode", []))

    @jsii.member(jsii_name="resetClientValidationTrustConfig")
    def reset_client_validation_trust_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientValidationTrustConfig", []))

    @builtins.property
    @jsii.member(jsii_name="clientValidationCa")
    def client_validation_ca(
        self,
    ) -> NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaList:
        return typing.cast(NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaList, jsii.get(self, "clientValidationCa"))

    @builtins.property
    @jsii.member(jsii_name="clientValidationCaInput")
    def client_validation_ca_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa]]], jsii.get(self, "clientValidationCaInput"))

    @builtins.property
    @jsii.member(jsii_name="clientValidationModeInput")
    def client_validation_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientValidationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="clientValidationTrustConfigInput")
    def client_validation_trust_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientValidationTrustConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="clientValidationMode")
    def client_validation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientValidationMode"))

    @client_validation_mode.setter
    def client_validation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c440307d3f1ef571923d0853dec3e5d85ad6191ee754477770591091de37934b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientValidationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientValidationTrustConfig")
    def client_validation_trust_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientValidationTrustConfig"))

    @client_validation_trust_config.setter
    def client_validation_trust_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b146479b1b27a5fc23d03ab5a61db1bf85dc1945642115629f92d920c763ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientValidationTrustConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecurityServerTlsPolicyMtlsPolicy]:
        return typing.cast(typing.Optional[NetworkSecurityServerTlsPolicyMtlsPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityServerTlsPolicyMtlsPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b686d8080d02a63d26cb97186fbf1282d76ed3eafaa97d1d058a1240c406a31f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityServerTlsPolicy.NetworkSecurityServerTlsPolicyServerCertificate",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_provider_instance": "certificateProviderInstance",
        "grpc_endpoint": "grpcEndpoint",
    },
)
class NetworkSecurityServerTlsPolicyServerCertificate:
    def __init__(
        self,
        *,
        certificate_provider_instance: typing.Optional[typing.Union["NetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        grpc_endpoint: typing.Optional[typing.Union["NetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param certificate_provider_instance: certificate_provider_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#certificate_provider_instance NetworkSecurityServerTlsPolicy#certificate_provider_instance}
        :param grpc_endpoint: grpc_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#grpc_endpoint NetworkSecurityServerTlsPolicy#grpc_endpoint}
        '''
        if isinstance(certificate_provider_instance, dict):
            certificate_provider_instance = NetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance(**certificate_provider_instance)
        if isinstance(grpc_endpoint, dict):
            grpc_endpoint = NetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint(**grpc_endpoint)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d322626dcfa7d4023dc3c5e8649cf67c459749a6831619a3dd0d45f5726083a2)
            check_type(argname="argument certificate_provider_instance", value=certificate_provider_instance, expected_type=type_hints["certificate_provider_instance"])
            check_type(argname="argument grpc_endpoint", value=grpc_endpoint, expected_type=type_hints["grpc_endpoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_provider_instance is not None:
            self._values["certificate_provider_instance"] = certificate_provider_instance
        if grpc_endpoint is not None:
            self._values["grpc_endpoint"] = grpc_endpoint

    @builtins.property
    def certificate_provider_instance(
        self,
    ) -> typing.Optional["NetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance"]:
        '''certificate_provider_instance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#certificate_provider_instance NetworkSecurityServerTlsPolicy#certificate_provider_instance}
        '''
        result = self._values.get("certificate_provider_instance")
        return typing.cast(typing.Optional["NetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance"], result)

    @builtins.property
    def grpc_endpoint(
        self,
    ) -> typing.Optional["NetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint"]:
        '''grpc_endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#grpc_endpoint NetworkSecurityServerTlsPolicy#grpc_endpoint}
        '''
        result = self._values.get("grpc_endpoint")
        return typing.cast(typing.Optional["NetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityServerTlsPolicyServerCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityServerTlsPolicy.NetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance",
    jsii_struct_bases=[],
    name_mapping={"plugin_instance": "pluginInstance"},
)
class NetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance:
    def __init__(self, *, plugin_instance: builtins.str) -> None:
        '''
        :param plugin_instance: Plugin instance name, used to locate and load CertificateProvider instance configuration. Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#plugin_instance NetworkSecurityServerTlsPolicy#plugin_instance}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__421d5f4541c14a7ffeb6f52455121ce46d6a9800733d3fe9a97012153a0415c5)
            check_type(argname="argument plugin_instance", value=plugin_instance, expected_type=type_hints["plugin_instance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "plugin_instance": plugin_instance,
        }

    @builtins.property
    def plugin_instance(self) -> builtins.str:
        '''Plugin instance name, used to locate and load CertificateProvider instance configuration.

        Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#plugin_instance NetworkSecurityServerTlsPolicy#plugin_instance}
        '''
        result = self._values.get("plugin_instance")
        assert result is not None, "Required property 'plugin_instance' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityServerTlsPolicy.NetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3546c04b8d46b1fac75e87663323551c69ec403220d7506435906f47073ff89b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="pluginInstanceInput")
    def plugin_instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginInstance")
    def plugin_instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginInstance"))

    @plugin_instance.setter
    def plugin_instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6191374409fe154c2aa3c6c2e11746b88825a221e4d7485cf8fa879ec6f2fa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance]:
        return typing.cast(typing.Optional[NetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c4892bd2c029ac71931e1a457c404cf0d90bfc6b50cf5b6b494b95b622d41b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityServerTlsPolicy.NetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint",
    jsii_struct_bases=[],
    name_mapping={"target_uri": "targetUri"},
)
class NetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint:
    def __init__(self, *, target_uri: builtins.str) -> None:
        '''
        :param target_uri: The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#target_uri NetworkSecurityServerTlsPolicy#target_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51bcfbd4ed1da882adda167a66fe14c101111d7143c4ee8c2717392221b481aa)
            check_type(argname="argument target_uri", value=target_uri, expected_type=type_hints["target_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_uri": target_uri,
        }

    @builtins.property
    def target_uri(self) -> builtins.str:
        '''The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#target_uri NetworkSecurityServerTlsPolicy#target_uri}
        '''
        result = self._values.get("target_uri")
        assert result is not None, "Required property 'target_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityServerTlsPolicyServerCertificateGrpcEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityServerTlsPolicy.NetworkSecurityServerTlsPolicyServerCertificateGrpcEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f345f91e132b34c86e43b362d83be43fab1140818d5414db1831549f651761a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="targetUriInput")
    def target_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetUriInput"))

    @builtins.property
    @jsii.member(jsii_name="targetUri")
    def target_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetUri"))

    @target_uri.setter
    def target_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07c3aae3825bd79b329571c5763ee1a0a914c7ac0d48602ae2f14c330f72c19c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint]:
        return typing.cast(typing.Optional[NetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f6a3830e53343b51e7be42ebd33fbd43eebbdbad0ac0fcb3f1a0586de025192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityServerTlsPolicyServerCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityServerTlsPolicy.NetworkSecurityServerTlsPolicyServerCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94af6578cef0352ee31aa4e9619ace649dda949373978e0693225adb3acc744d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCertificateProviderInstance")
    def put_certificate_provider_instance(
        self,
        *,
        plugin_instance: builtins.str,
    ) -> None:
        '''
        :param plugin_instance: Plugin instance name, used to locate and load CertificateProvider instance configuration. Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#plugin_instance NetworkSecurityServerTlsPolicy#plugin_instance}
        '''
        value = NetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance(
            plugin_instance=plugin_instance
        )

        return typing.cast(None, jsii.invoke(self, "putCertificateProviderInstance", [value]))

    @jsii.member(jsii_name="putGrpcEndpoint")
    def put_grpc_endpoint(self, *, target_uri: builtins.str) -> None:
        '''
        :param target_uri: The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#target_uri NetworkSecurityServerTlsPolicy#target_uri}
        '''
        value = NetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint(
            target_uri=target_uri
        )

        return typing.cast(None, jsii.invoke(self, "putGrpcEndpoint", [value]))

    @jsii.member(jsii_name="resetCertificateProviderInstance")
    def reset_certificate_provider_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateProviderInstance", []))

    @jsii.member(jsii_name="resetGrpcEndpoint")
    def reset_grpc_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpcEndpoint", []))

    @builtins.property
    @jsii.member(jsii_name="certificateProviderInstance")
    def certificate_provider_instance(
        self,
    ) -> NetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstanceOutputReference:
        return typing.cast(NetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstanceOutputReference, jsii.get(self, "certificateProviderInstance"))

    @builtins.property
    @jsii.member(jsii_name="grpcEndpoint")
    def grpc_endpoint(
        self,
    ) -> NetworkSecurityServerTlsPolicyServerCertificateGrpcEndpointOutputReference:
        return typing.cast(NetworkSecurityServerTlsPolicyServerCertificateGrpcEndpointOutputReference, jsii.get(self, "grpcEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="certificateProviderInstanceInput")
    def certificate_provider_instance_input(
        self,
    ) -> typing.Optional[NetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance]:
        return typing.cast(typing.Optional[NetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance], jsii.get(self, "certificateProviderInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcEndpointInput")
    def grpc_endpoint_input(
        self,
    ) -> typing.Optional[NetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint]:
        return typing.cast(typing.Optional[NetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint], jsii.get(self, "grpcEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecurityServerTlsPolicyServerCertificate]:
        return typing.cast(typing.Optional[NetworkSecurityServerTlsPolicyServerCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityServerTlsPolicyServerCertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac31a65c29c04d0579176a038c29d91230c7c88ada7ed69cd01987aea28e177a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityServerTlsPolicy.NetworkSecurityServerTlsPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class NetworkSecurityServerTlsPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#create NetworkSecurityServerTlsPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#delete NetworkSecurityServerTlsPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#update NetworkSecurityServerTlsPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ed7cfd0b3d6b05d4084d8a0919b1667937120d30841697e6fabbd0fd320250f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#create NetworkSecurityServerTlsPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#delete NetworkSecurityServerTlsPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_server_tls_policy#update NetworkSecurityServerTlsPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityServerTlsPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityServerTlsPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityServerTlsPolicy.NetworkSecurityServerTlsPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__82bc54d796184371dd325559f45aade921bbdd32a1173998bb7eab73f13995e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__56ba00362b907c79154e85aec98bb90d8ad98b2021783e7c1959f175d58979eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dc2b1657a1d155a378c4ffc9b631ee1a72ad355c2fd2c2bf2020377375e8526)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17d5a10d71a066fa1579331d0e034b87a3bffe962442f7e546ddcc87f632fc17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityServerTlsPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityServerTlsPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityServerTlsPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79f9adffdf209ee0478a1cb4273e3cb992ee000422940701b2808cdbc727b5ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetworkSecurityServerTlsPolicy",
    "NetworkSecurityServerTlsPolicyConfig",
    "NetworkSecurityServerTlsPolicyMtlsPolicy",
    "NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa",
    "NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance",
    "NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstanceOutputReference",
    "NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint",
    "NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpointOutputReference",
    "NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaList",
    "NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaOutputReference",
    "NetworkSecurityServerTlsPolicyMtlsPolicyOutputReference",
    "NetworkSecurityServerTlsPolicyServerCertificate",
    "NetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance",
    "NetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstanceOutputReference",
    "NetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint",
    "NetworkSecurityServerTlsPolicyServerCertificateGrpcEndpointOutputReference",
    "NetworkSecurityServerTlsPolicyServerCertificateOutputReference",
    "NetworkSecurityServerTlsPolicyTimeouts",
    "NetworkSecurityServerTlsPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__427864b3affbe282e2d390aabb9f1fa42be724c955fc3017097915ed42d0ca0d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    allow_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    mtls_policy: typing.Optional[typing.Union[NetworkSecurityServerTlsPolicyMtlsPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    server_certificate: typing.Optional[typing.Union[NetworkSecurityServerTlsPolicyServerCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[NetworkSecurityServerTlsPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__71e3fbb64a11a482938b67d20b8b22e8bf68f57eed0bed9b81441370d8c5b5f8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f2ea14012857a48513f68d59cae8104ce23bb8f74ecff72fee917b8223efd61(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec40f91c8a418122fa3eefe744b3b751a56dbd24cba8e590ec23b73e4032a5f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1bbec92584eb02af2e6f54142daf8aeff62fae31f7169e9b0b3c018a1ce012e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d96ddaffc4a681739eec9d3ac5dc4ddc185a8f29d87755e9fe1b6b1acacf27ca(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__488dc7b59e63da50627701258a5b32acb86cd95a1e9b576d6089380872804777(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7df934a271e3324d32213a8e1cbac56b4e7fcc9b1bf4706bfaf5071399a9e699(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b4a144f7d2656d5d10f0b97668d4680212f8a739bfaadd3d1eab8356be66a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2be049cdeed2676af3c176d2a1aa35ec9472f9c2fbacc78e2619545ea6c6efc(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    allow_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    mtls_policy: typing.Optional[typing.Union[NetworkSecurityServerTlsPolicyMtlsPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    server_certificate: typing.Optional[typing.Union[NetworkSecurityServerTlsPolicyServerCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[NetworkSecurityServerTlsPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b367a566d87eddb65b9d885dd22644e1c42fbb72a239f1c0e8f14fa33a695d4(
    *,
    client_validation_ca: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa, typing.Dict[builtins.str, typing.Any]]]]] = None,
    client_validation_mode: typing.Optional[builtins.str] = None,
    client_validation_trust_config: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b14d7eb90f132815e88c22dba314d3a7a49b2c6d3ca696a64836ab4b7edc06e(
    *,
    certificate_provider_instance: typing.Optional[typing.Union[NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance, typing.Dict[builtins.str, typing.Any]]] = None,
    grpc_endpoint: typing.Optional[typing.Union[NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4034fda14d999589c06d482d3ccf4013d3efb74742c6ae0cfadb40d5a05fe5ce(
    *,
    plugin_instance: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f0e9c526e646a65357ea9c448c7e4a06e474935c3f3b70931efc52f28af40c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a14101ff4def439571848498af7e147a47d3fedc1a9f1d0f51fc988f98639973(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__454f99b2d5510b77f6cd14a05db38aef91b38c47c3959cd3abf9d4bfe4d3877e(
    value: typing.Optional[NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b11f01a3c119e7def9d116a660bff1359cade62c047c7a894e375df4774f01(
    *,
    target_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9399104fe6f148a7be3f128440d09b2c3bc0becbc32dcac43f66887ae4047fbc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef0a5d43fbcc2a993849bed0b14387d7df84cbb5e72e9b183b0026598799398(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8eb0613045a40429a9dfea2386b61d7db36155f08eec7f92cc7ce9c927adc90(
    value: typing.Optional[NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbcdc6a33bcdfa805ea7c93ced44461ec068a4266b22e2243b78a52a0899cc5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45c4151667f911432378e1c95138f4c49a73a3d6ca9f6c19377be24a98abc72e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2be70ffeb4bebd773f9763fc4f4e615a1e5752b5bc3907de9883463c60fd51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d6e022d4807cbbd03d48f16a97dfc89ae6d3f2ef7858901da13f44075a49a8e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b3e4f8da32104e0accdf2084870e4a6a56e138f9f7cd900b617378e512fd94(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__091a9f1c4ff926bb3023443caf58cafa047827799b7b94a22eaf9fd0ead4d4b5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__196badd5ce0516acd29061b3619a01378e6bd5741fd551dec4d9063c4453ad64(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a6be54d8db5825a51bb0c359c4193f4a212884983412304042b05ab1afa7f4c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b098256fdab8b1466e4dc7d4a21bf59a3ada464b6a89fe001c124c13572f033(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6959ec3d0f0e3acc258b57fdc5fe794db19b8d3354208a8170397cf5aaeea70a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c440307d3f1ef571923d0853dec3e5d85ad6191ee754477770591091de37934b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b146479b1b27a5fc23d03ab5a61db1bf85dc1945642115629f92d920c763ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b686d8080d02a63d26cb97186fbf1282d76ed3eafaa97d1d058a1240c406a31f(
    value: typing.Optional[NetworkSecurityServerTlsPolicyMtlsPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d322626dcfa7d4023dc3c5e8649cf67c459749a6831619a3dd0d45f5726083a2(
    *,
    certificate_provider_instance: typing.Optional[typing.Union[NetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance, typing.Dict[builtins.str, typing.Any]]] = None,
    grpc_endpoint: typing.Optional[typing.Union[NetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__421d5f4541c14a7ffeb6f52455121ce46d6a9800733d3fe9a97012153a0415c5(
    *,
    plugin_instance: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3546c04b8d46b1fac75e87663323551c69ec403220d7506435906f47073ff89b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6191374409fe154c2aa3c6c2e11746b88825a221e4d7485cf8fa879ec6f2fa1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c4892bd2c029ac71931e1a457c404cf0d90bfc6b50cf5b6b494b95b622d41b8(
    value: typing.Optional[NetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51bcfbd4ed1da882adda167a66fe14c101111d7143c4ee8c2717392221b481aa(
    *,
    target_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f345f91e132b34c86e43b362d83be43fab1140818d5414db1831549f651761a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c3aae3825bd79b329571c5763ee1a0a914c7ac0d48602ae2f14c330f72c19c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f6a3830e53343b51e7be42ebd33fbd43eebbdbad0ac0fcb3f1a0586de025192(
    value: typing.Optional[NetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94af6578cef0352ee31aa4e9619ace649dda949373978e0693225adb3acc744d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac31a65c29c04d0579176a038c29d91230c7c88ada7ed69cd01987aea28e177a(
    value: typing.Optional[NetworkSecurityServerTlsPolicyServerCertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed7cfd0b3d6b05d4084d8a0919b1667937120d30841697e6fabbd0fd320250f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82bc54d796184371dd325559f45aade921bbdd32a1173998bb7eab73f13995e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56ba00362b907c79154e85aec98bb90d8ad98b2021783e7c1959f175d58979eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dc2b1657a1d155a378c4ffc9b631ee1a72ad355c2fd2c2bf2020377375e8526(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17d5a10d71a066fa1579331d0e034b87a3bffe962442f7e546ddcc87f632fc17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f9adffdf209ee0478a1cb4273e3cb992ee000422940701b2808cdbc727b5ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityServerTlsPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
