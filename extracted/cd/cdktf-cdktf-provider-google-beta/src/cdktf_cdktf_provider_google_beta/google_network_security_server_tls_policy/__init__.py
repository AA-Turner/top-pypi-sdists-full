r'''
# `google_network_security_server_tls_policy`

Refer to the Terraform Registry for docs: [`google_network_security_server_tls_policy`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy).
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


class GoogleNetworkSecurityServerTlsPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityServerTlsPolicy.GoogleNetworkSecurityServerTlsPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy google_network_security_server_tls_policy}.'''

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
        mtls_policy: typing.Optional[typing.Union["GoogleNetworkSecurityServerTlsPolicyMtlsPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        server_certificate: typing.Optional[typing.Union["GoogleNetworkSecurityServerTlsPolicyServerCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkSecurityServerTlsPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy google_network_security_server_tls_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the ServerTlsPolicy resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#name GoogleNetworkSecurityServerTlsPolicy#name}
        :param allow_open: This field applies only for Traffic Director policies. It is must be set to false for external HTTPS load balancer policies. Determines if server allows plaintext connections. If set to true, server allows plain text connections. By default, it is set to false. This setting is not exclusive of other encryption modes. For example, if allowOpen and mtlsPolicy are set, server allows both plain text and mTLS connections. See documentation of other encryption modes to confirm compatibility. Consider using it if you wish to upgrade in place your deployment to TLS while having mixed TLS and non-TLS traffic reaching port :80. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#allow_open GoogleNetworkSecurityServerTlsPolicy#allow_open}
        :param description: A free-text description of the resource. Max length 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#description GoogleNetworkSecurityServerTlsPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#id GoogleNetworkSecurityServerTlsPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the ServerTlsPolicy resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#labels GoogleNetworkSecurityServerTlsPolicy#labels}
        :param location: The location of the server tls policy. The default value is 'global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#location GoogleNetworkSecurityServerTlsPolicy#location}
        :param mtls_policy: mtls_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#mtls_policy GoogleNetworkSecurityServerTlsPolicy#mtls_policy}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#project GoogleNetworkSecurityServerTlsPolicy#project}.
        :param server_certificate: server_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#server_certificate GoogleNetworkSecurityServerTlsPolicy#server_certificate}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#timeouts GoogleNetworkSecurityServerTlsPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb8e6b5be56300ee4698d6e8b2a982b328a745ead18b1e43d5a67d1483b8996f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleNetworkSecurityServerTlsPolicyConfig(
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
        '''Generates CDKTF code for importing a GoogleNetworkSecurityServerTlsPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleNetworkSecurityServerTlsPolicy to import.
        :param import_from_id: The id of the existing GoogleNetworkSecurityServerTlsPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleNetworkSecurityServerTlsPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d200199ae0976cc6b0a576b3ebdb0707c8b286c8d709186d17a50a1721d74d3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMtlsPolicy")
    def put_mtls_policy(
        self,
        *,
        client_validation_ca: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa", typing.Dict[builtins.str, typing.Any]]]]] = None,
        client_validation_mode: typing.Optional[builtins.str] = None,
        client_validation_trust_config: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_validation_ca: client_validation_ca block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#client_validation_ca GoogleNetworkSecurityServerTlsPolicy#client_validation_ca}
        :param client_validation_mode: When the client presents an invalid certificate or no certificate to the load balancer, the clientValidationMode specifies how the client connection is handled. Required if the policy is to be used with the external HTTPS load balancing. For Traffic Director it must be empty. Possible values: ["CLIENT_VALIDATION_MODE_UNSPECIFIED", "ALLOW_INVALID_OR_MISSING_CLIENT_CERT", "REJECT_INVALID"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#client_validation_mode GoogleNetworkSecurityServerTlsPolicy#client_validation_mode}
        :param client_validation_trust_config: Reference to the TrustConfig from certificatemanager.googleapis.com namespace. If specified, the chain validation will be performed against certificates configured in the given TrustConfig. Allowed only if the policy is to be used with external HTTPS load balancers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#client_validation_trust_config GoogleNetworkSecurityServerTlsPolicy#client_validation_trust_config}
        '''
        value = GoogleNetworkSecurityServerTlsPolicyMtlsPolicy(
            client_validation_ca=client_validation_ca,
            client_validation_mode=client_validation_mode,
            client_validation_trust_config=client_validation_trust_config,
        )

        return typing.cast(None, jsii.invoke(self, "putMtlsPolicy", [value]))

    @jsii.member(jsii_name="putServerCertificate")
    def put_server_certificate(
        self,
        *,
        certificate_provider_instance: typing.Optional[typing.Union["GoogleNetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        grpc_endpoint: typing.Optional[typing.Union["GoogleNetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param certificate_provider_instance: certificate_provider_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#certificate_provider_instance GoogleNetworkSecurityServerTlsPolicy#certificate_provider_instance}
        :param grpc_endpoint: grpc_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#grpc_endpoint GoogleNetworkSecurityServerTlsPolicy#grpc_endpoint}
        '''
        value = GoogleNetworkSecurityServerTlsPolicyServerCertificate(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#create GoogleNetworkSecurityServerTlsPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#delete GoogleNetworkSecurityServerTlsPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#update GoogleNetworkSecurityServerTlsPolicy#update}.
        '''
        value = GoogleNetworkSecurityServerTlsPolicyTimeouts(
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
    def mtls_policy(
        self,
    ) -> "GoogleNetworkSecurityServerTlsPolicyMtlsPolicyOutputReference":
        return typing.cast("GoogleNetworkSecurityServerTlsPolicyMtlsPolicyOutputReference", jsii.get(self, "mtlsPolicy"))

    @builtins.property
    @jsii.member(jsii_name="serverCertificate")
    def server_certificate(
        self,
    ) -> "GoogleNetworkSecurityServerTlsPolicyServerCertificateOutputReference":
        return typing.cast("GoogleNetworkSecurityServerTlsPolicyServerCertificateOutputReference", jsii.get(self, "serverCertificate"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleNetworkSecurityServerTlsPolicyTimeoutsOutputReference":
        return typing.cast("GoogleNetworkSecurityServerTlsPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["GoogleNetworkSecurityServerTlsPolicyMtlsPolicy"]:
        return typing.cast(typing.Optional["GoogleNetworkSecurityServerTlsPolicyMtlsPolicy"], jsii.get(self, "mtlsPolicyInput"))

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
    ) -> typing.Optional["GoogleNetworkSecurityServerTlsPolicyServerCertificate"]:
        return typing.cast(typing.Optional["GoogleNetworkSecurityServerTlsPolicyServerCertificate"], jsii.get(self, "serverCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetworkSecurityServerTlsPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetworkSecurityServerTlsPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3df442828ab0715900868147439c5f2591bc3aeae9422085b5592ad6b4278c86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowOpen", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2a2613ad378f23bac6adc542ab0816fb18630cb09cccad043a920cb9cef80c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69d066db6567020dec2cde9589b9f7d4653176cb3dd3ec702ac37495b587116a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4a6019823f5e857b393955b9afc3d0d9272452a64301750a0bac97d8d962aac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6854a49b2ff8582aed550a6b1bb4586f6475f95bd6c8d66958a24eb003742ef7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e26244b81c5f8addf2bf771b645ea2175452014cc2a4453a8377afc1b870637)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef3da5a5f58d5e05c34fc3a4ac3ca3cdcf917c94b4dc0d2cdea04bcec91d019d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityServerTlsPolicy.GoogleNetworkSecurityServerTlsPolicyConfig",
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
class GoogleNetworkSecurityServerTlsPolicyConfig(
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
        name: builtins.str,
        allow_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        mtls_policy: typing.Optional[typing.Union["GoogleNetworkSecurityServerTlsPolicyMtlsPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        server_certificate: typing.Optional[typing.Union["GoogleNetworkSecurityServerTlsPolicyServerCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkSecurityServerTlsPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the ServerTlsPolicy resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#name GoogleNetworkSecurityServerTlsPolicy#name}
        :param allow_open: This field applies only for Traffic Director policies. It is must be set to false for external HTTPS load balancer policies. Determines if server allows plaintext connections. If set to true, server allows plain text connections. By default, it is set to false. This setting is not exclusive of other encryption modes. For example, if allowOpen and mtlsPolicy are set, server allows both plain text and mTLS connections. See documentation of other encryption modes to confirm compatibility. Consider using it if you wish to upgrade in place your deployment to TLS while having mixed TLS and non-TLS traffic reaching port :80. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#allow_open GoogleNetworkSecurityServerTlsPolicy#allow_open}
        :param description: A free-text description of the resource. Max length 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#description GoogleNetworkSecurityServerTlsPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#id GoogleNetworkSecurityServerTlsPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the ServerTlsPolicy resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#labels GoogleNetworkSecurityServerTlsPolicy#labels}
        :param location: The location of the server tls policy. The default value is 'global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#location GoogleNetworkSecurityServerTlsPolicy#location}
        :param mtls_policy: mtls_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#mtls_policy GoogleNetworkSecurityServerTlsPolicy#mtls_policy}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#project GoogleNetworkSecurityServerTlsPolicy#project}.
        :param server_certificate: server_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#server_certificate GoogleNetworkSecurityServerTlsPolicy#server_certificate}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#timeouts GoogleNetworkSecurityServerTlsPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(mtls_policy, dict):
            mtls_policy = GoogleNetworkSecurityServerTlsPolicyMtlsPolicy(**mtls_policy)
        if isinstance(server_certificate, dict):
            server_certificate = GoogleNetworkSecurityServerTlsPolicyServerCertificate(**server_certificate)
        if isinstance(timeouts, dict):
            timeouts = GoogleNetworkSecurityServerTlsPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b812c597589d898284b889e722f0a3579d0d93341fc7b0bd3b4b8cf3cee082)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#name GoogleNetworkSecurityServerTlsPolicy#name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#allow_open GoogleNetworkSecurityServerTlsPolicy#allow_open}
        '''
        result = self._values.get("allow_open")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A free-text description of the resource. Max length 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#description GoogleNetworkSecurityServerTlsPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#id GoogleNetworkSecurityServerTlsPolicy#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#labels GoogleNetworkSecurityServerTlsPolicy#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location of the server tls policy. The default value is 'global'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#location GoogleNetworkSecurityServerTlsPolicy#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mtls_policy(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityServerTlsPolicyMtlsPolicy"]:
        '''mtls_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#mtls_policy GoogleNetworkSecurityServerTlsPolicy#mtls_policy}
        '''
        result = self._values.get("mtls_policy")
        return typing.cast(typing.Optional["GoogleNetworkSecurityServerTlsPolicyMtlsPolicy"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#project GoogleNetworkSecurityServerTlsPolicy#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_certificate(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityServerTlsPolicyServerCertificate"]:
        '''server_certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#server_certificate GoogleNetworkSecurityServerTlsPolicy#server_certificate}
        '''
        result = self._values.get("server_certificate")
        return typing.cast(typing.Optional["GoogleNetworkSecurityServerTlsPolicyServerCertificate"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityServerTlsPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#timeouts GoogleNetworkSecurityServerTlsPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleNetworkSecurityServerTlsPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityServerTlsPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityServerTlsPolicy.GoogleNetworkSecurityServerTlsPolicyMtlsPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "client_validation_ca": "clientValidationCa",
        "client_validation_mode": "clientValidationMode",
        "client_validation_trust_config": "clientValidationTrustConfig",
    },
)
class GoogleNetworkSecurityServerTlsPolicyMtlsPolicy:
    def __init__(
        self,
        *,
        client_validation_ca: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa", typing.Dict[builtins.str, typing.Any]]]]] = None,
        client_validation_mode: typing.Optional[builtins.str] = None,
        client_validation_trust_config: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_validation_ca: client_validation_ca block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#client_validation_ca GoogleNetworkSecurityServerTlsPolicy#client_validation_ca}
        :param client_validation_mode: When the client presents an invalid certificate or no certificate to the load balancer, the clientValidationMode specifies how the client connection is handled. Required if the policy is to be used with the external HTTPS load balancing. For Traffic Director it must be empty. Possible values: ["CLIENT_VALIDATION_MODE_UNSPECIFIED", "ALLOW_INVALID_OR_MISSING_CLIENT_CERT", "REJECT_INVALID"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#client_validation_mode GoogleNetworkSecurityServerTlsPolicy#client_validation_mode}
        :param client_validation_trust_config: Reference to the TrustConfig from certificatemanager.googleapis.com namespace. If specified, the chain validation will be performed against certificates configured in the given TrustConfig. Allowed only if the policy is to be used with external HTTPS load balancers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#client_validation_trust_config GoogleNetworkSecurityServerTlsPolicy#client_validation_trust_config}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7955f79955ca0d8a5af193ab6d15bd1c880899cea634feddebe25c47301faab0)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa"]]]:
        '''client_validation_ca block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#client_validation_ca GoogleNetworkSecurityServerTlsPolicy#client_validation_ca}
        '''
        result = self._values.get("client_validation_ca")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa"]]], result)

    @builtins.property
    def client_validation_mode(self) -> typing.Optional[builtins.str]:
        '''When the client presents an invalid certificate or no certificate to the load balancer, the clientValidationMode specifies how the client connection is handled.

        Required if the policy is to be used with the external HTTPS load balancing. For Traffic Director it must be empty. Possible values: ["CLIENT_VALIDATION_MODE_UNSPECIFIED", "ALLOW_INVALID_OR_MISSING_CLIENT_CERT", "REJECT_INVALID"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#client_validation_mode GoogleNetworkSecurityServerTlsPolicy#client_validation_mode}
        '''
        result = self._values.get("client_validation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_validation_trust_config(self) -> typing.Optional[builtins.str]:
        '''Reference to the TrustConfig from certificatemanager.googleapis.com namespace. If specified, the chain validation will be performed against certificates configured in the given TrustConfig. Allowed only if the policy is to be used with external HTTPS load balancers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#client_validation_trust_config GoogleNetworkSecurityServerTlsPolicy#client_validation_trust_config}
        '''
        result = self._values.get("client_validation_trust_config")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityServerTlsPolicyMtlsPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityServerTlsPolicy.GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_provider_instance": "certificateProviderInstance",
        "grpc_endpoint": "grpcEndpoint",
    },
)
class GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa:
    def __init__(
        self,
        *,
        certificate_provider_instance: typing.Optional[typing.Union["GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        grpc_endpoint: typing.Optional[typing.Union["GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param certificate_provider_instance: certificate_provider_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#certificate_provider_instance GoogleNetworkSecurityServerTlsPolicy#certificate_provider_instance}
        :param grpc_endpoint: grpc_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#grpc_endpoint GoogleNetworkSecurityServerTlsPolicy#grpc_endpoint}
        '''
        if isinstance(certificate_provider_instance, dict):
            certificate_provider_instance = GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance(**certificate_provider_instance)
        if isinstance(grpc_endpoint, dict):
            grpc_endpoint = GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint(**grpc_endpoint)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e5ae27904b1aa8799c10cbb96305d99a6aafd3eb368c7f2b7341bb67d14f095)
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
    ) -> typing.Optional["GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance"]:
        '''certificate_provider_instance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#certificate_provider_instance GoogleNetworkSecurityServerTlsPolicy#certificate_provider_instance}
        '''
        result = self._values.get("certificate_provider_instance")
        return typing.cast(typing.Optional["GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance"], result)

    @builtins.property
    def grpc_endpoint(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint"]:
        '''grpc_endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#grpc_endpoint GoogleNetworkSecurityServerTlsPolicy#grpc_endpoint}
        '''
        result = self._values.get("grpc_endpoint")
        return typing.cast(typing.Optional["GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityServerTlsPolicy.GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance",
    jsii_struct_bases=[],
    name_mapping={"plugin_instance": "pluginInstance"},
)
class GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance:
    def __init__(self, *, plugin_instance: builtins.str) -> None:
        '''
        :param plugin_instance: Plugin instance name, used to locate and load CertificateProvider instance configuration. Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#plugin_instance GoogleNetworkSecurityServerTlsPolicy#plugin_instance}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6c38e62bd9d393fd78e246efb151db459a763c52b52d8b4083d032c0423da3a)
            check_type(argname="argument plugin_instance", value=plugin_instance, expected_type=type_hints["plugin_instance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "plugin_instance": plugin_instance,
        }

    @builtins.property
    def plugin_instance(self) -> builtins.str:
        '''Plugin instance name, used to locate and load CertificateProvider instance configuration.

        Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#plugin_instance GoogleNetworkSecurityServerTlsPolicy#plugin_instance}
        '''
        result = self._values.get("plugin_instance")
        assert result is not None, "Required property 'plugin_instance' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityServerTlsPolicy.GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a6d372497157a62f0640d2c929f69294867f65f16f71d5571563f63455648cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6fb33237565ca7ad5711167c409792064180df6d4ac7c97e3b771a6b6b6bc90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e1f90217ef7ea3da79c503d288b9b1c0bba6336f2432baa63552f1ffbb5b89f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityServerTlsPolicy.GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint",
    jsii_struct_bases=[],
    name_mapping={"target_uri": "targetUri"},
)
class GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint:
    def __init__(self, *, target_uri: builtins.str) -> None:
        '''
        :param target_uri: The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#target_uri GoogleNetworkSecurityServerTlsPolicy#target_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d277b2b9a10657be2560f89d1445d62ed717f0c3bcf5d2123b81db4d61fce07)
            check_type(argname="argument target_uri", value=target_uri, expected_type=type_hints["target_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_uri": target_uri,
        }

    @builtins.property
    def target_uri(self) -> builtins.str:
        '''The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#target_uri GoogleNetworkSecurityServerTlsPolicy#target_uri}
        '''
        result = self._values.get("target_uri")
        assert result is not None, "Required property 'target_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityServerTlsPolicy.GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__795b9ada6484aa964617dcf91ee8d6b69fb49b1f450013dc1a022324a2eb7376)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4e24d72eab488802b240844dbb9bc1aa70eb6ebaa0d53543f9f7c41ad587fa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__864a97ac3ddf96469ae4b49aa4651008a60ec8099d440269e2696c742a28925d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityServerTlsPolicy.GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f1d714191b31f940c22f1b89b8ab25da8b5cab053b2829e842bdfd2a460c708)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7bee949cb1c172f990f646112e4783bf127e0a6fefa17b357c7a498f08b945)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__635c7ac43b66d812ed1b0c679c64696cdf9e0f1d6bb69629e57661442257ecae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__604861e16faeb41603ae98ebea4cf8c9b3449b52fea4ba5e9204a018e45e66fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83f640377eb4209ef1654909eda56b1a45b269be87415d9fd08a4753feff54a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce04f47f16ca4288059043c5627f14cddfaacbf296c0e60df261a8ed23e6cf4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityServerTlsPolicy.GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac48daa4adf39707e2450214b2d2c2325fd34312d0243d7c1a47a0b68c148e5a)
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
        :param plugin_instance: Plugin instance name, used to locate and load CertificateProvider instance configuration. Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#plugin_instance GoogleNetworkSecurityServerTlsPolicy#plugin_instance}
        '''
        value = GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance(
            plugin_instance=plugin_instance
        )

        return typing.cast(None, jsii.invoke(self, "putCertificateProviderInstance", [value]))

    @jsii.member(jsii_name="putGrpcEndpoint")
    def put_grpc_endpoint(self, *, target_uri: builtins.str) -> None:
        '''
        :param target_uri: The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#target_uri GoogleNetworkSecurityServerTlsPolicy#target_uri}
        '''
        value = GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint(
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
    ) -> GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstanceOutputReference:
        return typing.cast(GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstanceOutputReference, jsii.get(self, "certificateProviderInstance"))

    @builtins.property
    @jsii.member(jsii_name="grpcEndpoint")
    def grpc_endpoint(
        self,
    ) -> GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpointOutputReference:
        return typing.cast(GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpointOutputReference, jsii.get(self, "grpcEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="certificateProviderInstanceInput")
    def certificate_provider_instance_input(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance], jsii.get(self, "certificateProviderInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcEndpointInput")
    def grpc_endpoint_input(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint], jsii.get(self, "grpcEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b50c9542ef2c9d658f9cf536dac252c70332921b0394be914f0dcf93ad5761de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityServerTlsPolicyMtlsPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityServerTlsPolicy.GoogleNetworkSecurityServerTlsPolicyMtlsPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49d3f309ccd0b9895c89191ff0448c7facf4cfa6af477bcb3a0e91420890f000)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientValidationCa")
    def put_client_validation_ca(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4160289c614fa407b36200807292fd0c233cfd64d24dcce093e235470762cadf)
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
    ) -> GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaList:
        return typing.cast(GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaList, jsii.get(self, "clientValidationCa"))

    @builtins.property
    @jsii.member(jsii_name="clientValidationCaInput")
    def client_validation_ca_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa]]], jsii.get(self, "clientValidationCaInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b234a95a5146228d9efd46c5580ad3802d2e9d3babdada56425d36deae5af771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientValidationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientValidationTrustConfig")
    def client_validation_trust_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientValidationTrustConfig"))

    @client_validation_trust_config.setter
    def client_validation_trust_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f0dd07f4c7a1198e3549c645a0a544771828589787ffe17536235169d1d51b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientValidationTrustConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityServerTlsPolicyMtlsPolicy]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityServerTlsPolicyMtlsPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityServerTlsPolicyMtlsPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf425bba9a54fc449b84af68aed98617b8a6be409fda76af5cef52a075cb67fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityServerTlsPolicy.GoogleNetworkSecurityServerTlsPolicyServerCertificate",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_provider_instance": "certificateProviderInstance",
        "grpc_endpoint": "grpcEndpoint",
    },
)
class GoogleNetworkSecurityServerTlsPolicyServerCertificate:
    def __init__(
        self,
        *,
        certificate_provider_instance: typing.Optional[typing.Union["GoogleNetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        grpc_endpoint: typing.Optional[typing.Union["GoogleNetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param certificate_provider_instance: certificate_provider_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#certificate_provider_instance GoogleNetworkSecurityServerTlsPolicy#certificate_provider_instance}
        :param grpc_endpoint: grpc_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#grpc_endpoint GoogleNetworkSecurityServerTlsPolicy#grpc_endpoint}
        '''
        if isinstance(certificate_provider_instance, dict):
            certificate_provider_instance = GoogleNetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance(**certificate_provider_instance)
        if isinstance(grpc_endpoint, dict):
            grpc_endpoint = GoogleNetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint(**grpc_endpoint)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e745a559d81f3947f1076c66662d56a56f10cbdf3f0cd171df79189589be43fc)
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
    ) -> typing.Optional["GoogleNetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance"]:
        '''certificate_provider_instance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#certificate_provider_instance GoogleNetworkSecurityServerTlsPolicy#certificate_provider_instance}
        '''
        result = self._values.get("certificate_provider_instance")
        return typing.cast(typing.Optional["GoogleNetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance"], result)

    @builtins.property
    def grpc_endpoint(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint"]:
        '''grpc_endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#grpc_endpoint GoogleNetworkSecurityServerTlsPolicy#grpc_endpoint}
        '''
        result = self._values.get("grpc_endpoint")
        return typing.cast(typing.Optional["GoogleNetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityServerTlsPolicyServerCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityServerTlsPolicy.GoogleNetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance",
    jsii_struct_bases=[],
    name_mapping={"plugin_instance": "pluginInstance"},
)
class GoogleNetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance:
    def __init__(self, *, plugin_instance: builtins.str) -> None:
        '''
        :param plugin_instance: Plugin instance name, used to locate and load CertificateProvider instance configuration. Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#plugin_instance GoogleNetworkSecurityServerTlsPolicy#plugin_instance}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__923b35d6599156ea26888b3d61c643851e9675e751f511151194bdd9af4871b4)
            check_type(argname="argument plugin_instance", value=plugin_instance, expected_type=type_hints["plugin_instance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "plugin_instance": plugin_instance,
        }

    @builtins.property
    def plugin_instance(self) -> builtins.str:
        '''Plugin instance name, used to locate and load CertificateProvider instance configuration.

        Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#plugin_instance GoogleNetworkSecurityServerTlsPolicy#plugin_instance}
        '''
        result = self._values.get("plugin_instance")
        assert result is not None, "Required property 'plugin_instance' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityServerTlsPolicy.GoogleNetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bf991cdf755657c9d53874aa5efb89b09d37ec70f126c7273a9818a8e20abf1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1e4d08286e58d37cae016a6949689cee7ac86224035bbd4fa0d1c43fcb2b19d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b87b0640c07622f58a09de224d175ed6f4dd824b5173883e7400a7efdff56298)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityServerTlsPolicy.GoogleNetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint",
    jsii_struct_bases=[],
    name_mapping={"target_uri": "targetUri"},
)
class GoogleNetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint:
    def __init__(self, *, target_uri: builtins.str) -> None:
        '''
        :param target_uri: The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#target_uri GoogleNetworkSecurityServerTlsPolicy#target_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3bd1c7a378086e7bc2d87a0e7e8088a953fc7903cf3cc10558ec59d78239494)
            check_type(argname="argument target_uri", value=target_uri, expected_type=type_hints["target_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_uri": target_uri,
        }

    @builtins.property
    def target_uri(self) -> builtins.str:
        '''The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#target_uri GoogleNetworkSecurityServerTlsPolicy#target_uri}
        '''
        result = self._values.get("target_uri")
        assert result is not None, "Required property 'target_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityServerTlsPolicyServerCertificateGrpcEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityServerTlsPolicy.GoogleNetworkSecurityServerTlsPolicyServerCertificateGrpcEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad37e2a01b4c3db6c143151f6418a8c98a33c8a26f5aeb24eed6bf6db83732e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__888937359d6d447f1cb72a73bac25960e951fd4d7a79ab3ef92fdda91799f22f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9702bf6c1252dae920a960b1c7c270367da6180b359cc0ca36fd2e24dec68f6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityServerTlsPolicyServerCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityServerTlsPolicy.GoogleNetworkSecurityServerTlsPolicyServerCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad4bcb614f9703e1c03a4eb03e0529b9da3fdba7cf32cc0ca3fe2aad194214c1)
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
        :param plugin_instance: Plugin instance name, used to locate and load CertificateProvider instance configuration. Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#plugin_instance GoogleNetworkSecurityServerTlsPolicy#plugin_instance}
        '''
        value = GoogleNetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance(
            plugin_instance=plugin_instance
        )

        return typing.cast(None, jsii.invoke(self, "putCertificateProviderInstance", [value]))

    @jsii.member(jsii_name="putGrpcEndpoint")
    def put_grpc_endpoint(self, *, target_uri: builtins.str) -> None:
        '''
        :param target_uri: The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#target_uri GoogleNetworkSecurityServerTlsPolicy#target_uri}
        '''
        value = GoogleNetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint(
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
    ) -> GoogleNetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstanceOutputReference:
        return typing.cast(GoogleNetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstanceOutputReference, jsii.get(self, "certificateProviderInstance"))

    @builtins.property
    @jsii.member(jsii_name="grpcEndpoint")
    def grpc_endpoint(
        self,
    ) -> GoogleNetworkSecurityServerTlsPolicyServerCertificateGrpcEndpointOutputReference:
        return typing.cast(GoogleNetworkSecurityServerTlsPolicyServerCertificateGrpcEndpointOutputReference, jsii.get(self, "grpcEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="certificateProviderInstanceInput")
    def certificate_provider_instance_input(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance], jsii.get(self, "certificateProviderInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcEndpointInput")
    def grpc_endpoint_input(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint], jsii.get(self, "grpcEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityServerTlsPolicyServerCertificate]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityServerTlsPolicyServerCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityServerTlsPolicyServerCertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50afa647aacd3cf1ad415ffa10ec77351f4125d2fcb389f175834e5807d5b251)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityServerTlsPolicy.GoogleNetworkSecurityServerTlsPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleNetworkSecurityServerTlsPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#create GoogleNetworkSecurityServerTlsPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#delete GoogleNetworkSecurityServerTlsPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#update GoogleNetworkSecurityServerTlsPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8b92313e6677ede19db5e05aa1ee63ec202998d3af472add25a1a277616174f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#create GoogleNetworkSecurityServerTlsPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#delete GoogleNetworkSecurityServerTlsPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_server_tls_policy#update GoogleNetworkSecurityServerTlsPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityServerTlsPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityServerTlsPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityServerTlsPolicy.GoogleNetworkSecurityServerTlsPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__866975c9f04abc403a68185346afc63035f6c813a29754b5f5b3d48ce2bec0e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a3ddcbc3b58bc1e8cd82ec73f16920bf8f0708ca094c87c718f9ed8e833bac1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__501f35ed24ae7a0b6892d87fe55c4a8b40b2db0bf433cebd31fcc0e60076ff73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ad9ae54d3229d60e19d24bba109fc3ccabee384fb2fba91dc619afcf7988bbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityServerTlsPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityServerTlsPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityServerTlsPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__308b8d7601a7ce7b6317a3354847ea50bbad3975431f6f66c9b24a9f37b2845c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleNetworkSecurityServerTlsPolicy",
    "GoogleNetworkSecurityServerTlsPolicyConfig",
    "GoogleNetworkSecurityServerTlsPolicyMtlsPolicy",
    "GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa",
    "GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance",
    "GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstanceOutputReference",
    "GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint",
    "GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpointOutputReference",
    "GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaList",
    "GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaOutputReference",
    "GoogleNetworkSecurityServerTlsPolicyMtlsPolicyOutputReference",
    "GoogleNetworkSecurityServerTlsPolicyServerCertificate",
    "GoogleNetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance",
    "GoogleNetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstanceOutputReference",
    "GoogleNetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint",
    "GoogleNetworkSecurityServerTlsPolicyServerCertificateGrpcEndpointOutputReference",
    "GoogleNetworkSecurityServerTlsPolicyServerCertificateOutputReference",
    "GoogleNetworkSecurityServerTlsPolicyTimeouts",
    "GoogleNetworkSecurityServerTlsPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__fb8e6b5be56300ee4698d6e8b2a982b328a745ead18b1e43d5a67d1483b8996f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    allow_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    mtls_policy: typing.Optional[typing.Union[GoogleNetworkSecurityServerTlsPolicyMtlsPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    server_certificate: typing.Optional[typing.Union[GoogleNetworkSecurityServerTlsPolicyServerCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetworkSecurityServerTlsPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2d200199ae0976cc6b0a576b3ebdb0707c8b286c8d709186d17a50a1721d74d3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3df442828ab0715900868147439c5f2591bc3aeae9422085b5592ad6b4278c86(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2a2613ad378f23bac6adc542ab0816fb18630cb09cccad043a920cb9cef80c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69d066db6567020dec2cde9589b9f7d4653176cb3dd3ec702ac37495b587116a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a6019823f5e857b393955b9afc3d0d9272452a64301750a0bac97d8d962aac(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6854a49b2ff8582aed550a6b1bb4586f6475f95bd6c8d66958a24eb003742ef7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e26244b81c5f8addf2bf771b645ea2175452014cc2a4453a8377afc1b870637(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef3da5a5f58d5e05c34fc3a4ac3ca3cdcf917c94b4dc0d2cdea04bcec91d019d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b812c597589d898284b889e722f0a3579d0d93341fc7b0bd3b4b8cf3cee082(
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
    mtls_policy: typing.Optional[typing.Union[GoogleNetworkSecurityServerTlsPolicyMtlsPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    server_certificate: typing.Optional[typing.Union[GoogleNetworkSecurityServerTlsPolicyServerCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetworkSecurityServerTlsPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7955f79955ca0d8a5af193ab6d15bd1c880899cea634feddebe25c47301faab0(
    *,
    client_validation_ca: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa, typing.Dict[builtins.str, typing.Any]]]]] = None,
    client_validation_mode: typing.Optional[builtins.str] = None,
    client_validation_trust_config: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5ae27904b1aa8799c10cbb96305d99a6aafd3eb368c7f2b7341bb67d14f095(
    *,
    certificate_provider_instance: typing.Optional[typing.Union[GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance, typing.Dict[builtins.str, typing.Any]]] = None,
    grpc_endpoint: typing.Optional[typing.Union[GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c38e62bd9d393fd78e246efb151db459a763c52b52d8b4083d032c0423da3a(
    *,
    plugin_instance: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a6d372497157a62f0640d2c929f69294867f65f16f71d5571563f63455648cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6fb33237565ca7ad5711167c409792064180df6d4ac7c97e3b771a6b6b6bc90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1f90217ef7ea3da79c503d288b9b1c0bba6336f2432baa63552f1ffbb5b89f(
    value: typing.Optional[GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaCertificateProviderInstance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d277b2b9a10657be2560f89d1445d62ed717f0c3bcf5d2123b81db4d61fce07(
    *,
    target_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__795b9ada6484aa964617dcf91ee8d6b69fb49b1f450013dc1a022324a2eb7376(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4e24d72eab488802b240844dbb9bc1aa70eb6ebaa0d53543f9f7c41ad587fa8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864a97ac3ddf96469ae4b49aa4651008a60ec8099d440269e2696c742a28925d(
    value: typing.Optional[GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCaGrpcEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f1d714191b31f940c22f1b89b8ab25da8b5cab053b2829e842bdfd2a460c708(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7bee949cb1c172f990f646112e4783bf127e0a6fefa17b357c7a498f08b945(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__635c7ac43b66d812ed1b0c679c64696cdf9e0f1d6bb69629e57661442257ecae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604861e16faeb41603ae98ebea4cf8c9b3449b52fea4ba5e9204a018e45e66fe(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83f640377eb4209ef1654909eda56b1a45b269be87415d9fd08a4753feff54a2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce04f47f16ca4288059043c5627f14cddfaacbf296c0e60df261a8ed23e6cf4b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac48daa4adf39707e2450214b2d2c2325fd34312d0243d7c1a47a0b68c148e5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b50c9542ef2c9d658f9cf536dac252c70332921b0394be914f0dcf93ad5761de(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d3f309ccd0b9895c89191ff0448c7facf4cfa6af477bcb3a0e91420890f000(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4160289c614fa407b36200807292fd0c233cfd64d24dcce093e235470762cadf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityServerTlsPolicyMtlsPolicyClientValidationCa, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b234a95a5146228d9efd46c5580ad3802d2e9d3babdada56425d36deae5af771(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f0dd07f4c7a1198e3549c645a0a544771828589787ffe17536235169d1d51b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf425bba9a54fc449b84af68aed98617b8a6be409fda76af5cef52a075cb67fd(
    value: typing.Optional[GoogleNetworkSecurityServerTlsPolicyMtlsPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e745a559d81f3947f1076c66662d56a56f10cbdf3f0cd171df79189589be43fc(
    *,
    certificate_provider_instance: typing.Optional[typing.Union[GoogleNetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance, typing.Dict[builtins.str, typing.Any]]] = None,
    grpc_endpoint: typing.Optional[typing.Union[GoogleNetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__923b35d6599156ea26888b3d61c643851e9675e751f511151194bdd9af4871b4(
    *,
    plugin_instance: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bf991cdf755657c9d53874aa5efb89b09d37ec70f126c7273a9818a8e20abf1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e4d08286e58d37cae016a6949689cee7ac86224035bbd4fa0d1c43fcb2b19d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b87b0640c07622f58a09de224d175ed6f4dd824b5173883e7400a7efdff56298(
    value: typing.Optional[GoogleNetworkSecurityServerTlsPolicyServerCertificateCertificateProviderInstance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3bd1c7a378086e7bc2d87a0e7e8088a953fc7903cf3cc10558ec59d78239494(
    *,
    target_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad37e2a01b4c3db6c143151f6418a8c98a33c8a26f5aeb24eed6bf6db83732e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__888937359d6d447f1cb72a73bac25960e951fd4d7a79ab3ef92fdda91799f22f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9702bf6c1252dae920a960b1c7c270367da6180b359cc0ca36fd2e24dec68f6d(
    value: typing.Optional[GoogleNetworkSecurityServerTlsPolicyServerCertificateGrpcEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad4bcb614f9703e1c03a4eb03e0529b9da3fdba7cf32cc0ca3fe2aad194214c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50afa647aacd3cf1ad415ffa10ec77351f4125d2fcb389f175834e5807d5b251(
    value: typing.Optional[GoogleNetworkSecurityServerTlsPolicyServerCertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b92313e6677ede19db5e05aa1ee63ec202998d3af472add25a1a277616174f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__866975c9f04abc403a68185346afc63035f6c813a29754b5f5b3d48ce2bec0e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a3ddcbc3b58bc1e8cd82ec73f16920bf8f0708ca094c87c718f9ed8e833bac1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__501f35ed24ae7a0b6892d87fe55c4a8b40b2db0bf433cebd31fcc0e60076ff73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ad9ae54d3229d60e19d24bba109fc3ccabee384fb2fba91dc619afcf7988bbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__308b8d7601a7ce7b6317a3354847ea50bbad3975431f6f66c9b24a9f37b2845c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityServerTlsPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
