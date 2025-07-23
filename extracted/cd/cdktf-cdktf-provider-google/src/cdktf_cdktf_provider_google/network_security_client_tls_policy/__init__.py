r'''
# `google_network_security_client_tls_policy`

Refer to the Terraform Registry for docs: [`google_network_security_client_tls_policy`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy).
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


class NetworkSecurityClientTlsPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityClientTlsPolicy.NetworkSecurityClientTlsPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy google_network_security_client_tls_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        client_certificate: typing.Optional[typing.Union["NetworkSecurityClientTlsPolicyClientCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        server_validation_ca: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityClientTlsPolicyServerValidationCa", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sni: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkSecurityClientTlsPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy google_network_security_client_tls_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the ClientTlsPolicy resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#name NetworkSecurityClientTlsPolicy#name}
        :param client_certificate: client_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#client_certificate NetworkSecurityClientTlsPolicy#client_certificate}
        :param description: A free-text description of the resource. Max length 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#description NetworkSecurityClientTlsPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#id NetworkSecurityClientTlsPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the ClientTlsPolicy resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#labels NetworkSecurityClientTlsPolicy#labels}
        :param location: The location of the client tls policy. The default value is 'global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#location NetworkSecurityClientTlsPolicy#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#project NetworkSecurityClientTlsPolicy#project}.
        :param server_validation_ca: server_validation_ca block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#server_validation_ca NetworkSecurityClientTlsPolicy#server_validation_ca}
        :param sni: Server Name Indication string to present to the server during TLS handshake. E.g: "secure.example.com". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#sni NetworkSecurityClientTlsPolicy#sni}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#timeouts NetworkSecurityClientTlsPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b914d1e8bb192c9bcb9f30f0ab2e5cc0fb8e8a134be77b1a3142bc3918ab231f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkSecurityClientTlsPolicyConfig(
            name=name,
            client_certificate=client_certificate,
            description=description,
            id=id,
            labels=labels,
            location=location,
            project=project,
            server_validation_ca=server_validation_ca,
            sni=sni,
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
        '''Generates CDKTF code for importing a NetworkSecurityClientTlsPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkSecurityClientTlsPolicy to import.
        :param import_from_id: The id of the existing NetworkSecurityClientTlsPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkSecurityClientTlsPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7188bfb1edc97a1b8be29af314396160e1ed6534ecf97a28786effa17b4ea5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putClientCertificate")
    def put_client_certificate(
        self,
        *,
        certificate_provider_instance: typing.Optional[typing.Union["NetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        grpc_endpoint: typing.Optional[typing.Union["NetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param certificate_provider_instance: certificate_provider_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#certificate_provider_instance NetworkSecurityClientTlsPolicy#certificate_provider_instance}
        :param grpc_endpoint: grpc_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#grpc_endpoint NetworkSecurityClientTlsPolicy#grpc_endpoint}
        '''
        value = NetworkSecurityClientTlsPolicyClientCertificate(
            certificate_provider_instance=certificate_provider_instance,
            grpc_endpoint=grpc_endpoint,
        )

        return typing.cast(None, jsii.invoke(self, "putClientCertificate", [value]))

    @jsii.member(jsii_name="putServerValidationCa")
    def put_server_validation_ca(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityClientTlsPolicyServerValidationCa", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fff50be84df0b4de5d91e15bcb37d25a39e51500fb11286dca6ec77f89a5157d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putServerValidationCa", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#create NetworkSecurityClientTlsPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#delete NetworkSecurityClientTlsPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#update NetworkSecurityClientTlsPolicy#update}.
        '''
        value = NetworkSecurityClientTlsPolicyTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetClientCertificate")
    def reset_client_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificate", []))

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

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetServerValidationCa")
    def reset_server_validation_ca(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerValidationCa", []))

    @jsii.member(jsii_name="resetSni")
    def reset_sni(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSni", []))

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
    @jsii.member(jsii_name="clientCertificate")
    def client_certificate(
        self,
    ) -> "NetworkSecurityClientTlsPolicyClientCertificateOutputReference":
        return typing.cast("NetworkSecurityClientTlsPolicyClientCertificateOutputReference", jsii.get(self, "clientCertificate"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="serverValidationCa")
    def server_validation_ca(
        self,
    ) -> "NetworkSecurityClientTlsPolicyServerValidationCaList":
        return typing.cast("NetworkSecurityClientTlsPolicyServerValidationCaList", jsii.get(self, "serverValidationCa"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetworkSecurityClientTlsPolicyTimeoutsOutputReference":
        return typing.cast("NetworkSecurityClientTlsPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateInput")
    def client_certificate_input(
        self,
    ) -> typing.Optional["NetworkSecurityClientTlsPolicyClientCertificate"]:
        return typing.cast(typing.Optional["NetworkSecurityClientTlsPolicyClientCertificate"], jsii.get(self, "clientCertificateInput"))

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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="serverValidationCaInput")
    def server_validation_ca_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityClientTlsPolicyServerValidationCa"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityClientTlsPolicyServerValidationCa"]]], jsii.get(self, "serverValidationCaInput"))

    @builtins.property
    @jsii.member(jsii_name="sniInput")
    def sni_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sniInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkSecurityClientTlsPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkSecurityClientTlsPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec378edb8ea76441542db0b88754fc63711c646a11b368c4ab896e094a854cae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa7411d158fb0539930fcfe91fdfb24213f7c5a770af72f73ca51a930a9d3f3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8bd8e2a64c95cce6d8bd8392bf24553a8f630cdb828858149f6344dbb2dee5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e7d1bba7d9d55f5f722bced349679a6ff43f7b63eb19d38d82bfa722c756f27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe0f9bd3a94c6509c0b0f953e893113ebe6105532ce37943dee0858472516261)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b02e7f3795902d0b8bee2dae4f64792729a66393f6ff70b00748572c9b757101)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sni")
    def sni(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sni"))

    @sni.setter
    def sni(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77bd7eb5bdbd3b5ae8473895f4647a57a55f900544650c1f24dafddae32b21c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sni", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityClientTlsPolicy.NetworkSecurityClientTlsPolicyClientCertificate",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_provider_instance": "certificateProviderInstance",
        "grpc_endpoint": "grpcEndpoint",
    },
)
class NetworkSecurityClientTlsPolicyClientCertificate:
    def __init__(
        self,
        *,
        certificate_provider_instance: typing.Optional[typing.Union["NetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        grpc_endpoint: typing.Optional[typing.Union["NetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param certificate_provider_instance: certificate_provider_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#certificate_provider_instance NetworkSecurityClientTlsPolicy#certificate_provider_instance}
        :param grpc_endpoint: grpc_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#grpc_endpoint NetworkSecurityClientTlsPolicy#grpc_endpoint}
        '''
        if isinstance(certificate_provider_instance, dict):
            certificate_provider_instance = NetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance(**certificate_provider_instance)
        if isinstance(grpc_endpoint, dict):
            grpc_endpoint = NetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint(**grpc_endpoint)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92296b9ce28f34379ed931d27d89b94c63b8a998b3498d70bc8aad12f7123ea0)
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
    ) -> typing.Optional["NetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance"]:
        '''certificate_provider_instance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#certificate_provider_instance NetworkSecurityClientTlsPolicy#certificate_provider_instance}
        '''
        result = self._values.get("certificate_provider_instance")
        return typing.cast(typing.Optional["NetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance"], result)

    @builtins.property
    def grpc_endpoint(
        self,
    ) -> typing.Optional["NetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint"]:
        '''grpc_endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#grpc_endpoint NetworkSecurityClientTlsPolicy#grpc_endpoint}
        '''
        result = self._values.get("grpc_endpoint")
        return typing.cast(typing.Optional["NetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityClientTlsPolicyClientCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityClientTlsPolicy.NetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance",
    jsii_struct_bases=[],
    name_mapping={"plugin_instance": "pluginInstance"},
)
class NetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance:
    def __init__(self, *, plugin_instance: builtins.str) -> None:
        '''
        :param plugin_instance: Plugin instance name, used to locate and load CertificateProvider instance configuration. Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#plugin_instance NetworkSecurityClientTlsPolicy#plugin_instance}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97f23c2fe70a2902ee2c6220de2783d599599cec2e6e18d4270821dfd5db17b2)
            check_type(argname="argument plugin_instance", value=plugin_instance, expected_type=type_hints["plugin_instance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "plugin_instance": plugin_instance,
        }

    @builtins.property
    def plugin_instance(self) -> builtins.str:
        '''Plugin instance name, used to locate and load CertificateProvider instance configuration.

        Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#plugin_instance NetworkSecurityClientTlsPolicy#plugin_instance}
        '''
        result = self._values.get("plugin_instance")
        assert result is not None, "Required property 'plugin_instance' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityClientTlsPolicy.NetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a345a6042bfefea0cd9855acf3f3ad5ec062fcab337bfb23b8eda8455cc48dd6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db9ea7d91f06395d1a0f740e225f76c924efd44a2523805515aaba679331c92e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance]:
        return typing.cast(typing.Optional[NetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58709f384a06e055f2ac47cedd4a48f84c85a2eb681d7efd779ecc5bff50d85e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityClientTlsPolicy.NetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint",
    jsii_struct_bases=[],
    name_mapping={"target_uri": "targetUri"},
)
class NetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint:
    def __init__(self, *, target_uri: builtins.str) -> None:
        '''
        :param target_uri: The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#target_uri NetworkSecurityClientTlsPolicy#target_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e63d14b7e3e0e795053b589ee1d25ee832173e19b4797a2e34198aed0c9ec151)
            check_type(argname="argument target_uri", value=target_uri, expected_type=type_hints["target_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_uri": target_uri,
        }

    @builtins.property
    def target_uri(self) -> builtins.str:
        '''The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#target_uri NetworkSecurityClientTlsPolicy#target_uri}
        '''
        result = self._values.get("target_uri")
        assert result is not None, "Required property 'target_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityClientTlsPolicyClientCertificateGrpcEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityClientTlsPolicy.NetworkSecurityClientTlsPolicyClientCertificateGrpcEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36382491de8dd75fac91eb76dbe2a48a0efcf17357d421a79a64a81f5c9c8597)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9050dd2b02add1a4b86b8b7909ba4bcf5b999fa97e1c9094adfa143c8d026f80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint]:
        return typing.cast(typing.Optional[NetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__133a402fc90c59ec8cc85868a016c9ccde3ae0b7801cd17636155ddb15e90cc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityClientTlsPolicyClientCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityClientTlsPolicy.NetworkSecurityClientTlsPolicyClientCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e0879a49b4b3b15aba2a130b66a988d7cfbf6318aded4db988837fa178b9aad)
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
        :param plugin_instance: Plugin instance name, used to locate and load CertificateProvider instance configuration. Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#plugin_instance NetworkSecurityClientTlsPolicy#plugin_instance}
        '''
        value = NetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance(
            plugin_instance=plugin_instance
        )

        return typing.cast(None, jsii.invoke(self, "putCertificateProviderInstance", [value]))

    @jsii.member(jsii_name="putGrpcEndpoint")
    def put_grpc_endpoint(self, *, target_uri: builtins.str) -> None:
        '''
        :param target_uri: The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#target_uri NetworkSecurityClientTlsPolicy#target_uri}
        '''
        value = NetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint(
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
    ) -> NetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstanceOutputReference:
        return typing.cast(NetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstanceOutputReference, jsii.get(self, "certificateProviderInstance"))

    @builtins.property
    @jsii.member(jsii_name="grpcEndpoint")
    def grpc_endpoint(
        self,
    ) -> NetworkSecurityClientTlsPolicyClientCertificateGrpcEndpointOutputReference:
        return typing.cast(NetworkSecurityClientTlsPolicyClientCertificateGrpcEndpointOutputReference, jsii.get(self, "grpcEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="certificateProviderInstanceInput")
    def certificate_provider_instance_input(
        self,
    ) -> typing.Optional[NetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance]:
        return typing.cast(typing.Optional[NetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance], jsii.get(self, "certificateProviderInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcEndpointInput")
    def grpc_endpoint_input(
        self,
    ) -> typing.Optional[NetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint]:
        return typing.cast(typing.Optional[NetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint], jsii.get(self, "grpcEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecurityClientTlsPolicyClientCertificate]:
        return typing.cast(typing.Optional[NetworkSecurityClientTlsPolicyClientCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityClientTlsPolicyClientCertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed2b5287df0c47edab5ac3af89b12ffd6780bc7f33522db33fe72f0cf0cc0dd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityClientTlsPolicy.NetworkSecurityClientTlsPolicyConfig",
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
        "client_certificate": "clientCertificate",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "location": "location",
        "project": "project",
        "server_validation_ca": "serverValidationCa",
        "sni": "sni",
        "timeouts": "timeouts",
    },
)
class NetworkSecurityClientTlsPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        client_certificate: typing.Optional[typing.Union[NetworkSecurityClientTlsPolicyClientCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        server_validation_ca: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityClientTlsPolicyServerValidationCa", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sni: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkSecurityClientTlsPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the ClientTlsPolicy resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#name NetworkSecurityClientTlsPolicy#name}
        :param client_certificate: client_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#client_certificate NetworkSecurityClientTlsPolicy#client_certificate}
        :param description: A free-text description of the resource. Max length 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#description NetworkSecurityClientTlsPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#id NetworkSecurityClientTlsPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the ClientTlsPolicy resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#labels NetworkSecurityClientTlsPolicy#labels}
        :param location: The location of the client tls policy. The default value is 'global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#location NetworkSecurityClientTlsPolicy#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#project NetworkSecurityClientTlsPolicy#project}.
        :param server_validation_ca: server_validation_ca block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#server_validation_ca NetworkSecurityClientTlsPolicy#server_validation_ca}
        :param sni: Server Name Indication string to present to the server during TLS handshake. E.g: "secure.example.com". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#sni NetworkSecurityClientTlsPolicy#sni}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#timeouts NetworkSecurityClientTlsPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(client_certificate, dict):
            client_certificate = NetworkSecurityClientTlsPolicyClientCertificate(**client_certificate)
        if isinstance(timeouts, dict):
            timeouts = NetworkSecurityClientTlsPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__049e21e03391ad05173e1ebbd1b67b911b8fd8a90200b3a7c825b024da9a72b2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument client_certificate", value=client_certificate, expected_type=type_hints["client_certificate"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument server_validation_ca", value=server_validation_ca, expected_type=type_hints["server_validation_ca"])
            check_type(argname="argument sni", value=sni, expected_type=type_hints["sni"])
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
        if client_certificate is not None:
            self._values["client_certificate"] = client_certificate
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if location is not None:
            self._values["location"] = location
        if project is not None:
            self._values["project"] = project
        if server_validation_ca is not None:
            self._values["server_validation_ca"] = server_validation_ca
        if sni is not None:
            self._values["sni"] = sni
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
        '''Name of the ClientTlsPolicy resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#name NetworkSecurityClientTlsPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_certificate(
        self,
    ) -> typing.Optional[NetworkSecurityClientTlsPolicyClientCertificate]:
        '''client_certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#client_certificate NetworkSecurityClientTlsPolicy#client_certificate}
        '''
        result = self._values.get("client_certificate")
        return typing.cast(typing.Optional[NetworkSecurityClientTlsPolicyClientCertificate], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A free-text description of the resource. Max length 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#description NetworkSecurityClientTlsPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#id NetworkSecurityClientTlsPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Set of label tags associated with the ClientTlsPolicy resource.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#labels NetworkSecurityClientTlsPolicy#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location of the client tls policy. The default value is 'global'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#location NetworkSecurityClientTlsPolicy#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#project NetworkSecurityClientTlsPolicy#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_validation_ca(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityClientTlsPolicyServerValidationCa"]]]:
        '''server_validation_ca block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#server_validation_ca NetworkSecurityClientTlsPolicy#server_validation_ca}
        '''
        result = self._values.get("server_validation_ca")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityClientTlsPolicyServerValidationCa"]]], result)

    @builtins.property
    def sni(self) -> typing.Optional[builtins.str]:
        '''Server Name Indication string to present to the server during TLS handshake. E.g: "secure.example.com".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#sni NetworkSecurityClientTlsPolicy#sni}
        '''
        result = self._values.get("sni")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetworkSecurityClientTlsPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#timeouts NetworkSecurityClientTlsPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetworkSecurityClientTlsPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityClientTlsPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityClientTlsPolicy.NetworkSecurityClientTlsPolicyServerValidationCa",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_provider_instance": "certificateProviderInstance",
        "grpc_endpoint": "grpcEndpoint",
    },
)
class NetworkSecurityClientTlsPolicyServerValidationCa:
    def __init__(
        self,
        *,
        certificate_provider_instance: typing.Optional[typing.Union["NetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        grpc_endpoint: typing.Optional[typing.Union["NetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param certificate_provider_instance: certificate_provider_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#certificate_provider_instance NetworkSecurityClientTlsPolicy#certificate_provider_instance}
        :param grpc_endpoint: grpc_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#grpc_endpoint NetworkSecurityClientTlsPolicy#grpc_endpoint}
        '''
        if isinstance(certificate_provider_instance, dict):
            certificate_provider_instance = NetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance(**certificate_provider_instance)
        if isinstance(grpc_endpoint, dict):
            grpc_endpoint = NetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint(**grpc_endpoint)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ecd1e94e9fdc08e4574fa7d84fb34f53d5e51085a0e01ca7f91d6ce5260e2dc)
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
    ) -> typing.Optional["NetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance"]:
        '''certificate_provider_instance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#certificate_provider_instance NetworkSecurityClientTlsPolicy#certificate_provider_instance}
        '''
        result = self._values.get("certificate_provider_instance")
        return typing.cast(typing.Optional["NetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance"], result)

    @builtins.property
    def grpc_endpoint(
        self,
    ) -> typing.Optional["NetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint"]:
        '''grpc_endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#grpc_endpoint NetworkSecurityClientTlsPolicy#grpc_endpoint}
        '''
        result = self._values.get("grpc_endpoint")
        return typing.cast(typing.Optional["NetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityClientTlsPolicyServerValidationCa(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityClientTlsPolicy.NetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance",
    jsii_struct_bases=[],
    name_mapping={"plugin_instance": "pluginInstance"},
)
class NetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance:
    def __init__(self, *, plugin_instance: builtins.str) -> None:
        '''
        :param plugin_instance: Plugin instance name, used to locate and load CertificateProvider instance configuration. Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#plugin_instance NetworkSecurityClientTlsPolicy#plugin_instance}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b02678dd2d4ec5c1bb0f206db5f4a6ec13982cfee0de7d717863b30046239042)
            check_type(argname="argument plugin_instance", value=plugin_instance, expected_type=type_hints["plugin_instance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "plugin_instance": plugin_instance,
        }

    @builtins.property
    def plugin_instance(self) -> builtins.str:
        '''Plugin instance name, used to locate and load CertificateProvider instance configuration.

        Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#plugin_instance NetworkSecurityClientTlsPolicy#plugin_instance}
        '''
        result = self._values.get("plugin_instance")
        assert result is not None, "Required property 'plugin_instance' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityClientTlsPolicy.NetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61cd624322b3982f6f8a5df14a4b9eed229a2c931ddb259731f4d51fc991b4a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c370d44fbe2de2b366fadd5e8cd52126b0d8bce1cd80adf920e152b63cf31999)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance]:
        return typing.cast(typing.Optional[NetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5802803e67d98af993336ae49ef0e3309892b912236a076875a62bfdfa578b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityClientTlsPolicy.NetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint",
    jsii_struct_bases=[],
    name_mapping={"target_uri": "targetUri"},
)
class NetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint:
    def __init__(self, *, target_uri: builtins.str) -> None:
        '''
        :param target_uri: The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#target_uri NetworkSecurityClientTlsPolicy#target_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__110ddb92a8f8bca99a8084abd456ff91aab3ed7861b7c0b455622992dd28e51b)
            check_type(argname="argument target_uri", value=target_uri, expected_type=type_hints["target_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_uri": target_uri,
        }

    @builtins.property
    def target_uri(self) -> builtins.str:
        '''The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#target_uri NetworkSecurityClientTlsPolicy#target_uri}
        '''
        result = self._values.get("target_uri")
        assert result is not None, "Required property 'target_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityClientTlsPolicy.NetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24c611e6daf1c4d6769a24c9177b3a1021ca45bd81ba069552d510aa395fddc1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17438b307f1335355e931126ac712ef99e4ae5e7fb1c2204a62e927753ae9fbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint]:
        return typing.cast(typing.Optional[NetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba21f0797a8201cafb7210f28fa88ea04653b852b227b0fef30cf49abf18d10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityClientTlsPolicyServerValidationCaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityClientTlsPolicy.NetworkSecurityClientTlsPolicyServerValidationCaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b4529271bb614f3ab8bbc0f78692af49e54dfa8b240e2ceac5c5b593dd53ace)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkSecurityClientTlsPolicyServerValidationCaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a455ca64d014c57b9cbd853de8535b67dcfababbe4ceadb556dc97802a44c854)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkSecurityClientTlsPolicyServerValidationCaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3068ca8d0a1529c1ad2758a5491f374cf08804a4a4036bb61c798cc63cb78c99)
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
            type_hints = typing.get_type_hints(_typecheckingstub__703b5a5d798685328dfee0836b567689edf58f9ca1933f5ce8b24ef3e4306c8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__181728d68f1f8e4d6d3d47291afeef543c1bd2e515f7c523c2041b926222f5f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityClientTlsPolicyServerValidationCa]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityClientTlsPolicyServerValidationCa]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityClientTlsPolicyServerValidationCa]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__809b58395459da676dac1301d3bae286e518461a67f2d38199772eaa86ca4268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityClientTlsPolicyServerValidationCaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityClientTlsPolicy.NetworkSecurityClientTlsPolicyServerValidationCaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f42974d87f33c11320f45be6c06be44472e2d7df960ad11f4d93b94700aa2ae)
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
        :param plugin_instance: Plugin instance name, used to locate and load CertificateProvider instance configuration. Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#plugin_instance NetworkSecurityClientTlsPolicy#plugin_instance}
        '''
        value = NetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance(
            plugin_instance=plugin_instance
        )

        return typing.cast(None, jsii.invoke(self, "putCertificateProviderInstance", [value]))

    @jsii.member(jsii_name="putGrpcEndpoint")
    def put_grpc_endpoint(self, *, target_uri: builtins.str) -> None:
        '''
        :param target_uri: The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#target_uri NetworkSecurityClientTlsPolicy#target_uri}
        '''
        value = NetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint(
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
    ) -> NetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstanceOutputReference:
        return typing.cast(NetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstanceOutputReference, jsii.get(self, "certificateProviderInstance"))

    @builtins.property
    @jsii.member(jsii_name="grpcEndpoint")
    def grpc_endpoint(
        self,
    ) -> NetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpointOutputReference:
        return typing.cast(NetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpointOutputReference, jsii.get(self, "grpcEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="certificateProviderInstanceInput")
    def certificate_provider_instance_input(
        self,
    ) -> typing.Optional[NetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance]:
        return typing.cast(typing.Optional[NetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance], jsii.get(self, "certificateProviderInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcEndpointInput")
    def grpc_endpoint_input(
        self,
    ) -> typing.Optional[NetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint]:
        return typing.cast(typing.Optional[NetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint], jsii.get(self, "grpcEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityClientTlsPolicyServerValidationCa]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityClientTlsPolicyServerValidationCa]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityClientTlsPolicyServerValidationCa]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03b0649f0bc36a2f9d56da55b701d0e98d2b9919dbacbb2e7cb585291674b9c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityClientTlsPolicy.NetworkSecurityClientTlsPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class NetworkSecurityClientTlsPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#create NetworkSecurityClientTlsPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#delete NetworkSecurityClientTlsPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#update NetworkSecurityClientTlsPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ac0ea6a5451e1fe012443173dff257cf6056045f4e1358d749c2d1087591ab4)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#create NetworkSecurityClientTlsPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#delete NetworkSecurityClientTlsPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_client_tls_policy#update NetworkSecurityClientTlsPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityClientTlsPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityClientTlsPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityClientTlsPolicy.NetworkSecurityClientTlsPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5a8f2f1f3a5c124254e80e6c9c6222ac51a9f2c70547ece8d0b90107c1cdc4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9c91c87159468c722d6f6d79e1ec9c594a56e703a835ba83b35c5527c2ad70a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae8f41bc4d4f95d6963c1325e11118330c546cd2b2dedfd89c8a1b108f1d2294)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__706af90d4d45820b8c97ab2730fa112fc5310974225f21dc4b27673d5a182521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityClientTlsPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityClientTlsPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityClientTlsPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__121579c533803ba18bbdcaa54c110b5587d759f13288d47992646d8ae8d13878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetworkSecurityClientTlsPolicy",
    "NetworkSecurityClientTlsPolicyClientCertificate",
    "NetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance",
    "NetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstanceOutputReference",
    "NetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint",
    "NetworkSecurityClientTlsPolicyClientCertificateGrpcEndpointOutputReference",
    "NetworkSecurityClientTlsPolicyClientCertificateOutputReference",
    "NetworkSecurityClientTlsPolicyConfig",
    "NetworkSecurityClientTlsPolicyServerValidationCa",
    "NetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance",
    "NetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstanceOutputReference",
    "NetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint",
    "NetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpointOutputReference",
    "NetworkSecurityClientTlsPolicyServerValidationCaList",
    "NetworkSecurityClientTlsPolicyServerValidationCaOutputReference",
    "NetworkSecurityClientTlsPolicyTimeouts",
    "NetworkSecurityClientTlsPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b914d1e8bb192c9bcb9f30f0ab2e5cc0fb8e8a134be77b1a3142bc3918ab231f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    client_certificate: typing.Optional[typing.Union[NetworkSecurityClientTlsPolicyClientCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    server_validation_ca: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityClientTlsPolicyServerValidationCa, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sni: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkSecurityClientTlsPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8f7188bfb1edc97a1b8be29af314396160e1ed6534ecf97a28786effa17b4ea5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff50be84df0b4de5d91e15bcb37d25a39e51500fb11286dca6ec77f89a5157d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityClientTlsPolicyServerValidationCa, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec378edb8ea76441542db0b88754fc63711c646a11b368c4ab896e094a854cae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7411d158fb0539930fcfe91fdfb24213f7c5a770af72f73ca51a930a9d3f3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8bd8e2a64c95cce6d8bd8392bf24553a8f630cdb828858149f6344dbb2dee5f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e7d1bba7d9d55f5f722bced349679a6ff43f7b63eb19d38d82bfa722c756f27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe0f9bd3a94c6509c0b0f953e893113ebe6105532ce37943dee0858472516261(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b02e7f3795902d0b8bee2dae4f64792729a66393f6ff70b00748572c9b757101(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77bd7eb5bdbd3b5ae8473895f4647a57a55f900544650c1f24dafddae32b21c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92296b9ce28f34379ed931d27d89b94c63b8a998b3498d70bc8aad12f7123ea0(
    *,
    certificate_provider_instance: typing.Optional[typing.Union[NetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance, typing.Dict[builtins.str, typing.Any]]] = None,
    grpc_endpoint: typing.Optional[typing.Union[NetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f23c2fe70a2902ee2c6220de2783d599599cec2e6e18d4270821dfd5db17b2(
    *,
    plugin_instance: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a345a6042bfefea0cd9855acf3f3ad5ec062fcab337bfb23b8eda8455cc48dd6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db9ea7d91f06395d1a0f740e225f76c924efd44a2523805515aaba679331c92e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58709f384a06e055f2ac47cedd4a48f84c85a2eb681d7efd779ecc5bff50d85e(
    value: typing.Optional[NetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63d14b7e3e0e795053b589ee1d25ee832173e19b4797a2e34198aed0c9ec151(
    *,
    target_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36382491de8dd75fac91eb76dbe2a48a0efcf17357d421a79a64a81f5c9c8597(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9050dd2b02add1a4b86b8b7909ba4bcf5b999fa97e1c9094adfa143c8d026f80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__133a402fc90c59ec8cc85868a016c9ccde3ae0b7801cd17636155ddb15e90cc1(
    value: typing.Optional[NetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e0879a49b4b3b15aba2a130b66a988d7cfbf6318aded4db988837fa178b9aad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2b5287df0c47edab5ac3af89b12ffd6780bc7f33522db33fe72f0cf0cc0dd0(
    value: typing.Optional[NetworkSecurityClientTlsPolicyClientCertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__049e21e03391ad05173e1ebbd1b67b911b8fd8a90200b3a7c825b024da9a72b2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    client_certificate: typing.Optional[typing.Union[NetworkSecurityClientTlsPolicyClientCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    server_validation_ca: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityClientTlsPolicyServerValidationCa, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sni: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkSecurityClientTlsPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ecd1e94e9fdc08e4574fa7d84fb34f53d5e51085a0e01ca7f91d6ce5260e2dc(
    *,
    certificate_provider_instance: typing.Optional[typing.Union[NetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance, typing.Dict[builtins.str, typing.Any]]] = None,
    grpc_endpoint: typing.Optional[typing.Union[NetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b02678dd2d4ec5c1bb0f206db5f4a6ec13982cfee0de7d717863b30046239042(
    *,
    plugin_instance: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61cd624322b3982f6f8a5df14a4b9eed229a2c931ddb259731f4d51fc991b4a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c370d44fbe2de2b366fadd5e8cd52126b0d8bce1cd80adf920e152b63cf31999(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5802803e67d98af993336ae49ef0e3309892b912236a076875a62bfdfa578b8(
    value: typing.Optional[NetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__110ddb92a8f8bca99a8084abd456ff91aab3ed7861b7c0b455622992dd28e51b(
    *,
    target_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24c611e6daf1c4d6769a24c9177b3a1021ca45bd81ba069552d510aa395fddc1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17438b307f1335355e931126ac712ef99e4ae5e7fb1c2204a62e927753ae9fbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba21f0797a8201cafb7210f28fa88ea04653b852b227b0fef30cf49abf18d10(
    value: typing.Optional[NetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b4529271bb614f3ab8bbc0f78692af49e54dfa8b240e2ceac5c5b593dd53ace(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a455ca64d014c57b9cbd853de8535b67dcfababbe4ceadb556dc97802a44c854(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3068ca8d0a1529c1ad2758a5491f374cf08804a4a4036bb61c798cc63cb78c99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__703b5a5d798685328dfee0836b567689edf58f9ca1933f5ce8b24ef3e4306c8f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__181728d68f1f8e4d6d3d47291afeef543c1bd2e515f7c523c2041b926222f5f0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809b58395459da676dac1301d3bae286e518461a67f2d38199772eaa86ca4268(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityClientTlsPolicyServerValidationCa]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f42974d87f33c11320f45be6c06be44472e2d7df960ad11f4d93b94700aa2ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b0649f0bc36a2f9d56da55b701d0e98d2b9919dbacbb2e7cb585291674b9c6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityClientTlsPolicyServerValidationCa]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ac0ea6a5451e1fe012443173dff257cf6056045f4e1358d749c2d1087591ab4(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a8f2f1f3a5c124254e80e6c9c6222ac51a9f2c70547ece8d0b90107c1cdc4c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c91c87159468c722d6f6d79e1ec9c594a56e703a835ba83b35c5527c2ad70a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8f41bc4d4f95d6963c1325e11118330c546cd2b2dedfd89c8a1b108f1d2294(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__706af90d4d45820b8c97ab2730fa112fc5310974225f21dc4b27673d5a182521(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__121579c533803ba18bbdcaa54c110b5587d759f13288d47992646d8ae8d13878(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityClientTlsPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
