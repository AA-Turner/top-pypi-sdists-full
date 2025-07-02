r'''
# `azurerm_data_factory_linked_service_azure_sql_database`

Refer to the Terraform Registry for docs: [`azurerm_data_factory_linked_service_azure_sql_database`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database).
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


class DataFactoryLinkedServiceAzureSqlDatabase(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceAzureSqlDatabase.DataFactoryLinkedServiceAzureSqlDatabase",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database azurerm_data_factory_linked_service_azure_sql_database}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        data_factory_id: builtins.str,
        name: builtins.str,
        additional_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        annotations: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection_string: typing.Optional[builtins.str] = None,
        credential_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        integration_runtime_name: typing.Optional[builtins.str] = None,
        key_vault_connection_string: typing.Optional[typing.Union["DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultConnectionString", typing.Dict[builtins.str, typing.Any]]] = None,
        key_vault_password: typing.Optional[typing.Union["DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultPassword", typing.Dict[builtins.str, typing.Any]]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        service_principal_id: typing.Optional[builtins.str] = None,
        service_principal_key: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataFactoryLinkedServiceAzureSqlDatabaseTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        use_managed_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database azurerm_data_factory_linked_service_azure_sql_database} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_factory_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#data_factory_id DataFactoryLinkedServiceAzureSqlDatabase#data_factory_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#name DataFactoryLinkedServiceAzureSqlDatabase#name}.
        :param additional_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#additional_properties DataFactoryLinkedServiceAzureSqlDatabase#additional_properties}.
        :param annotations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#annotations DataFactoryLinkedServiceAzureSqlDatabase#annotations}.
        :param connection_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#connection_string DataFactoryLinkedServiceAzureSqlDatabase#connection_string}.
        :param credential_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#credential_name DataFactoryLinkedServiceAzureSqlDatabase#credential_name}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#description DataFactoryLinkedServiceAzureSqlDatabase#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#id DataFactoryLinkedServiceAzureSqlDatabase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param integration_runtime_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#integration_runtime_name DataFactoryLinkedServiceAzureSqlDatabase#integration_runtime_name}.
        :param key_vault_connection_string: key_vault_connection_string block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#key_vault_connection_string DataFactoryLinkedServiceAzureSqlDatabase#key_vault_connection_string}
        :param key_vault_password: key_vault_password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#key_vault_password DataFactoryLinkedServiceAzureSqlDatabase#key_vault_password}
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#parameters DataFactoryLinkedServiceAzureSqlDatabase#parameters}.
        :param service_principal_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#service_principal_id DataFactoryLinkedServiceAzureSqlDatabase#service_principal_id}.
        :param service_principal_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#service_principal_key DataFactoryLinkedServiceAzureSqlDatabase#service_principal_key}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#tenant_id DataFactoryLinkedServiceAzureSqlDatabase#tenant_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#timeouts DataFactoryLinkedServiceAzureSqlDatabase#timeouts}
        :param use_managed_identity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#use_managed_identity DataFactoryLinkedServiceAzureSqlDatabase#use_managed_identity}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efaf2b60c0f429183fdacd337f87afaf772368ee0e0a9fd3d8da37d71e24e518)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataFactoryLinkedServiceAzureSqlDatabaseConfig(
            data_factory_id=data_factory_id,
            name=name,
            additional_properties=additional_properties,
            annotations=annotations,
            connection_string=connection_string,
            credential_name=credential_name,
            description=description,
            id=id,
            integration_runtime_name=integration_runtime_name,
            key_vault_connection_string=key_vault_connection_string,
            key_vault_password=key_vault_password,
            parameters=parameters,
            service_principal_id=service_principal_id,
            service_principal_key=service_principal_key,
            tenant_id=tenant_id,
            timeouts=timeouts,
            use_managed_identity=use_managed_identity,
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
        '''Generates CDKTF code for importing a DataFactoryLinkedServiceAzureSqlDatabase resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataFactoryLinkedServiceAzureSqlDatabase to import.
        :param import_from_id: The id of the existing DataFactoryLinkedServiceAzureSqlDatabase that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataFactoryLinkedServiceAzureSqlDatabase to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c5873eb9e102cb244a6d48420bcb20e2de29e96395a5c55f3316d259639803a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putKeyVaultConnectionString")
    def put_key_vault_connection_string(
        self,
        *,
        linked_service_name: builtins.str,
        secret_name: builtins.str,
    ) -> None:
        '''
        :param linked_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#linked_service_name DataFactoryLinkedServiceAzureSqlDatabase#linked_service_name}.
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#secret_name DataFactoryLinkedServiceAzureSqlDatabase#secret_name}.
        '''
        value = DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultConnectionString(
            linked_service_name=linked_service_name, secret_name=secret_name
        )

        return typing.cast(None, jsii.invoke(self, "putKeyVaultConnectionString", [value]))

    @jsii.member(jsii_name="putKeyVaultPassword")
    def put_key_vault_password(
        self,
        *,
        linked_service_name: builtins.str,
        secret_name: builtins.str,
    ) -> None:
        '''
        :param linked_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#linked_service_name DataFactoryLinkedServiceAzureSqlDatabase#linked_service_name}.
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#secret_name DataFactoryLinkedServiceAzureSqlDatabase#secret_name}.
        '''
        value = DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultPassword(
            linked_service_name=linked_service_name, secret_name=secret_name
        )

        return typing.cast(None, jsii.invoke(self, "putKeyVaultPassword", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#create DataFactoryLinkedServiceAzureSqlDatabase#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#delete DataFactoryLinkedServiceAzureSqlDatabase#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#read DataFactoryLinkedServiceAzureSqlDatabase#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#update DataFactoryLinkedServiceAzureSqlDatabase#update}.
        '''
        value = DataFactoryLinkedServiceAzureSqlDatabaseTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdditionalProperties")
    def reset_additional_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalProperties", []))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetConnectionString")
    def reset_connection_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionString", []))

    @jsii.member(jsii_name="resetCredentialName")
    def reset_credential_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentialName", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIntegrationRuntimeName")
    def reset_integration_runtime_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegrationRuntimeName", []))

    @jsii.member(jsii_name="resetKeyVaultConnectionString")
    def reset_key_vault_connection_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultConnectionString", []))

    @jsii.member(jsii_name="resetKeyVaultPassword")
    def reset_key_vault_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultPassword", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetServicePrincipalId")
    def reset_service_principal_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServicePrincipalId", []))

    @jsii.member(jsii_name="resetServicePrincipalKey")
    def reset_service_principal_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServicePrincipalKey", []))

    @jsii.member(jsii_name="resetTenantId")
    def reset_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUseManagedIdentity")
    def reset_use_managed_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseManagedIdentity", []))

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
    @jsii.member(jsii_name="keyVaultConnectionString")
    def key_vault_connection_string(
        self,
    ) -> "DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultConnectionStringOutputReference":
        return typing.cast("DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultConnectionStringOutputReference", jsii.get(self, "keyVaultConnectionString"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultPassword")
    def key_vault_password(
        self,
    ) -> "DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultPasswordOutputReference":
        return typing.cast("DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultPasswordOutputReference", jsii.get(self, "keyVaultPassword"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "DataFactoryLinkedServiceAzureSqlDatabaseTimeoutsOutputReference":
        return typing.cast("DataFactoryLinkedServiceAzureSqlDatabaseTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    @jsii.member(jsii_name="connectionStringInput")
    def connection_string_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionStringInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialNameInput")
    def credential_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dataFactoryIdInput")
    def data_factory_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataFactoryIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="integrationRuntimeNameInput")
    def integration_runtime_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integrationRuntimeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultConnectionStringInput")
    def key_vault_connection_string_input(
        self,
    ) -> typing.Optional["DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultConnectionString"]:
        return typing.cast(typing.Optional["DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultConnectionString"], jsii.get(self, "keyVaultConnectionStringInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultPasswordInput")
    def key_vault_password_input(
        self,
    ) -> typing.Optional["DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultPassword"]:
        return typing.cast(typing.Optional["DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultPassword"], jsii.get(self, "keyVaultPasswordInput"))

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
    @jsii.member(jsii_name="servicePrincipalIdInput")
    def service_principal_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "servicePrincipalIdInput"))

    @builtins.property
    @jsii.member(jsii_name="servicePrincipalKeyInput")
    def service_principal_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "servicePrincipalKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataFactoryLinkedServiceAzureSqlDatabaseTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataFactoryLinkedServiceAzureSqlDatabaseTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="useManagedIdentityInput")
    def use_managed_identity_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useManagedIdentityInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9e141e1d2cedd83fc22848d831e59b587963a739d96998484fd468395a7b2b56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25c7dc83134a2e1ec42f39a8c92a2a5ea461ab4eb4c37f0bb319c55fce22037b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectionString")
    def connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionString"))

    @connection_string.setter
    def connection_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4dd79b179d770d2cad04720bb22d52857cec6ccdb6de72956cbbcc0eb234f45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="credentialName")
    def credential_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentialName"))

    @credential_name.setter
    def credential_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__306b929db938d8f6ca3576a6f8539389b94e16620cc123968b9954dc40332413)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentialName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataFactoryId")
    def data_factory_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataFactoryId"))

    @data_factory_id.setter
    def data_factory_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6946544b793d9e6abce257c07e42250a623d0c75622c12adefde5e1c6ff3d823)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataFactoryId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9cfab2f31982e51aacf48c730003579342cb31e96fec4cda244d4fdf1318298)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a6587e1222780d652f29a04067b1f7582398bcb74aea46979f1a1d229a18e2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integrationRuntimeName")
    def integration_runtime_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "integrationRuntimeName"))

    @integration_runtime_name.setter
    def integration_runtime_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92117a4d00155faf2ee9dd537797589b5a4f02de5ec2666ba82a5c40eadc20c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationRuntimeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eacd40e48deb77eac3f9e8e7195e0ed16d1d99dd69f5fa07d98d668d2e2141e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ec47ee11e31144c579e7f741d21113016973e58e6951c184fffb30866caffda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servicePrincipalId")
    def service_principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servicePrincipalId"))

    @service_principal_id.setter
    def service_principal_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bbd029132647f734a14d5478cbf18d1147f27498e197c8d76a47925a89b7766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servicePrincipalId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servicePrincipalKey")
    def service_principal_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servicePrincipalKey"))

    @service_principal_key.setter
    def service_principal_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__192408d8e1921ef1c07da439f9fcca4dc229c6b576fc95706c68661229eca83f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servicePrincipalKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b5f0be4b4bb70556cbae8b1cf9caf571fffa26c4073bb929ff9df2677cb8764)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useManagedIdentity")
    def use_managed_identity(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useManagedIdentity"))

    @use_managed_identity.setter
    def use_managed_identity(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__956b66949292efa67fcf343e39408619473e22bb12b502c1ff6862ddd65abf96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useManagedIdentity", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceAzureSqlDatabase.DataFactoryLinkedServiceAzureSqlDatabaseConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "data_factory_id": "dataFactoryId",
        "name": "name",
        "additional_properties": "additionalProperties",
        "annotations": "annotations",
        "connection_string": "connectionString",
        "credential_name": "credentialName",
        "description": "description",
        "id": "id",
        "integration_runtime_name": "integrationRuntimeName",
        "key_vault_connection_string": "keyVaultConnectionString",
        "key_vault_password": "keyVaultPassword",
        "parameters": "parameters",
        "service_principal_id": "servicePrincipalId",
        "service_principal_key": "servicePrincipalKey",
        "tenant_id": "tenantId",
        "timeouts": "timeouts",
        "use_managed_identity": "useManagedIdentity",
    },
)
class DataFactoryLinkedServiceAzureSqlDatabaseConfig(
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
        data_factory_id: builtins.str,
        name: builtins.str,
        additional_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        annotations: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection_string: typing.Optional[builtins.str] = None,
        credential_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        integration_runtime_name: typing.Optional[builtins.str] = None,
        key_vault_connection_string: typing.Optional[typing.Union["DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultConnectionString", typing.Dict[builtins.str, typing.Any]]] = None,
        key_vault_password: typing.Optional[typing.Union["DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultPassword", typing.Dict[builtins.str, typing.Any]]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        service_principal_id: typing.Optional[builtins.str] = None,
        service_principal_key: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataFactoryLinkedServiceAzureSqlDatabaseTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        use_managed_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param data_factory_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#data_factory_id DataFactoryLinkedServiceAzureSqlDatabase#data_factory_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#name DataFactoryLinkedServiceAzureSqlDatabase#name}.
        :param additional_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#additional_properties DataFactoryLinkedServiceAzureSqlDatabase#additional_properties}.
        :param annotations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#annotations DataFactoryLinkedServiceAzureSqlDatabase#annotations}.
        :param connection_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#connection_string DataFactoryLinkedServiceAzureSqlDatabase#connection_string}.
        :param credential_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#credential_name DataFactoryLinkedServiceAzureSqlDatabase#credential_name}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#description DataFactoryLinkedServiceAzureSqlDatabase#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#id DataFactoryLinkedServiceAzureSqlDatabase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param integration_runtime_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#integration_runtime_name DataFactoryLinkedServiceAzureSqlDatabase#integration_runtime_name}.
        :param key_vault_connection_string: key_vault_connection_string block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#key_vault_connection_string DataFactoryLinkedServiceAzureSqlDatabase#key_vault_connection_string}
        :param key_vault_password: key_vault_password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#key_vault_password DataFactoryLinkedServiceAzureSqlDatabase#key_vault_password}
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#parameters DataFactoryLinkedServiceAzureSqlDatabase#parameters}.
        :param service_principal_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#service_principal_id DataFactoryLinkedServiceAzureSqlDatabase#service_principal_id}.
        :param service_principal_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#service_principal_key DataFactoryLinkedServiceAzureSqlDatabase#service_principal_key}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#tenant_id DataFactoryLinkedServiceAzureSqlDatabase#tenant_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#timeouts DataFactoryLinkedServiceAzureSqlDatabase#timeouts}
        :param use_managed_identity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#use_managed_identity DataFactoryLinkedServiceAzureSqlDatabase#use_managed_identity}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(key_vault_connection_string, dict):
            key_vault_connection_string = DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultConnectionString(**key_vault_connection_string)
        if isinstance(key_vault_password, dict):
            key_vault_password = DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultPassword(**key_vault_password)
        if isinstance(timeouts, dict):
            timeouts = DataFactoryLinkedServiceAzureSqlDatabaseTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d60bd269185b88cd46679adf649aa67781198e2cf3dcdde4502279e6d8f53cf6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument data_factory_id", value=data_factory_id, expected_type=type_hints["data_factory_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument additional_properties", value=additional_properties, expected_type=type_hints["additional_properties"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument connection_string", value=connection_string, expected_type=type_hints["connection_string"])
            check_type(argname="argument credential_name", value=credential_name, expected_type=type_hints["credential_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument integration_runtime_name", value=integration_runtime_name, expected_type=type_hints["integration_runtime_name"])
            check_type(argname="argument key_vault_connection_string", value=key_vault_connection_string, expected_type=type_hints["key_vault_connection_string"])
            check_type(argname="argument key_vault_password", value=key_vault_password, expected_type=type_hints["key_vault_password"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument service_principal_id", value=service_principal_id, expected_type=type_hints["service_principal_id"])
            check_type(argname="argument service_principal_key", value=service_principal_key, expected_type=type_hints["service_principal_key"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument use_managed_identity", value=use_managed_identity, expected_type=type_hints["use_managed_identity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_factory_id": data_factory_id,
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
        if additional_properties is not None:
            self._values["additional_properties"] = additional_properties
        if annotations is not None:
            self._values["annotations"] = annotations
        if connection_string is not None:
            self._values["connection_string"] = connection_string
        if credential_name is not None:
            self._values["credential_name"] = credential_name
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if integration_runtime_name is not None:
            self._values["integration_runtime_name"] = integration_runtime_name
        if key_vault_connection_string is not None:
            self._values["key_vault_connection_string"] = key_vault_connection_string
        if key_vault_password is not None:
            self._values["key_vault_password"] = key_vault_password
        if parameters is not None:
            self._values["parameters"] = parameters
        if service_principal_id is not None:
            self._values["service_principal_id"] = service_principal_id
        if service_principal_key is not None:
            self._values["service_principal_key"] = service_principal_key
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if use_managed_identity is not None:
            self._values["use_managed_identity"] = use_managed_identity

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
    def data_factory_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#data_factory_id DataFactoryLinkedServiceAzureSqlDatabase#data_factory_id}.'''
        result = self._values.get("data_factory_id")
        assert result is not None, "Required property 'data_factory_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#name DataFactoryLinkedServiceAzureSqlDatabase#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#additional_properties DataFactoryLinkedServiceAzureSqlDatabase#additional_properties}.'''
        result = self._values.get("additional_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def annotations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#annotations DataFactoryLinkedServiceAzureSqlDatabase#annotations}.'''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def connection_string(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#connection_string DataFactoryLinkedServiceAzureSqlDatabase#connection_string}.'''
        result = self._values.get("connection_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def credential_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#credential_name DataFactoryLinkedServiceAzureSqlDatabase#credential_name}.'''
        result = self._values.get("credential_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#description DataFactoryLinkedServiceAzureSqlDatabase#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#id DataFactoryLinkedServiceAzureSqlDatabase#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def integration_runtime_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#integration_runtime_name DataFactoryLinkedServiceAzureSqlDatabase#integration_runtime_name}.'''
        result = self._values.get("integration_runtime_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_connection_string(
        self,
    ) -> typing.Optional["DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultConnectionString"]:
        '''key_vault_connection_string block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#key_vault_connection_string DataFactoryLinkedServiceAzureSqlDatabase#key_vault_connection_string}
        '''
        result = self._values.get("key_vault_connection_string")
        return typing.cast(typing.Optional["DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultConnectionString"], result)

    @builtins.property
    def key_vault_password(
        self,
    ) -> typing.Optional["DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultPassword"]:
        '''key_vault_password block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#key_vault_password DataFactoryLinkedServiceAzureSqlDatabase#key_vault_password}
        '''
        result = self._values.get("key_vault_password")
        return typing.cast(typing.Optional["DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultPassword"], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#parameters DataFactoryLinkedServiceAzureSqlDatabase#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def service_principal_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#service_principal_id DataFactoryLinkedServiceAzureSqlDatabase#service_principal_id}.'''
        result = self._values.get("service_principal_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_principal_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#service_principal_key DataFactoryLinkedServiceAzureSqlDatabase#service_principal_key}.'''
        result = self._values.get("service_principal_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#tenant_id DataFactoryLinkedServiceAzureSqlDatabase#tenant_id}.'''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["DataFactoryLinkedServiceAzureSqlDatabaseTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#timeouts DataFactoryLinkedServiceAzureSqlDatabase#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataFactoryLinkedServiceAzureSqlDatabaseTimeouts"], result)

    @builtins.property
    def use_managed_identity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#use_managed_identity DataFactoryLinkedServiceAzureSqlDatabase#use_managed_identity}.'''
        result = self._values.get("use_managed_identity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryLinkedServiceAzureSqlDatabaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceAzureSqlDatabase.DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultConnectionString",
    jsii_struct_bases=[],
    name_mapping={
        "linked_service_name": "linkedServiceName",
        "secret_name": "secretName",
    },
)
class DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultConnectionString:
    def __init__(
        self,
        *,
        linked_service_name: builtins.str,
        secret_name: builtins.str,
    ) -> None:
        '''
        :param linked_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#linked_service_name DataFactoryLinkedServiceAzureSqlDatabase#linked_service_name}.
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#secret_name DataFactoryLinkedServiceAzureSqlDatabase#secret_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69e2e0938f9f42b8fb37b178473ca212a37b21cac6e10ccee6e3121f2828e3b6)
            check_type(argname="argument linked_service_name", value=linked_service_name, expected_type=type_hints["linked_service_name"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "linked_service_name": linked_service_name,
            "secret_name": secret_name,
        }

    @builtins.property
    def linked_service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#linked_service_name DataFactoryLinkedServiceAzureSqlDatabase#linked_service_name}.'''
        result = self._values.get("linked_service_name")
        assert result is not None, "Required property 'linked_service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#secret_name DataFactoryLinkedServiceAzureSqlDatabase#secret_name}.'''
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultConnectionString(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultConnectionStringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceAzureSqlDatabase.DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultConnectionStringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f9fdf905d4dd7a048be6ad95ab69ba6349e1ac93e777a34f3ebaf38e4a78342)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1eeeb45b3d422d27f64f457b716336d61ce32e31f954a70a68b4b24b68778b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkedServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17499fc93af59bd2ded1123b3ecac4431c986d56d785df637654eaa73a6c27c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultConnectionString]:
        return typing.cast(typing.Optional[DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultConnectionString], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultConnectionString],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39d4a61334528fb2a6d70b066ef0ce288f7584193a7226e8ef20c7d8053a70f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceAzureSqlDatabase.DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultPassword",
    jsii_struct_bases=[],
    name_mapping={
        "linked_service_name": "linkedServiceName",
        "secret_name": "secretName",
    },
)
class DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultPassword:
    def __init__(
        self,
        *,
        linked_service_name: builtins.str,
        secret_name: builtins.str,
    ) -> None:
        '''
        :param linked_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#linked_service_name DataFactoryLinkedServiceAzureSqlDatabase#linked_service_name}.
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#secret_name DataFactoryLinkedServiceAzureSqlDatabase#secret_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59c5e39fda605ddab8fd4f217a8f8ebfd2f548039b8242cebf7ba05d2de5c64e)
            check_type(argname="argument linked_service_name", value=linked_service_name, expected_type=type_hints["linked_service_name"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "linked_service_name": linked_service_name,
            "secret_name": secret_name,
        }

    @builtins.property
    def linked_service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#linked_service_name DataFactoryLinkedServiceAzureSqlDatabase#linked_service_name}.'''
        result = self._values.get("linked_service_name")
        assert result is not None, "Required property 'linked_service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#secret_name DataFactoryLinkedServiceAzureSqlDatabase#secret_name}.'''
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultPassword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultPasswordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceAzureSqlDatabase.DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultPasswordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc700531f833055e60ba376d675925a0b39f96794c498e16535222ee14666467)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f9a30d3a4048348d14a0723fd4044a7132304e7cc26a2c4eef5141aaef7d4ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkedServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbe4f86ce0ee4f8a794688cc5a2f550e34387d0c6acc3b82390a51480a0afbf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultPassword]:
        return typing.cast(typing.Optional[DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultPassword], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultPassword],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cdb85dc9c9ef5644502db34ea36e163e25fb9aa89c25fa892ef7dae0ddbc304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceAzureSqlDatabase.DataFactoryLinkedServiceAzureSqlDatabaseTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class DataFactoryLinkedServiceAzureSqlDatabaseTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#create DataFactoryLinkedServiceAzureSqlDatabase#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#delete DataFactoryLinkedServiceAzureSqlDatabase#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#read DataFactoryLinkedServiceAzureSqlDatabase#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#update DataFactoryLinkedServiceAzureSqlDatabase#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00d0b5bdf244efdcdde4c06be45ee2dd51c183fb3ce5b87a1ffed432dbd47af5)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#create DataFactoryLinkedServiceAzureSqlDatabase#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#delete DataFactoryLinkedServiceAzureSqlDatabase#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#read DataFactoryLinkedServiceAzureSqlDatabase#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_sql_database#update DataFactoryLinkedServiceAzureSqlDatabase#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryLinkedServiceAzureSqlDatabaseTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryLinkedServiceAzureSqlDatabaseTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceAzureSqlDatabase.DataFactoryLinkedServiceAzureSqlDatabaseTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a427d6606f10b021ca6478158e2af8ea927c36839578dace0809d82bf646e0c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6689952d08fe82d15004e36836a74e725e8d9c06fbb33ccd096d6f45b418a40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__babd5f509feecd766d261d35a62aa831bcad3e6773303dc0ea46dc20db08c85f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b6edbd79a556f9872078c1e377c625140852497aa428c0977f3a423cbf0cf25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8792784179e396b3438c08c0e28b1234ee20cfba68b15758384eb373d6c91d38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryLinkedServiceAzureSqlDatabaseTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryLinkedServiceAzureSqlDatabaseTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryLinkedServiceAzureSqlDatabaseTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d0e0e2464f3a400a87206530364aea50dcfec61b0bfaa8cf1b7e0d54dae4617)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataFactoryLinkedServiceAzureSqlDatabase",
    "DataFactoryLinkedServiceAzureSqlDatabaseConfig",
    "DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultConnectionString",
    "DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultConnectionStringOutputReference",
    "DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultPassword",
    "DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultPasswordOutputReference",
    "DataFactoryLinkedServiceAzureSqlDatabaseTimeouts",
    "DataFactoryLinkedServiceAzureSqlDatabaseTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__efaf2b60c0f429183fdacd337f87afaf772368ee0e0a9fd3d8da37d71e24e518(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    data_factory_id: builtins.str,
    name: builtins.str,
    additional_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    annotations: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection_string: typing.Optional[builtins.str] = None,
    credential_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    integration_runtime_name: typing.Optional[builtins.str] = None,
    key_vault_connection_string: typing.Optional[typing.Union[DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultConnectionString, typing.Dict[builtins.str, typing.Any]]] = None,
    key_vault_password: typing.Optional[typing.Union[DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultPassword, typing.Dict[builtins.str, typing.Any]]] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    service_principal_id: typing.Optional[builtins.str] = None,
    service_principal_key: typing.Optional[builtins.str] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataFactoryLinkedServiceAzureSqlDatabaseTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    use_managed_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__4c5873eb9e102cb244a6d48420bcb20e2de29e96395a5c55f3316d259639803a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e141e1d2cedd83fc22848d831e59b587963a739d96998484fd468395a7b2b56(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25c7dc83134a2e1ec42f39a8c92a2a5ea461ab4eb4c37f0bb319c55fce22037b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4dd79b179d770d2cad04720bb22d52857cec6ccdb6de72956cbbcc0eb234f45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__306b929db938d8f6ca3576a6f8539389b94e16620cc123968b9954dc40332413(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6946544b793d9e6abce257c07e42250a623d0c75622c12adefde5e1c6ff3d823(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9cfab2f31982e51aacf48c730003579342cb31e96fec4cda244d4fdf1318298(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a6587e1222780d652f29a04067b1f7582398bcb74aea46979f1a1d229a18e2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92117a4d00155faf2ee9dd537797589b5a4f02de5ec2666ba82a5c40eadc20c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eacd40e48deb77eac3f9e8e7195e0ed16d1d99dd69f5fa07d98d668d2e2141e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec47ee11e31144c579e7f741d21113016973e58e6951c184fffb30866caffda(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bbd029132647f734a14d5478cbf18d1147f27498e197c8d76a47925a89b7766(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__192408d8e1921ef1c07da439f9fcca4dc229c6b576fc95706c68661229eca83f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b5f0be4b4bb70556cbae8b1cf9caf571fffa26c4073bb929ff9df2677cb8764(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__956b66949292efa67fcf343e39408619473e22bb12b502c1ff6862ddd65abf96(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d60bd269185b88cd46679adf649aa67781198e2cf3dcdde4502279e6d8f53cf6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_factory_id: builtins.str,
    name: builtins.str,
    additional_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    annotations: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection_string: typing.Optional[builtins.str] = None,
    credential_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    integration_runtime_name: typing.Optional[builtins.str] = None,
    key_vault_connection_string: typing.Optional[typing.Union[DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultConnectionString, typing.Dict[builtins.str, typing.Any]]] = None,
    key_vault_password: typing.Optional[typing.Union[DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultPassword, typing.Dict[builtins.str, typing.Any]]] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    service_principal_id: typing.Optional[builtins.str] = None,
    service_principal_key: typing.Optional[builtins.str] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataFactoryLinkedServiceAzureSqlDatabaseTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    use_managed_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69e2e0938f9f42b8fb37b178473ca212a37b21cac6e10ccee6e3121f2828e3b6(
    *,
    linked_service_name: builtins.str,
    secret_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f9fdf905d4dd7a048be6ad95ab69ba6349e1ac93e777a34f3ebaf38e4a78342(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1eeeb45b3d422d27f64f457b716336d61ce32e31f954a70a68b4b24b68778b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17499fc93af59bd2ded1123b3ecac4431c986d56d785df637654eaa73a6c27c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d4a61334528fb2a6d70b066ef0ce288f7584193a7226e8ef20c7d8053a70f5(
    value: typing.Optional[DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultConnectionString],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c5e39fda605ddab8fd4f217a8f8ebfd2f548039b8242cebf7ba05d2de5c64e(
    *,
    linked_service_name: builtins.str,
    secret_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc700531f833055e60ba376d675925a0b39f96794c498e16535222ee14666467(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f9a30d3a4048348d14a0723fd4044a7132304e7cc26a2c4eef5141aaef7d4ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbe4f86ce0ee4f8a794688cc5a2f550e34387d0c6acc3b82390a51480a0afbf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cdb85dc9c9ef5644502db34ea36e163e25fb9aa89c25fa892ef7dae0ddbc304(
    value: typing.Optional[DataFactoryLinkedServiceAzureSqlDatabaseKeyVaultPassword],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00d0b5bdf244efdcdde4c06be45ee2dd51c183fb3ce5b87a1ffed432dbd47af5(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a427d6606f10b021ca6478158e2af8ea927c36839578dace0809d82bf646e0c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6689952d08fe82d15004e36836a74e725e8d9c06fbb33ccd096d6f45b418a40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__babd5f509feecd766d261d35a62aa831bcad3e6773303dc0ea46dc20db08c85f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6edbd79a556f9872078c1e377c625140852497aa428c0977f3a423cbf0cf25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8792784179e396b3438c08c0e28b1234ee20cfba68b15758384eb373d6c91d38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d0e0e2464f3a400a87206530364aea50dcfec61b0bfaa8cf1b7e0d54dae4617(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryLinkedServiceAzureSqlDatabaseTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
