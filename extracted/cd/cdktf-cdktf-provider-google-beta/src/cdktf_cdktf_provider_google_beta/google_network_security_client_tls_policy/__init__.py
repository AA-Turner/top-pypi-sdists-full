r'''
# `google_network_security_client_tls_policy`

Refer to the Terraform Registry for docs: [`google_network_security_client_tls_policy`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy).
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


class GoogleNetworkSecurityClientTlsPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityClientTlsPolicy.GoogleNetworkSecurityClientTlsPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy google_network_security_client_tls_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        client_certificate: typing.Optional[typing.Union["GoogleNetworkSecurityClientTlsPolicyClientCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        server_validation_ca: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityClientTlsPolicyServerValidationCa", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sni: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkSecurityClientTlsPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy google_network_security_client_tls_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the ClientTlsPolicy resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#name GoogleNetworkSecurityClientTlsPolicy#name}
        :param client_certificate: client_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#client_certificate GoogleNetworkSecurityClientTlsPolicy#client_certificate}
        :param description: A free-text description of the resource. Max length 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#description GoogleNetworkSecurityClientTlsPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#id GoogleNetworkSecurityClientTlsPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the ClientTlsPolicy resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#labels GoogleNetworkSecurityClientTlsPolicy#labels}
        :param location: The location of the client tls policy. The default value is 'global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#location GoogleNetworkSecurityClientTlsPolicy#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#project GoogleNetworkSecurityClientTlsPolicy#project}.
        :param server_validation_ca: server_validation_ca block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#server_validation_ca GoogleNetworkSecurityClientTlsPolicy#server_validation_ca}
        :param sni: Server Name Indication string to present to the server during TLS handshake. E.g: "secure.example.com". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#sni GoogleNetworkSecurityClientTlsPolicy#sni}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#timeouts GoogleNetworkSecurityClientTlsPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deb72eb40eaf51c83a66c72fe198880bc7e48eabe6a839c99a167f3806ba34d0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleNetworkSecurityClientTlsPolicyConfig(
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
        '''Generates CDKTF code for importing a GoogleNetworkSecurityClientTlsPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleNetworkSecurityClientTlsPolicy to import.
        :param import_from_id: The id of the existing GoogleNetworkSecurityClientTlsPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleNetworkSecurityClientTlsPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2929d96507df41de484c7639753738adc70b25f50580497981eeccaf740efff)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putClientCertificate")
    def put_client_certificate(
        self,
        *,
        certificate_provider_instance: typing.Optional[typing.Union["GoogleNetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        grpc_endpoint: typing.Optional[typing.Union["GoogleNetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param certificate_provider_instance: certificate_provider_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#certificate_provider_instance GoogleNetworkSecurityClientTlsPolicy#certificate_provider_instance}
        :param grpc_endpoint: grpc_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#grpc_endpoint GoogleNetworkSecurityClientTlsPolicy#grpc_endpoint}
        '''
        value = GoogleNetworkSecurityClientTlsPolicyClientCertificate(
            certificate_provider_instance=certificate_provider_instance,
            grpc_endpoint=grpc_endpoint,
        )

        return typing.cast(None, jsii.invoke(self, "putClientCertificate", [value]))

    @jsii.member(jsii_name="putServerValidationCa")
    def put_server_validation_ca(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityClientTlsPolicyServerValidationCa", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1d49602637ec198374c92512932fd7dc1421e1a87928610b9bfd70e99eea619)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#create GoogleNetworkSecurityClientTlsPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#delete GoogleNetworkSecurityClientTlsPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#update GoogleNetworkSecurityClientTlsPolicy#update}.
        '''
        value = GoogleNetworkSecurityClientTlsPolicyTimeouts(
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
    ) -> "GoogleNetworkSecurityClientTlsPolicyClientCertificateOutputReference":
        return typing.cast("GoogleNetworkSecurityClientTlsPolicyClientCertificateOutputReference", jsii.get(self, "clientCertificate"))

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
    ) -> "GoogleNetworkSecurityClientTlsPolicyServerValidationCaList":
        return typing.cast("GoogleNetworkSecurityClientTlsPolicyServerValidationCaList", jsii.get(self, "serverValidationCa"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleNetworkSecurityClientTlsPolicyTimeoutsOutputReference":
        return typing.cast("GoogleNetworkSecurityClientTlsPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateInput")
    def client_certificate_input(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityClientTlsPolicyClientCertificate"]:
        return typing.cast(typing.Optional["GoogleNetworkSecurityClientTlsPolicyClientCertificate"], jsii.get(self, "clientCertificateInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityClientTlsPolicyServerValidationCa"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityClientTlsPolicyServerValidationCa"]]], jsii.get(self, "serverValidationCaInput"))

    @builtins.property
    @jsii.member(jsii_name="sniInput")
    def sni_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sniInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetworkSecurityClientTlsPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetworkSecurityClientTlsPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61d021b266ee7afedc77f6cdfd02b64bf72c9481ad81a91a2809d0c37ea58044)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf970db02fcf676c51726ae9a5ecb650855d51e87c2edd7778cc9037fd0a1f35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec271f80e9af0a724f159290d7ec4623cb45e524a3c7439281f6a4428f3e692b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbffec9feb912d73556ad7388b346218d56549d81ead4bacd19d64cdf3a10df6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc6e3d4dd6f2768ad60a06687af3d9bff2e781dfd91054daf30768910ecd63e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b63941541cf781d24d4586a6fd60d0da64e41839b20f3a5f291a8284e02dc7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sni")
    def sni(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sni"))

    @sni.setter
    def sni(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e05772ff6e797b36db7c9073cf9d7cbfa3c08a415debea135f08bceae61d6889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sni", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityClientTlsPolicy.GoogleNetworkSecurityClientTlsPolicyClientCertificate",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_provider_instance": "certificateProviderInstance",
        "grpc_endpoint": "grpcEndpoint",
    },
)
class GoogleNetworkSecurityClientTlsPolicyClientCertificate:
    def __init__(
        self,
        *,
        certificate_provider_instance: typing.Optional[typing.Union["GoogleNetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        grpc_endpoint: typing.Optional[typing.Union["GoogleNetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param certificate_provider_instance: certificate_provider_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#certificate_provider_instance GoogleNetworkSecurityClientTlsPolicy#certificate_provider_instance}
        :param grpc_endpoint: grpc_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#grpc_endpoint GoogleNetworkSecurityClientTlsPolicy#grpc_endpoint}
        '''
        if isinstance(certificate_provider_instance, dict):
            certificate_provider_instance = GoogleNetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance(**certificate_provider_instance)
        if isinstance(grpc_endpoint, dict):
            grpc_endpoint = GoogleNetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint(**grpc_endpoint)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3a833eef74f59abac0c7aeba96e6648b39067c1afb0605c191adb360a66687b)
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
    ) -> typing.Optional["GoogleNetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance"]:
        '''certificate_provider_instance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#certificate_provider_instance GoogleNetworkSecurityClientTlsPolicy#certificate_provider_instance}
        '''
        result = self._values.get("certificate_provider_instance")
        return typing.cast(typing.Optional["GoogleNetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance"], result)

    @builtins.property
    def grpc_endpoint(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint"]:
        '''grpc_endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#grpc_endpoint GoogleNetworkSecurityClientTlsPolicy#grpc_endpoint}
        '''
        result = self._values.get("grpc_endpoint")
        return typing.cast(typing.Optional["GoogleNetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityClientTlsPolicyClientCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityClientTlsPolicy.GoogleNetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance",
    jsii_struct_bases=[],
    name_mapping={"plugin_instance": "pluginInstance"},
)
class GoogleNetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance:
    def __init__(self, *, plugin_instance: builtins.str) -> None:
        '''
        :param plugin_instance: Plugin instance name, used to locate and load CertificateProvider instance configuration. Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#plugin_instance GoogleNetworkSecurityClientTlsPolicy#plugin_instance}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d5ecfdc880508684ae9670ee5ea0b79c8722482dde5cc4a5879547a9a269ad8)
            check_type(argname="argument plugin_instance", value=plugin_instance, expected_type=type_hints["plugin_instance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "plugin_instance": plugin_instance,
        }

    @builtins.property
    def plugin_instance(self) -> builtins.str:
        '''Plugin instance name, used to locate and load CertificateProvider instance configuration.

        Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#plugin_instance GoogleNetworkSecurityClientTlsPolicy#plugin_instance}
        '''
        result = self._values.get("plugin_instance")
        assert result is not None, "Required property 'plugin_instance' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityClientTlsPolicy.GoogleNetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4a03816781775dc6831db0936b3cf25417a30fc84f7845eac42121b107f6050)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ab03238ba53fb881cd292edf97f0b33b4e5b69cc79aefe94ff6902d95e7a668)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d6e731155a48a993ee49a6d510ea7b9fe6302a7ee9855d75cf8f45022a18b7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityClientTlsPolicy.GoogleNetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint",
    jsii_struct_bases=[],
    name_mapping={"target_uri": "targetUri"},
)
class GoogleNetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint:
    def __init__(self, *, target_uri: builtins.str) -> None:
        '''
        :param target_uri: The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#target_uri GoogleNetworkSecurityClientTlsPolicy#target_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__891276d8044e241665ccf9141797c569bacf77e90751194af752acaff55346eb)
            check_type(argname="argument target_uri", value=target_uri, expected_type=type_hints["target_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_uri": target_uri,
        }

    @builtins.property
    def target_uri(self) -> builtins.str:
        '''The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#target_uri GoogleNetworkSecurityClientTlsPolicy#target_uri}
        '''
        result = self._values.get("target_uri")
        assert result is not None, "Required property 'target_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityClientTlsPolicyClientCertificateGrpcEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityClientTlsPolicy.GoogleNetworkSecurityClientTlsPolicyClientCertificateGrpcEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af4cbd9e3bf983578c088d040feeb0a8f1b4918e276269d183e595cddeac5e2e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5f65931880e303fb609643a984926bee4369cdad3a40afcbb1e8571dcae534c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__064add7b260775e22e307a8b6a6f04c590cffa05a278ede03718a960eaff028f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityClientTlsPolicyClientCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityClientTlsPolicy.GoogleNetworkSecurityClientTlsPolicyClientCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0360252b9af43218d75a710d74b521097d27d07b4040166d6523e005286eec8d)
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
        :param plugin_instance: Plugin instance name, used to locate and load CertificateProvider instance configuration. Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#plugin_instance GoogleNetworkSecurityClientTlsPolicy#plugin_instance}
        '''
        value = GoogleNetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance(
            plugin_instance=plugin_instance
        )

        return typing.cast(None, jsii.invoke(self, "putCertificateProviderInstance", [value]))

    @jsii.member(jsii_name="putGrpcEndpoint")
    def put_grpc_endpoint(self, *, target_uri: builtins.str) -> None:
        '''
        :param target_uri: The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#target_uri GoogleNetworkSecurityClientTlsPolicy#target_uri}
        '''
        value = GoogleNetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint(
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
    ) -> GoogleNetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstanceOutputReference:
        return typing.cast(GoogleNetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstanceOutputReference, jsii.get(self, "certificateProviderInstance"))

    @builtins.property
    @jsii.member(jsii_name="grpcEndpoint")
    def grpc_endpoint(
        self,
    ) -> GoogleNetworkSecurityClientTlsPolicyClientCertificateGrpcEndpointOutputReference:
        return typing.cast(GoogleNetworkSecurityClientTlsPolicyClientCertificateGrpcEndpointOutputReference, jsii.get(self, "grpcEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="certificateProviderInstanceInput")
    def certificate_provider_instance_input(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance], jsii.get(self, "certificateProviderInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcEndpointInput")
    def grpc_endpoint_input(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint], jsii.get(self, "grpcEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityClientTlsPolicyClientCertificate]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityClientTlsPolicyClientCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityClientTlsPolicyClientCertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82575dbc072834f292ec3ff6f3401cc4e654294c7ec2f7b668ef7899059727fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityClientTlsPolicy.GoogleNetworkSecurityClientTlsPolicyConfig",
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
class GoogleNetworkSecurityClientTlsPolicyConfig(
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
        client_certificate: typing.Optional[typing.Union[GoogleNetworkSecurityClientTlsPolicyClientCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        server_validation_ca: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityClientTlsPolicyServerValidationCa", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sni: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkSecurityClientTlsPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the ClientTlsPolicy resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#name GoogleNetworkSecurityClientTlsPolicy#name}
        :param client_certificate: client_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#client_certificate GoogleNetworkSecurityClientTlsPolicy#client_certificate}
        :param description: A free-text description of the resource. Max length 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#description GoogleNetworkSecurityClientTlsPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#id GoogleNetworkSecurityClientTlsPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the ClientTlsPolicy resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#labels GoogleNetworkSecurityClientTlsPolicy#labels}
        :param location: The location of the client tls policy. The default value is 'global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#location GoogleNetworkSecurityClientTlsPolicy#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#project GoogleNetworkSecurityClientTlsPolicy#project}.
        :param server_validation_ca: server_validation_ca block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#server_validation_ca GoogleNetworkSecurityClientTlsPolicy#server_validation_ca}
        :param sni: Server Name Indication string to present to the server during TLS handshake. E.g: "secure.example.com". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#sni GoogleNetworkSecurityClientTlsPolicy#sni}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#timeouts GoogleNetworkSecurityClientTlsPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(client_certificate, dict):
            client_certificate = GoogleNetworkSecurityClientTlsPolicyClientCertificate(**client_certificate)
        if isinstance(timeouts, dict):
            timeouts = GoogleNetworkSecurityClientTlsPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d6ff4c96245c6bbff1c9ddd223b3a26d97faba3983ad619a5c73d7b9f18f663)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#name GoogleNetworkSecurityClientTlsPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_certificate(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityClientTlsPolicyClientCertificate]:
        '''client_certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#client_certificate GoogleNetworkSecurityClientTlsPolicy#client_certificate}
        '''
        result = self._values.get("client_certificate")
        return typing.cast(typing.Optional[GoogleNetworkSecurityClientTlsPolicyClientCertificate], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A free-text description of the resource. Max length 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#description GoogleNetworkSecurityClientTlsPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#id GoogleNetworkSecurityClientTlsPolicy#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#labels GoogleNetworkSecurityClientTlsPolicy#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location of the client tls policy. The default value is 'global'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#location GoogleNetworkSecurityClientTlsPolicy#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#project GoogleNetworkSecurityClientTlsPolicy#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_validation_ca(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityClientTlsPolicyServerValidationCa"]]]:
        '''server_validation_ca block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#server_validation_ca GoogleNetworkSecurityClientTlsPolicy#server_validation_ca}
        '''
        result = self._values.get("server_validation_ca")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityClientTlsPolicyServerValidationCa"]]], result)

    @builtins.property
    def sni(self) -> typing.Optional[builtins.str]:
        '''Server Name Indication string to present to the server during TLS handshake. E.g: "secure.example.com".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#sni GoogleNetworkSecurityClientTlsPolicy#sni}
        '''
        result = self._values.get("sni")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityClientTlsPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#timeouts GoogleNetworkSecurityClientTlsPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleNetworkSecurityClientTlsPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityClientTlsPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityClientTlsPolicy.GoogleNetworkSecurityClientTlsPolicyServerValidationCa",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_provider_instance": "certificateProviderInstance",
        "grpc_endpoint": "grpcEndpoint",
    },
)
class GoogleNetworkSecurityClientTlsPolicyServerValidationCa:
    def __init__(
        self,
        *,
        certificate_provider_instance: typing.Optional[typing.Union["GoogleNetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        grpc_endpoint: typing.Optional[typing.Union["GoogleNetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param certificate_provider_instance: certificate_provider_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#certificate_provider_instance GoogleNetworkSecurityClientTlsPolicy#certificate_provider_instance}
        :param grpc_endpoint: grpc_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#grpc_endpoint GoogleNetworkSecurityClientTlsPolicy#grpc_endpoint}
        '''
        if isinstance(certificate_provider_instance, dict):
            certificate_provider_instance = GoogleNetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance(**certificate_provider_instance)
        if isinstance(grpc_endpoint, dict):
            grpc_endpoint = GoogleNetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint(**grpc_endpoint)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9311348407d67aa912c78cff9f67690edd59ce2b419db6a04feabb747e61bad6)
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
    ) -> typing.Optional["GoogleNetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance"]:
        '''certificate_provider_instance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#certificate_provider_instance GoogleNetworkSecurityClientTlsPolicy#certificate_provider_instance}
        '''
        result = self._values.get("certificate_provider_instance")
        return typing.cast(typing.Optional["GoogleNetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance"], result)

    @builtins.property
    def grpc_endpoint(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint"]:
        '''grpc_endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#grpc_endpoint GoogleNetworkSecurityClientTlsPolicy#grpc_endpoint}
        '''
        result = self._values.get("grpc_endpoint")
        return typing.cast(typing.Optional["GoogleNetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityClientTlsPolicyServerValidationCa(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityClientTlsPolicy.GoogleNetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance",
    jsii_struct_bases=[],
    name_mapping={"plugin_instance": "pluginInstance"},
)
class GoogleNetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance:
    def __init__(self, *, plugin_instance: builtins.str) -> None:
        '''
        :param plugin_instance: Plugin instance name, used to locate and load CertificateProvider instance configuration. Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#plugin_instance GoogleNetworkSecurityClientTlsPolicy#plugin_instance}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4e7fe56caa9b536c854982624b9793e03abb1e1dd72dbeb8104ed955ae0111d)
            check_type(argname="argument plugin_instance", value=plugin_instance, expected_type=type_hints["plugin_instance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "plugin_instance": plugin_instance,
        }

    @builtins.property
    def plugin_instance(self) -> builtins.str:
        '''Plugin instance name, used to locate and load CertificateProvider instance configuration.

        Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#plugin_instance GoogleNetworkSecurityClientTlsPolicy#plugin_instance}
        '''
        result = self._values.get("plugin_instance")
        assert result is not None, "Required property 'plugin_instance' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityClientTlsPolicy.GoogleNetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1833fcde42f99e8f524a181fbfbe5256db778cc6482c6036a736a95ce1c2c3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe31889fe32033f6bf779908369563e0a772347ad14a0d76e312623ffd8ec2ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e11d893a0ba0333e0df7d73ad7587c3d16935a022bba45f15bcd23124304e0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityClientTlsPolicy.GoogleNetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint",
    jsii_struct_bases=[],
    name_mapping={"target_uri": "targetUri"},
)
class GoogleNetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint:
    def __init__(self, *, target_uri: builtins.str) -> None:
        '''
        :param target_uri: The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#target_uri GoogleNetworkSecurityClientTlsPolicy#target_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f8497f38191e74776ee57e6e2f82da4b1013033a3fa5df572c8cddde79f89f8)
            check_type(argname="argument target_uri", value=target_uri, expected_type=type_hints["target_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_uri": target_uri,
        }

    @builtins.property
    def target_uri(self) -> builtins.str:
        '''The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#target_uri GoogleNetworkSecurityClientTlsPolicy#target_uri}
        '''
        result = self._values.get("target_uri")
        assert result is not None, "Required property 'target_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityClientTlsPolicy.GoogleNetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89500d1248a765d0275811fdbb5efe38181cb7dba15d88206c86abd142178759)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecbaf67b45ce89137722804714be6c80f636de3c8ee9983fd10903c78f4492cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3a933858d883122daadfed6fa2e8d0e7f2420a1f09899ac63556294e8ac4e7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityClientTlsPolicyServerValidationCaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityClientTlsPolicy.GoogleNetworkSecurityClientTlsPolicyServerValidationCaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c416ed8bb8896909b2b16e871194eb033dbe2b09ed5018df9ec5ecd4fbf10aba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkSecurityClientTlsPolicyServerValidationCaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7536a2017ec5e1a76953e138f84da6eaeec2f9b04a63e280bda0ad284413535b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkSecurityClientTlsPolicyServerValidationCaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__babb81ae56e0add243ce7ba39a41a3be87b6ea97efc9c42cea3fec08bdcc07f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98edc641af1427c19bb7a59397490f7173b62c843ef851a9928b85135c73a495)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bdbea236c0fd7c14d73fac85879f0cd384285596ab918971a55e167cc11aff2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityClientTlsPolicyServerValidationCa]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityClientTlsPolicyServerValidationCa]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityClientTlsPolicyServerValidationCa]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fc256e67cfca00df06e93f553c0e3e0057e6a18e2c65d6328b12da3347332dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityClientTlsPolicyServerValidationCaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityClientTlsPolicy.GoogleNetworkSecurityClientTlsPolicyServerValidationCaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c7776b65e16f5b46ced5dd869e9d8e0a7bd7f368c24057b25c61d456fafbb83)
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
        :param plugin_instance: Plugin instance name, used to locate and load CertificateProvider instance configuration. Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#plugin_instance GoogleNetworkSecurityClientTlsPolicy#plugin_instance}
        '''
        value = GoogleNetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance(
            plugin_instance=plugin_instance
        )

        return typing.cast(None, jsii.invoke(self, "putCertificateProviderInstance", [value]))

    @jsii.member(jsii_name="putGrpcEndpoint")
    def put_grpc_endpoint(self, *, target_uri: builtins.str) -> None:
        '''
        :param target_uri: The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#target_uri GoogleNetworkSecurityClientTlsPolicy#target_uri}
        '''
        value = GoogleNetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint(
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
    ) -> GoogleNetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstanceOutputReference:
        return typing.cast(GoogleNetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstanceOutputReference, jsii.get(self, "certificateProviderInstance"))

    @builtins.property
    @jsii.member(jsii_name="grpcEndpoint")
    def grpc_endpoint(
        self,
    ) -> GoogleNetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpointOutputReference:
        return typing.cast(GoogleNetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpointOutputReference, jsii.get(self, "grpcEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="certificateProviderInstanceInput")
    def certificate_provider_instance_input(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance], jsii.get(self, "certificateProviderInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcEndpointInput")
    def grpc_endpoint_input(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint], jsii.get(self, "grpcEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityClientTlsPolicyServerValidationCa]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityClientTlsPolicyServerValidationCa]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityClientTlsPolicyServerValidationCa]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83b1f7e1e9ee9fe6f93c1ed58a00882b3b86796c599b9b77285ecfda1eabd1d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityClientTlsPolicy.GoogleNetworkSecurityClientTlsPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleNetworkSecurityClientTlsPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#create GoogleNetworkSecurityClientTlsPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#delete GoogleNetworkSecurityClientTlsPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#update GoogleNetworkSecurityClientTlsPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cd973632dc9716ab7316662c6d45cbac49e85676ceed979dacf0fb17660a240)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#create GoogleNetworkSecurityClientTlsPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#delete GoogleNetworkSecurityClientTlsPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_client_tls_policy#update GoogleNetworkSecurityClientTlsPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityClientTlsPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityClientTlsPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityClientTlsPolicy.GoogleNetworkSecurityClientTlsPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a5636dc5f77e7a01fa4554e5f75f15bac291e9b21c2e51ea92bccf7a3090e6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5f881d5ab68f2da2f624da42e501375b5a85b7a5e7133292690b94d3bb4c091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a78c69c2612e5cfd5b51b35e65121aa4a0b7af75473abbc20582eb6af1716f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75c3c3ee1e86326c9ee29875ac4e3dc4df687a4e2d3f6feeec58a5674b143864)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityClientTlsPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityClientTlsPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityClientTlsPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e80e45a8ecccd0317fab0979f74457cab8af8109a67286d096cada57a157861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleNetworkSecurityClientTlsPolicy",
    "GoogleNetworkSecurityClientTlsPolicyClientCertificate",
    "GoogleNetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance",
    "GoogleNetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstanceOutputReference",
    "GoogleNetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint",
    "GoogleNetworkSecurityClientTlsPolicyClientCertificateGrpcEndpointOutputReference",
    "GoogleNetworkSecurityClientTlsPolicyClientCertificateOutputReference",
    "GoogleNetworkSecurityClientTlsPolicyConfig",
    "GoogleNetworkSecurityClientTlsPolicyServerValidationCa",
    "GoogleNetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance",
    "GoogleNetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstanceOutputReference",
    "GoogleNetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint",
    "GoogleNetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpointOutputReference",
    "GoogleNetworkSecurityClientTlsPolicyServerValidationCaList",
    "GoogleNetworkSecurityClientTlsPolicyServerValidationCaOutputReference",
    "GoogleNetworkSecurityClientTlsPolicyTimeouts",
    "GoogleNetworkSecurityClientTlsPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__deb72eb40eaf51c83a66c72fe198880bc7e48eabe6a839c99a167f3806ba34d0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    client_certificate: typing.Optional[typing.Union[GoogleNetworkSecurityClientTlsPolicyClientCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    server_validation_ca: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityClientTlsPolicyServerValidationCa, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sni: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetworkSecurityClientTlsPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c2929d96507df41de484c7639753738adc70b25f50580497981eeccaf740efff(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d49602637ec198374c92512932fd7dc1421e1a87928610b9bfd70e99eea619(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityClientTlsPolicyServerValidationCa, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61d021b266ee7afedc77f6cdfd02b64bf72c9481ad81a91a2809d0c37ea58044(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf970db02fcf676c51726ae9a5ecb650855d51e87c2edd7778cc9037fd0a1f35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec271f80e9af0a724f159290d7ec4623cb45e524a3c7439281f6a4428f3e692b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbffec9feb912d73556ad7388b346218d56549d81ead4bacd19d64cdf3a10df6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6e3d4dd6f2768ad60a06687af3d9bff2e781dfd91054daf30768910ecd63e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b63941541cf781d24d4586a6fd60d0da64e41839b20f3a5f291a8284e02dc7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e05772ff6e797b36db7c9073cf9d7cbfa3c08a415debea135f08bceae61d6889(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3a833eef74f59abac0c7aeba96e6648b39067c1afb0605c191adb360a66687b(
    *,
    certificate_provider_instance: typing.Optional[typing.Union[GoogleNetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance, typing.Dict[builtins.str, typing.Any]]] = None,
    grpc_endpoint: typing.Optional[typing.Union[GoogleNetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d5ecfdc880508684ae9670ee5ea0b79c8722482dde5cc4a5879547a9a269ad8(
    *,
    plugin_instance: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a03816781775dc6831db0936b3cf25417a30fc84f7845eac42121b107f6050(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ab03238ba53fb881cd292edf97f0b33b4e5b69cc79aefe94ff6902d95e7a668(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d6e731155a48a993ee49a6d510ea7b9fe6302a7ee9855d75cf8f45022a18b7f(
    value: typing.Optional[GoogleNetworkSecurityClientTlsPolicyClientCertificateCertificateProviderInstance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__891276d8044e241665ccf9141797c569bacf77e90751194af752acaff55346eb(
    *,
    target_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af4cbd9e3bf983578c088d040feeb0a8f1b4918e276269d183e595cddeac5e2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5f65931880e303fb609643a984926bee4369cdad3a40afcbb1e8571dcae534c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__064add7b260775e22e307a8b6a6f04c590cffa05a278ede03718a960eaff028f(
    value: typing.Optional[GoogleNetworkSecurityClientTlsPolicyClientCertificateGrpcEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0360252b9af43218d75a710d74b521097d27d07b4040166d6523e005286eec8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82575dbc072834f292ec3ff6f3401cc4e654294c7ec2f7b668ef7899059727fd(
    value: typing.Optional[GoogleNetworkSecurityClientTlsPolicyClientCertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d6ff4c96245c6bbff1c9ddd223b3a26d97faba3983ad619a5c73d7b9f18f663(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    client_certificate: typing.Optional[typing.Union[GoogleNetworkSecurityClientTlsPolicyClientCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    server_validation_ca: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityClientTlsPolicyServerValidationCa, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sni: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetworkSecurityClientTlsPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9311348407d67aa912c78cff9f67690edd59ce2b419db6a04feabb747e61bad6(
    *,
    certificate_provider_instance: typing.Optional[typing.Union[GoogleNetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance, typing.Dict[builtins.str, typing.Any]]] = None,
    grpc_endpoint: typing.Optional[typing.Union[GoogleNetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4e7fe56caa9b536c854982624b9793e03abb1e1dd72dbeb8104ed955ae0111d(
    *,
    plugin_instance: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1833fcde42f99e8f524a181fbfbe5256db778cc6482c6036a736a95ce1c2c3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe31889fe32033f6bf779908369563e0a772347ad14a0d76e312623ffd8ec2ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e11d893a0ba0333e0df7d73ad7587c3d16935a022bba45f15bcd23124304e0d(
    value: typing.Optional[GoogleNetworkSecurityClientTlsPolicyServerValidationCaCertificateProviderInstance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f8497f38191e74776ee57e6e2f82da4b1013033a3fa5df572c8cddde79f89f8(
    *,
    target_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89500d1248a765d0275811fdbb5efe38181cb7dba15d88206c86abd142178759(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecbaf67b45ce89137722804714be6c80f636de3c8ee9983fd10903c78f4492cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a933858d883122daadfed6fa2e8d0e7f2420a1f09899ac63556294e8ac4e7a(
    value: typing.Optional[GoogleNetworkSecurityClientTlsPolicyServerValidationCaGrpcEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c416ed8bb8896909b2b16e871194eb033dbe2b09ed5018df9ec5ecd4fbf10aba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7536a2017ec5e1a76953e138f84da6eaeec2f9b04a63e280bda0ad284413535b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__babb81ae56e0add243ce7ba39a41a3be87b6ea97efc9c42cea3fec08bdcc07f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98edc641af1427c19bb7a59397490f7173b62c843ef851a9928b85135c73a495(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bdbea236c0fd7c14d73fac85879f0cd384285596ab918971a55e167cc11aff2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc256e67cfca00df06e93f553c0e3e0057e6a18e2c65d6328b12da3347332dd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityClientTlsPolicyServerValidationCa]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c7776b65e16f5b46ced5dd869e9d8e0a7bd7f368c24057b25c61d456fafbb83(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b1f7e1e9ee9fe6f93c1ed58a00882b3b86796c599b9b77285ecfda1eabd1d0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityClientTlsPolicyServerValidationCa]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cd973632dc9716ab7316662c6d45cbac49e85676ceed979dacf0fb17660a240(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a5636dc5f77e7a01fa4554e5f75f15bac291e9b21c2e51ea92bccf7a3090e6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f881d5ab68f2da2f624da42e501375b5a85b7a5e7133292690b94d3bb4c091(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a78c69c2612e5cfd5b51b35e65121aa4a0b7af75473abbc20582eb6af1716f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c3c3ee1e86326c9ee29875ac4e3dc4df687a4e2d3f6feeec58a5674b143864(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e80e45a8ecccd0317fab0979f74457cab8af8109a67286d096cada57a157861(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityClientTlsPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
