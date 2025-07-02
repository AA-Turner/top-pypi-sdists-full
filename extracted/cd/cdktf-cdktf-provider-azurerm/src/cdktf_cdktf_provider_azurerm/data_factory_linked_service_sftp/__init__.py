r'''
# `azurerm_data_factory_linked_service_sftp`

Refer to the Terraform Registry for docs: [`azurerm_data_factory_linked_service_sftp`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp).
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


class DataFactoryLinkedServiceSftp(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceSftp.DataFactoryLinkedServiceSftp",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp azurerm_data_factory_linked_service_sftp}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        authentication_type: builtins.str,
        data_factory_id: builtins.str,
        host: builtins.str,
        name: builtins.str,
        port: jsii.Number,
        username: builtins.str,
        additional_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        annotations: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        host_key_fingerprint: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        integration_runtime_name: typing.Optional[builtins.str] = None,
        key_vault_password: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataFactoryLinkedServiceSftpKeyVaultPassword", typing.Dict[builtins.str, typing.Any]]]]] = None,
        key_vault_private_key_content_base64: typing.Optional[typing.Union["DataFactoryLinkedServiceSftpKeyVaultPrivateKeyContentBase64", typing.Dict[builtins.str, typing.Any]]] = None,
        key_vault_private_key_passphrase: typing.Optional[typing.Union["DataFactoryLinkedServiceSftpKeyVaultPrivateKeyPassphrase", typing.Dict[builtins.str, typing.Any]]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        password: typing.Optional[builtins.str] = None,
        private_key_content_base64: typing.Optional[builtins.str] = None,
        private_key_passphrase: typing.Optional[builtins.str] = None,
        private_key_path: typing.Optional[builtins.str] = None,
        skip_host_key_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["DataFactoryLinkedServiceSftpTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp azurerm_data_factory_linked_service_sftp} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param authentication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#authentication_type DataFactoryLinkedServiceSftp#authentication_type}.
        :param data_factory_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#data_factory_id DataFactoryLinkedServiceSftp#data_factory_id}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#host DataFactoryLinkedServiceSftp#host}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#name DataFactoryLinkedServiceSftp#name}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#port DataFactoryLinkedServiceSftp#port}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#username DataFactoryLinkedServiceSftp#username}.
        :param additional_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#additional_properties DataFactoryLinkedServiceSftp#additional_properties}.
        :param annotations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#annotations DataFactoryLinkedServiceSftp#annotations}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#description DataFactoryLinkedServiceSftp#description}.
        :param host_key_fingerprint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#host_key_fingerprint DataFactoryLinkedServiceSftp#host_key_fingerprint}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#id DataFactoryLinkedServiceSftp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param integration_runtime_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#integration_runtime_name DataFactoryLinkedServiceSftp#integration_runtime_name}.
        :param key_vault_password: key_vault_password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#key_vault_password DataFactoryLinkedServiceSftp#key_vault_password}
        :param key_vault_private_key_content_base64: key_vault_private_key_content_base64 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#key_vault_private_key_content_base64 DataFactoryLinkedServiceSftp#key_vault_private_key_content_base64}
        :param key_vault_private_key_passphrase: key_vault_private_key_passphrase block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#key_vault_private_key_passphrase DataFactoryLinkedServiceSftp#key_vault_private_key_passphrase}
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#parameters DataFactoryLinkedServiceSftp#parameters}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#password DataFactoryLinkedServiceSftp#password}.
        :param private_key_content_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#private_key_content_base64 DataFactoryLinkedServiceSftp#private_key_content_base64}.
        :param private_key_passphrase: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#private_key_passphrase DataFactoryLinkedServiceSftp#private_key_passphrase}.
        :param private_key_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#private_key_path DataFactoryLinkedServiceSftp#private_key_path}.
        :param skip_host_key_validation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#skip_host_key_validation DataFactoryLinkedServiceSftp#skip_host_key_validation}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#timeouts DataFactoryLinkedServiceSftp#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ff937372663ca2b07e58e9e11d371570db88330a2f6ae131684d8caddfe1c42)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataFactoryLinkedServiceSftpConfig(
            authentication_type=authentication_type,
            data_factory_id=data_factory_id,
            host=host,
            name=name,
            port=port,
            username=username,
            additional_properties=additional_properties,
            annotations=annotations,
            description=description,
            host_key_fingerprint=host_key_fingerprint,
            id=id,
            integration_runtime_name=integration_runtime_name,
            key_vault_password=key_vault_password,
            key_vault_private_key_content_base64=key_vault_private_key_content_base64,
            key_vault_private_key_passphrase=key_vault_private_key_passphrase,
            parameters=parameters,
            password=password,
            private_key_content_base64=private_key_content_base64,
            private_key_passphrase=private_key_passphrase,
            private_key_path=private_key_path,
            skip_host_key_validation=skip_host_key_validation,
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
        '''Generates CDKTF code for importing a DataFactoryLinkedServiceSftp resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataFactoryLinkedServiceSftp to import.
        :param import_from_id: The id of the existing DataFactoryLinkedServiceSftp that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataFactoryLinkedServiceSftp to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05a63bef93c6dae594710d81157ec6cbef183d3b26c54d90d1b1306ff96ed20e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putKeyVaultPassword")
    def put_key_vault_password(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataFactoryLinkedServiceSftpKeyVaultPassword", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb27f35c1e71c30d3e11188afd15734ae5b7c60b59bce49b558a35f61eee3d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putKeyVaultPassword", [value]))

    @jsii.member(jsii_name="putKeyVaultPrivateKeyContentBase64")
    def put_key_vault_private_key_content_base64(
        self,
        *,
        linked_service_name: builtins.str,
        secret_name: builtins.str,
    ) -> None:
        '''
        :param linked_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#linked_service_name DataFactoryLinkedServiceSftp#linked_service_name}.
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#secret_name DataFactoryLinkedServiceSftp#secret_name}.
        '''
        value = DataFactoryLinkedServiceSftpKeyVaultPrivateKeyContentBase64(
            linked_service_name=linked_service_name, secret_name=secret_name
        )

        return typing.cast(None, jsii.invoke(self, "putKeyVaultPrivateKeyContentBase64", [value]))

    @jsii.member(jsii_name="putKeyVaultPrivateKeyPassphrase")
    def put_key_vault_private_key_passphrase(
        self,
        *,
        linked_service_name: builtins.str,
        secret_name: builtins.str,
    ) -> None:
        '''
        :param linked_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#linked_service_name DataFactoryLinkedServiceSftp#linked_service_name}.
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#secret_name DataFactoryLinkedServiceSftp#secret_name}.
        '''
        value = DataFactoryLinkedServiceSftpKeyVaultPrivateKeyPassphrase(
            linked_service_name=linked_service_name, secret_name=secret_name
        )

        return typing.cast(None, jsii.invoke(self, "putKeyVaultPrivateKeyPassphrase", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#create DataFactoryLinkedServiceSftp#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#delete DataFactoryLinkedServiceSftp#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#read DataFactoryLinkedServiceSftp#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#update DataFactoryLinkedServiceSftp#update}.
        '''
        value = DataFactoryLinkedServiceSftpTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdditionalProperties")
    def reset_additional_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalProperties", []))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetHostKeyFingerprint")
    def reset_host_key_fingerprint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostKeyFingerprint", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIntegrationRuntimeName")
    def reset_integration_runtime_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegrationRuntimeName", []))

    @jsii.member(jsii_name="resetKeyVaultPassword")
    def reset_key_vault_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultPassword", []))

    @jsii.member(jsii_name="resetKeyVaultPrivateKeyContentBase64")
    def reset_key_vault_private_key_content_base64(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultPrivateKeyContentBase64", []))

    @jsii.member(jsii_name="resetKeyVaultPrivateKeyPassphrase")
    def reset_key_vault_private_key_passphrase(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultPrivateKeyPassphrase", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPrivateKeyContentBase64")
    def reset_private_key_content_base64(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateKeyContentBase64", []))

    @jsii.member(jsii_name="resetPrivateKeyPassphrase")
    def reset_private_key_passphrase(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateKeyPassphrase", []))

    @jsii.member(jsii_name="resetPrivateKeyPath")
    def reset_private_key_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateKeyPath", []))

    @jsii.member(jsii_name="resetSkipHostKeyValidation")
    def reset_skip_host_key_validation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipHostKeyValidation", []))

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
    @jsii.member(jsii_name="keyVaultPassword")
    def key_vault_password(self) -> "DataFactoryLinkedServiceSftpKeyVaultPasswordList":
        return typing.cast("DataFactoryLinkedServiceSftpKeyVaultPasswordList", jsii.get(self, "keyVaultPassword"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultPrivateKeyContentBase64")
    def key_vault_private_key_content_base64(
        self,
    ) -> "DataFactoryLinkedServiceSftpKeyVaultPrivateKeyContentBase64OutputReference":
        return typing.cast("DataFactoryLinkedServiceSftpKeyVaultPrivateKeyContentBase64OutputReference", jsii.get(self, "keyVaultPrivateKeyContentBase64"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultPrivateKeyPassphrase")
    def key_vault_private_key_passphrase(
        self,
    ) -> "DataFactoryLinkedServiceSftpKeyVaultPrivateKeyPassphraseOutputReference":
        return typing.cast("DataFactoryLinkedServiceSftpKeyVaultPrivateKeyPassphraseOutputReference", jsii.get(self, "keyVaultPrivateKeyPassphrase"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataFactoryLinkedServiceSftpTimeoutsOutputReference":
        return typing.cast("DataFactoryLinkedServiceSftpTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="additionalPropertiesInput")
    def additional_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "additionalPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationTypeInput")
    def authentication_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="dataFactoryIdInput")
    def data_factory_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataFactoryIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="hostKeyFingerprintInput")
    def host_key_fingerprint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostKeyFingerprintInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="integrationRuntimeNameInput")
    def integration_runtime_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integrationRuntimeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultPasswordInput")
    def key_vault_password_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryLinkedServiceSftpKeyVaultPassword"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryLinkedServiceSftpKeyVaultPassword"]]], jsii.get(self, "keyVaultPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultPrivateKeyContentBase64Input")
    def key_vault_private_key_content_base64_input(
        self,
    ) -> typing.Optional["DataFactoryLinkedServiceSftpKeyVaultPrivateKeyContentBase64"]:
        return typing.cast(typing.Optional["DataFactoryLinkedServiceSftpKeyVaultPrivateKeyContentBase64"], jsii.get(self, "keyVaultPrivateKeyContentBase64Input"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultPrivateKeyPassphraseInput")
    def key_vault_private_key_passphrase_input(
        self,
    ) -> typing.Optional["DataFactoryLinkedServiceSftpKeyVaultPrivateKeyPassphrase"]:
        return typing.cast(typing.Optional["DataFactoryLinkedServiceSftpKeyVaultPrivateKeyPassphrase"], jsii.get(self, "keyVaultPrivateKeyPassphraseInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyContentBase64Input")
    def private_key_content_base64_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyContentBase64Input"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyPassphraseInput")
    def private_key_passphrase_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyPassphraseInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyPathInput")
    def private_key_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyPathInput"))

    @builtins.property
    @jsii.member(jsii_name="skipHostKeyValidationInput")
    def skip_host_key_validation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipHostKeyValidationInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataFactoryLinkedServiceSftpTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataFactoryLinkedServiceSftpTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalProperties")
    def additional_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "additionalProperties"))

    @additional_properties.setter
    def additional_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e88e4feed128874872dd1951e04306ea80f4f606deebb42820643569ad87b95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c882571b2498a7bb4dca3ac986568d42543b37234eb05596e9ef258ec486847e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authenticationType")
    def authentication_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationType"))

    @authentication_type.setter
    def authentication_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32ad8561050c670116fe430eca7fdcd2a764f07fb336162231782d4a616864ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataFactoryId")
    def data_factory_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataFactoryId"))

    @data_factory_id.setter
    def data_factory_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdc24fdd4591b34b7679a890fdf246a63edc0d1f47727943a0bbed55d748b809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataFactoryId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc71585af2ba22f4eab502618b346415ab9ead61f207414332a5e3820258221)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e3533816b657303b0cad3e1c5f43519e0a990a25fe12d73da4fb87ca02ab054)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostKeyFingerprint")
    def host_key_fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostKeyFingerprint"))

    @host_key_fingerprint.setter
    def host_key_fingerprint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d70b124c6c2953a0f824945ec4ede64290ae331dec1ff07e46ecf558ea1cf091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostKeyFingerprint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c503e44915b656055dc0a8173cb921f4a2c5769342b6e0e825ccce52d00e20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integrationRuntimeName")
    def integration_runtime_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "integrationRuntimeName"))

    @integration_runtime_name.setter
    def integration_runtime_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e65c1e92c009b90163486727faacd22950da44781e2654c261b3e1ec09bf0be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationRuntimeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__445c351a1cb5455e9284bd2e6a1ef0f1f6770514ffca4f816237da9b87ab794e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db8c7fee2dbba14c501d09538ddc6676e41c333d704314f29eac6bde757836e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ee504b8de0d846409358fcb2e1000dbb377030985dad04d9df36666329cf0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e545b7059a2b19cea56a3e8afced56370a389187625e4ebd289cc4949df269dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKeyContentBase64")
    def private_key_content_base64(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKeyContentBase64"))

    @private_key_content_base64.setter
    def private_key_content_base64(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbb55cdee5dce5b32e166a0bc2dcc8c1bfdcf96bed53af006ec967460674d565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKeyContentBase64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKeyPassphrase")
    def private_key_passphrase(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKeyPassphrase"))

    @private_key_passphrase.setter
    def private_key_passphrase(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e04c209efa2fa2e53de0f6d8420fab34f6581dd3e46648135f5b0afbddb1cb55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKeyPassphrase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKeyPath")
    def private_key_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKeyPath"))

    @private_key_path.setter
    def private_key_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c612a476917c5da24388c0ccc51f8f6db235feeb58f48415d5e4f342062c002)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKeyPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipHostKeyValidation")
    def skip_host_key_validation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipHostKeyValidation"))

    @skip_host_key_validation.setter
    def skip_host_key_validation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__889701b658dc7cad5884bebfeb1cba4417ff00ee8431e9610bd3a8718a6d5e7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipHostKeyValidation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3146256028373179bc8fde9da5ee2ab5727afcf2b38cd71ba44e0ed1f318b5a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceSftp.DataFactoryLinkedServiceSftpConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "authentication_type": "authenticationType",
        "data_factory_id": "dataFactoryId",
        "host": "host",
        "name": "name",
        "port": "port",
        "username": "username",
        "additional_properties": "additionalProperties",
        "annotations": "annotations",
        "description": "description",
        "host_key_fingerprint": "hostKeyFingerprint",
        "id": "id",
        "integration_runtime_name": "integrationRuntimeName",
        "key_vault_password": "keyVaultPassword",
        "key_vault_private_key_content_base64": "keyVaultPrivateKeyContentBase64",
        "key_vault_private_key_passphrase": "keyVaultPrivateKeyPassphrase",
        "parameters": "parameters",
        "password": "password",
        "private_key_content_base64": "privateKeyContentBase64",
        "private_key_passphrase": "privateKeyPassphrase",
        "private_key_path": "privateKeyPath",
        "skip_host_key_validation": "skipHostKeyValidation",
        "timeouts": "timeouts",
    },
)
class DataFactoryLinkedServiceSftpConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        authentication_type: builtins.str,
        data_factory_id: builtins.str,
        host: builtins.str,
        name: builtins.str,
        port: jsii.Number,
        username: builtins.str,
        additional_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        annotations: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        host_key_fingerprint: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        integration_runtime_name: typing.Optional[builtins.str] = None,
        key_vault_password: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataFactoryLinkedServiceSftpKeyVaultPassword", typing.Dict[builtins.str, typing.Any]]]]] = None,
        key_vault_private_key_content_base64: typing.Optional[typing.Union["DataFactoryLinkedServiceSftpKeyVaultPrivateKeyContentBase64", typing.Dict[builtins.str, typing.Any]]] = None,
        key_vault_private_key_passphrase: typing.Optional[typing.Union["DataFactoryLinkedServiceSftpKeyVaultPrivateKeyPassphrase", typing.Dict[builtins.str, typing.Any]]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        password: typing.Optional[builtins.str] = None,
        private_key_content_base64: typing.Optional[builtins.str] = None,
        private_key_passphrase: typing.Optional[builtins.str] = None,
        private_key_path: typing.Optional[builtins.str] = None,
        skip_host_key_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["DataFactoryLinkedServiceSftpTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param authentication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#authentication_type DataFactoryLinkedServiceSftp#authentication_type}.
        :param data_factory_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#data_factory_id DataFactoryLinkedServiceSftp#data_factory_id}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#host DataFactoryLinkedServiceSftp#host}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#name DataFactoryLinkedServiceSftp#name}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#port DataFactoryLinkedServiceSftp#port}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#username DataFactoryLinkedServiceSftp#username}.
        :param additional_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#additional_properties DataFactoryLinkedServiceSftp#additional_properties}.
        :param annotations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#annotations DataFactoryLinkedServiceSftp#annotations}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#description DataFactoryLinkedServiceSftp#description}.
        :param host_key_fingerprint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#host_key_fingerprint DataFactoryLinkedServiceSftp#host_key_fingerprint}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#id DataFactoryLinkedServiceSftp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param integration_runtime_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#integration_runtime_name DataFactoryLinkedServiceSftp#integration_runtime_name}.
        :param key_vault_password: key_vault_password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#key_vault_password DataFactoryLinkedServiceSftp#key_vault_password}
        :param key_vault_private_key_content_base64: key_vault_private_key_content_base64 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#key_vault_private_key_content_base64 DataFactoryLinkedServiceSftp#key_vault_private_key_content_base64}
        :param key_vault_private_key_passphrase: key_vault_private_key_passphrase block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#key_vault_private_key_passphrase DataFactoryLinkedServiceSftp#key_vault_private_key_passphrase}
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#parameters DataFactoryLinkedServiceSftp#parameters}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#password DataFactoryLinkedServiceSftp#password}.
        :param private_key_content_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#private_key_content_base64 DataFactoryLinkedServiceSftp#private_key_content_base64}.
        :param private_key_passphrase: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#private_key_passphrase DataFactoryLinkedServiceSftp#private_key_passphrase}.
        :param private_key_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#private_key_path DataFactoryLinkedServiceSftp#private_key_path}.
        :param skip_host_key_validation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#skip_host_key_validation DataFactoryLinkedServiceSftp#skip_host_key_validation}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#timeouts DataFactoryLinkedServiceSftp#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(key_vault_private_key_content_base64, dict):
            key_vault_private_key_content_base64 = DataFactoryLinkedServiceSftpKeyVaultPrivateKeyContentBase64(**key_vault_private_key_content_base64)
        if isinstance(key_vault_private_key_passphrase, dict):
            key_vault_private_key_passphrase = DataFactoryLinkedServiceSftpKeyVaultPrivateKeyPassphrase(**key_vault_private_key_passphrase)
        if isinstance(timeouts, dict):
            timeouts = DataFactoryLinkedServiceSftpTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42469904a8ab71d9d37aec58d076dbd7af07eeae765a1e74f997b9b2ab96c264)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
            check_type(argname="argument data_factory_id", value=data_factory_id, expected_type=type_hints["data_factory_id"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument additional_properties", value=additional_properties, expected_type=type_hints["additional_properties"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument host_key_fingerprint", value=host_key_fingerprint, expected_type=type_hints["host_key_fingerprint"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument integration_runtime_name", value=integration_runtime_name, expected_type=type_hints["integration_runtime_name"])
            check_type(argname="argument key_vault_password", value=key_vault_password, expected_type=type_hints["key_vault_password"])
            check_type(argname="argument key_vault_private_key_content_base64", value=key_vault_private_key_content_base64, expected_type=type_hints["key_vault_private_key_content_base64"])
            check_type(argname="argument key_vault_private_key_passphrase", value=key_vault_private_key_passphrase, expected_type=type_hints["key_vault_private_key_passphrase"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument private_key_content_base64", value=private_key_content_base64, expected_type=type_hints["private_key_content_base64"])
            check_type(argname="argument private_key_passphrase", value=private_key_passphrase, expected_type=type_hints["private_key_passphrase"])
            check_type(argname="argument private_key_path", value=private_key_path, expected_type=type_hints["private_key_path"])
            check_type(argname="argument skip_host_key_validation", value=skip_host_key_validation, expected_type=type_hints["skip_host_key_validation"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authentication_type": authentication_type,
            "data_factory_id": data_factory_id,
            "host": host,
            "name": name,
            "port": port,
            "username": username,
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
        if additional_properties is not None:
            self._values["additional_properties"] = additional_properties
        if annotations is not None:
            self._values["annotations"] = annotations
        if description is not None:
            self._values["description"] = description
        if host_key_fingerprint is not None:
            self._values["host_key_fingerprint"] = host_key_fingerprint
        if id is not None:
            self._values["id"] = id
        if integration_runtime_name is not None:
            self._values["integration_runtime_name"] = integration_runtime_name
        if key_vault_password is not None:
            self._values["key_vault_password"] = key_vault_password
        if key_vault_private_key_content_base64 is not None:
            self._values["key_vault_private_key_content_base64"] = key_vault_private_key_content_base64
        if key_vault_private_key_passphrase is not None:
            self._values["key_vault_private_key_passphrase"] = key_vault_private_key_passphrase
        if parameters is not None:
            self._values["parameters"] = parameters
        if password is not None:
            self._values["password"] = password
        if private_key_content_base64 is not None:
            self._values["private_key_content_base64"] = private_key_content_base64
        if private_key_passphrase is not None:
            self._values["private_key_passphrase"] = private_key_passphrase
        if private_key_path is not None:
            self._values["private_key_path"] = private_key_path
        if skip_host_key_validation is not None:
            self._values["skip_host_key_validation"] = skip_host_key_validation
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
    def authentication_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#authentication_type DataFactoryLinkedServiceSftp#authentication_type}.'''
        result = self._values.get("authentication_type")
        assert result is not None, "Required property 'authentication_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_factory_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#data_factory_id DataFactoryLinkedServiceSftp#data_factory_id}.'''
        result = self._values.get("data_factory_id")
        assert result is not None, "Required property 'data_factory_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#host DataFactoryLinkedServiceSftp#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#name DataFactoryLinkedServiceSftp#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#port DataFactoryLinkedServiceSftp#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#username DataFactoryLinkedServiceSftp#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#additional_properties DataFactoryLinkedServiceSftp#additional_properties}.'''
        result = self._values.get("additional_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def annotations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#annotations DataFactoryLinkedServiceSftp#annotations}.'''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#description DataFactoryLinkedServiceSftp#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_key_fingerprint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#host_key_fingerprint DataFactoryLinkedServiceSftp#host_key_fingerprint}.'''
        result = self._values.get("host_key_fingerprint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#id DataFactoryLinkedServiceSftp#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def integration_runtime_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#integration_runtime_name DataFactoryLinkedServiceSftp#integration_runtime_name}.'''
        result = self._values.get("integration_runtime_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_password(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryLinkedServiceSftpKeyVaultPassword"]]]:
        '''key_vault_password block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#key_vault_password DataFactoryLinkedServiceSftp#key_vault_password}
        '''
        result = self._values.get("key_vault_password")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryLinkedServiceSftpKeyVaultPassword"]]], result)

    @builtins.property
    def key_vault_private_key_content_base64(
        self,
    ) -> typing.Optional["DataFactoryLinkedServiceSftpKeyVaultPrivateKeyContentBase64"]:
        '''key_vault_private_key_content_base64 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#key_vault_private_key_content_base64 DataFactoryLinkedServiceSftp#key_vault_private_key_content_base64}
        '''
        result = self._values.get("key_vault_private_key_content_base64")
        return typing.cast(typing.Optional["DataFactoryLinkedServiceSftpKeyVaultPrivateKeyContentBase64"], result)

    @builtins.property
    def key_vault_private_key_passphrase(
        self,
    ) -> typing.Optional["DataFactoryLinkedServiceSftpKeyVaultPrivateKeyPassphrase"]:
        '''key_vault_private_key_passphrase block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#key_vault_private_key_passphrase DataFactoryLinkedServiceSftp#key_vault_private_key_passphrase}
        '''
        result = self._values.get("key_vault_private_key_passphrase")
        return typing.cast(typing.Optional["DataFactoryLinkedServiceSftpKeyVaultPrivateKeyPassphrase"], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#parameters DataFactoryLinkedServiceSftp#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#password DataFactoryLinkedServiceSftp#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key_content_base64(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#private_key_content_base64 DataFactoryLinkedServiceSftp#private_key_content_base64}.'''
        result = self._values.get("private_key_content_base64")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key_passphrase(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#private_key_passphrase DataFactoryLinkedServiceSftp#private_key_passphrase}.'''
        result = self._values.get("private_key_passphrase")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#private_key_path DataFactoryLinkedServiceSftp#private_key_path}.'''
        result = self._values.get("private_key_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_host_key_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#skip_host_key_validation DataFactoryLinkedServiceSftp#skip_host_key_validation}.'''
        result = self._values.get("skip_host_key_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataFactoryLinkedServiceSftpTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#timeouts DataFactoryLinkedServiceSftp#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataFactoryLinkedServiceSftpTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryLinkedServiceSftpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceSftp.DataFactoryLinkedServiceSftpKeyVaultPassword",
    jsii_struct_bases=[],
    name_mapping={
        "linked_service_name": "linkedServiceName",
        "secret_name": "secretName",
    },
)
class DataFactoryLinkedServiceSftpKeyVaultPassword:
    def __init__(
        self,
        *,
        linked_service_name: builtins.str,
        secret_name: builtins.str,
    ) -> None:
        '''
        :param linked_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#linked_service_name DataFactoryLinkedServiceSftp#linked_service_name}.
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#secret_name DataFactoryLinkedServiceSftp#secret_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa6e19574f529f5eb20dc2030e2ff298c9ae1c0f103a027d4296f0b7a5a21b14)
            check_type(argname="argument linked_service_name", value=linked_service_name, expected_type=type_hints["linked_service_name"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "linked_service_name": linked_service_name,
            "secret_name": secret_name,
        }

    @builtins.property
    def linked_service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#linked_service_name DataFactoryLinkedServiceSftp#linked_service_name}.'''
        result = self._values.get("linked_service_name")
        assert result is not None, "Required property 'linked_service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#secret_name DataFactoryLinkedServiceSftp#secret_name}.'''
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryLinkedServiceSftpKeyVaultPassword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryLinkedServiceSftpKeyVaultPasswordList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceSftp.DataFactoryLinkedServiceSftpKeyVaultPasswordList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92de6688856da263a55dfd4467c3429dfac64bb05a27e676ae131e23ac7048e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataFactoryLinkedServiceSftpKeyVaultPasswordOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5343c6283f703ac0b29f4d26fc5fc1ea1b219f33966e336ac8a4eb9e3a51dff5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataFactoryLinkedServiceSftpKeyVaultPasswordOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee6d488f27bb99289153ddd8046da15a2f261ba4e7a15f0ea12fecae95839b31)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22775667f6d072d092f576465d0e8fea5ffb29ba71f7e9c026d5fb6d57f48140)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26d6152e15fc8a55acd4135f30ad48ef4c72dad119982a947b757120f9973fc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryLinkedServiceSftpKeyVaultPassword]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryLinkedServiceSftpKeyVaultPassword]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryLinkedServiceSftpKeyVaultPassword]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f30842d5d828da4bdb48cf0b0badb867f256c39e9d969ac2e3ad15c3fafb3d77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataFactoryLinkedServiceSftpKeyVaultPasswordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceSftp.DataFactoryLinkedServiceSftpKeyVaultPasswordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5ac88653549d6b3b9b42965edd7d3fecc7a4e1ea938831650e538a68c72cc7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="linkedServiceNameInput")
    def linked_service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "linkedServiceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedServiceName")
    def linked_service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "linkedServiceName"))

    @linked_service_name.setter
    def linked_service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d750359019fb9b97b49f37467daa070fa94dab2b2cfc12f5238910250c7b56f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkedServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13a4f43fb008ed2139844b3fb0bf90a826542a24098f0dd597ea27f45c0450bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryLinkedServiceSftpKeyVaultPassword]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryLinkedServiceSftpKeyVaultPassword]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryLinkedServiceSftpKeyVaultPassword]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a32757d2572d16c7d7ac108d80c0fb7549c66723cd330b059b31f0e6ad0fbcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceSftp.DataFactoryLinkedServiceSftpKeyVaultPrivateKeyContentBase64",
    jsii_struct_bases=[],
    name_mapping={
        "linked_service_name": "linkedServiceName",
        "secret_name": "secretName",
    },
)
class DataFactoryLinkedServiceSftpKeyVaultPrivateKeyContentBase64:
    def __init__(
        self,
        *,
        linked_service_name: builtins.str,
        secret_name: builtins.str,
    ) -> None:
        '''
        :param linked_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#linked_service_name DataFactoryLinkedServiceSftp#linked_service_name}.
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#secret_name DataFactoryLinkedServiceSftp#secret_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35f214141af3fcb404979f3b5fee1aea448815b4fb501c503f5cc4d03b18e903)
            check_type(argname="argument linked_service_name", value=linked_service_name, expected_type=type_hints["linked_service_name"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "linked_service_name": linked_service_name,
            "secret_name": secret_name,
        }

    @builtins.property
    def linked_service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#linked_service_name DataFactoryLinkedServiceSftp#linked_service_name}.'''
        result = self._values.get("linked_service_name")
        assert result is not None, "Required property 'linked_service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#secret_name DataFactoryLinkedServiceSftp#secret_name}.'''
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryLinkedServiceSftpKeyVaultPrivateKeyContentBase64(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryLinkedServiceSftpKeyVaultPrivateKeyContentBase64OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceSftp.DataFactoryLinkedServiceSftpKeyVaultPrivateKeyContentBase64OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39e41347b0bb49c687e2d34666b6f52c1b34c30681b2db2c43c23a3ed0e1791b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="linkedServiceNameInput")
    def linked_service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "linkedServiceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedServiceName")
    def linked_service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "linkedServiceName"))

    @linked_service_name.setter
    def linked_service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5273e707a65c2d01a98857b8c7df89029fbb1e92eb8479fafebf40d5d8dd1e60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkedServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa62f8ed787cb24873c09c6851d7241ca4b63e5c2b735665a8cf6885366c534d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryLinkedServiceSftpKeyVaultPrivateKeyContentBase64]:
        return typing.cast(typing.Optional[DataFactoryLinkedServiceSftpKeyVaultPrivateKeyContentBase64], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryLinkedServiceSftpKeyVaultPrivateKeyContentBase64],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0754811932eb06561fd29c736abfca5a9b0b34c9676e489c4d2db2abf184ca3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceSftp.DataFactoryLinkedServiceSftpKeyVaultPrivateKeyPassphrase",
    jsii_struct_bases=[],
    name_mapping={
        "linked_service_name": "linkedServiceName",
        "secret_name": "secretName",
    },
)
class DataFactoryLinkedServiceSftpKeyVaultPrivateKeyPassphrase:
    def __init__(
        self,
        *,
        linked_service_name: builtins.str,
        secret_name: builtins.str,
    ) -> None:
        '''
        :param linked_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#linked_service_name DataFactoryLinkedServiceSftp#linked_service_name}.
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#secret_name DataFactoryLinkedServiceSftp#secret_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3b9ba696b2255c21de148843104b41e8af05be3ebffd837060d5231f27c6087)
            check_type(argname="argument linked_service_name", value=linked_service_name, expected_type=type_hints["linked_service_name"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "linked_service_name": linked_service_name,
            "secret_name": secret_name,
        }

    @builtins.property
    def linked_service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#linked_service_name DataFactoryLinkedServiceSftp#linked_service_name}.'''
        result = self._values.get("linked_service_name")
        assert result is not None, "Required property 'linked_service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#secret_name DataFactoryLinkedServiceSftp#secret_name}.'''
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryLinkedServiceSftpKeyVaultPrivateKeyPassphrase(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryLinkedServiceSftpKeyVaultPrivateKeyPassphraseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceSftp.DataFactoryLinkedServiceSftpKeyVaultPrivateKeyPassphraseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b74f5be6a48827def1f998955c605ad4813e1f200c5ba00dd61a00eb9288d12d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="linkedServiceNameInput")
    def linked_service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "linkedServiceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedServiceName")
    def linked_service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "linkedServiceName"))

    @linked_service_name.setter
    def linked_service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__740b02aa7d44cd725c4d971655b774bfc5f0ded2a568f2e5ff4c6a0803d27410)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkedServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abf281ba5f2992191d7998ce5247687b619d67b8aed3eea2ced83618f1576f58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryLinkedServiceSftpKeyVaultPrivateKeyPassphrase]:
        return typing.cast(typing.Optional[DataFactoryLinkedServiceSftpKeyVaultPrivateKeyPassphrase], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryLinkedServiceSftpKeyVaultPrivateKeyPassphrase],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__881c3c09b5b5dfc1ee9fa8995a4ea07f46cc52cbe2e6d0be61490072f3d5a597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceSftp.DataFactoryLinkedServiceSftpTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class DataFactoryLinkedServiceSftpTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#create DataFactoryLinkedServiceSftp#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#delete DataFactoryLinkedServiceSftp#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#read DataFactoryLinkedServiceSftp#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#update DataFactoryLinkedServiceSftp#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__334ed2fb7d38acf9797cc644755c76ed603bbcae961ccc6455103adce4d32144)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#create DataFactoryLinkedServiceSftp#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#delete DataFactoryLinkedServiceSftp#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#read DataFactoryLinkedServiceSftp#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_sftp#update DataFactoryLinkedServiceSftp#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryLinkedServiceSftpTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryLinkedServiceSftpTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceSftp.DataFactoryLinkedServiceSftpTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a20fcb973551c482c3419a2c81dd8d0507f21251a112ec4a93815a394716ad16)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b57511fe206b12653e7d44d4b4f5fad988e30d9cc251a452921b3caad7f8f51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d0bc7b5ca1ba1572726ed980f519896b8d7cd7af7abcada6c238a024ca9245c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ad828caa58bb2b07560d85b82af0f2179fc1bc43dcd5adb130caca9cdad4cba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__148e186359a77def962a64393c1cabc69d8277e133c205571f87d3ef3ddbd0ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryLinkedServiceSftpTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryLinkedServiceSftpTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryLinkedServiceSftpTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__056e35433b349ea1170061cf0f27199c334ac5f13da02ed959bbdbd24bb48c58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataFactoryLinkedServiceSftp",
    "DataFactoryLinkedServiceSftpConfig",
    "DataFactoryLinkedServiceSftpKeyVaultPassword",
    "DataFactoryLinkedServiceSftpKeyVaultPasswordList",
    "DataFactoryLinkedServiceSftpKeyVaultPasswordOutputReference",
    "DataFactoryLinkedServiceSftpKeyVaultPrivateKeyContentBase64",
    "DataFactoryLinkedServiceSftpKeyVaultPrivateKeyContentBase64OutputReference",
    "DataFactoryLinkedServiceSftpKeyVaultPrivateKeyPassphrase",
    "DataFactoryLinkedServiceSftpKeyVaultPrivateKeyPassphraseOutputReference",
    "DataFactoryLinkedServiceSftpTimeouts",
    "DataFactoryLinkedServiceSftpTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7ff937372663ca2b07e58e9e11d371570db88330a2f6ae131684d8caddfe1c42(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    authentication_type: builtins.str,
    data_factory_id: builtins.str,
    host: builtins.str,
    name: builtins.str,
    port: jsii.Number,
    username: builtins.str,
    additional_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    annotations: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    host_key_fingerprint: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    integration_runtime_name: typing.Optional[builtins.str] = None,
    key_vault_password: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryLinkedServiceSftpKeyVaultPassword, typing.Dict[builtins.str, typing.Any]]]]] = None,
    key_vault_private_key_content_base64: typing.Optional[typing.Union[DataFactoryLinkedServiceSftpKeyVaultPrivateKeyContentBase64, typing.Dict[builtins.str, typing.Any]]] = None,
    key_vault_private_key_passphrase: typing.Optional[typing.Union[DataFactoryLinkedServiceSftpKeyVaultPrivateKeyPassphrase, typing.Dict[builtins.str, typing.Any]]] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    password: typing.Optional[builtins.str] = None,
    private_key_content_base64: typing.Optional[builtins.str] = None,
    private_key_passphrase: typing.Optional[builtins.str] = None,
    private_key_path: typing.Optional[builtins.str] = None,
    skip_host_key_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[DataFactoryLinkedServiceSftpTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__05a63bef93c6dae594710d81157ec6cbef183d3b26c54d90d1b1306ff96ed20e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb27f35c1e71c30d3e11188afd15734ae5b7c60b59bce49b558a35f61eee3d9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryLinkedServiceSftpKeyVaultPassword, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e88e4feed128874872dd1951e04306ea80f4f606deebb42820643569ad87b95(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c882571b2498a7bb4dca3ac986568d42543b37234eb05596e9ef258ec486847e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32ad8561050c670116fe430eca7fdcd2a764f07fb336162231782d4a616864ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc24fdd4591b34b7679a890fdf246a63edc0d1f47727943a0bbed55d748b809(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc71585af2ba22f4eab502618b346415ab9ead61f207414332a5e3820258221(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e3533816b657303b0cad3e1c5f43519e0a990a25fe12d73da4fb87ca02ab054(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d70b124c6c2953a0f824945ec4ede64290ae331dec1ff07e46ecf558ea1cf091(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c503e44915b656055dc0a8173cb921f4a2c5769342b6e0e825ccce52d00e20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e65c1e92c009b90163486727faacd22950da44781e2654c261b3e1ec09bf0be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__445c351a1cb5455e9284bd2e6a1ef0f1f6770514ffca4f816237da9b87ab794e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db8c7fee2dbba14c501d09538ddc6676e41c333d704314f29eac6bde757836e4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ee504b8de0d846409358fcb2e1000dbb377030985dad04d9df36666329cf0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e545b7059a2b19cea56a3e8afced56370a389187625e4ebd289cc4949df269dd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbb55cdee5dce5b32e166a0bc2dcc8c1bfdcf96bed53af006ec967460674d565(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e04c209efa2fa2e53de0f6d8420fab34f6581dd3e46648135f5b0afbddb1cb55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c612a476917c5da24388c0ccc51f8f6db235feeb58f48415d5e4f342062c002(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__889701b658dc7cad5884bebfeb1cba4417ff00ee8431e9610bd3a8718a6d5e7b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3146256028373179bc8fde9da5ee2ab5727afcf2b38cd71ba44e0ed1f318b5a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42469904a8ab71d9d37aec58d076dbd7af07eeae765a1e74f997b9b2ab96c264(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    authentication_type: builtins.str,
    data_factory_id: builtins.str,
    host: builtins.str,
    name: builtins.str,
    port: jsii.Number,
    username: builtins.str,
    additional_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    annotations: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    host_key_fingerprint: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    integration_runtime_name: typing.Optional[builtins.str] = None,
    key_vault_password: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryLinkedServiceSftpKeyVaultPassword, typing.Dict[builtins.str, typing.Any]]]]] = None,
    key_vault_private_key_content_base64: typing.Optional[typing.Union[DataFactoryLinkedServiceSftpKeyVaultPrivateKeyContentBase64, typing.Dict[builtins.str, typing.Any]]] = None,
    key_vault_private_key_passphrase: typing.Optional[typing.Union[DataFactoryLinkedServiceSftpKeyVaultPrivateKeyPassphrase, typing.Dict[builtins.str, typing.Any]]] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    password: typing.Optional[builtins.str] = None,
    private_key_content_base64: typing.Optional[builtins.str] = None,
    private_key_passphrase: typing.Optional[builtins.str] = None,
    private_key_path: typing.Optional[builtins.str] = None,
    skip_host_key_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[DataFactoryLinkedServiceSftpTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa6e19574f529f5eb20dc2030e2ff298c9ae1c0f103a027d4296f0b7a5a21b14(
    *,
    linked_service_name: builtins.str,
    secret_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92de6688856da263a55dfd4467c3429dfac64bb05a27e676ae131e23ac7048e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5343c6283f703ac0b29f4d26fc5fc1ea1b219f33966e336ac8a4eb9e3a51dff5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee6d488f27bb99289153ddd8046da15a2f261ba4e7a15f0ea12fecae95839b31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22775667f6d072d092f576465d0e8fea5ffb29ba71f7e9c026d5fb6d57f48140(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26d6152e15fc8a55acd4135f30ad48ef4c72dad119982a947b757120f9973fc0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f30842d5d828da4bdb48cf0b0badb867f256c39e9d969ac2e3ad15c3fafb3d77(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryLinkedServiceSftpKeyVaultPassword]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ac88653549d6b3b9b42965edd7d3fecc7a4e1ea938831650e538a68c72cc7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d750359019fb9b97b49f37467daa070fa94dab2b2cfc12f5238910250c7b56f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13a4f43fb008ed2139844b3fb0bf90a826542a24098f0dd597ea27f45c0450bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a32757d2572d16c7d7ac108d80c0fb7549c66723cd330b059b31f0e6ad0fbcb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryLinkedServiceSftpKeyVaultPassword]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35f214141af3fcb404979f3b5fee1aea448815b4fb501c503f5cc4d03b18e903(
    *,
    linked_service_name: builtins.str,
    secret_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39e41347b0bb49c687e2d34666b6f52c1b34c30681b2db2c43c23a3ed0e1791b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5273e707a65c2d01a98857b8c7df89029fbb1e92eb8479fafebf40d5d8dd1e60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa62f8ed787cb24873c09c6851d7241ca4b63e5c2b735665a8cf6885366c534d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0754811932eb06561fd29c736abfca5a9b0b34c9676e489c4d2db2abf184ca3(
    value: typing.Optional[DataFactoryLinkedServiceSftpKeyVaultPrivateKeyContentBase64],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3b9ba696b2255c21de148843104b41e8af05be3ebffd837060d5231f27c6087(
    *,
    linked_service_name: builtins.str,
    secret_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b74f5be6a48827def1f998955c605ad4813e1f200c5ba00dd61a00eb9288d12d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740b02aa7d44cd725c4d971655b774bfc5f0ded2a568f2e5ff4c6a0803d27410(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf281ba5f2992191d7998ce5247687b619d67b8aed3eea2ced83618f1576f58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__881c3c09b5b5dfc1ee9fa8995a4ea07f46cc52cbe2e6d0be61490072f3d5a597(
    value: typing.Optional[DataFactoryLinkedServiceSftpKeyVaultPrivateKeyPassphrase],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__334ed2fb7d38acf9797cc644755c76ed603bbcae961ccc6455103adce4d32144(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a20fcb973551c482c3419a2c81dd8d0507f21251a112ec4a93815a394716ad16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b57511fe206b12653e7d44d4b4f5fad988e30d9cc251a452921b3caad7f8f51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0bc7b5ca1ba1572726ed980f519896b8d7cd7af7abcada6c238a024ca9245c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad828caa58bb2b07560d85b82af0f2179fc1bc43dcd5adb130caca9cdad4cba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__148e186359a77def962a64393c1cabc69d8277e133c205571f87d3ef3ddbd0ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056e35433b349ea1170061cf0f27199c334ac5f13da02ed959bbdbd24bb48c58(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryLinkedServiceSftpTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
