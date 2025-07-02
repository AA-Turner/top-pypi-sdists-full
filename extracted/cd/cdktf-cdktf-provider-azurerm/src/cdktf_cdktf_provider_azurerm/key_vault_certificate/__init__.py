r'''
# `azurerm_key_vault_certificate`

Refer to the Terraform Registry for docs: [`azurerm_key_vault_certificate`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate).
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


class KeyVaultCertificate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate azurerm_key_vault_certificate}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        key_vault_id: builtins.str,
        name: builtins.str,
        certificate: typing.Optional[typing.Union["KeyVaultCertificateCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        certificate_policy: typing.Optional[typing.Union["KeyVaultCertificateCertificatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["KeyVaultCertificateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate azurerm_key_vault_certificate} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param key_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#key_vault_id KeyVaultCertificate#key_vault_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#name KeyVaultCertificate#name}.
        :param certificate: certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#certificate KeyVaultCertificate#certificate}
        :param certificate_policy: certificate_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#certificate_policy KeyVaultCertificate#certificate_policy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#id KeyVaultCertificate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#tags KeyVaultCertificate#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#timeouts KeyVaultCertificate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a99b35a74b7748ca24f041d124860840389f3ba1eb85546f6b3f03b9f654429)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = KeyVaultCertificateConfig(
            key_vault_id=key_vault_id,
            name=name,
            certificate=certificate,
            certificate_policy=certificate_policy,
            id=id,
            tags=tags,
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
        '''Generates CDKTF code for importing a KeyVaultCertificate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the KeyVaultCertificate to import.
        :param import_from_id: The id of the existing KeyVaultCertificate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the KeyVaultCertificate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e9f52db486f8f06bb8c0dc137b8234c8e17560df88723c5f10ddab52443322a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCertificate")
    def put_certificate(
        self,
        *,
        contents: builtins.str,
        password: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param contents: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#contents KeyVaultCertificate#contents}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#password KeyVaultCertificate#password}.
        '''
        value = KeyVaultCertificateCertificate(contents=contents, password=password)

        return typing.cast(None, jsii.invoke(self, "putCertificate", [value]))

    @jsii.member(jsii_name="putCertificatePolicy")
    def put_certificate_policy(
        self,
        *,
        issuer_parameters: typing.Union["KeyVaultCertificateCertificatePolicyIssuerParameters", typing.Dict[builtins.str, typing.Any]],
        key_properties: typing.Union["KeyVaultCertificateCertificatePolicyKeyProperties", typing.Dict[builtins.str, typing.Any]],
        secret_properties: typing.Union["KeyVaultCertificateCertificatePolicySecretProperties", typing.Dict[builtins.str, typing.Any]],
        lifetime_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KeyVaultCertificateCertificatePolicyLifetimeAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        x509_certificate_properties: typing.Optional[typing.Union["KeyVaultCertificateCertificatePolicyX509CertificateProperties", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param issuer_parameters: issuer_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#issuer_parameters KeyVaultCertificate#issuer_parameters}
        :param key_properties: key_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#key_properties KeyVaultCertificate#key_properties}
        :param secret_properties: secret_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#secret_properties KeyVaultCertificate#secret_properties}
        :param lifetime_action: lifetime_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#lifetime_action KeyVaultCertificate#lifetime_action}
        :param x509_certificate_properties: x509_certificate_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#x509_certificate_properties KeyVaultCertificate#x509_certificate_properties}
        '''
        value = KeyVaultCertificateCertificatePolicy(
            issuer_parameters=issuer_parameters,
            key_properties=key_properties,
            secret_properties=secret_properties,
            lifetime_action=lifetime_action,
            x509_certificate_properties=x509_certificate_properties,
        )

        return typing.cast(None, jsii.invoke(self, "putCertificatePolicy", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#create KeyVaultCertificate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#delete KeyVaultCertificate#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#read KeyVaultCertificate#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#update KeyVaultCertificate#update}.
        '''
        value = KeyVaultCertificateTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetCertificatePolicy")
    def reset_certificate_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificatePolicy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> "KeyVaultCertificateCertificateOutputReference":
        return typing.cast("KeyVaultCertificateCertificateOutputReference", jsii.get(self, "certificate"))

    @builtins.property
    @jsii.member(jsii_name="certificateAttribute")
    def certificate_attribute(self) -> "KeyVaultCertificateCertificateAttributeList":
        return typing.cast("KeyVaultCertificateCertificateAttributeList", jsii.get(self, "certificateAttribute"))

    @builtins.property
    @jsii.member(jsii_name="certificateData")
    def certificate_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateData"))

    @builtins.property
    @jsii.member(jsii_name="certificateDataBase64")
    def certificate_data_base64(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateDataBase64"))

    @builtins.property
    @jsii.member(jsii_name="certificatePolicy")
    def certificate_policy(
        self,
    ) -> "KeyVaultCertificateCertificatePolicyOutputReference":
        return typing.cast("KeyVaultCertificateCertificatePolicyOutputReference", jsii.get(self, "certificatePolicy"))

    @builtins.property
    @jsii.member(jsii_name="resourceManagerId")
    def resource_manager_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceManagerId"))

    @builtins.property
    @jsii.member(jsii_name="resourceManagerVersionlessId")
    def resource_manager_versionless_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceManagerVersionlessId"))

    @builtins.property
    @jsii.member(jsii_name="secretId")
    def secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretId"))

    @builtins.property
    @jsii.member(jsii_name="thumbprint")
    def thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprint"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "KeyVaultCertificateTimeoutsOutputReference":
        return typing.cast("KeyVaultCertificateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="versionlessId")
    def versionless_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionlessId"))

    @builtins.property
    @jsii.member(jsii_name="versionlessSecretId")
    def versionless_secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionlessSecretId"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(self) -> typing.Optional["KeyVaultCertificateCertificate"]:
        return typing.cast(typing.Optional["KeyVaultCertificateCertificate"], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="certificatePolicyInput")
    def certificate_policy_input(
        self,
    ) -> typing.Optional["KeyVaultCertificateCertificatePolicy"]:
        return typing.cast(typing.Optional["KeyVaultCertificateCertificatePolicy"], jsii.get(self, "certificatePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultIdInput")
    def key_vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KeyVaultCertificateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KeyVaultCertificateTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13675c1696965bf0a15af2ff6abf4fa158d4a3255f7b7823b31f0e3623012dae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultId")
    def key_vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultId"))

    @key_vault_id.setter
    def key_vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8d39b76e6c90db9d5ec589d41857842f38d0e0c6cb32f1b98b049dd71a2b0f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3355ef225c585621a66517728193c7d2049b22a186b4abc8d0f73b723a12b80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eb5a87159112dadf3ee8d69615b533eae7987867b6f6766dd8770e3147083c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificate",
    jsii_struct_bases=[],
    name_mapping={"contents": "contents", "password": "password"},
)
class KeyVaultCertificateCertificate:
    def __init__(
        self,
        *,
        contents: builtins.str,
        password: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param contents: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#contents KeyVaultCertificate#contents}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#password KeyVaultCertificate#password}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__940a3afc372bd2322286e6a26cb0dc1d6fbc41852b42b4c46a4099a4a26ee1f6)
            check_type(argname="argument contents", value=contents, expected_type=type_hints["contents"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "contents": contents,
        }
        if password is not None:
            self._values["password"] = password

    @builtins.property
    def contents(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#contents KeyVaultCertificate#contents}.'''
        result = self._values.get("contents")
        assert result is not None, "Required property 'contents' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#password KeyVaultCertificate#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyVaultCertificateCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificateAttribute",
    jsii_struct_bases=[],
    name_mapping={},
)
class KeyVaultCertificateCertificateAttribute:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyVaultCertificateCertificateAttribute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyVaultCertificateCertificateAttributeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificateAttributeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d64e3771086ce2ee3d722567092720dc7132a8506a7752fa07db4f33cf07489)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KeyVaultCertificateCertificateAttributeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c907dba08fdef672c82b6175963b316504b1ec4183a138f3e6ee9d7997e1420)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KeyVaultCertificateCertificateAttributeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd4ad1ec38b48e3b4b92f1f62eea732db69b663ecbe2fd110623e363181a5ab5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d63d3f28a37363a0f83fb14a3275b3330a99309887e9732c8800ca46db840e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6c5b33ebed202811929a2bfa0fd560c6e4857c5bdf9ee74ce8b83efcb40285f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class KeyVaultCertificateCertificateAttributeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificateAttributeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__437ca10e2cc4f0e273b662d0ca4356fd0db3085493f6c7710282e6675a2281e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="created")
    def created(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "created"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="expires")
    def expires(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expires"))

    @builtins.property
    @jsii.member(jsii_name="notBefore")
    def not_before(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notBefore"))

    @builtins.property
    @jsii.member(jsii_name="recoveryLevel")
    def recovery_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recoveryLevel"))

    @builtins.property
    @jsii.member(jsii_name="updated")
    def updated(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updated"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KeyVaultCertificateCertificateAttribute]:
        return typing.cast(typing.Optional[KeyVaultCertificateCertificateAttribute], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KeyVaultCertificateCertificateAttribute],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__042f645a7ff2d4e9d07a66543fd08df2b06d9a71de4a0d8143c994e816c7bc20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KeyVaultCertificateCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec2781319ea06ae6870031b39aef3ac4b6646898a0db2ba83f9f7ea166b099cf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @builtins.property
    @jsii.member(jsii_name="contentsInput")
    def contents_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentsInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="contents")
    def contents(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contents"))

    @contents.setter
    def contents(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ffc11d929d90b2762ef993b11b0960a25fff69dfcca19fa879217097526f88d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7445f4c017d5036817f53cabc930e4f31734255ed42d05fbc9313ae9c357421)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KeyVaultCertificateCertificate]:
        return typing.cast(typing.Optional[KeyVaultCertificateCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KeyVaultCertificateCertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed0846d5050580b6f1d0a37d3922efe4aba44d97582efe4513c471e608289438)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificatePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "issuer_parameters": "issuerParameters",
        "key_properties": "keyProperties",
        "secret_properties": "secretProperties",
        "lifetime_action": "lifetimeAction",
        "x509_certificate_properties": "x509CertificateProperties",
    },
)
class KeyVaultCertificateCertificatePolicy:
    def __init__(
        self,
        *,
        issuer_parameters: typing.Union["KeyVaultCertificateCertificatePolicyIssuerParameters", typing.Dict[builtins.str, typing.Any]],
        key_properties: typing.Union["KeyVaultCertificateCertificatePolicyKeyProperties", typing.Dict[builtins.str, typing.Any]],
        secret_properties: typing.Union["KeyVaultCertificateCertificatePolicySecretProperties", typing.Dict[builtins.str, typing.Any]],
        lifetime_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KeyVaultCertificateCertificatePolicyLifetimeAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        x509_certificate_properties: typing.Optional[typing.Union["KeyVaultCertificateCertificatePolicyX509CertificateProperties", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param issuer_parameters: issuer_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#issuer_parameters KeyVaultCertificate#issuer_parameters}
        :param key_properties: key_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#key_properties KeyVaultCertificate#key_properties}
        :param secret_properties: secret_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#secret_properties KeyVaultCertificate#secret_properties}
        :param lifetime_action: lifetime_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#lifetime_action KeyVaultCertificate#lifetime_action}
        :param x509_certificate_properties: x509_certificate_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#x509_certificate_properties KeyVaultCertificate#x509_certificate_properties}
        '''
        if isinstance(issuer_parameters, dict):
            issuer_parameters = KeyVaultCertificateCertificatePolicyIssuerParameters(**issuer_parameters)
        if isinstance(key_properties, dict):
            key_properties = KeyVaultCertificateCertificatePolicyKeyProperties(**key_properties)
        if isinstance(secret_properties, dict):
            secret_properties = KeyVaultCertificateCertificatePolicySecretProperties(**secret_properties)
        if isinstance(x509_certificate_properties, dict):
            x509_certificate_properties = KeyVaultCertificateCertificatePolicyX509CertificateProperties(**x509_certificate_properties)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c6b8e99bd9df35e7967f22c5232a33c87408d2882a0554e1e8087134a27c7ee)
            check_type(argname="argument issuer_parameters", value=issuer_parameters, expected_type=type_hints["issuer_parameters"])
            check_type(argname="argument key_properties", value=key_properties, expected_type=type_hints["key_properties"])
            check_type(argname="argument secret_properties", value=secret_properties, expected_type=type_hints["secret_properties"])
            check_type(argname="argument lifetime_action", value=lifetime_action, expected_type=type_hints["lifetime_action"])
            check_type(argname="argument x509_certificate_properties", value=x509_certificate_properties, expected_type=type_hints["x509_certificate_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "issuer_parameters": issuer_parameters,
            "key_properties": key_properties,
            "secret_properties": secret_properties,
        }
        if lifetime_action is not None:
            self._values["lifetime_action"] = lifetime_action
        if x509_certificate_properties is not None:
            self._values["x509_certificate_properties"] = x509_certificate_properties

    @builtins.property
    def issuer_parameters(
        self,
    ) -> "KeyVaultCertificateCertificatePolicyIssuerParameters":
        '''issuer_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#issuer_parameters KeyVaultCertificate#issuer_parameters}
        '''
        result = self._values.get("issuer_parameters")
        assert result is not None, "Required property 'issuer_parameters' is missing"
        return typing.cast("KeyVaultCertificateCertificatePolicyIssuerParameters", result)

    @builtins.property
    def key_properties(self) -> "KeyVaultCertificateCertificatePolicyKeyProperties":
        '''key_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#key_properties KeyVaultCertificate#key_properties}
        '''
        result = self._values.get("key_properties")
        assert result is not None, "Required property 'key_properties' is missing"
        return typing.cast("KeyVaultCertificateCertificatePolicyKeyProperties", result)

    @builtins.property
    def secret_properties(
        self,
    ) -> "KeyVaultCertificateCertificatePolicySecretProperties":
        '''secret_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#secret_properties KeyVaultCertificate#secret_properties}
        '''
        result = self._values.get("secret_properties")
        assert result is not None, "Required property 'secret_properties' is missing"
        return typing.cast("KeyVaultCertificateCertificatePolicySecretProperties", result)

    @builtins.property
    def lifetime_action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KeyVaultCertificateCertificatePolicyLifetimeAction"]]]:
        '''lifetime_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#lifetime_action KeyVaultCertificate#lifetime_action}
        '''
        result = self._values.get("lifetime_action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KeyVaultCertificateCertificatePolicyLifetimeAction"]]], result)

    @builtins.property
    def x509_certificate_properties(
        self,
    ) -> typing.Optional["KeyVaultCertificateCertificatePolicyX509CertificateProperties"]:
        '''x509_certificate_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#x509_certificate_properties KeyVaultCertificate#x509_certificate_properties}
        '''
        result = self._values.get("x509_certificate_properties")
        return typing.cast(typing.Optional["KeyVaultCertificateCertificatePolicyX509CertificateProperties"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyVaultCertificateCertificatePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificatePolicyIssuerParameters",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class KeyVaultCertificateCertificatePolicyIssuerParameters:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#name KeyVaultCertificate#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82052023ed8eb058979d9fcc627c15d1293a0d3dd299b45f4daced0690bde02f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#name KeyVaultCertificate#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyVaultCertificateCertificatePolicyIssuerParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyVaultCertificateCertificatePolicyIssuerParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificatePolicyIssuerParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f51679d1b890b4ce326e37a852dfeb837f8f83dcfb3820f46261e8371a4d206a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a9b7090f4c00b79da8acaa15d32c19c72f5da3517fb5cfd12eaf532624fd43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KeyVaultCertificateCertificatePolicyIssuerParameters]:
        return typing.cast(typing.Optional[KeyVaultCertificateCertificatePolicyIssuerParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KeyVaultCertificateCertificatePolicyIssuerParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f4886381d6b24bf9e327534eb7b526d7ebf931caf04bda14c53cf4467f94101)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificatePolicyKeyProperties",
    jsii_struct_bases=[],
    name_mapping={
        "exportable": "exportable",
        "key_type": "keyType",
        "reuse_key": "reuseKey",
        "curve": "curve",
        "key_size": "keySize",
    },
)
class KeyVaultCertificateCertificatePolicyKeyProperties:
    def __init__(
        self,
        *,
        exportable: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        key_type: builtins.str,
        reuse_key: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        curve: typing.Optional[builtins.str] = None,
        key_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param exportable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#exportable KeyVaultCertificate#exportable}.
        :param key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#key_type KeyVaultCertificate#key_type}.
        :param reuse_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#reuse_key KeyVaultCertificate#reuse_key}.
        :param curve: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#curve KeyVaultCertificate#curve}.
        :param key_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#key_size KeyVaultCertificate#key_size}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da4349c081fa313fc0ece1c36ead219b608a661a3e00ca955137e38b55e31013)
            check_type(argname="argument exportable", value=exportable, expected_type=type_hints["exportable"])
            check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
            check_type(argname="argument reuse_key", value=reuse_key, expected_type=type_hints["reuse_key"])
            check_type(argname="argument curve", value=curve, expected_type=type_hints["curve"])
            check_type(argname="argument key_size", value=key_size, expected_type=type_hints["key_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "exportable": exportable,
            "key_type": key_type,
            "reuse_key": reuse_key,
        }
        if curve is not None:
            self._values["curve"] = curve
        if key_size is not None:
            self._values["key_size"] = key_size

    @builtins.property
    def exportable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#exportable KeyVaultCertificate#exportable}.'''
        result = self._values.get("exportable")
        assert result is not None, "Required property 'exportable' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def key_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#key_type KeyVaultCertificate#key_type}.'''
        result = self._values.get("key_type")
        assert result is not None, "Required property 'key_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def reuse_key(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#reuse_key KeyVaultCertificate#reuse_key}.'''
        result = self._values.get("reuse_key")
        assert result is not None, "Required property 'reuse_key' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def curve(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#curve KeyVaultCertificate#curve}.'''
        result = self._values.get("curve")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#key_size KeyVaultCertificate#key_size}.'''
        result = self._values.get("key_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyVaultCertificateCertificatePolicyKeyProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyVaultCertificateCertificatePolicyKeyPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificatePolicyKeyPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4de8d09212b8199802e502d19699c2c894bd0acdd93e73ff3b573ebe2c6e3973)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCurve")
    def reset_curve(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCurve", []))

    @jsii.member(jsii_name="resetKeySize")
    def reset_key_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeySize", []))

    @builtins.property
    @jsii.member(jsii_name="curveInput")
    def curve_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "curveInput"))

    @builtins.property
    @jsii.member(jsii_name="exportableInput")
    def exportable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "exportableInput"))

    @builtins.property
    @jsii.member(jsii_name="keySizeInput")
    def key_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keySizeInput"))

    @builtins.property
    @jsii.member(jsii_name="keyTypeInput")
    def key_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="reuseKeyInput")
    def reuse_key_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "reuseKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="curve")
    def curve(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "curve"))

    @curve.setter
    def curve(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea1563618c251c67528970004ff8e4d18eeb00b6e8014173857ed5f0ae1820d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "curve", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exportable")
    def exportable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "exportable"))

    @exportable.setter
    def exportable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1873d4961c3a2afcd002e74fd893b0e5b63b054e50a1e9e8bf327574f11396ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exportable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keySize")
    def key_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keySize"))

    @key_size.setter
    def key_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd58f07e41a37d0e15e8ecbceb1f9de0c4205165a5855757a7a6eee3e1aa5a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keySize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyType")
    def key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyType"))

    @key_type.setter
    def key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e0e27250f74e56734040dd178c6ef418b91d42db7b6bb546dc024a230957185)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reuseKey")
    def reuse_key(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "reuseKey"))

    @reuse_key.setter
    def reuse_key(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0776d65e06d9eb05fb1ab7e510b07dadb0914d9dfc68969d1f4ecf7ed7b43c78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reuseKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KeyVaultCertificateCertificatePolicyKeyProperties]:
        return typing.cast(typing.Optional[KeyVaultCertificateCertificatePolicyKeyProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KeyVaultCertificateCertificatePolicyKeyProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21142730244cc7b01771057c622373da8d807a02c4bcd7c91ae9d82fbd1ad6db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificatePolicyLifetimeAction",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "trigger": "trigger"},
)
class KeyVaultCertificateCertificatePolicyLifetimeAction:
    def __init__(
        self,
        *,
        action: typing.Union["KeyVaultCertificateCertificatePolicyLifetimeActionAction", typing.Dict[builtins.str, typing.Any]],
        trigger: typing.Union["KeyVaultCertificateCertificatePolicyLifetimeActionTrigger", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#action KeyVaultCertificate#action}
        :param trigger: trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#trigger KeyVaultCertificate#trigger}
        '''
        if isinstance(action, dict):
            action = KeyVaultCertificateCertificatePolicyLifetimeActionAction(**action)
        if isinstance(trigger, dict):
            trigger = KeyVaultCertificateCertificatePolicyLifetimeActionTrigger(**trigger)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a09bf2d92761c2e9b9741533f6544fd9278acf8d40679e954ddeae4460f0853)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument trigger", value=trigger, expected_type=type_hints["trigger"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "trigger": trigger,
        }

    @builtins.property
    def action(self) -> "KeyVaultCertificateCertificatePolicyLifetimeActionAction":
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#action KeyVaultCertificate#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("KeyVaultCertificateCertificatePolicyLifetimeActionAction", result)

    @builtins.property
    def trigger(self) -> "KeyVaultCertificateCertificatePolicyLifetimeActionTrigger":
        '''trigger block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#trigger KeyVaultCertificate#trigger}
        '''
        result = self._values.get("trigger")
        assert result is not None, "Required property 'trigger' is missing"
        return typing.cast("KeyVaultCertificateCertificatePolicyLifetimeActionTrigger", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyVaultCertificateCertificatePolicyLifetimeAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificatePolicyLifetimeActionAction",
    jsii_struct_bases=[],
    name_mapping={"action_type": "actionType"},
)
class KeyVaultCertificateCertificatePolicyLifetimeActionAction:
    def __init__(self, *, action_type: builtins.str) -> None:
        '''
        :param action_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#action_type KeyVaultCertificate#action_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8531a4571088787c741f9025d90a3835c202dbc737370af74cda43ffd8c29d58)
            check_type(argname="argument action_type", value=action_type, expected_type=type_hints["action_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_type": action_type,
        }

    @builtins.property
    def action_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#action_type KeyVaultCertificate#action_type}.'''
        result = self._values.get("action_type")
        assert result is not None, "Required property 'action_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyVaultCertificateCertificatePolicyLifetimeActionAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyVaultCertificateCertificatePolicyLifetimeActionActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificatePolicyLifetimeActionActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2494433790c650a6099926a24a57497c69050c3903ffdffbc3a61a6e9536dbdf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="actionTypeInput")
    def action_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="actionType")
    def action_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionType"))

    @action_type.setter
    def action_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c55d36e24081f6c75f647022bd879476576239567871fbb8a1584fe7f5d36ca0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KeyVaultCertificateCertificatePolicyLifetimeActionAction]:
        return typing.cast(typing.Optional[KeyVaultCertificateCertificatePolicyLifetimeActionAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KeyVaultCertificateCertificatePolicyLifetimeActionAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f58295c97de192cb069ae0078420c96138a21124152cdde2c3edae5caaa09a5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KeyVaultCertificateCertificatePolicyLifetimeActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificatePolicyLifetimeActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56a0b774f474fa2ca7490dec39d95d5241b2648d61b75489adb1b4f2ede52fdc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KeyVaultCertificateCertificatePolicyLifetimeActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b0427775b3120e4178d14cd4e70f618b1904e70ca654671a3afda7c6ca834bc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KeyVaultCertificateCertificatePolicyLifetimeActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7cf89724e1a97f89fd01e52bcf752c2bd83e530ece5e882241f30d415dce19a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e16e9fcba70b5a97f5dbf8d33dff45e949c2f0dd71d530618d034758f9c1b006)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17b1b3823e846333072798400f17471ab7663843d5f8c31ed2ed92dc16facca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyVaultCertificateCertificatePolicyLifetimeAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyVaultCertificateCertificatePolicyLifetimeAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyVaultCertificateCertificatePolicyLifetimeAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__763d00855fa1ada02df35dc58def825174373d6f55f7a2cd17a5c0b541cbaa53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KeyVaultCertificateCertificatePolicyLifetimeActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificatePolicyLifetimeActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7fb17fffafc750e39aefa4254c9beba49c9bd2b55765c474fd4abe3735f0334)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAction")
    def put_action(self, *, action_type: builtins.str) -> None:
        '''
        :param action_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#action_type KeyVaultCertificate#action_type}.
        '''
        value = KeyVaultCertificateCertificatePolicyLifetimeActionAction(
            action_type=action_type
        )

        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putTrigger")
    def put_trigger(
        self,
        *,
        days_before_expiry: typing.Optional[jsii.Number] = None,
        lifetime_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param days_before_expiry: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#days_before_expiry KeyVaultCertificate#days_before_expiry}.
        :param lifetime_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#lifetime_percentage KeyVaultCertificate#lifetime_percentage}.
        '''
        value = KeyVaultCertificateCertificatePolicyLifetimeActionTrigger(
            days_before_expiry=days_before_expiry,
            lifetime_percentage=lifetime_percentage,
        )

        return typing.cast(None, jsii.invoke(self, "putTrigger", [value]))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(
        self,
    ) -> KeyVaultCertificateCertificatePolicyLifetimeActionActionOutputReference:
        return typing.cast(KeyVaultCertificateCertificatePolicyLifetimeActionActionOutputReference, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="trigger")
    def trigger(
        self,
    ) -> "KeyVaultCertificateCertificatePolicyLifetimeActionTriggerOutputReference":
        return typing.cast("KeyVaultCertificateCertificatePolicyLifetimeActionTriggerOutputReference", jsii.get(self, "trigger"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(
        self,
    ) -> typing.Optional[KeyVaultCertificateCertificatePolicyLifetimeActionAction]:
        return typing.cast(typing.Optional[KeyVaultCertificateCertificatePolicyLifetimeActionAction], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerInput")
    def trigger_input(
        self,
    ) -> typing.Optional["KeyVaultCertificateCertificatePolicyLifetimeActionTrigger"]:
        return typing.cast(typing.Optional["KeyVaultCertificateCertificatePolicyLifetimeActionTrigger"], jsii.get(self, "triggerInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyVaultCertificateCertificatePolicyLifetimeAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyVaultCertificateCertificatePolicyLifetimeAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyVaultCertificateCertificatePolicyLifetimeAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3c01858a60a8c297c51a80e53953e912d64c3a974c1fc8e36d716476c35690f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificatePolicyLifetimeActionTrigger",
    jsii_struct_bases=[],
    name_mapping={
        "days_before_expiry": "daysBeforeExpiry",
        "lifetime_percentage": "lifetimePercentage",
    },
)
class KeyVaultCertificateCertificatePolicyLifetimeActionTrigger:
    def __init__(
        self,
        *,
        days_before_expiry: typing.Optional[jsii.Number] = None,
        lifetime_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param days_before_expiry: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#days_before_expiry KeyVaultCertificate#days_before_expiry}.
        :param lifetime_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#lifetime_percentage KeyVaultCertificate#lifetime_percentage}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4cedbc6bb18f045cd403c454f9dd556406c56b67e5d3f548d43a5eea4792fd6)
            check_type(argname="argument days_before_expiry", value=days_before_expiry, expected_type=type_hints["days_before_expiry"])
            check_type(argname="argument lifetime_percentage", value=lifetime_percentage, expected_type=type_hints["lifetime_percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if days_before_expiry is not None:
            self._values["days_before_expiry"] = days_before_expiry
        if lifetime_percentage is not None:
            self._values["lifetime_percentage"] = lifetime_percentage

    @builtins.property
    def days_before_expiry(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#days_before_expiry KeyVaultCertificate#days_before_expiry}.'''
        result = self._values.get("days_before_expiry")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def lifetime_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#lifetime_percentage KeyVaultCertificate#lifetime_percentage}.'''
        result = self._values.get("lifetime_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyVaultCertificateCertificatePolicyLifetimeActionTrigger(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyVaultCertificateCertificatePolicyLifetimeActionTriggerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificatePolicyLifetimeActionTriggerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f864975626c57754174b7ed15ebac52f8079a93dd2449b4be9577a0c0d6c9e80)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDaysBeforeExpiry")
    def reset_days_before_expiry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDaysBeforeExpiry", []))

    @jsii.member(jsii_name="resetLifetimePercentage")
    def reset_lifetime_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifetimePercentage", []))

    @builtins.property
    @jsii.member(jsii_name="daysBeforeExpiryInput")
    def days_before_expiry_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "daysBeforeExpiryInput"))

    @builtins.property
    @jsii.member(jsii_name="lifetimePercentageInput")
    def lifetime_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lifetimePercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="daysBeforeExpiry")
    def days_before_expiry(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "daysBeforeExpiry"))

    @days_before_expiry.setter
    def days_before_expiry(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__177c399eedc840d7ac68a5a5b146d6d9de94f3c2dc7bc92472d0b8b9cf0063ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysBeforeExpiry", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lifetimePercentage")
    def lifetime_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lifetimePercentage"))

    @lifetime_percentage.setter
    def lifetime_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__282d5eefde5ec496485f74404ce3ac14cf9e8aa48a49c30b13aa5d088072befa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifetimePercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KeyVaultCertificateCertificatePolicyLifetimeActionTrigger]:
        return typing.cast(typing.Optional[KeyVaultCertificateCertificatePolicyLifetimeActionTrigger], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KeyVaultCertificateCertificatePolicyLifetimeActionTrigger],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fac38411eaae1cebc27a95b3a0448e815d0cbdc5ed3ec6aa445fae77e2388aa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KeyVaultCertificateCertificatePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificatePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a78f5035fa1f966bf1bd98a4a01867d5e970c56423fa7bded51ad4eb5454b21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIssuerParameters")
    def put_issuer_parameters(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#name KeyVaultCertificate#name}.
        '''
        value = KeyVaultCertificateCertificatePolicyIssuerParameters(name=name)

        return typing.cast(None, jsii.invoke(self, "putIssuerParameters", [value]))

    @jsii.member(jsii_name="putKeyProperties")
    def put_key_properties(
        self,
        *,
        exportable: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        key_type: builtins.str,
        reuse_key: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        curve: typing.Optional[builtins.str] = None,
        key_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param exportable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#exportable KeyVaultCertificate#exportable}.
        :param key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#key_type KeyVaultCertificate#key_type}.
        :param reuse_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#reuse_key KeyVaultCertificate#reuse_key}.
        :param curve: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#curve KeyVaultCertificate#curve}.
        :param key_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#key_size KeyVaultCertificate#key_size}.
        '''
        value = KeyVaultCertificateCertificatePolicyKeyProperties(
            exportable=exportable,
            key_type=key_type,
            reuse_key=reuse_key,
            curve=curve,
            key_size=key_size,
        )

        return typing.cast(None, jsii.invoke(self, "putKeyProperties", [value]))

    @jsii.member(jsii_name="putLifetimeAction")
    def put_lifetime_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KeyVaultCertificateCertificatePolicyLifetimeAction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff00e4477a10a04d3a79082354aaf0b549795f0f73675274ad554aeeb538f46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLifetimeAction", [value]))

    @jsii.member(jsii_name="putSecretProperties")
    def put_secret_properties(self, *, content_type: builtins.str) -> None:
        '''
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#content_type KeyVaultCertificate#content_type}.
        '''
        value = KeyVaultCertificateCertificatePolicySecretProperties(
            content_type=content_type
        )

        return typing.cast(None, jsii.invoke(self, "putSecretProperties", [value]))

    @jsii.member(jsii_name="putX509CertificateProperties")
    def put_x509_certificate_properties(
        self,
        *,
        key_usage: typing.Sequence[builtins.str],
        subject: builtins.str,
        validity_in_months: jsii.Number,
        extended_key_usage: typing.Optional[typing.Sequence[builtins.str]] = None,
        subject_alternative_names: typing.Optional[typing.Union["KeyVaultCertificateCertificatePolicyX509CertificatePropertiesSubjectAlternativeNames", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param key_usage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#key_usage KeyVaultCertificate#key_usage}.
        :param subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#subject KeyVaultCertificate#subject}.
        :param validity_in_months: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#validity_in_months KeyVaultCertificate#validity_in_months}.
        :param extended_key_usage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#extended_key_usage KeyVaultCertificate#extended_key_usage}.
        :param subject_alternative_names: subject_alternative_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#subject_alternative_names KeyVaultCertificate#subject_alternative_names}
        '''
        value = KeyVaultCertificateCertificatePolicyX509CertificateProperties(
            key_usage=key_usage,
            subject=subject,
            validity_in_months=validity_in_months,
            extended_key_usage=extended_key_usage,
            subject_alternative_names=subject_alternative_names,
        )

        return typing.cast(None, jsii.invoke(self, "putX509CertificateProperties", [value]))

    @jsii.member(jsii_name="resetLifetimeAction")
    def reset_lifetime_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifetimeAction", []))

    @jsii.member(jsii_name="resetX509CertificateProperties")
    def reset_x509_certificate_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetX509CertificateProperties", []))

    @builtins.property
    @jsii.member(jsii_name="issuerParameters")
    def issuer_parameters(
        self,
    ) -> KeyVaultCertificateCertificatePolicyIssuerParametersOutputReference:
        return typing.cast(KeyVaultCertificateCertificatePolicyIssuerParametersOutputReference, jsii.get(self, "issuerParameters"))

    @builtins.property
    @jsii.member(jsii_name="keyProperties")
    def key_properties(
        self,
    ) -> KeyVaultCertificateCertificatePolicyKeyPropertiesOutputReference:
        return typing.cast(KeyVaultCertificateCertificatePolicyKeyPropertiesOutputReference, jsii.get(self, "keyProperties"))

    @builtins.property
    @jsii.member(jsii_name="lifetimeAction")
    def lifetime_action(self) -> KeyVaultCertificateCertificatePolicyLifetimeActionList:
        return typing.cast(KeyVaultCertificateCertificatePolicyLifetimeActionList, jsii.get(self, "lifetimeAction"))

    @builtins.property
    @jsii.member(jsii_name="secretProperties")
    def secret_properties(
        self,
    ) -> "KeyVaultCertificateCertificatePolicySecretPropertiesOutputReference":
        return typing.cast("KeyVaultCertificateCertificatePolicySecretPropertiesOutputReference", jsii.get(self, "secretProperties"))

    @builtins.property
    @jsii.member(jsii_name="x509CertificateProperties")
    def x509_certificate_properties(
        self,
    ) -> "KeyVaultCertificateCertificatePolicyX509CertificatePropertiesOutputReference":
        return typing.cast("KeyVaultCertificateCertificatePolicyX509CertificatePropertiesOutputReference", jsii.get(self, "x509CertificateProperties"))

    @builtins.property
    @jsii.member(jsii_name="issuerParametersInput")
    def issuer_parameters_input(
        self,
    ) -> typing.Optional[KeyVaultCertificateCertificatePolicyIssuerParameters]:
        return typing.cast(typing.Optional[KeyVaultCertificateCertificatePolicyIssuerParameters], jsii.get(self, "issuerParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="keyPropertiesInput")
    def key_properties_input(
        self,
    ) -> typing.Optional[KeyVaultCertificateCertificatePolicyKeyProperties]:
        return typing.cast(typing.Optional[KeyVaultCertificateCertificatePolicyKeyProperties], jsii.get(self, "keyPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="lifetimeActionInput")
    def lifetime_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyVaultCertificateCertificatePolicyLifetimeAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyVaultCertificateCertificatePolicyLifetimeAction]]], jsii.get(self, "lifetimeActionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretPropertiesInput")
    def secret_properties_input(
        self,
    ) -> typing.Optional["KeyVaultCertificateCertificatePolicySecretProperties"]:
        return typing.cast(typing.Optional["KeyVaultCertificateCertificatePolicySecretProperties"], jsii.get(self, "secretPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="x509CertificatePropertiesInput")
    def x509_certificate_properties_input(
        self,
    ) -> typing.Optional["KeyVaultCertificateCertificatePolicyX509CertificateProperties"]:
        return typing.cast(typing.Optional["KeyVaultCertificateCertificatePolicyX509CertificateProperties"], jsii.get(self, "x509CertificatePropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KeyVaultCertificateCertificatePolicy]:
        return typing.cast(typing.Optional[KeyVaultCertificateCertificatePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KeyVaultCertificateCertificatePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c99adfead2cf84815320e8a04cc74112bcf67ab2ae3718044197a7349d348fb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificatePolicySecretProperties",
    jsii_struct_bases=[],
    name_mapping={"content_type": "contentType"},
)
class KeyVaultCertificateCertificatePolicySecretProperties:
    def __init__(self, *, content_type: builtins.str) -> None:
        '''
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#content_type KeyVaultCertificate#content_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa965482a24fceaf73094cc633020ecfe9d225c7c833f1e03d1d62ddd3ef3d2c)
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content_type": content_type,
        }

    @builtins.property
    def content_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#content_type KeyVaultCertificate#content_type}.'''
        result = self._values.get("content_type")
        assert result is not None, "Required property 'content_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyVaultCertificateCertificatePolicySecretProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyVaultCertificateCertificatePolicySecretPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificatePolicySecretPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c150ffaef68ad49e9201352b2a6d08f9fda8810bfcbdf2d46ae19bcab37d8a70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc3c525bef53cee55f5e807c02bbc03291c0f019082c9837fe6a36742dc2273b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KeyVaultCertificateCertificatePolicySecretProperties]:
        return typing.cast(typing.Optional[KeyVaultCertificateCertificatePolicySecretProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KeyVaultCertificateCertificatePolicySecretProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5005a9920d4c9537071ad2b39c631844e1d4c27e90c8b94f251ba7aa3c5119d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificatePolicyX509CertificateProperties",
    jsii_struct_bases=[],
    name_mapping={
        "key_usage": "keyUsage",
        "subject": "subject",
        "validity_in_months": "validityInMonths",
        "extended_key_usage": "extendedKeyUsage",
        "subject_alternative_names": "subjectAlternativeNames",
    },
)
class KeyVaultCertificateCertificatePolicyX509CertificateProperties:
    def __init__(
        self,
        *,
        key_usage: typing.Sequence[builtins.str],
        subject: builtins.str,
        validity_in_months: jsii.Number,
        extended_key_usage: typing.Optional[typing.Sequence[builtins.str]] = None,
        subject_alternative_names: typing.Optional[typing.Union["KeyVaultCertificateCertificatePolicyX509CertificatePropertiesSubjectAlternativeNames", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param key_usage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#key_usage KeyVaultCertificate#key_usage}.
        :param subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#subject KeyVaultCertificate#subject}.
        :param validity_in_months: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#validity_in_months KeyVaultCertificate#validity_in_months}.
        :param extended_key_usage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#extended_key_usage KeyVaultCertificate#extended_key_usage}.
        :param subject_alternative_names: subject_alternative_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#subject_alternative_names KeyVaultCertificate#subject_alternative_names}
        '''
        if isinstance(subject_alternative_names, dict):
            subject_alternative_names = KeyVaultCertificateCertificatePolicyX509CertificatePropertiesSubjectAlternativeNames(**subject_alternative_names)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb9053f72d5d54a32e2aac9c6ab097747be064565bf51bac2c61b293b56c6a43)
            check_type(argname="argument key_usage", value=key_usage, expected_type=type_hints["key_usage"])
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            check_type(argname="argument validity_in_months", value=validity_in_months, expected_type=type_hints["validity_in_months"])
            check_type(argname="argument extended_key_usage", value=extended_key_usage, expected_type=type_hints["extended_key_usage"])
            check_type(argname="argument subject_alternative_names", value=subject_alternative_names, expected_type=type_hints["subject_alternative_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_usage": key_usage,
            "subject": subject,
            "validity_in_months": validity_in_months,
        }
        if extended_key_usage is not None:
            self._values["extended_key_usage"] = extended_key_usage
        if subject_alternative_names is not None:
            self._values["subject_alternative_names"] = subject_alternative_names

    @builtins.property
    def key_usage(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#key_usage KeyVaultCertificate#key_usage}.'''
        result = self._values.get("key_usage")
        assert result is not None, "Required property 'key_usage' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def subject(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#subject KeyVaultCertificate#subject}.'''
        result = self._values.get("subject")
        assert result is not None, "Required property 'subject' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def validity_in_months(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#validity_in_months KeyVaultCertificate#validity_in_months}.'''
        result = self._values.get("validity_in_months")
        assert result is not None, "Required property 'validity_in_months' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def extended_key_usage(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#extended_key_usage KeyVaultCertificate#extended_key_usage}.'''
        result = self._values.get("extended_key_usage")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subject_alternative_names(
        self,
    ) -> typing.Optional["KeyVaultCertificateCertificatePolicyX509CertificatePropertiesSubjectAlternativeNames"]:
        '''subject_alternative_names block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#subject_alternative_names KeyVaultCertificate#subject_alternative_names}
        '''
        result = self._values.get("subject_alternative_names")
        return typing.cast(typing.Optional["KeyVaultCertificateCertificatePolicyX509CertificatePropertiesSubjectAlternativeNames"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyVaultCertificateCertificatePolicyX509CertificateProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyVaultCertificateCertificatePolicyX509CertificatePropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificatePolicyX509CertificatePropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dbe3bc97652df2c45c0b6a2c892291b8ba49523997ca4778a0561f4f5d7fa1f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSubjectAlternativeNames")
    def put_subject_alternative_names(
        self,
        *,
        dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        emails: typing.Optional[typing.Sequence[builtins.str]] = None,
        upns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param dns_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#dns_names KeyVaultCertificate#dns_names}.
        :param emails: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#emails KeyVaultCertificate#emails}.
        :param upns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#upns KeyVaultCertificate#upns}.
        '''
        value = KeyVaultCertificateCertificatePolicyX509CertificatePropertiesSubjectAlternativeNames(
            dns_names=dns_names, emails=emails, upns=upns
        )

        return typing.cast(None, jsii.invoke(self, "putSubjectAlternativeNames", [value]))

    @jsii.member(jsii_name="resetExtendedKeyUsage")
    def reset_extended_key_usage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtendedKeyUsage", []))

    @jsii.member(jsii_name="resetSubjectAlternativeNames")
    def reset_subject_alternative_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectAlternativeNames", []))

    @builtins.property
    @jsii.member(jsii_name="subjectAlternativeNames")
    def subject_alternative_names(
        self,
    ) -> "KeyVaultCertificateCertificatePolicyX509CertificatePropertiesSubjectAlternativeNamesOutputReference":
        return typing.cast("KeyVaultCertificateCertificatePolicyX509CertificatePropertiesSubjectAlternativeNamesOutputReference", jsii.get(self, "subjectAlternativeNames"))

    @builtins.property
    @jsii.member(jsii_name="extendedKeyUsageInput")
    def extended_key_usage_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "extendedKeyUsageInput"))

    @builtins.property
    @jsii.member(jsii_name="keyUsageInput")
    def key_usage_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "keyUsageInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectAlternativeNamesInput")
    def subject_alternative_names_input(
        self,
    ) -> typing.Optional["KeyVaultCertificateCertificatePolicyX509CertificatePropertiesSubjectAlternativeNames"]:
        return typing.cast(typing.Optional["KeyVaultCertificateCertificatePolicyX509CertificatePropertiesSubjectAlternativeNames"], jsii.get(self, "subjectAlternativeNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectInput")
    def subject_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectInput"))

    @builtins.property
    @jsii.member(jsii_name="validityInMonthsInput")
    def validity_in_months_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "validityInMonthsInput"))

    @builtins.property
    @jsii.member(jsii_name="extendedKeyUsage")
    def extended_key_usage(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "extendedKeyUsage"))

    @extended_key_usage.setter
    def extended_key_usage(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95cf7dce7901e171093871b46362b3adc97e14363ce1ef727daf8b18a81ded6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extendedKeyUsage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyUsage")
    def key_usage(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "keyUsage"))

    @key_usage.setter
    def key_usage(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34f78baf743766000114383bb12887e69d7f1f6a6cc19598ff7752dac538a4ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyUsage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @subject.setter
    def subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2803acbd51a30448fd6c8846c8a25476fe33c85dcd0ad24d94b0791674198a1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validityInMonths")
    def validity_in_months(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "validityInMonths"))

    @validity_in_months.setter
    def validity_in_months(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be320243aa2da495f7bb7ff3febda452d184fbed07eba9f720e111682a92fbdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validityInMonths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KeyVaultCertificateCertificatePolicyX509CertificateProperties]:
        return typing.cast(typing.Optional[KeyVaultCertificateCertificatePolicyX509CertificateProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KeyVaultCertificateCertificatePolicyX509CertificateProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb61ec5b92cec2b5f6a3fe71e6ab6b38f712074f0074dd0c492cb577c879aa0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificatePolicyX509CertificatePropertiesSubjectAlternativeNames",
    jsii_struct_bases=[],
    name_mapping={"dns_names": "dnsNames", "emails": "emails", "upns": "upns"},
)
class KeyVaultCertificateCertificatePolicyX509CertificatePropertiesSubjectAlternativeNames:
    def __init__(
        self,
        *,
        dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        emails: typing.Optional[typing.Sequence[builtins.str]] = None,
        upns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param dns_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#dns_names KeyVaultCertificate#dns_names}.
        :param emails: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#emails KeyVaultCertificate#emails}.
        :param upns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#upns KeyVaultCertificate#upns}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92cd8f5c9e83de5c1e47b50724d9767473baa7bb6de2494b9ade6b68182709a4)
            check_type(argname="argument dns_names", value=dns_names, expected_type=type_hints["dns_names"])
            check_type(argname="argument emails", value=emails, expected_type=type_hints["emails"])
            check_type(argname="argument upns", value=upns, expected_type=type_hints["upns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dns_names is not None:
            self._values["dns_names"] = dns_names
        if emails is not None:
            self._values["emails"] = emails
        if upns is not None:
            self._values["upns"] = upns

    @builtins.property
    def dns_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#dns_names KeyVaultCertificate#dns_names}.'''
        result = self._values.get("dns_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def emails(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#emails KeyVaultCertificate#emails}.'''
        result = self._values.get("emails")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def upns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#upns KeyVaultCertificate#upns}.'''
        result = self._values.get("upns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyVaultCertificateCertificatePolicyX509CertificatePropertiesSubjectAlternativeNames(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyVaultCertificateCertificatePolicyX509CertificatePropertiesSubjectAlternativeNamesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateCertificatePolicyX509CertificatePropertiesSubjectAlternativeNamesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa5b5dc72c9626bb61af0f99c5bea582845e57123f833e32f6739c85713406fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDnsNames")
    def reset_dns_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsNames", []))

    @jsii.member(jsii_name="resetEmails")
    def reset_emails(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmails", []))

    @jsii.member(jsii_name="resetUpns")
    def reset_upns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpns", []))

    @builtins.property
    @jsii.member(jsii_name="dnsNamesInput")
    def dns_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dnsNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="emailsInput")
    def emails_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailsInput"))

    @builtins.property
    @jsii.member(jsii_name="upnsInput")
    def upns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "upnsInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsNames")
    def dns_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dnsNames"))

    @dns_names.setter
    def dns_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6816722e4ddd996fdea41a2645882d8d49d9cf417ffd38af6a784789e40613e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emails")
    def emails(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "emails"))

    @emails.setter
    def emails(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__114b7b25b91cb7288bf6f722c032095431d2aed74f4b81806be1717aa113e6ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emails", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="upns")
    def upns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "upns"))

    @upns.setter
    def upns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3005670821340ed4cce5690d8b314380a30f0ff4016adb7cb909395066471320)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "upns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KeyVaultCertificateCertificatePolicyX509CertificatePropertiesSubjectAlternativeNames]:
        return typing.cast(typing.Optional[KeyVaultCertificateCertificatePolicyX509CertificatePropertiesSubjectAlternativeNames], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KeyVaultCertificateCertificatePolicyX509CertificatePropertiesSubjectAlternativeNames],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0d867581ed22ceda216185aa51befc0b9e1874ffa454cc216fe3af7df5ad073)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "key_vault_id": "keyVaultId",
        "name": "name",
        "certificate": "certificate",
        "certificate_policy": "certificatePolicy",
        "id": "id",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class KeyVaultCertificateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        key_vault_id: builtins.str,
        name: builtins.str,
        certificate: typing.Optional[typing.Union[KeyVaultCertificateCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
        certificate_policy: typing.Optional[typing.Union[KeyVaultCertificateCertificatePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["KeyVaultCertificateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param key_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#key_vault_id KeyVaultCertificate#key_vault_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#name KeyVaultCertificate#name}.
        :param certificate: certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#certificate KeyVaultCertificate#certificate}
        :param certificate_policy: certificate_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#certificate_policy KeyVaultCertificate#certificate_policy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#id KeyVaultCertificate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#tags KeyVaultCertificate#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#timeouts KeyVaultCertificate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(certificate, dict):
            certificate = KeyVaultCertificateCertificate(**certificate)
        if isinstance(certificate_policy, dict):
            certificate_policy = KeyVaultCertificateCertificatePolicy(**certificate_policy)
        if isinstance(timeouts, dict):
            timeouts = KeyVaultCertificateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5def7834cec9c2bea78b8d678750a1da68a928c14b039ce41ef8862a7bf030a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument key_vault_id", value=key_vault_id, expected_type=type_hints["key_vault_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument certificate_policy", value=certificate_policy, expected_type=type_hints["certificate_policy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_vault_id": key_vault_id,
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
        if certificate is not None:
            self._values["certificate"] = certificate
        if certificate_policy is not None:
            self._values["certificate_policy"] = certificate_policy
        if id is not None:
            self._values["id"] = id
        if tags is not None:
            self._values["tags"] = tags
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
    def key_vault_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#key_vault_id KeyVaultCertificate#key_vault_id}.'''
        result = self._values.get("key_vault_id")
        assert result is not None, "Required property 'key_vault_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#name KeyVaultCertificate#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate(self) -> typing.Optional[KeyVaultCertificateCertificate]:
        '''certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#certificate KeyVaultCertificate#certificate}
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[KeyVaultCertificateCertificate], result)

    @builtins.property
    def certificate_policy(
        self,
    ) -> typing.Optional[KeyVaultCertificateCertificatePolicy]:
        '''certificate_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#certificate_policy KeyVaultCertificate#certificate_policy}
        '''
        result = self._values.get("certificate_policy")
        return typing.cast(typing.Optional[KeyVaultCertificateCertificatePolicy], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#id KeyVaultCertificate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#tags KeyVaultCertificate#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["KeyVaultCertificateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#timeouts KeyVaultCertificate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["KeyVaultCertificateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyVaultCertificateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class KeyVaultCertificateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#create KeyVaultCertificate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#delete KeyVaultCertificate#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#read KeyVaultCertificate#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#update KeyVaultCertificate#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8daebd797f017a4f935925171d791789f2915ee5e6cf24c56eb26a4b2ab3fa7c)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#create KeyVaultCertificate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#delete KeyVaultCertificate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#read KeyVaultCertificate#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_certificate#update KeyVaultCertificate#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyVaultCertificateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyVaultCertificateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.keyVaultCertificate.KeyVaultCertificateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f581d20d23e0221f1af33d99703ed513771642a5e593ae032aaa1b878b89dbe1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__58d5f586beb531d79066f08f51607987edfd02ea77a6e29cba5509f632272670)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__259a5ff621833bfa8b9801465b7294ba7383e462d30c9682f9fd28171b3ea435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa750550f448397d7277bccb0eda5c97094cbcd06a61ffa4b35759006f81309f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbaa53d1ff2cab4cdc8aa7bc46e416c7cb2540b5c80d0754d47b197279c4138a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyVaultCertificateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyVaultCertificateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyVaultCertificateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd127b909cc60f3c67b7e180087c33af0836c91c97d9945617de439e9b9cb0ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "KeyVaultCertificate",
    "KeyVaultCertificateCertificate",
    "KeyVaultCertificateCertificateAttribute",
    "KeyVaultCertificateCertificateAttributeList",
    "KeyVaultCertificateCertificateAttributeOutputReference",
    "KeyVaultCertificateCertificateOutputReference",
    "KeyVaultCertificateCertificatePolicy",
    "KeyVaultCertificateCertificatePolicyIssuerParameters",
    "KeyVaultCertificateCertificatePolicyIssuerParametersOutputReference",
    "KeyVaultCertificateCertificatePolicyKeyProperties",
    "KeyVaultCertificateCertificatePolicyKeyPropertiesOutputReference",
    "KeyVaultCertificateCertificatePolicyLifetimeAction",
    "KeyVaultCertificateCertificatePolicyLifetimeActionAction",
    "KeyVaultCertificateCertificatePolicyLifetimeActionActionOutputReference",
    "KeyVaultCertificateCertificatePolicyLifetimeActionList",
    "KeyVaultCertificateCertificatePolicyLifetimeActionOutputReference",
    "KeyVaultCertificateCertificatePolicyLifetimeActionTrigger",
    "KeyVaultCertificateCertificatePolicyLifetimeActionTriggerOutputReference",
    "KeyVaultCertificateCertificatePolicyOutputReference",
    "KeyVaultCertificateCertificatePolicySecretProperties",
    "KeyVaultCertificateCertificatePolicySecretPropertiesOutputReference",
    "KeyVaultCertificateCertificatePolicyX509CertificateProperties",
    "KeyVaultCertificateCertificatePolicyX509CertificatePropertiesOutputReference",
    "KeyVaultCertificateCertificatePolicyX509CertificatePropertiesSubjectAlternativeNames",
    "KeyVaultCertificateCertificatePolicyX509CertificatePropertiesSubjectAlternativeNamesOutputReference",
    "KeyVaultCertificateConfig",
    "KeyVaultCertificateTimeouts",
    "KeyVaultCertificateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7a99b35a74b7748ca24f041d124860840389f3ba1eb85546f6b3f03b9f654429(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    key_vault_id: builtins.str,
    name: builtins.str,
    certificate: typing.Optional[typing.Union[KeyVaultCertificateCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate_policy: typing.Optional[typing.Union[KeyVaultCertificateCertificatePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[KeyVaultCertificateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9e9f52db486f8f06bb8c0dc137b8234c8e17560df88723c5f10ddab52443322a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13675c1696965bf0a15af2ff6abf4fa158d4a3255f7b7823b31f0e3623012dae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d39b76e6c90db9d5ec589d41857842f38d0e0c6cb32f1b98b049dd71a2b0f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3355ef225c585621a66517728193c7d2049b22a186b4abc8d0f73b723a12b80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb5a87159112dadf3ee8d69615b533eae7987867b6f6766dd8770e3147083c8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__940a3afc372bd2322286e6a26cb0dc1d6fbc41852b42b4c46a4099a4a26ee1f6(
    *,
    contents: builtins.str,
    password: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d64e3771086ce2ee3d722567092720dc7132a8506a7752fa07db4f33cf07489(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c907dba08fdef672c82b6175963b316504b1ec4183a138f3e6ee9d7997e1420(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd4ad1ec38b48e3b4b92f1f62eea732db69b663ecbe2fd110623e363181a5ab5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d63d3f28a37363a0f83fb14a3275b3330a99309887e9732c8800ca46db840e7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c5b33ebed202811929a2bfa0fd560c6e4857c5bdf9ee74ce8b83efcb40285f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__437ca10e2cc4f0e273b662d0ca4356fd0db3085493f6c7710282e6675a2281e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__042f645a7ff2d4e9d07a66543fd08df2b06d9a71de4a0d8143c994e816c7bc20(
    value: typing.Optional[KeyVaultCertificateCertificateAttribute],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec2781319ea06ae6870031b39aef3ac4b6646898a0db2ba83f9f7ea166b099cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ffc11d929d90b2762ef993b11b0960a25fff69dfcca19fa879217097526f88d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7445f4c017d5036817f53cabc930e4f31734255ed42d05fbc9313ae9c357421(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed0846d5050580b6f1d0a37d3922efe4aba44d97582efe4513c471e608289438(
    value: typing.Optional[KeyVaultCertificateCertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c6b8e99bd9df35e7967f22c5232a33c87408d2882a0554e1e8087134a27c7ee(
    *,
    issuer_parameters: typing.Union[KeyVaultCertificateCertificatePolicyIssuerParameters, typing.Dict[builtins.str, typing.Any]],
    key_properties: typing.Union[KeyVaultCertificateCertificatePolicyKeyProperties, typing.Dict[builtins.str, typing.Any]],
    secret_properties: typing.Union[KeyVaultCertificateCertificatePolicySecretProperties, typing.Dict[builtins.str, typing.Any]],
    lifetime_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KeyVaultCertificateCertificatePolicyLifetimeAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    x509_certificate_properties: typing.Optional[typing.Union[KeyVaultCertificateCertificatePolicyX509CertificateProperties, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82052023ed8eb058979d9fcc627c15d1293a0d3dd299b45f4daced0690bde02f(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f51679d1b890b4ce326e37a852dfeb837f8f83dcfb3820f46261e8371a4d206a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a9b7090f4c00b79da8acaa15d32c19c72f5da3517fb5cfd12eaf532624fd43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f4886381d6b24bf9e327534eb7b526d7ebf931caf04bda14c53cf4467f94101(
    value: typing.Optional[KeyVaultCertificateCertificatePolicyIssuerParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da4349c081fa313fc0ece1c36ead219b608a661a3e00ca955137e38b55e31013(
    *,
    exportable: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    key_type: builtins.str,
    reuse_key: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    curve: typing.Optional[builtins.str] = None,
    key_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4de8d09212b8199802e502d19699c2c894bd0acdd93e73ff3b573ebe2c6e3973(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea1563618c251c67528970004ff8e4d18eeb00b6e8014173857ed5f0ae1820d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1873d4961c3a2afcd002e74fd893b0e5b63b054e50a1e9e8bf327574f11396ba(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd58f07e41a37d0e15e8ecbceb1f9de0c4205165a5855757a7a6eee3e1aa5a6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e0e27250f74e56734040dd178c6ef418b91d42db7b6bb546dc024a230957185(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0776d65e06d9eb05fb1ab7e510b07dadb0914d9dfc68969d1f4ecf7ed7b43c78(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21142730244cc7b01771057c622373da8d807a02c4bcd7c91ae9d82fbd1ad6db(
    value: typing.Optional[KeyVaultCertificateCertificatePolicyKeyProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a09bf2d92761c2e9b9741533f6544fd9278acf8d40679e954ddeae4460f0853(
    *,
    action: typing.Union[KeyVaultCertificateCertificatePolicyLifetimeActionAction, typing.Dict[builtins.str, typing.Any]],
    trigger: typing.Union[KeyVaultCertificateCertificatePolicyLifetimeActionTrigger, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8531a4571088787c741f9025d90a3835c202dbc737370af74cda43ffd8c29d58(
    *,
    action_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2494433790c650a6099926a24a57497c69050c3903ffdffbc3a61a6e9536dbdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55d36e24081f6c75f647022bd879476576239567871fbb8a1584fe7f5d36ca0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f58295c97de192cb069ae0078420c96138a21124152cdde2c3edae5caaa09a5c(
    value: typing.Optional[KeyVaultCertificateCertificatePolicyLifetimeActionAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a0b774f474fa2ca7490dec39d95d5241b2648d61b75489adb1b4f2ede52fdc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b0427775b3120e4178d14cd4e70f618b1904e70ca654671a3afda7c6ca834bc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7cf89724e1a97f89fd01e52bcf752c2bd83e530ece5e882241f30d415dce19a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e16e9fcba70b5a97f5dbf8d33dff45e949c2f0dd71d530618d034758f9c1b006(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b1b3823e846333072798400f17471ab7663843d5f8c31ed2ed92dc16facca8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__763d00855fa1ada02df35dc58def825174373d6f55f7a2cd17a5c0b541cbaa53(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyVaultCertificateCertificatePolicyLifetimeAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7fb17fffafc750e39aefa4254c9beba49c9bd2b55765c474fd4abe3735f0334(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3c01858a60a8c297c51a80e53953e912d64c3a974c1fc8e36d716476c35690f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyVaultCertificateCertificatePolicyLifetimeAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4cedbc6bb18f045cd403c454f9dd556406c56b67e5d3f548d43a5eea4792fd6(
    *,
    days_before_expiry: typing.Optional[jsii.Number] = None,
    lifetime_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f864975626c57754174b7ed15ebac52f8079a93dd2449b4be9577a0c0d6c9e80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177c399eedc840d7ac68a5a5b146d6d9de94f3c2dc7bc92472d0b8b9cf0063ee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__282d5eefde5ec496485f74404ce3ac14cf9e8aa48a49c30b13aa5d088072befa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac38411eaae1cebc27a95b3a0448e815d0cbdc5ed3ec6aa445fae77e2388aa6(
    value: typing.Optional[KeyVaultCertificateCertificatePolicyLifetimeActionTrigger],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a78f5035fa1f966bf1bd98a4a01867d5e970c56423fa7bded51ad4eb5454b21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff00e4477a10a04d3a79082354aaf0b549795f0f73675274ad554aeeb538f46(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KeyVaultCertificateCertificatePolicyLifetimeAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c99adfead2cf84815320e8a04cc74112bcf67ab2ae3718044197a7349d348fb1(
    value: typing.Optional[KeyVaultCertificateCertificatePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa965482a24fceaf73094cc633020ecfe9d225c7c833f1e03d1d62ddd3ef3d2c(
    *,
    content_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c150ffaef68ad49e9201352b2a6d08f9fda8810bfcbdf2d46ae19bcab37d8a70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc3c525bef53cee55f5e807c02bbc03291c0f019082c9837fe6a36742dc2273b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5005a9920d4c9537071ad2b39c631844e1d4c27e90c8b94f251ba7aa3c5119d2(
    value: typing.Optional[KeyVaultCertificateCertificatePolicySecretProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb9053f72d5d54a32e2aac9c6ab097747be064565bf51bac2c61b293b56c6a43(
    *,
    key_usage: typing.Sequence[builtins.str],
    subject: builtins.str,
    validity_in_months: jsii.Number,
    extended_key_usage: typing.Optional[typing.Sequence[builtins.str]] = None,
    subject_alternative_names: typing.Optional[typing.Union[KeyVaultCertificateCertificatePolicyX509CertificatePropertiesSubjectAlternativeNames, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dbe3bc97652df2c45c0b6a2c892291b8ba49523997ca4778a0561f4f5d7fa1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95cf7dce7901e171093871b46362b3adc97e14363ce1ef727daf8b18a81ded6c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34f78baf743766000114383bb12887e69d7f1f6a6cc19598ff7752dac538a4ce(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2803acbd51a30448fd6c8846c8a25476fe33c85dcd0ad24d94b0791674198a1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be320243aa2da495f7bb7ff3febda452d184fbed07eba9f720e111682a92fbdb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb61ec5b92cec2b5f6a3fe71e6ab6b38f712074f0074dd0c492cb577c879aa0e(
    value: typing.Optional[KeyVaultCertificateCertificatePolicyX509CertificateProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92cd8f5c9e83de5c1e47b50724d9767473baa7bb6de2494b9ade6b68182709a4(
    *,
    dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    emails: typing.Optional[typing.Sequence[builtins.str]] = None,
    upns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa5b5dc72c9626bb61af0f99c5bea582845e57123f833e32f6739c85713406fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6816722e4ddd996fdea41a2645882d8d49d9cf417ffd38af6a784789e40613e6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__114b7b25b91cb7288bf6f722c032095431d2aed74f4b81806be1717aa113e6ed(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3005670821340ed4cce5690d8b314380a30f0ff4016adb7cb909395066471320(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d867581ed22ceda216185aa51befc0b9e1874ffa454cc216fe3af7df5ad073(
    value: typing.Optional[KeyVaultCertificateCertificatePolicyX509CertificatePropertiesSubjectAlternativeNames],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5def7834cec9c2bea78b8d678750a1da68a928c14b039ce41ef8862a7bf030a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    key_vault_id: builtins.str,
    name: builtins.str,
    certificate: typing.Optional[typing.Union[KeyVaultCertificateCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate_policy: typing.Optional[typing.Union[KeyVaultCertificateCertificatePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[KeyVaultCertificateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8daebd797f017a4f935925171d791789f2915ee5e6cf24c56eb26a4b2ab3fa7c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f581d20d23e0221f1af33d99703ed513771642a5e593ae032aaa1b878b89dbe1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58d5f586beb531d79066f08f51607987edfd02ea77a6e29cba5509f632272670(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__259a5ff621833bfa8b9801465b7294ba7383e462d30c9682f9fd28171b3ea435(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa750550f448397d7277bccb0eda5c97094cbcd06a61ffa4b35759006f81309f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbaa53d1ff2cab4cdc8aa7bc46e416c7cb2540b5c80d0754d47b197279c4138a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd127b909cc60f3c67b7e180087c33af0836c91c97d9945617de439e9b9cb0ee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyVaultCertificateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
